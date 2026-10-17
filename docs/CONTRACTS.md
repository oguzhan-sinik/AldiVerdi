# Shared contracts and integration rules

## Authority
The **current checked-in** `contracts/schema.json` and `contracts/investigation.schema.json` are canonical. The audit reportedly added fields including `data_mode`, `playback_status`, `segment_id`, `model`, `limitations`, `alt_m`, `geometry_status`, `recording_start_utc`, `timestamp_basis`, `rights_note`, and `measured` status. **Do not assume every listed field exists at every nesting level:** inspect actual JSON Schema. It reportedly sets `additionalProperties: false`, so extra fields are invalid.

## Stable identity
Use exact existing incident, camera, video, evidence and action IDs. All references must resolve; no synthetic ID masquerades as real footage. `video_id` is a logical identifier, not a file path.

## Time
- `start_s`/`end_s` are video-relative playback offsets unless contract explicitly states otherwise.
- `recording_start_utc` is meaningful only with a verified clock basis.
- Time-lapse footage may have non-linear real-time mapping. Store verified playback-to-recording anchors in the **asset ledger**; do not infer a ratio from duration.
- Do not synthesize wall-clock times for evidence.

## Local playback
Convention: `data/processed/<video_id>.mp4`. The platform's media resolver maps logical video ID to an approved local or remote playable resource; it must not expose arbitrary filesystem paths. Do not add `local_path` to frozen incident objects without joint schema revision.

## Canonical outputs
- `data/sources/manifest-notes.md`: source provenance, rights, view independence, gaps.
- `data/processed/asset-ledger.csv`: canonical asset mapping and temporal transformations.
- `data/evidence.json`: source-backed observations, if this is consistent with existing validated consumers.
- `data/geometry.geojson`: verified geographic features only.
- `data/geometry-status.md`: spatial readiness and limitations.
Avoid duplicate authoritative `observations.json` or conflicting schema variants.

## Change protocol
1. Explain why existing contract cannot express a required verified use case.
2. Propose the smallest backwards-compatible schema change.
3. Obtain A+B sign-off before editing shared contracts.
4. Update fixtures, TS/Python consumers and tests together.
5. Rerun `scripts/validate_contracts.py` and pytest.
6. Record migration notes in commit/PR description.

## Acceptance
All schema validations pass, no unresolved references, explicit mock/source-backed flags, no fabricated spatial data, and video offsets resolvable through the agreed asset ledger.
