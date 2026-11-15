#!/usr/bin/env python3
"""Build the library listings and 16:9 covers for the rebuilt NEB past papers.

Source of truth is notes/papers/manifest.json (written by notes/papers/build_paper.py), so nothing
about a paper is typed here twice. Output:

    tools/publish/papers_listing.json      one listing per paper, ready for api.import_past_papers
    tools/publish/paper_covers/<id>.jpg    1280 x 720 cover, drawn with Pillow

Usage (from the repo root):
    python tools/publish/build_papers.py                # all grade 12 papers
    python tools/publish/build_papers.py --grade 10      # another grade
    python tools/publish/build_papers.py --only 12-phy-2082-general
"""
import argparse
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
PAPERS = os.path.join(REPO, "notes", "papers")
OUT = os.path.join(HERE, "papers_listing.json")
COVERS = os.path.join(HERE, "paper_covers")

FACULTY = {
    "Physics": "Science",
    "Chemistry": "Science",
    "Biology": "Science",
    "Mathematics": "Science",
    "Computer Science": "Science",
    "Accounting": "Management",
    "Business Studies": "Management",
    "Business Mathematics": "Management",
    "Economics": "Management",
    "Marketing": "Management",
    "Finance": "Management",
    "Hotel Management": "Management",
    "Social Studies": "Humanities",
}

GRADE_LABEL = {"8": "Class 8", "9": "Class 9", "10": "Class 10 / SEE", "11": "Class 11", "12": "Class 12"}

NAVY = (11, 27, 51)
INK = (60, 72, 88)
BLUE = (37, 99, 235)
PAPER = (247, 249, 252)
LINE = (214, 221, 232)


def font(size, weight="bold"):
    """Poppins if it is on the machine, Segoe UI otherwise. Cover art only, never the PDF."""
    names = {"bold": ["Poppins-Bold.ttf", "segoeuib.ttf", "arialbd.ttf"],
             "semi": ["Poppins-SemiBold.ttf", "seguisb.ttf", "arial.ttf"],
             "reg": ["Poppins-Regular.ttf", "segoeui.ttf", "arial.ttf"]}
    homes = [os.path.join(HERE, "fonts"), os.path.expanduser("~/.fonts"), os.path.expanduser("~/.local/share/fonts"),
             "/usr/share/fonts/truetype/google-fonts", "C:/Windows/Fonts"]
    from PIL import ImageFont
    for name in names[weight]:
        for home in homes:
            path = os.path.join(home, name)
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except OSError:
                    continue
    return ImageFont.load_default()


def fit(draw, text, max_width, start, weight="bold"):
    size = start
    while size > 24:
        f = font(size, weight)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 4
    return font(24, weight)


def cover(paper, out_path):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (1280, 720), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 1279, 719], outline=LINE, width=2)
    d.rectangle([56, 96, 62, 130], fill=BLUE)
    d.text((80, 96), "NEBIANS", font=font(30, "bold"), fill=NAVY)
    label = "%s Board Paper" % GRADE_LABEL.get(str(paper["grade"]), "Grade " + str(paper["grade"]))
    d.text((80, 146), label, font=font(34, "reg"), fill=INK)

    subject = paper["subject"]
    f = fit(d, subject, 780, 96)
    d.text((78, 236), subject, font=f, fill=NAVY)

    year = paper.get("year_bs") or ""
    ad = paper.get("year_ad") or ""
    d.text((78, 380), year, font=font(150, "bold"), fill=BLUE)
    if ad:
        d.text((84 + int(d.textlength(year, font=font(150, "bold"))), 452), "(%s)" % ad,
               font=font(40, "semi"), fill=INK)

    detail = []
    if paper.get("code"):
        detail.append("Code %s" % paper["code"].strip())
    if paper.get("marks"):
        detail.append("%s marks" % paper["marks"])
    if paper.get("time"):
        detail.append(paper["time"])
    d.text((80, 578), "  ·  ".join(detail), font=font(32, "reg"), fill=INK)
    d.text((80, 630), "Full solutions included", font=font(32, "bold"), fill=BLUE)
    d.rectangle([0, 668, 1279, 719], fill=NAVY)
    d.text((80, 680), "nebians.consica.com.np", font=font(24, "semi"), fill=(255, 255, 255))
    d.text((1200 - int(d.textlength("%s page PDF" % paper.get("pages", ""), font=font(24, "reg"))), 680),
           "%s page PDF" % paper.get("pages", ""), font=font(24, "reg"), fill=(190, 205, 225))
    img.save(out_path, "JPEG", quality=88, optimize=True)


def title_for(paper, dupe):
    """Keyword first, then the exact set, so a search for a subject and a year lands here."""
    base = "NEB %s %s Past Paper %s (%s)" % (
        GRADE_LABEL.get(str(paper["grade"]), "Grade " + str(paper["grade"])),
        paper["subject"], paper.get("year_bs", ""), paper.get("year_ad", ""))
    if dupe:
        label = stream_label(paper)
        if label:
            base += " " + label
    return base + " with Solutions"


def stream_label(paper):
    """A short, readable stream name for the papers that share a subject and a year."""
    s = (paper.get("stream") or "")
    for noise in ("(New course)", "(Old course)", "(new course)", "(old course)"):
        s = s.replace(noise, "")
    s = " ".join(s.replace(",", " ").split())
    if not s:
        return ""
    low = s.lower()
    if low.startswith("technical"):
        return "Technical Stream"
    if low.startswith("general"):
        return "General Stream"
    if low.startswith("old course"):
        return "Old Course"
    if low.startswith("optional"):
        return "Optional Set"
    return s


def description_for(paper):
    bits = []
    label = GRADE_LABEL.get(str(paper["grade"]), "Grade " + str(paper["grade"]))
    when = paper.get("year_bs", "")
    if paper.get("year_ad"):
        when += " (%s)" % paper["year_ad"]
    bits.append("The complete NEB %s %s board question paper of %s, re-typeset in full from the printed exam."
                % (label, paper["subject"], when))
    facts = []
    if paper.get("code"):
        facts.append("code %s" % paper["code"].strip())
    if paper.get("marks"):
        facts.append("%s marks" % paper["marks"])
    if paper.get("time"):
        facts.append("%s" % paper["time"])
    if facts:
        bits.append("The paper is %s." % ", ".join(facts))
    if paper.get("stream"):
        bits.append("Set for %s." % paper["stream"].rstrip("."))
    bits.append("Every question is followed by a worked solution, so you can sit the paper under exam time "
                "and then check each answer line by line. Free to read in the browser.")
    if paper.get("students"):
        bits.append(paper["students"].rstrip(".") + ".")
    return " ".join(bits)


def listing_for(paper, dupe):
    subject = paper["subject"]
    tags = ["NEB", GRADE_LABEL.get(str(paper["grade"]), "Grade"), subject, "past paper", "board exam",
            paper.get("year_bs", ""), paper.get("year_ad", ""), "solved paper", "with solutions", "Nepal"]
    if "Technical" in (paper.get("stream") or ""):
        tags.append("technical stream")
    return {
        "slug": paper["id"],
        "title": title_for(paper, dupe),
        "description": description_for(paper),
        "subject": subject,
        "grade_level": GRADE_LABEL.get(str(paper["grade"]), "Other"),
        "year": paper.get("year_bs", ""),
        "exam_type": "Board",
        "type": "Past Paper",
        "faculty": FACULTY.get(subject, ""),
        "program": "",
        "author_name": "National Examinations Board (NEB)",
        "source_label": "NEB board paper, re-typeset and solved by NEBians",
        "tags": ", ".join([t for t in tags if t]),
        "pdf": os.path.join("notes", "papers", "pdf", paper["file"]),
        "cover": os.path.join("tools", "publish", "paper_covers", paper["id"] + ".jpg"),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--grade", default="12")
    ap.add_argument("--only", nargs="*", default=[])
    ap.add_argument("--no-covers", action="store_true")
    args = ap.parse_args()

    papers = json.load(io.open(os.path.join(PAPERS, "manifest.json"), encoding="utf-8"))
    papers = [p for p in papers if str(p.get("grade")) == str(args.grade)]
    if args.only:
        papers = [p for p in papers if p["id"] in args.only]
    papers.sort(key=lambda p: (p["subject"], p.get("year_bs", ""), p["id"]))

    seen = {}
    for p in papers:
        seen[(p["subject"], p.get("year_bs"))] = seen.get((p["subject"], p.get("year_bs")), 0) + 1

    listings = []
    missing = []
    for p in papers:
        pdf = os.path.join(REPO, "notes", "papers", "pdf", p["file"])
        if not os.path.exists(pdf):
            missing.append(p["id"])
            continue
        item = listing_for(p, seen[(p["subject"], p.get("year_bs"))] > 1)
        if not args.no_covers:
            os.makedirs(COVERS, exist_ok=True)
            cover(p, os.path.join(REPO, item["cover"]))
        listings.append(item)

    json.dump(listings, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("%d listings written to %s" % (len(listings), os.path.relpath(OUT, REPO)))
    if missing:
        print("PDF missing for:", " ".join(missing), file=sys.stderr)
        return 1
    titles = [x["title"] for x in listings]
    if len(set(titles)) != len(titles):
        print("duplicate titles:", [t for t in titles if titles.count(t) > 1][:3], file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
