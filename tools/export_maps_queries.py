"""Prepare read-only browser queries from current authored names, never coordinates."""
import argparse
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    rows = []
    for path in sorted((ROOT / 'regions/jp/miyako-jima/points').glob('*.yaml')):
        source = yaml.safe_load(path.read_text(encoding='utf-8'))
        p = source['point']
        if source['locationReview']['status'] != 'verified':
            continue
        primary = next((s for s in source.get('sources', []) if 'miyakojimabunkazai.jp/bunkazaiinfo' in s['url']), None)
        name = re.sub(r'【[^】]*】', '', primary['title']).split('～')[0].strip() if primary else p['title']
        rows.append({'id':p['id'], 'title':p['title'], 'query':name+' 宮古島', 'location':p['location']})
    args.output.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Prepared {len(rows)} named queries, no data changed.')


if __name__ == '__main__':
    main()
