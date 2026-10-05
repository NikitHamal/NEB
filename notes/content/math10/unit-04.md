---
subject: Mathematics
grade: 10
unit: 4
title: Population Growth and Depreciation
hours: 0
area: Compulsory Mathematics
---

A town's population grows year after year, and a new motorbike loses value year after year. Both are the same mathematics as compound interest: the quantity changes by a **fixed percentage of its present value** every period. Growth multiplies by a number bigger than 1; depreciation multiplies by a number smaller than 1. In this chapter you will use the compound-interest idea to find a population after some years, the population in the past, the effect of births, deaths and migration, and the value of a machine, vehicle or house after several years of depreciation.

::: key What the SEE asks from this chapter
One 3- or 4-mark question, almost always in one of these forms: (i) population after 2 or 3 years at a given rate; (ii) population changing at **different rates** in different years; (iii) a rate made from **birth, death and migration**; (iv) the **present population** of a town given its population 2 years ago, or the reverse; (v) value of a machine/vehicle after depreciation, or the **original cost** from the present value. Write the formula, substitute, simplify, and answer in a sentence.
:::

```photo id="math10/kathmandu-valley" caption="The Kathmandu valley seen from Battisputali. The number of people living here does not grow by the same number each year — it grows by a fixed percentage of the number already there, which is exactly compound growth." width="88"
```

## 4.1 Population Growth and Depreciation: concepts, formulas and worked problems

### Growth and decay are repeated multiplications

If a quantity increases by $R\%$ it becomes $\left(1+\dfrac{R}{100}\right)$ times itself. If it decreases by $R\%$ it becomes $\left(1-\dfrac{R}{100}\right)$ times itself. After $T$ periods we multiply $T$ times — the **same argument** as for compound interest in Chapter 3.

| Change | Factor | Example, $R=10$ |
|---|---|---|
| Increase by $R\%$ (population growth) | $1+\dfrac{R}{100}$ | $1.10$ |
| Decrease by $R\%$ (depreciation) | $1-\dfrac{R}{100}$ | $0.90$ |

### Population growth

::: key Population growth formulas
Let $P_0$ be the population at the beginning, $R\%$ the yearly growth rate and $P_T$ the population after $T$ years.

$$ P_T = P_0\left(1+\frac{R}{100}\right)^T $$

Population $T$ years **ago**: $P_0 = \dfrac{P_T}{\left(1+\frac{R}{100}\right)^T}$.

Increase in population $=P_T-P_0$.

If the rate is $R_1\%$, $R_2\%$, $R_3\%$ in successive years:
$$ P_3 = P_0\left(1+\frac{R_1}{100}\right)\left(1+\frac{R_2}{100}\right)\left(1+\frac{R_3}{100}\right) $$
:::

::: example Population after 3 years
**Problem.** The population of a village is 40,000. It increases at 5% every year. Find its population after 3 years.

**Solution.** $P_0=40000$, $R=5$, $T=3$.

$$ P_3 = 40000\left(1+\frac{5}{100}\right)^3 = 40000\times(1.05)^3 = 40000\times 1.157625 = 46305 $$

The population after 3 years is **46,305**. The increase is $46305-40000=6305$.
:::

::: example Population in the past
**Problem.** The present population of a town is 24,200. If it has been increasing at 10% per year, what was its population 2 years ago?

**Solution.** $24200 = P_0(1.1)^2 = 1.21\,P_0$.

$$ P_0 = \frac{24200}{1.21} = 20000 $$

The population 2 years ago was **20,000**.
:::

::: caution Population 2 years ago is a division
When the question asks for the population in the **past**, divide by the growth factor. Do not subtract 10% of the present population twice. 10% of 24,200 is 2,420, and $24200-2420-2420=19360$, which is wrong.
:::

### Different rates in different years

::: example Changing yearly rates
**Problem.** The population of a municipality is 1,25,000. It increases by 8% in the first year and by 5% in the second year, and decreases by 2% in the third year. Find the population after 3 years.

**Solution.** After year 1: $125000\times 1.08=135000$.

After year 2: $135000\times 1.05=141750$.

After year 3 (a decrease): $141750\times(1-0.02)=141750\times 0.98=138915$.

The population after 3 years is **1,38,915**.
:::

### Birth, death and migration

A population changes for three reasons: people are **born**, people **die**, and people **migrate** (move in or out). Each can be given as a rate (% of the population per year). **Net growth rate** is the combined effect.

::: definition Net growth rate
$$ \text{Net rate} = \text{birth rate} - \text{death rate} + \text{immigration rate} - \text{emigration rate} $$

Immigration means people **coming in**; emigration means people **going out**. If a question says "migration out", subtract it.
:::

```figure caption="Net growth rate of a town: birth rate 3.2%, death rate 1.2% and 0.5% of the people migrating out give a net growth of 1.5% per year."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.7, 2.7))
names = ['Births', 'Deaths', 'Migration\nout', 'Net growth']
start = [0, 3.2, 2.0, 0]
h = [3.2, -1.2, -0.5, 1.5]
cols = [SERIES[2], SERIES[1], SERIES[3], ACCENT]
for i in range(4):
    ax.bar(i, h[i], bottom=start[i], color=cols[i], width=0.55)
ax.text(0, 3.3, '+3.2%', ha='center', va='bottom', fontsize=8.5)
ax.text(1, 3.3, '−1.2%', ha='center', va='bottom', fontsize=8.5)
ax.text(2, 2.1, '−0.5%', ha='center', va='bottom', fontsize=8.5)
ax.text(3, 1.6, '1.5%', ha='center', va='bottom', fontsize=8.5, fontweight='bold')
ax.set_xticks(range(4)); ax.set_xticklabels(names, fontsize=8.5)
ax.set_ylim(0, 4.0)
ax.set_ylabel('% of population per year', fontsize=8.5)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='y', color=GRID, lw=0.5); ax.set_axisbelow(True)
```

::: example Using birth, death and migration rates
**Problem.** In a city of population 2,00,000, the birth rate is 3.2% and the death rate is 1.2% per year. Every year 0.5% of the population migrates out. Find the population after 2 years.

**Solution.** Net rate $=3.2-1.2-0.5=1.5\%$ per year.

$$ P_2 = 200000\left(1+\frac{1.5}{100}\right)^2 = 200000\times(1.015)^2 = 200000\times 1.030225 = 206045 $$

The population after 2 years is **2,06,045**.
:::

Sometimes a fixed **number** of people (not a percentage) migrates. Then you must apply the growth to the whole population and adjust the number **at the time** the migration happens.

::: example A fixed number migrates
**Problem.** A town has 50,000 people. In the first year the population grows by 4%; at the end of that year 2,000 people migrate out. In the second year it grows by 5%. Find the population at the end of the second year.

**Solution.** End of year 1 before migration: $50000\times 1.04=52000$.

After 2,000 leave: $52000-2000=50000$.

End of year 2: $50000\times 1.05=52500$.

The population is **52,500**.
:::

### Finding the rate or the time

::: example Finding the rate of growth
**Problem.** The population of a village increases from 20,000 to 22,050 in 2 years. Find the yearly rate of growth.

**Solution.** $22050=20000\left(1+\dfrac{R}{100}\right)^2$.

$$ \left(1+\frac{R}{100}\right)^2=\frac{22050}{20000}=1.1025=(1.05)^2 \;\Rightarrow\; R = 5 $$

The rate of growth is **5% per year**.
:::

::: example Finding the time
**Problem.** At what time will a population of 10,000, growing at 10% per year, become 13,310?

**Solution.** $13310=10000\times(1.1)^T$, so $(1.1)^T=1.331=(1.1)^3$, giving $T=3$ years.
:::

### Depreciation

::: definition Depreciation
**Depreciation** is the decrease in the value of an article (a machine, vehicle, computer, building) with time and use. The **rate of depreciation** is the percentage by which the value falls each year. The new value is the **present value**, **book value** or **depreciated value**.
:::

::: derivation Depreciation formula $V = P\left(1-\frac{R}{100}\right)^T$
We start from the original cost and find the value after each year, and then generalise.

**Setting up.** Original cost (or value) $=P$; depreciation $R\%$ per year, on the value at the beginning of the year; value after $T$ years $=V$. Write $r=\dfrac{R}{100}$.

**Step 1 — after 1 year.** Depreciation $=Pr$, so

$$ V_1 = P - Pr = P(1-r) $$

**Step 2 — after 2 years.** Depreciation in year 2 is charged on $V_1$ (not on $P$), so

$$ V_2 = V_1 - V_1 r = V_1(1-r) = P(1-r)^2 $$

**Step 3 — after $T$ years.** Each year multiplies the value by $(1-r)$, so

$$ V = P(1-r)^T = P\left(1-\frac{R}{100}\right)^T $$

**Result.** $V=P\left(1-\dfrac{R}{100}\right)^T$ and total depreciation $=P-V$.

**What it means.** The yearly loss in rupees gets smaller each year, because the percentage is taken on a smaller value. The depreciation in year 1 at 10% of Rs 5,00,000 is Rs 50,000; in year 2 it is 10% of Rs 4,50,000, which is only Rs 45,000.
:::

```figure caption="A population growing at 10% a year and a machine depreciating at 10% a year, both starting from 100 units. Growth curves up; depreciation curves down and flattens."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.7, 2.8))
t = np.arange(0, 11)
ax.plot(t, 100*1.1**t, color=SERIES[2], lw=2, marker='o', ms=3)
ax.plot(t, 100*0.9**t, color=SERIES[1], lw=2, marker='o', ms=3)
ax.axhline(100, color=MUTED, lw=0.8, ls='--')
ax.text(10.2, 100*1.1**10, 'growth\n259', fontsize=8, color=SERIES[2], va='center')
ax.text(10.2, 100*0.9**10, 'depreciation\n35', fontsize=8, color=SERIES[1], va='center')
ax.text(5.5, 104, 'start = 100', fontsize=8, color=MUTED)
ax.set_xlim(0, 13.5); ax.set_ylim(0, 280)
ax.set_xlabel('time (years)', fontsize=8.5)
ax.set_ylabel('value', fontsize=8.5)
ax.spines[['top','right']].set_visible(False)
ax.grid(color=GRID, lw=0.5); ax.set_axisbelow(True)
```

::: example Value after 3 years
**Problem.** A machine costs Rs 5,00,000 and depreciates at 10% per year. Find its value after 3 years and the total depreciation.

**Solution.** $V=500000\left(1-\dfrac{10}{100}\right)^3=500000\times(0.9)^3=500000\times 0.729=\text{Rs } 3{,}64{,}500$.

Total depreciation $=500000-364500=\text{Rs } 1{,}35{,}500$.

Year by year: $500000\to450000\to405000\to364500$.
:::

```figure caption="Value of the machine each year (Rs lakh). Each bar is 90% of the one before, so the yearly fall (50,000, 45,000, 40,500) is smaller each year."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 2.7))
vals = [500000, 450000, 405000, 364500]
labs = ['Start', 'After 1 yr', 'After 2 yrs', 'After 3 yrs']
for i, v in enumerate(vals):
    ax.bar(i, v/100000, color=ACCENT if i else INK, width=0.55)
    ax.text(i, v/100000 + 0.08, 'Rs {:,}'.format(v), ha='center', va='bottom', fontsize=6.8)
ax.set_xticks(range(4)); ax.set_xticklabels(labs, fontsize=8.5)
ax.set_ylim(0, 6)
ax.set_ylabel('value (Rs lakh)', fontsize=8.5)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='y', color=GRID, lw=0.5); ax.set_axisbelow(True)
```

::: example Different rates for different years
**Problem.** A car is bought for Rs 8,00,000. It depreciates by 15% in the first year and 10% in the second year. Find its value after 2 years.

**Solution.** After year 1: $800000\times(1-0.15)=800000\times 0.85=\text{Rs } 6{,}80{,}000$.

After year 2: $680000\times(1-0.10)=680000\times 0.90=\text{Rs } 6{,}12{,}000$.

The value after 2 years is **Rs 6,12,000**.
:::

::: example Finding the original cost
**Problem.** The value of a machine after 2 years is Rs 1,62,000. It depreciates at 10% per year. Find its original cost.

**Solution.** $162000=P(0.9)^2=0.81\,P$.

$$ P=\frac{162000}{0.81}=\text{Rs } 2{,}00{,}000 $$
:::

::: example Finding the rate of depreciation
**Problem.** A laptop bought for Rs 60,000 is worth Rs 38,400 after 2 years. Find the yearly rate of depreciation.

**Solution.** $38400=60000\left(1-\dfrac{R}{100}\right)^2$.

$$ \left(1-\frac{R}{100}\right)^2=\frac{38400}{60000}=0.64=(0.8)^2 $$

So $1-\dfrac{R}{100}=0.8$, giving $R=20$. The rate of depreciation is **20% per year**.
:::

::: example Depreciation compounded half-yearly
**Problem.** A machine worth Rs 2,00,000 depreciates at 20% per year, the depreciation being calculated half-yearly. Find its value after 1 year.

**Solution.** Rate per half-year $=\dfrac{20}{2}=10\%$ and number of half-years $=2$.

$$ V=200000\times(0.9)^2=200000\times 0.81=\text{Rs } 1{,}62{,}000 $$

(Calculated yearly it would be $200000\times 0.8=1{,}60{,}000$.)
:::

### Increase followed by decrease

A frequent trap: a rise of $x\%$ followed by a fall of $x\%$ does **not** return to the start.

::: example Up 10%, then down 10%
**Problem.** The population of a town increases by 10% in one year and then decreases by 10% in the next year. If the present population is 1,98,000, find the original population and the net percentage change.

**Solution.** Factor over two years $=1.1\times 0.9=0.99$.

$$ 198000 = 0.99\,P_0 \;\Rightarrow\; P_0=\frac{198000}{0.99}=200000 $$

Net change $=0.99-1=-0.01$, i.e. a **1% decrease** overall.

Why? The 10% rise is on 2,00,000 (a gain of 20,000), but the 10% fall is on the larger 2,20,000 (a loss of 22,000), so the town ends with 2,000 fewer people.
:::

::: tip Choosing between growth and depreciation
Ask one question: *is the quantity getting larger or smaller?* Larger — factor $1+\frac{R}{100}$. Smaller — factor $1-\frac{R}{100}$. Everything else (powers, finding $P$, $R$ or $T$) works exactly as in compound interest.
:::

::: caution Common mistakes
- Using the **original** value for every year's change. The change in each year is on the value at the **start of that year**.
- Using $1+\frac{R}{100}$ for depreciation. A depreciation of 10% means factor $0.9$, not $1.1$.
- Adding the rates for several years (e.g. 5% and 10% make 15%). Multiply the factors $1.05\times 1.10=1.155$.
- Subtracting the original population when the question asks for **increase** and giving the final population instead.
:::

### More practice in context

::: example Comparing two towns
**Problem.** Town A has 1,00,000 people and grows at 4% per year. Town B has 1,20,000 people and its population falls by 1% per year. Find the difference in their populations after 2 years.

**Solution.** Town A: $100000\times(1.04)^2=100000\times 1.0816=108160$.

Town B: $120000\times(0.99)^2=120000\times 0.9801=117612$.

Difference $=117612-108160=9452$. Town B is still larger by 9,452 people, although it is shrinking and Town A is growing.
:::

::: example Value lost by a computer
**Problem.** A school buys a computer for Rs 90,000. It depreciates at 10% per year. Find its value after 2 years and the loss in value.

**Solution.** $V=90000\times(0.9)^2=90000\times 0.81=\text{Rs } 72{,}900$.

Loss in value $=90000-72900=\text{Rs } 17{,}100$.

This is $\dfrac{17100}{90000}\times 100=19\%$ of the cost, not $20\%$, because the second year's 10% is charged on the smaller value.
:::

::: example Students in a school
**Problem.** A school has 1,250 students. The number increases by 8% every year. How many students will there be after 2 years, and what is the increase?

**Solution.** $1250\times 1.08=1350$ and $1350\times 1.08=1458$.

Students after 2 years $=1{,}458$. Increase $=1458-1250=208$ students.
:::

## 4.2 Exercises of the SEE type

### Method

1. Decide: growth (factor $1+\frac{R}{100}$) or depreciation (factor $1-\frac{R}{100}$).
2. If birth, death and migration are given, first find the **net rate**.
3. Write $P_T=P_0(\ldots)^T$ or $V=P(\ldots)^T$, substitute and compute the power step by step.
4. For "past" values, divide by the factor.
5. For "increase" or "depreciation amount", subtract the smaller value from the larger.
6. State the answer with its unit (people, Rs).

## Chapter summary

- Growth: $P_T=P_0\left(1+\frac{R}{100}\right)^T$. Past population: divide by the factor.
- Net rate $=$ birth $-$ death $+$ immigration $-$ emigration (all in % per year).
- For different yearly rates multiply the factors; for a fixed number of migrants add or subtract at the correct time.
- Depreciation: $V=P\left(1-\frac{R}{100}\right)^T$; total depreciation $=P-V$.
- Depreciation each year is charged on the value at the start of that year, so the yearly loss shrinks.
- Half-yearly: halve the rate and double the number of periods.
- Find $R$ or $T$ by matching $A/P$ (or $V/P$) with a power such as $1.1^2=1.21$, $0.9^2=0.81$, $0.8^2=0.64$.
- An increase of $x\%$ followed by a decrease of $x\%$ gives a net decrease.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. A population of 10,000 grows at 10% per year. After 1 year it is <span class="marks">[1]</span>
   (a) 10,010 (b) 11,000 (c) 10,100 (d) 9,000
2. The value of an article after $T$ years of depreciation at $R\%$ per year is <span class="marks">[1]</span>
   (a) $P(1+\frac{R}{100})^T$ (b) $P(1-\frac{RT}{100})$ (c) $P(1-\frac{R}{100})^T$ (d) $P(1-\frac{R}{100})^{2T}$
3. Birth rate 3%, death rate 1% and emigration 0.5% give a net growth rate of <span class="marks">[1]</span>
   (a) 4.5% (b) 2% (c) 1.5% (d) 3.5%
4. A machine worth Rs 1,00,000 depreciates 10% in one year. Its value is <span class="marks">[1]</span>
   (a) Rs 99,000 (b) Rs 90,000 (c) Rs 1,10,000 (d) Rs 80,000
5. If a population decreases by 10% each year, the yearly factor is <span class="marks">[1]</span>
   (a) 1.1 (b) 0.1 (c) 0.9 (d) 1.9

::: note Answers to Group A
**1.** (b) — $10000\times 1.1=11000$.
**2.** (c) — each year multiplies the value by $1-\frac{R}{100}$.
**3.** (c) — $3-1-0.5=1.5\%$.
**4.** (b) — $100000\times 0.9=90000$.
**5.** (c) — $1-\frac{10}{100}=0.9$.
:::

**Group B — Short answer (2 marks each)**

1. The population of a village is 50,000 and grows at 4% per year. Find the population after 2 years. <span class="marks">[2]</span>
2. The present population of a town is 36,300. It has increased at 10% a year. What was it 2 years ago? <span class="marks">[2]</span>
3. A scooter bought for Rs 1,00,000 depreciates at 10% per year. Find its value after 2 years. <span class="marks">[2]</span>
4. A machine costs Rs 2,50,000 and loses 20% of its value in one year. Find its value after one year. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $50000\times(1.04)^2=50000\times 1.0816=54{,}080$.
**2.** $P_0=\dfrac{36300}{(1.1)^2}=\dfrac{36300}{1.21}=30{,}000$.
**3.** $100000\times(0.9)^2=100000\times 0.81=\text{Rs } 81{,}000$.
**4.** $250000\times 0.8=\text{Rs } 2{,}00{,}000$.
:::

**Group C — Short answer (3 marks each)**

1. The population of a town is 60,000. It grows by 5% in the first year and by 10% in the second year. Find the population after 2 years. <span class="marks">[3]</span>
2. The population of a village increases from 25,000 to 30,250 in 2 years. Find the yearly rate of growth. <span class="marks">[3]</span>
3. A car costing Rs 12,00,000 depreciates at 15% per year. Find its value after 2 years. <span class="marks">[3]</span>
4. In a town of population 1,50,000, the birth rate is 3.5%, the death rate is 1% and 0.5% migrate out each year. Find the population after 2 years. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $60000\times 1.05=63000$; $63000\times 1.10=69{,}300$.
**2.** $\left(1+\frac{R}{100}\right)^2=\dfrac{30250}{25000}=1.21=(1.1)^2$, so $R=10\%$.
**3.** $1200000\times(0.85)^2=1200000\times 0.7225=\text{Rs } 8{,}67{,}000$.
**4.** Net rate $=3.5-1-0.5=2\%$. $P_2=150000\times(1.02)^2=150000\times 1.0404=1{,}56{,}060$.
:::

**Group D — Long answer (4 marks each)**

1. A city has a population of 2,00,000 and grows at 5% per year. At the end of the first year 5,000 people migrate out. Find the population at the end of the second year. <span class="marks">[4]</span>
2. A machine bought for Rs 4,00,000 depreciates at 20% per year. Find its value after 2 years. If it is then sold at 10% above this value, find the selling price and the loss compared with the cost price. <span class="marks">[4]</span>
3. The value of a machine after 3 years is Rs 3,64,500. It depreciates at 10% per year. Find its original cost and the total depreciation. <span class="marks">[4]</span>
4. The population of a town increases by 10% in a year and decreases by 10% in the next year. If the present population is 1,98,000, find the original population. What is the net percentage change? <span class="marks">[4]</span>

::: note Answers to Group D
**1.** End of year 1: $200000\times 1.05=210000$; after migration $210000-5000=205000$. End of year 2: $205000\times 1.05=2{,}15{,}250$ people.
**2.** Value after 2 years $=400000\times(0.8)^2=400000\times 0.64=\text{Rs } 2{,}56{,}000$. Selling price $=256000\times 1.1=\text{Rs } 2{,}81{,}600$. Loss $=400000-281600=\text{Rs } 1{,}18{,}400$.
**3.** $364500=P(0.9)^3=0.729\,P$, so $P=\dfrac{364500}{0.729}=\text{Rs } 5{,}00{,}000$. Total depreciation $=500000-364500=\text{Rs } 1{,}35{,}500$.
**4.** Factor $=1.1\times 0.9=0.99$. $P_0=\dfrac{198000}{0.99}=2{,}00{,}000$. Net change $=0.99-1=-0.01$, a **1% decrease**.
:::
