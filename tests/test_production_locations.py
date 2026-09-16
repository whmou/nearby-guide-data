import json
import sys
import zipfile
from pathlib import Path
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from location_contract import location_errors
from build_packs import build_pack

PACKS = sorted((ROOT / "regions").glob("*/*/pack.yaml"))


def test_review_batch_covers_every_point_once():
    entries = []
    for report in sorted((ROOT / "audits/location-2026-09-16").glob("*.json")):
        entries.extend(json.loads(report.read_text(encoding="utf-8-sig")))
    reports = {entry["id"]: entry for entry in entries}
    assert len(reports) == len(entries), "Duplicate review ownership"
    sources = [yaml.safe_load(p.read_text(encoding="utf-8-sig")) for p in (ROOT / "regions").glob("*/*/points/*.yaml")]
    assert set(reports) == {s["point"]["id"] for s in sources}
    assert "tw-hsinchu-zhongzheng-park" not in reports
    for source in sources:
        entry = reports[source["point"]["id"]]
        review = source["locationReview"]
        assert (review["status"], review["anchorType"], review["sources"]) == (entry["status"], entry["anchorType"], entry["sources"])
        if entry["status"] == "verified":
            assert source["point"]["location"] == {"latitude": entry["latitude"], "longitude": entry["longitude"]}


def test_viewer_export_cannot_keep_old_pins_or_text():
    export = json.loads((ROOT / "public/viewer_data.json").read_text(encoding="utf-8"))
    points = {p["id"]: p for pack in export["packs"] for p in pack["points"]}
    sources = [yaml.safe_load(p.read_text(encoding="utf-8-sig")) for p in (ROOT / "regions").glob("*/*/points/*.yaml")]
    assert set(points) == {s["point"]["id"] for s in sources}
    for source in sources:
        p = source["point"]
        loc = p.get("location") or {}
        exported = points[p["id"]]
        assert (exported["lat"], exported["lng"]) == (loc.get("latitude"), loc.get("longitude"))
        assert exported["locationReview"] == source["locationReview"]
        for field in ("googleMapsUrl", "locationHint", "title", "summary", "narration", "observationPrompt"):
            assert exported[field] == p.get(field), (p["id"], field)


@pytest.mark.parametrize("path", PACKS, ids=lambda p: p.parent.name)
def test_all_current_sources_and_archives_have_coordinate_evidence(path, tmp_path):
    pack = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    sources = {}
    for point_path in sorted((path.parent / "points").glob("*.yaml")):
        source = yaml.safe_load(point_path.read_text(encoding="utf-8-sig"))
        assert not location_errors(source, True), (point_path.name, location_errors(source, True))
        sources[source["point"]["id"]] = source
    assert sources
    build_pack(path.parent, tmp_path, verbose=False)
    archives = sorted((tmp_path / "packs").glob("*.guidepack"))
    assert len(archives) == 2
    for archive in archives:
        with zipfile.ZipFile(archive) as z:
            manifest = json.loads(z.read("manifest.json"))
            points = json.loads(z.read("points.json"))["points"]
        assert manifest["packVersion"] == pack["version"]
        assert len(points) == manifest["guidePointCount"] == len(sources)
        assert {p["id"] for p in points} == set(sources)
        for point in points:
            assert point.get("location") == sources[point["id"]]["point"].get("location")
            assert point.get("googleMapsUrl") == sources[point["id"]]["point"].get("googleMapsUrl")
            errors = location_errors({"point": point, "locationReview": point["extensions"].get("nearbyGuide.locationReview")}, True)
            assert not errors, (point["id"], errors)
