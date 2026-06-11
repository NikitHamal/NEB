package com.consica.code.data.prefs

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.longPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.core.stringSetPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.CodingInterest
import com.consica.code.core.model.ExperienceLevel
import com.consica.code.core.model.GuidanceLevel
import com.consica.code.core.model.LearningGoal
import com.consica.code.core.model.ThemeIntensity
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "ccode_prefs")

/** Mastery points required before professional mode unlocks automatically. */
const val PRO_MODE_MASTERY_THRESHOLD = 12

data class UserState(
    val onboardingDone: Boolean = false,
    val ageGroup: AgeGroup = AgeGroup.TEENS,
    val goal: LearningGoal = LearningGoal.FOR_FUN,
    val experience: ExperienceLevel = ExperienceLevel.BRAND_NEW,
    val themeIntensity: ThemeIntensity = ThemeIntensity.BALANCED,
    val interests: Set<CodingInterest> = emptySet(),
    val guidance: GuidanceLevel = GuidanceLevel.BALANCED,
    // Settings
    val darkMode: Boolean = false,
    val highContrast: Boolean = false,
    val reducedMotion: Boolean = false,
    val soundEnabled: Boolean = true,
    val proModeUnlockedManually: Boolean = false,
    // Stats
    val xp: Int = 0,
    val sunCoins: Int = 0,
    val waterDrops: Int = 0,
    val mastery: Int = 0,
    val streak: Int = 0,
    val bestStreak: Int = 0,
    val lastActiveEpochDay: Long = 0L,
) {
    val level: Int get() = xp / 100 + 1
    val xpIntoLevel: Int get() = xp % 100
    val xpPerLevel: Int get() = 100

    /** Pro tooling is available by age, by mastery, or by parent/setting unlock. */
    val proToolsUnlocked: Boolean
        get() = ageGroup == AgeGroup.PRO || ageGroup == AgeGroup.TEENS ||
            proModeUnlockedManually || mastery >= PRO_MODE_MASTERY_THRESHOLD

    /** Full professional editor experience (16+ default, or unlocked). */
    val professionalEditor: Boolean
        get() = ageGroup == AgeGroup.PRO || proModeUnlockedManually ||
            mastery >= PRO_MODE_MASTERY_THRESHOLD
}

class UserPreferencesRepository(private val context: Context) {

    private object Keys {
        val ONBOARDING_DONE = booleanPreferencesKey("onboarding_done")
        val AGE_GROUP = stringPreferencesKey("age_group")
        val GOAL = stringPreferencesKey("goal")
        val EXPERIENCE = stringPreferencesKey("experience")
        val THEME_INTENSITY = stringPreferencesKey("theme_intensity")
        val INTERESTS = stringSetPreferencesKey("interests")
        val GUIDANCE = stringPreferencesKey("guidance")
        val DARK_MODE = booleanPreferencesKey("dark_mode")
        val HIGH_CONTRAST = booleanPreferencesKey("high_contrast")
        val REDUCED_MOTION = booleanPreferencesKey("reduced_motion")
        val SOUND = booleanPreferencesKey("sound")
        val PRO_MANUAL = booleanPreferencesKey("pro_manual")
        val XP = intPreferencesKey("xp")
        val SUN = intPreferencesKey("sun")
        val WATER = intPreferencesKey("water")
        val MASTERY = intPreferencesKey("mastery")
        val STREAK = intPreferencesKey("streak")
        val BEST_STREAK = intPreferencesKey("best_streak")
        val LAST_ACTIVE_DAY = longPreferencesKey("last_active_day")
    }

    val userState: Flow<UserState> = context.dataStore.data.map { p ->
        UserState(
            onboardingDone = p[Keys.ONBOARDING_DONE] ?: false,
            ageGroup = p[Keys.AGE_GROUP].toEnum(AgeGroup.TEENS),
            goal = p[Keys.GOAL].toEnum(LearningGoal.FOR_FUN),
            experience = p[Keys.EXPERIENCE].toEnum(ExperienceLevel.BRAND_NEW),
            themeIntensity = p[Keys.THEME_INTENSITY].toEnum(ThemeIntensity.BALANCED),
            interests = (p[Keys.INTERESTS] ?: emptySet()).mapNotNull { name ->
                CodingInterest.entries.firstOrNull { it.name == name }
            }.toSet(),
            guidance = p[Keys.GUIDANCE].toEnum(GuidanceLevel.BALANCED),
            darkMode = p[Keys.DARK_MODE] ?: false,
            highContrast = p[Keys.HIGH_CONTRAST] ?: false,
            reducedMotion = p[Keys.REDUCED_MOTION] ?: false,
            soundEnabled = p[Keys.SOUND] ?: true,
            proModeUnlockedManually = p[Keys.PRO_MANUAL] ?: false,
            xp = p[Keys.XP] ?: 0,
            sunCoins = p[Keys.SUN] ?: 0,
            waterDrops = p[Keys.WATER] ?: 0,
            mastery = p[Keys.MASTERY] ?: 0,
            streak = p[Keys.STREAK] ?: 0,
            bestStreak = p[Keys.BEST_STREAK] ?: 0,
            lastActiveEpochDay = p[Keys.LAST_ACTIVE_DAY] ?: 0L,
        )
    }

    suspend fun completeOnboarding(
        ageGroup: AgeGroup,
        goal: LearningGoal,
        experience: ExperienceLevel,
        themeIntensity: ThemeIntensity,
        interests: Set<CodingInterest>,
    ) {
        context.dataStore.edit { p ->
            p[Keys.ONBOARDING_DONE] = true
            p[Keys.AGE_GROUP] = ageGroup.name
            p[Keys.GOAL] = goal.name
            p[Keys.EXPERIENCE] = experience.name
            p[Keys.THEME_INTENSITY] = themeIntensity.name
            p[Keys.INTERESTS] = interests.map { it.name }.toSet()
            p[Keys.GUIDANCE] = when (ageGroup) {
                AgeGroup.KIDS -> GuidanceLevel.FULL.name
                AgeGroup.TEENS -> GuidanceLevel.BALANCED.name
                AgeGroup.PRO -> GuidanceLevel.MINIMAL.name
            }
        }
    }

    suspend fun setAgeGroup(value: AgeGroup) = edit { it[Keys.AGE_GROUP] = value.name }
    suspend fun setThemeIntensity(value: ThemeIntensity) = edit { it[Keys.THEME_INTENSITY] = value.name }
    suspend fun setGuidance(value: GuidanceLevel) = edit { it[Keys.GUIDANCE] = value.name }
    suspend fun setDarkMode(value: Boolean) = edit { it[Keys.DARK_MODE] = value }
    suspend fun setHighContrast(value: Boolean) = edit { it[Keys.HIGH_CONTRAST] = value }
    suspend fun setReducedMotion(value: Boolean) = edit { it[Keys.REDUCED_MOTION] = value }
    suspend fun setSoundEnabled(value: Boolean) = edit { it[Keys.SOUND] = value }
    suspend fun setProModeManualUnlock(value: Boolean) = edit { it[Keys.PRO_MANUAL] = value }

    suspend fun addRewards(xp: Int = 0, sun: Int = 0, water: Int = 0, mastery: Int = 0) {
        context.dataStore.edit { p ->
            p[Keys.XP] = (p[Keys.XP] ?: 0) + xp
            p[Keys.SUN] = (p[Keys.SUN] ?: 0) + sun
            p[Keys.WATER] = (p[Keys.WATER] ?: 0) + water
            p[Keys.MASTERY] = (p[Keys.MASTERY] ?: 0) + mastery
        }
    }

    /**
     * Records app activity for today and updates the streak.
     * Returns the new streak count when the streak changed, or null otherwise.
     */
    suspend fun recordDailyActivity(todayEpochDay: Long): Int? {
        var newStreak: Int? = null
        context.dataStore.edit { p ->
            val last = p[Keys.LAST_ACTIVE_DAY] ?: 0L
            if (last == todayEpochDay) return@edit
            val current = p[Keys.STREAK] ?: 0
            val updated = if (last == todayEpochDay - 1) current + 1 else 1
            p[Keys.STREAK] = updated
            p[Keys.LAST_ACTIVE_DAY] = todayEpochDay
            val best = p[Keys.BEST_STREAK] ?: 0
            if (updated > best) p[Keys.BEST_STREAK] = updated
            newStreak = updated
        }
        return newStreak
    }

    suspend fun resetProgress() {
        context.dataStore.edit { p ->
            p[Keys.XP] = 0
            p[Keys.SUN] = 0
            p[Keys.WATER] = 0
            p[Keys.MASTERY] = 0
            p[Keys.STREAK] = 0
            p[Keys.BEST_STREAK] = 0
            p[Keys.LAST_ACTIVE_DAY] = 0L
            p[Keys.PRO_MANUAL] = false
        }
    }

    private suspend fun edit(block: (androidx.datastore.preferences.core.MutablePreferences) -> Unit) {
        context.dataStore.edit(block)
    }
}

private inline fun <reified T : Enum<T>> String?.toEnum(default: T): T =
    this?.let { name -> enumValues<T>().firstOrNull { it.name == name } } ?: default
