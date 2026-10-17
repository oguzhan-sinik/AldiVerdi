# 02 — Launch the platform shell

**Owner:** Developer A  
**Window:** T+00:20–T+00:45 (elapsed hackathon time)  
**Priority:** P0  
**Files owned:** `frontend/`  
**Depends on:** Ticket 01

## Goal
A usable local app with a three-panel investigation layout and fixture data.

## Implementation — smallest useful version
- Scaffold Next.js/TypeScript/Tailwind if not present.
- Create one `/incident/[id]` route and static panels: camera list, map placeholder, evidence panel.
- Read `fixtures/incident.json` through a small adapter.
- Include loading/error states and one consistent dark theme.

## Acceptance criteria
- `npm run dev` loads without errors.
- One fixture incident and camera list render.
- No backend is needed to navigate the page.

## Constraints / do not build
- No global state framework, component library migration, login, animations, or premature abstraction.
- Maximum one route and 3–5 components.

## Deliverable / handoff
A screenshots the page; no dependency on B.
