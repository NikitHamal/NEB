"""Port of blobatar/src/expression.ts — the 14 poses and their bake/tint machinery (v2).

A pose is data plus the two ways to apply it: `bake` for the static path (eye
channels baked into geometry, body channels as a rigid translate wrap) and an
optional `tint` for the colour-shifting poses (mad/love/shy/sick).
"""

import math

from .color import BLUSH, BILE, HOT, ROSE, mix_hex, tinted


IDENT = {
    "esx": 1, "esy": 1, "tilt": 0, "edy": 0, "edx": 0,
    "esx2": 0, "esy2": 0, "tilt2": 0, "edy2": 0,
    "lock": 0, "heat": 0, "shake": 0, "rock": 0, "bdy": 0,
}


def _r3(v):
    s = math.floor(v * 1000 + 0.5) / 1000
    if s == 0:
        return "0"
    if s.is_integer():
        return str(int(s))
    return str(s)


def bake_pose(l, p):
    """Static path: eye channels baked into geometry, body offset as a transform."""
    eyes = []
    for i, e in enumerate(l["eyes"]):
        eyes.append({
            "n": e["n"],
            "cx": e["cx"] + p["edx"] * (1 if i else -1),
            "cy": e["cy"] + p["edy"] + (p["edy2"] if i else 0),
            "rx": e["rx"] * (p["esx"] + (p["esx2"] if i else 0)),
            "ry": e["ry"] * (p["esy"] + (p["esy2"] if i else 0)),
            "rot": e["rot"] * (1 - p["lock"])
                   + (p["tilt"] + (p["tilt2"] if i else 0)) * (1 if i else -1),
        })
    new_l = dict(l)
    new_l["eyes"] = eyes
    wrap = "translate(0 %s)" % _r3(p["bdy"]) if p["bdy"] != 0 else ""
    return new_l, wrap


def tint_with(pal, p, t):
    head, eye = tinted(pal["head"], pal["eye"], t)
    return {
        "head": mix_hex(pal["head"], head, p["heat"]),
        "eye": mix_hex(pal["eye"], eye, p["heat"]),
    }


def _mk(p, tint=None):
    e = {"p": p, "bake": bake_pose}
    if tint is not None:
        e["tint"] = tint
    return e


IDLE = _mk(IDENT)

HAPPY = _mk({
    "esx": 1.72, "esy": 0.3, "tilt": 8, "edy": -1.5, "edx": 1.5,
    "esx2": 0.08, "esy2": 0.05, "tilt2": -16, "edy2": 0,
    "lock": 1, "heat": 0, "shake": 0, "rock": 0, "bdy": -2.2,
})

SAD = _mk({
    "esx": 0.6, "esy": 0.56, "tilt": 26, "edy": 3.6, "edx": 1.9,
    "esx2": -0.05, "esy2": -0.07, "tilt2": -7, "edy2": 0,
    "lock": 1, "heat": 0, "shake": 0, "rock": 0, "bdy": 2.6,
})

MAD = _mk({
    "esx": 1.85, "esy": 0.26, "tilt": -33, "edy": 0.4, "edx": 0.6,
    "esx2": 0, "esy2": -0.03, "tilt2": 5, "edy2": 0,
    "lock": 1, "heat": 0.62, "shake": 0.55, "rock": 0, "bdy": 0.8,
}, tint=lambda pal, p: tint_with(pal, p, HOT))

SURPRISED = _mk({
    "esx": 1.34, "esy": 1.2, "tilt": -6, "edy": -1.05, "edx": 0.5,
    "esx2": 0.05, "esy2": 0.07, "tilt2": 3, "edy2": 0,
    "lock": 1, "heat": 0, "shake": 0, "rock": 0, "bdy": -1.4,
})

WINK = _mk({
    "esx": 1.32, "esy": 0.76, "tilt": 5, "edy": -0.6, "edx": 0.8,
    "esx2": 0.26, "esy2": -0.56, "tilt2": -11, "edy2": 0,
    "lock": 1, "heat": 0, "shake": 0, "rock": 0, "bdy": -1.1,
})

SLEEPY = _mk({
    "esx": 1.14, "esy": 0.22, "tilt": 0, "edy": 2.4, "edx": 0.3,
    "esx2": -0.04, "esy2": 0.03, "tilt2": 4, "edy2": 0,
    "lock": 1, "heat": 0, "shake": 0, "rock": 0, "bdy": 1.2,
})

SMUG = _mk({
    "esx": 1.3, "esy": 0.42, "tilt": 18, "edy": -0.5, "edx": 0.5,
    "esx2": 0.06, "esy2": -0.06, "tilt2": -36, "edy2": 0,
    "lock": 1, "heat": 0, "shake": 0, "rock": 0, "bdy": -1,
})

UNSURE = _mk({
    "esx": 0.95, "esy": 1.02, "tilt": 4, "edy": -0.2, "edx": 0.3,
    "esx2": 0.24, "esy2": -0.44, "tilt2": -18, "edy2": 0,
    "lock": 1, "heat": 0, "shake": 0, "rock": 0, "bdy": 0,
})

SCARED = _mk({
    "esx": 0.78, "esy": 0.96, "tilt": -12, "edy": -1.5, "edx": -0.8,
    "esx2": -0.04, "esy2": 0.05, "tilt2": 4, "edy2": 0,
    "lock": 1, "heat": 0, "shake": 0.35, "rock": 0, "bdy": -0.6,
})

LOVE = _mk({
    "esx": 0.86, "esy": 1.28, "tilt": -14, "edy": -0.5, "edx": -0.35,
    "esx2": 0.05, "esy2": 0.06, "tilt2": 6, "edy2": 0,
    "lock": 1, "heat": 0.6, "shake": 0, "rock": 0, "bdy": -1.6,
}, tint=lambda pal, p: tint_with(pal, p, ROSE))

SHY = _mk({
    "esx": 0.62, "esy": 0.5, "tilt": 10, "edy": 1.4, "edx": -0.2,
    "esx2": -0.05, "esy2": -0.04, "tilt2": -8, "edy2": 0,
    "lock": 1, "heat": 0.55, "shake": 0, "rock": 0, "bdy": 0.9,
}, tint=lambda pal, p: tint_with(pal, p, BLUSH))

SICK = _mk({
    "esx": 1.25, "esy": 0.34, "tilt": 20, "edy": 1.8, "edx": 0.8,
    "esx2": 0.05, "esy2": -0.05, "tilt2": -6, "edy2": 0,
    "lock": 1, "heat": 0.6, "shake": 0.18, "rock": 0, "bdy": 1.4,
}, tint=lambda pal, p: tint_with(pal, p, BILE))

THINKING = _mk({
    "esx": 1.15, "esy": 0.62, "tilt": 0, "edy": 4.2, "edx": 0.4,
    "esx2": 0.02, "esy2": 0.06, "tilt2": 0, "edy2": -8.4,
    "lock": 1, "heat": 0, "shake": 0, "rock": 0.8, "bdy": -0.4,
})

EXPRESSIONS = {
    "idle": IDLE,
    "happy": HAPPY,
    "sad": SAD,
    "mad": MAD,
    "surprised": SURPRISED,
    "wink": WINK,
    "sleepy": SLEEPY,
    "smug": SMUG,
    "unsure": UNSURE,
    "scared": SCARED,
    "love": LOVE,
    "shy": SHY,
    "sick": SICK,
    "thinking": THINKING,
}