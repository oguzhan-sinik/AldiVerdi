# Setup and event credentials

## Prerequisites
Node 20+, Python 3.11+, FFmpeg, npm/pnpm, Cesium Ion access or alternative terrain provider, VAST/CoreWeave/W&B event credentials.

## Frontend
`cd frontend && npm install && npm run dev` once scaffolded at event. Use client-only Cesium dynamic import and set asset base path for Cesium workers.

## Backend
`python -m venv .venv && source .venv/bin/activate && pip install fastapi uvicorn opencv-python-headless numpy pydantic httpx` once scaffolded. Add geospatial library only if required.

## Secrets
Never commit keys. `.env.example` lists names only. Verify endpoint model names and multimodal request formats against team-provided config; do not assume standard OpenAI chat payload accepts video.

## Video prep
Keep raw source files and a manifest of URLs, capture time, camera IDs and license. Encode web-friendly preview clips and preserve mapping from preview time to source time.

## Operational check
- Map loads, sources credited.
- Camera marker opens actual video.
- Evidence time jumps to correct offset.
- Agent tool call trace has valid evidence IDs.
- Camera geometry cannot render if unverified.
- Offline fallback runs from cached JSON and local video files.
