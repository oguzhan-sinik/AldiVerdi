# Environment and initial setup

## Prerequisites
- Existing FireFront repository, Git and Node.js compatible with its `frontend/package.json`.
- Python 3.12 or repository-supported Python, pip/venv.
- FFmpeg and ffprobe for Developer B's video work.
- Hackathon-assigned workshop VM, organizer repository, team configuration and approved service access.
- Cesium ion account/token if the chosen terrain provider requires it.
- W&B account/credentials only for the features actually used.

## Safety and preservation
1. Check `git status --short`, initialize Git if needed, and commit/snapshot this new contract baseline after joint review.
2. Use separate branches/worktrees for A and B where possible.
3. Keep `frontend/`, `backend/`, `contracts/`, `fixtures/`, `scripts/`, `tests/`, `.env.example` and `.gitignore` in place during development.
4. Do not paste credentials into chat, commit them, or expose private model URLs to the browser.

## Frontend implementation
No `frontend/package.json` exists yet. Developer A must create the Next.js 15 app before running `npm ci`, `npm run build`, `npm run lint` or `npm run dev`.

## Verify contracts
```bash
python3 -m pip install -r scripts/requirements.txt
python3 scripts/validate_contracts.py
python3 -m pytest tests/test_contracts.py
```
Use a venv as appropriate. If the repository uses different paths, inspect before running.

## Access the hackathon environment
Follow the organizer's current instructions for your assigned VM and team. Open the organizer repository on that VM; review `.cursor/skills/` and the team's config. Reference: https://github.com/vast-data/vast-builders-challenge and its `ARCHITECTURE_REFERENCE.md`. Do not assume endpoint names or request schemas from memory; inspect the actual installed skills and config.

Expected variable **names to check**, not guaranteed exhaustive:
- `COSMOS3_REASON_URL`
- `COSMOS_EMBED1_URL`
- `YOLO_URL`
- `WANDB_API_KEY`
- `INGRESS_URL`
- VAST-specific credentials/hostnames as documented for your team
- `NEXT_PUBLIC_CESIUM_ION_TOKEN` (browser-public Cesium token only)

Run this only after the organizer's documented config-loading procedure:
```bash
python3 - <<'PY'
import os
for key in ["COSMOS3_REASON_URL","COSMOS_EMBED1_URL","YOLO_URL","WANDB_API_KEY","INGRESS_URL"]:
    print(key, "SET" if os.getenv(key) else "MISSING")
PY
```
Do not print secret values. A config file's presence does not imply variables have been loaded or endpoints are reachable.

## Where secrets belong
- Frontend **server** environment: private VAST/Cosmos/W&B settings required by Next.js API routes.
- Browser environment: only explicitly public values, such as `NEXT_PUBLIC_CESIUM_ION_TOKEN`, with appropriate token restrictions.
- Developer B processing environment: private inference and storage settings; never embed in evidence JSON.
- VM: prefer the organizer's prescribed secrets/config mechanism.

## Connectivity gates
1. Open the provided VAST search interface; verify search, metadata and clip playback using an **existing approved** indexed video.
2. Verify the actual Cosmos reasoning interface and what it accepts (video URL, frames, file or segment reference).
3. Verify whether custom external wildfire footage is permitted **and** indexable.
4. Verify W&B inference and/or Weave independently; they are different capabilities.
5. Determine where FireFront's backend must run to reach private VAST endpoints.
6. If any gate fails, mark it BLOCKED and continue with clearly labelled fixtures.

## FFmpeg
On macOS, if absent and package installation is approved: `brew install ffmpeg`. On Linux use the VM's supported package manager, only with permission. Verify `ffmpeg -version` and `ffprobe -version`.

## Media conventions
- Original approved footage: `data/raw/`
- Normalized local playable files: `data/processed/<video_id>.mp4`
- Ledger: `data/processed/asset-ledger.csv`
- Evidence: `data/evidence.json`
- Source notes: `data/sources/manifest-notes.md`
- Geometry: `data/geometry.geojson` and `data/geometry-status.md`

Do not place large footage in Git. A local filesystem path is not a browser playback URL; resolve video IDs through a server-side media adapter with safe path validation and HTTP range support where needed.

## Required human decisions
- Approve specific media downloads after source, size and rights are known.
- Confirm with organizers whether external HPWREN footage may be uploaded/indexed.
- Provide or configure team VM access and Cesium token as applicable.
- Do not purchase/rent another GPU VM unless the provided CoreWeave-hosted endpoints cannot meet a verified need.
