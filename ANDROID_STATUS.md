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
