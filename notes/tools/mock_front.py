#!/usr/bin/env python3
"""Wrap an assembled model paper with frontmatter, instructions, the unit-count table and the score line.

    python3 notes/tools/mock_front.py N notes/drafts/cee-mock/mpN-a.md notes/drafts/cee-mock/mpN-b.md

Assembles the two drafts and writes notes/content/cee-mock/unit-(N+1).md.
"""
import subprocess
import sys
import tempfile

N = int(sys.argv[1])
drafts = sys.argv[2:]
out = f"notes/content/cee-mock/unit-{N + 1:02d}.md"
with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as t:
    t.write("\n".join(open(d, encoding="utf-8").read().rstrip("\n") + "\n" for d in drafts))
asm = t.name + ".out"
subprocess.run([sys.executable, "notes/tools/assemble_paper.py", t.name, asm], check=True)
body = open(asm, encoding="utf-8").read()
head = f"""---
subject: Model Papers and Mock Tests
grade: CEE
unit: {N + 1}
title: Model Paper {N}
hours: 200
area: Full Model Papers
---

Model Paper {N} follows the MECEE-BL Group I paper question for question: Zoology 40, Botany 40,
Chemistry 50, Physics 50 and Mental Agility Test 20, 200 single-best-answer questions in 3 hours.
Take it as a timed test, with no book and no pause, then read the explained key at the end.

::: key Instructions
- 200 questions, 180 minutes, 200 marks. Each question has four options and exactly one best answer.
- +1 for a right answer, −0.25 for a wrong answer, 0 for a blank. Score = R − 0.25 W.
- Two options ruled out? Answer. Nothing ruled out? Skip it unless time is spare (see §1.3 of the exam guide).
- Constants are given in the question where needed; take g = 10 m s⁻² unless a question says otherwise.
:::

| Subject | Questions | Question numbers |
|---|---|---|
| Zoology | 40 | 1–40 |
| Botany | 40 | 41–80 |
| Chemistry | 50 | 81–130 |
| Physics | 50 | 131–180 |
| Mental Agility Test | 20 | 181–200 |

The questions in each subject follow the official unit weightage of the MEC syllabus (exam guide, §1.2).
**Score yourself:** score = right − 0.25 × wrong. Around 150 is a strong paper; the merit list is cut from the 50th percentile upward, so
what matters is beating the field, not a fixed mark.

"""
open(out, "w", encoding="utf-8").write(head + body)
print("wrote", out)
