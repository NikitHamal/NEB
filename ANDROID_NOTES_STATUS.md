# Android Notes + on-device voice: status

Canvas is out of the app (routes, tab, home tile, settings and tools rows removed; the code in
`ui/screens/canvas/` stays, unreferenced). The bottom tab, the create menu, Home and Settings now point to **Notes**.

## What shipped

- **Notes** (`ui/screens/notes/`, Room table `notes`, DB v3, migration 2 to 3, `NotesRepository`). Offline only.
  - List: staggered grid or list, search, filters (All, Pinned, Archive, Bin), tag chips from the notes, sort (edited, created, title),
    long-press multi-select (pin, colour, archive, bin, restore, delete forever), undo snackbar, 30 day bin, checklist progress on cards.
  - Editor: borderless title, tags, Markdown body, autosave (500 ms) and flush on leave, undo/redo, list continuation on Enter,
    toolbar (bold, italic, heading, checklist, bullets, numbers, quote, code, divider), preview with tappable checkboxes,
    tonal colours (7), pin, archive, duplicate, share, word count, bin/restore.
  - Empty notes are never kept.
- **Speech to text: Cactus Whistle** (16.9 MB, 7 languages) on the Needle engine. `speech/WhistleEngine.kt`, JNI in
  `src/main/cpp/speech_jni.cpp`, prebuilt `libneedle.a` (arm64-v8a, armeabi-v7a) in `src/main/cpp/needle/`.
  Live dictation: 16 kHz mic, about one second per pass, committed words are inserted at the caret, the unconfirmed tail shows in the strip.
  The engine is process-global, so every call runs on one thread. Language: Auto or a fixed one.
- **Text to speech: Gradium Phonon 31m** (English, Apache-2.0, q8 GGUF, ~65 MB) through `libptts_ffi.so`
  (built by `.github/workflows/build-phonon-lib.yml`, committed in `src/main/jniLibs/arm64-v8a/`, opened with `dlopen`).
  `speech/PhononEngine.kt` reads a note sentence by sentence into an `AudioTrack` (float PCM 24 kHz): pause, resume, skip, stop, audio focus.
  The model is released after a quiet minute. Voices come from the public `gradium/phonon-voices` catalog (English), downloaded one by one, with preview.
- **Model management** (`speech/SpeechModelManager.kt`, screen `VoiceModelsScreen`): nothing is bundled. The user downloads or removes each
  model on demand; downloads resume (`.part` + Range), report progress, survive leaving the screen, check free storage. Using dictation or read aloud
  before the model exists opens a setup sheet that downloads it and then continues.
- Phonon 40m is CC BY-NC and gated, so it is not offered.

## Limits and decisions

- Phonon needs arm64 with ARMv8.2 dotprod + fp16 (checked in `/proc/cpuinfo`); otherwise the card says it is unsupported. Whistle works on arm64 and armv7.
  x86_64 builds a stub so emulators still install.
- Whistle has no unload call: removing the model deletes the file and the engine drops out of use; memory is returned when the process ends.
- Reading stops when the editor closes (no background service yet).
- Nothing here is built locally. The check is the GitHub Actions `Build Student Release APKs & AAB` run.

## Not done

- Background playback with a media notification; word-level highlight while reading; Nepali (neither model supports it).
- Notes sync to the account.
