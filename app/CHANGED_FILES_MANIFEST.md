# Changed Files Manifest — Native Production Pass

## Student app native updates
- `src/main/java/com/neb/ians/data/api/ApiService.kt`
  - Added result-checker request/response models.
  - Added native `/ajax/results/check/` Retrofit endpoint.
  - Added news-detail page endpoint.
- `src/main/java/com/neb/ians/data/news/NewsAnnouncement.kt`
  - Existing lightweight news card model retained.
- `src/main/java/com/neb/ians/data/news/NewsDetail.kt`
  - New native article-detail model.
- `src/main/java/com/neb/ians/data/repository/NewsRepository.kt`
  - Added article-detail loading/parsing/cache.
  - Hardened news list parsing and content cleanup.
- `src/main/java/com/neb/ians/data/repository/ResultRepository.kt`
  - New result checker repository.
- `src/main/java/com/neb/ians/data/results/ResultModels.kt`
  - New result UI/domain models.
- `src/main/java/com/neb/ians/ui/screens/results/ResultCheckerViewModel.kt`
  - New native result checker state, single lookup, bulk lookup, progress, and gradesheet state.
- `src/main/java/com/neb/ians/ui/screens/results/ResultCheckerScreen.kt`
  - Replaced WebView result checker with native Compose UI.
- `src/main/java/com/neb/ians/ui/screens/news/NewsDetailViewModel.kt`
  - New native news-detail view model.
- `src/main/java/com/neb/ians/ui/screens/news/NewsDetailScreen.kt`
  - Replaced WebView article detail with native Compose UI.
- `src/main/java/com/neb/ians/ui/Navigation.kt`
  - Related news now routes to the native detail screen instead of opening a browser URL.
- `src/main/res/xml/file_paths.xml`
  - Added cache export path for native CSV sharing.
- `STUDENT_NATIVE_PRODUCTION_NOTES.md`
  - Added production-pass notes and root integration instructions.

## Admin app module
- `admin/` is a separate Android application module with package `com.neb.ians.admin`.
- Includes production WebView admin shell, file uploads, downloads, cookies, external-link safety, and release signing config.

## Workflow
- `build-release-updated.yml` updates the supplied GitHub Actions workflow so it builds and uploads both student and admin app artifacts.
