---
subject: Mathematics
grade: 10
unit: 3
title: Compound Interest
hours: 0
area: Compulsory Mathematics
---

When you keep money in a bank for several years, the bank does not simply pay the same interest every year. At the end of each year it adds the interest to your deposit, and next year's interest is calculated on this bigger amount. Interest earned on interest is called **compound interest**, and it is the reason savings in a cooperative or a fixed deposit grow faster and faster, and the reason a loan left unpaid becomes frighteningly large. In this chapter you will learn the formula for compound interest, apply it to yearly, half-yearly and quarterly compounding, and work backwards to find the principal, the rate or the time.

::: key What the SEE asks from this chapter
The SEE usually carries one 4-mark question on compound interest. The usual forms are: (i) find the amount or compound interest for 2 or 3 years; (ii) **half-yearly** compounding; (iii) find the principal, rate or time; (iv) the **difference between compound and simple interest** for 2 years; (v) a loan or deposit where the rate changes each year. Always write the formula first, substitute carefully, and finish with the unit (Rs).
:::

## 3.1 Compound Interest: concepts, formulas and worked problems

### Simple interest revised

Recall the terms: **principal** $P$ is the money deposited or borrowed; **rate** $R$ is the interest per Rs 100 per year (written $R\%$ p.a.); **time** $T$ is in years; **interest** is the earning on the principal; **amount** $A=P+I$.

::: key Simple interest
$$ I = \frac{P\times T\times R}{100}, \qquad A = P + I $$
:::

In simple interest the interest is always calculated on the **original** principal. The interest for every year is the same.

### What is compound interest?

::: definition Compound interest
In **compound interest** the interest earned at the end of each period (a year, half-year or quarter) is **added to the principal**. The new, larger sum becomes the principal for the next period. The **compound interest** is the total interest earned over all periods:

$$ \text{Compound interest} = \text{Compound amount} - \text{Original principal} $$
:::

::: example Year-by-year calculation
**Problem.** Find the compound interest on Rs 15,000 for 2 years at 8% p.a., compounded yearly.

**Solution.** Year 1:

Principal $=\text{Rs } 15{,}000$. Interest $=\dfrac{15000\times 8}{100}=\text{Rs } 1{,}200$. Amount $=16{,}200$.

Year 2: the principal is now Rs 16,200.

Interest $=\dfrac{16200\times 8}{100}=\text{Rs } 1{,}296$. Amount $=16200+1296=\text{Rs } 17{,}496$.

Compound interest $=17496-15000=\text{Rs } 2{,}496$.

Simple interest for the same time would be $\dfrac{15000\times 2\times 8}{100}=\text{Rs } 2{,}400$. Compound interest is more by Rs 96 because the second year's interest (Rs 1,296) is larger than the first (Rs 1,200).
:::

### The compound amount formula

Doing the year-by-year method for 5 or 10 years is slow. We derive a formula.

::: derivation Compound amount formula $A = P\left(1+\frac{R}{100}\right)^T$
We start from the idea that after each year the amount is multiplied by the same factor, and we get to a single formula for any number of years.

**Setting up.** Principal $=P$, rate $=R\%$ p.a. compounded yearly, time $=T$ years. Write $r=\dfrac{R}{100}$, so interest on Rs 1 for one year is $r$.

**Step 1 — amount after 1 year.** Interest $=Pr$, so

$$ A_1 = P + Pr = P(1+r) $$

**Step 2 — amount after 2 years.** The principal for year 2 is $A_1$. Interest for year 2 $=A_1 r$, so

$$ A_2 = A_1 + A_1 r = A_1(1+r) = P(1+r)^2 $$

**Step 3 — amount after 3 years.** The principal for year 3 is $A_2$, so

$$ A_3 = A_2(1+r) = P(1+r)^3 $$

**Step 4 — the pattern.** Each year multiplies the amount by $(1+r)$. After $T$ years, we multiply $T$ times:

$$ A = P(1+r)^T = P\left(1+\frac{R}{100}\right)^T $$

**Result.**

$$ A = P\left(1+\frac{R}{100}\right)^T, \qquad CI = A - P $$

**What it means.** The factor $\left(1+\frac{R}{100}\right)$ is the "growth per year". At 10% it is 1.10, so money is multiplied by 1.10 every year. This is *exponential growth*, which is why the graph curves upwards.
:::

::: key Compound interest formulas (compounded yearly)
$$ A = P\left(1+\frac{R}{100}\right)^T $$
$$ CI = A - P = P\left[\left(1+\frac{R}{100}\right)^T - 1\right] $$

Find $P$: $P = \dfrac{A}{\left(1+\frac{R}{100}\right)^T}$.
:::

::: example Amount and compound interest for 3 years
**Problem.** Find the amount and the compound interest on Rs 20,000 for 3 years at 10% p.a. compounded yearly. Also find the simple interest and the difference.

**Solution.** $P=20000$, $R=10$, $T=3$.

$$ A = 20000\left(1+\frac{10}{100}\right)^3 = 20000\times(1.1)^3 = 20000\times 1.331 = \text{Rs } 26{,}620 $$

Compound interest $=26620-20000=\text{Rs } 6{,}620$.

Simple interest $=\dfrac{20000\times 3\times 10}{100}=\text{Rs } 6{,}000$.

Difference $=6620-6000=\text{Rs } 620$.
:::

```figure caption="Growth of Rs 20,000 at 10% p.a. Simple interest rises in a straight line; compound interest curves upward and the gap widens every year."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.7, 2.9))
t = np.arange(0, 11)
si = 20000 + 2000*t
ci = 20000*1.1**t
ax.plot(t, si/1000, color=SERIES[2], lw=2, marker='o', ms=3)
ax.plot(t, ci/1000, color=ACCENT, lw=2, marker='o', ms=3)
ax.text(10.15, si[-1]/1000, 'simple\n40,000', fontsize=8, color=SERIES[2], va='center')
ax.text(10.15, ci[-1]/1000, 'compound\n51,875', fontsize=8, color=ACCENT, va='center')
ax.set_xlim(0, 12.6); ax.set_ylim(15, 56)
ax.set_xlabel('time (years)', fontsize=8.5)
ax.set_ylabel('amount (Rs thousand)', fontsize=8.5)
ax.spines[['top','right']].set_visible(False)
ax.grid(color=GRID, lw=0.5); ax.set_axisbelow(True)
```

::: caution Common mistakes
- Using $A=P(1+\frac{R}{100}\times T)$. That is **simple** interest amount. In compound interest, $T$ is an **exponent**.
- Forgetting to subtract $P$. The formula gives the **amount**, not the interest. Compound interest $=A-P$.
- Calculating $(1.1)^3$ as $1.1\times 3$. Multiply $1.1\times1.1\times1.1=1.331$.
- Writing the final answer without "Rs".
:::

### Half-yearly and quarterly compounding

Sometimes the bank adds the interest more than once a year. If interest is added every 6 months it is compounded **half-yearly** (2 times a year); every 3 months, **quarterly** (4 times a year).

The idea: the rate per period is the yearly rate divided by the number of periods per year, and the number of periods is the number of years times the periods per year.

::: key Compounding more than once a year
| Compounded | Periods per year | Rate per period | Number of periods |
|---|---|---|---|
| Yearly | 1 | $R$ | $T$ |
| Half-yearly | 2 | $\dfrac{R}{2}$ | $2T$ |
| Quarterly | 4 | $\dfrac{R}{4}$ | $4T$ |

$$ A = P\left(1+\frac{R}{200}\right)^{2T}\ \text{(half-yearly)}, \qquad A = P\left(1+\frac{R}{400}\right)^{4T}\ \text{(quarterly)} $$
:::

::: example Half-yearly compounding
**Problem.** Find the amount and compound interest on Rs 20,000 for $1\frac12$ years at 10% p.a. compounded half-yearly.

**Solution.** $P=20000$, $R=10$, $T=1.5$ years. Half-yearly compounding: rate per half-year $=\dfrac{10}{2}=5\%$, number of half-years $=2\times 1.5=3$.

$$ A = 20000\left(1+\frac{5}{100}\right)^3 = 20000\times(1.05)^3 = 20000\times 1.157625 = \text{Rs } 23{,}152.50 $$

Compound interest $=23152.50-20000=\text{Rs } 3{,}152.50$.
:::

::: example Quarterly compounding
**Problem.** Find the compound interest on Rs 10,000 for 1 year at 8% p.a. compounded quarterly.

**Solution.** Rate per quarter $=\dfrac{8}{4}=2\%$; number of quarters $=4\times 1=4$.

$$ A = 10000\times(1.02)^4 = 10000\times 1.08243216 = \text{Rs } 10{,}824.32 $$

Compound interest $=10824.32-10000=\text{Rs } 824.32$.
:::

::: example Yearly versus half-yearly
**Problem.** Rs 10,000 is deposited for 1 year at 20% p.a. Find the amount if interest is compounded (a) yearly, (b) half-yearly. Find the difference.

**Solution.** (a) Yearly: $A=10000\times 1.2=\text{Rs } 12{,}000$.

(b) Half-yearly: rate per period $=10\%$, periods $=2$: $A=10000\times(1.1)^2=10000\times 1.21=\text{Rs } 12{,}100$.

Difference $=12100-12000=\text{Rs } 100$.

The more often the interest is added, the larger the amount.
:::

```figure caption="One year, Rs 10,000 at 12% p.a. The more often interest is compounded, the larger the amount (the bars start at Rs 10,000)."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 2.7))
names = ['Yearly', 'Half-yearly', 'Quarterly', 'Monthly']
vals = [10000*1.12, 10000*1.06**2, 10000*1.03**4, 10000*1.01**12]
for i, v in enumerate(vals):
    ax.bar(i, v - 10000, bottom=10000, color=SERIES[i], width=0.55)
    ax.text(i, v + 15, 'Rs %.2f' % v, ha='center', va='bottom', fontsize=8)
ax.set_xticks(range(4)); ax.set_xticklabels(names, fontsize=8.5)
ax.set_ylim(10000, 11400)
ax.set_ylabel('amount (Rs)', fontsize=8.5)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='y', color=GRID, lw=0.5); ax.set_axisbelow(True)
```

### Finding the principal, the rate or the time

Use the amount formula as an equation with one unknown.

::: example Finding the principal
**Problem.** A sum of money amounts to Rs 17,640 in 2 years at 5% p.a. compound interest. Find the sum.

**Solution.** $A=P(1.05)^2$, so $17640=P\times 1.1025$.

$$ P = \frac{17640}{1.1025} = \text{Rs } 16{,}000 $$

Check: $16000\times 1.1025=17640$ ✓.
:::

::: example Finding the rate
**Problem.** At what rate of compound interest per annum will Rs 10,000 become Rs 12,100 in 2 years?

**Solution.** $12100=10000\left(1+\dfrac{R}{100}\right)^2$.

$$ \left(1+\frac{R}{100}\right)^2 = \frac{12100}{10000}=1.21 = (1.1)^2 $$

So $1+\dfrac{R}{100}=1.1$ and $R=10$.

The rate is **10% p.a.**
:::

::: example Finding the time
**Problem.** In how many years will Rs 8,000 become Rs 10,648 at 10% p.a. compound interest?

**Solution.** $10648=8000\times(1.1)^T$, so $(1.1)^T=\dfrac{10648}{8000}=1.331$.

Since $1.1\times 1.1\times 1.1=1.331$, $T=3$ years.
:::

::: tip Finding the rate and time
For the SEE, the numbers are chosen so that $A\div P$ is a perfect power: 1.21 $=1.1^2$, 1.331 $=1.1^3$, 1.1025 $=1.05^2$, 1.44 $=1.2^2$, 1.1664 $=1.08^2$. Divide $A$ by $P$, recognise the power, read off the rate or the exponent.
:::

### Compound interest and simple interest compared

::: derivation Difference between CI and SI for 2 years
We start with the amount formula for 2 years and compare the compound interest with the simple interest for the same period, to find a shortcut.

**Setting up.** Principal $P$, rate $R\%$, time 2 years; let $r=\dfrac{R}{100}$.

**Step 1 — compound interest.**

$$ CI = P(1+r)^2 - P = P(1+2r+r^2) - P = 2Pr + Pr^2 $$

**Step 2 — simple interest.**

$$ SI = \frac{P\times 2\times R}{100} = 2Pr $$

**Step 3 — subtract.**

$$ CI - SI = (2Pr + Pr^2) - 2Pr = Pr^2 $$

**Result.**

$$ CI - SI = P\left(\frac{R}{100}\right)^2 \quad (\text{2 years}) $$

**What it means.** The difference is the **interest on the first year's interest**: first-year interest is $Pr$ and its interest in year 2 is $Pr\times r=Pr^2$.
:::

::: example Difference between CI and SI
**Problem.** Find the difference between the compound interest and simple interest on Rs 25,000 for 2 years at 4% p.a.

**Solution.**

$$ CI - SI = 25000\times\left(\frac{4}{100}\right)^2 = 25000\times 0.0016 = \text{Rs } 40 $$

Verification: $A=25000\times(1.04)^2=25000\times 1.0816=27040$, so $CI=2040$. $SI=\dfrac{25000\times 2\times 4}{100}=2000$. Difference $=2040-2000=40$ ✓.
:::

::: example Finding the principal from the difference
**Problem.** The difference between CI and SI on a sum for 2 years at 5% p.a. is Rs 90. Find the sum.

**Solution.** $P\left(\dfrac{5}{100}\right)^2=90$, so $P\times 0.0025=90$.

$$ P = \frac{90}{0.0025} = \text{Rs } 36{,}000 $$
:::

### Different rates in different years

If the rate is different each year, apply a different growth factor for each year, one after the other.

::: example Changing rates
**Problem.** Rs 40,000 is invested for 3 years. The rate of compound interest is 5% in the first year, 8% in the second year and 10% in the third year. Find the amount and the compound interest.

**Solution.**

$$ A = 40000\times 1.05\times 1.08\times 1.10 $$

After year 1: $40000\times 1.05=\text{Rs } 42{,}000$.

After year 2: $42000\times 1.08=\text{Rs } 45{,}360$.

After year 3: $45360\times 1.10=\text{Rs } 49{,}896$.

Compound interest $=49896-40000=\text{Rs } 9{,}896$.
:::

::: example Withdrawing in between
**Problem.** Mrs Rai deposits Rs 1,00,000 at 10% p.a. compounded yearly. After one year she withdraws Rs 50,000. What is the amount in her account at the end of the second year?

**Solution.** After 1 year: $100000\times 1.1=\text{Rs } 1{,}10{,}000$.

After withdrawing: $110000-50000=\text{Rs } 60{,}000$.

After the second year: $60000\times 1.1=\text{Rs } 66{,}000$.
:::

::: example Interest given, find the principal
**Problem.** The compound interest on a sum for 2 years at 10% p.a. is Rs 2,100. Find the sum.

**Solution.** $CI=P\left[(1.1)^2-1\right]=P\times 0.21$.

$$ 0.21P = 2100 \;\Rightarrow\; P = \frac{2100}{0.21} = \text{Rs } 10{,}000 $$
:::

### Real-life applications

::: example A loan left unpaid
**Problem.** A farmer borrows Rs 2,00,000 from a cooperative at 12% p.a. compound interest, compounded yearly, and pays nothing for 3 years. How much must he pay at the end of 3 years, and how much of it is interest?

**Solution.** $A=200000\times(1.12)^3=200000\times 1.404928=\text{Rs } 2{,}80{,}985.60$.

Interest $=280985.60-200000=\text{Rs } 80{,}985.60$.

Simple interest would have been $\dfrac{200000\times 3\times 12}{100}=\text{Rs } 72{,}000$. Waiting costs Rs 8,985.60 extra, which is why loans should be repaid early.
:::

::: example Which bank pays more?
**Problem.** Bank A pays 10% p.a. compounded yearly. Bank B pays 9.8% p.a. compounded half-yearly. Which bank gives more on Rs 1,00,000 in 1 year?

**Solution.** Bank A: $A=100000\times 1.10=\text{Rs } 1{,}10{,}000$.

Bank B: rate per half-year $=\dfrac{9.8}{2}=4.9\%$, so $A=100000\times(1.049)^2=100000\times 1.100401=\text{Rs } 1{,}10{,}040.10$.

Bank B gives Rs 40.10 more, because it adds interest twice a year.
:::

::: note Reading an interest rate
"10% p.a." with no other word means **compounded yearly** unless the question says half-yearly or quarterly. For a period such as $1\frac12$ years the question will say half-yearly, so that the number of periods is a whole number.
:::

## 3.2 Exercises of the SEE type

### Method for every question

1. Write what is given: $P$, $R$, $T$, whether yearly or half-yearly.
2. If compounded half-yearly, **halve the rate and double the time**; if quarterly, divide the rate by 4 and multiply the time by 4.
3. Write the formula, substitute, and calculate the power carefully, step by step.
4. Subtract $P$ if the question asks for the **interest**.
5. If the unknown is $P$, $R$ or $T$, divide $A$ by the rest and match the power.
6. Write the answer with a unit.

::: tip Marks pattern
A typical 4-mark question gives 1 mark for the correct formula, 1 mark for correct substitution, 1 mark for the calculation and 1 mark for the final answer with unit. Skipping the formula often loses a mark even when the answer is right.
:::

## Chapter summary

- Simple interest $I=\frac{PTR}{100}$; compound interest adds interest to the principal every period.
- $A=P\left(1+\frac{R}{100}\right)^T$ and $CI=A-P$ (compounded yearly).
- Half-yearly: $A=P\left(1+\frac{R}{200}\right)^{2T}$; quarterly: $A=P\left(1+\frac{R}{400}\right)^{4T}$.
- $P=\dfrac{A}{(1+R/100)^T}$; find $R$ or $T$ by matching $A/P$ with a power.
- For 2 years, $CI-SI=P\left(\frac{R}{100}\right)^2$.
- If the rate changes each year, multiply by each year's factor in turn.
- More frequent compounding gives a larger amount.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. For 1 year, the simple interest and the compound interest (yearly) on the same sum at the same rate are <span class="marks">[1]</span>
   (a) unequal (b) CI is greater (c) equal (d) SI is greater
2. The amount on principal $P$ at $R\%$ for $T$ years compounded half-yearly is <span class="marks">[1]</span>
   (a) $P(1+\frac{R}{100})^{T}$ (b) $P(1+\frac{R}{200})^{2T}$ (c) $P(1+\frac{R}{100})^{2T}$ (d) $P(1+\frac{R}{400})^{4T}$
3. The compound interest on Rs 1,000 for 2 years at 10% p.a. is <span class="marks">[1]</span>
   (a) Rs 200 (b) Rs 210 (c) Rs 220 (d) Rs 1,210
4. For 6% p.a. compounded half-yearly for 2 years, the rate per period and the number of periods are <span class="marks">[1]</span>
   (a) 6% and 2 (b) 3% and 4 (c) 12% and 1 (d) 3% and 2
5. A sum becomes four times itself in 2 years at compound interest. The rate is <span class="marks">[1]</span>
   (a) 50% (b) 25% (c) 100% (d) 200%

::: note Answers to Group A
**1.** (c) — for one period the interest is on the same principal.
**2.** (b) — halve the rate, double the time.
**3.** (b) — $1000\times 1.21=1210$, so $CI=210$.
**4.** (b) — $6\div 2=3\%$ per half-year; $2\times 2=4$ half-years.
**5.** (c) — $(1+\frac{R}{100})^2=4$, so $1+\frac{R}{100}=2$, $R=100$.
:::

**Group B — Short answer (2 marks each)**

1. Find the compound interest on Rs 5,000 for 2 years at 10% p.a. <span class="marks">[2]</span>
2. Find the amount of Rs 8,000 for 2 years at 5% p.a. compounded yearly. <span class="marks">[2]</span>
3. Find the difference between CI and SI on Rs 10,000 for 2 years at 5% p.a. <span class="marks">[2]</span>
4. Find the amount of Rs 16,000 for 1 year at 10% p.a. compounded half-yearly. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $A=5000\times 1.21=6050$; $CI=6050-5000=\text{Rs } 1{,}050$.
**2.** $A=8000\times(1.05)^2=8000\times 1.1025=\text{Rs } 8{,}820$.
**3.** $CI-SI=10000\times(0.05)^2=10000\times 0.0025=\text{Rs } 25$.
**4.** Rate $5\%$, 2 periods: $A=16000\times(1.05)^2=16000\times 1.1025=\text{Rs } 17{,}640$.
:::

**Group C — Short answer (3 marks each)**

1. Find the amount and compound interest on Rs 30,000 for 3 years at 10% p.a. compounded yearly. <span class="marks">[3]</span>
2. A sum amounts to Rs 13,310 in 3 years at 10% p.a. compound interest. Find the sum. <span class="marks">[3]</span>
3. Find the compound interest on Rs 40,000 for 1 year at 10% p.a. compounded half-yearly. <span class="marks">[3]</span>
4. At what rate of compound interest will Rs 6,250 become Rs 7,290 in 2 years? <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $A=30000\times(1.1)^3=30000\times 1.331=\text{Rs } 39{,}930$; $CI=39930-30000=\text{Rs } 9{,}930$.
**2.** $P=\dfrac{13310}{1.331}=\text{Rs } 10{,}000$.
**3.** Rate $5\%$ per half-year, 2 periods: $A=40000\times 1.1025=44100$; $CI=\text{Rs } 4{,}100$.
**4.** $\left(1+\frac{R}{100}\right)^2=\dfrac{7290}{6250}=1.1664=(1.08)^2$, so $R=8\%$ p.a.
:::

**Group D — Long answer (4 marks each)**

1. The difference between the compound interest and simple interest on a sum for 2 years at 8% p.a. is Rs 160. Find the sum, and the compound interest. <span class="marks">[4]</span>
2. Rs 80,000 is invested for 2 years at compound interest, with a rate of 5% for the first year and 10% for the second year. Find the amount and the compound interest. <span class="marks">[4]</span>
3. Rs 50,000 is deposited for 1 year at 12% p.a. Find the difference in the amounts when interest is compounded (a) half-yearly and (b) yearly. <span class="marks">[4]</span>
4. A sum of Rs 25,000 grows to Rs 36,000 in 2 years at compound interest. Find the rate of interest and the amount after 3 years. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** $P\left(\frac{8}{100}\right)^2=160$, so $P\times 0.0064=160$ and $P=\text{Rs } 25{,}000$. $A=25000\times(1.08)^2=25000\times 1.1664=29160$, so $CI=\text{Rs } 4{,}160$ (and $SI=4000$; difference $160$ ✓).
**2.** After year 1: $80000\times 1.05=84{,}000$. After year 2: $84000\times 1.10=92{,}400$. Amount $=\text{Rs } 92{,}400$; $CI=92400-80000=\text{Rs } 12{,}400$.
**3.** (a) Half-yearly: rate 6%, 2 periods, $A=50000\times(1.06)^2=50000\times 1.1236=\text{Rs } 56{,}180$. (b) Yearly: $A=50000\times 1.12=\text{Rs } 56{,}000$. Difference $=56180-56000=\text{Rs } 180$.
**4.** $\left(1+\frac{R}{100}\right)^2=\dfrac{36000}{25000}=1.44=(1.2)^2$, so $R=20\%$. After 3 years: $25000\times(1.2)^3=25000\times 1.728=\text{Rs } 43{,}200$.
:::
