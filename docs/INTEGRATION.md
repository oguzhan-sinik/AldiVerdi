# Shared contracts and integration gates

## Frozen API endpoints
- `GET /api/incidents/{incident_id}` → incident, cameras, videos.
- `GET /api/incidents/{incident_id}/evidence` → indexed evidence list.
- `GET /api/evidence/{evidence_id}` → observation, provenance, video offsets.
- `GET /api/incidents/{incident_id}/geometry` → GeoJSON.
- `POST /api/investigations` → investigation result/actions (streaming optional).
- `POST /api/tools/inspect` → `{segment_id, question}`.
- `POST /api/tools/localize` → `{evidence_ids:[...]}`.

## Protocol
A owns HTTP routing and orchestration. B owns functions that return the schema and a FastAPI router or JSON artifact. B never modifies A's UI; A never modifies B's science pipeline. A may mock all B responses with fixtures.

## Merge gates
- **T+00:20** Freeze IDs, JSON schema and endpoints. One joint 10-minute call.
- **T+02:30** B provides first real manifest/evidence JSON. A swaps fixture adapter for real data; no simultaneous edits to shared files.
- **T+04:30** Agent calls B's inspect/localize tools through agreed adapter. Pair integration for 20 minutes.
- **T+06:00** Freeze features and merge. Both validate end-to-end demo.

## Contract testing
Validate sample JSON against `contracts/schema.json` and reject missing provenance, invalid timestamp ranges, unverified bearing claims, and evidence from different incidents. If schema must change, version it to v2 and update fixtures first.

## Failure modes
Indexing fails → local evidence search over precomputed Cosmos descriptions. Model endpoint fails → cached genuine model responses, labeled as replay. Camera calibration fails → render camera pins, not fake triangulation. Terrain fails → 2D geographic fallback with correct camera coordinates.
