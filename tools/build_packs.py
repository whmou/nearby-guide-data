"""
tools/build_packs.py — Build deterministic .guidepack ZIP archives from source YAML.

Usage:
    python tools/build_packs.py --all --output dist
    python tools/build_packs.py --region tw/hsinchu --output dist

Each pack produces two archives:
  <packId>-<version>-compact.guidepack   (no media files)
  <packId>-<version>-complete.guidepack  (with media files, if present)
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

# Fixed timestamp for reproducible ZIPs (year, month, day, hour, min, sec)
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
    info.external_attr = 0o644 << 16  # normalized Unix permissions
    return info


# ---------------------------------------------------------------------------
# Points JSON generation
# ---------------------------------------------------------------------------

def _build_point_record(point_data: dict) -> dict:
    """Convert source point YAML data to the compact points.json record."""
    p = point_data["point"]
    re_data = point_data.get("ratingEvidence", {})
    media = point_data.get("media", [])

    # Build stable-key-order dict
    record: dict[str, Any] = {
        "id": p["id"],
        "parentId": p.get("parentId"),
        "kind": p["kind"],
        "title": p["title"],
        "summary": p["summary"],
        "narration": p["narration"],
        "observationPrompt": p["observationPrompt"],
        "countryCode": p["countryCode"],
        "adminAreaLevel1": p["adminAreaLevel1"],
        "hierarchy": p["hierarchy"],
        "tagGroups": p["tagGroups"],
        "indoor": p["indoor"],
        "location": p["location"],
        "trigger": p["trigger"],
        "locationHint": p.get("locationHint"),
        "nearbyGuideRating": re_data.get("final"),
        "media": [
            {
                "id": m["id"],
                "type": m["type"],
                "creator": m["creator"],
                "license": m["license"],
                "licenseUrl": m["licenseUrl"],
                "compactPath": m.get("compactPath"),
                "completePath": m.get("completePath"),
            }
            for m in media
        ],
    }
    return record


# ---------------------------------------------------------------------------
# Build a single pack
# ---------------------------------------------------------------------------

def build_pack(pack_dir: Path, output_dir: Path, verbose: bool = True) -> dict[str, Any]:
    """Build compact and complete guidepacks for a pack directory.

    Returns catalog entry dict.
    """
    pack_yaml_path = pack_dir / "pack.yaml"
    pack_data = _load_yaml(pack_yaml_path)

    pack_id = pack_data["packId"]
    version = pack_data["version"]
    # Note: builtAt is intentionally omitted from the archive manifest so that
    # builds are fully reproducible (same source → identical bytes on any OS).

    # Collect points
    points_dir = pack_dir / "points"
    point_files = sorted(points_dir.glob("*.yaml"))
    points: list[dict] = []
    for pf in point_files:
        pd = _load_yaml(pf)
        points.append(_build_point_record(pd))

    # Build points.json bytes
    points_json_obj = {
        "format": "nearby-guide-points",
        "schemaVersion": 1,
        "points": points,
        "extensions": {},
    }
    points_json_bytes = json.dumps(
        points_json_obj, ensure_ascii=False, indent=2, sort_keys=False
    ).encode("utf-8")

    packs_dir = output_dir / "packs"
    packs_dir.mkdir(parents=True, exist_ok=True)

    results: dict[str, Any] = {}

    for variant in ("compact", "complete"):
        filename = f"{pack_id}-{version}-{variant}.guidepack"
        out_path = packs_dir / filename

        # Files to include
        file_entries: list[tuple[str, bytes]] = []
        file_entries.append(("points.json", points_json_bytes))

        # Add media for complete variant
        if variant == "complete":
            media_base = pack_dir / "media"
            if media_base.exists():
                for mf in sorted(media_base.rglob("*")):
                    if mf.is_file() and mf.name != "source.yaml":
                        rel = mf.relative_to(pack_dir).as_posix()
                        file_entries.append((rel, mf.read_bytes()))

        # Build manifest
        manifest_files: list[dict] = []
        for name, data in file_entries:
            manifest_files.append({
                "path": name,
                "bytes": len(data),
                "sha256": _sha256(data),
            })

        variant_titles = {
            "compact": {"title": "精簡離線", "description": "文字與壓縮縮圖離線", "includes": ["text", "thumbnails"]},
            "complete": {"title": "完整離線", "description": "文字與完整多媒體離線，以圖片為主", "includes": ["text", "images", "media"]},
        }
        manifest_obj = {
            "format": "nearby-guide-pack",
            "schemaVersion": 1,
            "packId": pack_id,
            "packVersion": version,
            "variantId": variant,
            "mediaMode": variant,
            "title": pack_data["title"],
            "contentLanguage": pack_data["contentLanguage"],
            "region": pack_data["region"],
            "guidePointCount": len(points),
            "minAppVersionCode": pack_data["minAppVersionCode"],
            "pointsFile": "points.json",
            "files": manifest_files,
            "extensions": {},
        }
        manifest_bytes = json.dumps(
            manifest_obj, ensure_ascii=False, indent=2
        ).encode("utf-8")

        # Write deterministic ZIP
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", allowZip64=False) as zf:
            # manifest first, stored (not compressed)
            info = _make_zip_info("manifest.json", zipfile.ZIP_STORED)
            zf.writestr(info, manifest_bytes)
            # then other files, sorted, deflated
            for name, data in sorted(file_entries, key=lambda x: x[0]):
                info = _make_zip_info(name, zipfile.ZIP_DEFLATED)
                zf.writestr(info, data)

        zip_bytes = buf.getvalue()
        out_path.write_bytes(zip_bytes)

        archive_sha256 = _sha256(zip_bytes)
        archive_bytes = len(zip_bytes)

        if verbose:
            print(f"  {variant}: {out_path.name} ({archive_bytes:,} bytes, sha256={archive_sha256[:16]}…)")

        results[variant] = {
            "filename": filename,
            "url": f"https://github.com/whmou/nearby-guide-data/releases/latest/download/{filename}",
            "bytes": archive_bytes,
            "sha256": archive_sha256,
        }

    return {
        "packId": pack_id,
        "version": version,
        "title": pack_data["title"],
        "subtitle": pack_data["subtitle"],
        "region": pack_data["region"],
        "contentLanguage": pack_data["contentLanguage"],
        "minAppVersionCode": pack_data["minAppVersionCode"],
        "guidePointCount": len(points),
        "compact": results["compact"],
        "complete": results["complete"],
    }


# ---------------------------------------------------------------------------
# Top-level builders
# ---------------------------------------------------------------------------

def build_all(output_dir: Path) -> list[dict]:
    """Build all packs and return list of catalog entries."""
    entries = []
    pack_dirs = sorted(
        p.parent for p in REGIONS_DIR.rglob("pack.yaml") if p.parent != REGIONS_DIR
    )
    for pack_dir in pack_dirs:
        pack_data = yaml.safe_load((pack_dir / "pack.yaml").read_text(encoding="utf-8"))
        print(f"Building {pack_data['packId']} v{pack_data['version']} …")
        entry = build_pack(pack_dir, output_dir)
        entries.append(entry)
    return entries


def build_region(region_path: str, output_dir: Path) -> list[dict]:
    """Build a single region."""
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

    if args.all:
        entries = build_all(output_dir)
    else:
        entries = build_region(args.region, output_dir)

    print(f"\nBuilt {len(entries)} pack(s) into {output_dir}/packs/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
