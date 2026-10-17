# Product experience and visual design

## Layout
Three-panel incident workspace: left cameras/sources, center Cesium terrain and map controls, right video/evidence and investigation rail. Implement the Next.js 15 shell from scratch; no previous application code is included.

## Interactions
- Incident page loads a validated incident or clear unknown-ID error.
- Select camera → map focuses when coordinates exist; evidence list filters appropriately.
- Select evidence → correct video loads and seeks to `start_s`; cite provenance.
- Ask question → display agent actions and findings; allow clicking cited evidence.
- Switch fixture/live modes explicitly; never visually imply mock evidence is live.

## Empty/error states
Unknown camera position: 'Location unavailable', no marker. Missing media: 'Video unavailable', not a broken fake player. Missing Cesium token: honest map fallback. No search results: report no evidence found, not an invented conclusion. Model unavailable: label analysis unavailable.

## Design priorities
Readable, compelling geographic visualization, low-latency interactions, minimal dependencies. Do not prioritize particles, fire animations or photorealistic tiles over functioning evidence search and playback.

## Accessibility
Keyboard-accessible controls, meaningful labels, sufficient contrast, clear focus states and reduced-motion-friendly navigation.
