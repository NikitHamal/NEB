# Consica Code ProGuard / R8 rules

# Keep Kotlinx Serialization metadata
-keepattributes *Annotation*, InnerClasses
-dontnote kotlinx.serialization.**
-keepclassmembers class **$$serializer { *; }
-keepclasseswithmembers class * {
    kotlinx.serialization.KSerializer serializer(...);
}
-keep,includedescriptorclasses class com.consica.code.**$$serializer { *; }
-keepclassmembers class com.consica.code.** {
    *** Companion;
}

# Room
-keep class * extends androidx.room.RoomDatabase { <init>(); }
-dontwarn androidx.room.paging.**

# WebView JS interface bridges
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# Keep enum values used by reflection / serialization
-keepclassmembers enum * { *; }

# Compose
-dontwarn org.jetbrains.annotations.**
