---
subject: General Knowledge and IT
grade: BCA
unit: 3
title: Computer Fundamentals, Hardware and Software
hours: 3
area: General IT
---

General IT carries about five of the ten GK-and-IT questions: three on computer fundamentals (this chapter) and two on the Internet, HTML, programming and full forms (the next). The Dean's Office model asked "which is not an output device" (OCR), SSD/storage, and the father of the computer. Everything here is stable knowledge; learn the tables.

::: key What the paper asks from this chapter
- **Generations**: vacuum tube → transistor → IC → microprocessor → AI.
- **Devices**: which are input, output, storage.
- **Memory**: RAM is volatile, ROM is not; units (byte, KB, MB, GB).
- **Software**: system vs application; operating systems.
- **Number systems**: binary, octal, hexadecimal conversions.
:::

## 3.1 Generations, types and parts of a computer

| Generation | Technology |
|---|---|
| First (1940–56) | vacuum tubes (ENIAC) |
| Second (1956–63) | transistors |
| Third (1964–71) | integrated circuits |
| Fourth (1971– ) | microprocessors |
| Fifth | artificial intelligence |

Types by size: supercomputer, mainframe, minicomputer, microcomputer (PC, laptop). The CPU has the **ALU** (Arithmetic Logic Unit), the **control unit** and **registers**; it is called the brain of the computer. Charles Babbage is the "father of the computer".

```photogrid label="3.1" cols="5" ratio="1.0" caption="Real hardware of the five generations, left to right: (a) a vacuum tube (first), (b) a power transistor (second), (c) integrated circuits in DIP packages (third), (d) a modern microprocessor (fourth), (e) a Google TPU AI accelerator board (fifth)."
@ photo id="bca101/vacuum-tube" cap="1st: vacuum tube"
focus 0.5 0.55
@ photo id="bca101/transistor" cap="2nd: transistor"
crop 0.0 0.5 1.0 1.0
focus 0.5 0.5
@ photo id="bca101/ic-dip" cap="3rd: integrated circuits"
@ photo id="bca101/cpu-i7" cap="4th: microprocessor"
@ photo id="bca101/tpu" cap="5th: AI hardware"
```

```svgfig label="3.1" caption="The five generations drawn to scale on one time axis. The first three generations last 16, 7 and 7 years; the fourth has lasted more than 55 years because the microprocessor is still the heart of every PC and phone. Fifth-generation work (AI) overlaps the fourth, so exam papers treat it as artificial intelligence rather than a single hardware date."
g = [("1st", 1940, 1956, "vacuum tube", "ENIAC, UNIVAC I", "#fecaca", RED), ("2nd", 1956, 1963, "transistor", "IBM 1401", "#fed7aa", AMBER),
     ("3rd", 1964, 1971, "integrated circuit", "IBM 360", "#fef08a", AMBER), ("4th", 1971, 2026, "microprocessor", "PC, laptop, phone", "#bbf7d0", TEAL)]
d = [b - a for _, a, b, *_ in g]; assert d == [16, 7, 7, 55]
f = Fig(780, 330); X0, X1, A0, A1 = 60, 750, 1940, 2030; ax = lambda y: X0 + (y - A0) * (X1 - X0) / (A1 - A0)
f.line(X0, 290, X1, 290, color=SLATE, sw=1.4)
for y in range(1940, 2031, 10):
    f.line(ax(y), 286, ax(y), 294, color=SLATE); f.text(ax(y), 308, str(y), size=10, color=SLATE)
for i, (n, a, b, tech, ex, col, ec) in enumerate(g):
    y = 14 + i * 52; w = ax(b) - ax(a)
    f.box(ax(a), y, w, 38, f"{n}: {tech}, {ex}" if w > 300 else n, fill=col, stroke=ec, size=10.5, bold=True, r=4)
    if w <= 300:
        f.text(ax(b) + 8, y + 19, f"{a}-{b}: {tech}; {ex}", size=10, color=NAVY, bold=True, anchor="start", vmid=True)
f.box(ax(1990), 14 + 4 * 52, ax(2030) - ax(1990), 38, "5th: AI, ML", fill="#e9d5ff", stroke=NAVY, size=10.5, bold=True, r=4, dash=True)
f.text(ax(1990) - 8, 14 + 4 * 52 + 19, "1990s onward: artificial intelligence", size=10, color=NAVY, bold=True, anchor="end", vmid=True)
```

```photogrid label="3.2" cols="3" ratio="1.2" caption="Charles Babbage, called the father of the computer, and his machines: (a) Babbage; (b) a working Difference Engine built from his plans; (c) an IBM 1401, the machine that arrived in Nepal for the 2028 BS census."
@ photo id="bcagk/babbage" cap="Charles Babbage (1791-1871)"
focus 0.5 0.4
@ photo id="bcagk/diffeng" cap="Difference Engine (built 1991 from his plans)"
focus 0.5 0.5
@ photo id="bca101/ibm1401" cap="IBM 1401: Nepal's first computer"
focus 0.5 0.5
```

```photogrid label="3.3" cols="4" ratio="1.0" caption="Computers by size, largest to smallest: (a) a supercomputer (Cray XE6 racks), (b) an IBM mainframe, (c) a DEC PDP-11 minicomputer, (d) a laptop (microcomputer)."
@ photo id="bcagk/super" cap="Supercomputer racks"
focus 0.5 0.45
@ photo id="bcagk/mainframe" cap="IBM mainframe (System z)"
focus 0.5 0.5
@ photo id="bca102/pdp11" cap="PDP-11 minicomputer"
focus 0.5 0.5
@ photo id="bcagk/laptop" cap="Laptop: microcomputer"
focus 0.5 0.5
```

```svgfig label="3.2" caption="Types of computers by size and power. The triangle narrows towards the top: only a few supercomputers exist, while billions of microcomputers (PCs, laptops, phones) are in use. Speed and price rise upwards; numbers fall."
f = Fig(780, 290)
lv = [("Supercomputer", "weather, science, nuclear simulation", "#fecaca", RED), ("Mainframe", "banks, airlines, census, thousands of users", "#fed7aa", AMBER),
      ("Minicomputer", "mid-size firms, labs, small departments", "#fef08a", AMBER), ("Microcomputer", "PC, laptop, tablet, phone: one user", "#bbf7d0", TEAL)]
for i, (n, u, col, ec) in enumerate(lv):
    y = 20 + i * 62; t0 = 40 + i * 42; t1 = t0 + 42
    f.poly([(260 - t0, y), (260 + t0, y), (260 + t1, y + 56), (260 - t1, y + 56)], fill=col, stroke=ec, sw=1.4, label=n, lx=260, ly=y + 30, size=10.5)
    f.text(430 + 60, y + 30, u, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
f.arrow([(745, 270), (745, 30)], color=RED, label="speed, cost", lpos=(715, 150))
f.arrow([(40, 30), (40, 270)], color=TEAL, label="number of machines", lpos=(75, 150))
```

```photogrid label="3.4" cols="2" ratio="1.25" caption="The parts of a computer, from the real board: (a) a micro-ATX motherboard with its main parts numbered; (b) the die of an Intel 8086 microprocessor, with the ALU, control unit and registers all on one chip."
@ photo id="bca101/mobo" cap="Motherboard with numbered parts"
mark 0.51 0.65 "1"
mark 0.79 0.75 "2"
mark 0.50 0.25 "3"
mark 0.66 0.17 "4"
mark 0.87 0.68 "5"
key 1 CPU socket
key 2 RAM slots
key 3 PCIe slot
key 4 Chipset
key 5 24-pin power
@ photo id="bca101/cpu-die-8086" cap="Intel 8086 die: the CPU on a chip"
focus 0.5 0.5
```

```svgfig label="3.3" caption="Block diagram of a computer. The CPU contains the ALU (arithmetic and logic), the control unit and registers. Instructions and data come from main memory (RAM) over the buses, input devices feed data in, output devices take results out and secondary storage keeps files permanently."
f = Fig(780, 330)
f.box(250, 20, 280, 140, "", fill="#eff6ff", stroke=NAVY, r=10, sw=2)
f.text(390, 40, "CPU (processor)", size=12, color=NAVY, bold=True)
f.box(268, 56, 110, 44, "ALU\narith. + logic", fill="#fed7aa", stroke=AMBER, size=10, bold=True)
f.box(402, 56, 110, 44, "Control unit\nfetch, decode", fill="#bbf7d0", stroke=TEAL, size=10, bold=True)
f.box(268, 112, 244, 36, "Registers: PC, IR, accumulator", fill="#fef9c3", stroke=AMBER, size=10, bold=True)
f.box(570, 50, 170, 70, "Main memory\nRAM (volatile) + ROM", fill="#e9d5ff", stroke=NAVY, size=10.5, bold=True)
f.box(20, 50, 170, 70, "Input devices\nkeyboard, mouse, OMR", fill="#dbeafe", stroke=NAVY, size=10.5, bold=True)
f.box(20, 220, 170, 70, "Output devices\nmonitor, printer", fill="#fee2e2", stroke=RED, size=10.5, bold=True)
f.box(570, 220, 170, 70, "Secondary storage\nSSD, HDD, pen drive", fill="#ecfdf5", stroke=TEAL, size=10.5, bold=True)
f.arrow([(190, 85), (250, 85)], color=NAVY, label="data in", lpos=(220, 76)); f.arrow([(250, 130), (190, 250), (190, 250)], color=RED)
f.arrow([(530, 85), (570, 85)], color=NAVY, both=True)
f.arrow([(655, 120), (655, 220)], color=TEAL, both=True)
f.line(250, 190, 740, 190, color=SLATE, sw=3); f.text(495, 182, "system bus: address + data + control", size=10, color=SLATE, bold=True)
f.arrow([(390, 160), (390, 190)], color=SLATE, both=True)
f.text(390, 255, "Stored-program idea: program and data both live in memory", size=10.5, color=NAVY, bold=True)
f.text(390, 275, "CPU cycle: fetch -> decode -> execute -> store", size=10.5, color=TEAL, bold=True)
```

## 3.2 Input, output and storage devices, memory

| Input | Output | Storage |
|---|---|---|
| keyboard, mouse, scanner, microphone, light pen, joystick | monitor, printer, plotter, speaker, projector | HDD, **SSD**, pen drive, CD/DVD, memory card |
| OCR, OMR, MICR, barcode reader | | |

- **OMR** reads pencil marks (answer sheets); **OCR** reads printed text; **MICR** reads magnetic ink on bank cheques. All three are *input* devices.
- **RAM** is volatile main memory; **ROM** is non-volatile; **cache** is the fastest and sits near the CPU; **SSD/HDD** are secondary (mass) storage.
- 1 byte = 8 bits; 1 KB = 1,024 bytes; 1 MB = 1,024 KB; 1 GB = 1,024 MB.

```photogrid label="3.5" cols="4" ratio="1.1" caption="Special input devices that GK papers ask about: (a) an OMR mark sheet read by light, (b) a cheque with the MICR line of magnetic-ink digits at the bottom, (c) a handheld barcode scanner, (d) a joystick."
@ photo id="bcagk/omr" cap="OMR sheet: pencil marks"
focus 0.5 0.5
@ photo id="bcagk/micr" cap="Cheque with MICR line"
call 0.55 0.85 0.5 0.18 "MICR line"
@ photo id="bcagk/barcode" cap="Barcode scanner"
focus 0.5 0.5
@ photo id="bcagk/joystick" cap="Joystick"
focus 0.5 0.5
```

```photogrid label="3.6" cols="4" ratio="1.0" caption="More input devices: (a) a trackball, (b) a USB microphone, (c) an open flatbed scanner, (d) a light pen and console from the SAGE air-defence system."
@ photo id="bcagk/trackball" cap="Trackball"
focus 0.5 0.5
@ photo id="bcagk/mic" cap="USB microphone"
focus 0.5 0.45
@ photo id="bcagk/scanner" cap="Flatbed scanner"
focus 0.5 0.5
@ photo id="bcagk/lightpen" cap="Light pen on SAGE console"
focus 0.4 0.55
```

```photogrid label="3.7" cols="4" ratio="1.0" caption="Output devices: (a) a monitor showing a 1920 x 1080 test pattern, (b) a video projector, (c) a pen plotter for large technical drawings, (d) an inkjet printer with its cover removed."
@ photo id="bcagk/monitor" cap="Monitor 1920x1080"
focus 0.5 0.5
@ photo id="bcagk/projector" cap="Video projector"
focus 0.5 0.5
@ photo id="bcagk/plotter" cap="Plotter"
focus 0.5 0.5
@ photo id="bcagk/inkjet" cap="Inkjet printer inside"
focus 0.5 0.5
```

```svgfig label="3.4" caption="Classification of devices. Note the red box: OCR, OMR, MICR and barcode readers are all input devices, a favourite trick question, because they read data into the computer even though their names sound like machines that print."
f = Fig(780, 330)
f.box(300, 8, 180, 34, "Peripheral devices", fill="#dbeafe", stroke=NAVY, size=11.5, bold=True)
cols = [("Input", "#dbeafe", NAVY, ["keyboard", "mouse, trackball", "scanner", "microphone", "light pen, joystick", "OCR, OMR, MICR,\nbarcode reader"]),
        ("Output", "#fee2e2", RED, ["monitor", "printer (inkjet, laser)", "plotter", "speaker", "projector"]),
        ("Storage", "#ecfdf5", TEAL, ["HDD", "SSD", "pen drive", "CD / DVD", "memory card"])]
for i, (t, fill, ec, items) in enumerate(cols):
    x = 20 + i * 255
    f.box(x + 25, 80, 180, 32, t, fill=fill, stroke=ec, size=12, bold=True)
    f.arrow([(390, 42), (x + 115, 80)], color=SLATE)
    for j, it in enumerate(items):
        hh = 44 if "\n" in it else 28
        yy = 124 + sum(44 if "\n" in k else 28 for k in items[:j]) + j * 6
        hot = "OCR" in it
        f.box(x + 25, yy, 180, hh, it, fill=("#fecaca" if hot else "#ffffff"), stroke=(RED if hot else ec), size=10, bold=hot, r=4)
```

```svgfig label="3.5" caption="Memory hierarchy: speed and cost per byte fall, and capacity rises, going down. The typical times are rounded: a hard disk access (about 10 ms) is 100,000 times slower than a RAM access (about 100 ns). Registers, cache and RAM are volatile; ROM, SSD and HDD keep data when the power is off."
lv = [("Registers", "< 1 KB", "0.3 ns", "#fecaca", RED), ("Cache (L1-L3)", "KB to MB", "1-10 ns", "#fed7aa", AMBER), ("RAM (main memory)", "GB", "100 ns", "#fef08a", AMBER),
      ("SSD (flash)", "100 GB-TB", "100 us", "#bbf7d0", TEAL), ("HDD / DVD", "TB", "10 ms", "#bfdbfe", NAVY)]
assert 10e-3 / 100e-9 == 100000
f = Fig(780, 320)
for i, (n, cap, t, col, ec) in enumerate(lv):
    y = 14 + i * 58; t0 = 60 + i * 24; t1 = t0 + 24
    f.poly([(300 - t0, y), (300 + t0, y), (300 + t1, y + 52), (300 - t1, y + 52)], fill=col, stroke=ec, sw=1.4, label=n, lx=300, ly=y + 28, size=10.5)
    f.text(500, y + 20, f"capacity: {cap}", size=10.5, color=NAVY, bold=True, anchor="start"); f.text(500, y + 38, f"access time: {t}", size=10.5, color=SLATE, anchor="start")
f.arrow([(30, 290), (30, 20)], color=RED, label="faster, costlier", lpos=(58, 150)); f.arrow([(760, 20), (760, 290)], color=TEAL, label="larger, cheaper", lpos=(715, 150))
f.box(480, 296, 270, 20, "RAM vs HDD: 10 ms / 100 ns = 100,000 times", fill=SAND, stroke=AMBER, size=9.5, bold=True)
```

```svgfig label="3.6" caption="The storage-unit ladder: each step is x 1,024 (2 to the power 10), not x 1,000. All the values are computed. A pen drive sold as 4 GB holds 4 x 1,024 = 4,096 MB; 1 byte = 8 bits."
u = ["Byte", "KB", "MB", "GB", "TB"]; v = [1024 ** k for k in range(5)]
assert v[4] == 1099511627776 and v[3] == 1073741824 and 4 * 1024 == 4096
f = Fig(780, 230)
for i, (n, val) in enumerate(zip(u, v)):
    x = 20 + i * 150; h = 40 + i * 20
    f.box(x, 150 - h, 130, h, n, fill=["#fef9c3", "#fed7aa", "#fecaca", "#bbf7d0", "#bfdbfe"][i], stroke=SLATE, size=12, bold=True, r=4)
    f.text(x + 65, 172, f"{val:,}", size=9.5, color=NAVY, bold=True)
    f.text(x + 65, 186, "bytes", size=9, color=SLATE)
    if i: f.arrow([(x - 8, 120), (x + 2, 120)], color=RED)
    if i: f.text(x - 10, 100 - i * 6 - 8, "x1024", size=9, color=RED, bold=True)
f.text(390, 215, "1 byte = 8 bits;  1 KB = 1,024 B;  1 MB = 1,024 KB;  1 GB = 1,024 MB;  1 TB = 1,024 GB", size=10.5, color=NAVY, bold=True)
```

## 3.3 System and application software, operating systems, number systems

- **System software**: operating system (Windows, Linux, macOS, Android), device drivers, utilities, language translators. **Application software**: MS Word, Excel, browsers, games.
- An OS manages processes, memory, files and devices. It does not "design web pages".
- Translators: **compiler** (whole program), **interpreter** (line by line), **assembler** (assembly to machine code).
- Number systems: binary (base 2), octal (8), decimal (10), hexadecimal (16, digits 0–9 and A–F). Examples: $(1010)_2=10$, $(13)_{10}=(1101)_2$, $(17)_8=15$, $(FF)_{16}=255$, $A_{16}=10$. Four bits make 16 values.

```photogrid label="3.8" cols="4" ratio="1.1" caption="The storage family in real life: (a) static RAM chip, the type used for cache; (b) a DDR4 DRAM module, main memory; (c) an SD memory card; (d) a USB pen drive."
@ photo id="bca101/sram" cap="SRAM chip (cache type)"
@ photo id="bca101/ram" cap="DRAM module (RAM)"
crop 0.08 0.0 0.92 1.0
@ photo id="bcagk/mem" cap="SD memory card"
@ photo id="bca101/pendrive" cap="USB pen drive"
```

```photogrid label="3.9" cols="3" ratio="1.25" caption="Secondary storage up close: (a) a hard disk platter and head arm, (b) a DVD, (c) an NVMe SSD. The disk spins and has moving parts, the DVD is read by a laser, and the SSD has no moving parts at all."
@ photo id="bca101/hdd-arm" cap="HDD: platter and read-write arm"
@ photo id="bca101/dvd" cap="DVD (optical, laser)"
@ photo id="bca101/nvme" cap="NVMe SSD (flash)"
```

```photogrid label="3.10" cols="4" ratio="1.1" caption="Operating systems you must recognise: (a) MS-DOS, a command-line OS; (b) Windows 10; (c) Ubuntu Linux; (d) Android, the most widely used mobile OS."
@ photo id="bca101/dos" cap="MS-DOS"
@ photo id="bca101/win10b" cap="Windows 10"
@ photo id="bca101/ubuntu" cap="Ubuntu Linux"
@ photo id="bca101/android" cap="Android"
```

```svgfig label="3.7" caption="Software classification. System software runs the machine (operating system, drivers, utilities, translators); application software does the user's job (word processor, spreadsheet, browser, games). An OS does not design web pages; a browser does not manage memory."
f = Fig(780, 290)
f.box(310, 8, 160, 34, "Software", fill="#dbeafe", stroke=NAVY, size=12, bold=True)
f.box(80, 84, 230, 36, "System software", fill="#fed7aa", stroke=AMBER, size=11.5, bold=True)
f.box(470, 84, 230, 36, "Application software", fill="#bbf7d0", stroke=TEAL, size=11.5, bold=True)
f.arrow([(350, 42), (200, 84)], color=SLATE); f.arrow([(430, 42), (580, 84)], color=SLATE)
for i, t in enumerate(["Operating system: Windows, Linux, macOS, Android", "Device drivers: printer, graphics", "Utilities: antivirus, backup, disk tools", "Translators: compiler, interpreter, assembler"]):
    f.box(30, 140 + i * 36, 330, 30, t, fill="#fffbeb", stroke=AMBER, size=9.5, r=4)
for i, t in enumerate(["Word processor: MS Word", "Spreadsheet: MS Excel", "Web browser: Chrome, Firefox", "Games, media players, Nagarik App"]):
    f.box(420, 140 + i * 36, 330, 30, t, fill="#ecfdf5", stroke=TEAL, size=10, r=4)
```

```svgfig label="3.8" caption="Translators. A compiler reads the whole program and writes an executable file (C, C++); an interpreter reads one line, runs it, then reads the next (Python, JavaScript); an assembler turns assembly mnemonics into machine code. Only the compiler gives a separate output file."
f = Fig(780, 270)
rows = [("Compiler", "whole source\nprogram", "machine code\nfile (.exe)", "run later, fast", "#bbf7d0", TEAL), ("Interpreter", "one line at\na time", "run that line\nimmediately", "no output file, slower", "#bfdbfe", NAVY), ("Assembler", "assembly code\nMOV, ADD", "machine code\n0s and 1s", "one-to-one translation", "#fed7aa", AMBER)]
for i, (n, a, b, c, col, ec) in enumerate(rows):
    y = 14 + i * 84
    f.box(14, y + 8, 120, 50, n, fill=col, stroke=ec, size=12, bold=True)
    f.box(190, y + 8, 150, 50, a, fill="#ffffff", stroke=SLATE, size=10, bold=True)
    f.arrow([(340, y + 33), (420, y + 33)], color=ec, label="translate", lpos=(380, y + 24))
    f.box(420, y + 8, 150, 50, b, fill="#ffffff", stroke=SLATE, size=10, bold=True)
    f.text(585, y + 33, c, size=10, color=ec, bold=True, anchor="start", vmid=True)
```

```svgfig label="3.9" caption="Number-system conversion worked on (214) in decimal. Repeated division by 2 (remainders read bottom to top) gives 11010110; grouping bits in fours gives hexadecimal D6; grouping in threes gives octal 326. All values are computed and checked: 3 x 64 + 2 x 8 + 6 = 214 and 13 x 16 + 6 = 214."
n = 214; steps = []; q = n
while q: steps.append((q, q // 2, q % 2)); q //= 2
b = "".join(str(s[2]) for s in reversed(steps)); assert b == "11010110" == format(n, "b")
assert format(n, "X") == "D6" and format(n, "o") == "326" and 3 * 64 + 2 * 8 + 6 == 214 and 13 * 16 + 6 == 214
f = Fig(780, 330)
f.text(110, 18, "Divide by 2", size=11, color=NAVY, bold=True)
for i, (a, qq, r) in enumerate(steps):
    y = 30 + i * 33
    f.box(20, y, 70, 26, f"{a}", fill="#eff6ff", stroke=NAVY, size=10.5, bold=True, r=3)
    f.text(112, y + 13, f"÷ 2 = {qq}", size=10.5, color=SLATE, vmid=True, anchor="start")
    f.box(180, y, 56, 26, f"r {r}", fill=("#bbf7d0" if r else "#fee2e2"), stroke=(TEAL if r else RED), size=10.5, bold=True, r=3)
f.arrow([(250, 270), (250, 40)], color=TEAL, label="read up", lpos=(272, 150))
f.text(560, 22, f"(214)10 = ({b})2", size=14, color=NAVY, bold=True)
f.text(560, 52, "Group in 4 bits for hex", size=10.5, color=AMBER, bold=True)
for i, (g, h) in enumerate([("1101", "D"), ("0110", "6")]):
    f.box(430 + i * 140, 62, 120, 30, g, fill="#fef3c7", stroke=AMBER, size=13, bold=True); f.text(490 + i * 140, 112, h, size=15, color=AMBER, bold=True)
f.text(560, 138, "(D6)16 = 13 x 16 + 6 = 214", size=10.5, color=AMBER, bold=True)
f.text(560, 172, "Group in 3 bits for octal", size=10.5, color=TEAL, bold=True)
for i, (g, h) in enumerate([("011", "3"), ("010", "2"), ("110", "6")]):
    f.box(430 + i * 95, 182, 85, 30, g, fill="#ccfbf1", stroke=TEAL, size=13, bold=True); f.text(472 + i * 95, 232, h, size=15, color=TEAL, bold=True)
f.text(560, 258, "(326)8 = 3 x 64 + 2 x 8 + 6 = 214", size=10.5, color=TEAL, bold=True)
f.text(560, 290, "Hex digits: 0-9 then A=10 B=11 C=12 D=13 E=14 F=15", size=10, color=SLATE, bold=True)
```

## 3.4 Eight traps in computer-fundamentals questions

Computer questions look easy, which is why marks leak. These eight traps are drawn from the Dean's Office model (OCR as the odd one out, SSD, the father of the computer) and from past TU entrance papers.

1. **OCR, OMR and MICR are input devices.** They read marks, text or magnetic ink *into* the computer, so a question "which is not an output device" can have OCR as the correct answer (Fig 3.4). A bank cheque with a MICR line, an exam sheet read by OMR and a barcode at a Bhat-Bhateni till are three Nepali examples. A printer or a plotter, by contrast, only sends results out.
2. **Volatile means data is lost at power-off.** RAM, cache and registers are volatile, while ROM, SSD, HDD and pen drives keep their data. If the stem asks for "the fastest memory" the answer is cache or registers, not RAM. If it asks for "main memory" the answer is RAM.
3. **SSD is storage, not main memory.** A solid-state drive uses flash chips but acts as secondary storage, like a hard disk, only much faster because it has no spinning parts (Plate 3.9). Do not choose SSD for "primary memory" or "volatile memory". Remember the order: register, cache, RAM, SSD, HDD.
4. **1 KB is 1,024 bytes.** The ladder uses powers of 2, so 1 MB = 1,024 KB and 1 GB = 1,024 MB (Fig 3.6). A shop may sell a 500 GB disk using 1 GB = 1,000,000,000 bytes, but the exam key uses 1,024. Convert carefully: 2 GB = 2 x 1,024 = 2,048 MB, and 1 byte is always 8 bits.
5. **Match the generation to the technology.** First generation is the vacuum tube (ENIAC), second the transistor (IBM 1401, which Nepal used for the 2028 BS census), third the integrated circuit, fourth the microprocessor, and fifth artificial intelligence. A question that says "microprocessor" is the fourth generation even if the machine is a laptop in your hand. Associate each generation with its photograph in Plate 3.1 and you will not mix them up.
6. **System software versus application software.** The operating system, device drivers, utilities and translators are system software; Word, Excel, a browser and a game are application software (Fig 3.7). Windows and Android are operating systems, so they are system software even though you use them every day. An OS manages processes, memory, files and devices, but it does not design web pages.
7. **Compiler or interpreter?** A compiler translates the whole program at once and produces an executable file, so it is used for C and C++. An interpreter works line by line and stops at the first error, which is how Python and JavaScript normally run. An assembler is the third translator and it converts assembly language, not high-level code (Fig 3.8).
8. **Number-system digits and base.** Binary uses 0 and 1, octal 0-7, decimal 0-9 and hexadecimal 0-9 plus A-F, where A is 10 and F is 15. So (FF)16 = 15 x 16 + 15 = 255, and four bits make 16 values (0 to 15). If a digit is larger than the base allows, such as 8 in an octal number, the option is wrong.

### 3.4.1 Worked checks

**Q. Convert (101111) in binary to hexadecimal and decimal.**

**Answer.** Group from the right in fours: 0010 1111, which is 2 and F, so the hexadecimal number is 2F. In decimal, 2F = 2 x 16 + 15 = 47, and checking directly, 32 + 8 + 4 + 2 + 1 = 47. If the options include 2F and 47 together, both are consistent. Fig 3.9 shows the same method on the number 214.

**Q. Which of the following is not an output device? (a) Plotter (b) Projector (c) OCR (d) Speaker**

**Answer: (c).** A plotter draws large diagrams, a projector throws the screen on a wall and a speaker produces sound, so all three send information out of the computer. OCR (optical character recognition) reads printed text and sends it into the computer, so it is an input device. The key idea is the direction of the data: *into* the CPU is input, *out of* the CPU is output.

## Formula and fact sheet

| Item | Fact |
|---|---|
| Vacuum tube / transistor / IC / microprocessor | 1st / 2nd / 3rd / 4th |
| Volatile memory | RAM, cache |
| 1 byte | 8 bits |
| $(FF)_{16}$ | 255 |

## Chapter summary

- OCR, OMR, MICR and barcode readers are input devices.
- RAM loses its data when power is off; ROM does not.
- SSD and HDD are storage, not main memory.
- A compiler translates all at once; an interpreter line by line.
- Fourth generation = microprocessor.

## Practice questions

**Set A — Recall (20 questions)**

1. Which generation of computers used vacuum tubes?
   (a) fourth (b) third (c) second (d) first
2. Second-generation computers used
   (a) vacuum tubes (b) transistors (c) integrated circuits (d) microprocessors
3. The brain of the computer is the
   (a) CPU (b) monitor (c) RAM (d) keyboard
4. Which of these is NOT an output device?
   (a) plotter (b) monitor (c) OCR (d) printer
5. RAM is
   (a) non-volatile (b) volatile (c) read-only (d) permanent
6. ROM is
   (a) lost when power is off (b) freely writable (c) volatile (d) non-volatile
7. One byte equals how many bits?
   (a) 4 (b) 6 (c) 8 (d) 16
8. One kilobyte equals how many bytes?
   (a) 1,024 (b) 1,000 (c) 512 (d) 8
9. Which of these is an input device?
   (a) printer (b) monitor (c) speaker (d) scanner
10. An SSD is a type of
    (a) cache memory (b) secondary (mass) storage (c) RAM (d) register
11. Which is an operating system?
    (a) MS Word (b) Chrome (c) Linux (d) Excel
12. Which is application software?
    (a) MS Excel (b) Windows (c) Linux (d) BIOS
13. Which is the fastest among these?
    (a) hard disk (b) cache memory (c) DVD (d) USB drive
14. ALU stands for
    (a) Array Logic Unit (b) Applied Logic Unit (c) Advanced Logical Unit (d) Arithmetic Logic Unit
15. The binary form of decimal 5 is
    (a) 101 (b) 110 (c) 111 (d) 100
16. The decimal value of $(1010)_2$ is
    (a) 8 (b) 12 (c) 10 (d) 5
17. Charles Babbage is known as the
    (a) inventor of the Internet (b) father of the computer (c) inventor of the mouse (d) creator of Windows
18. BIOS stands for
    (a) Binary Input Output Software (b) Basic Integrated Output System (c) Basic Input Output Software (d) Basic Input Output System
19. Fourth-generation computers use
    (a) vacuum tubes (b) transistors (c) microprocessors (d) artificial intelligence
20. A laptop is a
    (a) microcomputer (b) mainframe (c) supercomputer (d) minicomputer

::: note Answers and explanations — Set A
**1.** (d) — first generation, 1940–56.
**2.** (b) — transistors replaced vacuum tubes.
**3.** (a) — the CPU processes all instructions.
**4.** (c) — OCR reads text into the computer: an input device.
**5.** (b) — RAM loses its contents without power.
**6.** (d) — ROM keeps its contents.
**7.** (c) — 8 bits.
**8.** (a) — 1 KB = 2¹⁰ = 1,024 bytes.
**9.** (d) — a scanner sends data in.
**10.** (b) — solid-state drives store data permanently.
**11.** (c) — Linux; the others are applications.
**12.** (a) — Excel is an application program.
**13.** (b) — cache is faster than disks.
**14.** (d) — Arithmetic Logic Unit.
**15.** (a) — 4 + 1 = 101.
**16.** (c) — 8 + 2 = 10.
**17.** (b) — he designed the Analytical Engine.
**18.** (d) — Basic Input Output System.
**19.** (c) — the microprocessor era.
**20.** (a) — personal computers are microcomputers.
:::

**Set B — Understanding (12 questions)**

1. One megabyte equals
   (a) 1,000 KB (b) 1,024 KB (c) 512 KB (d) 1,024 bytes
2. The decimal value of $(FF)_{16}$ is
   (a) 16 (b) 15 (c) 256 (d) 255
3. The binary form of decimal 13 is
   (a) 1101 (b) 1011 (c) 1110 (d) 1001
4. The decimal value of $(17)_8$ is
   (a) 17 (b) 14 (c) 15 (d) 16
5. The part of the CPU that fetches and decodes instructions is the
   (a) ALU (b) control unit (c) RAM (d) ROM
6. Which is NOT a function of an operating system?
   (a) memory management (b) file management (c) process management (d) designing web pages
7. The device that reads pencil marks on answer sheets is
   (a) OMR (b) OCR (c) MICR (d) barcode reader
8. MICR is mainly used in
   (a) schools (b) hospitals (c) banks (d) cinemas
9. A compiler
   (a) translates one line at a time (b) translates the whole program at once (c) removes comments (d) repairs hardware
10. The translator that converts assembly language into machine code is the
    (a) compiler (b) interpreter (c) linker (d) assembler
11. Which memory is volatile?
    (a) ROM (b) HDD (c) RAM (d) SSD
12. The binary form of decimal 10 is
    (a) 1010 (b) 1001 (c) 1100 (d) 1111

::: note Answers and explanations — Set B
**1.** (b) — 1,024 KB.
**2.** (d) — 15 × 16 + 15 = 255.
**3.** (a) — 8 + 4 + 1.
**4.** (c) — 1 × 8 + 7 = 15.
**5.** (b) — the control unit.
**6.** (d) — web design is done with application tools.
**7.** (a) — optical mark recognition.
**8.** (c) — cheque processing.
**9.** (b) — an interpreter works line by line.
**10.** (d) — assembler.
**11.** (c) — RAM loses data when power is off.
**12.** (a) — 8 + 2.
:::

**Set C — Application (8 questions)**

1. The binary sum 101 + 11 equals
   (a) 1000 (b) 1001 (c) 110 (d) 1010
2. The number of bits needed to represent 16 distinct values is
   (a) 3 (b) 8 (c) 4 (d) 16
3. One gigabyte equals
   (a) 1,000 MB (b) 1,024 MB (c) 100 MB (d) 512 MB
4. The decimal value of the hexadecimal digit A is
   (a) 11 (b) 9 (c) 12 (d) 10
5. The largest value in one byte is
   (a) 127 (b) 128 (c) 255 (d) 256
6. The integrated circuit was introduced in the
   (a) third generation (b) first generation (c) second generation (d) fourth generation
7. The first general-purpose electronic digital computer was
   (a) Mark I (b) Altair (c) Apple I (d) ENIAC
8. The CPU consists of
   (a) RAM and ROM only (b) ALU, control unit and registers (c) monitor and keyboard (d) printer and scanner

::: note Answers and explanations — Set C
**1.** (a) — 5 + 3 = 8 = 1000.
**2.** (c) — 2⁴ = 16.
**3.** (b) — 1,024 MB.
**4.** (d) — A is 10 in hexadecimal.
**5.** (c) — 11111111 = 255.
**6.** (a) — third generation (1964–71).
**7.** (d) — ENIAC (1945).
**8.** (b) — ALU, control unit and registers.
:::
