"""Versioned source reviews. A generated Maps URL is not proof of a Google listing."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_review_layers(root: Path = ROOT) -> dict[str, dict]:
    """Explicit layers preserve old investigations and reject duplicate ownership."""
    index = json.loads((root / 'audits/index.json').read_text(encoding='utf-8'))
    latest = {}
    for layer in index['layers']:
        owned = set()
        for rel in layer['files']:
            for row in json.loads((root / 'audits' / rel).read_text(encoding='utf-8-sig')):
                if row['id'] in owned:
                    raise ValueError(f"Duplicate review ownership in {layer['name']}: {row['id']}")
                owned.add(row['id'])
                latest[row['id']] = row
    return latest


def load_batch(batch: str, root: Path = ROOT) -> dict[str, dict]:
    index = json.loads((root / 'audits/index.json').read_text(encoding='utf-8'))
    layers = [layer for layer in index['layers'] if layer['name'] == batch]
    if len(layers) != 1:
        raise ValueError(f'Unknown/duplicate review batch: {batch}')
    records = {}
    for rel in layers[0]['files']:
        for entry in json.loads((root / 'audits' / rel).read_text(encoding='utf-8-sig')):
            if entry['id'] in records:
                raise ValueError(f"Duplicate reviewed point: {entry['id']}")
            records[entry['id']] = entry
    return records


def content_digest(source: dict) -> str:
    """Any later story, coordinate, media or evidence edit invalidates the seal."""
    serialized = json.dumps(source, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()


def review_errors(source: dict, entry: dict) -> list[str]:
    errors = []
    point, review = source['point'], source['locationReview']
    if entry.get('id') != point['id'] or entry.get('title') != point['title']:
        errors.append('review identity/title does not match source')
    for field in ('status', 'anchorType', 'reason', 'sources', 'checkedAt'):
        if entry.get(field) != review.get(field):
            errors.append(f'review {field} does not match source')
    if review['status'] == 'verified':
        if point['location'] != {'latitude': entry.get('latitude'), 'longitude': entry.get('longitude')}:
            errors.append('review coordinates do not match source')
        if entry.get('locationHint') != point.get('locationHint'):
            errors.append('review arrival instructions do not match source')
    evidence = entry.get('googleMapsVerification', {})
    if evidence.get('method') not in {'named_listing', 'official_embedded_pin', 'unavailable'} or not evidence.get('result'):
        errors.append('Google Maps verification method/result must be explicit')
    if evidence.get('method') != 'unavailable':
        if not (evidence.get('originalUrl') or '').startswith('https://'):
            errors.append('Google Maps verification must preserve its original link')
    claims = entry.get('storyClaims', [])
    if review['status'] == 'verified' and len(claims) < 2:
        errors.append('verified attraction needs at least two sourced story facts')
    source_urls = {s['url'] for s in source.get('sources', [])}
    source_ids = [s['id'] for s in source.get('sources', [])]
    if len(set(source_ids)) != len(source_ids):
        errors.append('duplicate source IDs in reviewed story')
    for dimension in ('significance', 'distinctiveness', 'interpretability', 'visitorValue', 'evidenceQuality'):
        for reference in source.get('ratingEvidence', {}).get(dimension, {}).get('sources', []):
            if reference not in source_ids:
                errors.append('rating references an absent source ID')
    for claim in claims:
        if not claim.get('claim') or claim.get('sourceUrl') not in source_urls:
            errors.append('story fact must refer to a declared source page')
    return errors


def sealed_batch(batch: str, sources: list[dict], root: Path = ROOT) -> dict[str, dict]:
    records = load_batch(batch, root)
    seals = json.loads((root / 'audits' / batch / 'seals.json').read_text(encoding='utf-8'))
    ids = {source['point']['id'] for source in sources}
    if (ids != set(records) or ids != set(seals['sha256'])
            or ids != set(seals.get('reviewSha256', {}))):
        raise ValueError('review/source/seal coverage mismatch; every published point needs review')
    for source in sources:
        point_id = source['point']['id']
        problems = review_errors(source, records[point_id])
        if seals['sha256'][point_id] != content_digest(source):
            problems.append('source changed since reviewed snapshot; re-review before sealing')
        if seals['reviewSha256'][point_id] != content_digest(records[point_id]):
            problems.append('evidence changed since reviewed snapshot; re-review before sealing')
        if problems:
            raise ValueError(f'{point_id}: ' + '; '.join(problems))
    return records
