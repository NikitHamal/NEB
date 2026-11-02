---
subject: Web Technology I
grade: BCA Semester 3
unit: 7
title: Website Page Layout and Design Issues
area: BCA 203 · Web Technology I · Unit 7
---

A site can be technically correct and still fail: people cannot find things, the text is unreadable, it is slow on a phone, or it is unusable with a screen reader. This unit covers the **design decisions** around layout, usability, accessibility and publishing.

::: key What this unit gives you
- Planning: audience, site map, wireframes; layout types and common page patterns.
- Navigation, typography, colour and contrast (with a computed WCAG check).
- Responsiveness, accessibility, performance, SEO, browser compatibility.
- Security basics and a publishing checklist.
:::

## 7.1 Planning a website

1. **Purpose and audience:** who visits and what do they need to do (apply, read results, buy)?
2. **Content inventory and site map:** a tree of pages; most information within three clicks.
3. **Wireframes:** simple grey-box sketches of each page's layout before any colours or code.
4. **Visual design:** grid, type, colour, imagery; a style guide keeps pages consistent.
5. **Build, test, publish, maintain.**

## 7.2 Layout types and page patterns

| Layout | Description | Pros / cons |
|---|---|---|
| **Fixed** | set width in px (e.g. 960) | predictable; poor on phones; wasted space on wide screens |
| **Fluid (liquid)** | widths in `%` | fills any screen; line lengths may become too long |
| **Responsive** | fluid grid + media queries (Unit 4) | one site for all devices; more design effort |
| **Adaptive** | several fixed layouts chosen by device width | tuned designs; more to maintain |

Common page anatomy: **header** (logo, nav), **hero** or intro, **main content** (one to three columns), **sidebar**, **footer** (contacts, legal, sitemap). Patterns: F-shaped reading (people scan the top and left), the **visual hierarchy** (size, weight, colour and whitespace mark what is important), **grid alignment**, generous **whitespace**, and **above the fold** content that answers "what is this site?" without scrolling.

## 7.3 Navigation

- Keep the main menu **consistent** on every page; limit it to about 5–7 items.
- Show **where you are** (highlight the current item, **breadcrumbs**: Home › Courses › Web).
- Links must **look like links** and say what they lead to ("Download syllabus", not "click here").
- Provide **search** for large sites, a **footer sitemap**, and a helpful **404 page**.
- On phones use a compact menu (hamburger) with large touch targets (at least about 44 × 44 px).

## 7.4 Typography, colour and contrast

- Body text 16 px or larger, line height about 1.5, line length 45–75 characters; limit to two font families; use real headings for hierarchy.
- Colour: a palette of a primary, an accent and neutrals; never use colour as the only signal (add icons or text for errors).
- **WCAG contrast:** relative luminance of an sRGB colour is L = 0.2126 R + 0.7152 G + 0.0722 B with each channel linearised (c/255 ≤ 0.03928 → c/12.92, else ((c/255 + 0.055)/1.055)^2.4). **Contrast ratio = (L₁ + 0.05)/(L₂ + 0.05)** with L₁ the lighter. AA requires **4.5 : 1** for normal text and 3 : 1 for large text; AAA requires 7 : 1.

```js
const lin = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
const lum = hex => { const n = parseInt(hex.slice(1), 16); return 0.2126 * lin(n >> 16) + 0.7152 * lin((n >> 8) & 255) + 0.0722 * lin(n & 255); };
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
for (const [fg, bg] of [["#000000", "#ffffff"], ["#1F4E8C", "#ffffff"], ["#777777", "#ffffff"], ["#999999", "#ffffff"], ["#ffffff", "#ffa500"]]) {
  const r = ratio(fg, bg);
  console.log(fg, "on", bg, r.toFixed(2) + ":1", r >= 7 ? "AAA" : r >= 4.5 ? "AA" : r >= 3 ? "large text only" : "FAIL");
}
```
```output
#000000 on #ffffff 21.00:1 AAA
#1F4E8C on #ffffff 8.31:1 AAA
#777777 on #ffffff 4.48:1 large text only
#999999 on #ffffff 2.85:1 FAIL
#ffffff on #ffa500 1.97:1 FAIL
```

## 7.5 Accessibility

About 15% of people have a disability; accessibility also helps people on slow connections, in sunlight or with a broken mouse. The **WCAG** principles are **POUR**: Perceivable, Operable, Understandable, Robust. Practices:

- Meaningful `alt` text; captions/transcripts for media; semantic HTML (Unit 2) and a logical heading order.
- Everything usable by **keyboard**; visible focus outline; a "skip to content" link.
- Sufficient contrast; text resizable to 200% without breaking; do not rely on colour alone.
- Labels on every form control; clear error messages; ARIA attributes only when native HTML cannot express the role.
- Test with a screen reader (NVDA, TalkBack) and automated checkers (Lighthouse, axe).

## 7.6 Performance

Slower pages lose visitors (a delay of a few seconds loses many mobile users). Measures:

- **Optimise images:** right size, modern formats (WebP/AVIF), `loading="lazy"`.
- **Minify** CSS and JavaScript and combine files; **compress** responses (gzip/Brotli).
- **Cache** static files (`Cache-Control`) and use a **CDN** (copies near the user).
- Put CSS in the head and load scripts with `defer`; avoid heavy libraries and render-blocking resources.
- Reduce HTTP requests; use fast hosting; measure with Lighthouse and the Network tab.

::: example Worked example: why image size matters
A page has 10 photos of 2 MB each = 20 MB. On a 4 Mbps (0.5 MB/s) connection that is 40 s of download. Resizing to display size and using WebP at about 100 KB each gives 1 MB: **2 s**, a 20× improvement from one change.
:::

## 7.7 SEO and browser compatibility

**Search engine optimisation:** unique `<title>` (about 60 characters) and `<meta name="description">`; one `<h1>`; semantic headings; descriptive URLs and link text; `alt` on images; a `sitemap.xml` and `robots.txt`; fast, mobile-friendly, HTTPS pages; useful original content and incoming links. **Compatibility:** test in several browsers and devices; use standards, feature detection and **progressive enhancement** (basic content works everywhere, extras are added where supported); use a CSS reset or normalisation; check support tables such as caniuse.com before using new features.

## 7.8 Security and publishing

- Use **HTTPS** everywhere. **Validate and escape** all user input; never insert untrusted text with `innerHTML` (**cross-site scripting, XSS**); use parameterised queries (**SQL injection**); set `HttpOnly`/`Secure` cookies; keep software updated; hash passwords; never expose secrets in client code.
- **Publishing checklist:** run an HTML/CSS validator; test links, forms and every page on phone and desktop; check contrast and keyboard use; set title, description and favicon; compress images; add analytics and a privacy notice; register the domain, upload to hosting, enable HTTPS; back up; plan maintenance.

## Formula and fact sheet

- Layout types: fixed, fluid, responsive, adaptive.
- Contrast ratio = (L₁ + 0.05)/(L₂ + 0.05); AA 4.5:1 (3:1 large), AAA 7:1.
- POUR: Perceivable, Operable, Understandable, Robust.
- Speed: optimise images, minify, compress, cache, CDN, `defer`.
- SEO: title, description, h1, alt, sitemap, mobile, HTTPS.

## Chapter summary

- Good sites start with purpose, audience, site map and wireframes.
- Layout, navigation, typography and colour must support reading and finding things; contrast can be measured.
- Accessibility, performance, SEO and compatibility are design requirements, not extras.
- Security basics and a final checklist precede publishing.

## Practice

1. Differentiate fixed, fluid and responsive layouts.
2. List five navigation guidelines.
3. Compute whether #777777 text on white meets WCAG AA (use the program's idea) and state the result.
4. Explain the four WCAG principles.
5. List six ways to speed up a web page.
6. What is progressive enhancement?
7. List five SEO practices.
8. Name two common web security attacks and the defence for each.

::: note Answers and worked solutions
**1.** Fixed: pixel width. Fluid: percentage widths. Responsive: fluid grid plus media queries that change the layout by screen width.
**2.** Consistent menu; limited items; show current location and breadcrumbs; descriptive link text; search/sitemap/404; large touch targets.
**3.** The program above gives 4.48:1 for #777777 on white, **just below 4.5**, so it fails AA for normal text (passes for large text); #999999 gives about 2.85:1 and fails.
**4.** Perceivable (see or hear it), Operable (use it with keyboard, enough time), Understandable (clear, predictable), Robust (works with assistive technology and many browsers).
**5.** Compress and resize images; minify CSS/JS; enable gzip/Brotli; cache static files; use a CDN; defer scripts; reduce requests.
**6.** Build a basic version that works everywhere, then add enhancements for browsers that support them.
**7.** Unique title and description, one h1, alt text, sitemap and robots.txt, fast mobile-friendly HTTPS pages, quality content.
**8.** XSS: escape output and avoid `innerHTML` with untrusted text. SQL injection: parameterised queries.
:::
