# Developer A — Complete Continuous Implementation Prompt (Clean Start)

You own `frontend/` and `backend/platform/`. The repository is **empty of application code**: no Ticket 02 implementation exists. Read `PROJECT-AGREEMENT.md`, `docs/SETUP.md`, `docs/ARCHITECTURE.md`, `docs/CONTRACTS.md`, `docs/AGENT.md`, `docs/UX.md`, `docs/INTEGRATION.md`, and the actual JSON schemas/fixtures.

## Phase 0: Contract approval
Run `python3 scripts/validate_contracts.py` and `python3 -m pytest tests/test_contracts.py`. Confirm TS consumer types can represent the current schema. Do not unilaterally modify shared contracts.

## Phase 1: Implement frontend from zero
Create a minimal working Next.js 15 + TypeScript + Tailwind app in `frontend/`. Provide `/` redirect to `/incident/holy-fire-2018`; incident page with three panels: camera list, map placeholder, evidence and investigation rail. Read `fixtures/incident.json` via a fixture/live adapter. Unknown IDs must show explicit errors. Label synthetic data. Build and lint must pass. **Do not claim this phase was already done.**

## Phase 2: Real Cesium
Replace placeholder with browser-safe CesiumJS terrain. Only show verified camera coordinates; fixture cameras with null coords must have no pins. Handle missing Cesium token and lifecycle cleanup.

## Phase 3: Evidence playback
Implement a server-side `video_id` asset resolver supporting approved local MP4 and authorized remote segment URLs. Preserve source provenance, implement range requests if needed, seek to evidence `start_s`, and handle missing media explicitly. Do not treat a news webpage as video.

## Phase 4: VAST retrieval
On the workshop VM inspect organizer skills and team config; verify actual indexed search, metadata and clip retrieval. Implement typed server-side adapter. Do not invent endpoints or claim Holy Fire is indexed without proof. Keep fixture mode honest.

## Phase 5: Autonomous agent
Implement a bounded, evidence-dependent tool loop using the actual investigation contract. Search, inspect, compare, optionally measure and evaluate geometry; validate IDs, cite evidence, expose action trace. Use live Cosmos output only through a verified adapter; W&B Weave tracing only when configured.

## Phase 6: Integration and deployment
Consume B's validated evidence ledger, playable assets and geometry. Run full journey smoke tests; deploy only with organizer-approved workflow.

## Rules
Stay within ownership, avoid overengineering, preserve schemas and real scientific uncertainty. After each phase report changed files, executed tests (PASS/FAIL/BLOCKED/NOT RUN), mock/live status, blockers and next dependency. Continue based on acceptance, not schedules.

**Start now with contract approval and the Next.js shell from zero.**
