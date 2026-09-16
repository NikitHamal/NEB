# ============================================================================
# NEBians ProGuard Rules
# ============================================================================

# ----------------------------------------------------------------------------
# General Android Rules
# ----------------------------------------------------------------------------

# Keep annotations
-keepattributes *Annotation*
-keepattributes Signature
-keepattributes InnerClasses,EnclosingMethod
-keepattributes SourceFile,LineNumberTable

# Keep the application class
-keep public class * extends android.app.Application

# Keep all classes in the app package (data models, etc.)
-keep class com.neb.ians.data.model.** { *; }

# Prevent stripping of Parcelable
-keep class * implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator *;
}

# Keep Serializable classes
-keepclassmembers class * implements java.io.Serializable {
    static final long serialVersionUID;
    private static final java.io.ObjectStreamField[] serialPersistentFields;
    !static !transient <fields>;
    private void writeObject(java.io.ObjectOutputStream);
    private void readObject(java.io.ObjectInputStream);
    java.lang.Object writeReplace();
    java.lang.Object readResolve();
}

# Enum classes
-keepclassmembers enum * {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}

# ----------------------------------------------------------------------------
# Room Database
# ----------------------------------------------------------------------------

-keep class * extends androidx.room.RoomDatabase
-keep @androidx.room.Entity class *
-dontwarn androidx.room.paging.**

# Keep Room DAO methods
-keep interface * extends androidx.room.Dao {
    <methods>;
}

# Keep Room type converters
-keep class * extends androidx.room.TypeConverter {
    <methods>;
}
-keep @androidx.room.TypeConverters class *
-keep @androidx.room.TypeConverter class *

# ----------------------------------------------------------------------------
# Dagger / Hilt
# ----------------------------------------------------------------------------

-dontwarn dagger.**
-keep class dagger.** { *; }
-keep class javax.inject.** { *; }
-keep class * extends dagger.hilt.android.lifecycle.HiltViewModel

# Keep Hilt generated components
-keep class **_HiltModules* { *; }
-keep class **_HiltComponents* { *; }
-keep class *_Factory { *; }
-keep class *_MembersInjector { *; }

# Hilt entry points
-keep class * extends dagger.hilt.android.internal.managers.ViewComponentManager$FragmentContextWrapper { *; }
-keep @dagger.hilt.android.EarlyEntryPoint class * { *; }
-keep @dagger.hilt.InstallIn class * { *; }
-keep @dagger.Module class * { *; }
-keep @dagger.hilt.EntryPoint class * { *; }

# Keep @Inject constructors
-keepclasseswithmembernames class * {
    @javax.inject.Inject <init>(...);
}
-keepclasseswithmembernames class * {
    @javax.inject.Inject <fields>;
}

# ----------------------------------------------------------------------------
# Kotlin Serialization
# ----------------------------------------------------------------------------

-keepattributes RuntimeVisibleAnnotations,AnnotationDefault

# Keep serializers
-keep,includedescriptorclasses class com.neb.ians.**$$serializer { *; }
-keepclassmembers class com.neb.ians.** {
    *** Companion;
}
-keepclasseswithmembers class com.neb.ians.** {
    kotlinx.serialization.KSerializer serializer(...);
}

# Keep @Serializable classes
-if @kotlinx.serialization.Serializable class **
-keepclassmembers class <1> {
    static <1>$Companion Companion;
}
-if @kotlinx.serialization.Serializable class ** {
    static **$* *;
}
-keepclassmembers class <2>$<3> {
    kotlinx.serialization.KSerializer serializer(...);
}
-if @kotlinx.serialization.Serializable class ** {
    public static ** INSTANCE;
}
-keepclassmembers class <1> {
    public static <1> INSTANCE;
    kotlinx.serialization.KSerializer serializer(...);
}

# Kotlinx serialization core
-dontwarn kotlinx.serialization.**
-keep class kotlinx.serialization.** { *; }

# ----------------------------------------------------------------------------
# Kotlin Coroutines
# ----------------------------------------------------------------------------

-keepnames class kotlinx.coroutines.internal.MainDispatcherFactory {}
-keepnames class kotlinx.coroutines.CoroutineExceptionHandler {}
-keepclassmembers class kotlinx.coroutines.** {
    volatile <fields>;
}
-dontwarn kotlinx.coroutines.**

# ----------------------------------------------------------------------------
# Compose
# ----------------------------------------------------------------------------

-dontwarn androidx.compose.**

# ----------------------------------------------------------------------------
# Coil
# ----------------------------------------------------------------------------

-dontwarn coil.**

# ----------------------------------------------------------------------------
# DataStore
# ----------------------------------------------------------------------------

-keep class androidx.datastore.** { *; }
-dontwarn androidx.datastore.**

-keepclassmembers class com.neb.ians.data.needle.NeedleWebRuntime$Bridge {
    @android.webkit.JavascriptInterface <methods>;
}

# ----------------------------------------------------------------------------
# WorkManager
# ----------------------------------------------------------------------------

-keep class * extends androidx.work.Worker
-keep class * extends androidx.work.ListenableWorker {
    public <init>(android.content.Context, androidx.work.WorkerParameters);
}
-keep class * extends androidx.work.CoroutineWorker {
    public <init>(android.content.Context, androidx.work.WorkerParameters);
}

# ----------------------------------------------------------------------------
# OkHttp / Okio (transitive dependency via Coil)
# ----------------------------------------------------------------------------

-dontwarn okhttp3.**
-dontwarn okio.**
