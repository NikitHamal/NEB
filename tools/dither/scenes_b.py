"""Ancient scenes: pyramids, ziggurats, eyes, columns, waves, tablets, a marble bust."""
import numpy as np
from engine import smooth, fbm, rot, sd_sphere, sd_box, smin, march
from kit import scene


def _stars(c, pal, mask, density=.992, seed=12):
    s = (np.random.default_rng(seed).random((c.h, c.w)) > density) & ~mask
    c.rgb[s] = pal.rgb[-1]


@scene('three-pyramids', 'Three pyramids', 'Ancient', 240, 150,
       [('sand', 'bayer8', {}), ('amber', 'floyd', {}), ('ember', 'atkinson', {}), ('bone', 'blue', {})])
def three_pyramids(c, pal, method, **kw):
    X, Y = c.X, c.Y
    hz = .38
    sky = .35 + .6 * smooth(hz, -1, Y)
    sun = np.hypot(X - .55, Y + .3) < .2
    f = np.where(sun, 1.0, sky * .9)
    dunes = fbm(c.h, c.w, 5, 3, 3)
    ground = .32 + .22 * dunes + .1 * np.sin(Y * 40 + dunes * 6)
    f = np.where(Y > hz, ground * (.7 + .3 * smooth(hz, 1, Y)), f)
    for ax, ay, b in ((-.2, -.42, .62), (-.82, -.05, .4), (.42, .12, .26)):
        base = hz + (.06 if ax == .42 else 0)
        tri = (Y > ay) & (Y < base) & (np.abs(X - ax) < (Y - ay) * b / (base - ay))
        lit = X < ax
        tex = .06 * np.sin(Y * 80)
        f = np.where(tri & lit, .86 + tex, f)
        f = np.where(tri & ~lit, .16 + tex, f)
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('ziggurat-night', 'Ziggurat at night', 'Ancient', 160, 200,
       [('gold', 'bayer8', {}), ('bone', 'floyd', {}), ('terracotta', 'atkinson', {}), ('jade', 'bayer4', {})])
def ziggurat(c, pal, method, **kw):
    X, Y = c.X, c.Y
    hz = .62
    moon = np.hypot(X + .3, Y + .55)
    f = .08 + .18 * smooth(hz, -1, Y) + np.where(moon < .2, .95, 0) + np.exp(-np.maximum(moon - .2, 0) * 6) * .35
    f = np.where(Y > hz, .12 + .1 * fbm(c.h, c.w, 3, 3, 4), f)
    tiers = [(.75, -.05, .15), (.58, .15, .35), (.42, .35, .55), (.27, .55, .62)]
    for hw, y0, y1 in tiers:
        box = (np.abs(X) < hw * .62) & (Y > y0 - .2) & (Y < y1 + .0)
        top = box & (Y < y0 - .2 + .045)
        face = box & ~top
        f = np.where(face & (X < 0), .6 + .08 * np.sin(Y * 90), f)
        f = np.where(face & (X >= 0), .22, f)
        f = np.where(top, .85, f)
    stair = (np.abs(X) < .07) & (Y > -.25) & (Y < .62)
    f = np.where(stair, .35 + .5 * (np.sin(Y * 140) > 0), f)
    c.paint(np.clip(f, 0, 1), pal, method=method)
    _stars(c, pal, (moon < .35) | (Y > hz - .1), .99)


@scene('seeing-eye', 'Seeing eye', 'Ancient', 220, 140,
       [('gold', 'radial', {'cell': 3.2}), ('bone', 'bayer4', {}), ('ember', 'floyd', {}), ('jade', 'atkinson', {})])
def seeing_eye(c, pal, method, **kw):
    X, Y = c.X * .95, c.Y * .95 + .0
    lid = .34 * np.clip(1 - (X / .95) ** 2, 0, 1) ** .8
    almond = (np.abs(Y) < lid) & (np.abs(X) < .95)
    r = np.hypot(X, Y)
    iris = r < .3
    rings = .55 + .35 * np.sin(r * 90) * (r > .1)
    f = np.where(almond, .92, .26 + .1 * np.sin(Y * 38))
    f = np.where(almond & iris, rings * (.5 + .5 * smooth(.3, .1, r) * 0 + .5), f)
    f = np.where(r < .11, .02, f)
    f = np.where(np.hypot(X + .07, Y + .08) < .035, 1, f)
    brow = np.abs(Y + .5 + .22 * (X / .95) ** 2 - .0) < .045
    f = np.where(brow & (np.abs(X) < 1.0), .02, f)
    outline = (np.abs(np.abs(Y) - lid) < .018) & (np.abs(X) < .95)
    f = np.where(outline, .02, f)
    drop = (np.abs(X - .08) < .035) & (Y > lid * .8) & (Y < .62)
    f = np.where(drop, .02, f)
    spiral = np.abs(np.hypot(X - .22, Y - .6) - .12 - .06 * np.arctan2(Y - .6, X - .22) / np.pi) < .02
    f = np.where(spiral & (X > .08), .02, f)
    c.paint(np.clip(f, 0, 1), pal, method=method, cell=3.2)


@scene('fluted-column', 'Fluted column', 'Ancient', 160, 200,
       [('sand', 'bayer8', {}), ('bone', 'floyd', {}), ('terracotta', 'atkinson', {}), ('jade', 'blue', {})])
def fluted_column(c, pal, method, **kw):
    X, Y = c.X, c.Y
    clouds = fbm(c.h, c.w, 7, 5, 3)
    f = .42 + .45 * smooth(.2, .8, clouds) * (1 - .4 * smooth(-1, .6, Y))
    f = np.where(Y > .6, .2 + .3 * (np.sin(X * 40 + Y * 20) > 0) * .4 + .1 * fbm(c.h, c.w, 2, 3, 4), f)
    step = (Y > .52) & (Y < .66) & (np.abs(X) < .55)
    f = np.where(step, .72 - .15 * (Y > .59), f)
    u = np.clip(X / .26, -1, 1)
    shaft = (np.abs(X) < .26 * (1 - .05 * (Y + .5))) & (Y > -.5) & (Y < .5)
    lam = np.clip(-u * .55 + np.sqrt(1 - u * u) * .8, 0, 1)
    flutes = .78 + .22 * np.cos(X * 120)
    f = np.where(shaft, np.clip(lam * flutes + .05, 0, 1), f)
    cap = (np.abs(X) < .36) & (Y > -.62) & (Y < -.5)
    echinus = (np.abs(X) < .3) & (Y >= -.5) & (Y < -.46)
    f = np.where(cap | echinus, .8 - .3 * (X > .1), f)
    base = (np.abs(X) < .34) & (Y > .46) & (Y < .54)
    f = np.where(base, .75 - .3 * (X > .1), f)
    brk = (X < -.58) & (X > -.9) & (Y > -.05 - .12 * np.sin(X * 33)) & (Y < .55)
    u2 = np.clip((X + .74) / .16, -1, 1)
    f = np.where(brk, np.clip((-u2 * .55 + np.sqrt(1 - u2 ** 2) * .8) * (.8 + .2 * np.cos(X * 120)), 0, 1), f)
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('sun-disc', 'Sun disc', 'Ancient', 180, 180,
       [('gold', 'spiral', {'cell': 3.4, 'freq': 1.0}), ('ember', 'bayer8', {}), ('bone', 'radial', {'cell': 3.0}), ('lava', 'floyd', {})])
def sun_disc(c, pal, method, **kw):
    r = np.hypot(c.X, c.Y) + 1e-4
    th = np.arctan2(c.Y, c.X)
    straight = (np.sin(th * 24) > 0)
    wavy = np.sin(th * 12 + r * 26) > .1
    rays = np.where(np.sin(th * 12) > 0, straight, wavy).astype(float)
    f = np.exp(-np.maximum(r - .3, 0) * 2.4) * (.35 + .65 * rays)
    f = np.where(r < .3, .55 + .45 * np.cos(r * 40) ** 2, f)
    f = np.where((np.abs(r - .31) < .012) | (np.abs(r - .4) < .008), 1, f)
    f = np.where(r > .96, 0, f)
    c.paint(np.clip(f, 0, 1), pal, method=method, cell=kw.get('cell', 3.4), freq=kw.get('freq', 1.0))


@scene('seigaiha', 'Seigaiha waves', 'Ancient', 200, 200,
       [('jade', 'bayer4', {}), ('bone', 'floyd', {}), ('ink-red', 'bayer8', {}), ('amber', 'atkinson', {})])
def seigaiha(c, pal, method, **kw):
    R = 21.0
    f = np.zeros((c.h, c.w))
    grad = .3 + .55 * (c.Y * .5 + .5)
    j = 0
    y = -R
    while y < c.h + R:
        x = -R + (R if j % 2 else 0)
        while x < c.w + R:
            d = np.hypot(c.px - x, c.py - y) / R
            ring = np.floor(d * 5)
            val = np.where(ring % 2 == 0, .9, .35)
            val = np.where(ring >= 4, .15, val)
            m = d < 1
            f = np.where(m, val * grad, f)
            x += 2 * R
        y += R / 2
        j += 1
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('square-labyrinth', 'Square labyrinth', 'Ancient', 180, 180,
       [('bone', 'bayer4', {}), ('terracotta', 'floyd', {}), ('gold', 'atkinson', {})])
def labyrinth(c, pal, method, **kw):
    d = np.maximum(np.abs(c.X), np.abs(c.Y))
    th = np.arctan2(c.Y, c.X) / (2 * np.pi)
    path = (d * 9 + th) % 1
    wall = (path < .5).astype(float)
    light = np.clip(1 - np.hypot(c.X + .35, c.Y + .4) * .8, .15, 1)
    f = (.1 + .8 * wall) * light
    f = np.where(d > .97, 0, f)
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('great-wave', 'Great wave', 'Ancient', 240, 150,
       [('jade', 'bayer8', {}), ('bone', 'floyd', {}), ('ink-red', 'atkinson', {}), ('ice', 'blue', {})])
def great_wave(c, pal, method, **kw):
    X, Y = c.X, c.Y
    sky = .62 + .3 * smooth(.3, -1, Y)
    f = np.where(np.hypot(X + .95, Y + .55) < .17, 1.0, sky)
    fuji = (Y > -.12 + np.abs(X + .5) * .7) & (Y < .4) & (X > -1.1) & (X < .1)
    f = np.where(fuji, .3 + .4 * (Y < -.0), f)
    sea = Y > .3 + .04 * np.sin(X * 9)
    f = np.where(sea, .26 + .18 * (.5 + .5 * np.sin(Y * 70 + X * 8)), f)
    outer = np.hypot(X - .1, Y - .12) < .78
    inner = np.hypot(X - .36, Y - .26) < .52
    cres = outer & ~inner & (X < .1 + .6 * (Y < .1) + .8)
    d = np.hypot(X - .36, Y - .26) - .52
    body = .22 + .38 * smooth(0, .26, d)
    foam = fbm(c.h, c.w, 17, 5, 8)
    f = np.where(cres, body, f)
    f = np.where(cres & (d > .1) & (foam > .6) & (Y < .0), 1.0, f)
    tip = cres & (d < .05) & (Y < .0)
    f = np.where(tip, .96, f)
    f = np.where(outer & ~inner & (Y > .3), .24 + .15 * np.sin(Y * 70), f)
    spray = (np.random.default_rng(3).random((c.h, c.w)) > .975) & (np.hypot(X - .45, Y + .15) < .5) & ~outer
    f = np.where(spray, 1.0, f)
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('torii-tide', 'Torii at tide', 'Ancient', 160, 200,
       [('lava', 'bayer8', {}), ('ember', 'floyd', {}), ('bone', 'atkinson', {}), ('gold', 'bayer4', {})])
def torii(c, pal, method, **kw):
    X, Y = c.X, c.Y
    hz = .38
    sun = np.hypot(X, Y + .12)
    f = .3 + .35 * smooth(hz, -1, Y)
    f = np.where(sun < .55, .95 - .05 * (np.sin(Y * 38) > .55) * (Y > -.12) * 8 * (Y + .12), f)
    sea = Y > hz
    refl = .25 + .4 * (np.abs(X) < .5) * (.5 + .5 * np.sin(Y * 90 + fbm(c.h, c.w, 1, 3, 5) * 8))
    f = np.where(sea, refl * (1 - .3 * smooth(hz, 1, Y)), f)
    sil = 0.0
    pil = ((np.abs(np.abs(X) - .36) < .035) & (Y > -.38) & (Y < .55 + 0 * Y))
    kas = (np.abs(X) < .72) & (Y > -.52 - .1 * (X / .72) ** 2 * 1.2) & (Y < -.42 - .05 * (X / .72) ** 2)
    nuki = (np.abs(X) < .43) & (Y > -.27) & (Y < -.21)
    mid = (np.abs(X) < .05) & (Y > -.42) & (Y < -.27)
    mask = pil | kas | nuki | mid
    f = np.where(mask, sil, f)
    refl_mask = (Y > hz) & ((np.abs(np.abs(X) - .36) < .035) & (np.sin(Y * 60) > -.2)) 
    f = np.where(refl_mask, .06, f)
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('desert-gate', 'Desert gate', 'Ancient', 160, 200,
       [('sand', 'bayer4', {}), ('gold', 'floyd', {}), ('bone', 'atkinson', {}), ('terracotta', 'bayer8', {})])
def desert_gate(c, pal, method, **kw):
    X, Y = c.X, c.Y
    sx, sy = .18, -.22
    ang = np.arctan2(Y - sy, X - sx)
    rays = .5 + .5 * np.sin(ang * 34 + fbm(c.h, c.w, 4, 3, 4) * 5)
    dist = np.hypot(X - sx, Y - sy)
    brick_row = np.floor((Y + 1) * 9)
    bx = ((X + 1.5) * 7 + (brick_row % 2) * .5) % 1
    by = ((Y + 1) * 9) % 1
    mortar = (bx < .06) | (by < .08)
    stone = .38 + .2 * fbm(c.h, c.w, 6, 4, 8) - .22 * mortar
    stone = stone * (.55 + .45 * smooth(.2, 1.3, dist) * 0 + .45) + .2 * rays * np.exp(-dist * 1.1)
    opening = (np.abs(X) < .42) & (Y > -.1) | (np.hypot(X, Y + .1) < .42)
    sunc = np.hypot(X - sx, Y - sy)
    outside = .5 + .45 * smooth(.45, -.9, Y) + np.where(sunc < .09, 1, 0) + np.exp(-sunc * 6) * .4
    dunes = (Y > .3 + .08 * np.sin(X * 6 + 1)) 
    outside = np.where(dunes, .35 + .25 * fbm(c.h, c.w, 8, 3, 5), outside)
    f = np.where(opening, outside, stone)
    beam = (Y > .62) & (np.abs(X - .05 * (Y - .62) * 4) < .3 + (Y - .62) * .45)
    f = np.where(beam & ~opening, f + .0, f)
    floor = (Y > .62)
    f = np.where(floor & (np.abs(X - (Y - .62) * .35) < .3 + (Y - .62) * .5), .85 - .2 * (Y - .62), np.where(floor, .18, f))
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('obelisk-dusk', 'Obelisk at dusk', 'Ancient', 160, 200,
       [('amber', 'bayer8', {}), ('bone', 'floyd', {}), ('ember', 'atkinson', {}), ('sand', 'blue', {})])
def obelisk(c, pal, method, **kw):
    def sdf(p):
        q = rot(p, 1, .6)
        k = 1 - (q[..., 1] + 1.0) * .045
        qq = q.copy()
        qq[..., 0] /= k
        qq[..., 2] /= k
        body = np.maximum(sd_box(qq, (.22, 1.05, .22)), -1e9)
        body = np.maximum(body, q[..., 1] - 1.0) * .8
        m = np.maximum(np.abs(q[..., 0]), np.abs(q[..., 2]))
        cap = np.maximum((m - .16 * (1.45 - q[..., 1]) / .45) * .6, 1.0 - q[..., 1])
        cap = np.maximum(cap, q[..., 1] - 1.45)
        return np.minimum(np.minimum(body, cap), p[..., 1] + 1.05)
    hit, sh, t, n = march(sdf, c.w, c.h, cam=(0, -.3, -4.0), fov=.46, steps=120, far=40, light=(-.8, .35, -.4))
    fog = smooth(5, 26, t)
    sunr = np.hypot(c.X + .0, c.Y - .38)
    sky = .35 + .5 * smooth(-.3, .6, -c.Y) + np.where(sunr < .16, 1, 0) + np.exp(-sunr * 3) * .4
    f = np.where(hit, np.clip(sh * (1 - fog) + fog * .45, 0, 1), sky * (c.Y < .45) + .22 * (c.Y >= .45))
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('clay-tablet', 'Clay tablet', 'Ancient', 220, 150,
       [('clay', 'bayer4', {}), ('sand', 'floyd', {}), ('terracotta', 'atkinson', {}), ('bone', 'bayer8', {})])
def clay_tablet(c, pal, method, **kw):
    X, Y = c.X, c.Y
    q = np.stack([np.abs(X) - 1.08, np.abs(Y) - .7], -1)
    d = np.hypot(np.maximum(q[..., 0], 0), np.maximum(q[..., 1], 0)) + np.minimum(np.maximum(q[..., 0], q[..., 1]), 0) - .12
    gy, gx = np.gradient(d)
    lam = np.clip(-(gx + gy) * 14, -1, 1)
    f = .45 + .25 * fbm(c.h, c.w, 14, 4, 6)
    edge = smooth(0, -.14, d)
    f = f + .3 * lam * (1 - edge)
    cw, ch = 7, 12
    i = (c.px // cw).astype(int)
    j = (c.py // ch).astype(int)
    rid = np.random.default_rng(5).integers(0, 7, (c.h // ch + 2, c.w // cw + 2))
    pid = rid[j, i]
    u = (c.px % cw) / cw
    v = (c.py % ch) / ch
    groove = np.zeros_like(f, dtype=bool)
    groove |= (pid == 0) & (np.abs(v - .5) < .14) & (u > .1) & (u < .9)
    groove |= (pid == 1) & (np.abs(u - .5) < .16) & (v > .15) & (v < .9)
    groove |= (pid == 2) & (np.abs(u - v) < .16)
    groove |= (pid == 3) & ((np.abs(v - .28) < .1) | (np.abs(v - .72) < .1)) & (u > .1) & (u < .9)
    groove |= (pid == 4) & (np.abs(np.abs(u - .5) * 1.5 - (v - .2)) < .14)
    area = (np.abs(X) < .95) & (np.abs(Y) < .56) & (d < -.1)
    f = np.where(groove & area, f * .42, f)
    rule = (np.abs(((c.py) % ch) - 0) < 1) & area
    f = np.where(rule, f * .7, f)
    f = np.where(d > 0, .06, f)
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('lotus-top', 'Lotus from above', 'Ancient', 160, 200,
       [('rose', 'bayer8', {}), ('gold', 'floyd', {}), ('bone', 'atkinson', {}), ('ice', 'bayer4', {})])
def lotus(c, pal, method, **kw):
    X, Y = c.X, c.Y + .0
    r = np.hypot(X, Y) + 1e-4
    th = np.arctan2(Y, X)
    f = .08 + .12 * (.5 + .5 * np.cos(r * 42)) * smooth(1.2, .2, r)
    layers = [(.9, 8, 0), (.68, 8, np.pi / 8), (.46, 8, 0), (.26, 6, np.pi / 6)]
    for n, (R, k, off) in enumerate(layers):
        rmax = R * np.abs(np.cos(k * (th + off) / 2)) ** .75 + .05
        m = r < rmax
        shade = .35 + .5 * (n / 3.0) + .15 * (r / rmax)
        vein = .06 * np.sin((th + off) * k * 3)
        f = np.where(m, shade + vein, f)
        edge = m & (r > rmax - .012)
        f = np.where(edge, .02, f)
    seed = r < .1
    f = np.where(seed, .95 - .3 * (np.sin(X * 90) * np.sin(Y * 90) > .2), f)
    c.paint(np.clip(f, 0, 1), pal, method=method)


@scene('marble-bust', 'Marble bust', 'Ancient', 160, 200,
       [('bone', 'floyd', {}), ('sand', 'bayer8', {}), ('lava', 'atkinson', {'glitch': True}), ('jade', 'blue', {})])
def marble_bust(c, pal, method, **kw):
    def sdf(p):
        q = rot(p, 1, .55) - np.array([0, .12, 0])
        head = sd_sphere(q / np.array([1, 1.22, 1.0]), .6) * .78
        nose = sd_sphere((q - np.array([0, -.02, -.6])) / np.array([.075, .24, .11]), 1.0) * .07
        head = smin(head, nose, .1)
        brow = sd_sphere((q - np.array([0, .2, -.5])) / np.array([.42, .06, .16]), 1.0) * .06
        head = smin(head, brow, .1)
        lips = sd_sphere((q - np.array([0, -.3, -.55])) / np.array([.15, .03, .06]), 1.0) * .03
        head = smin(head, lips, .05)
        chin = sd_sphere(q - np.array([0, -.58, -.34]), .2)
        head = smin(head, chin, .14)
        for sx in (-.22, .22):
            eye = sd_sphere(q - np.array([sx, .1, -.58]), .09)
            head = np.maximum(head, -eye + .02)
        neck = np.maximum(np.hypot(q[..., 0], q[..., 2]) - .24, np.abs(q[..., 1] + .95) - .4) * .8
        sh = sd_box(p - np.array([0, -1.15, 0]), (.9, .1, .36)) - .1
        return smin(smin(head, neck, .2), sh, .22)
    hit, sh, t, n = march(sdf, c.w, c.h, cam=(0, -.2, -3.4), fov=.52, steps=110, light=(-.7, .5, -.6), gamma=1.1)
    bgf = .22 * np.clip(1 - np.hypot(c.X * .8, c.Y + .1), 0, 1) + .06
    c.paint(np.where(hit, sh, bgf), pal, method=method)
    if kw.get('glitch'):
        c.glitch(n=9, maxshift=18, zone=(.1, .8), seed=4)
