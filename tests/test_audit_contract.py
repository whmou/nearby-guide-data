import json
import sys
from pathlib import Path
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from audit_contract import content_digest, load_review_layers, review_errors, sealed_batch
from summarize_browser_maps import explicit_pin


def test_google_viewport_not_a_landmark_coordinate():
    assert explicit_pin('https://www.google.com/maps/@24.8,125.2,15z') is None
    assert explicit_pin('https://www.google.com/maps/search/name/@24.8,125.2,15z') is None
    assert explicit_pin('https://www.google.com/maps/place/site/@24.7,125.1,17z/data=!3d24.8!4d125.2') == {'latitude':24.8,'longitude':125.2}
    assert explicit_pin('https://www.google.com/maps/data=!3d24.8!4d125.2!3d24.7!4d125.1') is None


def sample():
    url = 'https://example.org/named-place'
    source = {'point': {'id':'example', 'title':'Named place', 'narration':'Original narrative',
                       'summary':'Summary', 'locationHint':'Public landmark',
                       'location':{'latitude':24.8,'longitude':125.2}},
              'sources':[{'id':'s1','url':url}],
              'locationReview': {'status':'verified','anchorType':'landmark','reason':'Fetched exact pin',
                                 'checkedAt':'2026-09-16','sources':[{'url':url,'title':'Official place','coordinateEvidence':'Explicit pin'}]}}
    entry = {'id':'example','title':'Named place','latitude':24.8,'longitude':125.2,
             'locationHint':'Public landmark', **source['locationReview'],
             'googleMapsVerification': {'method':'official_embedded_pin','originalUrl':'https://www.google.com/maps?q=24.8,125.2',
                                       'result':'Official named page explicitly links a numeric destination; no street-view inspection'},
             'storyClaims':[{'claim':'First sourced fact','sourceUrl':url},{'claim':'Second sourced fact','sourceUrl':url}]}
    return source, entry


def test_explicit_maps_method_not_a_generated_link_claim():
    source, entry = sample()
    assert not review_errors(source, entry)
    entry['googleMapsVerification'] = {'method':'generated_query','originalUrl':'https://www.google.com/maps?q=24.8,125.2'}
    assert review_errors(source, entry)


def test_narrative_claim_requires_declared_source():
    source, entry = sample()
    entry['storyClaims'][0]['sourceUrl'] = 'https://example.org/not-read'
    assert 'story fact must refer to a declared source page' in review_errors(source, entry)


def test_rating_reference_cannot_survive_deleted_source():
    source, entry = sample()
    source['ratingEvidence'] = {'significance':{'sources':['removed-source']}}
    assert 'rating references an absent source ID' in review_errors(source, entry)


def test_changed_story_or_coordinate_invalidates_digest():
    source, _ = sample()
    before = content_digest(source)
    source['point']['narration'] += ' A new unsupported claim.'
    assert content_digest(source) != before
    source['point']['location']['latitude'] = 24.9
    assert content_digest(source) != before


def test_review_pin_must_match_source():
    source, entry = sample()
    entry['latitude'] = 25
    assert 'review coordinates do not match source' in review_errors(source, entry)


def test_reviewed_story_and_maps_evidence_embedded_in_archive(tmp_path):
    from build_packs import build_pack
    import zipfile
    directory = ROOT / 'regions/jp/miyako-jima'
    pack = yaml.safe_load((directory / 'pack.yaml').read_text(encoding='utf-8'))
    sources = [yaml.safe_load(p.read_text(encoding='utf-8')) for p in sorted((directory / 'points').glob('*.yaml'))]
    entries = sealed_batch(pack['reviewBatch'], sources)
    build_pack(directory, tmp_path, verbose=False)
    for path in (tmp_path / 'packs').glob('*.guidepack'):
        with zipfile.ZipFile(path) as archive:
            points = json.loads(archive.read('points.json'))['points']
            referenced = set()
            for point in points:
                assert point['extensions']['nearbyGuide.storyClaims'] == entries[point['id']]['storyClaims']
                assert point['extensions']['nearbyGuide.googleMapsVerification'] == entries[point['id']]['googleMapsVerification']
                assert point['contentSourceUrl']
                referenced.update(m['path'] for m in point['media'])
            assert set(archive.namelist()) == referenced | {'points.json', 'manifest.json'}, 'Withdrawn/wrong photos must not remain packaged'


def test_layer_rejects_duplicate_ownership(tmp_path):
    folder = tmp_path / 'audits'
    folder.mkdir()
    (folder / 'index.json').write_text(json.dumps({'layers':[{'name':'batch','files':['a.json','b.json']}]}),encoding='utf-8')
    for name in ('a.json','b.json'):
        (folder / name).write_text(json.dumps([{'id':'same-point'}]),encoding='utf-8')
    with pytest.raises(ValueError, match='Duplicate review ownership'):
        load_review_layers(tmp_path)


@pytest.mark.parametrize('change', ['narration', 'evidence', 'coverage'])
def test_sealed_batch_rejects_unreviewed_changes(tmp_path, change):
    source, entry = sample()
    folder = tmp_path / 'audits' / 'batch'
    folder.mkdir(parents=True)
    (folder.parent / 'index.json').write_text(json.dumps({'layers':[
        {'name':'batch', 'files':['batch/review.json']}]}), encoding='utf-8')
    review_file = folder / 'review.json'
    review_file.write_text(json.dumps([entry]), encoding='utf-8')
    (folder / 'seals.json').write_text(json.dumps({
        'sha256':{'example':content_digest(source)},
        'reviewSha256':{'example':content_digest(entry)}}), encoding='utf-8')
    assert sealed_batch('batch', [source], tmp_path)['example'] == entry
    if change == 'narration':
        source['point']['narration'] += ' An unchecked story.'
    elif change == 'evidence':
        entry['googleMapsVerification']['result'] = 'Changed verification claim.'
        review_file.write_text(json.dumps([entry]), encoding='utf-8')
    else:
        review_file.write_text('[]', encoding='utf-8')
    with pytest.raises(ValueError, match='changed since reviewed|coverage mismatch'):
        sealed_batch('batch', [source], tmp_path)
