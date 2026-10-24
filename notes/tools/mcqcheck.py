#!/usr/bin/env python3
"""Check the multiple-choice questions of a chapter the way the web reader will see them.

    python3 notes/tools/mcqcheck.py notes/content/cee-phy/unit-04.md [more.md ...]

Renders the chapter with the web exporter (maths left as TeX, so it is quick), then
reports every multiple-choice list: where it starts, how many questions it has, how many
were tied to a key, and the spread of key letters. Exits non-zero if any question in an
option grid has no key, or if a list was left without any key at all.
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "pipeline"))

import export_study  # noqa: E402
import spine  # noqa: E402


def check(path):
    md2html = export_study._patch_md2html()
    import i18n
    slug = os.path.basename(os.path.dirname(os.path.abspath(path)))
    i18n.set_book(slug)
    meta, htm, _ = md2html.convert(open(path, encoding="utf-8").read(), "mcqcheck", 1)
    htm, _ = export_study._finish(htm, far=bool(spine.track_of(slug)[0]))
    bad = 0
    total = keyed = 0
    letters = collections.Counter()
    print(path)
    for m in re.finditer(r'<ol( class="mcq")?( start="(\d+)")?>(.*?)</ol>', htm, re.S):
        block = m.group(4)
        items = re.findall(r"<li( data-key=\"(\w)\")?>(.*?)</li>", block, re.S)
        grid = [it for it in items if 'class="opts' in it[2]]
        if not grid:
            continue
        got = [it for it in grid if it[1]]
        for it in got:
            letters[it[1]] += 1
        start = int(m.group(3) or 1)
        total += len(grid)
        keyed += len(got)
        flag = "" if len(got) == len(grid) else "   <-- %d WITHOUT A KEY" % (len(grid) - len(got))
        if flag:
            bad += 1
        print("  list from %-4d %3d MCQs, %3d keyed%s" % (start, len(grid), len(got), flag))
    spread = ", ".join("%s %d" % (k, letters[k]) for k in "abcd")
    top = max(letters.values()) / keyed if keyed else 0
    warn = "   <-- one letter is %.0f%% of the keys" % (100 * top) if keyed and top > 0.36 else ""
    print("  total %d MCQs, %d keyed; keys: %s%s" % (total, keyed, spread, warn))
    return bad == 0 and total > 0 and keyed == total


if __name__ == "__main__":
    ok = all([check(p) for p in sys.argv[1:]])
    sys.exit(0 if ok else 1)
