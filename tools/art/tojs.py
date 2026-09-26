import os
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
#!/usr/bin/env python3
"""
A JavaScript backend for the same Kotlin transpiler that drives the previews.

The point is parity that cannot rot. The app draws 67 banner arts and 7 profile
cover motifs from Kotlin; the website used to draw flat gradients. Rather than
transcribe 4,400 lines of drawing code into JS by hand -- which would be wrong
within a week -- this reads the shipping Kotlin and emits the JS, so both
platforms run the same arithmetic on the same seeds and produce the same
picture. Re-run it whenever the Kotlin changes.
"""
import sys, re, json
sys.path.insert(0, _HERE)
import render as R

BANNER_KT = os.path.join(_ROOT, "app/src/main/java/com/neb/ians/ui/components/ResourceBannerArt.kt")
COVER_KT = os.path.join(_ROOT, "app/src/main/java/com/neb/ians/ui/components/ProfileCoverArt.kt")

# ------------------------------------------------------------- expressions ---
JS_POSTFIX = {
    "toInt": lambda rv, a: "Math.trunc(%s)" % rv,
    "coerceIn": lambda rv, a: "Math.min(Math.max(%s, %s), %s)" % (rv, a[0], a[1]),
    "coerceAtLeast": lambda rv, a: "Math.max(%s, %s)" % (rv, a[0]),
    "coerceAtMost": lambda rv, a: "Math.min(%s, %s)" % (rv, a[0]),
}


def _postfix_js(s):
    pat = re.compile(r"\.(" + "|".join(JS_POSTFIX) + r")\(")
    while True:
        m = pat.search(s)
        if not m:
            return s
        i = m.start() - 1
        d = 0
        while i >= 0:
            c = s[i]
            if c in ")]":
                d += 1
            elif c in "([":
                if d == 0:
                    break
                d -= 1
            elif d == 0 and not (c.isalnum() or c in "._"):
                break
            i -= 1
        recv = s[i + 1:m.start()]
        j = m.end() - 1
        d = 0
        for k in range(j, len(s)):
            if s[k] == "(":
                d += 1
            elif s[k] == ")":
                d -= 1
                if d == 0:
                    break
        args = R._split_args(s[j + 1:k])
        s = s[:i + 1] + JS_POSTFIX[m.group(1)](recv, args) + s[k + 1:]


def _inline_ifs_js(s):
    """Kotlin's `if (C) A else B` expression -> the JS ternary."""
    pos = 0
    pat = re.compile(r"(?<![\w.])if \(")
    while True:
        m = pat.search(s, pos)
        if not m:
            return s
        st = m.start()
        j = s.index("(", st)
        depth = 0
        for k in range(j, len(s)):
            if s[k] == "(":
                depth += 1
            elif s[k] == ")":
                depth -= 1
                if depth == 0:
                    break
        cond = s[j + 1:k]
        rest = s[k + 1:]
        d, epos = 0, -1
        for i in range(len(rest)):
            if d == 0 and rest.startswith(" else ", i):
                epos = i
                break
            c = rest[i]
            if c in "([{":
                d += 1
            elif c in ")]}":
                if d == 0:
                    break
                d -= 1
            elif c == "," and d == 0:
                break
        if epos < 0:
            raise SyntaxError("no else for: " + s[st:st + 70])
        a, tail = rest[:epos], rest[epos + 6:]
        d, end = 0, len(tail)
        for i in range(len(tail)):
            c = tail[i]
            if c in "([{":
                d += 1
            elif c in ")]}":
                if d == 0:
                    end = i
                    break
                d -= 1
            elif c == "," and d == 0:
                end = i
                break
        b = tail[:end]
        repl = "((%s) ? (%s) : (%s))" % (cond, a.strip(), b.strip())
        s = s[:st] + repl + tail[end:]
        pos = st + len(repl)


DRAW_FNS = ("drawRect", "drawCircle", "drawLine", "drawPath", "drawArc")
# Calls whose Kotlin named arguments become one JS object literal.
OBJ_CALLS = DRAW_FNS + ("Stroke", "Brush.verticalGradient", "Brush.linearGradient",
                        "Brush.radialGradient")


def _named_to_object(s):
    """`drawRect(color = x, size = y)` -> `drawRect({color: x, size: y})`.

    Only for the calls listed above, and only at the top level of their own
    argument list -- a nested `Brush.radialGradient(colors = ...)` keeps its own
    shape because it is rewritten separately."""
    for fn in OBJ_CALLS:
        pos = 0
        while True:
            m = re.search(r"(?<![\w.])" + re.escape(fn) + r"\(", s[pos:])
            if not m:
                break
            st = pos + m.start()
            j = pos + m.end() - 1
            d = 0
            for k in range(j, len(s)):
                if s[k] == "(":
                    d += 1
                elif s[k] == ")":
                    d -= 1
                    if d == 0:
                        break
            inner = s[j + 1:k]
            args = R._split_args(inner)
            if args and all(re.match(r"^\w+\s*=[^=]", a) for a in args):
                parts = []
                for a in args:
                    nm, v = a.split("=", 1)
                    parts.append("%s: %s" % (nm.strip(), v.strip()))
                inner = "{" + ", ".join(parts) + "}"
            s = s[:j + 1] + inner + s[k:]
            pos = j + 1 + len(inner) + 1
    return s


def jsexpr(s):
    s = s.replace("size.width", "d.w").replace("size.height", "d.h")
    s = s.replace("PI.toFloat()", "Math.PI").replace(".toFloat()", "")
    s = re.sub(r"(\d)f\b", r"\1", s)
    s = s.replace("StrokeCap.Round", "'round'").replace("StrokeCap.Butt", "'butt'")
    s = s.replace("Color.White", "WHITE").replace("Color.Black", "BLACK")
    s = re.sub(r"\blistOf\(", "[](", s)          # marker, closed below
    s = _postfix_js(s)
    s = re.sub(r"(?<![\w.])sin\(", "Math.sin(", s)
    s = re.sub(r"(?<![\w.])cos\(", "Math.cos(", s)
    s = re.sub(r"(?<![\w.])sqrt\(", "Math.sqrt(", s)
    s = re.sub(r"(?<![\w.])abs\(", "Math.abs(", s)
    s = re.sub(r"(?<![\w.])hypot\(", "Math.hypot(", s)
    s = re.sub(r"(?<![\w.])(min|max)\(", lambda m: "Math.%s(" % m.group(1), s)
    if " else " in s and re.search(r"(?<![\w.])if \(", s):
        s = _inline_ifs_js(s)
    s = re.sub(r"\.copy\(alpha\s*=\s*", ".copy(", s)
    s = _named_to_object(s)
    s = re.sub(r"(?<![\w.])Path\(\)", "new P()", s)
    s = re.sub(r"(?<![\w.])Offset\(", "new Off(", s)
    s = re.sub(r"(?<![\w.])Size\(", "new Sz(", s)
    for fn in DRAW_FNS:
        s = re.sub(r"(?<![\w.])" + fn + r"\(", "d." + fn + "(", s)
    # close the listOf marker: `[](a, b)` -> `[a, b]`
    while "[](" in s:
        i = s.index("[](")
        d = 0
        for k in range(i + 2, len(s)):
            if s[k] == "(":
                d += 1
            elif s[k] == ")":
                d -= 1
                if d == 0:
                    break
        s = s[:i] + "[" + s[i + 3:k] + "]" + s[k + 1:]
    return s


def transpile_js(src, sig):
    """One JS function per `fun DrawScope.name(p: X, r: Rng)` in the source."""
    out = {}
    for m in re.finditer(sig, src):
        name = m.group(1)
        i = m.end() - 1
        depth = 0
        for k in range(i, len(src)):
            if src[k] == "{":
                depth += 1
            elif src[k] == "}":
                depth -= 1
                if depth == 0:
                    break
        body = src[i + 1:k]
        lines = []
        for raw in body.split("\n"):
            t = raw.split("//")[0].rstrip()
            if t.strip():
                lines.append(t.strip())
        merged, buf = [], ""
        for t in lines:
            buf = (buf + " " + t).strip()
            if buf.count("(") == buf.count(")"):
                merged.append(buf)
                buf = ""
        js, ind, kinds = [], 1, []

        def emit(t):
            js.append("  " * ind + t)

        for t in merged:
            if t == "}":
                ind -= 1
                emit("});" if kinds.pop() == "xform" else "}")
                continue
            if t.startswith("} else if"):
                ind -= 1
                kinds.pop()
                emit("} else if (" + jsexpr(t[t.index("(") + 1:t.rindex(")")]) + ") {")
                ind += 1
                kinds.append("block")
                continue
            if t.startswith("} else"):
                ind -= 1
                kinds.pop()
                emit("} else {")
                ind += 1
                kinds.append("block")
                continue
            fm = re.match(r"for \((\w+) in (.+?) until (.+?)\) \{$", t)
            if fm:
                v = fm.group(1)
                emit("for (let %s = Math.trunc(%s); %s < Math.trunc(%s); %s++) {"
                     % (v, jsexpr(fm.group(2)), v, jsexpr(fm.group(3)), v))
                ind += 1
                kinds.append("block")
                continue
            im = re.match(r"if \((.+)\) \{$", t)
            if im:
                emit("if (" + jsexpr(im.group(1)) + ") {")
                ind += 1
                kinds.append("block")
                continue
            bm = re.match(r"(rotate|translate|scale)\((.*)\) \{$", t)
            if bm:
                # Compose's transform blocks scope their matrix; the JS
                # runtime takes the body as a callback and save/restores it.
                targs = [re.sub(r"^\w+\s*=\s*", "", a)
                         for a in R._split_args(jsexpr(bm.group(2)))]
                emit("d.%s(%s, () => {" % (bm.group(1), ", ".join(targs)))
                ind += 1
                kinds.append("xform")
                continue
            # single-statement if, no braces
            sm = re.match(r"if \((.+?)\) (\{ .+ \})$", t)
            if sm:
                emit("if (" + jsexpr(sm.group(1)) + ") " + jsexpr(sm.group(2)))
                continue
            if t.endswith("{"):
                raise SyntaxError("unhandled block: " + t)
            decl = re.match(r"^(val|var) ", t)
            t2 = re.sub(r"^(val|var) ", "", t)
            line = jsexpr(t2)
            emit(("const " if decl and decl.group(1) == "val" else
                  "let " if decl else "") + line + ";")
        while ind > 1:
            ind -= 1
            js.append("  " * ind + ("});" if kinds.pop() == "xform" else "}"))
        out[name] = "function %s(d, p, r) {\n%s\n}" % (name, "\n".join(js))
    return out


