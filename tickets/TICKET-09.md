# 09 — Create fast video frame and change tools

**Owner:** Developer B  
**Window:** T+01:25–T+01:50 (elapsed hackathon time)  
**Priority:** P1  
**Files owned:** `backend/intelligence/video_tools.py, tests/`  
**Depends on:** Tickets 07–08

## Goal
Supply reliable lightweight visual evidence tools that Cosmos can later call.

## Implementation — smallest useful version
- Implement `extract_frames(video_id, start_s, end_s, max_frames=6)`.
- Implement `frame_difference(video_id, t1, t2)` using grayscale resized OpenCV frames.
- Return file paths, requested/actual timestamps, and an image-change score with no physical interpretation.
- Test on one real clip.

## Acceptance criteria
- Two frame extractions and one difference calculation work.
- Out-of-range timestamps produce a clear error.
- Output labels the score as image change, not fire intensity or fire growth.

## Constraints / do not build
- No SAM2, detector training, optical flow, fire propagation, or fragile vision pipeline.
- Avoid generating thousands of frames.

## Deliverable / handoff
B exposes two simple Python functions for later agent tool wrappers.
