"""Seal an explicitly reviewed batch; not a substitute for checking sources.

Run only AFTER editorial/location review, e.g.:
python tools/seal_review.py --region jp/miyako-jima
"""
import argparse
import json
from pathlib import Path
import yaml
from audit_contract import ROOT, content_digest, load_batch, review_errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--region', required=True)
    args = parser.parse_args()
    directory = (ROOT / 'regions' / args.region).resolve()
    if not directory.is_relative_to((ROOT / 'regions').resolve()):
        parser.error('region must stay inside regions/')
    pack = yaml.safe_load((directory / 'pack.yaml').read_text(encoding='utf-8'))
    batch = pack['reviewBatch']
    entries = load_batch(batch)
    digests = {}
    for path in sorted((directory / 'points').glob('*.yaml')):
        source = yaml.safe_load(path.read_text(encoding='utf-8'))
        point_id = source['point']['id']
        errors = review_errors(source, entries[point_id])
        if errors:
            raise ValueError(f'{point_id}: ' + '; '.join(errors))
        digests[point_id] = content_digest(source)
    if set(digests) != set(entries):
        raise ValueError('Source/review coverage mismatch')
    output = {'batch': batch, 'note': 'Editorial snapshot, NOT proof of factual correctness or a field test.',
              'sha256': digests, 'reviewSha256': {key: content_digest(entries[key]) for key in sorted(entries)}}
    target = ROOT / 'audits' / batch / 'seals.json'
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'Sealed {len(digests)} explicitly reviewed records: {target}')


if __name__ == '__main__':
    main()
