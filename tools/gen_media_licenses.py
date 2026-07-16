"""
tools/gen_media_licenses.py — Regenerate MEDIA_LICENSES.md from the metadata cache
written by tools/download_images.py.

Usage:
    python tools/gen_media_licenses.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_PATH = REPO_ROOT / "tools" / "image_metadata_cache.json"
OUT_PATH = REPO_ROOT / "MEDIA_LICENSES.md"

HEADER = """# Media Licenses

Media files referenced in point YAMLs (images) are NOT covered by the repository's
CC-BY-4.0 data license. Each media item carries its own license, declared in the point
YAML's `media[].license` and `media[].licenseUrl` fields.

All images are sourced from Wikimedia Commons under CC0 / Public Domain / CC-BY / CC-BY-SA
licenses. The table below is generated from `tools/image_metadata_cache.json` by
`tools/gen_media_licenses.py`. Do not edit it by hand.

## Policy

- Only CC0, CC-BY, or CC-BY-SA licensed media may be included in production packs.
- CC-BY-SA / CC-BY media require the downstream app to display attribution; the
  `media[].creator` and `media[].licenseUrl` fields are included in the generated
  points.json for this purpose.
- When a media file is downloaded, the SHA-256 of the **original** is recorded in
  `media[].originalSha256`. Never modify a downloaded original without updating this hash.
- Some original references were missing or pointed at a Category page; in those cases a
  suitable licensed replacement image was selected (marked ✔ in the *Replaced* column).

"""


def _esc(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


def main() -> int:
    if not CACHE_PATH.exists():
        print(f"ERROR: {CACHE_PATH} not found — run tools/download_images.py first", file=sys.stderr)
        return 1

    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    rows = sorted(cache.values(), key=lambda r: r["pointId"])

    lines = [HEADER]
    lines.append(f"## Image attributions ({len(rows)} points)\n")
    lines.append("| Point ID | Title | Creator | License | Source (Wikimedia Commons) | Accessed | Replaced |")
    lines.append("|----------|-------|---------|---------|-----------------------------|----------|:--------:|")

    replaced_notes = []
    for r in rows:
        replaced = r.get("replaced")
        mark = "✔" if replaced else ""
        lines.append(
            f"| `{_esc(r['pointId'])}` "
            f"| {_esc(r.get('title', ''))} "
            f"| {_esc(r.get('creator', ''))} "
            f"| {_esc(r.get('license', ''))} "
            f"| [source]({_esc(r.get('sourceUrl', ''))}) "
            f"| {_esc(r.get('accessedAt', ''))} "
            f"| {mark} |"
        )
        if replaced and r.get("originalSource"):
            replaced_notes.append((r["pointId"], r["originalSource"], r["sourceUrl"]))

    if replaced_notes:
        lines.append("\n## Replacement notes\n")
        lines.append(
            "The following points had a missing/invalid or Category-only original reference; "
            "a licensed replacement was selected:\n"
        )
        lines.append("| Point ID | Original reference | Replacement |")
        lines.append("|----------|--------------------|-------------|")
        for pid, old, new in replaced_notes:
            lines.append(f"| `{_esc(pid)}` | {_esc(old)} | {_esc(new)} |")

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"MEDIA_LICENSES.md regenerated with {len(rows)} image rows "
          f"({len(replaced_notes)} replacements).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
