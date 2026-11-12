---
subject: Web Technology I
grade: BCA Semester 3
unit: 4
title: CSS (Cascading Style Sheets)
area: BCA 203 · Web Technology I · Unit 4
---

**CSS** separates *presentation* from *structure*: HTML says what content is, CSS says how it looks. One stylesheet can restyle a whole site.

::: key What this unit gives you
- Three ways to add CSS, the rule syntax, selectors, specificity and the cascade.
- The box model, units, colours, text and fonts.
- Display, positioning, Flexbox and Grid layout.
- Pseudo-classes, transitions and media queries for responsive pages.
:::

## 4.1 Syntax and ways to add CSS

A rule is `selector { property: value; … }`.

```html
<link rel="stylesheet" href="style.css">          <!-- external: best, cached, shared by pages -->
<style> h1 { color: navy; } </style>              <!-- internal: one page -->
<p style="color: red;">Inline: highest priority, hard to maintain</p>
```

```css
/* style.css */
body  { font-family: "Segoe UI", Arial, sans-serif; margin: 0; line-height: 1.6; }
h1, h2 { color: #1F4E8C; }
.note { background: #fff7e6; border-left: 4px solid orange; padding: 8px 12px; }
```

**Style classes** (`.note`) can be reused on many elements and several can be combined (`class="note big"`); an `id` selector (`#header`) targets one element.

## 4.2 Selectors, specificity and the cascade

| Selector | Matches |
|---|---|
| `p` | all `<p>` (type selector) |
| `.card` / `#main` | class / id |
| `div p` | `<p>` anywhere inside a `<div>` (descendant) |
| `ul > li` | direct children only |
| `h1 + p` / `h1 ~ p` | the next sibling / all following siblings |
| `a[target="_blank"]` | attribute selector |
| `a:hover`, `li:first-child`, `li:nth-child(2n)`, `input:focus` | pseudo-classes (state or position) |
| `p::first-line`, `.x::before` | pseudo-elements |
| `*` | everything |

When several rules apply, the **cascade** decides: (1) importance (`!important` wins); (2) **specificity**, counted as (inline, ids, classes/attributes/pseudo-classes, elements): `p` = 0,0,0,1; `.note` = 0,0,1,0; `#main .note p` = 0,1,1,1; inline style = 1,0,0,0; (3) **source order**: later wins on a tie. Some properties are **inherited** by children (`color`, `font-*`, `line-height`); others (`border`, `margin`) are not.

## 4.3 The box model, units, colours

Every element is a rectangle: **content → padding → border → margin** (inside out). By default `width` sets only the content, so total width = width + padding + border; `box-sizing: border-box` makes `width` include padding and border, which is almost always what you want.

```css
* { box-sizing: border-box; }
.card { width: 300px; padding: 16px; border: 2px solid #ccc; margin: 20px auto; border-radius: 8px; }
```

With `content-box`, that card would occupy 300 + 2 × 16 + 2 × 2 = **336 px**; with `border-box` it occupies 300 px. `margin: 20px auto` centres a block horizontally. Vertical margins of adjacent blocks **collapse** to the larger one.

| Units | Meaning |
|---|---|
| `px` | CSS pixel (absolute) |
| `em` | relative to the element's font size; `rem` relative to the root font size |
| `%` | relative to the parent |
| `vw`, `vh` | 1% of viewport width / height |
| `fr` | fraction of free space in Grid |

Colours: names (`tomato`), hex `#1F4E8C`, `rgb(31 78 140)`, `rgba(0,0,0,.5)` (alpha = transparency), `hsl(214 64% 33%)`.

## 4.4 Text, fonts, lists, backgrounds

`font-family`, `font-size`, `font-weight`, `font-style`, `color`, `text-align`, `text-decoration`, `text-transform`, `letter-spacing`, `line-height`; `list-style-type`; `background-color`, `background-image`, `background-size: cover`. Web fonts load with `@font-face` or a `<link>` to a font service. Always give fallback fonts and a generic family (`serif`, `sans-serif`, `monospace`).

## 4.5 Display and positioning

| `display` | Behaviour |
|---|---|
| `block` | starts a new line, fills the width (`div`, `p`, `h1`) |
| `inline` | flows in a line, ignores width/height (`span`, `a`) |
| `inline-block` | flows in a line but accepts width and height |
| `none` | removed from layout (`visibility: hidden` keeps the space) |
| `flex`, `grid` | layout containers |

| `position` | Behaviour |
|---|---|
| `static` | normal flow (default) |
| `relative` | shifted from its normal place with `top/left`; its space is kept; becomes the reference for absolute children |
| `absolute` | removed from flow, placed relative to the nearest positioned ancestor |
| `fixed` | fixed to the viewport (sticky headers, chat buttons) |
| `sticky` | scrolls until a threshold, then sticks |

`z-index` orders overlapping positioned elements; `float` is the old way of wrapping text around images (clear it with `clear: both`).

## 4.6 Flexbox and Grid

**Flexbox** arranges items in one dimension:

```css
.nav { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
.nav .grow { flex: 1; }
```

`justify-content` aligns along the main axis, `align-items` across it; `flex-direction: row | column`.

**Grid** arranges in two dimensions:

```css
.gallery { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.gallery .wide { grid-column: span 2; }
```

Use Flexbox for a row of items (a menu), Grid for whole-page or card layouts.

## 4.7 Pseudo-classes, transitions, responsive design

```css
.btn { background: #1F4E8C; color: white; padding: 8px 16px; border-radius: 6px; transition: background .3s, transform .2s; }
.btn:hover { background: #163a69; transform: translateY(-2px); }
.btn:focus-visible { outline: 3px solid orange; }
@keyframes pulse { from { opacity: 1; } to { opacity: .4; } }
.badge { animation: pulse 1s infinite alternate; }

/* Responsive: mobile-first with a media query */
.layout { display: grid; grid-template-columns: 1fr; gap: 16px; }
@media (min-width: 768px) { .layout { grid-template-columns: 1fr 3fr; } }
img { max-width: 100%; height: auto; }
```

**Responsive design** uses a viewport meta tag (Unit 2), fluid widths (`%`, `fr`, `max-width`), flexible images and **media queries** at breakpoints (about 600, 768, 1024 px). **Mobile-first** means writing the small-screen layout first and adding `min-width` queries.

::: example Worked example: specificity
HTML `<p id="x" class="note">`. Rules: `p { color: red }` (0,0,0,1), `.note { color: green }` (0,0,1,0), `#x { color: blue }` (0,1,0,0), all with equal importance. The `#x` rule wins: **blue**. Add inline `style="color: black"` (1,0,0,0): **black**. `!important` on the `.note` rule would override all of them except another `!important`.
:::

## 4.8 Seeing CSS: the box, the cascade and the layout

CSS is a visual language, so its rules are best learned from pictures with numbers on them. The plate shows the person who proposed CSS and a timeline of its versions; the figures show the box model with real sizes, the winner of a specificity contest, flexbox and grid layouts with their arithmetic and the breakpoints of a responsive page.

```photogrid label="4.1" cols="2" ratio="1.25" caption="(a) Hakon Wium Lie, who proposed Cascading Style Sheets in October 1994 while working with Tim Berners-Lee at CERN. His proposal had the word cascading in it from the start: several style sheets (author, reader, browser) are combined by rules. (b) The main versions. Each CSS3 module (flexbox, grid, animations, media queries) is specified and released separately instead of as one large version number."
@ photo id="bca203/hakon" cap="Hakon Wium Lie"
fit 1.25
focus 0.5 0.62
@ svg cap="CSS timeline"
f = Fig(330, 264)
ev = [("1994", "Proposal at CERN"), ("1996", "CSS1: fonts, colour, box"), ("1998", "CSS2: positioning"), ("2011", "CSS 2.1 final"), ("2012", "Media queries, modules"), ("2017", "Grid in all browsers")]
for i, (y, t) in enumerate(ev):
    yy = 10 + i * 42
    f.box(6, yy, 60, 28, y, fill=BLUE, stroke=NAVY, size=12.5, bold=True)
    f.text(76, yy + 14, t, size=13, color=SLATE, bold=True, anchor="start")
    if i < 5: f.line(36, yy + 28, 36, yy + 42, color=SLATE)
```

```svgfig label="4.1" caption="The box model with numbers. For div { width: 200px; height: 100px; padding: 20px; border: 5px solid; margin: 30px; } the content box is 200 x 100. With the default box-sizing: content-box the border box is 200 + 2 x 20 + 2 x 5 = 250 px wide and the space the element occupies, including margins, is 250 + 2 x 30 = 310 px wide and 100 + 40 + 10 + 60 = 210 px high. With box-sizing: border-box the width of 200 px already includes padding and border, so the content shrinks to 200 - 40 - 10 = 150 px. Almost every modern stylesheet starts with * { box-sizing: border-box }."
f = Fig(580, 232)
f.box(10, 10, 330, 212, "", fill=SAND, stroke=AMBER, dash=True)
f.box(40, 40, 270, 152, "", fill="#e2e8f0", stroke=SLATE, sw=4)
f.box(46, 46, 258, 140, "", fill=MINT, stroke=TEAL)
f.box(86, 86, 178, 60, "content\n200 x 100", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.text(16, 24, "margin 30", size=10, color=AMBER, bold=True, anchor="start")
f.text(46, 58, "border 5 / padding 20", size=10, color=TEAL, bold=True, anchor="start")
f.text(360, 40, "content-box (default)", size=11, color=NAVY, bold=True, anchor="start")
f.text(360, 60, "border box   = 250 x 150", size=10.5, color=SLATE, anchor="start")
f.text(360, 78, "with margins = 310 x 210", size=10.5, color=SLATE, anchor="start")
f.text(360, 112, "border-box (modern)", size=11, color=NAVY, bold=True, anchor="start")
f.text(360, 132, "width 200 includes padding + border", size=10.5, color=SLATE, anchor="start")
f.text(360, 150, "content = 200 - 40 - 10 = 150", size=10.5, color=SLATE, anchor="start")
f.text(360, 186, "Margins of neighbouring blocks may collapse:", size=10, color=RED, bold=True, anchor="start")
f.text(360, 202, "30 px under 20 px gives 30 px, not 50 px.", size=10, color=RED, bold=True, anchor="start")
```

```svgfig label="4.2" caption="Specificity decides the winner. Four rules target the same paragraph <p class='note'> inside <div id='intro'>. Specificity is written (ids, classes, elements): p = (0,0,1); .note = (0,1,0); p.note = (0,1,1); #intro p = (1,0,1). Compare left to right, not by adding: one id beats any number of classes. So #intro p wins and the text is red. An inline style attribute beats all four, and !important beats inline; if two rules tie, the later one in the file wins."
f = Fig(580, 190)
rules = [("p { color: blue }", "(0,0,1)", 1, NAVY), (".note { color: green }", "(0,1,0)", 10, TEAL), ("p.note { color: orange }", "(0,1,1)", 11, AMBER), ("#intro p { color: red }", "(1,0,1)", 101, RED)]
for i, (r, s, v, c) in enumerate(rules):
    y = 14 + i * 36
    f.text(10, y + 12, r, size=10.5, color=SLATE, bold=True, anchor="start")
    f.text(200, y + 12, s, size=10.5, color=c, bold=True, anchor="start")
    f.box(270 + 0, y, 20 + v * 2.6 if v < 100 else 280, 24, "winner" if v == 101 else "", fill=ROSE if v == 101 else SOFT, stroke=c, color=c, size=10.5, bold=True, r=3)
f.text(10, 176, "Order of strength:  browser default < element < class < id < inline style < !important", size=10, color=NAVY, bold=True, anchor="start")
```

```svgfig label="4.3" caption="How justify-content places three 60 px items in a 300 px flex container. Free space = 300 - 3 x 60 = 120 px. flex-start leaves all 120 px at the end; center puts 60 px on each side; space-between puts 120 / 2 = 60 px in each of the two gaps; space-around gives each item 120 / 3 = 40 px of space split equally, so 20 px on both sides of an item and 40 px between neighbours; space-evenly makes all four gaps 120 / 4 = 30 px. align-items does the same job on the cross axis."
f = Fig(580, 232)
modes = [("flex-start", [0, 60, 120]), ("center", [60, 120, 180]), ("space-between", [0, 120, 240]), ("space-around", [20, 120, 220]), ("space-evenly", [30, 120, 210])]
for i, (m, xs) in enumerate(modes):
    y = 10 + i * 44
    f.text(10, y + 17, m, size=10.5, color=NAVY, bold=True, anchor="start")
    f.box(150, y, 300, 34, "", fill=SOFT, stroke=SLATE)
    for x in xs:
        f.box(150 + x, y + 3, 60, 28, "", fill=BLUE, stroke=NAVY)
    f.text(462, y + 17, "gaps " + ["0 / 120 end", "60 | 60", "60 | 60", "20 | 40 | 20", "30 each"][i], size=9.5, color=TEAL, bold=True, anchor="start")
```

```svgfig label="4.4" caption="A page layout in CSS Grid. grid-template-columns: 200px 1fr 1fr in a 600 px container with no gap gives the two flexible columns 200 px each ((600 - 200) / 2). With column-gap: 20px the free space is 600 - 200 - 2 x 20 = 360 px, so each 1fr column becomes 180 px. grid-template-areas names the regions: the header spans all three columns, the sidebar takes the first column and main spans the other two, and the footer spans all three. Flexbox arranges items in one direction; Grid arranges rows and columns together."
f = Fig(580, 220)
f.box(10, 10, 560, 34, "header   (spans 3 columns)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(10, 52, 186, 110, "sidebar\n200 px", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(206, 52, 364, 110, "main   (spans 2 columns)\n2 x 1fr", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(10, 170, 560, 34, "footer   (spans 3 columns)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.text(290, 216, "container 600 px, column-gap 20 px: 200 + 180 + 180 + 2 x 20 = 600", size=10, color=SLATE, bold=True)
```

```svgfig label="4.5" caption="The position property. static is the normal flow. relative moves the element from where it would have been (top: 20px; left: 30px shifts it 20 px down and 30 px right) but still keeps its old space. absolute removes the element from the flow and places it relative to the nearest ancestor that is positioned (not static), here the card; fixed places it relative to the browser window and it stays when scrolling, as on a sticky header or a chat button; sticky behaves like relative until a scroll threshold and then like fixed."
f = Fig(580, 200)
f.box(10, 10, 270, 180, "", fill=SOFT, stroke=SLATE)
f.text(18, 26, "card  (position: relative)", size=10, color=SLATE, bold=True, anchor="start")
f.box(24, 40, 90, 34, "static A", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(24, 84, 90, 34, "", fill="#ffffff", stroke=SLATE, dash=True)
f.box(54, 104, 90, 34, "relative B", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(69, 101), (54, 104)], color=TEAL)
f.box(180, 146, 90, 34, "absolute C", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.text(180, 138, "bottom:10px; right:10px", size=9, color=AMBER, bold=True, anchor="start")
f.box(310, 10, 260, 180, "", fill=SOFT, stroke=SLATE)
f.text(320, 26, "browser window", size=10, color=SLATE, bold=True, anchor="start")
f.box(320, 36, 240, 26, "fixed header  (top: 0)", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(480, 150, 70, 28, "fixed chat", fill=ROSE, stroke=RED, size=10, bold=True)
f.text(320, 110, "scrolled content passes under", size=10, color=SLATE, anchor="start")
f.text(320, 128, "the fixed parts and they stay put.", size=10, color=SLATE, anchor="start")
```

```svgfig label="4.6" caption="Mobile-first responsive design with two breakpoints. The base CSS is for phones (one column). @media (min-width: 600px) switches to two columns and @media (min-width: 992px) to three. Each rule only adds to the smaller layout. The viewport meta tag, width=device-width, is required, otherwise the phone pretends to be 980 px wide and shows a tiny desktop page."
f = Fig(580, 170)
def card(x, w, cols, title):
    f.box(x, 10, w, 120, "", fill=SOFT, stroke=SLATE)
    cw = (w - 8 - (cols - 1) * 4) / cols
    for i in range(cols):
        f.box(x + 4 + i * (cw + 4), 18, cw, 104, "", fill=BLUE, stroke=NAVY)
    f.text(x + w / 2, 148, title, size=10.5, color=NAVY, bold=True)
card(10, 100, 1, "under 600 px: 1 column")
card(150, 190, 2, "600 px and up: 2 columns")
card(380, 190, 3, "992 px and up: 3 columns")
f.text(290, 166, "@media (min-width: 600px)  and  @media (min-width: 992px)", size=9.5, color=TEAL, bold=True)
```

### 4.8.1 Eight rules for maintainable CSS

1. **Reset the box model first.** Start the stylesheet with box-sizing: border-box for all elements. Then a width of 200 px really means 200 px, and padding does not secretly make columns wider. This single line prevents most layout surprises in a college website with many forms.
2. **Keep specificity low and flat.** Prefer single class selectors such as .card-title over long chains or ids. Low specificity makes later overrides easy, while high specificity leads to !important wars. A team that follows this can change one button style without breaking ten pages.
3. **Use relative units.** Write font sizes in rem, widths in percentages or fr and spacing in em or rem. The page then respects the user's browser font size and adapts to different screens. A reader with weak eyesight who enlarges the text in a Nepali news portal still gets a usable layout.
4. **Name by purpose, not by looks.** A class called .notice-warning stays correct when the colour changes, but .red-text does not. Meaningful names make the HTML readable and the CSS easier to search. Conventions such as BEM (block__element--modifier) help large teams.
5. **Build mobile-first.** Write the single-column phone layout as the base and add min-width media queries for bigger screens. Most Nepali users open sites on phones, and this method sends them the lightest code. It also forces the designer to decide what is truly important.
6. **Choose the right layout tool.** Use flexbox for one-dimensional rows or columns such as a navigation bar, and grid for two-dimensional page layouts. Avoid floats and tables for layout. A results page with a header, sidebar and table is a natural grid job.
7. **Use variables and a small palette.** Define colours, spacing and fonts once as custom properties such as --brand: #1e3a8a. Changing one line then re-themes the entire site. A college that changes its logo colour can update all pages in minutes.
8. **Check contrast, focus and print.** Text needs enough contrast against its background (at least 4.5 to 1 for normal text), links need a visible focus outline, and a print stylesheet can hide menus. These details make the site usable by everyone, including people with colour-vision problems or in bright sunlight.

```photogrid label="4.2" cols="2" ratio="1.2" caption="Counting pixels in the box model. (a) A framed picture with a mat shows the layers of every CSS box: the picture is the content, the mat is the padding, the frame is the border and the gap to the next frame on the wall is the margin. (b) A box declared as width: 300px with padding 20px, border 5px and margin 10px is not 300 pixels wide in the default content-box model: the layers are added outside the width, so it occupies 370px of the row. With box-sizing: border-box the 300px already includes padding and border, the content shrinks to 250px, and the box occupies 320px with its margin. In a 960px row that is the difference between 2 boxes and 3 boxes, which is why most style sheets begin with the border-box rule. All sums were checked in code."
@ photo id="bcawt/mat" cap="A picture-frame mat: padding, border, margin"
fit 1.2
focus 0.5 0.5
@ svg cap="Box model: content-box vs border-box"
w, pad, bor, mar = 300, 20, 5, 10
cb_total = w + 2 * (pad + bor + mar)
bb_content = w - 2 * (pad + bor)
bb_total = w + 2 * mar
box_cb = 960 // cb_total
box_bb = 960 // bb_total
assert (cb_total, bb_content, bb_total, box_cb, box_bb) == (370, 250, 320, 2, 3)
facts = dict(cb=cb_total, bbc=bb_content, bb=bb_total, ncb=box_cb, nbb=box_bb)
f = Fig(300, 252)
f.text(150, 12, "width: 300px; padding 20; border 5; margin 10", size=10.5, color=NAVY, bold=True)
f.box(50, 22, 200, 124, "", fill=SAND, stroke=SLATE, r=2, sw=1)
f.box(64, 36, 172, 96, "", fill="#fcd34d", stroke=AMBER, r=2, sw=1)
f.box(78, 50, 144, 68, "", fill=BLUE, stroke=NAVY, r=0, sw=1)
f.box(92, 64, 116, 40, "content", fill=MINT, stroke=TEAL, size=10.5, bold=True, r=2, sw=1)
f.text(150, 29, "margin 10", size=10.5, color=SLATE, bold=True, vmid=True)
f.text(150, 43, "border 5", size=10.5, color=NAVY, bold=True, vmid=True)
f.text(150, 57, "padding 20", size=10.5, color=NAVY, bold=True, vmid=True)
f.text(150, 162, "A 960px-wide row, scale 0.29", size=10.5, color=NAVY, bold=True)
sc = 280 / 960
for r, (lab, wd, n, col) in enumerate([("content-box: %dpx each, %d fit" % (cb_total, box_cb), cb_total, box_cb, "#fecaca"), ("border-box: %dpx each, %d fit" % (bb_total, box_bb), bb_total, box_bb, "#bbf7d0")]):
    y = 168 + r * 38
    for k in range(n):
        f.box(10 + k * wd * sc, y + 14, wd * sc - 2, 16, "", fill=col, stroke=SLATE, r=2, sw=1)
    f.text(10, y + 8, lab, size=10.5, color=NAVY, anchor="start", bold=True)
f.text(150, 246, "so: * { box-sizing: border-box; }", size=10.5, color=TEAL, bold=True)
```

## Formula and fact sheet

- Rule: `selector { property: value; }`. Specificity (inline, id, class, element); later rule wins ties.
- Box: content + padding + border + margin; `box-sizing: border-box` includes padding and border in `width`.
- `em` relative to element, `rem` to root, `%` to parent, `vw/vh` to viewport.
- Position: static, relative, absolute, fixed, sticky. Flexbox 1-D, Grid 2-D.
- Media query: `@media (min-width: 768px) { … }`.

## Chapter summary

- CSS styles HTML through selectors; the cascade resolves conflicts by importance, specificity and order.
- The box model determines element size and spacing; units can be absolute or relative.
- `display`, `position`, Flexbox and Grid build layouts; transitions and media queries add polish and responsiveness.

## Practice

1. Differentiate inline, internal and external CSS.
2. Write selectors for: all links inside a nav; every second table row; the first paragraph after each h2.
3. Compute the specificity of `ul#menu li.active a:hover`.
4. A box has `width: 200px; padding: 10px; border: 5px solid; margin: 15px`. Find its rendered width under both box-sizing values.
5. Write CSS to centre a 600 px wide block and make it full width below 600 px.
6. Differentiate `position: relative`, `absolute` and `fixed`.
7. Write a Flexbox rule to space three items evenly in a row.
8. Explain mobile-first design.

::: note Answers and worked solutions
**1.** Inline: `style` attribute on one element; internal: `<style>` in the head for one page; external: a `.css` file linked from many pages (best).
**2.** `nav a { }`; `tr:nth-child(2n) { }`; `h2 + p { }`.
**3.** `#menu` 1 id; `.active` 1 class and `:hover` 1 pseudo-class (2 in the class column); `ul`, `li`, `a` 3 elements: **(0, 1, 2, 3)**.
**4.** content-box: 200 + 2·10 + 2·5 = **230 px** (margin adds outside: 260 px of space). border-box: **200 px**.
**5.** `.page { max-width: 600px; margin: 0 auto; }` — a `max-width` shrinks automatically on narrower screens.
**6.** Relative: shifted from its own place, space kept. Absolute: out of flow, positioned against the nearest positioned ancestor. Fixed: out of flow, positioned against the viewport and stays during scroll.
**7.** `.row { display: flex; justify-content: space-evenly; }`
**8.** Design and write CSS for the smallest screen first, then use `min-width` media queries to add layout for larger screens.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the CSS box model. For an element with width 200 px, padding 20 px, border 5 px and margin 30 px, calculate the total horizontal space it occupies in both box-sizing modes.**

*Introduction.* Every element is drawn as a rectangular box made of four layers, from the inside out: content, padding, border and margin (section 4.3, Figure 4.1).

1. **Content** holds the text or image; its size is set by width and height.
2. **Padding** is transparent space between the content and the border and takes the element's background.
3. **Border** is the line around the padding, with its own width, style and colour.
4. **Margin** is the transparent space outside the border that separates the element from its neighbours; vertical margins of adjacent blocks collapse to the larger one.
5. **Calculation, content-box (default).** Total = 200 + (2 x 20) + (2 x 5) + (2 x 30) = 200 + 40 + 10 + 60 = **310 px**.
6. **Calculation, border-box.** The width of 200 px already includes padding and border, so the content is 200 - 40 - 10 = 150 px, and the total including margins is 200 + 60 = **260 px**.

| Layer | Size | Counted in content-box width? |
|---|---|---|
| Content | 200 px | Yes, it is the width |
| Padding | 20 px each side | No, it is added |
| Border | 5 px each side | No, it is added |
| Margin | 30 px each side | No, it is outside |

*Conclusion.* The same CSS gives 310 px or 260 px depending on box-sizing, which is why modern sheets set border-box for every element.

**Q2 (5 marks). What is the cascade? Explain how the browser resolves conflicting CSS rules using origin, specificity and order, with an example.**

*Introduction.* More than one rule can set the same property on one element, so CSS defines an ordered way to choose a single winner (section 4.2, Figure 4.2).

1. **Origin and importance.** Rules come from the browser default, the user and the author. Author rules beat browser defaults, and a declaration marked !important beats normal ones.
2. **Specificity.** For equal origin, the more specific selector wins. It is a triple (ids, classes, elements) compared left to right: p is (0,0,1), .note is (0,1,0), #intro p is (1,0,1).
3. **Inline style.** A style attribute is stronger than any selector in a stylesheet.
4. **Order.** If specificity ties, the rule written later in the document wins.
5. **Inheritance.** Properties like color and font-family pass from parent to child when no rule applies; box properties such as margin do not.

```css
p { color: blue; }
.note { color: green; }
#intro p { color: red; }
```

For `<div id="intro"><p class="note">Hello</p></div>` the three rules apply, and the text is **red** because (1,0,1) beats (0,1,0) and (0,0,1).

*Conclusion.* The cascade is a fixed ranking of origin, specificity and order, so the same page always renders the same way.

**Q3 (10 marks). Explain how a responsive page layout is built with Flexbox, Grid and media queries. Write the CSS for a page with a header, a sidebar, a main area and a footer that becomes a single column on phones.**

*Introduction.* Visitors use screens from 360 px phones to wide monitors, so a page must adapt its layout instead of being fixed at one width. Modern CSS gives three tools: flexbox for one-dimensional arrangement, grid for two-dimensional layout, and media queries for changing the rules at chosen widths (sections 4.6 and 4.7, Figures 4.3, 4.4 and 4.6).

1. **Viewport tag.** The page needs meta name="viewport" content="width=device-width, initial-scale=1"; otherwise phones show a shrunken desktop page.
2. **Fluid units.** Use percentages, fr, rem and max-width instead of fixed pixel widths, and max-width: 100% for images.
3. **Flexbox.** display: flex on a container arranges children in a row; justify-content distributes free space on the main axis (Figure 4.3), align-items on the cross axis, and flex-wrap lets items move to the next line. It suits navigation bars and card rows.
4. **Grid.** display: grid with grid-template-columns and grid-template-areas defines rows and columns together; 200px 1fr 1fr gives a fixed sidebar and two equal flexible columns (Figure 4.4).
5. **Media queries.** @media (min-width: 768px) { ... } applies rules only above a width, so the base CSS serves phones (mobile-first).
6. **Breakpoints.** Choose breakpoints where the content breaks, typically near 600 px and 992 px, not at the sizes of particular devices.
7. **Testing.** Resize the browser and use the device toolbar of the developer tools to check each width.
8. **Accessibility.** Keep text readable without zooming and keep touch targets about 44 px high.

```css
* { box-sizing: border-box; }
.page { display: grid; gap: 16px;
        grid-template-areas: "head" "side" "main" "foot"; }
header { grid-area: head; } aside { grid-area: side; }
main { grid-area: main; }   footer { grid-area: foot; }
@media (min-width: 768px) {
  .page { grid-template-columns: 200px 1fr;
          grid-template-areas: "head head" "side main" "foot foot"; }
}
```

| Tool | Dimension | Best for |
|---|---|---|
| Flexbox | One (row or column) | Menus, toolbars, card rows |
| Grid | Two (rows and columns) | Whole-page layout |
| Media query | Conditions on the screen | Changing layout at breakpoints |

*Conclusion.* A responsive layout starts with a fluid, single-column base and adds grid or flex rules inside media queries; this serves phones first and scales up, with the same HTML for all devices.
