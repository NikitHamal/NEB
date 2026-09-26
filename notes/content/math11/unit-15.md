---
subject: Mathematics
grade: 11
unit: 15
title: Measures of Dispersion
hours: 6
area: Statistics and Probability
---

An average tells you where a set of data sits, but nothing about how tightly the
values cluster round that centre. Two classes can have the same mean mark of 50
and yet one class may have everyone between 45 and 55 while the other has marks
from 5 to 95. **Dispersion** is the measure of that spread, and it is what turns a
single average into a usable description of the data.

::: key The one idea behind this unit
Two distributions can share a mean and be completely different. Dispersion
measures how far the observations wander from the mean; the **standard deviation**
measures it in the original units, the **coefficient of variation** measures it as
a percentage so that different units can be compared, and **skewness** measures
whether the wandering is symmetric or lopsided.
:::

```figure caption="Two distributions with exactly the same mean $\bar{x} = 50$. The narrow one has $\sigma = 4$, the wide one $\sigma = 8$. The mean alone cannot tell them apart — dispersion can."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
x=np.linspace(20,80,500)
def curve(s): return np.exp(-0.5*((x-50)/s)**2)/(s*np.sqrt(2*np.pi))
for s,c,lab in [(4,ACCENT,'$\\sigma = 4$  (small spread)'),(8,SERIES[1],'$\\sigma = 8$  (large spread)')]:
    ax.plot(x,curve(s),color=c,lw=2.0,label=lab)
    ax.fill_between(x,0,curve(s),where=(np.abs(x-50)<=s),color=c,alpha=0.12)
ax.axvline(50,color=INK,lw=1.1,ls=(0,(4,2)))
ax.annotate('$\\bar{x}=50$',(50,0.107),color=INK,fontsize=9.5,ha='center')
for s,c,y in [(4,ACCENT,0.020),(8,SERIES[1],0.008)]:
    ax.annotate('',xy=(50-s,y),xytext=(50+s,y),
                arrowprops=dict(arrowstyle='<|-|>',color=c,lw=1.2,mutation_scale=9))
    ax.annotate('$\\pm\\sigma$',(50+s,y),textcoords='offset points',xytext=(6,-3),
                color=c,fontsize=8.6)
ax.set_xlabel('value of the variable  $x$'); ax.set_ylabel('frequency density')
ax.set_xlim(20,80); ax.set_ylim(0,0.126); ax.set_yticks([])
ax.spines[['top','right']].set_visible(False); ax.legend(loc='upper left',fontsize=8.4)
```

## 15.1 Standard deviation and variance

### The measures of dispersion, in order of usefulness

| Measure | Formula | Comment |
|---|---|---|
| Range | $R = L - S$ (largest $-$ smallest) | uses only two values; very crude |
| Quartile deviation | $Q.D. = \dfrac{Q_3 - Q_1}{2}$ | ignores the extreme quarter at each end |
| Mean deviation | $M.D. = \dfrac{\sum | x - \bar{x}|}{n}$ | uses all values, but $|\ |$ is awkward algebra |
| Standard deviation | $\sigma = \sqrt{\dfrac{\sum (x-\bar{x})^{2}}{n}}$ | uses all values; the standard measure |

The first three are quick but throw information away. The standard deviation
squares the deviations instead of taking their absolute value: squaring removes
the sign, keeps every observation in play, and behaves well algebraically. That
is why it is the measure used everywhere.

```figure caption="A box plot of the data $12, 15, 18, 20, 22, 25, 30, 35, 40, 45$. The box runs from $Q_1 = 17.25$ to $Q_3 = 36.25$, so $Q.D. = \frac{1}{2}(36.25-17.25) = 9.5$: half the width of the box."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.4))
data=[12,15,18,20,22,25,30,35,40,45]
q1,md,q3=17.25,23.5,36.25
ax.add_patch(plt.Rectangle((q1,0.62),q3-q1,0.36,facecolor=ACCENT,alpha=0.16,
                           edgecolor=ACCENT,lw=1.4))
ax.plot([md,md],[0.62,0.98],color=SERIES[1],lw=2.2)
ax.plot([12,q1],[0.80,0.80],color=INK,lw=1.1); ax.plot([q3,45],[0.80,0.80],color=INK,lw=1.1)
for v in (12,45): ax.plot([v,v],[0.70,0.90],color=INK,lw=1.1)
ax.plot(data,[0.40]*len(data),'o',color=MUTED,ms=4.5,alpha=0.85)
for v,lab,c,yy in [(q1,'$Q_1=17.25$',ACCENT,1.02),(md,'median $=23.5$',SERIES[1],1.19),
                   (q3,'$Q_3=36.25$',ACCENT,1.02)]:
    ax.annotate(lab,(v,yy),color=c,fontsize=8.6,ha='center')
ax.annotate('',xy=(q1,0.25),xytext=(q3,0.25),
            arrowprops=dict(arrowstyle='<|-|>',color=SERIES[2],lw=1.3,mutation_scale=10))
ax.annotate('inter-quartile range $=19$,  so $Q.D.=9.5$',((q1+q3)/2,0.25),
            textcoords='offset points',xytext=(0,-15),color=SERIES[2],fontsize=8.8,ha='center')
ax.annotate('data values',(12,0.40),textcoords='offset points',xytext=(-4,-1),
            color=MUTED,fontsize=8.4,ha='right',va='center')
ax.set_xlim(6,50); ax.set_ylim(0.0,1.34); ax.set_yticks([])
ax.set_xlabel('value'); ax.spines[['top','right','left']].set_visible(False)
```

### Variance and standard deviation of an individual series

::: definition Variance and standard deviation
For $n$ observations $x_1, x_2, \ldots, x_n$ with mean $\bar{x}$, the **variance**
is the mean of the squared deviations and the **standard deviation** is its
positive square root:
$$ \sigma^{2} = \frac{\sum (x - \bar{x})^{2}}{n}, \qquad \sigma = \sqrt{\frac{\sum (x-\bar{x})^{2}}{n}} $$
Variance is measured in the square of the original unit; standard deviation is in
the original unit.
:::

Expanding the square gives a second form that avoids computing every deviation:

$$ \sigma^{2} = \frac{\sum x^{2}}{n} - \left(\frac{\sum x}{n}\right)^{2} = \frac{\sum x^{2}}{n} - \bar{x}^{2} $$

and if the mean is awkward, subtract a convenient **assumed mean** $A$ and work
with $d = x - A$:

$$ \sigma = \sqrt{\frac{\sum d^{2}}{n} - \left(\frac{\sum d}{n}\right)^{2}} $$

::: example Worked example 15.1
**Problem.** Find the range, mean deviation from the mean, variance and standard
deviation of $2, 4, 4, 4, 5, 5, 7, 9$.

**Solution.** Here $n = 8$ and $\sum x = 2+4+4+4+5+5+7+9 = 40$, so
$\bar{x} = 40/8 = 5$.

| $x$ | $d = x-\bar{x}$ | $| d|$ | $d^{2}$ |
|---|---|---|---|
| 2 | $-3$ | 3 | 9 |
| 4 | $-1$ | 1 | 1 |
| 4 | $-1$ | 1 | 1 |
| 4 | $-1$ | 1 | 1 |
| 5 | $0$ | 0 | 0 |
| 5 | $0$ | 0 | 0 |
| 7 | $2$ | 2 | 4 |
| 9 | $4$ | 4 | 16 |
| **$\sum x = 40$** | **$\sum d = 0$** | **$\sum| d| = 12$** | **$\sum d^{2} = 32$** |

Range $= 9 - 2 = 7$.

$$ M.D. = \frac{\sum | d |}{n} = \frac{12}{8} = 1.5 $$

$$ \sigma^{2} = \frac{\sum d^{2}}{n} = \frac{32}{8} = 4, \qquad \sigma = \sqrt{4} = 2 $$

**Check by the $\sum x^{2}$ method.** $\sum x^{2} = 4+16+16+16+25+25+49+81 = 232$, so

$$ \sigma^{2} = \frac{232}{8} - 5^{2} = 29 - 25 = 4 \ \checkmark $$
:::

::: caution The $\sum d = 0$ column is not a mistake
The deviations from the mean always add to zero — that is what "mean" means. So
$\sum d$ can never be used as a measure of spread, and this is exactly why we
square the deviations. Use the $\sum d = 0$ row as a check on your arithmetic.
:::

::: example Worked example 15.2
**Problem.** The daily earnings (in hundreds of rupees) of five shopkeepers in
Asan bazaar are $25, 32, 43, 19, 21$. Find the variance and the standard deviation.

**Solution.** The mean is not a round number here, so use the $\sum x^{2}$ form.

| $x$ | 25 | 32 | 43 | 19 | 21 | total |
|---|---|---|---|---|---|---|
| $x^{2}$ | 625 | 1024 | 1849 | 361 | 441 | $\sum x^{2} = 4300$ |

$\sum x = 140$, $n = 5$, so $\bar{x} = 140/5 = 28$.

$$ \sigma^{2} = \frac{\sum x^{2}}{n} - \bar{x}^{2} = \frac{4300}{5} - 28^{2} = 860 - 784 = 76 $$

$$ \sigma = \sqrt{76} = 8.72 \text{ (hundred rupees)} $$
:::

### Discrete frequency distribution

When each value $x$ occurs $f$ times, every sum is weighted by the frequency.
With $N = \sum f$,

$$ \bar{x} = \frac{\sum fx}{N}, \qquad \sigma = \sqrt{\frac{\sum f(x-\bar{x})^{2}}{N}} = \sqrt{\frac{\sum fx^{2}}{N} - \bar{x}^{2}} $$

::: example Worked example 15.3
**Problem.** Find the mean, variance and standard deviation of the following
distribution.

| Marks $(x)$ | 2 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|
| No. of students $(f)$ | 1 | 4 | 6 | 4 | 1 |

**Solution.** Build the table column by column.

| $x$ | $f$ | $fx$ | $d = x - 6$ | $d^{2}$ | $fd^{2}$ |
|---|---|---|---|---|---|
| 2 | 1 | 2 | $-4$ | 16 | 16 |
| 4 | 4 | 16 | $-2$ | 4 | 16 |
| 6 | 6 | 36 | $0$ | 0 | 0 |
| 8 | 4 | 32 | $2$ | 4 | 16 |
| 10 | 1 | 10 | $4$ | 16 | 16 |
| **Total** | **$N=16$** | **$\sum fx = 96$** | | | **$\sum fd^{2} = 64$** |

$$ \bar{x} = \frac{\sum fx}{N} = \frac{96}{16} = 6 \text{ marks} $$

(The $d$ column was written using this mean, which is why it was computed first.)

$$ \sigma^{2} = \frac{\sum fd^{2}}{N} = \frac{64}{16} = 4, \qquad \sigma = 2 \text{ marks} $$
:::

### Continuous distribution: the step-deviation method

For a grouped distribution take $x$ to be the **mid-value** of each class. If the
class width $h$ is constant, choose an assumed mean $A$ (a convenient mid-value)
and set

$$ d' = \frac{x - A}{h} $$

Then the step-deviation formulae are

::: key Step-deviation formulae
$$ \bar{x} = A + \frac{\sum f d'}{N} \times h, \qquad \sigma = h\sqrt{\frac{\sum f d'^{2}}{N} - \left(\frac{\sum f d'}{N}\right)^{2}} $$
These are the fastest hand methods for grouped data. The $h$ **multiplies** the
standard deviation but only the *correction term* of the mean.
:::

::: example Worked example 15.4
**Problem.** Calculate the mean and the standard deviation of the following
distribution of daily wages.

| Wages (Rs) | 0–10 | 10–20 | 20–30 | 30–40 | 40–50 |
|---|---|---|---|---|---|
| No. of workers | 5 | 8 | 15 | 16 | 6 |

**Solution.** Take $A = 25$ (the mid-value of $20$–$30$) and $h = 10$.

| Class | $f$ | mid $x$ | $d' = \dfrac{x-25}{10}$ | $fd'$ | $fd'^{2}$ |
|---|---|---|---|---|---|
| 0–10 | 5 | 5 | $-2$ | $-10$ | 20 |
| 10–20 | 8 | 15 | $-1$ | $-8$ | 8 |
| 20–30 | 15 | 25 | $0$ | $0$ | 0 |
| 30–40 | 16 | 35 | $1$ | $16$ | 16 |
| 40–50 | 6 | 45 | $2$ | $12$ | 24 |
| **Total** | **$N = 50$** | | | **$\sum fd' = 10$** | **$\sum fd'^{2} = 68$** |

$$ \bar{x} = A + \frac{\sum fd'}{N}\times h = 25 + \frac{10}{50}\times 10 = 25 + 2 = \text{Rs } 27 $$

$$ \sigma = h\sqrt{\frac{\sum fd'^{2}}{N} - \left(\frac{\sum fd'}{N}\right)^{2}} = 10\sqrt{\frac{68}{50} - \left(\frac{10}{50}\right)^{2}} $$

$$ \sigma = 10\sqrt{1.36 - 0.04} = 10\sqrt{1.32} = 10(1.1489) = \text{Rs } 11.49 $$

Variance $= \sigma^{2} = 132$ (rupees squared).
:::

```figure caption="The distribution of Worked example 15.4. The mean is Rs 27 and $\sigma = $ Rs 11.49; the shaded band is $\bar{x}\pm\sigma$ and the outer marks are $\bar{x}\pm2\sigma$, which here covers essentially the whole distribution."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.9))
edges=np.array([0,10,20,30,40,50]); f=np.array([5,8,15,16,6])
m, s = 27.0, 11.489
ax.bar(edges[:-1],f,width=10,align='edge',color=ACCENT,alpha=0.30,
       edgecolor=ACCENT,lw=1.1)
ax.axvspan(m-s,m+s,color=SERIES[2],alpha=0.10,zorder=0)
ax.axvline(m,color=SERIES[1],lw=1.8)
for v,ls in [(m-s,'-'),(m+s,'-')]:
    ax.axvline(v,color=SERIES[2],lw=1.2,ls=(0,(4,2)))
for v in (m-2*s,m+2*s):
    ax.axvline(v,color=MUTED,lw=1.0,ls=':')
ax.annotate('$\\bar{x}=27$',(m,17.1),color=SERIES[1],fontsize=9.2,ha='center')
ax.annotate('$\\bar{x}-\\sigma$',(m-s,14.6),color=SERIES[2],fontsize=8.4,ha='right')
ax.annotate('$\\bar{x}+\\sigma$',(m+s,14.6),color=SERIES[2],fontsize=8.4,ha='left')
ax.annotate('$\\bar{x}-2\\sigma$',(m-2*s,11.4),color=MUTED,fontsize=8.0,ha='left')
ax.annotate('$\\bar{x}+2\\sigma$',(m+2*s,11.4),color=MUTED,fontsize=8.0,ha='right')
ax.set_xlabel('daily wages (Rs)'); ax.set_ylabel('number of workers')
ax.set_xlim(-2,52); ax.set_ylim(0,18.6)
ax.set_xticks(edges)
ax.spines[['top','right']].set_visible(False); ax.grid(axis='y',alpha=0.45)
```

### Properties of the standard deviation

::: key Four properties worth memorising
1. $\sigma \geq 0$, and $\sigma = 0$ only when every observation is equal.
2. **Independent of change of origin.** Adding a constant $c$ to every observation
   leaves $\sigma$ unchanged (the whole distribution shifts, the spread does not).
3. **Not independent of change of scale.** Multiplying every observation by $k$
   multiplies $\sigma$ by $| k|$ and the variance by $k^{2}$.
4. **Combined standard deviation** of two groups with sizes $n_1, n_2$, means
   $\bar{x}_1, \bar{x}_2$ and standard deviations $\sigma_1, \sigma_2$:
   $$ \sigma_{12} = \sqrt{\frac{n_1(\sigma_1^{2} + d_1^{2}) + n_2(\sigma_2^{2} + d_2^{2})}{n_1 + n_2}} $$
   where $d_1 = \bar{x}_1 - \bar{x}_{12}$, $d_2 = \bar{x}_2 - \bar{x}_{12}$ and
   $\bar{x}_{12} = \dfrac{n_1\bar{x}_1 + n_2\bar{x}_2}{n_1+n_2}$.
:::

::: example Worked example 15.5
**Problem.** The standard deviation of $2, 4, 6, 8, 10$ is $2\sqrt{2}$. Without
recomputing from scratch, write down the standard deviation of (a)
$7, 9, 11, 13, 15$ and (b) $6, 12, 18, 24, 30$.

**Solution.**

(a) Each value is $5$ more than the original: this is a change of **origin** only.
The standard deviation is unchanged, $\sigma = 2\sqrt{2} = 2.83$.

(b) Each value is $3$ times the original: this is a change of **scale** with
$k = 3$. Hence $\sigma' = 3 \times 2\sqrt{2} = 6\sqrt{2} = 8.49$, and the variance
becomes $9 \times 8 = 72$.
:::

::: example Worked example 15.6
**Problem.** Section A has $50$ students with mean mark $54$ and $\sigma_1 = 8$;
section B has $100$ students with mean mark $60$ and $\sigma_2 = 10$. Find the
combined mean and the combined standard deviation.

**Solution.** Combined mean first:

$$ \bar{x}_{12} = \frac{n_1\bar{x}_1 + n_2\bar{x}_2}{n_1+n_2} = \frac{50(54) + 100(60)}{150} = \frac{2700 + 6000}{150} = \frac{8700}{150} = 58 $$

Deviations of the group means from the combined mean:
$d_1 = 54 - 58 = -4$ and $d_2 = 60 - 58 = 2$.

$$ \sigma_{12}^{2} = \frac{50(8^{2} + (-4)^{2}) + 100(10^{2} + 2^{2})}{150} = \frac{50(64+16) + 100(100+4)}{150} $$

$$ = \frac{50(80) + 100(104)}{150} = \frac{4000 + 10400}{150} = \frac{14400}{150} = 96 $$

$$ \sigma_{12} = \sqrt{96} = 9.80 \text{ marks} $$
:::

## 15.2 Coefficient of variation

Standard deviation carries the unit of the data, so it cannot compare a
distribution of weights in kilograms with one of wages in rupees — and even in the
same unit, a standard deviation of Rs 500 means something very different on a mean
wage of Rs 5{,}000 than on a mean wage of Rs 2{,}000. Dividing by the mean removes
both problems.

::: definition Coefficient of variation
$$ C.V. = \frac{\sigma}{\bar{x}} \times 100\% $$
It is a pure number (a percentage), independent of the unit of measurement. The
series with the **greater** C.V. is the **more variable** (less consistent, less
uniform, less stable); the series with the **smaller** C.V. is the more consistent.
:::

```figure caption="Standard deviation alone can mislead. Factory B has the smaller $\sigma$ but, measured against its much smaller mean wage, it is the more variable of the two: $C.V. = 20\%$ against $10\%$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.5))
rows=[('Factory A',5000,500,ACCENT),('Factory B',2000,400,SERIES[1])]
for i,(name,m,s,c) in enumerate(rows):
    y=1-i
    ax.errorbar([m],[y],xerr=[s],fmt='o',color=c,ecolor=c,elinewidth=2.4,
                capsize=6,capthick=1.6,ms=7)
    ax.annotate(name,(0,y),textcoords='offset points',xytext=(2,14),
                color=c,fontsize=9.2,ha='left')
    ax.annotate(f'mean = Rs {m:,}   σ = Rs {s}   C.V. = {s/m*100:.0f}%',
                (0,y),textcoords='offset points',xytext=(2,-15),
                color=MUTED,fontsize=8.6,ha='left')
ax.set_xlim(0,6200); ax.set_ylim(-0.75,1.75); ax.set_yticks([])
ax.set_xlabel('daily wage (Rs)')
ax.spines[['top','right','left']].set_visible(False); ax.grid(axis='x',alpha=0.45)
```

::: example Worked example 15.7
**Problem.** The runs scored by two batsmen in five innings are

| Anil | 44 | 48 | 50 | 52 | 56 |
|---|---|---|---|---|---|
| **Bikash** | 38 | 46 | 50 | 54 | 62 |

Who is the better scorer on average, and who is the more consistent?

**Solution.** Both totals are $250$, so both means are $\bar{x} = 250/5 = 50$ runs:
on average the two are equally good. Now the deviations.

| Anil $x$ | $d = x-50$ | $d^{2}$ | | Bikash $y$ | $d = y-50$ | $d^{2}$ |
|---|---|---|---|---|---|---|
| 44 | $-6$ | 36 | | 38 | $-12$ | 144 |
| 48 | $-2$ | 4 | | 46 | $-4$ | 16 |
| 50 | $0$ | 0 | | 50 | $0$ | 0 |
| 52 | $2$ | 4 | | 54 | $4$ | 16 |
| 56 | $6$ | 36 | | 62 | $12$ | 144 |
| **250** | **0** | **80** | | **250** | **0** | **320** |

$$ \sigma_A = \sqrt{\frac{80}{5}} = \sqrt{16} = 4, \qquad \sigma_B = \sqrt{\frac{320}{5}} = \sqrt{64} = 8 $$

$$ C.V._A = \frac{4}{50}\times 100 = 8\%, \qquad C.V._B = \frac{8}{50}\times 100 = 16\% $$

Both average $50$ runs, but Anil's C.V. is the smaller, so **Anil is the more
consistent** batsman. Bikash is twice as variable.
:::

::: example Worked example 15.8
**Problem.** Factory A pays a mean daily wage of Rs $5000$ with
$\sigma = $ Rs $500$; factory B pays a mean of Rs $2000$ with $\sigma = $ Rs $400$.
(a) Which factory has more variable wages? (b) If a third factory has
$C.V. = 25\%$ and mean wage Rs $4000$, find its standard deviation.

**Solution.**

(a) Compare the coefficients of variation, not the standard deviations:

$$ C.V._A = \frac{500}{5000}\times100 = 10\%, \qquad C.V._B = \frac{400}{2000}\times100 = 20\% $$

Factory B has the larger C.V., so **B has the more variable wages** — even though
its standard deviation is the smaller of the two.

(b) Rearranging $C.V. = \dfrac{\sigma}{\bar{x}}\times100$:

$$ \sigma = \frac{C.V. \times \bar{x}}{100} = \frac{25 \times 4000}{100} = \text{Rs } 1000 $$
:::

::: caution Never compare standard deviations across different means
"Series A has $\sigma = 500$ and series B has $\sigma = 400$, so B is more
consistent" is wrong unless the two means are equal. Consistency questions are
always decided by the C.V.
:::

## 15.3 Skewness; Karl Pearson's coefficient of skewness

Dispersion says how *wide* a distribution is. **Skewness** says whether it is
*lopsided*.

::: definition Skewness
A distribution is **symmetric** if the two halves about the centre are mirror
images; then mean $=$ median $=$ mode. It is **positively skewed** if it has a long
tail to the right (mean $>$ median $>$ mode) and **negatively skewed** if it has a
long tail to the left (mean $<$ median $<$ mode).
:::

```figure caption="The three shapes. For a symmetric curve mean, median and mode coincide; a long right tail drags the mean above the mode (positive skew), a long left tail drags it below (negative skew). Note the order: $M_o, M_d, \\bar{x}$ always runs the same way as the tail."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(3,1,figsize=(4.8,4.3))
x=np.linspace(0,10,800)
def gam(x,k,th):
    xx=np.clip(x,1e-9,None)
    return xx**(k-1)*np.exp(-xx/th)
curves=[('negatively skewed',gam(10-x,3.0,1.15)),
        ('symmetric',np.exp(-0.5*((x-5)/1.5)**2)),
        ('positively skewed',gam(x,3.0,1.15))]
for ax,(title,y) in zip(axes,curves):
    y=y/y.max()
    ax.plot(x,y,color=ACCENT,lw=2.0)
    ax.fill_between(x,0,y,color=ACCENT,alpha=0.10)
    mode=x[np.argmax(y)]
    cum=np.cumsum(y); med=x[np.searchsorted(cum,cum[-1]/2)]
    mean=(x*y).sum()/y.sum()
    if title=='symmetric':
        ax.axvline(5,color=SERIES[1],lw=1.4)
        ax.annotate('mean = median = mode',(5,0.62),color=SERIES[1],fontsize=8.4,
                    ha='center',bbox=dict(boxstyle='round,pad=0.14',fc='white',ec='none'))
    else:
        items=sorted([(mode,'mode $M_o$',SERIES[2]),(med,'median $M_d$',MUTED),
                      (mean,'mean $\\bar{x}$',SERIES[1])])
        for v,lab,c in items:
            ax.axvline(v,color=c,lw=1.3,ls=(0,(4,2)))
        for j,(v,lab,c) in enumerate(items):
            ha='right' if title=='negatively skewed' else 'left'
            dx=-8 if ha=='right' else 8
            ax.annotate(lab,(v,0.92-0.26*j),textcoords='offset points',xytext=(dx,0),
                        color=c,fontsize=8.4,ha=ha,va='center',
                        bbox=dict(boxstyle='round,pad=0.10',fc='white',ec='none'))
    ax.set_title(title,fontsize=9.0,loc='left')
    ax.set_xlim(0,10); ax.set_ylim(0,1.20); ax.set_xticks([]); ax.set_yticks([])
    ax.spines[['top','right','left']].set_visible(False)
fig.tight_layout(h_pad=0.9)
```

The standard numerical measure is due to Karl Pearson. It measures how far the
mean has been dragged from the mode, in units of standard deviation, so the
answer is a pure number.

::: key Karl Pearson's coefficient of skewness
$$ S_k = \frac{\bar{x} - M_o}{\sigma} $$
where $M_o$ is the mode. When the mode is ill-defined, use the empirical relation
$M_o = 3M_d - 2\bar{x}$ (with $M_d$ the median) to get the second form:
$$ S_k = \frac{3(\bar{x} - M_d)}{\sigma} $$
Interpretation: $S_k > 0$ positively skewed, $S_k < 0$ negatively skewed,
$S_k = 0$ symmetric. In practice $S_k$ lies between $-3$ and $+3$.
:::

::: example Worked example 15.9
**Problem.** For a distribution, mean $= 45$, mode $= 42$ and $\sigma = 6$. Find
Karl Pearson's coefficient of skewness and state the type of skewness.

**Solution.**

$$ S_k = \frac{\bar{x} - M_o}{\sigma} = \frac{45 - 42}{6} = \frac{3}{6} = 0.5 $$

$S_k$ is positive, so the distribution is **positively skewed**: it has a longer
tail on the right-hand (higher-value) side.
:::

::: example Worked example 15.10
**Problem.** A distribution has mean $50$, median $48$ and standard deviation $12$.
Find its coefficient of skewness, and estimate the mode.

**Solution.** The mode is not given, so use the median form:

$$ S_k = \frac{3(\bar{x} - M_d)}{\sigma} = \frac{3(50 - 48)}{12} = \frac{6}{12} = 0.5 $$

From the empirical relation,

$$ M_o = 3M_d - 2\bar{x} = 3(48) - 2(50) = 144 - 100 = 44 $$

and as a check $\dfrac{\bar{x}-M_o}{\sigma} = \dfrac{50-44}{12} = 0.5$ ✔. The
distribution is positively skewed.
:::

::: example Worked example 15.11
**Problem.** Compute the mean, mode, standard deviation and Karl Pearson's
coefficient of skewness for

| Number of absences $(x)$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Number of students $(f)$ | 10 | 8 | 5 | 4 | 3 |

**Solution.** Work in one table, including a cumulative-frequency column so the
median is available too.

| $x$ | $f$ | c.f. | $fx$ | $x^{2}$ | $fx^{2}$ |
|---|---|---|---|---|---|
| 1 | 10 | 10 | 10 | 1 | 10 |
| 2 | 8 | 18 | 16 | 4 | 32 |
| 3 | 5 | 23 | 15 | 9 | 45 |
| 4 | 4 | 27 | 16 | 16 | 64 |
| 5 | 3 | 30 | 15 | 25 | 75 |
| **Total** | **$N = 30$** | | **$\sum fx = 72$** | | **$\sum fx^{2} = 226$** |

$$ \bar{x} = \frac{\sum fx}{N} = \frac{72}{30} = 2.4 $$

The **mode** is the value with the largest frequency: $M_o = 1$ (frequency $10$).

$$ \sigma^{2} = \frac{\sum fx^{2}}{N} - \bar{x}^{2} = \frac{226}{30} - (2.4)^{2} = 7.5333 - 5.76 = 1.7733 $$

$$ \sigma = \sqrt{1.7733} = 1.3317 $$

$$ S_k = \frac{\bar{x} - M_o}{\sigma} = \frac{2.4 - 1}{1.3317} = 1.05 $$

The distribution is strongly **positively skewed** — most students are absent once
or twice, with a thin tail of frequent absentees pulling the mean up.

*Cross-check with the median.* The median is the $\left(\frac{N+1}{2}\right)$th
$= 15.5$th value; the cumulative frequency reaches $18$ at $x = 2$, so $M_d = 2$.
Then $S_k = \dfrac{3(2.4-2)}{1.3317} = 0.90$ — the same sign and the same message.
The two formulas agree exactly only when the empirical relation
$M_o = 3M_d - 2\bar{x}$ holds exactly; here it gives $M_o = 6 - 4.8 = 1.2$ against
the true mode of $1$.
:::

```figure caption="The absence data of Worked example 15.11. The mode sits at the peak ($x=1$) and the long right tail pulls the mean up to $2.4$, giving $S_k = +1.05$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.7,2.7))
x=np.array([1,2,3,4,5]); f=np.array([10,8,5,4,3])
ax.bar(x,f,width=0.62,color=ACCENT,alpha=0.32,edgecolor=ACCENT,lw=1.2)
for v,lab,c,dy in [(1,'mode $=1$',SERIES[2],10.9),(2,'median $=2$',MUTED,9.6),
                   (2.4,'mean $=2.4$',SERIES[1],8.3)]:
    ax.axvline(v,color=c,lw=1.5,ls=(0,(4,2)))
    ax.annotate(lab,(v,dy),color=c,fontsize=8.6,ha='left',
                textcoords='offset points',xytext=(4,0))
ax.annotate('long right tail',(4.4,3.6),color=MUTED,fontsize=8.6,ha='center',
            xytext=(-16,26),textcoords='offset points',
            arrowprops=dict(arrowstyle='-|>',color=MUTED,lw=1.0,mutation_scale=9))
ax.set_xlabel('number of absences  $x$'); ax.set_ylabel('number of students  $f$')
ax.set_xticks(x); ax.set_xlim(0.3,5.9); ax.set_ylim(0,11.8)
ax.spines[['top','right']].set_visible(False); ax.grid(axis='y',alpha=0.45)
```

## Chapter summary

- Dispersion measures spread about the average. Range $= L-S$;
  $Q.D. = \frac{Q_3-Q_1}{2}$; $M.D. = \frac{\sum| x-\bar{x}|}{n}$.
- Variance $\sigma^{2} = \dfrac{\sum(x-\bar{x})^{2}}{n} = \dfrac{\sum x^{2}}{n} - \bar{x}^{2}$;
  standard deviation $\sigma = \sqrt{\sigma^{2}}$, in the original unit.
- Frequency data: $\bar{x} = \dfrac{\sum fx}{N}$ and
  $\sigma = \sqrt{\dfrac{\sum fx^{2}}{N} - \bar{x}^{2}}$ with $N = \sum f$.
- Grouped data (step deviation, $d' = \frac{x-A}{h}$):
  $\bar{x} = A + \dfrac{\sum fd'}{N}h$ and
  $\sigma = h\sqrt{\dfrac{\sum fd'^{2}}{N} - \left(\dfrac{\sum fd'}{N}\right)^{2}}$.
- $\sigma$ is unchanged by adding a constant and multiplied by $| k|$ when
  every value is multiplied by $k$.
- Combined SD: $\sigma_{12} = \sqrt{\dfrac{n_1(\sigma_1^{2}+d_1^{2}) + n_2(\sigma_2^{2}+d_2^{2})}{n_1+n_2}}$
  with $d_i = \bar{x}_i - \bar{x}_{12}$.
- $C.V. = \dfrac{\sigma}{\bar{x}}\times100\%$: smaller C.V. $=$ more consistent. Use it
  whenever the means or the units differ.
- Skewness measures lopsidedness: $S_k = \dfrac{\bar{x}-M_o}{\sigma} = \dfrac{3(\bar{x}-M_d)}{\sigma}$,
  with $M_o = 3M_d - 2\bar{x}$ as the empirical link.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The variance is the square of the <span class="marks">[1]</span>
   (a) mean deviation (b) standard deviation (c) quartile deviation (d) range
2. Standard deviation is independent of change of <span class="marks">[1]</span>
   (a) origin (b) scale (c) both origin and scale (d) neither
3. If every observation of a series is multiplied by $4$, the standard deviation is <span class="marks">[1]</span>
   (a) unchanged (b) multiplied by $2$ (c) multiplied by $4$ (d) multiplied by $16$
4. For a symmetric distribution, Karl Pearson's coefficient of skewness is <span class="marks">[1]</span>
   (a) $1$ (b) $0$ (c) $-1$ (d) $3$
5. Of two series with the same mean, the more consistent is the one with the <span class="marks">[1]</span>
   (a) greater range (b) greater C.V. (c) smaller C.V. (d) greater variance
6. If mean $= 30$, median $= 28$ and $\sigma = 6$, then $S_k$ equals <span class="marks">[1]</span>
   (a) $0.33$ (b) $1.00$ (c) $0.67$ (d) $2.00$

::: note Answers to Group A
**1.** (b) — by definition $\sigma^{2}$ is the variance.
**2.** (a) — shifting every value leaves all deviations $x-\bar{x}$ unchanged.
**3.** (c) — $\sigma$ scales with $| k|$; the *variance* would become $16$ times.
**4.** (b) — mean $=$ mode, so the numerator $\bar{x}-M_o$ is zero.
**5.** (c) — a smaller C.V. means less relative variation.
**6.** (b) — $S_k = 3(30-28)/6 = 1$.
:::

**Group B — Short answer (5 marks each)**

1. Define variance and standard deviation. Find the standard deviation of
   $2, 4, 6, 8, 10, 12, 14$. <span class="marks">[5]</span>
2. Calculate the mean and the standard deviation of the distribution below. <span class="marks">[5]</span>

    | $x$ | 5 | 10 | 15 | 20 | 25 |
    |---|---|---|---|---|---|
    | $f$ | 1 | 4 | 6 | 4 | 1 |

3. Find the mean, standard deviation and coefficient of variation of the
   following grouped data using the step-deviation method. <span class="marks">[5]</span>

    | Class | 0–10 | 10–20 | 20–30 | 30–40 | 40–50 |
    |---|---|---|---|---|---|
    | $f$ | 4 | 6 | 10 | 12 | 8 |

4. The mean and standard deviation of the heights of the boys in a class are
   $160$ cm and $8$ cm; for the girls they are $150$ cm and $6$ cm. State with
   reasons which group is more variable in height. <span class="marks">[5]</span>
5. For a distribution the mean is $40$, the median is $38$ and the standard
   deviation is $10$. Find the mode and Karl Pearson's coefficient of skewness by
   both formulae. <span class="marks">[5]</span>
6. A group of $30$ students has mean weight $20$ kg with $\sigma_1 = 3$ kg; another
   group of $20$ students has mean weight $25$ kg with $\sigma_2 = 4$ kg. Find the
   combined mean and the combined standard deviation. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Variance is the mean of the squared deviations from the mean;
$\sigma$ is its positive square root. Here $n = 7$, $\sum x = 56$, so $\bar{x} = 8$.

| $x$ | 2 | 4 | 6 | 8 | 10 | 12 | 14 | total |
|---|---|---|---|---|---|---|---|---|
| $d = x-8$ | $-6$ | $-4$ | $-2$ | 0 | 2 | 4 | 6 | $0$ |
| $d^{2}$ | 36 | 16 | 4 | 0 | 4 | 16 | 36 | $112$ |

$\sigma^{2} = 112/7 = 16$, so $\sigma = 4$.

**2.** $N = 16$; $\sum fx = 5+40+90+80+25 = 240$, so $\bar{x} = 240/16 = 15$.
With $d = x-15$: $fd^{2} = 1(100)+4(25)+6(0)+4(25)+1(100) = 400$.
Hence $\sigma^{2} = 400/16 = 25$ and $\sigma = 5$.

**3.** Mid-values $5,15,25,35,45$; take $A = 25$, $h = 10$, $N = 40$.

| $x$ | 5 | 15 | 25 | 35 | 45 | total |
|---|---|---|---|---|---|---|
| $f$ | 4 | 6 | 10 | 12 | 8 | $40$ |
| $d'$ | $-2$ | $-1$ | 0 | 1 | 2 | |
| $fd'$ | $-8$ | $-6$ | 0 | 12 | 16 | $14$ |
| $fd'^{2}$ | 16 | 6 | 0 | 12 | 32 | $66$ |

$\bar{x} = 25 + \frac{14}{40}(10) = 25 + 3.5 = 28.5$;
$\sigma = 10\sqrt{\frac{66}{40} - \left(\frac{14}{40}\right)^{2}} = 10\sqrt{1.65-0.1225}
= 10\sqrt{1.5275} = 12.36$; and
$C.V. = \frac{12.36}{28.5}\times100 = 43.37\%$.

**4.** The means differ, so compare coefficients of variation:
$C.V._{\text{boys}} = \frac{8}{160}\times100 = 5\%$ and
$C.V._{\text{girls}} = \frac{6}{150}\times100 = 4\%$. The boys' C.V. is larger, so
the **boys are more variable** in height, even though a quick glance at the
standard deviations only says their spread is larger in absolute centimetres.

**5.** $M_o = 3M_d - 2\bar{x} = 3(38) - 2(40) = 114 - 80 = 34$.
Then $S_k = \frac{\bar{x}-M_o}{\sigma} = \frac{40-34}{10} = 0.6$, and by the median
form $S_k = \frac{3(40-38)}{10} = 0.6$ — the two agree. Positively skewed.

**6.** $\bar{x}_{12} = \frac{30(20)+20(25)}{50} = \frac{600+500}{50} = 22$ kg.
Then $d_1 = 20-22 = -2$ and $d_2 = 25-22 = 3$, so

$$ \sigma_{12}^{2} = \frac{30(9+4) + 20(16+9)}{50} = \frac{390 + 500}{50} = \frac{890}{50} = 17.8 $$

giving $\sigma_{12} = \sqrt{17.8} = 4.22$ kg.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define standard deviation and coefficient of variation, and explain why the
   coefficient of variation is needed. <span class="marks">[2]</span>
   (b) Calculate the mean, standard deviation and coefficient of variation of the
   marks below. <span class="marks">[6]</span>

    | Marks | 0–10 | 10–20 | 20–30 | 30–40 | 40–50 |
    |---|---|---|---|---|---|
    | No. of students | 5 | 10 | 20 | 10 | 5 |

2. (a) Define skewness and state Karl Pearson's coefficient of skewness in both
   its forms, explaining how to read its sign. <span class="marks">[3]</span>
   (b) Find the mean, mode, standard deviation and coefficient of skewness of the
   distribution below. <span class="marks">[5]</span>

    | $x$ | 10 | 20 | 30 | 40 | 50 |
    |---|---|---|---|---|---|
    | $f$ | 2 | 5 | 12 | 8 | 3 |

::: note Answers to Group C
**1.** (a) $\sigma = \sqrt{\sum(x-\bar{x})^{2}/n}$ measures absolute spread in the
unit of the data; $C.V. = (\sigma/\bar{x})\times100\%$ measures it as a percentage of
the mean. The C.V. is needed because a standard deviation of, say, $500$ is large
on a mean of $1000$ but small on a mean of $50\,000$, and because two series in
different units cannot otherwise be compared.

(b) Mid-values $5,15,25,35,45$; $A = 25$, $h = 10$, $N = 50$.

| $x$ | 5 | 15 | 25 | 35 | 45 | total |
|---|---|---|---|---|---|---|
| $f$ | 5 | 10 | 20 | 10 | 5 | $50$ |
| $d'$ | $-2$ | $-1$ | 0 | 1 | 2 | |
| $fd'$ | $-10$ | $-10$ | 0 | 10 | 10 | $0$ |
| $fd'^{2}$ | 20 | 10 | 0 | 10 | 20 | $60$ |

$\bar{x} = 25 + \frac{0}{50}(10) = 25$ marks (the distribution is symmetric).

$\sigma = 10\sqrt{\frac{60}{50} - 0^{2}} = 10\sqrt{1.2} = 10(1.0954) = 10.95$ marks.

$C.V. = \frac{10.95}{25}\times100 = 43.82\%$.

**2.** (a) Skewness is the lack of symmetry of a distribution. Karl Pearson's
coefficient is $S_k = \dfrac{\bar{x}-M_o}{\sigma}$, or
$S_k = \dfrac{3(\bar{x}-M_d)}{\sigma}$ when the mode is ill-defined. A positive value
means a longer tail to the right, a negative value a longer tail to the left, and
zero means symmetry.

(b)

| $x$ | $f$ | $fx$ | $x^{2}$ | $fx^{2}$ |
|---|---|---|---|---|
| 10 | 2 | 20 | 100 | 200 |
| 20 | 5 | 100 | 400 | 2000 |
| 30 | 12 | 360 | 900 | 10800 |
| 40 | 8 | 320 | 1600 | 12800 |
| 50 | 3 | 150 | 2500 | 7500 |
| **Total** | **30** | **950** | | **33300** |

$\bar{x} = \frac{950}{30} = 31.67$; mode $M_o = 30$ (largest frequency, $12$).

$\sigma^{2} = \frac{33300}{30} - (31.67)^{2} = 1110 - 1002.78 = 107.22$, so
$\sigma = 10.35$.

$S_k = \frac{31.67-30}{10.35} = 0.16$: a slight positive skew.
:::
