# Developer B — Complete Continuous Implementation Prompt (Clean Start)

You own `backend/intelligence/` and `data/`. This repository has **no implemented video intelligence**. Read `PROJECT-AGREEMENT.md`, `docs/SETUP.md`, `docs/DATA.md`, `docs/SPATIAL.md`, `docs/CONTRACTS.md`, `docs/INTEGRATION.md`, and actual schemas/fixtures.

## Phase 0: Contract sign-off
Run validator and pytest. Review whether current v1 can represent two source-backed videos, independent cameras, evidence intervals, unknown geometry, timestamp basis and provenance. Map logical `video_id` to `data/processed/<video_id>.mp4` in a separate ledger. Time-lapse anchors belong in ledger. Coordinate any schema change with A before freezing.

## Phase 1: Source verification
Survey HPWREN 2018 Holy Fire archives, actual video URLs, independent viewpoints, camera positions/orientation, clock basis and usage rights. Write `data/sources/manifest-notes.md`. Browsing only until authorized. Confirm whether organizer permits external video ingestion into VAST.

## Phase 2: Authorized video assets
With permission, acquire minimum necessary source clips into `data/raw/`; normalize to `data/processed/<video_id>.mp4`. Install FFmpeg/ffprobe if permitted. Write `data/processed/asset-ledger.csv` with SHA256, fps, dimensions, duration, source, rights and time mapping. Never invent a playable URL.

## Phase 3: Real evidence
Write contract-valid source-backed incident/evidence outputs with human-verified observations and accurate video-relative offsets. `data/evidence.json` is canonical unless both developers agree on a change. No duplicate authoritative files.

## Phase 4: OpenCV
Implement `backend/intelligence/video_tools.py` with frame extraction, small CLI, optional change score and error handling. Test on approved or synthetic media; respect variable frame rate and timestamp semantics.

## Phase 5: Cosmos
Inspect actual organizer-provided Cosmos/VAST interfaces and team config. Prefer existing VAST descriptions when available. Implement small Cosmos analysis adapter only after verifying input/output contract; never fake live results.

## Phase 6: Geometry
Create `data/geometry.geojson` with only verified locations and `data/geometry-status.md` with readiness, uncertainty and gaps. Test synthetic bearing geometry; no unsupported triangulation.

## Handoff and rules
Give A stable IDs, playable asset mapping, evidence provenance, time mapping, geometry status and test results. Never download/upload external footage without authorization and rights verification. Never unilaterally edit contracts. Work acceptance-driven without project schedules; report actual tests and blockers after each phase.

**Start now with contract review and HPWREN source verification.**
