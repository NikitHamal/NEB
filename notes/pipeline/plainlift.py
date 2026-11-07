"""Lift mathematics that was typed as plain text into real TeX before the page is built.

Authors and the older migrations left stray `x^2`, `O(b^d)`, `dy/dx`, `sqrt(x)`, `(a+b)/(c+d)`
and ASCII arrows in running prose and tables. Printed as typed they look like a terminal, not
like a textbook. `lift()` rewrites only what is unmistakable and only outside code and outside
existing maths, so a book that is already clean comes back byte for byte.

Used by `md2html.convert`, so the PDF books, the website reader and the app all get it.
"""
import re

_PROTECT = re.compile(
    r"(^```.*?^```[^\n]*$|^~~~.*?^~~~[^\n]*$|`[^`\n]+`|\$\$.*?\$\$|\\\$|(?<!\$)\$(?!\$)[^$\n]*\$(?!\$))",
    re.S | re.M)
_SKIP_LINE = re.compile(r"^\s*(#{1,6}\s|:::|\|?\s*:?-{3,}|<)")

_GREEK = {"ε": "varepsilon", "π": "pi", "θ": "theta", "Δ": "Delta", "σ": "sigma", "μ": "mu", "λ": "lambda",
          "α": "alpha", "β": "beta", "γ": "gamma", "ω": "omega", "τ": "tau", "φ": "varphi", "ρ": "rho"}
_SUP = {"²": "2", "³": "3", "¹": "1"}

# O(b^d), O(n^2 log n), O(b^(d/2)): up to two levels of parentheses, ASCII only
_BIGO = re.compile(r"(?<![\w$\\])([OΘΩ])\(((?:[^()\n$`*|]|\([^()\n]*\))*\^(?:[^()\n$`*|]|\([^()\n]*\))*)\)")
_POW = re.compile(
    r"(?<![\w$\\^.])([A-Za-z]|\d+(?:\.\d+)?|\))\^(\([^()\n]+\)|-?\d+(?:\.\d+)?|-?[A-Za-z])(?![\w^])")
_SMALLO = re.compile(r"(?<![\w$\\])([OΘΩ])\(([A-Za-z0-9 +*/.\-]{1,24})\)(?![\w(])")
_DERIV = re.compile(r"(?<![\w$\\/])d([A-Za-z]?)/d([a-z])(?![\w(])")
_SQRT = re.compile(r"(?<![\w$\\])sqrt\(([^()\n$`|]{1,40})\)")
_PFRAC = re.compile(r"(?<![\w$\\])\(([^()\n$`|%&#]{1,36})\)\s?/\s?\(([^()\n$`|%&#]{1,36})\)(?![\w(])")
_ARROW = re.compile(r"(?<=\s)->(?=\s)")
_CMP = {"<=": "≤", ">=": "≥", "!=": "≠"}
_CMP_RE = re.compile(r"(?<=\s)(<=|>=|!=)(?=\s)")


def _tex(expr):
    expr = expr.strip()
    for k, v in _SUP.items():
        expr = expr.replace(k, "^{%s}" % v)
    expr = expr.replace("−", "-").replace("×", r"\times ").replace("·", r"\cdot ").replace("÷", r"\div ")
    for k, v in _GREEK.items():
        expr = expr.replace(k, "\\%s " % v)
    return expr


def _group(exp):
    if exp.startswith("(") and exp.endswith(")"):
        exp = exp[1:-1]
    return "{%s}" % _tex(exp)


def _bigo(m):
    body = m.group(2)
    body = _tex(body)
    body = re.sub(r"\^\(([^()\n]*)\)", lambda x: "^{%s}" % x.group(1), body)
    body = re.sub(r"\^(-?[A-Za-z0-9]+)", lambda x: "^{%s}" % x.group(1), body)
    body = re.sub(r"\blog\b", r"\\log ", body)
    return "$%s(%s)$" % (m.group(1), body)


def _pow(m):
    base, exp = m.group(1), m.group(2)
    if base == ")":                       # (a+b)^2 is left to the author
        return m.group(0)
    return "$%s^%s$" % (base, _group(exp) if exp.startswith("(") else "{%s}" % exp)


def _smallo(m):
    inner = m.group(2)
    if re.search(r"[A-Za-z]{3,}", re.sub(r"\blog\b", "", inner)):
        return m.group(0)
    return "$%s(%s)$" % (m.group(1), re.sub(r"\blog\b", r"\\log ", inner).replace("*", r"\cdot "))


def _deriv(m):
    num, var = m.group(1), m.group(2)
    return r"$\dfrac{d%s}{d%s}$" % (num, var)


def _sqrt(m):
    return r"$\sqrt{%s}$" % _tex(m.group(1))


def _pfrac(m):
    a, b = m.group(1), m.group(2)
    # words in brackets are prose, not a fraction: "(distance travelled) / (time taken)"
    if re.search(r"[A-Za-z]{3,}", re.sub(r"\b(?:sin|cos|tan|log|ln|exp|dy|dx|dt|dz|du|dv)\b", "", a + " " + b)):
        return m.group(0)
    a, b = (re.sub(r"\b([A-Za-z])(\d)\b", r"\1_\2", x) for x in (a, b))
    a, b = (_DERIV.sub(lambda m: r"\dfrac{d%s}{d%s}" % m.groups(), _tex(x)) for x in (a, b))
    return r"$\dfrac{%s}{%s}$" % (a, b)


def _plain(seg):
    seg = _BIGO.sub(_bigo, seg)
    seg = _PFRAC.sub(_pfrac, seg)
    seg = _DERIV.sub(_deriv, seg)
    seg = _SQRT.sub(_sqrt, seg)
    seg = _SMALLO.sub(_smallo, seg)
    seg = _POW.sub(_pow, seg)
    seg = _ARROW.sub("→", seg)
    return _CMP_RE.sub(lambda m: _CMP[m.group(1)], seg)


# ---- reactions typed as  A + B --cond--> C  (chemistry, every grade) ----------------------------
_SUBS = dict(zip("₀₁₂₃₄₅₆₇₈₉", "0123456789"))
_SUPS = {"⁺": "+", "⁻": "-", "²": "2", "³": "3"}
_RXN = re.compile(r"--([^>\n$`|]{0,60}?)-->")
_SPECIES = re.compile(
    r"^\d*(?:[A-Z][a-z]?[0-9₀-₉]*|\((?:[A-Za-z0-9₀-₉=]+)\)[0-9₀-₉]*|[=≡·.\-])+(?:[⁺⁻]|\^?\d*[+-])?[↑↓]?$")


def _cond(c):
    """Condition over the arrow: 'Cu, 573 K', 'Δ, −H₂O', 'dil. NaOH, 280 K' -> TeX."""
    out = []
    for piece in [x.strip() for x in re.split(r",(?![^()]*\))", c) if x.strip()]:
        piece = piece.replace("−", "-")
        if piece == "Δ":
            out.append(r"\Delta")
            continue
        t, buf = "", ""
        for ch in piece:
            if ch in _SUBS:
                t += (r"\text{%s}" % buf if buf else "") + "_{%s}" % _SUBS[ch]
                buf = ""
            else:
                buf += ch
        t += r"\text{%s}" % buf if buf else ""
        out.append(t)
    return r",\ ".join(out)


def _rxn_side(side):
    """One side of a reaction -> mhchem, or None when it holds anything but formulas."""
    toks = side.split()
    if not toks:
        return None
    for t in toks:
        if t in ("+", "→", "⇌", "<=>", "->"):
            continue
        if not _SPECIES.match(t):
            return None
    return side


def _ce(seg):
    if seg.count("-->") < 1:
        return None
    parts = _RXN.split(seg)       # side, cond, side, cond, side ...
    if len(parts) < 3 or len(parts) % 2 == 0:
        return None
    sides = parts[0::2]
    note = ""
    m = re.search(r"\s{2,}\(.*\)\s*$|\s\([a-z][^()]*\)\s*$", sides[-1])
    if m:
        note, sides[-1] = m.group(0).strip(), sides[-1][:m.start()]
    if any(_rxn_side(x.strip()) is None for x in sides):
        return None
    out = ""
    for i, sd in enumerate(sides):
        sd = sd.strip().replace("−", "-").replace("·", ".").replace("⇌", "<=>").replace("→", "->")
        sd = "".join(_SUBS.get(c, c) for c in sd)
        sd = re.sub(r"([A-Za-z0-9)])([⁺⁻])", lambda m: "%s^%s" % (m.group(1), _SUPS[m.group(2)]), sd)
        sd = sd.replace("↑", "^").replace("↓", "v")
        out += sd + (" " if i < len(sides) - 1 else "")
        if i < len(sides) - 1:
            out += "->[%s] " % _cond(parts[2 * i + 1])
    tex = r"\ce{%s}" % out.strip()
    return tex, note


def _arrow_inline(seg):
    return _RXN.sub(lambda m: r"$\xrightarrow{%s}$" % _cond(m.group(1)), seg)


def _react(seg):
    """Reaction lines become a display equation; any other `--cond-->` becomes a typeset arrow."""
    if "-->" not in seg:
        return seg
    cells = seg.split("|")
    if len(cells) > 1:
        return "|".join(_react(c) if "-->" in c else c for c in cells)
    m = re.match(r"^(\s*(?:[-*]\s+|\d+\.\s+)?)(.*?)\s*$", seg)
    lead, core = m.group(1), m.group(2)
    r = _ce(core)
    if r and not lead.strip():
        tex, note = r
        return "$$%s$$" % tex + (("\n\n" + note) if note else "")
    if r:
        return lead + "$%s$" % r[0] + ((" " + r[1]) if r[1] else "")
    return _arrow_inline(seg)


def _line(seg):
    if _SKIP_LINE.match(seg) or "$" in seg:     # a stray $ (money) would pair with ours
        return seg
    if "-->" in seg:
        seg = _react(seg)
    return _plain(seg) if "$" not in seg else seg


def lift(body):
    """Rewrite plain-text maths outside code and outside $...$."""
    parts = _PROTECT.split(body)
    for i in range(0, len(parts), 2):
        parts[i] = "\n".join(_line(l) for l in parts[i].split("\n"))
    return "".join(parts)


if __name__ == "__main__":      # dry run:  python plainlift.py file.md ...
    import sys
    for path in sys.argv[1:]:
        text = open(path, encoding="utf-8").read()
        new = lift(text)
        if new != text:
            for a, b in zip(text.split("\n"), new.split("\n")):
                if a != b:
                    print(path, "|", a.strip()[:110], "\n   ->", b.strip()[:140])
