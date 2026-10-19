# Writing a lesson video

The reference lesson is `scripts/phy12/unit_01.py` (Physics 12, Rotational Dynamics, ~25 min).
Read it fully before writing a new one; it shows every kit feature in use.

## The bar

These are the best explainer videos a Nepali NEB student has ever seen. Every chapter
video is **long (15–30 min), complete, accurate and visual**:

1. **Cold open (30–60 s).** A hook that makes the student want the answer: a race, a
   paradox, a real Nepali scene, a question from the exam. Resolve it later in the lesson.
2. **Title card + roadmap.** `self.title_card()` → narration → `self.end_title(g, nb)` →
   `self.roadmap(narration)`.
3. **One part per syllabus bullet**, in the order of `notes/curriculum/<book>.md` and the
   chapter `notes/content/<book>/unit-NN.md`. Every part starts with `self.section(i)`.
   Teach, do not read: build each idea visually (geometry that moves, values that change
   live with `ValueTracker`, equations that transform into each other, diagrams that
   assemble, counters, bars, timelines, maps, cards). A static slide with a voice over it
   is a failure.
4. **Worked examples** from the chapter, solved step by step, each step written as it is
   spoken. Recompute every number yourself before you write it.
5. **At least two `self.quiz(...)`** (pause-and-think, with countdown), taken from the
   chapter's practice questions, the reveal explaining *why* the answer is right and why
   the tempting wrong one is wrong.
6. **At least one `self.tip(...)`** (exam tip / common mistake), Neby beside it.
7. **`self.recap(points, narration)`** and **`self.outro(narration)`** with `NEXT` set.

## Mechanics

```python
from manim import *
import numpy as np
from kit import Lesson, M, T, para, th

class Lesson(Lesson):            # the class must be called Lesson
    SUBJECT = "chem"             # key into theme.SUBJECT_COLORS: phy chem bio math cs eng nep soc health sci omath acc eco qbank
    GRADE = 12
    UNIT = 3
    TITLE = "Chemical Kinetics"
    SUBTITLE = "How fast, and why"
    LANG = "en"                  # "ne" for Nepali-medium books
    SECTIONS = [...]             # one short title per syllabus bullet; drives the HUD progress bar
    NEXT = "Unit 4 · ..."

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, ..., self.ending)
```

- `with self.say("spoken text"):` — narration. Everything played inside is padded to
  the length of the speech, so picture and voice never drift. `as v:` gives `v.dur`.
  Keep each `say` to 1–4 sentences, and put the animation that matches those words inside it.
- Write narration as it is **spoken**: "v equals r omega", "two point five kilogram metre
  squared", "ten to the power five". Never put symbols, LaTeX or abbreviations in a `say`.
- `T(text, size, color, weight)` text (auto Mukta for Devanagari), `para(text, width, size)`
  wrapped paragraph, `M(r"latex", size, color)` maths, `th.*` colours.
- `self.sfx(name)` — whoosh, whoosh_down, pop, pop_low, click, tick, bell, correct, wrong,
  thud, riser, shimmer, type, impact, count. Use them on reveals and hits, never constantly.
- `self.neby(state, height)` — the pixel mascot. States: idle, think, talk, read, hop, wink,
  love, laugh, cool, surprised, sad, dizzy, oops, success, celebrate, namaste, wave (never in
  Nepali), sleep, listen, look-around. `self.add(nb)` before animating it, `self.remove(nb)` after
  fading it out. Use Neby for reactions (surprised at a paradox, success after a solved
  problem, think during a hard step) — a few times per part, not constantly.
- `self.callout(kind, body)` with kind key/tip/careful/remember returns a boxed VGroup.
- `self.hold(t)` instead of `self.wait(t)` when `t` might be ≤ 0.
- Keep everything inside x∈[-6.8, 6.8], y∈[-3.3, 3.3]: the HUD owns the top-left corner and
  the bottom 0.4 units. Titles of a scene go at `to_edge(UP, buff=0.7)` or lower.
- Clean up: fade out what you made at the end of each beat; `always_redraw` objects must also
  be `self.remove(...)`d after fading.
- Performance: `always_redraw` that builds `T()` or `M()` every frame is slow — keep live
  text to a few short readouts. Prefer `DecimalNumber` with an updater for live numbers.

## Nepali-medium books (`nep`, `soc`, `health`)

`LANG = "ne"`. **No English word anywhere**: not in narration, not on screen, not in labels.
Use `self.num(x)` for every number on screen (Nepali digits). Quiz letters are क ख ग घ
automatically. Do not use `M()` for anything with words; write Nepali text with `T`/`para`.
Narration in natural, warm, standard Nepali, as a good teacher in Kathmandu would speak it.
For literature: who the author is (with a timeline), the context, the text's structure,
key lines shown and explained, the theme, characters (relationship maps), language and style,
and how NEB asks about it (answer-writing frames). For grammar: rule → many examples built
up on screen → exceptions → practice.

## Checking your work

```
python3 build.py scripts/<book>/unit_NN.py --preview               # 480p15, cheapest
LESSON_ONLY=2,3 python3 build.py scripts/<book>/unit_NN.py --preview   # only some parts
python3 contact.py .work/drafts/<book>-unit_NN-preview.mp4 /tmp/sheet.png 24   # then LOOK at the sheet
```

Look at contact sheets of every part: overlaps, text running off screen, things left on
stage, unreadable sizes, wrong colours. Fix and re-check. Renders are CPU-bound on a small
machine: preview single parts while iterating, and never run more than one render at a time
yourself.
