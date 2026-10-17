# Source and geometry gate — do this BEFORE the tickets

## Source verification checklist
1. Open `https://www.hpwren.ucsd.edu/news/20180812/` and identify the **exact** clips for 2018 Holy Fire. Write down page links, direct media links, camera labels and capture date/time claims. Confirm whether the page exposes a movie, a panorama, or multiple independent cameras.
2. Download or stream one small clip and verify actual playback. `ffprobe` duration, fps and dimensions. Check whether the time lapse has source clock overlays or documented capture cadence.
3. Identify a second asset **from the same documented incident**. Determine if it is another time interval from the same camera or an independent camera position. Both are useful, but only independent calibrated viewpoints support triangulation.
4. Check whether camera coordinates are documented. Distinguish site location from optical heading; PTZ footage may have unknown pan/zoom per segment.
5. Open Cesium ion dashboard and check access token and terrain availability. Do not start implementing Google 3D tiles; terrain + imagery is sufficient.
6. At the event, test Cosmos input payload and VAST custom-video ingestion against **one 5–10-second clip** before batch ingestion. Capture actual API response, latency, and IDs. No model response should be faked as live.

## Decision table
| What is verified | What the demo may claim | What it must not claim |
|---|---|---|
| Same incident, 2 clips, unknown camera locations | Multi-video temporal investigation | Geographic triangulation |
| Same incident, 2 documented camera sites, unknown orientations | Geolocated camera pins and cross-camera search | Intersecting optical rays |
| 2 cameras, headings/FOV verified, overlapping observations | Approximate viewing wedges / candidate overlap | Exact ignition GPS or fire perimeter |
| Only one verified video | Single-video investigation with multiple time windows | Cross-camera corroboration |
| Model/index unavailable | Labeled fixture or cached replay | Live Cosmos/VAST analysis |

## Source integrity checklist
- [ ] Two assets genuinely belong to same incident
- [ ] Direct video URLs and rights/attribution recorded
- [ ] Time-lapse mapping documented or marked unknown
- [ ] Camera IDs consistent across source and manifest
- [ ] Location and heading are independently verified or null
- [ ] Local playback and source links tested
- [ ] Original footage preserved, processed copies distinguished

## Time-saving contingency
If Holy Fire archive navigation or downloads are blocked, switch to a documented HPWREN FIgLib incident. The primary demo becomes evidence timeline + agent investigation + known map context. Geometry is optional and conditional.

## Source links
- HPWREN Holy Fire: https://www.hpwren.ucsd.edu/news/20180812/
- HPWREN Fire Ignition Library: https://www.hpwren.ucsd.edu/FIgLib/
- CesiumJS: https://cesium.com/platform/cesiumjs/
- NVIDIA VSS: https://docs.nvidia.com/vss/latest/
- CoreWeave serverless: https://docs.coreweave.com/products/inference/serverless
- Weave: https://wandb.ai/site/weave/
