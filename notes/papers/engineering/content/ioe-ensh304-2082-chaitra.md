---
file: NEBians-IOE-Past-Paper-Probability-and-Statistics-ENSH304-2082-Chaitra.pdf
subject: Probability and Statistics
level: BE · Year III / Part I
code: ENSH 304
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: BEI, BCT, BAM, BIE, BCH
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Necessary charts are attached herewith · Assume suitable data if necessary</small>

@q 1
Explain how the statistical approach helps engineers perform better in their work. [[5]]

@q 2
An assembly plant receives its voltage regulators from three different suppliers: 60% from supplier $B_1$, 30% from supplier $B_2$, and 10% from supplier $B_3$. It is known that 95% of the voltage regulators from $B_1$, 80% from $B_2$, and 65% from $B_3$ perform according to specifications. Find the probability that:

a) A randomly selected voltage regulator received by the plant performs according to specifications.

b) A voltage regulator that performs according to specifications came from supplier $B_3$. [[1+2+2]]

@q 3
An important factor in solid missile fuel is the particle size distribution. Significant problems occur if the particle sizes are too large. From production data in the past, it has been determined that the particle size (in micrometers) distribution is characterized by

$$f(x) = \begin{cases} 3x^{-4}, & x > 1 \\ 0, & \text{elsewhere.} \end{cases}$$

a) Verify that this is a valid density function.

b) What is the probability that a random particle from the manufactured fuel exceeds 4 micrometers? [[2+3]]

@q 4
Define the Binomial distribution and state its conditions. The probability that the noise level of a wideband amplifier exceeds 2 dB is 0.05. Suppose 12 such amplifiers are selected. Find the probability that:

a) Exactly one amplifier has a noise level exceeding 2 dB.

b) At most two amplifiers have noise levels exceeding 2 dB.

c) Two or more amplifiers have noise levels exceeding 2 dB. [[2+3]]

@q 5
The output voltage of a precision voltage regulator used in an electronic circuit is Normally distributed with a mean of 12 V and a standard deviation of 0.2 V. Answer the following:

a) What is the probability that the output voltage of a randomly selected regulator is less than 11.7 V?

b) What is the probability that the output voltage lies between 11.8 V and 12.3 V?

c) What is the probability that the output voltage is greater than 12.4 V? [[2+2+1]]

@or
A population consists of the five numbers 2, 4, 9, 7, 8.

a) Write down all possible samples of size three without replacement.

b) Find the sampling distribution of the sample mean.

c) Verify that the sample mean is an unbiased estimate of the population mean.

@q 6
What are the types of errors in testing of hypothesis? What steps should be followed to testing hypothesis for difference between two population proportions. [[5]]

@q 7
Samples of two types of electric bulbs were tested for length of life and the following data were obtained.

| | Type I bulb | Type II bulb |
|---|---|---|
| Sample size | 8 | 7 |
| Sample means | 1234 hrs. | 1036 hrs. |
| Sample S. D. | 36 hrs. | 40 hrs. |

Is the difference in means sufficient to warrant that type I is superior to type II regarding length of life? Test at 5% level of significance. [[5]]

@q 8
Differentiate between point estimation and interval estimation. A regular supplier to a manufacturing industry claims that only 5% of the total units of a product supplied by him are defective. To verify this claim, a random sample of 500 units was taken from one of his recent supplies, and 36 units were found to be defective. Based on this sample:

a) Construct a 95% confidence interval for the true proportion of defective units in the population.

b) Using the confidence interval obtained, comment on whether the supplier's claim that the true proportion of defective units is 5% (0.05) appears to be reasonable or supported by the sample data. [[2+2+1]]

@q 9
A survey was conducted to study the relationship between Gender and Choice of Engineering Branch. The following data were obtained. Is there association between gender and choice of branch? Test it at 5% level of significance.

| Gender/Branch | Civil | Computer | Electrical |
|---|---|---|---|
| Male | 30 | 25 | 45 |
| Female | 20 | 30 | 50 |

[[5]]

@q 10
In computer engineering, understanding the relationship between CPU utilization and power consumption is crucial for energy-efficient server design, dynamic voltage and frequency scaling (DVFS), and predictive power modeling in data centers.

| Observation | CPU Utilization (%) (X) | Power Consumption (W) (Y) |
|---|---|---|
| 1 | 10 | 85 |
| 2 | 15 | 92 |
| 3 | 25 | 110 |
| 4 | 30 | 118 |
| 5 | 40 | 135 |
| 6 | 50 | 152 |
| 7 | 60 | 168 |
| 8 | 70 | 185 |
| 9 | 80 | 202 |
| 10 | 90 | 220 |

a) Compute the Pearson's correlation coefficient $r$ between CPU utilization and power consumption. Use the formulation.

b) Draw appropriate graph to represent the relation.

c) Interpret the value of $r$ obtained in (a) and (b). What does it indicate about the linear relationship between CPU utilization and power consumption in this dataset? [[2+2+1]]

@q 11
A corporation owns several companies. The strategic planner for the corporation believes money spent on advertising can to some extent be a predictor of total sales. As an aid in long-term planning, she gathers the following sales and advertising information from several of the companies for 2009 (Rs. Millions).

| Advertising | 12.5 | 3.7 | 21.6 | 60.0 | 37.6 | 6.1 | 16.8 | 41.2 |
|---|---|---|---|---|---|---|---|---|
| Sales | 148 | 55 | 338 | 994 | 541 | 89 | 126 | 379 |

a) Develop the equation of the simple regression line to predict sales from advertising expenditures using these data.

b) Also find the standard error of estimate.

c) Comment on the value obtained in part (b). [[2+2+1]]

@q 12
The diameter (in mm) of bolts produced by a machine is measured by taking 5 samples, each of size 4. The data are:

| Sample No. | Observation |
|---|---|
| 1 | 20, 22, 21, 23 |
| 2 | 21, 20, 22, 21 |
| 3 | 23, 24, 22, 23 |
| 4 | 20, 21, 19, 22 |
| 5 | 22, 23, 21, 22 |

Construct $\bar{X}$-chart and comment on the state of statistical control. *Given: for sample size $n = 4$, $A_2 = 0.729$.* [[4+1]]
<!-- SOLUTIONS -->

@s 1
**Statistics** is the science of collecting, organising, analysing and interpreting data in order to make decisions under uncertainty. Every engineering measurement carries variation (material, machine, operator, environment), so engineers cannot rely on a single reading or on intuition. The statistical approach turns this variation into numbers that can be trusted.

| Engineering task | How statistics helps |
|---|---|
| **Collecting data** | Design of experiments and sampling plans give valid conclusions from a small, affordable number of tests instead of testing every unit. |
| **Describing data** | Mean, median, standard deviation, histograms and box plots summarise thousands of readings in a few numbers and pictures. |
| **Quality control** | Control charts ($\bar X$, $R$, $p$) detect a drifting process early; acceptance sampling decides whether to accept or reject a lot. |
| **Reliability and life testing** | Exponential and Weibull models predict failure rates, warranty periods and maintenance schedules. |
| **Decision making** | Hypothesis tests decide between two designs, suppliers or materials with a stated risk of error ($\alpha$, $\beta$). |
| **Estimation** | Confidence intervals give a range for a mean, proportion or defect rate, not just a point value. |
| **Relationships and prediction** | Correlation and regression relate load to deflection, CPU load to power, advertising to sales, and predict unseen cases. |
| **Risk and design** | Probability models (binomial, Poisson, normal) give the chance of overload, signal error or system failure, so safety factors are chosen rationally. |
| **Optimisation** | Analysis of variance and response-surface methods find the setting of temperature, speed or mix that gives the best output. |

**Result.** Using statistics, engineers (i) reduce waste and rework, (ii) make products consistent and reliable, (iii) compare alternatives objectively, (iv) justify decisions with data and (v) quantify the risk of being wrong. That is why "the statistical approach helps engineers perform better in their work".

@s 2
Let $S$ = "regulator performs according to specification".

$P(B_1)=0.60,\; P(B_2)=0.30,\; P(B_3)=0.10$ and $P(S|B_1)=0.95,\; P(S|B_2)=0.80,\; P(S|B_3)=0.65$.

**(a) Total probability.**

$$\begin{aligned}P(S) &= \sum_{i=1}^{3}P(B_i)P(S|B_i)\\ &= 0.60(0.95) + 0.30(0.80) + 0.10(0.65)\\ &= 0.570 + 0.240 + 0.065\end{aligned}$$

$$\boxed{P(S) = 0.875}$$

**(b) Bayes' theorem.**

$$P(B_3|S) = \frac{P(B_3)\,P(S|B_3)}{P(S)} = \frac{0.065}{0.875}$$

$$\boxed{P(B_3|S) = 0.0743}$$

About $7.4\%$ of the good regulators come from supplier $B_3$, close to its $10\%$ share of supply but a little less, because $B_3$ has the worst performance.

@s 3
**(a) Validity.** A function is a pdf if $f(x)\ge0$ for all $x$ and $\int_{-\infty}^{\infty}f(x)\,dx = 1$.

For $x>1$, $3x^{-4}>0$, and $f=0$ elsewhere, so $f(x)\ge0$ everywhere. Now

$$\int_{-\infty}^{\infty}f(x)\,dx = \int_1^{\infty}3x^{-4}\,dx = 3\left[\frac{x^{-3}}{-3}\right]_1^{\infty} = \left[-x^{-3}\right]_1^{\infty} = 0 - (-1) = 1.$$

Both conditions hold, so $f(x)$ **is a valid density function**.

**(b)**

$$P(X>4) = \int_4^{\infty}3x^{-4}\,dx = \left[-x^{-3}\right]_4^{\infty} = 4^{-3} = \frac{1}{64}$$

$$\boxed{P(X>4) = 0.015625 \approx 1.56\%}$$

@s 4
**Binomial distribution.** A discrete random variable $X$, the number of successes in $n$ trials, follows the binomial distribution $X\sim B(n,p)$ with

$$\begin{gathered}P(X=x) = \binom{n}{x}p^{x}q^{\,n-x} \\ x = 0,1,\dots,n,\quad q = 1-p.\end{gathered}$$

Its mean is $np$ and its variance is $npq$.

**Conditions**

1. The number of trials $n$ is fixed in advance.
2. Each trial has only two outcomes, success and failure.
3. The trials are independent.
4. The probability of success $p$ is the same in every trial.

**Here** $n = 12$, $p = 0.05$ (a noise level above 2 dB is the "success"), $q = 0.95$.

**(a) Exactly one**

$$P(X=1) = \binom{12}{1}(0.05)(0.95)^{11} = 12(0.05)(0.5688) = 0.3413$$

$$\boxed{P(X=1) = 0.3413}$$

**(b) At most two**

$$\begin{aligned}P(X=0) &= (0.95)^{12} = 0.5404\\ P(X=1) &= 0.3413\\ P(X=2) &= \binom{12}{2}(0.05)^2(0.95)^{10} = 66(0.0025)(0.5987) = 0.0988\end{aligned}$$

$$P(X\le2) = 0.5404 + 0.3413 + 0.0988$$

$$\boxed{P(X\le 2) = 0.9804}$$

**(c) Two or more**

$$P(X\ge2) = 1 - P(X\le1) = 1 - (0.5404 + 0.3413)$$

$$\boxed{P(X\ge 2) = 0.1184}$$

@s 5
$X\sim N(\mu = 12,\ \sigma = 0.2)$ and $Z = (X-12)/0.2$.

**(a)**

$$P(X<11.7) = P\left(Z<\frac{11.7-12}{0.2}\right) = P(Z<-1.5) = 0.0668$$

**(b)**

$$P(11.8<X<12.3) = P(-1<Z<1.5) = \Phi(1.5)-\Phi(-1) = 0.9332 - 0.1587$$

$$\boxed{P = 0.7745}$$

**(c)**

$$P(X>12.4) = P\left(Z>\frac{12.4-12}{0.2}\right) = P(Z>2) = 1-0.9772 = 0.0228$$

**Answers:** (a) $0.0668$, (b) $0.7745$, (c) $0.0228$.

```figure caption="The three areas under the N(12, 0.2) curve: (a) X < 11.7 (6.68%), (b) 11.8 < X < 12.3 (77.45%), (c) X > 12.4 (2.28%)."
import numpy as np, matplotlib.pyplot as plt
x=np.linspace(11.3,12.7,400); y=np.exp(-(x-12)**2/(2*0.2**2))/(0.2*np.sqrt(2*np.pi))
fig,axs=plt.subplots(1,3,figsize=(6.6,2.0),sharey=True)
cases=[(x<11.7,"(a) $X<11.7$\nP = 0.0668"),((x>11.8)&(x<12.3),"(b) $11.8<X<12.3$\nP = 0.7745"),(x>12.4,"(c) $X>12.4$\nP = 0.0228")]
for ax,(m,t) in zip(axs,cases):
    ax.plot(x,y,color=INK,lw=1.2); ax.fill_between(x,y,where=m,color=ACCENT,alpha=.45)
    ax.set_title(t,fontsize=7.5); ax.set_xticks([11.4,12,12.6]); ax.tick_params(labelsize=7); ax.set_xlabel("output voltage (V)",fontsize=7)
axs[0].set_ylabel("density",fontsize=7)
```

**OR**

Population: $\{2,4,9,7,8\}$, $N = 5$, sample size $n = 3$ without replacement.

**(a) All samples.** The number of samples is $\binom{5}{3} = 10$.

| No. | Sample | Sum | Sample mean $\bar x$ |
|---|---|---|---|
| 1 | 2, 4, 9 | 15 | $5$ |
| 2 | 2, 4, 7 | 13 | $13/3 = 4.333$ |
| 3 | 2, 4, 8 | 14 | $14/3 = 4.667$ |
| 4 | 2, 9, 7 | 18 | $6$ |
| 5 | 2, 9, 8 | 19 | $19/3 = 6.333$ |
| 6 | 2, 7, 8 | 17 | $17/3 = 5.667$ |
| 7 | 4, 9, 7 | 20 | $20/3 = 6.667$ |
| 8 | 4, 9, 8 | 21 | $7$ |
| 9 | 4, 7, 8 | 19 | $19/3 = 6.333$ |
| 10 | 9, 7, 8 | 24 | $8$ |

**(b) Sampling distribution of $\bar x$.** Each sample has probability $1/10$.

| $\bar x$ | $13/3$ | $14/3$ | $5$ | $17/3$ | $6$ | $19/3$ | $20/3$ | $7$ | $8$ | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| $f$ | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 10 |
| $P(\bar x)$ | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.2 | 0.1 | 0.1 | 0.1 | 1 |

**(c) Unbiasedness.** Population mean

$$\mu = \frac{2+4+9+7+8}{5} = \frac{30}{5} = 6.$$

Mean of the sampling distribution

$$E(\bar x) = \frac{\sum \text{(sample sums)}/3}{10} = \frac{15+13+14+18+19+17+20+21+19+24}{3\times10} = \frac{180}{30} = 6.$$

$$\boxed{E(\bar x) = 6 = \mu}$$

So the sample mean is an **unbiased estimator** of the population mean.

*Extra check.* $\sigma^2 = \frac{16+4+9+1+4}{5} = 6.8$. The variance of $\bar x$ computed from the ten means is $1.1333$, and the finite-population formula gives $\frac{\sigma^2}{n}\cdot\frac{N-n}{N-1} = \frac{6.8}{3}\cdot\frac{2}{4} = 1.1333$. They agree.

@s 6
**Types of errors**

| Decision \ Truth | $H_0$ true | $H_0$ false |
|---|---|---|
| Reject $H_0$ | **Type I error** (probability $\alpha$) | Correct (power $1-\beta$) |
| Accept $H_0$ | Correct ($1-\alpha$) | **Type II error** (probability $\beta$) |

- **Type I error:** rejecting a true null hypothesis. $P = \alpha$, the level of significance (usually 5% or 1%).
- **Type II error:** accepting (failing to reject) a false null hypothesis. $P = \beta$.
- For a fixed sample size, decreasing $\alpha$ increases $\beta$; both fall only when the sample size is increased.

**Steps for testing the difference between two population proportions** (large samples).

Let $x_1$ and $x_2$ be the numbers of successes in independent samples of sizes $n_1$ and $n_2$, so $\hat p_1 = x_1/n_1$ and $\hat p_2 = x_2/n_2$.

1. **State the hypotheses.** $H_0: p_1 = p_2$ against $H_1: p_1 \ne p_2$ (two-tailed), or $p_1 > p_2$ / $p_1 < p_2$ (one-tailed).
2. **Choose the level of significance** $\alpha$ (for example $0.05$).
3. **Choose the test statistic.** For large $n_1, n_2$ (each $n\hat p$ and $n\hat q$ at least 5), use the normal $Z$ test. Under $H_0$ both proportions have the common estimate (pooled proportion)

$$\begin{gathered}\hat p = \frac{x_1+x_2}{n_1+n_2} \\ \hat q = 1-\hat p.\end{gathered}$$

4. **Compute the statistic**

$$Z = \frac{\hat p_1 - \hat p_2}{\sqrt{\hat p\hat q\left(\dfrac{1}{n_1}+\dfrac{1}{n_2}\right)}}\ \sim N(0,1).$$

5. **Find the critical region.** Two-tailed: $|Z| > z_{\alpha/2}$ ($1.96$ at 5%). One-tailed: $Z > z_\alpha$ or $Z < -z_\alpha$ ($1.645$ at 5%).
6. **Decide.** If $Z$ falls in the critical region, reject $H_0$ (the proportions differ significantly); otherwise do not reject $H_0$.
7. **Conclude** in words about the problem (for example "the defect rates of the two machines differ").

@s 7
$n_1 = 8,\ \bar x_1 = 1234,\ s_1 = 36$; $n_2 = 7,\ \bar x_2 = 1036,\ s_2 = 40$. Sample standard deviations of small samples, population variances unknown, so a $t$-test is used. The two sample variances are close ($F = 40^2/36^2 = 1.23$, well below the 5% critical value $3.87$ of $F_{6,7}$), so equal population variances are assumed (pooled test).

1. $H_0: \mu_1 = \mu_2$ (no difference in life). $H_1: \mu_1 > \mu_2$ (type I is superior). One-tailed.
2. $\alpha = 0.05$.
3. Pooled variance

$$s_p^2 = \frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2} = \frac{7(1296) + 6(1600)}{13} = \frac{18672}{13} = 1436.31$$

$$s_p = 37.90$$

4. Test statistic

$$t = \frac{\bar x_1-\bar x_2}{s_p\sqrt{\frac{1}{n_1}+\frac{1}{n_2}}} = \frac{1234-1036}{37.90\sqrt{\frac18+\frac17}} = \frac{198}{37.90(0.5175)} = \frac{198}{19.61}$$

$$\boxed{t = 10.09}$$

5. Degrees of freedom $= 8+7-2 = 13$. One-tailed critical value $t_{0.05,13} = 1.771$.
6. Since $t = 10.09 > 1.771$, we **reject $H_0$** (the $p$-value is about $10^{-7}$).

**Conclusion.** The difference of $198$ hours is highly significant. At the 5% level, type I bulbs are superior to type II bulbs in length of life.

@s 8
**Point vs interval estimation**

| Point estimation | Interval estimation |
|---|---|
| A single number computed from the sample is used as the estimate of the parameter, for example $\hat p = x/n$. | A range of values $(L, U)$ is given that contains the parameter with a stated confidence $(1-\alpha)$. |
| Gives no idea of the error or reliability. | Shows the precision through the width of the interval. |
| Probability that it equals the true value is essentially zero. | Confidence level such as 95% describes the long-run proportion of intervals that contain the parameter. |
| Example: $\bar x = 1234$ h. | Example: $1234 \pm 30$ h with 95% confidence. |

**(a)** $n = 500$, $x = 36$.

$$\begin{gathered}\hat p = \frac{36}{500} = 0.072 \\ \hat q = 0.928\end{gathered}$$

$$SE = \sqrt{\frac{\hat p\hat q}{n}} = \sqrt{\frac{0.072(0.928)}{500}} = \sqrt{0.00013363} = 0.01156$$

For 95% confidence $z_{0.025} = 1.96$:

$$\text{margin} = 1.96(0.01156) = 0.02266$$

$$p = 0.072 \pm 0.02266 \;\Rightarrow\; \boxed{0.0493 < p < 0.0947}$$

**(b)** The claimed value $0.05$ lies inside the interval $(0.0493,\ 0.0947)$, so at the 95% level the sample **does not contradict** the supplier's claim; the claim of 5% defective is statistically plausible.

*Remark.* The claimed value sits only just inside the lower limit and the sample estimate is $7.2\%$. If one tests $H_0: p = 0.05$ directly with the standard error under $H_0$, $z = \dfrac{0.072-0.05}{\sqrt{0.05(0.95)/500}} = 2.26 > 1.96$, which would reject the claim at 5%. So the claim is only weakly supported, and a larger sample or a closer inspection of the supply is advisable. By the interval method asked in the question, the answer is that the claim appears reasonable.

@s 9
**Chi-square test of independence.**

1. $H_0$: gender and choice of branch are independent (no association). $H_1$: they are associated.
2. $\alpha = 0.05$.
3. Totals: rows male $100$, female $100$; columns Civil $50$, Computer $55$, Electrical $95$; grand total $N = 200$.

Expected frequency $E = \dfrac{\text{row total}\times\text{column total}}{N}$:

| | Civil | Computer | Electrical |
|---|---|---|---|
| Male | $\frac{100\cdot50}{200} = 25$ | $\frac{100\cdot55}{200} = 27.5$ | $\frac{100\cdot95}{200} = 47.5$ |
| Female | $25$ | $27.5$ | $47.5$ |

4. Test statistic $\chi^2 = \sum\dfrac{(O-E)^2}{E}$:

| Cell | $O$ | $E$ | $(O-E)^2/E$ |
|---|---|---|---|
| Male, Civil | 30 | 25 | 1.0000 |
| Male, Computer | 25 | 27.5 | 0.2273 |
| Male, Electrical | 45 | 47.5 | 0.1316 |
| Female, Civil | 20 | 25 | 1.0000 |
| Female, Computer | 30 | 27.5 | 0.2273 |
| Female, Electrical | 50 | 47.5 | 0.1316 |
| | | **Total** | $\chi^2 = 2.7177$ |

5. Degrees of freedom $= (2-1)(3-1) = 2$. Critical value $\chi^2_{0.05,2} = 5.991$.
6. Since $2.718 < 5.991$ (the $p$-value is $0.257$), we **fail to reject $H_0$**.

**Conclusion.** At the 5% level there is no significant association between gender and the choice of engineering branch; the two attributes are independent on this evidence.

@s 10
$n = 10$. Sums: $\sum x = 470$, $\sum y = 1467$, $\sum xy = 80510$, $\sum x^2 = 28950$, $\sum y^2 = 234695$.

| $X$ | 10 | 15 | 25 | 30 | 40 | 50 | 60 | 70 | 80 | 90 |
|---|---|---|---|---|---|---|---|---|---|---|
| $Y$ | 85 | 92 | 110 | 118 | 135 | 152 | 168 | 185 | 202 | 220 |
| $XY$ | 850 | 1380 | 2750 | 3540 | 5400 | 7600 | 10080 | 12950 | 16160 | 19800 |

**(a) Pearson's coefficient**

$$r = \frac{n\sum xy - \sum x\sum y}{\sqrt{\left[n\sum x^2 - (\sum x)^2\right]\left[n\sum y^2 - (\sum y)^2\right]}}$$

$$\begin{aligned}n\sum xy - \sum x\sum y &= 805100 - 689490 = 115610\\ n\sum x^2 - (\sum x)^2 &= 289500 - 220900 = 68600\\ n\sum y^2 - (\sum y)^2 &= 2346950 - 2152089 = 194861\end{aligned}$$

$$r = \frac{115610}{\sqrt{68600\times194861}} = \frac{115610}{115617.4}$$

$$\boxed{r = 0.9999}$$

**(b) Scatter diagram.** The least-squares line is $\hat y = 67.49 + 1.685\,x$.

```figure caption="Scatter diagram of power consumption against CPU utilization with the least-squares line y = 67.49 + 1.685 x (r = 0.9999)."
import numpy as np, matplotlib.pyplot as plt
x=np.array([10,15,25,30,40,50,60,70,80,90]); y=np.array([85,92,110,118,135,152,168,185,202,220])
b,a=np.polyfit(x,y,1)
fig,ax=plt.subplots(figsize=(5.2,2.9))
ax.plot(x,y,'o',color=ACCENT,ms=5,label="observations")
xs=np.array([0,100]); ax.plot(xs,a+b*xs,color=SERIES[1],lw=1.3,label="$\\hat y = 67.49 + 1.685x$")
ax.set_xlabel("CPU utilization X (%)"); ax.set_ylabel("power consumption Y (W)"); ax.set_xlim(0,100); ax.set_ylim(60,240)
ax.grid(True); ax.legend(fontsize=7,loc="upper left")
```

**(c) Interpretation.** $r = +0.9999$ is almost exactly $+1$:

- **Direction:** positive, so power consumption rises as CPU utilization rises.
- **Strength:** an almost perfect linear relationship; the points lie practically on a straight line, as the scatter diagram confirms. The coefficient of determination is $r^2 = 0.9999$, so about $99.99\%$ of the variation in power is explained by CPU utilization.
- **Slope:** each extra $1\%$ of CPU load adds about $1.69$ W, and the intercept $67.5$ W is the idle power at $0\%$ load.

This supports linear power models used in DVFS and in data-centre power prediction. (Correlation shows association, not by itself causation, though here the physical cause is clear: more switching activity draws more power.)

@s 11
$n = 8$, $x$ = advertising, $y$ = sales. Sums: $\sum x = 199.5$, $\sum y = 2670$, $\sum xy = 107610.4$, $\sum x^2 = 7667.15$, $\sum y^2 = 1587328$.

$$\begin{gathered}\bar x = 24.9375 \\ \bar y = 333.75\end{gathered}$$

**(a) Regression of sales on advertising** $\hat y = b_0 + b_1x$.

$$\begin{aligned}S_{xx} &= \sum x^2 - \frac{(\sum x)^2}{n} = 7667.15 - 4975.03 = 2692.12\\ S_{xy} &= \sum xy - \frac{\sum x\sum y}{n} = 107610.4 - 66584.4 = 41026.0\end{aligned}$$

$$b_1 = \frac{S_{xy}}{S_{xx}} = \frac{41026.0}{2692.12} = 15.240$$

$$b_0 = \bar y - b_1\bar x = 333.75 - 15.240(24.9375) = -46.29$$

$$\boxed{\hat y = -46.29 + 15.24\,x}$$

Each additional Rs. 1 million of advertising is associated with about Rs. 15.24 million of extra sales.

**(b) Standard error of estimate.**

$$S_{yy} = 1587328 - \frac{2670^2}{8} = 1587328 - 891112.5 = 696215.5$$

$$SSE = S_{yy} - b_1S_{xy} = 696215.5 - 15.2398(41026.0) = 70969.2$$

$$s_e = \sqrt{\frac{SSE}{n-2}} = \sqrt{\frac{70969.2}{6}} = \sqrt{11828.2}$$

$$\boxed{s_e = 108.76\ \text{(Rs. millions)}}$$

(The fitted values are $144.2,\ 10.1,\ 282.9,\ 868.0,\ 526.6,\ 46.7,\ 209.7,\ 581.6$ against the observed $148, 55, 338, 994, 541, 89, 126, 379$.)

```figure caption="Advertising expenditure against sales with the fitted line y = -46.29 + 15.24 x. The scatter about the line has standard error 108.76."
import numpy as np, matplotlib.pyplot as plt
x=np.array([12.5,3.7,21.6,60.0,37.6,6.1,16.8,41.2]); y=np.array([148,55,338,994,541,89,126,379])
fig,ax=plt.subplots(figsize=(5.2,2.8))
ax.plot(x,y,'o',color=ACCENT,ms=5,label="companies")
xs=np.array([0,65]); ax.plot(xs,-46.29+15.24*xs,color=SERIES[1],lw=1.3,label="$\\hat y=-46.29+15.24x$")
ax.set_xlabel("advertising (Rs. million)"); ax.set_ylabel("sales (Rs. million)"); ax.grid(True); ax.legend(fontsize=7,loc="upper left")
```

**(c) Comment.** The standard error $s_e \approx 108.8$ million is the typical (root-mean-square) distance of the actual sales from the regression line, in the same units as sales. Relative to the mean sales of $333.75$ million this is about $33\%$, so predictions are only moderately precise: a predicted value should be quoted as about $\pm 2s_e \approx \pm 218$ million at roughly 95%. The line still explains most of the variation ($r^2 = 0.898$, $r = 0.948$), so advertising is a good, but not perfect, predictor of sales; the scatter is larger for the big companies, and with only 8 points the estimate is rough. (Dividing by $n$ instead of $n-2$ would give $94.2$, but the unbiased standard error uses $n-2$.)

@s 12
$n = 4$ per sample, $k = 5$ samples, $A_2 = 0.729$.

| Sample | Observations | $\bar x$ | Range $R$ |
|---|---|---|---|
| 1 | 20, 22, 21, 23 | 21.5 | 3 |
| 2 | 21, 20, 22, 21 | 21.0 | 2 |
| 3 | 23, 24, 22, 23 | 23.0 | 2 |
| 4 | 20, 21, 19, 22 | 20.5 | 3 |
| 5 | 22, 23, 21, 22 | 22.0 | 2 |

$$\begin{gathered}\bar{\bar x} = \frac{21.5+21.0+23.0+20.5+22.0}{5} = \frac{108}{5} = 21.6 \\ \bar R = \frac{3+2+2+3+2}{5} = 2.4\end{gathered}$$

**Control limits of the $\bar X$-chart**

$$CL = \bar{\bar x} = 21.6$$

$$UCL = \bar{\bar x} + A_2\bar R = 21.6 + 0.729(2.4) = 21.6 + 1.750$$

$$\boxed{UCL = 23.35}$$

$$LCL = \bar{\bar x} - A_2\bar R = 21.6 - 1.750$$

$$\boxed{LCL = 19.85}$$

```figure caption="X-bar chart of bolt diameter: CL = 21.6 mm, UCL = 23.35 mm, LCL = 19.85 mm. All five sample means lie inside the limits."
import numpy as np, matplotlib.pyplot as plt
m=np.array([21.5,21.0,23.0,20.5,22.0]); k=np.arange(1,6)
fig,ax=plt.subplots(figsize=(5.2,2.6))
ax.plot(k,m,'o-',color=ACCENT)
ax.axhline(21.6,color=INK,lw=1); ax.axhline(23.35,color=SERIES[1],ls='--'); ax.axhline(19.85,color=SERIES[1],ls='--')
ax.text(5.15,23.35,"UCL 23.35",fontsize=7,va='center'); ax.text(5.15,21.6,"CL 21.6",fontsize=7,va='center'); ax.text(5.15,19.85,"LCL 19.85",fontsize=7,va='center')
ax.set_xlim(0.6,6.2); ax.set_ylim(19,24.2); ax.set_xticks(k); ax.set_xlabel("sample number"); ax.set_ylabel("sample mean (mm)"); ax.grid(True)
```

**Comment.** The sample means $21.5,\ 21.0,\ 23.0,\ 20.5,\ 22.0$ all lie between $LCL = 19.85$ and $UCL = 23.35$, and there is no run or trend pattern. Sample 3 ($23.0$) is the closest to the upper limit and sample 4 ($20.5$) is the lowest, but both are inside.

$$\boxed{\text{The process mean is in statistical control}}$$

(With only five subgroups the limits are provisional; the range chart should also be plotted, and the limits revised as more samples are collected.)
