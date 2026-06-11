# Consica Code ProGuard rules

# Kotlinx serialization
-keepattributes *Annotation*, InnerClasses
-dontnote kotlinx.serialization.AnnotationsKt
-keepclassmembers class kotlinx.serialization.json.** {
    *** Companion;
}
-keepclasseswithmembers class kotlinx.serialization.json.** {
    kotlinx.serialization.KSerializer serializer(...);
}
-keep,includedescriptorclasses class com.consica.code.**$$serializer { *; }
-keepclassmembers class com.consica.code.** {
    *** Companion;
}
-keepclasseswithmembers class com.consica.code.** {
    kotlinx.serialization.KSerializer serializer(...);
}

# Room
-keep class * extends androidx.room.RoomDatabase
-dontwarn androidx.room.paging.**

# WebView JS bridge (HTML preview sandbox)
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# Keep enums used in Room type converters / DataStore
-keepclassmembers enum com.consica.code.** { *; }
