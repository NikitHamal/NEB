---
subject: Mental Agility Test
grade: CEE
unit: 3
title: Logical Sequencing
hours: 5
area: Mental Agility Test
---

Logical sequencing carries **5 of the 20 MAT questions**. A sequence of numbers,
letters or letter–number groups follows a hidden rule, and you must find the next term,
a missing term or the one term that breaks the rule. The same skill reads number grids
and "missing number" figures, and it also covers the two calendar-and-clock types that
every reasoning paper includes. The official MEC sample is a number series in which
each term appears twice (53, 53, 40, 40, 27, 27, …). The whole chapter rests on one
habit: **write the differences (or the ratios) under the terms before you guess**.

::: key What the paper asks from this chapter
- **Number series**: constant difference, constant ratio, differences that themselves
  form a series, squares and cubes ± a constant, primes, "add the last two", and two
  series interleaved.
- **Letter series**: turn letters into positions (A = 1 … Z = 26) and treat them as
  numbers; opposite letters add to 27.
- **Grids and figures**: the same operation in every row (or column, or figure) —
  sum, product, (a × b) − c, squares — found from the complete rows and applied to the
  incomplete one.
- **Calendar**: odd days — an ordinary year has 1, a leap year 2; a month of 31 days
  has 3, of 30 days 2. Century years are leap years only if divisible by 400.
- **Clock**: the angle between the hands is $|30H - 5.5M|$ degrees; the hands meet
  22 times a day.
- **Mirror clock**: the real time is 11:60 minus the time shown in the mirror.
:::

## 3.1 Number series

### The method in four steps

1. **Differences.** Write the difference between each pair of neighbours. Constant →
   arithmetic series. If the differences form their own pattern (2, 4, 6, 8 or
   2, 4, 8, 16), continue that pattern.
2. **Ratios.** If the terms grow fast, divide each term by the one before it. Constant
   ratio → geometric series; ratios ×2, ×3, ×4 … → a factorial-type series.
3. **Known numbers.** Look for squares, cubes, primes, or these ± 1. Squares and cubes
   near the terms are the first suspects (24, 35, 48 are $5^2 - 1$, $6^2 - 1$,
   $7^2 - 1$).
4. **Two series in one.** If nothing fits, split the odd-numbered and even-numbered
   positions — each may be a simple series of its own. Also check for repeated terms
   (the MEC sample).

| Type | Example | Rule | Next |
|---|---|---|---|
| Arithmetic | 7, 11, 15, 19 | +4 | 23 |
| Geometric | 5, 15, 45, 135 | ×3 | 405 |
| Differences in AP | 2, 6, 12, 20, 30 | +4, +6, +8, +10 | 42 |
| Differences in GP | 5, 7, 11, 19, 35 | +2, +4, +8, +16 | 67 |
| Squares ± k | 3, 8, 15, 24, 35 | $n^2 - 1$ | 48 |
| Cubes ± k | 2, 9, 28, 65 | $n^3 + 1$ | 126 |
| Primes | 11, 13, 17, 19, 23 | consecutive primes | 29 |
| Fibonacci type | 2, 3, 5, 8, 13 | add the last two | 21 |
| × then + | 3, 7, 15, 31 | ×2 + 1 | 63 |
| Growing multiplier | 1, 2, 6, 24, 120 | ×2, ×3, ×4, ×5 | 720 |
| Interleaved | 1, 10, 3, 9, 5, 8 | 1, 3, 5 … and 10, 9, 8 … | 7 |
| Repeated pairs | 53, 53, 40, 40, 27, 27 | each term twice, −13 | 14 |

::: example The MEC sample question
**Problem.** Look at this series: 53, 53, 40, 40, 27, 27, … Which number should come
next? (A) 12 (B) 14 (C) 27 (D) 53

**Solution.** Each number is written twice, and the distinct numbers fall by 13:
53 → 40 → 27 → **14** (key B). The next pair would be 14, 14. Option C (27) is the
trap for students who think the series has to repeat 27 a third time.
:::

::: example Differences that double
**Problem.** 5, 7, 11, 19, 35, ?

**Solution.** Differences: 2, 4, 8, 16 — each doubles. The next difference is 32, so
the next term is 35 + 32 = **67**.
:::

::: example Two series interleaved
**Problem.** 1, 10, 3, 9, 5, 8, 7, ?

**Solution.** The differences (+9, −7, +6, −4 …) have no pattern, so split the positions.
Odd places: 1, 3, 5, 7 (+2). Even places: 10, 9, 8, ? (−1). The 8th term is in the even
series: **7**.
:::

### The wrong term

"Find the wrong number" uses the same method. Write the differences; the wrong term
spoils *two* neighbouring differences, one too big and one too small. In 3, 5, 9, 17,
34, 65 the differences are 2, 4, 8, 17, 31; the doubling pattern 2, 4, 8, 16, 32 is
restored when 34 is replaced by 33. So **34** is wrong.

::: caution Do not stop at the first rule that fits three terms
Many rules fit three terms; the right rule fits *every* term. Check your rule on the
whole series before you look at the options — and if two rules fit, the options usually
contain only one of the two answers. When none of the options matches, you have the
wrong rule, not a wrong question.
:::

```photogrid label="3.1" cols="2" ratio="1.2" caption="A famous series: 1, 1, 2, 3, 5, 8, 13, 21 ... in which each term is the sum of the two before it. (a) A chambered nautilus: its shell grows as a logarithmic spiral, often compared with the Fibonacci spiral, though the nautilus ratio is not exactly golden. (b) The ratio of each term to the one before it, 1, 2, 1.5, 1.67, 1.6, 1.625 ..., zig-zags and settles at 1.618, the golden ratio (1 + sqrt 5) / 2. By the twelfth term (144) the ratio 233 / 144 = 1.6181 agrees with it to three decimal places. In a number-series question, test the differences first, then the ratios, then sums of two or three previous terms, and finally squares, cubes and alternating patterns."
@ photo id="ceemat/nautilus" cap="A chambered nautilus"
fit 1.2
focus 0.5 0.45
@ svg cap="Ratio of successive Fibonacci terms"
F = [1, 1]
while len(F) < 14:
    F.append(F[-1] + F[-2])
rt = [F[i + 1] / F[i] for i in range(12)]
phi = (1 + 5 ** 0.5) / 2
assert F[:12] == [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144] and F[12] == 233
assert abs(rt[-1] - phi) < 1e-3 and round(rt[-1], 4) == 1.6181
f = Fig(300, 236)
f.text(150, 12, "Ratio F(n+1) / F(n) settles at 1.618", size=10.5, color=NAVY, bold=True)
ax = Axes(f, 44, 28, 234, 150, (1, 12), (0.8, 2.2))
ax.grid(1, 0.4, yfmt=lambda v: "%.1f" % v).axes("n", "ratio")
ax.hline(phi, color=AMBER)
for i in range(11):
    f.line(ax.X(i + 1), ax.Y(rt[i]), ax.X(i + 2), ax.Y(rt[i + 1]), color=RED, sw=1.6)
for i in range(12):
    ax.pt(i + 1, rt[i], "", r=3)
f.text(ax.X(12), ax.Y(phi) - 8, "1.618", size=10.5, color=AMBER, bold=True, anchor="end")
f.text(150, 206, "1, 2, 1.5, 1.67, 1.6, 1.625, 1.615 ...", size=10.5, color=NAVY, bold=True)
f.text(150, 222, "F13 / F12 = 233 / 144 = 1.6181", size=10.5, color=SLATE, bold=True)
```

## 3.2 Letter and alphanumeric series

Change every letter to its position and the letter series becomes a number series.
Count forwards past Z by subtracting 26 (Z + 2 = B).

| A | B | C | D | E | F | G | H | I | J | K | L | M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |

| N | O | P | Q | R | S | T | U | V | W | X | Y | Z |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |

| Type | Example | Rule | Next |
|---|---|---|---|
| Fixed skip | D, G, J, M | +3 | P |
| Growing skip | A, D, H, M | +3, +4, +5 | S (13 + 6 = 19) |
| Backwards | Y, V, S, P | −3 | M |
| Opposite pairs | AZ, BY, CX | first letter +1, second −1 (sum 27) | DW |
| Groups | ABD, DEG, GHJ | each group +3; inside a group +1, +2 | JKM |
| Alphanumeric | B2, D4, F6 | letter +2, number = letter's position | H8 |
| Letter and number apart | KM5, IP8, GS11 | −2 / +3 / +3 | EV14 |

### Repeating-letter series (fill the blanks)

A string like **a _ b a a _ a a b _ a b** hides a short block repeated. Try blocks of 2,
3 and 4 letters until the given letters all fit: here the block is *aab* (a a b | a a b
| a a b | a a b), so the blanks are **a, b, a**. Count the letters: the total length is
usually a multiple of the block length.

::: example A growing skip
**Problem.** A, D, H, M, ?

**Solution.** Positions 1, 4, 8, 13: differences +3, +4, +5. Next +6: 13 + 6 = 19 =
**S**.
:::

::: memory Positions without counting
E J O T Y = 5, 10, 15, 20, 25 ("EJOTY"). Any letter is at most two steps from one of
them: P = O + 1 = 16, W = Y − 2 = 23. The opposite letter is at 27 − position (H ↔ S).
:::

## 3.3 Patterns in grids and missing-number figures

The figure (a grid, circles, triangles, a wheel) hides one operation that is the same
in every row, column or figure. **Find it from the complete parts, then apply it to the
incomplete part.** Try, in this order:

1. Sum of the row (or column) is constant, or the third number = first + second.
2. Product: third = first × second; or the centre = the product of the corners.
3. Mixed: (first + second) × k, first × second − third, (a × b) − (c × d).
4. Squares and cubes: third = first² + second², or a square in the centre.
5. Rows versus columns: if no row rule works, try columns; then try the diagonals.

```figure caption="A missing-number grid. Rows 1 and 2 show the rule: (first + second) × 2 = third. Row 3 gives (4 + 6) × 2 = 20."
fig, ax = plt.subplots(figsize=(4.0, 2.4))
rows = [['5', '3', '16'], ['7', '2', '18'], ['4', '6', '?']]
for i, r in enumerate(rows):
    for j, t in enumerate(r):
        fc = '#fde9c8' if t == '?' else 'white'
        ax.add_patch(Rectangle((j, 2-i), 1, 1, fc=fc, ec=INK, lw=1.2))
        ax.text(j+0.5, 2-i+0.5, t, ha='center', va='center', fontsize=12, fontweight='bold')
notes = ['(5 + 3) × 2 = 16', '(7 + 2) × 2 = 18', '(4 + 6) × 2 = 20']
for i, n in enumerate(notes):
    ax.text(3.35, 2-i+0.5, n, ha='left', va='center', fontsize=9, color=SERIES[1] if i == 2 else MUTED)
ax.set_xlim(-0.1, 6.0); ax.set_ylim(-0.1, 3.1); ax.set_aspect('equal'); ax.axis('off')
```

::: example Checking a grid rule
**Problem.** In the grid above, which number replaces the question mark?

**Solution.** Row 1: 5 + 3 = 8 and 8 × 2 = 16. Row 2: 7 + 2 = 9 and 9 × 2 = 18. The
rule holds for both complete rows, so row 3 gives (4 + 6) × 2 = **20**. (A product
rule fails at once: 5 × 3 = 15, not 16.)
:::

::: tip A rule must work for every complete row
A rule that explains one row is a guess; a rule that explains two rows is an answer.
If two different rules both fit the complete rows, they will usually give the same
answer — if they do not, look again at the options.
:::

## 3.4 Calendar and clock reasoning

### Calendar: odd days

An **odd day** is a day left over after counting complete weeks. Days of the week
repeat every 7 days, so only the remainder on division by 7 matters.

| Period | Days | Odd days |
|---|---|---|
| Ordinary year | 365 = 52 weeks + 1 day | 1 |
| Leap year | 366 = 52 weeks + 2 days | 2 |
| Month of 31 days | 31 = 4 weeks + 3 | 3 |
| Month of 30 days | 30 = 4 weeks + 2 | 2 |
| February | 28 or 29 | 0 or 1 |
| 100 years | 76 ordinary + 24 leap | 5 |
| 200 / 300 / 400 years | | 3 / 1 / 0 |

**Leap year rule.** A year is a leap year if it is divisible by 4 — except century
years (1900, 2100), which are leap years only if divisible by 400 (2000 was a leap
year; 1900 was not).

**Day of the week.** Count the odd days and move that many days forward. With the
odd-day method from the start of the calendar, 0 odd days = Sunday, 1 = Monday, …,
6 = Saturday.

::: example A date from history
**Problem.** Tenzing Norgay and Edmund Hillary first reached the summit of Mount Everest
on 29 May 1953. What day of the week was it?

**Solution.** Count odd days up to that date. 1600 years: 0. 1601–1900 (300 years): 1.
1901–1952: 52 years with 13 leap years: 52 + 13 = 65 → 65 − 63 = 2. 1953 up to 29 May:
January 3 + February 0 + March 3 + April 2 + 29 days of May (1) = 9 → 2. Total =
0 + 1 + 2 + 2 = 5 → **Friday**.
:::

| Fact | Rule |
|---|---|
| Same date next year | 1 day later (2 days if a 29 February comes in between) |
| After n days | move forward n mod 7 days (100 days → 2 days on) |
| A year's calendar repeats | when the starting weekday and the leap/ordinary type both match (2026 → 2037) |
| Last day of a century | can only be Monday, Wednesday, Friday or Sunday |

### Clock: the angle between the hands

The minute hand moves 6° per minute; the hour hand moves 30° per hour, i.e. 0.5° per
minute. At H hours and M minutes:

$$ \theta = \left|30H - \frac{11}{2}M\right| $$

If θ comes out above 180°, the smaller angle is 360° − θ.

```figure caption="The clock at 3:40. The hour hand has moved two-thirds of the way from 3 to 4 (90° + 20° = 110° from 12); the minute hand is at 240°. The angle between them is |90 − 5.5 × 40| = 130°."
fig, ax = plt.subplots(figsize=(4.4, 3.0))
ax.add_patch(Circle((0, 0), 1.0, fc='white', ec=INK, lw=1.5))
for k in range(12):
    a = np.radians(90 - 30*k)
    ax.plot([0.88*np.cos(a), 1.0*np.cos(a)], [0.88*np.sin(a), 1.0*np.sin(a)], color=INK, lw=1.2)
    ax.text(0.77*np.cos(a), 0.77*np.sin(a), str(12 if k == 0 else k), ha='center', va='center', fontsize=8.6)
ah = np.radians(90 - 110); am = np.radians(90 - 240)
ax.plot([0, 0.44*np.cos(ah)], [0, 0.44*np.sin(ah)], color=INK, lw=3.0, solid_capstyle='round')
ax.plot([0, 0.62*np.cos(am)], [0, 0.62*np.sin(am)], color=ACCENT, lw=2.0, solid_capstyle='round')
th = np.linspace(ah, am, 60)
ax.plot(0.26*np.cos(th), 0.26*np.sin(th), color=SERIES[1], lw=1.4)
ax.text(0.0, -0.4, '130°', ha='center', va='center', fontsize=9.5, color=SERIES[1], fontweight='bold')
ax.plot([0], [0], 'o', color=INK, ms=4)
ax.text(1.25, 0.55, 'hour hand: 30 × 3 + 0.5 × 40\n= 110° from 12', ha='left', va='center', fontsize=8.6)
ax.text(1.25, -0.25, 'minute hand: 6 × 40\n= 240° from 12', ha='left', va='center', fontsize=8.6, color=ACCENT)
ax.text(1.25, -0.85, 'angle = 240° − 110° = 130°', ha='left', va='center', fontsize=8.8, color=SERIES[1])
ax.set_xlim(-1.15, 3.6); ax.set_ylim(-1.15, 1.15); ax.set_aspect('equal'); ax.axis('off')
```

| Clock fact | Value |
|---|---|
| Minute hand gains on the hour hand | 5.5° per minute (55 minute-spaces per hour) |
| Hands together between H and H + 1 o'clock | at $60H/11$ minutes past H |
| Hands together | every $65\frac{5}{11}$ minutes; 11 times in 12 hours, **22 times a day** |
| Hands at right angles | 22 times in 12 hours, **44 times a day** |
| Hands opposite (180°) | 11 times in 12 hours, **22 times a day** |
| Mirror image (vertical mirror) | real time = 11:60 − time seen (mirror 3:15 → 8:45) |
| Clock gaining g minutes per hour | after t true hours it is ahead by g × t minutes |

::: example Angle and coincidence
**Problem.** (i) What is the angle between the hands at 4:30? (ii) At what time between
4 and 5 o'clock are the hands together?

**Solution.** (i) |30 × 4 − 5.5 × 30| = |120 − 165| = **45°**. (ii) Hands together when
30H = 5.5M: M = 120/5.5 = 240/11 = **21 9/11 minutes past 4**.
:::

::: caution Two clock traps
At 4:30 the hour hand is *not* on the 4 — it is halfway to the 5. Answers like 60°
come from forgetting that the hour hand moves. And the mirror rule 11:60 − t is for a
mirror placed beside the clock; check one time in your head (mirror 3:00 must give
9:00) before using it.
:::

```photogrid label="3.2" cols="2" ratio="1.2" caption="Clock problems use relative speed. (a) A clock face with its hands. (b) The minute hand turns 6 degrees a minute and the hour hand 0.5 degrees a minute, so the minute hand gains 5.5 degrees a minute. The angle between the hands at H hours M minutes is |30H - 5.5M| (or 360 minus that if it exceeds 180). Over 12 hours the graph touches zero 11 times, not 12, because the hands overlap every 720 / 11 = 65 5/11 minutes: the first overlap is at 1 h 5 5/11 min. The hands are at right angles 22 times and in a straight line 11 times in 12 hours. At 3:00 the angle is 90 degrees and at 6:00 it is 180."
@ photo id="ceemat/clock" cap="A clock face with hour and minute hands"
fit 1.2
focus 0.5 0.5
@ svg cap="Angle between the hands over 12 hours"
ang = lambda t: min(abs(0.5 * t - 6 * (t % 60)) % 360, 360 - abs(0.5 * t - 6 * (t % 60)) % 360)
assert ang(180) == 90 and ang(0) == 0 and ang(360) == 180
assert all(ang(k * 720 / 11) < 1e-9 for k in range(11)) and round(720 / 11, 2) == 65.45
rt = sum(1 for k in range(60) if 0 <= (90 + 180 * k) / 5.5 < 720)
st = sum(1 for k in range(60) if 0 <= (180 + 360 * k) / 5.5 < 720)
assert rt == 22 and st == 11
f = Fig(300, 236)
f.text(150, 12, "Angle between the hands, 12 hours", size=10.5, color=NAVY, bold=True)
ax = Axes(f, 44, 28, 234, 150, (0, 720), (0, 180))
ax.grid(120, 90, xfmt=lambda v: "%dh" % (v // 60)).axes("time", "deg")
ax.curve(ang, 0, 720, color=NAVY, sw=1.5, n=1500)
for k in range(11):
    ax.pt(k * 720 / 11, 0, "", r=3, color=RED)
f.text(150, 206, "overlaps (red) every 65 5/11 min: 11 in 12 h", size=10.5, color=NAVY, bold=True)
f.text(150, 222, "right angle 22 times, straight line 11 times", size=10.5, color=SLATE, bold=True)
```

```photogrid label="3.3" cols="2" ratio="1.2" caption="Calendar problems use odd days, the days left over after taking out whole weeks. (a) A wall calendar with 24 October 2007 boxed. (b) Counting from year 1 of the Gregorian calendar, 100 years hold 24 leap years and so 36,524 days, which is 5 odd days; 200 years give 3, 300 years give 1 and 400 years give 0, so the calendar repeats exactly every 400 years. For 24 October 2007: 2000 years give 0, the six years 2001-2006 give 6 + 1 leap day = 7 = 0, and 1 January to 24 October is 297 days = 3 odd days; 0 + 0 + 3 = 3, which is Wednesday (Sunday = 0, Monday = 1 ...). The year 2000 was a leap year but 1900 was not: century years must be divisible by 400."
@ photo id="ceemat/calendar" cap="A wall calendar, 24 October 2007 boxed"
fit 1.2
focus 0.5 0.5
@ svg cap="Odd days in 100, 200, 300 and 400 years"
import datetime
leap = lambda y: y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)
odd = lambda n: sum(366 if leap(y) else 365 for y in range(1, n + 1)) % 7
vals = [odd(n) for n in (100, 200, 300, 400)]
assert vals == [5, 3, 1, 0]
days = sum((31, 28, 31, 30, 31, 30, 31, 31, 30)) + 24
o1 = (6 * 1 + sum(1 for y in range(2001, 2007) if leap(y))) % 7
assert days == 297 and days % 7 == 3 and o1 == 0 and datetime.date(2007, 10, 24).strftime("%A") == "Wednesday"
f = Fig(300, 236)
f.text(150, 12, "Odd days in whole centuries", size=10.5, color=NAVY, bold=True)
for i, (n, v) in enumerate(zip((100, 200, 300, 400), vals)):
    x = 44 + i * 62
    h = max(v * 13, 2)
    f.box(x, 100 - h, 36, h, fill=SAND if v else MINT, stroke=AMBER if v else TEAL, r=2)
    f.text(x + 18, 100 - h - 8, str(v), size=11, color=AMBER if v else TEAL, bold=True)
    f.text(x + 18, 114, "%d yr" % n, size=10.5, color=SLATE, bold=True)
f.text(10, 140, "2000 yr: 0 odd days", size=10.5, color=SLATE, bold=True, anchor="start")
f.text(10, 158, "2001-06: 6 yr + 1 leap day = 0 odd", size=10.5, color=SLATE, bold=True, anchor="start")
f.text(10, 176, "1 Jan-24 Oct 2007: 297 days = 3 odd", size=10.5, color=SLATE, bold=True, anchor="start")
f.text(10, 194, "0 + 0 + 3 = 3: Wednesday (Sun = 0)", size=10.5, color=RED, bold=True, anchor="start")
f.text(150, 222, "calendar repeats every 400 years", size=10.5, color=NAVY, bold=True)
```

## Formula and fact sheet

| Topic | Rule |
|---|---|
| Series method | differences → ratios → squares/cubes/primes → split odd and even places |
| Second differences | constant second difference → next difference continues the AP |
| $n^2 \pm 1$ | 2, 5, 10, 17, 26 ($n^2 + 1$); 3, 8, 15, 24, 35 ($n^2 - 1$) |
| $n^3 \pm 1$ | 2, 9, 28, 65, 126 ($n^3 + 1$); 0, 7, 26, 63, 124 ($n^3 - 1$) |
| $n(n + 1)$ | 2, 6, 12, 20, 30, 42 |
| Primes to 50 | 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47 |
| Letters | EJOTY = 5, 10, 15, 20, 25; opposite letter = 27 − position |
| Wrong term | it spoils two neighbouring differences |
| Grid | the rule must fit every complete row/column/figure |
| Odd days | year 1 (leap 2); 31-day month 3, 30-day month 2, Feb 0 (leap 1); 100 years 5 |
| Leap year | divisible by 4; century years only if divisible by 400 |
| Day code | 0 Sunday, 1 Monday, … 6 Saturday |
| Clock angle | $|30H - 5.5M|$; use 360° − θ if θ > 180° |
| Hands together | at $60H/11$ minutes past H; 22 times a day |
| Right angles / opposite | 44 / 22 times a day |
| Mirror time | 11:60 − time seen |

## Chapter summary

- Logical sequencing carries 5 of the 20 MAT questions; the MEC sample (53, 53, 40, 40,
  27, 27 → 14) is a series of repeated pairs falling by 13.
- Write the differences first; then ratios; then squares, cubes and primes; then split
  the series into odd and even places.
- A rule is right only when it fits every term; a wrong term spoils two differences.
- Letters become numbers (A = 1 … Z = 26, EJOTY, opposite = 27 − n); repeating-letter
  series hide a short repeated block.
- Grid and figure puzzles: find one operation from the complete rows and apply it to
  the incomplete one.
- Calendar: odd days (year 1, leap year 2, 31-day month 3, 30-day month 2); century
  leap years must divide by 400.
- Clock: θ = |30H − 5.5M|; the hands meet 22 times a day; mirror time = 11:60 − t.

## Practice questions

**Set A — Recall (25 questions)**

1. Find the next term: 4, 9, 14, 19, 24, ?
   (a) 28 (b) 30 (c) 29 (d) 34
2. Find the next term: 3, 6, 12, 24, 48, ?
   (a) 96 (b) 72 (c) 84 (d) 100
3. Find the next term: 1, 4, 9, 16, 25, ?
   (a) 30 (b) 35 (c) 49 (d) 36
4. Find the next term: 2, 3, 5, 7, 11, 13, ?
   (a) 15 (b) 17 (c) 19 (d) 14
5. Find the next term: 1, 1, 2, 3, 5, 8, 13, ?
   (a) 21 (b) 18 (c) 20 (d) 26
6. Find the next term: 243, 81, 27, 9, ?
   (a) 1 (b) 6 (c) 3 (d) 0
7. Find the next term: 2, 6, 12, 20, 30, ?
   (a) 40 (b) 36 (c) 44 (d) 42
8. Look at this series: 35, 35, 29, 29, 23, 23, … Which number should come next?
   (a) 23 (b) 17 (c) 19 (d) 11
9. Find the next term: 1, 8, 27, 64, ?
   (a) 100 (b) 81 (c) 125 (d) 216
10. Find the next term: 5, 10, 8, 16, 14, 28, ?
   (a) 26 (b) 56 (c) 30 (d) 24
11. Find the next letter: A, C, E, G, ?
   (a) H (b) J (c) K (d) I
12. Find the next letter: Z, X, V, T, ?
   (a) S (b) Q (c) R (d) P
13. Find the next letter: B, E, H, K, ?
   (a) M (b) N (c) O (d) L
14. Find the next term: AZ, BY, CX, ?
   (a) DW (b) DV (c) EW (d) WD
15. Find the next term: A1, C3, E5, G7, ?
   (a) H8 (b) I8 (c) J9 (d) I9
16. Find the next letter: A, B, D, G, K, ?
   (a) O (b) P (c) Q (d) N

```figure caption="For Set A, question 17: the same rule holds in every row of the grid."
fig, ax = plt.subplots(figsize=(4.0, 2.3))
rows = [['3', '4', '12'], ['5', '2', '10'], ['6', '?', '42']]
for i, r in enumerate(rows):
    for j, t in enumerate(r):
        fc = '#fde9c8' if t == '?' else 'white'
        ax.add_patch(Rectangle((j, 2-i), 1, 1, fc=fc, ec=INK, lw=1.2))
        ax.text(j+0.5, 2-i+0.5, t, ha='center', va='center', fontsize=12, fontweight='bold')
ax.set_xlim(-1.6, 4.6); ax.set_ylim(-0.1, 3.1); ax.set_aspect('equal'); ax.axis('off')
```

17. In the figure above, which number replaces the question mark?
   (a) 6 (b) 8 (c) 7 (d) 9

```figure caption="For Set A, question 18: the number inside each triangle is found from the three numbers at its corners by the same rule."
fig, ax = plt.subplots(figsize=(5.0, 2.3))
data = [(('2', '3', '4'), '24'), (('3', '4', '5'), '60'), (('2', '5', '?'), '40')]
for k, (c, mid) in enumerate(data):
    x0 = 3.9*k
    P = [(x0, 0), (x0+2.4, 0), (x0+1.2, 2.0)]
    ax.add_patch(Polygon(P, closed=True, fc='#fde9c8' if '?' in c else 'white', ec=INK, lw=1.3))
    ax.text(x0+1.2, 0.68, mid, ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(x0+1.2, 2.18, c[0], ha='center', va='bottom', fontsize=10.5)
    ax.text(x0-0.12, -0.1, c[1], ha='right', va='center', fontsize=10.5)
    ax.text(x0+2.52, -0.1, c[2], ha='left', va='center', fontsize=10.5, fontweight='bold' if c[2] == '?' else 'normal')
ax.set_xlim(-0.7, 10.9); ax.set_ylim(-0.45, 2.6); ax.set_aspect('equal'); ax.axis('off')
```

18. In the figure above, which number replaces the question mark?
   (a) 4 (b) 5 (c) 3 (d) 6
19. If 1 January of a year is a Monday, what day of the week is 1 February of that year?
   (a) Wednesday (b) Friday (c) Tuesday (d) Thursday
20. How many odd days are there in a leap year?
   (a) 1 (b) 2 (c) 0 (d) 3
21. Which of the following years is a leap year?
   (a) 1900 (b) 2100 (c) 2000 (d) 2022
22. If today is Wednesday, what day of the week will it be exactly 100 days from today?
   (a) Friday (b) Thursday (c) Saturday (d) Tuesday
23. The angle between the hands of a clock at 4:30 is
   (a) 30° (b) 60° (c) 15° (d) 45°
24. How many times in a day do the hour hand and the minute hand of a clock coincide?
   (a) 24 (b) 22 (c) 12 (d) 11
25. The mirror image of a wall clock (mirror beside the clock) shows 3:15. The actual time is
   (a) 9:45 (b) 8:15 (c) 8:45 (d) 9:15

::: note Answers and explanations — Set A
**1.** (c) — Add 5 each time: 24 + 5 = 29.
**2.** (a) — Multiply by 2 each time: 48 × 2 = 96.
**3.** (d) — Squares of 1, 2, 3, 4, 5; next $6^2$ = 36.
**4.** (b) — Consecutive prime numbers; the prime after 13 is 17 (15 = 3 × 5 is not prime).
**5.** (a) — Each term is the sum of the two before it: 8 + 13 = 21.
**6.** (c) — Divide by 3 each time: 9 ÷ 3 = 3.
**7.** (d) — Differences 4, 6, 8, 10, so next 12: 30 + 12 = 42 (the terms are 1 × 2, 2 × 3, …, 6 × 7).
**8.** (b) — Each number appears twice and the numbers fall by 6: 35, 29, 23, then 17.
**9.** (c) — Cubes of 1, 2, 3, 4; next $5^3$ = 125.
**10.** (a) — The steps alternate ×2 and −2: 5 ×2 = 10, −2 = 8, ×2 = 16, −2 = 14, ×2 = 28, −2 = 26.
**11.** (d) — Positions 1, 3, 5, 7: skip one letter each time; next 9 = I.
**12.** (c) — Positions 26, 24, 22, 20: back two each time; next 18 = R.
**13.** (b) — Positions 2, 5, 8, 11: +3; next 14 = N.
**14.** (a) — First letters A, B, C, D (+1); second letters Z, Y, X, W (−1): DW. Each pair adds to 27.
**15.** (d) — Letters skip one (A, C, E, G, I) and the number is the letter's position: I9.
**16.** (b) — Positions 1, 2, 4, 7, 11: differences +1, +2, +3, +4; next +5 gives 16 = P.
**17.** (c) — In each row, first × second = third: 3 × 4 = 12, 5 × 2 = 10, so 6 × ? = 42 and ? = 7.
**18.** (a) — The centre is the product of the corners: 2 × 3 × 4 = 24, 3 × 4 × 5 = 60, so 2 × 5 × ? = 40 and ? = 4.
**19.** (d) — January has 31 days = 3 odd days; Monday + 3 = Thursday.
**20.** (b) — 366 days = 52 weeks + 2 days.
**21.** (c) — 2000 is a century year divisible by 400. 1900 and 2100 are century years not divisible by 400; 2022 is not divisible by 4.
**22.** (a) — 100 = 14 × 7 + 2, so two days after Wednesday: Friday.
**23.** (d) — |30 × 4 − 5.5 × 30| = |120 − 165| = 45°. The hour hand is halfway between 4 and 5.
**24.** (b) — 11 times in every 12 hours (the meeting at 12 is shared), so 22 times in 24 hours.
**25.** (c) — Real time = 11:60 − 3:15 = 8:45.
:::

**Set B — Understanding (16 questions)**

1. Find the next term: 2, 5, 10, 17, 26, ?
   (a) 35 (b) 36 (c) 37 (d) 38
2. Find the next term: 3, 7, 15, 31, 63, ?
   (a) 127 (b) 125 (c) 126 (d) 95
3. Find the next term: 6, 11, 21, 36, 56, ?
   (a) 76 (b) 86 (c) 71 (d) 81
4. Find the next term: 1, 2, 6, 24, 120, ?
   (a) 240 (b) 720 (c) 600 (d) 144
5. Find the wrong number in the series: 2, 5, 11, 20, 32, 48
   (a) 5 (b) 11 (c) 48 (d) 32
6. Find the next term: 4, 6, 9, 13.5, ?
   (a) 18 (b) 20.25 (c) 19.5 (d) 27
7. Find the next term: 1, 3, 4, 7, 11, 18, ?
   (a) 25 (b) 27 (c) 28 (d) 29
8. Find the next term: 0, 7, 26, 63, 124, ?
   (a) 215 (b) 217 (c) 216 (d) 225
9. Find the next letter: Z, W, S, P, L, I, ?
   (a) F (b) D (c) E (d) G
10. Which group of letters fills the blanks, in order, in the series a _ b a a _ a a b _ a b?
   (a) aba (b) abb (c) baa (d) bab
11. Find the next term: B2, D4, F8, H16, ?
   (a) I32 (b) J24 (c) K32 (d) J32
12. Find the next term: ABD, DEG, GHJ, ?
   (a) JKL (b) JLM (c) KLN (d) JKM
13. If 15 August 2026 is a Saturday, what day of the week is 15 August 2027?
   (a) Saturday (b) Sunday (c) Monday (d) Friday
14. The angle between the hands of a clock at 7:20 is
   (a) 90° (b) 110° (c) 100° (d) 120°
15. In a mirror placed beside a wall clock, the clock appears to show 6:40. The actual time is
   (a) 5:20 (b) 6:20 (c) 4:20 (d) 5:40

```figure caption="For Set B, question 16: in each square the number in the middle is found from the four corner numbers by the same rule."
fig, ax = plt.subplots(figsize=(4.8, 2.3))
data = [('6', '4', '3', '2', '18'), ('7', '5', '4', '3', '23'), ('8', '6', '5', '?', '33')]
for k, (a, b, c, d, m) in enumerate(data):
    x0 = 3.0*k
    ax.add_patch(Rectangle((x0, 0), 2.2, 2.2, fc='#fde9c8' if '?' in (a, b, c, d) else 'white', ec=INK, lw=1.3))
    ax.add_patch(Circle((x0+1.1, 1.1), 0.42, fc='white', ec=MUTED, lw=1.0))
    ax.text(x0+1.1, 1.1, m, ha='center', va='center', fontsize=11, fontweight='bold')
    for (x, y, t) in [(x0+0.35, 1.85, a), (x0+1.85, 1.85, b), (x0+0.35, 0.35, c), (x0+1.85, 0.35, d)]:
        ax.text(x, y, t, ha='center', va='center', fontsize=10.5, fontweight='bold' if t == '?' else 'normal')
ax.set_xlim(-0.2, 8.4); ax.set_ylim(-0.2, 2.4); ax.set_aspect('equal'); ax.axis('off')
```

16. In the figure above, which number replaces the question mark?
   (a) 2 (b) 3 (c) 4 (d) 5

::: note Answers and explanations — Set B
**1.** (c) — The terms are $n^2 + 1$ for n = 1 … 5 (differences 3, 5, 7, 9); next $6^2 + 1$ = 37.
**2.** (a) — Each term is the one before × 2 + 1: 63 × 2 + 1 = 127.
**3.** (d) — Differences 5, 10, 15, 20; next 25: 56 + 25 = 81.
**4.** (b) — Multiply by 2, 3, 4, 5, then 6: 120 × 6 = 720.
**5.** (c) — The differences should be 3, 6, 9, 12, 15: 2, 5, 11, 20, 32, 47. 48 is wrong; changing any other term breaks two differences.
**6.** (b) — Each term is 1.5 times the one before: 13.5 × 1.5 = 20.25.
**7.** (d) — Each term is the sum of the two before it: 11 + 18 = 29.
**8.** (a) — The terms are $n^3 - 1$: 1 − 1, 8 − 1, 27 − 1, 64 − 1, 125 − 1; next 216 − 1 = 215.
**9.** (c) — Positions 26, 23, 19, 16, 12, 9: the steps alternate −3 and −4; next −4 gives 5 = E.
**10.** (a) — The block "aab" repeats: aab aab aab aab. The blanks (2nd, 6th and 10th letters) are a, b, a.
**11.** (d) — Letters skip one (B, D, F, H, J); numbers double (2, 4, 8, 16, 32): J32.
**12.** (d) — Each group starts 3 letters on (A, D, G, J), and inside a group the steps are +1, +2: J, K, M.
**13.** (b) — 15 Aug 2026 to 15 Aug 2027 is 365 days (no 29 February in between: 2027 is not a leap year), 1 odd day: Sunday.
**14.** (c) — |30 × 7 − 5.5 × 20| = |210 − 110| = 100°.
**15.** (a) — Real time = 11:60 − 6:40 = 5:20. Check: a mirror swaps 5:20 and 6:40, which are symmetric about the 12–6 line.
**16.** (b) — Middle = (top-left × top-right) − (bottom-left × bottom-right): 6 × 4 − 3 × 2 = 18 and 7 × 5 − 4 × 3 = 23. So 8 × 6 − 5 × ? = 33, giving 5 × ? = 15 and ? = 3.
:::

**Set C — Application (11 questions)**

1. Find the next term: 13, 15, 19, 27, 43, ?
   (a) 59 (b) 75 (c) 71 (d) 86
2. Find the next term: 2, 10, 4, 20, 8, 40, 16, ?
   (a) 32 (b) 60 (c) 80 (d) 64
3. Find the next term: 1, 2, 5, 14, 41, ?
   (a) 122 (b) 123 (c) 121 (d) 82
4. Find the next letter: C, F, J, O, ?
   (a) T (b) V (c) S (d) U
5. Find the next term: KM5, IP8, GS11, EV14, ?
   (a) CY17 (b) CX17 (c) DY17 (d) CY15
6. If 1 January 2026 is a Thursday, what day of the week is 1 March 2026?
   (a) Saturday (b) Sunday (c) Monday (d) Wednesday
7. In which year will the calendar of 2026 be repeated exactly?
   (a) 2032 (b) 2036 (c) 2037 (d) 2031
8. At what time between 4 and 5 o'clock are the hands of a clock together?
   (a) 20 minutes past 4 (b) 22 minutes past 4 (c) 21 7/11 minutes past 4 (d) 21 9/11 minutes past 4
9. A clock gains 5 minutes every hour. It is set right at 6 a.m. What time will it show when the correct time is 6 p.m. the same day?
   (a) 6:55 p.m. (b) 7:05 p.m. (c) 7:00 p.m. (d) 7:12 p.m.

```figure caption="For Set C, question 10: the same rule links the three numbers in every column."
fig, ax = plt.subplots(figsize=(4.0, 2.3))
cols = [['3', '4', '25'], ['5', '12', '169'], ['6', '8', '?']]
for j, c in enumerate(cols):
    for i, t in enumerate(c):
        fc = '#fde9c8' if t == '?' else 'white'
        ax.add_patch(Rectangle((j*1.2, 2-i), 1.2, 1, fc=fc, ec=INK, lw=1.2))
        ax.text(j*1.2+0.6, 2-i+0.5, t, ha='center', va='center', fontsize=12, fontweight='bold')
ax.set_xlim(-1.4, 5.0); ax.set_ylim(-0.1, 3.1); ax.set_aspect('equal'); ax.axis('off')
```

10. In the figure above, which number replaces the question mark?
   (a) 14 (b) 48 (c) 196 (d) 100
11. The angle between the hands of a clock at 9:15 is
   (a) 172.5° (b) 180° (c) 165° (d) 157.5°

::: note Answers and explanations — Set C
**1.** (b) — Differences 2, 4, 8, 16 double each time; next 32: 43 + 32 = 75.
**2.** (c) — Two series: odd places 2, 4, 8, 16 (×2) and even places 10, 20, 40 (×2). The 8th term belongs to the even series: 80.
**3.** (a) — Each term is the one before × 3 − 1: 41 × 3 − 1 = 122.
**4.** (d) — Positions 3, 6, 10, 15: steps +3, +4, +5; next +6 gives 21 = U.
**5.** (a) — First letters K, I, G, E, C (−2); second letters M, P, S, V, Y (+3); numbers 5, 8, 11, 14, 17 (+3): CY17.
**6.** (b) — January (31) + February 2026 (28, not a leap year) = 59 days = 8 weeks + 3 days; Thursday + 3 = Sunday.
**7.** (c) — A repeat needs the same first weekday (Thursday) and the same year type (ordinary). Odd days: 2026 to 2031 give 1 + 1 + 2 + 1 + 1 + 1 = 7, so 2032 starts on a Thursday — but 2032 is a leap year. 2032 to 2036 give 2 + 1 + 1 + 1 + 2 = 7 more, so 2037 starts on a Thursday and is an ordinary year.
**8.** (d) — Together when 30 × 4 = 5.5M: M = 240/11 = 21 9/11 minutes past 4.
**9.** (c) — From 6 a.m. to 6 p.m. is 12 hours; it gains 12 × 5 = 60 minutes, so it shows 7:00 p.m.
**10.** (d) — In each column, top² + middle² = bottom: 9 + 16 = 25, 25 + 144 = 169, so 36 + 64 = 100. 196 = (6 + 8)² squares the sum instead.
**11.** (a) — |30 × 9 − 5.5 × 15| = |270 − 82.5| = 187.5°, which is more than 180°, so the angle is 360 − 187.5 = 172.5°.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Explain a systematic method for number series and letter series and solve problems of each common type. <span class="marks">[10]</span>
2. Explain the rules of the calendar and the clock and solve problems on odd days, the day of a date and angles between the hands. <span class="marks">[10]</span>

### Model answer D1: Number and letter series (10 marks)

**Introduction.** A series follows a rule. A fixed order of checks finds the rule quickly.

**Order of checks.** (1) Differences; (2) differences of differences; (3) ratios; (4) squares, cubes, primes; (5) alternate terms; (6) mixed operations.

| Type | Series | Rule | Next term |
|---|---|---|---|
| Arithmetic | 5, 9, 13, 17 | +4 | 21 |
| Second-order differences | 2, 6, 12, 20, 30 | differences 4, 6, 8, 10, so next +12 | **42** (n × (n + 1)) |
| Geometric | 3, 6, 12, 24 | × 2 | 48 |
| Squares | 1, 4, 9, 16 | n² | 25 |
| Primes | 2, 3, 5, 7, 11 | prime numbers | 13 |
| Fibonacci type | 1, 1, 2, 3, 5, 8 | sum of previous two | 13 |
| Factorials | 1, 2, 6, 24, 120 | × 2, × 3, × 4, × 5, × 6 | **720** |
| Descending squares | 100, 81, 64, 49 | 10², 9², 8², 7² | 36 |

**Two interleaved series.** 2, 5, 4, 10, 8, 15, … The odd places are 2, 4, 8 (× 2), so the next is 16; the even places are 5, 10, 15 (+ 5), so the next is 20. The series continues **16, 20**.

**Letter series.** Convert letters to positions (A = 1 … Z = 26). Example: A, C, F, J, O, … positions 1, 3, 6, 10, 15, with differences 2, 3, 4, 5, so the next difference is 6: 15 + 6 = 21 = **U**. Opposite letters: the opposite of a letter at position p is at 27 − p (A–Z, B–Y).

**Missing number in a figure.** In a triangle with 4, 5, 6 outside and 120 inside, the product is 4 × 5 × 6 = 120. Test the *same* rule in the second figure before using it.

**Exam tip.** If the numbers grow slowly, try differences; if they grow fast, try multiplication, squares or cubes.

**Conclusion.** Use the order of checks, test the rule on every term, and only then give the next term.

### Model answer D2: Calendar and clock reasoning (10 marks)

**Introduction.** The calendar repeats in a 7-day week, so only the **remainder after dividing by 7** (the odd days) matters.

**Calendar rules.**

1. An ordinary year has 365 days = 52 weeks + **1 odd day**; a leap year has **2 odd days**.
2. **100 years = 5 odd days**, 200 years = 3, 300 years = 1, 400 years = 0.
3. Months with 31 days give 3 odd days, with 30 days give 2, and February gives 0 (or 1 in a leap year).
4. Leap year: divisible by 4, but a century year only if divisible by 400 (so 1900 was not a leap year, 2000 was).

**Worked problem.** What day was 15 August 1947? Verify: the day is **Friday**. A quick check by odd days: 1600 years = 0 odd days; 300 years = 1; 46 completed years from 1901 to 1946 have 11 leap years, so 46 + 11 = 57 odd days = 1; days from 1 January to 15 August 1947 = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 15 = 227 days = 3 odd days. Total = 0 + 1 + 1 + 3 = 5, which is **Friday** (0 = Sunday). Similarly, 26 January 2000 was a **Wednesday**.

**Clock rules.**

1. The minute hand moves 6° per minute and the hour hand 0.5° per minute, so the angle between them at H hours M minutes is |30H − 5.5M|.
2. The hands **coincide 22 times** and are **at right angles 44 times** in a day.
3. Mirror image of a clock time T is 11:60 − T; the water image is 6:00 − T.

| Time | Working | Angle |
|---|---|---|
| 3:40 | \|90 − 220\| | 130° |
| 4:20 | \|120 − 110\| | 10° |
| 9:00 | \|270 − 0\| | 270°, so 90° the short way |
| 12:30 | \|0 − 165\| | 165° (take the smaller of x and 360 − x) |

**Mirror example.** The mirror image of 3:25 is 11:60 − 3:25 = **8:35**; its water image is 6:00 − 3:25 = **2:35**.

**Conclusion.** Reduce the calendar to odd days and the clock to degrees per minute; both turn long counting into one short calculation.
