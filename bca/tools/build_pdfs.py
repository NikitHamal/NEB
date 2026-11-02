#!/usr/bin/env python3
"""Build the BCA PDFs (entrance + course) from the Markdown sources.

    python3 bca/tools/build_pdfs.py            # every book under bca/
    python3 bca/tools/build_pdfs.py bca/course/semester-1/programming-in-c

A "book" is any directory that directly contains unit-*.md files. Its PDF is written to the
`pdfs/` folder of the enclosing section (bca/entrance/pdfs, bca/course/semester-N/pdfs).

Needs: pip install weasyprint markdown pygments ; system libs libpango-1.0-0, libpangoft2-1.0-0,
fonts-liberation, fonts-dejavu.
"""
import datetime, glob, html, os, re, sys
import markdown
from pygments.formatters import HtmlFormatter
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SUP = dict(zip("0123456789+-=()n", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ"))
SUB = dict(zip("0123456789+-=()", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"))
SYM = {"times": "×", "cdot": "·", "le": "≤", "leq": "≤", "ge": "≥", "geq": "≥", "ne": "≠", "neq": "≠", "pi": "π",
       "theta": "θ", "alpha": "α", "beta": "β", "gamma": "γ", "lambda": "λ", "mu": "μ", "sigma": "σ", "omega": "ω",
       "phi": "φ", "circ": "°", "infty": "∞", "to": "→", "rightarrow": "→", "Rightarrow": "⇒", "iff": "⇔",
       "in": "∈", "notin": "∉", "cup": "∪", "cap": "∩", "subseteq": "⊆", "subset": "⊂", "varnothing": "∅",
       "emptyset": "∅", "Delta": "Δ", "perp": "⊥", "pm": "±", "int": "∫", "sum": "Σ", "prod": "Π", "ldots": "…",
       "dots": "…", "cdots": "…", "lvert": "|", "rvert": "|", "mid": "|", "quad": " ", "qquad": "  ", "left": "",
       "right": "", "bmod": " mod ", "ln": "ln", "log": "log", "sin": "sin", "cos": "cos", "tan": "tan", "cot": "cot",
       "sec": "sec", "csc": "csc", "lim": "lim", "ell": "ℓ", "forall": "∀", "exists": "∃", "neg": "¬", "land": "∧",
       "lor": "∨", "oplus": "⊕", "equiv": "≡", "approx": "≈", "div": "÷", "vee": "∨", "wedge": "∧",
       "leftrightarrow": "↔", "Leftrightarrow": "⇔", "setminus": "∖", "min": "min", "max": "max", "gcd": "gcd",
       "Sigma": "Σ", "propto": "∝", "angle": "∠", "triangle": "△", "parallel": "∥", "nabla": "∇", "partial": "∂",
       "therefore": "∴", "because": "∵", "ll": "≪", "gg": "≫", "nmid": "∤", "Pi": "Π", "epsilon": "ε",
       "delta": "δ", "tau": "τ", "rho": "ρ", "eta": "η", "xi": "ξ", "Omega": "Ω", "Theta": "Θ", "Lambda": "Λ",
       "Gamma": "Γ", "lfloor": "⌊", "rfloor": "⌋", "lceil": "⌈", "rceil": "⌉", "ast": "∗", "bullet": "•"}


def sup(s):
    return "".join(SUP[c] for c in s) if all(c in SUP for c in s) else f"<sup>{s}</sup>"


def sub(s):
    return "".join(SUB[c] for c in s) if all(c in SUB for c in s) else f"<sub>{s}</sub>"


def tex(m):
    s = html.escape(m, quote=False)
    for _ in range(8):
        s = re.sub(r"\\binom\{([^{}]*)\}\{([^{}]*)\}", r"C(\1,\2)", s)
        s = re.sub(r"\\d?frac\{([^{}]*)\}\{([^{}]*)\}",
                   r'<span class="fr"><span class="n">\1</span><span class="d">\2</span></span>', s)
        s = re.sub(r"\\sqrt\[(\w+)\]\{([^{}]*)\}", lambda x: sup(x.group(1)) + '√<span class="sq">' + x.group(2) + "</span>", s)
        s = re.sub(r"\\sqrt\{([^{}]*)\}", r'√<span class="sq">\1</span>', s)
        s = re.sub(r"\\(?:overline|bar)\{([^{}]*)\}", r'<span class="ov">\1</span>', s)
        s = re.sub(r"\\(?:vec|hat)\{([^{}]*)\}", r"<b>\1</b>", s)
        s = re.sub(r"\^\{([^{}]*)\}", lambda x: sup(x.group(1)), s)
        s = re.sub(r"_\{([^{}]*)\}", lambda x: sub(x.group(1)), s)
        s = re.sub(r"\\(?:text|mathrm|mathbf|operatorname|mathbb|textbf)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\^([\w+-])", lambda x: sup(x.group(1)), s)
    s = re.sub(r"_(\w)", lambda x: sub(x.group(1)), s)
    s = re.sub(r"\\([A-Za-z]+)", lambda x: SYM.get(x.group(1), x.group(1)), s)
    for a, b in (("\\%", "%"), ("\\{", "{"), ("\\}", "}"), ("\\,", " "), ("\\;", " "), ("\\ ", " "), ("\\!", ""),
                 ("\\$", "$"), ("\\\\", "<br>"), ("\\|", "‖")):
        s = s.replace(a, b)
    s = s.replace("{", "").replace("}", "")
    return f'<span class="m">{s}</span>'


OPT = re.compile(r"^\s{2,}\(a\)\s.*\s\(b\)\s.*\s\(c\)\s.*\s\(d\)\s")


def options(line):
    parts = re.split(r"\s\(([abcd])\)\s", " " + line.strip())
    out = ['<span class="opts">']
    for i in range(1, len(parts), 2):
        out.append(f'<span class="o"><b>({parts[i]})</b> {parts[i + 1].strip()}</span>')
    return "".join(out) + "</span>"


class Renderer:
    def __init__(self):
        self.stash = []

    def hold(self, htm):
        self.stash.append(htm)
        return f"\ue000{len(self.stash) - 1}\ue001"

    def unhold(self, text):
        for _ in range(4):
            text = re.sub(r"\ue000(\d+)\ue001", lambda m: self.stash[int(m.group(1))], text)
        return text

    def prep(self, body):
        body = re.sub(r"^```(\w*)[^\n]*\n(.*?)^```[ \t]*$",
                      lambda m: self.hold(self.code(m.group(1), m.group(2))), body, flags=re.S | re.M)
        body = re.sub(r"`([^`\n]+)`", lambda m: self.hold(f"<code>{html.escape(m.group(1), quote=False)}</code>"), body)
        body = re.sub(r"\$\$(.+?)\$\$", lambda m: self.hold('<div class="dm">' + tex(m.group(1)) + "</div>"), body, flags=re.S)
        body = re.sub(r"(?<!\\)\$(.+?)(?<!\\)\$", lambda m: self.hold(tex(m.group(1))), body)
        out = []
        for l in body.split("\n"):
            if OPT.match(l):
                out.append("   " + self.hold(options(l)))
            elif re.match(r"^\*\*\d+\.\*\*\s", l):
                out.append("")
                out.append(l)
            else:
                out.append(l)
        return "\n".join(out)

    def code(self, lang, src):
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name, TextLexer
        try:
            lex = get_lexer_by_name(lang or "text")
        except Exception:
            lex = TextLexer()
        return highlight(src.rstrip("\n"), lex, HtmlFormatter(cssclass="hl", nowrap=False))

    def md(self, text):
        return markdown.markdown(text, extensions=["tables", "sane_lists"], output_format="html5")

    def render(self, body):
        body = self.prep(body)
        segs, buf, i, lines = [], [], 0, body.split("\n")
        while i < len(lines):
            m = re.match(r"^::: (\w+)\s*(.*)$", lines[i])
            if m:
                if buf:
                    segs.append(self.md("\n".join(buf)))
                    buf = []
                j, inner = i + 1, []
                while j < len(lines) and lines[j].strip() != ":::":
                    inner.append(lines[j])
                    j += 1
                kind, title = m.group(1), m.group(2) or m.group(1).title()
                t = self.md(title)
                t = t[3:-4] if t.startswith("<p>") else t
                segs.append(f'<div class="box {kind}"><div class="bt">{t}</div>{self.md(chr(10).join(inner))}</div>')
                i = j + 1
            else:
                buf.append(lines[i])
                i += 1
        if buf:
            segs.append(self.md("\n".join(buf)))
        return self.unhold("\n".join(segs))


CSS = open(os.path.join(HERE, "pdf.css"), encoding="utf-8").read() + "\n" + \
    HtmlFormatter(style="friendly", cssclass="hl").get_style_defs(".hl")


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    fm = dict(l.split(": ", 1) for l in m.group(1).splitlines() if ": " in l) if m else {}
    return fm, (text[m.end():] if m else text)


def section_of(bookdir):
    rel = os.path.relpath(bookdir, ROOT).split(os.sep)
    if rel[0] == "entrance":
        return "BCA Entrance", os.path.join(ROOT, "entrance")
    return "BCA Course · " + rel[1].replace("semester-", "Semester "), os.path.join(ROOT, "course", rel[1])


def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")


def build(bookdir):
    files = sorted(glob.glob(os.path.join(bookdir, "unit-*.md")))
    docs = [frontmatter(open(f, encoding="utf-8").read()) for f in files]
    subject = docs[0][0].get("subject", os.path.basename(bookdir))
    label, section = section_of(bookdir)
    r = Renderer()
    chapters, toc = [], []
    for n, (fm, body) in enumerate(docs):
        u = fm.get("unit", str(n + 1))
        t = fm.get("title", "")
        cid = f"c{n}"
        toc.append(f'<li><a href="#{cid}">{html.escape(t)}</a></li>')
        area = fm.get("area", "")
        kick = f'<div class="kick">{html.escape(area)}</div>' if area else ""
        chapters.append(f'<section class="chapter" id="{cid}">{kick}<h1><span class="un">{u}</span>{html.escape(t)}</h1>{r.render(body)}</section>')
    words = sum(len(b.split()) for _, b in docs)
    intro = ""
    readme = os.path.join(bookdir, "README.md")
    if os.path.exists(readme):
        _, rb = frontmatter(open(readme, encoding="utf-8").read())
        rb = re.sub(r"^# .*\n", "", rb.lstrip("\n"), count=1)
        intro = f'<section class="chapter intro"><h1 class="plain">About this book</h1>{r.render(rb)}</section>'
    cover = f'''<section class="cover"><div class="brand">NEBians</div><div class="tag">Open learning for every ambitious student</div>
<h1 class="ct">{html.escape(subject)}</h1><div class="cl">{html.escape(label)}</div>
<div class="cm">{len(docs)} chapters · about {words:,} words · built {datetime.date.today():%d %B %Y}</div>
<div class="cf">Free to read, print and share · nebians.consica.com.np<br>Source: github.com/NikitHamal/NEB — branch claude/bca-entrance-complete</div></section>
<section class="tocpage"><h1 class="plain">Contents</h1><ol class="toc">{"".join(toc)}</ol></section>'''
    doc = (f'<html><head><meta charset="utf-8"><title>{html.escape(subject)} — {label}</title><style>{CSS}</style></head>'
           f'<body data-run="{html.escape(subject)} · {html.escape(label)}">{cover}{intro}{"".join(chapters)}</body></html>')
    outdir = os.path.join(section, "pdfs")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, f"NEBians-{slug(label)}-{slug(subject)}.pdf")
    HTML(string=doc, base_url=bookdir).write_pdf(out)
    print(f"{os.path.relpath(out, os.path.dirname(ROOT))}  ({os.path.getsize(out) // 1024} KB, {len(docs)} chapters)")


def main():
    targets = sys.argv[1:]
    dirs = [os.path.abspath(t) for t in targets] if targets else \
        sorted({os.path.dirname(p) for p in glob.glob(os.path.join(ROOT, "**", "unit-*.md"), recursive=True)})
    for d in dirs:
        build(d)


if __name__ == "__main__":
    main()
