import json
import os

import numpy as np
from manim import (
    DOWN, LEFT, ORIGIN, RIGHT, UL, UP, UR, DL, DR, PI, TAU,
    AnimationGroup, Arc, Circle, Create, Dot, FadeIn, FadeOut, GrowFromCenter, Indicate, LaggedStart,
    Line, Rectangle, RoundedRectangle, Scene, Succession, Transform, VGroup, ValueTracker, Write,
    always_redraw, config, rate_functions, Group,
)

from . import sfx
from . import theme as th
from .neby import Neby
from .text import T, is_deva, ne_num, para
from .voice import speak

STR = {
    "en": {
        "class": "Class", "unit": "Unit", "part": "Part", "pause": "PAUSE & THINK", "recap": "Quick recap",
        "roadmap": "In this lesson", "tip": "Exam tip", "key": "Key idea", "example": "Worked example",
        "answer": "Answer", "next": "Up next", "brand": "NEBians", "url": "nebians.consica.com.np",
        "free": "Free notes, papers and lessons", "careful": "Careful", "remember": "Remember",
    },
    "ne": {
        "class": "कक्षा", "unit": "एकाइ", "part": "भाग", "pause": "रोकिनुहोस् र सोच्नुहोस्", "recap": "छोटो पुनरावलोकन",
        "roadmap": "यस पाठमा", "tip": "परीक्षा सुझाव", "key": "मुख्य कुरा", "example": "उदाहरण",
        "answer": "उत्तर", "next": "अर्को पाठ", "brand": "नेबियन्स", "url": "निःशुल्क नोट, प्रश्नपत्र र पाठ",
        "free": "निःशुल्क नोट, प्रश्नपत्र र पाठ", "careful": "सावधान", "remember": "सम्झनुहोस्",
    },
}

SUBJECT_NAMES = {
    "en": {"phy": "Physics", "chem": "Chemistry", "bio": "Biology", "math": "Mathematics", "cs": "Computer Science",
           "eng": "English", "sci": "Science", "omath": "Optional Mathematics", "acc": "Accountancy",
           "eco": "Economics", "qbank": "Question Bank", "qbankc": "Commerce Question Bank"},
    "ne": {"nep": "नेपाली", "soc": "सामाजिक अध्ययन", "health": "स्वास्थ्य, शारीरिक तथा सिर्जनात्मक कला"},
}

LOOKS = {"phy": "scientist", "chem": "scientist", "bio": "scientist", "sci": "scientist", "nep": "topi",
         "soc": "topi", "health": "topi", "cs": "headphones"}


class Narration:
    def __init__(self, scene, text, gap):
        self.scene, self.text, self.gap = scene, text, gap

    def __enter__(self):
        s = self.scene
        wav, self.dur, cues = speak(self.text, s.VOICE)
        self.start = s.renderer.time
        s.add_sound(wav, gain=0)
        if not cues:
            cues = [[0, self.dur, self.text]]
        self.cues = cues
        for a, b, t in cues:
            s._subs.append((self.start + a, self.start + min(b, self.dur), t))
        if s._talker is not None and s._talker in s.mobjects:
            s._talker.set_state("talk")
        return self

    @property
    def left(self):
        return max(0.0, self.start + self.dur - self.scene.renderer.time)

    def frac(self, k):
        return max(0.3, self.dur * k)

    def at(self, phrase):
        """Seconds into this line where `phrase` is spoken: found in its sentence cue, interpolated by characters."""
        for a, b, t in self.cues:
            i = t.find(phrase)
            if i >= 0:
                return a + (min(b, self.dur) - a) * i / max(1, len(t))
        i = self.text.find(phrase)
        if i < 0:
            raise ValueError(f"cue {phrase!r} is not in the narration")
        return self.dur * i / max(1, len(self.text))

    def until(self, phrase, lead=0.15):
        """Hold until just before `phrase` is spoken, so the next animation lands on the word."""
        self.scene.hold(self.start + self.at(phrase) - lead - self.scene.renderer.time)

    def __exit__(self, exc_type, *a):
        if exc_type is not None:
            return False
        s = self.scene
        rem = self.left
        if rem > 0.02:
            s.wait(rem)
        if s._talker is not None and s._talker in s.mobjects:
            s._talker.set_state("idle")
        if self.gap > 0:
            s.wait(self.gap)
        return False


class Lesson(Scene):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 1
    TITLE = "Title"
    SUBTITLE = ""
    LANG = "en"
    VOICE = None
    SECTIONS = []
    NEXT = ""
    MOOD = "calm"

    def setup(self):
        self.camera.background_color = th.BG
        self.VOICE = self.VOICE or ("ne" if self.LANG == "ne" else "en")
        self.S = STR[self.LANG]
        self.color = th.SUBJECT_COLORS.get(self.SUBJECT, th.ACCENT)
        self.look = LOOKS.get(self.SUBJECT, "graduate")
        self._subs = []
        self._chapters = [[0.0, "Introduction"]]
        self._talker = None
        self._sec = -1
        self.hud = None
        self._add_backdrop()

    def construct(self):
        self.lesson()

    def lesson(self):
        raise NotImplementedError

    def parts(self, *fns):
        only = os.environ.get("LESSON_ONLY")
        only = {int(x) for x in only.split(",")} if only else None
        for i, f in enumerate(fns):
            if only is not None and i not in only:
                continue
            if i > 0 and self.hud is None and fns[-1] is not f:
                self.build_hud()
            f()

    def num(self, x):
        return ne_num(x) if self.LANG == "ne" else str(x)

    def subject_name(self):
        return SUBJECT_NAMES[self.LANG].get(self.SUBJECT, self.SUBJECT)

    def hold(self, t):
        if t > 1 / 30:
            self.wait(t)

    def say(self, text, gap=0.25):
        return Narration(self, text, gap)

    def sfx(self, name, gain=-6, delay=0.0):
        self.add_sound(sfx.get(name), time_offset=delay, gain=gain)

    def neby(self, state="idle", height=2.0):
        if self.LANG == "ne" and state == "wave":
            state = "namaste"
        return Neby(state, self.look, height=height)

    def _add_backdrop(self):
        w, h = config.frame_width, config.frame_height
        dots = VGroup()
        for x in np.arange(-w / 2 + 0.4, w / 2, 0.8):
            for y in np.arange(-h / 2 + 0.4, h / 2, 0.8):
                dots.add(Dot([x, y, 0], radius=0.012, color=th.FAINT, fill_opacity=0.55))
        glow = VGroup(*[
            Circle(radius=r, stroke_width=0, fill_color=th.BRAND, fill_opacity=0.018).move_to([-4.5, 2.6, 0])
            for r in np.linspace(1.2, 6.5, 9)
        ])
        glow2 = VGroup(*[
            Circle(radius=r, stroke_width=0, fill_color=self.color, fill_opacity=0.012).move_to([5.0, -3.0, 0])
            for r in np.linspace(1.0, 5.5, 8)
        ])
        self.add(dots, glow, glow2)

    def clear_stage(self, keep=(), run_time=0.6):
        keep = set(keep) | {self.hud} if self.hud else set(keep)
        base = self.mobjects[:3]
        out = [m for m in self.mobjects if m not in keep and m not in base]
        if out:
            self.play(*[FadeOut(m) for m in out], run_time=run_time)

    def title_card(self):
        c = self.color
        sub = self.subject_name()
        top = T(f"{self.S['class']} {self.num(self.GRADE)}  ·  {sub}", size=30, color=c, weight="SEMIBOLD")
        unit = T(f"{self.S['unit']} {self.num(self.UNIT)}", size=26, color=th.MUTED)
        big = T(self.num(f"{self.UNIT:02d}"), size=300, color=c, weight="BOLD", display=True).set_opacity(0.10)
        title = T(self.TITLE, size=74 if len(self.TITLE) < 24 else 58, color=th.INK, weight="BOLD", display=True)
        words, wrapped = self.TITLE.split(), False
        if title.width > 12 * 58 / 46 and len(words) > 1:
            # a title that would shrink below ~46 pt on one line goes on two balanced lines instead
            k = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
            title = VGroup(*[T(" ".join(w), size=58, color=th.INK, weight="BOLD", display=True)
                             for w in (words[:k], words[k:])]).arrange(DOWN, buff=0.22)
            wrapped = True
        if title.width > 12:
            title.scale_to_fit_width(12)
        subtitle = T(self.SUBTITLE, size=30, color=th.BODY) if self.SUBTITLE else VGroup()
        block = VGroup(top, title, subtitle).arrange(DOWN, buff=0.35)
        if wrapped:  # keep the subtitle where a one-line title leaves it, clear of the bars
            block.shift(UP * (title.height - 0.75) / 2)
        unit.next_to(top, UP, buff=0.25)
        big.move_to(block).shift(UP * 0.2)
        bars = VGroup(*[
            Rectangle(width=config.frame_width * 1.4, height=0.07 + 0.05 * i, stroke_width=0,
                      fill_color=col, fill_opacity=0.85).rotate(-0.18).shift(DOWN * (2.4 + 0.33 * i))
            for i, col in enumerate([c, th.ACCENT, th.AMBER])
        ])
        nb = self.neby("wave" if self.LANG != "ne" else "namaste", height=1.9).to_corner(DR, buff=0.5)
        self.sfx("riser", gain=-10)
        self.play(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_expo).shift(RIGHT * 0.01) for b in bars], lag_ratio=0.1),
                  *[FadeIn(b, shift=LEFT * 6) for b in bars], run_time=0.9)
        self.sfx("impact", gain=-8)
        self.play(FadeIn(big, scale=1.4), FadeIn(unit, shift=DOWN * 0.2), FadeIn(top, shift=UP * 0.3), run_time=0.7)
        self.play(Write(title), run_time=1.3)
        if self.SUBTITLE:
            self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.5)
        self.sfx("pop")
        self.add(nb)
        self.play(FadeIn(nb, scale=0.4, rate_func=rate_functions.ease_out_back), run_time=0.5)
        return VGroup(big, unit, top, title, subtitle, bars), nb

    def end_title(self, g, nb):
        self.sfx("whoosh", gain=-10)
        self.play(FadeOut(g, shift=UP * 0.6), FadeOut(nb, shift=DOWN), run_time=0.7)
        self.remove(nb)
        self.build_hud()

    def build_hud(self):
        c = self.color
        chip_dot = Dot(radius=0.07, color=c)
        chip_txt = T(f"{self.subject_name()} {self.num(self.GRADE)}  ·  {self.S['unit']} {self.num(self.UNIT)}  ·  {self.TITLE}",
                     size=17, color=th.MUTED)
        chip = VGroup(chip_dot, chip_txt).arrange(RIGHT, buff=0.15).to_corner(UL, buff=0.32)
        n = max(1, len(self.SECTIONS))
        total_w = config.frame_width - 1.0
        seg_w = total_w / n
        track = VGroup()
        for i in range(n):
            r = RoundedRectangle(corner_radius=0.025, width=seg_w - 0.08, height=0.05, stroke_width=0,
                                 fill_color=th.FAINT, fill_opacity=0.7)
            r.move_to([-total_w / 2 + seg_w * (i + 0.5), -config.frame_height / 2 + 0.22, 0])
            track.add(r)
        self.hud_track = track
        self.hud_sec = VGroup()
        self.hud = VGroup(chip, track, self.hud_sec)
        self.play(FadeIn(self.hud), run_time=0.5)

    def roadmap(self, narration=None):
        head = T(self.S["roadmap"], size=40, color=self.color, weight="BOLD", display=True).to_edge(UP, buff=0.9)
        rows = VGroup()
        for i, s in enumerate(self.SECTIONS):
            num = T(self.num(f"{i + 1:02d}"), size=26, color=self.color, weight="BOLD", display=True)
            txt = T(s, size=28, color=th.INK)
            rows.add(VGroup(num, txt).arrange(RIGHT, buff=0.35))
        if len(rows) > 10:
            half = (len(rows) + 1) // 2
            cols = VGroup(VGroup(*rows[:half]).arrange(DOWN, aligned_edge=LEFT, buff=0.26),
                          VGroup(*rows[half:]).arrange(DOWN, aligned_edge=LEFT, buff=0.26))
            cols.arrange(RIGHT, aligned_edge=UP, buff=0.8)
            if cols.width > 10.2:
                cols.scale_to_fit_width(10.2)
            if cols.height > 5.4:
                cols.scale_to_fit_height(5.4)
            cols.next_to(head, DOWN, buff=0.5).shift(LEFT * 0.9)
        else:
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26)
            if rows.height > 5.4:
                rows.scale_to_fit_height(5.4)
            rows.next_to(head, DOWN, buff=0.5).shift(LEFT * 1.2)
        nb = self.neby("read", height=2.0).to_corner(DR, buff=0.7)
        self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.5)
        self.add(nb)
        self.play(FadeIn(nb, scale=0.5), run_time=0.4)
        with self.say(narration or "") if narration else _Null() as v:
            per = max(0.25, (v.dur * 0.8 if narration else 2.5) / max(1, len(rows)))
            for r in rows:
                self.sfx("tick", gain=-12)
                self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=min(0.45, per))
                self.hold(per - 0.45)
        self.play(FadeOut(VGroup(head, rows)), FadeOut(nb), run_time=0.5)
        self.remove(nb)

    def section(self, i, narration=None):
        self._sec = i
        self._chapters.append([round(self.renderer.time, 2), self.SECTIONS[i]])
        c = self.color
        title = self.SECTIONS[i]
        wipe = Rectangle(width=config.frame_width + 1, height=config.frame_height + 1, stroke_width=0,
                         fill_color=th.BG2, fill_opacity=1).shift(LEFT * (config.frame_width + 1))
        lab = T(f"{self.S['part']} {self.num(i + 1)}", size=28, color=c, weight="SEMIBOLD")
        tt = T(title, size=62 if len(title) < 28 else 48, color=th.INK, weight="BOLD", display=True)
        if tt.width > 12.4:
            tt.scale_to_fit_width(12.4)
        line = Line(LEFT * 2, RIGHT * 2, color=c, stroke_width=6)
        g = VGroup(lab, tt, line).arrange(DOWN, buff=0.35)
        self.clear_stage(run_time=0.4)
        self.sfx("whoosh", gain=-9)
        self.play(wipe.animate.shift(RIGHT * (config.frame_width + 1)), run_time=0.5, rate_func=rate_functions.ease_in_out_cubic)
        self.play(FadeIn(lab, shift=UP * 0.2), Write(tt), Create(line), run_time=0.9)
        if self.hud is not None and i < len(self.hud_track):
            seg = self.hud_track[i]
            fill = seg.copy().set_fill(c, opacity=1)
            self.hud_sec.add(fill)
            self.add(self.hud)
            self.play(GrowFromCenter(fill), run_time=0.4)
        if narration:
            with self.say(narration):
                pass
        else:
            self.wait(0.8)
        self.sfx("whoosh_down", gain=-12)
        self.play(FadeOut(g, shift=UP * 0.4), wipe.animate.shift(RIGHT * (config.frame_width + 1)), run_time=0.55)
        self.remove(wipe)

    def panel(self, w, h, color=None, fill=th.PANEL, opacity=0.92):
        return RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=color or th.PANEL_EDGE,
                                stroke_width=2, fill_color=fill, fill_opacity=opacity)

    def callout(self, kind, body, width=10.5, size=30):
        colors = {"key": self.color, "tip": th.AMBER, "careful": th.CORAL, "remember": th.MINT}
        col = colors.get(kind, self.color)
        head = T(self.S.get(kind, kind), size=24, color=col, weight="BOLD")
        txt = para(body, width=width - 0.8, size=size, color=th.INK) if isinstance(body, str) else body
        inner = VGroup(head, txt).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        box = self.panel(inner.width + 0.8, inner.height + 0.7, color=col)
        bar = Rectangle(width=0.09, height=box.height - 0.3, stroke_width=0, fill_color=col, fill_opacity=1)
        bar.move_to(box.get_left() + RIGHT * 0.2)
        inner.move_to(box).shift(RIGHT * 0.12)
        return VGroup(box, bar, inner)

    def tip(self, body, narration, state="think", width=9.0):
        box = self.callout("tip", body, width=width)
        nb = self.neby(state, height=2.0)
        g = Group(box, nb).arrange(RIGHT, buff=0.4).move_to(ORIGIN)
        self.sfx("pop")
        self.add(nb)
        self.play(FadeIn(box, shift=UP * 0.3), FadeIn(nb, scale=0.5), run_time=0.6)
        self._talker = nb
        with self.say(narration):
            pass
        self._talker = None
        self.play(FadeOut(box), FadeOut(nb), run_time=0.5)
        self.remove(nb)

    def quiz(self, question, options, answer, intro, reveal, think=5):
        self.clear_stage()
        head = T(self.S["pause"], size=28, color=th.AMBER, weight="BOLD").to_edge(UP, buff=0.75)
        q = para(question, width=11.5, size=32, color=th.INK) if isinstance(question, str) else question
        q.next_to(head, DOWN, buff=0.35)
        letters = ["क", "ख", "ग", "घ"] if self.LANG == "ne" else ["A", "B", "C", "D"]
        cards = VGroup()
        for i, o in enumerate(options):
            lab = T(letters[i], size=26, color=self.color, weight="BOLD")
            body = o if not isinstance(o, str) else T(o, size=28, color=th.INK)
            if body.width > 4.4:
                body.scale_to_fit_width(4.4)
            row = VGroup(lab, body).arrange(RIGHT, buff=0.3)
            box = self.panel(5.6, max(1.0, row.height + 0.45))
            row.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.35)
            cards.add(VGroup(box, row))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.4, 0.3))
        cards.next_to(q, DOWN, buff=0.5)
        if cards.get_bottom()[1] < -3.4:
            cards.shift(UP * (-3.4 - cards.get_bottom()[1]))
        nb = self.neby("think", height=1.5).to_corner(DR, buff=0.45)
        self.sfx("bell", gain=-14)
        self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(q, shift=UP * 0.2), run_time=0.6)
        self.add(nb)
        with self.say(intro):
            self.play(LaggedStart(*[FadeIn(cd, shift=UP * 0.25) for cd in cards], lag_ratio=0.15), FadeIn(nb), run_time=1.2)
        ring_bg = Circle(radius=0.42, stroke_color=th.FAINT, stroke_width=8).to_corner(UR, buff=0.6)
        tracker = ValueTracker(1.0)
        ring = always_redraw(lambda: Arc(radius=0.42, start_angle=PI / 2, angle=TAU * max(tracker.get_value(), 0.001),
                                         stroke_color=th.AMBER, stroke_width=8).move_arc_center_to(ring_bg.get_center()))
        self.play(FadeIn(ring_bg), FadeIn(ring), run_time=0.3)
        for k in range(think):
            label = T(self.num(think - k), size=30, color=th.INK, weight="BOLD").move_to(ring_bg)
            self.add(label)
            self.sfx("count", gain=-16)
            self.play(tracker.animate.set_value(1 - (k + 1) / think), run_time=1.0, rate_func=rate_functions.linear)
            self.remove(label)
        self.play(FadeOut(ring_bg), FadeOut(ring), run_time=0.2)
        self.remove(ring)
        right = cards[answer]
        self.sfx("correct", gain=-8)
        nb.set_state("success", once=True)
        anims = [right[0].animate.set_stroke(th.MINT, width=5).set_fill(th.MINT, opacity=0.18)]
        anims += [cd.animate.set_opacity(0.3) for j, cd in enumerate(cards) if j != answer]
        self.play(*anims, run_time=0.5)
        self.play(Indicate(right, color=th.MINT, scale_factor=1.06), run_time=0.6)
        with self.say(reveal):
            pass
        self.play(FadeOut(VGroup(head, q, cards)), FadeOut(nb), run_time=0.5)
        self.remove(nb)

    def recap(self, points, narration):
        self._chapters.append([round(self.renderer.time, 2), self.S.get("recap", "Recap")])
        self.clear_stage()
        head = T(self.S["recap"], size=44, color=self.color, weight="BOLD", display=True).to_edge(UP, buff=0.8)
        rows = VGroup()
        for p in points:
            mark = VGroup(Circle(radius=0.17, stroke_color=th.MINT, stroke_width=3),
                          )
            txt = para(p, width=10.4, size=27, color=th.INK) if isinstance(p, str) else p
            rows.add(VGroup(mark, txt).arrange(RIGHT, buff=0.3, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        if rows.height > 5.6:
            rows.scale_to_fit_height(5.6)
        rows.next_to(head, DOWN, buff=0.45)
        nb = self.neby("read", height=1.6).to_corner(DR, buff=0.45)
        if rows.get_bottom()[1] < nb.get_top()[1] and rows.get_right()[0] > nb.get_left()[0] - 0.2:
            # long recaps reach the bottom corner: slide the list left (and shrink if needed) so Neby never covers text
            rows.to_edge(LEFT, buff=0.6)
            room = nb.get_left()[0] - 0.25 - rows.get_left()[0]
            if rows.width > room:
                rows.scale(room / rows.width, about_edge=UL)
        self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.5)
        self.add(nb)
        self.play(FadeIn(nb), run_time=0.3)
        with self.say(narration) as v:
            per = max(0.5, v.dur * 0.9 / len(rows))
            for r in rows:
                o = r[0][0].get_center()
                ck = VGroup(Line(o + [-0.08, 0.0, 0], o + [-0.02, -0.07, 0], color=th.MINT, stroke_width=4),
                            Line(o + [-0.02, -0.07, 0], o + [0.09, 0.07, 0], color=th.MINT, stroke_width=4))
                r[0].add(ck)
                self.sfx("tick", gain=-12)
                self.play(FadeIn(r, shift=RIGHT * 0.2), Create(ck), run_time=0.5)
                self.hold(per - 0.5)
        nb.set_state("success", once=True)
        self.wait(0.8)
        self.play(FadeOut(VGroup(head, rows)), FadeOut(nb), run_time=0.5)
        self.remove(nb)

    def outro(self, narration):
        if self.hud is not None:
            self.play(FadeOut(self.hud), run_time=0.4)
            self.hud = None
        self.clear_stage()
        nb = self.neby("celebrate", height=2.6).shift(UP * 1.1)
        brand = T(self.S["brand"], size=64, color=th.INK, weight="BOLD", display=True).next_to(nb, DOWN, buff=0.3)
        url = T(self.S["url"], size=28, color=self.color).next_to(brand, DOWN, buff=0.2)
        nxt = VGroup()
        if self.NEXT:
            nxt = VGroup(T(self.S["next"], size=22, color=th.MUTED), T(self.NEXT, size=30, color=th.INK, weight="SEMIBOLD"))
            nxt.arrange(DOWN, buff=0.12).next_to(url, DOWN, buff=0.55)
        self.sfx("shimmer", gain=-8)
        self.add(nb)
        self.play(FadeIn(nb, scale=0.4, rate_func=rate_functions.ease_out_back), run_time=0.6)
        self.play(Write(brand), FadeIn(url, shift=UP * 0.2), run_time=1.0)
        with self.say(narration):
            if self.NEXT:
                self.play(FadeIn(nxt, shift=UP * 0.2), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(Group(nb, brand, url, nxt)), run_time=0.8)
        self.wait(0.3)

    def tear_down(self):
        out = os.environ.get("LESSON_SRT")
        if not out:
            return
        def ts(x):
            t = int(round(x * 1000))
            return f"{t // 3600000:02d}:{t // 60000 % 60:02d}:{t // 1000 % 60:02d},{t % 1000:03d}"
        with open(out, "w", encoding="utf-8") as f:
            for i, (a, b, t) in enumerate(self._subs, 1):
                f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n")
        meta = os.environ.get("LESSON_META")
        if meta:
            json.dump({"subject": self.SUBJECT, "grade": self.GRADE, "unit": self.UNIT, "title": self.TITLE,
                       "subtitle": self.SUBTITLE, "lang": self.LANG, "sections": self.SECTIONS,
                       "duration": self.renderer.time, "mood": self.MOOD, "chapters": self._chapters},
                      open(meta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


class _Null:
    dur = 2.5

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False
