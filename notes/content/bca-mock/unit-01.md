---
subject: Model Papers and Mock Tests
grade: BCA
unit: 1
title: The BCA Entrance Examination: Pattern, Syllabus, Strategy and the Programme
hours: 0
area: The Examination
---

The BCA entrance examination is how Tribhuvan University's Faculty of Humanities and Social Sciences (FOHSS) selects students for the four-year Bachelor in Computer Application at its affiliated colleges. This chapter says what the paper is, what each part carries, how to plan twelve weeks and two hours, and what the degree teaches afterwards. Read it once, then use the three model papers in this book as timed tests.

::: key What the paper asks, in one view
- **100 multiple-choice questions, 100 marks, 2 hours.** English grammar 40, Mathematics 50, General Knowledge and IT 10.
- **Layout in the Dean's Office model papers**: Group A English (Q1–40), Group B Mathematics (Q41–90), Group C General Knowledge and IT (Q91–100).
- **One mark each; no negative marking is reported** by the sources we found, so *never leave a question blank*. Confirm this in the notice of your year. **Pass mark:** sources disagree (35 on some sites, 40 on others) and TU's page lists none, so treat it as unconfirmed. In practice seats go by merit rank, so aim far above either figure.
- **Mathematics is half the paper**: arithmetic, algebra, calculus, coordinate geometry, trigonometry, vectors and reasoning.
:::

## 1.1 Who sits the paper, eligibility and how admission works

- **Conducting body**: Tribhuvan University, Faculty of Humanities and Social Sciences, Office of the Dean, through the portal `entrance.tufohss.edu.np`. Applications open once a year, usually in Shrawan–Bhadra; the 2082 batch paid Rs 1,500 and the 2083 notice gave an exam date in mid-August 2026. Fees and dates change: always read the current notice.
- **Eligibility** (as published by the faculty and repeated by college sites): +2 / PCL or equivalent in **any stream**. For students who passed grade 12 in **2079 BS or later**: at least a **D** grade in each subject of grades 11 and 12 and a **CGPA of 1.8 or more** (or second division marks). For those who passed *before* 2079 BS the older rule applies: D+ in each subject and CGPA 2.0. Students awaiting the grade 12 result may apply, but must show the completion certificate at the time of entrance. Mathematics in +2 is *not* compulsory.
- **Admission**: candidates are ranked by entrance score and choose from TU-affiliated colleges that run BCA; each college has a limited number of seats (often about 35–48 per section), so the merit position matters more than the pass mark.

## 1.2 The paper: layout, 100 questions, 2 hours

| Group | Subject | Questions | What is tested |
|---|---|---|---|
| A | English | 40 | grammar, vocabulary, idioms, a reading passage (4–5 questions) |
| B | Mathematics | 50 | calculus 6–8, coordinate 5–8, trigonometry 2–5, vectors 1–2, algebra 8–10, arithmetic 8–10, reasoning 7–10 |
| C | General Knowledge and IT | 10 | about 5 GK, about 5 computer/IT |

The Dean's Office model for 2018 follows exactly this layout: Q1–40 English (ending with a genetics passage), Q41–90 Mathematics (number properties, equations, matrices, series, a figure-counting question, $\cos0^\circ$), Q91–100 GK/IT (the date of the constitution, "Father of Computer", the Nobel Prizes, SSD, the FIFA World Cup, an output device, the scientific name of humans, the deepest river of Nepal, the first prime minister, the author of *Basain*).

```photogrid label="1.1" cols="3" ratio="1.0" caption="Three things the paper tests. (a) A candidate marking a bubble-style answer sheet with a pencil: every question is multiple choice, so clear marks and no blank answers matter (Fig 1.3). (b) The main building of Tribhuvan University, Kirtipur, whose Faculty of Humanities and Social Sciences runs the BCA entrance. (c) A vintage stopwatch: 100 questions in 120 minutes means every group has a time budget (Fig 1.1)."
@ photo id="bcamodel/exam" cap="(a) answer sheet: mark every item"
focus 0.55 0.4
@ photo id="bcamodel/tu" cap="(b) TU, Kirtipur"
focus 0.5 0.6
@ photo id="bcamodel/stopwatch" cap="(c) the clock decides"
focus 0.75 0.4
```

```svgfig label="1.1" caption="The paper in one picture. Top: the 100 marks (English 40, Mathematics 50, General Knowledge and IT 10). Middle: the 120-minute time plan from the text (English 30, GK and IT 5, Mathematics 70, checking 15). Bottom: the seconds per question that this plan gives, which the cell computes: English 45 s, Mathematics 84 s, GK and IT 30 s. Mathematics is half the marks and more than half the time, so it is the group that decides the rank."
G = [("English", 40, 30), ("Mathematics", 50, 70), ("GK and IT", 10, 5)]
assert sum(g[1] for g in G) == 100 and sum(g[2] for g in G) + 15 == 120
sec = {g[0]: g[2] * 60 / g[1] for g in G}
assert sec["English"] == 45 and sec["Mathematics"] == 84 and sec["GK and IT"] == 30
f = Fig(780, 314)
cols = {"English": (NAVY, BLUE), "Mathematics": (TEAL, MINT), "GK and IT": (AMBER, SAND)}
f.text(14, 14, "Marks (100)", size=11.5, color=NAVY, bold=True, anchor="start")
x = 14
for n, q, m in G:
    w = q * 7.52
    f.box(x, 24, w - 3, 40, ("GK+IT  10" if n == "GK and IT" else "%s  %d" % (n, q)), fill=cols[n][0], stroke=cols[n][0], color="#ffffff", size=11, bold=True)
    x += w
f.text(14, 90, "Minutes (120)", size=11.5, color=NAVY, bold=True, anchor="start")
x = 14
for n, q, m in [("English", 40, 30), ("Mathematics", 50, 70), ("GK", 10, 5), ("check", 0, 15)]:
    w = m * 6.27
    c = cols.get(n if n != "GK" else "GK and IT", (SLATE, SOFT))
    f.box(x, 100, w - 3, 40, ("5" if n == "GK" else "%s  %d" % (n, m)), fill=c[0], stroke=c[0], color="#ffffff", size=10.5, bold=True)
    x += w
f.text(14, 168, "Seconds per question", size=11.5, color=NAVY, bold=True, anchor="start")
for i, (n, q, m) in enumerate(G):
    y = 182 + i * 36
    f.box(14, y, 110, 28, n, fill=cols[n][1], stroke=cols[n][0], color=cols[n][0], size=11, bold=True)
    w = sec[n] * 6
    f.box(130, y, w, 28, "%d s" % sec[n], fill=cols[n][0], stroke=cols[n][0], color="#ffffff", size=11, bold=True)
f.text(14, 304, "Skip a question that costs more than twice its budget, mark it, and come back in the 15-minute check.", size=10.5, color=SLATE, anchor="start")
```

## 1.3 A 12-week plan and a 120-minute time plan

| Weeks | Focus |
|---|---|
| 1–2 | Mathematics: arithmetic (units 1–2) and algebra (units 3–4); English vocabulary and prepositions (units 1–2) |
| 3–4 | Sequences, matrices, counting (units 5–7); articles, tenses, voice (units 3–4) |
| 5–6 | Trigonometry, straight line, circle and conics (units 8–10); clauses and pronouns (units 5–6) |
| 7–8 | Vectors, calculus (units 11–13); reasoning (units 14–15); reading passages (unit 7) |
| 9 | General knowledge and IT (all four GK units); revise formula sheets |
| 10–12 | Three model papers under exam conditions, then fix every wrong answer in an error log |

**Time plan for 120 minutes**: English 30 min (it is quick if you know the rules), General Knowledge and IT 5 min, Mathematics 70 min (84 seconds a question), 15 min to check. With no negative marking, answer everything: eliminate two options and guess.

::: tip The error log
After every paper write each wrong question, the reason (formula, arithmetic slip, grammar rule, never learnt) and the page of this book that fixes it. Two weeks of this beats two more months of fresh questions.
:::

```svgfig label="1.2" caption="The 12-week plan from the table, drawn on a 12-week axis. The cell reads the six bands and checks that they cover weeks 1 to 12 exactly once with no gap: 2 + 2 + 2 + 2 + 1 + 3 = 12. Weeks 1 to 8 are for learning units, week 9 for GK and IT, and the last three weeks are for timed papers and the error log."
bands = [(1, 2, "Mathematics: arithmetic, algebra\nEnglish: vocabulary, prepositions", TEAL),
         (3, 4, "Sequences, matrices, counting\nArticles, tenses, voice", TEAL),
         (5, 6, "Trigonometry, line, circle, conics\nClauses and pronouns", TEAL),
         (7, 8, "Vectors, calculus, reasoning\nReading passages", TEAL),
         (9, 9, "GK and IT\nformula sheets", AMBER),
         (10, 12, "Three timed model papers\nthen fix the error log", RED)]
cover = [w for a, b, _, _ in bands for w in range(a, b + 1)]
assert cover == list(range(1, 13)) and sum(b - a + 1 for a, b, _, _ in bands) == 12
f = Fig(780, 330)
X0, W = 14, 62
for w in range(1, 13):
    f.box(X0 + (w - 1) * W, 6, W - 3, 22, "W%d" % w, fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
for i, (a, b, t, c) in enumerate(bands):
    y = 36 + i * 48
    f.box(X0 + (a - 1) * W, y, (b - a + 1) * W - 3, 42, "", fill=c, stroke=c)
    if a >= 10:
        f.text(X0 + (a - 1) * W - 8, y + 21, t, size=10.5, color=c, anchor="end", bold=True, vmid=True)
    else:
        f.text(X0 + b * W + 8, y + 21, t, size=10.5, color=c, anchor="start", bold=True, vmid=True)
f.text(14, 326, "Never skip the last block: timed papers teach pace, and the error log turns mistakes into marks.", size=10.5, color=SLATE, anchor="start")
```

## 1.4 What the BCA programme teaches after admission

BCA is a four-year, eight-semester programme under TU FOHSS, taught in English. The 2074 curriculum (batches up to 2081) carries 126 credit hours; a **revised curriculum applies from the 2082 batch**. The list below is compiled from college and education-portal summaries of the TU syllabus (not from the TU PDF itself), so check your college for the exact list.

| Semester | Revised curriculum (2082 batch onwards) |
|---|---|
| I | Computer Fundamentals and Applications; Programming in C; Digital Logic; Mathematics I; Professional Communication and Ethics; Hardware Workshop |
| II | Discrete Structure; Microprocessor and Computer Architecture; OOP in Java; Mathematics II; UX/UI Design; Principles of Management |
| III | Data Structure and Algorithms; Database Management System; Web Technology I; System Analysis and Design; Probability and Statistics; Applied Economics |
| IV | Operating Systems; Software Engineering; Numerical Methods; Python Programming; Web Technology II; Project I |
| V | Computer Network; Artificial Intelligence; Advanced Java Programming; MIS and e-Business; Society and Technology; Project II |
| VI | Computer Graphics and Animation; Mobile Programming; Cryptography and Network Security; Technical Writing; Distributed System; Project III |
| VII | Cyber Security and Ethical Hacking; Software Project Management; Financial Accounting; Project IV; two electives |
| VIII | Cloud Computing; Internship; two electives |

Under the eight-semester BCA structure, assessment in each course is 60 % semester-end examination and 40 % internal evaluation. Mathematics I and II, Discrete Structure, Probability and Statistics, and Numerical Methods build directly on the algebra, sequences, matrices, combinatorics, and calculus tested in the entrance examination.

```svgfig label="1.3" caption="Should you guess? With no negative marking, a blank scores 0 and a guess among k remaining options has expected value 1/k. For a candidate who knows 60 questions for sure and guesses the remaining 40: blind guesses (4 options) add 10 marks, guesses after removing one option add 13.3, and guesses after removing two options add 20."
import random
K, U = 60, 40
exp = {n: K + U / n for n in (4, 3, 2)}
assert exp[4] == 70 and abs(exp[3] - 73.33) < 0.01 and exp[2] == 80
rnd = random.Random(7)
sim = {n: sum(K + sum(rnd.random() < 1 / n for _ in range(U)) for _ in range(20000)) / 20000 for n in (4, 3, 2)}
assert all(abs(sim[n] - exp[n]) < 0.2 for n in sim), sim
f = Fig(780, 300)
f.text(14, 14, "Expected score: 60 known + 40 unknown questions", size=11.5, color=NAVY, bold=True, anchor="start")
rows = [("leave blank", 60, SLATE), ("guess blind (4 options)", exp[4], AMBER), ("remove 1 option (3 left)", exp[3], TEAL), ("remove 2 options (2 left)", exp[2], NAVY)]
for i, (lab, v, c) in enumerate(rows):
    y = 30 + i * 52
    f.box(14, y, 190, 40, lab, fill=SOFT, stroke=c, color=c, size=11, bold=True)
    f.box(208, y, v * 5.4, 40, "%.1f" % v if v != int(v) else "%d" % v, fill=c, stroke=c, color="#ffffff", size=12, bold=True)
f.line(208 + 100 * 5.4, 26, 208 + 100 * 5.4, 238, color=RED, dash=True)
f.text(208 + 100 * 5.4 - 4, 252, "100", size=10.5, color=RED, anchor="end")
f.text(14, 276, "Every removed option is worth marks. If the notice announces negative marking, guess only after you can remove two options.", size=10.5, color=SLATE, anchor="start")
```

```svgfig label="1.4" caption="The eight semesters of the revised BCA curriculum, with the mathematics-related subjects marked in amber. The cell counts the subjects from the semester table (six in each of semesters I to VII and four in semester VIII, including electives, 46 in all) and finds the five mathematics-related ones: Mathematics I, Discrete Structure, Mathematics II, Probability and Statistics and Numerical Methods. Entrance mathematics is therefore the first step of a thread that runs through the first four semesters."
sem = {"I": 6, "II": 6, "III": 6, "IV": 6, "V": 6, "VI": 6, "VII": 6, "VIII": 4}
maths = {"I": ["Mathematics I"], "II": ["Discrete Structure", "Mathematics II"], "III": ["Probability and Statistics"],
         "IV": ["Numerical Methods"], "V": [], "VI": [], "VII": [], "VIII": []}
assert sum(sem.values()) == 46 and sum(len(v) for v in maths.values()) == 5
f = Fig(780, 330)
for i, (s, n) in enumerate(sem.items()):
    y = 8 + i * 39
    f.box(14, y, 70, 32, "Sem " + s, fill=NAVY, stroke=NAVY, color="#ffffff", size=11, bold=True)
    m = len(maths[s])
    f.box(88, y, (n - m) * 40 - 3, 32, "%d other subjects" % (n - m) if m else "%d subjects" % n, fill=BLUE, stroke=NAVY, color=NAVY, size=10.5)
    if m:
        f.box(88 + (n - m) * 40, y, m * 40 - 3, 32, "%d" % m, fill=SAND, stroke=AMBER, color=AMBER, size=11, bold=True, sw=2)
    f.text(340, y + 16, ", ".join(maths[s]) if m else "", size=11, color=AMBER, anchor="start", bold=True, vmid=True)
f.text(340, 322, "amber = mathematics-related subject", size=10.5, color=AMBER, anchor="start")
```

## 1.5 How to use the books

1. Study each Mathematics unit, then do Sets A–C without notes, then read the explanations of every miss.
2. Do the English units in order; the grammar units build on each other.
3. Revise the GK units from the dated tables; refresh current affairs in the month before the exam.
4. Take the model papers on paper, with a timer, in one sitting.

## 1.6 Eight traps in preparing for the paper

Each trap is a habit that costs rank positions; the numbers come from the figures above.

1. **Treating Mathematics as one subject among three.** It carries 50 of the 100 marks and needs 70 of the 120 minutes (Fig 1.1). Start the plan with it and keep it in every week.
2. **Spending equal time on every question.** The budget is 84 seconds for a mathematics question and 45 seconds for an English one (Fig 1.1). A question that takes twice its budget should be marked and left for the final 15 minutes.
3. **Leaving answers blank.** If no negative marking applies, a blank is a lost chance: blind guessing earns 10 of 40 and guessing after removing two options earns 20 (Fig 1.3). Confirm the rule in your year's notice.
4. **Trusting an unverified pass mark.** Sources disagree on 35 or 40, and the TU page lists none. Seats go by merit rank, so plan for a score far above any quoted figure.
5. **Skipping the last three weeks.** Weeks 10 to 12 hold the timed papers and the error log (Fig 1.2). Students who finish learning at week 12 never train their pace.
6. **Doing papers without a timer.** A paper taken in pieces tells you nothing about the 120-minute limit. Sit each model paper in one go, on paper, with a stopwatch on the desk (Plate 1.1).
7. **Not logging the reason for a miss.** Write each wrong question with the cause (formula, slip, rule, never learnt) and the page that fixes it. The same reasons repeat, and that is where the marks are.
8. **Forgetting what comes after the entrance.** The first four semesters contain five mathematics-related subjects (Fig 1.4). Solid mathematics now makes the first year easier.

### 1.6.1 Worked checks

**Q. A mathematics question gets 70 minutes for 50 questions. How many seconds per question?**

**Answer.** 70 × 60 = 4200 seconds, and 4200 ÷ 50 = **84 seconds** (Fig 1.1).

**Q. A candidate knows 60 answers and guesses the other 40 blindly with 4 options each. What is the expected score?**

**Answer.** Each blind guess is right with probability 1/4, so 40 × 1/4 = 10 and the expected score is 60 + 10 = **70** (Fig 1.3).

**Q. The same candidate removes two wrong options before guessing. What is the expected score now?**

**Answer.** Two options remain, so each guess is right with probability 1/2: 40 × 1/2 = 20 and the expected score is 60 + 20 = **80** (Fig 1.3).

**Q. How many weeks of the plan are for timed papers and the error log?**

**Answer.** Weeks 10 to 12, which is **3 weeks** (Fig 1.2).

## Chapter summary

- 100 questions in 2 hours: English 40, Mathematics 50, GK and IT 10.
- Any +2 stream with the required grades can apply; apply through the TU FOHSS entrance portal.
- No negative marking is reported: answer every question.
- Mathematics is half the paper; start preparing it first.
- Use the model papers as timed tests and keep an error log.
