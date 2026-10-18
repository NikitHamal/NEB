---
subject: Question Bank
grade: 10
unit: 1
title: "The SEE Examination: Pattern, Grid and Strategy"
hours: 0
area: How to Use This Book
---

The Secondary Education Examination (SEE) is the first national examination a Nepali student sits, and it is built from a public specification. The number of questions, their size and the share of marks each content area carries are fixed before the paper is written, so only the wording changes from year to year. A question bank can therefore prepare you for the *shape* of the paper, not just for its content. This chapter lays out that shape for the six subjects in this series, explains how marks become a letter grade and a GPA, and gives a time plan you can rehearse.

::: key Five numbers to hold in your head
**75** — external (written) marks in each subject of this series. **25** — internal-assessment marks added by your school. **35%** — the minimum on the external paper (26.25 out of 75). **40%** — the minimum on the internal marks (10 out of 25). **2.4** — minutes available for every written mark in a three-hour, 75-mark paper. The rest of this chapter follows from these numbers.
:::

::: caution Read this about "past papers" first
This book does not label any question with the year it "appeared". Papers circulate on the internet with years attached, but this book could not verify individual items against an official released paper, so every question here is an **original practice question** written to the board's pattern. The sources it does stand behind are the published CDC specification grids and model questions, which give the pattern and the weights. Likewise, the "predicted questions" in chapters 4 and 7 are **ranked from the grid and the syllabus**; they are study priorities, not forecasts of what will be set.
:::

```figure caption="How the 100 marks of one subject are split, and where the pass lines fall. The external paper is 75 marks and 35 % (26.25 marks) passes it; the internal 25 marks need 40 % (10 marks)."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 2.5))
rows = ["Internal\n(25 marks, 40 % needed)", "External paper\n(75 marks, 35 % needed)"]
need = [10, 26.25]
rest = [15, 48.75]
y = np.arange(len(rows))
ax.barh(y, need, height=0.5, color=ACCENT, label="Minimum marks to pass")
ax.barh(y, rest, left=need, height=0.5, color=SERIES[3], label="Remaining marks")
for i, (n, r) in enumerate(zip(need, rest)):
    ax.text(n / 2, i, f"{n:g}", ha="center", va="center", color="white",
            fontsize=8.5, fontweight="bold")
    ax.text(n + r / 2, i, f"+{r:g}", ha="center", va="center", color=INK, fontsize=8)
ax.set_yticks(y, rows, fontsize=8)
ax.set_xlim(0, 80)
ax.set_xlabel("Marks", fontsize=8.5)
ax.tick_params(axis="x", labelsize=8)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.grid(axis="x", color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(fontsize=7.5, frameon=False, loc="lower right")
fig.tight_layout()
```

## 1.1 The SEE at a glance

Each subject paper is marked out of 75. Your school separately awards up to 25 internal marks for practical work, project work, class participation and terminal tests. The two parts are graded separately, and both must clear their minimum.

| Subject | Time | External | Internal | Shape of the external paper |
|---|---|---|---|---|
| Science and Technology | 3 hr | 75 | 25 | 10 MCQ, 9 very short, 14 short (2 marks), 7 long (4 marks) |
| Compulsory Mathematics | 3 hr | 75 | 25 | 16 numbered questions made of 49 items; no MCQ group |
| Compulsory English | 3 hr | 75 | 25 | skill-based questions: reading, literature, writing, grammar |
| Compulsory Nepali (अनिवार्य नेपाली) | 3 hr | 75 | 25 | skill-based questions: reading, writing, grammar, literature |
| Social Studies | 3 hr | 75 | 25 | objective, short and long questions across nine units |
| Optional Mathematics | 3 hr | 75 | 25 | Group A of 10 questions of 1 mark, Group B of 8 questions of 2 marks, then longer questions |

::: caution Check the notice for your year
The two rows with full detail (Science and Mathematics) are taken from the CDC specification grids for SEE 2080 onward. The other rows are described only as far as this book could confirm. Rules can be revised by the National Examination Board, so before the examination read the grid and model questions your school issues and trust them over any book, including this one.
:::

Two facts that are easy to miss:

- Some notes give Science as **two hours thirty minutes**. The 2081 science paper states **three hours** for 75 marks, and this book plans for three hours.
- Internal marks are not a safety net you can ignore. A student who scores 40 out of 75 on the external paper but only 8 out of 25 internally does not clear the 40% internal minimum.

## 1.2 From marks to a letter grade and GPA

Under the Letter Grading Guidelines used for SEE from 2080 onward, external and internal marks are converted to grades separately, using one percentage scale.

| Percentage | Letter grade | Grade point | Description |
|---|---|---|---|
| 90 and above | A+ | 4.0 | Outstanding |
| 80 to below 90 | A | 3.6 | Excellent |
| 70 to below 80 | B+ | 3.2 | Very good |
| 60 to below 70 | B | 2.8 | Good |
| 50 to below 60 | C+ | 2.4 | Satisfactory |
| 40 to below 50 | C | 2.0 | Acceptable |
| 35 to below 40 | D | 1.6 | Basic |
| below 35 | NG | — | Not graded |

### 1.2.1 Minimums and NG

A subject is graded only when the external paper reaches **35%** (26.25 of 75) **and** the internal marks reach **40%** (10 of 25). Missing either gives **NG** (not graded) in that subject. As announced for SEE 2080, a student with NG in at most two subjects may sit a grade-improvement examination; NG in more than two subjects means sitting the examination again in the following year. Treat this as the rule *as published*, and check the current notice.

### 1.2.2 Marks needed for each grade

Because the scale is a percentage, the external paper alone decides the grade you can reach on that component.

| External grade wanted | Percentage | Marks needed out of 75 |
|---|---|---|
| A+ | 90% | 67.5 |
| A | 80% | 60 |
| B+ | 70% | 52.5 |
| B | 60% | 45 |
| C+ | 50% | 37.5 |
| C | 40% | 30 |
| D | 35% | 26.25 |

For internal marks out of 25 the same percentages mean 22.5 for A+, 20 for A, 17.5 for B+, 15 for B, 12.5 for C+, 10 for C (and 8.75 for D, though 10 is the internal minimum for any grade).

### 1.2.3 Weighted GPA

The public SEE calculators weight each component by its credit hours: **3.75 external plus 1.25 internal** (5 credit hours) for Science, Mathematics, English and Nepali, and **3 plus 1** (4 credit hours) for Social Studies and each optional subject. With two optionals the total is $4\times5+3\times4=32$ credit hours. The overall GPA is

$$ \text{GPA}=\frac{\sum(\text{grade point}\times\text{credit hours})}{\sum\text{credit hours}} $$

::: example A GPA worked by hand
**Problem.** A student's marks (external out of 75, internal out of 25) are: Nepali 58, 21; English 62, 22; Mathematics 66, 20; Science 60, 21; Social Studies 52, 19; Optional I 70, 22; Optional II 48, 18. Find the GPA.

**Solution.** Convert each mark to a percentage and then a grade point.

| Subject | External % → GP | Internal % → GP | Credit split |
|---|---|---|---|
| Nepali | 77.3 → 3.2 | 84 → 3.6 | 3.75 + 1.25 |
| English | 82.7 → 3.6 | 88 → 3.6 | 3.75 + 1.25 |
| Mathematics | 88 → 3.6 | 80 → 3.6 | 3.75 + 1.25 |
| Science | 80 → 3.6 | 84 → 3.6 | 3.75 + 1.25 |
| Social Studies | 69.3 → 2.8 | 76 → 3.2 | 3 + 1 |
| Optional I | 93.3 → 4.0 | 88 → 3.6 | 3 + 1 |
| Optional II | 64 → 2.8 | 72 → 3.2 | 3 + 1 |

Weighted points: Nepali $3.2(3.75)+3.6(1.25)=16.5$; English $3.6\times5=18$; Mathematics $18$; Science $18$; Social Studies $2.8(3)+3.2(1)=11.6$; Optional I $4.0(3)+3.6(1)=15.6$; Optional II $2.8(3)+3.2(1)=11.6$. Sum $=16.5+18+18+18+11.6+15.6+11.6=109.3$.

$$ \text{GPA}=\frac{109.3}{32}\approx 3.42 $$
:::

The certificate issued by the board is the final word; the calculation shows where marks matter. Science, Mathematics, English and Nepali each carry $5\div32\approx15.6\%$ of the GPA, while Social Studies and each optional carry $4\div32=12.5\%$.

```figure caption="Marks to grade: the percentage you score on a subject becomes a letter grade and a grade point. Both the external paper and the internal assessment are graded on the same scale, and a GPA is the credit-weighted average of the subject grade points."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 2.6))
lo = np.array([90, 80, 70, 60, 50, 40, 35, 0])
hi = np.array([100, 90, 80, 70, 60, 50, 40, 35])
pts = np.array([4.0, 3.6, 3.2, 2.8, 2.4, 2.0, 1.6, 0.8])
labels = ["A+", "A", "B+", "B", "C+", "C", "D+", "NG"]
colors = [SERIES[0], SERIES[1], SERIES[2], SERIES[3], SERIES[4], SERIES[5], "#94a3b8", "#cbd5e1"]
for i in range(len(lo)):
    ax.barh(0, hi[i] - lo[i], left=lo[i], height=0.5, color=colors[i],
            edgecolor="white", linewidth=0.8)
    ax.text((lo[i] + hi[i]) / 2, 0, labels[i], ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="white" if i < 6 else INK)
    if i < len(lo) - 1:
        ax.text(lo[i], -0.42, f"{pts[i]:.1f}", ha="center", va="top",
                fontsize=7.5, color=MUTED)
ax.text(0, -0.62, "grade point", ha="left", va="top", fontsize=7.5, color=MUTED)
ax.set_xlim(0, 100)
ax.set_ylim(-0.85, 0.5)
ax.set_yticks([])
ax.set_xlabel("Percentage in the subject", fontsize=8.5)
ax.tick_params(axis="x", labelsize=8)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.grid(axis="x", color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

## 1.3 Science and Technology: the grid

### 1.3.1 Question types

| Group | Type | Questions | Marks each | Marks |
|---|---|---|---|---|
| A | Multiple choice | 10 | 1 | 10 |
| B | Very short answer | 9 | 1 | 9 |
| C | Short answer | 14 | 2 | 28 |
| D | Long answer | 7 | 4 | 28 |
| | **Total** | **40** | | **75** |

The board labels these groups in different ways in different papers; this book calls them A to D in the order above. The 19 chapters of the textbook cover Biology, Physics, Chemistry, Astronomy and ICT, and a typical paper draws on every area. The MCQs in the CDC model papers are often short scenarios (a lab observation, a number to substitute) rather than bare definitions, so practise using facts, not only recalling them.

### 1.3.2 What each type asks of you

| Type | What earns the mark | Typical length |
|---|---|---|
| MCQ (1) | The one correct option; usually a fact, a unit or a one-step calculation | 30–60 seconds |
| Very short (1) | One exact word, definition or value | one line |
| Short (2) | Two separate points, or a definition plus an example; a one-step numerical | 3–5 lines |
| Long (4) | Four creditable steps: an explanation with a labelled diagram, a comparison of four points, or a numerical with formula, substitution, answer and unit | 8–12 lines |

### 1.3.3 A time plan for 180 minutes

| Block | Marks | Minutes |
|---|---|---|
| Group A and B | 19 | 30 |
| Group C (14 questions) | 28 | 60 |
| Group D (7 questions) | 28 | 70 |
| Checking | — | 20 |
| **Total** | **75** | **180** |

That gives about 4.3 minutes per 2-mark question and 10 minutes per 4-mark question. If a numerical is not working after five minutes, mark it and move on.

## 1.4 Compulsory Mathematics: the grid

### 1.4.1 Marks by content area

The CDC grid for Compulsory Mathematics covers 160 working hours. Each area carries marks roughly in proportion to its hours.

| Area | Hours | Questions | Marks |
|---|---|---|---|
| Sets | 12 | 1 | 6 |
| Arithmetic | 28 | 3 | 13 |
| Mensuration | 28 | 3 | 13 |
| Algebra | 32 | 3 | 15 |
| Geometry | 28 | 3 | 13 |
| Statistics and Probability | 24 | 2 | 11 |
| Trigonometry | 8 | 1 | 4 |
| **Total** | **160** | **16** | **75** |

```figure caption="Marks carried by each content area of the Compulsory Mathematics paper (out of 75)."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.6))
areas=["Sets","Arithmetic","Mensuration","Algebra","Geometry","Stat. and Prob.","Trigonometry"]
marks=[6,13,13,15,13,11,4]
y=np.arange(len(areas))[::-1]
ax.barh(y,marks,color=ACCENT,height=0.6)
for yi,m in zip(y,marks):
    ax.text(m+0.3,yi,str(m),va='center',fontsize=8,color=INK)
ax.set_yticks(y); ax.set_yticklabels(areas,fontsize=8,color=INK)
ax.set_xlim(0,18); ax.set_xlabel("Marks",fontsize=8,color=INK)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='x',color=GRID,lw=0.5); ax.set_axisbelow(True)
```

### 1.4.2 Marks by thinking level

Each area is also split by the kind of thinking asked. The totals across the paper are:

| Level | What it tests | Marks |
|---|---|---|
| Knowledge | recall a formula, term or definition | 12 |
| Understanding | interpret, draw, explain, relate | 18 |
| Application | solve a standard problem | 30 |
| Higher ability | multi-step or unfamiliar problem | 15 |
| **Total** | | **75** |

Sixty marks (knowledge, understanding, application) come from standard material you can practise, and 15 from higher-ability items. The grid also says a question may link more than one area: an item can start with a Venn diagram and end with a ratio, for instance, with the parts marked separately.

### 1.4.3 Time plan

Sixteen questions in 180 minutes is about **11 minutes** a question, or 2.4 minutes a mark. A question worth 6 marks (Sets) deserves about 14 minutes; the 4-mark Trigonometry question about 10. Do the parts worth the first one or two marks of each question first: those are the knowledge and understanding marks, and they are the easiest to bank.

## 1.5 The other four subjects

**Compulsory English.** The paper tests reading, literature, writing and grammar in separate questions, so the most reliable gain is practice in the skill, not memorising text. Chapters 8 to 10 follow the question types.

**Compulsory Nepali (अनिवार्य नेपाली).** The paper is organised by language skill: comprehension, writing, grammar and literature. Chapters 11 to 13 mirror it.

**Social Studies.** Nine units spread across culture, civic sense, geography, history, economy, international relations and development. The marks are spread widely, so no unit can be skipped. Chapters 14 to 16 give unit-wise banks.

**Optional Mathematics.** The CDC model paper opens with ten one-mark questions and eight two-mark questions, then moves to longer ones across algebra, matrices, trigonometry, vectors, geometry and statistics. Chapters 17 to 19 follow it.

## 1.6 Strategy that works across subjects

1. **Read the whole paper for five minutes** (or use the first minutes of each group) and mark the questions you can finish fastest.
2. **Bank the one-mark questions first.** In Science, 19 of 75 marks are one-mark items; these are secured in 30 minutes.
3. **Write to the marks.** Two marks means two points; four marks means four creditable steps. Extra lines earn nothing, and a missing step costs a mark.
4. **Show every numerical step**: formula, substitution, answer, unit. A correct final number with no working may earn partial marks only.
5. **Draw diagrams in pencil, labelled, in a ruled box.** A labelled diagram is often a full mark by itself.
6. **Never leave a blank.** An attempt at a definition or a first step often earns a mark; a blank earns none.
7. **Keep five minutes at the end** to check units, signs and that every question number is written.

### 1.6.1 A revision calendar

| Weeks left | What to do |
|---|---|
| 8–6 | Read the chapter notes; do the objective bank for each chapter |
| 5–3 | Do the subjective bank in timed blocks; correct against the model answers |
| 2 | Sit one full model set per subject under exam conditions |
| 1 | Revisit only your error list and the formula sheets; sleep well |

## 1.7 How to use this book

| Chapters | Subject | Contents |
|---|---|---|
| 2–4 | Science and Technology | objective bank, subjective bank, two model sets and ranked practice questions |
| 5–7 | Compulsory Mathematics | the same three parts |
| 8–10 | Compulsory English | the same three parts |
| 11–13 | Compulsory Nepali (अनिवार्य नेपाली) | the same three parts |
| 14–16 | Social Studies | the same three parts |
| 17–19 | Optional Mathematics | the same three parts |

Every question is marked **practice**: it is an original item written to the pattern. Each objective question has a key with a one-line reason, and each subjective question has a model answer; numerical answers have been recomputed.

## Chapter summary

- Each subject is **75 external + 25 internal**; the external paper is three hours.
- A subject is graded only if the external mark is at least 35% (26.25 of 75) and the internal mark at least 40% (10 of 25); otherwise it is NG.
- Grades: A+ at 90%, A 80%, B+ 70%, B 60%, C+ 50%, C 40%, D 35%, with grade points 4.0, 3.6, 3.2, 2.8, 2.4, 2.0, 1.6.
- Science: $10\times1+9\times1+14\times2+7\times4=75$. Mathematics: 16 questions, 49 items, area marks 6, 13, 13, 15, 13, 11, 4.
- Time: 2.4 minutes per mark. Bank the one-mark items first, show every step, never leave a blank.
- Practice questions in this book are original and ranked predictions are study priorities, not forecasts.

## Practice questions

**Short answer**

1. A student scores 45 out of 75 externally and 18 out of 25 internally in Science. Find the grade for each part and say whether the subject is graded. <span class="marks">[2]</span>
2. Calculate the total of $10\times1+9\times1+14\times2+7\times4$ and name the group each term represents. <span class="marks">[2]</span>
3. A student gets 26 out of 75 in the external paper of English. What happens to the subject, and what is the minimum external mark needed? <span class="marks">[2]</span>
4. How many minutes per mark does a three-hour, 75-mark paper allow? How many minutes does that give for a 4-mark question? <span class="marks">[2]</span>
5. In the Mathematics grid, which two areas together carry 28 marks? <span class="marks">[2]</span>

::: note Answers
**1.** External: $45\div75=60\%$ → B (2.8). Internal: $18\div25=72\%$ → B+ (3.2). Both clear their minimums, so the subject is graded.

**2.** $10+9+28+28=75$. Terms: MCQ (Group A), very short (B), short (C), long (D).

**3.** $26<26.25$, which is below 35%, so the subject is **NG**. The minimum external mark is 26.25 out of 75.

**4.** $180\div75=2.4$ minutes per mark; a 4-mark question gets about $4\times2.4=9.6\approx10$ minutes.

**5.** Algebra (15) and Arithmetic, Mensuration or Geometry (13 each) give $15+13=28$, so Algebra with any one of those three.
:::
