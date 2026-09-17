# Miyakojima v1.1.1 Android locationHint repair

The user reported an installation rejection after v1.1.0: `室內 view 導覽點必須提供 locationHint`.
This was a dataset/validation gap, not evidence that these records are indoors.

## Contract and reproduction

Read the user-supplied `nearby-guide-android-source-v0.8.0-2026-07-27.zip`:
`app/src/main/java/com/example/nearbyguide/guidepack/GuidePackFormat.kt`, lines 161–167.
If `location == null` and `kind.lowercase()` is one of `zone`, `artwork`,
`exhibit`, `view`, Android requires `!locationHint.isNullOrBlank()`.
The old validator checked source `indoor` only; Android does not use that flag.

The new archive check reproduces rejection of the existing v1.1.0 compact ZIP
(exit 1), identifying both offending records:

- `jp-miyakojima-biyandam-viewpoint` — unresolved place identity/entrance.
- `jp-miyakojima-ikema-dugong` — conservation reading, not a fixed wildlife viewpoint.

## Bounded repair

Added meaningful location hints explaining those existing limitations, reviewed
against each record's already-reviewed summary, narration and location evidence.
Synchronized both hints into `existing-1.json` and resealed that editorial snapshot.
No new coordinate, entrance, navigation link, wildlife guarantee or factual story
claim was introduced. Both records retain null GPS/trigger/navigation and their
existing unresolved/non_point status. All 108 records and 72 GPS points remain.
Only the Miyako pack version changes (1.1.0 → 1.1.1); other pack bytes must remain
unchanged. The old release is preserved for traceability, not reused or overwritten.

## Prevention

`tools/android_contract.py` expresses the actual no-GPS hint predicate. Source
validation, direct builds, ZIP inspection and anonymous public-download checks
all call it, so archive hashes alone cannot certify installation compatibility.
Regression tests cover absent/null/empty/whitespace hints, all four kinds and
mixed case, source and built artifacts, as well as permitted GPS/text-only cases.
This is a targeted parity check, not execution of the Android app or a claim that
every future Android rule is mirrored. On-device install remains a separate check.

Local verification: 307 tests passed, zero skips; all eight current archives
passed inspection and byte-for-byte rebuild reproducibility. The six non-Miyako
assets match the previously published catalog's byte counts and SHA-256 hashes.
Comparing v1.1.0 against v1.1.1, both variants change only the two point hints
plus manifest version/date/integrity metadata; images, coordinates and stories
are unchanged. An independent static check of the supplied Kotlin model,
format validator and import checks found no other rejection in these eight
artifacts. This does not substitute for on-device installation.
