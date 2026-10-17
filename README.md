# FireFront 3D — Clean Start

**State:** contract-first starter repository; no frontend or backend application has been implemented.

## Start here
1. Read `PROJECT-AGREEMENT.md`, `docs/SETUP.md`, `docs/CONTRACTS.md`.
2. Run `python3 -m pip install -r scripts/requirements.txt`, `python3 scripts/validate_contracts.py`, and `python3 -m pytest tests/test_contracts.py`.
3. Confirm VAST workshop VM access, actual API contracts and external wildfire footage permission.
4. Follow exactly two active tickets: [Developer A — agent and frontend](tickets/DEVELOPER-A-platform-agent-frontend.md) and [Developer B — VAST access and evidence](tickets/DEVELOPER-B-vast-data-evidence.md). A develops UI and agent together; B delivers the typed VAST provider and real data. Use existing checkouts; create separate branches/checkouts only when explicitly requested.
5. Both agents must approve the schemas before making incompatible changes.

The repository intentionally contains no `frontend/package.json`, no Next.js application, no FastAPI application, no real videos, no Cosmos integration, and no calibrated geometry. These are implementation work, not existing capabilities.

## Project structure
- `contracts/`: versioned schemas (authoritative)
- `fixtures/`: explicitly synthetic examples
- `scripts/`, `tests/`: executable contract checks
- `frontend/`, `backend/platform/`: Developer A's frontend, orchestration and application delivery
- `backend/intelligence/`, `data/`: Developer B's VAST adapter, evidence, media and spatial tools
- `docs/`: supporting documentation and links to the two developer tickets
- `HACKATHON.md`, `ARCHITECTURE_REFERENCE.md`, `BEFORE_YOU_BUILD.md`, `config.example`, `.cursor/`, `docs/images/`, `docs/hackathon/`, `docs/*.pdf`: merged from the VAST Builders Challenge repo (rules, VSS API skills)
- `tickets/`: exactly two active implementation tickets, one per developer

The complete-demo target is Next.js/React/Cesium, real geographic terrain and at least two independent verified Holy Fire camera views. Localization requires adequate calibration; fixtures do not satisfy live-demo acceptance. External-footage permission and supported deployment feasibility remain implementation gates.
