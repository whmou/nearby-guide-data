# nearby-guide-data

Data repository for the [NearbyGuide](https://github.com/whmou/nearby-guide) Android app.

- **App versionCode**: 8 (minimum required to read these packs)
- **Schema version**: 1
- **Content language**: zh-Hant-TW (Traditional Chinese, Taiwan)

## Repository structure

```
regions/           Source YAML files organized by country/region
  tw/hsinchu/      新竹市 (Hsinchu City, Taiwan)
  tw/xiaoliuqiu/   小琉球 (Liuqiu Township, Taiwan)
  jp/miyako-jima/  宮古島 (Miyakojima, Okinawa, Japan)
  jp/ishigaki/     石垣島與八重山 (Ishigaki/Yaeyama, Okinawa)
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
| tw-hsinchu      | 新竹市 | 35     | See location review |
| jp-miyakojima   | 宮古島 | 108    | v1.1.0: 72 located / 36 text-only |
| jp-ishigaki     | 石垣島與八重山 | 30 | See location review |
| tw-xiaoliuqiu   | 小琉球 | 22     | See location review |

Counts include text-only themes and unresolved entries, not only GPS attractions.
The [location review rules](LOCATION_REVIEW.md) and per-point `locationReview`
record evidence, anchor meaning, and original coordinates. Unresolved/non-point
entries do not supply GPS triggers or navigation links. Coordinate review does
not certify old narratives, ratings, photos, opening times, or safe access.

宮古島 **2026-09-23～27 旅行版**：重查原有 71 筆並新增 37 筆，共 108 篇內容；
其中 72 筆有定位，23 筆為背景主題，13 筆仍待確認而停用導航。不是「108 個已確認可到訪景點」。
這次以實際 Google Maps 具名頁、官方圖釘及逐項故事來源核對，另做獨立定位／敘事抽查。
42 筆錯配或無法支持地點的舊媒體紀錄已撤下，新點不借用別處照片；目前 29 筆保留既有圖片，未重新認證其授權。
見 [五組區域選點與旅期提醒](MIYAKO_TRIP_2026-09.md) 及 [查核紀錄](audits/miyako-trip-2026-09-23/)。

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
