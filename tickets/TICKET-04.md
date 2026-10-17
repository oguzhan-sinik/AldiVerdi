# 04 — Evidence viewer and timeline

**Owner:** Developer A  
**Priority:** P0  
**Files owned:** `frontend/components/EvidenceViewer.tsx, frontend/components/EvidenceTimeline.tsx`  
**Depends on:** Tickets 01–03

## Goal
Clicking a timestamped observation opens the right video at the right moment.

## Implementation — smallest useful version
- Use native HTML5 video.
- Resolve `evidence_id → video_id → playable URL`, and seek to `start_s`.
- Show evidence text and `observed/inferred/unresolved` status.
- Display time offsets, not invented wall-clock timestamps.
- Implement previous/next evidence navigation only if trivial.

## Acceptance criteria
- Clicking at least two fixture evidence entries changes clip/time.
- Missing media gives a clear unavailable state.
- Evidence always identifies its source video.

## Constraints / do not build
- No synchronized multicam player, waveform, custom transcoding, timeline editor, or elaborate video controls.

## Deliverable / handoff
A has a clickable fixture-based demo independent of B.
