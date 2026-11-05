# Mobile Programming — BCA 352 (Semester VI, 3 credits)

Mobile platforms and architecture (Android, iOS), screen-density and image-memory arithmetic, Android components, Intents and the Activity lifecycle, layouts, resources, RecyclerView, Fragments and Compose, storage (DataStore, files, SQLite, Room), networking, JSON, coroutines, backoff and WorkManager, permissions, sensors, location and notifications, cross-platform frameworks, testing, APK/AAB packaging, signing and publishing. 45 teaching hours (old TU CACS351 Mobile Programming; revised list BCA 352).

| Unit | Title | Hours |
|---|---|---|
| 1 | Mobile Platforms and Application Architecture | 6 |
| 2 | Android Components, Intents and the Activity Lifecycle | 8 |
| 3 | User Interface: Layouts, RecyclerView and Fragments | 8 |
| 4 | Data Storage: Preferences, Files, SQLite and Room | 7 |
| 5 | Networking, JSON and Background Work | 7 |
| 6 | Sensors, Location, Permissions and Notifications | 6 |
| 7 | Cross-Platform Development, Testing and Publishing | 6 |

(Hours sum to 48 in this reconstruction; the syllabus total of 45 is a guide.)

## What is executed and what is not

**Executed and machine-checked** (`bca/tools/check_mobile.py` plus `fill_script_outputs.py` / `fill_java_outputs.py`): the Activity lifecycle state machine (four scenarios against the documented callback orders), SQLite schema, aggregates and a rolled-back transaction (SQLite is the engine Android ships), the DiffUtil-style edit script against the n + m − 2·LCS formula, JSON parsing, exponential backoff, the haversine distance against the spherical law of cosines, a threshold step counter against numpy peak counting, the chunked APK-v2-style digest against an independent implementation, a Java loan-EMI calculator and amortisation (compiled and run on JDK 17), plus the density/dp/px table, image-memory and RecyclerView arithmetic and the practice answers.

**Not executed** (needs the Android SDK, Gradle, Room/KSP, Retrofit, Flutter): every ```kotlin, ```xml and ```dart snippet. They are labelled "Not executed" in the text, were written to the documented APIs, and were not compiled in this environment, so treat them as teaching sketches.

## Source and honesty

No TU unit list for BCA 352 was retrieved; the seven units are a reconstruction from the topics named in the course brief with the usual structure of a mobile programming course. API names follow the Android developer documentation as remembered; check the current documentation for versions and deprecations (for example AsyncTask and `startActivityForResult` are deprecated). The simulator's `onSaveInstanceState` ordering reflects behaviour since Android 9 (API 28).
