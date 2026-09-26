import os
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
#!/usr/bin/env python3
"""Renders app/.../ResourceBannerArt.kt by transpiling it, so the preview is
literally the shipping code rather than a transcription of it."""
import math, re, os
from PIL import Image, ImageDraw

KT = os.path.join(_ROOT, "app/src/main/java/com/neb/ians/ui/components/ResourceBannerArt.kt")
COLOR_KT = os.path.join(_ROOT, "app/src/main/java/com/neb/ians/ui/theme/Color.kt")
SS = 4  # supersample

# ---------------------------------------------------------------- colour ----
class Color:
    __slots__ = ("r", "g", "b", "a")
    def __init__(self, r, g, b, a=1.0):
        self.r, self.g, self.b, self.a = r, g, b, a
    @staticmethod
    def hex(v):
        return Color(((v >> 16) & 255) / 255, ((v >> 8) & 255) / 255, (v & 255) / 255,
                     ((v >> 24) & 255) / 255 if v > 0xFFFFFF else 1.0)
    def copy(self, alpha=None):
        return Color(self.r, self.g, self.b, self.a if alpha is None else alpha)
    def rgba(self):
        return (int(self.r * 255 + .5), int(self.g * 255 + .5), int(self.b * 255 + .5),
                int(self.a * 255 + .5))

def lerp(a, b, t):
    return Color(a.r + (b.r - a.r) * t, a.g + (b.g - a.g) * t, a.b + (b.b - a.b) * t,
                 a.a + (b.a - a.a) * t)

WHITE = Color(1, 1, 1)

# --------------------------------------------------------- subject hues -----
def load_hues():
    src = open(COLOR_KT).read()
    block = src[src.index("private val SubjectHues"):]
    block = block[:block.index("\n)")]
    hues = {}
    for m in re.finditer(r'"([^"]+)" to SubjectHue\(', block):
        vals = re.findall(r"0x([0-9A-Fa-f]{8})", block[m.end():m.end() + 260])[:6]
        hues[m.group(1)] = [Color.hex(int(v, 16)) for v in vals]
    return hues

HUES = load_hues()

def load_tokens():
    """Brand.B40 and friends: the ramps the subject hues are written in."""
    src = open(COLOR_KT).read()
    out = {}
    for om in re.finditer(r"(?:internal |private )?object (\w+) \{([\s\S]*?)\n\}", src):
        ns = om.group(1)
        for vm in re.finditer(r"val (\w+)\s*=\s*Color\(0x([0-9A-Fa-f]{8})\)", om.group(2)):
            out[ns + "." + vm.group(1)] = Color.hex(int(vm.group(2), 16))
    return out

TOKENS = load_tokens()

def _hue_args(text):
    """The six colours of one SubjectHue(...) argument list, whether they are
    written as hex literals or as ramp tokens."""
    out = []
    for m in re.finditer(r"Color\(0x([0-9A-Fa-f]{8})\)|((?:Brand|Steel|Violet|Neutral|NeutralVariant)\.\w+)", text):
        if m.group(1):
            out.append(Color.hex(int(m.group(1), 16)))
        else:
            out.append(TOKENS[m.group(2)])
    return out[:6]

def _decl_block(src, decl):
    blk = src[src.index(decl):]
    return blk[:blk.index("\n)")]

def load_family_keywords():
    blk = _decl_block(open(COLOR_KT).read(), "private val SubjectFamilyKeywords")
    out = []
    for m in re.finditer(r"SubjectFamily\.(\w+) to listOf\(([\s\S]*?)\)", blk):
        out.append((m.group(1), re.findall(r'"([^"]*)"', m.group(2))))
    return out

def load_brand_hue():
    blk = _decl_block(open(COLOR_KT).read(), "private val BrandSubjectHue")
    h = _hue_args(blk)
    assert len(h) == 6, blk
    return h

def load_family_hues():
    blk = _decl_block(open(COLOR_KT).read(), "private val SubjectFamilyHues")
    blk = re.sub(r"//[^\n]*", "", blk)
    hits = [(m.start(), m.group(1)) for m in re.finditer(r"SubjectFamily\.(\w+) to", blk)]
    out = {}
    for k, (pos, fam) in enumerate(hits):
        end = hits[k + 1][0] if k + 1 < len(hits) else len(blk)
        val = blk[pos:end]
        g = re.search(r'SubjectHues\.getValue\("([^"]+)"\)', val)
        if g:
            out[fam] = HUES[g.group(1)]
        elif "BrandSubjectHue" in val:
            out[fam] = "BRAND"
        else:
            h = _hue_args(val)
            assert len(h) == 6, (fam, val)
            out[fam] = h
    return out

FAM_KEYWORDS = load_family_keywords()
BRAND_HUE = load_brand_hue()
FAM_HUES = load_family_hues()
for _k, _v in list(FAM_HUES.items()):
    if _v == "BRAND":
        FAM_HUES[_k] = BRAND_HUE

def subject_family(subject):
    t = subject.strip().lower()
    if not t:
        return "GENERAL"
    for fam, kws in FAM_KEYWORDS:
        for kw in kws:
            if kw in t:
                return fam
    return "GENERAL"

def subject_hue(subject):
    if subject in HUES:
        return HUES[subject]
    for k, v in HUES.items():
        if k.lower() == subject.strip().lower():
            return v
    return FAM_HUES.get(subject_family(subject), BRAND_HUE)
SURFACE_LIGHT = Color.hex(0xFFF5F6F8)
SURFACE_DARK = Color.hex(0xFF0B1C30)

class Palette:
    def __init__(self, top, bottom, ink, paper, field):
        self.top, self.bottom, self.ink, self.paper, self.field = top, bottom, ink, paper, field

class _Theme:
    def __init__(self, color, container): self.color, self.container = color, container

def _palette_exprs():
    """Pull the four colour expressions for each mode straight out of
    bannerPalette() so the preview cannot drift from the shipping palette."""
    src = open(KT).read()
    body = src[src.index("fun bannerPalette("):]
    body = body[:body.index("\n}")]
    blocks = re.findall(r"BannerPalette\(([^;]*?)\n\s*\)", body)
    out = []
    for blk in blocks:
        blk = re.sub(r"//[^\n]*", "", blk)
        parts = re.findall(r"(top|bottom|ink|paper|field)\s*=\s*([^\n]+?),?\s*\n", blk + "\n")
        d = {}
        for k, v in parts:
            v = re.sub(r"(\d)f\b", r"\1", v.strip().rstrip(","))
            v = v.replace("Color.White", "WHITE").replace("theme.", "t.")
            d[k] = v
        out.append(d)
    assert len(out) == 2, out
    return out  # [dark, light]

PAL_DARK, PAL_LIGHT = _palette_exprs()

def banner_palette(subject, dark):
    h = subject_hue(subject)
    t = _Theme(*((h[3], h[4]) if dark else (h[0], h[1])))
    surface = SURFACE_DARK if dark else SURFACE_LIGHT
    e = PAL_DARK if dark else PAL_LIGHT
    env = dict(t=t, surface=surface, lerp=lerp, WHITE=WHITE)
    return Palette(*[eval(e[k], env) for k in ("top", "bottom", "ink", "paper", "field")])

# ------------------------------------------------------------------ rng -----
M32 = 0xFFFFFFFF

def stable_seed(key):
    h = 0x811C9DC5
    for ch in key:
        h = (h ^ ord(ch)) & M32
        h = (h * 16777619) & M32
    return h

class Rng:
    def __init__(self, seed):
        self.s = seed & M32 or 1
    def next(self):
        s = self.s
        s ^= (s << 13) & M32
        s ^= s >> 17
        s ^= (s << 5) & M32
        self.s = s
        return ((s >> 8) & 0xFFFFFF) / 16777216.0
    def range(self, a, b):
        return a + (b - a) * self.next()
    def int(self, n):
        v = int(self.next() * n)
        return n - 1 if v >= n else v

# --------------------------------------------------------------- geometry ---
class Offset:
    __slots__ = ("x", "y")
    def __init__(self, x, y): self.x, self.y = x, y

class Size:
    __slots__ = ("w", "h")
    def __init__(self, w, h): self.w, self.h = w, h

class Stroke:
    def __init__(self, width, cap=None): self.width, self.cap = width, cap

class Path:
    def __init__(self): self.ops = []
    def moveTo(self, x, y): self.ops.append(("M", x, y))
    def lineTo(self, x, y): self.ops.append(("L", x, y))
    def cubicTo(self, a, b, c, d, e, f): self.ops.append(("C", a, b, c, d, e, f))
    def close(self): self.ops.append(("Z",))
    def subpaths(self):
        subs, cur, start = [], [], None
        for op in self.ops:
            if op[0] == "M":
                if len(cur) > 1: subs.append([cur, False])
                cur = [(op[1], op[2])]; start = (op[1], op[2])
            elif op[0] == "L":
                cur.append((op[1], op[2]))
            elif op[0] == "C":
                x0, y0 = cur[-1]
                for i in range(1, 17):
                    t = i / 16.0; u = 1 - t
                    cur.append((u*u*u*x0 + 3*u*u*t*op[1] + 3*u*t*t*op[3] + t*t*t*op[5],
                                u*u*u*y0 + 3*u*u*t*op[2] + 3*u*t*t*op[4] + t*t*t*op[6]))
            elif op[0] == "Z":
                if len(cur) > 1: subs.append([cur, True])
                cur = [start] if start else []
        if len(cur) > 1: subs.append([cur, False])
        return subs

class Mat:
    __slots__ = ("a", "b", "c", "d", "e", "f")
    def __init__(self, a=1, b=0, c=0, d=1, e=0, f=0):
        self.a, self.b, self.c, self.d, self.e, self.f = a, b, c, d, e, f
    def apply(self, x, y):
        return (self.a * x + self.c * y + self.e, self.b * x + self.d * y + self.f)
    def mul(self, o):
        return Mat(self.a*o.a + self.c*o.b, self.b*o.a + self.d*o.b,
                   self.a*o.c + self.c*o.d, self.b*o.c + self.d*o.d,
                   self.a*o.e + self.c*o.f + self.e, self.b*o.e + self.d*o.f + self.f)

class _Ctx:
    def __init__(self, d, m): self.d, self.m = d, m
    def __enter__(self): self.d.stack.append(self.d.m); self.d.m = self.d.m.mul(self.m)
    def __exit__(self, *a): self.d.m = self.d.stack.pop()

class DrawScope:
    def __init__(self, w, h):
        self.w, self.h = float(w), float(h)
        # RGB, not RGBA: PIL only alpha-blends a drawing into an RGB image.
        # On an RGBA target it overwrites, which silently turned every 20%%
        # wash in these drawings into a solid slab.
        self.img = Image.new("RGB", (int(w * SS), int(h * SS)), (255, 255, 255))
        self.g = ImageDraw.Draw(self.img, "RGBA")
        self.m = Mat(); self.stack = []

    def rotate(self, degrees, pivot):
        a = math.radians(degrees); co, si = math.cos(a), math.sin(a)
        r = Mat(co, si, -si, co, pivot.x - co*pivot.x + si*pivot.y,
                pivot.y - si*pivot.x - co*pivot.y)
        return _Ctx(self, r)

    def _p(self, x, y):
        x, y = self.m.apply(x, y)
        return (x * SS, y * SS)

    def _poly(self, pts, color):
        if len(pts) < 3: return
        self.g.polygon([self._p(x, y) for x, y in pts], fill=color.rgba())

    def _stroke(self, pts, color, width, closed=False, cap=None):
        """One stroke is one shape. Drawing the polyline and then a disc at
        every join straight onto the canvas double-composites the overlaps, so
        a 30%-alpha curve came out beaded. Translucent strokes are rasterised
        into a mask first and composited once, which is what Compose does."""
        if len(pts) < 2:
            return
        dev = [self._p(x, y) for x, y in pts]
        if closed:
            dev = dev + [dev[0]]
        wpx = max(1, int(round(width * SS)))
        rr = wpx / 2.0
        nodes = dev if (closed or cap == "round") else dev[1:-1]
        rgba = color.rgba()
        if color.a >= 0.999:
            self.g.line(dev, fill=rgba, width=wpx, joint="curve")
            for (X, Y) in nodes:
                self.g.ellipse([X - rr, Y - rr, X + rr, Y + rr], fill=rgba)
            return
        W, H = self.img.size
        pad = rr + 2
        x0 = max(0, int(min(x for x, _ in dev) - pad))
        y0 = max(0, int(min(y for _, y in dev) - pad))
        x1 = min(W, int(max(x for x, _ in dev) + pad) + 1)
        y1 = min(H, int(max(y for _, y in dev) + pad) + 1)
        if x1 <= x0 or y1 <= y0:
            return
        mask = Image.new("L", (x1 - x0, y1 - y0), 0)
        mg = ImageDraw.Draw(mask)
        loc = [(x - x0, y - y0) for x, y in dev]
        mg.line(loc, fill=255, width=wpx, joint="curve")
        for (X, Y) in [(x - x0, y - y0) for x, y in nodes]:
            mg.ellipse([X - rr, Y - rr, X + rr, Y + rr], fill=255)
        av = int(color.a * 255 + 0.5)
        if av != 255:
            mask = mask.point(lambda v, a=av: (v * a) // 255)
        self.img.paste(Image.new("RGB", mask.size, rgba[:3]), (x0, y0), mask)

    # --- Compose-shaped primitives ---
    def drawRect(self, color=None, topLeft=None, size=None, style=None, brush=None):
        if brush is not None:
            brush.paint(self); return
        if topLeft is None: topLeft = Offset(0, 0)
        if size is None: size = Size(self.w, self.h)
        pts = [(topLeft.x, topLeft.y), (topLeft.x + size.w, topLeft.y),
               (topLeft.x + size.w, topLeft.y + size.h), (topLeft.x, topLeft.y + size.h)]
        if style is None: self._poly(pts, color)
        else: self._stroke(pts, color, style.width, closed=True, cap=style.cap)

    def drawCircle(self, color=None, radius=None, center=None, style=None):
        cx, cy = self._p(center.x, center.y)
        rr = radius * SS
        if style is None:
            self.g.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill=color.rgba())
        else:
            wpx = max(1, int(round(style.width * SS)))
            self.g.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], outline=color.rgba(), width=wpx)

    def drawLine(self, color=None, start=None, end=None, strokeWidth=1.0, cap=None):
        self._stroke([(start.x, start.y), (end.x, end.y)], color, strokeWidth, cap=cap)

    def drawPath(self, path=None, color=None, style=None):
        for pts, closed in path.subpaths():
            if style is None: self._poly(pts, color)
            else: self._stroke(pts, color, style.width, closed=closed, cap=style.cap)

    def drawArc(self, color=None, startAngle=0.0, sweepAngle=0.0, useCenter=False,
                topLeft=None, size=None, style=None):
        rx, ry = size.w / 2.0, size.h / 2.0
        cx, cy = topLeft.x + rx, topLeft.y + ry
        n = max(12, int(abs(sweepAngle) / 4))
        pts = []
        for i in range(n + 1):
            a = math.radians(startAngle + sweepAngle * i / n)
            pts.append((cx + math.cos(a) * rx, cy + math.sin(a) * ry))
        closed = abs(sweepAngle) >= 359.9
        if style is None:
            if useCenter: pts = [(cx, cy)] + pts
            self._poly(pts, color)
        else:
            self._stroke(pts, color, style.width, closed=closed, cap=style.cap)

def ramp(colors, t):
    if t <= 0.0: return colors[0]
    if t >= 1.0: return colors[-1]
    n = len(colors) - 1
    f = t * n
    i = int(f)
    if i >= n: i = n - 1
    return lerp(colors[i], colors[i + 1], f - i)

class _Grad:
    """Gradients are evaluated at 1x and upscaled. They are smooth by
    definition, so the supersample buys nothing and costs 16x the pixels."""
    def __init__(self, colors): self.colors = colors
    def t(self, x, y): return 0.0
    def paint(self, d):
        W, H = d.img.size
        lw, lh = max(1, W // SS), max(1, H // SS)
        px, pa = [], []
        for yy in range(lh):
            y = yy + 0.5
            for xx in range(lw):
                c = ramp(self.colors, self.t(xx + 0.5, y))
                px.append((int(c.r * 255 + .5), int(c.g * 255 + .5), int(c.b * 255 + .5)))
                pa.append(int(c.a * 255 + .5))
        rgb = Image.new("RGB", (lw, lh)); rgb.putdata(px)
        al = Image.new("L", (lw, lh)); al.putdata(pa)
        d.img.paste(rgb.resize((W, H), Image.BILINEAR),
                    (0, 0), al.resize((W, H), Image.BILINEAR))

class VerticalGradient(_Grad):
    def __init__(self, colors, startY=0.0, endY=None):
        _Grad.__init__(self, colors); self.y0, self.y1 = startY, endY
    def paint(self, d):
        self._h = d.h; _Grad.paint(self, d)
    def t(self, x, y):
        y1 = self._h if self.y1 is None or self.y1 == float("inf") else self.y1
        return (y - self.y0) / max(1e-6, y1 - self.y0)

class LinearGradient(_Grad):
    def __init__(self, colors, start, end):
        _Grad.__init__(self, colors); self.s, self.e = start, end
    def t(self, x, y):
        dx, dy = self.e.x - self.s.x, self.e.y - self.s.y
        return ((x - self.s.x) * dx + (y - self.s.y) * dy) / max(1e-6, dx * dx + dy * dy)

class RadialGradient(_Grad):
    def __init__(self, colors, center, radius):
        _Grad.__init__(self, colors); self.c, self.rad = center, radius
    def t(self, x, y):
        return math.hypot(x - self.c.x, y - self.c.y) / max(1e-6, self.rad)

class Brush:
    @staticmethod
    def verticalGradient(colors, startY=0.0, endY=None): return VerticalGradient(colors, startY, endY)
    @staticmethod
    def linearGradient(colors, start=None, end=None): return LinearGradient(colors, start, end)
    @staticmethod
    def radialGradient(colors, center=None, radius=None): return RadialGradient(colors, center, radius)

# --------------------------------------------------------------- transpile ---
DRAW_FNS = ("drawRect", "drawCircle", "drawLine", "drawPath", "drawArc")

def _inline_ifs(s):
    """`if (C) A else B` -> `((A) if (C) else (B))`, where B runs to the comma
    or closing bracket that ends the argument it sits in."""
    pos = 0
    pat = re.compile(r"(?<![\w.])if \(")
    while True:
        m = pat.search(s, pos)
        if not m:
            return s
        st = m.start()
        j = s.index("(", st)
        depth = 0
        for k in range(j, len(s)):
            if s[k] == "(":
                depth += 1
            elif s[k] == ")":
                depth -= 1
                if depth == 0:
                    break
        cond = s[j + 1:k]
        rest = s[k + 1:]
        d, epos = 0, -1
        for i in range(len(rest)):
            if d == 0 and rest.startswith(" else ", i):
                epos = i
                break
            c = rest[i]
            if c in "([":
                d += 1
            elif c in ")]":
                if d == 0:
                    break
                d -= 1
            elif c == "," and d == 0:
                break
        if epos < 0:
            raise SyntaxError("no else for: " + s[st:st + 70])
        a, tail = rest[:epos], rest[epos + 6:]
        d, end = 0, len(tail)
        for i in range(len(tail)):
            c = tail[i]
            if c in "([":
                d += 1
            elif c in ")]":
                if d == 0:
                    end = i
                    break
                d -= 1
            elif c == "," and d == 0:
                end = i
                break
        b = tail[:end]
        repl = "((%s) if (%s) else (%s))" % (a.strip(), cond, b.strip())
        s = s[:st] + repl + tail[end:]
        pos = st + len(repl)

POSTFIX = {
    "toInt": lambda rv, a: "int(%s)" % rv,
    "coerceIn": lambda rv, a: "min(max(%s, %s), %s)" % (rv, a[0], a[1]),
    "coerceAtLeast": lambda rv, a: "max(%s, %s)" % (rv, a[0]),
    "coerceAtMost": lambda rv, a: "min(%s, %s)" % (rv, a[0]),
}

def _split_args(s):
    out, d, cur = [], 0, ""
    for c in s:
        if c in "([":
            d += 1
        elif c in ")]":
            d -= 1
        if c == "," and d == 0:
            out.append(cur.strip()); cur = ""
        else:
            cur += c
    if cur.strip():
        out.append(cur.strip())
    return out

def _postfix(s):
    """Rewrite Kotlin postfix calls (x.toInt(), y.coerceIn(a, b)) into the
    prefix Python equivalents, finding the receiver by walking left and
    balancing brackets so nested expressions survive."""
    pat = re.compile(r"\.(" + "|".join(POSTFIX) + r")\(")
    while True:
        m = pat.search(s)
        if not m:
            return s
        # receiver: walk left from the dot
        i = m.start() - 1
        d = 0
        while i >= 0:
            c = s[i]
            if c in ")]":
                d += 1
            elif c in "([":
                if d == 0:
                    break
                d -= 1
            elif d == 0 and not (c.isalnum() or c in "._"):
                break
            i -= 1
        recv = s[i + 1:m.start()]
        # call args: balance from the open paren
        j = m.end() - 1
        d = 0
        for k in range(j, len(s)):
            if s[k] == "(":
                d += 1
            elif s[k] == ")":
                d -= 1
                if d == 0:
                    break
        args = _split_args(s[j + 1:k])
        s = s[:i + 1] + POSTFIX[m.group(1)](recv, args) + s[k + 1:]

def expr(s):
    s = s.replace("size.width", "d.w").replace("size.height", "d.h")
    s = s.replace("PI.toFloat()", "math.pi").replace(".toFloat()", "")
    s = re.sub(r"(\d)f\b", r"\1", s)
    s = re.sub(r"\bfalse\b", "False", s)
    s = re.sub(r"\btrue\b", "True", s)
    s = s.replace("StrokeCap.Round", "'round'").replace("StrokeCap.Butt", "None")
    s = re.sub(r"\bsin\(", "math.sin(", s)
    s = re.sub(r"\bcos\(", "math.cos(", s)
    s = re.sub(r"\bsqrt\(", "math.sqrt(", s)
    s = _postfix(s)
    s = s.replace("&&", " and ").replace("||", " or ")
    if " else " in s and re.search(r"(?<![\w.])if \(", s):
        s = _inline_ifs(s)
    for fn in DRAW_FNS:
        s = re.sub(r"(?<![\w.])" + fn + r"\(", "d." + fn + "(", s)
    return s

def transpile(src):
    out = {}
    for m in re.finditer(r"(?:private )?fun DrawScope\.(\w+)\(p: (?:BannerPalette|CoverPalette), r: Rng\) \{", src):
        name = m.group(1)
        i = m.end() - 1
        depth = 0
        for k in range(i, len(src)):
            if src[k] == "{": depth += 1
            elif src[k] == "}":
                depth -= 1
                if depth == 0: break
        body = src[i+1:k]
        lines = []
        for raw in body.split("\n"):
            t = raw.split("//")[0].rstrip()
            if t.strip(): lines.append(t.strip())
        # merge continuations by paren depth
        merged, buf = [], ""
        for t in lines:
            buf = (buf + " " + t).strip()
            if buf.count("(") == buf.count(")"):
                merged.append(buf)
                buf = ""
        py, ind = [], 1
        def emit(s): py.append("    " * ind + s)
        for t in merged:
            if t == "}":
                ind -= 1; continue
            if t.startswith("} else if"):
                ind -= 1
                emit("elif " + expr(t[t.index("(")+1:t.rindex(")")]) + ":"); ind += 1; continue
            if t.startswith("} else"):
                ind -= 1; emit("else:"); ind += 1; continue
            fm = re.match(r"for \((\w+) in (.+?) until (.+?)\) \{$", t)
            if fm:
                emit("for %s in range(int(%s), int(%s)):" % (fm.group(1), expr(fm.group(2)), expr(fm.group(3))))
                ind += 1; continue
            im = re.match(r"if \((.+)\) \{$", t)
            if im:
                emit("if " + expr(im.group(1)) + ":"); ind += 1; continue
            bm = re.match(r"(rotate|translate|scale)\((.*)\) \{$", t)
            if bm:
                emit("with d.%s(%s):" % (bm.group(1), expr(bm.group(2)))); ind += 1; continue
            if t.endswith("{"):
                raise SyntaxError("unhandled block: " + t)
            t = re.sub(r"^(val|var) ", "", t)
            if re.match(r"(d|p|r|math|Path|Offset|Size|Stroke)\s*=[^=]", t):
                raise SyntaxError("local shadows a renderer name: " + t)
            emit(expr(t))
        out[name] = "def %s(d, p, r):\n%s\n    pass\n" % (name, "\n".join(py))
    return out

SRC = open(KT).read()
FNS = transpile(SRC)
def _family_dispatch(src):
    body = src[src.index("fun DrawScope.drawBannerArt("):]
    body = body[:body.index("\n}\n")]
    out = {}
    for m in re.finditer(r"SubjectFamily\.(\w+) -> when \(i\) \{([\s\S]*?)\n        \}", body):
        out[m.group(1)] = re.findall(r"->\s*(art\w+)\(p, r\)", m.group(2))
    return out

def _family_counts(src):
    body = src[src.index("fun bannerArtCount("):]
    body = body[:body.index("\n}")]
    return {m.group(1): int(m.group(2))
            for m in re.finditer(r"SubjectFamily\.(\w+) -> (\d+)", body)}

FAMILY = _family_dispatch(SRC)
COUNTS = _family_counts(SRC)
ORDER = [n for f in FAMILY for n in FAMILY[f]]
GLOBALS = dict(math=math, Offset=Offset, Size=Size, Stroke=Stroke, Path=Path,
               Brush=Brush, Color=Color, lerp=lerp, listOf=lambda *a: list(a), abs=abs, range=range, int=int, len=len, min=min, max=max)
for name, code in FNS.items():
    exec(compile(code, "<art:%s>" % name, "exec"), GLOBALS)

def _draw(name, subject, dark, w, h, rng):
    p = banner_palette(subject, dark)
    d = DrawScope(w, h)
    Brush.verticalGradient([p.top, p.bottom]).paint(d)
    GLOBALS[name](d, p, rng)
    return d.img.resize((w, h), Image.LANCZOS)

def render_family(family, index, subject, dark, w=300, h=110, seed=None):
    """One slot of one family's set, the way drawBannerArt dispatches it."""
    names = FAMILY[family]
    assert COUNTS[family] == len(names), (family, COUNTS[family], len(names))
    key = seed if seed is not None else subject + "#" + family + "#" + str(index)
    return _draw(names[index % len(names)], subject, dark, w, h, Rng(stable_seed(key)))

def render(index, subject, dark, w=300, h=110):
    fam = subject_family(subject)
    return render_family(fam, index, subject, dark, w, h)

def render_seed(seed, subject, dark, w=300, h=110):
    """The real path: subject picks the family, the hash picks within it."""
    fam = subject_family(subject)
    hsh = stable_seed(seed)
    names = FAMILY[fam]
    return _draw(names[((hsh >> 3) & 0x7FFFFFFF) % len(names)], subject, dark, w, h, Rng(hsh))

if __name__ == "__main__":
    print(len(FNS), "arts defined;", len(set(ORDER)), "dispatched")
    for f in FAMILY:
        print("  %-10s %2d  %s" % (f, COUNTS[f], " ".join(n[3:] for n in FAMILY[f])))
