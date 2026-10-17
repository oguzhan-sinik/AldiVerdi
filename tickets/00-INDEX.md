# FireFront 3D — Initial ticket backlog (01–10)

No clocks, deadlines, fixed-duration windows, or scheduled handoffs. **Advance only when a ticket passes its acceptance criteria.**

## Independent work tracks

| Developer A — Platform & Agent | Developer B — Video, Data & CV |
|---|---|
| 01 Contract and fixtures | 06 Verify incident footage and provenance |
| 02 App shell | 07 Acquire playable clips |
| 03 Cesium terrain and camera markers | 08 Export source-backed manifest |
| 04 Evidence viewer and seek | 09 OpenCV frame tools |
| 05 Mock investigation trace | 10 Camera geometry readiness |

**Contract gate:** A proposes the minimum shared schema; B confirms it can represent actual assets and unknown metadata. Once accepted, both tracks proceed independently.

**Integration gate:** A demonstrates fixture-backed map → camera → evidence playback → investigation trace. B supplies validated JSON and playable source-backed media. Swap fixtures for real assets only after both deliverables pass; fix mismatches at the boundary, not by cross-editing each other's code.

**Scientific gate:** Do not present camera-bearing intersections as triangulation without verified independent viewpoints, orientations, and corresponding events. A map with verified camera pins and evidence is a valid fallback.

**Rule:** Stop at acceptance criteria. No extra infrastructure, premature abstraction, speculative features, or work on another developer's owned files. If blocked, document it and apply the specified fallback.
