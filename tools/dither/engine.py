"""Dither engine: fields in, limited-palette pixels out.

A scene builds float fields (0 dark .. 1 light) and paints them onto a Canvas through a palette and a
dither method. Everything is numpy; the only image code is the final write. Cells are the dither pixels,
`scale` blows each one up with nearest neighbour so the grain stays crisp.
"""
import numpy as np
from PIL import Image


# ---------------------------------------------------------------- palettes
def hexrgb(h):
    h = h.lstrip('#')
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


class Pal:
    """A ramp from darkest to lightest."""

    def __init__(self, name, *colors):
        self.name = name
        self.hex = list(colors)
        self.rgb = np.array([hexrgb(c) for c in colors], dtype=float)

    @property
    def k(self):
        return len(self.hex)


# ---------------------------------------------------------------- threshold maps
def _bayer(n):
    m = np.array([[0, 2], [3, 1]], dtype=float)
    while m.shape[0] < n:
        m = np.block([[4 * m, 4 * m + 2], [4 * m + 3, 4 * m + 1]])
    return (m + .5) / (n * n)


_BLUE = {}


def blue_noise(h, w, seed=7):
    key = (h, w, seed)
    if key not in _BLUE:
        r = np.random.default_rng(seed).random((h, w))
        f = np.fft.fft2(r)
        rad = np.sqrt(np.fft.fftfreq(h)[:, None] ** 2 + np.fft.fftfreq(w)[None, :] ** 2)
        f *= np.clip(rad * 7, 0, 1) ** 1.5
        b = np.fft.ifft2(f).real
        _BLUE[key] = (b.ravel().argsort().argsort().reshape(h, w) + .5) / (h * w)
    return _BLUE[key]


KERNELS = {
    'floyd': ([(1, 0, 7), (-1, 1, 3), (0, 1, 5), (1, 1, 1)], 16),
    'atkinson': ([(1, 0, 1), (2, 0, 1), (-1, 1, 1), (0, 1, 1), (1, 1, 1), (0, 2, 1)], 8),
    'jjn': ([(1, 0, 7), (2, 0, 5), (-2, 1, 3), (-1, 1, 5), (0, 1, 7), (1, 1, 5), (2, 1, 3),
             (-2, 2, 1), (-1, 2, 3), (0, 2, 5), (1, 2, 3), (2, 2, 1)], 48),
    'sierra': ([(1, 0, 2), (-1, 1, 1), (0, 1, 1)], 4),
}


def _diffuse(f, k, method):
    kern, div = KERNELS[method]
    f = f.astype(float).copy()
    h, w = f.shape
    out = np.zeros((h, w), dtype=int)
    km = k - 1
    for y in range(h):
        row = f[y]
        for x in range(w):
            old = row[x]
            i = int(round(min(1.0, max(0.0, old)) * km))
            out[y, x] = i
            err = old - i / km
            if err:
                for dx, dy, wt in kern:
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < w and yy < h:
                        f[yy, xx] += err * wt / div
    return out


def quant(f, k, method='bayer4', seed=3, cell=6.0, angle=45.0, center=None, freq=1.0):
    """Quantise field f (0..1) to k levels. Returns an int index array."""
    h, w = f.shape
    f = np.clip(f, 0, 1)
    if method in KERNELS:
        return _diffuse(f, k, method)
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    if method.startswith('bayer'):
        n = int(method[5:] or 4)
        thr = np.tile(_bayer(n), (h // n + 1, w // n + 1))[:h, :w]
    elif method == 'white':
        thr = np.random.default_rng(seed).random((h, w))
    elif method == 'blue':
        thr = blue_noise(h, w, seed)
    elif method == 'ign':
        thr = (52.9829189 * ((0.06711056 * xx + 0.00583715 * yy) % 1)) % 1
    elif method == 'halftone':
        a = np.radians(angle)
        u = (xx * np.cos(a) + yy * np.sin(a)) * 2 * np.pi / cell
        v = (-xx * np.sin(a) + yy * np.cos(a)) * 2 * np.pi / cell
        thr = (np.cos(u) + np.cos(v)) / 4 + .5
        thr = 1 - thr
    elif method == 'lines':
        a = np.radians(angle)
        u = (xx * np.cos(a) + yy * np.sin(a)) / cell
        thr = np.abs((u % 1) * 2 - 1)
    elif method == 'cross':
        a = np.radians(angle)
        u = (xx * np.cos(a) + yy * np.sin(a)) / cell
        v = (-xx * np.sin(a) + yy * np.cos(a)) / cell
        thr = np.minimum(np.abs((u % 1) * 2 - 1), np.abs((v % 1) * 2 - 1))
    elif method == 'radial':
        cx, cy = center if center else (w / 2, h / 2)
        r = np.hypot(xx - cx, yy - cy) / cell
        thr = np.abs((r % 1) * 2 - 1)
    elif method == 'spiral':
        cx, cy = center if center else (w / 2, h / 2)
        r = np.hypot(xx - cx, yy - cy) / cell
        th = np.arctan2(yy - cy, xx - cx) / (2 * np.pi)
        thr = np.abs((((r * freq) + th) % 1) * 2 - 1)
    else:
        raise ValueError(method)
    v = f * (k - 1)
    base = np.floor(v)
    idx = base + ((v - base) > thr)
    return np.clip(idx, 0, k - 1).astype(int)


# ---------------------------------------------------------------- field toolkit
def smooth(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def fbm(h, w, seed=1, octaves=5, base=4, gain=.5):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w))
    amp = 1.0
    tot = 0.0
    n = base
    for _ in range(octaves):
        g = rng.random((max(2, int(n * h / max(h, w)) + 2), max(2, int(n * w / max(h, w)) + 2)))
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += amp * np.asarray(im, dtype=float) / 255
        tot += amp
        amp *= gain
        n *= 2
    out /= tot
    lo, hi = out.min(), out.max()
    return (out - lo) / (hi - lo + 1e-9)


def rot(p, ax, a):
    """Rotate (...,3) points about an axis index."""
    c, s = np.cos(a), np.sin(a)
    q = p.copy()
    i, j = [(1, 2), (2, 0), (0, 1)][ax]
    q[..., i] = c * p[..., i] - s * p[..., j]
    q[..., j] = s * p[..., i] + c * p[..., j]
    return q


def sd_sphere(p, r):
    return np.linalg.norm(p, axis=-1) - r


def sd_box(p, b):
    q = np.abs(p) - np.array(b)
    return np.linalg.norm(np.maximum(q, 0), axis=-1) + np.minimum(q.max(axis=-1), 0)


def sd_torus(p, R, r):
    q = np.stack([np.hypot(p[..., 0], p[..., 2]) - R, p[..., 1]], -1)
    return np.linalg.norm(q, axis=-1) - r


def smin(a, b, k=.3):
    h = np.clip(.5 + .5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


def march(sdf, w, h, cam=(0, 0, -3.4), fov=.9, steps=70, far=14, light=(-.55, .7, -.45), gamma=1.0, amb=.08):
    """Sphere-trace sdf(p) over a w x h grid. Returns hit mask, shade 0..1, depth, normal."""
    xs = ((np.arange(w) + .5) / w * 2 - 1) * (w / h) * fov
    ys = (1 - (np.arange(h) + .5) / h * 2) * fov
    px, py = np.meshgrid(xs, ys)
    d = np.stack([px, py, np.ones_like(px)], -1)
    d /= np.linalg.norm(d, axis=-1, keepdims=True)
    o = np.broadcast_to(np.array(cam, dtype=float), d.shape)
    t = np.zeros((h, w))
    used = np.zeros((h, w))
    for _ in range(steps):
        dd = sdf(o + d * t[..., None])
        act = (dd > .002) & (t < far)
        t = t + np.where(act, dd, 0)
        used += act
    p = o + d * t[..., None]
    hit = (sdf(p) < .02) & (t < far)
    e = .004
    n = np.stack([sdf(p + np.array(v) * e) - sdf(p - np.array(v) * e) for v in ((1, 0, 0), (0, 1, 0), (0, 0, 1))], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-9
    L = np.array(light, dtype=float)
    L /= np.linalg.norm(L)
    lam = np.clip((n * L).sum(-1), 0, 1)
    rim = np.clip(1 - (n * -d).sum(-1), 0, 1) ** 3
    ao = 1 - .55 * (used / steps)
    shade = np.clip((amb + (1 - amb) * lam ** gamma) * ao + .18 * rim, 0, 1)
    return hit, shade, t, n


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg='#000000', seed=0):
        self.w, self.h = w, h
        self.rgb = np.zeros((h, w, 3)) + np.array(hexrgb(bg), dtype=float)
        self.rng = np.random.default_rng(seed)
        yy, xx = np.mgrid[0:h, 0:w].astype(float)
        self.X = (xx + .5 - w / 2) / (h / 2)
        self.Y = (yy + .5 - h / 2) / (h / 2)
        self.px, self.py = xx, yy

    def paint(self, field, pal, mask=None, method='bayer4', **kw):
        idx = quant(field, pal.k, method, **kw)
        col = pal.rgb[idx]
        if mask is None:
            self.rgb[:] = col
        else:
            self.rgb[mask] = col[mask]
        return idx

    def fill(self, mask, color):
        self.rgb[mask] = np.array(hexrgb(color), dtype=float)

    # -- glitch family -----------------------------------------------------------
    def glitch(self, n=8, maxshift=24, hmin=2, hmax=14, seed=5, zone=(0, 1)):
        rng = np.random.default_rng(seed)
        for _ in range(n):
            y0 = int(rng.uniform(*zone) * self.h)
            hh = int(rng.integers(hmin, hmax + 1))
            self.rgb[y0:y0 + hh] = np.roll(self.rgb[y0:y0 + hh], int(rng.integers(-maxshift, maxshift + 1)), axis=1)
        return self

    def split(self, dx=3, dy=0):
        self.rgb[..., 0] = np.roll(self.rgb[..., 0], dx, axis=1)
        self.rgb[..., 2] = np.roll(self.rgb[..., 2], -dx, axis=1)
        if dy:
            self.rgb[..., 0] = np.roll(self.rgb[..., 0], dy, axis=0)
        return self

    def scan(self, every=3, amt=.18):
        self.rgb[::every] *= 1 - amt
        return self

    def sort_band(self, y0, y1, seed=2):
        """Pixel-sort a band of rows by brightness, a classic glitch."""
        for y in range(int(y0 * self.h), int(y1 * self.h)):
            row = self.rgb[y]
            if (y * 7 + seed) % 3:
                continue
            a = int(self.w * .2); b = int(self.w * .85)
            order = np.argsort(row[a:b].sum(-1))
            row[a:b] = row[a:b][order]
        return self

    # -- output ------------------------------------------------------------------
    def image(self, scale=4):
        im = Image.fromarray(np.clip(self.rgb, 0, 255).astype(np.uint8))
        return im.resize((self.w * scale, self.h * scale), Image.NEAREST)
