---
subject: Mobile Programming
grade: BCA Semester 6
unit: 1
title: Mobile Platforms and Application Architecture
hours: 6
area: BCA 352 · Mobile Programming · Unit 1
---

A phone in a Humla village and a phone in a Kathmandu office run the same app, yet one has a cracked 720-pixel screen, 2 GB of memory and a connection that drops every few minutes, while the other has a 1080-pixel OLED display, 8 GB and fibre Wi-Fi. A mobile programmer writes for *both*, on a device that is small, battery-powered, always moving and shared among dozens of apps competing for the same memory. This unit surveys the platforms (Android and iOS), their layered architectures, the constraints that shape mobile design, and the arithmetic of screen density and image memory that every layout decision rests on.

::: key What this unit gives you
- The mobile ecosystem: devices, operating systems, app types (native, web, hybrid, cross-platform).
- Android and iOS architecture layers; the Android runtime and the app sandbox.
- Mobile constraints and the density arithmetic (dp, sp, px), with image-memory calculations.
- Setting up an Android project and reading its structure.
:::

*Code in this book is labelled. Python and Java programs were **executed** and their output pasted by a tool. Kotlin, XML and Gradle snippets need the Android SDK, are **not executed** here, and are marked "not executed".*

## 1.1 The mobile landscape

A **mobile application** is software designed for handheld devices (phones, tablets, wearables) that uses their sensors, touch input and connectivity. The platform market is dominated by two systems: **Android** (an open-source operating system led by Google, running on devices from many manufacturers, the majority platform in Nepal) and **iOS** (Apple's closed system for iPhone and iPad). Others (HarmonyOS, KaiOS feature phones) exist but are smaller. Apps are distributed through **stores** (Google Play, Apple App Store) and, on Android, also by direct installation of an **APK** file.

| Approach | How it is built | Strengths | Weaknesses |
|---|---|---|---|
| **Native** | Kotlin/Java for Android; Swift for iOS; platform SDKs | Best performance, full access to features, platform look | Two code bases |
| **Mobile web** | HTML/CSS/JS in the browser, responsive design | One code base, no install | Limited device access, needs network |
| **Progressive web app (PWA)** | Web app with service worker, installable | Offline, push notifications on some platforms | Restricted on iOS, less integration |
| **Hybrid** | Web UI inside a native shell (Cordova, Ionic, Capacitor) | Reuse web skills | Slower UI, plugin dependence |
| **Cross-platform native-UI** | One code base compiled to native widgets or custom renderer (Flutter, React Native, Kotlin Multiplatform) | One team, near-native speed | Larger runtime, occasional platform gaps |

The choice is an engineering trade-off between cost, speed and fidelity; Unit 7 returns to it.

## 1.2 Android architecture

Android is a stack of layers, each using the one below:

1. **Linux kernel:** process and memory management, drivers (display, camera, Wi-Fi, Binder IPC), and security through Linux users and permissions.
2. **Hardware abstraction layer (HAL):** standard interfaces so that the framework talks to camera, audio and sensors regardless of the chip.
3. **Native libraries and Android Runtime (ART):** C/C++ libraries (SQLite, OpenGL ES, libc, media codecs) and **ART**, which runs app code. Apps are compiled to **DEX** bytecode; ART compiles it ahead of time and just in time to machine code (earlier versions used the Dalvik VM).
4. **Java API framework:** the services apps call: **Activity Manager** (lifecycle), **Package Manager**, **Window Manager**, **Content Providers**, **Notification Manager**, **Location Manager**, **Resource Manager** and the **View system**.
5. **System apps and your app:** the dialler, contacts and browser are ordinary apps built on the same APIs.

**The sandbox.** Each app runs as its own Linux user in its own process with a private data directory, so one app cannot read another's files; sharing needs explicit mechanisms (Intents, content providers, permissions). **Binder** is the inter-process communication system that connects apps to system services. Memory is managed aggressively: when memory is short the system **kills background processes** (least recently used first) without warning, so an app must save its state when it leaves the screen, a point that dominates Unit 2.

## 1.3 iOS architecture in outline

iOS has four layers: **Core OS** (kernel based on Darwin, security, drivers), **Core Services** (Foundation, Core Data, networking, location), **Media** (graphics, Metal, audio, video) and **Cocoa Touch** (UIKit or SwiftUI for the interface, notifications, multitasking). Apps are written in **Swift** (or Objective-C) in **Xcode**, run in a sandbox, and must be signed and distributed through Apple's programs. Concepts map closely: an Android *Activity* corresponds to a *UIViewController*, a *Fragment* to a child view controller, *RecyclerView* to *UITableView/UICollectionView*, *Intent* to URL schemes and *app extensions*, *Room* to Core Data or SwiftData, *Jetpack Compose* to SwiftUI. Learning one platform's lifecycle and layout model makes the other easy.

## 1.4 Constraints that shape mobile design

| Constraint | Consequence for the programmer |
|---|---|
| **Battery** | Avoid polling, wake locks and constant GPS; batch network and background work |
| **Memory** | Load scaled images, recycle views, release resources when hidden; the OS may kill the process |
| **Small, varied screens** | Density-independent units, responsive layouts, many sizes and orientations |
| **Touch input** | Targets of at least 48 dp, gestures, on-screen keyboard changes the layout |
| **Intermittent networks** | Cache, retry, work offline, show progress; expect failure |
| **Interruptions** | A call or notification can pause the app at any moment |
| **Fragmentation** | Many OS versions and manufacturers; test on low-end devices; declare minimum and target API levels |
| **Security and privacy** | Runtime permissions, secure storage, minimal data collection |

Context for Nepal: many users have low-end Android phones with limited storage and memory, prepaid mobile data, uneven connectivity outside cities and a need for Nepali-language interfaces and Devanagari text input, so *small download size*, *offline behaviour* and *language support* are core requirements, not extras.

## 1.5 Screen density arithmetic

Android measures size in **dp** (density-independent pixels): 1 dp is one pixel on a 160 dpi screen (**mdpi**, the baseline), so **px = dp × (dpi ÷ 160)**. Text uses **sp** (scale-independent pixels), which are dp scaled by the user's font-size setting. Using dp makes a 48 dp button about the same *physical* size (roughly 9 mm) on every device.

| Bucket | dpi | Scale (dpi ÷ 160) | 48 dp in px | 16 sp in px (font scale 1.0) |
|---|---|---|---|---|
| ldpi | 120 | 0.75 | 36 | 12 |
| mdpi | 160 | 1 | 48 | 16 |
| hdpi | 240 | 1.5 | 72 | 24 |
| xhdpi | 320 | 2 | 96 | 32 |
| xxhdpi | 480 | 3 | 144 | 48 |
| xxxhdpi | 640 | 4 | 192 | 64 |

A phone with a 1080 × 2400 pixel screen at 420 dpi has density 420 ÷ 160 = **2.625**, so its size in dp is 1080 ÷ 2.625 = **411.43 dp** wide and 2400 ÷ 2.625 = **914.29 dp** tall. Layouts are designed in dp, so this phone behaves like a 411 × 914 dp screen; the **smallest-width qualifier** (sw360dp, sw600dp for tablets) selects resource folders accordingly. Provide images for several density buckets (or use vector drawables) so that the system does not scale a small bitmap up and make it blurry.

### Image memory

An image decoded into memory takes **width × height × bytes per pixel**, regardless of its file size (JPEG compression is gone once it is decoded). A 12-megapixel photo (4000 × 3000) as ARGB_8888 (4 bytes a pixel) needs 4000 × 3000 × 4 = **4,80,00,000 bytes** (45.78 MiB). Loading it into a list of thumbnails would exhaust the memory of a 2 GB phone quickly. Decoding with **inSampleSize = 4** (every fourth pixel in each direction) gives 1000 × 750 and **30,00,000 bytes**, which is **16 times smaller**, ample for a screen thumbnail. Libraries (Coil, Glide, Picasso) do this sampling, caching and background loading for you.

## 1.6 Setting up an Android project

Development uses **Android Studio** (the official IDE based on IntelliJ), the **Android SDK** (platform libraries, build tools, emulator), and the **Gradle** build system. A project contains:

| Item | Purpose |
|---|---|
| `app/src/main/AndroidManifest.xml` | Declares the package, components, permissions, minimum API level |
| `app/src/main/java/...` (or `kotlin/`) | Source code |
| `app/src/main/res/` | Resources: `layout/`, `values/` (strings, colours, styles), `drawable/`, `mipmap/` (launcher icons), `values-ne/` (Nepali strings) |
| `app/build.gradle(.kts)` | Module build settings: `compileSdk`, `minSdk`, `targetSdk`, dependencies |
| `build/` | Generated output, including the APK |

Not executed (needs the Android SDK): a minimal module build file in Kotlin DSL.

```kotlin
android {
    namespace = "np.edu.demo.notes"
    compileSdk = 34
    defaultConfig {
        applicationId = "np.edu.demo.notes"
        minSdk = 24
        targetSdk = 34
        versionCode = 20307
        versionName = "2.3.7"
    }
}
dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.recyclerview:recyclerview:1.3.2")
}
```

**minSdk** is the oldest Android version supported (lower reaches more users, higher gives newer APIs); **targetSdk** declares the version the app was tested against and enables newer behaviour, and Google Play requires a recent value. The build turns sources and resources into DEX code and a compiled resource table, packages them into an **APK**, and **signs** it (Unit 7). The **emulator** (Android Virtual Device) and a real phone connected over **USB debugging** run the app, and **Logcat** shows logs.

## Chapter summary

- Android and iOS dominate; native, web, PWA, hybrid and cross-platform approaches trade cost against fidelity.
- Android layers: Linux kernel, HAL, native libraries and ART, Java API framework, apps; each app is sandboxed in its own process and can be killed in the background.
- iOS layers: Core OS, Core Services, Media, Cocoa Touch; concepts map one-to-one to Android.
- Mobile constraints (battery, memory, screens, intermittent network, interruptions) shape design; in Nepal, low-end devices, offline use and Nepali support matter most.
- px = dp × dpi/160; image memory = width × height × bytes per pixel; sample down large images.

## Practice

1. Compare native, hybrid and cross-platform development in three points each.
2. Name the five layers of the Android stack and give one component of each.
3. What is the Android sandbox and what mechanism lets apps cooperate?
4. How many pixels is a 48 dp target on an xhdpi (320 dpi) screen and on an xxhdpi (480 dpi) screen?
5. A 720 × 1600 screen has density 2.0. What is its size in dp?
6. How much memory does a 2000 × 1500 ARGB_8888 bitmap need?
7. How much does inSampleSize = 2 reduce the memory of a bitmap?
8. Distinguish dp and sp.
9. Why must an app save its state when it leaves the screen?
10. Explain minSdk and targetSdk.

::: note Answers and worked solutions
**1.** Native: best performance, full feature access, two code bases. Hybrid: web skills reused, one code base, slower UI. Cross-platform: one team and near-native speed, bigger runtime and occasional gaps.
**2.** Linux kernel (drivers, Binder), HAL (camera interface), native libraries/ART (SQLite, DEX runtime), Java API framework (Activity Manager), apps (dialler).
**3.** Each app runs in its own process as its own Linux user with private storage; apps cooperate through Intents, content providers and permissions (via Binder IPC).
**4.** xhdpi: 48 × 2 = **96 px**. xxhdpi: 48 × 3 = **144 px**.
**5.** 720/2 = 360 dp wide and 1600/2 = **800 dp** tall: **360 × 800 dp**.
**6.** 2000 × 1500 × 4 = **12,000,000 bytes** (11.44 MiB).
**7.** Each dimension halves, so the area is a quarter: a **4×** reduction.
**8.** dp scales with screen density only; sp also scales with the user's font-size preference (used for text).
**9.** The system can kill a background process at any time to free memory, losing unsaved in-memory state.
**10.** minSdk is the oldest API level the app runs on; targetSdk is the level the app was tested for, enabling that version's behaviour and store requirements.
:::
