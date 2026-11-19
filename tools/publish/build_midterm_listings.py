"""Listings and covers for the NEBians Class 11 mid-term practice papers (and their stream bundles).

    python tools/publish/build_midterm_listings.py        # merges into papers_listing.json, writes paper_covers/

Mid-term exams are set by each school, so these are original NEBians papers in the NEB pattern, not copies of any
school paper. exam_type is "Midterm", type stays "Past Paper" so the Past Paper filter finds them.
"""
import io, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_papers as bp
from PIL import Image, ImageDraw

REPO = bp.REPO
MAN = json.load(io.open(os.path.join(REPO, "notes", "papers", "manifest.json"), encoding="utf-8"))
BUN = json.load(io.open(os.path.join(REPO, "notes", "papers", "bundles.json"), encoding="utf-8"))
PAPERS = [m for m in MAN if str(m.get("id", "")).startswith("11-") and m.get("id", "").endswith("-mid-2083")]
UNITS = {"Physics": "Physical Quantities, Vectors, Kinematics, Dynamics, Work Energy and Power, Circular Motion",
         "Chemistry": "Foundation and Fundamentals, Stoichiometry, Atomic Structure, Periodic Table, Chemical Bonding",
         "Mathematics": "Logic and Set, Real Numbers, Functions, Curve Sketching, Sequence and Series, Matrices and Determinants",
         "Computer Science": "Computer System, Number System and Boolean Logic, Software and Operating System, Application Package",
         "Biology": "Biomolecules and Cell Biology, Floral Diversity, Introductory Microbiology, Ecology"}
STREAM = {"Physics": "Science", "Chemistry": "Science", "Mathematics": "Science",
          "Computer Science": "Science with Computer Science", "Biology": "Science with Biology"}
COMMON = "mid term, midterm, first terminal exam, internal exam, school exam, practice paper, model question, solved paper, with solutions, NEB, 2083, 2026, Nepal"


def cover(title_top, big, sub, foot, out):
    img = Image.new("RGB", (1280, 720), bp.PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 1279, 719], outline=bp.LINE, width=2)
    d.rectangle([56, 96, 62, 130], fill=bp.BLUE)
    d.text((80, 96), "NEBIANS", font=bp.font(30, "bold"), fill=bp.NAVY)
    d.text((80, 146), title_top, font=bp.font(34, "reg"), fill=bp.INK)
    d.text((78, 236), big, font=bp.fit(d, big, 1100, 96), fill=bp.NAVY)
    d.text((80, 400), "Mid-Term", font=bp.font(120, "bold"), fill=bp.BLUE)
    d.text((80, 548), sub, font=bp.font(32, "reg"), fill=bp.INK)
    d.text((80, 600), "Full solutions included", font=bp.font(32, "bold"), fill=bp.BLUE)
    d.rectangle([0, 668, 1279, 719], fill=bp.NAVY)
    d.text((80, 680), "nebians.consica.com.np", font=bp.font(24, "semi"), fill=(255, 255, 255))
    t = foot
    d.text((1200 - int(d.textlength(t, font=bp.font(24, "reg"))), 680), t, font=bp.font(24, "reg"), fill=(190, 205, 225))
    img.save(out, "JPEG", quality=88, optimize=True)


def base(slug, title, desc, subject, tags, pdf):
    return {"slug": slug, "title": title, "description": desc, "subject": subject, "grade_level": "Class 11",
            "year": "2083", "exam_type": "Midterm", "type": "Past Paper", "faculty": "Science", "program": "",
            "author_name": "NEBians", "source_label": "Original NEBians mid-term practice paper in the NEB pattern, with solutions",
            "tags": ", ".join(tags), "pdf": pdf.replace("\\", "/"),
            "cover": "tools/publish/paper_covers/%s.jpg" % slug}


def main():
    out, cdir = [], os.path.join(HERE, "paper_covers")
    for p in sorted(PAPERS, key=lambda m: m["id"]):
        s = p["subject"]
        title = "NEB Class 11 %s Mid-Term Question Paper 2083 (2026) %s Practice Paper with Solutions" % (s, STREAM[s])
        desc = ("A complete Class 11 %s mid-term (first terminal) question paper of %s marks and %s, written in the NEB new-course "
                "pattern: Group A multiple choice (10 x 1), Group B short answers (6 x 4) and Group C long answers (2 x 8). "
                "It covers %s. Mid-term exams are set by each school, so this is an original NEBians practice paper, not a copy "
                "of any school's paper. Every question is followed by a worked solution with the answer key, numericals and diagrams, "
                "so you can sit it under exam time and then check each answer. Free to read in the browser."
                % (s, p["marks"], p["time"], UNITS[s]))
        tags = ["NEB", "Class 11", s, "mid term question paper", "Class 11 %s mid term" % s, STREAM[s].lower(), COMMON]
        it = base(p["id"], title, desc, s, tags, "notes/papers/pdf/" + p["file"])
        bp.os.makedirs(cdir, exist_ok=True)
        cover("Class 11 Mid-Term Practice Paper", s, "%s marks  ·  %s  ·  2083 BS" % (p["marks"], p["time"]), "%s page PDF" % p["pages"],
              os.path.join(REPO, it["cover"]))
        out.append(it)
    for b in BUN:
        if not b.get("slug", "").startswith("11-science-") or not b["slug"].endswith("-mid-2083"):
            continue
        cs = "cs" in b["slug"]
        stream = "Science with Computer Science" if cs else "Science with Biology"
        subs = [next(m["subject"] for m in PAPERS if m["id"] == i) for i in b["papers"]]
        title = "NEB Class 11 %s Mid-Term Question Papers 2083 (2026) Bundle with Solutions: %s" % (stream, ", ".join(subs))
        desc = ("Four Class 11 mid-term (first terminal) practice papers for the %s stream in one PDF: %s. Each paper is 50 marks, "
                "2 hours, in the NEB new-course pattern, and is followed by full worked solutions. A contents page and PDF bookmarks "
                "take you to each paper. These are original NEBians papers, not copies of any school's paper, because mid-term "
                "exams are set by each school. Free to read in the browser." % (stream.lower(), ", ".join(subs)))
        tags = ["NEB", "Class 11", stream.lower(), "mid term question paper bundle", "mid term papers"] + subs + [COMMON]
        it = base(b["slug"] + "-bundle", title, desc, stream, tags, "notes/papers/pdf/" + b["file"])
        cover("Class 11 Mid-Term Papers", stream, "4 papers  ·  50 marks each  ·  2083 BS", "%s page PDF" % b["pages"],
              os.path.join(REPO, it["cover"]))
        out.append(it)
    lp = os.path.join(HERE, "papers_listing.json")
    old = json.load(io.open(lp, encoding="utf-8"))
    keep = [x for x in old if x["slug"] not in {y["slug"] for y in out}]
    json.dump(keep + out, io.open(lp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for x in out:
        assert os.path.exists(os.path.join(REPO, x["pdf"])), x["pdf"]
    print(len(out), "listings merged;", len(keep + out), "total;", [x["slug"] for x in out])


main()
