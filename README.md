# FireFront 3D — Autonomous Geospatial Wildfire Investigation

**Hackathon:** 7-hour build, two developers. **Primary case:** 2018 Holy Fire / Santiago Peak, California (subject to source verification).

## Product
Upload multiple real videos of one documented wildfire. A video agent retrieves and inspects relevant segments, reasons about their chronology, requests independent observations, and connects findings to a CesiumJS terrain map with camera locations, viewing bearings, evidence citations and uncertainty. **The video is the evidence; the map is the spatial index; the agent decides the next investigative action.**

## Judge's question
> Where did smoke first become visible, and does a second camera corroborate it?

The answer must include evidence IDs, source-video timestamps, and geographic qualification. Never invent a camera location, orientation, fire coordinate, or cross-video temporal relationship.

## Ownership — hard boundary
- **A — Platform + Agent:** `frontend/`, `backend/platform/`, `docs/UX.md`, `docs/AGENT.md`. Cesium terrain, UI, agent planning, retrieval adapter, Weave instrumentation.
- **B — Video + Science:** `backend/intelligence/`, `data/`, `docs/DATA.md`, `docs/SPATIAL.md`. Incident acquisition, metadata, segment analysis, OpenCV, calibrated bearings and intersection.
- **Shared, frozen early:** `contracts/`, `fixtures/`, `docs/INTEGRATION.md`. Only edit via explicit agreement.

## MVP — required
1. Cesium terrain around verified incident coordinates, camera markers, clickable video evidence.
2. At least two verified videos of the same incident (two viewpoints preferred; otherwise honest single-view multi-segment fallback).
3. Agent searches and inspects footage, then deliberately selects additional evidence.
4. Timestamped event timeline and clickable claim-to-clip provenance.
5. Spatial overlay: documented camera sites; bearings and candidate intersection only when calibrated.
6. Weave trace or locally logged trace if Weave is unavailable.

## Explicitly out of scope
Operational fire forecasting; 3D reconstruction of flames from monocular video; automatic photogrammetric camera calibration; training a wildfire detector; speculative geolocated fire points; deploying PhysicsNeMo/Earth-2; assuming all wildfire clips are the same incident.

## Repository status
This tree is an **implementation scaffold** plus frozen-path contracts, fixtures, and tickets. Application code under `frontend/` and `backend/` is not yet scaffolded; see ticket backlog. Validate contracts with:

```bash
pip install -r scripts/requirements.txt
python scripts/validate_contracts.py
pytest tests/test_contracts.py
```

## First actions
1. Read `docs/DECISIONS.md`, `docs/INTEGRATION.md`, `docs/INITIAL-MILESTONE-EXECUTION.md`, and `tickets/00-INDEX.md`.
2. Agree on `contracts/schema.json`, `contracts/investigation.schema.json`, and fixture samples; freeze before independent feature work.
3. A starts Cesium + UI + agent on labelled synthetic fixtures. B starts real evidence acquisition + metadata + science adapter.
4. Integrate only via frozen JSON contracts after both tracks meet their acceptance gates.

## Stack
Next.js, TypeScript, Tailwind, CesiumJS, FastAPI/Python, OpenCV, NumPy, NVIDIA Cosmos Reason endpoint, VAST AI OS video search / Cosmos Embed1 if available, CoreWeave hosted inference, W&B Weave tracing. Exact endpoint request formats are **environment-specific** and must be tested at the event.

## Sources
- HPWREN Holy Fire: https://www.hpwren.ucsd.edu/news/20180812/
- HPWREN FIgLib: https://www.hpwren.ucsd.edu/FIgLib/
- NVIDIA VSS: https://docs.nvidia.com/vss/latest/
- VAST AI OS: https://www.vastdata.com/platform/ai-os
- VAST video intelligence: https://www.vastdata.com/blog/unlock-video-intelligence-build-real-time-video-search-and-ai-summary
- CoreWeave serverless: https://docs.coreweave.com/products/inference/serverless
- W&B Weave: https://wandb.ai/site/weave/
- CesiumJS: https://cesium.com/platform/cesiumjs/
