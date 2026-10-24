---
subject: Question Bank
grade: 8
unit: 1
title: "The Basic Level Examination: Pattern, Grid and Strategy"
hours: 0
area: How to Use This Book
---

Grade 8 closes the basic level of school education in Nepal. The examination at the end of it — the **Basic Level Examination (BLE)** — is conducted by the local level (municipality or rural municipality) under the assessment scheme of the Curriculum Development Centre, Sanothimi. It is the first public examination most students sit, and the habits formed here carry straight into Grade 9 and the SEE two years later.

This book is a drill book, not a textbook. For each of the six subjects of this series it gives three chapters: a **unit-wise objective bank** (the one-mark items), a **unit-wise subjective bank** (the two- and four-mark items) and **model question sets** written to the official grid. Every question comes with an answer, and almost every answer comes with a one-line reason, because an answer you cannot explain is an answer you will lose next time.

::: key How the 100 marks of a subject are made up
The basic level scheme splits each subject in half: **50 marks of continuous (internal) assessment** collected through the year, and **50 marks of written examination** at the end. The internal half rewards classwork, project work, practical work, participation and unit tests — marks you earn slowly and cannot earn back in a day. The written half is what this book trains.
:::

## 1.1 The written paper at a glance

| Group | Question type | Items | Marks each | Total |
|---|---|---|---|---|
| A | Very short answer (objective, fill in, true/false, match, one word) | 10 | 1 | 10 |
| B | Short answer | 10 | 2 | 20 |
| C | Long answer | 5 | 4 | 20 |
| | | **25** | | **50** |

Time allowed is **two hours** (some local levels allow 2 hours 15 minutes for the language papers — check your own admit card). The same three-group shape is used for Science, Mathematics, Social Studies, Health/Physical/Creative Arts and the two language papers, though the language papers spend part of Group B and C on reading comprehension and guided writing instead of recall.

```figure caption="How the 50 written marks are distributed across the three groups. Group A is cheap and quick; Group C is where papers are won and lost."
groups = ["Group A\n10 × 1", "Group B\n10 × 2", "Group C\n5 × 4"]
marks = [10, 20, 20]
fig, ax = plt.subplots(figsize=(4.6, 3.0))
bars = ax.bar(groups, marks, color=[SERIES[0], SERIES[1], SERIES[2]],
              width=0.55, edgecolor="white", linewidth=1.2)
for b, v in zip(bars, marks):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.5, f"{v} marks",
            ha="center", color=INK, fontsize=9.5)
ax.set_ylim(0, 24)
ax.set_ylabel("Marks", color=MUTED, fontsize=9)
ax.grid(axis="y", color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(colors=MUTED, labelsize=9)
```

## 1.2 Reading the specification grid

A **specification grid** tells you how many marks a chapter is worth and at which level of thinking it will be asked. The CDC grid uses three levels:

| Level | What it asks for | Share |
|---|---|---|
| Knowledge | Recall a fact, a name, a unit, a definition | about 30 % |
| Understanding | Explain, classify, compare, give reasons | about 45 % |
| Application / higher ability | Use the idea in a new situation, solve, judge | about 25 % |

Two consequences follow, and both are practical. First, **no chapter can be skipped**: the grid spreads marks across every unit, so four chapters left unread cost more than any single long answer can return. Second, roughly a quarter of the paper is *application* — a question you have not seen before, built from ideas you have. Memorising answers prepares you for 75 % of the paper at best.

::: caution Practice questions, not past papers
Every item in this book is an original **practice** question written to the official pattern and to the chapter sequence of the CDC textbooks. None is claimed to be a reproduction of any year's paper, and no local level's paper is quoted. Where a numerical answer depends on a constant, the question states it.
:::

## 1.3 A revision timetable that works

Ten weeks is enough if the weeks are honest. The plan below assumes about an hour a day on examination preparation, on top of classwork.

| Weeks | What to do |
|---|---|
| 1–4 | One subject chapter a day: read the notes, then do that unit's objective bank here. Mark your own answers. |
| 5–7 | Subjective banks: write full two- and four-mark answers **on paper**, timed. Writing is a skill; thinking an answer is not the same as writing it. |
| 8–9 | Model sets, one per sitting, with a clock. Mark against the answer notes, then re-read only the chapters you lost marks in. |
| 10 | Formulas, diagrams, maps, definitions and the mistakes you recorded. No new material. |

::: tip Keep an error list
After every practice set, write the questions you got wrong on one page — question, your answer, correct answer, the reason. By the tenth week that page is worth more than the whole book, because it contains your mistakes rather than everyone's.
:::

## 1.4 Answering technique, group by group

**Group A (1 mark, 10 items).** These are decided in seconds. Read the stem fully — a *not* or an *except* changes everything. Eliminate two options first, then choose. Never leave one blank: an unanswered objective item scores zero, a guess from two options scores half the time.

**Group B (2 marks, 10 items).** Two marks means **two scoring points**, not two sentences of introduction. Name the thing and give the reason; or give two differences; or state the formula and substitute. A labelled sketch counts as a point in Science and Social Studies.

**Group C (4 marks, 5 items).** Four marks almost always means four parts: a definition, an explanation, an example and an application — or in Mathematics, the formula, the substitution, the working and the answer with its unit. Spend thirty seconds listing the four points in the margin before you write, and you will not forget one.

```figure caption="Time budget for a two-hour, 50-mark paper. The five minutes at the start and the ten at the end are not wasted time — they are where careless marks are saved."
labels = ["Read the\npaper\n5 min", "Group A\n15 min", "Group B\n40 min",
          "Group C\n50 min", "Check\n10 min"]
mins = [5, 15, 40, 50, 10]
fig, ax = plt.subplots(figsize=(4.9, 2.6))
left = 0
for m, lab, col in zip(mins, labels, SERIES):
    ax.barh([0], [m], left=left, color=col, edgecolor="white", linewidth=1.2,
            height=0.5)
    ax.text(left + m / 2, 0, lab, ha="center", va="center", color="white",
            fontsize=7.6)
    left += m
ax.set_xlim(0, 120)
ax.set_ylim(-0.5, 0.5)
ax.set_xlabel("minutes", color=MUTED, fontsize=9)
ax.set_yticks([])
ax.tick_params(colors=MUTED, labelsize=8.5)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
```

## 1.5 Mistakes that cost marks every year

1. **Answering the question you expected** instead of the one printed. Underline the command word — *define, explain, differentiate, list, solve, justify* — before writing.
2. **No units.** In Science and Mathematics, a number without its unit is an incomplete answer.
3. **Unlabelled diagrams.** A drawing with no labels earns almost nothing; labels are where the marks sit.
4. **Rounding too early** in a calculation, then losing the last mark on an answer that is nearly right.
5. **Writing English words in the Nepali papers** (and the reverse). The language of the paper is the language of the answer.
6. **Leaving Group C half-finished** because Group B ran long. Watch the clock at the 60-minute mark; if Group B is not done, move on and return.
7. **Not reading the whole option list** in Group A, choosing the first option that looks right.

## 1.6 How to use the six subject parts

Each subject part has the same three chapters:

- **Objective bank** — the chapter opens with a *facts line* (what the one-mark items keep returning to), then gives the items, then a key with reasons. Use it immediately after reading a chapter, while the material is fresh.
- **Subjective bank** — two-mark and four-mark questions with **answer notes**: the scoring points, in order, not a model essay. Write your own full answer first, then compare.
- **Model sets** — complete 50-mark papers to the grid above. Sit them timed and in silence. A model set done in two hours tells you something; the same set done in pieces over a week tells you nothing.

::: note The point of a question bank
A question bank is not a shortcut around the textbook; it is a way of finding out whether you have actually learned it. The textbook tells you what is true. The question bank tells you what you can still do when the page is closed and the clock is running.
:::

## 1.7 The optional papers: Optional Mathematics and Computer Science

Many schools also teach **Optional Mathematics** and **Computer Science** in Grade 8. These are not among the six compulsory subjects of the Basic Level Examination: each school sets and marks its own paper, so the questions come from your own teachers, not from the local level. They are the first step towards Optional Mathematics and Computer Science in Grades 9 and 10, and the habits you build in them carry straight into the SEE. Computer Science also has practical work in the lab, assessed by the school, besides the written paper.

This book trains both written papers to one 50-mark pattern, the same three-group shape as the compulsory papers:

| Group | Question type | Items | Marks each | Total |
|---|---|---|---|---|
| A | Objective (multiple choice) | 10 | 1 | 10 |
| B | Short answer | 10 | 2 | 20 |
| C | Long answer | 5 | 4 | 20 |
| | | **25** | | **50** |

Time allowed is **two hours**. Split it as in section 1.4: five minutes to read the paper, about 15 minutes for Group A, 40 for Group B, 50 for Group C and the last ten for checking. If your school uses a different grid, keep the same rule of thumb: give each group time in proportion to its marks, and give a 4-mark question more than twice the time of a 2-mark one.

**Revising Optional Mathematics.** Keep one card of formulas and rules (the facts lines of chapter 20), and practise methods with a pen rather than reading them: draw the figure for every height-and-distance and transformation question, write the table for every mean, and check answers by substituting back. Chapters 20 to 22 give the objective bank, the subjective bank and two model papers.

**Revising Computer Science.** Learn definitions, differences and examples as small tables; draw the labelled diagrams (block diagram of a computer, network topologies, flowcharts); practise number-system conversions until they are quick; and write short programs on paper and trace them line by line, because the paper tests the output of a program as well as its code. Chapters 23 to 25 follow the same three-part plan.

::: tip One pattern, two subjects
Because both optional papers share the 50-mark shape of the compulsory papers, the revision timetable and the error list of section 1.3 work for them too. Add one optional-subject model paper to each of weeks 8 and 9.
:::
