---
subject: Programming in C
grade: BCA Semester 1
unit: 2
title: Elements of C: Tokens, Data Types, Operators and Console Input/Output
hours: 8
area: BCA 102 · Programming in C · Units 2 and 3
---

This chapter is the vocabulary and grammar of C: the smallest meaningful pieces (tokens), the kinds of data, the operators that combine them, and how to read and print values. Every later chapter assumes all of it.

::: key What this unit gives you
- The six token classes and the rules for identifiers.
- Every basic data type, its size and range, and when conversions happen silently.
- Constants, `const` and `#define`.
- All operators, precedence and associativity, and the classic pitfalls (`/` on integers, `=` vs `==`, `i++ + ++i`).
- `printf`, `scanf`, `getchar`, `putchar` with format specifiers.
:::

## 2.1 Character set and tokens

The C **character set** is letters (A–Z, a–z), digits (0–9), special characters (`+ - * / % = < > ! & | ^ ~ ( ) [ ] { } , ; : . ' " # ? \ _`) and white space (blank, tab, newline). A **token** is the smallest unit the compiler recognises:

| Token class | Examples |
|---|---|
| Keywords | `int`, `return`, `while`, `struct` (32 in C89, reserved; cannot be used as names) |
| Identifiers | `total`, `_count`, `student_1` |
| Constants | `25`, `3.14`, `'A'`, `0x1F` |
| String literals | `"Nepal"` |
| Operators | `+`, `==`, `&&`, `++` |
| Punctuators | `;`, `,`, `{ }`, `( )` |

**The 32 keywords of C89:** auto break case char const continue default do double else enum extern float for goto if int long register return short signed sizeof static struct switch typedef union unsigned void volatile while.

**Identifier rules.** Letters, digits and underscore only; must not start with a digit; case-sensitive; not a keyword; at least the first 31 characters are significant. `2fast`, `my-name`, `int`, `total marks` are invalid; `fast2`, `my_name`, `Int`, `total_marks` are valid. Choose meaningful names: `average` beats `a`.

## 2.2 Data types

| Type | Typical size (64-bit GCC) | Range | Specifier |
|---|---|---|---|
| `char` | 1 byte | −128 to 127 | `%c` (or `%d`) |
| `unsigned char` | 1 | 0 to 255 | `%u` |
| `short` | 2 | −32,768 to 32,767 | `%hd` |
| `int` | 4 | −2,147,483,648 to 2,147,483,647 | `%d` |
| `unsigned int` | 4 | 0 to 4,294,967,295 | `%u` |
| `long` | 8 on Linux/Mac, 4 on Windows | | `%ld` |
| `long long` | 8 | about ±9.22 × 10¹⁸ | `%lld` |
| `float` | 4 | about 6–7 significant digits | `%f` |
| `double` | 8 | about 15–16 significant digits | `%lf` (in `scanf`), `%f` (in `printf`) |

Sizes are **implementation-defined**; the standard only guarantees `char` is 1 byte and `short ≤ int ≤ long`. Old Turbo C (16-bit) had a 2-byte `int` ranging −32,768 to 32,767, which is why older exam answers say that. Use `sizeof(type)` to ask the compiler.

An *n*-bit signed integer in two's complement ranges from −2ⁿ⁻¹ to 2ⁿ⁻¹ − 1; unsigned from 0 to 2ⁿ − 1. Overflow of a **signed** integer is undefined behaviour; overflow of an unsigned wraps around modulo 2ⁿ.

```c
#include <stdio.h>
#include <limits.h>

int main(void)
{
    printf("char=%zu short=%zu int=%zu long long=%zu\n",
           sizeof(char), sizeof(short), sizeof(int), sizeof(long long));
    printf("float=%zu double=%zu\n", sizeof(float), sizeof(double));
    printf("INT_MAX=%d\n", INT_MAX);
    unsigned char u = 255;
    u = u + 1;
    printf("255 + 1 in an unsigned char = %d\n", u);
    return 0;
}
```
```output
char=1 short=2 int=4 long long=8
float=4 double=8
INT_MAX=2147483647
255 + 1 in an unsigned char = 0
```

**Derived** types are built from these (arrays, pointers, structures); **user-defined** types come from `typedef` and `enum`; `void` means "no value".

## 2.3 Variables and constants

A **variable** is a named memory location whose value can change. **Declare** before use: `int age;`. **Initialise** at declaration: `int age = 19;`. An uninitialised local variable holds garbage, not zero.

**Constants.**

| Kind | Examples | Notes |
|---|---|---|
| Integer | `25`, `-7`, `025` (octal = 21), `0x1F` (hex = 31), `100L`, `7u` | a leading `0` means octal: a classic trap |
| Real | `3.14`, `2.5e3` (= 2500), `1.5f` | a real literal is `double` unless suffixed `f` |
| Character | `'A'` (65), `'0'` (48), `'a'` (97), `'\n'` | a character constant is really an `int` code |
| String | `"BCA"` | array of characters ending with the hidden null character `'\0'`, so it occupies 4 bytes |

**Escape sequences:** `\n` newline, `\t` tab, `\\` backslash, `\"` quote, `\'` apostrophe, `\0` null, `\a` alert, `\b` backspace, `\r` carriage return.

**Symbolic constants.** `#define PI 3.14159` is textual replacement done by the preprocessor (no type, no memory, no semicolon). `const double PI = 3.14159;` is a real typed variable the compiler forbids you to change. Prefer `const`. Beware: `#define SQ(x) x*x` makes `SQ(2+3)` become `2+3*2+3 = 11`, not 25; write `#define SQ(x) ((x)*(x))`.

## 2.4 Operators

| Group | Operators |
|---|---|
| Arithmetic | `+ - * / %` |
| Relational | `< <= > >= == !=` (result is 1 or 0) |
| Logical | `&& || !` |
| Assignment | `= += -= *= /= %= <<= >>= &= ^= |=` |
| Increment/decrement | `++ --` (prefix and postfix) |
| Bitwise | `& | ^ ~ << >>` |
| Conditional | `?:` |
| Others | `sizeof`, comma `,`, address `&`, dereference `*`, member `.` `->` |

**Integer division and remainder.** `7 / 2` is `3`; `7 % 2` is `1`; `-7 / 2` is `-3` (truncates towards zero in C99); `-7 % 2` is `-1` (the sign follows the dividend). `%` works only on integers. `7 / 2.0` is `3.5`. A frequent bug: `float avg = (a + b) / 2;` with integer `a`, `b` loses the fraction before the assignment.

**Relational and logical.** C has no separate Boolean in C89; any non-zero value is true. `&&` and `||` **short-circuit**: in `x != 0 && y / x > 2` the division is never executed when `x` is 0. The classic mistake is `if (x = 5)`, which *assigns* 5 and is always true; the test is `==`.

**Increment/decrement.** `y = x++` copies `x` then increments; `y = ++x` increments then copies. Never modify the same variable twice in one expression (`i = i++ + ++i` is undefined behaviour; there is no "correct" output).

**Bitwise operators** work on each bit. `5 & 3 = 1` (0101 & 0011 = 0001); `5 | 3 = 7`; `5 ^ 3 = 6`; `~5 = -6`; `5 << 1 = 10` (multiply by 2); `20 >> 2 = 5` (divide by 4). Test bit *k*: `(n >> k) & 1`. Set bit *k*: `n | (1 << k)`. Clear: `n & ~(1 << k)`. Toggle: `n ^ (1 << k)`.

**Conditional operator.** `max = (a > b) ? a : b;` is the one-line form of an if-else.

**Precedence and associativity** (high to low):

| Rank | Operators | Associativity |
|---|---|---|
| 1 | `() [] -> .` postfix `++ --` | left to right |
| 2 | unary `+ - ! ~ ++ -- * & sizeof (type)` | **right to left** |
| 3 | `* / %` | left to right |
| 4 | `+ -` | left to right |
| 5 | `<< >>` | left to right |
| 6 | `< <= > >=` | left to right |
| 7 | `== !=` | left to right |
| 8 | `&` then `^` then `|` | left to right |
| 9 | `&&` then `||` | left to right |
| 10 | `?:` | right to left |
| 11 | `= += -=` etc. | **right to left** |
| 12 | `,` | left to right |

Memory device: *"Unary, Multiply, Add, Shift, Relate, Equate, Bit, Logic, Condition, Assign, Comma"*. Note `&` binds *looser* than `==`, so `x & 1 == 0` means `x & (1 == 0)`; write `(x & 1) == 0`.

**Type conversion.** *Implicit*: in a mixed expression the smaller type is promoted (`char`/`short` → `int` → `unsigned` → `long` → `float` → `double`); assigning a `double` to an `int` truncates. *Explicit cast*: `(double)a / b` converts `a` first, giving real division.

```c
#include <stdio.h>

int main(void)
{
    int a = 7, b = 2;
    printf("%d %d %d\n", a / b, a % b, -a / b);
    printf("%.2f %.2f\n", (double)a / b, (float)(a / b));
    int x = 5;
    int y = x++ + 10;
    int z = ++x * 2;
    printf("x=%d y=%d z=%d\n", x, y, z);
    printf("%d %d %d %d\n", 5 & 3, 5 | 3, 5 ^ 3, 20 >> 2);
    int m = (a > b) ? a : b;
    printf("max=%d, 8 > 3 > 1 is %d\n", m, 8 > 3 > 1);
    return 0;
}
```
```output
3 1 -3
3.50 3.00
x=7 y=15 z=14
1 7 6 5
max=7, 8 > 3 > 1 is 0
```

Check the last line: `8 > 3` is 1, then `1 > 1` is 0. Check `x`: starts 5; `x++` uses 5 (y = 15) and x becomes 6; `++x` makes 7, z = 14.

## 2.5 Formatted output with `printf`

`printf("format", args...)` copies the format text and replaces each `%…` with the next argument.

| Spec | Prints | Example → output |
|---|---|---|
| `%d` / `%i` | int | `printf("%d", 42)` → `42` |
| `%u` | unsigned | |
| `%ld`, `%lld` | long, long long | |
| `%f` | float/double (6 decimals) | `3.141593` |
| `%.2f` | 2 decimals | `3.14` |
| `%e` | scientific | `3.141593e+00` |
| `%c` | character | `printf("%c", 65)` → `A` |
| `%s` | string | |
| `%x`, `%X`, `%o` | hex, octal | `printf("%x", 255)` → `ff` |
| `%p` | pointer address | |
| `%%` | a percent sign | |

**Width, precision, flags:** `%5d` right-aligns in 5 columns, `%-5d` left-aligns, `%05d` pads with zeros (`00042`), `%8.3f` is width 8 with 3 decimals, `%+d` always shows the sign, `%10s` pads a string, `%.3s` prints at most 3 characters. `printf` returns the number of characters printed.

A type mismatch such as `printf("%d", 3.5)` prints garbage; the compiler (with `-Wall`) warns.

## 2.6 Input with `scanf`, `getchar`, `gets`-family

`scanf("%d", &n);` reads an integer into `n`. The **`&` is mandatory** for ordinary variables because `scanf` needs the *address* to store into; omit it and the program crashes or corrupts memory.

| To read | Use |
|---|---|
| int | `scanf("%d", &i)` |
| float | `scanf("%f", &f)` |
| double | `scanf("%lf", &d)` (note `l`) |
| char | `scanf(" %c", &c)` (the space before `%c` skips leftover white space) |
| word | `scanf("%s", name)` (stops at white space; no `&` because an array name is already an address) |
| a line | `fgets(line, sizeof line, stdin)` |

`scanf` returns the number of items successfully read, so `if (scanf("%d", &n) != 1)` detects bad input. **Never use `gets`**: it cannot limit the length, was removed in C11, and is the textbook source of buffer overflows. Use `fgets`.

`getchar()` reads one character and returns it as an `int` (`EOF` at end of input); `putchar(c)` writes one. `scanf("%d %d", &a, &b)` reads two numbers separated by any white space. After `scanf("%d")` the newline stays in the buffer, which is why a following `scanf("%c")` without the leading space appears to be "skipped".

```c
#include <stdio.h>

int main(void)
{
    int a, b;
    char op;
    scanf("%d %c %d", &a, &op, &b);
    if (op == '+')
        printf("%d + %d = %d\n", a, b, a + b);
    else if (op == '/' && b != 0)
        printf("%d / %d = %.3f\n", a, b, (double)a / b);
    else
        printf("unsupported\n");
    printf("[%5d][%-5d][%05d][%8.3f][%x]\n", a, a, a, 3.14159, 255);
    return 0;
}
```
```input
12 / 8
```
```output
12 / 8 = 1.500
[   12][12   ][00012][   3.142][ff]
```

## Formula and fact sheet

- Identifier: letters, digits, `_`; not starting with a digit; not a keyword; case-sensitive.
- Sizes: `char` 1, `short` 2, `int` 4 (modern), `long long` 8, `float` 4, `double` 8 bytes. Signed *n*-bit range: −2ⁿ⁻¹ … 2ⁿ⁻¹ − 1.
- `7/2 = 3`, `7%2 = 1`, `-7/2 = -3`, `-7%2 = -1`, `7/2.0 = 3.5`.
- `x++` uses then increments; `++x` increments then uses. `=` assigns, `==` compares.
- `&&`, `||` short-circuit. `(x & 1) == 0` tests even. `n << k` = n × 2ᵏ.
- `scanf` needs `&` (not for arrays); `%lf` for double in `scanf`; `" %c"` skips white space.
- `#define SQ(x) ((x)*(x))` – always parenthesise macro arguments.

## Chapter summary

- Tokens are keywords, identifiers, constants, strings, operators, punctuators.
- Pick the type by the range you need; integer arithmetic truncates, so cast before dividing when you want a real result.
- Precedence rules decide grouping; parentheses remove doubt. Never modify one variable twice in an expression.
- `printf` formats, `scanf` parses; check `scanf`'s return value and prefer `fgets` for lines.

## Practice

**A. Short questions**

1. Which of these are valid identifiers: `_total`, `9lives`, `float`, `Roll_No`, `a-b`?
2. What are the values of `17 / 5`, `17 % 5`, `-17 / 5`, `-17 % 5`, `17 / 5.0`?
3. What is the difference between `#define N 10` and `const int n = 10;`?
4. Explain why `scanf("%d", n)` (without `&`) is a bug.
5. What does `printf("%5.2f|%-6d|%c", 3.14159, 42, 66)` print?
6. Differentiate prefix and postfix increment with an example.
7. Distinguish `=` from `==`, and `&` from `&&`.

**B. Predict the output** (assume 4-byte `int`)

8. `int a = 10; printf("%d %d %d", a++, a, ++a);` Explain why you should not write this.
9. `int x = 6; printf("%d", x > 5 && x < 10 || x == 0);`
10. `printf("%d", 5 + 3 * 2 - 8 / 4 % 3);`
11. `int n = 12; printf("%d %d", n & 1, n >> 2);`
12. `float f = 7 / 2; printf("%.1f", f);`

**C. Programs.** Write a program that (13) reads a three-digit number and prints the sum of its digits; (14) converts a temperature from Celsius to Fahrenheit (F = 9C/5 + 32), taking care of integer division; (15) swaps two numbers with and without a third variable; (16) reads the radius and prints area and circumference to 2 decimals.

::: note Answers and worked solutions
**1.** Valid: `_total`, `Roll_No`. Invalid: `9lives` (starts with a digit), `float` (keyword), `a-b` (contains `-`).
**2.** 3, 2, −3, −2, 3.4.
**3.** `#define` is textual substitution by the preprocessor with no type and no storage; `const int n` is a typed object checked by the compiler, visible to a debugger, obeying scope rules.
**4.** `scanf` stores through an address. Passing the *value* of an uninitialised `n` as an address writes to a random location: crash or silent corruption.
**5.** ` 3.14|42    |B` (width 5 with a leading space; `-6` left-justifies 42 in 6 columns; 66 is `'B'`).
**6.** `int x = 5, y; y = x++;` gives y = 5, x = 6. `y = ++x;` gives y = 6, x = 6.
**7.** `=` assigns; `==` tests equality. `&` is bitwise AND of each bit (6 & 3 = 2); `&&` is logical AND of truth values and short-circuits (6 && 3 = 1).
**8.** Undefined behaviour: the order of evaluation of function arguments is unspecified, and `a` is modified and read without a sequence point. Any answer is "allowed"; write one change per statement.
**9.** `6 > 5 && 6 < 10` is true, so the whole is 1. (`&&` binds tighter than `||`.)
**10.** `3 * 2 = 6`; `8 / 4 = 2`, `2 % 3 = 2`; `5 + 6 - 2 = 9`.
**11.** `12 & 1 = 0` (12 is 1100); `12 >> 2 = 3`. Output `0 3`.
**12.** `7 / 2` is integer division = 3, converted to 3.0. Output `3.0`, not 3.5.
**13.** `int n, s = 0; scanf("%d", &n); s += n % 10; n /= 10; s += n % 10; n /= 10; s += n; printf("%d", s);`
**14.** `float f = 9.0f * c / 5 + 32;` (writing `9 / 5 * c` gives `1 * c` because `9 / 5` is 1).
**15.** With a temp: `t = a; a = b; b = t;`. Without: `a = a + b; b = a - b; a = a - b;` (or `a ^= b; b ^= a; a ^= b;`; both fail if `a` and `b` are the same object).
**16.** `printf("%.2f %.2f", 3.14159 * r * r, 2 * 3.14159 * r);` with `r` a `double` read using `%lf`.
:::
