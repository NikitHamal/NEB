"""Genetics drawing helpers: bases, nucleotides, a live double helix, chromosomes with gene loci, Punnett squares,
pea plants and seeds, pedigree symbols and a simple mouse."""
import numpy as np
from manim import *

from kit import M, T, para, th

BASE = {"A": "#FF6B6B", "T": "#FFD166", "G": "#7BE495", "C": "#4CC9F0", "U": "#C77DFF"}
PAIR = {"A": "T", "T": "A", "G": "C", "C": "G"}
RNA_PAIR = {"A": "U", "T": "A", "G": "C", "C": "G"}
SUGAR = "#B8A1FF"
PHOS = "#FFB547"
OLD = "#4CC9F0"
NEW = "#FF8FB1"
CODON = {"AUG": "Met", "GCU": "Ala", "UGG": "Trp", "UAA": "stop", "UAG": "stop", "UGA": "stop", "GAG": "Glu", "GUG": "Val",
         "UUU": "Phe", "GGC": "Gly", "CAU": "His", "AAA": "Lys", "CUG": "Leu", "GAA": "Glu", "UCC": "Ser", "ACU": "Thr",
         "GAU": "Asp", "GGA": "Gly", "CGA": "Arg", "UAC": "Tyr", "GCA": "Ala", "CCU": "Pro", "AGC": "Ser",
         "UGC": "Cys", "GUA": "Val", "AAG": "Lys", "CAG": "Gln", "GCC": "Ala", "UCA": "Ser", "AUC": "Ile", "GGU": "Gly",
         "CGG": "Arg", "AGG": "Arg", "UUG": "Leu", "CAA": "Gln", "AUA": "Ile", "GUC": "Val", "ACG": "Thr", "UGU": "Cys"}


def base_chip(b, w=0.42, h=0.42, size=24):
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_width=0, fill_color=BASE[b], fill_opacity=0.95)
    return VGroup(r, T(b, size=size, color="#0B0E1A", weight="BOLD").move_to(r))


def seq_row(s, w=0.42, gap=0.06, size=24):
    g = VGroup(*[base_chip(b, w, w, size) for b in s])
    g.arrange(RIGHT, buff=gap)
    return g


def purine(color, s=0.42):
    hexa = RegularPolygon(6, radius=s, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.25).rotate(PI / 6)
    pent = RegularPolygon(5, radius=s * 0.85, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.25)
    pent.rotate(-PI / 10).next_to(hexa, RIGHT, buff=-0.08)
    return VGroup(hexa, pent)


def pyrimidine(color, s=0.42):
    return VGroup(RegularPolygon(6, radius=s, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.25).rotate(PI / 6))


def nucleotide(b="A", s=1.0):
    ph = VGroup(Circle(radius=0.32 * s, stroke_width=0, fill_color=PHOS, fill_opacity=1), T("P", size=int(26 * s), color="#0B0E1A", weight="BOLD"))
    sug = RegularPolygon(5, radius=0.42 * s, stroke_color=SUGAR, stroke_width=4, fill_color=SUGAR, fill_opacity=0.3)
    bs = (purine if b in "AG" else pyrimidine)(BASE[b], 0.36 * s)
    sug.move_to(ORIGIN)
    ph.next_to(sug, LEFT + UP, buff=0.1 * s)
    bs.next_to(sug, RIGHT, buff=0.3 * s)
    l1 = Line(ph.get_center(), sug.get_center(), color=th.MUTED, stroke_width=3)
    l2 = Line(sug.get_right(), bs.get_left(), color=th.MUTED, stroke_width=3)
    lab = T(b, size=int(26 * s), color=BASE[b], weight="BOLD").move_to(bs)
    g = VGroup(l1, l2, ph, sug, bs, lab)
    g.parts = dict(phosphate=ph, sugar=sug, base=bs, label=lab)
    return g


class Helix(VGroup):
    """Two backbones as phase-shifted sines along x, with base-pair rungs; `phase` tracker spins it."""

    def __init__(self, seq="ATGCGTACGATCCGTA", x0=-5.5, x1=5.5, amp=1.0, turns=1.6, phase=None, center_y=0.0):
        super().__init__()
        self.seq, self.x0, self.x1, self.amp, self.turns, self.cy = seq, x0, x1, amp, turns, center_y
        self.phase = phase or ValueTracker(0.0)
        self.add(always_redraw(self._draw))

    def _y(self, x, off):
        k = TAU * self.turns / (self.x1 - self.x0)
        return self.cy + self.amp * np.sin(k * (x - self.x0) + self.phase.get_value() + off)

    def _draw(self):
        g = VGroup()
        xs = np.linspace(self.x0, self.x1, 160)
        n = len(self.seq)
        for j, b in enumerate(self.seq):
            x = self.x0 + (j + 0.5) * (self.x1 - self.x0) / n
            ya, yb = self._y(x, 0), self._y(x, PI * 0.75)
            mid = (ya + yb) / 2
            depth = np.cos(TAU * self.turns / (self.x1 - self.x0) * (x - self.x0) + self.phase.get_value() + PI * 0.375)
            op = 0.45 + 0.55 * (depth + 1) / 2
            g.add(Line([x, ya, 0], [x, mid, 0], stroke_width=7, color=BASE[b], stroke_opacity=op))
            g.add(Line([x, mid, 0], [x, yb, 0], stroke_width=7, color=BASE[PAIR[b]], stroke_opacity=op))
        for off, col in ((0, OLD), (PI * 0.75, "#9C8CFF")):
            g.add(VMobject(stroke_color=col, stroke_width=7).set_points_smoothly([[x, self._y(x, off), 0] for x in xs]))
        return g


def chromatid(genes, colors, x, y0, h=3.2, w=0.34, color=OLD, gene_col=None):
    """A vertical chromatid with gene bands; genes listed top to bottom at fractions of h."""
    body = RoundedRectangle(corner_radius=w / 2, width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([x, y0, 0])
    marks = VGroup()
    for (g, f), c in zip(genes, colors):
        y = y0 + h / 2 - f * h
        marks.add(Rectangle(width=w, height=0.1, stroke_width=0, fill_color=c, fill_opacity=1).move_to([x, y, 0]))
        marks.add(T(g, size=24, color=c, weight="BOLD").move_to([x - 0.42, y, 0]))
    return VGroup(body, marks)


def lab(s, size, color, weight="BOLD"):
    if s.startswith("$"):
        return M(s.strip("$"), size=int(size * 1.35), color=color)
    return T(s, size=size, color=color, weight=weight)


def punnett(rows, cols, cells, cell=0.95, size=26, head_color=th.AMBER, fills=None):
    """rows/cols: gamete labels; cells[i][j]: text ('$...$' = LaTeX). Returns (grid, cell squares, cell texts)."""
    g = VGroup()
    sq, tx = {}, {}
    n, m = len(rows), len(cols)
    for j, c in enumerate(cols):
        g.add(lab(c, size, head_color).move_to([(j + 1) * cell, 0, 0]))
    for i, r in enumerate(rows):
        g.add(lab(r, size, head_color).move_to([0, -(i + 1) * cell, 0]))
        for j in range(m):
            box = Square(side_length=cell * 0.96, stroke_color=th.PANEL_EDGE, stroke_width=2, fill_color=(fills[i][j] if fills else th.PANEL), fill_opacity=0.9)
            box.move_to([(j + 1) * cell, -(i + 1) * cell, 0])
            t = lab(cells[i][j], size, th.INK, "SEMIBOLD").move_to(box)
            if t.width > cell * 0.9:
                t.scale_to_fit_width(cell * 0.88)
            sq[(i, j)], tx[(i, j)] = box, t
            g.add(box)
    g.add(*tx.values())
    return g, sq, tx


def pea(tall=True, color="#5FB04A", h=None):
    h = h or (1.9 if tall else 0.8)
    stem = Line([0, 0, 0], [0, h, 0], color=color, stroke_width=6)
    lv = VGroup(*[Ellipse(width=0.42, height=0.18, stroke_width=0, fill_color=color, fill_opacity=1).rotate(s * 0.4).move_to([s * 0.2, y, 0])
                  for y, s in [(h * 0.35, 1), (h * 0.6, -1), (h * 0.85, 1)]])
    return VGroup(stem, lv)


def seed(round_=True, yellow=True, r=0.24):
    col = "#FFD23F" if yellow else "#7BC043"
    if round_:
        m = Circle(radius=r, stroke_color=WHITE, stroke_width=1.5, fill_color=col, fill_opacity=1)
    else:
        pts = [r * (0.82 + 0.14 * np.cos(7 * a)) * np.array([np.cos(a), np.sin(a), 0]) for a in np.linspace(0, TAU, 60)]
        m = VMobject(stroke_color=WHITE, stroke_width=1.5, fill_color=col, fill_opacity=1).set_points_smoothly(pts + [pts[0]])
    return m


def person(male, affected=False, carrier=False, s=0.5, color=th.INK):
    shape = Square(side_length=s, stroke_color=color, stroke_width=3) if male else Circle(radius=s / 2, stroke_color=color, stroke_width=3)
    if affected:
        shape.set_fill(color, opacity=1)
    g = VGroup(shape)
    if carrier:
        g.add(Dot(radius=s * 0.14, color=color))
    return g


def mouse(alive=True, color="#D9D9E8"):
    body = Ellipse(width=1.1, height=0.62, stroke_width=0, fill_color=color, fill_opacity=1)
    head = Circle(radius=0.24, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0.6, 0.12, 0])
    ear = Circle(radius=0.12, stroke_width=0, fill_color="#F2A7C0", fill_opacity=1).move_to([0.55, 0.36, 0])
    eye = Dot([0.7, 0.16, 0], radius=0.035, color="#0B0E1A")
    tail = VMobject(stroke_color=color, stroke_width=3).set_points_smoothly([[-0.55, 0, 0], [-0.9, 0.15, 0], [-1.1, -0.05, 0], [-1.3, 0.1, 0]])
    g = VGroup(tail, body, head, ear, eye)
    if not alive:
        g.rotate(PI)
        x = VGroup(Line([0.45, 0.0, 0], [0.75, 0.3, 0], color=th.CORAL, stroke_width=5), Line([0.45, 0.3, 0], [0.75, 0.0, 0], color=th.CORAL, stroke_width=5))
        g.add(x.move_to(head.get_center()))
    return g


def chrom_bar(labels, x0, y, w=0.62, h=0.5, colors=None, size=24):
    g = VGroup()
    for i, l in enumerate(labels):
        c = colors[i] if colors else th.PANEL_EDGE
        r = Rectangle(width=w, height=h, stroke_color=th.INK, stroke_width=2, fill_color=c, fill_opacity=0.85).move_to([x0 + i * w, y, 0])
        g.add(VGroup(r, T(l, size=size, color=th.INK, weight="BOLD").move_to(r)))
    return g
