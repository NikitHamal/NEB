#!/usr/bin/env python3
"""Build the BCA PDFs with ReportLab and write the viewer manifest.

    python3 notes/tools/bca_build.py --public /path/to/public/bca

Needs: pip install reportlab matplotlib (matplotlib only for its bundled DejaVu fonts).
"""
import argparse, glob, json, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); NOTES = os.path.dirname(HERE)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib
FD = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
for n, f in (("DV", "DejaVuSans.ttf"), ("DV-B", "DejaVuSans-Bold.ttf"), ("DV-I", "DejaVuSans-Oblique.ttf"), ("DV-M", "DejaVuSansMono.ttf")):
    pdfmetrics.registerFont(TTFont(n, os.path.join(FD, f)))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-B")

BOOKS = {"bca-math": ("Mathematics", 50), "bca-eng": ("English", 40), "bca-gk": ("General-Knowledge-and-IT", 10), "bca-mock": ("Model-Papers-and-Mock-Tests", 100)}
SUP = dict(zip("0123456789+-=()n", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ")); SUB = dict(zip("0123456789+-=()", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"))
SYM = {"times": "×", "cdot": "·", "le": "≤", "leq": "≤", "ge": "≥", "geq": "≥", "ne": "≠", "pi": "π", "theta": "θ", "alpha": "α", "beta": "β", "lambda": "λ", "circ": "°", "infty": "∞", "to": "→", "Rightarrow": "⇒", "iff": "⇔", "in": "∈", "cup": "∪", "cap": "∩", "subseteq": "⊆", "varnothing": "∅", "Delta": "Δ", "perp": "⊥", "pm": "±", "int": "∫", "sum": "Σ", "ldots": "…", "dots": "…", "cdots": "…", "lvert": "|", "rvert": "|", "mid": "|", "quad": " ", "left": "", "right": "", "text": "", "mathrm": "", "mathbf": "", "hat": "", "overline": "", "bmod": " mod ", "ln": "ln", "log": "log", "sin": "sin", "cos": "cos", "tan": "tan", "cot": "cot", "sec": "sec", "csc": "csc", "lim": "lim", "ell": "ℓ"}

def script(s, table, pre):
    return "".join(table.get(c, None) or "" for c in s) if all(c in table for c in s) else f"{pre}({s})"

def tex(m):
    s = m
    for _ in range(6):
        s = re.sub(r"\\binom\{([^{}]*)\}\{([^{}]*)\}", r"C(\1,\2)", s)
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", lambda x: (x.group(1) + "/" + x.group(2)) if re.fullmatch(r"[\w.]+", x.group(1)) and re.fullmatch(r"[\w.]+", x.group(2)) else f"({x.group(1)})/({x.group(2)})", s)
        s = re.sub(r"\\sqrt\[(\w+)\]\{([^{}]*)\}", lambda x: SUP.get(x.group(1), x.group(1)) + "√(" + x.group(2) + ")", s)
        s = re.sub(r"\\sqrt\{([^{}]*)\}", lambda x: "√" + (x.group(1) if re.fullmatch(r"\w+", x.group(1)) else f"({x.group(1)})"), s)
        s = re.sub(r"\^\{([^{}]*)\}", lambda x: script(x.group(1), SUP, "^"), s)
        s = re.sub(r"_\{([^{}]*)\}", lambda x: script(x.group(1), SUB, "_"), s)
        s = re.sub(r"\\(?:text|mathrm|mathbf|hat|overline)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\^(\w)", lambda x: SUP.get(x.group(1), "^" + x.group(1)), s)
    s = re.sub(r"_(\w)", lambda x: SUB.get(x.group(1), "_" + x.group(1)), s)
    s = re.sub(r"\\([A-Za-z]+)", lambda x: SYM.get(x.group(1), x.group(1)), s)
    s = s.replace("\\%", "%").replace("\\{", "{").replace("\\}", "}").replace("\\,", " ").replace("\\ ", " ").replace("\\!", "")
    return s.replace("{", "").replace("}", "")

def inline(t):
    t = re.sub(r"\$\$?(.+?)\$\$?", lambda m: tex(m.group(1)), t)
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"`([^`]+)`", r'<font name="DV-M">\1</font>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    return t

ST = {"b": ParagraphStyle("b", fontName="DV", fontSize=9.2, leading=13, spaceAfter=3),
      "h1": ParagraphStyle("h1", fontName="DV-B", fontSize=17, leading=21, spaceBefore=6, spaceAfter=8, textColor=colors.HexColor("#1f2a44")),
      "h2": ParagraphStyle("h2", fontName="DV-B", fontSize=12.5, leading=16, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor("#8F5507")),
      "h3": ParagraphStyle("h3", fontName="DV-B", fontSize=10.5, leading=14, spaceBefore=6, spaceAfter=2),
      "li": ParagraphStyle("li", fontName="DV", fontSize=9.2, leading=13, leftIndent=12, bulletIndent=2, spaceAfter=1.5),
      "opt": ParagraphStyle("opt", fontName="DV", fontSize=9, leading=12.5, leftIndent=18, spaceAfter=3),
      "box": ParagraphStyle("box", fontName="DV", fontSize=8.8, leading=12.2, spaceAfter=2),
      "cell": ParagraphStyle("cell", fontName="DV", fontSize=8.2, leading=10.5)}
BOXC = {"key": "#E8EEFB", "note": "#F3F3F3", "caution": "#FDECEA", "tip": "#E9F6EC", "example": "#FFF6E0", "memory": "#F1EAFB", "definition": "#E8EEFB"}

def cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]

def flow(lines, W):
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1; continue
        m = re.match(r"::: (\w+)\s*(.*)", l)
        if m:
            j = i + 1; body = []
            while lines[j].strip() != ":::":
                body.append(lines[j]); j += 1
            inner = flow(body, W - 12 * mm)
            title = Paragraph("<b>" + inline(m.group(2) or m.group(1).title()) + "</b>", ST["box"])
            t = Table([[title]] + [[f] for f in inner], colWidths=[W])
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(BOXC.get(m.group(1), "#F3F3F3"))), ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
            out += [t, Spacer(1, 5)]; i = j + 1; continue
        if l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.fullmatch(r"\|[\s:|-]+\|?", lines[i].strip()):
                    rows.append(cells(lines[i]))
                i += 1
            n = max(len(r) for r in rows); rows = [r + [""] * (n - len(r)) for r in rows]
            ln = [max(len(r[c]) for r in rows) + 6 for c in range(n)]; tot = sum(ln)
            t = Table([[Paragraph(inline(c), ST["cell"]) for c in r] for r in rows], colWidths=[W * x / tot for x in ln], repeatRows=1)
            t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#b8b8b8")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ECE7DD")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
            out += [t, Spacer(1, 5)]; continue
        h = re.match(r"(#{1,3}) (.*)", l)
        if h:
            out.append(Paragraph(inline(h.group(2)), ST["h%d" % len(h.group(1))])); i += 1; continue
        if re.match(r"\s{2,}\(a\) ", l):
            out.append(Paragraph(inline(l.strip()), ST["opt"])); i += 1; continue
        bl = re.match(r"- (.*)", l)
        if bl:
            out.append(Paragraph(inline(bl.group(1)), ST["li"], bulletText="•")); i += 1; continue
        nl = re.match(r"(\d+)\. (.*)", l)
        if nl:
            out.append(Paragraph("<b>%s.</b> %s" % (nl.group(1), inline(nl.group(2))), ParagraphStyle("q", parent=ST["b"], leftIndent=18, firstLineIndent=-18, spaceAfter=1))); i += 1; continue
        para = [l.strip()]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"(#|\||- |\d+\. |::: |\s{2,}\(a\))", lines[i]):
            para.append(lines[i].strip()); i += 1
        out.append(Paragraph(inline(" ".join(para)), ST["b"]))
    return out

def foot(name):
    def f(c, d):
        c.saveState(); c.setFont("DV", 7.5); c.setFillColor(colors.grey)
        c.drawString(18 * mm, 10 * mm, "NEBians · BCA Entrance · " + name + " · free and open · nebians.consica.com.np")
        c.drawRightString(A4[0] - 18 * mm, 10 * mm, str(d.page)); c.restoreState()
    return f

def build_pdf(slug, out):
    name, q = BOOKS[slug]; W = A4[0] - 36 * mm
    story = [Spacer(1, 50 * mm), Paragraph("NEBians", ParagraphStyle("c0", fontName="DV-B", fontSize=14, textColor=colors.HexColor("#8F5507"))),
             Paragraph("BCA Entrance — " + name.replace("-", " "), ParagraphStyle("c1", fontName="DV-B", fontSize=26, leading=32, spaceBefore=10)),
             Paragraph("Tribhuvan University, Faculty of Humanities and Social Sciences · 100 MCQs · 2 hours · English 40, Mathematics 50, General Knowledge and IT 10", ParagraphStyle("c2", fontName="DV", fontSize=11, leading=15, spaceBefore=10)),
             Spacer(1, 10 * mm), Paragraph("Free for every student. Original practice written to the published pattern; not a TU publication. Every book needs a subject-teacher review before it is trusted blindly: if you find a wrong key, report it.", ST["b"]), PageBreak()]
    for f in sorted(glob.glob(os.path.join(NOTES, "content", slug, "unit-*.md"))):
        s = open(f, encoding="utf-8").read(); fm = dict(re.findall(r"^(\w+): (.*)$", re.match(r"---\n(.*?)\n---\n", s, re.S).group(1), re.M))
        body = s.split("\n---\n", 1)[1].splitlines()
        story += [Paragraph("Chapter %s — %s" % (fm["unit"], inline(fm["title"])), ST["h1"])] + flow(body, W) + [PageBreak()]
    SimpleDocTemplate(out, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=18 * mm, title="NEBians BCA Entrance " + name, author="NEBians").build(story, onFirstPage=foot(name), onLaterPages=foot(name))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--public", required=True); ap.add_argument("--no-pdf", action="store_true"); a = ap.parse_args()
    pub = a.public
    for d in ("content", "pdf", "docs", "syllabus"): os.makedirs(os.path.join(pub, d), exist_ok=True)
    pdfdir = os.path.join(NOTES, "pdf"); man = {"books": [], "docs": [], "title": "NEBians BCA Entrance Preparation"}
    for slug, (name, q) in BOOKS.items():
        pn = "NEBians-BCA-Entrance-%s.pdf" % name
        if not a.no_pdf: build_pdf(slug, os.path.join(pdfdir, pn))
        if os.path.exists(os.path.join(pdfdir, pn)): shutil.copy(os.path.join(pdfdir, pn), os.path.join(pub, "pdf", pn))
        shutil.copy(os.path.join(NOTES, "curriculum", slug + ".md"), os.path.join(pub, "syllabus", slug + ".md"))
        head = open(os.path.join(NOTES, "curriculum", slug + ".md"), encoding="utf-8").readline()
        units = []; os.makedirs(os.path.join(pub, "content", slug), exist_ok=True)
        for f in sorted(glob.glob(os.path.join(NOTES, "content", slug, "unit-*.md"))):
            s = open(f, encoding="utf-8").read(); fm = dict(re.findall(r"^(\w+): (.*)$", re.match(r"---\n(.*?)\n---\n", s, re.S).group(1), re.M))
            shutil.copy(f, os.path.join(pub, "content", slug, os.path.basename(f)))
            units.append({"n": int(fm["unit"]), "title": fm["title"], "area": fm["area"], "questions": int(fm["hours"]), "file": "content/%s/%s" % (slug, os.path.basename(f)), "words": len(re.findall(r"\w+", s)), "mcq": len(re.findall(r"^\s{2,}\(a\) ", s, re.M))})
        man["books"].append({"slug": slug, "name": name.replace("-", " "), "paperQuestions": q, "pdf": "pdf/" + pn, "syllabus": "syllabus/%s.md" % slug, "units": units, "header": head.strip("# \n")})
    for d in ("HANDOFF-BCA.md", "AUTHORING-ENTRANCE.md"):
        shutil.copy(os.path.join(NOTES, d), os.path.join(pub, "docs", d)); man["docs"].append({"name": d, "file": "docs/" + d})
    json.dump(man, open(os.path.join(pub, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("books", len(man["books"]), "units", sum(len(b["units"]) for b in man["books"]), "mcq", sum(u["mcq"] for b in man["books"] for u in b["units"]))

main()
