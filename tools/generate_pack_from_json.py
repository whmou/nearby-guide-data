"""
tools/generate_pack_from_json.py — Generate pack YAML files from a research JSON file.

Usage:
    python tools/generate_pack_from_json.py <json_file>

The JSON file should be an array of point objects with fields matching
the NearbyGuide source YAML schema (id, title, summary, narration,
observationPrompt, lat, lng, locationHint, tags, indoor, triggerRadiusM,
mediaUrl, mediaCreator, mediaLicense, mediaLicenseUrl, mediaDescription,
significance, distinctiveness, interpretability, visitorValue,
sourceTitle, sourceUrl, admissionFree, admissionNote,
packId, packTitle, packSubtitle, countryCode, adminAreaLevel1,
adminAreaLevel2, hierarchy).
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def rating_final(d: dict) -> float:
    s  = d.get("significance", 3)
    di = d.get("distinctiveness", 3)
    i  = d.get("interpretability", 3)
    v  = d.get("visitorValue", 3)
    return round(0.30*s + 0.25*di + 0.20*i + 0.15*v + 0.10*3, 2)


def tag_groups_yaml(tags: list, indoor: bool) -> str:
    tag_map = {
        "海灘": "subject", "自然": "subject", "歷史": "subject",
        "文化": "subject", "建築": "subject", "宗教": "subject",
        "藝術": "subject", "美食": "experience", "購物": "experience",
        "體驗": "experience", "展望台": "subject", "珊瑚礁": "subject",
        "紅樹林": "subject", "洞窟": "subject", "離島": "subject",
        "免費": "access", "潛水": "experience", "浮潛": "experience",
        "海龜": "subject", "夜間": "experience", "玻璃船": "experience",
        "潮間帶": "subject", "燈塔": "subject", "漁港": "subject",
        "老街": "subject", "寺廟": "subject", "市場": "experience",
    }
    groups: dict[str, list[str]] = {
        "setting": ["室內" if indoor else "室外"],
        "subject": [], "experience": [], "access": [],
    }
    for t in tags:
        cat = tag_map.get(t, "subject")
        if t not in groups[cat]:
            groups[cat].append(t)

    lines = []
    labels = {"setting": "場域", "subject": "主題",
              "experience": "體驗", "access": "入場"}
    for gid in ("setting", "subject", "experience", "access"):
        items = groups[gid]
        if not items:
            continue
        lines += [f"  - id: {gid}", f"    label: {labels[gid]}", "    tags:"]
        for item in items:
            lines += [f"      - id: {item}", f"        label: {item}"]
    return "\n".join(lines)


def safe(s) -> str:
    return str(s or "").replace('"', "'").replace("\n", " ").strip()


def write_point_yaml(d: dict, points_dir: Path) -> None:
    pid = d.get("id", "")
    if not pid:
        return

    lat = d.get("lat") or 0.0
    lng = d.get("lng") or 0.0
    indoor = bool(d.get("indoor", False))
    final = rating_final(d)
    radius = float(d.get("triggerRadiusM") or 150)
    admission_free = bool(d.get("admissionFree", True))
    admission_label = "免費" if admission_free else safe(d.get("admissionNote", "需購票"))

    narration_raw = (d.get("narration") or "").strip()
    narration_lines = "\n".join(f"    {line}" for line in narration_raw.split("\n"))

    pack_id      = d.get("packId", "")
    country_code = d.get("countryCode", "TW")
    level1       = d.get("adminAreaLevel1", "")
    level2       = d.get("adminAreaLevel2", "")
    hierarchy    = d.get("hierarchy", ["台灣"])
    hierarchy_yaml = json.dumps(hierarchy, ensure_ascii=False)

    media_url        = d.get("mediaUrl", "")
    media_license_url = d.get("mediaLicenseUrl", "https://creativecommons.org/licenses/by-sa/4.0")

    src_url = d.get("sourceUrl", "")

    tg = tag_groups_yaml(d.get("tags") or [], indoor)

    compact_p = f"media/compact/{pid}.webp"
    complete_p = f"media/complete/{pid}.webp"

    level2_line = f"  adminAreaLevel2: {level2}\n" if level2 else ""

    yaml_content = (
        f"schemaVersion: 1\n"
        f"point:\n"
        f"  id: {pid}\n"
        f"  parentId: null\n"
        f"  kind: venue\n"
        f'  title: "{safe(d.get("title",""))}"\n'
        f'  summary: "{safe(d.get("summary",""))}"\n'
        f"  narration: |\n"
        f"{narration_lines}\n"
        f'  observationPrompt: "{safe(d.get("observationPrompt",""))}"\n'
        f"  countryCode: {country_code}\n"
        f"  adminAreaLevel1: {level1}\n"
        f"{level2_line}"
        f"  hierarchy: {hierarchy_yaml}\n"
        f"  tagGroups:\n"
        f"{tg}\n"
        f'  indoor: {"true" if indoor else "false"}\n'
        f"  location:\n"
        f"    latitude: {lat}\n"
        f"    longitude: {lng}\n"
        f'    locationHint: "{safe(d.get("locationHint",""))}"\n'
        f'  googleMapsUrl: "https://maps.google.com/maps?q={lat},{lng}"\n'
        f"  trigger:\n"
        f"    radiusMeters: {radius:.1f}\n"
        f"    dwellMillis: 2000\n"
        f"    rearmDistanceMeters: 800.0\n"
        f"ratingEvidence:\n"
        f"  rubricVersion: 1\n"
        f"  significance:\n"
        f"    score: {d.get('significance',3)}\n"
        f'    note: "{safe(d.get("significanceNote",""))}"\n'
        f"    sources: [{pid}-source]\n"
        f"  distinctiveness:\n"
        f"    score: {d.get('distinctiveness',3)}\n"
        f'    note: "{safe(d.get("distinctivenessNote",""))}"\n'
        f"    sources: [{pid}-source]\n"
        f"  interpretability:\n"
        f"    score: {d.get('interpretability',3)}\n"
        f'    note: "{safe(d.get("interpretabilityNote",""))}"\n'
        f"    sources: [{pid}-source]\n"
        f"  visitorValue:\n"
        f"    score: {d.get('visitorValue',3)}\n"
        f'    note: "{safe(d.get("visitorValueNote",""))}"\n'
        f"    sources: [{pid}-source]\n"
        f"  evidenceQuality:\n"
        f"    score: 3\n"
        f"    note: \"網路資料為主\"\n"
        f"    sources: [{pid}-source]\n"
        f"  final: {final}\n"
        f"sources:\n"
        f"  - id: {pid}-source\n"
        f'    title: "{safe(d.get("sourceTitle",""))}"\n'
        f"    publisher: \"\"\n"
        f"    url: {src_url}\n"
        f"    accessedAt: \"2026-07-26\"\n"
        f"    language: zh-TW\n"
        f"    supports:\n"
        f"      - \"座標與景點基本資訊\"\n"
        f"media:\n"
        f"  - id: primary-image\n"
        f"    type: image\n"
        f"    sourceUrl: {media_url}\n"
        f'    creator: "{safe(d.get("mediaCreator",""))}"\n'
        f'    license: "{d.get("mediaLicense","CC BY-SA 4.0")}"\n'
        f"    licenseUrl: {media_license_url}\n"
        f"    accessedAt: \"2026-07-26\"\n"
        f"    originalSha256: \"\"\n"
        f"    compactPath: {compact_p}\n"
        f"    completePath: {complete_p}\n"
        f"admissions:\n"
        f'  - label: "{admission_label}"\n'
        f'    isFree: {"true" if admission_free else "false"}\n'
        f"review:\n"
        f"  status: draft\n"
        f"  checkedAt: \"2026-07-26\"\n"
        f"  notes: []\n"
    )

    (points_dir / f"{pid}.yaml").write_text(yaml_content, encoding="utf-8")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python generate_pack_from_json.py <data.json>")
        sys.exit(1)

    data_path = Path(sys.argv[1])
    data: list[dict] = json.loads(data_path.read_text(encoding="utf-8"))

    if not data:
        print("ERROR: empty data")
        sys.exit(1)

    # Infer pack info from first point
    first = data[0]
    pack_id    = first.get("packId", "unknown")
    pack_title = first.get("packTitle", pack_id)
    subtitle   = first.get("packSubtitle", "")
    country    = first.get("countryCode", "TW")
    level1     = first.get("adminAreaLevel1", "")
    level2     = first.get("adminAreaLevel2", "")
    country_name = "台灣" if country == "TW" else "日本"
    lang       = "zh-Hant-TW"

    pack_dir   = REPO_ROOT / "regions" / country.lower() / pack_id.split("-", 1)[-1]
    points_dir = pack_dir / "points"
    points_dir.mkdir(parents=True, exist_ok=True)

    # Write pack.yaml
    level2_line = f"  adminAreaLevel2: {level2}\n" if level2 else ""
    pack_yaml = (
        f"schemaVersion: 1\n"
        f"packId: {pack_id}\n"
        f'version: "1.0.0"\n'
        f'title: "{pack_title}"\n'
        f'subtitle: "{subtitle}"\n'
        f"region:\n"
        f"  countryCode: {country}\n"
        f"  countryName: {country_name}\n"
        f"  adminAreaLevel1: {level1}\n"
        f"{level2_line}"
        f"contentLanguage: {lang}\n"
        f"minAppVersionCode: 8\n"
        f'createdAt: "2026-07-26T00:00:00Z"\n'
    )
    (pack_dir / "pack.yaml").write_text(pack_yaml, encoding="utf-8")
    print(f"Wrote pack.yaml for {pack_id}")

    count = 0
    for d in data:
        write_point_yaml(d, points_dir)
        count += 1
        print(f"  [{count}/{len(data)}] {d.get('id','?')}")

    print(f"\nDone: {count} point YAML files in {points_dir}")


if __name__ == "__main__":
    main()
