"""Internal HTTP service exposing VSSClient to Developer A's server.

Run: `python3 -m vss.server` from backend/intelligence. Binds to 127.0.0.1 unless
VSS_ADAPTER_HOST says otherwise; it is not meant to be reachable from browsers.
"""
from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from .client import (AUTH, INVALID_INPUT, MALFORMED, NOT_FOUND, UNAVAILABLE, UPSTREAM, VSSClient,
                     VSSError, config_from_env)

STATUS = {INVALID_INPUT: 400, NOT_FOUND: 404, AUTH: 502, UNAVAILABLE: 503, MALFORMED: 502, UPSTREAM: 502}
MAX_BODY = 64 * 1024


def make_handler(client: VSSClient):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, fmt, *args):  # path only: no query strings in logs
            sys.stderr.write(f"{self.command} {urlsplit(self.path).path} {args[1] if len(args) > 1 else ''}\n")

        def _json(self, status: int, payload) -> None:
            body = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _fail(self, kind: str, message: str) -> None:
            self._json(STATUS.get(kind, 500), {"error": {"kind": kind, "message": message}})

        def _param(self, name: str, required: bool = True) -> str | None:
            value = parse_qs(urlsplit(self.path).query).get(name, [None])[0]
            if required and not value:
                raise VSSError(INVALID_INPUT, f"missing query parameter: {name}")
            return value

        def _dispatch(self, routes: dict) -> None:
            route = routes.get(urlsplit(self.path).path)
            if route is None:
                return self._fail(NOT_FOUND, "no such route")
            try:
                route()
            except VSSError as e:
                self._fail(e.kind, e.message)
            except (BrokenPipeError, ConnectionResetError):
                pass
            except Exception as e:  # never leak internals to the caller
                sys.stderr.write(f"internal error: {type(e).__name__}\n")
                self._fail("internal", "internal error")

        def do_GET(self) -> None:
            self._dispatch({
                "/health": self._health,
                "/v1/filters": lambda: self._json(200, client.filters()),
                "/v1/videos": lambda: self._json(200, {"videos": client.list_videos(
                    location=self._param("location", False), date=self._param("date", False))}),
                "/v1/segments": lambda: self._json(200, {"segments": client.segments(self._param("original_video"))}),
                "/v1/segment": lambda: self._json(200, client.segment(self._param("source"))),
                "/v1/detections": lambda: self._json(200, client.detections(self._param("source"))),
                "/v1/media": self._media,
            })

        def do_POST(self) -> None:
            self._dispatch({"/v1/search": self._search})

        def _health(self) -> None:
            try:
                client.me()
            except VSSError as e:
                return self._json(503, {"ok": False, "error": {"kind": e.kind, "message": e.message}})
            self._json(200, {"ok": True})

        def _search(self) -> None:
            length = int(self.headers.get("Content-Length") or 0)
            if not 0 < length <= MAX_BODY:
                raise VSSError(INVALID_INPUT, "request body missing or too large")
            try:
                req = json.loads(self.rfile.read(length))
            except ValueError:
                raise VSSError(INVALID_INPUT, "body is not JSON") from None
            if not isinstance(req, dict):
                raise VSSError(INVALID_INPUT, "body must be a JSON object")
            unknown = set(req) - {"query", "top_k", "min_similarity", "filters", "time_filter"}
            if unknown:
                raise VSSError(INVALID_INPUT, f"unknown field(s): {', '.join(sorted(unknown))}")
            self._json(200, client.search(req.get("query"), top_k=req.get("top_k", 15),
                                          min_similarity=req.get("min_similarity"),
                                          filters=req.get("filters"), time_filter=req.get("time_filter")))

        def _media(self) -> None:
            media = client.open_media(self._param("source"), self.headers.get("Range"))
            try:
                self.send_response(media.status)
                for name, value in media.headers.items():
                    self.send_header(name, value)
                if media.status == 416:
                    self.send_header("Content-Length", "0")
                elif "content-length" not in media.headers:
                    self.send_header("Connection", "close")
                    self.close_connection = True
                self.end_headers()
                for chunk in media.chunks():
                    self.wfile.write(chunk)  # raises BrokenPipe when the caller goes away
            finally:
                media.close()

    return Handler


def load_scope(path: str | None) -> list[str] | None:
    if not path:
        return None
    with open(path) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def main() -> None:
    client = VSSClient(config_from_env(), allowed_parents=load_scope(os.environ.get("VSS_SCOPE_FILE")))
    host = os.environ.get("VSS_ADAPTER_HOST", "127.0.0.1")
    port = int(os.environ.get("VSS_ADAPTER_PORT", "8090"))
    server = ThreadingHTTPServer((host, port), make_handler(client))
    sys.stderr.write(f"vss adapter listening on {host}:{port}\n")
    server.serve_forever()


if __name__ == "__main__":
    main()
