"""Typeset LaTeX to inline SVG with MathJax (Computer Modern outlines). Cached on disk by hash.

The old backend was matplotlib mathtext: no aligned/cases/array, STIX glyphs that did not
match the book, and every multi-step solution collapsed into one line. MathJax gives the
TeX the books were authored in (aligned, cases, matrices, \\text, mhchem `\\ce`, cancel) and
the look of a printed textbook.

A single Node process (`mathjax/mj_server.cjs`) answers one JSON line per formula. Results are
cached by hash, so a rebuild only typesets what changed. API kept from the old backend:
`render(tex, fontsize, display, color) -> (svg_path, height_px, depth_px)` where px are 100 dpi
pixels, the SVG is padded by exactly 1.2 px and callers lower the image by depth + pad.
"""
import atexit, hashlib, json, os, re, subprocess, threading

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "figures", "_math")
os.makedirs(CACHE, exist_ok=True)
SERVER = os.path.join(HERE, "mathjax", "mj_server.cjs")
VERSION = "mj3"
FAILS = []

# Nepali formulas are typeset as HTML text by devaeqn.py, never sent here.
DEVA = re.compile(r"[\u0900-\u097F]")

# A display equation wider than the text column is shrunk by CSS and lands as 6 pt type.
# Record it so check.py fails the file; `derive()` normally prevents it by breaking at `=`.
OVERWIDE = []
COLUMN_IN = 6.93        # A4 210 mm less 17 mm margins each side
COLUMN_MM = COLUMN_IN * 25.4
PAD_PX = 1.2            # md2html / svgkit lower the image by depth + this pad
PX_PT = 0.72            # one 100 dpi px in pt
SCALE = 1.06            # Computer Modern sits a little small beside Source Serif 4

# ---------------------------------------------------------------- node process
_proc = None
_lock = threading.Lock()


def _start():
    global _proc
    _proc = subprocess.Popen(["node", SERVER], cwd=os.path.join(HERE, "mathjax"),
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL, text=True, bufsize=1)


def _stop():
    if _proc and _proc.poll() is None:
        try:
            _proc.stdin.close(); _proc.wait(timeout=3)
        except Exception:
            _proc.kill()


atexit.register(_stop)


def _ask(tex, display):
    with _lock:
        for attempt in (0, 1):
            if _proc is None or _proc.poll() is not None:
                _start()
            try:
                _proc.stdin.write(json.dumps({"tex": tex, "display": bool(display)}) + "\n")
                _proc.stdin.flush()
                line = _proc.stdout.readline()
                if line:
                    return json.loads(line)
            except (BrokenPipeError, OSError, ValueError):
                pass
            try:
                _proc.kill()
            except Exception:
                pass
        return {"ok": False, "err": "mathjax server not running (cd notes/pipeline/mathjax && npm ci)"}


# ---------------------------------------------------------------- source cleanup
def _clean(tex: str, display: bool = False) -> str:
    """Light normalisation. MathJax takes real LaTeX, so almost nothing is rewritten."""
    s = tex.strip().strip("$").strip()
    s = re.sub(r"\\label\{[^}]*\}", "", s)
    s = re.sub(r"\\(nonumber|notag)\b", "", s)
    s = s.replace("\\mathdefault", "\\mathrm")
    s = re.sub(r"\\(dfrac|tfrac)\b", r"\\frac", s) if not display else s
    # `\\` outside an environment is a line break: give it one so rows align
    if "\\\\" in s and "\\begin" not in s:
        s = ("\\begin{aligned}" + s + "\\end{aligned}") if "&" in s else \
            ("\\begin{gathered}" + s + "\\end{gathered}")
    return s.strip()


# ---------------------------------------------------------------- derivations
_BREAKS = [(r"\Longleftrightarrow", "arrow"), (r"\Leftrightarrow", "arrow"), (r"\iff", "arrow"),
           (r"\Longrightarrow", "arrow"), (r"\Rightarrow", "arrow"), (r"\implies", "arrow"),
           (r"=", "eq")]


def _top_breaks(s):
    """Positions (index, token, kind) of relation signs at brace depth 0, outside \\left..\\right."""
    out, depth, lr, i, n = [], 0, 0, 0, len(s)
    while i < n:
        c = s[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == "\\":
            m = re.match(r"\\[a-zA-Z]+", s[i:])
            if m:
                name = m.group()
                if name == "\\left":
                    lr += 1
                elif name == "\\right":
                    lr -= 1
                elif depth == 0 and lr == 0:
                    for tok, kind in _BREAKS:
                        if kind == "arrow" and name == tok:
                            out.append((i, tok, kind)); break
                i += len(name); continue
            i += 2; continue
        elif c == "=" and depth == 0 and lr == 0:
            prev = s[i - 1] if i else ""
            if prev not in "<>!:":
                out.append((i, "=", "eq"))
        i += 1
    return out


def chain_links(tex: str) -> int:
    """How many relation signs a formula chains (a = b = c has 2)."""
    s = _clean(tex)
    if "\\begin" in s or "\\\\" in s:
        return 0
    return len(_top_breaks(s))


def derive(tex: str, min_links: int = 2) -> str:
    """Turn `a = b = c = d` (or an implication chain) into an aligned multi-line derivation."""
    s = _clean(tex)
    if "\\begin" in s or "\\\\" in s or "&" in s:
        return s
    br = _top_breaks(s)
    if len(br) < min_links:
        return s
    # first segment, then (op, segment) pairs
    segs, ops, last = [], [], 0
    for idx, tok, kind in br:
        segs.append(s[last:idx].strip())
        ops.append((tok, kind))
        last = idx + len(tok)
    segs.append(s[last:].strip())
    if any(not x for x in segs[1:]):
        return s
    lines = []
    if ops[0][1] == "eq":
        lines.append(f"{segs[0]} &= {segs[1]}")
        rest = list(zip(ops[1:], segs[2:]))
    else:
        lines.append("&" + segs[0])
        rest = list(zip(ops, segs[1:]))
    for (tok, kind), seg in rest:
        lines.append(f"&{'=' if kind == 'eq' else tok + chr(92) + ' '} {seg}")
    return "\\begin{aligned}" + " \\\\ ".join(lines) + "\\end{aligned}"


# ---------------------------------------------------------------- rendering
_VB = re.compile(r'viewBox="\s*([-0-9.eE]+)\s+([-0-9.eE]+)\s+([-0-9.eE]+)\s+([-0-9.eE]+)\s*"')


def _finish(svg, fontsize, color):
    """MathJax svg -> padded pt-sized svg. Returns (svg, height_px, depth_px, width_px)."""
    m = _VB.search(svg)
    if not m:
        return None
    x0, y0, w, h = (float(v) for v in m.groups())
    k = fontsize * SCALE / 1000.0            # pt per MathJax unit (1 em = 1000 units)
    pad_u = PAD_PX * PX_PT / k               # padding in MathJax units
    height_u, depth_u = max(0.0, -y0), max(0.0, y0 + h)
    body = svg[svg.index(">", svg.index("<svg")) + 1:]
    body = body.replace("currentColor", color)
    W, H = (w + 2 * pad_u), (h + 2 * pad_u)
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W * k:.3f}pt" height="{H * k:.3f}pt" '
           f'viewBox="{x0 - pad_u:.2f} {y0 - pad_u:.2f} {W:.2f} {H:.2f}">{body}')
    to_px = k / PX_PT
    return out, height_u * to_px, depth_u * to_px, w * to_px


def render_info(tex: str, fontsize: float = 11.0, display: bool = False, color: str = "#14181f"):
    """Return (svg_path, height_px, depth_px, width_px), or (None, 0, 0, 0) if unrenderable."""
    s = _clean(tex, display)
    if not s:
        return None, 0, 0, 0
    key = hashlib.sha1(f"{s}|{fontsize}|{display}|{color}|{VERSION}".encode()).hexdigest()[:20]
    out = os.path.join(CACHE, key + ".svg")
    meta = out + ".meta"
    if os.path.exists(out) and os.path.exists(meta):
        parts = open(meta).read().split()
        if len(parts) >= 3:
            h, d, w = float(parts[0]), float(parts[1]), float(parts[2])
            if display and w / 100.0 > COLUMN_IN:
                OVERWIDE.append((tex, w / 100.0 * 25.4))
            return out, h, d, w
    res = _ask(s, display)
    if not res.get("ok"):
        FAILS.append((tex, str(res.get("err", ""))[:160]))
        return None, 0, 0, 0
    fin = _finish(res["svg"], fontsize, color)
    if not fin:
        FAILS.append((tex, "no viewBox"))
        return None, 0, 0, 0
    svg, h, d, w = fin
    if display and w / 100.0 > COLUMN_IN:
        OVERWIDE.append((tex, w / 100.0 * 25.4))
    tmp = f"{out}.{os.getpid()}.tmp"
    with open(tmp, "w") as fh:
        fh.write(svg)
    os.replace(tmp, out)
    mtmp = f"{meta}.{os.getpid()}.tmp"
    with open(mtmp, "w") as fh:
        fh.write(f"{h} {d} {w}")
    os.replace(mtmp, meta)
    return out, h, d, w


def render(tex: str, fontsize: float = 11.0, display: bool = False, color: str = "#14181f"):
    """Return (svg_path, height_px, depth_px) or (None, 0, 0) if unrenderable."""
    p, h, d, _ = render_info(tex, fontsize, display, color)
    return p, h, d


def width_mm(tex: str, fontsize: float = 10.7, display: bool = False) -> float:
    p, h, d, w = render_info(tex, fontsize, display)
    return w / 100.0 * 25.4 if p else 0.0


# ---------------------------------------------------------------- formula sheets
_EDGE = re.compile(r"^(?:\\[ ,;:!]|\\q?quad|\s)+|(?:\\[ ,;:!]|\\q?quad|\s)+$")


def split_sheet(tex: str):
    """`f_1 ; f_2 ; f_3` (semicolons at depth 0) -> [f_1, f_2, f_3]; [] when it is one formula.
    Authors and the maths migration chain a whole fact sheet into a single $...$."""
    s = tex.strip().strip("$").strip()
    if "\\begin" in s or "\\\\" in s:
        return []
    parts, depth, lr, last, i, n = [], 0, 0, 0, 0, len(s)
    while i < n:
        c = s[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == "\\":
            m = re.match(r"\\[a-zA-Z]+", s[i:])
            if m:
                if m.group() == "\\left":
                    lr += 1
                elif m.group() == "\\right":
                    lr -= 1
                i += len(m.group()); continue
            i += 2; continue
        elif c == ";" and depth == 0 and lr == 0:
            parts.append(s[last:i]); last = i + 1
        i += 1
    parts.append(s[last:])
    parts = [_EDGE.sub("", x).strip() for x in parts]
    parts = [x for x in parts if x]
    plain = sum(len(re.sub(r"\\[a-zA-Z]+|[{}\s]", "", x)) for x in parts)
    if len(parts) < 2 or (len(parts) == 2 and plain < 44):
        return []
    return parts
