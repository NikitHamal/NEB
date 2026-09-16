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
    private const val FALLBACK_AUTH_TOKEN = "auth_token"

    @Volatile
    private var prefs: SharedPreferences? = null

    @Volatile
    private var fallbackPrefs: SharedPreferences? = null

    @Volatile
    private var masterKey: MasterKey? = null

    private fun getMasterKey(context: Context): MasterKey {
        masterKey?.let { return it }
        return synchronized(this) {
            masterKey?.let { return it }
            val mk = MasterKey.Builder(context.applicationContext)
                .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
                .build()
            masterKey = mk
            mk
        }
    }

    private fun getFallback(context: Context): SharedPreferences {
        fallbackPrefs?.let { return it }
        val sp = context.getSharedPreferences(FALLBACK_FILE, Context.MODE_PRIVATE)
        fallbackPrefs = sp
        return sp
    }

    fun init(context: Context): SharedPreferences? {
        prefs?.let { return it }
        try {
            val sp = EncryptedSharedPreferences.create(
                context.applicationContext,
                FILE_NAME,
                getMasterKey(context),
                EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
                EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
            )
            prefs = sp
            return sp
        } catch (e: Exception) {
            Log.w("SecurePrefs", "EncryptedSharedPreferences init failed, using fallback", e)
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
        return getFallback(context).getString(FALLBACK_AUTH_TOKEN, null)
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
        getFallback(context).edit().apply {
            if (token != null) putString(FALLBACK_AUTH_TOKEN, token) else remove(FALLBACK_AUTH_TOKEN)
        }.apply()
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
        getFallback(context).edit().remove(FALLBACK_AUTH_TOKEN).apply()
    }
}