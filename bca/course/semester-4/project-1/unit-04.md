---
subject: Project I
grade: BCA Semester 4
unit: 4
title: Building and Testing: Code, Test Cases and Defects
area: BCA 256 · Project I · Unit 4
---

With a design in hand, coding is translation. This unit builds the working core of CampusShelf (database, login, issue, return, fine and overdue list) as a real Python module, runs it, then tests it with written test cases and an automated test file. Every output shown here is the real output of the code.

::: key What this unit gives you
- A three-layer structure for a small project, and coding rules that keep it readable.
- The complete CampusShelf logic (about 60 lines) with a demo run.
- Test types, test cases linked to requirements, an automated `unittest` file and a bug life cycle.
:::

## 4.1 Structure: three layers

Keep three layers apart so that three students can work in parallel and each part can be tested alone (Figure 4.1). The **screen layer** shows forms and reads input (a Tkinter window, a Flask page or a command menu). The **logic layer** holds the rules (loan period, fine, availability). The **data layer** is the database. The logic never prints and never draws; the screen never writes SQL.

```svgfig label="4.1" caption="Three-layer structure of CampusShelf. The screen calls named functions in the logic layer; only the logic layer talks to SQLite. Each layer can be replaced (for example a web page for a window) without touching the others."
f = Fig(780, 200)
layers = [("Screen layer", "login form, issue form,\noverdue report", BLUE, NAVY), ("Logic layer", "login(), issue_book(),\nreturn_book(), overdue()", SOFT, TEAL), ("Data layer", "SQLite file: member, book,\nissue, librarian", BLUE, AMBER)]
for i, (t, d, fl, st) in enumerate(layers):
    x = 20 + i*260
    f.box(x, 40, 220, 100, "", fill=fl, stroke=st)
    f.text(x + 110, 66, t, size=13, color=NAVY, bold=True)
    f.text(x + 110, 94, d.split("\n")[0], size=10.5, color=SLATE)
    f.text(x + 110, 110, d.split("\n")[1], size=10.5, color=SLATE)
f.arrow([(240, 80), (280, 80)], color=NAVY, both=True)
f.arrow([(500, 80), (540, 80)], color=NAVY, both=True)
f.text(260, 70, "calls", size=9.5, color=SLATE)
f.text(520, 70, "SQL", size=9.5, color=SLATE)
f.text(390, 175, "Rule: the screen never writes SQL; the logic never prints", size=11, color=RED, bold=True)
```

## 4.2 The CampusShelf logic layer

The listing below is the complete logic and data layer in one file, `campusshelf.py`, followed by a short demo. Read it with the requirements of Section 3.1 beside you: F1 is `login`, F3 is `issue_book`, F4 is `return_book`, F5 is `overdue`, N2 is `hash_pw`. Dates are AD for simplicity; a BS converter belongs to the future-enhancements list.

```python
import sqlite3, hashlib, os, time
import datetime as dt

LOAN_DAYS, FINE_PER_DAY = 14, 2
SCHEMA = """
CREATE TABLE member (member_id INTEGER PRIMARY KEY, name TEXT NOT NULL, program TEXT);
CREATE TABLE book (book_id INTEGER PRIMARY KEY, title TEXT NOT NULL, author TEXT, copies INTEGER CHECK (copies >= 0));
CREATE TABLE issue (issue_id INTEGER PRIMARY KEY, member_id INTEGER NOT NULL REFERENCES member,
    book_id INTEGER NOT NULL REFERENCES book, issue_date TEXT NOT NULL, due_date TEXT NOT NULL,
    return_date TEXT, fine INTEGER DEFAULT 0);
CREATE TABLE librarian (user TEXT PRIMARY KEY, pw TEXT NOT NULL);
"""
def connect():
    db = sqlite3.connect(":memory:"); db.execute("PRAGMA foreign_keys = ON"); db.executescript(SCHEMA); return db
def hash_pw(pw, salt=None):
    salt = salt or os.urandom(8).hex()
    return salt + "$" + hashlib.sha256((salt + pw).encode()).hexdigest()
def add_librarian(db, user, pw):
    db.execute("INSERT INTO librarian VALUES (?, ?)", (user, hash_pw(pw)))
def login(db, user, pw):
    row = db.execute("SELECT pw FROM librarian WHERE user = ?", (user,)).fetchone()
    return bool(row) and hash_pw(pw, row[0].split("$")[0]) == row[0]
def add_member(db, name, program):
    return db.execute("INSERT INTO member (name, program) VALUES (?, ?)", (name, program)).lastrowid
def add_book(db, title, author, copies):
    return db.execute("INSERT INTO book (title, author, copies) VALUES (?, ?, ?)", (title, author, copies)).lastrowid
def copies_left(db, book_id):
    total = db.execute("SELECT copies FROM book WHERE book_id = ?", (book_id,)).fetchone()[0]
    out = db.execute("SELECT COUNT(*) FROM issue WHERE book_id = ? AND return_date IS NULL", (book_id,)).fetchone()[0]
    return total - out
def issue_book(db, member_id, book_id, today):
    if copies_left(db, book_id) <= 0:
        raise ValueError("no copy available")
    due = today + dt.timedelta(days=LOAN_DAYS)
    return db.execute("INSERT INTO issue (member_id, book_id, issue_date, due_date) VALUES (?, ?, ?, ?)",
                      (member_id, book_id, today.isoformat(), due.isoformat())).lastrowid
def return_book(db, issue_id, today):
    due = dt.date.fromisoformat(db.execute("SELECT due_date FROM issue WHERE issue_id = ?", (issue_id,)).fetchone()[0])
    fine = FINE_PER_DAY * max(0, (today - due).days)
    db.execute("UPDATE issue SET return_date = ?, fine = ? WHERE issue_id = ?", (today.isoformat(), fine, issue_id))
    return fine
def overdue(db, today):
    return db.execute("SELECT m.name, b.title, i.due_date FROM issue i JOIN member m USING (member_id) "
                      "JOIN book b USING (book_id) WHERE i.return_date IS NULL AND i.due_date < ? ORDER BY i.due_date",
                      (today.isoformat(),)).fetchall()

# ---- demo ----
db = connect(); add_librarian(db, "ram", "pass123")
print("login right:", login(db, "ram", "pass123"), "| wrong:", login(db, "ram", "oops"))
stored = db.execute("SELECT pw FROM librarian").fetchone()[0]
print("plain text stored:", "pass123" in stored, "| stored length:", len(stored))
asha, ram = add_member(db, "Asha", "BCA"), add_member(db, "Ram", "BCA")
c, dbms = add_book(db, "C Programming", "Kernighan", 1), add_book(db, "DBMS", "Elmasri", 2)
t0 = dt.date(2025, 1, 1)
i1 = issue_book(db, asha, c, t0)
print("issue 1 due:", db.execute("SELECT due_date FROM issue WHERE issue_id = ?", (i1,)).fetchone()[0], "| copies left:", copies_left(db, c))
try:
    issue_book(db, ram, c, t0)
except ValueError as e:
    print("second issue of the last copy:", e)
print("fine when returned 19 days after issue:", return_book(db, i1, t0 + dt.timedelta(days=19)))
issue_book(db, ram, dbms, t0)
print("overdue on", t0 + dt.timedelta(days=20), ":", overdue(db, t0 + dt.timedelta(days=20)))
slowest = 0
for k in range(20):
    s = time.perf_counter(); n = issue_book(db, asha, dbms, t0); return_book(db, n, t0); slowest = max(slowest, time.perf_counter() - s)
print("20 transactions, slowest under 30 s (N1):", slowest < 30)
```
```output
login right: True | wrong: False
plain text stored: False | stored length: 81
issue 1 due: 2025-01-15 | copies left: 0
second issue of the last copy: no copy available
fine when returned 19 days after issue: 10
overdue on 2025-01-21 : [('Ram', 'DBMS', '2025-01-15')]
20 transactions, slowest under 30 s (N1): True
```
The fine check is arithmetic you can do by hand: issued on 1 January, due on 15 January; returned on 20 January is 5 days late, so the fine is 5 × Rs 2 = Rs 10. Only the **salted hash** of the password is stored; the plain text never reaches the database.

**Coding rules that earn marks.** Meaningful names (`copies_left`, not `x1`); one function, one job; comments for *why*, not *what*; parameterised SQL (`?` placeholders, never string joins, which block SQL injection); constants at the top (`LOAN_DAYS`); and a commit after every working step.

## 4.3 Kinds of testing

| Level | Tests what | Who | Example in CampusShelf |
|---|---|---|---|
| Unit test | one function alone | developer | `return_book` gives Rs 10 for 5 late days |
| Integration test | modules working together | developer, tester | issue then return then overdue list |
| System test | the whole program against the requirements | tester | all F and N requirements on a clean install |
| Acceptance test | the user accepts the system | librarian | she issues 20 real books on the demo day |

**Black-box** testing checks inputs and outputs without looking at the code (acceptance and system tests). **White-box** testing uses the code structure, trying every branch such as "copy available" and "no copy". Figure 4.2 (the **V-model**) pairs each design stage with the test level that verifies it.

```svgfig label="4.2" caption="The V-model. Each stage on the left is checked by the test on the same level on the right: requirements by acceptance tests, system design by system tests, module design by integration tests, code by unit tests. Dashed lines show the pairing."
f = Fig(780, 250)
left = [("Requirements", 10, 20), ("System design", 90, 75), ("Module design", 170, 130), ("Coding", 250, 185)]
right = [("Unit test", 390, 185), ("Integration test", 470, 130), ("System test", 550, 75), ("Acceptance test", 630, 20)]
for n, x, y in left: f.box(x, y, 120, 40, n, fill=BLUE, stroke=NAVY, size=11, bold=True)
for n, x, y in right: f.box(x, y, 130 if x == 630 else 120, 40, n, fill=SOFT, stroke=TEAL, size=11, bold=True)
f.arrow([(130, 40), (630, 40)], color=SLATE, dash=True, both=True)
f.arrow([(210, 95), (550, 95)], color=SLATE, dash=True, both=True)
f.arrow([(290, 150), (470, 150)], color=SLATE, dash=True, both=True)
f.arrow([(370, 205), (390, 205)], color=SLATE, dash=True, both=True)
f.text(380, 60, "verified by", size=10, color=SLATE, italic=True)
```

## 4.4 Test cases linked to requirements

A **test case** has an ID, the requirement it checks, the input, the expected result and the actual result. Writing the expected result *before* running is what makes it a test and not a demonstration.

| TC | Req | Input | Expected | Actual |
|---|---|---|---|---|
| 1 | F1 | user ram, password oops | login refused | refused |
| 2 | F3 | issue on 2025-01-01 | due date 2025-01-15 | 2025-01-15 |
| 3 | F3 | issue the last copy twice | second issue refused | "no copy available" |
| 4 | F4 | return 5 days late | fine Rs 10 | 10 |
| 5 | F4 | return on the due date | fine Rs 0 | 0 |
| 6 | F5 | one late open loan | list has 1 row | 1 row |
| 7 | N2 | inspect librarian table | no plain text | not found |
| 8 | data | issue to member 99 | database rejects | IntegrityError |

## 4.5 Automated tests with `unittest`

Typing these cases by hand every time is slow. Python's `unittest` module runs them in a fraction of a second after every change. The file below holds one test per case and imports the logic layer (Listing 4.2, saved as `campusshelf.py`). Its real output follows.

```py
# test_campusshelf.py: run with  python -m unittest -v
import sqlite3, unittest
import datetime as dt
from campusshelf import *

T0 = dt.date(2025, 1, 1)

class CampusShelfTests(unittest.TestCase):
    def setUp(self):
        self.db = connect()
        add_librarian(self.db, "ram", "pass123")
        self.m = add_member(self.db, "Asha", "BCA")
        self.b = add_book(self.db, "C Programming", "Kernighan", 1)

    def test_F1_wrong_password_rejected(self):
        self.assertTrue(login(self.db, "ram", "pass123"))
        self.assertFalse(login(self.db, "ram", "oops"))

    def test_F3_due_date_is_14_days_later(self):
        i = issue_book(self.db, self.m, self.b, T0)
        due = self.db.execute("SELECT due_date FROM issue WHERE issue_id = ?", (i,)).fetchone()[0]
        self.assertEqual(due, "2025-01-15")

    def test_F3_last_copy_cannot_be_issued_twice(self):
        issue_book(self.db, self.m, self.b, T0)
        with self.assertRaises(ValueError):
            issue_book(self.db, self.m, self.b, T0)

    def test_F4_fine_is_rs2_per_late_day(self):
        i = issue_book(self.db, self.m, self.b, T0)
        self.assertEqual(return_book(self.db, i, dt.date(2025, 1, 20)), 10)

    def test_F4_no_fine_on_the_due_date(self):
        i = issue_book(self.db, self.m, self.b, T0)
        self.assertEqual(return_book(self.db, i, dt.date(2025, 1, 15)), 0)

    def test_F5_overdue_lists_only_unreturned_late_loans(self):
        i = issue_book(self.db, self.m, self.b, T0)
        self.assertEqual(len(overdue(self.db, dt.date(2025, 1, 20))), 1)
        return_book(self.db, i, dt.date(2025, 1, 20))
        self.assertEqual(overdue(self.db, dt.date(2025, 1, 20)), [])

    def test_N2_password_not_stored_in_plain_text(self):
        stored = self.db.execute("SELECT pw FROM librarian").fetchone()[0]
        self.assertNotIn("pass123", stored)

    def test_foreign_key_blocks_unknown_member(self):
        with self.assertRaises(sqlite3.IntegrityError):
            issue_book(self.db, 99, self.b, T0)

unittest.main(verbosity=2)
```

```output
test_F1_wrong_password_rejected (__main__.CampusShelfTests.test_F1_wrong_password_rejected) ... ok
test_F3_due_date_is_14_days_later (__main__.CampusShelfTests.test_F3_due_date_is_14_days_later) ... ok
test_F3_last_copy_cannot_be_issued_twice (__main__.CampusShelfTests.test_F3_last_copy_cannot_be_issued_twice) ... ok
test_F4_fine_is_rs2_per_late_day (__main__.CampusShelfTests.test_F4_fine_is_rs2_per_late_day) ... ok
test_F4_no_fine_on_the_due_date (__main__.CampusShelfTests.test_F4_no_fine_on_the_due_date) ... ok
test_F5_overdue_lists_only_unreturned_late_loans (__main__.CampusShelfTests.test_F5_overdue_lists_only_unreturned_late_loans) ... ok
test_N2_password_not_stored_in_plain_text (__main__.CampusShelfTests.test_N2_password_not_stored_in_plain_text) ... ok
test_foreign_key_blocks_unknown_member (__main__.CampusShelfTests.test_foreign_key_blocks_unknown_member) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.003s

OK
```

All eight tests pass. If a test fails after a later change, you learn within seconds which requirement broke, which is the main reason to automate. (The test names with `F1`, `F3`, `N2` link every test to its requirement.)

## 4.6 Defects and the bug life cycle

A **defect** (bug) is any difference between the expected and the actual result. Record each one in a bug log with an ID, a description, the steps to reproduce it, a severity and a status. A bug without steps to reproduce cannot be fixed.

```svgfig label="4.3" caption="Life cycle of a defect. The tester logs it, the leader assigns it, the developer fixes it and the tester re-tests. A failed re-test sends it back (reopened); a passed re-test closes it."
f = Fig(780, 150)
st = [("New", BLUE, NAVY), ("Assigned", BLUE, NAVY), ("Fixed", SOFT, TEAL), ("Re-test", SOFT, TEAL), ("Closed", BLUE, NAVY)]
for i, (n, fl, sk) in enumerate(st):
    x = 20 + i*150
    f.box(x, 40, 110, 44, n, fill=fl, stroke=sk, size=12, bold=True)
    if i < 4: f.arrow([(x + 110, 62), (x + 150, 62)], color=NAVY)
f.arrow([(470, 84), (470, 120), (170, 120), (170, 84)], color=RED, dash=True, label="re-test fails: reopen", lpos=(320, 112))
f.text(75, 28, "tester logs", size=10, color=SLATE); f.text(225, 28, "leader assigns", size=10, color=SLATE)
f.text(375, 28, "developer fixes", size=10, color=SLATE); f.text(525, 28, "tester checks", size=10, color=SLATE)
```

| Bug | Steps to reproduce | Severity | Status |
|---|---|---|---|
| B1 | return a book on the due date: fine shows Rs 2 | high | fixed (test 5) |
| B2 | add a book with copies = -1: accepted | medium | fixed (CHECK rule) |
| B3 | search is case-sensitive: "dbms" finds nothing | low | open (future) |

**Severity** is the damage (crash, wrong money, cosmetic); **priority** is how soon it is fixed. Wrong fines are high severity because they hurt students.

## 4.7 Eight reasons to test early and often

1. **Bugs are cheaper when young.** A bug found the day it is written takes minutes; the same bug found in the viva can sink the demo. Test each function as soon as you write it. Early testing is the cheapest insurance you have.
2. **Tests prove requirements.** A test named F4 shows the examiner that the fine rule works. Claims without tests are only opinions. Printed test output is strong evidence in the report.
3. **Changes become safe.** When you improve the code or add a feature, the old tests tell you at once if something else broke. Without them, every change is a gamble. This is called regression testing.
4. **Edge cases are caught.** Returning on the due date, issuing the last copy and a negative copy count are exactly where programs fail. Writing the expected result forces you to think about them. Real users find edge cases quickly.
5. **Team members trust each other's code.** If a teammate's module passes its tests, you can build on it. Disagreements become evidence, not arguments. Integration week is calmer.
6. **The demo is repeatable.** A demo that depends on typing the right data in the right order is fragile. A test file runs the same steps every time. You can run it five minutes before the viva.
7. **Documentation writes itself.** Test names and the test-case table describe how the system behaves. New teammates and future students can read them as a guide. The report's testing chapter is largely a copy of this table.
8. **Confidence for the viva.** When you have seen your own system fail and then fixed it, you can speak about it honestly. Examiners like students who can describe a bug they found and how they closed it. That story is worth marks.

```photogrid label="4.1" cols="2" ratio="1.2" caption="Do the tests really test? (a) A crash-test dummy is used because failures are cheap to find before the real car is on the road. (b) The CampusShelf fine rule is Rs 5 for each day late, capped at Rs 200. Seven faulty copies (mutants) of the function were made by changing one symbol each, and two test sets were run against all of them. Set A uses typical values (-5, 2, 7, 20) and catches only 3 of the 6 catchable mutants; set B uses boundary values (-1, 0, 1, 39, 40, 41) and catches all 6. One mutant (< 0 instead of <= 0) behaves identically for every input, so no test can catch it: it is an equivalent mutant, and 1 of 7 is normal. The lesson of boundary-value analysis is measured here: bugs live at the edges (0, 1, the cap), so test the edges first."
@ photo id="bcapj/dummy" cap="A crash-test dummy: test before the real thing"
fit 1.2
focus 0.5 0.5
@ svg cap="Mutation test: 7 faulty copies of fine()"
SRC = "def fine(d):\n    if d <= 0:\n        return 0\n    return min(5 * d, 200)\n"
MUT = [("<= 0 to < 0", SRC.replace("d <= 0", "d < 0")), ("<= 0 to <= 1", SRC.replace("d <= 0", "d <= 1")),
       ("rate 5 to 6", SRC.replace("5 * d", "6 * d")), ("cap 200 to 199", SRC.replace("200)", "199)")),
       ("cap 200 to 250", SRC.replace("200)", "250)")), ("min to max", SRC.replace("min(", "max(")),
       ("5*d to 5+d", SRC.replace("5 * d", "5 + d"))]
def load(s):
    ns = {}
    exec(s, ns)
    return ns["fine"]
orig = load(SRC)
A = [-5, 2, 7, 20]
B = [-1, 0, 1, 39, 40, 41]
def killed(fn, tests):
    return any(fn(t) != orig(t) for t in tests)
res = []
for n, s in MUT:
    fn = load(s)
    eq = all(fn(d) == orig(d) for d in range(-50, 200))
    res.append((n, killed(fn, A), killed(fn, B), eq))
kA = sum(r[1] for r in res)
kB = sum(r[2] for r in res)
eqn = sum(r[3] for r in res)
assert eqn == 1 and kB == 6 and kA < kB
facts = dict(kA=kA, kB=kB, eqn=eqn, total=len(res))
f = Fig(300, 236)
f.text(150, 12, "fine = min(5 x days late, 200)", size=10.5, color=NAVY, bold=True)
f.text(196, 30, "A typical", size=10.5, color=SLATE, bold=True)
f.text(266, 30, "B boundary", size=10.5, color=SLATE, bold=True)
for i, (n, a, b, eq) in enumerate(res):
    y = 38 + i * 24
    f.box(4, y, 124, 20, n, fill=SAND if not eq else "#e5e7eb", stroke=SLATE, size=10.5, r=3, sw=1)
    for x, v in ((196, a), (266, b)):
        if eq:
            f.text(x, y + 10, "same", size=10.5, color=SLATE, vmid=True)
        else:
            f.text(x, y + 10, "caught" if v else "missed", size=10.5, color=TEAL if v else RED, bold=True, vmid=True)
f.text(150, 214, "A %d of %d caught, B %d of %d caught" % (kA, len(res) - eqn, kB, len(res) - eqn), size=10.5, color=NAVY, bold=True)
f.text(150, 230, "A = -5,2,7,20  B = -1,0,1,39,40,41", size=10.5, color=SLATE)
```

## Formula and fact sheet

- Layers: screen, logic, data; the screen never writes SQL, the logic never prints.
- Fine = 2 × max(0, days late); loan period 14 days; hash passwords with a salt.
- Test case = ID + requirement + input + expected + actual. Levels: unit, integration, system, acceptance.
- Bug life cycle: new, assigned, fixed, re-test, closed (or reopened).

## Chapter summary

- Separate screen, logic and data so that parts can be built and tested alone.
- The CampusShelf logic layer runs: hashed login, 14-day loans, Rs 2 fines, overdue list.
- Test cases are tied to requirements; `unittest` automates them (8 of 8 pass).
- A bug log with steps to reproduce, severity and status keeps fixing organised.

## Practice

1. Why are the screen, logic and data layers kept apart?
2. Why must SQL use `?` placeholders and not string concatenation?
3. Explain why a salted hash is safer than storing the password.
4. Differentiate unit, integration, system and acceptance testing.
5. What is the difference between black-box and white-box testing?
6. Write three test cases for a function that calculates a bus fare.
7. A book is due 10 January and returned on 25 January. Compute the fine with Rs 2 per day.
8. Draw the bug life cycle and label the person responsible at each step.
9. What is regression testing and why does `unittest` help?
10. A test suite has 40 tests; 3 fail. What is the pass percentage? What do you do first?

::: note Answers and worked solutions
**1.** Each layer can change or be tested without the others, and team members can work in parallel.
**2.** Placeholders send values as data, so a user cannot inject SQL commands such as `'; DROP TABLE book; --`.
**3.** A hash cannot be reversed; a random salt makes equal passwords give different hashes, which defeats look-up tables.
**4.** Unit: one function. Integration: modules together. System: whole program against requirements. Acceptance: the user's approval.
**5.** Black-box uses inputs and outputs only; white-box uses the code's structure (every branch).
**6.** Child fare (age 5): half price; adult (age 30): full fare; invalid age (-1): rejected.
**7.** 15 days late × Rs 2 = **Rs 30**.
**8.** New (tester) → Assigned (leader) → Fixed (developer) → Re-test (tester) → Closed or Reopened.
**9.** Re-running old tests after a change to check nothing else broke; `unittest` does it in a second.
**10.** 37 / 40 = **92.5 %**; read the first failing test, reproduce it, fix the code (or the test if it was wrong), then re-run all.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the levels of software testing with examples.**

*Introduction.* Testing compares the actual behaviour of the software with the expected behaviour. It is done at four levels, from the smallest piece to the complete system.

1. **Unit testing** checks a single function. Example: `return_book` must give a fine of Rs 10 when the book is 5 days late. It is done by the developer and is fast.
2. **Integration testing** checks modules working together. Example: issue a book, return it, and check that the overdue list no longer shows it. Errors here come from wrong assumptions between modules.
3. **System testing** checks the whole program against all requirements on a clean machine, including non-functional ones such as 30 seconds per transaction.
4. **Acceptance testing** is done by the user. The librarian issues and returns real books; if she accepts, the system is complete.

*V-model.* Each level verifies a design stage (Figure 4.2): code by unit tests, module design by integration tests, system design by system tests, requirements by acceptance tests.

*Conclusion.* Lower levels find bugs cheaply; higher levels prove the system is right for the user. Both are needed.

**Q2 (5 marks). What is a test case? Write test cases for the fine calculation of CampusShelf.**

*Definition.* A test case is a documented check with an ID, the requirement it verifies, the input, the expected result and the actual result. The expected result is written before the test is run.

*Fine rule (F4).* Fine = Rs 2 × days after the due date; no fine on or before the due date.

| TC | Input (due 15 Jan) | Expected fine | Reason |
|---|---|---|---|
| 1 | returned 10 Jan | Rs 0 | early |
| 2 | returned 15 Jan | Rs 0 | boundary: due date itself |
| 3 | returned 16 Jan | Rs 2 | boundary: 1 day late |
| 4 | returned 20 Jan | Rs 10 | typical |
| 5 | returned 15 Feb | Rs 62 | 31 days late, 31 × 2 |

*Technique.* The cases use **boundary values** (the due date and the day after) because errors collect at boundaries, as bug B1 showed. In the project the cases were automated with `unittest`, and 8 of 8 passed.

*Conclusion.* Written cases make testing repeatable and give evidence for the report.

**Q3 (10 marks). Describe how you would implement and test a small library system, with the structure of the code, the tests and the handling of defects.**

*Introduction.* After analysis and design (Unit 3) the team builds and tests the system in small steps. The CampusShelf work is the model.

*1. Structure.* Three layers (Figure 4.1): screen, logic and data. The logic layer has pure functions (`login`, `issue_book`, `return_book`, `overdue`); the data layer is SQLite with the four tables of the ER design; the screen only calls the logic.

*2. Coding rules.* Meaningful names, one job per function, constants at the top (`LOAN_DAYS = 14`, `FINE_PER_DAY = 2`), parameterised SQL against injection, salted hashes for passwords (N2), commits after every working step.

*3. Implementation order.* Database and schema first; then login; then add book and member; then issue and return with fine; then overdue report; finally the screens. Each step is demonstrated to the supervisor.

*4. Test design.* Every requirement gets at least one test case with an expected result: wrong password refused, due date 14 days later, last copy not issued twice, fine Rs 10 for 5 days late, no fine on the due date, overdue list correct, hashed password, foreign key rejection (Section 4.4).

*5. Automation.* The cases are written as `unittest` functions named after the requirement and run after every change; the real run printed `Ran 8 tests ... OK`.

*6. Levels.* Unit tests by developers, integration tests for the issue-return-overdue chain, a system test against F1 to N3 on a clean install, and an acceptance test by the librarian (Section 4.3).

*7. Defect handling.* Bugs are logged with steps to reproduce, severity and status and move through new, assigned, fixed, re-test and closed (Figure 4.3). Example: B1 (fine on the due date) was reproduced, fixed and closed after test 5 passed.

*8. Evidence for the report.* The test-case table, the test output, the bug log and the pass percentage (8 of 8 = 100 %) go into the testing chapter.

| Stage | Output | Evidence |
|---|---|---|
| Structure | three layers | Figure 4.1 |
| Code | `campusshelf.py` | Listing 4.2 and demo output |
| Tests | 8 test cases | Section 4.4 table |
| Automation | `unittest` run | OK, 8 tests |
| Defects | bug log | B1 to B3 |

*Conclusion.* Layered code, requirement-linked tests and a disciplined bug log produce software that can be demonstrated confidently and defended in the viva.
