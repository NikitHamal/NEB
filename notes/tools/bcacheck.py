#!/usr/bin/env python3
"""Dependency-free chapter checker for the BCA books (works on Python 3.8+).

    python3 notes/tools/bcacheck.py notes/content/bca-math/unit-01.md [more.md ...]

For every chapter it checks the things that silently break the reader:
  * frontmatter present with subject / grade / unit / title / hours / area
  * every numbered MCQ has a stem line plus ONE option line "(a) .. (b) .. (c) .. (d) .."
  * every option is <= 78 characters and the stem <= 60 words
  * every question has a key in an answer box ("**n.** (x) - ...") and no key is orphaned
  * an answer box title contains "Answers"
  * no run of five identical key letters, no letter above 40 % of a set (50 % under 10 Qs)
  * inline math: an even number of unescaped $ on every line, no unbraced \\frac / \\sqrt / \\mathbb
Exits 1 on any problem and prints a one-line summary per chapter.
"""
import re, sys, collections

OPT = re.compile(r"^\s{2,}\(a\)\s.*\s\(b\)\s.*\s\(c\)\s.*\s\(d\)\s")
STEM = re.compile(r"^(\d+)\.\s+(.*)$")
KEY = re.compile(r"^\*\*(\d+)\.\*\*\s*\(([a-d])\)")
BAD_TEX = [re.compile(r"\\frac\s*[0-9a-zA-Z]"), re.compile(r"\\sqrt\s*[0-9a-zA-Z]"),
           re.compile(r"\\mathbb"), re.compile(r"\\operatorname"), re.compile(r"\\underline")]


def check(path):
    errs, text = [], open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return ["no frontmatter"], {}
    fm = dict(l.split(": ", 1) for l in m.group(1).splitlines() if ": " in l)
    for k in ("subject", "grade", "unit", "title", "hours", "area"):
        if k not in fm:
            errs.append(f"frontmatter missing {k}")
    lines = text.splitlines()
    # inline math sanity
    in_code = False
    for i, l in enumerate(lines, 1):
        if l.startswith("```"):
            in_code = not in_code
        if in_code:
            continue
        s = l.replace("\\$", "")
        if s.count("$$") % 2 == 0:
            s = s.replace("$$", "")
        if s.count("$") % 2:
            errs.append(f"line {i}: unpaired $")
        for r in BAD_TEX:
            if r.search(l):
                errs.append(f"line {i}: unbraced/unsupported TeX {r.pattern}")
    # collect questions: a numbered stem followed by an option line
    qs, cur_sets = [], []
    i = 0
    while i < len(lines):
        sm = STEM.match(lines[i])
        if sm and i + 1 < len(lines) and OPT.match(lines[i + 1]):
            n = int(sm.group(1))
            stem = sm.group(2)
            if len(stem.split()) > 60:
                errs.append(f"Q{n} (line {i+1}): stem over 60 words")
            opts = re.split(r"\s\(([abcd])\)\s", " " + lines[i + 1].strip())
            texts = opts[2::2]
            if len(texts) != 4:
                errs.append(f"Q{n} (line {i+1}): option count {len(texts)}")
            for t in texts:
                if len(t.strip()) > 78:
                    errs.append(f"Q{n}: option over 78 chars")
            qs.append((n, i + 1))
            i += 2
            continue
        if sm and not (i + 1 < len(lines) and OPT.match(lines[i + 1])):
            # numbered line that is not a question: allowed only in plain lists (no key) - flag if inside Practice
            pass
        i += 1
    # answer boxes
    keys, box_titles = [], []
    for i, l in enumerate(lines):
        if l.startswith("::: note") and "Answers" in l:
            box_titles.append(l)
            j = i + 1
            box = []
            while j < len(lines) and lines[j].strip() != ":::":
                km = KEY.match(lines[j])
                if km:
                    box.append((int(km.group(1)), km.group(2)))
                j += 1
            keys.append(box)
    # match: split questions into runs where numbering restarts or jumps
    runs, run = [], []
    for n, ln in qs:
        if run and n != run[-1][0] + 1:
            runs.append(run)
            run = []
        run.append((n, ln))
    if run:
        runs.append(run)
    if len(runs) != len(keys):
        # a model paper numbers straight through while keeping one answer box per section
        flat_q = [x for r in runs for x in r]
        flat_k = [x for b in keys for x in b]
        if [n for n, _ in flat_q] == [n for n, _ in flat_k] and len(keys) > 1:
            runs = [flat_q]
            keys = [flat_k]
        else:
            errs.append(f"{len(runs)} question runs but {len(keys)} answer boxes")
    spread = collections.Counter()
    for r, box in zip(runs, keys):
        qn = [n for n, _ in r]
        kn = [n for n, _ in box]
        if qn != kn:
            errs.append(f"run starting Q{qn[0]} (line {r[0][1]}): questions {qn[0]}-{qn[-1]} vs keys {kn[:1]}-{kn[-1:]} ({len(qn)} vs {len(kn)})")
        letters = [k for _, k in box]
        c = collections.Counter(letters)
        spread.update(c)
        cap = 0.4 if len(letters) >= 10 else 0.5
        for ch, v in c.items():
            if len(letters) >= 8 and v / len(letters) > cap:
                errs.append(f"run at Q{qn[0]}: letter ({ch}) is {v}/{len(letters)}")
        streak = 1
        for a, b in zip(letters, letters[1:]):
            streak = streak + 1 if a == b else 1
            if streak >= 5:
                errs.append(f"run at Q{qn[0]}: five identical keys in a row")
                break
    info = {"mcq": len(qs), "sets": len(runs), "spread": dict(sorted(spread.items())),
            "words": len(re.findall(r"\w+", text))}
    return errs, info


if __name__ == "__main__":
    bad = 0
    for p in sys.argv[1:]:
        e, info = check(p)
        print(("OK  " if not e else "FAIL"), p.split("content/")[-1], info)
        for x in e[:20]:
            print("     -", x)
        bad += bool(e)
    sys.exit(1 if bad else 0)
