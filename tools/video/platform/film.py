"""NEBians platform launch film (22 s). Every frame is a pure function of t (seconds)."""
import importlib.util
import math
import os
import sys

import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "neby"))
from characters import logo  # noqa: E402
from kit import (AMBER, BLUE, BLUE_BRIGHT, BLUE_WASH, CORAL, H, INK, MINT, MUTED, NAVY,  # noqa: E402
                 PURPLE, TEAL, W, WHITE, clamp, ease_in_cubic, ease_in_out, ease_out_back,
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


def scene_label(c, lead, chip_text, fg, bg, t0, t, x=110, y=170, size=104, out=0.0):
    c.save()
    c.translate(0, -out * 300)
    f = font("ExtraBold", size)
    w = rise_text(c, lead, x, y, f, INK, t0, t)
    chip(c, chip_text, x + w + 26, y, size, t0 + 0.30, t, fg=fg, bg=bg)
    c.restore()


# ------------------------------------------------------------------ S1 hook (0–2.5)

HOOK = [("Notes.", BLUE_BRIGHT), ("Past papers.", PURPLE), ("Textbooks.", CORAL), ("Questions.", MINT)]


def s1_hook(c, t):
    if t >= 2.5:
        return
    i = min(3, int(t / 0.5))
    word, col = HOOK[i]
    u = t - i * 0.5
    implode = ease_in_cubic(seg(t, 2.0, 2.3))
    c.save()
    if t < 2.0:
        c.drawPaint(paint(col))
        prev = HOOK[i - 1][1] if i > 0 else WHITE
        k = ease_out_expo(seg(u, 0, 0.22))
        r = 2300 * k
        c.drawPaint(paint(prev))
        c.drawCircle(960, 540, r, paint(col))
        s = 1.25 - 0.25 * ease_out_back(seg(u, 0, 0.3), 2.2)
        c.translate(960, 600)
        c.scale(s, s)
        text(c, word, 0, 0, font("Black", 210), WHITE, "center")
        tag = f"0{i + 1} / 04"
        c.restore()
        text(c, tag, 80, 1010, font("SemiBold", 34), with_alpha(WHITE, 0.8))
        return
    c.restore()
    r = 2300 * (1 - implode) + 0.0
    c.drawCircle(960, 600, max(r, 0), paint(MINT))


# ------------------------------------------------------------------ S2 hello & logo (2.5–5)

def s2_logo(c, t):
    if t < 2.4 or t > 5.2:
        return
    out = ease_in_cubic(seg(t, 4.75, 5.1))
    c.save()
    c.translate(0, -out * 500)
    kt = seg(t, 2.85, 3.25)
    if kt > 0:
        e = ease_out_back(kt, 1.7)
        c.save()
        c.translate(1180, 400)
        c.rotate((1 - e) * -14)
        c.scale(e, e)
        rrect(c, -130, -130 + 20, 260, 260, 64, paint(with_alpha(NAVY, 0.18), blur=28))
        rrect(c, -130, -130, 260, 260, 64, paint(WHITE))
        c.restore()
    logo(c, 1175, 400, 180, seg(t, 2.95, 3.7) * 1.25, t)
    rise_text(c, "NEBians", 1180, 680, font("ExtraBold", 150), INK, 3.55, t, align="center", stagger=0.04)
    k = seg(t, 3.95, 4.35)
    if k > 0:
        text(c, "Nepal's learning community", 1180, 760 + (1 - ease_out_cubic(k)) * 20, font("Medium", 48),
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


def s3_materials(c, t):
    if t < 4.9 or t > 9.2:
        return
    out = ease_in_cubic(seg(t, 8.8, 9.15))
    scene_label(c, "Study", "materials.", PURPLE, PURPLE_WASH, 5.05, t, out=out)
    c.save()
    c.translate(0, out * 900)
    ks = ease_out_back(seg(t, 5.25, 5.65), 1.4)
    if ks > 0:
        sw = 1040 * clamp(ks)
        x0, y0 = 110, 230
        shadow_rrect(c, x0, y0, sw, 84, 42, alpha=0.12, dy=10, blur=16)
        rrect(c, x0, y0, sw, 84, 42, paint(WHITE))
        c.drawCircle(x0 + 50, y0 + 38, 15, paint(MUTED, stroke=4))
        c.drawLine(x0 + 61, y0 + 49, x0 + 72, y0 + 60, paint(MUTED, stroke=4))
        q = "class 12 physics notes"
        n = int(len(q) * clamp(seg(t, 5.6, 6.35)))
        f = font("Medium", 36)
        text(c, q[:n], x0 + 96, y0 + 54, f, INK)
        if (t * 2) % 1 < 0.6 and t < 6.6:
            cx = x0 + 98 + f.measureText(q[:n])
            c.drawLine(cx, y0 + 24, cx, y0 + 62, paint(BLUE_BRIGHT, stroke=3))
    x = 110
    for i, lv in enumerate(LEVELS):
        k = seg(t, 6.55 + i * 0.12, 6.95 + i * 0.12)
        fw = font("Bold", 30)
        pw = fw.measureText(lv) + 44
        if k > 0:
            e = ease_out_back(k, 2.2)
            active = lv == "Class 12" and t > 7.1
            c.save()
            c.translate(x + pw / 2, 375)
            c.scale(e, e)
            rrect(c, -pw / 2, -30, pw, 60, 30, paint(BLUE if active else WHITE))
            if not active:
                rrect(c, -pw / 2, -30, pw, 60, 30, paint(mix(BLUE_WASH, BLUE, 0.2), stroke=2.5))
            text(c, lv, 0, 11, fw, WHITE if active else BLUE, "center")
            c.restore()
        x += pw + 14
    for i, (typ, title, sub, col, kind) in enumerate(RESOURCES):
        t0 = 7.30 + i * 0.12
        k = seg(t, t0, t0 + 0.45)
        if k <= 0:
            continue
        e = ease_out_back(k, 1.6)
        r, cidx = divmod(i, 3)
        cw, ch = 420, 270
        cx = 110 + cidx * (cw + 30)
        cy = 450 + r * (ch + 28)
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
    c.restore()


# ------------------------------------------------------------------ S4 study mates (9–12.5)

def avatar(c, x, y, r, ini, col, a=1.0):
    c.drawCircle(x, y, r, paint(with_alpha(col, a)))
    text(c, ini, x, y + r * 0.36, font("ExtraBold", r * 1.0), with_alpha(WHITE, a), "center")


def s4_mates(c, t):
    if t < 8.9 or t > 12.7:
        return
    out = ease_in_cubic(seg(t, 12.3, 12.65))
    scene_label(c, "Study", "mates.", AMBER_INK, AMBER_WASH, 9.05, t, out=out)
    c.save()
    c.translate(0, out * 900)
    k = seg(t, 9.6, 10.0)
    if k > 0:
        e = ease_out_back(k, 1.5)
        x, y, w, h = 110, 260, 1000, 300
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
        text(c, q[:n], -w / 2 + 40, -h / 2 + 168, font("SemiBold", 38), INK)
        likes = 1 + int(min(4, max(0, (t - 10.4) / 0.15)))
        rrect(c, -w / 2 + 40, h / 2 - 82, 130, 54, 27, paint(BLUE_WASH))
        c.drawPath(polygon([(-w / 2 + 64, h / 2 - 48), (-w / 2 + 64, h / 2 - 64), (-w / 2 + 74, h / 2 - 64),
                            (-w / 2 + 84, h / 2 - 78), (-w / 2 + 90, h / 2 - 74), (-w / 2 + 86, h / 2 - 64),
                            (-w / 2 + 100, h / 2 - 64), (-w / 2 + 96, h / 2 - 44), (-w / 2 + 64, h / 2 - 44)]), paint(BLUE))
        text(c, str(likes), -w / 2 + 128, h / 2 - 43, font("Bold", 30), BLUE, "center")
        replies = 0 + (t > 10.15) + (t > 10.7)
        text(c, f"{replies} replies", -w / 2 + 200, h / 2 - 43, font("SemiBold", 28), MUTED)
        c.restore()
    for i, (ini, name, col, msg, t0) in enumerate([("R", "Rohan", MINT, "Uploaded one in the library. Check Class 8!", 10.15),
                                                  ("P", "Ms. Pandey", PURPLE, "Try Q5 first, it's the trickiest.", 10.70)]):
        k = seg(t, t0, t0 + 0.4)
        if k <= 0:
            continue
        e = ease_out_back(k, 1.6)
        x, y, w, h = 190 + i * 40, 590 + i * 130, 920, 110
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
    kp = seg(t, 11.2, 11.6)
    if kp > 0:
        e = ease_out_back(kp, 1.6)
        x, y, w, h = 1190, 300, 620, 470
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
    c.restore()


# ------------------------------------------------------------------ S5 share, earn, climb (12.5–15.5)

BOARD = [("Prashant", "P", TEAL, 1840), ("Anil", "A", CORAL, 1620), ("Bikram", "B", PURPLE, 1490),
         ("Sita", "S", MINT, 1310), ("You", "Y", BLUE_BRIGHT, 1180)]


def s5_share(c, t):
    if t < 12.4 or t > 15.7:
        return
    out = ease_in_cubic(seg(t, 15.3, 15.65))
    c.save()
    c.translate(0, -out * 300)
    f = font("ExtraBold", 104)
    w1 = rise_text(c, "Share.", 110, 170, f, INK, 12.55, t)
    w2 = rise_text(c, "Earn.", 110 + w1 + 30, 170, f, INK, 12.70, t)
    chip(c, "Climb.", 110 + w1 + w2 + 60, 170, 104, 12.85, t, fg=WHITE, bg=BLUE_BRIGHT)
    c.restore()
    c.save()
    c.translate(0, out * 900)
    zx, zy, zw, zh = 110, 280, 760, 470
    kz = seg(t, 12.6, 12.95)
    if kz > 0:
        a = clamp(kz * 2)
        rrect(c, zx, zy, zw, zh, 34, paint(with_alpha(WHITE, a)))
        dash = paint(with_alpha(mix(BLUE_WASH, BLUE, 0.35), a), stroke=4)
        dash.setPathEffect(skia.DashPathEffect.Make([18, 14], t * 40))
        rrect(c, zx + 18, zy + 18, zw - 36, zh - 36, 26, dash)
        text(c, "Upload a resource", zx + zw / 2, zy + zh - 60, font("Bold", 34), with_alpha(INK, a), "center")
        kd = seg(t, 12.8, 13.15)
        fy = lerp(zy - 260, zy + 150, ease_out_back(kd, 1.6))
        if kd > 0:
            c.save()
            c.translate(zx + zw / 2 - 90, fy)
            rrect(c, -70, -90, 140, 180, 16, paint(WHITE))
            rrect(c, -70, -90, 140, 180, 16, paint(mix(CORAL, WHITE, 0.3), stroke=4))
            rrect(c, -56, 30, 112, 44, 10, paint(CORAL))
            text(c, "PDF", 0, 62, font("ExtraBold", 30), WHITE, "center")
            c.restore()
        ku = seg(t, 13.15, 13.7)
        if ku > 0:
            ring = skia.Path()
            ring.addCircle(zx + zw / 2 - 90, zy + 150, 128)
            c.drawPath(ring, paint(with_alpha(BLUE_WASH, 1), stroke=10))
            c.drawPath(partial_path(ring, ease_in_out(ku)), paint(BLUE_BRIGHT, stroke=10))
        kb = seg(t, 13.75, 14.15)
        if kb > 0:
            e = ease_out_back(kb, 2.4)
            c.save()
            c.translate(zx + zw - 170, zy + 120)
            c.rotate((1 - e) * 40)
            c.scale(e, e)
            c.drawCircle(0, 0, 76, paint(AMBER))
            c.drawCircle(0, 0, 60, paint(mix(AMBER, WHITE, 0.25)))
            star(c, 0, 0, 34, WHITE)
            c.restore()
            text(c, "Top contributor", zx + zw - 170, zy + 240, font("Bold", 26), with_alpha(AMBER_INK, clamp(kb * 2)), "center")
    bx, by, bw = 950, 280, 860
    kl = seg(t, 12.9, 13.3)
    if kl > 0:
        a = clamp(kl * 2)
        shadow_rrect(c, bx, by, bw, 560, 30, alpha=0.12 * a, dy=14, blur=22)
        rrect(c, bx, by, bw, 560, 30, paint(with_alpha(WHITE, a)))
        text(c, "Leaderboard", bx + 40, by + 70, font("Bold", 34), with_alpha(INK, a))
        climb = ease_in_out(seg(t, 14.3, 14.8))
        order = {n: i for i, (n, *_r) in enumerate(BOARD)}
        for i, (name, ini, col, pts) in enumerate(BOARD):
            rank = i
            if name == "You":
                rank = lerp(4, 1, climb)
            elif i >= 1:
                rank = i + climb if i < 4 else i
            y = by + 120 + rank * 86
            ki = seg(t, 13.0 + i * 0.07, 13.35 + i * 0.07)
            if ki <= 0:
                continue
            you = name == "You"
            rrect(c, bx + 24, y, bw - 48, 72, 18, paint(mix(BLUE_WASH, WHITE, 0.2) if you else 0x00000000))
            text(c, f"#{int(round(rank)) + 1}", bx + 64, y + 48, font("ExtraBold", 30), BLUE if you else MUTED, "center")
            avatar(c, bx + 138, y + 36, 26, ini, col)
            text(c, name, bx + 182, y + 47, font("Bold", 30), INK)
            p = pts if not you else int(lerp(1180, 1705, climb))
            text(c, f"{p:,} pts", bx + bw - 50, y + 47, font("SemiBold", 28), MUTED, "right")
    c.restore()


# ------------------------------------------------------------------ S6 tools & app (15.5–18)

def s6_tools(c, t):
    if t < 15.4 or t > 18.2:
        return
    out = ease_in_cubic(seg(t, 17.75, 18.05))
    c.save()
    c.translate(0, -out * 300)
    rise_text(c, "Handy tools, built in.", 110, 170, font("ExtraBold", 96), INK, 15.55, t)
    c.restore()
    tiles = [("Result Checker", "SEE, Class 11 & 12 gradesheets", BLUE_BRIGHT, 15.80),
             ("PDF Tools", "Merge, split, compress, convert", CORAL, 16.05),
             ("Android app", "Ask Neby, right in the PDF reader", MINT, 16.30)]
    for i, (title, sub, col, t0) in enumerate(tiles):
        k = seg(t, t0, t0 + 0.45)
        if k <= 0:
            continue
        e = ease_out_back(k, 1.6)
        w, h = 540, 640
        x = 110 + i * (w + 40)
        y = 270 + (1 - e) * 100 + out * 900
        c.save()
        c.translate(x + w / 2, y + h / 2)
        c.scale(lerp(0.85, 1, e), lerp(0.85, 1, e))
        shadow_rrect(c, -w / 2, -h / 2, w, h, 34, alpha=0.13, dy=16, blur=24)
        rrect(c, -w / 2, -h / 2, w, h, 34, paint(WHITE))
        rrect(c, -w / 2 + 20, -h / 2 + 20, w - 40, 380, 24, paint(mix(col, WHITE, 0.88)))
        kk = seg(t, t0 + 0.2, t0 + 1.2)
        if i == 0:
            for j, (g, v) in enumerate([("A+", 1.0), ("A", 0.86), ("B+", 0.72), ("A", 0.88), ("A+", 0.98)]):
                bh = 230 * v * ease_out_back(clamp(kk * 1.4 - j * 0.12), 1.4)
                rrect(c, -w / 2 + 70 + j * 84, -h / 2 + 340 - bh, 54, bh, 10, paint(col if g == "A+" else mix(col, WHITE, 0.45)))
                text(c, g, -w / 2 + 97 + j * 84, -h / 2 + 330 - bh - 12, font("Bold", 24), INK, "center")
            text(c, f"GPA {3.2 + 0.4 * ease_out_cubic(kk):.2f}", 0, -h / 2 + 96, font("ExtraBold", 44), col, "center")
        elif i == 1:
            for j in range(3):
                off = (1 - ease_in_out(clamp(kk * 1.5))) * (j - 1) * 120
                c.save()
                c.translate(off, -h / 2 + 210 + (j - 1) * 18)
                rrect(c, -80, -110, 160, 210, 14, paint(WHITE))
                rrect(c, -80, -110, 160, 210, 14, paint(mix(col, WHITE, 0.4), stroke=3))
                for q in range(4):
                    c.drawLine(-52, -70 + q * 34, 52, -70 + q * 34, paint(mix(col, WHITE, 0.6), stroke=8))
                c.restore()
        else:
            px, py, pw, ph = -110, -h / 2 + 40, 220, 340
            rrect(c, px, py, pw, ph, 30, paint(0xFF101828))
            rrect(c, px + 10, py + 10, pw - 20, ph - 20, 22, paint(WHITE))
            for q in range(6):
                c.drawLine(px + 34, py + 50 + q * 30, px + pw - 34, py + 50 + q * 30, paint(mix(BLUE_WASH, MUTED, 0.3), stroke=7))
            ka = seg(t, 16.7, 17.0)
            sc = 1 - 0.12 * math.sin(math.pi * ka)
            c.save()
            c.translate(px + pw / 2, py + ph - 52)
            c.scale(sc, sc)
            rrect(c, -78, -24, 156, 48, 24, paint(BLUE_BRIGHT))
            text(c, "Ask Neby", 0, 9, font("Bold", 22), WHITE, "center")
            c.restore()
            if 0 < ka < 1:
                c.drawCircle(px + pw / 2, py + ph - 52, 20 + 90 * ka, paint(with_alpha(BLUE_BRIGHT, 0.35 * (1 - ka))))
        text(c, title, -w / 2 + 40, h / 2 - 150, font("ExtraBold", 44), INK)
        text(c, sub, -w / 2 + 40, h / 2 - 96, font("Medium", 26), MUTED)
        c.restore()


# ------------------------------------------------------------------ S7 end card (18–22)

def s7_end(c, t):
    if t < 17.7:
        return
    k = ease_in_out(seg(t, 17.75, 18.15))
    p = paint(WHITE)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(1100, 500), 1500, [0xFF1466F0, BLUE, 0xFF0A2E8A], [0, 0.55, 1]))
    c.drawCircle(480, 760, 2600 * k, p)
    if t < 18.0:
        return
    for j in range(46):
        a = j * 2.399
        kk = seg(t, 18.05 + (j % 7) * 0.03, 19.6 + (j % 5) * 0.1)
        if 0 < kk < 1:
            r = 120 + 950 * ease_out_expo(kk)
            px = 480 + math.cos(a) * r
            py = 560 + math.sin(a) * r * 0.7 + 220 * kk * kk
            col = [AMBER, CORAL, WHITE, MINT, 0xFF9CC3FF][j % 5]
            c.save()
            c.translate(px, py)
            c.rotate(j * 37 + t * 300)
            rrect(c, -8, -3.5, 16, 7, 3.5, paint(with_alpha(col, 1 - kk)))
            c.restore()
    lx = 1230
    fy = math.sin(t * 2.0) * 5
    kt0 = seg(t, 18.3, 18.7)
    if kt0 > 0:
        e = ease_out_back(kt0, 1.7)
        c.save()
        c.translate(lx, 290 + fy)
        c.rotate((1 - e) * -14)
        c.scale(e, e)
        rrect(c, -125, -125 + 18, 250, 250, 62, paint(with_alpha(0xFF001A66, 0.35), blur=26))
        rrect(c, -125, -125, 250, 250, 62, paint(WHITE))
        c.restore()
    logo(c, lx - 5, 290 + fy, 172, seg(t, 18.4, 19.2) * 1.25, t)
    rise_text(c, "NEBians", lx, 545, font("ExtraBold", 140), WHITE, 19.05, t, align="center", stagger=0.04)
    kt = seg(t, 19.45, 19.85)
    if kt > 0:
        f = font("ExtraBold", 50)
        parts = [("Study ", WHITE), ("materials", 0xFFC9BDFF), (". Study ", WHITE), ("mates", 0xFFFFD58A), (".", WHITE)]
        total = sum(f.measureText(s) for s, _ in parts)
        x = lx - total / 2
        for s, col in parts:
            text(c, s, x, 630 + (1 - ease_out_cubic(kt)) * 20, f, with_alpha(col, kt))
            x += f.measureText(s)
    ku = seg(t, 19.8, 20.2)
    if ku > 0:
        e = ease_out_back(ku, 1.8)
        fu = font("Bold", 44)
        url = "nebians.consica.com.np"
        uw = fu.measureText(url) + 84
        c.save()
        c.translate(lx, 745)
        c.scale(e, e)
        rrect(c, -uw / 2, -44, uw, 88, 44, paint(WHITE))
        text(c, url, 0, 16, fu, BLUE, "center")
        c.restore()
    ks = seg(t, 20.2, 20.6)
    if ks > 0:
        text(c, "Free on the web  ·  Android app on Google Play", lx, 850, font("Medium", 34),
             with_alpha(0xFFC9D8FF, ks), "center")
        text(c, "Class 8 to Masters  ·  Notes, papers, books and a community", lx, 905, font("Medium", 28),
             with_alpha(0xFF9FB8F0, ks), "center")
    for (sx, sy, d) in [(1010, 150, 0.0), (1460, 200, 0.15), (1500, 420, 0.25), (950, 430, 0.35)]:
        kk = seg(t, 19.1 + d, 19.8 + d)
        if 0 < kk < 1:
            star(c, sx, sy, 24 * math.sin(math.pi * kk), WHITE)


# ------------------------------------------------------------------ Neby's path

def neby_path(t):
    """(x, y, size, rot, sx, sy) for Neby across the film, with hops and squash."""
    def hop(a, b, p0, p1, h, s0, s1, lean=8):
        k = seg(t, a, b)
        e = ease_in_out(k)
        st = math.sin(math.pi * k)
        return (lerp(p0[0], p1[0], e), lerp(p0[1], p1[1], e) - h * st, lerp(s0, s1, e),
                lean * st * (1 if p1[0] >= p0[0] else -1), 1 - 0.06 * st, 1 + 0.10 * st)

    def land(after, base):
        u = t - after
        x, y, s, r, sx, sy = base
        if 0 < u < 0.7:
            q = 0.13 * math.exp(-u * 8) * math.cos(u * 24)
            sx, sy = 1 + q, 1 - q
        return (x, y, s, r, sx, sy)

    A = (960, 600)
    if t < 2.15:
        return None
    if t < 2.6:
        k = ease_out_back(seg(t, 2.15, 2.55), 1.8)
        return (960, 600, 380 * k, 0, 1, 1)
    if t < 2.9:
        return land(2.55, (960, 600, 380, 0, 1, 1))
    if t < 3.3:
        return hop(2.9, 3.3, A, (520, 580), 160, 380, 360)
    if t < 4.85:
        return land(3.3, (520, 580, 360, 0, 1, 1))
    if t < 5.35:
        return hop(4.85, 5.35, (520, 580), (1640, 830), 260, 360, 300)
    if t < 8.85:
        return land(5.35, (1640, 830, 300, 0, 1, 1))
    if t < 9.35:
        return hop(8.85, 9.35, (1640, 830), (1500, 930), 160, 300, 240)
    if t < 12.35:
        return land(9.35, (1500, 930, 240, 0, 1, 1))
    if t < 12.85:
        return hop(12.35, 12.85, (1500, 930), (490, 930), 240, 240, 240)
    if t < 15.35:
        return land(12.85, (490, 930, 240, 0, 1, 1))
    if t < 15.85:
        return hop(15.35, 15.85, (490, 930), (1690, 175), 200, 240, 170)
    if t < 17.75:
        return land(15.85, (1690, 175, 170, 0, 1, 1))
    if t < 18.05:
        k = ease_in_out(seg(t, 17.75, 18.05))
        return (lerp(1690, 480, k), lerp(175, 560, k) - 120 * math.sin(math.pi * k), lerp(170, 300, k), 0, 1, 1)
    k = ease_out_back(seg(t, 18.05, 18.5), 1.5)
    base = (480, 560 + math.sin(t * 2.4) * 10, lerp(300, 520, k), 0, 1, 1)
    hopp = 0.0
    if 18.0 < t < 18.9:
        hopp = 90 * abs(math.sin((t - 18.0) / 0.45 * math.pi))
    x, y, s, r, sx, sy = land(18.5, base)
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
