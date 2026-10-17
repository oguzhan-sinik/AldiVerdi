# FireFront 3D — Project Agreement & Source of Truth

## Confirmed implementation decisions — 2026-10-17

These decisions apply to the pasted project goal below and supersede earlier ticket plans:

- **Stack:** Next.js 15, React, TypeScript, Tailwind and CesiumJS. Prove feasibility of the organizer-supported deployment before committing to a delivery design. Do not silently switch to Python/static HTML because one VM lacks Node.
- **Complete demo:** real geographic terrain and at least two independent, verified Holy Fire camera views. Localization, viewing cones and triangulation require adequate metadata/calibration. Fixture or single-camera demonstrations are interim states.
- **Developer A:** build frontend and autonomous agent together; own application API/media routes, W&B planning/traces and application delivery.
- **Developer B:** own all VAST access, the server-only provider, authorized ingestion, source-backed evidence, timing/provenance and scientific tools. A consumes B's provider instead of writing a second VSS adapter.
- **Existing services:** reuse VSS ingestion, Cosmos Reason, Cosmos Embed and retrieval; do not deploy or call separate Cosmos services for routine capabilities already provided by VSS.
- **Active work:** only [Developer A's ticket](tickets/DEVELOPER-A-platform-agent-frontend.md) and [Developer B's ticket](tickets/DEVELOPER-B-vast-data-evidence.md). The pages in `docs/DEVELOPER-A.md` and `docs/DEVELOPER-B.md` are entry points to these tickets.
- **Permissions:** the owner has not confirmed organizer approval for external Holy Fire footage. B must document it and asset rights before further acquisition/ingestion. Approval is an implementation dependency, not a claim that it already exists.
- **Current state:** this checkout contains schemas, synthetic fixtures, docs and skills, with no implemented frontend/backend or verified real dataset. Historical VM diagnostics must be rechecked on that VM. These tickets plan implementation; writing them does not establish live integration readiness.

## Hackathon rules and evidence

The owner supplied this excerpt from <https://tokensand.com/vastlondon> after the planning environment's proxy blocked direct access:

> Build a video agent that searches footage, answers questions, spots events, or takes action. One idea, working by the end of the day.
>
> Pick a specific use case: “flag someone missing a hard hat,” rather than “watch for safety issues.” Adapt your idea to the footage available on build day.
>
> Search depends on what the model’s prompt captures in each video description. You can ingest video with a different prompt on build day.

The supplied partner descriptions identify VAST AI OS for ingestion/storage/indexing; VSS Blueprint and Cosmos for searchable descriptions/embeddings; Cursor for event development; and CoreWeave/W&B for inference, experiment tracking and observability. This is user-provided event text, not an independent live-page check or a complete judging rubric.

Current upstream <https://github.com/vast-data/vast-builders-challenge/tree/main> was checked at commit `a770d207da66fe46cc40a85457dfa01082869bf8`. Its `README.md` matches this repository's `HACKATHON.md`. The relevant copied retrieval, upload and no-registry deployment skills match upstream; differences in the architecture/rules files only redirect README references to `HACKATHON.md`.

Apply the checked organizer guidance: use the existing team-31 stack and skills, use W&B serverless inference for application reasoning, keep credentials private, and deliver through the supported team Kubernetes `/app` workflow. The deployment skill permits public Node images as well as Python; it imposes ConfigMap/packaging constraints that A must test, not assume impossible.

The organizer README also says not to ingest internet footage. General upload/prompt support does not resolve that specific external-footage restriction. B records permission and rights; no messages to organizers are sent automatically. A confirms any remaining current submission instructions, judging rubric and actual deadline before submission. No copied historical time is treated as the current deadline, and the implementation plan has no fixed schedule.

**Project:** FireFront 3D
**Category:** Autonomous Video AI / Geospatial Intelligence / Scientific Investigation
**Purpose:** Hackathon project using NVIDIA video intelligence, VAST infrastructure, and an interactive 3D geographic environment.

## 1. What we are building

FireFront 3D is an **autonomous, multi-camera wildfire investigation platform** that transforms real wildfire footage into geographically contextualized, timestamped, verifiable evidence.

Instead of simply detecting smoke or predicting wildfire spread, the platform investigates what is happening across multiple video sources.

Users can explore a real wildfire location in a 3D environment, select cameras, watch footage, and ask an AI agent questions about the incident.

The agent autonomously searches relevant footage, investigates observations, compares evidence across cameras, performs scientific measurements when necessary, and produces findings supported by video timestamps.

**Our core innovation is connecting autonomous video reasoning with real-world spatial investigation.**

The 3D map is not just a visualization. It represents camera positions, viewing directions, candidate event locations, and the geographic context of the agent's findings.

## 2. The problem

Wildfire incidents may be recorded by multiple cameras, including stationary monitoring cameras, drones, and thermal sensors.

These recordings contain valuable evidence, but understanding their relationship is difficult.

Important observations may be distributed across different videos and timestamps. A smoke plume visible from one camera might be obscured from another. An apparent new ignition could instead be the result of existing fire spreading, camera movement, or previously hidden activity.

Existing workflows often require people to manually examine footage and determine which observations correspond to the same event.

FireFront aims to automate parts of that investigation while preserving transparency and uncertainty.

## 3. The intended user experience

The user opens FireFront and sees a visually impressive 3D map of a real wildfire area.

The terrain should represent the actual geography rather than a fictional landscape.

Available video sources appear as camera markers at their verified locations.

Where orientation information is available, cameras can display viewing directions or viewing cones.

The user can select a camera and watch its associated wildfire footage.

A timeline allows navigation through the available recordings and events.

The user can then ask questions such as:

- Where did smoke first become visible?
- Which camera first recorded the suspected ignition?
- Can another camera corroborate this observation?
- Did a separate fire appear away from the original front?
- What changed between these two observations?
- Where might this observed event be located geographically?

The agent investigates using available video evidence and scientific tools.

Its findings appear in the interface with clickable source references.

Selecting a finding should navigate to the corresponding footage and, when supported by metadata, its geographic context.

## 4. The central video-agent requirement

We explicitly rejected an earlier design in which wildfire prediction was the primary product.

That approach could largely be implemented using OpenCV, segmentation, and numerical modelling without meaningful video-agent reasoning.

**The redesigned FireFront must genuinely depend on video agents.**

The agent should:

1. Understand the investigation question.
2. Determine which video evidence may be relevant.
3. Retrieve footage using semantic search.
4. Inspect video segments using a video reasoning model.
5. Identify important observations and potential inconsistencies.
6. Form or evaluate competing explanations.
7. Decide whether additional footage or measurements are needed.
8. Invoke the appropriate video or spatial tools.
9. Update its investigation based on the results.
10. Produce an evidence-grounded report.

The agent's actions should depend on the evidence it discovers.

A fixed sequence of predetermined video summaries is not sufficient.

## 5. The 3D geographic environment

We agreed to use a real geographic environment as the visual foundation of the platform.

**Preferred technology: CesiumJS.**

CesiumJS is suitable for geographic coordinates, real terrain, camera placement, spatial entities, and map navigation.

Next.js and React will provide the surrounding application.

Three.js can be used for additional visual effects if needed, but building the entire geographic environment manually with raw Three.js is not the preferred approach.

Google Photorealistic 3D Tiles were considered as a possible enhancement, particularly for populated areas.

However, the initial implementation should prioritize reliable terrain rendering rather than depending on Google 3D Tiles access.

### Expected 3D capabilities

- Real terrain and satellite imagery.
- Camera markers at verified geographic positions.
- Camera selection and navigation.
- Viewing cones when camera orientation is sufficiently known.
- Candidate event locations.
- Geographic evidence overlays.
- Smooth transitions between relevant cameras.
- A connection between the investigation timeline and spatial visualization.

Animated fire perimeters, advanced particles, and photorealistic effects are optional enhancements.

They must not take priority over the core investigation workflow.

## 6. Multi-video investigation

We agreed that FireFront should support multiple videos associated with a single real wildfire incident.

These videos may come from different monitoring cameras, drone footage, or other documented sources.

The system should preserve the identity of each source and avoid treating unrelated videos as part of the same incident.

The agent should be able to retrieve and compare observations across sources.

### Selected incident target

**2018 Holy Fire — Santiago Peak, California.**

The HPWREN archive was identified as a promising source because it documents multiple camera views of the same wildfire and provides historical footage.

Reference:

https://www.hpwren.ucsd.edu/news/20180812/

### Backup candidate requiring owner approval

**2025 Palisades Fire — California.**

Multi-camera ALERTCalifornia footage was identified as a possible alternative.

### Important limitation

Holy Fire is the confirmed complete-demo target. This does not establish that usable footage, permission or calibration metadata have already been obtained. A fallback incident requires the project owner's decision.

Before claiming a multi-camera reconstruction, we must verify:

- That the selected videos belong to the same incident.
- That the relevant footage is accessible.
- That camera identities are known.
- That recording times can be interpreted correctly.
- That camera positions are documented.
- That orientation metadata is available or can be calibrated.
- That the observations being compared actually correspond to the same event.

If precise spatial reconstruction is not supported, the system must still provide useful video investigation without fabricating geographic results.

## 7. Video-to-map localization

One of our key differentiating features is connecting observations from video footage to geographic locations.

The proposed process is:

1. A video model identifies a relevant smoke or fire observation.
2. A vision tool identifies an approximate image region.
3. The system uses the camera's verified geographic position and calibrated orientation to derive a viewing direction.
4. Another camera provides a second observation of the same event.
5. The spatial engine combines compatible viewing directions to estimate a candidate geographic region.
6. The 3D map displays the result with appropriate uncertainty.

This is a geometric calculation, not something the language model should invent.

A single camera usually provides a direction rather than a precise geographic location.

Two calibrated cameras may support triangulation, but accuracy depends on camera geometry, event correspondence, and the observed target.

Smoke height and terrain visibility can introduce additional uncertainty.

**We will never represent unsupported triangulation as an accurate result.**

## 8. Technical architecture

### Frontend

- Next.js
- React
- TypeScript
- CesiumJS
- Interactive video player
- Investigation workspace
- Timeline
- Camera and evidence selection
- Hypothesis and findings panels

### Agent orchestration

- A bounded investigation loop.
- Structured tool calls.
- Evidence retrieval.
- Video inspection.
- Hypothesis evaluation.
- Scientific tool invocation.
- Evidence-grounded reporting.

### Video intelligence

- NVIDIA Cosmos video reasoning through the existing VSS ingestion/retrieval infrastructure.
- VAST video indexing and retrieval.
- Cosmos embeddings where available.
- OpenCV and Python utilities.
- Frame extraction and comparison.
- Video metadata processing.
- Source provenance tracking.

### Spatial intelligence

- Camera coordinates.
- Camera orientation.
- Viewing direction calculations.
- Geographic coordinate transformations.
- Candidate event localization.
- Triangulation where justified.
- Explicit uncertainty handling.

### Infrastructure and observability

- CoreWeave for available model inference services.
- W&B serverless inference for application reasoning; W&B Weave for agent execution traces when configured.
- VAST infrastructure for video storage, indexing, and retrieval where supported by the available environment.

Exact API endpoints, model versions, authentication, and deployment capabilities must be verified against the actual infrastructure.

## 9. Division of work

We agreed to divide development into two largely independent tracks.

### Developer A — Platform & Agent Systems

Responsible for:

- Next.js application.
- Frontend architecture.
- CesiumJS integration.
- 3D map visualization.
- Camera markers and map interactions.
- Video viewer and timeline.
- Investigation interface.
- Agent orchestration.
- Tool planning and execution.
- Consuming Developer B's typed VSS provider for retrieval, indexed analysis and private playback.
- W&B serverless inference for agent planning, using provided CoreWeave infrastructure.
- W&B Weave tracing.
- Final user-facing investigation workflow.

Developer A should use validated fixture responses when Developer B's services are not yet available.

### Developer B — VAST Integration, Video Intelligence & Spatial Science

Responsible for:

- All VAST access: team-31 configuration discovery, authentication, HTTP adapter, search, metadata, segments, ingestion readiness and private playback transport.
- Finding and verifying wildfire video sources.
- Downloading and preparing video footage.
- Incident and camera metadata.
- Video preprocessing.
- Existing VSS/Cosmos analysis integration; reuse the deployed Reason/Embed pipeline rather than create separate services.
- OpenCV measurements.
- Frame extraction and temporal alignment.
- Camera calibration.
- Geographic calculations.
- Viewing cones and bearings.
- Triangulation where possible.
- Scientific validity and evidence provenance.
- Producing structured outputs for Developer A.

Developer B should not depend on the frontend implementation.

### Shared integration

Both developers must use the same agreed data contracts.

Integration should occur when the required interfaces and deliverables are ready.

We explicitly removed fixed development schedules and time-based ticket planning.

**Development is now completion-driven, not clock-driven.**

## 10. Engineering principles

We agreed that the codebase should be:

- Small and understandable.
- Modular without unnecessary abstraction.
- Built around explicit contracts.
- Easy for two independent coding agents to work on.
- Practical for a hackathon.
- Focused on demonstrable functionality.
- Honest about model and data limitations.

Avoid:

- Bloated frameworks.
- Unnecessary microservices.
- Premature optimization.
- Speculative infrastructure.
- Large amounts of boilerplate.
- Complex multi-agent architectures without justification.
- Rewriting working components.
- Implementing optional features before core functionality works.

Each implementation ticket should define its deliverables, constraints, acceptance criteria, dependencies, and out-of-scope work.

Each developer owns one continuous ticket, validates its acceptance criteria, reports actual outcomes and coordinates the companion handoff. There are exactly two active tickets.

## 11. Scope priorities

### Essential functionality

- Working 3D geographic environment.
- At least one genuine wildfire incident.
- At least two independent, verified Holy Fire camera views; temporal segments from one camera do not satisfy this requirement.
- Selectable video evidence.
- Correct timestamps and provenance.
- Functional video reasoning.
- Evidence retrieval.
- An investigation agent that selects tools based on findings.
- A visible investigation trace.
- Evidence-grounded conclusions.

### Important enhancements

- Cross-camera event comparison.
- Camera viewing cones.
- Geographic event localization.
- Hypothesis comparison.
- OpenCV-based measurements.
- Spatial uncertainty visualization.
- Agent-directed map transitions.

### Optional enhancements

- Photorealistic 3D tiles.
- Animated fire perimeters.
- Advanced smoke and fire effects.
- Complex thermal segmentation.
- Wildfire spread forecasting.
- Sophisticated physical simulations.

The optional features should not delay the essential investigation system.

## 12. Scientific and product constraints

FireFront must not:

- Invent geographic metadata.
- Fabricate video evidence.
- Invent timestamps.
- Assume unrelated footage is synchronized.
- Present model speculation as observed fact.
- Claim a precise ignition point without sufficient evidence.
- Treat approximate computer vision detections as ground truth.
- Present the system as a validated emergency response product.
- Claim that an external integration works without testing it.

Findings should distinguish observations, measurements, hypotheses, and unresolved questions.

The user must be able to inspect the supporting evidence.

## 13. Intended demonstration

The ideal demonstration begins with a 3D map of a real wildfire area.

Multiple cameras are visible around the terrain.

The user asks:

**"Where did the fire first become visible, and can another camera corroborate it?"**

The agent retrieves relevant footage.

A video reasoning model identifies an observation.

The map focuses on the corresponding camera.

The agent determines that another viewpoint could provide useful evidence.

It searches another camera's recordings and examines the relevant segment.

The map moves to the second camera.

Where calibrated geometry supports it, viewing directions are displayed and combined to highlight a candidate region.

The final report explains what the footage supports, what remains uncertain, and which video timestamps justify the findings.

The agent's investigation steps should be visible through the interface and trace logs.

This demonstrates autonomous video reasoning, evidence retrieval, scientific tools, and geospatial visualization in one coherent workflow.

## 14. What is not yet decided or verified

The following are not final implementation facts:

- Exact usable video assets.
- Final verified Holy Fire asset set and permitted ingestion status.
- Availability of all required camera calibration metadata.
- Actual model endpoint schemas and authentication.
- Whether automatic triangulation is feasible for the selected footage.
- Whether photorealistic tiles will be used.
- Whether real wildfire perimeter data can be integrated.
- Final deployment infrastructure.
- Which optional visual effects will be implemented.

These should be resolved through source verification, integration testing, and implementation results.

They must not be treated as completed capabilities.

## 15. Definition of success

FireFront succeeds when it demonstrates a coherent investigation in which:

1. Real wildfire footage is linked to a real geographic environment.
2. Video evidence can be selected and inspected.
3. The agent autonomously decides what evidence to examine.
4. NVIDIA video reasoning contributes meaningfully to the investigation.
5. Multiple observations can be compared where supported.
6. Spatial tools provide geographic context without inventing precision.
7. Findings remain traceable to original evidence.
8. The application is visually compelling and technically credible.

**Final agreed positioning:**

FireFront 3D is an autonomous geospatial video investigation system that connects real wildfire footage, AI-driven evidence discovery, multi-camera reasoning, and geographic reconstruction into one interactive experience.

Its differentiator is not wildfire detection alone, nor a 3D map alone, but the combination of an agent that investigates visual evidence and a spatial interface that makes its findings understandable and verifiable.
