"""The scenes. Each takes a Painter and draws one picture; build.py runs every scene in every look."""
import math

import props as X
from painter import circle_d


# ---------------------------------------------------------------- profile covers, 3:1
def cover_member(p):
    p.sky("dusk")
    p.stars(40, p.h * 0.35)
    p.glow(1230, 120, 150, "a", 0.8); p.circle(1230, 120, 38, "a")
    X.mountain_range(p, 380, [(150, 210, 230), (480, 160, 220), (880, 250, 290), (1300, 180, 250)])
    X.prayer_flags(p, -10, 210, 560, 300, 12, 40)
    p.ground(360)
    hx, hy, hr, top = X.soul(p, 760, 520, 290, lean=-8)
    p.glow(880, 400, 110, "a", 0.75)
    X.open_book(p, 880, 415, 170, tilt=-6)


def cover_verified(p):
    p.sky("dawn")
    X.mountain_range(p, 400, [(300, 180, 260), (760, 230, 280), (1250, 170, 260)])
    p.ground(380)
    p.glow(1020, 175, 230, "a", 0.9)
    X.rosette(p, 1020, 160, 78)
    X.soul(p, 520, 520, 260, lean=14, mood="smile")
    for k, (x, y) in enumerate(((1200, 80), (860, 70), (1300, 250), (780, 260))):
        p.s.path(__import__("kit").star_path(x, y, 14, 3.5), p.c("e"))


def cover_tutor(p):
    p.sky("day")
    p.glow(260, 110, 170, "a", 0.6)
    X.mountain_range(p, 390, [(200, 150, 250), (640, 200, 260), (1100, 160, 300), (1450, 210, 220)], snow=True)
    p.ground(380)
    X.numbers(p, 860, 120, 56)
    hx, hy, hr, top = X.soul(p, 520, 520, 300, body="d", head="a", lean=10)
    X.open_book(p, 640, 300, 130, tilt=-18)
    X.soul(p, 1080, 520, 150, body="b", head="h", lean=-10, glow=False, arm=False)
    X.soul(p, 1270, 520, 120, body="g", head="h", lean=-6, glow=False, arm=False)


def cover_institution(p):
    p.sky("day")
    p.glow(1250, 110, 150, "a", 0.6); p.circle(1250, 110, 36, "a")
    X.mountain_range(p, 380, [(150, 190, 260), (620, 240, 300), (1050, 170, 260), (1420, 200, 240)])
    p.ground(390)
    X.school(p, 760, 455, 360)
    for x, a in ((420, -95), (460, -80), (1080, -100), (1120, -75)):
        X.sprig(p, x, 470, 120, a, 5)
    X.stem_flower(p, 540, 470, 70, -100, "f")
    X.stem_flower(p, 990, 470, 60, -80, "a")


def cover_moderator(p):
    p.sky("night")
    p.glow(1280, 100, 120, "e", 0.5); p.circle(1280, 100, 34, "e")
    X.mountain_range(p, 380, [(200, 200, 250), (650, 160, 260), (1100, 230, 300)], snow=True)
    p.ground(360)
    for k, (x, w) in enumerate(((880, 70), (980, 60), (1080, 80), (1200, 64), (1310, 72))):
        y = 470 - (k % 2) * 14
        p.form(X.poly((x - w / 2, y), (x - w / 2, y - w * 0.6), (x, y - w), (x + w / 2, y - w * 0.6), (x + w / 2, y)), "e" if k % 2 else "h", w, shade=False)
        p.s.rect(x - w * 0.12, y - w * 0.4, w * 0.24, w * 0.22, p.c("a"))
    hx, hy, hr, top = X.soul(p, 460, 520, 300, body="c", head="a", lean=8)
    X.lantern(p, 650, 300, 90)


def cover_admin(p):
    p.sky("dusk")
    X.mountain_range(p, 390, [(250, 170, 260), (700, 230, 300), (1200, 190, 280)])
    p.ground(380)
    p.glow(980, 220, 220, "a", 0.8)
    X.key(p, 980, 220, 210, -28)
    X.shield(p, 1260, 300, 120, "c")
    X.soul(p, 520, 520, 270, body="d", head="a", lean=12)


def cover_bot(p):
    p.sky("night")
    X.planet(p, 1250, 150, 48, "b", "a")
    X.atom(p, 300, 170, 80)
    X.mountain_range(p, 420, [(150, 120, 240), (600, 160, 260), (1100, 130, 300), (1450, 150, 220)], snow=False)
    p.ground(410)
    X.orb(p, 760, 230, 120)
    for k, (x, y) in enumerate(((560, 120), (980, 100), (1040, 330), (520, 330))):
        p.s.path(__import__("kit").star_path(x, y, 12, 3), p.c("a"))


COVERS = {"member": cover_member, "verified": cover_verified, "tutor": cover_tutor, "institution": cover_institution,
          "moderator": cover_moderator, "admin": cover_admin, "bot": cover_bot}


# ---------------------------------------------------------------- resource banners, 2:1
def _plant_corners(p, ground):
    X.sprig(p, 70, ground, 200, -70, 6)
    X.sprig(p, 140, ground, 140, -100, 4, "leaf2")
    X.sprig(p, p.w - 70, ground, 210, -112, 6)
    X.sprig(p, p.w - 150, ground, 130, -80, 4, "leaf2")


def banner_physics(p):
    p.sky("dusk")
    p.stars(30, p.h * 0.5)
    X.planet(p, 930, 170, 70, "b", "a")
    X.prism(p, 560, 360, 230)
    p.circle(200, 120, 3, "e")


def banner_chemistry(p):
    p.sky("day")
    X.atom(p, 880, 200, 120)
    X.flask(p, 480, 520, 300, "g")
    X.flask(p, 700, 520, 200, "f", bubbles=True)
    _plant_corners(p, 600)


def banner_math(p):
    p.sky("day")
    X.numbers(p, 760, 140, 70, "π √ ∑ ÷ ∞ =")
    X.geometry(p, 420, 340, 330)


def banner_biology(p):
    p.sky("day")
    X.leaf_cell(p, 820, 300, 150)
    X.microscope(p, 420, 540, 360)
    X.butterfly(p, 1010, 140, 70)
    _plant_corners(p, 600)


def banner_science(p):
    p.sky("night")
    X.planet(p, 880, 170, 64, "b", "a")
    p.glow(1050, 300, 90, "a", 0.7); p.circle(1050, 300, 22, "a")
    X.mountain_range(p, 560, [(150, 160, 250), (600, 110, 260), (1050, 180, 260)], snow=True)
    p.ground(540)
    X.telescope(p, 420, 540, 240)


def banner_language(p):
    p.sky("day")
    X.stem_flower(p, 300, 560, 220, -110, "b")
    X.stem_flower(p, 900, 560, 240, -60, "a")
    X.stem_flower(p, 980, 560, 150, -40, "c")
    X.sprig(p, 380, 600, 230, -80, 6)
    X.sprig(p, 820, 600, 250, -100, 6, "leaf2")
    X.open_book(p, 600, 360, 300, tilt=-4)
    X.butterfly(p, 720, 170, 74)
    for k, (g, x, y) in enumerate((("A", 300, 200), ("अ", 420, 140), ("क", 860, 290), ("a", 230, 330))):
        p.s.add('<text x="%d" y="%d" font-family="Georgia, \'Noto Serif Devanagari\', serif" font-size="%d" fill="%s" opacity="0.85">%s</text>' % (x, y, 58 - k * 6, p.c(("d", "b", "d", "g")[k]), g))


def banner_computing(p):
    p.sky("plain")
    X.laptop(p, 560, 500, 380)
    X.bubble(p, 860, 190, 170, 90, "e", tail=-1)
    X.atom(p, 980, 420, 70, "a", "c")
    _plant_corners(p, 600)


def banner_commerce(p):
    p.sky("day")
    X.coins_chart(p, 520, 520, 420)
    _plant_corners(p, 600)


def banner_social(p):
    p.sky("dawn")
    X.mountain_range(p, 520, [(160, 200, 260), (560, 150, 260), (1000, 220, 280)], snow=True)
    X.prayer_flags(p, -10, 130, 1210, 160, 18, 50)
    p.ground(500)
    X.globe(p, 600, 330, 140)


def banner_health(p):
    p.sky("day")
    X.heart_pulse(p, 600, 300, 210)
    X.stem_flower(p, 260, 560, 200, -105, "f")
    X.stem_flower(p, 960, 560, 200, -75, "a")
    _plant_corners(p, 600)


def banner_exam(p):
    p.sky("day")
    X.paper(p, 360, 120, 300, 390, -6)
    X.pencil(p, 560, 560, 260, -62)
    X.clock(p, 880, 220, 110)
    X.cap(p, 860, 450, 200)


def banner_general(p):
    p.sky("dusk")
    p.stars(20, p.h * 0.4)
    X.upright_books(p, 220, 520, 330, 7)
    X.book_stack(p, 760, 520, 300, 4)
    X.lamp_diyo(p, 1000, 515, 110)
    p.solid(X.rrect_d(120, 520, 980, 26, 8), "ink" if p.look == "riso" else "brown")


BANNERS = {"physics": banner_physics, "chemistry": banner_chemistry, "math": banner_math, "biology": banner_biology,
           "science": banner_science, "language": banner_language, "computing": banner_computing, "commerce": banner_commerce,
           "social": banner_social, "health": banner_health, "exam": banner_exam, "general": banner_general}


# ---------------------------------------------------------------- onboarding, 3:4
def ob_welcome(p):
    p.sky("dawn")
    p.glow(450, 300, 300, "a", 0.7)
    X.mountain_range(p, 820, [(120, 300, 320), (480, 420, 360), (820, 330, 320)])
    X.prayer_flags(p, -10, 560, 910, 620, 14, 60)
    p.ground(800)
    X.orb(p, 450, 640, 130)


def ob_class(p):
    """Four stacks for Class 8, 10, 11 and 12, each taller than the last, Neby on the top one."""
    p.sky("day")
    p.glow(700, 260, 220, "a", 0.6)
    tops = []
    for k, (x, n) in enumerate(((150, 3), (350, 5), (550, 7), (750, 9))):
        X.book_stack(p, x, 1060, 180, n)
        tops.append(1060 - sum(180 * (0.16 + 0.03 * (j % 2)) for j in range(n)))
    X.orb(p, 750, tops[-1] - 92, 88, mood="smile", ring=False)
    p.solid(X.rrect_d(40, 1060, 820, 36, 12), "ink" if p.look == "riso" else "brown")
    for x, y, r in ((160, 260, 16), (420, 180, 12), (300, 420, 10)):
        p.s.path(__import__("kit").star_path(x, y, r, r * 0.25), p.c("a"))


def ob_subjects(p):
    """The subjects circling Neby: a flask, an atom, the globe, a book, geometry and a laptop."""
    p.sky("plain")
    cx, cy = 450, 620
    p.line(circle_d(cx, cy, 320), "c", 3, op=0.55)
    p.line(circle_d(cx, cy, 200), "c", 2, op=0.35)
    X.orb(p, cx, cy, 120, ring=False)
    X.flask(p, cx + 320, cy + 110, 190, "g")
    X.atom(p, cx - 330, cy - 40, 105)
    X.globe(p, cx + 30, cy - 330, 85)
    X.open_book(p, cx - 20, cy + 330, 210)
    X.geometry(p, cx - 330, cy + 250, 130)
    X.laptop(p, cx + 260, cy - 200, 170)


def ob_study(p):
    p.sky("night")
    p.glow(700, 160, 90, "e", 0.6); p.circle(700, 160, 30, "e")
    p.solid(X.rrect_d(80, 900, 740, 34, 10), "ink" if p.look == "riso" else "brown")
    X.soul(p, 380, 1200, 420, body="c", head="a", lean=10)
    X.lamp_diyo(p, 660, 895, 100)
    X.open_book(p, 520, 860, 170, tilt=-4)
    X.book_stack(p, 180, 900, 130, 3)


def ob_community(p):
    p.sky("day")
    X.mountain_range(p, 860, [(150, 260, 300), (520, 330, 340), (860, 280, 300)])
    p.ground(840)
    X.soul(p, 280, 1200, 280, body="b", head="h", lean=10, glow=False)
    X.soul(p, 640, 1200, 300, body="c", head="a", lean=-12)
    X.bubble(p, 300, 470, 220, 110, "e", tail=-1)
    X.bubble(p, 630, 360, 200, 100, "page", tail=1)
    p.circle(470, 250, 10, "a"); p.circle(500, 220, 6, "b")


def ob_ready(p):
    p.sky("dawn")
    p.glow(450, 420, 330, "a", 0.9)
    X.mountain_range(p, 860, [(150, 300, 320), (480, 380, 360), (830, 300, 320)])
    p.ground(850)
    X.rosette(p, 450, 380, 95)
    X.soul(p, 450, 1220, 340, lean=0, mood="smile")
    for x, y, r in ((200, 250, 18), (720, 220, 14), (760, 480, 10), (140, 520, 12)):
        p.s.path(__import__("kit").star_path(x, y, r, r * 0.25), p.c("e"))


ONBOARDING = {"welcome": ob_welcome, "choose-class": ob_class, "subjects": ob_subjects, "study": ob_study,
              "community": ob_community, "ready": ob_ready}


# ---------------------------------------------------------------- empty states, square
def _empty_base(p):
    p.sky("plain")
    p.glow(400, 430, 330, "a", 0.35)
    p.form(circle_d(400, 430, 250), "h", 500, shade=False)


def empty_offline(p):
    _empty_base(p)
    X.cloud(p, 400, 420, 360, "c" if p.look == "flat" else "e")
    X.rain(p, 400, 470, 300)


def empty_search(p):
    _empty_base(p)
    X.magnifier(p, 370, 380, 130)


def empty_bookmarks(p):
    _empty_base(p)
    X.book_stack(p, 400, 600, 300, 3)
    X.ribbon_bookmark(p, 470, 200, 70, 200)


def empty_downloads(p):
    _empty_base(p)
    X.tray(p, 400, 470, 320)


def empty_notifications(p):
    _empty_base(p)
    X.bell(p, 400, 420, 300)


def empty_inbox(p):
    _empty_base(p)
    X.envelope(p, 400, 440, 330)


def empty_error(p):
    _empty_base(p)
    X.orb(p, 400, 430, 140, mood="o", ring=False)


def empty_done(p):
    _empty_base(p)
    X.rosette(p, 400, 380, 120)


EMPTY = {"offline": empty_offline, "search": empty_search, "bookmarks": empty_bookmarks, "downloads": empty_downloads,
         "notifications": empty_notifications, "inbox": empty_inbox, "error": empty_error, "done": empty_done}


# ---------------------------------------------------------------- backgrounds
def bg_auth(p):
    p.sky("dusk")
    p.stars(80, p.h * 0.45)
    p.glow(p.w * 0.5, p.h * 0.36, 380, "a", 0.8)
    X.open_book(p, p.w * 0.5, p.h * 0.37, 300)
    X.mountain_range(p, p.h * 0.78, [(80, 380, 360), (560, 520, 420), (1000, 420, 380)])
    p.ground(p.h * 0.76)
    X.soul(p, p.w * 0.5, p.h + 40, 520, lean=0, mood="smile")


def bg_landscape(p):
    p.sky("dusk")
    p.stars(50, p.h * 0.4)
    p.glow(1180, 220, 220, "a", 0.8); p.circle(1180, 220, 56, "a")
    X.mountain_range(p, 640, [(120, 330, 360), (620, 420, 420), (1150, 360, 380), (1550, 300, 300)])
    X.prayer_flags(p, -10, 420, 760, 520, 14, 60)
    p.ground(620)


def bg_glow(p):
    p.sky("plain")
    p.glow(420, 320, 420, "a", 0.8)
    p.glow(1180, 600, 380, "b", 0.7)
    p.glow(900, 150, 260, "f", 0.5)


def bg_night(p):
    p.sky("night")
    p.stars(140, p.h)
    X.planet(p, 1250, 220, 70, "b", "a")
    p.glow(380, 640, 300, "c", 0.6)


BACKGROUNDS = {"auth": (bg_auth, 1080, 1920), "landscape": (bg_landscape, 1600, 900), "glow": (bg_glow, 1600, 900), "night": (bg_night, 1600, 900)}

SETS = {
    "covers": (COVERS, 1500, 500, "Profile covers", "One per account type, 3:1"),
    "banners": (BANNERS, 1200, 600, "Resource banners", "One per subject family, 2:1"),
    "onboarding": (ONBOARDING, 900, 1200, "Onboarding scenes", "The first-run steps, 3:4"),
    "empty": (EMPTY, 800, 800, "Empty states", "Offline, nothing found, nothing saved yet, 1:1"),
}
