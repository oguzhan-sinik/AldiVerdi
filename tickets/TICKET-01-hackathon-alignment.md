# 01 — Align FireFront with the VAST Builders Challenge rules

**Owner:** Developer A + Developer B (joint sign-off on the decisions below)
**Priority:** P0 — every later ticket depends on these decisions
**Rules source:** `vast-builders-challenge/README.md`, `ARCHITECTURE_REFERENCE.md`, `.cursor/rules/build-day.mdc`, `.cursor/skills/`
**External deadline:** organizer submission window (README §6, "around 4:30pm" event time). Not a project milestone; it is the hard stop.

## Goal
Keep the FireFront idea (evidence-grounded wildfire video investigator) but build it the way the hackathon requires: on the pre-running VSS stack, through its APIs, deployed as a web app on the team cluster at `/app`.

## Verified facts (team-31 VM, 2026-10-17)
| Fact | Evidence |
|---|---|
| VSS API reachable; login as `team-31` works | `POST /api/v1/auth/login`, `GET /auth/me` |
| Index: 612 videos / 3,537 segments, **no wildfire footage** | `GET /dashboard/stats` |
| Upload: `POST /api/v1/videos/upload`, max 100 MB, one file per request, `custom_prompt` ≤ 800 chars | `GET /api/v1/config`, `/metadata/ingest-config` |
| Two test uploads (`20261017_105838_ca2d70ef`, `20261017_110131_217ea46c`) were segmented (13 × 5 s) and detected, but **never indexed** | `tools/segments` total = 0 |
| **Root cause:** clips are ~0.5 fps; Cosmos Reason samples at 4 fps and rejects them (`Target fps (4.0) must be <= original fps (0.5)`) | reasoner pod logs |
| YOLO (COCO classes) finds **0 objects** in wildfire clips — no `smoke`/`fire` class | detection sidecars |
| First upload's custom prompt hit the 800-char cap and was cut mid-word | S3 object metadata |
| Direct S3 read works with team creds; `vastdb` SDK not installed; GPU model URLs not in team config | boto3 listing, `/config/team-31.config` |
| `kubectl` works in namespace `team-31`; `ffmpeg`/`ffprobe` installed; **no Node.js** on VM | VM checks |

## Hackathon rules that change our plan
1. **Deliverable = web app on K8s at `/app`** via `deploy-app-no-registry`: `python:3.12-slim` image, code mounted from a ConfigMap (≤ ~1 MiB), creds from a Secret. No Docker build, no local server as the deliverable.
2. **Use the provided stack only.** Don't edit or redeploy DataEngine functions; stay in `team-31`; use skills before raw REST.
3. **LLM logic for our agent runs on W&B serverless inference** (`WANDB_*` already in env). VSS search/QA comes from the VSS API.
4. **Secrets:** never print, log, commit, or send to the browser. List env names only.
5. **External footage:** README says "Don't ingest videos from the internet." The team has decided to upload wildfire footage anyway → we must record rights per clip and get organizer confirmation on Cosmos (risk: judged as a rules breach).

## Decisions requiring A+B sign-off
| # | Decision | Replaces |
|---|---|---|
| D1 | **Frontend:** single static HTML/JS page served by the Python app; CesiumJS from a CDN. No Next.js. | `PROJECT-AGREEMENT.md` "Next.js 15" — cannot be built (no Node) or shipped (ConfigMap size, Python image) |
| D2 | **Backend:** one small Python app (`app/main.py`, FastAPI or stdlib) — serves the page, proxies VSS (login, search, segments, synthesize, stream with Range), runs the agent loop. | `backend/platform/` Next.js API routes |
| D3 | **Video store = VSS.** Footage goes in via `/videos/upload`; playback via our proxy of `/videos/stream` (JWT stays server-side). Local `data/processed/` is only the pre-upload staging area. | Local media resolver as primary playback |
| D4 | **Contract change (smallest):** add optional `vss_original_video` (S3 URI) to `video`; use existing `evidence.segment_id` for the VSS segment `source`. | — (needs CONTRACTS.md change protocol) |
| D5 | **Wildfire signal comes from Cosmos Reason text + Cosmos Embed vectors, not YOLO.** Optional OpenCV change score stays a Developer B tool. | Any plan relying on detections for smoke |
| D6 | **Scope cut:** triangulation and viewing cones are stretch; ship camera markers only for verified HPWREN site coordinates. | Geometry as core |

## Work breakdown

### B1 — Make uploads index (unblocks everything)
- Normalize each clip with ffmpeg to constant ≥ 8 fps H.264 (`-vf fps=8`), ≤ 100 MB. Record the time-lapse mapping (playback s → recording time) in `data/processed/asset-ledger.csv` — the frame-rate change alters playback timing, not recording time.
- Write one wildfire `custom_prompt` that fits in 800 chars (save it in `data/sources/ingest-prompt.txt`).
- Upload one clip with `camera_id=<hpwren site>`, `location=holy_fire_2018`, `capture_type=general`, `tags=wildfire`.
- **Acceptance:** `GET /tools/segments?original_video=…` returns > 0 rows; `POST /search {"query":"smoke plume"}` returns that clip.
- Delete or ignore the two broken test uploads (do not re-ingest them as-is).

### B2 — Source-backed footage
- HPWREN Holy Fire: ≥ 2 independent cameras, rights note, camera site lat/lon from HPWREN pages only. Ledger + `manifest-notes.md`.
- Upload sequentially after B1 passes. **Acceptance:** all clips indexed; contract-valid `data/incident.json` (`data_mode: source_backed`).

### A1 — App skeleton deployed
- `app/main.py` + `app/static/index.html`; health route; VSS login from Secret env.
- Deploy with `deploy-app-no-registry` (Deployment + Service + Ingress `/app`, host `video-lab-team-31.cosmos.vastdata.com`).
- **Acceptance:** pod Running; `/app` loads via workshop **App** button; page shows fixture incident labelled synthetic.

### A2 — Evidence playback
- Proxy `/videos/stream` with Range; list segments for a video; click evidence → seek to `start_s`.
- **Acceptance:** a real indexed segment plays and seeks; missing video shows "Video unavailable".

### A3 — Investigation agent
- Bounded loop (≤ 8 actions, no repeated identical calls) on W&B inference. Tools map to VSS: `search_evidence` → `POST /search`; `inspect_clip` → `GET /tools/segment` (+ `/videos/synthesize` for whole video); `compare_observations` → LLM over two segments' reasoning; `measure_frames` / `evaluate_geometry` → B's tools when ready, else explicit `unavailable`.
- Output validates against `investigation.schema.json`; claims cite `segment_id` + offsets.
- Optional: W&B Weave trace.
- **Acceptance:** "Where did smoke first appear, and does another camera corroborate it?" returns a valid investigation with clickable citations.

### A4 — Map (stretch)
- Cesium from CDN, terrain if a token is configured, else honest fallback. Markers only for verified coordinates.

## Constraints / do not build
- No Next.js, no Docker images, no edits to VSS/DataEngine deployments, no direct Cosmos calls from the browser.
- No fabricated coordinates, bearings, timestamps, or "live" labels on fixture data.
- No secrets in repo, ConfigMap, page source, or logs.

## Open questions
1. Organizer OK for external wildfire footage? (post on Cosmos; record answer here)
2. Does the pod have outbound internet for `pip install` and the Cesium CDN? Check in A1.
3. W&B inference model choice — pick from what `WANDB_API_KEY` can list.

## Definition of done
Deployed `/app` → open Holy Fire incident → play an indexed wildfire segment at the right offset → ask a question → bounded agent trace with cited, contract-valid claims. Everything not live is visibly labelled.
