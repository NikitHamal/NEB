#!/usr/bin/env python3
"""Refresh already-published library resources with rebuilt PDFs, covers and listing text.

Companion to publish_books.py. That script creates the listings once; this one compares each book's
PDF, cover and listing fields on disk with the versions recorded in published_files.json (written by
this script's --seed and after every successful update) and PATCHes only what changed. The edit
endpoint puts a resource back in `pending`, so approve again on the server:

    python manage.py approve_book_uploads <username> --yes

Credentials (environment, never in the repo):
    NEB_TOKEN                   an authToken for the account that owns the books, or
    NEB_EMAIL, NEB_PASSWORD     sign in with that account
    NEB_BASE_URL                default https://nebians.consica.com.np

Usage (run from the repo root):
    python tools/publish/update_books.py --seed          # record what is uploaded now (once)
    python tools/publish/update_books.py --dry-run       # show what changed, touch nothing
    python tools/publish/update_books.py                 # upload every changed file/field
    python tools/publish/update_books.py --only phy11 cee-phy
"""
import argparse
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import publish_books as pub

HERE = pub.HERE
STATE = os.path.join(HERE, "published_files.json")


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fields_of(b):
    return {k: b.get(k, "") for k in pub.FIELDS}


def fields_md5(b):
    blob = json.dumps(fields_of(b), sort_keys=True, ensure_ascii=False).encode()
    return hashlib.md5(blob).hexdigest()


def book_files(b, repo):
    pdf = os.path.join(repo, b["file"])
    cover = os.path.join(HERE, b.get("cover", "")) if b.get("cover") else ""
    return pdf, cover


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--only", nargs="*", default=[], help="slugs to update")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--seed", action="store_true",
                    help="record the current files as already uploaded (no requests)")
    ap.add_argument("--no-cover", action="store_true", help="never send the cover image")
    ap.add_argument("--no-fields", action="store_true", help="keep listing text as published")
    ap.add_argument("--pause", type=float, default=2.0, help="seconds between updates")
    args = ap.parse_args()

    manifest = json.load(open(os.path.join(HERE, "manifest.json"), encoding="utf-8"))
    published_path = os.path.join(HERE, "published.json")
    if not os.path.exists(published_path):
        sys.exit("published.json missing: run publish_books.py first.")
    published = json.load(open(published_path))
    hashes = json.load(open(STATE)) if os.path.exists(STATE) else {}
    base = (os.environ.get("NEB_BASE_URL") or manifest["site"]).rstrip("/")

    books = [b for b in manifest["books"] if b["slug"] in published]
    if args.only:
        unknown = set(args.only) - {b["slug"] for b in books}
        if unknown:
            sys.exit("Not published: " + ", ".join(sorted(unknown)))
        books = [b for b in books if b["slug"] in args.only]

    if args.seed:
        for b in books:
            pdf, cover = book_files(b, pub.REPO)
            if not os.path.exists(pdf):
                print(b["slug"], "PDF missing:", b["file"])
                continue
            hashes[b["slug"]] = {
                "file": md5(pdf),
                "cover": md5(cover) if not args.no_cover and cover and os.path.exists(cover) else "",
                "fields": fields_md5(b),
            }
        json.dump(hashes, open(STATE, "w"), indent=1)
        print(f"recorded {len(books)} books in published_files.json")
        return

    token = None if args.dry_run else pub.sign_in(base)
    changed = uploaded = failed = 0
    for b in books:
        pdf, cover = book_files(b, pub.REPO)
        if not os.path.exists(pdf):
            print(b["slug"], "PDF missing:", b["file"])
            failed += 1
            continue
        prev = hashes.get(b["slug"], {})
        file_md5 = md5(pdf)
        cover_md5 = md5(cover) if not args.no_cover and cover and os.path.exists(cover) else ""
        fields_hash = fields_md5(b)
        files = {}
        if file_md5 != prev.get("file"):
            files["file"] = pdf
        if cover_md5 and cover_md5 != prev.get("cover"):
            files["thumbnail"] = cover
        fields_changed = not args.no_fields and fields_hash != prev.get("fields")
        if not files and not fields_changed:
            continue
        changed += 1
        detail = " + ".join(list(sorted(files)) + (["fields"] if fields_changed else []))
        if args.dry_run:
            print(b["slug"], "would update", detail)
            continue
        body, ctype = pub.multipart(fields_of(b) if fields_changed else {}, files)
        print(b["slug"], "updating", detail, f"{len(body) / 1048576:.1f} MB")
        status, res = pub.call(base, "PATCH", f"/api/resources/{published[b['slug']]}/",
                               token=token, body=body, content_type=ctype)
        if status not in (200, 201):
            print("   FAILED", status, res.get("error", res))
            failed += 1
            continue
        hashes[b["slug"]] = {"file": file_md5, "cover": cover_md5, "fields": fields_hash}
        json.dump(hashes, open(STATE, "w"), indent=1)
        uploaded += 1
        print("   updated (pending: approve with manage.py approve_book_uploads)")
        time.sleep(args.pause)
    print(f"\n{uploaded} updated, {changed - uploaded} changed but not uploaded, {failed} failed, "
          f"{len(books)} checked")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()