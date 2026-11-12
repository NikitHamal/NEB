#!/usr/bin/env python3
"""Refresh only the `bca-course-*` entries of manifest.json from the rebuilt BCA PDFs.

`build_manifest.py` rewrites every book (school, entrance and BCA) and re-renders all covers.
After a BCA-only rebuild that is more churn than needed, so this script re-reads the BCA registry,
re-counts pages and sizes from the built PDFs, rewrites each listing description (units, pages,
topics) and re-renders the 16:9 cover only for the entries that changed.

    /tmp/v/bin/python tools/publish/refresh_bca_manifest.py [--no-cover]

Then (credentials in the environment, never in the repo):
    python tools/publish/update_books.py --dry-run --only bca-course-semester-1-professional-communication-ethics
    python tools/publish/update_books.py          --only bca-course-semester-1-professional-communication-ethics
    python manage.py approve_book_uploads <username> --yes      # on the server
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_manifest as bm  # noqa: E402


def main():
    no_cover = "--no-cover" in sys.argv
    path = os.path.join(HERE, "manifest.json")
    data = json.load(open(path, encoding="utf-8"))
    by_slug = {b["slug"]: b for b in data["books"]}
    changed = []
    for e in bm.course_entries():
        old = by_slug.get(e["slug"])
        if old is None:
            continue
        pdf = bm.pdf_for(e)
        if not os.path.exists(pdf):
            continue
        pages, size = bm.pdf_info(pdf)
        desc = bm.describe(e, pages)
        if (old.get("pages"), old.get("description")) == (pages, desc) and old.get("size") == size:
            continue
        old_pages = old.get("pages")
        old.update(pages=pages, size=size, description=desc)
        old["tags"] = ", ".join(dict.fromkeys(t for t in e["tags"] if t))
        if not no_cover:
            old["cover"] = bm.cover(pdf, e["slug"]).replace(os.sep, "/")
        changed.append((e["slug"], old_pages, pages))
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for slug, a, b in changed:
        print(f"{slug}: {a} -> {b} pages")
    print(f"{len(changed)} BCA listings refreshed")


if __name__ == "__main__":
    main()
