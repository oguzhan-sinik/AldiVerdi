"""Server-only client for the team's VSS retrieval backend (standard library only).

Handles login and one token refresh, bounded retries on transient failures, scope
(incident isolation), error classification and response normalization. Never logs or
returns credentials, tokens or presigned URLs.
"""
from __future__ import annotations

import json
import os
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Iterable

INVALID_INPUT = "invalid_input"
NOT_FOUND = "not_found"
AUTH = "auth"
UNAVAILABLE = "unavailable"
MALFORMED = "malformed"
UPSTREAM = "upstream"

TRANSIENT_STATUS = {502, 503, 504}
MEDIA_HEADERS = ("content-length", "content-range", "accept-ranges")
EXPLORE_PAGE = 100  # backend maximum
MAX_PAGES = 200


class VSSError(Exception):
    def __init__(self, kind: str, message: str):
        super().__init__(message)
        self.kind = kind
        self.message = message


class TransportError(Exception):
    """Connection failure or timeout before an HTTP status was received."""


@dataclass
class RawResponse:
    status: int
    headers: dict[str, str]  # lower-cased names
    body: bytes = b""
    stream: Any = None  # file-like with read(n) and close() when streaming


@dataclass
class MediaResponse:
    status: int
    headers: dict[str, str]
    stream: Any

    def chunks(self, size: int = 64 * 1024) -> Iterable[bytes]:
        while True:
            data = self.stream.read(size)
            if not data:
                return
            yield data

    def close(self) -> None:
        self.stream.close()


@dataclass(frozen=True)
class VSSConfig:
    url: str
    username: str
    password: str

    def __repr__(self) -> str:
        return f"VSSConfig(url={self.url!r}, username={self.username!r}, password=<redacted>)"


def config_from_env(env: dict[str, str] | None = None) -> VSSConfig:
    env = os.environ if env is None else env
    url = env.get("VSS_URL") or env.get("INGRESS_URL")
    user = env.get("VSS_USERNAME") or env.get("USERNAME")
    password = env.get("VSS_PASSWORD") or env.get("PASSWORD")
    missing = [n for n, v in (("VSS_URL", url), ("VSS_USERNAME", user), ("VSS_PASSWORD", password)) if not v]
    if missing:
        raise VSSError(AUTH, f"missing configuration: {', '.join(missing)}")
    return VSSConfig(url.rstrip("/"), user, password)


def config_from_file(path: str) -> VSSConfig:
    values = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                values[key] = value
    return config_from_env(values)


def urllib_transport(method: str, url: str, headers: dict[str, str], body: bytes | None,
                     timeout: float, stream: bool) -> RawResponse:
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        resp = e
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
        raise TransportError(type(e).__name__) from None
    hdrs = {k.lower(): v for k, v in resp.headers.items()}
    if stream and 200 <= resp.status < 300:
        return RawResponse(resp.status, hdrs, stream=resp)
    try:
        data = resp.read()
    except (TimeoutError, OSError) as e:
        raise TransportError(type(e).__name__) from None
    finally:
        resp.close()
    return RawResponse(resp.status, hdrs, body=data)


class VSSClient:
    def __init__(self, config: VSSConfig, *, allowed_parents: Iterable[str] | None = None,
                 transport: Callable[..., RawResponse] = urllib_transport,
                 retries: int = 2, timeout: float = 30.0, search_timeout: float = 90.0,
                 sleep: Callable[[float], None] = time.sleep):
        self._cfg = config
        self._base = config.url + "/api/v1"
        self._transport = transport
        self._retries = retries
        self._timeout = timeout
        self._search_timeout = search_timeout
        self._sleep = sleep
        self._token: str | None = None
        self._lock = threading.Lock()
        self._fields: dict[str, list[str]] | None = None
        self._parent_of: dict[str, str] = {}
        self.allowed_parents = frozenset(allowed_parents) if allowed_parents is not None else None

    # ---- auth & transport -------------------------------------------------

    def _redact(self, text: str) -> str:
        for secret in (self._cfg.password, self._token):
            if secret:
                text = text.replace(secret, "<redacted>")
        return text

    def _login(self) -> str:
        body = json.dumps({"username": self._cfg.username, "password": self._cfg.password}).encode()
        resp = self._send("POST", "/auth/login", None, body, {"Content-Type": "application/json"},
                          self._timeout, False)
        if resp.status == 401:
            raise VSSError(AUTH, "VSS rejected the configured credentials")
        if resp.status != 200:
            raise self._error(resp)
        token = self._parse(resp).get("access_token")
        if not isinstance(token, str) or not token:
            raise VSSError(MALFORMED, "login response has no access_token")
        return token

    def _ensure_token(self, stale: str | None = None) -> str:
        with self._lock:
            if self._token is None or self._token == stale:
                self._token = self._login()
            return self._token

    def _send(self, method, path, params, body, headers, timeout, stream) -> RawResponse:
        url = self._base + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        for attempt in range(self._retries + 1):
            try:
                resp = self._transport(method, url, headers, body, timeout, stream)
            except TransportError as e:
                if attempt == self._retries:
                    raise VSSError(UNAVAILABLE, f"VSS unreachable ({e})") from None
            else:
                if resp.status not in TRANSIENT_STATUS or attempt == self._retries:
                    return resp
                if resp.stream is not None:
                    resp.stream.close()
            self._sleep(0.5 * 2 ** attempt)
        raise AssertionError("unreachable")

    def _request(self, method: str, path: str, *, params: dict | None = None, json_body: Any = None,
                 headers: dict | None = None, timeout: float | None = None, stream: bool = False,
                 token_in_query: bool = False) -> RawResponse:
        body = json.dumps(json_body).encode() if json_body is not None else None
        token = self._ensure_token()
        for refreshed in (False, True):
            hdrs = dict(headers or {})
            qp = dict(params or {})
            if body is not None:
                hdrs["Content-Type"] = "application/json"
            if token_in_query:
                qp["token"] = token
            else:
                hdrs["Authorization"] = f"Bearer {token}"
            resp = self._send(method, path, qp, body, hdrs, timeout or self._timeout, stream)
            if resp.status != 401 or refreshed:
                break
            token = self._ensure_token(stale=token)
        if resp.status == 401:
            raise VSSError(AUTH, "VSS rejected a freshly issued token")
        if resp.status in TRANSIENT_STATUS:
            raise VSSError(UNAVAILABLE, f"VSS returned HTTP {resp.status} after retries")
        return resp

    def _parse(self, resp: RawResponse) -> Any:
        try:
            return json.loads(resp.body)
        except (ValueError, TypeError):
            raise VSSError(MALFORMED, f"VSS returned non-JSON (HTTP {resp.status})") from None

    def _error(self, resp: RawResponse) -> VSSError:
        try:
            detail = json.loads(resp.body).get("detail")
        except (ValueError, TypeError, AttributeError):
            detail = None
        text = detail if isinstance(detail, str) else json.dumps(detail) if detail else ""
        if resp.status == 404 or (resp.status == 500 and "(404)" in text and "Not Found" in text):
            return VSSError(NOT_FOUND, "not found")
        if resp.status in (400, 422):
            return VSSError(INVALID_INPUT, self._redact(text)[:300] or f"HTTP {resp.status}")
        # Never echo 5xx detail: the backend includes SQL and internals there.
        return VSSError(UPSTREAM, f"VSS returned HTTP {resp.status}")

    def _get_json(self, path: str, params: dict | None = None) -> Any:
        resp = self._request("GET", path, params=params)
        if resp.status != 200:
            raise self._error(resp)
        return self._parse(resp)

    # ---- scope ------------------------------------------------------------

    def _in_scope(self, parent: str | None) -> bool:
        return self.allowed_parents is None or parent in self.allowed_parents

    def _require_parent_scope(self, parent: str) -> None:
        if not self._in_scope(parent):
            raise VSSError(NOT_FOUND, "not found")

    def _require_source_scope(self, source: str) -> None:
        """A source is in scope if it is an allowed parent or a segment of one."""
        if self.allowed_parents is None or source in self.allowed_parents:
            return
        if source not in self._parent_of:
            self.segment(source)  # raises not_found when out of scope
        self._require_parent_scope(self._parent_of[source])

    # ---- public operations ------------------------------------------------

    def me(self) -> dict:
        data = self._get_json("/auth/me")
        if not isinstance(data, dict) or "username" not in data:
            raise VSSError(MALFORMED, "unexpected /auth/me response")
        return {"username": data["username"]}

    def filters(self) -> dict[str, list[str]]:
        """Filterable metadata fields and their current values."""
        if self._fields is None:
            data = self._get_json("/metadata/schema")
            try:
                self._fields = {f["name"]: list(f.get("options") or []) for f in data["schema"]}
            except (KeyError, TypeError):
                raise VSSError(MALFORMED, "unexpected /metadata/schema response") from None
        return self._fields

    def search(self, query: str, *, top_k: int = 15, min_similarity: float | None = None,
               filters: dict[str, str] | None = None, time_filter: str | None = None) -> dict:
        if not isinstance(query, str) or not query.strip():
            raise VSSError(INVALID_INPUT, "query must be a non-empty string")
        if not isinstance(top_k, int) or isinstance(top_k, bool) or not 1 <= top_k <= 100:
            raise VSSError(INVALID_INPUT, "top_k must be an integer from 1 to 100")
        filters = filters or {}
        if not isinstance(filters, dict):
            raise VSSError(INVALID_INPUT, "filters must be an object")
        unknown = sorted(set(filters) - set(self.filters()))
        if unknown:
            raise VSSError(INVALID_INPUT, f"unknown filter field(s): {', '.join(unknown)}")
        if not all(isinstance(v, str) for v in filters.values()):
            raise VSSError(INVALID_INPUT, "filter values must be strings")
        body: dict[str, Any] = {"query": query.strip(), "top_k": top_k, "llm_top_n": 1,
                                "metadata_filters": filters}
        if min_similarity is not None:
            body["min_similarity"] = min_similarity
        if time_filter is not None:
            body["time_filter"] = time_filter
        resp = self._request("POST", "/search", json_body=body, timeout=self._search_timeout)
        if resp.status != 200:
            raise self._error(resp)
        data = self._parse(resp)
        try:
            rows, chunks = data["results"], data["chunk_results"]
        except (KeyError, TypeError):
            raise VSSError(MALFORMED, "unexpected /search response") from None
        segments = [s for s in map(self._segment, rows) if self._in_scope(s["original_video"])]
        videos = [v for v in map(self._video, chunks) if self._in_scope(v["original_video"])]
        return {"segments": segments, "videos": videos, "total": len(segments)}

    def list_videos(self, *, location: str | None = None, date: str | None = None) -> list[dict]:
        """Every fully indexed parent video, across all pages."""
        params: dict[str, Any] = {"scope": "all", "limit": EXPLORE_PAGE}
        if location:
            params["location"] = location
        if date:
            params["date"] = date
        videos, offset = [], 0
        for _ in range(MAX_PAGES):
            data = self._get_json("/videos/explore", {**params, "offset": offset})
            try:
                page, total = data["chunks"], int(data["total"])
            except (KeyError, TypeError, ValueError):
                raise VSSError(MALFORMED, "unexpected /videos/explore response") from None
            videos += [self._video(c) for c in page]
            offset += len(page)
            if not page or offset >= total:
                break
        else:
            raise VSSError(MALFORMED, "/videos/explore did not finish paging")
        return [v for v in videos if self._in_scope(v["original_video"])]

    def segments(self, original_video: str) -> list[dict]:
        self._require_parent_scope(original_video)
        data = self._get_json("/tools/segments", {"original_video": original_video})
        try:
            rows = data["segments"]
        except (KeyError, TypeError):
            raise VSSError(MALFORMED, "unexpected /tools/segments response") from None
        return sorted(map(self._segment, rows), key=lambda s: s["segment_number"] or 0)

    def segment(self, source: str) -> dict:
        data = self._get_json("/tools/segment", {"source": source})
        if not isinstance(data, dict) or not isinstance(data.get("segment"), dict):
            raise VSSError(MALFORMED, "unexpected /tools/segment response")
        seg = self._segment(data["segment"])
        self._require_parent_scope(seg["original_video"])
        return seg

    def detections(self, source: str) -> dict:
        self._require_source_scope(source)
        data = self._get_json("/videos/detections", {"source": source})
        if not isinstance(data, dict) or not isinstance(data.get("frames"), list):
            raise VSSError(MALFORMED, "unexpected /videos/detections response")
        return data

    def index_status(self) -> dict:
        data = self._get_json("/dashboard/stats", {"scope": "all"})
        if not isinstance(data, dict) or not isinstance(data.get("overview"), dict):
            raise VSSError(MALFORMED, "unexpected /dashboard/stats response")
        return {"overview": data["overview"], "quality": data.get("quality")}

    def open_media(self, source: str, range_header: str | None = None) -> MediaResponse:
        """Open a parent or segment video. Caller must close() the result."""
        self._require_source_scope(source)
        headers = {"Range": range_header} if range_header else {}
        resp = self._request("GET", "/videos/stream", params={"source": source}, headers=headers,
                             stream=True, token_in_query=True)
        if resp.status in (200, 206):
            hdrs = {k: resp.headers[k] for k in MEDIA_HEADERS if k in resp.headers}
            hdrs["content-type"] = "video/mp4"
            return MediaResponse(resp.status, hdrs, resp.stream)
        if resp.status == 416:
            hdrs = {k: resp.headers[k] for k in ("content-range",) if k in resp.headers}
            return MediaResponse(416, hdrs, _Empty())
        raise self._error(resp)

    # ---- normalization ----------------------------------------------------

    def _segment(self, row: Any) -> dict:
        if not isinstance(row, dict):
            raise VSSError(MALFORMED, "segment row is not an object")
        source, parent = row.get("source"), row.get("original_video")
        start, end = _num(row.get("segment_start_sec")), _num(row.get("segment_end_sec"))
        if not isinstance(source, str) or not isinstance(parent, str) or start is None or end is None:
            raise VSSError(MALFORMED, "segment row lacks source, original_video or timing")
        self._parent_of[source] = parent
        extra = _json_obj(row.get("extra_metadata"))
        counts = _json_obj(row.get("object_counts"))
        return {
            "source": source,
            "original_video": parent,
            "segment_number": _int(row.get("segment_number")),
            "total_segments": _int(row.get("total_segments")),
            "start_s": start,
            "end_s": end,
            "duration_s": _num(row.get("duration")),
            "description": row.get("reasoning_content") if isinstance(row.get("reasoning_content"), str) else None,
            "description_model": row.get("cosmos_model") if isinstance(row.get("cosmos_model"), str) else None,
            "camera_id": _str(row.get("camera_id")),
            "capture_type": _str(row.get("capture_type")),
            "location": _str(row.get("location")),
            "object_classes": _classes(row.get("object_classes")),
            "object_counts": counts,
            "ingested_at": _str(row.get("upload_timestamp")),
            "stream_id": _str(extra.get("stream_id")),
            "chunk_index": _int(extra.get("chunk_index")),
            "chunk_start_s": _num(extra.get("chunk_start_sec")),
            "similarity": _num(row.get("similarity_score")),
        }

    def _video(self, row: Any) -> dict:
        if not isinstance(row, dict) or not isinstance(row.get("original_video"), str):
            raise VSSError(MALFORMED, "video row lacks original_video")
        return {
            "original_video": row["original_video"],
            "filename": _str(row.get("filename")),
            "duration_s": _num(row.get("chunk_duration_sec")),
            "total_segments": _int(row.get("total_segments")),
            "best_segment_number": _int(row.get("best_segment_number")),
            "best_start_s": _num(row.get("best_match_start_sec")),
            "best_end_s": _num(row.get("best_match_end_sec")),
            "best_source": _str(row.get("preview_source")),
            "matched_segment_count": _int(row.get("matched_segment_count")),
            "similarity": _num(row.get("similarity_score")),
            "description": _str(row.get("reasoning_content")),
            "camera_id": _str(row.get("camera_id")),
            "capture_type": _str(row.get("capture_type")),
            "location": _str(row.get("location")),
            "ingested_at": _str(row.get("upload_timestamp")),
            "stream_id": _str(row.get("stream_id")),
            "chunk_index": _int(row.get("chunk_index")),
        }


class _Empty:
    def read(self, _n: int = -1) -> bytes:
        return b""

    def close(self) -> None:
        pass


def _num(v: Any) -> float | None:
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def _int(v: Any) -> int | None:
    return v if isinstance(v, int) and not isinstance(v, bool) else None


def _str(v: Any) -> str | None:
    return v if isinstance(v, str) and v else None


def _json_obj(v: Any) -> dict:
    if isinstance(v, dict):
        return v
    if isinstance(v, str):
        try:
            parsed = json.loads(v)
        except ValueError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _classes(v: Any) -> list[str]:
    if isinstance(v, list):
        return [c for c in v if isinstance(c, str)]
    if isinstance(v, str):
        return [c.strip() for c in v.split(",") if c.strip()]
    return []
