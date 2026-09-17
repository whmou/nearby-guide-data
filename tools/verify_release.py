"""Download public catalog assets, verify byte/hash and the shipped GPS contract."""
import argparse
import hashlib
import io
import json
import os
import subprocess
import urllib.request
import zipfile
from pathlib import Path
from location_contract import location_errors
from android_contract import point_errors


def verify(catalog_path, transport="urllib"):
    catalog = json.loads(Path(catalog_path).read_text(encoding="utf-8"))
    seen = set()
    for pack in catalog["packs"]:
        if pack["packId"] in seen:
            raise ValueError("Duplicate packId")
        seen.add(pack["packId"])
        for variant in pack["variants"]:
            url = variant["downloadUrl"]
            if "/releases/download/" not in url:
                raise ValueError("Release URL must be pinned")
            print(f"Downloading {pack['packId']} {variant['variantId']} ({variant['downloadBytes']:,} bytes)", flush=True)
            if transport == "curl":
                # Explicit alternate client for local networking problems;
                # fetch the same anonymous public URL, never an API/mirror.
                result = subprocess.run(
                    ["curl.exe" if os.name == "nt" else "curl", "--ipv4", "--fail", "--location",
                     "--silent", "--show-error", "--connect-timeout", "15", "--max-time", "90", "--url", url],
                    check=True, capture_output=True, timeout=100,
                )
                payload = result.stdout
            else:
                with urllib.request.urlopen(url, timeout=120) as response:
                    payload = response.read()
            assert len(payload) == variant["downloadBytes"], url
            assert hashlib.sha256(payload).hexdigest() == variant["sha256"], url
            with zipfile.ZipFile(io.BytesIO(payload)) as archive:
                manifest = json.loads(archive.read("manifest.json"))
                points = json.loads(archive.read(manifest["pointsFile"]))["points"]
                assert (manifest["packId"], manifest["packVersion"], manifest["variantId"]) == (pack["packId"], pack["version"], variant["variantId"])
                assert len(points) == manifest["guidePointCount"] == pack["guidePointCount"]
                for entry in manifest["files"]:
                    data = archive.read(entry["path"])
                    assert len(data) == entry["bytes"]
                    assert hashlib.sha256(data).hexdigest() == entry["sha256"]
                for point in points:
                    errors = point_errors(point)
                    assert not errors, (point["id"], errors)
                    errors = location_errors({"point": point, "locationReview": point.get("extensions", {}).get("nearbyGuide.locationReview")}, True)
                    assert not errors, (point["id"], errors)
            print(f"OK {pack['packId']} {pack['version']} {variant['variantId']}: {len(points)} points, hash + coordinates + Android locationHint verified", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--transport", choices=("urllib", "curl"), default="urllib")
    args = parser.parse_args()
    verify(args.catalog, args.transport)
