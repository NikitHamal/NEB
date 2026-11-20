package com.neb.ians.data.api

import kotlinx.serialization.Serializable

/** GET site-theme/: the festival theme the admins have live, if any (api/views_site_theme.py). */
@Serializable
data class ApiSiteTheme(
    val key: String = "everyday",
    val name: String = "",
    val festive: Boolean = false,
    val light: ApiThemeColors? = null,
    val dark: ApiThemeColors? = null,
    val motif: String? = null,
    val greeting: ApiThemeGreeting? = null,
    val card: ApiSeasonCard? = null,
    /** How Neby looks and behaves right now: an admin's pick, or the festival's dress. */
    val neby: ApiNebyConfig? = null,
    /** One-time "What's New / Try Out" release sheet configuration controlled by backend or local fallback. */
    @kotlinx.serialization.SerialName("whats_new")
    val whatsNew: ApiWhatsNewConfig? = null,
)

@Serializable
data class ApiWhatsNewConfig(
    @kotlinx.serialization.SerialName("release_key")
    val releaseKey: String = "1.8",
    val items: List<ApiWhatsNewItem> = emptyList(),
)

@Serializable
data class ApiWhatsNewItem(
    val id: String = "",
    val badge: String = "NEW",
    val title: String = "",
    val description: String = "",
    @kotlinx.serialization.SerialName("cta_label")
    val ctaLabel: String = "Try now",
    @kotlinx.serialization.SerialName("target_route")
    val targetRoute: String = "pathways",
    val kind: String = "pathways",
)

@Serializable
data class ApiNebyConfig(
    val look: String = "classic",
    val ambient: Boolean = true,
    val reactions: Boolean = true,
    /** The festival's own greeting animation (tika at Dashain, diyo at Tihar...), or null. */
    val greet: String? = null,
)

@Serializable
data class ApiThemeColors(
    val primary: String,
    val onPrimary: String,
    val primaryContainer: String,
    val onPrimaryContainer: String,
)

@Serializable
data class ApiThemeGreeting(val ne: String = "", val en: String = "")

@Serializable
data class ApiSeasonCard(val message: String = "", val cta: ApiSeasonCta? = null)

@Serializable
data class ApiSeasonCta(val label: String = "", val url: String = "")
