---
subject: Question Bank
grade: 8
unit: 25
title: "Computer Science: Model Question Sets and Predicted Questions"
hours: 0
area: Computer Science
---

This chapter does three jobs. It sets out the **pattern** of the 50-mark Computer Science paper used throughout this bank and shows where each area's marks come from; it gives **two complete model papers**, each of 50 marks and two hours, built to that pattern, with a full answer to every question; and it closes with a **ranked list of practice priorities**, each with the reason it holds its place. Sit each model paper in one go, with a clock, before you look at the answers. Every Python program in the answers was run in Python 3.12, and its output is printed exactly.

::: caution What "predicted" means here, and what it does not
Computer Science in grade 8 is set and marked by your own school, so no outsider knows your paper. The ranks in section 25.4 rest only on the pattern of the paper, on the syllabus of the CDC course and on how much each topic can be asked in a written test: a high rank means **practise this first**, never "this will come"; a low rank means "likely to carry fewer marks", never "safe to skip". Every question in this chapter is an original practice item; none is copied from any school's paper.
:::

::: key The pattern: 50 marks in 2 hours
| Group | Questions | Marks each | Total | What it asks for |
|---|---|---|---|---|
| A | 10 | 1 | 10 | multiple choice: a fact, a full form, a key, a symbol, an output |
| B | 10 | 2 | 20 | two points, a difference, a short conversion, a small program or output |
| C | 5 | 4 | 20 | an explanation with a diagram, a full conversion, an algorithm and flowchart, a complete program |
| **Total** | **25** | | **50** | 2 hours |

Practical work in the computer lab is assessed separately by the school. Groups B and C carry 40 of the 50 written marks, so the paper is won by complete answers, not by quick recall.
:::

## 25.1 What the paper looks like

### Where the marks of each area come from

The twenty lessons fall into the five areas of the CDC course. Both model papers follow the same blueprint: every area has two Group A items and two Group B questions; four areas have a long question, and programming has two, because writing a program or an algorithm with its flowchart is the work that takes a full page.

```figure caption="The blueprint of the two model papers: marks per area, split by group. Programming carries the most (14 marks) because it has two long questions; application software, which is tested mostly in the lab, has no long question."
fig, ax = plt.subplots(figsize=(5.0, 2.9))
areas = ["Computer fundamentals (1–6)", "Application software (7–9)", "Web, communication, society (10–14)",
         "Numbers, graphics, multimedia (15–17)", "Programming (18–20)"]
A = [2, 2, 2, 2, 2]; B = [4, 4, 4, 4, 4]; C = [4, 0, 4, 4, 8]
y = np.arange(5)[::-1]
ax.barh(y, A, color=MUTED, height=0.6, label="Group A")
ax.barh(y, B, left=A, color=ACCENT, height=0.6, label="Group B")
ax.barh(y, C, left=[a + b for a, b in zip(A, B)], color=SERIES[3], height=0.6, label="Group C")
for yi, a, b, c in zip(y, A, B, C):
    ax.text(a + b + c + 0.25, yi, f"{a + b + c}", va="center", fontsize=8, color=INK)
ax.set_yticks(y); ax.set_yticklabels(areas, fontsize=7.8)
ax.set_xlim(0, 16.5); ax.set_xticks([0, 2, 4, 6, 8, 10, 12, 14])
ax.set_xlabel("marks (of 50)", fontsize=8)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="x", color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.legend(fontsize=7.4, loc="lower center", bbox_to_anchor=(0.4, 1.0), ncol=3, frameon=False)
```

| Area (lessons) | Group A | Group B | Group C | Marks |
|---|---|---|---|---|
| Computer fundamentals (1–6) | 2 | 2 questions | 1 question | 10 |
| Application software (7–9) | 2 | 2 questions | | 6 |
| Web, communication and society (10–14) | 2 | 2 questions | 1 question | 10 |
| Number system, graphics and multimedia (15–17) | 2 | 2 questions | 1 question | 10 |
| Programming (18–20) | 2 | 2 questions | 2 questions | 14 |
| **Total** | **10** | **10 (20 marks)** | **5 (20 marks)** | **50** |

Your school may share the marks differently, but the point of a blueprint holds for any grid: **every area appears**. Three lessons left unread cost at least three Group A marks and possibly a long question as well.

::: tip A timing plan that fits the paper
Reading the paper: **5 minutes**. Group A: **10 minutes** (one minute an item). Group B: **40 minutes** (4 minutes a question). Group C: **55 minutes** (about 11 minutes a question; a program or a flowchart takes longer than a definition). Checking: **10 minutes** — trace each program once with a simple input and check every conversion by converting back. Start Group C by the 55-minute mark even if two Group B questions are left; return to them at the end.
:::

## 25.2 Model Set 1

**Computer Science — Class 8. Time: 2 hours. Full marks: 50.**
**Attempt all questions. Give answers in your own words as far as practicable.**

### Question paper

**Group A — Choose the correct answer. [10 × 1 = 10]**

1. The full form of GIGO is
   (a) Good Input, Good Output (b) Garbage In, Garbage Out (c) General Input, General Output (d) Give In, Give Out
2. Integrated circuits were first used in the
   (a) first generation (b) second generation (c) third generation (d) fourth generation
3. The shortcut key for Find and Replace in MS Word is
   (a) Ctrl + F (b) Ctrl + H (c) Ctrl + R (d) Ctrl + P
4. Which formula gives the total of the cells B2 to B10?
   (a) `=TOTAL(B2:B10)` (b) `=SUM(B2:B10)` (c) `=ADD(B2,B10)` (d) `SUM B2-B10`
5. The HTML tag that breaks a line is
   (a) `<lb>` (b) `<br>` (c) `<break>` (d) `<p>`
6. Malware that locks a user's files and demands money is
   (a) adware (b) spyware (c) ransomware (d) a worm
7. The binary equivalent of $(13)_{10}$ is
   (a) 1011 (b) 1101 (c) 1110 (d) 1001
8. Which image format stays sharp however much it is enlarged?
   (a) JPEG (b) BMP (c) PNG (d) SVG
9. The flowchart symbol used for a decision is
   (a) an oval (b) a parallelogram (c) a diamond (d) a rectangle
10. What is printed by `print(19 % 4)` in Python?
    (a) 4 (b) 4.75 (c) 3 (d) 0

**Group B — Answer the following questions briefly. [10 × 2 = 20]**

11. Differentiate between analog and digital computers, with one example of each.
12. What is an operating system? Write any two of its functions.
13. Differentiate between relative and absolute cell references, with examples.
14. Write two differences between a slide transition and an animation.
15. What is e-governance? Give two examples from Nepal.
16. What is phishing? Write two ways to stay safe from it.
17. Convert $(110110)_2$ into decimal and into octal.
18. Write two advantages and two disadvantages of multimedia.
19. Write two differences between a compiler and an interpreter.
20. Write the output of the following Python program.

```python
for i in range(5, 0, -1):
    print(i * i, end=" ")
```

**Group C — Answer the following questions in detail. [5 × 4 = 20]**

21. Explain the first four generations of computers, giving the main component, one feature and one example of each. [4]
22. What is a computer network? Explain bus, ring and star topologies with diagrams. [1+3]
23. (a) Convert $(350)_{10}$ into binary and hexadecimal. (b) Convert $(5B)_{16}$ into octal through binary. [2+2]
24. Write an algorithm and draw a flowchart to find the greatest of three numbers. [2+2]
25. Write a Python program to display the first ten terms of the series 1, 1, 2, 3, 5, 8, … [4]

### Solutions

::: note Group A — answers with reasons
**1.** (b) — wrong input gives wrong output.
**2.** (c) — first vacuum tubes, then transistors, then ICs.
**3.** (b) — Ctrl + F only finds; Ctrl + H finds and replaces.
**4.** (b) — SUM adds a range written with a colon.
**5.** (b) — `<br>` is an empty tag for a line break.
**6.** (c) — ransom-ware: files are held to ransom.
**7.** (b) — 8 + 4 + 0 + 1 = 13.
**8.** (d) — SVG is a vector format; the others are raster.
**9.** (c) — the diamond holds a yes/no question.
**10.** (c) — 19 = 4 × 4 + 3, so the remainder is 3.
:::

::: note Group B — answers
**11.** An analog computer works on continuous quantities such as temperature, speed or pressure and shows its result as a reading on a scale, for example a speedometer. A digital computer works on discrete data counted as 0s and 1s and gives exact numbers, for example a personal computer or a calculator.

**12.** An operating system is the main system software that manages all the hardware and software of a computer and gives the user an interface, such as Windows or Android. Any two functions: process management, memory management, file management, device management, security, providing the user interface.

**13.** A relative reference such as `B2` changes when a formula is copied: copied one row down, `=B2*2` becomes `=B3*2`. An absolute reference such as `$E$1` has dollar signs and stays the same wherever the formula is copied, so `=B2*$E$1` copied down becomes `=B3*$E$1`.

**14.** A transition is the effect when the show moves from one slide to the next; an animation is an effect on one object — a title, picture or chart — on a slide. A transition is applied from the Transitions tab to a whole slide; an animation is applied from the Animations tab and can make an object enter, be emphasised or leave.

**15.** E-governance is the use of ICT by the government to provide its services and information to people quickly and openly. Examples: the Nagarik App, which gives citizens their PAN, driving licence and other records on the phone; paying taxes and registering companies online; online application for passports and public service examinations (any two).

**16.** Phishing is tricking people into giving their passwords, PINs or OTPs through a fake message, e-mail or website that looks as if it came from a bank, wallet or office. Ways to stay safe: never share an OTP, PIN or password with anyone; check the sender and the link, and type the bank's address yourself instead of clicking; turn on multi-factor authentication; report the message (any two).

**17.** $1\times32 + 1\times16 + 0\times8 + 1\times4 + 1\times2 + 0\times1 = 54$, so $(110110)_2 = (54)_{10}$. In threes from the right: 110 110 → 6, 6, so $(110110)_2 = (66)_8$. Check: $6\times8 + 6 = 54$ ✓.

**18.** Advantages: it makes learning interesting and holds attention; it explains hard ideas with pictures, sound and motion (also: suits different learners; reaches a large audience). Disadvantages: making it needs time, skill and costly equipment; its files are large and need storage and fast Internet (also: too many effects distract).

**19.** A compiler translates the whole program at once, while an interpreter translates and runs one line at a time. A compiler makes an object program (.exe) that runs again without it; an interpreter makes no object program and is needed every time the program runs. (Also: a compiler lists all errors at the end; an interpreter stops at the first error.)

**20.** The loop runs for I = 5, 4, 3, 2, 1 and prints each square on one line:

```text
 25  16  9  4  1
```
:::

::: note Group C — answers
**21.**

| Generation | Main component | One feature | Example |
|---|---|---|---|
| First (about 1946–1958) | vacuum tubes | huge, hot and unreliable; machine language | ENIAC, UNIVAC I |
| Second (about 1958–1964) | transistors | smaller, cooler, faster; assembly language and FORTRAN | IBM 1401 |
| Third (about 1964–1975) | integrated circuits | keyboards and monitors; high-level languages; time-sharing | IBM System/360 |
| Fourth (about 1975 to now) | microprocessors (VLSI) | personal computers, GUIs, networks and the Internet | IBM PC, laptops, smartphones |

One mark for each generation with its component, feature and example.

**22.** A computer network is two or more computers and devices connected by wired or wireless media to share data, hardware, software and an Internet connection (1 mark). *Bus*: all computers are joined to one main cable, the backbone, with a terminator at each end; it uses the least cable, but a break in the backbone stops the whole network. Diagram: a long horizontal line with short lines down to four or five computers and a block at each end. *Ring*: each computer is joined to the next and the last to the first in a closed loop, and data travels round in one direction; there are no collisions, but one broken link can stop the ring. Diagram: five or six computers in a circle, each joined to its neighbours. *Star*: every computer has its own cable to a central switch; one faulty cable affects only one computer and faults are easy to find, but if the switch fails the whole network stops. Diagram: a switch in the middle with computers around it, each on its own line (3 marks).

**23.** (a) Divide 350 by 2 and read the remainders from the bottom up:

| Division | Quotient | Remainder |
|---|---|---|
| 350 ÷ 2 | 175 | 0 |
| 175 ÷ 2 | 87 | 1 |
| 87 ÷ 2 | 43 | 1 |
| 43 ÷ 2 | 21 | 1 |
| 21 ÷ 2 | 10 | 1 |
| 10 ÷ 2 | 5 | 0 |
| 5 ÷ 2 | 2 | 1 |
| 2 ÷ 2 | 1 | 0 |
| 1 ÷ 2 | 0 | 1 |

$(350)_{10} = (101011110)_2$. Hexadecimal: 350 ÷ 16 = 21 r 14 (E); 21 ÷ 16 = 1 r 5; 1 ÷ 16 = 0 r 1; so $(350)_{10} = (15E)_{16}$. Check: $1\times256 + 5\times16 + 14 = 256 + 80 + 14 = 350$ ✓.

(b) Four bits for each hexadecimal digit: 5 = 0101, B = 1011, giving 01011011. Regroup in threes from the right: 001 011 011 → 1, 3, 3, so $(5B)_{16} = (133)_8$. Check: $(5B)_{16} = 5\times16 + 11 = 91$ and $(133)_8 = 64 + 24 + 3 = 91$ ✓.

**24.** *Algorithm.* Step 1: Start. Step 2: Read A, B and C. Step 3: Is A > B and A > C? If yes, display A and go to step 6. Step 4: Is B > C? If yes, display B and go to step 6. Step 5: Display C. Step 6: Stop.
*Flowchart.* Start (oval) → Read A, B, C (parallelogram) → diamond "Is A > B and A > C?" → Yes: parallelogram "Display A"; No: diamond "Is B > C?" → Yes: parallelogram "Display B"; No: parallelogram "Display C" → the three paths join → Stop (oval). Both exits of each diamond are labelled Yes and No.
*Test.* A = 45, B = 72, C = 68: the first test fails (45 > 72 is false), the second passes (72 > 68), so the output is 72.

**25.** Each new term is the sum of the two terms before it.

```python
# The first ten terms of 1, 1, 2, 3, 5, ...
a = 1
b = 1
print(a, b, end=" ")
for i in range(3, 11):
    c = a + b
    print(c, end=" ")
    a = b
    b = c
```

```text
1 1 2 3 5 8 13 21 34 55 
```

Marks: the two first terms `a = 1`, `b = 1`; the `for` loop that runs eight more times; the update of `a` and `b` in the right order; labelled/clean output.
:::

::: caution Two Group C slips that this set is built to catch
In question 23, students read the remainders **from the top down** and write 011110101 — the binary number backwards. In question 25, students write `a = b` **after** `b = c`, so `a` and `b` become equal and the series breaks. Order matters in both: remainders are read from the bottom up, and in the update the old `b` must be saved in `a` before `b` changes.
:::

## 25.3 Model Set 2

**Computer Science — Class 8. Time: 2 hours. Full marks: 50.**
**Attempt all questions. Give answers in your own words as far as practicable.**

### Question paper

**Group A — Choose the correct answer. [10 × 1 = 10]**

1. Who is called the father of the computer?
   (a) Blaise Pascal (b) Charles Babbage (c) Herman Hollerith (d) John Napier
2. Software whose source code anyone may study, change and share is called
   (a) proprietary software (b) shareware (c) open-source software (d) tailor-made software
3. Which key starts a PowerPoint slide show from the first slide?
   (a) F1 (b) F5 (c) F7 (d) F12
4. Combining one letter with a list of names to print a personalised copy for each person is called
   (a) mail merge (b) WordArt (c) find and replace (d) page layout
5. To send an e-mail to many people without showing their addresses to each other, put the addresses in
   (a) To (b) Cc (c) Bcc (d) Subject
6. Which device joins a school LAN to the Internet and forwards packets by IP address?
   (a) hub (b) switch (c) router (d) NIC
7. The decimal value of $(17)_8$ is
   (a) 15 (b) 17 (c) 13 (d) 71
8. Which of these is an output device for multimedia?
   (a) microphone (b) webcam (c) projector (d) scanner
9. A program runs without any message but prints a wrong answer. It has
   (a) a syntax error (b) a logical error (c) a run-time error (d) a hardware fault
10. Which Python function generates a sequence of integers for a `for` loop?
    (a) `input()` (b) `print()` (c) `len()` (d) `range()`

**Group B — Answer the following questions briefly. [10 × 2 = 20]**

11. Differentiate between hardware and software, with two examples of each.
12. Write a short note on Charles Babbage's Analytical Engine.
13. What are a header and a footer in a document? Write the steps to insert page numbers in MS Word.
14. Marks are in the cells C2 to C20. Write formulas to find (a) their average and (b) "Pass" in D2 if C2 is 40 or more, otherwise "Fail".
15. Write HTML to show the words "NEB website" as a link to `https://www.neb.gov.np` and a picture `logo.png` 200 pixels wide.
16. Write any four symptoms of a computer infected by a virus.
17. How many bytes does an uncompressed 1024 × 768 image with 24-bit colour need? Give the answer in MB too.
18. Convert $(A9)_{16}$ into binary and into decimal.
19. Write an algorithm to find the simple interest when the principal, time and rate are given.
20. Write the output of the following Python program.

```python
s = "pokhara"
print(s.upper(), len(s), s[2:5].upper())
```

**Group C — Answer the following questions in detail. [5 × 4 = 20]**

21. What is an operating system? Explain CUI and GUI, and single-user and multi-user operating systems, with examples. [1+3]
22. What is cyber crime? Explain any three cyber crimes, and write the punishment that Nepal's Electronic Transactions Act, 2063 gives for two of them. [1+3]
23. (a) Convert $(1101101)_2$ into octal and hexadecimal. (b) Convert $(476)_8$ into decimal and binary. [2+2]
24. The Python program below should print a table of Celsius and Fahrenheit temperatures from 0 °C to 100 °C in steps of 20. Find the three errors, name the type of each, and write the corrected program with its output. [4]

```python
# Celsius to Fahrenheit table
print("Celsius", "Fahrenheit")
for c in range(0, 101, 20)
    f = c * 9 / 5 + 23
    prnt(c, f)
```

25. Write a Python program that reads ten numbers one by one and displays the largest and the smallest of them. [4]

### Solutions

::: note Group A — answers with reasons
**1.** (b) — his Analytical Engine had input, mill, store and output, like a modern computer.
**2.** (c) — "open source": the code is open to all.
**3.** (b) — F5 starts from the beginning; Shift + F5 from the current slide.
**4.** (a) — mail merge joins a main document with a data source.
**5.** (c) — Bcc means blind carbon copy.
**6.** (c) — a router joins different networks and uses IP addresses.
**7.** (a) — $1\times8 + 7 = 15$.
**8.** (c) — a projector shows pictures; the others take input.
**9.** (b) — the method is wrong, but the grammar is correct.
**10.** (d) — `range()` generates a sequence of whole numbers for a `for` loop.
:::

::: note Group B — answers
**11.** Hardware is the physical, touchable part of a computer, such as the keyboard, monitor, CPU and printer. Software is the set of programs that tells the hardware what to do, such as Windows and MS Word. Hardware cannot work without software, and software needs hardware to run on.

**12.** Charles Babbage designed the Analytical Engine in 1834 as a general-purpose calculating machine to be controlled by punched cards. It had an input unit (cards), a **mill** that did the calculations, a **store** (memory) and an output unit — the same parts as a modern computer — although it was never completed. Ada Lovelace wrote a program for it in 1843.

**13.** A header is text printed at the top of every page and a footer is text printed at the bottom of every page, such as the school's name, a title or the date. To insert page numbers: Insert tab → Page Number → choose the position (top or bottom of the page) and a style; the numbers appear on every page automatically.

**14.** (a) `=AVERAGE(C2:C20)` (b) `=IF(C2>=40,"Pass","Fail")`, then copy it down with AutoFill for the other students.

**15.**

```html
<a href="https://www.neb.gov.np">NEB website</a>
<img src="logo.png" alt="Logo" width="200">
```

**16.** Any four: the computer becomes very slow or hangs; programs crash or the computer restarts by itself; files go missing, change or will not open; folders on a pen drive become shortcuts; unwanted pop-ups appear; the antivirus is turned off by itself; messages are sent from your account without you.

**17.** Pixels = 1024 × 768 = 786,432; 24 bits = 3 bytes, so size = 786,432 × 3 = **2,359,296 bytes**; ÷ 1024 ÷ 1024 = **2.25 MB**.

**18.** Four bits for each digit: A = 1010, 9 = 1001, so $(A9)_{16} = (10101001)_2$. Decimal: $10\times16 + 9 = 169$, so $(A9)_{16} = (169)_{10}$. Check: 128 + 32 + 8 + 1 = 169 ✓.

**19.** Step 1: Start. Step 2: Read P, T and R. Step 3: SI = P × T × R ÷ 100. Step 4: Display SI. Step 5: Stop.

**20.** `s.upper()` gives `POKHARA`, `len(s)` gives `7` and `s[2:5].upper()` gives `KHA`. On one line:

```text
POKHARA 7 KHA
```
:::

::: note Group C — answers
**21.** An operating system is the main system software that manages all the hardware and software of a computer and gives an interface between the user and the computer (1 mark). *CUI* (character user interface): the user types commands at a prompt — MS-DOS, the Linux terminal; commands must be remembered. *GUI* (graphical user interface): the user works with windows, icons, menus and a pointer or touch — Windows, macOS, Android; easy for beginners. *Single-user* OS: one person uses the computer at a time — Windows 11 Home on a home PC. *Multi-user* OS: many users work on the same computer at the same time, usually over a network — Linux and UNIX servers (3 marks).

**22.** Cyber crime is any illegal act done with a computer, a phone or the Internet (1 mark). Any three: *hacking* — getting into a computer, account or network without permission; *phishing* — fake messages or websites that trick people into giving passwords, PINs or OTPs; *cyber bullying* — insulting, threatening or shaming someone online again and again; *identity theft* — using someone's personal details to pretend to be them; *software piracy* — copying or using software without a licence. Punishments under the ETA 2063 (any two): unauthorised access (hacking), section 45 — a fine up to Rs 2 lakh, imprisonment up to 3 years, or both; pirating, destroying or altering computer source code, section 44 — up to 3 years, up to Rs 2 lakh, or both; damaging a computer and its information, section 46 — up to Rs 2 lakh, up to 3 years, or both; publishing illegal material in electronic form, section 47 — up to Rs 1 lakh, up to 5 years, or both; computer fraud, section 52 — up to Rs 1 lakh, up to 2 years, or both (3 marks).

**23.** (a) In threes from the right, padding the left with zeros: 001 101 101 → 1, 5, 5, so $(1101101)_2 = (155)_8$. In fours from the right: 0110 1101 → 6, D, so $(1101101)_2 = (6D)_{16}$. Check: $(155)_8 = 64 + 40 + 5 = 109$ and $(6D)_{16} = 96 + 13 = 109$ ✓.

(b) $4\times8^2 + 7\times8^1 + 6\times8^0 = 256 + 56 + 6 = 318$, so $(476)_8 = (318)_{10}$. Binary, three bits for each octal digit: 4 = 100, 7 = 111, 6 = 110, so $(476)_8 = (100111110)_2$. Check: 256 + 32 + 16 + 8 + 4 + 2 = 318 ✓.

**24.** (1) `for c in range(0, 101, 20)` is missing the colon `:` at the end — a **syntax error**. (2) `f = c * 9 / 5 + 23` — a **logical error**: the formula adds `32`, not `23`. (3) `prnt(c, f)` — a **run-time (`NameError`)** error: the built-in function is `print`. Corrected program:

```python
# Celsius to Fahrenheit table
print("Celsius", "Fahrenheit")
for c in range(0, 101, 20):
    f = c * 9 / 5 + 32
    print(c, f)
```

```text
Celsius Fahrenheit
0 32.0
20 68.0
40 104.0
60 140.0
80 176.0
100 212.0
```

Check: 100 × 9 ÷ 5 + 32 = 180 + 32 = 212 ✓.

**25.** The first number read becomes both the largest and the smallest so far; each later number is compared with both.

```python
# Largest and smallest of ten numbers
for i in range(1, 11):
    n = float(input("Number: "))
    if i == 1:
        largest = n
        smallest = n
    if n > largest:
        largest = n
    if n < smallest:
        smallest = n
print("Largest =", largest)
print("Smallest =", smallest)
```

```text
Number: 23
Number: 7
Number: 56
Number: 12
Number: 89
Number: 4
Number: 61
Number: 33
Number: 18
Number: 45
Largest = 89.0
Smallest = 4.0
```

Marks: the loop of ten; reading each number; the starting values from the first number; the two comparisons; the labelled output.
:::

::: caution The answer that loses the mark in question 25
Many students set `largest = 0` and `smallest = 0` before the loop. The largest still comes out right for positive numbers, but the smallest stays `0`, because no number typed is below `0`. Start both from the **first number read**, as above.
:::

## 25.4 Ranked practice priorities

The order below is a judgement from the pattern of the paper, the syllabus and how easily each topic is turned into written questions. **Tier A** is worth rehearsing until it is automatic; **Tier B** is the second pass; **Tier C** is a quick pass in the last week.

### Tier A — rehearse until automatic

| Rank | Topic and likely form | Marks | Why it ranks here |
|---|---|---|---|
| 1 | Number conversions: decimal to binary, octal and hexadecimal by division; to decimal by expansion; binary ↔ octal ↔ hexadecimal by grouping | 1, 2 or 4 | A fixed method marked step by step; it fits every group, and both model sets give it a long question. |
| 2 | A complete Python program with input, a decision or a loop, and labelled output | 4 | Programming has two long questions; a program is marked by its parts, so a partly right program still scores. |
| 3 | An algorithm and a matching flowchart for a short problem (area, interest, odd or even, greatest, sums, tables, factorial) | 2 or 4 | The other programming long question; the symbols and the matching of steps are easy to mark. |
| 4 | The output of a Python program or of built-in functions (`%`, `//`, `**`, `len()`, `round()`, `range()`, string slicing) | 1 or 2 | Quick to set and to mark; tracing a loop in a table makes it safe. |
| 5 | Network topologies with diagrams; LAN, MAN and WAN; network devices | 1, 2 or 4 | The natural long question of the web and communication area; three diagrams earn three marks. |
| 6 | Compiler and interpreter, low- and high-level languages, the three types of error, finding errors in a program | 1, 2 or 4 | Two-point differences are the favourite short question, and "find the errors" turns into a long one. |

### Tier B — second pass

| Rank | Topic and likely form | Marks | Why it ranks here |
|---|---|---|---|
| 7 | Malware types (virus, worm, Trojan, spyware, adware, ransomware), symptoms, antivirus and protection | 1 or 2 | Many short definitions and lists; a common Group B question. |
| 8 | Cyber crimes and the Electronic Transactions Act, 2063 with its sections and punishments | 1, 2 or 4 | The section numbers and penalties are exact facts, easy to ask in any group. |
| 9 | Spreadsheet formulas: SUM, AVERAGE, MAX, MIN, COUNT, IF; relative and absolute references | 1 or 2 | The most "written" part of application software; every formula is right or wrong. |
| 10 | HTML: the page structure, headings, lists, images, links and tables | 1, 2 or 4 | A small page or table is a quick program-like question. |
| 11 | Generations of computers: component, feature and example of each | 1 or 4 | Fits neatly into a table answer; first-to-fourth generations make a ready long question. |
| 12 | Types of computer: analog, digital, hybrid; super, mainframe, mini, micro; general and special purpose | 1 or 2 | Classifications with examples, often as a difference. |
| 13 | System and application software; packaged and tailor-made; software licences | 1 or 2 | Clear differences, each with examples. |
| 14 | Raster and vector graphics; BMP, JPEG, PNG, GIF and SVG; image size from pixels and colour depth | 1 or 2 | A difference, a full form or a one-line calculation. |

### Tier C — a quick pass before the paper

| Rank | Topic and likely form | Marks | Why it ranks here |
|---|---|---|---|
| 15 | Operating system: functions, CUI and GUI, types, files, paths and the Recycle Bin | 1, 2 or 4 | Well known from daily use; usually short questions. |
| 16 | ICT: components, Internet services, e-mail fields, e-governance, digital payments, the digital divide | 1 or 2 | Many facts, each worth a short answer. |
| 17 | History: Babbage, Lovelace, ENIAC and UNIVAC, computers in Nepal | 1 or 2 | Names and years make good objective items; a short note on Babbage is common. |
| 18 | Multimedia: the five elements, hardware and software, uses, advantages and disadvantages | 1 or 2 | Lists and examples; one calculation of sound size at most. |
| 19 | Word processor and presentation features: shortcut keys, mail merge, header and footer, transition and animation, slide views | 1 or 2 | Mostly practical work; the written paper asks keys and short steps. |
| 20 | Fundamentals: data and information, IPOS, characteristics, limitations and uses | 1 or 2 | The first lesson of the book; definitions and lists, rarely a long question. |

```figure caption="The marks of each model set sorted by tier. Tier A carries half of Set 1 (25 marks) and 22 marks of Set 2; together Tiers A and B cover 40 and 35 of the 50 marks, so Tier C can never be skipped entirely."
fig, ax = plt.subplots(figsize=(5.0, 2.6))
tiers = ["Tier A (ranks 1–6)", "Tier B (ranks 7–14)", "Tier C (ranks 15–20)"]
s1 = [25, 15, 10]; s2 = [22, 13, 15]
x = np.arange(3)
ax.bar(x - 0.19, s1, width=0.36, color=ACCENT, label="Model Set 1")
ax.bar(x + 0.19, s2, width=0.36, color=SERIES[3], label="Model Set 2")
for xi, a, b in zip(x, s1, s2):
    ax.text(xi - 0.19, a + 0.5, str(a), ha="center", fontsize=8, color=INK)
    ax.text(xi + 0.19, b + 0.5, str(b), ha="center", fontsize=8, color=INK)
ax.set_xticks(x); ax.set_xticklabels(tiers, fontsize=8)
ax.set_ylim(0, 30); ax.set_ylabel("marks (of 50)", fontsize=8)
ax.spines[["top", "right"]].set_visible(False)
ax.yaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.legend(fontsize=7.6, frameon=False)
```

| Tier | Set 1 questions | Set 2 questions |
|---|---|---|
| A | 7, 9, 10, 17, 19, 20, 22, 23, 24, 25 | 6, 7, 9, 10, 18, 19, 20, 23, 24, 25 |
| B | 2, 4, 5, 6, 8, 11, 13, 16, 21 | 2, 14, 15, 16, 17, 22 |
| C | 1, 3, 12, 14, 15, 18 | 1, 3, 4, 5, 8, 11, 12, 13, 21 |

::: tip The last week before the paper
Day 1–2: number conversions, ten of each kind, each checked by converting back. Day 3–4: write and trace six Python programs — one each with `if`, `if … elif … else`, `for … in range()`, `while`, and string slicing/methods. Day 5: three algorithms with flowcharts, drawn with all the symbols. Day 6: the differences of Tier A and B, as two-column tables. Day 7: one model set, timed, then the error list of everything you got wrong.
:::

## 25.5 Two answers written the way the marker pays

::: example A 2-mark difference: compiler and interpreter
**Question.** Write two differences between a compiler and an interpreter.

**Model answer.** (1) A compiler translates the **whole program at once**, while an interpreter translates and runs it **one line at a time**. (2) A compiler **makes an object program** (an `.exe` file) that runs again without it, while an interpreter **makes no standalone object program** and is needed every time the program runs.

One mark for each difference. Each sentence compares the same feature of both translators. Writing "a compiler is fast" alone earns nothing, because it says nothing about the interpreter.
:::

::: example A 4-mark program: odd or even, written to be marked
**Question.** Write a Python program to read a number and display whether it is odd or even.

**Model answer.**

```python
# Odd or even
n = int(input("Enter a whole number: "))
if n % 2 == 0:
    print(n, "is an even number.")
else:
    print(n, "is an odd number.")
```

```text
Enter a whole number: 46
46 is an even number.
```

Four marks: (1) a descriptive `#` comment; (2) `int(input(...))` with a clear prompt; (3) the condition `n % 2 == 0` in a properly indented `if … else:` block; (4) both outputs with labels. The sample run shows the marker that the program works; it was produced by running the program.
:::

## Chapter summary

- The paper is **10 + 20 + 20 = 50** marks in two hours: ten 1-mark multiple-choice items, ten 2-mark short questions and five 4-mark long questions; practical work is assessed separately.
- In the blueprint every area has two Group A items and two Group B questions; programming carries 14 marks with two long questions, and fundamentals, web and communication, and numbers, graphics and multimedia carry 10 each.
- A workable clock: 5 minutes reading, 10 for Group A, 40 for Group B, 55 for Group C, 10 for checking.
- The six topics worth rehearsing first: number conversions, complete Python programs, algorithms with flowcharts, program output, network topologies, and translators and errors.
- Write points, not paragraphs; compare the same feature in every difference; show every division in a conversion and check it by converting back; trace every program once and write its output.
- Both model papers are rehearsals built to the pattern, not forecasts: no one outside your school knows its paper.
