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
The Compose side (`ReadingMode.kt`, `PdfAssistantFab.kt`, screen wiring, sheets, chrome) was written without an Android SDK in the sandbox: it was reviewed by hand but **not compiled**. First step next session: `KEYSTORE_PASSWORD=x KEY_PASSWORD=x ./gradlew :app:compileModernDebugKotlin` and fix whatever the compiler finds, then look at it on a device (reading mode on a book page with a table and a figure, tapping the contents page, dragging the Neby button).

## Known gaps
- Reading mode keeps one column: two column papers interleave. Search is not available inside reading mode (page mode search is unchanged and still needs the platform text API).
- Password protected files have no links or reading mode (the renderer cannot open them either).
- Crops come from `PdfRenderer` pages, so tables made of vector math are shown as pictures, not text.
