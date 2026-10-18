"""Animate the real Neby smoothly.

A performance is a list of expression keys (time, expression id, blend seconds, ease). Each
key fades in over the composite of everything before it (layered crossfade), so Neby always
moves from where it actually is. Blinks are cosine dips, look-at is a smooth curve, and
squash/stretch/hops are applied in the compositor. Geometry comes from the product's own
engine via neby_rig.mjs."""
import json
import math
import os
import subprocess

import skia

HERE = os.path.dirname(os.path.abspath(__file__))
RIG = os.path.join(HERE, "neby_rig.mjs")
REPO_JS = os.path.join(HERE, "..", "..", "..", "backend_python", "web", "static", "web", "js", "neby-avatar.js")


def smoother(k):
    k = max(0.0, min(1.0, k))
    return k * k * k * (k * (6 * k - 15) + 10)


def soft_spring(k):
    """Ease with a small, well-damped overshoot (about 6%)."""
    if k <= 0:
        return 0.0
    if k >= 1:
        return 1.0
    return 1 - math.exp(-7.5 * k) * math.cos(5.2 * k) * (1 - k) - 0.0 * k


EASES = {"smooth": smoother, "spring": soft_spring}


class Performance:
    def __init__(self, keys, blinks=(), looks=(), body_colors=(), props=None):
        """keys: [(t, expression_id, blend_s, ease)], blinks: [t], looks: [(t, x, y, blend_s)]."""
        self.keys = sorted(keys)
        self.blinks = sorted(blinks)
        self.looks = sorted(looks)
        self.props = props

    def weights(self, t):
        ws = []
        for i, (t0, eid, dur, ease) in enumerate(self.keys):
            if t0 > t and i > 0:
                break
            k = 1.0 if i == 0 else EASES[ease]((t - t0) / max(dur, 1e-3))
            ws = [(e, w * (1 - k)) for e, w in ws] + [(eid, k)]
        merged = {}
        for e, w in ws:
            merged[e] = merged.get(e, 0.0) + w
        return [[e, w] for e, w in merged.items() if abs(w) > 1e-4] or [[self.keys[0][1], 1.0]]

    def blink(self, t):
        b = 1.0
        for tb in self.blinks:
            u = (t - tb) / 0.17
            if 0 <= u <= 1:
                b = min(b, 0.5 + 0.5 * math.cos(2 * math.pi * u))
        return b

    def look(self, t):
        x = y = 0.0
        for t0, lx, ly, d in self.looks:
            k = smoother((t - t0) / max(d, 1e-3))
            x += (lx - x) * k
            y += (ly - y) * k
        return [x, y]


class NebyRig:
    def __init__(self, js=None):
        js = js or os.environ.get("NEBY_AVATAR_JS") or REPO_JS
        self.p = subprocess.Popen(["node", RIG, js], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
        self.cache = {}

    def svg(self, perf, t):
        key = (id(perf), round(t, 4))
        if key in self.cache:
            return self.cache[key]
        req = {"keys": perf.weights(t), "t": t * 1000.0, "blink": perf.blink(t), "look": perf.look(t)}
        if perf.props:
            req.update(perf.props(t))
        self.p.stdin.write(json.dumps(req) + "\n")
        out = self.p.stdout.readline().strip()
        if out.startswith("ERR"):
            raise RuntimeError(out)
        if len(self.cache) > 64:
            self.cache.clear()
        self.cache[key] = out
        return out

    def draw(self, c, perf, t, cx, cy, size, alpha=1.0, rot=0.0, sx=1.0, sy=1.0, shadow=True, ground=None):
        """Neby centred at (cx, cy), `size` px wide. sx/sy squash about the bottom of the head."""
        if alpha <= 0 or size <= 1:
            return
        dom = skia.SVGDOM.MakeFromStream(skia.MemoryStream(self.svg(perf, round(t * 120) / 120).encode(), True))
        dom.setContainerSize(skia.Size(300, 300))
        s = size / 300.0
        bottom = cy + size * 0.40
        if shadow:
            gy = ground if ground is not None else bottom
            lift = max(0.0, gy - bottom)
            k = max(0.3, 1 - lift / (size * 1.6))
            p = skia.Paint(AntiAlias=True, Color=skia.ColorSetARGB(int(46 * alpha * k), 2, 27, 84))
            p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, size * 0.045))
            c.drawOval(skia.Rect.MakeXYWH(cx - size * 0.33 * k * sx, gy - size * 0.03, size * 0.66 * k * sx, size * 0.08), p)
        c.save()
        c.translate(cx, bottom)
        c.rotate(rot)
        c.scale(sx, sy)
        c.translate(0, -size * 0.40)
        c.scale(s, s)
        c.translate(-150, -150)
        if alpha < 1:
            c.saveLayerAlpha(None, int(255 * alpha))
        dom.render(c)
        if alpha < 1:
            c.restore()
        c.restore()
