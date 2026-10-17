# FireFront 3D — Project Agreement (Canonical)

## Mission
FireFront 3D is an autonomous, evidence-grounded **geospatial wildfire video investigator**. It connects genuine multi-view wildfire footage to an interactive CesiumJS terrain interface. A user asks a question; the investigation agent retrieves, inspects, compares and measures relevant footage, then produces findings with source video IDs and playable timestamps.

**This is not a wildfire spread forecast, emergency-response decision system, or a smoke-detector demo.** Video-agent reasoning must be central to the product.

## Agreed user journey
1. Open an incident on a real 3D map.
2. Select a verified camera or evidence item and inspect its video.
3. Ask a question (e.g. where smoke first appeared, or whether another camera corroborates it).
4. Observe an autonomous, bounded investigation using search, clip inspection, comparisons and optional measurement tools.
5. Open evidence citations to exact video-relative offsets.
6. See spatial observations only where the camera's verified geometry supports them.
7. Distinguish observed, measured, hypothesized and unresolved claims.

## Technical decisions
- Frontend: Next.js 15, React, TypeScript, Tailwind, CesiumJS.
- Investigation: one clear orchestrator with typed tools; not an unnecessarily complex multi-agent framework.
- Video intelligence: NVIDIA Cosmos reasoning; VAST video search/metadata where actual supported endpoints and dataset access exist.
- Measurements: Python, OpenCV, FFmpeg/ffprobe.
- Geometry: verified camera metadata, bearings, viewing cones and **conditional** triangulation; no invented locations.
- Infrastructure: hackathon's provided VAST environment and CoreWeave-hosted endpoints if accessible. Do not redeploy provided DataEngine or self-host models without a demonstrated need.
- Observability: W&B Weave if configured.
- Prefer minimal implementation over speculative abstraction.

## Data strategy
Preferred candidate: **2018 Holy Fire**, documented by HPWREN (https://www.hpwren.ucsd.edu/news/20180812/). Backup candidate: 2025 Palisades Fire. These are **candidates**, not verified or approved video assets. Before download, ingestion or public redistribution, check original asset URLs, independent viewpoints, timestamps, camera locations, and usage rights. The hackathon's pre-indexed corpus may not include wildfire footage; custom ingestion must be confirmed with organizers.

## Two independent developer tracks
**Developer A** owns `frontend/`, `backend/platform/`, Cesium, playback UI, agent orchestration, VAST retrieval integration and W&B tracing.

**Developer B** owns `backend/intelligence/`, `data/`, provenance, video preprocessing, Cosmos video-analysis adapter, OpenCV and scientific geometry.

The existing repository's validated contracts, IDs and tests are the integration boundary. No unilateral schema changes.

## Existing baseline (as reported, not independently verified in this document)
- Contract validation passes; seven pytest contract tests pass.
- Developer A completed the Next.js application shell, fixture/live adapter, camera list, map placeholder and evidence panel; build/lint/route smoke tests passed.
- Cesium real map, playable media, agent, live integrations, real footage and geometry are **not yet demonstrated**.
- Developer B has read the current docs but has not begun implementation.

## Development process
Two continuous implementation tracks replace ten active tickets. Historical ticket acceptance criteria may inform the tracks, but **`docs/DEVELOPER-A.md` and `docs/DEVELOPER-B.md` are the active execution instructions**. No fixed-duration planning, artificial checkpoints or schedule-driven handoffs. Proceed when dependencies and acceptance checks pass.

## Scientific integrity
- Never fabricate source URLs, camera coordinates, headings, absolute recording timestamps, evidence, citations or model outputs.
- `fixture`, `mock`, `source-backed`, `live` and `unavailable` states must be explicit.
- A single camera generally gives a direction, not a precise ground coordinate.
- Time-lapse playback seconds are not necessarily recording seconds.
- A model description is not independent corroboration of itself.
- A precise geographic point requires sufficient calibrated geometry and a documented uncertainty model.
- If metadata is missing, report the limitation and render no false spatial certainty.

## Success criteria
A real or honestly labelled fixture-backed incident opens; real terrain works; playable evidence seeks correctly; the agent makes meaningful tool choices and produces traceable claims; multiple views are compared when available; real VAST/Cosmos connectivity is demonstrated before being advertised as live.
