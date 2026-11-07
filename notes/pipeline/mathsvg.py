"""Render LaTeX math to inline SVG via matplotlib mathtext. Cached on disk by hash."""
import hashlib, os, re, warnings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.mathtext import MathTextParser
from matplotlib.font_manager import FontProperties

warnings.filterwarnings("ignore")
matplotlib.rcParams["mathtext.fontset"] = "stix"
matplotlib.rcParams["svg.fonttype"] = "path"   # embed outlines: no font deps in PDF

CACHE = os.path.join(os.path.dirname(__file__), "..", "figures", "_math")
os.makedirs(CACHE, exist_ok=True)
_parser = MathTextParser("path")
FAILS = []

# mathtext places glyphs one by one: it cannot shape Devanagari conjuncts or
# position matras, and STIX has no Devanagari glyphs at all. Nepali formulas
# are therefore typeset as HTML text by devaeqn.py, never sent here.
DEVA = re.compile(r"[\u0900-\u097F]")

# A display equation wider than the text column is not an error — CSS shrinks it
# to fit — but it lands on the page as a strip of 6pt type nobody can read. The
# fix belongs in the source (break it at an `=`), so record it and let check.py
# fail the file.
OVERWIDE = []
COLUMN_IN = 6.93        # A4 210mm less 17mm margins each side

# Common LaTeX that mathtext does not know -> safe equivalents
_FIX = [
    (r"\\left\s*\|", "|"), (r"\\right\s*\|", "|"),
    (r"\\lvert", "|"), (r"\\rvert", "|"),
    (r"\\left\s*\.", ""), (r"\\right\s*\.", ""),
    (r"\\(bigg?|Bigg?)[lrm]?", ""), (r"\\limits", ""),
    (r"\\iff", r"\\Leftrightarrow"), (r"\\implies", r"\\Rightarrow"),
    (r"\\displaystyle", ""), (r"\\!", ""), (r"\\,", r"\\ "), (r"\;", r"\\ "),
    (r"\\qquad", r"\\ \\ \\ \\ "), (r"\\quad", r"\\ \\ "),
    (r"\\mathrm\b", r"\\mathdefault"), (r"\\textrm\b", r"\\text"),
    (r"\\mbox\b", r"\\text"), (r"\\operatorname\b", r"\\mathdefault"),
    (r"\\dfrac", r"\\frac"), (r"\\tfrac", r"\\frac"),
    (r"\\ce\b", r"\\text"), (r"\\degree", r"^\\circ"), (r"\\micro", r"\\mu"),
    (r"\\textbf\b", r"\\mathbf"), (r"\\textit\b", r"\\mathit"),
    (r"\\le\b", r"\\leq"), (r"\\ge\b", r"\\geq"),
    (r"\\ne\b", r"\\neq"), (r"\\to\b", r"\\rightarrow"),
    (r"\\nonumber", ""), (r"\\notag", ""), (r"\\label\{[^}]*\}", ""),
]

_DIGIT_ARG = re.compile(r"\\(frac|binom)\s*([0-9a-zA-Z])\s*([0-9a-zA-Z])")

def _strip_wrapper(s: str, name: str) -> str:
    """Remove \\name{...} keeping its argument, brace-balanced."""
    out, i, tok = [], 0, "\\\\" + name + "{"
    while True:
        j = s.find(tok.replace("\\\\", "\\"), i)
        if j < 0:
            out.append(s[i:]); break
        out.append(s[i:j])
        k = j + len(name) + 2; depth = 1
        while k < len(s) and depth:
            if s[k] == "{": depth += 1
            elif s[k] == "}": depth -= 1
            k += 1
        out.append(s[j + len(name) + 2: k - 1])
        i = k
    return "".join(out)


def _take_arg(s: str, i: int):
    """Read one TeX argument at s[i:] (after spaces): a {group}, a \\command or one char.
    Returns (inner_text, next_index) or (None, i)."""
    while i < len(s) and s[i] == " ":
        i += 1
    if i >= len(s):
        return None, i
    if s[i] == "{":
        depth, k = 1, i + 1
        while k < len(s) and depth:
            depth += (s[k] == "{") - (s[k] == "}")
            k += 1
        return s[i + 1:k - 1], k
    if s[i] == "\\":
        m = re.match(r"\\[a-zA-Z]+", s[i:])
        if m:
            return m.group(), i + m.end()
    return s[i], i + 1

def _norm_args(s: str) -> str:
    """\\frac 1{12} -> \\frac{1}{12}; \\sqrt 9 -> \\sqrt{9} (TeX shorthand mathtext rejects)."""
    out, i = [], 0
    pat = re.compile(r"\\(frac|binom|sqrt)(?![a-zA-Z])")
    while True:
        m = pat.search(s, i)
        if not m:
            out.append(s[i:]); break
        out.append(s[i:m.start()])
        name, j = m.group(1), m.end()
        if name == "sqrt":
            k = j
            while k < len(s) and s[k] == " ":
                k += 1
            if k < len(s) and s[k] == "[":      # \\sqrt[n]{x}: leave alone
                out.append("\\sqrt"); i = j; continue
            a, k = _take_arg(s, j)
            if a is None:
                out.append("\\sqrt"); i = j; continue
            out.append("\\sqrt{" + _norm_args(a) + "}"); i = k
        else:
            a, k = _take_arg(s, j)
            b, k2 = _take_arg(s, k) if a is not None else (None, k)
            if a is None or b is None:
                out.append("\\" + name); i = j; continue
            out.append("\\" + name + "{" + _norm_args(a) + "}{" + _norm_args(b) + "}"); i = k2
    return "".join(out)

def _stack(items, style=""):
    """Stack cells vertically with nested \\genfrac (mathtext has no matrix)."""
    if len(items) == 1:
        return items[0]
    return "\\genfrac{}{}{0}{" + style + "}{" + _stack(items[:-1], style) + "}{" + items[-1] + "}"

_MATRIX = re.compile(r"\\begin\{([pbvBV]?)matrix\}(.*?)\\end\{\1matrix\}")

def _matrices(s: str) -> str:
    """pmatrix/bmatrix/vmatrix -> brackets around columns of stacked cells."""
    br = {"p": ("(", ")"), "b": ("[", "]"), "v": ("\\\\vert", "\\\\vert"), "": ("", ""),
          "B": ("\\{", "\\}"), "V": ("\\|", "\\|")}
    def one(m):
        rows = [[c.strip() for c in r.split("&")] for r in re.split(r"\\\\", m.group(2)) if r.strip()]
        ncol = max(len(r) for r in rows)
        rows = [r + [""] * (ncol - len(r)) for r in rows]
        cols = ["\\ ".join([]) or _stack([r[c] or "\\ " for r in rows], "0" if len(rows) > 2 else "") for c in range(ncol)]
        body = "\\ \\ ".join(cols)
        l, r = br[m.group(1)]
        return ("\\left" + l if l else "") + body + ("\\right" + r if r else "")
    prev = None
    while prev != s:
        prev, s = s, _MATRIX.sub(one, s)
    return s

def _clean(tex: str) -> str:
    s = tex.strip().strip("$").strip()
    # `\ge1` is read as a command named "ge1"; a command butted against a
    # digit always needs the space mathtext expects.
    s = re.sub(r"(\\[a-zA-Z]+)(?=[0-9])", r"\1 ", s)
    s = re.sub(r"\s+", " ", s)                 # mathtext cannot span newlines
    s = _matrices(s)
    for name in ("boxed", "mbox", "textnormal", "ensuremath", "phantom"):
        s = _strip_wrapper(s, name)
    for pat, rep in _FIX:
        s = re.sub(pat, rep, s)
    s = _norm_args(s)
    s = _DIGIT_ARG.sub(r"\\\1{\2}{\3}", s)   # \frac12 -> \frac{1}{2} (after \tfrac->\frac)
    # strip alignment environments mathtext cannot parse
    s = re.sub(r"\\begin\{(aligned|align\*?|gather\*?|split|equation\*?)\}", "", s)
    s = re.sub(r"\\end\{(aligned|align\*?|gather\*?|split|equation\*?)\}", "", s)
    # `\\` is a line break only when it really ends a line. An author who
    # typed `\\approx` meant `\approx`; left alone the next rule would turn it
    # into the literal word "approx" and check.py would not notice.
    s = re.sub(r"\\\\(?=[A-Za-z])", r"\\", s)
    s = s.replace("&", "").replace("\\\\", "\\ \\ ")
    return s.strip()

def render(tex: str, fontsize: float = 11.0, display: bool = False, color: str = "#14181f"):
    """Return (svg_path, height_px, depth_px) or (None, 0, 0) if unrenderable."""
    s = _clean(tex)
    if not s:
        return None, 0, 0
    key = hashlib.sha1(f"{s}|{fontsize}|{display}|{color}|v8".encode()).hexdigest()[:20]
    out = os.path.join(CACHE, key + ".svg")
    meta = out + ".meta"
    if os.path.exists(out) and os.path.exists(meta):
        # A concurrent writer may have created the file but not yet filled it.
        # Treat a short/partial read as a cache miss and re-render rather than
        # crashing the whole chapter (audit.py runs 12 of these in parallel).
        parts = open(meta).read().split()
        if len(parts) >= 2:
            h, d = float(parts[0]), float(parts[1])
            if display and len(parts) > 2 and float(parts[2]) / 100.0 > COLUMN_IN:
                OVERWIDE.append((tex, float(parts[2]) / 100.0 * 25.4))
            return out, h, d
    prop = FontProperties(size=fontsize)
    expr = "$" + s + "$"
    try:
        w, h, d, _, _ = _parser.parse(expr, dpi=100, prop=prop)
    except Exception as e:
        FAILS.append((tex, str(e)[:160]))
        return None, 0, 0
    if display and w / 100.0 > COLUMN_IN:
        OVERWIDE.append((tex, w / 100.0 * 25.4))
    try:
        pad = 1.2   # px; md2html and svgkit lower the image by exactly this pad plus the depth
        W, H = max(w, 1) + 2 * pad, max(h, 1) + 2 * pad
        fig = plt.figure(figsize=(W / 100.0, H / 100.0), dpi=100)
        fig.patch.set_alpha(0.0)
        fig.text(pad / W, (d + pad) / H, expr, fontsize=fontsize,
                 va="baseline", ha="left", color=color)
        # Write both files atomically: a reader in another process must never
        # observe a half-written SVG or an empty .meta.
        tmp = f"{out}.{os.getpid()}.tmp"
        fig.savefig(tmp, format="svg", transparent=True)
        plt.close(fig)
        os.replace(tmp, out)
    except Exception as e:
        FAILS.append((tex, str(e)[:160]))
        plt.close("all")
        return None, 0, 0
    mtmp = f"{meta}.{os.getpid()}.tmp"
    with open(mtmp, "w") as fh:
        fh.write(f"{h} {d} {w}")
    os.replace(mtmp, meta)
    return out, h, d

