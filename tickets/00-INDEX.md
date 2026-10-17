# FireFront 3D — First two hours (Tickets 01–10)

These tickets extend the existing FireFront 3D preparation ZIP. Copy the Markdown files into your existing `tickets/` folder. Times are elapsed from hackathon start, not clock times. **Developer A owns platform and agent; Developer B owns video/data/OpenCV/geometry.**

## Parallel schedule

| Window | Developer A | Developer B |
|---|---|---|
| 00:00–00:20 | 01 Contract freeze | 06 Source verification (brief joint contract review) |
| 00:20–00:45 | 02 Platform shell | 06 then 07 Clips |
| 00:45–01:00 | 03 Cesium terrain | 07 Clips |
| 01:00–01:20 | 03 Cesium terrain | 08 Evidence manifest |
| 01:20–01:25 | 04 Viewer | 08 Evidence manifest |
| 01:25–01:50 | 04 Viewer | 09 OpenCV frame tools |
| 01:50–02:00 | 05 Mock investigation | 10 Camera GeoJSON |

## Integration policy
- First 20 minutes: jointly approve the schema, then **no shared-file edits** until T+02:30.
- A never depends on B's files in this window: use fixtures.
- B never depends on A's frontend: validate JSON and media independently.
- At T+02:00, both have independently demonstrable deliverables. T+02:30 is the planned swap from fixtures to real data.
- If a ticket runs over by 10 minutes, cut optional work, not the acceptance criteria of P0 tickets.
- No automatic triangulation without verified camera position, bearing, and cross-view event correspondence.

## Definition of done at T+02:00
A: terrain + camera selection + evidence playback + labelled mock investigation.  
B: two source-backed clips + validated manifest + minimal frame tools + honest camera GeoJSON.
