#!/usr/bin/env python3
"""Check the multiple-choice questions of a chapter the way the web reader will see them.

    python3 notes/tools/mcqcheck.py notes/content/cee-phy/unit-04.md [more.md ...]

Renders the chapter with the web exporter (maths left as TeX, so it is quick; media go to a
temporary folder, not the site), then reports every multiple-choice list: where it starts,
how many questions it has, how many were tied to a key, and the spread of key letters.
Also catches the silent failures:

  - a question whose options are too long for the option grid (any option over 78
    visible characters) is shown as stacked parts and cannot be tapped;
  - a stem over 60 words (the MEC rule for the paper);
  - an answer box whose numbers skip, repeat, or do not match the questions above it;
  - a run of five or more identical key letters.

Exits non-zero if any question in an option grid has no key, a list has no key at all,
or a four-option question fell out of the grid.
"""
import collections
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "pipeline"))

import export_study  # noqa: E402
import spine  # noqa: E402

export_study.MEDIA = tempfile.mkdtemp(prefix="mcqcheck-")


def _source_checks(text):
    """Stem length and answer-box numbering, from the markdown itself."""
    notes = []
    prac = text.find("## Practice questions")
    body = text if prac < 0 else text[prac:]
    for m in re.finditer(r"^(\d+)\. (.+)$", body, re.M):
        nxt = body[m.end():m.end() + 400].split("\n")
        if len(nxt) > 1 and nxt[1].lstrip().startswith("(a)"):
            words = len(re.sub(r"\$[^$]*\$", "x", m.group(2)).split())
            if words > 60:
                notes.append("question %s: stem has %d words (the paper allows 60)" % (m.group(1), words))
    for m in re.finditer(r"^::: \w+ (Answers[^\n]*)\n(.*?)^:::", text, re.S | re.M):
        nums = [int(n) for n in re.findall(r"^\*\*(\d+)\.\*\*", m.group(2), re.M)]
        keys = re.findall(r"^\*\*\d+\.\*\*\s*\(([a-d])\)", m.group(2), re.M)
        if nums and nums != list(range(nums[0], nums[0] + len(nums))):
            notes.append("'%s': answer numbers are not contiguous" % m.group(1)[:50])
        seq = "".join(keys)
        run = max((len(r.group(0)) for r in re.finditer(r"(.)\1*", seq)), default=0)
        if run >= 5:
            notes.append("'%s': %d identical key letters in a row" % (m.group(1)[:50], run))
    return notes


def check(path):
    md2html = export_study._patch_md2html()
    import i18n
    slug = os.path.basename(os.path.dirname(os.path.abspath(path)))
    i18n.set_book(slug)
    text = open(path, encoding="utf-8").read()
    meta, htm, _ = md2html.convert(text, "mcqcheck", 1)
    htm, _ = export_study._finish(htm, far=bool(spine.track_of(slug)[0]))
    bad = 0
    total = keyed = 0
    letters = collections.Counter()
    print(path)
    for m in re.finditer(r'<ol( class="mcq")?( start="(\d+)")?>(.*?)</ol>', htm, re.S):
        block = m.group(4)
        items = re.findall(r"<li( data-key=\"(\w)\")?>(.*?)</li>", block, re.S)
        start = int(m.group(3) or 1)
        for i, it in enumerate(items):
            parts = re.findall(r'<span class="part"><i>\(([a-e])\)</i>', it[2])
            if parts[:4] == list("abcd") and 'class="marks"' not in it[2]:
                bad += 1
                print("  question %d: an option is too long for the option grid (78 characters); "
                      "it shows as stacked parts and cannot be tapped   <-- SHORTEN" % (start + i))
        grid = [it for it in items if 'class="opts' in it[2]]
        if not grid:
            continue
        got = [it for it in grid if it[1]]
        for it in got:
            letters[it[1]] += 1
        total += len(grid)
        keyed += len(got)
        flag = "" if len(got) == len(grid) else "   <-- %d WITHOUT A KEY" % (len(grid) - len(got))
        if flag:
            bad += 1
        print("  list from %-4d %3d MCQs, %3d keyed%s" % (start, len(grid), len(got), flag))
    for note in _source_checks(text):
        print("  note: " + note)
    spread = ", ".join("%s %d" % (k, letters[k]) for k in "abcd")
    top = max(letters.values()) / keyed if keyed else 0
    warn = "   <-- one letter is %.0f%% of the keys" % (100 * top) if keyed and top > 0.36 else ""
    print("  total %d MCQs, %d keyed; keys: %s%s" % (total, keyed, spread, warn))
    return bad == 0 and total > 0 and keyed == total


if __name__ == "__main__":
    ok = all([check(p) for p in sys.argv[1:]])
    sys.exit(0 if ok else 1)
