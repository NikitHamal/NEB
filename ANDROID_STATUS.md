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
