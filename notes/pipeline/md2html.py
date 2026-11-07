"""NEBians chapter markdown -> styled HTML fragment."""
import base64, os, re, html as _html
import markdown as _md
import mathsvg
import devaeqn, figrun, photo, assets, i18n, svgkit, readflow, plainlift

_PLACE = "\x00NEB{}\x00"

def _svg_data_uri(path):
    with open(path, "rb") as f:
        return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode()


def _png_uri(path):
    """PNGs go in by file URL, not base64 — a photo is ~0.5 MB and WeasyPrint
    can then share one decoded copy between every place it appears."""
    return "file://" + os.path.abspath(path)

# ---------- frontmatter ----------
def parse_front(text):
    meta, body = {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if m:
        body = text[m.end():]
        key = None
        for line in m.group(1).split("\n"):
            if re.match(r"^\s*-\s+", line) and key:
                meta.setdefault(key, []) if not isinstance(meta.get(key), list) else None
                if not isinstance(meta.get(key), list):
                    meta[key] = []
                meta[key].append(re.sub(r"^\s*-\s+", "", line).strip().strip('"\''))
            elif ":" in line:
                k, v = line.split(":", 1)
                key = k.strip()
                v = v.strip().strip('"\'')
                meta[key] = v if v else []
    return meta, body

# ---------- extraction passes ----------
def _extract_figures(body, store, chapter_id):
    def rep(m):
        info, code = m.group(1) or "", m.group(2)
        cap = re.search(r'caption\s*=\s*"([^"]*)"', info)
        wide = "wide" in info
        path = figrun.run(code, chapter_id)
        if not path:
            return ""
        i = len(store)
        style = ' style="max-width:100%"' if wide else ""
        store.append(
            f'<figure class="nobreak"><img src="{_svg_data_uri(path)}"{style} alt="figure">'
            + (f'<figcaption>{{CAP}}{_inline_math_html(cap.group(1))}</figcaption>' if cap else "")
            + "</figure>")
        return "\n\n" + _PLACE.format(i) + "\n\n"
    return re.sub(r"^```figure([^\n]*)\n(.*?)^```\s*$", rep, body, flags=re.S | re.M)


def _extract_svgfigs(body, store, chapter_id):
    """```svgfig label="1.1" caption="…"  + svgkit code -> numbered vector figure (no matplotlib)."""
    def rep(m):
        info, code = m.group(1) or "", m.group(2)
        cap = re.search(r'caption\s*=\s*"([^"]*)"', info)
        lab = re.search(r'label\s*=\s*"([^"]*)"', info)
        try:
            svg = svgkit.render(code, f"{chapter_id}:{lab.group(1) if lab else '?'}")
        except Exception as e:
            svgkit.WARN.append(f"{chapter_id}: svgfig failed: {e}")
            raise
        uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
        i = len(store)
        c = (f'<figcaption><b>{_html.escape(("Figure " + lab.group(1) + ".") if lab else "Figure.")}</b> '
             f'{_inline_math_html(cap.group(1))}</figcaption>') if cap else ""
        store.append(f'<figure class="nobreak diagram"><img src="{uri}" alt="diagram">{c}</figure>')
        return "\n\n" + _PLACE.format(i) + "\n\n"
    return re.sub(r"^```svgfig([^\n]*)\n(.*?)^```\s*$", rep, body, flags=re.S | re.M)


def _extract_photogrids(body, store, chapter_id):
    """```photogrid cols="3" caption="…" ratio="1.25"  — N-up horizontal strip / grid.

    Items are separated by lines starting with ``@``::
        @ photo id="bca101/ram" cap="DDR4 DIMM" fit="1.3"   (then overlay directives)
        @ svg cap="Block diagram"                           (then svgkit code)
    Photos are rendered through photo.render (crop/fit/mark/call/label/key), so a
    cell can carry numbered callouts; svg cells draw with svgkit.
    """
    def rep(m):
        info, code = m.group(1) or "", m.group(2)
        at = photo.parse_attrs(info)
        cols = max(1, int(at.get("cols", "3")))
        ratio = at.get("ratio", "1.3")
        parts = re.split(r"(?m)^@\s+", code)[1:]
        cells, credits, keys_all = [], [], []
        per_w = 100.0 / cols * 0.96
        for k, part in enumerate(parts):
            head, _, script = part.partition("\n")
            kind, _, rest = head.partition(" ")
            a = photo.parse_attrs(rest)
            cap = a.get("cap", "")
            if kind.strip() == "svg":
                svg = svgkit.render(script, f"{chapter_id}:grid{k}")
                uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
                img = f'<img src="{uri}" alt="diagram">'
            else:
                aid = a.get("id", "")
                fit = a.get("fit", ratio)
                sc = f"fit {fit}\n" + script
                path = photo.render(aid, sc, a.get("w", per_w))
                if not path:
                    return ""
                img = f'<img class="gp" src="{_png_uri(path)}" alt="photograph">'
                rec = assets.record(aid) or {}
                if rec:
                    credits.append(f'({chr(97 + k)}) {_html.escape(re.sub(r"\s*\(.*?\)\s*|\s*:.*$", " ", rec.get("author") or "unknown").strip()[:42])}, '
                                   f'{_html.escape(rec.get("license", ""))}')
                _, keys, _o = photo.parse_script(script)
                keys_all += keys
            cap = re.sub(r"^\(" + chr(97 + k) + r"\)\s*", "", cap)   # the letter is added below; drop a hand-typed duplicate
            cells.append(f'<td class="gc">{img}<div class="gcap"><b>({chr(97 + k)})</b> '
                         f'{_inline_math_html(cap)}</div></td>')
        rows = [cells[i:i + cols] for i in range(0, len(cells), cols)]
        trs = ""
        for r in rows:
            r += ['<td class="gc"></td>'] * (cols - len(r))
            trs += "<tr>" + "".join(r) + "</tr>"
        cap = at.get("caption", "")
        i = len(store)
        store.append(
            f'<figure class="nobreak photo grid"><table class="pgrid"><tbody>{trs}</tbody></table>'
            + photo.key_html(keys_all)
            + (f'<figcaption>' + (f'<b>Plate {_html.escape(at["label"])}.</b> ' if at.get("label") else "{CAP}") + f'{_inline_math_html(cap)}'
               + (f'<span class="src">Photo credits: {"; ".join(credits)}.</span>' if credits else "")
               + "</figcaption>" if cap else "")
            + "</figure>")
        return "\n\n" + _PLACE.format(i) + "\n\n"
    return re.sub(r"^```photogrid([^\n]*)\n(.*?)^```\s*$", rep, body, flags=re.S | re.M)


def _extract_photos(body, store, chapter_id):
    """```photo id="slug/name" caption="…" width="86"  + overlay directives."""
    def rep(m):
        info, script = m.group(1) or "", m.group(2)
        at = photo.parse_attrs(info)
        aid = at.get("id", "").strip()
        if not aid:
            photo.FAILS.append((chapter_id, "photo block with no id="))
            return ""
        try:
            wpct = float(at.get("width", "88"))
        except ValueError:
            wpct = 88.0
        path = photo.render(aid, script, wpct)
        if not path:
            return ""
        _, keys, _ = photo.parse_script(script)
        rec = assets.record(aid) or {}
        src_note = ""
        if rec:
            who = rec.get("author") or "unknown"
            src_note = (f'<span class="src">{i18n.CUR['source']} {_html.escape(who[:70])} / '
                        f'{_html.escape(rec.get("source", ""))} '
                        f'({_html.escape(rec.get("license", ""))})</span>')
        cap = re.search(r'caption\s*=\s*"([^"]*)"', info)
        i = len(store)
        store.append(
            f'<figure class="nobreak photo">'
            f'<img src="{_png_uri(path)}" style="width:{wpct:.0f}%" alt="photograph">'
            + photo.key_html(keys)
            + (f'<figcaption>{{CAP}}{_inline_math_html(cap.group(1))} {src_note}</figcaption>'
               if cap else (f"<figcaption>{src_note}</figcaption>" if src_note else ""))
            + "</figure>")
        return "\n\n" + _PLACE.format(i) + "\n\n"
    return re.sub(r"^```photo([^\n]*)\n(.*?)^```\s*$", rep, body, flags=re.S | re.M)

# Inline math may be hard-wrapped across a line break in the source. It must
# not run past a blank line or into a new block construct, or one stray `$`
# would swallow the rest of the section.
_MB_LINE = r"[^\$\n]*"
# A continuation may not cross a blank line or start a new block. A wrapped
# formula often continues with "+ ..." or "- ...", so list markers are not a
# stop; the span is instead capped at four source lines.
_MB_NL = r"\n(?![ \t]*(?:\n|:::|\#{1,6} |```|~~~|\||>))"
_MATH_BODY = _MB_LINE + r"(?:" + _MB_NL + _MB_LINE + r"){0,3}?"
_IMATH = re.compile(r"(?<!\$)\$(?!\$)(" + _MATH_BODY + r")(?<!\$)\$(?!\$)")

def _inline_math_html(text: str) -> str:
    """Render $...$ in a RAW string; HTML-escape only the non-math segments."""
    out, pos = [], 0
    for m in _IMATH.finditer(text):
        out.append(_html.escape(text[pos:m.start()]))
        if devaeqn.DEVA.search(m.group(1)):
            out.append(devaeqn.html(m.group(1)))
            pos = m.end()
            continue
        out.append(_inline_one(m.group(1)))
        pos = m.end()
    out.append(_html.escape(text[pos:]))
    res = "".join(out)
    # captions are not run through Markdown: honour *emphasis* and **strong** here
    res = re.sub(r"\*\*([^*\s][^*]*?)\*\*", r"<strong>\1</strong>", res)
    return re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"<em>\1</em>", res)

# Regions where $...$ must NOT be treated as math: fenced code blocks and
# inline code spans (PHP, shell and JS all use $ as ordinary syntax).
_CODE_REGION = re.compile(r"(^```.*?^```[^\n]*$|^~~~.*?^~~~[^\n]*$|`[^`\n]+`)",
                          re.S | re.M)

def _outside_code(body, fn):
    """Apply fn to the parts of body that are not inside code."""
    parts = _CODE_REGION.split(body)
    for i in range(0, len(parts), 2):          # even indices are non-code
        parts[i] = fn(parts[i])
    return "".join(parts)

def _math_img(tex, size, display=False, cls="im", derive_min=None):
    """One formula as an inline SVG <img>, or None when MathJax rejects it.
    `derive_min`: break `a = b = c` into aligned lines when it chains at least this many signs."""
    src = mathsvg.derive(tex, derive_min) if derive_min else tex
    path, h, d, w = mathsvg.render_info(src, size, display)
    if not path:
        return None
    ca = f' class="{cls}"' if cls else ""
    return (f'<img{ca} data-w="{w / 100.0 * 25.4:.1f}" src="{_svg_data_uri(path)}" '
            f'style="vertical-align:-{d * 0.72 + 0.86:.2f}pt" alt="math">')


# A formula that is long enough to need several lines is a derivation, not a clause.
_DERIVE_CHARS = 26
_WRAP_MM = 150.0     # an inline formula wider than this would run off the line


def _inline_one(tex):
    """HTML for one $...$ span. Short formulas stay in the sentence; chains of `=` and long
    formulas become an aligned block so a step reads as working, not as one long line."""
    if devaeqn.DEVA.search(tex):
        return devaeqn.html(tex)
    parts = mathsvg.split_sheet(tex)
    if parts:
        html = _sheet(parts)
        if html:
            return html
    facts = readflow.split_commas(tex)
    if facts:
        return '<span class="cl">' + ", ".join(_inline_one(f) for f in facts) + "</span>"
    links = mathsvg.chain_links(tex)
    plain = re.sub(r"\\[a-zA-Z]+|[{}\s]", "", tex)
    if links >= 2 and len(plain) >= _DERIVE_CHARS:
        img = _math_img(tex, 11.4, display=True, cls="dvi", derive_min=2)
        if img:
            return f'<span class="dv">{img}</span>'
    elif links >= 1 and mathsvg.width_mm(tex, 10.7) > _WRAP_MM:
        img = _math_img(tex, 11.4, display=True, cls="dvi", derive_min=1)
        if img:
            return f'<span class="dv">{img}</span>'
    img = _math_img(tex, 10.7)
    if img and _TALL.search(tex):
        w = float(re.search(r'data-w="([0-9.]+)"', img).group(1))
        if w >= 24:          # readflow.promote_tall may set it on its own line
            img = img.replace("<img ", f'<img data-t="{_html.escape(tex, quote=True)}" ', 1)
    return img or f'<code>{_html.escape(tex)}</code>'


_TALL = re.compile(r"\\(?:frac|dfrac|int|sum|prod|lim|binom|begin)")


def _extract_display_math(body, store):
    def rep(m):
        tex = m.group(1)
        i = len(store)
        if devaeqn.DEVA.search(tex):
            # A formula written in Nepali words is running text, not maths:
            # typeset it in the book's Devanagari font (see devaeqn.py).
            store.append('<div class="dm">%s</div>' % devaeqn.html(tex, True))
            return "\n\n" + _PLACE.format(i) + "\n\n"
        wide = mathsvg.width_mm(tex, 15.4, display=True) > mathsvg.COLUMN_MM * 0.92
        img = _math_img(tex, 15.4, display=True, cls="", derive_min=1 if wide else 2)
        if not img:
            store.append(f'<div class="dm"><code>{_html.escape(tex.strip())}</code></div>')
        else:
            store.append(f'<div class="dm">{img}</div>')
        return "\n\n" + _PLACE.format(i) + "\n\n"
    return _outside_code(body, lambda t: re.sub(r"\$\$(.+?)\$\$", rep, t, flags=re.S))


def _sheet(parts):
    """A fact sheet: every formula in its own cell, on a grid of equal columns."""
    cells, widest = [], 0.0
    for t in parts:
        if devaeqn.DEVA.search(t):
            return None
        img = _math_img(t, 11.2, display=True, cls="fxm", derive_min=2)
        if not img:
            return None
        widest = max(widest, mathsvg.width_mm(mathsvg.derive(t, 2), 11.2, display=True))
        cells.append(f"<span>{img}</span>")
    cols = "c3" if widest <= 50 else ("c2" if widest <= 80 else "c1")
    n, k = len(cells), int(cols[1])
    r = n % k if k > 1 else 0
    # the last row is filled edge to edge: a lone cell spans the row, two cells share it
    for j in range(n - r, n):
        if r:
            cells[j] = cells[j].replace("<span>", f'<span class="w{r}">', 1)
    return f'<span class="fxs {cols}">' + "".join(cells) + "</span>"


# Three or more formulas in a row, separated only by spaces ("$a^m a^n=a^{m+n}$ $(a^m)^n=a^{mn}$ ..."),
# are a formula sheet as well.
_FRUN = re.compile(r"(?<![\w$])((?:(?<!\$)\$(?!\$)[^$\n]+?(?<!\$)\$(?!\$)[ \t]+){2,}(?<!\$)\$(?!\$)[^$\n]+?(?<!\$)\$(?!\$))(?![\w$])")
_FONE = re.compile(r"(?<!\$)\$(?!\$)([^$\n]+?)(?<!\$)\$(?!\$)")
SHEETS = set()


def _extract_formula_runs(body, store):
    def rep(m):
        html = _sheet(_FONE.findall(m.group(1)))
        if not html:
            return m.group(0)
        i = len(store)
        store.append(html); SHEETS.add(i)
        return _PLACE.format(i)
    def line(t):
        return "\n".join(ln if ln.lstrip().startswith("|") else _FRUN.sub(rep, ln) for ln in t.split("\n"))
    return _outside_code(body, line)


def _extract_inline_math(body, store):
    def rep(m):
        i = len(store)
        store.append(_inline_one(m.group(1)))
        return _PLACE.format(i)
    body = _extract_formula_runs(body, store)
    body = _outside_code(body, lambda t: _IMATH.sub(rep, t))
    # the sentence-ending mark after a sheet would hang alone on the next line
    for i, frag in enumerate(store):
        if frag.startswith('<span class="fxs'):
            body = re.sub(re.escape(_PLACE.format(i)) + r"[ \t]*[.,;:](?=\s|$)", _PLACE.format(i), body)
    return body

LEAKS = []   # unpaired `$` left in the body: raw LaTeX would reach the PDF

def _find_leaks(body):
    """Record any `$` still outside a code region after math extraction."""
    def scan(t):
        for ln in t.split("\n"):
            if "$" in ln:
                LEAKS.append(ln.strip()[:110])
        return t
    _outside_code(body, scan)


_BOXES = {"key": "Key point", "example": "Worked example", "caution": "Common mistake",
          "tip": "Exam tip", "definition": "Definition", "derivation": "Derivation",
          "note": "Note", "memory": "Remember"}

def _callouts(body):
    """::: type Optional title  ...  :::"""
    out, lines, i = [], body.split("\n"), 0
    while i < len(lines):
        m = re.match(r"^:::\s*(\w+)\s*(.*)$", lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        kind = m.group(1).lower()
        title = m.group(2).strip() or i18n.CUR['boxes'].get(kind, kind.title())
        cls = kind if kind in _BOXES else "note"
        inner, i = [], i + 1
        depth = 1
        while i < len(lines):
            if re.match(r"^:::\s*\w+", lines[i]): depth += 1
            elif re.match(r"^:::\s*$", lines[i]):
                depth -= 1
                if depth == 0: i += 1; break
            inner.append(lines[i]); i += 1
        out.append(f'<div class="box {cls}" markdown="1"><div class="bt">'
                   f'{_html.escape(title)}</div>')
        out.extend(inner)
        out.append("</div>")
    return "\n".join(out)

_MD = _md.Markdown(extensions=["tables", "attr_list", "fenced_code", "md_in_html",
                               "sane_lists", "def_list", "footnotes", "abbr"],
                   extension_configs={"footnotes": {"PLACE_MARKER": "///FN///"}})

# ---------- question / answer layout ----------
# Authors write MCQ options and multi-part questions as one inline run,
# "(a) ... (b) ... (c) ... (d) ...". Set on a justified page that reads as a
# wall of text, so split the run into real option/part blocks here rather than
# asking 144 chapters to change their markup.
_LABEL = re.compile(r"\(([a-e])\)")
_TAGS = re.compile(r"<[^>]+>")


def _mm_len(frag):
    """Printed width of an option in mm: 1.8 mm a character plus the real width of each formula."""
    w = sum(float(x) for x in re.findall(r'data-w="([0-9.]+)"', frag))
    return w + 1.8 * len(_TAGS.sub("", re.sub(r"<img[^>]*>", "", frag)).strip()) + 7


def _plain_len(frag):
    """Visible length, counting each math image as the glyphs it stands for."""
    return len(_TAGS.sub("\u00b7\u00b7\u00b7", frag).strip())


def _label_run(inner):
    """Longest run of labels starting at (a) and stepping a, b, c, ...  """
    run = []
    for m in _LABEL.finditer(inner):
        want = chr(ord("a") + len(run))
        if m.group(1) == want:
            run.append(m)
        elif m.group(1) == "a" and not run:
            run = [m]
    return run if len(run) >= 2 else []


def _split_question(inner):
    run = _label_run(inner)
    if not run:
        return None
    stem = inner[:run[0].start()].rstrip()
    opts = [inner[run[i].end():(run[i + 1].start() if i + 1 < len(run) else len(inner))]
            .strip() for i in range(len(run))]
    if not all(o for o in opts):
        return None
    labels = [m.group(1) for m in run]
    # a sub-part carries its own mark allocation, or is simply long prose
    longest = max(_plain_len(o) for o in opts)
    if (len(run) < 3 or any('class="marks"' in o for o in opts)
            or longest > 78):
        parts = "".join(f'<span class="part"><i>({l})</i> {o}</span>'
                        for l, o in zip(labels, opts))
        return f'{stem}<span class="parts">{parts}</span>'
    mm = max(_mm_len(o) for o in opts)
    cols = "c4" if mm <= 36 else ("c3" if mm <= 50 and len(run) % 3 == 0 else ("c2" if mm <= 80 else "c1"))
    cells = "".join(f'<span class="opt"><i>{l}</i><span class="ob">{o}</span></span>'
                    for l, o in zip(labels, opts))
    return f'{stem}<span class="opts {cols}">{cells}</span>'


_LI = re.compile(r"(<li>)(.*?)(</li>)", re.S)


def _restructure_questions(htm):
    def li(m):
        new = _split_question(m.group(2))
        return m.group(1) + (new if new else m.group(2)) + m.group(3)
    return _LI.sub(li, htm)


# Answer keys are written one answer per source line; markdown joins them into
# a single justified paragraph. Give each numbered answer its own line back.
_ANSP = re.compile(r"<p>(<strong>\d+\.(?:</strong>|\s).*?)</p>", re.S)
_ANUM = re.compile(r"(?=<strong>\d+\.(?:</strong>|\s))")


def _split_answer_runs(htm):
    """Answer keys are written one answer per source line; markdown joins them
    into a single justified paragraph. Give each numbered answer its line back."""
    def para(m):
        chunks = [c.strip() for c in _ANUM.split(m.group(1)) if c.strip()]
        if len(chunks) < 2:
            return m.group(0)
        return "".join(f'<p class="ansline">{c}</p>' for c in chunks)
    return _ANSP.sub(para, htm)


# The chapter summary is the highest-value page in a chapter; give it a frame.
def _frame_summary(htm):
    def rep(m):
        head, rest = m.group(1), m.group(2)
        # A summary whose points are short is set two to a row: the page then
        # shows the whole chapter at a glance instead of a long thin column.
        items = re.findall(r"<li>(.*?)</li>", rest, re.S)
        if items:
            plain = [re.sub(r"<[^>]+>", "", t) for t in items]
            if len(items) >= 4 and sum(len(t) for t in plain) / len(plain) <= 118:
                rest = rest.replace("<ul>", '<ul class="cols2">', 1)
        return (f'<section class="chsum">{head}{rest}</section>')
    return re.sub(
        r'(<h2[^>]*>\s*(?:' + i18n.CUR["summary_re"] + r')\s*</h2>)'
        r'(.*?)(?=<h2|<section|\Z)', rep, htm, flags=re.S | re.I)


# ---------- solutions: parts, derivation tails, ragged maths paragraphs ----------
_ANSLINE = re.compile(r'<p(?: class="[^"]*")?>(<strong>\d+\.(?:</strong>|\s).*?)</p>', re.S)


_SENT = re.compile(r"(?<!\bRs)(?<!e\.g)(?<!i\.e)(?<!\bNo)(?<!\bvs)(?<!etc)(?<!\bFig)\.\s+(?=<img class=\"(?:im|dvi)\"|<em>|<strong>|[A-Z])")


def _sentences(text):
    """An answer that makes several statements gets one line per statement."""
    if "dvt" in text or "fxs" in text:
        return text
    bits = _SENT.split(text.strip())
    if len(bits) < 2 or sum(1 for b in bits if "<img" in b) < 2:
        return text
    last = len(bits) - 1
    return "".join(f'<span class="stp">{b}{"." if i < last else ""}</span>' for i, b in enumerate(bits))


def _answer_parts(htm):
    """`1. (a) ... (b) ... (c) ...` in an answer key: one line per part."""
    def one(m):
        inner = m.group(1)
        run = _label_run(inner)
        if not run:
            mm = re.match(r"(<strong>\d+\.</strong>)\s*(.*)$", inner, re.S)
            if not mm:
                return m.group(0)
            body = _sentences(mm.group(2))
            if body == mm.group(2):
                return m.group(0)
            return f'<p class="ansline np hm">{mm.group(1)}<span class="stps">{body}</span></p>'
        stem = inner[:run[0].start()].rstrip()
        opts = [inner[run[i].end():(run[i + 1].start() if i + 1 < len(run) else len(inner))].strip()
                for i in range(len(run))]
        if not all(opts):
            return m.group(0)
        parts = "".join(f'<span class="part"><i>({r.group(1)})</i> {_sentences(o)}</span>'
                        for r, o in zip(run, opts))
        np_ = " np" if re.fullmatch(r"<strong>\d+\.</strong>", stem) else ""
        return f'<p class="ansline{np_} hm">{stem}<span class="parts">{parts}</span></p>'
    return _ANSLINE.sub(one, htm)


_TAIL = re.compile(
    r'(<span class="dv"><img[^>]*></span>)'
    r'((?:[^<]|<img\b[^>]*>|</?(?:strong|em|b|i)>)*?)'
    r'(?:(\.)(?=\s|<|$)|(?=</p>|</li>|</span>|<span class="(?:dv|part)|<br|<div|</div|$))')


def _derivation_tails(htm):
    """`<derivation> , so x < 2.` -> the conclusion sits on its own line under the working
    instead of dangling after a comma."""
    htm = re.sub(r'(<span class="dv"><img[^>]*></span>)\s*[.,;]+\s*', r'\1', htm)

    def one(m):
        tail = m.group(2).strip().lstrip(",;: ").strip()
        plain = _TAGS.sub("", tail).strip()
        if not plain or len(plain) > 170 or m.group(0).count("<img") > 6:
            return m.group(0)
        return f'{m.group(1)}<span class="dvt">{tail}{m.group(3) or ""}</span>'
    return _TAIL.sub(one, htm)


_HM = re.compile(r'<(p|li)>((?:(?!</\1>).)*?class="(?:im|dvi|fxm)".*?)</\1>', re.S)


def _ragged_maths(htm):
    """A paragraph holding formulas is set ragged-right (a justified line stretches its words
    around the unbreakable formula)."""
    return _HM.sub(lambda m: f'<{m.group(1)} class="hm">{m.group(2)}</{m.group(1)}>', htm)


def _layout_fixes(htm):
    """m3x print fixes: (1) a heading never strands at a page foot before an unbreakable
    figure or table (wrap the pair in .hk, break-inside:avoid); (2) tables with many
    columns get a denser class so they stay inside the page."""
    def dense(m):
        tbl = m.group(0)
        if 'class="pgrid"' in tbl[:60]:
            return tbl
        first = re.search(r"<tr>.*?</tr>", tbl, flags=re.S)
        cols = len(re.findall(r"<t[hd]\b", first.group(0))) if first else 0
        cls = "dense2" if cols >= 9 else ("dense" if cols >= 7 else "")
        if cls and 'class="' not in tbl[:30]:
            return tbl.replace("<table", '<table class="%s"' % cls, 1)
        return tbl
    htm = re.sub(r"<table\b.*?</table>", dense, htm, flags=re.S)
    pat = re.compile(r"(<h[234]\b[^>]*>(?:(?!</h[234]>).)*</h[234]>\s*)((?:<p>\s*)?(?:<(?:figure|table)\b.*?</(?:figure|table)>|<div class=.dm.>.*?</div>)(?:\s*</p>)?)", re.S)
    htm = pat.sub(lambda m: '<div class="hk">' + m.group(1) + m.group(2) + '</div>', htm)
    return htm

def convert(text, chapter_id="", fig_no_start=1):
    meta, body = parse_front(text)
    body = plainlift.lift(body)
    store = []
    body = _extract_figures(body, store, chapter_id)
    body = _extract_svgfigs(body, store, chapter_id)
    body = _extract_photogrids(body, store, chapter_id)
    body = _extract_photos(body, store, chapter_id)
    body = _extract_display_math(body, store)
    body = _extract_inline_math(body, store)
    _find_leaks(body)
    body = readflow.blank_before_lists(body)
    body = _callouts(body)
    # Python-Markdown's list regex uses \d, which also matches Devanagari
    # digits, so a bullet written "- १. text" became a nested <ol> that
    # restarted at a Latin "1." for every item. Escape the dot so the number
    # stays literal text after the bullet.
    body = re.sub(r"(?m)^(\s*[-*+]\s+)([\u0966-\u096F]+)\.(\s)", r"\1\2\\.\3", body)
    _MD.reset()
    htm = _MD.convert(body)
    for i, frag in enumerate(store):
        htm = htm.replace(_PLACE.format(i), frag)
    # number figures
    n = [fig_no_start]
    def fignum(m):
        s = m.group(0).replace("{CAP}", f"<b>{i18n.CUR['figure']} {i18n.num(n[0])}.</b> ")
        n[0] += 1
        return s
    htm = re.sub(r"<figcaption>\{CAP\}.*?</figcaption>", fignum, htm, flags=re.S)
    htm = htm.replace("{CAP}", "")
    # style question sections
    htm = re.sub(r"<h2([^>]*)>\s*((?:" + i18n.CUR["qs_re"] + r")[^<]*)</h2>",
                 r'<h2\1 class="qs">\2</h2>', htm, flags=re.I)
    htm = re.sub(r"<li>(?=[\u0966-\u096F]+\.)", '<li class="num">', htm)
    htm = _frame_summary(htm)
    htm = _restructure_questions(htm)
    htm = _split_answer_runs(htm)
    htm = readflow.promote_tall(htm)
    htm = _derivation_tails(htm)
    htm = _answer_parts(htm)
    htm = readflow.example_steps(htm)
    htm = readflow.structure_prose(htm)
    htm = readflow.sheet_paragraphs(htm)
    htm = readflow.keep_with_next(htm)
    htm = readflow.align_tables(htm)
    htm = _ragged_maths(htm)
    # WeasyPrint ignores <ol start="N">: a list resumed after a display
    # equation would restart at 1. Mirror the attribute with a counter reset.
    htm = re.sub(r'<ol start="(\d+)"(?![^>]*style=)>',
                 lambda m: f'<ol start="{m.group(1)}" style="counter-reset:list-item {int(m.group(1)) - 1}">',
                 htm)
    htm = _layout_fixes(htm)
    return meta, htm, n[0]
