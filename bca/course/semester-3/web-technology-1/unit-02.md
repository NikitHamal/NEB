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
