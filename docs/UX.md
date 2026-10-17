# UX / web application — Developer A

## Visual hierarchy
**Full-screen Cesium terrain** is the hero. Left rail: incident library and cameras. Right rail: investigation question, agent actions, hypothesis board. Bottom: synchronized evidence timeline. Clicking a claim flies to its camera and opens video at `start_s`.

## Map entities
- Real terrain and imagery with attribution.
- Camera pins with verification state.
- Direction wedges only if orientation is calibrated.
- Candidate event area with uncertainty and provenance, never an unsupported fire perimeter.
- Camera-to-evidence links and fly-to transitions.

## Core screens
1. Incident overview: Holy Fire context, cameras, source library.
2. Investigation: ask question, stream tool actions, open evidence.
3. Evidence review: video player, source credits, time interval, visual observation.
4. Findings: chronological report, verified/inferred/unresolved claims, supporting citations.

## Visual polish
Dark graphite/navy surfaces, restrained orange fire accents, teal for confirmed geometry, amber for uncertainty. Animate only real state transitions. Avoid fake confidence percentages and simulated inference indicators.

## Fixture-first development
Frontend renders from `fixtures/incident.json` and `fixtures/investigation.json`. Implement a single `EvidenceClient` interface; switch from fixture to real API with environment flag, no UI rewrite.

## Demo choreography
Initial 3D flyover → user question → search highlight → camera A video opens → agent requests camera B → map flies to camera B → evidence compare → candidate sightlines (if calibrated) → report with clickable sources.
