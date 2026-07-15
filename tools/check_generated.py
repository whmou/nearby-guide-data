"""
tools/check_generated.py — Rebuild packs into a temp dir and verify SHA-256 reproducibility.

Usage:
    python tools/check_generated.py
"""

from __future__ import annotations

import hashlib
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = REPO_ROOT / "dist"


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    packs_dir = DIST_DIR / "packs"
    if not packs_dir.exists() or not any(packs_dir.glob("*.guidepack")):
        print("No .guidepack files in dist/packs/ — run build_packs.py first.", file=sys.stderr)
        return 1

    # Capture original hashes
    originals: dict[str, str] = {}
    for f in sorted(packs_dir.glob("*.guidepack")):
        originals[f.name] = _sha256_file(f)

    # Rebuild into temp dir
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "build_packs", REPO_ROOT / "tools" / "build_packs.py"
    )
    build_packs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(build_packs)  # type: ignore[union-attr]

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        build_packs.build_all(tmp_path)

        tmp_packs_dir = tmp_path / "packs"
        errors = 0

        for name, original_sha in sorted(originals.items()):
            rebuilt = tmp_packs_dir / name
            if not rebuilt.exists():
                print(f"  MISSING in rebuild: {name}", file=sys.stderr)
                errors += 1
                continue
            rebuilt_sha = _sha256_file(rebuilt)
            if rebuilt_sha == original_sha:
                print(f"  OK  {name}")
            else:
                print(
                    f"  DIFF {name}\n"
                    f"       original:  {original_sha}\n"
                    f"       rebuilt:   {rebuilt_sha}",
                    file=sys.stderr,
                )
                errors += 1

        # Check for extra files in rebuild not in original
        for f in sorted(tmp_packs_dir.glob("*.guidepack")):
            if f.name not in originals:
                print(f"  EXTRA in rebuild (not in dist): {f.name}", file=sys.stderr)
                errors += 1

    if errors == 0:
        print(f"\nAll {len(originals)} pack(s) are reproducible.")
        return 0
    else:
        print(f"\n{errors} reproducibility error(s) found.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
