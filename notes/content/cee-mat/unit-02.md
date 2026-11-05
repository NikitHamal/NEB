---
subject: Mental Agility Test
grade: CEE
unit: 2
title: Numerical Reasoning
hours: 5
area: Mental Agility Test
---

Numerical reasoning carries **5 of the 20 MAT questions**. They are arithmetic word
problems of the kind met up to Grade 10 — percentages, ratios, averages, profit and
interest, work, speed, ages, mixtures, number facts — set so that the student who knows
the shortcut answers in thirty seconds and the student who sets up long equations
answers in three minutes. There is no calculator. The official MEC sample is a
percentage-change question (a rectangle's length up 15 %, breadth up 25 %: area up
43.75 %, "44 %"). This chapter gives, for each type, the one formula or picture that
answers it fastest, and the trap that the wrong options are built from.

::: key What the paper asks from this chapter
- **Successive percentage change**: $a\%$ then $b\%$ gives a net change of
  $a + b + ab/100$ per cent (a decrease is negative).
- **Percent of what?** Profit and loss per cent are on the cost price, discount per
  cent on the marked price; "A is $r\%$ more than B" is on B.
- **Interest**: SI = PRT/100; amount at CI = $P(1 + R/100)^T$; for two years
  CI − SI = $P(R/100)^2$.
- **Work**: turn days into work per day (1/a), add rates, invert. The LCM of the days
  makes everything whole numbers.
- **Speed**: km/h × 5/18 = m/s; equal distances at x and y give an average speed
  of $2xy/(x + y)$; trains add their lengths, and opposite directions add speeds.
- **Mixtures**: the alligation cross gives the ratio at once.
- **Numbers**: divisibility rules, unit-digit cycles, HCF × LCM = product.
- **Estimation**: round, compute roughly, and pick the nearest option.
:::

## 2.1 Percentages, ratio and proportion, averages

### Percentages

"Per cent" means per hundred: $x\% = x/100$. Learn these fraction values — they turn
percentage questions into mental arithmetic.

| Fraction | 1/2 | 1/3 | 1/4 | 1/5 | 1/6 | 1/8 | 1/9 | 1/10 | 1/11 | 1/12 | 1/16 | 1/20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Per cent | 50 | 33⅓ | 25 | 20 | 16⅔ | 12½ | 11 1/9 | 10 | 9 1/11 | 8⅓ | 6¼ | 5 |

| Situation | Formula |
|---|---|
| Percentage change | (new − old) / old × 100 |
| Increase by $r\%$ | multiply by $(1 + r/100)$; 20 % up = × 1.2 |
| Decrease by $r\%$ | multiply by $(1 - r/100)$; 20 % down = × 0.8 |
| Two successive changes $a\%$, $b\%$ | net change $= a + b + \frac{ab}{100}$ per cent |
| Price up $r\%$, same spending | cut consumption by $\frac{r}{100 + r} \times 100\%$ |
| A is $r\%$ more than B | B is $\frac{r}{100 + r} \times 100\%$ less than A |

The successive-change formula covers area (length × breadth), revenue (price ×
quantity) and population over two years — any product of two quantities.

```figure caption="Why length +15 % and breadth +25 % increase the area by 43.75 %: the old area (100 %) gains a strip of 15 %, a strip of 25 % and a corner of 15 % of 25 % = 3.75 %."
fig, ax = plt.subplots(figsize=(4.6, 3.0))
L, B = 1.0, 1.0
ax.add_patch(Rectangle((0, 0), L, B, fc='#dbe8f6', ec=ACCENT, lw=1.4))
ax.add_patch(Rectangle((L, 0), 0.15, B, fc='#fde9c8', ec=SERIES[3], lw=1.2))
ax.add_patch(Rectangle((0, B), L, 0.25, fc='#d9f0e1', ec=SERIES[2], lw=1.2))
ax.add_patch(Rectangle((L, B), 0.15, 0.25, fc='#f8dede', ec=SERIES[1], lw=1.2))
ax.text(0.5, 0.5, 'old area\n100 %', ha='center', va='center', fontsize=10, fontweight='bold')
ax.text(1.075, 0.5, '15 %', ha='center', va='center', fontsize=8.6, rotation=90)
ax.text(0.5, 1.125, '25 %', ha='center', va='center', fontsize=8.6)
ax.annotate('15 % of 25 %\n= 3.75 %', xy=(1.075, 1.125), xytext=(1.38, 1.38),
            fontsize=8.6, color=SERIES[1], ha='left', va='center',
            arrowprops=dict(arrowstyle='-', color=SERIES[1], lw=0.9))
ax.annotate('', xy=(1.15, -0.1), xytext=(0, -0.1), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.9))
ax.text(0.575, -0.18, 'length × 1.15', ha='center', va='top', fontsize=8.6)
ax.annotate('', xy=(-0.1, 1.25), xytext=(-0.1, 0), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.9))
ax.text(-0.18, 0.625, 'breadth × 1.25', ha='right', va='center', fontsize=8.6, rotation=90)
ax.text(1.38, 0.45, 'new area\n= 100 + 15 + 25 + 3.75\n= 143.75 %', ha='left', va='center', fontsize=8.8)
ax.set_xlim(-0.45, 2.25); ax.set_ylim(-0.38, 1.6); ax.set_aspect('equal'); ax.axis('off')
```

::: example The MEC sample question
**Problem.** The length and breadth of a rectangle are increased by 15 % and 25 %
respectively. What is the percentage increase in the area? (a) 20 % (b) 30 % (c) 40 %
(d) 44 %

**Solution.** Net change = 15 + 25 + (15 × 25)/100 = 40 + 3.75 = 43.75 %, which the
options round to **44 %** (key D). Check with numbers: 1.15 × 1.25 = 1.4375. The
tempting 40 % forgets the corner piece.
:::

### Ratio and proportion

| Idea | Rule |
|---|---|
| Ratio | $a : b = a/b$; multiply or divide both terms by the same number freely |
| Sharing an amount in $a : b : c$ | share of A = amount × $a/(a + b + c)$ |
| Joining $a : b$ and $b : c$ | make the two b's equal (multiply crosswise) |
| Proportion $a : b = c : d$ | $ad = bc$ (product of extremes = product of means) |
| Fourth proportional to a, b, c | $d = bc/a$ |
| Mean proportional of a and b | $\sqrt{ab}$ |
| Third proportional to a and b | $b^2/a$ |
| Direct proportion | x doubles → y doubles ($y/x$ constant) |
| Inverse proportion | x doubles → y halves ($xy$ constant), e.g. workers and days |

::: example Sharing in a ratio
**Problem.** Rs 5,400 is divided among Anil, Bina and Chandra in the ratio 2 : 3 : 4.
How much does Chandra get?

**Solution.** Total parts = 2 + 3 + 4 = 9; one part = 5400/9 = Rs 600. Chandra gets
4 × 600 = **Rs 2,400**.
:::

### Averages

Average = sum ÷ number of items, so **sum = average × number**. Work with sums, not
averages, whenever an item is added, removed or replaced.

- The average of equally spaced numbers is the middle one (or the mean of the first and
  the last). Average of 1, 2, …, n is $(n + 1)/2$.
- Replacing one member changes the sum by (new − old), so the average changes by
  (new − old) / n.
- Adding a member raises the average by d: the newcomer = old average + d × (new count).

::: example Replacing one member
**Problem.** The average weight of 8 people rises by 2.5 kg when one of them, who
weighs 65 kg, is replaced by a new person. What is the new person's weight?

**Solution.** The total rose by 8 × 2.5 = 20 kg, so the newcomer is 65 + 20 =
**85 kg**.
:::

## 2.2 Profit and loss, simple and compound interest

### Profit, loss and discount

CP = cost price, SP = selling price, MP = marked (list) price.

| Quantity | Formula | Calculated on |
|---|---|---|
| Profit % | (SP − CP)/CP × 100 | CP |
| Loss % | (CP − SP)/CP × 100 | CP |
| SP from CP | SP = CP × (100 + profit%)/100 | CP |
| CP from SP | CP = SP × 100/(100 + profit%) | — |
| Discount % | (MP − SP)/MP × 100 | MP |
| Two discounts $d_1$, $d_2$ | single discount $= d_1 + d_2 - d_1 d_2/100$ | MP |
| Marked $m\%$ above CP, discount $d\%$ | multiply: $(1 + m/100)(1 - d/100)$ | CP |
| Same SP, $x\%$ gain on one and $x\%$ loss on the other | always a **loss** of $x^2/100$ per cent | — |
| False weight (sells $w$ g for 1000 g at cost price) | gain $= \frac{1000 - w}{w} \times 100\%$ | — |

::: example Mark-up and discount
**Problem.** A shopkeeper buys a jacket for Rs 800, marks it 25 % above the cost and
then gives a 10 % discount. What is the profit per cent?

**Solution.** SP = 800 × 1.25 × 0.90 = Rs 900. Profit = 100 on a cost of 800:
**12.5 %**. (Shortcut: 1.25 × 0.9 = 1.125.)
:::

::: caution Profit is on the cost price
Buying at Rs 400 and selling at Rs 500 is a 25 % profit (100 on 400), not 20 %
(100 on 500). A discount is on the marked price. If a CP is found from an SP with
20 % profit, divide by 1.2 — do not multiply by 0.8.
:::

### Simple and compound interest

$$ \text{SI} = \frac{P \times R \times T}{100}, \qquad A = P\left(1 + \frac{R}{100}\right)^{T} $$

P = principal (Rs), R = rate per cent per annum, T = time in years, A = amount
(principal + interest). Compound interest CI = A − P.

| Fact | Rule |
|---|---|
| Money doubles at SI in T years | $R = 100/T$ |
| CI − SI for 2 years | $P(R/100)^2$ |
| CI − SI for 3 years | $P(R/100)^2(3 + R/100)$ |
| Interest compounded half-yearly | use R/2 per half-year and 2T half-years |
| Successive years at CI | the amounts form a geometric progression (× (1 + R/100) each year) |
| Rule of 72 (estimate) | money doubles at CI in about 72/R years |

::: example CI against SI
**Problem.** Find the difference between the compound and the simple interest on
Rs 20,000 for 2 years at 10 % per annum.

**Solution.** SI = 20000 × 10 × 2/100 = Rs 4,000. A = 20000 × 1.1² = Rs 24,200, so
CI = Rs 4,200. Difference = **Rs 200** — the same as $P(R/100)^2$ = 20000 × 0.01. The
difference is the interest on the first year's interest.
:::

```photogrid label="2.1" cols="2" ratio="1.2" caption="Why compound interest beats simple interest. (a) An old Nepali paper banknote: money kept in a bank earns interest, and the way interest is counted decides how fast it grows. (b) Rs 10,000 at 10 per cent a year. Simple interest adds the same Rs 1,000 every year (SI = PRT/100), so the amount is a straight line. Compound interest earns interest on interest, A = P(1 + r/100)^t, a curve that bends upwards. After 3 years the two differ by only Rs 310 (13,310 against 13,000) but after 10 years compound interest gives Rs 25,937 against Rs 20,000. The money doubles in ln 2 / ln 1.1 = 7.27 years, which the rule of 72 (72 / 10 = 7.2) estimates quickly."
@ photo id="ceemat/rupee" cap="An old Nepali paper banknote"
fit 1.2
focus 0.5 0.5
@ svg cap="Rs 10,000 at 10 per cent: simple against compound"
import math
P0, r = 10000, 0.10
si = lambda t: P0 * (1 + r * t)
ci = lambda t: P0 * (1 + r) ** t
t2 = math.log(2) / math.log(1 + r)
assert round(si(3)) == 13000 and round(ci(3)) == 13310 and round(ci(10)) == 25937 and round(si(10)) == 20000
assert abs(t2 - 7.27) < 0.005 and abs(ci(t2) - 20000) < 1e-6
f = Fig(300, 236)
f.text(150, 12, "Rs 10,000 at 10% a year", size=10.5, color=NAVY, bold=True)
ax = Axes(f, 48, 28, 230, 150, (0, 10), (10000, 26000))
ax.grid(2, 5000, xfmt=lambda v: "%d" % v, yfmt=lambda v: "%dk" % (v // 1000)).axes("yr", "Rs")
ax.curve(si, 0, 10, color=TEAL)
ax.curve(ci, 0, 10, color=RED)
ax.pt(t2, 20000, "doubles in 7.3 yr", dx=-8, dy=-8, anchor="end")
f.line(58, 42, 78, 42, color=RED, sw=2.2)
f.text(84, 42, "compound (CI)", size=10.5, color=RED, bold=True, anchor="start", vmid=True)
f.line(58, 58, 78, 58, color=TEAL, sw=2.2)
f.text(84, 58, "simple (SI)", size=10.5, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(150, 206, "3 years: CI Rs 13,310 against SI Rs 13,000", size=10.5, color=NAVY, bold=True)
f.text(150, 222, "10 years: CI Rs 25,937 against SI Rs 20,000", size=10.5, color=SLATE, bold=True)
```

## 2.3 Time and work, speed, distance and time

### Time and work

If A finishes a job in $a$ days, A does $1/a$ of it each day. Rates add when people
(or pipes) work together:

$$ \frac{1}{T} = \frac{1}{a} + \frac{1}{b} \quad \Rightarrow \quad T = \frac{ab}{a + b} $$

**LCM method (faster).** Take the total work = LCM of the days. A in 10 days and B in
15 days: total 30 units; A does 3 units a day, B 2; together 5 a day, so 30/5 = 6 days.

| Situation | Rule |
|---|---|
| A and B together | $T = ab/(a + b)$ |
| A + B together in $t$ days, A alone in $a$ days | B's rate $= 1/t - 1/a$ |
| Workers and days | $M_1 D_1 H_1 / W_1 = M_2 D_2 H_2 / W_2$ (men, days, hours, work) |
| Filling pipe and emptying pipe | rates subtract: $1/a - 1/b$ |
| Work partly done, someone leaves | find the fraction done, then finish the rest at the new rate |

::: example Working together
**Problem.** Asha can paint a room in 10 days and Binod in 15 days. How long do they
take together?

**Solution.** LCM 30 units. Asha 3 units/day, Binod 2 units/day, together 5/day:
30/5 = **6 days**. Check: 10 × 15/(10 + 15) = 150/25 = 6.
:::

### Speed, distance and time

Distance = speed × time. To change units: **km/h × 5/18 = m/s** and m/s × 18/5 = km/h
(72 km/h = 20 m/s, 54 km/h = 15 m/s, 36 km/h = 10 m/s, 18 km/h = 5 m/s).

| Situation | Rule |
|---|---|
| Average speed | total distance ÷ total time — never the plain mean of speeds |
| Equal distances at x and y | average speed $= 2xy/(x + y)$ |
| Same direction | relative speed = difference of speeds |
| Opposite directions | relative speed = sum of speeds |
| Train passes a pole or a person | distance = length of the train |
| Train passes a platform or a bridge | distance = train length + platform length |
| Two trains pass each other | distance = sum of lengths, at the relative speed |
| Boat of speed u in still water, stream v | downstream $u + v$, upstream $u - v$ |
| From downstream D and upstream U | boat $= (D + U)/2$, stream $= (D - U)/2$ |
| Late at one speed, early at another | the difference of the two times = the total of "late" and "early" |

::: example A train and a platform
**Problem.** A 240 m train running at 54 km/h crosses a 360 m platform. How long
does it take?

**Solution.** 54 km/h = 15 m/s. Distance = 240 + 360 = 600 m. Time = 600/15 =
**40 s**. Forgetting the platform gives 16 s; forgetting the train gives 24 s.
:::

::: example Average speed for a round trip
**Problem.** Sunil cycles to a village at 30 km/h and returns along the same road at
20 km/h. What is his average speed for the whole trip?

**Solution.** Equal distances: 2 × 30 × 20/(30 + 20) = 1200/50 = **24 km/h**, not 25.
(Take the distance as 60 km: 2 h out, 3 h back, 120 km in 5 h = 24 km/h.)
:::

```photogrid label="2.2" cols="2" ratio="1.2" caption="Average speed is not the average of the speeds. (a) A red city bus in Kathmandu. (b) A bus climbs a hill at 40 km/h and returns at 60 km/h. The simple mean of the speeds is 50 km/h, but the bus spends longer on the slow leg, so the true average is total distance over total time = 2 x 40 x 60 / (40 + 60) = 48 km/h (the harmonic mean). Check with 120 km each way: 3 h up and 2 h down is 5 h for 240 km, again 48. The red curve stays below the dashed line of simple means for every return speed except 40, where both give 40. Use the harmonic mean whenever equal distances are covered at different speeds, and the ordinary mean when equal times are used."
@ photo id="ceemat/bus" cap="A red city bus in Kathmandu"
fit 1.2
focus 0.5 0.5
@ svg cap="Out at 40 km/h, back at v: average speed"
u = 40
hm = lambda v: 2 * u * v / (u + v)
am = lambda v: (u + v) / 2
assert hm(60) == 48 and am(60) == 50 and hm(40) == 40
d = 120
assert abs(2 * d / (d / 40 + d / 60) - 48) < 1e-9 and d / 40 + d / 60 == 5
f = Fig(300, 236)
f.text(150, 12, "Average speed, out at 40 km/h", size=10.5, color=NAVY, bold=True)
ax = Axes(f, 48, 28, 230, 150, (0, 120), (0, 80))
ax.grid(20, 20).axes("v back", "avg")
ax.curve(hm, 1, 120, color=RED)
ax.curve(am, 0, 120, color=AMBER, dash=True)
ax.pt(60, 48, "48", dx=6, dy=16)
f.line(58, 42, 78, 42, color=RED, sw=2.2)
f.text(84, 42, "true (harmonic)", size=10.5, color=RED, bold=True, anchor="start", vmid=True)
f.line(58, 58, 78, 58, color=AMBER, sw=2.2, dash=True)
f.text(84, 58, "simple mean", size=10.5, color=AMBER, bold=True, anchor="start", vmid=True)
f.text(150, 206, "up 40, down 60 km/h: average 48, not 50", size=10.5, color=NAVY, bold=True)
f.text(150, 222, "120 km each way: 3 h + 2 h = 5 h for 240 km", size=10.5, color=SLATE, bold=True)
```

## 2.4 Ages, mixtures and number properties

### Ages

Let the present age be $x$. "n years ago" is $x - n$; "after n years" is $x + n$ —
and the *difference* of two people's ages never changes. With a ratio, write the ages
as $3x$ and $5x$.

**Fastest route:** put each option into the conditions. Age questions almost always have
whole-number answers, and checking an option takes ten seconds.

::: example Ages from two ratios
**Problem.** The ages of Ram and Hari are in the ratio 4 : 5. Five years ago the ratio
was 3 : 4. What is Hari's present age?

**Solution.** Ages 4x and 5x: (4x − 5)/(5x − 5) = 3/4 → 16x − 20 = 15x − 15 → x = 5.
Hari is **25 years**. Check: 20 and 25 now; 15 and 20 five years ago, which is 3 : 4.
:::

### Mixtures and alligation

When two ingredients at prices (or strengths) c (cheaper) and d (dearer) are mixed to
give a mean m:

$$ \frac{\text{quantity of cheaper}}{\text{quantity of dearer}} = \frac{d - m}{m - c} $$

```figure caption="The alligation cross. Write the two prices on top and the mean in the middle, then subtract along each diagonal. The number under each price is how much of that ingredient to take: cheaper : dearer = 10 : 5 = 2 : 1."
fig, ax = plt.subplots(figsize=(4.4, 2.8))
def box(x, y, t, c, ec=INK, w=1.2, fs=10, bold=True):
    ax.add_patch(Rectangle((x-w/2, y-0.28), w, 0.56, fc=c, ec=ec, lw=1.1, zorder=3))
    ax.text(x, y, t, ha='center', va='center', fontsize=fs, fontweight='bold' if bold else 'normal', zorder=4)
ax.plot([0.0, 3.4], [2.0, 0.0], color=MUTED, lw=1.1, zorder=1)
ax.plot([3.4, 0.0], [2.0, 0.0], color=MUTED, lw=1.1, zorder=1)
box(0.0, 2.0, 'Rs 60', '#dbe8f6'); box(3.4, 2.0, 'Rs 75', '#fde9c8')
box(1.7, 1.0, 'Rs 65', '#eeeeee')
box(0.0, 0.0, '75 − 65 = 10', 'white', ec=ACCENT, w=1.75, fs=8.8, bold=False)
box(3.4, 0.0, '65 − 60 = 5', 'white', ec=SERIES[3], w=1.75, fs=8.8, bold=False)
ax.text(0.0, 2.38, 'cheaper', ha='center', va='bottom', fontsize=8.5, color=MUTED)
ax.text(3.4, 2.38, 'dearer', ha='center', va='bottom', fontsize=8.5, color=MUTED)
ax.text(2.45, 1.0, 'mean', ha='left', va='center', fontsize=8.5, color=MUTED)
ax.text(0.0, -0.42, 'parts of cheaper', ha='center', va='top', fontsize=8.3, color=ACCENT)
ax.text(3.4, -0.42, 'parts of dearer', ha='center', va='top', fontsize=8.3, color=SERIES[3])
ax.set_xlim(-1.0, 4.4); ax.set_ylim(-0.85, 2.7); ax.set_aspect('equal'); ax.axis('off')
```

**Replacement.** If $x$ litres are taken out of $V$ litres of a liquid and replaced by
water, $n$ times over, the pure liquid left is $V(1 - x/V)^n$.

### Number properties

| Divisible by | Test |
|---|---|
| 2, 5, 10 | last digit even; 0 or 5; 0 |
| 3, 9 | sum of digits divisible by 3, by 9 |
| 4, 8 | last two digits by 4; last three digits by 8 |
| 6 | by 2 and by 3 |
| 11 | (sum of digits in odd places) − (sum in even places) is 0 or a multiple of 11 |

- The 25 primes below 100: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
  59, 61, 67, 71, 73, 79, 83, 89, 97. 1 is neither prime nor composite; 2 is the only
  even prime.
- For two numbers, **HCF × LCM = product of the numbers**.
- Numbers that leave the same remainder r when divided by a, b and c are
  k × LCM(a, b, c) + r (k = 0, 1, 2, …).
- $1 + 2 + \dots + n = n(n + 1)/2$; the sum of the first n odd numbers is $n^2$.

**Unit digits repeat in cycles.** The last digit of a power depends only on the last
digit of the base:

| Last digit of base | Cycle of last digits of powers | Cycle length |
|---|---|---|
| 0, 1, 5, 6 | always itself | 1 |
| 4 | 4, 6 | 2 |
| 9 | 9, 1 | 2 |
| 2 | 2, 4, 8, 6 | 4 |
| 3 | 3, 9, 7, 1 | 4 |
| 7 | 7, 9, 3, 1 | 4 |
| 8 | 8, 4, 2, 6 | 4 |

::: example Unit digit of a large power
**Problem.** What is the unit digit of $3^{47}$?

**Solution.** The cycle for 3 is 3, 9, 7, 1 (length 4). 47 = 4 × 11 + 3, so take the
3rd term of the cycle: **7**.
:::

## 2.5 Fast calculation and estimation

### Squares and cubes worth knowing

| n | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 25 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $n^2$ | 121 | 144 | 169 | 196 | 225 | 256 | 289 | 324 | 361 | 400 | 625 |

| n | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $n^3$ | 8 | 27 | 64 | 125 | 216 | 343 | 512 | 729 | 1000 | 1331 | 1728 |

### Tricks that save time

| Trick | Example |
|---|---|
| × 5 = × 10 ÷ 2 | 468 × 5 = 4680 ÷ 2 = 2340 |
| × 25 = × 100 ÷ 4 | 36 × 25 = 3600 ÷ 4 = 900 |
| Square of a number ending in 5 | 85²: 8 × 9 = 72, then 25 → 7225 |
| $(a + b)(a - b) = a^2 - b^2$ | 48 × 52 = 50² − 2² = 2496 |
| × 11 for two digits: put the digit sum in the middle | 35 × 11 = 3 (3+5) 5 = 385 |
| Split a percentage | 17 % of 240 = 10 % (24) + 5 % (12) + 2 % (4.8) = 40.8 |
| $x\%$ of $y$ = $y\%$ of $x$ | 16 % of 25 = 25 % of 16 = 4 |
| Order of operations | brackets, then ÷ and ×, then + and − (BODMAS) |

### Estimation

When the options are far apart, round every number to one or two significant figures,
compute, and choose the nearest option. Round some numbers up and some down so the
errors cancel. Stop as soon as only one option is possible.

::: example Estimation
**Problem.** 19.98 % of 501.2 + 3.01 × 49.9 ≈ ? (a) 150 (b) 200 (c) 250 (d) 300

**Solution.** 20 % of 500 = 100, and 3 × 50 = 150. Total ≈ **250**. (Exactly: 250.34.)
:::

::: tip Use the options
In numerical MCQs the options are information. Check divisibility (is the answer a
whole number of rupees, people, days?), the last digit, and the size before computing
anything. A ratio answer must make the total come out whole; an age must be positive
in every year the question mentions. Plugging the options back into the question is
a legitimate and fast method.
:::

## Formula and fact sheet

| Topic | Formula or fact |
|---|---|
| Successive change | $a + b + ab/100$ (%) |
| Same spending after a price rise of $r\%$ | cut consumption by $100r/(100 + r)$ % |
| Profit %, loss % | on CP; SP = CP(100 + P%)/100 |
| Discount | on MP; two discounts: $d_1 + d_2 - d_1 d_2/100$ |
| Equal SP, $x\%$ gain and $x\%$ loss | loss of $x^2/100$ % |
| False weight $w$ g for 1 kg | gain $100(1000 - w)/w$ % |
| SI | PRT/100; doubles in T years when R = 100/T |
| CI | $A = P(1 + R/100)^T$; CI − SI (2 years) = $P(R/100)^2$ |
| Work | together $ab/(a + b)$; use LCM units |
| Pipes | filling +, emptying − |
| Units | km/h × 5/18 = m/s |
| Average speed (equal distances) | $2xy/(x + y)$ |
| Trains | pole: own length; platform: sum of lengths; relative speed: sum (opposite) / difference (same direction) |
| Boats | boat = (down + up)/2, stream = (down − up)/2 |
| Alligation | cheaper : dearer = (d − m) : (m − c) |
| Replacement | $V(1 - x/V)^n$ |
| HCF and LCM | HCF × LCM = product of the two numbers |
| Unit digits | cycles of 4 for 2, 3, 7, 8; of 2 for 4, 9 |
| Sums | $1 + \dots + n = n(n + 1)/2$; first n odd numbers $= n^2$ |

## Chapter summary

- Numerical reasoning carries 5 of the 20 MAT questions; the MEC sample is a
  successive-percentage (area) question: 15 % and 25 % give 43.75 %.
- Two successive changes: $a + b + ab/100$; a price rise of $r\%$ needs a consumption
  cut of $100r/(100 + r)$ % to keep spending the same.
- Profit and loss are on the cost price, discount on the marked price; multiply the
  factors (1.25 × 0.9) for mark-up then discount.
- SI = PRT/100; CI from $P(1 + R/100)^T$; CI − SI for 2 years = $P(R/100)^2$.
- Work: add rates (1/a + 1/b) or use LCM units; pipes that empty subtract.
- Speed: × 5/18 for m/s; average speed is total distance ÷ total time; trains add
  lengths; opposite directions add speeds.
- Ages: test the options; mixtures: the alligation cross; numbers: divisibility
  rules, HCF × LCM = product, unit-digit cycles.
- Estimate when options are far apart; use the options to check size and last digit.

## Practice questions

**Set A — Recall (25 questions)**

1. 25 % of 480 is
   (a) 96 (b) 120 (c) 125 (d) 140
2. 12 is what per cent of 80?
   (a) 12 % (b) 18 % (c) 15 % (d) 20 %
3. When a number is increased by 20 %, it becomes 360. The number is
   (a) 300 (b) 288 (c) 320 (d) 432
4. A price is increased by 10 % and then by 20 %. The total increase is
   (a) 30 % (b) 28 % (c) 35 % (d) 32 %
5. The price of sugar rises by 25 %. By what per cent must a family cut its consumption so that its spending on sugar does not change?
   (a) 25 % (b) 20 % (c) 15 % (d) 30 %
6. A's salary is 20 % more than B's. By what per cent is B's salary less than A's?
   (a) 20 % (b) 18 % (c) 16⅔ % (d) 25 %
7. Rs 7,200 is divided between two brothers in the ratio 4 : 5. The larger share is
   (a) Rs 4,000 (b) Rs 3,200 (c) Rs 4,500 (d) Rs 3,600
8. If a : b = 2 : 3 and b : c = 4 : 5, then a : b : c is
   (a) 2 : 3 : 5 (b) 6 : 12 : 15 (c) 8 : 15 : 12 (d) 8 : 12 : 15
9. The fourth proportional to 4, 6 and 10 is
   (a) 12 (b) 15 (c) 20 (d) 24
10. The mean proportional between 4 and 25 is
   (a) 10 (b) 14.5 (c) 29 (d) 100
11. The average of six numbers is 15. If the number 25 is removed, the average of the remaining five is
   (a) 12 (b) 14 (c) 13 (d) 15
12. The average of the first 20 natural numbers is
   (a) 10 (b) 11 (c) 21 (d) 10.5
13. A shopkeeper buys an article for Rs 400 and sells it for Rs 500. His profit per cent is
   (a) 25 % (b) 20 % (c) 10 % (d) 15 %
14. An article sold for Rs 960 gives a profit of 20 %. Its cost price is
   (a) Rs 768 (b) Rs 780 (c) Rs 800 (d) Rs 1,152
15. A bag marked at Rs 1,200 is sold at a discount of 15 %. Its selling price is
   (a) Rs 1,035 (b) Rs 1,020 (c) Rs 1,080 (d) Rs 1,180
16. The simple interest on Rs 5,000 at 8 % per annum for 3 years is
   (a) Rs 400 (b) Rs 1,250 (c) Rs 6,200 (d) Rs 1,200
17. The compound interest on Rs 10,000 at 10 % per annum for 2 years, compounded yearly, is
   (a) Rs 2,000 (b) Rs 12,100 (c) Rs 2,100 (d) Rs 2,010
18. At what rate of simple interest does a sum of money double itself in 8 years?
   (a) 12.5 % (b) 8 % (c) 10 % (d) 16 %
19. A can finish a job in 12 days and B in 24 days. Working together, they finish it in
   (a) 18 days (b) 8 days (c) 6 days (d) 9 days
20. A speed of 72 km/h is equal to
   (a) 25 m/s (b) 7.2 m/s (c) 259.2 m/s (d) 20 m/s
21. A bus covers 150 km in 2 hours 30 minutes. Its average speed is
   (a) 50 km/h (b) 75 km/h (c) 60 km/h (d) 65 km/h
22. A 200 m long train running at 72 km/h passes an electric pole in
   (a) 10 s (b) 2.8 s (c) 20 s (d) 36 s
23. The sum of the ages of a father and his son is 50 years, and the father is four times as old as the son. The son's age is
   (a) 12.5 years (b) 10 years (c) 40 years (d) 8 years
24. The unit digit of $7^{23}$ is
   (a) 7 (b) 9 (c) 3 (d) 1
25. 98 × 102 =
   (a) 10,004 (b) 9,994 (c) 9,896 (d) 9,996

::: note Answers and explanations — Set A
**1.** (b) — 25 % = 1/4; 480/4 = 120.
**2.** (c) — 12/80 × 100 = 15 %.
**3.** (a) — The number × 1.2 = 360, so the number = 360/1.2 = 300. Taking 20 % off 360 (288) is the trap: the 20 % was of the original number.
**4.** (d) — 10 + 20 + (10 × 20)/100 = 32 %. Check: 1.1 × 1.2 = 1.32.
**5.** (b) — Cut = 25/(100 + 25) × 100 = 20 %. Check: 1.25 × 0.8 = 1.
**6.** (c) — 20/(100 + 20) × 100 = 16⅔ %. If B = 100, A = 120, and 20 out of 120 is 1/6.
**7.** (a) — One part = 7200/9 = 800; the larger share = 5 × 800 = Rs 4,000.
**8.** (d) — Make b equal: a : b = 8 : 12 and b : c = 12 : 15, so a : b : c = 8 : 12 : 15.
**9.** (b) — 4 : 6 = 10 : d gives d = 6 × 10/4 = 15.
**10.** (a) — $\sqrt{4 \times 25}$ = 10. 14.5 is the arithmetic mean, not the mean proportional.
**11.** (c) — Sum = 6 × 15 = 90; without 25 it is 65; 65/5 = 13.
**12.** (d) — (n + 1)/2 = 21/2 = 10.5.
**13.** (a) — Profit 100 on a cost of 400 is 25 %. 20 % is the profit on the selling price — the classic wrong base.
**14.** (c) — CP = 960/1.2 = Rs 800. 768 (= 960 × 0.8) takes 20 % of the selling price.
**15.** (b) — 1200 × 0.85 = Rs 1,020.
**16.** (d) — 5000 × 8 × 3/100 = Rs 1,200. Rs 6,200 is the amount, not the interest.
**17.** (c) — Amount = 10000 × 1.1² = 12,100; CI = 12,100 − 10,000 = Rs 2,100.
**18.** (a) — Doubling means SI = P: R = 100/T = 100/8 = 12.5 %.
**19.** (b) — 12 × 24/(12 + 24) = 288/36 = 8 days. (LCM 24: A does 2 units/day, B 1; 24/3 = 8.)
**20.** (d) — 72 × 5/18 = 20 m/s. 259.2 multiplies by 18/5, the wrong way.
**21.** (c) — 150/2.5 = 60 km/h.
**22.** (a) — 72 km/h = 20 m/s; the train covers its own length: 200/20 = 10 s.
**23.** (b) — Son x, father 4x: 5x = 50, so x = 10. (40 is the father's age.)
**24.** (c) — Powers of 7 end in 7, 9, 3, 1 (cycle 4). 23 = 4 × 5 + 3, so the 3rd term: 3.
**25.** (d) — (100 − 2)(100 + 2) = 10000 − 4 = 9,996.
:::

**Set B — Understanding (15 questions)**

1. The length of a rectangle is increased by 20 % and its breadth is decreased by 20 %. Its area
   (a) does not change (b) decreases by 4 % (c) increases by 4 % (d) decreases by 2 %
2. The population of a town is 20,000. It rises by 10 % in the first year and by 20 % in the second. The population after two years is
   (a) 26,000 (b) 24,000 (c) 26,400 (d) 28,000
3. Two successive discounts of 20 % and 10 % are equal to a single discount of
   (a) 28 % (b) 30 % (c) 25 % (d) 72 %
4. A man sells two watches for Rs 990 each. On one he gains 10 % and on the other he loses 10 %. On the whole he makes
   (a) no profit, no loss (b) 1 % gain (c) 2 % loss (d) 1 % loss
5. A dishonest shopkeeper sells rice at cost price but uses a 900 g weight in place of 1 kg. His gain per cent is
   (a) 10 % (b) 11 1/9 % (c) 9 % (d) 12.5 %
6. The difference between the compound interest (compounded yearly) and the simple interest on Rs 8,000 for 2 years at 5 % per annum is
   (a) Rs 20 (b) Rs 40 (c) Rs 10 (d) Rs 80
7. A and B together can do a piece of work in 10 days, and A alone can do it in 15 days. B alone can do it in
   (a) 25 days (b) 5 days (c) 30 days (d) 6 days
8. Pipe A can fill a tank in 6 hours and pipe B can empty the full tank in 9 hours. If both are opened together in the empty tank, it fills in
   (a) 3 hours (b) 15 hours (c) 3.6 hours (d) 18 hours
9. A car goes from Butwal to Bhairahawa at 40 km/h and returns along the same road at 60 km/h. Its average speed for the round trip is
   (a) 50 km/h (b) 48 km/h (c) 45 km/h (d) 52 km/h
10. Two trains, 150 m and 100 m long, run on parallel tracks in opposite directions at 54 km/h and 36 km/h. The time they take to cross each other is
   (a) 10 s (b) 50 s (c) 25 s (d) 18 s
11. A boat goes downstream at 15 km/h and upstream at 9 km/h. The speed of the stream is
   (a) 6 km/h (b) 12 km/h (c) 3 km/h (d) 4.5 km/h
12. The ages of Ram and Hari are in the ratio 4 : 5. Five years ago the ratio was 3 : 4. Hari's present age is
   (a) 20 years (b) 30 years (c) 15 years (d) 25 years
13. In what ratio must rice at Rs 60 per kg be mixed with rice at Rs 75 per kg so that the mixture is worth Rs 65 per kg?
   (a) 2 : 1 (b) 1 : 2 (c) 3 : 2 (d) 13 : 15
14. The HCF of two numbers is 12 and their LCM is 360. If one number is 72, the other is
   (a) 30 (b) 60 (c) 120 (d) 180
15. (19.98 % of 501.2) + (3.01 × 49.9) is closest to
   (a) 150 (b) 200 (c) 250 (d) 300

::: note Answers and explanations — Set B
**1.** (b) — 20 + (−20) + (20 × −20)/100 = −4 %. Check: 1.2 × 0.8 = 0.96. "No change" is the trap.
**2.** (c) — 20000 × 1.1 × 1.2 = 26,400. Adding 30 % to 20,000 (26,000) ignores the growth on the first year's growth.
**3.** (a) — 20 + 10 − (20 × 10)/100 = 28 %. You pay 0.8 × 0.9 = 72 % of the marked price.
**4.** (d) — Equal SPs with equal gain and loss always give a loss of $x^2/100$ = 1 %. Check: CPs are 990/1.1 = 900 and 990/0.9 = 1,100; total 2,000 against 1,980 received.
**5.** (b) — He gives 900 g but charges for 1000 g: gain = 100/900 × 100 = 11 1/9 %. The gain is on what he gives, not on 1 kg.
**6.** (a) — $P(R/100)^2$ = 8000 × 0.05² = Rs 20.
**7.** (c) — B's rate = 1/10 − 1/15 = 1/30, so 30 days.
**8.** (d) — Net rate = 1/6 − 1/9 = 1/18 per hour: 18 hours. 3.6 hours adds the rates as if both pipes filled.
**9.** (b) — 2 × 40 × 60/(40 + 60) = 48 km/h. 50 km/h is the plain mean, which is wrong because more time is spent at the lower speed.
**10.** (a) — Relative speed = 54 + 36 = 90 km/h = 25 m/s; distance = 150 + 100 = 250 m; time = 10 s. 50 s uses the difference of speeds.
**11.** (c) — Stream = (15 − 9)/2 = 3 km/h; the boat's own speed is (15 + 9)/2 = 12 km/h.
**12.** (d) — Ages 4x, 5x: (4x − 5)/(5x − 5) = 3/4 gives x = 5, so Hari is 25. Check: 15 : 20 = 3 : 4.
**13.** (a) — Alligation: (75 − 65) : (65 − 60) = 10 : 5 = 2 : 1 (cheaper : dearer).
**14.** (b) — Other = 12 × 360/72 = 60. Check: HCF(72, 60) = 12, LCM = 360.
**15.** (c) — 20 % of 500 = 100 and 3 × 50 = 150: about 250 (exactly 250.34).
:::

**Set C — Application (11 questions)**

1. The price of petrol rises by 20 %. A driver wants his spending on petrol to rise by only 8 %. By what per cent must he reduce his consumption?
   (a) 12 % (b) 10 % (c) 8 % (d) 20 %
2. A shopkeeper marks his goods 40 % above the cost price and allows a discount of 10 %. His profit per cent is
   (a) 30 % (b) 36 % (c) 26 % (d) 24 %
3. A sum of money amounts to Rs 13,310 in 3 years at 10 % per annum compound interest, compounded yearly. The sum is
   (a) Rs 10,000 (b) Rs 9,000 (c) Rs 11,000 (d) Rs 10,241
4. A can do a job in 20 days and B in 30 days. They work together for 6 days, and then A leaves. B finishes the remaining work in
   (a) 12 days (b) 18 days (c) 9 days (d) 15 days
5. A train crosses a 300 m long platform in 30 s and an electric pole in 15 s. The length of the train is
   (a) 300 m (b) 150 m (c) 450 m (d) 600 m
6. A vendor has 40 litres of milk. He takes out 4 litres and replaces it with water. After mixing, he again takes out 4 litres of the mixture and replaces it with water. How much milk is left?
   (a) 32 litres (b) 36 litres (c) 32.4 litres (d) 30.4 litres
7. The average age of 30 students is 15 years. When the teacher's age is included, the average rises by 1 year. The teacher's age is
   (a) 31 years (b) 45 years (c) 16 years (d) 46 years
8. Walking at 3 km/h, a student reaches school 10 minutes late; walking at 4 km/h, he reaches 10 minutes early. The distance to the school is
   (a) 4 km (b) 6 km (c) 2 km (d) 12 km
9. The smallest two-digit number that leaves a remainder of 3 when divided by each of 4, 6 and 9 is
   (a) 36 (b) 39 (c) 42 (d) 75
10. A father is three times as old as his son. After 10 years he will be twice as old as his son. The father's present age is
   (a) 40 years (b) 20 years (c) 30 years (d) 45 years
11. A sum lent at simple interest amounts to Rs 7,200 in 2 years and to Rs 8,400 in 4 years. The rate of interest is
   (a) 8 % (b) 12 % (c) 15 % (d) 10 %

::: note Answers and explanations — Set C
**1.** (b) — New spending = 1.2 × (new consumption) = 1.08, so consumption = 1.08/1.2 = 0.9: a 10 % cut.
**2.** (c) — 1.4 × 0.9 = 1.26, a 26 % profit. Subtracting (40 − 10 = 30 %) ignores that the discount is on the higher, marked price.
**3.** (a) — P = 13310/1.1³ = 13310/1.331 = Rs 10,000.
**4.** (d) — In 6 days they do 6 × (1/20 + 1/30) = 6 × 1/12 = 1/2 of the work. B does the other half at 1/30 per day: 15 days.
**5.** (a) — Speed = L/15 = (L + 300)/30, so 2L = L + 300 and L = 300 m (speed 20 m/s).
**6.** (c) — Each replacement keeps 9/10 of the milk: 40 × 0.9 × 0.9 = 32.4 litres. 32 litres would be right only if 8 litres of pure milk were removed.
**7.** (d) — New total = 31 × 16 = 496; old total = 30 × 15 = 450; teacher = 46 years. (Shortcut: 16 + 30 × 1 = 46.)
**8.** (a) — The two times differ by 20 minutes: d/3 − d/4 = 1/3 hour, so d/12 = 1/3 and d = 4 km. Check: 80 min and 60 min around a 70-minute schedule.
**9.** (b) — LCM(4, 6, 9) = 36, so the numbers are 36k + 3: 3, 39, 75, … The smallest two-digit one is 39.
**10.** (c) — Son s, father 3s: 3s + 10 = 2(s + 10) gives s = 10, so the father is 30. Check: in 10 years, 40 = 2 × 20.
**11.** (d) — Two years' interest = 8400 − 7200 = 1,200, so Rs 600 a year. P = 7200 − 1200 = 6,000; R = 600/6000 × 100 = 10 %.
:::
