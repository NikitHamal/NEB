---
subject: Python Programming
grade: BCA Semester 4
unit: 9
title: Putting It Together: Three Complete Programs
hours: 4
area: BCA 254 · Python Programming · Unit 9
---

Knowing each tool is not the same as building something with them. This unit assembles the earlier units into three small but complete programs. Each is split into short, self-contained pieces so that you can run and understand it one step at a time. Each is also a template for the project work of this semester.

::: key What this unit gives you
- Project 1: a student-record manager (classes, JSON persistence, error handling).
- Project 2: a text analyser (files, dictionaries, regular expressions, sorting).
- Project 3: a bank with transactions in SQLite and custom exceptions.
:::

## 9.1 Project 1: student-record manager

**Requirements.** Store students with several marks; compute average and grade; save to and load from a JSON file; reject invalid marks.

```python
import json

class InvalidMark(ValueError):
    pass

class Student:
    def __init__(self, roll, name, marks=None):
        self.roll, self.name, self.marks = roll, name, list(marks or [])

    def add(self, mark):
        if not 0 <= mark <= 100:
            raise InvalidMark(f"{mark} is not between 0 and 100")
        self.marks.append(mark)

    @property
    def average(self):
        return sum(self.marks) / len(self.marks) if self.marks else 0.0

    @property
    def grade(self):
        a = self.average
        return "Distinction" if a >= 80 else "First" if a >= 60 else "Second" if a >= 45 else "Fail"

    def to_dict(self):
        return {"roll": self.roll, "name": self.name, "marks": self.marks}

s = Student(1, "Sita")
for m in (88, 92, 75):
    s.add(m)
try:
    s.add(120)
except InvalidMark as e:
    print("rejected:", e)
print(s.name, round(s.average, 2), s.grade, s.to_dict())
```
```output
rejected: 120 is not between 0 and 100
Sita 85.0 Distinction {'roll': 1, 'name': 'Sita', 'marks': [88, 92, 75]}
```
The second half stores a whole class in a file and reads it back.

```python
import json

class Student:
    def __init__(self, roll, name, marks=None):
        self.roll, self.name, self.marks = roll, name, list(marks or [])
    @property
    def average(self):
        return sum(self.marks) / len(self.marks) if self.marks else 0.0

class Register:
    def __init__(self):
        self.students = {}
    def add(self, st):
        self.students[st.roll] = st
    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([vars(s) for s in self.students.values()], f, indent=1)
    @classmethod
    def load(cls, path):
        reg = cls()
        with open(path, encoding="utf-8") as f:
            for d in json.load(f):
                reg.add(Student(**d))
        return reg
    def ranking(self):
        return sorted(self.students.values(), key=lambda s: -s.average)

reg = Register()
for roll, name, marks in [(1, "Sita", [88, 92]), (2, "Ram", [70, 64]), (3, "Hari", [95, 81, 90])]:
    reg.add(Student(roll, name, marks))
reg.save("register.json")
again = Register.load("register.json")
print([(s.name, round(s.average, 1)) for s in again.ranking()])
print(open("register.json").read().count("roll"), "records saved")
```
```output
[('Sita', 90.0), ('Hari', 88.7), ('Ram', 67.0)]
3 records saved
```
**Extensions:** a menu loop with `input()`, CSV export, a `Course` class, unit tests for `average` and `grade`.

## 9.2 Project 2: text analyser

**Requirements.** Count words, sentences and the most frequent words in a text file, ignoring common stop-words; report the longest word.

```python
import re
from collections import Counter

text = """Nepal is a land of mountains. The mountains of Nepal attract climbers from the world.
Climbers come in spring and autumn! Is Everest the only mountain? No: Nepal has eight of the world's
fourteen highest mountains."""
with open("sample.txt", "w", encoding="utf-8") as f:
    f.write(text)

STOP = {"the", "of", "is", "a", "in", "and", "from", "has", "no", "only"}
with open("sample.txt", encoding="utf-8") as f:
    raw = f.read()
words = re.findall(r"[a-z']+", raw.lower())
sentences = [s for s in re.split(r"[.!?]+", raw) if s.strip()]
print("words:", len(words), "| sentences:", len(sentences), "| distinct:", len(set(words)))
```
```output
words: 36 | sentences: 5 | distinct: 25
```
```python
import re
from collections import Counter
raw = """Nepal is a land of mountains. The mountains of Nepal attract climbers from the world.
Climbers come in spring and autumn! Is Everest the only mountain? No: Nepal has eight of the world's
fourteen highest mountains."""
STOP = {"the", "of", "is", "a", "in", "and", "from", "has", "no", "only"}
words = re.findall(r"[a-z']+", raw.lower())
content = [w for w in words if w not in STOP]
freq = Counter(content)
print(freq.most_common(4))
print("longest:", max(content, key=len), "| average length:", round(sum(map(len, content)) / len(content), 2))
print("capitalised:", sorted(set(re.findall(r"\b[A-Z][a-z]+\b", raw)))[:5])
```
```output
[('nepal', 3), ('mountains', 3), ('climbers', 2), ('land', 1)]
longest: mountains | average length: 6.6
capitalised: ['Climbers', 'Everest', 'Is', 'Nepal', 'No']
```
(Each block of this book is run on its own, so the second block repeats the text instead of reading `sample.txt`.) **Extensions:** read the file name from `sys.argv`, plot a bar chart of the top ten words, handle `FileNotFoundError`.

## 9.3 Project 3: a small bank in SQLite

**Requirements.** Accounts in a database; deposit and withdraw with a custom exception for insufficient funds; every change is a transaction and is recorded in a ledger; print a statement.

```python
import sqlite3

class InsufficientFunds(Exception):
    pass

class Bank:
    def __init__(self):
        self.con = sqlite3.connect(":memory:")
        self.con.executescript("""
            CREATE TABLE account (id INTEGER PRIMARY KEY, owner TEXT UNIQUE NOT NULL, balance INTEGER NOT NULL CHECK (balance >= 0));
            CREATE TABLE ledger (n INTEGER PRIMARY KEY AUTOINCREMENT, account_id INTEGER, kind TEXT, amount INTEGER);
        """)

    def open_account(self, owner, initial=0):
        with self.con:
            cur = self.con.execute("INSERT INTO account (owner, balance) VALUES (?, ?)", (owner, initial))
            self.con.execute("INSERT INTO ledger (account_id, kind, amount) VALUES (?, 'open', ?)", (cur.lastrowid, initial))
        return cur.lastrowid

    def change(self, acct, delta):
        with self.con:
            (bal,) = self.con.execute("SELECT balance FROM account WHERE id = ?", (acct,)).fetchone()
            if bal + delta < 0:
                raise InsufficientFunds(f"balance {bal}, tried to take {-delta}")
            self.con.execute("UPDATE account SET balance = balance + ? WHERE id = ?", (delta, acct))
            self.con.execute("INSERT INTO ledger (account_id, kind, amount) VALUES (?, ?, ?)",
                             (acct, "deposit" if delta > 0 else "withdraw", abs(delta)))

    def statement(self, acct):
        return self.con.execute("SELECT kind, amount FROM ledger WHERE account_id = ? ORDER BY n", (acct,)).fetchall()

bank = Bank()
ram = bank.open_account("Ram", 1000)
bank.change(ram, 500)
bank.change(ram, -200)
try:
    bank.change(ram, -5000)
except InsufficientFunds as e:
    print("refused:", e)
print(bank.statement(ram))
print(bank.con.execute("SELECT owner, balance FROM account").fetchall())
```
```output
refused: balance 1300, tried to take 5000
[('open', 1000), ('deposit', 500), ('withdraw', 200)]
[('Ram', 1300)]
```
The refused withdrawal leaves no trace in the ledger because the `with self.con:` block is one atomic transaction.

## 9.4 Habits of a good Python programmer

- Run `python -m unittest` before every commit; write the test for a bug before fixing it.
- Keep functions short and named for what they do; prefer comprehensions and the standard library to hand-written loops.
- Use `with` for resources, specific `except` clauses, and parameterised SQL.
- Follow PEP 8 (a linter such as `flake8` or `ruff` checks it) and document with docstrings.
- Work in a virtual environment and record dependencies in `requirements.txt`.
- Read other people's code; the standard library is excellent reading.

## 9.5 Seeing the ideas: from requirements to a working program

Each project of this unit has a real-world counterpart: a filing cabinet of student records, a body of text about Nepal's mountains to analyse, and a bank that must never lose a rupee. The figures follow the data through each program with real results from running the code.

```photogrid label="9.1" cols="3" ratio="1.25" caption="Three projects, three real settings. (a) A library card cabinet: every record has a key and is kept in order, as the roll numbers of Project 1 are kept in the Register and saved to a file. (b) Mount Everest and the Khumbu valley: the sample text analysed in Project 2 is about Nepal's mountains, and counting its words shows how much of a text is about what. (c) The head office of Nepal Rastra Bank: a bank must apply every deposit and withdrawal completely or not at all, which is what the transactions of Project 3 guarantee."
@ photo id="bca254/cabinet" cap="Card cabinet: records with keys"
fit 1.25
focus 0.5 0.5
@ photo id="bca254/everest" cap="Everest: text about mountains"
fit 1.25
focus 0.5 0.5
@ photo id="bca304/nrb" cap="Nepal Rastra Bank: safe money"
fit 1.25
focus 0.5 0.5
```

```svgfig label="9.1" caption="Project 1: how data flows. Each Student object holds a roll number, a name and marks, and computes its own average (real values shown). The Register keeps the objects in a dictionary keyed by roll number. save() turns each object into a plain dictionary with vars() and writes the whole list as JSON text; load() reads the JSON and rebuilds Student objects with Student(**d). The box on the right shows the first record exactly as json.dumps writes it."
import json
class Student:
    def __init__(self, roll, name, marks):
        self.roll, self.name, self.marks = roll, name, list(marks)
    @property
    def average(self):
        return sum(self.marks) / len(self.marks)
data = [(1, "Sita", [88, 92]), (2, "Ram", [70, 64]), (3, "Hari", [95, 81, 90])]
studs = [Student(*d) for d in data]
first = json.dumps(vars(studs[0]))
f = Fig(580, 190)
for i, s in enumerate(studs):
    f.box(8, 14 + i * 50, 130, 40, "", fill=BLUE, stroke=NAVY)
    f.text(73, 28 + i * 50, f"{s.roll}  {s.name}", size=11.5, color=NAVY, bold=True)
    f.text(73, 45 + i * 50, f"average {s.average:.1f}", size=10.5, color=SLATE)
    f.arrow([(140, 34 + i * 50), (184, 90)], color=SLATE, sw=1.3)
f.box(186, 50, 130, 80, "", fill=MINT, stroke=TEAL)
f.text(251, 70, "Register", size=12.5, color=TEAL, bold=True)
f.text(251, 90, "dict: roll -> Student", size=10, color=SLATE)
f.text(251, 108, "ranking(), add()", size=10, color=SLATE)
f.arrow([(318, 80), (352, 80)], color=NAVY, sw=1.6, label="save", lpos=(335, 72))
f.arrow([(352, 100), (318, 100)], color=TEAL, sw=1.6, label="load", lpos=(335, 118))
f.box(354, 40, 218, 100, "", fill=SAND, stroke=AMBER)
f.text(463, 56, "register.json", size=11.5, color=AMBER, bold=True)
f.text(364, 84, first, size=9.5, color=SLATE, anchor="start")
f.text(364, 104, "... one record per student", size=9.5, color=SLATE, anchor="start")
f.text(364, 122, "%d characters in all" % len(json.dumps([vars(s) for s in studs])), size=9.5, color=SLATE, anchor="start")
f.text(290, 180, "to_dict / vars() out, Student(**d) back in", size=10.5, color=NAVY, bold=True)
```

```svgfig label="9.2" caption="Project 2: the text analyser as a pipeline, with real counts. The raw text is cut into words by the pattern [a-z']+ on the lower-cased text, the stop-words are removed, and Counter tallies what is left. The bars are the real top four content words; ties (nepal and mountains, three each) keep the order in which they first appeared. Removing stop-words matters: without it, the, of and is would head the list and tell us nothing."
import re
from collections import Counter
raw = """Nepal is a land of mountains. The mountains of Nepal attract climbers from the world.
Climbers come in spring and autumn! Is Everest the only mountain? No: Nepal has eight of the world's
fourteen highest mountains."""
STOP = {"the", "of", "is", "a", "in", "and", "from", "has", "no", "only"}
words = re.findall(r"[a-z']+", raw.lower())
content = [w for w in words if w not in STOP]
freq = Counter(content)
top = freq.most_common(4)
f = Fig(580, 196)
steps = [("raw text", "3 lines"), ("findall", "%d words" % len(words)), ("remove stop-words", "%d left" % len(content)), ("Counter", "%d distinct" % len(freq))]
for i, (a, b) in enumerate(steps):
    x = 8 + i * 145
    f.box(x, 8, 128, 44, "", fill=BLUE, stroke=NAVY)
    f.text(x + 64, 24, a, size=11, color=NAVY, bold=True)
    f.text(x + 64, 41, b, size=10.5, color=SLATE)
    if i < 3:
        f.arrow([(x + 130, 30), (x + 143, 30)], color=SLATE, sw=1.5)
f.text(8, 80, "most_common(4)", size=11, color=TEAL, bold=True, anchor="start")
for i, (w, c) in enumerate(top):
    y = 90 + i * 24
    f.text(100, y + 11, w, size=11.5, color=NAVY, bold=True, anchor="end", vmid=True)
    f.box(108, y, 60 * c, 20, "", fill=MINT, stroke=TEAL, r=3)
    f.text(108 + 60 * c + 8, y + 11, str(c), size=11.5, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(330, 110, "longest content word: %s" % max(content, key=len), size=10.5, color=SLATE, anchor="start")
f.text(330, 130, "average length: %.2f letters" % (sum(map(len, content)) / len(content)), size=10.5, color=SLATE, anchor="start")
f.text(330, 150, "sentences: %d" % len([s for s in re.split(r"[.!?]+", raw) if s.strip()]), size=10.5, color=SLATE, anchor="start")
```

```svgfig label="9.3" caption="Project 3: what Bank.change does. It reads the balance, and one test decides the path: if balance + delta would be negative it raises InsufficientFunds and the with-block rolls everything back, otherwise it updates the account and writes a ledger line and the block commits. On the right are the real results of the run in Section 9.3: the refusal message, the ledger (open 1000, deposit 500, withdraw 200) and the final balance 1300; the refused withdrawal left no ledger line."
import sqlite3
class InsufficientFunds(Exception):
    pass
con = sqlite3.connect(":memory:")
con.executescript("CREATE TABLE account (id INTEGER PRIMARY KEY, owner TEXT, balance INTEGER CHECK (balance >= 0)); CREATE TABLE ledger (n INTEGER PRIMARY KEY AUTOINCREMENT, account_id INTEGER, kind TEXT, amount INTEGER);")
con.execute("INSERT INTO account VALUES (1, 'Ram', 1000)")
con.execute("INSERT INTO ledger (account_id, kind, amount) VALUES (1, 'open', 1000)")
def change(delta):
    with con:
        (bal,) = con.execute("SELECT balance FROM account WHERE id = 1").fetchone()
        if bal + delta < 0:
            raise InsufficientFunds("balance %d, tried to take %d" % (bal, -delta))
        con.execute("UPDATE account SET balance = balance + ? WHERE id = 1", (delta,))
        con.execute("INSERT INTO ledger (account_id, kind, amount) VALUES (1, ?, ?)", ("deposit" if delta > 0 else "withdraw", abs(delta)))
change(500); change(-200)
msg = ""
try:
    change(-5000)
except InsufficientFunds as e:
    msg = str(e)
led = con.execute("SELECT kind, amount FROM ledger ORDER BY n").fetchall()
fin = con.execute("SELECT balance FROM account").fetchone()[0]
f = Fig(580, 214)
f.box(10, 8, 170, 34, "change(acct, delta)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(95, 44), (95, 62)], color=SLATE, sw=1.5)
f.box(10, 64, 170, 34, "read the balance", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(95, 100), (95, 116)], color=SLATE, sw=1.5)
f.poly([(95, 118), (178, 146), (95, 174), (12, 146)], fill=SAND, stroke=AMBER, label="balance + delta < 0 ?", lx=95, ly=146, size=9.5, color=AMBER)
f.arrow([(95, 176), (95, 200)], color=TEAL, sw=1.5)
f.text(105, 189, "no", size=10, color=TEAL, bold=True, anchor="start")
f.text(95, 211, "UPDATE + ledger, COMMIT", size=10, color=TEAL, bold=True)
f.arrow([(180, 146), (210, 146)], color=RED, sw=1.5)
f.box(212, 130, 130, 32, "raise InsufficientFunds", fill="#ffffff", stroke=RED, size=9.5, bold=True)
f.text(195, 138, "yes", size=10, color=RED, bold=True)
f.text(277, 178, "ROLLBACK, no ledger line", size=10, color=RED, bold=True)
f.text(360, 22, "real results", size=11.5, color=NAVY, bold=True, anchor="start")
f.text(360, 46, "refused: " + msg, size=10, color=RED, anchor="start")
for i, (k, a) in enumerate(led):
    f.box(360, 62 + i * 26, 150, 22, "%s  %d" % (k, a), fill=MINT, stroke=TEAL, size=11, bold=True)
f.text(360, 62 + len(led) * 26 + 14, "final balance: %d" % fin, size=11.5, color=TEAL, bold=True, anchor="start")
```

```svgfig label="9.4" caption="Testing the grade boundaries of Project 1. The bar is the average from 0 to 100 split into the four grades. Bugs hide at the edges, so the tests pick the last value of one band and the first of the next: 44 and 45, 59 and 60, 79 and 80. The labels come from calling the real grade function; each pair must show a change of grade. These six values are the unit tests asked for in Practice question 4, and boundary tests of this kind are the cheapest way to find an off-by-one mistake (for example writing the wrong comparison operator)."
def grade(a):
    return "Distinction" if a >= 80 else "First" if a >= 60 else "Second" if a >= 45 else "Fail"
f = Fig(580, 176)
x0, k = 30, 5.2
bands = [(0, 45, "Fail", SAND, AMBER), (45, 60, "Second", BLUE, NAVY), (60, 80, "First", MINT, TEAL), (80, 100, "Distinction", "#ede9fe", "#6d28d9")]
for a, b, n, fl, st in bands:
    f.box(x0 + a * k, 20, (b - a) * k, 40, n, fill=fl, stroke=st, size=11, bold=True, r=2)
for v in (0, 45, 60, 80, 100):
    f.text(x0 + v * k, 74, str(v), size=10.5, color=SLATE, bold=True)
pairs = [(44, 45, 120), (59, 60, 300), (79, 80, 470)]
for a, b, cx in pairs:
    bx = x0 + (b * k if False else (a + 1) * k)
    f.arrow([(cx, 112), (bx, 80)], color=SLATE, sw=1.2)
    f.box(cx - 78, 114, 156, 50, "", fill=SOFT, stroke=SLATE)
    f.text(cx, 130, "%d -> %s" % (a, grade(a)), size=11, color=NAVY, bold=True)
    f.text(cx, 150, "%d -> %s" % (b, grade(b)), size=11, color=TEAL, bold=True)
f.text(290, 10, "average marks", size=10, color=SLATE)
```

### 9.5.1 Eight steps for building a small program properly

1. **Write the requirements first.** Say in plain sentences what the program must do and what it must refuse, such as "store marks, compute the grade, reject marks above 100". A student writing a result system for a college can turn each sentence into a test later. Unclear requirements cause more rework than any coding mistake.
2. **Model the things as classes.** A `Student`, a `Register` and a `Bank` match the nouns in the requirements, with their data and actions together (Fig. 9.1). The class names then read like the problem itself. This makes the program easier to explain to a teacher or a client.
3. **Keep storage separate from logic.** The `Student` class should not know whether it is saved to JSON or to SQLite. Only `Register.save` and `Register.load` deal with the file. When a college later moves from a JSON file to a database, only that part changes.
4. **Check input and raise clear exceptions.** `InvalidMark` and `InsufficientFunds` say exactly what went wrong, and the caller can answer each one differently. A Fonepay-style app can show "balance too low" instead of a long error trace. Catch specific exceptions, never a bare `except`.
5. **Build the smallest working piece first.** Start with one student and one mark, run it, and then add the file and the ranking. Small steps mean that a bug is always in the last few lines you wrote. Large untested programs hide their bugs for days.
6. **Test the boundaries.** Grade changes at 45, 60 and 80, so test 44 and 45, 59 and 60, 79 and 80 (Fig. 9.4). A test costs a minute to write and can save an unfair result sheet. Run all tests before every commit.
7. **Use transactions when money or marks change together.** A deposit changes the balance and writes a ledger line, and both must happen or neither (Fig. 9.3). The `with con:` block gives this for free in SQLite. This is the rule that protects wallets and fee accounts.
8. **Read, tidy and document.** After the program works, rename unclear variables, shorten long functions, add docstrings and follow PEP 8. Reading code written by others, such as the standard library, teaches patterns faster than any book. A program that is easy to read is easy to fix.

## Formula and fact sheet

- Structure: classes for entities, a manager class for collections, JSON/SQLite for persistence, custom exceptions for rule violations.
- `json.dump(vars(obj))` / `Cls(**dict)`; `Counter(...).most_common(n)`; `with con:` for transactions.

## Chapter summary

- Small programs combine classes, files, text processing, databases and exceptions; keep the pieces short and independent.
- Persistence can be a JSON file for small data or SQLite for structured, transactional data.
- Tests, parameterised queries and clear errors turn scripts into dependable software.

## Practice

1. Extend Project 1 with a method that returns students who failed (average below 40).
2. Modify Project 2 to report the three longest words and the number of sentences ending in `?`.
3. Add a `transfer(src, dst, amount)` method to the bank that is atomic.
4. Write three unit tests for `Student.grade` boundaries (45, 60, 80).
5. Which exceptions can occur when loading `register.json`, and how would you handle each?

::: note Answers and worked solutions
**1.**

```python
class Student:
    def __init__(self, name, marks):
        self.name, self.marks = name, marks
    @property
    def average(self):
        return sum(self.marks) / len(self.marks)

students = [Student("A", [30, 35]), Student("B", [70, 80]), Student("C", [20, 50])]
print([s.name for s in students if s.average < 40])
```
```output
['A', 'C']
```
**2.**

```python
import re
raw = "Is Everest high? Nepal has mountains. Extraordinary peaks! Are they climbed? Yes."
words = re.findall(r"[A-Za-z']+", raw)
print(sorted(set(words), key=len, reverse=True)[:3], len(re.findall(r"\?", raw)))
```
```output
['Extraordinary', 'mountains', 'climbed'] 2
```
**3.** Do both updates inside one `with self.con:` block so that either both happen or neither does; check the balance first and raise `InsufficientFunds`:

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.executescript("CREATE TABLE a (id INTEGER PRIMARY KEY, bal INTEGER CHECK (bal >= 0)); INSERT INTO a VALUES (1, 100), (2, 50);")
def transfer(src, dst, amt):
    with con:
        con.execute("UPDATE a SET bal = bal - ? WHERE id = ?", (amt, src))
        con.execute("UPDATE a SET bal = bal + ? WHERE id = ?", (amt, dst))
transfer(1, 2, 70)
try:
    transfer(1, 2, 70)
except sqlite3.IntegrityError:
    print("second transfer rolled back")
print(con.execute("SELECT id, bal FROM a").fetchall())
```
```output
second transfer rolled back
[(1, 30), (2, 120)]
```
**4.**

```python
import io, unittest
def grade(a):
    return "Distinction" if a >= 80 else "First" if a >= 60 else "Second" if a >= 45 else "Fail"
class T(unittest.TestCase):
    def test_45(self): self.assertEqual(grade(45), "Second")
    def test_60(self): self.assertEqual(grade(60), "First")
    def test_80(self): self.assertEqual(grade(80), "Distinction")
r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(T))
print(r.testsRun, r.wasSuccessful())
```
```output
3 True
```
**5.** `FileNotFoundError` (no file yet: start with an empty register), `json.JSONDecodeError` (corrupt file: report and keep a backup), `KeyError`/`TypeError` (missing or wrong fields: validate the records). Catch each specifically and give a helpful message.
:::

## Model answers (5 and 10 marks)

**Q1. Design and write a student-record manager in Python with classes, validation, file storage and ranking. Explain the design. (10 marks)**

**Introduction.** A student-record manager keeps the roll number, name and marks of each student, computes the average and the grade, rejects impossible marks, saves the records to a file and loads them again. It is a good first complete program because it uses classes, exceptions, files and sorting together. The design follows three layers: one class for **one student**, one class for the **collection** (the register), and a **file format** (JSON) for storage (Fig. 9.1).

**Design.**

1. **Requirements.** Store several marks per student; compute the average; give the grade (Distinction at 80 or more, First at 60, Second at 45, otherwise Fail); refuse marks outside 0 to 100; save and load; rank by average.
2. **`Student` class.** Holds `roll`, `name` and `marks`. The method `add` checks the mark and raises the custom exception `InvalidMark`; the properties `average` and `grade` compute their values when asked, so they are never out of date.
3. **`Register` class.** Keeps a dictionary from roll number to `Student`, so a student is found directly by roll number. Its `save` method writes `vars(student)` of every student as JSON, and the class method `load` rebuilds the objects with `Student(**d)`.
4. **Ranking.** `sorted(..., key=lambda s: -s.average)` sorts from the highest average to the lowest.
5. **Errors.** `InvalidMark` for wrong marks; `FileNotFoundError` and `json.JSONDecodeError` when loading are handled by the caller with specific `except` clauses.

```python
import json

class InvalidMark(ValueError):
    pass

class Student:
    def __init__(self, roll, name, marks=None):
        self.roll, self.name, self.marks = roll, name, list(marks or [])
    def add(self, mark):
        if not 0 <= mark <= 100:
            raise InvalidMark(f"{mark} is not between 0 and 100")
        self.marks.append(mark)
    @property
    def average(self):
        return sum(self.marks) / len(self.marks) if self.marks else 0.0
    @property
    def grade(self):
        a = self.average
        return "Distinction" if a >= 80 else "First" if a >= 60 else "Second" if a >= 45 else "Fail"

class Register:
    def __init__(self):
        self.students = {}
    def add(self, st):
        self.students[st.roll] = st
    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([vars(s) for s in self.students.values()], f)
    @classmethod
    def load(cls, path):
        reg = cls()
        with open(path, encoding="utf-8") as f:
            for d in json.load(f):
                reg.add(Student(**d))
        return reg
    def ranking(self):
        return sorted(self.students.values(), key=lambda s: -s.average)

reg = Register()
for roll, name, marks in [(1, "Sita", [88, 92]), (2, "Ram", [70, 64]), (3, "Hari", [95, 81, 90]), (4, "Gita", [40, 35])]:
    reg.add(Student(roll, name, marks))
try:
    reg.students[2].add(130)
except InvalidMark as e:
    print("rejected:", e)
reg.save("r.json")
again = Register.load("r.json")
print([(s.name, round(s.average, 1), s.grade) for s in again.ranking()])
try:
    Register.load("missing.json")
except FileNotFoundError:
    print("file not found handled")
```
```output
rejected: 130 is not between 0 and 100
[('Sita', 90.0, 'Distinction'), ('Hari', 88.7, 'Distinction'), ('Ram', 67.0, 'First'), ('Gita', 37.5, 'Fail')]
file not found handled
```
**Comparison of storage choices.**

| Storage | Good for | Weakness |
|---|---|---|
| JSON file | small data, easy to read and share | whole file rewritten; no queries; no transactions |
| SQLite | structured data, queries, transactions | needs SQL knowledge |

**Extensions.** A menu loop with `input()`, CSV export, a `Course` class and unit tests for `average` and `grade` (Fig. 9.4).

**Conclusion.** Separating the student, the register and the file format keeps each part short and testable; custom exceptions and boundary tests make the program dependable.

**Q2. What is a custom exception? Explain with a bank example how exceptions and transactions keep data safe. (5 marks)**

**Introduction.** A **custom exception** is a new exception class, usually written as a subclass of `Exception` or `ValueError`, that names a problem of your own program, such as `InsufficientFunds`. Python's built-in exceptions describe technical problems, but a custom one describes a rule of the application, so the caller can catch exactly that case and answer it properly.

**Main points.**

1. **Define:** `class InsufficientFunds(Exception): pass`; the class body can be empty because the name carries the meaning.
2. **Raise:** `raise InsufficientFunds("balance 1300, tried to take 5000")` stops the current function at the point of the rule violation.
3. **Catch:** `except InsufficientFunds as e:` handles only this case, so other errors are not hidden.
4. **Transaction:** the `with con:` block of `sqlite3` commits if the block finishes and rolls back if any exception leaves it. The refused withdrawal therefore changes nothing and writes no ledger line (Fig. 9.3).
5. **Database rule as a second guard:** `CHECK (balance >= 0)` stops a negative balance even if the Python check were forgotten.

```python
import sqlite3

class InsufficientFunds(Exception):
    pass

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE account (id INTEGER PRIMARY KEY, balance INTEGER CHECK (balance >= 0))")
con.execute("INSERT INTO account VALUES (1, 1300)")
con.commit()

def withdraw(amount):
    with con:
        (bal,) = con.execute("SELECT balance FROM account WHERE id = 1").fetchone()
        if amount > bal:
            raise InsufficientFunds(f"balance {bal}, tried to take {amount}")
        con.execute("UPDATE account SET balance = balance - ? WHERE id = 1", (amount,))

withdraw(300)
try:
    withdraw(5000)
except InsufficientFunds as e:
    print("refused:", e)
print(con.execute("SELECT balance FROM account").fetchone()[0])
```
```output
refused: balance 1000, tried to take 5000
1000
```
**Example.** A wallet application can show "balance too low" for `InsufficientFunds` and "try again later" for a database error, because the two cases are different exception classes.

**Conclusion.** Custom exceptions name the rules of the application, and a transaction makes sure that a refused operation leaves the data exactly as it was.

**Q3. Describe how Python can analyse a text file to count words and find the most frequent words. Write a program. (5 marks)**

**Introduction.** Text analysis turns a block of text into numbers: how many words, how many sentences, which words are used most. It is the first step of search engines, spam filters and survey analysis. In Python it needs only three tools: **regular expressions** to cut the text into words, a **set of stop-words** to ignore common words such as "the", and `collections.Counter` to count.

**Main points.**

1. **Read.** `with open(path, encoding="utf-8") as f: raw = f.read()` reads the file and closes it afterwards.
2. **Split into words.** `re.findall(r"[a-z']+", raw.lower())` lower-cases the text and returns every run of letters; lower-casing makes "Nepal" and "nepal" the same word.
3. **Split into sentences.** `re.split(r"[.!?]+", raw)` cuts at full stops, exclamation marks and question marks; empty pieces are dropped.
4. **Remove stop-words.** A list comprehension keeps only words not in the `STOP` set; a set makes each test fast.
5. **Count.** `Counter(content).most_common(4)` returns the four most frequent words with their counts, as in Fig. 9.2.

```python
import re
from collections import Counter

raw = """Nepal is a land of mountains. The mountains of Nepal attract climbers from the world.
Climbers come in spring and autumn! Is Everest the only mountain? No: Nepal has eight of the world's
fourteen highest mountains."""
STOP = {"the", "of", "is", "a", "in", "and", "from", "has", "no", "only"}
words = re.findall(r"[a-z']+", raw.lower())
sentences = [s for s in re.split(r"[.!?]+", raw) if s.strip()]
content = [w for w in words if w not in STOP]
print(len(words), len(sentences), len(content))
print(Counter(content).most_common(3))
print(sum(1 for s in re.findall(r"[^.!?]*\?", raw)), "question")
```
```output
36 5 20
[('nepal', 3), ('mountains', 3), ('climbers', 2)]
1 question
```
**Example.** Reading a notice of a hundred lines and printing its five most frequent content words shows its topic at a glance; replacing `most_common(4)` with `most_common(5)` is the only change needed.

**Conclusion.** Regex for words, a stop-word set for noise and `Counter` for counting make a text analyser of about ten lines.

**Q4. Write a program for a bank with an atomic `transfer` method between two accounts and test it with `unittest`. Explain the design. (10 marks)**

**Introduction.** A **transfer** moves money from one account to another and has two steps: take from the source and add to the destination. If the first step succeeds and the second fails, money disappears; so both steps must form one **atomic transaction**. A program like the one behind a Fonepay transfer must also refuse a transfer larger than the balance and must leave a ledger of every change. We build a small version with SQLite (Fig. 9.3) and check it with tests (Fig. 8.5).

**Design.**

1. **Tables.** `account(id, owner, balance)` with `CHECK (balance >= 0)`, and `ledger(n, account_id, kind, amount)` as a record that is only added to, never changed.
2. **Class `Bank`.** One method `open_account`, one method `transfer(src, dst, amount)` and one method `balance(acct)`.
3. **Atomic transfer.** Inside one `with self.con:` block: read the source balance, raise `InsufficientFunds` if it is too small, subtract from the source, add to the destination, and write two ledger lines. Any exception rolls back all of it.
4. **Validation.** The amount must be positive (`ValueError` otherwise), and an unknown account must raise an error instead of creating money.
5. **Tests.** A good transfer changes both balances and the sum stays the same; a refused transfer changes nothing; the total money in the bank never changes.

```python
import sqlite3, unittest, io

class InsufficientFunds(Exception):
    pass

class Bank:
    def __init__(self):
        self.con = sqlite3.connect(":memory:")
        self.con.executescript("""
            CREATE TABLE account (id INTEGER PRIMARY KEY, owner TEXT, balance INTEGER NOT NULL CHECK (balance >= 0));
            CREATE TABLE ledger (n INTEGER PRIMARY KEY AUTOINCREMENT, account_id INTEGER, kind TEXT, amount INTEGER);
        """)
    def open_account(self, owner, initial):
        with self.con:
            return self.con.execute("INSERT INTO account (owner, balance) VALUES (?, ?)", (owner, initial)).lastrowid
    def balance(self, acct):
        return self.con.execute("SELECT balance FROM account WHERE id = ?", (acct,)).fetchone()[0]
    def transfer(self, src, dst, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        with self.con:
            bal = self.balance(src)
            if bal < amount:
                raise InsufficientFunds(f"balance {bal}, tried to move {amount}")
            self.con.execute("UPDATE account SET balance = balance - ? WHERE id = ?", (amount, src))
            self.con.execute("UPDATE account SET balance = balance + ? WHERE id = ?", (amount, dst))
            self.con.execute("INSERT INTO ledger (account_id, kind, amount) VALUES (?, 'out', ?)", (src, amount))
            self.con.execute("INSERT INTO ledger (account_id, kind, amount) VALUES (?, 'in', ?)", (dst, amount))

class BankTests(unittest.TestCase):
    def setUp(self):
        self.b = Bank()
        self.a, self.c = self.b.open_account("Ram", 1000), self.b.open_account("Sita", 200)
    def test_good_transfer(self):
        self.b.transfer(self.a, self.c, 300)
        self.assertEqual((self.b.balance(self.a), self.b.balance(self.c)), (700, 500))
    def test_refused_changes_nothing(self):
        with self.assertRaises(InsufficientFunds):
            self.b.transfer(self.a, self.c, 5000)
        self.assertEqual((self.b.balance(self.a), self.b.balance(self.c)), (1000, 200))
        self.assertEqual(self.b.con.execute("SELECT COUNT(*) FROM ledger").fetchone()[0], 0)
    def test_total_is_constant(self):
        self.b.transfer(self.a, self.c, 1000)
        self.assertEqual(self.b.balance(self.a) + self.b.balance(self.c), 1200)
    def test_bad_amount(self):
        with self.assertRaises(ValueError):
            self.b.transfer(self.a, self.c, 0)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(BankTests)
result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
print("ran", result.testsRun, "failures", len(result.failures), "errors", len(result.errors))
```
```output
ran 4 failures 0 errors 0
```
**Why the design is safe.**

| Danger | Protection |
|---|---|
| Failure between debit and credit | one `with self.con:` transaction |
| Overdraft | Python check and `CHECK (balance >= 0)` |
| Injection through names or ids | `?` parameters only |
| Lost history | append-only ledger written in the same transaction |
| Silent breakage later | the four tests run before every commit |

**Conclusion.** An atomic transfer, a rule enforced both in Python and in the database, an append-only ledger and automatic tests together give a small bank that cannot create or lose money.
