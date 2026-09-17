"""Regression coverage for Android's locationHint install gate.

Verified against nearby-guide-android-source-v0.8.0-2026-07-27.zip,
app/src/main/java/com/example/nearbyguide/guidepack/GuidePackFormat.kt:161-167:
null location + kind.lowercase() in zone/artwork/exhibit/view requires a
nonblank locationHint. The predicate does not consult the indoor flag.
"""

from __future__ import annotations

import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path
from unittest.mock import Mock

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_packs
import inspect_pack
import validate
import verify_release
from android_contract import point_errors


REQUIRED_KINDS = ("zone", "artwork", "exhibit", "view")
KIND_CASES = tuple(
    spelling
    for kind in REQUIRED_KINDS
    for spelling in (kind, kind.upper(), kind.title())
)
MISSING = object()
INVALID_HINTS = (
    pytest.param(MISSING, id="missing"),
    pytest.param(None, id="null"),
    pytest.param("", id="empty"),
    pytest.param(" \t\r\n\u3000", id="whitespace"),
)
MEANINGFUL_HINT = "  依現場指示牌尋找展示區；此項目沒有 GPS 導航點。  "
REGIONS = ("tw/hsinchu", "jp/miyako-jima", "jp/ishigaki", "tw/xiaoliuqiu")
SOURCE_FIXTURE = (
    ROOT / "tests/fixtures/valid/tw-hsinchu-test/points/tw-hsinchu-test-point-a.yaml"
)


def _set_hint(point: dict, hint: object) -> None:
    if hint is MISSING:
        point.pop("locationHint", None)
    else:
        point["locationHint"] = hint


def _point(kind: str = "view", hint: object = MEANINGFUL_HINT) -> dict:
    point = {
        "id": "test-android-location-hint",
        "parentId": None,
        "kind": kind,
        "title": "Synthetic location-hint fixture",
        "summary": "A text-only fixture, not a real attraction.",
        "narration": "Use the synthetic exhibition label to identify this fixture.",
        "nearbyGuideRating": 3.0,
        "countryCode": "TW",
        "adminAreaLevel1": "Test region",
        "hierarchy": ["Test region"],
        "tagGroups": [],
        "indoor": False,
        "location": None,
        "trigger": None,
        "media": [],
        "extensions": {},
    }
    _set_hint(point, hint)
    return point


def _source(kind: str, hint: object) -> dict:
    source = yaml.safe_load(SOURCE_FIXTURE.read_text(encoding="utf-8-sig"))
    source["point"].update(
        kind=kind, indoor=False, location=None, trigger=None, googleMapsUrl=None
    )
    _set_hint(source["point"], hint)
    return source


@pytest.mark.parametrize("kind", KIND_CASES)
@pytest.mark.parametrize("hint", INVALID_HINTS)
@pytest.mark.parametrize("location_missing", (False, True), ids=("null-gps", "missing-gps"))
def test_no_gps_requires_nonblank_hint_even_when_outdoor(kind, hint, location_missing):
    point = _point(kind, hint)
    if location_missing:
        point.pop("location")
    errors = point_errors(point)
    assert isinstance(errors, list)
    assert errors, point
    assert all(isinstance(error, str) for error in errors)
    assert any("locationHint" in error for error in errors), errors


@pytest.mark.parametrize("kind", KIND_CASES)
@pytest.mark.parametrize("indoor", (True, MISSING), ids=("indoor", "no-indoor-field"))
def test_hint_requirement_does_not_depend_on_indoor_field(kind, indoor):
    point = _point(kind, None)
    if indoor is MISSING:
        point.pop("indoor")
    else:
        point["indoor"] = indoor
    assert any("locationHint" in error for error in point_errors(point))


@pytest.mark.parametrize("kind", KIND_CASES)
def test_no_gps_accepts_meaningful_hint(kind):
    assert point_errors(_point(kind)) == []


@pytest.mark.parametrize("kind", ("view", "VIEW", "ViEw"))
@pytest.mark.parametrize("hint", INVALID_HINTS)
def test_android_helper_allows_gps_view_without_hint(kind, hint):
    # Coordinate-review policy is deliberately stricter than Android's parser.
    point = _point(kind, hint)
    point["location"] = {"latitude": 24.0, "longitude": 121.0}
    point["trigger"] = {
        "radiusMeters": 75.0, "dwellMillis": 2000, "rearmDistanceMeters": 1000.0
    }
    assert point_errors(point) == []


@pytest.mark.parametrize("kind", ("attraction", "ATTRACTION", "AtTrAcTiOn"))
@pytest.mark.parametrize("hint", INVALID_HINTS)
def test_android_helper_allows_no_gps_attraction_without_hint(kind, hint):
    assert point_errors(_point(kind, hint)) == []


@pytest.mark.parametrize("kind", REQUIRED_KINDS)
@pytest.mark.parametrize("hint", INVALID_HINTS)
def test_source_validation_rejects_outdoor_no_gps_without_hint(
    kind, hint, tmp_path, monkeypatch
):
    # Keep schemas/taxonomy real, but place synthetic YAML outside production.
    monkeypatch.setattr(validate, "REPO_ROOT", tmp_path)
    point_path = tmp_path / "point.yaml"
    taxonomy = validate._load_taxonomy_tags()
    source = _source(kind, MEANINGFUL_HINT)
    point_path.write_text(yaml.safe_dump(source, allow_unicode=True), encoding="utf-8")
    valid_result = validate._validate_point_yaml(point_path, taxonomy)
    assert valid_result.ok, [error.message for error in valid_result.errors]

    _set_hint(source["point"], hint)
    point_path.write_text(yaml.safe_dump(source, allow_unicode=True), encoding="utf-8")
    result = validate._validate_point_yaml(point_path, taxonomy)
    assert not result.ok
    assert all("locationHint" in error.message for error in result.errors)
    if hint is not MISSING:
        # Null/blank hints are schema-valid: the semantic gate must catch them.
        assert all("Schema error" not in error.message for error in result.errors)


@pytest.mark.parametrize("kind", REQUIRED_KINDS)
@pytest.mark.parametrize("hint", INVALID_HINTS)
@pytest.mark.parametrize("variant", ("compact", "complete"))
def test_builder_rejects_invalid_hint_before_media(kind, hint, variant, tmp_path, monkeypatch):
    source = _source(kind, hint)
    source["media"] = [{"id": "must-not-be-processed", "type": "image"}]
    media_builder = Mock(side_effect=AssertionError("Media processed before the hint gate"))
    monkeypatch.setattr(build_packs, "_build_media_record", media_builder)

    with pytest.raises(ValueError, match="locationHint"):
        build_packs._build_point_record(source, variant, tmp_path)
    media_builder.assert_not_called()


@pytest.mark.parametrize("kind", REQUIRED_KINDS)
@pytest.mark.parametrize("variant", ("compact", "complete"))
def test_builder_preserves_meaningful_hint_without_gps(kind, variant, tmp_path):
    record = build_packs._build_point_record(_source(kind, MEANINGFUL_HINT), variant, tmp_path)
    assert record["locationHint"] == MEANINGFUL_HINT
    assert record.get("location") is None
    assert record.get("trigger") is None
    assert point_errors(record) == []


def _write_archive(path: Path, point: dict) -> None:
    points_bytes = json.dumps({
        "format": "nearby-guide-points",
        "schemaVersion": 1,
        "points": [point],
        "extensions": {},
    }, ensure_ascii=False).encode("utf-8")
    manifest = {
        "format": "nearby-guide-pack",
        "schemaVersion": 1,
        "packId": "test-android-location-hint",
        "packVersion": "1.0.0",
        "variantId": "compact",
        "mediaMode": "compact",
        "title": "Synthetic hint regression pack",
        "subtitle": "No media or real-world coordinates",
        "createdAt": "2026-07-27T00:00:00Z",
        "contentLanguage": "zh-Hant-TW",
        "region": {"countryCode": "TW", "countryName": "台灣", "adminAreaLevel1": "Test region"},
        "minAppVersionCode": 8,
        "pointsFile": "points.json",
        "guidePointCount": 1,
        "files": [{
            "path": "points.json",
            "bytes": len(points_bytes),
            "sha256": hashlib.sha256(points_bytes).hexdigest(),
        }],
        "extensions": {},
    }
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False).encode("utf-8"))
        archive.writestr("points.json", points_bytes)


@pytest.mark.parametrize("kind", ("ZoNe", "ArTwOrK", "ExHiBiT", "ViEw"))
@pytest.mark.parametrize("hint", INVALID_HINTS)
def test_inspector_rejects_missing_hint_despite_correct_archive_hashes(kind, hint, tmp_path, capsys):
    point = _point(kind, hint)
    point.pop("indoor")  # Runtime records need not carry this source-only field.
    invalid_path = tmp_path / "invalid-hint.guidepack"
    _write_archive(invalid_path, point)
    with zipfile.ZipFile(invalid_path) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == {"manifest.json", "points.json"}
        manifest = json.loads(archive.read("manifest.json"))
        points_bytes = archive.read("points.json")
        assert manifest["files"] == [{
            "path": "points.json", "bytes": len(points_bytes),
            "sha256": hashlib.sha256(points_bytes).hexdigest(),
        }]

    assert inspect_pack.inspect(invalid_path) is False
    errors = capsys.readouterr().err
    assert "locationHint" in errors
    assert point["id"] in errors
    assert "mismatch" not in errors.lower()

    # Changing only the hint (and recomputing the hash) must make this ZIP valid.
    point["locationHint"] = MEANINGFUL_HINT
    valid_path = tmp_path / "valid-hint.guidepack"
    _write_archive(valid_path, point)
    assert inspect_pack.inspect(valid_path) is True


@pytest.mark.parametrize("hint", INVALID_HINTS)
def test_release_verification_rejects_hint_despite_matching_catalog_hash(hint, tmp_path, monkeypatch):
    point = _point("ViEw", hint)
    point.pop("indoor")
    point["extensions"]["nearbyGuide.locationReview"] = {
        "status": "unresolved",
        "anchorType": "none",
        "reason": "Synthetic text-only fixture; no verified navigation point.",
        "checkedAt": "2026-07-27",
        "sources": [],
    }
    archive_path = tmp_path / "release-hint.guidepack"
    _write_archive(archive_path, point)
    payload = archive_path.read_bytes()
    url = "https://example.invalid/releases/download/data-test-v1.0.0/release-hint.guidepack"
    variant = {
        "variantId": "compact",
        "downloadUrl": url,
        "downloadBytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }
    catalog = {"packs": [{
        "packId": "test-android-location-hint",
        "version": "1.0.0",
        "guidePointCount": 1,
        "variants": [variant],
    }]}
    catalog_path = tmp_path / "catalog.json"
    catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
    download = Mock(return_value=io.BytesIO(payload))
    monkeypatch.setattr(verify_release.urllib.request, "urlopen", download)

    with pytest.raises(AssertionError, match="locationHint") as rejected:
        verify_release.verify(catalog_path)
    assert point["id"] in str(rejected.value)
    download.assert_called_once_with(url, timeout=120)

    # The independent coordinate gate and transport must accept the repaired ZIP.
    point["locationHint"] = MEANINGFUL_HINT
    _write_archive(archive_path, point)
    payload = archive_path.read_bytes()
    variant.update(downloadBytes=len(payload), sha256=hashlib.sha256(payload).hexdigest())
    catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
    download.reset_mock()
    download.return_value = io.BytesIO(payload)
    verify_release.verify(catalog_path)
    download.assert_called_once_with(url, timeout=120)


@pytest.mark.parametrize("region", REGIONS)
@pytest.mark.parametrize("variant", ("compact", "complete"))
def test_current_built_packs_satisfy_android_location_hint_rule(region, variant):
    pack_path = ROOT / "regions" / region / "pack.yaml"
    assert pack_path.is_file(), f"Missing current pack source: {pack_path}"
    pack = yaml.safe_load(pack_path.read_text(encoding="utf-8-sig"))
    archive_path = ROOT / "dist/packs" / f"{pack['packId']}-{pack['version']}-{variant}.guidepack"
    assert archive_path.is_file(), f"Build the current source version first: {archive_path}"
    with zipfile.ZipFile(archive_path) as archive:
        manifest = json.loads(archive.read("manifest.json"))
        points = json.loads(archive.read("points.json"))["points"]

    assert manifest["packId"] == pack["packId"]
    assert manifest["packVersion"] == pack["version"]
    assert manifest["variantId"] == variant
    assert manifest["guidePointCount"] == len(points) > 0
    if region == "jp/miyako-jima":
        by_id = {point["id"]: point for point in points}
        for point_id in ("jp-miyakojima-biyandam-viewpoint", "jp-miyakojima-ikema-dugong"):
            # Repair the hint, not the absence of an evidence-backed GPS point.
            point = by_id[point_id]
            assert point["kind"].lower() == "view"
            assert point.get("location") is None, point_id
            assert point.get("trigger") is None, point_id
            assert point.get("googleMapsUrl") is None, point_id
    for point in points:
        context = f"{archive_path.name}: {point['id']}"
        # Keep an independent assertion, so a regressed helper cannot bless a ZIP.
        if point.get("location") is None and point["kind"].lower() in REQUIRED_KINDS:
            hint = point.get("locationHint")
            assert isinstance(hint, str) and hint.strip(), f"{context}: missing nonblank locationHint"
        assert point_errors(point) == [], context
