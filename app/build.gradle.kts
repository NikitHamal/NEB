plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.plugin.compose")
    id("com.google.devtools.ksp")
    id("com.google.dagger.hilt.android")
    id("org.jetbrains.kotlin.plugin.serialization")
    id("com.google.gms.google-services")
}

android {
    namespace = "com.neb.ians"
    compileSdk = 36
    ndkVersion = "27.0.12077973"

    defaultConfig {
        applicationId = "com.neb.ians"
        minSdk = 24
        targetSdk = 36
        versionCode = 27
        versionName = "1.7.3"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {
            useSupportLibrary = true
        }
        androidResources {
            localeFilters += listOf("en", "ne")
        }
        ndk {
            // Whistle (speech to text) ships for arm64 and armv7; Phonon (text to speech)
            // for arm64. x86_64 builds a stub so emulators still install and run.
            abiFilters += listOf("arm64-v8a", "armeabi-v7a", "x86_64")
        }
    }

    externalNativeBuild {
        cmake {
            path = file("src/main/cpp/CMakeLists.txt")
            version = "3.22.1"
        }
    }

    signingConfigs {
        create("release") {
            storeFile = file("${rootProject.projectDir}/nebians-release.keystore")
            storePassword = System.getenv("KEYSTORE_PASSWORD") ?: project.findProperty("KEYSTORE_PASSWORD") as? String
                ?: throw GradleException("KEYSTORE_PASSWORD not set")
            keyAlias = System.getenv("KEY_ALIAS") ?: project.findProperty("KEY_ALIAS") as? String ?: "nebians"
            keyPassword = System.getenv("KEY_PASSWORD") ?: project.findProperty("KEY_PASSWORD") as? String
                ?: throw GradleException("KEY_PASSWORD not set")
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            signingConfig = signingConfigs.getByName("release")
        }
        debug {
            isMinifyEnabled = false
            isDebuggable = true
        }
    }

    flavorDimensions += "target"
    productFlavors {
        create("modern") {
            dimension = "target"
            minSdk = 28
            signingConfig = signingConfigs.getByName("release")
        }
        create("legacy") {
            dimension = "target"
            minSdk = 24
            signingConfig = signingConfigs.getByName("release")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }

    packaging {
        resources {
            excludes += listOf(
                "/META-INF/{AL2.0,LGPL2.1}",
                "/META-INF/*.version",
                "/META-INF/com/android/build/gradle/**",
                "/META-INF/DEPENDENCIES",
                "/META-INF/LICENSE*",
                "/META-INF/NOTICE*",
                "DebugProbesKt.bin",
                "kotlin-tooling-metadata.json"
            )
        }
        jniLibs {
            // Compress native libraries inside the APK: the 7 MB Phonon library shrinks the
            // download by about two thirds. Android extracts them once at install time.
            useLegacyPackaging = true
        }
    }
}

kotlin {
    compilerOptions {
        jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17
    }
}

ksp {
    arg("room.schemaLocation", "$projectDir/schemas")
}

composeCompiler {
    stabilityConfigurationFiles.add(rootProject.layout.projectDirectory.file("compose_stability.conf"))
}

dependencies {
    // Compose BOM
    val composeBom = platform("androidx.compose:compose-bom:2025.10.00")
    implementation(composeBom)
    androidTestImplementation(composeBom)

    // Compose UI
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")

    // Material 3
    implementation("androidx.compose.material3:material3:1.5.0-alpha10")
    implementation("androidx.compose.material:material-icons-extended:1.7.8")

// Activity Compose
    implementation("androidx.activity:activity-compose:1.9.3")

// Core KTX
    implementation("androidx.core:core-ktx:1.15.0")
    implementation("androidx.webkit:webkit:1.12.1")

// Lifecycle + ViewModel Compose
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.7")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.8.7")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.7")

// Navigation Compose
    implementation("androidx.navigation:navigation-compose:2.8.5")

// Room
    implementation("androidx.room:room-runtime:2.8.5")
    implementation("androidx.room:room-ktx:2.8.5")
    ksp("androidx.room:room-compiler:2.8.5")

// Hilt
    implementation("com.google.dagger:hilt-android:2.60.1")
    ksp("com.google.dagger:hilt-android-compiler:2.60.1")
    implementation("androidx.hilt:hilt-navigation-compose:1.3.0")
    implementation("androidx.hilt:hilt-work:1.3.0")
    ksp("androidx.hilt:hilt-compiler:1.3.0")

// Coil Compose
    implementation("io.coil-kt:coil-compose:2.7.0")

// Installs the baseline profile (src/main/baseline-prof.txt) on sideloaded installs too
    implementation("androidx.profileinstaller:profileinstaller:1.4.1")

// DataStore Preferences
    implementation("androidx.datastore:datastore-preferences:1.1.1")

// Encrypted SharedPreferences (auth token security)
    implementation("androidx.security:security-crypto:1.1.0-alpha06")

// WorkManager
    implementation("androidx.work:work-runtime-ktx:2.10.0")

// Kotlin Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.9.0")

// Kotlinx Serialization
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.7.3")

// Retrofit & OkHttp
    implementation("com.squareup.retrofit2:retrofit:2.11.0")
    implementation("com.squareup.retrofit2:converter-kotlinx-serialization:2.11.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")

// Firebase BoM and FCM
    implementation(platform("com.google.firebase:firebase-bom:33.6.0"))
    implementation("com.google.firebase:firebase-messaging-ktx")

// Credential Manager (Google Sign-In)
    implementation("androidx.credentials:credentials:1.3.0")
    implementation("androidx.credentials:credentials-play-services-auth:1.3.0")
    implementation("com.google.android.libraries.identity.googleid:googleid:1.1.1")

// Browser (Custom Tabs for GitHub OAuth)
    implementation("androidx.browser:browser:1.8.0")

// Media3 (ExoPlayer) for video/audio playback
    implementation("androidx.media3:media3-exoplayer:1.5.1")
    implementation("androidx.media3:media3-ui:1.5.1")

// Google Play In-App Update
    implementation("com.google.android.play:app-update:2.1.0")
    implementation("com.google.android.play:app-update-ktx:2.1.0")

    // Testing
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
}
