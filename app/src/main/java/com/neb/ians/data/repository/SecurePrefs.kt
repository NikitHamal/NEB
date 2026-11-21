package com.neb.ians.data.repository

import android.content.Context
import android.content.SharedPreferences
import android.util.Base64
import android.util.Log
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
import com.neb.ians.util.AppIntegrity
import java.security.MessageDigest
import java.security.SecureRandom
import javax.crypto.Cipher
import javax.crypto.spec.GCMParameterSpec
import javax.crypto.spec.SecretKeySpec

object SecurePrefs {

    private const val FILE_NAME = "nebians_secure_prefs"
    private const val KEY_AUTH_TOKEN = "auth_token"
    private const val FALLBACK_FILE = "nebians_secure_prefs_fallback"
    private const val FALLBACK_AUTH_TOKEN = "auth_token"
    private const val SEAL_PREFIX = "v2:"

    @Volatile
    private var prefs: SharedPreferences? = null

    @Volatile
    private var initAttempted = false

    @Volatile
    private var fallbackPrefs: SharedPreferences? = null

    @Volatile
    private var token: String? = null

    @Volatile
    private var tokenRead = false

    /** True once the token has been read, after which [getAuthToken] is a field read. */
    val isTokenLoaded: Boolean get() = tokenRead

    private fun getFallback(context: Context): SharedPreferences {
        fallbackPrefs?.let { return it }
        val sp = context.applicationContext.getSharedPreferences(FALLBACK_FILE, Context.MODE_PRIVATE)
        fallbackPrefs = sp
        return sp
    }

    @Synchronized
    fun init(context: Context): SharedPreferences? {
        prefs?.let { return it }
        if (initAttempted) return null
        initAttempted = true
        val appCtx = context.applicationContext
        try {
            val sp = createEncryptedPrefs(appCtx)
            prefs = sp
            return sp
        } catch (firstErr: Exception) {
            try {
                appCtx.deleteSharedPreferences(FILE_NAME)
                val sp = createEncryptedPrefs(appCtx)
                prefs = sp
                return sp
            } catch (e: Exception) {
                Log.w("SecurePrefs", "EncryptedSharedPreferences init failed, using fallback", firstErr)
                return null
            }
        }
    }

    private fun createEncryptedPrefs(appCtx: Context): SharedPreferences {
        val masterKey = MasterKey.Builder(appCtx)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build()
        return EncryptedSharedPreferences.create(
            appCtx,
            FILE_NAME,
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        )
    }

    private fun deriveFallbackKey(context: Context): SecretKeySpec {
        val appCtx = context.applicationContext ?: context
        val cert = AppIntegrity.signingCertSha256(appCtx)
        val seed = "${appCtx.packageName}|$cert|neb-fallback-aes-v2"
        val keyBytes = MessageDigest.getInstance("SHA-256").digest(seed.toByteArray(Charsets.UTF_8))
        return SecretKeySpec(keyBytes, "AES")
    }

    private fun sealFallbackToken(context: Context, plain: String): String = runCatching {
        val iv = ByteArray(12).also { SecureRandom().nextBytes(it) }
        val cipher = Cipher.getInstance("AES/GCM/NoPadding")
        cipher.init(Cipher.ENCRYPT_MODE, deriveFallbackKey(context), GCMParameterSpec(128, iv))
        val ct = cipher.doFinal(plain.toByteArray(Charsets.UTF_8))
        val combined = ByteArray(iv.size + ct.size)
        System.arraycopy(iv, 0, combined, 0, iv.size)
        System.arraycopy(ct, 0, combined, iv.size, ct.size)
        SEAL_PREFIX + Base64.encodeToString(combined, Base64.NO_WRAP)
    }.getOrDefault("")

    private fun unsealFallbackToken(context: Context, raw: String): String? {
        if (!raw.startsWith(SEAL_PREFIX)) return raw
        return runCatching {
            val combined = Base64.decode(raw.removePrefix(SEAL_PREFIX), Base64.NO_WRAP)
            if (combined.size <= 12) return null
            val iv = combined.copyOfRange(0, 12)
            val ct = combined.copyOfRange(12, combined.size)
            val cipher = Cipher.getInstance("AES/GCM/NoPadding")
            cipher.init(Cipher.DECRYPT_MODE, deriveFallbackKey(context), GCMParameterSpec(128, iv))
            String(cipher.doFinal(ct), Charsets.UTF_8)
        }.getOrNull()
    }

    fun getAuthToken(context: Context): String? {
        if (AppIntegrity.isRepackagedOrDebugPatched(context)) return null
        if (tokenRead) return token
        synchronized(this) {
            if (!tokenRead) {
                token = readAuthToken(context)
                tokenRead = true
            }
            return token
        }
    }

    private fun readAuthToken(context: Context): String? {
        val sp = init(context)
        val fb = getFallback(context)
        if (sp != null) {
            try {
                val encVal = sp.getString(KEY_AUTH_TOKEN, null)
                if (!encVal.isNullOrBlank()) {
                    if (fb.contains(FALLBACK_AUTH_TOKEN)) {
                        fb.edit().remove(FALLBACK_AUTH_TOKEN).apply()
                    }
                    return encVal
                }
            } catch (e: Exception) {
                Log.w("SecurePrefs", "Failed to read from EncryptedSharedPreferences", e)
            }
        }
        val fbRaw = fb.getString(FALLBACK_AUTH_TOKEN, null) ?: return null
        val resolved = unsealFallbackToken(context, fbRaw) ?: return null
        if (sp != null) {
            runCatching {
                sp.edit().putString(KEY_AUTH_TOKEN, resolved).apply()
                fb.edit().remove(FALLBACK_AUTH_TOKEN).apply()
            }
        } else if (!fbRaw.startsWith(SEAL_PREFIX)) {
            val sealed = sealFallbackToken(context, resolved)
            if (sealed.isNotEmpty()) fb.edit().putString(FALLBACK_AUTH_TOKEN, sealed).apply()
        }
        return resolved
    }

    fun setAuthToken(context: Context, token: String?) {
        this.token = token
        tokenRead = true
        synchronized(this) {
            val sp = init(context)
            val fb = getFallback(context)
            var wrotePrimary = false
            if (sp != null) {
                try {
                    sp.edit().apply {
                        if (token != null) putString(KEY_AUTH_TOKEN, token) else remove(KEY_AUTH_TOKEN)
                    }.apply()
                    wrotePrimary = true
                } catch (e: Exception) {
                    Log.w("SecurePrefs", "Failed to write to EncryptedSharedPreferences", e)
                }
            }
            if (wrotePrimary || token == null) {
                if (fb.contains(FALLBACK_AUTH_TOKEN)) {
                    fb.edit().remove(FALLBACK_AUTH_TOKEN).apply()
                }
            } else {
                val sealed = sealFallbackToken(context, token)
                if (sealed.isNotEmpty()) {
                    fb.edit().putString(FALLBACK_AUTH_TOKEN, sealed).apply()
                }
            }
        }
    }

    fun clearAuthToken(context: Context) {
        token = null
        tokenRead = true
        synchronized(this) {
            val sp = init(context)
            if (sp != null) {
                try {
                    sp.edit().remove(KEY_AUTH_TOKEN).apply()
                } catch (e: Exception) {
                    Log.w("SecurePrefs", "Failed to clear from EncryptedSharedPreferences", e)
                }
            }
            getFallback(context).edit().remove(FALLBACK_AUTH_TOKEN).apply()
        }
    }
}
