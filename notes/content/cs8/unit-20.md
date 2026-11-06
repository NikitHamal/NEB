---
subject: Computer Science
grade: 8
unit: 20
title: Computer Programming using QBASIC
hours: 0
area: Programming
---

In Lesson 18 you planned solutions as algorithms and flowcharts, and in Lesson 19 you met the languages that turn plans into programs. Now you will write real programs in **QBASIC**: programs that read data from the keyboard, calculate, decide and repeat, and print their results on the screen. QBASIC is small, forgiving and almost plain English, which makes it an ideal first language. Every program in this lesson was run in two modern QBASIC-compatible systems, FreeBASIC 1.10 (`fbc -lang qb`) and QB64-PE 4.7, and the output shown under each program is exactly what appeared on the screen. Type them in, run them, and then change them: that is how programming is learnt.

::: key What the examination asks from this lesson
Expect **definitions and features** (QBASIC, the parts of its screen, character set, constants, variables, operators, library functions), the **syntax and use of statements** (CLS, REM, LET, INPUT, PRINT, END, IF … THEN … ELSE, SELECT CASE, FOR … NEXT, WHILE … WEND, DO … LOOP), **QBASIC expressions** from algebra, the **output** of a short program or of a library function (`LEN`, `LEFT$`, `MID$`, `INT`, `MOD`), **debugging** (find and correct the errors) and, above all, **writing complete programs**. A 4-mark program is marked by its parts: CLS and REM, correct input with a prompt, the correct calculation or condition or loop, correct output, and END.
:::

## 20.1 QBASIC: features and the QBASIC screen

::: definition QBASIC
**QBASIC** (Quick Beginner's All-purpose Symbolic Instruction Code) is a high-level programming language and its programming environment, made by Microsoft and supplied with MS-DOS 5.0 in 1991. It grew out of BASIC, which John Kemeny and Thomas Kurtz created at Dartmouth College in 1964. QBASIC programs are run by an **interpreter**, one statement at a time.
:::

### Features of QBASIC

1. **Easy to learn.** Its keywords are plain English words — `PRINT`, `INPUT`, `IF`, `THEN`, `FOR`, `NEXT`.
2. **Interpreter.** A program runs at once, without a separate compiling step, and stops at the first error with a message, so mistakes are easy to find.
3. **A smart editor.** When you finish typing a line, QBASIC checks its syntax, changes keywords to capital letters and points out mistakes straight away.
4. **Structured programming.** It has block IF, SELECT CASE, several kinds of loop, and SUB and FUNCTION procedures, so a program can be divided into clear parts. Line numbers are not needed.
5. **Many library functions** for mathematics, text, date and time.
6. **Graphics and sound** statements (such as `CIRCLE`, `LINE`, `SOUND` and `PLAY`) for drawing and music.
7. **Built-in help.** Pressing F1 on a keyword shows its syntax and an example.
8. Programs are saved as plain text files with the extension **.BAS**.

QBASIC was written for MS-DOS and does not run directly on 64-bit Windows. In computer labs today it is usually run in a DOS emulator such as DOSBox, or replaced by **QB64**, a free program that looks and works like QBASIC and runs the same programs on Windows, Linux and macOS.

### The QBASIC screen

When QBASIC starts, a welcome box appears; press **Esc** to clear it. The screen then has these parts.

```photo id="cs8/qb-qbi-screen" caption="The opening screen of the QuickBASIC Interpreter 1.0, the direct parent of QBASIC, which kept the same menus and windows. The numbers mark the parts named in the key." width="86"
mark 0.655 0.975 "1"
mark 0.575 0.943 "2"
mark 0.075 0.60 "3"
mark 0.10 0.182 "4"
mark 0.21 0.085 "5"
mark 0.93 0.022 "6"
mark 0.19 0.735 "7"
key 1 Menu bar: File, Edit, View, Search, Run, Debug, Options and Help. Press Alt to reach it from the keyboard.
key 2 Title bar: the name of the program file, "Untitled" until the program is saved.
key 3 Program window (view window): the large blue area where a program is typed and edited.
key 4 Scroll bars: move through a program that is longer or wider than the window.
key 5 Immediate window: a statement typed here, such as PRINT 7 * 6, runs at once when Enter is pressed.
key 6 Status bar: shortcut keys and, while you edit, the line and column of the cursor (such as 00001:001).
key 7 Welcome box: press Esc to clear it and start typing a program.
```

| Key | What it does |
|---|---|
| Shift + F5 | runs the program from the beginning (Run → Start) |
| F5 | continues a program that has paused (Run → Continue) |
| F4 | shows the output screen; any key returns to the program |
| F6 | moves the cursor between the program window and the Immediate window |
| F8 | runs the program one line at a time (Debug → Step) |
| F9 | sets or removes a breakpoint on the current line |
| F1 | help on the keyword under the cursor |
| Alt | selects the menu bar |
| Esc | closes a menu or a dialog box |

```photo id="cs8/qb-qb64-ide" caption="QB64, a free modern descendant of QBASIC, with its QBASIC-style menu bar, program window and, at the bottom, a status area showing the cursor's line and column (1:56). The program on the screen is an advanced one; the programs in this lesson run in QB64 exactly as typed." width="90"
```

```photogrid label="20.H" cols="4" ratio="1.25" caption="BASIC on real machines. (a) The Altair 8800 with a Teletype terminal, 1975: Altair BASIC was the first product of Microsoft. (b) The Commodore 64, which started straight into BASIC when switched on. (c) The ZX Spectrum, whose keys had BASIC words printed on them. (d) QB64, the modern free program that runs QBASIC programs. BASIC means Beginner's All-purpose Symbolic Instruction Code; John Kemeny and Thomas Kurtz made it at Dartmouth College in 1964 so that students could learn to program."
@ photo id="cs8/basic-altair" cap="(a) Altair 8800, 1975"
@ photo id="cs8/basic-c64" cap="(b) Commodore 64"
@ photo id="cs8/basic-zx" cap="(c) ZX Spectrum"
@ photo id="cs8/qb-qb64-ide" cap="(d) QB64 today"
```

## 20.2 Character set, constants, variables and operators

### Character set

The **character set** of QBASIC is the set of characters from which every statement is built.

| Group | Characters |
|---|---|
| Letters | A to Z and a to z |
| Digits | 0 to 9 |
| Special characters | `+ - * / \ ^ = < > ( ) . , ; : ' " $ % & ! # ?` and the space |

Words with a fixed meaning in QBASIC, such as `PRINT`, `INPUT`, `IF`, `FOR` and `END`, are called **keywords** or **reserved words**. They cannot be used as variable names.

### Constants and variables

Lesson 19 defined constants, variables and data types. In QBASIC:

- A **numeric constant** is written without commas or currency signs: `25000`, not `25,000` or `Rs 25000`. Very large or small numbers may use E notation: `1.5E+6` means 1,500,000.
- A **string constant** is written between double quotes: `"Pokhara"`, `"98"`.
- A **symbolic constant** is made with `CONST`: `CONST PI = 3.14` gives the name PI to 3.14, and the program cannot change it later.
- A **numeric variable** holds a number (`A`, `TOTAL`, `AGE%`); a **string variable** holds text and ends in `$` (`N$`, `ADDRESS$`). A variable's type can also be declared in words: `DIM AGE AS INTEGER`, `DIM NM AS STRING`.

### Operators

An **operator** is a symbol or word that tells the computer to do something with values (its **operands**). An **expression** combines constants, variables and operators into one value.

| Arithmetic operator | Meaning | Example | Result |
|---|---|---|---|
| `^` | exponent (power) | `2 ^ 5` | 32 |
| `*` | multiplication | `6 * 7` | 42 |
| `/` | division | `17 / 5` | 3.4 |
| `\` | integer division (the whole-number part of the quotient) | `17 \ 5` | 3 |
| `MOD` | remainder after division | `17 MOD 5` | 2 |
| `+` | addition | `17 + 5` | 22 |
| `-` | subtraction, or a negative sign | `17 - 5` | 12 |

**Relational** (comparison) operators compare two values and give **true** or **false**. QBASIC stores true as −1 and false as 0.

| Relational operator | Meaning | Example | Result |
|---|---|---|---|
| `=` | equal to | `5 = 5` | true (−1) |
| `<>` | not equal to | `5 <> 5` | false (0) |
| `>` | greater than | `5 > 3` | true |
| `<` | less than | `5 < 3` | false |
| `>=` | greater than or equal to | `7 >= 7` | true |
| `<=` | less than or equal to | `8 <= 7` | false |

**Logical** operators join conditions. **AND** is true only when both conditions are true; **OR** is true when at least one is true; **NOT** turns true into false and false into true. So `(5 > 3) AND (2 > 4)` is false, `(5 > 3) OR (2 > 4)` is true and `NOT (5 > 3)` is false.

| A | B | A AND B | A OR B | NOT A |
|---|---|---|---|---|
| true | true | true | true | false |
| true | false | false | true | false |
| false | true | false | true | true |
| false | false | false | false | true |

The **string operator** `+` joins (concatenates) strings: `"Kath" + "mandu"` gives `"Kathmandu"`.

### Hierarchy of operations

When an expression has several operators, QBASIC works them out in this order (the **hierarchy**, or precedence); operators of the same level are done from left to right.

| Order | Operation |
|---|---|
| 1 | brackets `( )`, innermost first |
| 2 | exponent `^` |
| 3 | negative sign `-` |
| 4 | multiplication `*` and division `/` |
| 5 | integer division `\` |
| 6 | `MOD` |
| 7 | addition `+` and subtraction `-` |
| 8 | relational operators `= <> < > <= >=` |
| 9 | `NOT`, then `AND`, then `OR` |

::: example Worked example 20.1 — evaluating and writing expressions
**Problem.** (a) Find the value of `10 + 8 / 2 ^ 2 * 3`. (b) Write QBASIC expressions for $\frac{a+b}{c}$, $a^2 + 2ab$ and $\sqrt{a^2 + b^2}$, and find their values when a = 3, b = 4 and c = 5.

**Solution.** (a) Exponent first: 2 ^ 2 = 4. Then division and multiplication from left to right: 8 / 4 = 2 and 2 * 3 = 6. Last, addition: 10 + 6 = **16**.

(b)

| Algebra | QBASIC expression | Value for A = 3, B = 4, C = 5 |
|---|---|---|
| $\frac{a+b}{c}$ | `(A + B) / C` | 7 / 5 = **1.4** |
| $a^2 + 2ab$ | `A ^ 2 + 2 * A * B` | 9 + 24 = **33** |
| $\sqrt{a^2 + b^2}$ | `SQR(A ^ 2 + B ^ 2)` | √25 = **5** |

QBASIC printed exactly these values, ` 1.4  33  5`, when the three expressions were run. In algebra *ab* means a × b, but in QBASIC the `*` must always be written: `2AB` is an error, `2 * A * B` is correct.
:::

## 20.3 Statements: CLS, REM, LET, INPUT, PRINT and END

A **statement** is one complete instruction. Each line of a QBASIC program usually holds one statement; two short statements may share a line if they are separated by a colon (`:`).

| Statement | Purpose | Syntax | Example |
|---|---|---|---|
| `CLS` | clears the output screen | `CLS` | `CLS` |
| `REM` | writes a remark (comment) for people; it is not carried out | `REM remark` or `' remark` | `REM Area of a circle` |
| `LET` | stores the value of an expression in a variable (assignment); the word LET may be left out | `[LET] variable = expression` | `LET S = A + B` |
| `INPUT` | waits for the user to type values and stores them in variables | `INPUT ["prompt";] variable list` | `INPUT "Your age"; A` |
| `PRINT` | displays values, text and results on the screen | `PRINT [list]` | `PRINT "Sum ="; S` |
| `END` | ends the program | `END` | `END` |

**INPUT** prints its prompt and waits. If a **semicolon** follows the prompt, QBASIC adds a question mark and a space (`Your age? `); with a **comma** it adds nothing (`Your age: ` is shown exactly as typed). Several variables can be read at once — `INPUT "Two numbers: ", A, B` — and the user then types the values separated by commas, such as `20, 8`. Type numbers **without** commas or units: typed as `25,000`, the number is read as two values, and QBASIC asks again with "Redo from start".

**PRINT** displays each item of its list. A **semicolon** prints the next item right after the last one; a **comma** moves to the next **print zone** (the screen is divided into zones of 14 columns, starting at columns 1, 15, 29, 43 and 57); `TAB(n)` moves to column n; and `PRINT` alone prints a blank line. A semicolon at the very end of a PRINT keeps the next output on the same line. QBASIC prints every number with a space in front (where a minus sign would go) and a space after it, so `PRINT "Sum ="; 28` shows `Sum = 28`.

```figure caption="Where PRINT puts things on the 80-column screen. A semicolon prints the next item straight after the last; a comma jumps to the start of the next 14-column zone (columns 1, 15, 29, 43 …); TAB(10) and TAB(25) move to columns 10 and 25. Every number carries a leading space for its sign."
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.2, 3.3))
ncol = 44
ax.set_xlim(-0.2, ncol + 0.2); ax.set_ylim(0.2, 10.2); ax.axis("off")
y0 = 9.15
for c in range(1, ncol + 1):
    zone = (c - 1) // 14
    ax.add_patch(Rectangle((c - 1, y0), 1, 0.65, fc=["#e3ecf7", "#f2f5f9"][zone % 2], ec="white", lw=0.6))
for c in (1, 10, 15, 25, 29, 43):
    ax.text(c - 0.5, y0 + 0.33, str(c), ha="center", va="center", fontsize=6.9, color=INK)
ax.text(7.0, y0 + 0.98, "zone 1", ha="center", va="center", fontsize=7.0, color=MUTED)
ax.text(21.0, y0 + 0.98, "zone 2", ha="center", va="center", fontsize=7.0, color=MUTED)
ax.text(35.0, y0 + 0.98, "zone 3", ha="center", va="center", fontsize=7.0, color=MUTED)
rows = [('PRINT "Name"; "Marks"', {1: "NameMarks"}),
        ('PRINT "Name", "Marks"', {1: "Name", 15: "Marks"}),
        ('PRINT "Asha", 87', {1: "Asha", 15: " 87"}),
        ('PRINT 1; TAB(10); "Asha"; TAB(25); 87', {1: " 1", 10: "Asha", 25: " 87"})]
for k, (stmt, items) in enumerate(rows):
    yt = 8.35 - k * 2.05
    ys = yt - 1.15
    ax.text(0, yt, stmt, ha="left", va="center", fontsize=7.6, family="monospace", color=SERIES[0])
    for c in range(1, ncol + 1):
        zone = (c - 1) // 14
        ax.add_patch(Rectangle((c - 1, ys), 1, 0.72, fc=["#eef3fa", "#fafbfc"][zone % 2], ec="#d5dbe4", lw=0.4))
    for start, txt in items.items():
        for i, ch in enumerate(txt):
            if ch != " ":
                ax.text(start + i - 0.5, ys + 0.36, ch, ha="center", va="center", fontsize=7.4,
                        family="monospace", color=INK, fontweight="bold")
ax.set_xticks([]); ax.set_yticks([])
```

::: example Program 20.1 — my first program
**Problem.** Write a program that displays the name and address of a school, a blank line, and the class.

**Solution.**

```basic
CLS
REM Program 20.1: my first program
PRINT "Shree Janata Secondary School"
PRINT "Biratnagar-7, Morang"
PRINT
PRINT "Class 8 Computer Science"
END
```

```text
Shree Janata Secondary School
Biratnagar-7, Morang

Class 8 Computer Science
```

The REM line does not appear in the output: it is a note for people reading the program.
:::

::: example Program 20.2 — semicolon, comma and TAB
**Problem.** Show the effect of `;`, `,` and `TAB` in PRINT statements.

**Solution.**

```basic
CLS
REM Program 20.2: semicolon, comma and TAB
PRINT "Name"; "Marks"
PRINT "Name", "Marks"
PRINT "Asha", 87
PRINT "Bikash", 92
PRINT "Roll"; TAB(10); "Name"; TAB(25); "Marks"
PRINT 1; TAB(10); "Asha"; TAB(25); 87
END
```

```text
NameMarks
Name          Marks
Asha           87
Bikash         92
Roll     Name           Marks
 1       Asha            87
```

The semicolon joined "Name" and "Marks" with no space. The comma started "Marks" at column 15; the numbers 87 and 92 begin at column 15 too, but their first character is the space for the sign. TAB lines up the columns of a table.
:::

::: example Program 20.3 — four operations on two numbers
**Problem.** Read two numbers and display their sum, difference, product and quotient.

**Solution.**

```basic
CLS
REM Program 20.3: four operations on two numbers
INPUT "Enter the first number"; A
INPUT "Enter the second number"; B
LET S = A + B
LET D = A - B
LET P = A * B
LET Q = A / B
PRINT "Sum ="; S
PRINT "Difference ="; D
PRINT "Product ="; P
PRINT "Quotient ="; Q
END
```

```text
Enter the first number? 20
Enter the second number? 8
Sum = 28
Difference = 12
Product = 160
Quotient = 2.5
```
:::

::: note The same in Python
```python
a = int(input("Enter the first number: "))
b = int(input("Enter the second number: "))
print("Sum =", a + b)
print("Difference =", a - b)
print("Product =", a * b)
print("Quotient =", a / b)
```

```text
Enter the first number: 20
Enter the second number: 8
Sum = 28
Difference = 12
Product = 160
Quotient = 2.5
```

Python's `input()` always gives text, so `int()` turns it into a whole number; QBASIC's INPUT does this by itself for a numeric variable.
:::

::: example Program 20.4 — simple interest and amount
**Problem.** Read the principal, time and rate, and display the simple interest and the amount. (This is the algorithm of Worked example 18.3, now coded.)

**Solution.**

```basic
CLS
REM Program 20.4: simple interest
INPUT "Principal (Rs)"; P
INPUT "Time (years)"; T
INPUT "Rate (% per year)"; R
SI = P * T * R / 100
A = P + SI
PRINT "Simple interest = Rs"; SI
PRINT "Amount = Rs"; A
END
```

```text
Principal (Rs)? 25000
Time (years)? 3
Rate (% per year)? 9.5
Simple interest = Rs 7125
Amount = Rs 32125
```

Check: 25,000 × 3 × 9.5 ÷ 100 = 7,125 and 25,000 + 7,125 = 32,125 ✓.
:::

::: example Program 20.5 — Celsius to Fahrenheit
**Problem.** Convert a temperature from degrees Celsius to degrees Fahrenheit using F = C × 9 ÷ 5 + 32.

**Solution.**

```basic
CLS
REM Program 20.5: Celsius to Fahrenheit
INPUT "Temperature in Celsius: ", C
F = C * 9 / 5 + 32
PRINT C; "degrees Celsius ="; F; "degrees Fahrenheit"
END
```

```text
Temperature in Celsius: 37
 37 degrees Celsius = 98.6 degrees Fahrenheit
```

The prompt ends with a comma, so no question mark appears. The output line starts with a space because it begins with a number.
:::

::: example Program 20.6 — area and circumference of a circle, with CONST
**Problem.** Read the radius of a circle and display its area (πr²) and circumference (2πr), taking π = 3.14.

**Solution.**

```basic
CLS
REM Program 20.6: area and circumference of a circle
CONST PI = 3.14
INPUT "Radius of the circle (cm)"; R
A = PI * R ^ 2
C = 2 * PI * R
PRINT "Area ="; A; "sq. cm"
PRINT "Circumference ="; C; "cm"
END
```

```text
Radius of the circle (cm)? 7
Area = 153.86 sq. cm
Circumference = 43.96 cm
```
:::

::: caution Five slips that stop a program
(1) A prompt or text without its closing quote. (2) A missing `*`: `2 * PI * R`, never `2PIR`. (3) A variable name that changes spelling in the middle of a program — `TOTAL` and `TOTL` are two different variables, and the misspelt one is 0. (4) `INPUT A, B` but only one value typed. (5) Forgetting `CLS` and `END` in an exam answer: the program may still run, but each carries a mark.
:::

## 20.4 Library functions: mathematical and string functions

::: definition Library function
A **library function** (built-in function) is a ready-made routine supplied with QBASIC that takes one or more values, called **arguments**, and gives back (**returns**) one result. A function is always used inside an expression or a statement, never alone: `PRINT SQR(16)` or `R = SQR(X)`. Functions whose names end in `$` return strings.
:::

### Mathematical functions

| Function | Returns | Example | Result |
|---|---|---|---|
| `SQR(x)` | square root of x (x must not be negative) | `SQR(144)` | 12 |
| `ABS(x)` | absolute value (the number without its sign) | `ABS(-25)` | 25 |
| `INT(x)` | the largest whole number not greater than x | `INT(7.8)`, `INT(-7.8)` | 7, −8 |
| `FIX(x)` | x with its decimal part removed | `FIX(7.8)`, `FIX(-7.8)` | 7, −7 |
| `CINT(x)` | x rounded to the nearest whole number | `CINT(7.8)`, `CINT(-7.3)` | 8, −7 |
| `SGN(x)` | 1 if x is positive, −1 if negative, 0 if zero | `SGN(-9)` | −1 |
| `SIN(x)`, `COS(x)`, `TAN(x)` | sine, cosine, tangent of x in radians | `COS(0)` | 1 |
| `LOG(x)`, `EXP(x)` | natural logarithm, and e to the power x | `EXP(0)` | 1 |
| `RND` | a random number from 0 up to (not including) 1 | `INT(RND * 6) + 1` | a dice throw, 1 to 6 |

::: example Program 20.7 — mathematical functions
**Problem.** Display the values of several mathematical functions.

**Solution.**

```basic
CLS
REM Program 20.7: mathematical functions
PRINT "SQR(144) ="; SQR(144)
PRINT "ABS(-25) ="; ABS(-25)
PRINT "INT(7.8) ="; INT(7.8); "  INT(-7.8) ="; INT(-7.8)
PRINT "FIX(7.8) ="; FIX(7.8); "  FIX(-7.8) ="; FIX(-7.8)
PRINT "CINT(7.8) ="; CINT(7.8); "  CINT(-7.3) ="; CINT(-7.3)
PRINT "SGN(-9) ="; SGN(-9); "  SGN(0) ="; SGN(0)
PRINT "17 MOD 5 ="; 17 MOD 5; "  2 ^ 10 ="; 2 ^ 10
END
```

```text
SQR(144) = 12
ABS(-25) = 25
INT(7.8) = 7   INT(-7.8) =-8
FIX(7.8) = 7   FIX(-7.8) =-7
CINT(7.8) = 8   CINT(-7.3) =-7
SGN(-9) =-1   SGN(0) = 0
17 MOD 5 = 2   2 ^ 10 = 1024
```

A negative number is printed with its minus sign in the place where a positive number has its leading space, which is why "=-8" has no gap.
:::

::: caution INT and FIX differ only for negative numbers
For 7.8 both give 7. For −7.8, `FIX` simply cuts off the decimals and gives −7, while `INT` goes down to the next whole number, −8, because −8 is less than −7.8. Students who learn "INT removes the decimal part" lose this mark every year.
:::

### String functions

| Function | Returns | Example (`W$ = "Kathmandu"`) | Result |
|---|---|---|---|
| `LEN(s$)` | the number of characters | `LEN(W$)` | 9 |
| `LEFT$(s$, n)` | the first n characters | `LEFT$(W$, 4)` | Kath |
| `RIGHT$(s$, n)` | the last n characters | `RIGHT$(W$, 5)` | mandu |
| `MID$(s$, p, n)` | n characters starting at position p | `MID$(W$, 3, 4)` | thma |
| `UCASE$(s$)` | the string in capital letters | `UCASE$(W$)` | KATHMANDU |
| `LCASE$(s$)` | the string in small letters | `LCASE$("NEPAL")` | nepal |
| `LTRIM$(s$)`, `RTRIM$(s$)` | the string without spaces on the left or right | `LTRIM$("   Nepal")` | Nepal |
| `ASC(s$)` | the ASCII code of the first character | `ASC("A")` | 65 |
| `CHR$(n)` | the character whose ASCII code is n | `CHR$(66)` | B |
| `STR$(n)` | a number turned into a string (with a leading space if positive) | `STR$(45)` | " 45" |
| `VAL(s$)` | a string of digits turned into a number | `VAL("12.5")` | 12.5 |
| `INSTR(s$, t$)` | the position where `t$` first appears in `s$` (0 if not found) | `INSTR(W$, "man")` | 5 |
| `SPACE$(n)`, `STRING$(n, c$)` | n spaces; n copies of a character | `STRING$(5, "*")` | ***** |
| `DATE$`, `TIME$` | today's date (mm-dd-yyyy) and the time (hh:mm:ss) from the computer's clock | `PRINT DATE$` | the date |

::: example Program 20.8 — string functions
**Problem.** Display the results of the main string functions on the word "Kathmandu".

**Solution.**

```basic
CLS
REM Program 20.8: string functions
W$ = "Kathmandu"
PRINT LEN(W$)
PRINT LEFT$(W$, 4)
PRINT RIGHT$(W$, 5)
PRINT MID$(W$, 3, 4)
PRINT UCASE$(W$); " "; LCASE$(W$)
PRINT ASC("A"); CHR$(66)
PRINT "["; STR$(45); "]"; VAL("12.5") + 1
PRINT "["; LTRIM$("   Nepal"); "]"; INSTR(W$, "man")
END
```

```text
 9
Kath
mandu
thma
KATHMANDU kathmandu
 65 B
[ 45] 13.5
[Nepal] 5
```

The square brackets show where each string starts and ends: `STR$(45)` keeps the leading space of a positive number, and `LTRIM$` removed the three spaces before "Nepal".
:::

## 20.5 Selection: IF...THEN...ELSE and SELECT CASE

Selection lets a program choose what to do, as the diamond does in a flowchart (Lesson 18).

**Single-line IF.** The whole decision is written on one line:

```basic
IF condition THEN statement
IF condition THEN statement1 ELSE statement2
```

For example, `IF M >= 35 THEN PRINT "Pass" ELSE PRINT "Fail"`.

**Block IF.** When each branch needs several statements, or there are more than two choices, use the block form. It must end with `END IF`.

```basic
IF condition1 THEN
    statements done when condition1 is true
ELSEIF condition2 THEN
    statements done when condition2 is true
ELSE
    statements done when no condition is true
END IF
```

The conditions are tested from the top, and only the **first** true branch is carried out. ELSEIF and ELSE parts may be left out. An IF inside another IF is a **nested IF**.

::: example Program 20.9 — odd or even
**Problem.** Read a whole number and say whether it is odd or even.

**Solution.** A number is even when the remainder after dividing by 2 is 0.

```basic
CLS
REM Program 20.9: odd or even
INPUT "Enter a whole number"; N
IF N MOD 2 = 0 THEN
    PRINT N; "is an even number."
ELSE
    PRINT N; "is an odd number."
END IF
END
```

Two runs:

```text
Enter a whole number? 46
 46 is an even number.
```

```text
Enter a whole number? -7
-7 is an odd number.
```
:::

::: example Program 20.10 — the greatest of three numbers
**Problem.** Read three numbers and display the greatest.

**Solution.** AND joins two conditions; `>=` handles equal numbers.

```basic
CLS
REM Program 20.10: the greatest of three numbers
INPUT "Enter three numbers: ", A, B, C
IF A >= B AND A >= C THEN
    G = A
ELSEIF B >= A AND B >= C THEN
    G = B
ELSE
    G = C
END IF
PRINT "The greatest number is"; G
END
```

```text
Enter three numbers: 45, 72, 68
The greatest number is 72
```
:::

::: caution IF A > B > C does not mean what it says
To test "A is greater than both", students write `IF A > B > C`. QBASIC first works out `A > B` as −1 or 0 and then compares that number with C, so the answer is nonsense. Join two complete conditions with AND: `IF A > B AND A > C THEN`.
:::

### SELECT CASE

When one value is compared with many possibilities, **SELECT CASE** is neater than a long chain of ELSEIFs.

```basic
SELECT CASE expression
    CASE value list
        statements
    CASE value1 TO value2
        statements
    CASE IS relational-operator value
        statements
    CASE ELSE
        statements
END SELECT
```

A CASE can list several values separated by commas (`CASE 1, 3, 5`), a range (`CASE 40 TO 49`), or a comparison (`CASE IS >= 90`). As with block IF, only the **first** matching CASE is carried out; `CASE ELSE` catches everything else.

::: example Program 20.11 — SEE grade from percentage
**Problem.** Read a percentage and display the letter grade of the SEE grading system: A+ (90 and above), A (80 to below 90), B+ (70–80), B (60–70), C+ (50–60), C (40–50), D (35–40) and NG (below 35).

**Solution.** The cases are checked from the top, so `CASE IS >= 80` is reached only by marks below 90.

```basic
CLS
REM Program 20.11: SEE grade from percentage
INPUT "Enter the percentage"; P
SELECT CASE P
    CASE IS > 100, IS < 0
        G$ = "not a valid percentage"
    CASE IS >= 90
        G$ = "A+"
    CASE IS >= 80
        G$ = "A"
    CASE IS >= 70
        G$ = "B+"
    CASE IS >= 60
        G$ = "B"
    CASE IS >= 50
        G$ = "C+"
    CASE IS >= 40
        G$ = "C"
    CASE IS >= 35
        G$ = "D"
    CASE ELSE
        G$ = "NG"
END SELECT
PRINT "Grade: "; G$
END
```

Three runs:

```text
Enter the percentage? 86.5
Grade: A
```

```text
Enter the percentage? 33
Grade: NG
```

```text
Enter the percentage? 105
Grade: not a valid percentage
```
:::

::: note The same in Python
Python has no SELECT CASE in the grade 9 course; an `if … elif … else` chain does the same job.

```python
p = float(input("Enter the percentage: "))
if p > 100 or p < 0:
    g = "not a valid percentage"
elif p >= 90:
    g = "A+"
elif p >= 80:
    g = "A"
elif p >= 70:
    g = "B+"
elif p >= 60:
    g = "B"
elif p >= 50:
    g = "C+"
elif p >= 40:
    g = "C"
elif p >= 35:
    g = "D"
else:
    g = "NG"
print("Grade:", g)
```

```text
Enter the percentage: 86.5
Grade: A
```
:::

::: example Program 20.12 — day of the week
**Problem.** Read a number from 1 to 7 and display the day of the week, Sunday being day 1.

**Solution.**

```basic
CLS
REM Program 20.12: day of the week
INPUT "Enter a day number (1 to 7)"; D
SELECT CASE D
    CASE 1
        PRINT "Sunday"
    CASE 2
        PRINT "Monday"
    CASE 3
        PRINT "Tuesday"
    CASE 4
        PRINT "Wednesday"
    CASE 5
        PRINT "Thursday"
    CASE 6
        PRINT "Friday"
    CASE 7
        PRINT "Saturday - the weekly holiday in Nepal"
    CASE ELSE
        PRINT "There is no day number"; D
END SELECT
END
```

Two runs:

```text
Enter a day number (1 to 7)? 7
Saturday - the weekly holiday in Nepal
```

```text
Enter a day number (1 to 7)? 9
There is no day number 9
```
:::

::: example Program 20.13 — vowel or consonant (SELECT CASE with strings)
**Problem.** Read a letter and say whether it is a vowel or a consonant.

**Solution.** `UCASE$` turns a small letter into a capital, so only capitals need to be listed. A string range such as `"B" TO "Z"` follows alphabetical order.

```basic
CLS
REM Program 20.13: vowel or consonant
INPUT "Enter a letter"; L$
L$ = UCASE$(L$)
SELECT CASE L$
    CASE "A", "E", "I", "O", "U"
        PRINT L$; " is a vowel."
    CASE "B" TO "Z"
        PRINT L$; " is a consonant."
    CASE ELSE
        PRINT "That is not a letter."
END SELECT
END
```

Three runs, with e, k and 7:

```text
Enter a letter? e
E is a vowel.
```

```text
Enter a letter? k
K is a consonant.
```

```text
Enter a letter? 7
That is not a letter.
```
:::

| Point | IF … THEN … ELSE | SELECT CASE |
|---|---|---|
| Tests | any conditions, possibly on different variables | one expression against many values |
| Joins conditions with AND, OR | yes | no (but a CASE may list several values) |
| Ranges | written as `M >= 40 AND M < 50` | written as `CASE 40 TO 49` or `CASE IS >= 40` |
| Best for | two or three choices, or mixed conditions | many choices on one value: grades, menus, days |
| Ends with | `END IF` (block form) | `END SELECT` |

## 20.6 Loops: FOR...NEXT, WHILE...WEND and DO...LOOP

A **loop** repeats a block of statements. QBASIC has three kinds.

**FOR … NEXT** repeats a fixed number of times, using a counter variable:

```basic
FOR counter = start TO end [STEP increment]
    statements
NEXT counter
```

The counter starts at `start`, goes up by the STEP (1 if STEP is left out) after each pass, and the loop stops when the counter passes `end`. A negative STEP counts down. The number of passes is (end − start) ÷ step + 1, ignoring any fraction: `FOR I = 1 TO 10 STEP 3` runs for I = 1, 4, 7 and 10, which is (10 − 1) ÷ 3 + 1 = 4 times.

**WHILE … WEND** repeats as long as a condition is true. The condition is tested **before** each pass, so if it is false at the start, the loop does not run at all.

```basic
WHILE condition
    statements
WEND
```

**DO … LOOP** is the most flexible. The test can be at the top (WHILE or UNTIL after DO) or at the bottom (after LOOP); WHILE means "repeat while true", UNTIL means "repeat until true". A loop with its test at the bottom always runs **at least once**.

```basic
DO WHILE condition          DO
    statements                  statements
LOOP                        LOOP UNTIL condition
```

```figure caption="The three loops as flowcharts. FOR … NEXT counts its passes; WHILE … WEND and DO WHILE … LOOP test before the body, so they may run zero times; DO … LOOP UNTIL tests after the body, so it always runs at least once."
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle
fig, ax = plt.subplots(figsize=(5.2, 3.6))
ax.set_xlim(0, 10.4); ax.set_ylim(0, 7.2); ax.axis("off")
FC = "#e8f1fa"; FS = 7.6
def proc(x, y, t, w=2.0, h=0.56):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=FC, ec=ACCENT, lw=1.2))
    ax.text(x, y, t, ha="center", va="center", fontsize=FS)
def dec(x, y, t, w=2.0, h=1.0):
    ax.add_patch(Polygon([(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)],
                         closed=True, fc=FC, ec=ACCENT, lw=1.2))
    ax.text(x, y, t, ha="center", va="center", fontsize=FS - 0.2, linespacing=1.1)
def arr(p, q):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0,
                mutation_scale=9, shrinkA=0, shrinkB=0))
def seg(xs, ys):
    ax.plot(xs, ys, color=INK, lw=1.0)
def lab(x, y, t, c, ha="left"):
    ax.text(x, y, t, ha=ha, va="center", fontsize=7.3, color=c, fontweight="bold")
x = 1.65
arr((x, 6.95), (x, 6.53)); proc(x, 6.25, "I = 1")
arr((x, 5.97), (x, 5.35)); dec(x, 4.85, "I ≤ 5?")
arr((x, 4.35), (x, 3.93)); lab(x + 0.08, 4.12, "Yes", SERIES[2])
proc(x, 3.65, "loop body"); arr((x, 3.37), (x, 2.93))
proc(x, 2.65, "I = I + 1")
seg([x - 1.0, x - 1.45], [2.65, 2.65]); seg([x - 1.45, x - 1.45], [2.65, 5.66]); arr((x - 1.45, 5.66), (x - 0.02, 5.66))
seg([x + 1.0, x + 1.35], [4.85, 4.85]); arr((x + 1.35, 4.85), (x + 1.35, 1.6)); lab(x + 1.03, 5.07, "No", SERIES[1])
ax.text(x + 1.35, 1.35, "after NEXT", ha="center", va="center", fontsize=7.2, color=MUTED)
ax.text(x + 0.35, 0.45, "FOR … NEXT", ha="center", va="center", fontsize=8.4, fontweight="bold")
x = 5.2
arr((x, 6.95), (x, 5.35)); dec(x, 4.85, "condition\ntrue?")
arr((x, 4.35), (x, 3.93)); lab(x + 0.08, 4.12, "Yes", SERIES[2])
proc(x, 3.65, "loop body")
seg([x, x], [3.37, 2.9]); seg([x, x - 1.45], [2.9, 2.9]); seg([x - 1.45, x - 1.45], [2.9, 5.66]); arr((x - 1.45, 5.66), (x - 0.02, 5.66))
seg([x + 1.0, x + 1.35], [4.85, 4.85]); arr((x + 1.35, 4.85), (x + 1.35, 1.6)); lab(x + 1.03, 5.07, "No", SERIES[1])
ax.text(x + 1.35, 1.35, "after WEND", ha="center", va="center", fontsize=7.2, color=MUTED)
ax.text(x + 0.35, 0.95, "WHILE … WEND,", ha="center", va="center", fontsize=8.4, fontweight="bold")
ax.text(x + 0.35, 0.45, "DO WHILE … LOOP", ha="center", va="center", fontsize=8.4, fontweight="bold")
x = 8.65
arr((x, 6.95), (x, 6.33)); proc(x, 6.05, "loop body")
arr((x, 5.77), (x, 5.15)); dec(x, 4.65, "condition\ntrue?")
seg([x - 1.0, x - 1.4], [4.65, 4.65]); seg([x - 1.4, x - 1.4], [4.65, 6.6]); arr((x - 1.4, 6.6), (x - 0.02, 6.6))
lab(x - 1.05, 4.87, "No", SERIES[1], ha="right")
arr((x, 4.15), (x, 1.6)); lab(x + 0.08, 3.9, "Yes", SERIES[2])
ax.text(x, 1.35, "after LOOP", ha="center", va="center", fontsize=7.2, color=MUTED)
ax.text(x, 0.45, "DO … LOOP UNTIL", ha="center", va="center", fontsize=8.4, fontweight="bold")
ax.set_xticks([]); ax.set_yticks([])
```

| Point | FOR … NEXT | WHILE … WEND / DO WHILE … LOOP | DO … LOOP UNTIL |
|---|---|---|---|
| Use when | the number of passes is known | the loop goes on while a condition holds | the body must run at least once |
| Where the test is | at the top (the counter is compared with the end value) | at the top | at the bottom |
| Fewest passes | 0 | 0 | 1 |
| Counter changed by | NEXT, automatically | a statement you write in the body | a statement you write in the body |

::: example Program 20.14 — multiplication table (FOR … NEXT)
**Problem.** Display the multiplication table of a number.

**Solution.**

```basic
CLS
REM Program 20.14: multiplication table
INPUT "Enter a number"; N
FOR I = 1 TO 10
    PRINT N; "x"; I; "="; N * I
NEXT I
END
```

```text
Enter a number? 7
 7 x 1 = 7
 7 x 2 = 14
 7 x 3 = 21
 7 x 4 = 28
 7 x 5 = 35
 7 x 6 = 42
 7 x 7 = 49
 7 x 8 = 56
 7 x 9 = 63
 7 x 10 = 70
```
:::

::: note The same in Python
`range(1, 11)` produces 1 to 10: the end value 11 is not included.

```python
n = int(input("Enter a number: "))
for i in range(1, 11):
    print(n, "x", i, "=", n * i)
```

```text
Enter a number: 7
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
7 x 6 = 42
7 x 7 = 49
7 x 8 = 56
7 x 9 = 63
7 x 10 = 70
```
:::

::: example Program 20.15 — counting with STEP
**Problem.** Display the even numbers from 2 to 20 and their sum, then count down from 10 to 1.

**Solution.**

```basic
CLS
REM Program 20.15: counting with STEP
PRINT "Even numbers from 2 to 20:"
S = 0
FOR I = 2 TO 20 STEP 2
    PRINT I;
    S = S + I
NEXT I
PRINT
PRINT "Their sum ="; S
PRINT "Countdown:"
FOR I = 10 TO 1 STEP -1
    PRINT I;
NEXT I
PRINT
PRINT "Blast off!"
END
```

```text
Even numbers from 2 to 20:
 2  4  6  8  10  12  14  16  18  20
Their sum = 110
Countdown:
 10  9  8  7  6  5  4  3  2  1
Blast off!
```

The semicolon after `PRINT I` keeps the numbers on one line; the empty `PRINT` after the loop ends that line.
:::

::: caution Counting down needs STEP -1
`FOR I = 10 TO 1` without `STEP -1` does not count down: the start is already past the end, so the loop body is skipped completely and nothing is printed. When FreeBASIC and QB64 ran such a loop, its body was carried out **0 times**.
:::

::: example Program 20.16 — factorial (FOR … NEXT)
**Problem.** Find the factorial of a number, N! = 1 × 2 × … × N.

**Solution.** F starts at 1 (not 0), because it is a product.

```basic
CLS
REM Program 20.16: factorial of a number
INPUT "Enter a number"; N
F = 1
FOR I = 1 TO N
    F = F * I
NEXT I
PRINT "Factorial of"; N; "is"; F
END
```

```text
Enter a number? 6
Factorial of 6 is 720
```
:::

::: example Program 20.17 — sum of digits, reverse and palindrome (WHILE … WEND)
**Problem.** Read a positive whole number. Find the sum of its digits and the number reversed, and say whether it is a palindrome (the same when reversed).

**Solution.** `N MOD 10` gives the last digit and `N \ 10` removes it; the loop goes on while digits are left. The original number is kept in M, because N is used up by the loop.

```basic
CLS
REM Program 20.17: sum of digits, reverse and palindrome
INPUT "Enter a positive whole number"; N
M = N
S = 0
R = 0
WHILE N > 0
    D = N MOD 10
    S = S + D
    R = R * 10 + D
    N = N \ 10
WEND
PRINT "Sum of the digits ="; S
PRINT "Reversed number ="; R
IF R = M THEN PRINT M; "is a palindrome." ELSE PRINT M; "is not a palindrome."
END
```

Two runs:

```text
Enter a positive whole number? 4521
Sum of the digits = 12
Reversed number = 1254
 4521 is not a palindrome.
```

```text
Enter a positive whole number? 12321
Sum of the digits = 9
Reversed number = 12321
 12321 is a palindrome.
```

Trace for 4521: digits 1, 2, 5, 4 come off one by one; S goes 1, 3, 8, 12; R goes 1, 12, 125, 1254; N goes 452, 45, 4, 0 and the loop stops.
:::

::: note The same in Python
Python writes MOD as `%` and integer division as `//`.

```python
n = int(input("Enter a positive whole number: "))
m = n
s = 0
r = 0
while n > 0:
    d = n % 10
    s = s + d
    r = r * 10 + d
    n = n // 10
print("Sum of the digits =", s)
print("Reversed number =", r)
if r == m:
    print(m, "is a palindrome.")
else:
    print(m, "is not a palindrome.")
```

```text
Enter a positive whole number: 4521
Sum of the digits = 12
Reversed number = 1254
4521 is not a palindrome.
```
:::

::: example Program 20.18 — Fibonacci series (DO WHILE … LOOP)
**Problem.** Display the Fibonacci numbers (0, 1, 1, 2, 3, 5, …, each the sum of the two before it) that are less than a given limit.

**Solution.**

```basic
CLS
REM Program 20.18: Fibonacci series below a limit
INPUT "Show the Fibonacci numbers below"; L
A = 0
B = 1
DO WHILE A < L
    PRINT A;
    C = A + B
    A = B
    B = C
LOOP
PRINT
END
```

```text
Show the Fibonacci numbers below? 100
 0  1  1  2  3  5  8  13  21  34  55  89
```

The number of terms is not known in advance, so a FOR loop does not fit; the loop runs while A is still below the limit.
:::

::: example Program 20.19 — add numbers until 0 is entered (DO … LOOP UNTIL)
**Problem.** Keep reading numbers until the user types 0, then display how many numbers were entered and their total.

**Solution.** The body must run at least once — a number has to be read before it can be tested — so the test goes at the bottom.

```basic
CLS
REM Program 20.19: add numbers until 0 is entered
T = 0
C = 0
DO
    INPUT "Enter a number (0 to stop)"; N
    T = T + N
    IF N <> 0 THEN C = C + 1
LOOP UNTIL N = 0
PRINT "You entered"; C; "numbers."
PRINT "Their total is"; T
END
```

```text
Enter a number (0 to stop)? 25
Enter a number (0 to stop)? 40
Enter a number (0 to stop)? 15
Enter a number (0 to stop)? 0
You entered 3 numbers.
Their total is 80
```
:::

::: note The same in Python
Python has no DO … LOOP UNTIL. A `while True` loop with `break` does the same: the test sits after the input.

```python
total = 0
count = 0
while True:
    n = float(input("Enter a number (0 to stop): "))
    if n == 0:
        break
    total = total + n
    count = count + 1
print("You entered", count, "numbers.")
print("Their total is", total)
```

```text
Enter a number (0 to stop): 25
Enter a number (0 to stop): 40
Enter a number (0 to stop): 15
Enter a number (0 to stop): 0
You entered 3 numbers.
Their total is 80.0
```
:::

::: example Program 20.20 — a number triangle (nested loops)
**Problem.** Display the pattern 1 / 1 2 / 1 2 3 / 1 2 3 4 / 1 2 3 4 5, one row per line.

**Solution.** The outer loop counts the rows (I = 1 to 5); the inner loop prints the numbers 1 to I on that row.

```basic
CLS
REM Program 20.20: a number triangle (nested loops)
FOR I = 1 TO 5
    FOR J = 1 TO I
        PRINT J;
    NEXT J
    PRINT
NEXT I
END
```

```text
 1
 1  2
 1  2  3
 1  2  3  4
 1  2  3  4  5
```

The inner loop must be completely inside the outer one: `NEXT J` comes before `NEXT I`.
:::

::: example Program 20.21 — reverse a word and count its vowels
**Problem.** Read a word, display it reversed, count its vowels, and say if it is a palindrome.

**Solution.** The loop runs backwards over the positions of the word, from `LEN(W$)` down to 1, taking one character at a time with `MID$`. `INSTR` checks whether that character appears in the list of vowels.

```basic
CLS
REM Program 20.21: reverse a word and count its vowels
INPUT "Enter a word"; W$
R$ = ""
V = 0
FOR I = LEN(W$) TO 1 STEP -1
    CH$ = MID$(W$, I, 1)
    R$ = R$ + CH$
    IF INSTR("AEIOUaeiou", CH$) > 0 THEN V = V + 1
NEXT I
PRINT "Reversed: "; R$
PRINT "Number of vowels:"; V
IF UCASE$(R$) = UCASE$(W$) THEN PRINT W$; " is a palindrome."
END
```

Two runs:

```text
Enter a word? Nepal
Reversed: lapeN
Number of vowels: 2
```

```text
Enter a word? Malayalam
Reversed: malayalaM
Number of vowels: 4
Malayalam is a palindrome.
```
:::

::: note The same in Python
`w[::-1]` reverses a string in one step, and `in` tests whether a character is in a string.

```python
w = input("Enter a word: ")
r = w[::-1]
v = 0
for ch in w:
    if ch in "AEIOUaeiou":
        v = v + 1
print("Reversed:", r)
print("Number of vowels:", v)
if r.upper() == w.upper():
    print(w, "is a palindrome.")
```

```text
Enter a word: Malayalam
Reversed: malayalaM
Number of vowels: 4
Malayalam is a palindrome.
```
:::

::: caution The loop that never ends
In Program 20.17, if the line `N = N \ 10` is left out, N never becomes 0, the condition `N > 0` stays true, and the program prints nothing and never stops. Press **Ctrl + Break** to stop a program that is stuck in a loop. Before running any WHILE or DO loop, find the line that moves the condition towards false.
:::

## 20.7 Writing, running and debugging simple programs

### From problem to program

1. **Plan** the solution: write the algorithm or draw the flowchart (Lesson 18) and list the input, process and output.
2. **Start QBASIC** (or QB64) and press Esc to clear the welcome box. For a new program choose **File → New**.
3. **Type** the program in the program window, one statement per line. QBASIC capitalises the keywords as you leave each line; if it shows an error box instead, correct that line at once.
4. **Run** the program with **Shift + F5** (Run → Start). Type the inputs it asks for.
5. **Read the output screen.** Press any key to return to the program; press F4 to see the output again.
6. **Test** with data whose answers you know, including unusual values.
7. **Save** with **File → Save** (or Save As), giving a name such as `MARKS.BAS`; in MS-DOS a file name has at most eight characters before the extension. **File → Open** loads a saved program; **File → Print** prints it; **File → Exit** closes QBASIC.

### Finding and fixing errors

- **Syntax errors** are caught as you type or when you run: QBASIC shows a message box and highlights the line.
- **Run-time errors** stop the running program with a message such as "Division by zero", "Overflow" or "Illegal function call", and the line is highlighted when you return to the editor.
- **Logical errors** give no message. Find them by comparing the output with the answers you worked out, by a **trace table**, by pressing **F8** to run one line at a time, by setting a **breakpoint** with **F9** to pause at a chosen line, or by typing `PRINT S` in the Immediate window while the program is paused, to see the value of S at that moment.

```figure caption="The cycle of writing, running and debugging a program. A program is finished only when it runs without an error message and gives the right output for every test."
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle
fig, ax = plt.subplots(figsize=(5.2, 4.2))
ax.set_xlim(0, 10.4); ax.set_ylim(0.2, 8.6); ax.axis("off")
FC = "#e8f1fa"; FS = 7.7
def proc(x, y, t, w=3.4, h=0.66, fc=FC):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=fc, ec=ACCENT, lw=1.2))
    ax.text(x, y, t, ha="center", va="center", fontsize=FS, linespacing=1.15)
def dec(x, y, t, w=2.8, h=1.15):
    ax.add_patch(Polygon([(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)],
                         closed=True, fc=FC, ec=ACCENT, lw=1.2))
    ax.text(x, y, t, ha="center", va="center", fontsize=FS - 0.2, linespacing=1.1)
def arr(p, q):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0,
                mutation_scale=9, shrinkA=0, shrinkB=0))
def seg(xs, ys):
    ax.plot(xs, ys, color=INK, lw=1.0)
x = 3.0
proc(x, 8.05, "Plan: algorithm or flowchart")
arr((x, 7.72), (x, 7.38)); proc(x, 7.05, "Type the program")
arr((x, 6.72), (x, 6.38)); proc(x, 6.05, "Run it: Shift + F5")
arr((x, 5.72), (x, 5.3)); dec(x, 4.72, "Error\nmessage?")
seg([x + 1.4, 6.55], [4.72, 4.72]); arr((6.55, 4.72), (6.55, 4.48))
ax.text(x + 1.5, 4.85, "Yes", ha="left", va="bottom", fontsize=7.3, color=SERIES[1], fontweight="bold")
proc(7.75, 4.1, "Read the message;\ncorrect the line", w=3.0, h=0.76, fc="#fbe9e8")
seg([7.75, 7.75], [4.48, 4.48])
arr((x, 4.15), (x, 3.72)); ax.text(x - 0.1, 3.98, "No", ha="right", va="center", fontsize=7.3, color=SERIES[2], fontweight="bold")
dec(x, 3.15, "Output right for\nthe test data?", w=3.2, h=1.15)
seg([x + 1.6, 6.25], [3.15, 3.15]); arr((6.25, 3.15), (6.25, 2.68))
ax.text(x + 1.7, 3.28, "No", ha="left", va="bottom", fontsize=7.3, color=SERIES[1], fontweight="bold")
proc(7.75, 2.25, "Find the logical error:\ntrace table, F8, F9,\nPRINT values", w=3.0, h=0.9, fc="#fbe9e8")
seg([9.25, 9.7], [4.1, 4.1]); seg([9.25, 9.7], [2.25, 2.25]); seg([9.7, 9.7], [2.25, 6.05])
arr((9.7, 6.05), (x + 1.72, 6.05))
arr((x, 2.57), (x, 2.08)); ax.text(x - 0.1, 2.33, "Yes", ha="right", va="center", fontsize=7.3, color=SERIES[2], fontweight="bold")
proc(x, 1.75, "Save it: File → Save, NAME.BAS", fc="#e5f4ea")
arr((x, 1.42), (x, 1.02))
ax.text(x, 0.8, "finished", ha="center", va="center", fontsize=7.6, color=MUTED)
ax.set_xticks([]); ax.set_yticks([])
```

::: example Program 20.22 — debugging a program
**Problem.** This program should find the average of N numbers typed by the user, but it has three faults. Find each, name its type, and write the corrected program.

```basic
CLS
REM Average of N numbers typed by the user
INPUT "How many numbers"; N
S = 1
FOR I = 1 TO N
    INPUT "Enter a number"; X
    S = S + X
NEXT J
PRINT "Average ="; S / N
END
```

**Solution.**

1. `NEXT J` does not match `FOR I`. QBASIC cannot pair them and refuses to run the program; FreeBASIC reported "FOR/NEXT variable name mismatch" and QB64 "Incorrect variable after NEXT". It must be `NEXT I`.
2. `S = 1` is a **logical error**: a sum must start at 0. With only the NEXT corrected, the numbers 12, 15, 9 and 20 gave "Average = 14.25" instead of 14, with no warning at all.
3. If the user enters 0 for N, `S / N` divides by zero — a **run-time error**. The corrected program checks N first.

```basic
CLS
REM Program 20.22: average of N numbers typed by the user
INPUT "How many numbers"; N
IF N <= 0 THEN
    PRINT "Nothing to average."
ELSE
    S = 0
    FOR I = 1 TO N
        INPUT "Enter a number"; X
        S = S + X
    NEXT I
    PRINT "Average ="; S / N
END IF
END
```

Two runs:

```text
How many numbers? 4
Enter a number? 12
Enter a number? 15
Enter a number? 9
Enter a number? 20
Average = 14
```

```text
How many numbers? 0
Nothing to average.
```

Check: (12 + 15 + 9 + 20) ÷ 4 = 56 ÷ 4 = 14 ✓.
:::

::: tip Writing a program in the examination
Start with `CLS` and a `REM` line saying what the program does; give every INPUT a clear prompt; use the same variable names throughout; indent the statements inside IF, SELECT CASE and loops; print the answer with a label (`PRINT "Area ="; A`); end with `END`. Then dry-run the program with one simple input and write that output below the program. In "give the output" questions, remember the leading space before every positive number, and trace loops in a table, one row per pass.
:::

::: note Activity 20.1 — the lab challenge
In pairs, in the computer lab: (1) Type and run Programs 20.3, 20.11 and 20.17 and save them as `OPS.BAS`, `GRADE.BAS` and `DIGITS.BAS`. (2) Change Program 20.14 so that it prints the table up to 20 and in the form 7 × 1 = 7. (3) Write a program that reads the electricity units used by a household and prints the bill at Rs 10 per unit with a minimum charge of Rs 100. (4) Write a program that prints the squares of the numbers 1 to 10, first with FOR … NEXT and then with WHILE … WEND. (5) Swap programs with your partner, find one error in each other's work by testing, and record it as a syntax, run-time or logical error.
:::

## Chapter summary

- **QBASIC** (Microsoft, 1991; from BASIC, 1964) is an interpreted, easy, structured language with a smart editor and built-in help; its screen has a title bar, menu bar, program window, Immediate window, scroll bars and status bar. Shift + F5 runs a program; F8 steps; F9 sets a breakpoint.
- **Character set**: letters, digits and special characters. **Operators**: arithmetic (`^ * / \ MOD + -`), relational (`= <> > < >= <=`, true = −1, false = 0), logical (NOT, AND, OR) and string `+`; brackets first, then `^`, then `* /`, then `\`, then MOD, then `+ -`.
- **Statements**: CLS clears the screen, REM writes a remark, LET assigns, INPUT reads (`;` adds "? "), PRINT displays (`;` joins, `,` jumps to a 14-column zone, TAB(n) moves to column n), END ends.
- **Library functions**: mathematical (SQR, ABS, INT, FIX, CINT, SGN, RND …) and string (LEN, `LEFT$`, `RIGHT$`, `MID$`, `UCASE$`, `LCASE$`, ASC, `CHR$`, `STR$`, VAL, INSTR …).
- **Selection**: single-line IF, block IF … ELSEIF … ELSE … END IF, and SELECT CASE with value lists, `TO` ranges, `IS` comparisons and CASE ELSE; only the first true branch runs.
- **Loops**: FOR … NEXT (known count; STEP, negative STEP to count down), WHILE … WEND and DO WHILE … LOOP (test first; may run 0 times), DO … LOOP UNTIL (test last; runs at least once); loops can be nested.
- **Writing and debugging**: plan, type, run, test with known answers, save as .BAS; syntax and run-time errors give messages, logical errors are found by testing, trace tables, F8 and F9.

## Practice questions

**Group A — Objective (1 mark each)**

1. Which statement clears the output screen? <span class="marks">[1]</span>
   (a) END (b) CLS (c) REM (d) CLEAR SCREEN
2. What is printed by `PRINT 17 MOD 5`? <span class="marks">[1]</span>
   (a) 3 (b) 3.4 (c) 2 (d) 5
3. What is the value of `LEN("NEPAL")`? <span class="marks">[1]</span>
   (a) 4 (b) 5 (c) 6 (d) NEPAL
4. `MID$("COMPUTER", 4, 3)` gives <span class="marks">[1]</span>
   (a) COM (b) PUT (c) MPU (d) TER
5. Which key runs a QBASIC program from the beginning? <span class="marks">[1]</span>
   (a) F1 (b) F4 (c) Shift + F5 (d) F9
6. How many times does `FOR I = 1 TO 10 STEP 3` repeat its body? <span class="marks">[1]</span>
   (a) 3 (b) 4 (c) 10 (d) 30
7. Which loop always runs its body at least once? <span class="marks">[1]</span>
   (a) FOR … NEXT (b) WHILE … WEND (c) DO WHILE … LOOP (d) DO … LOOP UNTIL
8. The value of `INT(-4.5)` is <span class="marks">[1]</span>
   (a) −4 (b) −5 (c) 4 (d) −4.5
9. In QBASIC the expression `2 ^ 3 * 2` gives <span class="marks">[1]</span>
   (a) 64 (b) 12 (c) 16 (d) 10
10. Which of these is a string function? <span class="marks">[1]</span>
    (a) SQR (b) ABS (c) `UCASE$` (d) INT
11. The REM statement is used to <span class="marks">[1]</span>
    (a) remove a line (b) write remarks that are not executed (c) repeat statements (d) read input
12. The QBASIC window in which a statement runs as soon as Enter is pressed is the <span class="marks">[1]</span>
    (a) program window (b) Immediate window (c) title bar (d) status bar

::: note Answers to Group A
**1.** (b) — CLS means clear screen.
**2.** (c) — 17 ÷ 5 = 3 remainder 2.
**3.** (b) — N, E, P, A, L: five characters.
**4.** (b) — three characters from position 4: P, U, T.
**5.** (c) — Shift + F5 is Run → Start.
**6.** (b) — I = 1, 4, 7, 10.
**7.** (d) — its test comes after the body.
**8.** (b) — INT goes down to the next whole number below −4.5.
**9.** (c) — the power first: 2 ^ 3 = 8, then 8 × 2 = 16.
**10.** (c) — `UCASE$` works on a string and returns a string.
**11.** (b) — REM lines are remarks for people.
**12.** (b) — the Immediate window carries out a statement at once.
:::

**Group B — Short answer (2 marks each)**

1. Write any four features of QBASIC. <span class="marks">[2]</span>
2. Write QBASIC expressions for (a) $\frac{a+b}{2}$ (b) $\pi r^2$ (c) $\sqrt{b^2-4ac}$ (d) $p \times t \times \frac{r}{100}$. <span class="marks">[2]</span>
3. Write the syntax and one example of the INPUT and PRINT statements. <span class="marks">[2]</span>
4. Write the output of `PRINT LEFT$("BHAKTAPUR", 4)`, `PRINT RIGHT$("BHAKTAPUR", 3)`, `PRINT MID$("BHAKTAPUR", 3, 4)` and `PRINT LEN("BHAKTAPUR")`. <span class="marks">[2]</span>
5. Differentiate between WHILE … WEND and DO … LOOP UNTIL. <span class="marks">[2]</span>
6. Write a program to find the area of a triangle from its base and height. <span class="marks">[2]</span>
7. Write a program to check whether a number is divisible by 5. <span class="marks">[2]</span>
8. Write a program to display the squares of the numbers from 1 to 5. <span class="marks">[2]</span>
9. Write the output of this program and say how many times the loop runs. <span class="marks">[2]</span>

```basic
FOR I = 1 TO 10 STEP 3
    PRINT I;
NEXT I
```

10. What is the difference between `/`, `\` and `MOD`? Give the value of each for 17 and 5. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Any four: it is easy to learn, with English keywords; programs are run by an interpreter, line by line; its smart editor checks syntax and capitalises keywords; it supports structured programming (block IF, SELECT CASE, loops, SUB and FUNCTION) without line numbers; it has many library functions; it has graphics and sound statements; it has built-in help (F1).

**2.** (a) `(A + B) / 2` (b) `3.14 * R ^ 2` (or `PI * R ^ 2` after `CONST PI = 3.14`) (c) `SQR(B ^ 2 - 4 * A * C)` (d) `P * T * R / 100`.

**3.** INPUT: `INPUT ["prompt";] variable list`, for example `INPUT "Enter your name"; N$`. PRINT: `PRINT [list of expressions separated by ; or ,]`, for example `PRINT "Total ="; T`.

**4.** The four statements print BHAK, PUR, AKTA and 9 on four lines (the 9 with a space in front, because it is a number).

**5.** WHILE … WEND tests its condition **before** each pass, so its body may run zero times, and it repeats **while** the condition is true. DO … LOOP UNTIL tests **after** each pass, so its body runs at least once, and it repeats **until** the condition becomes true.

**6.**

```basic
CLS
INPUT "Base and height of the triangle: ", B, H
A = 1 / 2 * B * H
PRINT "Area of the triangle ="; A
END
```

```text
Base and height of the triangle: 10, 6
Area of the triangle = 30
```

**7.**

```basic
CLS
INPUT "Enter a number"; N
IF N MOD 5 = 0 THEN PRINT N; "is divisible by 5." ELSE PRINT N; "is not divisible by 5."
END
```

```text
Enter a number? 35
 35 is divisible by 5.
```

**8.**

```basic
CLS
FOR I = 1 TO 5
    PRINT I ^ 2;
NEXT I
END
```

```text
 1  4  9  16  25
```

**9.** The output is ` 1  4  7  10`, on one line. The loop runs **4 times** (I = 1, 4, 7, 10; the next value, 13, is past 10).

**10.** `/` is ordinary division, `\` is integer division (the whole-number part of the quotient) and `MOD` gives the remainder. For 17 and 5: `17 / 5` = 3.4, `17 \ 5` = 3 and `17 MOD 5` = 2.
:::

**Group C — Long answer (4 marks each)**

1. Write a program that reads the marks of a student in five subjects, then displays the total, the percentage and the SEE grade (A+ 90 and above, A 80, B+ 70, B 60, C+ 50, C 40, D 35, NG below 35), using SELECT CASE. <span class="marks">[4]</span>
2. Write a program to display the series 5, 10, 15, …, 50 and the sum of its terms. <span class="marks">[4]</span>
3. Write a program to check whether a number is prime or composite. <span class="marks">[4]</span>
4. Write a program to display this pattern: <span class="marks">[4]</span>

```text
 5  4  3  2  1
 5  4  3  2
 5  4  3
 5  4
 5
```

5. Dry-run the program below in a trace table and write its output. <span class="marks">[4]</span>

```basic
CLS
N = 5
S = 0
WHILE N > 0
    S = S + N * N
    N = N - 2
WEND
PRINT "S ="; S
END
```

::: note Answers to Group C
**1.**

```basic
CLS
REM Total, percentage and grade from marks in five subjects
T = 0
FOR I = 1 TO 5
    PRINT "Marks in subject"; I;
    INPUT M
    T = T + M
NEXT I
P = T / 5
SELECT CASE P
    CASE IS >= 90
        G$ = "A+"
    CASE IS >= 80
        G$ = "A"
    CASE IS >= 70
        G$ = "B+"
    CASE IS >= 60
        G$ = "B"
    CASE IS >= 50
        G$ = "C+"
    CASE IS >= 40
        G$ = "C"
    CASE IS >= 35
        G$ = "D"
    CASE ELSE
        G$ = "NG"
END SELECT
PRINT "Total ="; T
PRINT "Percentage ="; P
PRINT "Grade: "; G$
END
```

```text
Marks in subject 1 ? 78
Marks in subject 2 ? 85
Marks in subject 3 ? 69
Marks in subject 4 ? 92
Marks in subject 5 ? 74
Total = 398
Percentage = 79.6
Grade: B+
```

(Marks: the loop or five INPUTs, the total and percentage, the SELECT CASE, and the output.)

**2.**

```basic
CLS
REM The series 5, 10, 15, ..., 50 and its sum
S = 0
FOR I = 5 TO 50 STEP 5
    PRINT I;
    S = S + I
NEXT I
PRINT
PRINT "Sum ="; S
END
```

```text
 5  10  15  20  25  30  35  40  45  50
Sum = 275
```

**3.** A prime number has exactly two factors, 1 and itself, so the program counts the factors.

```basic
CLS
REM Prime or composite
INPUT "Enter a whole number greater than 1"; N
C = 0
FOR I = 1 TO N
    IF N MOD I = 0 THEN C = C + 1
NEXT I
IF C = 2 THEN
    PRINT N; "is a prime number."
ELSE
    PRINT N; "is a composite number. It has"; C; "factors."
END IF
END
```

Two runs:

```text
Enter a whole number greater than 1? 29
 29 is a prime number.
```

```text
Enter a whole number greater than 1? 51
 51 is a composite number. It has 4 factors.
```

(51 = 3 × 17, so its factors are 1, 3, 17 and 51.)

**4.** Row I prints the numbers from 5 down to I.

```basic
CLS
REM A pattern made with nested loops
FOR I = 1 TO 5
    FOR J = 5 TO I STEP -1
        PRINT J;
    NEXT J
    PRINT
NEXT I
END
```

The program printed the pattern exactly as shown in the question.

**5.**

| Pass | N at the test | N > 0? | S = S + N × N | N = N − 2 |
|---|---|---|---|---|
| 1 | 5 | yes | 0 + 25 = 25 | 3 |
| 2 | 3 | yes | 25 + 9 = 34 | 1 |
| 3 | 1 | yes | 34 + 1 = 35 | −1 |
| — | −1 | no | — | — |

Output:

```text
S = 35
```
:::

**Group D — Extended answers (10 marks each, for deeper revision)**

1. What is QBASIC? Explain its eight features and the parts of the QBASIC screen. <span class="marks">[10]</span>
2. Explain the statements and library functions of QBASIC with programs. <span class="marks">[10]</span>
3. Explain selection and loops of QBASIC with programs and outputs. <span class="marks">[10]</span>

### Model answer D1: features of QBASIC (10 marks)

**Introduction.** **QBASIC** (Quick Beginner's All-purpose Symbolic Instruction Code) is a high-level programming language and its environment, made by Microsoft in 1991 as an improved form of BASIC. It is used in schools to teach the first lessons of programming (Plate 20.H).

**Features.**

1. **Easy to learn.** It uses English words such as PRINT, INPUT and IF, so a beginner can write a first program within minutes.
2. **Interpreter.** QBASIC runs the program line by line, so a mistake is found and shown at once. This helps in learning.
3. **Editor and environment in one.** Writing, running and debugging all happen in the same screen.
4. **Structured programming.** It has block IF, SELECT CASE, and loops such as FOR...NEXT, WHILE...WEND and DO...LOOP, which keeps programs neat.
5. **Built-in functions.** Mathematical and string functions such as SQR, INT, LEN and `UCASE$` are ready to use.
6. **Graphics and sound.** Simple commands like SCREEN, LINE, CIRCLE and SOUND draw pictures and make tones.
7. **Immediate window.** A statement typed in the lower window runs at once, which is good for testing.
8. **Modular programming and help.** SUB and FUNCTION procedures divide a long program into parts, and the Help menu explains every keyword.

**Parts of the QBASIC screen.**

| Part | Use |
|---|---|
| Title bar | Shows the name of the program (Untitled at first) |
| Menu bar | File, Edit, View, Search, Run, Debug, Options, Help |
| View (program) window | Where the program is typed |
| Immediate window | Runs a single statement at once |
| Status bar | Shows help keys and the cursor line and column |
| Scroll bars | Move through a long program |

**Steps to run.** Type the program, press **Shift + F5** (or choose **Run** → **Start**) to run it, **Alt + F** → **S** to save, and **F1** for help.

**Conclusion.** QBASIC is simple and powerful enough for learning the basics of programming, and these ideas carry over to Python and C.

### Model answer D2: statements, functions and programs (10 marks)

**Introduction.** A QBASIC program is a list of statements. The common ones are CLS (clear the screen), REM (a remark, not run), LET (give a value), INPUT (take a value from the user), PRINT (show a result) and END (stop the program).

**Program 1: area and circumference of a circle.**

```
CLS
REM Area and circumference of a circle
INPUT "Enter the radius: ", R
LET A = 3.14159 * R ^ 2
LET C = 2 * 3.14159 * R
PRINT "Area = "; A
PRINT "Circumference = "; C
END
```

For R = 7, A = 3.14159 × 49 = 153.9379 and C = 2 × 3.14159 × 7 = 43.98226. The output is: `Area =  153.9379` and `Circumference =  43.98226`.

| Line | Meaning |
|---|---|
| CLS | Clears the screen |
| REM | A comment for the reader; ignored by the computer |
| INPUT "text", R | Shows the text and stores the typed number in R |
| LET A = ... | Calculates and stores in A (LET is optional) |
| PRINT "text"; A | Shows the text and the value |
| END | Ends the program |

**Operators.** Arithmetic: + − * / ^ (power), \ (integer division) and MOD (remainder). For example, `17 MOD 5` is 2.

**Library functions.**

| Function | Meaning | Example | Result |
|---|---|---|---|
| SQR(x) | Square root | `SQR(81)` | 9 |
| INT(x) | Whole part (rounds down) | `INT(7.8)` | 7 |
| ABS(x) | Absolute value | `ABS(-5)` | 5 |
| `LEN(s$)` | Number of characters | `LEN("NEPAL")` | 5 |
| `UCASE$(s$)` | Capital letters | `UCASE$("nepal")` | NEPAL |
| `LEFT$(s$, n)` | First n characters | `LEFT$("COMPUTER", 3)` | COM |
| `RIGHT$(s$, n)` | Last n characters | `RIGHT$("COMPUTER", 3)` | TER |
| `MID$(s$, p, n)` | n characters from position p | `MID$("COMPUTER", 4, 3)` | PUT |

**Conclusion.** With INPUT, LET and PRINT, and a few functions, we can already write useful programs that take data, calculate and show the answer.

### Model answer D3: selection and loops in QBASIC (10 marks)

**Introduction.** **Selection** chooses between paths by a condition, and **loops** repeat a block of statements.

**Selection: IF...THEN...ELSE (division of a student).**

```
CLS
INPUT "Enter the marks: ", M
IF M >= 80 THEN
    PRINT "Distinction"
ELSEIF M >= 60 THEN
    PRINT "First division"
ELSEIF M >= 45 THEN
    PRINT "Second division"
ELSE
    PRINT "Below second division"
END IF
END
```

For M = 72, the first test is false and the second is true, so the output is `First division`.

**SELECT CASE** is neater when one value is compared with many choices.

```
INPUT "Enter day number (1-3): ", D
SELECT CASE D
    CASE 1
        PRINT "Sunday"
    CASE 2
        PRINT "Monday"
    CASE 3
        PRINT "Tuesday"
    CASE ELSE
        PRINT "Not in the list"
END SELECT
```

**Loops.**

1. **FOR...NEXT** repeats a fixed number of times. This program prints the sum of 1 to 10:

```
S = 0
FOR I = 1 TO 10
    S = S + I
NEXT I
PRINT "Sum = "; S
```

The output is `Sum =  55`. With `STEP 2`, `FOR I = 2 TO 10 STEP 2` gives 2, 4, 6, 8, 10.

2. **WHILE...WEND** repeats while the condition is true (the test is made first):

```
N = 1
S = 0
WHILE N <= 5
    S = S + N
    N = N + 1
WEND
PRINT "Sum = "; S
```

The output is `Sum =  15`.

3. **DO...LOOP** repeats until or while a condition. This asks again until the right password is typed:

```
DO
    INPUT "Enter the password: ", P$
LOOP UNTIL P$ = "neb8"
PRINT "Welcome"
```

| Loop | Test | Best when |
|---|---|---|
| FOR...NEXT | Counter reaches the limit | The number of repeats is known |
| WHILE...WEND | Before each pass | Repeating while a condition holds |
| DO...LOOP | Before or after (WHILE or UNTIL) | Repeating until something happens |

**Conclusion.** Selection lets a program decide and loops let it repeat, and together with INPUT and PRINT they make a complete program.
