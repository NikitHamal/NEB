"""Bundle every subject's papers across years into one PDF (e.g. Chemistry 2081-2082), newest year first.

    python3 bundle_papers.py            # reads manifest.json, writes pdf/bundles/*.pdf + bundles.json

A bundle = NEBians cover page (contents table with page numbers) + each paper's PDF (question paper + solutions) with
PDF bookmarks. Only subjects with two or more papers get a bundle. Run build_paper.py --all first.
"""
import os, json, html as _html, collections
import pymupdf
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "pdf")
OUT = os.path.join(PDF, "bundles")

CSS = """
@page { size:A4; margin:18mm 16mm; }
body { font-family:'Source Serif 4',serif; color:#14181f; font-size:10.5pt; }
.brand { font-family:Poppins,sans-serif; font-weight:700; letter-spacing:.12em; color:#1f5fbf; font-size:10pt; }
h1 { font-family:Poppins,sans-serif; font-size:28pt; margin:10mm 0 1mm; }
.sub { font-family:Poppins,sans-serif; color:#1f5fbf; font-size:13pt; margin-bottom:8mm; }
table { width:100%; border-collapse:collapse; font-family:Inter,sans-serif; font-size:9.5pt; }
th { text-align:left; border-bottom:.5mm solid #14181f; padding:2mm; }
td { border-bottom:.25mm solid #cfd5de; padding:2.2mm 2mm; }
p.note { font-size:9pt; color:#4a5568; margin-top:8mm; }
"""


def build():
    m = json.load(open(os.path.join(HERE, "manifest.json"), encoding="utf-8"))
    groups = collections.defaultdict(list)
    for r in m:
        groups[(r["grade"], r["subject"])].append(r)
    os.makedirs(OUT, exist_ok=True)
    records = []
    for (grade, subject), rs in sorted(groups.items()):
        if len(rs) < 2:
            continue
        rs.sort(key=lambda r: (-int(r["year_bs"]), r["stream"]))
        years = sorted({int(r["year_bs"]) for r in rs})
        yr = f"{years[0]}-{years[-1]}" if len(years) > 1 else str(years[0])
        name = f"NEBians-Past-Papers-Grade-{grade}-{subject.replace(' ', '-')}-{yr}-Bundle.pdf"
        # contents page numbers: cover is 1 page
        start, rows, page = 2, [], 2
        for r in rs:
            rows.append((r, page)); page += r["pages"]
        trs = "".join(
            f"<tr><td>{r['year_bs']} BS ({r['year_ad']} AD)</td><td>{_html.escape(r['stream'])}</td><td>{_html.escape(r['code'])}</td><td>{r['marks']}</td><td>{p}</td></tr>"
            for r, p in rows)
        cover = f"""<html><head><style>{CSS}</style></head><body><div class="brand">NEBIANS</div>
<h1>{_html.escape(subject)}</h1><div class="sub">Grade {grade} · Board past papers {yr} BS · with full solutions</div>
<table><tr><th>Year</th><th>Paper</th><th>Code</th><th>Marks</th><th>Page</th></tr>{trs}</table>
<p class="note">{len(rs)} papers, {page - 1} pages. Every paper is followed by its worked solutions: MCQ answer key with reasons, full working for numericals, and answers sized to the marks.</p></body></html>"""
        tmp = os.path.join(OUT, "_cover.pdf")
        HTML(string=cover).write_pdf(tmp)
        out = pymupdf.open(tmp)
        toc = [[1, f"{subject} {yr} Bundle", 1]]
        for r, p in rows:
            src = pymupdf.open(os.path.join(PDF, r["file"]))
            out.insert_pdf(src)
            toc.append([1, f"{r['year_bs']} BS · {r['stream']}", p])
        out.set_toc(toc)
        out.set_metadata({"title": f"{subject} Grade {grade} Past Papers {yr} — NEBians", "author": "NEBians"})
        path = os.path.join(OUT, name)
        out.save(path, garbage=4, deflate=True)
        os.remove(tmp)
        records.append({"file": "bundles/" + name, "subject": subject, "grade": grade, "years_bs": yr, "papers": [r["id"] for r in rs],
                        "pages": len(out), "bytes": os.path.getsize(path), "category": "Board Exam Bundle"})
        print(f"{name}: {len(rs)} papers, {len(out)} pages, {records[-1]['bytes']/1e3:.0f} KB")
    json.dump(records, open(os.path.join(HERE, "bundles.json"), "w"), indent=1)


if __name__ == "__main__":
    build()
