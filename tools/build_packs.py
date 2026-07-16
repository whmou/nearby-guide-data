"""
tools/build_packs.py — Build deterministic .guidepack ZIP archives from source YAML.

Usage:
    python tools/build_packs.py --all --output dist
    python tools/build_packs.py --region tw/hsinchu --output dist

Each pack produces two archives:
  <packId>-<version>-compact.guidepack
  <packId>-<version>-complete.guidepack
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
REGIONS_DIR = REPO_ROOT / "regions"

# Fixed ZIP entry timestamp for reproducible archives
ZIP_TIMESTAMP = (2024, 1, 1, 0, 0, 0)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _make_zip_info(name: str, compression: int = zipfile.ZIP_DEFLATED) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=ZIP_TIMESTAMP)
    info.compress_type = compression
    info.external_attr = 0o644 << 16
    return info


# ---------------------------------------------------------------------------
# Media record builder
# ---------------------------------------------------------------------------

def _build_media_record(m: dict, variant: str, pack_dir: Path) -> dict:
    """Build a runtime media item for the given variant.

    Uses compactPath / completePath from source to select the variant-specific
    local path, but only emits 'path' if the file actually exists in the repo.
    Falls back to sourceUrl for remote-only images.
    """
    local_rel: str | None = m.get("compactPath") if variant == "compact" else m.get("completePath")

    has_local = bool(local_rel and (pack_dir / local_rel).exists())

    record: dict[str, Any] = {
        "id": m["id"],
        "type": m["type"],
        "mimeType": "image/webp" if m.get("type") == "image" else m.get("mimeType", ""),
    }

    if has_local:
        record["path"] = local_rel

    if m.get("sourceUrl"):
        record["sourceUrl"] = m["sourceUrl"]

    # 'credit' is the runtime field name; source uses 'creator'
    credit = m.get("creator") or m.get("credit", "")
    if credit:
        record["credit"] = credit

    if m.get("license"):
        record["license"] = m["license"]
    if m.get("licenseUrl"):
        record["licenseUrl"] = m["licenseUrl"]

    content_desc = m.get("contentDescription")
    if content_desc:
        record["contentDescription"] = content_desc

    return record


# ---------------------------------------------------------------------------
# Points JSON generation (variant-specific because media paths differ)
# ---------------------------------------------------------------------------

def _build_point_record(point_data: dict, variant: str, pack_dir: Path) -> dict:
    """Convert source point YAML to a variant-specific runtime record."""
    p = point_data["point"]
    re_data = point_data.get("ratingEvidence", {})
    media_src = point_data.get("media", [])

    record: dict[str, Any] = {
        "id": p["id"],
        "parentId": p.get("parentId"),
        "kind": p["kind"],
        "title": p["title"],
        "summary": p["summary"],
        "narration": p["narration"],
        "nearbyGuideRating": re_data.get("final"),
        "countryCode": p["countryCode"],
        "adminAreaLevel1": p["adminAreaLevel1"],
        "hierarchy": p["hierarchy"],
        "tagGroups": p["tagGroups"],
        "legacyTags": [],
        "media": [_build_media_record(m, variant, pack_dir) for m in media_src],
        "observationPrompt": p.get("observationPrompt"),
        "contentSourceLabel": None,
        "contentSourceUrl": None,
        "googleMapsUrl": None,
        "googleMapsRating": None,
        "googleMapsReviewCount": None,
        "locationHint": p.get("locationHint"),
        "extensions": {},
    }

    if p.get("location"):
        record["location"] = p["location"]
        record["trigger"] = p["trigger"]

    return record


# ---------------------------------------------------------------------------
# Build a single pack
# ---------------------------------------------------------------------------

def build_pack(pack_dir: Path, output_dir: Path, verbose: bool = True) -> dict[str, Any]:
    """Build compact and complete guidepacks. Returns catalog entry dict."""
    pack_data = _load_yaml(pack_dir / "pack.yaml")

    pack_id = pack_data["packId"]
    version = pack_data["version"]
    # createdAt is a fixed field in pack.yaml for reproducibility
    created_at = pack_data.get("createdAt", "2026-07-15T00:00:00Z")

    # Collect source point files (sorted for determinism)
    point_files = sorted((pack_dir / "points").glob("*.yaml"))

    packs_dir = output_dir / "packs"
    packs_dir.mkdir(parents=True, exist_ok=True)

    results: dict[str, Any] = {}

    for variant in ("compact", "complete"):
        # Build variant-specific points list
        points: list[dict] = []
        for pf in point_files:
            pd = _load_yaml(pf)
            points.append(_build_point_record(pd, variant, pack_dir))

        points_json_bytes = json.dumps(
            {
                "format": "nearby-guide-points",
                "schemaVersion": 1,
                "points": points,
                "extensions": {},
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=False,
        ).encode("utf-8")

        # Collect media files present on disk for this variant
        file_entries: list[tuple[str, bytes]] = [("points.json", points_json_bytes)]

        media_subdir = "compact" if variant == "compact" else "complete"
        media_dir = pack_dir / "media" / media_subdir
        if media_dir.exists():
            for mf in sorted(media_dir.rglob("*")):
                if mf.is_file():
                    rel = mf.relative_to(pack_dir).as_posix()
                    file_entries.append((rel, mf.read_bytes()))

        # Build manifest.json
        manifest_files: list[dict] = [
            {"path": name, "bytes": len(data), "sha256": _sha256(data)}
            for name, data in file_entries
        ]

        manifest_obj = {
            "format": "nearby-guide-pack",
            "schemaVersion": 1,
            "packId": pack_id,
            "packVersion": version,
            "variantId": variant,
            "mediaMode": variant,
            "title": pack_data["title"],
            "createdAt": created_at,
            "contentLanguage": pack_data["contentLanguage"],
            "region": pack_data["region"],
            "guidePointCount": len(points),
            "minAppVersionCode": pack_data["minAppVersionCode"],
            "pointsFile": "points.json",
            "files": manifest_files,
            "extensions": {},
        }
        manifest_bytes = json.dumps(manifest_obj, ensure_ascii=False, indent=2).encode("utf-8")

        # Write deterministic ZIP: manifest first (STORED), then others (DEFLATED, sorted)
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", allowZip64=False) as zf:
            zf.writestr(_make_zip_info("manifest.json", zipfile.ZIP_STORED), manifest_bytes)
            for name, data in sorted(file_entries, key=lambda x: x[0]):
                zf.writestr(_make_zip_info(name, zipfile.ZIP_DEFLATED), data)

        zip_bytes = buf.getvalue()
        archive_sha256 = _sha256(zip_bytes)
        archive_bytes = len(zip_bytes)

        out_path = packs_dir / f"{pack_id}-{version}-{variant}.guidepack"
        out_path.write_bytes(zip_bytes)

        if verbose:
            print(f"  {variant}: {out_path.name} ({archive_bytes:,} bytes, sha256={archive_sha256[:16]}…)")

        results[variant] = {
            "filename": out_path.name,
            "url": f"https://github.com/whmou/nearby-guide-data/releases/latest/download/{out_path.name}",
            "bytes": archive_bytes,
            "sha256": archive_sha256,
        }

    return {
        "packId": pack_id,
        "version": version,
        "title": pack_data["title"],
        "subtitle": pack_data.get("subtitle", ""),
        "region": pack_data["region"],
        "contentLanguage": pack_data["contentLanguage"],
        "minAppVersionCode": pack_data["minAppVersionCode"],
        "guidePointCount": len(point_files),
        "compact": results["compact"],
        "complete": results["complete"],
    }


# ---------------------------------------------------------------------------
# Top-level builders
# ---------------------------------------------------------------------------

def build_all(output_dir: Path) -> list[dict]:
    entries = []
    pack_dirs = sorted(
        p.parent for p in REGIONS_DIR.rglob("pack.yaml") if p.parent != REGIONS_DIR
    )
    for pack_dir in pack_dirs:
        pack_data = yaml.safe_load((pack_dir / "pack.yaml").read_text(encoding="utf-8"))
        print(f"Building {pack_data['packId']} v{pack_data['version']} …")
        entries.append(build_pack(pack_dir, output_dir))
    return entries


def build_region(region_path: str, output_dir: Path) -> list[dict]:
    pack_dir = REGIONS_DIR / region_path
    pack_data = yaml.safe_load((pack_dir / "pack.yaml").read_text(encoding="utf-8"))
    print(f"Building {pack_data['packId']} v{pack_data['version']} …")
    return [build_pack(pack_dir, output_dir)]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Build .guidepack archives")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true")
    group.add_argument("--region", metavar="REGION")
    parser.add_argument("--output", required=True, metavar="DIR")
    args = parser.parse_args()

    output_dir = Path(args.output)
    entries = build_all(output_dir) if args.all else build_region(args.region, output_dir)
    print(f"\nBuilt {len(entries)} pack(s) into {output_dir}/packs/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
