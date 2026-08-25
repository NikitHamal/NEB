package com.neb.ians.data.repository

import android.content.Context
import android.content.SharedPreferences
import android.util.Log
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

object SecurePrefs {

    private const val FILE_NAME = "nebians_secure_prefs"
    private const val KEY_AUTH_TOKEN = "auth_token"
    private const val FALLBACK_FILE = "nebians_secure_prefs_fallback"

    @Volatile
    private var prefs: SharedPreferences? = null

    private fun clearLegacyFallback(context: Context) {
        context.getSharedPreferences(FALLBACK_FILE, Context.MODE_PRIVATE)
            .edit()
            .clear()
            .apply()
    }

    fun init(context: Context): SharedPreferences? {
        prefs?.let { return it }
        try {
            val masterKey = MasterKey.Builder(context)
                .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
                .build()
            val sp = EncryptedSharedPreferences.create(
                context,
                FILE_NAME,
                masterKey,
                EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
                EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
            )
            prefs = sp
            clearLegacyFallback(context)
            return sp
        } catch (e: Exception) {
            clearLegacyFallback(context)
            Log.e("SecurePrefs", "EncryptedSharedPreferences init failed", e)
            return null
        }
    }

    fun getAuthToken(context: Context): String? {
        val sp = init(context)
        if (sp != null) {
            try {
                return sp.getString(KEY_AUTH_TOKEN, null)
            } catch (e: Exception) {
                Log.w("SecurePrefs", "Failed to read from EncryptedSharedPreferences", e)
            }
        }
        return null
    }

    fun setAuthToken(context: Context, token: String?) {
        val sp = init(context)
        if (sp != null) {
            try {
                sp.edit().apply {
                    if (token != null) putString(KEY_AUTH_TOKEN, token) else remove(KEY_AUTH_TOKEN)
                }.apply()
                return
            } catch (e: Exception) {
                Log.w("SecurePrefs", "Failed to write to EncryptedSharedPreferences", e)
            }
        }
        throw IllegalStateException("Secure credential storage is unavailable")
    }

    fun clearAuthToken(context: Context) {
        val sp = init(context)
        if (sp != null) {
            try {
                sp.edit().remove(KEY_AUTH_TOKEN).apply()
            } catch (e: Exception) {
                Log.w("SecurePrefs", "Failed to clear from EncryptedSharedPreferences", e)
            }
        }
        clearLegacyFallback(context)
    }
}