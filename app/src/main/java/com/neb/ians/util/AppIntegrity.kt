package com.neb.ians.util

import android.content.Context
import android.content.pm.ApplicationInfo
import android.content.pm.PackageManager
import android.os.Build
import android.os.Debug
import android.webkit.WebView
import com.neb.ians.BuildConfig
import com.neb.ians.speech.NativeSpeech
import java.security.MessageDigest
import java.util.Locale

/**
 * Non-destructive runtime integrity & anti-tamper guard against APK editors (APKTool, MT Manager,
 * NP Manager, Lucky Patcher), debuggable-manifest patching, package cloning, and Frida/Xposed hooks.
 */
object AppIntegrity {

    const val FLAG_DEBUGGER = 0x01
    const val FLAG_HOOK_MAP = 0x02
    const val FLAG_PATCH_PATH = 0x04
    const val FLAG_PKG_TAMPER = 0x08
    const val FLAG_DEBUGGABLE_PATCH = 0x10
    const val FLAG_CERT_MISMATCH = 0x20

    @Volatile
    private var cachedFlags: Int = -1

    @Volatile
    private var cachedCertSha256: String? = null

    @Volatile
    private var cachedCertRegistered: Boolean? = null

    /** Reconstructs `"com.neb.ians"` at runtime so global APK string replacement cannot rewrite the check. */
    private fun expectedPackage(): String {
        val codes = intArrayOf(0x30, 0x3c, 0x3e, 0x7d, 0x3d, 0x36, 0x31, 0x7d, 0x3a, 0x32, 0x3d, 0x20)
        val out = CharArray(codes.size) { i -> (codes[i] xor 0x53).toChar() }
        return String(out)
    }

    fun flags(context: Context): Int {
        val existing = cachedFlags
        if (existing >= 0) {
            return if (!BuildConfig.DEBUG && (Debug.isDebuggerConnected() || Debug.waitingForDebugger())) {
                existing or FLAG_DEBUGGER
            } else {
                existing
            }
        }
        val appCtx = context.applicationContext ?: context
        var mask = 0
        runCatching {
            if (!BuildConfig.DEBUG) {
                if (Debug.isDebuggerConnected() || Debug.waitingForDebugger()) {
                    mask = mask or FLAG_DEBUGGER
                }
                val appInfo = appCtx.applicationInfo
                if (appInfo != null && (appInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE) != 0) {
                    mask = mask or FLAG_DEBUGGABLE_PATCH
                }
                val expPkg = expectedPackage()
                if (appCtx.packageName != expPkg || !appCtx.filesDir.absolutePath.contains(expPkg)) {
                    mask = mask or FLAG_PKG_TAMPER
                }
                val srcDir = appInfo?.sourceDir.orEmpty()
                mask = mask or NativeSpeech.safeEnvFlags(srcDir)
                if (!isSigningCertRegistered(appCtx)) {
                    mask = mask or FLAG_CERT_MISMATCH
                }
            }
        }
        cachedFlags = mask
        return mask
    }

    /** True if the APK's manifest or package identity was patched by an APK editor in a release build. */
    fun isRepackagedOrDebugPatched(context: Context): Boolean {
        if (BuildConfig.DEBUG) return false
        val f = flags(context)
        return (f and (FLAG_PKG_TAMPER or FLAG_DEBUGGABLE_PATCH or FLAG_CERT_MISMATCH or FLAG_PATCH_PATH)) != 0
    }

    /** Enforces release WebView lockdown even if `android:debuggable="true"` was patched into AndroidManifest.xml. */
    fun enforceReleaseHardening(context: Context) {
        if (BuildConfig.DEBUG) return
        val f = flags(context)
        if ((f and (FLAG_DEBUGGABLE_PATCH or FLAG_DEBUGGER or FLAG_HOOK_MAP)) != 0) {
            runCatching { WebView.setWebContentsDebuggingEnabled(false) }
        }
    }

    @Suppress("DEPRECATION")
    fun signingCertSha256(context: Context): String {
        cachedCertSha256?.let { return it }
        val hash = runCatching {
            val pm = context.packageManager
            val sigs = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                val info = pm.getPackageInfo(context.packageName, PackageManager.GET_SIGNING_CERTIFICATES).signingInfo
                if (info == null) emptyArray()
                else if (info.hasMultipleSigners()) info.apkContentsSigners
                else info.signingCertificateHistory
            } else {
                pm.getPackageInfo(context.packageName, PackageManager.GET_SIGNATURES).signatures ?: emptyArray()
            }
            val first = sigs.firstOrNull() ?: return@runCatching ""
            val digest = MessageDigest.getInstance("SHA-256").digest(first.toByteArray())
            val sb = StringBuilder(digest.size * 2)
            for (b in digest) sb.append(String.format(Locale.US, "%02x", b.toInt() and 0xff))
            sb.toString()
        }.getOrDefault("")
        cachedCertSha256 = hash
        return hash
    }

    @Suppress("DEPRECATION")
    fun isSigningCertRegistered(context: Context): Boolean {
        cachedCertRegistered?.let { return it }
        val registered = BuildConfig.GOOGLE_ANDROID_CERT_HASHES
            .split(",")
            .map { it.trim().replace(":", "").lowercase(Locale.US) }
            .filter { it.length == 40 || it.length == 64 }
            .toSet()
        if (registered.isEmpty()) {
            cachedCertRegistered = true
            return true
        }
        val valid = runCatching {
            val pm = context.packageManager
            val sigs = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                val info = pm.getPackageInfo(context.packageName, PackageManager.GET_SIGNING_CERTIFICATES).signingInfo
                if (info == null) emptyArray()
                else if (info.hasMultipleSigners()) info.apkContentsSigners
                else info.signingCertificateHistory
            } else {
                pm.getPackageInfo(context.packageName, PackageManager.GET_SIGNATURES).signatures ?: emptyArray()
            }
            if (sigs.isEmpty()) return@runCatching true
            val sha1Digest = MessageDigest.getInstance("SHA-1")
            val sha256Digest = MessageDigest.getInstance("SHA-256")
            sigs.any { sig ->
                val bytes = sig.toByteArray()
                val sha1 = sha1Digest.digest(bytes).joinToString("") { "%02x".format(Locale.US, it.toInt() and 0xff) }
                val sha256 = sha256Digest.digest(bytes).joinToString("") { "%02x".format(Locale.US, it.toInt() and 0xff) }
                sha1 in registered || sha256 in registered
            }
        }.getOrDefault(true)
        cachedCertRegistered = valid
        return valid
    }
}
