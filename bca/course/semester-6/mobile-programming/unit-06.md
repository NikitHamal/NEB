---
subject: Mobile Programming
grade: BCA Semester 6
unit: 6
title: Sensors, Location, Permissions and Notifications
hours: 6
area: BCA 352 · Mobile Programming · Unit 6
---

What makes a phone more than a small computer is what it can *sense*: where it is, how it is moving, what it sees and hears. Maps, step counters, ride-hailing and flood alerts all rest on those sensors, and all of them touch private information, so Android makes the user decide, through **permissions**. This unit covers the permission model, the motion and environment sensors with a runnable step-counting algorithm, location services with the **haversine** distance formula (executed), camera and media access, and notifications.

::: key What this unit gives you
- The permission model: install-time, runtime, special permissions, and good practice for asking.
- Sensors and sampling: accelerometer, gyroscope, proximity, light; a step-detection algorithm (executed).
- Location: GPS, network and fused providers; the haversine formula (executed); battery trade-offs.
- Camera, media pickers and notifications (channels, PendingIntent).
:::

## 6.1 Permissions

Android guards sensitive data and features with **permissions** declared in the manifest. They have **protection levels**: **normal** permissions (such as INTERNET) are granted automatically at install; **dangerous** permissions (camera, microphone, precise location, contacts, SMS, notifications on recent versions) must be approved by the user **at runtime**, in context, and can be revoked in settings at any time; **special** permissions (draw over other apps, exact alarms, all-files access) need a settings screen; **signature** permissions are for apps signed by the same key.

Principles for asking: request **only what you need**, **when you need it**, with a short **rationale** before the system dialog; handle **denial** gracefully (offer the feature without it, or explain how to enable it); and if the user chose "Don't ask again", send them to settings instead of asking repeatedly. Prefer privacy-preserving alternatives: the system **photo picker** and **document picker** need no storage permission; **approximate location** is enough for weather; the **camera intent** needs no CAMERA permission when you only want a photo. Since Android 11 a user can grant a permission *once* and the system auto-resets unused permissions.

Not executed (needs the Android SDK): the runtime-permission flow.

```kotlin
val launcher = registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
    if (granted) startCamera() else showExplanation()
}
fun onPhotoClicked() {
    when {
        ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
            == PackageManager.PERMISSION_GRANTED -> startCamera()
        shouldShowRequestPermissionRationale(Manifest.permission.CAMERA) -> showRationale()
        else -> launcher.launch(Manifest.permission.CAMERA)
    }
}
```

## 6.2 Sensors

The `SensorManager` exposes **motion sensors** (accelerometer, gyroscope, gravity, rotation vector, step counter and detector), **position sensors** (magnetometer for the compass, proximity) and **environment sensors** (light, pressure, temperature, humidity; availability varies by device). An app registers a `SensorEventListener` with a **sampling rate** and receives `onSensorChanged` events carrying a `values` array. Rules: *unregister in `onPause`* (a forgotten listener drains the battery), choose the lowest rate that works (`SENSOR_DELAY_NORMAL`, `UI`, `GAME`, `FASTEST`), and treat values as noisy.

The **accelerometer** reports acceleration along x, y, z in m/s², *including gravity* (about 9.8 m/s² when still), so the **magnitude** √(x² + y² + z²) is about 9.8 at rest and oscillates around it when walking, with peaks at each footfall. A simple **step detector** counts when the magnitude rises above a threshold, with a minimum gap between steps to avoid double counting. The executed program simulates 10 seconds of walking at 2 steps per second sampled at 50 Hz (a clean sine wave of amplitude 3 around 9.8) and counts the steps:

```python
import math
rate = 50
samples = [9.8 + 3.0 * math.sin(2 * math.pi * 2.0 * (i / rate)) for i in range(10 * rate)]
steps, above, last = 0, False, -100
for i, v in enumerate(samples):
    if v > 11.0 and not above and i - last >= 10:
        steps += 1
        last = i
    above = v > 11.0
print("steps =", steps)
```
```output
steps = 20
```
Two seconds of steps per second over ten seconds should give 20, and the checker confirms it by counting the local maxima above 11 with numpy. Real data are noisy, so real counters smooth the signal (a low-pass filter), adapt the threshold and use the hardware **step counter** sensor (a low-power chip) when available. The **gyroscope** reports rotation rates, and fusing accelerometer, gyroscope and magnetometer gives the device **orientation** (for compasses, games and AR). **Proximity** turns the screen off during a call; the **light** sensor drives auto-brightness.

## 6.3 Location

Location comes from **GPS** (accurate to a few metres outdoors, slow to start and power-hungry), **Wi-Fi and cell-tower positioning** (coarser, fast and efficient) and sensors. The **Fused Location Provider** (Google Play services) blends them and lets the app state a priority (`PRIORITY_HIGH_ACCURACY`, `PRIORITY_BALANCED_POWER_ACCURACY`), an interval and a minimum distance. Permissions: `ACCESS_COARSE_LOCATION` (about a city block or more) and `ACCESS_FINE_LOCATION` (precise); **background location** is a separate, tightly reviewed permission. Battery rules: ask for a single fix when a stream is not needed, lengthen the interval, stop updates in `onStop`, and use **geofences** instead of constant tracking.

Distances between two coordinates use the **haversine formula** on a sphere of radius R = 6371 km: a = sin²(Δφ/2) + cos φ₁ cos φ₂ sin²(Δλ/2), d = 2R·asin(√a), with latitudes φ and longitude difference Δλ in radians. For Kathmandu (27.7172° N, 85.3240° E) and Pokhara (28.2096° N, 83.9856° E):

```python
import math
def haversine(lat1, lon1, lat2, lon2, R=6371.0):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = p2 - p1
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlam / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

print(f"Kathmandu-Pokhara: {haversine(27.7172, 85.3240, 28.2096, 83.9856):.1f} km")
```
```output
Kathmandu-Pokhara: 142.4 km
```
The checker recomputes the distance with the *spherical law of cosines*, an independent formula, and the two agree to the printed precision. This is the **straight-line (great-circle)** distance, shorter than the road distance (the Prithvi Highway is much longer). Map display uses **Google Maps SDK**, **OpenStreetMap-based** libraries (osmdroid, MapLibre) or the system map; geocoding turns addresses into coordinates (poorly for Nepali addresses without street names, which is why some Nepali apps use landmarks or plus-codes).

## 6.4 Camera, media and sensors of the environment

Taking a photo can use the system camera app through an Intent (no permission, simple) or **CameraX**, a Jetpack library with use cases (preview, image capture, analysis) that handles device differences. Images are large (Unit 1): downscale before display or upload and **compress** (JPEG quality 80 gives a size that is a fraction of the original). Reading from the gallery uses the **photo picker**; audio recording needs `RECORD_AUDIO`. **Barcode and QR scanning** (ML Kit) and **text recognition** run on the device; QR is central to Nepali payments, where wallets and banks scan merchant QR codes (see *MIS and e-Business*). **Bluetooth Low Energy**, **NFC** and **Wi-Fi Direct** connect to nearby devices; they need permissions too.

## 6.5 Notifications

A **notification** reaches the user when the app is not on screen. Since Android 8, every notification belongs to a **channel** (importance level, sound, vibration) that the user can silence individually; Android 13 added the runtime **POST_NOTIFICATIONS** permission. A notification has a small icon, title, text, optional actions and a **PendingIntent** that opens the right screen when tapped. Push messages from a server arrive through **Firebase Cloud Messaging (FCM)**: the app registers, obtains a **token**, the server sends a message to the token and the app's `FirebaseMessagingService` shows the notification. Good practice: group related messages, never use notifications for advertising by default, let users choose categories, and respect quiet hours.

Not executed (needs the Android SDK): building a notification.

```kotlin
val channel = NotificationChannel("alerts", "Alerts", NotificationManager.IMPORTANCE_HIGH)
getSystemService(NotificationManager::class.java).createNotificationChannel(channel)
val tap = PendingIntent.getActivity(this, 0, Intent(this, DetailActivity::class.java),
    PendingIntent.FLAG_IMMUTABLE)
val n = NotificationCompat.Builder(this, "alerts")
    .setSmallIcon(R.drawable.ic_alert).setContentTitle("Flood warning")
    .setContentText("River level rising near your ward").setContentIntent(tap)
    .setAutoCancel(true).build()
NotificationManagerCompat.from(this).notify(1, n)
```

## 6.6 Seeing the sensors: chips, satellites, curves and prompts

The phone senses the world through small chips and radios, and each of them needs a permission and costs battery. The first plate shows the hardware: a motion chip, a proximity-style sensor and a fingerprint sensor. The second plate shows the satellites behind GPS and the geometry by which a position is found. The figures draw the permission flow, the accelerometer signal and the step threshold, the haversine triangle, the accuracy ladder and the anatomy of a notification.

```photogrid label="6.1" cols="3" ratio="1.0" caption="Sensors you can hold. (a) An InvenSense MPU-6050, a 4 x 4 mm chip that puts a 3-axis MEMS accelerometer and a 3-axis gyroscope on one silicon die; chips of this kind sit in every phone and report at 50 Hz or more. (b) A passive infrared (PIR) motion sensor module, the same idea as a proximity or presence sensor. (c) A fingerprint sensor, which needs its own permission flow (biometric prompt) and never exposes the image to the app. Every sensor listener must be unregistered in onPause."
@ photo id="bca352/mpu6050" cap="MPU-6050 motion chip"
fit 1.0
focus 0.5 0.5
@ photo id="bca101/pir" cap="PIR motion sensor"
fit 1.0
focus 0.5 0.5
@ photo id="bca401/fingerprint" cap="Fingerprint sensor"
fit 1.0
focus 0.5 0.5
```

```photogrid label="6.2" cols="2" ratio="1.05" caption="How a satellite fix works. (a) The GPS constellation: about 24 satellites in six orbital planes, about 20,200 km above the Earth, so that at least four are above the horizon from almost anywhere. (b) The idea in two dimensions: the signal travel time gives the distance to each satellite, a circle around it; one circle leaves a ring of positions, two leave two points, and a third circle picks the single point. In three dimensions the phone needs a fourth satellite to correct its own clock."
@ photo id="bca352/gps" cap="GPS satellite constellation"
fit 1.05
focus 0.5 0.5
@ svg cap="Position from three distances"
f = Fig(300, 300)
f.circle(95, 85, 78, fill="none", stroke=NAVY, sw=1.8)
f.circle(215, 95, 79, fill="none", stroke=TEAL, sw=1.8)
f.circle(150, 205, 65, fill="none", stroke=AMBER, sw=1.8)
f.circle(95, 85, 4, fill=NAVY, stroke=NAVY); f.circle(215, 95, 4, fill=TEAL, stroke=TEAL); f.circle(150, 205, 4, fill=AMBER, stroke=AMBER)
f.text(95, 72, "S1", size=12, color=NAVY, bold=True); f.text(215, 82, "S2", size=12, color=TEAL, bold=True); f.text(150, 223, "S3", size=12, color=AMBER, bold=True)
f.circle(150, 140, 6, fill=RED, stroke=RED)
f.text(160, 128, "you", size=13, color=RED, bold=True, anchor="start")
f.text(150, 292, "distance = c x travel time", size=12.5, color=SLATE, bold=True)
```

```svgfig label="6.1" caption="The runtime-permission flow of section 6.1. The app first checks whether the permission is already granted. If it is, the feature runs. If not, and the system says the user has refused once, a short rationale is shown first; otherwise the system dialog is launched. A grant starts the feature, a denial must leave the app usable, and after 'don't ask again' the only route is the Settings screen."
f = Fig(580, 250)
f.box(10, 20, 120, 40, "checkSelfPermission", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.poly([(190, 40), (250, 14), (310, 40), (250, 66)], fill=SAND, stroke=AMBER, label="granted?", lx=250, ly=40, size=10)
f.box(440, 20, 130, 40, "Run the feature", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(130, 40), (190, 40)], color=SLATE); f.arrow([(310, 40), (440, 40)], color=TEAL, label="yes", lpos=(375, 32))
f.arrow([(250, 66), (250, 100)], color=RED, label="no", lpos=(262, 86))
f.poly([(190, 126), (250, 100), (310, 126), (250, 152)], fill=SAND, stroke=AMBER, label="refused\nbefore?", lx=250, ly=126, size=9)
f.box(10, 106, 140, 40, "Show rationale\n(why we need it)", fill=BLUE, stroke=NAVY, size=10)
f.arrow([(190, 126), (150, 126)], color=SLATE, label="yes", lpos=(170, 118))
f.arrow([(250, 152), (250, 182)], color=SLATE, label="no", lpos=(262, 170))
f.box(170, 182, 160, 40, "System dialog\nlauncher.launch()", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.arrow([(80, 146), (80, 202), (170, 202)], color=SLATE)
f.arrow([(330, 202), (440, 202)], color=TEAL, label="Allow", lpos=(385, 194))
f.box(440, 182, 130, 40, "Feature or\ngraceful fallback", fill=MINT, stroke=TEAL, size=10)
f.text(290, 242, "Denied: keep the app usable; 'don't ask again': link to Settings", size=10, color=RED, bold=True)
```

```svgfig label="6.2" caption="The accelerometer magnitude of the step-counter program of section 6.2: 9.8 + 3 sin(2 pi x 2 t) m/s^2, a walk of two steps per second, sampled at 50 Hz. The signal never leaves the range 6.8 to 12.8. Each peak crosses the threshold 11 once and stays above it for about 0.18 s, so each peak is one step: 2 per second, 20 in 10 seconds, from 500 samples. The minimum gap of 10 samples (0.2 s) stops one peak being counted twice."
f = Fig(580, 250)
ax = Axes(f, 50, 20, 500, 180, (0, 2), (6, 14))
ax.grid(dx=0.5, dy=2, labels=True, size=9.5)
ax.axes("", "")
ax.curve(lambda t: 9.8 + 3 * math.sin(2 * math.pi * 2 * t), 0, 2, color=NAVY, sw=2.2)
ax.hline(11, color=RED); ax.hline(9.8, color=AMBER)
f.text(520, ax.Y(11) - 6, "threshold 11", size=9.5, color=RED, bold=True)
f.text(500, ax.Y(9.8) + 14, "rest = 9.8", size=9.5, color=AMBER, bold=True)
for k in range(4):
    t = 0.125 + 0.5 * k
    ax.pt(t, 12.8, label=f"step {k + 1}", color=RED, dx=-18, dy=-9, size=9.5)
f.text(300, 224, "time in seconds; 2 steps/s x 10 s = 20 steps", size=10.5, color=NAVY, bold=True)
f.text(300, 242, "samples 500 = 50 Hz x 10 s", size=10, color=SLATE)
```

```svgfig label="6.3" caption="The haversine triangle for Kathmandu (27.7172 N, 85.3240 E) and Pokhara (28.2096 N, 83.9856 E). The latitude difference of 0.4924 degrees is 54.75 km north and the longitude difference of 1.3384 degrees is 131.45 km west at the mean latitude, so the straight-line distance is about 142.4 km (haversine: a = 0.000124879, d = 2 x 6371 x asin(sqrt(a)) = 142.39 km). The road is longer because it follows river valleys."
f = Fig(580, 240)
f.box(10, 10, 560, 220, "", fill=SOFT, stroke="#cbd5e1")
kx, ky = 470, 190
px, py = 470 - 131.45 * 2.6, 190 - 54.75 * 2.6
f.line(px, py, kx, ky, color=RED, sw=2.4)
f.line(px, ky, kx, ky, color=NAVY, sw=1.6, dash=True)
f.line(px, py, px, ky, color=NAVY, sw=1.6, dash=True)
f.circle(kx, ky, 6, fill=RED, stroke=RED); f.circle(px, py, 6, fill=TEAL, stroke=TEAL)
f.text(kx, ky + 18, "Kathmandu", size=10.5, color=RED, bold=True)
f.text(px, py - 12, "Pokhara", size=10.5, color=TEAL, bold=True)
f.text((px + kx) / 2, ky + 18, "131.45 km west", size=10, color=NAVY, bold=True)
f.text(px - 8, (py + ky) / 2, "54.75 km north", size=10, color=NAVY, bold=True, anchor="end")
f.text((px + kx) / 2 + 20, (py + ky) / 2 - 12, "142.4 km", size=12, color=RED, bold=True)
f.text(30, 206, "R = 6371 km", size=10, color=SLATE, bold=True, anchor="start")
f.text(30, 222, "both formulas agree: 142.39 km", size=10, color=AMBER, bold=True, anchor="start")
```

```svgfig label="6.4" caption="The accuracy-power ladder for location (typical orders of magnitude; real values depend on the phone and the place). GPS is accurate to a few metres outdoors but is slow to start and uses the most power; Wi-Fi positioning is good to tens of metres in towns; cell-tower positioning gives hundreds of metres or more but costs almost nothing. The Fused Location Provider blends them, and an app should ask for the lowest accuracy that serves its purpose."
f = Fig(580, 230)
D = [("GPS", "3 - 10 m", "high power, slow start", 40, RED), ("Wi-Fi", "20 - 50 m", "medium power, fast", 110, AMBER), ("Cell tower", "300 m - 3 km", "low power, instant", 260, TEAL)]
f.text(10, 20, "accuracy (bar length = error, not to scale)", size=10, color=SLATE, bold=True, anchor="start")
for i, (n, a, p, w, c) in enumerate(D):
    y = 36 + i * 52
    f.text(10, y + 22, n, size=11, color=c, bold=True, anchor="start")
    f.box(100, y + 6, w, 28, a, fill=BLUE if i else MINT, stroke=c, size=10, bold=True)
    f.text(100 + w + 12, y + 24, p, size=10, color=SLATE, anchor="start")
f.text(290, 214, "ask for the lowest accuracy that does the job (coarse for weather, fine for navigation)", size=10, color=NAVY, bold=True)
```

```svgfig label="6.5" caption="Anatomy of a notification (section 6.5). The channel (here 'Alerts', importance high) decides sound and vibration and can be silenced by the user. The small icon, title and text are what the user reads. The content intent is a PendingIntent, created with FLAG_IMMUTABLE, that starts DetailActivity when the notification is tapped. Android 13 and later also need the POST_NOTIFICATIONS runtime permission."
f = Fig(580, 230)
f.box(10, 20, 270, 110, "", fill="#ffffff", stroke=SLATE, sw=2)
f.box(22, 34, 34, 34, "!", fill=ROSE, stroke=RED, size=16, bold=True)
f.text(70, 46, "Flood warning", size=12, color=NAVY, bold=True, anchor="start")
f.text(70, 66, "River level rising near your ward", size=10, color=SLATE, anchor="start")
f.text(22, 100, "Alerts  -  now", size=9, color=SLATE, anchor="start")
f.text(22, 118, "tap  ->  PendingIntent  ->  DetailActivity", size=9, color=TEAL, bold=True, anchor="start")
L = [("1  Channel 'alerts'", "importance, sound, vibration", 24), ("2  Small icon", "R.drawable.ic_alert", 56), ("3  Title + text", "setContentTitle / Text", 88), ("4  contentIntent", "PendingIntent.FLAG_IMMUTABLE", 120), ("5  POST_NOTIFICATIONS", "runtime permission (Android 13+)", 152)]
for k, (t, s, y) in enumerate(L):
    yy = 22 + k * 36
    f.text(300, yy, t, size=10.5, color=NAVY, bold=True, anchor="start")
    f.text(300, yy + 14, s, size=9, color=SLATE, anchor="start")
f.text(290, 220, "notify(1, n) posts it; setAutoCancel(true) removes it after the tap", size=10, color=AMBER, bold=True)
```

### 6.6.1 Eight guidelines for permissions, sensors and location

1. **Ask only for what you need.** A torch app has no reason to read contacts, and a calculator has no use for location. Every extra permission is a reason for the user to refuse or uninstall the app. Reviewers of the Play Store also flag over-asking.
2. **Ask at the moment of use.** Request the camera permission when the user taps "Take photo", not when the app opens. The user then understands the reason, and the grant rate is much higher. A KYC app for a bank can explain "we need the camera to read your citizenship card" at that screen.
3. **Always plan for a refusal.** If the user says no, offer a smaller feature such as picking an existing photo, or explain how to enable the permission in Settings. An app that closes after a denial is useless. After "don't ask again" the only route is the Settings screen.
4. **Unregister sensor listeners in onPause.** A listener left registered keeps the sensor chip and the processor awake, and the battery drains within hours. Register in onResume and unregister in onPause as in Unit 2. Choose the slowest rate that still serves the feature; 50 Hz is plenty for steps.
5. **Filter noisy sensor data.** Raw accelerometer values jump, so a step counter needs a threshold, a minimum gap between steps and often a low-pass filter (Figure 6.2). Without them one step may count twice. A fitness app for trekkers must also adapt to different walking speeds.
6. **Use the Fused Location Provider.** It blends GPS, Wi-Fi and cell data and chooses the cheapest source that meets the accuracy you ask for (Figure 6.4). Ask for coarse location for a weather or nearby-ward-office feature, and for fine location only for navigation. Stop updates when the screen closes.
7. **Compute distance with the right formula.** Straight-line distance on a sphere uses the haversine formula, 142.4 km for Kathmandu to Pokhara, while the road distance is longer. Do not treat latitude and longitude as flat x and y over long distances. A taxi or delivery app uses the haversine for a first estimate and a routing service for the real route.
8. **Respect the user in notifications.** Create channels so the user can silence one kind without disabling all, keep the text useful, and use FLAG_IMMUTABLE on the PendingIntent. Ask for the POST_NOTIFICATIONS permission on Android 13 when the value is clear. A flood or earthquake alert deserves a high-importance channel, while a promotion does not.

## Chapter summary

- Permissions are normal, dangerous (runtime), special or signature; ask minimally, in context, with a rationale and a fallback.
- Sensors deliver noisy values at chosen rates; unregister listeners in `onPause`; a magnitude-threshold step detector counted 20 steps in the simulated walk.
- Location uses GPS, network and fused providers; the haversine formula gives great-circle distance; trade accuracy against battery.
- CameraX, photo picker, QR scanning and Bluetooth/NFC extend the device's reach with their own permissions.
- Notifications need channels, a PendingIntent and (recent Android) a runtime permission; FCM delivers push messages.

## Practice

1. Distinguish normal and dangerous permissions with an example of each.
2. List three good practices when asking for a permission.
3. Why should sensor listeners be unregistered in `onPause`?
4. What is the accelerometer magnitude at rest and why?
5. Describe how a threshold step detector works and one improvement for real data.
6. Compare GPS and network location in accuracy and battery cost.
7. Compute the haversine inputs: convert 28.2096° to radians.
8. Why is the haversine distance shorter than the road distance?
9. What is a notification channel and why does it exist?
10. How does an FCM push message reach a notification on the phone?

::: note Answers and worked solutions
**1.** Normal: INTERNET (granted at install). Dangerous: CAMERA or ACCESS_FINE_LOCATION (user approves at runtime).
**2.** Ask only when the feature is used, explain why before the dialog, handle denial gracefully (and send the user to settings if they chose "don't ask again").
**3.** An active listener keeps the sensor running and drains the battery while the app is not in use.
**4.** About 9.8 m/s², because the sensor includes gravity.
**5.** It counts a step when the acceleration magnitude crosses a threshold upward, ignoring crossings that come too soon after the last step; real signals need smoothing (a low-pass filter) or an adaptive threshold.
**6.** GPS: accurate to metres outdoors but slow and power-hungry. Network (Wi-Fi/cell): coarser but fast and efficient.
**7.** 28.2096 × π/180 = **0.49235 rad**.
**8.** It is the great-circle (straight-line) distance over the earth's surface; roads wind around hills and rivers.
**9.** A user-controllable category with its own importance, sound and vibration, so the user can silence one kind of alert without disabling all.
**10.** The app obtains an FCM token and sends it to your server; the server sends a message for that token through FCM; the app's messaging service receives it and builds the notification.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the runtime-permission flow of Android with the camera as an example.**

*Introduction.* Android protects sensitive data and features with permissions declared in the manifest; dangerous permissions (camera, microphone, location, contacts) must also be granted by the user at run time (section 6.1, Figure 6.1).

1. **Declare.** Add `<uses-permission android:name="android.permission.CAMERA"/>` to the manifest.
2. **Check.** Call `ContextCompat.checkSelfPermission`; if it returns PERMISSION_GRANTED, start the camera.
3. **Rationale.** If `shouldShowRequestPermissionRationale` is true, the user has refused once, so explain in a sentence why the camera is needed.
4. **Request.** Launch the request through `registerForActivityResult(ActivityResultContracts.RequestPermission())`; the system shows its dialog.
5. **Result.** The callback receives granted or denied. Granted starts the camera; denied must leave the app usable, for example by letting the user pick an existing photo.
6. **Don't ask again.** After this choice the dialog no longer appears, and the app can only guide the user to Settings.

*Principles.* Ask only what you need, at the moment of need, with a reason and a fallback.

*Conclusion.* The flow is declare, check, explain, request and handle either result, so that the user stays in control.

**Q2 (5 marks). A walk produces the accelerometer magnitude 9.8 + 3 sin(2π · 2 t) m/s² sampled at 50 Hz for 10 s. How many steps does the threshold method count with threshold 11?**

*Introduction.* The accelerometer reports acceleration including gravity, about 9.8 m/s² at rest, and each footfall produces a peak (section 6.2, Figure 6.2).

1. **Signal.** The range is 9.8 ± 3, that is 6.8 to 12.8 m/s².
2. **Samples.** 50 Hz × 10 s = **500** samples.
3. **Period.** The frequency is 2 Hz, so one cycle lasts 0.5 s and contains one peak.
4. **Threshold crossing.** The signal exceeds 11 when sin(·) > (11 − 9.8) ÷ 3 = 0.4. That holds for about 0.18 s of every 0.5 s cycle.
5. **Counting rule.** Count a step when the value rises above 11 after being below it, and require at least 10 samples (0.2 s) since the last step.
6. **Result.** One step per cycle: 2 × 10 = **20 steps**, as the program prints.

*Note.* Real data are noisy, so real counters smooth the signal and adapt the threshold.

*Conclusion.* The method counts 20 steps; the threshold and the minimum gap prevent missed and double counts.

**Q3 (5 marks). Use the haversine formula to find the distance between Kathmandu (27.7172, 85.3240) and Pokhara (28.2096, 83.9856).**

*Introduction.* The haversine formula gives the great-circle distance on a sphere of radius R = 6371 km: a = sin²(Δφ/2) + cos φ₁ cos φ₂ sin²(Δλ/2), d = 2R · asin(√a) (section 6.3, Figure 6.3).

1. **Differences.** Δφ = 28.2096 − 27.7172 = 0.4924° = 0.008594 rad; Δλ = 83.9856 − 85.3240 = −1.3384° = −0.023359 rad.
2. **Compute a.** a = sin²(0.004297) + cos(27.7172°) cos(28.2096°) sin²(0.011680) = **0.000124879**.
3. **Root.** √a = 0.011175 and asin(0.011175) = 0.011175 rad.
4. **Distance.** d = 2 × 6371 × 0.011175 = **142.4 km**.
5. **Check.** The spherical law of cosines gives 142.39 km; the flat triangle of Figure 6.3 (54.75 km north, 131.45 km west) gives 142.40 km.
6. **Meaning.** This is the straight-line distance; the road, which follows the river valleys, is longer.

*Conclusion.* Kathmandu to Pokhara is about 142.4 km in a straight line.

**Q4 (10 marks). Describe the sensors and location services of an Android phone. How do GPS, Wi-Fi and the Fused Location Provider differ, and how should an app save battery?**

*Introduction.* The SensorManager exposes motion, position and environment sensors, and the location services estimate where the phone is (sections 6.2 and 6.3, Plate 6.1, Figure 6.4).

1. **Motion sensors.** The accelerometer reports acceleration in x, y, z including gravity; the gyroscope reports rotation rate; step counter and detector, gravity and rotation vector are derived from them. Both chips can sit on one MEMS die (Plate 6.1a).
2. **Position sensors.** The magnetometer gives a compass heading and the proximity sensor switches the screen off during a call.
3. **Environment sensors.** Light, pressure and temperature sensors vary by model.
4. **Using a sensor.** Register a `SensorEventListener` in onResume with a sampling rate and unregister in onPause.
5. **GPS.** Accurate to about 3–10 m outdoors; the phone needs signals from at least four satellites (three distances plus a clock correction, Plate 6.2); slow to start and the most power-hungry.
6. **Wi-Fi and cell positioning.** Wi-Fi gives tens of metres, cell towers hundreds of metres or more; both are fast and cheap.
7. **Fused Location Provider.** Part of Google Play services; it blends all sources and picks the cheapest that satisfies the requested priority and interval.
8. **Battery rules.** Ask for the lowest accuracy that is enough, use the longest interval, stop updates in onPause or when the screen closes, and ask for background location only when essential.

| Source | Typical accuracy | Power | Start-up |
|---|---|---|---|
| GPS | 3–10 m | High | Slow |
| Wi-Fi | 20–50 m | Medium | Fast |
| Cell tower | 300 m–3 km | Low | Instant |
| Fused | Chosen by priority | Lowest that fits | Fast |

*Conclusion.* Sensors and location are powerful but costly; a careful app registers listeners only while visible, filters noisy data and asks for the coarsest accuracy that serves its feature.

**Q5 (10 marks). Explain how an Android app creates and shows a notification. What is a notification channel and what is the role of a PendingIntent?**

*Introduction.* A notification reaches the user when the app is not on screen; it is built by an app and shown by the system's Notification Manager (section 6.5, Figure 6.5).

1. **Channel.** Since Android 8 every notification belongs to a NotificationChannel with an id, a name and an importance level; the user can silence a channel without losing the others.
2. **Creating it.** `NotificationChannel("alerts", "Alerts", IMPORTANCE_HIGH)` is registered once with the NotificationManager.
3. **Builder.** `NotificationCompat.Builder(this, "alerts")` with `setSmallIcon`, `setContentTitle` and `setContentText` describes what the user sees.
4. **PendingIntent.** `PendingIntent.getActivity(..., FLAG_IMMUTABLE)` wraps an Intent and gives the system the right to fire it later, in the name of the app, when the user taps.
5. **Immutability.** FLAG_IMMUTABLE stops another app changing the Intent's contents, which is a security rule on recent Android versions.
6. **Posting.** `NotificationManagerCompat.from(this).notify(1, n)` shows it; `setAutoCancel(true)` removes it after the tap.
7. **Permission.** Android 13 added the runtime POST_NOTIFICATIONS permission, requested like any dangerous permission.
8. **Push.** Firebase Cloud Messaging delivers a message from the server even when the app is not running, and the app converts it into a notification.

*Example.* A flood-warning app uses a high-importance channel and a PendingIntent that opens the detail screen; a promotion uses a low-importance channel.

*Conclusion.* A notification is a channel plus content plus a PendingIntent, shown with the user's permission, and channels give the user fine control.
