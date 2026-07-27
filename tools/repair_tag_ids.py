"""
tools/repair_tag_ids.py — Fix Chinese tag IDs to ASCII slugs in source YAMLs.

Scans regions/jp/ishigaki/points/ and regions/tw/xiaoliuqiu/points/.
For each point YAML:
  - Maps tag id fields in tagGroups from Chinese labels to ASCII slugs
  - Deduplicates tags within each group (first mapping wins)
  - Rounds ratingEvidence.final to 1 decimal (round-half-up)

Updates files in-place, preserving all other formatting.

Usage:
    python tools/repair_tag_ids.py [--dry-run]
"""
from __future__ import annotations

import argparse
import decimal
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

LABEL_TO_SLUG: dict[str, str] = {
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
    '步道': 'trail', '海岸步道': 'trail', '木棧道': 'trail',
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
    # Geographic
    '小琉球': 'island', '琉球嶼': 'island', '屏東': 'nature', '屏東離島': 'island',
    '花瓶石周邊': 'scenic',
}

RATING_WEIGHTS = {
    'significance': decimal.Decimal('0.30'),
    'distinctiveness': decimal.Decimal('0.25'),
    'interpretability': decimal.Decimal('0.20'),
    'visitorValue': decimal.Decimal('0.15'),
    'evidenceQuality': decimal.Decimal('0.10'),
}

# Regex to match the tagGroups block (between "tagGroups:" and "indoor:")
TAGGROUPS_RE = re.compile(
    r'(?m)(^  tagGroups:\n)(.*?)(?=^  indoor:)',
    re.DOTALL | re.MULTILINE,
)

# Regex to match ratingEvidence.final line
FINAL_RE = re.compile(r'^(  final: )[\d.]+', re.MULTILINE)


def _label_to_slug(label: str) -> str:
    if label in LABEL_TO_SLUG:
        return LABEL_TO_SLUG[label]
    slug = ''.join(c for c in label.lower() if c.isascii() and (c.isalnum() or c == '-'))
    return slug or 'unknown'


def _round_half_up(value: float, decimals: int = 1) -> float:
    quantizer = decimal.Decimal(10) ** -decimals
    d = decimal.Decimal(str(round(value, decimals + 3)))
    return float(d.quantize(quantizer, rounding=decimal.ROUND_HALF_UP))


def _compute_final(re_data: dict) -> float:
    total = sum(
        RATING_WEIGHTS[dim] * decimal.Decimal(str(re_data.get(dim, {}).get('score', 0)))
        for dim in RATING_WEIGHTS
    )
    return _round_half_up(float(total), 1)


def _fix_tag_groups(tag_groups: list) -> list:
    """Return new tagGroups with ASCII slug IDs, deduplicated."""
    result = []
    for group in tag_groups:
        gid = group.get('id', '')
        glabel = group.get('label', gid)
        seen: set[str] = set()
        new_tags = []
        for tag in group.get('tags', []):
            old_id = str(tag.get('id', ''))
            new_id = _label_to_slug(old_id)
            if new_id not in seen:
                seen.add(new_id)
                new_tags.append({'id': new_id, 'label': tag.get('label', old_id)})
        if new_tags:
            result.append({'id': gid, 'label': glabel, 'tags': new_tags})
    return result


def _render_tag_groups(tag_groups: list) -> str:
    """Render tagGroups list as YAML text block (without the 'tagGroups:' header)."""
    lines = []
    for group in tag_groups:
        lines.append(f"  - id: {group['id']}")
        lines.append(f"    label: {group['label']}")
        lines.append(f"    tags:")
        for tag in group['tags']:
            lines.append(f"      - id: {tag['id']}")
            lines.append(f"        label: {tag['label']}")
    return '\n'.join(lines) + '\n'


def repair_file(path: Path, dry_run: bool = False) -> tuple[bool, list[str]]:
    """
    Repair a single point YAML file.
    Returns (changed, list_of_change_descriptions).
    """
    text = path.read_text(encoding='utf-8')
    data = yaml.safe_load(text)

    changes: list[str] = []
    new_text = text

    # --- Fix tagGroups ---
    point = data.get('point', {})
    tag_groups = point.get('tagGroups', [])
    new_tag_groups = _fix_tag_groups(tag_groups)

    # Check if anything changed in tags
    old_ids = [
        (g['id'], t['id'])
        for g in tag_groups
        for t in g.get('tags', [])
    ]
    new_ids = [
        (g['id'], t['id'])
        for g in new_tag_groups
        for t in g.get('tags', [])
    ]
    if old_ids != new_ids:
        changes.append(f"  tags: {old_ids} → {new_ids}")
        new_rendered = _render_tag_groups(new_tag_groups)

        def _replace_tag_groups(m: re.Match) -> str:
            return m.group(1) + new_rendered

        replaced = TAGGROUPS_RE.sub(_replace_tag_groups, new_text)
        if replaced == new_text:
            # Fallback if regex didn't match (shouldn't happen in well-formed files)
            changes.append("  WARNING: tagGroups regex did not match — skipping tag fix")
        else:
            new_text = replaced

    # --- Fix ratingEvidence.final ---
    re_data = data.get('ratingEvidence', {})
    declared_final = re_data.get('final')
    computed_final = _compute_final(re_data)

    if declared_final is not None and round(float(declared_final), 1) != computed_final:
        changes.append(f"  final: {declared_final} → {computed_final}")
        new_text = FINAL_RE.sub(lambda m: f"{m.group(1)}{computed_final}", new_text)
    elif declared_final is not None and float(declared_final) != computed_final:
        # Declared is already 1dp but differs from computed — update to match
        changes.append(f"  final: {declared_final} → {computed_final}")
        new_text = FINAL_RE.sub(lambda m: f"{m.group(1)}{computed_final}", new_text)

    changed = new_text != text
    if changed and not dry_run:
        path.write_text(new_text, encoding='utf-8')

    return changed, changes


def main() -> int:
    parser = argparse.ArgumentParser(description='Repair tag IDs and ratings in source YAMLs')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without writing')
    args = parser.parse_args()

    target_dirs = [
        REPO_ROOT / 'regions' / 'jp' / 'ishigaki' / 'points',
        REPO_ROOT / 'regions' / 'tw' / 'xiaoliuqiu' / 'points',
    ]

    total_files = 0
    changed_files = 0

    for points_dir in target_dirs:
        if not points_dir.exists():
            print(f'WARNING: {points_dir} does not exist', file=sys.stderr)
            continue
        yaml_files = sorted(points_dir.glob('*.yaml'))
        print(f'\n{points_dir} ({len(yaml_files)} files)')
        for path in yaml_files:
            total_files += 1
            changed, changes_desc = repair_file(path, dry_run=args.dry_run)
            if changed:
                changed_files += 1
                action = 'WOULD UPDATE' if args.dry_run else 'UPDATED'
                print(f'  {action}: {path.name}')
                for c in changes_desc:
                    print(c)
            else:
                print(f'  ok: {path.name}')

    mode = ' (dry run)' if args.dry_run else ''
    print(f'\n{changed_files}/{total_files} files updated{mode}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
