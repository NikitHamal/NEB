# NEBians chapter authoring contract — READ FULLY BEFORE WRITING

You are writing one chapter of a printed study book for Nepali NEB (National
Examination Board) Grade 11/12 science-stream students. The output is a PDF
built by a custom pipeline. **Follow this format exactly** or the build breaks.

Your file: `/workspace/nebians/content/<slug>/unit-NN.md` (NN zero-padded).
The exemplar to imitate for depth, tone and structure:
`/workspace/nebians/content/phy11/unit-03.md` — **read it first.**

---

## 1. Required frontmatter

```
---
subject: Physics
grade: 11
unit: 3
title: Kinematics
hours: 5
area: Mechanics
---
```

Copy `title`, `hours`, `area` **verbatim from the curriculum spine** at
`/workspace/nebians/curriculum/<slug>.md`. Do not invent or reword them. The
syllabus bullet list under the unit in the spine is injected automatically — you
do not write it, but **every bullet must be covered** by a section of your
chapter, in the same order.

## 2. Structure of the chapter

1. A 3–6 line opening paragraph: what this unit is about and why it matters.
2. Optionally one `::: key` box orienting the student to what the exam wants.
3. One `## N.1`, `## N.2`, … section **per syllabus bullet** (N = unit number),
   in syllabus order. Use `### ` for subsections when a section gets long.
4. `## Chapter summary` — 5–9 tight bullets, every formula restated.
5. `## Practice questions` — see §7.

## 3. Markdown you may use

Standard markdown: `**bold**`, `*italic*`, `-` bullets, `1.` numbered lists,
pipe tables with a header row, `> ` blockquote. Use tables generously —
comparisons, properties, units, reagents, classifications all belong in tables.

## 4. Math

- Inline: `$v = u + at$` — single dollars, must stay on one line.
- Display: `$$ ... $$` — may span lines.
- The renderer is matplotlib **mathtext**, not LaTeX. It supports `\frac`,
  `\sqrt`, `\int`, `\sum`, `\lim`, `\vec`, `\hat`, `\text{...}`, `\mathrm`,
  greek letters, `^`, `_`, `\left(...\right)`, `\times`, `\cdot`, `\approx`, `\le`,
  `\Rightarrow`, `\Longrightarrow`, `\partial`, `\infty`, `\circ`.
- It does **not** support: `\begin{align}`, `\mathbf`, `\underbrace`, `\ce{}`,
  `\SI{}`, `\substack`, matrices, `\overset`, `\xrightarrow`. Do not use them.
- Chemical equations are **plain text, not math**: write
  `2H₂ + O₂ → 2H₂O` or `CaCO₃ --Δ--> CaO + CO₂` as ordinary text/table cells
  using Unicode subscripts (₀₁₂₃₄₅₆₇₈₉), superscripts (⁺⁻²³) and arrows (→ ⇌ ↑ ↓).
- Inside **figure code**, matplotlib text is NOT passed through the rewriter:
  `\ge`, `\le`, `\ne`, `\to`, `\lvert` will crash `savefig`. Use Unicode
  (≥ ≤ ≠ → |) in figure labels instead.
- `\lvert`/`\rvert` are unsupported anywhere — use plain `|`.
- numpy 2.x: `np.trapz` is gone, use `np.trapezoid`.
- Units in prose: prefer Unicode (`m s⁻¹`, `Ω`, `μF`, `°C`) over math mode.

## 5. Figures — you write real matplotlib code

Every chapter needs **2–6 figures**. Use a fenced block tagged `figure`:

````
```figure caption="Velocity–time graph for uniform acceleration."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.8))
...
```
````

Rules:
- The code is executed at build time. It **must** leave a matplotlib `Figure`
  in a variable named `fig`. Never call `plt.show()` or `savefig`.
- Available already in scope: `plt`, `np`, `matplotlib`, and the palette
  constants `INK` (near-black), `MUTED` (grey), `GRID`, `ACCENT` (blue),
  `SERIES` (6-colour list). Use them instead of default colours.
- `figsize` width must be **4.0–5.2 inches**, height 2.2–3.4 in.
  Portrait/diagram figures may be up to 4.6 in tall.
- Hide chartjunk: `ax.spines[['top','right']].set_visible(False)`, light grid.
- Captions may contain `$math$`. Caption is auto-numbered "Figure N." — do not
  number it yourself.
- Diagrams (ray diagrams, circuits, apparatus, cell structure, free-body
  diagrams, energy-level diagrams, titration setups) are drawn with
  `ax.plot`, `ax.annotate`, `Circle`/`Rectangle`/`FancyArrow` patches and
  `ax.axis('off')`. Draw them properly — labelled, to scale, exam-accurate.
- If a figure would be pure decoration, don't include it. Every figure must
  carry information the text cannot.

## 6. Callout boxes

```
::: key Title here
Body markdown, may contain math and lists.
:::
```
Types and when to use them:

| Type | Use for |
|---|---|
| `key` | the central idea a student must not miss |
| `definition` | a formal definition, stated the way NEB expects it |
| `derivation` | a full step-by-step derivation (examiners award marks per step) |
| `example` | a fully worked numerical problem with **Problem.** / **Solution.** |
| `caution` | a specific common mistake students actually make |
| `tip` | exam technique, shortcuts, what the marker is looking for |
| `note` | answers to the practice questions, side remarks |
| `memory` | mnemonics, ordered lists worth memorising |

Every chapter needs **at least 3 worked examples** (`::: example`) with full
numerical solutions showing every step and units, and at least one `caution`.
Derivable results must actually be derived, not asserted.

## 7. Practice questions — NEB exam style

End with `## Practice questions` containing the groups that match the subject's
real paper pattern (given in the header line of the curriculum spine file).

For Physics/Chemistry/Biology/Maths/CS:

```
**Group A — Multiple choice (1 mark each)**

1. Question text <span class="marks">[1]</span>
   (a) option (b) option (c) option (d) option
2. ...

::: note Answers to Group A
**1.** (b) — one-line reason.
:::

**Group B — Short answer (5 marks each)**

1. ... <span class="marks">[5]</span>

::: note Answers to Group B
**1.** full worked solution.
:::

**Group C — Long answer (8 marks each)**
```

Rules:
- **Number each group from 1 again** and reference answers by that number.
- Minimum per chapter: 4 MCQs, 4 short, 2 long. Answer keys for MCQs (with a
  one-line reason) and full solutions for every numerical question. Purely
  theoretical "derive/explain" questions need at least an answer outline.
- Marks must match the subject's real pattern. Biology: short = 4 marks, long =
  8. Computer Science: paper is 2 hrs / 50 marks. English and Nepali have no
  Group A/B/C — use the real section names from the spine header.
- Write questions in the style of actual NEB papers: numerical answers should
  come out to clean numbers, and phrasing should mirror board wording
  ("Define …", "Derive an expression for …", "A body of mass 5 kg …").

## 8. Depth and accuracy — the part that actually matters

- Target **1,500–2,600 words** of substantive content per chapter, plus figures,
  examples and questions. A 5-hour unit gets more than a 2-hour unit.
- This must be **correct**. Every constant, formula, date, reaction, taxonomic
  name and numerical answer must be right. Recompute every worked example
  before writing the answer. If you are unsure of a fact, look it up with
  WebSearch/WebFetch rather than guessing.
- Use SI units and NEB/CDC conventions and terminology, and Nepali context in
  examples where natural (Nepali place names, rupees, local phenomena) — but
  never at the cost of clarity.
- Do not pad. No "in conclusion", no restating the syllabus, no filler.
- Write plainly for a 16–18 year old who may be reading in their second
  language. Short sentences. Define jargon at first use.

## 9. Before you finish

Run the build on your file to prove it compiles:

```
cd /workspace/nebians/build && python3 check.py ../content/<slug>/unit-NN.md
```

It prints any math that failed to parse and any figure code that raised. **Fix
every failure** and rebuild until clean. Then report: the file path, word count,
number of figures, examples and questions.

## 10. Matrices and determinants (Mathematics)

`mathtext` has no `\begin{matrix}` / `pmatrix` / `bmatrix` / `vmatrix`. **Never write
one** — it will fail to parse. Draw matrices as figures instead, using the two
helpers already available inside every ```figure block:

```figure caption="Inverse of a $2\times2$ matrix."
fig = mateq(["$A^{-1} =$", "$\\frac{1}{ad-bc}$", [["$d$", "$-b$"], ["$-c$", "$a$"]]])
```

`mateq(items)` lays out one line of a matrix equation. Each item is either:
- a string — a text run, mathtext allowed (`"A ="`, `"$\\times$"`, `"= -2"`)
- a list of lists — a bracketed matrix `[[1, 2], [3, 4]]`
- `("det", [[...], [...]])` — a determinant with vertical bars

Optional kwargs: `fontsize` (default 11), `colw` (0.52 — widen for long entries
like `$a_{11}$`), `rowh`, `gap`, `scale`.

`matrix(ax, rows, x, y, bracket="[")` draws a single matrix onto an axes you
already own, for when a matrix is one part of a larger diagram.

For a matrix mentioned in running prose, prefer naming its entries
($a_{11}$, $a_{12}$, …) over trying to typeset the array inline.

## 11. What the build does for you (do not hand-roll these)

Added after issue #48, where a teacher review of the Physics 11 PDF turned up
layout and rendering faults that were cheaper to fix once in the pipeline than
144 times in the content.

**Inline math may wrap.** `$...$` may now be hard-wrapped across up to four
source lines. It must not cross a blank line or run into a new block (a
heading, a table row, a `:::` fence, a code fence). Before this, a wrapped
formula silently failed to pair and its `$` signs paired with the *neighbouring*
formula's — so raw LaTeX reached the PDF while an innocent word like "Height"
rendered as italic math. `check.py` now reports any `$` left unpaired as
**UNPAIRED $** and fails the file. Never ship a chapter that reports one.

**Never write `\\` in front of a command.** `\\approx` is not `\approx`; the
second backslash used to be eaten and the word "approx" printed into the PDF.
The cleaner now repairs this, but write `\approx`.

**MCQ options and question parts lay themselves out.** Keep writing them the
natural way, all on one line:

    1. The value of $g$ at the centre of the Earth is <span class="marks">[1]</span>
       (a) maximum (b) equal to the surface value (c) zero (d) infinite

The build splits the `(a) (b) (c) (d)` run into a proper option grid, choosing
four, two or one column from the longest option. A run whose parts carry their
own `[n]` marks, or whose parts are long prose, is laid out as stacked
sub-parts instead. Do not build tables or lists of options by hand.

**Answer keys split themselves.** `**1.** ... **2.** ...` written on consecutive
lines inside a `::: note` box is given one line per answer.

**The chapter summary is framed automatically.** Use the exact heading
`## Chapter summary` and nothing else; the build wraps it in a highlighted
panel. Keep the summary to the facts a student revises from.

**Every page carries the NEBians watermark** from `build/brand/`. Do not add
logos to figures.

## 12. Figure quality bar

A figure is not done when it renders. It is done when you have rendered it to
PNG **in your own private directory** and looked at it. The review that
prompted this said: *"figures are good but please take care of
clutteredness/overlaps — make clean ones, handle texts cleanly, no overlaps."*

Check every one of these before you move on:

- no text overlapping other text, an arrow, a line, a box or a shaded region
- no label clipped by the tight bounding box
- no arrow starting or ending inside a label
- no legend over data
- a label that must sit on a busy area gets `bbox=dict(fc="white", ec="none", pad=1.5)`,
  but moving it to clear space is always better
- if a label cannot be placed clear, use a short leader line to it

Real faults this pass caught, all of which rendered without error: a prism
whose rays crossed both faces without refracting, dipole field lines with the
arrowheads pointing into the positive charge, an angle of incidence marked on
the wrong side of the normal, a conduction band drawn with `alpha=0.0` so the
box vanished from two panels out of three, and two force arrows drawn at
identical coordinates so one hid the other.

## 13. Derivations

From the same review: *"important derivations shall be focused a bit more and
show extra steps, in simplified language."*

Put every examinable derivation in a `::: derivation` box, titled with the
result being derived, and follow this shape:

1. One plain sentence: what we start from, what we are heading for.
2. **Setting up** — the physical situation and the symbols.
3. **Step n — a short plain-English reason.** One algebraic move per displayed
   line. Never "it can be shown that", "after simplification" or "similarly".
4. **Result**, stated cleanly.
5. **What it means** physically, and the **conditions** it relies on.

Follow it with a `::: tip The examiner is looking for` listing the
marks-bearing steps. Write for a 16-year-old whose first language is not
English: short sentences, ordinary words.
