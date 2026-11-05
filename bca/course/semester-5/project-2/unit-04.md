---
subject: Project II
grade: BCA Semester 5
unit: 4
title: Testing, Performance and Deployment
area: BCA 306 · Project II · Unit 4
---

A web project that "works on my laptop" is only half finished. It must be tested so that the demo does not depend on luck, measured so that you know how many users it can serve, and deployed so that the examiner can open a URL. This unit gives a test plan, runnable automated tests, a capacity calculation and a deployment checklist.

::: key What this unit gives you
- The test pyramid and how unit, API and manual tests share the work.
- A runnable `unittest` suite for ClinicQ rules, with the real pass/fail result.
- A test-case table in the format examiners expect, with expected and actual results.
- A capacity calculation using arrival rate and response time, and a deployment pipeline with Nginx and systemd.
:::

## 4.1 What to test, and in what proportion

Testing a web system has levels. **Unit tests** check one function (is `98x` an invalid phone?). **API tests** call endpoints and check status codes and bodies. **End-to-end and manual tests** click through the real pages. Lower levels are fast and cheap, so you write many; higher levels are slow and fragile, so you write few. This shape is called the **test pyramid**.

```photogrid label="4.1" cols="2" ratio="1.4" caption="Testing is a discipline of small checks. (a) Source code on a developer's monitor: every function in it should have a test that fails when the function is wrong. (b) The test pyramid: many fast unit tests at the base, fewer API tests above them, and a few slow manual or end-to-end checks at the top."
@ photo id="bca306/code" cap="Code under test"
fit 1.4
focus 0.6 0.5
call 0.5 0.92 0.5 0.75 "Each line can hide a bug"
@ svg cap="The test pyramid"
f = Fig(330, 235)
f.poly([(165,14),(215,70),(115,70)], fill=BLUE, stroke=RED, label="Manual", lx=165, ly=52, size=10, color=NAVY)
f.poly([(110,78),(220,78),(262,140),(68,140)], fill=SOFT, stroke=AMBER, label="API tests: 15", lx=165, ly=112, size=11, color=NAVY)
f.poly([(62,148),(268,148),(318,222),(12,222)], fill=BLUE, stroke=TEAL, label="Unit tests: 60", lx=165, ly=188, size=12, color=NAVY)
f.text(165, 232, "slow and few (top) to fast and many (base)", size=9.5, color=NAVY)
```

## 4.2 Automated unit tests for the ClinicQ rules

The rules of ClinicQ that do not need a network can be tested as plain functions. The suite below checks phone validation, the next-token rule and the role check from Unit 3. Each test has a name that says what it proves.

```python
import unittest, io
def valid_phone(p): return isinstance(p, str) and p.isdigit() and len(p) == 10
def next_no(existing): return max(existing, default=0) + 1
def may(role, action): return {"public": {"read"}, "clerk": {"read", "issue"}, "nurse": {"read", "issue", "serve"}}.get(role, set()) >= {action}

class Rules(unittest.TestCase):
    def test_phone_ok(self):            self.assertTrue(valid_phone("9841000001"))
    def test_phone_letters(self):       self.assertFalse(valid_phone("98x1000001"))
    def test_phone_too_short(self):     self.assertFalse(valid_phone("98410"))
    def test_phone_not_text(self):      self.assertFalse(valid_phone(9841000001))
    def test_first_token_is_one(self):  self.assertEqual(next_no([]), 1)
    def test_next_after_gap(self):      self.assertEqual(next_no([1, 2, 7]), 8)
    def test_public_cannot_serve(self): self.assertFalse(may("public", "serve"))
    def test_nurse_can_serve(self):     self.assertTrue(may("nurse", "serve"))
    def test_unknown_role_denied(self): self.assertFalse(may("hacker", "read"))

suite = unittest.defaultTestLoader.loadTestsFromTestCase(Rules)
total = bad = 0
for t in suite:
    r = unittest.TestResult(); t.run(r); total += 1
    ok = r.wasSuccessful(); bad += (not ok)
    print(("PASS " if ok else "FAIL ") + t._testMethodName)
print(f"{total} tests, {bad} failed")
```
```output
PASS test_first_token_is_one
PASS test_next_after_gap
PASS test_nurse_can_serve
PASS test_phone_letters
PASS test_phone_not_text
PASS test_phone_ok
PASS test_phone_too_short
PASS test_public_cannot_serve
PASS test_unknown_role_denied
9 tests, 0 failed
```
Notice that the test names read like a specification. When you change a rule, the failing test tells you exactly which behaviour changed. Run the whole suite before every commit and, later, automatically on every push (Section 4.5).

## 4.3 The test-case table for the report

Examiners expect a table of test cases with **expected** and **actual** results. Write each case before you run it, then fill in the actual result and the verdict. These cases come from the real run in Unit 2.

| ID | Test | Input | Expected | Actual | Result |
|---|---|---|---|---|---|
| T1 | register valid patient | `Sita Gurung`, `9841000001` | 201 and an id | 201 `{'id': 1}` | Pass |
| T2 | reject letters in phone | phone `98x` | 400 | 400 | Pass |
| T3 | issue first two tokens | patient 1 twice | numbers 1 and 2 | 1 and 2 | Pass |
| T4 | unknown patient | patient 99 | 404 | 404 | Pass |
| T5 | mark served | status `served` | 200, 1 row updated | 200 `{'updated': 1}` | Pass |
| T6 | bad status | status `done` | 422 | 422 | Pass |
| T7 | parallel duplicate | two clerks, same read | numbers differ | 8 and 9 after retry | Pass |
| T8 | injection name | `nobody' OR '1'='1` | no rows leaked | `[]` | Pass |
| T9 | expired token | now after expiry | 401 | 401 expired | Pass |
| T10 | forged role | `nurse` edited into a clerk token | 401 | 401 bad signature | Pass |

A failing row is not a disgrace; it is a **defect** to log with steps to reproduce, severity and the fix commit. A report with ten passes and no defect history looks untested.

## 4.4 Performance: how many users can one server carry?

Performance is measured, not guessed. Two numbers matter: **throughput** (requests per second) and **response time** (seconds per request). **Little's law** links them: the average number of requests being served at once = arrival rate × average time per request. The script uses assumed figures that you must replace with your own measurements (for example from the `ab` or `wrk` load-testing tools).

```python
patients_per_day, busy_share, busy_minutes = 150, 0.30, 120
watchers, poll_seconds, service_ms = 60, 15, 40          # assumed: 40 ms per request on a small VPS
issue_rate = patients_per_day * busy_share / busy_minutes / 60           # token requests per second
poll_rate = watchers / poll_seconds                                      # queue-page refreshes per second
total = issue_rate + poll_rate
service_s = service_ms / 1000
print(f"token requests at peak : {issue_rate:.4f} per second")
print(f"queue refreshes at peak: {poll_rate:.2f} per second")
print(f"concurrent requests (Little's law): {total * service_s:.3f}")
cap = 1 / service_s
print(f"one worker can serve   : {cap:.0f} requests per second")
print(f"utilisation            : {total / cap:.1%}")
for users in (60, 600, 6000):
    print(f"{users:>5} watchers -> {users / poll_seconds / cap:.1%} of one worker")
cache_s = 5
print(f"with a {cache_s}-second cache the database sees at most {1 / cache_s:.1f} queue reads per second")
```
```output
token requests at peak : 0.0063 per second
queue refreshes at peak: 4.00 per second
concurrent requests (Little's law): 0.160
one worker can serve   : 25 requests per second
utilisation            : 16.0%
   60 watchers -> 16.0% of one worker
  600 watchers -> 160.0% of one worker
 6000 watchers -> 1600.0% of one worker
with a 5-second cache the database sees at most 0.2 queue reads per second
```
At peak the clinic needs about 4 requests per second, which is 16 % of one small worker, so the design is comfortable. The same arithmetic shows when to act: 600 watchers use 160 % of a worker, so you would add workers or a cache. A **cache** stores a recent answer and reuses it; with a 5-second cache the database sees at most 0.2 queue reads per second no matter how many people refresh the page.

## 4.5 Deployment: from your laptop to a URL

**Deployment** means running the tested code on a server where users can reach it. A typical student-grade pipeline has five stages, and each stage has a gate that stops a broken build.

```svgfig label="4.1" caption="A simple delivery pipeline for ClinicQ. Code is pushed to Git; automated tests run; if they pass, the new version is copied to the server and the service restarts behind Nginx. A failed test stops the line, so a broken version never reaches the demo server."
f = Fig(560, 150)
steps = [("git push", BLUE), ("run tests", SOFT), ("build / copy", BLUE), ("restart service", SOFT), ("health check", BLUE)]
for i, (n, c) in enumerate(steps):
    x = 10 + i * 110
    f.box(x, 45, 92, 46, n, fill=c, stroke=NAVY, size=11, color=NAVY)
    if i < 4: f.arrow([(x + 92, 68), (x + 110, 68)], color=NAVY)
f.arrow([(166, 91), (166, 125), (30, 125), (30, 91)], color=RED, dash=True)
f.text(98, 140, "tests fail: stop, fix, push again", size=10, color=RED)
f.text(460, 120, "health check = GET /api/health returns 200", size=10, color=NAVY)
```

The application runs as a **service** so that it starts at boot and restarts after a crash. On Linux that is a `systemd` unit; Nginx sits in front as the reverse proxy and handles HTTPS. These two files are the whole deployment of a small project (shown for reading, not executed here).

```ini
# /etc/systemd/system/clinicq.service
[Service]
User=clinicq
WorkingDirectory=/srv/clinicq
Environment=CLINICQ_SECRET=...        # from a protected file in real use
ExecStart=/srv/clinicq/venv/bin/gunicorn -w 2 -b 127.0.0.1:8000 app:app
Restart=on-failure
```

```nginx
# /etc/nginx/sites-available/clinicq
server {
    listen 443 ssl;
    server_name clinicq.example.edu.np;
    ssl_certificate     /etc/letsencrypt/live/clinicq.example.edu.np/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/clinicq.example.edu.np/privkey.pem;
    location /api/ { proxy_pass http://127.0.0.1:8000; }
}
```

Before the demo go through this checklist: HTTPS works; the secret is in the environment, not in Git; debug mode is off; the database file is backed up; `/api/health` answers 200; a clean clone of the repository starts with the README steps alone; and a printed screenshot set exists in case the college Wi-Fi fails.

## 4.6 Eight practices that make a project demo-proof

1. **Write the test with the feature.** A rule written today with one test costs five minutes; found broken in week 12 it costs a night. Name tests after the behaviour, such as `test_phone_letters`, so the list reads like a specification for the viva.
2. **Test the unhappy paths.** Blank input, wrong password, expired token and unknown id are what examiners type. Each should return a clean 4xx reply. A crash with a stack trace on screen is the most common way a good project loses marks.
3. **Measure before you claim.** Never write "the system is fast" in the report. Write "the slowest of 20 token requests took 38 ms on a 1 vCPU server". Numbers can be defended and numbers can be checked.
4. **Use the same steps every time.** Deploy by one script or one pipeline, not by hand. Manual steps are forgotten under pressure. A script also documents how the system is built for the next student.
5. **Keep configuration outside the code.** Ports, secrets and database paths come from environment variables. Then the same code runs on the laptop, the test server and the demo server without edits, and no secret reaches Git.
6. **Monitor and log.** A health URL, a request log and a simple uptime check tell you the system is down before the examiner does. Log time, route, status and duration, but never passwords or tokens.
7. **Back up and rehearse a restore.** Copy the database daily to another machine. Practise restoring it onto a clean server once, because a backup that was never restored is not proof of anything.
8. **Prepare a fallback.** Keep a recorded demo, screenshots and a local copy ready. Load-shedding or a failed Wi-Fi link in a Nepali college is common; a calm switch to the fallback shows maturity, not failure.

## Formula and fact sheet

- Little's law: concurrent requests = arrival rate × time per request.
- Capacity of one worker = 1 / service time; utilisation = arrival rate / capacity (keep below about 70 %).
- Test pyramid: many unit tests, fewer API tests, few manual tests.
- A test case has ID, input, expected, actual and result; a defect has steps, severity and fix.
- Deployment stages: push, test, build, restart, health check.

## Chapter summary

- Tests are layered; the 9-test suite for ClinicQ rules passed and each test name states a requirement.
- The test-case table with expected and actual results is the evidence the examiner reads.
- Capacity is computed: at peak ClinicQ needs about 4 requests per second, 16 % of one small worker.
- A cache and more workers are the first scaling steps.
- Deployment is a repeatable pipeline with a health check; Nginx handles HTTPS and systemd keeps the service alive.

## Practice

1. Differentiate unit, API and manual testing with a ClinicQ example for each.
2. Why does the test pyramid have many unit tests but few manual tests?
3. Write three more unit tests for `valid_phone`.
4. Fill a test-case row for "login with a wrong password".
5. State Little's law and use it for 20 requests per second at 50 ms each.
6. If one worker serves 25 requests per second, how many workers are needed for 60 requests per second at 70 % utilisation?
7. What does a cache do, and what is its risk?
8. Why does the pipeline run tests before restarting the service?
9. What is the purpose of `/api/health`?
10. List five items of a pre-demo deployment checklist.

::: note Answers and worked solutions
**1.** Unit: `valid_phone("98x")` is false. API: `POST /api/patients` with `98x` returns 400. Manual: a person fills the form in a browser.
**2.** Unit tests are fast, cheap and exact; manual tests are slow and vary between people.
**3.** For example `valid_phone("")`, `valid_phone("98410000012")` (11 digits) and `valid_phone(" 9841000001")` (space) should be false.
**4.** ID T11; wrong password for sunita; expected 401; actual 401; Pass.
**5.** Concurrent = 20 × 0.05 = 1 request on average.
**6.** One worker at 70 % serves 17.5 per second, so 60 / 17.5 = 3.4, so 4 workers.
**7.** It stores a recent answer to avoid repeating work; the risk is showing slightly old data.
**8.** A failing test must stop a broken version from replacing a working one.
**9.** It lets scripts and monitors confirm that the application and its database are alive.
**10.** HTTPS, secret in the environment, debug off, backup done, clean-clone start works.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain software testing levels for a web application with examples.**

*Introduction.* Testing is the activity of running a program with chosen inputs to find defects. A web application is tested at several levels because defects hide at different depths.

*Levels.*

1. **Unit testing** checks one function in isolation, such as `valid_phone("98x1000001")` must be false. Unit tests are written by the developer, run in milliseconds and number in the dozens.
2. **Integration or API testing** calls real endpoints and checks status codes and bodies together with the database, for example `POST /api/tokens` for patient 99 must return 404.
3. **System and end-to-end testing** exercises the complete deployed system through its pages, such as registering a patient and watching the queue change on another phone.
4. **Acceptance testing** lets the real user, the clinic clerk, check that the system meets the objectives, such as a token in under one second.

*The pyramid.* Because unit tests are cheap and manual tests are slow, a project should have many unit tests, fewer API tests and a few manual checks (Figure 4.1).

*Example.* The ClinicQ suite ran 9 unit tests, all passing, and the test-case table listed 10 cases with expected and actual results.

*Conclusion.* Layered testing finds each kind of defect at the cheapest level and gives the examiner evidence.

**Q2 (5 marks). Describe how to deploy a student web project so that it is reachable over the internet.**

*Introduction.* Deployment moves the tested application from the developer's laptop to a server with a public address.

*Steps.*

1. **Prepare the server.** Rent a small virtual machine or use the college server; install Python, the database and Nginx.
2. **Copy the code.** `git pull` from the repository; create a virtual environment and install the pinned requirements.
3. **Configure.** Set the secret key, database path and port as environment variables; switch debug mode off.
4. **Run as a service.** A `systemd` unit starts the application at boot and restarts it after a crash.
5. **Reverse proxy and HTTPS.** Nginx listens on 443 with a Let's Encrypt certificate and forwards `/api/` to the application on a local port.
6. **Verify and back up.** Call the health URL, run the smoke tests and schedule a daily database backup.

*Example.* ClinicQ is reached at a domain name over HTTPS; Nginx forwards to port 8000; a health check returns 200.

*Conclusion.* A scripted, repeatable deployment with HTTPS and a health check is what turns a project into a service.

**Q3 (10 marks). Describe the testing and deployment plan for a web-based system such as ClinicQ, including test design, performance estimation and deployment pipeline.**

*Introduction.* A web system must be shown to be correct, fast enough and available. The plan has four parts: tests, defect handling, performance estimation and deployment.

*1. Test design.* Requirements are turned into tests. Unit tests check rules (phone format, next token number, role permissions); the 9-test suite of Section 4.2 passed. API tests check each endpoint for the success code and each error code: 201, 400, 404, 422, 401. Security tests try an injection string, a forged role and an expired token. A concurrency test sends two requests with the same read and confirms numbers 8 and 9.

*2. Test cases and defects.* Each case has an ID, input, expected result, actual result and verdict (Section 4.3). A failure becomes a defect with steps to reproduce, severity and the commit that fixed it, and the test is re-run (regression).

*3. Performance estimation.* From the clinic's 150 patients per day with 30 % in a 2-hour peak and 60 watchers refreshing every 15 seconds, the load is 4.0 requests per second. At 40 ms per request one worker handles 25 per second, so utilisation is 16 % and the system is comfortable. Little's law gives 0.16 concurrent requests. A 5-second cache limits database reads to 0.2 per second if the watchers grow to 600 (160 % of one worker without it).

*4. Deployment pipeline.* Code is pushed to Git; tests run automatically; if they pass the new version is copied to the server, the `systemd` service restarts, and a health check confirms 200 (Figure 4.1). Nginx terminates HTTPS and forwards to the application. Configuration comes from environment variables.

*5. Operations.* Logs record route, status and duration; a daily backup is copied off the machine and a restore is rehearsed; a recorded demo is kept as a fallback for load-shedding or network failure.

| Part | Evidence in the report |
|---|---|
| tests | test-case table, pass counts |
| defects | defect log with fixes |
| performance | request rate, service time, utilisation |
| deployment | pipeline figure, service and Nginx files, checklist |

*Conclusion.* The plan connects every claim to evidence: tests for correctness, arithmetic for capacity and a repeatable pipeline for delivery. This is the standard the examiner looks for in the Project II viva.
