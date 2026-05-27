# Compose / Material 3 keeps
-keep class androidx.compose.** { *; }
-keep class kotlin.Metadata { *; }
-keepclassmembers class * {
    @androidx.compose.runtime.Composable <methods>;
}

# Hilt
-keep class dagger.hilt.** { *; }
-keep class javax.inject.** { *; }
-keep class * extends androidx.lifecycle.ViewModel { <init>(...); }

# Room
-keep class androidx.room.RoomDatabase { *; }
-keep @androidx.room.Entity class * { *; }
-keep @androidx.room.Dao class * { *; }

# Kotlinx serialization / coroutines noise
-dontwarn kotlinx.coroutines.debug.**

# Crash readability
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile
