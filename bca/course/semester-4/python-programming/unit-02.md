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
