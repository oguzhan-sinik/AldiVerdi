# Agent and sponsor integrations — Developer A

## Agent state
`question`, `incident_id`, `hypotheses[]`, `evidence_ids[]`, `actions[]`, `open_questions[]`, `budget_remaining`, `status`.

## Tools
- `search_evidence(incident_id, query, camera_ids?, time_range?)` → evidence hits with video/segment IDs.
- `inspect_video(segment_id, question)` → B's Cosmos analysis output with bounded segment timestamps.
- `get_camera(camera_id)` → position/orientation and verification state.
- `compare_observations(evidence_ids)` → consistency/contradiction and time constraints.
- `localize_event(evidence_ids)` → B's candidate bearing geometry, uncertainty or unavailable reason.
- `get_temporal_changes(video_id, range)` → B's OpenCV measurements.
- `finish_report()` → claims with provenance and epistemic labels.

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
Every `claim` must carry `status: observed|inferred|unresolved`, `evidence_ids`, and optional `limitations`. Never use `confirmed ignition location` when only a smoke bearing was estimated.

## Evaluation
Test that the agent: (a) cites real evidence, (b) asks for a second observation when needed, (c) stops when geometry is uncalibrated, (d) refuses to combine unrelated incidents, (e) returns within action budget.
