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
    (r"\\le(?![a-zA-Z])", r"\\leq"), (r"\\ge(?![a-zA-Z])", r"\\geq"),
    (r"\\ne(?![a-zA-Z])", r"\\neq"), (r"\\to(?![a-zA-Z])", r"\\rightarrow"),
    (r"\\nonumber", ""), (r"\\notag", ""), (r"\\label\{[^}]*\}", ""),
]

_DIGIT_ARG = re.compile(r"\\(frac|binom)\s*([0-9a-zA-Z])\s*([0-9a-zA-Z])")
# `\sqrt3` and `\sqrt x` both parse in no matplotlib version; the braced form
# parses in every one. Repair the unbraced single-token argument here so an
# author's slip cannot fail a whole chapter at build time.
_SQRT_ARG = re.compile(r"\\sqrt\s*([0-9a-zA-Z])(?![0-9a-zA-Z{])")

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

def _clean(tex: str) -> str:
    s = tex.strip().strip("$").strip()
    s = re.sub(r"\s+", " ", s)                 # mathtext cannot span newlines
    for name in ("boxed", "mbox", "textnormal", "ensuremath", "phantom"):
        s = _strip_wrapper(s, name)
    for pat, rep in _FIX:
        s = re.sub(pat, rep, s)
    s = _DIGIT_ARG.sub(r"\\\1{\2}{\3}", s)   # \frac12 -> \frac{1}{2} (after \tfrac->\frac)
    s = _SQRT_ARG.sub(r"\\sqrt{\1}", s)       # \sqrt3 -> \sqrt{3}, \sqrt x -> \sqrt{x}
    # strip alignment environments mathtext cannot parse
    s = re.sub(r"\\begin\{(aligned|align\*?|gather\*?|split|equation\*?)\}", "", s)
    s = re.sub(r"\\end\{(aligned|align\*?|gather\*?|split|equation\*?)\}", "", s)
    # `\\` is a line break only when it really ends a line. An author who
    # typed `\\approx` meant `\approx`; left alone the next rule would turn it
    # into the literal word "approx" and check.py would not notice.
    s = re.sub(r"\\\\(?=[A-Za-z])", r"\\", s)
    s = s.replace("&", "").replace("\\\\", "\\ \\ ")
    return s.strip()

def render(tex: str, fontsize: float = 11.0, display: bool = False):
    """Return (svg_path, height_px, depth_px) or (None, 0, 0) if unrenderable."""
    s = _clean(tex)
    if not s:
        return None, 0, 0
    key = hashlib.sha1(f"{s}|{fontsize}|{display}|v4".encode()).hexdigest()[:20]
    out = os.path.join(CACHE, key + ".svg")
    meta = out + ".meta"
    if os.path.exists(out) and os.path.exists(meta):
        parts = open(meta).read().split()
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
        fig = plt.figure(figsize=(max(w, 1) / 100.0, max(h, 1) / 100.0), dpi=100)
        fig.patch.set_alpha(0.0)
        fig.text(0, d / h if h else 0, expr, fontsize=fontsize,
                 va="baseline", ha="left", color="#14181f")
        fig.savefig(out, format="svg", transparent=True,
                    bbox_inches="tight", pad_inches=0.012)
        plt.close(fig)
    except Exception as e:
        FAILS.append((tex, str(e)[:160]))
        plt.close("all")
        return None, 0, 0
    open(meta, "w").write(f"{h} {d} {w}")
    return out, h, d
