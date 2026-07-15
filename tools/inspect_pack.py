"""
tools/inspect_pack.py — Inspect and validate a built .guidepack archive.

Usage:
    python tools/inspect_pack.py dist/packs/tw-hsinchu-1.0.0-compact.guidepack
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

FORBIDDEN_PATH = re.compile(
    r"(\.\.|^/|\\|\.DS_Store$|Thumbs\.db$|desktop\.ini$)", re.IGNORECASE
)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inspect(archive_path: Path) -> bool:
    """Return True if the archive passes all checks."""
    ok = True

    if not archive_path.exists():
        print(f"ERROR: file not found: {archive_path}", file=sys.stderr)
        return False

    # ZIP integrity
    try:
        zf = zipfile.ZipFile(archive_path, "r")
    except zipfile.BadZipFile as exc:
        print(f"ERROR: bad ZIP file: {exc}", file=sys.stderr)
        return False

    with zf:
        names = set(zf.namelist())

        # No path traversal
        for name in names:
            if FORBIDDEN_PATH.search(name):
                print(f"ERROR: forbidden path in archive: '{name}'", file=sys.stderr)
                ok = False

        # manifest.json must be present
        if "manifest.json" not in names:
            print("ERROR: manifest.json not found in archive", file=sys.stderr)
            return False

        manifest_bytes = zf.read("manifest.json")
        try:
            manifest = json.loads(manifest_bytes)
        except json.JSONDecodeError as exc:
            print(f"ERROR: manifest.json is not valid JSON: {exc}", file=sys.stderr)
            return False

        # Manifest format check
        if manifest.get("format") != "nearby-guide-pack":
            print(f"ERROR: manifest.format expected 'nearby-guide-pack', got {manifest.get('format')!r}", file=sys.stderr)
            ok = False

        # All declared files present, no undeclared files
        declared_paths = {f["path"] for f in manifest.get("files", [])}
        actual_paths = names - {"manifest.json"}

        for path in sorted(declared_paths - actual_paths):
            print(f"ERROR: declared file missing from archive: '{path}'", file=sys.stderr)
            ok = False

        for path in sorted(actual_paths - declared_paths):
            print(f"ERROR: undeclared file found in archive: '{path}'", file=sys.stderr)
            ok = False

        # File byte counts and SHA-256
        for file_info in manifest.get("files", []):
            path = file_info["path"]
            if path not in names:
                continue
            data = zf.read(path)
            actual_bytes = len(data)
            actual_sha = _sha256(data)

            if actual_bytes != file_info.get("bytes"):
                print(
                    f"ERROR: '{path}' byte count mismatch: expected {file_info.get('bytes')}, got {actual_bytes}",
                    file=sys.stderr,
                )
                ok = False

            if actual_sha != file_info.get("sha256"):
                print(
                    f"ERROR: '{path}' SHA-256 mismatch: expected {file_info.get('sha256')}, got {actual_sha}",
                    file=sys.stderr,
                )
                ok = False

        # points.json validation
        if "points.json" in names:
            points_bytes = zf.read("points.json")
            try:
                points_obj = json.loads(points_bytes)
            except json.JSONDecodeError as exc:
                print(f"ERROR: points.json is not valid JSON: {exc}", file=sys.stderr)
                ok = False
                points_obj = None

            if points_obj is not None:
                actual_count = len(points_obj.get("points", []))
                declared_count = manifest.get("guidePointCount")
                if actual_count != declared_count:
                    print(
                        f"ERROR: guidePointCount mismatch: manifest says {declared_count}, "
                        f"points.json has {actual_count}",
                        file=sys.stderr,
                    )
                    ok = False

    if ok:
        print(f"OK: {archive_path.name}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a .guidepack archive")
    parser.add_argument("archive", help="Path to .guidepack file")
    args = parser.parse_args()

    path = Path(args.archive)
    return 0 if inspect(path) else 1


if __name__ == "__main__":
    sys.exit(main())
