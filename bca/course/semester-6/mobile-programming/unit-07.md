---
subject: Mobile Programming
grade: BCA Semester 6
unit: 7
title: Cross-Platform Development, Testing and Publishing
hours: 6
area: BCA 352 · Mobile Programming · Unit 7
---

An app that works on the developer's phone is only the start. It must run on hundreds of device models, be tested, shrunk, **signed** with a key that proves who built it, versioned so updates install in the right order and published to a store. A team with one developer may also have to reach iPhone users too. This unit compares cross-platform frameworks, describes testing and quality practice, and explains packaging (APK and AAB), signing, versioning and store release. The signing explanation is accompanied by a *simplified* chunked-digest program, executed, that shows why changing a single byte of the package invalidates its signature.

::: key What this unit gives you
- Cross-platform options: Flutter, React Native, Kotlin Multiplatform, PWAs; when to choose each.
- Testing pyramid, tools and release quality (crash reporting, staged rollout).
- Build outputs: APK, AAB, R8 shrinking; APK signing with a digest demonstration; versionCode arithmetic.
- Publishing: Play Console, store listing, policies; distribution and monetisation in Nepal.
:::

## 7.1 Cross-platform frameworks

| Framework | Language | How the UI is drawn | Notes |
|---|---|---|---|
| **Flutter** (Google) | Dart | Its own rendering engine draws every pixel | Consistent look, fast, large community; custom widgets rather than native ones |
| **React Native** (Meta) | JavaScript/TypeScript | A bridge to real native widgets | Reuses web skills; native modules needed for some features |
| **Kotlin Multiplatform** (JetBrains) | Kotlin | Share logic; build UI natively or with Compose Multiplatform | Gradual adoption, native look |
| **Xamarin / .NET MAUI** | C# | Native widgets through .NET | Good for .NET teams |
| **Ionic / Capacitor / Cordova** | Web (HTML, CSS, JS) | A web view inside a native shell | Quickest for web teams, weakest performance |
| **PWA** | Web | Browser | No store, limited device access |

**Choosing.** One developer, standard screens and a deadline: Flutter or React Native. An app that needs deep platform features (a custom camera pipeline, a new OS feature on launch day) or maximum performance: native. Business logic shared between an existing Android and iOS app: Kotlin Multiplatform. A content service with little device access: a PWA. The costs of cross-platform are a larger app size, a dependence on the framework's roadmap, and the need to learn some native code for plugins. Hiring and maintenance are often the deciding factors: choose what the team can maintain for years.

Not executed (needs the Flutter SDK): the Flutter counter, the equivalent of the Compose example in Unit 3.

```dart
class Counter extends StatefulWidget {
  const Counter({super.key});
  @override
  State<Counter> createState() => _CounterState();
}
class _CounterState extends State<Counter> {
  int count = 0;
  @override
  Widget build(BuildContext context) => Column(children: [
        Text('Clicks: $count'),
        ElevatedButton(onPressed: () => setState(() => count++), child: const Text('Add')),
      ]);
}
```

## 7.2 Testing and quality

The **testing pyramid** recommends many fast tests at the bottom and few slow ones at the top:

| Level | Runs on | Tests | Tools |
|---|---|---|---|
| **Unit tests** | Local JVM (seconds) | Logic: ViewModels, repositories, parsers, calculators (like the EMI program of Unit 4) | JUnit, Mockito/MockK, Truth, coroutine test utilities |
| **Integration tests** | JVM or device | Room with a real database, repository with a fake server | Room testing, MockWebServer |
| **UI / instrumented tests** | Device or emulator | Screens and flows | Espresso, Compose test rules, UI Automator |
| **Manual and exploratory** | Real devices | Look and feel, odd devices | Test on a low-end phone, slow network, small screen, Nepali locale, large fonts |

Also: **static analysis** (Lint, detekt, ktlint), **performance profiling** (Android Studio Profiler: CPU, memory, network, energy), **StrictMode** (flags accidental disk and network on the main thread) and **LeakCanary** (finds memory leaks). Test the awkward cases: rotation in the middle of a request, process death, permission denial, airplane mode, a server returning an error. After release, **crash reporting** (Firebase Crashlytics) and analytics tell you what broke on devices you do not own; **staged rollout** (release to 5%, then 20%, then 100%) limits the damage of a bad release. Accessibility checks (TalkBack, contrast, 48 dp targets) are part of quality.

## 7.3 Packaging: APK, AAB and shrinking

The Gradle build produces either an **APK** (Android Package, a zip containing DEX code, resources, native libraries and the manifest, installable directly) or an **AAB** (Android App Bundle), the format Google Play requires for new apps: Play uses the bundle to generate *split APKs* tuned to each device (its screen density, CPU architecture and language), so users download less. To reduce size: **R8** shrinks (removes unused code), optimises and **obfuscates** (renames classes) according to ProGuard rules; **resource shrinking** removes unused resources; use vector drawables and WebP; avoid large libraries for small features. Download size matters to prepaid-data users: under about 20 MB is a common target for the Nepali market, and an app that offers a **lite** variant for low-end devices gains users.

## 7.4 Signing

Every APK must be **digitally signed** before it can be installed. The developer holds a **private key** in a keystore; the signature proves that the package comes from the key's owner and has not been modified, and Android refuses to install an *update* signed by a different key than the installed version (so nobody else can update your app). Rules: **keep the keystore and passwords safe and backed up** (losing the key means you can never update the app under the same identity, unless you enrolled in **Play App Signing**, where Google holds the app-signing key and you hold only an upload key); never commit the keystore or its passwords to a repository.

**APK Signature Scheme v2** and later signs the *whole file*: the APK content is split into **1 MiB chunks**; each chunk is hashed (SHA-256 of a 0xA5 byte, the chunk length and the chunk), and a top-level digest is the hash of a 0x5A byte, the number of chunks and all chunk digests; the signature covers that top-level digest. Verification recomputes it, so changing *any byte* changes a chunk digest and then the top-level digest, and the signature check fails. The program below follows this structure on synthetic data (a simplification: the real format also treats the signing block and the zip central directory specially):

```python
import hashlib, struct
CHUNK = 1024 * 1024
data = bytes((i * 7) % 251 for i in range(2500000))

def root_digest(blob):
    digests = []
    for off in range(0, len(blob), CHUNK):
        chunk = blob[off:off + CHUNK]
        digests.append(hashlib.sha256(b"\xa5" + struct.pack("<I", len(chunk)) + chunk).digest())
    return hashlib.sha256(b"\x5a" + struct.pack("<I", len(digests)) + b"".join(digests)).hexdigest(), len(digests)

root, n = root_digest(data)
print(len(data), "bytes ->", n, "chunks")
print("root digest:", root[:32])
tampered = bytearray(data)
tampered[1500000] ^= 1
print("tampered root differs:", root_digest(bytes(tampered))[0] != root)
```
```output
2500000 bytes -> 3 chunks
root digest: 395837017c7c09ab60d2b9d8d5ab05e1
tampered root differs: True
```
The three chunks are 1,048,576 + 1,048,576 + 402,848 bytes. Flipping one bit at offset 1,500,000 (inside the second chunk) changes that chunk's digest and so the root, and the verification fails.

## 7.5 Versioning and release

Two version numbers matter: **versionName** (shown to users, for example "2.3.7") and **versionCode** (an integer that must *increase* with every release; the store and installer use it to decide what is an update). A common scheme derives the code from the semantic version: **versionCode = major × 10,000 + minor × 100 + patch**, so 2.3.7 becomes 2 × 10,000 + 3 × 100 + 7 = **20307**, and 2.10.0 becomes 21000, which sorts after 2.9.9 (20909) as it should. Release steps: update the version, run tests, build the **release AAB**, sign, upload to the **Google Play Console** (internal testing track, then closed, open, and production), complete the **store listing** (title, short and full description in English and Nepali, screenshots, icon, feature graphic, privacy policy URL, content rating, a *Data safety* form describing what you collect), and use a staged rollout. Play enforces **policies** (permissions justification, user data, ads, deceptive behaviour) and **target API** deadlines; apps that miss them lose visibility. Alternatives for distribution include direct APK download from a website (users must enable installing from unknown sources, which is a security risk), third-party stores and the Apple App Store (for which an Apple developer account, a Mac and Xcode are needed).

**Monetisation.** Paid download, in-app purchases and subscriptions (Google Play Billing; developers outside supported payout countries may need workarounds, so check current rules), advertising (AdMob) and sponsorship. In Nepal, local payment integrations (wallet and bank QR SDKs) are common for in-app payments for physical goods and services (which Play's billing rules allow); always respect store policy about digital goods.

## 7.6 A development checklist

- Define **minSdk** from your audience, declare only the permissions you use.
- Use **ViewModel + repository + Room + coroutines**; keep the UI declarative or thin.
- Support **Nepali** and large fonts; use dp/sp; test on small, slow phones.
- Treat the network as unreliable: timeouts, retries with backoff, offline cache.
- Protect secrets and personal data; encrypt, minimise, explain.
- Automate: unit tests in CI, lint, signed release builds from a CI secret store.
- Monitor: crash reports, ANR rate, staged rollout, user feedback.

## 7.7 Seeing the release: frameworks, tests, packages and keys

Shipping an app is a chain of decisions and artefacts: which framework, how much testing, which package format, which key signs it and which version number it carries. The plate shows three physical or visible parts of that chain: a hardware key, a phone making a payment, and the line of Android versions the app must keep working on. The figures then draw each artefact with the numbers used in this unit.

```photogrid label="7.1" cols="3" ratio="1.0" caption="Three things a release depends on. (a) A hardware security key: the same kind of device that can hold the private key for signing builds or protect the developer's Google account, so that a stolen password is not enough. (b) A customer paying with a phone at a card terminal: payments, wallets and QR codes are the most common revenue and use case in Nepal, and they must follow the store's billing policy. (c) Android version statues at the Google campus: every release must state the oldest version it supports (minSdk) and the version it was tested on (targetSdk)."
@ photo id="bca401/yubikey" cap="Hardware security key"
fit 1.0
focus 0.5 0.5
@ photo id="bca352/nfc" cap="Payment by phone"
fit 1.0
focus 0.6 0.45
@ photo id="bca352/droids" cap="Android versions"
fit 1.0
focus 0.35 0.5
```

```svgfig label="7.1" caption="Four ways to build one app. Native uses one code base per platform. Flutter has one Dart code base and its own engine that draws every pixel, so the look is identical on both systems. React Native has one JavaScript code base that drives real native widgets through a bridge. Kotlin Multiplatform shares only the logic and keeps the native user interface. The more that is shared, the less the app feels native."
f = Fig(580, 260)
cols = [("Native", ["Kotlin UI", "Kotlin logic", "Swift UI", "Swift logic"], TEAL, MINT, 10), ("Flutter", ["Dart widgets", "Own engine draws", "Android | iOS"], NAVY, BLUE, 155), ("React Native", ["JavaScript", "Bridge", "Native widgets", "Android | iOS"], AMBER, SAND, 300), ("Kotlin Multiplatform", ["Native UI x 2", "Shared Kotlin logic", "Android | iOS"], RED, ROSE, 445)]
for t, L, st, fl, x in cols:
    f.text(x + 62, 14, t, size=10.5, color=st, bold=True)
    for i, s in enumerate(L):
        f.box(x, 26 + i * 42, 124, 36, s, fill=fl, stroke=st, size=9.5)
f.text(72, 222, "2 code bases", size=10, color=TEAL, bold=True); f.text(217, 222, "1 code base", size=10, color=NAVY, bold=True)
f.text(362, 222, "1 code base", size=10, color=AMBER, bold=True); f.text(507, 222, "shared logic", size=10, color=RED, bold=True)
f.text(290, 248, "less shared  <---------------------------->  more shared (but less native feel)", size=10, color=SLATE)
```

```svgfig label="7.2" caption="The testing pyramid. Many fast unit tests (JUnit, on the local JVM, seconds) form the base; fewer integration tests (Room with a real database, MockWebServer) sit in the middle; a few slow UI tests (Espresso, Compose test rules on a device) sit at the top. A common guideline is about 70 per cent unit, 20 per cent integration and 10 per cent UI tests. Manual testing on a low-end phone, a slow network, a small screen, a Nepali locale and large fonts is added beside the pyramid."
f = Fig(580, 240)
f.poly([(290, 14), (350, 74), (230, 74)], fill=ROSE, stroke=RED, label="UI", lx=290, ly=56, size=11)
f.poly([(220, 82), (360, 82), (410, 140), (170, 140)], fill=SAND, stroke=AMBER, label="Integration", lx=290, ly=111, size=11)
f.poly([(160, 148), (420, 148), (480, 220), (100, 220)], fill=MINT, stroke=TEAL, label="Unit tests", lx=290, ly=184, size=12)
f.text(495, 50, "10 %\nslowest", size=10.5, color=RED, bold=True, anchor="start")
f.text(495, 114, "20 %\nmedium", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(495, 184, "70 %\nfastest", size=10.5, color=TEAL, bold=True, anchor="start")
f.box(8, 60, 110, 100, "Also by hand:\nlow-end phone\nslow network\nNepali locale\nlarge fonts", fill=BLUE, stroke=NAVY, size=9.5)
```

```svgfig label="7.3" caption="Why Play wants a bundle. The developer uploads one AAB. For each phone Play assembles split APKs: the base code, only the screen-density resources that phone needs, only its CPU architecture and only its languages. The illustrative sizes show a universal APK of 30 MB against a download of 9.0 + 2.5 + 6.0 + 0.3 = 17.8 MB, a saving of 12.2 MB (40.7 per cent). The sizes are an example, not a measurement; the principle is that users download less."
f = Fig(580, 240)
f.box(10, 90, 100, 60, "One AAB\nuploaded", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(150, 90, 90, 60, "Google\nPlay", fill=SAND, stroke=AMBER, size=11, bold=True)
f.arrow([(110, 120), (150, 120)], color=SLATE)
S = [("base code 9.0 MB", NAVY, MINT), ("xxhdpi resources 2.5 MB", TEAL, BLUE), ("arm64 libraries 6.0 MB", AMBER, SAND), ("Nepali strings 0.3 MB", RED, ROSE)]
for i, (t, c, fl) in enumerate(S):
    y = 20 + i * 48
    f.box(300, y, 190, 38, t, fill=fl, stroke=c, size=10)
    f.arrow([(240, 120), (300, y + 19)], color=c, sw=1.3)
f.text(535, 90, "= 17.8 MB", size=11, color=TEAL, bold=True)
f.text(535, 110, "download", size=10, color=SLATE)
f.box(150, 196, 340, 32, "universal APK for every device: 30 MB", fill=ROSE, stroke=RED, size=10.5, bold=True)
```

```svgfig label="7.4" caption="APK Signature Scheme v2 on the 2,500,000-byte test file of section 7.4. The file is cut into 1 MiB chunks of 1,048,576 + 1,048,576 + 402,848 bytes; each chunk is hashed with SHA-256 (with a 0xA5 prefix and the chunk length), and the three digests are hashed again into the root digest 395837017c7c09ab... which is signed with the developer's private key. Flipping one bit at offset 1,500,000 (inside chunk 2) changes digest 2 and therefore the root, so the installer rejects the file."
f = Fig(580, 250)
C = [("chunk 1\n1,048,576 B", MINT, TEAL, 10), ("chunk 2\n1,048,576 B", ROSE, RED, 195), ("chunk 3\n402,848 B", MINT, TEAL, 380)]
for t, fl, st, x in C:
    f.box(x, 14, 180 if "402" not in t else 190, 48, t, fill=fl, stroke=st, size=10.5, bold=True)
    f.arrow([(x + 90, 62), (x + 90, 92)], color=st)
    f.box(x + 20, 92, 140, 34, "SHA-256 digest", fill=ROSE if st == RED else BLUE, stroke=st, size=10)
    f.arrow([(x + 90, 126), (290, 160)], color=st, sw=1.2)
f.box(190, 160, 200, 40, "root digest 39583701...", fill=SAND, stroke=AMBER, size=11, bold=True)
f.arrow([(390, 180), (440, 180)], color=NAVY)
f.box(440, 160, 130, 40, "signed with\nprivate key", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.text(290, 224, "one flipped bit at offset 1,500,000 -> digest 2 changes -> root changes -> install refused", size=10, color=RED, bold=True)
```

```svgfig label="7.5" caption="Why versionCode = major x 10,000 + minor x 100 + patch sorts correctly. The codes for the versions shown are 1.12.5 = 11205, 2.0.0 = 20000, 2.3.7 = 20307, 2.9.9 = 20909, 2.10.0 = 21000 and 3.4.12 = 30412; they increase in the same order as the versions. A plain string comparison would wrongly put 2.10.0 before 2.9.9, and the installer treats a lower versionCode as a downgrade and refuses it."
f = Fig(580, 200)
V = [("1.12.5", 11205), ("2.0.0", 20000), ("2.3.7", 20307), ("2.9.9", 20909), ("2.10.0", 21000), ("3.4.12", 30412)]
lo, hi = 11205, 30412
f.line(40, 100, 560, 100, color=SLATE, sw=2)
for i, (n, c) in enumerate(V):
    x = 60 + i * 92
    up = i % 2 == 0
    f.circle(x, 100, 5, fill=TEAL if n != "2.10.0" else RED, stroke=NAVY)
    f.text(x, 100 - 26 if up else 100 + 30, n, size=10.5, color=NAVY, bold=True)
    f.text(x, 100 - 12 if up else 100 + 44, str(c), size=9.5, color=SLATE)
f.text(290, 180, "string order: 2.10.0 < 2.9.9 (wrong)   code order: 20909 < 21000 (right)", size=10.5, color=AMBER, bold=True)
f.text(290, 22, "versionCode increases with every release (spacing not to scale)", size=10.5, color=NAVY, bold=True)
```

```svgfig label="7.6" caption="The release pipeline. A version bump, tests and a release build precede signing; the signed AAB goes to the internal track (the team), then closed testing (invited users), open testing and production; production is released in stages (for example 1, 10, 50 and 100 per cent of users) while crash and ANR rates are watched, and the rollout is halted if they rise."
f = Fig(580, 230)
S = [("1 Version\nbump", BLUE, NAVY), ("2 Run tests\n(CI)", MINT, TEAL), ("3 Build\nrelease AAB", BLUE, NAVY), ("4 Sign", SAND, AMBER), ("5 Upload to\nPlay Console", BLUE, NAVY)]
for i, (t, fl, st) in enumerate(S):
    x = 8 + i * 115
    f.box(x, 16, 100, 46, t, fill=fl, stroke=st, size=10, bold=True)
    if i < 4: f.arrow([(x + 100, 39), (x + 115, 39)], color=SLATE)
T = [("Internal", 30), ("Closed", 110), ("Open", 190), ("Production", 270)]
f.arrow([(520, 62), (520, 90), (47, 90), (47, 100)], color=SLATE)
for i, (n, x) in enumerate(T):
    f.box(10 + i * 82, 100, 74, 36, n, fill=SAND, stroke=AMBER, size=9.5 if n == "Production" else 10.5, bold=True)
for i, p in enumerate(["1 %", "10 %", "50 %", "100 %"]):
    f.box(350 + i * 56, 100, 50, 36, p, fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.text(460, 154, "staged rollout of production", size=10, color=TEAL, bold=True)
f.text(290, 190, "watch crash rate and ANR rate at each stage; halt the rollout if they rise", size=10.5, color=RED, bold=True)
f.text(290, 214, "listing: English + Nepali text, screenshots, privacy policy URL, Data safety form", size=10, color=SLATE)
```

### 7.7.1 Eight things to check before publishing an app

1. **Pick the framework with the team in mind.** A one-person team with standard screens can use Flutter or React Native, and a bank with a custom camera pipeline may need native code. The wrong choice costs months. Write down the reasons, as the diagram in Figure 7.1 shows the trade between sharing and native feel.
2. **Run the whole test pyramid.** Most of the tests should be fast unit tests of the logic, such as the EMI calculator of Unit 4, with a few UI tests on top (Figure 7.2). Add manual runs on a cheap phone with a slow network. An app tested only on a new flagship phone often fails for the many users on 2 GB devices.
3. **Shrink the download.** Use R8, resource shrinking, WebP and vector drawables, and upload an AAB so that Play builds split APKs (Figure 7.3). A user on a prepaid data pack decides in seconds whether a 60 MB download is worth it. An app under about 20 MB is far more likely to be installed.
4. **Protect the signing key.** The private key proves that an update comes from you, and losing it means you can never update the app under the same identity. Keep a backup in a safe place, use Play App Signing and protect the Google account with a hardware key (Plate 7.1a). Never commit a keystore or its password to a public repository.
5. **Increase versionCode every time.** The installer treats a lower or equal code as a downgrade and refuses it. A formula such as major × 10,000 + minor × 100 + patch sorts correctly (Figure 7.5). Keep versionName readable for users, for example 2.3.7.
6. **Complete the store listing honestly.** Give a title and descriptions in English and Nepali, real screenshots, a privacy-policy URL, a content rating and an accurate Data safety form. Play compares the form with what the app really does. A mismatch can lead to rejection or removal.
7. **Release in stages and watch.** Start with internal and closed testers, then roll out to 1 per cent, 10 per cent and more of the users while crash and ANR rates are watched (Figure 7.6). If a bug appears, halting at 1 per cent harms few people. A school app released to every user at once and broken on one phone model teaches this lesson quickly.
8. **Follow the payment and policy rules.** Digital goods inside the app must use Play Billing, while physical goods and services may use local wallets and QR payments such as Fonepay (Plate 7.1b). Keep the target API level current, justify every permission and respect advertising rules. Apps that miss the deadlines lose visibility in the store.

## Chapter summary

- Cross-platform frameworks (Flutter, React Native, Kotlin Multiplatform, PWAs) trade one code base against size, fidelity and plugin dependence; choose by team skills and requirements.
- Test mostly with fast JVM unit tests, some integration tests and few UI tests; test on low-end devices, slow networks and Nepali locale.
- Release as a shrunk (R8) AAB; Play generates device-specific APKs; keep download size low.
- Signing proves authorship and integrity; v2 signs chunk digests of the whole file (tampering flips the root digest); protect the key.
- versionCode must increase (major × 10,000 + minor × 100 + patch); publish through staged tracks with a complete listing.

## Practice

1. Compare Flutter and React Native in three points.
2. When would you choose native development over cross-platform?
3. Describe the testing pyramid and one tool per level.
4. What is the difference between APK and AAB?
5. What does R8 do?
6. Why must you protect the signing key and what is Play App Signing?
7. In the signing digest scheme, how many 1 MiB chunks does a 5,000,000-byte file have, and what is the size of the last one?
8. Compute versionCode for version 3.14.2 using the scheme of this unit.
9. Why is a staged rollout useful?
10. List four items needed for a Play Store listing.

::: note Answers and worked solutions
**1.** Flutter: Dart, draws its own widgets, consistent UI. React Native: JavaScript, native widgets through a bridge, reuses web skills, depends on native modules. Both give one code base for Android and iOS.
**2.** For deep platform features, maximum performance, a new OS feature on day one, or a platform-specific look.
**3.** Unit tests on the JVM (JUnit), integration tests (Room testing, MockWebServer), UI tests on a device (Espresso), with many at the bottom and few at the top.
**4.** An APK is an installable package; an AAB is a publishing format from which Play builds optimised split APKs for each device.
**5.** It shrinks (removes unused code), optimises and obfuscates the code.
**6.** Updates must be signed by the same key; losing it blocks updates. Play App Signing lets Google hold the app-signing key so a lost upload key can be reset.
**7.** 5,000,000 / 1,048,576 = 4.77, so **5 chunks**; the last has 5,000,000 − 4 × 1,048,576 = **805,696 bytes**.
**8.** 3 × 10,000 + 14 × 100 + 2 = **31402**.
**9.** A bad release reaches only a small share of users first, so problems found by crash reports can be fixed before most users are affected.
**10.** Title, descriptions (English and Nepali), screenshots, icon, privacy-policy URL, content rating, Data safety form.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Compare Flutter, React Native and native development and say when each is the better choice.**

*Introduction.* Cross-platform frameworks trade one code base against size, fidelity and plugin dependence (section 7.1, Figure 7.1).

1. **Flutter.** One Dart code base; its own engine draws every pixel, so the look is the same on Android and iOS and animation is smooth. The cost is custom widgets and a larger app.
2. **React Native.** One JavaScript or TypeScript code base driving real native widgets through a bridge, so it reuses web skills; features without a ready module need native code.
3. **Native.** Kotlin or Swift with the platform SDK: best performance, immediate access to new features, and the platform look, but two code bases.
4. **Kotlin Multiplatform.** Shares the logic only and keeps the native UI, which allows gradual adoption.

| Point | Flutter | React Native | Native |
|---|---|---|---|
| Language | Dart | JavaScript | Kotlin / Swift |
| UI | Own engine | Native widgets | Native |
| Code bases | 1 | 1 | 2 |
| Best for | Fast, consistent UI | Web teams | Deep platform features |

*Conclusion.* One developer with standard screens and a deadline should choose Flutter or React Native; an app needing maximum performance or day-one OS features should be native.

**Q2 (5 marks). Explain the testing pyramid and name the tools used at each level.**

*Introduction.* The pyramid recommends many fast tests at the bottom and few slow ones at the top (section 7.2, Figure 7.2).

1. **Unit tests (about 70 per cent).** Run on the local JVM in seconds and test logic such as ViewModels, repositories, parsers and the EMI calculator. Tools: JUnit, MockK or Mockito, Truth and coroutine test utilities.
2. **Integration tests (about 20 per cent).** Test components together, for example Room with a real database or a repository with a fake server. Tools: Room testing support and MockWebServer.
3. **UI tests (about 10 per cent).** Run on an emulator or device and drive screens and flows. Tools: Espresso, Compose test rules and UI Automator.
4. **Manual testing.** Real devices, a low-end phone, a slow network, a small screen, the Nepali locale and large fonts.
5. **Supporting tools.** Lint and detekt for static analysis, the Profiler for CPU, memory, network and energy, StrictMode for main-thread I/O and LeakCanary for leaks.

*Conclusion.* A pyramid keeps feedback fast and the suite cheap, while a few UI and manual tests confirm that the whole app works on real devices.

**Q3 (5 marks). Using versionCode = major × 10,000 + minor × 100 + patch, compute the codes for 1.12.5, 2.3.7, 2.9.9, 2.10.0 and 3.4.12, and explain why the formula is used.**

*Introduction.* Two numbers identify a release: versionName (shown to users) and versionCode (an integer that must increase, section 7.5, Figure 7.5).

1. **1.12.5:** 1 × 10,000 + 12 × 100 + 5 = **11205**.
2. **2.3.7:** 2 × 10,000 + 3 × 100 + 7 = **20307**.
3. **2.9.9:** 20,000 + 900 + 9 = **20909**.
4. **2.10.0:** 20,000 + 1,000 + 0 = **21000**, greater than 20909 as it should be.
5. **3.4.12:** 30,000 + 400 + 12 = **30412**.
6. **Why.** The store and the installer decide what is an update from the integer; a lower or equal code is a downgrade and is refused. Text comparison would put "2.10.0" before "2.9.9". The formula assumes minor and patch stay below 100.

*Conclusion.* The codes 11205 < 20307 < 20909 < 21000 < 30412 increase with the versions, so each release counts as an update.

**Q4 (10 marks). Explain why Android apps are signed. Describe APK Signature Scheme v2 and show with the test file of section 7.4 how tampering is detected.**

*Introduction.* Every APK must be digitally signed before it can be installed; the signature proves who published the package and that it has not been modified (section 7.4, Figure 7.4).

1. **Private key.** The developer holds a private key in a keystore (ideally protected by hardware, Plate 7.1a); the public certificate travels inside the APK.
2. **Update rule.** Android installs an update only if it is signed with the same key as the installed app, so another publisher cannot replace the app.
3. **Scheme v2.** The whole file is signed, not each entry, and the signature block sits just before the central directory.
4. **Chunking.** The APK is cut into 1 MiB (1,048,576-byte) chunks. The 2,500,000-byte test file gives 3 chunks of 1,048,576, 1,048,576 and 402,848 bytes.
5. **Digests.** Each chunk is hashed with SHA-256 over a 0xA5 byte, the chunk length and the chunk. A top-level digest is the SHA-256 of a 0x5A byte, the number of chunks and the concatenated chunk digests; its value for the test file begins 395837017c7c09ab.
6. **Signature.** The root digest is signed with the private key, and the installer verifies it with the certificate.
7. **Tampering.** Flipping one bit at offset 1,500,000, which lies in chunk 2, changes digest 2 and therefore the root digest; the program prints `tampered root differs: True` and the installer refuses the package.
8. **Parallel and fast.** Chunks can be hashed in parallel, so verification is faster than checking every entry of the older v1 jar signing.

| Point | v1 (jar signing) | v2 and later |
|---|---|---|
| Covers | Each file entry | Whole APK |
| Speed | Slower | Faster, parallel |
| Extra bytes inserted | May go unnoticed | Detected |
| Hash unit | File | 1 MiB chunk |

*Conclusion.* Signing gives identity and integrity; v2 protects every byte of the file, and the developer must guard the key because losing it means losing the ability to update.

**Q5 (10 marks). Describe the steps for preparing and publishing an Android app on Google Play, including packaging, testing tracks and the store listing.**

*Introduction.* Publishing is a pipeline from source code to a signed bundle in front of users (sections 7.3 to 7.6, Figure 7.6).

1. **Prepare.** Fix minSdk from the audience, declare only the needed permissions, and keep targetSdk current because Play enforces deadlines.
2. **Version.** Raise versionName and versionCode (for example 2.3.7 becomes 20307).
3. **Test.** Run unit and integration tests in CI, then UI tests and manual runs on a low-end phone, a slow network and the Nepali locale.
4. **Shrink.** Enable R8 and resource shrinking, use vector drawables and WebP; aim for a small download.
5. **Build and sign.** Build a release AAB and sign it; use Play App Signing and a protected key.
6. **Upload and tracks.** Upload to the Play Console, publish first to the internal track, then closed, open and production.
7. **Listing.** Provide a title and descriptions in English and Nepali, screenshots, icon, feature graphic, privacy-policy URL, content rating and the Data safety form.
8. **Roll out and monitor.** Release in stages (for example 1, 10, 50 and 100 per cent), watch crash and ANR rates and halt if they rise.

**Monetisation.** Paid download, in-app purchases and subscriptions through Play Billing, advertising (AdMob) and sponsorship; physical goods and services may use local wallets or QR payments, but digital goods must respect store policy.

| Step | Purpose |
|---|---|
| Version + tests | Safe, ordered updates |
| R8 + AAB | Small downloads |
| Sign | Identity and integrity |
| Tracks | Gradual exposure |
| Listing + Data safety | Compliance and trust |

*Conclusion.* A disciplined pipeline of testing, shrinking, signing and staged rollout gets an app to users safely and keeps it updatable.
