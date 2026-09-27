---
subject: Computer Science
grade: 11
unit: 4
title: Application Package
hours: 5
---

Most people who use a computer never write a line of code. They write letters,
add up columns of figures, make slides and look things up in a database — and
they do it with ready-made **application packages**. This short unit surveys the
four members of the standard office package and then looks at the
**domain-specific** software written for one particular line of work: a school,
a shop, a payroll office, a hotel or a weather service.

::: key What the examiner wants from this unit
Only five teaching hours, but questions appear every year. Be able to name the
four office packages with **two features and two examples of each**, write
correct spreadsheet formulas, define *field*, *record*, *table* and *primary
key*, and describe at least three domain-specific systems in terms of their
**inputs, processing and outputs**.
:::

## 4.1 Introduction to office packages

::: definition Application package
An **application package** (or package software) is ready-made application
software developed for general use and sold to many customers, rather than
written for one organisation. An **office package** (office suite) is a bundle of
such programs that share a common look, a common file format and the ability to
exchange data with each other.
:::

The best known office suites, as of 2025, are **Microsoft 365 / MS Office**
(Word, Excel, PowerPoint, Access, Outlook), the free and open-source
**LibreOffice** (Writer, Calc, Impress, Base), the web-based **Google Workspace**
(Docs, Sheets, Slides), **WPS Office**, and Apple's **iWork** (Pages, Numbers,
Keynote).

```figure caption="Classification of application packages. The office package is general purpose and is used by everybody; domain-specific tools are written for one line of business."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.0))
GRN='#2e8b57'
def box(cx,cy,w,h,t,c,fs=7.2,bold=False):
    ax.add_patch(FancyBboxPatch((cx-w/2,cy-h/2),w,h,
        boxstyle="round,pad=0.02,rounding_size=0.12",fc=c,ec=c,lw=1.1,alpha=0.15,zorder=2))
    ax.add_patch(FancyBboxPatch((cx-w/2,cy-h/2),w,h,
        boxstyle="round,pad=0.02,rounding_size=0.12",fc='none',ec=c,lw=1.1,zorder=3))
    ax.text(cx,cy,t,ha='center',va='center',fontsize=fs,color=INK,zorder=4,
            fontweight='bold' if bold else 'normal')
def link(sx,sy,x,y,c):
    ax.plot([sx,sx,x],[sy,y,y],color=c,lw=1.0,zorder=1)
box(5.65,6.32,5.10,0.60,'APPLICATION PACKAGES',INK,7.8,True)
box(2.40,4.95,4.30,0.58,'General purpose (office)',ACCENT,7.4,True)
box(8.90,4.95,4.30,0.58,'Domain specific tools',GRN,7.4,True)
ax.plot([2.40,2.40,8.90],[5.24,5.72,5.72],color=INK,lw=1.0,zorder=1)
ax.plot([8.90,8.90],[5.72,5.24],color=INK,lw=1.0,zorder=1)
ax.plot([5.65,5.65],[6.02,5.72],color=INK,lw=1.0,zorder=1)
left=['Word processor','Spreadsheet package','Presentation tool','Database (DBMS)']
right=['School management','Inventory management','Payroll system','Financial accounting',
       'Hotel management','Weather forecasting']
for k,name in enumerate(left):
    y=4.05-k*0.72; box(2.70,y,3.70,0.54,name,ACCENT,7.0); link(0.65,4.66,0.85,y,ACCENT)
for k,name in enumerate(right):
    y=4.05-k*0.72; box(9.20,y,3.70,0.54,name,GRN,7.0); link(7.15,4.66,7.35,y,GRN)
ax.set_xlim(0.0,11.35); ax.set_ylim(-0.02,6.73); ax.set_aspect('equal'); ax.axis('off')
```

### (a) Word processor

::: definition Word processor
A **word processor** is application software used to create, edit, format, store
and print text documents such as letters, reports, notices and books.
:::

**Examples:** MS Word, LibreOffice Writer, Google Docs, WPS Writer, Apple Pages.

**Main features**

- Typing with automatic **word wrap**, insert and overtype modes.
- **Editing**: cut, copy, paste, undo/redo, and **find and replace**.
- **Formatting** of characters (font, size, bold, italic, underline, colour),
  paragraphs (alignment, indent, line spacing, bullets and numbering) and pages
  (margins, orientation, size, columns).
- **Styles and templates** so that every heading in a long report looks the same.
- **Tables**, pictures, shapes, charts, equations and symbols.
- **Header and footer** with automatic page numbers.
- **Spelling and grammar check**, thesaurus, word count.
- **Mail merge** — one letter combined with a list of names to produce many
  personalised letters.
- **Track changes and comments** for reviewing, and export to PDF.

```figure caption="A word-processed page with the features that carry marks: margins, header and footer, heading style, justified paragraph, bulleted list, table and automatic page number."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.1,3.0))
PW,PH = 5.00, 6.60
ax.add_patch(Rectangle((0,0),PW,PH,fc='white',ec=INK,lw=1.3,zorder=3))
M=0.60
ax.add_patch(Rectangle((M,M),PW-2*M,PH-2*M,fc='none',ec=ACCENT,lw=0.8,ls=(0,(4,3)),zorder=4))
def rule(y,x0,x1,c=MUTED,lw=2.2,a=0.30):
    ax.plot([x0,x1],[y,y],color=c,lw=lw,alpha=a,solid_capstyle='butt',zorder=5)
ax.text(PW/2,PH-0.32,'Shree Janata Secondary School',ha='center',va='center',
        fontsize=5.4,color=MUTED,zorder=5)
ax.text(PW/2,PH-1.05,'ANNUAL REPORT 2082',ha='center',va='center',
        fontsize=7.2,color=INK,fontweight='bold',zorder=5)
for k in range(4):
    rule(PH-1.55-k*0.24,M,PW-M)
for k in range(3):
    ax.plot([M+0.18],[PH-2.72-k*0.26],'o',ms=2.0,color=INK,zorder=5)
    rule(PH-2.75-k*0.26,M+0.34,PW-M-0.55)
TX,TY,TW,TH = M, 1.75, PW-2*M, 1.05
for r in range(4):
    ax.plot([TX,TX+TW],[TY+r*TH/3,TY+r*TH/3],color=MUTED,lw=0.7,zorder=5)
for c in range(4):
    ax.plot([TX+c*TW/3,TX+c*TW/3],[TY,TY+TH],color=MUTED,lw=0.7,zorder=5)
ax.add_patch(Rectangle((TX,TY+2*TH/3),TW,TH/3,fc=ACCENT,ec='none',alpha=0.18,zorder=4))
for k in range(3):
    rule(1.35-k*0.24,M,PW-M)
ax.text(PW-M,0.34,'Page 1 of 8',ha='right',va='center',fontsize=5.6,color=MUTED,zorder=5)
def call(p,q,t,ha='left'):
    ax.annotate('',xy=p,xytext=q,zorder=7,arrowprops=dict(arrowstyle='-',color=MUTED,lw=0.8))
    ax.text(q[0]+(0.10 if ha=='left' else -0.10),q[1],t,ha=ha,va='center',
            fontsize=6.8,color=MUTED,zorder=7)
call((PW,PH-0.32),(PW+0.35,PH-0.10),'header')
call((PW-M-0.10,PH-1.05),(PW+0.35,PH-0.95),'heading style, centred')
call((PW-M-0.20,PH-1.79),(PW+0.35,PH-1.80),'justified paragraph')
call((PW-M-0.55,PH-2.75),(PW+0.35,PH-2.62),'bulleted list')
call((TX+TW,TY+TH*0.5),(PW+0.35,TY+0.45),'table')
call((PW-M,0.34),(PW+0.35,0.22),'footer with page number')
call((M,PH/2+0.30),(-0.35,PH/2+0.95),'margins','right')
ax.set_xlim(-3.10,9.30); ax.set_ylim(-0.38,6.97); ax.set_aspect('equal'); ax.axis('off')
```

### (b) Spreadsheet package

::: definition Spreadsheet
A **spreadsheet package** is application software that arranges data in a grid of
rows and columns and performs calculations on it automatically using formulas
and built-in functions.
:::

**Examples:** MS Excel, LibreOffice Calc, Google Sheets, WPS Spreadsheets, Apple
Numbers.

A file is a **workbook**; each page of it is a **worksheet**. Columns are named
with letters (A, B, C …), rows with numbers (1, 2, 3 …), and the box where a
column and a row meet is a **cell** whose **address** is the column letter
followed by the row number, such as `C5`. A rectangular block of cells is a
**range**, written `B2:E6`.

```figure caption="Parts of a spreadsheet window. The name box shows the address of the active cell and the formula bar shows what was actually typed into it, not the displayed result."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.1,3.0))
CW,RH = 1.45, 0.42
NC,NR = 6, 6
X0,Y0 = 1.10, 0.55
cols=['A','B','C','D','E','F']
data=[['Name','Comp','Phy','Math','Total','Grade'],
      ['Anisha','78','71','84','233','A'],
      ['Bikash','65','58','70','193','B'],
      ['Chetana','88','82','91','261','A+'],
      ['Dipak','54','61','49','164','C'],
      ['Average','71.3','68.0','73.5','','']]
for c in range(NC):
    x=X0+c*CW
    ax.add_patch(Rectangle((x,Y0+NR*RH),CW,RH,fc=MUTED,ec=INK,lw=0.7,alpha=0.16,zorder=3))
    ax.text(x+CW/2,Y0+NR*RH+RH/2,cols[c],ha='center',va='center',fontsize=7.0,color=INK,zorder=4)
for r in range(NR):
    y=Y0+(NR-1-r)*RH
    ax.add_patch(Rectangle((X0-0.52,y),0.52,RH,fc=MUTED,ec=INK,lw=0.7,alpha=0.16,zorder=3))
    ax.text(X0-0.26,y+RH/2,str(r+1),ha='center',va='center',fontsize=7.0,color=INK,zorder=4)
    for c in range(NC):
        x=X0+c*CW
        ax.add_patch(Rectangle((x,y),CW,RH,fc='white',ec=GRID,lw=0.7,zorder=3))
        ax.text(x+CW/2,y+RH/2,data[r][c],ha='center',va='center',
                fontsize=6.4,color=INK,zorder=4,
                fontweight='bold' if r==0 else 'normal')
ACX,ACY = X0+4*CW, Y0+(NR-1-4)*RH
ax.add_patch(Rectangle((ACX,ACY),CW,RH,fc='none',ec=ACCENT,lw=2.0,zorder=6))
RE = X0+NC*CW
BY = Y0+NR*RH+RH+0.22
ax.add_patch(Rectangle((X0-0.52,BY),1.30,RH,fc='white',ec=INK,lw=0.9,zorder=3))
ax.text(X0-0.52+0.65,BY+RH/2,'E5',ha='center',va='center',fontsize=6.8,color=INK,zorder=4)
ax.add_patch(Rectangle((X0+0.90,BY),RE-X0-0.90,RH,fc='white',ec=INK,lw=0.9,zorder=3))
ax.text(X0+1.05,BY+RH/2,'=SUM(B5:D5)',ha='left',va='center',fontsize=6.8,color=ACCENT,zorder=4)
def call(p,q,t,ha='left'):
    ax.annotate('',xy=p,xytext=q,zorder=7,arrowprops=dict(arrowstyle='-',color=MUTED,lw=0.8))
    ax.text(q[0]+(0.12 if ha=='left' else -0.12),q[1],t,ha=ha,va='center',
            fontsize=7.0,color=MUTED,zorder=7)
call((X0-0.52,BY+RH/2),(X0-0.90,BY+0.92),'name box','right')
call((RE,BY+RH/2),(RE+0.30,BY+0.92),'formula bar')
call((RE,Y0+NR*RH+RH/2),(RE+0.30,Y0+NR*RH+0.30),'column headings')
call((X0-0.52,Y0+2.6*RH),(X0-0.90,Y0+3.5*RH),'row headings','right')
call((RE,ACY+RH/2),(RE+0.30,ACY-0.05),'active cell E5')
ax.set_xlim(-3.10,12.90); ax.set_ylim(0.30,4.75); ax.axis('off')
```

**Main features**

- **Formulas** always begin with `=` and may use the operators `+ - * / ^` and
  the comparison operators.
- **Built-in functions** such as `SUM`, `AVERAGE`, `MAX`, `MIN`, `COUNT`,
  `COUNTIF`, `IF`, `ROUND`, `RANK`, `TODAY`, `VLOOKUP`.
- **Automatic recalculation**: change one number and every dependent cell updates
  at once — this is the whole point of a spreadsheet.
- **Cell references**: *relative* (`B2`, which changes when the formula is
  copied), *absolute* (`$B$2`, which never changes) and *mixed* (`B$2`, `$B2`).
- **Charts** — column, bar, line, pie, scatter — drawn from a range of cells and
  updated automatically.
- Sorting, filtering, conditional formatting, data validation, pivot tables,
  "what-if" analysis and Goal Seek.

::: example Worked example 4.1 — writing the formulas for a marks sheet
**Problem.** A worksheet holds student names in column A and marks in Computer,
Physics and Mathematics in columns B, C and D for rows 2 to 11. Write formulas
to find (a) the total of the first student, (b) the average of the first student,
(c) the highest total in the class, (d) the result "Pass" or "Fail" using a pass
mark of 40 in each subject, and (e) the percentage of the first student when the
full marks per subject is stored in cell `H1`.

**Solution.**

| Cell | Formula | What it does |
|---|---|---|
| `E2` | `=SUM(B2:D2)` | total of the three subjects |
| `F2` | `=AVERAGE(B2:D2)` | mean mark, same as `=E2/3` |
| `G2` | `=MAX(E$2:E$11)` | the highest total in the class |
| `H2` | `=IF(MIN(B2:D2)>=40,"Pass","Fail")` | fails if **any** subject is below 40 |
| `I2` | `=E2/(3*$H$1)*100` | percentage; `$H$1` is absolute so it does not move |

Each formula is then copied down to row 11 by dragging the fill handle. The
relative references `B2:D2` become `B3:D3`, `B4:D4` and so on automatically,
while `$H$1` stays fixed.
:::

::: caution Absolute references and the fill handle
When a formula is copied, a *relative* reference moves with it. If the divisor
or a lookup table must stay put, lock it with dollar signs (`$H$1`). Forgetting
this is the commonest reason a copied column of formulas produces `#DIV/0!` or
nonsense after the first row.
:::

```figure caption="A chart drawn from a range of spreadsheet cells. If a mark in the worksheet is changed, the chart redraws itself immediately."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.6))
names=['Anisha','Bikash','Chetana','Dipak']
comp=[78,65,88,54]; phy=[71,58,82,61]; math=[84,70,91,49]
x=np.arange(len(names)); w=0.26
ax.bar(x-w,comp,width=w,color=SERIES[0],label='Computer')
ax.bar(x,  phy, width=w,color=SERIES[1],label='Physics')
ax.bar(x+w,math,width=w,color=SERIES[2],label='Mathematics')
ax.set_xticks(x); ax.set_xticklabels(names,fontsize=8.0)
ax.set_ylabel('marks obtained',fontsize=8.0); ax.set_ylim(0,110)
ax.tick_params(labelsize=7.6)
ax.legend(fontsize=7.2,frameon=False,ncol=3,loc='upper center')
ax.grid(axis='y',color=GRID,lw=0.6); ax.set_axisbelow(True)
for s in ('top','right'): ax.spines[s].set_visible(False)
fig.tight_layout()
```

### (c) Presentation tool

::: definition Presentation software
**Presentation software** is application software used to create a sequence of
electronic **slides** containing text, pictures, charts, sound and video, which
are displayed one after another to support a talk.
:::

**Examples:** MS PowerPoint, LibreOffice Impress, Google Slides, Prezi, Canva.

**Main features:** slide **layouts** and **placeholders**; design **themes**,
templates and the **slide master** that fixes the look of every slide;
**transitions** between slides and **animations** within a slide; **speaker
notes** and **handouts**; views — Normal, **Slide Sorter**, Reading and
**Slide Show** (`F5`); rehearse timings; insert tables, charts, SmartArt, audio,
video and hyperlinks; and export to PDF or video.

```figure caption="Presentation software. The normal view shows one slide with its placeholders and the speaker notes; the slide sorter view shows the whole deck so that slides can be reordered."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.1,2.8))
def slide(x,y,w,h,ec=INK,lw=1.2,fc='white'):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
SX,SY,SW,SH = 0.20, 1.35, 4.60, 2.60
slide(SX,SY,SW,SH)
ax.add_patch(Rectangle((SX+0.28,SY+SH-0.78),SW-0.56,0.54,fc=ACCENT,ec=ACCENT,
             lw=0.9,alpha=0.20,zorder=4))
ax.text(SX+SW/2,SY+SH-0.51,'Click to add title',ha='center',va='center',
        fontsize=7.6,color=INK,zorder=5)
ax.add_patch(Rectangle((SX+0.28,SY+0.30),SW-0.56,SH-1.24,fc=MUTED,ec=MUTED,
             lw=0.9,alpha=0.12,zorder=4))
for k,tx in enumerate(['Click to add text','second bullet','third bullet']):
    ax.plot([SX+0.55],[SY+SH-1.15-k*0.38],'o',ms=2.4,color=INK,zorder=5)
    ax.text(SX+0.72,SY+SH-1.15-k*0.38,tx,ha='left',va='center',fontsize=6.8,
            color=INK,zorder=5)
ax.add_patch(Rectangle((SX,SY-0.70),SW,0.58,fc=MUTED,ec=MUTED,lw=0.8,alpha=0.10,zorder=3))
ax.text(SX+0.14,SY-0.41,'Speaker notes …',ha='left',va='center',fontsize=6.6,
        color=MUTED,zorder=4)
ax.text(SX+SW/2,SY+SH+0.16,'Normal view',ha='center',va='bottom',fontsize=8.2,
        color=INK,fontweight='bold')
GX,GY,GW,GH = 5.45, 1.35, 1.55, 0.96
for r in range(2):
    for c in range(2):
        x=GX+c*(GW+0.22); y=GY+1.30-r*(GH+0.26)
        slide(x,y,GW,GH,ec=MUTED,lw=0.9)
        ax.add_patch(Rectangle((x+0.10,y+GH-0.28),GW-0.20,0.18,fc=ACCENT,ec='none',
                     alpha=0.30,zorder=4))
        for k in range(2):
            ax.plot([x+0.12,x+GW-0.35],[y+0.34-k*0.16,y+0.34-k*0.16],
                    color=MUTED,lw=1.6,alpha=0.30,solid_capstyle='butt',zorder=4)
        ax.text(x+GW/2,y-0.08,str(r*2+c+1),ha='center',va='top',fontsize=6.0,
                color=MUTED,zorder=5)
ax.text(GX+GW+0.11,GY+2.26+0.16,'Slide sorter view',ha='center',va='bottom',
        fontsize=8.2,color=INK,fontweight='bold')
ax.set_xlim(0.0,8.85); ax.set_ylim(0.22,4.45); ax.set_aspect('equal'); ax.axis('off')
```

### (d) Database management system (DBMS)

::: definition Database and DBMS
A **database** is an organised collection of related data stored so that it can
be retrieved and updated easily. A **database management system (DBMS)** is the
software that creates a database, stores the data, and lets users insert, query,
update, delete and protect it.
:::

**Examples:** MS Access, LibreOffice Base, MySQL, PostgreSQL, Oracle, Microsoft
SQL Server, SQLite, MongoDB.

In a **relational** DBMS data is held in **tables**:

- A **field (column or attribute)** is one item of information, for example
  *Roll No* or *Address*.
- A **record (row or tuple)** is the complete set of fields about one entity,
  for example everything about one student.
- A **primary key** is a field whose value is different in every record and is
  never empty; it identifies a record uniquely.
- A **foreign key** is a field in one table that holds the primary key of
  another table, and is what links the two tables together.

```figure caption="Two related tables. Roll No is the primary key of the Student table; the same field appearing in the Marks table is a foreign key, and it is the link that lets one query report a student's name together with the marks."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.1,3.0))
def table(x,y,title,cols,rows,cw,key=0):
    n=len(cols); RH=0.42
    ax.text(x+sum(cw)/2,y+0.14,title,ha='center',va='bottom',fontsize=8.0,
            color=INK,fontweight='bold')
    cx=x
    for j,c in enumerate(cols):
        ax.add_patch(Rectangle((cx,y-RH),cw[j],RH,fc=ACCENT if j==key else MUTED,
                     ec=INK,lw=0.8,alpha=0.22,zorder=3))
        ax.text(cx+cw[j]/2,y-RH/2,c,ha='center',va='center',fontsize=6.8,
                color=INK,fontweight='bold',zorder=4)
        cx+=cw[j]
    for i,r in enumerate(rows):
        cx=x; yy=y-RH*(i+2)
        for j,v in enumerate(r):
            ax.add_patch(Rectangle((cx,yy),cw[j],RH,fc='white',ec=GRID,lw=0.7,zorder=3))
            ax.text(cx+cw[j]/2,yy+RH/2,v,ha='center',va='center',fontsize=6.6,
                    color=INK,zorder=4)
            cx+=cw[j]
    return y-RH*(len(rows)+1)
CW1=[1.80,2.10,1.30]; CW2=[1.80,2.10,1.30]
B1=table(1.30,4.30,'STUDENT',['Roll No','Name','Class'],
         [['1','Anisha','11'],['2','Bikash','11'],['3','Chetana','11']],CW1)
B2=table(8.00,4.30,'MARKS',['Roll No','Subject','Mark'],
         [['1','Computer','78'],['2','Computer','65'],['3','Computer','88']],CW2)
for xk,lab in [(2.20,'primary key'),(8.90,'foreign key')]:
    ax.plot([xk,xk],[B1,B1-0.34],color=ACCENT,lw=0.9,zorder=5)
    ax.text(xk,B1-0.42,lab,ha='center',va='top',fontsize=7.0,color=ACCENT,zorder=5)
ax.annotate('',xy=(8.30,1.72),xytext=(2.80,1.72),zorder=6,
    arrowprops=dict(arrowstyle='-|>',color=ACCENT,lw=1.2,mutation_scale=11,
                    connectionstyle='arc3,rad=-0.16'))
ax.text(5.55,1.30,'one student, many mark records',ha='center',va='top',
        fontsize=7.0,color=ACCENT)
def call(p,q,t):
    ax.annotate('',xy=p,xytext=q,zorder=7,arrowprops=dict(arrowstyle='-',color=MUTED,lw=0.8))
    ax.text(q[0]+0.12,q[1],t,ha='left',va='center',fontsize=7.0,color=MUTED,zorder=7)
call((13.20,4.09),(13.50,4.42),'field  (column)')
call((13.20,3.25),(13.50,2.95),'record  (row)')
ax.set_xlim(0.60,16.60); ax.set_ylim(1.00,4.75); ax.axis('off')
```

The four objects of a desktop DBMS such as MS Access are **tables** (store the
data), **queries** (ask questions of it), **forms** (a friendly screen for data
entry) and **reports** (formatted printed output). Common field data types are
Text/Short Text, Number, Date/Time, Currency, Yes/No, AutoNumber and Memo/Long
Text.

::: example Worked example 4.2 — designing a table
**Problem.** Design a table for a school library that records books. Give the
fields, a suitable data type for each, and state the primary key.

**Solution.**

| Field name | Data type | Reason |
|---|---|---|
| `BookID` | AutoNumber | unique, never repeats — **primary key** |
| `Title` | Short Text | the name of the book |
| `Author` | Short Text | name of the writer |
| `Publisher` | Short Text | publishing house |
| `Price` | Currency | money value, two decimal places |
| `DateAdded` | Date/Time | when the library bought it |
| `Issued` | Yes/No | whether it is out on loan |

`BookID` is the primary key because no two books may share it and it can never be
left blank. `Title` would be a poor key, because a library may hold two different
books with the same title.
:::

| | Word processor | Spreadsheet | Presentation | DBMS |
|---|---|---|---|---|
| Works with | text documents | numbers in a grid | slides | tables of records |
| Basic unit | character, paragraph, page | cell, worksheet | slide | field, record |
| Key strength | formatting and printing text | automatic calculation and charts | visual support for a talk | storing and querying large data |
| Typical file | `.docx`, `.odt` | `.xlsx`, `.ods` | `.pptx`, `.odp` | `.accdb`, `.sql` |
| Example | MS Word, Writer | MS Excel, Calc | PowerPoint, Impress | MS Access, MySQL |

## 4.2 Introduction to domain-specific tools

::: definition Domain-specific software
**Domain-specific software** is application software designed for one particular
field of work. It contains the rules, vocabulary and reports of that field
already built in, so it cannot usefully be used anywhere else.
:::

A general package can be bent to almost any purpose, but a domain-specific system
is built around the workflow of one industry. Compare the two:

| | General purpose package | Domain-specific tool |
|---|---|---|
| Users | everybody | one line of business |
| Cost | low, mass produced | higher; may be custom built |
| Features | broad but shallow | exactly what that field needs |
| Training | general computer skill | job-specific training |
| Example | MS Excel used to keep stock | a full inventory management system |

Almost every such system has the same three-part shape: **input** of transactions,
**processing** against stored master data, and **output** of reports.

```figure caption="The input-process-output shape shared by every domain-specific system, illustrated with a payroll system. The master file holds data that changes rarely; the transaction data changes every month."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.0))
GRN='#2e8b57'
def box(cx,cy,w,h,t,c,fs=7.2,bold=False):
    ax.add_patch(FancyBboxPatch((cx-w/2,cy-h/2),w,h,
        boxstyle="round,pad=0.02,rounding_size=0.12",fc=c,ec=c,lw=1.1,alpha=0.15,zorder=2))
    ax.add_patch(FancyBboxPatch((cx-w/2,cy-h/2),w,h,
        boxstyle="round,pad=0.02,rounding_size=0.12",fc='none',ec=c,lw=1.1,zorder=3))
    ax.text(cx,cy,t,ha='center',va='center',fontsize=fs,color=INK,zorder=4,
            fontweight='bold' if bold else 'normal')
def arw(p,q,c=MUTED):
    ax.annotate('',xy=q,xytext=p,zorder=2,
        arrowprops=dict(arrowstyle='-|>',color=c,lw=1.3,mutation_scale=12,
                        shrinkA=3,shrinkB=3))
box(1.55,3.55,2.90,0.52,'INPUT',ACCENT,8.4,True)
for k,s in enumerate(['days present / absent','overtime hours','leave taken','loan deduction']):
    box(1.55,2.80-k*0.60,2.90,0.48,s,ACCENT,6.4)
box(5.45,2.45,2.50,2.70,'',SERIES[2],7.0)
ax.text(5.45,3.42,'PROCESSING',ha='center',va='center',fontsize=8.4,color=INK,
        fontweight='bold',zorder=5)
for k,s in enumerate(['gross pay','allowances','tax and PF','net pay']):
    ax.text(5.45,2.85-k*0.45,s,ha='center',va='center',fontsize=7.0,color=INK,zorder=5)
box(9.35,3.55,2.90,0.52,'OUTPUT',GRN,8.4,True)
for k,s in enumerate(['pay slips','bank transfer file','tax return','monthly summary']):
    box(9.35,2.80-k*0.60,2.90,0.48,s,GRN,6.4)
box(5.45,0.42,3.10,0.70,'MASTER FILE\n(employee records)',SERIES[4],6.4)
arw((3.05,2.35),(4.20,2.35))
arw((6.70,2.35),(7.85,2.35))
arw((5.45,0.77),(5.45,1.10))
ax.set_xlim(0.0,10.90); ax.set_ylim(0.02,4.05); ax.set_aspect('equal'); ax.axis('off')
```

### (a) School management system

Handles admission and student records, class routines, daily **attendance**,
examination marks and result processing, fee collection and dues, the library,
the hostel and transport, payroll for the staff, and SMS or app notices to
parents. In Nepal, community schools report their data through the government's
**IEMIS** (Integrated Educational Management Information System) platform.

### (b) Inventory management system

Records every item in a store with a code, name, unit, rate and reorder level;
posts each purchase and each sale; keeps the **stock balance** up to date; warns
when an item falls below its reorder level; values the stock; and prints
purchase orders and stock reports. Barcode or QR scanning at the counter is the
usual input method.

### (c) Payroll system

Keeps a master file of employees with grade, basic salary and allowances; accepts
monthly attendance, overtime, leave and loan data; computes **gross pay**, then
deductions (income tax, provident fund, CIT, insurance, advances) and finally
**net pay**; prints pay slips and the bank transfer file; and produces statutory
tax returns.

```figure caption="A school management system. Every module reads from and writes to one shared database, which is why a fee paid at the counter is visible instantly in the student's record."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse
fig, ax = plt.subplots(figsize=(4.6,3.8))
ax.add_patch(Ellipse((0,0),3.30,1.95,fc=ACCENT,ec=ACCENT,lw=1.4,alpha=0.16,zorder=2))
ax.add_patch(Ellipse((0,0),3.30,1.95,fc='none',ec=ACCENT,lw=1.4,zorder=3))
ax.text(0,0.18,'CENTRAL',ha='center',va='center',fontsize=8.6,color=INK,fontweight='bold')
ax.text(0,-0.22,'DATABASE',ha='center',va='center',fontsize=8.6,color=INK,fontweight='bold')
items=[(90,'Admission and\nstudent records'),(150,'Attendance'),(210,'Examination\nand results'),
       (270,'Fee and\naccounts'),(330,'Library and\nhostel'),(30,'Staff payroll\nand notices')]
RX,RY=3.35,2.85; W,H=2.50,0.80
for k,(ang,t) in enumerate(items):
    a=np.radians(ang); cx,cy=RX*np.cos(a),RY*np.sin(a)
    c=SERIES[k%6]
    ax.add_patch(FancyBboxPatch((cx-W/2,cy-H/2),W,H,
        boxstyle="round,pad=0.02,rounding_size=0.12",fc=c,ec=c,lw=1.1,alpha=0.16,zorder=2))
    ax.add_patch(FancyBboxPatch((cx-W/2,cy-H/2),W,H,
        boxstyle="round,pad=0.02,rounding_size=0.12",fc='none',ec=c,lw=1.1,zorder=3))
    ax.text(cx,cy,t,ha='center',va='center',fontsize=7.0,color=INK,zorder=4)
    s=min((W/2+0.06)/max(abs(np.cos(a)),1e-6),(H/2+0.06)/max(abs(np.sin(a)),1e-6))
    tail=(cx-s*np.cos(a),cy-s*np.sin(a))
    r=1.06/np.sqrt((np.cos(a)/1.65)**2+(np.sin(a)/0.975)**2)
    head=(r*np.cos(a),r*np.sin(a))
    ax.annotate('',xy=head,xytext=tail,zorder=1,
                arrowprops=dict(arrowstyle='<|-|>',color=c,lw=1.1,mutation_scale=9))
ax.set_xlim(-4.75,4.75); ax.set_ylim(-3.65,3.65); ax.set_aspect('equal'); ax.axis('off')
```

### (d) Financial accounting system

Maintains the chart of accounts; records journal vouchers of every receipt,
payment, purchase and sale; posts them to the ledger automatically; and prints
the **trial balance, trading and profit-and-loss account, balance sheet**, VAT
returns, and party-wise receivables and payables. Widely used examples are Tally,
Busy, Sage, QuickBooks and Odoo.

### (e) Hotel management system

Handles room inventory and tariffs, online and telephone **reservations**,
check-in and check-out, housekeeping status, restaurant and laundry billing
posted to the room, the final guest folio, and occupancy and revenue reports. It
usually connects to online travel agents and to a payment gateway.

### (f) Weather forecasting system

Collects readings of temperature, pressure, humidity, rainfall, wind speed and
direction from ground stations, balloons, radar and satellites; feeds them into
**numerical weather prediction** models, which solve the equations of the
atmosphere on a three-dimensional grid; and issues forecasts, flood and landslide
warnings and aviation bulletins. Because the models are enormous, this work is
done on supercomputers. In Nepal the **Department of Hydrology and Meteorology**
publishes the national forecast and monsoon and flood warnings.

| System | Typical inputs | Typical outputs |
|---|---|---|
| School management | admission forms, attendance, marks, fees | mark ledger, grade sheet, fee receipt, attendance report |
| Inventory | purchase and sales vouchers, item master | stock balance, reorder alert, valuation report |
| Payroll | attendance, overtime, leave, loans | pay slip, bank file, tax statement |
| Financial accounting | vouchers of all transactions | ledger, trial balance, profit and loss, balance sheet |
| Hotel management | reservations, check-in, restaurant bills | guest folio, occupancy report, revenue report |
| Weather forecasting | station, radar and satellite readings | forecast maps, warnings, aviation bulletins |

::: example Worked example 4.3 — choose the right package
**Problem.** Name the most suitable software for each task and justify it:
(a) preparing a two-page notice for the school notice board; (b) preparing the
examination result ledger with totals, percentages and division; (c) a talk on
"Cyber Safety" for the school assembly; (d) keeping the records of 4,000 library
books with searching and issue tracking; (e) running the daily billing of a
50-room hotel.

**Solution.**
(a) **Word processor** (MS Word) — the job is formatting and printing text.
(b) **Spreadsheet** (MS Excel) — repetitive arithmetic on rows of marks, done by
formulas that recalculate automatically.
(c) **Presentation tool** (PowerPoint) — slides with pictures and bullet points
support a spoken talk.
(d) **DBMS** (MS Access or MySQL) — thousands of records that must be searched,
related to borrowers and kept consistent; a spreadsheet would be slow and
unsafe.
(e) A **hotel management system** — a domain-specific tool, because room status,
reservations, restaurant posting and the guest folio are built in.
:::

::: tip A spreadsheet is not a database
Both look like a grid, but a spreadsheet stores *values you calculate with*,
while a DBMS stores *records you retrieve and relate*. A DBMS enforces data
types, prevents duplicate keys, links tables, handles many users at once and
copes with millions of records — none of which a spreadsheet does well.
:::

## Chapter summary

- An **application package** is ready-made software sold to many users; an
  **office package** bundles a word processor, spreadsheet, presentation tool and
  DBMS that share a common interface.
- A **word processor** creates and formats text: editing, styles, tables, header
  and footer, spell check, mail merge. Examples: MS Word, LibreOffice Writer.
- A **spreadsheet** holds data in cells addressed by column letter and row
  number, calculates with formulas beginning with `=` and functions such as
  `SUM`, `AVERAGE`, `MAX`, `IF`, and draws charts. References may be relative
  (`B2`), absolute (`$B$2`) or mixed.
- **Presentation software** builds a deck of slides with layouts, themes,
  transitions and animations, shown with `F5`.
- A **DBMS** stores data in tables of **records** made of **fields**, identified
  by a **primary key** and linked by a **foreign key**; its objects are tables,
  queries, forms and reports.
- **Domain-specific tools** are built for one field: school management,
  inventory, payroll, financial accounting, hotel management and weather
  forecasting. Describe each by its **inputs, processing and outputs**.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following is **not** part of a standard office package? <span class="marks">[1]</span>
   (a) word processor (b) spreadsheet (c) compiler (d) DBMS
2. In a spreadsheet, the intersection of a row and a column is called a <span class="marks">[1]</span>
   (a) range (b) cell (c) field (d) worksheet
3. Every spreadsheet formula must begin with <span class="marks">[1]</span>
   (a) `+` (b) `#` (c) `=` (d) `@`
4. `=SUM(B2:B10)` adds <span class="marks">[1]</span>
   (a) B2 and B10 only (b) all cells from B2 to B10 (c) column B entirely
   (d) rows 2 to 10 entirely
5. A field that uniquely identifies each record in a table is the <span class="marks">[1]</span>
   (a) foreign key (b) index (c) primary key (d) attribute
6. A row of a database table is also called a <span class="marks">[1]</span>
   (a) field (b) record (c) query (d) form
7. Mail merge is a feature of <span class="marks">[1]</span>
   (a) a spreadsheet (b) a word processor (c) a DBMS (d) presentation software
8. Which of these is a domain-specific software? <span class="marks">[1]</span>
   (a) MS Excel (b) LibreOffice Impress (c) a hotel management system
   (d) Google Chrome
9. The view used to reorder the slides of a presentation is <span class="marks">[1]</span>
   (a) Normal view (b) Slide Sorter view (c) Reading view (d) Notes page

::: note Answers to Group A
**1.** (c) — a compiler is system software.
**2.** (b) — a cell.
**3.** (c) — the equals sign.
**4.** (b) — the colon means "through", so the whole range is added.
**5.** (c) — the primary key.
**6.** (b) — a record (tuple).
**7.** (b) — a word processor.
**8.** (c) — it serves one line of business only.
**9.** (b) — Slide Sorter view.
:::

**Group B — Short answer (5 marks each)**

1. What is an application package? Name the four components of an office package
   and write two features of each. <span class="marks">[5]</span>
2. Define cell, range, worksheet and workbook. Write the formulas to find the
   total, the average, the largest and the smallest of the marks stored in cells
   `C3` to `C20`. <span class="marks">[5]</span>
3. Differentiate between a relative, an absolute and a mixed cell reference with
   one example of each, and explain why absolute references are needed. <span class="marks">[5]</span>
4. Define database, DBMS, field, record and primary key. Name two DBMS
   packages. <span class="marks">[5]</span>
5. What is domain-specific software? Differentiate it from a general purpose
   package under any four headings. <span class="marks">[5]</span>
6. Explain any two of the following with their inputs and outputs: inventory
   management system, payroll system, hotel management system. <span class="marks">[5]</span>

::: note Answers to Group B
**2.** A **cell** is the box where one column meets one row, addressed as `C3`.
A **range** is a rectangular block of cells, written `C3:C20`. A **worksheet** is
one page of the grid; a **workbook** is the whole file containing several
worksheets.
Total `=SUM(C3:C20)`; average `=AVERAGE(C3:C20)`; largest `=MAX(C3:C20)`;
smallest `=MIN(C3:C20)`.

**3.** *Relative* (`B2`) changes when the formula is copied — copying
`=B2*2` from `C2` to `C3` gives `=B3*2`. *Absolute* (`$B$2`) never changes,
because the dollar signs lock both the column and the row. *Mixed* (`B$2` or
`$B2`) locks only one of the two. Absolute references are needed when a formula
must always refer to one fixed cell, such as a rate of tax or a full-marks value,
while being copied down a column.

**4.** A **database** is an organised collection of related data; a **DBMS** is
the software that creates and manages it; a **field** is one column or attribute;
a **record** is one complete row about one entity; a **primary key** is a field
whose value is unique and never empty, so it identifies a record. Examples of a
DBMS: MS Access and MySQL (also Oracle, PostgreSQL).
:::

**Group C — Long answer (8 marks each)**

1. (a) What is a spreadsheet package? Explain any four of its features. <span class="marks">[4]</span>
   (b) A worksheet stores the names of 20 students in column A and their marks
   in five subjects in columns B to F, in rows 2 to 21. Write the formulas for
   the total, the average, the percentage out of 500, the result (Pass if the
   average is 40 or above) and the highest total in the class, and explain how
   the formulas are copied to the remaining rows. <span class="marks">[4]</span>
2. (a) What is a DBMS? Explain the terms table, field, record, primary key and
   foreign key with a suitable example. <span class="marks">[5]</span>
   (b) Explain the four objects of MS Access and state the purpose of each. <span class="marks">[3]</span>
3. (a) What is domain-specific software? <span class="marks">[2]</span>
   (b) Explain the school management system, the payroll system and the weather
   forecasting system, mentioning the inputs, the processing and the outputs of
   each. <span class="marks">[6]</span>

::: note Answers to Group C
**1. (b)** With the first student in row 2:
total `G2` `=SUM(B2:F2)`; average `H2` `=AVERAGE(B2:F2)`; percentage `I2`
`=G2/500*100`; result `J2` `=IF(H2>=40,"Pass","Fail")`; highest total `K2`
`=MAX($G$2:$G$21)`.
Select `G2:K2`, then drag the small square **fill handle** at the bottom-right
corner down to row 21 (or copy and paste). The relative references `B2:F2` become
`B3:F3`, `B4:F4` and so on, while the absolute reference `$G$2:$G$21` stays
pointing at the whole column of totals.

**2. (b)** **Tables** store the data in rows and columns and are the only object
that actually holds data. **Queries** ask questions of one or more tables —
select, filter, sort, calculate — and can also update or delete records.
**Forms** provide a friendly on-screen layout for entering and editing one record
at a time. **Reports** produce formatted, printable output such as a mark ledger
or a fee statement, with grouping and totals.

**3. (b)** *School management*: inputs — admission forms, daily attendance, exam
marks, fee receipts; processing — validation, totalling, grading, dues
calculation; outputs — grade sheets, mark ledgers, attendance and fee reports,
SMS to parents. *Payroll*: inputs — employee master data, attendance, overtime,
leave, loans; processing — gross pay, then tax, provident fund and other
deductions, then net pay; outputs — pay slips, bank transfer file, tax returns.
*Weather forecasting*: inputs — temperature, pressure, humidity, rainfall and
wind readings from ground stations, radar and satellites; processing —
numerical weather prediction models run on supercomputers; outputs — forecast
maps, rainfall and flood warnings, aviation bulletins.
:::
