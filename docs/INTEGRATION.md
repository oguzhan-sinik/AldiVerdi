# Integration and external service verification

## First verify, then connect
1. Developer B reads the organizer repo and installed `.cursor/skills/`; verifies actual VAST authentication, query, search result, segment retrieval, media and ingestion contracts; and owns the single typed provider consumed by A.
2. Inspect team config and confirm network reachability from the intended server environment.
3. Test pre-indexed search and playback with approved organizer video.
4. Verify whether **external wildfire footage** can be indexed in the team environment.
5. Verify Cosmos-generated descriptions and embeddings through the existing VSS pipeline/API. Do not deploy or call a separate Cosmos service for capabilities VSS already provides; distinguish indexed descriptions from fresh clip analysis.
6. Verify W&B inference and Weave separately.
7. Build typed adapters and test live responses.
8. Replace fixtures only after actual response validation.

## CoreWeave and VAST
Prefer provided CoreWeave-hosted inference and VAST services. Do not provision a new GPU VM or redeploy DataEngine without evidence it is required and authorized.

## Local media
Developer B delivers approved files, ledger, stable ID/time mappings and a private playback transport. Developer A's server uses that transport for a validated browser-facing media route with seeking/range support. Keep VSS credentials, JWTs and signed upstream URLs server-side; distinguish a source webpage from playable media and parent-relative citations from clip-local seeks.

## Handshake between A and B
- Both sign off on current schema and fixtures.
- B provides video IDs, provenance, timestamp basis, asset mappings and geometry readiness.
- A consumes through adapters, not direct filesystem assumptions.
- Run contract tests and a single evidence-seek smoke test before declaring integrated.
- Shared schema changes require both owners' agreement.

## External blockers
If VM access, endpoints, rights or credentials are absent, record exact BLOCKED state. Do not create fake successes. Use fixtures to continue independent development.

## Deployment
Use organizer's supported team deployment workflow if available; do not overwrite shared VSS services. Test browser → app server → VAST/Cosmos reachability after deployment.
