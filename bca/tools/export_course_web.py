#!/usr/bin/env python3
"""Put the BCA course books (41 subjects, 8 semesters) into the website's and the app's syllabus.

The PDF adapter (`nebpdf.py`) already knows how to stage a course book and to give it a spine.
This script reuses that staging and the exporters of the school and entrance books
(`notes/tools/export_study.py`, `export_syllabus.py`), so a course unit is typeset exactly like
every other chapter: the same Markdown pipeline, KaTeX maths, figures written once by content hash.

Output (track key `bca-course`, kind `course`; one card group per semester):

    backend_python/web/data/syllabus/bca-course-<subject>.json    units, topics, summaries, terms
    backend_python/web/data/syllabus/index.json                   the `bca-course` entry is replaced
    backend_python/web/data/study/bca-course-<subject>/           unit-NN.json and index.json
    backend_python/web/static/web/study/                          figures (shared with the other books)

Run:  python3 bca/tools/export_course_web.py                      every book
      python3 bca/tools/export_course_web.py semester-1/digital-logic ...
Needs the same environment as the PDF build (see PDF_M3X_STATUS.md). `notes/tools/export_syllabus.py`
keeps the `bca-course` entry of index.json when it rewrites the file.
"""
import json
import os
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "notes", "tools"))

import nebpdf  # noqa: E402  (stages course books, patches the house pipeline for them)
import spine  # noqa: E402
import export_study as es  # noqa: E402
import export_syllabus as sy  # noqa: E402

TRACK = "bca-course"
INFO = {
    "label": "BCA · Tribhuvan University course notes",
    "label_ne": "बीसीए पाठ्यक्रम",
    "exam": "Tribhuvan University BCA, semester examinations (2082 batch curriculum)",
    "short": "BCA Course",
    "kind": "course",
}
ASSESSMENT = ("TU assessment: 60% final examination set by the university, 40% internal "
              "(assignments, lab work, attendance). Confirm the split in your college's notice.")
ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII"}
ICONS = {
    "programming-in-c": "terminal", "digital-logic": "memory", "computer-fundamentals": "computer",
    "mathematics-1": "calculate", "professional-communication-ethics": "groups",
    "hardware-workshop": "build", "discrete-structure": "account_tree", "oop-in-java": "code",
    "mathematics-2": "functions", "microprocessor-computer-architecture": "memory",
    "ux-ui-design": "palette", "principles-of-management": "work",
    "data-structure-and-algorithms": "schema", "dbms": "database", "web-technology-1": "web",
    "system-analysis-and-design": "analytics", "probability-and-statistics": "analytics",
    "applied-economics": "trending_up", "operating-systems": "dns", "numerical-methods": "calculate",
    "software-engineering": "engineering", "python-programming": "terminal", "web-technology-2": "language",
    "computer-networking": "lan", "network-administration": "lan", "artificial-intelligence": "smart_toy", "advanced-java": "code",
    "mis-and-e-business": "storage", "society-and-technology": "public", "computer-graphics": "draw",
    "mobile-programming": "smartphone", "cryptography-network-security": "lock",
    "technical-writing": "edit_note", "distributed-system": "hub", "financial-accounting": "account_balance",
    "cloud-computing": "cloud", "cyber-security-and-ethical-hacking": "security", "project-1": "assignment",
    "project-2": "assignment", "project-3": "assignment", "project-4": "rocket_launch",
    "internship": "school",
}


def _paths(slug):
    d = os.path.join(nebpdf.STAGE, "content", slug)
    return sorted(os.path.join(d, f) for f in os.listdir(d)
                  if f.startswith("unit-") and f.endswith(".md"))


def export_book(book, pool, write_study=True):
    kind, slug, src, _ = book
    meta = nebpdf._course_meta[slug]
    key = os.path.basename(src)
    nebpdf.stage(kind, slug, src)
    head, units = spine.load(slug)
    sy.NOTES = nebpdf.STAGE            # read_unit() reads <NOTES>/content/<slug>/unit-NN.md
    out_units = []
    for u in units:
        body = sy.read_unit(slug, u["no"]) or {}
        hours = int(u["hours"]) if str(u["hours"]).isdigit() and int(u["hours"]) > 0 else None
        out_units.append({
            "no": u["no"], "title": sy.clean(u["title"]), "hours": hours, "area": "",
            "topics": sy.topics_for(u, body), "sections": body.get("sections", []),
            "summary": body.get("summary", []), "terms": body.get("terms", []),
            "stats": {k: body.get(k, 0) for k in ("words", "figures", "examples")},
            "has_notes": bool(body),
        })
    sem = int(meta["semester"])
    data = {
        "grade": TRACK, "grade_label": "BCA Course", "grade_label_ne": INFO["label_ne"],
        "short": INFO["short"], "kind": "course", "subject": key, "name": meta["name"], "name_ne": "",
        "icon": ICONS.get(key, "menu_book"), "group": "semester-%d" % sem,
        "group_label": "Semester %s" % ROMAN[sem], "color": meta["accent"], "lang": "en",
        "code": meta["code"], "credits": meta["credits"], "semester": sem,
        "hours": sum(u["hours"] or 0 for u in out_units) or None, "questions": None,
        "exam": ASSESSMENT, "areas": [], "units": out_units, "unit_count": len(out_units),
        "topic_count": sum(len(u["topics"]) for u in out_units),
        "notes_ready": sum(1 for u in out_units if u["has_notes"]),
    }
    with open(os.path.join(sy.OUT, "%s-%s.json" % (TRACK, key)), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    if write_study:
        folder = os.path.join(es.DATA, "%s-%s" % (TRACK, key))
        os.makedirs(folder, exist_ok=True)
        chapters = pool.map(es._chapter, [(slug, p) for p in _paths(slug)])
        items = []
        for ch in chapters:
            with open(os.path.join(folder, "unit-%02d.json" % ch["no"]), "w", encoding="utf-8", newline="\n") as fh:
                json.dump(ch, fh, ensure_ascii=False, separators=(",", ":"))
            items.append({k: ch[k] for k in ("no", "title", "area", "words", "read_min", "figures", "has_questions")})
        es._merge_index(folder, {"book": slug, "units": items})
    card = {k: data[k] for k in sy.CARD_KEYS}
    card.update(questions=None, credits=data["credits"], semester=sem, group_label=data["group_label"],
                code=data["code"])
    print("%-52s %2d units  %3d topics" % (slug, len(out_units), data["topic_count"]), flush=True)
    return sem, meta["code"], card


def write_index(cards):
    path = os.path.join(sy.OUT, "index.json")
    index = json.load(open(path, encoding="utf-8"))
    old = next((g for g in index["grades"] if g.get("grade") == TRACK), None)
    keep = {c["subject"]: c for c in (old or {}).get("subjects", [])}
    for _, _, card in cards:
        keep[card["subject"]] = card
    ordered = sorted(keep.values(), key=lambda c: (c["semester"], c["code"]))
    entry = dict(INFO, grade=TRACK, subjects=ordered)
    index["grades"] = [g for g in index["grades"] if g.get("grade") != TRACK] + [entry]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(index, fh, ensure_ascii=False, indent=1)


def main(argv):
    sels = [a for a in argv if not a.startswith("--")]
    books = [b for b in nebpdf.discover(None) if b[0] == "course"]
    if sels:
        books = [b for b in books if any(b[2].endswith(s.strip("/")) for s in sels)]
    if not books:
        sys.exit("no course book matched")
    spine.CUR = os.path.join(nebpdf.STAGE, "curriculum")
    os.makedirs(es.MEDIA, exist_ok=True)
    os.makedirs(es.DATA, exist_ok=True)
    cards = []
    with Pool(2) as pool:
        for book in books:
            cards.append(export_book(book, pool, "--no-study" not in argv))
    write_index(cards)
    print("index.json: %d subjects in %s" % (len(cards), TRACK))


if __name__ == "__main__":
    main(sys.argv[1:])
