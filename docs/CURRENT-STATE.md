# Current state and verified boundaries

## Reported working baseline
A prior repository auditor reported `python scripts/validate_contracts.py` PASS, `pytest tests/test_contracts.py` 7/7, and created or revised:
- `contracts/schema.json` with `data_mode`, `playback_status`, nullable geometry and related metadata;
- `contracts/investigation.schema.json` for investigation actions and claims;
- `fixtures/incident.json`, `fixtures/investigation.json`;
- `scripts/validate_contracts.py` and `tests/test_contracts.py`.

Developer A reported Next.js 15 shell implemented and tested: `frontend/app/incident/[id]/page.tsx`, three-panel layout, camera list, Cesium placeholder, evidence panel, `frontend/lib/api.ts` fixture/live adapter. Reported `npm run build` and `npm run lint` passed. These are **agent reports**, not tests rerun by this document author.

## Not yet implemented or not demonstrated
- Real Cesium terrain and geolocated camera markers.
- Video playback with validated media resolution and evidence seeking.
- Working autonomous investigation agent and W&B trace.
- Live VAST/Cosmos video search and reasoning for wildfire footage.
- Verified, playable wildfire footage; OpenCV CLI; calibrated geometry.
- End-to-end live deployment.

## Immediate dependencies
- Joint sign-off on **current** schemas and fixtures; do not restore older schema versions.
- Developer A continues at real Cesium map, not frontend scaffolding.
- Developer B begins source verification and metadata/rights assessment, not invented observations.
- Confirm workshop VM/team config, VAST search access and external media ingestion policy.
- Real media acquisition needs authorization and verified rights.

## Status semantics
`PASS`: command executed and succeeded. `FAIL`: executed and failed. `BLOCKED`: external dependency missing. `NOT RUN`: not executed. Mock and live results must never be conflated.
