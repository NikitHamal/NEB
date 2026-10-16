---
subject: Mathematics
grade: 8
title: Statistics
unit: 21
hours: 0
area: Compulsory Mathematics
---

Statistics is how a large number of facts is turned into a few sentences. Two
hundred marks become one average; a week of temperature readings become a line on
a graph; fifty households become a pie chart. This chapter covers the three
averages — mean, median and mode — and the two pictures, the bar graph and the
pie chart, that a reader can take in at a glance.

::: key What this chapter asks of you
You should be able to collect, tally and tabulate data, draw and read a bar
graph, draw a pie chart by converting frequencies into angles, and find the
mean, the median and the mode of an individual series and say when each is the
most useful average.
:::

## 21.1 Collecting and tabulating data

**Data** are facts or numbers collected for a purpose. **Statistics** is the
science of collecting, organising, presenting and interpreting them.

**Method.**

1. Decide exactly what you want to find out and write the question down.
2. Collect the data — by counting, measuring, asking, or reading a record.
3. Tally it as you go, in groups of five.
4. Make a frequency table with a total row, and check the total against the
   number of observations.
5. Present it as a table, a bar graph or a pie chart.
6. Interpret: say in words what the table shows.

| Marks | Tally | Frequency |
|---|---|---|
| 0–20 | II | 2 |
| 20–40 | IIII I | 6 |
| 40–60 | IIII IIII I | 11 |
| 60–80 | IIII III | 8 |
| 80–100 | III | 3 |
| **Total** | | **30** |

::: caution The frequency must add up
Before doing anything with a frequency table, add the frequencies and compare
with the number of observations. A total that does not match means a miscount,
and every average and every angle calculated from it will be wrong. In the table
above, $2+6+11+8+3=30$ ✓.
:::

## 21.2 Pictographs, bar graphs and pie charts

### 21.2.1 Bar graph

A **bar graph** shows the frequency of each value or class as a bar whose height
is proportional to the frequency. Bars are of equal width and are separated by
equal gaps.

```figure caption="A bar graph of the frequency table above. The height of each bar reads the frequency directly, which is why a bar graph is the quickest way to compare classes."
fig, ax = plt.subplots(figsize=(4.9, 2.6))
labels = ["0-20", "20-40", "40-60", "60-80", "80-100"]
vals = [2, 6, 11, 8, 3]
bars = ax.bar(labels, vals, color=[MUTED, MUTED, ACCENT, MUTED, MUTED], width=0.62)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.25, str(v), ha="center",
            fontsize=7.5, color=INK)
ax.set_ylabel("number of students", fontsize=8)
ax.set_xlabel("marks", fontsize=8)
ax.set_ylim(0, 13)
ax.tick_params(labelsize=7.5, length=0)
ax.spines[["top", "right"]].set_visible(False)
ax.yaxis.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

### 21.2.2 Pie chart

A **pie chart** shows each frequency as a slice of a circle. The whole circle is
360°, so the angle of a slice is

$$\text{angle}=\frac{\text{frequency}}{\text{total}}\times360°$$

```figure caption="A pie chart of the same data. The slice angle is proportional to the frequency, so the largest class takes the largest angle."
fig, ax = plt.subplots(figsize=(4.6, 2.8))
labels = ["0-20", "20-40", "40-60", "60-80", "80-100"]
vals = [2, 6, 11, 8, 3]
colors = [MUTED, SERIES[0], ACCENT, SERIES[1], SERIES[2]]
ax.pie(vals, labels=labels, colors=colors, autopct="%1.0f%%", startangle=90,
       textprops=dict(fontsize=7.0, color=INK), wedgeprops=dict(lw=0.8, ec="white"))
ax.set_aspect("equal")
fig.tight_layout()
```

::: example A pie chart from a table
**Problem.** In a class of 40 students, 12 come on foot, 10 by bicycle, 14 by
bus and 4 by other means. Draw a pie chart.

**Solution.** Total $=40$, so each student is $\frac{360}{40}=9°$.

| Means | Frequency | Angle |
|---|---|---|
| On foot | 12 | $12\times9=108°$ |
| Bicycle | 10 | $10\times9=90°$ |
| Bus | 14 | $14\times9=126°$ |
| Other | 4 | $4\times9=36°$ |
| **Total** | **40** | **360°** |

Draw a circle, mark a radius, and lay off the angles in order with a protractor.

**Answer.** As in the table.

**Check.** $108+90+126+36=360$ ✓ — the angles of a pie chart must close the
circle exactly. A total that is not 360° means an arithmetic slip somewhere.
:::

::: example Reading a pie chart
**Problem.** A pie chart shows household spending: food 144°, rent 90°, school
72°, and the rest as savings. If the monthly income is Rs 20,000, find the
amount spent on food and the amount saved.

**Solution.** The savings angle is

$$360-(144+90+72)=360-306=54°$$

Food: $\frac{144}{360}\times20\,000=\text{Rs }8000$.

Savings: $\frac{54}{360}\times20\,000=\text{Rs }3000$.

**Answer.** Food Rs 8,000; savings Rs 3,000.

**Check.** Rent is $\frac{90}{360}\times20\,000=\text{Rs }5000$ and school is
$\frac{72}{360}\times20\,000=\text{Rs }4000$; the four amounts add to
$8000+5000+4000+3000=\text{Rs }20\,000$ ✓.
:::

## 21.3 Mean, median and mode

For an **individual series** — a plain list of values, without frequencies:

| Average | Definition | How to find it |
|---|---|---|
| Mean | the sum of all the values divided by how many there are | $\bar x=\frac{\sum x}{n}$ |
| Median | the middle value when the values are arranged in order | odd $n$: the $\frac{n+1}{2}$th value; even $n$: the mean of the two middle values |
| Mode | the value that occurs most often | count the repeats |

```figure caption="The three averages on one set of data: 2, 3, 3, 5, 12. The mean is pulled up by the 12, the median sits in the middle of the ordered list, and the mode is the value that repeats."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0, 2.5))
data = [2, 3, 3, 5, 12]
ax.plot([0, 14], [1.0, 1.0], color=INK, lw=1.4)
for v in data:
    ax.plot([v], [1.0], "o", color=ACCENT, ms=6)
mean = sum(data) / len(data)
med = sorted(data)[len(data) // 2]
for v, name, c, y in [(mean, "mean 5", SERIES[1], 1.5), (med, "median 3", SERIES[2], 1.9),
                      (3, "mode 3", SERIES[3], 2.3)]:
    ax.plot([v, v], [1.0, y - 0.08], color=c, lw=1.2, ls="--")
    ax.text(v, y, name, ha="center", fontsize=7.0, color=c)
for v in data:
    ax.text(v, 0.75, str(v), ha="center", fontsize=7.0, color=INK)
ax.set_xlim(-0.5, 14)
ax.set_ylim(0.4, 2.7)
ax.axis("off")
ax.text(7, 0.45, "mean = sum/number = 25/5", ha="center", fontsize=6.6, color=MUTED)
fig.tight_layout()
```

::: example The three averages
**Problem.** Find the mean, median and mode of the data
2, 3, 3, 5, 12.

**Solution.** **Mean.**
$\bar x=\frac{2+3+3+5+12}{5}=\frac{25}{5}=5$.

**Median.** Arrange in order (already ordered): 2, 3, 3, 5, 12. With $n=5$ the
median is the $\frac{5+1}{2}=3$rd value, which is **3**.

**Mode.** The value that appears most often is **3** (twice).

**Answer.** Mean 5, median 3, mode 3.

**What it shows.** Four of the five values are 5 or less, and yet the mean is 5
because the single value 12 pulls it up. The median is not affected by how large
the largest value is — which is why house prices and salaries are usually
reported as medians. This is the meaning of an **outlier**.
:::

::: example An even number of values
**Problem.** Find the median of 8, 4, 6, 10, 3, 7.

**Solution.** Arrange in order: 3, 4, 6, 7, 8, 10. With $n=6$ (even) the median
is the mean of the 3rd and 4th values:

$$\frac{6+7}{2}=6.5$$

**Answer.** 6.5.

**Check.** Three values lie below 6.5 and three above ✓. Note that the median
need not be one of the data values.
:::

::: example Choosing the best average
**Problem.** The monthly salaries in a small office are Rs 18,000, Rs 18,000,
Rs 20,000, Rs 22,000 and Rs 150,000. Which average best describes a typical
salary, and why?

**Solution.** Mean
$=\frac{18\,000+18\,000+20\,000+22\,000+150\,000}{5}
=\frac{228\,000}{5}=\text{Rs }45\,600$.
Median $=$ Rs 20,000 (the third of five ordered values).
Mode $=$ Rs 18,000.

The **median** is the honest description: four of the five people earn Rs 22,000
or less, and the mean of Rs 45,600 describes nobody, because it has been pulled
up by the one very large salary.

**Check.** The median lies in the middle of the ordered list, with two salaries
below and two above ✓.
:::

::: caution The mean is not always the fairest summary
The mean uses every value, which is usually an advantage — but one extreme value
can move it a long way. Whenever a set contains an outlier, report the median as
well, and say which one you are using and why.
:::

### 21.3.1 A frequency table with classes

When the data are grouped into classes, use the **mid-value** of each class as
the representative value.

| Class | Mid-value $m$ | Frequency $f$ | $fm$ |
|---|---|---|---|
| 0–20 | 10 | 2 | 20 |
| 20–40 | 30 | 6 | 180 |
| 40–60 | 50 | 11 | 550 |
| 60–80 | 70 | 8 | 560 |
| 80–100 | 90 | 3 | 270 |
| **Total** | | **30** | **1580** |

$$\bar x=\frac{\sum fm}{\sum f}=\frac{1580}{30}\approx52.67$$

The **modal class** is the class with the highest frequency — here 40–60 — and
for a grouped table that is what "mode" means. The median class is the class in
which the $\frac{n+1}{2}$th value falls; here $\frac{31}{2}=15.5$, and the
cumulative frequencies (2, 8, 19, …) show that the 15.5th value lies in the
class 40–60.

## 21.5 Choosing the right average

Mean, median and mode answer different questions. The examiner often asks
**which** average is suitable, and that is a reasoning mark.

| Average | Best when | Weakness |
|---|---|---|
| Mean | the data are evenly spread and every value matters | one extreme value drags it |
| Median | there is an extreme value (income, land size) | ignores the size of the other values |
| Mode | the data are categories (shoe size, favourite subject) | may not exist, or there may be several |

```figure caption="One extreme value moves the mean but not the median. Five daily wages of Rs 500–700 and one of Rs 5,000 give a mean nobody earns."
wages = [500, 550, 600, 650, 700, 5000]
mean = sum(wages) / len(wages)
med = (600 + 650) / 2
fig, ax = plt.subplots(figsize=(5.4, 2.6))
ax.scatter(wages, [1] * len(wages), s=70, color=SERIES[0], zorder=3)
ax.axvline(mean, color=SERIES[1], linewidth=1.6,
           label=f"mean = Rs {mean:,.0f}")
ax.axvline(med, color=SERIES[2], linewidth=1.6,
           label=f"median = Rs {med:,.0f}")
ax.set_yticks([])
ax.set_xlabel("daily wage (Rs)", color=MUTED)
ax.legend(fontsize=8, frameon=False, loc="upper center")
ax.set_ylim(0.6, 1.8)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.grid(axis="x", color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
ax.tick_params(colors=MUTED)
```

::: example Mean from a frequency table, step by step
**Question.** The marks of 50 students are: $0$–$10$: 4, $10$–$20$: 8,
$20$–$30$: 14, $30$–$40$: 16, $40$–$50$: 8. Find the mean mark and name the
modal class.

**Answer.** Mid-values: 5, 15, 25, 35, 45.
$\sum fx = 4(5) + 8(15) + 14(25) + 16(35) + 8(45)
= 20 + 120 + 350 + 560 + 360 = 1410$.
Mean $= \frac{1410}{50} = \textbf{28.2 marks}$.
The highest frequency is 16, so the **modal class is 30–40**.
:::

::: example Reading a pie chart backwards
**Question.** In a pie chart of 900 households, the sector for firewood is
$140°$. How many households use firewood?

**Answer.** Households $= \frac{140}{360} \times 900 = \textbf{350}$.
:::

::: note Project — a survey of your own
Collect one piece of data from every household in your lane (say, the number
of people, or the main cooking fuel). Make a frequency table, find the mean,
median and mode where they apply, and draw both a bar chart and a pie chart.
Write three sentences on which average describes your data best and why.
:::

## Chapter summary

- Data are tallied, tabulated with a total, and then presented as a table, a bar
  graph or a pie chart.
- On a bar graph the height of the bar reads the frequency; bars have equal
  width and equal gaps.
- On a pie chart $\text{angle}=\frac{\text{frequency}}{\text{total}}\times360°$,
  and the angles must add to exactly 360°.
- $\text{mean}=\frac{\sum x}{n}$; the median is the middle value of the ordered
  list; the mode is the most frequent value.
- With an even number of values the median is the mean of the two middle ones.
- For grouped data, use the mid-value of each class for the mean, and speak of
  the modal class rather than the mode.
- An outlier pulls the mean but not the median; report the median when the data
  contain an extreme value.

## Practice questions

**Group A — Objective (1 mark each)**

1. The mean of 4, 6, 8, 10, 12 is <span class="marks">[1]</span>
   (a) 6 (b) 8 (c) 10 (d) 40
2. The mode of 3, 5, 5, 7, 9 is <span class="marks">[1]</span>
   (a) 3 (b) 5 (c) 7 (d) 9
3. The median of 7, 3, 9, 5, 11 is <span class="marks">[1]</span>
   (a) 5 (b) 7 (c) 9 (d) 11
4. In a pie chart the angle for a frequency of 10 out of a total of 50 is
   <span class="marks">[1]</span>
   (a) 36° (b) 72° (c) 60° (d) 90°
5. The median of 2, 4, 6, 8 is <span class="marks">[1]</span>
   (a) 4 (b) 5 (c) 6 (d) 7
6. A value that is much larger or smaller than the rest is called
   <span class="marks">[1]</span>
   (a) the mode (b) the median (c) an outlier (d) the range

::: note Answers to Group A
**1.** (b) — $40\div5=8$.
**2.** (b) — 5 appears twice.
**3.** (b) — in order 3, 5, 7, 9, 11 the middle is 7.
**4.** (b) — $\frac{10}{50}\times360=72°$.
**5.** (b) — $\frac{4+6}{2}=5$.
**6.** (c) — an outlier.
:::

**Group B — Short answer (2 marks each)**

1. Find the mean of 12, 15, 18, 20, 25. <span class="marks">[2]</span>
2. Find the median and the mode of 4, 7, 7, 9, 11, 13. <span class="marks">[2]</span>
3. A pie chart represents 60 students. One slice has an angle of 90°. How many
   students does it represent? <span class="marks">[2]</span>
4. The temperatures for a week were 20°, 22°, 21°, 23°, 25°, 24°, 26°. Find the
   mean temperature. <span class="marks">[2]</span>
:::

::: note Answers to Group B
**1.** $\frac{12+15+18+20+25}{5}=\frac{90}{5}=18$.
**2.** Median: with 6 values, $\frac{7+9}{2}=8$; mode $=7$.
**3.** $\frac{90}{360}\times60=15$ students.
**4.** $\frac{20+22+21+23+25+24+26}{7}=\frac{161}{7}=23°$.
:::

**Group C — Long answer (4 marks each)**

1. The marks of 20 students are: 35, 42, 48, 55, 60, 62, 65, 68, 70, 72, 74,
   75, 78, 80, 82, 85, 88, 90, 92, 95. Find the mean and the median, and say
   why they are close together here. <span class="marks">[4]</span>
2. A survey of 180 families found 45 with no bicycle, 90 with one, 36 with two
   and 9 with three. Draw a pie chart, and find the mean number of bicycles per
   family. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **Mean.** The sum is
$35+42+48+55+60+62+65+68+70+72+74+75+78+80+82+85+88+90+92+95=1416$, so
$\bar x=\frac{1416}{20}=70.8$.
**Median.** With $n=20$ (even) it is the mean of the 10th and 11th values:
$\frac{72+74}{2}=73$.
**Why they are close.** The values rise steadily with no extreme value and no
gap, so there is no outlier to pull the mean away from the middle of the list.
When data are spread evenly like this, the mean and the median agree closely;
when they differ a lot, look for an outlier.
**2.** **Pie chart.** Total families $=45+90+36+9=180$, so one family is
$\frac{360}{180}=2°$.

| Bicycles | Families | Angle |
|---|---|---|
| 0 | 45 | $90°$ |
| 1 | 90 | $180°$ |
| 2 | 36 | $72°$ |
| 3 | 9 | $18°$ |
| **Total** | **180** | **360°** |

**Check.** $90+180+72+18=360$ ✓.
**Mean.** $\bar x=\frac{0\times45+1\times90+2\times36+3\times9}{180}
=\frac{0+90+72+27}{180}=\frac{189}{180}=1.05$ bicycles per family.
**Interpretation.** The mean is just over one bicycle per family, while the
median and modal class are both "one bicycle" — which describes the typical
family better than 1.05 does.
:::

**Extra practice**

**Group B (2 marks)**

14. The mean of 8 numbers is 17. Find their sum.
15. In a pie chart of 72 students, how many degrees represent 18 students?

**Group C (4 marks)**

16. The daily wages of 40 workers are: $300$–$400$: 6, $400$–$500$: 12,
    $500$–$600$: 14, $600$–$700$: 8. Find the mean wage and the modal class,
    and say which average best describes the data.

::: note Extra practice — answers
**14.** $8 \times 17 = 136$.
**15.** $\frac{18}{72} \times 360° = 90°$.
**16.** Mid-values 350, 450, 550, 650.
$\sum fx = 6(350) + 12(450) + 14(550) + 8(650) = 2100 + 5400 + 7700 + 5200
= 20400$; mean $= \frac{20400}{40} = $ **Rs 510**.
Modal class **500–600** (frequency 14). The mean describes these data well
because the wages are evenly spread with no extreme value; had one worker
earned Rs 5,000, the median would have been the fairer average.
:::
