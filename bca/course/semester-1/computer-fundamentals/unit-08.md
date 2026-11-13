---
subject: Computer Fundamentals and Applications
grade: BCA Semester 1
unit: 8
title: Laboratory Applications: Word Processor, Spreadsheet, Presentation and Photo Editing
hours: 12
area: BCA 101 · Computer Fundamentals and Applications · Laboratory works (units 2 to 5 of the practical)
---

The TU course carries a practical half: **application packages** for a word processor, a spreadsheet, a presentation and a photo-editing program. Units 1 to 7 teach the theory behind the machine; this unit teaches the *skills* and the concepts that make the menus predictable. Every step is described for Microsoft Office and for the free LibreOffice (Writer, Calc, Impress) and GIMP, because the ideas are the same in all of them. Where a calculation is involved (loan schedules, goal seek, pivot tables, image sizes) it is also done in a short program that was run, so you can check your spreadsheet against a second method.

::: key What this unit gives you
- Word processor: formatting, styles, tables, pictures, hyperlinks, headers and footers, page layout, mail merge, spelling and grammar, macros.
- Spreadsheet: references, functions, charts, validation, protection, templates, what-if tools (data table, goal seek, scenario manager), consolidation, pivot tables, loan amortisation, external data.
- Presentation: structure, masters, layout, transitions and animations, speaker notes, delivery.
- Photo editing: bitmap and vector graphics, resolution, colour depth, file formats, compression, selections, layers, text, web optimisation.
- A lab record checklist.
:::

## 8.1 Word processor

A **word processor** (Microsoft Word, LibreOffice Writer, Google Docs) creates documents in which text is separated from its *formatting*. The most important habit is to format with **styles**, not by hand.

### Creating, editing and formatting

- **Character formatting**: font, size, bold, italic, underline, colour, subscript and superscript (H₂O, x²), case change. **Paragraph formatting**: alignment (left, centre, right, justify), line spacing, indents (left, right, first-line, hanging), space before and after, borders and shading, bullets and numbering.
- **Editing**: select, cut, copy, paste, paste special (unformatted text), undo and redo, **Find and Replace** (with wildcards and formatting), the format painter.
- **Styles**: a style is a named bundle of formatting. Apply *Heading 1*, *Heading 2*, *Normal* and change the look of the whole document by editing the style once. Headings applied with styles also let the program build a **table of contents** (References, Table of Contents) and the navigation pane.
- **Lists**: multilevel numbering (1, 1.1, 1.1.1) linked to heading styles gives automatic section numbers.

### Page layout

**Margins**, orientation (portrait or landscape), paper size (A4, Letter), **columns** (a newsletter layout), section breaks (so one page can be landscape), page breaks, and **headers and footers** with **page numbers** (Insert, Page Number; "different first page" for a title page; "link to previous" off when a section needs a different header).

### Tables, pictures, clip art and hyperlinks

- **Tables**: insert rows and columns, merge and split cells, set borders and shading, align cell text, sort a column, repeat the header row on every page, and use a formula such as `=SUM(ABOVE)`.
- **Pictures, clip art, shapes and WordArt**: insert from file, resize while keeping the aspect ratio, crop, wrap text (in line, square, tight, behind text), add a caption (automatic Figure 1, Figure 2) and alternative text for accessibility.
- **Hyperlinks**: link to a web page, an e-mail address (`mailto:`), another file or a bookmark inside the same document; **cross-references** keep "see Table 2" correct when numbers change.

### Proofing and review

**Spelling and grammar checking** underlines errors; set the proofing language (English or Nepali where a dictionary is installed), add technical words to the custom dictionary and do not accept every suggestion without thinking. **Track changes** and **comments** support editing by several people, and **Word Count**, **Thesaurus** and **Read aloud** help polish. Save regularly, turn on AutoRecover, and export a final copy as PDF so layout does not change on another machine.

### Mail merge

**Mail merge** produces many personalised copies of one letter: a **main document** with merge fields such as `«Name»` and `«Amount»` plus a **data source** (a spreadsheet, a table, a CSV file) with one row per recipient. Steps: (1) start the merge and choose letters, (2) select recipients (the data source), (3) write the letter and insert merge fields, (4) preview results, (5) finish and merge to a new document, to the printer or to e-mail. The program below does the same job in Python so that you can see exactly what the wizard does: it fills each field of the template from one row.

```python
import csv, io

data = io.StringIO("""Name,Course,Fee
Asha Gurung,BCA,95000
Bikash Rai,BIM,88000
Sita Thapa,BCA,95000
""")
template = "Dear {Name}, your {Course} fee of Rs {Fee:,} is due on 15 Magh."

rows = list(csv.DictReader(data))
for row in rows:
    row["Fee"] = int(row["Fee"])
    print(template.format(**row))
print(len(rows), "letters produced from 1 template")
```
```output
Dear Asha Gurung, your BCA fee of Rs 95,000 is due on 15 Magh.
Dear Bikash Rai, your BIM fee of Rs 88,000 is due on 15 Magh.
Dear Sita Thapa, your BCA fee of Rs 95,000 is due on 15 Magh.
3 letters produced from 1 template
```
A merge is only as good as its data: fix blank cells, duplicate people and inconsistent capitalisation in the source *before* merging.

### Macros and advanced editing

A **macro** is a recorded or written sequence of actions that you can replay with a button or shortcut, for example "apply my report style, insert today's date and save". Record it (View, Macros, Record Macro), perform the steps, stop recording, and run it again later; macros are stored as Visual Basic for Applications code (LibreOffice also supports Basic and Python). Because a macro can do anything the user can do, **macro viruses** are a known threat: never enable macros in a document from an unknown sender, and keep the default "disable with notification" setting. Other advanced features are **templates** (.dotx, a document that starts with your layout), **sections**, **footnotes and endnotes**, the **bibliography and citation manager**, **equation editor**, **password protection** and **document inspector** (removes hidden personal data before sharing).

## 8.2 Spreadsheet

A **spreadsheet** (Excel, LibreOffice Calc, Google Sheets) is a grid of **cells** named by column letter and row number (`B3`). A cell holds a number, text, a date, or a **formula** that starts with `=` and recalculates automatically when its inputs change; that automatic recalculation is why a spreadsheet is an excellent tool for "what if" questions.

### References and functions

| Kind | Example | Behaviour when copied one cell down |
|---|---|---|
| Relative | `=B2*C2` | becomes `=B3*C3` |
| Absolute | `=B2*$F$1` | `$F$1` never moves (use for a tax rate) |
| Mixed | `=B$2*$A3` | row or column is locked, the other moves |
| Another sheet | `=Sheet2!B5` | refers to a cell in another worksheet |

Core functions to practise: `SUM`, `AVERAGE`, `MIN`, `MAX`, `COUNT`, `COUNTA`, `COUNTIF`, `SUMIF`, `ROUND`, `IF` (and nested `IF`, `AND`, `OR`), `VLOOKUP` or `XLOOKUP`, `INDEX` with `MATCH`, `LEFT`, `RIGHT`, `MID`, `CONCAT`, `TODAY`, `DATEDIF`, and the financial functions `PMT`, `FV`, `PV`, `RATE`. Typical error values: `#DIV/0!` (division by zero), `#NAME?` (misspelled function), `#REF!` (deleted cell), `#VALUE!` (wrong type), `#N/A` (lookup failed).

### Templates, protection and graphic objects

A **template** is a workbook saved with its formulas, formatting and layout but no data (an invoice, a payslip, a mark sheet); File, New, offers built-in ones, and you can save your own (`.xltx`). **Protecting** a file has two levels: *protect sheet* locks cells (all cells are "locked" by default, but the lock only works after the sheet is protected, so first unlock the input cells, then protect, with an optional password), and *encrypt with password* (File, Info, Protect Workbook) stops the file being opened. You can insert **clip art**, **WordArt**, shapes, pictures and **maps** into a sheet to make a report readable.

### Charts

Choose the chart by the question: a **column or bar** chart compares categories, a **line** chart shows change over time, a **pie** chart shows parts of a whole (use only for up to about five slices that add to 100%), a **scatter** chart shows the relation between two numbers, a **histogram** shows the distribution. Select the data including headings, Insert, Chart; then add a title, axis titles, data labels and a legend only if it helps. Do not truncate the vertical axis of a bar chart (it exaggerates differences) and avoid 3-D effects.

### Data validation

**Data validation** (Data, Validation) restricts what may be typed in a cell: whole numbers between 0 and 100 for marks, a **list** (a drop-down of `BCA, BIM, BBA`), dates within a range, text of a certain length, or a custom formula. Add an input message and an error alert ("Marks must be 0 to 100"). It prevents bad data at the source, which is cheaper than cleaning it later.

### Loan amortisation scheduling

A loan repaid in equal monthly instalments has a fixed payment `PMT = P·r / (1 − (1 + r)^−n)`, where *P* is the amount borrowed, *r* the monthly rate (annual rate ÷ 12) and *n* the number of months. Each month the interest is *r* times the balance still owed; the rest of the payment reduces the balance. In a spreadsheet: `=PMT(12%/12, 60, -500000)` gives the payment; interest is `=IPMT(...)` or `=balance*rate/12`; principal is `=PPMT(...)`; the new balance is the old balance minus the principal. The program reproduces the first rows and the totals for a Rs 5,00,000 loan at 12% a year for 5 years:

```python
P, annual, years = 500000, 0.12, 5
r, n = annual / 12, years * 12
pmt = P * r / (1 - (1 + r) ** -n)
print(f"monthly payment = {pmt:,.2f}")

bal, total_int = P, 0.0
print(f"{'month':>5} {'payment':>10} {'interest':>10} {'principal':>10} {'balance':>12}")
for m in range(1, n + 1):
    interest = bal * r
    principal = pmt - interest
    bal -= principal
    total_int += interest
    if m <= 3 or m == n:
        print(f"{m:5d} {pmt:10,.2f} {interest:10,.2f} {principal:10,.2f} {max(bal, 0):12,.2f}")
print(f"total paid = {pmt * n:,.2f}, total interest = {total_int:,.2f}")
```
```output
monthly payment = 11,122.22
month    payment   interest  principal      balance
    1  11,122.22   5,000.00   6,122.22   493,877.78
    2  11,122.22   4,938.78   6,183.45   487,694.33
    3  11,122.22   4,876.94   6,245.28   481,449.05
   60  11,122.22     110.12  11,012.10         0.00
total paid = 667,333.43, total interest = 167,333.43
```
Check your sheet against this: the last balance must be 0.00 (differences of a few paisa come from rounding the payment to two decimals).

### What-if analysis: data table, goal seek and scenario manager

A **what-if analysis** changes inputs and watches the result. Excel has three tools (Data, What-If Analysis):

- **Data table**: shows a formula's result for a *range of input values*. A one-variable table lists interest rates down a column; a two-variable table lists rates down and years across, with the PMT formula in the corner cell. The sheet fills the grid.
- **Goal seek**: works *backwards*. You name a formula cell, the target value and the one input cell that may change; Excel searches until the formula reaches the target. "How many units must I sell to make a profit of Rs 1,00,000?"
- **Scenario manager**: stores named sets of input values (Best, Expected, Worst) and shows them side by side in a summary report.

The program does the same three things: a two-variable table of monthly payments, a goal seek by bisection (the method of Numerical Methods, Semester 4) and three scenarios.

```python
def pmt(P, annual, years):
    r, n = annual / 12, years * 12
    return P * r / (1 - (1 + r) ** -n)

print("Data table: monthly payment of Rs 5,00,000")
print("rate \\ years      3        5        7")
for rate in (0.10, 0.12, 0.14):
    print(f"{rate:5.0%}      " + "  ".join(f"{pmt(500000, rate, y):7,.0f}" for y in (3, 5, 7)))

price, cost, fixed = 250, 150, 400000
profit = lambda units: units * (price - cost) - fixed
lo, hi = 0.0, 100000.0
for _ in range(60):
    mid = (lo + hi) / 2
    if profit(mid) < 100000:
        lo = mid
    else:
        hi = mid
print(f"Goal seek: units for profit Rs 1,00,000 = {hi:,.1f}")

print("Scenario manager:")
for name, units, p in (("Worst", 3000, 220), ("Expected", 5000, 250), ("Best", 7000, 270)):
    print(f"  {name:9s} units={units} price={p} profit={units * (p - cost) - fixed:,}")
```
```output
Data table: monthly payment of Rs 5,00,000
rate \ years      3        5        7
  10%       16,134   10,624    8,301
  12%       16,607   11,122    8,826
  14%       17,089   11,634    9,370
Goal seek: units for profit Rs 1,00,000 = 5,000.0
Scenario manager:
  Worst     units=3000 price=220 profit=-190,000
  Expected  units=5000 price=250 profit=100,000
  Best      units=7000 price=270 profit=440,000
```
### Consolidation, outlining and external data

**Data, Consolidate** combines ranges from several sheets (the branches' monthly sales) into one summary using `SUM`, `AVERAGE` or `COUNT`, matched by row and column labels. **Outlining and subtotals** (Data, Subtotal after sorting) group rows and add a subtotal for each change in a column, with +/− buttons to collapse detail. **Accessing external data** (Data, Get Data) imports a CSV, a text file, a web table or a database query and can refresh it later, so the sheet acts as a front end to a database.

### Working with a worksheet as a database

A list with one header row and one record per row behaves like a table: **sort** by one or more columns, **filter** with AutoFilter (or advanced filter with criteria), use `DSUM`, `DCOUNT`, `DAVERAGE` (database functions that take a criteria range) and **structured tables** (Insert, Table) that grow automatically and give formulas such as `=SUM(Sales[Amount])`.

### Pivot tables

A **pivot table** summarises a long list without writing formulas. Drag one field to **Rows**, another to **Columns**, a numeric field to **Values** (choose Sum, Count, Average) and optional fields to **Filters**; add a **slicer** for clicking filters and a **pivot chart** for the picture. After the source changes, choose Refresh. The program does the same with the `pandas` library:

```python
import pandas as pd

sales = pd.DataFrame({
    "Branch":  ["Kathmandu", "Pokhara", "Kathmandu", "Pokhara", "Kathmandu", "Biratnagar"],
    "Product": ["Laptop", "Laptop", "Phone", "Phone", "Phone", "Laptop"],
    "Amount":  [120000, 95000, 45000, 52000, 38000, 88000],
})
pt = pd.pivot_table(sales, index="Branch", columns="Product", values="Amount",
                    aggfunc="sum", fill_value=0, margins=True, margins_name="Total")
print(pt)
```
```output
Product     Laptop   Phone   Total
Branch                            
Biratnagar   88000       0   88000
Kathmandu   120000   83000  203000
Pokhara      95000   52000  147000
Total       303000  135000  438000
```
Constructing and analysing a pivot table is a skill the lab explicitly tests: always check that the grand total equals the sum of the source column (here 438,000).

## 8.3 Presentation package

A **presentation** (PowerPoint, Impress, Google Slides) supports a talk; it is not the talk. The theory of why most slides fail is in the reading on PowerPoint in the Professional Communication book; the working rules are these.

- **Structure first**: title, agenda, three to five key points, a summary, questions. One idea per slide, with at most about six short lines; the audience reads faster than you speak, so full sentences compete with you.
- **Slide master and layouts**: edit the *slide master* (View, Slide Master) once to set fonts, colours, logo and footer for every slide; pick a layout (title, title and content, two content, section header) instead of dragging boxes. Use a template with strong contrast and at least 24 pt body text.
- **Content objects**: bullets and numbering, tables, charts linked from a spreadsheet, pictures, shapes and SmartArt (process, hierarchy, cycle), audio and video, hyperlinks and action buttons to jump to a slide.
- **Transitions and animations**: a transition is how one slide *replaces* the previous; an animation is how an *object* appears (entrance), changes (emphasis) or leaves (exit). Use them to reveal a list one point at a time, and use the same effect throughout.
- **Delivery tools**: speaker notes, rehearse timings, Slide Show (F5), Presenter View, handouts, export to PDF. Practise aloud; keep a backup copy on a pen drive and a PDF in case the projector computer cannot open your file.

## 8.4 Photo editing package

### Graphics basics

**Bitmap (raster) graphics** store a picture as a grid of **pixels**, each with a colour value (photographs, screenshots; formats JPEG, PNG, GIF, BMP, TIFF). They are *resolution dependent*: enlarging them shows blocky pixels. **Vector graphics** store shapes as mathematical descriptions (lines, curves, fills; formats SVG, AI, EPS, PDF) and are *resolution independent*: they scale to a signboard without losing sharpness, and are best for logos, icons and diagrams. Programs: GIMP and Adobe Photoshop (bitmap), Inkscape and Illustrator (vector).

```svgfig label="8.1" caption="The same diagonal line as a bitmap and as a vector. Left: a grid of pixels shows steps (aliasing) and gets blockier when enlarged. Right: the vector stores only two end points and a rule, so it stays smooth at any size."
f = Fig(780, 270)
f.text(190, 18, "Bitmap: 12 x 12 pixels", size=11, color=TEAL, bold=True)
s = 18
for r in range(12):
    for c in range(12):
        on = abs(r - c) <= 0
        f.box(30 + c * s, 34 + r * s, s, s, "", fill=(NAVY if on else "#ffffff"), stroke="#cbd5e1", size=8)
f.text(190, 262, "stores 144 colour values", size=10, color=SLATE)
f.text(590, 18, "Vector: two points and a stroke", size=11, color=TEAL, bold=True)
f.line(480, 40, 700, 250, color=NAVY, sw=3)
f.circle(480, 40, 6, fill=SAND, stroke=NAVY)
f.circle(700, 250, 6, fill=SAND, stroke=NAVY)
f.text(525, 30, "(x1, y1)", size=10, color=SLATE)
f.text(660, 245, "(x2, y2)", size=10, color=SLATE, anchor="end")
f.text(590, 262, "stores 4 numbers, scales without loss", size=10, color=SLATE)
```

- **Resolution**: the number of pixels (1920 x 1080) and the **density** in ppi or dpi (pixels or dots per inch). Screens use about 72 to 150 ppi, print needs 300 ppi. Print size in inches is pixels divided by ppi.
- **Colour (bit) depth**: bits per pixel. 1 bit = black and white, 8 bits = 256 colours or greys, 24 bits = **true colour** (8 bits each for red, green and blue, 16.7 million colours), 32 bits adds an 8-bit **alpha** channel for transparency. **Colour models**: RGB (screens, additive) and CMYK (print, subtractive).
- **Uncompressed size** = width x height x bits per pixel ÷ 8 bytes. The program computes it and a print size:

```python
w, h = 1920, 1080
for bits, name in ((1, "black and white"), (8, "256 greys"), (24, "true colour"), (32, "true colour + alpha")):
    size = w * h * bits / 8
    print(f"{name:20s} {bits:2d} bits  {size / 1024 / 1024:6.2f} MB uncompressed")
print(f"printed at 300 ppi: {w / 300:.1f} x {h / 300:.1f} inches")
print(f"one A4 page (8.27 x 11.69 in) at 300 ppi needs {round(8.27 * 300)} x {round(11.69 * 300)} pixels")
```
```output
black and white       1 bits    0.25 MB uncompressed
256 greys             8 bits    1.98 MB uncompressed
true colour          24 bits    5.93 MB uncompressed
true colour + alpha  32 bits    7.91 MB uncompressed
printed at 300 ppi: 6.4 x 3.6 inches
one A4 page (8.27 x 11.69 in) at 300 ppi needs 2481 x 3507 pixels
```
- **File formats**: **JPEG** (lossy, small photographs, no transparency), **PNG** (lossless, transparency, screenshots and logos), **GIF** (256 colours, simple animation), **BMP** (uncompressed), **TIFF** (lossless, printing and archives), **WebP** and **AVIF** (modern, smaller than JPEG at the same quality), **RAW** (sensor data from a camera) and the program's own layered formats (**XCF** in GIMP, **PSD** in Photoshop).
- **Lossy versus lossless compression**: lossless (PNG, GIF, TIFF-LZW) restores every pixel exactly; lossy (JPEG) discards detail the eye barely notices for a much smaller file, but quality drops each time the file is re-saved. Never edit and re-save a JPEG repeatedly; keep a lossless master.
- **Optimising web graphics**: resize to the display size, choose JPEG for photographs and PNG or SVG for flat graphics, reduce quality to 70-85%, strip metadata, and serve modern formats. **Interlaced** (progressive) images appear first as a blurry full picture that sharpens, instead of loading from the top down, so a visitor sees something quickly. **Dithering** simulates colours missing from a small palette (GIF's 256) by mixing dots of neighbouring colours; **non-dithered** images use flat nearest colours and compress better. **Anti-aliased text** smooths jagged edges using partially transparent pixels along the outline; non-anti-aliased text looks sharp-edged and blocky but is used for tiny pixel fonts. **Pixel resize** versus **smart (content-aware) resize**: the first scales everything evenly; the second removes or stretches the least interesting parts so the faces do not distort.

### Core editing tasks

1. **Open, crop, rotate and straighten**; **resize canvas** (more space around the picture) versus **resize image** (change the pixels).
2. **Selections**: rectangle, ellipse, lasso (free hand), **magic wand** (selects similar colours), quick selection, and adjusting with feather (soft edge), grow and invert. A standard selection has a hard edge; a feathered one blends.
3. **Layers**: a stack of transparent sheets, each editable on its own (text on top of a photograph on top of a background); layer opacity, blend modes, masks (paint black to hide, white to reveal) and groups. Keep the layered master (XCF/PSD) and export a flattened JPEG or PNG.
4. **Retouching**: brightness and contrast, levels and curves, hue and saturation, sharpen, blur, clone stamp (copy pixels from one place to another), healing brush (blend a blemish away), red-eye removal.
5. **Text and shapes**: type tool, font, size, colour, anti-aliasing, layer styles (stroke, drop shadow, but use sparingly); **filters** and special effects.
6. **Export for use**: Save As the master, Export As JPEG, PNG or WebP at the right size.

## 8.5 Laboratory record checklist

| Package | Programs you must be able to do from memory |
|---|---|
| Word processor | a formatted report with title page, automatic table of contents, headings by styles, a table, a picture with caption, header, footer and page numbers; a letter with mail merge from a spreadsheet; a recorded macro |
| Spreadsheet | a mark sheet with `SUM`, `AVERAGE`, `IF` grade, `RANK` and data validation; charts of the results; a protected template; a loan schedule with `PMT`; data table, goal seek and scenario summary; a pivot table with a chart; consolidation of two sheets |
| Presentation | a ten-slide talk on a topic with a master, a chart, a table, transitions, animation, notes and a PDF export |
| Photo editing | resize and crop a photograph to a passport size at 300 ppi; remove a background with selection and layer mask; add text on a layer; export one JPEG and one PNG and compare sizes; convert an image to 256-colour GIF with and without dithering |
| Operating system | Windows file management and settings, and the DOS internal and external commands of Unit 3 |

## Formula and fact sheet

- `PMT = P·r / (1 − (1 + r)^−n)` with *r* = annual rate ÷ 12 and *n* = months; the last balance is 0.
- Relative `B2`, absolute `$B$2`; `F4` cycles the reference types.
- Uncompressed image bytes = width x height x bits ÷ 8; true colour = 24 bits; print pixels = inches x ppi.
- Bitmap: pixels, resolution dependent. Vector: shapes, resolution independent.
- JPEG lossy, PNG lossless with transparency, GIF 256 colours, TIFF archival.
- Goal seek changes one input to reach a target; data table shows a range of inputs; scenario manager saves named sets.

## Chapter summary

- A word processor works best with styles, section settings and mail merge; macros automate but must be treated as a security risk.
- A spreadsheet recalculates formulas, so it supports validation, protection, what-if analysis, consolidation and pivot tables.
- A presentation supports a speaker: structure, master slides and restrained effects.
- Bitmap graphics depend on resolution and colour depth; compression and format choice control file size.

## Practice

1. Differentiate relative, absolute and mixed cell references with an example.
2. Write the formula that gives the monthly payment for a loan of Rs 8,00,000 at 10% a year for 4 years.
3. What is mail merge? Name its two documents.
4. Distinguish data table, goal seek and scenario manager.
5. What is a pivot table used for?
6. Why are macros a security risk?
7. Differentiate bitmap and vector graphics with two uses of each.
8. Calculate the uncompressed size of a 1000 x 800 image with 24-bit colour.
9. What is the difference between lossy and lossless compression? Give a format for each.
10. What is a layer? Why do we keep a layered master file?
11. How many pixels are needed to print a 4 x 6 inch photograph at 300 ppi?
12. List four rules for a good presentation slide.

::: note Answers and worked solutions
**1.** `B2` changes when copied; `$B$2` stays fixed; `B$2` fixes only the row, `$B2` fixes only the column. Use absolute for a tax rate cell.
**2.** `=PMT(10%/12, 48, -800000)`; the payment is positive because the loan amount is entered as negative.
**3.** Producing personalised copies of a document from a main document with merge fields and a data source (a spreadsheet or table).
**4.** The data table lists results for many input values; goal seek finds one input that gives a target result; the scenario manager stores named sets of inputs and compares them.
**5.** To summarise and cross-tabulate a long list (totals by branch and product) interactively without formulas.
**6.** A macro can run any action the user can, including deleting files or downloading malware, and documents from strangers can contain malicious macros.
**7.** Bitmap: photographs, screenshots (pixel grid, loses quality when enlarged). Vector: logos, diagrams (shapes, scales without loss).
**8.** 1000 x 800 x 24 / 8 = 2,400,000 bytes = about 2.29 MB (2,343.75 KiB).
**9.** Lossless restores every pixel (PNG); lossy discards some detail for smaller files (JPEG).
**10.** A transparent sheet in a stack that can be edited independently; the layered file (XCF or PSD) keeps everything editable, and the flattened export cannot be undone.
**11.** 4 x 300 = 1200 by 6 x 300 = 1800 pixels, i.e. 2.16 million pixels.
**12.** One idea per slide, large readable text, high contrast, few words, visuals that support the point, consistent master.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). What is mail merge? Explain the steps.**

Mail merge creates many personalised documents from one template. It uses a **main document** (the letter with merge fields such as Name and Amount) and a **data source** (a spreadsheet, table or CSV, one record per row). Steps: choose the document type, select the recipients, write the letter and insert merge fields, preview the results, then merge to a new document, to the printer or to e-mail. Typical uses are invitations, fee notices, certificates and address labels.

**Q (10 marks). Explain the what-if analysis tools of a spreadsheet with an example.**

What-if analysis varies the inputs of a model to study the output. Take a loan of Rs 5,00,000 for 5 years. A **data table** shows the monthly payment for several interest rates and several terms in a grid, using `PMT` in the corner cell. **Goal seek** reverses the question: if the profit formula is `units x (price - cost) - fixed`, goal seek sets the profit cell to 1,00,000 by changing the units cell and reports 5,000 units for price 250, cost 150 and fixed cost 4,00,000. The **scenario manager** saves sets of values called Worst, Expected and Best and shows their results in one summary report. Together they support planning and decision making without rewriting formulas.
