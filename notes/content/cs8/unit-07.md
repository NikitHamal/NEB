---
subject: Computer Science
grade: 8
unit: 7
title: Word Processing
hours: 0
area: Application Software
---

Applications, notices, letters, project reports, CVs and question papers are
all typed in a **word processor**. It lets you write, correct and decorate a
document on the screen before a single sheet is printed, and change it again
next year without retyping a word. This lesson teaches the word processor as a
set of real tasks: creating, saving and printing a document; editing it;
formatting text, paragraphs and pages; adding tables, pictures, shapes and
WordArt; and producing a hundred personalised letters at once with mail merge.
Commands are given for **Microsoft Word (Microsoft 365)**, with the
**LibreOffice Writer** way in brackets, so you can follow on either.

::: key What questions on this lesson ask
Theory questions ask you to **define a word processor**, list **features**,
name **examples**, and explain terms such as **font, alignment, margin, header,
footer, mail merge**. Short questions ask for **shortcut keys** (Ctrl + B,
Ctrl + H …), the difference between **Cut and Copy** or **Save and Save As**,
and **which tab** holds a command. Long questions ask for **steps**: insert a
table, add page numbers, use Find and Replace, or perform a mail merge. The
practical exam asks you to produce a formatted document — so practise every
worked example at a computer.
:::

## 7.1 Word processor: features and examples

::: definition Word processor
A **word processor** is application software used to **create, edit, format,
save and print text documents** such as letters, notices, reports and
applications. Working on documents this way is called **word processing**.
:::

**Examples:** **Microsoft Word** (part of Microsoft 365), **LibreOffice Writer**
(free and open source), **Google Docs** (works in a web browser), WPS Writer
and Apple Pages. Simple editors such as **Notepad** handle only plain text
without formatting, so they are *text editors*, not word processors. (WordPad,
a small word processor, was removed from Windows 11 in 2024.)

**Features of a word processor**

- **Word wrap:** text moves to the next line by itself when a line is full.
- **Editing:** insert, delete, select, cut, copy, paste and move text; **undo**
  and **redo** mistakes.
- **Find and Replace:** find a word anywhere and change it everywhere at once.
- **Spelling and grammar check** and **AutoCorrect** of common typing errors.
- **Formatting:** fonts, sizes, colours, bold, italic, underline; alignment,
  line spacing, indents, bullets and numbering; margins, page size and
  orientation; headers, footers and page numbers.
- **Objects:** tables, pictures, shapes, WordArt, charts, symbols and
  equations.
- **Mail merge:** many personalised letters from one document and a list.
- **Templates** for letters, CVs and reports; **word count**; **print preview**.
- **Saving in many formats** (DOCX, ODT, PDF) and, in Microsoft 365 and Google
  Docs, **sharing and editing together online**.

| Typewriter | Word processor |
|---|---|
| a mistake means retyping the page | mistakes are corrected on screen before printing |
| one copy at a time (carbon copies are faint) | any number of identical copies |
| nothing is saved | documents are saved and reused |
| one typeface, no pictures | many fonts, colours, tables and pictures |
| no spelling check | spelling and grammar checked automatically |

::: tip Typing in Nepali
Word processors type Nepali in **Unicode** fonts such as **Kalimati, Mangal or
Nirmala UI**. Add the Nepali keyboard in Windows (Settings → Time & language →
Language & region), or use a Romanized Nepali Unicode keyboard. Avoid old
non-Unicode fonts such as Preeti for documents you will share: on a computer
without that font the text turns into English letters.
:::

### The word processor window

```figure caption="The Microsoft Word window (Microsoft 365), drawn with its parts numbered. The ribbon's commands change when you click a different tab; the Home tab, shown here, holds the commands used most often."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.2, 4.4))
T = 1.75
ax.add_patch(Rectangle((0, T), 10, 6.0, fc="white", ec=INK, lw=1.0))
ax.add_patch(Rectangle((0, T + 5.55), 10, 0.45, fc="#2b579a", ec=INK, lw=0.8))
ax.text(0.2, T + 5.775, "AutoSave  ▣  ↶  ↷", ha="left", va="center", fontsize=6.6, color="white")
ax.text(4.6, T + 5.775, "Notice - Word", ha="center", va="center", fontsize=7.0, color="white")
ax.text(9.15, T + 5.775, "–   □   ×", ha="center", va="center", fontsize=7.4, color="white")
tabs = ["File", "Home", "Insert", "Draw", "Design", "Layout", "References", "Mailings", "Review", "View", "Help"]
ax.set_xlim(-0.1, 10.1); ax.set_ylim(-0.05, T + 6.1)
fig.canvas.draw()
rend = fig.canvas.get_renderer()
inv = ax.transData.inverted()
x = 0.15
for t in tabs:
    txt = ax.text(x, T + 5.3, t, ha="left", va="center", fontsize=6.4, color=INK,
                  fontweight="bold" if t == "Home" else "normal", zorder=3)
    bb = txt.get_window_extent(rend)
    w = inv.transform((bb.x1, 0))[0] - inv.transform((bb.x0, 0))[0]
    if t == "Home":
        ax.add_patch(Rectangle((x - 0.08, T + 5.12), w + 0.16, 0.38, fc="#f3f3f3", ec=MUTED, lw=0.6, zorder=2))
    x += w + 0.16
ax.add_patch(Rectangle((0, T + 4.0), 10, 1.1, fc="#f3f3f3", ec=MUTED, lw=0.6))
groups = [("Clipboard", 0.05, 1.6, "Paste\nCut  Copy", 0), ("Font", 1.7, 2.2, "Aptos ▾  12 ▾\nB  I  U  A▾", 0),
          ("Paragraph", 3.95, 2.3, "•≡  1≡  ↕\n≡  ≡  ≡  ≡", 0), ("Styles", 6.3, 2.2, "Normal\nHeading 1", -0.45),
          ("Editing", 8.55, 1.4, "Find\nReplace", 0)]
for name, gx, gw, cmds, dx in groups:
    ax.add_patch(Rectangle((gx, T + 4.03), gw, 1.04, fc="none", ec=GRID, lw=0.6))
    ax.text(gx + gw / 2 + dx, T + 4.67, cmds, ha="center", va="center", fontsize=6.2, color=INK, linespacing=1.3)
    ax.text(gx + gw / 2, T + 4.15, name, ha="center", va="center", fontsize=6.2, color=MUTED)
ax.add_patch(Rectangle((0, T + 3.65), 10, 0.3, fc="#fafafa", ec=MUTED, lw=0.5))
for k in range(1, 18):
    ax.plot([1.5 + k * 0.4, 1.5 + k * 0.4], [T + 3.65, T + 3.75], color=MUTED, lw=0.5)
ax.add_patch(Rectangle((0, T + 0.4), 10, 3.25, fc="#e6e6e6", ec="none"))
ax.add_patch(Rectangle((1.5, T + 0.45), 7.0, 3.15, fc="white", ec=MUTED, lw=0.6))
ax.text(5.0, T + 3.2, "NOTICE", ha="center", va="center", fontsize=8.0, fontweight="bold", color=INK)
for k in range(4):
    ax.plot([2.3, 7.7 if k < 3 else 5.0], [T + 2.75 - k * 0.38, T + 2.75 - k * 0.38], color="#b9bec7", lw=2.2)
ax.plot([5.15, 5.15], [T + 1.47, T + 1.75], color=INK, lw=1.0)
ax.add_patch(Rectangle((9.75, T + 0.45), 0.2, 3.15, fc="#f3f3f3", ec=MUTED, lw=0.5))
ax.add_patch(Rectangle((9.78, T + 2.8), 0.14, 0.7, fc="#c4c8cf", ec="none"))
ax.add_patch(Rectangle((0, T), 10, 0.4, fc="#f3f3f3", ec=MUTED, lw=0.6))
ax.text(0.15, T + 0.2, "Page 1 of 1    86 words    English (India)", ha="left", va="center", fontsize=6.2, color=INK)
ax.text(7.3, T + 0.2, "▭ ▤ ▦   −──●──+  100%", ha="left", va="center", fontsize=6.2, color=INK)
def mk(x, y, n):
    ax.text(x, y, str(n), ha="center", va="center", fontsize=6.6, color="white", fontweight="bold", zorder=6,
            bbox=dict(boxstyle="circle,pad=0.22", fc=SERIES[1], ec="white", lw=0.6))
marks = [(2.75, T + 5.775, 1), (6.1, T + 5.775, 2), (8.25, T + 5.775, 3), (9.6, T + 5.3, 4),
         (8.15, T + 4.67, 5), (3.25, T + 4.15, 6), (0.75, T + 3.8, 7), (5.6, T + 1.6, 8),
         (7.95, T + 0.85, 9), (9.45, T + 2.3, 10), (4.95, T + 0.2, 11), (6.9, T + 0.2, 12)]
for x, y, n in marks:
    mk(x, y, n)
keys = ["Quick Access Toolbar", "title bar", "window buttons", "ribbon tabs",
        "ribbon commands", "group name", "ruler", "insertion point", "document area",
        "scroll bar", "status bar", "view buttons and zoom"]
for n, t in enumerate(keys, 1):
    col, row = (n - 1) // 4, (n - 1) % 4
    xk, yk = 0.25 + col * 3.45, 1.35 - row * 0.4
    mk(xk, yk, n)
    ax.text(xk + 0.28, yk, t, ha="left", va="center", fontsize=6.9, color=INK)
ax.axis("off")
```

The **ribbon** replaces old drop-down menus. It has **tabs** (File, Home,
Insert, Draw, Design, Layout, References, Mailings, Review, View, Help); each
tab has **groups** of related commands (on the Home tab: Clipboard, Font,
Paragraph, Styles, Editing). A small arrow at the corner of a group, the
**dialog box launcher**, opens a dialog with more choices. The **File** tab
opens the **Backstage view** for New, Open, Save, Save As, Print and Export.
The blinking vertical line is the **insertion point (cursor)**: text appears
where it is.

```photo id="cs8/word-lo-tabbed" caption="LibreOffice Writer with its Tabbed user interface (View → User Interface → Tabbed), which looks much like Word's ribbon; here the References tab is open. With the Standard interface the same commands are in the menus File, Edit, View, Insert, Format, Styles, Table, Form, Tools." width="96"
mark 0.19 0.946 "1"
mark 0.935 0.946 "2"
mark 0.84 0.875 "3"
mark 0.155 0.831 "4"
mark 0.73 0.70 "5"
mark 0.26 0.323 "6"
mark 0.983 0.46 "7"
mark 0.115 0.045 "8"
mark 0.885 0.045 "9"
key 1 Quick-access icons: save, undo, redo, print
key 2 Tabs: File, Home, Insert, Layout, References, Review, View
key 3 Commands of the open tab, arranged in groups
key 4 Ruler: margins, indents and tab stops
key 5 The page (document area)
key 6 Insertion point
key 7 Sidebar: styles, properties and navigator
key 8 Status bar: page number and word count
key 9 View buttons and zoom slider
```

```photogrid label="7.H" cols="4" ratio="1.25" caption="The hardware of word processing. (a) The keyboard types the text; the QWERTY layout was designed for typewriters in the 1870s. (b) The mouse points, selects and clicks. (c) An inkjet printer puts the finished document on paper. (d) A flatbed scanner turns a printed page or photograph into a picture that can be inserted into the document. The word processor is the software; these four are the devices that feed it and carry its result out."
@ photo id="bca102/qwerty" cap="(a) Keyboard: input of text"
@ photo id="bca155/mouse" cap="(b) Mouse: pointing, selecting"
@ photo id="bcagk/inkjet" cap="(c) Inkjet printer: output"
@ photo id="bcagk/scanner" cap="(d) Scanner: pictures in"
```

## 7.2 Creating, saving, opening and printing a document

**Create a new document.** Open Word and click **Blank document**, or press
**Ctrl + N**. (Writer: File → New → Text Document.) Start typing. Press
**Enter** only at the **end of a paragraph** — word wrap starts new lines for
you. Press **Ctrl + Enter** to start a new page.

**Save a document for the first time** (File → Save As, or **F12**):
1. Choose the location — **This PC → Documents** or a folder of your own.
2. Type a meaningful **file name**, e.g. `Science Exhibition Notice`.
3. Keep **Save as type: Word Document (*.docx)** (Writer saves **.odt** by
   default; choose *Word 2007–365* to share with Word users).
4. Click **Save**. The name appears in the title bar.

After that, press **Ctrl + S** (Save) often while you work. **Save As** makes a
**new copy** with a different name, place or format; **Save** updates the same
file. To make a PDF that looks the same on every computer: File → **Save As** →
type **PDF**, or File → Export. (Writer: File → Export as PDF.) With Microsoft
365, files saved to **OneDrive** are saved automatically (**AutoSave**).

| Save | Save As |
|---|---|
| saves changes into the same file | saves a copy under a new name, place or format |
| Ctrl + S | F12 in Word; Ctrl + Shift + S in Writer |
| the first time, it opens the Save As box | always opens the Save As box |

**Open a document:** File → **Open** (**Ctrl + O**) → Browse → choose the file
→ Open. Recent files are listed on the Home and Open screens.

**Print a document** (File → **Print**, **Ctrl + P**): the right side shows a
**print preview** of every page. Set:

- **Copies** — how many copies;
- **Printer** — which printer;
- **Pages** — *Print All Pages*, *Print Current Page*, or a list such as
  `1-3, 6` (pages 1, 2, 3 and 6);
- **One sided / two sided**, **Collated**, **Orientation** (portrait or
  landscape), **paper size** (A4 in Nepal) and **margins**;
- then click **Print**.

::: example Worked example 7.1 — how many pages will print?
**Problem.** A 12-page project report is printed with **Pages:** `1-3, 6, 9-10`
and **Copies: 3**. (a) Which pages print, and how many printed pages come out
in all? (b) If *Print on Both Sides* is chosen, how many sheets of paper are
used?

**Solution.** (a) `1-3` means pages 1, 2 and 3; then 6; then `9-10` means 9 and
10. So pages **1, 2, 3, 6, 9, 10** print — **6 pages** per copy. For 3 copies:
6 × 3 = **18 printed pages**.
(b) Two-sided printing puts 2 pages on each sheet: 6 ÷ 2 = 3 sheets per copy,
so 3 × 3 = **9 sheets**.
:::

## 7.3 Editing: select, cut, copy, paste, undo, find and replace, spelling and grammar check

**Selecting text.** You must **select** text before you change it; selected
text is highlighted.

| To select | Do this |
|---|---|
| a word | double-click it |
| a paragraph | triple-click it |
| any part | drag the mouse over it, or hold Shift and press the arrow keys |
| a line | click in the left margin beside it |
| the whole document | Ctrl + A |

**Cut, copy and paste.** Selected text can be moved or duplicated through the
**clipboard**, a temporary store in memory.

| Command | Shortcut | Result |
|---|---|---|
| Cut | Ctrl + X | removes the selection and keeps it on the clipboard |
| Copy | Ctrl + C | leaves the selection and puts a copy on the clipboard |
| Paste | Ctrl + V | inserts the clipboard contents at the insertion point |
| Undo | Ctrl + Z | cancels the last action (press again for earlier ones) |
| Redo | Ctrl + Y | brings back what Undo cancelled |

**Cut + Paste moves** text; **Copy + Paste duplicates** it. You can also drag
selected text to a new place. Word's **Paste Options** (Ctrl after pasting, or
Home → Paste ▾) let you *Keep Source Formatting*, *Merge Formatting* or *Keep
Text Only* — the last is useful when copying from a website.

```photo id="cs8/word-context-menu" caption="Right-clicking selected text opens a context menu with Cut, Copy and Paste and their shortcut keys — here in LibreOffice Writer; Word's menu is similar." width="42"
```

**Find (Ctrl + F).** In Word, Ctrl + F opens the **Navigation pane**; type a
word and every place it occurs is highlighted and listed.

**Find and Replace (Ctrl + H).** Home → Editing → **Replace**. (Writer: Edit →
Find and Replace, Ctrl + H.)
1. Type the word to look for in **Find what**.
2. Type the new word in **Replace with**.
3. Click **More >>** for options such as **Match case** (capitals must match)
   and **Find whole words only** (do not match parts of longer words).
4. Click **Find Next** and **Replace** to change one at a time, or **Replace
   All** to change every one; Word reports how many replacements it made.

::: example Worked example 7.2 — Replace All with and without "whole words"
**Problem.** A document reads: *The cat sat near the category board; the cat
was black.* (a) What does it become if every "cat" is replaced by "dog" with
**Replace All** and no options? (b) What happens if **Find whole words only**
is ticked?

**Solution.** (a) Without the option, Word also finds the "cat" inside
"category": **3 replacements**, giving *The dog sat near the **dogegory**
board; the dog was black.* — a mistake.
(b) With **Find whole words only**, "category" is skipped: **2 replacements**,
giving *The dog sat near the category board; the dog was black.* Always think
about the options before pressing Replace All.
:::

**Spelling and grammar.** Word underlines possible **spelling** mistakes with a
**red wavy line** and **grammar** problems with a **blue double line**.
Right-click an underlined word to choose a correction, **Ignore** it, or **Add
to Dictionary** (useful for Nepali names such as *Bhaktapur*). To check the
whole document: Review → **Editor**, or press **F7**. (Writer: Tools →
Spelling, F7.) The checker is a help, not a teacher: *"I red the book"* passes
the spelling check because *red* is a real word.

## 7.4 Formatting: font, paragraph, bullets and numbering, page layout, header, footer and page numbers

**Formatting** means changing how text and pages **look** without changing what
they **say**.

### Character (font) formatting

Select the text, then use **Home → Font** (Writer: the Formatting toolbar, or
Format → Character).

| Formatting | How | Shortcut |
|---|---|---|
| Font (typeface) | Font box: Aptos, Times New Roman, Arial, Kalimati | — |
| Font size (in points) | Font Size box, or grow/shrink buttons | Ctrl + ] / Ctrl + [ |
| Bold, italic, underline | **B**, *I*, U buttons | Ctrl + B, Ctrl + I, Ctrl + U |
| Font colour, highlight | A▾ and highlighter buttons | — |
| Superscript, subscript | x², x₂ buttons (for 10², H₂O) | Ctrl + Shift + = , Ctrl + = |
| Change case | Aa▾: Sentence case, UPPERCASE, lowercase, Capitalize Each Word | Shift + F3 |
| All font options | dialog box launcher of the Font group | Ctrl + D |

A **font** is a design of letters. Its **size** is measured in **points**
(72 points = 1 inch): body text is usually 11 or 12 pt and headings larger. New
documents in Microsoft 365 use the **Aptos** font; LibreOffice uses Liberation
Serif.

### Paragraph formatting

A **paragraph** is everything typed before you press Enter. Click inside a
paragraph and use **Home → Paragraph** (Writer: Format → Paragraph).

```figure caption="Paragraph alignment and indents. Each grey bar is one line of a paragraph. Justified text is spread to touch both margins except on its last line; a first-line indent starts the first line further in; a hanging indent leaves the first line out and pushes the rest in."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axs = plt.subplots(2, 3, figsize=(5.0, 3.0))
lens = [0.86, 0.95, 0.78, 0.9, 0.55]
def panel(ax, title, mode):
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="white", ec=MUTED, lw=0.6))
    ax.plot([0.08, 0.08], [0.05, 0.95], color=SERIES[1], lw=0.6, ls="--")
    ax.plot([0.92, 0.92], [0.05, 0.95], color=SERIES[1], lw=0.6, ls="--")
    for k, L in enumerate(lens):
        y = 0.82 - k * 0.16
        w = 0.84 * L
        if mode == "left": x0 = 0.08
        elif mode == "centre": x0 = 0.5 - w / 2
        elif mode == "right": x0 = 0.92 - w
        elif mode == "justify":
            x0 = 0.08; w = 0.84 if k < 4 else 0.84 * L
        elif mode == "first":
            x0 = 0.18 if k == 0 else 0.08; w = (0.74 if k == 0 else 0.84) if k < 4 else 0.84 * L
        else:
            x0 = 0.08 if k == 0 else 0.2; w = (0.84 if k == 0 else 0.72) if k < 4 else 0.6
        ax.add_patch(Rectangle((x0, y - 0.04), w, 0.08, fc="#aeb4be", ec="none"))
    ax.set_title(title, fontsize=7.6, pad=3)
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02); ax.axis("off")
panel(axs[0][0], "Left (Ctrl + L)", "left")
panel(axs[0][1], "Centre (Ctrl + E)", "centre")
panel(axs[0][2], "Right (Ctrl + R)", "right")
panel(axs[1][0], "Justify (Ctrl + J)", "justify")
panel(axs[1][1], "First-line indent", "first")
panel(axs[1][2], "Hanging indent", "hanging")
fig.subplots_adjust(wspace=0.12, hspace=0.32)
```

- **Alignment:** left (Ctrl + L), centre (Ctrl + E), right (Ctrl + R) or
  justify (Ctrl + J).
- **Line spacing:** the ↕ button — 1.0, 1.15, 1.5, 2.0 lines; **spacing before
  and after** a paragraph adds space between paragraphs.
- **Indents:** the *Increase/Decrease Indent* buttons move a paragraph in from
  the margin; the ruler's markers or the Paragraph dialog (Special: *First
  line* or *Hanging*) set a first-line or hanging indent.
- **Borders and shading** put a box or a background colour behind a paragraph.

::: caution Spaces and Enter are not formatting tools
Do not centre a title by pressing the spacebar many times, and do not press
Enter at the end of every line. The text will jump out of place as soon as the
font or margins change. Use the **alignment buttons**, **line spacing** and
**Ctrl + Enter** for a new page.
:::

### Bullets and numbering

Select the lines and click **Bullets** (•≡) or **Numbering** (1≡) in Home →
Paragraph; the arrow beside each button chooses the symbol or the number style
(1, 2, 3 · a, b, c · i, ii, iii). **Multilevel List** makes sub-points;
press **Tab** to go one level in and **Shift + Tab** to come back. (Writer:
Format → Bullets and Numbering, or the toolbar buttons.) Use bullets when the
order does not matter and numbers when it does, as in steps.

### Page layout

**Layout** tab (Writer: Format → Page Style):

- **Margins:** the blank space around the text. *Normal* is 2.54 cm (1 inch)
  on every side.
- **Orientation:** **Portrait** (tall) or **Landscape** (wide).
- **Size:** **A4** (21 cm × 29.7 cm), the standard paper in Nepal.
- **Columns:** text in two or three columns, as in a newspaper.
- **Breaks:** a **page break** starts a new page; a **section break** lets one
  part of a document have different margins or orientation.

### Header, footer and page numbers

A **header** is text that repeats at the **top** of every page (for example the
school's name); a **footer** repeats at the **bottom** (for example the page
number or date).

1. **Insert → Header** (or **Footer**) → choose a style, or double-click the
   top or bottom margin of a page.
2. Type the text; it appears on every page.
3. **Insert → Page Number → Bottom of Page → Plain Number 2** puts a centred
   number at the foot of every page; Word counts the pages for you.
4. Tick **Different First Page** on the Header & Footer tab to leave the cover
   page without a number.
5. Click **Close Header and Footer** (or double-click the body).

(Writer: Insert → Header and Footer → Header → Default Page Style; then Insert
→ Page Number, or Insert → Field → Page Number.)

::: example Worked example 7.3 — formatting a notice step by step
**Problem.** Type and format a notice for a school Science Exhibition: a title,
a subtitle, the date on the right, one justified paragraph, three bulleted
points, the principal's signature and a page number in the footer.

**Solution.**
1. Ctrl + N for a new document. Layout → Margins → **Normal**; Size → **A4**;
   Orientation → **Portrait**.
2. Type all the text first, pressing Enter only at the end of each paragraph.
3. Select the title **NOTICE**: Font size **20**, **Ctrl + B**, **Ctrl + E**.
4. Select the subtitle: size **14**, bold, centred.
5. Click in the date line and press **Ctrl + R** (right-align).
6. Select the paragraph: **Ctrl + J** (justify) and line spacing **1.15**.
7. Select the three points and click **Bullets**.
8. Select the signature line *Principal*: bold, right-aligned.
9. Insert → Page Number → Bottom of Page → **Plain Number 2**; Close Header and
   Footer.
10. Ctrl + S, name it `Science Exhibition Notice`, then Ctrl + P to preview and
    print.
:::

```figure caption="The notice of Worked example 7.3 after formatting, with the formatting of each part written beside it. The page is A4 with normal (2.54 cm) margins; the footer carries the page number."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.2, 4.5))
ax.set_xlim(0.0, 10.6); ax.set_ylim(-0.1, 6.1)
PL, PR, PB, PT = 2.4, 8.2, 0.0, 5.95
ML, MR = PL + 0.55, PR - 0.55
ax.add_patch(Rectangle((PL, PB), PR - PL, PT - PB, fc="white", ec=INK, lw=0.9))
ax.add_patch(Rectangle((ML, 0.42), MR - ML, 5.1, fc="none", ec=GRID, lw=0.6, ls="--"))
cx = (PL + PR) / 2
ax.text(cx, 5.12, "NOTICE", ha="center", va="center", fontsize=11, fontweight="bold", color=INK)
ax.text(cx, 4.74, "Science Exhibition 2083", ha="center", va="center", fontsize=8.4, fontweight="bold", color=INK)
ax.text(MR, 4.4, "Date: 2083/11/05", ha="right", va="center", fontsize=6.8, color=INK)
fig.canvas.draw()
rend = fig.canvas.get_renderer(); inv = ax.transData.inverted()
def width(t):
    tx = ax.text(0, 0, t, fontsize=6.8)
    bb = tx.get_window_extent(rend); tx.remove()
    return inv.transform((bb.x1, 0))[0] - inv.transform((bb.x0, 0))[0]
lines = [["All", "students", "of", "Grades", "6", "to", "10"],
         ["are", "informed", "that", "the", "school", "will"],
         ["hold", "its", "Science", "Exhibition", "on", "15"],
         ["Falgun", "2083.", "Each", "class", "must", "prepare"],
         ["one", "working", "model."]]
f = min(5.9 / 5.2, 1.3)
y = 4.05
for k, words in enumerate(lines):
    ws = [width(w) / f for w in words]
    if k < len(lines) - 1:
        gap = (MR - ML - sum(ws)) / (len(words) - 1)
    else:
        gap = width(" ") / f
    x = ML
    for w, wd in zip(words, ws):
        ax.text(x, y, w, ha="left", va="center", fontsize=6.8, color=INK)
        x += wd + gap
    y -= 0.27
bul = ["Register your model by 10 Falgun.", "Bring it to the hall by 9:00 a.m.", "Prizes for the best three models."]
for k, b in enumerate(bul):
    ax.text(ML + 0.2, 2.5 - k * 0.3, "•", ha="center", va="center", fontsize=8, color=INK)
    ax.text(ML + 0.42, 2.5 - k * 0.3, b, ha="left", va="center", fontsize=6.8, color=INK)
ax.plot([MR - 0.95, MR], [1.42, 1.42], color=INK, lw=0.6)
ax.text(MR, 1.25, "Principal", ha="right", va="center", fontsize=6.9, fontweight="bold", color=INK)
ax.text(cx, 0.22, "Page 1", ha="center", va="center", fontsize=6.6, color=MUTED)
def note(tx, ty, px, py, t, side):
    ax.annotate(t, xy=(px, py), xytext=(tx, ty), fontsize=6.8, color=SERIES[1],
                ha="right" if side == "L" else "left", va="center", linespacing=1.15,
                arrowprops=dict(arrowstyle="-", color=SERIES[1], lw=0.7))
note(2.2, 5.12, cx - 0.75, 5.12, "20 pt, bold,\ncentred", "L")
note(2.2, 4.55, cx - 1.45, 4.74, "14 pt, bold,\ncentred", "L")
note(8.4, 4.4, MR + 0.05, 4.4, "right-aligned", "R")
note(8.4, 3.5, MR + 0.05, 3.5, "justified,\nline spacing\n1.15", "R")
note(2.2, 2.2, ML + 0.12, 2.2, "bulleted\nlist", "L")
note(8.4, 1.25, MR + 0.05, 1.25, "bold,\nright-aligned", "R")
note(8.4, 0.3, cx + 0.42, 0.22, "footer:\npage number", "R")
note(2.2, 0.75, ML, 0.6, "margins\n2.54 cm", "L")
ax.axis("off")
```

## 7.5 Tables, pictures, shapes and WordArt

### Tables

A **table** arranges information in **rows** (across) and **columns** (down);
each box is a **cell**. Tables suit class routines, marks lists and price lists.

1. Click where the table should go. **Insert → Table** and drag across the grid
   to choose, say, 5 columns × 4 rows — or click **Insert Table…** and type the
   **number of columns and rows**. (Writer: Table → Insert Table, Ctrl + F12.)
2. Type in the cells; press **Tab** to go to the next cell (Tab in the last cell
   adds a new row).
3. The **Table Design** tab changes the **style**, **shading** and **borders**.
4. The **Layout** tab (next to Table Design) has **Insert Above/Below/Left/
   Right**, **Delete**, **Merge Cells** (join selected cells into one), **Split
   Cells**, **AutoFit**, alignment of text in cells, and **Formula** (for
   example `=SUM(ABOVE)` to total a column of numbers).

::: example Worked example 7.4 — rows, columns and merged cells
**Problem.** A class routine table is inserted with 5 columns and 4 rows.
(a) How many cells does it have? (b) The 5 cells of the top row are merged to
hold the title *Class 8 Routine*. How many cells are there now? (c) One more row
is inserted below. How many cells in all?

**Solution.** (a) 5 × 4 = **20 cells**.
(b) Merging 5 cells makes 1 cell, so 20 − 5 + 1 = **16 cells**.
(c) A new row has 5 cells: 16 + 5 = **21 cells**.
:::

### Pictures

**Insert → Pictures → This Device**, find the photo and click **Insert**.
(Writer: Insert → Image.) Drag the round **handles** at the corners to resize it
without stretching it out of shape; the **Picture Format** tab can **crop** it,
add a border or a style. **Wrap Text** decides how text flows around it.

```figure caption="Text-wrapping options for a picture (Picture Format → Wrap Text in Word; Format → Wrap in LibreOffice). The blue box is the picture and the grey bars are lines of text."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse
fig, axs = plt.subplots(2, 3, figsize=(5.0, 3.1))
def panel(ax, title, mode):
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="white", ec=MUTED, lw=0.6))
    px, py, pw, ph = 0.32, 0.36, 0.36, 0.32
    rows = [0.88, 0.76, 0.64, 0.52, 0.40, 0.28, 0.16]
    if mode == "behind":
        ax.add_patch(Rectangle((px, py), pw, ph, fc="#9cc3e6", ec=ACCENT, lw=0.8, zorder=1))
    for y in rows:
        overlap = py - 0.03 < y < py + ph + 0.03
        if mode == "inline":
            if y == 0.40:
                ax.add_patch(Rectangle((0.08, 0.40), 0.23, 0.06, fc="#aeb4be", ec="none", zorder=2))
                ax.add_patch(Rectangle((0.65, 0.40), 0.27, 0.06, fc="#aeb4be", ec="none", zorder=2))
                continue
            if 0.5 <= y <= 0.64:
                continue
            ax.add_patch(Rectangle((0.08, y - 0.03), 0.84, 0.06, fc="#aeb4be", ec="none", zorder=2))
        elif mode in ("square", "tight") and overlap:
            gap = 0.03 if mode == "square" else -0.02
            ax.add_patch(Rectangle((0.08, y - 0.03), px - 0.08 - gap, 0.06, fc="#aeb4be", ec="none", zorder=2))
            ax.add_patch(Rectangle((px + pw + gap, y - 0.03), 0.92 - px - pw - gap, 0.06, fc="#aeb4be", ec="none", zorder=2))
        elif mode == "topbottom" and overlap:
            continue
        else:
            ax.add_patch(Rectangle((0.08, y - 0.03), 0.84, 0.06, fc="#aeb4be", ec="none", zorder=2))
    if mode == "inline":
        ax.add_patch(Rectangle((0.33, 0.4), 0.3, 0.26, fc="#9cc3e6", ec=ACCENT, lw=0.8, zorder=3))
    elif mode == "tight":
        ax.add_patch(Ellipse((px + pw / 2, py + ph / 2), pw, ph, fc="#9cc3e6", ec=ACCENT, lw=0.8, zorder=3))
    elif mode != "behind":
        ax.add_patch(Rectangle((px, py), pw, ph, fc="#9cc3e6", ec=ACCENT, lw=0.8, zorder=3,
                               alpha=0.92 if mode == "front" else 1))
    ax.set_title(title, fontsize=7.4, pad=3)
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02); ax.axis("off")
panel(axs[0][0], "In Line with Text", "inline")
panel(axs[0][1], "Square", "square")
panel(axs[0][2], "Tight", "tight")
panel(axs[1][0], "Top and Bottom", "topbottom")
panel(axs[1][1], "Behind Text", "behind")
panel(axs[1][2], "In Front of Text", "front")
fig.subplots_adjust(wspace=0.12, hspace=0.32)
```

### Shapes and WordArt

**Shapes:** **Insert → Shapes** offers lines, arrows, rectangles, circles,
stars, flowchart symbols and callouts. Click a shape, then drag on the page to
draw it (hold **Shift** for a perfect square or circle). The **Shape Format**
tab changes its **fill**, **outline** and **effects**; right-click → **Add
Text** writes inside it. (Writer: Insert → Shape, or the Drawing toolbar.)

**WordArt** is decorative text with colour, outline, shadow and curved
effects, used for titles of posters and certificates. **Insert → WordArt** (in
the Text group) → choose a style → type the words. The **Shape Format** tab's
**Text Effects → Transform** bends it into an arch or a wave. (Writer: Insert →
**Fontwork**.) Use WordArt sparingly: one decorative title is enough.

| Object | Insert | Format tab | Writer |
|---|---|---|---|
| Table | Insert → Table | Table Design, Layout | Table → Insert Table |
| Picture | Insert → Pictures | Picture Format | Insert → Image |
| Shape | Insert → Shapes | Shape Format | Insert → Shape |
| WordArt | Insert → WordArt | Shape Format | Insert → Fontwork |

## 7.6 Mail merge

Suppose the school must send an invitation to the parents of 32 students. The
letter is the same except for each parent's name, the student's name and the
class. Typing 32 letters wastes time and invites mistakes. **Mail merge**
types them all at once.

::: definition Mail merge
**Mail merge** is a feature of a word processor that **combines a main document
with a data source** to produce many **personalised copies** — letters,
envelopes, labels, certificates or emails — each filled with the details of one
person from the list.
:::

Mail merge needs three things:

- the **main document** — the text that is the same for everyone, with
  **merge fields** such as «Name» where the details should go;
- the **data source** — a table of names and details (a Word table, an Excel
  or Calc sheet, or Outlook contacts), with **one row (record) per person**
  and **one column (field) per detail**;
- the **merged documents** — one finished copy for every row.

```figure caption="Mail merge. One main document holds the text that is the same for everyone and merge fields in « » marks; the data source holds one row per person. Merging puts each row into the fields and makes one letter per row."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
fig, ax = plt.subplots(figsize=(5.2, 3.2))
ax.add_patch(Rectangle((0.1, 1.9), 2.6, 2.1, fc="white", ec=ACCENT, lw=1.2))
ax.text(1.4, 3.8, "Main document", ha="center", va="center", fontsize=7.6, fontweight="bold", color=ACCENT)
ax.text(0.25, 3.35, "Dear «Parent»,\nYour child «Name»\nof Grade «Class» is\ninvited to the Parents'\nDay on Magh 15.", ha="left",
        va="top", fontsize=6.9, color=INK, linespacing=1.3)
ax.text(1.4, 1.65, "letter text + merge fields", ha="center", va="center", fontsize=6.9, color=MUTED)
ax.add_patch(Rectangle((0.1, 0.05), 2.6, 1.3, fc="white", ec=SERIES[2], lw=1.2))
ax.text(1.4, 1.15, "Data source", ha="center", va="center", fontsize=7.6, fontweight="bold", color=SERIES[2])
rows = [("Parent", "Name", "Class"), ("Hari Rai", "Asha", "8"), ("Gita Khadka", "Rohan", "7"), ("Mohan Das", "Sunita", "8")]
for r, row in enumerate(rows):
    for c, v in enumerate(row):
        ax.text(0.2 + [0, 1.15, 2.05][c], 0.88 - r * 0.22, v, ha="left", va="center", fontsize=6.6,
                color=INK, fontweight="bold" if r == 0 else "normal")
ax.annotate("", xy=(4.0, 2.2), xytext=(2.8, 2.9), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2))
ax.annotate("", xy=(4.0, 1.9), xytext=(2.8, 0.7), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2))
ax.add_patch(FancyBboxPatch((3.25, 1.75), 0.8, 0.5, boxstyle="round,pad=0.02", fc="#fbf7ee", ec=SERIES[3], lw=1.0))
ax.text(3.65, 2.0, "merge", ha="center", va="center", fontsize=7.2, color=INK)
names = [("Hari Rai", "Asha", "8"), ("Gita Khadka", "Rohan", "7"), ("Mohan Das", "Sunita", "8")]
for k, (p, n, c) in enumerate(names):
    x0, y0 = 4.5, 2.9 - k * 1.42
    ax.add_patch(Rectangle((x0, y0), 3.3, 1.28, fc="white", ec=INK, lw=0.9))
    ax.text(x0 + 0.12, y0 + 1.18, f"Dear {p},\nYour child {n} of Grade {c}\nis invited to the Parents'\nDay on Magh 15.",
            ha="left", va="top", fontsize=6.6, color=INK, linespacing=1.25)
ax.text(6.15, 4.33, "3 merged letters", ha="center", va="center", fontsize=6.9, color=MUTED)
ax.set_xlim(0.0, 7.95); ax.set_ylim(-0.1, 4.5); ax.axis("off")
```

**Steps in Microsoft Word**

1. Type the letter, leaving out the details that change.
2. **Mailings → Start Mail Merge → Letters.**
3. **Mailings → Select Recipients →** *Use an Existing List* (choose an Excel
   file such as `parents.xlsx` and its sheet) or *Type a New List* (type the
   names in Word's own table).
4. Click where a detail belongs, then **Insert Merge Field** and choose the
   field, e.g. «Parent». Repeat for «Name» and «Class».
5. **Preview Results** and use the arrows to check each record; **Edit
   Recipient List** can untick people who should not get a letter.
6. **Finish & Merge → Edit Individual Documents** (makes one new document
   with every letter), **Print Documents**, or **Send Email Messages**.

Word also offers a guided **Step-by-Step Mail Merge Wizard** under Start Mail
Merge. In LibreOffice Writer: **Tools → Mail Merge Wizard**, using a Calc sheet
as the data source.

**Uses:** invitations and notices to parents, report cards and certificates
with each student's name, fee reminders, envelopes and address labels, and
greeting letters from businesses to customers.

::: example Worked example 7.5 — how many letters?
**Problem.** A school's data source sheet has 32 rows of parents, with the
columns Parent, Name, Class and Fee_Due. (a) How many letters does Finish &
Merge make? (b) In Edit Recipient List the teacher unticks 4 parents who have
already paid. How many letters now? (c) Write the merge fields for the line
*"Please pay Rs ... for your child ... by Magh 15."*

**Solution.** (a) One letter per row: **32 letters**.
(b) 32 − 4 = **28 letters**.
(c) *Please pay Rs «Fee_Due» for your child «Name» by Magh 15.* — the main
document holds this one line; the merge fills in each parent's amount and
child's name.
:::

::: note Activity 7.1 — a word-processing portfolio
At the lab, make these four documents and save each in a folder named after
you: (1) the notice of Worked example 7.3; (2) your class routine as a table
with a merged title row; (3) a one-page report on a festival with one picture
wrapped **Square**, a WordArt title, a header with your school's name and page
numbers in the footer; (4) a mail-merged invitation to five friends from a
data table you type yourself. Print or export each as PDF.
:::

::: tip Learn the shortcuts in pairs
**Ctrl + X / C / V** cut, copy, paste · **Ctrl + Z / Y** undo, redo · **Ctrl +
B / I / U** bold, italic, underline · **Ctrl + L / E / R / J** left, centre,
right, justify · **Ctrl + S / O / P / N** save, open, print, new · **Ctrl + F /
H** find, replace. In an exam, write the tab and command too, e.g. *Insert →
Page Number*.
:::

## Chapter summary

- A **word processor** creates, edits, formats, saves and prints documents:
  Microsoft Word, LibreOffice Writer, Google Docs. Features include word wrap,
  find and replace, spell check, tables, pictures and mail merge.
- Word's window: title bar, Quick Access Toolbar, **ribbon** (tabs → groups →
  commands), ruler, document area, insertion point, scroll bars, status bar.
- **New** Ctrl + N, **Open** Ctrl + O, **Save** Ctrl + S (**Save As** F12 makes a
  new copy), **Print** Ctrl + P with copies, pages (`1-3, 6`) and sides; DOCX for
  Word, ODT for Writer, PDF for sharing.
- **Editing:** select, **Cut** Ctrl + X (move), **Copy** Ctrl + C, **Paste**
  Ctrl + V, **Undo** Ctrl + Z, **Find** Ctrl + F, **Replace** Ctrl + H (match
  case, whole words), **spelling and grammar** F7.
- **Formatting:** font, size (points), bold/italic/underline; alignment
  (Ctrl + L/E/R/J), line spacing, indents; bullets and numbering; margins
  (Normal 2.54 cm), orientation, A4 size; **header** (top), **footer**
  (bottom), page numbers (Insert → Page Number).
- **Objects:** tables (rows × columns = cells; merge, split), pictures (Wrap
  Text), shapes and **WordArt** (Writer: Fontwork).
- **Mail merge** = main document + data source → one merged copy per row
  (Mailings → Start Mail Merge → Select Recipients → Insert Merge Field →
  Preview → Finish & Merge).

## Practice questions

**Group A — Objective (1 mark each)**

1. Which of these is a word processor? <span class="marks">[1]</span>
   (a) Microsoft Excel (b) LibreOffice Writer (c) Google Chrome (d) VLC
2. The default file extension of a Microsoft Word document is <span class="marks">[1]</span>
   (a) .xlsx (b) .docx (c) .pptx (d) .odt
3. The shortcut key for Undo is <span class="marks">[1]</span>
   (a) Ctrl + Y (b) Ctrl + U (c) Ctrl + Z (d) Ctrl + X
4. Text that repeats at the top of every page is the <span class="marks">[1]</span>
   (a) footer (b) header (c) margin (d) footnote
5. Ctrl + H opens <span class="marks">[1]</span>
   (a) Find and Replace (b) Help (c) Header (d) Hyperlink
6. Which alignment makes text touch both the left and right margins? <span class="marks">[1]</span>
   (a) left (b) centre (c) right (d) justify
7. The Mail Merge commands are on the <span class="marks">[1]</span>
   (a) Insert tab (b) Mailings tab (c) Review tab (d) View tab
8. In Word, a red wavy underline below a word shows a possible <span class="marks">[1]</span>
   (a) grammar mistake (b) spelling mistake (c) hyperlink (d) bold word
9. Printing with **Pages:** `2-4, 7` prints <span class="marks">[1]</span>
   (a) 2 pages (b) 3 pages (c) 4 pages (d) 7 pages
10. Decorative text with curved and shadow effects is <span class="marks">[1]</span>
    (a) WordArt (b) a footer (c) a table (d) a bullet
11. A table of 6 columns and 5 rows has <span class="marks">[1]</span>
    (a) 11 cells (b) 25 cells (c) 30 cells (d) 36 cells
12. In LibreOffice Writer, WordArt is called <span class="marks">[1]</span>
    (a) Fontwork (b) SmartArt (c) ClipArt (d) TextArt

::: note Answers to Group A
**1.** (b) — Writer is LibreOffice's word processor.
**2.** (b) — .docx; .odt is Writer's format.
**3.** (c) — Ctrl + Z undoes; Ctrl + Y redoes.
**4.** (b) — the header; the footer is at the bottom.
**5.** (a) — Find and Replace.
**6.** (d) — justify spreads text to both margins.
**7.** (b) — Mailings tab.
**8.** (b) — red for spelling; blue double line for grammar.
**9.** (c) — pages 2, 3, 4 and 7.
**10.** (a) — WordArt.
**11.** (c) — 6 × 5 = 30.
**12.** (a) — Insert → Fontwork.
:::

**Group B — Short answer (2 marks each)**

1. What is a word processor? Name two examples. <span class="marks">[2]</span>
2. Write any four features of a word processor. <span class="marks">[2]</span>
3. Differentiate between Save and Save As. <span class="marks">[2]</span>
4. Differentiate between Cut and Copy. <span class="marks">[2]</span>
5. Write the steps to find the word "Kathmandu" and replace it with "Lalitpur" everywhere in a document. <span class="marks">[2]</span>
6. What are header and footer? Give one use of each. <span class="marks">[2]</span>
7. Write the steps to insert page numbers at the bottom of every page in Word. <span class="marks">[2]</span>
8. Write the steps to insert a table of 4 columns and 6 rows. <span class="marks">[2]</span>
9. What is meant by text wrapping? Name two wrapping options. <span class="marks">[2]</span>
10. Write the shortcut keys for: bold, centre alignment, paste and print. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A word processor is application software used to create, edit, format,
save and print text documents. Examples: Microsoft Word, LibreOffice Writer,
Google Docs (any two).

**2.** Any four: word wrap; editing with cut, copy, paste and undo; find and
replace; spelling and grammar check; formatting of fonts, paragraphs and pages;
tables, pictures and shapes; headers, footers and page numbers; mail merge;
saving as PDF; templates.

**3.** Save stores the changes in the same file (Ctrl + S); the first time, it
asks for a name. Save As stores a new copy with a different name, location or
format (F12), leaving the original unchanged.

**4.** Cut (Ctrl + X) removes the selected text and keeps it on the clipboard,
so pasting moves it. Copy (Ctrl + C) leaves the text where it is and puts a copy
on the clipboard, so pasting duplicates it.

**5.** Press Ctrl + H (Home → Editing → Replace). Type *Kathmandu* in Find what
and *Lalitpur* in Replace with; under More, tick Find whole words only if
needed; click Replace All, then OK.

**6.** A header is text at the top margin that repeats on every page, e.g. the
school's name; a footer is text at the bottom margin that repeats on every
page, e.g. the page number or date.

**7.** Insert tab → Page Number → Bottom of Page → choose a style such as Plain
Number 2; then click Close Header and Footer.

**8.** Place the cursor; Insert → Table → Insert Table…; type 4 in Number of
columns and 6 in Number of rows; click OK. (In Writer: Table → Insert Table.)

**9.** Text wrapping decides how the text of the document flows around a
picture or shape. Options (any two): In Line with Text, Square, Tight, Top and
Bottom, Behind Text, In Front of Text.

**10.** Bold: Ctrl + B; centre: Ctrl + E; paste: Ctrl + V; print: Ctrl + P.
:::

**Group C — Long answer (4 marks each)**

1. Explain any four parts of the Microsoft Word window with a labelled sketch. <span class="marks">[4]</span>
2. What is mail merge? Write the steps to prepare invitation letters for ten parents with mail merge. <span class="marks">[1+3]</span>
3. Write the steps to (a) save a new document with the name *Report* in the Documents folder, and (b) print pages 1 to 3 of it twice. <span class="marks">[2+2]</span>
4. Explain any four types of paragraph formatting with examples. <span class="marks">[4]</span>
5. A 20-page document is printed with **Pages:** `1-5, 11, 15-16` and **Copies:** 4 on both sides of the paper. How many pages print per copy, how many printed pages in all, and how many sheets are used? Show your working. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Sketch as in Figure 1. Any four: *Title bar* — shows the document's name
and the program. *Quick Access Toolbar* — Save, Undo, Redo always at hand.
*Ribbon* — tabs (Home, Insert, Layout …) with groups of commands. *Ruler* —
shows and sets margins, indents and tab stops. *Document area* — where text is
typed; the insertion point marks the typing position. *Scroll bars* — move
through the document. *Status bar* — page number, word count and language;
*zoom slider* — enlarge or shrink the view.

**2.** Mail merge combines a main document with a data source to produce a
personalised copy for every person (1 mark). Steps: type the invitation,
leaving blanks for the details; Mailings → Start Mail Merge → Letters; Select
Recipients → Type a New List and enter the ten parents' names and their
children's names (or Use an Existing List from Excel); place the cursor and
Insert Merge Field «Parent», «Name» in the right places; Preview Results to
check; Finish & Merge → Edit Individual Documents (or Print Documents). Ten
letters are produced.

**3.** (a) File → Save As (or F12) → choose This PC → Documents → type *Report*
in File name → keep the type Word Document (*.docx) → Save. (b) File → Print
(Ctrl + P) → in Pages type `1-3` → set Copies to 2 → choose the printer →
Print.

**4.** Any four. *Alignment:* the position of lines between the margins — left,
centre (a title), right (a date), justify (a report). *Line spacing:* the space
between lines — 1.0 for normal text, 1.5 or 2.0 for drafts. *Indentation:*
moving a paragraph in from the margin — first-line indent in a story, hanging
indent in a list of references. *Spacing before and after:* space between
paragraphs. *Bullets and numbering:* lists of points or steps. *Borders and
shading:* a box or background colour behind a paragraph.

**5.** `1-5` gives pages 1, 2, 3, 4, 5 (5 pages); 11 (1 page); `15-16` gives
15 and 16 (2 pages). Pages per copy = 5 + 1 + 2 = **8**.
Printed pages = 8 × 4 = **32**.
Both sides: 8 ÷ 2 = 4 sheets per copy, so 4 × 4 = **16 sheets**.
:::

**Group D — Extended answers (10 marks each, for deeper revision)**

1. What is a word processor? Explain its eight main features. <span class="marks">[10]</span>
2. Explain the formatting of a document: character, paragraph and page formatting, with headers and footers. <span class="marks">[10]</span>
3. What is mail merge? Write the steps of mail merge with the parts needed. <span class="marks">[10]</span>

### Model answer D1: features of a word processor (10 marks)

**Introduction.** A **word processor** is application software used to create, edit, format, save and print text documents such as letters, reports, notices and books. MS Word, LibreOffice Writer and Google Docs are examples. It has replaced the typewriter because mistakes can be corrected before anything is printed (Plate 7.H).

1. **Easy editing.** Text can be inserted, deleted, cut, copied and pasted at any place. If we make a mistake we press Undo, so no page has to be typed again. A headteacher can correct a notice in seconds.
2. **Formatting.** The font, size, colour, bold, italic, alignment and line spacing can be changed. This makes a document neat and easy to read. A school magazine uses such formatting for headings and articles.
3. **Spelling and grammar check.** The program underlines wrong spellings in red and grammar mistakes in blue. It suggests the correct word, which helps students write error-free English. Find and Replace changes a word everywhere in a long file at once.
4. **Tables, pictures and shapes.** A table can arrange marks or a timetable in rows and columns. Pictures, shapes, charts and WordArt make a report attractive. A project report often has all of these.
5. **Header, footer and page numbers.** Text such as the school name can be repeated at the top or bottom of every page, and pages can be numbered automatically. This is needed for long documents.
6. **Page layout.** The paper size (A4, Letter), margins, orientation and columns can be set. A newspaper-style page can be made with columns.
7. **Mail merge.** One letter can be sent to many people, each with a different name and address. A school uses it to send result letters to all parents.
8. **Saving, printing and sharing.** The document is saved as a file, printed on paper or shared as PDF or by e-mail. Google Docs lets many people work on one document at the same time.

**Conclusion.** A word processor saves time and paper, gives a neat result and lets us correct and reuse our work. It is the most used application in schools and offices.

### Model answer D2: formatting a document (10 marks)

**Introduction.** **Formatting** means changing the appearance of a document without changing its meaning. In MS Word the commands are on the **Home**, **Layout** and **Insert** tabs. There are three levels of formatting.

1. **Character (font) formatting** changes single letters or words: font type (Arial, Times New Roman), font size, **bold** (Ctrl + B), *italic* (Ctrl + I), underline (Ctrl + U), font colour, superscript (x²) and subscript (H₂O).
2. **Paragraph formatting** changes a whole paragraph: alignment (left, centre, right, justify), line spacing, indentation, and the space before and after, and bullets and numbering.
3. **Page formatting** changes the whole page: paper size, margins, orientation (portrait or landscape), columns and page borders.

**Header, footer and page number.** A **header** is text that appears at the top margin of every page, and a **footer** at the bottom margin. Steps: click **Insert** → **Header** → choose a style → type the text, for example the school name → **Close Header and Footer**. Page numbers: **Insert** → **Page Number** → choose the position.

| Type | Applies to | Examples of commands |
|---|---|---|
| Character | Selected letters and words | Font, size, bold, colour |
| Paragraph | One whole paragraph | Alignment, spacing, bullets |
| Page | Every page | Margins, orientation, columns |
| Header and footer | Top and bottom of each page | School name, page number |

**A worked case.** To make a notice: select the title → centre it, set the size to 20 and bold; select the body → set Times New Roman 12, justified, line spacing 1.5; set the margins to 2.5 cm; add the date in the footer.

**Conclusion.** Good formatting makes the document clear and attractive, and each level of formatting has its own use.

### Model answer D3: mail merge (10 marks)

**Introduction.** **Mail merge** is the feature that joins one common document with a list of data (names and addresses) to produce many personalised copies. It saves the work of typing the same letter again and again.

**Parts of mail merge.**

1. **Main document:** the letter with the fixed text, such as an invitation to a parents' meeting.
2. **Data source:** a table (Word table, Excel sheet or database) with one row for each person and one column for each field, such as Name, Address and Marks.
3. **Merge fields:** place-holders such as «Name» in the main document, which are replaced by the data of each row.

| Name | Address | Class |
|---|---|---|
| Asha Gurung | Pokhara | 8 |
| Bikash Thapa | Butwal | 8 |
| Chandra Rai | Dharan | 8 |

**Steps in MS Word.**

1. Type the main letter and leave the places for the name and address.
2. Click **Mailings** → **Start Mail Merge** → **Letters**.
3. Click **Select Recipients** → **Use an Existing List** and choose the file; or **Type a New List**.
4. Put the cursor where the name goes and click **Insert Merge Field** → **Name**; repeat for the other fields.
5. Click **Preview Results** to see each letter.
6. Click **Finish & Merge** → **Print Documents** or **Edit Individual Documents**.

**Uses.** Result letters, invitations, certificates, address labels, and bills.

**Conclusion.** Mail merge needs a main document and a data source, and it produces one personal letter for each record, saving time and avoiding mistakes.
