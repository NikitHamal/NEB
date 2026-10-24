---
subject: Computer Science
grade: 8
unit: 2
title: History of Computer
hours: 0
area: Computer Fundamentals
---

People needed to count long before they had computers: shepherds counted
sheep with pebbles, traders kept accounts with knots in a rope, and tax
officers added long columns of figures by hand. Every machine in this lesson
was built to make counting and calculating faster and more accurate, from the
bead frame of an abacus to ENIAC, which filled a large room. Following them in
order shows how each inventor borrowed an idea from the one before — and how
Nepal took its first computer in 2028 BS to count its people.

::: key What questions on this lesson ask
Questions here are about **who invented what, when, and why it mattered**.
Learn the table in section 2.4 by heart: machine, inventor, year and one key
feature. Expect "match the inventor with the machine", full forms (ENIAC,
EDVAC, UNIVAC, ABC), short notes on the abacus or Napier's bones, "why is
Babbage called the father of the computer?", the parts of the Analytical
Engine, and the history of computers in Nepal with BS dates.
:::

```figure caption="From counting frame to computer. The machines fall into four ages: manual devices moved by hand, mechanical calculators with gears, electromechanical machines driven by electric motors and relays, and electronic computers with no moving parts in their calculating circuits."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2, 4.6))
ev = [("c. 2700 BC", "Abacus (counting board; later the bead frame)", 0),
      ("1617", "Napier's bones — John Napier", 0),
      ("1622", "Slide rule — William Oughtred", 0),
      ("1642", "Pascaline — Blaise Pascal", 1),
      ("1673", "Stepped reckoner — G. W. Leibniz", 1),
      ("1804", "Jacquard loom, run by punched cards", 1),
      ("1822", "Difference Engine designed — Charles Babbage", 1),
      ("1834", "Analytical Engine designed — Babbage", 1),
      ("1843", "First published program — Ada Lovelace", 1),
      ("1890", "Tabulating machine — Herman Hollerith", 2),
      ("1942", "ABC — Atanasoff and Berry", 3),
      ("1944", "Harvard Mark I — Howard Aiken and IBM", 2),
      ("1946", "ENIAC — Eckert and Mauchly", 3),
      ("1949", "EDVAC delivered: stored program, binary", 3),
      ("1951", "UNIVAC I — first commercial computer in the USA", 3)]
cols = [SERIES[3], SERIES[0], SERIES[4], SERIES[2]]
n = len(ev)
ys = [n - 1 - i for i in range(n)]
ax.plot([1.55, 1.55], [-0.4, n - 0.6], color=GRID, lw=2.2, zorder=1)
for (yr, txt, era), y in zip(ev, ys):
    ax.scatter([1.55], [y], s=34, color=cols[era], zorder=3, edgecolor="white", linewidth=0.8)
    ax.text(1.38, y, yr, ha="right", va="center", fontsize=7.4, color=INK, fontweight="bold")
    ax.text(1.75, y, txt, ha="left", va="center", fontsize=7.4, color=INK)
labels = ["manual", "mechanical", "electromechanical", "electronic"]
lx = [1.75, 3.05, 4.6, 6.85]
for i, lab in enumerate(labels):
    ax.scatter([lx[i]], [-1.25], s=30, color=cols[i], edgecolor="white", linewidth=0.8)
    ax.text(lx[i] + 0.14, -1.25, lab, ha="left", va="center", fontsize=7.2, color=MUTED)
ax.set_xlim(0.0, 8.6); ax.set_ylim(-1.7, n - 0.4); ax.axis("off")
```

## 2.1 Early calculating devices: abacus, Napier's bones and the slide rule

Before any machine, people counted on their **fingers**, with **pebbles** and
**sticks**, by cutting **notches** in wood or by tying **knots** in a rope. These
work for small numbers but are slow and easily lost track of. The first true
calculating devices were all worked by hand; they are called **manual
devices**.

### The abacus

::: definition Abacus
An **abacus** is a hand-operated counting device made of a frame holding rods
(or wires) on which beads slide. The position of the beads shows a number, and
moving them up and down performs addition and subtraction.
:::

The idea is very old. People in **Mesopotamia** (present-day Iraq) were
calculating on lined counting boards about 2700–2300 BC; the word *abacus*
comes from the Greek *abax*, a board. The bead frame best known today is the
Chinese **suanpan**, used by traders for centuries and still sold in Nepal for
teaching mental arithmetic. The Japanese **soroban** is a lighter version.

The suanpan is divided by a wooden **beam** (bar) into two decks:

- the upper deck, called **heaven**, has **2 beads** on each rod, each worth
  **5**;
- the lower deck, called **earth**, has **5 beads** on each rod, each worth **1**.

A bead counts only when it is pushed **towards the beam**. The rods stand for
place values: from the right, ones, tens, hundreds, thousands and so on.

```photo id="cs8/hist-abacus" caption="A Chinese abacus (suanpan) with thirteen rods. Each rod has two heaven beads above the beam and five earth beads below it. Only the four rods on the right have beads pushed to the beam: 5 + 4 = 9, then 0, 3 and 4, so the abacus shows 9034." width="80"
crop 0.0 0.04 1.0 0.96
```

```figure caption="The number 2028 on a Chinese abacus (suanpan). A bead counts only when it is pushed against the beam: each upper (heaven) bead is worth 5 and each lower (earth) bead is worth 1. The ones rod shows 5 + 1 + 1 + 1 = 8."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse
fig, ax = plt.subplots(figsize=(4.6, 3.3))
vals = [2, 0, 2, 8]
names = ["thousands", "hundreds", "tens", "ones"]
xs = [1.0, 2.25, 3.5, 4.75]
L, R = 0.3, 5.45
ax.add_patch(Rectangle((L, 0.0), R - L, 4.75, fc="none", ec="#6b4a2b", lw=3.0))
ax.add_patch(Rectangle((L, 3.12), R - L, 0.16, fc="#6b4a2b", ec="none"))
bw, bh = 0.72, 0.32
def bead(x, y, on):
    ax.add_patch(Ellipse((x, y), bw, bh, fc=SERIES[1] if on else "#d9c3a5",
                         ec="#5a3e22", lw=0.8, zorder=3))
for x, v, nm in zip(xs, vals, names):
    ax.plot([x, x], [0.04, 4.71], color="#b8a27e", lw=1.6, zorder=1)
    up = 1 if v >= 5 else 0
    low = v - 5 * up
    if up:
        bead(x, 3.46, True); bead(x, 4.55, False)
    else:
        bead(x, 4.55, False); bead(x, 4.21, False)
    for k in range(low):
        bead(x, 2.94 - 0.34 * k, True)
    for k in range(5 - low):
        bead(x, 0.2 + 0.34 * k, False)
    ax.text(x, -0.34, str(v), ha="center", va="center", fontsize=11, fontweight="bold", color=INK)
    ax.text(x, -0.74, nm, ha="center", va="center", fontsize=7.0, color=MUTED)
ax.text(5.62, 4.1, "heaven:\n5 each", ha="left", va="center", fontsize=7.2, color=INK, linespacing=1.2)
ax.text(5.62, 3.2, "beam", ha="left", va="center", fontsize=7.2, color=INK)
ax.text(5.62, 1.6, "earth:\n1 each", ha="left", va="center", fontsize=7.2, color=INK, linespacing=1.2)
ax.set_xlim(0.15, 6.45); ax.set_ylim(-0.98, 4.9); ax.set_aspect("equal"); ax.axis("off")
```

::: example Worked example 2.1 — setting a number on the abacus
**Problem.** (a) Read the number shown in the figure above. (b) How would you
show 1975 on four rods? How many heaven beads and how many earth beads touch
the beam?

**Solution.** (a) Thousands rod: 2 earth beads = 2. Hundreds: none = 0. Tens:
2 earth beads = 2. Ones: 1 heaven bead + 3 earth beads = 5 + 3 = 8. The number
is **2028**.

(b) Write each digit as fives and ones:
1 = one earth bead; 9 = 5 + 4, one heaven and four earth beads;
7 = 5 + 2, one heaven and two earth beads; 5 = one heaven bead.
Heaven beads at the beam: 0 + 1 + 1 + 1 = **3**.
Earth beads at the beam: 1 + 4 + 2 + 0 = **7**.
:::

### Napier's bones

**John Napier** (1550–1617) was a Scottish mathematician who also invented
**logarithms** (1614). In 1617 he described a set of numbered rods, which
became known as **Napier's bones** because the best sets were cut from bone or
ivory.

::: definition Napier's bones
**Napier's bones** are a set of rods, one for each digit 0 to 9, each marked
with the multiples of its digit (1 to 9 times) in squares divided by a
diagonal. Placing the rods side by side turns a multiplication into a few
easy additions. They can also help with division and square roots.
:::

```photo id="cs8/hist-napier-bones" caption="A set of Napier's bones made about 1700, in its wooden tray. The column of numbers on the left is the index; each rod carries one digit at the top and its multiples below, split into tens and units by a diagonal line." width="78"
```

```figure caption="Multiplying 46 × 7 with Napier's bones. Put the bones for 4 and 6 side by side and read across row 7 (shaded, and enlarged on the right). Add the digits in each diagonal strip from the right: 2, then 8 + 4 = 12 (write 2, carry 1), then 2 + 1 = 3. The answer is 322."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
fig, ax = plt.subplots(figsize=(5.0, 3.5))
w, h, top = 0.82, 0.33, 3.45
for r in range(1, 10):
    ax.text(0.28, top - r * h + h / 2, str(r), ha="center", va="center", fontsize=7.4,
            color=INK if r == 7 else MUTED, fontweight="bold" if r == 7 else "normal")
for d, x0 in ((4, 0.55), (6, 1.42)):
    ax.add_patch(Rectangle((x0, top), w, 0.36, fc="#efe3cc", ec="#8a6a3a", lw=0.9))
    ax.text(x0 + w / 2, top + 0.18, str(d), ha="center", va="center", fontsize=9, fontweight="bold", color=INK)
    for r in range(1, 10):
        y = top - r * h
        ax.add_patch(Rectangle((x0, y), w, h, fc="#fde9c8" if r == 7 else "#faf4e8", ec="#8a6a3a", lw=0.7))
        ax.plot([x0, x0 + w], [y, y + h], color="#8a6a3a", lw=0.6)
        p = d * r
        ax.text(x0 + 0.22, y + h * 0.68, str(p // 10), ha="center", va="center", fontsize=7.0, color=INK)
        ax.text(x0 + 0.60, y + h * 0.30, str(p % 10), ha="center", va="center", fontsize=7.0, color=INK)
y7 = top - 7 * h
ax.plot([2.3, 3.05], [y7 + h / 2, 1.75], color=MUTED, lw=0.8, ls=":")
W, H, X0, Y0 = 1.25, 1.0, 3.1, 1.25
for i, (t, u) in enumerate(((2, 8), (4, 2))):
    x = X0 + i * W
    ax.add_patch(Rectangle((x, Y0), W, H, fc="#fde9c8", ec="#8a6a3a", lw=1.0))
    ax.plot([x, x + W], [Y0, Y0 + H], color="#8a6a3a", lw=0.9)
    ax.text(x + 0.33, Y0 + 0.68, str(t), ha="center", va="center", fontsize=10, color=INK)
    ax.text(x + 0.92, Y0 + 0.30, str(u), ha="center", va="center", fontsize=10, color=INK)
ax.text(X0 + W, Y0 + H + 0.28, "row 7, enlarged", ha="center", va="center", fontsize=7.4, color=MUTED)
res = [(X0 + 0.15, "2 + 1 = 3"), (X0 + W, "8 + 4 = 12"), (X0 + 2 * W - 0.15, "2")]
for x, t in res:
    ax.text(x, Y0 - 0.32, t, ha="center", va="center", fontsize=7.6, color=SERIES[1])
ax.text(X0 + W, Y0 - 0.78, "46 × 7 = 322", ha="center", va="center", fontsize=9, fontweight="bold", color=INK)
ax.set_xlim(0.1, 5.75); ax.set_ylim(0.0, 3.95); ax.set_aspect("equal"); ax.axis("off")
```

::: example Worked example 2.2 — multiplying with Napier's bones
**Problem.** Use Napier's bones to find (a) 46 × 7 and (b) 365 × 4.

**Solution.** (a) Place bones 4 and 6 side by side. Row 7 reads 2|8 on bone 4
and 4|2 on bone 6. Add along the diagonals from the right:
units: **2**; next diagonal: 8 + 4 = 12, write **2** and carry 1; last: 2 + 1
= **3**. So 46 × 7 = **322**.

(b) Place bones 3, 6 and 5 side by side. Row 4 reads 1|2, 2|4 and 2|0.
From the right: **0**; 2 + 4 = **6**; 2 + 2 = **4**; and **1**. So
365 × 4 = **1460**. Check: 365 × 4 = 1,460. ✓
:::

### The slide rule

Napier's logarithms turn multiplication into addition of lengths. In 1620
Edmund Gunter drew numbers on a ruler spaced according to their logarithms.
About **1622** the English mathematician **William Oughtred** placed two such
scales side by side so that one could **slide** along the other. This was the
**slide rule**.

::: definition Slide rule
A **slide rule** is a hand-held calculating device with two logarithmic
scales, one fixed and one sliding, and usually a clear cursor with a hairline.
Sliding one scale along the other adds or subtracts lengths, which multiplies
or divides the numbers marked on them.
:::

A slide rule shows its answer as a **position on a scale**, not as separate
digits, so it is an **analog** device (Lesson 4 explains analog and digital).
It gives an answer to about three figures — accurate enough for engineers,
who used slide rules for about 350 years, until pocket electronic calculators
replaced them in the 1970s.

| Device | Inventor and date | Used for | Type |
|---|---|---|---|
| Abacus | Mesopotamia, c. 2700 BC; Chinese suanpan later | addition and subtraction | manual, digital |
| Napier's bones | John Napier, 1617 | multiplication (and division) | manual, digital |
| Slide rule | William Oughtred, c. 1622 | multiplication, division, roots | manual, analog |

## 2.2 Mechanical calculators: Pascaline, Leibniz's stepped reckoner and the Jacquard loom

A **mechanical calculator** does the arithmetic with **gears and wheels**. The
user still turns a handle or a dial, but the machine itself carries tens from
one column to the next.

### The Pascaline

The French mathematician **Blaise Pascal** (1623–1662) built his calculating
machine in **1642**, at the age of about 19, to help his father, a tax
official, add long columns of money. It is called the **Pascaline** (or
Pascal's calculator), and it was one of the first mechanical calculators;
about fifty were made.

- It had a row of **toothed wheels (dials)**, one for each place value, each
  marked **0 to 9**.
- When a wheel turned past 9 back to 0, it pushed the next wheel on by one
  step. This **automatic carry** is the Pascaline's great idea.
- It could **add and subtract** directly; it multiplied only by repeated
  addition.

The same idea works today in the **odometer** of a motorbike and the old
meters at a petrol pump: when the right-hand wheel passes 9, the next wheel
moves on by one.

```photo id="cs8/hist-pascaline" caption="A Pascaline in the Musée des Arts et Métiers, Paris. The six wheels in front are turned with a stylus; the result appears in the six small windows along the top." width="74"
crop 0.0 0.18 1.0 0.88
```

::: example Worked example 2.3 — the automatic carry
**Problem.** The windows of a Pascaline show 0 0 7 9 6. The ones wheel is
turned on by 8 steps. Explain what happens and give the new reading.

**Solution.** The ones wheel moves 6 → 7 → 8 → 9 → 0 → 1 → 2 → 3 → 4. As it
passes from 9 to 0 it carries 1 to the tens wheel. The tens wheel is at 9, so
it also passes from 9 to 0 and carries 1 to the hundreds wheel, which moves
from 7 to 8. The new reading is **0 0 8 0 4**, that is 796 + 8 = **804**.
:::

### Leibniz's stepped reckoner

The German mathematician **Gottfried Wilhelm Leibniz** (1646–1716) improved
Pascal's design. His **stepped reckoner**, shown to the Royal Society in
London in **1673**, used a drum with teeth of nine different lengths, called
the **stepped drum** or *Leibniz wheel*, turned by a **handle (crank)**.

- It could **add, subtract, multiply and divide**.
- Multiplication was done by turning the crank once for each unit of the
  multiplier and shifting a carriage for each place.
- The stepped drum was used in mechanical calculators for nearly 300 years.

Leibniz also studied the **binary number system**, which uses only 0 and 1,
and published it in 1703. Every modern computer works in binary.

### The Jacquard loom

In **1804** the French weaver **Joseph Marie Jacquard** fitted a loom with a
chain of **punched cards**. Each card had holes in a pattern: where there was
a hole, a hook passed through and lifted a thread; where there was no hole, it
did not. The chain of cards controlled the pattern woven into the cloth.

The loom is not a calculator, but its idea changed computing: **instructions
can be stored as holes in cards**, and changing the cards changes the work
without changing the machine. Babbage borrowed punched cards for his
Analytical Engine, Hollerith used them to count the American census, and
computers read programs from punched cards until the 1970s.

| Machine | Inventor, country | Year | Could do | Key idea |
|---|---|---|---|---|
| Pascaline | Blaise Pascal, France | 1642 | + and − | wheels 0–9 with automatic carry |
| Stepped reckoner | G. W. Leibniz, Germany | 1673 | +, −, ×, ÷ | stepped drum turned by a crank |
| Jacquard loom | J. M. Jacquard, France | 1804 | weaves patterns | punched cards as instructions |

## 2.3 Charles Babbage's Difference Engine and Analytical Engine; Ada Lovelace

**Charles Babbage** (1791–1871) was an English mathematician and professor at
Cambridge. In his time, ships, banks and engineers used printed **tables** of
numbers — logarithms, interest and tides — calculated by hand and full of
mistakes. Babbage wanted a machine that would calculate and **print** the
tables with no human error.

### The Difference Engine

In **1822** Babbage proposed the **Difference Engine**, a machine that
calculates a table of values of a polynomial using the **method of
differences**, which needs only addition. The British government paid for it,
but after ten years of work and a quarrel with his engineer, building stopped
in 1833. Only a small working section was ever finished.

From 1847 to 1849 Babbage designed an improved **Difference Engine No. 2**. He
never built it either. To find out whether his design worked, the **Science
Museum in London** built it from his drawings, finishing the calculating
section in **1991**, two hundred years after his birth, and adding the printer
in 2002. It has about **8,000 parts**, weighs **5 tonnes** and calculates
perfectly, proving that Babbage was right.

```photo id="cs8/hist-difference-engine" caption="Difference Engine No. 2, built by the Science Museum, London, from Babbage's drawings. Each vertical column of brass wheels holds one number, one wheel for each digit; the whole engine is worked by turning a crank handle." width="72"
crop 0.0 0.08 1.0 1.0
```

### The Analytical Engine

While working on the Difference Engine, Babbage had a far bigger idea. From
**1834** he designed the **Analytical Engine**, a machine that could do *any*
calculation, not just one kind, by following instructions on punched cards.
It was to be driven by a steam engine and had four parts that every modern
computer still has:

| Part of the Analytical Engine | What it did | Modern name |
|---|---|---|
| Input: punched cards | gave numbers and operations to the engine (Jacquard's idea) | input devices, program |
| Mill | did the arithmetic | CPU (processor) |
| Store | held 1,000 numbers of up to 40 digits | memory |
| Output: printer, curve plotter, bell | gave out the results | output devices |

It could also make **decisions** (do one thing or another depending on a
result) and **repeat** a set of steps — the same ideas found in every program
you will write. The Analytical Engine was never completed: it needed money and
precision engineering that the 1800s could not supply.

```figure caption="Babbage's Analytical Engine (designed from 1834) already had the four units of a modern computer. Only the names have changed: his mill is our processor and his store is our memory."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1, 2.9))
def box(x, y, w, h, t, fc, ec, fs=7.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                 fc=fc, ec=ec, lw=1.1))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, color=INK, linespacing=1.2)
ax.text(1.75, 3.55, "Analytical Engine (1834)", ha="center", fontsize=8.4, fontweight="bold", color=SERIES[3])
ax.text(6.85, 3.55, "Modern computer", ha="center", fontsize=8.4, fontweight="bold", color=ACCENT)
rows = [("punched cards for numbers\nand for operations", "input devices\nand the program"),
        ("the mill:\ndoes the arithmetic", "processor (CPU):\ncontrol unit and ALU"),
        ("the store:\nholds 1,000 numbers", "memory and\nstorage"),
        ("printer, curve plotter\nand bell", "output devices")]
for i, (a, b) in enumerate(rows):
    y = 2.55 - i * 0.82
    box(0.1, y, 3.3, 0.64, a, "#fbf7ee", SERIES[3])
    box(5.2, y, 3.3, 0.64, b, "#eef4fa", ACCENT)
    ax.annotate("", xy=(5.12, y + 0.32), xytext=(3.48, y + 0.32),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1, ls="--"))
ax.set_xlim(0.0, 8.6); ax.set_ylim(0.0, 3.85); ax.axis("off")
```

::: definition Father of the computer
**Charles Babbage** is called the **father of the computer** because his
Analytical Engine was the first design for a general-purpose, programmable
computer, with separate units for input, processing (the mill), storage (the
store) and output — the same plan that every computer follows today.
:::

### Ada Lovelace, the first programmer

**Augusta Ada King, Countess of Lovelace** (1815–1852), the daughter of the
poet Lord Byron, was a gifted mathematician and a friend of Babbage. In 1843
she translated an Italian engineer's article about the Analytical Engine into
English and added her own **notes**, three times longer than the article. In
the last of them, Note G, she wrote out **step by step how the engine would
calculate a series of numbers called Bernoulli numbers**. This is regarded as
the **first published computer program**, so Ada Lovelace is called the
**first computer programmer**.

She also saw further than Babbage himself: she wrote that such a machine could
work with any symbols, not only numbers, and might one day compose music. The
programming language **Ada**, made for the United States Department of
Defense in 1980, is named after her.

::: caution Babbage's engines were decimal, not binary
Some guides say that Ada Lovelace suggested binary numbers for the Analytical
Engine. That is not true: Babbage's engines counted in **decimal**, with wheels
marked 0 to 9. Binary was described by **Leibniz** (published 1703) and first
used in electronic computers such as the ABC and EDVAC. Do not mix up the two.
:::

## 2.4 Electromechanical and electronic machines

::: definition Electromechanical and electronic
An **electromechanical** machine uses electricity to drive **moving parts**:
motors, relays (electrically operated switches), gears and rotating shafts.
An **electronic** computer calculates with **no moving parts**, using vacuum
tubes (and later transistors and chips) that switch electric current on and
off thousands of times faster.
:::

### Hollerith's tabulating machine (1890)

The United States counts its people every ten years. Counting the **1880
census** by hand took about **eight years**, and the population was growing
fast. **Herman Hollerith** (1860–1929), who worked for the Census Office,
built an electric **tabulating machine** to count the **1890 census**.

- Each person's details were punched as holes in a **punched card**, an idea
  taken from the Jacquard loom.
- The machine pressed spring pins onto the card; wherever there was a hole, a
  pin passed through into a cup of mercury, completed an electric circuit and
  moved a counting dial on by one.
- With his machines the population count was ready in about six months and
  the full tables in about two years, saving the government about five million
  dollars.

Hollerith started the **Tabulating Machine Company** in **1896**. In 1911 it
joined three other firms, and in **1924** the new company was renamed
**International Business Machines — IBM**.

### Mark I (1944)

The **Harvard Mark I** (its official name was the Automatic Sequence
Controlled Calculator) was designed by **Howard Aiken** of Harvard University
and built by **IBM**. It was completed in **1944**.

- It was **electromechanical**: thousands of relays and switches turned by a
  long rotating shaft, and it made a loud clicking noise as it worked.
- It was about **15.5 m (51 feet) long, 2.4 m (8 feet) high**, weighed about
  **4.3 tonnes**, had about 765,000 parts and 800 km of wire.
- It read its instructions from punched paper **tape** and worked
  automatically, so it is often called the first **automatic** (programmable)
  calculator in the USA.
- It was slow: about **3 additions per second** and 6 seconds for one
  multiplication. Grace Hopper, later a famous programmer, was one of its
  operators.

### ABC, the Atanasoff–Berry Computer (1942)

**John Vincent Atanasoff**, a physics professor at Iowa State College, and his
student **Clifford Berry** built the **ABC** between 1939 and 1942.

- It was the first **electronic digital** computer: it calculated with about
  **300 vacuum tubes**.
- It used **binary** numbers and stored them as electric charges on
  capacitors fixed to two rotating drums, a memory of **3,000 bits**.
- It was **not programmable**: it was built only to solve sets of linear
  equations (up to 29 at a time).

In 1973 a United States court ruled that Atanasoff, not the makers of ENIAC,
had invented the electronic digital computer.

### ENIAC (1946)

**ENIAC — Electronic Numerical Integrator and Computer** — was built at the
University of Pennsylvania by **J. Presper Eckert** and **John Mauchly** for
the United States Army, to calculate tables for aiming artillery guns. It was
finished at the end of 1945 and shown to the public in **February 1946**.

- It was the first **general-purpose electronic digital computer**: it could
  be set up to solve many kinds of problems.
- It used about **17,468 vacuum tubes**, 70,000 resistors, 10,000 capacitors,
  1,500 relays and 6,000 switches.
- It weighed about **27 tonnes**, filled about **167 m²** (1,800 square feet)
  and used **150 kW** of electricity; vacuum tubes burned out often and had to
  be replaced.
- It did about **5,000 additions per second** — a thousand times faster than
  any machine before it — but it worked in **decimal**, not binary.
- It had no stored program. To change the problem, operators re-plugged
  hundreds of cables and set switches, which took days. Its first programmers
  were six women: Kay McNulty, Betty Jennings, Betty Snyder, Marlyn Wescoff,
  Fran Bilas and Ruth Lichterman.

```photo id="cs8/hist-eniac" caption="ENIAC in use at the US Army's Ballistic Research Laboratory. Its panels of vacuum tubes and plugboards lined the walls of a whole room; Betty Snyder (front) and Glen Beck (back) are setting it up for a problem." width="80"
```

::: example Worked example 2.4 — how much faster was ENIAC?
**Problem.** Mark I did 3 additions per second and ENIAC 5,000. How long
would each take to do one million additions? A laptop does about one thousand
million (10⁹) simple additions per second; how long would it take?

**Solution.** Time = number of additions ÷ additions per second.
Mark I: 1,000,000 ÷ 3 ≈ 333,333 s ≈ 333,333 ÷ 86,400 ≈ **3.9 days**.
ENIAC: 1,000,000 ÷ 5,000 = **200 s** = 3 minutes 20 seconds.
Laptop: 1,000,000 ÷ 1,000,000,000 = **0.001 s**, one thousandth of a second.
ENIAC was about 5,000 ÷ 3 ≈ 1,700 times faster than Mark I.
:::

### EDVAC and the stored-program idea

Setting up ENIAC by hand was so slow that its builders wanted the **program
itself to be kept in memory**, just like the data. In 1945 the mathematician
**John von Neumann** wrote a famous report describing such a machine.

::: definition Stored-program concept
The **stored-program concept** is the idea that a computer's **instructions
are stored in its memory together with the data**, so the computer can fetch
and carry them out one after another, and a new program can be loaded without
rewiring the machine. It was described by John von Neumann in 1945.
:::

**EDVAC — Electronic Discrete Variable Automatic Computer** — was designed by
Eckert and Mauchly on this plan. It worked in **binary**, used about **6,000
vacuum tubes**, and stored 1,000 numbers in tubes of mercury. It was delivered
in 1949 and worked regularly from 1951. In Britain, **Maurice Wilkes's EDSAC**
(Electronic Delay Storage Automatic Calculator) at Cambridge ran its first
stored program on 6 May 1949 and became the first stored-program computer in
regular use.

### UNIVAC I (1951)

**UNIVAC I — Universal Automatic Computer** — was built by Eckert and
Mauchly's company (later part of Remington Rand). The first one was accepted
by the **US Census Bureau** on **31 March 1951**.

- It was the **first commercial computer made in the USA**: it was sold to
  businesses and offices, not built for one army or university.
- It used about **5,200 vacuum tubes**, weighed about **13 tonnes**, and stored
  data on **magnetic tape** instead of punched cards. Forty-six were built.
- In 1952 a UNIVAC correctly predicted, on television, that Eisenhower would
  win the American presidential election, from early results alone.

| Machine | Year | Built by | Type | Remember it for |
|---|---|---|---|---|
| Tabulating machine | 1890 | Herman Hollerith | electromechanical | punched cards for the US census; led to IBM |
| ABC | 1942 | Atanasoff and Berry | electronic | first electronic digital computer; binary; not programmable |
| Mark I | 1944 | Howard Aiken and IBM | electromechanical | automatic, read paper tape; 3 additions per second |
| ENIAC | 1946 | Eckert and Mauchly | electronic | first general-purpose electronic computer; 17,468 tubes; 27 t |
| EDVAC | 1949 | Eckert and Mauchly (von Neumann's plan) | electronic | stored program; binary |
| UNIVAC I | 1951 | Eckert and Mauchly | electronic | first commercial computer in the USA; magnetic tape |

::: memory Full forms to learn
**ABC** — Atanasoff–Berry Computer. **ENIAC** — Electronic Numerical
Integrator and Computer. **EDVAC** — Electronic Discrete Variable Automatic
Computer. **EDSAC** — Electronic Delay Storage Automatic Calculator.
**UNIVAC** — Universal Automatic Computer. **IBM** — International Business
Machines.
:::

::: caution Do not mix up the "firsts"
Each machine is the first of something different. The **ABC** was the first
*electronic digital* computer but could not be programmed. **Mark I** was an
automatic *electromechanical* calculator. **ENIAC** was the first
*general-purpose electronic* computer. **EDSAC** and **EDVAC** were early
*stored-program* computers. **UNIVAC I** was the first *commercial* computer in
the USA. Write the exact "first" the question asks for.
:::

## 2.5 Computers in Nepal: from the census of 2028 BS to today

Nepal's story begins, like Hollerith's, with a **census**. Counting a growing
population by hand had become too slow, so for the census of **2028 BS
(1971 AD)** the government brought in the country's first computer.

| Year | Event |
|---|---|
| 2028 BS (1971 AD) | **IBM 1401**, a second-generation (transistor) computer, is brought to Nepal **on rent** at Rs 1,25,000 a month to process the census of 2028 BS, which counted 1,15,55,983 people. It is installed at the Central Bureau of Statistics; processing takes about a year and a half. |
| 2031 BS (1974 AD) | The **Electronic Data Processing Centre** (यान्त्रिक सारिणीकरण केन्द्र) is set up to run the government's computer work. It later becomes the **National Computer Centre (NCC)**, which also trains people in programming and data processing. |
| 2038 BS (1981 AD) | The **ICL 2950/10**, a mainframe from Britain costing about 2 million US dollars and supported by UNDP and UNFPA, arrives for the census of 2038 BS. It has 64 terminals, so many people can use it at once. |
| 2039–2040 BS (early 1980s) | **Microcomputers** such as Apple, Vector and Sirius are imported by private companies. Computer training institutes and private firms begin to use them. |
| 2052 BS (1995 AD) | Mercantile Communications starts the first **commercial internet** service in Nepal. |
| 2057 BS (2000 AD) | Nepal's first **Information Technology Policy**. |
| 2063 BS | The **Electronic Transactions Act** gives legal value to electronic records and signatures and punishes computer crimes (Lesson 12). |
| 2073 BS (2017 AD) | Nepal Telecom and Ncell launch **4G** mobile internet. |
| 2077–2078 BS (2021 AD) | The **Nagarik App** is launched; the first **e-passport** is issued; the census of 2078 BS uses tablets in some areas and counts 2,91,64,578 people. |

Today computers are used in every bank, ministry, school and hospital, the
government runs its own data centre, and Nepali software companies build apps
for customers at home and abroad. Nepali can be typed in **Unicode**, so
websites, phones and apps work in Nepali as well as English.

::: example Worked example 2.5 — Nepal's first computer bill
**Problem.** The IBM 1401 was rented for Rs 1,25,000 a month. (a) What was the
rent for one year? (b) What was the rent for 19 months, about the time the
census processing took? (c) How many years separate the census of 2028 BS from
the census of 2078 BS?

**Solution.** (a) 1,25,000 × 12 = **Rs 15,00,000** (fifteen lakh) a year.
(b) 1,25,000 × 19 = **Rs 23,75,000**.
(c) 2078 − 2028 = **50 years**. In that time the population grew from
1,15,55,983 to 2,91,64,578, about 2.5 times — and the computers used to count
it went from one rented machine to tablets in the enumerators' hands.
:::

::: note Activity 2.1 — a history chart
Work in groups. Make a wall chart of the history of computers with three
columns: *device, inventor and year,* and *one feature*. Draw or paste a
picture of each device. Add a fourth row of the chart for Nepal, from the
IBM 1401 to the Nagarik App. Then ask an older family member when they first
used a computer or a mobile phone, and add their story to the chart.
:::

::: tip Answering "history" questions
A short note on a device should have four points: **who** invented it,
**when**, **how it worked** and **why it mattered**. For example: "Pascaline —
Blaise Pascal, 1642; toothed wheels marked 0–9 with automatic carry; could add
and subtract; first step towards mechanical calculation."
:::

## Chapter summary

- **Manual devices:** abacus (c. 2700 BC; suanpan: heaven beads 5, earth
  beads 1), Napier's bones (John Napier, 1617; multiplication), slide rule
  (William Oughtred, c. 1622; analog).
- **Mechanical calculators:** Pascaline (Blaise Pascal, 1642; add and subtract,
  automatic carry), stepped reckoner (Leibniz, 1673; all four operations),
  Jacquard loom (1804; punched cards as instructions).
- **Charles Babbage**, father of the computer: Difference Engine (1822) and
  Analytical Engine (1834) with input cards, **mill**, **store** and output.
  **Ada Lovelace** wrote the first published program (1843).
- **Electromechanical:** Hollerith's tabulator (1890 census; IBM, 1924),
  Harvard Mark I (Aiken and IBM, 1944).
- **Electronic:** ABC (1942, first electronic digital), ENIAC (1946, first
  general-purpose; 17,468 tubes), EDVAC (stored program, binary), UNIVAC I
  (1951, first commercial in the USA).
- **Nepal:** IBM 1401 rented in 2028 BS for the census; EDPC 2031 BS (later
  NCC); ICL 2950/10 in 2038 BS; microcomputers from 2039 BS.

## Practice questions

**Group A — Objective (1 mark each)**

1. On a Chinese abacus, each bead above the beam is worth <span class="marks">[1]</span>
   (a) 1 (b) 5 (c) 10 (d) 2
2. Napier's bones were mainly used for <span class="marks">[1]</span>
   (a) addition (b) subtraction (c) multiplication (d) storing data
3. Which of these is an analog calculating device? <span class="marks">[1]</span>
   (a) abacus (b) slide rule (c) Napier's bones (d) Pascaline
4. The Pascaline was invented by <span class="marks">[1]</span>
   (a) Leibniz (b) Blaise Pascal (c) Charles Babbage (d) Napier
5. The first machine controlled by punched cards was the <span class="marks">[1]</span>
   (a) Jacquard loom (b) Pascaline (c) slide rule (d) Mark I
6. In Babbage's Analytical Engine, the part that did the arithmetic was the <span class="marks">[1]</span>
   (a) store (b) mill (c) printer (d) card reader
7. The first computer programmer is considered to be <span class="marks">[1]</span>
   (a) Ada Lovelace (b) Grace Hopper (c) Betty Snyder (d) Herman Hollerith
8. Hollerith's tabulating machine was first used to count the census of <span class="marks">[1]</span>
   (a) Nepal (b) Britain (c) the USA (d) India
9. Mark I was <span class="marks">[1]</span>
   (a) a mechanical calculator (b) an electromechanical machine (c) a fully electronic computer (d) a microcomputer
10. The ABC was built by <span class="marks">[1]</span>
    (a) Eckert and Mauchly (b) Atanasoff and Berry (c) Aiken and IBM (d) Babbage and Lovelace
11. ENIAC stands for <span class="marks">[1]</span>
    (a) Electronic Numerical Integrator and Computer (b) Electrical Number Integrating Automatic Computer (c) Electronic Numeric Input and Calculator (d) Early Numerical Integrated Analog Computer
12. The first computer brought to Nepal was <span class="marks">[1]</span>
    (a) ICL 2950/10 (b) IBM 1401 (c) UNIVAC I (d) Apple II
13. The stored-program concept was given by <span class="marks">[1]</span>
    (a) John von Neumann (b) Charles Babbage (c) Blaise Pascal (d) John Napier

::: note Answers to Group A
**1.** (b) — heaven beads are worth 5; earth beads 1.
**2.** (c) — a row of the bones turns a multiplication into additions.
**3.** (b) — it shows the answer as a position on a scale.
**4.** (b) — Pascal, 1642.
**5.** (a) — Jacquard's loom, 1804.
**6.** (b) — the mill was the processor; the store was the memory.
**7.** (a) — her Note G of 1843 is the first published program.
**8.** (c) — the US census of 1890.
**9.** (b) — relays and rotating shafts driven by electricity.
**10.** (b) — Atanasoff and Berry at Iowa State College.
**11.** (a) — Electronic Numerical Integrator and Computer.
**12.** (b) — rented in 2028 BS for the census.
**13.** (a) — von Neumann's report of 1945.
:::

**Group B — Short answer (2 marks each)**

1. What is an abacus? Write the value of a heaven bead and an earth bead on a suanpan. <span class="marks">[2]</span>
2. Show how Napier's bones give 46 × 7. <span class="marks">[2]</span>
3. Write two features of the Pascaline. <span class="marks">[2]</span>
4. Why is Charles Babbage called the father of the computer? <span class="marks">[2]</span>
5. Why is Ada Lovelace called the first programmer? <span class="marks">[2]</span>
6. How did the Jacquard loom influence the development of computers? <span class="marks">[2]</span>
7. Write the full forms of EDVAC, UNIVAC, ABC and EDSAC. <span class="marks">[2]</span>
8. Write any two features of ENIAC. <span class="marks">[2]</span>
9. What is the stored-program concept? Why was it an improvement on ENIAC? <span class="marks">[2]</span>
10. Write a short note on the IBM 1401 in Nepal. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** An abacus is a hand-operated counting device: a frame with rods on
which beads slide, used for addition and subtraction. On a suanpan each heaven
bead (above the beam) is worth 5 and each earth bead (below) is worth 1.

**2.** Place bones 4 and 6 side by side and read row 7: 2|8 and 4|2. Add the
diagonals from the right: 2; 8 + 4 = 12, write 2 carry 1; 2 + 1 = 3. Answer:
**322**.

**3.** Any two: invented by Blaise Pascal in 1642; toothed wheels marked 0 to
9, one for each place value; automatic carry from one wheel to the next; could
add and subtract directly (multiply only by repeated addition).

**4.** Because his Analytical Engine (1834) was the first design for a
general-purpose, programmable computer, and it had input (punched cards), a
mill (processor), a store (memory) and output — the same units as modern
computers.

**5.** In 1843 she wrote notes on Babbage's Analytical Engine in which she set
out step by step how the engine would calculate Bernoulli numbers. This is the
first published computer program; she also foresaw that computers could work
with symbols and music, not only numbers.

**6.** The loom (1804) was controlled by punched cards: the pattern of holes
decided the woven pattern. This showed that instructions could be stored on
cards and changed without changing the machine; Babbage used the idea for the
Analytical Engine and Hollerith for his census tabulator.

**7.** EDVAC — Electronic Discrete Variable Automatic Computer; UNIVAC —
Universal Automatic Computer; ABC — Atanasoff–Berry Computer; EDSAC —
Electronic Delay Storage Automatic Calculator.

**8.** Any two: built by Eckert and Mauchly, shown in 1946; first
general-purpose electronic computer; about 17,468 vacuum tubes; weighed about
27 tonnes and filled 167 m²; about 5,000 additions per second; programmed by
re-plugging cables and switches.

**9.** The stored-program concept (von Neumann, 1945) keeps the program's
instructions in memory with the data. ENIAC had to be re-wired by hand to
change its program, which took days; a stored-program computer just loads new
instructions.

**10.** The IBM 1401, a second-generation computer, was Nepal's first
computer. It was brought on rent in 2028 BS (1971 AD), at Rs 1,25,000 a month,
to process the census of 2028 BS at the Central Bureau of Statistics.
:::

**Group C — Long answer (4 marks each)**

1. Describe the abacus, Napier's bones and the slide rule. <span class="marks">[4]</span>
2. Describe Babbage's Analytical Engine and explain why it is important. <span class="marks">[4]</span>
3. Write short notes on (a) Mark I and (b) ENIAC. <span class="marks">[2+2]</span>
4. Describe the history of computers in Nepal. <span class="marks">[4]</span>
5. Match the inventors with their machines and give one feature of each: Leibniz, Hollerith, Atanasoff, Eckert and Mauchly. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** *Abacus:* the oldest calculating device (counting boards in
Mesopotamia c. 2700 BC; the Chinese suanpan later). A frame of rods with
beads; a beam divides heaven beads (worth 5) from earth beads (worth 1); beads
moved to the beam are counted; used for addition and subtraction.
*Napier's bones:* John Napier, Scotland, 1617. Rods for the digits 0–9, each
carrying the multiples of its digit in squares split by a diagonal; placing
rods side by side and adding along the diagonals gives a product.
*Slide rule:* William Oughtred, c. 1622, based on Napier's logarithms. Two
logarithmic scales slide past each other to multiply and divide; an analog
device used by engineers until calculators replaced it in the 1970s.

**2.** Designed by Charles Babbage from 1834 as a general-purpose machine
driven by steam. Its parts: **input** by punched cards (from the Jacquard
loom) for numbers and operations; the **mill**, which did the arithmetic; the
**store**, which held 1,000 numbers; and **output** by printer, curve plotter
and bell. It could make decisions and repeat steps. It was never completed,
for lack of money and precise engineering. *Importance:* it was the first
design of a programmable computer, and its plan — input, processor, memory,
output — is still the plan of every computer; Ada Lovelace wrote the first
program for it. That is why Babbage is called the father of the computer.

**3.** (a) *Mark I:* designed by Howard Aiken of Harvard and built by IBM,
completed in 1944. Electromechanical (relays, switches, rotating shaft); about
15.5 m long and 4.3 tonnes; read instructions from punched paper tape; did
about 3 additions per second. (b) *ENIAC:* Electronic Numerical Integrator and
Computer, by Eckert and Mauchly, University of Pennsylvania, shown in 1946.
The first general-purpose electronic computer; about 17,468 vacuum tubes,
27 tonnes, 167 m², 150 kW; 5,000 additions per second; programmed by
re-plugging cables, which took days.

**4.** In 2028 BS (1971 AD) the government rented an IBM 1401, a
second-generation computer, at Rs 1,25,000 a month to process the census; it
was installed at the Central Bureau of Statistics. In 2031 BS the Electronic
Data Processing Centre was set up, later called the National Computer Centre.
In 2038 BS the ICL 2950/10 mainframe, with 64 terminals, came from Britain
with UNDP and UNFPA help for the census of 2038 BS. From 2039 BS private
companies imported microcomputers such as Apple and Sirius. Commercial
internet began in 2052 BS (1995), and today Nepal has e-governance services
such as the Nagarik App and e-passports.

**5.** *Leibniz* — stepped reckoner (1673): a stepped drum turned by a crank;
could add, subtract, multiply and divide. *Hollerith* — tabulating machine
(1890): read punched cards electrically to count the US census; his company
became IBM. *Atanasoff (with Berry)* — ABC (1942): first electronic digital
computer, binary, capacitor-drum memory, not programmable. *Eckert and
Mauchly* — ENIAC (1946), the first general-purpose electronic computer (and
later EDVAC and UNIVAC I).
:::
