# Web PDF reader: Book mode (3D page turning) and Classic, one shared kit

Read this before touching the resource viewer (`/app/reader/<id>/`). Android has its own viewer and is not part of this.
The first Book mode (commit f208bba) was rebuilt in the second pass; this file replaces the old notes.

## Files
- `static/web/js/pdf-core.js` - `NebPdfKit`, everything both readers share: `sfx` (synthesized WebAudio paper sounds, no files),
  `speech` (read aloud), `store` (resume page, furthest page, reading time, bookmarks; key `neb.book.doc:<src>`), `ink` (pen /
  highlighter strokes as 0..1 coordinates; key `neb.pdf.ink:<src>`), `text` (lazy text index, search, highlight rectangles; only 20
  pages keep full geometry), `thumbs` (one render queue, newest request first, LRU 90, `peek`), `panels` (Pages / Contents / Search /
  Bookmarks), `scrubber` (page preview on hover/drag), settings sheet builder, help, toast, ink bar. ES5, no template literals.
- `static/web/js/pdf-book.js` - `NebBook.mount(src, title, {page, onClassic})` the 3D book.
- `static/web/js/pdf-reader.js` - `NebPdf.open(src)` (one download per file) and the classic reader
  `NebPdf.mount(src, title, {page, onBook})`.
- `static/web/js/resource-viewer.js` - picks the style (`localStorage neb.reader.mode`, default `book`), hands the page across when
  switching, destroys whichever reader is open when the stage is closed (timers, voice, sound, canvases), falls back to the browser PDF.
- CSS (bundle with `python3 tools/css/bundle.py`): `m3x/app-pdfkit.css` (shared `nx-*` chrome), `m3x/app-book.css` (`bk-*` stage),
  `m3x/app-classic.css` (`cl-*`). Load order: pdf-core, pdf-reader, pdf-book, resource-viewer (`resource_detail.html`).

## Book reader
- Hardcover (cover colour from the subject `--sc`, or Navy / Forest / Crimson / Ink), spine hinge, boards, page stacks that grow and
  shrink with progress, contact shade that follows the visible pages. Cover alone, then spreads; one page on phones.
- Leaf: 1 / 9 / 18 nested strips (Flat / Soft / Rich), pooled (built once per size, repainted per turn, never re-created), each face shaded
  and given a moving sheen by its own angle, cast shade on the page below. Tone is baked into the leaf with `ctx.filter` (CSS fallback on Safari).
- The book tilts toward the pointer (setting), drag a corner / swipe (velocity decides), hover edge peek, click halves, keys, wheel.
- Zoom 100-400%: buttons, Ctrl+wheel, pinch, double tap / double click, drag to pan.
- Annotate (A): pen, highlighter, eraser, 5-6 colours, 3 sizes, undo, clear page. Strokes are composited into the turning leaf.
- Read aloud (R): speaks the spread, turns the page, continues; keeps up if you turn manually.
- Search with page highlights, contents, thumbnails, bookmarks with notes, scrubber with page preview, "Back" toast after long jumps,
  auto-turn, controls fade after 4.5 s without movement (H toggles), `?` lists the keys.
- Sounds: paper turn (speed-matched), landing thud, flurry for long jumps, cover open, end-of-book bump, bookmark chime, UI ticks,
  pen and eraser. On by default, Volume + switch in settings, `M` mutes. Shared with the classic reader (`neb.pdf.sfx`).
- Memory: page canvases live in a byte-budgeted cache (`K.budget`: 28 MB per GB of `deviceMemory`, 56-190 MB), farthest pages freed
  first, stale sizes dropped, per-canvas cap 9 MP, leaf at most 1100 px wide, `page.cleanup()` after each render, `doc.cleanup()` when idle,
  blurry thumbnail stand-in while a page renders, prefetch shrinks when zoomed.
- Reduced motion: leaves jump, no tilt, no 3D tweening.

## Classic reader
Continuous scroll, Two pages, One page (snap) views; Fit width / Fit page / 25-400% presets menu, +/- steps, pinch, Ctrl+wheel, double
click, rotate, drag to pan, auto-scroll (3 speeds), progress bar, same tones / brightness / warmth, same panels, search highlights, ink,
bookmarks, sounds, resume. Zoom re-renders in place (old canvas stays until the sharp one is ready); pages release off screen; canvas
cap 12 MP. "Switch to book reader" lives in settings and in the stage bar.

## Rules kept
No box shadows (page shading and the contact shade are neutral gradients), no emojis, no blue/purple gradients, no profile-picture
rings, buttons never lose their radius on hover, tonal role pairs, Poppins. Icons must exist in `fonts/app/material-symbols-outlined.txt`
(a subset: `last_page`, `view_agenda`, `bookmark_added`, `volume_off`, `ink_highlighter`, `view_column` are NOT in it).

## Gotchas
- Never set `root.dataset.panel` (delegated `closest('[data-panel]')` would match the root).
- rjsmin minifies JS: no template literals (a test checks the reader files).
- Local checks: `export DEBUG=True DB_ENGINE=sqlite; python3 manage.py test web.test_viewer`. Visual checks: serve `web/static` with
  `python3 -m http.server`, a small harness page loading fonts.css, material3.css, app.css, m3x.css, m3x-app.css and the 3 scripts,
  a reportlab PDF, Playwright (needs `sudo apt-get install libnss3 libatk1.0-0 ...` in a fresh sandbox).

## Not done
Text selection/copy (view only on purpose), sticky notes, Android parity, RTL page order.
