---
subject: Programming in C
grade: BCA Semester 1
unit: 3
title: Control Statements: Decisions, Loops and Jumps
hours: 7
area: BCA 102 · Programming in C · Unit 4
---

Straight-line code runs once, top to bottom. Real programs *decide* and *repeat*. Control statements are the whole of that power, and every algorithm in the rest of your degree (searching, sorting, graph traversal) is built from them.

::: key What this unit gives you
- `if`, `if-else`, `else-if` ladder, nested `if`, and the dangling-else rule.
- `switch` and exactly when it falls through.
- `for`, `while`, `do-while`: which to choose, and the loop patterns that recur (counting, accumulating, digit processing, searching, nested loops for patterns).
- `break`, `continue`, `goto`.
- A tracing method for predicting loop output.
:::

## 3.1 Decision making

**`if`** runs a statement when the condition is non-zero:

```text
if (condition)
    statement;
else
    statement;
```

A body of more than one statement needs braces. *Always use braces*, even for one statement; adding a second line later without braces is a standard bug.

**else-if ladder.** Conditions are tested top to bottom and the first true one wins; put the most restrictive first.

```c
#include <stdio.h>

int main(void)
{
    int marks = 67;
    char grade;
    if (marks >= 90)      grade = 'A';
    else if (marks >= 80) grade = 'B';
    else if (marks >= 60) grade = 'C';
    else if (marks >= 40) grade = 'D';
    else                  grade = 'F';
    printf("%d -> %c\n", marks, grade);
    return 0;
}
```
```output
67 -> C
```

**Dangling else.** An `else` belongs to the *nearest unmatched* `if`, whatever the indentation suggests:

```c
#include <stdio.h>

int main(void)
{
    int a = 1, b = 0;
    if (a)
        if (b)
            printf("both\n");
        else
            printf("a only\n");
    return 0;
}
```
```output
a only
```

The `else` pairs with `if (b)`. To attach it to the outer `if`, wrap the inner one in braces.

**Leap-year logic**, a favourite exam program: a year is leap if divisible by 4 and not by 100, unless divisible by 400.

`if ((y % 4 == 0 && y % 100 != 0) || y % 400 == 0)`

Checks: 2000 → leap (400); 1900 → not (100 but not 400); 2024 → leap; 2026 → not.

### A decision with a time axis: the traffic light

A traffic-light controller is a decision made again and again. At every second it asks which part of the cycle the clock is in and then switches the lamps: if the position is below 40 the light is green, below 45 it is yellow, otherwise red. Plate 3.1 runs that controller for 300 seconds with `if`/`else if` and a `switch` on the state; the three cycles of 100 seconds give 120 s of green, 15 s of yellow and 165 s of red. Note how the two decision tools work together: `if` chooses the state from a range, and `switch` acts on the exact state value.

```photogrid label="3.1" cols="2" ratio="1.1" caption="Decisions repeated every second. (a) A traffic signal head: only one lamp is lit at a time. (b) A C program that decides the state from clock % 100 (green below 40, yellow below 45, red otherwise) run for 300 seconds: three cycles, totals computed by the program."
@ photo id="bca102/traffic" cap="Traffic signal: one state is selected every second"
fit 1.1
focus 0.5 0.5
@ svg cap="Three cycles of a 100-second signal"
def state(t):
    p = t % 100
    return 0 if p < 40 else (1 if p < 45 else 2)
seq = [state(t) for t in range(300)]
assert (seq.count(0), seq.count(1), seq.count(2)) == (120, 15, 165)
runs = []
for t, s in enumerate(seq):
    if not runs or runs[-1][0] != s: runs.append([s, t, 1])
    else: runs[-1][2] += 1
assert len(runs) == 9
fills = [("#bbf7d0", TEAL), ("#fde68a", AMBER), ("#fecaca", RED)]
f = Fig(400, 250)
f.text(200, 16, "Lamp state for t = 0 to 299 s", size=11, color=NAVY, bold=True)
sc = 380 / 300
for s, t0, n in runs:
    fl, st = fills[s]
    f.box(10 + t0 * sc, 40, n * sc, 40, "", fill=fl, stroke=st, r=1)
for t in (0, 100, 200, 300):
    f.line(10 + t * sc, 82, 10 + t * sc, 92, color=SLATE)
    f.text(10 + t * sc, 106, f"{t}", size=10.5, color=SLATE, anchor="middle")
for i, (nm, k, (fl, st)) in enumerate(zip(["green", "yellow", "red"], [120, 15, 165], fills)):
    y = 128 + i * 30
    f.box(14, y, 24, 20, "", fill=fl, stroke=st, r=3)
    f.text(48, y + 10, f"{nm}: {k} s = {k / 3:.0f} s per cycle", size=11, color=SLATE, bold=True, anchor="start", vmid=True)
f.text(200, 236, "9 state changes in 300 s (3 per cycle); asserted by a simulation.", size=10.5, color=SLATE)
```

## 3.2 The `switch` statement

```text
switch (integer-expression) {
    case constant1: statements; break;
    case constant2: statements; break;
    default: statements;
}
```

Rules: the expression must be an integer or character type (no `float`, no strings); case labels must be distinct integer *constants*; `default` is optional and may appear anywhere. Execution jumps to the matching label and then **falls through** every following label until a `break` or the closing brace. Fall-through is useful when several labels share code:

```c
#include <stdio.h>

int main(void)
{
    char c = 'e';
    switch (c) {
    case 'a': case 'e': case 'i': case 'o': case 'u':
        printf("vowel\n");
        break;
    default:
        printf("consonant\n");
    }
    int n = 2;
    switch (n) {
    case 1: printf("one ");
    case 2: printf("two ");
    case 3: printf("three ");
    default: printf("end");
    }
    printf("\n");
    return 0;
}
```
```output
vowel
two three end
```

The second switch shows the danger: with no `break`, `n = 2` prints "two", "three" and "end". Use `switch` for a menu or a fixed set of values; use `if` for ranges.

### The switch that keeps falling

Each `case` is only a label, not a closed box. After the matching label, C keeps running the following statements until it meets `break` or the closing brace. That behaviour is called fall-through and it is the usual cause of the "extra output" bug. Plate 3.2 runs the same four inputs through two versions of a menu: one with `break` after every case, and one where `case 1` and `case 3` forget it. Fall-through is useful when it is meant, for example `case 'a': case 'e': case 'i':` sharing one action for vowels.

```photogrid label="3.2" cols="2" ratio="1.1" caption="Selecting one of several positions. (a) A rotary selector switch: a knob with named positions, the hardware idea behind switch. (b) Output of a real C program for k = 1 to 4, with and without break statements."
@ photo id="bca102/selector" cap="Rotary selector: the knob points to exactly one position"
fit 1.1
focus 0.5 0.5
@ svg cap="Same menu, with and without break"
def with_break(k): return {1: "A", 2: "B", 3: "C"}.get(k, "D")
def fall(k):
    out = []
    if k == 1: out += ["A", "B"]
    elif k == 2: out += ["B"]
    elif k == 3: out += ["C", "D"]
    else: out += ["D"]
    return " ".join(out)
assert [fall(k) for k in range(1, 5)] == ["A B", "B", "C D", "D"]
assert [with_break(k) for k in range(1, 5)] == ["A", "B", "C", "D"]
f = Fig(400, 250)
f.text(200, 16, "Printed output for k = 1..4", size=11, color=NAVY, bold=True)
f.text(86, 40, "k", size=10.5, color=SLATE, bold=True)
f.text(190, 40, "break everywhere", size=10.5, color=TEAL, bold=True)
f.text(320, 40, "missing breaks", size=10.5, color=RED, bold=True)
for k in range(1, 5):
    y = 50 + (k - 1) * 40
    ok = with_break(k) == fall(k).replace(" ", "")
    f.box(60, y, 54, 32, str(k), fill=BLUE, stroke=NAVY, color=NAVY, size=12, bold=True)
    f.box(124, y, 130, 32, with_break(k), fill=MINT, stroke=TEAL, color=TEAL, size=12, bold=True)
    f.box(264, y, 130, 32, fall(k), fill=MINT if ok else ROSE, stroke=TEAL if ok else RED, color=TEAL if ok else RED, size=12, bold=True)
f.text(200, 232, "case 1 prints A B and case 3 prints C D: execution fell through.", size=10.5, color=SLATE)
```

## 3.3 Loops

A loop has four parts: **initialisation, condition, body, update**. Pick the form by what you know in advance.

| Loop | Form | Tested | Use when |
|---|---|---|---|
| `while` | `while (cond) body` | before each pass | number of passes unknown; may run zero times |
| `do-while` | `do body while (cond);` | after each pass | must run at least once (menus, input validation) |
| `for` | `for (init; cond; update) body` | before each pass | counted loops |

`for (;;)` is an infinite loop (an empty condition means true). **Trace** by writing a small table of variable values per iteration; it is the only reliable way to predict output.

```c
#include <stdio.h>

int main(void)
{
    int n = 4305, sum = 0, rev = 0;
    int t = n;
    while (t > 0) {
        int d = t % 10;
        sum += d;
        rev = rev * 10 + d;
        t /= 10;
    }
    printf("sum of digits = %d, reverse = %d\n", sum, rev);

    int i, fact = 1;
    for (i = 1; i <= 10; i++)
        fact *= i;
    printf("10! = %d\n", fact);

    int a = 0, b = 1;
    printf("Fibonacci:");
    for (i = 0; i < 10; i++) {
        printf(" %d", a);
        int next = a + b;
        a = b;
        b = next;
    }
    printf("\n");

    int k = 10;
    do {
        printf("%d ", k);
        k -= 3;
    } while (k > 0);
    printf("\n");
    return 0;
}
```
```output
sum of digits = 12, reverse = 5034
10! = 3628800
Fibonacci: 0 1 1 2 3 5 8 13 21 34
10 7 4 1 
```

Overflow warning: 13! does not fit in a 4-byte `int` (12! = 479,001,600 is the last that does); use `long long` or `double` for larger factorials.

**Common loop patterns.**

- *Counting*: `count++` when a condition holds.
- *Accumulating*: `sum += x`; `product *= x` (start at 0 and 1 respectively).
- *Digit processing*: `d = n % 10; n /= 10;` (Armstrong, palindrome, reverse, digit sum).
- *Prime test*: loop `i` from 2 while `i * i <= n`.
- *Search with early exit*: `break` when found.
- *Sentinel input*: read until a special value or until `scanf` returns something other than 1.

**Nested loops** — the outer loop drives rows, the inner drives columns:

```c
#include <stdio.h>

int main(void)
{
    int n = 4;
    for (int i = 1; i <= n; i++) {
        for (int s = 1; s <= n - i; s++)
            printf(" ");
        for (int j = 1; j <= 2 * i - 1; j++)
            printf("*");
        printf("\n");
    }
    return 0;
}
```
```output
   *
  ***
 *****
*******
```

(Declaring `int i` inside `for` needs C99 or later; compile with `-std=c99` or `-std=c11`.) For a pattern, count per row: spaces = `n − i`, stars = `2i − 1`; this "row formula" method solves every pattern question.

```svgfig label="3.1" caption="Flowcharts of the three control structures. (a) if-else chooses one of two paths; (b) the while loop tests first and may run zero times; (c) the do-while loop runs the body once before testing."
f = Fig(760, 270)
def dia(x, y, t):
    f.box(x - 52, y, 104, 40, t, fill=BLUE, stroke=NAVY, size=10.5, bold=True)
dia(100, 20, "cond?")
f.arrow([(100, 60), (100, 90)], color=NAVY); f.text(114, 80, "no", size=9.5, color=RED, bold=True)
f.box(40, 90, 120, 30, "else part", fill=SOFT, stroke=NAVY, size=10.5)
f.arrow([(152, 40), (205, 40), (205, 90)], color=NAVY); f.text(170, 33, "yes", size=9.5, color=TEAL, bold=True)
f.box(165, 90, 80, 30, "then part", fill=SOFT, stroke=NAVY, size=10.5)
f.arrow([(205, 120), (205, 150)], color=NAVY)
f.box(10, 150, 235, 28, "next statement", fill=SOFT, stroke=TEAL, size=10.5)
f.arrow([(100, 120), (100, 150)], color=NAVY)
f.text(30, 18, "(a) if-else", size=11, color=TEAL, bold=True)
dia(350, 20, "cond?")
f.arrow([(350, 60), (350, 94)], color=NAVY); f.text(364, 80, "true", size=9.5, color=TEAL, bold=True)
f.box(290, 94, 120, 30, "loop body", fill=SOFT, stroke=NAVY, size=10.5)
f.arrow([(290, 109), (255, 109), (255, 40), (298, 40)], color=AMBER)
f.arrow([(402, 40), (440, 40), (440, 160)], color=NAVY); f.text(420, 32, "false", size=9.5, color=RED, bold=True)
f.box(290, 150, 160, 28, "next statement", fill=SOFT, stroke=TEAL, size=10.5)
f.text(260, 12, "(b) while / for", size=11, color=TEAL, bold=True)
f.box(570, 20, 120, 30, "loop body", fill=SOFT, stroke=NAVY, size=10.5)
f.arrow([(630, 50), (630, 80)], color=NAVY)
dia(630, 80, "cond?")
f.arrow([(578, 100), (540, 100), (540, 35), (570, 35)], color=AMBER); f.text(556, 92, "true", size=9.5, color=TEAL, bold=True)
f.arrow([(630, 120), (630, 150)], color=NAVY); f.text(644, 140, "false", size=9.5, color=RED, bold=True)
f.box(550, 150, 160, 28, "next statement", fill=SOFT, stroke=TEAL, size=10.5)
f.text(540, 12, "(c) do-while", size=11, color=TEAL, bold=True)
f.text(380, 214, "while: entry-controlled (test, then body).   do-while: exit-controlled (body, then test).", size=10.5, color=SLATE)
f.text(380, 236, "for (init; test; update) is a while loop with the three parts on one line.", size=10.5, color=SLATE)
```

### Counting trips through a loop

The three loop statements are not interchangeable at the boundary. `for` and `while` test first, so they may run zero times; `do-while` tests last, so it always runs at least once. Plate 3.3 counts the real trips for three values of n, and also counts the trips of a nested loop and of a loop that uses `continue` and `break`. These numbers are the answers to a favourite exam question: how many times does the body run?

```photogrid label="3.3" cols="2" ratio="1.1" caption="How many times does the body run? (a) A rotary selector on the console of an IBM 1620, a 1960s computer whose programs were loops over memory addresses. (b) Trips counted by a real C program for three loop forms and three limits, plus a nested loop (1+2+...+10 = 55 trips) and a loop with continue and break (sum 867)."
@ photo id="bca102/ibm1620" cap="IBM 1620 console: selector for the memory address register display"
fit 1.1
focus 0.5 0.5
@ svg cap="Trips taken by for, while and do-while"
rows = []
for n in (0, 1, 5):
    fr = len(range(n)); wh = fr; do = max(1, n)
    rows.append((n, fr, wh, do))
assert rows == [(0, 0, 0, 1), (1, 1, 1, 1), (5, 5, 5, 5)]
assert sum(i for i in range(1, 101) if i % 3 and i <= 50) == 867 and sum(range(1, 11)) == 55
f = Fig(400, 250)
f.text(200, 16, "Body executions", size=11, color=NAVY, bold=True)
for j, h in enumerate(["limit n", "for", "while", "do-while"]):
    f.text(70 + j * 90, 42, h, size=10.5, color=SLATE, bold=True)
for i, r in enumerate(rows):
    y = 52 + i * 38
    for j, v in enumerate(r):
        hot = j == 3 and r[0] == 0
        f.box(30 + j * 90, y, 80, 30, str(v), fill=ROSE if hot else BLUE, stroke=RED if hot else NAVY, color=RED if hot else NAVY, size=12, bold=True)
f.text(200, 184, "n = 0: do-while still runs once.", size=10.5, color=RED, bold=True)
f.text(200, 208, "for i = 1..10, for j = 1..i  ->  55 trips", size=10.5, color=SLATE, bold=True)
f.text(200, 228, "i = 1..100, skip multiples of 3, stop above 50  ->  sum 867", size=10.5, color=SLATE, bold=True)
```

## 3.4 `break`, `continue`, `goto`

- `break` leaves the *innermost* loop or `switch` immediately.
- `continue` skips the rest of the current iteration and goes to the update (in `for`) or condition (in `while`).
- `goto label;` jumps to a label in the same function. It is legal, rarely justified; one accepted use is leaving several nested loops at once. Avoid it elsewhere: it produces "spaghetti" flow.

```c
#include <stdio.h>

int main(void)
{
    int i;
    for (i = 1; i <= 10; i++) {
        if (i % 2 == 0)
            continue;
        if (i > 7)
            break;
        printf("%d ", i);
    }
    printf("| stopped at i=%d\n", i);
    return 0;
}
```
```output
1 3 5 7 | stopped at i=9
```

Trace: even `i` skipped; at `i = 9` (odd, > 7) the loop breaks, so `i` is 9 afterwards.

::: caution Loop traps
`for (i = 0; i < 5; i++);` — the stray semicolon is an empty body; the following block runs once. `while (i = 5)` assigns instead of testing. `for (float x = 0; x != 1.0; x += 0.1)` may never terminate because 0.1 has no exact binary form; compare with `<` or a tolerance. An unsigned counter counting down with `i >= 0` never ends because it cannot go negative.
:::

### The loop that nobody could prove would end

Edsger Dijkstra argued in 1968 that unrestricted `goto` makes programs hard to understand, and the structured statements of this chapter (`if`, `switch`, `for`, `while`, `do-while`) grew from that idea. Even a very short loop can behave in a way that is hard to predict. The Collatz rule (halve an even number, triple and add one to an odd number) is a two-line `while` loop, yet nobody has proved that it always reaches 1. Plate 3.4 plots the real trajectory of 27, which takes 111 steps and climbs to 9,232 before collapsing.

```photogrid label="3.4" cols="2" ratio="1.1" caption="A short loop with a long life. (a) Edsger W. Dijkstra, whose 1968 letter on goto helped make structured programming standard. (b) The path of the Collatz loop starting from 27, computed by the same while loop as in C: 111 steps and a peak of 9,232."
@ photo id="bca102/dijkstra" cap="Edsger W. Dijkstra (1930-2002)"
fit 1.1
focus 0.5 0.35
@ svg cap="while (n != 1) from n = 27"
n, path = 27, [27]
while n != 1:
    n = n // 2 if n % 2 == 0 else 3 * n + 1
    path.append(n)
assert len(path) - 1 == 111 and max(path) == 9232
def steps(s):
    c = 0
    while s != 1:
        s = s // 2 if s % 2 == 0 else 3 * s + 1; c += 1
    return c
assert max(range(1, 100), key=steps) == 97 and steps(97) == 118
f = Fig(400, 260)
f.text(200, 16, "Collatz path of 27 (value against step)", size=11, color=NAVY, bold=True)
L, T, W, H = 40, 34, 340, 170
f.line(L, T + H, L + W, T + H, color=SLATE); f.line(L, T, L, T + H, color=SLATE)
pts = [(L + i / 111 * W, T + H - v / 9232 * H) for i, v in enumerate(path)]
for a, b in zip(pts, pts[1:]):
    f.line(a[0], a[1], b[0], b[1], color=NAVY, sw=1.3)
pk = path.index(9232)
f.circle(pts[pk][0], pts[pk][1], 4, fill=ROSE, stroke=RED)
f.text(pts[pk][0] + 8, pts[pk][1] + 4, f"9,232 at step {pk}", size=10.5, color=RED, bold=True, anchor="start")
for v in (0, 4000, 9232):
    f.text(L - 4, T + H - v / 9232 * H + 4, f"{v:,}", size=10.5, color=SLATE, anchor="end")
f.text(L, T + H + 16, "0", size=10.5, color=SLATE); f.text(L + W, T + H + 16, "111", size=10.5, color=SLATE)
f.text(200, 238, "Below 100 the longest start is 97: 118 steps.", size=10.5, color=SLATE, bold=True)
f.text(200, 254, "No one has proved that every start ends at 1.", size=10.5, color=SLATE)
```

## 3.5 Eight uses of loops and decisions in real programs

1. **Menu-driven programs.** A `do-while` loop shows the menu at least once and repeats until the user chooses Exit. A `switch` then selects the action. A mobile top-up or ATM menu in Nepal works in just this way.
2. **Input validation.** A loop asks again until the value is acceptable, for example a mark between 0 and 100. The decision `if (m < 0 || m > 100)` stops wrong data from entering the record. This protects every later calculation.
3. **Processing a list of records.** A `for` loop visits each student, voter or customer in turn to add, count or find the largest. A TU result program with 500 students needs one loop and a few decisions. Without loops the same code would have to be written 500 times.
4. **Grading and classification.** An `if-else if` ladder maps a percentage to Distinction, First, Second or Pass. The conditions are tested from top to bottom, and the first true one wins. The order of the conditions therefore matters.
5. **Searching and sorting.** Linear search uses a loop with a `break` when the key is found, and bubble sort uses a loop inside a loop. These are the base of every directory and phone-book function. The number of repeats decides the speed.
6. **Number problems.** Sum of digits, reversal, prime test, GCD and Fibonacci series all use `while` loops with `%` and `/`. A prime test loops only up to the square root of n to save work. These are the favourite exam programs.
7. **Pattern printing.** Nested loops print triangles and pyramids: the outer loop controls the rows, the inner loop controls the columns. This trains the habit of tracing two counters together. The same idea draws rows and columns on a screen.
8. **Games and real-time monitoring.** A game loop reads input, updates the state and redraws the screen until the player quits. A sensor program that checks a river level every minute and sounds an alarm above a limit is also an endless loop with a decision. In such programs a `break` is the safe exit.

## Formula and fact sheet

- `else` pairs with the nearest `if`. `switch` falls through without `break`; its expression must be integral.
- `while` and `for` test first; `do-while` runs at least once.
- Pattern rows: spaces `n − i`, stars `2i − 1` for a centred pyramid.
- Leap year: `(y%4==0 && y%100!=0) || y%400==0`.
- Digit loop: `d = n % 10; n /= 10;` · reverse: `rev = rev*10 + d`.
- 12! = 479,001,600 is the largest factorial in a 32-bit `int`.

## Chapter summary

- Decide with `if`/`else if`/`switch`; repeat with `for`/`while`/`do-while`.
- Trace loops in a table; count iterations by hand before running.
- `break` exits, `continue` skips, `goto` is a last resort.
- The commonest bugs are `=` for `==`, an accidental `;` after `for`/`if`, missing `break`, and floating-point loop counters.

## Practice

**A. Predict the output**

1. `int i; for (i = 0; i < 3; i++) printf("%d ", i * i); printf("%d", i);`
2. `int n = 5, s = 0; while (n) { s += n; n -= 2; } printf("%d", s);`
3. `int x = 0; do { x += 5; } while (x < 5); printf("%d", x);`
4. `for (int i = 1; i <= 3; i++) for (int j = 1; j <= i; j++) printf("%d", i * j);`
5. `int k = 3; switch (k) { case 1: printf("A"); case 3: printf("B"); case 4: printf("C"); break; case 5: printf("D"); }`

**B. Programs**

6. Read a number and print whether it is prime.
7. Print all Armstrong numbers from 100 to 999 (153 = 1³ + 5³ + 3³).
8. Read n and print the sum 1 + 1/2 + 1/3 + … + 1/n to 4 decimals (careful with integer division).
9. Print the pattern with n = 4: row i has the numbers 1 … i.
10. Menu-driven calculator using `do-while` and `switch` that quits on option 5.

::: note Answers and worked solutions
**1.** `0 1 4 3` (squares 0, 1, 4; after the loop `i` is 3).
**2.** It never ends. Trace: s = 5, n = 3; s = 8, n = 1; s = 9, n = −1. The value −1 is non-zero, hence true, so n keeps decreasing past zero. Test `n > 0` instead of `n`.
**3.** The body runs once before the test: x = 5, test `5 < 5` false. Output `5`.
**4.** i = 1 prints `1`; i = 2 prints `2` and `4`; i = 3 prints `3`, `6`, `9`. No separators are printed, so the output is `124369`.
**5.** k = 3 jumps to `case 3`: prints `B`, falls to `case 4` prints `C`, then `break`. Output `BC`.
**6.** `scanf("%d",&n); int p = n >= 2; for (int i = 2; i * i <= n; i++) if (n % i == 0) { p = 0; break; } printf(p ? "prime" : "not prime");`
**7.** For n from 100 to 999: `a = n/100, b = n/10%10, c = n%10`; if `a*a*a + b*b*b + c*c*c == n` print. The four are 153, 370, 371, 407.
**8.** `double s = 0; for (int i = 1; i <= n; i++) s += 1.0 / i; printf("%.4f", s);` (`1 / i` would be 0 for i > 1.)
**9.** `for (i = 1; i <= 4; i++) { for (j = 1; j <= i; j++) printf("%d ", j); printf("\n"); }`
**10.** `do { printf("1.Add 2.Sub 3.Mul 4.Div 5.Quit: "); scanf("%d",&ch); switch (ch) { case 1: ...; break; ... case 5: break; default: printf("invalid"); } } while (ch != 5);`
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Differentiate between `if-else if` ladder and `switch`. Write a program that prints the day name for a number from 1 to 7.**

Both statements choose one action out of many. The **`if-else if` ladder** tests a chain of conditions from top to bottom and runs the block of the first true condition; its conditions can be any logical or relational expression, including ranges such as `marks >= 80`. The **`switch`** compares one integer or character expression with constant `case` labels, jumps directly to the matching label and needs `break` to stop falling into the next case; a `default` label handles all other values.

| Point | `if-else if` | `switch` |
|---|---|---|
| Condition | any expression, ranges, `&&` `\|\|` | one integer/char value against constants |
| Data types | int, float, char, strings (with `strcmp`) | int and char only |
| Speed | tests one by one | often a jump table, faster |
| Missing `break` | not applicable | falls through to next case |
| Best use | ranges, grades | menus, days, options |

```c
#include <stdio.h>
int main(void) {
    int d;
    scanf("%d", &d);
    switch (d) {
        case 1: printf("Sunday\n");    break;
        case 2: printf("Monday\n");    break;
        case 3: printf("Tuesday\n");   break;
        case 4: printf("Wednesday\n"); break;
        case 5: printf("Thursday\n");  break;
        case 6: printf("Friday\n");    break;
        case 7: printf("Saturday\n");  break;
        default: printf("Invalid day\n");
    }
    return 0;
}
```

For input 6 the output is `Friday`. In Nepal's week Saturday is the holiday, so a programmer could group `case 7` with a message "Holiday" without any change to the other cases.

**Q (10 marks). Explain the loop statements of C with syntax, flowchart and an example of each. Compare the `while`, `do-while` and `for` loops, and explain `break` and `continue`.**

*Introduction.* A **loop** repeats a block of statements as long as a condition holds. Loops remove repeated code, so a program that handles 500 students needs the same few lines as one that handles 5. C has three loops: `while`, `do-while` and `for` (Figure 3.1).

*The while loop.* `while (condition) { body }`. The condition is tested **first**; if it is false at the start, the body never runs (entry-controlled). Example: `i = 1; while (i <= 5) { printf("%d ", i); i++; }` prints `1 2 3 4 5`.

*The do-while loop.* `do { body } while (condition);` The body runs **once before** the test (exit-controlled), so it always runs at least once. Note the semicolon after the condition. It suits menus: `do { show_menu(); scanf("%d", &c); } while (c != 0);`

*The for loop.* `for (init; condition; update) { body }`. The initialisation runs once, then the condition is tested before every pass and the update runs after every pass. Example: `for (i = 1; i <= 5; i++) sum += i;` gives sum = 15. It is the best choice when the number of repeats is known.

*Jump statements.* **`break`** leaves the nearest loop or `switch` at once; for example, a linear search stops when the key is found. **`continue`** skips the rest of the current pass and goes to the next test (in a `for` loop to the update); for example, skipping negative marks while adding. `goto` jumps to a label and should be avoided.

*Comparison.*

| Point | `while` | `do-while` | `for` |
|---|---|---|---|
| Test position | before body | after body | before body |
| Minimum runs | 0 | 1 | 0 |
| Best when | repeats unknown | menu, validation | repeats known |
| Init/update | separate lines | separate lines | in header |
| Semicolon at end | no | **yes** | no |

*Nested loops.* A loop inside a loop runs the inner loop fully for each pass of the outer loop. A 4-row triangle uses `for (i = 1; i <= 4; i++) { for (j = 1; j <= i; j++) printf("*"); printf("\n"); }` and prints 1, 2, 3 and 4 stars in the four rows, 10 stars in total.

*Conclusion.* The three loops are interchangeable in power, so the choice is about clarity: `for` for counting, `while` for waiting on a condition, `do-while` when the body must run once. A loop must always change something that leads to a false condition, or it never ends.
