# Spatial science and map truthfulness

## Camera data
Use verified WGS84 lat/lon, optional altitude with stated vertical datum, verified heading, pitch, and FOV. Store unknown values as null. Validate lat [-90,90], lon [-180,180], units and source citations. Never geocode a camera from an ambiguous name and present it as verified.

## Cesium
Render actual geographic terrain. Camera markers only for known coordinates. Viewing cones only with enough calibration; visually label approximate geometry. Handle terrain provider failures explicitly.

## Image-to-bearing
A pixel observation does not determine a world coordinate without intrinsic/extrinsic calibration. For approximate horizontal bearing, document lens model, field of view, crop and heading assumptions. Smoke plumes may be elevated and move; they are not reliable ground intersections.

## Triangulation gate
Requires at least two independent calibrated camera observations of the **same event** with compatible recording-time mapping. Reject near-parallel rays, incompatible timestamps, uncertain camera heading, and invalid intersections. Report residual/error and uncertainty. If inputs are insufficient, return `insufficient_metadata` or the contract's equivalent; no precise point.

## Testing
Synthetic known-camera geometries should recover expected bearings/intersections within declared tolerance. Test deg/rad errors, lat/lon swaps, nearly parallel rays, missing coordinates, altitude, and mismatched observations. Passing synthetic tests does not validate real-world accuracy.

## GeoJSON
`data/geometry.geojson` contains only source-backed camera positions or explicitly qualified candidate geometry. Keep a separate `data/geometry-status.md` describing what is and is not justified.
