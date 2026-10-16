"""Typeset a Nepali formula as HTML text instead of sending it to mathtext.

mathtext draws glyph by glyph: it cannot shape Devanagari conjuncts, it puts
matras in the wrong place, and its maths fonts carry no Devanagari glyphs at
all — `\\text{जनघनत्व}` arrives in the PDF as a row of dummy boxes. A formula
whose terms are Nepali words is really running text with a few operators, so
it is set in the book's own Devanagari font and the one genuinely
two-dimensional construct, the fraction, is built from stacked inline blocks.
"""
import html as _html
import re

DEVA = re.compile(r"[\u0900-\u097F]")

# What a school formula actually uses. Anything else is dropped rather than
# printed as a stray command name.
SYM = {
    r"\times": "×", r"\div": "÷", r"\cdot": "·", r"\pm": "±", r"\mp": "∓",
    r"\approx": "≈", r"\neq": "≠", r"\ne": "≠", r"\leq": "≤", r"\le": "≤",
    r"\geq": "≥", r"\ge": "≥", r"\rightarrow": "→", r"\to": "→",
    r"\Rightarrow": "⇒", r"\leftarrow": "←", r"\infty": "∞", r"\degree": "°",
    r"\circ": "°", r"\%": "%", r"\&": "&", r"\#": "#", r"\$": "$",
    r"\{": "{", r"\}": "}", r"\sum": "∑", r"\ldots": "…", r"\dots": "…",
    r"\,": "\u2009", r"\;": "\u2009", r"\:": "\u2009", r"\!": "",
    r"\quad": "\u2003", r"\qquad": "\u2003\u2003", r"\ ": " ",
}
_SYM_KEYS = sorted(SYM, key=len, reverse=True)
_TEXTY = re.compile(r"\\(?:text|textrm|textbf|mathrm|mathbf|mathit|operatorname)\s*\{")
_DROP = re.compile(r"\\(?:left|right|displaystyle|limits|big|Big|bigg|Bigg)[lrm]?")


def _group(s, i):
    """Content and end index of the brace group that starts at s[i] == '{'."""
    depth, j = 0, i
    while j < len(s):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    return s[i + 1:], len(s)


def _next_group(s, i):
    """Skip blanks, then take either a brace group or a single character."""
    while i < len(s) and s[i] in " \t":
        i += 1
    if i < len(s) and s[i] == "{":
        return _group(s, i)
    if i < len(s):
        return s[i], i + 1
    return "", i


def convert(tex):
    """Render a Devanagari-bearing TeX fragment as inline HTML."""
    s = tex.strip()
    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == "\\":
            m = _TEXTY.match(s, i)
            if m:
                body, i = _group(s, m.end() - 1)
                out.append(convert(body))
                continue
            if s.startswith(r"\frac", i) or s.startswith(r"\dfrac", i):
                num, i = _next_group(s, i + (6 if s[i + 1] == "d" else 5))
                den, i = _next_group(s, i)
                out.append('<span class="fr"><span class="fn">%s</span>'
                           '<span class="fd">%s</span></span>'
                           % (convert(num), convert(den)))
                continue
            if s.startswith(r"\sqrt", i):
                arg, i = _next_group(s, i + 5)
                out.append('<span class="sq">√<span class="sqb">%s</span></span>'
                           % convert(arg))
                continue
            m = _DROP.match(s, i)
            if m:
                i = m.end()
                continue
            for k in _SYM_KEYS:
                if s.startswith(k, i):
                    out.append(_html.escape(SYM[k]))
                    i += len(k)
                    break
            else:                                   # unknown command: drop it
                m = re.match(r"\\[A-Za-z]+", s[i:])
                i += len(m.group(0)) if m else 2
            continue
        if c in "^_":
            arg, i = _next_group(s, i + 1)
            tag = "sup" if c == "^" else "sub"
            out.append("<%s>%s</%s>" % (tag, convert(arg), tag))
            continue
        if c in "{}":
            i += 1
            continue
        if c == "=":
            out.append(" = ")
            i += 1
            continue
        out.append(_html.escape(c))
        i += 1
    return re.sub(r"\s{2,}", " ", "".join(out))


def html(tex, display=False):
    cls = "eqx eqd" if display else "eqx"
    return '<span class="%s">%s</span>' % (cls, convert(tex))
