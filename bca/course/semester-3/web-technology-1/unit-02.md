---
subject: Web Technology I
grade: BCA Semester 3
unit: 2
title: HTML and Graphics
area: BCA 203 · Web Technology I · Unit 2
---

**HTML** (HyperText Markup Language) describes the *structure and meaning* of a web page with **elements** made of tags. HTML5 is the current standard; CSS (Unit 4) handles appearance and JavaScript (Unit 3) behaviour.

::: key What this unit gives you
- Document structure, text, links, images, lists, tables.
- Forms with every input type, and semantic HTML5 layout elements.
- Audio, video and frames, plus graphics with image maps, `<canvas>` and SVG.
:::

## 2.1 Document structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>My first page</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1>Welcome</h1>
  <p>Hello, <strong>world</strong>!</p>
  <script src="app.js"></script>
</body>
</html>
```

An element is `<tag attribute="value">content</tag>`; **void** elements (`<br>`, `<img>`, `<hr>`, `<input>`, `<meta>`, `<link>`) have no end tag. Tags nest properly; names are case-insensitive but written lowercase. **Global attributes**: `id` (unique), `class`, `style`, `title`, `lang`, `hidden`, `data-*`. **Comments:** `<!-- … -->`. **Entities:** `&lt;` `&gt;` `&amp;` `&quot;` `&nbsp;` `&copy;`. The `<head>` holds metadata (not displayed); `<body>` holds visible content.

## 2.2 Text, links, images, lists

| Element | Purpose |
|---|---|
| `<h1>`–`<h6>` | headings (one `h1` per page; do not skip levels) |
| `<p>`, `<br>`, `<hr>` | paragraph, line break, thematic break |
| `<strong>`, `<em>`, `<mark>`, `<code>`, `<pre>`, `<blockquote>`, `<sub>`, `<sup>` | meaning-carrying inline and block text (prefer these to `<b>`, `<i>`) |
| `<a href="url">` | **hyperlink**; `target="_blank"` opens a new tab (add `rel="noopener"`); `href="#id"` jumps within the page; `mailto:` and `tel:` links |
| `<img src alt width height>` | image; `alt` text is essential for accessibility and when the image fails to load |
| `<ul>`/`<ol>`/`<li>` | unordered (bullets) and ordered (numbers) lists; `<dl><dt><dd>` description lists |

```html
<h2>Course links</h2>
<p>Read the <a href="unit3.html">JavaScript unit</a> or
   <a href="https://developer.mozilla.org" target="_blank" rel="noopener">MDN</a>.</p>
<img src="logo.png" alt="NEBians logo" width="120" height="120">
<ol>
  <li>HTML</li>
  <li>CSS
    <ul><li>Selectors</li><li>Box model</li></ul>
  </li>
</ol>
```

## 2.3 Tables

```html
<table border="1">
  <caption>Marks sheet</caption>
  <thead><tr><th>Name</th><th>DBMS</th><th>DSA</th></tr></thead>
  <tbody>
    <tr><td>Sita</td><td>85</td><td>72</td></tr>
    <tr><td>Ram</td><td colspan="2">absent</td></tr>
  </tbody>
  <tfoot><tr><td colspan="3">Pass marks: 40</td></tr></tfoot>
</table>
```

`<tr>` row, `<th>` header cell, `<td>` data cell; `colspan` and `rowspan` merge cells; `<thead>`, `<tbody>`, `<tfoot>` group rows. Use tables for **data**, not for page layout (use CSS, Unit 4).

## 2.4 Forms

A form sends user input to a server: `<form action="/register" method="post">`. `action` is the URL that receives the data; `method` is `get` or `post`; `enctype="multipart/form-data"` is required for file upload. Each control needs a `name` (the key sent) and a `<label for="id">`.

```html
<form action="/register" method="post">
  <label for="nm">Name</label>
  <input type="text" id="nm" name="name" required minlength="2" placeholder="Full name">

  <label for="em">Email</label>
  <input type="email" id="em" name="email" required>

  <label for="pw">Password</label>
  <input type="password" id="pw" name="password" minlength="8" required>

  <label for="dob">Date of birth</label>
  <input type="date" id="dob" name="dob">

  Gender:
  <input type="radio" name="gender" value="f" id="gf"><label for="gf">Female</label>
  <input type="radio" name="gender" value="m" id="gm"><label for="gm">Male</label>

  <input type="checkbox" name="agree" value="yes" id="ag"><label for="ag">I agree</label>

  <label for="sem">Semester</label>
  <select id="sem" name="semester">
    <option value="">--choose--</option>
    <option value="3" selected>Third</option>
    <option value="4">Fourth</option>
  </select>

  <label for="msg">Message</label>
  <textarea id="msg" name="message" rows="3" cols="30"></textarea>

  <input type="hidden" name="source" value="signup">
  <button type="submit">Register</button>
  <button type="reset">Clear</button>
</form>
```

| Input `type` | Control |
|---|---|
| `text`, `password`, `email`, `url`, `tel`, `search` | one-line text with built-in checks for email/url |
| `number`, `range` | numeric box / slider with `min`, `max`, `step` |
| `date`, `time`, `datetime-local`, `month`, `week`, `color` | pickers |
| `radio` | one choice from a group sharing the same `name` |
| `checkbox` | on/off; several may be chosen |
| `file` | upload |
| `hidden` | value sent but not shown |
| `submit`, `reset`, `button`, `image` | buttons |

**HTML5 validation attributes:** `required`, `pattern="regex"`, `min`/`max`, `minlength`/`maxlength`, `readonly`, `disabled`, `autofocus`, `placeholder`. `<fieldset>`/`<legend>` group controls; `<datalist>` offers suggestions. Client-side validation helps users but **can be bypassed**, so the server must validate again.

## 2.5 Semantic HTML5 layout

```html
<body>
  <header><h1>College portal</h1><nav><a href="/">Home</a> <a href="/results">Results</a></nav></header>
  <main>
    <article><h2>Exam notice</h2><p>…</p></article>
    <aside>Related links</aside>
  </main>
  <footer>&copy; 2082 NEBians</footer>
</body>
```

`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`, `<figure>`/`<figcaption>`, `<time>` tell browsers, search engines and screen readers what each part *is*, unlike anonymous `<div>` and `<span>`.

## 2.6 Multimedia and frames

```html
<video controls width="320" poster="cover.jpg">
  <source src="lesson.mp4" type="video/mp4">
  <source src="lesson.webm" type="video/webm">
  Your browser does not support video.
</video>
<audio controls src="song.mp3"></audio>
<iframe src="https://www.openstreetmap.org/export/embed.html" width="400" height="250" title="Map"></iframe>
```

`<video>` and `<audio>` replaced Flash plug-ins; supply several formats and a fallback message. `<iframe>` embeds another page (maps, videos); beware of security and use `sandbox`. The old `<frameset>` is obsolete.

## 2.7 Graphics: images, image maps, canvas and SVG

- **Raster images** (JPEG for photos, PNG for transparency and sharp edges, GIF for simple animation, WebP/AVIF for smaller files) are grids of pixels and blur when enlarged. **Vector** graphics (SVG) are shapes defined by math and scale without loss. Use `srcset` and `<picture>` to serve sizes suited to the screen.
- **Image map**: clickable regions on one image.

```html
<img src="campus.png" alt="Campus map" usemap="#campus" width="400" height="200">
<map name="campus">
  <area shape="rect" coords="0,0,200,100" href="library.html" alt="Library">
  <area shape="circle" coords="300,100,50" href="lab.html" alt="Computer lab">
  <area shape="poly" coords="200,150,350,150,275,200" href="canteen.html" alt="Canteen">
</map>
```

- **SVG** is XML-based vector graphics embedded directly in HTML and styled with CSS:

```html
<svg width="220" height="120" viewBox="0 0 220 120" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="100" height="60" fill="#1F4E8C" rx="8"/>
  <circle cx="160" cy="40" r="30" fill="orange" stroke="black" stroke-width="2"/>
  <line x1="10" y1="100" x2="210" y2="100" stroke="green" stroke-width="3"/>
  <text x="10" y="116" font-size="12">SVG shapes</text>
</svg>
```

- **Canvas** is a pixel drawing surface painted by JavaScript (good for games and charts):

```html
<canvas id="c" width="200" height="100"></canvas>
<script>
  const ctx = document.getElementById("c").getContext("2d");
  ctx.fillStyle = "tomato";  ctx.fillRect(10, 10, 80, 50);
  ctx.beginPath(); ctx.arc(140, 40, 30, 0, 2 * Math.PI); ctx.stroke();
</script>
```

| | SVG | Canvas |
|---|---|---|
| Model | retained: each shape is a DOM element | immediate: pixels, no objects remain |
| Scaling | perfect | blurs unless redrawn |
| Events | per shape | you compute hits |
| Best for | logos, icons, diagrams | games, many moving objects |

## 2.8 Seeing HTML: browsers, trees and boxes

HTML is easiest to understand when you see what a browser does with it. The plate below shows the first mainstream graphical browser, a 1990s commercial browser and a modern developer-tools panel. The figures then draw the document tree, the semantic page layout, a table with merged cells, the form controls and the canvas coordinate system.

```photogrid label="2.1" cols="3" ratio="1.1" caption="Three views of the same idea: a browser turns tagged text into a page. (a) NCSA Mosaic, the 1993 browser that made inline images popular. (b) Netscape Navigator 3, which added frames, tables with colour and JavaScript support. (c) The inspector of a modern Firefox, where the HTML tree is shown at the bottom and the matching CSS rules at the right. Screenshots are free of copyright restrictions or licensed as listed in the Picture Credits."
@ photo id="bca203/mosaic" cap="NCSA Mosaic, 1993"
fit 1.1
focus 0.5 0.6
mark 0.12 0.83 "1"
mark 0.30 0.52 "2"
key 1 Page title and address bar
key 2 Inline image and hyperlinks (blue, underlined)
@ photo id="bca203/netscape" cap="Netscape Navigator 3"
fit 1.1
focus 0.4 0.6
mark 0.10 0.70 "1"
mark 0.12 0.40 "2"
key 1 Toolbar with Back, Reload, Home
key 2 Logos placed beside text
@ photo id="bca203/inspector" cap="Modern developer tools"
fit 1.1
focus 0.5 0.35
mark 0.40 0.62 "1"
mark 0.75 0.30 "2"
key 1 Element tree (the DOM)
key 2 CSS rules for the chosen element
```

```svgfig label="2.1" caption="The document tree built from a five-line page. The browser parses html into a tree of elements: html has two children, head and body; body has an h1 and a p; the p contains the text, a link element a and more text. Every element is a node, text is a node, and attributes (href here) belong to their element. CSS and JavaScript later select nodes from this same tree, so a missing closing tag changes the tree and therefore the page."
f = Fig(580, 230)
def n(x, y, t, c=NAVY, fill=BLUE, w=70):
    f.box(x - w / 2, y, w, 28, t, fill=fill, stroke=c, size=10.5, bold=True)
n(290, 8, "html"); n(150, 66, "head"); n(430, 66, "body")
n(90, 124, "title", w=60); n(430 - 90, 124, "h1", w=50); n(500, 124, "p", w=50)
n(90, 182, "text", c=TEAL, fill=MINT, w=60); n(340, 182, "text", c=TEAL, fill=MINT, w=60); n(440, 182, "a", c=RED, fill=ROSE, w=50); n(540, 182, "text", c=TEAL, fill=MINT, w=60)
for a, b in [((290, 36), (150, 66)), ((290, 36), (430, 66)), ((150, 94), (90, 124)), ((430, 94), (340, 124)), ((430, 94), (500, 124)), ((90, 152), (90, 182)), ((340, 152), (340, 182)), ((500, 152), (440, 182)), ((500, 152), (540, 182))]:
    f.line(a[0], a[1], b[0], b[1], color=SLATE)
f.text(440, 218, 'attribute href="/about"', size=9.5, color=RED, bold=True)
f.text(30, 218, "elements = blue/red, text = green", size=9.5, color=SLATE, anchor="start")
```

```svgfig label="2.2" caption="A semantic HTML5 page. header holds the logo and title, nav the main links, main the unique content of the page (with article for self-contained stories and aside for related items), and footer the contact and copyright text. Screen readers and search engines use these landmarks to jump to the right part, which divs with only class names cannot offer."
f = Fig(580, 250)
f.box(60, 8, 460, 36, "<header>  logo + site title", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(60, 50, 460, 28, "<nav>  Home | Notices | Admission | Contact", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(60, 84, 460, 118, "", fill=SOFT, stroke=SLATE)
f.text(76, 98, "<main>", size=10.5, color=SLATE, bold=True, anchor="start")
f.box(76, 108, 290, 84, "<article>\n<h1> + <p> + <figure>", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(380, 108, 124, 84, "<aside>\nrelated links", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(60, 208, 460, 34, "<footer>  address, phone, copyright", fill=BLUE, stroke=NAVY, size=11, bold=True)
```

```svgfig label="2.3" caption="A table with merged cells and the code that makes it. The heading cell Time spans two columns (colspan=2) and the cell Break spans two rows (rowspan=2). The grid has 3 columns and 4 rows, but the second row has only two cells of its own because Break covers the third. Count cells per row after merging: row 1 = 2 cells (Day, Time), row 2 = 3, row 3 = 3, row 4 = 2 + the merged cell."
f = Fig(580, 200)
f.box(10, 10, 130, 30, "Day", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(140, 10, 260, 30, "Time  (colspan=2)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(10, 40, 130, 30, "Sunday", fill=SOFT, stroke=SLATE, size=11)
f.box(140, 40, 130, 30, "10:00 HTML", fill=SOFT, stroke=SLATE, size=11)
f.box(270, 40, 130, 60, "Break\n(rowspan=2)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(10, 70, 130, 30, "Monday", fill=SOFT, stroke=SLATE, size=11)
f.box(140, 70, 130, 30, "10:00 CSS", fill=SOFT, stroke=SLATE, size=11)
f.box(10, 100, 130, 30, "Tuesday", fill=SOFT, stroke=SLATE, size=11)
f.box(140, 100, 130, 30, "10:00 JS", fill=SOFT, stroke=SLATE, size=11)
f.box(270, 100, 130, 30, "11:00 Lab", fill=SOFT, stroke=SLATE, size=11)
f.text(420, 26, "<th colspan=\"2\">Time</th>", size=9.5, color=NAVY, bold=True, anchor="start")
f.text(420, 70, "<td rowspan=\"2\">Break</td>", size=9.5, color=AMBER, bold=True, anchor="start")
f.text(10, 170, "Rows of the code: <tr><th>Day</th><th colspan=\"2\">Time</th></tr> then one <tr> per day.", size=9.5, color=SLATE, anchor="start")
f.text(10, 188, "Remember: a spanned cell is written once; the cells it covers are left out of later rows.", size=9.5, color=TEAL, bold=True, anchor="start")
```

```svgfig label="2.4" caption="A sign-up form and the HTML control behind each part. text accepts any characters, email checks the @ pattern, password hides the characters, radio buttons share one name so only one can be chosen, checkbox allows many, select gives a drop-down list and textarea accepts several lines. The required attribute makes the browser refuse an empty field before the form is sent, but the server must still validate because client checks can be bypassed."
f = Fig(580, 250)
f.box(10, 8, 300, 234, "", fill=SOFT, stroke=SLATE)
rows = [("Name", "input type=text  required"), ("Email", "input type=email"), ("Password", "input type=password  minlength=8"), ("Level", "radio: +2 / Bachelor"), ("Interests", "checkbox: web, AI, data"), ("District", "select > option"), ("Message", "textarea rows=3")]
for i, (l, c) in enumerate(rows):
    y = 18 + i * 30
    f.text(22, y + 11, l, size=10, color=SLATE, bold=True, anchor="start")
    f.box(100, y, 196, 22, "", fill="#ffffff", stroke=SLATE)
    f.arrow([(296, y + 11), (330, y + 11)], color=TEAL)
    f.text(338, y + 11, c, size=9.5, color=TEAL, bold=True, anchor="start")
```

```svgfig label="2.5" caption="The canvas coordinate system, origin at the top-left and y increasing downwards. On a 200 x 100 canvas, ctx.fillRect(20, 20, 80, 40) draws a rectangle whose top-left corner is (20, 20) and whose bottom-right corner is (20 + 80, 20 + 40) = (100, 60). ctx.arc(150, 50, 30, 0, 2*Math.PI) draws a circle with centre (150, 50) and radius 30, so it touches x = 120 to 180 and y = 20 to 80. Canvas pixels cannot be selected after drawing, whereas every SVG shape stays an element that CSS and JavaScript can reach."
f = Fig(580, 200)
f.raw('<rect x="40" y="30" width="400" height="200" fill="none"/>')
f.box(20, 20, 400, 160, "", fill=SOFT, stroke=SLATE)
f.box(60, 60, 160, 80, "", fill=BLUE, stroke=NAVY, sw=2)
f.circle(320, 100, 60, fill=MINT, stroke=TEAL, sw=2)
f.circle(60, 60, 3.5, fill=RED, stroke=RED); f.text(66, 52, "(20, 20)", size=10, color=RED, bold=True, anchor="start")
f.circle(220, 140, 3.5, fill=RED, stroke=RED); f.text(226, 154, "(100, 60)", size=10, color=RED, bold=True, anchor="start")
f.circle(320, 100, 3.5, fill=RED, stroke=RED); f.text(326, 94, "(150, 50)", size=10, color=RED, bold=True, anchor="start")
f.text(140, 106, "fillRect 80 x 40", size=10.5, color=NAVY, bold=True)
f.text(320, 150, "r = 30", size=10.5, color=TEAL, bold=True)
f.arrow([(20, 190), (110, 190)], color=SLATE); f.text(118, 194, "x grows right (2 px per unit shown)", size=9.5, color=SLATE, anchor="start")
f.arrow([(430, 20), (430, 100)], color=SLATE); f.text(436, 60, "y grows down", size=9.5, color=SLATE, anchor="start")
```

### 2.8.1 Eight rules for writing good HTML

1. **Always declare the document type and language.** Start with the doctype line and put lang="en" or lang="ne" on the html element. The doctype keeps the browser out of old quirks mode, and the language helps screen readers pronounce the words. A Nepali news page that sets lang="ne" is read aloud correctly by assistive tools.
2. **Use semantic elements first.** Choose header, nav, main, article, section, aside and footer before reaching for a plain div. These names tell browsers, search engines and screen readers what each part means. A search engine can then show the main article of a Tribhuvan University notice and skip the menu.
3. **Close and nest elements correctly.** Each opening tag needs its closing tag, and inner elements must close before outer ones. A missing end tag silently changes the document tree and breaks the layout. Validating a page with the W3C checker finds these slips before a user does.
4. **Give every image alt text.** The alt attribute describes the picture for people who cannot see it and appears when the file fails to load. Decorative pictures get an empty alt so they are skipped. A product photo on a Daraz-style shop needs a useful description so that a blind customer knows what is sold.
5. **Use tables for data, not for layout.** A table should hold rows and columns of related facts, with th cells and a caption. Layout tables confuse screen readers and cannot adapt to a phone screen. A results table with scope attributes on the headings is read correctly cell by cell.
6. **Label every form control.** Connect each input to its label with for and id, and choose the right type: email, tel, number, date. The right type shows a better keyboard on a phone and lets the browser check the value. A bank sign-up form that labels its fields correctly reduces mistakes and support calls.
7. **Write meaningful links.** Link text such as "Download the 2081 syllabus (PDF)" is clearer than "click here". Add rel="noopener" when opening a new tab to another site, and mark file links with their type. People who move through links with the keyboard hear only the link text, so it must make sense alone.
8. **Keep content, style and behaviour separate.** Put the meaning in HTML, the look in CSS files and the behaviour in script files. This keeps pages small, lets the browser cache the shared files and makes later changes easy. A college site with one shared stylesheet can change its colours on all 200 pages with one edit.

## Formula and fact sheet

- Skeleton: `<!DOCTYPE html>`, `html`, `head` (meta, title, link), `body`.
- Void elements: br, hr, img, input, meta, link.
- Forms: `action`, `method`, `name`, `label for`; radio buttons share a `name`; validation attributes.
- Semantic tags: header, nav, main, section, article, aside, footer.
- Raster: JPEG/PNG/GIF/WebP; vector: SVG; programmatic: canvas.

## Chapter summary

- HTML structures content with nested elements; the head describes the page and the body shows it.
- Text, links, images, lists and tables carry content; forms collect input with typed, validated controls.
- Semantic elements give meaning; video, audio and iframe embed media; SVG and canvas draw graphics.

## Practice

1. Write the minimal valid HTML5 page with title "Results".
2. Write HTML for a table with a header row, two data rows and a cell spanning two columns.
3. Create a registration form with name, email, gender (radio), hobbies (checkboxes), country (select) and a submit button.
4. Differentiate `<b>` and `<strong>`, `div` and `section`.
5. What is the purpose of `alt`, `label for`, and `name`?
6. Differentiate SVG and canvas; raster and vector.
7. Make an image map with two clickable regions.
8. Why must forms be validated on the server as well?

::: note Answers and worked solutions
**1.** `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Results</title></head><body><h1>Results</h1></body></html>`
**2.** See 2.3: `<tr><th>…</th></tr>`, then two `<tr>` rows of `<td>`, one cell with `colspan="2"`.
**3.** See the form in 2.4; hobbies use `type="checkbox"` with the same `name="hobby"`, country uses `<select>` with `<option>`s.
**4.** `<b>` only bolds; `<strong>` says the text is important (screen readers can emphasise). `div` is a meaningless block; `section` is a thematic grouping of content, normally with a heading.
**5.** `alt`: text alternative for images (accessibility and fallback). `label for`: ties a label to an input by `id`, enlarging the click target and helping screen readers. `name`: the key under which the value is sent to the server.
**6.** See the tables in 2.7: raster = pixel grid, vector = mathematical shapes; SVG retains objects, canvas paints pixels.
**7.** `<img usemap="#m"><map name="m"><area shape="rect" coords="0,0,100,50" href="a.html" alt="A"><area shape="circle" coords="150,50,30" href="b.html" alt="B"></map>`
**8.** Client-side checks run in the user's browser and can be disabled or bypassed (the form can be sent with any tool), so the server must treat all input as untrusted.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What are semantic elements in HTML5? Write the structure of a simple page using at least six of them.**

*Introduction.* A semantic element describes the meaning of its content through its name, unlike div and span which describe nothing (section 2.5, Figure 2.2).

1. **header** holds the introduction of a page or section, such as the logo and title.
2. **nav** marks a block of main navigation links, so screen readers can jump to it.
3. **main** holds the unique content of the page; there is only one visible main per page.
4. **article** is a self-contained piece, such as a news story, that would make sense on its own; **section** groups related content under a heading.
5. **aside** holds side content such as related links; **footer** holds copyright and contact details.
6. **Benefits.** Better accessibility, better search-engine understanding, and simpler, more readable code.

```html
<body>
  <header><h1>Kathmandu College</h1></header>
  <nav><a href="/">Home</a> <a href="/notice">Notices</a></nav>
  <main>
    <article><h2>Admission open</h2><p>Forms close on Friday.</p></article>
    <aside><a href="/fees">Fee structure</a></aside>
  </main>
  <footer>&copy; 2082 Kathmandu College</footer>
</body>
```

*Conclusion.* Semantic tags give the same visual result as divs but add machine-readable meaning, so they should be preferred.

**Q2 (5 marks). Write HTML code for a timetable table in which the heading Time covers two columns and the cell Break covers two rows. Explain colspan and rowspan.**

*Introduction.* A table is built row by row with tr, and th and td cells; cells can be merged using two attributes (section 2.3, Figure 2.3).

1. **colspan** makes one cell extend over several columns to its right; the covered columns must not be repeated in that row.
2. **rowspan** makes one cell extend downwards over several rows; the covered position must be left out of the next rows.
3. **Structure.** Use thead for headings and tbody for data, and a caption for the title.
4. **Check.** A row's cells plus the cells carried down by earlier rowspans must equal the number of columns, or the browser misaligns the table.

```html
<table border="1">
  <caption>Weekly timetable</caption>
  <tr><th>Day</th><th colspan="2">Time</th></tr>
  <tr><td>Sunday</td><td>10:00 HTML</td><td rowspan="2">Break</td></tr>
  <tr><td>Monday</td><td>10:00 CSS</td></tr>
  <tr><td>Tuesday</td><td>10:00 JS</td><td>11:00 Lab</td></tr>
</table>
```

*Conclusion.* colspan merges across, rowspan merges downwards; counting cells per row prevents the usual mistakes.

**Q3 (10 marks). Explain HTML forms. Describe the form element, its attributes, the common input controls, and the difference between GET and POST. Write a complete registration form.**

*Introduction.* A form collects data from a visitor and sends it to a server program as name-value pairs. Login, admission, exam-form and payment pages all rely on forms, so they are among the most important parts of HTML (section 2.4, Figure 2.4).

1. **The form element.** It wraps all controls. Its action attribute gives the URL that receives the data, method gives GET or POST, and enctype must be multipart/form-data when files are uploaded.
2. **Text-like inputs.** input has types text, password, email, tel, number, url and search. The type changes the keyboard on a phone and the built-in check.
3. **Choice controls.** Radio buttons with the same name allow one choice; checkboxes allow several; select with option gives a drop-down list; datalist gives suggestions.
4. **Other controls.** textarea for several lines, input type=file for uploads, input type=date, button type=submit and reset, and hidden for values the user does not edit.
5. **Labels and grouping.** label connects text to a control through for and id, and makes the click area bigger; fieldset and legend group related controls.
6. **Validation attributes.** required, minlength, maxlength, min, max and pattern let the browser check values before sending, but a server must repeat every check because the browser can be bypassed.
7. **GET and POST.** GET adds the data to the URL (for searching, bookmarks, small data) and is visible and limited in length. POST places the data in the message body (for logins, uploads, changes) and is not shown in the address bar, though it is not secure without HTTPS.
8. **Name attribute.** Only controls with a name are sent; the name is the key used by the server.

```html
<form action="/register" method="post">
  <label for="n">Name</label>
  <input id="n" name="name" type="text" required>
  <label for="e">Email</label>
  <input id="e" name="email" type="email" required>
  <label for="p">Password</label>
  <input id="p" name="pw" type="password" minlength="8" required>
  <fieldset><legend>Level</legend>
    <label><input type="radio" name="level" value="plus2"> +2</label>
    <label><input type="radio" name="level" value="bachelor"> Bachelor</label>
  </fieldset>
  <select name="district"><option>Kathmandu</option><option>Pokhara</option></select>
  <textarea name="msg" rows="3"></textarea>
  <button type="submit">Register</button>
</form>
```

| Point | GET | POST |
|---|---|---|
| Data location | URL query string | Message body |
| Visible in address bar | Yes | No |
| Length limit | About 2,000 characters in practice | Very large |
| Bookmark / repeat safely | Yes | No (may change data) |
| Typical use | Search, filters | Login, upload, payment |

*Conclusion.* A form is a form element plus labelled controls, each with a name. Correct types and validation improve the user experience, GET suits reading and POST suits changing data, and the server must always validate again.
