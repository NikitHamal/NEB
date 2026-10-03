---
subject: Mathematics
grade: 8
unit: 7
title: Simple Interest
hours: 0
area: Compulsory Mathematics
---

When you keep money in a bank, the bank pays you for the use of it; when you
borrow money, you pay the lender. That payment is **interest**, and the amount
borrowed or deposited is the **principal**. At this level the interest is
simple: it is a fixed percentage of the original sum for each year, so it grows
in a straight line and never earns interest on itself. This chapter works the
formula in every direction and ends with the practical arithmetic of saving and
borrowing.

::: key What this chapter asks of you
You should be able to use $I=\frac{PTR}{100}$, find the amount
$A=P+I$, and find any one of principal, rate or time when the other quantities
are known.
:::

## 7.1 The simple interest formula

$$\text{Interest}=\frac{\text{Principal}\times\text{Time}\times\text{Rate}}{100}$$

$$I=\frac{PTR}{100}$$

| Symbol | Meaning | Unit |
|---|---|---|
| $P$ | principal, the sum deposited or borrowed | rupees |
| $T$ | time | years |
| $R$ | rate of interest per year | percent per annum |
| $I$ | simple interest | rupees |
| $A$ | amount $=P+I$ | rupees |

Note that $R$ is a **yearly** rate, so the time must be in years. Six months is
$T=\frac12$ year, and eight months is $T=\frac{8}{12}=\frac23$ year.

::: caution The rate is per year, and the time must be in years
If $T$ is left in months, the answer will be wrong by a factor of 12. Convert
first, then substitute: 9 months is $T=0.75$ years, 15 months is $T=1.25$ years.
:::

```figure caption="Simple interest grows in a straight line because it is always calculated on the original principal; the total amount is the principal plus that straight line."
import numpy as np
fig, ax = plt.subplots(figsize=(4.9, 2.5))
t = np.array([0, 1, 2, 3, 4, 5])
principal = 5000
interest = principal * 0.10 * t
ax.plot(t, interest, "-o", color=ACCENT, lw=1.6, ms=4, label="interest")
ax.plot(t, principal + interest, "-s", color=SERIES[1], lw=1.6, ms=4,
        label="amount")
ax.set_xlabel("time (years)", fontsize=8)
ax.set_ylabel("rupees", fontsize=8)
ax.set_xticks(t)
ax.tick_params(labelsize=7.5, length=0)
ax.legend(fontsize=7.5, frameon=False, loc="upper left")
ax.spines[["top", "right"]].set_visible(False)
ax.yaxis.grid(True, color=GRID, lw=0.5)
ax.set_axisbelow(True)
fig.tight_layout()
```

::: example Finding the interest and the amount
**Problem.** Find the simple interest and the amount on Rs 5,000 for 3 years at
10 % per annum.

**Solution.** $P=5000$, $T=3$, $R=10$.

$$I=\frac{PTR}{100}=\frac{5000\times3\times10}{100}=\text{Rs }1500$$

$$A=P+I=5000+1500=\text{Rs }6500$$

**Answer.** Interest Rs 1,500; amount Rs 6,500.

**Check.** 10 % of 5000 is 500 a year, and 3 years gives
$3\times500=1500$ ✓ — simple interest is the same every year.
:::

::: example A time in months
**Problem.** Find the simple interest on Rs 8,400 for 9 months at 8 % per annum.

**Solution.** Convert the time: $T=\frac{9}{12}=0.75$ years.

$$I=\frac{8400\times0.75\times8}{100}=\text{Rs }504$$

**Answer.** Rs 504.

**Check.** One year's interest would be $0.08\times8400=\text{Rs }672$;
nine months is $\frac34$ of a year, so $672\times0.75=504$ ✓.
:::

## 7.2 Finding principal, rate or time

The same formula is rearranged. Write it in the triangle form and cover the
quantity you want:

$$P=\frac{100I}{TR},\qquad R=\frac{100I}{PT},\qquad T=\frac{100I}{PR}$$

::: example Finding the rate
**Problem.** A sum of Rs 6,000 earns Rs 1,080 as simple interest in 3 years.
Find the rate percent per annum.

**Solution.**

$$R=\frac{100I}{PT}=\frac{100\times1080}{6000\times3}=\frac{108000}{18000}=6\%$$

**Answer.** 6 % per annum.

**Check.** 6 % of 6000 is 360 a year, and $3\times360=1080$ ✓.
:::

::: example Finding the principal
**Problem.** What sum will earn Rs 900 as simple interest in 2 years at
7.5 % per annum?

**Solution.**

$$P=\frac{100I}{TR}=\frac{100\times900}{2\times7.5}=\frac{90\,000}{15}
=\text{Rs }6000$$

**Answer.** Rs 6,000.

**Check.** 7.5 % of 6000 is 450 a year, and two years give 900 ✓.
:::

::: example Finding the time
**Problem.** In how many years will Rs 12,000 earn Rs 2,160 as simple interest
at 9 % per annum?

**Solution.**

$$T=\frac{100I}{PR}=\frac{100\times2160}{12\,000\times9}
=\frac{216\,000}{108\,000}=2\text{ years}$$

**Answer.** 2 years.

**Check.** 9 % of 12,000 is 1,080 a year, and $2\times1080=2160$ ✓.
:::

::: example Working from the amount
**Problem.** A sum becomes Rs 7,200 in 4 years at 5 % simple interest per
annum. Find the principal.

**Solution.** The amount is $A=P+I$, and
$I=\frac{PTR}{100}=\frac{P\times4\times5}{100}=0.2P$. So

$$A=P+0.2P=1.2P\;\Longrightarrow\;P=\frac{7200}{1.2}=\text{Rs }6000$$

**Answer.** Rs 6,000.

**Check.** $I=0.2\times6000=\text{Rs }1200$, and $6000+1200=7200$ ✓.
:::

::: tip The "amount is 1.2 P" shortcut
When the amount is given rather than the interest, express $A$ as a multiple of
$P$:
$A=P\left(1+\frac{TR}{100}\right)$. For $T=4$ and $R=5$, the factor is
$1+\frac{20}{100}=1.2$, so $P=\frac{A}{1.2}$. This saves a step and avoids
solving two equations.
:::

## 7.3 Simple interest in daily life

- **Saving.** Rs 20,000 in a fixed deposit at 9 % for 2 years earns
  $\frac{20000\times2\times9}{100}=\text{Rs }3600$. A cooperative at 11 % would
  earn Rs 4,400, i.e. Rs 800 more — this is the whole reason people compare
  rates.
- **Borrowing.** A loan of Rs 50,000 at 12 % for 18 months costs
  $\frac{50\,000\times1.5\times12}{100}=\text{Rs }9000$ in interest, so the
  borrower repays Rs 59,000 in total. Borrowing for longer at the same rate
  costs proportionally more.
- **Comparing offers.** The offer with the smaller *rate × time* is cheaper,
  even if its rate is higher. Rs 50,000 for 1 year at 15 % costs Rs 7,500;
  for 2 years at 12 % it costs Rs 12,000.

::: caution Simple interest is not what a bank really charges on a loan
Most real loans charge compound interest, or a flat rate on the whole sum while
the balance falls, which is much more expensive than simple interest suggests.
The simple interest formula is the correct tool for the questions in this book
and for a rough comparison; for an actual loan, read the repayment schedule.
:::

## Chapter summary

- $I=\frac{PTR}{100}$ and $A=P+I$, with $T$ always in years.
- Rearranged: $P=\frac{100I}{TR}$, $R=\frac{100I}{PT}$, $T=\frac{100I}{PR}$.
- When the amount is given, use
  $A=P\left(1+\frac{TR}{100}\right)$ and solve for $P$.
- Simple interest is the same every year, so it grows in a straight line.
- Comparing two offers means comparing $P\times T\times R$, not the rate alone.

## Practice questions

**Group A — Objective (1 mark each)**

1. The simple interest on Rs 4,000 at 5 % for 2 years is
   <span class="marks">[1]</span>
   (a) Rs 200 (b) Rs 400 (c) Rs 800 (d) Rs 1,000
2. If $P=$ Rs 5,000, $T=2$ years and $I=$ Rs 800, the rate is
   <span class="marks">[1]</span>
   (a) 6% (b) 7% (c) 8% (d) 10%
3. The amount on Rs 2,500 at 8 % for 3 years is
   <span class="marks">[1]</span>
   (a) Rs 2,600 (b) Rs 3,100 (c) Rs 3,500 (d) Rs 600
4. 18 months expressed in years is <span class="marks">[1]</span>
   (a) 1.8 (b) 1.5 (c) 18 (d) 0.18
5. The simple interest on Rs 10,000 at 12 % for 5 years is
   <span class="marks">[1]</span>
   (a) Rs 1,200 (b) Rs 3,600 (c) Rs 6,000 (d) Rs 12,000
6. If the interest is Rs 900, $P=$ Rs 3,000 and $R=10\%$, then $T$ is
   <span class="marks">[1]</span>
   (a) 2 years (b) 3 years (c) 4 years (d) 5 years

::: note Answers to Group A
**1.** (b) — $\frac{4000\times2\times5}{100}=400$.
**2.** (c) — $R=\frac{100\times800}{5000\times2}=8\%$.
**3.** (b) — $I=600$, so $A=2500+600=3100$.
**4.** (b) — $\frac{18}{12}=1.5$.
**5.** (c) — $5\times1200=6000$.
**6.** (b) — $T=\frac{100\times900}{3000\times10}=3$ years.
:::

**Group B — Short answer (2 marks each)**

1. Find the simple interest on Rs 7,500 for 2 years at 6 % per annum.
   <span class="marks">[2]</span>
2. Find the principal that earns Rs 1,260 in 3 years at 7 % per annum.
   <span class="marks">[2]</span>
3. Find the rate at which Rs 9,000 earns Rs 1,620 in 2 years.
   <span class="marks">[2]</span>
4. In how many years will Rs 15,000 earn Rs 4,500 at 10 % per annum?
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $I=\frac{7500\times2\times6}{100}=\text{Rs }900$.
**2.** $P=\frac{100\times1260}{3\times7}=\text{Rs }6000$.
**3.** $R=\frac{100\times1620}{9000\times2}=9\%$.
**4.** $T=\frac{100\times4500}{15\,000\times10}=3$ years.
:::

**Group C — Long answer (4 marks each)**

1. Rs 12,000 is deposited at 8 % per annum for 2 years in bank A, and the same
   sum at 9 % per annum for 18 months in bank B. Which deposit earns more
   interest, and by how much? <span class="marks">[4]</span>
2. A sum of money becomes Rs 7,800 in 3 years at 10 % simple interest per
   annum. Find the principal and the interest earned. If the same sum is then
   invested at 8 % per annum for 2 years 6 months, what amount will it become?
   <span class="marks">[4]</span>
::: note Answers to Group C
**1.** **Bank A.** $I=\frac{12\,000\times2\times8}{100}=\text{Rs }1920$.
**Bank B.** $T=1.5$ years, so
$I=\frac{12\,000\times1.5\times9}{100}=\text{Rs }1620$.
Bank A earns more, by $1920-1620=\text{Rs }300$.
**Check.** $P\times T\times R$: A gives $12\,000\times2\times8=192\,000$ and B
gives $12\,000\times1.5\times9=162\,000$; A is bigger ✓.
**2.** **Principal.** $I=\frac{P\times3\times10}{100}=0.3P$, and
$A=P+I=P+0.3P=1.3P$. So
$P=\frac{7800}{1.3}=\text{Rs }6000$, and the interest earned is
$7800-6000=\text{Rs }1800$.
**Second part.** $T=2.5$ years, so
$I=\frac{6000\times2.5\times8}{100}=\text{Rs }1200$, and the amount is
$6000+1200=\text{Rs }7200$.
**Check.** 10 % of 6000 is 600 a year, and three years give $3\times600=1800$,
so the amount is $6000+1800=7800$ ✓. For the second part, 8 % of 6000 is 480 a
year, and 2.5 years give $2.5\times480=1200$ ✓. Note that the same principal
earns less here, because both the rate and the time are lower.
:::
