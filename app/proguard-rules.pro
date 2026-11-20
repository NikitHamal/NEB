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
-renamesourcefileattribute SourceFile
-optimizationpasses 5
-overloadaggressively
-allowaccessmodification

# Strip verbose/debug/info logs from release DEX so internal log strings and tags are not exposed
-assumenosideeffects class android.util.Log {
    public static boolean isLoggable(java.lang.String, int);
    public static int v(...);
    public static int d(...);
    public static int i(...);
}

# Keep the application class.
# AGP 9 turns on android.r8.strictFullModeForKeepRules, so a bare -keep no
# longer implies keeping the default constructor. Every class below is
# instantiated reflectively by the framework, so the constructor is kept
# explicitly rather than relying on the old implicit behaviour.
-keep public class * extends android.app.Application {
    public <init>();
}

# Keep all API & serializable data models and Retrofit interfaces in R8 full mode
-keep class com.neb.ians.data.model.** { *; }
-keep class com.neb.ians.data.api.** { *; }
-keep interface com.neb.ians.data.api.** { *; }
-keep class com.neb.ians.data.news.** { *; }
-keep @kotlinx.serialization.Serializable class com.neb.ians.** { *; }
-keepclassmembers,allowshrinking,allowobfuscation interface * {
    @retrofit2.http.* <methods>;
}
-dontwarn retrofit2.**

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

-keep class * extends androidx.room.RoomDatabase {
    public <init>();
}
-keep @androidx.room.Entity class * {
    public <init>();
}
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
-keep class * extends dagger.hilt.android.lifecycle.HiltViewModel {
    public <init>();
}
-keep class * extends dagger.hilt.android.internal.managers.ViewComponentManager$FragmentContextWrapper { *; }
-keep @dagger.hilt.android.EarlyEntryPoint class * { *; }
-keep @dagger.hilt.EntryPoint class * { *; }

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

-dontwarn kotlinx.serialization.**

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
# Compose & Coil & DataStore
# ----------------------------------------------------------------------------

-dontwarn androidx.compose.**
-dontwarn coil.**
-keepclassmembers class * extends androidx.datastore.preferences.protobuf.GeneratedMessageLite {
    <fields>;
}
-dontwarn androidx.datastore.**

# ----------------------------------------------------------------------------
# OkHttp / Okio (transitive dependency via Coil)
# ----------------------------------------------------------------------------

-dontwarn okhttp3.**
-dontwarn okio.**

# ----------------------------------------------------------------------------
# On-device speech (JNI): Whistle STT and Phonon TTS bridge in libneb_speech.so
# ----------------------------------------------------------------------------
-keep class com.neb.ians.speech.NativeSpeech { *; }
-keep interface com.neb.ians.speech.PcmSink { *; }
-keep class com.neb.ians.speech.PcmSink { *; }
-keepclasseswithmembers class * implements com.neb.ians.speech.PcmSink {
    public boolean onPcm(float[]);
}

# ----------------------------------------------------------------------------
# AndroidX Credentials & Google Identity (Loaded reflectively in R8 full mode)
# ----------------------------------------------------------------------------
-keep class androidx.credentials.CredentialProviderFactory { *; }
-keep class * implements androidx.credentials.CredentialProvider {
    public <init>(android.content.Context);
    public <init>();
    *;
}
-keep class androidx.credentials.playservices.** {
    public <init>(android.content.Context);
    public <init>();
    *;
}
-keep class com.google.android.libraries.identity.googleid.** { *; }
-dontwarn androidx.credentials.**
-dontwarn com.google.android.libraries.identity.googleid.**
