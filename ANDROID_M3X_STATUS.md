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
- Shadows: every `shadowElevation` outside `LiquidGlassNav` is 0.
- Post composer: poll duration is a row of single-choice chips (`ui/components/NebChoiceChips.kt`) instead of a sheet. Inline images, markdown toolbar, preview and mentions were already in.

## Not done yet

- Nested replies are always comments (the kind chips live only on the main thread composer, matching the API).
- Mark sheet shows no label counts yet.
- Post cards inside profile and search lists use `ForumPostCard`; `WebPostCard` (compact variant) still has the older drawing.
- Nothing here has been seen on a device. Both `compileModernDebugKotlin` and `compileLegacyDebugKotlin` pass. First thing to do on hardware: splash timing, intro blob morph (assumes MaterialShapes polygons live in the unit box), dark theme.

## Build

JDK 17 and the Android SDK are installed per session (see `ANDROID_UI_CONTINUITY.md` section 8). Compile both variants, one after the other. On a 4 GB box the Kotlin daemon dies when both run in parallel: use `--no-parallel -Pkotlin.compiler.execution.strategy=in-process -Dorg.gradle.jvmargs="-Xmx2800m"`.
