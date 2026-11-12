---
subject: Mathematics
grade: BCA
unit: 15
title: Series, Calendar, Clock and Figure Reasoning
hours: 5
area: Reasoning
---

The second reasoning chapter covers the questions that depend on pattern spotting and counting: number and letter series, calendar days, clock angles, cubes, dice and counting figures. The Dean's Office model asks "how many squares are in the figure". All of these have a standard method that you can run in under a minute.

::: key What the paper asks from this chapter
- **Series**: differences, ratios, squares, cubes, primes, alternating patterns.
- **Calendar**: odd days; leap years; the day after $n$ days.
- **Clock**: angle $=|30H-5.5M|$; coincidences and right angles.
- **Cubes and dice**: opposite faces sum to 7; painted-cube counts.
- **Counting figures**: squares in an $n\times n$ grid.
:::

## 15.1 Number and letter series, odd one out

- Test differences (constant → AP), ratios (constant → GP), squares ($n^2$: 1, 4, 9; $n^2+1$: 2, 5, 10, 17, 26), cubes, primes (2, 3, 5, 7, 11, 13), triangular numbers (1, 3, 6, 10), factorials, Fibonacci (1, 1, 2, 3, 5, 8, 13).
- $2,6,12,20,30,\ldots$ is $n(n+1)$, next 42. $3,7,15,31$ doubles and adds 1, next 63.
- Letter series: convert to positions and look for a constant step, or opposite-letter pairs (AZ, BY, CX, DW).
- Odd one out: find the property shared by all but one (cubes, primes, capitals, vegetables).

```svgfig label="15.1" caption="Five series solved by the same routine. Write the differences under each term. A constant difference means an AP; differences that rise by a constant (here 2) mean a quadratic such as n(n + 1) or n^2 + 1; differences that double mean 2x + 1; a ratio that stays the same means a GP; and when the differences reproduce the series itself it is Fibonacci. The amber box is the next term, computed in the cell: 42, 63, 37, 13 and 162."
f = Fig(780, 330)
rows = []
S = [2 * 3 * 0 + n * (n + 1) for n in range(1, 7)]
assert S == [2, 6, 12, 20, 30, 42] and [b - a for a, b in zip(S, S[1:])] == [4, 6, 8, 10, 12]
rows.append(("n(n + 1)", S, ["+%d" % (b - a) for a, b in zip(S, S[1:])]))
T = [3]
for _ in range(4): T.append(2 * T[-1] + 1)
assert T == [3, 7, 15, 31, 63]
rows.append(("double and add 1", T, ["+%d" % (b - a) for a, b in zip(T, T[1:])]))
U = [n * n + 1 for n in range(1, 7)]
assert U == [2, 5, 10, 17, 26, 37] and [b - a for a, b in zip(U, U[1:])] == [3, 5, 7, 9, 11]
rows.append(("n^2 + 1", U, ["+%d" % (b - a) for a, b in zip(U, U[1:])]))
F = [1, 1]
for _ in range(5): F.append(F[-1] + F[-2])
assert F == [1, 1, 2, 3, 5, 8, 13]
rows.append(("Fibonacci", F, ["+%d" % (b - a) for a, b in zip(F, F[1:])]))
G = [2 * 3 ** k for k in range(5)]
assert G == [2, 6, 18, 54, 162] and all(b == 3 * a for a, b in zip(G, G[1:]))
rows.append(("GP, ratio 3", G, ["x3"] * 4))
for i, (nm, seq, dif) in enumerate(rows):
    y = 24 + i * 58
    f.text(20, y + 18, nm, size=11, color=NAVY, anchor="start", bold=True)
    for j, v in enumerate(seq):
        x = 190 + j * 54
        last = (j == len(seq) - 1)
        f.box(x, y, 46, 26, str(v), fill=("#fde68a" if last else BLUE), stroke=(AMBER if last else NAVY), size=11, bold=True)
        if j < len(dif): f.text(x + 50, y + 42, dif[j], size=10.5, color=(TEAL if dif[j] != "x3" else RED), bold=True)
f.text(700, 44, "Order of tests", size=11, color=NAVY, bold=True)
for j, t in enumerate(["1. differences", "2. second differences", "3. ratios", "4. squares, cubes", "5. primes, Fibonacci"]):
    f.text(642, 74 + j * 24, t, size=10.5, color=SLATE, anchor="start")
f.text(700, 224, "2 interleaved series?", size=10.5, color=RED, bold=True)
f.text(700, 244, "split odd and even places", size=10.5, color=SLATE)
```

## 15.2 Calendar problems

- Odd days: ordinary year 1, leap year 2. 100 years have 5, 200 have 3, 300 have 1, 400 have 0.
- Leap year: divisible by 4; century years only if divisible by 400 (2000 yes; 1900, 2100 no).
- Months: 31 days → 3 odd days; 30 days → 2; February 28 → 0 (29 → 1).
- Day after $n$ days: $n \mathrm{mod} 7$ steps forward. 100 days after Monday is Wednesday ($100=14\times7+2$).
- 1 January 2026 is a Thursday, so 1 January 2027 is a Friday (2026 is not a leap year), and 5 March 2026 (day 64) is also a Thursday.

```photogrid label="15.1" cols="2" ratio="1.1" caption="Two ways of measuring days and hours. (a) Pope Gregory XIII (1502-1585), whose 1582 reform gave us the rule used in every calendar question: a year is a leap year if it is divisible by 4, except century years, which must be divisible by 400. (b) A sundial on a church porch: the shadow of the pointer turns round the dial, which is why a morning shadow falls to the west and an evening shadow to the east."
@ photo id="bcamath/gregory" cap="Gregory XIII and the leap-year rule"
focus 0.5 0.3
@ photo id="bcamath/sundial" cap="A sundial tells time by a shadow"
focus 0.5 0.4
```

```svgfig label="15.2" caption="Calendar arithmetic, all verified with Python date functions. The month grid is March 2026: 1 March is a Sunday, so every Thursday is highlighted and 5 March (amber) is the first. Because 2026 is not a leap year, 1 January 2026 (Thursday) is followed by 1 January 2027 on a Friday. The table counts odd days in the first 100, 200, 300 and 400 years with the Gregorian leap rule: 5, 3, 1, 0. The average year is 365.2425 days."
import calendar, datetime
calendar.setfirstweekday(6)
assert datetime.date(2026, 3, 1).weekday() == 6 and datetime.date(2026, 3, 5).weekday() == 3
assert datetime.date(2026, 1, 1).weekday() == 3 and datetime.date(2027, 1, 1).weekday() == 4 and not calendar.isleap(2026)
assert (0 + 100) % 7 == 2
def odd(Y):
    leaps = sum(1 for y in range(1, Y + 1) if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0)
    return (Y + leaps) % 7, leaps
assert [odd(Y)[0] for Y in (100, 200, 300, 400)] == [5, 3, 1, 0] and [odd(Y)[1] for Y in (100, 200, 300, 400)] == [24, 48, 72, 97]
assert (365 * 400 + 97) / 400 == 365.2425
assert [calendar.isleap(y) for y in (1900, 2000, 2024, 2100)] == [False, True, True, False]
f = Fig(780, 330)
f.text(130, 24, "March 2026", size=12, color=NAVY, bold=True)
for j, d in enumerate("SMTWTFS"):
    f.box(20 + j * 36, 36, 34, 22, d, fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
for r, wk in enumerate(calendar.monthcalendar(2026, 3)):
    for j, dd in enumerate(wk):
        if dd == 0: continue
        th = (j == 4)
        f.box(20 + j * 36, 62 + r * 28, 34, 24, str(dd), fill=("#fde68a" if dd == 5 else ("#bfdbfe" if th else SOFT)), stroke=(AMBER if dd == 5 else "#cbd5e1"), color=SLATE, size=10.5, bold=th)
f.text(130, 250, "Thursdays: 5, 12, 19, 26", size=10.5, color=NAVY, bold=True)
f.text(130, 272, "1 Jan 2026 Thu, 1 Jan 2027 Fri (+1 odd day)", size=10.5, color=SLATE)
f.text(130, 294, "100 days after Mon: 100 mod 7 = 2, Wed", size=10.5, color=TEAL, bold=True)
f.text(130, 316, "5 Mar = day 64, 63 = 9 x 7 days after 1 Jan", size=10.5, color=SLATE)
f.text(540, 24, "Odd days in the first n years", size=12, color=NAVY, bold=True)
for j, hd in enumerate(["years", "leap years", "days + leaps", "odd days"]):
    f.box(320 + j * 112, 36, 108, 24, hd, fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
for i, Y in enumerate((100, 200, 300, 400)):
    o, lp = odd(Y)
    for j, t in enumerate([str(Y), str(lp), "%d + %d = %d" % (Y, lp, Y + lp), str(o)]):
        f.box(320 + j * 112, 62 + i * 28, 108, 24, t, fill=(MINT if j == 3 else SOFT), stroke="#cbd5e1", color=(TEAL if j == 3 else SLATE), size=10.5, bold=(j == 3))
f.text(540, 190, "Leap year test", size=11.5, color=NAVY, bold=True)
for j, (y, ok) in enumerate([(1900, False), (2000, True), (2024, True), (2100, False)]):
    f.box(330 + j * 108, 204, 100, 26, "%d: %s" % (y, "leap" if ok else "not leap"), fill=(MINT if ok else ROSE), stroke=(TEAL if ok else RED), color=(TEAL if ok else RED), size=10.5, bold=True)
f.text(540, 262, "month with 31 days = 3 odd days, 30 days = 2, February = 0 (leap year 1)", size=10.5, color=SLATE)
f.text(540, 288, "one leap year in 4, but 3 are skipped in 400: 97 per 400", size=10.5, color=NAVY, bold=True)
f.text(540, 312, "average year = 365.2425 days", size=10.5, color=RED, bold=True)
```

## 15.3 Clock problems

- Minute hand: 6° per minute; hour hand: 0.5° per minute. Angle $=|30H-5.5M|$ (take 360° minus it if it exceeds 180°).
- In 12 hours the hands coincide 11 times, are at right angles 22 times and opposite 11 times; in a day, 22, 44 and 22.
- Examples: 3:00 → 90°; 4:00 → 120°; 3:30 → 75°; 7:20 → 100°; 9:15 → 172.5°.

```photogrid label="15.2" cols="2" ratio="1.05" caption="Two real clock faces for the angle questions. (a) The inner face of the Big Ben clock in London, with Roman numerals and a long minute hand: the minute hand moves 6 degrees a minute and the short hour hand 0.5 degrees a minute. (b) A clock on a brick tower: at a time like 3 o'clock the hands make exactly 90 degrees, the standard right angle of the hands."
@ photo id="bcamath/bigben" cap="Big Ben: minute hand 6 deg/min"
focus 0.5 0.5
@ photo id="bcamath/clock2" cap="Hands at right angles: 90 deg"
focus 0.5 0.5
```

```svgfig label="15.3" caption="Clock angles drawn from the formula. The hour hand sits at 30H + 0.5M degrees and the minute hand at 6M degrees, so the angle between them is |30H - 5.5M|, or 360 minus that when it is more than 180. Computed here: 3:30 gives 75, 9:15 gives 187.5 which is 172.5 after reduction, and 7:20 gives 100. The table lists when the hands coincide: every 720/11 minutes, so 11 times in 12 hours. Counting in the cell also gives 22 right angles and 11 opposite positions."
import math
def ang(H, M):
    a = abs(30 * H - 5.5 * M)
    return 360 - a if a > 180 else a
assert (ang(3, 0), ang(4, 0), ang(3, 30), ang(7, 20), ang(9, 15)) == (90, 120, 75, 100, 172.5)
co = [k * 720 / 11 for k in range(12) if k * 720 / 11 < 720]
assert len(co) == 11
cnt = lambda target: len([t for t in [(target + 360 * j) / 5.5 for j in range(12)] if 0 <= t < 720])
assert cnt(180) == 11 and cnt(90) + cnt(270) == 22 and cnt(0) == 11
def hms(m):
    h = int(m // 60); mm = m - 60 * h; s = round((mm - int(mm)) * 60); mi = int(mm)
    if s == 60: s = 0; mi += 1
    return "%d:%02d:%02d" % (h if h else 12, mi, s)
assert hms(co[1]) == "1:05:27" and hms(co[2]) == "2:10:55" and hms(co[3]) == "3:16:22"
f = Fig(780, 330)
for (cx, cy, H, M) in [(90, 100, 3, 30), (260, 100, 9, 15), (430, 100, 7, 20)]:
    f.circle(cx, cy, 70, fill="#ffffff", stroke=NAVY, sw=2.4)
    for k in range(12):
        a = math.radians(30 * k)
        f.line(cx + 62 * math.sin(a), cy - 62 * math.cos(a), cx + 69 * math.sin(a), cy - 69 * math.cos(a), color=NAVY, sw=1.6)
    for k, t in [(0, "12"), (3, "3"), (6, "6"), (9, "9")]:
        a = math.radians(30 * k); f.text(cx + 50 * math.sin(a), cy - 50 * math.cos(a) + 4, t, size=10.5, color=SLATE, bold=True)
    ah = math.radians(30 * H + 0.5 * M); am = math.radians(6 * M)
    f.line(cx, cy, cx + 38 * math.sin(ah), cy - 38 * math.cos(ah), color=NAVY, sw=4)
    f.line(cx, cy, cx + 56 * math.sin(am), cy - 56 * math.cos(am), color=RED, sw=2.4)
    f.circle(cx, cy, 3.5, fill=NAVY, stroke=NAVY)
    f.text(cx, 196, "%d:%02d" % (H, M), size=12, color=NAVY, bold=True)
    raw = abs(30 * H - 5.5 * M)
    f.text(cx, 218, "|30 x %d - 5.5 x %d| = %s" % (H, M, ("%g" % raw)), size=10.5, color=SLATE)
    f.text(cx, 240, "angle = %g degrees" % ang(H, M), size=11, color=(RED if raw > 180 else TEAL), bold=True)
f.text(260, 264, "reduce a reflex angle: 360 - 187.5 = 172.5", size=10.5, color=RED, bold=True)
f.text(260, 292, "hour hand (short, thick, navy): 0.5 deg per minute;  minute hand (long, red): 6 deg per minute", size=10.5, color=SLATE)
f.text(260, 316, "relative speed 5.5 deg per minute", size=10.5, color=NAVY, bold=True)
f.text(650, 24, "Hands coincide at", size=11.5, color=NAVY, bold=True)
for j in range(6):
    f.text(580, 54 + j * 26, "%d)" % (j + 1), size=10.5, color=SLATE, anchor="start", bold=True)
    f.text(612, 54 + j * 26, hms(co[j]), size=10.5, color=NAVY, anchor="start")
f.text(650, 224, "12 hours: 11 coincide,", size=10.5, color=TEAL, bold=True)
f.text(650, 244, "22 right angles, 11 opposite", size=10.5, color=TEAL, bold=True)
f.text(650, 270, "one day: 22, 44, 22", size=10.5, color=RED, bold=True)
```

## 15.4 Counting figures, dice and cubes

- **Squares** in an $n\times n$ grid: $\frac{n(n+1)(2n+1)}{6}$ (2×2: 5, 3×3: 14, 4×4: 30, chessboard: 204). Rectangles in an $m\times n$ grid: $\binom{m+1}{2}\binom{n+1}{2}$ (2×2: 9).
- **Dice**: opposite faces sum to 7 (1–6, 2–5, 3–4). A cube has 6 faces, 8 corners, 12 edges.
- **Painted cube** of side $n$ cut into unit cubes: 3 faces painted 8; 2 faces $12(n-2)$; 1 face $6(n-2)^2$; none $(n-2)^3$. For $n=3$: 8, 12, 6, 1.

```photogrid label="15.3" cols="3" ratio="1.0" caption="Real objects for counting questions. (a) A Rubik's cube is a 3 x 3 x 3 cube of 27 small cubes: 8 corner pieces, 12 edge pieces, 6 centres and 1 hidden core, the same split as the painted cube (Fig 15.5). (b) A chessboard is an 8 x 8 grid that hides 204 squares of every size (Fig 15.4). (c) A die has 6 faces, 8 corners and 12 edges, and opposite faces add up to 7."
@ photo id="bcamath/rubik" cap="3 x 3 x 3 = 27 small cubes"
focus 0.5 0.5
@ photo id="bcamath/chess" cap="8 x 8 board, 204 squares"
focus 0.5 0.5
@ photo id="bcamath/dice" cap="Opposite faces add to 7"
focus 0.5 0.5
```

```svgfig label="15.4" caption="How many squares? A 4 x 4 grid holds 16 + 9 + 4 + 1 = 30 squares, not 16: count squares of every size. The cell finds the numbers by brute force and checks them against n(n + 1)(2n + 1)/6: 1, 5, 14, 30, 55, 91, 140, 204 for n = 1 to 8, so the chessboard has 204. Rectangles in an m x n grid are C(m + 1, 2) x C(n + 1, 2): a 2 x 2 grid has 9 and a chessboard has 1296."
import itertools
def squares(n): return sum(1 for s in range(1, n + 1) for x in range(n) for y in range(n) if x + s <= n and y + s <= n)
def rects(m, n): return sum(1 for x1, x2 in itertools.combinations(range(m + 1), 2) for y1, y2 in itertools.combinations(range(n + 1), 2))
vals = [squares(n) for n in range(1, 9)]
assert vals == [1, 5, 14, 30, 55, 91, 140, 204] and all(squares(n) == n * (n + 1) * (2 * n + 1) // 6 for n in range(1, 12))
assert squares(4) == 16 + 9 + 4 + 1 and rects(2, 2) == 9 and rects(8, 8) == 1296 and rects(3, 3) == 36 and rects(4, 4) == 100
f = Fig(780, 330)
c = 42
for i in range(4):
    for j in range(4):
        f.box(30 + i * c, 40 + j * c, c, c, "", fill="#ffffff", stroke="#94a3b8")
f.box(30, 40, 4 * c, 4 * c, "", fill="none", stroke=NAVY)
f.box(30 + c * 1, 40 + c * 1, 2 * c, 2 * c, "", fill="none", stroke=RED)
f.box(30 + c * 0, 40 + c * 0, 3 * c, 3 * c, "", fill="none", stroke=TEAL)
f.box(30 + 3 * c + 4, 40 + 3 * c + 4, c - 8, c - 8, "", fill="#fde68a", stroke=AMBER)
f.text(114, 30, "4 x 4 grid: sizes 1, 2, 3, 4", size=10.5, color=NAVY, bold=True)
for j, (t, col) in enumerate([("1 x 1: 16", AMBER), ("2 x 2: 9", RED), ("3 x 3: 4", TEAL), ("4 x 4: 1", NAVY)]):
    f.text(114, 232 + j * 22, t, size=10.5, color=col, bold=True)
f.text(114, 322, "16 + 9 + 4 + 1 = 30", size=11, color=NAVY, bold=True)
mx = max(vals)
for i, v in enumerate(vals):
    x = 270 + i * 58; h = 210 * v / mx
    f.box(x, 270 - h, 40, h, "", fill=("#fde68a" if i == 7 else "#bfdbfe"), stroke=(AMBER if i == 7 else NAVY))
    f.text(x + 20, 270 - h - 8, str(v), size=11, color=(RED if i == 7 else NAVY), bold=True)
    f.text(x + 20, 290, "%dx%d" % (i + 1, i + 1), size=10.5, color=SLATE)
f.text(520, 22, "squares in an n x n grid = n(n + 1)(2n + 1)/6", size=11.5, color=NAVY, bold=True)
f.text(520, 316, "rectangles in m x n = C(m + 1, 2) x C(n + 1, 2): 2 x 2 gives 9", size=10.5, color=TEAL, bold=True)
```

```svgfig label="15.5" caption="A die net and a painted cube. (a) The net folds into a die with 3 opposite 4, 1 opposite 6 and 5 opposite 2, and each pair adds up to 7; all six faces total 21, so if the visible faces show 2, 3 and 5 the hidden faces total 21 - 10 = 11. (b) A 3 x 3 x 3 cube is painted on the outside and cut into 27 unit cubes. The three layers show the number of painted faces on each small cube: 8 corners with 3 faces, 12 edge pieces with 2, 6 face centres with 1, and 1 core with none. The table gives the formulas 8, 12(n - 2), 6(n - 2)^2, (n - 2)^3 checked by brute force for n = 3, 4, 5."
import itertools
net = {(1, 0): 5, (0, 1): 3, (1, 1): 1, (2, 1): 4, (3, 1): 6, (1, 2): 2}
assert net[(0, 1)] + net[(2, 1)] == 7 and net[(1, 1)] + net[(3, 1)] == 7 and net[(1, 0)] + net[(1, 2)] == 7 and sum(net.values()) == 21 and 21 - (2 + 3 + 5) == 11
def painted(n):
    cnt = {0: 0, 1: 0, 2: 0, 3: 0}
    for x, y, z in itertools.product(range(n), repeat=3):
        k = sum(1 for v in (x, y, z) if v in (0, n - 1))
        cnt[k] += 1
    return cnt
for n in (3, 4, 5):
    p = painted(n)
    assert (p[3], p[2], p[1], p[0]) == (8, 12 * (n - 2), 6 * (n - 2) ** 2, (n - 2) ** 3) and sum(p.values()) == n ** 3
assert painted(3) == {0: 1, 1: 6, 2: 12, 3: 8}
PIPS = {1: [(.5, .5)], 2: [(.25, .25), (.75, .75)], 3: [(.25, .25), (.5, .5), (.75, .75)], 4: [(.25, .25), (.75, .25), (.25, .75), (.75, .75)], 5: [(.25, .25), (.75, .25), (.5, .5), (.25, .75), (.75, .75)], 6: [(.3, .22), (.3, .5), (.3, .78), (.7, .22), (.7, .5), (.7, .78)]}
f = Fig(780, 340)
cs = 54; x0, y0 = 24, 44
f.text(130, 26, "Die net: opposite faces add to 7", size=11.5, color=NAVY, bold=True)
for (i, j), v in net.items():
    f.box(x0 + i * cs, y0 + j * cs, cs, cs, "", fill="#ffffff", stroke=NAVY)
    for px, py in PIPS[v]:
        f.circle(x0 + i * cs + px * cs, y0 + j * cs + py * cs, 4.2, fill=NAVY, stroke=NAVY)
for j, t in enumerate(["3 + 4 = 7", "1 + 6 = 7", "5 + 2 = 7"]):
    f.text(130, 232 + j * 22, t, size=11, color=TEAL, bold=True)
f.text(130, 304, "all faces: 1+2+3+4+5+6 = 21", size=10.5, color=SLATE)
f.text(130, 324, "see 2, 3, 5 so hidden = 21 - 10 = 11", size=10.5, color=RED, bold=True)
COL = {3: "#fca5a5", 2: "#fde68a", 1: "#bfdbfe", 0: "#bbf7d0"}
f.text(480, 26, "3 x 3 x 3 cube, layer by layer (painted faces)", size=11.5, color=NAVY, bold=True)
for L, z in enumerate((2, 1, 0)):
    lx = 300 + L * 100
    f.text(lx + 39, 52, ["top layer", "middle layer", "bottom layer"][L], size=10.5, color=SLATE, bold=True)
    for x in range(3):
        for y in range(3):
            k = sum(1 for v in (x, y, z) if v in (0, 2))
            f.box(lx + x * 26, 60 + y * 26, 26, 26, str(k), fill=COL[k], stroke="#94a3b8", color=SLATE, size=11, bold=True)
for j, k in enumerate([3, 2, 1, 0]):
    f.box(604, 60 + j * 24, 20, 20, str(k), fill=COL[k], stroke="#94a3b8", color=SLATE, size=10.5, bold=True)
    f.text(634, 75 + j * 24, ["3 faces: 8", "2 faces: 12", "1 face: 6", "no face: 1"][j], size=10.5, color=NAVY, anchor="start", bold=True)
for j, hd in enumerate(["n", "3 faces", "2 faces", "1 face", "0 faces", "total"]):
    f.box(300 + j * 74, 176, 70, 24, hd, fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
for i, n in enumerate((3, 4, 5)):
    p = painted(n)
    for j, t in enumerate([n, p[3], p[2], p[1], p[0], sum(p.values())]):
        f.box(300 + j * 74, 202 + i * 26, 70, 24, str(t), fill=SOFT, stroke="#cbd5e1", color=SLATE, size=10.5, bold=(j in (0, 5)))
f.text(520, 300, "8,  12(n - 2),  6(n - 2)^2,  (n - 2)^3", size=11, color=TEAL, bold=True)
f.text(520, 322, "total = n^3 (27, 64, 125)", size=10.5, color=SLATE)
```

## 15.5 Eight traps in reasoning series and counting

These questions are won by method, not by speed. The eight traps below are the ones that make a student lose a mark on a question he or she could have solved.

1. **Look at the second differences before you give up.** For 2, 6, 12, 20, 30 the first differences 4, 6, 8, 10 are not constant, but the second differences are all 2, so the rule is quadratic and the next term is 42 (Fig 15.1). If the ratios are constant it is a GP instead. Always write the differences under the terms.
2. **A series can be two series woven together.** In 2, 10, 4, 20, 6, 40 the odd places give 2, 4, 6 and the even places give 10, 20, 40. If one rule does not fit all terms, split the odd and even places. Letter series are tested the same way after converting letters to positions.
3. **Know the neighbours of the squares.** The numbers 2, 5, 10, 17, 26 are $n^2+1$, while 0, 3, 8, 15, 24 are $n^2-1$. A series that rises faster than an AP but slower than a GP is usually squares or cubes. Compare each term with the nearest perfect square.
4. **Odd days are remainders, not days.** 100 years have 5 odd days, 200 have 3, 300 have 1 and 400 have 0 (Fig 15.2). Ordinary years add 1 odd day and leap years add 2. Always reduce the total modulo 7 at the end.
5. **A century year is a leap year only if it is divisible by 400.** So 2000 is a leap year but 1900 and 2100 are not (Fig 15.2). This one rule is the most common reason for a wrong day in the options. Check the divisibility by 400 first when you see a year ending in 00.
6. **Count the days from the right date.** 100 days after Monday is Wednesday, because $100=14\times7+2$. For "the day on 26 January" given 1 January, add 25 days, not 26. Remember that months with 31 days give 3 odd days and 30 days give 2.
7. **The clock formula needs two corrections.** The angle is $|30H-5.5M|$, and if the answer is more than 180 you subtract it from 360 (9:15 gives 187.5, which becomes 172.5; Fig 15.3). Use $H$ in the 12-hour form, so 15:00 means $H=3$. In 12 hours the hands coincide 11 times, not 12.
8. **Count every size, and remember what lies inside.** A 4 × 4 grid has 30 squares, not 16, and an 8 × 8 board has 204 (Fig 15.4). In a painted cube of side $n$ the pieces with no paint are $(n-2)^3$ and the edge pieces are $12(n-2)$ (Fig 15.5). On a die the opposite faces add to 7, but faces that touch each other can be any other pair.

### 15.5.1 Worked checks

**Q. Find the next term of 2, 6, 12, 20, 30, …**

**Answer.** The differences are 4, 6, 8, 10 and the second differences are all 2, so the term is $n(n+1)$. The next term is $6\times7=42$ (Fig 15.1).

**Q. 1 January 2026 is a Thursday. What day of the week is 26 January 2026?**

**Answer.** 26 January is $25$ days after 1 January, and $25=3\times7+4$. Four days after Thursday is **Monday**.

**Q. Find the angle between the hands at 7:20.**

**Answer.** The angle is $|30\times7-5.5\times20|=|210-110|=100^\circ$. It is less than 180, so it stays as it is (Fig 15.3).

**Q. A cube of side 4 cm is painted on all faces and cut into 1 cm cubes. How many have exactly two faces painted? How many have none?**

**Answer.** Edge pieces have two painted faces: $12(4-2)=24$. Pieces with no paint lie inside: $(4-2)^3=8$. Check: $8+24+24+8=64=4^3$ (Fig 15.5).

**Q. How many squares are there in a 5 × 5 grid?**

**Answer.** Count all sizes: $25+16+9+4+1=55$, which equals $\frac{5\cdot6\cdot11}{6}=55$ (Fig 15.4).

## Formula and fact sheet

| Item | Rule |
|---|---|
| Clock angle | $\lvert30H-5.5M\rvert$ |
| Odd days | 100 y = 5, 200 y = 3, 300 y = 1, 400 y = 0 |
| Squares in $n\times n$ | $\frac{n(n+1)(2n+1)}{6}$ |
| Painted cube | corners 8, edges $12(n-2)$, faces $6(n-2)^2$, inside $(n-2)^3$ |

## Chapter summary

- Check first and second differences, then squares, cubes, primes.
- Count odd days, then take the remainder by 7.
- Century years are leap only if divisible by 400.
- Use 5.5M for the clock; reduce reflex angles.
- Count squares of every size, not just the smallest.

## Practice questions

**Set A — Recall (20 questions)**

1. The next number in 2, 4, 8, 16 is
   (a) 24 (b) 30 (c) 32 (d) 64
2. The next number in 1, 4, 9, 16, 25 is
   (a) 36 (b) 30 (c) 49 (d) 35
3. The next number in 2, 6, 12, 20, 30 is
   (a) 40 (b) 36 (c) 44 (d) 42
4. The next letter in A, C, E, G is
   (a) H (b) I (c) J (d) K
5. The next number in 3, 6, 9, 12 is
   (a) 13 (b) 14 (c) 15 (d) 18
6. The number of odd days in 100 years is
   (a) 1 (b) 3 (c) 0 (d) 5
7. The number of odd days in 400 years is
   (a) 0 (b) 1 (c) 2 (d) 3
8. An ordinary year has how many odd days?
   (a) 0 (b) 1 (c) 2 (d) 7
9. The minute hand of a clock moves through how many degrees in one minute?
   (a) 0.5° (b) 1° (c) 12° (d) 6°
10. The angle between the hands of a clock at 3:00 is
    (a) 60° (b) 180° (c) 90° (d) 30°
11. On a standard die the face opposite 1 is
    (a) 6 (b) 5 (c) 3 (d) 2
12. A cube has how many corners?
    (a) 6 (b) 8 (c) 12 (d) 4
13. A cube has how many edges?
    (a) 8 (b) 6 (c) 12 (d) 10
14. Which of these is a leap year?
    (a) 1900 (b) 2100 (c) 2026 (d) 2000
15. The next number in 5, 10, 20, 40 is
    (a) 80 (b) 60 (c) 70 (d) 100
16. The hands of a clock coincide how many times in 12 hours?
    (a) 12 (b) 11 (c) 10 (d) 22
17. The next number in 2, 3, 5, 7, 11 is
    (a) 12 (b) 14 (c) 13 (d) 15
18. In a leap year February has
    (a) 28 days (b) 30 days (c) 27 days (d) 29 days
19. Which is the odd one out?
    (a) Potato (b) Mango (c) Banana (d) Apple
20. The next number in 1, 8, 27, 64 is
    (a) 100 (b) 125 (c) 81 (d) 216

::: note Answers and explanations — Set A
**1.** (c) — doubling.
**2.** (a) — perfect squares, 6² = 36.
**3.** (d) — n(n + 1): 1·2, 2·3, …, 6·7 = 42.
**4.** (b) — every second letter.
**5.** (c) — add 3.
**6.** (d) — 100 years = 76 ordinary + 24 leap years: 76 + 48 = 124 odd days = 17 weeks + 5 days.
**7.** (a) — the 400-year cycle repeats exactly.
**8.** (b) — 365 = 52 weeks + 1 day.
**9.** (d) — 360° in 60 minutes.
**10.** (c) — hands at 12 and 3.
**11.** (a) — opposite faces sum to 7.
**12.** (b) — 8 vertices.
**13.** (c) — 12 edges.
**14.** (d) — 2000 is divisible by 400; 1900 and 2100 are not; 2026 is not a multiple of 4.
**15.** (a) — doubling.
**16.** (b) — 11 times (not 12: the 12th coincidence is the start of the next cycle).
**17.** (c) — the next prime.
**18.** (d) — 29 days.
**19.** (a) — a vegetable among fruits.
**20.** (b) — cubes: 5³ = 125.
:::

**Set B — Understanding (12 questions)**

1. The next number in 1, 1, 2, 3, 5, 8 is
   (a) 11 (b) 12 (c) 10 (d) 13
2. If today is Monday, the day after 100 days is
   (a) Tuesday (b) Wednesday (c) Thursday (d) Monday
3. The angle between the hands at 4:00 is
   (a) 120° (b) 150° (c) 90° (d) 100°
4. The angle between the hands at 3:30 is
   (a) 90° (b) 60° (c) 75° (d) 105°
5. The number of squares of all sizes in a 3 × 3 grid is
   (a) 9 (b) 14 (c) 13 (d) 10
6. A 3 × 3 × 3 painted cube is cut into 27 unit cubes. The number with exactly one face painted is
   (a) 8 (b) 12 (c) 1 (d) 6
7. In the same cube the number with exactly two faces painted is
   (a) 6 (b) 8 (c) 12 (d) 1
8. The next number in 3, 7, 15, 31 is
   (a) 63 (b) 62 (c) 47 (d) 51
9. 1 January 2026 is a Thursday. 1 January 2027 is a
   (a) Thursday (b) Saturday (c) Sunday (d) Friday
10. The next pair in AZ, BY, CX is
    (a) DX (b) DW (c) EW (d) CW
11. The number of rectangles of all sizes in a 2 × 2 grid is
    (a) 9 (b) 4 (c) 8 (d) 10
12. In one day the hands of a clock coincide
    (a) 11 times (b) 24 times (c) 22 times (d) 44 times

::: note Answers and explanations — Set B
**1.** (d) — Fibonacci: 5 + 8 = 13.
**2.** (b) — 100 = 14 × 7 + 2, so two days after Monday.
**3.** (a) — 4 × 30°.
**4.** (c) — |30·3 − 5.5·30| = |90 − 165| = 75°.
**5.** (b) — 9 + 4 + 1.
**6.** (d) — 6 face centres: 6(3 − 2)² = 6.
**7.** (c) — 12 edge cubes.
**8.** (a) — each term is double the last plus 1.
**9.** (d) — 365 days is 1 odd day.
**10.** (b) — first letter moves forward, second backward.
**11.** (a) — C(3,2) × C(3,2) = 9.
**12.** (c) — 11 per half day.
:::

**Set C — Application (8 questions)**

1. The next number in 2, 5, 10, 17, 26 is
   (a) 35 (b) 37 (c) 36 (d) 40
2. 1 January 2026 was a Thursday, so 5 March 2026 (Nepal's election day) fell on a
   (a) Monday (b) Tuesday (c) Wednesday (d) Thursday
3. The angle between the hands at 7:20 is
   (a) 100° (b) 110° (c) 90° (d) 120°
4. The smaller angle between the hands at 9:15 is
   (a) 180° (b) 165° (c) 172.5° (d) 187.5°
5. A 4 × 4 × 4 painted cube is cut into 64 unit cubes. The number with no painted face is
   (a) 4 (b) 16 (c) 24 (d) 8
6. The number of squares of all sizes in a 4 × 4 grid is
   (a) 16 (b) 30 (c) 20 (d) 25
7. Which of these is NOT a leap year?
   (a) 2100 (b) 2000 (c) 2024 (d) 2028
8. The next number in 1, 2, 6, 24, 120 is
   (a) 240 (b) 480 (c) 720 (d) 600

::: note Answers and explanations — Set C
**1.** (b) — n² + 1 with n = 6.
**2.** (d) — 63 days after 1 January: 63 = 9 weeks exactly, so the same weekday.
**3.** (a) — |210 − 110| = 100°.
**4.** (c) — |270 − 82.5| = 187.5°, so the smaller angle is 172.5°.
**5.** (d) — (4 − 2)³ = 8.
**6.** (b) — 16 + 9 + 4 + 1.
**7.** (a) — 2100 is a century year not divisible by 400.
**8.** (c) — factorials: 6! = 720.
:::
