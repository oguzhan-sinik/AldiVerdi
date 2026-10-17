# FireFront 3D — Clean Start

**State:** contract-first starter repository; no frontend or backend application has been implemented.

## Start here
1. Read `PROJECT-AGREEMENT.md`, `docs/SETUP.md`, `docs/CONTRACTS.md`.
2. Run `python3 -m pip install -r scripts/requirements.txt`, `python3 scripts/validate_contracts.py`, and `python3 -m pytest tests/test_contracts.py`.
3. Confirm VAST workshop VM access, actual API contracts and external wildfire footage permission.
4. Run Developer A with `docs/DEVELOPER-A.md`; run Developer B with `docs/DEVELOPER-B.md` on separate branches/worktrees.
5. Both agents must approve the schemas before making incompatible changes.

The repository intentionally contains no `frontend/package.json`, no Next.js application, no FastAPI application, no real videos, no Cosmos integration, and no calibrated geometry. These are implementation work, not existing capabilities.

## Project structure
- `contracts/`: versioned schemas (authoritative)
- `fixtures/`: explicitly synthetic examples
- `scripts/`, `tests/`: executable contract checks
- `frontend/`, `backend/platform/`: Developer A implementation space
- `backend/intelligence/`, `data/`: Developer B implementation space
- `docs/`: full current documentation and two continuous developer specifications

No timed tickets, old runbooks, replacement guides, or inherited app code.
