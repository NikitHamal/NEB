---
subject: Computer Science
grade: 8
unit: 8
title: Spreadsheet Software
hours: 0
area: Application Software
---

A class teacher has the marks of forty students in six subjects. She must add
them, find percentages, decide who passed, rank the class and draw a chart for
the parents' meeting. With a calculator this takes a whole day, and one wrong
key spoils everything; with a **spreadsheet** it takes minutes, and changing one
mark updates every total, rank and chart at once. Shopkeepers keep their
accounts, families their budgets and offices their salary sheets in the same
way. This lesson builds a working mark sheet step by step: cells and ranges,
entering data, formulas and references, the six functions of the syllabus,
formatting, sorting and filtering, and charts. Commands are for **Microsoft
Excel (Microsoft 365)**, with **LibreOffice Calc** in brackets.

::: key What questions on this lesson ask
Expect definitions of **spreadsheet, workbook, worksheet, cell, cell address,
range, formula, function** and **chart**; counting the **cells in a range**;
writing a **formula or function** for a task and **working out its result**
(SUM, AVERAGE, MAX, MIN, COUNT, IF); the difference between **relative and
absolute references**, and what a formula becomes when it is **copied**; the
steps to **sort, filter** or **insert a chart**; and **which chart** suits given
data. Always begin a formula with **=**, and show the result you expect.
:::

## 8.1 Spreadsheet: workbook, worksheet, row, column, cell, cell address and range

::: definition Spreadsheet
A **spreadsheet** is application software that stores data in a **grid of rows
and columns** and **calculates** with it automatically using formulas and
functions. It is used for calculations, keeping records, analysing data and
drawing charts.
:::

**Examples:** **Microsoft Excel**, **LibreOffice Calc**, **Google Sheets**,
Apple Numbers and WPS Spreadsheets. The first spreadsheet program, **VisiCalc**,
appeared in 1979; Excel followed in 1985.

**Uses:** mark sheets and result analysis, family and school budgets, shop
accounts and bills, salary sheets, stock records, attendance, loan and
interest calculations, and charts for reports.

| Term | Meaning | Example |
|---|---|---|
| **Workbook** | a spreadsheet file; it holds one or more worksheets | `Marks2083.xlsx` (Excel), `.ods` (Calc) |
| **Worksheet** (sheet) | one grid of rows and columns, chosen by its **sheet tab** at the bottom | Sheet1, Term 1, Term 2 |
| **Row** | a horizontal line of cells, numbered 1, 2, 3 … | Excel has 1,048,576 rows |
| **Column** | a vertical line of cells, lettered A, B, … Z, AA, AB … | Excel has 16,384 columns, up to XFD |
| **Cell** | the box where a row and a column cross; it holds one item of data | — |
| **Cell address** (reference) | the column letter followed by the row number | **C5** = column C, row 5 |
| **Active cell** | the selected cell, with a thick border; typing goes here | its address shows in the **Name Box** |
| **Range** | a rectangular block of cells, written *first cell* **:** *last cell* | **B2:E6** |

```figure caption="A worksheet holding a mark sheet. Cell F2 is the active cell: the Name Box shows its address and the formula bar shows the formula inside it, while the cell itself shows the result. The shaded cells B2:E2 are the range the formula adds; the small square at the corner of F2 is the fill handle."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.2, 3.5))
cols = ["A", "B", "C", "D", "E", "F"]
cw = [1.45, 1.05, 1.0, 1.05, 1.3, 0.95]
x0s = [0.45]
for w in cw[:-1]:
    x0s.append(x0s[-1] + w)
rh = 0.36
top = 4.05
data = [["Name", "English", "Maths", "Science", "Computer", "Total"],
        ["Aarati", 78, 85, 92, 88, 343], ["Bibek", 55, 38, 61, 70, 224], ["Chandani", 90, 95, 88, 97, 370],
        ["Dipesh", 42, 35, 30, 55, 162], ["Esha", 66, 72, 58, 80, 276]]
ax.add_patch(Rectangle((0.0, top + 0.45), 1.3, 0.34, fc="white", ec=MUTED, lw=0.8))
ax.text(0.65, top + 0.62, "F2", ha="center", va="center", fontsize=7.6, color=INK)
ax.text(1.55, top + 0.62, "fx", ha="center", va="center", fontsize=7.6, color=MUTED, style="italic")
ax.add_patch(Rectangle((1.8, top + 0.45), 5.0, 0.34, fc="white", ec=MUTED, lw=0.8))
ax.text(1.9, top + 0.62, "=SUM(B2:E2)", ha="left", va="center", fontsize=7.6, color=INK)
for c, (x, w) in enumerate(zip(x0s, cw)):
    ax.add_patch(Rectangle((x, top), w, rh, fc="#e9ecf1" if c != 5 else "#cfdcee", ec=MUTED, lw=0.6))
    ax.text(x + w / 2, top + rh / 2, cols[c], ha="center", va="center", fontsize=7.4, color=INK)
ax.add_patch(Rectangle((0.0, top), 0.45, rh, fc="#e9ecf1", ec=MUTED, lw=0.6))
for r, row in enumerate(data):
    y = top - (r + 1) * rh
    ax.add_patch(Rectangle((0.0, y), 0.45, rh, fc="#e9ecf1" if r != 1 else "#cfdcee", ec=MUTED, lw=0.6))
    ax.text(0.225, y + rh / 2, str(r + 1), ha="center", va="center", fontsize=7.4, color=INK)
    for c, (x, w) in enumerate(zip(x0s, cw)):
        fc = "white"
        if r == 1 and 1 <= c <= 4:
            fc = "#fdf1d6"
        ax.add_patch(Rectangle((x, y), w, rh, fc=fc, ec=GRID, lw=0.6))
        v = row[c]
        bold = (r == 0)
        if isinstance(v, str):
            ax.text(x + 0.08, y + rh / 2, v, ha="left", va="center", fontsize=7.2, color=INK,
                    fontweight="bold" if bold else "normal")
        else:
            ax.text(x + w - 0.08, y + rh / 2, str(v), ha="right", va="center", fontsize=7.2, color=INK)
yF2 = top - 2 * rh
ax.add_patch(Rectangle((x0s[5], yF2), cw[5], rh, fc="none", ec=SERIES[2], lw=1.8, zorder=5))
ax.add_patch(Rectangle((x0s[5] + cw[5] - 0.06, yF2 - 0.06), 0.12, 0.12, fc=SERIES[2], ec="white", lw=0.5, zorder=6))
def lab(tx, ty, px, py, t, ha="left"):
    ax.annotate(t, xy=(px, py), xytext=(tx, ty), fontsize=7.0, color=SERIES[1], ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color=SERIES[1], lw=0.7, shrinkA=1, shrinkB=0,
                                relpos=(0, 0.5) if ha == "left" else (1, 0.5)))
lab(7.25, top + 0.62, 6.82, top + 0.62, "formula bar")
lab(1.5, top + 1.12, 0.9, top + 0.8, "Name Box (cell address)")
lab(7.25, yF2 + 0.18, x0s[5] + cw[5] + 0.02, yF2 + 0.18, "active cell F2 = 343")
lab(7.25, yF2 - 0.4, x0s[5] + cw[5] + 0.05, yF2 - 0.05, "fill handle")
lab(7.25, top + 0.18, x0s[5] + cw[5], top + 0.18, "column headings")
lab(-0.15, top - 3.5 * rh, 0.02, top - 3.5 * rh, "row\nheadings", ha="right")
ax.set_xlim(-1.1, 9.7); ax.set_ylim(top - 6.4 * rh, top + 1.3); ax.axis("off")
```

The **formula bar** shows what is really inside the active cell — a typed
value or a formula — while the cell shows the **result**. The **status bar**
at the bottom shows the **Average, Count and Sum** of the selected cells. The
Excel ribbon has the tabs File, Home, Insert, Draw, Page Layout, **Formulas**,
**Data**, Review, View, Automate and Help.

### Counting the cells in a range

A range from column *X* to column *Y* and row *m* to row *n* has
(number of columns) × (number of rows) cells. Several separate ranges are
joined with a comma: `A1:A5,C1:C5`.

::: example Worked example 8.1 — cells in a range
**Problem.** How many cells are in (a) B2:D6, (b) A1:E1, (c) C3:C12,
(d) A1:B3,D1:D3? (e) Write the address of the cell in the 5th column and the
12th row.

**Solution.** (a) Columns B, C, D = 3; rows 2 to 6 = 5; cells = 3 × 5 =
**15**. (b) Columns A to E = 5; one row: **5**. (c) One column; rows 3 to 12 =
12 − 3 + 1 = 10: **10**. (d) A1:B3 has 2 × 3 = 6 cells and D1:D3 has 3, so
**9**. (e) The 5th column is E, so **E12**.
:::

```photo id="cs8/calc-sum" caption="LibreOffice Calc with cell C1 active. The cell shows the result, 2, while the formula bar shows the formula =SUM(A1,B1) that produced it. The Functions sidebar lists the functions of this lesson: SUM, AVERAGE, MIN, MAX and IF." width="96"
crop 0.0 0.0 1.0 0.894
call 0.13 0.60 0.07 0.745 "Name Box"
call 0.42 0.60 0.30 0.745 "formula bar"
call 0.30 0.47 0.20 0.66 "active cell C1"
call 0.14 0.33 0.03 0.33 "row numbers"
call 0.30 0.15 0.14 0.07 "sheet tab"
call 0.62 0.15 0.77 0.035 "status bar: average and sum"
call 0.66 0.50 0.82 0.57 "list of functions"
```

```photogrid label="8.H" cols="4" ratio="1.25" caption="Tables of numbers behind everyday Nepali scenes. (a) A barcode gives the shop a product code, which is looked up in a price table. (b) A QR payment terminal records each sale as a row of data. (c) An ATM works on account tables. (d) A smart electricity meter produces a table of readings that becomes the bill. Whenever data come in rows and columns and are added, averaged or compared, a spreadsheet is the tool."
@ photo id="bca103/ean13" cap="(a) Barcode: product code"
@ photo id="bca101/qrpay" cap="(b) QR payment: sales rows"
@ photo id="bca101/atm-nepal" cap="(c) ATM: account tables"
@ photo id="bca101/smartmeter" cap="(d) Smart meter: readings"
```

## 8.2 Entering and editing data; data types; AutoFill

**Entering data.** Click a cell (or move to it with the arrow keys), type, and
press **Enter** (the next cell down becomes active) or **Tab** (the next cell to
the right). Press **Esc** to cancel what you are typing.

**Editing data.** Click the cell and type again to **replace** its contents.
To **change** part of it, double-click the cell or press **F2** (or click in the
formula bar), edit, and press Enter. **Delete** clears the contents of the
selected cells; **Ctrl + Z** undoes.

### Data types

| Type | What it is | Example | Lines up |
|---|---|---|---|
| Text (label) | letters, or numbers not used for calculation | Name, Kathmandu, Grade 8 | left |
| Number | values used in calculations | 85, 12.5, −40 | right |
| Currency, percentage | numbers with a format | Rs 1,200.00, 13% | right |
| Date and time | stored as numbers, so they can be subtracted | 24-10-2026, 10:30 | right |
| Formula | begins with `=`; shows its result | `=B2+C2` | result's type |
| Logical (Boolean) | TRUE or FALSE, the answer of a comparison | `=B2>=40` gives TRUE | centre |

A number that should be kept as text, such as a roll number like `008`, is
typed with an apostrophe in front: `'008`.

When something is wrong, the cell shows an **error value**:

| Error | Meaning | Fix |
|---|---|---|
| `#####` | the column is too narrow to show the number | widen the column |
| `#DIV/0!` | a number is divided by zero or by an empty cell | check the divisor |
| `#NAME?` | a misspelled function or name, e.g. `=SUMM(A1:A5)` | correct the spelling |
| `#VALUE!` | text used where a number is needed | check the cells used |
| `#REF!` | the formula refers to a cell that was deleted | rewrite the reference |

### AutoFill

The **fill handle** is the small square at the bottom-right corner of the
active cell or selection. Dragging it **copies** the contents to the next cells
or **continues a series**:

| Type in the first cell(s) | Drag the fill handle to get |
|---|---|
| 1, 2 (two cells selected) | 3, 4, 5, 6 … |
| 5, 10 | 15, 20, 25 … |
| Sunday | Monday, Tuesday, Wednesday … |
| Jan | Feb, Mar, Apr … |
| Grade 1 | Grade 2, Grade 3 … |
| a formula `=B2+C2` | `=B3+C3`, `=B4+C4` … (Section 8.3) |
| any other single value, e.g. 7 | 7, 7, 7 … (a copy) |

Double-clicking the fill handle fills a formula down as far as the data beside
it goes. For more control: Home → **Fill → Series** (Calc: Sheet → Fill Cells
→ Fill Series).

## 8.3 Formulas and operators; relative and absolute cell references

::: definition Formula
A **formula** is an instruction that calculates a value. It always **begins
with an equal sign (=)** and may contain numbers, **cell references**,
**operators** and **functions**, e.g. `=B2+C2+D2` or `=F2/400*100`.
:::

Because a formula uses **cell references** instead of fixed numbers, it is
**recalculated automatically** whenever any of those cells changes.

| Kind | Operator | Meaning | Example | Result |
|---|---|---|---|---|
| Arithmetic | `+` `-` | add, subtract | `=12+8-5` | 15 |
| | `*` `/` | multiply, divide | `=6*4/3` | 8 |
| | `^` | power | `=2^5` | 32 |
| | `%` | per cent | `=200*13%` | 26 |
| Comparison | `=` `<>` | equal, not equal | `=5<>3` | TRUE |
| | `>` `<` `>=` `<=` | greater, less, at least, at most | `=38>=40` | FALSE |
| Text | `&` | join text | `="Ram "&"Thapa"` | Ram Thapa |
| Reference | `:` | range | `=SUM(A1:A5)` | — |
| | `,` | union (several ranges) | `=SUM(A1:A5,C1:C5)` | — |

**Order of operations.** As in mathematics (BODMAS): **brackets first**, then
**%** and **^**, then **× and ÷** from left to right, then **+ and −** from left
to right.

::: example Worked example 8.2 — formulas and their results
**Problem.** Work out the result of each formula: (a) `=2+3*4`,
(b) `=(2+3)*4`, (c) `=20-12/4`, (d) `=2^3*5`. (e) Cells B2, C2, D2 and E2 hold
78, 85, 92 and 88. Write a formula for the average of the four marks and give
its result. (f) What is wrong with `=B2+C2+D2+E2/4`?

**Solution.** (a) Multiplication first: 3 × 4 = 12; 2 + 12 = **14**.
(b) Brackets first: 5 × 4 = **20**. (c) 12 ÷ 4 = 3; 20 − 3 = **17**.
(d) 2³ = 8; 8 × 5 = **40**.
(e) `=(B2+C2+D2+E2)/4` = 343 ÷ 4 = **85.75**.
(f) Only E2 is divided by 4, giving 78 + 85 + 92 + 22 = 277 — wrong. The
brackets are needed.
:::

### Relative and absolute references

When a formula is **copied** to another cell — with Copy and Paste or by
dragging the fill handle — its references change.

::: definition Relative and absolute references
A **relative reference** such as **B2** changes by the same number of rows and
columns as the formula moves when it is copied. An **absolute reference** such
as `$B$1` has a dollar sign before the column letter and the row number and
**does not change** when the formula is copied. In a **mixed reference**
(`$B1` or `B$1`) only the part with the dollar sign is fixed.
:::

Press **F4** in Excel (Shift + F4 in Calc) while the cursor is in a reference
to cycle through `B1 → $B$1 → B$1 → $B1`.

```figure caption="Copying a formula down with the fill handle. A relative reference (B2, C2) changes row by row as it is copied; an absolute reference to B1, written with dollar signs, stays locked on the same cell. The red text beside each sheet shows the formula in each result cell."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.6))
def sheet(ax, title, rows, formulas, widths, hl):
    ax.set_title(title, fontsize=7.8, pad=4)
    xs = [0]
    for w in widths[:-1]:
        xs.append(xs[-1] + w)
    for r, row in enumerate(rows):
        y = -r * 0.5
        for c, v in enumerate(row):
            fc = "#e9ecf1" if r == 0 or c == 0 else "white"
            if (r, c) in hl:
                fc = "#fdf1d6"
            ax.add_patch(Rectangle((xs[c], y), widths[c], 0.5, fc=fc, ec=GRID, lw=0.6))
            ax.text(xs[c] + widths[c] / 2, y + 0.25, str(v), ha="center", va="center", fontsize=7.0, color=INK,
                    fontweight="bold" if r == 0 or c == 0 else "normal")
    for r, f in formulas:
        y = -r * 0.5
        ax.text(xs[-1] + widths[-1] + 0.1, y + 0.25, f, ha="left", va="center", fontsize=6.9, color=SERIES[1])
    ax.set_xlim(-0.05, xs[-1] + widths[-1] + 2.6); ax.set_ylim(-len(rows) * 0.5 + 0.4, 0.55); ax.axis("off")
sheet(axs[0], "Relative reference",
      [["", "B", "C", "D"], ["2", 10, 4, 40], ["3", 7, 5, 35], ["4", 6, 9, 54]],
      [(1, "D2: =B2*C2"), (2, "D3: =B3*C3"), (3, "D4: =B4*C4")], [0.45, 0.75, 0.75, 0.75], {(1, 3), (2, 3), (3, 3)})
sheet(axs[1], "Absolute reference",
      [["", "A", "B", "C"], ["1", "VAT", "13%", ""], ["4", "", 1200, 156], ["5", "", 850, 110.5], ["6", "", 2500, 325]],
      [(2, "C4: =B4*\\$B\\$1"), (3, "C5: =B5*\\$B\\$1"), (4, "C6: =B6*\\$B\\$1")], [0.45, 0.7, 0.75, 0.75], {(1, 2), (2, 3), (3, 3), (4, 3)})
fig.subplots_adjust(wspace=0.05)
```

::: example Worked example 8.3 — VAT with an absolute reference
**Problem.** A shop keeps the VAT rate **13%** in cell **B1**. The prices of
four items are in **B4:B7**: 1200, 850, 2500 and 640 rupees. (a) Write a
formula for the VAT on the first item in C4 that can be copied down to C7, and
give the four results. (b) Write a formula in D4 for the price with VAT, copy
it down, and find the grand total in D8. (c) What goes wrong if C4 holds
`=B4*B1` and is copied down?

**Solution.** (a) C4: `=B4*$B$1`. Copied down it becomes `=B5*$B$1`,
`=B6*$B$1`, `=B7*$B$1`. Results: 1200 × 13% = **156**; 850 × 13% = **110.5**;
2500 × 13% = **325**; 640 × 13% = **83.2**.
(b) D4: `=B4+C4`, copied down: **1356**, **960.5**, **2825**, **723.2**. D8:
`=SUM(D4:D7)` = **5864.7** rupees.
(c) With the relative `B1`, the copy in C5 becomes `=B5*B2`, C6 becomes
`=B6*B3` and so on — pointing at empty cells, so the VAT shows **0**. The `$`
signs keep every copy pointing at B1.
:::

## 8.4 Functions: SUM, AVERAGE, MAX, MIN, COUNT and IF

::: definition Function
A **function** is a ready-made formula with a name that does a particular
calculation. It is written `=NAME(arguments)`, where the **arguments** — the
values or ranges it works on — are written in brackets and separated by commas.
:::

| Function | What it returns | Example (B2:B6 hold 78, 55, 90, 42, 66) | Result |
|---|---|---|---|
| `SUM` | the total of the numbers | `=SUM(B2:B6)` | 331 |
| `AVERAGE` | the mean (sum ÷ how many numbers) | `=AVERAGE(B2:B6)` | 66.2 |
| `MAX` | the largest number | `=MAX(B2:B6)` | 90 |
| `MIN` | the smallest number | `=MIN(B2:B6)` | 42 |
| `COUNT` | how many cells contain **numbers** | `=COUNT(B2:B6)` | 5 |
| `IF` | one value if a condition is TRUE, another if FALSE | `=IF(B2>=40,"Pass","Fail")` | Pass |

The **AutoSum** button (Σ) on the Home tab, or **Alt + =**, writes a SUM of the
numbers above or to the left for you; its arrow offers Average, Count Numbers,
Max and Min. (Calc: the Σ button beside the formula bar. In Calc the
separator between arguments may be a semicolon: `=IF(B2>=40;"Pass";"Fail")`.)

**The IF function** has three arguments:

`=IF(condition, value_if_true, value_if_false)`

- the **condition** is a comparison that is TRUE or FALSE, e.g. `G2>=40`;
- text answers are written in **double quotes**: `"Pass"`;
- numbers and formulas need no quotes: `=IF(B2>1000,B2*5%,0)` gives a 5%
  discount only on bills above Rs 1,000.

::: example Worked example 8.4 — a complete mark sheet
**Problem.** The mark sheet in Figure 1 has names in A2:A6 and marks out of 100
in English (B), Maths (C), Science (D) and Computer (E). (a) Write the formulas
for the total in F2 and the percentage in G2, and give the results for all five
students. (b) The school rule is that a student passes only with **at least 40
in every subject**. Write a formula for the result in H2. (c) Write formulas for
the highest total, the lowest total, the class average of the totals and the
number of students. (d) Bibek's Maths mark, 38, is corrected to 48. What
changes?

**Solution.**
(a) F2: `=SUM(B2:E2)`; G2: `=F2/400*100`. Fill both down to row 6.

| Name | English | Maths | Science | Computer | Total | % | Result |
|---|---|---|---|---|---|---|---|
| Aarati | 78 | 85 | 92 | 88 | 343 | 85.75 | Pass |
| Bibek | 55 | 38 | 61 | 70 | 224 | 56 | Fail |
| Chandani | 90 | 95 | 88 | 97 | 370 | 92.5 | Pass |
| Dipesh | 42 | 35 | 30 | 55 | 162 | 40.5 | Fail |
| Esha | 66 | 72 | 58 | 80 | 276 | 69 | Pass |

(b) H2: `=IF(MIN(B2:E2)>=40,"Pass","Fail")` — MIN finds the lowest mark; if even
that is 40 or more, every mark is. Bibek (38 in Maths) and Dipesh (30 and 35)
fail.
(c) `=MAX(F2:F6)` = **370**; `=MIN(F2:F6)` = **162**; `=AVERAGE(F2:F6)` = 1375 ÷ 5
= **275**; `=COUNT(F2:F6)` = **5**.
(d) Bibek's total becomes 234, his percentage 58.5 and his result **Pass**; the
class average becomes 277 — all **recalculated automatically**.
:::

::: caution Three formula mistakes that lose marks
**Forgetting the `=`**: `SUM(B2:E2)` is stored as text and shows itself.
**Using the wrong signs**: multiply is `*` and divide is `/`, never × or ÷, and
a range uses a **colon**, `B2:E2`, not a dash. **Testing the percentage
instead of every subject**: `=IF(G2>=40,"Pass","Fail")` would pass Dipesh
(40.5%) although he failed three subjects. Read the rule, then choose the
formula.
:::

**COUNT counts only numbers.** If D5 holds the word *Absent* instead of a mark,
`=COUNT(D2:D6)` gives **4**, not 5, and AVERAGE divides by 4.

**Nested IF.** One IF can be placed inside another to choose among more than two
answers. For a grade: `=IF(G2>=80,"A",IF(G2>=60,"B",IF(G2>=40,"C","D")))`
gives A for Aarati (85.75) and Chandani (92.5), B for Esha (69), and C for
Bibek (56) and Dipesh (40.5).

## 8.5 Formatting cells; sorting and filtering data

### Formatting cells

Formatting changes how cells **look**, not the values inside them. Select the
cells, then use the **Home** tab or **Format Cells** (**Ctrl + 1**). (Calc:
Format → Cells, also Ctrl + 1.)

| Group / dialog tab | What you can set |
|---|---|
| Font | font, size, bold, italic, colour |
| Alignment | left, centre, right; top, middle, bottom; **Wrap Text**; **Merge & Center** for a title across columns; text direction |
| Number | General, Number (decimal places), **Currency** (Rs), Percentage, Date; Increase/Decrease Decimal; thousands separator |
| Border and Fill | lines around cells; background colour |
| Cells → Format | **column width**, **row height**, AutoFit |

**Conditional formatting** colours cells automatically by their value: Home →
**Conditional Formatting → Highlight Cells Rules → Less Than…** → type 40 →
choose *Light Red Fill* shows every failing mark in red. (Calc: Format →
Conditional → Condition.)

::: caution Formatting does not change the value
If a cell holds 85.756 and is formatted with one decimal place, it **shows**
85.8 but still **holds** 85.756, and formulas use 85.756. Likewise 0.13
formatted as a percentage shows 13% — so type 13% (or 0.13), not 13, in a cell
that will be multiplied.
:::

### Sorting

**Sorting** arranges rows in **ascending** (A→Z, smallest first) or
**descending** (Z→A, largest first) order of one column.

1. Click any cell in the table (or select the whole table with its headings).
2. **Data → Sort**. Tick *My data has headers*.
3. **Sort by:** Total; **Order:** Largest to Smallest. Click **Add Level** to sort
   ties by a second column. Click **OK**.

The quick buttons **Sort A to Z / Z to A** (Calc: Data → Sort Ascending / Sort
Descending) sort by the column of the active cell.

::: caution Sort the whole table, not one column
If only the Total column is selected and sorted, the totals move but the names
do not, so every total is given to the wrong student. If Excel asks, choose
**Expand the selection**.
:::

### Filtering

**Filtering** shows only the rows that meet a condition and **hides** the rest
(nothing is deleted).

1. Click inside the table. **Data → Filter** (**Ctrl + Shift + L**); a drop-down
   arrow appears in each heading. (Calc: Data → AutoFilter.)
2. Click the arrow of a column, then tick the values you want, or choose
   **Number Filters → Greater Than Or Equal To…** and type a value.
3. Row numbers of a filtered list turn blue; click the arrow → **Clear Filter**
   to show all rows again.

::: example Worked example 8.5 — sort and filter the mark sheet
**Problem.** Using the mark sheet of Worked example 8.4: (a) list the students
after sorting by Total, largest to smallest; (b) which students remain if the
Maths column is filtered with *Greater Than Or Equal To 60*?

**Solution.** (a) Chandani 370, Aarati 343, Esha 276, Bibek 224, Dipesh 162.
(b) Only rows with Maths ≥ 60 are shown: **Aarati (85), Chandani (95) and Esha
(72)**. Bibek (38) and Dipesh (35) are hidden, not deleted.
:::

```photo id="cs8/calc-window" caption="A formatted worksheet in LibreOffice Calc: heading cells with coloured fill and borders, numbers with one decimal place, and line charts drawn from the data. The menus along the top (File, Edit, View, Insert, Format, Sheet, Data …) hold the same commands as Excel's ribbon." width="96"
mark 0.44 0.922 "1"
mark 0.955 0.835 "2"
mark 0.045 0.577 "3"
mark 0.84 0.575 "4"
mark 0.27 0.067 "5"
key 1 Menu bar
key 2 Formatting toolbar: font, bold, alignment, number formats, borders
key 3 Heading cells formatted with fill colour, bold text and borders
key 4 Line charts made from the table
key 5 Sheet tabs: this workbook has two worksheets
```

## 8.6 Charts: column, bar, line and pie

::: definition Chart
A **chart** (graph) is a picture of worksheet data that makes comparisons and
trends easy to see. It is **linked** to its data: change a number and the chart
redraws itself.
:::

**Parts of a chart:** **chart title**; **axes** (the horizontal *category* axis
and the vertical *value* axis) with **axis titles**; **data series** (the bars,
line or slices); **data labels** (the numbers on them); **legend** (which colour
means what); **gridlines**; and the **plot area**.

```figure caption="The same kinds of data drawn with the four basic chart types. Column and bar charts compare separate items; a line chart shows how a value changes over time; a pie chart shows how a whole is divided into parts."
import numpy as np, matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 2, figsize=(5.2, 4.2))
a = axs[0][0]
subj = ["English", "Maths", "Science", "Computer"]; m = [78, 85, 92, 88]
a.bar(subj, m, color=ACCENT, width=0.6)
for i, v in enumerate(m):
    a.text(i, v + 2, str(v), ha="center", va="bottom", fontsize=6.8, color=INK)
a.set_ylim(0, 110); a.set_title("Column: Aarati's marks", fontsize=7.8)
a.tick_params(axis="x", labelsize=6.8, rotation=0); a.tick_params(axis="y", labelsize=6.8)
b = axs[0][1]
sp = ["Football", "Cricket", "Volleyball", "Badminton", "Table tennis"]; n = [18, 12, 7, 5, 3]
b.barh(sp[::-1], n[::-1], color=SERIES[2], height=0.6)
for i, v in enumerate(n[::-1]):
    b.text(v + 0.4, i, str(v), va="center", fontsize=6.8, color=INK)
b.set_xlim(0, 22); b.set_title("Bar: favourite sport (45 students)", fontsize=7.8)
b.tick_params(labelsize=6.8)
c = axs[1][0]
days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri"]; v = [45, 52, 38, 60, 72, 30]
c.plot(days, v, color=SERIES[1], marker="o", ms=3.5)
c.set_ylim(0, 85); c.set_title("Line: library visitors in a week", fontsize=7.8)
c.tick_params(labelsize=6.8); c.grid(axis="y", color=GRID, lw=0.6)
d = axs[1][1]
lab = ["Food", "Rent", "Education", "Transport", "Others"]; e = [12000, 8000, 6000, 3000, 1000]
w, t = d.pie(e, colors=SERIES[:5], startangle=90, counterclock=False,
             wedgeprops=dict(edgecolor="white", linewidth=0.8))
pct = [40, 26.7, 20, 10, 3.3]
for wd, L, p in zip(w, lab, pct):
    mid = np.radians((wd.theta1 + wd.theta2) / 2)
    if p >= 20:
        d.text(0.6 * np.cos(mid), 0.6 * np.sin(mid), f"{L}\n{p:g}%", ha="center", va="center", fontsize=6.6,
               color="white", linespacing=1.05)
    else:
        x, y = 1.18 * np.cos(mid), 1.18 * np.sin(mid)
        d.text(x, y, f"{L} {p:g}%", ha="right" if x < -0.2 else "left", va="center", fontsize=6.6, color=INK)
d.set_title("Pie: a family's monthly spending", fontsize=7.8)
d.set_aspect("equal"); d.set_xlim(-1.9, 1.3); d.set_ylim(-1.15, 1.45)
for ax in (a, b, c):
    ax.spines[["top", "right"]].set_visible(False)
fig.subplots_adjust(hspace=0.55, wspace=0.45)
```

| Chart | Looks like | Best for | Example |
|---|---|---|---|
| **Column** | vertical bars | comparing separate items or groups | marks in each subject; sales of each shop |
| **Bar** | horizontal bars | comparing items, especially with long names | votes for each sport or candidate |
| **Line** | points joined by a line | **change over time** (a trend) | temperature through a week; monthly savings |
| **Pie** | a circle cut into slices | **parts of one whole**, as percentages | how a family's income is spent |

**Inserting a chart in Excel**

1. Select the data **with its labels**, e.g. A1:B6 (subjects in A, marks in B).
2. **Insert → Recommended Charts**, or choose a type in the **Charts** group:
   *Insert Column or Bar Chart*, *Insert Line*, *Insert Pie*.
3. With the chart selected, the **Chart Design** tab offers **Add Chart
   Element** (Chart Title, Axis Titles, Data Labels, Legend), **Chart Styles**,
   **Switch Row/Column**, **Change Chart Type** and **Move Chart** (to its own
   sheet). The **+** button beside the chart turns elements on and off.
4. Click the title on the chart and type a meaningful one.

(Calc: select the data → **Insert → Chart** → the **Chart Wizard** asks for the
chart type, data range, data series and chart elements → Finish.)

::: example Worked example 8.6 — the pie chart's angles
**Problem.** A family spends Rs 12,000 on food, Rs 8,000 on rent, Rs 6,000 on
education, Rs 3,000 on transport and Rs 1,000 on other things in a month.
(a) Which chart shows how the money is shared out? (b) Work out the percentage
and the angle of each slice, as the spreadsheet does. (c) Write the formulas if
the amounts are in B2:B6.

**Solution.** (a) A **pie chart**: the data are parts of one whole.
(b) Total = 12,000 + 8,000 + 6,000 + 3,000 + 1,000 = **Rs 30,000**.
Food: 12,000 ÷ 30,000 = **40%**, angle 0.40 × 360° = **144°**.
Rent: 8,000 ÷ 30,000 ≈ **26.7%**, angle **96°**.
Education: **20%**, angle **72°**. Transport: **10%**, angle **36°**.
Others: ≈ **3.3%**, angle **12°**. Check: 144 + 96 + 72 + 36 + 12 = 360°.
(c) B7: `=SUM(B2:B6)`; C2: `=B2/$B$7` formatted as Percentage, filled down;
D2: `=B2/$B$7*360`, filled down. The `$` keeps every row dividing by the total.
:::

::: note Activity 8.1 — your class mark sheet
In the lab, build the mark sheet of Worked example 8.4 for ten classmates
(use your own unit-test marks with their permission, or invented ones). Use
AutoFill for the roll numbers, SUM, percentage, MAX, MIN, AVERAGE and COUNT, an
IF for the result and a nested IF for the grade. Format it with a merged,
centred title, borders and conditional formatting for marks below 40. Sort it by
total, filter the students above 60% in Computer, and make a column chart of
your own marks. Save it as `Marksheet.xlsx`.
:::

::: tip Showing working in a formula question
Write the **formula** exactly as typed — `=AVERAGE(B2:E2)` — and then the
**result** with a line of working: (78 + 85 + 92 + 88) ÷ 4 = 85.75. When a
formula is copied, write the new formula in the new cell, e.g. "`=B4*$B$1` in C4
becomes `=B5*$B$1` in C5".
:::

## Chapter summary

- A **spreadsheet** (Excel, Calc, Google Sheets) calculates with data in rows
  and columns. A **workbook** (.xlsx, .ods) holds **worksheets**; a **cell** is
  where a **row** (number) meets a **column** (letter); its **address** is like
  C5; a **range** is written B2:E6 and has columns × rows cells.
- **Data types:** text (left), numbers (right), currency, percentage, dates,
  formulas, TRUE/FALSE. Errors: `#####`, `#DIV/0!`, `#NAME?`, `#VALUE!`, `#REF!`.
  **AutoFill** with the fill handle copies or continues series.
- **Formulas** start with **=**; operators `+ - * / ^ %`, comparisons
  `= <> > < >= <=`, `&`; brackets first, then ^, then × ÷, then + −.
- **Relative** references (B2) change when copied; **absolute** (`$B$1`) do not;
  mixed `$B1`, `B$1`; F4 toggles.
- **Functions:** `SUM`, `AVERAGE`, `MAX`, `MIN`, `COUNT` (numbers only),
  `IF(condition, if_true, if_false)`; nested IF for grades.
- **Formatting** (Ctrl + 1) changes appearance, not values; **sort** the whole
  table (Data → Sort); **filter** hides rows (Data → Filter).
- **Charts:** column and bar compare items, **line** shows change over time,
  **pie** shows parts of a whole (angle = share × 360°).

## Practice questions

**Group A — Objective (1 mark each)**

1. A spreadsheet file is called a <span class="marks">[1]</span>
   (a) worksheet (b) workbook (c) cell (d) range
2. The address of the cell in column D and row 7 is <span class="marks">[1]</span>
   (a) 7D (b) D7 (c) D:7 (d) 4,7
3. How many cells are in the range B3:D7? <span class="marks">[1]</span>
   (a) 10 (b) 12 (c) 15 (d) 21
4. Every formula must begin with <span class="marks">[1]</span>
   (a) `+` (b) `#` (c) `=` (d) `$`
5. The result of `=10+6/2` is <span class="marks">[1]</span>
   (a) 8 (b) 13 (c) 16 (d) 3
6. Which is an absolute cell reference? <span class="marks">[1]</span>
   (a) `B5` (b) `$B5` (c) `B$5` (d) `$B$5`
7. If B2:B5 hold 10, 20, "Absent" and 30, then `=COUNT(B2:B5)` gives <span class="marks">[1]</span>
   (a) 4 (b) 3 (c) 60 (d) 20
8. `=IF(C2>=40,"Pass","Fail")` when C2 holds 38 gives <span class="marks">[1]</span>
   (a) Pass (b) Fail (c) 38 (d) TRUE
9. The small square at the bottom-right corner of the active cell is the <span class="marks">[1]</span>
   (a) Name Box (b) fill handle (c) formula bar (d) sheet tab
10. A cell shows `#####`. This means <span class="marks">[1]</span>
    (a) the formula is wrong (b) the column is too narrow (c) the value is negative (d) the file is damaged
11. Which chart is best for showing how a whole is divided into parts? <span class="marks">[1]</span>
    (a) line (b) column (c) pie (d) bar
12. The formula `=A2*B1` in C2 is copied to C3. It becomes <span class="marks">[1]</span>
    (a) =A2*B1 (b) =A3*B2 (c) =A3*B1 (d) =B3*C2

::: note Answers to Group A
**1.** (b) — a workbook holds worksheets.
**2.** (b) — column letter, then row number.
**3.** (c) — 3 columns (B, C, D) × 5 rows (3 to 7) = 15.
**4.** (c) — the equal sign.
**5.** (b) — 6 ÷ 2 = 3 first, then 10 + 3 = 13.
**6.** (d) — dollar signs before both the column and the row.
**7.** (b) — COUNT counts only the three numbers.
**8.** (b) — 38 is not ≥ 40, so the FALSE value is shown.
**9.** (b) — the fill handle, used for AutoFill.
**10.** (b) — widen the column to see the number.
**11.** (c) — a pie chart shows parts of a whole.
**12.** (b) — both relative references move down one row.
:::

**Group B — Short answer (2 marks each)**

1. Define cell, cell address and range with an example of each. <span class="marks">[2]</span>
2. Differentiate between a workbook and a worksheet. <span class="marks">[2]</span>
3. Differentiate between a formula and a function, with an example of each. <span class="marks">[2]</span>
4. What is AutoFill? Write what appears when "Monday" is filled down three cells. <span class="marks">[2]</span>
5. Differentiate between relative and absolute cell references. <span class="marks">[2]</span>
6. Cells A1:A4 hold 12, 18, 25 and 5. Write the result of `=SUM(A1:A4)`, `=AVERAGE(A1:A4)`, `=MAX(A1:A4)` and `=MIN(A1:A4)`. <span class="marks">[2]</span>
7. Write an IF function that shows "Eligible" if the age in B2 is 16 or more and "Not eligible" otherwise. <span class="marks">[2]</span>
8. Differentiate between sorting and filtering. <span class="marks">[2]</span>
9. Write any four parts of a chart. <span class="marks">[2]</span>
10. Which chart would you use to show (a) the monthly temperature of Pokhara over a year, (b) the share of votes won by four candidates? Give reasons. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A cell is the box where a row and a column meet, e.g. the cell holding
Aarati's Maths mark. A cell address is its column letter and row number, e.g.
C2. A range is a rectangular block of cells written first:last, e.g. B2:E6.

**2.** A workbook is the whole spreadsheet file (e.g. `Marks.xlsx`); a worksheet
is one grid of rows and columns inside it, chosen by a sheet tab. One workbook
can hold many worksheets.

**3.** A formula is any calculation the user writes, beginning with =, e.g.
`=B2+C2+D2`. A function is a built-in, named formula, e.g. `=SUM(B2:D2)`.
Functions can be used inside formulas.

**4.** AutoFill copies cell contents or continues a series when the fill
handle is dragged. Filling "Monday" down three cells gives **Tuesday,
Wednesday, Thursday**.

**5.** A relative reference (B2) changes when the formula is copied, by the
number of rows and columns moved. An absolute reference (`$B$2`) stays fixed on
the same cell when copied, e.g. a VAT rate in one cell.

**6.** SUM = 12 + 18 + 25 + 5 = **60**; AVERAGE = 60 ÷ 4 = **15**; MAX =
**25**; MIN = **5**.

**7.** `=IF(B2>=16,"Eligible","Not eligible")`.

**8.** Sorting rearranges all the rows in ascending or descending order of a
column; filtering shows only the rows that meet a condition and hides the
others without changing their order.

**9.** Any four: chart title, axes, axis titles, data series (bars, line or
slices), data labels, legend, gridlines, plot area.

**10.** (a) A **line chart**, because temperature changes over time and a line
shows the trend. (b) A **pie chart**, because the votes are parts of one whole
(total votes).
:::

**Group C — Long answer (4 marks each)**

1. Explain any four functions of a spreadsheet with syntax and an example of each. <span class="marks">[4]</span>
2. In a sheet, B2:B6 hold the prices 450, 1200, 880, 2300 and 170 and the discount rate 10% is in E1. (a) Write a formula in C2 for the discount that can be copied down, and give all five results. (b) Write a formula for the price after discount in D2, and find the total of D2:D6. <span class="marks">[2+2]</span>
3. Write the steps to (a) sort a mark sheet by total, largest first, and (b) show only the students who scored at least 60 in Science. <span class="marks">[2+2]</span>
4. Describe the column, line and pie charts with one use of each, and write the steps to insert a column chart. <span class="marks">[3+1]</span>
5. The marks of a student out of 100 are 64, 38, 75, 81 and 57 in B2:F2. Write formulas for the total, the percentage (out of 500), the highest and lowest marks, and a result that is "Pass" only if every mark is at least 40. Give each result. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Any four. `SUM(range)` adds numbers: `=SUM(B2:B6)` gives 331 for 78,
55, 90, 42, 66. `AVERAGE(range)` gives the mean: `=AVERAGE(B2:B6)` = 66.2.
`MAX(range)` gives the largest: `=MAX(B2:B6)` = 90. `MIN(range)` gives the
smallest: `=MIN(B2:B6)` = 42. `COUNT(range)` counts cells with numbers:
`=COUNT(B2:B6)` = 5. `IF(condition, value_if_true, value_if_false)`:
`=IF(B2>=40,"Pass","Fail")` gives Pass for 78.

**2.** (a) C2: `=B2*$E$1` (E1 must be absolute), filled down. Results: 450 ×
10% = **45**; 1200 → **120**; 880 → **88**; 2300 → **230**; 170 → **17**.
(b) D2: `=B2-C2`, filled down: 405, 1080, 792, 2070, 153. Total
`=SUM(D2:D6)` = **4500**.

**3.** (a) Click any cell in the table → Data → Sort → tick *My data has
headers* → Sort by *Total* → Order *Largest to Smallest* → OK. (b) Click in the
table → Data → Filter → click the arrow on the *Science* heading → Number
Filters → Greater Than Or Equal To → type 60 → OK. Only those students' rows are
shown; Clear Filter shows all again.

**4.** *Column chart:* vertical bars comparing separate items — marks in each
subject. *Line chart:* points joined by a line showing change over time —
temperature through a week. *Pie chart:* a circle divided into slices showing
parts of a whole — a family's spending. Steps for a column chart: select the
data with labels → Insert → Insert Column or Bar Chart → 2-D Clustered Column →
add a chart title with Chart Design → Add Chart Element → Chart Title.

**5.** Total: `=SUM(B2:F2)` = 64 + 38 + 75 + 81 + 57 = **315**. Percentage:
`=SUM(B2:F2)/500*100` (or the total's cell /500*100) = **63**. Highest:
`=MAX(B2:F2)` = **81**. Lowest: `=MIN(B2:F2)` = **38**. Result:
`=IF(MIN(B2:F2)>=40,"Pass","Fail")` gives **Fail**, because the lowest mark,
38, is below 40.
:::

**Group D — Extended answers (10 marks each, for deeper revision)**

1. What is a spreadsheet? Explain its eight main features and uses. <span class="marks">[10]</span>
2. A teacher keeps the marks of three students in a spreadsheet. Explain the formulas and functions used to find the total, average, result and highest total. <span class="marks">[10]</span>
3. Differentiate between relative and absolute cell references, with a worked example. <span class="marks">[10]</span>

### Model answer D1: features and uses of a spreadsheet (10 marks)

**Introduction.** A **spreadsheet** is application software that arranges data in rows and columns and calculates with them. A file is a **workbook**, made of **worksheets**; the meeting of a row and a column is a **cell** with an address such as B3. MS Excel, LibreOffice Calc and Google Sheets are examples (Plate 8.H).

1. **Automatic calculation.** When a formula is typed, the answer appears at once. If a number changes, the answer is recalculated without any extra work. A shopkeeper can change a price and see the new bill immediately.
2. **Formulas and functions.** Ready-made functions such as SUM, AVERAGE, MAX, MIN, COUNT and IF do long calculations in one step. A teacher can total the marks of 40 students by copying one formula.
3. **Large capacity.** A worksheet has over a million rows and 16,000 columns, so very large tables can be kept. A municipality can keep the records of thousands of households.
4. **Charts and graphs.** Data can be shown as column, bar, line or pie charts. A chart makes a comparison clear, such as the monthly sales of a shop.
5. **Sorting and filtering.** Data can be arranged in ascending or descending order, or filtered to show only chosen rows. A school can list the students who scored above 80.
6. **Formatting.** Number formats (currency, percentage, date), colours, borders and alignment make a sheet easy to read.
7. **AutoFill and copying.** Series such as 1, 2, 3 or Sunday, Monday can be filled by dragging the fill handle, and formulas can be copied with the references adjusted.
8. **Saving, printing and sharing.** The workbook can be saved, printed or shared online so that several people can edit it together.

**Uses.** Marks sheets, accounts and budgets, salary and billing, attendance, inventory, and science data.

**Conclusion.** A spreadsheet saves time, avoids calculation mistakes and shows data clearly, so it is used in schools, offices, shops and banks.

### Model answer D2: marks sheet with formulas and functions (10 marks)

**Introduction.** A teacher enters the marks of three students in the cells A1 to G4. A **formula** starts with an equals sign (=); a **function** is a ready-made formula such as SUM.

| | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| 1 | Name | Nepali | English | Maths | Total | Average | Result |
| 2 | Asha | 72 | 65 | 80 | 217 | 72.33 | Pass |
| 3 | Bikash | 45 | 38 | 52 | 135 | 45.00 | Pass |
| 4 | Chandra | 88 | 91 | 79 | 258 | 86.00 | Pass |

1. **Total** in E2: `=SUM(B2:D2)` adds 72 + 65 + 80 = 217. Copy it down to E3 and E4.
2. **Average** in F2: `=AVERAGE(B2:D2)` gives 217 ÷ 3 = 72.33.
3. **Result** in G2: `=IF(F2>=40,"Pass","Fail")`. The condition is true because 72.33 is at least 40, so the cell shows Pass. The IF function has three parts: the test, the value if true, and the value if false.
4. **Highest total:** `=MAX(E2:E4)` gives 258, the lowest total `=MIN(E2:E4)` gives 135, and the number of students `=COUNT(E2:E4)` gives 3.
5. **Chart:** select A1:A4 and E1:E4, click **Insert** → **Column Chart** to compare the totals of the three students.

| Function | Use | Result here |
|---|---|---|
| SUM | Adds the numbers in a range | 217 |
| AVERAGE | Finds the mean | 72.33 |
| MAX | Largest value | 258 |
| MIN | Smallest value | 135 |
| COUNT | Counts numeric cells | 3 |
| IF | Decides between two answers | Pass |

**Conclusion.** One formula written for the first student can be copied for all, and every answer changes by itself if a mark is corrected.

### Model answer D3: relative and absolute references (10 marks)

**Introduction.** A **cell reference** tells a formula which cell to use. There are two main kinds, and the difference shows when a formula is copied.

**Relative reference.** It changes when the formula is copied to another cell. If `=B2*C2` in D2 is copied to D3, it becomes `=B3*C3`. Because the row moves, the reference moves with it. This is the default (A1 style).

**Absolute reference.** It does not change when copied. A dollar sign is placed before the column letter and the row number, for example `$G$1`. It is typed by pressing **F4** after the cell reference. It is used when one cell, such as a tax rate, must be used by all formulas.

**Worked example.** A shop bill with a 13 percent VAT rate kept in G1 (0.13).

| | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | Item | Rate (Rs) | Quantity | Amount (Rs) | VAT (Rs) |
| 2 | Pen | 20 | 10 | 200 | 26 |
| 3 | Copy | 60 | 5 | 300 | 39 |
| 4 | Ruler | 25 | 4 | 100 | 13 |

- Amount in D2: `=B2*C2` (relative); copied down it gives `=B3*C3`, `=B4*C4`.
- VAT in E2: `=D2*G1` is wrong when copied, because it becomes `=D3*G2`, which points to an empty cell. The correct formula is `=D2*$G$1`; copied down, it is `=D3*$G$1`, always using the same rate.
- Total amount: `=SUM(D2:D4)` = 600, total VAT = 78.

| Point | Relative | Absolute |
|---|---|---|
| Form | B2 | $B$2 |
| When copied | Changes | Stays fixed |
| Use | Row-wise or column-wise calculation | A fixed value such as a rate |
| Shortcut | Default | F4 key |

**Conclusion.** Use a relative reference when each row has its own data, and an absolute reference when every formula must use the same cell.
