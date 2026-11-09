"""Engineering bundles: per-subject multi-year PDFs + the master All-in-One book.

    PAPERS_CONTENT=.../engineering/content PAPERS_OUT=.../engineering/pdf python3 bundle_engineering.py

Reads the front matter of every content/*.md, groups papers by (programme level, subject),
writes pdf/bundles/<subject-slug>-<yearA>-<yearB>.pdf (cover + contents + each paper, with bookmarks)
and pdf/bundles/NEBians-Engineering-All-In-One-Book.pdf (master cover, master contents, every subject, every year).
Writes bundles.json for the app. Idempotent: just re-run after adding papers.
"""
import os, re, json, glob, html as _html, collections
import pymupdf
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.environ.get("PAPERS_CONTENT") or os.path.join(HERE, "content")
PDF = os.environ.get("PAPERS_OUT") or os.path.join(HERE, "pdf")
OUT = os.path.join(PDF, "bundles")
MONTH = {m: i for i, m in enumerate(
    "Baishakh Jestha Ashadh Shrawan Bhadra Ashwin Kartik Mangsir Poush Magh Falgun Chaitra".split(), 1)}
MONTH.update({"Asar": 3, "Ashoj": 6, "Asoj": 6, "Shrawan": 4, "Mangshir": 8})

CSS = """
@page { size:A4; margin:16mm 15mm; }
body { font-family:'Source Serif 4',serif; color:#14181f; font-size:10pt; }
.brand { font-family:Poppins,sans-serif; font-weight:700; letter-spacing:.14em; color:#1f5fbf; font-size:10pt; }
h1 { font-family:Poppins,sans-serif; font-size:27pt; margin:8mm 0 1mm; line-height:1.15; }
h2 { font-family:Poppins,sans-serif; font-size:12.5pt; color:#1f5fbf; margin:6mm 0 1.5mm; }
.sub { font-family:Poppins,sans-serif; color:#1f5fbf; font-size:12pt; margin-bottom:6mm; }
table { width:100%; border-collapse:collapse; font-family:Poppins,sans-serif; font-size:8.6pt; }
th { text-align:left; border-bottom:.5mm solid #14181f; padding:1.6mm 2mm; }
td { border-bottom:.25mm solid #cfd5de; padding:1.8mm 2mm; }
p.note { font-size:9pt; color:#4a5568; margin-top:6mm; }
"""


def meta(path):
    t = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    fm = re.match(r"^---\n(.*?)\n---", t, re.S).group(1)
    d = {}
    for ln in fm.split("\n"):
        k, _, v = ln.partition(":")
        d[k.strip()] = v.strip()
    d["id"] = os.path.basename(path)[:-3]
    y, _, mo = d["year_bs"].partition(" ")
    d["y"], d["mo"] = int(y), MONTH.get(mo.split()[0], 0)
    d["pdfpath"] = os.path.join(PDF, d["file"])
    d["pages"] = len(pymupdf.open(d["pdfpath"]))
    return d


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def yr_range(rs):
    ys = sorted({r["y"] for r in rs})
    return f"{ys[0]}-{ys[-1]}" if len(ys) > 1 else str(ys[0])


def newest_first(rs):
    return sorted(rs, key=lambda r: (-r["y"], -r["mo"], r["code"]))


def cover_pdf(path, title, sub, sections, note, first_page):
    """sections: [(heading|None, [(paper, page)])]"""
    body = ""
    for head, rows in sections:
        if head:
            body += f"<h2>{_html.escape(head)}</h2>"
        trs = "".join(
            f"<tr><td>{r['year_bs']} BS ({r['year_ad']} AD)</td><td>{_html.escape(r['code'])}</td>"
            f"<td>{_html.escape(r['students'].split('.')[1].strip() if '.' in r['students'] else '')}</td>"
            f"<td>{r['marks']}</td><td>{p}</td></tr>" for r, p in rows)
        body += f"<table><tr><th>Sitting</th><th>Code</th><th>Course</th><th>Marks</th><th>Page</th></tr>{trs}</table>"
    html = (f"<html><head><style>{CSS}</style></head><body><div class='brand'>NEBIANS</div><h1>{_html.escape(title)}</h1>"
            f"<div class='sub'>{_html.escape(sub)}</div>{body}<p class='note'>{_html.escape(note)}</p></body></html>")
    HTML(string=html).write_pdf(path)
    return len(pymupdf.open(path))


def assemble(out_path, cover_tmp, entries, title):
    """entries: [(label, level, pdfpath)] -> merged pdf with bookmarks."""
    out = pymupdf.open(cover_tmp)
    toc = [[1, title, 1]]
    for lvl, label, p in entries:
        if p is None:
            toc.append([lvl, label, len(out) + 1])
            continue
        start = len(out) + 1
        out.insert_pdf(pymupdf.open(p))
        toc.append([lvl, label, start])
    out.set_toc(toc)
    out.set_metadata({"title": f"{title} — NEBians", "author": "NEBians"})
    out.save(out_path, garbage=4, deflate=True)
    return len(out)


def build():
    papers = [meta(p) for p in sorted(glob.glob(os.path.join(CONTENT, "*.md")))]
    os.makedirs(OUT, exist_ok=True)
    groups = collections.defaultdict(list)
    for r in papers:
        groups[(r["level"].split(" / ")[0], r["subject"])].append(r)
    records, tmp = [], os.path.join(OUT, "_cover.pdf")
    for (level, subject), rs in sorted(groups.items()):
        if len(rs) < 2:
            continue
        rs = newest_first(rs)
        yr = yr_range(rs)
        name = f"{slug(subject)}-{yr}.pdf"
        # cover length is unknown before rendering: render once, then fix page numbers
        n_cover = 1
        for _ in range(2):
            page, rows = n_cover + 1, []
            for r in rs:
                rows.append((r, page)); page += r["pages"]
            n_cover = cover_pdf(tmp, subject, f"{level} · Tribhuvan University, IOE · past papers {yr} BS with full solutions",
                                [(None, rows)], f"{len(rs)} papers, {page - 1} pages. Each paper is followed by its complete worked solutions.", 1)
        path = os.path.join(OUT, name)
        pages = assemble(path, tmp, [(1, f"{r['year_bs']} · {r['code']}", r["pdfpath"]) for r in rs], f"{subject} {yr}")
        records.append({"file": "bundles/" + name, "subject": subject, "level": level, "years_bs": yr,
                        "papers": [r["id"] for r in rs], "pages": pages, "bytes": os.path.getsize(path), "kind": "subject-bundle"})
        print(f"{name}: {len(rs)} papers, {pages} pages")
    # ---- master all-in-one book
    subj = collections.OrderedDict()
    for r in sorted(papers, key=lambda r: (r["level"].split(" / ")[0], r["subject"])):
        subj.setdefault((r["level"].split(" / ")[0], r["subject"]), []).append(r)
    n_cover = 1
    for _ in range(3):
        page, secs = n_cover + 1, []
        for (level, subject), rs in subj.items():
            rows = []
            for r in newest_first(rs):
                rows.append((r, page)); page += r["pages"]
            secs.append((f"{subject}  ·  {level}  ·  {yr_range(rs)} BS", rows))
        n_cover = cover_pdf(tmp, "Engineering Past Papers, All-in-One Book",
                            "Tribhuvan University, Institute of Engineering · every solved paper · free forever", secs,
                            f"{len(papers)} papers across {len(subj)} subjects, {page - 1} pages. Each paper is the full question paper "
                            "reconstructed from the official scan, followed by complete worked solutions. Free for every student.", 1)
    entries = []
    for (level, subject), rs in subj.items():
        entries.append((1, f"{subject} ({yr_range(rs)})", None))
        for r in newest_first(rs):
            entries.append((2, f"{r['year_bs']} · {r['code']}", r["pdfpath"]))
    name = "NEBians-Engineering-All-In-One-Book.pdf"
    path = os.path.join(OUT, name)
    pages = assemble(path, tmp, entries, "Engineering Past Papers, All-in-One Book")
    records.append({"file": "bundles/" + name, "subject": "ALL", "years_bs": yr_range(papers), "papers": [r["id"] for r in papers],
                    "pages": pages, "bytes": os.path.getsize(path), "kind": "master-book"})
    print(f"{name}: {len(papers)} papers, {pages} pages")
    os.remove(tmp)
    json.dump(records, open(os.path.join(HERE, "bundles.json"), "w"), indent=1)


if __name__ == "__main__":
    build()
