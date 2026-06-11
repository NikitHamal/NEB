# Consica Code (Ccode)

A modern, offline-first, Material Design 3 educational coding playground for learners
aged 8–18/19. Learners grow digital ecosystems by writing real Python and HTML —
guided by **Terra the Owl** through the **Eco-Logic** design system.

- **Package:** `com.consica.code`
- **Stack:** Kotlin · Jetpack Compose · Material 3 · Room · DataStore · Navigation Compose
- **Min SDK:** 26 · **Target SDK:** 35

## Highlights

- **Age-adaptive experience** — onboarding asks for age group (8–12 / 13–16 / 16+),
  goal, experience, theme intensity and interests; the entire app adapts tone, tools,
  editor complexity, rewards and guidance.
- **Biome Map** — a vertical nature path of lessons across four biomes
  (Forest Floor → Sunny Meadow → Riverbank → Canopy) with locked/active/completed nodes.
- **Green-Code Playground** — dark high-contrast editor with live syntax highlighting,
  custom snippet keyboard (kid + professional layouts), line numbers, run history,
  workspace saving, and a Grow/Run button that adapts to age.
- **Offline Python** — a sandboxed MiniPython interpreter written in Kotlin
  (variables, math, strings, lists, if/elif/else, loops, functions, 15+ builtins,
  bounded execution). No network, no external runtime.
- **Offline HTML preview** — sandboxed WebView (JavaScript disabled, network blocked).
- **Drag-and-drop puzzles** — native Compose long-press drag reorder with accessible
  arrow-button fallback, decoy blocks for advanced puzzles.
- **Rewards** — XP, levels, badges, streaks, sun coins, water drops, mastery points,
  path certificates, leaf confetti and Terra celebrations.
- **Progressive unlocking** — professional tools unlock by mastery, or instantly via
  the parent/guardian switch in Settings.
- **Localization-first** — every user-facing string (including all lesson content)
  lives in `strings.xml`, ready for `values-ne/` Nepali resources later.
- **Accessibility** — high-contrast theme, reduced motion, large touch targets,
  content descriptions, scalable typography.

## Build

Open the `consica-code/` folder in Android Studio, or:

```bash
cd consica-code
./gradlew assembleRelease   # signed with the bundled dev keystore
./gradlew assembleDebug
```

### Signing

A development/release keystore is bundled at `ccode-release.keystore`
(PKCS12, alias `ccode`, password `ccode123`) so the project builds out of the box
and produces reproducible signed APKs in CI. Override via env vars
`CCODE_KEYSTORE_PASSWORD` / `CCODE_KEY_PASSWORD` for production use.

### CI

`.github/workflows/build-ccode.yml` builds a single signed release APK on every push
touching `consica-code/**` (plus manual dispatch) and uploads it as
`ConsicaCode-v<version>-<commitHash>.apk`.

## Project layout

```
consica-code/app/src/main/java/com/consica/code/
├── CcodeApp.kt / MainActivity.kt / AppContainer.kt
├── core/
│   ├── designsystem/      # Eco-Logic theme: colors, type (Fredoka/Nunito/Fira Code), shapes
│   └── model/             # Domain models (lessons, challenges, puzzles, badges)
├── data/
│   ├── content/           # LessonCatalog (31 lessons) + BadgeCatalog
│   ├── local/             # Room: progress, workspaces, badges, run history
│   ├── prefs/             # DataStore: onboarding, settings, stats, streaks
│   └── repo/              # LearningRepository, WorkspaceRepository
├── runtime/
│   ├── python/MiniPython.kt    # offline Python interpreter
│   ├── html/HtmlSupport.kt     # tag checks + safe preview wrapper
│   ├── highlight/              # syntax highlighter
│   └── ChallengeValidator.kt   # declarative challenge checks
├── ui/
│   ├── character/         # TerraAvatar (Canvas owl) + CharacterGuide
│   ├── common/            # EcoCard, StatChip, LeafConfetti, skeletons, offline banner
│   ├── ecosystem/         # HtmlPreview, ConsolePanel, GrowingPlant, DryPlant
│   ├── navigation/        # Routes + bottom nav
│   └── screens/           # onboarding, home (biome map), lesson, playground,
│                          # ecosystem result, puzzle, rewards, workspaces, settings
└── util/                  # SoundManager, ConnectivityObserver, TimeFormat
```
