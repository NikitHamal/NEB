---
subject: Computer Science
grade: 8
unit: 10
title: Web Page Design
hours: 0
area: Web, Communication and Society
---

Every website you open — the NEB results page, a news portal, the Nagarik App's
web version, Wikipedia — is built from plain text files written in **HTML**. A
browser reads those files and turns them into headings, paragraphs, pictures,
tables and links. In this lesson you learn how the World Wide Web works and
then write web pages yourself: the structure of an HTML document, tags for
formatting text, lists, images, links and tables, and finally a small website of
linked pages that you can open in any browser. All the code in this lesson was
tested in a real browser (Chromium), and what it shows is described exactly.

::: key What questions on this lesson ask
Expect the full forms **WWW, HTML, URL, HTTP(S)**; definitions of **web page,
website, home page, web browser, tag, attribute**; the **parts of a URL**; the
**four structure tags**; the difference between **container and empty tags**;
and writing **HTML code** for a given output — headings, a formatted paragraph,
an ordered or unordered list, an image, a hyperlink, or a **table** (often with
`rowspan` or `colspan`). You will also be asked **what a given code shows** in
the browser. Practise writing code by hand, with every tag closed.
:::

## 10.1 World Wide Web: web page, website, web browser, URL and HTML

The **World Wide Web (WWW, or "the web")** was invented by **Tim Berners-Lee**,
a British scientist at **CERN**, the European physics laboratory near Geneva.
He proposed it in **March 1989**, wrote the first web server, the first browser
and **HTML** by the end of 1990, and announced the web to the public in **August
1991**. In 1993 CERN made the web software free for everyone, and the web grew
explosively.

```photo id="cs8/web-first-server" caption="The NeXT computer that Tim Berners-Lee used at CERN as the world's first web server, now in a museum. The handwritten sticker on the cube says 'This machine is a server. DO NOT POWER IT DOWN!!'; the paper on the left is his 1989 proposal, Information Management: A Proposal." width="66"
```

::: definition World Wide Web
The **World Wide Web** is a huge collection of **web pages**, stored on computers
called **web servers** all over the world and joined to one another by
**hyperlinks**, which people open over the Internet with a **web browser**.
:::

The **Internet** and the **web** are not the same. The Internet is the worldwide
**network of networks** — cables, satellites, routers and computers joined
together. The web is one **service that runs on the Internet**, like email,
video calls and online games.

| Term | Meaning | Example |
|---|---|---|
| **Web page** | a single document on the web, written in HTML, that can contain text, pictures, links, sound and video | the results page of a school |
| **Website** | a group of related web pages under one **domain name**, linked to each other | `www.neb.gov.np` (National Examinations Board) |
| **Home page** | the first, main page of a website, usually saved as `index.html` | the page that opens at `www.ntc.net.np` |
| **Web browser** | application software that requests web pages from servers and displays them | Google Chrome, Mozilla Firefox, Microsoft Edge, Safari, Opera |
| **Web server** | a computer that stores websites and sends pages to browsers when they ask | the computers of a hosting company |
| **Hyperlink** | text or a picture that opens another page when clicked | blue, underlined words |
| **URL** | **Uniform Resource Locator**: the unique address of a page on the web | `https://www.moecdc.gov.np` |
| **HTTP / HTTPS** | **HyperText Transfer Protocol (Secure)**: the rules browsers and servers use to send pages; HTTPS encrypts them | a padlock in the address bar means HTTPS |

```photo id="cs8/web-firefox" caption="Mozilla Firefox, a web browser, showing a Wikipedia page. The tab shows the page's title and the address bar shows its URL; blue words on the page are hyperlinks." width="96"
crop 0.0 0.717 1.0 1.0
mark 0.406 0.893 "1"
mark 0.828 0.686 "2"
mark 0.099 0.686 "3"
mark 0.49 0.507 "4"
mark 0.583 0.257 "5"
mark 0.776 0.257 "6"
key 1 Tabs: one for each open page; a tab shows the page's title
key 2 Address bar: the URL, here https://en.wikipedia.org/wiki/Firefox
key 3 Back, forward and reload buttons
key 4 Bookmarks toolbar for favourite pages
key 5 The web page itself
key 6 Hyperlinks (blue text) that open other pages
```

### The parts of a URL

```figure caption="The parts of a URL (web address). The protocol says how to fetch the page, the domain name says which web server holds it, and the path and file name say where the page is on that server."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2, 1.5))
parts = [("https://", SERIES[1], "protocol"), ("www.janataschool.edu.np", ACCENT, "domain name"),
         ("/notices/", SERIES[2], "path (folder)"), ("exam.html", SERIES[3], "file name")]
ax.set_xlim(0, 10); ax.set_ylim(0.9, 2.6)
fig.canvas.draw(); rend = fig.canvas.get_renderer(); inv = ax.transData.inverted()
f = min(5.9 / 5.2, 1.3)
x = 0.15
spans = []
for t, c, lab in parts:
    txt = ax.text(x, 2.2, t, ha="left", va="center", fontsize=10.5, color=c, family="monospace", fontweight="bold")
    bb = txt.get_window_extent(rend)
    w = (inv.transform((bb.x1, 0))[0] - inv.transform((bb.x0, 0))[0]) / f
    spans.append((x, x + w, c, lab))
    x += w
for x0, x1, c, lab in spans:
    ax.plot([x0 + 0.03, x0 + 0.03, x1 - 0.03, x1 - 0.03], [1.85, 1.7, 1.7, 1.85], color=c, lw=1.2)
    ax.text((x0 + x1) / 2, 1.35, lab, ha="center", va="center", fontsize=7.6, color=c)
ax.axis("off")
```

A domain name is read from the right. In `www.janataschool.edu.np`, **np** is
the **country code** of Nepal, **edu** shows the type of organisation
(education), **janataschool** is the organisation's own name and **www** is the
name of its web server. Other types used in Nepal are **gov.np** (government),
**com.np** (companies) and **org.np** (organisations); worldwide there are
**.com**, **.org**, **.net** and many more. A **.np** domain is registered free
of charge for Nepali citizens and organisations at `register.com.np`.

### HTML

::: definition HTML
**HTML (HyperText Markup Language)** is the language used to create web pages.
It **marks up** text with **tags** that tell the browser what each part is — a
heading, a paragraph, a list, a picture, a link. *HyperText* means text with
links to other text. HTML was created by Tim Berners-Lee; the current version
is **HTML5**.
:::

HTML is a **markup language**, not a programming language: it describes a
document but cannot calculate or make decisions.

**Tags.** A **tag** is a keyword written inside angle brackets: `<p>`. Most tags
are **container (paired) tags**: an **opening tag** `<b>` and a **closing tag**
`</b>` with a slash, with the content between them. A few are **empty
(unpaired) tags** that have no content and no closing tag: `<br>`, `<hr>`,
`<img>`. An **element** is the opening tag, the content and the closing tag
together.

**Attributes.** An **attribute** gives extra information about an element. It is
written **inside the opening tag** as `name="value"`, for example
`<img src="school.jpg" width="300">` or `<p align="center">`. HTML tags are
**not case-sensitive** (`<B>` works like `<b>`), but lower case is the modern
practice.

| Container (paired) tag | Empty (unpaired) tag |
|---|---|
| has an opening and a closing tag | has only one tag |
| encloses content: `<b>bold</b>` | has no content: `<br>` |
| e.g. `<html>`, `<p>`, `<h1>`, `<a>`, `<table>` | e.g. `<br>`, `<hr>`, `<img>` |

**Tools.** An HTML file is plain text, so any text editor will do: **Notepad**
on Windows, or code editors such as **Notepad++**, **Visual Studio Code** and
Sublime Text, which colour the tags. The file is saved with the extension
**.html** (or .htm) and opened in a **browser**.

## 10.2 Structure of an HTML document: html, head, title and body

Every web page has the same skeleton:

```html
<!DOCTYPE html>
<html>
<head>
  <title>My First Page</title>
</head>
<body>
  Namaste! This is my first web page.
</body>
</html>
```

| Part | Meaning |
|---|---|
| `<!DOCTYPE html>` | a declaration (not a tag) telling the browser that this is an HTML5 document; always the first line |
| `<html> … </html>` | the **root element**: everything else goes inside it |
| `<head> … </head>` | information **about** the page — its title, character set and so on; nothing in the head appears in the window |
| `<title> … </title>` | the page's title, shown on the browser **tab**, in bookmarks and in search results |
| `<body> … </body>` | everything that **appears in the browser window**: text, pictures, lists, tables, links |

```figure caption="The structure of an HTML document and where each part appears. Everything in the head (orange) is information about the page — the title shows on the browser's tab — while everything in the body (green) is shown in the window."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 2.9))
O, G = SERIES[3], SERIES[2]
code = ["<!DOCTYPE html>", "<html>", "<head>", "  <title>My First Page</title>", "</head>", "<body>",
        "  Namaste! This is my", "  first web page.", "</body>", "</html>"]
cols = [MUTED, INK, O, O, O, G, G, G, G, INK]
ax.add_patch(Rectangle((0.0, 0.1), 4.6, 4.6, fc="#f7f8fa", ec=MUTED, lw=0.7))
for k, (ln, c) in enumerate(zip(code, cols)):
    ax.text(0.15, 4.42 - k * 0.43, ln, ha="left", va="center", fontsize=7.4, family="monospace", color=c)
ax.add_patch(FancyBboxPatch((0.07, 2.5), 4.45, 1.27, boxstyle="round,pad=0.02", fc="none", ec=O, lw=1.0, ls="--"))
ax.add_patch(FancyBboxPatch((0.07, 0.77), 4.45, 1.68, boxstyle="round,pad=0.02", fc="none", ec=G, lw=1.0, ls="--"))
ax.text(4.42, 3.6, "head", ha="right", va="center", fontsize=7.0, color=O, fontweight="bold")
ax.text(4.42, 0.92, "body", ha="right", va="center", fontsize=7.0, color=G, fontweight="bold")
X0 = 5.0
ax.add_patch(Rectangle((X0, 0.6), 4.8, 3.9, fc="white", ec=INK, lw=0.9))
ax.add_patch(Rectangle((X0, 4.0), 4.8, 0.5, fc="#e9ecf1", ec=INK, lw=0.6))
ax.add_patch(Rectangle((X0 + 0.15, 4.07), 2.2, 0.36, fc="white", ec=O, lw=1.4))
ax.text(X0 + 0.25, 4.25, "My First Page", ha="left", va="center", fontsize=7.2, color=INK)
ax.text(X0 + 2.5, 4.25, "← the title", ha="left", va="center", fontsize=6.9, color=O)
ax.add_patch(Rectangle((X0 + 0.15, 3.55), 4.5, 0.32, fc="white", ec=MUTED, lw=0.6))
ax.text(X0 + 0.25, 3.71, "file:///D:/mysite/first.html", ha="left", va="center", fontsize=6.8, color=MUTED)
ax.add_patch(Rectangle((X0 + 0.12, 0.75), 4.56, 2.65, fc="none", ec=G, lw=1.0, ls="--"))
ax.text(X0 + 0.25, 3.12, "Namaste! This is my first web page.", ha="left", va="center", fontsize=7.4, color=INK, family="serif")
ax.text(X0 + 2.4, 0.98, "the body is shown here", ha="center", va="center", fontsize=6.9, color=G)
ax.set_xlim(-0.05, 9.9); ax.set_ylim(0.0, 4.8); ax.axis("off")
```

**Nesting.** Elements fit inside one another like boxes, and they must be
**closed in the reverse order** of opening: `<b><i>Nepal</i></b>` is correct,
`<b><i>Nepal</b></i>` is not. Indenting the code (as above) makes the nesting
easy to see.

The **body** tag can take attributes for the whole page, for example
`<body bgcolor="lightyellow" text="navy">` for the background and text colours.
Like `<font>` and `align` below, these old attributes still work in browsers but
are replaced in HTML5 by **CSS** (styles), which you will meet in Grade 9.

::: example Worked example 10.1 — your first web page
**Problem.** Write, save and open a web page whose tab reads *My First Page* and
whose window shows *Namaste! This is my first web page.*

**Solution.**
1. Open **Notepad** and type the seven lines of code shown above.
2. **File → Save As**. Choose a folder, e.g. `D:\mysite`. In **Save as type**
   choose **All files (\*.\*)**, type the name **`first.html`**, keep **Encoding:
   UTF-8**, and click **Save**.
3. Double-click `first.html` in File Explorer; it opens in the default browser.
   The tab shows **My First Page** and the window shows **Namaste! This is my
   first web page.**
4. To change the page, edit it in Notepad, **save** (Ctrl + S) and press **F5**
   in the browser to reload. **Ctrl + U** in the browser shows the page's source
   code.
:::

::: caution "first.html.txt" is not a web page
If **Save as type** is left as *Text Documents (\*.txt)*, Notepad saves
`first.html.txt`, which opens as plain text in Notepad again. Always choose
**All files** and type the `.html` extension yourself — and switch on *File name
extensions* in File Explorer so you can see what you saved.
:::

The browser ignores extra spaces and line breaks in the code: three spaces show
as one, and pressing Enter in Notepad does not start a new line on the page.
Lines and paragraphs are made with tags. Notes for yourself can be written as
**comments**, `<!-- like this -->`, which the browser does not show.

## 10.3 Formatting tags: headings, paragraphs, line breaks, bold, italic, underline and font

| Tag | Purpose | Example |
|---|---|---|
| `<h1>` … `<h6>` | headings, `<h1>` the largest and most important, `<h6>` the smallest; shown bold with space above and below | `<h1>Nepal</h1>` |
| `<p>` | a paragraph, with a blank line above and below | `<p>Text…</p>` |
| `<br>` | a line break: the next text starts on a new line (empty tag) | `Kathmandu<br>Nepal` |
| `<hr>` | a horizontal rule (line) across the page (empty tag) | `<hr>` |
| `<b>` | bold text (`<strong>` also bolds, marking important text) | `<b>China</b>` |
| `<i>` | italic text (`<em>` also italicises, for emphasis) | `<i>India</i>` |
| `<u>` | underlined text | `<u>Everest</u>` |
| `<sup>` / `<sub>` | superscript / subscript | `x<sup>2</sup>`, `H<sub>2</sub>O` |
| `<font>` | font face, size (1–7, default 3) and colour of text | `<font face="Arial" size="5" color="green">` |

The **align** attribute of headings and paragraphs takes `left` (default),
`center`, `right` or `justify`: `<h1 align="center">`. Colours are written as
names (`red`, `green`, `navy`) or as hexadecimal codes such as `#FF0000` (red)
and `#008000` (green).

::: example Worked example 10.2 — formatting text
**Problem.** Write the HTML for a page titled *Nepal* that shows a main heading
*Nepal*, a sub-heading *Geography*, a paragraph in which **China** is bold and
*India* is italic, a paragraph in which *Mount Everest* is underlined and the
height starts on a new line, a horizontal line, and the words *Visit Nepal!* in
green Arial at size 5.

**Solution.**

```html
<!DOCTYPE html>
<html>
<head>
  <title>Nepal</title>
</head>
<body>
  <h1>Nepal</h1>
  <h2>Geography</h2>
  <p>Nepal lies between <b>China</b> and <i>India</i>.</p>
  <p>Its highest peak is <u>Mount Everest</u>,<br>8,848.86 metres high.</p>
  <hr>
  <p><font face="Arial" size="5" color="green">Visit Nepal!</font></p>
</body>
</html>
```

The browser shows the two headings in bold, `<h1>` larger than `<h2>`; the
paragraphs with *China* in bold and *India* in italics; *Mount Everest*
underlined, with *8,848.86 metres high.* starting on the next line because of
`<br>`; a grey line across the page from `<hr>`; and *Visit Nepal!* in larger
green Arial letters.
:::

```figure caption="What Chromium shows for the formatting example of Worked example 10.2, redrawn: two headings of different sizes, bold, italic and underlined words, a forced line break, a horizontal rule, and green text from the font tag."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.6, 3.3))
ax.set_xlim(-0.05, 10.05); ax.set_ylim(0.8, 7.35)
f = min(5.9 / 4.6, 1.3)
ax.add_patch(Rectangle((0, 0.85), 10, 6.45, fc="white", ec=INK, lw=0.9))
ax.add_patch(Rectangle((0, 6.6), 10, 0.7, fc="#e9ecf1", ec=INK, lw=0.6))
ax.add_patch(Rectangle((0.2, 6.7), 2.6, 0.5, fc="white", ec=MUTED, lw=0.6))
ax.text(0.35, 6.95, "Nepal", ha="left", va="center", fontsize=7.4, color=INK)
S = dict(family="serif", color=INK, va="baseline")
ax.text(0.3, 5.75, "Nepal", fontsize=16, fontweight="bold", **S)
ax.text(0.3, 4.85, "Geography", fontsize=12, fontweight="bold", **S)
fig.canvas.draw(); rend = fig.canvas.get_renderer(); inv = ax.transData.inverted()
def run(x, y, parts):
    for t, kw in parts:
        tx = ax.text(x, y, t, fontsize=8.2, **S, **kw)
        bb = tx.get_window_extent(rend)
        x += (inv.transform((bb.x1, 0))[0] - inv.transform((bb.x0, 0))[0]) / f
    return x
run(0.3, 4.1, [("Nepal lies between ", {}), ("China", {"fontweight": "bold"}), (" and ", {}), ("India", {"style": "italic"}), (".", {})])
x0 = run(0.3, 3.45, [("Its highest peak is ", {})])
x1 = run(x0, 3.45, [("Mount Everest", {})])
ax.plot([x0, x1], [3.36, 3.36], color=INK, lw=0.7)
run(x1, 3.45, [(",", {})])
run(0.3, 2.95, [("8,848.86 metres high.", {})])
ax.plot([0.3, 9.7], [2.45, 2.45], color="#9aa1ab", lw=1.2)
ax.text(0.3, 1.6, "Visit Nepal!", fontsize=12, color="#008000", va="baseline")
ax.axis("off")
```

::: caution `<font>` and `align` are old HTML
The `<font>` tag and the `align`, `bgcolor` and `text` attributes come from
older HTML. Browsers still obey them, and they are in your syllabus, but HTML5
replaces them with **CSS**: the same green text is written
`<p style="color: green; font-family: Arial; font-size: 24px;">Visit Nepal!</p>`.
Learn the old tags for the exam and know that CSS is the modern way.
:::

## 10.4 Lists, images and hyperlinks

### Lists

**Unordered list** `<ul>` — items marked with bullets. Each item is an `<li>`
(list item). The `type` attribute chooses the bullet: `disc` (filled circle, the
default), `circle` (hollow) or `square`.

**Ordered list** `<ol>` — items numbered automatically. `type` chooses the
numbering: `1` (1, 2, 3 — default), `A` (A, B, C), `a` (a, b, c), `I` (I, II,
III) or `i` (i, ii, iii); `start` chooses the first number.

Lists can be **nested**: a `<ul>` or `<ol>` placed inside an `<li>` makes
sub-points. A **description list** `<dl>` holds terms `<dt>` and their
descriptions `<dd>`.

::: example Worked example 10.3 — what the browser shows
**Problem.** What does the browser show for this body?

```html
<h3>Fruits of Nepal</h3>
<ul type="square">
  <li>Mango</li>
  <li>Litchi</li>
  <li>Orange</li>
</ul>
<h3>Making tea</h3>
<ol>
  <li>Boil water.</li>
  <li>Add tea leaves.</li>
  <li>Add milk and sugar.</li>
</ol>
<ol type="I" start="3">
  <li>Kathmandu</li>
  <li>Pokhara</li>
  <li>Chitwan</li>
</ol>
```

**Solution.** The heading *Fruits of Nepal*, then Mango, Litchi and Orange each
with a **small square bullet**; the heading *Making tea*, then the steps numbered
**1. 2. 3.**; then Kathmandu, Pokhara and Chitwan numbered **III. IV. V.** —
Roman numerals (`type="I"`) starting from 3 (`start="3"`).
:::

### Images

The empty tag **`<img>`** places a picture on the page:

```html
<img src="images/school.jpg" alt="Our school building" width="320">
```

| Attribute | Meaning |
|---|---|
| `src` | **source**: the file name or path of the picture (required) |
| `alt` | **alternative text**: shown if the picture cannot load, and read aloud for blind users |
| `width`, `height` | size in pixels (give only one to keep the shape) |
| `border` | a border around the picture, in pixels (old HTML) |
| `align` | `left` or `right`: the picture floats and text flows beside it (old HTML) |

Pictures for the web are usually **JPG** (photos), **PNG** (drawings, logos,
transparency) or **GIF** (simple animations). The path is **relative** to the
page: `images/school.jpg` means "the file school.jpg in the folder images,
next to this page".

### Hyperlinks

The **anchor** tag `<a>` makes a hyperlink; its **`href`** (hypertext reference)
attribute gives the destination, and the text between the tags is what the
visitor clicks. Links appear **blue and underlined**, and purple once visited.

| Kind of link | Code |
|---|---|
| to another website (external) | `<a href="https://www.welcomenepal.com">Nepal Tourism Board</a>` |
| to another page of the same site | `<a href="about.html">About us</a>` |
| to open an email message | `<a href="mailto:info@janataschool.edu.np">Email us</a>` |
| to open in a new tab | `<a href="https://www.neb.gov.np" target="_blank">NEB</a>` |
| a picture as a link | `<a href="gallery.html"><img src="images/trip.jpg" alt="Photos"></a>` |
| to a place on the same page | `<a href="#notices">Notices</a>` jumps to `<h2 id="notices">` |

::: example Worked example 10.4 — a picture and links
**Problem.** A page in the same folder as an `images` folder has this body. The
file `missing.jpg` does not exist. What does the browser show?

```html
<h2>Phewa Lake</h2>
<img src="images/pokhara.jpg" alt="Phewa Lake, Pokhara" width="300">
<img src="images/missing.jpg" alt="Photo of Phewa Lake (file missing)" width="200">
<p>Read more at the <a href="https://www.welcomenepal.com">Nepal Tourism Board</a> website.</p>
<p><a href="about.html">About us</a> | <a href="mailto:info@janataschool.edu.np">Email us</a></p>
```

**Solution.** The heading, then the first picture 300 pixels wide. For the
second picture the browser finds no file, so it shows a small **broken-picture
icon with the alt text** *Photo of Phewa Lake (file missing)* — the reason `alt`
matters. Then a paragraph in which *Nepal Tourism Board* is a **blue underlined
link** to that website, and a line with two links: *About us* opens
`about.html`, and *Email us* opens the email program with the address filled in.
:::

## 10.5 Tables in HTML

A table is built row by row:

| Tag | Meaning |
|---|---|
| `<table>` … `</table>` | the whole table |
| `<caption>` | a title, shown centred above the table |
| `<tr>` | a **table row** |
| `<th>` | a **table heading** cell — bold and centred |
| `<td>` | a **table data** cell — normal and left-aligned |

| Attribute | Used in | Effect |
|---|---|---|
| `border="1"` | `<table>` | draws lines around cells (without it the table has no lines) |
| `cellpadding="6"` | `<table>` | space inside each cell, between text and border |
| `cellspacing="2"` | `<table>` | space between neighbouring cells |
| `width`, `bgcolor`, `align` | `<table>`, `<td>` | width, background colour, position |
| `colspan="2"` | `<th>`, `<td>` | the cell **spans two columns** |
| `rowspan="2"` | `<th>`, `<td>` | the cell **spans two rows** |

::: example Worked example 10.5 — two tables
**Problem.** (a) Write the code for a bordered table captioned *Class 8
Results* with headings Name, Maths and Science and two rows: Asha 85 92 and
Rohan 72 64. (b) What does the following code show, and how many cells does it
have?

```html
<table border="1" cellpadding="6">
  <tr>
    <th rowspan="2">Day</th>
    <th colspan="2">Periods</th>
  </tr>
  <tr>
    <th>1st</th>
    <th>2nd</th>
  </tr>
  <tr>
    <td>Sunday</td>
    <td>Maths</td>
    <td>Science</td>
  </tr>
  <tr>
    <td>Monday</td>
    <td colspan="2">Sports Day</td>
  </tr>
</table>
```

**Solution.** (a)

```html
<table border="1">
  <caption>Class 8 Results</caption>
  <tr>
    <th>Name</th>
    <th>Maths</th>
    <th>Science</th>
  </tr>
  <tr>
    <td>Asha</td>
    <td>85</td>
    <td>92</td>
  </tr>
  <tr>
    <td>Rohan</td>
    <td>72</td>
    <td>64</td>
  </tr>
</table>
```

The caption appears centred above; the three headings are bold and centred.

(b) A 4-row, 3-column routine: *Day* fills two rows on the left, *Periods* fills
two columns above *1st* and *2nd*, the Sunday row has three cells, and *Sports
Day* stretches across both period columns on Monday. Counting the `<th>` and
`<td>` tags: 2 + 2 + 3 + 2 = **9 cells**, filling the 4 × 3 = 12 places because
three cells each cover two places (12 − 3 = 9).
:::

```figure caption="The routine table of Worked example 10.5 as the browser draws it. The heading Day spans two rows (rowspan=2), Periods spans two columns (colspan=2), and so does Sports Day, so the 4 × 3 grid holds only 9 cells."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0, 2.6))
W = [1.6, 1.3, 1.3]; H = 0.55
xs = [0, 1.6, 2.9]
def cell(c0, r0, cs, rs, t, head=False, hl=None):
    x = xs[c0]; w = sum(W[c0:c0 + cs]); y = 3 - (r0 + rs) * H
    ax.add_patch(Rectangle((x, y), w, rs * H, fc=hl or ("#eef1f5" if head else "white"), ec=INK, lw=0.9))
    ax.text(x + w / 2, y + rs * H / 2, t, ha="center", va="center", fontsize=7.6, color=INK,
            fontweight="bold" if head else "normal", family="serif")
cell(0, 0, 1, 2, "Day", True, "#fdf1d6")
cell(1, 0, 2, 1, "Periods", True, "#e6f0fa")
cell(1, 1, 1, 1, "1st", True); cell(2, 1, 1, 1, "2nd", True)
cell(0, 2, 1, 1, "Sunday"); cell(1, 2, 1, 1, "Maths"); cell(2, 2, 1, 1, "Science")
cell(0, 3, 1, 1, "Monday"); cell(1, 3, 2, 1, "Sports Day", False, "#e6f0fa")
def note(tx, ty, px, py, t, c, ha="left"):
    ax.annotate(t, xy=(px, py), xytext=(tx, ty), fontsize=7.0, color=c, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color=c, lw=0.7, relpos=(0, 0.5) if ha == "left" else (1, 0.5)))
note(4.6, 2.85, 4.1, 2.75, '<th colspan="2">', ACCENT)
note(4.6, 0.95, 4.1, 1.07, '<td colspan="2">', ACCENT)
note(-0.25, 2.45, 0.05, 2.45, '<th rowspan="2">', SERIES[3], ha="right")
ax.text(4.6, 2.2, "row 2: two <th> cells", fontsize=6.9, color=MUTED, va="center")
ax.text(4.6, 1.65, "row 3: three <td> cells", fontsize=6.9, color=MUTED, va="center")
ax.set_xlim(-2.4, 7.6); ax.set_ylim(0.65, 3.1); ax.axis("off")
```

::: caution Every row must add up
In a table, every row must cover the same number of columns once the spans are
counted. If the first row has `colspan="2"` plus one cell (3 columns), every
other row must also total 3. A missing `<td>` or an extra one makes the columns
slip out of line.
:::

## 10.6 Creating and viewing a small website

A **website** is a set of web pages in one folder, linked to each other by a
menu of links. Plan it on paper first: the pages, what each holds, and the
links between them (a **site map**).

```figure caption="A small school website. The folder mysite holds four pages and a folder of pictures; the menu of links at the top of every page (dashed arrows) lets a visitor move from any page to any other. The home page is named index.html."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
fig, ax = plt.subplots(figsize=(5.2, 3.0))
tree = [(0.0, "mysite", "folder"), (0.35, "index.html", "page"), (0.35, "about.html", "page"),
        (0.35, "gallery.html", "page"), (0.35, "contact.html", "page"), (0.35, "images", "folder"),
        (0.7, "school.jpg", "file"), (0.7, "trip.jpg", "file")]
for k, (x, t, kind) in enumerate(tree):
    y = 4.3 - k * 0.5
    col = "#f6d47a" if kind == "folder" else ("#cfe0f1" if kind == "page" else "#e2e6ec")
    ax.add_patch(Rectangle((x, y - 0.14), 0.26, 0.28, fc=col, ec=MUTED, lw=0.6))
    ax.text(x + 0.36, y, t, ha="left", va="center", fontsize=7.4, color=INK, family="monospace")
    if k > 0:
        px = 0.13 if x == 0.35 else 0.48
        ax.plot([px, px, x], [y + (0.36 if k in (1, 6) else 0.5), y, y], color=MUTED, lw=0.7)
pages = {"index.html\n(Home)": (5.0, 3.7), "about.html": (8.85, 3.7), "gallery.html": (5.0, 1.4), "contact.html": (8.85, 1.4)}
for t, (x, y) in pages.items():
    ax.add_patch(FancyBboxPatch((x - 1.6, y - 0.55), 3.2, 1.1, boxstyle="round,pad=0.02,rounding_size=0.08",
                 fc="white", ec=ACCENT, lw=1.1))
    ax.add_patch(Rectangle((x - 1.55, y + 0.25), 3.1, 0.22, fc="#e6f0fa", ec="none"))
    ax.text(x, y + 0.36, "Home | About | Gallery | Contact", ha="center", va="center", fontsize=6.1, color=ACCENT)
    ax.text(x, y - 0.18, t, ha="center", va="center", fontsize=7.4, color=INK, family="monospace", linespacing=1.15)
pairs = [((6.63, 3.7), (7.22, 3.7)), ((5.0, 3.12), (5.0, 1.98)), ((8.85, 3.12), (8.85, 1.98)), ((6.63, 1.4), (7.22, 1.4)),
         ((6.1, 3.12), (7.75, 1.98)), ((7.75, 3.12), (6.1, 1.98))]
for a, b in pairs:
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="<|-|>", color=MUTED, lw=0.9, ls="--", mutation_scale=9))
ax.set_xlim(-0.1, 10.55); ax.set_ylim(0.6, 4.6); ax.axis("off")
```

**Steps**

1. Make a folder `mysite`, and inside it a folder `images` holding the pictures
   (e.g. `school.jpg`).
2. Write the **home page** and save it in `mysite` as **`index.html`**:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Shree Janata School - Home</title>
</head>
<body bgcolor="#f2f7ff">
  <p>
    <a href="index.html">Home</a> |
    <a href="about.html">About</a> |
    <a href="gallery.html">Gallery</a> |
    <a href="contact.html">Contact</a>
  </p>
  <hr>
  <h1 align="center">Shree Janata Secondary School</h1>
  <p align="center"><i>Lakeside, Pokhara</i></p>
  <img src="images/school.jpg" alt="Our school building" width="320">
  <h2>Notices</h2>
  <ul>
    <li>Science Exhibition on 15 Falgun</li>
    <li>Admission open for Grade 6</li>
  </ul>
</body>
</html>
```

3. Save a copy as `about.html`, keep the head and the menu, change the title to
   *Shree Janata School - About* and replace the rest of the body with that
   page's content. Do the same for `gallery.html` and `contact.html`, so every
   page has the **same menu**.
4. **View:** double-click `index.html`. Tested in Chromium, it shows a pale blue
   page with the menu of four blue links, a line, the centred heading and the
   italic address, the picture and the bulleted notices; clicking **About**
   opens `about.html` and the tab changes to *Shree Janata School - About*.
5. **Test** every link and picture, in more than one browser if you can, and
   fix any page that does not work.
6. **Publish** (optional): to put the site on the Internet, copy the folder to a
   **web server** through a hosting service, and connect a domain name to it.
   Free hosting such as GitHub Pages exists, and a `.np` domain is free for
   Nepali citizens and organisations.

::: example Worked example 10.6 — find the mistakes
**Problem.** A student's page shows a broken picture; clicking *About us* gives
"File not found"; the second paragraph comes out bold as well; and the word
*Pokhara* does not appear at all. The files in the folder are `index.html`,
`about.html` and `images/logo.png`. Find the four mistakes:

```html
<img src="image/logo.png" alt="School logo">
<a href="About.htm">About us</a>
<p>Welcome to <b>our school.</p>
<p>We teach Grades 1 to 10.</p>
<p align="center>Pokhara</p>
```

**Solution.** (1) The folder is `images`, not `image`: write
`src="images/logo.png"`. (2) The file is `about.html`, not `About.htm`: the
extension is wrong, and on web servers capital letters matter too, so write
`href="about.html"`. (3) `<b>` is never closed, so the browser keeps the bold
going into the next paragraph: write `<b>our school.</b>`. (4) The quotation mark
after `center` is missing, so the browser reads everything up to the next
quotation mark as the attribute's value and *Pokhara* disappears: write
`align="center"`.
:::

::: note Activity 10.1 — your own three-page website
Make a folder named after your district. Write three pages — `index.html`
(home), `places.html` and `contact.html` — with the same menu of links on each.
The home page needs a heading, a paragraph with bold and italic words, and a
picture; *places.html* needs an ordered list of five places and a table of their
distances from your school; *contact.html* needs an email link. Test every link
in two browsers, then show your teacher the code with **Ctrl + U**.
:::

::: tip Writing HTML in the exam
Always start with the skeleton: `<!DOCTYPE html>`, `<html>`, `<head>` with
`<title>`, `<body>`. Close every container tag in reverse order, put attribute
values in **double quotes**, and indent nested tags. For a table, draw the grid
first and count the cells of every row, including the spans.
:::

## Chapter summary

- The **WWW** (Tim Berners-Lee, CERN, 1989–1991) is a collection of linked web
  pages on web servers, opened over the Internet with a **browser**. A **web
  page** is one HTML document; a **website** is related pages under one domain;
  the **home page** is `index.html`.
- **URL** (Uniform Resource Locator) = protocol (`https://`) + domain name
  (`www.name.edu.np`) + path + file name. **HTTP(S)** is the transfer protocol.
- **HTML** (HyperText Markup Language, now HTML5) uses **tags** in angle
  brackets: **container** tags `<p>…</p>`, **empty** tags `<br>`, `<hr>`,
  `<img>`; **attributes** go in the opening tag: `name="value"`.
- **Structure:** `<!DOCTYPE html>`, `<html>`, `<head>` with `<title>` (shown on
  the tab), `<body>` (shown in the window). Close tags in reverse order.
- **Formatting:** `<h1>`–`<h6>`, `<p>`, `<br>`, `<hr>`, `<b>`, `<i>`, `<u>`,
  `<sup>`, `<sub>`, `<font face size color>` (old; CSS today), `align`.
- **Lists:** `<ul type="disc|circle|square">`, `<ol type="1|A|a|I|i"
  start="n">`, `<li>`. **Image:** `<img src alt width height>`. **Link:** `<a
  href="…">`, `mailto:`, `target="_blank"`.
- **Tables:** `<table border>`, `<caption>`, `<tr>`, `<th>` (bold, centred),
  `<td>`; `colspan`, `rowspan`. A **website** is a folder of linked pages with
  the same menu, saved as .html and tested in a browser.

## Practice questions

**Group A — Objective (1 mark each)**

1. The World Wide Web was invented by <span class="marks">[1]</span>
   (a) Charles Babbage (b) Tim Berners-Lee (c) Bill Gates (d) Linus Torvalds
2. HTML stands for <span class="marks">[1]</span>
   (a) HyperText Markup Language (b) High Transfer Machine Language (c) HyperText Making Language (d) Home Tool Markup Language
3. Which of these is a web browser? <span class="marks">[1]</span>
   (a) Notepad (b) Microsoft Edge (c) Excel (d) Windows
4. In `https://www.neb.gov.np/results.html`, the domain name is <span class="marks">[1]</span>
   (a) https (b) www.neb.gov.np (c) results.html (d) np
5. Which is an empty (unpaired) tag? <span class="marks">[1]</span>
   (a) `<p>` (b) `<b>` (c) `<br>` (d) `<title>`
6. The text between `<title>` and `</title>` appears <span class="marks">[1]</span>
   (a) as the largest heading (b) on the browser tab (c) at the bottom of the page (d) nowhere
7. Which heading tag shows the largest text? <span class="marks">[1]</span>
   (a) `<h6>` (b) `<h3>` (c) `<h1>` (d) `<head>`
8. `<ol type="A" start="2">` with three items numbers them <span class="marks">[1]</span>
   (a) A, B, C (b) B, C, D (c) 2, 3, 4 (d) II, III, IV
9. The attribute that gives the file of a picture in `<img>` is <span class="marks">[1]</span>
   (a) href (b) alt (c) src (d) link
10. The tag that makes a hyperlink is <span class="marks">[1]</span>
    (a) `<a>` (b) `<link>` (c) `<h>` (d) `<l>`
11. In a table, a cell that stretches across two columns uses <span class="marks">[1]</span>
    (a) `rowspan="2"` (b) `colspan="2"` (c) `cellpadding="2"` (d) `border="2"`
12. A web page should be saved with the extension <span class="marks">[1]</span>
    (a) .txt (b) .docx (c) .html (d) .exe

::: note Answers to Group A
**1.** (b) — Tim Berners-Lee at CERN, 1989–1991.
**2.** (a) — HyperText Markup Language.
**3.** (b) — Edge is a browser; Notepad is a text editor.
**4.** (b) — https is the protocol and results.html the file name.
**5.** (c) — `<br>` has no closing tag.
**6.** (b) — the title is shown on the tab.
**7.** (c) — `<h1>` is the largest.
**8.** (b) — capital letters starting from the 2nd, B.
**9.** (c) — src (source); alt is the alternative text.
**10.** (a) — the anchor tag with href.
**11.** (b) — colspan spans columns.
**12.** (c) — .html (or .htm).
:::

**Group B — Short answer (2 marks each)**

1. Differentiate between a web page and a website. <span class="marks">[2]</span>
2. What is a URL? Name its parts in `https://www.moecdc.gov.np/index.html`. <span class="marks">[2]</span>
3. Differentiate between the Internet and the World Wide Web. <span class="marks">[2]</span>
4. Differentiate between container and empty tags with two examples of each. <span class="marks">[2]</span>
5. What is an attribute? Give an example. <span class="marks">[2]</span>
6. Write the basic structure of an HTML document. <span class="marks">[2]</span>
7. Write HTML code to show *Computer Science* as the largest, centred heading and *Grade 8* below it in red. <span class="marks">[2]</span>
8. Write the code for an unordered list of three districts with square bullets. <span class="marks">[2]</span>
9. Write the code to insert the picture `rhino.jpg`, 250 pixels wide, with suitable alternative text. <span class="marks">[2]</span>
10. Write code that makes the words *Visit NEB* a link to `https://www.neb.gov.np`, opening in a new tab. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A web page is a single HTML document that can be viewed in a browser. A
website is a collection of related web pages under one domain name, linked
together, such as `www.neb.gov.np`.

**2.** A URL (Uniform Resource Locator) is the unique address of a resource on
the web. Parts: protocol `https://`, domain name `www.moecdc.gov.np`, file name
`index.html`.

**3.** The Internet is the worldwide network of networks — the cables, routers
and computers. The World Wide Web is a service that runs on the Internet: the
collection of linked web pages opened with a browser. (Email is another Internet
service.)

**4.** A container tag has an opening and a closing tag around content, e.g.
`<p>…</p>`, `<b>…</b>`. An empty tag has no content and no closing tag, e.g.
`<br>`, `<hr>`, `<img>`.

**5.** An attribute gives extra information about an element and is written in
the opening tag as name="value", e.g. `<img src="logo.png">` or
`<p align="center">`.

**6.**
```html
<!DOCTYPE html>
<html>
<head>
  <title>Page title</title>
</head>
<body>
  Page content
</body>
</html>
```

**7.**
```html
<h1 align="center">Computer Science</h1>
<p><font color="red">Grade 8</font></p>
```

**8.**
```html
<ul type="square">
  <li>Kaski</li>
  <li>Chitwan</li>
  <li>Jhapa</li>
</ul>
```

**9.** `<img src="rhino.jpg" alt="One-horned rhinoceros" width="250">`

**10.** `<a href="https://www.neb.gov.np" target="_blank">Visit NEB</a>`
:::

**Group C — Long answer (4 marks each)**

1. Write the HTML for a page titled *My District* that shows a centred main heading, a paragraph with one bold and one italic word, a line, and a numbered list of three places to visit. <span class="marks">[4]</span>
2. Write the HTML for this table, with a border and the caption *Marks*: a header row Name, English, Nepali; and rows Sita 78 85 and Hari 66 72. <span class="marks">[4]</span>
3. Write the HTML for a table whose first row is a heading *Fee Details* spanning three columns, followed by the heading row Grade, Monthly fee, Exam fee and the rows 7, 1500, 300 and 8, 1700, 350. How many cells does it have? <span class="marks">[3+1]</span>
4. Explain the steps to create a two-page website (home and about) linked to each other, and to view it in a browser. <span class="marks">[4]</span>
5. Explain the terms web browser, URL, HTML and hyperlink with one example each. <span class="marks">[4]</span>

::: note Answers to Group C
**1.**
```html
<!DOCTYPE html>
<html>
<head>
  <title>My District</title>
</head>
<body>
  <h1 align="center">Kaski District</h1>
  <p>Kaski is famous for <b>Phewa Lake</b> and the <i>Annapurna</i> range.</p>
  <hr>
  <ol>
    <li>Sarangkot</li>
    <li>World Peace Pagoda</li>
    <li>Davis Falls</li>
  </ol>
</body>
</html>
```

**2.**
```html
<table border="1">
  <caption>Marks</caption>
  <tr>
    <th>Name</th>
    <th>English</th>
    <th>Nepali</th>
  </tr>
  <tr>
    <td>Sita</td>
    <td>78</td>
    <td>85</td>
  </tr>
  <tr>
    <td>Hari</td>
    <td>66</td>
    <td>72</td>
  </tr>
</table>
```

**3.**
```html
<table border="1">
  <tr>
    <th colspan="3">Fee Details</th>
  </tr>
  <tr>
    <th>Grade</th>
    <th>Monthly fee</th>
    <th>Exam fee</th>
  </tr>
  <tr>
    <td>7</td>
    <td>1500</td>
    <td>300</td>
  </tr>
  <tr>
    <td>8</td>
    <td>1700</td>
    <td>350</td>
  </tr>
</table>
```
Cells: 1 + 3 + 3 + 3 = **10** (the first cell covers three places of the
4 × 3 = 12, so 12 − 2 = 10).

**4.** Make a folder `mysite`. In Notepad write the home page with the HTML
skeleton, a title, a heading and a link `<a href="about.html">About</a>`; save it
in the folder as `index.html` (Save as type: All files, Encoding UTF-8). Write the
about page with its own title and content and a link `<a href="index.html">Home</a>`;
save it as `about.html` in the same folder. Double-click `index.html` to open it in
the browser; click *About* to check that the about page opens, and *Home* to come
back. Correct any mistakes in Notepad, save, and press F5 to reload.

**5.** *Web browser:* application software that requests and displays web
pages — Google Chrome, Firefox. *URL:* the unique address of a web page —
`https://www.neb.gov.np`. *HTML:* the markup language of web pages, using tags —
`<h1>Nepal</h1>`. *Hyperlink:* text or a picture that opens another page when
clicked — `<a href="about.html">About us</a>`.
:::
