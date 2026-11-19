"""Listings and covers for the NEBians Class 8 BLE (Basic Level Examination) solved papers.

    python tools/publish/build_class8_listings.py     # merges into papers_listing.json, writes paper_covers/

Add one dict to PAPERS per new paper (id = notes/papers/content id). The page count comes from the built PDF.
exam_type is "Final" (BLE is the end-of-year exam of Class 8, set by each municipality), type stays "Past Paper".
"""
import io, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_papers as bp
from PIL import Image, ImageDraw
import pymupdf

REPO = bp.REPO
PAPERS = [
    {"id": "8-math-ble-2082-kathmandu", "file": "NEBians-BLE-Past-Paper-Grade-8-Mathematics-2082-Kathmandu.pdf",
     "subject": "Mathematics", "year_bs": "2082", "year_ad": "2026", "muni": "Kathmandu Metropolitan City",
     "district": "Kathmandu", "pradesh": "Bagmati", "marks": "50", "time": "2 hours",
     "topics": "sets, number systems, ratio, simple interest, direct and indirect variation, area of a trapezium, indices, "
               "quadratic expressions, algebraic tiles, coordinates and reflection, tessellation and the square pyramid, "
               "construction of a rectangle, and mean"},
    {"id": "8-eng-ble-2082-kathmandu", "file": "NEBians-BLE-Past-Paper-Grade-8-English-2082-Kathmandu.pdf",
     "subject": "English", "year_bs": "2082", "year_ad": "2026", "muni": "Kathmandu Metropolitan City",
     "district": "Kathmandu", "pradesh": "Bagmati", "marks": "50", "time": "2 hours",
     "topics": "reading comprehension (formal request letter, natural habitat passage, vacancy advertisement, and unseen passage on friendship), "
               "punctuation and error correction, pie-chart interpretation (crop production of Dang), essay writing (advantages and disadvantages "
               "of using mobile phones), sentence transformation (question tag, negative, passive voice, tense, indirect speech), and grammar cloze"},
]
COMMON = "BLE, basic level examination, class 8, grade 8, past paper, solved paper, with solutions, Nepal, 2082, 2026"


def cover(big, sub, foot, out):
    img = Image.new("RGB", (1280, 720), bp.PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 1279, 719], outline=bp.LINE, width=2)
    d.rectangle([56, 96, 62, 130], fill=bp.BLUE)
    d.text((80, 96), "NEBIANS", font=bp.font(30, "bold"), fill=bp.NAVY)
    d.text((80, 146), "Class 8 BLE Past Paper", font=bp.font(34, "reg"), fill=bp.INK)
    d.text((78, 236), big, font=bp.fit(d, big, 1100, 96), fill=bp.NAVY)
    d.text((80, 400), "2082", font=bp.font(120, "bold"), fill=bp.BLUE)
    d.text((80, 548), sub, font=bp.font(32, "reg"), fill=bp.INK)
    d.text((80, 600), "Full solutions included", font=bp.font(32, "bold"), fill=bp.BLUE)
    d.rectangle([0, 668, 1279, 719], fill=bp.NAVY)
    d.text((80, 680), "nebians.consica.com.np", font=bp.font(24, "semi"), fill=(255, 255, 255))
    t = foot
    d.text((1200 - int(d.textlength(t, font=bp.font(24, "reg"))), 680), t, font=bp.font(24, "reg"), fill=(190, 205, 225))
    img.save(out, "JPEG", quality=88, optimize=True)


def main():
    out = []
    cdir = os.path.join(HERE, "paper_covers")
    os.makedirs(cdir, exist_ok=True)
    for p in PAPERS:
        s, y = p["subject"], p["year_bs"]
        pdf = "notes/papers/pdf/" + p["file"]
        pages = len(pymupdf.open(os.path.join(REPO, pdf)))
        title = "NEB Class 8 %s BLE Past Paper %s (%s) %s with Solutions" % (s, y, p["year_ad"], p["muni"])
        desc = ("The Class 8 Basic Level Examination (BLE) %s paper of %s for %s BS (%s AD), %s marks and %s, re-typeset in English "
                "with a full worked solution for every question and sub-part, marks shown beside each step and diagrams where the "
                "question needs one. It covers %s. Use it as a timed mock for your BLE and then check each answer against the "
                "solutions. Free to read in the browser."
                % (s, p["muni"], y, p["year_ad"], p["marks"], p["time"], p["topics"]))
        tags = ["NEB", "BLE", "Class 8", s, "BLE %s %s" % (s, y), p["muni"], "%s past paper" % p["district"], COMMON]
        it = {"slug": p["id"], "title": title, "description": desc, "subject": s, "grade_level": "Class 8", "year": y,
              "exam_type": "Final", "type": "Past Paper", "faculty": "", "program": "", "pradesh": p["pradesh"],
              "district": p["district"], "school": "", "author_name": "NEBians",
              "source_label": "BLE paper of %s, re-typeset with NEBians solutions" % p["muni"],
              "tags": ", ".join(tags), "pdf": pdf, "cover": "tools/publish/paper_covers/%s.jpg" % p["id"]}
        cover(s, "%s  ·  %s marks  ·  %s" % (p["muni"], p["marks"], p["time"]), "%d page PDF" % pages,
              os.path.join(REPO, it["cover"]))
        out.append(it)
    lp = os.path.join(HERE, "papers_listing.json")
    old = json.load(io.open(lp, encoding="utf-8"))
    keep = [x for x in old if x["slug"] not in {y["slug"] for y in out}]
    json.dump(keep + out, io.open(lp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(len(out), "listings merged;", len(keep + out), "total;", [x["slug"] for x in out])


main()
