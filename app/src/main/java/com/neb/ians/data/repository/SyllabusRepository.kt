package com.neb.ians.data.repository

import android.content.Context
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiSyllabusCategoriesResponse
import com.neb.ians.data.api.ApiSyllabusSubjectDetailResponse
import dagger.hilt.android.qualifiers.ApplicationContext
import java.io.File
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SyllabusRepository @Inject constructor(
    private val api: ApiService,
    @ApplicationContext context: Context
) {
    private val directory = File(context.filesDir, "syllabus-study-v1")
    private val json = Json { ignoreUnknownKeys = true; coerceInputValues = true }

    private fun detailFile(grade: String, subject: String): File {
        val safe = "$grade-$subject".replace(Regex("[^a-zA-Z0-9-]"), "_")
        return File(directory, "$safe.json")
    }

    suspend fun cachedCategories(): ApiSyllabusCategoriesResponse? = withContext(Dispatchers.IO) {
        runCatching { json.decodeFromString<ApiSyllabusCategoriesResponse>(File(directory, "categories.json").readText()) }.getOrNull()
    }

    suspend fun cachedDetail(grade: String, subject: String): ApiSyllabusSubjectDetailResponse? = withContext(Dispatchers.IO) {
        runCatching { json.decodeFromString<ApiSyllabusSubjectDetailResponse>(detailFile(grade, subject).readText()) }.getOrNull()
    }

    private fun save(file: File, content: String) {
        runCatching {
            directory.mkdirs()
            val temporary = File(file.path + ".tmp")
            temporary.writeText(content)
            if (!temporary.renameTo(file)) temporary.delete()
        }
    }

    suspend fun categories(): ApiSyllabusCategoriesResponse {
        val response = api.getSyllabusCategories()
        withContext(Dispatchers.IO) { save(File(directory, "categories.json"), json.encodeToString(response)) }
        return response
    }

    suspend fun detail(grade: String, subject: String): ApiSyllabusSubjectDetailResponse {
        val response = api.getSyllabusSubjectDetail(grade, subject)
        withContext(Dispatchers.IO) { save(detailFile(grade, subject), json.encodeToString(response)) }
        return response
    }
}
