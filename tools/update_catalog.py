"""
tools/update_catalog.py — Regenerate catalog.json from built dist/packs/ artifacts.

For each packId, only the highest semantic version is emitted.  Running the
generator against a dist/packs/ directory that contains both old and new
archives (e.g. 1.0.1 and 1.0.2) is therefore safe — stale artifacts are
silently superseded.

Usage:
    python tools/update_catalog.py --dist dist
    python tools/update_catalog.py --dist dist --output /tmp/catalog.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = REPO_ROOT / "catalog.json"


# ---------------------------------------------------------------------------
# Semantic version comparison
# ---------------------------------------------------------------------------

def _parse_semver(version_str: str) -> tuple:
    """Parse a version string into a comparable tuple.

    Supports N.N.N and N.N.N-prerelease.  A stable release sorts AFTER its
    prerelease (PEP 440 / semver convention).
    """
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:-([\w.]+))?", version_str.strip())
    if not m:
        raise ValueError(f"Cannot parse version: {version_str!r}")
    major, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))
    pre = m.group(4)
    # Stable release > prerelease: stable gets (1,) suffix, prerelease gets (0, pre)
    pre_key = (1,) if pre is None else (0, pre)
    return (major, minor, patch) + pre_key


def _latest_version(versions: list[str]) -> str:
    return max(versions, key=_parse_semver)


# ---------------------------------------------------------------------------
# Catalog generation
# ---------------------------------------------------------------------------

VARIANT_META = {
    "compact": {
        "title": "精簡離線",
        "description": "文字與壓縮縮圖離線",
        "includes": ["text", "thumbnails"],
    },
    "complete": {
        "title": "完整離線",
        "description": "文字與完整多媒體離線，以圖片為主",
        "includes": ["text", "images", "media"],
    },
}


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _read_manifest(archive_path: Path) -> dict:
    with zipfile.ZipFile(archive_path, "r") as zf:
        return json.loads(zf.read("manifest.json"))


def regenerate_catalog(dist_dir: Path, output_path: Path | None = None) -> None:
    packs_dir = dist_dir / "packs"
    if not packs_dir.exists():
        print(f"ERROR: {packs_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    # Collect all (packId, version) → {variant → archive info}
    # Structure: raw_groups[pack_id][version][variant] = {...}
    raw_groups: dict[str, dict[str, dict]] = defaultdict(lambda: defaultdict(dict))
    manifests: dict[tuple, dict] = {}  # (pack_id, version) → manifest

    for archive in sorted(packs_dir.glob("*.guidepack")):
        try:
            manifest = _read_manifest(archive)
        except Exception as exc:
            print(f"WARNING: could not read {archive.name}: {exc}", file=sys.stderr)
            continue

        pack_id = manifest.get("packId", "")
        version = manifest.get("packVersion") or manifest.get("version", "")
        if not pack_id or not version:
            print(f"WARNING: missing packId/version in {archive.name}", file=sys.stderr)
            continue

        try:
            _parse_semver(version)
        except ValueError as exc:
            print(f"WARNING: {archive.name}: {exc}", file=sys.stderr)
            continue

        if archive.name.endswith("-compact.guidepack"):
            variant = "compact"
        elif archive.name.endswith("-complete.guidepack"):
            variant = "complete"
        else:
            print(f"WARNING: unrecognized archive name: {archive.name}", file=sys.stderr)
            continue

        tag = VARIANT_META.get(variant, {})
        base_url = (
            f"https://github.com/whmou/nearby-guide-data/releases/latest/download/{archive.name}"
        )
        raw_groups[pack_id][version][variant] = {
            "variantId": variant,
            "mediaMode": variant,
            "title": tag.get("title", variant),
            "description": tag.get("description", ""),
            "downloadUrl": base_url,
            "downloadBytes": archive.stat().st_size,
            "sha256": _sha256_file(archive),
            "includes": tag.get("includes", []),
        }
        manifests[(pack_id, version)] = manifest

    # For each packId, keep only the highest version
    entries = []
    for pack_id in sorted(raw_groups):
        available_versions = list(raw_groups[pack_id].keys())
        best = _latest_version(available_versions)
        if len(available_versions) > 1:
            dropped = sorted(v for v in available_versions if v != best)
            print(
                f"INFO: {pack_id}: selecting {best}, dropping {dropped}",
                file=sys.stderr,
            )

        variants_by_id = raw_groups[pack_id][best]
        manifest = manifests[(pack_id, best)]

        # Validate: both variants must exist (or warn)
        variants = []
        for v in ("compact", "complete"):
            if v in variants_by_id:
                variants.append(variants_by_id[v])
            else:
                print(f"WARNING: {pack_id} {best}: missing {v} variant", file=sys.stderr)

        entries.append({
            "packId": pack_id,
            "version": best,
            "title": manifest.get("title", ""),
            "subtitle": manifest.get("subtitle", ""),
            "region": manifest.get("region", {}),
            "contentLanguage": manifest.get("contentLanguage", ""),
            "guidePointCount": manifest.get("guidePointCount", 0),
            "minAppVersionCode": manifest.get("minAppVersionCode", 8),
            "variants": variants,
        })

    # Validate unique packId
    pack_ids = [e["packId"] for e in entries]
    duplicates = [pid for pid in set(pack_ids) if pack_ids.count(pid) > 1]
    if duplicates:
        print(f"ERROR: duplicate packId values: {duplicates}", file=sys.stderr)
        sys.exit(1)

    catalog = {
        "format": "nearby-guide-index",
        "schemaVersion": 1,
        "updatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "packs": entries,
    }

    dest = output_path or CATALOG_PATH
    dest.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"catalog.json updated with {len(entries)} pack(s).")


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate catalog.json from dist/packs/")
    parser.add_argument("--dist", default="dist", metavar="DIR")
    parser.add_argument("--output", default=None, metavar="FILE",
                        help="Output path (default: catalog.json in repo root)")
    args = parser.parse_args()
    output = Path(args.output) if args.output else None
    regenerate_catalog(REPO_ROOT / args.dist, output_path=output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
