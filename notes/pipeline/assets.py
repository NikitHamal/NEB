"""Real photographs and reference diagrams: fetch, licence-gate, register, credit.

Drawn figures (```figure blocks) carry the schematic work; some things a student
needs cannot be drawn from code and must be a real image — a micrograph, a
crystal, an apparatus photograph, a portrait, a published reference diagram.

Every image in the books is fetched through here, so three things are true by
construction:

1. The licence is free (public domain / CC0 / CC BY / CC BY-SA / GFDL). A file
   whose licence string does not match the allowlist is refused, not downloaded.
2. The attribution the licence requires is recorded at fetch time in
   ``assets/credits.json`` — author, licence, licence URL, source page — so the
   book's Picture Credits appendix is generated, never hand-written.
3. The bytes live in the repo under ``assets/<slug>/<id>.<ext>``, so a build
   never depends on the network.

CLI
    python3 assets.py search "mitochondrion diagram"      # candidates + licences
    python3 assets.py get bio11/mitochondrion "File:Animal mitochondrion diagram en.svg"
    python3 assets.py geturl chem11/flame-test <url> --title T --author A \
            --license "CC BY-SA 4.0" --license-url U --page P --source "Site"
    python3 assets.py list [slug]
    python3 assets.py verify            # every registered id has bytes on disk
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
ASSETS = os.path.join(ROOT, "assets")
REGISTRY = os.path.join(ASSETS, "credits.json")

UA = ("NEBiansNotes/1.0 (https://nebians.consica.com.np; "
      "free study books for Nepali NEB students)")
COMMONS = "https://commons.wikimedia.org/w/api.php"

# Licences we may reproduce in a freely-redistributable study book. Matched
# case-insensitively as a substring of the file's licence short name.
FREE = (
    "public domain", "pd-", "cc0", "cc-zero", "no restrictions",
    "cc by", "cc-by", "attribution",
    "gfdl", "free art", "fal", "ogl",
)
# Explicitly refused, even when the words above appear somewhere in the string.
NONFREE = ("non-commercial", "noncommercial", "-nc", "no derivative",
           "noderiv", "-nd", "fair use", "all rights reserved", "copyright")

MAX_BYTES = 3_000_000


# ------------------------------------------------------------------ registry
def load() -> dict:
    if os.path.exists(REGISTRY):
        with open(REGISTRY, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save(reg: dict) -> None:
    os.makedirs(ASSETS, exist_ok=True)
    tmp = REGISTRY + f".{os.getpid()}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    os.replace(tmp, REGISTRY)


class _Lock:
    """Chapter authors fetch images in parallel; one registry, so serialise the
    read-modify-write or the last writer silently drops everyone else's credits."""

    def __enter__(self):
        import fcntl
        os.makedirs(ASSETS, exist_ok=True)
        self.fh = open(REGISTRY + ".lock", "w")
        fcntl.flock(self.fh, fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc):
        import fcntl
        fcntl.flock(self.fh, fcntl.LOCK_UN)
        self.fh.close()
        return False


def path_for(asset_id: str) -> str | None:
    """Absolute path to the bytes of a registered asset, or None."""
    rec = load().get(asset_id)
    if not rec:
        return None
    p = os.path.join(ASSETS, rec["file"])
    return p if os.path.exists(p) else None


def record(asset_id: str) -> dict | None:
    return load().get(asset_id)


# ------------------------------------------------------------------- licence
def licence_ok(lic: str) -> bool:
    s = (lic or "").lower()
    if not s:
        return False
    if any(b in s for b in NONFREE):
        return False
    return any(a in s for a in FREE)


# -------------------------------------------------------------------- HTTP
def _get(url: str, timeout: int = 45) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _api(params: dict) -> dict:
    params = dict(params, format="json", formatversion="2")
    url = COMMONS + "?" + urllib.parse.urlencode(params)
    return json.loads(_get(url).decode("utf-8"))


def _strip_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = s.replace("&amp;", "&").replace("&nbsp;", " ").replace("&quot;", '"')
    return re.sub(r"\s+", " ", s).strip()


# ------------------------------------------------------------------- search
def search(query: str, limit: int = 12) -> list[dict]:
    """Search Commons' File namespace; return candidates with licence info."""
    res = _api({"action": "query", "list": "search", "srsearch": query,
                "srnamespace": 6, "srlimit": limit})
    titles = [h["title"] for h in res.get("query", {}).get("search", [])]
    if not titles:
        return []
    out = []
    for chunk in (titles[i:i + 10] for i in range(0, len(titles), 10)):
        info = _api({"action": "query", "titles": "|".join(chunk),
                     "prop": "imageinfo",
                     "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 900})
        for page in info.get("query", {}).get("pages", []):
            ii = (page.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata", {})
            lic = _strip_html(em.get("LicenseShortName", {}).get("value", ""))
            out.append({
                "title": page.get("title", ""),
                "license": lic,
                "free": licence_ok(lic),
                "author": _strip_html(em.get("Artist", {}).get("value", "")),
                "mime": ii.get("mime", ""),
                "width": ii.get("width", 0),
                "height": ii.get("height", 0),
                "page": ii.get("descriptionurl", ""),
                "desc": _strip_html(em.get("ImageDescription", {}).get("value", ""))[:180],
            })
    order = {t: i for i, t in enumerate(titles)}
    out.sort(key=lambda r: order.get(r["title"], 99))
    return out


# -------------------------------------------------------------------- fetch
def _clean_url(u: str) -> str:
    """Drop the API's analytics query string; keep the bare file URL."""
    return u.split("?")[0] if u else u


def get_commons(asset_id: str, title: str, width: int = 1400,
                force: bool = False) -> dict:
    """Fetch one Commons file into assets/<asset_id> and register its credit."""
    if asset_id in load() and not force and path_for(asset_id):
        return load()[asset_id]
    if not title.lower().startswith("file:"):
        title = "File:" + title
    info = _api({"action": "query", "titles": title, "prop": "imageinfo",
                 "iiprop": "url|size|mime|extmetadata", "iiurlwidth": width})
    pages = info.get("query", {}).get("pages", [])
    if not pages or "missing" in pages[0]:
        raise SystemExit(f"no such Commons file: {title}")
    page = pages[0]
    ii = (page.get("imageinfo") or [{}])[0]
    em = ii.get("extmetadata", {})
    lic = _strip_html(em.get("LicenseShortName", {}).get("value", ""))
    if not licence_ok(lic):
        raise SystemExit(f"REFUSED (licence {lic!r} not free): {title}")

    url = _clean_url(ii.get("thumburl") or ii.get("url"))
    data = _get(url)
    if len(data) > MAX_BYTES:                      # step down once, then give up
        info2 = _api({"action": "query", "titles": title, "prop": "imageinfo",
                      "iiprop": "url", "iiurlwidth": max(800, width // 2)})
        url2 = _clean_url((info2["query"]["pages"][0]["imageinfo"][0]).get("thumburl"))
        if url2:
            url, data = url2, _get(url2)
    ext = ".png" if url.lower().endswith(".png") else \
          (".jpg" if url.lower().endswith((".jpg", ".jpeg")) else
           ("." + url.rsplit(".", 1)[-1].lower() if "." in url.rsplit("/", 1)[-1] else ".png"))
    rel = asset_id + ext
    dest = os.path.join(ASSETS, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)

    author = _strip_html(em.get("Artist", {}).get("value", "")) or "Unknown author"
    rec = {
        "file": rel,
        "title": re.sub(r"^File:", "", page["title"]).rsplit(".", 1)[0],
        "author": author[:160],
        "license": lic,
        "license_url": _strip_html(em.get("LicenseUrl", {}).get("value", "")),
        "source": "Wikimedia Commons",
        "page": ii.get("descriptionurl", ""),
        "credit": _strip_html(em.get("Credit", {}).get("value", ""))[:160],
        "fetched": datetime.date.today().isoformat(),
        "bytes": len(data),
        "sha1": hashlib.sha1(data).hexdigest()[:16],
    }
    with _Lock():
        reg = load()
        reg[asset_id] = rec
        save(reg)
    return rec


def get_url(asset_id: str, url: str, title: str, author: str, license: str,
            license_url: str = "", page: str = "", source: str = "",
            force: bool = False) -> dict:
    """Register an image from a non-Commons free source; attribution supplied."""
    if asset_id in load() and not force and path_for(asset_id):
        return load()[asset_id]
    if not licence_ok(license):
        raise SystemExit(f"REFUSED (licence {license!r} not free)")
    data = _get(url)
    tail = url.split("?")[0].rsplit("/", 1)[-1]
    ext = "." + tail.rsplit(".", 1)[-1].lower() if "." in tail else ".png"
    rel = asset_id + ext
    dest = os.path.join(ASSETS, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)
    rec = {"file": rel, "title": title, "author": author, "license": license,
           "license_url": license_url, "source": source or "Web",
           "page": page or url, "credit": "",
           "fetched": datetime.date.today().isoformat(),
           "bytes": len(data), "sha1": hashlib.sha1(data).hexdigest()[:16]}
    with _Lock():
        reg = load()
        reg[asset_id] = rec
        save(reg)
    return rec


# ------------------------------------------------------------------- credits
def credit_line(asset_id: str) -> str:
    """One plain-text attribution line, as the licence requires."""
    r = record(asset_id)
    if not r:
        return f"[missing credit for {asset_id}]"
    bits = [f'“{r["title"]}”']
    if r.get("author") and r["author"].lower() != "unknown author":
        bits.append(r["author"])
    bits.append(r.get("license") or "licence unknown")
    if r.get("source"):
        bits.append(r["source"])
    return " · ".join(bits)


# ----------------------------------------------------------------------- CLI
def _cli(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("-n", type=int, default=12)
    g = sub.add_parser("get"); g.add_argument("id"); g.add_argument("title")
    g.add_argument("--width", type=int, default=1400); g.add_argument("--force", action="store_true")
    u = sub.add_parser("geturl")
    u.add_argument("id"); u.add_argument("url")
    u.add_argument("--title", required=True); u.add_argument("--author", required=True)
    u.add_argument("--license", required=True); u.add_argument("--license-url", default="")
    u.add_argument("--page", default=""); u.add_argument("--source", default="")
    u.add_argument("--force", action="store_true")
    l = sub.add_parser("list"); l.add_argument("prefix", nargs="?", default="")
    sub.add_parser("verify")
    a = ap.parse_args(argv)

    if a.cmd == "search":
        for r in search(a.query, a.n):
            flag = "FREE" if r["free"] else "----"
            print(f"{flag}  {r['title']}\n      {r['license']} | {r['width']}x{r['height']} "
                  f"{r['mime']} | {r['author'][:60]}\n      {r['desc'][:150]}")
    elif a.cmd == "get":
        r = get_commons(a.id, a.title, a.width, a.force)
        print(f"{a.id} -> assets/{r['file']}  ({r['bytes']/1000:.0f} kB)  {r['license']}")
    elif a.cmd == "geturl":
        r = get_url(a.id, a.url, a.title, a.author, a.license, a.license_url,
                    a.page, a.source, a.force)
        print(f"{a.id} -> assets/{r['file']}  ({r['bytes']/1000:.0f} kB)  {r['license']}")
    elif a.cmd == "list":
        reg = load()
        for k in sorted(reg):
            if k.startswith(a.prefix):
                print(f"{k:38} {reg[k]['license'][:28]:30} {reg[k]['file']}")
        print(f"— {sum(1 for k in reg if k.startswith(a.prefix))} assets")
    elif a.cmd == "verify":
        reg, bad = load(), 0
        for k, r in sorted(reg.items()):
            if not os.path.exists(os.path.join(ASSETS, r["file"])):
                print(f"MISSING BYTES  {k} -> {r['file']}"); bad += 1
            if not licence_ok(r.get("license", "")):
                print(f"NON-FREE       {k} -> {r.get('license')}"); bad += 1
            if not r.get("page"):
                print(f"NO SOURCE URL  {k}"); bad += 1
        print(f"{len(reg)} assets, {bad} problems")
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
