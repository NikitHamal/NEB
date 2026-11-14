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
