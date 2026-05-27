-keepattributes *Annotation*,Signature,InnerClasses,EnclosingMethod

# Kotlinx Serialization
-keepattributes RuntimeVisibleAnnotations,AnnotationDefault
-keep,includedescriptorclasses class com.neb.ians.**$$serializer { *; }
-keepclassmembers class com.neb.ians.** {
    *** Companion;
}
-keepclasseswithmembers class com.neb.ians.** {
    kotlinx.serialization.KSerializer serializer(...);
}

# Room
-keep class * extends androidx.room.RoomDatabase
-dontwarn androidx.room.paging.**

# Hilt
-keep class dagger.hilt.** { *; }
-keep class javax.inject.** { *; }

# Compose
-keep class androidx.compose.** { *; }

# PDF viewer
-keep class com.shockwave.** { *; }
-keep class com.github.barteksc.** { *; }

# Firebase
-keep class com.google.firebase.** { *; }
