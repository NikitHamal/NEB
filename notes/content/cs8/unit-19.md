---
subject: Computer Science
grade: 8
unit: 19
title: Fundamentals of Computer Programming
hours: 0
area: Programming
---

A computer's processor understands only one thing: patterns of 0s and 1s. People, on the other hand, think in words and numbers. A **programming language** is the bridge between the two. This lesson explains the kinds of programming language, the translator programs that turn what we write into what the machine runs, the three kinds of mistake every programmer makes and how to find them, four languages you will meet in school and beyond, and the basic building blocks of every program: constants, variables and data types. Lesson 20 then puts all of it to work in QBASIC.

::: key What the examination asks from this lesson
Expect **definitions** (programming language, machine language, assembly language, high-level language, compiler, interpreter, assembler, source code, object code, bug, debugging, constant, variable), two-point **differences** (low-level and high-level language, compiler and interpreter, syntax and logical error, constant and variable), **lists** (rules for naming variables, QBASIC data types and their symbols) and a **4-mark question** that explains the three levels of language or the three types of error with examples. A favourite short question gives a few variable names and asks which are valid.
:::

## 19.1 Programming languages: low-level (machine and assembly) and high-level languages

::: definition Programming language
A **programming language** is a set of words, symbols and rules (its **syntax**) used to write instructions that a computer can carry out. A program written in a programming language is called **code**, and writing it is called **coding**.
:::

Programming languages are divided into two groups according to how close they are to the machine.

### Low-level languages

A **low-level language** is close to the hardware: each instruction does one tiny job inside the processor, and a program written for one type of processor does not work on another. There are two low-level languages.

**Machine language** (first generation, 1GL) is written entirely in **binary** — 0s and 1s. It is the only language the processor understands directly, so it needs no translation and runs fastest. But it is almost impossible for people to read, very easy to get wrong, and different for every family of processors (it is **machine-dependent**). The first computers were programmed this way, by setting switches or punching holes in cards.

**Assembly language** (second generation, 2GL) replaces each binary instruction with a short word called a **mnemonic**: MOV (move), ADD, SUB (subtract), JMP (jump). It is easier to read than binary, but it is still machine-dependent and needs one instruction for each tiny step. A program called an **assembler** translates it into machine language. Assembly language is still used where speed and size matter most, as in parts of device drivers and the tiny chips inside washing machines and remote controls.

### High-level languages

A **high-level language** (third generation, 3GL, and later) uses English words and ordinary mathematical signs, such as `PRINT`, `IF`, `INPUT` and `C = A + B`. One high-level statement may stand for many machine instructions. High-level programs are easy to read, write and correct, and the same program works on many kinds of computer (it is **portable**, or machine-independent). They must be translated into machine language by a **compiler** or an **interpreter** before they run. QBASIC, Python, C, C++ and Java are high-level languages. Some books also name **fourth-generation languages (4GL)** such as SQL, used to ask a database for information, and **fifth-generation languages (5GL)** such as Prolog, used in artificial intelligence.

```figure caption="The same job — add 3 to 5 — at three levels of language. The two assembly instructions and the four machine-code bytes are real Intel x86 code: MOV AL, 5 is the byte pair 10110000 00000101 and ADD AL, 3 is 00000100 00000011."
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 3.3))
ax.set_xlim(0, 10.4); ax.set_ylim(0, 6.6); ax.axis("off")
bands = [(4.55, "High-level language", "C = 5 + 3", "English words and maths signs;\nportable; easy to read", SERIES[0]),
         (2.55, "Assembly language", "MOV AL, 5\nADD AL, 3", "mnemonics, one per machine\ninstruction; machine-dependent", SERIES[2]),
         (0.55, "Machine language", "10110000 00000101\n00000100 00000011", "binary; runs directly on the\nprocessor; very hard to read", SERIES[3])]
for y, name, code, note, c in bands:
    ax.add_patch(FancyBboxPatch((1.2, y), 9.0, 1.5, boxstyle="round,pad=0,rounding_size=0.16",
                                fc=c, ec="none", alpha=0.14))
    ax.add_patch(FancyBboxPatch((1.2, y), 9.0, 1.5, boxstyle="round,pad=0,rounding_size=0.16",
                                fc="none", ec=c, lw=1.2))
    ax.text(1.45, y + 1.18, name, ha="left", va="center", fontsize=8.6, fontweight="bold", color=c)
    ax.text(3.9, y + 0.62, code, ha="center", va="center", fontsize=8.6, family="monospace",
            color=INK, linespacing=1.3)
    ax.text(7.65, y + 0.70, note, ha="center", va="center", fontsize=7.5, color=MUTED, linespacing=1.25)
ax.annotate("", xy=(0.55, 0.6), xytext=(0.55, 6.0),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.4, mutation_scale=12))
ax.text(0.25, 3.3, "closer to people  →  closer to the machine", rotation=-90, ha="center", va="center",
        fontsize=7.4, color=MUTED)
ax.text(5.2, 4.29, "↓ translated by a compiler or an interpreter", ha="center", va="center",
        fontsize=7.4, color=INK, bbox=dict(fc="white", ec="none", pad=1.2))
ax.text(5.2, 2.29, "↓ translated by an assembler", ha="center", va="center",
        fontsize=7.4, color=INK, bbox=dict(fc="white", ec="none", pad=1.2))
ax.set_xticks([]); ax.set_yticks([])
```

| Point | Low-level language | High-level language |
|---|---|---|
| Form | binary (machine) or mnemonics (assembly) | English-like words and mathematical signs |
| Closeness | close to the machine | close to the programmer |
| Ease | hard to write, read and correct | easy to write, read and correct |
| Portability | machine-dependent | machine-independent (portable) |
| Translation | none (machine) or an assembler | a compiler or an interpreter |
| Speed of the program | very fast, small | a little slower and larger |
| Examples | machine code, assembly language | QBASIC, Python, C, Java |

```photo id="cs8/prog-fortran-card" caption="A punched card carrying one line of a FORTRAN program. Until the 1970s each line of a program was typed on a card punch, one card per line; the printed text along the top shows what the rectangular holes in the columns below mean. The computer read the holes, so a dropped and shuffled deck of cards was a shuffled program." width="78"
```

::: example Worked example 19.1 — which level, and which translator?
**Problem.** For each piece of code, name the level of language and the translator (if any) needed before it can run: (a) `10110000 00000101` (b) `ADD AL, 3` (c) `PRINT "Namaste"` (QBASIC) (d) `print("Namaste")` (Python) (e) `printf("Namaste");` (C).

**Solution.**

| Code | Level | Translator needed |
|---|---|---|
| (a) | machine language (low-level) | none |
| (b) | assembly language (low-level) | assembler |
| (c) | high-level (QBASIC) | interpreter (QBASIC) |
| (d) | high-level (Python) | interpreter (Python) |
| (e) | high-level (C) | compiler (for example GCC) |
:::

## 19.2 Language processors: compiler, interpreter and assembler

::: definition Language processor (translator)
A **language processor**, or **translator**, is a program that converts a program written in assembly or a high-level language into machine language. The program the programmer writes is the **source code** (source program); the machine-language result is the **object code** (object program). There are three kinds: the **compiler**, the **interpreter** and the **assembler**.
:::

**Compiler.** A compiler reads the **whole** source program, checks all of it, and translates it **at once** into an object program — on Windows, usually an `.exe` file. If there are errors, it lists them all after it has finished reading, and no object program is made until they are corrected. Once compiled, the program runs on its own, without the compiler, as often as you like, and it runs fast. C, C++ and FORTRAN programs are compiled; GCC (the GNU Compiler Collection) and the compiler in Microsoft Visual Studio are examples.

**Interpreter.** An interpreter takes the source program **one line (statement) at a time**: it translates that line, carries it out at once, and only then moves to the next line. It stops at the **first** error it meets and reports it, which makes errors easy to find and fix — ideal for learning. But no separate object program is made, so the interpreter is needed every time the program runs, and the program runs more slowly. QBASIC and Python are run by interpreters.

**Assembler.** An assembler translates a program in **assembly language** into machine language, one mnemonic at a time into the matching binary instruction.

```figure caption="How a compiler and an interpreter differ. A compiler translates the whole program once and leaves an object program that runs by itself. An interpreter translates and runs one line, then the next, every time the program is run."
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 3.2))
ax.set_xlim(0, 10.4); ax.set_ylim(0, 6.4); ax.axis("off")
def box(x, y, w, h, t, c, fs=8.0, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.14",
                                fc=c, ec="none", alpha=0.92))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", color="white", fontsize=fs,
            fontweight="bold" if bold else "normal", linespacing=1.2)
def arr(p, q):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.3,
                mutation_scale=10, shrinkA=0, shrinkB=0))
ax.text(0.1, 6.05, "Compiler", ha="left", va="center", fontsize=9, fontweight="bold", color=INK)
box(0.1, 4.1, 2.1, 1.45, "source\nprogram\n(all lines)", SERIES[0], fs=7.6)
arr((2.25, 4.82), (2.75, 4.82))
box(2.8, 4.1, 1.9, 1.45, "compiler:\ntranslates\nall at once", SERIES[3], fs=7.6)
arr((4.75, 4.82), (5.25, 4.82))
box(5.3, 4.1, 2.25, 1.45, "object\nprogram\n(.exe file)", SERIES[2], fs=7.6)
arr((7.6, 4.82), (8.1, 4.82))
box(8.15, 4.1, 2.15, 1.45, "runs by\nitself, again\nand again", SERIES[5], fs=7.6)
ax.text(0.1, 2.95, "Interpreter", ha="left", va="center", fontsize=9, fontweight="bold", color=INK)
box(0.1, 0.55, 2.1, 1.95, "source\nprogram:\nline 1,\nline 2, …", SERIES[0], fs=7.6)
arr((2.25, 1.52), (2.75, 1.52))
ax.add_patch(FancyBboxPatch((2.8, 0.55), 5.0, 1.95, boxstyle="round,pad=0,rounding_size=0.14",
                            fc=SERIES[1], ec="none", alpha=0.14))
ax.add_patch(FancyBboxPatch((2.8, 0.55), 5.0, 1.95, boxstyle="round,pad=0,rounding_size=0.14",
                            fc="none", ec=SERIES[1], lw=1.2))
ax.text(5.3, 2.2, "interpreter, for each line in turn:", ha="center", va="center", fontsize=7.6,
        color=SERIES[1], fontweight="bold")
box(3.05, 0.8, 1.9, 1.0, "translate\nthe line", SERIES[1], fs=7.6)
arr((5.0, 1.3), (5.6, 1.3))
box(5.65, 0.8, 1.9, 1.0, "carry it\nout at once", SERIES[1], fs=7.6)
ax.annotate("", xy=(4.0, 0.78), xytext=(6.6, 0.78), arrowprops=dict(arrowstyle="-|>", color=MUTED,
            lw=1.1, mutation_scale=9, connectionstyle="arc3,rad=-0.35"))
arr((7.85, 1.52), (8.35, 1.52))
box(8.4, 0.55, 1.9, 1.95, "output;\nstops at\nthe first\nerror", SERIES[5], fs=7.6)
ax.set_xticks([]); ax.set_yticks([])
```

| Point | Compiler | Interpreter |
|---|---|---|
| How it translates | the whole program at once | one line at a time, running each line straight away |
| Errors | listed together after the whole program is checked | shown one at a time; stops at the first error |
| Object program | made and saved (for example an `.exe` file) | not made |
| Needed to run the program again | no | yes, every time |
| Speed of running | fast | slower |
| Finding mistakes | harder for a beginner | easier, so good for learning |
| Examples | C, C++, FORTRAN compilers; GCC | QBASIC, Python |

```photo id="cs8/prog-devcpp" caption="A five-line C program in the free Dev-C++ editor. Its compiler, GCC, has translated the whole program at once: the Compile Log at the bottom reports 0 errors and 0 warnings and names the object program it made, hello world.exe, which now runs without the compiler." width="92"
```

::: caution A language is not a translator
"Python is an interpreter" and "C is a compiler" are common slips, and one textbook even lists COBOL among compilers. Python, C and COBOL are **languages**. The **Python interpreter** is the program that runs Python code; **GCC** is a program that compiles C code. Write "QBASIC programs are run by an interpreter", not "QBASIC is a compiler".
:::

::: example Worked example 19.2 — compiler or interpreter?
**Problem.** Which translator suits each situation, and why? (a) A grade 8 student is learning to program and wants to see the effect of each line at once. (b) A software company in Lalitpur wants to sell a fast billing program without giving customers its source code. (c) A teacher wants to test a short program again and again after each small change.

**Solution.** (a) **Interpreter** — it runs one line at a time and stops at the first error, so the student sees exactly where things go wrong. (b) **Compiler** — it makes a fast object program (`.exe`) that runs without the compiler, so only the object program need be given to customers. (c) **Interpreter** — there is no separate compiling step, so each change can be run at once.
:::

## 19.3 Syntax errors, logical errors and run-time errors; testing and debugging

An error in a program is called a **bug**. The word was used by engineers long before computers, but it became famous on 9 September 1947, when operators of the Harvard Mark II computer found a moth stuck in one of its relays, taped it into their log book and wrote "First actual case of bug being found."

```photo id="cs8/prog-first-bug" caption="The page of the Harvard Mark II log book for 9 September 1947, with the moth taped to it. The entry at 15:45 reads: Relay #70 Panel F (moth) in relay. First actual case of bug being found." width="70"
```

Program errors are of three kinds.

::: definition Syntax error
A **syntax error** is a mistake in the grammar of the language: a misspelt keyword, a missing bracket or quotation mark, a wrong symbol. The translator cannot understand the line, so it reports the error and the program does not run. Example: `PRIMT "Average ="; AVG` in QBASIC (PRINT misspelt), or `print("Namaste"` in Python (closing bracket missing).
:::

::: definition Run-time error
A **run-time error** (execution error) happens **while the program is running**: the program is grammatically correct, but it is asked to do something impossible, and it stops with an error message. Examples: dividing by zero (QBASIC shows "Division by zero"), finding the square root of a negative number ("Illegal function call"), storing a number too big for its variable ("Overflow"), or opening a file that does not exist.
:::

::: definition Logical error
A **logical error** is a mistake in the method of the program. The program runs to the end without any message, but its **output is wrong**: a wrong formula, a wrong operator, a wrong condition such as `>` where `>=` was meant, or steps in the wrong order. The computer cannot detect a logical error; only testing with known answers can.
:::

| Point | Syntax error | Run-time error | Logical error |
|---|---|---|---|
| What it is | breaking the rules of the language | an impossible operation while running | a mistake in the method |
| When it is found | when the program is translated | while the program runs | when the output is checked |
| Who finds it | the compiler or interpreter | the computer, which stops the program | the programmer, by testing |
| Message shown | yes | yes | none |
| Example | `PRIMT` for `PRINT` | dividing by zero | AVG = A + B / 2 for the average |

::: note The same in Python
Python gives exactly the same kinds of error. These messages were produced by Python 3.12:

```python
print("Namaste"
```

```text
SyntaxError: '(' was never closed
```

```python
total = 500
students = 0
print("Share =", total / students)
```

```text
ZeroDivisionError: division by zero
```
:::

### Testing and debugging

**Testing** means running a program with chosen **test data** — inputs whose correct outputs you have worked out beforehand — and comparing the program's output with them. Good test data includes **normal** values (a mark of 65), **boundary** values (0, 100, and exactly the pass mark), and **wrong** values (a negative mark, or a word where a number is expected), to see whether the program copes.

**Debugging** means finding where an error is and correcting it. Useful ways are:

1. **Read the error message**: it names the error and usually the line.
2. **Dry run** (trace) the program on paper with a trace table, as in Lesson 18.
3. **Print the values** of variables at different points to see where they first go wrong.
4. **Step through** the program one line at a time and watch the variables. In QBASIC, F8 runs one line at a time and F9 sets a **breakpoint**, a line where the program pauses.
5. **Check one part at a time**, and test again after every correction.

::: example Worked example 19.3 — find, name and correct the errors
**Problem.** This QBASIC program should print the average of the marks in English and Maths. Find the errors, name the type of each, and write the corrected program with its output for marks 60 and 80.

```basic
CLS
INPUT "Enter marks in English and Maths: ", E, M
AVG = E + M / 2
PRIMT "Average ="; AVG
END
```

**Solution.** Line 4: `PRIMT` is a misspelling of `PRINT` — a **syntax error**; neither FreeBASIC nor QB64 (two modern QBASIC-compatible compilers) will accept the program. Line 3: the computer divides before it adds, so it works out 60 + 80 ÷ 2 = 60 + 40 = 100 instead of the average 70 — a **logical error**. With only line 4 corrected, the program runs and prints the wrong answer without any warning:

```text
Enter marks in English and Maths: 60, 80
Average = 100
```

The corrected program puts brackets round the sum:

```basic
CLS
INPUT "Enter marks in English and Maths: ", E, M
AVG = (E + M) / 2
PRINT "Average ="; AVG
END
```

```text
Enter marks in English and Maths: 60, 80
Average = 70
```

Check: (60 + 80) ÷ 2 = 140 ÷ 2 = 70 ✓. Only the test with known marks revealed the logical error.
:::

::: tip Naming the error type
In "identify the error" questions, ask yourself two things. Does the program **run at all**? If not, it is a syntax error. If it runs, does it **stop with a message**? Then it is a run-time error. If it finishes but the answer is **wrong**, it is a logical error. Always write the corrected line too: the correction usually carries a mark of its own.
:::

## 19.4 Common high-level languages: QBASIC, Python, C and Java

Hundreds of high-level languages exist. The first to be widely used was **FORTRAN** (FORmula TRANslation), released by John Backus and his team at IBM in 1957 for science and engineering; **COBOL** (COmmon Business-Oriented Language), from 1959, ran the accounts of banks and governments for decades. Four languages matter most to you.

**QBASIC** (Quick Beginner's All-purpose Symbolic Instruction Code). The first BASIC was created by John G. Kemeny and Thomas E. Kurtz at Dartmouth College in the USA; its first program ran on 1 May 1964. Microsoft's QBASIC came with MS-DOS 5.0 in 1991. It is run by an interpreter inside its own simple editor, its keywords are plain English (`PRINT`, `INPUT`, `IF`, `FOR`), and it needs no setting up, so it is still a favourite first language in Nepali schools. Modern free programs such as **QB64** and **FreeBASIC** run QBASIC programs on today's computers.

**Python.** Created by Guido van Rossum in the Netherlands and first released in February 1991. Python code is short and very readable, it uses indentation instead of END words, and it comes with a huge collection of ready-made libraries. It is used for artificial intelligence, data science, websites and automation, and it is the programming language of the CDC grade 9 and 10 course.

**C.** Developed by Dennis Ritchie at Bell Laboratories in the USA in 1972, to write the UNIX operating system. C programs are compiled; they are fast and work closely with the hardware, so C is used for operating systems (much of Linux and Windows), device drivers and the small computers inside machines. C++, an extension of C made by Bjarne Stroustrup, came in 1985.

**Java.** Developed by James Gosling and his team at Sun Microsystems and released in 1995. A Java compiler turns the program into **bytecode**, which the **Java Virtual Machine (JVM)** then runs on any computer — "write once, run anywhere". Java is widely used for Android apps, banking systems and large business software. (JavaScript, the language of web pages, is a different language with a similar name.)

| Language | Released | Created by | How it is translated | Typical use |
|---|---|---|---|---|
| QBASIC | 1991 (BASIC 1964) | Microsoft (BASIC: Kemeny and Kurtz) | interpreter | learning to program |
| Python | 1991 | Guido van Rossum | interpreter | AI, data, web, school courses |
| C | 1972 | Dennis Ritchie, Bell Labs | compiler | operating systems, drivers, devices |
| Java | 1995 | James Gosling, Sun Microsystems | compiler to bytecode, run by the JVM | Android apps, banking, business software |

::: example Worked example 19.4 — one job in four languages
**Problem.** Write a program in QBASIC, Python, C and Java that stores 25 and 17 in two variables and prints their sum.

**Solution.** Each program was run, and each printed the same line, `Sum = 42`.

```basic
A = 25
B = 17
PRINT "Sum ="; A + B
END
```

```python
a = 25
b = 17
print("Sum =", a + b)
```

```c
#include <stdio.h>

int main(void)
{
    int a = 25, b = 17;
    printf("Sum = %d\n", a + b);
    return 0;
}
```

```java
public class Sum {
    public static void main(String[] args) {
        int a = 25, b = 17;
        System.out.println("Sum = " + (a + b));
    }
}
```

```text
Sum = 42
```

The QBASIC and Python versions are the shortest. C and Java need more lines because the program must be placed inside a `main` function and each variable's type (`int`) must be declared first.
:::

## 19.5 Constants, variables and data types

Every program works with **data**: numbers such as marks, prices and ages, and text such as names and addresses. A program stores data in two ways, as constants and as variables.

::: definition Constant
A **constant** is a value that does not change while the program runs. A **numeric constant** is a number, such as `45`, `-7.5` or `3.2E+4` (which means 3.2 × 10⁴ = 32,000). A **string constant** is any group of characters inside double quotation marks, such as `"Kathmandu"`, `"9841234567"` or `"2081"`. A constant can also be given a name: in QBASIC, `CONST PI = 3.14159` makes PI a **symbolic constant**.
:::

::: definition Variable
A **variable** is a name given to a location in the computer's memory, where a value is stored. The value can change while the program runs, but the variable holds only **one value at a time**: storing a new value replaces the old one. In QBASIC, `LET A = 5` (or simply `A = 5`) stores 5 in the variable A.
:::

```figure caption="Variables are named boxes in memory. Each assignment puts a value into a box and wipes out whatever was there; the right-hand side is worked out first, so A = A + B uses the old A (5) to make the new A (8)."
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 2.9))
ax.set_xlim(0, 10.4); ax.set_ylim(-0.15, 5.3); ax.axis("off")
steps = ["A = 5", "B = 3", "A = A + B", "N\\$ = \"Ram\""]
state = [{"A": "5"}, {"A": "5", "B": "3"}, {"A": "8", "B": "3"}, {"A": "8", "B": "3", "N\\$": "\"Ram\""}]
names = ["A", "B", "N\\$"]
for i, (st, mem) in enumerate(zip(steps, state)):
    x0 = 0.15 + i * 2.6
    ax.add_patch(FancyBboxPatch((x0, 4.15), 2.3, 0.75, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=SERIES[0], ec="none"))
    ax.text(x0 + 1.15, 4.52, st, ha="center", va="center", color="white", fontsize=8.4,
            family="monospace", fontweight="bold")
    ax.text(x0 + 1.15, 3.7, f"after statement {i + 1}", ha="center", va="center", fontsize=7.2, color=MUTED)
    for j, nm in enumerate(names):
        y = 2.75 - j * 1.2
        filled = nm in mem
        ax.add_patch(FancyBboxPatch((x0 + 0.85, y - 0.36), 1.3, 0.72, boxstyle="round,pad=0,rounding_size=0.06",
                                    fc="#eef4fb" if filled else "white", ec=ACCENT if filled else GRID, lw=1.2))
        ax.text(x0 + 0.65, y, nm, ha="right", va="center", fontsize=8.2, color=INK if filled else MUTED,
                family="monospace")
        if filled:
            changed = (i == 2 and nm == "A")
            ax.text(x0 + 1.5, y, mem[nm], ha="center", va="center", fontsize=8.6, family="monospace",
                    color=SERIES[1] if changed else INK, fontweight="bold" if changed else "normal")
    if i < 3:
        ax.annotate("", xy=(x0 + 2.55, 4.52), xytext=(x0 + 2.33, 4.52),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1, mutation_scale=8))
ax.text(0.15 + 2 * 2.6 + 1.5, 2.13, "(was 5)", ha="center", va="center", fontsize=7.0, color=SERIES[1])
ax.set_xticks([]); ax.set_yticks([])
```

| Constant | Variable |
|---|---|
| a fixed value | a named memory location whose value can change |
| its value never changes while the program runs | its value can be changed by assignment or input |
| examples: `25`, `3.14`, `"Nepal"` | examples: `A`, `AGE`, `N$` |

::: caution "A = A + 1" is not an equation
In mathematics A = A + 1 is impossible. In a program, `=` means **"work out the right-hand side, then store it in the variable on the left"**. So `A = A + 1` adds 1 to the old value of A — the update step of every counter in Lesson 18. For the same reason `5 = A` is wrong: the left side must always be a variable.
:::

### Rules for naming variables in QBASIC

1. A name must **begin with a letter** (A to Z).
2. It may contain **letters, digits and the full stop (period)**, up to **40 characters**.
3. **No spaces** and no other symbols are allowed, except one type symbol (`%`, `&`, `!`, `#` or `$`) at the end.
4. A **keyword** (reserved word) such as `PRINT`, `INPUT` or `END` cannot be a variable name.
5. Capital and small letters are the same in QBASIC: `age`, `Age` and `AGE` are one variable. (In Python they are three different variables.)

Choose **meaningful** names — `TOTAL`, `PRICE`, `NAME$` — rather than single letters, so that the program explains itself. Python's rules are similar: a name starts with a letter or underscore, may contain letters, digits and underscores, cannot be a keyword, and is case-sensitive.

::: example Worked example 19.5 — valid or invalid?
**Problem.** Which of these are valid QBASIC variable names? Give a reason for each invalid one: `AGE`, `2NDNAME`, `FIRST NAME`, `N$`, `PRINT`, `TOTAL.MARKS`, `ROLL-NO`, `PRICE%`.

**Solution.** Valid: `AGE`, `N$` (a string variable), `TOTAL.MARKS` (a full stop is allowed), `PRICE%` (an integer variable). Invalid: `2NDNAME` begins with a digit; `FIRST NAME` contains a space; `PRINT` is a keyword; `ROLL-NO` contains a hyphen, which QBASIC reads as a minus sign.
:::

### Data types

The **data type** of a value tells the computer what kind of data it is, how much memory to give it and what can be done with it. The two basic kinds are **numeric** data, used in calculations, and **string** (character) data, which is text: letters, digits and symbols treated as characters, not as amounts. In QBASIC the type of a variable is shown by a **symbol at the end of its name**; a name with no symbol is SINGLE.

| QBASIC type | Symbol | Memory | Values it can hold | Example |
|---|---|---|---|---|
| INTEGER | `%` | 2 bytes | whole numbers from −32,768 to 32,767 | `AGE% = 14` |
| LONG (long integer) | `&` | 4 bytes | whole numbers from −2,147,483,648 to 2,147,483,647 | `POP& = 29164578` |
| SINGLE (default) | `!` or none | 4 bytes | numbers with decimals, about 7 significant digits | `HEIGHT! = 1.52` |
| DOUBLE | `#` | 8 bytes | numbers with decimals, about 15 to 16 significant digits | `PI# = 3.14159265358979` |
| STRING | `$` | 1 byte per character | text of up to 32,767 characters | `N$ = "Sita"` |

::: example Worked example 19.6 — variables of different types
**Problem.** Write a QBASIC program that stores a student's name, age and height, and the population of Nepal from the 2021 census (29,164,578), in variables of suitable types, and prints them.

**Solution.**

```basic
CLS
REM Variables of different data types
N$ = "Sita Thapa"
AGE% = 14
HEIGHT! = 1.52
POP& = 29164578
PRINT N$; " is"; AGE%; "years old and"; HEIGHT!; "m tall."
PRINT "Population of Nepal, census 2021:"; POP&
END
```

```text
Sita Thapa is 14 years old and 1.52 m tall.
Population of Nepal, census 2021: 29164578
```

The population needs LONG, because it is far larger than 32,767, the biggest INTEGER. Notice the spaces in the output: QBASIC prints every number with a space in front (where a minus sign would go) and a space after it, so `" is"; AGE%; "years"` comes out as "is 14 years".
:::

::: note The same in Python
Python works out the type from the value itself, and `type()` shows it. It has a fourth basic type, **bool**, for True and False.

```python
name = "Sita Thapa"
age = 14
height = 1.52
population = 29164578
is_student = True
print(name, "is", age, "years old and", height, "m tall.")
print(type(name), type(age), type(height), type(is_student))
```

```text
Sita Thapa is 14 years old and 1.52 m tall.
<class 'str'> <class 'int'> <class 'float'> <class 'bool'>
```
:::

::: example Worked example 19.7 — choosing a data type
**Problem.** Choose a QBASIC data type for each: (a) the number of students in a class; (b) the price of 1 kg of rice, Rs 85.50; (c) the name of a district; (d) a mobile number, 9841234567; (e) the number of people in Kathmandu district.

**Solution.** (a) **INTEGER** (`%`) — a small whole number. (b) **SINGLE** (`!`) — it has decimals. (c) **STRING** (`$`) — text. (d) **STRING** (`$`) — no arithmetic is ever done with a phone number, and as a number it is too big even for LONG (whose largest value is 2,147,483,647). (e) **LONG** (`&`) — a whole number of about two million, too big for INTEGER.
:::

::: note Activity 19.1 — meet the translators
In the computer lab, open QB64 (or QBASIC, if your lab has it) and Python's IDLE. (1) Type `PRINT 7 * 6` in QB64's editor and `print(7 * 6)` at IDLE's `>>>` prompt, and run both. (2) Misspell the keyword in each and note the exact error message. (3) Make each program divide by zero and note the message. (4) Make a three-column table — language, translator, message — for your notebook, and label each message as a syntax or run-time error.
:::

## Chapter summary

- A **programming language** is a set of words, symbols and rules (syntax) for writing instructions for a computer.
- **Low-level** languages: **machine language** (binary; runs directly; machine-dependent) and **assembly language** (mnemonics such as MOV and ADD; needs an assembler). **High-level** languages (QBASIC, Python, C, Java) are English-like and portable.
- **Language processors** turn source code into object code: a **compiler** translates the whole program at once and makes an object program; an **interpreter** translates and runs one line at a time; an **assembler** translates assembly language.
- **Syntax error**: breaking the rules of the language. **Run-time error**: an impossible operation while running, such as division by zero. **Logical error**: wrong method, wrong output, no message.
- **Testing** runs a program with test data of known answers; **debugging** finds and corrects errors (error messages, dry runs, printing values, stepping with F8, breakpoints with F9).
- **QBASIC** (Microsoft, 1991; BASIC 1964), **Python** (Guido van Rossum, 1991), **C** (Dennis Ritchie, 1972), **Java** (James Gosling, Sun, 1995).
- A **constant** never changes (numeric or string); a **variable** is a named memory location whose value can change; QBASIC names begin with a letter, have no spaces and are not keywords.
- QBASIC data types: INTEGER `%`, LONG `&`, SINGLE `!` (the default), DOUBLE `#`, STRING `$`.

## Practice questions

**Group A — Objective (1 mark each)**

1. Machine language is written using <span class="marks">[1]</span>
   (a) English words (b) mnemonics (c) 0s and 1s (d) flowchart symbols
2. The translator that converts assembly language into machine language is <span class="marks">[1]</span>
   (a) a compiler (b) an interpreter (c) an assembler (d) an editor
3. Which translator converts the whole program at once and makes an object program? <span class="marks">[1]</span>
   (a) interpreter (b) compiler (c) assembler (d) debugger
4. QBASIC programs are run by <span class="marks">[1]</span>
   (a) an assembler (b) an interpreter (c) an operating system (d) a modem
5. Which of these is a low-level language? <span class="marks">[1]</span>
   (a) Python (b) Java (c) assembly language (d) QBASIC
6. Dividing a number by zero while a program is running causes <span class="marks">[1]</span>
   (a) a syntax error (b) a logical error (c) a run-time error (d) no error
7. A program runs to the end but prints a wrong answer because of a wrong formula. This is <span class="marks">[1]</span>
   (a) a syntax error (b) a logical error (c) a run-time error (d) a hardware fault
8. Python was created by <span class="marks">[1]</span>
   (a) Dennis Ritchie (b) James Gosling (c) Guido van Rossum (d) John Kemeny
9. In QBASIC, the symbol that marks a string variable is <span class="marks">[1]</span>
   (a) `%` (b) `&` (c) `!` (d) `$`
10. Which is a valid QBASIC variable name? <span class="marks">[1]</span>
    (a) 1STNAME (b) FIRST NAME (c) TOTAL.MARKS (d) PRINT
11. The range of an INTEGER variable in QBASIC is <span class="marks">[1]</span>
    (a) 0 to 255 (b) −32,768 to 32,767 (c) −2,147,483,648 to 2,147,483,647 (d) unlimited
12. A program written by a programmer in a high-level language is called <span class="marks">[1]</span>
    (a) object code (b) source code (c) machine code (d) bytecode

::: note Answers to Group A
**1.** (c) — machine language is binary.
**2.** (c) — an assembler translates mnemonics into machine code.
**3.** (b) — a compiler translates everything at once.
**4.** (b) — QBASIC is an interpreter, running one line at a time.
**5.** (c) — assembly language is close to the machine; the others are high-level.
**6.** (c) — the error appears only while the program runs.
**7.** (b) — the program runs, but the method is wrong.
**8.** (c) — Guido van Rossum, 1991.
**9.** (d) — `$` marks a string, as in `N$`.
**10.** (c) — a full stop is allowed; the others start with a digit, contain a space or are a keyword.
**11.** (b) — INTEGER uses 2 bytes.
**12.** (b) — the translator turns source code into object code.
:::

**Group B — Short answer (2 marks each)**

1. Write any two differences between a low-level and a high-level language. <span class="marks">[2]</span>
2. What is a language processor? Name its three types. <span class="marks">[2]</span>
3. Write any two differences between a compiler and an interpreter. <span class="marks">[2]</span>
4. What is assembly language? Why does it need an assembler? <span class="marks">[2]</span>
5. Define syntax error and logical error with one example each. <span class="marks">[2]</span>
6. What is a run-time error? Give two examples. <span class="marks">[2]</span>
7. What is debugging? Write any two ways of debugging a program. <span class="marks">[2]</span>
8. Define constant and variable with one example of each. <span class="marks">[2]</span>
9. Write any four rules for naming a variable in QBASIC. <span class="marks">[2]</span>
10. Name the five data types of QBASIC with their type symbols. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A low-level language (machine or assembly) is close to the hardware and machine-dependent, while a high-level language uses English-like words and is portable. Low-level programs are hard to write and correct but run very fast; high-level programs are easy to write and correct but must be translated by a compiler or interpreter.

**2.** A language processor (translator) is a program that converts a program written in assembly or a high-level language into machine language. Its three types are the compiler, the interpreter and the assembler.

**3.** A compiler translates the whole program at once, while an interpreter translates and runs one line at a time. A compiler makes an object program that runs without it, while an interpreter makes no object program and is needed every time. (Also: a compiler lists all errors after checking the whole program; an interpreter stops at the first error.)

**4.** Assembly language is a low-level language that uses short words called mnemonics (such as MOV, ADD, SUB) in place of binary instructions. The processor understands only machine language, so an assembler must translate the mnemonics into binary before the program can run.

**5.** A syntax error breaks the grammar rules of the language, for example `PRIMT "Hello"` instead of `PRINT "Hello"`. A logical error is a mistake in the method, so the program runs but gives a wrong result, for example `AVG = A + B / 2` instead of `AVG = (A + B) / 2`.

**6.** A run-time error is an error that occurs while the program is running, when it is asked to do something impossible, and it stops the program with a message. Examples: dividing a number by zero; the square root of a negative number; storing a number too large for its variable (overflow).

**7.** Debugging is the process of finding and correcting the errors (bugs) in a program. Any two ways: reading the error messages; dry running the program with a trace table; printing the values of variables at different points; stepping through it line by line (F8 in QBASIC) or using breakpoints (F9).

**8.** A constant is a value that does not change while the program runs, for example `25` or `"Nepal"`. A variable is a named memory location whose value can change while the program runs, for example `AGE` in `AGE = 14`.

**9.** Any four: it must begin with a letter; it may contain letters, digits and a full stop; it may be up to 40 characters long; it must not contain spaces or other symbols except a type symbol at the end; it must not be a keyword such as PRINT or END.

**10.** INTEGER (`%`), LONG (`&`), SINGLE (`!`, the default when no symbol is used), DOUBLE (`#`) and STRING (`$`).
:::

**Group C — Long answer (4 marks each)**

1. What is a programming language? Explain machine language, assembly language and high-level language, giving one advantage and one disadvantage of each. <span class="marks">[1+3]</span>
2. Explain compiler, interpreter and assembler. Which translator is used for QBASIC programs and which for C programs? <span class="marks">[3+1]</span>
3. What are testing and debugging? Explain the three types of programming error with one example each. <span class="marks">[1+3]</span>
4. Write short notes on any two of these languages: QBASIC, Python, C, Java. <span class="marks">[2+2]</span>
5. Study the program below. Find the errors, name the type of each, and write the correct program and its output when the length is 12 and the breadth is 5. <span class="marks">[4]</span>

```basic
CLS
INPUT "Enter length and breadth: ", L, B
A = L + B
PRINT "Area ="; A
P = 2 * L + B
PRNT "Perimeter ="; P
END
```

::: note Answers to Group C
**1.** A programming language is a set of words, symbols and rules used to write instructions for a computer (1 mark). *Machine language*: written in 0s and 1s; advantage — runs directly and fastest, needs no translation; disadvantage — very hard to write and correct, and machine-dependent. *Assembly language*: uses mnemonics such as MOV and ADD; advantage — easier than binary while still fast; disadvantage — machine-dependent and needs an assembler. *High-level language*: English-like statements, such as QBASIC and Python; advantage — easy to write, read and correct, and portable; disadvantage — must be translated by a compiler or interpreter and runs a little slower.

**2.** A *compiler* translates the whole high-level program at once into an object program (such as an `.exe` file), lists all errors after checking, and the object program then runs fast without the compiler. An *interpreter* translates and carries out one line at a time, stops at the first error, makes no object program and is needed every time the program runs. An *assembler* translates assembly-language mnemonics into machine code (3 marks). QBASIC programs are run by an **interpreter**; C programs are translated by a **compiler** such as GCC (1 mark).

**3.** Testing is running a program with test data whose correct results are known and comparing the outputs; debugging is finding and correcting the errors (1 mark). *Syntax error*: breaking the rules of the language, found by the translator, e.g. `PRIMT` for `PRINT`. *Run-time error*: an impossible operation while the program runs, which stops it with a message, e.g. dividing by zero. *Logical error*: a wrong method; the program runs but gives wrong output and no message, e.g. `AVG = A + B / 2` (3 marks).

**4.** Any two, about four points each. *QBASIC*: Microsoft, 1991, based on BASIC (Kemeny and Kurtz, Dartmouth College, 1964); run by an interpreter in its own editor; English-like keywords; used for learning. *Python*: Guido van Rossum, 1991; very readable, uses indentation; interpreted; large libraries; used in AI, data science and the web, and in the CDC grade 9–10 course. *C*: Dennis Ritchie, Bell Labs, 1972; compiled, fast, close to the hardware; used for operating systems and device programs. *Java*: James Gosling, Sun Microsystems, 1995; compiled to bytecode run by the Java Virtual Machine, so programs run on any computer; used for Android apps and business software.

**5.** Line 3 `A = L + B` is a **logical error** — area is length × breadth. Line 5 `P = 2 * L + B` is a **logical error** — perimeter is 2 × (length + breadth), so brackets are needed. Line 6 `PRNT` is a **syntax error** — the keyword is PRINT. Corrected program:

```basic
CLS
INPUT "Enter length and breadth: ", L, B
A = L * B
PRINT "Area ="; A
P = 2 * (L + B)
PRINT "Perimeter ="; P
END
```

```text
Enter length and breadth: 12, 5
Area = 60
Perimeter = 34
```

Check: 12 × 5 = 60 and 2 × (12 + 5) = 34 ✓.
:::
