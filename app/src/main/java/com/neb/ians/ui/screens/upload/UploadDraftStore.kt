package com.neb.ians.ui.screens.upload

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import kotlinx.coroutines.flow.first
import javax.inject.Inject
import javax.inject.Singleton

/**
 * What the last upload was about.
 *
 * Someone uploading their notes is almost never uploading one thing — they are
 * working through a folder of the same subject, the same class, the same
 * school. Asking again for all of it on every upload is the part that makes the
 * screen feel like paperwork, so the answers are kept and offered back already
 * filled in.
 */
@Singleton
class UploadDraftStore @Inject constructor(
    private val dataStore: DataStore<Preferences>
) {

    suspend fun lastUsed(): UploadDefaults {
        val prefs = runCatching { dataStore.data.first() }.getOrNull() ?: return UploadDefaults()
        return UploadDefaults(
            subject = prefs[SUBJECT].orEmpty(),
            gradeLevel = prefs[GRADE_LEVEL].orEmpty(),
            school = prefs[SCHOOL].orEmpty(),
            pradesh = prefs[PRADESH].orEmpty(),
            district = prefs[DISTRICT].orEmpty(),
            tags = prefs[TAGS].orEmpty()
        )
    }

    suspend fun remember(defaults: UploadDefaults) {
        runCatching {
            dataStore.edit { prefs ->
                prefs[SUBJECT] = defaults.subject
                prefs[GRADE_LEVEL] = defaults.gradeLevel
                prefs[SCHOOL] = defaults.school
                prefs[PRADESH] = defaults.pradesh
                prefs[DISTRICT] = defaults.district
                prefs[TAGS] = defaults.tags
            }
        }
    }

    private companion object {
        val SUBJECT = stringPreferencesKey("upload_last_subject")
        val GRADE_LEVEL = stringPreferencesKey("upload_last_grade_level")
        val SCHOOL = stringPreferencesKey("upload_last_school")
        val PRADESH = stringPreferencesKey("upload_last_pradesh")
        val DISTRICT = stringPreferencesKey("upload_last_district")
        val TAGS = stringPreferencesKey("upload_last_tags")
    }
}

data class UploadDefaults(
    val subject: String = "",
    val gradeLevel: String = "",
    val school: String = "",
    val pradesh: String = "",
    val district: String = "",
    val tags: String = ""
) {
    val isEmpty: Boolean
        get() = subject.isBlank() && gradeLevel.isBlank() && school.isBlank() &&
            pradesh.isBlank() && district.isBlank() && tags.isBlank()
}
