-keepattributes *Annotation*
-keepattributes SourceFile,LineNumberTable

-keep class com.neb.ians.data.model.** { *; }
-keep class com.neb.ians.data.local.entity.** { *; }

-dontwarn okhttp3.**
-dontwarn okio.**
-keep class okhttp3.** { *; }

-keep class com.google.gson.** { *; }
-keepclassmembers class * {
    @com.google.gson.annotations.SerializedName <fields>;
}

-keep class androidx.room.** { *; }
-keep class * extends androidx.room.RoomDatabase
-keep @androidx.room.Entity class *
-keep @androidx.room.Dao interface *
