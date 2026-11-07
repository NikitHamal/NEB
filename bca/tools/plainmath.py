#!/usr/bin/env python3
"""Plain-text maths -> typeset `$...$` / `$$...$$` for the BCA course sources.

Four BCA course books were authored with Unicode maths in running prose ("lim (x->a) f(x) = L",
"x^{2}", "d/dx", "[f(x + h) - f(x)]/h"). The PDF then shows a slash, a caret and a
sigma where a textbook shows a built-up fraction, an exponent and a summation. This tool finds the
maths in each prose line and rewrites it as LaTeX that notes/pipeline/mathsvg.py typesets.

    python3 bca/tools/plainmath.py --dry bca/course/semester-1/mathematics-1/unit-03.md
    python3 bca/tools/plainmath.py bca/course/semester-1/mathematics-1/*.md        # rewrite in place

Every converted expression is test-parsed by matplotlib's mathtext. If it does not parse, the
original text is kept, so the tool can never make a source worse. Re-running is a no-op (lines that
already hold `$` are left alone). Fenced blocks (code, svgfig, photogrid), headings, front matter and
`:::` opener lines are never touched.
"""
import os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "notes", "pipeline"))

SUP = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱᵃᵇᶜᵈᵉᶠᵍʰʲᵏˡᵐᵒᵖʳˢᵗᵘᵛʷˣʸᶻ", "0123456789+-=()niabcdefghjklmoprstuvwxyz"))
SUP["ᵀ"] = "T"
SUB = dict(zip("₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₙₖₗₘₛₜᵢⱼₕₚ", "0123456789+-=()aeoxnklmstijhp"))
PRIMES = {"′": "'", "″": "''", "‴": "'''", "⁗": "''''", "’": "'"}
SYM = {
    "×": r"\times", "÷": r"\div", "·": r"\cdot", "⋅": r"\cdot", "−": "-", "–": "-", "≤": r"\leq",
    "≥": r"\geq", "≠": r"\neq", "≈": r"\approx", "→": r"\to", "←": r"\leftarrow", "⇒": r"\Rightarrow",
    "⇔": r"\Leftrightarrow", "↔": r"\leftrightarrow", "⟹": r"\Rightarrow", "∞": r"\infty",
    "∈": r"\in", "∉": r"\notin", "∪": r"\cup", "∩": r"\cap", "⊂": r"\subset", "⊆": r"\subseteq",
    "∅": r"\emptyset", "∂": r"\partial", "∇": r"\nabla", "∀": r"\forall", "∃": r"\exists",
    "¬": r"\neg", "∧": r"\wedge", "∨": r"\vee", "⊕": r"\oplus", "±": r"\pm", "∓": r"\mp",
    "≡": r"\equiv", "∝": r"\propto", "∼": r"\sim", "∘": r"\circ", "°": r"^{\circ}", "∠": r"\angle",
    "⊥": r"\perp", "∥": r"\parallel", "△": r"\triangle", "ℝ": r"\mathbb{R}", "ℕ": r"\mathbb{N}",
    "ℤ": r"\mathbb{Z}", "ℚ": r"\mathbb{Q}", "ℂ": r"\mathbb{C}", "…": r"\ldots", "∴": r"\therefore",
    "∵": r"\because", "∣": r"\mid", "∑": r"\sum", "Σ": r"\sum", "∫": r"\int", "∏": r"\prod",
    "%": r"\%", "⊢": r"\vdash", "⊨": r"\models", "½": r"\frac{1}{2}", "¼": r"\frac{1}{4}", "¾": r"\frac{3}{4}", "⅓": r"\frac{1}{3}", "⌈": r"\lceil", "⌉": r"\rceil", "⌊": r"\lfloor", "⌋": r"\rfloor", "≪": r"\ll", "≫": r"\gg",
}
GREEK = {}
for _n in ("alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho "
           "sigma tau upsilon phi chi psi omega").split():
    for _c, _t in ((_n.upper(), _n.capitalize()), (_n, _n)):
        try:
            _ch = unicodedata.lookup(f"GREEK {'CAPITAL' if _c.isupper() else 'SMALL'} LETTER {_c.upper()}")
        except KeyError:
            continue
        if _n in ("omicron",):
            continue
        GREEK[_ch] = "\\" + _t if _c.islower() or _n in (
            "gamma delta theta lambda xi pi sigma phi psi omega upsilon").split() else _ch
GREEK["λ"] = r"\lambda"; GREEK["Λ"] = r"\Lambda"; GREEK["ε"] = r"\epsilon"; GREEK["φ"] = r"\varphi"; GREEK["ϕ"] = r"\varphi"
for k in list(GREEK):
    if k.isupper() and GREEK[k] == k:
        GREEK[k] = k          # Alpha, Beta... are plain Latin capitals in TeX
GREEK.pop("Σ", None)          # Σ is the summation sign here

FUNCS = ["arcsin", "arccos", "arctan", "cosech", "cosec", "sech", "sinh", "cosh", "tanh", "coth", "sin", "cos", "tan", "cot", "sec",
         "csc", "ln", "log", "exp", "lim", "max", "min", "gcd", "det", "mod", "sup", "inf", "deg", "dim"]
BARE_F = {"det", "gcd", "cosec", "sin", "cos", "tan", "cot", "sec", "csc", "ln", "log", "exp", "lim", "sinh", "cosh", "tanh",
          "arcsin", "arccos", "arctan"}
OPS = set("⊢ ⊨ = + − - × ÷ · ⋅ * < > ≤ ≥ ≠ ≈ ∈ ∉ ∪ ∩ ⊂ ⊆ → ⇒ ⇔ ↔ / ± ∓ ∣ ≡ ∝ ∼ ∘ ∧ ∨ ⊕ ∴ ∵ ≪ ≫ ⟹".split())
MATHCH = set("²³⁴⁵⁶⁷⁸⁹⁰ⁿ⁺⁻⁽⁾₀₁₂₃₄₅₆₇₈₉₊₋ₐₑₓₙ√∫∑Σ∞∈∉∪∩⊂⊆≠≤≥≈→←⇒⇔↔∂∇∀∃¬∧∨⊕±∓≡∝∼∘°′″‴⁗∠⊥∥△ℝℕℤℚℂ∅∴∵×÷"
             "πθλμσαβγδεζηικνξορτυφχψωΔΘΛΞΠΦΨΩΓ⌈⌉⌊⌋≪≫…½¼¾⅓ᵀᵢⱼₕₖₗₘₚₛₜ⊢⊨̄ᵃᵇᶜᵈᵉᶠᵍʰʲᵏˡᵐᵒᵖʳˢᵗᵘᵛʷˣʸᶻ")
UNITS = re.compile(r"^\d+(st|nd|rd|th|cm|mm|km|kg|ml|hrs|hr|min|am|pm|bit|bits|mb|gb|kb|px|pt|hz|khz|mhz|ghz|ma|mw|kw|kv|us|ms|ns|V|A|W)$")
LABEL = re.compile(r"^\(([a-i]|i{1,3}|iv|v|vi{0,3}|ix)\)$")
SPAN_OPEN = {"(": ")", "[": "]"}


class Unsupported(Exception):
    pass


# ------------------------------------------------------------------------------ span -> TeX
class Node:
    __slots__ = ("kind", "tex", "adj", "inner", "br")

    def __init__(self, kind, tex, adj, inner=None, br=None):
        self.kind, self.tex, self.adj, self.inner, self.br = kind, tex, adj, inner, br


ATOMK = {"num", "var", "group", "fn", "sqrt", "frac", "sym"}


def _match(s, i):
    op = s[i]; cl = SPAN_OPEN[op]; depth = 0
    for k in range(i, len(s)):
        if s[k] == op: depth += 1
        elif s[k] == cl:
            depth -= 1
            if depth == 0:
                return k
    return -1


def _wrap_group(op, inner_tex):
    cl = SPAN_OPEN[op]
    if re.search(r"\\(frac|sqrt|sum|int|prod|binom)", inner_tex):
        return f"\\left{op} {inner_tex} \\right{cl}"
    return f"{op}{inner_tex}{cl}"


def _postfix(s, i, base):
    """Collect ^, _, unicode super/subscripts and primes that follow `base`. Returns (tex, i)."""
    sup = sub = ""; primes = ""
    while i < len(s):
        c = s[i]
        if c in PRIMES:
            primes += PRIMES[c]; i += 1
        elif c == "'" and (i + 1 >= len(s) or not s[i + 1].isalpha()):
            primes += "'"; i += 1
        elif c in SUP:
            j = i
            while j < len(s) and s[j] in SUP: j += 1
            sup += "".join(SUP[x] for x in s[i:j]); i = j
        elif c in SUB:
            j = i
            while j < len(s) and s[j] in SUB: j += 1
            sub += "".join(SUB[x] for x in s[i:j]); i = j
        elif c in "^_" and i + 1 < len(s):
            kind = c; j = i + 1
            if s[j] == "{":
                k = j + 1; d = 1
                while k < len(s) and d:
                    d += (s[k] == "{") - (s[k] == "}"); k += 1
                body = to_tex(s[j + 1:k - 1]); i = k
            elif s[j] == "(":
                k = _match(s, j)
                if k < 0: break
                body = to_tex(s[j + 1:k]); i = k + 1
            else:
                m = re.match(r"[-+−]?(?:\d+|[A-Za-z]|[α-ωΑ-Ω]|∞)", s[j:])
                if not m: break
                body = to_tex(m.group()); i = j + m.end()
            if kind == "^": sup += "{" + body + "}" if sup == "" or not sup else body
            else: sub += "{" + body + "}" if not sub else body
        else:
            break
    out = base + primes
    if sub: out += "_{" + sub.strip("{}") + "}" if not sub.startswith("{") else "_" + sub
    if sup: out += "^{" + sup.strip("{}") + "}" if not sup.startswith("{") else "^" + sup
    return out, i


def to_tex(s):
    nodes, i, sp = [], 0, False
    n = len(s)
    summed = False
    while i < n:
        c = s[i]
        if c.isspace():
            sp = True; i += 1; continue
        adj = not sp and bool(nodes); sp = False
        if c == "\u0001":
            k = s.index("\u0001", i + 1); nodes.append(Node("group", MATS[int(s[i + 1:k])], adj, br="m")); i = k + 1; continue
        if c in "0123456789":
            m = re.match(r"\d+(?:\.\d+)?", s[i:])
            tex, i = _postfix(s, i + m.end(), m.group())
            nodes.append(Node("num", tex, adj)); continue
        if c.isalpha() and c.isascii():
            m = re.match(r"[A-Za-z]+", s[i:]); run = m.group(); j = i + m.end(); first = True
            if j < n and s[j] == "\u0304":
                if len(run) > 1:
                    for ch in run[:-1]:
                        nodes.append(Node("var", ch, adj if first else True)); first = False
                tex, i = _postfix(s, j + 1, "\\bar{" + run[-1] + "}")
                nodes.append(Node("var", tex, adj if first else True)); continue
            while run:
                fm = next((f for f in FUNCS if run.startswith(f) and (len(run) == len(f) or len(run) - len(f) <= 2
                                                                      or f in ("lim", "log", "ln"))), None)
                if fm and (len(run) == len(fm) or len(fm) >= 2):
                    run = run[len(fm):]
                    if not run:
                        tex, i = _postfix(s, j, ("\\csc" if fm == "cosec" else "\\mathrm{cosech}" if fm == "cosech" else "\\" + fm) if fm not in ("mod", "deg", "dim", "sup", "inf", "gcd", "det") else
                                          {"mod": r"\mathrm{mod}", "deg": r"\deg", "dim": r"\mathrm{dim}",
                                           "sup": r"\sup", "inf": r"\inf", "gcd": r"\gcd", "det": r"\det"}[fm])
                    else:
                        tex = ("\\csc" if fm == "cosec" else "\\" + fm) if fm not in ("mod", "dim") else r"\mathrm{" + fm + "}"
                    nodes.append(Node("fn", tex, adj if first else True)); first = False
                    if not run: break
                    continue
                if len(run) >= 4 or (len(run) == 3 and (run in ENG or not set(run) <= VARSET)):
                    nodes.append(Node("var", r"\mathrm{" + run + "}", adj if first else True)); i = j; run = ""; break
                ch = run[0]; run = run[1:]
                if run:
                    nodes.append(Node("var", ch, adj if first else True))
                else:
                    tex, i = _postfix(s, j, ch)
                    nodes.append(Node("var", tex, adj if first else True))
                first = False
            continue
        if c in GREEK:
            tex, i = _postfix(s, i + 1, GREEK[c]); nodes.append(Node("var", tex, adj)); continue
        if c == "√":
            nodes.append(Node("sqrtmark", "", adj)); i += 1; continue
        if c in SUP and not nodes or (c in SUP and nodes and nodes[-1].kind in ("op", "punct")):
            j = i
            while j < n and s[j] in SUP: j += 1
            if j < n and s[j] == "√":
                nodes.append(Node("sqrtmark", "[" + "".join(SUP[x] for x in s[i:j]) + "]", adj)); i = j + 1; continue
            raise Unsupported(c)
        if c in "∫∑Σ∏":
            tex, i = _postfix(s, i + 1, SYM[c]); nodes.append(Node("sym", tex, adj))
            summed = summed or c == "∫"; continue
        if c in "([":
            k = _match(s, i)
            if k < 0:
                nodes.append(Node("open", c, adj)); i += 1; continue
            inner = s[i + 1:k]
            tex, i = _postfix(s, k + 1, "")
            itex = to_tex(inner)
            nodes.append(Node("group", _wrap_group(c, itex) + tex, adj, inner=itex, br=c)); continue
        if c in ")]":
            nodes.append(Node("close", c, adj)); i += 1; continue
        if c == "{":
            k = s.find("}", i)
            if k < 0: raise Unsupported(s)
            nodes.append(Node("group", "\\{" + to_tex(s[i + 1:k]) + "\\}", adj)); i = k + 1; continue
        if c == "|":
            k = s.find("|", i + 1)
            if k > i + 1 and not s[i + 1].isspace() and not s[k - 1].isspace():
                itex = to_tex(s[i + 1:k]); tex, i = _postfix(s, k + 1, "")
                nodes.append(Node("group", "|" + itex + "|" + tex, adj, inner=itex, br="|")); continue
            nodes.append(Node("op", r"\mid", adj)); i += 1; continue
        if c in SYM:
            tex = SYM[c]
            if tex == r"\ldots" or c == "…":
                nodes.append(Node("sym", tex, adj)); i += 1; continue
            if c in "°∞∅∂∇ℝℕℤℚℂ∠△":
                t2, i = _postfix(s, i + 1, tex); nodes.append(Node("var" if c != "°" else "sup", t2, adj)); continue
            nodes.append(Node("op", tex, adj)); i += 1; continue
        if s.startswith("...", i):
            nodes.append(Node("sym", r"\ldots", adj)); i += 3; continue
        if c in "=+-<>/*:!~&":
            if c == "!":
                nodes.append(Node("sym", "!", adj)); i += 1; continue
            nodes.append(Node("op", {"*": r"\ast", "~": r"\sim"}.get(c, c), adj)); i += 1; continue
        if c in ",;":
            nodes.append(Node("punct", c + r"\ ", adj)); i += 1; continue
        if c == ".":
            nodes.append(Node("punct", ".", adj)); i += 1; continue
        raise Unsupported(c)

    # sqrt marks consume the next atom
    out, k = [], 0
    while k < len(nodes):
        nd = nodes[k]
        if nd.kind == "sqrtmark":
            if k + 1 >= len(nodes): raise Unsupported("sqrt")
            nx = nodes[k + 1]
            body = nx.inner if nx.kind == "group" and (nx.br or "x") in "([" and "^" not in nx.tex[-3:] else nx.tex
            if nx.kind == "group" and (nx.br or "x") in "([" and re.search(r"[\^_']$|\^\{[^}]*\}$", nx.tex) and nx.inner is not None:
                body = nx.tex
            out.append(Node("sqrt", "\\sqrt" + nd.tex + "{" + body + "}", nd.adj)); k += 2; continue
        out.append(nd); k += 1
    nodes = out
    # lim with a (x -> a) group becomes \lim_{x \to a}
    out, k = [], 0
    while k < len(nodes):
        nd = nodes[k]
        if nd.kind == "fn" and nd.tex == r"\lim" and k + 1 < len(nodes) and nodes[k + 1].kind == "group" \
                and nodes[k + 1].br == "(" and r"\to" in (nodes[k + 1].inner or ""):
            out.append(Node("fn", r"\lim_{" + nodes[k + 1].inner + "}", nd.adj)); k += 2; continue
        out.append(nd); k += 1
    nodes = out
    nodes = _fractions(nodes)
    if summed:
        res = []
        for nd in nodes:
            if nd.kind == "var" and nd.tex == "d" and res and res[-1].kind != "op":
                res.append(Node("punct", r"\,", True))
            res.append(nd)
        nodes = res
    return " ".join(nd.tex for nd in nodes).replace("\\, ", "\\,").strip()


def _strip_one(chain):
    if len(chain) == 1 and chain[0].kind == "group" and (chain[0].br or "x") in "([" and chain[0].inner is not None \
            and chain[0].tex.endswith(")" if chain[0].br == "(" else "]") and not re.search(r"[\^_]", chain[0].tex[-6:]) :
        return chain[0].inner
    return " ".join(x.tex for x in chain)


def _fractions(nodes):
    while True:
        idx = next((k for k, nd in enumerate(nodes) if nd.kind == "op" and nd.tex == "/"), None)
        if idx is None:
            return nodes
        if idx == 0 or idx == len(nodes) - 1:
            nodes[idx] = Node("op", "/", nodes[idx].adj); nodes[idx].kind = "slash"; continue
        a = idx - 1
        if nodes[a].kind not in ATOMK:
            nodes[idx].kind = "slash"; continue
        while a > 0 and nodes[a - 1].kind in ATOMK and not (nodes[a - 1].kind == "fn" and nodes[a - 1].tex.startswith(
                ("\\lim", "\\max", "\\min", "\\sup", "\\inf"))):
            if not nodes[a].adj and nodes[a - 1].kind == "frac":
                break
            a -= 1
        b = idx + 1
        if nodes[b].kind not in ATOMK:
            nodes[idx].kind = "slash"; continue
        if nodes[b].kind == "fn" and b + 1 < len(nodes) and nodes[b + 1].kind in ATOMK:
            b += 1
        while b + 1 < len(nodes) and nodes[b + 1].adj and nodes[b + 1].kind in ATOMK:
            if nodes[b + 1].kind == "group" and nodes[b].kind == "var" and b > idx + 1 \
                    and nodes[idx + 1].tex == "d" and b == idx + 2:
                break
            if nodes[b + 1].kind == "group" and nodes[b].kind == "var" and nodes[b].tex in ("x", "y", "t", "z", "u") \
                    and nodes[idx + 1].tex == "d" and b == idx + 2:
                break
            b += 1
        left, right = nodes[a:idx], nodes[idx + 1:b + 1]
        if all(x.kind == "num" for x in left + right) and any(len(x.tex) >= 3 for x in left + right):
            nodes[idx].kind = "slash"; continue
        tex = "\\frac{" + _strip_one(left) + "}{" + _strip_one(right) + "}"
        nodes[a:b + 1] = [Node("frac", tex, nodes[a].adj)]
    return nodes


# ------------------------------------------------------------------------------ prose scanning
ENG = set("""ms mb gb kb kg cm mm km hz ns us ml mhz ghz nth th rd nd st am an as at be by do go he if in is it me my no of on or so to up us we ex ok id
and are but can for has how its may not now one our the two use was who why yes you any all get new out let say
too via did off own put run sum top end key row way cut due few gap her him his big bit box buy car day eye far
fit fun hit hot job law lot low map mix net old pay per raw red sat sea set sit six ten tie tin use war win
add age ago aim air bad bar bed bus cap cat cup dot dry eat fan fix fly fur gas gun hat ice ink key kid lay led
leg lie lip log mad man mud nor oil pen pet pie pin pot rat ray rub sad sky sun tax tea tip toy van vet wet
yet zip""".split())
ACR = set("TU BCA CPU RAM ROM NEB IT OS DB PC AI ML UI UX ID IP OK US UK EU UN TV GK DNE LAN WAN CSS SQL XML PDF URL API DOS GUI IDE SDK ERP CRM HTML HTTP FIFO LIFO ALU ASCII CD DVD USB GPU DNS ISP VPN MAC LED LCD ISO CGPA CEE IOE MCQ NB Q A B C".split())
VARSET = set("abcdhkmnpqrstuvwxyz")


def _strip_br(core):
    """Drop leading ( [ and trailing ) ] that are not closed/opened inside the word."""
    lead = re.match(r"^[\(\[]*", core).group()
    while lead and core[len(lead):].count(")") + core[len(lead):].count("]") and False:
        break
    t = core[len(lead):]
    tail = ""
    while t and t[-1] in ")]" and t.count(")") + t.count("]") > t.count("(") + t.count("["):
        tail = t[-1] + tail; t = t[:-1]
    return t


def classify(word):
    """-> (class, core, trail). class in M strong, O operator, W weak, F function word, T text."""
    m = re.match(r"^(.*?)([.,;:!?]+)$", word)
    core, trail = (m.group(1), m.group(2)) if m and m.group(1) else (word, "")
    if re.fullmatch(r"(\.\.\.|…),?", word):
        return "W", "…", "," if word.endswith(",") else ""
    if not core:
        return "T", word, ""
    if "\u0001" in core:
        return "M", core, trail
    if trail.startswith("!") and re.search(r"(\d|\)|^[\(\[]*[A-Za-z])$", core) and not re.fullmatch(r"[A-Za-z]{2,}", core):
        return "M", core + "!", trail[1:]
    if core in OPS:
        return "O", core, trail
    x = _strip_br(core)
    if not x:
        return "T", core, trail
    if re.fullmatch(r"\d+(\.\d+)?[eE][+\-−]?\d+|\d+\s?[–-]\s?\d+", x):
        return "T", core, trail
    if x in BARE_F:
        return "F", core, trail
    if LABEL.match(core):
        return "T", core, trail
    if re.fullmatch(r"[A-Za-z]", x):
        return "W", core, trail
    if re.fullmatch(r"[+\-−]?\d+(?:\.\d+)?", x):
        return "W", core, trail
    if re.fullmatch(r"[a-z]{2,3}", x) and x in FUNCS:
        return "T", core, trail
    if re.fullmatch(r"[A-Z]{2,3}", x) and x not in ACR:
        return "U", core, trail
    if re.fullmatch(r"[a-z]{2,3}", x):
        if x not in ENG and set(x) <= VARSET and not (len(x) == 3 and x[0] == x[1] == x[2]):
            return "W", core, trail
        return "T", core, trail
    if any(ch in MATHCH for ch in x) and not re.fullmatch(r"[A-Za-z]{4,}\W*", x):
        return "M", core, trail
    if "^" in x or re.search(r"_[\w{(]", x) or "..." in x:
        return "M", core, trail
    if re.search(r"(?<![A-Za-z])(?:\d+[a-z]?|[A-Za-z])\(|\)\(", x) and not re.search(r"[A-Za-z]{2,}\(", x.replace("sin(","").replace("cos(","").replace("tan(","").replace("ln(","").replace("log(","")):
        return "M", core, trail
    if re.search(r"(?<![A-Za-z])(?:sin|cos|tan|cot|sec|csc|cosec|ln|log|exp|lim|det|gcd|max|min|sinh|cosh|tanh)\(", x):
        return "M", core, trail
    if re.match(r"^[A-Za-z]\(", x) and not re.match(r"^[A-Za-z]\(s\)", x):
        return "M", core, trail
    if re.match(r"^[A-Za-z]['’′]+", x) and not re.match(r"^[A-Za-z]['’′]+[A-Za-z]", x):
        return "M", core, trail
    if re.fullmatch(r"\|.+\|", x) and " " not in x:
        return "M", core, trail
    if re.search(r"[A-Za-z0-9\)]\s*[=<>]\s*[A-Za-z0-9\(\-−]", x):
        return "M", core, trail
    if re.fullmatch(r"[+\-−]?\d+[a-z]{1,3}", x) and not UNITS.match(x) and set(x.lstrip("+-−0123456789")) <= set("xyzabcdhknt"):
        return "M", core, trail
    if re.search(r"[+\-−×*/]", x) and re.fullmatch(r"[\w.(\[|)\]²³⁴ⁿ'′+\-−×*/^{}!⁺⁻ᵃ-ᶻ]+", x):
        pieces = [p for p in re.split(r"[+\-−×*/]", x.strip("()[]")) if p]
        bad = [p for p in pieces if len(re.sub(r"[^A-Za-z]", "", p)) >= 2 and not re.fullmatch(r"d[xyztuvrsw]", p)
               and p not in FUNCS and not (set(p) <= VARSET and len(p) <= 3 and p not in ENG) \
               and not re.search(r"[²³ⁿ'′^{(]", p)]
        if re.fullmatch(r"[A-Z](/[A-Z])+", x):
            return "T", core, trail
        if not bad and pieces and any(re.search(r"\d|[A-Za-z]", p) for p in pieces) \
                and not re.fullmatch(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", x) and not re.fullmatch(r"[A-Za-z]+-[A-Za-z]+", x) \
                and not re.fullmatch(r"[\d]{3,}/[\d]+|[\d]+/[\d]{3,}", x):
            return "M", core, trail
    return "T", core, trail


def _valid(run):
    toks = [t for t in run if t[0] != "O"]
    if not toks:
        return False
    if any(t[0] == "M" for t in toks):
        return True
    if all(t[0] == "F" or t[1] in ("a", "A", "I") for t in toks):
        return False
    if any(t[0] == "F" for t in toks) and len(toks) >= 2:
        return True
    if any(t[0] == "O" for t in run) and len([t for t in toks if t[0] not in "F"]) >= 2:
        return True
    letters = [t for t in toks if t[0] == "W" and re.search(r"[a-z]", t[1]) and t[1].strip("()[]") not in ("a",)]
    if letters and len(toks) == 1:
        return True
    if len(toks) >= 2 and letters and all(t[0] == "W" for t in toks):
        return True
    return False


def _trim(run):
    """Remove edge tokens that are English ("a", "I") or bare numbers that touch no operator."""
    while run and run[0][0] == "O":
        run = run[1:]
    while run and run[-1][0] == "O":
        run = run[:-1]
    changed = True
    while changed and len(run) > 1:
        changed = False
        for pos in (0, -1):
            t = run[pos]; nb = run[1] if pos == 0 else run[-2]
            bare = (t[0] == "W" and not t[3] and (t[1] in ("a", "A", "I") or re.fullmatch(r"[\(\[]*\d+(\.\d+)?[\)\]]*", t[1]))) or t[0] == "U"
            if bare and nb[0] not in ("O", "F") and not (t[3] == "," if pos == -1 else False):
                run = run[1:] if pos == 0 else run[:-1]; changed = True; break
    return run


def _balance(text):
    lead = trail = ""
    for op, cl in (("(", ")"), ("[", "]")):
        while text.count(op) > text.count(cl) and text.startswith(op):
            lead += op; text = text[1:]
        while text.count(cl) > text.count(op) and text.endswith(cl):
            trail = cl + trail; text = text[:-1]
    return lead, text, trail


_parser = None
LOG = {"ok": 0, "fallback": []}


def _parses(tex):
    global _parser
    if _parser is None:
        import mathsvg
        from matplotlib.mathtext import MathTextParser
        _parser = (mathsvg, MathTextParser("path"))
    mathsvg, p = _parser
    from matplotlib.font_manager import FontProperties
    try:
        p.parse("$" + mathsvg._clean(tex) + "$", dpi=100, prop=FontProperties(size=10))
        return True
    except Exception:
        return False


MATS = []
MAT = re.compile(r"\[\s*(\[[^\[\]]*\](?:\s*,\s*\[[^\[\]]*\])+)\s*\]")


def _matrix(m):
    rows = re.findall(r"\[([^\[\]]*)\]", m.group(1))
    try:
        body = " \\\\ ".join(" & ".join(to_tex(c.strip()) for c in r.split(",")) for r in rows)
    except Unsupported:
        return None
    tex = "\\begin{bmatrix} " + body + " \\end{bmatrix}"
    return tex if _parses(tex) else None


def convert_text(text, display=False):
    if "[[" in text.replace("[ [", "[["):
        def keep(m):
            t = _matrix(m)
            if t is None:
                return m.group(0)
            MATS.append(t); return f"\u0001{len(MATS) - 1}\u0001"
        text = MAT.sub(keep, text)
        res = _convert_text(text, display=False)
        return re.sub(r"\u0001(\d+)\u0001", lambda m: "$" + MATS[int(m.group(1))] + "$", res)
    return _convert_text(text, display)


def _convert_text(text, display=False):
    """Convert one prose string. With display=True, return ('display', tex) if the whole string is
    one substantial formula, else the converted string."""
    words = []
    for m in re.finditer(r"\S+", text):
        if words and words[-1][3] > 0:
            w0, s0, e0, dep = words[-1]
            w = w0 + text[e0:m.end()]
            words[-1] = (w, s0, m.end(), w.count("{") - w.count("}"))
        else:
            w = m.group()
            words.append((w, m.start(), m.end(), w.count("{") - w.count("}")))
    words = [(w, s0, e0) for w, s0, e0, _ in words]
    cls = []
    for w, s0, e0 in words:
        c, core, trail = classify(w)
        cls.append([c, core, s0, trail, e0])
    runs, cur = [], []
    for t in cls:
        if t[0] == "T":
            if cur: runs.append(cur); cur = []
            continue
        cur.append(t)
        if t[3] and t[3].strip(",;") != "":     # . : ! ? close the run after this word
            runs.append(cur); cur = []
        elif t[3] and not t[3].strip(",;") and False:
            pass
    if cur: runs.append(cur)
    pieces, last = [], 0
    spans = []
    for run in runs:
        # a trailing comma/semicolon ends the run unless the next word continues it
        r = _trim(run)
        if not r or not _valid(r):
            continue
        # split at words whose trail is , or ; when the following word is text (handled by run order)
        a, b = r[0][2], r[-1][4] - len(r[-1][3])
        raw = text[a:b]
        lead, core_txt, trail = _balance(raw)
        a2, b2 = a + len(lead), b - len(trail)
        if not core_txt.strip():
            continue
        spans.append((a2, b2, core_txt))
    out = []
    for a, b, raw in spans:
        out.append(text[last:a])
        try:
            tex = to_tex(raw)
            if not tex or "$" in tex or not _parses(tex):
                raise Unsupported(raw)
            if re.fullmatch(r"[A-Za-z]|\\[a-z]+", tex) and tex not in ("\\infty",) and "\\" not in tex[1:]:
                out.append("*" + raw.strip() + "*")
            else:
                out.append("$" + tex + "$")
            LOG["ok"] += 1
            spans_tex = tex
        except Unsupported:
            LOG["fallback"].append(raw); out.append(raw)
        last = b
    out.append(text[last:])
    res = "".join(out)
    if display and len(spans) == 1 and spans[0][0] == 0 and text[spans[0][1]:].strip(" .") == "":
        tex = res[1:res.index("$", 1)] if res.startswith("$") else ""
        if tex and (re.search(r"\\(frac|lim|int|sum|prod|sqrt)", tex) or len(tex) > 28):
            return ("display", tex)
    return res


def _esc_pipes(txt):
    parts = txt.split("$")
    for i in range(0, len(parts), 2):
        parts[i] = parts[i].replace("|", "\\|")
    return "$".join(parts)


def convert_line(line):
    if "$" in line:
        return [line]
    m = re.match(r"^(\s*(?:[-*+] |\d+[.)] |> )*)(.*)$", line)
    prefix, rest = m.group(1), m.group(2)
    if rest.startswith("|") and rest.rstrip().endswith("|"):
        if re.fullmatch(r"[|\s:\-]+", rest):
            return [line]
        cells = re.split(r"(?<!\\)\|", rest.strip()[1:-1])
        conv = [_esc_pipes(_conv_segments(c.strip().replace("\\|", "|"))[0]) for c in cells]
        return [prefix + "| " + " | ".join(conv) + " |"]
    body, disp = _conv_segments(rest, allow_display=(prefix.strip() == ""))
    if disp:
        return ["", "$$" + disp + "$$", ""]
    return [prefix + body]


def _conv_segments(rest, allow_display=False):
    plain = rest.strip()
    if allow_display:
        inner = plain
        if inner.startswith("**") and inner.rstrip(".").endswith("**") and inner.count("**") == 2:
            inner = inner.strip("*")
        if "**" not in inner and "`" not in inner:
            r = convert_text(inner.rstrip(), display=True)
            if isinstance(r, tuple):
                return "", r[1]
    parts = re.split(r"(`[^`]*`|\[[^\]]*\]\([^)]*\)|</?[A-Za-z][^>]*>)", rest)
    for i in range(0, len(parts), 2):
        segs = re.split(r"(\*\*)", parts[i])
        for j in range(0, len(segs), 2):
            segs[j] = convert_text(segs[j])
        parts[i] = "".join(segs)
    return "".join(parts), None


def convert_file(src):
    lines = src.split("\n")
    out, fence, fm, block = [], False, False, False
    for idx, line in enumerate(lines):
        if idx == 0 and line.strip() == "---":
            fm = True; out.append(line); continue
        if fm:
            if line.strip() == "---": fm = False
            out.append(line); continue
        if line.lstrip().startswith("```"):
            fence = not fence; out.append(line); continue
        if fence or line.startswith("#") or not line.strip():
            out.append(line); continue
        if line.startswith(":::"):
            block = line.strip() != ":::"
            out.append(line); continue
        new = convert_line(line)
        if block and not re.match(r"^\s*([-*+] |\d+[.)] )", line) and out and out[-1].strip() \
                and not out[-1].startswith(":::") and not re.match(r"^\s*([-*+] |\d+[.)] )", out[-1]):
            out.append("")
        out.extend(new)
    res = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", res)


def convert_captions(src):
    """Only the caption="..." text on opening ``` lines (figure and plate captions)."""
    out = []
    for line in src.split("\n"):
        if line.startswith("```") and 'caption="' in line:
            def one(m):
                t = m.group(1)
                return 'caption="' + (t if "$" in t else convert_text(t)) + '"'
            line = re.sub(r'caption="([^"]*)"', one, line)
        out.append(line)
    return "\n".join(out)


def main(argv):
    if "--captions" in argv:
        for f in [a for a in argv if not a.startswith("--")]:
            src = open(f, encoding="utf8").read()
            new = convert_captions(src)
            if new != src:
                open(f, "w", encoding="utf8").write(new)
        return
    dry = "--dry" in argv
    files = [a for a in argv if not a.startswith("--")]
    for f in files:
        if os.path.basename(f) in ("README.md", "SPINE.md"):
            continue
        src = open(f, encoding="utf8").read()
        new = convert_file(src)
        if dry:
            import difflib
            for l in difflib.unified_diff(src.split("\n"), new.split("\n"), lineterm="", n=0):
                if l.startswith(("+", "-")) and not l.startswith(("+++", "---")):
                    print(l[:420])
        elif new != src:
            open(f, "w", encoding="utf8").write(new)
        print(f"# {f}: ok={LOG['ok']} fallback={len(LOG['fallback'])}", file=sys.stderr)
    if LOG["fallback"]:
        print("FALLBACKS:", file=sys.stderr)
        for r in LOG["fallback"][:60]:
            print("  ", r[:120], file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
