#!/usr/bin/env python3
"""Library listings for the IOE engineering past papers (branch note: content lives in
notes/papers/engineering, merged from claude/engineering).

Same contract as build_papers.py: the metadata is built from the authored files, never typed twice,
so a rebuilt paper cannot drift from its listing. The covers are drawn by notes/pipeline/thumb.py
(`python thumb.py --engineering`), the same m3x code that draws the book covers.

    python tools/publish/build_engineering.py               # write engineering_listing.json
    python tools/publish/build_engineering.py --only ioe-sh501-2081-bhadra
"""
import argparse
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "notes", "pipeline"))

import thumb  # noqa: E402  (engineering_papers parses the content front matter)

OUT = os.path.join(HERE, "engineering_listing.json")
COVERS = os.path.join(HERE, "paper_covers")
PDF_DIR = os.path.join(REPO, "notes", "papers", "engineering", "pdf")


def bs_year(year_bs):
    parts = (year_bs or "").split()
    return parts[0] if parts and parts[0].isdigit() else (year_bs or "")


def title_for(meta, dupe):
    base = "IOE %s Past Paper %s (%s)" % (meta.get("subject", ""), meta.get("year_bs", ""), meta.get("year_ad", ""))
    if dupe:
        extra = meta.get("code") or meta.get("stream") or ""
        if extra:
            base += ", %s" % extra
    return base + " with Solutions"


def description_for(meta):
    bits = ["The %s paper set by the Institute of Engineering, Tribhuvan University (IOE), "
            "for %s, re-typeset in full." % (meta.get("subject", "engineering"), meta.get("year_bs", ""))]
    facts = []
    if meta.get("code"):
        facts.append("code %s" % meta["code"])
    if meta.get("marks"):
        facts.append("%s marks" % meta["marks"])
    if meta.get("time"):
        facts.append(meta["time"])
    if facts:
        bits.append("The paper is %s." % ", ".join(facts))
    if meta.get("stream"):
        bits.append("For %s." % meta["stream"].rstrip("."))
    bits.append("Every question is followed by a worked solution, so you can attempt the paper under exam "
                "conditions and then check each step. Free to read in the browser.")
    if meta.get("students"):
        bits.append(meta["students"].rstrip(".") + ".")
    return " ".join(bits)


def listing_for(meta, dupe):
    subject = meta.get("subject", "")
    tags = ["IOE", "BE", "engineering", subject, "past paper", bs_year(meta.get("year_bs", "")),
            meta.get("year_ad", ""), "Tribhuvan University", "solved paper", "with solutions", "Nepal"]
    if meta.get("code"):
        tags.append(meta["code"])
    return {
        "slug": meta["slug"],
        "title": title_for(meta, dupe),
        "description": description_for(meta),
        "subject": subject,
        "grade_level": "Bachelors",
        "year": bs_year(meta.get("year_bs", "")),
        "exam_type": "Final",
        "type": "Past Paper",
        "faculty": "Engineering",
        "program": "BE",
        "author_name": "Institute of Engineering (IOE), Tribhuvan University",
        "source_label": "IOE exam paper, re-typeset and solved by NEBians",
        "tags": ", ".join([t for t in tags if t]),
        "pdf": os.path.join("notes", "papers", "engineering", "pdf", meta.get("file", "")),
        "cover": os.path.join("tools", "publish", "paper_covers", meta["slug"] + ".jpg"),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--only", nargs="*", default=[])
    args = ap.parse_args()

    papers = thumb.engineering_papers()
    slugs = sorted(papers)
    if args.only:
        slugs = [s for s in slugs if s in args.only]

    seen = {}
    for s in slugs:
        m = papers[s]
        key = (m.get("subject"), m.get("year_bs"))
        seen[key] = seen.get(key, 0) + 1

    listings, missing, no_cover = [], [], []
    for s in slugs:
        meta = dict(papers[s])
        pdf = os.path.join(PDF_DIR, meta.get("file", ""))
        if not meta.get("file") or not os.path.exists(pdf):
            missing.append(s)
            continue
        item = listing_for(meta, seen[(meta.get("subject"), meta.get("year_bs"))] > 1)
        if not os.path.exists(os.path.join(REPO, item["cover"])):
            no_cover.append(s)
        listings.append(item)

    titles = [x["title"] for x in listings]
    dupes = sorted({t for t in titles if titles.count(t) > 1})
    json.dump(listings, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("%d listings written to %s" % (len(listings), os.path.relpath(OUT, REPO)))
    if dupes:
        print("duplicate titles (%d): %s" % (len(dupes), "; ".join(dupes[:3])), file=sys.stderr)
    if no_cover:
        print("cover missing for %d papers (run: python thumb.py --engineering)" % len(no_cover), file=sys.stderr)
    if missing:
        print("PDF missing for %d papers: %s" % (len(missing), " ".join(missing[:5])), file=sys.stderr)
    return 1 if (missing or dupes) else 0


if __name__ == "__main__":
    sys.exit(main())
