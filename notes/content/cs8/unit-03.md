---
subject: Computer Science
grade: 8
unit: 3
title: Generations of Computer
hours: 0
area: Computer Fundamentals
---

ENIAC filled a room, weighed 27 tonnes and did 5,000 additions a second. The
phone in your pocket weighs less than 200 grams and does thousands of millions
of operations a second. That change did not happen all at once. It came in
**generations**, each starting when a new electronic part replaced the old
one: vacuum tubes, then transistors, then integrated circuits, then the
microprocessor. This lesson studies each generation — its main component,
features and example computers — and the fifth generation, which is trying to
make computers learn and reason.

::: key What questions on this lesson ask
Every exam on this lesson asks you to **match a generation with its main
component** (1st vacuum tube, 2nd transistor, 3rd IC, 4th microprocessor, 5th
artificial intelligence). Learn the **comparison table** in section 3.6: period,
component, memory, language, speed, size and examples. Long questions ask for
"features of the ___ generation" or "differences between two generations";
short ones ask you to define a generation, IC, microprocessor or AI, or to
expand IC, LSI, VLSI and ULSI.
:::

## 3.1 Meaning of a computer generation

In a family, a **generation** is the step from grandparents to parents to
children: about twenty-five or thirty years, during which much changes. Computers
also come in generations, but a computer generation is decided by
**technology**, not by age.

::: definition Generation of computer
A **generation of computer** is a stage in the development of computers in
which a **major new technology** — above all a new main electronic component
for processing — was used. Each new generation produced computers that were
**smaller, faster, cheaper, more reliable and more powerful**, and used less
electricity and gave off less heat, than those of the generation before.
:::

There are **five generations**. The first four are named after the component
used to build the processor; the fifth is named after what the computers try
to do.

```figure caption="The five generations on one time line, with some well-known machines placed at the year they appeared. The boundaries are approximate: each generation began when its new component took over, and the older machines went on working for years."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2, 3.5))
gens = [("1st", "vacuum tubes", 1946, 1958, SERIES[1]),
        ("2nd", "transistors", 1958, 1964, SERIES[3]),
        ("3rd", "integrated circuits", 1964, 1975, SERIES[2]),
        ("4th", "microprocessors", 1975, 2026, ACCENT),
        ("5th", "AI, parallel processing", 1990, 2026, SERIES[4])]
for i, (g, dev, a, b, c) in enumerate(gens):
    y = 4 - i
    ax.barh(y, b - a, left=a, height=0.55, color=c, alpha=0.88)
    lab = f"{g}: {dev}"
    if b - a > 25:
        ax.text(a + 1.2, y, lab, ha="left", va="center", fontsize=7.4, color="white", fontweight="bold")
    else:
        ax.text(b + 1.0, y, lab, ha="left", va="center", fontsize=7.4, color=INK)
ev = [(1946, "ENIAC", 0), (1951, "UNIVAC I", 1), (1959, "IBM 1401", 0), (1964, "System/360", 2),
      (1971, "Intel 4004", 1), (1981, "IBM PC", 2), (2007, "smartphones", 0), (2022, "AI chatbots", 1)]
rowy = [-0.5, -1.1, -1.7]
for yr, name, r in ev:
    yy = rowy[r]
    ax.plot([yr, yr], [yy + 0.2, 4.35], color=MUTED, lw=0.6, ls=":", zorder=0)
    ax.text(yr, yy, f"{name}\n{yr}", ha="center", va="center", fontsize=6.9, color=INK, linespacing=1.1)
ax.set_xlim(1940, 2032); ax.set_ylim(-2.05, 4.55)
ax.set_yticks([]); ax.set_xticks([1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020])
ax.tick_params(axis="x", labelsize=7.6)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_position(("data", -2.05))
```

As we move from one generation to the next:

- the processing component becomes **smaller** and computers shrink from rooms
  to desks to pockets;
- **speed** rises from thousandths of a second (milliseconds) per operation to
  billionths (nanoseconds) and less;
- **memory and storage** grow from a few thousand numbers to many gigabytes;
- **power use, heat and cost** fall, and **reliability** rises;
- computers become **easier to use**, from switches and punched cards to
  keyboards, mice, touch screens and voice.

::: caution The dates are only a guide
Books give slightly different years for each generation (some start the fourth
in 1971, when the first microprocessor was made). A computer belongs to a
generation because of its **main component**, not because of its date. If a
question describes a machine "built with transistors", it is second
generation whatever the year.
:::

```photogrid label="3.G" cols="5" ratio="1.1" caption="The five generations of computers in one row. (a) First: vacuum tubes, each as long as a finger, hot and unreliable. (b) Second: a transistor, smaller, cooler and more reliable than a tube. (c) Third: integrated circuits, many transistors on one chip. (d) Fourth: the Intel 4004, the first microprocessor, a whole CPU on one chip (1971). (e) Fifth: a Tensor Processing Unit, a chip built for artificial-intelligence work. The components shrink from the size of a finger to the size of a grain of rice, while the speed grows millions of times."
@ photo id="cs8/gen-vacuum-tubes" cap="(a) 1st: vacuum tubes"
@ photo id="bca101/transistor" cap="(b) 2nd: transistor"
@ photo id="cs8/gen-ic-chips" cap="(c) 3rd: integrated circuits"
@ photo id="cs8/gen-intel-4004" cap="(d) 4th: microprocessor"
@ photo id="bca101/tpu" cap="(e) 5th: AI chip (TPU)"
```

## 3.2 First generation: vacuum tubes (about 1946–1958)

::: definition Vacuum tube
A **vacuum tube** (also called a *valve*) is a sealed glass tube with the air
removed, containing a heated wire (cathode) that gives off electrons, a metal
plate (anode) that collects them and, in most tubes, a grid between them that
controls the flow. It can switch an electric current on and off and can
amplify (strengthen) a signal.
:::

The vacuum tube was invented by John Ambrose Fleming (the diode, 1904) and
improved by Lee de Forest (the triode, with a grid, 1906). A first-generation
computer used thousands of tubes as its switches: ENIAC had 17,468.

```photo id="cs8/gen-vacuum-tubes" caption="Three vacuum tubes (type PCL82). Each is about as long as a finger. The metal parts inside the glass are the cathode, grid and anode; the pins at the bottom plug into a socket. A tube glows and gets hot like a bulb, which is why rooms full of them needed strong air conditioning." width="62"
```

**Features of first-generation computers**

- **Vacuum tubes** were the main component for processing.
- **Magnetic drums** were used for main memory; data and programs went in on
  **punched cards** and **paper tape**, and results came out on printed paper.
- They were programmed in **machine language** — long strings of 0s and 1s
  that are very hard to write and check.
- They were **huge** (a whole room), **very heavy** and **very expensive**.
- They used a lot of **electricity** and gave off so much **heat** that
  tubes often burned out; the computers broke down frequently and were
  **unreliable**.
- They were **slow** by today's standards: one operation took about a
  **millisecond** (thousandth of a second).
- They could do only one job at a time.

**Examples:** ENIAC, EDVAC, EDSAC, UNIVAC I, IBM 650, IBM 701.

```photogrid label="3.N" cols="3" ratio="1.3" caption="Generations in action. (a) A technician changes a burnt-out vacuum tube in ENIAC; with 17,000 tubes, one failed every day or two. (b) The IBM 1401, a second-generation machine, was the computer that Nepal used for its census of 2028 BS. (c) A punched card, the input medium of the first three generations; a program or data was a stack of such cards."
@ photo id="bca101/eniac-tube" cap="(a) Changing a tube in ENIAC"
@ photo id="bca101/ibm1401" cap="(b) IBM 1401, used in Nepal 2028 BS"
@ photo id="bca101/punchcard" cap="(c) Punched card"
```

## 3.3 Second generation: transistors (about 1958–1964)

::: definition Transistor
A **transistor** is a small electronic component made of a **semiconductor**
such as silicon or germanium. It can switch a current on and off and amplify
signals, like a vacuum tube, but it is far smaller, uses much less power, gives
off little heat and lasts much longer.
:::

The transistor was invented in **1947** at Bell Laboratories in the USA by
**John Bardeen, Walter Brattain and William Shockley**, who won the Nobel Prize
for it in 1956. From the late 1950s, computers were built from thousands of
transistors soldered onto small circuit cards.

```photo id="cs8/gen-sms-card" caption="An IBM SMS circuit card of the kind used in the IBM 1401, the second-generation computer that Nepal rented in 2028 BS. The five round metal cans along the bottom are transistors; the cylinders above them are resistors and capacitors. A 1401 held hundreds of such cards." width="80"
crop 0.0 0.06 1.0 0.94
call 0.14 0.18 0.30 0.27 "transistors"
```

**Features of second-generation computers**

- **Transistors** replaced vacuum tubes as the main component.
- **Magnetic core memory** (tiny rings of magnetic material threaded on wires)
  was used for main memory; **magnetic tape** and **magnetic disks** for
  storage.
- Programs were written in **assembly language**, and the first **high-level
  languages** appeared: FORTRAN (1957) for science and COBOL (1959) for
  business.
- They were **smaller, cheaper, faster and more reliable** than first-generation
  computers, and used less power and gave off less heat — but they still
  needed air-conditioned rooms.
- One operation took about a **microsecond** (millionth of a second).
- Punched cards were still used for input, and printers for output.

**Examples:** IBM 1401 (1959) — Nepal's first computer — IBM 7090, CDC 1604,
PDP-1, Honeywell 400.

::: example Worked example 3.1 — how much faster?
**Problem.** A first-generation computer took about one millisecond per
operation and a second-generation one about one microsecond. (a) How many
operations could each do in one second? (b) How many times faster is a
computer that takes one nanosecond per operation than the first-generation
machine?

**Solution.** (a) 1 ms = 1/1000 s, so the first generation did about
**1,000 operations per second**. 1 μs = 1/1,000,000 s, so the second did about
**1,000,000 operations per second** — a thousand times more.
(b) 1 ms ÷ 1 ns = $10^{-3} \div 10^{-9} = 10^6$, so it is about **one million
times faster**.
:::

## 3.4 Third generation: integrated circuits (about 1964–1975)

::: definition Integrated circuit
An **integrated circuit (IC)**, or **chip**, is a complete electronic circuit —
many transistors, resistors and capacitors and the connections between them —
made together on one small piece (chip) of **silicon**, usually smaller than a
fingernail, and sealed in a plastic or ceramic package with metal pins.
:::

The IC was invented by **Jack Kilby** of Texas Instruments in **1958**
(he won the Nobel Prize in Physics in 2000) and, independently, by **Robert
Noyce** of Fairchild Semiconductor in 1959, whose silicon design is the one
used today. Early ICs held a few to a few hundred components; these are called
**SSI** and **MSI**.

```photo id="cs8/gen-ic-chips" caption="Integrated circuits in DIP (dual in-line) packages. The black plastic body protects a tiny silicon chip; the metal legs on both sides connect it to the circuit board. One such chip replaced a whole card of separate transistors." width="58"
```

**Features of third-generation computers**

- **Integrated circuits** replaced individual transistors, so one chip did the
  work of many transistors.
- Main memory was magnetic core and, later, **semiconductor memory**; magnetic
  disks were used widely for storage.
- **Keyboards and monitors** began to replace punched cards and printouts for
  working with the computer.
- **Operating systems** let one computer run several programs at once
  (multiprogramming) and let many users at terminals share it (time-sharing).
- **High-level languages** such as BASIC (1964), Pascal (1970) and C (1972)
  were widely used.
- They were **smaller, cheaper, faster** (about a **nanosecond** per basic
  operation), more reliable and gave off less heat. Smaller, cheaper
  **minicomputers** appeared beside the big mainframes.

**Examples:** IBM System/360 (1964), PDP-11 (1970), Honeywell 6000 series.

| Short form | Full form | Approximate size |
|---|---|---|
| IC | Integrated Circuit | — |
| SSI | Small Scale Integration | up to about 100 components on a chip |
| MSI | Medium Scale Integration | hundreds |
| LSI | Large Scale Integration | thousands to tens of thousands |
| VLSI | Very Large Scale Integration | hundreds of thousands to millions |
| ULSI | Ultra Large Scale Integration | more than a million (today, billions) |

## 3.5 Fourth generation: microprocessors (about 1975 to the present)

::: definition Microprocessor
A **microprocessor** is a single chip that contains a computer's entire
**central processing unit** — the control unit, the arithmetic logic unit and
the registers. It is made with LSI, VLSI or ULSI technology.
:::

The first microprocessor, the **Intel 4004**, came out in **1971**. It was
designed for a Japanese calculator company by Ted Hoff, Federico Faggin,
Stanley Mazor and Masatoshi Shima, held **2,300 transistors** and worked on
4 bits at a time. Because a whole CPU now fitted on one chip, a computer could
fit on a desk — and later in a hand.

```photo id="cs8/gen-intel-4004" caption="The Intel 4004 of 1971, the first microprocessor, with its cover removed. The grey square in the middle is the silicon chip itself, about 3 mm by 4 mm, holding the whole CPU; fine gold wires join it to the sixteen pins." width="70"
```

**Features of fourth-generation computers**

- The **microprocessor** (LSI, then VLSI and ULSI) is the main component.
- Main memory is **semiconductor RAM**; storage moved from floppy disks to
  hard disks, CDs and DVDs, **flash drives**, memory cards and **SSDs**.
- **Personal computers** appeared: the Altair 8800 (1975), Apple II (1977),
  **IBM PC** (1981) and Apple Macintosh (1984), followed by laptops, tablets and
  **smartphones**.
- The **graphical user interface (GUI)** with windows, icons and a **mouse**,
  and later the **touch screen**, made computers easy for everyone to use.
- Computers were joined into **networks** and the **Internet**.
- Languages such as C, C++, Java and **Python**, and ready-made application
  software (word processors, spreadsheets, games), are used.
- Computers are **very small, very fast** (operations in nanoseconds and
  fractions of a nanosecond), **cheap, reliable** and use little power.

**Examples:** IBM PC, Apple Macintosh, today's desktops, laptops, tablets and
smartphones. The computer you use at school is a fourth-generation computer.

```figure caption="Transistors on one processor chip, 1971 to 2023, on a logarithmic scale where each grid line is a thousand times the one below. The points lie close to a straight line because the count has doubled roughly every two years, as Gordon Moore predicted (Moore's law)."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 3.2))
chips = [(1971, 2300, "Intel 4004"), (1978, 29000, "Intel 8086"), (1985, 275000, "Intel 80386"),
         (1993, 3.1e6, "Pentium"), (2000, 42e6, "Pentium 4"), (2006, 291e6, "Core 2 Duo"),
         (2021, 57e9, "Apple M1 Max"), (2023, 19e9, "Apple A17 Pro (phone)")]
x = np.array([c[0] for c in chips]); y = np.array([c[1] for c in chips])
yy = np.linspace(1971, 2023, 50)
ax.plot(yy, 2300 * 2 ** ((yy - 1971) / 2), color=GRID, lw=2.0, zorder=1)
ax.scatter(x, y, s=26, color=ACCENT, zorder=3)
offs = {"Intel 4004": (2, -0.35), "Intel 8086": (2, -0.35), "Intel 80386": (2, -0.35), "Pentium": (2, -0.35),
        "Pentium 4": (2, -0.35), "Core 2 Duo": (2, -0.35), "Apple M1 Max": (-1.5, 0.45),
        "Apple A17 Pro (phone)": (1.0, -0.55)}
for xi, yi, name in chips:
    dx, dl = offs[name]
    ax.text(xi + dx, yi * 10 ** dl, name, fontsize=7.0, color=INK,
            ha="left" if dx > 0 else "right", va="center")
ax.set_yscale("log"); ax.set_ylim(3e2, 1e12); ax.set_xlim(1968, 2030)
ax.set_yticks([1e3, 1e6, 1e9, 1e12]); ax.set_yticklabels(["thousand", "million", "billion", "trillion"])
ax.minorticks_off()
ax.grid(axis="y", color=GRID, lw=0.7); ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_xlabel("year", fontsize=8); ax.set_ylabel("transistors per chip", fontsize=8)
ax.text(1976, 4e6, "doubling about\nevery 2 years", fontsize=7.0, color=MUTED, ha="center")
```

::: example Worked example 3.2 — Moore's law
**Problem.** In 1965 Gordon Moore, a founder of Intel, predicted that the
number of transistors on a chip would keep doubling; from 1975 he put it at
**every two years**. The Intel 4004 of 1971 had 2,300 transistors. If the
count doubled every two years, how many would a chip of 2021 have? Compare
with the Apple M1 Max of 2021, which has about 57 billion.

**Solution.** From 1971 to 2021 is 50 years, which is 50 ÷ 2 = **25
doublings**.
Transistors = 2,300 × $2^{25}$ = 2,300 × 33,554,432 = **77,175,193,600**,
about 77 billion.
The real chip has about 57 billion — less than the prediction, but of the same
size. Moore's law has held remarkably well for fifty years.
:::

## 3.6 Fifth generation: artificial intelligence and parallel processing

The fifth generation is **not** named after a new component. It is named after
a goal: computers that can **learn, reason and understand** in ways that once
needed human intelligence. The name comes from Japan's *Fifth Generation
Computer Systems* project (1982–1992), which tried to build such machines
using parallel processing and the logic language Prolog.

::: definition Artificial intelligence
**Artificial intelligence (AI)** is the ability of a computer program to do
tasks that normally need human intelligence: understanding speech and
language, recognising faces and objects, learning from examples, solving
problems and making decisions.
:::

::: definition Parallel processing
**Parallel processing** is a way of working in which a large task is divided
into parts that are processed **at the same time** by several processors (or
several cores of one processor), so the whole task finishes much faster.
:::

```figure caption="Parallel processing. One processor must do the four parts of a job one after another; four processors (or four cores of one chip) do them at the same time, so the job finishes in about a quarter of the time."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 2.6))
cols = [SERIES[0], SERIES[1], SERIES[2], SERIES[3]]
ax.text(-0.2, 3.95, "one processor (serial)", ha="left", va="center", fontsize=7.8, fontweight="bold", color=INK)
for k in range(4):
    ax.barh(3.35, 2, left=2 * k, height=0.55, color=cols[k], alpha=0.9, edgecolor="white")
    ax.text(2 * k + 1, 3.35, f"part {k + 1}", ha="center", va="center", fontsize=7.4, color="white")
ax.text(8.2, 3.35, "8 hours", ha="left", va="center", fontsize=7.6, color=INK)
ax.text(-0.2, 2.45, "four processors (parallel)", ha="left", va="center", fontsize=7.8, fontweight="bold", color=INK)
for k in range(4):
    y = 1.95 - 0.5 * k
    ax.barh(y, 2, left=0, height=0.4, color=cols[k], alpha=0.9, edgecolor="white")
    ax.text(1, y, f"part {k + 1}", ha="center", va="center", fontsize=7.2, color="white")
    ax.text(2.2, y, f"core {k + 1}", ha="left", va="center", fontsize=7.0, color=MUTED)
ax.text(3.4, 1.2, "2 hours", ha="left", va="center", fontsize=7.6, color=INK)
ax.set_xlim(-0.3, 9.6); ax.set_ylim(0.2, 4.2); ax.axis("off")
```

Parallel processing is everywhere today. A phone's processor may have eight
cores; a graphics processor has thousands; and the fastest supercomputer in
June 2026, China's LineShine, used about 13.8 million cores together.

**Features of fifth-generation computers**

- They use **artificial intelligence**: they can learn from data, recognise
  speech, faces and handwriting, translate languages and answer questions.
- They work in **natural language**: you can talk or type to them in ordinary
  words, in Nepali or English, instead of exact commands.
- They use **parallel processing** and **ULSI** chips with billions of
  transistors.
- Research continues on **quantum computers**, which use the laws of atomic
  physics to solve some problems far faster, and on chips made from biological
  materials (**bio-chips**) and nanotechnology.
- Languages such as **Python**, Prolog and LISP are used to build AI programs.

**Examples you may already use:** voice assistants (Siri, Google Assistant),
AI chatbots that write and explain text (from 2022), face unlock on phones,
Google Translate, recommendations on YouTube, robots in factories and
self-driving cars being tested on roads.

::: caution AI is useful, but it is not a person
An AI program does not *understand* the world as you do. It finds patterns in
the data it was trained on, so it can give a confident answer that is wrong,
and it can copy unfair ideas hidden in its data. Check important facts in a
reliable source, and never present an AI's work as your own.
:::

::: example Worked example 3.3 — parallel processing
**Problem.** A weather-forecast calculation takes 64 hours on one processor.
The job can be split into equal parts. Ideally, how long does it take on
(a) 8 processors and (b) 16 processors? (c) Why is the real time a little
longer?

**Solution.** Ideal time = time on one processor ÷ number of processors.
(a) 64 ÷ 8 = **8 hours**. (b) 64 ÷ 16 = **4 hours**.
(c) The processors must share out the work, wait for one another and combine
their results, and a few steps cannot be split at all, so the real time is
somewhat longer than the ideal.
:::

### Comparison of the five generations

| Feature | 1st | 2nd | 3rd | 4th | 5th |
|---|---|---|---|---|---|
| Period (approx.) | 1946–1958 | 1958–1964 | 1964–1975 | 1975–present | present and future |
| Main component | vacuum tube | transistor | integrated circuit (SSI, MSI) | microprocessor (LSI, VLSI, ULSI) | ULSI chips, AI, parallel processing |
| Main memory | magnetic drum | magnetic core | magnetic core, then semiconductor | semiconductor RAM | semiconductor RAM |
| Input and output | punched cards, paper tape | punched cards, magnetic tape, printers | keyboard, monitor | keyboard, mouse, touch screen | voice, touch, camera, natural language |
| Language | machine language | assembly; FORTRAN, COBOL | high-level: BASIC, Pascal, C | high-level, 4GL: C++, Java, Python, SQL | AI languages, Python, natural language |
| Speed of one operation | milliseconds | microseconds | nanoseconds | nanoseconds and less | very fast, parallel |
| Size, heat, reliability | room-sized, very hot, unreliable | smaller, less heat | smaller still, reliable | desk to pocket, very reliable | all sizes |
| Examples | ENIAC, EDVAC, UNIVAC I | IBM 1401, IBM 7090, CDC 1604 | IBM System/360, PDP-11 | IBM PC, Macintosh, laptops, phones | AI assistants, robots |

::: memory One line for each generation
**1st tube, 2nd transistor, 3rd chip (IC), 4th processor on a chip, 5th
thinking machine (AI).** Speeds: milli → micro → nano → faster still.
:::

::: example Worked example 3.4 — name the generation
**Problem.** Name the generation of each computer: (a) it used 5,200 vacuum
tubes and magnetic tape; (b) it was built from transistors on circuit cards
and rented by Nepal in 2028 BS; (c) its whole CPU is one chip, and it runs
Windows 11; (d) it was built from ICs and let many users share it through
terminals; (e) it understands spoken questions and learns from examples.

**Solution.** (a) **First** (vacuum tubes — UNIVAC I). (b) **Second**
(transistors — the IBM 1401). (c) **Fourth** (microprocessor). (d) **Third**
(integrated circuits, time-sharing). (e) **Fifth** (artificial
intelligence).
:::

::: note Activity 3.1 — five generations, five groups
The class divides into five groups, one for each generation. Each group makes
a chart with: the period, the main component (draw it or paste a picture), the
memory, the language, four features and two example computers. Present your
chart in two minutes; then put the five charts in order on the wall. As a
class, discuss: will the fifth generation be a blessing or a danger for
people? Give reasons on both sides.
:::

::: tip Writing "features of a generation"
For a 4-mark question on one generation, write **the period, the main
component, and at least four features** (memory, language, speed, size/heat or
cost, input and output), then **two examples**. Start every answer with the
component — it is the one point the marker looks for first.
:::

## Chapter summary

- A **generation** is a stage of computer development marked by a major new
  technology, especially a new processing component; each generation is
  smaller, faster, cheaper, more reliable and more powerful.
- **1st (1946–1958): vacuum tubes**, magnetic drums, machine language,
  milliseconds; huge, hot, unreliable. ENIAC, UNIVAC I.
- **2nd (1958–1964): transistors** (Bell Labs, 1947), magnetic core memory,
  assembly language, FORTRAN and COBOL, microseconds. IBM 1401 (Nepal), IBM 7090.
- **3rd (1964–1975): integrated circuits** (Kilby, 1958; Noyce, 1959),
  keyboards and monitors, time-sharing, BASIC and C, nanoseconds. IBM System/360.
- **4th (1975–present): microprocessors** (Intel 4004, 1971; LSI, VLSI, ULSI),
  PCs, GUI, networks and the Internet. IBM PC, laptops, smartphones.
- **5th: artificial intelligence and parallel processing**; natural language,
  learning machines, quantum research.
- **Moore's law:** transistors on a chip double about every two years.

## Practice questions

**Group A — Objective (1 mark each)**

1. First-generation computers used <span class="marks">[1]</span>
   (a) transistors (b) vacuum tubes (c) integrated circuits (d) microprocessors
2. The transistor was invented in 1947 at <span class="marks">[1]</span>
   (a) IBM (b) Bell Laboratories (c) Intel (d) Texas Instruments
3. Which generation used magnetic core memory and assembly language? <span class="marks">[1]</span>
   (a) first (b) second (c) fourth (d) fifth
4. The integrated circuit was invented by <span class="marks">[1]</span>
   (a) Jack Kilby (b) Charles Babbage (c) Herman Hollerith (d) Ted Hoff
5. The first microprocessor was the <span class="marks">[1]</span>
   (a) Pentium (b) Intel 4004 (c) IBM 1401 (d) Apple A17 Pro
6. The computers we use at school belong to the <span class="marks">[1]</span>
   (a) second generation (b) third generation (c) fourth generation (d) first generation
7. VLSI stands for <span class="marks">[1]</span>
   (a) Very Large Scale Integration (b) Very Long System Instruction (c) Visual Large Scale Interface (d) Very Low Speed Integration
8. Artificial intelligence is the main feature of the <span class="marks">[1]</span>
   (a) second generation (b) third generation (c) fourth generation (d) fifth generation
9. Nepal's first computer, the IBM 1401, was a <span class="marks">[1]</span>
   (a) first-generation computer (b) second-generation computer (c) third-generation computer (d) fourth-generation computer
10. Dividing a task among many processors that work at the same time is called <span class="marks">[1]</span>
    (a) parallel processing (b) time-sharing (c) batch processing (d) multiprogramming
11. Keyboards and monitors began to replace punched cards in the <span class="marks">[1]</span>
    (a) first generation (b) second generation (c) third generation (d) fifth generation
12. The language used by first-generation computers was <span class="marks">[1]</span>
    (a) Python (b) machine language (c) BASIC (d) COBOL

::: note Answers to Group A
**1.** (b) — vacuum tubes, e.g. ENIAC's 17,468.
**2.** (b) — Bardeen, Brattain and Shockley at Bell Labs.
**3.** (b) — core memory and assembly language came with transistors.
**4.** (a) — Jack Kilby, Texas Instruments, 1958.
**5.** (b) — Intel 4004, 1971, 2,300 transistors.
**6.** (c) — they are built around microprocessors.
**7.** (a) — Very Large Scale Integration.
**8.** (d) — the fifth generation aims at AI.
**9.** (b) — it was built with transistors.
**10.** (a) — parallel processing.
**11.** (c) — the third generation brought keyboards and monitors.
**12.** (b) — only 0s and 1s.
:::

**Group B — Short answer (2 marks each)**

1. What is meant by a generation of computer? <span class="marks">[2]</span>
2. Write any four features of first-generation computers. <span class="marks">[2]</span>
3. What is a transistor? Why was it better than a vacuum tube? <span class="marks">[2]</span>
4. What is an integrated circuit? Who invented it? <span class="marks">[2]</span>
5. What is a microprocessor? Name the first microprocessor. <span class="marks">[2]</span>
6. Write the full forms of IC, LSI, VLSI and ULSI. <span class="marks">[2]</span>
7. What is artificial intelligence? Give two examples of its use. <span class="marks">[2]</span>
8. What is parallel processing? Give one example. <span class="marks">[2]</span>
9. A job takes 48 hours on one processor. Ideally, how long will it take on 6 processors? Why is the real time longer? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A generation of computer is a stage in the development of computers
marked by a major new technology, especially a new main processing component.
Each new generation was smaller, faster, cheaper, more reliable and more
powerful than the one before.

**2.** Any four: vacuum tubes as the main component; magnetic drum memory;
machine language; punched cards and paper tape for input; huge size; much heat
and electricity; unreliable; slow (milliseconds); very expensive.

**3.** A transistor is a small semiconductor component that switches and
amplifies electric current. It was better because it was much smaller, used
less power, gave off little heat, was faster and lasted longer, so computers
became smaller, cheaper and more reliable.

**4.** An integrated circuit (chip) is a complete circuit of many transistors,
resistors and capacitors made on one small piece of silicon. It was invented
by Jack Kilby (1958), and independently by Robert Noyce (1959).

**5.** A microprocessor is a single chip that contains the whole CPU (control
unit, ALU and registers). The first was the Intel 4004 (1971).

**6.** IC — Integrated Circuit; LSI — Large Scale Integration; VLSI — Very
Large Scale Integration; ULSI — Ultra Large Scale Integration.

**7.** AI is the ability of a computer program to do tasks that need human
intelligence, such as understanding language, recognising faces, learning and
deciding. Examples: voice assistants, face unlock, Google Translate, AI
chatbots, self-driving cars (any two).

**8.** Parallel processing divides a big task into parts that several
processors work on at the same time, so it finishes faster. Example: a
supercomputer running a weather forecast on thousands of processors, or the
eight cores of a phone processor.

**9.** Ideal time = 48 ÷ 6 = **8 hours**. It is longer in practice because the
processors must share out the work, wait for each other and combine results,
and some steps cannot be split.
:::

**Group C — Long answer (4 marks each)**

1. Describe the features of second-generation computers with examples. <span class="marks">[4]</span>
2. Differentiate between third- and fourth-generation computers in any four points. <span class="marks">[4]</span>
3. What is the fifth generation of computers? Describe its features. <span class="marks">[1+3]</span>
4. Make a table showing the main component, language, speed and one example of each of the first four generations. <span class="marks">[4]</span>
5. The Intel 4004 (1971) had 2,300 transistors. Assuming the number doubles every two years, find the expected number in 1991. What is this rule called? <span class="marks">[3+1]</span>

::: note Answers to Group C
**1.** Period about 1958–1964. Main component: **transistors** (invented at
Bell Labs in 1947) instead of vacuum tubes. Magnetic core memory; magnetic tape
and disks for storage. Assembly language and the first high-level languages,
FORTRAN and COBOL. Smaller, faster (microseconds), cheaper and more reliable
than the first generation; less heat and power, but still air-conditioning.
Punched cards for input, printers for output. Examples: IBM 1401 (Nepal's
first computer, 2028 BS), IBM 7090, CDC 1604.

**2.**

| Third generation | Fourth generation |
|---|---|
| integrated circuits (SSI, MSI) | microprocessor (LSI, VLSI, ULSI) |
| about 1964–1975 | about 1975 to the present |
| mainframes and minicomputers, still large | personal computers, laptops, smartphones |
| keyboard and monitor; time-sharing terminals | GUI, mouse, touch screen; networks and the Internet |
| BASIC, Pascal, C | C++, Java, Python, 4GL |
| example: IBM System/360 | example: IBM PC, Apple Macintosh |

**3.** The fifth generation is the present and future stage in which computers
use **artificial intelligence** to learn, reason and understand natural
language (1 mark). Features: AI that learns from data and recognises speech,
faces and writing; natural-language input in ordinary words; parallel
processing on many processors; ULSI chips with billions of transistors;
research on quantum computers and bio-chips; AI languages such as Python and
Prolog. Examples: voice assistants, AI chatbots, self-driving cars.

**4.**

| Generation | Main component | Language | Speed of one operation | Example |
|---|---|---|---|---|
| 1st | vacuum tube | machine language | milliseconds | ENIAC |
| 2nd | transistor | assembly; FORTRAN, COBOL | microseconds | IBM 1401 |
| 3rd | integrated circuit | high-level: BASIC, C | nanoseconds | IBM System/360 |
| 4th | microprocessor | high-level, 4GL | nanoseconds and less | IBM PC |

**5.** From 1971 to 1991 is 20 years = 20 ÷ 2 = 10 doublings.
Expected number = 2,300 × $2^{10}$ = 2,300 × 1,024 = **2,355,200** (about
2.4 million). The rule is **Moore's law**. (The real Intel 486 of 1989 had
about 1.2 million transistors, so the rule is a good rough guide.)
:::

**Group D — Extended answers (10 marks each, for deeper revision)**

1. What is a generation of computers? Describe the five generations with their main features. <span class="marks">[10]</span>
2. Compare the first four generations of computers in a table, with advantages and limitations of each. <span class="marks">[10]</span>
3. Explain the fifth generation. What is Moore's law? <span class="marks">[10]</span>

### Model answer D1: the five generations of computers (10 marks)

**Introduction.** A **generation** of computers is a stage in the development of computers marked by a change in the main electronic component, which made computers smaller, faster, cheaper and more reliable. There are five generations (Plate 3.G).

1. **First generation (about 1946–1958): vacuum tubes.** Computers were as big as a room, used much electricity, gave off great heat and often broke down. Programs were in machine language; input was by punched cards and output was printed. Examples: ENIAC, UNIVAC I.
2. **Second generation (about 1958–1964): transistors.** The transistor, invented in 1947 at Bell Labs, replaced the tube. Computers became smaller, faster and cooler. They used magnetic core memory, assembly language and the first high-level languages FORTRAN and COBOL. Examples: IBM 1401 (used in Nepal's census of 2028 BS), IBM 7090.
3. **Third generation (about 1964–1975): integrated circuits (IC).** Many transistors were put on one small silicon chip. Computers were smaller and cheaper, with keyboards and monitors, and operating systems. Languages: BASIC, Pascal, C. Examples: IBM System/360, PDP-8.
4. **Fourth generation (about 1975 to the present): microprocessors.** A whole CPU on one chip (LSI and VLSI) made the personal computer possible. Features: GUI, mouse, networks, the internet, laptops and smartphones. Examples: IBM PC, Apple Macintosh.
5. **Fifth generation (present and future): artificial intelligence.** Computers that can learn, understand speech and decide, using parallel processing, ULSI chips and AI. Examples: voice assistants, chatbots, self-driving cars.

| Generation | Period | Main component | Language | Example |
|---|---|---|---|---|
| 1st | 1946–1958 | Vacuum tube | Machine | ENIAC |
| 2nd | 1958–1964 | Transistor | Assembly, FORTRAN | IBM 1401 |
| 3rd | 1964–1975 | Integrated circuit | BASIC, C | IBM System/360 |
| 4th | 1975–now | Microprocessor | C++, Java, Python | IBM PC |
| 5th | Now and future | AI, ULSI | AI languages | Chatbots |

**Conclusion.** In each generation the computer became smaller, faster, cheaper and more reliable, so that today it fits in a pocket.

### Model answer D2: comparison of the first four generations (10 marks)

**Introduction.** The four generations differ in the component used, the size, the speed and the cost.

| Point | 1st | 2nd | 3rd | 4th |
|---|---|---|---|---|
| Component | Vacuum tube | Transistor | IC | Microprocessor |
| Size | Room-size | Smaller | Cabinet | Desktop, pocket |
| Speed | Milliseconds | Microseconds | Nanoseconds | Faster than nanoseconds |
| Memory | Magnetic drum | Magnetic core | Semiconductor | Semiconductor RAM |
| Heat and power | Very high | Less | Low | Very low |
| Language | Machine | Assembly, FORTRAN | BASIC, C | Java, Python |
| Cost | Very high | High | Lower | Low |
| Example | ENIAC | IBM 1401 | IBM 360 | IBM PC |

**Advantages and limitations.**

1. **First:** it was the first electronic computer and was faster than any machine before; but it was huge, hot, costly, unreliable and hard to program.
2. **Second:** it was smaller, faster, cooler and more reliable than the first; but it was still costly and needed air-conditioning.
3. **Third:** it was cheaper, smaller and more reliable and ran several programs; but it was still not for individuals and needed repair of the chips as a unit.
4. **Fourth:** it was cheap, small, very fast and available to everybody, with networks and the internet; but it creates e-waste, viruses and cyber-crime.

**Conclusion.** The comparison shows a steady move from big, hot and costly machines to small, cool and cheap ones.

### Model answer D3: fifth generation and Moore's law (10 marks)

**Introduction.** The fifth generation is named not after a new component but after a goal: computers that can **learn, reason and understand** like humans. The name comes from Japan's *Fifth Generation Computer Systems* project (1982–1992).

**Features.**

1. **Artificial intelligence (AI):** programs that learn from data, understand speech and recognise faces.
2. **Natural-language input:** we can speak or write in ordinary words.
3. **Parallel processing:** one job is divided among many processors working together, so it is done faster.
4. **ULSI chips:** billions of transistors on one chip.
5. **Large storage and fast networks:** cloud storage and the internet.
6. **New technologies under research:** quantum computers and bio-chips.
7. **AI languages:** Python and Prolog.

**Examples and uses.** Voice assistants such as Google Assistant, AI chatbots, self-driving cars, medical image reading, language translation and robots.

**Moore's law.** In 1965 Gordon Moore observed that the number of transistors on a chip doubles about every two years. The Intel 4004 of 1971 had 2,300 transistors. From 1971 to 1991 is 20 years, or 10 doublings, so the expected number is $2{,}300 \times 2^{10} = 2{,}355{,}200$, about 2.4 million. The real Intel 486 of 1989 had about 1.2 million, so the law is a good guide.

| Point | Fourth generation | Fifth generation |
|---|---|---|
| Aim | Fast personal computing | Machines that learn and reason |
| Key technology | Microprocessor | AI, parallel processing |
| Input | Keyboard, mouse | Voice, touch, camera |
| Example | IBM PC | Chatbot, self-driving car |

**Conclusion.** The fifth generation moves computers from only following instructions toward helping us think and decide.
