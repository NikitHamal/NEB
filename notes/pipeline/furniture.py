"""Page furniture of a NEBians book: cover, about page, contents, chapter opener.

Pure HTML builders; every look lives in theme.css. build_pdf.py calls these.
"""
import html as _html, re
import i18n, m3x


def esc(s):
    return _html.escape(str(s))


def _brand(L):
    return "नेबियन्स" if L["digits"] else "NEBians"


def cover_html(slug, subject, grade, accent, code, head):
    L = i18n.CUR
    g = L["grade"].format(g=i18n.num(grade))
    parts = [p.strip() for p in g.split(" · ")]
    chips = "".join(f'<span class="chip {"solid" if i == 0 else ""}">{esc(p)}</span>'
                    for i, p in enumerate(parts))
    if code:
        chips += f'<span class="chip">{esc(L["code"])} {esc(code)}</span>'
    n = len(subject)
    size = 46 if n <= 22 else 40 if n <= 36 else 33 if n <= 60 else 27
    return f"""<section class="cover">{m3x.cover_art(slug, accent)}
<div class="inner">
  <div class="lockup">{m3x.mark_svg(m3x.tones(accent)["cover"], 8.4)}<span>{_brand(L)}</span></div>
  <div class="titleblock">
    <div class="chips">{chips}</div>
    <h1 style="font-size:{size}pt">{esc(subject)}</h1>
  </div>
  <div class="foot"><span class="chip">{L["edition"]}</span><span class="url">nebians.consica.com.np</span></div>
</div></section>"""


def front_html(subject, grade, head, units, exam_notes):
    L = i18n.CUR
    areas = []
    for u in units:
        if u["area"] and (not areas or areas[-1][0] != u["area"]):
            areas.append((u["area"], []))
        if areas:
            areas[-1][1].append(u)
    rows = "".join(
        f'<tr><td>{esc(a)}</td><td>{i18n.num(len(us))}</td>'
        f'<td>{i18n.num(sum(int(x["hours"]) for x in us if x["hours"])) if any(x["hours"] for x in us) else "·"}</td></tr>'
        for a, us in areas)
    exam = "".join(f"<li>{esc(n)}</li>" for n in exam_notes)
    def _tile(x):
        m = re.match(r"\s*<strong>(.*?)</strong>(.*)$", x, flags=re.S)
        return (f'<div class="tile"><b class="th">{m.group(1)}</b>{m.group(2).strip()}</div>'
                if m else f'<div class="tile">{x}</div>')
    tiles = "".join(_tile(x) for x in L["org_li"])
    th = "".join(f"<th>{x}</th>" for x in L["th"])
    return f"""<section class="frontmatter about">
<h1 class="fm-title">{L["front_title"]}</h1>
<p class="fm-lead">{L["front_lead"].format(subject=esc(subject), g=i18n.num(grade))}</p>

<h2>{L["org_h"]}</h2>
<p>{L["org_p"]}</p>
<div class="tiles">{tiles}</div>

<h2>{L["cover_h"]}</h2>
<table class="soft"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table>

<h2>{L["exam_h"]}</h2>
<div class="card"><ul>{exam}</ul></div>

<div class="box caution"><div class="bt">{L["read"]}</div>
<p>{L["disclaimer"]}</p></div>

<p class="fm-edition"><span class="chip">{L["edition"]}</span> {L["prep"]}</p>
</section>"""


def toc_html(units, present):
    L = i18n.CUR
    out, cur = [f'<section class="frontmatter toc"><h2>{L["contents"]}</h2>'], None
    for u in units:
        if u["no"] not in present:
            continue
        if u["area"] != cur:
            cur = u["area"]
            if cur:
                out.append(f'<div class="area"><span class="chip">{esc(cur)}</span></div>')
        hrs = (f' <span class="hrs">{i18n.num(u["hours"])}{L["hrs"]}</span>' if u["hours"] else "")
        out.append(f'<a href="#u{u["no"]}"><span class="n">{i18n.num(u["no"])}</span>'
                   f'<span class="tt">{esc(u["title"])}{hrs}</span></a>')
    out.append("</section>")
    return "".join(out)


def chapter_html(u, body, subject, grade, fig_start=1):
    L = i18n.CUR
    syl = "".join(f"<li>{esc(s)}</li>" for s in u["sub"])
    sylbox = (f'<div class="syllabus"><div class="t">{L["syl"]}</div><ul>{syl}</ul></div>'
              if syl else "")
    chips = ""
    if u["area"]:
        chips += f'<span class="chip">{esc(u["area"])}</span>'
    if u["hours"]:
        chips += f'<span class="chip">{i18n.num(u["hours"])} {L["teaching_hours"]}</span>'
    return f"""<section class="chapter" id="u{u['no']}">
<div class="ch-head"><div class="ch-num">{i18n.num(u['no'])}</div>
<div class="ch-text"><div class="ch-eyebrow">{L["unit"]} {i18n.num(u['no'])}</div>
<h1>{esc(u['title'])}</h1></div></div>
<div class="ch-chips">{chips}</div>
{sylbox}
{body}
</section>"""
