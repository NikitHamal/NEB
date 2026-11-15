# Android status: splash, polls, post detail, badges, FAB, glass

One file for this batch. Read it first, extend it, do not start another. Nothing is built locally; the check is the GitHub Actions Android run.

## Done

| # | What | Where |
| --- | --- | --- |
| 1 | **Splash**: the blue container wash is gone. Page colour only (white light, navy dark, by the app theme), N settles on a spring, letters rise, stack lifts. `values-night/colors.xml` matches the system window and the API 31 splash. Rule written in `docs/M3X_DESIGN_SYSTEM.md` and `AGENTS.md`. | `ui/screens/auth/SplashScreen.kt`, `res/values-night` |
| 2 | **Blog posts appear again**: the web moved to `.bcard` / `.bhero` and the app only parsed `.news-card`. List and detail parsers read both, nested article divs no longer cut the body, source link read from `nd-source-btn`. | `data/repository/NewsRepository.kt` |
| 3 | **Polls**: white 24dp card with a hairline, icon tile, ends chip, option fields whose stroke turns primary, springy check marks, result bars drawn in the draw phase (no per-frame layout), quiz tones from the web good/bad pair, new feed preview with up to three options. | `NebPollCard.kt`, `NebPollParts.kt` |
| 4 | **Post detail**: See more / See less at the right edge, 12sp, 36dp target, chevron flips; title 19sp, body 14.5sp; composer margins 8dp narrower; comments clamp at five lines with the same control. | `Markdown.kt`, `ForumPostDetailScreen.kt`, `CommentComposerBar.kt` |
| 5 | **Badges**: no disc. The nine Material Symbols the web draws are vector drawables (`ic_sym_*`), chosen by the API icon name, in the web ink colours. | `NebDesign.kt`, `res/drawable/ic_sym_*` |
| 6 | **Marked chips** sit on the author line (name, badge, time, chips), web colours, 24dp, pop in. **Solved** chip above the title with an arrow; tap scrolls to the accepted reply and flashes it. Accepted card: good tint and 4dp line. Marked replies rank first in the app and on the web (`views_forum.py`). | `ReplyKinds.kt`, `CommentCard.kt`, `PostDetailViewModel.kt` |
| 7 | **Create menu**: label then glyph on the right, hugging white pills, frosted scrim, the page blurs behind it on Android 12+. | `NebFabMenu.kt`, `Navigation.kt` |
| 8 | **Glass nav**: blur set in the draw pass, 26dp, clearer tint; skipped on low-end devices and below Android 12 (solid tint), which also stops the page being recorded twice. | `LiquidGlassNav.kt` |

| 9 | **Poll builder (create post and comment poll)**: fields are white with one 1.5dp stroke that animates to primary on focus (same as the poll card), correct-answer mark uses the web good tone, 44dp touch targets, finite radii. | `CreatePostComposer.kt` (`PostInput`), `CreatePostPoll.kt` |

## CI fix
First push failed to compile: duplicate `Icons` import in `ReplyKinds.kt`, missing `getValue` import in `NebPollParts.kt`, missing `KeyboardArrowDown` import in `Markdown.kt`. Fixed in `1ee2ba6`; the Android release build (APK + AAB) is green.

## Next
- On-device visual pass (poll card, Solved scroll offset, glass blur strength).


CI for the poll builder change: first push failed (missing `setValue` import in `PostInput`), fixed in `5484c06`; the Android release build is green.


---

# Session 2: sign-in stall, no-code composers, glass, notes empty state

Same file, same rule: nothing is built locally, the check is the GitHub Actions Android run.

## Done

| # | What | Where |
| --- | --- | --- |
| 10 | **Sign-in stall (Xiaomi 11i "NEBians isn't responding")**. Picked up from `59d3742` (Keystore token write moved to IO, Play update bind deferred). Added: the one deliberate main-thread block left, `currentUserNameFlow`'s `runBlocking` read while MainActivity is injected, is capped at 120 ms (the flow corrects the name when the read lands). Remaining suspects are listed under Next. | `AuthRepository.kt` |
| 11 | **Composers keep valid Markdown on every edit**. The leak came from the field holding raw Markdown while only a strict parser hid it: a space typed before a closing `**` (`**a **`), Enter inside bold, Backspace over a hidden marker, or a letter right after a closer each made the pair invalid for one frame or for good. `LiveReconcile.apply(old, new)` now runs on every edit (posts, comments, note blocks) and repairs the pair before it is stored: spaces move outside the markers, a trailing space leaves the style armed for the next letter, Enter closes and reopens the style per line, Backspace deletes the character you can see (never half a marker), an emptied run stays armed, a line prefix (bullet, number, quote, heading, to-do) goes in one Backspace, a destroyed marker removes its orphan. Plain typing returns on a cheap check. | `LiveReconcile.kt`, `LiveRebuild.kt`, `LiveMarkdown.kt` |
| 12 | **Formatting buttons**: a selection over several lines is styled per line (a pair never spans lines, so it used to show markers); `***` renders bold italic; stars and tildes work inside a word (`he**ll**o`) like the web; tapping Bold twice with nothing typed takes it back; armed styles no longer leave a stray character behind once the caret leaves. | `LiveMarkdown.kt` |
| 13 | **Typing cost**: one parse per text shared by field, toolbar and reconcile (4-entry cache, `structure()`), regexes compiled once. Before: every toolbar button re-parsed the whole text on each key. | `LiveMarkdown.kt` |
| 14 | **Comment field** holds a `TextFieldValue` (the `String` overload dropped the caret and the keyboard's composing word on each external change). | `CommentComposerBar.kt` |
| 15 | **Notes empty state is static**: the floating paper stack no longer animates. | `NotesScreen.kt` |
| 16 | **Glass**: blur plus a saturation lift on the blurred backdrop (`glassEffect`, API 31+), a rim lit along the top edge, a soft sheen. The page is not recorded into the glass layer on screens that show no glass (`GlassBackdrop.active`, set from `showBottomBar`). Low-end and pre-12 devices keep the solid tint. | `LiquidGlassNav.kt`, `Navigation.kt` |

Version 1.7.5 (29).

## Rules for composers (do not break)
- Every editable Markdown field passes `onValueChange` through `LiveReconcile.apply(old, new)`. Toolbar actions (`toggleInline`, `toggleLine`, ...) write directly.
- Pending style = `mark + U+200B + mark`; only `LiveReconcile` and `toggleInline` create or remove it.
- A pair never spans a line. Markers are `*`, `**`, `***`, `~~`, `` ` ``, `_`.

## Next
- On-device pass on a Xiaomi/MIUI phone: first sign-in with the process killed while the browser is open (MIUI kills background apps; the callback then cold-starts the app).
- Baseline Profile for the splash to first screen path.

CI: `7b3d9a8`, `0b0c977` and `b8a5254` (run merging) all green on the first push; Android release build (APK + AAB) compiles.


---

# Session 3: composers rebuilt, pictures in text, viewer, glass

Same file, same rule: nothing is built locally, the check is the GitHub Actions Android run. Picks up session 2 item 11 to 14 (the `LiveReconcile` approach) and replaces it for posts, replies and notes.

## Why session 2 was not enough
The field still held raw Markdown and a visual transformation hid the markers. Every fix had to rewrite the text the keyboard owns, so the keyboard resynced (a flash of `**`, a style reverting on space or backspace). A hidden marker can never be made safe while the text and the formatting are the same string.

## Done

| # | What | Where |
| --- | --- | --- |
| 17 | **One editing engine, no markers anywhere in the field.** `RichDoc` = plain text + one style mask per character (bold, italic, strike, code) + link id per character + one kind per line (heading, quote, bullet, number, to-do, code block, rule). `RichState.onChange` diffs the keyboard's text and moves the formatting with the characters (typing inside or at the end of bold continues it, a replaced word keeps the style of the first replaced letter, autocorrect keeps style). The text in the field always equals what the keyboard holds, so nothing resyncs. Toolbar buttons only change masks or line kinds; with nothing selected they arm the next letters (`armed`). Markdown is made only by `RichMarkdown.write` (spaces move outside markers, pairs never cross a line, `\*` `\_` escapes for typed marks, formulas `$..$` untouched) and read by `RichMarkdown.parse`. | `RichDoc.kt`, `RichState.kt`, `RichMarkdown.kt` |
| 18 | **Word-like line behaviour**: Enter on an empty list line ends the list; Backspace at the start of a list, quote or heading line removes the mark first (also at the very start of the text, through `onPreviewKeyEvent`); typing `- `, `1. `, `# `, `> `, `[] ` at a line start makes the line a list, heading, quote or to-do. | `RichState.onChange`, `RichTextField` |
| 19 | **`RichTextField`** replaces the three fields (post, reply, note block). Drawing: `RichVisual` builds the styled text, list marks drawn in front of lines, offset mapping. `rememberRichState(markdown, caret) { md, caret -> }` keeps view-model-held Markdown in step; an echo of what was just sent (250 ms) never reloads the field. | `RichTextField.kt`, `RichVisual.kt`, `CommentComposerBar.kt` |
| 20 | **Pictures in the text**: one object-replacement character per picture in the text (Backspace takes the whole picture, the caret cannot sit inside), 38dp rounded thumbnails drawn over a blank slot of the same width, so they wrap with the words. Several pictures can be picked at once. Tap opens the viewer on all pictures of the text, long press drags one elsewhere, the small cross removes it. | `RichTextField.kt`, `CreatePostScreen.kt` |
| 21 | **Nothing uploads on pick.** A picked picture is a `[[img:uKEY]]` slot plus a local `Uri` in `RichState.uris`. `CreatePostViewModel.submitPost` uploads each one (`ContentImageRepository.upload`), swaps the key for the server id, then creates or updates the post. Failure keeps the draft and says so. Preview shows pending pictures from the phone. | `CreatePostViewModel.kt`, `CreatePostComposer.kt` |
| 22 | **Notes blocks** use the same engine in block mode (no line marks, they belong to the block type; a code block is raw text). Enter splits through the engine so each new block carries its own valid Markdown. | `NoteBlockEditor.kt` (`BlockFieldRegistry.stateOf`) |
| 23 | **Notes list**: previews are drawn from the Markdown (`LiveMarkdown.transform(..).styled`), so `*italic*`, `_x_`, `[[img]]`, escapes and rules never show as characters. | `NotesScreen.kt` |
| 24 | **Create post chrome**: the identity picker ends in a real down arrow (the name shrinks first, so the arrow is never pushed out and an ellipsis shown in its place); Write / Preview is one control with a single sliding thumb and no press or ripple on either icon. | `NebIdentityPicker.kt`, `CreatePostChrome.kt` |
| 25 | **Fullscreen picture viewer**: swipe between all pictures (a post's inline and attached pictures, a reply's inline pictures), no arrows, counter at the top, tap hides controls, pinch and double tap zoom to the touched point, one finger at normal size belongs to the pager, drag down closes. Neighbour pages are composed ahead. `inlineGallery(clicked, content, extra)` builds the list from any card. | `ZoomableImageDialog.kt`, `ZoomableImagePage.kt`, `ForumPostDetailScreen.kt` |
| 26 | **Glass** goes back to the version before 1.7.5 (`LiquidGlassNav.kt`, one line in `Navigation.kt`). | `LiquidGlassNav.kt` |

## Rules for composers (replace session 2 rules)
- A composer never holds Markdown. It holds a `RichState`. Anything that needs Markdown asks `state.lastMarkdown` (kept current on every edit) and anything handing Markdown in goes through `setMarkdown` or `adopt`.
- Formatting changes go through `RichState` (`toggleInline`, `toggleLine`, `insertLink`, `insertImage`...). Never write a marker into the text.
- `LiveMarkdown` / `LiveReconcile` remain only for drawing stored Markdown (`transform`) in places that show, not edit, text.

## Not done / next
- Web composer parity (the web editor has its own pipeline in `backend_python/web`); the viewer and no-upload-on-pick rules are Android only for now.
- On-device pass: chip drag with a long press, caret placement after Enter on an empty list line, Gboard autocorrect on a bold word.
- Comment bar has no inline pictures yet (pictures there are attachments).

CI session 3: `cd67248` failed on one missing icon import (`KeyboardArrowDown`, fixed); `f9eb094` showed the same single error; `f0bccd4` is green, the Android release build (modern APK and AAB) compiles. Nothing was run on a device.

---

# Session 4: notes overhaul, picture tools, drop caret, appearance

Same file, same rule: nothing is built locally, the check is the GitHub Actions Android run. Picks up session 3 (`RichState` engine, pictures in text, notes blocks on the engine).

## Done

| # | What | Where |
| --- | --- | --- |
| 27 | **No handle, no 3-dot on blocks.** The per-block drag handle and menu are gone (the long menu was also clipped off screen). Block actions (turn into, indent, move, duplicate, delete, clear done to-dos) live in one **Block** sheet opened from the last button of the format bar. | `NoteBlockEditor.kt` (`BlockSheet`) |
| 28 | **Media blocks**: tap (or press and hold) selects; tools open right under the block, nothing floats over it. Press and drag moves it (haptic on pick up, others slide away). | `MediaFrame` |
| 29 | **Pictures in notes**: pick several at once from the bar (Photos button), each becomes a picture block. Selected picture: pinch with two fingers to size (one finger still scrolls the page), corner handle, S / M / L / Full, align left / centre / right, **text beside** (the next text block is written next to the picture, in one row), crop (original, square, wide, tall), replace, caption. Decoded at 1280 px max. New block fields `align`, `wrap`, `caption`, `ratio` (JSON `a`, `w`, `q`, `ra`; old notes load unchanged). | `NoteBlockMedia.kt`, `NoteBlocks.kt` |
| 30 | **Toolbar can be hidden**: chevron at the start of the bar folds it to a single Aa button plus the mic; tap to bring it back (state survives rotation). | `NoteEditorScreen.kt` |
| 31 | **To-dos**: progress bar with "n of m" and Clear (removes ticked items) above the blocks; Clear completed in the Block sheet. | `NoteEditorScreen.kt` (`TodoProgress`), `NoteEditorViewModel.clearDone` |
| 32 | **Appearance sheet** replaces three menu rows: 9 one-tap themes (colour + cover + icon), 18 note colours (11 new, light and dark pairs), Add / Change icon and cover. | `NoteTones.kt`, `NotePage.kt`, `NotesScreen.kt` (`ToneSwatches`) |
| 33 | **Covers 8 to 24** (flat tonal, 8 new palettes, dots / stripes / grid / wave patterns drawn flat, no gradients) and **icons 30 to 60**. Sheets scroll. | `NotePage.kt` |
| 34 | **Post / reply composer**: while a picture is dragged a caret bar shows where it will land (follows the finger, picture lifts 12 percent). Pictures are centred inside their own text line and never above it, so the line the keyboard scrolls into view holds the whole picture (the top clip with the keyboard open). | `RichTextField.kt` |
| 35 | **Web**: same drop bar for dragged pictures in the post editor, edge auto-scroll while dragging, caret and nearby picture kept inside the visible viewport when the keyboard opens (`visualViewport`). | `backend_python/web/static/web/js/inline-media.js` |

## Not done / next
- Web composers still write Markdown into a textarea (forum-composer.js). A contenteditable WYSIWYG like the Android `RichState` is the next big item; the drop bar and viewport fix above are the only web changes.
- Touch drag of inline pictures on the web relies on the browser's own long-press drag.
- Photo (gallery) covers and page backgrounds need a path column in the notes table.
- On-device pass: pinch sizing inside the scrolling page, text beside picture while typing, hide / show toolbar with keyboard open.

CI session 4: `e3650bb` is green on the first push; the Android release build (APK and AAB) compiles. Nothing was run on a device.

---

# Session 5: sheet insets, photo covers, more looks, web editor speed

Same file, same rule: nothing is built locally, the check is the GitHub Actions Android run. Picks up session 4 (block sheet, picture tools, appearance sheet) and the web editor `neb-live.js`, which already is a contenteditable WYSIWYG (the session 4 note saying the web composer still writes Markdown into a textarea was out of date: `forum-composer.js` / `home.js` talk to `NebLive`).

## Done

| # | What | Where |
| --- | --- | --- |
| 36 | **Sheets in notes no longer touch the screen sides.** The title was inset and the content was not (icon grid, New note tiles, Block, Appearance, Colour, voice setup). One wrapper, `NoteSheet`, insets the content to the title's edge. | `NotePage.kt` (`NoteSheet`), callers in `NotesScreen`, `NoteEditorScreen`, `NoteBlockEditor`, `VoiceModelsScreen` |
| 37 | **Cover from the gallery.** Cover sheet has a From gallery row; the picture is scaled to 1600 px, saved in the note's own folder (`notes/<id>/cover_<time>.jpg`), decoded off the main thread, shown on the page and on list cards (half size). Built-in cover index is -1 while a photo is set. Room version 6, column `coverPhoto` (migration 5 to 6). | `NoteCoverPhoto.kt`, `NoteEditorViewModel.setCoverPhoto`, `NoteEntity`, `DatabaseMigrations` |
| 38 | **More looks**: covers 24 to 40 (six new palettes), tones 18 to 22 (Rose, Teal, Coral, Dusk added), themes 9 to 15, icons 60 to 70. | `NotePage.kt`, `NoteTones.kt` |
| 39 | **Post composer: formatting row can be hidden** (chevron at its start, Aa brings it back, state survives rotation). | `CreatePostChrome.kt` (`ComposerFormatRow`) |
| 40 | **Web editor speed and glitches.** The Markdown copy and the textarea `input` event now run once per frame instead of once per key (`flush()` runs first on blur and whenever `value` is read). Writing back the text the editor already holds no longer rebuilds the document (that rebuild moved the caret and flashed the formatting). | `neb-live.js` |
| 41 | **Web: no code to start a list.** `- `, `* `, `1. `, `# `, `## `, `> ` at the start of a plain line become a bullet list, numbered list, heading or quote. | `neb-live.js` (`autoformat`) |
| 42 | **Web: formatting row folds** in the post dialog (chevron button, choice kept in localStorage). | `_home_composer.html`, `pages/home.js`, `m3x-app.css` |

## Not done / next
- Page background pictures (cover only for now), to-do due dates.
- On-device pass: photo cover on a list card, pinch sizing inside the scrolling note, Autoformat after Enter on the web.

---

# Session 6: underline, paper, to-do dates, touch drag on the web

Same file, same rule: nothing is built locally, the check is the GitHub Actions Android run. Picks up sessions 3 to 5 (`RichState`, notes blocks, `neb-live.js`). Checked first: block handle and 3-dot are already gone on Android (session 4), the Block sheet, sheet insets, formatting-row fold and the web drop bar are in; none of that was redone.

## Done

| # | What | Where |
| --- | --- | --- |
| 43 | **Underline** in post, reply and note composers. New style bit `Fmt.UNDERLINE`, stored as `<u>..</u>` (the web sanitiser already allows `u`). Parsed and written by `RichMarkdown`, drawn by `RichVisual`, rendered in `Markdown.kt` and `NoteMarkdownView.kt`. Link key in `RichVisual` moved from 16 to 256 so the new bit does not collide. Ctrl or Cmd + B / I / U on a hardware keyboard. | `RichDoc.kt`, `RichMarkdown.kt`, `RichVisual.kt`, `RichTextField.kt`, `PostExtras.kt`, `NoteBlockEditor.kt`, `ic_neb_underline.xml` |
| 44 | **Web: underline was lost on save** (the editor wrote nothing for `<u>`). It now writes `<u>..</u>`, and reads it back. | `neb-live.js` |
| 45 | **Web: list, heading and quote shortcuts on phone keyboards.** Gboard sends composition input, not plain text, so `- ` and `1. ` never fired. Now checked for both. | `neb-live.js` (`autoformat`) |
| 46 | **Web: touch drag of inline pictures.** Press and hold 360 ms (haptic), the picture follows the finger, the same drop bar shows where it lands, edge auto-scroll, release drops it. Native drag is cancelled while this runs; the mouse path is unchanged. | `inline-media.js` |
| 47 | **Note paper**: Plain, Lines, Grid, Dots, flat tint of the page ink, drawn once under the scrolling blocks. Room version 7, column `paper` (migration 6 to 7). Picked in Appearance. | `NotePaper.kt`, `NoteEntity`, `DatabaseMigrations`, `NoteEditorViewModel.setPaper` |
| 48 | **To-do due dates**: block field `due` (JSON `d`, whole UTC days, no time zone drift). Block sheet: Today, Tomorrow, Pick date, No date. The row shows a tonal chip (Today, Tomorrow, weekday, date), red once late and still open; tap it to change. | `NoteDue.kt`, `NoteBlocks.kt`, `NoteBlockEditor.kt`, `NoteEditorViewModel.setDue` |

## Not done / next
- Web has no notes screen, so note pictures and paper are Android only.
- Comment bar still has pictures as attachments, not inline.
- Paper and due dates are not in the plain-text share or the list cards yet.
- On-device pass: Underline with Gboard autocorrect, DatePicker inside the Block sheet, long-press drag of a picture on a phone browser.

CI session 6: `7eaf103` failed on two session 5 leftovers in `CreatePostChrome.kt` (missing `setValue`, `ChevronLeft` and `FormatSize` imports); fixed in `2584d07`, and the Android release build (modern APK and AAB) is green. Nothing was run on a device.

---

# Session 7: templates, photo cards, cover controls

Same file, same rule: nothing is built locally, the check is the GitHub Actions Android run. Picked up sessions 3 to 6. Audited first, nothing redone: the `RichState` engine (no markers in the field, so space and backspace cannot leak or revert formatting), block handle and 3-dot gone from every note block (the screenshots predate session 4), Block sheet, sheet insets, hide and show of the format bar in notes, posts and the comment composer, drop caret for dragged pictures, web `neb-live.js` (contenteditable, no Markdown in the field).

## Done

| # | What | Where |
| --- | --- | --- |
| 49 | **New note templates**: Meeting notes, Cornell notes, Project plan, Vocabulary (12 in all). Chapter outline had a bare chevron for an icon; it is now a tree icon. The template sheet scrolls once the grid is taller than the screen. | `NoteBlocks.kt` (`NoteTemplate`), `NotesScreen.kt` (`templateIcon`, `TemplateGrid`) |
| 50 | **List cards show the note's photos**: up to three thumbnails (two in the compact grid) decoded at 320 px, a +n count after them. The `[image]`, `[audio recording]`, `[drawing]` placeholders no longer show as text in the card preview. | `NotesScreen.kt` (`NoteCard`, `previewSkip`) |
| 52 | **Web: the full composer's formatting bar folds** (chevron at its start, Aa brings it back, choice kept in localStorage), the compact comment composer already had it. | `forum-composer.js`, `m3x/app-fc.css`, bundle rebuilt |
| 51 | **Cover controls**: Change keeps its label, Remove is an icon only; both 36dp with finite radii. The page icon over a cover uses the same tonal tile as without one (it was a white tile on a tinted page). | `NoteEditorScreen.kt` (`NotePageHeader`, `HeaderPill`) |

## Not done / next
- Page background pictures (full page, not cover): needs a column and a migration.
- Comment bar pictures are attachments, not inline.
- On-device pass for everything in sessions 4 to 7.

---

# Session 8: page pictures, text colour and highlight, alignment, more looks

Same file, same rule: nothing is built locally, the check is the GitHub Actions Android run. Picked up sessions 3 to 7. Audited first, nothing redone: `RichState` engine (no markers in the field, so space and backspace cannot leak or revert), block handle and 3-dot gone, Block sheet, hide and show of the format bar, drop caret and keyboard-safe pictures on Android and web, `neb-live.js` (contenteditable, one sync per frame). The two reference images used for ideas: a text format panel (colours, alignment) and a quiet reading page; ideas taken, nothing copied.

## Done

| # | What | Where |
| --- | --- | --- |
| 52 | **Page picture** (the open item from sessions 4 to 7). A gallery picture sits fixed behind the scrolling blocks, cropped to fill, with a flat 78 percent wash of the page colour so text stays readable. Scaled to 1600 px, saved as `notes/<id>/bg_<time>.jpg`, decoded once off the main thread, drawn in the draw phase only (no recomposition while scrolling). Appearance sheet: Page picture, Add / Change / Remove. Room version 8, column `bgPhoto` (migration 7 to 8). | `NoteBackdrop.kt`, `NoteEntity`, `DatabaseMigrations`, `NoteEditorViewModel.setBgPhoto`, `NoteEditorScreen` |
| 53 | **Text colour and highlight per block**: nine inks with light and dark pairs (`NoteInk`), one tap in the Block sheet, no codes. A highlight is a flat rounded tint behind the block. Block fields `tint` and `mark` (JSON `tc`, `tf`; old notes load unchanged). Enter keeps the look on the next block. | `NoteInk.kt`, `NoteInkControls.kt`, `NoteBlocks.kt`, `NoteBlockEditor.kt` |
| 54 | **Text alignment per block**: left, centre, right (reuses block `align`, JSON `a`; the hint follows it). The Block sheet scrolls now (it was taller than small screens once these were added). | `NoteBlockEditor.kt`, `NoteEditorViewModel.setLook` |
| 55 | **Paper**: Margin and Wide grid added; the picker scrolls. | `NotePaper.kt` |
| 56 | **Looks**: six more note colours (Lilac, Apricot, Olive, Cocoa, Charcoal, Steel; 28 in all) and five more one-tap themes (Notebook, Recipe, Grove, Cocoa, Studio; 20 in all). | `NoteTones.kt` |
| 57 | **List cards** show the nearest due date of the open to-dos as a tonal chip (red once late). Duplicating a note keeps its paper and copies its cover and page picture files into the new note's folder (`NotesRepository.duplicate`; picture blocks still point at the same files). | `NotesScreen.kt`, `NotesRepository.kt` |

## Rules
- Block look (`align`, `tint`, `mark`) is block data, never a marker in the text. Change it only through `NoteEditorViewModel.setLook`.
- The page picture is drawn by `Modifier.noteBackdrop` placed before `verticalScroll`; do not move it inside the scrolled content.

## Not done / next
- Comment bar pictures are still attachments, not inline.
- Web has no notes screen; the web composers are unchanged this session.
- On-device pass: wash strength on busy photos, ink contrast on the dark tones, Block sheet height with the keyboard open.

CI session 7: `0daff0f` (templates, photo cards, cover controls) is green. `5720dff` (a parallel push: page picture, ink, paper) failed on one wrong `ImageVector` import in `NoteInkControls.kt`; fixed in the next commit.

CI session 8: `5720dff` failed on one wrong `ImageVector` import (fixed in `d809ef8`); the duplicate-files change is the next commit.

---

# Session 9: drop caret and line height, press shape, nav on scroll, notes list, crash screen

Same file, same rule: nothing is built locally, the check is the GitHub Actions Android run. Picked up sessions 3 to 8 (pictures in text, cover controls, notes list). Nothing redone; what was wrong is replaced.

## Done

| # | What | Where |
| --- | --- | --- |
| 58 | **Crash fix**: `Horizontally scrollable component was measured with an infinity maximum width`. `ImageTools` had its own `horizontalScroll` Row and was placed inside the `MediaFrame` tools Row, which also scrolls. It now emits its controls straight into the caller's row. | `NoteBlockMedia.kt` |
| 59 | **Line height with pictures**: the field no longer raises the line height of every line when one picture exists. Only the paragraph holding a picture grows (`ParagraphStyle` with centred `LineHeightStyle`), the rest keep the text's own height. | `RichVisual.build(imageLine)`, `RichTextField.kt` |
| 60 | **Caret height**: with pictures in the field the platform caret is hidden and the field draws its own, text height, centred in the line, blinking, so it never grows on a picture line (as in Meta). | `RichTextField.kt` |
| 61 | **Drop caret**: dragging a picture shows the caret under the fingertip (not the picture's centre), the picture rides 30dp above the finger, the drop snaps before or after a neighbouring picture and never inside one. Web: the drop bar is capped to the text's line height. | `RichTextField.kt` (`RichChip`), `inline-media.js` |
| 62 | **No gap between tool tiles** (comment composer A and the next tile): `ComposerTools` is a Row with 6dp spacing; the note format bar uses 4dp. Web `.fc-tools` gap 6px. | `CommentComposerBar.kt`, `NoteBlockEditor.kt`, `m3x/app-press.css` |
| 63 | **Press follows the shape**: the create (clover) button and the profile sheet settings tile are clipped before they are clickable. Web: tap flash off globally, tool tiles keep their radius. Audit of 104 clickables found the rest already clipped or indication-free. Rule in the design system section 13 and `AGENTS.md` 7b. | `LiquidGlassNav.kt`, `LiquidGlassProfileSheet.kt`, `m3x/app-press.css` |
| 64 | **Contrast**: `readableOn` / `softReadable` pick an ink that reaches 4.5:1 (text) or 3:1 (icons) on the note colour. Used for the editor top bar (undo and redo no longer fade to 35%), the pin, the Untitled hint and the card pin and tick. | `NoteContrast.kt`, `NoteEditorScreen.kt`, `NotesScreen.kt` |
| 65 | **Notes header**: one 56dp row (title, four 40dp tools 4dp apart, filled add tile), filters directly under it, search field 48dp. Tools are clipped tonal tiles. | `NotesScreen.kt` (`Header`, `HeaderTool`) |
| 66 | **Note cards**: adaptive staggered grid (156dp minimum, 2 columns on phones), 8dp gaps; cover 64dp (grid) and 84dp (list); icon tile 24dp, title on titleSmall; at most 3 preview lines in the grid, 2 lines each; one row of thumbnails at 52 or 64dp. | `NotesScreen.kt` (`NoteCard`) |
| 67 | **Covers**: editor cover height follows the width (`aspectRatio(1.9)`, 168 to 264dp). Banner art scales with the banner's proportions. Change and Remove show only after tapping the cover and fold after 4s. | `NoteEditorScreen.kt`, `NotePage.kt` |
| 68 | **Bottom bar hides on scroll down, returns on scroll up** (Home, Library, Notes and every screen that shows it): one `NestedScrollConnection` above the NavHost, the bar follows the finger, a spring settles it, layer transform only. Pinned while the create menu is open; resets on route change. | `NavBarScroll.kt`, `Navigation.kt` |
| 69 | **Crash screen** rebuilt in M3X: page colour, expressive tile, short title, error type chip, details folded away, Copy log (tonal) and Restart (filled) pinned at the bottom. | `CrashActivity.kt` |

## Rules (also in `docs/M3X_DESIGN_SYSTEM.md` section 13)
- Clip before clickable, same shape. Tiles in a row have a gap. No same-axis scroller inside another. Icons on a themed surface go through `readableOn`.
- Text with pictures: normal line height, only the picture line grows, own caret at text height.

## Not done / next
- On-device pass: caret blink after a picture is inserted, the drop caret near the field's bottom edge (no auto-scroll while dragging yet), staggered card heights with many photos, the bar returning when a list is shorter than the screen.

CI session 9: `82ee9dc` failed to compile: `AnimatedVisibility` in the cover header resolved to the `ColumnScope` extension of the surrounding `Column` ("cannot be called in this context with an implicit receiver"). Fixed by moving the cover and its Change / Remove pills into `NoteCoverArea` (own function, no outer receiver). Rule: an `AnimatedVisibility` inside a `Box` that sits inside a `Column` or `Row` lambda needs its own composable.

| 70 | **Press follows the shape, second pass**: re-audited every `clickable` by script (clip within the 9 lines before it). Fixed the ones that still drew a square ripple: notification avatar (circle), note paper chips (22dp), comment composer menu rows (16dp), library selector (14dp), note icon tile (20dp). | `NotificationRow.kt`, `NotePaper.kt`, `CommentComposerBar.kt`, `LibraryScreen.kt`, `NoteEditorScreen.kt` |

CI: `abb8165` (cover area fix plus press pass) is green; the Android release build compiles. Web CSS bundle is in sync (`python3 tools/css/bundle.py --check`).


| 71 | **Drag follows the drop caret**: while a picture is dragged in a post, reply or comment field, the page scrolls so the drop caret (with 56dp of room above and below) stays visible (`BringIntoViewRequester`), closing the session 9 note about no auto-scroll. Web: inline pictures in the writing surface use a negative block margin so a picture never raises its line (`12-inline-images.css`, bundled into `app.css`). | `RichTextField.kt`, `css/app/12-inline-images.css` |

Session 10 audit (nothing redone): sessions 9 items 58 to 70 were re-checked against the request. Crash: no nested same-axis scroller is left (script over every `horizontalScroll` caller, `ImageTools` fixed in 58, no scroller inside a `LazyRow` item). CI for `abb8165` is green.

---

# Session 11: audit of sessions 9 and 10, global press shape

Same file, same rule: nothing is built locally, the check is the GitHub Actions Android run. The request came again (drop caret, line spacing, caret height, tile gaps, press shape, note contrast, notes list, covers, nav bar, crash, crash screen). Everything was audited against the code first; items 58 to 71 stand and nothing was redone.

| # | What | Where |
| --- | --- | --- |
| 72 | **Press shape, global**. The audit by script (clip within 9 lines before each `clickable`) only covers `clickable`. 19 more sites (`combinedClickable` on avatars, `tactileClickable`, full-width menu rows) can not all be clipped by hand, so the app now provides `NebIndication` as `LocalIndication` inside `NEBiansTheme`: a state layer in the content colour (press 12%, focus 10%, hover 8%) drawn inside a rounded shape, a circle on small square controls and 16dp elsewhere, one animated alpha read in the draw phase. A clipped control with a larger radius keeps its radius (the clip wins). Explicit `ripple(bounded = true)` sites were already clipped (audited). | `ui/theme/NebIndication.kt`, `Theme.kt` |
| 73 | **Note body line height** 26sp to 24sp (1.5 times the text, close to Meta); a line holding a picture still grows alone. | `NoteBlockEditor.kt` |
| 74 | Rule in `docs/M3X_DESIGN_SYSTEM.md` 13.1 and `AGENTS.md` 7b: do not remove or bypass `NebIndication`. | docs |

Crash re-check: every `horizontalScroll` / `LazyRow` caller was read for a scroller below a horizontal scroller. `ImageTools` (item 58) was the one; none left. Comment composer has no inline pictures (attachments), so the caret height fix applies to post, reply and note fields.

## Not done / next
- On-device pass for `NebIndication` on dark note tones (content colour on tone) and on the glass bottom bar.

---

# Session 12: crash guard, drag caret that follows the finger

Same file, same rule: nothing is built locally, the check is the GitHub Actions Android run. The request came a fourth time. Items 58 to 74 were read against the code again (nav bar scroll, notes header and cards, covers, contrast, crash screen, press shape, web drop bar). They stand; only what was still weak is changed.

| # | What | Where |
| --- | --- | --- |
| 75 | **Crash, defence in depth**. Sessions 9 to 11 removed the one known nested scroller, but the report keeps coming from a release build whose stack names no screen. Every `horizontalScroll` (33 files) now goes through `nebHorizontalScroll`, which puts `boundedWidth()` in front: an infinite max width from any ancestor becomes the screen width, so it can not throw. | `ui/components/SafeScroll.kt`, all callers |
| 76 | **Drop caret no longer drifts**. The finger was computed from accumulated drag deltas, so a page that scrolled during the drag (item 71) moved the caret away from the finger. It is now read with `localPositionOf` between the picture and the field's overlay. Scroll-follow keeps one job and cancels the previous. | `RichTextField.kt` |
| 77 | **Tighter picture line, Meta caret**. A picture line is the picture plus 6dp (was 10); the caret is 1.2 em (was the measured line height of the style). | `RichTextField.kt` |
| 78 | Rules: `nebHorizontalScroll` only; drop caret from screen position. | `docs/M3X_DESIGN_SYSTEM.md` 13.4, 13.5, `AGENTS.md` 7b |

## Not done / next
- On-device pass: drag a picture near the field's bottom edge while the page scrolls; caret on a picture line after the keyboard opens.

CI session 12: `8fc2292` (guarded scroller, drag caret, picture line) is green; the Android release build compiles.

---

# Session 13: crash guard for lazy lists and pagers

Same file, same rule: nothing is built locally, the check is the GitHub Actions Android run. The request came a fifth time with the same stack. Items 58 to 78 were read against the code again; they stand. The one hole left in the crash fix: session 12 guarded `horizontalScroll`, but `LazyRow` and `HorizontalPager` run the same constraint check (`checkScrollableContainerConstraints`) and were not guarded, so a lazy list under any horizontally scrolling or wrap-content ancestor still threw.

| # | What | Where |
| --- | --- | --- |
| 79 | **Crash, lazy lists and pagers**. All 15 `LazyRow` and 4 `HorizontalPager` calls take `Modifier.boundedWidth()` (an infinite max width becomes the screen width). | Home, news, marketplace, creator studio, upload, shimmer, reader, intro, zoom, post detail |
| 80 | **Audit script** `tools/android/check_scrollers.py`: fails on a bare `horizontalScroll(` or an unguarded `LazyRow(` / `HorizontalPager(`. Runs first in `build-release.yml`. Rule in design system 13.4 and `AGENTS.md` 7b. | `tools/android`, workflow |

## Not done / next
- On-device pass for the drag caret and for the bar hiding on Home, Library and Notes.

CI session 13: `3a2eb9a` (lazy list and pager guard, audit script step) is green; the Android release build compiles.


---

# Session 14: drop caret is the real caret, picture line gap, notes cards, selection menu, crash screen

Same file, same rule: nothing is built locally, the check is the GitHub Actions Android run. Picked up sessions 9 to 13 (drop caret, picture line height, notes list, crash screen); nothing redone, the causes of what still looked wrong were found and fixed.

## Done

| # | What | Where |
| --- | --- | --- |
| 81 | **The blue horizontal bar was a layout bug, and is gone.** `RichTextField` has `propagateMinConstraints = true`; the drop bar was a direct child with a fixed 2.5dp width, so the field's minimum width was forced on it and it stretched from the caret to the right edge. No bar is drawn any more. While a picture is dragged the field's own caret (the keyboard's cursor) moves to the landing place: `RichState.moveCaret` sets the real selection when the snapped offset changes, the caret is drawn solid while dragging, and `restoreSelection` hands the old selection back on cancel. After a drop the caret sits after the picture. | `RichTextField.kt`, `RichState.kt` |
| 82 | **The gap under a picture line was a platform quirk.** A Compose paragraph that ends in a real line break gets one more empty line (StaticLayout adds a line after a trailing break). The picture paragraph included its `\n`. Now the break next to a picture line is a zero width mark (U+200B) in the drawn text (same length, so the offset maps stay simple), a picture line is its own paragraph that ends on the mark, and an empty last line after a picture line gets a mark so it still has a line. Picture 38dp to 32dp, line = picture + 4dp (was + 6). | `RichVisual.kt`, `RichTextField.kt` |
| 83 | **Notes list cards**: staggered grid kept, cards shorter (cover 44 / 60dp, tighter padding, 22dp radius, one footer line with date, one chip, to-do progress). New previews of everything a note holds: pictures as a 1 / 2 / 3-up mosaic with +N, recordings as a waveform tile with the length, a drawing redrawn from its strokes (pens that would vanish on the note colour use the ink), a table as a mini grid, a code snippet as a mono tile. Media is read off the main thread and cached by id and edit time (`NoteMediaCache`), cards skip recomposition (`NoteEntity`, `NoteBlock`, `Stroke` added to `compose_stability.conf`), grid items have a `contentType`. | `NoteCard.kt`, `NoteCardMedia.kt`, `NoteMedia.kt`, `NotesScreen.kt` |
| 84 | **Record controls smaller** in notes: the dictation button 52 to 40dp (icon 20), the show-toolbar tile 48 to 40dp, the empty recording block is one 36dp row (Record, File), the live recording bar and the player are 36 to 40dp. | `NoteEditorScreen.kt`, `NoteBlockMedia.kt` |
| 85 | **Own menu for selected text**: a floating pill (float colour, hairline, no shadow, spring in) with Cut, Copy, Paste, Select all, and Bold, Italic, Underline icons in writing fields. Placed above the selection, below it near the top edge, never takes focus so the keyboard stays. `LocalTextToolbar` is provided once in `NEBiansTheme` (every field) and again in `RichTextField` with the format actions. Dialog and sheet windows keep the system menu (Compose gives them their own toolbar). | `NebTextToolbar.kt`, `Theme.kt`, `RichTextField.kt` |
| 86 | **Crash screen revamp**: clover tile that springs in, one short title and line, the error in a hairline card with the type as a tonal chip, the log folded in a second card (chevron turns on a spring, mono tile), Copy log and Share tonal, one filled Restart. | `CrashActivity.kt` |
| 87 | **Web**: the drop caret is 2px, like a text caret (the mouse path already moved the real selection while dragging). | `inline-media.js` |

## Rules
See `docs/M3X_DESIGN_SYSTEM.md` 13.5 (paragraph never ends on a line break, no fixed-size child under `propagateMinConstraints`), 13.5b (selection menu) and 13.6 (list card preview).

## Not done / next
- On-device pass: drag a picture between lines of a wrapped paragraph (the whole paragraph that holds a picture is the taller one, Compose has no per-visual-line height), caret placement on the empty line after a picture, the selection menu next to the top edge and with the glass bottom bar, staggered card heights with many media notes.

CI session 14: `7e078d9` is green on the first push; the Android release build (APK and AAB) compiles. Nothing was run on a device.

---

# Session 15: audit of session 14, startup profile for the notes path

Same file, same rule: nothing is built locally, the check is the GitHub Actions Android run. The request came again (caret that follows the dragged picture, line gap after a picture, staggered notes list with every preview, smaller record controls, own selection menu, crash screen, speed). Items 81 to 87 were read against the code and the screenshots; they cover every point, so nothing was redone:

- Drag: no bar anywhere in `RichTextField`; `RichState.moveCaret` walks the real selection under the fingertip, the field draws the caret at text height, solid while dragging, `restoreSelection` on cancel.
- Gap: picture paragraph ends on U+200B, not `\n`; picture 32dp, line = picture + 4dp, other lines keep the text's height.
- Notes list, record controls, selection menu, crash screen: items 83 to 86. Audit of those files: no emoji, no shadow, no gradient.
- Web: the 2px drop caret and the touch drag path exist in `inline-media.js`.

## Done

| # | What | Where |
| --- | --- | --- |
| 88 | **Baseline profile covers the notes path.** The profile listed Home, forum, library and the data layer only, so the notes list, the editor, the crash screen and settings, bookmarks, downloads, marketplace, reader, onboarding and upload ran interpreted until the idle-time compiler caught up. They are now compiled ahead of time at install (`components/**`, which holds the writing field, the selection menu and the card previews, was already listed). | `app/src/main/baseline-prof.txt` |

## Not done / next
- On-device pass (nothing here has run on a phone): drag between lines of a wrapped paragraph (the whole paragraph that holds a picture is the taller one; Compose has no per-visual-line height), the selection menu near the top edge, staggered card heights with many media notes. If the line gap still looks wrong on the phone, send a screenshot of the exact text; the cause will be in `RichVisual.build` paragraph ranges.

CI session 15: `66ad86e` is green; the Android release build (APK and AAB) compiles. Nothing was run on a device.


---

# Session 16: guest browsing, sign-in that returns, caret follow, Pathways, dynamic post demos

Same file, same rule: nothing is built locally, the check is the GitHub Actions Android run (and `backend-tests.yml` for the Django side). Picks up sessions 14 and 15; nothing redone.

## Done

| # | What | Where |
| --- | --- | --- |
| 89 | **No login gate.** Splash and Intro now go to Home for a guest. Signing out lands on Home, not Login. Login is a screen you are sent to, with a close button; system Back returns to where you were. | `Navigation.kt`, `LoginScreen.kt` |
| 90 | **One door for protected actions**: `AuthGate` (`LocalAuthGate.current.require(GateReason.X) { ... }`). A guest gets the `SignInSheet` (icon, one line, Sign in, Not now) and stays on the screen. Wired: like, save, follow, poll vote, reply (feed, forum, detail, thread sheet), New post and Upload in the create menu, profile avatar. The reply composer is replaced by `GuestReplyBar` for guests. | `components/AuthGate.kt`, `ForumPostDetailScreen.kt`, `ForumScreen.kt`, `HomeScreen.kt` |
| 91 | **Returns to the same screen after sign-in.** Login is pushed over the origin screen; every finish path (social sign-in, email, verify, forgot, complete profile) calls `leaveAuth()` which pops back to Login's parent. A gated destination (create post, upload, bookmarks, notifications, analytics, credits, edit profile ...) is stopped by `gateReasonFor(route)`, the guest is popped back and the sheet opens; the wanted route is kept in `pendingRoute` (saveable) and opened once signed in. Back from Login clears it. | `Navigation.kt` |
| 92 | **Caret follows the writing.** `RichTextField` scrolls the page so the caret line plus 112dp stays visible while typing (also after the keyboard has settled, 280 ms later), in posts, replies and note blocks. Skipped while a picture is dragged (that path has its own follow). | `RichTextField.kt` |
| 93 | **Pathways** (web `/app/pathways/`, API `/api/pathways/`, Android `PathwaysScreen`): 4 stages (After Class 8, SEE, +2, Bachelor) with 45 routes, 24 careers (demand, competition, abroad demand, monthly pay, trend), 17 listed providers, 14 scholarships (embassy and government routes), 10 study abroad countries. Route sheet: cost, duration, entry, exam, skills, careers, next steps, where to study with a district picker (listed providers plus live colleges from `/api/institutions/`). One shared JSON (`api/data/pathways/*.json`, merged by `api/pathways.py`, ETag + 1h cache). Android keeps a disk copy and refreshes with `If-None-Match`. Entry points: Home top row (guests too), Tools, web Tools hub. | `api/pathways.py`, `api/views_pathways.py`, `web/views_pathways.py`, `pathways.js/css/html`, `ui/screens/pathways/` |
| 94 | **Dynamic posts: demo lab** (no backend change yet). Six looks (Paper, Ink, Garden, Sunrise, Blueprint, Rose) plus Default, each with paper, ink, accent, type, a flat cover pattern, drop cap and quote bar; every look shown as feed card and as reading view. Tools, Android only for now. | `ui/screens/pathways/DynamicPostsLabScreen.kt` |

## Data rules (Pathways)
- Fees are total programme cost in NPR, pay is monthly NPR, demand and competition are 1 to 5. All are indicative and the screen says so. `api/test_pathways.py` fails on a broken id reference, an out of range score, a non-public API or an emoji.
- To add a college: append to `places.json` `providers` and put its id in the route's `where`. To add a course: append to `routes_*.json` (stage must exist, careers and next must resolve).
- Verify every figure against the institution or ministry before widening claims; many seat counts and fees change every intake.

## Not done / next
- Dynamic posts: pick a direction from the lab, then add a `look` field to posts (server) and a look picker in the composer; web lab page. Nothing of the post model changed.
- Web: guests already browse the web; sign-in prompts for web interactions are not unified with the Android sheet yet.
- Pathways: more providers per district (the live list falls back to the 24k institution catalogue), per-course seat and fee tables, Nepali labels, saved pathways for signed-in users.
- On-device pass: sign-in return from the reply bar, gated create menu, caret scroll with the glass bar.


---

# Session 17: CI repair, Pathways data wave 2, web sign-in sheet, web dynamic posts lab

Same file, same rule: nothing is built locally, the check is the GitHub Actions Android run. Session 16 (`c448719`) had failed CI, so that came first. Items 89 to 94 were read against the code and stand; nothing redone.

## Done

| # | What | Where |
| --- | --- | --- |
| 95 | **CI repair.** `c448719` failed: `NebModalSheet` is experimental material3 API and two files called it without the opt-in. Added `@file:OptIn(ExperimentalMaterial3Api::class)`. | `components/AuthGate.kt`, `screens/pathways/PathwaysScreen.kt` |
| 96 | **Pathways data wave 2** (no UI change, both apps read the same API): routes 45 to 63 (skill training, police and army, A Levels, hotel diploma, BE Electrical and Mechanical, BDS, BMLT, BPT, BPH, BVSc, BTTM, BFA, BSc science, MPH, ACCA, banking, freelance, PhD), careers 24 to 32, providers 17 to 36 (Pokhara, Dharan, Biratnagar, Surkhet, Mahendranagar, Chitwan, Bhaktapur, private colleges), scholarships 14 to 22 (Aga Khan, Rotary, Swiss, Holland, ICCR, Manaaki, Russia, Gates Cambridge), study abroad 10 to 16 (New Zealand, Netherlands, Finland, Malaysia, Turkiye, Russia). `where_add` in `extra_places.json` attaches new providers to existing routes. `problems()` now also reports duplicate ids. | `api/data/pathways/routes_d.json`, `extra_careers.json`, `extra_places.json`, `api/pathways.py` |
| 97 | **Web sign-in sheet, one door.** `NebAuth.require(reason)` (loaded from `base.html`) opens a bottom sheet on phones and a centred card on desktop: Sign in, Create account, Not now. Both links carry `?next=<this page>` so the person lands back on the same screen (the login page already honours `next`; it now also accepts `panel=signup`). Every guest redirect in home, forum, post, search, profile, subject, resource, news, poll, marketplace and peer-card code calls it instead of `window.location.href = /login/` (which dropped the page). An htmx 401 opens it too. `data-auth-gate="reply"` markup hook exists for new buttons. Styles are injected on first open. | `web/static/web/js/neb-auth-gate.js`, templates, `home.js` |
| 98 | **Web dynamic posts lab** `/app/lab/dynamic-posts/` (tools hub card "Dynamic posts"): the same six looks as Android plus Default, feed card and reading view, and a live customiser (pattern, type, corners, drop cap, quote bar, accent). Flat colour, SVG patterns, CSS variables only, no gradient or shadow. noindex. | `dynamic_posts_lab.html`, `dynamic-posts-lab.js/css`, `views_pathways.py` |

## Web composer caret
`composer-editor.js` already keeps the caret inside the viewport (twin-measured caret, scroll on input); Android got the same in item 92. Nothing changed.

## Not done / next
- Dynamic posts is still a lab. Next: pick the direction, add a `look` JSON field (paper, accent, font, pattern, flags) to forum posts with a null default so old posts keep the default look, a look picker in both composers, and render the look in feed cards and the reader.
- Pathways: Nepali labels, saved pathways for signed-in users, per-course seat and fee tables, a FAQ tab ("what after SEE" questions), more private colleges per district. Verify every figure against the institution before widening claims.
- Web: pass a specific reason (like, save, reply) from each call site to `NebAuth.require`.
- On-device pass: sign-in return from the reply bar, gated create menu.
