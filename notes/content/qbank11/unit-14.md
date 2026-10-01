---
subject: Question Bank
grade: 11
unit: 14
title: "Computer Science: Unit-wise Objective Question Bank"
hours: 0
area: Computer Science
---

Group A of the Grade 11 Computer Science paper is nine marks of multiple-choice items, one mark each. The paper is 2 hours and 50 marks, so nine marks is almost a fifth of it, and it is the part where a student who has read the book once can still score full marks in about ten minutes. Nothing is lost by a wrong answer, so never leave a bubble empty.

This chapter gives practice MCQs for all eight units of the Grade 11 syllabus, with an answer key and a one-line reason for every item, followed by a short study of how wrong options are built. The items test exactly what the matching chapter of the Computer Science textbook teaches.

::: caution About the labels in this chapter
Every item here is an **original practice item** written to the pattern and difficulty of a Group A question. None is claimed to be a question from a particular year's paper. A book that prints a board year beside every MCQ is usually guessing, and a wrong label teaches you to trust the wrong thing. Where a program is shown, its output was checked by compiling and running it.
:::

## 14.1 How the nine marks are spread

The syllabus carries 80 theory hours, and the weighting by unit is a better guide to the nine marks than any rumour about "important" topics.

| Unit | Hours | Share of 9 marks (approx.) | What the MCQs usually test |
|---|---|---|---|
| 1. Computer System | 20 | 2 | memory types, buses, input/output devices, units |
| 2. Number System and Boolean Logic | 11 | 1 to 2 | conversions, complements, gates, laws |
| 3. Software and Operating System | 12 | 1 | OS terms, software types, Linux and mobile OS |
| 4. Application Package | 5 | 0 to 1 | which package does which job |
| 5. Programming Concepts and Logics | 8 | 2 | C operators, loop output, errors, ASCII |
| 6. Web Technology I | 8 | 1 | tags, attributes, CSS types |
| 7. Multimedia | 6 | 0 to 1 | components, file types |
| 8. Information Security and Cyber Law | 10 | 1 | malware, cybercrime, IPR, cyber law |

```figure caption="Teaching hours of the eight Grade 11 units. Units 1, 3 and 2 together carry 43 of the 80 hours, but Unit 5 supplies most of the questions that need working out."
import numpy as np, matplotlib.pyplot as plt
units = ["1 System", "2 Number/Logic", "3 Software/OS", "4 Packages", "5 Programming", "6 Web I", "7 Multimedia", "8 Security"]
hours = [20, 11, 12, 5, 8, 8, 6, 10]
y = np.arange(len(units))[::-1]
fig, ax = plt.subplots(figsize=(4.8, 2.9))
ax.barh(y, hours, height=0.6, color=ACCENT)
for yi, h in zip(y, hours):
    ax.text(h + 0.3, yi, str(h), va="center", ha="left", fontsize=8, color=INK)
ax.set_yticks(y); ax.set_yticklabels(units, fontsize=8)
ax.set_xlim(0, 23)
ax.set_xlabel("Syllabus hours (theory)", fontsize=8)
ax.tick_params(labelsize=8, length=0)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.xaxis.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

::: tip The ten-minute method
Do the nine MCQs first, in order, and spend no more than a minute on any. For output questions, write the values of the variables on the margin line by line; do not do the program in your head. For concept questions, eliminate the two options that are plainly wrong, then choose between the remaining two by asking which word in the stem decides it (*volatile*, *bidirectional*, *universal*, *closing tag*).
:::

## 14.2 Unit 1: Computer System

1. The first generation of computers used <span class="marks">[1]</span>
   (a) transistors (b) vacuum tubes (c) integrated circuits (d) microprocessors
2. The Intel 4004, which began the fourth generation, was a <span class="marks">[1]</span>
   (a) microprocessor (b) transistor (c) vacuum tube (d) hard disk
3. The speed of a supercomputer is usually measured in <span class="marks">[1]</span>
   (a) MIPS (b) FLOPS (c) bits (d) bytes
4. How many bytes are there in 2 KB? <span class="marks">[1]</span>
   (a) 1000 (b) 2000 (c) 2048 (d) 1024
5. Which of the following is the fastest memory in a computer? <span class="marks">[1]</span>
   (a) hard disk (b) RAM (c) cache memory (d) DVD
6. Which memory loses its contents when the power is switched off? <span class="marks">[1]</span>
   (a) ROM (b) RAM (c) EPROM (d) flash BIOS chip
7. Which bus is unidirectional, carrying the location of the memory cell to be read or written? <span class="marks">[1]</span>
   (a) data bus (b) control bus (c) address bus (d) expansion bus
8. The unit of the microprocessor that performs arithmetic and logical operations is the <span class="marks">[1]</span>
   (a) control unit (b) ALU (c) register (d) cache
9. Which device reads the pencil-filled bubbles on an objective answer sheet? <span class="marks">[1]</span>
   (a) OCR (b) OMR (c) MICR (d) BCR
10. The special ink characters printed on the bottom of a bank cheque are read by <span class="marks">[1]</span>
    (a) MICR (b) OMR (c) light pen (d) scanner
11. Which printer forms characters by striking an inked ribbon with pins? <span class="marks">[1]</span>
    (a) inkjet printer (b) laser printer (c) dot matrix printer (d) thermal plotter
12. Which port carries both digital video and audio in a single cable? <span class="marks">[1]</span>
    (a) parallel port (b) serial port (c) HDMI (d) PS/2
13. Which of the following is a mobile computing device? <span class="marks">[1]</span>
    (a) mainframe (b) smartphone (c) desktop tower (d) minicomputer
14. The number of bits a CPU can process at one time is called its <span class="marks">[1]</span>
    (a) clock speed (b) word length (c) bus width (d) cache size
15. PROM, EPROM and EEPROM are types of <span class="marks">[1]</span>
    (a) RAM (b) ROM (c) cache (d) buffer
16. Which of these is a secondary storage device? <span class="marks">[1]</span>
    (a) register (b) cache (c) hard disk (d) ROM

::: note Answers to Unit 1
**1.** (b) — first generation (1940 to 1956) used vacuum tubes.
**2.** (a) — the 4004 (1971) was the first single-chip microprocessor.
**3.** (b) — supercomputers are rated in FLOPS (floating-point operations per second); MIPS suits ordinary processors.
**4.** (c) — 1 KB = 1024 bytes, so 2 KB = 2048 bytes.
**5.** (c) — cache sits between the CPU and RAM and is faster than RAM.
**6.** (b) — RAM is volatile; ROM and flash keep their data.
**7.** (c) — the address bus is one-way, from the CPU to memory; the data bus is two-way.
**8.** (b) — the ALU does arithmetic and logic; the control unit directs operations.
**9.** (b) — Optical Mark Recognition senses marks; OCR reads printed characters.
**10.** (a) — Magnetic Ink Character Recognition is used on cheques.
**11.** (c) — dot matrix is an impact printer with a print head of pins.
**12.** (c) — HDMI carries digital video and audio together.
**13.** (b) — a smartphone is portable and connects wirelessly; the others are fixed machines.
**14.** (b) — word length is the number of bits processed in one operation (for example 64).
**15.** (b) — all three are programmable forms of read-only memory.
**16.** (c) — secondary storage is permanent and outside the CPU; the hard disk is the only one listed.
:::

## 14.3 Unit 2: Number System and Boolean Logic

1. The decimal value of the binary number $(1101)_2$ is <span class="marks">[1]</span>
   (a) 11 (b) 12 (c) 13 (d) 14
2. The binary equivalent of the decimal number 25 is <span class="marks">[1]</span>
   (a) 10011 (b) 11001 (c) 11010 (d) 10101
3. The decimal value of the hexadecimal number $(2F)_{16}$ is <span class="marks">[1]</span>
   (a) 37 (b) 45 (c) 47 (d) 51
4. The octal number $(17)_8$ is equal to the decimal number <span class="marks">[1]</span>
   (a) 15 (b) 16 (c) 17 (d) 7
5. $(101)_2 + (11)_2$ equals <span class="marks">[1]</span>
   (a) $(110)_2$ (b) $(111)_2$ (c) $(1000)_2$ (d) $(1001)_2$
6. The 1's complement of $1010$ is <span class="marks">[1]</span>
   (a) 0101 (b) 0110 (c) 1011 (d) 1111
7. The 2's complement of $0101$ (4 bits) is <span class="marks">[1]</span>
   (a) 1010 (b) 1011 (c) 1001 (d) 0110
8. Which gate gives output 1 only when both inputs are 1? <span class="marks">[1]</span>
   (a) OR (b) AND (c) NAND (d) XOR
9. Which gate gives output 1 only when its two inputs are different? <span class="marks">[1]</span>
   (a) XNOR (b) NOR (c) XOR (d) AND
10. Which of the following gates is called a universal gate? <span class="marks">[1]</span>
    (a) AND (b) OR (c) NAND (d) XOR
11. According to Boolean algebra, $A + A'$ is equal to <span class="marks">[1]</span>
    (a) 0 (b) 1 (c) $A$ (d) $A'$
12. $A \cdot 0$ is equal to <span class="marks">[1]</span>
    (a) $A$ (b) 1 (c) 0 (d) $A'$
13. By De Morgan's theorem, $(A + B)'$ equals <span class="marks">[1]</span>
    (a) $A' + B'$ (b) $A' \cdot B'$ (c) $A \cdot B$ (d) $A + B'$
14. The number of rows in the truth table of a Boolean function of three variables is <span class="marks">[1]</span>
    (a) 3 (b) 6 (c) 8 (d) 9
15. In the hexadecimal system, the symbol E represents the decimal value <span class="marks">[1]</span>
    (a) 13 (b) 14 (c) 15 (d) 16

::: note Answers to Unit 2
**1.** (c) — $8 + 4 + 0 + 1 = 13$.
**2.** (b) — $25 = 16 + 8 + 1 = 11001$.
**3.** (c) — $2 \times 16 + 15 = 47$.
**4.** (a) — $1 \times 8 + 7 = 15$.
**5.** (c) — $5 + 3 = 8 = 1000$ in binary.
**6.** (a) — flip every bit: 1010 becomes 0101.
**7.** (b) — 1's complement 1010, add 1 gives 1011.
**8.** (b) — AND outputs 1 only for (1, 1); NAND is its inverse.
**9.** (c) — XOR is 1 when inputs differ; XNOR is 1 when they are equal.
**10.** (c) — NAND (and NOR) can build every other gate.
**11.** (b) — the complement law: $A + A' = 1$.
**12.** (c) — the null law: anything ANDed with 0 is 0.
**13.** (b) — De Morgan: complement of an OR is the AND of the complements.
**14.** (c) — $2^3 = 8$ combinations.
**15.** (b) — A=10, B=11, C=12, D=13, E=14, F=15.
:::

## 14.4 Unit 3: Computer Software and Operating System

1. Which of the following is system software? <span class="marks">[1]</span>
   (a) word processor (b) operating system (c) web browser (d) spreadsheet
2. A program that scans a computer for viruses and removes them is <span class="marks">[1]</span>
   (a) utility software (b) application software (c) an assembler (d) a compiler
3. An operating system that keeps several programs in main memory and switches the CPU among them is called <span class="marks">[1]</span>
   (a) multiprogramming (b) single-user (c) batch only (d) real-time only
4. A computer with more than one CPU working together is a <span class="marks">[1]</span>
   (a) multiprocessing system (b) single-tasking system (c) embedded system (d) time-sharing terminal
5. Which of the following is an open-source operating system? <span class="marks">[1]</span>
   (a) Windows 11 (b) macOS (c) Linux (d) iOS
6. Ubuntu, Fedora and Debian are examples of <span class="marks">[1]</span>
   (a) Linux distributions (b) UNIX shells (c) mobile operating systems (d) antivirus programs
7. Which of the following is a mobile operating system? <span class="marks">[1]</span>
   (a) Android (b) Ubuntu (c) MS-DOS (d) Solaris
8. Which of the following is NOT a function of an operating system? <span class="marks">[1]</span>
   (a) memory management (b) file management (c) designing web pages (d) device management
9. In Windows, which tool is used to browse, copy, move and delete files and folders? <span class="marks">[1]</span>
   (a) File Explorer (b) Notepad (c) Paint (d) Calculator
10. The kernel of Linux was first written by <span class="marks">[1]</span>
    (a) Bill Gates (b) Dennis Ritchie (c) Linus Torvalds (d) Steve Jobs
11. A system in which many computers connected by a network work together as one is called a <span class="marks">[1]</span>
    (a) distributed system (b) standalone system (c) batch system (d) palmtop
12. Software that is downloaded and run through a web browser, without installing it, is called <span class="marks">[1]</span>
    (a) utility software (b) web-based application (c) system software (d) firmware

::: note Answers to Unit 3
**1.** (b) — the OS manages the machine itself; the others serve users' tasks.
**2.** (a) — antivirus is a utility program that maintains the system.
**3.** (a) — multiprogramming keeps many jobs in memory so the CPU is never idle.
**4.** (a) — two or more CPUs sharing the load is multiprocessing.
**5.** (c) — Linux source code is freely available; the others are proprietary.
**6.** (a) — each is a packaged version of the Linux kernel with its own tools.
**7.** (a) — Android is a mobile OS; Ubuntu and Solaris are desktop or server systems.
**8.** (c) — designing pages is the job of application tools, not of the OS.
**9.** (a) — File Explorer manages files and folders.
**10.** (c) — Linus Torvalds began the Linux kernel in 1991.
**11.** (a) — a distributed OS makes networked machines act as one system.
**12.** (b) — web-based applications run on a server and are used through a browser.
:::

## 14.5 Unit 4: Application Package

1. Which package is used to prepare a letter or a report? <span class="marks">[1]</span>
   (a) spreadsheet (b) word processor (c) DBMS (d) presentation tool
2. Which package is best for calculating and analysing marks in rows and columns, with formulas and charts? <span class="marks">[1]</span>
   (a) spreadsheet (b) word processor (c) browser (d) compiler
3. Microsoft PowerPoint is an example of a <span class="marks">[1]</span>
   (a) presentation tool (b) spreadsheet (c) DBMS (d) operating system
4. Microsoft Access is an example of a <span class="marks">[1]</span>
   (a) word processor (b) spreadsheet (c) database management system (d) web browser
5. Software that keeps the stock, purchases and sales records of a shop is a <span class="marks">[1]</span>
   (a) payroll system (b) weather forecasting system (c) inventory management system (d) hotel management system
6. Software that calculates salary, tax and allowances of employees is a <span class="marks">[1]</span>
   (a) payroll system (b) school management system (c) inventory system (d) hotel system

::: note Answers to Unit 4
**1.** (b) — Word, Writer and similar programs create text documents.
**2.** (a) — a spreadsheet has cells, formulas and charts.
**3.** (a) — PowerPoint builds slides.
**4.** (c) — Access stores data in related tables and runs queries.
**5.** (c) — inventory systems track stock in and out.
**6.** (a) — a payroll system computes pay, deductions and payslips.
:::

## 14.6 Unit 5: Programming Concepts and Logics

These items include output questions. Each program was compiled and run with gcc; the stated answer is the output.

1. A translator that converts the whole source program into machine code before execution is a <span class="marks">[1]</span>
   (a) compiler (b) interpreter (c) assembler (d) editor
2. A translator that converts assembly language into machine language is <span class="marks">[1]</span>
   (a) an assembler (b) a compiler (c) an interpreter (d) a linker
3. An error caused by wrongly written program statements, such as a missing semicolon, is a <span class="marks">[1]</span>
   (a) syntax error (b) runtime error (c) logical error (d) semantic error
4. Division by zero during execution is an example of a <span class="marks">[1]</span>
   (a) syntax error (b) runtime error (c) compile-time error (d) typing error
5. The ASCII code of the capital letter `A` is <span class="marks">[1]</span>
   (a) 48 (b) 65 (c) 97 (d) 66
6. Which code can represent the characters of all the languages of the world? <span class="marks">[1]</span>
   (a) ASCII (b) BCD (c) Unicode (d) absolute binary
7. Which header file must be included to use `printf()` and `scanf()`? <span class="marks">[1]</span>
   (a) `conio.h` (b) `stdio.h` (c) `string.h` (d) `math.h`
8. What is the output of `printf("%d", 7 / 2);`? <span class="marks">[1]</span>
   (a) 3.5 (b) 4 (c) 3 (d) 3.0
9. What is the output of `printf("%d", 17 % 5);`? <span class="marks">[1]</span>
   (a) 3 (b) 2 (c) 3.4 (d) 5
10. What are the values of `x` and `y` after `int x = 5; int y = x++;`? <span class="marks">[1]</span>
    (a) x = 5, y = 5 (b) x = 6, y = 5 (c) x = 6, y = 6 (d) x = 5, y = 6
11. What is printed by `int a = 4; a *= 3 + 2; printf("%d", a);`? <span class="marks">[1]</span>
    (a) 14 (b) 20 (c) 12 (d) 10
12. What is the output of `printf("%d", 5 > 3 && 2 > 4);`? <span class="marks">[1]</span>
    (a) 1 (b) 0 (c) 5 (d) 2
13. What is the output of `int i, s = 0; for (i = 1; i <= 4; i++) s += i; printf("%d", s);`? <span class="marks">[1]</span>
    (a) 4 (b) 6 (c) 10 (d) 24
14. How many times is the loop body executed: `int i = 5; do { i--; } while (i > 7);`? <span class="marks">[1]</span>
    (a) 0 (b) 1 (c) 2 (d) infinite
15. What is printed by `int n = 2; switch (n) { case 1: printf("A"); case 2: printf("B"); case 3: printf("C"); break; default: printf("D"); }`? <span class="marks">[1]</span>
    (a) B (b) BC (c) BCD (d) ABC
16. What is the output of `int a[5] = {2, 4, 6, 8, 10}; printf("%d", a[1] + a[3]);`? <span class="marks">[1]</span>
    (a) 6 (b) 10 (c) 12 (d) 14
17. What is the output of `printf("%d", strlen("NEPAL"));`? <span class="marks">[1]</span>
    (a) 4 (b) 5 (c) 6 (d) 0
18. What is the output of `float f = 5 / 2; printf("%.1f", f);`? <span class="marks">[1]</span>
    (a) 2.5 (b) 2.0 (c) 3.0 (d) 2
19. Which of the following is a valid identifier in C? <span class="marks">[1]</span>
    (a) 2marks (b) total-marks (c) total_marks (d) int
20. Which control structure is used to repeat a block of statements? <span class="marks">[1]</span>
    (a) sequence (b) selection (c) iteration (d) declaration

::: note Answers to Unit 5
**1.** (a) — a compiler translates the whole program first; an interpreter works line by line.
**2.** (a) — the assembler handles assembly language.
**3.** (a) — a missing semicolon breaks the grammar rules of the language.
**4.** (b) — the error appears only when the program runs.
**5.** (b) — `A` is 65, `a` is 97, `0` is 48.
**6.** (c) — Unicode covers the characters of nearly every script.
**7.** (b) — `stdio.h` declares the standard input and output functions.
**8.** (c) — both operands are `int`, so integer division gives 3.
**9.** (b) — 17 = 3 x 5 + 2, remainder 2.
**10.** (b) — post-increment: `y` takes the old value 5, then `x` becomes 6.
**11.** (b) — `a *= 3 + 2` means `a = a * (3 + 2) = 4 * 5 = 20`.
**12.** (b) — `5 > 3` is 1 but `2 > 4` is 0; 1 AND 0 = 0.
**13.** (c) — 1 + 2 + 3 + 4 = 10.
**14.** (b) — a do-while body runs once before the condition is tested; after it, `i` is 4, and `4 > 7` is false.
**15.** (b) — no `break` after case 2, so execution falls through to case 3 and stops: output `BC`.
**16.** (c) — `a[1]` is 4 and `a[3]` is 8, so the sum is 12 (index starts at 0).
**17.** (b) — `strlen` counts the five letters, not the null character.
**18.** (b) — `5 / 2` is integer division (2), stored in a float as 2.0.
**19.** (c) — an identifier cannot begin with a digit, contain a hyphen, or be a keyword.
**20.** (c) — iteration (loops) repeats statements; selection chooses between them.
:::

## 14.7 Unit 6: Web Technology I

1. HTML stands for <span class="marks">[1]</span>
   (a) Hyper Text Markup Language (b) High Text Machine Language (c) Hyper Transfer Markup Language (d) Home Tool Markup Language
2. Which tag does not need a closing tag? <span class="marks">[1]</span>
   (a) `<p>` (b) `<b>` (c) `<br>` (d) `<title>`
3. Which heading tag gives the largest text? <span class="marks">[1]</span>
   (a) `<h6>` (b) `<h3>` (c) `<h1>` (d) `<head>`
4. Which tag creates a hyperlink? <span class="marks">[1]</span>
   (a) `<link>` (b) `<a>` (c) `<href>` (d) `<url>`
5. Which attribute of `<a>` gives the address of the target page? <span class="marks">[1]</span>
   (a) src (b) href (c) alt (d) name
6. Which tag is used for a table header cell? <span class="marks">[1]</span>
   (a) `<td>` (b) `<tr>` (c) `<th>` (d) `<thead>`
7. Which attribute makes an ordered list count with lower-case letters? <span class="marks">[1]</span>
   (a) `type="a"` (b) `type="A"` (c) `type="1"` (d) `type="i"`
8. Which HTML5 element is used to play a video file? <span class="marks">[1]</span>
   (a) `<movie>` (b) `<media>` (c) `<video>` (d) `<play>`
9. Which HTML5 element provides a drawing surface that is drawn on with JavaScript? <span class="marks">[1]</span>
   (a) `<canvas>` (b) `<svg>` (c) `<draw>` (d) `<paint>`
10. Which form control accepts several lines of text? <span class="marks">[1]</span>
    (a) `<input type="text">` (b) `<textarea>` (c) `<input type="radio">` (d) `<select>`
11. Which type of CSS is written directly in the `style` attribute of a tag? <span class="marks">[1]</span>
    (a) inline CSS (b) embedded CSS (c) external CSS (d) imported CSS
12. Where is embedded CSS written? <span class="marks">[1]</span>
    (a) in a `.css` file (b) in a `<style>` tag in the head (c) in the tag's attribute (d) in the `<footer>`
13. Which tag writes text as superscript, as in x<sup>2</sup>? <span class="marks">[1]</span>
    (a) `<sub>` (b) `<sup>` (c) `<super>` (d) `<small>`
14. A software system that lets users create, edit and manage web content without coding is a <span class="marks">[1]</span>
    (a) CMS (b) compiler (c) DBMS (d) router
15. In `<body bgcolor="yellow">`, `bgcolor` is a(n) <span class="marks">[1]</span>
    (a) tag (b) attribute (c) element (d) comment

::: note Answers to Unit 6
**1.** (a) — HyperText Markup Language.
**2.** (c) — `<br>` is an empty tag; `<p>`, `<b>` and `<title>` close.
**3.** (c) — `<h1>` is the largest heading and `<h6>` the smallest.
**4.** (b) — the anchor tag `<a>` makes links.
**5.** (b) — `href` holds the destination; `src` is for images and media.
**6.** (c) — `<th>` is a header cell; `<td>` is data and `<tr>` is a row.
**7.** (a) — `type="a"` gives a, b, c; `"A"` gives capitals; `"i"` gives Roman numerals.
**8.** (c) — HTML5 added `<video>` and `<audio>`.
**9.** (a) — `<canvas>` is drawn on by script; `<svg>` holds vector shapes written in markup.
**10.** (b) — `<textarea>` is the multi-line box.
**11.** (a) — inline CSS is placed in the tag's own `style` attribute.
**12.** (b) — embedded (internal) CSS sits in a `<style>` block in the page.
**13.** (b) — `<sup>` raises text; `<sub>` lowers it.
**14.** (a) — a Content Management System, such as WordPress.
**15.** (b) — `bgcolor` gives extra information to the `<body>` tag; it is an attribute.
:::

## 14.8 Unit 7: Multimedia

1. Which of the following is NOT a component of multimedia? <span class="marks">[1]</span>
   (a) text (b) audio (c) animation (d) printer
2. A sequence of still pictures shown quickly to create the illusion of motion is <span class="marks">[1]</span>
   (a) animation (b) audio (c) text (d) hypertext
3. Which file type holds compressed music? <span class="marks">[1]</span>
   (a) MP3 (b) JPEG (c) DOC (d) PDF
4. Multimedia that lets the user control what is shown next, as in an educational game, is called <span class="marks">[1]</span>
   (a) linear multimedia (b) interactive multimedia (c) printed media (d) analog media
5. Which of these is a graphics file format? <span class="marks">[1]</span>
   (a) WAV (b) MP4 (c) PNG (d) TXT
6. In which field is multimedia used for virtual classrooms and e-learning? <span class="marks">[1]</span>
   (a) education (b) mining only (c) farming only (d) plumbing

::: note Answers to Unit 7
**1.** (d) — the five components are text, graphics, audio, video and animation; a printer is hardware.
**2.** (a) — animation creates apparent motion from stills.
**3.** (a) — MP3 is a compressed audio format.
**4.** (b) — interactivity separates interactive from linear multimedia.
**5.** (c) — PNG is an image format; WAV is audio, MP4 video, TXT text.
**6.** (a) — education is a leading application of multimedia.
:::

## 14.9 Unit 8: Information Security and Cyber Law

1. A program that replicates by attaching itself to other files is a <span class="marks">[1]</span>
   (a) virus (b) firewall (c) browser (d) cookie
2. A malicious program that spreads on its own across a network without needing a host file is a <span class="marks">[1]</span>
   (a) worm (b) trojan horse (c) boot disk (d) patch
3. Software that pretends to be useful but secretly harms the system is a <span class="marks">[1]</span>
   (a) Trojan horse (b) shareware (c) freeware (d) utility
4. Unwanted bulk email is called <span class="marks">[1]</span>
   (a) spam (b) phishing (c) cookie (d) cache
5. Tricking users by a fake website or message to reveal passwords or bank details is called <span class="marks">[1]</span>
   (a) phishing (b) formatting (c) defragmenting (d) cropping
6. Software that demands money to restore access to locked files is <span class="marks">[1]</span>
   (a) ransomware (b) adware (c) freeware (d) middleware
7. The legal right given to the creator of a book, program or song is <span class="marks">[1]</span>
   (a) copyright (b) trademark (c) domain name (d) licence key
8. The right that protects a brand name or logo is <span class="marks">[1]</span>
   (a) copyright (b) trademark (c) patent (d) cookie
9. A digital signature is used to <span class="marks">[1]</span>
   (a) check the identity of the sender and the integrity of a message (b) compress a file (c) print a document (d) increase internet speed
10. Nepal's principal cyber law is the <span class="marks">[1]</span>
    (a) Electronic Transactions Act, 2063 (b) Copyright Act only (c) Education Act (d) Press Council Act
11. A hardware or software barrier that filters traffic between a network and the internet is a <span class="marks">[1]</span>
    (a) firewall (b) router table (c) cookie (d) hub
12. Using someone else's computer or account without permission is <span class="marks">[1]</span>
    (a) hacking (b) formatting (c) backup (d) booting

::: note Answers to Unit 8
**1.** (a) — a virus needs a host file or program to spread.
**2.** (a) — a worm copies itself over networks by itself.
**3.** (a) — a Trojan horse hides harmful code inside something that looks useful.
**4.** (a) — spam is unsolicited bulk mail; phishing is a fraud that may arrive by it.
**5.** (a) — phishing uses fake pages or messages to steal information.
**6.** (a) — ransomware encrypts files and demands payment.
**7.** (a) — copyright protects original works of authorship.
**8.** (b) — a trademark protects names, logos and marks that identify a brand.
**9.** (a) — a digital signature proves who sent it and that it was not changed.
**10.** (a) — the Electronic Transactions Act 2063 (BS) is the main cyber law.
**11.** (a) — a firewall filters packets by rules.
**12.** (a) — unauthorised access is hacking.
:::

## 14.10 Distractor analysis: how wrong options are built

A Group A question has one right option and three wrong ones, and the wrong ones are not random. Learning the four common builds lets you eliminate options even when you are unsure of the answer.

| Build | Example from this chapter | What to do |
|---|---|---|
| **The neighbour**: a term from the same family | In 14.2 item 3, MIPS is offered beside FLOPS | Recall which device the unit belongs to: supercomputers use FLOPS |
| **The inverse**: the opposite property | In 14.2 item 6, ROM is offered for "loses contents" | Re-read the stem for the key word (*volatile*) |
| **The near-miss number**: an off-by-one or a wrong base | In 14.3 item 2, 11010 against 11001; in 14.6 item 16, 6 for a[1] + a[3] | Redo the working on the margin; never trust memory |
| **The common slip**: the answer a careless student reaches | In 14.6 item 15, A is the output if the student ignores fall-through; in item 10, y = 6 if the student reads `x++` as `++x` | Trace the program line by line |

::: caution Three mistakes students actually make
- **Reading `x++` as `++x`.** In `y = x++` the old value is assigned first; in `y = ++x` the new value is assigned.
- **Treating 1 KB as 1000 bytes.** In a computer exam the unit is 1024 bytes unless the question says otherwise.
- **Counting array positions from 1.** The first element is `a[0]`. In 14.6 item 16, `a[1]` is the second element, 4.
:::

## Chapter summary

- Group A is 9 x 1 = 9 marks; answer all nine, because nothing is lost for a wrong one.
- Units 1, 2 and 5 feed most of the harder items: memory and buses, conversions and gates, and C output.
- Conversions to remember: $(1101)_2 = 13$, $25 = (11001)_2$, $(2F)_{16} = 47$, $(17)_8 = 15$; 2's complement = 1's complement + 1.
- Boolean laws: $A + A' = 1$, $A \cdot A' = 0$, $A + 1 = 1$, $A \cdot 0 = 0$, $(A + B)' = A' \cdot B'$.
- Memory: cache is the fastest; RAM and cache are volatile; ROM, PROM, EPROM, EEPROM and flash keep data.
- Programming: `7 / 2 = 3` in `int`; `y = x++` gives old `x`; a `do-while` runs at least once; a `switch` falls through without `break`.
- HTML: `<br>` has no closing tag; `href` is the link address; `<th>` is a header cell; inline, embedded and external are the three CSS types.
- Security: virus, worm, Trojan horse, ransomware, spam and phishing are different things; Nepal's main cyber law is the Electronic Transactions Act, 2063.

## Practice questions

**Group A: Multiple choice (1 mark each)**

1. The generation of computers that used integrated circuits is the <span class="marks">[1]</span>
   (a) first (b) second (c) third (d) fifth
2. Which of the following is the smallest unit of storage? <span class="marks">[1]</span>
   (a) byte (b) bit (c) nibble (d) word
3. What is the output of `printf("%d", 20 / 6 + 20 % 6);`? <span class="marks">[1]</span>
   (a) 5 (b) 3 (c) 6 (d) 8
4. Which HTML tag marks the start of the visible content of a web page? <span class="marks">[1]</span>
   (a) `<head>` (b) `<title>` (c) `<body>` (d) `<html>`

::: note Answers to Group A
**1.** (c) — third generation (1964 to 1971) used integrated circuits.
**2.** (b) — a bit is a single binary digit; a byte is eight bits.
**3.** (a) — `20 / 6` is 3 and `20 % 6` is 2, so the total is 5.
**4.** (c) — everything shown in the browser window sits inside `<body>`.
:::

**Group B: Short answer (5 marks each)**

1. Write the difference between RAM and ROM. Give any three points. <span class="marks">[5]</span>
2. Convert $(110101)_2$ to decimal and $(53)_{10}$ to binary. <span class="marks">[5]</span>
3. Differentiate between a compiler and an interpreter. <span class="marks">[5]</span>
4. What is a Trojan horse? State how it differs from a worm. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** RAM is read-write and volatile (it loses data at power off), holds programs and data in use, and is made of SRAM and DRAM. ROM is read-only in normal use, non-volatile, and stores start-up instructions such as the BIOS; its types are PROM, EPROM and EEPROM. RAM is also usually larger and faster to write than ROM.

**2.** $(110101)_2 = 32 + 16 + 0 + 4 + 0 + 1 = 53$. For 53 to binary: $53 \div 2 = 26$ r 1; $26 \div 2 = 13$ r 0; $13 \div 2 = 6$ r 1; $6 \div 2 = 3$ r 0; $3 \div 2 = 1$ r 1; $1 \div 2 = 0$ r 1. Reading remainders upward gives 110101, so $(53)_{10} = (110101)_2$.

**3.** A compiler translates the whole program into object code before it runs, reports all errors together, and the code then runs fast without the compiler (C is compiled). An interpreter translates and runs one statement at a time, stops at the first error, and needs the interpreter present each time (BASIC and Python are commonly interpreted).

**4.** A Trojan horse is a program that looks useful or harmless but secretly performs harmful acts, such as stealing passwords or opening a back door. It does not copy itself. A worm copies itself automatically across a network without a host program and without user action, and consumes bandwidth.
:::

**Group C: Long answer (8 marks each)**

1. Draw the truth table of the XOR gate with its Boolean expression, and prove $A + AB = A$ using a truth table. <span class="marks">[8]</span>
2. Write a C program to read a number and print whether it is positive, negative or zero, then print the sum of the first $n$ natural numbers using a loop. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** XOR: output is 1 when the inputs differ. Boolean expression: $Y = A \oplus B = A'B + AB'$.

| A | B | Y = A XOR B |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

Proof of $A + AB = A$:

| A | B | AB | A + AB |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 |

The column A + AB equals the column A in every row, so $A + AB = A$ (absorption law).

**2.** Program:

```
#include <stdio.h>
int main() {
    int n, i, sum = 0;
    printf("Enter a number: ");
    scanf("%d", &n);
    if (n > 0)
        printf("Positive\n");
    else if (n < 0)
        printf("Negative\n");
    else
        printf("Zero\n");
    for (i = 1; i <= n; i++)
        sum = sum + i;
    printf("Sum of first %d natural numbers = %d\n", n, sum);
    return 0;
}
```

For input 5 the output is `Positive` and `Sum of first 5 natural numbers = 15`. For a negative or zero input the loop does not run and the sum is 0.
:::
