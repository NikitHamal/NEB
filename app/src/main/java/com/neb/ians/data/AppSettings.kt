package com.neb.ians.data

import android.content.Context

class AppSettings(context: Context) {
    private val prefs = context.applicationContext.getSharedPreferences("neb_settings", Context.MODE_PRIVATE)

    fun isDarkMode(): Boolean = prefs.getBoolean(KEY_DARK_MODE, false)

    fun setDarkMode(enabled: Boolean) {
        prefs.edit().putBoolean(KEY_DARK_MODE, enabled).apply()
    }

    companion object {
        private const val KEY_DARK_MODE = "dark_mode"
    }
}
