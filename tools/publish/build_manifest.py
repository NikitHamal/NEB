#!/usr/bin/env python3
"""Write tools/publish/manifest.json (and covers/) for every built NEBians book.

The manifest is the one source of listing data for `publish_books.py`: title, description, level,
program, tags and the PDF path. It is generated from the spines and unit files (chapter counts and
titles), the built PDFs (pages, size) and the BCA registry, so nothing is typed twice and a rebuilt
book updates its own listing.

    /tmp/v/bin/python tools/publish/build_manifest.py        # needs pypdf + pymupdf (see PDF_M3X_STATUS.md)

Listing values follow api/education_catalog.py (levels '8', '11', '12', 'Bachelors', 'Entrance Prep').
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "notes", "pipeline"))
import spine  # noqa: E402

YEAR = "2082"
SCIENCE_PHYSICAL = {"phy", "chem", "math", "cs"}
NEPALI_NAMES = {"अनिवार्य नेपाली": "Compulsory Nepali", "नेपाली": "Nepali",
                "सामाजिक अध्ययन तथा मानव मूल्य शिक्षा": "Social Studies and Human Values Education",
                "स्वास्थ्य, शारीरिक तथा सिर्जनात्मक कला": "Health, Physical and Creative Arts"}
NEPALI_ORIG = {v: k for k, v in NEPALI_NAMES.items()}
ENTRANCE = {
    "cee": ("CEE", "MECEE medical entrance", "MBBS / BDS entrance", "CEE, MECEE, MBBS entrance, medical entrance Nepal"),
    "ioe": ("IOE", "IOE engineering entrance", "IOE entrance (Engineering)", "IOE, engineering entrance Nepal, BE entrance"),
    "bca": ("BCA", "BCA entrance (TU)", "BCA / BIT entrance", "BCA entrance, TU BCA, BCA entrance Nepal"),
}


def pdf_info(path):
    from pypdf import PdfReader
    return len(PdfReader(path).pages), os.path.getsize(path)


def cover(pdf, slug):
    import fitz
    out = os.path.join(HERE, "covers", slug + ".jpg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    page = fitz.open(pdf)[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(420 / page.rect.width, 420 / page.rect.width), alpha=False)
    pix.save(out, jpg_quality=82)
    return os.path.relpath(out, HERE)


def span(titles, n=4):
    """'A, B, C and D' (all of them when few), else the first n and 'more'."""
    titles = list(dict.fromkeys(titles))     # a question bank repeats a subject name per chapter
    if not titles:
        return ""
    if len(titles) <= n:
        return ", ".join(titles[:-1]) + " and " + titles[-1] if len(titles) > 1 else titles[0]
    return ", ".join(titles[:n]) + " and more"


def short(t):
    """'Unit 3: Health and Wellness' -> 'Health and Wellness'; long titles stop at the first colon or comma."""
    t = re.sub(r"^(?:Unit|Chapter|Lesson)\s*\d+\s*[:.\-]\s*", "", t.strip())
    t = re.split(r"[:,]| - ", t)[0].strip()
    return t if len(t) <= 48 else t[:48].rsplit(" ", 1)[0]


def units_of(slug):
    head, units = spine.load(slug)
    return head, [short(u["title"]) for u in units]


def course_units(folder):
    out = []
    for f in sorted(glob.glob(os.path.join(folder, "unit-*.md"))):
        m = re.search(r"^title:\s*[\"']?(.+?)[\"']?\s*$", open(f, encoding="utf-8").read(3000), re.M)
        if m:
            out.append(short(m.group(1)))
    return out


def clip(s, n):
    return s if len(s) <= n else s[:n - 1].rsplit(" ", 1)[0].rstrip(",;:") + "."


def school_entry(slug, pdf):
    name, _, grade = spine.meta_for(slug)
    key = re.match(r"([a-z]+)", slug).group(1)
    head, titles = units_of(slug)
    en = NEPALI_NAMES.get(name, name)
    nepali = name != en
    bank = key.startswith("qbank")
    level = {8: "Class 8", 10: "Class 10 / SEE", 11: "11", 12: "12"}[grade]
    klass = f"Class {grade}"
    seen = "SEE" if grade == 10 else "NEB" if grade >= 11 else "CDC"
    basis = "the NEB and CDC curriculum" if grade >= 11 else "the CDC curriculum" + (" for SEE" if grade == 10 else "")
    if bank:
        subject = {"qbank": "Question Bank", "qbankc": "Commerce", "qbankacc": "Accountancy", "qbankeco": "Economics"}[key]
        title = f"{klass} Question Bank: Practice with Solutions" if key == "qbank" else \
                f"{subject} Question Bank {klass}: Practice with Solutions"
        tags = [klass, "question bank", "practice questions", "model questions", seen, "Nepal"]
        exam = "SEE" if grade == 10 else "Board" if grade >= 11 else "Final"
    else:
        subject = en
        title = f"{en} {klass} Notes ({seen}): Chapter-wise"
        tags = [en, klass, "notes", "chapter-wise", seen, "Nepal"]
        exam = "Notes"
    if nepali:
        title = f"{en} ({name}) {klass} Notes" if not bank else title
        tags.append(name)
    program = ""
    faculty = ""
    if grade >= 11:
        if key in SCIENCE_PHYSICAL:
            program, faculty = "Science (Physical)", "Science"
        elif key == "bio":
            program, faculty = "Science (Biology)", "Science"
        if key == "cs":
            program = "Computer Science"
    return dict(slug=slug, kind="school", title=title, subject=subject, grade_level=level, program=program,
                faculty=faculty, exam_type=exam, tags=tags, titles=titles, count=len(titles), basis=basis)


def entrance_entry(slug, pdf):
    track, subj = spine.track_of(slug)
    short, exam_name, program, extra = ENTRANCE[track]
    name = spine.TRACK_SUBJECTS[subj][0]
    head, titles = units_of(slug)
    if subj == "mock":
        title = f"{short} Entrance Model Papers and Mock Tests"
        exam = "Mock"
    else:
        title = f"{short} Entrance {name}: Notes and Practice"
        exam = "Entrance"
    tags = [f"{short} entrance", name, exam_name, "entrance preparation", "Nepal"] + extra.split(", ")[:3]
    return dict(slug=slug, kind="entrance", title=title, subject=name, grade_level="Entrance Prep", program=program,
                faculty="", exam_type=exam, tags=tags, titles=titles, count=len(titles), basis=f"the {exam_name} syllabus")


def course_entries():
    reg = json.load(open(os.path.join(REPO, "bca", "course", "books.json"), encoding="utf-8"))
    for rel, meta in reg.items():
        if rel.startswith("_"):
            continue
        folder = os.path.join(REPO, "bca", "course", rel)
        slug = "bca-course-" + rel.replace("/", "-")
        titles = course_units(folder)
        if not titles:
            continue
        sem, code = meta["semester"], meta["code"]
        name = meta["name"]
        yield dict(slug=slug, kind="course", title=f"{name} ({code}): BCA Semester {sem} Notes",
                   subject=name, grade_level="Bachelors", program="BCA", faculty="Computer Science and IT",
                   exam_type="Notes",
                   tags=["BCA", f"BCA semester {sem}", name, code, "Tribhuvan University", "TU BCA syllabus", "Nepal"],
                   titles=titles, count=len(titles),
                   basis=f"the Tribhuvan University BCA syllabus ({meta.get('credits', 3)} credits)",
                   semester=sem, folder=rel)


def pdf_for(entry):
    slug = entry["slug"]
    if entry["kind"] == "course":
        sem = entry["semester"]
        return os.path.join(REPO, "bca", "course", f"semester-{sem}", "pdfs",
                            "NEBians-BCA-Course-Semester-%d-%s.pdf" % (sem, spine_course_name(entry)))
    if entry["kind"] == "entrance":
        bca = glob.glob(os.path.join(REPO, "bca", "entrance", "pdfs", spine.pdf_name(slug)))
        return bca[0] if bca else os.path.join(REPO, "notes", "pdf", spine.pdf_name(slug))
    return os.path.join(REPO, "notes", "pdf", spine.pdf_name(slug))


def spine_course_name(entry):
    sem = entry["semester"]
    want = entry["subject"].replace(" ", "-").replace("/", "-")
    for f in glob.glob(os.path.join(REPO, "bca", "course", f"semester-{sem}", "pdfs", "*.pdf")):
        base = os.path.basename(f)[len("NEBians-BCA-Course-Semester-%d-" % sem):-4]
        if base.lower().replace(",", "") .startswith(want.lower().replace(",", "")[:12]):
            return base
    return want


def describe(e, pages):
    n, unit = e["count"], ("units" if e["kind"] == "course" else "chapters")
    if e["kind"] == "entrance" and e["exam_type"] == "Mock":
        first = f"{n} model papers and mock tests with answer keys, {pages} pages."
        return clip(f"{first} Timed to {e['basis']}.", 300)
    first = f"{n} {unit}, {pages} pages, following {e['basis']}."
    return clip(f"{first} Covers {span(e['titles'])}.", 300)


def main():
    entries = []
    for slug in spine.ALL:
        track, _ = spine.track_of(slug)
        entries.append(entrance_entry(slug, None) if track else school_entry(slug, None))
    entries += list(course_entries())
    out, missing = [], []
    for e in entries:
        pdf = pdf_for(e)
        if not os.path.exists(pdf):
            missing.append(e["slug"])
            continue
        pages, size = pdf_info(pdf)
        e["pages"], e["size"] = pages, size
        e["description"] = describe(e, pages)
        e["file"] = os.path.relpath(pdf, REPO).replace(os.sep, "/")
        e["cover"] = cover(pdf, e["slug"]).replace(os.sep, "/")
        e["tags"] = ", ".join(dict.fromkeys(t for t in e["tags"] if t))
        e.update(type="PDF", year=YEAR, author_name="NEBians", source_label="NEBians", is_paid=False)
        for k in ("titles", "basis", "count", "folder", "semester"):
            e.pop(k, None)
        out.append(e)
    order = {"Class 8": 0, "Class 10 / SEE": 1, "11": 2, "12": 3, "Entrance Prep": 4, "Bachelors": 5}
    out.sort(key=lambda e: (order[e["grade_level"]], e["slug"]))
    json.dump({"site": "https://nebians.consica.com.np", "books": out},
              open(os.path.join(HERE, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(out)} books written; no PDF for: {missing or 'none'}")


if __name__ == "__main__":
    main()
