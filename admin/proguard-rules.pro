-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
-keep class android.webkit.** { *; }
-dontwarn android.webkit.**
