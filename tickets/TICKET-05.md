# 05 — Minimal investigation orchestrator with mock tools

**Owner:** Developer A  
**Priority:** P0  
**Files owned:** `backend/platform/`  
**Depends on:** Tickets 01–04

## Goal
Prove the UI can display a bounded investigation sequence without relying on live model access.

## Implementation — smallest useful version
- Define typed `search_evidence`, `inspect_clip`, `get_camera` tool interfaces.
- Add a mock investigation response using fixture evidence IDs.
- Render a 3-step trace: search → inspect → report.
- Mark responses as mock; reserve model adapter for later.

## Acceptance criteria
- One investigation can be triggered and yields valid evidence IDs.
- Trace and final finding appear in UI.
- Mock mode is visibly labelled.

## Constraints / do not build
- No complex agent framework, autonomous recursion, prompt tuning, RAG database, or real inference requirement in initial milestone.

## Deliverable / handoff
A supplies callable interfaces for later Cosmos/VAST integration.
