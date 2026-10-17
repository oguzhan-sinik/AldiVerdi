# 7-hour execution plan — zero blocking by design

| Time | Developer A — platform + agent | Developer B — video + science | Integration rule |
|---|---|---|---|
| 00:00–00:20 | Create Next.js shell, define client interface | Create dataset manifest skeleton, define evidence output | Joint freeze `contracts/` by 00:20 |
| 00:20–01:10 | Cesium terrain + camera pins using fixtures | Verify Holy Fire sources, acquire 2 videos, log provenance | Independent branches |
| 01:10–02:00 | UI rails, video player, clickable timeline using fixtures | Segment clips, establish source timestamps, draft Cosmos prompts | Independent branches |
| 02:00–02:30 | Agent planner + fixture tools + action feed | Cosmos smoke test + first real observations | B publishes JSON; A reads at 02:30 |
| 02:30–03:30 | Swap to real evidence adapter; VAST search if available | OpenCV visual change tools + camera metadata validation | Contract-only communication |
| 03:30–04:30 | Investigation hypotheses, Weave traces, source citations | Camera bearing geometry, test ray intersection or mark unavailable | Independent branches |
| 04:30–04:50 | Joint API integration and smoke tests | Joint API integration and smoke tests | Single planned pair checkpoint |
| 04:50–05:45 | Map fly-to actions, polished incident UI | Improve evidence alignment and geometry reliability | Independent branches |
| 05:45–06:00 | Freeze features, open merge PR | Freeze science outputs, open merge PR | Controlled merge |
| 06:00–06:30 | End-to-end rehearsal, fix platform bugs | End-to-end rehearsal, fix data/model bugs | Pair testing, no new features |
| 06:30–07:00 | Demo narration, final submission | Backup video, verify source provenance | Release only |

## Critical path
Two source videos → source metadata → Cosmos observations → evidence IDs → agent retrieves second observation → clickable map-linked finding.

## Pivot deadlines
- 01:00: if multi-view Holy Fire data not viable, switch to verified same-incident segments.
- 02:30: if Cosmos unavailable, cache actual tested observations or use manually reviewed evidence clearly labeled.
- 04:30: if orientation missing, remove triangulation feature from demo.
- 05:45: no new features, only bug fixes.

## Coordination
Only 3 mandatory synchronous checkpoints (00:20, 02:30, 04:30) plus release. Avoid parallel edits to contracts and common configuration. Developer A integrates B's artifacts; B does not modify the UI.
