import os
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
"""The same call streams, from the Python transpile of the same Kotlin."""
import sys, json, re, math
sys.path.insert(0, _HERE)
import render as R
import genjs as G

def n(v):
    return round(float(v), 6)

def col(c):
    return [n(c.r), n(c.g), n(c.b), n(c.a)]

class Rec:
    def __init__(self, w, h):
        self.w, self.h = float(w), float(h)
        self.log = []
    def _st(self, s):
        return [n(s.width), s.cap] if s else None
    def drawRect(self, color=None, topLeft=None, size=None, style=None, brush=None):
        if brush is not None:
            kind = {"VerticalGradient": "v", "LinearGradient": "l",
                    "RadialGradient": "r"}[type(brush).__name__]
            self.log.append(["rect", ["brush", kind, [col(c) for c in brush.colors]],
                             None, None, None])
            return
        self.log.append(["rect", col(color),
                         [n(topLeft.x), n(topLeft.y)] if topLeft else None,
                         [n(size.w), n(size.h)] if size else None, self._st(style)])
    def drawCircle(self, color=None, radius=None, center=None, style=None):
        self.log.append(["circle", col(color), n(radius), n(center.x), n(center.y),
                         self._st(style)])
    def drawLine(self, color=None, start=None, end=None, strokeWidth=1.0, cap=None):
        self.log.append(["line", col(color), n(start.x), n(start.y), n(end.x), n(end.y),
                         n(strokeWidth), cap])
    def drawPath(self, path=None, color=None, style=None):
        self.log.append(["path", col(color),
                         [[o[0]] + [n(v) for v in o[1:]] for o in path.ops],
                         self._st(style)])
    def drawArc(self, color=None, startAngle=0.0, sweepAngle=0.0, useCenter=False,
                topLeft=None, size=None, style=None):
        self.log.append(["arc", col(color), n(startAngle), n(sweepAngle), bool(useCenter),
                         n(topLeft.x), n(topLeft.y), n(size.w), n(size.h), self._st(style)])
    def rotate(self, degrees, pivot):
        log = self.log
        log.append(["rotate>", n(degrees), n(pivot.x), n(pivot.y)])
        class C:
            def __enter__(s): pass
            def __exit__(s, *a): log.append(["<rotate"])
        return C()
    def translate(self, x, y):
        log = self.log
        log.append(["translate>", n(x), n(y)])
        class C:
            def __enter__(s): pass
            def __exit__(s, *a): log.append(["<translate"])
        return C()

out = {}
W, H = 320, 120
for fam, names in R.FAMILY.items():
    for i, name in enumerate(names):
        key = "%s#%d#%s" % (fam, i, name)
        p = R.banner_palette("Physics", False)
        d = Rec(W, H)
        R.GLOBALS[name](d, p, R.Rng(R.stable_seed(key)))
        out[key] = d.log

# covers: transpile the cover Kotlin through the same Python backend
COVER_FNS = R.transpile(open(G.J.COVER_KT).read())
CG = dict(R.GLOBALS)
for nm, code in COVER_FNS.items():
    exec(compile(code, "<cover:%s>" % nm, "exec"), CG)

class CP:
    def __init__(self, **kw): self.__dict__.update(kw)

cp, cfb = G.cover_dispatch()
MOTIF = dict(cp)
for role, fields in G.cover_palettes():
    p = CP(**{k: R.Color.hex(int(v, 16)) for k, v in fields.items()})
    for stage in ("ground", "motif", "finish"):
        fn = {"ground": "drawCoverGround", "finish": "drawCoverFinish"}.get(
            stage, MOTIF.get(role, cfb))
        d = Rec(640, 260)
        CG[fn](d, p, R.Rng(R.stable_seed("cover|nikit|" + role)))
        out["COVER#%s#%s" % (role, stage)] = d.log

probes = ["Physics", "Health and Physical Education", "Computer Science",
          "सामाजिक अध्ययन", "Compulsory English", "Moral Education", "", "Model Set 2081"]
contract = []
for s in probes:
    h = R.stable_seed(s + "|pdf")
    fam = R.subject_family(s)
    idx = ((h >> 3) & 0x7FFFFFFF) % len(R.FAMILY[fam])
    signed = h - 0x100000000 if h >= 0x80000000 else h
    contract.append([s, fam, signed, idx, R.FAMILY[fam][idx]])
out["__contract"] = contract
json.dump(out, open(os.path.join(_HERE, "py.json"), "w"), ensure_ascii=False)
print("recorded", len(out), "streams")
