"""Print a patch replacing initial report entries with reviewed followup evidence."""
import json
from pathlib import Path
from normalize_authoring_metadata import hunks

ROOT = Path(__file__).resolve().parents[1]


def patch():
    followups = json.loads((ROOT / "audits/followups/xiaoliuqiu.json").read_text(encoding="utf-8-sig"))
    replacements = {p["id"]: p for p in followups}
    lines = ["*** Begin Patch"]
    for path in sorted((ROOT / "audits/location-2026-09-16").glob("*.json")):
        old = path.read_text(encoding="utf-8-sig")
        entries = json.loads(old)
        changed = False
        for i, entry in enumerate(entries):
            if entry["id"] in replacements:
                replacement = replacements.pop(entry["id"])
                if entry != replacement:
                    entries[i] = replacement
                    changed = True
        if changed:
            new = json.dumps(entries, ensure_ascii=False, indent=2) + "\n"
            lines.extend(hunks(path, old, new))
    if replacements:
        raise ValueError("Unexpected followup IDs")
    return "\n".join(lines + ["*** End Patch"])


if __name__ == "__main__":
    print(patch())
