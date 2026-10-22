"""Shared helpers for the Class 12 Computer Science lessons: syntax-coloured code blocks, named database tables,
terminal/output panels, network nodes and packets. Reuses the maths/biology helpers (worked, table, Captions …)."""
import os
import re
import sys

import numpy as np
from manim import *

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "math12"))
sys.path.insert(0, os.path.join(HERE, "..", "bio12"))
from kit import M, T, para, th  # noqa: E402
from _m import worked, head, bullets, reveal_list, table, reveal_table, neby_in, neby_out, Captions, example_head, clipped  # noqa: E402,F401

MONO = "JetBrains Mono"
KW_COL = th.SKY
STR_COL = th.AMBER
NUM_COL = th.PINK
CMT_COL = th.MUTED
FN_COL = th.MINT

SQL_KW = {"SELECT", "FROM", "WHERE", "AND", "OR", "NOT", "ORDER", "BY", "GROUP", "HAVING", "JOIN", "LEFT", "RIGHT", "INNER", "ON", "AS", "INSERT", "INTO", "VALUES", "UPDATE",
          "SET", "DELETE", "CREATE", "TABLE", "ALTER", "ADD", "DROP", "COLUMN", "PRIMARY", "KEY", "FOREIGN", "REFERENCES", "NULL", "DISTINCT", "IN", "LIKE", "BETWEEN", "DESC",
          "ASC", "VIEW", "TRUNCATE", "INTEGER", "INT", "VARCHAR", "CHAR", "DATE", "UNIQUE", "CHECK", "DEFAULT", "IS", "COUNT", "SUM", "AVG", "MAX", "MIN", "ROUND", "LIMIT"}
C_KW = {"int", "float", "double", "char", "void", "if", "else", "for", "while", "do", "return", "struct", "switch", "case", "break", "continue", "include", "define", "FILE",
        "long", "unsigned", "const", "sizeof", "typedef", "default", "union", "static"}
PY_KW = {"class", "def", "self", "return", "if", "else", "elif", "for", "in", "while", "import", "from", "print", "True", "False", "None", "super", "pass", "and", "or", "not", "lambda"}
JS_KW = {"function", "var", "let", "const", "if", "else", "for", "while", "return", "document", "true", "false", "new", "this", "echo", "php", "isset", "foreach", "as", "null"}

TOK = re.compile(r"(\s+|'[^']*'|\"[^\"]*\"|--.*$|//.*$|#.*$|/\*.*?\*/|\d+(?:\.\d+)?|[A-Za-z_]\w*|.)")


def _colour(tok, lang):
    if tok.startswith(("'", '"')):
        return STR_COL
    if tok.startswith(("--", "//", "/*")) or (tok.startswith("#") and lang not in ("c",)):
        return CMT_COL
    if re.fullmatch(r"\d+(?:\.\d+)?", tok):
        return NUM_COL
    kws = {"sql": SQL_KW, "c": C_KW, "py": PY_KW, "js": JS_KW}.get(lang, set())
    if (tok.upper() if lang == "sql" else tok) in kws:
        return KW_COL
    if lang == "c" and tok.startswith("#"):
        return th.CORAL
    return th.INK


def code_line(line, lang="sql", size=24):
    """One line of code as a row of coloured monospace Text pieces (keeps spacing exact)."""
    parts = VGroup()
    pieces = TOK.findall(line) or [" "]
    txt = ""
    spans = []
    for p_ in pieces:
        spans.append((len(txt), len(txt) + len(p_), _colour(p_, lang) if p_.strip() else th.INK))
        txt += p_
    mob = Text(txt if txt.strip() else ".", font=MONO, font_size=size, color=th.INK)
    if not txt.strip():
        mob.set_opacity(0)
        return mob
    # colour by character index (Text submobjects are non-space glyphs in order)
    glyph_idx = 0
    for a, b, col in spans:
        seg = txt[a:b]
        n = sum(1 for ch in seg if not ch.isspace())
        for k in range(glyph_idx, glyph_idx + n):
            if k < len(mob):
                mob[k].set_color(col)
        glyph_idx += n
    return mob


def code(lines, lang="sql", size=26, width=None, title=None, pad=0.3, max_width=12.8):
    """A code panel: rounded dark box, optional title tab, left-aligned coloured lines. .lines holds each line."""
    if isinstance(lines, str):
        lines = lines.strip("\n").split("\n")
    rows = VGroup(*[code_line(l_, lang, size) for l_ in lines])
    lh = size / 48 * 1.0
    cw = size / 48 * 0.6  # JetBrains Mono advance ≈ 0.6 em
    for i, r in enumerate(rows):
        indent = len(lines[i]) - len(lines[i].lstrip(" "))
        r.move_to([0, -i * lh, 0], aligned_edge=LEFT).shift(RIGHT * indent * cw * (48 / 48) * 0.5)
    w = max(rows.width + 2 * pad, width or 0)
    box = RoundedRectangle(corner_radius=0.12, width=w, height=rows.height + 2 * pad, stroke_color=th.FAINT, stroke_width=2, fill_color="#0D1022", fill_opacity=1)
    rows.move_to(box).align_to(box, LEFT).shift(RIGHT * pad)
    g = VGroup(box, rows)
    if title:
        tab = T(title, size=18, color=th.MUTED).next_to(box, UP, buff=0.06).align_to(box, LEFT).shift(RIGHT * 0.15)
        g.add(tab)
    g.lines = rows
    g.box = box
    if g.width > max_width:
        g.scale_to_fit_width(max_width)
    return g


def type_code(s, panel, per_line=0.35):
    """Reveal a code panel line by line (typing feel)."""
    s.play(FadeIn(panel.box), *([FadeIn(panel[2])] if len(panel) > 2 else []), run_time=0.3)
    for ln in panel.lines:
        s.play(AddTextLetterByLetter(ln, time_per_char=max(0.005, per_line / max(1, len(ln)))) if len(ln) else Wait(0.05), run_time=max(0.15, per_line))


def dbtable(name, cols, rows, widths=None, size=26, row_h=0.5, pk=(), fk=(), name_color=None):
    """A database table with its name above and key columns marked (PK amber, FK sky)."""
    widths = widths or [max(1.2, 0.16 * max(len(str(c)) for c in [col] + [r[i] for r in rows]) + 0.4) for i, col in enumerate(cols)]
    hdr = list(cols)
    colors = [th.AMBER if c in pk else (th.SKY if c in fk else th.INK) for c in cols]
    tb = table([hdr] + [[str(v) for v in r] for r in rows], widths, row_h=row_h, size=size, colors=colors)
    nm = T(name, size=size + 2, color=name_color or th.MINT, weight="BOLD").next_to(tb, UP, buff=0.12).align_to(tb, LEFT)
    g = VGroup(nm, tb)
    g.tb = tb
    return g


def terminal(lines, size=20, color=th.CORAL, width=None):
    rows = VGroup(*[Text(l_, font=MONO, font_size=size, color=color) for l_ in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    w = max(rows.width + 0.5, width or 0)
    box = RoundedRectangle(corner_radius=0.1, width=w, height=rows.height + 0.4, stroke_color=color, stroke_width=2, fill_color="#140B12", fill_opacity=1)
    rows.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
    return VGroup(box, rows)


def node(label, color=th.SKY, w=1.3, h=0.8, size=24, icon=None):
    box = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=3, fill_color=th.PANEL, fill_opacity=1)
    t = T(label, size=size, color=color, weight="BOLD").move_to(box)
    if t.width > w - 0.15:
        t.scale_to_fit_width(w - 0.15)
    return VGroup(box, t)


def packet(color=th.AMBER, w=0.36, h=0.22, label=None):
    r = RoundedRectangle(corner_radius=0.05, width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=1)
    if label:
        return VGroup(r, T(label, size=12, color=th.BG, weight="BOLD").move_to(r))
    return VGroup(r)


def browser(url="localhost/index.php", w=5.6, h=3.6):
    """A simple browser window: frame, address bar, content area at .area."""
    frame = RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=th.MUTED, stroke_width=3, fill_color="#F4F6FB", fill_opacity=1)
    bar = Rectangle(width=w, height=0.5, stroke_width=0, fill_color="#D9DEEA", fill_opacity=1).align_to(frame, UP)
    dots = VGroup(*[Dot(radius=0.06, color=c_) for c_ in ("#FF5F57", "#FEBC2E", "#28C840")]).arrange(RIGHT, buff=0.1).move_to(bar).align_to(bar, LEFT).shift(RIGHT * 0.2)
    addr = RoundedRectangle(corner_radius=0.1, width=w - 1.4, height=0.3, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(bar).shift(RIGHT * 0.35)
    ut = Text(url, font=MONO, font_size=16, color="#333333").move_to(addr).align_to(addr, LEFT).shift(RIGHT * 0.1)
    area = Rectangle(width=w - 0.3, height=h - 0.8, stroke_opacity=0, fill_opacity=0).move_to(frame.get_center() + DOWN * 0.25)
    g = VGroup(frame, bar, dots, addr, ut, area)
    g.area = area
    return g


def output(lines, size=22, title="output"):
    return code(lines, lang="none", size=size, title=title)
