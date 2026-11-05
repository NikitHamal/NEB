---
subject: Python Programming
grade: BCA Semester 4
unit: 2
title: Control Flow
hours: 5
area: BCA 254 · Python Programming · Unit 2
---

A program that runs line by line from top to bottom can only do one thing. **Control flow** lets it choose (`if`), repeat (`while`, `for`), and leave a loop early (`break`). With these three ideas plus variables you can express any algorithm.

::: key What this unit gives you
- Conditional statements: `if`, `elif`, `else`, conditional expressions, `match`.
- Loops: `while`, `for`, `range`, `break`, `continue`, loop `else`, nested loops.
- Classic algorithms: primes, GCD, factorial, Fibonacci, digit sums, number patterns.
:::

## 2.1 Conditional statements

```python
marks = 67
if marks >= 80:
    grade = "Distinction"
elif marks >= 60:
    grade = "First division"
elif marks >= 45:
    grade = "Second division"
else:
    grade = "Fail"
print(marks, "->", grade)
```
```output
67 -> First division
```
Only the first true branch runs. The colon and the indentation are mandatory. A **conditional expression** gives a value in one line: `status = "pass" if marks >= 40 else "fail"`. Conditions can be chained (`0 <= marks <= 100`) and combined with `and`, `or`, `not`.

```python
def classify(n):
    if n < 0:
        return "negative"
    if n == 0:
        return "zero"
    return "even" if n % 2 == 0 else "odd"

for n in (-4, 0, 7, 10):
    print(n, classify(n), "pass" if n >= 5 else "fail")
```
```output
-4 negative fail
0 zero fail
7 odd pass
10 even pass
```
### Structural pattern matching (Python 3.10+)

`match` compares a value against patterns; `_` is the wildcard.

```python
def describe(command):
    match command.split():
        case ["go", direction]:
            return f"moving {direction}"
        case ["take", item, *rest]:
            return f"taking {item} (+{len(rest)} more words)"
        case ["quit"]:
            return "bye"
        case _:
            return "unknown command"

for c in ("go north", "take lamp and key", "quit", "dance"):
    print(c, "->", describe(c))
```
```output
go north -> moving north
take lamp and key -> taking lamp (+2 more words)
quit -> bye
dance -> unknown command
```
## 2.2 The `while` loop

A `while` loop repeats as long as its condition is true. Make sure something in the body eventually makes the condition false.

```python
n, steps = 27, 0
while n != 1:
    n = n // 2 if n % 2 == 0 else 3 * n + 1
    steps += 1
print("Collatz steps for 27:", steps)

total, k = 0, 1
while total < 100:
    total += k
    k += 1
print("first k with 1+2+...+k >= 100:", k - 1, "sum", total)
```
```output
Collatz steps for 27: 111
first k with 1+2+...+k >= 100: 14 sum 105
```
## 2.3 The `for` loop and `range`

A `for` loop iterates over any **iterable** (list, string, tuple, dict, file, `range`). `range(stop)`, `range(start, stop)` and `range(start, stop, step)` produce integers up to, but **not including**, `stop`.

```python
for ch in "BCA":
    print(ch, end=" ")
print()
print(list(range(5)), list(range(2, 9, 3)), list(range(10, 0, -3)))
total = 0
for i in range(1, 11):
    total += i * i
print("sum of squares 1..10 =", total)
for i, name in enumerate(["Ram", "Sita", "Hari"], start=1):
    print(i, name)
```
```output
B C A 
[0, 1, 2, 3, 4] [2, 5, 8] [10, 7, 4, 1]
sum of squares 1..10 = 385
1 Ram
2 Sita
3 Hari
```
Prefer `for` when the number of repetitions is known or you are walking a collection; prefer `while` when you loop until some condition changes.

## 2.4 `break`, `continue`, `pass` and loop `else`

- `break` leaves the innermost loop immediately.
- `continue` skips to the next iteration.
- `pass` does nothing (a placeholder for an empty block).
- A loop's **`else`** clause runs only if the loop finished *without* `break`.

```python
def is_prime(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True

print([n for n in range(2, 40) if is_prime(n)])

for n in (91, 97):
    for d in range(2, n):
        if n % d == 0:
            print(n, "is composite: divisible by", d)
            break
    else:
        print(n, "is prime")
```
```output
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
91 is composite: divisible by 7
97 is prime
```
(91 = 7 × 13 is composite, so the loop is ended by `break` and its `else` clause is skipped; 97 completes the loop and prints "is prime".) Loop `else` is the neat way to express "search failed".

## 2.5 Nested loops and patterns

```python
for row in range(1, 5):
    print(" " * (4 - row) + "*" * (2 * row - 1))
print()
for i in range(1, 4):
    print("  ".join(f"{i * j:2d}" for j in range(1, 6)))
```
```output
   *
  ***
 *****
*******

 1   2   3   4   5
 2   4   6   8  10
 3   6   9  12  15
```
The inner loop runs completely for every iteration of the outer loop, so two nested loops of size *n* do about *n²* steps.

## 2.6 Classic programs

```python
# gcd by Euclid's algorithm, factorial, Fibonacci, digit sum, palindromes
a, b = 252, 105
while b:
    a, b = b, a % b
print("gcd(252, 105) =", a)

f = 1
for i in range(2, 11):
    f *= i
print("10! =", f)

x, y, fib = 0, 1, []
for _ in range(12):
    fib.append(x)
    x, y = y, x + y
print(fib)

n, s = 98765, 0
while n:
    s += n % 10
    n //= 10
print("digit sum:", s, "| palindrome check:", str(12321) == str(12321)[::-1])
```
```output
gcd(252, 105) = 21
10! = 3628800
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
digit sum: 35 | palindrome check: True
```
```python
# number guessing with a fixed 'secret' and a scripted list of guesses
secret = 37
for attempt, guess in enumerate([50, 25, 37], start=1):
    if guess < secret:
        print(attempt, guess, "too low")
    elif guess > secret:
        print(attempt, guess, "too high")
    else:
        print(attempt, guess, "correct!")
        break
```
```output
1 50 too high
2 25 too low
3 37 correct!
```
## 2.7 Common mistakes

- Using `=` where `==` is meant in a condition (Python reports a `SyntaxError`, which helps).
- Forgetting that `range(1, 10)` stops at 9.
- An infinite `while` loop because the loop variable is never updated.
- Modifying a list while iterating over it; iterate over a copy or build a new list.
- Comparing floats for equality.

## 2.8 Seeing the ideas: choices, loops and a very long trip

Every program is built from three moves: go straight, choose a branch, and go round again. A fork in a road is the plainest picture of a choice, and the plate pairs one with the grade ladder that a Python `if`, `elif` and `else` follows. The figures then show how long a `while` loop can run when you cannot guess the count, and how `break`, `continue` and the loop `else` change the path.

```photogrid label="2.1" cols="2" ratio="1.0" caption="One road splits into several: a choice. (a) A real fork where a signpost sends a traveller left, right or straight on, just as an if/elif/else chain sends control to exactly one branch. (b) The same idea for marks: Python tests from the top and stops at the first true condition, so the order 80, 60, 40 matters (a mark of 85 is also at least 60, but the first test already took it)."
@ photo id="bca254/fork" cap="A fork in the road"
fit 1.0
focus 0.5 0.45
call 0.52 0.58 0.04 0.9 "choose one way"
@ svg cap="Grade ladder: first true test wins"
f = Fig(300, 300)
rows = [("marks >= 80", "Distinction", MINT, TEAL), ("marks >= 60", "First division", BLUE, NAVY), ("marks >= 40", "Pass", SAND, AMBER), ("else", "Fail", ROSE, RED)]
for i, (c, r, fl, st) in enumerate(rows):
    y = 18 + i * 66
    f.box(12, y, 130, 44, c, fill=fl, stroke=st, size=13, bold=True)
    f.arrow([(144, y + 22), (176, y + 22)], color=st, sw=1.8)
    f.box(178, y, 112, 44, r, fill=fl, stroke=st, size=13, bold=True)
    if i < 3:
        f.arrow([(77, y + 46), (77, y + 64)], color=SLATE, sw=1.4)
        f.text(106, y + 56, "False", size=11, color=SLATE)
```

```svgfig label="2.1" caption="A while loop whose length you cannot guess: the Collatz rule. Start from n = 27; if n is even halve it, otherwise replace it by 3n + 1, and stop at 1. The number of steps and the peak are computed by the loop in the program below, not by hand. A for loop needs a known sequence; a while loop needs only a condition, so it suits problems like this one, validating input until it is correct, or reading until the end of a file."
seq = [27]
while seq[-1] != 1:
    n = seq[-1]
    seq.append(n // 2 if n % 2 == 0 else 3 * n + 1)
steps, peak = len(seq) - 1, max(seq)
pk = seq.index(peak)
f = Fig(580, 232)
L, T, W, H = 54, 22, 506, 170
def X(i): return L + i / steps * W
def Y(v): return T + H - v / 9500 * H
f.line(L, T + H, L + W, T + H, color=SLATE, sw=1.2)
f.line(L, T, L, T + H, color=SLATE, sw=1.2)
for v in (0, 3000, 6000, 9000):
    f.line(L - 4, Y(v), L, Y(v), color=SLATE)
    f.text(L - 8, Y(v) + 3, f"{v:,}", size=9, color=SLATE, anchor="end")
for i in range(0, steps + 1, 20):
    f.text(X(i), T + H + 14, str(i), size=9, color=SLATE)
for i in range(steps):
    f.line(X(i), Y(seq[i]), X(i + 1), Y(seq[i + 1]), color=NAVY, sw=1.3)
f.circle(X(pk), Y(peak), 4, fill=RED, stroke=RED)
f.text(X(pk) - 8, Y(peak) + 3, f"peak {peak:,} at step {pk}", size=10.5, color=RED, bold=True, anchor="end")
f.text(X(steps), Y(1) - 8, f"reaches 1 at step {steps}", size=10.5, color=TEAL, bold=True, anchor="end")
f.text(L + W / 2, 224, "step number (one pass through the while loop)", size=10, color=SLATE)
f.text(14, 14, "value of n", size=9.5, color=SLATE, anchor="start")
```

```python
n, steps, peak = 27, 0, 27
while n != 1:
    n = n // 2 if n % 2 == 0 else 3 * n + 1
    steps += 1
    peak = max(peak, n)
print(steps, peak)
```
```output
111 9232
```
```svgfig label="2.2" caption="How break, continue and else steer a loop. After each test of the condition the body runs. continue jumps straight back to the test, skipping the rest of the body. break jumps out of the loop and skips the else clause. If the condition turns false by itself, the loop ends normally and the else clause runs once. That last rule is why for ... else is the clean way to say 'the search found nothing'."
f = Fig(580, 214)
f.box(10, 78, 110, 46, "test the\ncondition", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(170, 78, 120, 46, "run the body", fill=MINT, stroke=TEAL, size=11, bold=True)
f.arrow([(122, 101), (168, 101)], color=TEAL, sw=1.7, label="true", lpos=(145, 92))
f.box(340, 20, 130, 40, "continue\n(skip the rest)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.arrow([(250, 76), (340, 44)], color=AMBER, sw=1.5, dash=True)
f.arrow([(405, 20), (405, 8), (65, 8), (65, 76)], color=AMBER, sw=1.5, dash=True)
f.box(340, 150, 130, 40, "break\n(leave at once)", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(250, 126), (340, 168)], color=RED, sw=1.5, dash=True)
f.arrow([(230, 126), (230, 202), (65, 202), (65, 126)], color=SLATE, sw=1.5)
f.text(150, 197, "end of body: test again", size=9.5, color=SLATE)
f.box(490, 78, 84, 46, "after the\nloop", fill=SOFT, stroke=SLATE, size=10.5, bold=True)
f.arrow([(472, 170), (532, 170), (532, 126)], color=RED, sw=1.6)
f.box(10, 150, 110, 40, "else clause\n(no break)", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(65, 126), (65, 148)], color=TEAL, sw=1.6, label="false", lpos=(88, 138))
```

Nested loops and while loops are easiest to trust after you have counted what they do. The two plates below run the loops for real and report the counts.

```photogrid label="2.2" cols="2" ratio="1.1" caption="Nested loops are an odometer. (a) A car odometer: the right-hand wheel turns on every step, and each wheel to its left turns only when the wheel on its right rolls over from 9 to 0, exactly like an inner loop inside an outer loop. (b) A four-wheel odometer swept from 0000 to 9999 with four nested for loops: the units wheel changes 9,999 times, the tens wheel 999 times, the hundreds wheel 99 times and the thousands wheel 9 times. Each level of nesting multiplies the work by 10, which is why three nested loops over a list of 1,000 items would run 10^9 times."
@ photo id="bca254/odometer" cap="Odometer rolling over from 99999"
fit 1.1
focus 0.5 0.5
@ svg cap="Wheel changes in one sweep 0000 to 9999"
changes = [0, 0, 0, 0]; prev = None
for th in range(10):
    for hu in range(10):
        for te in range(10):
            for un in range(10):
                cur = (th, hu, te, un)
                if prev is not None:
                    for w in range(4):
                        if cur[w] != prev[w]: changes[w] += 1
                prev = cur
assert changes == [9, 99, 999, 9999] and 10 ** 4 == 10000 and 1000 ** 3 == 10 ** 9
names = ["thousands wheel", "hundreds wheel", "tens wheel", "units wheel"]
f = Fig(300, 214)
f.text(150, 11, "how often each wheel changes (4 nested loops)", size=10, color=NAVY, bold=True)
for i, (nm, c) in enumerate(zip(names, changes)):
    y = 26 + i * 34
    w = max(c * 170 / 9999, 2)
    col = TEAL if i == 3 else (AMBER if i == 2 else NAVY)
    f.text(6, y + 7, nm, size=9.5, color=SLATE, bold=True, anchor="start")
    f.box(6, y + 13, w, 14, "", fill=col, stroke=col, r=2)
    f.text(6 + w + 6, y + 21, "{:,}".format(c), size=10, color=col, bold=True, anchor="start")
f.text(150, 176, "outer wheel = outer loop: each level is 10 times rarer", size=9.5, color=SLATE, bold=True)
f.text(150, 196, "3 nested loops over 1,000 items = 10^9 steps", size=9.5, color=RED, bold=True)
```

```photogrid label="2.3" cols="2" ratio="1.3" caption="A while loop whose length is random. (a) Dice. The loop rolls a die until a six appears. (b) 20,000 games simulated with random.Random(2081): the number of rolls needed ranges from 1 upward with no fixed limit, which is exactly why this must be a while loop and not a for loop. The measured mean is close to the theoretical 6 rolls (the expected value of a geometric distribution with p = 1/6), and each bar sits near its theoretical height 20,000 x (5/6)^(k-1) x (1/6)."
@ photo id="bcamath/dice" cap="Dice"
fit 1.3
focus 0.5 0.5
@ svg cap="Rolls needed to get a six (20,000 games)"
import random
rg = random.Random(2081); N = 20000; hist = {}; tot = 0
for _ in range(N):
    n = 0
    while True:
        n += 1
        if rg.randint(1, 6) == 6: break
    hist[n] = hist.get(n, 0) + 1; tot += n
mean = tot / N
assert 5.7 < mean < 6.3 and max(hist) > 25
print("mean rolls", mean, "max", max(hist))
f = Fig(300, 232)
f.text(150, 11, "games needing k rolls (k = 1..14, mean %.2f)" % mean, size=10, color=NAVY, bold=True)
top = max(hist[k] for k in range(1, 15))
for k in range(1, 15):
    c = hist.get(k, 0); h = 140 * c / top; x = 14 + (k - 1) * 20
    th = N * (5 / 6) ** (k - 1) / 6
    f.box(x, 176 - h, 16, h, "", fill=TEAL, stroke=TEAL, r=1)
    f.circle(x + 8, 176 - 140 * th / top, 3, fill=AMBER, stroke=AMBER)
    f.text(x + 8, 190, str(k), size=9, color=SLATE, bold=True)
f.text(150, 208, "teal bars: simulation; amber dots: theory", size=9.5, color=SLATE, bold=True)
f.text(150, 224, "longest game: %d rolls (no upper limit)" % max(hist), size=9.5, color=AMBER, bold=True)
```

### 2.8.1 Eight good habits when writing conditions and loops

1. **Test the most specific case first.** In an `if/elif` chain Python stops at the first true test, so `marks >= 40` placed before `marks >= 80` would give every student only a pass. Write the strictest condition at the top and the general one last. Read the chain once from the top as a check before you run it.
2. **Use `elif`, not many separate `if` lines, for exclusive choices.** Separate `if` statements are all tested, which wastes time and can print two answers for one input. An `elif` chain runs exactly one branch. A ConnectIPS fee-slab program is a good example of one value falling into exactly one slab.
3. **Prefer `for` when the sequence is known and `while` when it is not.** `for subject in subjects:` cannot run forever, while a `while` loop that forgets to change its variable can. Use `while` for input validation or for repeating until a goal is reached. This one choice removes most infinite-loop bugs.
4. **Always change the loop variable in a `while` loop.** The condition must be able to become false, so something inside the body must move towards that. A missing `i += 1` is the most common cause of a program that seems to hang. Press Ctrl+C to stop it, then add the update.
5. **Use `range` and `enumerate` instead of counting by hand.** `for i, name in enumerate(names, start=1):` gives both the position and the item and cannot go out of range. It is shorter than `range(len(names))` and easier to read. A roll-number list printed from 1 is a typical use.
6. **Do not change a list while you loop over it.** Removing items from the list you are walking over skips elements, because the positions shift. Loop over a copy such as `for x in items[:]:` or build a new list with a comprehension. This avoids a bug that does not produce any error message.
7. **Keep nesting shallow.** A loop inside a loop inside an `if` is hard to read, and its running time grows as n x n. Use `continue` to skip unwanted cases early, or move the inner part into a function. Two levels are fine for patterns and tables; more deserves a function.
8. **Use loop `else` and `break` for searches.** Instead of a flag variable such as `found = False`, put the failure message in the `else` of the `for` loop. The code is shorter and shows the intent: "if no break happened, nothing was found". The weakness is that many beginners do not know this feature, so add a comment.

## Formula and fact sheet

- `if / elif / else`: first true branch only. `x if cond else y` is an expression.
- `while cond:` repeats while true. `for x in iterable:` walks a sequence.
- `range(start, stop, step)` excludes `stop`.
- `break` exits; `continue` skips; loop `else` runs if no `break`.
- Euclid: `while b: a, b = b, a % b`.

## Chapter summary

- `if/elif/else` and `match` choose among alternatives; conditions use comparison and logical operators.
- `while` repeats until a condition fails; `for` iterates over iterables; `range` generates integer sequences.
- `break`, `continue`, `pass` and loop `else` fine-tune loops; nested loops cost the product of their sizes.
- Classic algorithms (primes, GCD, factorial, Fibonacci, digit sums) are all small loops.

## Practice

1. Write a program that prints the grade for marks using the TU scale (≥ 80 Distinction, ≥ 60 First, ≥ 45 Second, ≥ 40 Pass, else Fail) for marks 85, 62, 47, 41, 12.
2. Explain the difference between `break` and `continue` with a short program that prints odd numbers up to 9 but stops at 7.
3. Print all primes below 50.
4. Compute the sum of the digits and the reverse of 4096.
5. Print the first ten terms of the Fibonacci series.
6. What does the loop `else` do? Show an example of a search that uses it.
7. Print this pattern for n = 4: a right triangle of `#` with 1, 2, 3, 4 symbols.

::: note Answers and worked solutions
**1.**

```python
def grade(m):
    if m >= 80: return "Distinction"
    if m >= 60: return "First"
    if m >= 45: return "Second"
    if m >= 40: return "Pass"
    return "Fail"
for m in (85, 62, 47, 41, 12):
    print(m, grade(m))
```
```output
85 Distinction
62 First
47 Second
41 Pass
12 Fail
```
**2.** `break` ends the loop; `continue` skips only the current iteration.

```python
for n in range(1, 10):
    if n % 2 == 0:
        continue
    if n > 7:
        break
    print(n, end=" ")
print()
```
```output
1 3 5 7 
```
**3.**

```python
print([n for n in range(2, 50) if all(n % d for d in range(2, int(n ** 0.5) + 1))])
```
```output
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```
**4.**

```python
n, s, rev = 4096, 0, 0
while n:
    s += n % 10
    rev = rev * 10 + n % 10
    n //= 10
print("sum", s, "reverse", rev)
```
```output
sum 19 reverse 6904
```
**5.**

```python
a, b = 0, 1
out = []
for _ in range(10):
    out.append(a)
    a, b = b, a + b
print(out)
```
```output
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```
**6.** The `else` block runs only if the loop was not ended by `break`:

```python
target = 7
for x in [2, 4, 6, 8]:
    if x == target:
        print("found")
        break
else:
    print("not found")
```
```output
not found
```
**7.**

```python
for i in range(1, 5):
    print("#" * i)
```
```output
#
##
###
####
```
:::

## Model answers (5 and 10 marks)

**Q1. Explain the `if`, `if-else`, `if-elif-else` and `match` statements of Python with examples. (5 marks)**

A **conditional statement** runs a block only when a condition is true. A block is marked by indentation after a colon.

- **`if`** runs the block when the condition is true and does nothing otherwise.
- **`if-else`** chooses between two blocks.
- **`if-elif-else`** chooses one block out of many. Tests are made from the top and the first true one is taken (Plate 2.1b), so the order matters.
- **Conditional expression:** `result = "Pass" if marks >= 40 else "Fail"` for a two-way value.
- **`match` (Python 3.10 and later)** compares one value against patterns such as `case 1:`, `case "Sat" | "Sun":` and `case _:` (the default). It is neat for menu choices and for splitting a tuple.

```python
def grade(marks):
    if marks >= 80:
        return "Distinction"
    elif marks >= 60:
        return "First division"
    elif marks >= 40:
        return "Pass"
    else:
        return "Fail"

def day_type(day):
    match day:
        case "Sat":
            return "holiday"
        case "Sun" | "Mon":
            return "working (Nepal week starts on Sunday)"
        case _:
            return "working"

print([grade(m) for m in (85, 60, 59, 40, 39)])
print(day_type("Sat"), "|", day_type("Sun"), "|", day_type("Wed"))
```
```output
['Distinction', 'First division', 'Pass', 'Pass', 'Fail']
holiday | working (Nepal week starts on Sunday) | working
```
Boundary marks 60 and 40 are tested on purpose, because `>=` includes the boundary. Conditions can be joined with `and`, `or` and `not`, and a chain such as `0 <= m <= 100` is allowed.

**Q2. Explain `break`, `continue`, `pass` and the `else` clause of a loop with a program. (5 marks)**

These four statements change the normal path of a loop (Fig. 2.2).

- **`break`** ends the innermost loop at once; control goes to the first statement after the loop.
- **`continue`** abandons the rest of the current pass and goes back to the loop test (for a `for` loop, to the next item).
- **`pass`** does nothing; it is a placeholder where Python needs a block, such as `class Empty: pass`.
- **`else` on a loop** runs only when the loop ends **without** `break`. For a search it means "not found".

The program lists the primes below 30 by trial division. `continue` skips the even numbers, `break` stops testing as soon as a divisor is found, and `else` records a prime.

```python
primes = []
for n in range(2, 30):
    if n > 2 and n % 2 == 0:
        continue
    for d in range(3, int(n ** 0.5) + 1, 2):
        if n % d == 0:
            break
    else:
        primes.append(n)
print(primes, len(primes))
for _ in range(2):
    pass
print("done")
```
```output
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29] 10
done
```
Because the loop only tries odd divisors up to the square root of `n`, a number such as 29 needs just 2 tests (3 and 5), not 27.

**Q3. Explain the `while` and `for` loops of Python with `range`. Write programs for a multiplication table, a star pattern and the digit sum of a number, and compare the two loops. (10 marks)**

**Introduction.** A **loop** repeats a block while a condition holds or for every item of a sequence. Python has two loops: `while`, which repeats on a condition, and `for`, which walks over an iterable. Both can be nested, and both accept `break`, `continue` and `else`.

**The `while` loop.** Syntax: `while condition:` followed by an indented body. The condition is tested **before** every pass, so the body may run zero times. The body must change something so that the condition becomes false, otherwise the loop never ends (Fig. 2.1 shows a `while` loop of 111 passes whose length nobody can guess).

**The `for` loop and `range`.** `for item in sequence:` takes each item in turn from a list, string, tuple, dictionary or `range`. `range(stop)`, `range(start, stop)` and `range(start, stop, step)` produce integers up to, but not including, `stop`. So `range(1, 11)` gives 1 to 10 and `range(10, 0, -3)` gives 10, 7, 4, 1. A `range` stores only its three numbers, not the whole list, so it uses very little memory.

**Programs.**

```python
n = 7
for i in range(1, 6):
    print(f"{n} x {i} = {n * i}")

for row in range(1, 5):
    print(" " * (4 - row) + "*" * (2 * row - 1))

num, total = 98765, 0
while num > 0:
    total += num % 10
    num //= 10
print("digit sum =", total)
```
```output
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
   *
  ***
 *****
*******
digit sum = 35
```
**Nested loops.** In the star pattern, the outer loop picks the row and the inner work (string repetition) draws its stars; a nested `for` inside a `for` runs the inner body rows x columns times, so 4 rows of 3 columns give 12 passes.

**Comparison.**

| Point | `while` | `for` |
|---|---|---|
| Repeats | while a condition is true | once for each item |
| Count known in advance | not needed | yes (the sequence is fixed) |
| Loop variable | updated by you | assigned by Python |
| Risk of an infinite loop | high | very low |
| Typical use | input validation, convergence | lists, ranges, files |
| `else` clause | runs when condition becomes false | runs when items are exhausted |

**Common mistakes:** forgetting the update in a `while` loop, expecting `range(5)` to include 5, and changing a list while looping over it.

**Conclusion.** Choose `for` when the items are known and `while` when only the stopping condition is known; use `break`, `continue` and `else` to steer the path, and keep nesting shallow.
