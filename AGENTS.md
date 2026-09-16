# Dataset authoring and repair

Read `LOCATION_REVIEW.md` and `CONTRIBUTING.md` before edits. A plausible story or
successful build is not evidence that a place exists or its coordinates work.

- Actually fetch sources for every coordinate review; record exact source and
  extraction evidence. Do not invent GPS from memory, bounding boxes, photos,
  map viewport centres, or first geocoder results.
- Resolve place identity first. Never substitute an unrelated named business
  for a generic food/activity theme. Distinguish landmarks from entrances.
- Keep `location`, trigger eligibility, `googleMapsUrl`, and `locationHint`
  consistent. Unresolved/non-point entries retain text, not guessed navigation.
- Use bounded, non-overlapping review batches. Inspect and integrate their
  output; completion of agents is not completion of valid dataset files.
- Correct discovered unsafe/misleading directions; keep remaining editorial
  and image evidence gaps explicit. Never use fabricated photos or licenses.
- Do not change permission settings or promise to suppress all approvals.
- Build all four current packs from source, then run all tests and reproducibility
  checks. Do not accept skipped artifact tests or artifacts from older versions.
- Publish versioned assets without overwriting existing releases, verify public
  byte counts and hashes, then publish the pinned catalog and viewer export.
- Do not report an on-device success without an actual on-device test.
