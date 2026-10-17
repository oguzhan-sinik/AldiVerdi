# Autonomous investigation behavior

## Mission
The agent is not a scripted summary generator. It must make bounded evidence-dependent choices, using real tool outputs when available.

## Tool concepts
- `search_evidence(query, filters)`: VAST semantic search only when actual endpoint and relevant indexed corpus are verified; otherwise labelled fixture/local fallback.
- `inspect_clip(video_id, start_s, end_s)`: inspect a real segment with Cosmos when available, or a clearly labelled fixture.
- `compare_observations(evidence_ids)`: contrast multiple independent observations; identify inconsistencies.
- `measure_frames(video_id, offsets)`: call Developer B's OpenCV tool for relevant visual changes.
- `evaluate_geometry(evidence_ids)`: request bearing/triangulation readiness, not invented coordinates.

Actual names and arguments must match **current** validated investigation schema. Do not introduce `inspect_video` versus `inspect_clip` drift.

## Loop
Question → choose tool → validate arguments → execute → inspect result → update hypotheses → choose next useful action or stop → cited report. Limit actions and avoid repeated calls with identical inputs. A failure or missing service is an explicit tool result.

## Claim model
Observed: directly visible in footage; measured: tool-derived quantity; hypothesized: interpretation; unresolved: unsupported. Cite exact video IDs and offsets for substantive claims. Never hallucinate IDs, sources or confidence.

## W&B
W&B serverless inference and W&B Weave tracing are separate. Record action sequence, arguments with secrets redacted, outcomes, evidence IDs and failures. A mock trace is not a live agent run.

## Minimal acceptance
A user question produces a reproducible, bounded, validated investigation trace; clickable citations resolve; findings do not exceed the evidence.
