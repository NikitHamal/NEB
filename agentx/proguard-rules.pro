# AgentX ProGuard rules (mirrors NEBians keeps)
-keep public class * extends android.app.Application
-keep class com.agentx.app.data.** { *; }
-keep class * implements android.os.Parcelable { *; }
-keep class * implements java.io.Serializable { *; }
-keepattributes Signature, InnerClasses, EnclosingMethod, *Annotation*
-keep enum ** { *; }
# Room
-keep class * extends androidx.room.RoomDatabase
-keep @androidx.room.Entity class *
-keep @androidx.room.Dao class *
-keep @androidx.room.TypeConverter class *
-dontwarn androidx.room.**
# Hilt / Dagger
-keep class dagger.hilt.** { *; }
-keep class javax.inject.** { *; }
-keepclasseswithmembernames class * { @javax.inject.Inject <init>(...); }
-keepclasseswithmembernames class * { @dagger.Provides <methods>; }
-keep class **_Factory { *; }
-keep class **_MembersInjector { *; }
-keep @dagger.hilt.** class *
-keep @dagger.Module class *
# Kotlinx serialization
-keepattributes RuntimeVisibleAnnotations, AnnotationDefault
-keep class kotlinx.serialization.** { *; }
-dontwarn kotlinx.serialization.**
-keepclassmembers class **$$serializer { *; }
-keepclassmembers class **$Companion { kotlinx.serialization.KSerializer serializer(...); }
# DataStore / WorkManager
-keep class androidx.datastore.** { *; }
-dontwarn androidx.datastore.**
-keep class * extends androidx.work.Worker { public <init>(android.content.Context,androidx.work.WorkerParameters); }
-keep class * extends androidx.work.CoroutineWorker { public <init>(android.content.Context,androidx.work.WorkerParameters); }
# Needle WebView JS bridge
-keepclassmembers class com.agentx.app.data.engine.NeedleRuntime$Bridge {
    @android.webkit.JavascriptInterface <methods>;
}
# Compose / Coil / Coroutines / OkHttp
-dontwarn androidx.compose.**
-dontwarn kotlinx.coroutines.**
-dontwarn okhttp3.**
-dontwarn okio.**
