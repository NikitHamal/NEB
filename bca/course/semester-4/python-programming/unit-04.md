---
subject: Python Programming
grade: BCA Semester 4
unit: 4
title: Functions, Modules and Packages
hours: 7
area: BCA 254 · Python Programming · Unit 4
---

A function is a named, reusable piece of code. Functions let you write a solution once and use it a hundred times, test it separately and give a complicated idea a short name. Modules group related functions into files, and packages group modules into folders, which is how a large program is kept understandable.

::: key What this unit gives you
- Defining and calling functions; parameters, default and keyword arguments, `*args` and `**kwargs`, return values.
- Scope (LEGB), recursion, lambda, `map`/`filter`, closures, decorators, generators.
- Modules, packages, the `__name__` idiom, and a tour of the standard library.
:::

## 4.1 Defining and calling functions

```python
def area(length, width=1):
    """Return the area of a rectangle."""
    return length * width

print(area(5, 3), area(4), area(width=2, length=10))
print(area.__doc__)
```
```output
15 4 20
Return the area of a rectangle.
```
`def` creates a function object. **Parameters** are the names in the definition; **arguments** are the values passed. Arguments can be **positional** or **keyword** (`name=value`); a parameter with a **default** may be omitted. A function without `return` returns `None`. A function can return several values (really one tuple).

```python
def stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

lo, hi, mean = stats([4, 8, 15, 16, 23, 42])
print(lo, hi, round(mean, 2))
print(stats([1, 2, 3]))
```
```output
4 42 18.0
(1, 3, 2.0)
```
### Flexible parameter lists

```python
def total(*args, **kwargs):
    print("args:", args, "kwargs:", kwargs)
    return sum(args) * kwargs.get("scale", 1)

print(total(1, 2, 3))
print(total(1, 2, 3, scale=10))

def greet(name, /, greeting="Hello", *, punctuation="!"):
    return f"{greeting}, {name}{punctuation}"

print(greet("Sita"), greet("Ram", "Namaste", punctuation="."))
nums = [3, 4]
print(max(*nums), dict(**{"a": 1}))
```
```output
args: (1, 2, 3) kwargs: {}
6
args: (1, 2, 3) kwargs: {'scale': 10}
60
Hello, Sita! Namaste, Ram.
4 {'a': 1}
```
`*args` collects extra positional arguments into a tuple; `**kwargs` collects extra keyword arguments into a dict. Parameters before `/` are positional-only; those after a bare `*` are keyword-only. At a call, `*seq` and `**mapping` **unpack**.

### The mutable-default trap

Default values are created **once**, when the function is defined. A mutable default is therefore shared between calls.

```python
def bad(item, bucket=[]):
    bucket.append(item)
    return bucket

def good(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket

print(bad(1), bad(2), bad(3))
print(good(1), good(2), good(3))
```
```output
[1, 2, 3] [1, 2, 3] [1, 2, 3]
[1] [2] [3]
```
### Arguments are passed by object reference

A function receives references to the caller's objects. Mutating a mutable argument changes the caller's object; rebinding the parameter name does not.

```python
def modify(lst, n):
    lst.append(99)
    n += 1
    lst = [0]
    return n

a, k = [1, 2], 10
print(modify(a, k), a, k)
```
```output
11 [1, 2, 99] 10
```
## 4.2 Scope: the LEGB rule

Names are looked up in order: **L**ocal (the current function), **E**nclosing (outer functions), **G**lobal (module), **B**uilt-in. Assigning to a name inside a function makes it local unless declared `global` or `nonlocal`.

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        nonlocal x
        x = "changed by inner"
    inner()
    return x

counter = 0
def bump():
    global counter
    counter += 1

bump(); bump()
print(outer(), x, counter)
```
```output
changed by inner global 2
```
Avoid `global` where you can; pass values in and return results.

## 4.3 Recursion

A function that calls itself, with a **base case** that stops and a **recursive case** that moves toward it.

```python
def fact(n):
    return 1 if n <= 1 else n * fact(n - 1)

def fib(n, memo={0: 0, 1: 1}):
    if n not in memo:
        memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]

def hanoi(n, a, b, c):
    return 0 if n == 0 else hanoi(n - 1, a, c, b) + 1 + hanoi(n - 1, c, b, a)

print(fact(10), fib(50), hanoi(10, "A", "B", "C"))
import sys
print(sys.getrecursionlimit())
```
```output
3628800 12586269025 1023
1000
```
The deliberate use of a mutable default for `memo` is a *memoisation cache*. Python limits recursion depth (about 1000 frames by default), so very deep recursion should be rewritten as a loop. `fib(50)` would take minutes without the cache.

## 4.4 Anonymous functions and functional tools

A **lambda** is a one-expression anonymous function: `lambda x, y: x + y`. Common with `sorted`, `map`, `filter`.

```python
square = lambda x: x * x
nums = [1, 2, 3, 4, 5, 6]
print(square(7), list(map(square, nums)), list(filter(lambda n: n % 2, nums)))
words = ["fig", "banana", "kiwi", "apple"]
print(sorted(words, key=len), max(words, key=lambda w: w[-1]))
from functools import reduce
print(reduce(lambda a, b: a * b, nums), [n * n for n in nums if n % 2])
```
```output
49 [1, 4, 9, 16, 25, 36] [1, 3, 5]
['fig', 'kiwi', 'apple', 'banana'] kiwi
720 [1, 9, 25]
```
Comprehensions are often clearer than `map`/`filter`.

## 4.5 Closures, decorators and generators

A **closure** is an inner function that remembers variables of the enclosing function. A **decorator** wraps a function to add behaviour.

```python
import functools

def make_counter():
    count = 0
    def step():
        nonlocal count
        count += 1
        return count
    return step

def logged(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}{args} -> {result}")
        return result
    return wrapper

@logged
def add(a, b):
    return a + b

c = make_counter()
print(c(), c(), c())
add(2, 3)
```
```output
1 2 3
add(2, 3) -> 5
```
A **generator** function uses `yield` to produce values one at a time and remembers its state between them. It is memory-efficient for long or infinite sequences.

```python
def evens(limit):
    n = 0
    while n < limit:
        yield n
        n += 2

g = evens(10)
print(next(g), next(g), list(g))
print(sum(x * x for x in range(1_000_000)))
```
```output
0 2 [4, 6, 8]
333332833333500000
```
## 4.6 Modules and packages

A **module** is a file of Python code (`mylib.py`). `import mylib` runs it once and gives access through `mylib.name`; `from mylib import name` imports a name directly; `import mylib as m` aliases it. Python searches the current directory, then `sys.path` (installed packages, standard library).

The following program creates a small module on disk, imports it, and shows the `__name__` idiom: a file's `__name__` is `"__main__"` when it is run directly and its module name when imported, so test code can be guarded.

```python
import importlib, pathlib, sys
pathlib.Path("shapes.py").write_text('''
PI = 3.14159

def circle_area(r):
    return PI * r * r

if __name__ == "__main__":
    print("running directly:", circle_area(1))
''')
sys.path.insert(0, ".")
import shapes
print(shapes.__name__, shapes.circle_area(2), shapes.PI)
from shapes import circle_area as ca
print(ca(10))
print(sorted(n for n in dir(shapes) if not n.startswith("_")))
```
```output
shapes 12.56636 3.14159
314.159
['PI', 'circle_area']
```
A **package** is a directory containing modules (and traditionally an `__init__.py`); `import pkg.sub.mod` reaches into it. Install third-party packages with `pip install name` (use a **virtual environment**, `python -m venv venv`, to keep each project's packages separate).

### A tour of the standard library

```python
import math, random, datetime, collections, itertools, statistics, string
random.seed(7)
print(math.hypot(3, 4), math.factorial(6), round(math.log(100, 10), 3), math.isclose(0.1 * 3, 0.3))
print(random.randint(1, 6), random.choice("abc"), random.sample(range(10), 3))
d = datetime.date(2026, 11, 2)
print(d.strftime("%A %d %B %Y"), (d + datetime.timedelta(days=100)).isoformat())
print(collections.Counter("mississippi").most_common(2))
print(list(itertools.permutations("abc", 2))[:4], list(itertools.combinations(range(4), 2)))
print(statistics.mean([2, 4, 4, 6]), statistics.median([1, 3, 9]), string.ascii_lowercase[:5])
```
```output
5.0 720 2.0 True
3 a [6, 0, 1]
Monday 02 November 2026 2027-02-10
[('i', 4), ('s', 4)]
[('a', 'b'), ('a', 'c'), ('b', 'a'), ('b', 'c')] [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
4 3 abcde
```
`random.seed(7)` makes the "random" numbers reproducible. Other useful modules: `os` and `pathlib` (files), `sys`, `json`, `csv`, `re`, `sqlite3`, `argparse`, `logging`, `unittest`, `urllib`, `decimal`, `fractions`.

## 4.7 Seeing the ideas: bricks, scopes and the call stack

A function is a brick: a small, named piece that you can build, test and reuse, and a module or package is a box of such bricks. The plate shows real bricks beside the scope rule that decides which names a function can see. The figures then follow a recursive call down and back up the call stack, and show why a naive recursive Fibonacci repeats work that a cache removes.

```photogrid label="4.1" cols="2" ratio="1.0" caption="Small parts, one big program. (a) A heap of plastic bricks: each brick has a standard connector, so any brick can join any other. A function has a standard interface in the same way (its name, parameters and return value), and a module is a labelled box of bricks. (b) The LEGB rule: Python looks for a name first in the Local scope, then in any Enclosing function, then in the Global (module) scope, and last in the Built-in scope, and it uses the first match."
@ photo id="bca254/lego" cap="Standard bricks, many models"
fit 1.0
focus 0.5 0.5
call 0.5 0.5 0.04 0.9 "reusable parts"
@ svg cap="LEGB: where Python looks for a name"
f = Fig(300, 300)
f.box(6, 6, 288, 288, "", fill=SOFT, stroke=SLATE)
f.text(18, 20, "B  built-in:  len, print, range", size=10.5, color=SLATE, bold=True, anchor="start")
f.box(18, 34, 264, 244, "", fill=SAND, stroke=AMBER)
f.text(30, 50, "G  global (module):  x = 'global'", size=10.5, color=AMBER, bold=True, anchor="start")
f.box(30, 64, 240, 196, "", fill=BLUE, stroke=NAVY)
f.text(42, 80, "E  enclosing:  y = 'outer'", size=10.5, color=NAVY, bold=True, anchor="start")
f.box(42, 94, 216, 150, "", fill=MINT, stroke=TEAL)
f.text(54, 110, "L  local:  z = 'inner'", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(150, 150, "print(z, y, x, len)", size=11, color=NAVY, bold=True)
f.text(150, 172, "z found in L", size=10, color=TEAL)
f.text(150, 188, "y found in E", size=10, color=NAVY)
f.text(150, 204, "x found in G", size=10, color=AMBER)
f.text(150, 220, "len found in B", size=10, color=SLATE)
```

```svgfig label="4.1" caption="The call stack of factorial(4). Each call pushes a new frame that waits for the call below it. The deepest call, factorial(1), is the base case and returns 1 without calling again; the frames then pop one by one, each multiplying its n by the value that came back. The values on the right are computed by the cell. If the base case were missing, the stack would grow until Python stops it with a RecursionError."
import math
f = Fig(580, 214)
N = 4
f.text(110, 14, "calls go down (push)", size=10.5, color=NAVY, bold=True)
f.text(450, 14, "values come back (pop)", size=10.5, color=TEAL, bold=True)
for i in range(N):
    n = N - i
    y = 24 + i * 42
    fill = MINT if n == 1 else BLUE
    f.box(30 + i * 22, y, 170, 34, f"factorial({n})", fill=fill, stroke=TEAL if n == 1 else NAVY, size=11.5, bold=True)
    val = math.factorial(n)
    rhs = "base case: 1" if n == 1 else f"{n} x {math.factorial(n - 1)} = {val}"
    f.box(330 + (N - 1 - i) * 0, y, 230, 34, rhs, fill=MINT if n == 1 else SAND, stroke=TEAL if n == 1 else AMBER, size=11, bold=True)
    if i < N - 1:
        f.arrow([(115 + i * 22, y + 35), (126 + i * 22, y + 41)], color=NAVY, sw=1.5)
f.arrow([(318, 188), (266, 188)], color=TEAL, sw=1.5, dash=True)
f.arrow([(330, 40), (210, 40)], color=TEAL, sw=1.2, dash=True)
f.text(290, 208, f"depth = {N} frames,  result = {math.factorial(N)}", size=10.5, color=SLATE, bold=True)
```

```svgfig label="4.2" caption="The call tree of fib(5) with plain recursion. The same sub-problems are solved again and again: fib(3) appears twice, fib(2) three times and fib(1) five times (amber circles are repeats of fib(2)). The cell counts the calls: 15 for fib(5). A cache (functools.lru_cache) remembers each answer after its first computation, so only 6 distinct calls are needed. The gap grows quickly: fib(30) takes 2,692,537 plain calls but only 31 cached ones."
calls = []
def build(n, d):
    node = {"n": n, "d": d, "kids": []}
    calls.append(node)
    if n > 1:
        node["kids"] = [build(n - 1, d + 1), build(n - 2, d + 1)]
    return node
root = build(5, 0)
leaf = [0]
def place(nd):
    if not nd["kids"]:
        nd["x"] = leaf[0]; leaf[0] += 1
    else:
        for k in nd["kids"]: place(k)
        nd["x"] = sum(k["x"] for k in nd["kids"]) / 2
place(root)
f = Fig(580, 222)
def px(nd): return 30 + nd["x"] * 50
def py(nd): return 26 + nd["d"] * 38
for nd in calls:
    for k in nd["kids"]:
        f.line(px(nd), py(nd), px(k), py(k), color=SLATE, sw=1.2)
for nd in calls:
    rep = nd["n"] == 2
    f.circle(px(nd), py(nd), 13, fill=SAND if rep else BLUE, stroke=AMBER if rep else NAVY, label=f"f{nd['n']}", size=10, color=AMBER if rep else NAVY)
total = len(calls)
cnt = {}
for nd in calls: cnt[nd["n"]] = cnt.get(nd["n"], 0) + 1
def calls_of(n): return 1 if n < 2 else 1 + calls_of(n - 1) + calls_of(n - 2)
f.box(414, 40, 160, 120, "", fill=SOFT, stroke=SLATE)
f.text(494, 56, f"plain calls = {total}", size=11, color=RED, bold=True)
f.text(494, 76, f"f1 x{cnt[1]}  f0 x{cnt[0]}", size=10.5, color=SLATE)
f.text(494, 92, f"f2 x{cnt[2]}  f3 x{cnt[3]}", size=10.5, color=SLATE)
f.text(494, 116, "with a cache: 6 calls", size=11, color=TEAL, bold=True)
f.text(494, 138, f"fib(30): {calls_of(30):,} vs 31", size=10.5, color=NAVY, bold=True)
f.text(494, 210, "f2 = fib(2) repeated", size=9.5, color=AMBER, bold=True)
```

```python
from functools import lru_cache
import sys

def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

@lru_cache(maxsize=None)
def fibc(n):
    return n if n < 2 else fibc(n - 1) + fibc(n - 2)

print(fib(10), fibc(30), fibc.cache_info().misses)
print(sys.getrecursionlimit())
```
```output
55 832040 31
1000
```
Recursion has a price (stack frames) and a trick that removes most of it (remembering answers). The plate runs both for real.

```photogrid label="4.2" cols="2" ratio="1.1" caption="Dolls inside dolls. (a) Russian nesting dolls: opening one leads to a smaller copy of the same idea until the smallest doll, the base case, stops the process. (b) Real Python runs. Plain recursive fib(30) makes 2,692,537 calls because the same sub-problems are solved again and again; with functools.lru_cache it makes just 31 calls (one per value 0 to 30). A recursion with no base case stops with RecursionError once its depth reaches the interpreter limit, which is 1,000 frames by default."
@ photo id="bca102/matryoshka" cap="Matryoshka dolls: recursion with a base case"
fit 1.1
focus 0.5 0.5
@ svg cap="Calls for fib(30), and the recursion limit"
import sys
from functools import lru_cache
calls = [0]
def fib(n):
    calls[0] += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)
v = fib(30); naive = calls[0]
calls2 = [0]
@lru_cache(maxsize=None)
def fibm(n):
    calls2[0] += 1
    return n if n < 2 else fibm(n - 1) + fibm(n - 2)
v2 = fibm(30); cached = calls2[0]
def down(k):
    return down(k + 1)
reached = [0]
def probe(k):
    reached[0] = k; return probe(k + 1)
try:
    probe(0); msg = "none"
except RecursionError as e:
    msg = type(e).__name__
lim = sys.getrecursionlimit()
assert v == v2 == 832040 and naive == 2692537 and cached == 31 and lim == 1000 and msg == "RecursionError" and 700 < reached[0] <= lim
f = Fig(300, 226)
f.text(150, 11, "function calls to compute fib(30) = 832,040", size=10, color=NAVY, bold=True)
f.text(6, 34, "plain recursion", size=9.5, color=SLATE, bold=True, anchor="start")
f.box(6, 40, 288, 18, "{:,} calls".format(naive), fill=ROSE, stroke=RED, size=10, bold=True, r=2)
f.text(6, 76, "with lru_cache", size=9.5, color=SLATE, bold=True, anchor="start")
f.box(6, 82, 2, 18, "", fill=TEAL, stroke=TEAL, r=0)
f.text(14, 92, "{} calls ({:,} times fewer)".format(cached, naive // cached), size=10, color=TEAL, bold=True, anchor="start")
f.text(150, 128, "no base case: depth grows until the limit", size=10, color=NAVY, bold=True)
f.box(6, 138, 288, 20, "", fill=BLUE, stroke=NAVY, r=2)
f.box(6, 138, 288 * reached[0] / lim, 20, "", fill=AMBER, stroke=AMBER, r=2)
f.text(150, 170, "sys.getrecursionlimit() = %d; stopped by %s" % (lim, msg), size=9.5, color=AMBER, bold=True)
f.box(6, 184, 288, 34, "each call keeps a frame on the call stack:\nmore frames = more memory, so cache or loop", fill=SAND, stroke=AMBER, size=9.5, bold=True)
```

### 4.7.1 Eight advantages of using functions and modules

1. **Reuse of code.** A function is written once and called many times, so a fee-calculation routine does not have to be copied into five places. When the rule changes, you edit one function. This lowers both the effort and the number of bugs.
2. **Easier problem solving.** A large program is broken into small, named steps such as `read_marks()`, `average()` and `print_report()`. Each step can be understood on its own. This is the same idea that the Software Engineering book calls modular design.
3. **Easier testing and debugging.** A small function can be called with known inputs and its output checked at once (Unit 8). When a result is wrong, you know which brick to open. A fault inside one long script is much harder to find.
4. **Readable programs.** A line such as `total = sum_of_digits(num)` explains itself better than four lines of arithmetic. Good names serve as documentation. A new team member can follow the program from the top-level calls.
5. **Hiding detail (abstraction).** The caller needs to know what a function does, not how. A Nagarik App style function `verify_citizenship(no)` may change its inside completely without changing the callers. The weakness is that a badly named function hides detail that a reader needs.
6. **Controlled variables (scope).** Names created inside a function are local, so two functions can both use `i` or `total` without clashing. The LEGB rule decides what each name means. This prevents many accidental changes to global values.
7. **Teamwork through modules.** Each student writes one module, such as `fees.py` or `report.py`, and the group joins them with `import`. A package groups related modules in a folder with `__init__.py`. Work can go on in parallel with fewer merge problems.
8. **A huge ready-made library.** `import math`, `datetime`, `random`, `json`, `csv` and `statistics` give hundreds of tested functions for free, and `pip` adds more from PyPI. Using a tested module is faster and safer than writing your own. Check the licence and the version of any third-party package before you depend on it.

## Formula and fact sheet

- `def f(a, b=1, *args, **kw): return …`; no `return` → `None`.
- Arguments are references; never use a mutable default (use `None`).
- LEGB lookup; `global` / `nonlocal` to rebind outer names.
- Recursion = base case + progress; memoise repeated work.
- `lambda`, `map`, `filter`, `sorted(key=…)`; decorators wrap functions; `yield` makes generators.
- `if __name__ == "__main__":` guards script-only code.

## Chapter summary

- Functions package logic, with flexible parameter passing, scopes that follow LEGB, and first-class function objects.
- Recursion, closures, decorators and generators are the building blocks of idiomatic Python.
- Modules and packages organise code across files; the standard library covers most everyday tasks.

## Practice

1. Write a function `is_palindrome(s)` and test it on three words.
2. What is printed by a function that appends to a default empty list called three times? How do you fix it?
3. Explain `*args` and `**kwargs` with an example.
4. Write a recursive function to compute the sum of the digits of a non-negative integer.
5. Use `sorted` with a `lambda` to sort names by length and then alphabetically.
6. What is a decorator? Write one that times a call (print only that it ran, to keep the output fixed).
7. Explain LEGB and what `nonlocal` does.
8. What does `if __name__ == "__main__":` do, and why is it useful?

::: note Answers and worked solutions
**1.**

```python
def is_palindrome(s):
    s = s.lower()
    return s == s[::-1]
print([is_palindrome(w) for w in ("Level", "momo", "radar")])
```
```output
[True, False, True]
```
**2.** The default list is created once, so the calls return `[1]`, `[1, 2]`, `[1, 2, 3]` (the same list). Fix: default to `None` and create a new list inside (Section 4.1).
**3.** `*args` gathers extra positional arguments into a tuple, `**kwargs` gathers extra keyword arguments into a dict:

```python
def show(*args, **kwargs):
    return len(args), sorted(kwargs)
print(show(1, 2, 3, a=1, b=2))
```
```output
(3, ['a', 'b'])
```
**4.**

```python
def digit_sum(n):
    return n if n < 10 else n % 10 + digit_sum(n // 10)
print(digit_sum(98765))
```
```output
35
```
**5.**

```python
names = ["Sita", "Ram", "Hari", "Anita", "Bo"]
print(sorted(names, key=lambda s: (len(s), s)))
```
```output
['Bo', 'Ram', 'Hari', 'Sita', 'Anita']
```
**6.** A decorator is a function that takes a function and returns a wrapped version:

```python
import functools
def timed(f):
    @functools.wraps(f)
    def w(*a, **k):
        r = f(*a, **k)
        print(f"{f.__name__} ran")
        return r
    return w

@timed
def work(n):
    return sum(range(n))

print(work(1000))
```
```output
work ran
499500
```
**7.** Python looks for a name in the Local, then Enclosing, then Global and finally Built-in scope. `nonlocal x` in an inner function makes assignments to `x` change the enclosing function's variable instead of creating a local one.
**8.** The module-level `__name__` is `"__main__"` only when the file is run directly. The guard lets a file be both a reusable module (imported without side effects) and a runnable script.
:::

## Model answers (5 and 10 marks)

**Q1. Explain the kinds of function arguments in Python with a program. (5 marks)**

A **parameter** is a name in the `def` line; an **argument** is the value passed in the call. Python offers five kinds.

1. **Positional:** matched by position, `area(3, 4)`.
2. **Keyword:** matched by name, `area(h=4, w=3)`, so the order does not matter.
3. **Default:** `def area(w, h=1)` uses 1 when `h` is omitted. A default is evaluated once, when the function is defined, so never use a mutable default such as `[]`; use `None` and create the list inside.
4. **Variable positional `*args`:** collects extra positional arguments into a **tuple**.
5. **Variable keyword `**kwargs`:** collects extra keyword arguments into a **dictionary**.

The order in a definition is: normal parameters, defaults, `*args`, keyword-only, `**kwargs`. Python passes **object references**: a mutable argument such as a list can be changed inside the function, but rebinding the parameter name does not affect the caller.

```python
def report(name, marks=0, *extra, **info):
    print(name, marks, extra, info)

report("Sita")
report("Ram", 72, 5, 6, section="A", roll=7)
report(marks=90, name="Hari")

def add_item(item, box=None):
    box = [] if box is None else box
    box.append(item)
    return box

print(add_item(1), add_item(2))
```
```output
Sita 0 () {}
Ram 72 (5, 6) {'section': 'A', 'roll': 7}
Hari 90 () {}
[1] [2]
```
**Q2. Explain the scope of variables and the LEGB rule. How do `global` and `nonlocal` work? (5 marks)**

The **scope** of a name is the part of the program where it can be used. Python searches in the order **Local, Enclosing, Global, Built-in** (Plate 4.1b) and stops at the first match.

- **Local:** names assigned inside a function exist only while it runs.
- **Enclosing:** names of an outer function seen by an inner function (a closure).
- **Global:** names at the top level of the module.
- **Built-in:** `len`, `print`, `range` and so on.

Reading a global name inside a function is allowed. **Assigning** to a name inside a function creates a new local one, unless the name is declared. `global x` makes the assignment change the module-level `x`. `nonlocal n` makes it change the variable of the nearest enclosing function. Without the declaration, assigning to a variable that is also read earlier in the function raises `UnboundLocalError`.

```python
x = "global"

def outer():
    y = "outer"
    def inner():
        nonlocal y
        y = "changed by inner"
        z = "inner"
        return z, y, x, len(x)
    result = inner()
    return result, y

def bump():
    global x
    x = "global changed"

print(outer())
bump()
print(x)
```
```output
(('inner', 'changed by inner', 'global', 6), 'changed by inner')
global changed
```
**Advice:** prefer parameters and return values to global variables, because they make a function easy to test.

**Q3. What is recursion? Explain it with the factorial and Fibonacci programs, the call stack, and compare it with iteration. (10 marks)**

**Introduction.** **Recursion** is a technique in which a function calls itself to solve a smaller copy of the same problem. Every recursive function needs a **base case**, which returns without calling again, and a **recursive case**, which moves towards the base case. Without a base case the calls never stop and Python raises `RecursionError` at its limit (1000 frames by default).

**Factorial.** n! = n x (n-1)!, with 0! = 1! = 1. The call `factorial(4)` pushes four frames; the base case returns 1 and the frames pop, giving 2, 6 and 24 (Fig. 4.1).

**Fibonacci.** fib(n) = fib(n-1) + fib(n-2) with fib(0) = 0 and fib(1) = 1. The plain version calls itself twice, so the same sub-problems are repeated: fib(5) makes 15 calls, and fib(30) makes more than 2.6 million (Fig. 4.2). **Memoisation** with `functools.lru_cache` stores each result and reduces the work to 31 calls for fib(30).

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

def fib_loop(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(factorial(4), factorial(10))
print([fib(i) for i in range(10)])
print(fib(20) == fib_loop(20), fib_loop(90))
```
```output
24 3628800
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
True 2880067194370816120
```
**The call stack.** Each call stores its parameters, local names and return address in a stack frame. Deep recursion uses a lot of memory, which is the reason for the limit.

**Comparison.**

| Point | Recursion | Iteration |
|---|---|---|
| Repetition by | function calls itself | loop statement |
| Termination | base case | loop condition |
| Memory | one stack frame per call | constant |
| Speed | slower (call overhead) | faster |
| Code | short for trees, divide and conquer | simple for counting |
| Risk | RecursionError, repeated work | infinite loop |

**Where recursion is natural:** tree and folder traversal, the Tower of Hanoi, quick sort and merge sort, and parsing expressions.

**Conclusion.** Use recursion when the problem is itself defined in terms of smaller copies of itself and the depth is small; otherwise use a loop, or add a cache when sub-problems repeat.
