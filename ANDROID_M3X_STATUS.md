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

## Session 6 (CI-verified only; nothing is built locally)

Brief: the app still did not read like the web. Method this time: the web was run locally (Django on sqlite, seeded post and replies, Playwright at 390 px) and the screenshots were compared with the app's layout before each change.

- Home: the composer launcher is gone from the first row (Forum keeps its squircle FAB). `NebComposerLauncher` stays for the Forum row.
- Festival decor, app (`ui/theme/SeasonAmbience.kt`): Tihar is a thread of glass bulbs (cap, body, highlight, warm halo, twinkle) with a few crisp four-point sparkles, not blurred dots across the feed. Dashain is a mala of eight-petal marigolds swaying on a thread with falling petals. Holi is soft gulal clouds (no purple), gurans petals, rain and snow (tinted so it shows on white). The band is the top 190 dp only, fades out when the feed scrolls, holds still for reduced motion. `SiteThemeState.hasGarland` lets Home leave 36 dp under the garland. The season card is a flat tonal fill (gradient removed).
- Festival decor, web (`static/web/css/themes.css`, `themes/_decor.html`): every `box-shadow` removed (glows are radial pseudo-elements), Tihar bulbs get caps and halos, fireflies are sparkles, Dashain flowers are marigolds, purple rangoli petals replaced with orange, season card keeps wish, Neby and close on one row on phones.
- Post reader (`ForumPostDetailScreen.kt`) follows the web page top to bottom: `DiscussionHeader` (back, Discussion, `#category` tag, hairline), author row (44 dp avatar, name, `@handle · time`, more menu), title, body, time, hairline, ghost action row (like, comments with the web glyph, bookmark, share), the reply composer inline under the post, `Replies N` with the Oldest / Newest / Top segmented control, flat replies.
- Reply composer (`CommentComposerBar.kt`): inline (`docked = false`), 28 dp outlined pill, avatar with a chevron badge that opens the identity menu (`NebIdentityAvatarMenu`), placeholder `Post your reply...`, paperclip and the round send button in the trailing slot (`trailingContent`); disabled send is the secondary container, like the web. The thread sheet keeps the docked variant with the same controls.
- Replies (`CommentCard`) are flat: no frame, hairline under each, 36 dp avatar, body indented under the name, name bold.
- Like colour: `LikePill` is ghost and turns brand primary when liked (the web's `.liked`), never on-primary-container navy.
- Identity picker: the trigger shows a real 20 dp chevron-down in `onSurface`.
- Bottom bar (`LiquidGlassNav.kt`): real backdrop glass. `Modifier.glassSource(GlassBackdrop)` records the NavHost into a `GraphicsLayer`; `Modifier.liquidGlass` re-draws that layer behind the bar into its own layer with a `BlurEffect` (API 31+), then a neutral surface tint, a top sheen and a hairline rim. The create clover uses the same surface. Below API 31 the tint is 95 % opaque. No shadow, no coloured gradient.

## Not done yet (after session 6)

- Follow chip beside the author on the reader (needs the follow endpoint wired into the post detail view model).
- The reader's formatting ("A") tool in the reply composer.
- Everything here is seen only through CI compiles and the web screenshots; check blur strength and the garland on a device.

## Session 7 (CI-verified only; nothing is built locally)

- Analytics (`ui/screens/analytics/AnalyticsScreen.kt`): replaced remaining `CircleShape` hero, KPI, and table rank tiles with rounded squircles (`RoundedCornerShape`), swapped monochrome `onSurface` chart bars, accuracy ring, and progress bars for brand `primary` with tonal `primaryContainer`/`secondaryContainer` fills, and removed redundant helper subtitles across dashboard sections.

## Session 8: cleanup + analytics overhaul (CI-verified only; nothing is built locally)

Brief: remove AI chat, Study Lab and the other dead study surfaces from the app (only @neby and the PDF reader's Neby AI stay); rebuild the Analytics screen on m3x; rebuild the backend analytics behind it.

- Removed: AI chat (`NebyAiScreen`, view model, composer, empty state), Study Lab, Study Space, document detail, the unreferenced Canvas screens, their routes, the Study / Arena / Qwen endpoints and models in `ApiService`, and three dead Home composables (`HomeWelcomePanel`, `HomeQuickActions`, `HomeStudyHub`). The PDF reader's Neby AI keeps its message rows in `ui/screens/reader/NebyAnswer.kt` (moved from `ai/chat`, own `NebyMessage`). Syllabus reader, Interactive courses, Notes and Neby credits are untouched.
- Backend: `api/user_analytics.py` builds the v2 payload for `GET /api/users/me/analytics/?days=7|30|90` (see `docs/ANALYTICS.md`, member section). 24 queries, tests in `api/test_user_analytics.py`. Legacy keys stay; the Study Lab fields are gone. Backend deploys are manual (`deploy.ps1`): until it ships, the app shows "Analytics is updating" because the payload has no `version: 2`.
- Android models: `data/api/AnalyticsModels.kt` mirrors the payload field for field (checked against a real response, no field missing).
- Android screen (`ui/screens/analytics/`): `AnalyticsScreen` (title bar, range chips 7/30/90, one `LazyColumn`), `AnalyticsViewModel` (per-range cache, thin progress bar while a range loads), `AnalyticsOverview` (standing hero on primary container, streak card with the last seven days, "For you" insights, six KPI tiles with change tag and sparkline), `AnalyticsActivity` (trend bars with metric chips and tap-to-pick, 17-week consistency calendar, hour and weekday rhythm, what you did), `AnalyticsStanding` (reach, helpfulness with tonal label tags, community, top posts, top resources, topics, milestones), `AnalyticsCharts` (canvas bars, sparkline, heat grid), `AnalyticsParts` (card, tile, tag, stat grid, bar row).
- Rules kept: flat tonal surfaces, no shadow, no gradient, no emoji, no circle tiles (Expressive cookie, sunny, flower, clover, burst shapes and 12 to 28 dp radii), brand primary for data, tonal chips for tags and deltas, bare text for everything else.

## Not done yet (after session 8)

- The screen has not been seen on a device or emulator: production still serves the old payload until the backend is deployed, so a capture flow would only show the "updating" state. After deploying, add a flow to `tools/app-screens/flows` (Profile, Analytics icon) and run `App screen captures (reel)`.
- PageView rows are not read for members (no index on the member column); likes and replies received come from notifications.

## Session 9: neutral surfaces, web composer, About (compile checked on the Kotlin front end)

Brief: the app still read blue next to the web (cards, popups, backgrounds), the comment bar had hint and type chips and a mic that the web does not have, there was no About screen, and none of the surface rules were written down for agents.

- **Palette:** `ANDROID_LIGHT_OVERRIDES` now pins the whole light surface ramp, `outline`, `outlineVariant`, `onSurface` and `onSurfaceVariant` to neutral greys (see the script). Dark is unchanged. `Palette.kt` regenerated, `--check` passes.
- **Floating surfaces:** `ui/theme/NebFloat.kt` (`nebFloatColor`, `nebFloatLine`) and `ui/components/NebMenu.kt` (`NebDropdownMenu`). Every `DropdownMenu` in the app is now `NebDropdownMenu`; `NebModalSheet`, `NebDialog`, the raw `ModalBottomSheet` and `AlertDialog` call sites take `nebFloatColor()`. White in light, hairline, no elevation.
- **Comment bar** (`CommentComposerBar.kt`): rebuilt as the web `neb-composer`. Collapsed: avatar with identity chevron, field, A tool, poll and attach tools, round send. Opened with A: markdown row on top (from `MarkdownToolbar`), field, tool row with the reply type tool, expand and send. The reply type is `ReplyKindSheet` (bottom sheet, tick on the current one). The chip row (`ReplyKindPicker`) is deleted, the mic button is gone (voice notes were reachable only through it; `voiceNote` is still accepted so a recording in progress shows its strip). New params `kind` and `onKindChange` on both overloads; Forum post detail passes them.
- **Identity menu:** white popup with hairline, uppercase section labels like the web.
- **About** (`ui/screens/about/AboutScreen.kt`, route `about`, Settings > About > About NEBians): hero with a morphing mark (cookie, sunny, flower, clover) that squeezes on tap and three lines that land one by one, four pillar cards with shape tiles, four steps, four promises, the team in their own expressive shapes (tap turns the shape), Consica Labs card with a mailto. Copy is `web/about_data.py`. Entrances use `Reveal`; reduced motion snaps. Team photos do not exist on the web either, so initials sit in the shapes.
- **Docs:** `AGENTS.md` ("Android surface and parity rules"), `docs/M3X_DESIGN_SYSTEM.md` section 11 and checklist item 13, `ANDROID_UI_CONTINUITY.md` marks the old mono contract superseded.
- **Compile check on the sandbox:** swap file 3 GB, JDK 17, SDK 36 in `/tmp`, `local.properties` and `app/google-services.json` (both git-excluded), then `./gradlew :app:compileModernDebugKotlin --no-daemon --no-parallel -Pkotlin.compiler.execution.strategy=in-process -Dorg.gradle.jvmargs=-Xmx2600m` takes under two minutes and prints every `e:` line.

## Not done yet (after session 9)

- Nothing here has run on a device. First look on hardware: the composer open and closed states, the kind sheet, the About hero morph, menus in light and dark.
- Some `surfaceContainerLow` fills on white pages (55 sites) are now very light grey instead of blue; if any card reads flat, give it the hairline card treatment instead of a darker fill.
- Replies in a thread sheet still post comments only (no type tool on nested replies, matching the API).

## Session 10: reading mode second pass, audit of the session 9 surface rules

Brief: session 9's brief repeated with "go all out". `main` already had the palette pin, `NebFloat`, the web composer and About, so this session audited first.

- Audit: no bare `DropdownMenu` outside `NebMenu.kt`; every `ModalBottomSheet` and `AlertDialog` takes `nebFloatColor()` (`NebPickerSheet` takes its picker palette's page colour, `AuthLegalSheet` pins white or near-black itself). No light bluish hex values are hard-coded outside data colours, simulations and festival art.
- Reading mode: see `PDF_ANDROID_STATUS.md` session 4.
- Toolchain on a 2 GB box with no swap and no root: the whole-module Compose compile is killed (exit 137) even with `-Xmx1200m`. Use a bigger pod, or rely on CI.

## Session 11: system bars, splash, toast, composer, notes (CI-verified only)

- **Edges:** `MainActivity` wraps the nav host in a box with `nebSafeSides()` (system bars as if shown, plus the display cut-out, horizontal only), so a side navigation bar or a camera cut-out in landscape never sits on a touch target. `NebSystemBars(darkIcons)` sets and restores the status and navigation icon colour per screen (used by the splash and the PDF viewer).
- **Splash:** about 1.2 s instead of 2.4 s (faster springs, shorter holds), and the status bar is no longer hidden and shown again, which moved the first screen by its height.
- **Toast:** `NebToast` / `NebToastHost` replace every `SnackbarHost`: inverse surface card, a tonal tile by kind (done, problem, info, picked from the message), optional action pill, a timer hairline, spring in, swipe sideways to dismiss. Same `SnackbarHostState` calls. `Toast.makeText` calls (15) are still the system toast.
- **Composer (`CommentComposerBar.kt`):** the profile picture moves into the formatting row, before the tools, while writing (no longer under them); every part slides and fades (`AnimatedVisibility`). One plus button (`ComposerAttachMenu`: image, PDF, audio, video, poll where the screen takes polls) replaces the attach and poll buttons in the forum and resource composers and on the web (`composer-plus.js`, `18-comment-composer.css`). News keeps the minimal bar (field and send, no attachments); its identity switcher is not done because the news comment API and view model have no anonymous option.
- **Notes:** both floating buttons are gone. A tonal plus tile ends the header, and the empty list shows floating paper cards with Write a note and Dictate.

## Session 12: audit of the reading, toast, composer brief (CI-verified only)

Brief: the reading mode / sheet / system bars / splash / composer plus / notes / toast brief came back again. Audit of `main` first (sessions 5 and 11 had done most of it); what was missing is below.

- **Toast everywhere:** `ui/components/NebToastBus.kt` (`Context.nebToast`, `NebToastBusHost` in `MainActivity`). All 15 `Toast.makeText` calls outside the crash screen now draw the `NebToast` card (any thread; falls back to the system toast only if no host is collecting).
- **News composer identity:** the news comment bar (not the thread bar) now has the identity avatar menu (you or anonymous) in the leading slot. `NewsCommentRequest.isAnonymous`, `NewsRepository.postComment(.., isAnonymous)`, `NewsDetailViewModel.composerAnonymous` plus the identity flows. The backend (`ajax_blog_comment`) already read `isAnonymous`; the earlier note that the API had no anonymous option was wrong. No media, no plus there.
- **Checked, unchanged:** Reading sheet matches the bento reference (sp values, no page colour names, thick visible sliders, scroll, zen and the other switches); splash 1.2 s; notes header plus tile and empty state with no floating buttons; backend `web.test_institutions` and `web.test_institution_sites` pass (30 tests).
- Not run on a device. Look for: a toast over the composer with the keyboard open, the news identity menu with a signed out user (disabled).
- CI: `Build Student Release APKs & AAB` passed on `517c9e9` (the first push `d9a6dcf` failed on one missing import of the `BoxScope` extension `NebToastBusHost`, fixed).

## Session 13: audit, one composer (CI-verified only)

Brief: the reading, sheet, bars, splash, composer, plus menu, notes and toast brief came back a third time. Everything in sessions 5, 11 and 12 was re-checked on `main` first and left alone.

- **One composer:** the full-screen reply page (`ReplyScreen`, `ReplyViewModel`, route `forum/reply`) had no caller left (the thread sheet and the main bar already use `NebCommentComposerBar`). Removed it and the unused `onReplyClick` parameter of `ForumPostDetailScreen`. `NebCommentComposerBar` is now the only comment input (forum post, forum thread, resource, resource thread, news).
- **Copy:** the home feed filter "All Feed" lost its decorative glyph.
- **Still open, in order of value:** two column papers and fact sheet grids in reading mode (`PDF_ANDROID_STATUS.md`), a device pass on the sheet, splash and toast.
