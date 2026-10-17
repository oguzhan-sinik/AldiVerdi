# 01 — Freeze the evidence contract

**Owner:** Developer A  
**Window:** T+00:00–T+00:20 (elapsed hackathon time)  
**Priority:** P0  
**Files owned:** `contracts/schema.json, fixtures/*, docs/INTEGRATION.md`  
**Depends on:** None; B reviews for 10 minutes

## Goal
Both developers can work independently against one stable incident/evidence format.

## Implementation — smallest useful version
- Inspect the existing schema and fixture IDs.
- Add only fields that are essential for click-to-video provenance: video path/URL, offsets, camera linkage, and optional capture time with timezone or explicit unknown.
- Keep coordinates nullable; distinguish known camera positions from verified camera orientation.
- Run a JSON Schema validation of fixture(s); record version `v1` and freeze.

## Acceptance criteria
- B confirms the contract can represent a real incident with two videos.
- Fixture validates.
- Each evidence record resolves to a video and bounded time interval.
- No unverified geolocation or camera heading is required.

## Constraints / do not build
- Do not design a generalized geospatial ontology, database, event bus, or authentication.
- Do not change shared schema after T+00:20 without explicit joint agreement.

## Deliverable / handoff
A publishes frozen fixture/schema; B consumes them unchanged.
