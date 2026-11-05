---
subject: Python Programming
grade: BCA Semester 4
unit: 3
title: Strings and Built-in Data Structures
hours: 7
area: BCA 254 · Python Programming · Unit 3
---

Most real programs are about collections of data: marks of fifty students, words in a document, a phone book. Python gives you strings, lists, tuples, sets and dictionaries as built-in types, each tuned for a different job. Choosing the right one is half the work of writing a good program.

::: key What this unit gives you
- Strings: indexing, slicing, methods, formatting, immutability.
- Lists, tuples, sets and dictionaries: creation, operations, methods, comprehensions.
- Copying (shallow versus deep), sorting, and how to choose a structure.
:::

## 3.1 Strings

A string is an **immutable sequence** of Unicode characters. Indexes start at 0; negative indexes count from the end. Slicing `s[start:stop:step]` takes a sub-sequence (stop is excluded).

```python
s = "Pokhara Valley"
print(s[0], s[-1], s[0:7], s[8:], s[::-1], s[::2])
print(len(s), s.upper(), s.lower(), s.swapcase())
print(s.find("a"), s.rfind("a"), s.count("a"), s.replace("a", "@"))
print(s.split(), "-".join(["BCA", "TU", "4th"]))
print("  padded  ".strip() + "|", "42".zfill(5), "x".center(5, "*"))
print("momo".startswith("mo"), "momo".endswith("ma"), "abc123".isalnum(), "123".isdigit())
```
```output
P y Pokhara Valley yellaV arahkoP PkaaVle
14 POKHARA VALLEY pokhara valley pOKHARA vALLEY
4 9 3 Pokh@r@ V@lley
['Pokhara', 'Valley'] BCA-TU-4th
padded| 00042 **x**
True False True True
```
Strings cannot be changed in place: `s[0] = "p"` raises `TypeError`, so methods return **new** strings.

```python
# raises
s = "momo"
s[0] = "M"
```
```output
Traceback (most recent call last):
  File "p.py", line 3, in <module>
    s[0] = "M"
    ~^^^
TypeError: 'str' object does not support item assignment
```
**Useful methods:** `strip/lstrip/rstrip`, `split/rsplit/splitlines`, `join`, `find/index/count`, `startswith/endswith`, `isalpha/isdigit/isalnum/isspace/isupper/islower`, `title/capitalize`, `format`, `encode`. Triple-quoted strings span lines; raw strings `r"C:\new"` keep backslashes. Strings compare lexicographically by Unicode code point.

```python
text = "the quick brown fox jumps over the lazy dog the end"
words = text.split()
print(len(words), "words;", len(set(words)), "distinct")
print(text.title()[:20], "|", "".join(c for c in text if c in "aeiou")[:10])
nepali = "नमस्ते"
print(nepali, len(nepali), nepali.encode("utf-8")[:6])
```
```output
11 words; 9 distinct
The Quick Brown Fox  | euioouoeea
नमस्ते 6 b'\xe0\xa4\xa8\xe0\xa4\xae'
```
## 3.2 Lists

A **list** is a mutable, ordered sequence of any objects. Create with `[...]` or `list(iterable)`.

```python
marks = [72, 85, 60, 91]
marks.append(78)
marks.insert(1, 99)
marks.extend([55, 66])
print(marks, len(marks))
print(marks.pop(), marks.pop(0), marks.remove(60), marks)
marks.sort()
print(marks, marks[1:4], marks[-2:], max(marks), sum(marks) / len(marks))
marks.reverse()
print(marks, marks.index(85), marks.count(78), 85 in marks)
```
```output
[72, 99, 85, 60, 91, 78, 55, 66] 8
66 72 None [99, 85, 91, 78, 55]
[55, 78, 85, 91, 99] [78, 85, 91] [91, 99] 99 81.6
[99, 91, 85, 78, 55] 2 1 True
```
| Method | Effect |
|---|---|
| `append(x)`, `extend(it)`, `insert(i, x)` | add one item, many items, at a position |
| `pop([i])`, `remove(x)`, `clear()`, `del a[i]` | remove |
| `sort(key=…, reverse=…)`, `reverse()` | in place; return `None` |
| `index(x)`, `count(x)` | search |
| `copy()`, `a + b`, `a * n` | copy, concatenate, repeat |

`sorted(a)` returns a new sorted list and leaves `a` alone. The `key` function customises sorting.

```python
students = [("Sita", 88), ("Ram", 72), ("Hari", 88), ("Gita", 95)]
print(sorted(students, key=lambda p: p[1], reverse=True))
print(sorted(students, key=lambda p: (-p[1], p[0])))
print(sorted(["banana", "Apple", "cherry"], key=str.lower))
```
```output
[('Gita', 95), ('Sita', 88), ('Hari', 88), ('Ram', 72)]
[('Gita', 95), ('Hari', 88), ('Sita', 88), ('Ram', 72)]
['Apple', 'banana', 'cherry']
```
### List comprehensions

`[expr for item in iterable if condition]` builds a list in one expression.

```python
squares = [n * n for n in range(1, 8)]
evens = [n for n in range(20) if n % 2 == 0]
pairs = [(x, y) for x in range(1, 4) for y in range(1, 4) if x < y]
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(squares, evens, pairs, matrix, sep="\n")
```
```output
[1, 4, 9, 16, 25, 36, 49]
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
[(1, 2), (1, 3), (2, 3)]
[[1, 2, 3], [2, 4, 6], [3, 6, 9]]
```
### Copying: references, shallow copy, deep copy

Assigning a list to another name does *not* copy it.

```python
import copy
a = [[1, 2], [3, 4]]
alias = a
shallow = a.copy()
deep = copy.deepcopy(a)
a[0][0] = 99
print(alias, shallow, deep)
a.append([5, 6])
print(len(alias), len(shallow), len(deep))
```
```output
[[99, 2], [3, 4]] [[99, 2], [3, 4]] [[1, 2], [3, 4]]
3 2 2
```
`alias` is the same object. `shallow` has its own outer list but shares the inner lists (so the change to `a[0][0]` shows in it, while the appended row does not). `deep` shares nothing.

## 3.3 Tuples

A **tuple** is an immutable ordered sequence: `(1, 2, 3)`, or just `1, 2, 3`; a one-element tuple needs a comma: `(5,)`. Use tuples for fixed records (coordinates, a date), as dictionary keys, and for returning several values from a function.

```python
point = (3, 4)
x, y = point
single = (5,)
r, *rest = (10, 20, 30, 40)
print(x, y, type(single), r, rest, point + (5,), point * 2)
print(divmod(17, 5), tuple("abc"), (1, 2) < (1, 3), len(()))
```
```output
3 4 <class 'tuple'> 10 [20, 30, 40] (3, 4, 5) (3, 4, 3, 4)
(3, 2) ('a', 'b', 'c') True 0
```
Tuples are **hashable** (if their items are), faster and smaller than lists, and protect data from accidental change.

## 3.4 Sets

A **set** is an unordered collection of **unique, hashable** elements. Membership tests are very fast (average O(1)).

```python
a = {1, 2, 3, 4}
b = {3, 4, 5}
print(a | b, a & b, a - b, a ^ b)
print(a <= {1, 2, 3, 4, 5}, 3 in a, set("banana"), {1, 2, 2, 3})
a.add(10); a.discard(1)
print(sorted(a), len(set([5, 1, 5, 2, 1])))
```
```output
{1, 2, 3, 4, 5} {3, 4} {1, 2} {1, 2, 5}
True True {'a', 'n', 'b'} {1, 2, 3}
[2, 3, 4, 10] 3
```
`{}` is an empty **dict**; an empty set is `set()`. Operations: union `|`, intersection `&`, difference `-`, symmetric difference `^`, subset `<=`. Use sets to remove duplicates and to compare groups: who is enrolled in both courses?

## 3.5 Dictionaries

A **dictionary** maps unique, hashable **keys** to values. Since Python 3.7 it keeps insertion order.

```python
student = {"name": "Sita", "roll": 14, "marks": [88, 92]}
student["college"] = "Patan"
print(student["name"], student.get("phone", "n/a"), len(student))
print(list(student.keys()), list(student.values())[:2])
for k, v in student.items():
    print(f"{k:8} -> {v}")
del student["roll"]
print(student.pop("college"), student, "name" in student)
```
```output
Sita n/a 4
['name', 'roll', 'marks', 'college'] ['Sita', 14]
name     -> Sita
roll     -> 14
marks    -> [88, 92]
college  -> Patan
Patan {'name': 'Sita', 'marks': [88, 92]} True
```
Accessing a missing key with `d[k]` raises `KeyError`; `d.get(k, default)` is safe. `setdefault`, `update`, `pop`, `popitem`, `items`, `keys`, `values` complete the main methods. **Dictionary comprehension**: `{k: v for …}`.

```python
text = "to be or not to be that is the question"
count = {}
for w in text.split():
    count[w] = count.get(w, 0) + 1
print(count)
print({w: len(w) for w in set(text.split()) if len(w) > 3} == {"that": 4, "question": 8})
inv = {v: k for k, v in {"a": 1, "b": 2}.items()}
print(inv, dict(zip("xyz", range(3))))
top = sorted(count.items(), key=lambda kv: (-kv[1], kv[0]))[:3]
print(top)
```
```output
{'to': 2, 'be': 2, 'or': 1, 'not': 1, 'that': 1, 'is': 1, 'the': 1, 'question': 1}
True
{1: 'a', 2: 'b'} {'x': 0, 'y': 1, 'z': 2}
[('be', 2), ('to', 2), ('is', 1)]
```
(The standard library's `collections.Counter` does word counting in one line; see Unit 4.)

## 3.6 Choosing a data structure

| Need | Use |
|---|---|
| ordered, changeable sequence | `list` |
| fixed record or dictionary key | `tuple` |
| uniqueness, fast membership, set algebra | `set` |
| look up by key | `dict` |
| text | `str` |
| queue with fast ends | `collections.deque` |

| Operation | list | set | dict |
|---|---|---|---|
| `x in c` | O(n) | O(1) average | O(1) average (keys) |
| append / add | O(1) amortised | O(1) | O(1) |
| index `c[i]` | O(1) | none | O(1) by key |

## Formula and fact sheet

- Slice `s[a:b:c]`; negative index from the end; strings and tuples immutable, lists, sets, dicts mutable.
- `sorted()` returns a new list; `list.sort()` sorts in place and returns `None`.
- `a = b` aliases; `.copy()` is shallow; `copy.deepcopy` is deep.
- Set ops `| & - ^`; `{}` is an empty dict.
- `d.get(k, default)` avoids `KeyError`.

## Chapter summary

- Strings are immutable sequences with a rich method set; slicing is the universal tool for sequences.
- Lists are the general-purpose mutable sequence; comprehensions build them concisely; copies are shallow unless you ask for deep.
- Tuples are fixed records, sets give uniqueness and fast membership, dictionaries give key-based lookup.

## Practice

1. Given `s = "Computer"`, write expressions for its first three letters, last three letters, reversed string and every second character.
2. Why does `s[0] = "c"` fail for a string, and how would you produce "computer"?
3. Remove duplicates from `[3, 1, 3, 2, 1]` while keeping the first occurrence order.
4. Sort `[("a", 3), ("b", 1), ("c", 2)]` by the second element in descending order.
5. Explain the output difference between assignment, shallow copy and deep copy for nested lists.
6. Count the frequency of each character in `"mississippi"`.
7. Find the students who took both Maths and Physics given two sets of rolls.
8. When would you use a tuple instead of a list?

::: note Answers and worked solutions
**1.**

```python
s = "Computer"
print(s[:3], s[-3:], s[::-1], s[::2])
```
```output
Com ter retupmoC Cmue
```
**2.** Strings are immutable, so item assignment raises `TypeError`. Build a new string:

```python
s = "Computer"
print(s.lower(), "c" + s[1:])
```
```output
computer computer
```
**3.**

```python
data = [3, 1, 3, 2, 1]
print(list(dict.fromkeys(data)))
```
```output
[3, 1, 2]
```
(`dict` keeps insertion order and keys are unique.)
**4.**

```python
print(sorted([("a", 3), ("b", 1), ("c", 2)], key=lambda t: t[1], reverse=True))
```
```output
[('a', 3), ('c', 2), ('b', 1)]
```
**5.** See Section 3.2: the alias shows every change; a shallow copy shares the inner lists but not the outer one; a deep copy shares nothing.
**6.**

```python
freq = {}
for ch in "mississippi":
    freq[ch] = freq.get(ch, 0) + 1
print(freq)
```
```output
{'m': 1, 'i': 4, 's': 4, 'p': 2}
```
**7.**

```python
maths = {1, 2, 5, 7, 9}
physics = {2, 3, 7, 8}
print(sorted(maths & physics))
```
```output
[2, 7]
```
**8.** For fixed records that must not change, as dictionary keys or set members, for returning multiple values, and when you want the small speed and memory advantage and the guarantee of immutability.
:::
