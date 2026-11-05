# Android m3x parity: status

Goal: bring the Android app up to the web's m3x design system (brand blue, Poppins, tonal surfaces, no shadows, no emojis, no boxed user badges, finite radii).

## Shipped

- Palette: `tools/design/sync_android_palette.py` copies every `--md-*` role from `m3x/tokens.css` into `Palette.kt` (light and dark). Run it after any token change; `--check` fails on drift. Android and web now share primary `#0058DF`, the blue-tinted surfaces and the teal tertiary.
- Splash (`ui/screens/auth/SplashScreen.kt`): a cookie blooms and morphs through clover, sunny and flower while the N assembles; four tonal tiles (azure, sky, aqua, periwinkle) spring out and settle; NEBians rises letter by letter; everything pushes forward and fades. Springs only, honours reduced motion, destination resolved in parallel.
- Intro (`ui/screens/onboarding/Intro*.kt`, route `intro`, flag `SettingsRepository.isIntroSeen`): four pages taken from the landing page (hero search, level picker, forum, Ask Neby). One blob behind the pager morphs between landing shapes as you swipe; each page plays its entrance when it settles. Shown once, before sign-in; the profile-completion flow is unchanged.
- Shared pieces: `ui/components/NebShapeStage.kt` (`NebTone`, `NebGlyphShapes`, `NebMorphBlob`, `drawGlyph`).
- Forum replies: API replies now carry `kind`, `label`, `canLabel`; `POST /api/replies/<id>/label/`; replies accept `kind`. App: kind chips in the main comment composer, kind and label tags on `CommentCard` (tonal chips, no badge backgrounds elsewhere), a Mark sheet for the discussion author, comment card radius 8dp to 20dp.
- Landing: community heading is now "Ask what you wonder. Share what you know." (the old 11 pm line described traffic the forum does not have).
- Cards: `ForumPostCard` is the web `post-card` (24dp radius, outline-variant hairline, `#category` primary-container tag, ghost action row: tonal like pill, comment count, views for the author only, bookmark, share). `WebResourceCard` is the web `rcard` (28dp card, inset 20dp art, type badge, tonal subject and grade tags, avatar + views footer; no scrim, no circle badge). Rail cards in `NebCompactCards.kt` use the same radii and tonal chips; news chips use secondary-container instead of the data colour.
- Shadows: no `.shadow()` modifier and no non-zero `shadowElevation` remain (nav, floating bars, canvas cards, PDF pages included).
- Post composer: poll duration is a row of single-choice chips (`ui/components/NebChoiceChips.kt`) instead of a sheet. Inline images, markdown toolbar, preview and mentions were already in.

## Session 2 (CI-verified only; nothing is built locally)

- Light theme is paper white: `sync_android_palette.py` pins light `background` and `surface` to `#FFFFFF` (`ANDROID_LIGHT_OVERRIDES`); the web keeps its blue-tinted page. Dark is unchanged. `--check` still passes.
- Splash: the mark is `R.drawable.ic_launcher_foreground`, the launcher icon itself, drawn whole (springs in, slight turn). The old `NebLogoMark` re-drew each facet with its own stroke and transform and read as spliced; it is deleted. Splash page is white, matching the system splash window.
- Post composer (`ui/screens/forum/CreatePost*.kt`) is the web mobile dialog: header (close, identity pill, `#category` pill, round publish button, grey until the post is real), borderless title and the markdown row with the Write/Preview toggle pinned, a body that scrolls (writing area, poll builder, picture strip, attachment list), a hairline with the character count, and a footer of tools (photos, video/audio, poll, document, picture inside the text). Identity and category open choice sheets. Title is optional like the web (`derivePostTitle` stands in). Emoji picker is not ported (emoji ban); the keyboard has one.
- Poll builder: title row with Remove, Voting poll / MCQ quiz chips, question, options with the correct-answer mark for quizzes, Add option, closing time chips.
- Comment composer (`CommentComposerBar.kt`): one outlined container whose stroke turns primary while anything in it has focus, leading tools inside it, round send/mic button inside it, same as the web `neb-composer`. Kind chips use the secondary container.
- Intro: the picture trails the swipe and the words lead it and fade first; titles scale with screen width; dots are tappable; a light haptic lands each page; reduced motion snaps the entrances; the CTA label change animates its width.
- `WebPostCard` (search, profile rows): tonal `#tag`, author and time, ghost like and reply count, no outlined pills. Avatars (`NebAvatar`, `Avatar`, avatar preview, creator page) no longer draw a circle stroke.
- Home welcome panel: flat primary-container panel, no gradient, no tagline.

## Not done yet

- Nested replies are always comments (the kind chips live only on the main thread composer, matching the API).
- Mark sheet shows no label counts yet.
- Gradients elsewhere in the app (mini player, canvas, marketplace) have not been audited against the no-blue-gradient rule.
- LaTeX helper keys and table/spoiler/divider tools from the web toolbar are not in the Android markdown row.
- Nothing here has been seen on a device; the only compile check is the GitHub Actions `Build Student Release APKs & AAB` run on each push. Both `compileModernDebugKotlin` and `compileLegacyDebugKotlin` pass. First thing to do on hardware: splash timing, intro blob morph (assumes MaterialShapes polygons live in the unit box), dark theme.

## Build

JDK 17 and the Android SDK are installed per session (see `ANDROID_UI_CONTINUITY.md` section 8). Compile both variants, one after the other. On a 4 GB box the Kotlin daemon dies when both run in parallel: use `--no-parallel -Pkotlin.compiler.execution.strategy=in-process -Dorg.gradle.jvmargs="-Xmx2800m"`.
