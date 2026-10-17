import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

from vss_fake import PARENT_A, PARENT_B, PASSWORD, make_client, resp, seg_row

from vss.server import make_handler


class ServerTests(unittest.TestCase):
    def setUp(self):
        self.client, self.fake = make_client(allowed_parents=[PARENT_A])
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.client))
        self.server.RequestHandlerClass.log_message = lambda *a: None
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def call(self, path, body=None, headers=None):
        data = json.dumps(body).encode() if isinstance(body, (dict, list)) else body
        req = urllib.request.Request(self.base + path, data=data, headers=headers or {},
                                     method="POST" if data is not None else "GET")
        try:
            r = urllib.request.urlopen(req, timeout=5)
        except urllib.error.HTTPError as e:
            r = e
        with r:
            raw = r.read()
            hdrs = {k.lower(): v for k, v in r.headers.items()}
            status = r.status
        for secret in (PASSWORD, "tok-1"):
            self.assertNotIn(secret.encode(), raw)
        return status, hdrs, raw

    def test_health(self):
        status, _, raw = self.call("/health")
        self.assertEqual((status, json.loads(raw)), (200, {"ok": True}))

    def test_health_reports_login_failure(self):
        self.fake.routes[("POST", "/api/v1/auth/login")] = lambda q, h, b: resp(401, {"detail": "no"})
        status, _, raw = self.call("/health")
        self.assertEqual(status, 503)
        self.assertEqual(json.loads(raw)["error"]["kind"], "auth")

    def test_search_is_scoped(self):
        status, _, raw = self.call("/v1/search", {"query": "smoke", "top_k": 5})
        self.assertEqual(status, 200)
        self.assertEqual({s["original_video"] for s in json.loads(raw)["segments"]}, {PARENT_A})

    def test_search_input_errors(self):
        for body in (b"not json", {"query": "x", "extra": 1}, {"query": ""}, [1]):
            with self.subTest(body=body):
                status, _, raw = self.call("/v1/search", body, {"Content-Type": "application/json"})
                self.assertEqual(status, 400)
                self.assertEqual(json.loads(raw)["error"]["kind"], "invalid_input")

    def test_missing_param_and_unknown_route(self):
        self.assertEqual(self.call("/v1/segment")[0], 400)
        self.assertEqual(self.call("/v1/nope")[0], 404)

    def test_segments_and_out_of_scope(self):
        status, _, raw = self.call(f"/v1/segments?original_video={PARENT_A}")
        self.assertEqual((status, len(json.loads(raw)["segments"])), (200, 2))
        status, _, raw = self.call(f"/v1/segments?original_video={PARENT_B}")
        self.assertEqual((status, json.loads(raw)["error"]["kind"]), (404, "not_found"))

    def test_media_range(self):
        source = seg_row(PARENT_A, 1)["source"]
        status, hdrs, raw = self.call(f"/v1/media?source={source}", headers={"Range": "bytes=0-99"})
        self.assertEqual((status, len(raw)), (206, 100))
        self.assertEqual(hdrs["content-range"], "bytes 0-99/1024")
        self.assertEqual(hdrs["content-type"], "video/mp4")

    def test_media_full_and_416(self):
        status, hdrs, raw = self.call(f"/v1/media?source={PARENT_A}")
        self.assertEqual((status, len(raw), hdrs["content-length"]), (200, 1024, "1024"))
        status, hdrs, _ = self.call(f"/v1/media?source={PARENT_A}", headers={"Range": "bytes=9999-"})
        self.assertEqual((status, hdrs["content-range"]), (416, "bytes */1024"))

    def test_upstream_unavailable(self):
        self.fake.routes[("GET", "/api/v1/tools/segments")] = lambda q, h, b: resp(503, {})
        status, _, raw = self.call(f"/v1/segments?original_video={PARENT_A}")
        self.assertEqual((status, json.loads(raw)["error"]["kind"]), (503, "unavailable"))

    def test_unexpected_exception_is_generic(self):
        self.client.filters = lambda: (_ for _ in ()).throw(RuntimeError(f"boom {PASSWORD}"))
        status, _, raw = self.call("/v1/filters")
        self.assertEqual((status, json.loads(raw)["error"]), (500, {"kind": "internal", "message": "internal error"}))


if __name__ == "__main__":
    unittest.main()
