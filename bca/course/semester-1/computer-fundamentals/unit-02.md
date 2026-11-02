---
subject: Computer Fundamentals and Applications
grade: BCA Semester 1
unit: 2
title: Computer Software
hours: 3
area: BCA 101 · Computer Fundamentals and Applications · Unit 2
---

Hardware without software is an expensive paperweight. **Software** is the set of programs, data and documentation that tells the hardware what to do. This unit classifies software, explains how programs written by humans become machine instructions, and introduces algorithms and flowcharts, the first tools of problem solving.

::: key What this unit gives you
- Software classification: system, application, utility, firmware.
- Language translators: assembler, compiler, interpreter, and when each is used.
- Language generations (1GL to 5GL) and what a programming paradigm is.
- Algorithms and flowcharts with worked examples.
- Licensing: proprietary, freeware, shareware, open source.
:::

## 2.1 Software and its classification

| Category | Purpose | Examples |
|---|---|---|
| **System software** | Runs and manages the hardware; platform for other software | Windows, Linux, Android, device drivers, BIOS/UEFI firmware |
| **Utility software** | Maintenance and housekeeping | antivirus, disk defragmenter, backup, file compression (WinRAR, 7-Zip) |
| **Language translators** | Convert programs into machine code | assembler, compiler, interpreter |
| **Application software** | Does a task for the *user* | MS Word, Excel, browsers, Tally, games |

Application software is further split into:

- **General-purpose (packaged) software**: bought off the shelf for a common need: word processor, spreadsheet, presentation, browser, media player.
- **Custom (bespoke) software**: written for one organisation: a bank's core system, a college's result-processing system.
- **Integrated suites**: several applications sharing one interface, such as MS Office or LibreOffice.

**Firmware** is software stored permanently on a chip inside a device (a router's operating code, the UEFI that starts a PC). It sits between hardware and software.

::: note System vs application, the one-line test
If removing it stops the *computer* from working, it is system software. If removing it only stops *one task* (writing a letter), it is application software.
:::

## 2.2 Language translators

The CPU executes only **machine code**, binary patterns. Humans write in other languages, so a translator is needed.

| | Assembler | Compiler | Interpreter |
|---|---|---|---|
| Translates | assembly language → machine code | whole high-level program → machine code (or bytecode) before running | one statement at a time, while running |
| Output | object file | executable file | none; the result of running is produced directly |
| Speed of execution | fast | fast (translation done once) | slower (translation repeated every run) |
| Error reporting | at assembly time | all syntax errors listed after compiling | stops at the first error found |
| Typical languages | x86 / ARM assembly | C, C++, Go, Rust (Java compiles to bytecode) | Python, JavaScript, PHP (usually with a bytecode step in practice) |

The **source program** is what the programmer types; the **object program** is the translator's output. A **linker** joins object files and library code into one executable; a **loader** (part of the OS) places the executable in memory to run. Java and C# sit between the two camps: they compile to *bytecode*, which a virtual machine then interprets or compiles on the fly.

## 2.3 Generations of programming languages

| Generation | Name | Nature | Example |
|---|---|---|---|
| 1GL | Machine language | binary 0s and 1s; one CPU family only | `10110000 01100001` |
| 2GL | Assembly language | mnemonics (`MOV AL, 61h`), one-to-one with machine code | x86 assembly |
| 3GL | High-level language | English-like, portable, one statement becomes many machine instructions | C, Java, Python, Pascal |
| 4GL | Very high-level / declarative | say *what* you want, not *how* | SQL, report generators, form builders |
| 5GL | Constraint / logic based | the system solves the problem from stated constraints | Prolog, expert-system shells |

**Low-level** languages (1GL, 2GL) are close to the hardware: fast and compact, hard to write and not portable. **High-level** languages trade a little speed for productivity and portability.

**Programming paradigms** are styles of organising a program:

- **Procedural**: a sequence of procedures (functions) that act on data: C, Pascal.
- **Object-oriented**: objects bundle data and the methods that act on it: Java, C++, Python.
- **Functional**: programs are compositions of functions without changing state: Haskell, parts of JavaScript.
- **Declarative / logic**: describe the result: SQL, Prolog.
- **Event-driven**: code runs in response to events (a click): GUI and web programming.

## 2.4 Algorithms and flowcharts

An **algorithm** is a finite, ordered, unambiguous list of steps that solves a problem. A good algorithm has: **input** (zero or more), **output** (at least one), **definiteness** (each step precise), **finiteness** (it ends) and **effectiveness** (each step is doable).

A **flowchart** is a diagram of the algorithm.

| Symbol | Shape | Meaning |
|---|---|---|
| Terminator | rounded rectangle (oval) | Start / End |
| Process | rectangle | calculation or assignment |
| Input/Output | parallelogram | read or print |
| Decision | diamond | yes/no or true/false test, two exits |
| Flow line | arrow | order of execution |
| Connector | small circle | continue elsewhere / on next page |

::: example Worked example: largest of three numbers
**Algorithm**
1. Start.
2. Read A, B, C.
3. Set MAX = A.
4. If B > MAX then MAX = B.
5. If C > MAX then MAX = C.
6. Print MAX. Stop.

**Dry run** with A = 7, B = 19, C = 12: MAX = 7 → B > 7, so MAX = 19 → C = 12 is not > 19, so MAX stays 19 → prints **19**.

**Flowchart in words:** oval *Start* → parallelogram *Read A, B, C* → rectangle *MAX = A* → diamond *B > MAX?* (Yes: rectangle *MAX = B*; No: skip) → diamond *C > MAX?* (Yes: rectangle *MAX = C*; No: skip) → parallelogram *Print MAX* → oval *End*.
:::

::: example Worked example: sum of the digits of a number
**Algorithm**
1. Start. Read N. Set SUM = 0.
2. While N > 0: take DIGIT = N mod 10; SUM = SUM + DIGIT; N = N div 10 (integer division).
3. Print SUM. Stop.

**Dry run** N = 4072: digit 2 → SUM 2, N 407; digit 7 → SUM 9, N 40; digit 0 → SUM 9, N 4; digit 4 → SUM 13, N 0; loop ends. Prints **13**.
:::

::: example Worked example: is a number prime?
1. Read N. If N < 2, print "not prime" and stop.
2. Set I = 2.
3. While I × I ≤ N: if N mod I = 0, print "not prime" and stop; otherwise I = I + 1.
4. Print "prime".

Dry run N = 29: I = 2, 3, 4, 5 are tested (5×5 = 25 ≤ 29); none divides 29; I = 6 gives 36 > 29, so the loop ends: **prime**. For N = 91: I = 7 gives 91 mod 7 = 0, so **not prime**.
:::

The three basic **control structures** are **sequence**, **selection** (if/else) and **iteration** (loops). Every algorithm can be built from these three. **Pseudocode** writes an algorithm in plain structured English without flowchart symbols.

## 2.5 Software licensing and development basics

| Model | Source code | Cost | Example |
|---|---|---|---|
| Proprietary (commercial) | closed | paid licence | Windows, MS Office, Photoshop |
| Freeware | closed | free to use | Adobe Acrobat Reader |
| Shareware / trial | closed | free for a trial period, then pay | WinRAR trial, many games |
| Open source | open; may be modified and redistributed under a licence | usually free | Linux (GPL), Firefox, LibreOffice, VLC |
| SaaS | hosted by the vendor | subscription | Google Workspace, Microsoft 365 |

**Software piracy** (using unlicensed copies) is illegal; it harms developers and exposes users to malware hidden in cracked installers. **Open source** is not the same as *public domain*: the licence (GPL, MIT, Apache) still sets conditions.

Software is built through the **software development life cycle (SDLC)**: requirement gathering → design → coding → testing → deployment → maintenance. The BCA subject *Software Engineering* (Semester IV) treats this properly.

## Formula and fact sheet

- System software runs the machine; application software serves the user; utilities maintain.
- Assembler: assembly → machine. Compiler: whole program first. Interpreter: line by line.
- 1GL machine, 2GL assembly, 3GL high-level, 4GL declarative (SQL), 5GL constraint-based.
- Flowchart: oval start/end, rectangle process, parallelogram I/O, diamond decision.
- Algorithm = input + output + definiteness + finiteness + effectiveness.
- Open source ≠ public domain; shareware ≠ freeware.

## Chapter summary

- Software is divided into system software (OS, drivers, utilities, translators) and application software (general-purpose or custom).
- Translators convert human-readable code to machine code; compilers do it once, interpreters do it each run.
- Languages progress from machine code to assembly to high-level to declarative.
- An algorithm is a finite, precise procedure; a flowchart draws it; sequence, selection and iteration are enough to express any algorithm.
- Licences decide what you may do with software; open source gives freedoms, not freedom from conditions.

## Practice

**A. Short questions**

1. Differentiate system software and application software with two examples each.
2. What is a utility program? Give three examples.
3. Differentiate a compiler and an interpreter. Give one language for each.
4. What is firmware?
5. Write the characteristics of a good algorithm.
6. Name the flowchart symbols for decision, input/output and process.
7. Distinguish freeware, shareware and open-source software.
8. What are the five generations of programming languages?

**B. Problems**

9. Write an algorithm and describe the flowchart to find whether a number is even or odd.
10. Write an algorithm to find the factorial of N and dry-run it for N = 5.
11. Write an algorithm to print the multiplication table of N up to 10.
12. Dry-run the digit-sum algorithm for N = 90581.

**C. Long questions**

13. Explain the types of software with a classification chart.
14. Explain how a high-level program is converted to a running process (translator, linker, loader).

::: note Answers and worked solutions
**1.** System software manages hardware and provides a platform (Windows, Linux; also drivers). Application software performs user tasks (MS Word, Tally).
**2.** Utilities perform maintenance: antivirus, backup tool, disk clean-up, file compressor.
**3.** A compiler translates the whole program to machine code before execution (C); an interpreter translates and executes one statement at a time (Python). Compiled programs usually run faster; interpreted ones are easier to debug interactively.
**4.** Permanent software stored on a hardware chip, such as the UEFI/BIOS or a router's operating code.
**5.** Input, output, definiteness, finiteness, effectiveness.
**6.** Diamond, parallelogram, rectangle.
**7.** Freeware is free but closed; shareware is free for a limited time or with limited features; open source ships its source code under a licence permitting study, modification and redistribution.
**8.** Machine, assembly, high-level, very high-level (4GL), constraint/logic (5GL).
**9.** Read N; compute R = N mod 2; if R = 0 print "even" else print "odd". Flowchart: Start → Read N → R = N mod 2 → diamond *R = 0?* → Yes: Print "even" / No: Print "odd" → End.
**10.** Read N; F = 1; I = 1; while I ≤ N: F = F × I, I = I + 1; print F. For N = 5: F goes 1, 2, 6, 24, 120. **120**.
**11.** Read N; I = 1; while I ≤ 10: print N × I; I = I + 1.
**12.** 90581: digits 1, 8, 5, 0, 9 → 1 + 8 + 5 + 0 + 9 = **23**.
**13.** Software → system (OS, drivers, firmware, utilities, translators) and application (general-purpose, custom, suites); give an example under each branch.
**14.** The programmer writes source code; the compiler produces an object file; the linker combines object files and libraries into an executable; the loader copies the executable into memory and starts it as a process.
:::
