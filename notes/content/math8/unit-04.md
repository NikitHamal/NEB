---
subject: Mathematics
grade: 8
unit: 4
title: Ratio and Proportion
hours: 0
area: Compulsory Mathematics
---

A ratio compares two quantities of the same kind; a proportion says that two
ratios are equal. These two ideas are behind almost every practical
calculation — sharing a profit, mixing mortar, reading a map, or working out how
much rice a family of six needs for a month. This chapter works through the
definitions, then the two kinds of variation that make the difference between
a sum that takes one line and a sum that is done backwards.

::: key What this chapter asks of you
You should be able to write a ratio in its lowest terms, divide a quantity in a
given ratio, test whether four numbers are in proportion, find the fourth
proportional and the mean proportional, and solve direct and inverse variation
problems.
:::

## 4.1 Ratio

A **ratio** compares two quantities of the same kind by division. The ratio of
$a$ to $b$ is written $a:b$ and read "a is to b", where

$$a:b=\frac ab\qquad(b\ne0)$$

The two quantities must be in the **same unit**. A ratio has no unit, because it
is one quantity divided by another of the same kind.

| Statement | Ratio |
|---|---|
| 15 kg to 25 kg | $15:25=3:5$ |
| 500 m to 2 km | $500:2000=1:4$ (convert to the same unit first) |
| 45 minutes to 2 hours | $45:120=3:8$ |

**Simplification.** Divide every term by their highest common factor. A ratio is
usually written with whole numbers and in its lowest terms.

::: caution Convert the units before you compare
A ratio of 500 m to 2 km must be written $500:2000$, not $500:2$. Comparing a
number of metres with a number of kilometres is comparing two different things
and gives a meaningless ratio — the commonest single error in this chapter.
:::

### 4.1.1 Dividing a quantity in a given ratio

Add the terms of the ratio to find the number of equal parts, then give each
share as its term out of that total.

::: example Sharing a profit
**Problem.** Two partners invest Rs 60,000 and Rs 90,000 and make a profit of
Rs 45,000, shared in the ratio of their investments. Find each partner's share.

**Solution.** The ratio of investments is

$$60\,000:90\,000=2:3$$

The total number of parts is $2+3=5$. Each part is worth

$$\frac{45\,000}{5}=\text{Rs }9000$$

The shares are $2\times9000=\text{Rs }18\,000$ and
$3\times9000=\text{Rs }27\,000$.

**Check.** $18\,000+27\,000=45\,000$ ✓, and
$18\,000:27\,000=2:3$ ✓.
:::

::: example Dividing with three terms
**Problem.** A sum of Rs 2,400 is to be divided among three people in the ratio
$3:4:5$. Find each share.

**Solution.** Total parts $=3+4+5=12$, so one part is
$2400\div12=\text{Rs }200$.

$$3\times200=\text{Rs }600,\quad 4\times200=\text{Rs }800,\quad
5\times200=\text{Rs }1000$$

**Check.** $600+800+1000=2400$ ✓.
:::

## 4.2 Proportion

Four quantities $a$, $b$, $c$, $d$ are **in proportion** if

$$a:b=c:d,\qquad\text{that is}\qquad \frac ab=\frac cd$$

In the statement $a:b=c:d$, the outer terms $a$ and $d$ are the **extremes** and
the inner terms $b$ and $c$ are the **means**. The fundamental property of a
proportion is

$$\text{product of extremes}=\text{product of means},\qquad ad=bc$$

Three quantities $a$, $b$, $c$ are in **continued proportion** if
$a:b=b:c$, so that $b^2=ac$. Then $b$ is the **mean proportional** between $a$
and $c$, and

$$b=\sqrt{ac}$$

::: example Finding the fourth proportional
**Problem.** Find $x$ if $6:9=10:x$.

**Solution.** By the property of proportion, the product of the extremes equals
the product of the means:

$$6\times x=9\times10\;\Longrightarrow\;6x=90\;\Longrightarrow\;x=15$$

**Answer.** $x=15$.

**Check.** $6:9=2:3$ and $10:15=2:3$ ✓. The two ratios are equal.
:::

::: example The mean proportional
**Problem.** Find the mean proportional between 4 and 25.

**Solution.** If $b$ is the mean proportional, then $b^2=4\times25=100$, so
$b=10$ (taking the positive root, since lengths are positive).

**Answer.** 10.

**Check.** $4:10=2:5$ and $10:25=2:5$ ✓, so 4, 10 and 25 are in continued
proportion.
:::

::: example Using the product property to solve
**Problem.** If $\frac{x}{5}=\frac{12}{20}$, find $x$.

**Solution.** Cross-multiplying: $20x=5\times12=60$, so $x=3$.

**Answer.** $x=3$.

**Check.** $\frac{3}{5}=0.6$ and $\frac{12}{20}=0.6$ ✓. Notice that
$12:20=3:5$ — the second ratio was already the first in disguise.
:::

## 4.3 Direct and inverse variation

Two quantities are in **direct variation** when they increase or decrease
together in the same ratio, written $x\propto y$ and $x=ky$.

| Direct variation | Inverse variation |
|---|---|
| $x\propto y$, so $x=ky$ | $x\propto\frac1y$, so $x=\frac{k}{y}$ |
| $\frac{x_1}{y_1}=\frac{x_2}{y_2}$ | $x_1y_1=x_2y_2$ |
| more goods, more money | more workers, less time |
| more days, more wages | faster speed, less time |
| more rice, more people fed | more taps, less time to fill a tank |
| constant is the unit rate | constant is the total work |

The constant $k$ is found from the pair of values given in the problem; once it
is known, the second pair can be calculated.

```figure caption="The two kinds of variation. Direct variation is a straight line through the origin; inverse variation is a curve that falls away — doubling the one halves the other."
import numpy as np
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.5))
x = np.linspace(0.2, 5, 200)
ax1.plot(x, 2 * x, color=ACCENT, lw=1.6)
ax1.set_title("direct: $x=2y$", fontsize=8.5, color=INK)
ax1.set_xlabel("y", fontsize=8)
ax1.set_ylabel("x", fontsize=8)
ax2.plot(x, 6 / x, color=SERIES[1], lw=1.6)
ax2.set_title("inverse: $xy=6$", fontsize=8.5, color=INK)
ax2.set_xlabel("y", fontsize=8)
ax2.set_ylabel("x", fontsize=8)
for ax in (ax1, ax2):
    ax.tick_params(labelsize=7.5, length=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(True, color=GRID, lw=0.5)
    ax.set_axisbelow(True)
fig.tight_layout()
```

::: example Direct variation
**Problem.** If 5 kg of rice costs Rs 400, what will 8 kg cost?

**Solution.** More rice costs more money, so this is direct variation.
Find the cost of 1 kg first:

$$k=\frac{400}{5}=\text{Rs }80\text{ per kg}$$

Then $8\times80=\text{Rs }640$.

**Answer.** Rs 640.

**Check.** $400:640=5:8$ ✓, which is the ratio of the quantities. The unit rate
is the constant of variation.
:::

::: example Inverse variation
**Problem.** Six workers can build a wall in 12 days. How long will 9 workers
take, working at the same rate?

**Solution.** More workers means less time, so this is inverse variation, and
the total work is constant:

$$\text{total work}=6\times12=72\text{ worker-days}$$

With 9 workers, the time is

$$\frac{72}{9}=8\text{ days}$$

**Answer.** 8 days.

**Check.** $6\times12=9\times8=72$ ✓. Note the answer is *less* than 12, which
is what "more workers" must give — a quick way to catch a reversed calculation.
:::

::: caution Choosing the wrong kind of variation
Ask the question in words: **if one quantity gets bigger, does the other get
bigger or smaller?** Bigger–bigger means direct, bigger–smaller means inverse.
Almost every lost mark in this chapter comes from setting up a direct variation
when the quantities move in opposite directions.
:::

## 4.4 Map scale and similar figures

A map scale is a ratio of a length on the map to the real length, with both in
the same unit. A scale of $1:50\,000$ means 1 cm on the map represents
50 000 cm, that is 500 m or 0.5 km, on the ground.

::: example A map distance
**Problem.** On a map with scale $1:25\,000$, two towns are 6 cm apart. Find
the real distance in kilometres.

**Solution.** The real distance is $6\times25\,000=150\,000$ cm.

$$150\,000\text{ cm}=1500\text{ m}=1.5\text{ km}$$

**Answer.** 1.5 km.

**Check.** At this scale, 1 cm represents $25\,000$ cm $=0.25$ km, so 6 cm is
$6\times0.25=1.5$ km ✓.
:::

## 4.5 Sharing in a given ratio

```figure caption="Rs 1,800 shared in the ratio 2 : 3 : 4. The total is divided into 2 + 3 + 4 = 9 equal parts of Rs 200 each."
labels = ["A  2 parts", "B  3 parts", "C  4 parts"]
vals = [400, 600, 800]
fig, ax = plt.subplots(figsize=(4.4, 3.0))
ax.pie(vals, labels=labels, colors=[SERIES[0], SERIES[1], SERIES[2]],
       autopct=lambda p: f"Rs {int(round(p * 18)):,}", startangle=90,
       textprops=dict(color=INK, fontsize=8.6),
       wedgeprops=dict(edgecolor="white", linewidth=1.5))
ax.set_aspect("equal")
```

| Task | Method |
|---|---|
| Simplify a ratio | divide both terms by their HCF; make units the same first |
| Share $x$ in $m:n$ | shares are $\frac{m}{m+n}x$ and $\frac{n}{m+n}x$ |
| Compound ratio of $a:b$ and $c:d$ | $ac : bd$ |
| Mean proportional between $a$ and $b$ | $\sqrt{ab}$ |
| Check a proportion $a:b = c:d$ | $ad = bc$ (product of extremes = product of means) |

::: example Sharing with a condition
**Question.** Rs 4,500 is shared among A, B and C so that A : B $= 2 : 3$ and
B : C $= 4 : 5$. Find each share.

**Answer.** Make B common. A : B $= 2:3 = 8:12$; B : C $= 4:5 = 12:15$.
So A : B : C $= 8 : 12 : 15$, giving $8 + 12 + 15 = 35$ parts.
One part $= \frac{4500}{35} = 128.57$ (to 2 d.p.), so it is cleaner to compute
each share directly:
A $= \frac{8}{35}\times4500 = \textbf{Rs 1,028.57}$,
B $= \frac{12}{35}\times4500 = \textbf{Rs 1,542.86}$,
C $= \frac{15}{35}\times4500 = \textbf{Rs 1,928.57}$.
**Check:** the three add to Rs 4,500.
:::

::: note Activity — the ratio in a recipe
Take a simple recipe (say, rice and water in the ratio $1 : 2$, or tea with
milk, water and sugar). Write the ratio, then scale it for 4 people and for 15
people. Cook or prepare it if you can, and compare with the recipe for one.
**Discussion:** Which ingredients scale in direct proportion and which do not
(spices, cooking time)?
:::

## Chapter summary

- A ratio compares two quantities of the same kind and has no unit; write both
  in the same unit and simplify by the HCF.
- To divide a quantity in the ratio $a:b:c$, add the terms, find one part, then
  multiply.
- Four quantities are in proportion if $a:b=c:d$, which holds exactly when
  $ad=bc$.
- Three quantities are in continued proportion if $a:b=b:c$, and then the mean
  proportional is $b=\sqrt{ac}$.
- **Direct variation:** $x\propto y$, $x=ky$,
  $\frac{x_1}{y_1}=\frac{x_2}{y_2}$; both quantities rise together.
- **Inverse variation:** $x\propto\frac1y$, $xy=k$, $x_1y_1=x_2y_2$; one rises
  as the other falls.
- A map scale is a ratio, so both lengths must be converted to the same unit
  before multiplying.

## Practice questions

**Group A — Objective (1 mark each)**

1. The ratio 250 g to 1 kg in its lowest terms is
   <span class="marks">[1]</span>
   (a) $250:1$ (b) $1:4$ (c) $4:1$ (d) $1:250$
2. If $a:b=c:d$, then <span class="marks">[1]</span>
   (a) $ab=cd$ (b) $ad=bc$ (c) $ac=bd$ (d) $a+b=c+d$
3. The mean proportional between 9 and 16 is <span class="marks">[1]</span>
   (a) 12 (b) 25 (c) 144 (d) 7
4. More workers, less time is an example of
   <span class="marks">[1]</span>
   (a) direct variation (b) inverse variation (c) proportion
   (d) continued proportion
5. If 3 pens cost Rs 45, then 7 pens cost <span class="marks">[1]</span>
   (a) Rs 90 (b) Rs 105 (c) Rs 135 (d) Rs 63
6. On a map of scale $1:100\,000$, 3 cm represents
   <span class="marks">[1]</span>
   (a) 3 km (b) 30 km (c) 0.3 km (d) 300 km

::: note Answers to Group A
**1.** (b) — $250:1000=1:4$.
**2.** (b) — the product of the extremes equals the product of the means.
**3.** (a) — $\sqrt{9\times16}=12$.
**4.** (b) — one quantity rises as the other falls.
**5.** (b) — one pen is Rs 15, so seven cost Rs 105.
**6.** (a) — $3\times100\,000=300\,000$ cm $=3$ km.
:::

**Group B — Short answer (2 marks each)**

1. Express the ratio $45\text{ min}:2\text{ hr}$ in its lowest terms.
   <span class="marks">[2]</span>
2. Find $x$ if $x:8=9:12$. <span class="marks">[2]</span>
3. Divide Rs 5,400 in the ratio $2:3:4$. <span class="marks">[2]</span>
4. If 8 men can do a job in 15 days, how long will 12 men take?
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $45:120=3:8$.
**2.** $12x=72$, so $x=6$.
**3.** Total parts $=9$, one part $=600$; shares Rs 1200, Rs 1800 and Rs 2400.
**4.** Total work $=8\times15=120$ man-days; with 12 men the time is
$120\div12=10$ days.
:::

**Group C — Long answer (4 marks each)**

1. A sum of money is divided between two brothers in the ratio $5:7$. If the
   elder brother receives Rs 8,400, find the total sum and the younger
   brother's share. <span class="marks">[4]</span>
2. A truck covers a certain distance in 6 hours at 40 km/h. How long will it
   take at 60 km/h? State what kind of variation this is, find the constant, and
   verify the answer. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** The elder brother's share is the 7-part share:
$7\text{ parts}=\text{Rs }8400$, so 1 part $=8400\div7=\text{Rs }1200$.
The younger brother gets $5\times1200=\text{Rs }6000$, and the total is
$6000+8400=\text{Rs }14\,400$. **Check.** $6000:8400=5:7$ ✓ and
$6000+8400=14\,400$ ✓.
**2.** **Kind.** Faster speed means less time, so this is **inverse variation**
($\text{speed}\times\text{time}=$ constant distance). **Constant.** The distance
is $40\times6=240$ km. **Time at 60 km/h.** $240\div60=4$ hours.
**Verify.** $40\times6=240$ and $60\times4=240$ ✓ — the product is the same, as
inverse variation requires, and the time fell from 6 hours to 4 as the speed
rose.
:::

**Extra practice**

**Group B (2 marks)**

**11.** Simplify the ratio 1 hour 20 minutes : 2 hours.
**12.** Find the mean proportional between 8 and 18.

**Group C (4 marks)**

**13.** Divide Rs 7,560 among three workers in the ratio of the days they worked:
    6 days, 7 days and 8 days.

::: note Extra practice — answers
**11.** $80 : 120 = 2 : 3$.
**12.** $\sqrt{8 \times 18} = \sqrt{144} = 12$.
**13.** Parts $= 6 + 7 + 8 = 21$; one part $= \frac{7560}{21} = 360$.
Shares: $6 \times 360 = $ **Rs 2,160**, $7 \times 360 = $ **Rs 2,520**,
$8 \times 360 = $ **Rs 2,880**. Check: they total Rs 7,560.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** If $4:7=x:35$, then $x$ is
   (a) 15 (b) 20 (c) 25 (d) 28
**2.** The mean proportional between 9 and 16 is
   (a) 12 (b) 12.5 (c) 25 (d) 144
**3.** Rs 960 shared in the ratio $5:7$ gives the larger share
   (a) Rs 400 (b) Rs 480 (c) Rs 560 (d) Rs 600
**4.** The compound ratio of $3:4$ and $2:5$ is
   (a) $6:20$ (b) $3:10$ (c) $5:9$ (d) $6:9$
**5.** 40 minutes : 2 hours in simplest form is
   (a) $40:2$ (b) $1:3$ (c) $2:5$ (d) $1:5$

::: note Objective practice — answers
**1.** (b) — $x=\frac{4\times35}{7}=20$. **2.** (a) — $\sqrt{144}=12$. **3.** (c) — $\frac{7}{12}\times960=560$. **4.** (b) — $\frac{6}{20}=3:10$. **5.** (b) — $40:120=1:3$.
:::
