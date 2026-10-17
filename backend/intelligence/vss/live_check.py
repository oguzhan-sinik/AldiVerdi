"""Read-only checks against the real VSS backend. Prints PASS/FAIL per check, no secrets.

Run on the workshop VM: `python3 -m vss.live_check --config /config/team-31.config`
"""
from __future__ import annotations

import argparse
import sys

from .client import INVALID_INPUT, NOT_FOUND, VSSClient, VSSError, config_from_env, config_from_file


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", help="team config file (KEY=VALUE); default: environment")
    ap.add_argument("--query", default="car driving on a street")
    args = ap.parse_args()
    cfg = config_from_file(args.config) if args.config else config_from_env()
    client = VSSClient(cfg)
    results: list[tuple[str, bool, str]] = []

    def check(name, fn):
        try:
            detail = fn()
            results.append((name, True, detail or ""))
            return True
        except Exception as e:  # report and keep going
            kind = getattr(e, "kind", type(e).__name__)
            results.append((name, False, f"{kind}: {getattr(e, 'message', '')}"))
            return False

    state: dict = {}

    def login():
        return f"user={client.me()['username']}"

    def filters():
        f = client.filters()
        return f"fields={sorted(f)}"

    def videos():
        state["videos"] = client.list_videos()
        return f"{len(state['videos'])} indexed parents (paged)"

    def search():
        r = client.search(args.query, top_k=5, min_similarity=0.1)
        assert r["segments"], "no hits"
        state["seg"] = r["segments"][0]
        return f"{r['total']} hits, top={state['seg']['similarity']:.2f}"

    def segments():
        segs = client.segments(state["seg"]["original_video"])
        assert segs and segs[0]["start_s"] == 0.0, "segments missing or not starting at 0"
        return f"{len(segs)} segments, last ends at {segs[-1]['end_s']}s"

    def segment():
        s = client.segment(state["seg"]["source"])
        assert s["description"], "no description"
        return f"model={s['description_model']}"

    def detections():
        d = client.detections(state["seg"]["source"])
        return f"{len(d['frames'])} frames"

    def media_range():
        m = client.open_media(state["seg"]["source"], "bytes=0-99")
        try:
            data = b"".join(m.chunks())
        finally:
            m.close()
        assert m.status == 206 and len(data) == 100, f"status={m.status} bytes={len(data)}"
        return m.headers.get("content-range")

    def expect_error(kind, fn):
        def run():
            try:
                fn()
            except VSSError as e:
                assert e.kind == kind, f"got {e.kind}"
                return f"{kind} as expected"
            raise AssertionError("no error")
        return run

    def scope():
        parent = state["seg"]["original_video"]
        scoped = VSSClient(cfg, allowed_parents=[parent])
        r = scoped.search(args.query, top_k=10, min_similarity=0.1)
        assert all(s["original_video"] == parent for s in r["segments"]), "out-of-scope hit"
        other = next(v["original_video"] for v in state["videos"] if v["original_video"] != parent)
        try:
            scoped.segments(other)
        except VSSError as e:
            assert e.kind == NOT_FOUND
            return f"{r['total']} in-scope hits; other parent hidden"
        raise AssertionError("other parent visible")

    check("login + /auth/me", login)
    check("filters (metadata/schema)", filters)
    check("list_videos paging", videos)
    if check("search", search):
        check("segments of top parent", segments)
        check("segment", segment)
        check("detections", detections)
        check("media byte range", media_range)
        check("scope isolation", scope)
    check("missing media -> not_found", expect_error(NOT_FOUND, lambda: client.open_media(
        "s3://team-31-vss-chunks-segments/segments/does-not-exist.mp4", "bytes=0-9")))
    check("unknown filter -> invalid_input", expect_error(INVALID_INPUT, lambda: client.search("x", filters={"bogus": "1"})))

    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
    return 0 if all(ok for _, ok, _ in results) else 1


if __name__ == "__main__":
    sys.exit(main())
