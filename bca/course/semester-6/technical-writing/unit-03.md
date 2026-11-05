---
subject: Technical Writing
grade: BCA Semester 6
unit: 3
title: Software Documentation - SRS, README, API Reference, Runbooks and Postmortems
hours: 9
area: BCA 354 · Technical Writing · Unit 3
---

Software dies without documentation: the developer who understood it leaves, the customer cannot use it, the next engineer cannot change it, and the on-call person cannot fix it at 3 a.m. Different readers need different documents, written at different times. This unit tours the documents of a software project, **requirements specifications (SRS)**, **README files**, **user guides**, **API reference with OpenAPI**, **runbooks**, **postmortems** and the small texts (commit messages, release notes, error messages) that carry as much weight as the big ones. Two small programs are included and executed: a **requirement linter** that flags vague and non-testable statements, and an **OpenAPI checker** that finds missing summaries and undocumented error responses.

::: key What this unit gives you
- The map of software documents: audience, content and when each is written.
- Writing good requirements (shall statements, testable, unambiguous) with an executed linter.
- README, tutorials, user guides, API documentation and OpenAPI with an executed checker.
- Runbooks, postmortems, commit messages, release notes and error messages; docs as code.
:::

## 3.1 The documents of a software project

| Document | Reader | Purpose | Written when |
|---|---|---|---|
| **SRS** (software requirements specification) | Client, analysts, testers, developers | Agree what the system must do | Analysis |
| **Design document** | Developers, reviewers | Explain architecture and decisions (ADRs) | Design |
| **README** | New users and contributors | What it is, how to install and run | From day one |
| **User guide / tutorial** | End users | Learn tasks | Before release |
| **API reference** | Developers using the API | Exact behaviour of each endpoint or function | With the code |
| **Test plan and report** | Testers, managers | What was tested, results | Testing |
| **Runbook / operations guide** | On-call and operators | Steps to deploy, monitor, recover | Before production |
| **Postmortem** | Team, management | Learn from an incident | After an incident |
| **Release notes / changelog** | Users, support | What changed, upgrade steps | Each release |

The *four kinds* of documentation (the Diátaxis framework) differ in purpose: **tutorials** (learning-oriented: a guided lesson), **how-to guides** (task-oriented: steps to a goal), **reference** (information-oriented: facts, complete and accurate) and **explanation** (understanding-oriented: why and background). Mixing them in one page is a common reason documents fail: a tutorial that stops to explain theory loses the learner; a reference page padded with narrative slows the expert.

## 3.2 Writing requirements

An **SRS** states what the system shall do and the constraints on it. A good requirement is **necessary, unambiguous, testable, singular (one thing), feasible and consistent**. The standard of language: **"shall"** marks a mandatory requirement, "should" a recommendation, "may" an option, "will" a statement of fact or a future action of someone else. Typical structure (IEEE 830/29148 style): introduction (purpose, scope, definitions), overall description (users, environment, assumptions), **functional requirements** (numbered: FR-1…), **non-functional requirements** (performance, security, usability, reliability, portability), interfaces, and a requirements **traceability** matrix.

Bad: "The system should be fast and user-friendly." Why: *fast* and *user-friendly* cannot be tested. Good: "The system shall return search results within 2 seconds for at least 95% of requests with up to 100 concurrent users." Bad: "The system shall support reports, graphs, etc." (*etc.* hides the scope.) Good: "The system shall export the monthly attendance report as PDF and CSV." Bad: "The system shall validate and store the data and notify the administrator." (three requirements in one: split them.) Weak words to avoid: *fast, easy, user-friendly, flexible, adequate, as appropriate, and/or, etc., approximately, if possible, support* (without saying what).

The program below is a tiny linter that implements two of these checks: a requirement must contain "shall" and must not contain a weak word. (Real tools also look for passive voice, negatives and compound sentences.)

```python
WEAK = ["fast", "user-friendly", "easy", "as appropriate", "etc", "and/or", "flexible", "adequate"]
reqs = [
    "The system shall respond to a search within 2 seconds for 95% of requests.",
    "The interface should be fast and user-friendly.",
    "The system shall support reports, graphs, etc.",
    "A citizen shall be able to download a certificate in PDF.",
]
for i, r in enumerate(reqs, 1):
    hits = [w for w in WEAK if w in r.lower()]
    ok = "shall" in r.lower() and not hits
    print("R%d: %s %s" % (i, "PASS" if ok else "FAIL", hits))
```
```output
R1: PASS []
R2: FAIL ['fast', 'user-friendly']
R3: FAIL ['etc']
R4: PASS []
```
R1 and R4 pass; R2 fails because it uses *should* and the weak words *fast* and *user-friendly*; R3 fails on *etc*. Each requirement also needs a **unique ID**, a **priority** (must/should/could), a **source** (who asked), and a **verification method** (test, inspection, demonstration, analysis) so that it can be traced to a test.

## 3.3 README files, tutorials and user guides

The **README** is the front door of a project: a reader decides in 30 seconds whether to continue. A good one has: a **title and one-sentence description** (what it does and for whom); a **screenshot or short example**; **requirements**; **installation** (copy-paste commands); **quick start** (the shortest path to a visible result); **usage** and configuration; **how to run the tests**; **how to contribute**; **licence**; **contact and support**. Test the install commands on a clean machine every release: outdated instructions are the commonest documentation bug.

A **user guide** is organised by tasks and written in the imperative. A good procedure: a heading naming the goal ("Print a certificate"); a sentence on when and why; prerequisites; numbered steps with one action each, naming interface elements exactly as they appear (**File > Print**), with the expected result and screenshots where they save words; a "if something goes wrong" note; related tasks. **Error messages** are documentation too: say *what happened*, *why* (if known) and *what to do*: "Cannot save the file: the disk is full. Free some space or choose another folder." Avoid codes alone, blame ("You entered an invalid value") and jokes.

## 3.4 API documentation and OpenAPI

An API's reference tells a developer, for each endpoint or function: the purpose, the **request** (method, path, parameters, body schema), the **responses** (status codes, body schema, examples), **errors**, **authentication**, **rate limits** and **versioning**. Examples are the most-read part: provide a complete working request and response. Describing it in a machine-readable form, the **OpenAPI Specification** (formerly Swagger), lets tools generate interactive documentation, client libraries and tests, and lets you *check* the documentation automatically.

The program below parses a small OpenAPI document and applies three checks: every operation has a `summary`; every operation documents at least one `4xx` error response; and every `{path}` parameter in the URL is declared as a path parameter.

```python
import json
import re

spec = json.loads("""{
 "openapi": "3.0.3",
 "info": {"title": "Ward Services API", "version": "1.0.0"},
 "paths": {
  "/certificates": {
   "get": {"summary": "List certificates", "responses": {"200": {"description": "OK"}}},
   "post": {"responses": {"201": {"description": "Created"}}}
  },
  "/certificates/{id}": {
   "get": {"summary": "Get one certificate",
           "parameters": [{"name": "id", "in": "path", "required": true}],
           "responses": {"200": {"description": "OK"}, "404": {"description": "Not found"}}}
  }
 }
}""")

problems = []
count = 0
for path, ops in spec["paths"].items():
    for method, op in ops.items():
        count += 1
        tag = method.upper() + " " + path
        if "summary" not in op:
            problems.append(tag + ": missing summary")
        if not any(code.startswith("4") for code in op["responses"]):
            problems.append(tag + ": no 4xx response documented")
        for name in re.findall(r"\{(\w+)\}", path):
            if not any(p["name"] == name and p["in"] == "path" for p in op.get("parameters", [])):
                problems.append(tag + ": path parameter " + name + " not declared")

print(len(spec["paths"]), "paths,", count, "operations")
for p in problems:
    print(p)
```
```output
2 paths, 3 operations
GET /certificates: no 4xx response documented
POST /certificates: missing summary
POST /certificates: no 4xx response documented
```
Three of the four findings are the ones documentation reviews catch constantly: the list endpoint never says what an error looks like; the POST has no summary and no error responses. The `{id}` endpoint passes all checks. Fix the document, run the check in your continuous-integration pipeline, and the reference stays honest. (Full validators such as Spectral and the OpenAPI schema check far more; this shows the principle that *documentation can be tested like code*.)

## 3.5 Runbooks and postmortems

A **runbook** is the operations manual for a service: what it is, its dependencies, how to deploy and roll back, dashboards and alerts, and, for each alert, a **step-by-step response**. It is written for a tired person at night: short numbered steps, exact commands that can be copy-pasted, expected output, decision points ("if the disk is above 90%, go to step 6"), and an escalation contact. Keep it in the repository and test it by *following it* in an exercise.

A **postmortem** (incident review) records an incident to learn, not to blame. The **blameless** format has: **summary** (impact in one paragraph: what, how long, how many users); **timeline** (times in one time zone, from detection to resolution); **root cause(s)** (the chain of causes, not "human error"); **what went well / badly / where we were lucky**; **action items** (each with an owner and a due date, specific and testable); and **lessons**. Write it within a few days while memories are fresh. A vague postmortem ("be more careful") changes nothing; "add a pre-deployment check that fails if the migration lacks a rollback, owner: Sita, due 15 Jestha" does.

## 3.6 The small documents

- **Commit messages:** a subject line of up to about 50 characters in the imperative ("Fix login timeout on slow networks"), a blank line, then a body explaining *why*, not what. They form the history future maintainers read.
- **Code comments:** explain *why* and non-obvious constraints, not what the code plainly says; keep them true. Names and structure are the first documentation.
- **Release notes / changelog:** group by *Added, Changed, Fixed, Removed, Security*, linked to issues, with upgrade instructions and breaking changes first.
- **Architecture decision records (ADRs):** short documents with context, decision, consequences.
- **Emails and chat messages** to technical colleagues: subject that says the action ("Decision needed by Fri: choose backup vendor"), the ask in the first line, then context, then links.

**Docs as code:** store documentation (Markdown, reStructuredText, AsciiDoc) in version control beside the code, review it in pull requests, build it automatically (static site generators such as MkDocs or Sphinx), and run link checkers and linters in the pipeline. Treat out-of-date documentation as a bug.

## 3.7 Seeing the ideas: the four kinds of documents and the life of an incident

```photogrid label="3.1" cols="3" ratio="1.0" caption="Software documents are written for people in real places. (a) Source code on a screen: the README and inline comments sit next to it and explain what the code cannot. (b) A server rack: the runbook is the text an on-call engineer reads here at 2 am. (c) A stand-up briefing: the short, dated notes that feed minutes and postmortems."
@ photo id="bca306/code" cap="Code on a screen"
fit 1.0
focus 0.5 0.5
@ photo id="bca306/rack" cap="Server rack"
fit 1.0
focus 0.5 0.5
@ photo id="bca105/scrum" cap="Team briefing"
fit 1.0
focus 0.5 0.5
```

```svgfig label="3.1" caption="The four kinds of documentation (Diátaxis). Each answers a different question for a different reader mood; mixing them in one page is the commonest reason a manual feels confusing."
f = Fig(580, 250)
Q = [(14, 14, "Tutorial", "learning-oriented", "A guided first lesson:\nbuild a tiny working\nexample step by step.", MINT, TEAL), (296, 14, "How-to guide", "task-oriented", "Steps to reach a goal:\n\"Print a certificate\",\n\"Roll back a release\".", BLUE, NAVY), (14, 132, "Explanation", "understanding-oriented", "Why it works this way:\nbackground, design\nchoices, trade-offs.", SAND, AMBER), (296, 132, "Reference", "information-oriented", "Complete, accurate facts:\nAPI endpoints, options,\nerror codes.", ROSE, RED)]
for x, y, t, s, d, fl, st in Q:
    f.box(x, y, 270, 108, "", fill=fl, stroke=st)
    f.text(x + 135, y + 20, t, size=14, color=NAVY, bold=True)
    f.text(x + 135, y + 38, s, size=11, color=st, italic=True)
    f.text(x + 135, y + 74, d, size=11.5, color=SLATE)
f.text(290, 124, "study", size=10, color=SLATE, italic=True)
f.text(290, 242, "work", size=10, color=SLATE, italic=True)
```

```svgfig label="3.2" caption="Anatomy of a good requirement and the timeline of a blameless postmortem. (a) One requirement has an ID, a priority word, a measurable condition and a way to test it. (b) The incident story is written in clock times so the reader can see detection and recovery delay."
f = Fig(580, 250)
f.box(14, 10, 552, 30, "R7 | The system shall display the result page within 3 seconds for 95% of requests at 200 users.", fill=BLUE, stroke=NAVY, size=11)
P = [(14, 52, 80, "R7", "unique ID"), (100, 52, 80, "shall", "priority word"), (186, 52, 150, "within 3 seconds", "measurable limit"), (342, 52, 110, "95% of requests", "how often"), (458, 52, 108, "at 200 users", "test condition")]
for x, y, w, t, d in P:
    f.arrow([(x + w / 2, 42), (x + w / 2, 62)], color=TEAL)
    f.box(x, y + 12, w, 32, t, fill=MINT, stroke=TEAL, size=10.5, bold=True)
    f.text(x + w / 2, y + 58, d, size=10, color=SLATE, italic=True)
f.line(40, 190, 540, 190, color=SLATE, sw=2)
T = [(40, "14:02", "deploy"), (150, "14:09", "alerts fire"), (260, "14:20", "rollback"), (370, "14:31", "recovered"), (500, "next day", "review")]
for x, t, d in T:
    f.circle(x, 190, 6, fill=AMBER, stroke=RED)
    f.text(x, 172, t, size=11, color=NAVY, bold=True)
    f.text(x, 214, d, size=10.5, color=SLATE)
f.text(290, 242, "(b) detection 7 min, recovery 29 min after the deploy", size=10.5, color=SLATE, italic=True)
f.text(290, 148, "(a) requirement parts above", size=10, color=SLATE, italic=True)
```

### 3.7.1 Eight reasons to document software properly

1. **New people start quickly.** A good README and setup guide let a new teammate run the project in an hour instead of a week. A student joining a college project team can then contribute on day one. The cost of writing the guide is paid back every time someone joins.
2. **Requirements stop arguments.** A numbered, testable requirement such as "R7: results within 3 seconds for 95% of requests" is the same for the client and the developer. When the system is delivered, both sides can check it. Vague words like "fast" or "user-friendly" cause disputes.
3. **Maintainers understand the design.** Software lives for years, and the author may have left. Short design notes explain why a choice was made, for example why a ConnectIPS-style payment callback is retried three times. Without them the next developer breaks something that was done on purpose.
4. **APIs can be used without asking.** A clear reference with examples, error codes and a try-it page lets another team call your service by themselves. A school management system can then connect to the Tribhuvan University EMIS format without a meeting. Missing error documentation is the most common gap.
5. **Incidents are solved faster.** A runbook tells the on-call engineer what an alert means and which steps to follow. At 2 am nobody remembers rarely used commands, so a tested checklist shortens downtime. It also lets a junior engineer handle a fault safely.
6. **Teams learn from failures.** A blameless postmortem records what happened, the timeline and the actions that follow. The goal is to fix the process, not to punish a person. Banks and telecom companies in Nepal keep such reviews so the same outage does not repeat.
7. **Users succeed without support.** A task-based user guide with numbered steps and screenshots answers questions before they reach the help desk. A Nagarik App guide for renewing a document in six steps saves thousands of calls. Fewer calls mean lower cost and happier users.
8. **Audits and handovers are possible.** Many clients, banks and government offices ask for documents before accepting a system: SRS, test report, user manual and deployment guide. A project without them cannot be handed over or audited. Good documentation is therefore part of the deliverable, not an extra.

## Chapter summary

- Each document serves a reader at a time: SRS (agree), README (start), guide (do), reference (look up), runbook (respond), postmortem (learn).
- Requirements use "shall", one idea each, with testable numbers; vague words (fast, user-friendly, etc.) are defects; a linter can flag them.
- A README gets a reader to a first success in minutes; user guides are task-based numbered procedures; error messages say what, why and what to do.
- OpenAPI makes API documentation machine-checkable; the example checker found missing summaries and undocumented 4xx responses.
- Runbooks give exact steps for on-call; blameless postmortems end in owned, dated action items.

## Practice

1. Give the reader and purpose of an SRS, a README and a runbook.
2. Rewrite "The system should be easy to use" as a testable requirement.
3. Why is "The system shall validate and store the data and notify the admin" a poor requirement?
4. List five sections of a good README.
5. Rewrite the error message "Error 1045" as a helpful message for a failed database login.
6. What are the four kinds of documentation in the Diátaxis framework?
7. List three checks the example OpenAPI program performs.
8. What are the parts of a blameless postmortem?
9. Write a good commit message subject for a change that stops the app crashing when the phone number field is empty.
10. What does "docs as code" mean?

::: note Answers and worked solutions
**1.** SRS: client, analysts, testers; to agree on what the system shall do. README: new users and contributors; to explain, install and start the project. Runbook: on-call operators; to respond to alerts and operate the service.
**2.** For example: "A first-time clerk shall be able to register a new citizen record in under 3 minutes without help, measured in a usability test with five users."
**3.** It bundles three requirements (validate, store, notify) into one, so it cannot be tested or traced separately.
**4.** Title and description, requirements, installation, quick start, usage, tests, contributing, licence, support (any five).
**5.** "Cannot log in to the database: the user name or password is incorrect. Check your credentials in Settings > Database."
**6.** Tutorials, how-to guides, reference, explanation.
**7.** Each operation has a summary; each documents at least one 4xx response; each path parameter is declared.
**8.** Summary and impact, timeline, root causes, what went well and badly, action items with owners and dates, lessons.
**9.** "Prevent crash when phone number is empty" (imperative, under about 50 characters).
**10.** Keeping documentation in version control with the code, reviewing and building it automatically, and testing it like software.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What makes a good software requirement? Rewrite a poor requirement.**

*Introduction.* A **requirement** states what a system must do or the quality it must have. It becomes a contract between the client and the developer, so it must be checkable (Figure 3.2a).

*Qualities.* A good requirement is **unique** (has an ID), **clear** (one meaning), **testable** (a measurable condition), **necessary**, **feasible** and **consistent** with the others. It uses *shall* for a must and avoids weak words such as *fast*, *user-friendly*, *etc.*, *and/or* and *as appropriate*.

*Linter result from the book's program.*

| ID | Result | Reason |
|---|---|---|
| R1 | PASS | clear and measurable |
| R2 | FAIL | uses "should"; weak words *fast*, *user-friendly* |
| R3 | FAIL | uses *etc* |
| R4 | PASS | clear and measurable |

*Rewrite.* Poor: "The system should be fast and user-friendly." Good: "R7: The system shall display the result page within 3 seconds for 95% of requests at 200 concurrent users." The fixed version has an ID, *shall*, a number, a proportion and a test condition. *Conclusion:* a requirement that cannot be tested cannot be accepted or rejected.

**Q2 (5 marks). Explain the four kinds of documentation (tutorial, how-to guide, reference, explanation).**

*Introduction.* The Diátaxis framework says that documentation serves four different needs, and each kind should be written differently (Figure 3.1).

1. **Tutorial** (learning-oriented): a guided lesson for a beginner, building a small working example. It must work every time, so the author tests each step.
2. **How-to guide** (task-oriented): numbered steps for a competent user with a goal, such as "Roll back a release". It starts with the goal and prerequisites and leaves out theory.
3. **Reference** (information-oriented): complete, accurate and consistent facts, such as every endpoint, parameter and error code. It is for looking up, not reading in order.
4. **Explanation** (understanding-oriented): the why, covering design choices, trade-offs and background.

| Kind | Reader needs | Style | Example |
|---|---|---|---|
| Tutorial | to learn | friendly, step by step | "Build your first API call" |
| How-to | to do a task | imperative, short | "Print a certificate" |
| Reference | to look up | dry, complete | OpenAPI file |
| Explanation | to understand | discursive | "Why we retry payments" |

*Conclusion.* Keeping the four kinds separate stops a tutorial from turning into a reference and makes each page easier to use.

**Q3 (10 marks). Describe the major documents of a software project (SRS, README, API reference, runbook, postmortem). Explain how each is written and checked.**

*Introduction.* A software project produces several documents, each for a different reader and moment. Together they carry the knowledge that code cannot (Plate 3.1 and Figure 3.2).

*1. SRS (Software Requirements Specification).* Written at the start for clients and developers. It has purpose, scope, users, functional requirements, non-functional requirements (performance, security, usability) and constraints. Each requirement has a unique ID, priority, a measurable condition and a test. *Check:* a **requirement linter** flags weak words (*fast*, *etc*, *should*) as the program in 3.2 does; a review confirms that every requirement is traceable to a test.

*2. README.* The front door: title and one-line description, a screenshot, install and run steps, a minimal example, configuration, licence and contact. A reader decides in 30 seconds whether to continue. *Check:* follow the steps on a clean machine.

*3. User guide.* Organised by tasks, in the imperative, with prerequisites, numbered steps, expected results and troubleshooting. *Check:* usability test with five real users.

*4. API reference (OpenAPI).* Lists each path, operation, parameter, request and response schema, and every error. It should include examples and authentication. *Check:* an OpenAPI **checker** such as the one in 3.4 reports gaps, for example "GET /certificates: no 4xx response documented" and "POST /certificates: missing summary".

*5. Runbook.* The operations manual of a service: dependencies, deploy and rollback, dashboards, and a step-by-step response for each alert, written so a tired engineer can follow it. *Check:* a game day or drill where someone unfamiliar follows it.

*6. Postmortem.* A blameless incident review with summary (impact), timeline in clock times, root cause, what went well and badly, and dated action items with owners (Figure 3.2b). *Check:* each action item has an owner and a date and is tracked to closure.

*Comparison.*

| Document | Reader | When | Main check |
|---|---|---|---|
| SRS | client, developer | start | linter and review |
| README | new user | always | clean-machine run |
| User guide | end user | release | usability test |
| API reference | integrator | release | OpenAPI checker |
| Runbook | on-call engineer | operations | drill |
| Postmortem | whole team | after incident | action-item follow-up |

*Conclusion.* Each document has one reader, one purpose and one test. Writing them for that reader, and checking them with tools and real people, makes software maintainable and handover possible.
