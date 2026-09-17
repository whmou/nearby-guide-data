"""Android point checks shared by source, build and published-archive gates.

Ported from the supplied Android v0.8.0 GuidePackFormat.kt, validatePoints(),
lines 161-167. This module covers the locationHint rule, not the entire parser.
The Android error says 'indoor', but the predicate does NOT use indoor.
"""

HINT_REQUIRED_WITHOUT_GPS = frozenset({"zone", "artwork", "exhibit", "view"})


def point_errors(point: dict) -> list[str]:
    """Match Android's no-GPS locationHint requirement, including mixed case."""
    kind = point.get("kind", "")
    if point.get("location") is None and str(kind).lower() in HINT_REQUIRED_WITHOUT_GPS:
        hint = point.get("locationHint")
        if not isinstance(hint, str) or not hint.strip():
            return [f"Android: {kind} without GPS must provide a nonblank locationHint"]
    return []
