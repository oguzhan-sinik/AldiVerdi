# 03 — Render real terrain and camera markers

**Owner:** Developer A  
**Window:** T+00:45–T+01:20 (elapsed hackathon time)  
**Priority:** P0  
**Files owned:** `frontend/components/IncidentMap.tsx, frontend/lib/map.ts`  
**Depends on:** Tickets 01–02

## Goal
The 3D map shows the documented incident region and verified camera locations.

## Implementation — smallest useful version
- Load CesiumJS client-side only; configure terrain provider/token.
- Center on documented Holy Fire/Santiago Peak incident region, using source-backed coordinates.
- Render camera pins only when lat/lon are known.
- Clicking a pin selects its camera ID in app state.
- If Cesium fails, show a simple 2D map or geographic list.

## Acceptance criteria
- Terrain displays in browser; no SSR crash.
- Camera click updates selected camera ID.
- Unknown locations never appear as fabricated pins.

## Constraints / do not build
- No Google photorealistic tiles, custom shaders, particle fires, 3D fire reconstruction, automatic bearing cones, or geolocation guesses.

## Deliverable / handoff
A exposes `selectedCameraId` for the evidence viewer.
