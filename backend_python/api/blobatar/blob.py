"""Port of blobatar/src/styles/blob.ts — gen 1 layout and render."""

import math

from .color import palette as build_palette
from .shape import blob_path, superellipse
from .traits import Traits


def _shape_of(v):
    if v < 0.28:
        return "round"
    if v < 0.58:
        return "organic"
    if v < 0.72:
        return "boxy"
    if v < 0.84:
        return "nub"
    if v < 0.93:
        return "cloud"
    return "sun"


CORE = {
    "round": 1,
    "boxy": 0.86,
    "organic": 0.98,
    "cloud": 0.78,
    "sun": 0.7,
    "nub": 0.88,
}


def layout(t):
    shape = _shape_of(t("shape"))
    r = t.num("body.r", 31, 38) * CORE[shape]
    rx = r
    ry = r * t.num("body.ratio", 0.92, 1.08)

    body = {
        "cx": 50 + t.jitter("body.x", 1.5),
        "cy": 50 + t.jitter("body.y", 1.5),
        "rx": rx,
        "ry": ry,
        "n": t.num("body.n", 3.4, 6) if shape == "boxy" else t.num("body.n", 1.9, 2.5),
        "rot": t.num("body.rot", -20, 20) if shape == "boxy" else 0,
        "radii": [
            1 + t.jitter("body.r%d" % i, 0.16)
            for i in range(t.int("body.pts", 6, 8))
        ],
    }

    gx = t.jitter("gaze.x", 0.09) * rx
    gy = t.num("gaze.y", -0.2, 0.08) * ry

    er0 = t.num("eye.rx", 0.075, 0.105) * rx
    ratio = t.num("eye.ratio", 1.9, 3.2)
    scale = t.num("eye.scale", 0.78, 1.24)
    stretch = t.num("eye.stretch", 0.85, 1.18)

    clearance = t.num("eye.gap", 0.1, 0.24) * rx
    wide = er0 * max(1, scale)
    tall = er0 * ratio * max(1, scale * stretch)
    gap0 = wide + rx * 0.03 + clearance

    tight = (min(body["radii"]) * 0.95) if shape in ("organic", "cloud") else 1
    need = (abs(gx) + gap0 + math.hypot(wide, tall)) / rx
    fit = (tight * 0.9) / need if need > tight * 0.9 else 1

    er = er0 * fit
    gap = gap0 * fit
    eye_ry = er * ratio

    MAX_LEAN = 12
    room = max(0, min(1, (clearance * fit) / (tall * fit)))
    bound = min(MAX_LEAN, (math.asin(room) * 180) / math.pi)
    lean = t.num("eye.lean", -1, 1) * bound
    lean2 = max(-MAX_LEAN, min(MAX_LEAN, lean + t.jitter("eye.lean2", 3.5)))

    petals = []

    if shape == "sun":
        count = t.int("sun.n", 6, 9)
        dist = r * t.num("sun.dist", 1.0, 1.08)
        pr = r * t.num("sun.r", 0.2, 0.26)
        off = t.num("sun.rot", 0, 2 * math.pi)
        for i in range(count):
            a = off + (2 * math.pi * i) / count
            petals.append({
                "cx": body["cx"] + math.cos(a) * dist,
                "cy": body["cy"] + math.sin(a) * dist,
                "r": pr,
            })
    elif shape == "cloud":
        count = t.int("cloud.n", 4, 6)
        for i in range(count):
            a = math.pi + (math.pi * (i + 0.5)) / count
            petals.append({
                "cx": body["cx"] + math.cos(a) * r * 0.8,
                "cy": body["cy"] + math.sin(a) * r * 0.5,
                "r": r * t.num("cloud.r%d" % i, 0.44, 0.62),
            })
    elif shape == "nub":
        count = t.int("nub.n", 1, 2)
        for i in range(count):
            a = t.num("nub.a%d" % i, 0, 2 * math.pi)
            petals.append({
                "cx": body["cx"] + math.cos(a) * r * 0.88,
                "cy": body["cy"] + math.sin(a) * r * 0.88,
                "r": r * t.num("nub.r%d" % i, 0.24, 0.4),
            })

    return {
        "shape": shape,
        "body": body,
        "petals": petals,
        "eyes": [
            {
                "cx": body["cx"] + gx - gap,
                "cy": body["cy"] + gy,
                "rx": er,
                "ry": eye_ry,
                "n": t.num("eye.n", 3.5, 6),
                "rot": lean,
            },
            {
                "cx": body["cx"] + gx + gap,
                "cy": body["cy"] + gy + t.jitter("eye.dy", 0.04) * ry,
                "rx": er * scale,
                "ry": eye_ry * scale * stretch,
                "n": t.num("eye.n", 3.5, 6),
                "rot": lean2,
            },
        ],
    }


def _r2(v):
    s = math.floor(v * 100 + 0.5) / 100
    if s == 0:
        return "0"
    if s.is_integer():
        return str(int(s))
    return str(s)


def render(l, p, mo=False):
    b = l["body"]
    if l["shape"] in ("organic", "cloud"):
        core = blob_path(
            b["cx"], b["cy"], b["rx"], b["ry"], b["radii"],
            0 if l["shape"] == "cloud" else b["rot"],
        )
    else:
        core = superellipse(b["cx"], b["cy"], b["rx"], b["ry"], b["n"], b["rot"])

    def eye(e):
        return '<path d="%s"/>' % superellipse(e["cx"], e["cy"], e["rx"], e["ry"], e["n"], e["rot"])

    body = (
        '<g fill="%s">' % p["head"]
        + "".join(
            '<circle cx="%s" cy="%s" r="%s"/>' % (_r2(d["cx"]), _r2(d["cy"]), _r2(d["r"]))
            for d in l["petals"]
        )
        + '<path d="%s"/>' % core
        + "</g>"
        + '<g fill="%s">' % p["eye"]
        + "".join(eye(e) for e in l["eyes"])
        + "</g>"
    )

    return body


background = False
