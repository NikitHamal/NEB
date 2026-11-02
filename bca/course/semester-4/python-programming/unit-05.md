---
subject: Python Programming
grade: BCA Semester 4
unit: 5
title: File Handling and Exception Handling
hours: 6
area: BCA 254 · Python Programming · Unit 5
---

Variables vanish when a program ends; files persist. And real programs meet trouble: a file that is missing, a number that is not a number, a network that is down. This unit shows how to store and retrieve data in text, CSV and JSON files, and how to handle errors so that a program fails gracefully instead of crashing.

::: key What this unit gives you
- Opening, reading, writing and appending files; the `with` statement; paths with `pathlib`.
- CSV and JSON files.
- Exceptions: `try`/`except`/`else`/`finally`, raising, custom exceptions, `assert`.
:::

All programs below write into a temporary working directory, so you can run them safely.

## 5.1 Text files

`open(name, mode, encoding=…)` returns a file object. Modes: `"r"` read (default), `"w"` write (truncates), `"a"` append, `"x"` create (fails if it exists), with `"b"` for binary and `"+"` for read/write. Always use **`with`**: it closes the file automatically, even if an error occurs. Always pass `encoding="utf-8"` for text.

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("BCA semester 4\n")
    f.writelines(["Operating Systems\n", "Numerical Methods\n"])
    print("Python Programming", file=f)

with open("notes.txt", "a", encoding="utf-8") as f:
    f.write("Web Technology II\n")

with open("notes.txt", encoding="utf-8") as f:
    print(repr(f.readline()))
    print([line.strip() for line in f][:2])

with open("notes.txt", encoding="utf-8") as f:
    content = f.read()
print(len(content), content.count("\n"), f.closed)
```
```output
'BCA semester 4\n'
['Operating Systems', 'Numerical Methods']
88 5 True
```
| Method | Returns |
|---|---|
| `read(n)` | up to *n* characters (all if omitted) |
| `readline()` | next line including `\n` |
| `readlines()` | list of all lines |
| `for line in f` | lines lazily (best for big files) |
| `write(s)`, `writelines(seq)` | writes text; **no** newline is added |
| `seek(pos)`, `tell()` | move/report the position |

Iterate over the file object rather than calling `readlines()` on huge files: it holds only one line in memory.

```python
with open("data.txt", "w") as f:
    f.write("12\n7\n x \n30\n")
total, bad = 0, 0
with open("data.txt") as f:
    for lineno, line in enumerate(f, start=1):
        try:
            total += int(line)
        except ValueError:
            bad += 1
            print(f"line {lineno}: skipped {line.strip()!r}")
print("total", total, "bad lines", bad)
```
```output
line 3: skipped 'x'
total 49 bad lines 1
```
### Paths with `pathlib`

```python
from pathlib import Path
p = Path("reports") / "2026" / "marks.txt"
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("Ram 80\nSita 92\n", encoding="utf-8")
print(p, p.suffix, p.stem, p.exists(), p.stat().st_size)
print(p.read_text(encoding="utf-8").splitlines())
print(sorted(x.name for x in Path("reports").rglob("*")))
p.unlink()
```
```output
reports/2026/marks.txt .txt marks True 15
['Ram 80', 'Sita 92']
['2026', 'marks.txt']
```
`Path` objects replace string slicing of paths and work on every operating system. `os.rename`, `os.remove` (or `Path.rename`, `Path.unlink`), `shutil.copy` handle renaming, deleting and copying.

### Binary files

`open(name, "rb")` and `"wb"` read and write **bytes**, used for images, PDFs and executables.

```python
data = bytes([72, 101, 108, 108, 111, 0, 255])
with open("blob.bin", "wb") as f:
    f.write(data)
with open("blob.bin", "rb") as f:
    back = f.read()
print(back, list(back), back == data, len(back))
```
```output
b'Hello\x00\xff' [72, 101, 108, 108, 111, 0, 255] True 7
```
## 5.2 CSV and JSON

**CSV** (comma-separated values) is the lingua franca of spreadsheets; **JSON** is the lingua franca of web APIs. The `csv` and `json` modules handle quoting and types correctly.

```python
import csv
rows = [["roll", "name", "marks"], [1, "Ram", 78], [2, "Sita, K.", 91], [3, "Hari", 64]]
with open("class.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)
print(open("class.csv", encoding="utf-8").read())
with open("class.csv", newline="", encoding="utf-8") as f:
    records = list(csv.DictReader(f))
print(records[1])
print(sum(int(r["marks"]) for r in records) / len(records))
```
```output
roll,name,marks
1,Ram,78
2,"Sita, K.",91
3,Hari,64

{'roll': '2', 'name': 'Sita, K.', 'marks': '91'}
77.66666666666667
```
Note that the comma inside `"Sita, K."` was quoted automatically, and that everything read back is a **string**: convert numbers yourself.

```python
import json
student = {"name": "Sita", "marks": [88, 92], "passed": True, "address": None}
text = json.dumps(student, indent=2)
print(text)
back = json.loads(text)
print(back == student, back["marks"][1])
with open("student.json", "w", encoding="utf-8") as f:
    json.dump(student, f)
print(json.load(open("student.json", encoding="utf-8"))["name"])
print(json.dumps({"tuple": (1, 2), "pi": 3.14}), json.loads('{"a": [1, 2, {"b": null}]}'))
```
```output
{
  "name": "Sita",
  "marks": [
    88,
    92
  ],
  "passed": true,
  "address": null
}
True 92
Sita
{"tuple": [1, 2], "pi": 3.14} {'a': [1, 2, {'b': None}]}
```
JSON maps `dict`↔object, `list`/`tuple`↔array, `str`, `int`/`float`, `True`/`False`↔`true`/`false`, `None`↔`null`. Sets and custom classes are not serialisable without help.

## 5.3 Errors and exceptions

Two kinds of error exist: **syntax errors** (found before the program runs) and **exceptions** (raised while it runs). An uncaught exception prints a **traceback** and ends the program.

```python
# raises
def average(values):
    return sum(values) / len(values)

print(average([4, 6]))
print(average([]))
```
```output
5.0
Traceback (most recent call last):
  File "p.py", line 6, in <module>
    print(average([]))
          ^^^^^^^^^^^
  File "p.py", line 3, in average
    return sum(values) / len(values)
           ~~~~~~~~~~~~^~~~~~~~~~~~~
ZeroDivisionError: division by zero
```
Read a traceback from the bottom: the last line names the exception and its message; the lines above show the chain of calls that led to it.

| Exception | Typical cause |
|---|---|
| `ZeroDivisionError` | `1 / 0` |
| `ValueError` | right type, wrong value: `int("abc")` |
| `TypeError` | wrong type: `"a" + 1` |
| `IndexError`, `KeyError` | bad list index, missing dict key |
| `FileNotFoundError` (an `OSError`) | opening a missing file |
| `AttributeError`, `NameError` | missing attribute, undefined name |
| `ImportError`, `StopIteration`, `RecursionError` | and many more |

## 5.4 Handling exceptions

```python
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("cannot divide by zero")
        return None
    except TypeError as e:
        print("bad operand types:", e)
        return None
    else:
        print("division succeeded")
        return result
    finally:
        print("(finally always runs)")

print(safe_divide(10, 4))
print(safe_divide(1, 0))
print(safe_divide("1", 2))
```
```output
division succeeded
(finally always runs)
2.5
cannot divide by zero
(finally always runs)
None
bad operand types: unsupported operand type(s) for /: 'str' and 'int'
(finally always runs)
None
```

- `try`: the code that might fail.
- `except Type as e`: handles that type (and subclasses); several `except` clauses are tried in order; `except (A, B)` handles either. Catch the **most specific** exception you can; a bare `except:` hides bugs.
- `else`: runs only if the `try` raised nothing.
- `finally`: always runs, for cleanup (closing connections, releasing locks).

```python
def read_marks(name):
    try:
        with open(name, encoding="utf-8") as f:
            return [int(x) for x in f.read().split()]
    except FileNotFoundError:
        return []
    except ValueError as e:
        raise ValueError(f"{name} contains a non-number") from e

print(read_marks("missing.txt"))
open("m.txt", "w").write("50 60 seventy")
try:
    read_marks("m.txt")
except ValueError as e:
    print("caught:", e, "| cause:", repr(e.__cause__))
```
```output
[]
caught: m.txt contains a non-number | cause: ValueError("invalid literal for int() with base 10: 'seventy'")
```
### Raising exceptions, custom exceptions, assert

```python
class InsufficientFunds(Exception):
    def __init__(self, balance, needed):
        super().__init__(f"balance {balance} is less than {needed}")
        self.balance, self.needed = balance, needed

def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise InsufficientFunds(balance, amount)
    return balance - amount

for amt in (300, 5000, -5):
    try:
        print("new balance:", withdraw(1000, amt))
    except InsufficientFunds as e:
        print("refused:", e, "- short by", e.needed - e.balance)
    except ValueError as e:
        print("invalid:", e)
```
```output
new balance: 700
refused: balance 1000 is less than 5000 - short by 4000
invalid: amount must be positive
```
`assert condition, message` checks a *programmer* assumption and raises `AssertionError` if false; it can be disabled with `python -O`, so never use it to validate user input.

```python
def sqrt_floor(n):
    assert n >= 0, "n must be non-negative"
    return int(n ** 0.5)

print(sqrt_floor(50))
try:
    sqrt_floor(-1)
except AssertionError as e:
    print("AssertionError:", e)
```
```output
7
AssertionError: n must be non-negative
```
**EAFP versus LBYL.** Python style prefers *"Easier to Ask Forgiveness than Permission"*: try the operation and handle the failure, rather than checking every condition first. It avoids race conditions (the file may vanish between the check and the open) and is often shorter.

## Formula and fact sheet

- `with open(f, "r"/"w"/"a", encoding="utf-8") as fh:`; iterate lines with `for line in fh`.
- `write` adds no newline; `csv` and `json` handle quoting and structure.
- `try / except Type as e / else / finally`; most specific `except` first.
- `raise Exc("msg")`; custom exceptions subclass `Exception`.
- `assert cond, msg` for internal assumptions only.

## Chapter summary

- Files are opened with `with`, read lazily by iteration, and written with `write`; `pathlib` handles paths; `csv` and `json` handle structured text.
- Exceptions separate normal logic from error handling; `try/except/else/finally` give precise control, and custom exceptions make errors meaningful.
- Handle only what you can handle; let other exceptions propagate.

## Practice

1. Write a program that writes five lines to a file, appends one more, and prints the line count.
2. Read numbers from a file, skipping lines that are not numbers, and print their total.
3. Differentiate `"w"`, `"a"` and `"x"` modes.
4. Why use `with open(...)`?
5. Write a function that converts a string to `int`, returning `None` if it is not a number.
6. What is the order in which `else` and `finally` run?
7. Define a custom exception `NegativeMarks` and raise it for marks below 0.
8. Save a list of dictionaries to JSON and read it back.

::: note Answers and worked solutions
**1.**

```python
with open("five.txt", "w") as f:
    for i in range(1, 6):
        f.write(f"line {i}\n")
with open("five.txt", "a") as f:
    f.write("line 6\n")
print(sum(1 for _ in open("five.txt")))
```
```output
6
```
**2.** See the `data.txt` program in Section 5.1.
**3.** `"w"` creates or empties the file; `"a"` creates or appends at the end; `"x"` creates a new file and raises `FileExistsError` if it already exists.
**4.** `with` guarantees the file is closed, even after an exception, so data is flushed and the file handle is not leaked.
**5.**

```python
def to_int(s):
    try:
        return int(s)
    except ValueError:
        return None
print(to_int("42"), to_int("4.2"), to_int("x"))
```
```output
42 None None
```
**6.** If the `try` succeeds: `try` → `else` → `finally`. If an exception is handled: `try` (up to the error) → `except` → `finally`. `finally` always runs last.
**7.**

```python
class NegativeMarks(Exception):
    pass

def check(m):
    if m < 0:
        raise NegativeMarks(f"marks cannot be negative: {m}")
    return m

try:
    check(-3)
except NegativeMarks as e:
    print(e)
```
```output
marks cannot be negative: -3
```
**8.**

```python
import json
people = [{"name": "Ram", "age": 19}, {"name": "Sita", "age": 20}]
json.dump(people, open("people.json", "w"))
print(json.load(open("people.json")) == people)
```
```output
True
```
:::
