---
subject: Internship
grade: BCA Semester 8
unit: 5
title: Report, Presentation and Viva: Proving What You Did and Learned
area: BCA 452 · Internship · Unit 5
---

Friday of week eight. Anisha's desk is clear, her hand-over page is merged and her laptop is back in its drawer. Yet the internship is only two-thirds done in marks: the **report, the presentation and the viva** remain. These are the moments when the college decides whether the eight weeks were worth three credits. The good news is that a student who followed Units 2 to 4 already holds the evidence: a log, a plan, a ticket story and a signed supervisor page. This unit turns the evidence into a report that is honest, a talk that is clear and a viva that does not frighten.

::: key What this unit gives you
- A **report map** with a page budget (executed), and what each chapter must contain.
- The **supervisor letter and certificate**: what to request, when and how.
- A 10-minute presentation plan, a clear-slide checklist and a viva practice set of **twelve questions with model answers**.
- A reflection method with a self-assessment (executed) that shows growth honestly, including what is still weak.
- Photographs of a speaker, a handwritten letter and a poster, and eight habits that finish an internship well.
:::

## 5.1 The internship report

The report is the written proof. Colleges differ in the format, so **follow your own college template first**; the structure below is the common core. A good report is not long; it is **specific**. It names the organisation, dates, tasks and results, and every claim points to evidence in the appendix.

| Chapter | What it must contain | Evidence |
|---|---|---|
| 1 Introduction | purpose, duration, objectives L1 to L3 | objective table |
| 2 Organisation profile | what Himal Digital does, size, structure, tools | org chart (Figure 5.1) |
| 3 Plan and objectives | eight-week plan, expected outcomes | Figure 3.2 |
| 4 Weekly summary | one paragraph per week with hours and tasks | log, weekly reviews |
| 5 Technical contribution | one or two tickets in depth: problem, fix, tests, result | ticket HD-31, tests |
| 6 Learning, problems, ethics | skills gained, difficulties, confidentiality | self-assessment |
| 7 Conclusion | what was achieved against objectives, recommendations | table |
| Appendices | signed log, supervisor letter, hand-over page | scans |

The report is not a diary and not a brochure. Do not copy the company website into chapter 2, and do not claim work done by colleagues. Where the NDA forbids detail, describe the **method** and hide the client name; say that you did so.

## 5.2 Planning the pages

A report tends to grow where the writer feels comfortable and shrink where the examiner is looking. Decide a **page budget** early. The script below allocates a 40-page body (a typical college limit is 30 to 50; yours may differ) across the chapters, checks the total and estimates the word count at 300 words a page. Heavier chapters are the ones that carry marks: weekly summary and technical contribution.

```python
budget = [("1 Introduction", 3), ("2 Organisation profile", 4), ("3 Plan and objectives", 3),
          ("4 Weekly summary", 8), ("5 Technical contribution", 8),
          ("6 Learning, problems, ethics", 5), ("7 Conclusion", 2), ("Appendices", 7)]
total = sum(p for _, p in budget)
assert total == 40, total
for name, pages in budget:
    print(f"{name:<30} {pages:>2} pages {pages / total * 100:>5.1f}%  ~{pages * 300:>5} words")
core = sum(p for n, p in budget if n[0] in "45")
print(f"total {total} pages, ~{total * 300} words")
print(f"chapters 4 and 5 carry {core} pages = {core / total * 100:.0f}% of the report")
```
```output
1 Introduction                  3 pages   7.5%  ~  900 words
2 Organisation profile          4 pages  10.0%  ~ 1200 words
3 Plan and objectives           3 pages   7.5%  ~  900 words
4 Weekly summary                8 pages  20.0%  ~ 2400 words
5 Technical contribution        8 pages  20.0%  ~ 2400 words
6 Learning, problems, ethics    5 pages  12.5%  ~ 1500 words
7 Conclusion                    2 pages   5.0%  ~  600 words
Appendices                      7 pages  17.5%  ~ 2100 words
total 40 pages, ~12000 words
chapters 4 and 5 carry 16 pages = 40% of the report
```

*Reading the output.* The 40 pages come to about 12,000 words, but the appendices are mostly scans (signed log, letter), so the written text is nearer 10,000 words. The key line is the last one: **chapters 4 and 5 carry 40 percent of the report**. They are the evidence of what you did, so they must be the best. If your draft shows 15 pages on the history of the company and 3 on your own work, the budget has caught the problem before the examiner does.

```svgfig label="5.1" caption="Map of the internship report. Each chapter points to the evidence collected in Units 1 to 4, so the report is mostly assembly, not invention. The shaded chapters 4 and 5 carry 40 percent of the pages."
f = Fig(580, 230)
ch = [("1 Intro", "aims L1-L3", BLUE, NAVY), ("2 Organisation", "profile", BLUE, NAVY), ("3 Plan", "8-week plan", BLUE, NAVY),
      ("4 Weekly", "log, reviews", "#fde68a", AMBER), ("5 Technical", "HD-31 story", "#fde68a", AMBER), ("6 Learning", "skills", BLUE, NAVY), ("7 Conclusion", "vs aims", BLUE, NAVY)]
for i, (n, e, fl, s) in enumerate(ch):
    x = 6 + i * 82
    f.box(x, 24, 74, 56, "", fill=fl, stroke=s)
    f.text(x + 37, 46, n, size=10, color=NAVY, bold=True)
    f.text(x + 37, 66, e, size=9.6, color=NAVY)
ev = [("Unit 1: objectives,\nsearch records", 6, 150), ("Unit 3: plan, daily log,\nweekly reviews", 170, 150), ("Unit 4: ticket, tests,\nhand-over page", 334, 150), ("Appendix: signed log,\nsupervisor letter", 480, 100)]
for t, x, w in ev:
    f.box(x, 150, w, 52, t, fill=SOFT, stroke=TEAL, size=9.2, color=NAVY)
f.arrow([(43, 80), (80, 150)], color=TEAL); f.arrow([(125, 80), (110, 150)], color=TEAL)
f.arrow([(207, 80), (230, 150)], color=TEAL); f.arrow([(289, 80), (260, 150)], color=TEAL)
f.arrow([(371, 80), (400, 150)], color=TEAL); f.arrow([(453, 80), (420, 150)], color=TEAL)
f.arrow([(535, 80), (520, 150)], color=TEAL)
f.text(290, 222, "evidence first, writing second", size=10, color=SLATE, italic=True)
```

## 5.3 Reflection and the honest self-assessment

Chapter 6 asks the question examiners enjoy most: **"what did you learn?"** Weak answers list technologies ("I learned PHP, Git, MySQL"). Strong answers show **change**: where you started, where you ended, what caused the change and what is still weak. A simple tool is a before-and-after rating of eight skills on a 1 to 5 scale, written from the evidence (log, review comments, results) and not from mood. The script below holds Anisha's ratings and computes the gains.

```python
skills = [("Teamwork", 3, 4), ("Communication", 2, 4), ("Git and review", 2, 4),
          ("Testing", 1, 4), ("Debugging", 3, 4), ("Documentation", 2, 3),
          ("Time management", 3, 4), ("Confidentiality", 2, 5)]
print(f"{'skill':<17}{'before':>7}{'after':>7}{'gain':>6}")
for n, b, a in skills:
    print(f"{n:<17}{b:>7}{a:>7}{a - b:>+6}")
mb = sum(b for _, b, _ in skills) / len(skills)
ma = sum(a for _, _, a in skills) / len(skills)
print(f"mean before {mb:.2f}, after {ma:.2f}, mean gain {ma - mb:+.2f}")
best = max(a - b for _, b, a in skills)
print("largest gain:", ", ".join(n for n, b, a in skills if a - b == best), f"(+{best})")
print("still 3 or below:", ", ".join(n for n, b, a in skills if a <= 3))
```
```output
skill             before  after  gain
Teamwork               3      4    +1
Communication          2      4    +2
Git and review         2      4    +2
Testing                1      4    +3
Debugging              3      4    +1
Documentation          2      3    +1
Time management        3      4    +1
Confidentiality        2      5    +3
mean before 2.25, after 4.00, mean gain +1.75
largest gain: Testing, Confidentiality (+3)
still 3 or below: Documentation
```

*Reading the output.* The mean rating rises from **2.25 to 4.00**, a gain of 1.75. The largest gains are in **Testing** (1 to 4) and **Confidentiality** (2 to 5), both tied to concrete evidence: the six-test suite of Unit 4 and the secrets scanner of Unit 2. **Documentation** is the only skill still at 3, and the report should say so plainly and name the next step (write one hand-over page for every project). Notice the style: each rating is followed in the report by one sentence of evidence. A table of all fives with no evidence would convince nobody; a table with an honest weak spot convinces everyone.

```svgfig label="5.2" caption="Self-assessment before (light bar) and after (dark bar), drawn from the script output. Gains are largest for testing and confidentiality; documentation remains at 3, and the report names it as the next learning target."
f = Fig(580, 245)
sk = [("Teamwork", 3, 4), ("Communication", 2, 4), ("Git and review", 2, 4), ("Testing", 1, 4), ("Debugging", 3, 4), ("Documentation", 2, 3), ("Time mgmt", 3, 4), ("Confidentiality", 2, 5)]
f.line(60, 205, 560, 205, color=SLATE); f.line(60, 25, 60, 205, color=SLATE)
for v in range(0, 6):
    y = 205 - v * 34
    f.line(56, y, 60, y, color=SLATE); f.text(50, y, str(v), size=9, color=SLATE, anchor="end", vmid=True)
short = ["Team", "Comm.", "Git", "Test", "Debug", "Docs", "Time", "Confid."]
for i, (n, b, a) in enumerate(sk):
    x = 72 + i * 61
    f.box(x, 205 - b * 34, 22, b * 34, "", fill="#bfdbfe", stroke=NAVY)
    f.box(x + 24, 205 - a * 34, 22, a * 34, "", fill=NAVY, stroke=NAVY)
    f.text(x + 23, 205 - a * 34 - 8, f"+{a-b}", size=9.5, color=TEAL, bold=True)
    f.text(x + 23, 220, short[i], size=9.6, color=NAVY)
f.box(76, 24, 12, 12, "", fill="#bfdbfe", stroke=NAVY); f.text(94, 30, "before", size=10, color=NAVY, anchor="start", vmid=True)
f.box(76, 42, 12, 12, "", fill=NAVY, stroke=NAVY); f.text(94, 48, "after", size=10, color=NAVY, anchor="start", vmid=True)
f.text(310, 238, "rating 1 (new) to 5 (confident, can teach it)", size=9.5, color=SLATE, italic=True)
```

```photogrid label="5.1" cols="3" ratio="1.0" caption="The three endings of an internship. (a) A speaker at a conference: the presentation is one story told in ten minutes, with the speaker looking at the audience, not the slide. (b) A handwritten letter: a supervisor's signed letter and a thank-you note are the human record of the placement. (c) A poster presenter beside the work: some colleges hold poster days, where a clear one-page summary leads the conversation."
@ photo id="bca105/speaker" cap="Presenting"
fit 1.0
focus 0.5 0.5
call 0.5 0.85 0.5 0.65 "look at the audience"
@ photo id="bca105/pen" cap="Letters"
fit 1.0
focus 0.5 0.5
call 0.5 0.85 0.5 0.65 "signed letter, thank-you"
@ photo id="bca256/poster" cap="Poster day"
fit 1.0
focus 0.5 0.5
call 0.5 0.85 0.5 0.65 "one-page summary"
```

## 5.4 Supervisor letter, certificate and references

Request three things from the host organisation, and request them **early**, ideally in week seven: a **completion certificate** with dates and hours, a **supervisor evaluation form** from your college (signed and stamped), and, if the supervisor agrees, a short **reference letter** for your future applications. Give the supervisor a half-page summary of your work, with ticket numbers, to make writing easy. Always ask permission before listing the supervisor as a referee, and always send a thank-you message on the last day. The people you meet are the start of your professional network, and in a small industry such as Nepal's, reputation travels fast.

## 5.5 The presentation

The college presentation is usually ten minutes plus questions. The panel has read the report; they want to hear **what you did, what you learned and whether you understand it**. Use **one slide per minute**, one idea per slide, large text and few words. A good order is: title and organisation (1 min); objectives and plan (1); weekly story in one chart, such as Figure 3.1 (1); technical contribution, the HD-31 story (3); learning and the skill chart (2); thanks, limits and future steps (1); questions (the rest). Show the real screen if you can; a screenshot of the correct invoice beats a paragraph describing it.

Rehearse aloud twice with a timer, once for a friend and once for a teacher. Prepare for a failed projector: carry the slides as PDF on a pen drive and keep a printed copy. Wear what the office would expect, and speak slowly; nervous speakers go twice as fast as they think.

## 5.6 The viva: twelve questions and model answers

The viva checks that you did the work and understood it. Examiners ask short, direct questions. Answer in three parts: **claim, evidence, honest limit**. Never bluff; "I did not do that part, a colleague did" is respected.

| # | Question | Model answer (short) |
|---|---|---|
| 1 | What did the organisation do and what was your role? | Himal Digital builds websites and small management systems for schools and shops; I was a web-development intern on the billing module, reporting to Sanjay. |
| 2 | What were your objectives and did you meet them? | L1 (ship a fix and a feature) yes for the fix, the feature was merged in week 6; L2 (two demos) yes; L3 (6 h on 40 days) no: 33 of 40 days, one of them fever leave. |
| 3 | Describe one technical problem you solved. | HD-31: invoice totals differed by a paisa because float 0.565 rounds down; I used Decimal and rounded once; 6 tests pass. |
| 4 | Why did you use `Decimal`, not `float`? | Floats cannot represent most decimal fractions exactly; money needs exact decimal arithmetic. |
| 5 | What did you learn that you did not expect? | That reproduction and tests take more time than the fix itself, and that review comments are how a team teaches. |
| 6 | How did you handle confidential information? | I signed the NDA, kept secrets in environment variables, scanned diffs before commit, and reported one near-miss the same day. |
| 7 | What was your biggest mistake? | I asked a question after three hours stuck in week 1; I then adopted the 15-minute rule. |
| 8 | How did you work with your team? | Daily stand-up, ticket board, code review, pair work on difficult tasks. |
| 9 | What would you do differently? | Start the report in week 5, and write the hand-over page earlier. |
| 10 | Which skill is still weak? | Documentation, rated 3 of 5; next step is a hand-over page for each project. |
| 11 | How is the internship connected to your BCA subjects? | Database, programming, software engineering and professional communication all appeared in the work. |
| 12 | What are your next steps? | Build a portfolio from the anonymised work, apply for junior roles, and keep a weekly learning log. |

## 5.7 Eight habits that finish an internship well

1. **Start the report in week five.** Writing chapters as the work happens, with the log beside you, is faster and more accurate than writing everything in the last weekend. The report then becomes a polishing job. Students who wait often invent details and are caught in the viva.
2. **Make every claim point to evidence.** Link each sentence about work to a log date, ticket number or screenshot. Evidence turns a story into a proof and protects you from doubt. Examiners often ask "show me where it says that".
3. **Be honest about gaps.** State missed objectives, such as L3, and the lesson drawn. A report with no failures is suspected; a report that explains one calmly is trusted. The viva rewards the same honesty.
4. **Respect the NDA in the report.** Hide client names, remove data and describe methods instead. Ask your supervisor to read the draft before submission. A leaked detail in a public report can harm the firm and you.
5. **Keep slides simple and rehearse.** One idea per slide, large text, a chart instead of a paragraph, and two timed rehearsals. A short talk that fits in ten minutes shows control and respect for the panel.
6. **Prepare for the twelve questions.** Write short answers in your own words: claim, evidence, honest limit. Practise aloud with a friend. Never memorise a speech; examiners can tell, and they will ask a follow-up.
7. **Collect the paperwork early.** Certificate, evaluation form and supervisor signatures should be in hand a week before the deadline. People travel, offices close for festivals and stamps go missing. Early requests prevent late panic.
8. **Thank people and keep in touch.** Send a short thank-you message to your supervisor and team, connect on a professional network and share your portfolio piece (anonymised) with permission. Many first jobs come from the people who watched you work for eight weeks.

## Formula and fact sheet

| Item | Rule or fact |
|---|---|
| Report core | intro, organisation, plan, weekly summary, technical contribution, learning, conclusion, appendices |
| Page budget (example) | 40 pages; chapters 4 and 5 = 16 pages = 40% |
| Words per page | about 300, less with figures and tables |
| Presentation | 10 minutes, about 10 slides, one idea per slide |
| Viva answer | claim, evidence, honest limit |
| Self-assessment | before and after rating 1 to 5, each with one line of evidence |
| Paperwork | certificate, evaluation form, optional reference, requested in week 7 |

## Chapter summary

- The report is **specific, evidence-based and honest**; chapters 4 and 5 (your work) carry the most pages.
- Use a page budget, write from week five and cite log dates and ticket numbers.
- Reflect with a before-and-after self-assessment: mean 2.25 to 4.00 in the example, with one weak skill named.
- Request certificate, evaluation and reference early; thank people.
- A ten-minute talk tells one story; the viva rewards claim, evidence and an honest limit.

## Practice

1. List the eight parts of a standard internship report.
2. Why does the report need an appendix with the signed log?
3. In Section 5.2, what percentage of pages do chapters 4 and 5 carry?
4. Explain "claim, evidence, honest limit" with an example.
5. Compute the mean gain for ratings before 2, 3, 1 and after 4, 4, 3.
6. List the slide plan for a ten-minute presentation.
7. What three documents should you request from the host organisation, and when?
8. How should you handle client names in the report?
9. Write a short viva answer to "what was your biggest mistake?".
10. Why is a self-assessment with all fives weak?

::: note Answers and worked solutions
**1.** Introduction, organisation profile, plan and objectives, weekly summary, technical contribution, learning and ethics, conclusion, appendices.
**2.** It is the evidence that the work was done and the supervisor confirmed it.
**3.** 16 ÷ 40 = 40 percent.
**4.** "I fixed the VAT bug (claim); the six tests pass and the ticket is merged (evidence); I did not test on the production database (limit)."
**5.** Gains 2, 1, 2; mean = 5 ÷ 3 = **1.67**.
**6.** Title (1), objectives and plan (1), weekly chart (1), technical contribution (3), learning (2), thanks and future (1), questions (rest).
**7.** Completion certificate, college evaluation form, optional reference letter; ask in week 7.
**8.** Hide or replace names, describe method and say that this was done under the NDA.
**9.** "In week one I stayed stuck for three hours without asking; I then used the 15-minute rule and my speed improved."
**10.** It shows no honest reflection and no evidence; examiners will doubt the whole report.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Describe the structure of an internship report and the content of each chapter.**

*Introduction.* An internship report is the written proof of the placement. Colleges set their own template, but the core structure is common (Figure 5.1).

*Chapters.*

1. **Introduction:** purpose, duration and SMART objectives.
2. **Organisation profile:** the firm's work, structure and tools, in the intern's own words.
3. **Plan and objectives:** the eight-week plan chart and expected outcomes.
4. **Weekly summary:** one paragraph per week with hours and tasks, from the log.
5. **Technical contribution:** one or two tickets in depth: problem, fix, tests, result.
6. **Learning, problems and ethics:** skills gained, difficulties and confidentiality.
7. **Conclusion:** outcome against each objective and recommendations.
8. **Appendices:** signed log, supervisor letter, hand-over page.

*Quality rules.* Be specific, point every claim to evidence, avoid copying the company website, and respect the NDA. *Conclusion.* A report built from the log is mostly assembly and is easy to defend.

**Q2 (5 marks). How should a student prepare for the internship viva? Give four model questions with answers.**

*Introduction.* The viva tests whether the student did the work and understood it. Preparation consists of knowing the evidence, practising answers and being honest.

*Method.* Answer in three parts: **claim, evidence, honest limit**. Rehearse aloud with a friend, and prepare the numbers (hours, tickets, test results) in advance.

*Four model questions.*

1. **Role?** "Web-development intern on the billing module under Sanjay."
2. **Technical problem?** "HD-31: float 0.565 rounds down; I used `Decimal` and rounded once; six tests pass."
3. **Objective missed?** "L3: 33 of 40 days reached six hours; one day was fever leave; I would now write a 90-percent target."
4. **Weak skill?** "Documentation, 3 of 5; next step is a hand-over page for each project."

*Conclusion.* Honest, evidence-based answers show ownership; bluffing is the quickest way to lose marks.

**Q3 (10 marks). Explain how a BCA student should complete an internship by preparing the report, presentation and viva, and describe the role of reflection and evidence.**

*Introduction.* The final stage turns eight weeks of work into marks. A student who collected evidence during the placement (Units 1 to 4) finishes quickly and with confidence. The stage has four tasks: report, presentation, viva and relationships.

*Report.*

1. **Plan the pages.** A 40-page budget gives chapters 4 and 5 the largest share (16 pages, 40 percent).
2. **Write from week five.** Use the log as the source.
3. **Cite evidence.** Dates, ticket numbers, screenshots, signed pages.
4. **Respect the NDA.** Hide names and describe methods.

*Reflection.*

5. **Self-assessment.** Rate eight skills before and after (mean 2.25 to 4.00), add one line of evidence each and name the weak skill (Documentation).

*Presentation and viva.*

6. **Ten-minute talk.** One slide per minute, a weekly chart, the HD-31 story and the skills chart; rehearse twice.
7. **Viva.** Prepare twelve questions; answer with claim, evidence, honest limit.

*Relationships.*

8. **Paperwork and thanks.** Request the certificate, evaluation and reference in week 7; thank the team and stay connected.

| Task | Output | Evidence |
|---|---|---|
| Report | 40 pages | log, tickets, signed letter |
| Reflection | skills table | before and after ratings |
| Presentation | 10 slides | weekly chart, demo screenshot |
| Viva | 12 answers | claim, evidence, limit |
| Network | certificate, reference | signed documents |

*Example.* Anisha's report cites log day 12 for HD-31, shows 6 of 6 tests passing and admits that L3 was missed; her viva answers are short and specific, and her supervisor's letter closes the file. *Conclusion.* An internship is finished well when evidence, honesty and thanks are all in place; the habits it builds will matter in every later job.
