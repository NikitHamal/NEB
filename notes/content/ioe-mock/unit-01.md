---
subject: Model Papers and Mock Tests
grade: IOE
unit: 1
title: The IOE Entrance Examination: Pattern, Weightage and Strategy
hours: 0
area: Guide
---

This chapter sets out the structure, marking scheme and section-wise strategy of the IOE B.E. / B.Arch. entrance examination.

## 1.1 What the examination is

The **Institute of Engineering (IOE), Tribhuvan University** admits students to Bachelor of Engineering (B.E.) and Bachelor of Architecture (B.Arch.) programmes through one common entrance examination. It is the gateway to the five constituent campuses (**Pulchowk, Thapathali, Purwanchal (Dharan), Paschimanchal (Pokhara), Chitwan**) and to the affiliated colleges that use the same list.

| Fact | Value (IOE B.E./B.Arch. booklet 2083 and notice 2083/84) |
|---|---|
| Mode | **Computer-based test**, answered with the mouse only (keyboard disabled) |
| Duration | **2 hours** |
| Questions | **100**, all objective (four options) |
| Full marks | **140**: Section A = 60 questions × 1 mark, Section B = 40 questions × 2 marks |
| Negative marking | **10 % of that question's marks**: −0.1 for a wrong 1-mark question, −0.2 for a wrong 2-mark question |
| Subjects and marks | **Mathematics 50, Physics 40, Chemistry 30, English 20** |
| Unanswered | No penalty — but once you click an option you can change it but **not clear it**; to leave a question blank, never click |
| Centres (2083) | ICT Centre Pulchowk; Paschimanchal (Pokhara); Purwanchal (Dharan); Thapathali |

**Section distribution:** Across the two sections (Section A: $60 \times 1 = 60$ marks; Section B: $40 \times 2 = 80$ marks), the standard distribution matching the subject totals (50 / 40 / 30 / 20 marks) is Mathematics $20 + 15$, Physics $14 + 13$, Chemistry $14 + 8$, and English $12 + 4$.

**Pass mark.** There is no fixed published pass mark; IOE sets a minimum percentage for each year and only candidates at or above it enter the merit list. Past years' qualifying scores reported by third parties are in the region of 50–55 marks of 140 (35–40 %); treat that as a *floor*, not a target. Scholarship (regular) seats and full-fee seats are ranked by entrance score.

**Eligibility** (check the current notice): a pass in 10+2 Science (Physics, Chemistry, Mathematics) or A-level or an engineering diploma, with at least 45 % of the total marks in Physics, Chemistry and Mathematics taken together in Class 11 and 12 and, for NEB candidates, at least a C grade in each of those subjects in the final grade sheet (per the 2083/84 notice; equivalents apply for A-level and diploma).

**2083 cycle (as published July 2026).** Online form at **entrance.ioe.edu.np**; examinations in Shrawan 2083 (11–14 Shrawan at Pulchowk and the other three centres, in several shifts); admit card downloaded and printed in colour; original identification document carried to the hall. *Reports in June 2026 mentioned a different format and fee in an earlier draft; the final notice and the 2083 booklet both state 100 questions, 140 marks, 10 % negative marking — always confirm the date, fee and pattern on the IOE entrance portal before applying.*

## 1.2 What it tests

The paper tests the **Grade 11–12 science syllabus at entrance depth**: IOE's own 6-page "Detail Syllabus 2083" is the legal syllabus (a copy is included in the downloads). It is short: Mathematics 7 areas, Physics 6, Chemistry 3, English 4. The model questions printed in the official booklet show the level:

- Section A (1 mark): single-step — one identity, one standard result, one substitution. *Example: the value of $k$ for which one root of $3x^2+7x+6-k=0$ is zero.*
- Section B (2 marks): two or three steps. *Example: the projection of one vector on another; the depth at which a rubber ball's volume falls by 1 %; copper deposited by 2 faradays.*
- English: concord and tense, prepositions, word stress, initial vowel sound, one comprehension passage.

## 1.3 How the marks are distributed

| Subject | Marks | Questions (1-mark + 2-mark) | Heaviest chapters |
|---|---|---|---|
| Mathematics | 50 | 20 + 15 | Algebra, Calculus, Coordinate Geometry |
| Physics | 40 | 14 + 13 | Mechanics, Electricity and Magnetism |
| Chemistry | 30 | 14 + 8 | Physical, Organic |
| English | 20 | 12 + 4 | Grammar II, Grammar I, Comprehension |

**Reading the table:** Mathematics plus Physics are **90 of 140 marks (64 %)**. A candidate strong in Maths and Physics who is *accurate* in Chemistry and English will clear the qualifying line comfortably; a rank in Pulchowk's civil / computer / electronics programmes needs a high score in all four.

```photogrid label="1.1" cols="2" ratio="1.2" caption="Where the 140 marks sit. (a) Pulchowk Campus, one of the IOE campuses that admit through this paper. (b) The mark table of this book is checked line by line: 50 marks for Mathematics, 40 for Physics, 30 for Chemistry and 20 for English, each recomputed from its 1-mark and 2-mark questions, total 140 from 100 questions. Section A gives 60 marks and Section B 80. Mathematics and Physics together carry 90 marks, which is 64.3 per cent of the paper, so accuracy in those two subjects decides the rank. The split between subjects is this book's estimate, not an IOE announcement."
@ photo id="ioemock/pulchowk" cap="Pulchowk Campus, the largest IOE campus"
fit 1.2
focus 0.5 0.5
@ svg cap="Marks by subject, recomputed from 1-mark and 2-mark counts"
S = {"Mathematics": (20, 15), "Physics": (14, 13), "Chemistry": (14, 8), "English": (12, 4)}
mk = {k: a + 2 * b for k, (a, b) in S.items()}
assert list(mk.values()) == [50, 40, 30, 20] and sum(mk.values()) == 140
nq = sum(a + b for a, b in S.values()); sa = sum(a for a, b in S.values()); sb = sum(2 * b for a, b in S.values())
assert (nq, sa, sb) == (100, 60, 80)
mp = mk["Mathematics"] + mk["Physics"]
facts = dict(m=mk["Mathematics"], p=mk["Physics"], c=mk["Chemistry"], e=mk["English"], tot=140, nq=nq, sa=sa, sb=sb, mp=mp, mpp="%.1f" % (mp / 140 * 100))
f = Fig(300, 236)
f.text(150, 14, "140 marks, 100 questions", size=10.5, color=NAVY, bold=True)
cols = [(BLUE, NAVY), (SAND, AMBER), (MINT, TEAL), (ROSE, RED)]
for i, (k, v) in enumerate(mk.items()):
    y = 26 + i * 30
    f.text(8, y + 11, k, size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
    f.box(84, y, v * 2.8, 22, "", fill=cols[i][0], stroke=cols[i][1], r=3)
    f.text(84 + v * 2.8 + 6, y + 11, "%d (%.1f%%)" % (v, v / 140 * 100), size=10.5, color=cols[i][1], bold=True, anchor="start", vmid=True)
wa = 60 / 140 * 284
f.box(8, 152, wa, 24, "A: 60 x 1 = 60", fill=BLUE, stroke=NAVY, size=10.5, bold=True, r=3)
f.box(8 + wa, 152, 284 - wa, 24, "B: 40 x 2 = 80", fill=SAND, stroke=AMBER, size=10.5, bold=True, r=3)
f.text(150, 194, "Maths + Physics = %d of 140 marks" % mp, size=10.5, color=NAVY, bold=True)
f.text(150, 210, "that is %.1f per cent of the paper" % (mp / 140 * 100), size=10.5, color=NAVY, bold=True)
f.text(150, 226, "questions: 35 + 27 + 22 + 16 = 100", size=10.5, color=SLATE)
```

## 1.4 Strategy that the negative marking dictates

Penalty is 10 % of the question's marks, so a guess among four options has a small expected cost compared with its expected gain:

- *Random guess, 1 mark:* expected value $=\tfrac{1}{4}(1)-\tfrac{3}{4}(0.1)=+0.175$.
- *Random guess, 2 marks:* $=\tfrac{1}{4}(2)-\tfrac{3}{4}(0.2)=+0.35$.
- *Eliminate two options (50 : 50):* $+0.45$ (1 mark) and $+0.9$ (2 marks).

**So on this paper you should answer every question where you can eliminate at least one option, and rarely leave blanks.** Unlike CEE (−0.25), the IOE penalty is small. (If you can eliminate nothing, a guess is still mildly positive; time is the real cost.)

**Time plan (120 min / 100 questions):**
1. **0–45 min:** Section A (60 × 1). Do English first (12 questions, 10 minutes), then Chemistry facts, then Physics and Maths one-liners. Skip anything that needs more than 90 seconds and *mark it* in the on-screen palette.
2. **45–105 min:** Section B (40 × 2). Maths first while you are fresh, then Physics numerics, then Chemistry and English.
3. **105–120 min:** return to skipped questions; use elimination; check the units of your last few numerical answers.

**Technique list**
- Substitute the options into the question (test values) when a direct solution is long — especially in algebra, trigonometry and coordinate geometry.
- Use **dimensional analysis** and **limiting cases** (set $x\to0$, $\theta=90^\circ$) to kill wrong options in physics.
- In chemistry numericals, convert to **moles** first; in physics numericals write the **formula and units** before the numbers.
- In English, read the sentence aloud in your head: concord and tense errors "sound" wrong.
- On a computer-based test there is **no rough sheet on the screen** — carry the permitted pen and paper rules from the admit card; practise mental arithmetic with $\sqrt{2}=1.414$, $\sqrt{3}=1.732$, $\pi=3.14$, $\ln2=0.693$, $g=9.8$ or 10.

```photogrid label="1.2" cols="2" ratio="1.2" caption="Why a guess is worth making. (a) Dice remind us that a guess is a chance event with a known average. (b) With a penalty of one tenth of the marks, a guess among k options has expected value p x marks - (1 - p) x 0.1 x marks with p = 1/k. For four options this is 0.175 for a 1-mark and 0.35 for a 2-mark question; after eliminating two options it is 0.45 and 0.9. A guess pays on average whenever the chance of being right exceeds 1/11 = 9.1 per cent. A seeded run of 20,000 papers answered entirely by blind guessing averages 24.6 marks with standard deviation 7.1, matching the formula 24.5; the exam rewards eliminating options, but it does not punish an educated guess."
@ photo id="ioemock/dice" cap="A guess among four options is like rolling a four-sided chance"
fit 1.2
focus 0.5 0.5
@ svg cap="Expected marks of a guess and a simulated all-guess paper"
import random, math
ev = lambda k, m: (1 / k) * m - (1 - 1 / k) * 0.1 * m
assert abs(ev(4, 1) - 0.175) < 1e-12 and abs(ev(4, 2) - 0.35) < 1e-12 and abs(ev(2, 1) - 0.45) < 1e-12 and abs(ev(2, 2) - 0.9) < 1e-12
assert abs(1 / 11 - 0.0909) < 1e-4 and abs(ev(11, 1)) < 1e-12
rnd = random.Random(2083); n = 20000; sc = []
for _ in range(n):
    t = 0.0
    for q in range(100):
        m = 1 if q < 60 else 2
        t += m if rnd.random() < 0.25 else -0.1 * m
    sc.append(t)
mean = sum(sc) / n; sd = math.sqrt(sum((x - mean) ** 2 for x in sc) / n)
th = 60 * ev(4, 1) + 40 * ev(4, 2); thsd = math.sqrt(60 * 0.226875 + 40 * 0.9075)
assert abs(th - 24.5) < 1e-9 and abs(mean - th) < 0.2 and abs(sd - thsd) < 0.2
facts = dict(a1="%.3f" % ev(4, 1), a2="%.2f" % ev(4, 2), b1="%.2f" % ev(2, 1), b2="%.1f" % ev(2, 2), be="%.1f" % (100 / 11), n="{:,}".format(n), mean="%.1f" % mean, sd="%.1f" % sd, th="%.1f" % th)
f = Fig(300, 236)
f.text(150, 14, "expected marks of one guess, by options left", size=10.5, color=NAVY, bold=True)
base = 138
for i, k in enumerate((4, 3, 2, 1)):
    x = 14 + i * 70
    for j, (m, fl, st) in enumerate(((1, MINT, TEAL), (2, SAND, AMBER))):
        h = ev(k, m) * 46
        f.box(x + j * 31, base - h, 28, h, "", fill=fl, stroke=st, r=2, sw=1.2)
        f.text(x + j * 31 + 14, base - h - 8, "%.3g" % ev(k, m), size=10.5, color=st, bold=True)
    f.text(x + 30, base + 14, "%d left" % k, size=10.5, color=SLATE, bold=True)
f.line(8, base, 292, base, color=SLATE, sw=1.4)
f.text(150, 170, "teal: 1-mark question    amber: 2-mark question", size=10.5, color=SLATE)
f.text(150, 188, "break-even chance of being right: 1/11 = 9.1%", size=10.5, color=NAVY, bold=True)
f.text(150, 206, "20,000 all-guess papers: mean %.1f, sd %.1f" % (mean, sd), size=10.5, color=TEAL, bold=True)
f.text(150, 222, "formula: 60 x 0.175 + 40 x 0.35 = %.1f" % th, size=10.5, color=SLATE)
```

```photogrid label="1.3" cols="2" ratio="1.2" caption="A time plan that adds up. (a) A stopwatch: the exam allows 120 minutes for 100 questions. (b) The plan of this chapter gives Section A 45 minutes, Section B 60 minutes and 15 minutes for returning to skipped questions, which sum to 120 minutes. That is 45 seconds for each 1-mark question and 90 seconds for each 2-mark question, so both sections run at 45 seconds per mark; over the whole paper the average is 72 seconds per question or 51.4 seconds per mark, and the gap is the 15-minute reserve. Check the clock at 45 and 105 minutes."
@ photo id="ioemock/stopwatch" cap="An analog stopwatch: 120 minutes, split in advance"
fit 1.2
focus 0.5 0.5
@ svg cap="Section timings that sum to 120 minutes"
ta, tb, tr = 45, 60, 15
assert ta + tb + tr == 120
sa = ta * 60 / 60; sb = tb * 60 / 40
assert (sa, sb) == (45, 90) and sa / 1 == sb / 2 == 45
spq = 120 * 60 / 100; spm = 120 * 60 / 140
assert spq == 72 and abs(spm - 51.43) < 0.01
facts = dict(tot=120, nq=100, ta=ta, tb=tb, tr=tr, sumt=ta + tb + tr, sa="%d" % sa, sb="%d" % sb, spm="45", spq="%d" % spq, spm2="%.1f" % spm)
f = Fig(300, 236)
f.text(150, 14, "120 minutes", size=10.5, color=NAVY, bold=True)
X = lambda m: 10 + m * 280 / 120
f.box(X(0), 28, X(45) - X(0), 28, "A", fill=BLUE, stroke=NAVY, size=11, bold=True, r=3)
f.box(X(45), 28, X(105) - X(45), 28, "B", fill=SAND, stroke=AMBER, size=11, bold=True, r=3)
f.box(X(105), 28, X(120) - X(105), 28, "R", fill=MINT, stroke=TEAL, size=11, bold=True, r=3)
for m in (0, 45, 105, 120): f.line(X(m), 58, X(m), 64, color=SLATE, sw=1.4); f.text(min(max(X(m), 14), 286), 76, "%d" % m, size=10.5, color=SLATE, bold=True)
f.text(8, 98, "A: 60 questions x 1 mark, 45 minutes", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(8, 114, "   45 s for each question = 45 s per mark", size=10.5, color=SLATE, anchor="start")
f.text(8, 134, "B: 40 questions x 2 marks, 60 minutes", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(8, 150, "   90 s for each question = 45 s per mark", size=10.5, color=SLATE, anchor="start")
f.text(8, 170, "R: 15 minutes to revisit skipped questions", size=10.5, color=TEAL, bold=True, anchor="start")
f.line(8, 182, 292, 182, color=SOFT, sw=1)
f.text(150, 198, "whole paper: 72 s per question", size=10.5, color=NAVY, bold=True)
f.text(150, 214, "or %.1f s per mark (140 marks)" % spm, size=10.5, color=NAVY, bold=True)
f.text(150, 228, "", size=10)
```

## 1.5 A 12-week plan

| Weeks | Focus | Use this book |
|---|---|---|
| 1–2 | Mathematics: sets, functions, algebra | Maths units 1–2 |
| 3–4 | Mathematics: trigonometry, coordinate geometry | units 3–4 |
| 5–6 | Mathematics: calculus, vectors, statistics and probability | units 5–7 |
| 7 | Physics: mechanics | Physics unit 1 |
| 8 | Physics: heat, optics, waves | units 2–4 |
| 9 | Physics: electricity, magnetism, modern physics | units 5–6 |
| 10 | Chemistry: physical, inorganic | units 1–2 |
| 11 | Chemistry: organic; English grammar, phonetics, comprehension | Chem unit 3, English units 1–4 |
| 12 | Full-length timed papers; error log | Model Paper 1 (and the next papers) |

Daily rhythm: 90 minutes of theory, 90 minutes of MCQs, and at the end of each week one **timed 40-question set** (60 minutes) built from the Practice questions of that week's chapters. Keep an **error log** — the *reason* you lost each mark (formula, unit, arithmetic, misread, guess) — and review it every Sunday. After 3–4 weeks the log will show you which of those five causes you actually have.

## 1.6 How to use the books

1. Read the chapter's **"What the paper asks"** box, then the theory, then the **Formula and fact sheet**.
2. Do **Set A** (recall) without looking; **Set B** (understanding) and **Set C** (application) with a clock.
3. Every question has an explanation — read it even when you were right.
4. After each subject finish a **model paper section**; after all four, take a full paper under exam conditions (120 minutes, no pauses, mouse only if you can).

## 1.7 Common mistakes

- Treating Mathematics as the only subject: Physics + Chemistry + English are 90 marks.
- Leaving English until the last week: it is 20 marks and the fastest to improve.
- Using $g=9.8$ in one question and $10$ in another without reading the stem.
- Forgetting that IOE answers come as exact forms ($\sqrt{3}/2$, $\frac{\pi}{4}$): do not convert to decimals until the end.
- Losing marks on the **negative-marking arithmetic** by changing many answers in the last minutes; change an answer only when you find a concrete error.

## 1.8 After the exam

The Entrance Examination Board publishes the list of successful candidates; constituent campuses run admission and counselling; scorecards must be downloaded within the stated period after the result. Regular (scholarship) seats follow the Government of Nepal's scholarship rules; the fee for the four-year B.E. programme for regular students in 2083/84 was reported as roughly NPR 66,000 in total and about NPR 586,000 for full-fee students — **confirm every amount on the official notice**.

## Practice questions

**Set A — Check the rules (10 questions)**

1. The IOE B.E./B.Arch. question paper consists of
   (a) 100 questions in 2 hours (b) 140 questions in 3 hours (c) 100 questions in 3 hours (d) 200 questions in 2 hours
2. The marks deducted for a wrong Section A answer are
   (a) 0.1 (b) 0.5 (c) 0.25 (d) 0.2
3. A wrong answer to a 2-mark question costs
   (a) 0.1 (b) 0.2 (c) 0.4 (d) 0.5
4. Mathematics contributes how many of the 140 marks?
   (a) 40 (b) 30 (c) 50 (d) 20
5. A candidate answers 55 Section A questions correctly and 5 wrongly, with no blanks. Her Section A score is
   (a) 55 (b) 54.5 (c) 50 (d) 54
6. The expected value of a completely blind guess on a 2-mark question is
   (a) negative (b) exactly zero (c) +0.35 of a mark (d) +0.5 of a mark
7. The average time available per question in IOE is about
   (a) 72 seconds (b) 36 seconds (c) 90 seconds (d) 2 minutes
8. In this paper's split, how many Physics questions sit in Section B?
   (a) 14 (b) 13 (c) 8 (d) 18
9. If two options can be confidently eliminated on a 1-mark question, guessing between the rest has an expected value of
   (a) 0 (b) +1 mark (c) −0.1 of a mark (d) +0.45 of a mark
10. In the IOE B.E./B.Arch. entrance paper, Section A and Section B carry
    (a) 50 marks and 90 marks (b) 60 marks and 80 marks (c) 70 marks and 70 marks (d) 40 marks and 100 marks

::: note Answers and explanations — Set A
**1.** (a) — 100 objective questions, 2 hours, computer-based, mouse only.
**2.** (a) — 10 % of a 1-mark question: one tenth of a mark.
**3.** (d) — 10 % of 2 marks, so the penalty scales with the question's weight.
**4.** (c) — Mathematics 50, Physics 40, Chemistry 30, English 20.
**5.** (b) — $55 - 0.1 \times 5 = 54.5$; a blank would have scored the same as nothing.
**6.** (c) — $\frac14(2) - \frac34(0.2) = 0.5 - 0.15 = +0.35$: a guess still beats a blank.
**7.** (a) — 7,200 seconds ÷ 100 = 72 seconds, which is why the two-pass plan exists.
**8.** (b) — Physics is 14 in Section A and 13 in Section B, 27 questions for 40 marks.
**9.** (d) — $\frac12(1) - \frac12(0.1) = +0.45$: elimination, not courage, is what pays.
**10.** (b) — Section A has 60 one-mark questions (60 marks) and Section B has 40 two-mark questions (80 marks), giving a total of 140 marks.
:::
