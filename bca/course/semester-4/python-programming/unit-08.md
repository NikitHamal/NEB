---
subject: Python Programming
grade: BCA Semester 4
unit: 8
title: Regular Expressions, Databases and Testing
hours: 5
area: BCA 254 · Python Programming · Unit 8
---

Three tools turn a Python script into a dependable program: **regular expressions** to find structure in text, **SQLite** to store data in a real database without installing a server, and **unit tests** to check that the code still works after every change.

::: key What this unit gives you
- Regular expressions with the `re` module.
- Working with SQLite from Python: create, insert, query, update, parameters, transactions.
- Unit testing with `unittest`; virtual environments and `pip` in brief.
:::

## 8.1 Regular expressions

A **regular expression (regex)** is a pattern describing a set of strings. The `re` module searches, matches and replaces with them. Always write patterns as **raw strings** `r"…"` so that backslashes reach the regex engine.

| Pattern | Meaning |
|---|---|
| `.` | any character except newline |
| `\d \w \s` | digit; letter, digit or underscore; whitespace (capitals negate) |
| `^ $` | start, end of string |
| `* + ? {m,n}` | 0 or more; 1 or more; 0 or 1; between m and n repeats |
| `[abc] [a-z] [^0-9]` | character class; range; negated class |
| `( )` `\|` | group; alternation |
| `\b` | word boundary |

```python
import re
text = "Call 9841234567 or 01-4412345; mail ram@tu.edu.np, sita.k@bca.com.np by 2026-11-02."
print(re.findall(r"\b98\d{8}\b", text))
print(re.findall(r"[\w.]+@[\w.]+\w", text))
m = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
print(m.group(0), m.groups(), m.span())
print(re.sub(r"\d", "#", "Roll 42, Ph 98"), re.split(r"[,;]\s*", "a, b;c,d"))
print(bool(re.fullmatch(r"[A-Z]{3}\d{3}", "BCA254")), bool(re.fullmatch(r"[A-Z]{3}\d{3}", "bca254")))
```
```output
['9841234567']
['ram@tu.edu.np', 'sita.k@bca.com.np']
2026-11-02 ('2026', '11', '02') (72, 82)
Roll ##, Ph ## ['a', 'b', 'c', 'd']
True False
```
`findall` returns all matches; `search` finds the first anywhere; `match` anchors at the start; `fullmatch` needs the whole string to match; `sub` replaces; `split` splits; `compile` pre-builds a pattern. **Named groups** `(?P<year>\d{4})` make results self-documenting. Patterns are **greedy** by default (`.*` takes as much as possible); add `?` (`.*?`) for the shortest match.

```python
import re
log = '203.0.113.5 - [02/Nov/2026:10:15:32] "GET /result.php?id=14 HTTP/1.1" 200 512'
pat = re.compile(r'(?P<ip>[\d.]+) - \[(?P<when>[^\]]+)\] "(?P<method>\w+) (?P<path>\S+)[^"]*" (?P<status>\d{3})')
m = pat.match(log)
print(m.groupdict())
print(re.findall(r"<b>(.*?)</b>", "<b>one</b> and <b>two</b>"), re.findall(r"<b>(.*)</b>", "<b>one</b> and <b>two</b>"))
```
```output
{'ip': '203.0.113.5', 'when': '02/Nov/2026:10:15:32', 'method': 'GET', 'path': '/result.php?id=14', 'status': '200'}
['one', 'two'] ['one</b> and <b>two']
```
Regexes are powerful but easy to misuse. For well-formed formats such as HTML or JSON, use a real parser. Validate e-mail addresses loosely and confirm by sending a message.

## 8.2 SQLite from Python

**SQLite** is a complete SQL database stored in a single file, included with Python as the `sqlite3` module. The SQL itself is the subject of Semester III's DBMS book. Here is the Python side.

```python
import sqlite3
con = sqlite3.connect(":memory:")          # use a filename for a persistent database
cur = con.cursor()
cur.execute("""CREATE TABLE student (
                 roll INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 dept TEXT,
                 marks REAL CHECK (marks BETWEEN 0 AND 100))""")
rows = [(1, "Ram", "BCA", 78.5), (2, "Sita", "BCA", 91.0), (3, "Hari", "BIT", 64.0), (4, "Gita", "BIT", 85.5)]
cur.executemany("INSERT INTO student VALUES (?, ?, ?, ?)", rows)
con.commit()
for row in cur.execute("SELECT name, marks FROM student WHERE marks > ? ORDER BY marks DESC", (70,)):
    print(row)
print(cur.execute("SELECT dept, COUNT(*), AVG(marks) FROM student GROUP BY dept").fetchall())
```
```output
('Sita', 91.0)
('Gita', 85.5)
('Ram', 78.5)
[('BCA', 2, 84.75), ('BIT', 2, 74.75)]
```
**Always pass values as parameters** (`?`), never by pasting them into the SQL text with f-strings: parameters make **SQL injection** impossible (Web Technology II shows the attack).

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.row_factory = sqlite3.Row
con.execute("CREATE TABLE acct (id INTEGER PRIMARY KEY, owner TEXT, bal REAL CHECK (bal >= 0))")
con.executemany("INSERT INTO acct (owner, bal) VALUES (?, ?)", [("Ram", 500), ("Sita", 300)])
con.commit()

def transfer(src, dst, amount):
    try:
        with con:                                  # one transaction: commit or roll back
            con.execute("UPDATE acct SET bal = bal - ? WHERE id = ?", (amount, src))
            con.execute("UPDATE acct SET bal = bal + ? WHERE id = ?", (amount, dst))
        return "ok"
    except sqlite3.IntegrityError as e:
        return f"rolled back: {e}"

print(transfer(1, 2, 200), [tuple(r) for r in con.execute("SELECT owner, bal FROM acct")])
print(transfer(1, 2, 900), [tuple(r) for r in con.execute("SELECT owner, bal FROM acct")])
```
```output
ok [('Ram', 300.0), ('Sita', 500.0)]
rolled back: CHECK constraint failed: bal >= 0 [('Ram', 300.0), ('Sita', 500.0)]
```
The second transfer would make Ram's balance negative; the `CHECK` constraint raises `IntegrityError`, and the `with con:` block **rolls back** the whole transaction, so no money is lost or created: the ACID properties from DBMS in action. Other drivers (MySQL Connector, psycopg2) follow the same pattern (Python's DB-API): connect, cursor, execute, fetch, commit.

## 8.3 Unit testing with `unittest`

A **unit test** checks one small piece of behaviour automatically. Tests protect against regressions when you change code (Software Engineering, Unit 6).

```python
import io, unittest

def grade(m):
    if not 0 <= m <= 100:
        raise ValueError("marks out of range")
    return "A" if m >= 80 else "B" if m >= 60 else "C" if m >= 40 else "F"

class GradeTests(unittest.TestCase):
    def test_bands(self):
        self.assertEqual([grade(m) for m in (85, 65, 45, 10)], ["A", "B", "C", "F"])
    def test_boundaries(self):
        self.assertEqual((grade(80), grade(79), grade(40), grade(39)), ("A", "B", "C", "F"))
    def test_invalid(self):
        with self.assertRaises(ValueError):
            grade(101)
    def test_deliberate_failure(self):
        self.assertEqual(grade(60), "A")        # wrong on purpose

suite = unittest.defaultTestLoader.loadTestsFromTestCase(GradeTests)
result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
print("ran", result.testsRun, "failures", len(result.failures), "errors", len(result.errors))
print([ln for ln in result.failures[0][1].splitlines() if ln.startswith("AssertionError")][0])
```
```output
ran 4 failures 1 errors 0
AssertionError: 'B' != 'A'
```
A test class extends `unittest.TestCase`; methods starting with `test` are run, each with its own fresh `self`; `assertEqual`, `assertTrue`, `assertRaises`, `assertAlmostEqual` check results. Run a file's tests with `python -m unittest`. The deliberate failure shows how a failing test reports the expected and actual values. **pytest** is a popular third-party runner with shorter syntax (plain `assert`). Good tests are small, independent, fast and cover boundaries (as in the BVA technique).

## 8.4 Virtual environments and pip

Different projects need different library versions. A **virtual environment** is an isolated folder of packages:

```text
python -m venv venv                  # create
source venv/bin/activate             # Linux/macOS    (Windows: venv\Scripts\activate)
pip install requests pandas          # install into the environment
pip freeze > requirements.txt        # record exact versions
pip install -r requirements.txt      # recreate elsewhere
deactivate
```

Commit `requirements.txt` (not the `venv` folder) to version control, so that a teammate can rebuild the same environment.

## Formula and fact sheet

- Regex: `.`, `\d`, `\w`, `\s`, `* + ? {m,n}`, `[...]`, `( )`, `|`, `^ $`; raw strings; greedy vs lazy `*?`.
- `re.findall`, `search`, `match`, `fullmatch`, `sub`, `split`, `compile`.
- `sqlite3.connect`, `cursor.execute(sql, params)`, `executemany`, `commit`; `with con:` is a transaction. Parameters, not f-strings.
- `unittest.TestCase`, `assertEqual`, `assertRaises`; `python -m unittest`.
- `python -m venv`, `pip install`, `pip freeze`.

## Chapter summary

- Regular expressions find and transform text patterns; raw strings and named groups keep them readable.
- `sqlite3` gives a zero-setup SQL database; parameterised queries stop injection and `with con:` gives atomic transactions.
- Unit tests make change safe; virtual environments keep projects reproducible.

## Practice

1. Write a regex that matches Nepali mobile numbers (ten digits starting with 98 or 97) and test it.
2. Extract all years (four digits) from a sentence.
3. Explain greedy and non-greedy matching with an example.
4. Create an SQLite table, insert three rows and print those above the average.
5. Why must queries use `?` placeholders?
6. Write two unit tests for a function `is_even`.
7. What is the purpose of a virtual environment?

::: note Answers and worked solutions
**1.**

```python
import re
pat = re.compile(r"^9[78]\d{8}$")
print([bool(pat.match(n)) for n in ("9841234567", "9751234567", "9641234567", "98412345")])
```
```output
[True, True, False, False]
```
**2.**

```python
import re
print(re.findall(r"\b\d{4}\b", "TU began in 1959; BCA in 2074 BS and 2017 AD."))
```
```output
['1959', '2074', '2017']
```
**3.** Greedy `.*` takes the longest possible match; `.*?` the shortest (Section 8.1 shows `<b>(.*)</b>` returning one long match and `<b>(.*?)</b>` returning two).
**4.**

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE t (name TEXT, marks REAL)")
con.executemany("INSERT INTO t VALUES (?, ?)", [("a", 50), ("b", 80), ("c", 90)])
print(con.execute("SELECT name FROM t WHERE marks > (SELECT AVG(marks) FROM t)").fetchall())
```
```output
[('b',), ('c',)]
```
**5.** Placeholders send the values separately from the SQL text, so input like `'; DROP TABLE t; --` is treated as data, not as SQL, which prevents SQL injection; they also handle quoting and types.
**6.**

```python
import io, unittest
def is_even(n):
    return n % 2 == 0
class T(unittest.TestCase):
    def test_even(self): self.assertTrue(is_even(10))
    def test_odd(self): self.assertFalse(is_even(7))
r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(T))
print(r.testsRun, r.wasSuccessful())
```
```output
2 True
```
**7.** It isolates a project's packages and versions from the system and from other projects, so that dependency conflicts are avoided and the environment can be recreated from `requirements.txt`.
:::
