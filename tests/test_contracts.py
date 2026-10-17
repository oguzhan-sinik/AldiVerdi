import copy
import sys
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator, ValidationError
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_contracts import load, validate

def test_contract_gate():
    validate()

def test_schema_itself_valid():
    Draft202012Validator.check_schema(load("contracts/schema.json"))
    Draft202012Validator.check_schema(load("contracts/investigation.schema.json"))

def test_rejects_extra_field():
    fixture = load("fixtures/incident.json")
    fixture["unexpected"] = True
    with pytest.raises(ValidationError):
        Draft202012Validator(load("contracts/schema.json")).validate(fixture)

def test_rejects_invalid_latitude():
    fixture = load("fixtures/incident.json")
    fixture["cameras"][0]["lat"] = 95
    with pytest.raises(ValidationError):
        Draft202012Validator(load("contracts/schema.json")).validate(fixture)

def test_rejects_unknown_tool():
    fixture = load("fixtures/investigation.json")
    fixture["actions"][0]["tool"] = "invented_tool"
    with pytest.raises(ValidationError):
        Draft202012Validator(load("contracts/investigation.schema.json")).validate(fixture)

def test_synthetic_fixture_has_no_claimed_coordinates():
    fixture, _ = validate()
    assert all(c["lat"] is None and c["lon"] is None for c in fixture["cameras"])

def test_synthetic_video_is_unplayable():
    fixture, _ = validate()
    assert all(v["playback_status"] == "unavailable" for v in fixture["videos"])

def test_evidence_references_resolve():
    fixture, inv = validate()
    ids = {e["evidence_id"] for e in fixture["evidence"]}
    assert all(set(x["evidence_ids"]) <= ids for x in inv["actions"] + inv["claims"])
