# Ticket board — assign by ownership, no cross-edits

**Definition of Done:** reproducible behavior, tested against fixture or actual footage, source provenance intact, failure mode documented. P0 required; P1 nice-to-have; P2 only after demo works.

| ID | Owner | Priority | ETA | Ticket | Depends on | Acceptance |
|---|---|---|---|---|---|---|
| S00 | A+B | P0 | 20m | Freeze IDs/schema/fixture contracts | none | both approve fixture and API names |
| A01 | A | P0 | 40m | Cesium terrain scene and incident fly-to | S00 | real terrain/coordinates or labeled fallback |
| A02 | A | P0 | 35m | Camera markers and evidence video drawer | S00 | click marker opens matching video |
| A03 | A | P0 | 40m | Timeline and claim-to-timestamp jump | S00 | evidence click seeks correct seconds |
| A04 | A | P0 | 45m | Bounded investigation planner with typed tool calls | S00 | adaptive second action, max budget |
| A05 | A | P0 | 45m | VAST search adapter with local fallback | S00 | returns same evidence schema in both modes |
| A06 | A | P0 | 35m | Cosmos/inspection tool adapter and errors | S00 | validated tool args, no silent hallucinations |
| A07 | A | P1 | 30m | Hypothesis and findings board | A04 | each claim links to evidence and status |
| A08 | A | P1 | 25m | W&B Weave trace and local trace fallback | A04 | visible step sequence and timings |
| A09 | A | P1 | 30m | Cinematic fly-to and map overlays | A01,A02 | map changes with agent evidence choice |
| B01 | B | P0 | 50m | Acquire same-incident source videos and credits | S00 | 2 real playable assets and source URLs |
| B02 | B | P0 | 35m | Camera/time metadata and verification ledger | B01 | no invented orientation or UTC times |
| B03 | B | P0 | 40m | Video segmentation and evidence offsets | B01 | segment IDs and correct original time mapping |
| B04 | B | P0 | 45m | Cosmos visual inspection and structured output | B03 | observation JSON with citations and limitations |
| B05 | B | P0 | 30m | Evidence manifest/API contract export | B02,B04 | validates against shared schema |
| B06 | B | P1 | 40m | OpenCV visual change measurements | B03 | outputs image-space metrics with limits |
| B07 | B | P1 | 45m | Camera bearings and uncertainty GeoJSON | B02 | geometry only when calibrated |
| B08 | B | P1 | 25m | Synthetic triangulation and negative tests | B07 | rejects near-parallel and invalid cases |
| I01 | A+B | P0 | 20m | Real evidence integration checkpoint | A02,B05 | no UI or science source cross-edits |
| I02 | A+B | P0 | 20m | Agent-to-science tool integration | A04,B05 | agent retrieves real second clip |
| I03 | A+B | P0 | 30m | Demo smoke test and release freeze | I02 | 90s demo works twice |

## Suggested issue labels
`owner:A`, `owner:B`, `owner:shared`, `P0`, `P1`, `blocked`, `integration`, `data-risk`, `demo`.

## Strict ownership rule
Developer A never edits `backend/intelligence/` or `data/`; Developer B never edits `frontend/` or `backend/platform/`. Only `S00` and scheduled checkpoints can modify `contracts/` and `fixtures/`. Any schema change requires a short versioned migration note.
