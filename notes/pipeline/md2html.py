"""NEBians chapter markdown -> styled HTML fragment."""
import base64, os, re, html as _html
import markdown as _md
import mathsvg, figrun

_PLACE = "\x00NEB{}\x00"

def _svg_data_uri(path):
    with open(path, "rb") as f:
        return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode()

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
        path, h, d = mathsvg.render(m.group(1), 10.2)
        out.append(f'<img class="im" src="{_svg_data_uri(path)}" '
                   f'style="vertical-align:-{d * 0.72 + 0.86:.2f}pt" alt="math">'
                   if path else "<code>" + _html.escape(m.group(1)) + "</code>")
        pos = m.end()
    out.append(_html.escape(text[pos:]))
    return "".join(out)

def _unused_inline_math_html(text: str) -> str:
    def rep(m):
        path, h, d = mathsvg.render(m.group(1), 10.2)
        if not path:
            return "<code>" + _html.escape(m.group(1)) + "</code>"
        return (f'<img class="im" src="{_svg_data_uri(path)}" '
                f'style="vertical-align:-{d * 0.72 + 0.86:.2f}pt" alt="math">')
    return _IMATH.sub(rep, text)

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

def _extract_display_math(body, store):
    def rep(m):
        tex = m.group(1)
        path, h, d = mathsvg.render(tex, 14.6, display=True)
        i = len(store)
        if not path:
            store.append(f'<div class="dm"><code>{_html.escape(tex.strip())}</code></div>')
        else:
            store.append(f'<div class="dm"><img src="{_svg_data_uri(path)}" '
                         f'alt="equation"></div>')
        return "\n\n" + _PLACE.format(i) + "\n\n"
    return _outside_code(body, lambda t: re.sub(r"\$\$(.+?)\$\$", rep, t, flags=re.S))

def _extract_inline_math(body, store):
    def rep(m):
        tex = m.group(1)
        path, h, d = mathsvg.render(tex, 10.2)
        i = len(store)
        if not path:
            store.append(f'<code>{_html.escape(tex)}</code>')
        else:
            store.append(f'<img class="im" src="{_svg_data_uri(path)}" '
                         f'style="vertical-align:-{d * 0.72 + 0.86:.2f}pt" alt="math">')
        return _PLACE.format(i)
    return _outside_code(
        body,
        lambda t: _IMATH.sub(rep, t))

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
        title = m.group(2).strip() or _BOXES.get(kind, kind.title())
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
    cols = "c4" if longest <= 15 else ("c2" if longest <= 38 else "c1")
    cells = "".join(f'<span class="opt"><i>{l}</i>{o}</span>'
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
        return (f'<section class="chsum">{head}{rest}</section>')
    return re.sub(
        r'(<h2[^>]*>\s*(?:Chapter summary|Summary|Unit summary)\s*</h2>)'
        r'(.*?)(?=<h2|<section|\Z)', rep, htm, flags=re.S | re.I)


def convert(text, chapter_id="", fig_no_start=1):
    meta, body = parse_front(text)
    store = []
    body = _extract_figures(body, store, chapter_id)
    body = _extract_display_math(body, store)
    body = _extract_inline_math(body, store)
    _find_leaks(body)
    body = _callouts(body)
    _MD.reset()
    htm = _MD.convert(body)
    for i, frag in enumerate(store):
        htm = htm.replace(_PLACE.format(i), frag)
    # number figures
    n = [fig_no_start]
    def fignum(m):
        s = m.group(0).replace("{CAP}", f"<b>Figure {n[0]}.</b> ")
        n[0] += 1
        return s
    htm = re.sub(r"<figcaption>\{CAP\}.*?</figcaption>", fignum, htm, flags=re.S)
    htm = htm.replace("{CAP}", "")
    # style question sections
    htm = re.sub(r"<h2([^>]*)>\s*((?:Practice|Exercise|Review|Model|Self)[^<]*)</h2>",
                 r'<h2\1 class="qs">\2</h2>', htm, flags=re.I)
    htm = _frame_summary(htm)
    htm = _restructure_questions(htm)
    htm = _split_answer_runs(htm)
    return meta, htm, n[0]
