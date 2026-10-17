# Initial milestone — acceptance-driven execution for tickets 01–10

This replaces the time-boxed FIRST-2H-EXECUTION document. **Do not schedule work by clock time.** Each developer pulls their next ticket when the preceding ticket is demonstrably complete.

## Developer A

**01 — Shared contract:** Inspect `contracts/schema.json` and fixtures. Agree on stable incident/camera/video/evidence IDs, nullable coordinates, and the distinction between video-relative offsets and real-world recording time. One valid fixture and B's approval are the gate.

**02 — App shell:** A single dark Next.js page with map, evidence panel, and investigation rail. `npm run dev` works; no extra routes, auth, or global state framework.

**03 — Map:** Client-only Cesium terrain, verified camera pins, camera selection state. Graceful fallback to a geographic list if terrain provider is unavailable. Never fabricate positions.

**04 — Evidence viewer:** Click evidence → resolve `video_id` → load correct media → seek to `start_s` after metadata loads. Show provenance, interval, and uncertainty. Test two fixture entries and invalid media.

**05 — Investigation trace:** Show fixture-driven `search_evidence` → `inspect_clip` with clickable citations. Label mock execution explicitly. No model orchestration required at this gate.

## Developer B

**06 — Source provenance:** Verify Holy Fire incident assets, camera identity, recording dates, source URLs, rights notes, and whether viewpoints are genuinely independent. Mark uncertainty explicitly.

**07 — Playable media:** Acquire small sample clips or usable stable playback links; inspect with ffprobe/OpenCV; record checksums where local and source-to-clip offset mapping if transformed.

**08 — Evidence manifest:** Export schema-valid incident/video/camera/evidence records with source-backed IDs, nulls for unknowns, bounded video offsets, and 2–4 checked evidence intervals.

**09 — Frame tools:** Minimal CLI for frame extraction by video-relative seconds. Test valid requests and out-of-bounds errors. Optional change score, no unsupported physical claims.

**10 — Geometry readiness:** GeoJSON only for verified coordinates; heading/FOV null if not known. State whether cross-camera localization is supported, and why.

## Working agreement

- A owns `frontend/` and `backend/platform/`; B owns `backend/intelligence/` and `data/`.
- A uses fixtures; B produces real schema-compatible data. No waiting for the other track.
- Shared contract changes require both developers' approval and a documented schema revision.
- Integrate when both tracks pass their gates, not at a predefined time.
- When blocked, record exact blocker and use the documented fallback. Do not invent data to unblock a demo.
- Completion report per ticket: changed files, run command, test evidence, open blockers, and next ready ticket.
