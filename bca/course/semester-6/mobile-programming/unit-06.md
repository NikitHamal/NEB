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
