import math

import skia

from kit import (AMBER, BLUE, BLUE_BRIGHT, NAVY, WHITE, PINK, clamp, linear,
                 mix, paint, polygon, with_alpha)


def blob_path(cx, by, r, sx, sy, t, wobble=1.0, n=72):
    """A soft blob standing on (cx, by): radius r, scaled by sx/sy, gently breathing."""
    p = skia.Path()
    cy = by - r * sy
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        rr = r * (1 + wobble * (0.022 * math.sin(3 * a + t * 2.6) + 0.016 * math.sin(5 * a - t * 3.1)))
        flat = 1.0 - 0.10 * max(0.0, math.sin(a)) ** 6
        x = cx + rr * math.cos(a) * sx
        y = cy + rr * math.sin(a) * sy * flat
        if i == 0:
            p.moveTo(x, y)
        else:
            p.lineTo(x, y)
    p.close()
    return p


def neby(c, cx, by, r, t, sq=0.0, look=(0.0, 0.0), blink=0.0, wink=0.0,
         smile=1.0, cap=0.0, body=BLUE_BRIGHT, body2=BLUE, alpha=1.0, shadow=True,
         lift=0.0):
    """Neby: the NEBians mascot. (cx, by) is the point where it stands; lift raises it off
    the ground (the shadow stays). sq > 0 squashes, sq < 0 stretches."""
    if alpha <= 0:
        return
    sx, sy = 1 + sq, 1 - sq
    if shadow:
        k = clamp(1 - lift / (r * 3.5), 0.25, 1)
        c.drawOval(skia.Rect.MakeXYWH(cx - r * 0.9 * sx * k, by - r * 0.09, r * 1.8 * sx * k, r * 0.2),
                   paint(with_alpha(NAVY, 0.16 * alpha * k), blur=r * 0.06))
    by = by - lift
    body_path = blob_path(cx, by, r, sx, sy, t)
    top = by - 2 * r * sy
    p = paint(with_alpha(WHITE, alpha))
    p.setShader(linear((cx, top), (cx, by), [with_alpha(mix(body, WHITE, 0.10), alpha), with_alpha(body2, alpha)]))
    c.drawPath(body_path, p)
    c.save()
    c.clipPath(body_path, doAntiAlias=True)
    c.drawOval(skia.Rect.MakeXYWH(cx - r * 0.95 * sx, top + r * 1.25 * sy, r * 2.4 * sx, r * 1.2 * sy),
               paint(with_alpha(NAVY, 0.12 * alpha), blur=r * 0.12))
    c.drawOval(skia.Rect.MakeXYWH(cx - r * 0.62 * sx, top + r * 0.20 * sy, r * 0.62 * sx, r * 0.34 * sy),
               paint(with_alpha(WHITE, 0.30 * alpha), blur=r * 0.08))
    c.restore()

    ey = top + r * 0.86 * sy
    lx, ly = look
    for side in (-1, 1):
        ex = cx + side * r * 0.34 * sx + lx * r * 0.05
        closed = wink if side == 1 else 0.0
        open_k = clamp(1 - max(blink, closed))
        ew, eh = r * 0.25 * sx, r * 0.31 * sy * max(open_k, 0.08)
        if open_k > 0.12:
            c.drawOval(skia.Rect.MakeXYWH(ex - ew / 2, ey - eh / 2, ew, eh), paint(with_alpha(WHITE, alpha)))
            pr = r * 0.085
            px, py = ex + lx * r * 0.06, ey + ly * r * 0.05 * open_k
            c.drawCircle(px, py, pr * min(1, open_k * 1.4), paint(with_alpha(NAVY, alpha)))
            c.drawCircle(px - pr * 0.35, py - pr * 0.4, pr * 0.32, paint(with_alpha(WHITE, alpha)))
        else:
            arc = skia.Path()
            arc.moveTo(ex - ew * 0.55, ey)
            arc.quadTo(ex, ey + r * 0.09 * (1 if side == -1 or closed == 0 else 1), ex + ew * 0.55, ey)
            c.drawPath(arc, paint(with_alpha(WHITE, alpha), stroke=r * 0.055))
    for side in (-1, 1):
        c.drawOval(skia.Rect.MakeXYWH(cx + side * r * 0.58 * sx - r * 0.11, ey + r * 0.22 * sy, r * 0.22, r * 0.11),
                   paint(with_alpha(PINK, 0.55 * alpha), blur=r * 0.02))
    my = ey + r * 0.30 * sy
    m = skia.Path()
    mw = r * 0.20 * sx
    m.moveTo(cx - mw, my)
    m.quadTo(cx, my + r * 0.16 * smile, cx + mw, my)
    c.drawPath(m, paint(with_alpha(NAVY, alpha), stroke=r * 0.06))

    if cap > 0:
        k = clamp(cap)
        drop = (1 - k) * -r * 1.8
        capy = top + r * 0.12 + drop
        tilt = -8 * (1 - k) + 6
        c.save()
        c.rotate(tilt, cx, capy)
        a = alpha * clamp(k * 3)
        board = polygon([(cx - r * 0.78, capy), (cx, capy - r * 0.30), (cx + r * 0.78, capy), (cx, capy + r * 0.30)])
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - r * 0.42, capy, r * 0.84, r * 0.34), r * 0.08, r * 0.08),
                    paint(with_alpha(NAVY, a)))
        c.drawPath(board, paint(with_alpha(mix(NAVY, WHITE, 0.12), a)))
        c.drawCircle(cx, capy, r * 0.06, paint(with_alpha(AMBER, a)))
        tas = skia.Path()
        sway = math.sin(t * 5) * r * 0.05
        tas.moveTo(cx, capy)
        tas.quadTo(cx + r * 0.45, capy + r * 0.02, cx + r * 0.55 + sway, capy + r * 0.42)
        c.drawPath(tas, paint(with_alpha(AMBER, a), stroke=r * 0.045))
        c.drawCircle(cx + r * 0.55 + sway, capy + r * 0.46, r * 0.07, paint(with_alpha(AMBER, a)))
        c.restore()


def blobatar(c, cx, by, r, t, color, alpha=1.0, look=(0, 0), mood=1.0, sq=0.0, seed=0):
    """A classmate: the same blob family as Neby, in another colour."""
    neby(c, cx, by, r, t + seed * 1.7, sq=sq, look=look, smile=mood,
         body=mix(color, WHITE, 0.08), body2=color, alpha=alpha, shadow=True,
         blink=1.0 if (t * 0.9 + seed * 0.37) % 2.3 < 0.08 else 0.0)


LOGO = [
    ([(500, 42), (501, 135), (856, 370), (858, 1287), (943, 1219), (943, 331)], (0xFF07337F, 0xFF021B54)),
    ([(441, 191), (441, 282), (691, 447), (691, 799), (774, 886), (775, 408)], (0xFF06327C, 0xFF04215E)),
    ([(306, 320), (307, 377), (613, 706), (613, 485)], (0xFFA8C5FF, 0xFF82A8F5)),
    ([(51, 228), (51, 1132), (263, 1346), (267, 812), (775, 1353), (775, 887), (691, 800), (685, 902)], (0xFF0058DF, 0xFF003CC3)),
]
LOGO_BOX = (34, 26, 920, 1344)


def logo(c, cx, cy, h, progress, t, on_blue=False):
    """The real NEBians N (five facets of n-logo-tight-no-outline.svg) assembling facet by facet."""
    bx, by, bw, bh = LOGO_BOX
    s = h / bh
    for i, (pts, (c1, c2)) in enumerate(LOGO):
        k = clamp((progress - i * 0.12) / 0.55)
        if k <= 0:
            continue
        from kit import ease_out_back
        e = ease_out_back(k, 1.4)
        ox = (1 - e) * (-260 if i % 2 else 260)
        oy = (1 - e) * (-180 + 120 * i)
        rot = (1 - e) * (24 if i % 2 else -24)
        P = [(cx + (x - bx - bw / 2) * s + ox, cy + (y - by - bh / 2) * s + oy) for x, y in pts]
        path = polygon(P)
        c.save()
        c.rotate(rot, cx + ox, cy + oy)
        p = paint(with_alpha(WHITE, clamp(k * 2.5)))
        if on_blue and i == 3:
            c1, c2 = 0xFFFFFFFF, 0xFFDCE6FF
        if on_blue and i in (0, 1):
            c1, c2 = mix(c1, 0xFF0A2A7A, 0.2), c2
        ys = [q[1] for q in P]
        p.setShader(linear((P[0][0], min(ys)), (P[0][0], max(ys)), [with_alpha(c1, clamp(k * 2.5)), with_alpha(c2, clamp(k * 2.5))]))
        c.drawPath(path, p)
        c.restore()
