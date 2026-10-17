# System architecture

## Core flow
`Next.js / Cesium UI → Platform API → Investigation orchestrator → [VAST search, Cosmos reasoning, Developer B CV/geometry tools] → evidence-grounded claims → video viewer + Cesium map`

## Ownership
- A: `frontend/`, `backend/platform/`; UI, map, video resolver, orchestration, VAST API adapter, W&B traces.
- B: `backend/intelligence/`, `data/`; source verification, video assets, Cosmos analysis adapter, CV, geometry.
- Shared: `contracts/`, `fixtures/`, validation scripts and tests; schema changes require joint approval.

## Modules
**Frontend:** incident page; camera list; Cesium viewer; video/evidence panel; agent action and findings panel. No frontend code exists yet; Developer A builds the shell and then Cesium.

**Platform:** fixture/live incident adapter; safe media resolver; VAST retrieval adapter; bounded investigation loop; structured tool dispatcher; trace recorder.

**Intelligence:** source/asset ledger; frame extraction; video observations; optional change metrics; geometry computation; Cosmos adapter only after actual endpoint contract is known.

**Infrastructure:** workshop VM + organizer-provided VAST/CoreWeave services where reachable; Cesium ion terrain if configured; W&B Weave where enabled.

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
