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
