"""Print a reviewable apply_patch patch from per-point location evidence.

No edits are made by this script. Apply the output with apply_patch only after
cross-checking evidence. Existing narration, media, IDs and taxonomy survive.
"""
from __future__ import annotations
import json
import re
import argparse
from normalize_authoring_metadata import hunks
from pathlib import Path
import yaml
from location_contract import maps_url, location_errors, distance_m

ROOT = Path(__file__).resolve().parents[1]


def prepare(data, entry):
    p = data["point"]
    old = p.get("location")
    previous = {k: old[k] for k in ("latitude", "longitude")} if old else None
    status = entry["status"]
    if entry["anchorType"] == "area" and status == "verified":
        raise ValueError(f"{p['id']}: regional centroid cannot be auto-approved as arrival anchor")
    review = {"status": status, "anchorType": entry["anchorType"], "checkedAt": "2026-09-16",
              "reason": entry["reason"], "sources": entry["sources"],
              "previousLocation": data.get("locationReview", {}).get("previousLocation", previous)}
    if status == "verified":
        p["location"] = {"latitude": entry["latitude"], "longitude": entry["longitude"]}
        review["verifiedLocation"] = dict(p["location"])
        p["googleMapsUrl"] = maps_url(entry["latitude"], entry["longitude"])
    else:
        p["location"] = None
        p["trigger"] = None
        p["googleMapsUrl"] = None
        review["verifiedLocation"] = None
    p["locationHint"] = entry.get("locationHint") or "位置待確認，請勿依舊座標前往。"
    data["locationReview"] = review
    errors = location_errors(data, True)
    if errors:
        raise ValueError(p["id"] + ": " + "; ".join(errors))
    return data


def replace_field(text, name, value):
    block = yaml.safe_dump({name: value}, allow_unicode=True, sort_keys=False, width=10000).rstrip()
    block = "\n".join("  " + line for line in block.splitlines()) + "\n"
    pattern = rf"^  {name}:.*\n(?:(?:    .*(?:\n|$))|(?:\n))*"
    if re.search(pattern, text, flags=re.M):
        return re.sub(pattern, lambda _: block, text, count=1, flags=re.M)
    return text.replace("ratingEvidence:\n", block + "ratingEvidence:\n", 1)


def render_patch(report_name=None):
    reports = sorted((ROOT / "audits/location-2026-09-16").glob("*.json"))
    entries = {}
    for report in reports:
        if report_name and report.name != report_name:
            continue
        for item in json.loads(report.read_text(encoding="utf-8-sig")):
            if item["id"] in entries:
                raise ValueError("Duplicate audit entry: " + item["id"])
            entries[item["id"]] = item
    patches = ["*** Begin Patch"]
    for path in sorted((ROOT / "regions").glob("*/*/points/*.yaml")):
        old_text = path.read_text(encoding="utf-8-sig")
        data = yaml.safe_load(old_text)
        pid = data["point"]["id"]
        if pid not in entries:
            continue
        prepare(data, entries.pop(pid))
        new_text = old_text
        for field in ("location", "trigger", "googleMapsUrl", "locationHint"):
            new_text = replace_field(new_text, field, data["point"].get(field))
        new_text = re.sub(r"^locationReview:\n[\s\S]*\Z", "", new_text, flags=re.M).rstrip() + "\n"
        new_text += yaml.safe_dump({"locationReview": data["locationReview"]}, allow_unicode=True, sort_keys=False, width=10000)
        if yaml.safe_load(new_text) != data:
            raise ValueError(f"{pid}: text edit does not match intended YAML change")
        if old_text != new_text:
            patches.extend(hunks(path, old_text, new_text))
    if entries:
        raise ValueError("Unknown point IDs: " + ", ".join(entries))
    patches.append("*** End Patch")
    return "\n".join(patches)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", help="One audit report basename to apply in a bounded batch")
    print(render_patch(parser.parse_args().report))
