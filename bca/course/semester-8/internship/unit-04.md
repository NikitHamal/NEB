---
subject: Internship
grade: BCA Semester 8
unit: 4
title: Technical Contribution: Tickets, Code Review, Testing and Hand-over
area: BCA 452 · Internship · Unit 4
---

Week three at Himal Digital. Her supervisor, Sanjay, opens the team board and drags a card to Anisha's name: **HD-31, "Invoice total differs by a few paisa from the accountant's calculator."** This is a real task in a live code base, with a real client waiting. It is also the best kind of internship work: small, concrete, checkable and visible. This unit follows ticket HD-31 from the board to the hand-over page and shows the habits of a professional contributor.

::: key What this unit gives you
- The **life cycle of a ticket** and how to read an unfamiliar code base in an afternoon.
- The professional order of work for a bug: **reproduce, understand, fix, test, review, hand over**.
- An executed script that reproduces the VAT-rounding bug of HD-31 and an executed six-test suite that proves the fix.
- What a **code review** looks for, how to reply to comments, and what a hand-over page contains.
- Photographs of code, a technician and a review desk, and eight practices of interns whose work gets merged.
:::

## 4.1 The ticket life cycle

A **ticket** (or issue) is a written unit of work: a bug, a feature or a chore. Teams track tickets on a board so that everyone sees who is doing what. Figure 4.1 shows the usual flow. A ticket enters the **backlog**, is picked up (**in progress**), goes to **review** when the change is ready, is **merged** into the main branch after approval, and is **deployed** to users. At each step somebody other than you looks at the work.

Three habits keep tickets healthy. First, **one ticket, one branch, one purpose**: HD-31 changes rounding and nothing else. Second, **write down what "done" means** before starting ("every invoice total equals the hand calculation to the paisa, and tests prove it"). Third, **update the ticket** whenever you learn something; a ticket is a conversation that survives people going on leave.

## 4.2 Reading a code base you did not write

Anisha has never seen the Himal Digital billing code. Reading it from the top would take days. Use a **five-step tour** instead.

1. **Run it.** Follow the README, start the application and click through the feature you must change.
2. **Find the entry point.** Search for the page, button text or route name. `grep -rn "Invoice total"` often lands on the right file in seconds.
3. **Trace one path.** Follow a single request from the controller to the function that produces the number, and write it as a short list in your notebook.
4. **Look at the tests and the history.** Existing tests show intended behaviour; `git log -p` on the file shows why it looks the way it does.
5. **Ask one precise question.** "Is `calc_total` the only place VAT is added?" is better than "can you explain billing?".

## 4.3 Reproduce first, then fix

A fix without a reproduction is a guess. The accountant's complaint is the starting point: the system total and a calculator disagree by a paisa on some invoices. Anisha asks for three real (anonymised) invoices and writes the failing case. The script below holds the **old** method (round each line after adding 13 percent VAT, using floats) and the **new** method (add up exact `Decimal` subtotals, compute VAT once, round once, half-up). It compares both with the hand calculation on three invoices. The amounts are invented.

```python
from decimal import Decimal as D, ROUND_HALF_UP
def old_total(lines):
    return round(sum(round(p * q * 1.13, 2) for p, q in lines), 2)
def new_total(lines):
    sub = sum(D(p) * q for p, q in lines)
    vat = (sub * D("0.13")).quantize(D("0.01"), ROUND_HALF_UP)
    return sub + vat
invoices = {
    "INV-101": [("33.33", 3), ("10.10", 7)],
    "INV-102": [("0.50", 1), ("12.10", 4)],
    "INV-103": [("1.50", 3), ("2.50", 3)],
    "INV-104": [("125.50", 2), ("40.25", 3)],
}
bad = 0
for name, raw in invoices.items():
    old = old_total([(float(p), q) for p, q in raw])
    new = new_total(raw)
    flag = "" if D(str(old)) == new else "  <-- differs"
    bad += bool(flag)
    print(f"{name}: old {old:>8.2f}  new {new:>8}{flag}")
print("invoices with a paisa error:", bad, "of", len(invoices))
```
```output
INV-101: old   192.88  new   192.88
INV-102: old    55.25  new    55.26  <-- differs
INV-103: old    13.55  new    13.56  <-- differs
INV-104: old   420.08  new   420.08
invoices with a paisa error: 2 of 4
```

*Reading the output.* Two of the four invoices are wrong. In INV-102 the first line is Rs 0.50 plus 13 percent VAT, which is exactly 0.565. A binary float stores 0.565 as 0.56499999..., so `round` goes **down** to 0.56 and the old total is 55.25; the exact method gives subtotal 48.90, VAT 6.357 rounded half-up to 6.36, total **55.26**, which matches the accountant's calculator. INV-103 fails the same way (13.55 against 13.56). Two ordinary invoices, INV-101 and INV-104, hide the bug, which is why it was only noticed by an accountant. The lesson, and the one Anisha writes in her log, is **never use binary floats for money, and round once, at the end**.

```svgfig label="4.1" caption="Life cycle of ticket HD-31. Each arrow is a hand-over to another person: the author, the reviewer, the supervisor and the client all see the work. The dashed arrow shows the common loop back to In progress when a reviewer asks for changes."
f = Fig(580, 190)
st = [("Backlog", "bug reported\nby accountant", BLUE, NAVY), ("In progress", "Anisha reproduces,\nfixes, tests", SOFT, TEAL), ("In review", "Sanjay reads\nthe diff", "#fde68a", AMBER),
      ("Merged", "main branch,\ntests green", SOFT, TEAL), ("Deployed", "client sees\ncorrect totals", BLUE, NAVY)]
for i, (n, d, fl, s) in enumerate(st):
    x = 8 + i * 115
    f.box(x, 50, 100, 62, "", fill=fl, stroke=s)
    f.text(x + 50, 68, n, size=11.5, color=NAVY, bold=True)
    f.text(x + 50, 87, d.split("\n")[0], size=9, color=NAVY)
    f.text(x + 50, 100, d.split("\n")[1], size=9, color=NAVY)
    if i < 4:
        f.arrow([(x + 100, 81), (x + 115, 81)], color=SLATE)
f.arrow([(238, 112), (238, 140), (166, 140), (166, 112)], color=RED, dash=True)
f.text(202, 156, "changes requested", size=10, color=RED, bold=True)
f.text(290, 20, "one ticket, one branch, one purpose", size=11, color=NAVY, bold=True)
```

## 4.4 Fix, test and ask for review

With the failure reproduced, the fix is a ten-line change: replace the float function by the `Decimal` one and call it from the invoice page. Anisha does **not** stop there. She writes tests first, so that the bug can never return unnoticed. The program below is a small self-contained test suite of six checks, run with a minimal runner that prints one PASS or FAIL line per test (a real project would use `unittest` or `pytest`). Note the **edge cases**: an empty invoice and a negative quantity.

```python
from decimal import Decimal as D, ROUND_HALF_UP
def new_total(lines):
    for p, q in lines:
        if q <= 0:
            raise ValueError("quantity must be positive")
    sub = sum(D(p) * q for p, q in lines)
    vat = (sub * D("0.13")).quantize(D("0.01"), ROUND_HALF_UP)
    return sub + vat
def t_simple():     assert str(new_total([("100.00", 1)])) == "113.00"
def t_half_paisa(): assert str(new_total([("0.50", 1)])) == "0.57"
def t_inv102():     assert str(new_total([("0.50", 1), ("12.10", 4)])) == "55.26"
def t_inv103():     assert str(new_total([("1.50", 3), ("2.50", 3)])) == "13.56"
def t_empty():      assert str(new_total([])) == "0.00"
def t_negative():
    try:
        new_total([("5.00", -2)])
    except ValueError:
        return
    raise AssertionError("no error raised")
tests = [t_simple, t_half_paisa, t_inv102, t_inv103, t_empty, t_negative]
fails = 0
for t in tests:
    try:
        t()
        print("PASS", t.__name__)
    except AssertionError as e:
        fails += 1
        print("FAIL", t.__name__, e)
print(f"{len(tests) - fails} passed, {fails} failed")
```
```output
PASS t_simple
PASS t_half_paisa
PASS t_inv102
PASS t_inv103
PASS t_empty
PASS t_negative
6 passed, 0 failed
```

*Reading the output.* All six checks pass. The first four fix known answers (including the two failing invoices), the fifth guards the empty invoice, and the sixth proves that bad input is rejected instead of silently producing a total. The tests also act as **documentation**: a new reader sees in six lines what the function promises. Anisha adds the suite to the repository in the same branch as the fix, so the reviewer sees the evidence next to the change.

Before opening the review request, she does a **self-review**: she reads her own diff line by line as if somebody else wrote it, removes a debug `print`, checks that no password or client name slipped in (Unit 2) and writes a clear description.

```photogrid label="4.1" cols="3" ratio="1.0" caption="Where technical contribution happens. (a) Code on a monitor: most of an intern's week is reading and changing lines like these, not writing programs from scratch. (b) A technician working at server equipment: some firms also expect an intern to follow deployment and support work. (c) The anatomy of a review request: title, ticket link, what changed and why, how it was tested, and what the reviewer should check."
@ photo id="bca306/code" cap="Code on a monitor"
fit 1.0
focus 0.5 0.5
call 0.5 0.85 0.5 0.65 "read before you write"
@ photo id="bca306/tech" cap="Technician at racks"
fit 1.0
focus 0.5 0.5
call 0.5 0.85 0.5 0.65 "deploy and support"
@ svg cap="Review request"
f = Fig(300, 300)
f.box(8, 8, 284, 284, "", fill="#ffffff", stroke=NAVY)
rows = [("Title", "HD-31 Fix VAT rounding", BLUE), ("What", "Decimal, round once", SOFT), ("Why", "0.565 rounds to 0.56", SOFT),
        ("Tests", "6 added, all pass", "#bbf7d0"), ("Risk", "invoice page only", "#fde68a"), ("Check", "rounding, edge cases", "#fde68a")]
for i, (a, b, c) in enumerate(rows):
    y = 18 + i * 45
    f.box(16, y, 66, 38, a, fill=c, stroke=NAVY, size=13, color=NAVY, bold=True)
    f.box(86, y, 198, 38, b, fill="#ffffff", stroke=SLATE, size=12.5, color=NAVY)
```

## 4.5 What a code review looks for

A **code review** is a colleague reading your change before it joins the main branch. Reviewers ask the same questions in the same order: *Does it do what the ticket says? Is it correct for edge cases? Is it readable? Is it tested? Is it safe (no secrets, no injection, no data leak)? Does it follow the team style?* Expect comments, especially in the first weeks; ten comments on a first change is normal, not a failure.

Reply to every comment, even with "done". If you disagree, ask a question ("I used `Decimal` because floats cannot hold 0.565; is there a reason we avoid it here?") rather than arguing. If you do not understand, say so. When all comments are resolved, the reviewer approves and the change is merged. Anisha's HD-31 gets three comments: rename a variable, add the empty-invoice test (already done in her case), and mention the ticket in the commit message.

## 4.6 Documentation and hand-over

In week eight the interns leave, but the code stays. A **hand-over page** lets the next person continue without asking. It is one page with six headings: *what was done* (tickets and links), *how to run and test* (commands), *how it works* (a small diagram or three sentences), *known issues* (honestly listed), *what to do next* (suggested tickets) and *who to ask*. Keep it in the repository's `docs/` folder, not on your laptop. Hand-over also means returning access: badge, accounts, keys and any firm data on your own device.

## 4.7 Eight practices of interns whose work gets merged

1. **Reproduce before you fix.** Write the failing case first, as Anisha did with INV-102. A fix that cannot be shown to cure a visible failure is only a hope. The reproduction also becomes your best test.
2. **Keep changes small.** One ticket, one branch, one purpose, and a diff a reviewer can read in ten minutes. Large mixed changes wait in the queue and hide bugs. Small changes are merged the same day.
3. **Write tests with the fix.** Include the failing case and at least one edge case such as empty or negative input. Tests protect the next person from your mistake and protect you from "it worked yesterday". Reviewers trust code that proves itself.
4. **Read the existing style.** Match names, layout and error handling already in the code base. Your change should look as though the team wrote it. Consistency helps readers more than personal taste.
5. **Self-review before asking.** Read your diff line by line, remove debug prints, check for secrets and write a clear description with the ticket link. This catches half the review comments and shows respect for the reviewer's time.
6. **Reply to every comment.** Say "done" or ask a polite question. Do not argue for pride. Resolved comments teach you the team's standards faster than any document.
7. **Use exact types for money and dates.** Floats, time zones and encodings are classic causes of bugs in business software. Learn the one tool the team uses (here, `Decimal`) and explain why in the commit message.
8. **Leave a hand-over page.** Document how to run, test and extend your work, list known issues and name who to ask. A clear hand-over makes your work last and gives you the strongest line in your reference letter.

## Formula and fact sheet

| Item | Rule or fact |
|---|---|
| Ticket flow | backlog, in progress, in review, merged, deployed |
| Order of work | reproduce, understand, fix, test, review, hand over |
| Reading code | run, entry point, trace one path, tests and history, precise question |
| Money in code | use `Decimal`, round once at the end, half-up as the accountant does |
| VAT (Nepal, general) | 13 percent standard rate; total = subtotal + VAT |
| Review questions | correct, edge cases, readable, tested, safe, in style |
| Hand-over page | done, run and test, how it works, known issues, next, who to ask |

## Chapter summary

- A ticket moves from backlog to deployed, and **somebody else sees it at every step**.
- Read an unfamiliar code base by running it, finding the entry point, tracing one path and asking one precise question.
- **Reproduce first**: HD-31 failed on 2 of 4 invoices because float 0.565 rounds down; `Decimal` rounding once gives 55.26.
- Tests (6 of 6 passing) prove the fix and document the promise; edge cases matter.
- Code review is normal, expected and educational; reply to every comment.
- A hand-over page makes the work usable after you leave.

## Practice

1. List the five states of a ticket and who acts at each.
2. Why should one ticket have one branch?
3. State the five steps of the code-base tour.
4. In Section 4.3, why does the float method give 55.25 for INV-102 while the exact method gives 55.26?
5. Compute the exact total for lines (2.50 × 2) and (0.50 × 1) with 13 percent VAT, rounded half-up once.
6. Why is a negative-quantity test useful?
7. List four questions a reviewer asks.
8. How should you reply if you disagree with a review comment?
9. What six headings does a hand-over page have?
10. Name three things to return when the internship ends.

::: note Answers and worked solutions
**1.** Backlog (reporter), in progress (author), in review (reviewer), merged (maintainer), deployed (operations or the team).
**2.** The diff stays small and focused, the review is quick and the change can be reverted without side effects.
**3.** Run it; find the entry point; trace one path; read tests and history; ask one precise question.
**4.** 0.50 × 1.13 is 0.565, which a binary float stores slightly below, so rounding gives 0.56; the exact decimal rounds half-up to 0.57 (or computes VAT once on the 48.90 subtotal: 6.36).
**5.** Subtotal 5.00 + 0.50 = 5.50; VAT = 0.715, rounded half-up to 0.72; total **6.22**. The per-line float method gives 5.65 + 0.56 = 6.21.
**6.** It proves that invalid input is rejected instead of producing a wrong total silently.
**7.** Is it correct, does it handle edge cases, is it readable, is it tested, is it safe, does it follow style.
**8.** Ask a polite question with your reason, accept the team's decision if they insist, and record what you learned.
**9.** What was done, how to run and test, how it works, known issues, what to do next, who to ask.
**10.** Badge, accounts and keys, and any firm data on personal devices.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Describe the life cycle of a ticket in a software team, with the example of HD-31.**

*Introduction.* A ticket is a written unit of work (bug, feature or chore) tracked on a board so that the team sees who is doing what. Its life cycle has five states (Figure 4.1).

*States.*

1. **Backlog.** The accountant reports that invoice totals differ by a paisa; the ticket HD-31 is created.
2. **In progress.** Anisha reproduces the failure, fixes it and writes tests on her own branch.
3. **In review.** Sanjay reads the diff and may request changes, which sends the ticket back to progress.
4. **Merged.** After approval and green tests, the change joins the main branch.
5. **Deployed.** The client's system now shows 55.26 for INV-102.

*Good habits.* One ticket, one branch, one purpose; define "done" first; update the ticket with findings. *Conclusion.* The life cycle makes every change visible, reviewed and reversible.

**Q2 (5 marks). Explain why reproducing a bug and writing tests are essential parts of fixing it. Use the VAT example.**

*Introduction.* A fix without proof is a guess. Reproducing shows the failure exists; tests show it is gone and stays gone.

*Reproduction.* The script in Section 4.3 compares the old float method and the exact method on four invoices. Two differ: INV-102 (55.25 against 55.26) and INV-103 (13.55 against 13.56), because 0.565 is stored slightly below its true value.

*Fix.* Use `Decimal`, add VAT once on the subtotal, round half-up once.

*Tests.* Six checks pass: a simple invoice, the half-paisa case, the two failing invoices, an empty invoice and a negative quantity that must raise an error.

*Benefits.* The failing case becomes a permanent regression test; edge cases are documented; reviewers trust the change. *Conclusion.* Reproduce, fix, test is the professional order, and it turns a lucky patch into a reliable one.

**Q3 (10 marks). Explain how an intern should make a technical contribution to a company project, from receiving a ticket to hand-over.**

*Introduction.* Technical contribution means making real, reviewed changes in a live system. The process is the same in every software company: understand, reproduce, fix, test, review, deploy, hand over. Ticket HD-31 illustrates each step.

*Steps.*

1. **Understand the ticket.** Write what "done" means before starting.
2. **Tour the code base.** Run it, find the entry point, trace one path, read tests and history, ask one precise question.
3. **Reproduce.** Obtain anonymised data and write the failing case: INV-102 gives 55.25 instead of 55.26.
4. **Fix.** Replace floats with `Decimal`, round once at the end, half-up.
5. **Test.** Write six tests including edge cases; all pass.
6. **Self-review.** Read your diff, remove debug lines, check for secrets, write a clear description (Plate 4.1c).
7. **Respond to review.** Answer every comment, fix the same day, and learn the team style.
8. **Hand over.** Write a one-page document: done, how to run, how it works, known issues, next steps, who to ask; return access.

| Stage | Output | Evidence |
|---|---|---|
| Reproduce | failing case | script output with 2 of 4 errors |
| Fix | small diff | ten changed lines |
| Test | suite | 6 passed, 0 failed |
| Review | approval | resolved comments |
| Hand over | docs page | file in `docs/` |

*Example.* After merge, the client's totals match the accountant to the paisa; Anisha's log and the hand-over page are cited in her report. *Conclusion.* Small, tested, reviewed and documented changes are what employers value; they are also the easiest to explain and defend in the viva.
