# Developer B — Continuous Implementation Specification

**Role:** Wildfire video sourcing, scientific video intelligence, Cosmos analysis adapter, OpenCV and geometry.

## Start from real baseline
Current shared schemas and fixtures reportedly pass validation. Developer A's frontend shell exists. B has not written implementation code. Read `PROJECT-AGREEMENT.md`, `docs/CURRENT-STATE.md`, `docs/SETUP.md`, `docs/CONTRACTS.md`, `docs/DATA.md`, `docs/SPATIAL.md`, and this document.

## Workstream 1 — Contract sign-off
Confirm current schemas represent two real videos, independent camera IDs, video-relative offsets, nullable geometry, rights and provenance. Use `data/processed/<video_id>.mp4` **outside the incident schema** with a ledger mapping. Preserve time-lapse mapping in ledger (not an invented absolute time). Do not change frozen schema without A approval. Run contract tests.

## Workstream 2 — Source verification
Research HPWREN Holy Fire archive (https://www.hpwren.ucsd.edu/news/20180812/). Verify media asset URLs, incident/date, camera independence, clock basis, camera metadata and usage rights. Write `data/sources/manifest-notes.md`. Browsing source pages is permitted; ask for authorization before downloading specific footage, including source, size and license findings. Confirm VAST organizer permits external ingestion before uploading.

## Workstream 3 — Assets
After authorization, download minimum necessary original footage to `data/raw/`. Use ffprobe and FFmpeg (install if permitted and missing) to create playable `data/processed/<video_id>.mp4` files. Record SHA256, metadata, source, processing, playable status and timestamp anchors in `data/processed/asset-ledger.csv`. Never treat a news URL as playable footage.

## Workstream 4 — Evidence
Produce one canonical schema-valid `data/evidence.json` and source-backed incident metadata consistent with current consumers. Evidence must link to actual video IDs and intervals. Human review and model inference must be labelled distinctly. Do not create duplicate competing observations files.

## Workstream 5 — OpenCV tools
Implement `backend/intelligence/video_tools.py` with importable frame-extraction functions and a minimal CLI; optional change scoring. Handle invalid offsets, variable frame rates, decode failures, RGB/BGR, frame sizes and memory usage. Test on approved media or synthetic fixtures.

## Workstream 6 — Cosmos
Read organizer's actual model skill and configured endpoint. Implement a small adapter only after validating input/output contract. Prefer consuming VAST-generated Cosmos observations when they exist; otherwise use authorized direct inference if supported. Retain model, prompt, video ID, inspected interval and output provenance. Never claim untested live inference.

## Workstream 7 — Geometry
Produce `data/geometry.geojson` with verified camera locations only and `data/geometry-status.md` with missing calibration and triangulation readiness. Implement bearings only with documented assumptions; test synthetic known geometry. No precise ignition coordinate from insufficient metadata.

## Handoff to A
Provide canonical incident/evidence IDs, asset resolver mapping, verified timestamp basis, rights notes, geometry status, schema test results and clearly labelled live/fixture capabilities.

## Rules
- Own `backend/intelligence/` and `data/`; do not modify A's frontend/platform tree.
- No unilateral schema edits, invented coordinates, unsupported clock mapping or fake observations.
- No external footage download/ingestion without authorization and rights verification.
- Keep implementation lean and acceptance-driven; no project schedules.
- If a service is blocked, record it and continue independent tasks.

## Required report
What was implemented, exact data sources and authorization status, files changed, tests actually run, scientific limitations, A handoff and next dependency.

**Begin with schema sign-off and HPWREN source verification, not Cosmos deployment.**
