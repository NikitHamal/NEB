# Android PDF reader: links, reading mode, draggable Neby AI (status)

Read this before touching `app/.../ui/screens/reader/` (PdfViewerScreen, `pdf/`). Earlier reader work: `ANDROID_UI_CONTINUITY.md` sections 12 and 13. The web reader is separate (`PDF_BOOK_READER_STATUS.md`).

## What was added (session of this file)
- **Own PDF structure reader** (pure Kotlin, no Android classes, so it runs on a plain JVM): `pdf/PdfSyntax.kt` (memory mapped file, xref tables and streams, object streams, Flate/LZW/ASCII filters, predictors, page tree, rebuild for damaged files; encrypted files are skipped), `pdf/PdfStructure.kt` (link annotations, named destinations in `/Dests` and the `/Names` tree, GoTo and URI actions, the outline), `pdf/PdfFonts.kt` (widths, ToUnicode, encodings, bold/italic/mono from names and descriptor flags), `pdf/PdfContent.kt` (content stream walker: text runs with position and size, painted boxes, images, forms), `pdf/PdfReflow.kt` (runs to blocks: headings, paragraphs, lists, code, tables, labels; diagrams, equations drawn as outlines and unmapped text kept as crops).
- **Why:** `PdfRenderer` only draws; link and table-of-contents taps never worked, and its text API exists only on Android 15 or R-extension 13. The own reader works on every device. Verified against `pdftotext`, PyMuPDF links and outline on the NEBians books (30/50/23 links and 170/184/35 outline rows match) and on third party files (Word, Chrome, scanned model papers).
- **Links:** `PdfStructureEngine.links(page)` (lazy, LRU 160), `PageSource.links/cachedLinks/onLink`, `Modifier.linkTaps` on every `PdfPage` (a tap on a link is consumed; a drag, a tap elsewhere and double tap zoom are untouched). Internal links jump with the destination's y (anchored near the top) and show a "Back to page N" pill; web and mail links ask first. Contents sheet (`ContentsSheet`) from the three dots menu, marks the chapter being read.
- **Reading mode** (`pdf/ReadingMode.kt`, menu "Reading mode", remembered per document): single column, lazy per page (`ReflowPage`, LRU 48, read ahead 3 pages), Paper / Sepia / Night, text size 70-220%, line spacing, Serif or Poppins, margins, justified or left, brightness, zen mode (no bars, thin progress line, tap the top or bottom fifth to page, "Leave zen mode" pill), read aloud (TextToSpeech, page by page, `<queries>` entry added to the manifest), time left, page marks that open the original page, text selection, table of contents rows and links inside the text are tappable, tables and code in tonal rounded cards, figures are crops of the real page scaled with the text size (tap = original page). Crops: `PdfDocumentEngine.crop` renders the page just large enough and copies the part out (own LRU 12 MB). Settings: `ReadingSettings` in `ReaderPrefs`.
- **Neby AI button:** `PdfAssistantFab.kt`: drag anywhere (settles against the nearest side, position saved), drag onto the target at the bottom to dismiss, "Undo" pill, and it returns from the three dots menu ("Show Neby AI button") or the Page options and Reading sheets. No shadow on it.
- Top bar: back, title, bookmark, search, three dots (Reading mode, Contents, Page options, Neby AI button).

## Session 2 (compile check and search in reading mode)
- **Toolchain in the sandbox:** JDK 17 + Android SDK 36 from dl.google.com / adoptium into `/tmp`, `local.properties` (`sdk.dir`) and `app/google-services.json` copied from the `.example` (both git-excluded). The 2 GB box cannot finish the full `:app:compileModernDebugKotlin` (codegen runs out of memory at 1.1 GB heap), but the Kotlin front end (all type checking) runs in under two minutes and reports every `e:` line, so it is a real compile check of the new code: the first run found one error (`viewportSize / 3`, fixed), the next runs are clean. CI (`Build Student Release APKs & AAB`) still does the full build.
- **Search in reading mode** (`pdf/ReadingSearch.kt`, `PdfViewerViewModel.readSearch`): scans the reflowed text of every page from the one on screen, wraps round, marks every match in the text (the current one in amber), previous / next, count, progress hairline; the hit scrolls to the upper third. Works on every Android version. On devices without the platform text API the page mode search button opens reading mode with search open (before, it was hidden there).

## Tools
`tools/android/PdfReflowDump.kt` and `PdfReflowSweep.kt` (JVM harnesses). Build and run:
```
kotlinc tools/android/PdfReflowDump.kt app/src/main/java/com/neb/ians/ui/screens/reader/pdf/Pdf{Syntax,Structure,Fonts,Content,Reflow}.kt -d /tmp/out
java -cp /tmp/out:kotlin-stdlib.jar com.neb.ians.ui.screens.reader.pdf.PdfReflowDumpKt book.pdf 3 11 59   # pages to print
```
A sweep over 227 pages takes about 1.5 s, worst page 54 ms, no failures on 6 sample files.

## Not verified on a device (read this)
The Compose side (`ReadingMode.kt`, `PdfAssistantFab.kt`, screen wiring, sheets, chrome) was first written without an Android SDK; session 2 type-checked it with the Kotlin front end (see above) but it has **not run on a device**. Still worth doing: `KEYSTORE_PASSWORD=x KEY_PASSWORD=x ./gradlew :app:compileModernDebugKotlin` and fix whatever the compiler finds, then look at it on a device (reading mode on a book page with a table and a figure, tapping the contents page, dragging the Neby button).

## Known gaps
- Reading mode keeps one column: two column papers interleave. Page mode search marks hits only where the platform text API exists (Android 15 / R-ext 13); elsewhere search runs in reading mode.
- Password protected files have no links or reading mode (the renderer cannot open them either).
- Crops come from `PdfRenderer` pages, so tables made of vector math are shown as pictures, not text.

## Session 3 (reading mode: finger controls, figures, choices, callouts)

Brief: reading mode had no finger controls, weak figure, table and MCQ handling. What the print pipeline produces (`PDF_M3X_STATUS.md`): tonal `.box` cards with a label, typeset maths as small images (inline and display), fact sheets (`.fxs` grids of formulas), derivations (`.dv`), options (`.opt`, badge A to D with text or a maths image), answer keys (`1. (a) .. (b) ..`), rounded tables, `svgfig` diagrams and photo grids, code, contents rows.

- **Pinch:** two fingers anywhere on the text change the size live in 5 % steps (70 to 300 %), with a percentage badge (`pinchTextSize`, `RdSizeBadge` in `ReadingExtras.kt`). One finger still scrolls; a tap toggles the bars. The size is the same `fontScale` as the settings slider (slider range now 70 to 300 %), remembered per the usual prefs.
- **Figures and equations:** tap opens `RdZoomDialog` full screen: pinch to 8x, drag to pan inside the bounds, double tap to 2.5x and back, a crop rendered at 1800 px, and a button to open the original page (the old tap behaviour).
- **Tables:** an Expand control under every table opens the table full screen, scrollable both ways, pinch changes the type size; the in-page table still scrolls sideways for wide ones.
- **Choices:** a run of list items marked (a) a. A) (B) and so on, starting at a with at least two items, becomes tonal option rows with a letter tile; a tap marks your pick (kept while the page is composed), a second tap clears it. Search marks still work in them.
- **Callouts:** paragraphs that start with Answer, Ans, Solution, Hint, Note, Example, Definition, Remember, Tip, Caution, Warning, Key point, Explanation or Formula followed by a colon, full stop or dash are drawn as a tonal card with the label in the accent colour (the print `.box`).
- **Palette:** Paper is neutral white and grey (brand blue accent), no cream tint; Sepia and Night unchanged.
- **Compile:** type checked with the Kotlin front end (see `ANDROID_M3X_STATUS.md`, session 9).

### Still unmapped
- Maths images inside option rows and fact sheets arrive as figure crops after the option badge, so they sit under the option instead of inside it.
- Fact sheet cells (`.fxs`) read as a run of figures or short paragraphs; no grid yet.
- Callout card has no collapse for answers; every answer is visible.
- Two column papers still interleave; scanned pages have no text, so they stay crops.
- Not run on a device.

## Session 4 (reading mode: maths inside choices, folded answers, text size controls, accessibility)

- **Choices with pictures:** `optionRun` (`ReadingExtras.kt`) takes the figures that follow a lettered choice into that choice's row (print sets maths as small images). After the last choice only equations are taken, so a figure that belongs to the next paragraph stays a figure. Rows are `selectable` with the radio role, so TalkBack reads "selected".
- **Callout cards:** `RdCallout` is the print `.box`: icon and uppercase label on a header row, the text under it. Hint and Tip get a bulb, Answer, Solution and Explanation a tick, Caution and Warning a triangle, Formula a function sign, Example a notes mark, the rest an info mark. Search marks survive (the label is cut off the annotated string, not rebuilt).
- **Hide answers until tapped:** Reading sheet toggle (`ReadingSettings.hideAnswers`, pref `rd_hide_ans`). Answer, Solution and Explanation cards start folded; the header is a button with a chevron. A running search opens them.
- **Text size buttons:** the bottom bar has Smaller and Larger text (5 % steps, 70 to 300 %). The page slider announces "Page N of M". The text list exposes "Larger text" and "Smaller text" as TalkBack custom actions.
- **Bug fixed:** the saved text size was clamped to 220 % on load while the slider and pinch allow 300 %.
- Still unmapped: fact sheet grids (`.fxs`) read as figures and short paragraphs, two column papers interleave, scanned pages stay crops.
- Not compiled locally (a 2 GB box cannot hold the Compose compile) and not run on a device; the GitHub Actions build is the check.

## Session 5 (reading mode: choices, formulas inside the text, new Reading sheet)

Brief: reading mode treated question banks badly (choices in a row became a table with an Expand control, formulas set as pictures became text, figure, text, mixed sizes) and the Reading sheet was cut off (no scroll, zen and the switches never showed). CI is the only compile check; nothing was built locally.

- **Choices (`PdfReflow.optionRows`, `runInOptions`):** a line whose cells each start with a letter in order (a 8 / b 12 / c 19 / d 30, also (a) and A.), a lone letter in its own cell, a grid of two rows, and text wrapped under a choice (the "mark" under "d 1") become `ItemBlock`s with markers a to h; `optionRun` then draws them as option rows. Needs a, b, c in order (or two on one line), so a sentence that starts with "a" is untouched. Bold letters inside a paragraph ("a highlighting ... **b** practice testing ... **c**") split it into the question and its choices.
- **Tables:** a table needs at least two rows with two filled cells; a single line with gaps is a paragraph (`Line.spans` now puts a space between cells). Paragraphs no longer end at a line with gaps unless it is a real table or a row of choices.
- **Formulas inside text:** a picture that fits one line (<= 2.6 body sizes) and sits in a text line (`Fig.owner`) is no longer a whole-line crop. It becomes one private use character (`MATH_BASE + n`, `ReflowPage.inlines`) in that line, and the reader draws it as an inline placeholder (`appendInlineContent`) filled with a crop sized at the text's own scale, so it matches the words around it. Two formulas on one line no longer merge into a cluster that swallows the words between them. Crops share page renders (`PdfDocumentEngine.crop` rounds the render width to 256 px steps). Text, search and speech strip the private use characters (`plainText`).
- **Reading sheet (`ReadingSheet.kt`):** the reference bento. Cards: Text size (value in sp, 12 to 54 sp), Line spacing (value is the line height in sp), Margins (three line icons), Typeface ("Ag" Serif and Sans), Alignment (two icons), Brightness (Auto or percent, with an Auto pill), Page colour (Aa tiles, no names), then Zen mode, Hide answers, Neby AI. The sheet scrolls and pads for the navigation bar. `RdSlider` is a thick rail, a strong fill and a round thumb with a haptic tick and slider semantics. Stored values are unchanged (`fontScale` is sp / 18).
- **System bars:** `util/NebSystemBars.kt` (`NebSystemBars(darkIcons)`, `Modifier.nebSafeSides()`). The viewer sets the icon colour from the page it sits on; reading mode paints the status and navigation inset strips in the page colour so text never runs under the icons or the buttons.
- Not run on a device. Look for: option rows after a question on a model paper, a formula inline in a sentence, the sheet on a 360 dp wide phone.
