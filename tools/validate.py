"""
tools/validate.py — Validate source YAML files against schemas and business rules.

Usage:
    python tools/validate.py --all
    python tools/validate.py --region tw/hsinchu
    python tools/validate.py --fixture tests/fixtures/valid/tw-hsinchu-test
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import jsonschema
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = REPO_ROOT / "schemas"
TAXONOMY_FILE = REPO_ROOT / "taxonomy" / "tags.yaml"
REGIONS_DIR = REPO_ROOT / "regions"

PLACEHOLDER_PATTERNS = re.compile(r"\bTODO\b|\bTBD\b|\bPLACEHOLDER\b|\.\.\.", re.IGNORECASE)

RATING_WEIGHTS = {
    "significance": 0.30,
    "distinctiveness": 0.25,
    "interpretability": 0.20,
    "visitorValue": 0.15,
    "evidenceQuality": 0.10,
}


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class ValidationError:
    path: str
    message: str

    def __str__(self) -> str:
        return f"  ERROR  [{self.path}] {self.message}"


@dataclass
class ValidationResult:
    errors: list[ValidationError] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    def add(self, path: str, message: str) -> None:
        self.errors.append(ValidationError(path=path, message=message))

    def extend(self, other: "ValidationResult") -> None:
        self.errors.extend(other.errors)

    def report(self) -> None:
        for e in self.errors:
            print(str(e), file=sys.stderr)


# ---------------------------------------------------------------------------
# Schema loading (cached)
# ---------------------------------------------------------------------------

_schema_cache: dict[str, dict] = {}


def _load_schema(name: str) -> dict:
    if name not in _schema_cache:
        path = SCHEMAS_DIR / f"{name}.schema.json"
        with open(path, encoding="utf-8") as f:
            _schema_cache[name] = json.load(f)
    return _schema_cache[name]


# ---------------------------------------------------------------------------
# Taxonomy loading (cached)
# ---------------------------------------------------------------------------

_taxonomy_cache: dict[str, set[str]] | None = None


def _load_taxonomy_tags() -> dict[str, set[str]]:
    """Return dict mapping group_id -> set of tag ids."""
    global _taxonomy_cache
    if _taxonomy_cache is None:
        with open(TAXONOMY_FILE, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        _taxonomy_cache = {}
        for group in data.get("groups", []):
            gid = group["id"]
            _taxonomy_cache[gid] = {t["id"] for t in group.get("tags", [])}
    return _taxonomy_cache


# ---------------------------------------------------------------------------
# Individual validators
# ---------------------------------------------------------------------------

def _validate_pack_yaml(pack_path: Path) -> ValidationResult:
    result = ValidationResult()
    rel = str(pack_path.relative_to(REPO_ROOT))
    try:
        with open(pack_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as exc:
        result.add(rel, f"Failed to parse YAML: {exc}")
        return result

    schema = _load_schema("source-pack-v1")
    try:
        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as exc:
        result.add(rel, f"Schema error: {exc.message}")

    return result


def _validate_point_yaml(point_path: Path, taxonomy: dict[str, set[str]]) -> ValidationResult:
    result = ValidationResult()
    rel = str(point_path.relative_to(REPO_ROOT))

    try:
        with open(point_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as exc:
        result.add(rel, f"Failed to parse YAML: {exc}")
        return result

    # Schema validation
    schema = _load_schema("source-point-v1")
    try:
        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as exc:
        result.add(rel, f"Schema error: {exc.message}")
        # Don't continue if schema fails badly — we might get key errors below
        return result

    point = data.get("point", {})

    # Blank field check
    for field_name in ("title", "summary", "narration", "observationPrompt"):
        value = point.get(field_name, "")
        if not value or not str(value).strip():
            result.add(rel, f"point.{field_name} is blank")

    # Placeholder content check
    for field_name in ("title", "summary", "narration", "observationPrompt"):
        value = str(point.get(field_name, ""))
        if PLACEHOLDER_PATTERNS.search(value):
            result.add(rel, f"point.{field_name} contains placeholder text")

    # Coordinate validity
    loc = point.get("location", {})
    lat = loc.get("latitude")
    lon = loc.get("longitude")
    if lat is None or lon is None:
        result.add(rel, "point.location missing latitude or longitude")
    else:
        if not (-90 <= lat <= 90):
            result.add(rel, f"point.location.latitude {lat} is out of range [-90, 90]")
        if not (-180 <= lon <= 180):
            result.add(rel, f"point.location.longitude {lon} is out of range [-180, 180]")

    # Indoor requires locationHint
    if point.get("indoor") is True:
        hint = point.get("locationHint")
        if hint is None or (isinstance(hint, str) and not hint.strip()):
            result.add(rel, "point.locationHint must not be null/empty when point.indoor is true")

    # Trigger required when location is set
    if loc and not point.get("trigger"):
        result.add(rel, "point.trigger is required when point.location is set")

    # Tag ID validation
    taxonomy_tags = taxonomy
    for tg in point.get("tagGroups", []):
        group_id = tg.get("id")
        valid_tags = taxonomy_tags.get(group_id)
        if valid_tags is None:
            result.add(rel, f"tagGroup id '{group_id}' not found in taxonomy/tags.yaml")
            continue
        for tag in tg.get("tags", []):
            tid = tag.get("id")
            if tid not in valid_tags:
                result.add(rel, f"tag id '{tid}' not found in taxonomy group '{group_id}'")

    # Rating validation
    re_data = data.get("ratingEvidence", {})
    _validate_rating(rel, re_data, result)

    # Source completeness
    for src in data.get("sources", []):
        src_id = src.get("id", "?")
        for required_field in ("title", "url", "accessedAt"):
            val = src.get(required_field)
            if not val or not str(val).strip():
                result.add(rel, f"source '{src_id}' has empty or missing '{required_field}'")
        supports = src.get("supports", [])
        if not supports:
            result.add(rel, f"source '{src_id}' has no 'supports' entries")

    return result


def _validate_rating(rel: str, re_data: dict, result: ValidationResult) -> None:
    """Check each dimension score is 0-5 and final matches the weighted formula."""
    for dim in RATING_WEIGHTS:
        dim_data = re_data.get(dim, {})
        score = dim_data.get("score")
        if score is None:
            result.add(rel, f"ratingEvidence.{dim}.score is missing")
            return
        if not isinstance(score, int) or not (0 <= score <= 5):
            result.add(rel, f"ratingEvidence.{dim}.score={score} is out of range [0,5]")

    declared_final = re_data.get("final")
    if declared_final is None:
        result.add(rel, "ratingEvidence.final is missing")
        return

    import decimal as _decimal
    computed = sum(
        _decimal.Decimal(str(RATING_WEIGHTS[dim])) * _decimal.Decimal(str(re_data.get(dim, {}).get("score", 0)))
        for dim in RATING_WEIGHTS
    )
    computed_rounded = _round_half_up(float(computed), 1)

    if abs(declared_final - computed_rounded) > 0.05:
        result.add(
            rel,
            f"ratingEvidence.final={declared_final} does not match computed "
            f"{computed_rounded:.1f} "
            f"(0.30×{re_data.get('significance',{}).get('score',0)} + "
            f"0.25×{re_data.get('distinctiveness',{}).get('score',0)} + "
            f"0.20×{re_data.get('interpretability',{}).get('score',0)} + "
            f"0.15×{re_data.get('visitorValue',{}).get('score',0)} + "
            f"0.10×{re_data.get('evidenceQuality',{}).get('score',0)})"
        )


def _round_half_up(value: float, decimals: int) -> float:
    """Round half-up (0.05 → 0.1 not 0.0) using Decimal for exact arithmetic."""
    import decimal as _decimal
    quantizer = _decimal.Decimal(10) ** -decimals
    d = _decimal.Decimal(str(round(value, decimals + 3)))  # normalize float first
    return float(d.quantize(quantizer, rounding=_decimal.ROUND_HALF_UP))


# ---------------------------------------------------------------------------
# Pack-level validation (uniqueness, parent references)
# ---------------------------------------------------------------------------

def validate_pack_dir(
    pack_dir: Path,
    taxonomy: dict[str, set[str]],
    all_ids: dict[str, Path] | None = None,
) -> ValidationResult:
    """Validate a single pack directory (pack.yaml + all points/*.yaml)."""
    result = ValidationResult()
    pack_yaml = pack_dir / "pack.yaml"

    if not pack_yaml.exists():
        result.add(str(pack_dir), "pack.yaml not found")
        return result

    result.extend(_validate_pack_yaml(pack_yaml))

    points_dir = pack_dir / "points"
    if not points_dir.exists():
        result.add(str(pack_dir), "points/ directory not found")
        return result

    local_ids: dict[str, Path] = {}
    parent_map: dict[str, str | None] = {}

    point_files = sorted(points_dir.glob("*.yaml"))
    for point_path in point_files:
        pr = _validate_point_yaml(point_path, taxonomy)
        result.extend(pr)

        # Collect ID and parentId
        try:
            with open(point_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            point_id = data.get("point", {}).get("id")
            parent_id = data.get("point", {}).get("parentId")
            if point_id:
                rel = str(point_path.relative_to(REPO_ROOT))
                if point_id in local_ids:
                    result.add(rel, f"Duplicate point id '{point_id}' (first seen in {local_ids[point_id]})")
                else:
                    local_ids[point_id] = point_path
                if all_ids is not None:
                    if point_id in all_ids:
                        result.add(rel, f"Duplicate point id '{point_id}' (first seen globally in {all_ids[point_id]})")
                    else:
                        all_ids[point_id] = point_path
                parent_map[point_id] = parent_id
        except Exception:
            pass

    # Cycle detection in parentId references
    _detect_cycles(parent_map, str(pack_dir), result)

    return result


def _detect_cycles(parent_map: dict[str, str | None], context: str, result: ValidationResult) -> None:
    """Detect cycles in parentId references using DFS."""
    UNVISITED, IN_STACK, DONE = 0, 1, 2
    state: dict[str, int] = {k: UNVISITED for k in parent_map}

    def dfs(node: str, stack: list[str]) -> bool:
        if state.get(node, DONE) == DONE:
            return False
        if state.get(node) == IN_STACK:
            cycle = " -> ".join(stack + [node])
            result.add(context, f"Cycle detected in parentId references: {cycle}")
            return True
        state[node] = IN_STACK
        stack.append(node)
        parent = parent_map.get(node)
        if parent and parent in parent_map:
            if dfs(parent, stack):
                return True
        stack.pop()
        state[node] = DONE
        return False

    for node in list(parent_map.keys()):
        if state.get(node, DONE) == UNVISITED:
            dfs(node, [])


# ---------------------------------------------------------------------------
# Archive validation (path traversal)
# ---------------------------------------------------------------------------

def validate_archive(archive_path: Path) -> ValidationResult:
    """Open a .guidepack ZIP and check for path traversal and integrity."""
    import zipfile

    result = ValidationResult()
    rel = str(archive_path)
    FORBIDDEN = re.compile(r"\.\.|^/|\\|\.DS_Store|Thumbs\.db|desktop\.ini", re.IGNORECASE)

    try:
        with zipfile.ZipFile(archive_path, "r") as zf:
            for name in zf.namelist():
                if FORBIDDEN.search(name):
                    result.add(rel, f"Path traversal or forbidden file in archive: '{name}'")
    except zipfile.BadZipFile as exc:
        result.add(rel, f"Bad ZIP file: {exc}")
    except Exception as exc:
        result.add(rel, f"Error reading archive: {exc}")

    return result


# ---------------------------------------------------------------------------
# Top-level entry points
# ---------------------------------------------------------------------------

def validate_all(regions_dir: Path | None = None) -> ValidationResult:
    """Validate all pack directories under regions/."""
    result = ValidationResult()
    base = regions_dir or REGIONS_DIR
    taxonomy = _load_taxonomy_tags()
    all_ids: dict[str, Path] = {}

    pack_dirs = [p.parent for p in base.rglob("pack.yaml") if p.parent != base]
    if not pack_dirs:
        result.add(str(base), "No pack.yaml files found")
        return result

    for pack_dir in sorted(pack_dirs):
        pr = validate_pack_dir(pack_dir, taxonomy, all_ids)
        result.extend(pr)

    return result


def validate_region(region_path: str) -> ValidationResult:
    """Validate a single region by relative path (e.g. 'tw/hsinchu')."""
    taxonomy = _load_taxonomy_tags()
    pack_dir = REGIONS_DIR / region_path
    if not pack_dir.exists():
        r = ValidationResult()
        r.add(str(pack_dir), "Region directory not found")
        return r
    return validate_pack_dir(pack_dir, taxonomy)


def validate_fixture(fixture_path: Path) -> ValidationResult:
    """Validate a fixture directory (for tests)."""
    taxonomy = _load_taxonomy_tags()
    return validate_pack_dir(fixture_path, taxonomy)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate nearby-guide source YAML files")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Validate all regions")
    group.add_argument("--region", metavar="REGION", help="Validate one region (e.g. tw/hsinchu)")
    args = parser.parse_args()

    if args.all:
        result = validate_all()
    else:
        result = validate_region(args.region)

    if result.ok:
        print(f"OK — no validation errors found.")
        return 0
    else:
        print(f"FAILED — {len(result.errors)} error(s):", file=sys.stderr)
        result.report()
        return 1


if __name__ == "__main__":
    sys.exit(main())
