"""
tools/export_viewer_data.py — Export all point data for the web viewer.

Reads source YAML files and writes public/viewer_data.json.
Run after any coordinate or content change.

Usage:
    python tools/export_viewer_data.py
"""
from __future__ import annotations
import json
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    regions_dir = REPO_ROOT / "regions"
    output_dir = REPO_ROOT / "public"
    output_dir.mkdir(exist_ok=True)

    packs = []
    for pack_yaml in sorted(regions_dir.rglob("pack.yaml")):
        pack_dir = pack_yaml.parent
        pack_data = yaml.safe_load(pack_yaml.read_text(encoding="utf-8"))

        points = []
        for point_yaml in sorted(pack_dir.glob("points/*.yaml")):
            raw = yaml.safe_load(point_yaml.read_text(encoding="utf-8"))
            p = raw.get("point", {})
            loc = p.get("location", {})
            media = p.get("media", [])

            # Pick first media source URL for thumbnail preview
            media_url = next(
                (m["url"] for m in media if m.get("url")), None
            )

            # Admission summary
            admissions = p.get("admissions", [])
            admission_free = (
                any(a.get("isFree") for a in admissions) if admissions else None
            )

            rating_block = p.get("rating")
            rating_score = rating_block.get("score") if rating_block else None

            points.append({
                "id": p.get("id"),
                "title": p.get("title", ""),
                "summary": p.get("summary", ""),
                "lat": loc.get("latitude"),
                "lng": loc.get("longitude"),
                "googleMapsUrl": p.get("googleMapsUrl"),
                "indoor": p.get("indoor", False),
                "tags": p.get("tags", []),
                "mediaCount": len(media),
                "mediaSourceUrl": media_url,
                "rating": rating_score,
                "admissionFree": admission_free,
                "triggerRadiusM": p.get("trigger", {}).get("radiusMeters"),
            })

        packs.append({
            "packId": pack_data.get("packId"),
            "title": pack_data.get("title"),
            "subtitle": pack_data.get("subtitle"),
            "version": pack_data.get("version"),
            "region": pack_data.get("region", {}),
            "points": points,
        })

    total = sum(len(p["points"]) for p in packs)
    output = {
        "format": "nearby-guide-viewer-data",
        "packs": packs,
    }

    out_path = output_dir / "viewer_data.json"
    out_path.write_text(
        json.dumps(output, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"Exported {total} points across {len(packs)} packs → {out_path}")


if __name__ == "__main__":
    main()
