---
subject: Mobile Programming
grade: BCA Semester 6
unit: 2
title: Android Components, Intents and the Activity Lifecycle
hours: 8
area: BCA 352 · Mobile Programming · Unit 2
---

An Android app is not one program with a `main` function; it is a *collection of components* that the operating system creates, pauses and destroys as the user moves around, takes a call or rotates the phone. The programmer does not control when the app is running; the system calls the app's **lifecycle callbacks** and the app must respond correctly. This unit describes the four component types, the manifest that declares them, the **Intent** messages that connect them, and the Activity lifecycle, which you will see executed in a small simulator whose call sequences were checked against the documented lifecycle for launch, navigation, back and rotation.

::: key What this unit gives you
- The four component types and the role of AndroidManifest.xml.
- Explicit and implicit Intents, Intent filters, extras and results.
- The Activity lifecycle, task/back stack, configuration changes and saving state.
- A runnable lifecycle simulator.
:::

## 2.1 Application components

| Component | What it is | Example |
|---|---|---|
| **Activity** | One screen with a user interface | The login screen; the list of notes |
| **Service** | Work without UI that continues in the background | Playing music, uploading a file |
| **BroadcastReceiver** | Responds to system-wide or app announcements | "Battery low", "boot completed", "network changed" |
| **ContentProvider** | Shares structured data between apps through a URI interface | Contacts, the media store |

All are declared in **AndroidManifest.xml** (except dynamically registered receivers). Not executed (needs the Android SDK):

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <application android:label="@string/app_name" android:icon="@mipmap/ic_launcher">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        <activity android:name=".DetailActivity" android:exported="false" />
        <service android:name=".SyncService" />
    </application>
</manifest>
```

The **MAIN/LAUNCHER** filter makes MainActivity the app's entry point on the launcher. `exported` says whether other apps may start the component (required to be explicit on recent versions; keep it false unless needed, a security rule). Components are started by the system; they must not be created with `new`.

## 2.2 Intents

An **Intent** is a message object that asks the system to start a component or deliver a broadcast. It carries an **action**, optional **data** (a URI and MIME type), **categories**, **extras** (key–value pairs) and flags.

- **Explicit Intent:** names the target component class: start my DetailActivity.
- **Implicit Intent:** describes an action, and the system finds components whose **intent filters** match: *view a web page*, *dial a number*, *share text*, *take a photo*. If several match the user chooses (a *chooser*).

Not executed (needs the Android SDK):

```kotlin
val explicit = Intent(this, DetailActivity::class.java)
explicit.putExtra("note_id", 42)
startActivity(explicit)

val dial = Intent(Intent.ACTION_DIAL, Uri.parse("tel:+9779800000000"))
startActivity(dial)

val share = Intent(Intent.ACTION_SEND).apply {
    type = "text/plain"
    putExtra(Intent.EXTRA_TEXT, "Namaste from my app")
}
startActivity(Intent.createChooser(share, "Share via"))
```

To get a result back, use the **Activity Result API** (`registerForActivityResult`) instead of the older `startActivityForResult`; the second activity returns data with `setResult`. A **PendingIntent** hands another app (the notification manager, the alarm manager) the right to fire an Intent later on your behalf. **Extras** must be small (they travel through Binder with a size limit of about one megabyte for the whole transaction), so pass an *ID* and reload the data rather than passing a large object.

## 2.3 The Activity lifecycle

An Activity moves through states as it becomes visible, loses focus, is hidden and is destroyed. The system calls one callback on each transition:

| Callback | Called when | Typical work |
|---|---|---|
| `onCreate(Bundle?)` | The activity is first created | Inflate the layout, create view models, restore saved state |
| `onStart()` | Becoming visible | Start things the user sees |
| `onResume()` | In the foreground and interactive | Start animations, camera, sensors |
| `onPause()` | Losing focus (another activity partly covers it) | Pause what must not run in the background; save light state quickly |
| `onStop()` | No longer visible | Release heavy resources; save data |
| `onRestart()` | Coming back from stopped to started | Rare |
| `onDestroy()` | Being finished or destroyed by the system | Final cleanup |

The three nested loops: the **entire lifetime** runs from `onCreate` to `onDestroy`; the **visible lifetime** from `onStart` to `onStop`; the **foreground lifetime** from `onResume` to `onPause`. **`onSaveInstanceState(Bundle)`** is called (after `onStop` on current versions) so that the activity can store small UI state, which comes back as the Bundle in `onCreate`.

### A lifecycle simulator

The Python program below models the legal state transitions of an Activity and a small back stack, and replays four scenarios. Calling a callback that is illegal in the current state raises an error. The printed sequences are compared by the checker with the sequences documented in the Android guide for launch, opening B on top of A, pressing Back from B, and rotating A (on current Android versions `onSaveInstanceState` follows `onStop`).

```python
LEGAL = {
    "NONE": {"onCreate": "CREATED"},
    "CREATED": {"onStart": "STARTED", "onDestroy": "DESTROYED"},
    "RESTARTING": {"onStart": "STARTED"},
    "STARTED": {"onResume": "RESUMED", "onStop": "STOPPED"},
    "RESUMED": {"onPause": "PAUSED"},
    "PAUSED": {"onResume": "RESUMED", "onStop": "STOPPED"},
    "STOPPED": {"onRestart": "RESTARTING", "onDestroy": "DESTROYED",
                "onSaveInstanceState": "STOPPED"},
}
log, stack = [], []

class Activity:
    def __init__(self, name):
        self.name, self.state = name, "NONE"

def call(act, cb):
    act.state = LEGAL[act.state][cb]
    log.append(act.name + "." + cb)

def launch(a):
    for cb in ("onCreate", "onStart", "onResume"):
        call(a, cb)
    stack.append(a)

def open_new(b):
    top = stack[-1]
    call(top, "onPause")
    for cb in ("onCreate", "onStart", "onResume"):
        call(b, cb)
    call(top, "onStop")
    call(top, "onSaveInstanceState")
    stack.append(b)

def back():
    top = stack.pop()
    below = stack[-1]
    call(top, "onPause")
    for cb in ("onRestart", "onStart", "onResume"):
        call(below, cb)
    call(top, "onStop")
    call(top, "onDestroy")

def rotate():
    top = stack.pop()
    for cb in ("onPause", "onStop", "onSaveInstanceState", "onDestroy"):
        call(top, cb)
    launch(Activity(top.name))

def show(label, fn, *args):
    log.clear()
    fn(*args)
    print(label + ": " + " -> ".join(log))

A, B = Activity("A"), Activity("B")
show("Launch A", launch, A)
show("A opens B", open_new, B)
show("Back from B", back)
show("Rotate A", rotate)
```
```output
Launch A: A.onCreate -> A.onStart -> A.onResume
A opens B: A.onPause -> B.onCreate -> B.onStart -> B.onResume -> A.onStop -> A.onSaveInstanceState
Back from B: B.onPause -> A.onRestart -> A.onStart -> A.onResume -> B.onStop -> B.onDestroy
Rotate A: A.onPause -> A.onStop -> A.onSaveInstanceState -> A.onDestroy -> A.onCreate -> A.onStart -> A.onResume
```
The **back stack** is the key to the second and third lines: B is pushed on top of A, A is *stopped but kept*, and Back pops B and restarts A, which goes through `onRestart` instead of `onCreate`. The last line shows the surprise that surprises every beginner: **rotating the screen destroys the activity and creates a new one** because the configuration (orientation, language, font scale, dark mode) changed and the resources may differ.

## 2.4 Configuration changes and saving state

Three levels of state survive different events:

| What | Survives rotation? | Survives process death? | Use for |
|---|---|---|---|
| Fields in the Activity | No | No | Nothing important |
| **`onSaveInstanceState` Bundle** | Yes | Yes (while the task is alive) | Small UI state: scroll position, typed text, selected tab |
| **ViewModel** (Jetpack) | Yes | No | Screen data and logic, loaded data, ongoing requests |
| **Persistent storage** (Unit 4) | Yes | Yes | The user's real data |

A **ViewModel** is created for the activity's scope and survives configuration changes, so the data loaded from the network is not fetched again after a rotation; combine it with `onSaveInstanceState` (or `SavedStateHandle`) for process death. Declaring `android:configChanges="orientation|screenSize"` makes the system *not* recreate the activity, but you then handle the change manually; this is discouraged except for specific cases such as video players.

## 2.5 Tasks, back stack and launch modes

A **task** is the stack of activities a user visits while doing one job; pressing Back pops the top. Launch modes in the manifest or Intent flags change how new instances are handled: **standard** (a new instance every time, even if one is already on top), **singleTop** (reuse the top instance if it is the same type, calling `onNewIntent`), **singleTask** (one instance in the task, clearing the activities above it) and **singleInstance** (alone in its own task). A notification that opens a chat screen should typically use *singleTop* so that tapping repeatedly does not pile up copies.

## 2.6 Services, receivers and providers in outline

- A **started service** runs until it stops itself; a **bound service** offers an interface to clients and lives while they are bound; a **foreground service** shows an ongoing notification and may run long tasks (music, navigation). Modern Android restricts background services heavily, so deferrable work uses **WorkManager** (Unit 5).
- A **BroadcastReceiver** is a short-lived callback (it must finish quickly); many system broadcasts must now be registered at runtime and not in the manifest to protect battery. Local broadcasts and observable flows replace most in-app broadcasts.
- A **ContentProvider** offers a *table-like* interface over a URI such as `content://contacts/people/5`; apps query it through a **ContentResolver**. Apps rarely write their own, but the Contacts, MediaStore and Calendar providers are used constantly, and `FileProvider` shares files safely.

## Chapter summary

- An app is a set of components (Activity, Service, BroadcastReceiver, ContentProvider) declared in the manifest and started by the system.
- Intents are messages; explicit Intents name a class, implicit Intents describe an action matched by intent filters; extras must be small.
- The Activity lifecycle (`onCreate` … `onDestroy`) is driven by the system; the back stack keeps stopped activities; rotation destroys and recreates the activity.
- Survive rotation with ViewModel and `onSaveInstanceState`; survive everything with persistent storage.
- Launch modes control instance reuse; services, receivers and providers have narrow, battery-aware roles.

## Practice

1. Name the four component types and give one example of each.
2. What does the MAIN/LAUNCHER intent filter do?
3. Differentiate explicit and implicit Intents with an example of each.
4. List the callbacks called, in order, when activity A starts activity B.
5. Why is the activity destroyed on rotation and how can you keep the typed text?
6. Which state survives rotation but not process death?
7. Why should you pass an ID rather than a large object in an Intent extra?
8. Describe `singleTop`.
9. Compare started, bound and foreground services.
10. What replaced most background services for deferrable work?

::: note Answers and worked solutions
**1.** Activity (login screen), Service (music playback), BroadcastReceiver (battery low), ContentProvider (contacts).
**2.** It marks the activity as the app's entry point to appear in the launcher.
**3.** Explicit: `Intent(this, DetailActivity::class.java)`. Implicit: `ACTION_VIEW` with a web URL, matched to a browser by its intent filter.
**4.** A.onPause, B.onCreate, B.onStart, B.onResume, A.onStop (then A.onSaveInstanceState on current versions).
**5.** A configuration change may change resources, so the system recreates the activity; keep text with `onSaveInstanceState` (or let the view restore its state) and the loaded data in a ViewModel.
**6.** A ViewModel's data.
**7.** Extras travel through Binder, which has a size limit and copies the data; an ID lets the next screen load the data from its source.
**8.** If the activity is already on top, the existing instance receives the new Intent in `onNewIntent` instead of a new instance being created.
**9.** Started: runs until stopped. Bound: serves clients while bound. Foreground: long-running with a visible notification.
**10.** WorkManager (with JobScheduler underneath).
:::
