"""Assemble a subject PDF from authored chapter files."""
import os, re, sys, html as _html, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spine, md2html, mathsvg, figrun
from weasyprint import HTML, CSS

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CONTENT = os.path.join(ROOT, "content")
OUT = os.path.join(ROOT, "out")
EDITION = "Edition 1.0 · 2082 BS (2025–26 AD)"

def esc(s): return _html.escape(str(s))

def cover_html(subject, grade, accent, code, head):
    return f"""<section class="cover"><div class="band"></div><div class="inner">
  <div class="brand">NEBians<small>Open learning community for Nepal</small></div>
  <h1>{esc(subject)}</h1>
  <div class="grade">Grade {grade} · Science Stream</div>
  <div class="rule"></div>
  <div class="sub">Complete study notes for the NEB / CDC secondary education
     curriculum. Every unit of the official syllabus, with derivations, worked
     examples, diagrams, tables, summaries, practice questions and full model
     question papers.</div>
  <div class="foot"><span>Subject code {esc(code)}</span><span>{EDITION}</span></div>
</div></section>"""

def front_html(subject, grade, head, units, exam_notes):
    areas = []
    for u in units:
        if u["area"] and (not areas or areas[-1][0] != u["area"]):
            areas.append((u["area"], []))
        if areas: areas[-1][1].append(u)
    rows = "".join(
        f'<tr><td>{esc(a)}</td><td>{len(us)}</td>'
        f'<td>{sum(int(x["hours"]) for x in us if x["hours"]) or "—"}</td></tr>'
        for a, us in areas)
    exam = "".join(f"<li>{esc(n)}</li>" for n in exam_notes)
    return f"""<section class="frontmatter">
<h1 class="fm-title">About this book</h1>
<p class="fm-lead">These notes cover the complete official curriculum for
{esc(subject)}, Grade {grade}, as published by the Curriculum Development Centre
(CDC), Sanothimi, and examined by the National Examination Board (NEB).</p>

<h2>How this book is organised</h2>
<p>Each chapter maps to one unit of the CDC curriculum and opens with the exact
syllabus points that unit must cover, so you can tick off the syllabus as you
study. Inside a chapter you will find:</p>
<ul>
<li><strong>Concept sections</strong> following the order of the official curriculum.</li>
<li><strong>Derivations</strong> set out step by step, the way a full-mark answer should be written.</li>
<li><strong>Worked examples</strong> with the complete solution method, not just the answer.</li>
<li><strong>Figures, tables and graphs</strong> drawn to be redrawn by hand in the exam hall.</li>
<li><strong>Key points, exam tips and common mistakes</strong> pulled out of the running text.</li>
<li><strong>A chapter summary</strong> and <strong>practice questions with answers</strong>, in NEB question style.</li>
</ul>

<h2>Syllabus coverage at a glance</h2>
<table><thead><tr><th>Content area</th><th>Chapters</th><th>Teaching hours</th></tr></thead>
<tbody>{rows}</tbody></table>

<h2>Examination pattern</h2>
<ul>{exam}</ul>

<div class="box caution"><div class="bt">Please read this</div>
<p>This is a community study aid, not an official CDC or NEB publication, and it
does not replace your prescribed textbook. It was prepared from the official CDC
curriculum documents and past NEB question papers. Edition 1.0 is a first
release: if you spot an error, report it in the NEBians app so the next edition
can fix it for everybody.</p></div>

<p style="margin-top:6mm;font-size:9pt;color:#8a8f99">
{EDITION} · Prepared for the NEBians open learning community ·
Free to share and print for study purposes.</p>
</section>"""

def toc_html(units, present):
    out, cur = ['<section class="frontmatter toc"><h2>Contents</h2>'], None
    for u in units:
        if u["no"] not in present: continue
        if u["area"] != cur:
            cur = u["area"]
            out.append(f'<div class="area">{esc(cur)}</div>')
        hrs = f' <span class="hrs">· {u["hours"]} hrs</span>' if u["hours"] else ""
        out.append(f'<a href="#u{u["no"]}"><span class="n">{u["no"]}</span>'
                   f'{esc(u["title"])}{hrs}</a>')
    out.append("</section>")
    return "".join(out)

def chapter_html(u, body, subject, grade, fig_start):
    syl = "".join(f"<li>{esc(s)}</li>" for s in u["sub"])
    sylbox = (f'<div class="syllabus"><div class="t">CDC syllabus — this unit must cover</div>'
              f'<ul>{syl}</ul></div>') if syl else ""
    hrs = f'<span>{u["hours"]} teaching hours</span>' if u["hours"] else ""
    area = f'<span>{esc(u["area"])}</span>' if u["area"] else ""
    return f"""<section class="chapter" id="u{u['no']}">
<div class="ch-head"><div class="ch-eyebrow">Unit {u['no']}</div>
<h1>{esc(u['title'])}</h1>
<div class="ch-meta">{area}{hrs}</div></div>
{sylbox}
{body}
</section>"""

def build(slug, verbose=True):
    head, units = spine.load(slug)
    subject, accent, grade = spine.meta_for(slug)
    code = head.get("code", "").split()[0]
    cdir = os.path.join(CONTENT, slug)
    present, bodies, figno = set(), {}, 1
    for u in units:
        p = os.path.join(cdir, f"unit-{u['no']:02d}.md")
        if not os.path.exists(p): continue
        txt = open(p, encoding="utf-8").read()
        if len(txt.strip()) < 400: continue
        _, htm, figno = md2html.convert(txt, f"{slug}-u{u['no']}", figno)
        bodies[u["no"]] = htm
        present.add(u["no"])
    if not present:
        return None, 0, 0
    extras = []
    for name, title in (("model-questions", "Model Question Papers"),
                        ("formula-sheet", "Formula Sheet"),
                        ("answer-key", "Answer Key")):
        p = os.path.join(cdir, name + ".md")
        if os.path.exists(p) and len(open(p, encoding="utf-8").read().strip()) > 400:
            _, htm, figno = md2html.convert(open(p, encoding="utf-8").read(),
                                            f"{slug}-{name}", figno)
            extras.append(f'<section class="chapter paper"><div class="ch-head">'
                          f'<div class="ch-eyebrow">Appendix</div><h1>{title}</h1></div>{htm}</section>')
    exam_notes = [n for n in head["notes"] if n.startswith(("EXAM", "PATTERN", "GRID"))]
    exam_notes = [re.sub(r"^(EXAM|PATTERN|GRID):\s*", "", n) for n in exam_notes] or \
                 ["See the NEB specification grid for the current pattern."]
    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>{esc(subject)} Grade {grade} — NEBians</title>
<style>:root{{--accent:{accent};--accent-wash:{accent}12}}
.cover .band{{background:linear-gradient(155deg,{accent} 0%,#14181f 155%)}}
html{{string-set:booktitle "{esc(subject)} · Grade {grade}"}}</style>
</head><body>
{cover_html(subject, grade, accent, code, head)}
{front_html(subject, grade, head, units, exam_notes)}
{toc_html(units, present)}
{''.join(chapter_html(u, bodies[u['no']], subject, grade, 1) for u in units if u['no'] in present)}
{''.join(extras)}
</body></html>"""
    os.makedirs(OUT, exist_ok=True)
    name = f"NEBians-{subject.replace(' ', '-')}-Grade-{grade}.pdf"
    path = os.path.join(OUT, name)
    HTML(string=doc, base_url=ROOT).write_pdf(path, stylesheets=[CSS(filename=os.path.join(ROOT, "build", "theme.css"))])
    import pypdf_pages
    pages = pypdf_pages.count(path)
    if verbose:
        print(f"{slug:7} -> {name}  chapters={len(present)}/{len(units)}  pages={pages}  "
              f"{os.path.getsize(path)/1e6:.1f} MB")
    return path, len(present), pages

if __name__ == "__main__":
    targets = sys.argv[1:] or spine.ALL
    for s in targets:
        try:
            build(s)
        except Exception as e:
            print(f"{s}: BUILD ERROR {type(e).__name__}: {e}")
    if mathsvg.FAILS:
        print(f"\n[math] {len(mathsvg.FAILS)} expressions fell back to plain text")
        for t, e in mathsvg.FAILS[:8]: print("   ", t[:70], "|", e[:70])
    if figrun.FAILS:
        print(f"\n[figures] {len(figrun.FAILS)} failed")
        for c, e in figrun.FAILS[:5]: print("   ", c, e.strip().splitlines()[-1][:90])
