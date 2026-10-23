"""The riso look: monumental soft shapes lit in stipple, glows, paper grain."""
import math

from kit import RISO as P, Rng, Svg, blob, f, ridge, smooth, star_path


def sky(s, top=P["sky0"], mid=P["sky2"], low=P["sky3"], ground=None):
    s.rect(0, 0, s.w, s.h, s.lin([(0, top), (0.55, mid), (1, low)]))


def lit(s, d, base, light, shade=None, lx=0.5, ly=0.0, reach=0.65, sx=0.5, sy=1.0, sreach=0.7, scale=1.0):
    """One shape in three passes: the base colour, a light that falls off in stipple from (lx, ly),
    and a shade rising in stipple from (sx, sy), all clipped to the shape (object-bbox units)."""
    s.path(d, base)
    cid = s.clip(d)
    st = s.stipple(scale)
    s.group(lambda: s.path(d, s.rad([(0, light), (0.45, light, 0.85), (1, light, 0)], lx, ly, reach)), filt=st, clip=cid)
    if shade:
        s.group(lambda: s.path(d, s.rad([(0, shade), (0.5, shade, 0.7), (1, shade, 0)], sx, sy, sreach)), filt=st, clip=cid)


def glow(s, cx, cy, r, color=P["lemon"], strength=1.0):
    """A stippled halo: dense near the centre, dissolving outward."""
    s.group(lambda: s.circle(cx, cy, r, s.rad([(0, color, min(1, strength)), (0.35, color, 0.75 * strength), (1, color, 0)])),
            filt=s.stipple(1.0))


def face(s, cx, cy, size, ink=P["ink"], mood="smile"):
    """The tiny face of the references: two dot eyes and a small curve."""
    e = size * 0.18
    s.circle(cx - size * 0.28, cy - size * 0.05, e, ink)
    s.circle(cx + size * 0.28, cy - size * 0.05, e, ink)
    if mood == "smile":
        s.path("M%s %sQ%s %s %s %s" % (f(cx - size * 0.22), f(cy + size * 0.2), f(cx), f(cy + size * 0.42), f(cx + size * 0.22), f(cy + size * 0.2)),
               stroke=ink, sw=size * 0.1)
    elif mood == "calm":
        s.path("M%s %sL%s %s" % (f(cx - size * 0.15), f(cy + size * 0.28), f(cx + size * 0.15), f(cy + size * 0.28)), stroke=ink, sw=size * 0.09)


def mountains(s, base, rng, color, peaks, light=P["peach"], snow=True):
    d = ridge(-20, s.w + 20, base, peaks, rng)
    lit(s, d, color, light, None, lx=0.75, ly=0.0, reach=0.55, scale=1.2)
    if snow:
        for px, ph, pw in peaks:
            if ph > (base * 0.22):
                cap = "M%s %s" % (f(px - pw * 0.18), f(base - ph * 0.8))
                cap += "L%s %sL%s %sQ%s %s %s %sZ" % (f(px), f(base - ph), f(px + pw * 0.2), f(base - ph * 0.78),
                                                     f(px), f(base - ph * 0.72), f(px - pw * 0.18), f(base - ph * 0.8))
                s.path(cap, P["cream"], op=0.85)


def stars(s, rng, n, ymax, color=P["cream"]):
    for k in range(n):
        x, y, r = rng.u(0, s.w), rng.u(0, ymax), rng.u(0.8, 2.2)
        if rng.u() < 0.12:
            s.path(star_path(x, y, r * 3, r * 0.7), color, op=0.9)
        else:
            s.circle(x, y, r, color, op=rng.u(0.4, 0.9))


def figure(s, x, ground, size, rng, body=P["peri"], light=P["lemon"], shade=P["plum"], head_light=True, lean=0.0, mood="smile", arm=True):
    """The monumental rounded figure: a huge cloak-like body that spreads to the ground, sloped
    shoulders, a small round head lit from within, and one soft arm resting forward."""
    w, h = size, size * 1.05
    top = ground - h
    d = ("M%s %s" % (f(x - w * 0.78), f(ground)) +
         "C%s %s %s %s %s %s" % (f(x - w * 0.70), f(top + h * 0.55), f(x - w * 0.42 + lean), f(top + h * 0.05), f(x + lean * 0.6), f(top + h * 0.02)) +
         "C%s %s %s %s %s %s" % (f(x + w * 0.36 + lean), f(top), f(x + w * 0.62), f(top + h * 0.42), f(x + w * 0.70), f(top + h * 0.78)) +
         "C%s %s %s %s %s %s" % (f(x + w * 0.74), f(top + h * 0.9), f(x + w * 0.70), f(ground - h * 0.02), f(x + w * 0.66), f(ground)) + "Z")
    lit(s, d, body, light, shade, lx=0.48, ly=0.0, reach=0.55, sx=0.12, sy=0.95, sreach=0.8)
    if arm:
        ad = ("M%s %s" % (f(x - w * 0.05), f(top + h * 0.38)) +
              "C%s %s %s %s %s %s" % (f(x + w * 0.25), f(top + h * 0.42), f(x + w * 0.52), f(top + h * 0.62), f(x + w * 0.5), f(top + h * 0.8)) +
              "C%s %s %s %s %s %s" % (f(x + w * 0.38), f(top + h * 0.86), f(x + w * 0.12), f(top + h * 0.7), f(x - w * 0.05), f(top + h * 0.56)) + "Z")
        s.path(ad, P["periD"], op=0.55, filt=s.stipple(0.8))
    hr = size * 0.12
    hx, hy = x + lean * 0.6, top - hr * 0.5
    if head_light:
        glow(s, hx, hy, hr * 3.6, light, 0.85)
    s.circle(hx, hy, hr, light)
    face(s, hx, hy + hr * 0.1, hr, mood=mood)
    return hx, hy, hr


def ground_hills(s, rng, y, colors, light=P["peach"]):
    """Rolling foreground hills, back to front, each a little darker and lit along its crest."""
    from kit import hill
    for k, c in enumerate(colors):
        d = hill(-40, s.w + 40, s.h + 10, y + k * (s.h - y) * 0.28, rng, n=5)
        lit(s, d, c, light, None, lx=0.6, ly=0.0, reach=0.45, scale=1.1)


def book(s, cx, cy, w, color=P["cream"], cover=P["rose"], glowing=True):
    if glowing:
        glow(s, cx, cy - w * 0.1, w * 0.75, P["lemon"], 0.9)
    h = w * 0.28
    s.path("M%s %sQ%s %s %s %sL%s %sQ%s %s %s %sZ" % (f(cx - w / 2), f(cy), f(cx - w / 4), f(cy - h), f(cx), f(cy - h * 0.2),
                                                   f(cx), f(cy + h * 0.25), f(cx - w / 4), f(cy - h * 0.6), f(cx - w / 2), f(cy + h * 0.4)), color)
    s.path("M%s %sQ%s %s %s %sL%s %sQ%s %s %s %sZ" % (f(cx + w / 2), f(cy), f(cx + w / 4), f(cy - h), f(cx), f(cy - h * 0.2),
                                                   f(cx), f(cy + h * 0.25), f(cx + w / 4), f(cy - h * 0.6), f(cx + w / 2), f(cy + h * 0.4)), "#fff6e2")
    s.path("M%s %sQ%s %s %s %s" % (f(cx - w / 2), f(cy + h * 0.4), f(cx), f(cy + h * 0.1), f(cx + w / 2), f(cy + h * 0.4)), stroke=cover, sw=w * 0.04)
