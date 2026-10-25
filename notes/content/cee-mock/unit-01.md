---
subject: Model Papers and Mock Tests
grade: CEE
unit: 1
title: The MECEE-BL Examination: Pattern, Weightage and Strategy
hours: 0
area: The Examination
---

This chapter is the map for the rest of the book. It explains who sits the Medical
Education Common Entrance Examination for Bachelor Level (MECEE-BL, usually just
called "CEE"), how the 200 questions are spread across the syllabus, how the
negative marking really works and when a guess pays, and how to spend the last
four months, the last two months and the last fortnight. The five model papers that
follow are built on this map, question for question.

::: key The paper in one box
- **200 single-best-answer MCQs, four options, 3 hours** (180 minutes, 54 seconds a question), 200 marks, answered on an OMR sheet.
- **+1** for a right answer, **−0.25** for a wrong one, **0** for a blank.
- Group I (MBBS, BDS, BSc Nursing, BSc Midwifery, BASLP, B Perfusion): **Zoology 40, Botany 40, Chemistry 50, Physics 50, Mental Agility Test 20**.
- Setters are told to write **50 % recall, 30 % understanding, 20 % application**, with stems of at most 60 words.
- A candidate must reach the **50th percentile** of the scores to enter the merit list; a place on the list is not yet a seat.
- Syllabus in force: MEC bachelor-level syllabus, **third revision 2083-01-15 (28 April 2026)**. Older guides built on the second revision have different domains.
:::

## 1.1 Who sits the paper, the programme groups and the eligibility rules

The examination is conducted by the **Medical Education Commission (MEC)** under the
Medical Education Act, 2075. It is the single gateway to every bachelor-level
health-science seat in Nepal — government and private, in every university and
academy (TU, KU, BPKIHS, PAHS, NAMS, KAHS, Karnali and others). MEC names a cycle
after the year of admission, so the papers sat from **31 October to 4 November
2026 (Kartik 14–18, 2083)** belong to **MECEE-BL 2027**.

### The four programme groups

| Group | Programmes | Paper (200 questions) |
|---|---|---|
| I | MBBS, BDS, BSc Nursing, BSc Midwifery, BASLP, B Perfusion Technology | Zoology 40, Botany 40, Chemistry 50, Physics 50, MAT 20 |
| II | BAMS, BSc MLT, BSc MIT, BSc Radiotherapy, BPT, B Pharm, B Optometry and similar | Zoology 40, Botany 40, Chemistry 40, Physics 40, programme-specific PCL content 20, MAT 20 |
| III | BPH | Zoology 40, Botany 40, Chemistry 40, Physics 40, prerequisite health knowledge 20, MAT 20 |
| IV | BNS, BMS (for nurses with a PCL) | nursing subjects 150, basic and integrated health science 30, MAT 20 |

This book follows the **Group I** paper, which is also the one that most +2 science
students sit. A Group II or III candidate can use every chapter as it stands — the
Physics and Chemistry sections are simply ten questions shorter in the real paper.

### Eligibility in short

| Route | Usual minimum (check the year's notice) |
|---|---|
| +2 Science (NEB) or equivalent | Physics, Chemistry and Biology studied; **at least 50 % aggregate or CGPA 2.4** |
| Health-science PCL/diploma (for the programmes that allow it) | at least 50 % in the diploma, the Grade 12 science equivalence where required, and registration with the relevant council |
| BNS / BMS | PCL or diploma in Nursing with at least 50 %, registered with the Nepal Nursing Council |

The notice for each cycle can add conditions on subjects, equivalence, foreign
qualifications and quota categories, and the dates change every year. The rules
above are the stable core; the authority is always the current notice on the MEC
website and the admit card, which names your centre and reporting time.

::: caution Read the notice, not a coaching poster
Dates, fees and category rules change between cycles. In the 2027 cycle the
double-fee window closed in September 2026 and the MBBS paper was set for 31
October 2026, 11:00 a.m. to 2:00 p.m. — but for any later cycle, check MEC's own
notice before you plan backwards from a date.
:::

## 1.2 The paper: 200 questions, unit by unit, and how the marks are counted

The syllabus fixes the number of questions in every **unit** (area). How a unit's
questions fall between its chapters is not published; the NEBians books give an
estimate in each chapter, and the model papers use those estimates. The unit
totals below are official.

| Subject | Unit (official count) |
|---|---|
| Zoology (40) | Evolutionary biology 3 · Animal diversity and classification 4 · Animal tissues 4 · Plasmodium, earthworm and frog 6 · Human biology and physiology 15 · Microbial diseases and immunology 4 · Medical technology and applied biology 2 · Biota, environment and conservation 2 |
| Botany (40) | Basic components of life 2 · Biodiversity 9 · Ecology and vegetation 4 · Cell biology 5 · Genetics 6 · Plant anatomy 3 · Plant physiology 6 · Developmental botany 2 · Applied botany 3 |
| Chemistry (50) | Physical 17 · Inorganic 10 · Organic 17 · Applied 3 · Analytical 3 |
| Physics (50) | Mechanics 10 · Heat and thermodynamics 7 · Waves and optics 8 · Current electricity and magnetism 9 · Electrostatics and capacitors 4 · Modern physics 12 |
| MAT (20) | Verbal reasoning 5 · Numerical reasoning 5 · Logical sequencing 5 · Spatial relation and abstract reasoning 5 |

```figure caption="Where the 200 marks are. Each block is one official unit (the order of the table above), with its question count; the biggest single blocks are Human biology (15), Physical and Organic chemistry (17 each) and Modern physics (12)."
fig, ax = plt.subplots(figsize=(5.2, 4.4))
data = [
    ("Zoology", [("Evol.", 3), ("Divers.", 4), ("Tissues", 4), ("Animals", 6), ("Human", 15), ("Disease", 4), ("Med.tech", 2), ("Env.", 2)]),
    ("Botany", [("Biomol.", 2), ("Biodiv.", 9), ("Ecol.", 4), ("Cell", 5), ("Genetics", 6), ("Anat.", 3), ("Physiol.", 6), ("Devel.", 2), ("Applied", 3)]),
    ("Chemistry", [("Physical", 17), ("Inorg.", 10), ("Organic", 17), ("Applied", 3), ("Analyt.", 3)]),
    ("Physics", [("Mech.", 10), ("Heat", 7), ("Wave/opt.", 8), ("Elec/mag", 9), ("Electrost.", 4), ("Modern", 12)]),
    ("MAT", [("Verbal", 5), ("Numer.", 5), ("Sequence", 5), ("Spatial", 5)]),
]
y = 0
for si, (subj, units) in enumerate(data):
    left = 0
    for k, (name, n) in enumerate(units):
        ax.barh(y, n, left=left, color=SERIES[si % len(SERIES)], alpha=0.55 + 0.45 * (k % 2), edgecolor="white", height=0.62)
        lab = f"{name}\n{n}" if n >= 6 else f"{n}"
        ax.text(left + n / 2, y, lab, ha="center", va="center", fontsize=7, color=INK)
        left += n
    ax.text(-1, y, f"{subj} ({left})", ha="right", va="center", fontsize=9, color=INK)
    y -= 1
ax.set_xlim(-14, 52)
ax.set_ylim(-4.6, 0.6)
ax.set_xticks([0, 10, 20, 30, 40, 50])
ax.set_yticks([])
ax.set_xlabel("questions", fontsize=9)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.grid(axis="x", color=GRID, lw=0.6)
ax.set_axisbelow(True)
```

### The cognitive split and what it means for you

MEC instructs setters to write about **100 recall, 60 understanding and 40
application** questions. Recall questions (a name, a number, a definition, an
example) are the fastest marks in the hall — ten to twenty seconds each if you
know them. Application questions (a numerical, a cross, a reaction sequence) take
one to two minutes. So the 54-second average is not spent evenly: a student who
races through recall at 20 seconds a question banks more than an hour for the
numericals.

### How the score becomes a rank

1. Raw score = right − 0.25 × wrong. Blanks score zero.
2. Candidates at or above the **50th percentile** of the scores qualify for the
   merit list (the notice sets a fallback — a 50 % score qualifies — for a
   programme with fewer than twice as many applicants as seats).
3. The merit list is used for seat matching by rank, quota category, seat type
   (government scholarship or paying) and your stated preferences. A rank is not
   a seat until you are matched and you complete admission on time.

## 1.3 Negative marking and when to guess

With four options and a quarter-mark penalty, the arithmetic is simpler than most
students think. If $p$ is your chance of being right on a question, the expected
mark from answering it is

$$ E = p\times 1 - (1 - p)\times 0.25 = 1.25p - 0.25 $$

$E$ is positive whenever $p > 0.2$. A blind guess among four options has
$p = 0.25$, so even a blind guess has a small positive expectation
($E = +0.0625$). Every option you can eliminate with confidence raises it sharply.

| Options you can rule out | $p$ | Expected mark from answering | Verdict |
|---|---|---|---|
| none (blind) | 1/4 | +0.06 | barely worth it; costs time and adds variance |
| one | 1/3 | +0.17 | answer |
| two | 1/2 | +0.38 | answer, always |
| three (you know it) | 1 | +1.00 | answer |

```figure caption="Expected mark from answering one question, against the probability $p$ that your choice is right. Above $p = 0.2$ answering pays; eliminating options moves you up the line."
fig, ax = plt.subplots(figsize=(4.8, 2.9))
p = np.linspace(0, 1, 200)
ax.plot(p, 1.25 * p - 0.25, color=ACCENT, lw=2)
ax.axhline(0, color=MUTED, lw=0.8)
ax.axvline(0.2, color=MUTED, lw=0.8, ls="--")
for pp, lab in [(0.25, "blind"), (1/3, "1 out"), (0.5, "2 out"), (1.0, "known")]:
    e = 1.25 * pp - 0.25
    ax.plot(pp, e, "o", color=SERIES[1], ms=5)
    off, ha = ((-8, -4), "right") if pp == 1.0 else ((8, -12), "left")
    ax.annotate(f"{lab} {e:+.2f}", (pp, e), textcoords="offset points", xytext=off, fontsize=7.5, color=INK, ha=ha)
ax.text(0.205, -0.2, "break-even p = 0.2", fontsize=7.5, color=MUTED)
ax.set_xlabel("probability your answer is right, p", fontsize=9)
ax.set_ylabel("expected mark", fontsize=9)
ax.set_xlim(0, 1.05); ax.set_ylim(-0.3, 1.1)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(color=GRID, lw=0.6)
```

::: caution The trap in "a blind guess pays"
The calculation assumes that a wrong option is chosen at random. Setters build
distractors from the commonest mistakes, so a *half-understood* question can pull
your $p$ **below** 0.2 — you are drawn to the trap, not to a random option. Answer
when you have **eliminated at least one option for a reason**; skip when your
"hunch" is really a vague memory of a word in one option.
:::

::: example Worked example 1.1 — what skipping costs
**Problem.** A student knows 120 answers, can eliminate two options in 40 more,
and has no idea about the last 40. Compare (i) answering only the 120, (ii)
answering the 160, (iii) answering all 200 at random for the last 40.

**Solution.** (i) 120. (ii) The 40 half-known questions add $40\times0.375 = 15$
on average: about 135. (iii) The 40 blind guesses add $40\times0.0625 = 2.5$ on
average, but with a spread of about ±3.5 marks. **Answering the half-known
questions is worth fifteen marks — often thousands of places in rank.** Blind
guessing is close to neutral; spend that time checking instead.
:::

### Three passes through the paper

1. **First pass (≈ 90 min):** answer everything you know at once; mark (on the
   question paper, not the OMR) questions that need work.
2. **Second pass (≈ 60 min):** the marked numericals and two-step questions;
   eliminate options and answer where at least one is ruled out.
3. **Third pass (≈ 20 min):** OMR check — every bubble in the right row, darkened
   completely, no stray marks — and a last look at the remaining blanks.

::: tip OMR discipline
Fill the OMR **section by section** (after every 20–30 questions), not all at the
end and not one bubble at a time. A shifted row — answer 57 bubbled in row 58 —
costs more marks than any hard question in the paper.
:::

## 1.4 A study plan for the last 120, 60 and 15 days

The plans assume about 8–10 hours of study a day after +2 and the official
weightage above. Adjust the share to your weak units, never to your favourite ones.

### 120 days out: build the base

| Weeks | Physics + Chemistry (100 Q) | Biology (80 Q) | MAT (20 Q) |
|---|---|---|---|
| 1–6 | Mechanics, Heat, Physical chemistry, General organic chemistry | Human physiology, Plasmodium/earthworm/frog, Biodiversity | 20 min a day, one area a week |
| 7–12 | Optics, Electricity and magnetism, Inorganic, Hydrocarbons to Amines | Cell biology, Genetics, Plant physiology and anatomy | timed sets of 20 |
| 13–17 | Modern physics, Electrostatics, Applied and Analytical chemistry | Evolution, Tissues, Applied zoology, Ecology, Applied botany | mixed sets |

Every day: one chapter's theory, then **all its Set A and Set B questions**, then
review every wrong answer and write the fact you missed in a one-line error log.

### 60 days out: practise under the clock

- One subject test (40–50 questions in 40–45 minutes) every day, rotating subjects.
- From day 45: a **full model paper every fourth day**, 3 hours, OMR-style, in the
  morning at the real exam time (11:00 to 14:00).
- Score every paper with the negative marking; track right, wrong and blank per
  unit in a table. Units with the most *wrong* answers get the next week's revision.

### 15 days out: consolidate, do not start anything new

- Revise only from the **Formula and fact sheets** and **Chapter summaries** of the
  subject books and from your own error log.
- Two full papers in the first ten days; none in the last three.
- Sleep at the time you will sleep before the exam; travel to the centre once in
  advance if it is unfamiliar. Keep the admit card, a photo ID and two black/blue
  ballpoint pens ready the night before.

::: memory The weightage in one line
"**Fifty-fifty, forty-forty, twenty**": Physics 50, Chemistry 50, Zoology 40,
Botany 40, MAT 20. Inside them, the giants are **Human biology 15**, **Physical
chemistry 17**, **Organic chemistry 17** and **Modern physics 12** — 61 marks in four
units.
:::

## 1.5 How to use the model papers in this book

Each model paper (chapters 2–6) is a complete 200-question paper built to the
official unit counts. A table at the top of each paper shows its actual count per
unit. Every question is original practice written to the third-revision syllabus —
none is copied from or claimed to be a past paper.

- **On the NEBians website or app**, open a model paper and choose *Take as a timed
  test*: a three-hour clock that does not pause, one answer per question, a
  question palette, and the real marking (+1, −0.25, 0). At the end you get your
  score, the right/wrong/blank count, a per-subject table and every explanation.
- **On paper**, print the PDF, set a timer for 180 minutes, mark answers on a
  separate sheet, and score with right − 0.25 × wrong.
- **After each paper**, spend at least as long on the key as on the paper: for every
  wrong or blank answer read the explanation, find the chapter in the subject book
  and add the missed fact to your error log.
- Take the papers **in order** and several days apart: each one tests different
  facts and different numbers, so later papers measure improvement, not memory.

::: tip Reading your score
On these papers, aim first for **120+** (60 %) and then for **150+**. More useful
than the total is the per-subject table: a section where you score under half is
where the next week of study goes.
:::

## Formula and fact sheet

| Item | Value |
|---|---|
| Questions, time, marks | 200 MCQs, 180 min, 200 marks; 54 s a question on average |
| Marking | +1 right, −0.25 wrong, 0 blank; score = R − 0.25W |
| Expected value of answering | $E = 1.25p - 0.25$; break-even $p = 0.2$ |
| Blind / one out / two out | +0.06 / +0.17 / +0.38 per question |
| Group I split | Zoology 40, Botany 40, Chemistry 50, Physics 50, MAT 20 |
| Group II/III split | Physics 40 and Chemistry 40, plus 20 programme-specific |
| Cognitive mix | recall 50 %, understanding 30 %, application 20 %; stem ≤ 60 words |
| Merit list | 50th percentile and above (50 % score fallback for undersubscribed programmes) |
| Syllabus | MEC third revision, 2083-01-15 (28 April 2026) |

## Chapter summary

- MECEE-BL is MEC's single entrance for every bachelor-level health-science seat;
  the 2027 cycle's papers ran from 31 October to 4 November 2026.
- Group I sits Zoology 40, Botany 40, Chemistry 50, Physics 50 and MAT 20; the unit
  counts inside each subject are official and drive every model paper here.
- Marking is +1, −0.25, 0; answering pays whenever your chance of being right
  exceeds 0.2, so answer every question where you can eliminate an option for a reason.
- A half-understood question can make you *worse* than random — distractors are
  built from common mistakes.
- Work in three passes and fill the OMR section by section.
- Build the base for four months, practise under the clock for two, and only
  consolidate in the last fortnight.
- Use each model paper as a diagnostic: the key and the error log matter more than
  the score.
