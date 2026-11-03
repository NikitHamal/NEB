---
subject: Project II
grade: BCA Semester 5
unit: 5
title: Documentation, Demo, Report and Viva for Project II
area: BCA 306 · Project II · Unit 5
---

The last unit turns the finished system into marks. A web project is judged on the running demo, on the written report and on how well you can explain your choices in the viva. This unit shows what to document, how to prepare a 10-minute demo that survives a bad network, how to organise the report, and gives twelve viva questions specific to a web project.

::: key What this unit gives you
- The report structure with a figure, and what evidence each chapter must contain.
- API documentation generated from a route table, so docs and code cannot drift apart.
- A timed 10-minute demo script with a fallback plan.
- Twelve viva questions with short answers, and eight habits of students who score well.
:::

## 5.1 The report: what goes where

TU project reports follow a common pattern; **your college's template always wins**. The pattern fits a web project like this.

```svgfig label="5.1" caption="Map of a Project II report. Early chapters justify the project, middle chapters show the design and the build, late chapters give the evidence. Evidence from Units 2 to 4 (API replies, test table, capacity numbers) goes into chapters 5 and 6."
f = Fig(560, 170)
ch = [("1 Intro", "problem, objectives, scope"), ("2 Analysis", "stories, feasibility"), ("3 Design", "architecture, ER, REST"), ("4 Build", "code, security"), ("5 Test", "cases, defects, load"), ("6 Deploy", "pipeline, backup")]
for i, (t, d) in enumerate(ch):
    x = 6 + i * 92
    f.box(x, 30, 84, 44, t, fill=BLUE if i % 2 == 0 else SOFT, stroke=NAVY, size=11, color=NAVY)
    f.text(x + 42, 92, d.split(",")[0], size=9, color=NAVY)
    f.text(x + 42, 104, d.split(",")[1].strip(), size=9, color=NAVY)
f.arrow([(48, 120), (510, 120)], color=TEAL)
f.text(280, 140, "Each claim in the early chapters is proved by a table or figure in the later ones", size=11, color=NAVY)
f.text(280, 158, "Front matter: title, certificate, abstract, contents  |  Back matter: conclusion, references, appendices", size=9.5, color=NAVY)
```

| Chapter | What the examiner looks for | ClinicQ evidence |
|---|---|---|
| 1 Introduction | a numbered problem and SMART objectives | O1 to O5 table |
| 2 Analysis | user stories ranked by MoSCoW, feasibility | Section 1.6 table |
| 3 Design | three-tier figure, ER diagram, REST table | Figures 1.1, 2.1, table 1.5 |
| 4 Implementation | key code and the reasons for choices | API listing, hashing, token |
| 5 Testing | test-case table, defect log, load estimate | T1 to T10, capacity script |
| 6 Deployment | pipeline, configuration, backup | Figure 4.1, service and Nginx files |
| 7 Conclusion | objectives met or not, with numbers, and future work | O1 to O5 verdicts |

## 5.2 API documentation that cannot go out of date

An API that only its author understands is not finished. Keep one **route table** in the code and generate the documentation from it. The program below prints the Markdown table that goes into the report appendix; when a route changes, you re-run it and the document changes with it.

```python
routes = [
    ("POST", "/api/patients", "none", "201, 400", "register a patient"),
    ("POST", "/api/login", "none", "200, 401, 429", "exchange password for a token"),
    ("POST", "/api/tokens", "clerk", "201, 404", "issue the next token"),
    ("GET", "/api/tokens", "none", "200", "list today's queue"),
    ("PATCH", "/api/tokens/{id}", "nurse", "200, 401, 403, 404, 422", "mark a token served or cancelled"),
]
print("| Method | URL | Role | Codes | Purpose |")
print("|---|---|---|---|---|")
for m, u, r, c, p in routes:
    print(f"| {m} | `{u}` | {r} | {c} | {p} |")
protected = [u for m, u, r, c, p in routes if r != "none"]
print()
print(len(routes), "routes,", len(protected), "protected:", ", ".join(protected))
```
```output
| Method | URL | Role | Codes | Purpose |
|---|---|---|---|---|
| POST | `/api/patients` | none | 201, 400 | register a patient |
| POST | `/api/login` | none | 200, 401, 429 | exchange password for a token |
| POST | `/api/tokens` | clerk | 201, 404 | issue the next token |
| GET | `/api/tokens` | none | 200 | list today's queue |
| PATCH | `/api/tokens/{id}` | nurse | 200, 401, 403, 404, 422 | mark a token served or cancelled |

5 routes, 2 protected: /api/tokens, /api/tokens/{id}
```
Besides the table, every project needs a **README** with: what the system does in two sentences, how to install and run it in numbered steps, the environment variables it needs (names only), how to run the tests, a screenshot, and the licence. A stranger should be able to run the project from a clean clone using only the README; examiners sometimes try exactly that.

## 5.3 Preparing the 10-minute demo

A demo is a story told with a running system. Rehearse it with a stopwatch until it fits. Use test data that you created in advance, so that nothing depends on typing during the demo.

```python
plan = [("Problem and objectives", 1.0), ("Architecture figure", 1.0), ("Live: register, issue token, public queue", 3.0),
        ("Live: login, serve token, wrong-role 403", 2.0), ("Security and test evidence", 1.5), ("Deployment and conclusion", 1.0)]
total = sum(m for _, m in plan)
for name, m in plan:
    print(f"{m:4.1f} min  {name}")
print(f"total {total:.1f} min, spare {10 - total:.1f} min for questions")
```
```output
 1.0 min  Problem and objectives
 1.0 min  Architecture figure
 3.0 min  Live: register, issue token, public queue
 2.0 min  Live: login, serve token, wrong-role 403
 1.5 min  Security and test evidence
 1.0 min  Deployment and conclusion
total 9.5 min, spare 0.5 min for questions
```
```photogrid label="5.1" cols="2" ratio="1.4" caption="Plan for things going wrong. (a) A technician troubleshoots a live server with a laptop on the floor of a machine room: real systems fail, and the professional response is a checklist, not panic. (b) The demo timeline to scale: the live parts take 5 of the 9.5 planned minutes, and 0.5 minutes are spare."
@ photo id="bca306/tech" cap="Fixing a live system"
fit 1.4
focus 0.55 0.5
call 0.5 0.9 0.5 0.72 "Calm checklist"
@ svg cap="Demo timeline (minutes)"
f = Fig(330, 200)
items = [("Problem", 1.0, BLUE), ("Architecture", 1.0, SOFT), ("Live 1", 3.0, BLUE), ("Live 2", 2.0, SOFT), ("Evidence", 1.5, BLUE), ("Deploy", 1.0, SOFT)]
x = 15
for n, m, c in items:
    w = m * 30
    f.box(x, 50, w - 2, 44, n, fill=c, stroke=NAVY, size=9, color=NAVY)
    x += w
f.line(15, 110, 315, 110, color=NAVY)
f.text(165, 128, "0 ................................ 9.5 min", size=10, color=NAVY)
f.box(15, 150, 300, 36, "Fallback: recorded video + screenshots ready", fill=SOFT, stroke=RED, size=11, color=NAVY)
```

**Fallback plan.** Keep a local copy of the system on your laptop, a 3-minute screen recording and a folder of screenshots. If the network fails, say so calmly, switch to the local copy and continue; examiners mark the quality of your explanation, not the quality of the Wi-Fi.

## 5.4 Twelve viva questions for a web project

| # | Question | Short answer |
|---|---|---|
| 1 | Why a three-tier design? | Browser, logic and data can change and be secured separately; the browser never reaches the database. |
| 2 | Why REST and JSON? | Any client can use the same URLs; JSON is light and readable. |
| 3 | What does 201 mean and when do you use it? | Created; the reply to a successful POST that makes a resource. |
| 4 | What is the difference between 401 and 403? | 401: not logged in. 403: logged in but not allowed. |
| 5 | How do you store passwords? | Salted PBKDF2 hash with many rounds, compared in constant time. |
| 6 | What stops SQL injection? | Placeholders: input is data, never SQL text. |
| 7 | What if two clerks issue a token together? | `UNIQUE(day, no)` rejects the duplicate and the handler retries. |
| 8 | How does the token stop forgery? | An HMAC signature under a secret key; editing the role breaks it. |
| 9 | How many users can it carry? | About 25 requests per second per worker at 40 ms; the clinic needs 4 per second at peak. |
| 10 | What is in your test report? | 10 cases with expected and actual results and a defect log. |
| 11 | How is it deployed? | Git, tests, service restart, health check; Nginx with HTTPS in front. |
| 12 | What would you change with another month? | Add SMS notifications and an audit-log page; move to PostgreSQL and a framework such as Flask. |

If you do not know an answer, say so, then reason aloud from first principles. Examiners respect honest reasoning more than a memorised wrong answer.

## 5.5 Eight habits of students who score well

1. **Show numbers.** Every objective in the report has a measured result beside it: "token in 38 ms, objective was under 1 s". This turns opinion into evidence and shortens the viva because the examiner can read the proof.
2. **Own every line.** Each member can explain every module, not only their own. Rehearse by swapping modules in a mock viva. Examiners test this by asking a random member about a random file.
3. **Show the failure paths.** Demonstrate a 400, a 401 and a 403 on purpose. It proves that you designed for misuse, and examiners often type bad input anyway, so you control the moment.
4. **Keep the repository clean.** One README, a clear folder structure, small commits with meaningful messages and no secrets. The commit history tells the supervisor who did what and when, which is fair to every member.
5. **Write the report as you build.** After each unit's work, write that chapter while the details are fresh. Copying screenshots in the last week produces a report that does not match the running system.
6. **Be honest about limits.** A "Limitations and future work" section that says "no SMS, no mobile app, tested up to 600 watchers" is a mark of maturity. Claiming perfection invites the examiner to find the flaw.
7. **Prepare the room.** Arrive early, test the projector and the network, open the pages in tabs, and keep test data ready. Ten minutes of preparation prevents most demo disasters.
8. **Credit your sources.** List every library, image, tutorial and licence in the references. Under the Copyright Act of Nepal, 2059 (2002) and standard academic rules, copying without credit is plagiarism and costs far more than the marks you hoped to gain.

## Formula and fact sheet

- Report: front matter, 7 chapters (introduction to conclusion), references, appendices; the college template wins.
- Demo: 10 minutes, about half of it live; rehearse with a stopwatch; always have a fallback.
- API doc = generated from the route table; README = what, install, run, env names, tests, screenshot, licence.
- Objectives table: objective, how measured, result, verdict.

## Chapter summary

- The report proves every early claim with evidence in later chapters.
- Generated API documentation and a good README let a stranger use the system.
- A timed demo with a fallback survives load-shedding and network failures.
- Twelve viva questions cover architecture, REST, security, concurrency, testing and deployment.
- Honesty, numbers and shared understanding are what separate good projects from copied ones.

## Practice

1. List the chapters of a Project II report and one piece of evidence for each.
2. Why generate API documentation from the route table?
3. What must a README contain?
4. Plan a 10-minute demo for a bus-ticket system with times that add up.
5. What is a fallback plan and why is one needed?
6. Answer in two sentences: "Why 403 and not 401?"
7. A team shows an objective "fast response" in the report. Rewrite it as a measurable result.
8. Why should every member be able to explain every module?
9. Write the limitations section for ClinicQ in three bullets.
10. If the demo plan totals 11.5 minutes, what do you cut?

::: note Answers and worked solutions
**1.** Introduction: objectives table. Analysis: stories. Design: architecture figure. Implementation: code listing. Testing: test table. Deployment: pipeline. Conclusion: objective verdicts.
**2.** The document is rebuilt from the same source, so it cannot disagree with the code.
**3.** Purpose, install and run steps, environment variable names, how to test, screenshot, licence.
**4.** Problem 1, architecture 1, live booking 3, live cancel and 403 2, tests 1.5, deployment 1 = 9.5 minutes.
**5.** Recorded video, screenshots and a local copy; networks and power fail.
**6.** The user is known (logged in), so it is not an authentication failure; the action is not allowed for the role, which is 403.
**7.** "The slowest of 20 requests took 38 ms against an objective of 1 s."
**8.** The viva tests understanding, and a random question to any member shows who built what.
**9.** No SMS; tested only to 600 watchers; SQLite is single-writer so a larger deployment needs PostgreSQL or MariaDB.
**10.** Cut the architecture recap and shorten the live parts; never cut the failure-path demonstration.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Describe the structure of a project report for a web-based system.**

*Introduction.* A project report is the permanent record of the work; it must justify the project, show the design and prove the results.

*Structure.*

1. **Preliminary pages.** Title page, certificate, acknowledgement, abstract, table of contents and list of figures and tables.
2. **Introduction.** Problem statement with numbers, SMART objectives, scope and limitations.
3. **Analysis.** User stories, functional and non-functional requirements and feasibility.
4. **Design.** Three-tier architecture figure, ER diagram, REST API table, screen designs and security design.
5. **Implementation and testing.** Key code with reasons, test-case table with expected and actual results, defect log and a performance estimate.
6. **Deployment.** Pipeline, configuration, backup and checklist.
7. **Conclusion, references and appendices.** Objectives met or not, with numbers; future work; sources; API documentation and user manual.

*Example.* ClinicQ's report puts the objectives table (O1 to O5) in chapter 1 and the verdicts against the same table in chapter 7.

*Conclusion.* A report that links each objective to evidence is easy to mark and easy to defend.

**Q2 (5 marks). Explain how you would prepare and present a project demonstration.**

*Introduction.* A demonstration shows the examiner that the system works and that you understand it. It must be short, rehearsed and robust.

*Preparation.*

1. **Script.** Write a 10-minute plan: problem 1 minute, architecture 1, live happy path 3, live failure paths 2, security and tests 1.5, deployment and conclusion 1.
2. **Test data.** Create accounts and records in advance and reset them before each rehearsal.
3. **Rehearse.** Time it with a stopwatch; every member practises every part.
4. **Environment.** Check projector, network and browser tabs early; keep a local copy running.
5. **Fallback.** Prepare a recorded video and screenshots for network or power failure.

*Presentation.* Speak to the problem first, show the architecture figure, run the live parts, deliberately show a 400, 401 and 403, quote measured numbers and end with limits and future work.

*Conclusion.* Preparation turns a risky live event into a controlled story.

**Q3 (10 marks). Describe the complete process of documenting, presenting and defending a web-based final project, using ClinicQ as the example.**

*Introduction.* A project earns marks in three places: the written report, the live demonstration and the viva. A system that works but is not documented, presented and defended well scores poorly, so each part is planned.

*1. Documentation.* The report follows the college template and the common structure: preliminary pages, introduction, analysis, design, implementation, testing, deployment, conclusion, references and appendices (Figure 5.1). ClinicQ's chapter 1 states the problem with numbers (150 patients a day, 95-minute wait) and five SMART objectives. Later chapters carry the evidence: the REST table, the ER diagram, the 10-case test table, the capacity numbers and the pipeline.

*2. Generated API documentation and README.* A route table in the code generates the Markdown API table, so documentation matches the code. The README gives purpose, install steps, environment variable names, how to run tests, a screenshot and the licence, so a stranger can run the project.

*3. Demonstration.* A 10-minute script runs in this order: problem, architecture, live registration and token issue, login and serving a token, wrong-role 403, security and test evidence, deployment and conclusion. Test data is prepared; a stopwatch rehearsal fits the plan into 9.5 minutes. A recorded video and a local copy form the fallback.

*4. Viva preparation.* The team prepares answers to likely questions: why three tiers, why REST, status codes 401 and 403, password storage, SQL injection, duplicate tokens, token forgery, capacity, tests and deployment. Each member practises explaining every module, because examiners choose the person and the file at random.

*5. Honesty and limits.* The conclusion compares measured results with objectives O1 to O5 and lists limitations (no SMS, SQLite single-writer, tested to 600 watchers) and future work. All libraries, images and sources are credited to avoid plagiarism.

| Part | Output | Evidence |
|---|---|---|
| Report | bound document | objective table, figures, test table |
| Docs | API table, README | generated table, clean-clone start |
| Demo | 10-minute live show | timed script, fallback |
| Viva | oral defence | twelve prepared answers |

*Conclusion.* Documentation records the work, the demonstration shows it, and the viva proves understanding. Planning all three from the first week, with numbers as evidence and honesty about limits, is what the examiners reward.
