plugins {
    id("com.android.application") version "9.5.0" apply false
    id("com.android.library") version "9.5.0" apply false
    id("org.jetbrains.kotlin.android") version "2.0.21" apply false
    id("org.jetbrains.kotlin.plugin.compose") version "2.0.21" apply false
    id("com.google.devtools.ksp") version "2.0.21-1.0.28" apply false
    id("com.google.dagger.hilt.android") version "2.53.1" apply false
    id("org.jetbrains.kotlin.plugin.serialization") version "2.0.21" apply false
    id("com.google.gms.google-services") version "4.4.2" apply false
}

// AGP 9 keeps a runtime dependency on KGP 2.2.10 even with built-in Kotlin
// switched off, so Gradle resolves Kotlin up to 2.2.10 while KSP stayed on
// 2.0.21-1.0.28 - hence "unexpected jvm signature V" from KspAAWorkerAction.
// The AGP 9.0 release notes document pinning both back down with strict
// versions; 2.0.0 is the floor. Drop this block when the Material3 Expressive
// call sites are migrated and the stack can move forward as a whole.
buildscript {
    dependencies {
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin") {
            version { strictly("2.0.21") }
        }
        classpath("com.google.devtools.ksp:symbol-processing-gradle-plugin") {
            version { strictly("2.0.21-1.0.28") }
        }
    }
}
