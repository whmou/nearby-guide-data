"""
tools/add_google_maps_urls.py — Inject googleMapsUrl into point YAMLs from coordinates.

Usage:
    python tools/add_google_maps_urls.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGIONS = REPO_ROOT / "regions"


def make_maps_url(lat: float, lng: float) -> str:
    return f"https://maps.google.com/maps?q={lat},{lng}"


def inject_url(path: Path, dry_run: bool = False) -> str | None:
    """Return the URL added, or None if already set or no coordinates."""
    text = path.read_text(encoding="utf-8")

    # Skip if already has googleMapsUrl
    if "googleMapsUrl:" in text:
        return None

    # Extract lat/lng via regex (works without round-tripping the whole YAML)
    lat_m = re.search(r"^\s+latitude:\s*([\d.\-]+)", text, re.MULTILINE)
    lng_m = re.search(r"^\s+longitude:\s*([\d.\-]+)", text, re.MULTILINE)
    if not lat_m or not lng_m:
        return None

    lat = float(lat_m.group(1))
    lng = float(lng_m.group(1))
    url = make_maps_url(lat, lng)

    # Insert googleMapsUrl right before the trigger: block
    # The structure is always:  location: ... trigger: ...
    new_text = re.sub(
        r"(  trigger:)",
        f'  googleMapsUrl: "{url}"\n\\1',
        text,
        count=1,
    )

    if new_text == text:
        # Fallback: insert before locationHint:
        new_text = re.sub(
            r"(  locationHint:)",
            f'  googleMapsUrl: "{url}"\n\\1',
            text,
            count=1,
        )

    if new_text == text:
        return None  # couldn't find insertion point

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return url


def main() -> int:
    parser = argparse.ArgumentParser(description="Add googleMapsUrl to point YAMLs")
    parser.add_argument("--dry-run", action="store_true", help="Print what would change without writing")
    args = parser.parse_args()

    point_files = sorted(REGIONS.rglob("points/*.yaml"))
    added = 0
    skipped = 0
    failed = 0

    for pf in point_files:
        url = inject_url(pf, dry_run=args.dry_run)
        if url:
            added += 1
            label = "[DRY] " if args.dry_run else ""
            print(f"{label}+ {pf.parent.parent.name}/{pf.name}: {url}")
        elif "googleMapsUrl:" in pf.read_text(encoding="utf-8"):
            skipped += 1
        else:
            failed += 1
            print(f"WARN: could not inject into {pf.name}", file=sys.stderr)

    action = "Would add" if args.dry_run else "Added"
    print(f"\n{action} googleMapsUrl to {added} files, {skipped} already set, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
