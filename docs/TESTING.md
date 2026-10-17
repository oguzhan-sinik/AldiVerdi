# Acceptance and validation gates

## Shared contracts
- `python3 scripts/validate_contracts.py`
- `python3 -m pytest tests/test_contracts.py`
- Validate all new source-backed records and cross-references; no extra schema properties.

## Developer A
- `npm run build`, `npm run lint` from `frontend/`.
- Open known incident and unknown incident.
- Cesium terrain loads or explicit fallback; verified markers only.
- Media resolver handles valid/missing IDs, range requests and seek offsets.
- Agent validates tool args, bounds execution and cites real evidence.
- Mock/live UI labelling accurate.
- VAST/Cosmos/W&B status tested separately.

## Developer B
- ffprobe identifies source and derivative assets; hashes recorded.
- Frame extraction succeeds at valid offset and fails safely outside bounds.
- Time-lapse mapping tested against documented anchors.
- JSON evidence validates against actual schema.
- Geometry known-case synthetic tests pass; missing calibration yields no invented point.
- Cosmos adapter uses real documented request schema; live only when tested.

## Integration
Incident → camera → video → evidence seek → investigation question → tool actions → cited findings → map context. Run fixture end-to-end first, then source-backed, then live external integrations where available.

## Reporting
Each developer reports `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN` for actual checks, changed files, outstanding blockers and next dependency. No time estimates or time-based milestones.
