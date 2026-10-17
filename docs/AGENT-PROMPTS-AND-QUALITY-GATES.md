# Copy-ready coding-agent instructions and quality gates

## Prompt for Developer A's coding agent
You are implementing Developer A's platform/agent track of FireFront 3D. Read `README.md`, `docs/DECISIONS.md`, `docs/ARCHITECTURE.md`, `docs/INTEGRATION.md`, `contracts/schema.json`, `fixtures/incident.json`, `fixtures/investigation.json`, `docs/AGENT-IMPLEMENTATION-BRIEF.md`, and `docs/INITIAL-MILESTONE-EXECUTION.md`. Implement ONLY tickets 01–05 in order. Own only `frontend/` and `backend/platform/`. Use fixtures, not invented real-world data. Prefer direct components/functions over extra abstractions. After each ticket, run the relevant test, list changed files and show one screenshot/brief behavior report. If blocked by an external dependency, implement the documented fallback and move on. Never modify shared contracts without explicit approval. Stop after acceptance criteria; do not begin future tickets.

## Prompt for Developer B's coding agent
You are implementing Developer B's video/data/science track of FireFront 3D. Read `README.md`, `docs/DATA.md`, `docs/SPATIAL.md`, `docs/INTEGRATION.md`, `contracts/schema.json`, `docs/INTELLIGENCE-IMPLEMENTATION-BRIEF.md`, `docs/SOURCE-VERIFICATION-GATE.md`, and `docs/INITIAL-MILESTONE-EXECUTION.md`. Implement ONLY tickets 06–10 in order. Own only `backend/intelligence/` and `data/`. Use real source-backed video; never invent coordinates, headings, time sync or observations. Export schema-valid JSON, an asset ledger, frames, and conditional geometry. Keep scripts small and CLI-driven. After each ticket, report evidence URLs, validation outputs, and blockers. If no second video is verifiable, activate single-camera fallback. Do not edit platform code or shared contracts. Stop at acceptance criteria.

## Per-ticket completion report (mandatory)
```text
Ticket: XX
Status: DONE | PARTIAL | BLOCKED
Changed files:
How to run:
Acceptance checks actually run:
Evidence/source URLs (if applicable):
Known limitations:
Handoff artifact:
Next ticket:
```

## Definition of done
- App starts or script executes with documented commands.
- No hardcoded fabricated geography or timestamp claims.
- Evidence IDs resolve to a playable asset and valid interval.
- Model output explicitly distinguishes mock, cached, and live.
- No new dependency without a direct reason.
- One clear failure state for each external service.
- Existing files and contracts remain backward compatible.

## Scope-cut order if blocked
Cut in order: animated cones -> multi-source geometry -> live planner -> video semantic search -> cosmetic polish. Preserve: verified footage, evidence click-through, real terrain or fallback, visible agent action trace, source attribution.
