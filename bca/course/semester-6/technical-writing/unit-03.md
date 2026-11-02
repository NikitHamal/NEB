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
