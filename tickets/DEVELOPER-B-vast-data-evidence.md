# Developer B — VAST access, video evidence and spatial tools

**Owner:** Developer B
**Status:** Ready for implementation; external-footage approval and live capabilities remain verification gates.
**Companion:** [Developer A — Investigation agent, frontend and application delivery](DEVELOPER-A-platform-agent-frontend.md)
**Product authority:** [Project agreement](../PROJECT-AGREEMENT.md)

## Outcome

Give Developer A one verified, server-only interface to team-31's existing VSS infrastructure and a source-backed wildfire dataset. Own everything required to access VAST: configuration discovery, authentication, HTTP contracts, ingestion readiness, search, segment descriptions/metadata, playable media, and the mapping to FireFront's evidence contracts. Supply optional measurements and defensible geographic context.

The confirmed complete-demo target is real terrain and at least two independent verified Holy Fire camera views. The pre-indexed organizer corpus can prove infrastructure connectivity but cannot be relabelled as wildfire evidence. A successful upload or a segmented S3 object alone does not establish indexing or semantic searchability.

## Ownership and boundaries

- Own `backend/intelligence/`, `data/`, integration tests and public-safe VSS operating instructions. Place the importable server-only VSS adapter under `backend/intelligence/vss/`; agree its TypeScript interface with A before either builds an incompatible client. Keep Python scientific/processing tools separate and small.
- A owns the frontend, orchestrator, browser-facing API/media routes and application deployment. Hand A a playback transport with the range/status semantics needed by that route, not a browser-visible VSS JWT.
- Shared schemas, fixtures and provider types require A+B review. Keep the strict incident/investigation schemas unchanged unless a real use case requires the smallest coordinated extension. Prefer a separate typed asset ledger for VSS mapping over adding undeclared incident fields.
- Read `docs/CONTRACTS.md`, `docs/DATA.md`, `docs/SPATIAL.md`, `docs/INTEGRATION.md`, `docs/TESTING.md`, `HACKATHON.md`, `.cursor/rules/build-day.mdc` and the relevant ingest/retrieval skills.

## Dependencies and current evidence

The checkout contains schemas, synthetic fixtures, validation and organizer skills; it contains no application, real media, VSS adapter or calibrated geometry. The planning cloud session has no `/config` and cannot reach the VSS host through its proxy. Read actual runtime configuration on the workshop VM; do not assume this cloud machine is that VM.

The removed alignment ticket reported two unsuccessful Holy Fire test uploads, approximately 0.5-fps media rejected by a 4-fps Cosmos sampling path, absent model URL variables and no Node on the VM. These are historical reports, not checks performed for this plan. Recheck the actual assets, available tools and logs before treating them as current facts; do not change pipeline functions to accommodate them.

Organizer documentation restricts ingestion of internet footage, despite the presence of an upload API. Record explicit organizer permission for external Holy Fire footage and per-asset rights before additional acquisition, upload or re-ingestion. The owner supplied the event-page excerpt in the project agreement; it allows prompt-driven ingestion in general but does not confirm permission for external footage. The current organizer repository was checked at `a770d207da66fe46cc40a85457dfa01082869bf8`. Do not post messages to organizers automatically or infer approval from successful prior uploads.

## Deliverables and execution

### 1. Verify the actual team-31 environment

Use the existing workshop connection and checkout. Confirm hostname/workspace, locate the team's `/config/*.config` and Kubernetes configuration, and read installed skills. Never search repository `team-configs/`, print full configuration, or expose secrets.

Report variable names/presence only: `INGRESS_URL`, `USERNAME`, `PASSWORD`; deployment aliases may be `VSS_URL`, `VSS_USERNAME`, `VSS_PASSWORD`. Separate W&B inference (`WANDB_API_KEY`, `WANDB_TEAM`, `WANDB_PROJECT`) and terrain readiness for A. Optional direct S3/VastDB/model variables are not prerequisites for the HTTP adapter. Check current tools without assuming a missing global SDK means HTTP access is unavailable.

Follow `retrieval/login`, cache the JWT server-side, and verify authenticated identity. Inspect real responses from metadata schema/values, ingest configuration, explore, dashboard and one segment. Capture a concise sanitized contract report in `backend/intelligence/vss/README.md`: methods, paths, required inputs, response fields/types, pagination, identifiers, timing semantics, errors, ACL behavior and actual check outcomes. Do not save tokens, passwords, authentication headers, signed URLs or private configuration dumps.

### 2. Implement the single VSS adapter for A

Use the documented backend API and validate its actual responses at the boundary:

| Capability | Documented API to verify |
|---|---|
| Authentication | `POST /api/v1/auth/login`, `GET /api/v1/auth/me` |
| Filter discovery | `GET /api/v1/metadata/schema`, `/metadata/values`, `/metadata/ingest-config` |
| Search | `POST /api/v1/search` |
| Inventory/health of indexing | `GET /api/v1/videos/explore`, `/dashboard/stats` |
| Parent segments / one segment | `GET /api/v1/tools/segments?original_video=…`, `/tools/segment?source=…` |
| Indexed description and detections | `GET /api/v1/videos/metadata?source=…`, `/videos/detections?source=…` |
| Media | `GET /api/v1/videos/stream?source=…&token=…`, `/videos/playback-url?source=…&token=…` |
| Optional existing Q&A/summary | `POST /api/v1/agent/ask`, `/agent/search-and-answer`, `/videos/synthesize` |

These are documented candidates; mark them live only after a successful target-specific check. Use the skill's requests before raw SDK/database work. Do not invent missing endpoints or silently change teams.

Provide typed operations that A can call for search, parent/segment inspection, indexed Cosmos descriptions, logical-ID mapping and media transport. Discover real camera/location/capture-type values before applying filters, page complete inventories, and scope wildfire searches to the approved incident/source inventory. Normalize absent fields and distinguish no matches, authorization failure, unavailable analysis and malformed data.

Implement timeouts, cancellation, bounded retry for transient errors, and one controlled refresh after expired authentication. Keep private values out of diagnostics. Use HTTPS where supported; never disable TLS verification to make connectivity pass. Playback query tokens/signed URLs remain internal to the server transport.

Skills are agent instructions, not running RPC services. Reuse their verified HTTP contract in the adapter. The pipeline already calls Cosmos Reason and Cosmos Embed; do not deploy them or call separate model endpoints for routine retrieval. A's autonomous loop consumes this provider rather than delegating its entire investigation to a single Q&A endpoint.

### 3. Verify and prepare the real wildfire dataset

Start with the team's existing Holy Fire test assets. Check original source, incident, independent camera identities, rights, permitted use, file duration, frame rate, capture timestamps and any transformations. Prefer HPWREN 2018 Holy Fire; evaluate Palisades only if the project owner approves a fallback and rights/access are verified.

Write `data/sources/manifest-notes.md` with source citations, rights/organizer decision, view independence and gaps. Keep original authorized bytes intact. Store derivatives outside Git under the existing media conventions and record hashes, size, codec, dimensions, duration, frame rate, camera ID and original/derived relationships in `data/processed/asset-ledger.csv`.

If actual ingestion fails because the model samples faster than a low-fps input, create a compliant constant-frame-rate derivative after confirming the required sampling rate. Increasing output frame rate by duplicating frames must preserve playback duration and presentation timestamps; do not speed up footage or claim added temporal information. Re-probe the output and document every transformation. Preserve/verify time-lapse recording anchors independently.

Before uploading, read live extension/size limits from `/api/v1/config` and prompt/capture options from ingest configuration. Create a wildfire prompt within the reported maximum (currently documented as 800 characters) covering visible smoke/fire onset, change, uncertainty and absence, without asking the model to invent geographic coordinates or recording time.

Follow `ingest/upload-video` or the matching re-ingestion skill, with selected assets, visibility, prompt and metadata confirmed before mutation. Upload one file at a time and retain the returned object key. Do not delete old uploads or alter shared databases/pipeline settings as a shortcut.

Prove each target becomes indexed: segment rows exist, explore/dashboard shows the expected complete parent, Cosmos descriptions are present, and an incident-scoped semantic query returns the actual clip. Recheck failed ingestion using specific errors; uploaded/segmented/detected/indexed/searchable are distinct states. YOLO's ordinary object classes are not a smoke/fire detector.

### 4. Produce the evidence and playback handoff

- Provide stable FireFront incident/camera/video/evidence IDs and mappings to the actual `original_video`, `source`, `stream_id`, chunk and segment identifiers returned by VSS. Read the real response fields; never synthesize object paths as proof of existence.
- Store canonical source-backed observations in `data/evidence.json` as agreed in `docs/CONTRACTS.md`. Agree the incident assembly interface with A before adding any second authoritative incident/evidence file.
- Use the existing ledger for logical asset mappings, source provenance, VSS identifiers and timing transformations. No signed URLs or access tokens belong in it. Deliver sample records validated against the current incident schema through the agreed assembly path.
- Establish segment-local offsets, offsets within a parent chunk/upload, source-video offsets and any stream chunk offset separately. Verify the meaning of returned `best_match_start_sec/end_sec` and metadata timing fields using actual playback. Document exact conversion to clip-local seek positions.
- Prove playback through the VSS stream or URL resolver and A's intended server transport, including byte ranges and seek to a cited interval. Persist stable IDs; resolve expiring URLs at runtime.
- Preserve unknown recording times as unknown. “First visible” means first within the inspected coverage; lack of synchronized cameras prevents chronological comparison. Do not use ingest timestamps as capture timestamps.
- Preserve model identity and analysis provenance. Expose Cosmos-generated descriptions through search/metadata, state whether inspection used indexed captions or fresh analysis, and manually check a representative caption against its source clip. The original custom prompt may not be recoverable from VSS rows; keep the approved prompt text and ingestion record separately.

### 5. Supply measurements and truthful spatial context

Deliver verified camera coordinates and source references in `data/geometry.geojson`, plus `data/geometry-status.md` describing uncertainty and missing calibration. Unknown values stay null. Keep location filter labels separate from actual geographic coordinates.

Provide small frame-extraction/comparison tools only where they help investigate real evidence. Verify offsets and variable-frame-rate behavior; optional change scores are measurements, not proof of ignition. Test with approved or explicitly synthetic media.

Viewing cones require verified orientation/FOV. Bearing estimates and triangulation require calibration, independent observations of the same event, compatible recording-time mapping and an uncertainty model. Test known synthetic geometries and degenerate/missing-data cases before any real estimate. Return insufficient metadata instead of an invented point. Advanced reconstruction is conditional; source-backed camera positions and useful video investigation remain required.

## Acceptance criteria

- [ ] Team-31 identity/configuration and required service access are checked on the actual workshop runtime; sanitized response contracts and capability status are recorded.
- [ ] A can import/use the provider without implementing VSS authentication, REST calls, identifier mapping or private playback resolution again.
- [ ] Provider tests cover malformed responses, pagination, expired auth, unavailable services, empty results, incident isolation and secret redaction. Live checks are reported separately from fixture tests.
- [ ] External-footage permission and asset rights are documented before further ingestion; each selected source has traceable identity/provenance.
- [ ] The agreed real dataset is indexed, has Cosmos descriptions and is returned by incident-scoped semantic search. The complete demo includes at least two independent verified Holy Fire views.
- [ ] IDs, durations, source/parent/segment offsets and recording-time limits are validated; representative playback and seeking work without credentials reaching the browser.
- [ ] Source-backed incident/evidence output conforms to the agreed strict schema; existing contract checks pass and A's citation resolver consumes it.
- [ ] Verified camera positions render through A's consumer; unknown calibration produces an explicit unavailable/insufficient result, with no fabricated event point.
- [ ] Any implemented CV/geometry tools have meaningful known-case and failure checks; absent optional tools are reported as unavailable.
- [ ] Handoff includes executed commands/outcomes, a redacted integration guide, dataset/geometry limitations, retained files and restart/runtime requirements. A reproduces at least one search → segment inspection → evidence playback journey.

## Completion, dependencies and out of scope

Proceed by acceptance, without a fixed schedule. Deliver the provider types and labelled fixture examples early so A develops agent and UI concurrently. While rights/access/ingestion is blocked, continue schema mapping, tests, scientific metadata and source verification; mark the blocked live criteria accurately. Fixture success does not complete the live data handoff.

Out of scope: owning the UI or investigation planner, creating another retrieval service, retraining/self-hosting Cosmos, redeploying VSS/DataEngine, uncontrolled batch ingestion, direct database writes, unsupported precision, or claiming a smoke-capable YOLO model without evidence.
