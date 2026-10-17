"""Draw the real Neby (the product's neby-avatar.js) into the film.

`neby_capture.mjs` runs the avatar engine under a virtual clock and records the SVG it
draws for every frame; this module turns those SVG frames into Skia drawings."""
import json
import os
import subprocess

import skia

HERE = os.path.dirname(os.path.abspath(__file__))
CAPTURE = os.path.join(HERE, "..", "neby", "neby_capture.mjs")
REPO_JS = os.path.join(HERE, "..", "..", "..", "backend_python", "web", "static", "web", "js", "neby-avatar.js")

# What Neby does, and when (seconds). Fed to the real engine's react()/setLookAt().
SCRIPT = [
    ("excited", 3.0), ("look|-0.6|0.2", 3.2),
    ("scanning", 7.2), ("look|0.7|-0.2", 7.2),
    ("laughing", 10.6), ("look|0|0", 10.6),
    ("speaking", 13.6), ("look|-0.5|-0.3", 13.6),
    ("celebrate", 16.1), ("look|0|0", 16.1),
    ("wink", 18.3),
]


class Neby:
    def __init__(self, duration, fps=60, js=None, cache=None):
        js = js or os.environ.get("NEBY_AVATAR_JS") or REPO_JS
        cache = cache or os.path.join("/tmp", f"neby-frames-{fps}.json")
        if not os.path.exists(cache):
            plan = ",".join(f"{k}@{t}" for k, t in SCRIPT)
            subprocess.run(["node", CAPTURE, js, cache, str(fps), f"film=intro-neby:{duration + 0.5}:{plan}"],
                           check=True)
        data = json.load(open(cache))
        self.fps = data["fps"]
        self.frames = data["clips"]["film"]
        self._dom = {}

    def dom(self, t):
        i = max(0, min(len(self.frames) - 1, int(round(t * self.fps))))
        if i not in self._dom:
            if len(self._dom) > 240:
                self._dom.clear()
            d = skia.SVGDOM.MakeFromStream(skia.MemoryStream(self.frames[i].encode(), True))
            d.setContainerSize(skia.Size(300, 300))
            self._dom[i] = d
        return self._dom[i]

    def draw(self, c, t, cx, cy, size, alpha=1.0, rot=0.0, shadow=True):
        """Neby centred at (cx, cy), `size` px across the 300-unit avatar box."""
        if alpha <= 0 or size <= 1:
            return
        s = size / 300.0
        if shadow:
            p = skia.Paint(AntiAlias=True, Color=skia.ColorSetARGB(int(40 * alpha), 2, 27, 84))
            p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, size * 0.04))
            c.drawOval(skia.Rect.MakeXYWH(cx - size * 0.32, cy + size * 0.40, size * 0.64, size * 0.07), p)
        c.save()
        c.translate(cx, cy)
        c.rotate(rot)
        c.scale(s, s)
        c.translate(-150, -150)
        if alpha < 1:
            c.saveLayerAlpha(None, int(255 * alpha))
        self.dom(t).render(c)
        if alpha < 1:
            c.restore()
        c.restore()
