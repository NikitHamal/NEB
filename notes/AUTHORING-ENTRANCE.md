# Authoring contract for the entrance-examination books — READ FULLY BEFORE WRITING

These books prepare students for Nepal's bachelor-level entrance examinations:
**CEE / MECEE-BL** (medical, MEC), **IOE** (BE/BArch, TU), **BSc CSIT** (IOST, TU)
and **BCA** (FOHSS, TU). They are free, and they must be *better* than the paid
coaching material: more accurate, clearer, closer to the real paper, and with every
answer explained. Accuracy is the whole point — a wrong key teaches a wrong fact to
thousands of students. When unsure, check (WebSearch / WebFetch / compute in Python).

`notes/AUTHORING.md` still applies for everything this file does not override:
§3 Markdown, §4 Math (matplotlib mathtext — read the unsupported list), §5 Figures,
§6 Callout boxes, §11 What the build does for you, §12 Figure quality bar, §14 Real
images. Read those sections first. Look at `notes/content/phy11/unit-03.md` for the
house tone and box usage.

---

## 1. Files and frontmatter

Your file: `notes/content/<slug>/unit-NN.md` (NN zero-padded). Slugs are
`<track>-<subject>`: `cee-phy`, `cee-chem`, `cee-zoo`, `cee-bot`, `cee-mat`,
`cee-mock`, `ioe-math`, `ioe-phy`, `ioe-chem`, `ioe-eng`, `ioe-mock`, `csit-…`, `bca-…`.
The spine is `notes/curriculum/<slug>.md` — it is law.

```
---
subject: Physics
grade: CEE
unit: 4
title: Fluid Statics and Dynamics
hours: 1
area: Mechanics
---
```

- `subject`: the subject name exactly as in `pipeline/spine.py` `TRACK_SUBJECTS`.
- `grade`: the track short name — `CEE`, `IOE`, `CSIT` or `BCA`.
- `title`, `area` verbatim from the spine; `hours` is the number in the spine's
  `[n]` — **for these books it is the number of questions the chapter carries in
  the paper**, not teaching hours. For a non-numeric tag (`[Guide]`, `[Practice]`)
  write `hours: 0`.

The spine's bullet list is injected above your chapter automatically as
"Official syllabus — this chapter covers". Every bullet must be covered, in order.

## 2. Shape of a subject chapter

1. **Opening** (3–6 lines): what this part of the paper is, how many questions it
   carries, and which sub-topics carry the marks.
2. `::: key What the paper asks from this chapter` — the 5–8 ideas, facts or
   formula types that the questions are built on.
3. **One `## N.k` section per spine bullet**, in spine order (N = unit number).
   Use `### ` subsections freely. Each section is *complete but compact*:
   - definitions in the board's wording; laws with every symbol defined, with units
     and the conditions they hold under;
   - comparison tables (a table is the fastest revision tool — use them a lot);
   - for numerical subjects, 1–3 `::: example` boxes per section solved **the fast
     way an MCQ needs** (ratios, proportionality, dimensional shortcuts,
     limiting cases), each with **Problem.** / **Solution.** and the final answer;
   - `::: caution` boxes for the traps examiners build distractors from;
   - `::: memory` for mnemonics that are genuinely useful;
   - `::: tip` for exam technique (elimination, estimation, when to skip).
4. `## Formula and fact sheet` — every formula of the chapter (physics, chemistry,
   maths) or every number, name, example and exception the paper asks (biology,
   MAT), in tables or tight lists. This is what a student revises the night before.
5. `## Chapter summary` — 6–10 bullets (exact heading; the build frames it).
6. `## Practice questions` — the MCQ sets (§3).

Theory length: about **2,000–5,000 words**, scaled to the chapter's question count
and difficulty. Do not pad, do not repeat the syllabus, no filler. If a full
derivation is not examinable as an MCQ, give the result and the one idea behind it;
you may point to the NEBians Grade 11/12 book chapter for the derivation.

Figures: 1–4 per chapter where they carry information (graphs, ray diagrams,
circuits, cycles, life cycles, apparatus, shapes of molecules, cube nets for MAT).
Follow AUTHORING.md §5 and §12 exactly and render each one to PNG and look at it
(`python3 preview.py ../content/<slug>/unit-NN.md /tmp/<yourname>/`). Biology may
use 1–3 real images through `assets.py` (§14) where recognition is the point;
only if the fetch works quickly — never block the chapter on an image.

## 3. Multiple-choice practice — the heart of the book

Write the practice in three sets that mirror the paper's cognitive split
(MEC instructs setters: recall 50 %, understanding 30 %, application 20 %):

```
## Practice questions

**Set A — Recall (20 questions)**

1. The dimensional formula of surface tension is
   (a) [MLT⁻²] (b) [MT⁻²] (c) [ML⁻¹T⁻²] (d) [ML²T⁻²]
2. ...

::: note Answers and explanations — Set A
**1.** (b) — surface tension is force per unit length: [MLT⁻²]/[L] = [MT⁻²]. Option (a) is force itself.
**2.** (d) — ...
:::

**Set B — Understanding (15 questions)**

1. ...

::: note Answers and explanations — Set B
**1.** ...
:::

**Set C — Application (15 questions)**
...
```

Hard rules (the web reader turns these into tap-to-check questions; break the
format and the questions stop working):

- **Number every set from 1** and follow it immediately with its own answer box.
  The answer box title must contain the word **Answers** (`::: note Answers and
  explanations — Set A`). One line per answer: `**n.** (x) — explanation`.
- Question stem on the numbered line; the four options **on the next line, indented
  three spaces, all on one line**: `   (a) … (b) … (c) … (d) …`. Never put options on
  separate lines, never use (A)/(B), never add a fifth option.
- Inline math in stems and options is fine (`$…$`, one line). No display math
  (`$$`) inside a question or an option.
- Do not put `<span class="marks">` on MCQs.
- **Count**: a chapter carrying 1–2 questions in the paper needs at least
  **40 MCQs** (A 20 / B 12 / C 8); 3 or more questions in the paper needs at least
  **50** (A 25 / B 15 / C 10). More is welcome when the topic is broad.
- **Single best answer**, four options, one unambiguously correct. Stems at most
  60 words (the MEC rule). Distractors must be *plausible* — the wrong answers
  real students give (sign errors, a missing factor of 2, the confusable term,
  the exception to the rule). No "all of the above" / "none of the above" except
  rarely and only when truly the best format. Negative stems write NOT in capitals.
- **Spread the keys**: across a set, no letter more than about 35 % of the
  answers, and no long runs of the same letter. Decide the key position
  deliberately; do not let the correct answer drift to (b)/(c).
- **Every explanation teaches**: why the key is right in one to three lines, and
  where useful why the most tempting wrong option is wrong. Numerical questions
  show the working in one or two lines with units.
- **Verify every numerical answer by computing it in Python before you write the
  key** (`python3 -c "…"`). Recheck that the key letter points at the option that
  holds the value you computed. Biology/chemistry facts you are not certain of:
  look them up. A wrong key is the worst possible defect in this book.
- Use numbers that give clean answers; use standard values (g = 9.8 m s⁻² unless
  the question says 10; h = 6.63 × 10⁻³⁴ J s; e = 1.6 × 10⁻¹⁹ C; c = 3 × 10⁸ m s⁻¹;
  N_A = 6.02 × 10²³ mol⁻¹; R = 8.314 J mol⁻¹ K⁻¹) and say in the stem which you used
  when it matters.
- Nepali context where natural (Kathmandu, Pokhara, Mount Everest, the Koshi, NEA
  electricity, rupees), never at the cost of clarity.
- **Honesty about sources.** Every question is original practice written to the
  official syllabus. Never write "asked in CEE 2081" or similar unless you have
  verified it from a real published paper in this session (and then say where).
  Statements like "a favourite of the paper" must reflect the syllabus weightage,
  not invented history.

## 4. Model papers (`*-mock` books)

A model paper is one chapter, numbered **straight through like the real paper**
(1–200 for CEE), in subject sections, with the whole key at the end:

```
## Zoology (questions 1–40)

1. stem
   (a) … (b) … (c) … (d) …
...
40. stem
   (a) … (b) … (c) … (d) …

## Botany (questions 41–80)

41. stem
   (a) … (b) … (c) … (d) …
...

## Answer key and explanations

::: note Answers — Zoology (1–40)
**1.** (c) — explanation
...
**40.** (a) — explanation
:::

::: note Answers — Botany (41–80)
**41.** (b) — ...
:::
```

- The web exporter keys a list that starts at 41 from the first later answer
  box that contains answer 41, so continuous numbering works: keep each section's
  numbers contiguous and give each section its own answer box at the end.
- Follow the official weightage **unit by unit** (the spine header gives it for
  CEE: Zoology 3/4/4/6/15/4/2/2, Botany 2/9/4/5/6/3/6/2/3, Chemistry 17/10/17/3/3,
  Physics 10/7/8/9/4/12, MAT 5/5/5/5). Put a short table of your paper's actual
  per-unit counts at the top of the chapter, and make it true.
- Mix difficulty about 50:30:20 (recall : understanding : application).
- Each model paper must be **different** from the others: different questions,
  different numbers, different facts tested. Read the earlier papers in the book
  before writing a new one.
- Open the chapter with instructions as the real paper gives them (time, marks,
  negative marking) and a one-line "how to score yourself" with the negative
  marking rule.

## 5. Before you finish a chapter

1. `cd notes/pipeline && python3 check.py ../content/<slug>/unit-NN.md` → must end
   in **OK**. Fix every failure (unsupported mathtext, unpaired `$`, figure errors,
   too-wide display equations, small figure text).
2. Render your figures to PNG and look at each one.
3. Check MCQ formatting with the keying test:
   `python3 notes/tools/mcqcheck.py notes/content/<slug>/unit-NN.md` — prints how
   many MCQs it found per set, how many got a key, and the key-letter spread. Every
   MCQ must be keyed.
4. Commit and push your file(s) yourself, so nothing is lost if the session dies:
   `notes/tools/lockpush.sh "notes: <slug> unit NN — <title>" notes/content/<slug>/unit-NN.md`
   (only the paths you name are committed; never `git add -A`).
5. Report: file, words, figures, number of MCQs per set, check.py status.

Do **not** build PDFs or run the web export — the coordinator does that, once per
book, so the builds do not fight over the two CPU cores.
