plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

val appVersionName = "1.0.0"

android {
    namespace = "com.neb.ians"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.neb.ians"
        minSdk = 23
        targetSdk = 36
        versionCode = 1
        versionName = appVersionName
    }

    signingConfigs {
        create("release") {
            storeFile = file("${rootProject.projectDir}/keystore/nebians-release.jks")
            storePassword = "nebians2024"
            keyAlias = "nebians"
            keyPassword = "nebians2024"
        }
    }

    flavorDimensions += "androidVersion"
    productFlavors {
        create("legacy") {
            dimension = "androidVersion"
            minSdk = 23
            versionNameSuffix = "-android6"
        }
        create("modern") {
            dimension = "androidVersion"
            minSdk = 29
            versionNameSuffix = "-android10"
        }
    }

    buildTypes {
        debug {
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            signingConfig = signingConfigs.getByName("release")
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlin {
        compilerOptions {
            jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17)
        }
    }

    buildFeatures {
        compose = true
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    implementation(platform("androidx.compose:compose-bom:2026.05.01"))
    implementation(platform("com.google.firebase:firebase-bom:34.13.0"))

    implementation("androidx.core:core-ktx:1.18.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.10.0")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.10.0")
    implementation("androidx.activity:activity-compose:1.13.0")
    implementation("androidx.navigation:navigation-compose:2.9.8")
    implementation("androidx.datastore:datastore-preferences:1.2.1")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.11.0")
    implementation("com.google.firebase:firebase-messaging")

    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}

tasks.register<Exec>("printVersionName") {
    group = "versioning"
    description = "Prints the base app version name for CI artifact naming."
    commandLine("sh", "-c", "printf '%s\\n' '$appVersionName'")
}
