#!/usr/bin/env python3
"""Replace the thumbnail of books that are already in the library with the 16:9 covers in covers/.

The first uploads sent the portrait first page, which a 16:9 card crops. `covers/<slug>.jpg` are now 1280 x 720
(notes/pipeline/thumb.py). This PATCHes each existing resource owned by the signed-in account with its new cover;
nothing else on the listing changes. Standard library only.

    export NEB_EMAIL=... NEB_PASSWORD=...        # or NEB_TOKEN; NEB_BASE_URL defaults to the live site
    python tools/publish/update_covers.py --dry-run
    python tools/publish/update_covers.py                  # every book found by title
    python tools/publish/update_covers.py --only math11 cs8

A book is found through published.json (slug -> resource id) when present, else by exact title search.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import publish_books as pb  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", nargs="*", default=[])
    args = ap.parse_args()
    base = os.environ.get("NEB_BASE_URL", "https://nebians.consica.com.np").rstrip("/")
    manifest = json.load(open(os.path.join(HERE, "manifest.json"), encoding="utf-8"))["books"]
    state = json.load(open(pb.STATE)) if os.path.exists(pb.STATE) else {}
    books = [b for b in manifest if not args.only or b["slug"] in args.only]
    token = None if args.dry_run else pb.sign_in(base)
    done = missing = 0
    for b in books:
        cover = os.path.join(HERE, b["cover"])
        rid = state.get(b["slug"])
        if not rid and not args.dry_run:
            rid = pb.already_listed(base, token, b["title"])
        if args.dry_run:
            print(f"would update {b['slug']:60s} {os.path.getsize(cover) // 1024} KB")
            continue
        if not rid:
            print(f"not in library: {b['slug']}")
            missing += 1
            continue
        body, ctype = pb.multipart({}, {"thumbnail": cover})
        status, res = pb.call(base, "PATCH", f"/api/resources/{rid}/", token=token, body=body, content_type=ctype)
        if status == 200:
            done += 1
            print(f"updated {b['slug']}")
        else:
            print(f"FAILED {b['slug']} ({status}): {res.get('error', res)}")
    print(f"{done} updated, {missing} not found")


if __name__ == "__main__":
    main()
