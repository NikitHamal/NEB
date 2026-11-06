"""Assemble a subject PDF from authored chapter files."""
import os, re, sys, html as _html, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spine, md2html, mathsvg, figrun, photo, assets, i18n, furniture, m3x
from furniture import cover_html, front_html, toc_html, chapter_html
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


def localise_marks(html):
    """Devanagari digits inside the [n] marks chips of a Nepali book."""
    if not i18n.CUR["digits"]:
        return html
    return re.sub(r'(<span class="marks">)([^<]*)(</span>)',
                  lambda m: m.group(1) + i18n.num_str(m.group(2)) + m.group(3), html)

# Devanagari conjuncts break when tracked, and uppercasing is meaningless for
# it. Nepali books get this sheet appended after theme.css, so every tracked
# label in the furniture reverts to normal spacing and mixed case.
DEVA_FONT_NE = 'font-family:"Noto Sans Devanagari",Inter,sans-serif'
DEVA_CSS = """
.chip, .cover .lockup, .cover .foot, .ch-eyebrow, .toc .area, .syllabus .t,
.box .bt, .qs .grp, .chapsum h2, th, .runhead, .tile, .toc .hrs, figcaption .n
  { letter-spacing: normal !important; text-transform: none !important; }
/* Nepali books set every display string in Noto Sans Devanagari, the reference
   shaping for the script, instead of Poppins' secondary Devanagari set. */
.chip, .cover h1, .cover .lockup, .cover .foot, h1, h2, h3, h4, .toc, .about, .credits,
.qs .grp, .chapsum, .box .bt, .ch-eyebrow, .ch-num, .syllabus .t, .runhead, table, figcaption, .tile
  { font-family: "Noto Sans Devanagari", Poppins, sans-serif !important; }
figcaption .src { display:none; }
""".strip()

def chapter_html_for(u, body, subject, grade, L):
    i18n.CUR = i18n.for_title(u["title"], L)
    try:
        return chapter_html(u, body, subject, grade, 1)
    finally:
        i18n.CUR = L


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
<p class="sub">{L["credits_note"]}</p>
{''.join(rows)}
<p style="margin-top:6mm;font-size:8pt;color:#8a8f99">
{L["cr_foot"]}</p>
</section>"""


def build(slug, verbose=True):
    head, units = spine.load(slug)
    L = i18n.set_book(slug)
    DEVA_FONT = DEVA_FONT_NE if L["digits"] else ""
    subject, accent, grade = spine.meta_for(slug)
    photo.USED.clear()          # credits are per book, in order of first use
    code = head.get("code", "").split()[0] if head.get("code") else ""
    # Nepali books print nothing rather than a Latin code.
    if L["digits"] and code and not re.search(r"[\u0900-\u097F]", code):
        code = ""
    cdir = os.path.join(CONTENT, slug)
    present, bodies, figno = set(), {}, 1
    for u in units:
        p = os.path.join(cdir, f"unit-{u['no']:02d}.md")
        if not os.path.exists(p): continue
        txt = open(p, encoding="utf-8").read()
        if len(txt.strip()) < 400: continue
        i18n.CUR = i18n.for_title(u["title"], L)
        _, htm, figno = md2html.convert(txt, f"{slug}-u{u['no']}", figno)
        bodies[u["no"]] = localise_marks(htm)
        present.add(u["no"])
    i18n.CUR = L
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
<style>{DEVA_CSS if L["digits"] else ""}</style>
<style>{m3x.css_vars(accent)}
html{{string-set:booktitle "{esc(subject)} · {L["grade"].split(" ·")[0].format(g=i18n.num(grade))}"}}
@page{{@bottom-left{{content:"{L["footer"]}";{DEVA_FONT}}}@bottom-right{{content:counter(page{", devanagari" if L["digits"] else ""});{DEVA_FONT}}}@top-left{{{DEVA_FONT}}}@top-right{{{DEVA_FONT}}}}}
@page cover{{@top-left{{content:none}}@top-right{{content:none}}@bottom-left{{content:none}}@bottom-right{{content:none}}}}
@page frontmatter{{@bottom-right{{content:counter(page,{"devanagari" if L["digits"] else "lower-roman"});{DEVA_FONT}}}}}</style>
</head><body>
{cover_html(slug, subject, grade, accent, code, head)}
{front_html(subject, grade, head, units, exam_notes)}
{toc_html(units, present)}
{''.join(chapter_html_for(u, bodies[u['no']], subject, grade, L) for u in units if u['no'] in present)}
{''.join(extras)}
{credits_html(list(photo.USED))}
</body></html>"""
    os.makedirs(OUT, exist_ok=True)
    name = spine.pdf_name(slug)
    path = os.path.join(OUT, name)
    HTML(string=doc, base_url=HERE).write_pdf(path, stylesheets=[CSS(filename=THEME)],
                                             optimize_images=True, jpeg_quality=80, dpi=170)
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
