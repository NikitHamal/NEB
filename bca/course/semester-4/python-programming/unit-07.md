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
