plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.ksp)
    alias(libs.plugins.hilt)
}

// Optional google-services.json — apply the gms plugin only when present so CI does not
// break when no Firebase config is committed. The plugin is declared (apply false) in the
// root build script, so the classpath is available even when we skip applying it here.
if (file("google-services.json").exists()) {
    apply(plugin = libs.plugins.gms.get().pluginId)
}

android {
    namespace = "com.neb.ians"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.neb.ians"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"

        vectorDrawables { useSupportLibrary = true }
        resourceConfigurations += listOf("en", "ne")
    }

    signingConfigs {
        create("release") {
            storeFile = file("${rootProject.projectDir}/keystore/nebians-release.jks")
            storePassword = "nebians2024"
            keyAlias = "nebians"
            keyPassword = "nebians2024"
        }
    }

    // Two release variants — one minSdk 24 ("legacy"), one minSdk 26 ("modern").
    flavorDimensions += "api"
    productFlavors {
        create("legacy") {
            dimension = "api"
            minSdk = 24
            versionNameSuffix = "-legacy"
            buildConfigField("String", "API_FLAVOR", "\"legacy\"")
        }
        create("modern") {
            dimension = "api"
            minSdk = 26
            versionNameSuffix = "-modern"
            buildConfigField("String", "API_FLAVOR", "\"modern\"")
        }
    }

    buildTypes {
        debug {
            isMinifyEnabled = false
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
            signingConfig = signingConfigs.getByName("release")
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            signingConfig = signingConfigs.getByName("release")
        }
    }

    // Rename APKs to NEBians-<flavor>-<versionName>-<gitSha>.apk
    val gitSha: String = try {
        val proc = ProcessBuilder("git", "rev-parse", "--short=8", "HEAD")
            .directory(rootDir)
            .redirectErrorStream(true)
            .start()
        proc.inputStream.bufferedReader().readText().trim().ifEmpty { "local" }
    } catch (_: Exception) { "local" }

    applicationVariants.all {
        outputs.all {
            val output = this as com.android.build.gradle.internal.api.BaseVariantOutputImpl
            output.outputFileName = "NEBians-${flavorName}-${versionName}-${gitSha}.apk"
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
        isCoreLibraryDesugaringEnabled = true
    }

    kotlinOptions {
        jvmTarget = "17"
        freeCompilerArgs += listOf(
            "-opt-in=kotlin.RequiresOptIn",
            "-opt-in=androidx.compose.material3.ExperimentalMaterial3Api",
            "-opt-in=androidx.compose.foundation.ExperimentalFoundationApi",
            "-opt-in=androidx.compose.animation.ExperimentalAnimationApi",
            "-opt-in=androidx.compose.ui.ExperimentalComposeUiApi"
        )
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
            excludes += "/META-INF/DEPENDENCIES"
            excludes += "META-INF/LICENSE*"
            excludes += "META-INF/NOTICE*"
        }
    }

    androidResources {
        generateLocaleConfig = false
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.lifecycle.runtime.compose)
    implementation(libs.androidx.activity.compose)
    implementation(libs.androidx.splashscreen)

    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.ui.graphics)
    implementation(libs.androidx.compose.ui.tooling.preview)
    implementation(libs.androidx.compose.material3)
    implementation(libs.androidx.compose.material.icons.extended)
    implementation(libs.androidx.compose.foundation)
    implementation(libs.androidx.compose.animation)
    debugImplementation(libs.androidx.compose.ui.tooling)

    implementation(libs.androidx.navigation.compose)

    implementation(libs.hilt.android)
    ksp(libs.hilt.compiler)
    implementation(libs.hilt.navigation.compose)
    implementation(libs.hilt.work)
    ksp(libs.hilt.androidx.compiler)

    implementation(libs.room.runtime)
    implementation(libs.room.ktx)
    ksp(libs.room.compiler)

    implementation(libs.datastore.preferences)
    implementation(libs.coil.compose)
    implementation(libs.kotlinx.coroutines.android)
    implementation(libs.work.runtime.ktx)

    // Firebase Messaging — wired but optional; needs google-services.json to actually connect.
    implementation(platform(libs.firebase.bom))
    implementation(libs.firebase.messaging)

    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.2")
}
