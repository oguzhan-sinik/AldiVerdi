# Shared contracts and integration gates

## Frozen API endpoints
- `GET /api/incidents/{incident_id}` → incident, cameras, videos.
- `GET /api/incidents/{incident_id}/evidence` → indexed evidence list.
- `GET /api/evidence/{evidence_id}` → observation, provenance, video offsets.
- `GET /api/incidents/{incident_id}/geometry` → GeoJSON.
- `POST /api/investigations` → investigation result/actions (streaming optional).
- `POST /api/tools/inspect` → `{video_id, start_s, end_s, question}` (tool name: `inspect_clip`).
- `POST /api/tools/localize` → `{evidence_ids:[...]}`.

Optional `segment_id` may appear on evidence records for grouping; the canonical seek target is always `video_id` + `start_s`/`end_s`.

## Protocol
A owns HTTP routing and orchestration. B owns functions that return the schema and a FastAPI router or JSON artifact. B never modifies A's UI; A never modifies B's science pipeline. A may mock all B responses with fixtures labelled `data_mode: synthetic_fixture` / `execution_mode: mock`.

## Integration gates (acceptance-driven, not clock-driven)
1. **Contract gate:** Both approve `contracts/schema.json`, `contracts/investigation.schema.json`, and fixtures (`python scripts/validate_contracts.py` PASS).
2. **Track gate:** A demonstrates fixture-backed map → camera → evidence seek → mock investigation trace. B supplies source-backed JSON and playable media independently.
3. **Swap gate:** A points the evidence adapter at B's validated manifest; no simultaneous edits to shared contract files.
4. **Tool gate:** Agent calls inspect/localize through the agreed adapter with validated IDs only.
5. **Demo gate:** End-to-end smoke test twice; freeze features.

## Contract testing
Validate fixtures and B exports with `python scripts/validate_contracts.py`. Reject missing provenance, invalid timestamp ranges, unverified bearing claims, unknown evidence IDs in investigations, and `fixture://` URLs in `source_backed` manifests. If schema must change, version it and update fixtures first.

## Failure modes
Indexing fails → local evidence search over precomputed Cosmos descriptions. Model endpoint fails → cached genuine model responses, labeled as replay. Camera calibration fails → render camera pins only when coordinates exist; never fake triangulation. Terrain fails → 2D geographic fallback with correct camera coordinates when verified.
