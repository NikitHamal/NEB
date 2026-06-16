package com.neb.ians.data.repository

import android.content.Context
import android.content.SharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

object SecurePrefs {

    private const val FILE_NAME = "nebians_secure_prefs"
    private const val KEY_AUTH_TOKEN = "auth_token"

    @Volatile
    private var prefs: SharedPreferences? = null

    fun init(context: Context): SharedPreferences {
        prefs?.let { return it }
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
        return sp
    }

    fun getAuthToken(context: Context): String? {
        return init(context).getString(KEY_AUTH_TOKEN, null)
    }

    fun setAuthToken(context: Context, token: String?) {
        init(context).edit().apply {
            if (token != null) putString(KEY_AUTH_TOKEN, token) else remove(KEY_AUTH_TOKEN)
        }.apply()
    }

    fun clearAuthToken(context: Context) {
        init(context).edit().remove(KEY_AUTH_TOKEN).apply()
    }
}