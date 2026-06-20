# NEBians Admin Android App

This is a separate Android application module for the NEBians admin surface.

## Why WebView for admin
The existing admin panel is server-rendered and includes dashboard, users, push notifications, resources, syllabus/chapter management, pending review, resource requests, forum moderation, news/announcements, AI bots, study spaces, account deletion requests, upload forms, CSRF/session auth, downloads, and file inputs.

Wrapping the live `/admin/` panel inside a hardened WebView preserves those controls pixel-perfectly and avoids duplicating admin business logic in a second client.

## Build integration
Add this module to the root `settings.gradle.kts`:

```kotlin
include(":admin")
```

Then use the included updated GitHub Actions workflow. It builds:

- Student app modern APK/AAB
- Admin app modern APK/AAB
- Optional student/admin legacy APKs when `build_legacy=true`

## Package
- Application ID: `com.neb.ians.admin`
- Start URL: `https://nebians.consica.com.np/admin/`
- Uploads: Web file chooser enabled for images, PDFs, CSV/XLS/XLSX, and generic admin uploads
- Downloads: exported through Android DownloadManager into Downloads
- Cookies/session: persisted through Android WebView CookieManager
