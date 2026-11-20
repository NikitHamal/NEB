---
subject: Question Bank
grade: 8
unit: 23
title: "Computer Science: Unit-wise Objective Question Bank"
hours: 0
area: Computer Science
---

Computer Science in grade 8 is examined by your own school, in a written paper of 50 marks and two hours, beside the practical work in the lab. Group A of that paper is **ten one-mark objective items**. They are the quickest marks in the paper and the easiest to lose: a full form remembered wrongly, a hub confused with a switch, a binary number read from the wrong end, a Python `%` remainder operator worked out as a division. This chapter drills those items lesson by lesson for all twenty lessons of the Computer Science 8 book, in the same order as the book.

Each section opens with a **facts line** — the few facts that the items of that lesson actually use. Then come eight to ten items, and then a key that gives each answer with a one-line reason. Work an item in under a minute, check it in ten seconds, and move on. The reasons matter more than the letters: a reason you can repeat is a mark you will not lose next time.

::: key The 50-mark paper used in this bank
| Group | Items | Marks each | Total | What it tests |
|---|---|---|---|---|
| A | 10 | 1 | 10 | one fact, a full form, a short calculation or the output of one line of code |
| B | 10 | 2 | 20 | a definition with an example, two differences, a short program or a few steps |
| C | 5 | 4 | 20 | a full explanation, a diagram, a longer program or HTML page, or a scenario |
| **Total** | **25** | | **50** | 2 hours |

There is no national specification grid for this school paper. The weights in the chart below are the ones this bank uses for its model papers (chapter 25). The six lessons on computer fundamentals carry 14 marks, the three on application software 8, the five on the web, communication and society 13, number system, graphics and multimedia 5, and the three on programming 10.
:::

::: caution Practice items, not past questions
Every item below is an original **practice** item written to the pattern above and to the lessons of the Computer Science 8 book. None is claimed to come from any school's paper. Every calculation, conversion and Python result was worked out independently before it was written down.
:::

```figure caption="Marks per lesson in the 50-mark paper used in this bank. Python programming and web page design carry the most; the six lessons on computer fundamentals together carry 14 marks, so no area can be skipped."
fig, ax = barh_ranked(
    ["Computer Programming using Python", "Web Page Design", "Fundamentals of Computer", "History of Computer",
     "Word Processing", "Spreadsheet Software", "Computer Network", "Number System", "Program Design Tools",
     "Generations of Computer", "Types of Computer", "Computer Software", "Operating System",
     "Presentation Software", "Information and Communication Technology", "Computer Ethics and Cyber Law",
     "Computer Virus", "Fundamentals of Computer Programming", "Computer Graphics", "Multimedia"],
    [5, 4, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1], unit=" marks", figsize=(5.2, 4.6),
    highlight={"Computer Programming using Python", "Web Page Design"})
ax.tick_params(axis="y", labelsize=7.4)
for t in ax.texts:
    if t.get_text() == "1 marks":
        t.set_text("1 mark")
```

## 23.1 Fundamentals of Computer

**Facts.** A computer accepts data, processes it under a program, stores it and gives information (Latin *computare*, to calculate). **Data** are raw facts; **information** is processed data. **Hardware** can be touched; **software** is a set of programs. IPOS: input → CPU (**control unit** directs, **ALU** calculates and compares) → output, with storage (**RAM** temporary; hard disk, SSD, pen drive permanent). Characteristics: speed (ms, μs, ns), accuracy (**GIGO**), diligence, versatility, storage, automation. 1 KB = 1024 bytes; 1 GB = 1024 MB.

1. Processed, meaningful data is called <span class="marks">[1]</span>
   (a) data (b) information (c) an instruction (d) a program
2. Which part of the CPU compares two marks to find the larger? <span class="marks">[1]</span>
   (a) control unit (b) arithmetic logic unit (c) RAM (d) hard disk
3. A teacher typed 29 instead of 92, so a student's percentage came out wrong. This illustrates <span class="marks">[1]</span>
   (a) diligence (b) GIGO (c) versatility (d) automation
4. Which device is both an input and an output device? <span class="marks">[1]</span>
   (a) scanner (b) printer (c) touch screen (d) speaker
5. A computer prints 5,000 admit cards with the same quality from the first to the last. This shows its <span class="marks">[1]</span>
   (a) diligence (b) storage (c) versatility (d) automation
6. Which memory loses its contents when the power goes off? <span class="marks">[1]</span>
   (a) ROM (b) hard disk (c) RAM (d) pen drive
7. How many 4 MB photos can a 32 GB memory card hold, taking 1 GB = 1024 MB? <span class="marks">[1]</span>
   (a) 8,000 (b) 8,192 (c) 4,096 (d) 1,024
8. The Nagarik App is an example of computers used in <span class="marks">[1]</span>
   (a) agriculture (b) government services (c) entertainment (d) weather forecasting

::: note Answers to 23.1
**1.** (b) — data become information only after processing.
**2.** (b) — comparing is a logical operation, done by the ALU.
**3.** (b) — Garbage In, Garbage Out: wrong input gives wrong output.
**4.** (c) — it senses touch (input) and shows pictures (output).
**5.** (a) — working on without tiring or losing quality is diligence.
**6.** (c) — RAM is temporary; the others keep data without power.
**7.** (b) — 32 × 1024 = 32,768 MB, and 32,768 ÷ 4 = 8,192.
**8.** (b) — citizens keep records and use government services in it.
:::

## 23.2 History of Computer

**Facts.** Abacus: counting boards c. 2700 BC; on a suanpan a heaven bead = 5 and an earth bead = 1. Napier's bones (1617): multiplication. Slide rule (Oughtred, c. 1622): analog. Pascaline (Pascal, 1642): add and subtract, automatic carry. Stepped reckoner (Leibniz, 1673): all four operations. Jacquard loom (1804): punched cards. Babbage: Difference Engine (1822), Analytical Engine (1834) with **mill** (processor) and **store** (memory) — father of the computer; Ada Lovelace: first programmer (1843). Hollerith's tabulator: 1890 US census → IBM (1924). Mark I (1944): electromechanical. ABC (1942): first electronic digital. ENIAC (1946): first general-purpose electronic, 17,468 tubes. EDVAC: stored program. UNIVAC I (1951): first commercial computer in the USA. Nepal: IBM 1401 rented in 2028 BS for the census; ICL 2950/10 in 2038 BS.

1. On a Chinese abacus, the ones rod shows one heaven bead and three earth beads at the beam. The digit is <span class="marks">[1]</span>
   (a) 4 (b) 8 (c) 6 (d) 15
2. Numbered rods that made multiplication easy were invented by <span class="marks">[1]</span>
   (a) Blaise Pascal (b) John Napier (c) Leibniz (d) Jacquard
3. The machine with a stepped drum that could add, subtract, multiply and divide was the <span class="marks">[1]</span>
   (a) Pascaline (b) stepped reckoner (c) abacus (d) slide rule
4. In the Analytical Engine, the "mill" did the work of today's <span class="marks">[1]</span>
   (a) memory (b) CPU (c) printer (d) keyboard
5. Punched cards were first used to control a <span class="marks">[1]</span>
   (a) tabulating machine (b) loom for weaving (c) Pascaline (d) slide rule
6. Which of these was electromechanical? <span class="marks">[1]</span>
   (a) ENIAC (b) Harvard Mark I (c) UNIVAC I (d) ABC
7. The first commercial computer made in the USA was <span class="marks">[1]</span>
   (a) ENIAC (b) EDVAC (c) UNIVAC I (d) Mark I
8. Nepal's first computer, rented for the census of 2028 BS, was the <span class="marks">[1]</span>
   (a) ICL 2950/10 (b) IBM 1401 (c) Apple II (d) UNIVAC I

::: note Answers to 23.2
**1.** (b) — 5 + 1 + 1 + 1 = 8.
**2.** (b) — Napier's bones, 1617.
**3.** (b) — Leibniz's stepped reckoner, 1673; the Pascaline only added and subtracted.
**4.** (b) — the mill did the arithmetic; the store was the memory.
**5.** (b) — Jacquard's loom of 1804; Hollerith borrowed the idea later.
**6.** (b) — relays and a rotating shaft; the others were electronic.
**7.** (c) — the first was accepted by the US Census Bureau in 1951.
**8.** (b) — a second-generation computer rented at Rs 1,25,000 a month.
:::

## 23.3 Generations of Computer

**Facts.** A generation is a stage marked by a new main component. 1st (1946–1958): **vacuum tubes**, machine language, milliseconds — ENIAC, UNIVAC I. 2nd (1958–1964): **transistors** (Bell Labs, 1947), assembly, FORTRAN, COBOL, microseconds — IBM 1401. 3rd (1964–1975): **integrated circuits** (Kilby, 1958), keyboards and monitors, time-sharing, nanoseconds. 4th (1975–): **microprocessors** (Intel 4004, 1971, 2,300 transistors), PCs, GUI, Internet. 5th: **artificial intelligence** and **parallel processing**. VLSI = Very Large Scale Integration. Moore's law: transistors double about every two years.

1. The main component of second-generation computers was the <span class="marks">[1]</span>
   (a) vacuum tube (b) transistor (c) integrated circuit (d) microprocessor
2. ENIAC belongs to the <span class="marks">[1]</span>
   (a) first generation (b) second generation (c) third generation (d) fourth generation
3. Many transistors, resistors and capacitors made on one small piece of silicon form <span class="marks">[1]</span>
   (a) a vacuum tube (b) an integrated circuit (c) a relay (d) a punched card
4. The Intel 4004 of 1971 was the first <span class="marks">[1]</span>
   (a) transistor (b) integrated circuit (c) microprocessor (d) supercomputer
5. Operations measured in microseconds are typical of the <span class="marks">[1]</span>
   (a) first generation (b) second generation (c) third generation (d) fifth generation
6. Understanding natural language and learning from data are aims of the <span class="marks">[1]</span>
   (a) second generation (b) third generation (c) fourth generation (d) fifth generation
7. VLSI stands for <span class="marks">[1]</span>
   (a) Very Large Scale Integration (b) Very Long Silicon Instruction (c) Visual Large Scale Interface (d) Very Low Speed Integration
8. A chip has 1 million transistors. If the number doubles every two years, after four years it is expected to have <span class="marks">[1]</span>
   (a) 2 million (b) 4 million (c) 8 million (d) 16 million

::: note Answers to 23.3
**1.** (b) — transistors replaced vacuum tubes.
**2.** (a) — it used about 17,468 vacuum tubes.
**3.** (b) — an integrated circuit, or chip.
**4.** (c) — a whole CPU on one chip.
**5.** (b) — 1st milliseconds, 2nd microseconds, 3rd nanoseconds.
**6.** (d) — the fifth generation is about AI.
**7.** (a) — Very Large Scale Integration.
**8.** (b) — four years is two doublings: 1 → 2 → 4 million.
:::

## 23.4 Types of Computer

**Facts.** **Analog** computers measure continuous data (speedometer with a needle, mercury thermometer, slide rule); **digital** computers count discrete data in 0s and 1s; **hybrid** computers do both (ECG, ICU monitor, petrol-pump dispenser). By size: **supercomputer** (fastest, measured in **FLOPS**; weather, research), **mainframe** (thousands of users; banks, airlines), **minicomputer** (tens to hundreds of users; PDP-11), **microcomputer** (one user, microprocessor). Microcomputers: desktop, laptop, tablet, smartphone, **workstation** (3D design, video). **General-purpose** computers run many programs; **special-purpose** (embedded) ones do one job.

1. A car's speedometer with a moving needle works as <span class="marks">[1]</span>
   (a) a digital computer (b) an analog computer (c) a hybrid computer (d) a mainframe
2. A petrol-pump dispenser measures the flow of fuel and shows litres and rupees as numbers. It is <span class="marks">[1]</span>
   (a) analog (b) digital (c) hybrid (d) a supercomputer
3. The speed of a supercomputer is measured in <span class="marks">[1]</span>
   (a) bps (b) FLOPS (c) dpi (d) rpm
4. A bank's central computer that serves thousands of users at once is a <span class="marks">[1]</span>
   (a) microcomputer (b) minicomputer (c) mainframe (d) analog computer
5. An architect needs one powerful computer for 3D models. The best choice is a <span class="marks">[1]</span>
   (a) workstation (b) tablet (c) mainframe (d) embedded computer
6. The computer inside a washing machine is <span class="marks">[1]</span>
   (a) general-purpose (b) special-purpose (c) a supercomputer (d) a mainframe
7. Forecasting the monsoon over South Asia needs a <span class="marks">[1]</span>
   (a) smartphone (b) supercomputer (c) minicomputer (d) analog computer
8. A smartphone is a kind of <span class="marks">[1]</span>
   (a) mainframe (b) microcomputer (c) analog computer (d) minicomputer

::: note Answers to 23.4
**1.** (b) — the needle moves smoothly; it measures.
**2.** (c) — analog measuring, digital calculating.
**3.** (b) — floating-point operations per second.
**4.** (c) — mainframes serve thousands of users reliably.
**5.** (a) — a fast single-user machine with a strong graphics card.
**6.** (b) — it does one job all its life (an embedded system).
**7.** (b) — huge parallel calculations need a supercomputer.
**8.** (b) — one user, one microprocessor.
:::

## 23.5 Computer Software

**Facts.** **System software** runs the computer: operating system, **device drivers** (one per device), **utility programs** (antivirus, backup, compression, disk cleanup) and **language processors** (assembler; **compiler** — whole program at once; **interpreter** — line by line, stops at the first error). **Application software** does the user's work: **packaged** (made for many users — Word, Chrome, VLC) or **tailor-made** (for one organisation). Licences: **proprietary** (buy; code secret), **freeware** (free; code secret), **shareware** (free trial, then pay), **open source** (code open to change and share). Remove programs with **Uninstall**.

1. A program that lets the operating system control a scanner is a <span class="marks">[1]</span>
   (a) utility (b) device driver (c) compiler (d) game
2. 7-Zip, which compresses files, is <span class="marks">[1]</span>
   (a) application software (b) utility software (c) an operating system (d) a device driver
3. A translator that runs a program one line at a time and stops at the first error is <span class="marks">[1]</span>
   (a) a compiler (b) an interpreter (c) an assembler (d) a driver
4. Software written for one hospital's own billing and records is <span class="marks">[1]</span>
   (a) packaged (b) tailor-made (c) freeware (d) shareware
5. Software that may be used free for 30 days and must then be bought is <span class="marks">[1]</span>
   (a) freeware (b) shareware (c) open source (d) firmware
6. Software whose source code anyone may read, change and share is <span class="marks">[1]</span>
   (a) proprietary (b) freeware (c) open source (d) shareware
7. Which of these is proprietary software? <span class="marks">[1]</span>
   (a) LibreOffice (b) Linux (c) Microsoft Windows (d) Firefox
8. The safe way to remove a program from Windows 11 is to <span class="marks">[1]</span>
   (a) delete its desktop icon (b) use Settings → Apps → Installed apps → Uninstall (c) delete its folder (d) empty the Recycle Bin

::: note Answers to 23.5
**1.** (b) — each device needs its own driver.
**2.** (b) — it maintains files, so it is a utility.
**3.** (b) — an interpreter works line by line.
**4.** (b) — made for one organisation's own needs.
**5.** (b) — try before you buy.
**6.** (c) — open source.
**7.** (c) — Windows must be licensed; the others are open source.
**8.** (b) — deleting icons or folders leaves the program or breaks it.
:::

## 23.6 Operating System

**Facts.** The OS manages hardware and software and gives the user interface: process (multitasking), memory, file and device management, security, user interface. **Single-user** vs **multi-user**; **CUI** (typed commands — MS-DOS, Linux terminal) vs **GUI** (windows, icons, menus); **desktop** (Windows, macOS, Linux) vs **mobile** (Android, iOS). Linux: Linus Torvalds, 1991, open source; Android: Google, built on Linux. Dialog box: **option button** chooses one, **check boxes** several. Path: `D:\School\Grade 8\file.docx`. Copy: Ctrl + C, Ctrl + V; move: Ctrl + X, Ctrl + V; rename: F2. Shift + Delete and pen-drive deletions skip the **Recycle Bin**. Settings: Win + I; Nepal's time zone UTC+05:45.

1. Running a song while typing in Word is handled by the OS's <span class="marks">[1]</span>
   (a) file management (b) process management (c) security (d) device management
2. MS-DOS has <span class="marks">[1]</span>
   (a) a GUI (b) a CUI (c) a touch interface (d) a voice interface
3. Linux was created by <span class="marks">[1]</span>
   (a) Bill Gates (b) Linus Torvalds (c) Steve Jobs (d) Tim Berners-Lee
4. In a dialog box, the control that allows only one choice from a group is the <span class="marks">[1]</span>
   (a) check box (b) option button (c) text box (d) spin box
5. For the file `D:\School\Grade 8\notes.txt`, the folder that directly contains it is <span class="marks">[1]</span>
   (a) D: (b) School (c) Grade 8 (d) notes
6. Pressing Ctrl + X and then Ctrl + V on a file <span class="marks">[1]</span>
   (a) copies it (b) moves it (c) renames it (d) deletes it
7. A file deleted from a pen drive <span class="marks">[1]</span>
   (a) goes to the Recycle Bin (b) is deleted permanently (c) moves to Documents (d) is hidden
8. The shortcut that opens Windows Settings is <span class="marks">[1]</span>
   (a) Win + E (b) Win + I (c) Win + D (d) Alt + F4

::: note Answers to 23.6
**1.** (b) — sharing the CPU among programs is process management.
**2.** (b) — commands are typed.
**3.** (b) — in 1991, as open source.
**4.** (b) — option (radio) buttons; check boxes allow several.
**5.** (c) — the last folder before the file name.
**6.** (b) — cut and paste moves.
**7.** (b) — removable drives have no Recycle Bin.
**8.** (b) — Win + E opens File Explorer, Win + D the desktop.
:::

## 23.7 Word Processing

**Facts.** Word processors: Microsoft Word (.docx), LibreOffice Writer (.odt), Google Docs. Save Ctrl + S; Save As F12 (a new copy); Print Ctrl + P (pages `1-3, 6`); Undo Ctrl + Z, Redo Ctrl + Y; Cut, Copy, Paste Ctrl + X, C, V; Find Ctrl + F, Replace Ctrl + H; spelling F7; Bold, Italic, Underline Ctrl + B, I, U; Left, Centre, Right, Justify Ctrl + L, E, R, J. Header at the top, footer at the bottom; Insert → Page Number. Table cells = rows × columns; merging k cells into one removes k − 1. Wrap Text: In Line, Square, Tight, Top and Bottom, Behind, In Front. WordArt (Writer: Fontwork). Mail merge (Mailings tab) = main document + data source → one copy per row.

1. Which of these is **not** a word processor? <span class="marks">[1]</span>
   (a) Microsoft Word (b) LibreOffice Writer (c) Google Docs (d) Microsoft Excel
2. Ctrl + J applies <span class="marks">[1]</span>
   (a) justified alignment (b) bold (c) a new page (d) underline
3. To keep the original file and save a changed copy under a new name, use <span class="marks">[1]</span>
   (a) Save (b) Save As (c) Print (d) Close
4. Printing with **Pages:** `3-5, 8` prints how many pages of each copy? <span class="marks">[1]</span>
   (a) 3 (b) 4 (c) 5 (d) 8
5. Text that repeats at the bottom of every page is the <span class="marks">[1]</span>
   (a) header (b) footer (c) margin (d) caption
6. A table has 4 columns and 5 rows. After the 4 cells of the top row are merged, it has <span class="marks">[1]</span>
   (a) 17 cells (b) 20 cells (c) 16 cells (d) 19 cells
7. The Start Mail Merge command is on the <span class="marks">[1]</span>
   (a) Insert tab (b) Mailings tab (c) References tab (d) Review tab
8. Text flows around the rectangular box of a picture with the wrapping option <span class="marks">[1]</span>
   (a) In Line with Text (b) Square (c) Behind Text (d) Top and Bottom

::: note Answers to 23.7
**1.** (d) — Excel is a spreadsheet.
**2.** (a) — L, E, R, J are left, centre, right, justify.
**3.** (b) — Save As makes a new copy; Save overwrites.
**4.** (b) — pages 3, 4, 5 and 8.
**5.** (b) — the footer; the header is at the top.
**6.** (a) — 4 × 5 = 20, and merging 4 cells into 1 leaves 20 − 3 = 17.
**7.** (b) — Mailings → Start Mail Merge.
**8.** (b) — Square wraps around the box; Tight follows the outline.
:::

## 23.8 Spreadsheet Software

**Facts.** A workbook holds worksheets; a cell address is column + row (C5); a range B2:E6 has columns × rows cells. Formulas begin with `=`; brackets first, then `^`, then `*` and `/`, then `+` and `-`. Relative references (B2) change when copied; absolute ones (`$B$1`) do not. `SUM`, `AVERAGE`, `MAX`, `MIN`, `COUNT` (numbers only), `IF(condition, if_true, if_false)`. `#####` means the column is too narrow. **Sort** reorders rows; **filter** hides rows that do not match. Charts: column and bar compare items, **line** shows change over time, **pie** shows parts of a whole (angle = share × 360°).

1. How many cells are in the range A2:C6? <span class="marks">[1]</span>
   (a) 10 (b) 12 (c) 15 (d) 18
2. The result of `=20-8/4` is <span class="marks">[1]</span>
   (a) 3 (b) 18 (c) 12 (d) 2
3. A1:A4 hold 10, 15, 20 and 35. The result of `=AVERAGE(A1:A4)` is <span class="marks">[1]</span>
   (a) 20 (b) 80 (c) 35 (d) 4
4. B1:B5 hold 12, Absent, 9, 15 and 8. The result of `=COUNT(B1:B5)` is <span class="marks">[1]</span>
   (a) 5 (b) 4 (c) 44 (d) 1
5. C2 holds 40. The formula `=IF(C2>=40,"Pass","Fail")` shows <span class="marks">[1]</span>
   (a) Pass (b) Fail (c) TRUE (d) 40
6. The formula `=B2*$E$1` in C2 is copied to C3. In C3 it becomes <span class="marks">[1]</span>
   (a) `=B3*$E$1` (b) `=B3*$E$2` (c) `=B2*$E$1` (d) `=C3*$F$1`
7. To show only the rows in which Science is 60 or more, use <span class="marks">[1]</span>
   (a) Sort (b) Filter (c) Merge & Center (d) AutoFill
8. The best chart for Pokhara's temperature in each month of a year is a <span class="marks">[1]</span>
   (a) pie chart (b) line chart (c) table (d) WordArt
9. A cell shows `#####`. The reason is that <span class="marks">[1]</span>
   (a) the formula is wrong (b) the column is too narrow (c) a number is divided by zero (d) a function is misspelled
10. In a pie chart of a family's spending of Rs 24,000, the slice for Rs 6,000 has an angle of <span class="marks">[1]</span>
    (a) 60° (b) 90° (c) 25° (d) 120°

::: note Answers to 23.8
**1.** (c) — 3 columns (A, B, C) × 5 rows (2 to 6) = 15.
**2.** (b) — 8 ÷ 4 = 2 first, then 20 − 2 = 18.
**3.** (a) — (10 + 15 + 20 + 35) ÷ 4 = 80 ÷ 4 = 20.
**4.** (b) — COUNT ignores the text "Absent".
**5.** (a) — 40 >= 40 is TRUE.
**6.** (a) — B2 moves down a row; `$E$1` stays fixed.
**7.** (b) — a filter hides rows that do not match.
**8.** (b) — a line chart shows change over time.
**9.** (b) — widen the column to see the number.
**10.** (b) — 6,000 ÷ 24,000 = ¼, and ¼ × 360° = 90°.
:::

::: caution Dollar signs and colons
An absolute reference has a dollar sign before **both** parts, `$E$1`; `E$1` fixes only the row. A range uses a **colon**, `A2:C6`; a comma joins separate ranges, `A1:A5,C1:C5`. Read every `$` and every `:` in an option before choosing it.
:::

## 23.9 Presentation Software

**Facts.** PowerPoint (.pptx), LibreOffice Impress (.odp), Google Slides. New slide Ctrl + M; layouts arrange **placeholders**; a **theme** designs all slides. A **transition** works **between slides**; an **animation** works on **objects** — entrance (green), emphasis (yellow), exit (red), motion paths; starts *On Click*, *With Previous* or *After Previous*. Views: Normal, Outline, **Slide Sorter**, Notes Page, Reading View, Slide Show. The **slide master** changes every slide. F5 from the beginning, Shift + F5 from the current slide, Esc ends, B blacks the screen. 6 × 6 rule.

1. LibreOffice Impress saves presentations as <span class="marks">[1]</span>
   (a) .pptx (b) .odp (c) .ods (d) .odt
2. Ctrl + M in PowerPoint <span class="marks">[1]</span>
   (a) adds a new slide (b) opens the slide master (c) mutes the sound (d) moves a slide
3. The effect when one slide changes to the next is <span class="marks">[1]</span>
   (a) an animation (b) a transition (c) a layout (d) a theme
4. In PowerPoint, entrance animations are marked in <span class="marks">[1]</span>
   (a) green (b) yellow (c) red (d) blue
5. An animation that starts at the same time as the effect before it is set to <span class="marks">[1]</span>
   (a) On Click (b) With Previous (c) After Previous (d) Delay
6. The view that shows small thumbnails of all slides for reordering them is <span class="marks">[1]</span>
   (a) Normal (b) Slide Sorter (c) Notes Page (d) Reading View
7. Pressing Shift + F5 <span class="marks">[1]</span>
   (a) starts the show from the first slide (b) starts the show from the current slide (c) ends the show (d) blacks out the screen
8. An 8-slide self-running show moves on every 15 seconds. One run lasts <span class="marks">[1]</span>
   (a) 1 minute (b) 2 minutes (c) 23 seconds (d) 2 minutes 30 seconds

::: note Answers to 23.9
**1.** (b) — .odp, the OpenDocument presentation format.
**2.** (a) — Ctrl + M is New Slide in PowerPoint and Impress.
**3.** (b) — transitions work between slides.
**4.** (a) — green entrance, yellow emphasis, red exit.
**5.** (b) — With Previous runs together; After Previous waits.
**6.** (b) — Slide Sorter.
**7.** (b) — F5 starts from the first slide.
**8.** (b) — 8 × 15 = 120 seconds = 2 minutes.
:::

## 23.10 Web Page Design

**Facts.** The WWW was invented by **Tim Berners-Lee** at CERN (1989–1991). A web page is one HTML document; a website is related pages under one domain; the home page is `index.html`. URL = protocol (`https://`) + domain name + path + file name. HTML: container tags (`<p>`…`</p>`) and empty tags (`<br>`, `<hr>`, `<img>`); attributes go in the opening tag. Structure: `<html>`, `<head>` with `<title>` (shown on the tab), `<body>` (shown in the window). `<h1>` is the largest heading, `<h6>` the smallest. `<font>` size 1–7, default 3. `<ul type="square">`, `<ol type="a" start="3">`, `<li>`. `<img src alt width>`. `<a href>`, `mailto:`, `target="_blank"`. Tables: `<tr>`, `<th>`, `<td>`, `colspan`, `rowspan`.

1. The World Wide Web was invented by <span class="marks">[1]</span>
   (a) Tim Berners-Lee (b) Charles Babbage (c) Bill Gates (d) Linus Torvalds
2. In `https://www.ntc.net.np/plans.html`, the protocol is <span class="marks">[1]</span>
   (a) https (b) www (c) net.np (d) plans.html
3. Which of these is an empty (unpaired) tag? <span class="marks">[1]</span>
   (a) `<hr>` (b) `<h1>` (c) `<title>` (d) `<body>`
4. The text inside `<title>` appears <span class="marks">[1]</span>
   (a) on the browser tab (b) as the top heading (c) at the foot of the page (d) nowhere
5. The smallest heading tag is <span class="marks">[1]</span>
   (a) `<h1>` (b) `<h6>` (c) `<head>` (d) `<hr>`
6. A list `<ol type="a" start="3">` with two items numbers them <span class="marks">[1]</span>
   (a) a, b (b) c, d (c) 3, 4 (d) iii, iv
7. The attribute of `<img>` whose text is shown when the picture cannot load is <span class="marks">[1]</span>
   (a) src (b) alt (c) href (d) width
8. Clicking `<a href="mailto:info@school.edu.np">Write to us</a>` <span class="marks">[1]</span>
   (a) opens a web page (b) opens a new email message (c) downloads a file (d) shows a picture
9. A table cell that stretches down over two rows uses <span class="marks">[1]</span>
   (a) `colspan="2"` (b) `rowspan="2"` (c) `cellspacing="2"` (d) `border="2"`
10. The default size of text in the `<font>` tag is <span class="marks">[1]</span>
    (a) 1 (b) 3 (c) 5 (d) 7

::: note Answers to 23.10
**1.** (a) — at CERN, 1989–1991.
**2.** (a) — https is the protocol; www.ntc.net.np is the domain name.
**3.** (a) — `<hr>` has no closing tag.
**4.** (a) — the title belongs to the head and shows on the tab.
**5.** (b) — `<h1>` is the largest, `<h6>` the smallest.
**6.** (b) — small letters starting from the third, c.
**7.** (b) — alt is the alternative text.
**8.** (b) — mailto: opens the email program.
**9.** (b) — rowspan spans rows; colspan spans columns.
**10.** (b) — sizes run from 1 to 7 and 3 is the default.
:::

## 23.11 Information and Communication Technology

**Facts.** **ICT** is the use of computers, telecommunication equipment, networks and software to collect, store, process, send and receive information; its components are hardware, software, data, network, people and **procedures**. A **geostationary** satellite orbits at about 35,786 km. Nepal: Radio Nepal 1951, NTV 1985, e-mail 1994, first ISP 1995, GSM mobile 1999, 4G 2017, **NepaliSat-1 2019**, Nagarik App 2021. E-mail: To, Cc, **Bcc** (hidden copies), attachment. E-governance: **G2C**, G2B, G2G. Never share an **OTP** or MPIN. The **digital divide** is the gap between those with devices, Internet and skills and those without.

1. ICT stands for <span class="marks">[1]</span>
   (a) Information and Communication Technology (b) Internet and Computer Tools (c) Information and Computer Typing (d) International Communication Television
2. The rules and steps for using an ICT system correctly and safely form its <span class="marks">[1]</span>
   (a) procedures (b) hardware (c) network (d) data
3. A geostationary satellite orbits the Earth at a height of about <span class="marks">[1]</span>
   (a) 350 km (b) 3,579 km (c) 35,786 km (d) 357,860 km
4. Nepal's first satellite, NepaliSat-1, was launched in <span class="marks">[1]</span>
   (a) 2009 (b) 2017 (c) 2019 (d) 2021
5. To send a copy of an e-mail without the other receivers seeing that address, put it in <span class="marks">[1]</span>
   (a) To (b) Cc (c) Bcc (d) Subject
6. A citizen renewing a document through a government website is an example of <span class="marks">[1]</span>
   (a) G2G (b) G2B (c) G2C (d) B2B
7. A caller says he is from your bank and asks for the OTP sent to your phone. You should <span class="marks">[1]</span>
   (a) tell him quickly (b) never share it (c) share half of it (d) e-mail it
8. The gap between people who have devices, the Internet and the skill to use them and those who do not is the <span class="marks">[1]</span>
   (a) digital divide (b) bandwidth (c) e-governance (d) netiquette

::: note Answers to 23.11
**1.** (a) — Information and Communication Technology.
**2.** (a) — procedures are the rules and steps people follow.
**3.** (c) — about 35,786 km above the equator.
**4.** (c) — launched in 2019.
**5.** (c) — blind carbon copy.
**6.** (c) — government to citizen.
**7.** (b) — banks never ask for an OTP; it is a fraud.
**8.** (a) — the digital divide.
:::

## 23.12 Computer Ethics and Cyber Law

**Facts.** **Computer ethics** are moral rules for using computers; the **Ten Commandments** were written by the Computer Ethics Institute (1992). Cyber crimes: hacking, **phishing** (fake messages that steal details), cyber bullying, identity theft, software piracy, online fraud. Intellectual property: copyright (in Nepal the author's life plus 50 years — Copyright Act, 2059), patents, trademarks; **plagiarism** is using another's work without credit. Nepal's cyber law: the **Electronic Transactions Act, 2063**; unauthorised access can bring up to Rs 2 lakh, 3 years or both. Report to the **Cyber Bureau** of Nepal Police. Your **digital footprint** is the trail you leave online.

1. The Ten Commandments of Computer Ethics were written by <span class="marks">[1]</span>
   (a) the Computer Ethics Institute (b) the National Examinations Board (c) Microsoft (d) the United Nations
2. A fake e-mail that looks like it comes from a bank and asks for your password is <span class="marks">[1]</span>
   (a) hacking (b) phishing (c) plagiarism (d) cyber bullying
3. Copying an essay from a website and handing it in as your own work is <span class="marks">[1]</span>
   (a) piracy (b) plagiarism (c) hacking (d) spam
4. Nepal's cyber law is the <span class="marks">[1]</span>
   (a) Copyright Act, 2059 (b) Electronic Transactions Act, 2063 (c) Information Technology Policy, 2057 (d) Telecommunications Act, 2053
5. In Nepal, the copyright of a book lasts for <span class="marks">[1]</span>
   (a) 10 years (b) the author's life plus 50 years (c) 25 years (d) ever
6. Under the Electronic Transactions Act, entering another person's computer account without permission can be punished with up to <span class="marks">[1]</span>
   (a) Rs 2 lakh, 3 years in prison, or both (b) a Rs 500 fine only (c) a warning only (d) 20 years in prison
7. In Nepal, cyber crimes are reported to the <span class="marks">[1]</span>
   (a) Cyber Bureau of Nepal Police (b) National Examinations Board (c) Nepal Telecom (d) Curriculum Development Centre
8. The record of everything you post, search and share online is your <span class="marks">[1]</span>
   (a) digital footprint (b) bandwidth (c) IP address (d) avatar

::: note Answers to 23.12
**1.** (a) — in 1992.
**2.** (b) — phishing "fishes" for passwords with fake messages.
**3.** (b) — plagiarism; piracy is copying software or media.
**4.** (b) — the Electronic Transactions Act, 2063.
**5.** (b) — life plus 50 years under the Copyright Act, 2059.
**6.** (a) — unauthorised access is an offence under the Act.
**7.** (a) — the Cyber Bureau handles cyber crime.
**8.** (a) — your digital footprint.
:::

## 23.13 Computer Virus

**Facts.** A **virus** attaches itself to files and copies itself when they run; **malware** is the general name. Creeper (1971), Brain (1986, from **Lahore**, the first PC virus), Morris worm (1988), ILOVEYOU (2000), WannaCry (2017). Types: virus (needs a host), **worm** (spreads by itself over networks), **Trojan horse** (disguised as useful software), **spyware** (watches secretly; keyloggers), **adware** (unwanted adverts), **ransomware** (locks files for money). **Antivirus** detects, cleans, **quarantines** or deletes malware and must be updated — Microsoft Defender, Avast, Kaspersky. **3-2-1 backup**: three copies, on two kinds of media, one kept off-site.

1. Malware that spreads by itself across a network without needing a host file is a <span class="marks">[1]</span>
   (a) virus (b) worm (c) adware (d) Trojan horse
2. A free "game" that secretly opens the computer to an attacker is a <span class="marks">[1]</span>
   (a) Trojan horse (b) worm (c) firewall (d) driver
3. Malware that locks your files and demands money to unlock them is <span class="marks">[1]</span>
   (a) spyware (b) ransomware (c) adware (d) a boot sector virus
4. Brain, the first virus for PCs (1986), came from <span class="marks">[1]</span>
   (a) Lahore (b) Kathmandu (c) Delhi (d) London
5. A keylogger, which records everything you type, is a kind of <span class="marks">[1]</span>
   (a) spyware (b) antivirus (c) firewall (d) adware
6. Which of these is antivirus software? <span class="marks">[1]</span>
   (a) Microsoft Defender (b) WinRAR (c) Microsoft Excel (d) VLC
7. Moving a suspicious file to a locked, safe area so it cannot run is called <span class="marks">[1]</span>
   (a) quarantine (b) defragmenting (c) compressing (d) formatting
8. The 3-2-1 backup rule is three copies, on two kinds of media, with <span class="marks">[1]</span>
   (a) one copy off-site (b) one copy hidden (c) one copy printed (d) one copy compressed

::: note Answers to 23.13
**1.** (b) — a worm copies itself over networks by itself.
**2.** (a) — it hides inside something that looks useful.
**3.** (b) — ransomware, e.g. WannaCry (2017).
**4.** (a) — written in Lahore, Pakistan.
**5.** (a) — it spies on the user.
**6.** (a) — the antivirus built into Windows.
**7.** (a) — quarantine isolates the file.
**8.** (a) — one copy away from home (or in the cloud) survives fire or theft.
:::

## 23.14 Computer Network

**Facts.** A network joins two or more computers to share data, hardware and an Internet connection. **Hub**: copies data to all ports; **switch**: sends only to the destination port (by **MAC address**, 48 bits); **router**: joins different networks (by **IP address**); **modem**: digital ↔ analog. UTP cable uses **RJ-45** plugs (100 m); optical fibre carries light. **LAN** (a building), MAN (a city), WAN (a country or the world), PAN (about 10 m). Topologies: **bus** (one backbone), **ring** (a loop), **star** (central switch; if it fails, all stop). The Internet uses **TCP/IP** and packets. Speed in bits: Mbps ÷ 8 = MB per second.

1. The device that sends data only to the port of the computer it is meant for is a <span class="marks">[1]</span>
   (a) hub (b) switch (c) modem (d) repeater
2. The device that joins a school's LAN to the Internet using IP addresses is a <span class="marks">[1]</span>
   (a) router (b) hub (c) NIC (d) printer
3. A MAC address is <span class="marks">[1]</span>
   (a) 32 bits long (b) 48 bits long (c) 64 bits long (d) 128 bits long
4. The plug on a UTP network cable is <span class="marks">[1]</span>
   (a) RJ-45 (b) BNC (c) USB-C (d) HDMI
5. A network inside one school building is a <span class="marks">[1]</span>
   (a) PAN (b) LAN (c) MAN (d) WAN
6. In a star topology, if the central switch fails <span class="marks">[1]</span>
   (a) only one computer stops (b) the whole network stops (c) nothing changes (d) the speed doubles
7. A 100 Mbps connection can download at most <span class="marks">[1]</span>
   (a) 100 MB per second (b) 12.5 MB per second (c) 800 MB per second (d) 8 MB per second
8. The basic set of rules that every computer on the Internet follows is <span class="marks">[1]</span>
   (a) TCP/IP (b) HTML (c) ICT (d) GUI

::: note Answers to 23.14
**1.** (b) — a switch reads MAC addresses; a hub copies to all ports.
**2.** (a) — routers join different networks.
**3.** (b) — 48 bits, written as 12 hexadecimal digits.
**4.** (a) — RJ-45; BNC is for coaxial cable.
**5.** (b) — a local area network.
**6.** (b) — every computer depends on the centre.
**7.** (b) — 100 ÷ 8 = 12.5 megabytes per second.
**8.** (a) — Transmission Control Protocol / Internet Protocol.
:::

## 23.15 Number System

**Facts.** Base (radix) = number of digits; largest digit = base − 1. Binary (base 2: 0, 1), octal (8: 0–7), decimal (10), hexadecimal (16: 0–9, A–F with A = 10 … F = 15). **Decimal → base:** divide repeatedly, read the remainders **from the bottom up**. **Base → decimal:** multiply each digit by its place value ($\text{base}^0$, $\text{base}^1$, …) and add. **Binary → octal / hex:** groups of **3 / 4 bits from the right**. Memory: 4 bits = nibble, 8 bits = byte, 1 KB = 1024 bytes, 1 MB = 1024 KB, 1 GB = 1024 MB.

1. The base of the hexadecimal number system is <span class="marks">[1]</span>
   (a) 2 (b) 8 (c) 10 (d) 16
2. $(45)_{10}$ in binary is <span class="marks">[1]</span>
   (a) $(101101)_2$ (b) $(110101)_2$ (c) $(101011)_2$ (d) $(100101)_2$
3. $(110101)_2$ in decimal is <span class="marks">[1]</span>
   (a) 53 (b) 45 (c) 35 (d) 52
4. $(157)_8$ in decimal is <span class="marks">[1]</span>
   (a) 111 (b) 157 (c) 117 (d) 109
5. $(2F)_{16}$ in decimal is <span class="marks">[1]</span>
   (a) 32 (b) 47 (c) 215 (d) 45
6. $(11010110)_2$ in octal is <span class="marks">[1]</span>
   (a) $(326)_8$ (b) $(652)_8$ (c) $(316)_8$ (d) $(236)_8$
7. $(11010110)_2$ in hexadecimal is <span class="marks">[1]</span>
   (a) $(D6)_{16}$ (b) $(6D)_{16}$ (c) $(C6)_{16}$ (d) $(D5)_{16}$
8. $(A3)_{16}$ in binary is <span class="marks">[1]</span>
   (a) $(10100011)_2$ (b) $(10110011)_2$ (c) $(1010011)_2$ (d) $(11000011)_2$
9. The largest digit used in the octal system is <span class="marks">[1]</span>
   (a) 7 (b) 8 (c) 9 (d) F
10. 4 GB is equal to <span class="marks">[1]</span>
    (a) 4,000 MB (b) 4,096 MB (c) 1,024 MB (d) 4,096 KB

::: note Answers to 23.15
**1.** (d) — sixteen digits, 0–9 and A–F.
**2.** (a) — 45 = 32 + 8 + 4 + 1, so 101101.
**3.** (a) — 32 + 16 + 4 + 1 = 53.
**4.** (a) — 1 × 64 + 5 × 8 + 7 = 64 + 40 + 7 = 111.
**5.** (b) — 2 × 16 + 15 = 47.
**6.** (a) — 011 010 110 gives 3, 2, 6.
**7.** (a) — 1101 0110 gives D (13) and 6.
**8.** (a) — A = 1010 and 3 = 0011.
**9.** (a) — base 8 uses 0 to 7.
**10.** (b) — 4 × 1024 = 4,096 MB.
:::

::: caution Read the remainders upwards
In decimal-to-binary conversion the **last** remainder is the **leftmost** digit. Reading 45's remainders 1, 0, 1, 1, 0, 1 from the top gives 101101 by chance only because that number reads the same both ways; for 6 the remainders are 0, 1, 1 and the answer is 110, not 011. Always read from the bottom up, and check by converting back.
:::

## 23.16 Computer Graphics

**Facts.** **Raster** (bitmap) pictures are grids of **pixels** and blur or pixelate when enlarged; **vector** pictures store shapes as numbers and stay sharp at any size. Colour depth $n$ bits gives $2^n$ colours (8-bit = 256; 24-bit = 16,777,216); each pixel mixes red, green and blue (0–255 each). Uncompressed size = width × height × bits ÷ 8 bytes. **Paint** and **GIMP** edit raster pictures; **Inkscape** draws vectors (SVG); **Canva** uses online templates. **BMP** uncompressed; **JPEG** lossy, small, for photos; **PNG** lossless with transparency; **GIF** 256 colours, simple animation; **SVG** vector.

1. A picture made of a grid of tiny coloured squares is <span class="marks">[1]</span>
   (a) a raster graphic (b) a vector graphic (c) an animation (d) a font
2. A school logo that must stay sharp on a badge and on a banner should be made as <span class="marks">[1]</span>
   (a) a raster graphic (b) a vector graphic (c) a BMP file (d) a JPEG file
3. With a colour depth of 8 bits, a pixel can show <span class="marks">[1]</span>
   (a) 8 colours (b) 64 colours (c) 256 colours (d) 16,777,216 colours
4. The uncompressed size of an 800 × 600 picture with 24-bit colour is <span class="marks">[1]</span>
   (a) 480,000 bytes (b) 1,440,000 bytes (c) 11,520,000 bytes (d) 14,400 bytes
5. The free vector-drawing program that saves SVG files is <span class="marks">[1]</span>
   (a) Paint (b) GIMP (c) Inkscape (d) Excel
6. For a photograph on a website, where small file size matters most, the usual format is <span class="marks">[1]</span>
   (a) BMP (b) JPEG (c) SVG (d) TXT
7. The format that keeps every detail and allows a transparent background is <span class="marks">[1]</span>
   (a) PNG (b) JPEG (c) BMP (d) MP3
8. A small moving sticker with few colours is usually a <span class="marks">[1]</span>
   (a) GIF file (b) BMP file (c) DOCX file (d) XLSX file

::: note Answers to 23.16
**1.** (a) — pixels make a raster (bitmap) picture.
**2.** (b) — vectors scale without losing sharpness.
**3.** (c) — $2^8 = 256$.
**4.** (b) — 800 × 600 × 24 ÷ 8 = 1,440,000 bytes.
**5.** (c) — Inkscape; GIMP and Paint are raster editors.
**6.** (b) — JPEG compresses photos strongly (with some loss).
**7.** (a) — PNG is lossless and supports transparency.
**8.** (a) — GIF supports simple animation in up to 256 colours.
:::

## 23.17 Multimedia

**Facts.** **Multimedia** combines two or more media: **text, graphics, audio, video and animation**. Video is recorded from real life; **animation** is drawn or computer-made pictures shown quickly (about 12–30 a second). **Linear** multimedia plays in a fixed order (a film); **interactive** multimedia responds to the user (E-Paath, games). Hardware: microphone, webcam, scanner, speakers, projector, sound and graphics cards. Software: VLC, **Audacity** (audio), OpenShot and Kdenlive (video), Blender (animation). Uncompressed sound = samples per second × bits × channels × seconds ÷ 8 bytes. Uses in education, entertainment, business and **health**.

1. Which of these is **not** an element of multimedia? <span class="marks">[1]</span>
   (a) text (b) audio (c) animation (d) electricity
2. Pictures drawn one by one and shown quickly so that they seem to move form <span class="marks">[1]</span>
   (a) an animation (b) a video recording (c) text (d) audio
3. A film watched from beginning to end without any choices is <span class="marks">[1]</span>
   (a) linear multimedia (b) interactive multimedia (c) a raster graphic (d) a vector graphic
4. An E-Paath lesson in which you click to answer and choose what to see next is <span class="marks">[1]</span>
   (a) linear (b) interactive (c) analog (d) printed
5. The free program for recording and editing sound is <span class="marks">[1]</span>
   (a) Audacity (b) Inkscape (c) Excel (d) Paint
6. One minute of uncompressed CD-quality stereo sound (44,100 samples a second, 16 bits, 2 channels) takes about <span class="marks">[1]</span>
   (a) 1 MB (b) 10 MB (c) 100 MB (d) 1 GB
7. To play sound, a computer needs <span class="marks">[1]</span>
   (a) a sound card and speakers (b) a scanner (c) a webcam (d) a keyboard
8. Telemedicine and medical images are uses of multimedia in <span class="marks">[1]</span>
   (a) health (b) farming only (c) banking only (d) sports only

::: note Answers to 23.17
**1.** (d) — the five elements are text, graphics, audio, video and animation.
**2.** (a) — animation; video is recorded from real life.
**3.** (a) — linear: a fixed order.
**4.** (b) — interactive: it responds to the user.
**5.** (a) — Audacity is a free audio editor.
**6.** (b) — 44,100 × 16 × 2 × 60 ÷ 8 = 10,584,000 bytes, about 10 MB.
**7.** (a) — the sound card makes the signal; speakers play it.
**8.** (a) — health care.
:::

## 23.18 Program Design Tools

**Facts.** A **program** is a set of instructions; the program development life cycle is problem analysis (input, process, output) → design → coding → testing and debugging → documentation → implementation and maintenance. An **algorithm** is a finite set of clear steps from Start to Stop, with input, output, definiteness, **finiteness** and effectiveness. Flowchart symbols: **oval** (start/stop), **parallelogram** (input/output), **rectangle** (process), **diamond** (decision), arrows (flow), circle (connector). Every algorithm uses **sequence**, **selection** and **repetition**. **Pseudocode** is structured English (INPUT, PRINT, IF … ENDIF, WHILE … ENDWHILE). A **trace table** is a dry run.

1. The flowchart symbol for a decision is the <span class="marks">[1]</span>
   (a) diamond (b) rectangle (c) oval (d) parallelogram
2. The flowchart symbol for input and output is the <span class="marks">[1]</span>
   (a) parallelogram (b) diamond (c) circle (d) oval
3. Start and Stop are drawn in <span class="marks">[1]</span>
   (a) an oval (b) a rectangle (c) a diamond (d) an arrow
4. The property that an algorithm must end after a fixed number of steps is <span class="marks">[1]</span>
   (a) definiteness (b) finiteness (c) effectiveness (d) input
5. The first step of program development is <span class="marks">[1]</span>
   (a) coding (b) problem analysis (c) testing (d) documentation
6. "Repeat these steps until the counter reaches 10" is an example of <span class="marks">[1]</span>
   (a) sequence (b) selection (c) repetition (d) documentation
7. Structured English with keywords such as IF … ENDIF is called <span class="marks">[1]</span>
   (a) pseudocode (b) machine code (c) a flowchart (d) HTML
8. An algorithm sets N = 1, then repeats "PRINT N × 2; N = N + 1" while N ≤ 4. It prints <span class="marks">[1]</span>
   (a) 2, 4, 6, 8 (b) 1, 2, 3, 4 (c) 2, 4, 6, 8, 10 (d) 1, 3, 5, 7

::: note Answers to 23.18
**1.** (a) — a diamond has two labelled exits, yes and no.
**2.** (a) — parallelogram.
**3.** (a) — the oval terminal symbol.
**4.** (b) — finiteness.
**5.** (b) — first understand the input, process and output.
**6.** (c) — a loop repeats steps.
**7.** (a) — pseudocode.
**8.** (a) — N takes 1, 2, 3, 4, printing 2, 4, 6, 8; at N = 5 the loop stops.
:::

## 23.19 Fundamentals of Computer Programming

**Facts.** **Machine language** is binary and runs directly; **assembly language** uses mnemonics (MOV, ADD) and needs an assembler; **high-level** languages (Python, C, Java, C++) are English-like. A **compiler** translates the whole program; an **interpreter** one line at a time. Errors: **syntax** (breaking the language's rules), **run-time** (an impossible operation while running, e.g. division by zero), **logical** (wrong method, wrong answer, no message). **Debugging** finds and corrects errors. Python (Guido van Rossum, 1991), C (**Dennis Ritchie**, 1972), Java (James Gosling, 1995). Python data types: `int` (whole number), `float` (decimal), `str` (text in quotes), `bool` (`True`/`False`).

1. The language written only in 0s and 1s is <span class="marks">[1]</span>
   (a) machine language (b) assembly language (c) Python (d) Java
2. MOV and ADD are mnemonics of <span class="marks">[1]</span>
   (a) assembly language (b) HTML (c) Python (d) machine language
3. Dividing a number by zero while a program is running causes <span class="marks">[1]</span>
   (a) a syntax error (b) a run-time error (c) a logical error (d) no error
4. A program adds two numbers when it should multiply them; it runs and gives wrong answers with no message. This is <span class="marks">[1]</span>
   (a) a syntax error (b) a run-time error (c) a logical error (d) a compile error
5. The C language was developed by <span class="marks">[1]</span>
   (a) Dennis Ritchie (b) Guido van Rossum (c) James Gosling (d) Tim Berners-Lee
6. Python was created by <span class="marks">[1]</span>
   (a) Guido van Rossum (b) Dennis Ritchie (c) James Gosling (d) Linus Torvalds
7. In Python, the value `"Nepal"` has the data type <span class="marks">[1]</span>
   (a) `str` (b) `int` (c) `float` (d) `bool`
8. Finding and correcting the errors in a program is called <span class="marks">[1]</span>
   (a) debugging (b) compiling (c) coding (d) documenting

::: note Answers to 23.19
**1.** (a) — the only language the CPU runs directly.
**2.** (a) — mnemonics are short codes of assembly language.
**3.** (b) — it fails only while running (`ZeroDivisionError`).
**4.** (c) — the logic is wrong, so the answer is wrong.
**5.** (a) — Dennis Ritchie, 1972.
**6.** (a) — Guido van Rossum, 1991.
**7.** (a) — text enclosed in quotes is a string (`str`).
**8.** (a) — debugging.
:::

## 23.20 Computer Programming using Python

**Facts.** Python files end in **`.py`**, comments start with **`#`**, **`input()`** reads a string from the keyboard (`int()` and `float()` convert it to numbers), **`print()`** displays output, and **F5** runs a script in IDLE. Operators: `**` (power), `*`, `/` (float division), `//` (floor/integer division), `%` (remainder/modulo), `+`, `-`; relational results are `True` or `False`. Built-in functions and methods: `len()`, `abs()`, `round()`, `max()`, `min()`, `.upper()`, `.lower()`, string slicing `s[a:b]`. Loops: `for i in range(start, stop, step):` (stops before `stop`) and `while condition:`.

1. Which symbol begins a comment in Python? <span class="marks">[1]</span>
   (a) `#` (b) `//` (c) `REM` (d) `/*`
2. The value of `17 % 5` in Python is <span class="marks">[1]</span>
   (a) 2 (b) 3 (c) 3.4 (d) 12
3. The value of `17 // 5` in Python is <span class="marks">[1]</span>
   (a) 3 (b) 2 (c) 3.4 (d) 85
4. `len("NEPAL")` returns <span class="marks">[1]</span>
   (a) 4 (b) 5 (c) 6 (d) NEPAL
5. `"COMPUTER"[3:6]` returns <span class="marks">[1]</span>
   (a) PUT (b) MPU (c) UTE (d) COM
6. How many numbers are generated by `range(1, 11, 3)` in Python? <span class="marks">[1]</span>
   (a) 3 (b) 4 (c) 10 (d) 30
7. What is the value of `2 ** 4` in Python? <span class="marks">[1]</span>
   (a) 6 (b) 8 (c) 16 (d) 24
8. What type of value does `input("Enter age: ")` always return in Python? <span class="marks">[1]</span>
   (a) `int` (b) `str` (c) `float` (d) `bool`
9. Which key runs a Python script from the IDLE editor window? <span class="marks">[1]</span>
   (a) F5 (b) Shift + F5 (c) Ctrl + S (d) F8
10. `print(5 > 3)` displays <span class="marks">[1]</span>
    (a) True (b) 1 (c) -1 (d) YES

::: note Answers to 23.20
**1.** (a) — `#` starts a single-line comment in Python.
**2.** (a) — 17 = 3 × 5 + 2; `%` gives the remainder.
**3.** (a) — `//` is floor (integer) division and drops the remainder.
**4.** (b) — N, E, P, A, L: five characters.
**5.** (a) — 0-based indices 3, 4, 5 are P, U, T.
**6.** (b) — `range(1, 11, 3)` yields 1, 4, 7, 10 (four values).
**7.** (c) — `**` is exponentiation: $2^4 = 16$.
**8.** (b) — `input()` always returns a string (`str`).
**9.** (a) — F5 runs the module in IDLE.
**10.** (a) — Python boolean values are `True` and `False`.
:::

::: caution `//` and `%` are partners
For positive whole numbers, `a // b` gives the **quotient** and `a % b` the **remainder**: `17 // 5` is `3` and `17 % 5` is `2`, because $17 = 3 \times 5 + 2$. Check every such answer with that line. And remember `range(a, b)` stops **before** `b`.
:::

::: tip Before you leave this chapter
One hundred and sixty-eight items, twenty facts lines. Copy the twenty facts lines onto two sheets — inventors and dates, the generations, the shortcut keys, the spreadsheet functions, the HTML tags, the network devices, the conversions and the Python operators. In the last week before the paper those two sheets replace this chapter.
:::

## Chapter summary

- **Fundamentals, history and generations:** data → process → information; CU directs, ALU calculates; GIGO; Pascal 1642, Leibniz 1673, Babbage (mill and store), Lovelace, Hollerith 1890, ENIAC 1946, UNIVAC I 1951; IBM 1401 in Nepal (2028 BS); tube → transistor → IC → microprocessor → AI.
- **Types, software and OS:** analog measures, digital counts, hybrid does both; super > mainframe > mini > micro; system vs application software; compiler (whole) vs interpreter (line by line); proprietary, freeware, shareware, open source; CUI vs GUI; copy, move, Recycle Bin.
- **Office software:** Ctrl + S, F12, Ctrl + Z, Ctrl + H, Ctrl + J; header top, footer bottom; mail merge on Mailings; ranges are columns × rows; formulas start with `=`; `$E$1` stays fixed; COUNT counts numbers; transitions between slides, animations on objects; F5 and Shift + F5.
- **Web and society:** URL = protocol + domain + path + file; `<title>` on the tab; `<h1>` largest; empty tags `<br>`, `<hr>`, `<img>`; `alt`, `href`, `mailto:`, `colspan`, `rowspan`; ICT, G2C, Bcc, OTP; phishing, plagiarism, ETA 2063; worm, Trojan, ransomware, quarantine.
- **Networks, numbers and media:** switch by MAC, router by IP; RJ-45; LAN/MAN/WAN; star; Mbps ÷ 8 = MB/s; read remainders upwards; groups of 3 (octal) and 4 (hex); 1 GB = 1024 MB; raster vs vector; $2^n$ colours; PNG, JPEG, GIF, SVG; linear vs interactive multimedia.
- **Programming:** oval, parallelogram, rectangle, diamond; sequence, selection, repetition; syntax, run-time and logical errors; `//` quotient, `%` remainder, `**` power; `for i in range(...)` counts; `while` repeats while true; booleans are `True` and `False`.
