"""Cosmic and sculptural scenes: raymarched forms and orbs, dithered."""
import numpy as np
from engine import (smooth, fbm, rot, sd_sphere, sd_box, sd_torus, smin, march)
from kit import scene, P


def _stars(c, pal, mask, density=.994, seed=11):
    s = (np.random.default_rng(seed).random((c.h, c.w)) > density) & ~mask
    c.rgb[s] = pal.rgb[-1]


def _floor_shadow(c, cx, cy, rx, ry, amt):
    e = ((c.X - cx) / rx) ** 2 + ((c.Y - cy) / ry) ** 2
    return 1 - amt * np.exp(-e * 1.6)


@scene('moon-orb', 'Moon orb', 'Cosmic', 160, 200,
       [('bone', 'floyd', {}), ('ember', 'bayer8', {}), ('amber', 'atkinson', {}), ('jade', 'blue', {})])
def moon_orb(c, pal, method, **kw):
    hit, sh, t, n = march(lambda p: sd_sphere(p, .9), c.w, c.h, cam=(0, 0, -3), fov=.85, light=(-.7, .6, -.5))
    tex = fbm(c.h, c.w, 4, 5, 6)
    crater = np.clip((tex - .5) * .5, -.2, .2)
    r = np.hypot(c.X, c.Y)
    glow = np.exp(-np.maximum(r - .8, 0) * 5) * .45
    field = np.where(hit, np.clip(sh * .86 + crater, 0, 1), glow * (1 - hit))
    c.paint(field, pal, method=method)
    _stars(c, pal, hit)


@scene('torus-rest', 'Torus at rest', 'Modern', 160, 200,
       [('bone', 'bayer4', {}), ('lava', 'floyd', {}), ('lime', 'atkinson', {}), ('terracotta', 'bayer8', {})])
def torus_rest(c, pal, method, **kw):
    def sdf(p):
        q = rot(rot(p, 0, 1.0), 2, .45)
        return np.minimum(sd_torus(q, .72, .3), p[..., 1] + 1.0)
    hit, sh, t, n = march(sdf, c.w, c.h, cam=(0, .35, -3.2), fov=.58, light=(-.6, .8, -.5), far=18)
    fog = smooth(3, 12, t)
    sky = 1 - np.clip(np.hypot(c.X * .6, c.Y + .2), 0, 1)
    field = np.where(hit, np.clip(sh * (1 - .5 * fog) + .0, 0, 1), sky * .35)
    field = field * _floor_shadow(c, -.05, .62, .8, .12, .5) * (1 + 0 * field)
    c.paint(field, pal, method=method)


@scene('twist-ribbon', 'Twist ribbon', 'Modern', 160, 200,
       [('bone', 'floyd', {}), ('rose', 'bayer4', {}), ('amber', 'jjn', {})])
def twist_ribbon(c, pal, method, **kw):
    def sdf(p):
        q = rot(p, 0, 1.15)
        th = np.arctan2(q[..., 2], q[..., 0])
        qx = np.hypot(q[..., 0], q[..., 2]) - .75
        a = 3 * th
        u = qx * np.cos(a) + q[..., 1] * np.sin(a)
        v = -qx * np.sin(a) + q[..., 1] * np.cos(a)
        return (np.hypot(u / .36, v / .09) - 1) * .09 * .9
    hit, sh, t, n = march(sdf, c.w, c.h, cam=(0, 0, -3.3), fov=.6, steps=110, light=(-.5, .7, -.6))
    bgf = .22 * (1 - np.hypot(c.X, c.Y * .8))
    c.paint(np.where(hit, sh, np.clip(bgf, 0, 1)), pal, method=method)


@scene('melt-spheres', 'Melt spheres', 'Modern', 160, 200,
       [('bone', 'bayer8', {}), ('signal', 'floyd', {}), ('jade', 'atkinson', {}), ('sand', 'blue', {})])
def melt_spheres(c, pal, method, **kw):
    pts = [(-.35, .45, 0, .42), (.3, .15, .1, .5), (-.1, -.3, -.1, .36), (.28, -.62, 0, .26), (-.42, -.7, .1, .2)]
    def sdf(p):
        d = None
        for x, y, z, r in pts:
            s = sd_sphere(p - np.array([x, y, z]), r)
            d = s if d is None else smin(d, s, .32)
        return d
    hit, sh, t, n = march(sdf, c.w, c.h, cam=(0, 0, -3.2), fov=.62, light=(-.6, .5, -.7), gamma=1.2)
    bgf = .3 * smooth(.2, 1.1, np.hypot(c.X, c.Y)) * .0 + .16 * (1 - np.hypot(c.X, c.Y))
    c.paint(np.where(hit, sh, np.clip(bgf, 0, 1)), pal, method=method)


@scene('gyroid-cube', 'Gyroid cube', 'Modern', 160, 200,
       [('bone', 'bayer4', {}), ('lime', 'floyd', {}), ('ember', 'atkinson', {})])
def gyroid_cube(c, pal, method, **kw):
    k = 7.0
    def sdf(p):
        q = rot(rot(p, 1, .7), 0, .5)
        g = np.sin(q[..., 0] * k) * np.cos(q[..., 1] * k) + np.sin(q[..., 1] * k) * np.cos(q[..., 2] * k) \
            + np.sin(q[..., 2] * k) * np.cos(q[..., 0] * k)
        return np.maximum(sd_box(q, (.8, .8, .8)) - .02, (np.abs(g) - .55) / (k * 1.6)) * .8
    hit, sh, t, n = march(sdf, c.w, c.h, cam=(0, 0, -3.4), fov=.6, steps=90, light=(-.5, .8, -.5))
    bgf = .2 * np.clip(1 - np.hypot(c.X, c.Y) * .9, 0, 1)
    c.paint(np.where(hit, sh, bgf), pal, method=method)


@scene('orb-field', 'Orb field', 'Modern', 240, 150,
       [('bone', 'bayer4', {}), ('amber', 'floyd', {}), ('rose', 'atkinson', {})], scale=4)
def orb_field(c, pal, method, **kw):
    def sdf(p):
        q = p.copy()
        q[..., 0] = (q[..., 0] + 1.1) % 2.2 - 1.1
        q[..., 2] = (q[..., 2] + 1.1) % 2.2 - 1.1
        return np.minimum(sd_sphere(q - np.array([0, -.2, 0]), .7), p[..., 1] + 1.0)
    hit, sh, t, n = march(sdf, c.w, c.h, cam=(0, 1.1, -2.2), fov=.7, steps=100, far=40, light=(-.4, .8, -.3))
    fog = smooth(6, 34, t)
    sun = np.exp(-(((c.X + .35) ** 2 + (c.Y + .35) ** 2) / .035))
    sky = np.clip(.18 + .5 * smooth(-.35, .4, -c.Y) + .1 * (1 - np.abs(c.Y)) + sun * .9, 0, 1) * (c.Y < .25)
    c.paint(np.where(hit, np.clip(sh * (1 - fog) + fog * .5, 0, 1), sky), pal, method=method)


@scene('eclipse', 'Eclipse', 'Cosmic', 160, 200,
       [('bone', 'blue', {}), ('lava', 'bayer8', {}), ('gold', 'floyd', {})])
def eclipse(c, pal, method, **kw):
    r = np.hypot(c.X, c.Y)
    th = np.arctan2(c.Y, c.X)
    rays = 1 + .45 * np.sin(th * 21 + fbm(c.h, c.w, 3, 3, 5) * 9) * np.exp(-(r - .5) * 1.4)
    corona = np.exp(-np.maximum(r - .5, 0) * 4.2) * rays
    ring = np.exp(-((r - .5) / .018) ** 2)
    gem = np.exp(-(((c.X - .36) ** 2 + (c.Y + .34) ** 2) / .0025))
    field = np.clip(corona * .85 + ring + gem, 0, 1)
    field = np.where(r < .5, np.clip(ring * 0 + .02, 0, 1), field)
    c.paint(field, pal, method=method)


@scene('ringed-world', 'Ringed world', 'Cosmic', 160, 200,
       [('amber', 'floyd', {}), ('bone', 'bayer8', {}), ('ember', 'atkinson', {}), ('acid', 'jjn', {})])
def ringed_world(c, pal, method, **kw):
    X, Y = c.X * 1.0, c.Y * 1.0
    R = .62
    r = np.hypot(X, Y)
    inside = r < R
    z = np.sqrt(np.clip(R * R - X * X - Y * Y, 0, None))
    nx, ny, nz = X / R, Y / R, z / R
    lam = np.clip(nx * -.6 + ny * -.5 + nz * .6, 0, 1)
    bands = .5 + .5 * np.sin(Y * 22 + fbm(c.h, c.w, 2, 3, 6) * 4)
    planet = np.clip(lam * (.55 + .45 * bands), 0, 1)
    a = np.radians(-18)
    u = X * np.cos(a) - Y * np.sin(a)
    v = (X * np.sin(a) + Y * np.cos(a)) / .26
    rr = np.hypot(u, v)
    ring = (rr > .85) & (rr < 1.55)
    gaps = ((rr > 1.12) & (rr < 1.18)) | ((rr > 1.36) & (rr < 1.4))
    ring &= ~gaps
    ringf = .35 + .55 * (.5 + .5 * np.sin(rr * 55)) * smooth(.85, 1.0, rr) * (1 - smooth(1.4, 1.55, rr))
    front = v > 0
    shadow = inside & ~front & ring
    field = np.where(inside, planet, 0.0)
    field = np.where(ring & (front | ~inside), ringf, field)
    field = np.where(ring & inside & front, ringf, field)
    c.paint(np.clip(field, 0, 1), pal, method=method)
    _stars(c, pal, inside | ring, .993)


@scene('worm-tunnel', 'Worm tunnel', 'Modern', 160, 200,
       [('bone', 'bayer4', {}), ('signal', 'floyd', {}), ('lime', 'atkinson', {}), ('sand', 'bayer8', {})])
def worm_tunnel(c, pal, method, **kw):
    r = np.hypot(c.X, c.Y * .8) + 1e-3
    th = np.arctan2(c.Y, c.X)
    u = 1 / r
    f = .5 + .5 * np.sin(u * 5 + np.sin(th * 3) * 1.4)
    f2 = .5 + .5 * np.cos(th * 8 + u * 1.5)
    field = (f * .6 + f2 * .4) * smooth(.02, .5, r)
    c.paint(np.clip(field, 0, 1), pal, method=method)
    if kw.get('glitch', True):
        c.glitch(n=7, maxshift=14, seed=9)


@scene('liquid-chrome', 'Liquid chrome', 'Modern', 160, 200,
       [('bone', 'floyd', {}), ('lava', 'blue', {}), ('jade', 'bayer8', {}), ('gold', 'atkinson', {})])
def liquid_chrome(c, pal, method, **kw):
    a = fbm(c.h, c.w, 21, 4, 3)
    b = fbm(c.h, c.w, 22, 4, 3)
    f = np.sin((c.X * 2.4 + a * 5) + np.sin(c.Y * 3 + b * 6)) * .5 + .5
    f = np.sin(f * 7 + c.Y * 2) * .5 + .5
    f = np.clip(f * smooth(1.1, .35, np.hypot(c.X * .9, c.Y * .75)) + .06, 0, 1)
    c.paint(f, pal, method=method)


@scene('ripple-pond', 'Ripple pond', 'Modern', 160, 200,
       [('jade', 'bayer8', {}), ('bone', 'floyd', {}), ('signal', 'blue', {})])
def ripple_pond(c, pal, method, **kw):
    srcs = [(-.45, -.25), (.4, .1), (-.05, .62)]
    s = sum(np.cos(np.hypot(c.X - x, c.Y - y) * 38) for x, y in srcs) / 3
    f = (s * .5 + .5) * smooth(1.25, .5, np.hypot(c.X, c.Y))
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('mandala', 'Mandala', 'Ancient', 180, 180,
       [('gold', 'bayer8', {}), ('ember', 'floyd', {}), ('bone', 'atkinson', {}), ('rose', 'blue', {})], scale=4)
def mandala(c, pal, method, **kw):
    r = np.hypot(c.X, c.Y)
    th = np.arctan2(c.Y, c.X)
    k = 12
    a = np.abs(((th * k / (2 * np.pi)) % 1) - .5) * 2
    petals = .5 + .5 * np.cos(r * 34 - a * 4.2)
    rings = .5 + .5 * np.sin(r * 70 + a * 6)
    f = np.where(r < .35, petals, np.where(r < .62, rings, petals * (.6 + .4 * a)))
    f = f * (1 - smooth(.78, .96, r))
    edge = (np.abs(r - .97) < .015) | (np.abs(r - .99 + .12) < .008)
    c.paint(np.clip(f, 0, 1), pal, method=method)
    c.rgb[edge] = pal.rgb[-1]


@scene('shard-field', 'Shard field', 'Modern', 160, 200,
       [('bone', 'bayer4', {}), ('ice', 'floyd', {}), ('lava', 'atkinson', {})])
def shard_field(c, pal, method, **kw):
    rng = np.random.default_rng(31)
    pts = rng.random((46, 2)) * [c.w, c.h]
    tone = rng.random(46)
    yy, xx = c.py, c.px
    d = np.stack([np.hypot(xx - p[0], (yy - p[1]) * 1.15) for p in pts], 0)
    near = d.argmin(0)
    srt = np.sort(d, 0)
    edge = (srt[1] - srt[0]) < 1.1
    light = np.clip(1 - np.hypot(c.X + .3, c.Y + .4) * .7, 0, 1)
    f = tone[near] * .5 + light * .55
    f = np.where(edge, 0, f)
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('contour-hills', 'Contour hills', 'Modern', 160, 200,
       [('moss', 'bayer4', {}), ('bone', 'bayer2', {}), ('sand', 'floyd', {})])
def contour_hills(c, pal, method, **kw):
    e = fbm(c.h, c.w, 41, 5, 3)
    line = np.abs(((e * 16) % 1) * 2 - 1)
    e = smooth(.2, .8, e)
    f = .1 + .4 * e + .5 * (1 - smooth(.0, .3, line))
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('moire-bloom', 'Moire bloom', 'Modern', 180, 180,
       [('bone', 'atkinson', {}), ('signal', 'bayer4', {}), ('acid', 'floyd', {})])
def moire_bloom(c, pal, method, **kw):
    a = np.cos(np.hypot(c.X + .22, c.Y) * 90)
    b = np.cos(np.hypot(c.X - .22, c.Y) * 90)
    f = (a * b * .5 + .5) * smooth(1.2, .3, np.hypot(c.X, c.Y))
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('spiral-galaxy', 'Spiral galaxy', 'Cosmic', 180, 180,
       [('bone', 'blue', {}), ('ember', 'floyd', {}), ('lime', 'bayer8', {})])
def spiral_galaxy(c, pal, method, **kw):
    r = np.hypot(c.X, c.Y * 1.25) + 1e-3
    th = np.arctan2(c.Y * 1.25, c.X)
    arms = .5 + .5 * np.cos(2 * th - 7 * np.log(r) + fbm(c.h, c.w, 9, 4, 6) * 1.6)
    f = (arms ** 1.6) * np.exp(-r * 2.2) * 1.3 + np.exp(-r * 9) * .9
    c.paint(np.clip(f, 0, 1), pal, method=method)
    _stars(c, pal, f > .3, .985)
