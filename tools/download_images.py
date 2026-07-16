"""
tools/download_images.py — Download real Wikimedia Commons images for every point,
convert to compact/complete WebP, and update source YAML + metadata cache.

Usage:
    python tools/download_images.py

For each media item in regions/*/points/*.yaml:
  1. Resolve the Wikimedia Commons File page referenced by sourceUrl.
  2. If it is missing / a Category page / non-free, search Commons for a licensed
     replacement (CC0 / public domain / CC-BY / CC-BY-SA).
  3. Download the original, compute its SHA-256.
  4. Convert to compact (<=640px, q70) and complete (<=1600px, q80) WebP.
  5. Rewrite the media fields (sourceUrl, creator, license, licenseUrl,
     originalSha256) in the source YAML.
  6. Write tools/image_metadata_cache.json for MEDIA_LICENSES.md generation.

Only the converted WebP files are meant to be committed — never the originals.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import io
import json
import re
import sys
import threading
import time
from pathlib import Path
from urllib.parse import unquote

import requests
import yaml
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
REGIONS_DIR = REPO_ROOT / "regions"
CACHE_PATH = REPO_ROOT / "tools" / "image_metadata_cache.json"

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "NearbyGuideBot/1.0 (https://github.com/whmou/nearby-guide-data; whmou@gmail.com)"}
ACCESSED_AT = "2026-07-16"

COMPACT_EDGE = 640
COMPLETE_EDGE = 1600

# Accept CC0, public domain, or any CC-BY / CC-BY-SA license.
LICENSE_OK = re.compile(
    r"(cc0|cc[\-\s]?by|public\s*domain|pd[\-\s]|no\s+restrictions)", re.IGNORECASE
)
LICENSE_BAD = re.compile(r"(cc[\-\s]?by[\-\s]?nc|cc[\-\s]?by[\-\s]?nd|non[\-\s]?commercial|no[\-\s]?deriv|fair\s*use)", re.IGNORECASE)

# Curated search queries for points whose original reference is missing/broken and
# whose auto-derived queries return no licensed image. Ordered most-specific first;
# a broad island/area fallback guarantees a representative licensed image.
CURATED_QUERIES: dict[str, list[str]] = {
    "jp-miyakojima-17end-beach": ["Shimojishima Runway17", "17END Shimoji", "Shimoji Island beach"],
    "jp-miyakojima-biyandam-viewpoint": ["Miyakojima", "Miyako Island Okinawa"],
    "jp-miyakojima-irabu-diving": ["Irabujima", "Irabu Island diving", "Irabu Island"],
    "jp-miyakojima-irabu-katsuobushi": ["Irabujima", "Irabu Island Miyako", "Sarahama"],
    "jp-miyakojima-irabu-lighthouse": ["Irabu Island", "Irabujima", "Sarahama Irabu"],
    "jp-miyakojima-kaijin-no-mori": ["Ikema Island", "Ikemajima", "Miyakojima"],
    "jp-miyakojima-kamama-ridge-park": ["Miyakojima", "Miyako Island Okinawa"],
    "jp-miyakojima-maou-palace-cave": ["Shimoji Island", "Irabu Island", "Irabujima sky view"],
    "jp-miyakojima-miyako-traditional-textile": ["Miyakojima", "Miyako Island Okinawa"],
    "jp-miyakojima-nakanoshima-channel": ["Shimoji Island", "Shimojishima", "Nakanoshima Miyako"],
    "jp-miyakojima-shimajiri-uganzaki": ["Miyako Island mangrove", "Shimajiri Miyako", "Miyakojima"],
    "jp-miyakojima-shimoji-cave-dive": ["Shimoji Island", "Shimojishima", "Irabu Island diving"],
    "jp-miyakojima-shiratorisaki": ["Irabu Island", "Irabujima", "Miyakojima"],
    "tw-hsinchu-mifun-culture": ["Rice vermicelli Hsinchu", "Rice noodles Taiwan", "Hsinchu"],
    "jp-miyakojima-tropical-botanical-garden": [
        "Miyako Island tropical botanical garden", "Miyakojima", "Okinawa botanical garden"
    ],
}

SESSION = requests.Session()
SESSION.headers.update(UA)

# Global request throttle — Wikimedia rate-limits aggressive bots (HTTP 429).
# Serialize every request behind a minimum interval.
_THROTTLE_LOCK = threading.Lock()
_MIN_INTERVAL = 0.8  # seconds between any two requests
_last_request = [0.0]


def _throttled_get(url: str, **kwargs) -> requests.Response:
    """GET with a global minimum interval and 429/5xx-aware retry."""
    for attempt in range(7):
        with _THROTTLE_LOCK:
            wait = _MIN_INTERVAL - (time.monotonic() - _last_request[0])
            if wait > 0:
                time.sleep(wait)
            _last_request[0] = time.monotonic()
        try:
            r = SESSION.get(url, timeout=120, **kwargs)
        except Exception:  # noqa: BLE001 — network hiccup
            if attempt == 6:
                raise
            time.sleep(2 * (attempt + 1))
            continue
        if r.status_code == 429 or r.status_code >= 500:
            retry_after = r.headers.get("Retry-After")
            delay = float(retry_after) if (retry_after or "").isdigit() else 3 * (attempt + 1)
            time.sleep(min(delay, 30))
            continue
        r.raise_for_status()
        return r
    r.raise_for_status()
    return r


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def api_get(params: dict) -> dict:
    params = {**params, "format": "json"}
    r = _throttled_get(API, params=params)
    return r.json()


def license_acceptable(short: str) -> bool:
    if not short:
        return False
    if LICENSE_BAD.search(short):
        return False
    return bool(LICENSE_OK.search(short))


def file_page_url(title: str) -> str:
    # title like 'File:Some Name.jpg'
    return "https://commons.wikimedia.org/wiki/" + title.replace(" ", "_")


def parse_source(source_url: str) -> tuple[str, str | None]:
    """Return ('file', 'File:Name.jpg') or ('category', 'Category:X') or ('other', None)."""
    m = re.search(r"/wiki/(File:.+)$", source_url)
    if m:
        return "file", unquote(m.group(1)).replace("_", " ")
    m = re.search(r"/wiki/(Category:.+)$", source_url)
    if m:
        return "category", unquote(m.group(1)).replace("_", " ")
    return "other", None


def imageinfo_batch(titles: list[str]) -> dict[str, dict | None]:
    """Return {title: imageinfo_meta or None} for a list of File: titles."""
    out: dict[str, dict | None] = {}
    for i in range(0, len(titles), 40):
        chunk = titles[i : i + 40]
        data = api_get(
            {
                "action": "query",
                "titles": "|".join(chunk),
                "prop": "imageinfo",
                "iiprop": "url|user|extmetadata|size|mime",
            }
        )
        pages = data.get("query", {}).get("pages", {})
        # Map normalized titles back
        norm = {}
        for n in data.get("query", {}).get("normalized", []):
            norm[n["to"]] = n["from"]
        for _pid, pg in pages.items():
            title = pg.get("title")
            orig = norm.get(title, title)
            if pg.get("missing") is not None or "imageinfo" not in pg:
                out[orig] = None
            else:
                out[orig] = pg["imageinfo"][0]
    return out


def meta_from_imageinfo(title: str, ii: dict) -> dict:
    em = ii.get("extmetadata", {})
    artist = strip_html(em.get("Artist", {}).get("value", "")) or ii.get("user", "") or "Unknown"
    # collapse whitespace
    artist = re.sub(r"\s+", " ", artist).strip()
    license_short = strip_html(em.get("LicenseShortName", {}).get("value", "")).strip()
    license_url = em.get("LicenseUrl", {}).get("value", "").strip()
    if not license_url:
        # public domain often has no LicenseUrl
        if re.search(r"public\s*domain|cc0", license_short, re.IGNORECASE):
            license_url = "https://creativecommons.org/publicdomain/mark/1.0/"
    return {
        "title": title,
        "filePage": file_page_url(title),
        "url": ii["url"],
        "creator": artist,
        "license": license_short or "Unknown",
        "licenseUrl": license_url,
        "mime": ii.get("mime", ""),
        "width": ii.get("width"),
        "height": ii.get("height"),
    }


def search_titles(query: str, limit: int = 12) -> list[str]:
    data = api_get(
        {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srnamespace": 6,
            "srlimit": limit,
        }
    )
    return [it["title"] for it in data.get("query", {}).get("search", [])]


IMG_EXT = re.compile(r"\.(jpe?g|png|tiff?)$", re.IGNORECASE)


def pick_replacement(queries: list[str]) -> dict | None:
    """Search a list of query strings; return meta for the first acceptable image."""
    seen: set[str] = set()
    for q in queries:
        if not q.strip():
            continue
        titles = [t for t in search_titles(q) if IMG_EXT.search(t) and t not in seen]
        seen.update(titles)
        if not titles:
            continue
        infos = imageinfo_batch(titles)
        for t in titles:  # preserve search relevance order
            ii = infos.get(t)
            if not ii:
                continue
            if not str(ii.get("mime", "")).startswith("image/"):
                continue
            meta = meta_from_imageinfo(t, ii)
            if license_acceptable(meta["license"]):
                return meta
    return None


def derive_query_from_id(point_id: str, title: str) -> list[str]:
    """Build search queries from the point id and region."""
    parts = point_id.split("-")
    # region keyword
    region_kw = ""
    if point_id.startswith("tw-hsinchucounty"):
        region_kw = "Hsinchu"
        words = parts[2:]
    elif point_id.startswith("tw-hsinchu"):
        region_kw = "Hsinchu"
        words = parts[2:]
    elif point_id.startswith("jp-miyakojima"):
        region_kw = "Miyakojima"
        words = parts[2:]
    else:
        words = parts
    name = " ".join(words)
    q = f"{name} {region_kw}".strip()
    return [q, name]


# ---------------------------------------------------------------------------
# YAML rewriting (line-targeted to preserve formatting & comments)
# ---------------------------------------------------------------------------

def _yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def rewrite_media_yaml(path: Path, meta: dict, original_sha: str) -> None:
    text = path.read_text(encoding="utf-8")

    def repl(pattern: str, new_line_body: str) -> None:
        nonlocal text
        # keep original indentation
        m = re.search(pattern, text, re.MULTILINE)
        if not m:
            raise RuntimeError(f"{path.name}: could not find pattern {pattern!r}")
        indent = m.group("indent")
        text = text[: m.start()] + f"{indent}{new_line_body}" + text[m.end():]

    repl(r"(?P<indent>[ \t]+)sourceUrl:.*", f"sourceUrl: {meta['filePage']}")
    repl(r"(?P<indent>[ \t]+)creator:.*", f"creator: {_yaml_quote(meta['creator'])}")
    repl(r"(?P<indent>[ \t]+)license:.*", f"license: {_yaml_quote(meta['license'])}")
    repl(r"(?P<indent>[ \t]+)licenseUrl:.*", f"licenseUrl: {meta['licenseUrl']}")
    repl(r"(?P<indent>[ \t]+)originalSha256:.*", f'originalSha256: "{original_sha}"')

    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Image conversion
# ---------------------------------------------------------------------------

def convert_webp(original: bytes, longest_edge: int, quality: int) -> bytes:
    img = Image.open(io.BytesIO(original))
    img = img.convert("RGB")
    w, h = img.size
    if max(w, h) > longest_edge:
        scale = longest_edge / max(w, h)
        img = img.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="WEBP", quality=quality, method=6, exif=b"")
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Task discovery
# ---------------------------------------------------------------------------

class Task:
    def __init__(self, yaml_path: Path, region_dir: Path, point_id: str, point_title: str, media: dict):
        self.yaml_path = yaml_path
        self.region_dir = region_dir
        self.point_id = point_id
        self.point_title = point_title
        self.media = media
        self.meta: dict | None = None
        self.replaced = False
        self.old_source = media.get("sourceUrl", "")


def discover_tasks() -> list[Task]:
    tasks: list[Task] = []
    for pf in sorted(REGIONS_DIR.rglob("points/*.yaml")):
        data = yaml.safe_load(pf.read_text(encoding="utf-8"))
        point = data.get("point", {})
        pid = point.get("id") or data.get("id")
        title = point.get("title", "")
        region_dir = pf.parent.parent  # regions/<c>/<r>
        for m in data.get("media", []):
            if m.get("type") != "image":
                continue
            tasks.append(Task(pf, region_dir, pid, title, m))
    return tasks


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def resolve_meta(tasks: list[Task]) -> None:
    """Populate task.meta for every task, using direct File: lookup then search."""
    # Phase 1: batch imageinfo for direct File: references
    direct: dict[str, list[Task]] = {}
    for t in tasks:
        kind, ident = parse_source(t.old_source)
        if kind == "file":
            direct.setdefault(ident, []).append(t)

    print(f"Resolving {len(direct)} direct File: references via imageinfo …")
    infos = imageinfo_batch(list(direct.keys()))

    need_search: list[Task] = []
    for title, ts in direct.items():
        ii = infos.get(title)
        if ii and str(ii.get("mime", "")).startswith("image/"):
            meta = meta_from_imageinfo(title, ii)
            if license_acceptable(meta["license"]):
                for t in ts:
                    t.meta = meta
                continue
        need_search.extend(ts)

    for t in tasks:
        kind, _ = parse_source(t.old_source)
        if kind != "file":
            need_search.append(t)

    print(f"{len(tasks) - len(need_search)} resolved directly; {len(need_search)} need search fallback.")

    # Phase 2: search fallback (sequential — network bound but modest volume)
    for i, t in enumerate(need_search, 1):
        queries: list[str] = []
        kind, ident = parse_source(t.old_source)
        if kind == "file" and ident:
            queries.append(re.sub(IMG_EXT, "", ident.replace("File:", "")).strip())
        if kind == "category" and ident:
            cat = ident.replace("Category:", "")
            cat = re.sub(r"[,_]", " ", cat)
            queries.append(cat)
        queries.extend(CURATED_QUERIES.get(t.point_id, []))
        queries.extend(derive_query_from_id(t.point_id, t.point_title))
        if t.point_title:
            queries.append(t.point_title)
        meta = pick_replacement(queries)
        if meta:
            t.meta = meta
            t.replaced = True
            print(f"  [{i}/{len(need_search)}] REPLACED: {t.point_id}: {t.old_source} -> {meta['filePage']}")
        else:
            print(f"  [{i}/{len(need_search)}] FAILED: {t.point_id}: no licensed image found (queries={queries})")


def process_download(t: Task) -> tuple[Task, bool, str]:
    if not t.meta:
        return t, False, "no metadata"
    try:
        r = _throttled_get(t.meta["url"])
        original = r.content
        original_sha = sha256_bytes(original)

        compact = convert_webp(original, COMPACT_EDGE, 70)
        complete = convert_webp(original, COMPLETE_EDGE, 80)

        # verify decodable
        Image.open(io.BytesIO(compact)).verify()
        Image.open(io.BytesIO(complete)).verify()

        compact_dir = t.region_dir / "media" / "compact"
        complete_dir = t.region_dir / "media" / "complete"
        compact_dir.mkdir(parents=True, exist_ok=True)
        complete_dir.mkdir(parents=True, exist_ok=True)
        (compact_dir / f"{t.point_id}.webp").write_bytes(compact)
        (complete_dir / f"{t.point_id}.webp").write_bytes(complete)

        t.meta["originalSha256"] = original_sha
        t.meta["compactBytes"] = len(compact)
        t.meta["completeBytes"] = len(complete)
        return t, True, original_sha
    except Exception as exc:  # noqa: BLE001
        return t, False, f"error: {exc}"


def _webp_exist(t: Task) -> bool:
    return (t.region_dir / "media" / "compact" / f"{t.point_id}.webp").exists() and (
        t.region_dir / "media" / "complete" / f"{t.point_id}.webp"
    ).exists()


def main() -> int:
    force = "--force" in sys.argv
    prior_cache: dict[str, dict] = {}
    if CACHE_PATH.exists():
        try:
            prior_cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            prior_cache = {}

    all_tasks = discover_tasks()
    print(f"Discovered {len(all_tasks)} image media items.\n")

    # Skip points whose WebP already exist (idempotent re-runs) unless --force.
    done_tasks = [t for t in all_tasks if not force and _webp_exist(t)]
    tasks = [t for t in all_tasks if t not in done_tasks]
    if done_tasks:
        print(f"Skipping {len(done_tasks)} points that already have both WebP files.\n")

    resolve_meta(tasks)

    resolvable = [t for t in tasks if t.meta]
    unresolved = [t for t in tasks if not t.meta]

    print(f"\nDownloading & converting {len(resolvable)} images …")
    succeeded: list[Task] = []
    failed: list[tuple[Task, str]] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(process_download, t): t for t in resolvable}
        done = 0
        for fut in concurrent.futures.as_completed(futs):
            t, ok, info = fut.result()
            done += 1
            if ok:
                succeeded.append(t)
                print(f"  [{done}/{len(resolvable)}] OK {t.point_id} ({t.meta['compactBytes']}/{t.meta['completeBytes']} B)")
            else:
                failed.append((t, info))
                print(f"  [{done}/{len(resolvable)}] FAIL {t.point_id}: {info}")

    # Update YAML + build metadata cache for successes.
    # Preserve prior-cache entries for points skipped this run (already downloaded).
    cache: dict[str, dict] = {}
    for t in done_tasks:
        if t.point_id in prior_cache:
            cache[t.point_id] = prior_cache[t.point_id]
    for t in succeeded:
        rewrite_media_yaml(t.yaml_path, t.meta, t.meta["originalSha256"])
        cache[t.point_id] = {
            "pointId": t.point_id,
            "title": t.point_title,
            "creator": t.meta["creator"],
            "license": t.meta["license"],
            "licenseUrl": t.meta["licenseUrl"],
            "sourceUrl": t.meta["filePage"],
            "originalSha256": t.meta["originalSha256"],
            "accessedAt": ACCESSED_AT,
            "replaced": t.replaced,
            "originalSource": t.old_source if t.replaced else None,
            "region": t.region_dir.relative_to(REGIONS_DIR).as_posix(),
        }

    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

    replaced = [t for t in succeeded if t.replaced]
    covered = len(done_tasks) + len(succeeded)
    print("\n" + "=" * 60)
    print("SUMMARY")
    print(f"  total points        : {len(all_tasks)}")
    print(f"  already had WebP     : {len(done_tasks)}")
    print(f"  newly succeeded      : {len(succeeded)}")
    print(f"  replaced (this run)  : {len(replaced)}")
    print(f"  total with WebP now  : {covered}/{len(all_tasks)}")
    print(f"  failed               : {len(failed) + len(unresolved)}")
    if failed or unresolved:
        print("\n  FAILURES (need manual review):")
        for t, info in failed:
            print(f"    - {t.point_id}: {info}")
        for t in unresolved:
            print(f"    - {t.point_id}: unresolved (no licensed image found)")
    print(f"\n  metadata cache written to {CACHE_PATH}")
    return 0 if covered == len(all_tasks) else 1


if __name__ == "__main__":
    sys.exit(main())
