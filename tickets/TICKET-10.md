# 10 — Camera geometry readiness and B-side smoke test

**Owner:** Developer B  
**Priority:** P0  
**Files owned:** `backend/intelligence/geometry.py, data/processed/geometry-status.md`  
**Depends on:** Tickets 06–09

## Goal
Make the 3D overlay scientifically honest and integration-ready.

## Implementation — smallest useful version
- Implement `camera_geojson(manifest)` returning verified camera Point features only.
- Include `orientation_verified` and leave heading/FOV null when unknown.
- Write a one-paragraph status: camera count, viewpoint count, time alignment status, triangulation readiness.
- Validate GeoJSON output structure.

## Acceptance criteria
- GeoJSON includes no invented fire position.
- Missing headings result in pins without cones.
- B can hand off data without A editing intelligence code.

## Constraints / do not build
- Do not implement ray intersection before two calibrated bearings exist.
- Do not draw speculative viewing cones as observations.

## Deliverable / handoff
B publishes a concise integration handoff and verified camera GeoJSON.
