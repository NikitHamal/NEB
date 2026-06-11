package com.consica.code.data.prefs

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.longPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import com.consica.code.domain.model.AgeGroup
import com.consica.code.domain.model.CodingInterest
import com.consica.code.domain.model.ExperienceLevel
import com.consica.code.domain.model.GuidanceLevel
import com.consica.code.domain.model.LearningGoal
import com.consica.code.domain.model.OnboardingProfile
import com.consica.code.domain.model.PlayerStats
import com.consica.code.domain.model.ThemeIntensity
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

data class AppSettings(
    val highContrast: Boolean = false,
    val reducedMotion: Boolean = false,
    val soundEnabled: Boolean = true,
    val guidanceLevel: GuidanceLevel = GuidanceLevel.FULL,
    val professionalModeEnabled: Boolean = false,
    val displayName: String = "",
)

@Singleton
class UserPreferencesRepository @Inject constructor(
    private val dataStore: DataStore<Preferences>,
) {
    private object Keys {
        val onboardingComplete = booleanPreferencesKey("onboarding_complete")
        val ageGroup = stringPreferencesKey("age_group")
        val goal = stringPreferencesKey("learning_goal")
        val experience = stringPreferencesKey("experience_level")
        val themeIntensity = stringPreferencesKey("theme_intensity")
        val interests = stringPreferencesKey("interests")
        val displayName = stringPreferencesKey("display_name")

        val highContrast = booleanPreferencesKey("high_contrast")
        val reducedMotion = booleanPreferencesKey("reduced_motion")
        val soundEnabled = booleanPreferencesKey("sound_enabled")
        val guidanceLevel = stringPreferencesKey("guidance_level")
        val proModeEnabled = booleanPreferencesKey("pro_mode_enabled")

        val xp = longPreferencesKey("xp")
        val sunCoins = longPreferencesKey("sun_coins")
        val waterDrops = longPreferencesKey("water_drops")
        val masteryPoints = longPreferencesKey("mastery_points")
        val proUnlocked = booleanPreferencesKey("pro_unlocked")
        val streakDays = intPreferencesKey("streak_days")
        val lastActiveEpochDay = longPreferencesKey("last_active_epoch_day")
    }

    val onboardingComplete: Flow<Boolean> =
        dataStore.data.map { it[Keys.onboardingComplete] ?: false }

    val profile: Flow<OnboardingProfile> = dataStore.data.map { prefs ->
        OnboardingProfile(
            ageGroup = prefs[Keys.ageGroup].toEnum(AgeGroup.KIDS),
            goal = prefs[Keys.goal].toEnum(LearningGoal.FUN),
            experience = prefs[Keys.experience].toEnum(ExperienceLevel.BRAND_NEW),
            themeIntensity = prefs[Keys.themeIntensity].toEnum(ThemeIntensity.PLAYFUL),
            interests = prefs[Keys.interests]
                ?.split(',')
                ?.filter { it.isNotBlank() }
                ?.mapNotNull { name -> CodingInterest.entries.find { it.name == name } }
                ?.toSet()
                ?: emptySet(),
        )
    }

    val settings: Flow<AppSettings> = dataStore.data.map { prefs ->
        AppSettings(
            highContrast = prefs[Keys.highContrast] ?: false,
            reducedMotion = prefs[Keys.reducedMotion] ?: false,
            soundEnabled = prefs[Keys.soundEnabled] ?: true,
            guidanceLevel = prefs[Keys.guidanceLevel].toEnum(GuidanceLevel.FULL),
            professionalModeEnabled = prefs[Keys.proModeEnabled] ?: false,
            displayName = prefs[Keys.displayName] ?: "",
        )
    }

    val stats: Flow<PlayerStats> = dataStore.data.map { prefs ->
        PlayerStats(
            xp = prefs[Keys.xp] ?: 0L,
            sunCoins = prefs[Keys.sunCoins] ?: 0L,
            waterDrops = prefs[Keys.waterDrops] ?: 0L,
            masteryPoints = prefs[Keys.masteryPoints] ?: 0L,
            streakDays = prefs[Keys.streakDays] ?: 0,
            professionalModeUnlocked = prefs[Keys.proUnlocked] ?: false,
        )
    }

    val lastActiveEpochDay: Flow<Long> =
        dataStore.data.map { it[Keys.lastActiveEpochDay] ?: 0L }

    suspend fun completeOnboarding(profile: OnboardingProfile) {
        dataStore.edit { prefs ->
            prefs[Keys.onboardingComplete] = true
            prefs[Keys.ageGroup] = profile.ageGroup.name
            prefs[Keys.goal] = profile.goal.name
            prefs[Keys.experience] = profile.experience.name
            prefs[Keys.themeIntensity] = profile.themeIntensity.name
            prefs[Keys.interests] = profile.interests.joinToString(",") { it.name }
            // Sensible adaptive defaults derived from age.
            prefs[Keys.guidanceLevel] = when (profile.ageGroup) {
                AgeGroup.KIDS -> GuidanceLevel.FULL
                AgeGroup.TEENS -> GuidanceLevel.BALANCED
                AgeGroup.ADULTS -> GuidanceLevel.MINIMAL
            }.name
            if (profile.ageGroup == AgeGroup.ADULTS) {
                prefs[Keys.proUnlocked] = true
                prefs[Keys.proModeEnabled] = true
            }
        }
    }

    suspend fun setAgeGroup(ageGroup: AgeGroup) = dataStore.edit { prefs ->
        prefs[Keys.ageGroup] = ageGroup.name
        if (ageGroup == AgeGroup.ADULTS) prefs[Keys.proUnlocked] = true
    }

    suspend fun setHighContrast(enabled: Boolean) =
        dataStore.edit { it[Keys.highContrast] = enabled }

    suspend fun setReducedMotion(enabled: Boolean) =
        dataStore.edit { it[Keys.reducedMotion] = enabled }

    suspend fun setSoundEnabled(enabled: Boolean) =
        dataStore.edit { it[Keys.soundEnabled] = enabled }

    suspend fun setGuidanceLevel(level: GuidanceLevel) =
        dataStore.edit { it[Keys.guidanceLevel] = level.name }

    suspend fun setProfessionalModeEnabled(enabled: Boolean) =
        dataStore.edit { it[Keys.proModeEnabled] = enabled }

    suspend fun setThemeIntensity(intensity: ThemeIntensity) =
        dataStore.edit { it[Keys.themeIntensity] = intensity.name }

    suspend fun setDisplayName(name: String) =
        dataStore.edit { it[Keys.displayName] = name.take(40) }

    suspend fun unlockProfessionalMode() =
        dataStore.edit { it[Keys.proUnlocked] = true }

    suspend fun addRewards(xp: Long = 0, sun: Long = 0, water: Long = 0, mastery: Long = 0) {
        dataStore.edit { prefs ->
            prefs[Keys.xp] = (prefs[Keys.xp] ?: 0L) + xp
            prefs[Keys.sunCoins] = (prefs[Keys.sunCoins] ?: 0L) + sun
            prefs[Keys.waterDrops] = (prefs[Keys.waterDrops] ?: 0L) + water
            prefs[Keys.masteryPoints] = (prefs[Keys.masteryPoints] ?: 0L) + mastery
        }
    }

    suspend fun updateStreak(streakDays: Int, epochDay: Long) {
        dataStore.edit { prefs ->
            prefs[Keys.streakDays] = streakDays
            prefs[Keys.lastActiveEpochDay] = epochDay
        }
    }

    /** Clears all progress but keeps accessibility settings and onboarding choices. */
    suspend fun resetProgress() {
        dataStore.edit { prefs ->
            prefs[Keys.xp] = 0L
            prefs[Keys.sunCoins] = 0L
            prefs[Keys.waterDrops] = 0L
            prefs[Keys.masteryPoints] = 0L
            prefs[Keys.streakDays] = 0
            prefs[Keys.lastActiveEpochDay] = 0L
            prefs[Keys.proUnlocked] = false
            prefs[Keys.proModeEnabled] = false
        }
    }

    private inline fun <reified T : Enum<T>> String?.toEnum(default: T): T =
        this?.let { value -> enumValues<T>().find { it.name == value } } ?: default
}
