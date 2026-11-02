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
