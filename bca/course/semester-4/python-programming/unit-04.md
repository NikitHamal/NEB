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
