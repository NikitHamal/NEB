---
subject: Question Bank
grade: 11
unit: 15
title: "Computer Science: Unit-wise Subjective Question Bank"
hours: 0
area: Computer Science
---

The written part of the Grade 11 Computer Science paper is **41 of the 50 marks**: five short questions of 5 marks in Group B and two long questions of 8 marks in Group C. Group B usually carries an "or" choice in two or three of its questions, so a candidate who knows the syllabus well has room to choose. Group C is where C programs, HTML pages and the longer explanations are asked.

This chapter gives, for each of the eight units, short (5-mark) and long (8-mark) practice questions with model answers written the way an examiner wants to see them: a definition, the points in a list, a diagram or table where one helps, and for programs a clean listing with a sample run. All C programs below were compiled with gcc and run on the inputs shown.

::: key How to use this chapter
- **Time yourself by the marks.** The paper is 2 hours for 50 marks, so about 2.4 minutes per mark: roughly 12 minutes for a 5-mark answer and 19 for an 8-mark answer, leaving ten minutes for checking.
- **Attempt first, then read.** Compare your points with the model, not your words.
- **Count points.** A 5-mark question wants five markable statements; an 8-mark question wants a structure.
- **For programs:** declare, read, process, print; indent consistently; a missing semicolon or `&` costs marks.
:::

::: caution About years and labels
Every question here is an **original practice question** written to the NEB pattern from the Grade 11 syllabus. No question carries a past-paper year, because a wrong year teaches you to trust the wrong thing. Do not treat any question as "sure to come"; treat each as a skill to practise.
:::

## 15.1 What the examiner is paying for

| Question type | Marks | What earns the marks |
|---|---|---|
| Define and explain | 5 | one mark for the definition, then one mark per correct point (four) |
| Differentiate between | 5 | a table with at least five rows, each row a true contrast |
| Write a C program | 5 or 8 | correct header, declarations, input, logic, output; **a right-looking program with wrong logic loses most of the marks** |
| Write HTML code | 5 or 8 | correct nesting, closing tags, attributes in quotes, tags used for the stated job |
| Short notes | 5 | 2.5 + 2.5 for two topics, or four points with a diagram |
| Explain with diagram | 8 | diagram (about 3 marks) plus explanation |

## 15.2 Unit 1: Computer System

### Short questions (5 marks each)

**1. Define computer. Write any four characteristics of a computer. (1+4)**

A computer is an electronic device that accepts data as input, processes it under the control of a stored program, stores it, and produces information as output.

Characteristics:
1. **Speed**: it executes millions of instructions each second.
2. **Accuracy**: results are correct unless the data or program is wrong (garbage in, garbage out).
3. **Diligence**: it works for hours without tiredness or loss of concentration.
4. **Storage**: it keeps large amounts of data and recalls it instantly.
5. **Versatility**: the same machine does calculations, word processing, design and communication.

**2. Describe the five generations of computers. (5)**

| Generation | Period | Switching device | Features and example |
|---|---|---|---|
| First | 1940 to 1956 | Vacuum tubes | large, hot, machine language, high electricity use (ENIAC, UNIVAC) |
| Second | 1956 to 1963 | Transistors | smaller and faster, assembly language, magnetic core memory (IBM 1401) |
| Third | 1964 to 1971 | Integrated circuits | keyboard and monitor, operating systems, high-level languages (IBM 360) |
| Fourth | 1971 to present | Microprocessors (LSI/VLSI) | personal computers, GUI, networks (Intel 4004 began it) |
| Fifth | present and beyond | ULSI and artificial intelligence | parallel processing, speech recognition, robotics |

**3. Explain the types of RAM and ROM. (2.5+2.5)**

*RAM* is read-write, volatile memory that holds programs and data in use.
- **SRAM** (static RAM): uses flip-flops, no refreshing, faster and costlier; used for cache.
- **DRAM** (dynamic RAM): uses capacitors that must be refreshed constantly, cheaper and slower; used as main memory (SDRAM is a synchronous form).

*ROM* is non-volatile memory whose contents are fixed or changed only by special means; it stores the start-up (boot) program.
- **PROM**: programmed once by the user after manufacture.
- **EPROM**: erased by ultraviolet light and reprogrammed.
- **EEPROM**: erased electrically, byte by byte; flash memory is of this family.

**4. What is a bus? Explain the data bus, address bus and control bus. (1+4)**

A bus is a set of parallel wires that carries data, addresses or signals between the components of a computer.

| Bus | Carries | Direction |
|---|---|---|
| Data bus | the data and instructions being moved | bidirectional |
| Address bus | the memory or I/O address to be accessed; its width fixes the maximum memory (n lines give $2^n$ locations) | unidirectional (CPU to memory) |
| Control bus | control signals such as read, write, clock and interrupt | bidirectional |

**5. Differentiate between impact and non-impact printers, and between inkjet and laser printers. (2.5+2.5)**

| Impact printer | Non-impact printer |
|---|---|
| Characters formed by striking a ribbon with pins or hammers | No striking; uses ink spray, heat or toner |
| Noisy | Quiet |
| Can make carbon copies | Cannot make carbon copies |
| Dot matrix | Inkjet, laser |

| Inkjet printer | Laser printer |
|---|---|
| Sprays tiny ink droplets | Fuses toner powder with a laser-drawn drum image and heat |
| Cheaper to buy, costlier ink per page | Costlier to buy, cheaper per page |
| Slower | Faster and sharper |

**6. Write short notes on OMR, OCR, BCR and MICR. (5)**

- **OMR** (Optical Mark Recognition): senses pencil marks in bubbles, used for objective answer sheets.
- **OCR** (Optical Character Recognition): converts scanned images of printed or typed text into editable text.
- **BCR** (Bar Code Reader): reads the stripes of a bar code to identify a product at a sales counter.
- **MICR** (Magnetic Ink Character Recognition): reads characters printed in magnetic ink, used on bank cheques.
- All four are input devices that reduce typing and mistakes.

**7. What is a microprocessor? Explain clock speed and word length. (1+4)**

A microprocessor is a single integrated circuit that contains the arithmetic and logic unit (ALU), the control unit (CU) and registers; it is the CPU of a microcomputer.
- **Clock speed**: the number of clock pulses per second, measured in hertz (GHz). The higher it is, the more instructions are executed per second.
- **Word length**: the number of bits the processor handles in one operation (for example 32 or 64). A longer word processes more data per cycle and can address more memory.
- ALU does arithmetic and logic; CU fetches and decodes instructions and directs the other units; registers hold data temporarily.

**8. What is mobile computing? Write any three applications. (2+3)**

Mobile computing is the use of portable, wireless-connected devices, such as smartphones and tablets, to work, communicate and access information while moving.

Applications: (i) mobile banking and digital wallets, (ii) navigation and ride services using GPS, (iii) online classes and video meetings, (iv) email and messaging, (v) shopping and ticket booking.

### Long questions (8 marks each)

**9. Explain the components of a computer system with a block diagram. (3+5)**

```
            +---------------------- CPU -----------------------+
 Input ---> |  Control Unit  <--->  ALU      (registers inside) | ---> Output
 devices    +----------------------^----------------------------+      devices
                                    |
                          Primary memory (RAM, ROM, cache)
                                    |
                          Secondary storage (disk, flash, DVD)
```

- **Input unit**: receives data and instructions (keyboard, mouse, scanner, microphone) and converts them to a form the computer understands.
- **Processing unit (CPU)**: the control unit directs the work; the ALU carries out arithmetic and logic operations.
- **Memory**: primary memory (RAM, ROM, cache) holds the data and instructions in use; secondary memory stores them permanently.
- **Output unit**: gives results in a human form (monitor, printer, speaker).
- **Storage**: secondary storage is non-volatile and large, such as a hard disk, flash drive, DVD or external drive.

**10. Explain the types of computer on the basis of size. (8)**

| Type | Size and users | Features | Example uses |
|---|---|---|---|
| Supercomputer | largest, fastest, very costly | thousands of processors, speed in FLOPS | weather forecasting, scientific simulation |
| Mainframe | large, a room | serves hundreds or thousands of users at once; very reliable | banks, airline booking, large government systems |
| Minicomputer | medium | multi-user, smaller than a mainframe | small companies, factory control, departments |
| Microcomputer | smallest, single user | desktop, laptop, tablet, smartphone | home, office, school |

Add that they differ in speed, memory, cost and the number of users they can support.

**11. Explain the secondary storage devices. (8)**

Secondary storage is permanent, high-capacity storage outside the CPU.
- **Magnetic disk (hard disk)**: spinning platters coated with magnetic material, read by heads; large and cheap per gigabyte, capacities in terabytes.
- **Flash memory (pen drive, SSD, memory card)**: electronic EEPROM-type memory with no moving parts; fast, light and shock resistant.
- **Optical disk (CD, DVD, Blu-ray)**: data is burned as pits and read by a laser; CD about 700 MB, DVD about 4.7 GB; used for software and films.
- **External storage devices**: portable hard disks and flash drives connected by USB, used for backup and transfer.

## 15.3 Unit 2: Number System and Boolean Logic

### Short questions (5 marks each)

**1. Convert $(156)_{10}$ into binary, octal and hexadecimal. (5)**

Binary by repeated division by 2: 156 r 0, 78 r 0, 39 r 1, 19 r 1, 9 r 1, 4 r 0, 2 r 0, 1 r 0, 0 r 1. Reading upward: $(156)_{10} = (10011100)_2$.

Octal: group the bits in threes from the right, 010 011 100, which is 2, 3, 4, so $(234)_8$.

Hexadecimal: group in fours, 1001 1100, which is 9 and C, so $(9C)_{16}$.

Check: $9 \times 16 + 12 = 156$.

**2. Convert $(2AF)_{16}$ to binary and decimal, and $(754)_8$ to decimal and hexadecimal. (5)**

$(2AF)_{16}$: 2 = 0010, A = 1010, F = 1111, so $(001010101111)_2$. Decimal: $2 \times 256 + 10 \times 16 + 15 = 687$.

$(754)_8 = 7 \times 64 + 5 \times 8 + 4 = 492$. For hexadecimal, $492 = 1 \times 256 + 14 \times 16 + 12$, so $(1EC)_{16}$.

**3. Add $(1011)_2$ and $(1101)_2$. Then subtract $(1010)_2$ from $(1101)_2$ using 2's complement. (2+3)**

Addition: $1011 + 1101$: from the right, 1+1 = 10 (write 0, carry 1); 1+1+1 = 11 (write 1, carry 1); 0+1+1 = 10 (write 0, carry 1); 1+1+1 = 11. Result $(11000)_2$, which is 24 (11 + 13).

Subtraction: 4-bit numbers. 1's complement of 1010 = 0101; add 1 gives the 2's complement 0110. Then $1101 + 0110 = 1\,0011$. The carry out of the leftmost place is discarded, so the answer is $(0011)_2 = 3$ (13 - 10).

**4. Subtract $(10011)_2$ from $(11001)_2$ using 1's complement. (5)**

1's complement of 10011 = 01100. Add: $11001 + 01100 = 1\,00101$. There is a carry out of the leftmost bit, so add it back (end-around carry): $00101 + 1 = 00110$. The result is $(110)_2 = 6$, which agrees with 25 - 19 = 6.

**5. Draw the truth tables of NAND, NOR and XNOR gates, and state which are universal gates. (5)**

| A | B | NAND | NOR | XNOR |
|---|---|---|---|---|
| 0 | 0 | 1 | 1 | 1 |
| 0 | 1 | 1 | 0 | 0 |
| 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 0 | 1 |

NAND is AND followed by NOT; NOR is OR followed by NOT; XNOR gives 1 when the inputs are equal. **NAND and NOR are universal gates**, because any other gate can be built from either one alone.

**6. State and verify De Morgan's theorem $(A + B)' = A' \cdot B'$ using a truth table. (5)**

The complement of a sum is the product of the complements.

| A | B | A + B | (A + B)' | A' | B' | A'B' |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 1 | 1 | 1 | 1 |
| 0 | 1 | 1 | 0 | 1 | 0 | 0 |
| 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| 1 | 1 | 1 | 0 | 0 | 0 | 0 |

The columns $(A + B)'$ and $A'B'$ are identical, so the theorem is verified. The dual form is $(AB)' = A' + B'$.

**7. State and verify the distributive law $A(B + C) = AB + AC$. (5)**

| A | B | C | B + C | A(B + C) | AB | AC | AB + AC |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

The columns A(B + C) and AB + AC agree in all eight rows, so the law holds.

### Long questions (8 marks each)

**8. Describe the AND, OR, NOT, XOR gates, giving the Boolean function and truth table of each. (8)**

| Gate | Boolean function | Output is 1 when |
|---|---|---|
| AND | $Y = A \cdot B$ | both inputs are 1 |
| OR | $Y = A + B$ | at least one input is 1 |
| NOT | $Y = A'$ | the input is 0 (it inverts) |
| XOR | $Y = A \oplus B = A'B + AB'$ | the inputs are different |

| A | B | AND | OR | XOR | NOT A |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 |

Symbols: AND has a flat back and curved front; OR has a curved back and pointed front; NOT is a triangle with a small circle at the tip; XOR is the OR shape with an extra curved line at the input. A small circle on the output of AND or OR makes NAND or NOR.

**9. Explain the two methods of binary subtraction using complements, with one example each. (8)**

Computers subtract by adding a complement, which lets one adder do both jobs.
- **1's complement**: invert every bit of the number to be subtracted and add. If a carry comes out of the leftmost bit, add it back to the result (end-around carry); the answer is positive. If there is no carry, the answer is negative and is the 1's complement of the sum.
- **2's complement**: invert every bit and add 1; add this to the other number and discard any final carry. If there is no carry, the answer is negative and is in 2's complement form.

Example 1's complement: 13 - 10 with 4 bits. 1's complement of 1010 is 0101. $1101 + 0101 = 1\,0010$; end-around carry gives $0010 + 1 = 0011$, which is 3.

Example 2's complement: 13 - 10 with 4 bits. 2's complement of 1010 is 0110. $1101 + 0110 = 1\,0011$; discard the carry; the answer is 0011, which is 3.

## 15.4 Unit 3: Computer Software and Operating System

### Short questions (5 marks each)

**1. Define software. Explain system software and utility software. (1+4)**

Software is a set of programs and related data that tells hardware what to do.
- **System software** controls the hardware and provides a platform for other software: operating systems, language translators and device drivers.
- **Utility software** helps maintain, protect and tune the computer: antivirus, disk defragmenter, backup, file compression and disk cleanup tools.
- Application software (word processors, games) serves the user's own tasks; web-based software runs in a browser; mobile apps run on phones.

**2. What is an operating system? Write any four functions. (1+4)**

An operating system (OS) is system software that manages hardware and software resources and provides an interface between the user and the computer.
1. **Process management**: schedules the CPU among programs.
2. **Memory management**: allocates and frees RAM.
3. **File management**: creates, names, stores and protects files and folders.
4. **Device management**: controls input and output devices through drivers.
5. **Security and user interface**: passwords and permissions, and a command line or GUI.

**3. Differentiate between multiprogramming, multitasking, multiprocessing and distributed operating systems. (5)**

| Type | Idea |
|---|---|
| Multiprogramming | several programs kept in memory; while one waits for I/O, the CPU runs another, so the CPU is never idle |
| Multitasking | the CPU switches rapidly among tasks so that one user seems to run several programs at once |
| Multiprocessing | two or more CPUs in one computer execute tasks in parallel |
| Distributed | many networked computers cooperate and appear to the user as one system |

**4. Write any five features of a Windows GUI operating system. (5)**

1. Graphical interface of icons, windows, menus and a pointer.
2. Multitasking: several programs open at once.
3. Plug and play: new devices are detected and set up.
4. File Explorer for managing files and folders.
5. Control Panel and Settings for customising the desktop, devices, users and privacy.
6. Built-in tools and accessories (Notepad, Paint, Task Manager) and network and internet support.

**5. Differentiate between Windows and Linux. (5)**

| Windows | Linux |
|---|---|
| Proprietary (Microsoft); licence fee | Open source and free |
| Source code is closed | Source code can be read and modified |
| Mostly GUI | GUI and a powerful command line |
| Large amount of commercial software | Free software; choice of distributions |
| More targeted by viruses | Fewer virus attacks, strong permissions |

**6. What is a mobile operating system? Name two types and write two features. (1+2+2)**

A mobile operating system runs on smartphones and tablets and manages their hardware, touch screen, sensors and apps. Types: **Android** (Google, open source based on the Linux kernel) and **iOS** (Apple, closed, only on Apple devices). Other types: HarmonyOS and KaiOS. Features: touch interface, app stores, wireless connectivity, and battery and sensor management.

### Long questions (8 marks each)

**7. Explain Linux. State its features and name any three distributions. Compare it with UNIX. (3+3+2)**

Linux is a free, open-source, UNIX-like operating system whose kernel was written by Linus Torvalds in 1991 and is developed by a worldwide community.

Features: free and open source; multiuser and multitasking; secure, with file permissions; portable, running on many kinds of hardware; stable; has both a command line and a GUI.

Distributions: Ubuntu, Debian, Fedora, Red Hat Enterprise Linux, Linux Mint.

UNIX was developed at Bell Laboratories in the 1970s, is usually commercial and runs on specific hardware, while Linux is free; the two work in a similar way, with similar commands and directory structure.

**8. Explain the different categories of software with examples. (8)**

| Category | Purpose | Examples |
|---|---|---|
| System software | controls hardware and runs other software | Windows, Linux, device drivers, compilers |
| Utility software | maintains and protects the system | antivirus, disk cleanup, backup tools, WinRAR |
| Application software | does the user's work | MS Word, Excel, Tally, games, Photoshop |
| Web-based software | runs in a browser, no installation | Gmail, Google Docs, online banking |
| Mobile apps | built for phones and tablets | eSewa, WhatsApp, Daraz app |

Application software is further divided into general purpose (word processors) and specific purpose (payroll, hotel management). Add one line on each category explaining how it differs from the others.

## 15.5 Unit 4: Application Package

### Short questions (5 marks each)

**1. What is an office package? Explain its main components. (1+4)**

An office package is a bundle of application programs that handle the common tasks of an office.
- **Word processor** (MS Word): letters, reports and documents; formatting, tables, spell check, mail merge.
- **Spreadsheet** (MS Excel): data in rows and columns; formulas, functions, charts and what-if analysis.
- **Presentation tool** (MS PowerPoint): slides with text, pictures, sound, animation and transitions.
- **DBMS** (MS Access): stores related data in tables, with queries, forms and reports.

**2. Write short notes on a school management system and an inventory management system. (2.5+2.5)**

A *school management system* manages student admission, attendance, fee collection, timetable, examination marks, report cards and parents' communication, so that records are accurate and quickly found.

An *inventory management system* records goods bought, sold and in stock; it warns when an item is below the reorder level, prints invoices and prepares stock and sales reports for shops and warehouses.

**3. What is a payroll system? Write any four of its functions. (1+4)**

A payroll system is software that calculates the salaries of employees. Functions: (i) recording employee details and attendance, (ii) calculating basic pay, allowances and overtime, (iii) deducting tax, provident fund and loans, (iv) printing payslips, (v) producing salary reports and bank transfer lists.

**4. Write short notes on hotel management and weather forecasting systems. (2.5+2.5)**

A *hotel management system* handles room booking, check-in and check-out, billing, restaurant orders, housekeeping and reports.

A *weather forecasting system* collects data from satellites, radar and weather stations, and processes it with mathematical models on powerful computers to predict temperature, rainfall and storms.

### Long question (8 marks)

**5. Explain the use of a word processor, spreadsheet, presentation tool and database package in a school office. (2+2+2+2)**

- *Word processor*: notices, letters to guardians, certificates and the school magazine can be typed, formatted and printed; templates and mail merge send the same letter to many guardians.
- *Spreadsheet*: marks of students are entered in cells; formulas calculate totals, percentages and ranks (`=SUM(B2:F2)`); charts show the pass rate by class.
- *Presentation tool*: teachers and the principal prepare slides for lessons, parent meetings and annual reports.
- *Database package*: stores student, teacher and fee records in related tables so that queries, such as the list of students with unpaid fees, are answered quickly, and reports are printed.

## 15.6 Unit 5: Programming Concepts and Logics

### Short questions (5 marks each)

**1. Differentiate between low-level and high-level languages. (5)**

| Low-level language | High-level language |
|---|---|
| Machine language and assembly language | English-like language such as C, Python |
| Close to the hardware | Close to human language |
| Difficult to write and read | Easy to write and read |
| Machine dependent | Portable across machines |
| Needs an assembler (or none for machine code) | Needs a compiler or interpreter |

Fourth-generation languages (4GL), such as SQL, state *what* result is wanted rather than *how* to obtain it.

**2. Explain syntax, semantic and runtime errors with an example of each. (5)**

- **Syntax error**: a statement breaks the grammar rules of the language, so compilation fails. Example: `printf("Hi")` without the semicolon.
- **Semantic (logical) error**: the program is grammatical and runs but gives wrong results because the logic is wrong. Example: writing `area = l + b;` for the area of a rectangle.
- **Runtime error**: occurs while the program runs and usually stops it. Example: division by zero, `n / 0`.

**3. What is a control structure? Explain sequence, selection and iteration. (1+4)**

A control structure decides the order in which statements are executed.
- **Sequence**: statements are executed one after another in the order written.
- **Selection**: one of several paths is chosen on a condition (`if`, `if-else`, `switch`).
- **Iteration**: a block is repeated while a condition holds (`while`, `do-while`, `for`).

**4. Write an algorithm, pseudocode and describe the flowchart to find the area of a circle. (5)**

Algorithm: 1. Start. 2. Read the radius r. 3. Calculate area = 3.14159 x r x r. 4. Print area. 5. Stop.

Pseudocode:

```
BEGIN
  INPUT r
  area = 3.14159 * r * r
  OUTPUT area
END
```

Flowchart: an oval Start, a parallelogram "Input r", a rectangle "area = 3.14159 * r * r", a parallelogram "Print area" and an oval Stop, joined by arrows in that order.

**5. Write the difference between ASCII and Unicode, and explain BCD. (2.5+2.5)**

ASCII uses 7 bits (128 characters, extended ASCII 8 bits for 256) and covers English letters, digits and symbols; for example `A` is 65. Unicode uses up to 32 bits (UTF-8, UTF-16) and covers the characters of almost all the world's languages, including Devanagari, and emoji. ASCII is therefore a small subset of Unicode.

BCD (binary coded decimal) writes each decimal digit in its own 4-bit binary code, so $(59)_{10} = 0101\ 1001$ in BCD.

**6. List the basic data types of C with size, format specifier and an example. (5)**

| Type | Size (typical) | Specifier | Example |
|---|---|---|---|
| `int` | 4 bytes | `%d` | `int age = 17;` |
| `float` | 4 bytes | `%f` | `float pi = 3.14;` |
| `double` | 8 bytes | `%lf` | `double g = 9.80665;` |
| `char` | 1 byte | `%c` | `char grade = 'A';` |

**7. Explain the operators of C with examples. (5)**

- Arithmetic: `+ - * / %`, for example `7 % 3` is 1.
- Relational: `< > <= >= == !=`, giving 1 or 0.
- Logical: `&&`, `||`, `!`.
- Assignment: `=`, `+=`, `-=`, `*=`, `/=`.
- Unary: `++`, `--`, `-`; `i++` uses then increases, `++i` increases then uses.
- Conditional (ternary): `max = (a > b) ? a : b;`.

**8. Write a C program to find the largest of three numbers. (5)**

```
#include <stdio.h>
int main() {
    int a, b, c, max;
    printf("Enter three numbers: ");
    scanf("%d %d %d", &a, &b, &c);
    if (a >= b && a >= c)
        max = a;
    else if (b >= a && b >= c)
        max = b;
    else
        max = c;
    printf("Largest = %d\n", max);
    return 0;
}
```

Sample run: input `7 19 12` gives `Largest = 19`.

**9. Write a C program to display the factorial of a number. (5)**

```
#include <stdio.h>
int main() {
    int n, i, f = 1;
    printf("Enter a number: ");
    scanf("%d", &n);
    for (i = 1; i <= n; i++)
        f = f * i;
    printf("Factorial of %d = %d\n", n, f);
    return 0;
}
```

Sample run: input 5 gives `Factorial of 5 = 120`.

**10. Write a C program to display the following pattern. (5)**

```
1
1 2
1 2 3
1 2 3 4
```

```
#include <stdio.h>
int main() {
    int i, j;
    for (i = 1; i <= 4; i++) {
        for (j = 1; j <= i; j++)
            printf("%d ", j);
        printf("\n");
    }
    return 0;
}
```

The outer loop controls the rows and the inner loop prints the numbers 1 to the row number.

**11. Write a C program that gives a division from marks using if-else-if (80 and above Distinction, 60 and above First, 45 and above Second, 32 and above Pass, otherwise Fail). (5)**

```
#include <stdio.h>
int main() {
    int marks;
    printf("Enter marks: ");
    scanf("%d", &marks);
    if (marks >= 80)
        printf("Distinction\n");
    else if (marks >= 60)
        printf("First division\n");
    else if (marks >= 45)
        printf("Second division\n");
    else if (marks >= 32)
        printf("Pass\n");
    else
        printf("Fail\n");
    return 0;
}
```

Sample run: input 72 gives `First division`. Order matters: the largest limit must be tested first.

**12. Write a C program to make a simple calculator using switch. (5)**

```
#include <stdio.h>
int main() {
    float a, b;
    char op;
    printf("Enter number, operator, number: ");
    scanf("%f %c %f", &a, &op, &b);
    switch (op) {
        case '+': printf("Result = %.2f\n", a + b); break;
        case '-': printf("Result = %.2f\n", a - b); break;
        case '*': printf("Result = %.2f\n", a * b); break;
        case '/':
            if (b != 0)
                printf("Result = %.2f\n", a / b);
            else
                printf("Division by zero\n");
            break;
        default: printf("Invalid operator\n");
    }
    return 0;
}
```

Sample run: input `12 / 4` gives `Result = 3.00`.

**13. Write a C program to print the first n terms of the Fibonacci series. (5)**

```
#include <stdio.h>
int main() {
    int n, i, a = 0, b = 1, c;
    printf("How many terms? ");
    scanf("%d", &n);
    for (i = 1; i <= n; i++) {
        printf("%d ", a);
        c = a + b;
        a = b;
        b = c;
    }
    printf("\n");
    return 0;
}
```

Sample run: n = 8 gives `0 1 1 2 3 5 8 13`.

**14. Write a C program to read two words, find the length of the first, join them and compare them using string functions. (5)**

```
#include <stdio.h>
#include <string.h>
int main() {
    char s1[50], s2[50], s3[100];
    printf("Enter two words: ");
    scanf("%s %s", s1, s2);
    printf("Length of first = %d\n", (int)strlen(s1));
    strcpy(s3, s1);
    strcat(s3, s2);
    printf("Joined = %s\n", s3);
    if (strcmp(s1, s2) == 0)
        printf("Both words are equal\n");
    else
        printf("Words are different\n");
    return 0;
}
```

Sample run: input `nep al` gives length 3, joined `nepal`, and `Words are different`. `strcmp` returns 0 for equal strings.

### Long questions (8 marks each)

**15. Write a C program to read an integer, reverse it and check whether it is a palindrome. (8)**

```
#include <stdio.h>
int main() {
    int n, rev = 0, rem, orig;
    printf("Enter a number: ");
    scanf("%d", &n);
    orig = n;
    while (n > 0) {
        rem = n % 10;
        rev = rev * 10 + rem;
        n = n / 10;
    }
    printf("Reverse = %d\n", rev);
    if (orig == rev)
        printf("Palindrome\n");
    else
        printf("Not a palindrome\n");
    return 0;
}
```

Sample runs: 121 gives `Reverse = 121` and `Palindrome`; 1234 gives `Reverse = 4321` and `Not a palindrome`. The original number is saved in `orig` because `n` is destroyed by the loop.

**16. Write a C program to read a number and test whether it is prime. (8)**

```
#include <stdio.h>
int main() {
    int n, i, prime = 1;
    printf("Enter a number: ");
    scanf("%d", &n);
    if (n < 2)
        prime = 0;
    for (i = 2; i <= n / 2; i++) {
        if (n % i == 0) {
            prime = 0;
            break;
        }
    }
    if (prime)
        printf("%d is prime\n", n);
    else
        printf("%d is not prime\n", n);
    return 0;
}
```

Sample runs: 29 gives `29 is prime`; 15 gives `15 is not prime`. A number is prime if no integer from 2 to n/2 divides it.

**17. Write a C program to read n numbers into an array, then print the largest number and the average. (8)**

```
#include <stdio.h>
int main() {
    int a[50], n, i, max, sum = 0;
    printf("How many numbers? ");
    scanf("%d", &n);
    printf("Enter %d numbers: ", n);
    for (i = 0; i < n; i++) {
        scanf("%d", &a[i]);
        sum = sum + a[i];
    }
    max = a[0];
    for (i = 1; i < n; i++)
        if (a[i] > max)
            max = a[i];
    printf("Largest = %d\n", max);
    printf("Average = %.2f\n", (float)sum / n);
    return 0;
}
```

Sample run: n = 5 and the numbers `12 7 20 3 9` give `Largest = 20` and `Average = 10.20`. The cast `(float)` prevents integer division.

**18. Write a C program to add two 3 x 3 matrices. (8)**

```
#include <stdio.h>
int main() {
    int a[3][3], b[3][3], s[3][3], i, j;
    printf("Enter elements of first matrix:\n");
    for (i = 0; i < 3; i++)
        for (j = 0; j < 3; j++)
            scanf("%d", &a[i][j]);
    printf("Enter elements of second matrix:\n");
    for (i = 0; i < 3; i++)
        for (j = 0; j < 3; j++)
            scanf("%d", &b[i][j]);
    for (i = 0; i < 3; i++)
        for (j = 0; j < 3; j++)
            s[i][j] = a[i][j] + b[i][j];
    printf("Sum of the matrices:\n");
    for (i = 0; i < 3; i++) {
        for (j = 0; j < 3; j++)
            printf("%4d", s[i][j]);
        printf("\n");
    }
    return 0;
}
```

Sample run: first matrix 1 2 3 / 4 5 6 / 7 8 9 and second 9 8 7 / 6 5 4 / 3 2 1 give a sum matrix with every element equal to 10. For subtraction change `+` to `-` in the addition loop.

**19. Write a C program to read six numbers and arrange them in ascending order. (8)**

```
#include <stdio.h>
int main() {
    int a[6], n = 6, i, j, t;
    printf("Enter 6 numbers: ");
    for (i = 0; i < n; i++)
        scanf("%d", &a[i]);
    for (i = 0; i < n - 1; i++)
        for (j = 0; j < n - 1 - i; j++)
            if (a[j] > a[j + 1]) {
                t = a[j];
                a[j] = a[j + 1];
                a[j + 1] = t;
            }
    printf("Ascending order: ");
    for (i = 0; i < n; i++)
        printf("%d ", a[i]);
    printf("\n");
    return 0;
}
```

Sample run: `42 7 19 3 28 11` gives `Ascending order: 3 7 11 19 28 42`. This is bubble sort: neighbouring elements are swapped when out of order.

**20. Write a C program to read a word and check whether it is a palindrome. (8)**

```
#include <stdio.h>
#include <string.h>
int main() {
    char s[50];
    int i, n, flag = 1;
    printf("Enter a word: ");
    scanf("%s", s);
    n = strlen(s);
    for (i = 0; i < n / 2; i++) {
        if (s[i] != s[n - 1 - i]) {
            flag = 0;
            break;
        }
    }
    if (flag)
        printf("%s is a palindrome\n", s);
    else
        printf("%s is not a palindrome\n", s);
    return 0;
}
```

Sample run: `level` gives `level is a palindrome`. The loop compares the first character with the last, the second with the second last, and so on.

## 15.7 Unit 6: Web Technology I

### Short questions (5 marks each)

**1. What are a web browser and a search engine? Differentiate between them. (1+1+3)**

A web browser is software used to display web pages (Chrome, Firefox, Edge). A search engine is a website that searches an index of the web for pages that match the words typed (Google, Bing).

| Web browser | Search engine |
|---|---|
| Software installed on the device | A website with its own servers |
| Used to open and view web pages | Used to find web pages |
| Needs an address (URL) | Needs search words |
| Chrome, Firefox | Google, Bing |

**2. What is HTML? Differentiate between a tag and an attribute. (2+3)**

HTML (HyperText Markup Language) is the standard markup language used to structure web pages with tags. A *tag* is a keyword in angle brackets that tells the browser how to display content, such as `<p>`. An *attribute* gives extra information to a tag, written as name="value" inside the opening tag, such as `<body bgcolor="yellow">`. A tag says what the element is, an attribute describes how or where; attributes never appear in closing tags.

**3. Write the structure of an HTML document and explain its parts. (5)**

```
<!DOCTYPE html>
<html>
<head>
  <title>My Page</title>
</head>
<body>
  <h1>Welcome</h1>
  <p>This is my first page.</p>
</body>
</html>
```

`<html>` holds the whole document; `<head>` holds information not shown on the page, such as the title; `<title>` text appears on the browser tab; `<body>` holds the visible content. Save the file with the extension `.html` and open it in a browser.

**4. Write HTML code to produce an ordered list of three subjects that counts with capital letters, and an unordered list with square bullets. (5)**

```
<ol type="A">
  <li>Physics</li>
  <li>Chemistry</li>
  <li>Computer Science</li>
</ol>
<ul type="square">
  <li>Kathmandu</li>
  <li>Pokhara</li>
  <li>Biratnagar</li>
</ul>
```

`type="A"` gives A, B, C. A list can start from another number with `start="5"`.

**5. Write HTML code to create a table with a header row and two rows of student data. (5)**

```
<table border="1">
  <tr>
    <th>Roll</th>
    <th>Name</th>
    <th>Marks</th>
  </tr>
  <tr>
    <td>1</td>
    <td>Sita</td>
    <td>82</td>
  </tr>
  <tr>
    <td>2</td>
    <td>Ram</td>
    <td>76</td>
  </tr>
</table>
```

`<tr>` makes a row, `<th>` a bold centred header cell and `<td>` a data cell.

**6. Write the difference between inline, embedded and external CSS. (5)**

| Type | Where written | Scope |
|---|---|---|
| Inline | in the `style` attribute of one tag: `<p style="color:red">` | that one element |
| Embedded (internal) | in a `<style>` element in the `<head>` | the whole page |
| External | in a separate `.css` file linked with `<link rel="stylesheet" href="style.css">` | every page that links to it |

External CSS is best for a whole site because one file changes the look of every page.

**7. Differentiate between the canvas and svg elements of HTML5. (5)**

| `<canvas>` | `<svg>` |
|---|---|
| Pixel-based (raster) surface | Vector graphics written in markup |
| Drawn using JavaScript | Shapes written as elements: `<circle>`, `<rect>` |
| Loses quality on enlargement | Scales without loss |
| Good for games and fast animation | Good for logos, icons, charts |

**8. What is a domain name? Explain web hosting. (2.5+2.5)**

A domain name is the human-readable name of a website, such as `nebians.consica.com.np`, which the DNS translates into the IP address of the server. A top-level part such as `.np` or `.com` shows the country or type.

Web hosting is a service in which a company provides space and connectivity on a server so that a website's files are available on the internet all day. Types are shared, dedicated and cloud hosting.

### Long questions (8 marks each)

**9. Write HTML code to create a web page that has the page title "Admission Form", a heading, a paragraph, and a form with name (text box), gender (radio buttons), subjects (check boxes), address (text area) and a submit button. (8)**

```
<!DOCTYPE html>
<html>
<head>
  <title>Admission Form</title>
</head>
<body bgcolor="lightyellow">
  <h1 align="center">Admission Form</h1>
  <p>Please fill in the details below.</p>
  <form>
    Name: <input type="text" name="fullname"><br><br>
    Gender:
    <input type="radio" name="gender" value="male"> Male
    <input type="radio" name="gender" value="female"> Female<br><br>
    Subjects:
    <input type="checkbox" name="sub" value="physics"> Physics
    <input type="checkbox" name="sub" value="cs"> Computer Science<br><br>
    Address:<br>
    <textarea name="address" rows="3" cols="30"></textarea><br><br>
    <input type="submit" value="Submit">
  </form>
</body>
</html>
```

Points the examiner checks: the radio buttons share one `name` so that only one can be chosen; check boxes allow several; `<textarea>` has a closing tag; `<input>` has none.

**10. Write HTML code to create a page containing an image that is also a hyperlink to another page, a link to an e-mail address, a paragraph with the formatting tags bold, italic, underline, superscript and subscript, and a video. (8)**

```
<html>
<head>
  <title>Links and Media</title>
</head>
<body>
  <a href="home.html"><img src="logo.png" alt="Logo" width="100"></a>
  <p>Contact us: <a href="mailto:info@example.com">info@example.com</a></p>
  <p>
    <b>Bold</b>, <i>italic</i>, <u>underline</u>,
    x<sup>2</sup> and H<sub>2</sub>O.
  </p>
  <video src="lesson.mp4" width="320" height="240" controls>
    Your browser does not support video.
  </video>
</body>
</html>
```

The `<img>` tag placed inside `<a>` makes the picture clickable; `controls` gives play and pause buttons; the text between `<video>` tags shows only in browsers that cannot play video.

**11. Explain the features of a content management system and name any three. (3+3+2)**

A CMS is software that lets people create, edit, organise and publish web content without writing code, through a browser-based dashboard. Features: ready themes and templates; user roles and permissions; media library; plug-ins and extensions; search engine optimisation tools; versioning and scheduling of posts. Examples: WordPress, Joomla, Drupal.

## 15.8 Unit 7: Multimedia

### Short questions (5 marks each)

**1. What is multimedia? Explain any four of its components. (1+4)**

Multimedia is the combination of text, graphics, audio, video and animation delivered through a computer or digital device.
- **Text**: words, the basis of all information (titles, captions, articles).
- **Graphics**: still images such as drawings, photographs and charts (JPEG, PNG).
- **Audio**: sound, music and voice (MP3, WAV).
- **Video**: moving recorded images with sound (MP4).
- **Animation**: drawn or computer-made pictures shown in sequence to create motion (GIF, Flash-type animation).

**2. Write any five applications of multimedia. (5)**

1. Education: e-learning, virtual classrooms, simulations.
2. Entertainment: films, games, music and streaming.
3. Business: presentations, advertisements, product demonstrations.
4. Medicine: 3D models of organs and training simulators.
5. Journalism and public information: online news with video and infographics.
6. Tourism: virtual tours of places such as Pashupatinath or Lumbini.

**3. Differentiate between linear and interactive multimedia. (5)**

| Linear multimedia | Interactive multimedia |
|---|---|
| Content plays from start to end in a fixed order | The user controls what comes next |
| No navigation by the user | Menus, buttons and links |
| A film or a presentation | An educational game or a website |

### Long question (8 marks)

**4. Explain the components of multimedia and discuss its applications in education. (4+4)**

Write the five components as in question 1, with a file format for each. For education: (i) animations and video explain difficult ideas such as the working of the heart; (ii) audio helps language learning; (iii) interactive quizzes give instant feedback; (iv) virtual laboratories allow experiments that are costly or dangerous; (v) e-learning lets students study from any place and at their own speed; (vi) text and graphics combine in digital books and presentations that improve understanding and memory.

## 15.9 Unit 8: Information Security and Cyber Law

### Short questions (5 marks each)

**1. What is cybercrime? Write any four examples. (1+4)**

Cybercrime is a crime that is committed using a computer or network, or that is aimed at a computer or network. Examples: (i) **hacking**, unauthorised access to a system, (ii) **phishing**, fake messages or sites that steal passwords, (iii) **identity theft**, (iv) **cyberbullying**, harassing a person online, (v) **online fraud and piracy**, (vi) **denial of service**, flooding a server so that it stops working.

**2. Differentiate between a virus, a worm and a Trojan horse. (5)**

| Virus | Worm | Trojan horse |
|---|---|---|
| Attaches to a host file or program | Stand-alone program | Appears to be a useful program |
| Spreads when the infected file is run or shared | Spreads by itself across networks | Does not replicate; the user installs it |
| Corrupts files and slows the system | Uses bandwidth and resources | Steals data, opens a back door |

**3. What is spam? How can you protect yourself from cybercrime? (1+4)**

Spam is unwanted bulk electronic mail, usually advertising or carrying harmful links.

Protection: (i) use strong, different passwords and two-factor authentication, (ii) install antivirus and a firewall and keep software updated, (iii) do not click unknown links or open unknown attachments, (iv) take backups regularly, (v) share personal information carefully and check that a site begins with https.

**4. What is intellectual property right? Explain copyright, patent and trademark. (1+4)**

Intellectual property rights are the legal rights over creations of the mind. **Copyright** protects original works such as books, music and software code. **Patent** gives an inventor the sole right to make and sell an invention for a fixed time. **Trademark** protects the name, logo or sign that identifies a product or business.

**5. What is a digital signature? Why is it used? (2+3)**

A digital signature is an electronic code created with the sender's private key and attached to a message or document to prove who sent it. It is used for (i) authentication, confirming the sender, (ii) integrity, showing the message was not changed, and (iii) non-repudiation, so the sender cannot deny sending it. The receiver checks it with the sender's public key.

**6. Write short notes on the Electronic Transactions Act, 2063 of Nepal. (5)**

It is Nepal's principal cyber law, passed in 2063 BS. It gives legal recognition to electronic records and digital signatures, regulates certifying authorities, and defines computer-related offences. Offences include pirating or altering computer source code, unauthorised access, damaging a computer system and publishing illegal material in electronic form; punishments are fines or imprisonment or both. Cases go to the Information Technology Tribunal.

### Long questions (8 marks each)

**7. What is information security? Explain the measures taken to protect information. (2+6)**

Information security is the protection of information from unauthorised access, change, loss or destruction, so that it stays confidential, correct and available.

Measures: (i) **authentication** by passwords, PINs, biometrics and OTP; (ii) **authorisation** with access rights per user; (iii) **encryption**, scrambling data so that only key holders can read it; (iv) **firewall** to filter traffic; (v) **antivirus** and regular updates; (vi) **backup** of data in a second place; (vii) **physical security**: locked server rooms and CCTV; (viii) user education on phishing and safe use.

**8. Explain computer ethics and the digital society. Give any six rules of good computer ethics. (2+6)**

A digital society is a community in which communication, business, learning and government work through digital technology. Computer ethics is the set of moral rules for the proper use of computers and the internet.

Rules: (i) do not use another person's account or password, (ii) do not copy or sell pirated software, (iii) do not spread viruses or rumours, (iv) respect the privacy of others and never read their private files, (v) do not use the computer to harm, bully or cheat, (vi) acknowledge the source of any information you use, (vii) use resources such as the school network responsibly.

**9. Discuss the ICT policy of Nepal and the role of the Electronic Transactions Act. (4+4)**

The National Information and Communication Technology Policy, 2015 aims to make Nepal an information and knowledge-based society and economy. Main aims: affordable broadband for all, ICT in every school, services of the government delivered online, growth of the IT industry, security for networks and data, and closing the digital divide between town and village. The Digital Nepal Framework is the programme used to carry it out in sectors such as education, health, agriculture and finance.

The Electronic Transactions Act, 2063 provides the legal base: it makes digital signatures and electronic records valid, allows government to work electronically, and punishes cybercrime, for example hacking and the publication of illegal material. Together the policy gives direction and the Act gives legal force, but the Act is old and needs updating for social media and data protection.

## Chapter summary

- Group B is 5 x 5 = 25 marks and Group C is 2 x 8 = 16 marks; the two C programs are the most predictable use of an 8-mark slot.
- For every program: header, declarations, `scanf` with `&`, the logic, the output with `printf`, and `return 0`.
- Number-system questions are won by showing the working: division by 2 for binary, groups of 3 or 4 bits for octal and hexadecimal, complement then add for subtraction.
- Truth-table proofs need every row and a closing sentence saying the two columns are equal.
- A "differentiate" answer is a table of at least five contrasts; a "define and explain" answer is the definition plus four points.
- HTML answers need correct nesting and closing tags: `<br>`, `<img>` and `<input>` have none; radio buttons share one `name`.
- Security answers should name examples: virus, worm, Trojan, phishing, ransomware, and the Electronic Transactions Act, 2063.

## Practice questions

**Group A: Multiple choice (1 mark each)**

1. Which part of the CPU directs the operation of the other units? <span class="marks">[1]</span>
   (a) ALU (b) control unit (c) cache (d) register
2. In a C `for` loop, which part is executed once, at the beginning? <span class="marks">[1]</span>
   (a) initialisation (b) condition (c) increment (d) body
3. Which tag creates a line break in HTML? <span class="marks">[1]</span>
   (a) `<lb>` (b) `<br>` (c) `<break>` (d) `<newline>`
4. Which of the following is an example of a patent? <span class="marks">[1]</span>
   (a) exclusive right to make a new invention (b) a company logo (c) a song's lyrics (d) a domain name

::: note Answers to Group A
**1.** (b) — the control unit fetches, decodes and directs.
**2.** (a) — initialisation runs once; the condition runs before each pass.
**3.** (b) — `<br>` is the break tag.
**4.** (a) — a patent protects an invention.
:::

**Group B: Short answer (5 marks each)**

1. Differentiate between 1's complement and 2's complement. <span class="marks">[5]</span>
2. Write the differences between compiler and interpreter. <span class="marks">[5]</span>
3. Write a C program to print the multiplication table of a number up to 10. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** The 1's complement inverts every bit; the 2's complement is the 1's complement plus 1. The 1's complement has two zeros (+0 and -0) while the 2's complement has one. In subtraction the 1's complement needs an end-around carry; the 2's complement just discards the carry. The 2's complement is therefore the one used inside modern computers.

**2.** Compiler: translates the whole program at once; reports all errors after translation; faster execution; the object code is saved; C and C++. Interpreter: translates and executes line by line; stops at the first error; slower execution; no object code is produced; Python and BASIC.

**3.**

```
#include <stdio.h>
int main() {
    int n, i;
    printf("Enter a number: ");
    scanf("%d", &n);
    for (i = 1; i <= 10; i++)
        printf("%d x %d = %d\n", n, i, n * i);
    return 0;
}
```

For n = 7 the first line is `7 x 1 = 7` and the last is `7 x 10 = 70`.
:::

**Group C: Long answer (8 marks each)**

1. Write HTML code to display a page that has your name as the title and heading, a table of three subjects with their marks, and a link to `https://www.nebians.consica.com.np`. <span class="marks">[8]</span>

::: note Answer to Group C
**1.**

```
<html>
<head>
  <title>Sita Sharma</title>
</head>
<body>
  <h1>Sita Sharma</h1>
  <table border="1">
    <tr><th>Subject</th><th>Marks</th></tr>
    <tr><td>Physics</td><td>78</td></tr>
    <tr><td>Chemistry</td><td>81</td></tr>
    <tr><td>Computer Science</td><td>44</td></tr>
  </table>
  <p><a href="https://www.nebians.consica.com.np">Visit NEBians</a></p>
</body>
</html>
```

Marks are for the document structure, the title, the heading, the table with `<th>`, correctly closed rows and cells, and the `href` attribute in quotes.
:::
