# Developer A — Platform and agent coding brief

## Mission
Build a visually strong **working** 3D incident investigation interface with an agent whose tool choices are visible and evidence citations open the correct clip. Use fixture data until B hands off validated evidence JSON. Own `frontend/` and `backend/platform/` exclusively.

## The first screen (required)
- Full-height CesiumJS terrain viewport centered on **source-verified incident region**, not a guessed camera position.
- Small left incident/camera list with camera name and verification status.
- Evidence drawer with video player, timestamp, source URL, observation, and uncertainty.
- Right investigation panel with the question, ordered tool actions, retrieved evidence IDs, and final finding.
- Every evidence row is clickable: selects video and seeks to `start_s`.
- Map pin click selects `camera_id` and filters relevant evidence. Unknown camera coordinates => show list entry, **no pin**.

## Implementation shape
- Next.js App Router + TypeScript + Tailwind, Cesium loaded **client-only** (`dynamic(..., {ssr:false})`).
- One state container is sufficient: `selectedIncidentId`, `selectedCameraId`, `selectedEvidenceId`, `investigation`, `status`.
- A small typed `api.ts` adapter should support `mode=fixture|live`. Do not scatter fixture imports throughout UI.
- Reuse `contracts/schema.json` field names. Do not rename `camera_id`, `video_id`, `evidence_id`, `start_s`, `end_s`.
- If video is cross-origin/unplayable, show explicit error + source link; never show an unrelated clip as a substitute.
- Browser seek uses seconds relative to the **actual video asset**, not incident UTC time. Separate the two concepts.

## Agent MVP
Implement a deterministic investigation orchestrator in mock mode, not a fake free-form autonomous LLM. Trace example:
1. `search_evidence({incident_id, query})`
2. `inspect_clip({video_id, start_s, end_s, question})`
3. `select_next_evidence({reason, candidate_ids})`
4. `summarize_findings({evidence_ids})`
Store `{step, tool, args, result, evidence_ids, elapsed_ms, status}` for UI and later Weave.
When live model access arrives, replace **only the planner and tool adapters**. Every final claim must cite evidence IDs that exist in the manifest. Reject model output with unknown IDs.

## Required empty/error states
- Terrain token missing => clearly labeled geographic list fallback.
- No verified camera coordinates => list, no speculative pins.
- No videos => dataset gate blocked, do not populate fake wildfire footage.
- Model unavailable => fixture/demo replay badge.
- Retrieval empty => 'No matching evidence' and a suggested narrower question.

## Explicit non-goals for initial milestones
No authentication, billing, chat history DB, global app state framework, 3D fire particles, satellite texture customization, Google tiles, multi-user realtime, websocket streaming, or complex planner framework.

## Acceptance test
Load fixture incident, select a camera, click evidence, player seeks to exact `start_s`, action trace shows at least two **different** tools, unknown coordinates don't render a pin, terrain fallback works. Capture a short browser recording.

## Integration handoff to B
Consume B's JSON via the adapter. B must not edit your UI. If fields differ, show a validation error and resolve via contract owner instead of adding ad hoc conversions across components.
