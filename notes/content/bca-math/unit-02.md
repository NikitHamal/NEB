---
subject: Mathematics
grade: BCA
unit: 2
title: Profit and Loss, Interest, Work, Speed, Mixture and Mensuration
hours: 5
area: Arithmetic
---

This is the second half of the arithmetic block: the "business and motion" problems. Five questions of the 50 come from here in a typical paper, and they are the most formula-driven in the whole mathematics section. Each type has one setup that, once learnt, turns a 90-second question into a 30-second one. The mensuration part is the one most students forget: the Dean's Office model asks even "how many squares are in this figure", so know your areas and volumes cold.

::: key What the paper asks from this chapter
- **Profit and loss**: percent on the cost price; discount on the marked price; successive discounts; a "false weight" dealer.
- **Interest**: $\text{SI}=\frac{PRT}{100}$, compound amount $P(1+\frac{R}{100})^n$, and the two-year shortcut $\text{CI}-\text{SI}=P(\frac{R}{100})^2$.
- **Work**: $\frac{ab}{a+b}$ for two workers, and inlet/outlet pipes with a minus sign.
- **Speed**: $\text{km/h}\times\frac{5}{18}=\text{m/s}$, average speed over equal distances, trains and boats.
- **Mixture**: the alligation cross, and repeated replacement.
- **Mensuration**: area and volume formulas, and percentage change in area/volume.
:::

## 2.1 Profit, loss, discount and marked price

- $\text{Profit}=SP-CP$, $\text{Loss}=CP-SP$. **Profit % and loss % are always on the cost price.**
- $SP=CP\left(1+\frac{p}{100}\right)$ for profit $p\%$, and $SP=CP\left(1-\frac{l}{100}\right)$ for loss $l\%$.
- **Discount is on the marked price (MP)**: $SP=MP\left(1-\frac{d}{100}\right)$. Successive discounts multiply: $MP\times(1-d_1)(1-d_2)$.
- **Mark-up then discount**: marking 25 % above cost and allowing 20 % discount gives $1.25\times0.8=1.00$, so no profit and no loss.
- **False weight**: a dealer who uses $w$ grams for a kilogram gains $\frac{1000-w}{w}\times100\%$.
- If the same article is sold at two prices, one gaining $x\%$ and the other losing $x\%$, the net result is a loss of $\frac{x^2}{100}\%$.

::: example Reselling at a higher profit
**Problem.** By selling an article for Rs 540 a man gains 20 %. At what price must he sell it to gain 30 %?

**Solution.** $CP=\dfrac{540}{1.2}=450$. New $SP=450\times1.3=585$.
:::

```svgfig label="2.1" caption="Profit, loss and discount from one price tag, computed. An article marked Rs 1,000 is sold at 20 percent discount, so SP = Rs 800. It cost Rs 640, so profit = Rs 160, which is 25 percent of the COST price (160 / 640), while the discount of Rs 200 is 20 percent of the MARKED price. Profit is always on CP, discount always on MP."
MP = 1000; disc = 20; SP = MP * (100 - disc) // 100; CP = 640
profit = SP - CP; assert (SP, profit) == (800, 160) and profit * 100 / CP == 25 and MP - SP == 200
f = Fig(780, 300)
sc = 0.2; base = 250
def bar(x, v, lab, col, y0=0):
    h = v * sc; f.box(x, base - y0 * sc - h, 92, h, "Rs %d" % v, fill=col, stroke=NAVY, size=11.5, bold=True, r=2)
    f.text(x + 46, base + 20, lab, size=10.5, color=SLATE, bold=True)
bar(30, 640, "cost price CP", "#bfdbfe")
bar(140, 160, "profit", "#bbf7d0", y0=640)
bar(250, 800, "selling price SP", "#fde68a")
bar(360, 200, "discount", "#fecaca", y0=800)
bar(470, 1000, "marked price MP", "#e2e8f0")
f.line(30, base - 800 * sc, 562, base - 800 * sc, color=AMBER, sw=1, dash=True)
f.text(640, 40, "Rules to remember", size=11.5, color=NAVY, bold=True)
for j, (t, c) in enumerate([("Profit % = profit / CP x 100", TEAL), ("Discount % = discount / MP x 100", TEAL), ("SP = CP x (100 + p) / 100", SLATE), ("SP = MP x (100 - d) / 100", SLATE), ("Here: 160/640 = 25 percent", RED), ("and: 200/1000 = 20 percent", RED)]):
    f.text(600, 76 + j * 30, t, size=10.5, color=c, anchor="start", bold=(c == RED))
```

## 2.2 Simple and compound interest

- **Simple interest**: $\text{SI}=\dfrac{PRT}{100}$ and amount $A=P+\text{SI}$. $R$ is per year, $T$ in years.
- **Compound interest**: $A=P\left(1+\frac{R}{100}\right)^n$ and $\text{CI}=A-P$. For half-yearly compounding use $\frac{R}{2}$ and $2n$.
- **Two years**: $\text{CI}-\text{SI}=P\left(\frac{R}{100}\right)^2$. For two years at $R\%$ the CI equals $\left(2R+\frac{R^2}{100}\right)\%$ of $P$ (21 % for 10 %).
- **Doubling at SI**: a sum doubles in $\frac{100}{R}$ years; it becomes $n$ times in $\frac{100(n-1)}{R}$ years.
- If a sum amounts to $A_1$ in $t_1$ years and $A_2$ in $t_2$ years at SI, the yearly interest is $\frac{A_2-A_1}{t_2-t_1}$, and $P=A_1-t_1\times$ (yearly interest).

```photogrid label="2.1" cols="1" ratio="2.4" caption="An old Nepali paper note (the face is King Mahendra). Interest, profit and loss are all questions about money like this: Nepal Rastra Bank issues the notes, and banks, cooperatives and Fonepay wallets use the interest formulas of this section every day."
@ photo id="bcamath/oldnote" cap="An old Nepali one-rupee note"
focus 0.5 0.5
```

```svgfig label="2.2" caption="Simple versus compound interest on Rs 10,000 at 10 percent a year, computed. Simple interest grows by Rs 1,000 every year in a straight line; compound interest grows by 10 percent of a bigger amount each time, so the curve bends upward. After 2 years the gap is only P x r^2 / 100^2 = Rs 100, but after 10 years CI amount is Rs 25,937.42 against Rs 20,000."
P, r = 10000, 10
si = lambda t: P + P * r * t / 100
ci = lambda t: P * (1 + r / 100) ** t
assert round(ci(2) - si(2), 2) == 100 and round(ci(10), 2) == 25937.42 and si(10) == 20000
f = Fig(780, 320)
ax = Axes(f, 70, 30, 440, 250, (0, 10), (8000, 28000))
ax.grid(2, 4000)
ax.axes("years", "amount (Rs)")
ax.curve(si, 0, 10, color=TEAL, sw=2.4)
ax.curve(ci, 0, 10, color=NAVY, sw=2.4)
ax.pt(2, ci(2), "", r=4, color=RED); ax.pt(10, ci(10), "", r=4, color=RED); ax.pt(10, si(10), "", r=4, color=AMBER)
f.text(400, 90, "compound  25,937", size=11, color=NAVY, bold=True, anchor="end")
f.text(430, 175, "simple  20,000", size=11, color=TEAL, bold=True, anchor="end")
f.text(640, 40, "Amount after t years", size=11.5, color=NAVY, bold=True)
f.text(560, 70, "t", size=10.5, color=SLATE, bold=True, anchor="start"); f.text(620, 70, "simple", size=10.5, color=TEAL, bold=True, anchor="start"); f.text(700, 70, "compound", size=10.5, color=NAVY, bold=True, anchor="start")
for j, t in enumerate([1, 2, 3, 5, 10]):
    y = 100 + j * 30
    f.text(560, y, str(t), size=10.5, color=SLATE, anchor="start"); f.text(620, y, "{:,.0f}".format(si(t)), size=10.5, color=TEAL, anchor="start"); f.text(700, y, "{:,.0f}".format(ci(t)), size=10.5, color=NAVY, anchor="start")
f.text(640, 275, "CI - SI for 2 years = 100", size=11, color=RED, bold=True)
```

## 2.3 Time and work, pipes and cisterns

- If $A$ does a job in $a$ days, his one-day work is $\frac{1}{a}$. Rates add: together $\frac{1}{a}+\frac{1}{b}=\frac{a+b}{ab}$, so the time is $\frac{ab}{a+b}$.
- If $A+B$ take $t$ days and $A$ alone takes $a$, then $B$ alone takes $\frac{at}{a-t}$.
- **Men–days–hours**: $\dfrac{M_1D_1H_1}{W_1}=\dfrac{M_2D_2H_2}{W_2}$.
- **Pipes**: an inlet gives $+\frac{1}{x}$ per minute, an outlet $-\frac{1}{y}$. With both open: $\frac{1}{x}-\frac{1}{y}$ of the tank per minute.
- Work done in part: if $A$ works $k$ days, $\frac{k}{a}$ is done and the rest is $1-\frac{k}{a}$.

```svgfig label="2.3" caption="Rates of work add. A finishes a job in 10 days (1/10 per day), B in 15 days (1/15 per day), so together they do 1/10 + 1/15 = 1/6 of the job a day and need 6 days. For pipes the same idea: an inlet that fills a tank in 12 h and a leak that empties it in 18 h leave a net rate of 1/12 - 1/18 = 1/36, so the tank fills in 36 h. All values are computed with fractions."
from fractions import Fraction as F
a, b = F(1, 10), F(1, 15); tog = a + b; assert tog == F(1, 6) and 1 / tog == 6
inl, lk = F(1, 12), F(1, 18); net = inl - lk; assert net == F(1, 36) and 1 / net == 36
f = Fig(780, 300)
f.text(190, 22, "(a) Two workers", size=11.5, color=NAVY, bold=True)
W = 330
def seg(y, parts, lab):
    f.text(20, y + 18, lab, size=10.5, color=SLATE, anchor="start", bold=True)
    x = 120
    for frac, col, tx in parts:
        w = W * float(frac) * 3; f.box(x, y, w, 30, tx, fill=col, stroke=NAVY, size=10.5, bold=True, r=2); x += w
f.text(285, 56, "fraction of the job done in ONE day", size=10, color=SLATE)
seg(70, [(a, "#bfdbfe", "1/10")], "A alone")
seg(120, [(b, "#fde68a", "1/15")], "B alone")
seg(170, [(a, "#bfdbfe", "1/10"), (b, "#fde68a", "1/15")], "together")
f.box(120, 220, W / 2, 30, "1/6", fill="#bbf7d0", stroke=TEAL, size=10.5, bold=True, r=2)
f.text(20, 238, "one day = 1/6", size=10.5, color=TEAL, anchor="start", bold=True)
f.text(300, 238, "so 6 days for the whole job", size=10.5, color=TEAL, anchor="start", bold=True)
f.text(600, 22, "(b) Inlet and leak", size=11.5, color=NAVY, bold=True)
f.box(520, 60, 160, 150, "", fill="#f8fafc", stroke=NAVY)
f.box(521, 140, 158, 69, "", fill="#bfdbfe", stroke="#bfdbfe")
f.arrow([(470, 80), (520, 80)], color=TEAL, sw=2.4); f.text(470, 62, "inlet +1/12 per h", size=10, color=TEAL, bold=True, anchor="start")
f.arrow([(520, 195), (730, 195)], color=RED, sw=2.4); f.text(690, 180, "leak -1/18 per h", size=10, color=RED, bold=True, anchor="end")
f.text(600, 240, "net 1/12 - 1/18 = 1/36 per h", size=11, color=NAVY, bold=True)
f.text(600, 264, "tank full in 36 hours", size=11, color=RED, bold=True)
```

## 2.4 Speed, distance, time, trains and boats

- $v=\dfrac{d}{t}$. **km/h to m/s: multiply by $\frac{5}{18}$; m/s to km/h: multiply by $\frac{18}{5}$.** (36 km/h = 10 m/s.)
- **Average speed** over equal distances at $x$ and $y$ is $\dfrac{2xy}{x+y}$, not $\frac{x+y}{2}$. For equal times it is $\frac{x+y}{2}$.
- **Trains.** Crossing a pole or a person: distance $=L$. Crossing a platform or another train: distance $=L+P$ (or $L_1+L_2$). Relative speed is the **sum** for opposite directions and the **difference** for the same direction.
- **Boats.** With boat speed $u$ and stream speed $v$: downstream $u+v$, upstream $u-v$, so $u=\frac{D+U}{2}$ and $v=\frac{D-U}{2}$.

::: caution
Convert units *first*. The three commonest wrong options are the unconverted answer, the answer in m/s when km/h is asked, and the arithmetic mean instead of $\frac{2xy}{x+y}$.
:::

```svgfig label="2.4" caption="Trains and boats, computed. (a) A 150 m train at 54 km/h = 15 m/s crosses a 350 m platform by covering 150 + 350 = 500 m, which takes 500 / 15 = 33.3 s. (b) A boat of 15 km/h in still water in a 3 km/h stream goes at 18 km/h downstream and 12 km/h upstream; for the same distance each way the AVERAGE speed is 2 x 18 x 12 / 30 = 14.4 km/h, not 15."
v = 54 * 5 / 18; assert v == 15
t = (150 + 350) / v; assert round(t, 1) == 33.3
dn, up = 15 + 3, 15 - 3; avg = 2 * dn * up / (dn + up); assert (dn, up, round(avg, 1)) == (18, 12, 14.4)
f = Fig(780, 320)
f.text(200, 22, "(a) Train crossing a platform", size=11.5, color=NAVY, bold=True)
f.box(30, 90, 120, 40, "train 150 m", fill="#fde68a", stroke=AMBER, size=10.5, bold=True, r=3)
f.box(150, 110, 250, 20, "platform 350 m", fill="#e2e8f0", stroke=SLATE, size=10.5, bold=True, r=2)
f.arrow([(30, 160), (400, 160)], color=TEAL, sw=2, both=True)
f.text(215, 182, "distance = 150 + 350 = 500 m", size=11, color=TEAL, bold=True)
f.text(215, 212, "speed 54 km/h x 5/18 = 15 m/s", size=11, color=NAVY, bold=True)
f.text(215, 238, "time = 500 / 15 = 33.3 s", size=11.5, color=RED, bold=True)
f.text(215, 275, "km/h to m/s: multiply by 5/18", size=10.5, color=SLATE)
f.text(600, 22, "(b) Boat in a stream", size=11.5, color=NAVY, bold=True)
f.box(470, 95, 270, 40, "", fill="#dbeafe", stroke="#93c5fd", r=3)
f.arrow([(500, 70), (710, 70)], color=TEAL, sw=2.4); f.text(605, 56, "downstream 15 + 3 = 18 km/h", size=10.5, color=TEAL, bold=True)
f.arrow([(710, 160), (500, 160)], color=RED, sw=2.4); f.text(605, 182, "upstream 15 - 3 = 12 km/h", size=10.5, color=RED, bold=True)
f.text(605, 122, "still water 15, stream 3", size=10.5, color=NAVY, bold=True)
f.text(605, 222, "average for equal distance", size=10.5, color=SLATE)
f.text(605, 244, "2 x 18 x 12 / (18 + 12) = 14.4", size=11, color=NAVY, bold=True)
f.text(605, 275, "(not (18 + 12) / 2 = 15)", size=10.5, color=RED, bold=True)
```

## 2.5 Mixtures and alligation

- **Alligation.** For a mixture of a cheaper and a dearer item with mean price $m$: $\dfrac{\text{quantity of cheaper}}{\text{quantity of dearer}}=\dfrac{d-m}{m-c}$.
- **Replacement.** A vessel holds $V$ litres of pure liquid. Remove $x$ litres and refill with water, repeated $k$ times: pure liquid left $=V\left(1-\frac{x}{V}\right)^k$.
- Concentrations of two solutions mixed in ratio $p:q$ give $\frac{p\,c_1+q\,c_2}{p+q}$.

```svgfig label="2.5" caption="Alligation as a cross. To mix rice at Rs 40 and Rs 60 per kg into a blend worth Rs 52, write the mean 52 in the middle and subtract diagonally: 60 - 52 = 8 parts of the cheap rice and 52 - 40 = 12 parts of the dear rice, so the ratio cheap : dear = 8 : 12 = 2 : 3. A 50 kg bag then holds 20 kg and 30 kg, and the cost 20 x 40 + 30 x 60 = 2,600 = 50 x 52 confirms it."
cheap, dear, mean = 40, 60, 52
rc, rd = dear - mean, mean - cheap; assert (rc, rd) == (8, 12)
k = 50 / (rc + rd) ; q1, q2 = rc * k, rd * k; assert (q1, q2) == (20.0, 30.0)
assert q1 * cheap + q2 * dear == 50 * mean == 2600
f = Fig(780, 300)
f.box(60, 40, 130, 54, "cheap rice\nRs 40 per kg", fill="#bfdbfe", stroke=NAVY, size=11, bold=True, r=3)
f.box(60, 200, 130, 54, "dear rice\nRs 60 per kg", fill="#fde68a", stroke=AMBER, size=11, bold=True, r=3)
f.box(280, 118, 120, 64, "mean price\nRs 52", fill="#bbf7d0", stroke=TEAL, size=12, bold=True, r=3)
f.line(190, 67, 280, 140, color=SLATE, sw=1.4); f.line(190, 227, 280, 160, color=SLATE, sw=1.4)
f.line(400, 140, 500, 67, color=RED, sw=2); f.line(400, 160, 500, 227, color=RED, sw=2)
f.box(500, 40, 130, 54, "8 parts of\ncheap rice", fill="#fef2f2", stroke=RED, size=11, bold=True, r=3)
f.box(500, 200, 130, 54, "12 parts of\ndear rice", fill="#fef2f2", stroke=RED, size=11, bold=True, r=3)
f.text(255, 82, "60 - 52", size=10.5, color=SLATE); f.text(255, 232, "52 - 40", size=10.5, color=SLATE)
f.text(700, 130, "ratio 8 : 12", size=11.5, color=NAVY, bold=True); f.text(700, 152, "= 2 : 3", size=11.5, color=NAVY, bold=True)
f.text(700, 190, "50 kg bag:", size=10.5, color=SLATE); f.text(700, 210, "20 kg + 30 kg", size=11, color=TEAL, bold=True)
```

## 2.6 Area, perimeter and volume of plane and solid figures

| Figure | Area / surface | Perimeter / volume |
|---|---|---|
| Rectangle $l\times b$ | $lb$ | $2(l+b)$ |
| Square $a$ | $a^2$ | $4a$ |
| Triangle | $\frac{1}{2}bh$; equilateral $\frac{\sqrt{3}}{4}a^2$ | sum of sides |
| Trapezium | $\frac{1}{2}(a+b)h$ | |
| Rhombus | $\frac{1}{2}d_1d_2$ | $4a$ |
| Circle | $\pi r^2$ | $2\pi r$ |
| Cuboid | $2(lb+bh+hl)$ | $V=lbh$; diagonal $\sqrt{l^2+b^2+h^2}$ |
| Cube | $6a^2$ | $V=a^3$; diagonal $a\sqrt{3}$ |
| Cylinder | curved $2\pi rh$; total $2\pi r(r+h)$ | $V=\pi r^2h$ |
| Cone | curved $\pi rl$, $l=\sqrt{r^2+h^2}$ | $V=\frac{1}{3}\pi r^2h$ |
| Sphere | $4\pi r^2$ | $V=\frac{4}{3}\pi r^3$ |
| Hemisphere | curved $2\pi r^2$; total $3\pi r^2$ | $V=\frac{2}{3}\pi r^3$ |

- **Scaling.** If every length is multiplied by $k$, areas scale by $k^2$ and volumes by $k^3$. Doubling a sphere's radius multiplies the volume by 8.
- **Percentage change in area.** Length up $a\%$ and breadth up $b\%$: area changes by $a+b+\frac{ab}{100}$ per cent. The MEC-style example (15 % and 25 %) gives $43.75\%$.

::: tip
Use $\pi=\frac{22}{7}$ when the radius is a multiple of 7. Otherwise leave $\pi$ in the answer and compare options.
:::

```photogrid label="2.2" cols="2" ratio="1.35" caption="Solids you can measure. (a) The Great Pyramid of Giza, a square pyramid: with base 230.34 m and height 146.5 m its volume is one third of base area x height, about 2.59 million cubic metres. (b) A cylindrical hot-water tank: volume = pi r^2 h, curved surface = 2 pi r h."
@ photo id="bcamath/pyramid" cap="Square pyramid: V = (1/3) x base x height"
focus 0.5 0.55
@ photo id="bcamath/tank" cap="Cylinder: V = pi r^2 h"
focus 0.5 0.45
```

```svgfig label="2.6" caption="Archimedes' favourite result, computed. For a cone, a sphere and a cylinder of the SAME radius r = 7 cm, with height equal to the diameter (14 cm), the volumes are 718.67, 1,437.33 and 2,156 cm3, in the exact ratio 1 : 2 : 3. The pyramid on the left is checked in the cell: V = (1/3) x 230.34 x 230.34 x 146.5 = 2.59 million m3."
pi = 22 / 7; r = 7; h = 14
cone = pi * r * r * h / 3; sph = 4 * pi * r ** 3 / 3; cyl = pi * r * r * h
assert round(cone, 2) == 718.67 and round(sph, 2) == 1437.33 and round(cyl, 2) == 2156.0
assert round(sph / cone, 6) == 2 and round(cyl / cone, 6) == 3
V = 230.34 ** 2 * 146.5 / 3; assert 2.58e6 < V < 2.60e6
f = Fig(780, 320)
sc = 0.11
for i, (n, v, c, form) in enumerate([("cone", cone, "#bfdbfe", "(1/3) pi r^2 h"), ("sphere", sph, "#bbf7d0", "(4/3) pi r^3"), ("cylinder", cyl, "#fde68a", "pi r^2 h")]):
    x = 90 + i * 150; hh = v * sc
    f.box(x, 270 - hh, 100, hh, "%.2f" % v if i < 2 else "%.0f" % v, fill=c, stroke=NAVY, size=11, bold=True, r=2)
    f.text(x + 50, 290, n, size=11, color=NAVY, bold=True); f.text(x + 50, 308, form, size=10, color=SLATE)
f.text(250, 24, "same r = 7 cm, h = 2r = 14 cm (volumes in cm3)", size=11, color=NAVY, bold=True)
f.text(620, 80, "Ratio 1 : 2 : 3", size=14, color=RED, bold=True)
for j, t in enumerate(["cone : sphere : cylinder", "718.67 : 1437.33 : 2156", "(each divided by 718.67)", "Other solids to remember", "cuboid  lbh,  surface 2(lb + bh + hl)", "cube  a^3,  surface 6a^2", "cone slant l = sqrt(r^2 + h^2)", "sphere surface 4 pi r^2"]):
    f.text(560, 112 + j * 24, t, size=10.5, color=(NAVY if j == 3 else SLATE), anchor="start", bold=(j == 3))
```

## 2.7 Eight traps in profit, interest, work, speed and mixture questions

These problems are all short formulas, so the trap is nearly always a base, a unit or a sign. The eight below come up again and again in the Dean's Office model and in earlier TU entrance papers.

1. **Profit is on cost price; discount is on marked price.** A shopkeeper who marks Rs 1,000 and gives 20 percent off sells at Rs 800, and if the cost was Rs 640 the profit is $160/640=25$ percent, not 20 (Fig 2.1). Reading the wrong base is the single most common error. Underline "on cost" or "on marked price" before you calculate.
2. **A "gain of $p$ percent" means $SP=CP\times\frac{100+p}{100}$.** To find the cost price from the selling price you must divide, not subtract. If a radio sold for Rs 1,320 at a 10 percent gain, then $CP=1320\times\frac{100}{110}=1200$, not $1320-132=1188$. The same idea works for loss with $100-p$.
3. **Simple interest is a straight line; compound interest is not.** With $SI=\frac{PRT}{100}$ the interest is the same every year, but with compound interest the amount is $P\left(1+\frac{R}{100}\right)^n$ and each year's interest is bigger than the last (Fig 2.2). The question may ask for the interest, so subtract $P$ from the amount. For 2 years the difference $CI-SI$ equals $\frac{PR^2}{100^2}$, a quick check that saves time.
4. **Match the time unit to the rate.** A rate of 12 percent per annum for 9 months is $T=\frac{9}{12}=0.75$ year, not 9. With half-yearly compounding, halve the rate and double the number of periods. Forgetting this turns a Rs 1,080 answer into a Rs 10,800 one.
5. **Work adds as rates, never as days.** If A needs 10 days and B needs 15 days, together they need $\frac{10\times15}{10+15}=6$ days, not the average 12.5 days (Fig 2.3). A leak or outlet pipe has a negative rate, so subtract it. The answer is always smaller than the faster worker's time alone when both are helping.
6. **Convert units before using $d=vt$.** Speed in km/h becomes m/s on multiplying by $\frac{5}{18}$, and m/s becomes km/h on multiplying by $\frac{18}{5}$. A train crossing a platform covers its own length plus the platform's, while crossing a pole it covers only its own length (Fig 2.4). Mixing metres with kilometres is how a correct method gets a wrong option.
7. **Average speed is not the average of the speeds.** For equal distances the average speed is the harmonic mean $\frac{2uv}{u+v}$, so a boat going 18 km/h downstream and 12 km/h upstream averages 14.4 km/h. If the equal quantity is time, not distance, then the simple average is correct. Say which quantity is equal before you choose the formula.
8. **Alligation gives a ratio of quantities, and the mean sits in the middle.** Subtract diagonally (Fig 2.5): the quantity ratio is $(d-m):(m-c)$, which is the reverse of what students expect. The mean must lie between the two prices, otherwise the problem has no solution. Also keep $\pi=\frac{22}{7}$ for mensuration when the radius is a multiple of 7, and remember that the cone, sphere and cylinder ratio is $1:2:3$ when $h=2r$ (Fig 2.6).

### 2.7.1 Worked checks

**Q. A trader marks a watch 25 percent above cost and then allows a 20 percent discount. Find his gain percent.**

**Answer.** Take CP $=100$. Marked price $=125$. Selling price $=125\times0.80=100$. So the gain is $0$ percent. Using the successive-change formula, $25-20-\frac{25\times20}{100}=0$, which agrees.

**Q. Find the compound interest on Rs 8,000 for 2 years at 5 percent per annum.**

**Answer.** Amount $=8000\times1.05^2=8000\times1.1025=8820$, so $CI=8820-8000=\text{Rs }820$. Check with the shortcut: $SI=\frac{8000\times5\times2}{100}=800$ and $CI-SI=\frac{8000\times25}{10000}=20$, so $CI=820$. Both routes give the same result.

**Q. A can finish a job in 12 days and B in 18 days. They work together for 4 days and then A leaves. How many more days does B need?**

**Answer.** Work done in 4 days $=4\left(\frac1{12}+\frac1{18}\right)=4\times\frac{5}{36}=\frac{5}{9}$, so $\frac49$ remains. B works at $\frac1{18}$ per day, so he needs $\frac49\times18=8$ more days. Check: B in 12 days alone does $\frac{12}{18}=\frac23$, and A does $\frac4{12}=\frac13$, total 1.

## Formula and fact sheet

| Topic | Result |
|---|---|
| Profit % | $\frac{SP-CP}{CP}\times100$ |
| Discount | on MP; successive discounts multiply |
| SI, CI (2 yr) | $\frac{PRT}{100}$; $\text{CI}-\text{SI}=P(\frac{R}{100})^2$ |
| Two workers | $\frac{ab}{a+b}$ days |
| Average speed | $\frac{2xy}{x+y}$ (equal distances) |
| Boat | $u=\frac{D+U}{2}$, $v=\frac{D-U}{2}$ |
| Alligation | cheaper : dearer $=(d-m):(m-c)$ |
| Cylinder, cone, sphere | $\pi r^2h$, $\frac{1}{3}\pi r^2h$, $\frac{4}{3}\pi r^3$ |

## Chapter summary

- Profit and loss use the cost price; discount uses the marked price.
- Mark up 25 % and discount 20 % gives no gain, no loss.
- For two years, compound interest exceeds simple interest by $P(R/100)^2$.
- Two workers together take $ab/(a+b)$ days; a leaking pipe subtracts its rate.
- 36 km/h is 10 m/s; multiply by 5/18 to go from km/h to m/s.
- Average speed over equal distances is the harmonic mean, never the simple mean.
- A train crossing a platform covers its own length plus the platform.
- Alligation gives the ratio directly as the two differences across the cross.

## Practice questions

**Set A — Recall (20 questions)**

1. Profit per cent is calculated on the
   (a) selling price (b) marked price (c) cost price (d) discount
2. The simple interest on Rs 5,000 at 8 % per annum for 3 years is
   (a) Rs 1,200 (b) Rs 1,000 (c) Rs 1,500 (d) Rs 1,600
3. A speed of 36 km/h equals
   (a) 6 m/s (b) 8 m/s (c) 12 m/s (d) 10 m/s
4. A can do a job in 10 days and B in 15 days. Working together they finish in
   (a) 5 days (b) 6 days (c) 8 days (d) 12 days
5. An article bought for Rs 400 is sold for Rs 460. The profit per cent is
   (a) 15 % (b) 12 % (c) 14 % (d) 60 %
6. The area of a circle of radius 7 cm (π = 22/7) is
   (a) 44 cm² (b) 49 cm² (c) 154 cm² (d) 308 cm²
7. The volume of a cube of side 5 cm is
   (a) 25 cm³ (b) 75 cm³ (c) 150 cm³ (d) 125 cm³
8. The difference between compound and simple interest on Rs 1,000 at 10 % for 2 years is
   (a) Rs 1 (b) Rs 10 (c) Rs 100 (d) Rs 20
9. The area of a triangle of base 10 cm and height 6 cm is
   (a) 60 cm² (b) 16 cm² (c) 30 cm² (d) 15 cm²
10. A marked price of Rs 800 with a 10 % discount gives a selling price of
    (a) Rs 720 (b) Rs 710 (c) Rs 700 (d) Rs 730
11. A man covers equal distances at 40 km/h and 60 km/h. His average speed is
    (a) 50 km/h (b) 52 km/h (c) 45 km/h (d) 48 km/h
12. The surface area of a sphere of radius $r$ is
    (a) $2\pi r^2$ (b) $4\pi r^2$ (c) $\frac{4}{3}\pi r^2$ (d) $\pi r^2$
13. The curved surface area of a cylinder is
    (a) $\pi r^2h$ (b) $2\pi r(r+h)$ (c) $2\pi rh$ (d) $\pi rh$
14. To convert m/s into km/h we multiply by
    (a) $\frac{5}{18}$ (b) $\frac{3}{5}$ (c) $\frac{1000}{60}$ (d) $\frac{18}{5}$
15. The perimeter of a rectangle 12 m by 8 m is
    (a) 40 m (b) 96 m (c) 20 m (d) 48 m
16. The volume of a cone with radius 3 cm and height 7 cm (π = 22/7) is
    (a) 44 cm³ (b) 66 cm³ (c) 132 cm³ (d) 198 cm³
17. An article costing Rs 500 is sold at a 10 % loss. The selling price is
    (a) Rs 400 (b) Rs 440 (c) Rs 450 (d) Rs 490
18. If a worker finishes a job in 8 days, his one-day work is
    (a) $\frac{1}{8}$ (b) 8 (c) $\frac{1}{16}$ (d) $\frac{1}{4}$
19. A rhombus has diagonals 10 cm and 24 cm. Its area is
    (a) 240 cm² (b) 34 cm² (c) 60 cm² (d) 120 cm²
20. At simple interest a sum doubles itself in 10 years. The rate per annum is
    (a) 5 % (b) 10 % (c) 12.5 % (d) 20 %

::: note Answers and explanations — Set A
**1.** (c) — profit and loss per cent are on the cost price; discount is on the marked price.
**2.** (a) — 5000 × 8 × 3 / 100 = 1200.
**3.** (d) — 36 × 5/18 = 10 m/s.
**4.** (b) — 10 × 15 / 25 = 6 days.
**5.** (a) — profit 60 on cost 400 is 15 %. Option (d) divides by the selling price's gap wrongly.
**6.** (c) — (22/7) × 49 = 154. Option (a) 44 is the circumference.
**7.** (d) — 5³ = 125. Option (a) 25 is a face area.
**8.** (b) — P(R/100)² = 1000 × 0.01 = 10.
**9.** (c) — ½ × 10 × 6 = 30. Forgetting the ½ gives 60.
**10.** (a) — 800 × 0.9 = 720.
**11.** (d) — 2 × 40 × 60 / 100 = 48. The simple mean 50 is the standard distractor.
**12.** (b) — surface area 4πr²; (c) is a volume-like expression.
**13.** (c) — curved surface = circumference × height = 2πrh; (b) is the total surface.
**14.** (d) — m/s to km/h is × 18/5 (= 3.6); the reverse is × 5/18.
**15.** (a) — 2(12 + 8) = 40.
**16.** (b) — (1/3)(22/7)(9)(7) = 66.
**17.** (c) — 500 × 0.9 = 450.
**18.** (a) — one-day work is 1 over the days taken.
**19.** (d) — ½ × 10 × 24 = 120. Option (a) forgets the ½.
**20.** (b) — time to double = 100 / R, so R = 100 / 10 = 10 %.
:::

**Set B — Understanding (12 questions)**

1. A shopkeeper allows successive discounts of 10 % and 20 % on a marked price of Rs 1,000. The selling price is
   (a) Rs 700 (b) Rs 720 (c) Rs 730 (d) Rs 750
2. A trader marks goods 25 % above cost and allows a 20 % discount. He makes
   (a) 5 % profit (b) 5 % loss (c) 20 % profit (d) neither profit nor loss
3. The compound interest on Rs 8,000 at 10 % per annum for 2 years is
   (a) Rs 1,680 (b) Rs 1,600 (c) Rs 1,800 (d) Rs 1,720
4. At simple interest a sum becomes Rs 6,600 in 2 years and Rs 7,200 in 3 years. The principal is
   (a) Rs 5,000 (b) Rs 5,200 (c) Rs 5,400 (d) Rs 5,600
5. A can finish a job in 12 days and B in 18 days. A works for 4 days and leaves; B finishes the rest in
   (a) 8 days (b) 9 days (c) 10 days (d) 12 days
6. A pipe fills a tank in 20 minutes and another empties it in 30 minutes. With both open the tank fills in
   (a) 50 min (b) 60 min (c) 120 min (d) 25 min
7. A train 150 m long passes a pole in 10 seconds. Its speed is
   (a) 54 km/h (b) 45 km/h (c) 60 km/h (d) 72 km/h
8. A boat rows at 8 km/h in still water and the stream flows at 2 km/h. It goes 30 km downstream and comes back. The total time is
   (a) 6 h (b) 7 h (c) 8 h (d) 9 h
9. Sugar at Rs 40/kg is mixed with sugar at Rs 60/kg to give a mixture worth Rs 52/kg. The ratio of cheaper to dearer is
   (a) 3:2 (b) 2:3 (c) 1:2 (d) 4:5
10. The length of a rectangle is increased by 20 % and its breadth decreased by 10 %. The area
    (a) increases by 8 % (b) increases by 10 % (c) increases by 2 % (d) stays the same
11. The radius of a sphere is doubled. Its volume becomes
    (a) 2 times (b) 4 times (c) 6 times (d) 8 times
12. The diagonal of a cuboid measuring 3 cm × 4 cm × 12 cm is
    (a) 11 cm (b) 12 cm (c) 13 cm (d) 19 cm

::: note Answers and explanations — Set B
**1.** (b) — 1000 × 0.9 × 0.8 = 720. Adding the discounts (30 %) would wrongly give 700.
**2.** (d) — 1.25 × 0.8 = 1.00 of cost.
**3.** (a) — 8000 × (1.21 − 1) = 1,680. Simple interest would be 1,600.
**4.** (c) — yearly interest = 600, so P = 6600 − 2 × 600 = 5,400.
**5.** (d) — after 4 days 1 − 4/12 = 2/3 remains; B needs (2/3) × 18 = 12 days.
**6.** (b) — 1/20 − 1/30 = 1/60 per minute, so 60 min. Subtracting the times gives the wrong 10 min.
**7.** (a) — 150/10 = 15 m/s = 15 × 18/5 = 54 km/h.
**8.** (c) — 30/10 + 30/6 = 3 + 5 = 8 h.
**9.** (b) — cheaper : dearer = (60 − 52) : (52 − 40) = 8 : 12 = 2 : 3.
**10.** (a) — 1.2 × 0.9 = 1.08, an 8 % rise.
**11.** (d) — volume ∝ r³, so 2³ = 8.
**12.** (c) — √(9 + 16 + 144) = √169 = 13.
:::

**Set C — Application (10 questions)**

1. By selling an article for Rs 540 a man gains 20 %. To gain 30 % he must sell it for
   (a) Rs 560 (b) Rs 570 (c) Rs 580 (d) Rs 585
2. A sum at simple interest amounts to Rs 1,200 in 2 years and Rs 1,350 in 3 years. The rate per annum is
   (a) 16⅔ % (b) 15 % (c) 12.5 % (d) 20 %
3. A and B together can do a job in 12 days and A alone in 20 days. B alone can do it in
   (a) 24 days (b) 28 days (c) 30 days (d) 32 days
4. A train 120 m long crosses a platform 180 m long in 20 seconds. Its speed is
   (a) 45 km/h (b) 54 km/h (c) 60 km/h (d) 72 km/h
5. A man walks to a place at 4 km/h and returns at 6 km/h. The whole journey takes 5 hours. The distance is
   (a) 6 km (b) 8 km (c) 10 km (d) 12 km
6. From 40 L of milk, 4 L is drawn off and replaced with water; the process is repeated once more. The milk left is
   (a) 32.4 L (b) 32 L (c) 33.6 L (d) 36 L
7. The volume of a cylinder of radius 7 cm and height 10 cm (π = 22/7) is
   (a) 440 cm³ (b) 770 cm³ (c) 1,540 cm³ (d) 3,080 cm³
8. Two trains 100 m and 150 m long run in opposite directions at 36 km/h and 54 km/h. They cross each other in
   (a) 8 s (b) 10 s (c) 12.5 s (d) 25 s
9. A dealer uses a 900 g weight in place of 1 kg. His gain per cent is
   (a) 11⅑ % (b) 10 % (c) 9 % (d) 12 %
10. The side of a square is increased by 10 %. Its area increases by
    (a) 10 % (b) 11 % (c) 20 % (d) 21 %

::: note Answers and explanations — Set C
**1.** (d) — CP = 540 / 1.2 = 450; 450 × 1.3 = 585.
**2.** (a) — yearly interest 150, P = 1200 − 300 = 900, rate = 150/900 = 16⅔ %.
**3.** (c) — 1/12 − 1/20 = 2/60 = 1/30, so 30 days.
**4.** (b) — distance 300 m in 20 s is 15 m/s = 54 km/h; forgetting the platform gives 6 m/s.
**5.** (d) — d/4 + d/6 = 5d/12 = 5, so d = 12 km.
**6.** (a) — 40 × (1 − 4/40)² = 40 × 0.81 = 32.4 L.
**7.** (c) — (22/7) × 49 × 10 = 1,540.
**8.** (b) — relative speed 90 km/h = 25 m/s; distance 250 m; time 10 s.
**9.** (a) — gain = 100/900 × 100 = 11⅑ %; the dealer gets 1000 g's price for 900 g of goods.
**10.** (d) — 10 + 10 + 100/100 = 21 %; the common error is 20 %.
:::
