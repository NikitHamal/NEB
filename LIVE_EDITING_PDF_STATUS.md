# Live editing (web + Android) and PDF viewer speed: status

Read this first when touching composers, the Notes editor or the Android PDF viewer.
Nothing under `app/` is built locally: the check is the GitHub Actions Android build.

## Rule
Nobody types Markdown, LaTeX or KaTeX. Storage stays Markdown (old posts, the server and both renderers keep working);
the editors draw the result live and write the markers themselves.

## Web: `static/web/js/neb-live.js` + `css/neb-live.css` (loaded in `base.html`)
- `NebLive.attach(textarea)` hides the textarea and puts a formatted, editable surface in its place. `value`, `focus`, `setRangeText`,
  key events and `input` events still work on the textarea, so existing composer code reads Markdown without changes.
  `NebLive.bind(div)` does the same for an editable element that already exists (create-post `#cp-body`, with its image chips).
- Used by: home composer (`#homePostContent`), forum composer (`forum-composer.js` `mount`, covers replies, thread replies, post edit),
  create-post page, `reply.html`, and every `_comment_composer.html` box without a toolbar (add `data-live` to any textarea; a
  MutationObserver attaches to boxes built later).
- Floating bar over a selection (bold, italic, underline, strike, code, link, heading, quote, formula). Ctrl+K link, Ctrl+E code, Ctrl+Shift+X strike,
  Ctrl+Shift+M formula. Pasting Markdown or HTML becomes formatted text. Preview toggles are hidden on live surfaces.
- Formulas: dialog takes calculator-style input (`x^2 + 3/4`, `sqrt(a/b)`, `pi`, `<=`, `sum_(i=1)^n i`), converts it with `asciiToTex`
  and draws it with KaTeX; stored as `$...$` / `$$...$$`. Double-click a drawn formula to edit it.
- Markdown round trip was checked with jsdom (bold, lists, nested lists, quotes, code fences, tables, links, escapes, formulas).
- @mentions work on the surface (`composer-editor.js` uses `NebLive.textBefore/replaceBefore/caretRect`).

## Android composers: `ui/components/LiveMarkdown.kt`
- The text a composer holds is still Markdown. `LiveMarkdown.transform` hides the markers with a real `OffsetMapping` (inline markers stick
  left so typing at the end of a bold word stays bold; line-start markers stick right) and draws bold, italic, strike, code, links, headings,
  quotes, bullets, to-dos and dividers.
- `InlineImageField` (post body, reply screen) composes it with the image-chip transformation; `rawRanges` map chips back to raw offsets.
  Enter continues lists (`NoteFormatting.continueList`). `CommentComposerBar` draws live too.
- `MarkdownToolbar` now toggles (selection wraps/unwraps, caret in a word formats the word, empty caret starts the style with a zero-width
  marker pair), lights up where the caret is, adds a link dialog and a maths-symbol sheet (plain Unicode: x², √, π, ±, ≤, Greek).
  `LiveMarkdown.cleaned()` strips the zero-width helper if a caller wants a pristine string.
- Not done: comment bars have no format toolbar yet (live drawing only).

## Android Notes: blocks (`ui/screens/notes/NoteBlocks.kt`, `NoteBlockEditor.kt`, `NoteBlockMedia.kt`)
- Room v4 (`MIGRATION_3_4`): `notes.doc` = blocks as JSON; `notes.body` = Markdown export (list cards, search, share, read-aloud unchanged).
  Notes without `doc` open from `body` (`NoteDoc.fromMarkdown`).
- Blocks: text, heading 1-3, to-do, bullets, numbers, quote, callout, code, divider, table, photo, audio, drawing.
  Enter splits, Backspace at the start steps back (hardware key; menu has "Turn into" and Delete), "/" on an empty line opens the block list,
  per-block menu (turn into, move, duplicate, delete), format bar follows the focused block.
- Photos are copied into `filesDir/notes/<id>/` scaled to 2400 px; drag the corner handle or pick Small/Medium/Large/Full to resize.
  Audio: record (AAC m4a) or add a file; play with a seek bar. Table: type in cells, add or remove rows and columns. Drawing: pen colours and
  widths, stroke eraser, undo, clear, height. Duplicating a note copies its media.
- Dictation lands at the end of the block that last had the caret. Undo/redo snapshots whole block lists.
- Not done: drag-and-drop reordering (menu moves one step), image captions, nested lists, Backspace on soft keyboards at an empty field
  (some IMEs send no key event; use the block menu).

## Android PDF viewer (`ui/screens/reader/pdf/PdfDocumentEngine.kt`)
- Opening read every page of the document up front (1010 pages meant 1010 `openPage` calls before anything showed). Now it reads page 1 only,
  lays every page out with that shape, and `scanShapes` corrects the rest in the background (6 pages per lock, starting at the resume page,
  releasing the renderer between batches, emitting a new list only when a shape differs). Rendering also records the page's real shape.
- A 320 px preview of a page is rendered first and replaced by the sharp render, so fast scrolling shows content instead of blank paper.
- Cache budget raised to a fifth of the heap (24 to 112 MB). Render quality, buckets and zoom behaviour are unchanged.
