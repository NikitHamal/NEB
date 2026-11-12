# Splash, About, avatars, Notes, Upload, toasts: status

The one status doc for this batch. Read it first, extend it, do not start a second one.
Nothing under `app/` is built locally (no JDK or SDK in the agent sandbox). The check is the GitHub Actions Android build.

## Done

| # | What | Where |
| --- | --- | --- |
| 1 | **Splash**: the shape takes over the screen, the mark drops in, the name is cut in letter by letter. Nothing orbits the logo any more. | `ui/screens/auth/SplashScreen.kt` |
| 2 | **About**: poster, version tiles (version info lives here now), team, open source and on-device model credits (Whistle, Phonon, Needle, and the libraries). No scroll-driven motion, it fills the screen. Settings lost the separate version card and keeps one About row. | `ui/screens/about/AboutScreen.kt`, `SettingsScreen.kt` |
| 3 | **No generated avatars**: Blobatar, Neby avatar engine, avatar studio, avatar API routes and options removed on web, API and Android. A profile with no photo shows the initial in a neutral disc (`Avatar`, `neb-letter`). Admin bot avatar presets (dicebear) removed too. | `api/services.py`, `web/view_helpers.py`, `test_no_generated_avatars.py`, `admin_panel/user_detail.html` |
| 4 | **Toasts lose the progress bar** on web (`neb-toast.js`, `app-toast.css`) and Android (`NebToast.kt`). | |
| 5 | **Notes**: block editor with toggle lists, nested indent, slash menu with icons, starter templates, large title. New: **drag to reorder**. Every block has a drag handle (shown on the focused text block and on media blocks); the block follows the finger, the blocks it passes slide aside, and the drop moves it with everything nested under it (`NoteEditorViewModel.moveBlock`). | `ui/screens/notes/NoteBlockEditor.kt`, `NoteEditorViewModel.kt` |
| 6 | **Upload (Android)**: three pill stepper (the open pill carries its name, finished steps become ticks and tap back), steps slide in the direction you are going, no captions. Source step: a full width Scan tile with a morphing shape behind it, Gallery and Files in their own tones and glyph shapes, page strip items animate in and out. Publishing covers the screen with a morphing shape, the percentage and a flat bar (no bar in the bottom of the screen). Success screen: morphing shape and a tick, spring in. | `ui/screens/upload/UploadChrome.kt`, `UploadScreen.kt`, `UploadSource.kt`, `UploadDetails.kt` |

| 7 | **Compile fix**: `nebSpatialSpec()` / `nebEffectsSpec()` are composable; the upload stepper, step body and success screen called them inside `transitionSpec` / `LaunchedEffect` lambdas (CI run on 2149719 failed). They are hoisted into composable scope now. Rule: read a motion spec in the composable body, pass the value into the lambda. | `UploadChrome.kt`, `UploadScreen.kt`, `UploadDetails.kt` |
| 8 | **Notes: auto scroll while dragging.** Hold a block within 96dp of the top or bottom of the note and the page scrolls under it, faster nearer the edge; the block keeps following the finger. `BlockReorder` now owns the viewport edges and the finger position; `NoteEditorScreen` creates it and hands it to `NoteBlockEditor`. | `NoteBlockEditor.kt`, `NoteEditorScreen.kt` |

| 9 | **Notes: page icon and cover** (session 4). Room 4 to 5 adds `icon` (key into `NoteIcons`, 31 vector glyphs, no emoji) and `cover` (0 none, 1..8 flat tonal banners built from two big Material shapes). The editor header runs the cover edge to edge, the icon tile overlaps its lower edge, and a bare page shows quiet "Add icon" / "Add cover" actions; changing a cover springs its shapes in. Pickers are bottom sheets, also in the overflow menu. Note cards show the cover strip and icon. Duplicate copies both. | `NotePage.kt`, `NoteEntity.kt`, `DatabaseMigrations.kt`, `NoteEditorScreen.kt`, `NotesScreen.kt`, `NoteEditorViewModel.kt`, `NotesRepository.kt` |

## Next

- Notes: cover from a photo, page templates gallery in the empty state.
- Web upload composer is untouched in this batch (it already follows the `.fe` surface, see `UPLOADS_SELLING_STATUS.md`).

## Rules kept

No shadows, no emojis, no gradients, no ring on photos, no fills on role badges, no hover that squares a rounded button.

## Verified (session 3)

- Django suite: 908 tests OK (`cd backend_python && DEBUG=True DB_ENGINE=sqlite python3 manage.py test`).
- No leftover generated-avatar code or options (searched Kotlin, Python, templates, JS). Neby the AI bot keeps its mascot, it is a bot identity.
- No timer line left in `NebToast.kt`, `neb-toast.js`, `app-toast.css`.
- `docs/M3X_DESIGN_SYSTEM.md` now carries the rules from this batch: toast without progress, no generated avatars, splash, About, no scroll motion on Android, upload stepper.

## Verified (session 4)

- Django suite: 908 tests OK. Android CI build green on `df8c395` (Room 5, note icon and cover).
- Splash, About, avatar removal, toast without progress and upload stepper were re-checked in the code and left as built in sessions 1 to 3.
