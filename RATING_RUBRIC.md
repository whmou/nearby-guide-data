# Rating Rubric

Version: 1

Every point in this repository carries a `ratingEvidence` block. Scores are integers
0–5 on five dimensions. The weighted final score is stored in `ratingEvidence.final`.

## Dimensions

### Significance (weight 0.30)
Cultural, historical, natural, or artistic importance of the place.

| Score | Meaning |
|-------|---------|
| 5 | World-class or nationally iconic; widely studied/cited |
| 4 | Regionally significant; referenced in authoritative sources |
| 3 | Locally notable; known to most residents |
| 2 | Mildly interesting; limited documented importance |
| 1 | Marginal significance |
| 0 | No documented significance |

### Distinctiveness (weight 0.25)
How unique or irreplaceable the on-site experience is — what you can only get here.

| Score | Meaning |
|-------|---------|
| 5 | Singular experience; cannot be replicated anywhere else |
| 4 | Highly distinctive; very few comparable sites globally |
| 3 | Notable but similar experiences exist elsewhere in region |
| 2 | Generic; many equivalent sites |
| 1 | Nearly interchangeable with other sites |
| 0 | No distinguishing characteristic |

### Interpretability (weight 0.20)
How readily a visitor can observe and make sense of visible or discoverable details
without specialized knowledge.

| Score | Meaning |
|-------|---------|
| 5 | Richly legible; details self-evident or very well signed |
| 4 | Most key features clearly visible and interpretable |
| 3 | Core features visible; some require context |
| 2 | Limited visible evidence; mostly conceptual |
| 1 | Very little to observe; requires deep expertise |
| 0 | Nothing meaningfully observable on-site |

### Visitor Value (weight 0.15)
Practical accessibility and reliability of experience: hours, cost, safety, transit.

| Score | Meaning |
|-------|---------|
| 5 | Always open, free, safe, easily reached |
| 4 | Reliable access, low or no cost, good transit |
| 3 | Reasonable hours, modest cost, adequate transit |
| 2 | Limited hours, higher cost, or difficult access |
| 1 | Rarely accessible or significant barriers |
| 0 | Currently inaccessible |

### Evidence Quality (weight 0.10)
Confidence in the stated facts based on source type and number.

| Score | Meaning |
|-------|---------|
| 5 | Multiple independent official/academic sources |
| 4 | Official source(s) plus secondary corroboration |
| 3 | Single credible official source |
| 2 | Reputable secondary source only |
| 1 | Community-sourced or anecdotal only |
| 0 | Unverifiable |

## Formula

```
final = round(0.30 × significance + 0.25 × distinctiveness
            + 0.20 × interpretability + 0.15 × visitorValue
            + 0.10 × evidenceQuality,
            1 decimal place)
```

Rounding uses standard half-up: 0.05 → 0.1.

### Example

```
significance=4, distinctiveness=4, interpretability=3, visitorValue=4, evidenceQuality=4
= 0.30×4 + 0.25×4 + 0.20×3 + 0.15×4 + 0.10×4
= 1.20  + 1.00  + 0.60  + 0.60  + 0.40
= 3.80  → final: 3.8
```

## Validation

`tools/validate.py` recomputes `final` from the five dimension scores and rejects any
file where the declared `final` differs by more than 0.05 from the recalculated value.

## Rubric version history

| Version | Date       | Changes |
|---------|------------|---------|
| 1       | 2026-07-15 | Initial release |
