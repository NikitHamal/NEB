---
subject: Project IV
grade: BCA Semester 7
unit: 5
title: Final Defence: Report, Poster, Demo, Viva and Reflection
area: BCA 404 · Project IV · Unit 5
---

You have a problem, clean data, an honestly tested model and a monitored service. Now it must be **shown** to people who have fifteen minutes and an examiner's duty to be sceptical. The final defence is partly a performance, but mostly it is the moment when your preparation is checked with questions. This unit gives you the report map, the poster and slide rules, a timed demo plan, an originality check, twelve viva questions with model answers, an illustrative scoring rubric and a reflection that turns the project into a career story.

::: key What this unit gives you
- A **report map** for a 70-page capstone with a page budget that favours data, evaluation and ethics.
- A poster-and-slide plate and an **8-minute talk** with a 7-minute question slot, timed in code.
- An **originality check** you can run yourself, and an honest rule for using AI assistants.
- Twelve viva questions with model answers, an illustrative rubric, and a reflection template.
:::

## 5.1 The report map

TU does not publish a report template for Project IV; **always follow your college's format first**. The map below is a safe default for a data project, with a page budget. Notice that the data, evaluation and ethics chapters take about 43 percent of the pages. That is deliberate: they are where examiners look for honesty.

```python
chapters = [("Abstract and introduction", 6), ("Literature and related tools", 6), ("Problem, objectives, scope", 5),
            ("Data: sheet, cleaning, features", 10), ("Model and evaluation", 14), ("Fairness, privacy, ethics", 6),
            ("Service, tests, monitoring", 9), ("Results, limits, future work", 6), ("References and appendices", 8)]
total = sum(p for _, p in chapters)
print(f"total pages {total}")
for nm, p in chapters:
    print(f"  {nm:34s} {p:2d} pp  {p/total:5.1%}")
core = sum(p for nm, p in chapters if nm.startswith(("Data", "Model", "Fairness")))
print(f"data + evaluation + ethics chapters: {core} pp = {core/total:.1%} (target at least 40%)")
```
```output
total pages 70
  Abstract and introduction           6 pp   8.6%
  Literature and related tools        6 pp   8.6%
  Problem, objectives, scope          5 pp   7.1%
  Data: sheet, cleaning, features    10 pp  14.3%
  Model and evaluation               14 pp  20.0%
  Fairness, privacy, ethics           6 pp   8.6%
  Service, tests, monitoring          9 pp  12.9%
  Results, limits, future work        6 pp   8.6%
  References and appendices           8 pp  11.4%
data + evaluation + ethics chapters: 30 pp = 42.9% (target at least 40%)
```

*Reading the output.* The map totals 70 pages. The model and evaluation chapter is the longest (14 pages, 20 percent), followed by data (10 pages). Together with fairness, privacy and ethics (6 pages) they make **30 pages, 42.9 percent**, above the 40 percent target. Use the budget as a **check**, not a rule: if your evaluation chapter is only three pages, the panel will ask what you left out.

```svgfig label="5.1" caption="Report map for Project IV, drawn to the page budget. Block widths are proportional to pages. The three highlighted chapters (data, model and evaluation, fairness and ethics) carry the weight of the project."
f = Fig(580, 200)
items = [("Intro", 6, BLUE, NAVY), ("Related", 6, BLUE, NAVY), ("Problem", 5, BLUE, NAVY), ("Data", 10, "#bbf7d0", TEAL), ("Model and evaluation", 14, "#bbf7d0", TEAL), ("Ethics", 6, "#bbf7d0", TEAL), ("Service", 9, SOFT, AMBER), ("Results", 6, BLUE, NAVY), ("Refs", 8, SOFT, SLATE)]
x = 10; scale = 560 / 70
for nm, p, fl, st in items:
    wdt = p * scale
    f.box(x, 50, wdt - 2, 70, "", fill=fl, stroke=st)
    f.text(x + wdt / 2 - 1, 85, nm if p > 7 else nm[:7], size=9.5 if p > 7 else 8.5, color=NAVY, bold=p > 7)
    f.text(x + wdt / 2 - 1, 138, f"{p}", size=10, color=NAVY)
    x += wdt
f.text(290, 30, "70-page report, one block per chapter (page counts below)", size=11, color=NAVY, bold=True)
f.box(10, 160, 12, 12, "", fill="#bbf7d0", stroke=TEAL); f.text(28, 166, "data, evaluation, ethics: 30 pp (42.9%)", size=10, color=NAVY, anchor="start", vmid=True)
f.box(300, 160, 12, 12, "", fill=SOFT, stroke=AMBER); f.text(318, 166, "engineering: service, tests, monitoring", size=10, color=NAVY, anchor="start", vmid=True)
```

## 5.2 The poster and the slides

Many colleges hold a poster session before or with the defence. A poster is read from two metres by someone who has thirty seconds. Slides are read from the back of the room. The rules are the same: **few words, large numbers, one idea per block, a picture for every claim**.

```photogrid label="5.1" cols="2" ratio="1.1" caption="Showing the project. (a) A presenter at a poster session: the poster is a prop for a conversation, so the speaker faces the visitor, not the board. (b) A clean results slide for SikshyaSignal: one claim in the title, the numbers that prove it, and the baseline next to the model. Compare with a slide that lists ten bullet points."
@ photo id="bca256/poster" cap="Poster-session presenter"
fit 1.1
focus 0.5 0.5
call 0.5 0.85 0.5 0.65 "face the visitor"
@ svg cap="A clean results slide"
f = Fig(300, 270)
f.box(8, 8, 284, 254, "", fill="#ffffff", stroke=NAVY)
f.text(150, 32, "The model finds more failing students", size=11.5, color=NAVY, bold=True)
f.text(150, 48, "than the attendance rule", size=11.5, color=NAVY, bold=True)
f.box(24, 70, 120, 90, "Rule\nrecall 0.46\nprecision 0.43", fill=BLUE, stroke=NAVY, size=11, color=NAVY)
f.box(156, 70, 120, 90, "Model\nrecall 0.54\nprecision 0.58", fill="#bbf7d0", stroke=TEAL, size=11, color=NAVY, bold=True)
f.text(150, 185, "test set: 121 students, 28 fail", size=10, color=SLATE)
f.text(150, 205, "AUC 0.79 (5-fold mean 0.83)", size=10.5, color=NAVY)
f.text(150, 245, "Limit: still misses 13 of 28", size=10.5, color=RED, bold=True)
```

A good slide has a **claim** as its title ("The model finds more failing students than the attendance rule"), not a label ("Results"). The numbers come straight from the evaluation chapter, and the slide admits a limit. Put the confusion matrix, the fairness table and the drift chart in a spare **back-up section** of slides, which you do not show unless a question needs them. Looking ready for the hard question is the best impression you can make.

## 5.3 The eight-minute talk and the demo

Panels usually allow about ten to fifteen minutes. Plan a talk that ends **before** the time limit, so that the questions get their share.

```python
plan = [("Problem and who it helps", 1.0), ("Data and the cleaning rules", 1.0), ("Model, baselines, test result", 2.0),
        ("Fairness and privacy", 1.0), ("Live demo of the service", 2.0), ("Limits and next steps", 1.0)]
clock = 0.0
for nm, mins in plan:
    print(f"{clock:4.1f} - {clock + mins:4.1f} min  {nm}")
    clock += mins
print(f"talk {clock:.0f} min; questions 7 min; total {clock + 7:.0f} min")
```
```output
 0.0 -  1.0 min  Problem and who it helps
 1.0 -  2.0 min  Data and the cleaning rules
 2.0 -  4.0 min  Model, baselines, test result
 4.0 -  5.0 min  Fairness and privacy
 5.0 -  7.0 min  Live demo of the service
 7.0 -  8.0 min  Limits and next steps
talk 8 min; questions 7 min; total 15 min
```

*Reading the output.* The talk takes exactly 8 minutes and leaves 7 for questions: 15 in total. The model and results part gets 2 minutes and the live demo 2 minutes; the problem, data, fairness and limits parts get 1 minute each. The shape is deliberate: **start with the person who is helped, finish with the limits**. Rehearse with a stopwatch at least twice; most first rehearsals overrun by three minutes.

```svgfig label="5.2" caption="Timeline of the fifteen-minute defence slot, to scale. Eight minutes of talk (blue and green) and seven minutes of questions (amber). The live demo gets two minutes and has a prepared backup: a short screen recording and a saved output file."
f = Fig(580, 170)
x0 = 20; sc = 540 / 15
segs = [("Aim", 1, BLUE, NAVY), ("Data", 1, BLUE, NAVY), ("Model + test", 2, "#bbf7d0", TEAL), ("Ethics", 1, BLUE, NAVY), ("Demo", 2, "#bbf7d0", TEAL), ("Limits", 1, BLUE, NAVY), ("Questions (7 min)", 7, "#fde68a", AMBER)]
x = x0
for nm, m, fl, st in segs:
    f.box(x, 40, m * sc - 2, 50, "", fill=fl, stroke=st)
    f.text(x + m * sc / 2 - 1, 62, nm if m > 1 else nm[:6], size=9.5 if m > 1 else 8.5, color=NAVY, bold=True)
    f.text(x + m * sc / 2 - 1, 78, f"{m} min", size=9, color=NAVY)
    x += m * sc
for t in (0, 8, 15):
    f.line(x0 + t * sc, 94, x0 + t * sc, 106, color=SLATE)
    f.text(x0 + t * sc, 120, f"{t}", size=10, color=SLATE)
f.text(300, 20, "15-minute defence slot", size=11, color=NAVY, bold=True)
f.box(180, 134, 220, 28, "Backup: recording + saved output file", fill="#fecaca", stroke=RED, size=10, color=NAVY)
```

*Demo rules.* (i) Run the demo from a **saved example**, not live typing. (ii) Have the model file, the data and the sample requests on the laptop, not on the network. (iii) Show one normal request, one flagged request and one **rejected** request, because the rejection shows your guards. (iv) If anything fails, switch to the recording without apology and move on.

## 5.4 Originality: citing, checking and using AI tools honestly

An examiner can usually tell when the project is not the student's own, because the student cannot explain it. Originality is also a matter of ethics (Unit 1 of BCA 105) and, when text or code is copied without permission, of law. The rules are simple.

- **Cite** every idea, figure, dataset and library you did not create, with a reference in your college's style.
- **Check licences** of code and data. A snippet from the internet may carry conditions (MIT, GPL, CC BY-SA).
- **Write in your own words,** and then check yourself. The script below measures overlap with the **shingle similarity**: split texts into overlapping four-word chunks and compare the sets (Jaccard index = shared ÷ total distinct).

```python
import re
def shingles(text, k=4):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {" ".join(words[i:i + k]) for i in range(len(words) - k + 1)}
def jaccard(a, b):
    A, B = shingles(a), shingles(b)
    return len(A & B) / len(A | B)
orig = "Logistic regression turns a weighted score into a probability using the sigmoid function and learns its weights by gradient descent."
copy = "Logistic regression turns a weighted score into a probability using the sigmoid function and learns its weights by gradient descent."
light = "Logistic regression converts a weighted score into a probability with the sigmoid and learns weights by gradient descent."
own = "To build a risk model we scale each feature, give it a weight, add them, squash the result between zero and one, and nudge weights to reduce the loss."
for nm, t in (("verbatim copy", copy), ("light word swaps", light), ("own words", own)):
    print(f"{nm:17s} 4-word shingle similarity {jaccard(orig, t):.2f}")
```
```output
verbatim copy     4-word shingle similarity 1.00
light word swaps  4-word shingle similarity 0.14
own words         4-word shingle similarity 0.00
```

*Reading the output.* A verbatim copy scores **1.00**, and writing in your own words scores **0.00**. But look at the middle line: a light rewording with a few swapped words scores only **0.14**, so a simple checker would barely notice it. Real tools such as Turnitin are stronger, but the lesson stays: **a low similarity score does not prove originality**. The only real protection is to understand the material well enough to explain it from memory in the viva.

*AI assistants.* If your college allows them, treat them as you would a helpful senior: they may suggest, but you must **understand, test and be able to defend** every line you submit. Record in the report which tool helped with what (for example "explaining PSI", "reviewing grammar"), never submit generated text or code you cannot explain, and never let a tool invent references or numbers. Every number in your report should come from a run you did yourself.

## 5.5 Twelve viva questions with model answers

1. **Why logistic regression and not a neural network?** With 600 rows and five numeric features a simple model is enough, trains in a moment, and its weights can be inspected. A neural network would over-fit and be harder to explain to teachers. I compared it with a rule baseline, which it beat.
2. **Why is accuracy not your main metric?** Only 23 percent of students fail, so a model that says "nobody fails" scores 76.9 percent. Recall and precision measure what the teacher cares about: finding failing students without wasting time.
3. **How did you avoid leaking the test set?** I fixed a stratified split with a seed, fitted the scaling on training rows only, chose the threshold on validation, and looked at the test set once.
4. **What is data leakage? Did you meet it?** It is using information not available at prediction time. In my experiment `remedial_attended` gave an AUC of 0.930 because remedial classes follow flagging, so I excluded it.
5. **Your model recall is only 0.54. Is that good enough?** It is better than the rule (0.46) but still misses 13 of 28 failing students, so I present it as decision support, not a replacement for teachers, and I list this in the limitations.
6. **Is your data real?** No. It is simulated with seed 404, so that no privacy is at risk and every number is reproducible. Real data would need consent, anonymisation and a fresh evaluation.
7. **How did you check fairness?** I compared recall and false-alarm rates for students inside and outside the valley using out-of-fold predictions, with a bootstrap interval (−0.196 to +0.116), and I state which groups I could not check.
8. **Why was the weight on assignment positive?** Because assignment is correlated with marks and attendance, so its leftover weight is noise. Weights of correlated features must not be read as causes.
9. **What happens when next year's students are different?** I monitor PSI on inputs daily and check AUC at the end of each term. I have a written retraining rule, and a simulated third batch showed AUC falling to 0.761.
10. **How do you protect students' privacy?** Purpose limitation, only five columns, random ids, access control, delete scores after the term, no names in logs, and a human mentor reviews every flag.
11. **What would you do with another month?** Collect two real semesters with consent, test more groups, add calibration, and run a pilot with two teachers to see whether the ranked list changes what they do.
12. **What did you learn?** That the model was the shortest part. Most of the value was in clean data, honest measurement, and thinking about the people affected.

## 5.6 An illustrative rubric

TU does not publish a marking scheme for Project IV, so the table below is an **illustration of how a panel might weigh the work**, not an official rubric. Your college's form always wins. The script adds up an example score.

```python
rubric = {"Problem and objectives": (10, 8), "Data work": (15, 12), "Model and evaluation": (25, 19),
          "Fairness, privacy, ethics": (10, 7), "Software quality and tests": (15, 12), "Report writing": (10, 8), "Demo and viva": (15, 11)}
total = 0
for nm, (mx, got) in rubric.items():
    total += got
    print(f"{nm:28s} {got:2d} / {mx:2d}")
print(f"TOTAL {total} / {sum(m for m, _ in rubric.values())}")
```
```output
Problem and objectives        8 / 10
Data work                    12 / 15
Model and evaluation         19 / 25
Fairness, privacy, ethics     7 / 10
Software quality and tests   12 / 15
Report writing                8 / 10
Demo and viva                11 / 15
TOTAL 77 / 100
```

*Reading the output.* The example project earns **77 out of 100**. It does well on data work (12 of 15) and software quality (12 of 15), and loses most points on model evaluation (19 of 25) and fairness (7 of 10), exactly the areas where students tend to be thin. Use the rubric backwards: before the defence, score your own project honestly, then spend the last week on the weakest row.

## 5.7 Eight habits for a strong defence and a useful reflection

1. **Rehearse aloud with a stopwatch.** Run the full talk twice with a friend who asks questions. Reading silently hides stumbles. The second rehearsal should end at 7 minutes 30 seconds so that nerves cannot push you over time.
2. **Open with the person.** Start with the teacher who cannot visit 600 students, not with a definition of logistic regression. The panel then understands the purpose before the technique. Close with one honest limit.
3. **Show the baseline beside every result.** A number alone means nothing. "Recall 0.54, against 0.46 for the rule" is a claim; "recall 0.54" is a number. Put the comparison on the slide itself.
4. **Prepare the hard questions.** Write the twelve viva questions in Section 5.5 on cards and answer each in under 40 seconds. Add the three questions you fear most. Practise saying "I do not know, but this is how I would find out".
5. **Control the demo.** Use a saved example, keep a backup recording and show one rejected request. Panels forgive a failed live demo much more easily than a visible panic. Always carry the code on a laptop and a pen drive.
6. **Be generous with credit.** Name your supervisor, your datasets, your libraries and anyone who reviewed your work. Honest credit raises your standing. Include a short acknowledgement in the report.
7. **Close the loop in writing.** After the defence, note every question you could not answer and every correction the panel asked for, and fix the report before final submission. Examiners often ask for changes and later check that they were made.
8. **Write a one-page reflection.** State what you built, what you would do differently, what you learned about data and about people, and what you want to learn next. It becomes the paragraph in your CV and the answer to "tell me about your final-year project" in a job interview.

## Formula and fact sheet

| Item | Fact |
|---|---|
| Report budget | about 40 percent or more on data, evaluation and ethics |
| Defence slot | 8 minutes of talk and 7 of questions (typical, check your college) |
| Slide title | a claim, not a label |
| Demo | saved example, backup recording, one rejected request |
| Shingle similarity | shared 4-word chunks ÷ all distinct chunks; low score does not prove originality |
| Rubric | illustrative only; follow the college form |
| Reflection | built, would change, learned, next |

## Chapter summary

- Follow your college's report format first; use the 70-page map as a **budget check** that favours data, evaluation and ethics.
- Posters and slides use **claims as titles, big numbers, baselines beside results**, and a limit.
- Plan an **8-minute talk** with a protected question slot and a controlled demo with a backup.
- A similarity checker cannot prove originality; **understand and cite** everything, and be open about AI assistance.
- Prepare twelve viva answers, including honest ones about limits, leakage, fairness and privacy.
- Score yourself against a rubric before the defence and write a **one-page reflection** afterwards.

## Practice

1. Why does the report map spend about 43 percent of its pages on data, evaluation and ethics?
2. Write a claim-style title for a slide that shows the model's recall of 0.54 against 0.46 for the rule.
3. Why should a demo run from a saved example and include a rejected request?
4. Compute the end time of the "Fairness and privacy" part of the talk in Section 5.3 and the length of the talk.
5. A verbatim copy scores 1.00 and a lightly reworded copy 0.14 on the shingle checker. What does this tell you about such checkers?
6. State three rules for using an AI assistant honestly in a capstone.
7. In the viva, explain in two sentences why accuracy is not the main metric.
8. In the rubric example the model and evaluation row scored 19 of 25 and fairness 7 of 10. Compute each as a percentage and say which is weaker.
9. List the four parts of the reflection.
10. A panel asks you something you do not know. Describe a good response.

::: note Answers and worked solutions
**1.** Those chapters show whether the result can be trusted and whether people are treated fairly, so examiners look there first.
**2.** "The model finds more failing students than the attendance rule" (recall 0.54 against 0.46).
**3.** A saved example avoids typing errors and network failure; a rejected request shows the input checks.
**4.** Data and cleaning end at minute 2, model and test at minute 4, so fairness and privacy end at minute 5; the whole talk is 8 minutes.
**5.** Light rewording slips past simple checkers; a low score does not prove originality, so you must understand and cite your sources.
**6.** Understand and test every line; record which tool helped with what; never submit invented references, numbers or text you cannot explain.
**7.** Only 23 percent of students fail, so doing nothing is 76.9 percent accurate with zero recall; recall and precision measure the teacher's real need.
**8.** Model 19 ÷ 25 = 76 percent; fairness 7 ÷ 10 = 70 percent; fairness is weaker.
**9.** What you built, what you would change, what you learned, what you will learn next.
**10.** Say "I do not know exactly, but here is how I would find out", give your best reasoning, and note it for correction after the defence.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). How should a student prepare for the final defence of a data-driven capstone project? Give a talk plan with timings.**

*Introduction.* The defence is a short, high-stakes conversation. Good preparation consists of a planned talk, a controlled demo, and prepared answers to the hard questions.

*Talk plan (8 minutes).*

| Minutes | Part | Content |
|---|---|---|
| 0–1 | Problem | who is helped and why now (teachers cannot visit 600 students) |
| 1–2 | Data | data sheet, cleaning rules, simulated data |
| 2–4 | Model and test | baselines, test result, confusion matrix |
| 4–5 | Fairness and privacy | group check, consent, human review |
| 5–7 | Demo | normal, flagged and rejected requests |
| 7–8 | Limits and next steps | recall 0.54, simulated data, pilot plan |

*Preparation.* (i) Rehearse twice with a stopwatch. (ii) Run the demo from a saved example with a backup recording. (iii) Put baselines beside every result. (iv) Prepare answers to the twelve viva questions. (v) Keep spare slides for the confusion matrix, fairness table and drift chart.

*Conclusion.* Seven minutes are left for questions, so the talk must end on time and honestly state its limit; panels trust students who know what their work cannot do.

**Q2 (5 marks). Discuss originality in a final-year project. Explain how similarity checking works, its limits, and how AI tools should be used responsibly.**

*Introduction.* Originality means that the ideas, text, code and data in the report are the student's own or are properly credited. It is an ethical duty and often a legal one.

*Similarity checking.* A checker splits texts into overlapping chunks of words (shingles) and compares the sets; the score is shared chunks divided by all distinct chunks. In the experiment a verbatim copy scored 1.00, an independent rewrite 0.00, and a lightly reworded copy only 0.14.

*Limits.* Because light rewording scores low, a clean report does not prove originality; and a high score can arise from proper quotations. The real test is whether the student can explain the work in the viva.

*Honest practice.* (i) Cite every source and check licences. (ii) Write from understanding, not from a copied paragraph. (iii) If AI tools are allowed, record what each was used for. (iv) Never submit text, code or numbers you cannot explain or reproduce. (v) Never accept invented references.

*Conclusion.* Credit your sources, understand your work, and be open about assistance; those three habits protect both marks and reputation.

**Q3 (10 marks). Describe how you would plan, document and defend a final-year machine-learning project, from the report to the viva. Include the report structure, evaluation evidence, ethics, demo, originality and reflection.**

*Introduction.* The final defence judges the whole project: the clarity of the problem, the honesty of the evaluation, the care for people and the student's own understanding. The SikshyaSignal project shows how to prepare each part.

*1. Report structure.* Follow the college format first. A safe default is about 70 pages across nine chapters: introduction, related work, problem and objectives, data, model and evaluation, fairness and ethics, service and monitoring, results and limits, references. Give at least 40 percent of the pages to data, evaluation and ethics (here 42.9 percent).

*2. Evaluation evidence.* Show the baselines (do nothing, attendance rule), the confusion matrix (15, 11, 13, 82), precision 0.58, recall 0.54, AUC 0.791, cross-validation (mean 0.830) and the fairness table with its bootstrap interval. State clearly that the model still misses 13 of 28 failing students.

*3. Ethics and privacy.* Include a consent notice, a data-minimisation list, access control, retention and human review. Say that the data is simulated and what would change with real data.

*4. Poster and slides.* Use claims as titles, large numbers, baselines beside results, a limit on every results slide, and back-up slides for hard questions.

*5. Demo.* Run from a saved example with a backup recording; show a normal, a flagged and a rejected request; keep the talk to eight minutes so that seven remain for questions.

*6. Originality.* Cite sources, check licences, write in your own words, record any AI assistance and be ready to explain every line. Remember that a low similarity score does not prove originality.

*7. Viva and reflection.* Prepare twelve answers (method choice, metrics, leakage, fairness, privacy, drift, limits). Afterwards, fix the corrections and write a one-page reflection: what you built, what you would change, what you learned, what is next.

| Part | Evidence |
|---|---|
| Report | chapter map with page budget |
| Evaluation | baselines, matrix, CV, group table |
| Ethics | consent, minimisation, review |
| Defence | 8-minute plan, demo, backup |
| Integrity | citations, licences, tool log |

*Conclusion.* A project prepared in this way is easy to defend because every claim has evidence and every limit has been admitted in advance. Panels reward that honesty, and the habits formed here are the same ones that employers look for in a graduate who will build systems that affect real people.
