"""Assemble a subject PDF from authored chapter files."""
import os, re, sys, html as _html, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spine, md2html, mathsvg, figrun, photo, assets
from weasyprint import HTML, CSS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
CONTENT = os.path.join(ROOT, "content")
# Built books ship in the repo next to their sources, so the app can serve them
# without anyone running the pipeline.
OUT = os.path.join(ROOT, "pdf")
# theme.css and brand/ live beside this file. (They used to be looked for in a
# sibling `build/` directory, which meant every build had to be run out of a
# scratch copy of the tree shaped a particular way.)
THEME = os.path.join(HERE, "theme.css")
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


def credits_html(asset_ids):
    """Picture Credits appendix. Generated from assets/credits.json, never typed:
    every licence we reproduce under (CC BY, CC BY-SA, GFDL) requires the author
    and the licence to travel with the image, and a hand-kept list goes stale."""
    if not asset_ids:
        return ""
    rows = []
    for aid in asset_ids:
        r = assets.record(aid) or {}
        if not r:
            continue
        author = r.get("author") or "Unknown author"
        lic = r.get("license") or "licence unknown"
        lurl = r.get("license_url") or ""
        rows.append(
            f'<div class="cr"><b>{esc(r.get("title", aid))}</b> — '
            f'<span>{esc(author)}, {esc(lic)}'
            + (f' (<code>{esc(lurl)}</code>)' if lurl else "")
            + f', via {esc(r.get("source", "the web"))}.</span><br>'
            f'<code>{esc(r.get("page", ""))}</code></div>')
    if not rows:
        return ""
    return f"""<section class="chapter credits"><div class="ch-head">
<div class="ch-eyebrow">Appendix</div><h1>Picture Credits</h1></div>
<p>Schematic diagrams, graphs and derivation figures in this book were drawn for
it and are part of the book. The photographs, micrographs and reference diagrams
listed here came from free-licence sources and remain under their own licences;
they are reproduced with the attribution each licence asks for. Follow a licence
link to see exactly what it permits.</p>
<p>Where a source diagram was published in a numbered or non-English form, the
labels you see over it are ours, added so the terminology matches the CDC
syllabus. The underlying image is unchanged apart from cropping and those labels;
such an annotated version is a derivative work and is offered under the same
licence as the original.</p>
<h2>Images used in this book</h2>
{''.join(rows)}
<p style="margin-top:6mm;font-size:8pt;color:#8a8f99">
If you believe an image here is wrongly attributed or wrongly licensed, report it
in the NEBians app and it will be corrected or removed in the next edition.</p>
</section>"""


def build(slug, verbose=True):
    head, units = spine.load(slug)
    subject, accent, grade = spine.meta_for(slug)
    photo.USED.clear()          # credits are per book, in order of first use
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
{credits_html(list(photo.USED))}
</body></html>"""
    os.makedirs(OUT, exist_ok=True)
    name = f"NEBians-{subject.replace(' ', '-')}-Grade-{grade}.pdf"
    path = os.path.join(OUT, name)
    HTML(string=doc, base_url=HERE).write_pdf(path, stylesheets=[CSS(filename=THEME)])
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
    if photo.FAILS:
        print(f"\n[photos] {len(photo.FAILS)} failed")
        for c, e in photo.FAILS[:8]: print("   ", c, e.strip().splitlines()[-1][:100])
