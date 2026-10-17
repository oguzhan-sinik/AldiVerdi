# VSS adapter (Developer B)

Server-only access to team-31's VSS retrieval backend. Developer A calls the internal HTTP
service in this folder; nothing else in FireFront talks to VSS directly.

- `client.py` — Python client: login, token refresh, retries, response normalization.
- `server.py` — internal HTTP service A calls (localhost by default).
- `live_check.py` — read-only checks against the real backend; prints PASS/FAIL only.

Standard library only (Python 3.12), so it runs in a plain `python:3.12-slim` pod.

## Run

```bash
cd backend/intelligence
VSS_URL=... VSS_USERNAME=... VSS_PASSWORD=... python3 -m vss.server     # listens on 127.0.0.1:8090
python3 -m vss.live_check --config /config/team-31.config               # on the workshop VM
```

Credentials come from `VSS_URL`/`VSS_USERNAME`/`VSS_PASSWORD` (deployment Secret names) or,
for local checks, from the team config file passed with `--config`. They are never logged.

Optional `VSS_SCOPE_FILE`: a text file with one `original_video` URI per line. When set,
every search result, segment, detection and media request outside that list is treated as
not found. This keeps an incident's investigation from pulling in unrelated footage.

## Service API for Developer A

All responses are JSON except `/v1/media`. Errors are
`{"error": {"kind": "...", "message": "..."}}`.

| Route | Purpose |
|---|---|
| `GET /health` | `{"ok": true}` if login works, else 503 |
| `GET /v1/filters` | Filterable fields and their current values |
| `POST /v1/search` | Body: `query` (required), `top_k` (1–100, default 15), `min_similarity`, `filters` (dict), `time_filter` |
| `GET /v1/videos?location=&date=` | Every fully indexed parent video (all pages) |
| `GET /v1/segments?original_video=` | All indexed segments of one parent, by segment number |
| `GET /v1/segment?source=` | One segment |
| `GET /v1/detections?source=` | YOLO sidecar for one segment |
| `GET /v1/media?source=` | Video bytes; forwards `Range`, returns 200/206/416 |

| Error kind | HTTP | Meaning |
|---|---|---|
| `invalid_input` | 400 | Bad argument (unknown filter field, top_k out of range, empty query) |
| `not_found` | 404 | No such segment/object, or outside the scope file |
| `auth` | 502 | VSS rejected our credentials (server config problem, not the caller's) |
| `unavailable` | 503 | VSS unreachable or timing out after retries |
| `malformed` | 502 | VSS returned something the adapter could not parse |
| `upstream` | 502 | Any other VSS error |

### Normalized segment

```json
{
  "source": "s3://team-31-vss-chunks-segments/segments/<stem>_segment_002_of_006.mp4",
  "original_video": "s3://team-31-vss-chunks/team-31/<stem>.mp4",
  "segment_number": 2, "total_segments": 6,
  "start_s": 5.0, "end_s": 10.0, "duration_s": 5.0,
  "description": "…Cosmos-generated text…", "description_model": "nvidia/cosmos3-nano-reasoner",
  "camera_id": "…", "capture_type": "…", "location": "…",
  "object_classes": ["car"], "object_counts": {"car": 4},
  "ingested_at": "2026-10-01T07:36:17.696692",
  "stream_id": null, "chunk_index": null, "chunk_start_s": null,
  "similarity": 0.44
}
```

- `description` is the caption written at ingest time from the ingest prompt. It is indexed
  analysis, not a fresh look at the frames.
- `ingested_at` is when VSS received the upload. It is **not** the recording time.
- Search returns `{"segments": [...], "videos": [...], "total": n}`. `videos` groups hits by
  parent with `best_start_s`/`best_end_s`.

### Time offsets

| Name | Range | Source field |
|---|---|---|
| Parent offset | 0 … parent duration | `start_s`, `end_s`, `best_start_s` |
| Segment-local offset | 0 … ~5 s | parent offset − segment `start_s` |
| Stream offset (batch-chunked streams only) | from stream start | `chunk_start_s` + parent offset |

Both a parent and its segments can be streamed. To show a cited parent interval, either play
the parent and seek to `start_s`, or play the segment and seek to `parent_offset − start_s`.
Never seek a 5-second segment to a parent offset. Recording time is unknown unless the asset
ledger gives an anchor.

## Live VSS contract (checked 2026-10-17 on the team-31 workshop VM)

Base: `$INGRESS_URL/api/v1`. **HTTP only** — HTTPS on the same host does not answer, so TLS
cannot be enabled from our side. Auth is a JWT from login, sent as `Authorization: Bearer`,
except the media routes, which only accept `?token=` (header auth there returns 422).

| Route | Checked | Notes |
|---|---|---|
| `POST /auth/login` | 200 / 401 | Body `{username, password}` → `{access_token, token_type, username}`. Bad password: 401 `Invalid username or password` |
| `GET /auth/me` | 200 / 401 | `{username, email, auth_type}`. Bad token: 401 `Invalid token`; no token: 401 `Could not validate credentials` |
| `GET /metadata/schema` | 200 | Filterable fields: `camera_id`, `capture_type`, `location`, `object_classes` (all `select`) |
| `GET /metadata/values?field=` | 200 / 400 | `{field, values, count}`; unknown field → 400 |
| `GET /metadata/ingest-config` | 200 | Public. Scenarios, capture types, `custom_prompt_max_length` (800) |
| `POST /search` | 200 / 422 / 500 | `results[]` (segments), `chunk_results[]` (per parent, with `timeline[]`), `total`, `chunk_total`, `llm_synthesis`, `sql_query`. `top_k` ≤ 100; `llm_top_n` must be ≥ 1 (synthesis always runs, ~2–4 s). **Unknown `metadata_filters` key → 500 that leaks SQL**, so the adapter validates keys first |
| `GET /videos/explore` | 200 / 422 | `chunks[]`, `total`, `limit`, `offset`; `limit` ≤ 100, page with `offset`. Optional `location`, `date` |
| `GET /tools/segments?original_video=` | 200 | `{original_video, total, segments[]}`; unknown parent → 200 with `total: 0`; no paging |
| `GET /tools/segment?source=` | 200 / 404 | `{segment: {...}}` |
| `GET /videos/metadata?source=` | 200 | Same row as `tools/segment`, unwrapped |
| `GET /videos/detections?source=` | 200 / 404 | YOLO sidecar: `fps`, `frame_count`, `frames[].detections[]{label, confidence, bbox}` |
| `GET /videos/stream?source=&token=` | 200 / 206 / 416 / 401 / 500 | Supports `Range` (incl. suffix). Content-type is `binary/octet-stream`. **Missing object → 500** with `HeadObject … 404` text; the adapter maps it to `not_found` |
| `GET /videos/playback-url` | 200 | `{url, expires_in}` presigned S3 URL. Not used: bucket CORS unverified, and the URL is a credential |
| `GET /dashboard/stats` | 200 | Index overview, quality, objects, metadata counts, recent videos |
| `GET /config` | 200 | **Returns S3, VastDB and NVIDIA secret keys.** Never proxy it; the adapter does not call it |

Field notes:
- `object_classes` is a comma-separated string; `object_counts`, `perception_json` and
  `extra_metadata` are JSON encoded as strings. Any of them may be null.
- `extra_metadata` carries `stream_id`, `chunk_index`, `chunk_start_sec`, `ingest_kind`.
- The captioning model reported in rows is `nvidia/cosmos3-nano-reasoner`.
- Every row is filtered to `is_public OR allowed_users ∋ team-31`; `permission_filtered`
  reports how many hits were dropped.
- Not used by the adapter (A's agent does its own reasoning): `/agent/ask`,
  `/agent/search-and-answer`, `/videos/synthesize`.

## Ingestion status (not done by the adapter)

The two Holy Fire test uploads from 2026-10-17 (`20261017_105838_ca2d70ef`,
`20261017_110131_217ea46c`) were split into 13 segments each, but never indexed: the
captioning step rejected every segment (`Target fps (4.0) must be <= original fps (0.5)`).
New uploads are blocked until organizer permission for external footage is recorded.
