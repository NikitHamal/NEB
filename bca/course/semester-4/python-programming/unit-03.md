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

## 3.7 Seeing the ideas: text, code points and four containers

Everything in this unit is a way of holding many values: a string holds characters, a list holds items in order, a tuple holds a fixed record, a set holds unique items and a dictionary holds key-value pairs. The plate begins with a real stone that taught us how to decode one script into another, which is exactly what a character encoding does. The figures then show how a string is cut by index, how the four containers differ, and how a dictionary counts words.

```svgfig label="3.1" caption="Indexing and slicing the string 'KATHMANDU'. Each character has a positive index counted from 0 at the left and a negative index counted from -1 at the right. A slice s[a:b:c] takes the characters from index a up to, but not including, b, stepping by c. The three slices shown are computed by the cell, so the pictures cannot disagree with Python."
s = "KATHMANDU"
f = Fig(580, 216)
for i, ch in enumerate(s):
    x = 40 + i * 56
    f.box(x, 62, 50, 40, ch, fill=BLUE, stroke=NAVY, size=16, bold=True)
    f.text(x + 25, 52, str(i), size=11, color=TEAL, bold=True)
    f.text(x + 25, 118, str(i - len(s)), size=11, color=RED, bold=True)
f.text(12, 52, "index", size=9.5, color=TEAL, bold=True, anchor="start")
f.text(12, 118, "negative", size=9.5, color=RED, bold=True, anchor="start")
def span(a, b, y, color, label):
    f.line(40 + a * 56, y, 40 + b * 56 - 6, y, color=color, sw=4)
    f.text(40 + a * 56, y - 7, label, size=10.5, color=color, bold=True, anchor="start")
span(0, 4, 148, TEAL, f"s[0:4] = '{s[0:4]}'")
span(4, 9, 176, AMBER, f"s[4:] = '{s[4:]}'")
span(0, 9, 204, RED, f"s[::-2] = '{s[::-2]}'   (step -2, from the right)")
f.text(290, 14, f"len(s) = {len(s)}   s[-1] = '{s[-1]}'   s[2:6] = '{s[2:6]}'", size=11, color=NAVY, bold=True)
```

```photogrid label="3.1" cols="2" ratio="1.0" caption="Text is a code. (a) The Rosetta Stone carries one decree in three scripts, and it let scholars map Egyptian signs to known Greek letters. A character encoding is the same kind of table: Unicode gives every character a number, called a code point. (b) The Nepali word for Nepal has 5 code points but needs 15 bytes in UTF-8, so len() counts characters, not bytes. The numbers are computed by the program that draws this panel."
@ photo id="bca254/rosetta" cap="The Rosetta Stone, British Museum"
fit 1.0
focus 0.5 0.55
call 0.5 0.5 0.04 0.9 "three scripts"
@ svg cap="One word, five code points, fifteen bytes"
w = "\u0928\u0947\u092a\u093e\u0932"
f = Fig(300, 300)
f.text(150, 40, w, size=30, color=NAVY, bold=True)
for i, ch in enumerate(w):
    x = 14 + i * 56
    f.box(x, 64, 52, 38, "", fill=MINT, stroke=TEAL)
    f.text(x + 26, 78, ch, size=15, color=NAVY, bold=True)
    f.text(x + 26, 94, f"U+{ord(ch):04X}", size=9, color=TEAL, bold=True)
    bs = ch.encode("utf-8")
    f.box(x, 120, 52, 70, "", fill=SAND, stroke=AMBER)
    for j, b in enumerate(bs):
        f.text(x + 26, 136 + j * 18, f"{b:02X}", size=12, color=AMBER, bold=True)
f.text(150, 112, "UTF-8 bytes (3 per character)", size=10.5, color=SLATE)
f.text(150, 222, f"len(word) = {len(w)}", size=14, color=TEAL, bold=True)
f.text(150, 246, f"len(word.encode()) = {len(w.encode())}", size=14, color=AMBER, bold=True)
f.text(150, 276, "Devanagari block: U+0900 to U+097F", size=10.5, color=SLATE)
```

```svgfig label="3.2" caption="The four built-in containers side by side. Choose by asking three questions: must the order be kept, must the contents change, and must a value be found quickly by a key or by membership. Lists and tuples are indexed by position; sets and dictionaries use a hash table, which is why x in a_set takes about the same time for 10 items or 10 million."
f = Fig(580, 232)
cols = ["", "list", "tuple", "set", "dict"]
rows = [("syntax", ["[1, 2]", "(1, 2)", "{1, 2}", "{'a': 1}"]),
        ("ordered", ["yes", "yes", "no", "yes (insertion)"]),
        ("changeable", ["yes", "no", "yes", "yes"]),
        ("duplicates", ["allowed", "allowed", "removed", "keys unique"]),
        ("lookup by", ["position", "position", "membership", "key"]),
        ("use for", ["a sequence", "a fixed record", "unique items", "a table of facts"])]
cw = [96, 110, 110, 110, 138]
x0 = 4
xs = [x0]
for w_ in cw: xs.append(xs[-1] + w_)
fills = [BLUE, MINT, SAND, ROSE]
for j in range(1, 5):
    f.box(xs[j], 6, cw[j] - 4, 30, cols[j], fill=fills[j - 1], stroke=NAVY, size=12, bold=True)
for i, (r, vals) in enumerate(rows):
    y = 42 + i * 30
    f.box(xs[0], y, cw[0] - 4, 26, r, fill=SOFT, stroke=SLATE, size=10, bold=True)
    for j, v in enumerate(vals):
        bad = v in ("no", "removed")
        f.box(xs[j + 1], y, cw[j + 1] - 4, 26, v, fill=ROSE if bad else SOFT, stroke=RED if bad else SLATE, size=10)
```

```svgfig label="3.3" caption="A dictionary as a counter. The program below splits a sentence into words and uses word -> count pairs; the bars are drawn from the real result of the same loop. A dictionary is the natural tool whenever you ask 'how many of each' or 'what is the value for this key'."
text = "the cat sat on the mat the dog sat on the log"
cnt = {}
for w_ in text.split():
    cnt[w_] = cnt.get(w_, 0) + 1
items = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
f = Fig(580, 40 + 24 * len(items))
f.text(10, 14, f"words = {len(text.split())},  distinct keys = {len(cnt)}", size=11, color=NAVY, bold=True, anchor="start")
for i, (k, v) in enumerate(items):
    y = 30 + i * 24
    f.text(70, y + 12, f"'{k}'", size=11, color=SLATE, bold=True, anchor="end")
    f.box(80, y + 2, v * 70, 18, str(v), fill=MINT if v > 1 else SAND, stroke=TEAL if v > 1 else AMBER, size=10.5, bold=True, r=3)
```

```python
text = "the cat sat on the mat the dog sat on the log"
cnt = {}
for w in text.split():
    cnt[w] = cnt.get(w, 0) + 1
print(cnt)
print(max(cnt, key=cnt.get), cnt["the"])
```
```output
{'the': 4, 'cat': 1, 'sat': 2, 'on': 2, 'mat': 1, 'dog': 1, 'log': 1}
the 4
```
Choosing between a list, tuple, set and dictionary is partly a question of speed and memory, and partly of safety. The plates below measure the first two with real Python 3.12 and show the third with the real error messages.

```photogrid label="3.2" cols="2" ratio="1.1" caption="Dictionary look-up. (a) A printed dictionary: nobody reads from page one, you jump to the right place. A Python dict does the same with a hash table. (b) Finding the last of 1,000 keys: a list must compare with all 1,000 items (the in operator), a dict or set goes straight to the slot with about 1 probe. The container memory is measured with sys.getsizeof on 1,000 integers under the Python version that built this book: the bar lengths in the figure are those measured values."
@ photo id="bca102/oed" cap="A large printed dictionary"
fit 1.1
focus 0.5 0.5
@ svg cap="Comparisons and memory for 1,000 items"
import sys
n = 1000
data = list(range(n)); cmp_list = 0
for x in data:
    cmp_list += 1
    if x == n - 1: break
d = {k: k for k in data}; s = set(data); t = tuple(data)
assert cmp_list == 1000 and (n - 1) in d and (n - 1) in s
sizes = [("tuple", sys.getsizeof(t)), ("list", sys.getsizeof(data)), ("set", sys.getsizeof(s)), ("dict", sys.getsizeof(d))]
assert sizes[0][1] < sizes[1][1] < sizes[3][1] and sizes[2][1] > sizes[1][1]
f = Fig(300, 236)
f.text(150, 11, "search for the last of 1,000 keys", size=10, color=NAVY, bold=True)
f.text(6, 34, "list: x in data", size=9.5, color=SLATE, bold=True, anchor="start")
f.box(6, 40, 270, 14, "", fill=RED, stroke=RED, r=2); f.text(150, 47, "1,000 comparisons", size=9.5, color="#ffffff", bold=True, vmid=True)
f.text(6, 70, "dict / set: key in d", size=9.5, color=SLATE, bold=True, anchor="start")
f.box(6, 76, 2, 14, "", fill=TEAL, stroke=TEAL, r=0); f.text(14, 83, "about 1 probe", size=9.5, color=TEAL, bold=True, anchor="start")
f.text(150, 112, "memory of the container (bytes, sys.getsizeof)", size=10, color=NAVY, bold=True)
mx = max(v for _, v in sizes)
for i, (k, v) in enumerate(sizes):
    y = 122 + i * 26
    w = 170 * v / mx
    f.text(6, y + 8, k, size=9.5, color=SLATE, bold=True, anchor="start")
    f.box(50, y, w, 16, "", fill=(AMBER if k in ("set", "dict") else TEAL), stroke=(AMBER if k in ("set", "dict") else TEAL), r=2)
    f.text(50 + w + 5, y + 9, "{:,}".format(v), size=9.5, color=SLATE, bold=True, anchor="start")
f.text(150, 230, "speed is bought with memory: set and dict are larger", size=9.5, color=AMBER, bold=True)
```

```photogrid label="3.3" cols="2" ratio="1.0" caption="Locked containers and shared rows. (a) A combination padlock: once a tuple is made it stays locked, which is why a tuple can be a dictionary key and a list cannot. (b) Real Python 3.12 results. A list used as a key raises TypeError (unhashable type); the tuple works. The row-copy trap: [[0] * 3] * 3 makes three names for ONE row, so changing grid[0][0] changes all three rows, while the comprehension [[0] * 3 for _ in range(3)] makes three separate rows."
@ photo id="bca151/lock" cap="Combination padlock"
fit 1.0
focus 0.5 0.5
@ svg cap="Two traps, run for real"
try:
    {[1, 2]: "x"}
    err = "no error"
except TypeError as e:
    err = str(e)
ok = {(27, 85): "Kathmandu"}[(27, 85)]
g1 = [[0] * 3] * 3; g1[0][0] = 1
g2 = [[0] * 3 for _ in range(3)]; g2[0][0] = 1
assert err == "unhashable type: 'list'" and ok == "Kathmandu"
assert g1 == [[1, 0, 0]] * 3 and g2 == [[1, 0, 0], [0, 0, 0], [0, 0, 0]] and g1[0] is g1[1] and g2[0] is not g2[1]
f = Fig(300, 262)
f.box(6, 6, 288, 58, "{[1, 2]: 'x'}\nTypeError: " + err + "\n{(27, 85): 'Kathmandu'}[(27, 85)] -> " + ok, fill=SOFT, stroke=SLATE, size=9.5, bold=True, color=NAVY)
f.text(150, 84, "g[0][0] = 1 after building a 3 x 3 grid", size=10, color=NAVY, bold=True)
for c, (title, g, fl, st) in enumerate((("[[0]*3]*3\nshared row", g1, ROSE, RED), ("comprehension\nseparate rows", g2, MINT, TEAL))):
    x0 = 10 + c * 146
    f.text(x0 + 66, 106, title, size=9.5, color=st, bold=True)
    for r in range(3):
        for k in range(3):
            v = g[r][k]
            f.box(x0 + k * 44, 128 + r * 28, 42, 26, str(v), fill=(SAND if v == 1 else fl), stroke=st, size=11, bold=True, r=2)
f.box(6, 222, 288, 32, "same id for all rows (left): 1 object, 3 names\nthree different ids (right): 3 objects", fill=SAND, stroke=AMBER, size=9.5, bold=True)
```

### 3.7.1 Eight practical uses of strings, lists and dictionaries

1. **Cleaning names and codes.** Methods such as `strip()`, `title()` and `replace()` tidy text typed by users. A college clerk can turn `"  ram BAHADUR thapa "` into `"Ram Bahadur Thapa"` in one line. Clean text gives correct matches when records are joined later.
2. **Splitting and joining records.** `line.split(",")` turns a CSV row of exam marks into a list, and `",".join(list)` writes it back. Most data files exported from a school management system are of this type. These two methods are the basis of simple data pipelines.
3. **Keeping ordered collections.** A list holds a queue of tickets, the marks of a class or the pages of a report in order. It can grow, shrink and be sorted. The cost is that finding one item in a very long list means scanning it.
4. **Building new lists by comprehension.** `[m for m in marks if m >= 40]` keeps the passing marks in a single readable line. It replaces a four-line loop and is usually faster. A long or nested comprehension becomes hard to read, so split it then.
5. **Protecting fixed data with tuples.** A tuple such as `(27.7172, 85.3240)` for the latitude and longitude of Kathmandu cannot be changed by mistake. Tuples can be dictionary keys, while lists cannot. Use them for records that should stay constant.
6. **Removing duplicates with sets.** `set(roll_numbers)` drops repeated entries, and `a & b` shows students present in both of two lists. A set answers "is this item present" very fast. It has no order, so sort it when the order matters.
7. **Lookup tables with dictionaries.** A dictionary maps a district name to its code, or a ledger number to a balance, and finds a key without scanning. It is the Python form of a small database table. Keys must be hashable, so a list cannot be a key.
8. **Counting and grouping.** `collections.Counter` or `dict.get(k, 0) + 1` counts word frequencies, votes per candidate or sales per shop, as Fig. 3.3 shows. `defaultdict(list)` groups students by section. Nested dictionaries can store a whole record, but very deep nesting is better replaced by a class (Unit 6).

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

## Model answers (5 and 10 marks)

**Q1. Explain string slicing and any six string methods of Python with a program. (5 marks)**

A **string** is an immutable sequence of Unicode characters. Each character has an index from 0 (left) and from -1 (right), so `s[0]` is the first and `s[-1]` the last character (Fig. 3.1). A **slice** `s[a:b:c]` returns characters from index `a` up to but not including `b` with step `c`; omitted parts default to the start, the end and 1, and `s[::-1]` reverses the string. Because strings are immutable, every method returns a **new** string and leaves the original unchanged; `s[0] = "k"` raises a `TypeError`.

**Six common methods.**

- `upper()`, `lower()`, `title()` change case.
- `strip()` removes spaces from both ends.
- `replace(old, new)` substitutes text.
- `split(sep)` returns a list of parts and `sep.join(list)` joins them.
- `find(sub)` gives the first index or -1; `count(sub)` counts occurrences.
- `startswith()`, `endswith()` and `isdigit()` return `True` or `False`.

```python
s = "  Kathmandu Valley  "
t = s.strip()
print(t.upper(), "|", t.replace("Valley", "City"))
print(t.split(), t.find("Val"), t.count("a"))
print(t[0:4], t[-6:], t[::-1])
print(t.startswith("Kath"), "7".isdigit(), "-".join(["2082", "01", "15"]))
```
```output
KATHMANDU VALLEY | Kathmandu City
['Kathmandu', 'Valley'] 10 3
Kath Valley yellaV udnamhtaK
True True 2082-01-15
```
**Formatted output** uses f-strings such as `f"{x:.2f}"`. Strings can be compared with `==` and `<`, which follow Unicode order.

**Q2. Compare list, tuple, set and dictionary with suitable examples. (5 marks)**

Python has four built-in containers (Fig. 3.2). All can hold mixed types and all work with `len()`, `in` and `for`.

| Point | list | tuple | set | dict |
|---|---|---|---|---|
| Example | `[3, 1, 3]` | `(3, 1, 3)` | `{3, 1}` | `{"a": 3}` |
| Ordered | yes | yes | no | yes (insertion order) |
| Mutable | yes | no | yes | yes |
| Duplicates | allowed | allowed | not kept | keys unique |
| Access | `x[i]` | `x[i]` | `in` only | `x[key]` |

**When to use which.** A list is the default sequence (marks of a class). A tuple is a fixed record or a dictionary key (a point). A set removes duplicates and does union (`|`), intersection (`&`) and difference (`-`). A dictionary stores facts by key (district code).

```python
data = [3, 1, 3, 2, 1]
print(data, tuple(data), set(data), sorted(set(data)))
print({k: data.count(k) for k in set(data)} == {1: 2, 2: 1, 3: 2})
print({1, 2, 3} & {2, 3, 4}, {1, 2, 3} - {2})
```
```output
[3, 1, 3, 2, 1] (3, 1, 3, 2, 1) {1, 2, 3} [1, 2, 3]
True
{2, 3} {1, 3}
```
**Memory aid:** lists and tuples find by position, sets and dictionaries find by hash, so membership in a set is much faster than in a list.

**Q3. What is a dictionary? Explain its creation, access, modification and the main methods, and write a program that counts word frequency. Compare it with a list. (10 marks)**

**Introduction.** A **dictionary** (`dict`) is a mutable collection of **key-value pairs**. It is implemented with a hash table, so a value is found from its key in about constant time. Keys must be unique and hashable (strings, numbers, tuples of these); values can be any object. Since Python 3.7 a dictionary keeps the insertion order.

**Creation.** `d = {"ram": 72, "sita": 88}`, `d = dict(ram=72)`, `dict(zip(keys, values))`, or a comprehension `{n: n * n for n in range(4)}`.

**Access.** `d["ram"]` returns the value but raises `KeyError` for a missing key; `d.get("hari", 0)` returns a default instead; `"ram" in d` tests for a key.

**Modification.** `d["hari"] = 65` adds or replaces; `del d["ram"]` and `d.pop("sita")` remove; `d.update(other)` merges; `d.setdefault(k, v)` inserts only if absent.

**Main methods.**

1. `keys()`, `values()` and `items()` give live views for loops.
2. `get()` for safe access.
3. `pop()` and `popitem()` to remove.
4. `update()` to merge.
5. `setdefault()` to initialise.
6. `copy()` for a shallow copy.
7. `clear()` to empty.
8. `sorted(d.items())` to order by key.

**Program: word frequency.**

```python
text = "to be or not to be that is the question to be"
freq = {}
for word in text.split():
    freq[word] = freq.get(word, 0) + 1
for word, n in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:3]:
    print(word, n)
print(len(freq), sum(freq.values()))
```
```output
be 3
to 3
is 1
8 12
```
**Comparison with a list.**

| Point | dict | list |
|---|---|---|
| Access by | key | position |
| Search cost | about constant | grows with length |
| Order meaning | insertion | position |
| Memory | more (hash table) | less |
| Best for | lookups, counting, records | ordered sequences |

**Typical uses** are phone books, word counts, JSON data and caches (Fig. 3.3).

**Conclusion.** A dictionary trades some memory for very fast, readable access by key, which is why it is the most used structure in real Python programs.
