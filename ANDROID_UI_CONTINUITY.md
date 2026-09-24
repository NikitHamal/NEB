# NEBians Android — UI/UX Revamp Continuity

**Last updated:** September 25, 2026
**Working branches:** `design/nebians-onboarding-experience` (issue #44, §4), then `design/profile-revamp` (§5)
**Scope:** the mono / Material 3 Expressive redesign of the Android app (GitHub issues #41–#44). This file is the handoff for that work; `CONTINUITY.md` covers the Django/web side and is unrelated.

---

## 1. Read this first: the design contract

These are the owner's stated preferences. They have been reasserted several times and violations get filed back as bugs.

- **Mono only.** Graphite/black/grey. No blue, no coloured accents in chrome, illustrations or empty states. Category colours exist in the data (`NewsAnnouncement.categoryColorHex`) but the UI deliberately ignores them now.
- **No excessive shadows, no glows, no orbiting dots, no decorative particles.**
- **No bullet/dot prefixes** in copy (e.g. never "• No links yet").
- **Minimal empty states.** A single static icon plus a line of text. Animated canvas art in empty states was explicitly rejected (issue #44).
- **Keep the liquid-glass bottom nav exactly as it is.** `ui/components/LiquidGlassNav.kt` is the owner's favourite component — do not restyle it.
- The two screens the owner likes most are the **auth screen** and the **home feed**; match their density and restraint.
- Material 3 **Expressive** tokens, shapes and components — not the old ones. `ButtonGroup` over `SegmentedButton`, no circular FABs, `*Emphasized` type styles for editorial moments.
- **Spring motion only.** Never `tween()`.

## 2. Design-system invariants (verified against the code)

**Motion** — `ui/theme/NebSpring.kt`: `nebFastSpatialSpec()`, `nebSpatialSpec()`, `nebSlowSpatialSpec()`, `nebFastEffectsSpec()`, `nebEffectsSpec()`. All are `@Composable fun <T> (): FiniteAnimationSpec<T>` and all collapse to `snap()` when `ANIMATOR_DURATION_SCALE == 0`. Spatial for position/size/shape, effects for colour/alpha. Never hardcode a spring or a tween.

**Press feedback** — `Modifier.nebPressable(enabled, scale, tactile, onClick)` in `ui/components/NebAuthPrimitives.kt`. It is `graphicsLayer` scale plus `clickable(indication = null)`: **there is no ripple anywhere in the house components.** If a reviewer reports "ripples", it is two containers cross-fading, not a ripple.

**Component signatures worth memorising** (getting these wrong is the most common compile break):
- `NebIconButton(icon, contentDescription, onClick, modifier, tint, size: Dp)` — no `enabled`, no `iconSize`.
- `NebEmptyState(icon, title, subtitle, modifier, action)` — now a *static* 64dp `surfaceContainerHigh` circle behind a 28dp icon.
- `NebButton(text, onClick, modifier, icon, tone: NebButtonTone, size: NebButtonSize, fillWidth, weight)`.
- `NebTabRail(tabs: List<NebRailTab>, selectedIndex, onSelect, modifier, accent, contentPadding)`; `NebRailTab(label, icon, count, showZero)`.
- `NebLoader(modifier, size: NebLoaderSize, color)` — `Inline(20)/Small(26)/Standard(36)/Screen(48)`.
- Shimmer: `ShimmerCard(modifier, shape, height)`, `ShimmerLine(modifier, widthFraction, height, shape)`, `ShimmerCircle(modifier, size)`. `ShimmerCard`/`ShimmerLine` call `fillMaxWidth()` internally.
- `MarkdownText(markdown, modifier, style, onLinkClick)`.

**Shapes** — `WebCardShape` 14dp, `WebPanelShape` 18dp, `WebPillShape` 999dp; `NEBiansShapes` in `ui/theme/Shape.kt` (6/10/14/20/28).

**House screen pattern** (copy `ui/screens/notifications/NotificationsScreen.kt`): `TopAppBar` with a two-line title `Column` (title `SemiBold` + `labelMedium` subtitle in `onSurfaceVariant`), back `IconButton`, `containerColor = surface`; then `NebTabRail`; then `PullToRefreshBox`; then a `LazyColumn` of hairline-separated rows with `dayBucket()` section headers; `NebEmptyState` for empty/error.

## 3. Platform constraints that have bitten before

- Kotlin 2.0.21, AGP 8.8.0, Gradle 8.11.1, KSP 2.0.21-1.0.28, Hilt 2.53.1, compileSdk/targetSdk 36, minSdk 24 (legacy) / 28 (modern), JDK 17.
- Compose BOM 2025.10.00, `material3:1.5.0-alpha10`, `material-icons-extended:1.7.8`.
- **No `coreLibraryDesugaring`, so `java.time` is unusable.** Use `java.util.Calendar` + `TimeUnit` (see `dayBucket()` in `NotificationsScreen.kt` and `BookmarksScreen.kt`).
- `@file:OptIn(...)` must sit *above* `package`. `*Emphasized` type styles need `ExperimentalMaterial3ExpressiveApi`.
- `ImageVector` is in `androidx.compose.ui.graphics.vector`. `positionInParent()` needs an explicit `androidx.compose.ui.layout.positionInParent` import.
- `@ReadOnlyComposable` + `remember` is illegal; `AnimatedContent`'s `transitionSpec` is not `@Composable`.
- Double bottom inset on composer bars is fixed with `WindowInsets.ime.exclude(WindowInsets.navigationBars)`.
- `ButtonDefaults.shapesFor(height)` **renders square at ≥56dp** (its two-argument branch supplies a pressed shape whose resting shape resolves oddly). Confirmed by `javap` on the material3 AAR. `NebButton` therefore states its own `ButtonShapes` — see §4.

## 4. What was delivered in the issue #44 session — all of it compiles

Both `:app:compileModernDebugKotlin` and `:app:compileLegacyDebugKotlin` are green.

**a) Reader formatting bug (the run-on text with literal `##`, `---`, `>`, `1.`).**
Root cause was in `data/repository/NewsRepository.kt`: the site returns raw markdown with real newlines, and `cleanArticleContent()` finished by passing the whole document through `Html.fromHtml(...)`, which treats newlines as insignificant whitespace and flattened every block into one line. Replaced with `String.decodeEntitiesPerLine()`, which decodes entities line by line and preserves block structure.

**b) Markdown renderer** (`ui/components/Markdown.kt`):
- new `MdBlock.Rule` block, parsed from `---` / `***` / `___` (`HorizontalRuleRegex`) and drawn as a 1dp hairline;
- h4/h5/h6 now parsed (previously only h1–h3);
- heading type scale retuned (`headlineSmall` / `titleLarge` / `titleMedium` / `titleSmall`);
- **new spacing engine** `layoutMarkdownBlocks()` → `List<MdSpacedBlock>` with `gapAfter()`/`gapBefore()` per block type, replacing the flat 4dp gap. Blank source lines fold into a ≥10dp gap instead of rendering as empty paragraphs.
- If you add a new `MdBlock` subtype, remember `markdownToInlinePreview()` has its own exhaustive `when`.

**c) "Two ripples when switching tabs"** (`ui/components/NebTabRail.kt`, rewritten, public API unchanged).
There was never a ripple. Each `NebRailItem` used to cross-fade its own fill/border *and* animate its own horizontal padding, so during a switch two pills were visible and the row reflowed. Now there is **one shared indicator**: children report their bounds via `onGloballyPositioned` into a `mutableStateMapOf<Int, Rect>`, and two `Animatable`s (`travel`, `span`) slide/stretch it with `nebSpatialSpec()`. Item padding is constant; items only cross-fade content colour. The rail also auto-scrolls the selected tab into view.

**d) Square "Show results" button in the filter dialog** (`ui/components/NebActionButtons.kt`).
`NebButtonSize` gained a `pressedCorner`, and a private `nebButtonShapes(size)` returns `ButtonShapes(shape = RoundedCornerShape(percent = 50), pressedShape = RoundedCornerShape(size.pressedCorner))`. `ButtonDefaults.shapesFor(height)` is no longer used. This fixes every `Hero`/`Feature`-sized button app-wide, `FilterDialog.kt` included.

**e) Minimal empty states.**
- `NebEmptyState` no longer draws the breathing `NebIconHalo`; it is a static circle. `NebIconHalo` was deleted from `ui/components/art/NebStateArt.kt` (it had exactly one call site).
- `ResourceEmptyComments()` in `ui/screens/resource/ResourceDetailComponents.kt` dropped `NebStateArt(NebStateKind.Empty)` for a 26dp `ChatBubbleOutline`.
- The news reader's no-comments state is now an unboxed icon + two lines (was a bordered `Surface`).
- `NebStateArt` still exists and is still used by `UploadDetails.kt:281` (`Success`). Leave that one alone unless asked.

**f) Bookmarks, fully redesigned** — split into three files to honour the 500–600-line rule:
- `ui/screens/bookmarks/BookmarksViewModel.kt` — `BookmarkKind` enum (All/Posts/Replies/Resources), `BookmarksUiState` with `visibleItems`/`countOf()`, parallel `enrichBookmark()` fan-out, and a new **optimistic `remove()` + `undoRemove()`** pair driving a snackbar with Undo. Un-saving calls `toggleBookmark(token, BookmarkToggleRequest(targetType, targetId))`; a failure restores the pre-removal snapshot.
- `ui/screens/bookmarks/BookmarksScreen.kt` — house `TopAppBar` ("Bookmarks" / "N saved"), `NebTabRail` with live per-type counts, `PullToRefreshBox`, day-bucketed `LazyColumn`, shimmer skeletons instead of a centred spinner, per-filter empty copy.
- `ui/screens/bookmarks/BookmarksContent.kt` — `BookmarkRow` (42dp rounded-square mono glyph, grey kicker line, title, excerpt, trailing filled-bookmark un-save), `BookmarkSectionHeader`, `BookmarkRowSkeleton`.
- Call site unchanged: `ui/Navigation.kt` `Screen.Bookmarks`.

**g) Blogs list, redesigned** (`ui/screens/news/NewsScreen.kt` + new `ui/screens/news/NewsListContent.kt`).
Editorial index rather than a stack of bordered cards: house `TopAppBar` ("Blog" / "News, notices and updates"), `NebTabRail` over `NewsCategories`, then `NewsLeadStory` (16:10 cover, `headlineSmall` headline, standfirst) followed by `NewsIndexRow`s (text left, 96dp thumbnail right, hairline divider). Pinned shows as a small `PushPin` glyph on the kicker line, not a coloured pill. Shimmer skeletons via `NewsIndexSkeleton(lead)`. Pull-to-refresh is wired through `viewModel.retry()` with `isRefreshing` cleared by a `LaunchedEffect(uiState.isLoading)` because `NewsViewModel.retry()` returns `Unit`, not a `Job`.
`NewsScreen`'s `onNotificationsClick` / `onProfileClick` params are now unused but kept so `Navigation.kt` needn't change.

**h) Blog reader, redesigned** (`ui/screens/news/NewsDetailScreen.kt`).
Real `TopAppBar` (category label as the title, back, a direct Share action — the `⋮` `DropdownMenu` is gone, and so is the redundant "Share this article" button in the body). New editorial `NewsArticleHeader`: uppercase category kicker, `headlineMedium` `SemiBold` headline, `bodyLarge` standfirst at 27sp leading, byline row, rule. Cover moved below the header at 16:10 with 18dp corners. Body copy is `bodyLarge` at **30sp line height inside 20dp side padding** for a readable measure. "Read the original" is an outlined button; related articles reuse `NewsIndexRow`; the skeleton is shimmer-based. The comment-thread `NebModalSheet` and `safeOpenUri()` were left untouched.

## 5. What was delivered in the profile session — all of it compiles

Both `:app:compileModernDebugKotlin` and `:app:compileLegacyDebugKotlin` are green. Asked for: finish §6's open list, redesign the reply cards, fix the Resources tab, redesign the whole profile screen.

**a) The Resources tab bug ("No activity yet" for everyone).**
Not an empty-list bug — a **decode failure**. The two backend resource serialisers disagree about `price`: `backend_python/api/serializers.py:206` emits it as a string (`"150"`), `backend_python/web/view_helpers.py:222` (`_serialize_resource`) emits the raw float (`150.0`). `ApiResource.price` is a Kotlin `String`, and `coerceInputValues` rescues `null`, **not** a type mismatch, so `decodeString()` threw; because kotlinx decodes the whole response in one pass, one unquoted number emptied the entire list, and `ProfileViewModel.loadResources()`'s silent `catch` turned that into a permanent "No activity yet".
Fixed **client-side** in new `data/api/LenientSerializers.kt`: `object LenientStringSerializer : KSerializer<String>` takes whatever primitive arrives, strips a trailing `.0`, and maps `JsonNull`/non-primitives to `""`. Applied with `@Serializable(with = ...)` on `ApiResource.price`. The client fix works against the already-deployed backend and against both serialisers.
**The backend was deliberately left alone.** Four Django templates (`_home_suggested.html`, `_library_content.html`, `resource_detail.html`, `admin_panel/resources.html`) consume `{{ r.price|floatformat:"0" }}`, so normalising `view_helpers.py` to a string would change web rendering. If someone does unify them later, the lenient serialiser still works.

**b) Per-tab error state**, so no future parse or network failure can masquerade as an empty tab. `ProfileUiState` gained `postsError` / `repliesError` / `resourcesError`; each loader clears its field on start and on success and sets `ApiErrorMapper.mapException(e)` in the `catch`. The tab then draws a `NebEmptyState` plus a "Try again" button instead of the empty-state copy.

**c) The whole profile screen, rebuilt.** `ui/screens/profile/ProfileComponents.kt` (1197 lines, every screen-level card) was **deleted** after grepping every symbol in it; replaced by four focused files. `ProfileScreen`'s public signature is unchanged, so `Navigation.kt` needed no edit.
- `ProfileScreen.kt` — solid house `TopAppBar` instead of the old transparent overlay with black scrim circles; the title cross-fades in via `derivedStateOf` on `listState` scroll. `PullToRefreshBox` → `ProfileBody`. One private `LazyListScope.feedSection(...)` now drives all three tabs in a fixed order (skeletons on first load → error + retry → empty state → rows → trailing loader / inline retry / "Show more"), which is why the tabs finally behave identically. The tab rail is a `stickyHeader`. All four dialogs are preserved verbatim.
- `ProfileHeader.kt` — full-bleed 160dp banner with the avatar overhanging it (`offset(y = 40.dp)` inside an unclipped `Box`, repaid by a 48dp spacer), primary action beside the avatar, inline stats row, meta rows, achievement pills, social links, and `ProfileHeaderSkeleton`. Bot profiles render `NebyAvatar(animation = "idle", size = 84.dp, interactive = true)`.
- `ProfileRows.kt` — `ProfilePostRow`, **`ProfileReplyRow`**, `ProfileResourceRow`, plus skeletons. The reply redesign was the explicit ask: the old card put "Reply on {post title}" in bold on top and the reply body in grey underneath, which inverted the two — you had to read past the heading to find out what the person said. Now the context line is quiet ("Replied to **{title}**") and the reply body is the loud part, with a hairline spine down the left tying them together the way a thread does.
- `ProfileAbout.kt` — card-free About tab: an ACTIVITY section and a DETAILS section of label/value rows separated by hairlines. The old progress card is **gone**; it drew three bars hard-coded to zero, so it told every visitor the same untrue thing.
- `ProfileFormatting.kt` holds the pure text helpers (`formatRoleHeadline`, `shortProvince`, `parseAchievements`, `plainTextPreview`, …) so the screen files stay about layout.

**d) The §6.1 sweep, on the two screens named by name.**
- `ui/screens/analytics/AnalyticsScreen.kt` — `WebTopBar` → house `TopAppBar`; `WebEmptyState` → `NebEmptyState` + `NebButton("Try again")`; the bordered `AnalyticsCard` became `AnalyticsSection` (a plain band with a hairline under it, because nine bordered panels on a padded list read as nine unrelated boxes); `ChartLegend`/`LegendItem` deleted (four labels for a one-series chart); every `primary` / `primaryContainer` / `onPrimaryContainer` swapped for `onSurface` / `onSurfaceVariant` / `surfaceContainerHigh`, and both `LinearProgressIndicator`s given an explicit mono `color`.
- `ui/screens/downloads/DownloadsScreen.kt` — rewritten to the `BookmarksScreen` row idiom: `NebEmptyState`, "N saved" subtitle, 42dp rounded-square glyph tile, `nebPressable`, `NebIconButton` delete, hairline divider inset to 74dp. No `Card`, no `BorderStroke`, no `primary` tint.

**e) §6.3, the reader's comment loading skeleton** (`ui/screens/news/NewsDetailScreen.kt`). It was two flat grey boxes inside a `WebCardShape` `Surface`, which reads as content rather than as absence. Replaced with `NewsCommentSkeleton()` — `ShimmerCircle` + three `ShimmerLine`s in the `BookmarkRowSkeleton` idiom. Note `ResourceCommentsLoading()` in `ResourceDetailComponents.kt` is a centred `NebLoader` and was **not** the hand-rolled one; don't go looking for it there again.

**f) Encoding repair.** `NewsDetailScreen.kt` contained three raw cp1252 bytes (`0x97` em dash, two `0xb7` middle dots) — one in a comment and two in `bylineTail`'s `joinToString(" · ", prefix = "· ")`. The Kotlin compiler reads source as UTF-8, so the byline was rendering replacement characters at runtime. Rewritten as proper UTF-8. `app/src/main/java` is now clean; the check is a two-line `os.walk` + `decode('utf-8')`.

## 6. Still open

1. **The rest of the `WebTopBar` / `WebEmptyState` sweep.** 13 files still call them:
   `ui/screens/study/StudySpaceScreen.kt`, `StudyLabScreen.kt`, `StudyDocumentDetailView.kt`, `ui/screens/library/LibraryScreen.kt`, `SyllabusScreen.kt`, `SyllabusSubjectDetailContent.kt`, `InteractiveLibraryContent.kt`, `ui/screens/home/HomeScreen.kt`, `ui/screens/ai/NebyAiScreen.kt`, `ui/screens/forum/ForumScreen.kt`, `ui/screens/results/ToolsScreen.kt`, `ResultCheckerScreen.kt`, `ui/screens/canvas/CanvasListScreen.kt`.
   **Read this before starting:** on Home / Library / Forum, `WebTopBar` is not legacy chrome — it is the app's intentional global bar (greeting, avatar, notification badge, `TopBarViewModel`). Swapping it for a plain `TopAppBar` there would be a regression, not a cleanup. Only the `WebEmptyState` call sites and the genuinely secondary screens are in scope; ask the owner before touching the three main tabs.
2. **Visual verification.** Nothing in §4 or §5 has been seen on a device — only compiled. There is no emulator or screenshot path in this environment, so this cannot be closed here. `assembleModernDebug` and a screenshot pass on real hardware is the next sanity check, and it is the only remaining unknown for the profile rewrite.

## 7. Build and push mechanics

**Build.** The environment does not export these; set them every time:

```bash
export JAVA_HOME=/workspace/tools/jdk PATH=/workspace/tools/jdk/bin:$PATH
export ANDROID_HOME=/data/workspace/android-sdk        # no local.properties in the repo
cd /data/workspace/NEB
KEYSTORE_PASSWORD=android KEY_PASSWORD=android KEY_ALIAS=neb \
  ./gradlew :app:compileModernDebugKotlin :app:compileLegacyDebugKotlin \
  -Dorg.gradle.jvmargs="-Xmx4g -XX:MaxMetaspaceSize=768m -Dfile.encoding=UTF-8"
```

Compile **both** variants; they have different minSdk and catch different things. `./gradlew --stop` first if a daemon is wedged, and put the keystore vars on the same command line (changing them invalidates the configuration cache). `assembleModernDebug -x lint` for an APK. `javap` needs `PATH=/workspace/tools/jdk/bin:$PATH`.

**Push.** There are no git credentials in this environment and the local `.git` HEAD is far behind the remote, so **never trust `git status` to tell you what changed**. Pushing goes through the GitHub Git Data API via the connector:

```bash
actl connector call github --url https://api.github.com/repos/NikitHamal/NEB/...
```

`/tmp/push3.py` automates blob → tree → commit → ref against `PARENT` (update it to the current remote branch tip before each run) reading paths from `/tmp/files.txt` and deletions from `/tmp/deleted.txt`. Track the files you touch as you go and write that list by hand; `/tmp/diffremote.py` has produced bogus mass-deletion lists before.

**Never commit:** `google-services.json`, `app/google-services.json`, `nebians-release.keystore`, `local.properties`, `.env*`, `*.pem`, `Resources/`, `.secrets.local.json`, `client_secret_*.json`, `nebiansnepal-firebase-adminsdk-*.json`, `firebase-service-account.json`. The locally generated dummy keystore and placeholder `google-services.json` exist only to let the build run and are gitignored — keep it that way. `.claude/` and `skills-lock.json` are deliberately excluded from every push.

## 8. Earlier issues in this arc (for context)

- **#41** — post/forum detail KaTeX crash on "see more"; upload screen revamp; Neby credits minimalism; WhatsApp button without the number; better "People you may know" suggestions with follow-back.
- **#42** — delivered as `6844e864`.
- **#43** — delivered as `592ac588`, then a follow-up comment delivered as `6b78500f` + `1a8404f0` (white canvas background on both web and Android).
- Process lesson that still applies: **every scripted replacement must assert its match count.** A silent no-op `sed` caused a regression in #42. The Python edits in this session all `assert s.count(old) == 1`.
