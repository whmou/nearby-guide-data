# nearby-guide-data

Data repository for the [NearbyGuide](https://github.com/whmou/nearby-guide) Android app.

- **App versionCode**: 8 (minimum required to read these packs)
- **Schema version**: 1
- **Content language**: zh-Hant-TW (Traditional Chinese, Taiwan)

## Repository structure

```
regions/           Source YAML files organized by country/region
  tw/hsinchu/      新竹市 (Hsinchu City, Taiwan)
  jp/miyako-jima/  宮古島 (Miyakojima, Okinawa, Japan)
schemas/           JSON Schema definitions for all file formats
taxonomy/          Shared tag and kind definitions
tools/             Build and validation scripts
tests/             Pytest test suite
dist/              Build output (.guidepack archives) — not committed
catalog.json       Published pack index (updated by tools/update_catalog.py)
```

## Packs

| Pack ID         | Title  | Points | Status |
|-----------------|--------|--------|--------|
| tw-hsinchu      | 新竹市 | 7      | draft  |
| jp-miyakojima   | 宮古島 | 7      | draft  |

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

# Validate all source files
python tools/validate.py --all

# Build all packs
python tools/build_packs.py --all --output dist

# Run tests
pytest -v
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for authoring guidelines, rating rubric usage,
and the pull-request workflow.

## Licenses

- Data (`regions/`, `taxonomy/`, `catalog.json`, `schemas/`): **CC-BY-4.0** — see [DATA_LICENSE.md](DATA_LICENSE.md)
- Tools (`tools/`, `tests/`, `.github/`): **MIT** — see [LICENSE](LICENSE)
- Media: individually licensed per item — see [MEDIA_LICENSES.md](MEDIA_LICENSES.md)
