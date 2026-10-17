import json
import unittest

from vss_fake import (CFG, PARENT_A, PARENT_B, PASSWORD, RawResponse, TransportError, chunk_row, make_client,
                      resp, seg_row)

import vss.client as client_module
from vss.client import AUTH, INVALID_INPUT, MALFORMED, NOT_FOUND, UNAVAILABLE, UPSTREAM, VSSError, config_from_env


class AuthTests(unittest.TestCase):
    def test_logs_in_once_and_sends_bearer_header(self):
        client, fake = make_client()
        client.me()
        client.me()
        self.assertEqual(fake.logins, 1)
        self.assertEqual(fake.calls[-1][3]["Authorization"], "Bearer tok-1")

    def test_expired_token_is_refreshed_once(self):
        client, fake = make_client()
        client.me()
        fake.valid_tokens.discard("tok-1")
        self.assertEqual(client.me(), {"username": "team-31"})
        self.assertEqual(fake.logins, 2)

    def test_rejected_fresh_token_is_auth_error(self):
        client, fake = make_client()
        fake.valid_tokens = set()
        fake.login = lambda q, h, b: resp(200, {"access_token": "never-valid"})
        fake.routes[("POST", "/api/v1/auth/login")] = fake.login
        with self.assertRaises(VSSError) as cm:
            client.me()
        self.assertEqual(cm.exception.kind, AUTH)

    def test_bad_credentials(self):
        client, _ = make_client()
        client._cfg = type(CFG)(CFG.url, CFG.username, "wrong")
        with self.assertRaises(VSSError) as cm:
            client.me()
        self.assertEqual(cm.exception.kind, AUTH)

    def test_config_from_env_fallbacks_and_missing(self):
        cfg = config_from_env({"INGRESS_URL": "http://x/", "USERNAME": "u", "PASSWORD": "pw-xyz"})
        self.assertEqual((cfg.url, cfg.username), ("http://x", "u"))
        self.assertNotIn("pw-xyz", repr(cfg))
        with self.assertRaises(VSSError) as cm:
            config_from_env({"VSS_URL": "http://x"})
        self.assertIn("VSS_PASSWORD", cm.exception.message)


class TransientFailureTests(unittest.TestCase):
    def test_retries_transient_status_then_succeeds(self):
        client, fake = make_client()
        replies = [resp(503, {}), resp(502, {})]
        me = fake.routes[("GET", "/api/v1/auth/me")]
        fake.routes[("GET", "/api/v1/auth/me")] = lambda q, h, b: replies.pop(0) if replies else me(q, h, b)
        self.assertEqual(client.me()["username"], "team-31")

    def test_gives_up_after_retries(self):
        sleeps = []
        client, fake = make_client(sleep=sleeps.append)
        fake.routes[("GET", "/api/v1/auth/me")] = lambda q, h, b: resp(503, {})
        with self.assertRaises(VSSError) as cm:
            client.me()
        self.assertEqual(cm.exception.kind, UNAVAILABLE)
        self.assertEqual(sleeps, [0.5, 1.0])
        self.assertEqual(fake.paths().count("/api/v1/auth/me"), 3)

    def test_connection_failure_is_unavailable_and_redacted(self):
        client, fake = make_client()
        client.me()
        fake.routes[("GET", "/api/v1/auth/me")] = lambda q, h, b: TransportError("ConnectionRefusedError")
        with self.assertRaises(VSSError) as cm:
            client.me()
        self.assertEqual(cm.exception.kind, UNAVAILABLE)
        self.assertNotIn(PASSWORD, str(cm.exception))
        self.assertNotIn("tok-1", str(cm.exception))


class MalformedTests(unittest.TestCase):
    def test_non_json_body(self):
        client, fake = make_client()
        fake.routes[("GET", "/api/v1/auth/me")] = lambda q, h, b: resp(200, raw=b"<html>")
        with self.assertRaises(VSSError) as cm:
            client.me()
        self.assertEqual(cm.exception.kind, MALFORMED)

    def test_segment_without_timing(self):
        client, fake = make_client()
        fake.routes[("GET", "/api/v1/tools/segments")] = lambda q, h, b: resp(200, {
            "segments": [seg_row(PARENT_A, 1, segment_start_sec=None)]})
        with self.assertRaises(VSSError) as cm:
            client.segments(PARENT_A)
        self.assertEqual(cm.exception.kind, MALFORMED)

    def test_missing_top_level_key(self):
        client, fake = make_client()
        fake.routes[("POST", "/api/v1/search")] = lambda q, h, b: resp(200, {"results": []})
        with self.assertRaises(VSSError) as cm:
            client.search("smoke")
        self.assertEqual(cm.exception.kind, MALFORMED)

    def test_bad_embedded_json_fields_become_empty(self):
        client, fake = make_client()
        fake.routes[("GET", "/api/v1/tools/segments")] = lambda q, h, b: resp(200, {
            "segments": [seg_row(PARENT_A, 1, object_counts="{bad", extra_metadata=None, object_classes=None)]})
        seg = client.segments(PARENT_A)[0]
        self.assertEqual((seg["object_counts"], seg["stream_id"], seg["object_classes"]), ({}, None, []))


class NormalizationTests(unittest.TestCase):
    def test_segment_fields(self):
        client, _ = make_client()
        segs = client.segments(PARENT_A)
        self.assertEqual([s["segment_number"] for s in segs], [1, 2])
        s = segs[1]
        self.assertEqual((s["start_s"], s["end_s"], s["duration_s"]), (5.0, 10.0, 5.0))
        self.assertEqual(s["object_classes"], ["car", "person"])
        self.assertEqual(s["object_counts"], {"car": 2})
        self.assertEqual((s["stream_id"], s["chunk_index"], s["chunk_start_s"]), ("s-1", 3, 90.0))
        self.assertEqual(s["description"], "smoke rises in segment 2")
        self.assertEqual(s["ingested_at"], "2026-10-17T10:58:38")


class SearchTests(unittest.TestCase):
    def test_request_body_and_result_shape(self):
        client, fake = make_client()
        r = client.search("  smoke  ", top_k=5, min_similarity=0.3, filters={"location": "holy_fire_2018"})
        self.assertEqual(r["total"], 2)
        self.assertEqual(r["videos"][0]["best_start_s"], 5.0)
        body = [c for c in fake.calls if c[1] == "/api/v1/search"]
        self.assertEqual(len(body), 1)

    def test_empty_results(self):
        client, fake = make_client()
        fake.routes[("POST", "/api/v1/search")] = lambda q, h, b: resp(200, {"results": [], "chunk_results": [], "total": 0})
        self.assertEqual(client.search("nothing"), {"segments": [], "videos": [], "total": 0})

    def test_input_validation_never_reaches_search(self):
        client, fake = make_client()
        for kwargs in ({"query": ""}, {"query": "x", "top_k": 0}, {"query": "x", "top_k": 101},
                       {"query": "x", "top_k": True}, {"query": "x", "filters": {"bogus": "1"}},
                       {"query": "x", "filters": {"location": 3}}, {"query": "x", "filters": ["location"]}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(VSSError) as cm:
                    client.search(**kwargs)
                self.assertEqual(cm.exception.kind, INVALID_INPUT)
        self.assertNotIn("/api/v1/search", fake.paths())

    def test_server_error_detail_is_not_echoed(self):
        client, fake = make_client()
        fake.routes[("POST", "/api/v1/search")] = lambda q, h, b: resp(500, {"detail": "Search failed: SELECT * FROM secret"})
        with self.assertRaises(VSSError) as cm:
            client.search("smoke")
        self.assertEqual(cm.exception.kind, UPSTREAM)
        self.assertNotIn("SELECT", cm.exception.message)

    def test_validation_detail_is_redacted(self):
        client, fake = make_client()
        fake.routes[("POST", "/api/v1/search")] = lambda q, h, b: resp(422, {"detail": f"bad input {PASSWORD} tok-1"})
        with self.assertRaises(VSSError) as cm:
            client.search("smoke")
        self.assertEqual(cm.exception.kind, INVALID_INPUT)
        self.assertNotIn(PASSWORD, cm.exception.message)
        self.assertNotIn("tok-1", cm.exception.message)


class PaginationTests(unittest.TestCase):
    def _explore(self, total, page_size=100):
        offsets = []

        def explore(q, h, b):
            offset = int(q["offset"])
            offsets.append(offset)
            n = max(0, min(page_size, total - offset))
            return resp(200, {"chunks": [chunk_row(f"s3://b/team-31/v{offset + i}.mp4") for i in range(n)],
                              "total": total})
        return explore, offsets

    def test_reads_every_page(self):
        client, fake = make_client()
        fake.routes[("GET", "/api/v1/videos/explore")], offsets = self._explore(250)
        self.assertEqual(len(client.list_videos()), 250)
        self.assertEqual(offsets, [0, 100, 200])

    def test_stops_on_empty_page(self):
        client, fake = make_client()
        fake.routes[("GET", "/api/v1/videos/explore")] = lambda q, h, b: resp(200, {"chunks": [], "total": 999})
        self.assertEqual(client.list_videos(), [])

    def test_runaway_paging_is_malformed(self):
        client, fake = make_client()
        fake.routes[("GET", "/api/v1/videos/explore")] = lambda q, h, b: resp(200, {
            "chunks": [chunk_row(PARENT_A)], "total": 10 ** 9})
        old = client_module.MAX_PAGES
        client_module.MAX_PAGES = 3
        try:
            with self.assertRaises(VSSError) as cm:
                client.list_videos()
        finally:
            client_module.MAX_PAGES = old
        self.assertEqual(cm.exception.kind, MALFORMED)


class MediaTests(unittest.TestCase):
    def test_range_request_uses_query_token(self):
        client, fake = make_client()
        m = client.open_media(seg_row(PARENT_A, 1)["source"], "bytes=10-19")
        data = b"".join(m.chunks())
        m.close()
        self.assertEqual((m.status, len(data)), (206, 10))
        self.assertEqual(m.headers["content-type"], "video/mp4")
        self.assertEqual(m.headers["content-range"], "bytes 10-19/1024")
        _, _, query, headers = fake.calls[-1]
        self.assertEqual(query["token"], "tok-1")
        self.assertNotIn("Authorization", headers)

    def test_unsatisfiable_range(self):
        client, _ = make_client()
        m = client.open_media(PARENT_A, "bytes=5000-")
        self.assertEqual((m.status, m.headers["content-range"]), (416, "bytes */1024"))

    def test_missing_object_500_maps_to_not_found(self):
        client, _ = make_client()
        with self.assertRaises(VSSError) as cm:
            client.open_media("s3://team-31-vss-chunks-segments/segments/missing.mp4")
        self.assertEqual(cm.exception.kind, NOT_FOUND)

    def test_expired_token_refresh_rebuilds_query_token(self):
        client, fake = make_client()
        client.me()
        fake.valid_tokens.discard("tok-1")
        m = client.open_media(PARENT_A, "bytes=0-0")
        m.close()
        self.assertEqual(fake.calls[-1][2]["token"], "tok-2")


class ScopeTests(unittest.TestCase):
    def test_search_drops_out_of_scope_parents(self):
        client, _ = make_client(allowed_parents=[PARENT_A])
        r = client.search("smoke")
        self.assertEqual({s["original_video"] for s in r["segments"]}, {PARENT_A})
        self.assertEqual([v["original_video"] for v in r["videos"]], [PARENT_A])
        self.assertEqual(r["total"], 1)

    def test_out_of_scope_parent_segments_hidden_without_request(self):
        client, fake = make_client(allowed_parents=[PARENT_A])
        with self.assertRaises(VSSError) as cm:
            client.segments(PARENT_B)
        self.assertEqual(cm.exception.kind, NOT_FOUND)
        self.assertNotIn("/api/v1/tools/segments", fake.paths())

    def test_out_of_scope_segment_detections_and_media(self):
        client, _ = make_client(allowed_parents=[PARENT_A])
        other = seg_row(PARENT_B, 1)["source"]
        for call in (lambda: client.segment(other), lambda: client.detections(other),
                     lambda: client.open_media(other), lambda: client.open_media(PARENT_B)):
            with self.assertRaises(VSSError) as cm:
                call()
            self.assertEqual(cm.exception.kind, NOT_FOUND)

    def test_in_scope_segment_media(self):
        client, _ = make_client(allowed_parents=[PARENT_A])
        m = client.open_media(seg_row(PARENT_A, 2)["source"], "bytes=0-3")
        m.close()
        self.assertEqual(m.status, 206)

    def test_list_videos_scoped(self):
        client, fake = make_client(allowed_parents=[PARENT_B])
        fake.routes[("GET", "/api/v1/videos/explore")] = lambda q, h, b: resp(200, {
            "chunks": [chunk_row(PARENT_A), chunk_row(PARENT_B)], "total": 2})
        self.assertEqual([v["original_video"] for v in client.list_videos()], [PARENT_B])


if __name__ == "__main__":
    unittest.main()
