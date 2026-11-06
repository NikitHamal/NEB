"""Modern scenes, plus the dune library that backs the resource cover."""
import numpy as np
from engine import smooth, fbm
from kit import scene


def _ridge(c, seed, base, amp, freq, phase):
    prof = fbm(2, c.w, seed, 4, 3)[0]
    xs = c.px[0]
    return base + amp * np.sin(xs * freq + phase) + .09 * (prof - .5)


@scene('sunset-grid', 'Sunset grid', 'Modern', 240, 150,
       [('ember', 'bayer8', {}), ('lava', 'floyd', {}), ('amber', 'atkinson', {}), ('bone', 'bayer4', {})])
def sunset_grid(c, pal, method, **kw):
    X, Y = c.X, c.Y
    hz = .16
    sky = .1 + .55 * smooth(-.9, hz, Y)
    sun = np.hypot(X, Y + .1) < .52
    bars = (Y > -.08) & (((Y + .08) * 15) % 1 < (Y + .08) * 1.5)
    f = np.where(sun & ~bars, .55 + .45 * smooth(-.62, .35, Y), sky)
    ridge = hz - .11 * fbm(2, c.w, 6, 5, 4)[0][None, :] * np.ones((c.h, 1)) - .01
    f = np.where((Y > ridge) & (Y < hz), .04, f)
    z = 1 / np.maximum(Y - hz, 1e-3)
    vx = np.abs(((X * z * .55) % 1) - .5)
    vz = np.abs(((z * .45) % 1) - .5)
    line = (vx > .5 - .035 * np.minimum(z, 12)) | (vz > .5 - .02 * np.minimum(z, 12))
    f = np.where(Y >= hz, .05 + .85 * line * smooth(hz, hz + .4, Y) ** .6, f)
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('rain-city', 'Rain city', 'Modern', 240, 150,
       [('amber', 'bayer4', {}), ('bone', 'floyd', {}), ('acid', 'atkinson', {}), ('lava', 'bayer8', {})])
def rain_city(c, pal, method, **kw):
    rng = np.random.default_rng(8)
    X, Y = c.X, c.Y
    sky = .15 + .6 * smooth(-.8, .5, Y)
    f = np.where(np.hypot(X + .8, Y + .5) < .17, 1.0, sky)
    x = 0
    while x < c.w:
        bw = int(rng.integers(8, 20))
        top = int(c.h * (.25 + .5 * rng.random() ** 1.5))
        tone = .06 + .1 * rng.random()
        sl = (c.px >= x) & (c.px < x + bw) & (c.py >= top)
        f = np.where(sl, tone, f)
        win = sl & ((c.px - x) % 4 < 2) & ((c.py - top) % 5 < 3) & (c.px > x + 1) & (c.px < x + bw - 2) & (c.py > top + 2)
        lit = rng.random((c.h, c.w)) > .62
        f = np.where(win & lit, .85, f)
        x += bw + int(rng.integers(0, 3))
    offs = rng.integers(0, 23, c.w)
    on = rng.random(c.w) > .55
    streak = ((c.py + c.px * .35 + offs[c.px.astype(int)]) % 23 < 4) & on[c.px.astype(int)]
    f = np.where(streak, np.maximum(f, .5), f)
    c.paint(np.clip(f, 0, 1), pal, method=method)
    c.glitch(n=3, maxshift=6, seed=2, zone=(.5, 1))


@scene('data-rain', 'Data rain', 'Modern', 160, 200,
       [('phosphor', 'bayer2', {}), ('acid', 'floyd', {}), ('amber', 'bayer4', {}), ('signal', 'atkinson', {})])
def data_rain(c, pal, method, **kw):
    rng = np.random.default_rng(13)
    cw, ch = 4, 5
    ncol = c.w // cw + 1
    head = rng.random(ncol) * c.h * 1.6
    length = 30 + rng.random(ncol) * 90
    ci = (c.px // cw).astype(int)
    ri = (c.py // ch).astype(int)
    dy = head[ci] - c.py
    trail = np.where((dy >= 0) & (dy < length[ci]), np.exp(-dy / length[ci] * 3.2), 0)
    glyph = rng.random((c.h // ch + 2, ncol + 1))[ri, ci] > .3
    inner = ((c.px % cw) < cw - 1) & ((c.py % ch) < ch - 1)
    f = trail * glyph * inner
    f = np.where((dy >= 0) & (dy < ch) & inner, 1.0, f)
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('vinyl-light', 'Vinyl in light', 'Modern', 180, 180,
       [('bone', 'floyd', {}), ('signal', 'bayer4', {}), ('gold', 'atkinson', {}), ('jade', 'bayer8', {})])
def vinyl(c, pal, method, **kw):
    r = np.hypot(c.X, c.Y) + 1e-4
    th = np.arctan2(c.Y, c.X)
    groove = .5 + .5 * np.sin(r * 230)
    beam = np.maximum(np.cos(2 * (th + .7)), 0) ** 10
    f = .1 + .08 * groove + .75 * beam * (.4 + .6 * groove) * smooth(.3, .45, r)
    f = np.where(r < .3, .88, f)
    f = np.where((r < .3) & (np.abs(r - .25) < .012), .05, f)
    f = np.where((r < .3) & (r > .1) & (np.sin(th * 5 + r * 9) > .5) & (r < .22), .35, f)
    f = np.where(r < .03, .02, f)
    f = np.where(r > .92, .16 * smooth(1.2, .92, r), f)
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('dune-library', 'Dune library', 'Cover', 300, 190,
       [('sand', 'bayer4', {}), ('bone', 'bayer4', {}), ('ember', 'bayer8', {})], scale=4)
def dune_library(c, pal, method, **kw):
    X, Y = c.X, c.Y
    aspect = c.w / c.h
    f = .02 + .10 * smooth(.1, .55, Y)
    tex = fbm(c.h, c.w, 3, 5, 6)
    moon = np.hypot(X - aspect * .62, Y + .5)
    f = np.where(moon < .25, .78 + .22 * (tex > .55) * .0 + .12 * (tex - .5), f + np.exp(-np.maximum(moon - .25, 0) * 7) * .3)
    hz = .36
    # far ziggurat on the left, bright against the dark sky
    zx = -aspect * .72
    for hw, top in ((.2, .16), (.15, .09), (.1, .02), (.05, -.05)):
        f = np.where((np.abs(X - zx) < hw) & (Y > top) & (Y < hz + .05), .82 - .2 * (X > zx) - .1 * (top > .1), f)
    layers = [(.42, .06, 2.1, 0.3, 11, .34, .6), (.58, .08, 1.5, 2.0, 12, .5, .72), (.76, .08, 1.1, 4.1, 13, .66, .88)]
    for base, amp, freq, ph, seed, lo, hi in layers:
        rid = _ridge(c, seed, base, amp, freq, ph)[None, :]
        depth = (Y - rid)
        inside = depth > 0
        crest = smooth(0, .22, depth)
        wind = .5 + .5 * np.cos(c.px * .05 * freq + depth * 9)
        shade = lo + (hi - lo) * (.35 * crest + .65 * wind)
        shade = shade - .22 * (np.abs(((depth * 24) % 1) * 2 - 1) > .86)
        f = np.where(inside, shade, f)
    c.paint(np.clip(f, 0, 1), pal, method=method)
    # sparse stars far from the title area
    s = (np.random.default_rng(2).random((c.h, c.w)) > .993) & (Y < .22) & ((np.abs(X) > aspect * .45) | (Y < -.55))
    c.rgb[s] = pal.rgb[-1]
