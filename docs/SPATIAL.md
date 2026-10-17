# Spatial localization — Developer B

## Three levels of map accuracy
1. Verified camera point: documented lat/lon and altitude.
2. Calibrated viewing wedge: camera position + verified heading + horizontal FOV for a specific timestamp/clip.
3. Candidate source area: two compatible camera bearings, verified common target and synchronized observation; show error polygon, not a pin claiming ground truth.

## Geometry
For small local extents, convert WGS84 coordinates to a local ENU projection or use a geospatial library. Each image target horizontal offset from optical center maps approximately to bearing `heading + atan((u-cx)/fx)`, where `fx` is pixel focal length; valid only for a calibrated rectilinear camera with known distortion/crop. PTZ zoom/heading may vary. Intersect two bearing rays in the local tangent plane; reject near-parallel rays, rays behind cameras, and large residuals. Project to terrain only if elevation geometry is defensible.

## Honest smoke localization
Smoke is a volume and moves with wind. Bearings to plume pixels may not intersect at the ignition point. Prefer `candidate plume sightline intersection` with uncertainty, or `direction of observed smoke`, not `fire origin`.

## Camera metadata record
`camera_id`, `lat`, `lon`, `alt_m`, `heading_deg`, `pitch_deg`, `hfov_deg`, `orientation_verified`, `source_url`, `valid_from`, `valid_to`. Unknown fields remain null. Include per-segment PTZ calibration where needed.

## B output
Return GeoJSON `FeatureCollection` with point camera features, wedge/ray features when calibrated, and optional uncertainty polygon; include provenance IDs and geometry_status. A renders this without altering geometry.

## Validation
Synthetic geometry test with known intersecting bearings, near-parallel rejection, null metadata test, PTZ orientation-change test, and timeline mismatch test.
