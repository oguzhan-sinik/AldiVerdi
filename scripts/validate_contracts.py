#!/usr/bin/env python3
"""Validate schemas, fixtures, referential integrity and synthetic provenance."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def validate():
    schema = load("contracts/schema.json")
    investigation_schema = load("contracts/investigation.schema.json")
    for s in (schema, investigation_schema):
        Draft202012Validator.check_schema(s)
    incident = load("fixtures/incident.json")
    investigation = load("fixtures/investigation.json")
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(incident)
    Draft202012Validator(investigation_schema, format_checker=FormatChecker()).validate(investigation)
    assert investigation["incident_id"] == incident["incident_id"]
    assert investigation["data_mode"] == incident["data_mode"]
    def unique(values):
        assert len(values) == len(set(values)), "Duplicate IDs"
        return set(values)
    camera_ids = unique([x["camera_id"] for x in incident["cameras"]])
    video_ids = unique([x["video_id"] for x in incident["videos"]])
    evidence_ids = unique([x["evidence_id"] for x in incident["evidence"]])
    unique([x["action_id"] for x in investigation["actions"]])
    unique([x["claim_id"] for x in investigation["claims"]])
    for video in incident["videos"]:
        assert video["camera_id"] in camera_ids
        if video["playback_status"] == "unavailable":
            assert video["duration_s"] is None
    for ev in incident["evidence"]:
        assert ev["video_id"] in video_ids
        assert ev["start_s"] <= ev["end_s"]
        video = next(v for v in incident["videos"] if v["video_id"] == ev["video_id"])
        if video["duration_s"] is not None:
            assert ev["end_s"] <= video["duration_s"]
    for item in investigation["actions"] + investigation["claims"]:
        assert set(item["evidence_ids"]) <= evidence_ids
    if incident["data_mode"] == "synthetic_fixture":
        assert all(v["source_url"].startswith("fixture://") and v["playback_status"] == "unavailable" for v in incident["videos"])
        assert all(c["lat"] is None and c["lon"] is None and c["geometry_status"] == "unavailable" for c in incident["cameras"])
        assert all(ev["status"] == "unresolved" for ev in incident["evidence"])
        assert all(a["status"] == "mock" for a in investigation["actions"])
    return incident, investigation

if __name__ == "__main__":
    validate()
    print("PASS: schema, cross-references and synthetic provenance")
