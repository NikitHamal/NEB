---
subject: Project I
grade: BCA Semester 4
unit: 1
title: Choosing, Scoping and Justifying a Project
area: BCA 256 · Project I · Unit 1
---

Project I is the first time you build something that nobody gave you a question paper for. The college gives you a supervisor, a deadline and a viva; everything else (the idea, the plan, the code and the report) is yours. This unit shows how to pick an idea that can really be finished in one semester, write it down as a clear problem statement, and prove to the supervisor that it is feasible.

::: key What this unit gives you
- Where good project ideas come from, and a funnel to cut a long list down to one.
- How to write a problem statement, objectives and a scope table that a supervisor can sign.
- A feasibility check (technical, economic, operational, schedule) with a worked score.
- The project life cycle used in the rest of this book, and the running example, **CampusShelf**.
:::

## 1.1 What Project I is, and what it is not

BCA 256 is a 2-credit practical course. TU does not publish a unit-wise syllabus for it, so colleges follow a common pattern: a proposal in the first weeks, a supervised build, a written report in the TU format and a final viva before an internal and an external examiner. A good Project I is **small, finished and well explained**. It is not a copy of an internet repository, it is not a half-built "social network", and it is not judged by the number of pages in the report.

Throughout this book one small system is built from first idea to final demo: **CampusShelf**, a library book-issue system for a college with 1,200 students. The same steps apply to your own idea, whether it is a bus-ticket app, a clinic appointment system or a school result portal.

## 1.2 Where good ideas come from

| Source | Example question | Nepali example |
|---|---|---|
| A paper process you can see | "Which register could be a table?" | library issue register, fee receipts |
| A complaint you hear often | "What annoys people every week?" | long queues at a ward office counter |
| An existing app that misses something | "What would a local user want?" | an e-learning app in Nepali with offline notes |
| A public data set | "What can this data answer?" | Nepal census or weather data visualised |
| A lab or hardware kit | "What can a cheap sensor do?" | Arduino soil-moisture alert for a farm |

The funnel in Figure 1.1 turns 10 to 15 raw ideas into one. Each idea is dropped when it fails a gate: you cannot name a real user, you cannot finish it in 12 weeks, or you do not own the skills and tools to build it.

```photogrid label="1.1" cols="2" ratio="1.5" caption="Ideas are tested in public before they are built. (a) A student pitches a software idea at a hackathon: two minutes, one problem, one user. Practise this pitch on your classmates before you meet the supervisor. (b) The idea funnel used in this book: many ideas go in, one scoped project comes out."
@ photo id="bca256/pitch" cap="Pitching an idea at a hackathon"
fit 1.5
focus 0.40 0.55
call 0.40 0.90 0.38 0.70 "One speaker, one idea"
@ svg cap="The idea funnel"
f = Fig(330, 220)
f.poly([(10,8),(320,8),(285,58),(45,58)], fill=BLUE, stroke=NAVY, label="12 raw ideas", lx=165, ly=33, size=12, color=NAVY)
f.poly([(50,66),(280,66),(255,116),(75,116)], fill=SOFT, stroke=TEAL, label="Gate 1: real user", lx=165, ly=91, size=12, color=NAVY)
f.poly([(80,124),(250,124),(230,170),(100,170)], fill=SOFT, stroke=AMBER, label="Gate 2: 12 weeks", lx=165, ly=147, size=11, color=NAVY)
f.poly([(105,178),(225,178),(210,214),(120,214)], fill=BLUE, stroke=RED, label="Gate 3: skills", lx=165, ly=196, size=10.5, color=NAVY)
```

## 1.3 Writing the problem statement

A problem statement has four parts: **who** has the problem, **what** the problem is, **how big** it is (with a number), and **what happens if nothing changes**. It does not mention the solution.

*CampusShelf, version 1.* "Library staff at a 1,200-student college record every book issue by hand in a register. A student waits about 6 minutes at the counter because the staff must search the register for overdue entries and calculate the fine. About 1 issue in 10 is recorded wrongly, so the library cannot say who holds a missing book."

Notice the three numbers (1,200, 6 minutes, 1 in 10). Numbers make the problem real and give you a way to prove success at the demo: *"issue time reduced from 6 minutes to under 30 seconds"*.

**Objectives must be SMART:** specific, measurable, achievable, relevant, time-bound.

| Weak objective | SMART version |
|---|---|
| "Make the library faster." | "Issue or return a book in under 30 seconds, measured on 20 test transactions, by week 10." |
| "Add security." | "Only a logged-in librarian can issue books; passwords stored as salted hashes." |
| "Handle fines." | "Fine = Rs 2 per overdue day after a 14-day loan, calculated automatically." |

## 1.4 Scope: what is in, and what is out

The most common reason a project fails is **scope creep**: a new feature every week. A written scope table is your defence.

| In scope (must finish) | Out of scope (say no politely) |
|---|---|
| Add, search and edit books and members | Online payment of fines (eSewa, Khalti) |
| Issue and return with due-date and fine | Mobile app version |
| Overdue report for the librarian | Barcode scanner hardware |
| Login for librarian | SMS reminders to students |

Out-of-scope items are not wasted: put them in the final report as **future enhancements**, which examiners like to see.

## 1.5 Feasibility: can this really be finished?

Before you start, test four kinds of feasibility:

- **Technical:** do you know (or can you learn in two weeks) the language, database and tools?
- **Economic:** does it cost nothing, or only what the team can pay (hosting, a sensor kit)?
- **Operational:** will the real user (the librarian) actually use it?
- **Schedule:** can the work be done in about 12 weeks beside your other subjects?

A weighted score removes arguments. Each factor gets a weight and a mark out of 10; the code multiplies and adds.

```python
weights = {"technical": 0.35, "economic": 0.15, "operational": 0.30, "schedule": 0.20}
ideas = {
    "CampusShelf (library)":   {"technical": 9, "economic": 9, "operational": 8, "schedule": 8},
    "Social network":          {"technical": 4, "economic": 5, "operational": 5, "schedule": 2},
    "Soil-moisture alert":     {"technical": 6, "economic": 6, "operational": 7, "schedule": 6},
}
for name, marks in ideas.items():
    score = sum(weights[k] * marks[k] for k in weights)
    verdict = "GO" if score >= 7 else "RESCOPE"
    print(f"{name:24s} {score:4.2f}  {verdict}")
```
```output
CampusShelf (library)    8.50  GO
Social network           4.05  RESCOPE
Soil-moisture alert      6.30  RESCOPE
```
A score under 7 does not kill the idea; it tells you to shrink the scope (the "Social network" becomes "a class notice board").

## 1.6 The project life cycle used in this book

Figure 1.2 shows the six phases. They are not strictly one-way: testing sends you back to coding, and the supervisor's review can send you back to design. Units 2 to 5 follow the phases in order.

```svgfig label="1.2" caption="The Project I life cycle. Each phase ends with a deliverable that the supervisor can check. Dashed arrows show the loops: bugs go back to coding, review comments go back to design."
f = Fig(780, 230)
names = ["1 Idea &\nscope", "2 Plan &\nteam", "3 Analyse &\ndesign", "4 Build", "5 Test", "6 Report &\nviva"]
dels = ["proposal", "Gantt + board", "DFD, ER, UI", "working code", "test report", "report + demo"]
cols = [BLUE, SOFT, BLUE, SOFT, BLUE, SOFT]
for i, n in enumerate(names):
    x = 10 + i * 128
    f.box(x, 60, 108, 60, n, fill=cols[i], stroke=NAVY, size=11, bold=True)
    f.text(x + 54, 140, dels[i], size=10, color=TEAL, bold=True)
    if i < 5:
        f.arrow([(x + 108, 90), (x + 128, 90)], color=NAVY)
f.arrow([(522, 50), (522, 28), (394, 28), (394, 50)], color=RED, dash=True, label="bugs", lpos=(458, 20))
f.arrow([(394, 50), (394, 36), (266, 36), (266, 50)], color=AMBER, dash=True, label="review", lpos=(330, 30))
f.text(390, 205, "Deliverable of each phase shown in teal; 12 weeks in total", size=10.5, color=SLATE)
```

## 1.7 Eight reasons student projects fail, and the cure

1. **No clear user.** The team builds "for everyone", so nobody's needs are tested. The cure is to name one real person, such as the college librarian, and ask her to review each version. A real user gives honest feedback that classmates will not.
2. **Scope creep.** Every week brings a new feature from a friend or a YouTube video. The old features then stay unfinished. Keep the scope table of §1.4 pinned above your desk and add new ideas only to the future-enhancements list.
3. **Starting to code on day one.** Without a design, the database changes weekly and code is rewritten again and again. A two-week design phase (Unit 3) saves four weeks of rework. Supervisors can only help you if they see a design.
4. **Unrealistic schedule.** Teams plan 12 weeks of work in 12 weeks and forget exams, festivals (Dashain, Tihar) and load-shedding. Plan 9 weeks of work and keep 3 weeks as buffer.
5. **One person does everything.** The "team" is one hard-working student and three names on the cover. The viva exposes this quickly. Split the work by module and let every member explain every module.
6. **No version control or backup.** A laptop failure a week before the deadline ends the project. Use Git with a remote copy from day one (Unit 2) and commit at least every working day.
7. **Testing only at the end.** Bugs found in week 12 cannot be fixed. Write a few test cases with each module (Unit 4) so the demo does not depend on luck.
8. **Report written in the last week.** The report becomes copied text with screenshots that do not match the code. Write each chapter as its phase finishes, so the report records what you actually did.

```photogrid label="1.2" cols="2" ratio="1.2" caption="A fair way to pick the project idea. (a) A wall of sticky notes: brainstorming produces many ideas quickly, but the choice must be made with a rule. (b) Four candidate ideas were scored from 1 to 5 on usefulness, doability in 12 weeks, data already at hand and novelty (invented scores), and a weighted sum with weights 40, 30, 20 and 10 per cent put the Book exchange at 3.9 out of 5. To test whether the result depends on those weights, 10,000 other weightings were drawn at random (fixed seed): the book exchange still wins 49 per cent of the time, the mess tracker 26, the bus tracker 26 and the seat finder 0. An idea that wins only under one weighting is a fragile choice; one that wins under most is safe, and the supervisor meeting is the place to defend the scores."
@ photo id="bcapj/stickies" cap="A wall of ideas: choose with a rule, not a mood"
fit 1.2
focus 0.5 0.5
@ svg cap="Weighted idea matrix and 10,000 other weightings"
import numpy as np
ideas = ["Book exchange", "Mess tracker", "Bus tracker", "Seat finder"]
crit = ["Useful", "Doable in 12 wk", "Data at hand", "Novel"]
S = np.array([[4, 4, 4, 3], [3, 5, 4, 2], [5, 2, 2, 4], [3, 4, 3, 3]], float)
w = np.array([0.4, 0.3, 0.2, 0.1])
tot = S @ w
rng = np.random.default_rng(2081)
W = rng.dirichlet(np.ones(4), 10000)
win = np.bincount(np.argmax(W @ S.T, axis=1), minlength=4) / 10000
assert int(np.argmax(tot)) == 0 and abs(tot[0] - 3.9) < 1e-9
facts = dict(best=ideas[int(np.argmax(tot))], t=round(float(tot[0]), 2), w0=round(win[0] * 100), w1=round(win[1] * 100), w2=round(win[2] * 100), w3=round(win[3] * 100))
f = Fig(300, 236)
f.text(150, 12, "scores 1-5 (invented), weights 40/30/20/10", size=10.5, color=NAVY, bold=True)
for j, c in enumerate(crit):
    f.text(119 + j * 42, 34, ["Use", "Do", "Data", "New"][j], size=10.5, color=NAVY, bold=True)
f.text(272, 34, "Sum", size=10.5, color=NAVY, bold=True)
for i, nm in enumerate(ideas):
    y = 42 + i * 24
    f.box(4, y, 96, 20, nm, fill=BLUE if i else "#bbf7d0", stroke=NAVY, size=10.5, bold=True, r=3, sw=1)
    for j in range(4):
        f.box(99 + j * 42, y, 40, 20, "%d" % S[i][j], fill="#f1f5f9", stroke=SLATE, size=10.5, r=2, sw=1)
    f.box(246, y, 48, 20, "%.2f" % tot[i], fill="#fde68a", stroke=AMBER, size=10.5, bold=True, r=3, sw=1)
f.text(150, 152, "how often each idea wins over 10,000 random weightings", size=10.5, color=NAVY, bold=True)
for i, nm in enumerate(ideas):
    y = 162 + i * 17
    f.text(4, y + 7, nm, size=10.5, color=NAVY, anchor="start", vmid=True)
    f.box(104, y, win[i] * 180, 13, "", fill="#bbf7d0" if i == 0 else "#e5e7eb", stroke=SLATE, r=2, sw=1)
    f.text(108 + win[i] * 180, y + 7, "%d%%" % round(win[i] * 100), size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
```

## Formula and fact sheet

- Weighted feasibility score = Σ (weight × mark); go if ≥ 7 out of 10.
- Loan fine in the running example = Rs 2 × overdue days; loan period 14 days.
- Plan 9 working weeks inside 12 calendar weeks (25 % buffer).
- Problem statement = who + what + how big + what if nothing changes.

## Chapter summary

- A good Project I is small, finished and explained; it is judged on method, not size.
- Ideas come from real problems; a funnel with three gates leaves one project.
- The problem statement carries numbers; objectives are SMART; the scope table says what is out.
- Feasibility is technical, economic, operational and schedule; a weighted score makes the decision.

## Practice

1. Write a four-part problem statement for a project that helps a Nepali municipality ward office.
2. Convert "make the app secure" into two SMART objectives.
3. List four items for the in-scope and out-of-scope columns of a bus-ticket system.
4. Run the feasibility code with your own idea and weights. Is it a GO?
5. What is scope creep? Give three ways to control it.
6. Name the six phases of the project life cycle and one deliverable of each.
7. Why should the schedule keep a 25 % buffer?
8. Write the objectives for CampusShelf as a measurable table (three rows).
9. Differentiate technical and operational feasibility with an example.
10. The librarian types 30 issues per hour by hand; the system is expected to take 30 seconds each. How many issues per hour is that, and what is the gain?

::: note Answers and worked solutions
**1.** Example: "Ward office clerks at a municipality issue about 80 recommendation letters per day on paper. Citizens wait two hours because files are searched by hand, and 1 letter in 8 has a spelling error. Without change, queues grow with every new service."
**2.** "Passwords are stored as salted hashes"; "five wrong logins lock the account for 10 minutes".
**3.** In: seat booking, ticket print, cancellation, daily report. Out: online payment, GPS tracking, mobile app, SMS.
**4.** Output depends on your marks; a score of 7 or more is GO.
**5.** Uncontrolled addition of features after the plan is fixed. Control it with a signed scope table, a future-enhancements list and a supervisor approval for any change.
**6.** Idea (proposal), plan (Gantt), design (DFD/ER), build (code), test (test report), report and viva (report and demo).
**7.** Holidays, exams, illness and bugs always consume time; a buffer absorbs them.
**8.** Issue/return < 30 s on 20 tests; fine Rs 2/day after 14 days; librarian login with hashed passwords.
**9.** Technical: can the team write the code (they know Python). Operational: will the librarian use it daily (she must accept the new workflow).
**10.** 3600 / 30 = **120 issues per hour**, four times the manual rate of 30.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain feasibility study for a software project.**

*Introduction.* A feasibility study is a short investigation, done before any coding, to decide whether a proposed project can be completed successfully with the time, skills and money available. It protects the team from starting a project that cannot be finished.

*Four dimensions.*

1. **Technical feasibility** asks whether the required language, database and hardware are available and whether the team has or can learn the skills. A Python and SQLite system is technically easy; a face-recognition door lock needs new skills.
2. **Economic feasibility** compares costs (hosting, sensors, printing) with benefits. For a student project the target is near-zero cost.
3. **Operational feasibility** asks whether the intended users will accept and use the system. A librarian who dislikes computers can defeat the best software.
4. **Schedule feasibility** checks that the work fits the 12 weeks, with a buffer.

*Method and example.* Give each dimension a weight and a mark out of 10 and compute a weighted score (Section 1.5). For CampusShelf: 0.35 × 9 + 0.15 × 9 + 0.30 × 8 + 0.20 × 8 = 8.5, which is above 7, so the decision is GO. A social network scores 4.05 and must be rescoped.

*Conclusion.* The study turns opinion into evidence and gives the supervisor a reason to approve the proposal.

**Q2 (5 marks). Write the problem statement, objectives and scope of a project of your choice.**

*Project.* CampusShelf, a library book-issue system.

*Problem statement.* Library staff at a 1,200-student college record issues in a paper register. A student waits about 6 minutes, about 1 issue in 10 is recorded wrongly, and overdue books cannot be traced. If nothing changes, losses and queues grow with enrolment.

*Objectives (SMART).* (1) Issue or return a book in under 30 seconds on 20 test transactions by week 10. (2) Calculate fines automatically at Rs 2 per day after 14 days. (3) Let only a logged-in librarian change records. (4) Produce an overdue report in one click.

*Scope.* In: books, members, issue and return, fines, overdue report, login. Out: online payment, mobile app, barcode hardware, SMS.

*Conclusion.* Numbers in the problem and objectives allow the demo to prove success, and the scope table protects the schedule.

**Q3 (10 marks). Describe the stages of the project life cycle for a final-year-style software project and explain how each stage is checked.**

*Introduction.* A project life cycle divides the work into phases, each with a deliverable that the supervisor can inspect. It turns a vague "build a system" into steps that can be planned, tracked and marked. Figure 1.2 shows the six phases used in this book, with feedback loops.

*Phase 1: Idea and scope.* The team collects ideas, applies the funnel (real user, 12 weeks, skills) and writes the problem statement, SMART objectives and scope. Deliverable: the **project proposal**. Check: the supervisor signs it.

*Phase 2: Plan and team.* Work is broken into tasks, estimated, scheduled on a Gantt chart and placed on a task board. Roles are assigned and a Git repository is created. Deliverable: Gantt chart and board. Check: weekly stand-up and progress log.

*Phase 3: Analyse and design.* Requirements are written as functional and non-functional lists; a use-case diagram, data-flow diagrams, an ER diagram and screen sketches are drawn. Deliverable: the **design document**. Check: design review with the supervisor before coding.

*Phase 4: Build.* The team codes module by module, commits to Git every day and demonstrates a working increment every two weeks. Deliverable: working software. Check: demo of each increment.

*Phase 5: Test.* Test cases are run on each module and on the whole system; defects are logged and fixed, and the loop returns to Phase 4. Deliverable: **test report**. Check: pass rate against the objectives.

*Phase 6: Report and viva.* The report is compiled in the TU format, a presentation and a demo script are prepared and a mock viva is held. Deliverable: bound report and demo. Check: internal and external examiners.

| Phase | Deliverable | Checked by |
|---|---|---|
| 1 Idea and scope | proposal | supervisor signature |
| 2 Plan and team | Gantt, board, repository | weekly stand-up |
| 3 Analyse and design | DFD, ER, screens | design review |
| 4 Build | working code | fortnightly demo |
| 5 Test | test report | pass rate vs objectives |
| 6 Report and viva | report, demo | examiners |

*Conclusion.* The life cycle works because every phase has an output and a reviewer. Skipping a phase, usually design or testing, is the main reason student projects are rewritten at the last minute.
