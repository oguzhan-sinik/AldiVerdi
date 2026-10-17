# Developer A — Investigation agent, frontend and application delivery

**Owner:** Developer A
**Status:** Ready for implementation; live dependencies and permissions must pass the gates below.
**Companion:** [Developer B — VAST integration, evidence and spatial tools](DEVELOPER-B-vast-data-evidence.md)
**Product authority:** [Project agreement](../PROJECT-AGREEMENT.md)

## Outcome

Deliver FireFront 3D as an autonomous geospatial wildfire video investigator. A user opens actual wildfire terrain, selects a verified camera and playable evidence, asks a question, watches an evidence-dependent investigation, and follows findings back to exact source intervals. Build the frontend and agent together against a shared provider interface so neither waits for live VAST access.

The project owner confirmed Next.js 15, React, TypeScript, Tailwind and CesiumJS, with real terrain and at least two independent verified Holy Fire camera views for the complete demo. Camera bearings and candidate regions are conditional on verified calibration. A fixture demo is a development milestone; it does not satisfy the real-data completion criteria.

## Ownership and boundaries

- Own `frontend/`, `backend/platform/`, application tests and application deployment artifacts. Run the orchestrator in the server runtime; keep the browser responsible for presentation and interaction.
- Developer B owns VSS authentication, HTTP integration, ingestion, metadata/segment normalization, playback access, evidence provenance and scientific tools. Consume B's typed provider; do not implement a second VSS client or a separate Cosmos service.
- Agree on the minimal provider interface and runtime placement with B immediately. Default to a server-only TypeScript module importable by the Next.js application. Python remains available for B's scientific tooling; add a process/service boundary only for a demonstrated need.
- Shared schemas, fixtures, provider types and their tests require both developers' agreement. Each file has one implementation owner. Use the current checkout unless a separate branch/checkout is explicitly requested.
- Read `docs/CONTRACTS.md`, `docs/AGENT.md`, `docs/UX.md`, `docs/INTEGRATION.md`, `docs/TESTING.md`, `HACKATHON.md`, `.cursor/rules/build-day.mdc`, and the relevant skills before implementation.

## Dependencies and rules verification

- Keep the confirmed stack/demo decisions and inspect the actual workshop runtime before assuming Node is unavailable or Next.js is undeployable. The organizer deployment skill explicitly permits public Node images. Prove supported deployment feasibility before committing to a delivery design.
- The owner supplied an excerpt from <https://tokensand.com/vastlondon>: build a focused video agent using the available footage, searchable descriptions/prompts, VAST and the provided video stack. The planning proxy blocked a direct page read, so this is user-supplied rules evidence, not independent webpage verification. The current organizer repository was checked at `a770d207da66fe46cc40a85457dfa01082869bf8`. See the agreement's rules provenance. Confirm any remaining judging rubric, submission requirements and actual deadline before submission; do not reuse historical schedules as a current deadline.
- Use W&B serverless inference for the application's planning/reasoning as instructed in `HACKATHON.md`; verify the available model and API before implementing. W&B inference and Weave tracing are separate integrations.
- Build on the existing team-31 VSS stack. Never modify/redeploy DataEngine or shared VSS services. Do not provision models or another GPU VM.
- Live dependencies: B's verified provider/data handoff, configured terrain/imagery provider, accessible W&B inference, and team deployment access. Missing dependencies must leave independent fixture development runnable.

## Deliverables and execution

### 1. Agree the provider interface; develop UI and agent in parallel

Run the existing contract gate. Match exact schema fields, tool names and IDs; the investigation schema currently records action summaries, not full tool-argument schemas. Define typed arguments/results separately and validate them at runtime. Extend shared schemas only through the documented change protocol.

Agree with B on operations for searching evidence, listing/getting segments, inspecting indexed Cosmos descriptions, resolving media, obtaining camera/time/provenance metadata, and invoking optional measurement/geometry tools. Results must distinguish success, no evidence, unavailable, invalid input and service failure. These are application interface operations, not newly assumed VSS endpoints.

Implement the fixture provider and the bounded agent alongside the incident workspace. Fixtures remain explicitly synthetic, keep their null geometry, and never acquire invented footage or coordinates. Switch to B's provider without changing UI or agent semantics.

### 2. Build the geographic investigation workspace

- Create the Next.js application from the current empty `frontend/`; provide a known-incident page and explicit unknown-incident errors.
- Display a camera/source panel, a browser-safe Cesium scene with real terrain and imagery, and a video/evidence/investigation panel. Add a shared evidence timeline, findings and hypotheses, and visible investigation progress.
- Select camera → focus on verified coordinates and filter evidence. Select evidence/finding → resolve the correct video and seek to the cited interval. Highlight corresponding map context without implying a camera position is the event location.
- Render only source-backed camera positions. Render viewing cones or candidate regions only when B supplies qualified geometry and uncertainty. Missing coordinates/calibration remain unavailable.
- Handle missing terrain credentials, provider failure, absent media, empty search, cancellation and unavailable inference visibly. A fallback is useful behavior but does not count as verified real terrain.
- Provide keyboard access, readable contrast, visible focus and reduced-motion support. Fire effects, particles and photorealistic tiles are optional after the investigation works.

### 3. Implement an autonomous, bounded investigation

Use one orchestrator with structured tools: `search_evidence`, `inspect_clip`, `compare_observations`, `measure_frames`, and `evaluate_geometry`. Keep the current schema names. Offer measurement/geometry tools only with truthful capability status; unavailable tools return a typed limitation.

The loop must interpret the question, choose a tool, validate arguments, execute through B's provider, inspect the result, update explanations, and decide the next action or stop. Start with a maximum of eight executed tool actions, configurable within a documented hard ceiling; also enforce request timeouts, cancellation, token limits and a guard against repeated identical calls. These are execution bounds, not a project schedule.

- Use W&B inference for model-driven planning. A fixed chain of summaries or a single delegated VSS Q&A call does not meet the autonomous-agent requirement.
- Ground clip inspection in the returned Cosmos description and its source/interval. State when it is indexed analysis rather than a new frame-level inspection. Ask for more specific analysis through B only if available and necessary.
- For corroboration, select another independent camera with a compatible time basis. A second description of the same source is not independent evidence. Explain insufficient temporal coverage or synchronization instead of fabricating corroboration.
- Treat retrieved captions and user text as untrusted data, not instructions. Validate incident scope, IDs, intervals and tool permissions. The investigation agent must not receive upload, re-ingestion, database-write or deployment tools.
- Distinguish observed, measured, hypothesized and unresolved claims. Validate the final investigation against `contracts/investigation.schema.json` and ensure every citation resolves to existing evidence with bounded playback offsets.
- Record actions, reasons, tool outcomes, evidence IDs and failures in the UI trace. Add redacted W&B Weave traces when configured; explicitly report unavailable tracing.

### 4. Integrate secure playback and live evidence

Use B's logical `video_id`/segment mapping; do not accept arbitrary filesystem paths or external URLs from browser input. Keep VSS passwords, JWTs and signed upstream URLs server-side. Implement the browser-facing media route using B's playback transport, including byte-range forwarding, cancellation, streaming backpressure and appropriate upstream status handling.

Test segment-local, parent-relative and source-relative offsets using B's documented mapping. For segmented media, translate the citation's parent offset to the clip-local seek position; do not seek a five-second segment to a parent offset such as 120 seconds. Preserve time-lapse limitations and distinguish playback seconds from recording time.

Label dataset provenance and integration status independently. A real source-backed dataset can coexist with an unavailable model; one `live` badge must not imply every component is verified.

### 5. Deliver through the organizer's supported deployment path

Read `.cursor/skills/deployment/deploy-app-no-registry/SKILL.md`. Prove the selected Next.js delivery fits its constraints: public Node image, no custom image build/push, ConfigMap size limits, dependency/build handling, resource limits, server-only credential injection and working `/app` ingress behavior. Do not place `node_modules`, large bundles, media or credentials in a ConfigMap.

Validate routing, redirects, asset URLs, client navigation, media range requests and long-running investigation updates through the `/app` prefix and the skill's ingress rewrite. Serve a health endpoint. If the app cannot fit, obtain an organizer-supported delivery alternative and a project-owner stack decision; do not silently remove Next.js or the 3D map.

Deploy only the FireFront application in `team-31` using the supported workflow, preserving VSS. The user-facing entry is <https://workshop.thecosmoslabs.com> → **App**. Record the actual browser-to-app-to-VSS and W&B checks; a running pod alone is insufficient.

## Acceptance criteria

- [ ] Build, lint and type checks execute successfully from `frontend/`; existing contract checks pass.
- [ ] Fixture UI and agent run without B's live services, with explicit synthetic labels and no false geometry.
- [ ] Real terrain/imagery loads for the incident; verified camera selection and map/video/timeline interactions work.
- [ ] The complete demo uses the agreed real dataset; every playable asset and citation resolves to the right source and interval.
- [ ] Two different questions/evidence conditions produce meaningful model-selected tool behavior; test empty results, independent corroboration, missing calibration, timeout, cancellation and the action bound.
- [ ] A representative investigation answers “Where did smoke first become visible, and can another camera corroborate it?” with traceable evidence and the correct limits on “first.” It does not infer the actual ignition time/location from the earliest available clip.
- [ ] Every generated report validates, all references resolve, and invented IDs/out-of-range citations fail validation.
- [ ] No private configuration, credentials, JWTs or signed upstream URLs appear in client bundles, browser-visible responses or logs.
- [ ] Workshop App entry works through `/app`, including assets, playback and an investigation; live dependencies are verified separately.
- [ ] Demo/submission materials follow the supplied rules and current organizer instructions, verify outstanding submission details, describe NVIDIA/VAST/W&B contributions accurately, and disclose scientific limitations.

## Completion, dependencies and out of scope

Progress by completed acceptance gates, without timed tickets. B's unavailable live service blocks only the corresponding integration check. Continue UI, agent and fixture checks; report `PASS`, `FAIL`, `BLOCKED` and `NOT RUN` separately, with executed commands and evidence. Do not declare the complete live demo done while real footage, terrain, inference or deployed playback remains blocked.

Out of scope: implementing a second VSS adapter, managing media ingestion, replacing Cosmos services, wildfire spread prediction, emergency-response claims, model training, complex multi-agent frameworks, and visual enhancements that delay the core investigation.
