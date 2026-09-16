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


LABEL_TO_SLUG = {
    # Setting
    '室外': 'outdoor', '室內': 'indoor',
    # Nature
    '自然': 'nature', '自然生態': 'nature', '自然地標': 'nature', '生態': 'ecology',
    '生態保育': 'ecology', '生態廊道': 'ecology', '生態旅遊': 'ecology',
    '生態觀光': 'ecology', '生態觀察': 'ecology', '自然景觀': 'scenic',
    '海景': 'ocean-view', '地質': 'geology', '地質教育': 'geology', '地質景觀': 'geology',
    '海洋生態': 'marine-ecology', '海洋保育': 'marine-ecology',
    # Water/terrain
    '海灘': 'beach', '沙灘': 'beach', '海岸': 'coast', '北端海岸': 'coast',
    '珊瑚礁': 'coral-reef', '珊瑚礁地形': 'coral-reef', '珊瑚礁岩': 'coral-reef',
    '珊瑚礁島嶼': 'coral-reef', '珊瑚裙礁': 'coral-reef',
    '洞窟': 'cave', '海蝕洞': 'sea-cave',
    '紅樹林': 'mangrove', '離島': 'island', '燈塔': 'lighthouse',
    '漁港': 'fishing-port', '杉福漁港': 'fishing-port',
    '潮間帶': 'tidal-flat', '潮間帶生態': 'tidal-flat', '潮池生態': 'tidal-flat',
    '退潮': 'low-tide', '退潮景觀': 'low-tide',
    '礁石': 'reef-rock', '礁石地形': 'reef-rock', '礁石海岸': 'reef-rock',
    '礁岩地貌': 'reef-rock', '礁岩步道': 'reef-rock',
    '奇岩地貌': 'rock-formation', '奇石地景': 'rock-formation', '奇石景觀': 'rock-formation',
    '溶蝕溝': 'karst', '展望台': 'viewpoint', '景觀制高點': 'viewpoint', '制高點': 'viewpoint',
    '夜光藻': 'bioluminescence', '夜間觀察': 'night-activity', '夜觀生態': 'night-activity',
    # Wildlife
    '綠蠵龜': 'sea-turtle', '綠蠵龜棲地': 'sea-turtle', '海龜保育': 'sea-turtle',
    '海星': 'marine-life', '海膽': 'marine-life',
    # Culture/history
    '歷史': 'history', '歴史': 'history', '歷史古蹟': 'heritage', '歷史建築': 'heritage',
    '文化': 'culture', '在地生活': 'local-life', '慢活': 'local-life',
    '漁村文化': 'fishing-culture', '建築': 'architecture',
    '宗教': 'religion', '傳統信仰': 'religion', '文化信仰': 'religion',
    '王爺信仰': 'religion', '三山國王': 'religion', '廟宇': 'temple', '碧雲寺': 'temple',
    '宗教祭典': 'festival', '迎王平安祭典': 'festival', '三年一科': 'festival',
    '王船祭': 'festival', '遶境': 'festival',
    '傳說': 'legend', '傳說故事': 'legend', '歷史傳說': 'legend',
    '龍蝦傳說': 'legend', '地名故事': 'legend',
    '無形文化遺產': 'intangible-heritage',
    '荷蘭殖民': 'colonial-history', '日治時期': 'colonial-history',
    '原住民歷史': 'indigenous-history', '潮州移民': 'migration-history',
    # Experience/activity
    '體驗': 'experience', '体験': 'experience', '体驗': 'experience',
    '海洋體驗': 'ocean-experience',
    '步道': 'trail', '礁岩步道': 'trail', '海岸步道': 'trail', '木棧道': 'trail',
    '健行步道': 'hiking', '浮潛': 'snorkeling', '夜間浮潛': 'night-snorkeling',
    '水上活動': 'water-sports', '玻璃船': 'glass-boat',
    '親子': 'family', '親子旅遊': 'family',
    '打卡熱點': 'photogenic', '航海地標': 'maritime',
    # Food/market
    '美食': 'food', '小吃': 'street-food',
    '海鮮': 'seafood', '現撈': 'seafood', '石斑魚': 'seafood',
    '市場': 'market', '漁市': 'market', '老街': 'old-street', '購物': 'shopping',
    '購物街': 'shopping-street', '藝術': 'art',
    # Access
    '免費': 'free', '免費景點': 'free', '需購票': 'paid', '步行可達': 'walkable',
    '交通門戶': 'accessible',
    # Geographic (map to general)
    '小琉球': 'island', '琉球嶼': 'island', '屏東': 'nature', '屏東離島': 'island',
    '花瓶石周邊': 'scenic',
}

# Category each slug belongs to (for generate_pack_from_json new packs)
_SLUG_CATEGORY = {
    'outdoor': 'setting', 'indoor': 'setting',
    'nature': 'subject', 'ecology': 'subject', 'scenic': 'subject',
    'ocean-view': 'subject', 'geology': 'subject', 'marine-ecology': 'subject',
    'beach': 'subject', 'coast': 'subject', 'coral-reef': 'subject',
    'cave': 'subject', 'sea-cave': 'subject', 'mangrove': 'subject',
    'island': 'subject', 'lighthouse': 'subject', 'fishing-port': 'subject',
    'tidal-flat': 'subject', 'low-tide': 'subject', 'reef-rock': 'subject',
    'rock-formation': 'subject', 'karst': 'subject', 'viewpoint': 'experience',
    'bioluminescence': 'subject', 'night-activity': 'experience',
    'sea-turtle': 'subject', 'marine-life': 'subject',
    'history': 'subject', 'heritage': 'subject', 'culture': 'subject',
    'local-life': 'subject', 'fishing-culture': 'subject', 'architecture': 'subject',
    'religion': 'subject', 'temple': 'subject', 'festival': 'subject',
    'legend': 'subject', 'intangible-heritage': 'subject',
    'colonial-history': 'subject', 'indigenous-history': 'subject',
    'migration-history': 'subject',
    'experience': 'experience', 'ocean-experience': 'experience',
    'trail': 'experience', 'hiking': 'experience', 'snorkeling': 'experience',
    'night-snorkeling': 'experience', 'water-sports': 'experience',
    'glass-boat': 'experience', 'family': 'experience',
    'photogenic': 'experience', 'maritime': 'subject',
    'food': 'subject', 'street-food': 'subject', 'seafood': 'subject',
    'market': 'subject', 'old-street': 'subject', 'shopping': 'experience',
    'shopping-street': 'experience', 'art': 'subject',
    'free': 'access', 'paid': 'access', 'walkable': 'access', 'accessible': 'access',
}


def _label_to_slug(label: str) -> str:
    """Map a Chinese or other label to an ASCII slug."""
    if label in LABEL_TO_SLUG:
        return LABEL_TO_SLUG[label]
    # Fallback: keep only ASCII alnum + hyphen, lowercase
    slug = ''.join(c for c in label.lower() if c.isascii() and (c.isalnum() or c == '-'))
    return slug or 'unknown'


def rating_final(d: dict) -> float:
    import decimal as _decimal
    s  = d.get("significance", 3)
    di = d.get("distinctiveness", 3)
    i  = d.get("interpretability", 3)
    v  = d.get("visitorValue", 3)
    weights = {'significance': 0.30, 'distinctiveness': 0.25,
               'interpretability': 0.20, 'visitorValue': 0.15}
    total = sum(_decimal.Decimal(str(w)) * _decimal.Decimal(str(s_val))
                for (_, w), s_val in zip(weights.items(), [s, di, i, v]))
    total += _decimal.Decimal('0.10') * _decimal.Decimal('3')
    quantizer = _decimal.Decimal('0.1')
    return float(total.quantize(quantizer, rounding=_decimal.ROUND_HALF_UP))


def tag_groups_yaml(tags: list, indoor: bool) -> str:
    setting_slug = 'indoor' if indoor else 'outdoor'
    setting_label = '室內' if indoor else '室外'

    groups: dict[str, list[tuple[str, str]]] = {
        "setting": [(setting_slug, setting_label)],
        "subject": [], "experience": [], "access": [],
    }
    seen: dict[str, set[str]] = {k: {v[0] for v in vs} for k, vs in groups.items()}

    for t in tags:
        slug = _label_to_slug(t)
        cat = _SLUG_CATEGORY.get(slug, "subject")
        if slug not in seen[cat]:
            seen[cat].add(slug)
            groups[cat].append((slug, t))

    lines = []
    labels = {"setting": "場域", "subject": "主題",
              "experience": "體驗", "access": "入場"}
    for gid in ("setting", "subject", "experience", "access"):
        items = groups[gid]
        if not items:
            continue
        lines += [f"  - id: {gid}", f"    label: {labels[gid]}", "    tags:"]
        for slug, lbl in items:
            lines += [f"      - id: {slug}", f"        label: {lbl}"]
    return "\n".join(lines)


def safe(s) -> str:
    return str(s or "").replace('"', "'").replace("\n", " ").strip()


def write_point_yaml(d: dict, points_dir: Path) -> None:
    pid = d.get("id", "")
    if not pid:
        return

    lat = d.get("lat")
    lng = d.get("lng")
    if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)):
        raise ValueError(f"{pid}: explicit researched coordinates required; no 0,0 fallback")
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
        f'  locationHint: "{safe(d.get("locationHint",""))}"\n'
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
    pack_id    = first.get("packId")
    if not pack_id or not first.get("adminAreaLevel1"):
        raise ValueError("packId and adminAreaLevel1 are required; never create an unknown pack")
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
