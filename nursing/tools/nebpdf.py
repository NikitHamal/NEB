#!/usr/bin/env python3
"""BSc Nursing PDF builder: a thin adapter over the NEBians house pipeline (notes/pipeline).

The CEE, IOE and Grade 8-12 books are built by notes/pipeline/build_pdf.py (Markdown -> HTML ->
WeasyPrint, theme.css, Poppins/Inter/Source Serif 4/JetBrains Mono, N watermark, linked contents,
roman-numbered front matter, matplotlib maths). This file does NOT reimplement any of that. It only
(1) stages nursing/ sources into the tree shape the pipeline expects, (2) generates a spine for course
books from their unit files, (3) tells the pipeline's i18n/spine helpers about BCA course books,
then calls the pipeline's own build().

    python3 nursing/tools/nebpdf.py                 # every nursing book
    python3 nursing/tools/nebpdf.py entrance        # the 4 entrance books
    python3 nursing/tools/nebpdf.py course          # all course books
    python3 nursing/tools/nebpdf.py course/semester-1/digital-logic
    python3 nursing/tools/nebpdf.py --check-only    # validate maths/figures, build nothing

Output: bca/entrance/pdfs/ and bca/course/semester-N/pdfs/. Staging lives in nursing/.stage (gitignored).
"""
import json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BCA = os.path.dirname(HERE)  # = nursing/
REPO = os.path.dirname(BCA)
PIPE = os.path.join(REPO, "notes", "pipeline")
STAGE = os.path.join(BCA, ".stage")
sys.path.insert(0, PIPE)

import spine, i18n, build_pdf, mathsvg, figrun, photo  # noqa: E402  (the house pipeline)

ENTRANCE = {  # directory -> pipeline slug (track "bca", subjects defined in spine.TRACK_SUBJECTS)
    "mathematics": "bca-math", "english": "bca-eng",
    "gk-and-it": "bca-gk", "model-papers": "bca-mock",
}
COURSE_PREFIX = "nurcourse-"
_course_meta = {}          # slug -> dict(name, code, semester, credits, accent)

# ---------------------------------------------------------------- course furniture
COURSE_EN = dict(i18n.EN)
COURSE_EN.update(
    cover_sub=("The complete subject as the Nepal BSc Nursing programme (Tribhuvan University IOM and affiliated campuses) teaches it: every unit "
               "of the syllabus, real photographs, labelled diagrams, machine-verified clinical calculations, "
               "chapter summaries and practice questions with worked answers."),
    hrs=" hrs", teaching_hours="teaching hours", unit="Unit",
    syl="Syllabus: this unit covers", th=("Content area", "Units", "Teaching hours"),
    cover_h="Syllabus at a glance", exam_h="Assessment",
    front_lead=("This book covers {subject} from the Nepal BSc Nursing programme, unit by unit. It is written to "
                "be studied end to end without a second textbook: concepts first, then worked "
                "examples, then a fact sheet, a summary and a practice set with answers."),
    org_p=("Each unit follows the syllabus order and opens with the topics it covers. Inside a "
           "unit you will find:"),
    org_li=["<strong>Concept sections</strong> in syllabus order, defined precisely.",
            "<strong>Worked examples</strong> with the full method, including drug-dose and biostatistics sums.",
            "<strong>Photographs, diagrams and calculations</strong> that were checked, not copied.",
            "<strong>Key points, cautions and exam tips</strong> pulled out of the running text.",
            "<strong>A formula and fact sheet</strong> and <strong>a chapter summary</strong> for revision.",
            "<strong>Exam answers and NANDA-I care plans</strong> in the style of the university paper."],
    disclaimer=("This is a free community study aid, not an official publication of Tribhuvan "
                "University, the Nepal Nursing Council or the Medical Education Commission. It follows the published BSc Nursing curriculum as far as it could be verified; the university's own syllabus "
                "document and notices are the authority if they differ. It is not a substitute for hospital protocols or a prescriber's order. If you find an error, "
                "report it in the NEBians app so the next edition can fix it for everybody."),
    no_grid="See the university / MEC notice for the current pattern.",
)
_orig_set_book = i18n.set_book
_orig_track_of, _orig_meta_for, _orig_pdf_name = spine.track_of, spine.meta_for, spine.pdf_name


def _label(m):
    return "MECEE-BL Entrance · BSc Nursing" if str(m["year"]) == "E" else f"Year {m['year']} · BSc Nursing (Nepal)"


def _set_book(slug):
    if slug.startswith(COURSE_PREFIX):
        m = _course_meta[slug]
        i18n.CUR = dict(COURSE_EN, grade=_label(m))
        return i18n.CUR
    return _orig_set_book(slug)


def _meta_for(slug):
    if slug.startswith(COURSE_PREFIX):
        m = _course_meta[slug]
        return m["name"], m["accent"], _label(m)
    return _orig_meta_for(slug)


def _pdf_name(slug):
    if slug.startswith(COURSE_PREFIX):
        m = _course_meta[slug]
        return f"NEBians-BScNursing-{m['tag']}-{m['name'].replace(' ', '-').replace('/', '-')}.pdf"
    return _orig_pdf_name(slug)


i18n.set_book, spine.meta_for, spine.pdf_name = _set_book, _meta_for, _pdf_name
# `i18n.set_book` imports spine lazily and calls spine.track_of on slugs it knows; course slugs never reach it.


# ---------------------------------------------------------------- nursing-only table style
# The 5-column NANDA-I care plan (Assessment | Diagnosis | Goal | Interventions | Evaluation) gets fixed column
# widths and no hyphenation, so narrow cells do not break words ("diag-nosis"). Everything else is the m3x theme.
import md2html  # noqa: E402
NURSING_CSS = """
table.careplan { table-layout:fixed; font-size:8.3pt; width:100%; }
table.careplan th, table.careplan td { box-sizing:border-box; }
table.careplan th, table.careplan td { hyphens:manual; -weasy-hyphens:manual; overflow-wrap:break-word; padding-left:1.8mm; padding-right:1.8mm; }
table.careplan th:nth-child(1) { width:18%; } table.careplan th:nth-child(2) { width:17%; }
table.careplan th:nth-child(3) { width:17%; } table.careplan th:nth-child(4) { width:34%; }
table.careplan th:nth-child(5) { width:14%; }
table.careplan tr { break-inside:avoid; }
"""
_orig_layout = md2html._layout_fixes


def _layout(htm):
    def tag(m):
        t = m.group(0)
        head = re.sub(r"<[^>]+>", " ", t[:900])
        if 'class="' not in t[:30] and "NANDA" in head and len(re.findall(r"<th\b", t.split("</tr>")[0])) == 5:
            return t.replace("<table", '<table class="careplan"', 1)
        return t
    return _orig_layout(re.sub(r"<table\b.*?</table>", tag, htm, flags=re.S))


md2html._layout_fixes = _layout
os.makedirs(STAGE, exist_ok=True)
_theme = os.path.join(STAGE, "theme-nursing.css")
open(_theme, "w", encoding="utf-8").write(open(build_pdf.THEME, encoding="utf-8").read() + NURSING_CSS)
build_pdf.THEME = _theme

# ---------------------------------------------------------------- discovery and staging
def _units(d):
    return sorted(f for f in os.listdir(d) if re.fullmatch(r"unit-\d+\.md", f))


def _front(path):
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", txt, re.S)
    fm = dict(l.split(":", 1) for l in m.group(1).splitlines() if ":" in l) if m else {}
    return {k.strip(): v.strip() for k, v in fm.items()}, txt


def _course_spine(rel, meta, d):
    code = meta["code"].replace(" ", "-")   # the cover prints the first token of CODE
    lines = [f"# SUBJECT: {meta['name']} | CODE: {code} | CREDITS: {meta['credits']}",
             "# EXAM: " + meta.get("exam", "University assessment: internal plus final examination; confirm the split in your campus notice"),
             f"# AREA: {meta['code']} · {meta['name']} (Year {meta['year']})"]
    for f in _units(d):
        fm, txt = _front(os.path.join(d, f))
        n = int(fm.get("unit", re.search(r"\d+", f).group()))
        lines.append(f"## {n}. {fm['title']} [{fm.get('hours', '')}]".replace("[]", ""))
        for h in re.findall(r"^## (\d+\.\d+)\s+(.+)$", txt, re.M):
            lines.append(f"- {h[1].strip()}")
    return "\n".join(lines) + "\n"


def discover(selector=None):
    """Return [(kind, slug, srcdir, outdir)]."""
    books = []
    reg = json.load(open(os.path.join(BCA, "books.json"), encoding="utf-8"))
    for rel, meta in reg.items():
        if rel.startswith("_"):
            continue
        d = os.path.join(BCA, rel)
        if not os.path.isdir(d) or not _units(d):
            continue
        slug = COURSE_PREFIX + rel.replace("/", "-")
        meta["tag"] = ("Entrance" if str(meta["year"]) == "E" else f"Year-{meta['year']}")
        _course_meta[slug] = meta
        books.append(("course", slug, d, os.path.join(BCA, "pdfs")))
    if selector:
        sel = selector.strip("/").replace("nursing/", "", 1)
        books = [b for b in books if (sel == "course")
                 or b[2].endswith(sel) or b[1] == sel]
    return books


def stage(kind, slug, d):
    cdir = os.path.join(STAGE, "content", slug)
    shutil.rmtree(cdir, ignore_errors=True)
    os.makedirs(cdir)
    os.makedirs(os.path.join(STAGE, "curriculum"), exist_ok=True)
    for f in _units(d):
        shutil.copy(os.path.join(d, f), cdir)
    for extra in ("model-questions.md", "formula-sheet.md", "answer-key.md"):
        if os.path.exists(os.path.join(d, extra)):
            shutil.copy(os.path.join(d, extra), cdir)
    sp = os.path.join(STAGE, "curriculum", slug + ".md")
    if kind == "entrance":
        shutil.copy(os.path.join(d, "SPINE.md"), sp)
    else:
        open(sp, "w", encoding="utf-8").write(_course_spine(os.path.relpath(d, BCA), _course_meta[slug], d))


def main(argv):
    check_only = "--check-only" in argv
    sels = [a for a in argv if not a.startswith("--")]
    books = []
    for s in (sels or [None]):
        books += discover(s)
    if not books:
        sys.exit("no nursing book matched")
    spine.CUR = os.path.join(STAGE, "curriculum")
    build_pdf.CONTENT = os.path.join(STAGE, "content")
    results = []
    for kind, slug, d, out in books:
        stage(kind, slug, d)
        if check_only:
            import check as _c  # noqa: F401  (house check: renders every formula and figure)
            continue
        build_pdf.OUT = out
        path, nch, pages = build_pdf.build(slug)
        results.append((slug, path, nch, pages))
    bad = len(mathsvg.FAILS) + len(figrun.FAILS) + len(photo.FAILS)
    for t, e in mathsvg.FAILS[:10]:
        print("[math] fell back to text:", t[:80], "|", e[:60])
    for c, e in figrun.FAILS[:10]:
        print("[figure] failed:", c, e.strip().splitlines()[-1][:100])
    print(f"\nbuilt {len(results)} book(s); math/figure/photo failures: {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
