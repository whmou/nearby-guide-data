# Contributing to nearby-guide-data

Thank you for contributing! This document covers how to add or edit points, run
validation, and submit a pull request.

## Prerequisites

- Python 3.12+
- `pip install -r requirements-dev.txt`

## Adding a new point

1. Choose an existing region directory or create a new one under `regions/`.
2. Create a new YAML file: `regions/<country>/<region>/points/<id>.yaml`.
   - **ID format**: `<country>-<region>-<stable-slug>`, e.g. `tw-hsinchu-east-gate`
   - IDs are **immutable** after publication; choose carefully.
3. Fill in all required fields per `schemas/source-point-v1.schema.json`.
4. Rate the point using the rubric in [RATING_RUBRIC.md](RATING_RUBRIC.md).
   - Calculate `final` manually and verify with `tools/validate.py`.
5. Find CC0 or CC-BY/CC-BY-SA media that actually depicts this named place.
   - A licence and successful download do not prove the subject is correct.
   - Do not substitute a different island, shrine, shop, or generic island photo.
   - Use `media: []` while a matching image or its permission remains unverified.
   - `originalSha256` must contain the downloaded original's actual hash before publication.
6. Set `review.status: draft`.
7. Run `python tools/validate.py --all` — zero errors required before opening a PR.
8. Run `pytest -v` — all tests must pass.

## Narration guidelines

- Write in 繁體中文 (Traditional Chinese, Taiwan usage).
- Do **not** begin with "你來到…" or "歡迎來到…".
- Write natural, spoken-aloud prose. For the Miyako travel edition, aim for a
  short listen of roughly 220–420 Chinese characters, not an encyclopedia entry.
- Include at least one concrete observable detail the visitor can look for.
- The `observationPrompt` should ask about something **physically visible** at the site.
- Vary openings; do not make every guide start with the same instruction.
- Give a specific sourced local history, person, daily-life detail or natural
  process. Label legends as legends; do not invent quotations or sensory scenes.
- A Google Maps pin establishes neither opening hours nor safe public access.
  Match the named site/address and distinguish visitor access from a centre or
  underwater feature. Record current closure notices with their check date.
- Do not promise wildlife sightings, passing aircraft or activities without a
  confirmed operator. A general activity is a text-only theme, not another POI.

## Rating rubric summary

See [RATING_RUBRIC.md](RATING_RUBRIC.md) for full rubric.

```
final = round(0.30×sig + 0.25×dist + 0.20×interp + 0.15×visitor + 0.10×evidence, 1dp)
```

Rounding: half-up (3.85 → 3.9, not 3.8).

## Validation rules

`tools/validate.py --all` enforces:

- All YAML files validate against the JSON schemas.
- Point IDs are globally unique.
- Parent references form a DAG (no cycles).
- `ratingEvidence.final` matches the computed weighted sum (±0.05 tolerance).
- All tag IDs exist in `taxonomy/tags.yaml`.
- Sources have non-empty `title`, `url`, `accessedAt`, and at least one `supports` entry.
- No placeholder text (`TODO`, `TBD`, `PLACEHOLDER`, `...`) in title/summary/narration.
- Coordinates in valid ranges (lat −90..90, lon −180..180).
- If `indoor: true`, then `locationHint` must not be null.
- Android also requires a nonblank `locationHint` whenever `location` is absent
  and `kind` (case-insensitive) is `zone`, `artwork`, `exhibit`, or `view`, even
  when the source says `indoor: false`. The runtime format has no `indoor` flag.
  For unresolved/text-only entries, describe the limitation; never invent GPS
  coordinates or change the kind just to bypass this rule. Source validation,
  the builder, archive inspection and public-download verification all enforce it.

## Pull request checklist

- [ ] `python tools/validate.py --all` passes with zero errors
- [ ] `pytest -v` passes
- [ ] Narration reviewed for natural speech quality
- [ ] Rating documented with per-dimension notes and source citations
- [ ] `review.status: draft` on all new points
- [ ] No personal data, no copyrighted text, no trademarked logos as primary images

## File naming

| Type          | Convention                          | Example                             |
|---------------|-------------------------------------|-------------------------------------|
| Point YAML    | `<point-id>.yaml`                   | `tw-hsinchu-east-gate.yaml`         |
| Pack YAML     | `pack.yaml`                         | `regions/tw/hsinchu/pack.yaml`      |
| Media source  | `media/source.yaml`                 | `regions/tw/hsinchu/media/source.yaml` |
# Coordinate evidence is a publication requirement

Read [LOCATION_REVIEW.md](LOCATION_REVIEW.md) before adding or changing any point.
Every production point needs an evidence-backed location review, or an explicit
unresolved/non-point status with no GPS/trigger/navigation link. Search results
are candidates, not proof. Never reuse a region centre or generic experience as
a precise attraction. Changing reviewed coordinates invalidates that review.
