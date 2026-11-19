"""Build a Past Paper PDF: question paper (exam layout) followed by full solutions.

    python3 build_paper.py 12-phy-2082-general        # one paper (content/<id>.md)
    python3 build_paper.py --all                       # every paper + manifest.json

Source format: see PAPERS_TRACKER.md ("Paper source format").
"""
import os, re, sys, json, html as _html
HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.join(HERE, "..", "pipeline")
sys.path.insert(0, PIPE)
os.environ.setdefault("FIG_LINT", "0")
import md2html, mathsvg, figrun
from weasyprint import HTML, CSS

CONTENT = os.environ.get("PAPERS_CONTENT") or os.path.join(HERE, "content")
OUT = os.environ.get("PAPERS_OUT") or os.path.join(HERE, "pdf")
MARK = re.compile(r"\[\[([\d+.×x]+)\]\]")
ROMAN = re.compile(r"^\((i{1,3}|iv|v|अ|आ|इ|ई)\)\s")
PART = re.compile(r"^\(([a-eक-ङ])\)\s")
DEVA = False
NOTE_NE = "विद्यार्थीहरूले सकेसम्म आफ्नै शब्दमा उत्तर दिनुपर्ने छ । दायाँ किनारामा दिइएको अङ्कले पूर्णाङ्क जनाउँदछ ।"
DIG = str.maketrans("0123456789", "०१२३४५६७८९")


def front(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text.replace("\r\n", "\n"), re.S)
    meta = {}
    for ln in m.group(1).split("\n"):
        k, _, v = ln.partition(":")
        meta[k.strip()] = v.strip().strip('"')
    return meta, m.group(2)


def inline_imgs(src):
    """@img <file in figures/> | caption | width%  ->  an embedded figure (exact crop from the published sheet)."""
    import base64
    def rep(m):
        parts = [x.strip() for x in m.group(1).split("|")]
        f = parts[0]
        cap = parts[1] if len(parts) > 1 else ""
        w = parts[2] if len(parts) > 2 and parts[2] else "40"
        if f.endswith(".html"):
            raw = open(os.path.join(HERE, "figures", f), encoding="utf-8").read()
            c = f'<figcaption>{_html.escape(cap)}</figcaption>' if cap else ""
            return f'\n<figure class="nobreak photo">{raw}{c}</figure>\n'
        data = base64.b64encode(open(os.path.join(HERE, "figures", f), "rb").read()).decode()
        mime = "image/svg+xml" if f.endswith(".svg") else "image/png"
        c = f"<figcaption>{_html.escape(cap)}</figcaption>" if cap else ""
        return (f'\n<figure class="nobreak photo"><img src="data:{mime};base64,{data}" style="width:{w}%" alt="figure">{c}</figure>\n')
    return re.sub(r"^@img (.+?)\s*$", rep, src, flags=re.M)


def marks(s):
    return MARK.sub(lambda m: '<span class="marks">[%s]</span>' % (m.group(1).translate(DIG) if DEVA else m.group(1)), s)


def exam_markup(src):
    """@q N / (a) parts / (i) sub-parts / @or / @mcq N + @opts -> markdown with classed paragraphs."""
    out, num, first, buf = [], None, False, None
    after_or = False

    def flush():
        nonlocal buf
        if buf:
            out.append('\n<p class="%s" markdown="1">' % buf[1] + marks(buf[0]) + "</p>\n")
        buf = None

    for ln in src.split("\n"):
        s = ln.strip()
        if s.startswith("@q ") or s.startswith("@mcq "):
            flush(); num = s.split()[1]; first = True
            if s.startswith("@mcq "):
                buf = (f'<b class="qn">{num}.</b>', "part")
                first = False
                mc = True
            else:
                mc = False
            continue
        if s == "@or":
            flush(); out.append('\n<p class="or">Or</p>\n'); first = False; num = None; after_or = True; continue
        if s.startswith("@opts"):
            flush(); first = False; num = None
            col = s.startswith("@opts-col")
            opts = [o.strip() for o in s.split(" ", 1)[1].split("|")]
            cells = "".join(f'<span class="opt"><i>{chr(65+i)}</i>{marks(o)}</span>' for i, o in enumerate(opts))
            out.append(f'\n<p class="mcq-opts{" col" if col else ""}">{cells}</p>\n')
            continue
        if buf and buf[0].startswith('<b class="qn">') and not buf[0].count("\n") and PART.match(s) is None and ROMAN.match(s) is None and s and buf[1] == "part" and re.fullmatch(r'<b class="qn">\d+\.</b>', buf[0]):
            buf = (buf[0] + " " + s, "part"); continue
        m = PART.match(s)
        r = ROMAN.match(s)
        if s and not (m or r) and buf is None and after_or and not s.startswith(("#", "<", "`", "|", "@")):
            buf = (s, "part cont"); after_or = False; continue
        if s and not (m or r) and buf is None and first and num:
            buf = (f'<b class="qn">{num}.</b> ' + s, "part"); first = False; continue
        if m or r:
            flush(); after_or = False
            if r:
                if first and num:
                    buf = (f'<b class="qn">{num}.</b> ' + s, "part"); first = False
                else:
                    buf = (s, "sub")
            else:
                head = f'<b class="qn">{num}.</b> ' if first and num else ""
                first = False
                buf = (head + s, "part" if head or num is None or True else "part")
                if not head:
                    buf = (s, "part cont")
            continue
        if not s:
            flush(); out.append(""); continue
        if buf:
            buf = (buf[0] + "<br>" + s, buf[1])
        else:
            out.append(marks(ln))
    flush()
    return "\n".join(out)


def solution_markup(src):
    src = re.sub(r"^@s (\S+)\s*$", r'\n<p class="sq">Question \1</p>\n', src, flags=re.M)
    src = re.sub(r"\n(?=\(i{1,3}\)|Loop law|Dividing)", "\n\n", src)
    out = []
    for l in src.split("\n"):
        starts = l.startswith(("**(", "**Or", "- ", "1. "))
        if starts and out and out[-1].strip() and not (l[:2] in ("- ", "1.") and out[-1][:2] in ("- ", "1.")):
            out.append("")
        out.append(l)
    # keep the author's line breaks inside a paragraph (one reaction / step per line)
    res, fence, disp = [], False, False
    for i, l in enumerate(out):
        s = l.strip()
        if s.startswith("```"):
            fence = not fence
        if s == "$$" or (s.startswith("$$") and s.endswith("$$") is False and s.count("$$") == 1):
            disp = not disp
        nxt = out[i + 1].strip() if i + 1 < len(out) else ""
        plain = (s and nxt and not fence and not disp and not s.startswith(("|", "#", "```", "<", "$$", "@s")) and not nxt.startswith(("|", "#", "```", "<", "- ", "1. ", "$$", "@s", "**(", "**Or")) and not s.endswith("$$"))
        if plain and not s.startswith(("- ", "1. ")) or (plain and s.startswith(("- ", "1. ")) is False):
            l = l.rstrip() + "  "
        res.append(l)
    return marks("\n".join(res))


def render(pid):
    global DEVA
    meta, body = front(open(os.path.join(CONTENT, pid + ".md"), encoding="utf-8").read())
    DEVA = meta.get("lang") == "ne"
    secdeva = " deva" if DEVA else ""
    qsrc, _, ssrc = body.partition("<!-- SOLUTIONS -->")
    figno = 1
    qsrc, ssrc = inline_imgs(qsrc), inline_imgs(ssrc)
    _, qhtml, figno = md2html.convert(exam_markup(qsrc), pid + "-q", figno)
    _, shtml, figno = md2html.convert(solution_markup(ssrc), pid + "-s", figno)
    e = _html.escape
    stream = meta.get("stream", "")
    lvl = meta.get("level") or f'Grade {meta["grade"]}'
    title = f'{meta["subject"]}{(" · " + stream) if stream else ""}'
    who = meta.get("students", "")
    head = f"""<div class="pp-head"><div class="pp-brand"><span>NEBians</span><span>{e(lvl)}{(" · Sub. Code " + e(meta["code"])) if meta.get("code") else ""}</span></div>
<h1>{e(meta["subject"])}</h1><div class="yr">{e(lvl)} · {meta["year_bs"]} {meta.get("cal", "BS")} ({meta["year_ad"]} AD){(" · " + e(stream)) if stream else ""}</div>
{f'<p class="who">{e(who)}</p>' if who else ''}</div>
<div class="pp-meta"><span>Time: {e(meta["time"])}</span><span>Full Marks: {e(meta["marks"])}</span></div>
<p class="pp-note">{NOTE_NE if DEVA else "Candidates are required to give their answers in their own words as far as practicable. The figures in the margin indicate full marks. Attempt all the questions."}</p>"""
    running = f'{meta["subject"]} · {lvl} · {meta["year_bs"]}'
    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{e(title)} {meta["year_bs"]} | NEBians</title>
<style>html{{string-set:booktitle "{e(running)}"; }} .pp-head{{string-set:chaptitle "{e(meta.get("kind","Past Paper"))}"}} .sol{{string-set:chaptitle "Solutions"}}</style></head>
<body><section class="pp{secdeva}">{head}{qhtml}<div class="pp-end">End of paper</div></section>
<section class="pp sol{secdeva}"><h2>Solutions<small>{e(meta["subject"])} · {meta["year_bs"]} BS · {e(stream or "all students")}</small></h2>{shtml}</section></body></html>"""
    os.makedirs(OUT, exist_ok=True)
    name = meta["file"]
    path = os.path.join(OUT, name)
    HTML(string=doc, base_url=PIPE).write_pdf(path, stylesheets=[CSS(filename=os.path.join(PIPE, "theme.css")), CSS(filename=os.path.join(HERE, "paper.css"))],
                                             optimize_images=True, jpeg_quality=80, dpi=170)
    import fitz
    pages = len(fitz.open(path))
    meta.update(pages=pages, bytes=os.path.getsize(path), id=pid)
    print(f"{pid}: {name} pages={pages} {meta['bytes']/1e3:.0f} KB")
    return meta


def main(args):
    ids = [f[:-3] for f in sorted(os.listdir(CONTENT)) if f.endswith(".md")] if (not args or args == ["--all"]) else args
    metas = [render(i) for i in ids]
    if not args or args == ["--all"]:
        json.dump(metas, open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
    if mathsvg.FAILS:
        print("[math] fell back:", [t[:50] for t, _ in mathsvg.FAILS[:8]])
    if figrun.FAILS:
        print("[figures] failed:", [c for c, _ in figrun.FAILS][:5])


if __name__ == "__main__":
    main(sys.argv[1:])
