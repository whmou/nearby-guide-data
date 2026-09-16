"""Source-coordinate publication gate. Format validation is not a location audit."""
from __future__ import annotations

import math
from urllib.parse import parse_qs, urlparse

STATUSES = {"verified", "unresolved", "non_point"}
ANCHORS = {"entrance", "landmark", "viewpoint", "visitor_area", "area", "meeting_point", "none"}


def maps_url(latitude: float, longitude: float) -> str:
    return f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"


def distance_m(a: dict, b: dict) -> float:
    lat1, lat2 = map(math.radians, (a["latitude"], b["latitude"]))
    dl = math.radians(b["latitude"] - a["latitude"])
    dn = math.radians(b["longitude"] - a["longitude"])
    h = math.sin(dl / 2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dn / 2)**2
    return 6371000 * 2 * math.asin(min(1, math.sqrt(h)))


def location_errors(data: dict, require_review: bool = False) -> list[str]:
    p = data["point"]
    review = data.get("locationReview")
    loc, trigger, link = p.get("location"), p.get("trigger"), p.get("googleMapsUrl")
    errors = []
    if bool(loc) != bool(trigger):
        errors.append("location and trigger must be present or absent together")
    if loc:
        for key, limit in (("latitude", 90), ("longitude", 180)):
            value = loc.get(key)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or abs(value) > limit:
                errors.append(f"invalid {key}")
        if trigger and trigger.get("rearmDistanceMeters", 0) <= trigger.get("radiusMeters", 0):
            errors.append("rearmDistanceMeters must exceed radiusMeters")
        if not link and (require_review or review is not None):
            errors.append("GPS point must have a coordinate Google Maps URL")
        elif link:
            parsed = urlparse(link)
            params = parse_qs(parsed.query)
            query = params.get("query", params.get("q", [""]))[0]
            try:
                lat, lng = [float(v.strip()) for v in query.split(",")]
                if not math.isfinite(lat) or not math.isfinite(lng):
                    raise ValueError("nonfinite coordinate")
                if parsed.scheme != "https" or parsed.hostname not in {"maps.google.com", "www.google.com", "google.com"}:
                    raise ValueError("host")
                if abs(lat - loc["latitude"]) > 1e-7 or abs(lng - loc["longitude"]) > 1e-7:
                    raise ValueError("coordinate mismatch")
            except (ValueError, KeyError, TypeError):
                errors.append("Google Maps URL must match the point coordinates exactly")
    elif link:
        errors.append("point without a verified location must not publish a navigation link")
    if review is None:
        if require_review:
            errors.append("locationReview required; geographic bounds alone are not verification")
        return errors
    if review.get("status") not in STATUSES:
        errors.append("invalid locationReview status")
    if review.get("anchorType") not in ANCHORS:
        errors.append("invalid anchorType")
    if not review.get("reason", "").strip() or not review.get("checkedAt"):
        errors.append("locationReview must record reason and checkedAt")
    if review.get("status") == "verified":
        if not loc:
            errors.append("verified location must have coordinates")
        if review.get("anchorType") in {"none", "area"}:
            errors.append("area centres are not usable arrival anchors")
        if not p.get("locationHint", ""):
            errors.append("verified location must explain the arrival anchor")
        if loc != review.get("verifiedLocation"):
            errors.append("coordinates changed since review; re-verify before publishing")
        sources = review.get("sources", [])
        if not sources:
            errors.append("verified location needs coordinate evidence")
        for src in sources:
            if not src.get("url", "").startswith("https://") or not src.get("coordinateEvidence", "").strip() or not src.get("title", "").strip():
                errors.append("coordinate evidence requires HTTPS source, title and extraction details")
    elif loc or trigger or link:
        errors.append("unresolved/non_point must not emit GPS, trigger or navigation URL")
    return errors
