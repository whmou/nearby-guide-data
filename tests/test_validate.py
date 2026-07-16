"""
tests/test_validate.py — pytest suite for tools/validate.py.
"""

from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

import pytest

# Add tools/ to path so we can import validate.py
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import validate  # noqa: E402  (after sys.path manipulation)

FIXTURES_VALID = REPO_ROOT / "tests" / "fixtures" / "valid"
FIXTURES_INVALID = REPO_ROOT / "tests" / "fixtures" / "invalid"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _taxonomy():
    return validate._load_taxonomy_tags()


def _validate_fixture(name: str) -> validate.ValidationResult:
    """Run validate_fixture on a named fixture directory."""
    return validate.validate_fixture(FIXTURES_VALID / name)


def _validate_invalid(name: str) -> validate.ValidationResult:
    return validate.validate_fixture(FIXTURES_INVALID / name)


# ---------------------------------------------------------------------------
# Valid fixture must pass
# ---------------------------------------------------------------------------

def test_valid_fixture_passes():
    result = _validate_fixture("tw-hsinchu-test")
    assert result.ok, f"Expected no errors, got:\n" + "\n".join(str(e) for e in result.errors)


# ---------------------------------------------------------------------------
# Duplicate point ID fails
# ---------------------------------------------------------------------------

def test_duplicate_point_id_fails():
    result = _validate_invalid("duplicate-id")
    assert not result.ok
    assert any("Duplicate" in e.message for e in result.errors), \
        f"Expected 'Duplicate' error, got: {[e.message for e in result.errors]}"


# ---------------------------------------------------------------------------
# Cyclic parentId fails
# ---------------------------------------------------------------------------

def test_cyclic_parent_id_fails():
    result = _validate_invalid("cyclic-parent")
    assert not result.ok
    assert any("Cycle" in e.message or "cycle" in e.message.lower() for e in result.errors), \
        f"Expected cycle error, got: {[e.message for e in result.errors]}"


# ---------------------------------------------------------------------------
# Blank title fails
# ---------------------------------------------------------------------------

def test_blank_title_fails():
    result = _validate_invalid("blank-title")
    assert not result.ok
    # Either schema error (minLength) or blank field check
    messages = " ".join(e.message for e in result.errors)
    assert (
        "title" in messages.lower()
        or "minLength" in messages
        or "blank" in messages.lower()
        or "non-empty" in messages
        or "should be" in messages
    ), f"Expected title error, got: {[e.message for e in result.errors]}"


# ---------------------------------------------------------------------------
# Invalid coordinates fail
# ---------------------------------------------------------------------------

def test_invalid_coordinates_fail():
    result = _validate_invalid("invalid-coords")
    assert not result.ok
    messages = " ".join(e.message for e in result.errors)
    assert "latitude" in messages.lower() or "out of range" in messages.lower() or "maximum" in messages.lower(), \
        f"Expected coordinate error, got: {[e.message for e in result.errors]}"


# ---------------------------------------------------------------------------
# Rating out of range fails
# ---------------------------------------------------------------------------

def test_rating_out_of_range_fails():
    result = _validate_invalid("rating-out-of-range")
    assert not result.ok
    messages = " ".join(e.message for e in result.errors)
    assert "score" in messages.lower() or "rating" in messages.lower() or "range" in messages.lower() or "maximum" in messages.lower(), \
        f"Expected rating error, got: {[e.message for e in result.errors]}"


# ---------------------------------------------------------------------------
# Indoor item missing locationHint fails
# ---------------------------------------------------------------------------

def test_indoor_missing_location_hint_fails():
    result = _validate_invalid("indoor-no-hint")
    assert not result.ok
    assert any("locationHint" in e.message or "indoor" in e.message.lower() for e in result.errors), \
        f"Expected locationHint error, got: {[e.message for e in result.errors]}"


# ---------------------------------------------------------------------------
# Unknown tag ID fails
# ---------------------------------------------------------------------------

def test_unknown_tag_id_fails():
    result = _validate_invalid("unknown-tag")
    assert not result.ok
    assert any("tag" in e.message.lower() for e in result.errors), \
        f"Expected tag error, got: {[e.message for e in result.errors]}"


# ---------------------------------------------------------------------------
# Placeholder content fails
# ---------------------------------------------------------------------------

def test_placeholder_content_fails():
    result = _validate_invalid("placeholder-content")
    assert not result.ok
    assert any("placeholder" in e.message.lower() or "TODO" in e.message for e in result.errors), \
        f"Expected placeholder error, got: {[e.message for e in result.errors]}"


# ---------------------------------------------------------------------------
# Archive path traversal fails
# ---------------------------------------------------------------------------

def test_archive_path_traversal_fails(tmp_path: Path):
    """Create a ZIP with a path traversal entry and verify validate rejects it."""
    archive_path = tmp_path / "evil.guidepack"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        # Normal file
        info = zipfile.ZipInfo("points.json")
        zf.writestr(info, '{"schemaVersion":1,"packId":"x","points":[]}')
        # Path traversal
        info2 = zipfile.ZipInfo("../../../etc/passwd")
        zf.writestr(info2, "root:x:0:0:root:/root:/bin/bash")
    archive_path.write_bytes(buf.getvalue())

    result = validate.validate_archive(archive_path)
    assert not result.ok
    assert any("traversal" in e.message.lower() or "forbidden" in e.message.lower() for e in result.errors), \
        f"Expected traversal error, got: {[e.message for e in result.errors]}"


# ---------------------------------------------------------------------------
# Production packs validate cleanly
# ---------------------------------------------------------------------------

def test_production_hsinchu_pack_validates():
    """Full validation of the real tw/hsinchu production pack."""
    result = validate.validate_region("tw/hsinchu")
    assert result.ok, f"Production pack tw/hsinchu has errors:\n" + "\n".join(str(e) for e in result.errors)


def test_production_miyakojima_pack_validates():
    """Full validation of the real jp/miyako-jima production pack."""
    result = validate.validate_region("jp/miyako-jima")
    assert result.ok, f"Production pack jp/miyako-jima has errors:\n" + "\n".join(str(e) for e in result.errors)


# ---------------------------------------------------------------------------
# Rating formula correctness
# ---------------------------------------------------------------------------

def test_rating_formula_correct():
    """Verify _round_half_up and the weighted formula."""
    assert validate._round_half_up(3.85, 1) == 3.9
    assert validate._round_half_up(3.80, 1) == 3.8
    assert validate._round_half_up(3.05, 1) == 3.1
    assert validate._round_half_up(4.65, 1) == 4.7
    assert validate._round_half_up(4.25, 1) == 4.3
    assert validate._round_half_up(3.15, 1) == 3.2


def test_rating_calculation_matches_declared():
    """Validate that all production point files have correct final scores."""
    result = validate.validate_all()
    rating_errors = [e for e in result.errors if "ratingEvidence.final" in e.message]
    assert not rating_errors, \
        f"Rating calculation mismatches:\n" + "\n".join(str(e) for e in rating_errors)


# ---------------------------------------------------------------------------
# Android schema contract tests
# ---------------------------------------------------------------------------

def _open_built_pack(variant: str, pack_id: str) -> dict:
    """Open a built guidepack and return (manifest, points_list)."""
    import build_packs
    dist_dir = REPO_ROOT / "dist" / "packs"
    candidates = list(dist_dir.glob(f"{pack_id}-*-{variant}.guidepack"))
    assert candidates, f"No built {pack_id} {variant} pack found in dist/packs — run build_packs.py first"
    with zipfile.ZipFile(candidates[0]) as zf:
        manifest = json.loads(zf.read("manifest.json"))
        points_data = json.loads(zf.read("points.json"))
    return manifest, points_data["points"]


def test_manifest_has_created_at():
    """manifest.json must contain a non-empty createdAt field (required by Android app)."""
    for pack_id in ("tw-hsinchu", "jp-miyakojima"):
        for variant in ("compact", "complete"):
            manifest, _ = _open_built_pack(variant, pack_id)
            assert "createdAt" in manifest, f"{pack_id} {variant} manifest missing createdAt"
            assert manifest["createdAt"], f"{pack_id} {variant} manifest.createdAt is empty"


def test_media_runtime_fields():
    """Every media item in points.json must use mimeType + credit, not compactPath/completePath/creator."""
    for pack_id in ("tw-hsinchu", "jp-miyakojima"):
        for variant in ("compact", "complete"):
            _, points = _open_built_pack(variant, pack_id)
            for pt in points:
                for m in pt.get("media", []):
                    pid = pt["id"]
                    mid = m.get("id", "?")
                    assert "mimeType" in m, f"{pid}/{mid}: missing mimeType in {variant}"
                    assert "creator" not in m, f"{pid}/{mid}: 'creator' must be 'credit' in {variant}"
                    assert "compactPath" not in m, f"{pid}/{mid}: compactPath must not appear in runtime"
                    assert "completePath" not in m, f"{pid}/{mid}: completePath must not appear in runtime"
                    # 'path' may be absent if image file not yet downloaded — that's OK
                    # but if present it must be a non-empty string
                    if "path" in m:
                        assert m["path"], f"{pid}/{mid}: path is blank in {variant}"


def test_manifest_pack_version_field():
    """manifest.json must use 'packVersion', not 'version'."""
    for pack_id in ("tw-hsinchu", "jp-miyakojima"):
        manifest, _ = _open_built_pack("compact", pack_id)
        assert "packVersion" in manifest, f"{pack_id} manifest missing packVersion"
        assert "version" not in manifest, f"{pack_id} manifest must not have bare 'version' field"


def test_points_json_format_wrapper():
    """points.json must have format:'nearby-guide-points' and extensions:{{}} wrapper."""
    for pack_id in ("tw-hsinchu", "jp-miyakojima"):
        dist_dir = REPO_ROOT / "dist" / "packs"
        candidates = list(dist_dir.glob(f"{pack_id}-*-compact.guidepack"))
        assert candidates
        with zipfile.ZipFile(candidates[0]) as zf:
            pts = json.loads(zf.read("points.json"))
        assert pts.get("format") == "nearby-guide-points", f"{pack_id}: wrong format in points.json"
        assert "extensions" in pts, f"{pack_id}: points.json missing extensions"


# ---------------------------------------------------------------------------
# v1.0.1 media / build regression tests
# ---------------------------------------------------------------------------

import glob as _glob

import yaml as _yaml

DIST_PACKS = REPO_ROOT / "dist" / "packs"
REGIONS = REPO_ROOT / "regions"

_HEX64 = None


def _require_dist():
    if not DIST_PACKS.exists() or not any(DIST_PACKS.glob("*.guidepack")):
        pytest.skip("no built packs in dist/packs — run build_packs.py first")


def _pack_path(pack_id: str, variant: str) -> Path:
    _require_dist()
    cands = sorted(DIST_PACKS.glob(f"{pack_id}-*-{variant}.guidepack"))
    if not cands:
        pytest.skip(f"no {pack_id} {variant} pack built")
    return cands[-1]


def _open_pack(pack_id: str, variant: str):
    p = _pack_path(pack_id, variant)
    with zipfile.ZipFile(p) as zf:
        manifest = json.loads(zf.read("manifest.json"))
        points = json.loads(zf.read("points.json"))["points"]
        names = set(zf.namelist())
    return manifest, points, names


def _iter_source_points():
    for pf in sorted(REGIONS.rglob("points/*.yaml")):
        data = _yaml.safe_load(pf.read_text(encoding="utf-8"))
        yield pf, data


PACK_IDS = ("tw-hsinchu", "jp-miyakojima")
VARIANTS = ("compact", "complete")


def test_source_media_files_exist():
    for pf, data in _iter_source_points():
        pack_dir = pf.parent.parent
        for m in data.get("media", []):
            for key in ("compactPath", "completePath"):
                rel = m.get(key)
                assert rel, f"{pf.name}: media missing {key}"
                assert (pack_dir / rel).exists(), f"{pf.name}: {key} file missing: {rel}"


def test_original_sha256_populated():
    import re as _re
    hex64 = _re.compile(r"^[0-9a-f]{64}$")
    for pf, data in _iter_source_points():
        for m in data.get("media", []):
            sha = m.get("originalSha256")
            assert sha, f"{pf.name}: originalSha256 is null/empty"
            assert hex64.match(sha), f"{pf.name}: originalSha256 not 64 hex chars: {sha!r}"


def test_built_media_has_required_fields():
    for pack_id in PACK_IDS:
        for variant in VARIANTS:
            _, points, _ = _open_pack(pack_id, variant)
            for pt in points:
                for m in pt.get("media", []):
                    for field in ("mimeType", "path", "credit", "license", "sourceUrl"):
                        assert field in m and m[field], \
                            f"{pack_id}/{variant} {pt['id']}: media missing '{field}'"


def test_media_path_in_zip():
    for pack_id in PACK_IDS:
        for variant in VARIANTS:
            _, points, names = _open_pack(pack_id, variant)
            for pt in points:
                for m in pt.get("media", []):
                    assert m["path"] in names, \
                        f"{pack_id}/{variant} {pt['id']}: path {m['path']} not in ZIP"


def test_media_path_in_manifest_files():
    for pack_id in PACK_IDS:
        for variant in VARIANTS:
            manifest, points, _ = _open_pack(pack_id, variant)
            declared = {f["path"] for f in manifest.get("files", [])}
            for pt in points:
                for m in pt.get("media", []):
                    assert m["path"] in declared, \
                        f"{pack_id}/{variant} {pt['id']}: path {m['path']} not in manifest.files"


def test_manifest_bytes_and_sha256_correct():
    import hashlib
    for pack_id in PACK_IDS:
        for variant in VARIANTS:
            p = _pack_path(pack_id, variant)
            with zipfile.ZipFile(p) as zf:
                manifest = json.loads(zf.read("manifest.json"))
                for f in manifest.get("files", []):
                    data = zf.read(f["path"])
                    assert len(data) == f["bytes"], f"{p.name}: {f['path']} bytes mismatch"
                    assert hashlib.sha256(data).hexdigest() == f["sha256"], \
                        f"{p.name}: {f['path']} sha256 mismatch"


def test_compact_has_images():
    for pack_id in PACK_IDS:
        _, _, names = _open_pack(pack_id, "compact")
        extra = names - {"manifest.json", "points.json"}
        webps = [n for n in extra if n.endswith(".webp")]
        assert webps, f"{pack_id} compact has no image files"


def test_complete_larger_than_compact():
    for pack_id in PACK_IDS:
        compact = _pack_path(pack_id, "compact").stat().st_size
        complete = _pack_path(pack_id, "complete").stat().st_size
        assert complete > compact, f"{pack_id}: complete not larger than compact"


def test_complete_images_larger_than_compact():
    for pack_id in PACK_IDS:
        pc = _pack_path(pack_id, "compact")
        pl = _pack_path(pack_id, "complete")
        with zipfile.ZipFile(pc) as zc, zipfile.ZipFile(pl) as zl:
            c_sizes = {i.filename.split("/")[-1]: i.file_size for i in zc.infolist() if i.filename.endswith(".webp")}
            l_sizes = {i.filename.split("/")[-1]: i.file_size for i in zl.infolist() if i.filename.endswith(".webp")}
            common = set(c_sizes) & set(l_sizes)
            assert common, f"{pack_id}: no common images"
            assert any(l_sizes[k] > c_sizes[k] for k in common), \
                f"{pack_id}: no complete image larger than its compact equivalent"


def test_subtitle_in_manifest():
    for pack_id in PACK_IDS:
        for variant in VARIANTS:
            manifest, _, _ = _open_pack(pack_id, variant)
            assert manifest.get("subtitle"), f"{pack_id}/{variant}: subtitle missing/empty"


def test_point_counts():
    expected = {"tw-hsinchu": 36, "jp-miyakojima": 71}
    for pack_id, count in expected.items():
        _, points, _ = _open_pack(pack_id, "compact")
        assert len(points) == count, f"{pack_id}: expected {count} points, got {len(points)}"


def test_no_media_without_path():
    for pack_id in PACK_IDS:
        for variant in VARIANTS:
            _, points, _ = _open_pack(pack_id, variant)
            for pt in points:
                for m in pt.get("media", []):
                    if "sourceUrl" in m:
                        assert m.get("path"), \
                            f"{pack_id}/{variant} {pt['id']}: media has sourceUrl but no path"
