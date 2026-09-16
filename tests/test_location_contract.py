import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from location_contract import location_errors, maps_url, distance_m


def example():
    loc = {"latitude": 22.3, "longitude": 120.3}
    return {"point": {"location": loc, "trigger": {"radiusMeters": 80, "rearmDistanceMeters": 800},
                      "googleMapsUrl": maps_url(**loc), "locationHint": "Test fixture entrance"},
            "locationReview": {"status": "verified", "checkedAt": "2026-09-16", "anchorType": "entrance",
                "verifiedLocation": copy.deepcopy(loc), "reason": "Synthetic fixture, not a real attraction",
                "sources": [{"url": "https://example.com/fixture", "title": "Fixture", "coordinateEvidence": "22.3,120.3"}]}}


def test_verified_coordinate_contract():
    assert location_errors(example(), True) == []


def test_maps_url_cannot_drift_from_gps():
    data = example()
    data["point"]["googleMapsUrl"] = maps_url(22.31, 120.3)
    assert any("URL" in x for x in location_errors(data))


def test_maps_url_rejects_nan():
    data = example()
    data["point"]["googleMapsUrl"] = maps_url(float("nan"), 120.3)
    assert location_errors(data)


def test_review_does_not_survive_changed_coordinate():
    data = example()
    data["point"]["location"]["latitude"] += .01
    assert any("re-verify" in x for x in location_errors(data))


def test_inside_region_is_not_verification():
    data = example()
    del data["locationReview"]
    assert location_errors(data, require_review=True)


def test_unresolved_has_no_false_navigation():
    data = example()
    data["locationReview"]["status"] = "unresolved"
    assert location_errors(data)
    for field in ("location", "trigger", "googleMapsUrl"):
        data["point"][field] = None
    assert not location_errors(data)


def test_island_centre_is_not_arrival_anchor():
    data = example()
    data["locationReview"]["anchorType"] = "area"
    assert location_errors(data)


def test_needs_traceable_evidence():
    data = example()
    data["locationReview"]["sources"] = []
    assert location_errors(data)


def test_distance_is_in_metres():
    assert 1000 < distance_m({"latitude":22.3,"longitude":120.3}, {"latitude":22.31,"longitude":120.3}) < 1200


def test_automatic_geocoder_overwrite_is_disabled():
    import subprocess
    tool = Path(__file__).resolve().parents[1] / "tools" / "geocode_check.py"
    result = subprocess.run([sys.executable, str(tool), "--apply"], capture_output=True, text=True, encoding="utf-8")
    assert result.returncode != 0
    assert "Retired" in result.stderr
