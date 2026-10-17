# Dataset acquisition and video intelligence — Developer B

## Primary incident: 2018 Holy Fire / Santiago Peak
Source: https://www.hpwren.ucsd.edu/news/20180812/
Inspect the archive for source videos, source camera labels, exact capture dates, synchronized time and downloadable format. Do not assume every linked camera has a stable known bearing. Record licensing/attribution and whether the camera footage is a panorama or PTZ.

## Backup
HPWREN FIgLib: https://www.hpwren.ucsd.edu/FIgLib/ . Prefer documented multi-camera incident collections. 2025 Palisades ALERTCalifornia footage is a backup only if individual sources and provenance can be verified.

## Data acceptance gate
- At least 2 usable video assets for the same documented incident.
- `video_id`, source URL, incident ID, local duration, start timestamp if known, camera ID if known.
- Each video playable locally or via stable accessible URL.
- At least one time interval containing visible smoke or fire.
- For Gold localization: two calibrated camera bearings toward same visible event and overlapping times.

## Pipeline
1. Fetch or register source video with metadata, checksum and rights note.
2. Normalize playback format only if necessary; preserve original FPS and timeline mapping.
3. Segment into short evidence windows (e.g. 5–15 seconds for active changes; longer for time-lapse) with original-video offsets.
4. Cosmos prompt: identify directly visible smoke, flames, occlusion, camera movement, visual event ordering and limitations. Return structured JSON.
5. Optional OpenCV: frame differencing / smoke-region motion / optical flow or colour threshold. Treat apparent motion as image-space, not physical spread.
6. Save `segments.json`, `observations.json`, `camera_geometry.geojson`.

## Cross-video matching
Only align by actual UTC timestamp or documented synchronization. If no absolute time, allow qualitative comparison but do not assert simultaneity. An event's appearance at different times is not necessarily the same source.

## Evidence citation contract
Every observation includes `evidence_id`, `video_id`, `start_s`, `end_s`, `observation`, `status`, and optional `segment_id`, `model`, `limitations`. Canonical seek target is `video_id` + offsets. Never fabricate second-precision event timestamps from sparsely sampled time-lapses.
