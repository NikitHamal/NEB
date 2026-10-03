#!/usr/bin/env python3
"""Split display equations that overflow the text column (check.py: TOO WIDE).
Usage: python3 fixwide.py ../content/math11/unit-13.md [more files]
Splits an offending $$…$$ block at its own line breaks, then at \\quad/\\qquad,
and re-checks until no block is too wide or nothing more can be split."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mathsvg, md2html, figrun, photo

BLOCK = re.compile(r"\$\$(.*?)\$\$", re.S)

def overwide(text, cid):
    mathsvg.OVERWIDE.clear()
    md2html.convert(text, cid, 1)
    return {t.strip() for t, _ in mathsvg.OVERWIDE}

def _balanced(s):
    return s.count("\\left") == s.count("\\right") and s.count("{") == s.count("}")

def _regroup(pieces):
    """Merge pieces until each group is bracket-balanced (never split inside \\left…\\right)."""
    out, cur = [], ""
    for p in pieces:
        cur = (cur + " " + p).strip()
        if _balanced(cur):
            out.append(cur); cur = ""
    if cur:
        out.append(cur)
    return out

def _clean(p):
    return re.sub(r"(\\q?quad|\\[ ,;:!])+\s*$", "", p.strip()).rstrip(",;").strip()

def split_parts(tex):
    lines = [l.strip() for l in tex.strip().split("\n") if l.strip()]
    parts = _regroup(lines) if len(lines) > 1 else []
    if len(parts) < 2:
        parts = _regroup([p.strip() for p in re.split(r"\\q?quad", tex.strip()) if p.strip()])
    parts = [_clean(p) for p in parts if _clean(p)]
    return parts if len(parts) > 1 else [tex.strip()]

def fix(path):
    text = open(path, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in text else "\n"
    text = text.replace("\r\n", "\n")
    cid = os.path.basename(os.path.dirname(path)) + "-" + os.path.basename(path)
    for _ in range(4):
        bad = overwide(text, cid)
        if not bad:
            break
        changed = False
        def rep(m):
            nonlocal changed
            if m.group(1).strip() not in bad and not any(
                    re.sub(r"\s+", " ", b) == re.sub(r"\s+", " ", m.group(1).strip()) for b in bad):
                return m.group(0)
            parts = split_parts(m.group(1))
            if len(parts) < 2:
                return m.group(0)
            changed = True
            return "\n\n".join("$$\n" + p + "\n$$" for p in parts)
        text = BLOCK.sub(rep, text)
        if not changed:
            break
    open(path, "w", encoding="utf-8", newline="").write(text.replace("\n", nl))
    left = overwide(text, cid)
    print(f"{path}: {'clean' if not left else str(len(left)) + ' still too wide'}")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        fix(p)
