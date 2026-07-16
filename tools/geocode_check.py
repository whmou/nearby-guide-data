"""
tools/geocode_check.py — Check/fix point coordinates via Nominatim.

Only accepts geocoded results that fall WITHIN the region's bounding box.
Results outside the box are silently ignored (Nominatim found a different
place with the same name elsewhere in the world).

Usage:
    python tools/geocode_check.py             # report only
    python tools/geocode_check.py --apply     # update mismatches ≥ MIN_DIST
"""

from __future__ import annotations

import argparse
import math
import re
import sys
import time
from pathlib import Path

import requests
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
REGIONS = REPO_ROOT / "regions"

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "NearbyGuide-dataset-geocode-check/1.0 (whmou@gmail.com)"}
DELAY_S = 1.1  # Nominatim policy: max 1 req/s

# Bounding box per country — only accept geocoded results inside these boxes
REGION_BOUNDS = {
    "tw": {"lat": (24.60, 24.96), "lng": (120.78, 121.30)},
    "jp": {"lat": (24.55, 25.10), "lng": (124.80, 125.65)},
}

# Points where Nominatim's in-region result is known to be wrong
# (the stored coordinate is actually more accurate)
SKIP_NOMINATIM = {
    "jp-miyakojima-marine-park",       # Nominatim → Hirara; real location is south Miyako
    "jp-miyakojima-ikema-wetland",     # Nominatim → Irabu area; wetland is near Ikema island
    "jp-miyakojima-kurima-island",     # Nominatim → bridge area; stored island center is correct
    "jp-miyakojima-kurima-viewpoint",  # same reason
    "jp-miyakojima-yonaha-maehama",    # Nominatim 6km north; stored (24.676, 125.256) is closer
    "tw-hsinchu-qingcao-lake",         # Nominatim → wrong lake; stored (24.786, 121.004) is correct
}

REGION_CONFIG = {
    "tw": {"country_code": "tw", "suffix": ", 台灣"},
    "jp": {"country_code": "jp", "suffix": ", 沖縄県"},
}


def haversine_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6_371_000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin(math.radians(lat2 - lat1) / 2) ** 2 + \
        math.cos(p1) * math.cos(p2) * math.sin(math.radians(lng2 - lng1) / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def in_bounds(lat: float, lng: float, country: str) -> bool:
    b = REGION_BOUNDS.get(country, {})
    return (b["lat"][0] <= lat <= b["lat"][1]) and (b["lng"][0] <= lng <= b["lng"][1])


def nominatim_search(query: str, country_code: str) -> tuple[float, float] | None:
    for q in [query, query.split("（")[0].strip(), query.split("(")[0].strip()]:
        try:
            r = requests.get(
                NOMINATIM_URL,
                params={"q": q, "format": "json", "limit": 1, "countrycodes": country_code},
                headers=HEADERS,
                timeout=10,
            )
            r.raise_for_status()
            results = r.json()
            if results:
                return float(results[0]["lat"]), float(results[0]["lon"])
        except Exception as exc:
            print(f"  Nominatim error for {q!r}: {exc}", file=sys.stderr)
        time.sleep(DELAY_S)
    return None


def get_country(path: Path) -> str:
    for i, part in enumerate(path.parts):
        if part == "regions" and i + 1 < len(path.parts):
            return path.parts[i + 1]
    return "tw"


def update_file(path: Path, new_lat: float, new_lng: float) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"(latitude:\s*)[\d.\-]+", lambda m: f"{m.group(1)}{new_lat}", text, count=1)
    text = re.sub(r"(longitude:\s*)[\d.\-]+", lambda m: f"{m.group(1)}{new_lng}", text, count=1)
    new_url = f"https://maps.google.com/maps?q={new_lat},{new_lng}"
    text = re.sub(r'(googleMapsUrl:\s*")[^"]+"', f'\\g<1>{new_url}"', text, count=1)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true",
                        help="Update YAML files for mismatches ≥ --min-dist")
    parser.add_argument("--min-dist", type=int, default=500,
                        help="Min distance (m) to apply (default: 500)")
    args = parser.parse_args()

    point_files = sorted(REGIONS.rglob("points/*.yaml"))
    print(f"Checking {len(point_files)} points (bounding-box filter ON)…\n")

    applied, skipped_manual, skipped_oob, skipped_dist, no_result, ok_count = 0, 0, 0, 0, 0, 0

    for pf in point_files:
        data = yaml.safe_load(pf.read_text(encoding="utf-8"))
        p = data.get("point", {})
        loc = p.get("location")
        if not loc:
            continue

        pid = p["id"]
        title = p.get("title", "")
        country = get_country(pf)
        cfg = REGION_CONFIG.get(country, REGION_CONFIG["tw"])

        stored_lat, stored_lng = loc["latitude"], loc["longitude"]

        geo = nominatim_search(title + cfg["suffix"], cfg["country_code"])
        if not geo:
            no_result += 1
            print(f"  --  {pid}: no Nominatim result")
            continue

        geo_lat, geo_lng = geo

        if not in_bounds(geo_lat, geo_lng, country):
            skipped_oob += 1
            print(f"  OB  {pid}: geocoded ({geo_lat:.4f},{geo_lng:.4f}) outside region bbox → skip")
            continue

        dist = haversine_m(stored_lat, stored_lng, geo_lat, geo_lng)

        if pid in SKIP_NOMINATIM:
            skipped_manual += 1
            print(f"  SK  {pid}: in skip-list, stored kept ({dist:.0f} m diff)")
            continue

        if dist < args.min_dist:
            ok_count += 1
            print(f"  OK  {pid}: {dist:.0f} m")
            continue

        print(
            f"  !! {pid} ({dist:.0f} m)\n"
            f"      stored:   {stored_lat},{stored_lng}\n"
            f"      geocoded: {geo_lat},{geo_lng}"
        )

        if args.apply:
            update_file(pf, geo_lat, geo_lng)
            applied += 1
            print(f"      → UPDATED")

    print(f"\n=== Summary ===")
    print(f"OK (< {args.min_dist} m):      {ok_count}")
    print(f"Updated:             {applied}")
    print(f"Skipped (manual):    {skipped_manual}")
    print(f"Skipped (out-bbox):  {skipped_oob}")
    print(f"No Nominatim result: {no_result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
