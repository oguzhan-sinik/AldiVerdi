# 01 — Freeze the evidence contract

**Owner:** Developer A  
**Priority:** P0  
**Files owned:** `contracts/schema.json, contracts/investigation.schema.json, fixtures/*, docs/INTEGRATION.md, scripts/validate_contracts.py`  
**Depends on:** None; B reviews and approves the contract

## Goal
Both developers can work independently against one stable incident/evidence format.

## Implementation — smallest useful version
- Inspect the existing schema and fixture IDs.
- Add only fields that are essential for click-to-video provenance: video path/URL, offsets, camera linkage, and optional capture time with timezone or explicit unknown.
- Keep coordinates nullable; distinguish known camera positions from verified camera orientation.
- Label synthetic fixtures with `data_mode: synthetic_fixture`; never present them as source-backed media.
- Run `python scripts/validate_contracts.py` and `pytest tests/test_contracts.py`; record version `v1` and freeze.

## Acceptance criteria
- B confirms the contract can represent a real incident with two videos.
- Fixtures validate (`validate_contracts.py` PASS).
- Each evidence record resolves to a video and bounded time interval within `duration_s`.
- No unverified geolocation or camera heading is required (null + `geometry_status: unavailable`).
- Investigation fixture cites only known evidence IDs and sets `execution_mode: mock`.

## Constraints / do not build
- Do not design a generalized geospatial ontology, database, event bus, or authentication.
- Do not change shared schema after contract approval without explicit joint agreement.

## Deliverable / handoff
A publishes frozen fixture/schema; B consumes them unchanged.
