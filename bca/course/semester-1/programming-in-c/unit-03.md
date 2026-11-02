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
