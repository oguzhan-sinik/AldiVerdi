# Current State — Clean Start

This repository was deliberately reset. **No Developer A Ticket 02 code is included**; no Next.js, Cesium, FastAPI, OpenCV or agent implementation exists. The prior implementation was deleted by the user. This package provides only canonical documentation, schemas, synthetic fixtures and runnable contract tests. The prior agent audit's modified schemas are not available as source files; these are a newly authored v1 contract baseline and must be jointly reviewed before being frozen.

## Present
- Project agreement and full setup/architecture/science/integration documentation.
- Two continuous developer instructions.
- New strict incident and investigation JSON Schemas.
- Synthetic two-camera, two-video, two-evidence fixtures with unavailable media and null geometry.
- Executable contract validator and pytest suite.

## Missing by design
- `frontend/package.json` and all frontend app code.
- Platform and intelligence implementation.
- Real wildfire media and validated source metadata.
- Live VAST/Cosmos/CoreWeave/W&B/Cesium connections.

## First actions
1. Run contract tests; A and B sign off on this **new** v1 baseline.
2. Verify workshop VM/config, model endpoint accessibility and external footage policy.
3. A starts **Next.js shell from zero**, then Cesium and evidence viewer.
4. B starts HPWREN source verification, then authorized media preparation.
