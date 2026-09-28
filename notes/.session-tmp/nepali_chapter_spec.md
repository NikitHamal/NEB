# Nepali chapter-writing spec for subagents (from session bash#982)

# SELF-CONTAINED SPEC — NEBians अनिवार्य नेपाली कक्षा ११ chapter

You have a STRICT token budget. Do NOT read AUTHORING.md, do NOT read other unit files,
do NOT read the curriculum, do NOT web-search. Everything you need is in this spec plus
your one source file. Budget your calls like this:
  call 1: cat your source file (/tmp/chNN.txt)
  call 2: Write the whole chapter in ONE Write call
  calls 3+: the QA gate below
If you feel you are running low, WRITE THE FILE IMMEDIATELY. An unwritten chapter is a
total failure; a written chapter with a rough figure is recoverable.

## Source
/tmp/chNN.txt is the decoded primary-source CDC textbook chapter. It is a Preeti->Unicode
conversion, so stray glyphs appear (`÷` means `/`, strings like `ज्ञद्दठ` are page numbers,
`ः` is often `:`). Reconstruct sensibly. Where a word is unrecoverable, do NOT guess a fact.
Everything you write must come from this source. Never invent an author, date or statistic.

## Language
The ENTIRE chapter is in Nepali (Devanagari) — every heading, every sentence, every table
cell, every model answer. Only the frontmatter keys, the two English headings named below,
and the callout keys are in English.

## Frontmatter — exactly this shape, nothing more
---
subject: अनिवार्य नेपाली
grade: 11
unit: <N>
title: <given to you>
hours: <given to you>
area: पाठ
---

## Markup rules
- Headings are Nepali `## N.1 लेखक परिचय` style, EXCEPT the last two which must be
  literally `## Chapter summary` and `## Practice questions`. The build only auto-frames
  those exact English strings — Nepali equivalents silently lose their styling.
- Callout fences: ENGLISH key, Nepali body. Available keys:
  `::: key`, `::: definition`, `::: example`, `::: caution`, `::: note`, `::: tip`, `::: memory`
  Opened as `::: key शीर्षक` and closed with a bare `:::` on its own line.
- Exam marks: `<span class="marks">[5]</span>`
- Markdown tables are used heavily — they are the house style for comparisons,
  शब्दार्थ lists and खण्ड maps.
- NO math. Avoid the `$` character entirely anywhere in the file.
- Bold with `**…**`. Do not write backslash-commands of any kind.

## Chapter shape (follow this order)
1. An opening paragraph (no heading) that says what the पाठ is, who wrote it, and
   NAMES THE MARKS it carries in the exam (पाठगत बोध ८ अङ्क, समीक्षात्मक ८ अङ्क).
2. A `::: key` box called "परीक्षाले खोज्ने तीन कुरा" listing the three things most
   likely to be asked from this पाठ.
3. `## N.1 लेखक परिचय` — but if the textbook gives NO byline, title it
   `## N.1 रचनाको स्रोत र पृष्ठभूमि` and say plainly that no author is named.
4. `## N.2 पाठको पृष्ठभूमि`
5. `## N.3 विषयवस्तु — सार`
6. `## N.4 खण्डगत व्याख्या` — prose plus a table with columns
   | खण्ड | अनुच्छेद/दृश्य | विषय | सोधिने प्रश्न |
7. `## N.5 पात्र परिचय` — ONLY for नाटक and संवादात्मक रचना. Table of नाम / भूमिका /
   चारित्रिक विशेषता.
8. `## मूल भाव`
9. `## विधागत विशेषता — <विधा>`  <-- THE MOST IMPORTANT SECTION, see below.
10. `## भाषाशैली र अलङ्कार` — bulleted; name the शैली, the शब्दस्रोत mix
    (तत्सम/आगन्तुक/तद्भव), and at least three अलङ्कार with a quoted example each.
11. `## समीक्षात्मक टिप्पणी` — three labelled parts: **बलियो पक्ष**, **कमजोर पक्ष**,
    **समग्र मूल्याङ्कन**. Be genuinely critical, not just praising.
12. `## शब्दार्थ` — a two-column table, AT LEAST 18 entries, taken from the textbook's
    own शब्दार्थ list where it has one.
13. `## Chapter summary` — bullets only, exam-facing, carrying every name, number and date.
14. `## Practice questions` — see below.

Include at least one `::: example` that WORKS A QUESTION rather than stating a fact —
e.g. "व्याख्या कसरी लेख्ने" broken into चरण १ सन्दर्भ / चरण २ अर्थ विस्तार / चरण ३ निचोड,
with the full worked answer shown. Also at least one `::: caution` naming a mistake
students actually make, and one `::: memory` giving a mnemonic for a list.

## विधागत विशेषता — why this section decides the grade
Units 9–12 of this book exist to teach four DIFFERENT विधा (रिपोर्ताज, संवादात्मक रचना,
दैनिकी, वक्तृतात्मक रचना) and unit 8 teaches लघु नाटक. The exam asks, verbatim,
"यो रचनाको विधागत विशेषता लेख्नुहोस्". So this section must contain:
  - a `::: definition` of the विधा,
  - a two-column table: | विशेषता | यस पाठमा कसरी देखिन्छ | — at least 7 rows, every
    row's right-hand cell citing something concrete from THIS text,
  - a `::: caution` naming the commonest wrong answer and drawing the boundary against
    the neighbouring विधा.

## Practice questions
Reproduce the TEXTBOOK'S OWN exercise items from your source file — do not make up a
fresh exercise set. Group them under bold Nepali headings by mark value, e.g.
`**पाठगत बोध — छोटो उत्तर (२ अङ्क)**`. Each numbered question carries its
`<span class="marks">[2]</span>`. After each group, put the model answers in a
`::: note उत्तर` block, numbered `**१.**`, `**२.**` … in Nepali numerals.
5- and 8-mark answers must be genuinely full-length — an 8-mark answer runs several
paragraphs with an introduction, substantive body and निष्कर्ष. Not a sketch.

## Figures — exactly 2 drawn ```figure blocks
Fenced as:
    ```figure caption="<Nepali caption>"
    <python>
    ```
The code MUST begin with these two lines or all Devanagari renders as TOFU BOXES:
    matplotlib.rcParams['font.family'] = 'sans-serif'
    matplotlib.rcParams['font.sans-serif'] = ['Noto Sans Devanagari', 'DejaVu Sans']
Rules: create the figure yourself and leave it in a variable named `fig`.
figsize width must be 4.0–5.2 inches, height 2.2–4.6 inches.
`INK`, `MUTED`, `GRID`, `ACCENT`, `SERIES` are pre-injected palette constants — use them.
`matplotlib`, `plt`, `np` are pre-imported. No `plt.show()`, no `savefig`, no file I/O.
Prefer clean box-and-arrow diagrams over charts unless you have verified numbers.
Quality bar: no overlapping text, no label clipped by the axes limits, no arrow that
starts or ends inside a text label, no legend sitting on top of data, no tofu.

Working pattern for a box-and-arrow diagram:
    fig, ax = plt.subplots(figsize=(5.0, 3.0))
    ax.axis('off')
    ax.add_patch(matplotlib.patches.FancyBboxPatch((x-0.82, y-0.40), 1.64, 0.80,
        boxstyle='round,pad=0.05', fc='#e3f0e0', ec=INK, lw=1.0, zorder=3))
    ax.text(x, y, 'पाठ', ha='center', va='center', fontsize=8.4, color=INK, zorder=4)
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.4))
    ax.set_xlim(...); ax.set_ylim(...)
Set the limits generously so nothing is clipped.

## Photo blocks
Fenced as:
    ```photo id="nep11/xxx" caption="<Nepali caption>" width="92"
    crop 0.02 0.04 0.98 0.99
    tint 0.10
    mark 0.36 0.44 "1"
    key 1 <Nepali text>
    ```
CRITICAL: overlay text drawn by the `label`, `call`, `box "text"` and `scale "text"`
directives does NOT get the Devanagari font and comes out as TOFU BOXES. NEVER put
Devanagari in those directives. Use numbered `mark X Y "n"` discs (ASCII digits only)
plus `key n <Nepali text>` lines — key entries are emitted as HTML below the photo and
render Devanagari correctly. Coordinates are fractions of the image, y measured from
the BOTTOM. Never type an attribution or licence into the chapter; the build adds it.

## Length
2,800–3,400 words, unless told otherwise.

## QA GATE — you are not done until these pass and you have LOOKED at every PNG
    cd /data/workspace/NEB/notes/pipeline
    python3 check.py ../content/nep11/unit-NN.md          # must print OK
    python3 preview.py ../content/nep11/unit-NN.md /tmp/pNN    # then Read each PNG
    python3 photoprev.py ../content/nep11/unit-NN.md /tmp/qNN  # then Read each PNG (if you have a photo)
Read every PNG and judge it against the quality bar above. Fix and re-render until clean.

## Scope
Create/modify ONLY your own /data/workspace/NEB/notes/content/nep11/unit-NN.md.
Do not touch pipeline/, do not touch any other unit's file, do not git commit.

## Report back
Absolute path, title, word count, figure count, photo count, the exact check.py output
line, whether Devanagari rendered correctly in the figures and the photo, and anything
in the source you could not decipher or verify.
