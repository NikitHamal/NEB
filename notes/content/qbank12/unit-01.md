---
subject: Question Bank
grade: 12
unit: 1
title: "The NEB Grade 12 Examination: Pattern, Grid and Strategy"
hours: 0
area: How to Use This Book
---

This is the examination that decides where you study next. Grade 11 was
internal to your school; Grade 12 is a national board paper, and its result is
the gate you must pass through before an engineering, medical, management or
science entrance examination will even look at you. This chapter is not
revision. It is the map: what each paper is made of, how many minutes each mark
is worth, what a marker is actually ticking, how to use the 2,000-odd questions
in the rest of this book so that they stick, and what your result is worth once
the entrance season starts.

::: key Four numbers to hold in your head
**75** — written marks in Physics, Chemistry, Biology, Mathematics,
Compulsory English and अनिवार्य नेपाली. **50** — written marks in Computer
Science, in a 2-hour paper. **25** — the internal-assessment marks every
subject carries, awarded by your own school. **2.4** — minutes you have per
written mark, in *every* paper. Everything in this chapter follows from those
four numbers.
:::

## 1.1 The specification grid of every Grade 12 science subject

A **specification grid** (विशिष्टीकरण तालिका) is the table the Curriculum
Development Centre publishes to fix how a paper is built: how many questions,
of what type, carrying what marks, drawn from which content areas. The paper
setter is not free to ignore it. That is why a question bank works at all — the
*shape* of the paper is known a year in advance, and only the wording moves.

### 1.1.1 Written marks, internal marks and the shape of each paper

| Subject (code) | Time | Written | Group A / objective | Group B / short | Group C / long | Internal |
|---|---|---|---|---|---|---|
| Physics (1021) | 3 hr | 75 | MCQ 11 × 1 = 11 | 8 × 5 = 40 | 3 × 8 = 24 | 25 |
| Chemistry (3021) | 3 hr | 75 | MCQ 11 × 1 = 11 | 8 × 5 = 40 | 3 × 8 = 24 | 25 |
| Biology (2021) | 3 hr | 75 | MCQ 11 × 1 = 11 | 8 × 4 = 32 | 4 × 8 = 32 | 25 |
| Mathematics (0081) | 3 hr | 75 | MCQ 11 × 1 = 11 | 8 × 5 = 40 | 3 × 8 = 24 | 25 |
| Computer Science (4281) | 2 hr | 50 | MCQ 9 × 1 = 9 | 5 × 5 = 25 | 2 × 8 = 16 | 25 + 25 practical |
| Compulsory English (0041) | 3 hr | 75 | no groups — 8 questions | — | — | 25 |
| अनिवार्य नेपाली (0021) | 3 hr | 75 | no groups — 18 questions | — | — | 25 |

Three things in that table are worth a second look.

**Biology is split down the middle.** Botany carries 37 marks and Zoology 38,
in two sections answered in the same script. Its short answers are worth **4**
marks, not 5 — the only subject where that is true — and it has **four**
8-mark questions, two per section. A Biology candidate who budgets time as if
the paper were Physics will run out.

**Computer Science is a 50-mark paper inside a 100-mark subject.** The written
paper is half the subject; 25 marks come from the practical examination and 25
from internal assessment. The written paper is short, dense, and — as the past
papers in Chapters 14–16 show — extremely predictable in structure.

**English and Nepali have no Group A/B/C at all.** English is eight questions;
Nepali is eighteen. Neither has a multiple-choice group in the way the science
papers do. Chapter 20 of this book is therefore *not* an MCQ bank: it is a bank
of the short objective items the Nepali grid actually tests.

### 1.1.2 Marks distribution inside English and Nepali

These two are the papers students plan worst, because "75 marks of English"
sounds shapeless. It is not. The CDC curriculum for the compulsory subjects
fixes the split exactly.

**Compulsory English — 75 written marks**

| Skill area | Marks | Where it appears |
|---|---|---|
| Reading | 35 | Q1 unseen passage 15; Q2 short literary 5 × 2 = 10; Q3 long literary 2 × 5 = 10 |
| Writing | 25 | Q4 guided writing 7; Q5 functional writing 8; Q6 free writing 10 |
| Grammar | 10 | Q7, 10 items × 1 |
| Vocabulary | 5 | Q8, 5 items × 1 |

**अनिवार्य नेपाली — 75 written marks**

| क्षेत्र | अङ्क | क्षेत्र | अङ्क |
|---|---|---|---|
| अक्षर संरचना | ३ | पठनबोध | ८ |
| वर्णविन्यास | ३ | बुँदाटिपोट + सारांश | २+३ = ५ |
| पदवर्ग पहिचान | ३ | पाठगत बोध (उत्तरात्मक) | ८ |
| शब्दनिर्माण | ३ | पाठगत बोध (समीक्षात्मक) | ४+४ = ८ |
| कारक-विभक्ति, पदसङ्गति | ४ | स्वतन्त्र रचना (निबन्ध) | ८ |
| काल-पक्ष-भाव-वाच्य | ५ | प्रतिक्रिया लेखन | ४ |
| वाक्यान्तरण | ४ | व्यावहारिक लेखन | ४ |
| | | प्रतिवेदन-टिप्पणी | ५ |

Read that Nepali table again. **Grammar alone is 25 of the 75 marks** — अक्षर
संरचना through वाक्यान्तरण — and every one of those items is rule-governed and
completely learnable. A student who memorises nothing but grammar and the
essay, and reads no पाठ at all, still has 33 marks in reach. A student who
reads only the पाठ and skips grammar has capped themselves at 50. This is the
single most common planning error in the Nepali paper.

```figure caption="Written marks against internal marks for every Grade 12 science-stream subject. Every subject totals 100; only Computer Science splits its written paper down to 50 and pays the difference in a practical examination."
import numpy as np, matplotlib.pyplot as plt

subs   = ["Nepali", "English", "Comp. Sci.", "Maths", "Biology", "Chemistry", "Physics"]
writ   = [75, 75, 50, 75, 75, 75, 75]
prac   = [0, 0, 25, 0, 0, 0, 0]
intern = [25, 25, 25, 25, 25, 25, 25]

y = np.arange(len(subs))
fig, ax = plt.subplots(figsize=(5.1, 3.0))
h = 0.55
ax.barh(y, writ, h, color=ACCENT, label="Written paper")
ax.barh(y, prac, h, left=writ, color="#7fae56", label="Practical")
ax.barh(y, intern, h, left=np.array(writ) + np.array(prac),
        color="#d8dde3", label="Internal assessment")

for i, (w, p) in enumerate(zip(writ, prac)):
    ax.text(w / 2, i, str(w), ha="center", va="center", fontsize=7.4, color="white")
    if p:
        ax.text(w + p / 2, i, str(p), ha="center", va="center", fontsize=7.0, color="white")
    ax.text(w + p + 12.5, i, "25", ha="center", va="center", fontsize=7.0, color=MUTED)

ax.set_yticks(y); ax.set_yticklabels(subs, fontsize=7.6)
ax.set_xlim(0, 108)
ax.set_xticks([0, 25, 50, 75, 100])
ax.tick_params(axis="x", labelsize=7.2)
ax.set_xlabel("marks", fontsize=7.6, color=MUTED)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.xaxis.grid(True, color=GRID, lw=0.7)
ax.set_axisbelow(True)
ax.legend(fontsize=6.8, frameon=False, loc="lower center",
          bbox_to_anchor=(0.5, 1.01), ncol=3)
```

### 1.1.3 The time budget: every mark is worth 2.4 minutes

Divide the time by the marks and the same number falls out of both paper
lengths:

$$ \frac{180\ \text{min}}{75\ \text{marks}} = 2.4 \qquad
\frac{120\ \text{min}}{50\ \text{marks}} = 2.4 $$

So the rule is universal: **an 8-mark question deserves about 19 minutes, a
5-mark question about 12, a 4-mark question about 10, and a 1-mark MCQ about
one.** But you must also read the paper and check it, so in practice you work
slightly faster than 2.4 and bank the difference.

```figure caption="A worked time budget, phase by phase, for a 3-hour 75-mark science paper and for the 2-hour 50-mark Computer Science paper. Both budgets keep a protected checking block at the end."
import numpy as np, matplotlib.pyplot as plt

phases = ["Read the\npaper", "Group A\nMCQ", "Group B\nshort", "Group C\nlong", "Check"]
three  = [5, 12, 88, 60, 15]
two    = [4, 8, 55, 44, 9]

x = np.arange(len(phases)); w = 0.36
fig, ax = plt.subplots(figsize=(5.1, 2.8))
b1 = ax.bar(x - w/2, three, w, color=ACCENT, label="3 hr / 75 marks (science)")
b2 = ax.bar(x + w/2, two, w, color="#c9ced6", label="2 hr / 50 marks (Comp. Sci.)")
for bars in (b1, b2):
    for r in bars:
        ax.text(r.get_x() + r.get_width()/2, r.get_height() + 1.8,
                f"{int(r.get_height())}", ha="center", va="bottom",
                fontsize=7.0, color=INK)

ax.set_xticks(x); ax.set_xticklabels(phases, fontsize=6.9, linespacing=1.4)
ax.set_ylabel("minutes", fontsize=7.4, color=MUTED)
ax.set_ylim(0, 122)
ax.tick_params(axis="y", labelsize=7.0)
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.spines[["top", "right"]].set_visible(False)
ax.yaxis.grid(True, color=GRID, lw=0.7)
ax.set_axisbelow(True)
ax.legend(fontsize=6.8, frameon=False, loc="upper left")
```

::: example Worked example 1.1 — budgeting the Compulsory English paper
**Problem.** Compulsory English is 8 questions, 75 marks, 180 minutes. Q1 is a
15-mark unseen passage, Q6 a 10-mark essay of about 300 words. Build a minute
budget that leaves 20 minutes of checking time.

**Solution.**

Writing time available $= 180 - 20 = 160$ minutes for 75 marks, so

$$ \text{rate} = \frac{160}{75} \approx 2.13\ \text{min per mark} $$

Multiply each question's marks by 2.13 and round to a usable number:

| Q | Task | Marks | 2.13 × marks | Use |
|---|---|---|---|---|
| 1 | Unseen reading | 15 | 32 | **30** |
| 2 | Short literary, 5 × 2 | 10 | 21 | **20** |
| 3 | Long literary, 2 × 5 | 10 | 21 | **22** |
| 4 | Guided writing | 7 | 15 | **15** |
| 5 | Functional writing | 8 | 17 | **18** |
| 6 | Free writing / essay | 10 | 21 | **28** |
| 7 | Grammar, 10 × 1 | 10 | 21 | **12** |
| 8 | Vocabulary, 5 × 1 | 5 | 11 | **6** |
| | | **75** | | **151** |

That leaves $180 - 151 = 29$ minutes spare.

**Why the budget is deliberately uneven.** Grammar and vocabulary are 15 marks
of recall — you either know the tag or you do not, and 18 minutes is plenty for
both. The 21 minutes saved there is moved to the essay, which is 10 marks that
*cannot* be earned quickly: 300 words of planned, paragraphed argument takes
nearly half an hour. Move time from the questions that reward speed to the
questions that reward length.
:::

## 1.2 What the examiner rewards in a 4-, 5- and 8-mark answer

An NEB script is not read and given an impression mark. It is marked against a
**marking scheme** that lists the scoring points, and the marker ticks them. So
the question a candidate should ask is never "how much should I write?" but
**"how many separate ticks can this question carry, and have I given the marker
all of them?"**

::: key Marks ≈ scoring points
As a working rule, **one mark is one distinct, correct, labelled point.** A
5-mark question wants five ticks, not five paragraphs. If you cannot name five
separate things you are being asked for, you have not understood the question
yet — stop and re-read it.
:::

**The 4-mark answer (Biology short answer).** Four ticks. The usual shapes are
*definition + three features*, *four differences in a table*, or *a labelled
diagram (2) + two lines of function (2)*. A table of four rows is the safest
form because the marker can see the four points without hunting. Never write a
4-mark Biology answer as continuous prose if a table will do.

**The 5-mark answer (Physics, Chemistry, Maths, Computer Science; also the long
literary answers in English).** Five ticks, and the paper usually tells you how
they split — you will see `(1+4)`, `(2+3)` or `(5)` printed after the question.
Obey the split. For a numerical, the ticks are almost always:

1. the correct **formula or principle**, written down before any numbers;
2. correct **substitution** with consistent units;
3. the **algebra**, one step per line;
4. the **numerical answer**;
5. the **unit** and a sentence saying what the answer means.

A candidate who writes only the final number has done the hard part and earned
one mark out of five.

**The 8-mark answer (Group C).** Eight ticks is too many to find by writing
harder. Every NEB 8-mark question is therefore *already divided* — either
printed as `(a)` and `(b)`, or as a mark split like `(2+6)`, `(5+3)`, `(3+5)`.
Both the 2079 and 2080 Computer Science papers did this to every Group C
question. Your answer must show the same division. Write **(a)** and **(b)** as
headings, and inside each part give the marker the structure the verb demands:

| Command word | What the marker is ticking |
|---|---|
| Define | the exact wording, in one sentence |
| State | the fact alone — no explanation needed, and none rewarded |
| Explain / Describe | statement **plus** the reason, for each point |
| Derive | every algebraic step, labelled; the result alone earns little |
| Differentiate / Compare | a **table**, with a named basis of comparison for each row |
| Draw / Sketch | a clean labelled diagram; unlabelled diagrams score nearly nothing |
| Justify / To what extent | a position, then evidence, then a concession |

::: example Worked example 1.2 — the same 5 marks, answered two ways
**Problem.** *"A host has IP address 172.16.45.9 with mask 255.255.0.0. State
its class, network address, broadcast address and the number of usable hosts.
Also distinguish an IP address from a MAC address."* <span class="marks">[5]</span>

**A weak answer (scores 2).** *"It is class B. Hosts = 65534. IP address is
logical and MAC address is physical."*

Everything written is true. But the question named **five** things — class,
network address, broadcast address, host count, and a distinction — and two of
them were never answered. Two ticks.

**A full-mark answer (scores 5).**

1. The first octet is 172, which lies in 128–191, so the address is
   **class B**. `[1]`
2. The mask 255.255.0.0 makes the first two octets the network, so the
   **network address is 172.16.0.0**. `[1]`
3. Setting all host bits to 1 gives the **broadcast address 172.16.255.255**. `[1]`
4. There are 16 host bits, so usable hosts $= 2^{16} - 2 = 65{,}534$ (two
   addresses are reserved for network and broadcast). `[1]`
5. An IP address is a **32-bit logical** address assigned by software and
   changed when the host joins another network; a MAC address is a **48-bit
   physical** address burned into the NIC and never changed. `[1]`

**What changed.** Not the knowledge — the *accounting*. The second answer walks
the marker through five numbered ticks in the order the question asked for
them. It is also shorter to write than a page of prose.
:::

## 1.3 How to use a question bank: retrieval practice, spacing and timed papers

Most students use a question bank wrongly: they read the question, feel a flicker
of recognition, read the model answer, feel satisfied, and move on. That
produces **fluency without learning**. The research on this is unusually clear,
and it is worth knowing the actual findings rather than the slogans.

**Finding 1 — testing yourself beats re-reading, and the gap grows with time.**
Roediger and Karpicke (*Psychological Science*, 2006) had students learn prose
passages either by studying them four times, or by studying once and then
recalling them from memory three times. Tested **five minutes** later, the
re-readers were ahead: about 83% recalled against 71%. Tested **one week**
later the result reversed sharply — the re-readers had fallen to about 40%,
while the students who had practised *retrieving* held about 61%. Re-reading
feels better and performs worse. Karpicke and Roediger reported the same
pattern in *Science* in 2008 under the title "The critical importance of
retrieval for learning."

```figure caption="Roediger and Karpicke (2006), Experiment 2: proportion of a prose passage recalled after repeated study versus repeated retrieval. Re-reading wins at five minutes and loses badly at one week — which is the interval that matters for a board examination."
import numpy as np, matplotlib.pyplot as plt

conds = ["Study x4\n(re-reading)", "Study x3, test x1", "Study x1, test x3\n(retrieval)"]
five  = [83, 78, 71]
week  = [40, 56, 61]

x = np.arange(len(conds)); w = 0.36
fig, ax = plt.subplots(figsize=(5.0, 2.9))
b1 = ax.bar(x - w/2, five, w, color="#c9ced6", label="tested 5 minutes later")
b2 = ax.bar(x + w/2, week, w, color=ACCENT, label="tested 1 week later")
for bars in (b1, b2):
    for r in bars:
        ax.text(r.get_x() + r.get_width()/2, r.get_height() + 1.5,
                f"{r.get_height()}%", ha="center", va="bottom", fontsize=7.0,
                color=INK)
ax.set_xticks(x); ax.set_xticklabels(conds, fontsize=6.9, linespacing=1.4)
ax.set_ylabel("percent recalled", fontsize=7.4, color=MUTED)
ax.set_ylim(0, 100)
ax.tick_params(axis="y", labelsize=7.0)
ax.spines[["top", "right"]].set_visible(False)
ax.yaxis.grid(True, color=GRID, lw=0.7); ax.set_axisbelow(True)
ax.legend(fontsize=6.9, frameon=False, loc="upper right")
```

**Finding 2 — spreading practice out beats cramming it.** Cepeda, Pashler, Vul,
Wixted and Rohrer (*Psychological Bulletin*, 2006) meta-analysed 254 studies
covering more than 14,000 participants and found distributed practice reliably
beat massed practice. A follow-up (Cepeda and colleagues, *Psychological
Science*, 2008, 1,354 participants) found the best gap between study sessions
**grows with how long you need to remember**: roughly **10–20% of the retention
interval**. Your board examination is a few months away, so the arithmetic is
blunt — if the exam is 20 weeks off, revisit a unit every 2 to 4 weeks, not
every day and not once.

**Finding 3 — these two techniques are the ones that actually work.** Dunlosky,
Rawson, Marsh, Nathan and Willingham (*Psychological Science in the Public
Interest*, 2013) reviewed ten popular study techniques and rated only two as
**high utility**: practice testing and distributed practice. Highlighting,
re-reading and summarising were rated **low utility** — not useless, but far
weaker than students believe. This book is built around the two that won.

::: tip How to actually work through a chapter of this book
1. **Cover the answer box first.** Always. Read the question, and write a real
   answer on paper before you look. Thinking "I know this one" is not retrieval.
2. **Write it out.** Silent recognition is not what the examiner is buying.
3. **Then check, and mark yourself against the scoring points**, awarding
   yourself the tick only where you actually wrote the point.
4. **Record the misses in one list** — a single page per subject. That page,
   not the chapter, is what you revise in the last fortnight.
5. **Come back in two weeks, not tomorrow.** Redo only the questions you
   missed. Getting a question right after forgetting it is worth far more than
   getting it right again immediately.
:::

::: example Worked example 1.3 — a five-week spacing plan for one unit
**Problem.** You have 20 weeks until the board examination and 7 units of
Computer Science. Design a revision cycle for **Unit 2, Data Communication and
Networking**, using the 10–20% spacing rule.

**Solution.**

The retention interval is 20 weeks $= 140$ days. Applying the rule,

$$ \text{gap} \approx 0.10 \times 140 \ \text{to}\ 0.20 \times 140 = 14\ \text{to}\ 28\ \text{days} $$

so the unit should be revisited roughly every **two to four weeks**, four or
five times in all.

| Pass | Week | What you do | Time |
|---|---|---|---|
| 1 | 1 | Read the textbook chapter once. Then close it and attempt the whole Chapter 14 MCQ set for Unit 2 **cold**. | 60 min |
| 2 | 3 | Redo **only the MCQs you got wrong**, plus 4 short questions from Chapter 15 written in full. | 45 min |
| 3 | 7 | Whole-unit retrieval from a blank page: list the OSI layers, the topologies, the impairments, from memory. Then check. | 30 min |
| 4 | 12 | Attempt both Unit 2 long questions under a stopwatch, 19 minutes each. | 40 min |
| 5 | 18 | Read your misses page only. Attempt the predicted questions for this unit. | 25 min |

Total: **3 hours 20 minutes** spread over four months, against the three to four
solid hours a student typically spends re-reading the same unit in the last
week — for a result the research says will be substantially better retained.

Now repeat with the other six units offset by a week each, and the whole course
is on a rolling cycle with no week overloaded.
:::

**Timed past papers are a separate exercise.** Do not mix them with question
practice. From about eight weeks out, sit **one complete paper a week** under
real conditions: the real clock, no notes, no phone, no pausing, one answer
sheet, and the whole paper in one sitting. Then mark it against the scoring
points *harshly*. The purpose is not to learn content — you already have that —
it is to find out what your handwriting speed, your nerves and your time budget
actually do to you for three hours, while there is still time to fix it. The
two model sets in Chapters 16, 19 and 22 are built for exactly this.

## 1.4 The ways candidates actually lose marks

Almost none of these are about not knowing the subject.

| The mistake | What it costs | The fix |
|---|---|---|
| **Leaving a question blank** | An unattempted 8-mark Group C question is 10.7% of a 75-mark paper — more than a full grade band | Write *something* structured. A definition and a labelled diagram on a question you half-know beats a clean blank every time. |
| **Ignoring the mark split** | A `(2+6)` question answered entirely as one essay on part (a) caps you at 2 | Copy `(a)` and `(b)` as headings before you start writing. |
| **Attempting both halves of an OR** | 12–20 minutes gone, no extra marks — only the first attempt is marked | Decide in the first 60 seconds, strike out the other, never look back. |
| **No formula line in a numerical** | 1–2 marks per question, every question | Write the formula, then substitute, then solve. Three lines minimum. |
| **Missing units** | 1 mark per numerical, silently | Units on the substitution *and* on the final answer. |
| **Unlabelled diagrams** | Most of the diagram's marks | Every diagram gets a title and labelled parts. A network topology with no node labels earns almost nothing. |
| **Prose where a table was asked** | Markers cannot find your points, so they do not tick them | "Differentiate", "Compare", "Distinguish" always mean a table with a named basis per row. |
| **Ignoring the word limit** | An English essay asked at ~300 words and written in 120 cannot reach 10 | Count roughly: 10 words a line, so 300 words is about 30 lines. Plan four paragraphs. |
| **Answering the Nepali paper in English** | The answer is not marked | The whole of the नेपाली script must be in Nepali. |
| **Mis-numbering answers** | The marker marks Q11 against the Q12 scheme | Write the question number large, in the margin, before the answer. |
| **Running out of time on Group C** | The last 8-mark question gets 4 minutes | Protect your budget. If a question overruns by five minutes, leave a gap and move on; come back in the checking time. |
| **"Everything I know about the topic"** | Nothing extra — and time stolen from later questions | Five ticks, then stop. Length is not a scoring point. |

::: caution Three habits that feel productive and are not
**Re-reading your notes** is rated *low utility* by Dunlosky et al. (2013) — it
raises your confidence far more than your recall, which is exactly the wrong
direction before an examination.
**Highlighting** was rated low utility in the same review. A highlighted page
has not been retrieved from memory even once.
**Reading the model answer before attempting the question** destroys the
retrieval effect entirely. The value of this book is in the *gap* between the
question and the answer box. If you never sit in that gap, you are reading a
textbook with extra steps.
:::

## 1.5 What rides on the result: entrance examinations and admission

Here is the honest position, stated only as far as the official sources go.

**Your Grade 12 result is usually an eligibility gate, not a ranking score.**
For the two biggest technical entrances in Nepal, the merit list is built from
the entrance examination; the board result decides only whether you may sit it.

**IOE — Institute of Engineering, Tribhuvan University (BE / BArch).** The IOE
admission page states the entrance is a **computer-based test of 100
multiple-choice questions, full marks 140, duration 2 hours, with 10% negative
marking for each wrong answer**, covering mathematics, physics, chemistry and
English. Eligibility from the 10+2 Science route requires **at least grade C in
all subjects**, with Physics, Chemistry and **two papers of Mathematics (200
marks)**. That last clause matters: a science student who dropped Mathematics
is not eligible for IOE, however good the rest of the result.

**MECEE-BL — Medical Education Commission (MBBS, BDS, BSc Nursing / BSc
Midwifery, BASLP, B Perfusion Technology).** The Commission's published
syllabus gives the format precisely: **200 single-best-response MCQs with four
options, full marks 200, 3 hours, with 0.25 marks deducted for every wrong
answer**, and a qualifying mark set at the **50th percentile** (the 2082 review
replaced the earlier fixed 50% pass mark with this norm-referenced rule).
Eligibility is **10+2 Science or equivalent with Physics, Chemistry and
Biology, and 50% aggregate or GPA 2.4**. The subject weighting is fixed:

| Subject | Questions |
|---|---|
| Physics | 50 |
| Chemistry | 50 |
| Zoology | 40 |
| Botany | 40 |
| Mental Agility Test | 20 |
| **Total** | **200** |

Two details in that document are worth acting on. The paper is written to a
difficulty ratio of **50:30:20 — recall : understanding : application**, so half
the paper is straight factual recall of the Grade 11 and 12 syllabus. And the
question stem is capped at **60 words**, so these are short, dense items, not
comprehension puzzles.

**Other routes.** Tribhuvan University's Faculty of Management runs **CMAT**
for BBA / BIM / BBM / BHM, and Kathmandu University and other universities run
their own entrance tests. I was not able to reach an official page giving the
current structure of these, so this book states nothing about their format —
check `fom.tu.edu.np` and the university's own admission notice for the year
you apply, and do not trust a coaching-centre summary of them.

```figure caption="How the Grade 12 result feeds forward. The board result is an eligibility gate; the merit ranking that decides admission is built from the entrance score. Figures shown are those published by IOE and the Medical Education Commission."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(5.15, 3.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 6.6); ax.axis("off")

def box(x, y, w, h, t, fc, ec, fs=7.0, tc=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.10",
                                fc=fc, ec=ec, lw=1.1))
    ax.text(x + w/2, y + h/2, t, ha="center", va="center", fontsize=fs,
            color=tc or INK, linespacing=1.45)

box(2.60, 5.15, 4.80, 1.00,
    "NEB GRADE 12 RESULT\ngrades and GPA, all subjects", "#eef4fb", ACCENT, 7.6, INK)

ax.annotate("", xy=(5.00, 4.62), xytext=(5.00, 5.10),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1, mutation_scale=10))
ax.text(5.18, 4.86, "eligibility gate", ha="left", va="center",
        fontsize=6.6, color=MUTED)

box(0.20, 3.35, 4.45, 1.25,
    "IOE  (TU)  —  BE / BArch\ngrade C in all subjects, incl.\nPhysics, Chemistry, Maths 200 marks",
    "#ffffff", MUTED, 6.5)
box(5.35, 3.35, 4.45, 1.25,
    "MECEE-BL  —  MBBS, BDS,\nBSc Nursing and allied\n50% aggregate  or  GPA 2.4",
    "#ffffff", MUTED, 6.5)

ax.annotate("", xy=(2.42, 2.80), xytext=(2.42, 3.30),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1, mutation_scale=10))
ax.annotate("", xy=(7.57, 2.80), xytext=(7.57, 3.30),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1, mutation_scale=10))

box(0.20, 1.45, 4.45, 1.32,
    "ENTRANCE  (CBT)\n100 MCQ  ·  140 marks  ·  2 hr\n10% negative marking",
    "#f2f7f2", "#4f7a3a", 6.7)
box(5.35, 1.45, 4.45, 1.32,
    "ENTRANCE\n200 MCQ  ·  200 marks  ·  3 hr\n-0.25 per wrong  ·  50th percentile",
    "#f2f7f2", "#4f7a3a", 6.7)

ax.annotate("", xy=(4.55, 0.86), xytext=(2.42, 1.40),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2, mutation_scale=10))
ax.annotate("", xy=(5.45, 0.86), xytext=(7.57, 1.40),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2, mutation_scale=10))
box(2.60, 0.10, 4.80, 0.72,
    "MERIT RANK  →  ADMISSION", "#fdf3e8", "#b4690e", 7.6, "#8a4f08")
```

::: caution What this means for how you study this year
Because the entrance papers are **all multiple choice and all drawn from the
Grade 11 and 12 syllabus**, the objective chapters of this book (14, 17, 20)
are doing double duty: they are board revision *and* entrance preparation. But
the reverse is not true. A student who prepares only with entrance-style MCQs
will not be able to write an 8-mark Group C answer, and the board paper is what
comes first. Do both, in that order.
:::

## Chapter summary

- Every Grade 12 subject totals **100**: 75 written + 25 internal, except
  Computer Science, which is 50 written + 25 practical + 25 internal.
- Group patterns: Physics / Chemistry / Maths **11 MCQ + 8 × 5 + 3 × 8**;
  Biology **11 MCQ + 8 × 4 + 4 × 8** split across Botany 37 and Zoology 38;
  Computer Science **9 MCQ + 5 × 5 + 2 × 8** in 2 hours.
- English has no groups: 8 questions, **Reading 35, Writing 25, Grammar 10,
  Vocabulary 5**. Nepali has 18 questions, of which **25 marks are pure
  grammar**.
- Every written mark is worth about **2.4 minutes**; work at about 2.1 and bank
  the rest for checking.
- **One mark ≈ one distinct scoring point.** Answer the number of things the
  question names, in the order it names them, obeying any printed `(a)/(b)` or
  `(2+6)` split.
- Retrieval beats re-reading, and the advantage grows with delay: **61% against
  40% at one week** (Roediger & Karpicke, 2006).
- Space revision at roughly **10–20% of the time to the exam** — every 2 to 4
  weeks for a 20-week horizon (Cepeda et al., 2006, 2008).
- Practice testing and distributed practice are the only two techniques rated
  **high utility** by Dunlosky et al. (2013); highlighting and re-reading are
  rated low.
- Marks are lost to blanks, ignored mark-splits, both halves of an OR, missing
  formulae and units, unlabelled diagrams, prose instead of tables, and ignored
  word limits — not to ignorance.
- The board result is an **eligibility gate**: IOE needs grade C in all subjects
  with two Maths papers; MECEE-BL needs 50% aggregate or GPA 2.4. Admission
  rank comes from the entrance score.

::: note Sources reached for this chapter
**Examination pattern and marks:** NEB Grade 12 past papers 2079 and 2080
(subject codes 4281, 0041, 0021) and the CDC *Curriculum for Grades 11 and 12,
Compulsory Subjects, 2076*, which carries the English (Reading 35 / Writing 25
/ Grammar 10 / Vocabulary 5) and Nepali mark-allocation tables.
**IOE:** the Institute of Engineering undergraduate BE admission page,
`ioe.tu.edu.np`, read 2026-09-28.
**MECEE-BL:** Medical Education Commission, *Syllabus for Bachelor Level Common
Entrance Examination 2020*, third revision dated 28 April 2026, published at
`mec.gov.np`.
**Cognitive science:** Roediger & Karpicke, *Psychological Science* 17(3), 2006;
Karpicke & Roediger, *Science* 319, 2008; Cepeda, Pashler, Vul, Wixted & Rohrer,
*Psychological Bulletin* 132(3), 2006; Cepeda et al., *Psychological Science*
19(11), 2008; Dunlosky, Rawson, Marsh, Nathan & Willingham, *Psychological
Science in the Public Interest* 14(1), 2013.
**Not verified:** no standalone CDC specification grid for Grade 11–12
Compulsory English, Nepali or Computer Science could be reached; the grids above
are taken from the curriculum documents and from the papers themselves. The
current CMAT structure could not be verified from an official source and is
therefore not stated.
:::

## Practice questions

**Group A — Do you know your own paper? (1 mark each)**

1. In the Grade 12 Biology paper, a short-answer question carries <span class="marks">[1]</span>
   (a) 2 marks (b) 4 marks (c) 5 marks (d) 8 marks
2. How many marks does the Computer Science written paper carry? <span class="marks">[1]</span>
   (a) 40 (b) 50 (c) 75 (d) 100
3. In Compulsory English, the unseen reading passage (Q1) is worth <span class="marks">[1]</span>
   (a) 10 (b) 12 (c) 15 (d) 20
4. In अनिवार्य नेपाली, the total marks carried by grammar items (अक्षर संरचना through वाक्यान्तरण) is <span class="marks">[1]</span>
   (a) 15 (b) 20 (c) 25 (d) 30
5. Approximately how many minutes should an 8-mark Group C question receive? <span class="marks">[1]</span>
   (a) 8 (b) 12 (c) 19 (d) 30
6. In the MECEE-BL entrance examination, a wrong answer costs <span class="marks">[1]</span>
   (a) nothing (b) 0.25 marks (c) 0.5 marks (d) 1 mark
7. The IOE entrance examination carries full marks of <span class="marks">[1]</span>
   (a) 100 (b) 120 (c) 140 (d) 200
8. Which pair of study techniques did Dunlosky et al. (2013) rate as high utility? <span class="marks">[1]</span>
   (a) highlighting and summarising (b) practice testing and distributed practice (c) re-reading and imagery (d) keyword mnemonics and rereading

::: note Answers to Group A
**1.** (b) — Biology alone uses 4-mark short answers, 8 per section.
**2.** (b) — 50 written, plus 25 practical and 25 internal.
**3.** (c) — 15 of the 35 reading marks.
**4.** (c) — 3+3+3+3+4+5+4 = 25, a third of the paper.
**5.** (c) — 8 marks × 2.4 min ≈ 19 minutes.
**6.** (b) — 0.25 deducted per wrong response, per the MEC syllabus.
**7.** (c) — 100 questions, 140 marks, 2 hours.
**8.** (b) — the only two of the ten reviewed techniques rated high utility.
:::

**Group B — Plan your own examination (5 marks each)**

1. Write out the full question-by-question time budget you will use for your
   Physics paper, in minutes, and show that it sums to 180 with at least 15
   minutes of checking time left. <span class="marks">[5]</span>
2. Take any one 8-mark question from Chapter 16 of this book. Without answering
   it, write down the eight separate scoring points you believe the marking
   scheme contains. <span class="marks">[5]</span>
3. Using the 10–20% spacing rule, build a revision calendar for **all seven**
   Computer Science units across the weeks remaining before your examination.
   State your retention interval and the gap you derived from it. <span class="marks">[5]</span>
4. List five ways you personally have lost marks in your school terminal
   examinations, and write the one-line fix for each. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** A workable budget: read 5, Group A 12, Group B 8 × 11 = 88, Group C
3 × 20 = 60, check 15. Total $5+12+88+60+15 = 180$. Note that Group C is given
20 minutes rather than the full 19.2 it is "worth", paid for by finishing the
MCQs in 12 minutes instead of 26.
**2.** A correct answer here is a *list of eight nouns*, not prose — for
example, for "Explain the OSI reference model with a diagram (5) and compare it
with TCP/IP (3)": diagram, seven layer names, function of each, one protocol
per layer, then three named bases of comparison. If you cannot reach eight,
re-read the question; you have missed a part.
**3.** With 20 weeks (140 days) the gap is 14–28 days, so 4–5 passes per unit.
Offset the seven units by one week each so that in any given week you are
touching two units, one for the first time and one on a later pass.
**4.** Model answer shape: *"I wrote the answer but not the units — put units on
the substitution line and the final line. I answered both halves of an OR —
decide in 60 seconds and cross the other out. …"* The value of this question is
that the list is yours; a generic list scores nothing.
:::

**Group C — Long answer (8 marks each)**

1. (a) Draw up the specification grid of any **three** Grade 12 science-stream
   subjects side by side, showing time, written marks, number of questions in
   each group, and marks per question. <span class="marks">[5]</span>
   (b) Explain why the same 2.4 minutes-per-mark figure applies to both the
   3-hour and the 2-hour papers, and what a candidate should do with the
   difference between 2.4 and the 2.1 recommended in this chapter. <span class="marks">[3]</span>

2. (a) Describe, with the experimental evidence, why attempting a question
   before reading its answer produces better retention than reading the answer
   first. <span class="marks">[5]</span>
   (b) A friend tells you they revise by re-reading their notes three times the
   night before. Explain what the research predicts will happen to them, and
   what you would tell them to do instead. <span class="marks">[3]</span>

::: note Answer outline to Group C
**1(a).** Any three rows of the table in §1.1.1, with the columns time / written
marks / Group A / Group B / Group C, e.g. Physics 3 hr, 75, 11 × 1, 8 × 5,
3 × 8; Biology 3 hr, 75, 11 × 1, 8 × 4, 4 × 8 across two sections; Computer
Science 2 hr, 50, 9 × 1, 5 × 5, 2 × 8. One mark per correctly completed row,
two for a correct and complete table layout.
**1(b).** Because NEB fixes the same ratio in both: $180/75 = 120/50 = 2.4$.
The difference between 2.4 and 2.1 is deliberate slack — about 22 minutes on a
3-hour paper — and it should be spent on (i) reading the paper before writing,
(ii) the questions that cannot be answered quickly, such as an essay or a
derivation, and (iii) a real checking pass at the end, in that order.
**2(a).** Retrieval strengthens the memory trace, whereas reading it only
re-exposes you to it. Roediger and Karpicke (2006) showed the crossover
directly: re-reading led at a five-minute delay (≈83% vs 71%) but lost at one
week (≈40% vs 61%). Reading the answer first feels easier precisely because it
removes the effortful retrieval that produces the learning — the effort *is*
the mechanism. Credit for naming the study, quoting the direction of the
effect, and explaining why the short-delay result misleads students.
**2(b).** The research predicts high confidence and poor retention: massed
practice and re-reading both perform well on an immediate test and poorly after
a delay, and re-reading was rated low utility by Dunlosky et al. (2013).
Advice: close the notes, attempt questions from memory, mark them against the
scoring points, and — for anything still needed in a week's time — space the
repeats two to four weeks apart rather than stacking them into one night.
:::
