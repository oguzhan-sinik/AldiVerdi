#!/usr/bin/env python3
"""Validate FireFront fixtures against shared JSON Schema contracts.

Cross-checks ID references, video-relative intervals, and geometry honesty rules.
Does not call external services or invent missing media.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
INCIDENT_SCHEMA = ROOT / "contracts" / "schema.json"
INVESTIGATION_SCHEMA = ROOT / "contracts" / "investigation.schema.json"
DEFAULT_INCIDENT = ROOT / "fixtures" / "incident.json"
DEFAULT_INVESTIGATION = ROOT / "fixtures" / "investigation.json"


def _load(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _schema_errors(schema: dict, instance: dict) -> list[str]:
    validator = Draft202012Validator(schema)
    return [
        f"{'/'.join(str(p) for p in err.path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    ]


def validate_incident(incident: dict) -> list[str]:
    errors = _schema_errors(_load(INCIDENT_SCHEMA), incident)
    camera_ids = {c["camera_id"] for c in incident.get("cameras", [])}
    videos = {v["video_id"]: v for v in incident.get("videos", [])}

    for video in incident.get("videos", []):
        if video["camera_id"] not in camera_ids:
            errors.append(
                f"video {video['video_id']}: camera_id {video['camera_id']!r} not in cameras"
            )

    for evidence in incident.get("evidence", []):
        video = videos.get(evidence["video_id"])
        if video is None:
            errors.append(
                f"evidence {evidence['evidence_id']}: video_id {evidence['video_id']!r} missing"
            )
            continue
        if evidence["end_s"] < evidence["start_s"]:
            errors.append(
                f"evidence {evidence['evidence_id']}: end_s < start_s"
            )
        if evidence["end_s"] > video["duration_s"]:
            errors.append(
                f"evidence {evidence['evidence_id']}: end_s {evidence['end_s']} "
                f"exceeds video duration_s {video['duration_s']}"
            )

    for camera in incident.get("cameras", []):
        has_position = camera.get("lat") is not None and camera.get("lon") is not None
        geometry_status = camera.get("geometry_status", "unavailable")
        if not has_position and geometry_status == "verified":
            errors.append(
                f"camera {camera['camera_id']}: geometry_status=verified requires lat/lon"
            )
        if camera.get("orientation_verified") and (
            camera.get("heading_deg") is None or camera.get("hfov_deg") is None
        ):
            errors.append(
                f"camera {camera['camera_id']}: orientation_verified requires heading_deg and hfov_deg"
            )
        if camera.get("orientation_verified") and not has_position:
            errors.append(
                f"camera {camera['camera_id']}: orientation_verified requires lat/lon"
            )

    if incident.get("data_mode") == "source_backed":
        for video in incident.get("videos", []):
            if video.get("playback_status") == "unavailable":
                errors.append(
                    f"video {video['video_id']}: source_backed incidents cannot mark playback unavailable"
                )
            if str(video.get("source_url", "")).startswith("fixture://"):
                errors.append(
                    f"video {video['video_id']}: source_backed incidents cannot use fixture:// URLs"
                )

    return errors


def validate_investigation(investigation: dict, incident: dict | None = None) -> list[str]:
    errors = _schema_errors(_load(INVESTIGATION_SCHEMA), investigation)
    if incident is None:
        return errors

    if investigation.get("incident_id") != incident.get("incident_id"):
        errors.append(
            f"investigation incident_id {investigation.get('incident_id')!r} "
            f"!= incident {incident.get('incident_id')!r}"
        )

    known_evidence = {e["evidence_id"] for e in incident.get("evidence", [])}
    for action in investigation.get("actions", []):
        for evidence_id in action.get("evidence_ids") or []:
            if evidence_id not in known_evidence:
                errors.append(
                    f"action step {action.get('step')}: unknown evidence_id {evidence_id!r}"
                )
    for claim in investigation.get("claims", []):
        for evidence_id in claim.get("evidence_ids") or []:
            if evidence_id not in known_evidence:
                errors.append(
                    f"claim {claim.get('claim_id')}: unknown evidence_id {evidence_id!r}"
                )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--incident", type=Path, default=DEFAULT_INCIDENT)
    parser.add_argument("--investigation", type=Path, default=DEFAULT_INVESTIGATION)
    args = parser.parse_args(argv)

    incident = _load(args.incident)
    investigation = _load(args.investigation)

    incident_errors = validate_incident(incident)
    investigation_errors = validate_investigation(investigation, incident)
    all_errors = [
        *(f"incident: {e}" for e in incident_errors),
        *(f"investigation: {e}" for e in investigation_errors),
    ]

    if all_errors:
        print("Contract validation FAILED")
        for error in all_errors:
            print(f"  - {error}")
        return 1

    print("Contract validation PASS")
    print(f"  incident: {args.incident}")
    print(f"  investigation: {args.investigation}")
    print(f"  data_mode: {incident.get('data_mode')}")
    print(f"  execution_mode: {investigation.get('execution_mode')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
