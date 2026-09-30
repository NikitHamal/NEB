"""Assemble a subject PDF from authored chapter files."""
import os, re, sys, html as _html, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spine, md2html, mathsvg, figrun, photo, assets, i18n
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
    L = i18n.CUR
    return f"""<section class="cover"><div class="band"></div><div class="inner">
  <div class="brand">{"नेबियन्स" if L["digits"] else "NEBians"}<small>{L["tagline"]}</small></div>
  <h1>{esc(subject)}</h1>
  <div class="grade">{L["grade"].format(g=i18n.num(grade))}</div>
  <div class="rule"></div>
  <div class="sub">{L["cover_sub"]}</div>
  <div class="foot"><span>{L["code"]} {esc(code)}</span><span>{L["edition"]}</span></div>
</div></section>"""

def front_html(subject, grade, head, units, exam_notes):
    L = i18n.CUR
    areas = []
    for u in units:
        if u["area"] and (not areas or areas[-1][0] != u["area"]):
            areas.append((u["area"], []))
        if areas: areas[-1][1].append(u)
    rows = "".join(
        f'<tr><td>{esc(a)}</td><td>{i18n.num(len(us))}</td>'
        f'<td>{i18n.num(sum(int(x["hours"]) for x in us if x["hours"])) if any(x["hours"] for x in us) else "—"}</td></tr>'
        for a, us in areas)
    exam = "".join(f"<li>{esc(n)}</li>" for n in exam_notes)
    lis = "".join(f"<li>{x}</li>" for x in L["org_li"])
    th = "".join(f"<th>{x}</th>" for x in L["th"])
    return f"""<section class="frontmatter">
<h1 class="fm-title">{L["front_title"]}</h1>
<p class="fm-lead">{L["front_lead"].format(subject=esc(subject), g=i18n.num(grade))}</p>

<h2>{L["org_h"]}</h2>
<p>{L["org_p"]}</p>
<ul>{lis}</ul>

<h2>{L["cover_h"]}</h2>
<table><thead><tr>{th}</tr></thead>
<tbody>{rows}</tbody></table>

<h2>{L["exam_h"]}</h2>
<ul>{exam}</ul>

<div class="box caution"><div class="bt">{L["read"]}</div>
<p>{L["disclaimer"]}</p></div>

<p style="margin-top:6mm;font-size:9pt;color:#8a8f99">
{L["edition"]} · {L["prep"]}</p>
</section>"""

def toc_html(units, present):
    out, cur = [f'<section class="frontmatter toc"><h2>{i18n.CUR["contents"]}</h2>'], None
    for u in units:
        if u["no"] not in present: continue
        if u["area"] != cur:
            cur = u["area"]
            out.append(f'<div class="area">{esc(cur)}</div>')
        hrs = f' <span class="hrs">· {i18n.num(u["hours"])}{i18n.CUR["hrs"]}</span>' if u["hours"] else ""
        out.append(f'<a href="#u{u["no"]}"><span class="n">{i18n.num(u["no"])}</span>'
                   f'{esc(u["title"])}{hrs}</a>')
    out.append("</section>")
    return "".join(out)

def chapter_html(u, body, subject, grade, fig_start):
    syl = "".join(f"<li>{esc(s)}</li>" for s in u["sub"])
    sylbox = (f'<div class="syllabus"><div class="t">{i18n.CUR["syl"]}</div>'
              f'<ul>{syl}</ul></div>') if syl else ""
    hrs = f'<span>{i18n.num(u["hours"])} {i18n.CUR["teaching_hours"]}</span>' if u["hours"] else ""
    area = f'<span>{esc(u["area"])}</span>' if u["area"] else ""
    return f"""<section class="chapter" id="u{u['no']}">
<div class="ch-head"><div class="ch-eyebrow">{i18n.CUR["unit"]} {i18n.num(u['no'])}</div>
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
        author = r.get("author") or i18n.CUR["unknown_author"]
        lic = r.get("license") or i18n.CUR["lic_unknown"]
        lurl = r.get("license_url") or ""
        rows.append(
            f'<div class="cr"><b>{esc(r.get("title", aid))}</b> — '
            f'<span>{esc(author)}, {esc(lic)}'
            + (f' (<code>{esc(lurl)}</code>)' if lurl else "")
            + f', {i18n.CUR["via"]} {esc(r.get("source", i18n.CUR["web"]))}.</span><br>'
            f'<code>{esc(r.get("page", ""))}</code></div>')
    if not rows:
        return ""
    L = i18n.CUR
    return f"""<section class="chapter credits"><div class="ch-head">
<div class="ch-eyebrow">{L["appendix"]}</div><h1>{L["credits_h"]}</h1></div>
<p>{L["cr_p1"]}</p>
<p>{L["cr_p2"]}</p>
<h2>{L["credits_sub"]}</h2>
{''.join(rows)}
<p style="margin-top:6mm;font-size:8pt;color:#8a8f99">
{L["cr_foot"]}</p>
</section>"""


def build(slug, verbose=True):
    head, units = spine.load(slug)
    L = i18n.set_book(slug)
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
    for name, title in L["extras"]:
        p = os.path.join(cdir, name + ".md")
        if os.path.exists(p) and len(open(p, encoding="utf-8").read().strip()) > 400:
            _, htm, figno = md2html.convert(open(p, encoding="utf-8").read(),
                                            f"{slug}-{name}", figno)
            extras.append(f'<section class="chapter paper"><div class="ch-head">'
                          f'<div class="ch-eyebrow">{L["appendix"]}</div><h1>{title}</h1></div>{htm}</section>')
    exam_notes = [n for n in head["notes"] if n.startswith(("EXAM", "PATTERN", "GRID"))]
    exam_notes = [re.sub(r"^(EXAM|PATTERN|GRID):\s*", "", n) for n in exam_notes] or \
                 [L["no_grid"]]
    doc = f"""<!DOCTYPE html><html lang="{L["lang"]}"><head><meta charset="utf-8">
<title>{esc(subject)} {L["grade"].split(" ·")[0].format(g=i18n.num(grade))} — {"नेबियन्स" if L["digits"] else "NEBians"}</title>
<style>:root{{--accent:{accent};--accent-wash:{accent}12}}
.cover .band{{background:linear-gradient(155deg,{accent} 0%,#14181f 155%)}}
html{{string-set:booktitle "{esc(subject)} · {L["grade"].split(" ·")[0].format(g=i18n.num(grade))}"}}
@page{{@bottom-left{{content:"{L["footer"]}"}}@bottom-right{{content:counter(page{", devanagari" if L["digits"] else ""})}}}}
@page frontmatter{{@bottom-right{{content:counter(page,{"devanagari" if L["digits"] else "lower-roman"})}}}}</style>
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
