# Limitations (honest list)

- **Server-backed features are not in the desktop app:** forum, news, notifications, people, Neby AI, Study Lab/Space, Canvas, marketplace, uploads, analytics, result checker, credits. They need accounts/live data; the *Web app* tile and About page open the website. Email sign-in/sign-up/verify/forgot **are** real API calls, but the app keeps only the session token + username; nothing else is synced.
- **Google / GitHub sign-in** (OAuth through the system browser with a callback) is not implemented.
- **Profile is local.** Handle availability is validated by format only (Android asks the server). The portrait step picks a coloured monogram, not a photo.
- **Email flows were exercised against the live server only for the error path** (a wrong password returned the server's own message). I had no test account, so a *successful* login/signup/verify has not been run end to end.
- **Maths is linearised, not 2-D typeset:** `\frac{a}{b}` is shown as `a/b`; stacked fractions, matrices and big operators with limits are flattened (matrices/cases become lines). Vector/hat/bar accents use small raised marks (egui cannot place combining accents).
- **No in-app PDF viewer:** the built study-book PDFs open in the system viewer.
- **Text shaping:** no HarfBuzz, so complex Devanagari conjuncts depend on Poppins' precomposed glyphs.
- **Accessibility:** AccessKit is not enabled; keyboard navigation and focus rings exist, screen-reader support does not.
- **Windows binary was cross-compiled with mingw and could not be launched here** (no Windows/wine in the sandbox); the Linux build was run and screenshotted. A `windows-latest` CI workflow is provided as the native check. The mingw build needs an OpenGL 2+ driver at run time.
- **Content is read from the repo layout**, not embedded: the app needs `backend_python/web/data` (or a bundled `content/`) next to it. A bundle script makes a zip (~205 MB of figures/JSON; PDFs are optional and larger).
- Mac builds are untested.
