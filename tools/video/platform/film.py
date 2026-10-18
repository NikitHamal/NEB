"""NEBians platform launch film (22 s). Every frame is a pure function of t (seconds)."""
import importlib.util
import math
import os
import sys

import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "neby"))
from characters import logo  # noqa: E402
from kit import (AMBER, BLUE, BLUE_BRIGHT, BLUE_WASH, CORAL, CX, H, INK, MINT, MUTED, NAVY,  # noqa: E402
                 PURPLE, VERT, TEAL, W, WHITE, clamp, ease_in_cubic, ease_in_out, ease_out_back,
                 ease_out_cubic, ease_out_expo, font, lerp, linear, mix, paint, partial_path,
                 polygon, rrect, seg, shadow_rrect, text, with_alpha)
from rig import NebyRig, Performance  # noqa: E402

sys.path.insert(1, os.path.join(HERE, "..", "nebians-launch"))
_spec = importlib.util.spec_from_file_location("dashain_film", os.path.join(HERE, "..", "nebians-launch", "film.py"))
_d = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_d)
rise_text, chip, star, pop_scale = _d.rise_text, _d.chip, _d.star, _d.pop_scale

DURATION = 22.0
FPS = 60
BPM = 120
PURPLE_WASH = 0xFFEBE7FF
AMBER_INK, AMBER_WASH = 0xFFB84B0B, 0xFFFFEFCF
BG = 0xFFF5F8FF

CUES = [
    (0.00, "slam"), (0.50, "slam"), (1.00, "slam"), (1.50, "slam"), (2.00, "implode"), (2.25, "pop"),
    (2.55, "whoosh"), (2.95, "facet"), (3.07, "facet"), (3.19, "facet"), (3.31, "facet"), (3.55, "word"), (3.95, "chip"),
    (4.85, "whoosh"), (5.05, "word"), (5.35, "chip"), (5.60, "type"), (6.20, "type"),
    (6.55, "tick"), (6.67, "tick"), (6.79, "tick"), (6.91, "tick"), (7.03, "tick"), (7.15, "tick"),
    (7.30, "pop"), (7.42, "pop"), (7.54, "pop"), (7.66, "pop"), (7.78, "pop"), (7.90, "pop"),
    (8.85, "whoosh"), (9.05, "word"), (9.35, "chip"), (9.60, "bubble"), (10.15, "bubble"), (10.70, "bubble"),
    (10.40, "like"), (10.55, "like"), (10.70, "like"), (11.20, "pop"), (11.35, "write"),
    (12.35, "whoosh"), (12.55, "word"), (12.80, "drop"), (13.10, "upload"), (13.75, "badge"), (13.85, "sparkle"),
    (14.30, "swap"), (14.55, "swap"),
    (15.35, "whoosh"), (15.55, "word"), (15.80, "pop"), (16.05, "pop"), (16.30, "pop"), (16.70, "tap"), (17.00, "sheet"),
    (17.40, "riser"), (18.00, "boom"), (18.05, "confetti"), (18.40, "facet"), (18.52, "facet"), (18.64, "facet"),
    (18.76, "facet"), (19.05, "word"), (19.55, "chip"), (19.85, "chip"), (20.20, "word"), (20.60, "wink"), (21.0, "bells"),
]

RIG = None
PERF = Performance(
    keys=[(0.0, "intro-neby-closed", 0, "smooth"), (2.25, "intro-neby-peek", 0.25, "spring"),
          (2.60, "intro-neby-focus", 0.35, "spring"), (3.20, "joy", 0.35, "spring"), (4.20, "soft-smile", 0.5, "smooth"),
          (5.10, "focus", 0.4, "smooth"), (5.70, "scan-left", 0.5, "smooth"), (6.60, "scan-right", 0.6, "smooth"),
          (7.40, "delight", 0.35, "spring"), (8.20, "soft-smile", 0.5, "smooth"),
          (9.10, "anticipation", 0.3, "spring"), (9.70, "joy", 0.35, "spring"), (10.70, "delight", 0.4, "smooth"),
          (11.40, "joy", 0.4, "smooth"),
          (12.60, "focus", 0.35, "smooth"), (13.75, "cheer", 0.25, "spring"), (14.40, "smug", 0.4, "smooth"),
          (15.60, "soft-smile", 0.4, "smooth"), (16.70, "talk-a", 0.3, "smooth"), (17.10, "talk-b", 0.3, "smooth"),
          (18.05, "cheer", 0.25, "spring"), (18.80, "success", 0.4, "spring"), (19.60, "joy", 0.4, "smooth"),
          (20.60, "wink", 0.28, "spring"), (21.20, "soft-smile", 0.5, "smooth")],
    blinks=[3.9, 5.4, 8.0, 10.2, 12.2, 14.9, 16.4, 19.2, 21.6],
    looks=[(0.0, 0, 0, 0.1), (3.0, 0.6, -0.1, 0.5), (5.1, 0.5, -0.4, 0.5), (9.1, 0.7, -0.1, 0.4),
           (12.6, 0.6, 0.0, 0.4), (15.6, 0.6, -0.2, 0.4), (18.05, 0.0, -0.1, 0.4), (19.2, 0.5, 0.0, 0.6)])


def neby(c, t, x, y, size, rot=0.0, sx=1.0, sy=1.0, shadow=True, alpha=1.0):
    global RIG
    if RIG is None:
        RIG = NebyRig()
    RIG.draw(c, PERF, t, x, y, size, rot=rot, sx=sx, sy=sy, shadow=shadow, alpha=alpha)


def background(c, t):
    c.clear(BG)
    p = paint(WHITE)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(W * 0.55, H * 0.35), W * 0.8,
                                                [0xFFFFFFFF, 0xFFF1F5FF, 0xFFE4ECFF], [0, 0.55, 1]))
    c.drawPaint(p)
    for i, (x, y, r, col) in enumerate([(260, 180, 260, 0xFFDFF3FF), (1700, 880, 320, 0xFFEBE7FF), (1640, 120, 200, 0xFFFFEFCF)]):
        dx = math.sin(t * 0.35 + i * 2) * 40
        dy = math.cos(t * 0.3 + i) * 30
        c.drawCircle(x + dx, y + dy, r, paint(with_alpha(col, 0.75), blur=80))
    dot = paint(with_alpha(BLUE, 0.06))
    for gx in range(0, W + 1, 64):
        for gy in range(0, H + 1, 64):
            c.drawCircle(gx + (t * 6) % 64, gy, 2.0, dot)


def scene_label(c, lead, chip_text, fg, bg, t0, t, out=0.0):
    """'Study [materials.]' — one line in landscape; in portrait the chip drops to line two."""
    size = 104 if not VERT else 116
    f = font("ExtraBold", size)
    c.save()
    c.translate(0, -out * 400)
    if not VERT:
        w = rise_text(c, lead, 110, 170, f, INK, t0, t)
        chip(c, chip_text, 110 + w + 26, 170, size, t0 + 0.30, t, fg=fg, bg=bg)
    else:
        rise_text(c, lead, 80, 290, f, INK, t0, t)
        chip(c, chip_text, 80, 430, size, t0 + 0.30, t, fg=fg, bg=bg)
    c.restore()


# ------------------------------------------------------------------ S1 hook (0–2.5)

HOOK = [("Notes.", BLUE_BRIGHT), ("Past papers.", PURPLE), ("Textbooks.", CORAL), ("Questions.", MINT)]


def s1_hook(c, t):
    if t >= 2.5:
        return
    i = min(3, int(t / 0.5))
    word, col = HOOK[i]
    u = t - i * 0.5
    if t < 2.0:
        prev = HOOK[i - 1][1] if i > 0 else WHITE
        k = ease_out_expo(seg(u, 0, 0.22))
        c.drawPaint(paint(prev))
        c.drawCircle(CX, H / 2, 2600 * k, paint(col))
        size = 210
        f = font("Black", size)
        if f.measureText(word) > W * 0.86:
            size = size * W * 0.86 / f.measureText(word)
            f = font("Black", size)
        s = 1.25 - 0.25 * ease_out_back(seg(u, 0, 0.3), 2.2)
        c.save()
        c.translate(CX, H / 2 + size * 0.33)
        c.scale(s, s)
        text(c, word, 0, 0, f, WHITE, "center")
        c.restore()
        text(c, f"0{i + 1} / 04", 80, H - 70, font("SemiBold", 34), with_alpha(WHITE, 0.8))
        return
    implode = ease_in_cubic(seg(t, 2.0, 2.3))
    c.drawCircle(CX, H / 2, max(0.0, 2600 * (1 - implode)), paint(MINT))


# ------------------------------------------------------------------ S2 hello & logo (2.5–5)

def s2_logo(c, t):
    if t < 2.4 or t > 5.2:
        return
    out = ease_in_cubic(seg(t, 4.75, 5.1))
    c.save()
    c.translate(0, -out * 600)
    if not VERT:
        lx, tile_y, word_y, tag_y = 1180, 400, 680, 760
    else:
        lx, tile_y, word_y, tag_y = CX, 1060, 1350, 1430
    kt = seg(t, 2.85, 3.25)
    if kt > 0:
        e = ease_out_back(kt, 1.7)
        c.save()
        c.translate(lx, tile_y)
        c.rotate((1 - e) * -14)
        c.scale(e, e)
        rrect(c, -130, -130 + 20, 260, 260, 64, paint(with_alpha(NAVY, 0.18), blur=28))
        rrect(c, -130, -130, 260, 260, 64, paint(WHITE))
        c.restore()
    logo(c, lx - 5, tile_y, 180, seg(t, 2.95, 3.7) * 1.25, t)
    rise_text(c, "NEBians", lx, word_y, font("ExtraBold", 150), INK, 3.55, t, align="center", stagger=0.04)
    k = seg(t, 3.95, 4.35)
    if k > 0:
        text(c, "Nepal's learning community", lx, tag_y + (1 - ease_out_cubic(k)) * 20, font("Medium", 48),
             with_alpha(MUTED, k), "center")
    c.restore()


# ------------------------------------------------------------------ S3 study materials (5–9)

LEVELS = ["Class 8", "SEE", "Class 11", "Class 12", "Bachelor", "Masters"]
RESOURCES = [
    ("PDF", "BLE SET Solutions", "Class 8 · Science", BLUE_BRIGHT, "atom"),
    ("PAST PAPER", "NEB Board Papers 2083", "Class 12 · All subjects", PURPLE, "paper"),
    ("NOTES", "Probability", "Class 10 / SEE · Maths", CORAL, "chart"),
    ("NOTES", "Physics: Electrostatics", "Class 12 · Physics", TEAL, "wave"),
    ("TEXTBOOK", "Chemistry, Grade 11", "Class 11 · Chemistry", MINT, "flask"),
    ("MODEL Q", "Model Questions", "Class 12 · English", AMBER, "check"),
]

def glyph(c, kind, x, y, w, h, col, k):
    light = mix(col, WHITE, 0.55)
    if kind == "atom":
        for a in (0, 60, 120):
            c.save()
            c.rotate(a + k * 40, x + w / 2, y + h / 2)
            c.drawOval(skia.Rect.MakeXYWH(x + w / 2 - 46, y + h / 2 - 17, 92, 34), paint(col, stroke=5))
            c.restore()
        c.drawCircle(x + w / 2, y + h / 2, 8, paint(col))
    elif kind == "paper":
        for i in range(4):
            c.drawLine(x + 30, y + 28 + i * 24, x + 30 + (w - 60) * (0.9 if i % 2 == 0 else 0.6) * clamp(k * 1.5 - i * 0.1),
                       y + 28 + i * 24, paint(light, stroke=9))
    elif kind == "chart":
        for i, v in enumerate([0.4, 0.75, 0.55, 1.0]):
            bh = (h - 40) * v * clamp(k * 1.5 - i * 0.1)
            rrect(c, x + 34 + i * 42, y + h - 16 - bh, 28, bh, 6, paint(col if i == 3 else light))
    elif kind == "wave":
        p = skia.Path()
        for i in range(61):
            xx = x + 24 + (w - 48) * i / 60
            yy = y + h / 2 + math.sin(i / 60 * 4 * math.pi + k * 6) * 30
            p.moveTo(xx, yy) if i == 0 else p.lineTo(xx, yy)
        c.drawPath(partial_path(p, clamp(k * 1.3)), paint(col, stroke=6))
    elif kind == "flask":
        f = polygon([(x + w / 2 - 14, y + 20), (x + w / 2 + 14, y + 20), (x + w / 2 + 14, y + 50),
                     (x + w / 2 + 44, y + h - 16), (x + w / 2 - 44, y + h - 16), (x + w / 2 - 14, y + 50)])
        c.drawPath(f, paint(col, stroke=5))
        c.save()
        c.clipPath(f, doAntiAlias=True)
        lvl = y + h - 16 - (h - 60) * 0.45 * clamp(k * 1.4)
        c.drawRect(skia.Rect.MakeLTRB(x, lvl, x + w, y + h), paint(light))
        c.restore()
    else:
        for i in range(3):
            yy = y + 24 + i * 34
            c.drawCircle(x + 40, yy, 11, paint(col if clamp(k * 1.6 - i * 0.25) > 0.5 else light))
            c.drawLine(x + 64, yy, x + w - 30, yy, paint(light, stroke=8))




def level_chip(c, t, lv, x, y, k):
    fw = font("Bold", 30)
    pw = fw.measureText(lv) + 44
    if k > 0:
        e = ease_out_back(k, 2.2)
        active = lv == "Class 12" and t > 7.1
        c.save()
        c.translate(x + pw / 2, y)
        c.scale(e, e)
        rrect(c, -pw / 2, -30, pw, 60, 30, paint(BLUE if active else WHITE))
        if not active:
            rrect(c, -pw / 2, -30, pw, 60, 30, paint(mix(BLUE_WASH, BLUE, 0.2), stroke=2.5))
        text(c, lv, 0, 11, fw, WHITE if active else BLUE, "center")
        c.restore()
    return pw


def resource_card(c, t, i, cx, cy, cw, ch, t0):
    typ, title, sub, col, kind = RESOURCES[i]
    k = seg(t, t0, t0 + 0.45)
    if k <= 0:
        return
    e = ease_out_back(k, 1.6)
    c.save()
    c.translate(cx + cw / 2, cy + ch / 2 + (1 - e) * 80)
    c.scale(lerp(0.85, 1.0, e), lerp(0.85, 1.0, e))
    a = clamp(k * 3)
    shadow_rrect(c, -cw / 2, -ch / 2, cw, ch, 26, alpha=0.13 * a, dy=14, blur=20)
    rrect(c, -cw / 2, -ch / 2, cw, ch, 26, paint(with_alpha(WHITE, a)))
    rrect(c, -cw / 2 + 14, -ch / 2 + 14, cw - 28, 128, 18, paint(with_alpha(mix(col, WHITE, 0.88), a)))
    glyph(c, kind, -cw / 2 + 14, -ch / 2 + 14, cw - 28, 128, col, seg(t, t0 + 0.2, t0 + 1.0))
    fw = font("Bold", 20)
    tw = fw.measureText(typ) + 24
    rrect(c, -cw / 2 + 26, -ch / 2 + 26, tw, 34, 17, paint(with_alpha(col, a)))
    text(c, typ, -cw / 2 + 26 + tw / 2, -ch / 2 + 50, fw, with_alpha(WHITE, a), "center")
    text(c, title, -cw / 2 + 26, ch / 2 - 64, font("Bold", 30), with_alpha(INK, a))
    text(c, sub, -cw / 2 + 26, ch / 2 - 26, font("Medium", 24), with_alpha(MUTED, a))
    c.restore()


def s3_materials(c, t):
    if t < 4.9 or t > 9.2:
        return
    out = ease_in_cubic(seg(t, 8.8, 9.15))
    scene_label(c, "Study", "materials.", PURPLE, PURPLE_WASH, 5.05, t, out=out)
    c.save()
    c.translate(0, out * 1300)
    x0, y0, sw = (110, 230, 1040) if not VERT else (80, 500, 920)
    ks = ease_out_back(seg(t, 5.25, 5.65), 1.4)
    if ks > 0:
        w = sw * clamp(ks)
        shadow_rrect(c, x0, y0, w, 84, 42, alpha=0.12, dy=10, blur=16)
        rrect(c, x0, y0, w, 84, 42, paint(WHITE))
        c.drawCircle(x0 + 50, y0 + 38, 15, paint(MUTED, stroke=4))
        c.drawLine(x0 + 61, y0 + 49, x0 + 72, y0 + 60, paint(MUTED, stroke=4))
        q = "class 12 physics notes"
        n = int(len(q) * clamp(seg(t, 5.6, 6.35)))
        f = font("Medium", 36)
        text(c, q[:n], x0 + 96, y0 + 54, f, INK)
        if (t * 2) % 1 < 0.6 and t < 6.6:
            cxx = x0 + 98 + f.measureText(q[:n])
            c.drawLine(cxx, y0 + 24, cxx, y0 + 62, paint(BLUE_BRIGHT, stroke=3))
    rows = [LEVELS] if not VERT else [LEVELS[:3], LEVELS[3:]]
    ly = 375 if not VERT else 650
    idx = 0
    for r, row in enumerate(rows):
        x = x0
        for lv in row:
            k = seg(t, 6.55 + idx * 0.12, 6.95 + idx * 0.12)
            x += level_chip(c, t, lv, x, ly + r * 78, k) + 14
            idx += 1
    if not VERT:
        cw, ch, gx, gy, top, cols = 420, 270, 30, 28, 450, 3
    else:
        cw, ch, gx, gy, top, cols = 445, 270, 30, 26, 790, 2
    for i in range(6):
        r, cidx = divmod(i, cols)
        resource_card(c, t, i, x0 + cidx * (cw + gx), top + r * (ch + gy), cw, ch, 7.30 + i * 0.12)
    c.restore()


# ------------------------------------------------------------------ S4 study mates (9–12.5)

def avatar(c, x, y, r, ini, col, a=1.0):
    c.drawCircle(x, y, r, paint(with_alpha(col, a)))
    text(c, ini, x, y + r * 0.36, font("ExtraBold", r * 1.0), with_alpha(WHITE, a), "center")


def discussion(c, t, x, y, w, h):
    k = seg(t, 9.6, 10.0)
    if k <= 0:
        return
    e = ease_out_back(k, 1.5)
    c.save()
    c.translate(x + w / 2, y + h / 2 + (1 - e) * 60)
    c.scale(lerp(0.9, 1, e), lerp(0.9, 1, e))
    shadow_rrect(c, -w / 2, -h / 2, w, h, 30, alpha=0.13, dy=14, blur=22)
    rrect(c, -w / 2, -h / 2, w, h, 30, paint(WHITE))
    avatar(c, -w / 2 + 64, -h / 2 + 62, 30, "A", CORAL)
    text(c, "Asha started a discussion", -w / 2 + 112, -h / 2 + 56, font("Bold", 28), INK)
    text(c, "Mathematics · Class 8", -w / 2 + 112, -h / 2 + 90, font("Medium", 24), MUTED)
    q = "Can we get a solved paper for BLE maths?"
    n = int(len(q) * clamp(seg(t, 9.75, 10.3)))
    text(c, q[:n], -w / 2 + 40, -h / 2 + 168, font("SemiBold", 36), INK)
    likes = 1 + int(min(4, max(0, (t - 10.4) / 0.15)))
    rrect(c, -w / 2 + 40, h / 2 - 82, 130, 54, 27, paint(BLUE_WASH))
    c.drawPath(polygon([(-w / 2 + 64, h / 2 - 48), (-w / 2 + 64, h / 2 - 64), (-w / 2 + 74, h / 2 - 64),
                        (-w / 2 + 84, h / 2 - 78), (-w / 2 + 90, h / 2 - 74), (-w / 2 + 86, h / 2 - 64),
                        (-w / 2 + 100, h / 2 - 64), (-w / 2 + 96, h / 2 - 44), (-w / 2 + 64, h / 2 - 44)]), paint(BLUE))
    text(c, str(likes), -w / 2 + 128, h / 2 - 43, font("Bold", 30), BLUE, "center")
    replies = 0 + (t > 10.15) + (t > 10.7)
    text(c, f"{replies} replies", -w / 2 + 200, h / 2 - 43, font("SemiBold", 28), MUTED)
    c.restore()


def reply(c, t, i, x, y, w):
    ini, name, col, msg, t0 = [("R", "Rohan", MINT, "Uploaded one in the library. Check Class 8!", 10.15),
                               ("P", "Ms. Pandey", PURPLE, "Try Q5 first, it's the trickiest.", 10.70)][i]
    k = seg(t, t0, t0 + 0.4)
    if k <= 0:
        return
    e = ease_out_back(k, 1.6)
    h = 110
    c.save()
    c.translate(x, y + (1 - e) * 40)
    a = clamp(k * 3)
    shadow_rrect(c, 0, 0, w, h, 26, alpha=0.11 * a, dy=10, blur=16)
    rrect(c, 0, 0, w, h, 26, paint(with_alpha(WHITE, a)))
    avatar(c, 58, h / 2, 30, ini, col, a)
    text(c, name, 110, 44, font("Bold", 26), with_alpha(INK, a))
    n = int(len(msg) * clamp(seg(t, t0 + 0.1, t0 + 0.6)))
    text(c, msg[:n], 110, 82, font("Medium", 28), with_alpha(MUTED, a))
    c.restore()


def poll(c, t, x, y, w, h):
    kp = seg(t, 11.2, 11.6)
    if kp <= 0:
        return
    e = ease_out_back(kp, 1.6)
    c.save()
    c.translate(x + w / 2, y + h / 2)
    c.scale(e, e)
    shadow_rrect(c, -w / 2, -h / 2, w, h, 30, alpha=0.13, dy=14, blur=22)
    rrect(c, -w / 2, -h / 2, w, h, 30, paint(WHITE))
    rrect(c, -w / 2 + 36, -h / 2 + 34, 90, 40, 20, paint(AMBER_WASH))
    text(c, "POLL", -w / 2 + 81, -h / 2 + 62, font("Bold", 22), AMBER_INK, "center")
    text(c, "What should we add next?", -w / 2 + 36, -h / 2 + 128, font("Bold", 32), INK)
    for j, (opt, v, col) in enumerate([("More past papers", 0.62, BLUE_BRIGHT), ("Video lessons", 0.24, PURPLE),
                                       ("Practice quizzes", 0.14, MINT)]):
        yy = -h / 2 + 180 + j * 88
        kk = ease_out_cubic(seg(t, 11.4 + j * 0.12, 12.1 + j * 0.12))
        rrect(c, -w / 2 + 36, yy, w - 72, 62, 16, paint(mix(BLUE_WASH, WHITE, 0.4)))
        if kk > 0:
            rrect(c, -w / 2 + 36, yy, (w - 72) * v * kk, 62, 16, paint(mix(col, WHITE, 0.55)))
        text(c, opt, -w / 2 + 58, yy + 41, font("SemiBold", 27), INK)
        text(c, f"{int(round(v * 100 * kk))}%", w / 2 - 58, yy + 41, font("Bold", 27), INK, "right")
    c.restore()


def s4_mates(c, t):
    if t < 8.9 or t > 12.7:
        return
    out = ease_in_cubic(seg(t, 12.3, 12.65))
    scene_label(c, "Study", "mates.", AMBER_INK, AMBER_WASH, 9.05, t, out=out)
    c.save()
    c.translate(0, out * 1300)
    if not VERT:
        discussion(c, t, 110, 260, 1000, 300)
        reply(c, t, 0, 190, 590, 920)
        reply(c, t, 1, 230, 720, 920)
        poll(c, t, 1190, 300, 620, 470)
    else:
        discussion(c, t, 70, 520, 940, 300)
        reply(c, t, 0, 110, 850, 900)
        reply(c, t, 1, 150, 980, 860)
        poll(c, t, 70, 1130, 940, 470)
    c.restore()


# ------------------------------------------------------------------ S5 share, earn, climb (12.5–15.5)

BOARD = [("Prashant", "P", TEAL, 1840), ("Anil", "A", CORAL, 1620), ("Bikram", "B", PURPLE, 1490),
         ("Sita", "S", MINT, 1310), ("You", "Y", BLUE_BRIGHT, 1180)]
STEPS = [("1", "Share", "Upload notes and papers", BLUE_BRIGHT, 12.70),
         ("2", "Earn", "Points and badges", AMBER, 13.30),
         ("3", "Climb", "Rise on the leaderboard", MINT, 13.90)]


def panel(c, t, x, y, w, h, step):
    num, title, sub, col, t0 = step
    k = seg(t, t0, t0 + 0.45)
    if k <= 0:
        return 0.0
    e = ease_out_back(k, 1.5)
    c.save()
    c.translate(x + w / 2, y + h / 2 + (1 - e) * 70)
    s = lerp(0.88, 1, e)
    c.scale(s, s)
    shadow_rrect(c, -w / 2, -h / 2, w, h, 34, alpha=0.13, dy=16, blur=24)
    rrect(c, -w / 2, -h / 2, w, h, 34, paint(WHITE))
    c.drawCircle(-w / 2 + 56, -h / 2 + 56, 26, paint(col))
    text(c, num, -w / 2 + 56, -h / 2 + 67, font("ExtraBold", 30), WHITE, "center")
    text(c, title, -w / 2 + 98, -h / 2 + 54, font("ExtraBold", 36), INK)
    text(c, sub, -w / 2 + 98, -h / 2 + 86, font("Medium", 22), MUTED)
    c.restore()
    return k


def share_art(c, t, cx, cy, s):
    c.save()
    c.translate(cx, cy)
    c.scale(s, s)
    dash = paint(mix(BLUE_WASH, BLUE, 0.35), stroke=4)
    dash.setPathEffect(skia.DashPathEffect.Make([18, 14], t * 40))
    rrect(c, -190, -150, 380, 300, 30, dash)
    ring = skia.Path()
    ring.addCircle(0, -10, 112)
    ku = seg(t, 13.10, 13.60)
    c.drawPath(ring, paint(BLUE_WASH, stroke=10))
    if ku > 0:
        c.drawPath(partial_path(ring, ease_in_out(ku)), paint(BLUE_BRIGHT, stroke=10))
    kd = seg(t, 12.80, 13.12)
    if kd > 0:
        fy = lerp(-330, -10, ease_out_back(kd, 1.6))
        c.save()
        c.translate(0, fy)
        rrect(c, -58, -76, 116, 152, 14, paint(WHITE))
        rrect(c, -58, -76, 116, 152, 14, paint(mix(CORAL, WHITE, 0.3), stroke=4))
        rrect(c, -46, 22, 92, 38, 9, paint(CORAL))
        text(c, "PDF", 0, 50, font("ExtraBold", 26), WHITE, "center")
        c.restore()
    kc = seg(t, 13.60, 13.85)
    if kc > 0:
        e = ease_out_back(kc, 2.6)
        c.drawCircle(84, -94, 30 * e, paint(MINT))
        ck = skia.Path()
        ck.moveTo(70, -94)
        ck.lineTo(80, -83)
        ck.lineTo(99, -105)
        c.drawPath(partial_path(ck, kc), paint(WHITE, stroke=6))
    text(c, "Uploaded!" if t > 13.6 else "Uploading…", 0, 128, font("Bold", 26), MUTED, "center")
    c.restore()


def earn_art(c, t, cx, cy, s):
    c.save()
    c.translate(cx, cy)
    c.scale(s, s)
    kb = seg(t, 13.60, 14.00)
    if kb > 0:
        e = ease_out_back(kb, 2.4)
        for j in range(10):
            a = j * math.pi / 5 + t * 0.6
            c.drawLine(math.cos(a) * 120 * e, -30 + math.sin(a) * 120 * e, math.cos(a) * 150 * e, -30 + math.sin(a) * 150 * e,
                       paint(with_alpha(AMBER, 0.5), stroke=6))
        c.save()
        c.translate(0, -30)
        c.rotate((1 - e) * 60)
        c.scale(e, e)
        c.drawPath(polygon([(-40, 40), (-60, 120), (-20, 100), (0, 130), (0, 40)]), paint(BLUE_BRIGHT))
        c.drawPath(polygon([(40, 40), (60, 120), (20, 100), (0, 130), (0, 40)]), paint(CORAL))
        c.drawCircle(0, 0, 84, paint(AMBER))
        c.drawCircle(0, 0, 66, paint(mix(AMBER, WHITE, 0.25)))
        star(c, 0, 0, 38, WHITE)
        c.restore()
        text(c, "Top contributor", 0, 150, font("Bold", 28), AMBER_INK, "center")
    kp = seg(round(t * FPS) / FPS, 13.85, 14.35)
    if kp > 0:
        rrect(c, -90, 176, 180, 54, 27, paint(AMBER_WASH))
        text(c, f"+{int(round(120 * ease_out_cubic(kp)))} pts", 0, 213, font("ExtraBold", 28), AMBER_INK, "center")
    c.restore()


def climb_rows(c, t, x, y, w, rowh):
    climb = ease_in_out(seg(t, 14.30, 14.80))
    for i, (name, ini, col, pts) in enumerate(BOARD):
        rank = lerp(4, 1, climb) if name == "You" else (i + climb if 1 <= i <= 3 else i)
        yy = y + rank * rowh
        ki = seg(t, 14.0 + i * 0.06, 14.3 + i * 0.06)
        if ki <= 0:
            continue
        a = clamp(ki * 2)
        you = name == "You"
        if you:
            rrect(c, x, yy, w, rowh - 10, 16, paint(with_alpha(mix(BLUE_WASH, WHITE, 0.15), a)))
        text(c, f"#{int(round(rank)) + 1}", x + 40, yy + rowh * 0.58, font("ExtraBold", 28), with_alpha(BLUE if you else MUTED, a), "center")
        avatar(c, x + 108, yy + rowh * 0.45, 24, ini, col, a)
        text(c, name, x + 148, yy + rowh * 0.58, font("Bold", 28), with_alpha(INK, a))
        p = pts if not you else int(lerp(1180, 1705, climb))
        text(c, f"{p:,}", x + w - 24, yy + rowh * 0.58, font("SemiBold", 26), with_alpha(MUTED, a), "right")


def arrow(c, x0, y0, x1, y1, k):
    if k <= 0:
        return
    p = skia.Path()
    p.moveTo(x0, y0)
    p.lineTo(x1, y1)
    c.drawPath(partial_path(p, ease_out_cubic(k)), paint(mix(BLUE_WASH, BLUE, 0.45), stroke=6))
    if k > 0.8:
        ang = math.atan2(y1 - y0, x1 - x0)
        hx, hy = x1, y1
        c.drawPath(polygon([(hx, hy), (hx - 18 * math.cos(ang - 0.5), hy - 18 * math.sin(ang - 0.5)),
                            (hx - 18 * math.cos(ang + 0.5), hy - 18 * math.sin(ang + 0.5))]), paint(mix(BLUE_WASH, BLUE, 0.45)))


def s5_share(c, t):
    if t < 12.4 or t > 15.7:
        return
    out = ease_in_cubic(seg(t, 15.3, 15.65))
    f = font("ExtraBold", 104 if not VERT else 116)
    c.save()
    c.translate(0, -out * 400)
    if not VERT:
        ww = [f.measureText("Share."), f.measureText("Earn."), f.measureText("Climb.") + 2 * 0.30 * 104]
        total = sum(ww) + 2 * 30
        x = CX - total / 2
        rise_text(c, "Share.", x, 170, f, INK, 12.55, t)
        rise_text(c, "Earn.", x + ww[0] + 30, 170, f, INK, 12.70, t)
        chip(c, "Climb.", x + ww[0] + ww[1] + 60, 170, 104, 12.85, t, fg=WHITE, bg=BLUE_BRIGHT)
    else:
        w1 = f.measureText("Share. ")
        tot = w1 + f.measureText("Earn.")
        rise_text(c, "Share.", CX - tot / 2, 290, f, INK, 12.55, t)
        rise_text(c, "Earn.", CX - tot / 2 + w1, 290, f, INK, 12.70, t)
        cw = f.measureText("Climb.") + 2 * 0.30 * 116
        chip(c, "Climb.", CX - cw / 2, 430, 116, 12.85, t, fg=WHITE, bg=BLUE_BRIGHT)
    c.restore()
    c.save()
    c.translate(0, out * 1300)
    if not VERT:
        pw, ph, gap, py = 540, 640, 40, 280
        xs = [CX - 1.5 * pw - gap, CX - 0.5 * pw, CX + 0.5 * pw + gap]
        k1 = panel(c, t, xs[0], py, pw, ph, STEPS[0])
        if k1 > 0:
            share_art(c, t, xs[0] + pw / 2, py + 370, 1.0)
        k2 = panel(c, t, xs[1], py, pw, ph, STEPS[1])
        if k2 > 0:
            earn_art(c, t, xs[1] + pw / 2, py + 330, 1.0)
        k3 = panel(c, t, xs[2], py, pw, ph, STEPS[2])
        if k3 > 0:
            climb_rows(c, t, xs[2] + 24, py + 140, pw - 48, 96)
        arrow(c, xs[0] + pw + 6, py + ph / 2, xs[1] - 6, py + ph / 2, seg(t, 13.15, 13.4))
        arrow(c, xs[1] + pw + 6, py + ph / 2, xs[2] - 6, py + ph / 2, seg(t, 13.75, 14.0))
    else:
        pw, x = 940, 70
        k1 = panel(c, t, x, 520, pw, 400, STEPS[0])
        if k1 > 0:
            share_art(c, t, x + pw / 2, 520 + 235, 0.68)
        k2 = panel(c, t, x, 950, pw, 340, STEPS[1])
        if k2 > 0:
            earn_art(c, t, x + pw / 2, 950 + 165, 0.62)
        k3 = panel(c, t, x, 1320, pw, 560, STEPS[2])
        if k3 > 0:
            climb_rows(c, t, x + 30, 1320 + 120, pw - 60, 84)
    c.restore()


# ------------------------------------------------------------------ S6 tools & app (15.5–18)

TOOLS = [("Result Checker", "SEE, Class 11 & 12 gradesheets", BLUE_BRIGHT, 15.80),
         ("PDF Tools", "Merge, split, compress, convert", CORAL, 16.05),
         ("Android app", "Ask Neby, right in the PDF reader", MINT, 16.30)]


def tool_art(c, t, i, cx, cy, s, col, t0):
    c.save()
    c.translate(cx, cy)
    c.scale(s, s)
    kk = seg(t, t0 + 0.2, t0 + 1.2)
    if i == 0:
        for j, (g, v) in enumerate([("A+", 1.0), ("A", 0.86), ("B+", 0.72), ("A", 0.88), ("A+", 0.98)]):
            bh = 200 * v * ease_out_back(clamp(kk * 1.4 - j * 0.12), 1.4)
            rrect(c, -200 + j * 84, 150 - bh, 54, bh, 10, paint(col if g == "A+" else mix(col, WHITE, 0.45)))
            text(c, g, -173 + j * 84, 150 - bh - 12, font("Bold", 24), INK, "center")
        text(c, f"GPA {3.2 + 0.4 * ease_out_cubic(kk):.2f}", 0, -110, font("ExtraBold", 44), col, "center")
    elif i == 1:
        for j in range(3):
            off = (1 - ease_in_out(clamp(kk * 1.5))) * (j - 1) * 120
            c.save()
            c.translate(off, (j - 1) * 18)
            rrect(c, -80, -110, 160, 210, 14, paint(WHITE))
            rrect(c, -80, -110, 160, 210, 14, paint(mix(col, WHITE, 0.4), stroke=3))
            for q in range(4):
                c.drawLine(-52, -70 + q * 34, 52, -70 + q * 34, paint(mix(col, WHITE, 0.6), stroke=8))
            c.restore()
    else:
        px, py, pw, ph = -110, -165, 220, 340
        rrect(c, px, py, pw, ph, 30, paint(0xFF101828))
        rrect(c, px + 10, py + 10, pw - 20, ph - 20, 22, paint(WHITE))
        for q in range(6):
            c.drawLine(px + 34, py + 50 + q * 30, px + pw - 34, py + 50 + q * 30, paint(mix(BLUE_WASH, MUTED, 0.3), stroke=7))
        ka = seg(t, 16.7, 17.0)
        sc = 1 - 0.12 * math.sin(math.pi * ka)
        c.save()
        c.translate(0, py + ph - 52)
        c.scale(sc, sc)
        rrect(c, -78, -24, 156, 48, 24, paint(BLUE_BRIGHT))
        text(c, "Ask Neby", 0, 9, font("Bold", 22), WHITE, "center")
        c.restore()
        if 0 < ka < 1:
            c.drawCircle(0, py + ph - 52, 20 + 90 * ka, paint(with_alpha(BLUE_BRIGHT, 0.35 * (1 - ka))))
    c.restore()


def s6_tools(c, t):
    if t < 15.4 or t > 18.2:
        return
    out = ease_in_cubic(seg(t, 17.75, 18.05))
    c.save()
    c.translate(0, -out * 400)
    if not VERT:
        rise_text(c, "Handy tools, built in.", CX, 170, font("ExtraBold", 96), INK, 15.55, t, align="center")
    else:
        rise_text(c, "Handy tools,", 80, 290, font("ExtraBold", 112), INK, 15.55, t)
        rise_text(c, "built in.", 80, 410, font("ExtraBold", 112), BLUE_BRIGHT, 15.70, t)
    c.restore()
    for i, (title, sub, col, t0) in enumerate(TOOLS):
        k = seg(t, t0, t0 + 0.45)
        if k <= 0:
            continue
        e = ease_out_back(k, 1.6)
        if not VERT:
            w, h = 540, 640
            x = CX - 1.5 * w - 40 + i * (w + 40)
            y = 270
        else:
            w, h = 940, 420
            x, y = 70, 500 + i * 450
        y += (1 - e) * 100 + out * 1400
        c.save()
        c.translate(x + w / 2, y + h / 2)
        c.scale(lerp(0.85, 1, e), lerp(0.85, 1, e))
        shadow_rrect(c, -w / 2, -h / 2, w, h, 34, alpha=0.13, dy=16, blur=24)
        rrect(c, -w / 2, -h / 2, w, h, 34, paint(WHITE))
        if not VERT:
            rrect(c, -w / 2 + 20, -h / 2 + 20, w - 40, 380, 24, paint(mix(col, WHITE, 0.88)))
            tool_art(c, t, i, 0, -h / 2 + 210, 1.0, col, t0)
            text(c, title, -w / 2 + 40, h / 2 - 150, font("ExtraBold", 44), INK)
            text(c, sub, -w / 2 + 40, h / 2 - 96, font("Medium", 26), MUTED)
        else:
            rrect(c, -w / 2 + 20, -h / 2 + 20, 430, h - 40, 24, paint(mix(col, WHITE, 0.88)))
            tool_art(c, t, i, -w / 2 + 235, 0, 0.92, col, t0)
            text(c, title, -w / 2 + 490, -20, font("ExtraBold", 44), INK)
            sub_lines = [["SEE, Class 11 & 12", "gradesheets"], ["Merge, split,", "compress, convert"],
                         ["Ask Neby, right in", "the PDF reader"]][i]
            for j, ln in enumerate(sub_lines):
                text(c, ln, -w / 2 + 490, 30 + j * 38, font("Medium", 28), MUTED)
        c.restore()


# ------------------------------------------------------------------ S7 end card (18–22)

def s7_end(c, t):
    if t < 17.7:
        return
    origin = (480, 760) if not VERT else (CX, 520)
    k = ease_in_out(seg(t, 17.75, 18.15))
    p = paint(WHITE)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(CX, H * 0.46), 1700, [0xFF1466F0, BLUE, 0xFF0A2E8A], [0, 0.55, 1]))
    c.drawCircle(origin[0], origin[1], 3000 * k, p)
    if t < 18.0:
        return
    nx, ny = (480, 560) if not VERT else (CX, 500)
    for j in range(46):
        a = j * 2.399
        kk = seg(t, 18.05 + (j % 7) * 0.03, 19.6 + (j % 5) * 0.1)
        if 0 < kk < 1:
            r = 120 + 950 * ease_out_expo(kk)
            px = nx + math.cos(a) * r
            py = ny + math.sin(a) * r * 0.7 + 220 * kk * kk
            col = [AMBER, CORAL, WHITE, MINT, 0xFF9CC3FF][j % 5]
            c.save()
            c.translate(px, py)
            c.rotate(j * 37 + t * 300)
            rrect(c, -8, -3.5, 16, 7, 3.5, paint(with_alpha(col, 1 - kk)))
            c.restore()
    if not VERT:
        lx, tile_y, word_y, tag_y, url_y, free_y, cls_y = 1230, 290, 545, 630, 745, 850, 905
    else:
        lx, tile_y, word_y, tag_y, url_y, free_y, cls_y = CX, 930, 1200, 1285, 1400, 1505, 1560
    fy = math.sin(t * 2.0) * 5
    kt0 = seg(t, 18.3, 18.7)
    if kt0 > 0:
        e = ease_out_back(kt0, 1.7)
        c.save()
        c.translate(lx, tile_y + fy)
        c.rotate((1 - e) * -14)
        c.scale(e, e)
        rrect(c, -125, -125 + 18, 250, 250, 62, paint(with_alpha(0xFF001A66, 0.35), blur=26))
        rrect(c, -125, -125, 250, 250, 62, paint(WHITE))
        c.restore()
    logo(c, lx - 5, tile_y + fy, 172, seg(t, 18.4, 19.2) * 1.25, t)
    rise_text(c, "NEBians", lx, word_y, font("ExtraBold", 140), WHITE, 19.05, t, align="center", stagger=0.04)
    kt = seg(t, 19.45, 19.85)
    if kt > 0:
        f = font("ExtraBold", 50)
        parts = [("Study ", WHITE), ("materials", 0xFFC9BDFF), (". Study ", WHITE), ("mates", 0xFFFFD58A), (".", WHITE)]
        total = sum(f.measureText(s) for s, _ in parts)
        x = lx - total / 2
        for s, col in parts:
            text(c, s, x, tag_y + (1 - ease_out_cubic(kt)) * 20, f, with_alpha(col, kt))
            x += f.measureText(s)
    ku = seg(t, 19.8, 20.2)
    if ku > 0:
        e = ease_out_back(ku, 1.8)
        fu = font("Bold", 44)
        url = "nebians.consica.com.np"
        uw = fu.measureText(url) + 84
        c.save()
        c.translate(lx, url_y)
        c.scale(e, e)
        rrect(c, -uw / 2, -44, uw, 88, 44, paint(WHITE))
        text(c, url, 0, 16, fu, BLUE, "center")
        c.restore()
    ks = seg(t, 20.2, 20.6)
    if ks > 0:
        text(c, "Free on the web  ·  Android app on Google Play", lx, free_y, font("Medium", 34 if not VERT else 31),
             with_alpha(0xFFC9D8FF, ks), "center")
        text(c, "Class 8 to Masters  ·  Notes, papers, books and a community", lx, cls_y, font("Medium", 28 if not VERT else 25),
             with_alpha(0xFF9FB8F0, ks), "center")
    sparks = [(1010, 150), (1460, 200), (1500, 420), (950, 430)] if not VERT else [(260, 800), (830, 820), (870, 1060), (210, 1060)]
    for (sx, sy), d in zip(sparks, (0.0, 0.15, 0.25, 0.35)):
        kk = seg(t, 19.1 + d, 19.8 + d)
        if 0 < kk < 1:
            star(c, sx, sy, 24 * math.sin(math.pi * kk), WHITE)


# ------------------------------------------------------------------ Neby's path

SPOTS = {
    False: {"pop": (960, 600, 380), "hello": (520, 580, 360), "materials": (1640, 830, 300),
            "mates": (1500, 930, 240), "share": (CX, 1000, 130), "tools": (1690, 175, 170), "end": (480, 560, 520)},
    True: {"pop": (CX, 960, 460), "hello": (CX, 600, 380), "materials": (870, 330, 190),
           "mates": (CX, 1790, 250), "share": (910, 430, 150), "tools": (890, 350, 190), "end": (CX, 500, 470)},
}


def neby_path(t):
    S = SPOTS[VERT]

    def hop(a, b, p0, p1, h, lean=8):
        k = seg(t, a, b)
        e = ease_in_out(k)
        st = math.sin(math.pi * k)
        return (lerp(p0[0], p1[0], e), lerp(p0[1], p1[1], e) - h * st, lerp(p0[2], p1[2], e),
                lean * st * (1 if p1[0] >= p0[0] else -1), 1 - 0.06 * st, 1 + 0.10 * st)

    def land(after, spot, bob=0.0):
        u = t - after
        x, y, s = spot
        sx = sy = 1.0
        if 0 < u < 0.7:
            q = 0.13 * math.exp(-u * 8) * math.cos(u * 24)
            sx, sy = 1 + q, 1 - q
        return (x, y + bob, s, 0.0, sx, sy)

    if t < 2.15:
        return None
    if t < 2.6:
        k = ease_out_back(seg(t, 2.15, 2.55), 1.8)
        x, y, s = S["pop"]
        return (x, y, s * k, 0, 1, 1)
    if t < 2.9:
        return land(2.55, S["pop"])
    seq = [(2.9, 3.3, "pop", "hello", 160), (4.85, 5.35, "hello", "materials", 260),
           (8.85, 9.35, "materials", "mates", 160), (12.35, 12.85, "mates", "share", 240),
           (15.35, 15.85, "share", "tools", 200)]
    for a, b, p0, p1, h in seq:
        if a <= t < b:
            return hop(a, b, S[p0], S[p1], h)
    for (a, b, p0, p1, h), nxt in zip(seq, [x[0] for x in seq[1:]] + [17.75]):
        if b <= t < nxt:
            return land(b, S[p1], math.sin(t * 3) * 5)
    if t < 18.05:
        k = ease_in_out(seg(t, 17.75, 18.05))
        x0, y0, s0 = S["tools"]
        x1, y1, _ = S["end"]
        return (lerp(x0, x1, k), lerp(y0, y1, k) - 120 * math.sin(math.pi * k), lerp(s0, 300, k), 0, 1, 1)
    k = ease_out_back(seg(t, 18.05, 18.5), 1.5)
    x1, y1, s1 = S["end"]
    hopp = 90 * abs(math.sin((t - 18.0) / 0.45 * math.pi)) if 18.0 < t < 18.9 else 0.0
    x, y, s, r, sx, sy = land(18.5, (x1, y1 + math.sin(t * 2.4) * 10, lerp(300, s1, k)))
    return (x, y - hopp, s, r, sx, sy)


def draw_neby(c, t):
    p = neby_path(t)
    if not p:
        return
    x, y, s, r, sx, sy = p
    neby(c, t, x, y, s, rot=r, sx=sx, sy=sy, shadow=t < 17.75)


def frame(c, t):
    background(c, t)
    s2_logo(c, t)
    s3_materials(c, t)
    s4_mates(c, t)
    s5_share(c, t)
    s6_tools(c, t)
    s7_end(c, t)
    if t < 2.5:
        s1_hook(c, t)
    draw_neby(c, t)
