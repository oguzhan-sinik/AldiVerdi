# Developer A — Continuous Implementation Specification

**Role:** Platform, CesiumJS, video UX, VAST retrieval, autonomous investigation and observability.

## Start from the real baseline
The previous agent reported completing the Next.js 15 + TypeScript + Tailwind three-panel shell, fixture/live adapter, camera list, map placeholder and evidence panel; build/lint/route smoke tests passed. **Do not rebuild Ticket 02.** Inspect current code and Git status before editing. Read `PROJECT-AGREEMENT.md`, `docs/CURRENT-STATE.md`, `docs/SETUP.md`, `docs/CONTRACTS.md`, `docs/ARCHITECTURE.md`, and this document.

## Workstream 1 — Cesium map
Replace `MapPlaceholder` with a browser-safe Cesium viewer. Render actual terrain or explicit fallback. Show verified camera markers only; map selection must connect to camera list and evidence panel. Do not invent coordinates or orientation. Handle lifecycle cleanup and no-token errors. Run build/lint and route smoke tests.

## Workstream 2 — Playable evidence
Implement safe server-side `video_id` resolution from B's asset ledger and/or approved VAST segment URLs. A source webpage is not a media URL. Support local MP4 range requests and seeking to evidence-relative `start_s`, video switching, missing media, invalid offsets and provenance display. Use schema-valid fixtures until real media is available.

## Workstream 3 — VAST connectivity
Read actual organizer skills/config on workshop VM. Test an existing approved indexed video search and clip retrieval. Implement server-side typed search adapter. Verify custom wildfire ingestion before treating wildfire videos as searchable in VAST. Do not invent API schemas, deploy another DataEngine, or expose secrets in client JS.

## Workstream 4 — Agent
Build one bounded orchestrator with structured tool selection: search evidence, inspect clip, compare observations, optional CV measurements and optional geometry readiness. Tool choices must depend on prior results. Validate arguments, prevent hallucinated IDs, bound calls and failures, distinguish mock and live, produce cited claims. Use actual Cosmos outputs where accessible; coordinate video analysis interface with B. W&B inference (if used) is distinct from Weave tracing.

## Workstream 5 — Observability and integration
Instrument investigation steps with Weave when configured. Consume B's contract-valid evidence, media mappings and GeoJSON. End-to-end test incident → camera → media seek → agent actions → cited finding → map. Deploy only through supported organizer workflow and only when local checks pass.

## Rules
- Own `frontend/` and `backend/platform/`; do not edit B's `backend/intelligence/` or `data/` without coordination.
- Do not unilaterally edit `contracts/`.
- Preserve existing code, tests and current IDs.
- Continue when acceptance checks pass; no time-based planning.
- Avoid speculative frameworks and unnecessary refactors.
- Do not mark live VAST/Cosmos/Weave as complete until exercised.

## Required report after each completed capability
State what works, changed files, executed validation commands and results, mock/live status, blockers, B handoff needs and next eligible capability.

**Begin with Cesium real terrain and verified camera marker behavior.**
