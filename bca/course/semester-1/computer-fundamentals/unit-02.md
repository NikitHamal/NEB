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

```svgfig label="2.1" caption="Classification of computer software with an example under every branch."
f = Fig(760, 300)
f.box(300, 14, 160, 40, "SOFTWARE", fill=NAVY, stroke=NAVY, color="#ffffff", size=14, bold=True)
f.box(110, 96, 190, 40, "System software", fill=MINT, stroke=TEAL, size=13, bold=True)
f.box(470, 96, 190, 40, "Application software", fill=SAND, stroke=AMBER, size=13, bold=True)
f.arrow([(380, 54), (380, 76), (205, 76), (205, 96)], color=SLATE)
f.arrow([(380, 54), (380, 76), (565, 76), (565, 96)], color=SLATE)
for i, (t, e) in enumerate([("Operating\nsystem", "Windows,\nLinux"), ("Device\ndrivers", "printer,\nGPU driver"), ("Utilities", "antivirus,\nbackup"), ("Language\ntranslators", "compiler,\ninterpreter"), ("Firmware", "UEFI,\nrouter code")]):
    x = 8 + i * 74
    f.box(x, 178, 68, 40, t, fill=MINT, stroke=TEAL, size=9.5)
    f.box(x, 232, 68, 40, e, fill="#ffffff", stroke=TEAL, size=9, color=SLATE)
    f.arrow([(205, 136), (205, 158), (x + 34, 158), (x + 34, 178)], color=TEAL)
for i, (t, e) in enumerate([("General\npurpose", "Word,\nbrowser"), ("Custom /\nbespoke", "college\nERP"), ("Packaged\nsuite", "MS Office,\nTally"), ("Web and\nmobile apps", "Fonepay,\nNagarik App")]):
    x = 392 + i * 91
    f.box(x, 178, 84, 40, t, fill=SAND, stroke=AMBER, size=9.5)
    f.box(x, 232, 84, 40, e, fill="#ffffff", stroke=AMBER, size=9, color=SLATE)
    f.arrow([(565, 136), (565, 158), (x + 42, 158), (x + 42, 178)], color=AMBER)
```

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

```svgfig label="2.2" caption="From source code to a running process: the compiled path (top) and the interpreted path (bottom)."
f = Fig(760, 250)
items = [("Source\ncode (.c)", SLATE, SOFT), ("Compiler", TEAL, MINT), ("Object\nfile (.o)", SLATE, SOFT), ("Linker", AMBER, SAND), ("Executable\n(.exe)", SLATE, SOFT), ("Loader", NAVY, BLUE), ("Running\nprocess", RED, ROSE)]
for i, (t, c, bg) in enumerate(items):
    x = 6 + i * 107
    f.box(x, 40, 90, 52, t, fill=bg, stroke=c, size=10.5, bold=True)
    if i: f.arrow([(x - 17, 66), (x, 66)], color=SLATE)
f.text(380, 18, "Compiled language (C, C++): translate once, run many times", size=11, color=TEAL, bold=True)
f.text(380, 130, "Interpreted language (Python, JavaScript): translate and run line by line", size=11, color=AMBER, bold=True)
f.box(40, 152, 150, 52, "Source code\n(.py)", fill=SOFT, stroke=SLATE, size=10.5, bold=True)
f.box(285, 152, 190, 52, "Interpreter\n(reads one statement)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(570, 152, 150, 52, "Output / action", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(190, 178), (285, 178)], color=SLATE)
f.arrow([(475, 178), (570, 178)], color=SLATE)
f.arrow([(380, 204), (380, 232), (115, 232), (115, 204)], color=AMBER, label="next statement", lpos=(250, 224))
```

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

```svgfig label="2.3" caption="Flowchart to test whether a number is even or odd, with the standard symbols named."
f = Fig(760, 250)
f.box(20, 100, 110, 44, "Start", fill=MINT, stroke=TEAL, size=12, bold=True, r=22)
f.box(165, 96, 130, 52, "Read N", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(330, 96, 150, 52, "R = N mod 2", fill=SOFT, stroke=SLATE, size=12, bold=True)
f.poly([(585, 80), (670, 122), (585, 164), (500, 122)], fill=SAND, stroke=AMBER, label="R = 0 ?", lx=585, ly=122, size=12)
f.box(500, 200, 170, 36, "Print \"odd\"", fill=ROSE, stroke=RED, size=11.5, bold=True)
f.box(560, 8, 170, 36, "Print \"even\"", fill=MINT, stroke=TEAL, size=11.5, bold=True)
f.arrow([(130, 122), (165, 122)]); f.arrow([(295, 122), (330, 122)]); f.arrow([(480, 122), (500, 122)])
f.arrow([(585, 80), (585, 44)], color=TEAL, label="Yes", lpos=(605, 62))
f.arrow([(585, 164), (585, 200)], color=RED, label="No", lpos=(605, 182))
f.text(75, 60, "terminator\n(oval)", size=9, color=SLATE); f.text(230, 60, "input / output\n(parallelogram)", size=9, color=SLATE)
f.text(405, 60, "process\n(rectangle)", size=9, color=SLATE); f.text(400, 190, "decision (diamond)\nhas two exits: Yes / No", size=9, color=SLATE)
```

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

## Model answers: medium (5 marks) and long (10 marks) questions

### Medium questions (5 marks)

**Q3. Differentiate a compiler and an interpreter. (5 marks)**

A **compiler** translates the whole source program into machine code in one pass and saves it as an executable file; an **interpreter** reads, translates and executes the program one statement at a time (Figure 2.2). Because a compiled program is translated once, it starts quickly and runs fast. An interpreted program must be translated again on every run, so it is usually slower, but it can stop at the first error and let the programmer test ideas interactively.

| Point | Compiler | Interpreter |
|---|---|---|
| Translation unit | whole program | one statement |
| Output | object file and executable | no separate file |
| Speed of execution | fast | slower |
| Error reporting | all errors after compiling | stops at the first error |
| Memory use | more during compiling | less |
| Examples | C, C++, Java (to bytecode) | Python, JavaScript, PHP |

**Example.** A college billing program written in C is compiled once and the `.exe` is given to the accounts office. A Python script that cleans a marks sheet is run directly, edited and run again within seconds. An **assembler** is a third translator that converts assembly language to machine code.

**Q7. Distinguish freeware, shareware and open-source software. (5 marks)**

Software is distributed under a **licence** that states what the user may do. Three common models differ in price and in access to the source code.

1. **Freeware:** free to use for an unlimited time, but the source code is closed and you may not modify or sell it. *Example:* Adobe Acrobat Reader, Google Chrome.
2. **Shareware:** free to try for a limited time or with limited features; you pay to unlock the full version. *Example:* WinRAR trial, many antivirus programs.
3. **Open-source software:** the source code is published under a licence (GPL, MIT, Apache) that lets anyone study, change and share it. *Example:* Linux, LibreOffice, Firefox, VLC.
4. **Proprietary (commercial) software:** paid and closed. *Example:* Microsoft Office, Tally Prime.

| Type | Cost | Source code | Can modify? |
|---|---|---|---|
| Freeware | free | closed | no |
| Shareware | trial, then paid | closed | no |
| Open source | free or paid support | open | yes |
| Proprietary | paid | closed | no |

**Nepali example.** Many colleges run Linux servers and LibreOffice to avoid licence cost, while accounts departments buy licensed Tally. Using cracked software is piracy and an offence under Nepal's Copyright Act.

**Q5. Explain the characteristics of a good algorithm with a flowchart. (5 marks)**

An **algorithm** is a finite, ordered list of clear steps that solves a problem. A **flowchart** draws the same steps with standard symbols (Figure 2.3).

1. **Input:** zero or more values are supplied (the number N).
2. **Output:** at least one result is produced (even or odd).
3. **Definiteness:** every step is precise and has one meaning, such as "R = N mod 2".
4. **Finiteness:** the algorithm stops after a limited number of steps.
5. **Effectiveness:** each step is simple enough to be carried out by hand or by a machine.
6. **Generality:** it works for every valid input, not only one number.

**Algorithm (even or odd).** Step 1: Start. Step 2: Read N. Step 3: R = N mod 2. Step 4: If R = 0 print "even", else print "odd". Step 5: Stop.

**Flowchart.** Oval (Start) → parallelogram (Read N) → rectangle (R = N mod 2) → diamond (R = 0?) → two exits, Yes to "even" and No to "odd" → oval (Stop). **Dry run:** N = 7 gives R = 1, so the output is **odd**; N = 10 gives R = 0, so the output is **even**.

### Long questions (10 marks)

**Q13. Explain the types of software with a classification chart. (10 marks)**

**Introduction.** **Software** is the set of programs and data that tells the hardware what to do. Without software a computer is only an expensive box of circuits. Software is divided into **system software** and **application software** (Figure 2.1).

**A. System software** manages the hardware and provides a platform on which other programs run.

1. **Operating system:** controls the CPU, memory, files and devices, and gives the user an interface. *Examples:* Windows, Linux, Android.
2. **Device drivers:** small programs that let the OS talk to one device such as a printer, scanner or graphics card.
3. **Utility programs:** maintenance tools such as antivirus, backup, disk clean-up and file compression.
4. **Language translators:** compilers, interpreters and assemblers that convert programs to machine code.
5. **Firmware:** permanent software stored in a chip, for example the UEFI/BIOS or a router's operating code.

**B. Application software** performs tasks for the user.

6. **General-purpose software:** word processor, spreadsheet, browser, media player; useful to many users.
7. **Custom (bespoke) software:** written for one organisation, such as a college admission system or a bank's core system.
8. **Packaged suites:** a set of programs sold together, such as MS Office or Tally Prime.
9. **Web and mobile applications:** run in a browser or phone, such as Fonepay, ConnectIPS and the Nagarik App.

| Basis | System software | Application software |
|---|---|---|
| Purpose | runs and manages the computer | solves a user's task |
| Depends on | hardware | system software |
| Starts | when the computer boots | when the user opens it |
| Needed to run computer? | yes | no |
| Examples | Linux, drivers, BIOS | Word, Tally, Chrome |

**Conclusion.** System software is the foundation and application software is the visible layer built on it. A computer needs both: the OS to manage the machine and applications to do the user's real work.

**Q14. Explain how a high-level program is converted to a running process. (10 marks)**

**Introduction.** A processor understands only machine code (binary), but people write programs in high-level languages such as C. Several system programs, the **translator, linker and loader**, turn the source code into a running **process** (Figure 2.2).

**Stages**

1. **Editing:** the programmer writes the **source code** (`sum.c`) in a text editor or IDE.
2. **Preprocessing:** in C, `#include` files are inserted and macros are replaced.
3. **Compiling:** the **compiler** checks syntax and semantics, reports errors, and translates the code to assembly and then to an **object file** (`sum.o`) containing machine code with unresolved references.
4. **Assembling:** the **assembler** converts assembly to binary object code when the compiler produces assembly first.
5. **Linking:** the **linker** joins one or more object files with library code (for example `printf`) and resolves the addresses, producing the **executable** (`sum.exe`).
6. **Loading:** the **loader**, part of the OS, copies the executable into RAM, sets up the stack and data areas, and sets the program counter to the first instruction.
7. **Execution:** the CPU runs the instructions in the fetch-decode-execute cycle; the program is now a **process** with a process ID and a state (Ready, Running, Waiting).
8. **Debugging:** logical errors are found with a debugger, the source is edited, and the cycle repeats.

| Program | Input | Output | Done by |
|---|---|---|---|
| Compiler | source code | object code | translator |
| Linker | object files + libraries | executable | linker |
| Loader | executable | process in RAM | operating system |
| Interpreter | source code | immediate results | translator (no file) |

**Types of errors.** *Syntax errors* are found by the compiler, *link errors* by the linker (missing library), and *run-time/logical errors* only when the program runs.

**Conclusion.** Compiled languages pay the translation cost once and then run fast, while interpreted languages skip the separate stages and translate during execution. Understanding these stages explains why a program that compiles may still fail to link or run.
