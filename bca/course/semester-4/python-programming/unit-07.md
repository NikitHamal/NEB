---
subject: Python Programming
grade: BCA Semester 4
unit: 7
title: Data Analysis and Visualisation: NumPy, Pandas, Matplotlib
hours: 7
area: BCA 254 · Python Programming · Unit 7
---

Python became the language of data because of three libraries: **NumPy** (fast numerical arrays), **Pandas** (tables of data with labels) and **Matplotlib** (charts). Together they replace spreadsheet gymnastics with a few clear lines of code.

::: key What this unit gives you
- NumPy arrays: creation, indexing, slicing, vectorised operations, broadcasting, statistics.
- Pandas Series and DataFrame: loading data, selecting, filtering, grouping, handling missing values.
- Matplotlib: line, bar, histogram and pie charts saved to files.
:::

The libraries are installed with `pip install numpy pandas matplotlib`. The outputs below come from NumPy 2.5, Pandas 3.1 and Matplotlib 3.11 on Python 3.12; the layout of printed tables can differ slightly in other versions.

## 7.1 NumPy

A NumPy **ndarray** holds items of one type in a compact block of memory and applies operations to the **whole array at once** (**vectorisation**), which is typically tens to hundreds of times faster than a Python loop.

```python
import numpy as np
a = np.array([3, 1, 4, 1, 5, 9, 2, 6])
print(a, a.dtype, a.shape, a.ndim, a.size)
print(np.arange(0, 10, 2), np.linspace(0, 1, 5), np.zeros((2, 3)), np.eye(2), sep="\n")
m = np.arange(12).reshape(3, 4)
print(m, m.T.shape, m[1, 2], m[:, 1], m[1:, ::2], sep="\n")
```
```output
[3 1 4 1 5 9 2 6] int64 (8,) 1 8
[0 2 4 6 8]
[0.   0.25 0.5  0.75 1.  ]
[[0. 0. 0.]
 [0. 0. 0.]]
[[1. 0.]
 [0. 1.]]
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
(4, 3)
6
[1 5 9]
[[ 4  6]
 [ 8 10]]
```
### Vectorised operations and broadcasting

```python
import numpy as np
x = np.array([1.0, 2.0, 3.0, 4.0])
print(x * 2, x ** 2, x + np.array([10, 20, 30, 40]), np.sqrt(x))
m = np.arange(6).reshape(2, 3)
print(m + np.array([100, 200, 300]))
print(m * np.array([[1], [10]]))
print(x > 2, x[x > 2], np.where(x > 2, "big", "small"))
```
```output
[2. 4. 6. 8.] [ 1.  4.  9. 16.] [11. 22. 33. 44.] [1.         1.41421356 1.73205081 2.        ]
[[100 201 302]
 [103 204 305]]
[[ 0  1  2]
 [30 40 50]]
[False False  True  True] [3. 4.] ['small' 'small' 'big' 'big']
```
**Broadcasting** stretches the smaller array to the shape of the larger when their shapes are compatible (equal, or 1, in each dimension from the right): a row is added to every row of the matrix; a column multiplies every column.

### Statistics and linear algebra

```python
import numpy as np
marks = np.array([[72, 65, 80], [90, 85, 95], [55, 60, 58], [78, 82, 70]])
print(marks.mean(), marks.mean(axis=0), marks.max(axis=1), marks.sum(axis=0))
print(np.median(marks), round(marks.std(), 3), marks.argmax(), np.sort(marks[:, 0]))
A = np.array([[2.0, 1.0], [1.0, 3.0]])
b = np.array([5.0, 10.0])
x = np.linalg.solve(A, b)
print(x, A @ x, np.linalg.det(A), np.linalg.inv(A).round(3))
rng = np.random.default_rng(42)
print(rng.integers(1, 7, size=8), rng.normal(0, 1, 3).round(3))
```
```output
74.16666666666667 [73.75 73.   75.75] [80 95 60 82] [295 292 303]
75.0 12.409 5 [55 72 78 90]
[1. 3.] [ 5. 10.] 5.000000000000001 [[ 0.6 -0.2]
 [-0.2  0.4]]
[1 5 4 3 3 6 1 5] [-1.951 -1.302  0.128]
```
`axis=0` works down the columns, `axis=1` along the rows; `@` is matrix multiplication; `np.linalg` solves linear systems (the Numerical Methods book of this semester does it by hand). Seeding the random generator makes results reproducible.

## 7.2 Pandas

A **Series** is a labelled one-dimensional array; a **DataFrame** is a table of Series sharing an index, much like a spreadsheet or SQL table.

```python
import pandas as pd
s = pd.Series([88, 92, 79], index=["Ram", "Sita", "Hari"], name="marks")
print(s, s["Sita"], s.mean(), s[s > 80].index.tolist(), sep="\n")
df = pd.DataFrame({"name": ["Ram", "Sita", "Hari", "Gita"],
                   "dept": ["BCA", "BCA", "BIT", "BIT"],
                   "marks": [78, 91, 64, 85]})
print(df)
print(df.shape, list(df.columns), df["marks"].dtype)
print(df.describe().round(2))
```
```output
Ram     88
Sita    92
Hari    79
Name: marks, dtype: int64
92
86.33333333333333
['Ram', 'Sita']
   name dept  marks
0   Ram  BCA     78
1  Sita  BCA     91
2  Hari  BIT     64
3  Gita  BIT     85
(4, 3) ['name', 'dept', 'marks'] int64
       marks
count   4.00
mean   79.50
std    11.62
min    64.00
25%    74.50
50%    81.50
75%    86.50
max    91.00
```
### Loading data

`pd.read_csv("file.csv")` loads a CSV file into a DataFrame (`read_excel`, `read_json`, `read_sql` do likewise). Here the file content is supplied from a string so that the example is self-contained; it contains a missing value.

```python
import io
import pandas as pd
csv_text = """roll,name,dept,maths,physics
1,Ram,BCA,78,70
2,Sita,BCA,91,
3,Hari,BIT,64,58
4,Gita,BIT,85,90
5,Bikash,BCA,55,62
"""
df = pd.read_csv(io.StringIO(csv_text))
print(df)
print(df.isna().sum().to_dict())
df["physics"] = df["physics"].fillna(df["physics"].mean())
df["total"] = df["maths"] + df["physics"]
print(df[["name", "total"]])
```
```output
   roll    name dept  maths  physics
0     1     Ram  BCA     78     70.0
1     2    Sita  BCA     91      NaN
2     3    Hari  BIT     64     58.0
3     4    Gita  BIT     85     90.0
4     5  Bikash  BCA     55     62.0
{'roll': 0, 'name': 0, 'dept': 0, 'maths': 0, 'physics': 1}
     name  total
0     Ram  148.0
1    Sita  161.0
2    Hari  122.0
3    Gita  175.0
4  Bikash  117.0
```
### Selecting, filtering, sorting, grouping

```python
import io
import pandas as pd
df = pd.read_csv(io.StringIO("""name,dept,maths,physics
Ram,BCA,78,70
Sita,BCA,91,80
Hari,BIT,64,58
Gita,BIT,85,90
Bikash,BCA,55,62
"""))
print(df[df["maths"] > 70])
print(df.loc[df["dept"] == "BCA", ["name", "maths"]])
print(df.sort_values("maths", ascending=False).head(3)["name"].tolist())
print(df.iloc[1:3, 0:2])
g = df.groupby("dept")[["maths", "physics"]].mean().round(1)
print(g)
print(df.groupby("dept").agg(students=("name", "count"), best=("maths", "max")))
```
```output
   name dept  maths  physics
0   Ram  BCA     78       70
1  Sita  BCA     91       80
3  Gita  BIT     85       90
     name  maths
0     Ram     78
1    Sita     91
4  Bikash     55
['Sita', 'Gita', 'Ram']
   name dept
1  Sita  BCA
2  Hari  BIT
      maths  physics
dept                
BCA    74.7     70.7
BIT    74.5     74.0
      students  best
dept                
BCA          3    91
BIT          2    85
```
`loc` selects by label and conditions; `iloc` by integer position. `groupby` splits the rows, applies a function (mean, count, max) to each group and combines the results, the same idea as SQL `GROUP BY`. Other staples: `merge` (join two tables), `pivot_table`, `value_counts`, `apply`, `drop_duplicates`, `to_csv`.

```python
import pandas as pd
a = pd.DataFrame({"dept": ["BCA", "BIT"], "head": ["Dr. Shah", "Dr. Rai"]})
b = pd.DataFrame({"name": ["Ram", "Hari", "Zed"], "dept": ["BCA", "BIT", "BBA"]})
print(b.merge(a, on="dept", how="left"))
print(pd.Series(["a", "b", "a", "c", "a"]).value_counts().to_dict())
```
```output
   name dept      head
0   Ram  BCA  Dr. Shah
1  Hari  BIT   Dr. Rai
2   Zed  BBA       NaN
{'a': 3, 'b': 1, 'c': 1}
```
## 7.3 Matplotlib

Matplotlib draws charts. In a script you build a figure and either `plt.show()` it or `plt.savefig("name.png")`. The programs below save files (a non-interactive backend) and print what was produced.

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, os
x = np.linspace(0, 2 * np.pi, 100)
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(x, np.sin(x), label="sin x", color="tab:blue")
ax.plot(x, np.cos(x), "--", label="cos x", color="tab:red")
ax.set(title="Sine and cosine", xlabel="x (radians)", ylabel="value")
ax.legend(); ax.grid(True)
fig.tight_layout()
fig.savefig("trig.png", dpi=100)
print(os.path.exists("trig.png"), fig.get_size_inches(), len(ax.lines))
```
```output
True [6. 3.] 2
```
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
fig, axes = plt.subplots(1, 3, figsize=(10, 3))
subjects, avg = ["OS", "NM", "SE", "Py", "WT"], [68, 61, 72, 80, 75]
axes[0].bar(subjects, avg, color="tab:green"); axes[0].set_title("Bar chart")
rng = np.random.default_rng(1)
data = rng.normal(60, 12, 200)
axes[1].hist(data, bins=10, edgecolor="black"); axes[1].set_title("Histogram")
axes[2].pie([40, 30, 20, 10], labels=["A", "B", "C", "D"], autopct="%1.0f%%"); axes[2].set_title("Pie chart")
fig.tight_layout(); fig.savefig("charts.png")
counts, edges = np.histogram(data, bins=10)
print(len(axes), counts.sum(), round(data.mean(), 1), round(data.std(), 1))
```
```output
3 200 59.1 11.1
```
| Chart | Use | Call |
|---|---|---|
| Line | trends over an ordered axis | `plot` |
| Bar | compare categories | `bar`, `barh` |
| Histogram | distribution of one variable | `hist` |
| Scatter | relationship between two variables | `scatter` |
| Pie | parts of a whole (few slices only) | `pie` |

Good charts have a title, labelled axes with units, a legend when several series appear, and no unnecessary decoration. Pandas can draw directly: `df.plot(kind="bar")`.

## 7.4 Seeing the ideas: data made visible

Long before NumPy and Pandas, people turned numbers into pictures so that a pattern could be seen at once. The three historical charts below were each drawn by hand, and each one matches a chart type you can now make in a few lines of Matplotlib. After them, the figures show how broadcasting and `axis` work in NumPy, how `groupby` splits and combines a table, what the parts of a Matplotlib figure are, and what a real histogram looks like.

```photogrid label="7.1" cols="3" ratio="1.25" caption="Three hand-drawn data charts, each the ancestor of a Matplotlib chart type. (a) William Playfair's 1786 chart of trade between England and America from 1700 to 1780: a line chart with the gap between the lines shaded, the first time-series chart of its kind (plot, fill_between). (b) John Snow's 1854 map of cholera deaths in Soho: one dot per death and a cross for each water pump, so the cluster around one pump shows the cause (scatter plot). (c) Florence Nightingale's diagram of the causes of death in the army in the East: each month is a wedge whose area is the number of deaths, blue for disease (polar bar chart, pie chart family). All three are public-domain scans."
@ photo id="bca254/playfair" cap="Playfair 1786: line chart"
fit 1.25
focus 0.48 0.5
call 0.30 0.70 0.04 0.92 "two lines"
@ photo id="bca254/snow" cap="Snow 1854: scatter map"
fit 1.25
focus 0.5 0.5
call 0.47 0.34 0.04 0.92 "dot = death"
@ photo id="bca254/nightingale" cap="Nightingale: polar bars"
fit 1.25
focus 0.72 0.5
call 0.80 0.62 0.04 0.92 "wedge = month"
```

```photogrid label="7.2" cols="1" ratio="2.6" caption="Charles Minard's 1869 chart of Napoleon's march to Moscow and back. The width of the tan band is the number of soldiers going east and the width of the black band the number coming home, so one picture carries the route, the size of the army and (in the lower strip) the temperature. It is the standard example of a chart that shows several variables at once, and the kind of figure you can build from a DataFrame by plotting lines of different widths (public domain)."
@ photo id="bca254/minard" cap="Minard 1869: band width = number of soldiers"
fit 2.6
focus 0.5 0.62
call 0.52 0.40 0.04 0.92 "the army shrinks"
```

```svgfig label="7.1" caption="Split, apply, combine: the idea behind groupby, from a real run on the DataFrame of Section 7.2. groupby('dept') splits the five rows into one group per department, mean() is applied to each group, and the two results are combined into one small table. The values (74.67 and 74.5) are computed by the cell."
import pandas as pd
df = pd.DataFrame({"name": ["Ram", "Sita", "Hari", "Gita", "Bikash"], "dept": ["BCA", "BCA", "BIT", "BIT", "BCA"], "maths": [78, 91, 64, 85, 55]})
g = df.groupby("dept")["maths"].mean().round(2)
f = Fig(580, 150)
f.text(80, 12, "df (5 rows)", size=11, color=NAVY, bold=True)
for i, r in df.iterrows():
    f.box(10, 20 + i * 24, 140, 22, f"{r['name']}   {r['dept']}   {r['maths']}", fill=SOFT, stroke=SLATE, size=11)
f.text(300, 12, "split by dept", size=11, color=NAVY, bold=True)
f.box(230, 24, 140, 40, "BCA: 78  91  55", fill=BLUE, stroke=NAVY, size=11.5, bold=True)
f.box(230, 84, 140, 40, "BIT: 64  85", fill=SAND, stroke=AMBER, size=11.5, bold=True)
f.arrow([(152, 60), (228, 44)], color=SLATE, sw=1.4)
f.arrow([(152, 100), (228, 104)], color=SLATE, sw=1.4)
f.text(490, 12, "mean() then combine", size=11, color=NAVY, bold=True)
f.box(430, 24, 140, 40, f"BCA  {g['BCA']}", fill=MINT, stroke=TEAL, size=12, bold=True)
f.box(430, 84, 140, 40, f"BIT  {g['BIT']}", fill=MINT, stroke=TEAL, size=12, bold=True)
f.arrow([(372, 44), (428, 44)], color=SLATE, sw=1.4)
f.arrow([(372, 104), (428, 104)], color=SLATE, sw=1.4)
```

```svgfig label="7.2" caption="Broadcasting, computed by NumPy. Top: m + row. The 2 by 3 matrix m is added to the 1 by 3 row [100 200 300]; NumPy behaves as if the row were copied down to every row (the dashed ghost cells; no memory is really copied). Bottom: m * column. The 2 by 1 column [[1], [10]] is stretched across the columns instead. The right-hand matrices are the real results printed by the cell. The rule: compare shapes from the right; each pair of sizes must be equal or one of them must be 1."
import numpy as np
m = np.arange(6).reshape(2, 3)
row = np.array([100, 200, 300])
col = np.array([[1], [10]])
r1 = m + row
r2 = m * col
f = Fig(580, 250)
def grid(x, y, M, fill, stroke, dash=False):
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            f.box(x + j * 40, y + i * 30, 38, 28, str(M[i, j]), fill=fill, stroke=stroke, size=11.5, bold=True, dash=dash, r=4)
f.text(10, 14, "m + row", size=11.5, color=NAVY, bold=True, anchor="start")
grid(10, 26, m, BLUE, NAVY)
f.text(138, 56, "+", size=18, color=SLATE, bold=True)
grid(152, 26, np.broadcast_to(row, (2, 3)), SOFT, SLATE, dash=True)
f.box(152, 26, 38, 28, "100", fill=SAND, stroke=AMBER, size=11.5, bold=True, r=4)
f.box(192, 26, 38, 28, "200", fill=SAND, stroke=AMBER, size=11.5, bold=True, r=4)
f.box(232, 26, 38, 28, "300", fill=SAND, stroke=AMBER, size=11.5, bold=True, r=4)
f.text(290, 56, "=", size=18, color=SLATE, bold=True)
grid(304, 26, r1, MINT, TEAL)
f.text(430, 40, "the row is reused", size=10.5, color=SLATE, anchor="start")
f.text(430, 56, "for every row of m", size=10.5, color=SLATE, anchor="start")
f.text(10, 134, "m * col", size=11.5, color=NAVY, bold=True, anchor="start")
grid(10, 146, m, BLUE, NAVY)
f.text(138, 176, "*", size=18, color=SLATE, bold=True)
grid(152, 146, np.broadcast_to(col, (2, 3)), SOFT, SLATE, dash=True)
f.box(152, 146, 38, 28, "1", fill=SAND, stroke=AMBER, size=11.5, bold=True, r=4)
f.box(152, 176, 38, 28, "10", fill=SAND, stroke=AMBER, size=11.5, bold=True, r=4)
f.text(290, 176, "=", size=18, color=SLATE, bold=True)
grid(304, 146, r2, MINT, TEAL)
f.text(430, 160, "the column is reused", size=10.5, color=SLATE, anchor="start")
f.text(430, 176, "for every column of m", size=10.5, color=SLATE, anchor="start")
f.text(10, 236, "shapes (2,3) and (3,) -> (2,3)        shapes (2,3) and (2,1) -> (2,3)", size=10.5, color=NAVY, bold=True, anchor="start")
```

```svgfig label="7.3" caption="The axis argument, computed by NumPy on the 4 by 3 marks array of Section 7.1 (four students, three subjects). axis=0 means 'run down the rows and collapse them', so mean(axis=0) gives one value per column (per subject). axis=1 means 'run along the columns and collapse them', so max(axis=1) gives one value per row (per student). The numbers are the real results. Remember: the axis you name is the one that disappears from the shape."
import numpy as np
marks = np.array([[72, 65, 80], [90, 85, 95], [55, 60, 58], [78, 82, 70]])
cm = marks.mean(axis=0)
rm = marks.max(axis=1)
f = Fig(580, 214)
f.text(10, 14, "marks.shape = (4, 3)", size=11, color=NAVY, bold=True, anchor="start")
for j, s in enumerate(["Maths", "Physics", "Python"]):
    f.text(60 + j * 56 + 24, 36, s, size=10, color=SLATE, bold=True)
for i in range(4):
    for j in range(3):
        f.box(60 + j * 56, 44 + i * 30, 48, 26, str(marks[i, j]), fill=BLUE, stroke=NAVY, size=12, bold=True, r=4)
    f.arrow([(60 + 3 * 56 - 2, 57 + i * 30), (60 + 3 * 56 + 22, 57 + i * 30)], color=AMBER, sw=1.5)
    f.box(60 + 3 * 56 + 24, 44 + i * 30, 44, 26, str(rm[i]), fill=SAND, stroke=AMBER, size=12, bold=True, r=4)
for j in range(3):
    f.arrow([(84 + j * 56, 166), (84 + j * 56, 176)], color=TEAL, sw=1.5)
    f.box(60 + j * 56, 178, 48, 26, f"{cm[j]:.2f}", fill=MINT, stroke=TEAL, size=11, bold=True, r=4)
f.text(300, 60, "max(axis=1)", size=12, color=AMBER, bold=True, anchor="start")
f.text(300, 78, "one value per student", size=10.5, color=SLATE, anchor="start")
f.text(300, 96, "result shape (4,)", size=10.5, color=SLATE, anchor="start")
f.text(300, 150, "mean(axis=0)", size=12, color=TEAL, bold=True, anchor="start")
f.text(300, 168, "one value per subject", size=10.5, color=SLATE, anchor="start")
f.text(300, 186, "result shape (3,)", size=10.5, color=SLATE, anchor="start")
```

```svgfig label="7.4" caption="Anatomy of a Matplotlib figure. The Figure is the whole canvas; an Axes is one plot area inside it (a figure can hold many); each Axes has two Axis objects (the x and y axes with ticks and labels), a title, a legend and the artists that are drawn, such as lines and bars. The counts at the bottom come from a real run of the code that draws the sine/cosine figure of Section 7.3: one Axes, two lines. Use the object-oriented style fig, ax = plt.subplots() and call methods on ax."
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, math
x = np.linspace(0, 2 * np.pi, 100)
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(x, np.sin(x), label="sin x"); ax.plot(x, np.cos(x), "--", label="cos x")
ax.set(title="Sine and cosine", xlabel="x (radians)", ylabel="value"); ax.legend()
n_ax, n_lines = len(fig.axes), len(ax.lines)
f = Fig(580, 232)
f.box(8, 8, 360, 188, "", fill=SOFT, stroke=SLATE, sw=1.2)
f.text(16, 22, "Figure", size=11, color=SLATE, bold=True, anchor="start")
f.box(60, 40, 290, 118, "", fill="#ffffff", stroke=NAVY, sw=1.6)
f.text(205, 34, "title: Sine and cosine", size=11, color=NAVY, bold=True)
pts_s = [(70 + i * 5, 99 - 40 * math.sin(i * 2 * math.pi / 56)) for i in range(57)]
pts_c = [(70 + i * 5, 99 - 40 * math.cos(i * 2 * math.pi / 56)) for i in range(57)]
for a, b in zip(pts_s, pts_s[1:]):
    f.line(a[0], a[1], b[0], b[1], color=NAVY, sw=1.8)
for k, (a, b) in enumerate(zip(pts_c, pts_c[1:])):
    if k % 2 == 0:
        f.line(a[0], a[1], b[0], b[1], color=RED, sw=1.8)
f.box(268, 46, 76, 36, "", fill="#ffffff", stroke=SLATE, sw=1)
f.line(274, 58, 290, 58, color=NAVY, sw=1.8); f.text(296, 58, "sin x", size=9.5, color=SLATE, anchor="start", vmid=True)
f.line(274, 72, 290, 72, color=RED, sw=1.8); f.text(296, 72, "cos x", size=9.5, color=SLATE, anchor="start", vmid=True)
f.text(205, 178, "x (radians)", size=10.5, color=SLATE)
f.text(30, 99, "value", size=10.5, color=SLATE)
f.text(430, 24, "Figure: the whole canvas", size=10.5, color=SLATE, anchor="start")
f.text(430, 54, "Axes: one plot area", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(430, 84, "Axis: ticks and labels", size=10.5, color=SLATE, anchor="start")
f.text(430, 114, "Title, legend, grid", size=10.5, color=SLATE, anchor="start")
f.text(430, 144, "Artists: lines, bars", size=10.5, color=SLATE, anchor="start")
f.text(10, 220, f"real run: len(fig.axes) = {n_ax}, len(ax.lines) = {n_lines}", size=11, color=TEAL, bold=True, anchor="start")
```

```svgfig label="7.5" caption="A real histogram. The cell draws 200 values from NumPy's random generator (default_rng(1), normal with mean 60 and spread 12, as in Section 7.3) and counts them into 10 equal-width bins with np.histogram. Bar height is the number of values in the bin; the total is 200. The dashed line marks the mean. A histogram shows the shape of a distribution (centre, spread, skew), which a bar chart of categories cannot do."
import numpy as np
rng = np.random.default_rng(1)
data = rng.normal(60, 12, 200)
counts, edges = np.histogram(data, bins=10)
mean = float(data.mean())
f = Fig(580, 214)
x0, y0, w, h = 50, 178, 500, 150
top = counts.max()
f.line(x0, y0, x0 + w, y0, color=SLATE, sw=1.4)
f.line(x0, y0, x0, y0 - h, color=SLATE, sw=1.4)
bw = w / 10
for i, c in enumerate(counts):
    bh = h * c / (top * 1.1)
    f.box(x0 + i * bw + 2, y0 - bh, bw - 4, bh, "", fill=BLUE, stroke=NAVY, r=2)
    f.text(x0 + i * bw + bw / 2, y0 - bh - 7, str(int(c)), size=10.5, color=NAVY, bold=True)
    f.text(x0 + i * bw, y0 + 14, f"{edges[i]:.0f}", size=9.5, color=SLATE)
f.text(x0 + w, y0 + 14, f"{edges[-1]:.0f}", size=9.5, color=SLATE)
mx = x0 + (mean - edges[0]) / (edges[-1] - edges[0]) * w
f.line(mx, y0, mx, y0 - h - 6, color=RED, sw=1.6, dash=True)
f.text(mx + 8, y0 - h - 12, f"mean {mean:.1f}", size=10.5, color=RED, bold=True, anchor="start")
f.text(x0 + w / 2, y0 + 30, f"value (bin edges)       total = {int(counts.sum())}", size=10.5, color=SLATE)
f.text(14, 90, "count", size=10.5, color=SLATE, anchor="start")
```

```svgfig label="7.6" caption="Cleaning missing values, from a real Pandas run. A column of five marks has two missing entries (NaN, 'not a number'). isna().sum() counts them. dropna() removes the rows (3 left, mean of the known marks 75.67). fillna(mean) keeps all five rows by replacing each gap with that mean, which keeps the average but hides the fact that the data were missing. Which choice is right depends on how many values are missing and why."
import pandas as pd, numpy as np
s = pd.Series([78, np.nan, 64, 85, np.nan], name="marks")
miss = int(s.isna().sum())
m = s.mean()
d = s.dropna()
fl = s.fillna(round(m, 2))
f = Fig(580, 200)
def col(x, title, vals, fill, stroke):
    f.text(x + 40, 16, title, size=11, color=stroke, bold=True)
    for i, v in enumerate(vals):
        lab = "NaN" if (isinstance(v, float) and np.isnan(v)) else (f"{v:.2f}" if v != int(v) else str(int(v)))
        f.box(x, 26 + i * 30, 80, 26, lab, fill=fill if lab != "NaN" else SAND, stroke=stroke if lab != "NaN" else AMBER, size=12, bold=True, r=4)
col(10, "s", list(s), BLUE, NAVY)
f.arrow([(96, 90), (170, 60)], color=SLATE, sw=1.5)
f.arrow([(96, 100), (170, 150)], color=SLATE, sw=1.5)
col(176, "dropna()", list(d), MINT, TEAL)
col(366, "fillna(mean)", list(fl), MINT, TEAL)
f.text(300, 188, f"isna().sum() = {miss}   mean of known = {m:.2f}   rows kept: {len(d)} vs {len(fl)}", size=10.5, color=NAVY, bold=True)
f.text(470, 60, "all 5 rows kept", size=10.5, color=SLATE, anchor="start")
f.text(470, 78, "gaps become 75.67", size=10.5, color=SLATE, anchor="start")
f.text(270, 60, "3 rows kept", size=10.5, color=SLATE, anchor="start")
f.text(270, 78, "gaps removed", size=10.5, color=SLATE, anchor="start")
```

### 7.4.1 Eight applications of Python data analysis

1. **Examination and school results.** A board or a college holds thousands of marks in a table. With Pandas, `groupby("district")["pass"].mean()` gives the pass rate of every district in one line, and a bar chart shows the weak districts. Tribhuvan University and school education management systems (EMIS) use this kind of summary every year to plan teacher support.
2. **Banking and digital payments.** Wallets and bank transfers such as ConnectIPS and Fonepay produce a record for every payment. Pandas can total the payments per hour and Matplotlib can draw the daily curve, so the busiest hours are seen at once. Values that are far from the rest (outliers) can be flagged for a fraud check.
3. **Stock market (NEPSE).** A table of daily closing prices becomes a line chart in two lines of code. A moving average, such as `rolling(20).mean()`, smooths the noise and shows the trend. This helps a student of finance to study a company's price history before writing a report.
4. **Weather and floods.** The Department of Hydrology and Meteorology records rainfall and river levels every day. NumPy handles the long arrays of readings, and a line chart of the monsoon months shows when a river is rising. Such charts support early warning to villages along the river.
5. **Census and planning.** A census gives a table of population, households and literacy for each district. `merge` joins it with a second table (for example school counts) and `sort_values` finds the districts with the lowest services. Plans for roads, schools and clinics can then be based on numbers instead of guesses.
6. **Public health.** A weekly count of dengue or diarrhoea cases is a time series. Plotting it shows an outbreak starting, as John Snow's map did for cholera (Plate 7.1). Grouping the cases by ward then shows where to send the health team first.
7. **Electricity and energy.** The Nepal Electricity Authority needs the load of the grid every hour. A NumPy array of 24 values per day can be averaged over a month with `mean(axis=0)`, and the peak hour is found with `argmax`. The result guides when to start extra generation or to ask users to save power in the evening.
8. **Tourism and small business.** Monthly arrivals of tourists, or the daily sales of a shop in Pokhara, fit in one DataFrame. A bar chart by month shows the season, and `groupby` on product shows what sells. The owner can plan stock, staff and prices from the pattern.

## Formula and fact sheet

- `np.array`, `arange`, `linspace`, `zeros`, `reshape`; vectorised arithmetic; boolean masks; `axis=0` columns, `axis=1` rows.
- Broadcasting: shapes compatible from the right (equal or 1).
- `pd.Series`, `pd.DataFrame`, `read_csv`, `loc` (labels), `iloc` (positions), `groupby().agg()`, `merge`, `fillna`, `isna`.
- `plt.subplots`, `plot/bar/hist/pie`, `savefig`.

## Chapter summary

- NumPy arrays give fast, vectorised numerical work with broadcasting and built-in statistics and linear algebra.
- Pandas turns CSV-style data into DataFrames that can be cleaned, filtered, grouped and merged in a few expressions.
- Matplotlib communicates the results as charts.

## Practice

1. Create a NumPy array of the squares of 1 to 10 and print those greater than 30.
2. Explain broadcasting with an example of adding a vector to a matrix.
3. Compute the mean of each column of a 3 × 3 array.
4. Given a DataFrame of student marks, show how to find the students with more than 70 in maths.
5. Group a DataFrame by department and report the mean marks.
6. How would you handle missing values in a column?
7. Plot y = x² for x from −3 to 3 and save the figure.

::: note Answers and worked solutions
**1.**

```python
import numpy as np
sq = np.arange(1, 11) ** 2
print(sq, sq[sq > 30])
```
```output
[  1   4   9  16  25  36  49  64  81 100] [ 36  49  64  81 100]
```
**2.**

```python
import numpy as np
print(np.ones((2, 3)) + np.array([1, 2, 3]))
```
```output
[[2. 3. 4.]
 [2. 3. 4.]]
```
The vector of shape (3,) is stretched across both rows of the (2, 3) array.
**3.**

```python
import numpy as np
a = np.arange(9).reshape(3, 3)
print(a.mean(axis=0))
```
```output
[3. 4. 5.]
```
**4.**

```python
import pandas as pd
df = pd.DataFrame({"name": ["A", "B", "C"], "maths": [65, 82, 74]})
print(df[df["maths"] > 70]["name"].tolist())
```
```output
['B', 'C']
```
**5.**

```python
import pandas as pd
df = pd.DataFrame({"dept": ["BCA", "BIT", "BCA"], "marks": [70, 60, 90]})
print(df.groupby("dept")["marks"].mean().to_dict())
```
```output
{'BCA': 80.0, 'BIT': 60.0}
```
**6.** Count them with `df.isna().sum()`; then either drop (`dropna()`), fill with a constant or statistic (`fillna(df["col"].mean())`), or interpolate, depending on how much is missing and why.
**7.**

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
x = np.linspace(-3, 3, 61)
plt.plot(x, x ** 2)
plt.title("y = x squared")
plt.savefig("parabola.png")
print(len(x), x.min(), (x ** 2).min())
```
```output
61 -3.0 0.0
```
:::

## Model answers (5 and 10 marks)

**Q1. What is a NumPy array? Explain vectorisation, broadcasting and the `axis` argument with a program. (5 marks)**

**Introduction.** A NumPy **ndarray** is a fixed-size grid of items that all have the same type, stored together in one block of memory. Because the type is fixed and the items sit side by side, NumPy can run loops in fast compiled code instead of in the Python interpreter. This makes array work many times faster than the same work on a list, and it needs much less code.

**Main points.**

1. **Creation and shape.** Arrays are made with `np.array`, `arange`, `linspace`, `zeros` and `eye`. The attributes `shape`, `ndim`, `size` and `dtype` describe the array, and `reshape` changes the shape without changing the data.
2. **Vectorisation.** An operation such as `x * 2` or `np.sqrt(x)` is applied to every element at once, so no `for` loop is written. A comparison such as `x > 2` gives a Boolean array that can be used as a mask, `x[x > 2]`.
3. **Broadcasting.** When two arrays have different shapes, NumPy stretches the smaller one so the shapes match, provided that, comparing from the right, each pair of sizes is equal or one of them is 1 (Fig. 7.2).
4. **The axis argument.** `axis=0` collapses the rows and gives one result per column; `axis=1` collapses the columns and gives one result per row (Fig. 7.3).

```python
import numpy as np
marks = np.array([[72, 65, 80], [90, 85, 95], [55, 60, 58], [78, 82, 70]])
print(marks.shape, marks.dtype)
print(marks.mean(axis=0).round(2))          # per subject
print(marks.max(axis=1))                    # per student
print(marks + np.array([5, 0, 0]))          # broadcasting: +5 to the first subject
print(marks[marks > 90])                    # Boolean mask
```
```output
(4, 3) int64
[73.75 73.   75.75]
[80 95 60 82]
[[77 65 80]
 [95 85 95]
 [60 60 58]
 [83 82 70]]
[95]
```
**Example.** A teacher can add five grace marks to one subject for all students with the single expression `marks + [5, 0, 0]`, and find the best mark of every student with `marks.max(axis=1)`, without writing any loop.

**Conclusion.** NumPy arrays give compact storage, loop-free vectorised arithmetic, flexible broadcasting and one-line statistics, which is why Pandas and Matplotlib are built on top of them.

**Q2. Distinguish between a Pandas Series and a DataFrame. Explain how rows are selected, filtered and grouped, with a program. (5 marks)**

**Introduction.** Pandas is the library for working with tables of data that have labels. Its two main objects are the **Series**, a labelled one-dimensional array, and the **DataFrame**, a two-dimensional table in which every column is a Series and all columns share one row index. A DataFrame is much like a spreadsheet sheet or an SQL table, but it is controlled from code and can hold millions of rows.

**Main points.**

1. **Series versus DataFrame.** A Series has one column of values and an index (for example marks labelled by student name). A DataFrame has many named columns that may have different types (text, integers, decimals).
2. **Loading.** `pd.read_csv("file.csv")` reads a table from a file, and `head()`, `info()` and `describe()` give a quick look at its contents and statistics.
3. **Selecting.** `df["maths"]` gives a column; `df.loc[rows, columns]` selects by label; `df.iloc[i:j, k:l]` selects by position.
4. **Filtering.** A Boolean condition such as `df["maths"] > 70` keeps only the rows where it is true; conditions can be combined with `&` and `|`.
5. **Grouping.** `groupby("dept")` splits the rows by a column, applies a function such as `mean` or `count` to every group and combines the results into a new table (Fig. 7.1).

```python
import io
import pandas as pd
df = pd.read_csv(io.StringIO("""name,dept,maths
Ram,BCA,78
Sita,BCA,91
Hari,BIT,64
Gita,BIT,85
Bikash,BCA,55
"""))
print(type(df["maths"]).__name__, df.shape)
print(df[df["maths"] > 70]["name"].tolist())
print(df.loc[df["dept"] == "BCA", "maths"].max())
print(df.groupby("dept")["maths"].agg(["count", "mean"]).round(2))
```
```output
Series (5, 3)
['Ram', 'Sita', 'Gita']
91
      count   mean
dept              
BCA       3  74.67
BIT       2  74.50
```
**Example.** A college office can list all students above 70 in maths and the average of each department with three short expressions, and then send the result to a chart.

**Conclusion.** A Series holds one labelled column and a DataFrame holds a whole table; selection, Boolean filtering and `groupby` are the three operations that answer most questions asked of a table.

**Q3. Explain data visualisation with Matplotlib. Describe the parts of a figure, the common chart types and how to choose between them, with a program. (10 marks)**

**Introduction.** **Data visualisation** means turning numbers into a picture so that a pattern, a trend or an unusual value can be seen quickly. People did this long before computers: Playfair's trade chart, Snow's cholera map and Nightingale's mortality diagram (Plate 7.1) each changed a decision. **Matplotlib** is the standard Python library for drawing such charts, and it can save them as image files (PNG, PDF, SVG) for reports and web pages.

**Parts of a figure (Fig. 7.4).** The **Figure** is the whole canvas. An **Axes** is one plot area; a figure can hold several, created with `plt.subplots(rows, columns)`. Each Axes has an **x-axis and a y-axis** (ticks and labels), a **title**, an optional **legend**, a **grid**, and the **artists** that are drawn, such as lines, bars and text. The recommended style is the object-oriented one: `fig, ax = plt.subplots()` and then `ax.plot(...)`, `ax.set(...)`.

**Common chart types and their use.**

1. **Line chart (`plot`)** for a trend over an ordered axis such as time, for example the daily NEPSE closing price.
2. **Bar chart (`bar`, `barh`)** to compare a few categories, for example the average marks of five subjects.
3. **Histogram (`hist`)** to show how the values of one variable are spread (Fig. 7.5). The bins are equal-width ranges and the height is the count in each.
4. **Scatter plot (`scatter`)** to see whether two variables are related, for example study hours and marks.
5. **Pie chart (`pie`)** for parts of a whole, only when there are very few slices.

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
rng = np.random.default_rng(1)
hours = rng.uniform(1, 8, 30)
marks = 40 + 6 * hours + rng.normal(0, 5, 30)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 3))
a1.scatter(hours, marks, color="tab:blue"); a1.set(title="Study hours vs marks", xlabel="hours per day", ylabel="marks")
a2.hist(marks, bins=8, edgecolor="black"); a2.set(title="Marks", xlabel="marks", ylabel="students")
fig.tight_layout(); fig.savefig("study.png", dpi=100)
r = np.corrcoef(hours, marks)[0, 1]
print(len(fig.axes), round(float(r), 2))
```
```output
2 0.94
```
**Choosing a chart.**

| Question | Chart | Call |
|---|---|---|
| How does a value change over time? | Line | `plot` |
| Which category is larger? | Bar | `bar` |
| How are the values spread? | Histogram | `hist` |
| Are two variables related? | Scatter | `scatter` |
| What share does each part have? | Pie (few slices) | `pie` |

**Good practice.** Give every chart a title, label both axes with units, add a legend when there is more than one series, start a bar chart at zero, and avoid decoration that carries no data. Minard's chart (Plate 7.2) is admired because every visual element carries information.

**Conclusion.** Matplotlib turns a table into a chart with a few lines; by understanding the Figure/Axes structure and choosing the chart type that matches the question, a student can communicate results clearly in a project report.

**Q4. How are missing values handled in Pandas? Write a program and discuss when each method is suitable. (5 marks)**

**Introduction.** Real data are rarely complete: a student may have been absent from an exam, or a sensor may have failed on one day. Pandas marks such gaps as **NaN** (not a number). Most statistics skip NaN automatically, but if the gaps are not handled, counts, plots and models can be misleading, so cleaning is the first step of any analysis.

**Main points.**

1. **Detect.** `df.isna()` gives True where a value is missing, and `df.isna().sum()` counts the gaps in each column (Fig. 7.6).
2. **Drop.** `dropna()` removes rows (or columns) that contain gaps. It is simple and honest, but it throws away the other values in those rows, so it suits data where only a few rows are affected.
3. **Fill with a constant or a statistic.** `fillna(0)` or `fillna(s.mean())` keeps every row. The mean or median keeps the average roughly unchanged but hides the fact that the value was missing, so use the median if there are outliers.
4. **Fill from neighbours.** `ffill()` copies the previous value and `interpolate()` draws a line between the neighbours; this suits a time series such as daily rainfall (a gap at the very end is simply copied from the last known value).

```python
import pandas as pd, numpy as np
s = pd.Series([78, np.nan, 64, 85, np.nan], name="marks")
print(int(s.isna().sum()), round(float(s.mean()), 2))
print(s.dropna().tolist())
print(s.fillna(s.mean()).round(2).tolist())
print(s.interpolate().tolist())
```
```output
2 75.67
[78.0, 64.0, 85.0]
[78.0, 75.67, 64.0, 85.0, 75.67]
[78.0, 71.0, 64.0, 85.0, 85.0]
```
**Example.** If two marks out of five are missing, the mean of the three known marks is 75.67. Dropping the rows leaves three students; filling with the mean keeps five students but gives two of them an invented mark.

**Conclusion.** First count the missing values, then choose to drop, fill with a statistic or interpolate according to how many are missing and why, and always record which choice was made.
