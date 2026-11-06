---
subject: Project IV
grade: BCA Semester 7
unit: 1
title: From Idea to Capstone: Framing a Data Project, Scope and Ethics
area: BCA 404 · Project IV · Unit 1
---

Projects I to III asked "does the system work?". The final-year capstone asks a harder question: "**is the decision it makes good, fair and defensible?**" A model that labels a student "at risk" can change how teachers treat that student. So Project IV needs more than code. It needs a problem that is worth solving, data that is honestly collected, a result that is honestly measured, and a student who can explain every choice in front of an examiner.

::: key What this unit gives you
- The five things that change when a project moves from building systems to making decisions about people.
- A numbered problem statement, measurable objectives and a scope table for the running example, **SikshyaSignal**.
- A pipeline figure (data, features, model, service, human) and a decision chart: should this project use machine learning at all?
- Real photographs of the people, hardware and rooms behind a data project, and a first executed script that builds the dataset and shows the **accuracy trap**.
:::

## 1.1 What changes in Project IV

A capstone is judged by the same panel that will judge your career story, so it carries more weight. Five things change compared with Projects I to III.

| Concern | Project III (sensor system) | Project IV (decision system) |
|---|---|---|
| Output | a reading or an alert | a **judgement about a person** that someone may act on |
| Quality test | does it run, is the sensor accurate | precision, recall, fairness, and an honest baseline |
| Data | measured by a device | personal, sensitive, often biased, must be protected |
| Failure cost | spoiled crop | a student wrongly labelled, or a struggling student missed |
| Defence | demo and viva | demo, viva, **ethics questions** and a reproducibility check |

Because of this, the Project IV report has chapters that the earlier reports do not: a **data chapter** (where it came from, consent, cleaning), an **evaluation chapter** (with a baseline), a **fairness and privacy chapter**, and a **limitations chapter** that says plainly what the system cannot do.

## 1.2 The running example: SikshyaSignal

SikshyaSignal is invented for this book. A private college in Kathmandu has 600 first-year BCA students. Teachers learn that a student is in trouble only when the internal exam result arrives, which is too late for extra classes. About one student in four fails at least one subject.

*Problem statement, version 1.* "Roughly 23 percent of first-year students fail a subject, and the college learns this only after the internal exam, six weeks before the final. Teachers cannot visit 600 students, but they can talk to 40. A tool that ranks students by risk from attendance, assignments and internal marks could point the teachers to the right 40 early enough for two remedial weeks."

*Objectives (SMART).*

| # | Objective | How it is measured at the defence |
|---|---|---|
| O1 | A simulated dataset of 600 students is built and documented | data sheet with every column, range and source |
| O2 | The model beats the "nobody is at risk" baseline on **recall**, not only accuracy | recall on the held-out test set |
| O3 | Of the top 10 percent ranked (12 of the 121 test students), at least 60 percent really fail | precision at the top 10 percent, on the test set |
| O4 | Risk rates are checked across two student groups | group table, gap reported honestly |
| O5 | A prediction service answers in under 100 ms and passes 8 unit tests | test log, timing script |

*Scope table.*

| In scope | Out of scope (future work) |
|---|---|
| tabular data, logistic regression written with NumPy, evaluation, group check, a small JSON prediction service, drift monitor, report and viva | deep learning, real student records, automatic marks or admission decisions, mobile app, multi-college use |

Notice that **objective O2 names the metric**. "The model is accurate" can never be examined; "recall of at least 60 percent on the test set" can.

## 1.3 The pipeline and where the computing lives

Every data project, from a tiny capstone to a bank's fraud system, has the same chain of stages, and every stage can fail on its own.

1. **Data** from the real world: attendance sheets, marks, assignment logs.
2. **Features**: numbers prepared from the data, such as attendance percentage.
3. **Model**: a function that turns features into a risk score between 0 and 1.
4. **Service**: code that takes one student's features and returns the score.
5. **Human decision**: a teacher reads the ranked list and decides whom to meet.
6. **Feedback**: the end-of-term result is stored and used to check the model.

```svgfig label="1.1" caption="SikshyaSignal pipeline. Records become features, the model turns them into a risk score, a service ranks students, a teacher decides, and the final result flows back to check the model. The dashed arrow is the feedback loop that most capstones forget."
f = Fig(580, 215)
f.box(8, 70, 92, 66, "Records\nattendance,\nmarks", fill=BLUE, stroke=NAVY, size=10.5, color=NAVY)
f.box(122, 70, 92, 66, "Features\nclean, scale", fill=SOFT, stroke=TEAL, size=10.5, color=NAVY)
f.box(236, 70, 92, 66, "Model\nrisk score\n0 to 1", fill=SOFT, stroke=AMBER, size=10.5, color=NAVY)
f.box(350, 70, 92, 66, "Service\nrank top 40", fill=BLUE, stroke=RED, size=10.5, color=NAVY)
f.box(464, 70, 108, 66, "Teacher\nmeets 40\nstudents", fill=SOFT, stroke=NAVY, size=10.5, color=NAVY)
for x in (100, 214, 328, 442):
    f.arrow([(x, 103), (x + 22, 103)], color=NAVY)
f.arrow([(518, 70), (518, 30), (54, 30), (54, 70)], color=RED, dash=True)
f.text(286, 20, "feedback: final result checks the model", size=10, color=RED)
f.text(54, 160, "1 Data", size=10, color=NAVY)
f.text(168, 160, "2 Features", size=10, color=NAVY)
f.text(282, 160, "3 Model", size=10, color=NAVY)
f.text(396, 160, "4 Service", size=10, color=NAVY)
f.text(518, 160, "5 Human", size=10, color=NAVY)
f.text(290, 195, "Each arrow can fail: missing records, wrong features, over-fitted model, slow service, ignored advice.", size=9.5, color=SLATE)
```

Figure 1.1 shows why a capstone cannot be judged by the model alone. A perfect model fed by wrong attendance sheets is useless, and a perfect list that no teacher reads changes nothing. The best Project IV reports name the **failure of each arrow** and what the team did about it.

```photogrid label="1.1" cols="3" ratio="1.0" caption="The people, hardware and rooms behind a data project. (a) A secondary school building in Sankhu, Kathmandu: the attendance and marks that feed SikshyaSignal come from places like this, and each row of data is a real learner. (b) A graphics card: deep-learning projects train on such cards, but SikshyaSignal's 600 rows need only an ordinary laptop. (c) A computer-centre hall at CERN with rows of server racks: this is where large models are served; a capstone can use a free cloud tier or a college server instead."
@ photo id="bca404/students" cap="School building, Sankhu"
fit 1.0
focus 0.5 0.5
call 0.5 0.8 0.5 0.6 "learners = data rows"
@ photo id="bca404/gpu" cap="Graphics card (GPU)"
fit 1.0
focus 0.5 0.5
call 0.5 0.85 0.5 0.65 "fan and GPU chip"
@ photo id="bca404/datacenter" cap="Server racks at CERN"
fit 1.0
focus 0.5 0.5
call 0.5 0.8 0.5 0.6 "racks of servers"
```

## 1.4 Building the dataset and meeting the accuracy trap

The script below creates the 600 simulated students. Each student has a hidden "ability" that nudges attendance, internal marks, assignments and previous GPA, plus random noise; failure is then drawn from a logistic formula. Because **we wrote the simulator, we know the truth**, which is useful for learning but never true of real data. The script prints the data sheet, the failure rate and two baselines.

```python
import numpy as np
rng = np.random.default_rng(404)
n = 600
ability = rng.normal(0, 1, n)
attend = np.clip(78 + 4.5*ability + rng.normal(0, 10, n), 30, 100)
internal = np.clip(24 + 5*ability + 0.08*(attend-78) + rng.normal(0, 3.5, n), 0, 40)
assign = np.clip(80 + 6*ability + rng.normal(0, 14, n), 0, 100)
gpa = np.clip(2.9 + 0.45*ability + rng.normal(0, 0.3, n), 1.5, 4.0)
commute = rng.gamma(2.0, 20, n)
valley = rng.random(n) < 0.6
z = -2.0 - 0.05*(attend-78) - 0.18*(internal-24) - 0.01*(assign-80) - 0.8*(gpa-2.9) + 0.006*(commute-40)
risk = rng.random(n) < 1/(1+np.exp(-z))
print("n", n, "at-risk", risk.sum(), f"{risk.mean():.1%}")
for name, v in [("attendance %", attend), ("internal /40", internal), ("assignment %", assign), ("prev GPA", gpa), ("commute min", commute)]:
    print(f"{name:14s} mean {v.mean():6.2f}  sd {v.std():5.2f}  min {v.min():6.2f}  max {v.max():6.2f}")
print("valley share", f"{valley.mean():.1%}", "risk rate valley", f"{risk[valley].mean():.1%}", "outside", f"{risk[~valley].mean():.1%}")
print("baseline: predict nobody at risk -> accuracy", f"{1-risk.mean():.1%}", "recall 0%")
rule = attend < 70
tp = (rule & risk).sum(); fp = (rule & ~risk).sum(); fn = (~rule & risk).sum()
print("rule attendance<70: flagged", rule.sum(), "TP", tp, "FP", fp, "FN", fn, f"precision {tp/(tp+fp):.2f} recall {tp/(tp+fn):.2f}")
```
```output
n 600 at-risk 138 23.0%
attendance %   mean  78.11  sd 10.69  min  46.82  max 100.00
internal /40   mean  23.74  sd  6.76  min   1.43  max  40.00
assignment %   mean  79.04  sd 14.56  min  24.77  max 100.00
prev GPA       mean   2.87  sd  0.55  min   1.50  max   4.00
commute min    mean  40.48  sd 29.12  min   0.41  max 186.16
valley share 60.3% risk rate valley 22.7% outside 23.5%
baseline: predict nobody at risk -> accuracy 77.0% recall 0%
rule attendance<70: flagged 133 TP 63 FP 70 FN 75 precision 0.47 recall 0.46
```

*Reading the output.* Of 600 students, 138 (23.0 percent) fail. The lazy baseline "predict that nobody is at risk" is **77.0 percent accurate** yet finds no student at all: recall 0. This is the **accuracy trap**: when the rare class is the one you care about, accuracy rewards doing nothing. The one-line rule "attendance below 70 percent" flags 133 students and catches 63 of the 138 (recall 0.46) with precision 0.47, so more than half of the flags are false alarms and 75 failing students are missed. Any model in Unit 3 must be compared with **both** baselines, never with zero.

```svgfig label="1.2" caption="The accuracy trap, drawn from the script output. The do-nothing baseline has the tallest accuracy bar and zero recall; the attendance rule is less accurate but finds almost half of the failing students. The report must show recall and precision next to accuracy."
f = Fig(580, 215)
f.line(60, 170, 560, 170, color=SLATE)
f.line(60, 30, 60, 170, color=SLATE)
for v, y in ((0, 170), (50, 100), (100, 30)):
    f.line(56, y, 60, y, color=SLATE)
    f.text(46, y, str(v), size=9.5, color=SLATE, anchor="end", vmid=True)
f.text(20, 100, "%", size=10, color=SLATE)
def grp(x, vals, label):
    cols = [(BLUE, NAVY), (SOFT, TEAL), ("#fde68a", AMBER)]
    for i, v in enumerate(vals):
        h = v * 1.4
        f.box(x + i * 44, 170 - h, 38, h, "", fill=cols[i][0], stroke=cols[i][1])
        f.text(x + i * 44 + 19, 170 - h - 8, f"{v:g}", size=10, color=NAVY, bold=True)
    f.text(x + 66, 190, label, size=10.5, color=NAVY, bold=True)
grp(90, [77.0, 0, 0], "Do nothing")
grp(330, [75.8, 46, 47], "Attendance < 70 rule")
f.box(470, 38, 12, 12, "", fill=BLUE, stroke=NAVY); f.text(488, 44, "accuracy", size=9.5, color=NAVY, anchor="start", vmid=True)
f.box(470, 56, 12, 12, "", fill=SOFT, stroke=TEAL); f.text(488, 62, "recall", size=9.5, color=NAVY, anchor="start", vmid=True)
f.box(470, 74, 12, 12, "", fill="#fde68a", stroke=AMBER); f.text(488, 80, "precision", size=9.5, color=NAVY, anchor="start", vmid=True)
```

## 1.5 Should this project use machine learning at all?

A mature capstone does not start from "I want to use AI". It starts from the problem and asks, honestly, whether a simpler tool would do. Examiners respect a student who tried the simple rule first.

```svgfig label="1.3" caption="Decision chart for choosing the method. Start with the cheapest tool that could work: a clear rule or a spreadsheet. Use a model only when rules fail and enough labelled history exists, and always screen the idea for harm before any code is written."
f = Fig(580, 230)
f.box(10, 90, 106, 50, "Problem\nstatement", fill=BLUE, stroke=NAVY, size=10.5, color=NAVY)
f.box(150, 90, 110, 50, "Can a clear rule\nsolve it?", fill=SOFT, stroke=TEAL, size=10, color=NAVY)
f.box(150, 180, 110, 40, "Use the rule", fill=BLUE, stroke=TEAL, size=10.5, color=NAVY)
f.box(300, 90, 118, 50, "Enough labelled\nhistory?", fill=SOFT, stroke=AMBER, size=10, color=NAVY)
f.box(300, 180, 118, 40, "Collect data first", fill=BLUE, stroke=AMBER, size=10.5, color=NAVY)
f.box(458, 90, 114, 50, "Harm screen:\nconsent, bias", fill=SOFT, stroke=RED, size=10, color=NAVY)
f.box(458, 10, 114, 44, "Build model +\nhuman review", fill=BLUE, stroke=RED, size=10.5, color=NAVY)
f.arrow([(116, 115), (150, 115)], color=NAVY)
f.arrow([(260, 115), (300, 115)], color=NAVY); f.text(280, 105, "no", size=9.5, color=NAVY)
f.arrow([(205, 140), (205, 180)], color=NAVY); f.text(218, 160, "yes", size=9.5, color=NAVY)
f.arrow([(418, 115), (458, 115)], color=NAVY); f.text(438, 105, "yes", size=9.5, color=NAVY)
f.arrow([(359, 140), (359, 180)], color=NAVY); f.text(372, 160, "no", size=9.5, color=NAVY)
f.arrow([(515, 90), (515, 54)], color=NAVY); f.text(530, 74, "pass", size=9.5, color=NAVY)
```

For SikshyaSignal the chart gives: a single rule exists (attendance below 70) but it is weak (Section 1.4), enough history can be collected (previous batches), and the harm screen needs three checks: **consent** (students are told what is used), **bias** (the model must not be harsher on one group; Unit 3), and **human review** (the output is advice to a teacher, never an automatic penalty). Putting these checks in the proposal, before any code, is what separates a final-year capstone from a class exercise.

## 1.6 Eight reasons capstone data projects fail, and the cure

1. **The problem is too vague.** "Predict student performance" has no user, no decision and no deadline. Write the problem as in Section 1.2: who acts, on what, how early, and how success is counted. A sharp problem makes every later choice easier.
2. **The data was never checked.** The team trusts the spreadsheet because it opened without an error. Print the range, missing count and mean of every column, as in Section 1.4. Impossible values such as attendance above 100 are the first thing an examiner will look for.
3. **Accuracy is the only metric.** A model that predicts "nobody fails" scores 77 percent here. Always report a baseline, the confusion matrix, precision and recall, and say which matters for the decision. Unit 3 shows how.
4. **The test set was used for training.** The team tunes the model until the test score looks good, so the score no longer measures anything. Split the data once, tune on the training part only, and touch the test set a single time at the end.
5. **No thought for people.** The report never mentions consent, bias or what happens to a wrongly flagged student. Add a harm screen to the proposal, a group check to the evaluation, and a human-review step to the design. Nepal's Individual Privacy Act 2075 makes personal data a legal matter, not only an ethical one.
6. **A notebook is not a product.** The model works on the author's laptop and nowhere else. Save the model as a file, wrap it in a small service with tests, and write the run steps in the README so a stranger can reproduce the demo.
7. **Nobody plans for change.** Next year's batch behaves differently and the model slowly gets worse. Store predictions and outcomes, and compute a drift measure (Unit 4) so the college knows when to retrain.
8. **The defence is a surprise.** The student reads slides and cannot answer "why logistic regression?" or "what if the data is biased?". Prepare the twelve viva questions in Unit 5 and rehearse the demo twice, including the case where the network fails.

```photogrid label="1.6" cols="2" ratio="1.27" caption="In a dataset where only 12 per cent of students fail, accuracy is a trap. (a) The students a capstone model is meant to describe. (b) Among 1,000 students, 120 fail. A model that simply predicts that everyone passes is right for 88% of them, yet it finds none of the failing students, so its recall and precision are zero. A trained model that catches 84 of the 120 and raises 60 false alarms scores 90.4% accuracy, which looks only slightly better, but its recall is 70% and its precision is 58%. The extra metrics show the real gain. Always compare against the majority-class baseline before you report a score in the viva."
@ photo id="bcapj/sankhu-school" cap="Students at a school in Sankhu: the population a capstone model describes"
fit 1.27
focus 0.5 0.5
@ svg cap="The accuracy trap on 1000 students, 120 failing"
N, FAIL = 1000, 120
acc0 = (N - FAIL) / N * 100
TP, FN, FP = 84, FAIL - 84, 60
TN = N - FAIL - FP
acc1 = (TP + TN) / N * 100
rec1 = TP / (TP + FN) * 100
pre1 = TP / (TP + FP) * 100
assert abs(acc0 - 88.0) < 1e-9 and abs(acc1 - 90.4) < 1e-9 and abs(rec1 - 70.0) < 1e-9
f = Fig(300, 236)
f.text(150, 14, "Always predict pass", size=10.5, color=RED, bold=True)
hbars(f, [("accuracy", acc0), ("recall", 0.0), ("precision", 0.0)], vmax=100, fmt="%.0f", x0=70, y0=24, bw=190, gap=22,
      colors=[(ROSE, RED), (ROSE, RED), (ROSE, RED)], size=9.5)
f.text(150, 116, "Trained model (TP %d, FN %d, FP %d)" % (TP, FN, FP), size=10.5, color=TEAL, bold=True)
hbars(f, [("accuracy", acc1), ("recall", rec1), ("precision", pre1)], vmax=100, fmt="%.0f", x0=70, y0=126, bw=190, gap=22,
      colors=[(MINT, TEAL), (MINT, TEAL), (MINT, TEAL)], size=9.5)
f.text(150, 210, "88 percent accuracy, yet it finds no one", size=10.5, color=NAVY, bold=True)
f.text(150, 226, "report recall and precision as well", size=10, color=SLATE, bold=True)
facts = dict(a0=acc0, a1=acc1, r1=rec1, p1=pre1)
```

## Formula and fact sheet

| Item | Formula or fact |
|---|---|
| Accuracy | (TP + TN) / total |
| Precision | TP / (TP + FP): of those flagged, how many were right |
| Recall | TP / (TP + FN): of those who really fail, how many were found |
| Baseline | the score of the simplest possible rule; a model must beat it |
| SMART objective | Specific, Measurable, Achievable, Relevant, Time-bound |
| Pipeline | data, features, model, service, human decision, feedback |
| Simulated data | known truth, no privacy risk, but never proof about real students |

## Chapter summary

- A capstone is judged on the **quality of the decision** and on how honestly it is measured, not only on whether the code runs.
- Write a four-part problem statement and **measurable objectives** that name the metric.
- A data project is a pipeline of six stages; each arrow can fail, so name the failure of each.
- **Accuracy can lie.** With 23 percent failures, doing nothing is 77 percent accurate and useless.
- Try the cheapest method first and screen the idea for **consent, bias and human review** before coding.
- Keep a data sheet for every dataset and say clearly when the data is simulated.

## Practice

1. List the five concerns that change when a sensor project becomes a decision project.
2. Write a four-part problem statement for predicting which students will miss the Dashain-holiday assignment deadline.
3. Name the six stages of the pipeline in Figure 1.1 and one failure of each.
4. Why is "the model is accurate" a weak objective? Rewrite it as a measurable one.
5. In Section 1.4 the do-nothing baseline has 77.0 percent accuracy. Explain why that number is misleading.
6. Using the output TP = 63, FP = 70, FN = 75, compute the accuracy of the attendance rule on 600 students.
7. State two reasons why simulated data is useful for learning and one reason it can never replace real data.
8. What three checks make up the harm screen in Section 1.5?
9. Why must the final result be fed back to the system?
10. A model flags 50 students and 30 of them really fail; 138 students fail in total. Compute precision and recall.

::: note Answers and worked solutions
**1.** Output (a judgement about a person), quality test (precision, recall, fairness), data (personal and sensitive), failure cost (wrong label), defence (ethics questions).
**2.** Example: "Many students submit the assignment due after Dashain late or never. The class teacher learns of it only after the deadline. Using attendance and earlier submission history, a tool could list 15 students on the Monday before the deadline. Success is that at least half of the late submitters are on the list."
**3.** Data (wrong records), features (bad scaling), model (over-fitting), service (too slow), human decision (advice ignored), feedback (never collected).
**4.** It cannot be checked. Better: "recall of at least 60 percent and precision at 40 of at least 60 percent on the held-out test set".
**5.** It comes entirely from the 77 percent of students who do not fail; it finds none of the 138 who do (recall 0), so it is accurate and useless.
**6.** Errors are FP + FN = 70 + 75 = 145, so correct = 600 − 145 = 455; accuracy = 455 ÷ 600 = 75.8 percent, lower than doing nothing.
**7.** Useful: known truth for testing, and no privacy risk. Cannot replace real data because real behaviour has patterns the simulator's author never imagined.
**8.** Consent, bias check, human review.
**9.** Only the real outcome shows whether predictions were right, and drift is detected by comparing predictions with outcomes over time.
**10.** Precision = 30 ÷ 50 = 0.60; recall = 30 ÷ 138 = 0.217, about 22 percent.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the pipeline of a data-driven decision system with a diagram reference and an example.**

*Introduction.* A data-driven decision system turns raw records into advice that a person can act on. It is a chain of stages, and the quality of the final decision can be no better than the weakest stage. Figure 1.1 shows the chain for SikshyaSignal.

*The stages.*

1. **Data.** Attendance sheets, assignment logs and internal marks are collected with the students' knowledge.
2. **Features.** The data is cleaned and turned into numbers such as attendance percentage, scaled so that no column dominates.
3. **Model.** Logistic regression turns the features into a risk score between 0 and 1.
4. **Service.** A small program takes one student's features and returns the score, and ranks all students.
5. **Human decision.** A teacher reads the top 40 and decides whom to meet. The tool advises; it never punishes.
6. **Feedback.** The end-of-term result is stored so that the model can be checked and retrained.

*Example.* In the simulated college, 138 of 600 students fail. The service ranks all 600 by score and the teacher meets the top 40, so effort goes where help is most likely to matter.

*Why it matters.* (i) Each stage can be tested alone. (ii) A weak stage is easy to find. (iii) The feedback arrow shows when the model has gone stale.

*Conclusion.* Naming the failure of each arrow in the report shows the examiner that the student understands the whole system, not just the model.

**Q2 (5 marks). What is the accuracy trap? Explain it with the SikshyaSignal numbers and state which metrics should be reported instead.**

*Introduction.* Accuracy is the share of predictions that are correct. When one class is rare, a useless model can still score high accuracy, and this is called the accuracy trap.

*The numbers.* In the simulated college 138 of 600 students (23.0 percent) fail. A model that always answers "will not fail" is right for the other 462 students, so its accuracy is 462 ÷ 600 = **77.0 percent**. Yet it finds none of the failing students, so its **recall is 0**. The attendance-below-70 rule is only 75.8 percent accurate but finds 63 of the 138 failing students (recall 0.46).

| Method | Accuracy | Recall | Precision |
|---|---|---|---|
| Do nothing | 77.0% | 0% | undefined |
| Attendance < 70 rule | 75.8% | 46% | 47% |

*What to report.* (i) The **confusion matrix** (TP, FP, FN, TN). (ii) **Recall**, because missing a failing student is the costly error. (iii) **Precision**, because teachers have limited time and false alarms waste it. (iv) The scores of at least one **baseline** beside the model's score. (v) Precision at the top *k*, here the top 10 percent of the test students.

*Conclusion.* A report that gives only accuracy invites the first examiner question: "what would a model that always says no score?" Answer it in the report before it is asked.

**Q3 (10 marks). Describe how you would plan a final-year machine-learning project from idea to scope. Use the early-warning example and discuss the problem statement, objectives, the decision to use ML, data, ethics, evaluation and risks.**

*Introduction.* A final-year ML project is a decision system, so its plan must cover the problem, the data, the method, the evaluation and the effect on people. The running example is SikshyaSignal, which ranks first-year students by risk of failing a subject so that teachers can help early.

*1. Problem statement.* Write four parts: who is affected (600 first-year students and their teachers), what happens now (failures are noticed six weeks before the final, too late), how big (about 23 percent fail) and what the project will change (a ranked list of 40 students two weeks earlier).

*2. Objectives.* Make them measurable and name the metric: recall above the baseline, at least 60 percent of the top 10 percent truly failing, a group-gap report, a service answering within 100 ms and eight passing unit tests.

*3. Decide whether to use ML.* Follow Figure 1.3. A clear rule exists but is weak (recall 0.46). Enough labelled history can be collected from earlier batches. So a model is justified, and the rule becomes the baseline.

*4. Data.* List every column, its source, unit and valid range, and who may see it. State that the demo data is simulated, with seed 404, so that nothing private is at risk.

*5. Ethics and law.* Screen for consent, bias and human review. Keep only the columns needed, limit access, and follow the Individual Privacy Act 2075 and the Electronic Transactions Act 2063 in spirit.

*6. Evaluation plan.* Fix the split before modelling, compare with the do-nothing and rule baselines, and report precision, recall, the confusion matrix and group rates.

*7. Risks.* Biased or stale data, over-fitting, a model that is ignored, and a wrongly flagged student. Each gets a named cure.

| Plan part | Question it answers |
|---|---|
| Problem and objectives | what exactly will change and how it is counted |
| Method choice | why ML and not a rule |
| Data and ethics | is it available, legal and fair |
| Evaluation | how will we know it works |

*Conclusion.* A capstone that fixes these seven items before coding gives the supervisor something to review, the student a schedule, and the examiner a clear standard against which to judge the result.
