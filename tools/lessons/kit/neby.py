"""The real pixel Neby, played frame-accurately from the same sprite strips the site and the app use."""
import os

import numpy as np
from manim import ImageMobject
from manim.constants import RESAMPLING_ALGORITHMS
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
STRIPS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "backend_python", "web", "static", "web", "img", "neby"))

META = {
    "idle": (16, 115), "still": (1, 1000), "blink": (6, 110), "look-around": (12, 130), "think": (8, 160),
    "talk": (8, 95), "listen": (8, 140), "read": (14, 140), "sleep": (12, 140), "wave": (10, 110),
    "hop": (12, 72), "wink": (10, 110), "love": (12, 110), "kiss": (12, 110), "laugh": (10, 80),
    "cool": (10, 120), "surprised": (10, 80), "sad": (12, 130), "dizzy": (12, 100), "oops": (10, 100),
    "success": (12, 80), "celebrate": (14, 85), "tika": (18, 120), "kite": (16, 130), "swing": (16, 90),
    "diyo": (12, 110), "deusi": (12, 95), "splash": (16, 90), "fireworks": (16, 100), "namaste": (12, 120),
}

LATIN_STATES = {"wave"}

_cache = {}


def frames(look, state):
    key = (look, state)
    if key not in _cache:
        path = os.path.join(STRIPS, look, state + ".png")
        if not os.path.exists(path):
            path = os.path.join(STRIPS, "classic", state + ".png")
        im = Image.open(path).convert("RGBA")
        n = im.size[0] // 48
        fs = []
        for i in range(n):
            f = im.crop((i * 48, 0, i * 48 + 48, 48)).resize((240, 240), Image.NEAREST)
            fs.append(np.array(f))
        _cache[key] = fs
    return _cache[key]


class Neby(ImageMobject):
    def __init__(self, state="idle", look="classic", height=2.2, **kw):
        self.look = look
        self._fs = frames(look, state)
        super().__init__(self._fs[0], **kw)
        self.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        self.height = height
        self.state = state
        self.clock = 0.0
        self.queue = []
        self.add_updater(Neby._tick)

    def set_state(self, state, once=False, then="idle"):
        self.state = state
        self._fs = frames(self.look, state)
        self.clock = 0.0
        self.queue = [then] if once else []
        return self

    def _tick(self, dt):
        self.clock += dt
        n, ms = META.get(self.state, (len(self._fs), 120))
        n = len(self._fs)
        idx = int(self.clock * 1000 / ms)
        if self.queue and idx >= n:
            nxt = self.queue.pop(0)
            self.set_state(nxt)
            idx = 0
        self.pixel_array = self._fs[idx % n]
