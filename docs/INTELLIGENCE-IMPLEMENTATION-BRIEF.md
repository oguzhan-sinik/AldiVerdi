# Developer B — Video intelligence, data and spatial science coding brief

## Mission
Supply real, verifiable wildfire video evidence and small scientific tools. Own `backend/intelligence/` and `data/`. A must be able to consume your outputs without asking how they were produced.

## Source first, models second
Primary: HPWREN Holy Fire 2018 archive `https://www.hpwren.ucsd.edu/news/20180812/`. Verify exact downloadable assets, their camera names, recording periods, time-lapse conversion and whether views are distinct. A panorama cropped into several windows is not independent camera geometry. Backup: HPWREN FIgLib `https://www.hpwren.ucsd.edu/FIgLib/` for fixed-camera sequences; only treat multiple clips as one incident when explicitly documented.

## Asset ledger (one row per file)
`video_id, incident_id, camera_id, source_page_url, direct_asset_url, local_path, sha256, fps, width, height, duration_s, recording_start_utc|null, timestamp_basis, camera_position_source|null, heading_source|null, rights_note, verification_status`.
- `timestamp_basis`: `recorded_utc`, `source_local_time`, `time_lapse_relative`, `unknown`.
- If a movie is sped up, **video seconds != incident elapsed seconds**. Preserve both and document mapping if known.
- No geographic pin for undocumented camera location. No bearing for undocumented PTZ pan/zoom.

## Deliverables (acceptance gate for tickets 06–10)
1. Two playable files **or** a clearly documented single-camera fallback, no fabricated second viewpoint.
2. `data/processed/incident.json` with `data_mode: source_backed`, validating via `python scripts/validate_contracts.py --incident data/processed/incident.json`.
3. `data/processed/asset-ledger.csv` with provenance and verification statuses.
4. `data/processed/observations.json` with evidence IDs and offsets; observations can be manually verified initially and must say so.
5. `backend/intelligence/extract_frames.py`: CLI reads an MP4 and exports frames at requested seconds using OpenCV; handles invalid offsets and corrupt files with explicit errors.
6. `data/processed/geometry.geojson` with only verified positions; empty FeatureCollection is valid.

## Cosmos adapter (after endpoints are available)
Input `{video_id, start_s, end_s, question}`; output `[{evidence_id, observation, confidence_label, limitations, model, start_s, end_s}]`. Use timestamped sampled frames if the endpoint does not support video payloads. Verify frame-rate limits and payload constraints. Cosmos does not calculate calibrated GPS, wind speed, or physical fire propagation from uncalibrated frames.

## Geometry: conditional, not required for the initial science gate
Camera known position + calibrated bearing => ray on terrain/map. Two independent verified camera bearings with overlapping event time => candidate intersection + uncertainty. Unknown headings => map pins only. Pixel-to-bearing requires camera FOV, pan/tilt and pixel location; do not infer from arbitrary clip title. Smoke top and ground ignition location differ; triangulating smoke gives at best a smoke-volume hypothesis.

## Validation commands (adapt to installed environment)
- `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 <file>`
- `python backend/intelligence/extract_frames.py --input <file> --seconds 10 20 --output data/processed/frames/`
- Validate incident JSON against `contracts/schema.json` with `jsonschema`.
- Manually inspect at least three frames per video for actual smoke/fire and camera stability.

## Non-goals
No model training, full wildfire segmentation benchmark, fire prediction engine, automatic camera calibration, photogrammetry, optical-flow geolocation, large datasets, or inferred timestamp synchronization.

## Handoff to A
Deliver stable filenames, manifest and source ledger at the integration gate. Include `video_id` to local/public playback URL mapping. Do not touch A's frontend; give a reproducible CLI and data samples.
