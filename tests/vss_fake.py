"""Fake VSS transport for adapter tests. Shapes copied from live team-31 responses."""
import io
import json
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend" / "intelligence"))

from vss.client import RawResponse, TransportError, VSSClient, VSSConfig  # noqa: E402

PASSWORD = "s3cret-pass"
CFG = VSSConfig("http://vss.test", "team-31", PASSWORD)
PARENT_A = "s3://team-31-vss-chunks/team-31/a.mp4"
PARENT_B = "s3://team-31-vss-chunks/team-31/b.mp4"


def seg_row(parent, n, **extra):
    stem = parent.rsplit("/", 1)[1][:-4]
    row = {
        "filename": f"{stem}_segment_{n:03d}_of_002.mp4",
        "source": f"s3://team-31-vss-chunks-segments/segments/{stem}_segment_{n:03d}_of_002.mp4",
        "reasoning_content": f"smoke rises in segment {n}",
        "segment_number": n, "total_segments": 2,
        "segment_start_sec": (n - 1) * 5.0, "segment_end_sec": n * 5.0, "duration": 5.0,
        "original_video": parent, "object_classes": "car,person", "object_counts": '{"car": 2}',
        "upload_timestamp": "2026-10-17T10:58:38", "camera_id": "cam-1", "capture_type": "general",
        "location": "holy_fire_2018", "cosmos_model": "nvidia/cosmos3-nano-reasoner",
        "similarity_score": 0.5,
        "extra_metadata": '{"stream_id": "s-1", "chunk_index": 3, "chunk_start_sec": 90.0}',
    }
    row.update(extra)
    return row


def chunk_row(parent):
    return {"original_video": parent, "filename": parent.rsplit("/", 1)[1], "chunk_duration_sec": 10.0,
            "total_segments": 2, "best_segment_number": 2, "best_match_start_sec": 5.0,
            "best_match_end_sec": 10.0, "preview_source": seg_row(parent, 2)["source"],
            "similarity_score": 0.5, "reasoning_content": "smoke", "upload_timestamp": "2026-10-17T10:58:38",
            "camera_id": "cam-1", "location": "holy_fire_2018", "matched_segment_count": 1}


def resp(status, payload=None, headers=None, raw=None):
    body = raw if raw is not None else json.dumps(payload).encode()
    return RawResponse(status, {k.lower(): v for k, v in (headers or {}).items()}, body=body)


class FakeVSS:
    """Callable transport. `routes` maps (method, path) to a function(query, headers, body) -> RawResponse."""

    VIDEO = bytes(range(256)) * 4  # 1024 bytes

    def __init__(self):
        self.calls = []
        self.logins = 0
        self.valid_tokens = {"tok-1"}
        self.next_token = 1
        self.routes = {
            ("POST", "/api/v1/auth/login"): self.login,
            ("GET", "/api/v1/auth/me"): lambda q, h, b: resp(200, {"username": "team-31", "email": None}),
            ("GET", "/api/v1/metadata/schema"): lambda q, h, b: resp(200, {"schema": [
                {"name": "camera_id", "options": ["cam-1"]}, {"name": "location", "options": ["holy_fire_2018"]}]}),
            ("POST", "/api/v1/search"): lambda q, h, b: resp(200, {
                "results": [seg_row(PARENT_A, 2), seg_row(PARENT_B, 1)],
                "chunk_results": [chunk_row(PARENT_A), chunk_row(PARENT_B)], "total": 2}),
            ("GET", "/api/v1/tools/segments"): lambda q, h, b: resp(200, {
                "original_video": q["original_video"], "segments": [seg_row(q["original_video"], 2), seg_row(q["original_video"], 1)]}),
            ("GET", "/api/v1/tools/segment"): self.segment,
            ("GET", "/api/v1/videos/detections"): lambda q, h, b: resp(200, {"frames": [], "fps": 1.0}),
            ("GET", "/api/v1/videos/stream"): self.stream,
        }

    def login(self, q, h, b):
        self.logins += 1
        creds = json.loads(b)
        if creds["password"] != PASSWORD:
            return resp(401, {"detail": "Invalid username or password"})
        token = f"tok-{self.next_token}"
        self.next_token += 1
        self.valid_tokens.add(token)
        return resp(200, {"access_token": token, "token_type": "bearer", "username": "team-31"})

    def segment(self, q, h, b):
        for parent in (PARENT_A, PARENT_B):
            for n in (1, 2):
                if seg_row(parent, n)["source"] == q["source"]:
                    return resp(200, {"segment": seg_row(parent, n)})
        return resp(404, {"detail": "Segment not found"})

    def stream(self, q, h, b):
        if "missing" in q["source"]:
            return resp(500, {"detail": "Failed to stream video: An error occurred (404) when calling the HeadObject operation: Not Found"})
        size = len(self.VIDEO)
        rng = h.get("Range")
        if not rng:
            return RawResponse(200, {"content-length": str(size), "accept-ranges": "bytes"}, stream=io.BytesIO(self.VIDEO))
        start, end = rng.removeprefix("bytes=").split("-")
        start = int(start)
        if start >= size:
            return resp(416, raw=b"", headers={"content-range": f"bytes */{size}"})
        end = min(int(end) if end else size - 1, size - 1)
        part = self.VIDEO[start:end + 1]
        return RawResponse(206, {"content-length": str(len(part)), "content-range": f"bytes {start}-{end}/{size}",
                                 "accept-ranges": "bytes"}, stream=io.BytesIO(part))

    def __call__(self, method, url, headers, body, timeout, stream):
        parts = urlsplit(url)
        query = {k: v[0] for k, v in parse_qs(parts.query).items()}
        self.calls.append((method, parts.path, query, dict(headers)))
        if parts.path != "/api/v1/auth/login":
            token = query.get("token") or headers.get("Authorization", "").removeprefix("Bearer ")
            if token not in self.valid_tokens:
                return resp(401, {"detail": "Invalid token"})
        handler = self.routes.get((method, parts.path))
        if handler is None:
            return resp(404, {"detail": "Not Found"})
        result = handler(query, headers, body)
        if isinstance(result, Exception):
            raise result
        return result

    def paths(self):
        return [p for _, p, _, _ in self.calls]


def make_client(fake=None, **kw):
    fake = fake or FakeVSS()
    kw.setdefault("sleep", lambda s: None)
    return VSSClient(CFG, transport=fake, **kw), fake


__all__ = ["FakeVSS", "make_client", "resp", "seg_row", "chunk_row", "PARENT_A", "PARENT_B", "PASSWORD",
           "CFG", "TransportError", "RawResponse"]
