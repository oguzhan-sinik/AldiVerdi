"""Contract and fixture integrity tests (no external services)."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_contracts import (  # noqa: E402
    validate_incident,
    validate_investigation,
)

FIXTURE_INCIDENT = ROOT / "fixtures" / "incident.json"
FIXTURE_INVESTIGATION = ROOT / "fixtures" / "investigation.json"


@pytest.fixture
def incident() -> dict:
    return json.loads(FIXTURE_INCIDENT.read_text(encoding="utf-8"))


@pytest.fixture
def investigation() -> dict:
    return json.loads(FIXTURE_INVESTIGATION.read_text(encoding="utf-8"))


def test_fixture_incident_valid(incident: dict) -> None:
    assert validate_incident(incident) == []


def test_fixture_investigation_valid(incident: dict, investigation: dict) -> None:
    assert validate_investigation(investigation, incident) == []


def test_synthetic_fixture_is_labelled(incident: dict, investigation: dict) -> None:
    assert incident["data_mode"] == "synthetic_fixture"
    assert investigation["execution_mode"] == "mock"
    assert all(c["lat"] is None and c["lon"] is None for c in incident["cameras"])
    assert all(not c["orientation_verified"] for c in incident["cameras"])


def test_rejects_interval_beyond_duration(incident: dict) -> None:
    bad = copy.deepcopy(incident)
    bad["evidence"][0]["end_s"] = bad["videos"][0]["duration_s"] + 1
    errors = validate_incident(bad)
    assert any("exceeds video duration_s" in e for e in errors)


def test_rejects_verified_geometry_without_coordinates(incident: dict) -> None:
    bad = copy.deepcopy(incident)
    bad["cameras"][0]["geometry_status"] = "verified"
    errors = validate_incident(bad)
    assert any("geometry_status=verified requires lat/lon" in e for e in errors)


def test_rejects_unknown_claim_evidence_id(incident: dict, investigation: dict) -> None:
    bad = copy.deepcopy(investigation)
    bad["claims"][0]["evidence_ids"] = ["ev-does-not-exist"]
    errors = validate_investigation(bad, incident)
    assert any("unknown evidence_id" in e for e in errors)


def test_source_backed_rejects_fixture_urls(incident: dict) -> None:
    bad = copy.deepcopy(incident)
    bad["data_mode"] = "source_backed"
    bad["videos"][0]["playback_status"] = "playable"
    bad["videos"][0]["source_url"] = "fixture://still-fake"
    bad["videos"][1]["playback_status"] = "playable"
    bad["videos"][1]["source_url"] = "https://example.com/real.mp4"
    errors = validate_incident(bad)
    assert any("cannot use fixture://" in e for e in errors)
