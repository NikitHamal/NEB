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
