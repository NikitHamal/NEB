# Web PDF reader: Book mode (3D page turning) and Classic switch

Read this before touching the resource viewer (`/app/reader/<id>/`). Android has its own viewer and is not part of this.

## What exists
- `static/web/js/pdf-book.js` (`NebBook.mount(src, title, {page, onClassic})`): the book reader. Pages drawn by PDF.js through the shared
  `NebPdf.open(src)` (one download per file, in `pdf-reader.js`).
- `static/web/css/m3x/app-book.css` (bundled into `m3x-app.css`: run `python3 tools/css/bundle.py` after any edit).
- `resource-viewer.js`: picks the style (`localStorage neb.reader.mode`, default `book`), hands the page across when you switch,
  tears the book down when the reader is closed (timers, keys), falls back to the browser viewer if PDF.js fails.
- `_viewer_stage.html`: the Book / Classic switch in the stage bar (PDFs only). The old scrolling reader is untouched (`NebPdf.mount`,
  now also returns `goto(n)` and `page()`).

## Book reader behaviour
- Hardcover (colour from the subject `--sc`), closed cover that opens and centres, spreads on wide screens, single page on phones
  (Settings: Auto / One page / Two pages). Page stacks grow and shrink with progress.
- The turning leaf is 14 nested strips, each turned a little further, so the page bends; shade follows the angle; a cast shade falls on the page
  below only if one is there. Hover a page edge to peek, drag a corner or swipe to turn (velocity decides), click a half, arrow keys,
  PageUp/Down, Space, Home/End, horizontal wheel. Jumps up to 6 spreads flurry-turn, longer ones glide.
- Panels: Pages (lazy thumbnails), Contents (PDF outline), Search (whole book, snippets, yellow highlights on the page using the
  line's own font metrics), Bookmarks (notes, read progress, minutes read). Dock: scrubber with bookmark ticks, go-to-page, zoom 100-300%
  (re-rendered sharp, drag to pan, double click), auto-turn. Settings: paper / sepia / night tone, brightness, layout, turn speed,
  auto-turn interval, page curl, page sound (WebAudio, off by default). `?` lists the keys.
- Resume: last page, furthest page, reading time, bookmarks live in `localStorage neb.book.doc:<src>`; preferences in `neb.book.prefs`.
- Reduced motion: leaves jump, no 3D tweening.

## Rules kept
No shadows, no emojis, no gradient except neutral black page shading, buttons never lose their radius on hover, tonal role pairs,
Poppins. Icons must exist in `fonts/app/material-symbols-outlined.woff2` (a subset: `last_page`, `view_agenda`, `bookmark_added`
and `crop_portrait` are NOT in it; check with fontTools before using a new name).

## Gotchas
- Never set `root.dataset.panel`: delegated `closest('[data-panel]')` matches the root itself.
- rjsmin minifies JS: no template literals.
- Local test: `export DEBUG=True DB_ENGINE=sqlite; python3 manage.py test web.test_viewer`; visual checks used Playwright against a runserver
  with a reportlab PDF (cover, outline, 37 pages).

## Not done
Text selection/copy (view only on purpose), annotation drawing, Android parity.
