# Product decisions and scientific honesty

## Thesis
A map plus ordinary fire detection is replaceable by a static dashboard. FireFront is distinct because an autonomous agent asks which video can answer an unresolved question, searches it, inspects the correct time window, updates competing hypotheses and shows traceable evidence on real terrain.

## Demo success criteria
- User question triggers >=2 meaningful evidence-related actions and at least one adaptive choice.
- Two independently indexed evidence items are clickable and resolve to their correct source and time.
- 3D map shows real camera positions where verified; map does not mislabel arbitrary imagery as a geographically registered camera.
- A claim states whether it is observed, inferred, or unresolved.
- If triangulation cannot be calibrated, display bearing wedges or camera markers only; do not show a false point.

## Modes
**Gold:** same incident, two documented camera locations, orientation/FOV, overlapping observation, bearing intersection with uncertainty.
**Silver:** same incident, two documented cameras, map camera markers, temporal cross-evidence but no calibrated intersection.
**Bronze:** one camera with multiple incident segments, honest 3D site map and time-indexed evidence; demonstrate adaptive retrieval across segments.

## Risks and mitigations
- Source video provenance uncertain → require incident/source metadata; use Silver/Bronze.
- Cesium imagery credentials fail → use Cesium OSM buildings/ellipsoid or terrain provider fallback; camera markers still function.
- Video indexing delayed → local manifest + deterministic retrieval over Cosmos descriptions, while preserving source timestamp links.
- Cosmos returns imprecise timestamps → use known segment time bounds and cite them; never present invented frame-precision.
- PTZ camera orientation changes → store orientation per clip/time; no fixed cones without calibration.
- Smoke plume is elevated → ray intersections may identify projected sightline, not ground ignition point.
- Different cameras not time-synced → explicitly annotate offsets and uncertainty.

## Attribution and rights
Check HPWREN reuse terms, archive attribution, and video access before redistributing. Keep original source URLs and credits in metadata. Google 3D Tiles is optional and may require billing, keys, and specific attribution; prefer Cesium terrain first.
