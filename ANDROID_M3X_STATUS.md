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

## Session 3 (CI-verified only; nothing is built locally)

- Auth landing (`ui/screens/auth/AuthHero.kt`, `LoginScreen.kt`, `AuthActionButtons.kt`): the pixel sky is gone. White page, a tonal blob that keeps morphing cookie, sunny, flower, clover with the launcher N mark in it, three glyph tiles (search, forum, library) that spring out and drift. A tap squeezes the mark with a haptic. Title and buttons rise on `Reveal` springs. Tagline cut. Provider buttons are pressable pills (`nebPressable`: scale spring plus haptic), the email one in the brand soft tone. Reduced motion snaps everything.
- Email auth: `AuthGlyphMark` above the headline springs in and morphs cookie to flower when the form flips between sign-in and sign-up. The helper line under the headline is cut.
- Avatars (`ui/components/AvatarShapes.kt`): the web's seven silhouettes (cookie, sunny, flower, clover, burst, oval, squircle) chosen by the same FNV-1a hash of the name, and the same three tonal fills for initials. Used by `Avatar`, `NebAvatar`, profile header, creator pages. Neby, NEBians and Anonymous stay round. The gradient ring is gone; the admin and verified marks are bare icons, no disc behind them.
- Cards: `NebCard` presses with a spring scale and a one-step tonal warm-up, one haptic. Rail cards, home panels, search bar, subject chips, notification rows use `nebPressable`.
- Shapes instead of plain circles: home quick-action tiles (cookie, sunny, flower), system notification glyph.
- Gradients: the home banner, welcome wash, library panel and mini player are flat tonal fills now. Scrims (black to clear over photos) and the festival theme card stay.
- Screen transitions (`Navigation.kt`): shared-axis slide on springs instead of tweens; login fades.
- Markdown row: code block and divider added, tool buttons are tonal rounded squares with a spring and a tick.

## Not done yet (after session 3)

- Table and spoiler tools (the renderer has no table or `||spoiler||` support yet).
- Mark sheet label counts; kind chips on nested replies.
- Remaining `CircleShape` tiles in analytics, canvas, media player and study screens.
- Everything above is seen only through CI compiles; check it on a device.

## Session 4

Canvas is replaced by **Notes** with on-device dictation (Whistle) and read aloud (Phonon); see `ANDROID_NOTES_STATUS.md`.

## Build

JDK 17 and the Android SDK are installed per session (see `ANDROID_UI_CONTINUITY.md` section 8). Compile both variants, one after the other. On a 4 GB box the Kotlin daemon dies when both run in parallel: use `--no-parallel -Pkotlin.compiler.execution.strategy=in-process -Dorg.gradle.jvmargs="-Xmx2800m"`.

## Session 5 (CI-verified only; nothing is built locally)

Brief: the app still read bluish next to the web forum; the composer needed a dropdown identity switcher and the web's own icons; revamp every screen in that direction.

- Web icon set: `tools/design/svg_to_vector.py` turns the web composer's inline SVGs into `res/drawable/ic_neb_*.xml` (24 grid, 2px round stroke). `ui/components/NebIcon.kt` (`NebIcons`, `NebIcon`) is the only way to draw them; the markdown toolbar, composer header, footer and poll builder use them.
- Identity: `NebIdentityPicker` is the web dropdown (Post anonymously as `Anon#xxxx` / Post as yourself, tick on the active row). `anonTagFor` repeats the server hash. Replaces the old choice sheet. The same picker is reused by the home launcher.
- Composer chrome moved to `CreatePostChrome.kt` (header, format row with picture-in-text, footer with the counter at its end).
- Feed (Home and Forum): page is white (`surface`), the bluish `surfaceContainerLow` page fill is gone. Feed rows are flat like the web feed: no frame, one hairline under each (`NebHairline`), the same row on Home, Forum and (through `ForumPostCard`) everywhere it is used. Comment, share and view glyphs on the row come from the web set (`ic_neb_comment`, `ic_neb_share`, `ic_neb_eye`).
- Composer launcher (`NebComposerLauncher`): identity dropdown, prompt pill, four tool glyphs, first row of Home and Forum. `PostIdentityPreference` carries the identity pick into the composer. The Forum FAB is a squircle with the web plus and no elevation.
- Capture: `tools/app-screens/flows/07-composer.yaml` (launcher, composer, identity menu, anonymous). Run `App screen captures (reel)` after a green build.

## Not done yet (after session 5)

- Table and spoiler tools in the markdown row (renderer lacks them).
- Post detail, replies, library and profile screens still use Material glyphs for their own actions; swap them for `NebIcons` as the web set grows (bookmark, thumb, bell are not in it yet).
