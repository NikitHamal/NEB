---
subject: Python Programming
grade: BCA Semester 4
unit: 1
title: Introduction to Python and Basic Elements
hours: 6
area: BCA 254 · Python Programming · Unit 1
---

Python is the language in which you can write a working program on the first day and still be productive in your tenth year. It is used for web back ends, data analysis, automation, teaching, and most of artificial intelligence. In this unit you will run your first programs and learn the basic vocabulary: values, variables, types, operators and input/output.

::: key What this unit gives you
- What Python is, its features, versions and how to run it.
- Identifiers, keywords, variables, dynamic typing, indentation and comments.
- Numbers, strings, booleans, `None`; operators and precedence; type conversion.
- Console input and output; useful built-in functions.
:::

Every code block in this book was executed with **Python 3.12**; the output shown below each block is the real output.

## 1.1 What is Python?

Python was created by Guido van Rossum (first released 1991). It is **interpreted** (code is run by the interpreter without a separate compile-and-link step), **dynamically typed** (a variable has no declared type; values do), **high-level**, **object-oriented** (and also procedural and functional), and has a very large **standard library** ("batteries included") plus hundreds of thousands of third-party packages on PyPI.

| Feature | Meaning |
|---|---|
| Simple, readable syntax | indentation instead of braces; close to pseudo-code |
| Interpreted, cross-platform | the same source runs on Windows, Linux and macOS |
| Dynamic typing and automatic memory management | no type declarations; a garbage collector frees memory |
| Large standard library and ecosystem | files, networks, dates, databases, testing, data science |
| Free and open source | PSF licence |

**Applications:** web development (Django, Flask), data analysis and visualisation (NumPy, Pandas, Matplotlib), machine learning (scikit-learn, PyTorch), automation and scripting, scientific computing, education, game prototypes, embedded boards (MicroPython). **Limitations:** slower than C or Java for heavy numeric loops (use NumPy or compiled extensions), and less suited to mobile apps or hard real-time code.

**Versions.** Python 2 ended in 2020; always use **Python 3**. Features used here need Python 3.10 or later (`match`) and 3.8 or later (the walrus operator, f-string `=`).

### Installing and running

Install from python.org (Windows: tick "Add Python to PATH"), or use `sudo apt install python3` on Ubuntu. Three ways to run code:

1. **Interactive interpreter (REPL)**: type `python` (or `python3`) and enter statements at the `>>>` prompt; ideal for experiments.
2. **Script mode**: save code in `hello.py` and run `python hello.py`.
3. **IDEs and notebooks**: IDLE (bundled), VS Code, PyCharm, Jupyter notebooks.

```python
print("Namaste, Nepal!")
print(2 + 3 * 4)
```
```output
Namaste, Nepal!
14
```
## 1.2 Tokens: identifiers, keywords, comments, indentation

An **identifier** names a variable, function or class. Rules: letters (including Unicode), digits and underscore; cannot start with a digit; case-sensitive (`marks` ≠ `Marks`); cannot be a keyword. Convention (PEP 8): `snake_case` for variables and functions, `CapWords` for classes, `UPPER_CASE` for constants.

**Keywords** are reserved words. Python 3.12 has 35 of them; you can list them yourself:

```python
import keyword
print(len(keyword.kwlist))
print(keyword.kwlist[:12])
print(keyword.iskeyword("lambda"), keyword.iskeyword("print"))
```
```output
35
['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def']
True False
```
`print` is a built-in function, not a keyword, so it *can* be (mis)used as a variable name; do not.

**Comments** start with `#` and run to the end of the line. A string literal used as the first statement of a function or module is a **docstring** (documentation, retrievable with `help()`).

**Indentation** is syntax. A block (the body of `if`, `for`, `def`) is the set of lines indented by the same amount (four spaces by convention). Mixing tabs and spaces or wrong indentation raises `IndentationError`. **Statements** end at the line end; a long statement can continue inside brackets or after a backslash; several statements may share a line with `;` (avoid).

## 1.3 Variables and dynamic typing

A variable is a *name bound to an object*. Assignment `x = 5` does not copy a value into a box; it makes the name `x` refer to an `int` object. The same name can later refer to an object of a different type, and several names can refer to the same object.

```python
x = 10
print(x, type(x), id(x) == id(10))
x = "ten"
print(x, type(x))
a = b = 7
a, b = b + 1, a
print(a, b)
```
```output
10 <class 'int'> True
ten <class 'str'>
8 7
```
`a, b = b + 1, a` evaluates the right side first (8, 7), then assigns: tuple unpacking makes swapping a one-liner. **Constants** do not exist as a language feature; capitalised names signal "do not change".

## 1.4 Data types

| Type | Example | Notes |
|---|---|---|
| `int` | `42`, `-7`, `0b101`, `0o17`, `0xFF`, `1_000_000` | unlimited size |
| `float` | `3.14`, `2e-3` | IEEE 754 double, ~15–17 significant digits |
| `complex` | `3 + 4j` | `.real`, `.imag` |
| `bool` | `True`, `False` | subclass of `int` (`True == 1`) |
| `str` | `"Pokhara"`, `'it''s'`, `"""multi-line"""` | immutable sequence of Unicode characters |
| `NoneType` | `None` | absence of a value |
| `list`, `tuple`, `range` | `[1, 2]`, `(1, 2)`, `range(5)` | sequences (Unit 3) |
| `set`, `dict` | `{1, 2}`, `{"a": 1}` | unordered collection, mapping (Unit 3) |

```python
print(2 ** 100)
print(0.1 + 0.2, 0.1 + 0.2 == 0.3)
print(abs(0.1 + 0.2 - 0.3) < 1e-9)
print(type(3), type(3.0), type(3 + 4j), type(True), type("3"), type(None))
print(True + True, isinstance(True, int))
```
```output
1267650600228229401496703205376
0.30000000000000004 False
True
<class 'int'> <class 'float'> <class 'complex'> <class 'bool'> <class 'str'> <class 'NoneType'>
2 True
```
Integers never overflow, but floats are **binary** approximations: 0.1 + 0.2 is 0.30000000000000004. Compare floats with a tolerance (`math.isclose`), never with `==`.

## 1.5 Operators

| Category | Operators | Notes |
|---|---|---|
| Arithmetic | `+ - * / // % **` | `/` always gives a float; `//` floors; `%` has the sign of the divisor; `**` is power |
| Comparison | `== != < > <= >=` | can be chained: `1 < x < 10` |
| Logical | `and or not` | short-circuit; return one of the operands |
| Bitwise | `& \| ^ ~ << >>` | on integers |
| Assignment | `= += -= *= /= //= %= **= &= \|= ^= <<= >>=` | augmented forms |
| Identity | `is`, `is not` | same object? |
| Membership | `in`, `not in` | in a sequence, set, dict keys |

```python
print(7 / 2, 7 // 2, -7 // 2, 7 % 3, -7 % 3, 2 ** 10)
print(divmod(17, 5), round(2.5), round(3.5), round(3.14159, 2))
print(5 & 3, 5 | 3, 5 ^ 3, ~5, 1 << 4, 256 >> 2)
x = 5
print(1 < x < 10, x > 3 and x < 4, not x == 5)
print("" or "default", 0 and 99, [] or [1])
print("a" in "banana", 3 not in [1, 2, 3])
```
```output
3.5 3 -4 1 2 1024
(3, 2) 2 4 3.14
1 7 6 -6 16 64
True False False
default 0 [1]
True False
```
Python's `round` uses *banker's rounding* (round half to even): `round(2.5)` is 2.

### Precedence and associativity

From highest to lowest: `**`; unary `+ - ~`; `* / // %`; `+ -`; shifts; `&`; `^`; `|`; comparisons, `is`, `in`; `not`; `and`; `or`; conditional `x if c else y`; assignment. Most operators associate left to right; `**` associates **right to left**: `2 ** 3 ** 2` is `2 ** 9`. When in doubt, use parentheses.

```python
print(2 + 3 * 4 ** 2 / 8)
print(2 ** 3 ** 2, (2 ** 3) ** 2)
print(-3 ** 2, (-3) ** 2)
print(not True or True, not (True or True))
```
```output
8.0
512 64
-9 9
True False
```
## 1.6 Type conversion

Python does **implicit** conversion in mixed arithmetic (`int` + `float` gives `float`) but never between strings and numbers; use **explicit** conversion functions `int()`, `float()`, `str()`, `bool()`, `list()`, `tuple()`, `set()`.

```python
print(3 + 4.5, int("42") + 1, float("2.5"), str(99) + "!")
print(int(3.99), int(-3.99), int("101", 2), bin(10), hex(255))
print(bool(0), bool(""), bool([]), bool("False"), bool(-1))
try:
    int("12.5")
except ValueError as e:
    print("ValueError:", e)
```
```output
7.5 43 2.5 99!
3 -3 5 0b1010 0xff
False False False True True
ValueError: invalid literal for int() with base 10: '12.5'
```
**Truthiness.** In a condition, `0`, `0.0`, `""`, `[]`, `()`, `{}`, `set()` and `None` are false; everything else is true.

## 1.7 Console input and output

`print(*objects, sep=" ", end="\n", file=...)` writes text; `input(prompt)` reads a line and **always returns a string**. Convert it if you need a number.

```python
print("a", "b", "c", sep="-")
print("no newline", end=" | ")
print("same line")
name, marks = "Sita", 87.456
print(f"{name} scored {marks:.1f} ({marks / 100:.1%})")
print(f"{255:#x} {255:08b} {1234567.891:,.2f} {'left':<8}|{'right':>8}|")
print("%s has %d credits" % ("BCA", 126))
print("{} and {}".format("tea", "momo"))
```
```output
a-b-c
no newline | same line
Sita scored 87.5 (87.5%)
0xff 11111111 1,234,567.89 left    |   right|
BCA has 126 credits
tea and momo
```
The **f-string** (`f"…{expr:format}…"`) is the modern way to format; the specification after the colon controls width, alignment, precision and base. To read data, you write:

```python
# noexec
name = input("Name: ")
age = int(input("Age: "))
print(f"{name} will be {age + 1} next year")
```
(That block is not executed here because it waits for the keyboard.) The next program feeds `input` from a prepared string so that its output can be shown:

```python
import io, sys
sys.stdin = io.StringIO("Ram\n19\n")
name = input("Name: ")
age = int(input("Age: "))
print(f"{name} will be {age + 1} next year")
```
```output
Name: Age: Ram will be 20 next year
```
## 1.8 Useful built-in functions

| Function | Purpose | Example |
|---|---|---|
| `type(x)`, `isinstance(x, T)` | type of an object | `isinstance(3, int)` |
| `len(s)` | number of items | `len("momo") == 4` |
| `min`, `max`, `sum`, `abs` | aggregates | `sum([1, 2, 3])` |
| `round`, `pow`, `divmod` | arithmetic helpers | `pow(2, 10, 1000)` |
| `sorted`, `reversed`, `enumerate`, `zip` | iteration helpers | (Unit 3) |
| `range` | arithmetic sequence | `range(2, 10, 3)` |
| `help(x)`, `dir(x)`, `id(x)` | introspection | `dir("")` lists string methods |
| `chr`, `ord` | character ↔ code | `ord("A") == 65` |

```python
print(len("Kathmandu"), min(4, 9, 2), max("apple", "pear"), sum(range(1, 101)))
print(pow(2, 10), pow(2, 10, 1000), chr(65), ord("a"), abs(-3.5))
print(list(range(2, 20, 5)), list(reversed("abc")))
import math
print(math.sqrt(144), math.pi, math.floor(-2.5), math.ceil(-2.5), math.gcd(12, 18))
```
```output
9 2 pear 5050
1024 24 A 97 3.5
[2, 7, 12, 17] ['c', 'b', 'a']
12.0 3.141592653589793 -3 -2 6
```
**Importing libraries.** `import math` loads a module; `from math import sqrt` imports a name; `import numpy as np` gives an alias. Unit 4 covers modules in depth.

## Formula and fact sheet

- Python: interpreted, dynamically typed, indentation-delimited, batteries included.
- Types: `int`, `float`, `complex`, `bool`, `str`, `None`, collections.
- `/` true division, `//` floor division, `%` modulo, `**` power (right-associative).
- Truthy/falsy: empty or zero values are false. `and`/`or` return an operand.
- f-string: `f"{value:width.precisiontype}"`.
- `input()` returns `str`.

## Chapter summary

- Python is a readable, interpreted, general-purpose language with a rich library; use Python 3.
- Variables are names bound to objects; types belong to objects, not names.
- Operators follow a precedence table; floats are approximate; use parentheses and tolerances.
- Convert types explicitly; format output with f-strings.

## Practice

1. List five features of Python and two limitations.
2. Which of these are valid identifiers: `_total`, `2marks`, `class`, `Total_1`, `my-var`?
3. Predict the output of `print(7 // 2, -7 // 2, 7 % -3, 2 ** 3 ** 2)`.
4. Explain why `0.1 + 0.2 == 0.3` is `False` and how to compare floats correctly.
5. What does `input()` return? Write a program that reads two numbers and prints their average to two decimals.
6. What is the value of `bool("False")`? Explain.
7. Write one statement that swaps two variables without a temporary.
8. Show how to print `Total = 1,234,567.50` from the number 1234567.5 using an f-string.

::: note Answers and worked solutions
**1.** Features: simple syntax, interpreted, dynamic typing, large standard library, cross-platform, open source. Limitations: slower than compiled languages for tight numeric loops; weaker on mobile and hard real-time systems.
**2.** Valid: `_total`, `Total_1`. Invalid: `2marks` (starts with a digit), `class` (keyword), `my-var` (hyphen is the minus operator).
**3.** Run:

```python
print(7 // 2, -7 // 2, 7 % -3, 2 ** 3 ** 2)
```
```output
3 -4 -2 512
```
Floor division rounds toward minus infinity (3 and −4); `7 % -3` takes the sign of the divisor (−2); `**` is right-associative (2 ** 9 = 512).
**4.** 0.1 and 0.2 have no exact binary representation, so the sum is 0.30000000000000004. Compare with a tolerance:

```python
import math
print(0.1 + 0.2 == 0.3, math.isclose(0.1 + 0.2, 0.3))
```
```output
False True
```
**5.** `input()` returns a string. Program (input simulated):

```python
import io, sys
sys.stdin = io.StringIO("7\n10\n")
a = float(input())
b = float(input())
print(f"Average = {(a + b) / 2:.2f}")
```
```output
Average = 8.50
```
**6.** `bool("False")` is `True`: any non-empty string is truthy; only the empty string is false.
**7.** `a, b = b, a`.
**8.**

```python
total = 1234567.5
print(f"Total = {total:,.2f}")
```
```output
Total = 1,234,567.50
```
:::
