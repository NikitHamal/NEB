package com.neb.ians.data.theme

import android.content.Context
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiSiteTheme
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.serialization.json.Json
import java.util.Calendar
import javax.inject.Inject
import javax.inject.Singleton

/**
 * The festival theme the server has live. The last answer is kept on disk so the app opens
 * already dressed for the season, then refreshes at most every five minutes. The season card
 * on Home can be closed; that is remembered per theme per year, like on the web.
 */
@Singleton
class SiteThemeRepository @Inject constructor(
    @ApplicationContext context: Context,
    private val api: ApiService,
) {
    private val prefs = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
    private val json = Json { ignoreUnknownKeys = true }

    private val _theme = MutableStateFlow(load())
    val theme: StateFlow<ApiSiteTheme?> = _theme.asStateFlow()

    private val _dismissed = MutableStateFlow(prefs.getStringSet(DISMISSED, emptySet()).orEmpty())
    val dismissed: StateFlow<Set<String>> = _dismissed.asStateFlow()

    private var fetchedAt = 0L

    suspend fun refresh(force: Boolean = false) {
        val now = System.currentTimeMillis()
        if (!force && now - fetchedAt < FIVE_MINUTES) return
        val fresh = runCatching { api.getSiteTheme() }.getOrNull() ?: return
        fetchedAt = now
        _theme.value = fresh
        prefs.edit().putString(CACHED, json.encodeToString(ApiSiteTheme.serializer(), fresh)).apply()
    }

    fun dismissKey(theme: ApiSiteTheme) = "${theme.key}:${Calendar.getInstance().get(Calendar.YEAR)}"

    fun dismissCard(theme: ApiSiteTheme) {
        val next = _dismissed.value + dismissKey(theme)
        _dismissed.value = next
        prefs.edit().putStringSet(DISMISSED, next).apply()
    }

    private fun load(): ApiSiteTheme? = prefs.getString(CACHED, null)?.let { raw ->
        runCatching { json.decodeFromString(ApiSiteTheme.serializer(), raw) }.getOrNull()
    }

    companion object {
        /** NEBiansApp opens this file early so its disk read is done before MainActivity needs it. */
        const val PREFS = "nebians_site_theme"
        private const val CACHED = "theme_json"
        private const val DISMISSED = "dismissed"
        private const val FIVE_MINUTES = 5 * 60 * 1000L
    }
}
