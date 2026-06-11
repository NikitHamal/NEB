# Consica Code ProGuard rules

# Keep Room entities and DAOs metadata
-keep class com.consica.code.data.local.entity.** { *; }

# Kotlin coroutines
-dontwarn kotlinx.coroutines.**

# Compose
-dontwarn androidx.compose.**

# Keep enum values used in persistence (stored by name)
-keepclassmembers enum com.consica.code.** {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}

# WebView JS bridge is not used; keep WebViewClient subclasses anyway
-keep class com.consica.code.ui.ecosystem.** { *; }
