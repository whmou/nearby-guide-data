"""Print a mechanical patch for legacy authoring omissions, never invent facts.

Restore misplaced locationHint, use the actual source hostname when publisher
was empty, and recompute declared rubric totals with Decimal half-up. Explicit
existing tag vocabulary is registered in taxonomy so all four packs validate.
This does not claim the original prose or images are fact-checked.
"""
import re
import difflib
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from urllib.parse import urlparse
import yaml

ROOT = Path(__file__).resolve().parents[1]


def hunks(path, old, new):
    diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(), n=3, lineterm=""))[2:]
    return [f"*** Update File: {path.as_posix()}"] + ["@@" if line.startswith("@@") else line for line in diff]


def patch():
    parts = ["*** Begin Patch"]
    taxonomy_path = ROOT / "taxonomy/tags.yaml"
    taxonomy_text = taxonomy_path.read_text(encoding="utf-8")
    taxonomy = yaml.safe_load(taxonomy_text)
    groups = {g["id"]: g for g in taxonomy["groups"]}
    for path in sorted((ROOT / "regions").glob("*/*/points/*.yaml")):
        old = path.read_text(encoding="utf-8-sig")
        data = yaml.safe_load(old)
        p = data["point"]
        text = old
        if "locationHint" not in p:
            hint = (p.get("location") or {}).get("locationHint")
            line = yaml.safe_dump({"locationHint": hint}, allow_unicode=True, width=10000).strip()
            text = text.replace("ratingEvidence:\n", "  " + line + "\nratingEvidence:\n", 1)
        for source in data.get("sources", []):
            if not source.get("publisher"):
                hostname = urlparse(source["url"]).hostname
                if not hostname:
                    raise ValueError("Invalid source URL: " + source["url"])
                # Both generated packs have one source; preserve all other fields.
                text = text.replace('    publisher: ""', f'    publisher: "{hostname}"', 1)
        weights = {"significance": ".30", "distinctiveness": ".25", "interpretability": ".20", "visitorValue": ".15", "evidenceQuality": ".10"}
        rating = data["ratingEvidence"]
        total = sum(Decimal(w)*Decimal(rating[k]["score"]) for k,w in weights.items()).quantize(Decimal(".1"), rounding=ROUND_HALF_UP)
        if Decimal(str(rating["final"])) != total:
            text = re.sub(r"^  final:.*$", "  final: " + str(total), text, count=1, flags=re.M)
        for group in p["tagGroups"]:
            known = {t["id"] for t in groups[group["id"]]["tags"]}
            for tag in group["tags"]:
                if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", tag["id"]) or tag["id"] == "unknown":
                    raise ValueError("Unknown or non-slug production tag: " + tag["id"])
                if tag["id"] not in known:
                    groups[group["id"]]["tags"].append(tag)
                    known.add(tag["id"])
        if text != old:
            parts += hunks(path, old, text)
    new_taxonomy = yaml.safe_dump(taxonomy, allow_unicode=True, sort_keys=False)
    if new_taxonomy != taxonomy_text:
        parts += hunks(taxonomy_path, taxonomy_text, new_taxonomy)
    parts += ["*** End Patch"]
    return "\n".join(parts)


if __name__ == "__main__":
    print(patch())
