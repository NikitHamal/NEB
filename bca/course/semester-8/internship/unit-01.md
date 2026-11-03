---
subject: Internship
grade: BCA Semester 8
unit: 1
title: The Internship: Purpose, Placement Search, CV and Interview
area: BCA 452 · Internship · Unit 1
---

Seven semesters of classroom and lab work end in a place that has no timetable: a real office, with real clients, where a mistake costs somebody's money. The internship is the **bridge between study and work**. Done well, it turns "I know Java" into "I fixed a bug in a live system and my supervisor will say so". Done badly, it is eight weeks of making tea and a report copied from a friend. This unit shows how to choose the placement, prepare for it and win it.

::: key What this unit gives you
- What an internship is, and how it differs from a project, a training course and a job.
- A running example, **InternTrail**: Anisha Gurung's eight-week placement at the invented agency Himal Digital.
- Three **SMART learning objectives** written before the search begins, so the placement is judged by what you wanted from it.
- An executed **weighted shortlist** script that ranks five offers, a 12-week search timeline and a one-page CV anatomy.
- Real photographs of an open office, an interview table and a handshake, and the eight reasons good students lose good placements.
:::

## 1.1 What an internship is

An **internship** is a supervised, time-limited period of work in an organisation, done for learning and for assessment, usually in the final semester. The college marks it; the host organisation supervises it. Five things are often confused with it.

| Item | Who sets the task | Main purpose | Typical length | Output |
|---|---|---|---|---|
| **Internship** | the host organisation | learn to work in a real team | 6 to 8 weeks | log, report, supervisor letter |
| Project (BCA 256 to 404) | you and your college supervisor | build and defend one system | one semester | system, report, viva |
| Training course | the trainer | learn a fixed skill | days to weeks | certificate |
| Part-time job | the employer | produce value for pay | open-ended | salary |
| Volunteering | the organisation | help a cause | open-ended | experience |

Notice what the table says. In a project **you** choose the problem; in an internship the **organisation** does, and your job is to be useful on problems you did not choose. That is why attitude, reliability and communication count as much as code in an internship report.

## 1.2 The running example: InternTrail

InternTrail is invented for this book. **Anisha Gurung** is a Semester VIII BCA student in Kathmandu. She is fairly good at web development, nervous about speaking, and has a laptop, a half-finished portfolio and no work experience. **Himal Digital Pvt. Ltd.** is an imaginary 12-person web agency in Lalitpur that builds websites and small management systems for schools, cooperatives and shops. It takes two interns a year.

*Problem statement.* "Anisha has eight weeks, from the first Sunday of Magh to the last Friday of Falgun, to complete a placement worth 3 credits. She must (1) win a placement that matches her interests, (2) contribute to at least one real deliverable, (3) keep an honest daily log and (4) defend a report at the end."

The next four units follow her from the application email to the viva. Every number, name and log entry is made up; the **method** is real.

## 1.3 Write your learning objectives first

Most students begin by sending a CV to everyone. A better start is a half page that answers "what do I want from these eight weeks?". The objectives guide the search, shape the weekly review (Unit 3) and become the backbone of the report (Unit 5). Use the **SMART** test: Specific, Measurable, Achievable, Relevant, Time-bound.

| # | Weak objective | SMART version (Anisha) |
|---|---|---|
| L1 | "Learn web development" | "Ship one bug fix and one small feature in the company's Laravel code base by week 6, each reviewed by my supervisor" |
| L2 | "Improve communication" | "Give a five-minute demo to the team in week 4 and one to the client in week 7" |
| L3 | "Get experience" | "Keep a daily log of at least 6 hours' work for 40 working days and have it signed weekly" |

An objective that cannot be checked at the end cannot be reported honestly. If an organisation cannot let you reach L1 (for example, it only offers data entry), that is a reason to **decline the offer**, not to hide the gap later.

## 1.4 Searching and shortlisting

Placements come from five sources. **College placement cells** and past-student recommendations give the most trustworthy leads. **Professional networks** (LinkedIn, local IT-community groups, alumni) come next. **Company career pages and job portals** list advertised internships, and **cold email** to small firms works better than most students expect when it is short and specific. Whatever the source, collect three to five options before choosing; one offer is a deadline, five are a choice.

Choosing by gut feeling usually means choosing the biggest name. A **weighted decision matrix** forces you to say what matters. Give each criterion a weight (the weights sum to 1), score each option from 1 to 5, and compute the weighted total. The script below does this for five invented offers. It is the same method used in project selection (Project I) applied to your own career.

```python
weights = {"learning": .30, "mentor": .20, "travel": .15,
           "stack": .15, "stipend": .10, "letter": .10}
keys = list(weights)   # scores follow this order
raw = {
    "Himal Digital":   (5, 4, 4, 5, 2, 4),
    "Everest Bank IT": (3, 3, 3, 2, 4, 5),
    "Terai Telecom":   (3, 2, 1, 3, 5, 3),
    "Pokhara Pixels":  (4, 5, 2, 4, 3, 3),
    "Cousin's Shop":   (2, 1, 5, 1, 1, 1),
}
offers = {n: dict(zip(keys, v)) for n, v in raw.items()}
assert abs(sum(weights.values()) - 1) < 1e-9
rows = []
for name, s in offers.items():
    total = sum(weights[k] * s[k] for k in weights)
    rows.append((total, name))
rows.sort(reverse=True)
for rank, (total, name) in enumerate(rows, 1):
    print(f"{rank}. {name:<16} {total:.2f} / 5")
# sensitivity: what if travel mattered twice as much?
w2 = dict(weights); w2["travel"] = 0.30; w2["learning"] = 0.15
r2 = sorted(((sum(w2[k] * s[k] for k in w2), n) for n, s in offers.items()), reverse=True)
print("travel-heavy winner:", r2[0][1], f"{r2[0][0]:.2f}")
```
```output
1. Himal Digital    4.25 / 5
2. Pokhara Pixels   3.70 / 5
3. Everest Bank IT  3.15 / 5
4. Terai Telecom    2.70 / 5
5. Cousin's Shop    1.90 / 5
travel-heavy winner: Himal Digital 4.10
```

*Reading the output.* Himal Digital wins with 4.25 out of 5 because it scores well on the two heaviest criteria, learning and mentor. Check one total by hand: 0.30×5 + 0.20×4 + 0.15×4 + 0.15×5 + 0.10×2 + 0.10×4 = 1.50 + 0.80 + 0.60 + 0.75 + 0.20 + 0.40 = **4.25**. The last line is a **sensitivity test**: when travel is weighted twice as heavily and learning is halved, Himal Digital still wins (4.10), so the decision is robust. A winner that flips when the weights move slightly is a sign you do not yet know what you want. Notice also that the best stipend (Terai Telecom) ranks fourth: money matters, but it is 10 percent of this decision, not all of it.

```svgfig label="1.1" caption="Placement search timeline, counted backwards from the first day. Objectives and the CV come first; interviews and the decision happen at least five weeks before the start so that the college letter and the paperwork are never rushed. The shaded final block is the placement itself."
f = Fig(580, 200)
f.line(30, 90, 550, 90, color=SLATE, sw=2)
steps = [(40, "-12", "Write 3 SMART\nobjectives", BLUE, NAVY), (110, "-10", "CV, portfolio,\nLinkedIn", BLUE, NAVY),
         (180, "-9", "Shortlist 5 and\nsend 8 emails", SOFT, TEAL), (250, "-7", "Interviews,\ntest tasks", SOFT, TEAL),
         (320, "-5", "Score offers,\naccept one", "#fde68a", AMBER), (390, "-3", "College letter,\nNDA, ID forms", "#fde68a", AMBER),
         (460, "-1", "Set up laptop,\nroute, clothes", BLUE, NAVY)]
for x, wk, txt, fl, st in steps:
    f.circle(x + 25, 90, 7, fill=fl, stroke=st)
    f.text(x + 25, 68, "week " + wk, size=10, color=NAVY, bold=True)
    f.box(x - 6, 112, 62, 52, txt, fill=fl, stroke=st, size=8.8, color=NAVY)
f.box(526, 74, 46, 32, "Start", fill=SOFT, stroke=TEAL, size=10, color=NAVY, bold=True)
f.text(290, 30, "Weeks before the first working day", size=11, color=NAVY, bold=True)
f.text(290, 186, "Real life is messier, but a calendar beats good intentions.", size=9.5, color=SLATE, italic=True)
```

```photogrid label="1.1" cols="3" ratio="1.0" caption="Where an internship is won and done. (a) An open-plan working space: most Himal Digital-sized firms look like this, with shared desks, headphones and laptops, and a supervisor within shouting distance. (b) A career-fair interview table: two people, a few sheets of paper and ten minutes decide the shortlist. (c) A handshake after an agreement: the offer is confirmed in writing, but the handshake is where trust starts."
@ photo id="bca452/berlin" cap="Open-plan workspace"
fit 1.0
focus 0.4 0.5
call 0.5 0.85 0.5 0.65 "shared desks, laptops"
@ photo id="bca452/interview" cap="Interview table"
fit 1.0
focus 0.6 0.5
call 0.5 0.9 0.5 0.7 "ten minutes decide"
@ photo id="bca452/handshake" cap="Offer confirmed"
fit 1.0
focus 0.6 0.5
call 0.5 0.9 0.5 0.7 "trust starts here"
```

## 1.5 The CV, the email and the interview

**The one-page CV.** A recruiter at a small firm spends about thirty seconds on a CV, so it must be **one page, in a plain layout, with the evidence first**. Figure 1.2 shows the anatomy. Put projects above hobbies, link to code you are proud of, and give numbers: "built a result-entry system used by 3 teachers" beats "good at PHP". Never list a skill you cannot demonstrate in an interview; the interviewer will ask for it.

```svgfig label="1.2" caption="Anatomy of a one-page CV. The top band answers who and where; the profile line says what you want; projects and skills carry the proof; education and referees are short. Numbers in the right-hand callouts are the rules to apply to each block."
f = Fig(580, 280)
f.box(30, 10, 250, 262, "", fill="#ffffff", stroke=NAVY)
blocks = [(18, 42, "Name, phone, email, GitHub, city", BLUE), (66, 30, "Profile: one line, one goal", SOFT),
          (102, 72, "Projects: 3 items with numbers and links", "#fde68a"), (180, 38, "Skills: only what you can demo", SOFT),
          (224, 22, "Education: BCA, TU, expected year", BLUE), (250, 16, "Referees on request", BLUE)]
for y, h, t, c in blocks:
    f.box(40, y, 230, h - 3, t, fill=c, stroke=NAVY, size=9.2, color=NAVY)
notes = [(38, "1  Professional email, no nicknames"), (80, "2  Tailor the profile to each firm"),
         (138, "3  Verb + task + number + link"), (200, "4  List 6 to 8, strongest first"),
         (236, "5  One page, PDF, named Anisha-Gurung-CV.pdf")]
for y, t in notes:
    f.arrow([(286, y), (310, y)], color=TEAL)
    f.text(316, y, t, size=10.2, color=NAVY, anchor="start", vmid=True)
```

**The cover email.** Four short paragraphs are enough: who you are, why this firm, one proof of skill, and the ask. Attach the CV and the college letter. Use a clear subject such as "Internship application: Anisha Gurung, BCA Semester VIII (web development)". Follow up once after one week, politely.

**The interview.** Expect three kinds of question. *Motivation:* "Why us?" (answer with something specific you read about the firm). *Technical:* a small task or "explain this project" (be honest about what you did and what a teammate did). *Behavioural:* "Tell me about a time you missed a deadline." Use the **STAR** pattern: Situation, Task, Action, Result. Prepare two stories, one about teamwork and one about learning from a mistake. End by asking two questions of your own, such as "What will a good week-four look like for me?" and "Who will review my work?". Those questions also tell you how good the mentor will be.

## 1.6 Eight reasons good students lose good placements

1. **They apply to everyone with the same email.** A copy-pasted message that says "Dear Sir/Madam" is deleted in seconds. Name the firm, name one product or project of theirs, and say what you can do for them. This single change often doubles the reply rate.
2. **The CV is long and the evidence is thin.** Three pages of subjects studied tell the reader nothing. One page with three projects, each with a number and a link, proves ability. Recruiters at small agencies open the GitHub link first.
3. **They cannot explain their own project.** Asked "why did you choose MySQL?", the candidate goes silent. Rehearse a two-minute explanation of your best project: the problem, your part, one thing that went wrong and what you did about it.
4. **They arrive late or untidy to the interview.** Lateness says "I will be late to stand-up too". Plan the route the day before, arrive ten minutes early, dress as the office does, and keep your phone silent. Small signals decide close calls.
5. **They accept the first offer without a comparison.** A famous name may offer no mentor and only data entry. Score offers as in Section 1.4 and ask what you will actually do each week. A smaller firm with a caring supervisor often teaches more.
6. **They ignore the college paperwork.** The placement letter, supervisor form and ID details are due before the start. Missing them can delay the credit. Make a checklist at week minus three and tick it off with your coordinator.
7. **They lie or exaggerate.** Claiming "expert in React" and then failing a simple test ends an offer immediately and spreads in a small industry. Say "I have built two small apps and I learn fast". Honest limits plus visible effort are respected.
8. **They stop after one "no".** Most replies are silence or "not now". Send eight emails, follow up once, and keep a tracking table of firm, date, reply and next step. Persistence with politeness is a professional skill that the internship will itself require.

## Formula and fact sheet

| Item | Rule or fact |
|---|---|
| Internship | supervised, time-limited work placement for learning and assessment |
| SMART | Specific, Measurable, Achievable, Relevant, Time-bound |
| Weighted score | total = Σ (weight × score), weights sum to 1 |
| Sensitivity test | change the weights; a robust winner stays first |
| CV | one page, evidence first, PDF, professional email |
| STAR | Situation, Task, Action, Result |
| Search timeline | objectives −12, CV −10, apply −9, interview −7, decide −5, paperwork −3 weeks |

## Chapter summary

- An internship is **work in someone else's problem space**, supervised and assessed; it differs from a project, a course and a job.
- Write **three SMART learning objectives** before searching; they decide whether an offer is good.
- Compare at least three options with a **weighted matrix** and check the result with a sensitivity test.
- The CV is one page and proof-first; the email is short and specific; the interview uses honest STAR stories.
- Start the search twelve weeks before the placement and finish the paperwork three weeks before.

## Practice

1. Define internship and give two differences from a project.
2. Rewrite "I want to improve my coding" as a SMART objective.
3. Name four sources of placements and the strongest one.
4. In Section 1.4, compute the weighted score of Pokhara Pixels by hand.
5. Why is a sensitivity test useful?
6. List the five blocks of a one-page CV in order.
7. What does STAR stand for? Give an example for "a time you learned from a mistake".
8. Why should you ask the interviewer about code review?
9. Give three signs that an offered internship is a poor match.
10. State the date plan (in weeks) for applications and paperwork.

::: note Answers and worked solutions
**1.** A supervised work placement in an organisation for learning and credit. Differences: the organisation sets the task (you set it in a project); it is short (6 to 8 weeks) and ends in a log, report and supervisor letter.
**2.** "Complete 12 programming exercises on arrays and functions in two weeks, scoring at least 8 of 10 on the lab quiz."
**3.** College placement cell, professional networks (alumni, LinkedIn), career pages and portals, cold email. Placement cell and alumni recommendations are the most trustworthy.
**4.** 0.30×4 + 0.20×5 + 0.15×2 + 0.15×4 + 0.10×3 + 0.10×3 = 1.20 + 1.00 + 0.30 + 0.60 + 0.30 + 0.30 = 3.70.
**5.** It shows whether the winner depends on one weight; a robust winner gives confidence in the decision.
**6.** Contact details, profile line, projects, skills, education (referees last).
**7.** Situation, Task, Action, Result. Example: "My Java quiz marks fell (S); I had to pass the retake (T); I rewrote notes and solved ten programs a day (A); I scored 78 percent (R)."
**8.** Review shows whether someone will check and teach your work, which predicts how much you will learn.
**9.** No named supervisor; only data entry or tea-making; unpaid overtime with no learning; no letter or log signing; unsafe or illegal practices.
**10.** Objectives −12, CV −10, applications −9, interviews −7, decision −5, paperwork −3.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain SMART learning objectives for an internship with an example.**

*Introduction.* Learning objectives state what a student wants to gain from the placement. Writing them before the search makes the internship purposeful and gives the report a spine.

*The five letters.*

1. **Specific.** Name the skill and the task, such as "fix bugs in a Laravel code base" rather than "learn web development".
2. **Measurable.** Attach a number or a check: two reviewed pull requests, a demo, 40 signed log days.
3. **Achievable.** The goal must fit eight weeks and the firm's work; becoming a cloud architect does not.
4. **Relevant.** It must serve your career path, for example web development roles.
5. **Time-bound.** Give a week number, such as "by week 6".

*Example and use.* Anisha's L1 is "ship one bug fix and one small feature by week 6, each reviewed by my supervisor". It guides the search (the firm must use Laravel), the weekly review (are we on track?) and the report (did I achieve it?). *Conclusion.* SMART objectives turn an unplanned placement into a measurable one, and they let the student reject a poor offer early.

**Q2 (5 marks). Describe the weighted decision matrix for choosing between internship offers, with a worked example.**

*Introduction.* When several offers differ on many criteria, intuition favours the best-known name. A weighted decision matrix makes the trade-offs explicit.

*Steps.*

1. List criteria: learning, mentor, travel, stack match, stipend, letter value.
2. Give weights that sum to 1, higher for what matters most (learning 0.30, mentor 0.20).
3. Score each offer from 1 to 5 per criterion, with evidence from the interview.
4. Multiply and add: total = Σ weight × score.
5. Rank, then test sensitivity by changing two weights.

*Worked example.* Himal Digital scores 4.25 (1.50 + 0.80 + 0.60 + 0.75 + 0.20 + 0.40) and Pokhara Pixels 3.70, so Himal wins. When travel is doubled and learning halved it still wins with 4.10. *Conclusion.* The matrix does not remove judgement; it makes it visible and checkable.

**Q3 (10 marks). Explain how a BCA student should plan and complete the process of finding and winning an internship placement.**

*Introduction.* Finding a placement is a project with a deadline, so it deserves a plan. The process runs from self-knowledge through search and selection to preparation, and begins about twelve weeks before the first working day (Figure 1.1).

*The process.*

1. **Objectives first.** Write three SMART objectives (Section 1.3). They tell you what a good placement looks like.
2. **Prepare the evidence.** Build a one-page CV (Figure 1.2) with three projects, numbers and links, a clean GitHub and a professional email.
3. **Find leads.** Use the college placement cell, alumni, LinkedIn and careers pages, and send short, specific cold emails. Aim for eight applications and five replies.
4. **Interview well.** Prepare motivation, technical and behavioural answers, use STAR, arrive early, and ask about mentoring and code review.
5. **Compare offers.** Score each with the weighted matrix and run a sensitivity test.
6. **Close the paperwork.** Obtain the college letter, sign any confidentiality agreement, and confirm hours, supervisor and stipend in writing.
7. **Prepare logistics.** Test the route, prepare the laptop, and write a first-day checklist.
8. **Stay professional with refusals.** Thank the firms you decline; the industry is small.

| Stage | Output | Failure if skipped |
|---|---|---|
| Objectives | 3 SMART goals | accepts a poor match |
| CV and portfolio | one-page PDF, links | ignored in 30 seconds |
| Applications | tracking table | silence, no follow-up |
| Interview | STAR stories | unconvincing answers |
| Decision | weighted matrix | chooses by brand only |
| Paperwork | letter, NDA | credit delayed |

*Example.* Anisha writes L1 to L3, sends eight emails, gets five replies and three interviews, scores the offers and accepts Himal Digital at week minus five. *Conclusion.* A planned search turns luck into a repeatable process, and the same habits of planning, evidence and honesty carry into the internship itself.
