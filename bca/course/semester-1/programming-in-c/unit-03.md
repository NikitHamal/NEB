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
