# 07 — Download and normalize two playable clips

**Owner:** Developer B  
**Priority:** P0  
**Files owned:** `data/raw/, data/processed/, scripts/prepare_clips.py`  
**Depends on:** Ticket 06

## Goal
Produce two small, locally playable MP4 clips with stable IDs and offsets.

## Implementation — smallest useful version
- Download the smallest source-backed clips allowed by source terms.
- Use ffmpeg to trim/transcode to H.264 MP4 only if necessary.
- Record original URL, source start offset, clip duration, fps and any timestamp mapping.
- Use deterministic filenames (`video_id.mp4`).

## Acceptance criteria
- Both clips play in a standard browser.
- Metadata is documented; processing does not silently change source-time references.
- Combined sample size stays practical for local dev.

## Constraints / do not build
- No bulk ingest, cloud object storage, elaborate ETL, or 4K preservation.
- If a source is inaccessible or cannot be verified, record the blocker and use a documented fallback.

## Deliverable / handoff
B delivers two clips and manifest for later handoff; A continues with fixtures.
