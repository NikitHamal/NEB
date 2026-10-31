plugins {
    id("com.android.application") version "9.5.0" apply false
    id("com.android.library") version "9.5.0" apply false
    id("org.jetbrains.kotlin.plugin.compose") version "2.3.20" apply false
    id("com.google.devtools.ksp") version "2.3.9" apply false
    id("com.google.dagger.hilt.android") version "2.60.1" apply false
    id("org.jetbrains.kotlin.plugin.serialization") version "2.3.20" apply false
    id("com.google.gms.google-services") version "4.4.2" apply false
}

// AGP 9 ships built-in Kotlin and pulls KGP 2.2.10 as a runtime dependency.
// Declaring both here is how the AGP 9 release notes say to move above that
// floor; without it Gradle silently pins KGP back to 2.2.10 and the Kotlin
// compiler plugins below resolve against the wrong version.
buildscript {
    dependencies {
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:2.3.20")
        classpath("com.google.devtools.ksp:symbol-processing-gradle-plugin:2.3.9")
    }
}
