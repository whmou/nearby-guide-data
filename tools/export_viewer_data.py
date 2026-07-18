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


def _flat_tags(tag_groups: list) -> list[str]:
    tags = []
    for g in tag_groups:
        for t in g.get("tags", []):
            label = t.get("label", "")
            if label:
                tags.append(label)
    return tags


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
            media_list = raw.get("media", [])
            rating_ev = raw.get("ratingEvidence", {})

            # First media item
            first_media = media_list[0] if media_list else {}

            points.append({
                "id": p.get("id"),
                "title": p.get("title", ""),
                "summary": p.get("summary", ""),
                "narration": p.get("narration", ""),
                "observationPrompt": p.get("observationPrompt", ""),
                "lat": loc.get("latitude"),
                "lng": loc.get("longitude"),
                "locationHint": loc.get("locationHint", ""),
                "googleMapsUrl": p.get("googleMapsUrl"),
                "indoor": p.get("indoor", False),
                "tags": _flat_tags(p.get("tagGroups", [])),
                # Image paths (relative to guidepack ZIP root)
                "compactPath": first_media.get("compactPath"),
                "mediaSourceUrl": first_media.get("sourceUrl"),
                "mediaCount": len(media_list),
                "rating": rating_ev.get("final"),
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
