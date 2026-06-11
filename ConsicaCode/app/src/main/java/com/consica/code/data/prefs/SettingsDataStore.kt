package com.consica.code.data.prefs

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.floatPreferencesKey
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.longPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.core.stringSetPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.ExperienceLevel
import com.consica.code.core.model.GuidanceLevel
import com.consica.code.core.model.Interest
import com.consica.code.core.model.LearningGoal
import com.consica.code.core.model.ThemeIntensity
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "consica_settings")

/** Typed wrapper over Preferences DataStore. Fully offline, local-only. */
class SettingsDataStore(private val context: Context) {

    private object Keys {
        val onboarding = booleanPreferencesKey("onboarding_complete")
        val age = stringPreferencesKey("age_group")
        val goal = stringPreferencesKey("goal")
        val experience = stringPreferencesKey("experience")
        val intensity = stringPreferencesKey("intensity")
        val interests = stringSetPreferencesKey("interests")
        val guidance = stringPreferencesKey("guidance")
        val highContrast = booleanPreferencesKey("high_contrast")
        val reducedMotion = booleanPreferencesKey("reduced_motion")
        val sound = booleanPreferencesKey("sound")
        val fontScale = floatPreferencesKey("font_scale")
        val darkMode = stringPreferencesKey("dark_mode")
        val pro = booleanPreferencesKey("pro_unlocked")
        val xp = intPreferencesKey("xp")
        val sun = intPreferencesKey("sun")
        val water = intPreferencesKey("water")
        val mastery = intPreferencesKey("mastery")
        val streak = intPreferencesKey("streak")
        val bestStreak = intPreferencesKey("best_streak")
        val lastActive = longPreferencesKey("last_active_epoch_day")
    }

    val prefs: Flow<UserPrefs> = context.dataStore.data.map { p ->
        UserPrefs(
            onboardingComplete = p[Keys.onboarding] ?: false,
            ageGroup = AgeGroup.from(p[Keys.age]),
            goal = LearningGoal.from(p[Keys.goal]),
            experience = ExperienceLevel.from(p[Keys.experience]),
            intensity = ThemeIntensity.from(p[Keys.intensity]),
            interests = (p[Keys.interests] ?: emptySet()).mapNotNull { Interest.from(it) }.toSet(),
            guidance = GuidanceLevel.from(p[Keys.guidance]),
            highContrast = p[Keys.highContrast] ?: false,
            reducedMotion = p[Keys.reducedMotion] ?: false,
            soundEnabled = p[Keys.sound] ?: true,
            fontScale = p[Keys.fontScale] ?: 1f,
            darkMode = DarkMode.from(p[Keys.darkMode]),
            proUnlocked = p[Keys.pro] ?: false,
            xp = p[Keys.xp] ?: 0,
            sunCoins = p[Keys.sun] ?: 0,
            waterDrops = p[Keys.water] ?: 0,
            masteryPoints = p[Keys.mastery] ?: 0,
            currentStreak = p[Keys.streak] ?: 0,
            bestStreak = p[Keys.bestStreak] ?: 0,
            lastActiveEpochDay = p[Keys.lastActive] ?: 0L,
        )
    }

    suspend fun completeOnboarding(
        age: AgeGroup, goal: LearningGoal, experience: ExperienceLevel,
        intensity: ThemeIntensity, interests: Set<Interest>, guidance: GuidanceLevel,
    ) = context.dataStore.edit { p ->
        p[Keys.onboarding] = true
        p[Keys.age] = age.id
        p[Keys.goal] = goal.id
        p[Keys.experience] = experience.id
        p[Keys.intensity] = intensity.id
        p[Keys.interests] = interests.map { it.id }.toSet()
        p[Keys.guidance] = guidance.id
    }

    suspend fun setAgeGroup(age: AgeGroup) = edit { it[Keys.age] = age.id }
    suspend fun setIntensity(intensity: ThemeIntensity) = edit { it[Keys.intensity] = intensity.id }
    suspend fun setGuidance(level: GuidanceLevel) = edit { it[Keys.guidance] = level.id }
    suspend fun setHighContrast(on: Boolean) = edit { it[Keys.highContrast] = on }
    suspend fun setReducedMotion(on: Boolean) = edit { it[Keys.reducedMotion] = on }
    suspend fun setSound(on: Boolean) = edit { it[Keys.sound] = on }
    suspend fun setFontScale(scale: Float) = edit { it[Keys.fontScale] = scale }
    suspend fun setDarkMode(mode: DarkMode) = edit { it[Keys.darkMode] = mode.id }
    suspend fun setProUnlocked(on: Boolean) = edit { it[Keys.pro] = on }

    /** Atomically add gamification rewards. */
    suspend fun addRewards(xp: Int = 0, sun: Int = 0, water: Int = 0, mastery: Int = 0) =
        context.dataStore.edit { p ->
            p[Keys.xp] = (p[Keys.xp] ?: 0) + xp
            p[Keys.sun] = (p[Keys.sun] ?: 0) + sun
            p[Keys.water] = (p[Keys.water] ?: 0) + water
            p[Keys.mastery] = (p[Keys.mastery] ?: 0) + mastery
        }

    /** Update streak based on the current epoch-day. Returns nothing; reads via [prefs]. */
    suspend fun touchStreak(todayEpochDay: Long) = context.dataStore.edit { p ->
        val last = p[Keys.lastActive] ?: 0L
        if (last == todayEpochDay) return@edit
        val newStreak = if (last == todayEpochDay - 1) (p[Keys.streak] ?: 0) + 1 else 1
        p[Keys.streak] = newStreak
        p[Keys.lastActive] = todayEpochDay
        if (newStreak > (p[Keys.bestStreak] ?: 0)) p[Keys.bestStreak] = newStreak
    }

    suspend fun resetProgress() = context.dataStore.edit { p ->
        p[Keys.xp] = 0; p[Keys.sun] = 0; p[Keys.water] = 0; p[Keys.mastery] = 0
        p[Keys.streak] = 0; p[Keys.bestStreak] = 0; p[Keys.lastActive] = 0L
        p[Keys.pro] = false
    }

    private suspend fun edit(block: (androidx.datastore.preferences.core.MutablePreferences) -> Unit) {
        context.dataStore.edit(block)
    }
}
