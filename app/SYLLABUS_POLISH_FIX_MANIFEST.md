# Syllabus Native Polish Fix

## Scope
This pass updates only the Android native syllabus detail experience.
The backend API added in the previous pass is unchanged.

## UI/UX changes
- Hides the app bottom navigation while a syllabus subject detail is open.
- Hides the Library top bar, title row, upload/filter actions, and Library/Syllabus/Interactive tab header while a syllabus subject detail is open.
- Keeps the interactive breadcrumb as the only top navigation on the syllabus detail screen.
- Removes the extra subject title card that did not exist on the website subject page.
- Tightens the chapter picker, viewer spacing, bottom spacer, and subtabs to match the web subject page more closely.
- Groups solved Q&A content by section heading, matching the web page structure better.
- Keeps the implementation native Kotlin/Jetpack Compose; no WebView was added.
- Does not add the Neby AI / AI chat tab to the Android syllabus page.

## Files changed in this polish pass
- `src/main/java/com/neb/ians/ui/Navigation.kt`
- `src/main/java/com/neb/ians/ui/screens/library/LibraryScreen.kt`
- `src/main/java/com/neb/ians/ui/screens/library/SyllabusSubjectDetailContent.kt`
