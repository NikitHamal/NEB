"""Port of blobatar/src/styles/blob.ts, compose.ts and shapes.ts — the v2 silhouette vocabulary.

Ten weighted silhouettes (round, organic, boxy, capsule, nub, cloud, droplet,
hexagon, sun, triangle), a shared body/eyes composer and the frozen band table.
"""

import math

from .shape import blob_path, box, polygon, superellipse, taper
from .traits import Traits


def _poly(b):
    return polygon(b["cx"], b["cy"], b["rx"], b["ry"], b["sides"], b["round"], b["rot"])


def _spline(b):
    return blob_path(b["cx"], b["cy"], b["rx"], b["ry"], b["radii"], b["rot"])


def _shrunk(k):
    return lambda b: {"cx": b["cx"], "cy": b["cy"], "rx": b["rx"] * k, "ry": b["ry"] * k}


def _spline_face(b):
    return _shrunk(min(b["radii"]) * 0.95)(b)


def _poly_face(b):
    return _shrunk(0.84)(b)


ROUND = {"name": "round", "core": 1}

ORGANIC = {"name": "organic", "core": 0.98, "path": _spline, "face": _spline_face}

BOXY = {
    "name": "boxy", "core": 0.86,
    "body": lambda t, b: b.update({
        "n": t.num("body.n", 3.4, 6),
        "rot": t.num("body.rot", -20, 20),
    }),
}

CAPSULE = {
    "name": "capsule", "core": 1.02,
    "body": lambda t, b: b.update({"ry": b["ry"] * t.num("capsule.squat", 0.55, 0.68)}),
    "face": _shrunk(0.94),
    "decorate": lambda _t, b, out: [
        out["petals"].append({"cx": b["cx"] + s * (b["rx"] - b["ry"]), "cy": b["cy"], "r": b["ry"]})
        for s in (-1, 1)
    ],
    "path": lambda b: box(b["cx"], b["cy"], b["rx"] - b["ry"], b["ry"]),
}

NUB = {
    "name": "nub", "core": 0.88,
    "decorate": lambda t, b, out: [
        out["petals"].append({
            "cx": b["cx"] + math.cos(t.num("nub.a%d" % i, 0, 2 * math.pi)) * b["rx"] * 0.88,
            "cy": b["cy"] + math.sin(t.num("nub.a%d" % i, 0, 2 * math.pi)) * b["rx"] * 0.88,
            "r": b["rx"] * t.num("nub.r%d" % i, 0.24, 0.4),
        })
        for i in range(t.int("nub.n", 1, 2))
    ],
}

def _cloud_decorate(t, b, out):
    count = t.int("cloud.n", 4, 6)
    for i in range(count):
        a = math.pi + (math.pi * (i + 0.5)) / count
        out["petals"].append({
            "cx": b["cx"] + math.cos(a) * b["rx"] * 0.8,
            "cy": b["cy"] + math.sin(a) * b["rx"] * 0.5,
            "r": b["rx"] * t.num("cloud.r%d" % i, 0.44, 0.62),
        })


CLOUD = {
    "name": "cloud", "core": 0.78, "face": _spline_face, "path": _spline,
    "decorate": _cloud_decorate,
}

DROPLET = {
    "name": "droplet", "core": 0.78,
    "body": lambda _t, b: b.update({"cy": b["cy"] + 0.22 * b["ry"], "n": 2}),
    "face": lambda b: {"cx": b["cx"], "cy": b["cy"] + b["ry"] * 0.05,
                       "rx": b["rx"] * 0.88, "ry": b["ry"] * 0.88},
    "decorate": lambda t, b, out: out["extra"].append(
        taper(b["cx"], b["cy"], b["rx"], b["ry"], t.num("droplet.tip", 1.4, 1.65))
    ),
}

HEXAGON = {
    "name": "hexagon", "core": 1.05, "path": _poly, "face": _poly_face,
    "body": lambda t, b: b.update({
        "sides": 6,
        "rot": t.num("body.rot", -12, 12),
        "round": t.num("poly.round", 0.24, 0.5),
    }),
}

def _sun_decorate(t, b, out):
    count = t.int("sun.n", 6, 9)
    dist = b["rx"] * t.num("sun.dist", 1.0, 1.08)
    pr = b["rx"] * t.num("sun.r", 0.2, 0.26)
    off = t.num("sun.rot", 0, 2 * math.pi)
    for i in range(count):
        a = off + (2 * math.pi * i) / count
        out["petals"].append({
            "cx": b["cx"] + math.cos(a) * dist,
            "cy": b["cy"] + math.sin(a) * dist,
            "r": pr,
        })


SUN = {
    "name": "sun", "core": 0.7,
    "decorate": _sun_decorate,
}

TRIANGLE = {
    "name": "triangle", "core": 1.15, "path": _poly,
    "body": lambda t, b: b.update({
        "sides": 3,
        "rot": t.num("body.rot", -5, 5),
        "round": t.num("poly.round", 0.24, 0.5),
    }),
    "face": lambda b: {"cx": b["cx"], "cy": b["cy"] + b["ry"] * 0.1,
                       "rx": b["rx"] * 0.54, "ry": b["ry"] * 0.36},
}


BANDS = [
    (ROUND, 0.22), (ORGANIC, 0.48), (BOXY, 0.6), (CAPSULE, 0.7), (NUB, 0.79),
    (CLOUD, 0.86), (DROPLET, 0.915), (HEXAGON, 0.95), (SUN, 0.98), (TRIANGLE, 1),
]


def pick_shape(v):
    for shape, up_to in BANDS:
        if v < up_to:
            return shape
    return BANDS[-1][0]


def face_fit(t, b, face):
    """Fits the eye cluster against the silhouette's face region on both axes."""
    rx = b["rx"]
    er0 = t.num("eye.rx", 0.075, 0.105) * rx
    ratio = t.num("eye.ratio", 1.9, 3.2)
    scale = t.num("eye.scale", 0.78, 1.24)
    stretch = t.num("eye.stretch", 0.85, 1.18)
    clearance = t.num("eye.gap", 0.1, 0.24) * rx
    wide = er0 * max(1, scale)
    tall = er0 * ratio * max(1, scale * stretch)
    gap0 = wide + rx * 0.03 + clearance

    gx = t.jitter("gaze.x", 0.09) * face["rx"]
    gy = t.num("gaze.y", -0.2, 0.08) * face["ry"]
    dy = t.jitter("eye.dy", 0.04) * face["ry"]
    reach = math.hypot(wide, tall)
    need = math.hypot(
        (abs(gx) + gap0 + reach) / face["rx"],
        (abs(gy) + abs(dy) + reach) / face["ry"],
    )
    fit = 0.9 / need if need > 0.9 else 1

    er = er0 * fit
    eye_ry = er * ratio
    gap = gap0 * fit
    room = max(0, min(1, clearance / tall))
    bound = min(12, (math.asin(room) * 180) / math.pi)
    lean = t.num("eye.lean", -1, 1) * bound
    lean2 = max(-12, min(12, lean + t.jitter("eye.lean2", 3.5)))

    cx = face["cx"] + gx * fit
    cy = face["cy"] + gy * fit
    n = t.num("eye.n", 3.5, 6)
    return [
        {"cx": cx - gap, "cy": cy, "rx": er, "ry": eye_ry, "n": n, "rot": lean},
        {"cx": cx + gap, "cy": cy + dy * fit, "rx": er * scale,
         "ry": eye_ry * scale * stretch, "n": n, "rot": lean2},
    ]


def layout(t):
    shape = pick_shape(t("shape"))
    r = t.num("body.r", 31, 38) * shape["core"]
    body = {
        "cx": 50 + t.jitter("body.x", 1.5),
        "cy": 50 + t.jitter("body.y", 1.5),
        "rx": r,
        "ry": r * t.num("body.ratio", 0.92, 1.08),
        "n": t.num("body.n", 1.9, 2.5),
        "rot": 0,
        "radii": [1 + t.jitter("body.r%d" % i, 0.16)
                  for i in range(t.int("body.pts", 6, 8))],
    }
    if shape.get("body"):
        shape["body"](t, body)

    face = shape["face"](body) if shape.get("face") else body
    deco = {"petals": [], "extra": []}
    if shape.get("decorate"):
        shape["decorate"](t, body, deco)

    return {
        "shape": shape["name"],
        "draw": shape.get("path"),
        "body": body,
        "face": face,
        "petals": deco["petals"],
        "extra": deco["extra"],
        "eyes": face_fit(t, body, face),
    }


def _r2(v):
    s = math.floor(v * 100 + 0.5) / 100
    if s == 0:
        return "0"
    if s.is_integer():
        return str(int(s))
    return str(s)


def render(l, p, mo=False):
    def eye(e, i):
        path = '<path d="%s"/>' % superellipse(
            e["cx"], e["cy"], e["rx"], e["ry"], e["n"], e["rot"])
        if mo:
            return ('<g class="mo-eye" style="--mo-wrap:%d;--mo-lean:%s;'
                    'transform-origin:%s %s">%s</g>' % (
                        (1 if i else -1), _r2(e["rot"]), _r2(e["cx"]), _r2(e["cy"]), path))
        return path

    draw = l["draw"]
    core = draw(l["body"]) if draw else superellipse(
        l["body"]["cx"], l["body"]["cy"], l["body"]["rx"], l["body"]["ry"],
        l["body"]["n"], l["body"]["rot"])
    petals = "".join(
        '<circle cx="%s" cy="%s" r="%s"/>' % (_r2(d["cx"]), _r2(d["cy"]), _r2(d["r"]))
        for d in l["petals"]
    )
    extra = "".join('<path d="%s"/>' % d for d in l["extra"])
    body = (
        '<g fill="%s">' % p["head"]
        + petals + extra + '<path d="%s"/>' % core
        + "</g>"
        + '<g fill="%s">' % p["eye"]
        + "".join(eye(e, i) for i, e in enumerate(l["eyes"]))
        + "</g>"
    )
    if mo:
        return '<g class="mo-breathe"><g class="mo-bob">%s</g></g>' % body
    return body


background = False