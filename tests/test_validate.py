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
