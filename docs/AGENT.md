# Agent and sponsor integrations — Developer A

## Agent state
`question`, `incident_id`, `hypotheses[]`, `evidence_ids[]`, `actions[]`, `open_questions[]`, `budget_remaining`, `status`.

## Tools
Canonical MVP names (must match `contracts/investigation.schema.json` and tickets 05+):
- `search_evidence(incident_id, query, camera_ids?, time_range?)` → evidence hits with `evidence_id` / `video_id`.
- `inspect_clip(video_id, start_s, end_s, question)` → B's Cosmos analysis output with bounded video-relative timestamps.
- `get_camera(camera_id)` → position/orientation and verification state.
- `select_next_evidence(reason, candidate_ids)` → adaptive choice of next evidence IDs.
- `compare_observations(evidence_ids)` → consistency/contradiction and time constraints.
- `localize_event(evidence_ids)` → B's candidate bearing geometry, uncertainty or unavailable reason.
- `get_temporal_changes(video_id, range)` → B's OpenCV measurements.
- `summarize_findings(evidence_ids)` / `finish_report()` → claims with provenance and epistemic labels.

Do not invent tool names at runtime. Reject model/tool output that cites unknown `evidence_id` values.

## Agent loop
1. Interpret question and choose 2–3 candidate hypotheses.
2. Search relevant clips; inspect top hit with Cosmos.
3. Ask: what observation could falsify this hypothesis? Select different camera or earlier timestamp.
4. Inspect additional evidence and optionally call geometry / CV tools.
5. Stop after 4–6 tool calls or evidence sufficiency; report uncertainty.

## Sponsor responsibilities
- **VAST**: index custom wildfire clips, metadata and semantic retrieval where supported; fallback local manifest and embeddings.
- **Cosmos Reason**: event interpretation on selected clips/frames; not pixel-exact localization or physics.
- **CoreWeave**: hosted inference transport; endpoint URL and model-specific payload validated onsite.
- **W&B Weave**: trace each search/inspect/compare call, latency, errors and final report; avoid sending credentials or unnecessarily sensitive data.

## Strict reporting schema
Every `claim` must carry `status: observed|measured|inferred|unresolved`, `evidence_ids`, and optional `limitations`. Never use `confirmed ignition location` when only a smoke bearing was estimated.

## Evaluation
Test that the agent: (a) cites real evidence, (b) asks for a second observation when needed, (c) stops when geometry is uncalibrated, (d) refuses to combine unrelated incidents, (e) returns within action budget.
