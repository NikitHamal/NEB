#!/usr/bin/env python3
"""Shared helpers for the token-substitution verifiers (check_mis.py, check_society.py, ...).
A book unit contains {{token}} placeholders; --fill replaces them with computed values; --verify re-checks that
every computed value is present in the book text and that no placeholder is left."""
import re, sys, glob, os

def table(head, rows):
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows])

def inr(x):
    s = f"{abs(round(x)):d}"
    if len(s) > 3:
        h, t = s[:-3], s[-3:]
        parts = []
        while len(h) > 2:
            parts.insert(0, h[-2:]); h = h[:-2]
        if h: parts.insert(0, h)
        s = ",".join(parts + [t])
    return ("-" if x < 0 else "") + s

def run(T, argv, doc=""):
    mode = argv[0] if argv else "--print"
    files = argv[1:]
    if mode == "--print":
        for k, v in T.items():
            print(f"[{k}] {v}")
        return
    if mode == "--fill":
        for f in files:
            t = open(f, encoding="utf-8").read()
            missing = set(re.findall(r"\{\{(\w+)\}\}", t)) - set(T)
            if missing:
                sys.exit(f"{f}: unknown tokens {sorted(missing)}")
            t = re.sub(r"\{\{(\w+)\}\}", lambda m: str(T[m.group(1)]), t)
            open(f, "w", encoding="utf-8").write(t)
        print("filled", len(files), "files")
        return
    if mode == "--verify":
        txt = "\n".join(open(f, encoding="utf-8").read() for f in files)
        left = re.findall(r"\{\{\w+\}\}", txt)
        bad = [k for k, v in T.items() if not k.startswith("_") and str(v) not in txt and not k.endswith("_opt")]
        print(f"verify: {len(T)} tokens, {len(left)} unfilled placeholders, {len(bad)} values absent from book")
        if left or bad:
            print("unfilled:", left[:10], "absent:", bad[:20]); sys.exit(1)
        return
    sys.exit(doc or "usage: --print | --fill files | --verify files")
