# 06 — Verify incident sources and capture provenance

**Owner:** Developer B  
**Priority:** P0  
**Files owned:** `data/sources/, docs/DATA.md`  
**Depends on:** None; joins contract review in contract approval

## Goal
Select a real wildfire incident and identify at least two usable video segments from the same documented event.

## Implementation — smallest useful version
- Start with HPWREN Holy Fire archive; record canonical source URLs and camera labels.
- Verify footage belongs to the same incident; record source time ranges and download/licensing notes.
- Distinguish two independent camera viewpoints from two segments of one camera.
- Maintain a short evidence ledger with verified/unknown fields.

## Acceptance criteria
- At least two source candidates with provenance, or a documented fallback.
- No claim of synchronized viewpoints without timestamps.
- Every camera coordinate has a source or remains null.

## Constraints / do not build
- Do not scrape an entire archive, download multi-GB datasets, or use unrelated clips as one incident.
- Do not infer headings or timestamps from filename alone.

## Deliverable / handoff
B publishes `data/sources/manifest-notes.md` and candidate video links.
