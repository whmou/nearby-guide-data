"""Reduce private browser observations to factual map evidence (no reviews/photos).

This does NOT select candidates or alter coordinates. A search can return a
different attraction or even a different island. Review all matches manually.
"""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote
import yaml
from location_contract import distance_m

ROOT = Path(__file__).resolve().parents[1]


def explicit_pin(url):
    matches = re.findall(r'!3d(-?[\d.]+)!4d(-?[\d.]+)', unquote(url or ''))
    if len(matches) != 1:
        return None
    return {'latitude': float(matches[0][0]), 'longitude': float(matches[0][1])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    sources = {s['point']['id']: s for s in (yaml.safe_load(p.read_text(encoding='utf-8')) for p in
               (ROOT / 'regions/jp/miyako-jima/points').glob('*.yaml'))}
    results = []
    for observation in json.loads(args.input.read_text(encoding='utf-8')):
        point_id = observation['id']
        candidates = []
        url = next((url for url in (observation.get('resolvedShareUrl'), observation.get('url'))
                    if explicit_pin(url)), '')
        if explicit_pin(url):
            candidates.append({'name':(observation.get('headings') or [''])[0], 'url':url.split('?')[0],
                               'pin':explicit_pin(url), 'kind':'opened_named_place'})
        for link in observation.get('placeLinks', []):
            if explicit_pin(link['href']):
                candidates.append({'name':link['text'], 'url':link['href'].split('?')[0],
                                   'pin':explicit_pin(link['href']), 'kind':'search_candidate_only'})
        source_loc = sources.get(point_id, {}).get('point', {}).get('location')
        for candidate in candidates:
            candidate['distanceToAdoptedAnchorMeters'] = round(distance_m(source_loc, candidate['pin'])) if source_loc else None
        results.append({'id':point_id, 'query':observation['query'], 'checkedAt':observation['checkedAt'],
                        'pageTitle':observation.get('title'), 'httpStatus':observation.get('httpStatus'),
                        'blocked':observation.get('blocked', False), 'adoptedLocation':source_loc,
                        'candidates':candidates,
                        'note':'Google named pins, not map viewport centres. Search candidates are not identity verification; no automatic adoption.'})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'Exported {len(results)} browser observations; no coordinates changed.')


if __name__ == '__main__':
    main()
