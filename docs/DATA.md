# Data sourcing, permissions and video processing

## Source candidates
Primary candidate: 2018 Holy Fire HPWREN archive: https://www.hpwren.ucsd.edu/news/20180812/ and https://www.hpwren.ucsd.edu/FIgLib/. Backup: documented 2025 Palisades/ALERTCalifornia recordings. Do not assume either source supplies downloadable video, two calibrated independent cameras, or redistribution rights.

## Source verification gate
For each candidate video, record: original landing page, actual media URL if present, incident/date, camera identity, independent viewpoint, source owner, rights note, recording timestamp basis, known position, known heading/FOV, known missing information and whether asset can be used in the hackathon. Document evidence supporting each claim.

**Do not download or ingest external footage before approval and a rights check.** The organizer's provided indexed corpus has separate licensing conditions; confirm external ingestion is allowed.

## Acquisition and processing
- Save original authorized bytes under `data/raw/`; never overwrite originals.
- Record SHA256, size, ffprobe metadata, source URL, acquisition note and transformations.
- Produce minimal H.264 MP4 derivatives under `data/processed/<video_id>.mp4` when authorized.
- Keep original/derived file mapping in `asset-ledger.csv`.
- Treat time-lapse time mapping explicitly; distinguish frame time from wall-clock time.
- Validate a real playable clip rather than a news article URL.

## Evidence production
Evidence requires an actual existing video reference and verified interval. Human-reviewed observation may be labelled as such; Cosmos output must be labelled model-derived; OpenCV output must be labelled measured. A model's interpretation is not ground truth.

## Fallback
If custom wildfire ingestion is not permitted, use only authorized footage in a separate local analysis path and label VAST functionality separately. Do not claim wildfire clips were semantically indexed by VAST when they were not.
