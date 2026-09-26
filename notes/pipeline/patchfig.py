#!/usr/bin/env python3
"""Replace the Nth ```figure block's code (and optionally caption) in a chapter."""
import sys, re, io

def patch(path, index, new_code, new_caption=None):
    text = open(path, encoding="utf-8").read()
    pat = re.compile(r"^```figure([^\n]*)\n(.*?)^```\s*$", re.S | re.M)
    matches = list(pat.finditer(text))
    m = matches[index - 1]
    info = m.group(1)
    if new_caption is not None:
        info = f' caption="{new_caption}"'
    repl = "```figure" + info + "\n" + new_code.rstrip("\n") + "\n```"
    text = text[:m.start()] + repl + text[m.end():]
    open(path, "w", encoding="utf-8").write(text)
    print(f"patched figure {index} of {path}")
