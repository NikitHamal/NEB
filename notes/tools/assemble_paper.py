#!/usr/bin/env python3
"""Turn a model-paper draft into the chapter the book and the reader expect.

    python3 notes/tools/assemble_paper.py notes/drafts/cee-mock/unit-02.md notes/content/cee-mock/unit-02.md

A draft is written one section at a time, each section's answer box right after its
questions, so it can be checked (check.py, mcqcheck.py) and pushed after every section.
The paper itself puts every question first and the whole key at the end: this moves each
answer box (a `::: note` whose title contains "Answers") to the end, under
"## Answer key and explanations", in the order written, and checks that

  - the questions are numbered 1..N straight through, with no gap or repeat;
  - every question has exactly one key line `**n.** (x) — ...`, and no key is orphaned.

Prints the question count per section and the key-letter spread; exits non-zero (and
writes nothing) on any mismatch.
"""
import re
import sys
from collections import Counter

Q = re.compile(r"^(\d+)\.\s")
OPTS = re.compile(r"^\s{2,}\(a\)")
KEY = re.compile(r"^\*\*(\d+)\.\*\*\s*\(([a-d])\)")
BOX = re.compile(r"^:::\s*note\b.*Answers")


def main(src, dst):
    lines = open(src, encoding="utf-8").read().rstrip("\n").split("\n")
    body, boxes, i = [], [], 0
    while i < len(lines):
        ln = lines[i]
        if BOX.match(ln):
            j = i + 1
            while j < len(lines) and lines[j].strip() != ":::":
                j += 1
            boxes.append(lines[i:j + 1])
            i = j + 1
            continue
        if ln.strip() == "## Answer key and explanations":
            i += 1
            continue
        body.append(ln)
        i += 1

    qs, sections, current = [], [], None
    for k, ln in enumerate(body):
        if ln.startswith("## "):
            current = [ln[3:].strip(), 0]
            sections.append(current)
        m = Q.match(ln)
        if m and k + 1 < len(body) and OPTS.match(body[k + 1]):
            qs.append(int(m.group(1)))
            if current:
                current[1] += 1
    keys = [(int(m.group(1)), m.group(2)) for box in boxes for ln in box
            for m in [KEY.match(ln)] if m]

    errors = []
    if qs != list(range(1, len(qs) + 1)):
        gaps = [n for a, n in zip([0] + qs, qs) if n != a + 1]
        errors.append(f"questions not numbered 1..{len(qs)} straight through (break at {gaps[:5]})")
    knum = Counter(n for n, _ in keys)
    dup = sorted(n for n, c in knum.items() if c > 1)
    missing = sorted(set(qs) - set(knum))
    orphan = sorted(set(knum) - set(qs))
    if dup:
        errors.append(f"keyed more than once: {dup[:10]}")
    if missing:
        errors.append(f"no key line: {missing[:10]}")
    if orphan:
        errors.append(f"key without a question: {orphan[:10]}")

    for title, n in sections:
        if n:
            print(f"  {n:4d}  {title}")
    spread = Counter(x for _, x in keys)
    print(f"  {len(qs)} questions, {len(keys)} keys; keys: "
          + ", ".join(f"{x} {spread[x]}" for x in "abcd"))
    if errors:
        for e in errors:
            print("ERROR:", e)
        sys.exit(1)

    while body and not body[-1].strip():
        body.pop()
    out = body + ["", "## Answer key and explanations", ""]
    for box in boxes:
        out += box + [""]
    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n".join(out).rstrip("\n") + "\n")
    print(f"wrote {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
