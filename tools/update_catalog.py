"""
tools/update_catalog.py — Regenerate catalog.json from built dist/packs/ artifacts.

Usage:
    python tools/update_catalog.py --dist dist
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = REPO_ROOT / "catalog.json"


def _read_manifest(archive_path: Path) -> dict:
    with zipfile.ZipFile(archive_path, "r") as zf:
        return json.loads(zf.read("manifest.json"))


def regenerate_catalog(dist_dir: Path) -> None:
    packs_dir = dist_dir / "packs"
    if not packs_dir.exists():
        print(f"ERROR: {packs_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    # Group archives by (packId, version)
    from collections import defaultdict
    import hashlib

    groups: dict[tuple, dict] = defaultdict(dict)

    def sha256_file(path: Path) -> str:
        h = hashlib.sha256()
        h.update(path.read_bytes())
        return h.hexdigest()

    for archive in sorted(packs_dir.glob("*.guidepack")):
        try:
            manifest = _read_manifest(archive)
        except Exception as exc:
            print(f"WARNING: could not read {archive.name}: {exc}", file=sys.stderr)
            continue

        pack_id = manifest["packId"]
        version = manifest.get("packVersion") or manifest.get("version", "")
        key = (pack_id, version)

        # Determine variant from filename
        if archive.name.endswith("-compact.guidepack"):
            variant = "compact"
        elif archive.name.endswith("-complete.guidepack"):
            variant = "complete"
        else:
            print(f"WARNING: unrecognized archive name pattern: {archive.name}", file=sys.stderr)
            continue

        archive_bytes = archive.stat().st_size
        archive_sha = sha256_file(archive)

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
        tag = VARIANT_META.get(variant, {})
        base_url = f"https://github.com/whmou/nearby-guide-data/releases/latest/download/{archive.name}"
        groups[key][variant] = {
            "variantId": variant,
            "mediaMode": variant,
            "title": tag.get("title", variant),
            "description": tag.get("description", ""),
            "downloadUrl": base_url,
            "downloadBytes": archive_bytes,
            "sha256": archive_sha,
            "includes": tag.get("includes", []),
        }
        groups[key]["_manifest"] = manifest

    entries = []
    for (pack_id, version), data in sorted(groups.items()):
        manifest = data.pop("_manifest", {})
        variants = []
        for v in ("compact", "complete"):
            if v in data:
                variants.append(data[v])
        entry = {
            "packId": pack_id,
            "version": version,
            "title": manifest.get("title", ""),
            "subtitle": manifest.get("subtitle", ""),
            "region": manifest.get("region", {}),
            "contentLanguage": manifest.get("contentLanguage", ""),
            "guidePointCount": manifest.get("guidePointCount", 0),
            "minAppVersionCode": manifest.get("minAppVersionCode", 8),
            "variants": variants,
        }
        entries.append(entry)

    catalog = {
        "format": "nearby-guide-index",
        "schemaVersion": 1,
        "updatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "packs": entries,
    }

    CATALOG_PATH.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"catalog.json updated with {len(entries)} pack(s).")


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate catalog.json from dist/packs/")
    parser.add_argument("--dist", default="dist", metavar="DIR")
    args = parser.parse_args()
    regenerate_catalog(REPO_ROOT / args.dist)
    return 0


if __name__ == "__main__":
    sys.exit(main())
