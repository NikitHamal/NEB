#!/usr/bin/env python3
"""Emits the web's refraction displacement maps.

The app bends the backdrop in AGSL: it evaluates a rounded-rect signed-distance
function per pixel, takes its gradient for the surface normal, concentrates the
bend into the outer `rim` pixels with a cube, and samples the backdrop along
`-normal * bend * refraction`. See NEB_GLASS_AGSL in NebLiquidGlass.kt.

The web has no per-pixel shader in CSS, but it has SVG's feDisplacementMap,
which does exactly one thing: offset each pixel by a vector read out of a second
image. So the shader's *arithmetic* moves out of the renderer and into an image
computed here, once, with the same formulas:

    off = normalize(grad(sd)) * clamp(1 + sd/rim, 0, 1)^3 * refraction

feDisplacementMap computes  P'(x, y) = P(x + s*(R - 0.5), y + s*(G - 0.5)).
Matching `-off` with s = 2*refraction gives

    R = 0.5 - n.x * bend / 2
    G = 0.5 - n.y * bend / 2

which is what the red and green channels below hold. Blue is unused; alpha is
opaque, because a transparent map makes Chrome treat the pixel as zero rather
than as neutral and the glass tears at the corners.

Two maps, because a single one cannot serve both surfaces. The filter stretches
its map over the element with preserveAspectRatio="none", and stretching is only
free along an axis the field does not vary in:

  neb-glass-pill.png  A rounded rect. Authored at the bottom nav's own geometry
                      so its corners arrive undistorted; a narrower phone
                      squashes them by under a fifth, which is invisible at a
                      14px displacement.
  neb-glass-band.png  Top and bottom edges only, no corners, constant in x --
                      so it stretches across a 1400px topbar exactly.

Run: python3 tools/art/genglassmap.py
"""
import os
import math
import numpy as np
from PIL import Image

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
OUT = os.path.join(_ROOT, "backend_python/web/static/web/img/glass")

# The light style's values, from rememberNebGlassStyle(isDark = false). The dark
# style differs only in rim (21 vs 21) and refraction (14 vs 14) -- which is to
# say it does not differ at all in geometry, so one map serves both themes.
RIM = 21.0
SUPERSAMPLE = 2


def sd_round(px, py, bx, by, r):
    """The AGSL's sdRound, vectorised. p is relative to the centre, b is the
    half-extent, r the corner radius."""
    qx = np.abs(px) - bx + r
    qy = np.abs(py) - by + r
    inner = np.minimum(np.maximum(qx, qy), 0.0)
    outer = np.hypot(np.maximum(qx, 0.0), np.maximum(qy, 0.0))
    return inner + outer - r


def field(w, h, radius, rim, edges="all"):
    """The displacement map for a w x h rounded rect, as a float RGB array.

    `edges="y"` zeroes the x component and the left/right contribution, which
    is what makes the band map constant in x.
    """
    s = SUPERSAMPLE
    W, H = w * s, h * s
    # Pixel centres, in element units, relative to the centre of the rect.
    xs = (np.arange(W) + 0.5) / s - w * 0.5
    ys = (np.arange(H) + 0.5) / s - h * 0.5
    px, py = np.meshgrid(xs, ys)

    bx, by = w * 0.5, h * 0.5
    r = min(radius, bx, by)

    if edges == "y":
        # A rect infinitely wide: the left and right edges are pushed out of
        # reach, so only the horizontal edges contribute and the field has no
        # x variation at all.
        bx, r = bx + 4.0 * rim, 0.0

    d = sd_round(px, py, bx, by, r)

    # Central difference, same e = 1.0 as the shader. In element units, because
    # that is what the shader's uniforms are in.
    e = 1.0
    gx = (sd_round(px + e, py, bx, by, r) - sd_round(px - e, py, bx, by, r))
    gy = (sd_round(px, py + e, bx, by, r) - sd_round(px, py - e, bx, by, r))
    mag = np.hypot(gx, gy)
    mag = np.where(mag < 1e-6, 1.0, mag)
    nx, ny = gx / mag, gy / mag

    t = np.clip(1.0 + d / max(rim, 1.0), 0.0, 1.0)
    bend = t ** 3

    if edges == "y":
        nx = np.zeros_like(nx)

    # R and G as derived in the docstring; the halved amplitude is paid back by
    # the filter's scale = 2 * refraction.
    R = 0.5 - nx * bend * 0.5
    G = 0.5 - ny * bend * 0.5
    B = np.zeros_like(R)

    rgb = np.stack([R, G, B], axis=-1)
    # Box-downsample the supersampled field. The corners are where the normal
    # turns fastest and an aliased normal there shows up as a hard facet.
    rgb = rgb.reshape(h, s, w, s, 3).mean(axis=(1, 3))
    return np.clip(rgb, 0.0, 1.0)


def write(name, rgb):
    a = np.round(rgb * 255.0).astype(np.uint8)
    h, w, _ = a.shape
    rgba = np.dstack([a, np.full((h, w, 1), 255, np.uint8)])
    path = os.path.join(OUT, name)
    Image.fromarray(rgba, "RGBA").save(path, optimize=True)
    print("wrote %s  %dx%d  %d bytes" % (path, w, h, os.path.getsize(path)))
    return a


def shader_offset(x, y, w, h, radius, rim, edges="all"):
    """What NEB_GLASS_AGSL computes at one pixel centre, as (n.x*bend,
    n.y*bend). A scalar, literal transcription -- the point of it is to be
    obviously the same arithmetic as the shader, not to be fast."""
    bx, by, r = w * 0.5, h * 0.5, min(radius, w * 0.5, h * 0.5)
    if edges == "y":
        bx, r = bx + 4.0 * rim, 0.0
    px, py = x + 0.5 - w * 0.5, y + 0.5 - h * 0.5

    def sd(ax, ay):
        qx, qy = abs(ax) - bx + r, abs(ay) - by + r
        return (min(max(qx, qy), 0.0)
                + math.hypot(max(qx, 0.0), max(qy, 0.0)) - r)

    d = sd(px, py)
    gx = sd(px + 1.0, py) - sd(px - 1.0, py)
    gy = sd(px, py + 1.0) - sd(px, py - 1.0)
    mag = math.hypot(gx, gy) or 1.0
    nx, ny = gx / mag, gy / mag
    if edges == "y":
        nx = 0.0
    bend = min(max(1.0 + d / max(rim, 1.0), 0.0), 1.0) ** 3
    return nx * bend, ny * bend


def check(name, a, w, h, radius, rim, edges="all"):
    """Every pixel of the map must decode to the offset the shader would have
    produced there. Decoding is the browser's own: (C/255 - 0.5) * 2.

    Two known, quantified departures are tolerated. Neutral is 0.5, which 8 bits
    cannot hold -- it rounds to 128/255, so the whole field carries a +0.002
    bias, worth 0.055px of displacement at scale = 28. And the map is
    box-downsampled from 2x, so a pixel whose subsamples straddle a crease in
    the normal field lands between them; that is antialiasing, and it is why the
    corners do not facet."""
    h_px, w_px, _ = a.shape
    worst = 0.0
    worst_at = None
    total = 0.0
    for y in range(h_px):
        for x in range(w_px):
            wx, wy = shader_offset(x, y, w, h, radius, rim, edges)
            # The browser reads the map as a displacement, and the shader
            # displaces by *minus* the normal -- inward, which is what makes the
            # rim magnify rather than smear outward. So the decoded vector is
            # -n*bend and that is what the reference has to be compared against.
            gx = (a[y, x, 0] / 255.0 - 0.5) * 2.0
            gy = (a[y, x, 1] / 255.0 - 0.5) * 2.0
            e = math.hypot(gx + wx, gy + wy)
            total += e
            if e > worst:
                worst, worst_at = e, (x, y)
    n = w_px * h_px
    # 0.02 of a unit normal, at 14px of refraction, is 0.3px of displacement.
    ok = worst < 0.06
    print("  %s: %d px, mean err %.5f, worst %.5f at %s -- %s"
          % (name, n, total / n, worst, worst_at, "ok" if ok else "TOO HIGH"))
    return 0 if ok else 1


os.makedirs(OUT, exist_ok=True)
bad = 0

# The bottom nav: width min(340px, 100% - 32px), height 52, border-radius 24.
pill = field(340, 52, 24.0, RIM)
bad += check("pill", write("neb-glass-pill.png", pill), 340, 52, 24.0, RIM)

# The topbar: full width, square corners, height 64.
band = field(32, 64, 0.0, RIM, edges="y")
bad += check("band", write("neb-glass-band.png", band), 32, 64, 0.0, RIM,
             edges="y")

# Constant in x is the band map's whole contract; assert it rather than trust it.
spread = float(np.abs(band - band[:, :1, :]).max())
print("  band x-variance: %.9f (must be 0, or it cannot stretch)" % spread)
bad += spread > 1e-9

raise SystemExit(1 if bad else 0)
