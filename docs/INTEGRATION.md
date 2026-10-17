# Integration and external service verification

## First verify, then connect
1. Read organizer repo and installed `.cursor/skills/`; verify actual VAST query, search result, segment retrieval and ingestion contracts.
2. Inspect team config and confirm network reachability from the intended server environment.
3. Test pre-indexed search and playback with approved organizer video.
4. Verify whether **external wildfire footage** can be indexed in the team environment.
5. Verify Cosmos Reason input/output schema and access; do not guess a URL suffix.
6. Verify W&B inference and Weave separately.
7. Build typed adapters and test live responses.
8. Replace fixtures only after actual response validation.

## CoreWeave and VAST
Prefer provided CoreWeave-hosted inference and VAST services. Do not provision a new GPU VM or redeploy DataEngine without evidence it is required and authorized.

## Local media
Developer B delivers approved files and ledger. Developer A's server resolves `video_id` to media URLs, validates IDs, supports seeking/range requests, and distinguishes source page URL from playable URL.

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
