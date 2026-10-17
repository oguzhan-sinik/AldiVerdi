# System architecture

## Core flow
`Next.js / Cesium UI → Platform API → Investigation orchestrator → Developer B provider [existing VSS search, indexed Cosmos descriptions, media, optional CV/geometry] → evidence-grounded claims → video viewer + Cesium map`

## Ownership
- A: `frontend/`, `backend/platform/`; UI, map, browser-facing media routes, orchestration, W&B inference/traces and application delivery.
- B: `backend/intelligence/`, `data/`; the single VSS authentication/HTTP adapter and media transport, source verification, video assets, indexed Cosmos analysis, CV and geometry.
- Shared: `contracts/`, `fixtures/`, validation scripts and tests; schema changes require joint approval.

## Modules
**Frontend:** incident page; camera list; Cesium viewer; video/evidence panel; agent action and findings panel. No frontend code exists yet; Developer A builds the shell and then Cesium.

**Platform:** fixture/live incident consumer; safe media routes backed by B's transport; bounded investigation loop; structured tool dispatcher; trace recorder. A builds UI and orchestration together against B's agreed provider interface.

**Intelligence:** server-only typed VSS provider, source/asset ledger, identifier and time mappings, private media transport, frame extraction, video observations, optional change metrics and geometry computation. Use existing VSS Reason/Embed infrastructure; a separate Cosmos service is not part of the default architecture.

**Infrastructure:** workshop VM + existing team-31 VSS/CoreWeave services; configured real terrain/imagery; W&B serverless inference for planning and Weave where enabled. A must prove Next.js fits the supported Kubernetes `/app` workflow, including packaging and prefix/rewrite behavior, before committing to a deployment design.

## Integration strategy
Fixtures must be fully valid and explicitly synthetic. Implement real adapters behind the same consumer interfaces. Never infer that a source webpage is a playable MP4. Never treat VAST pre-indexed surveillance footage as Holy Fire evidence.

## Failure behavior
- No Cesium token: render an honest fallback, never pretend 3D terrain is loaded.
- Missing camera lat/lon: no marker.
- Missing heading/FOV: no calibrated viewing cone.
- Missing video asset: unavailable playback status and clear UI message.
- Missing inference endpoint: block live inference; do not silently substitute mock output while labelling live.
- Missing synchronized camera observations: no triangulated point.

## Non-goals
Earth-2, PhysicsNeMo, fire-spread prediction, distributed microservices, model training, arbitrary media upload systems, photogrammetric 3D reconstruction and speculative optimization.
