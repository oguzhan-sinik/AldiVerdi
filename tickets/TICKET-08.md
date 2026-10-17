# 08 — Produce incident JSON and evidence ledger

**Owner:** Developer B  
**Priority:** P0  
**Files owned:** `data/processed/incident.json, data/processed/evidence.json`  
**Depends on:** Tickets 01, 06–07

## Goal
Represent the real footage in the frozen contract, with at least two timestamped observations.

## Implementation — smallest useful version
- Assign stable `incident_id`, `camera_id`, `video_id`, `evidence_id`.
- Extract source-backed camera metadata, otherwise null.
- Record 2–4 manually verified observations with video-relative offsets and status `observed`.
- Validate against `contracts/schema.json` without modifying it.

## Acceptance criteria
- Manifest validates against frozen schema.
- Each evidence time lies within its video duration.
- Each observation links to an existing local video.

## Constraints / do not build
- No synthetic event observations presented as real.
- No automatic geolocation, timestamp extrapolation, or schema edits.

## Deliverable / handoff
B provides JSON and playable media for the integration gate.
