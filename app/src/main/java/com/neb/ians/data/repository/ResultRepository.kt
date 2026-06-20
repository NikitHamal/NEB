package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ResultCheckRequest
import com.neb.ians.data.results.ResultExam
import com.neb.ians.data.results.ResultExamType
import com.neb.ians.data.results.ResultLookup
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ResultRepository @Inject constructor(
    private val apiService: ApiService
) {
    suspend fun checkResult(
        exam: ResultExam,
        examType: ResultExamType,
        symbol: String,
        dob: String,
        batch: String
    ): Result<ResultLookup> = withContext(Dispatchers.IO) {
        runCatching {
            val examCode = when {
                exam == ResultExam.Class10 -> "see"
                examType == ResultExamType.ReExam -> "neb_reexam"
                else -> "neb"
            }
            val response = apiService.checkResult(
                ResultCheckRequest(
                    exam = examCode,
                    symbol = symbol.trim(),
                    dob = dob.trim(),
                    batch = batch.trim()
                )
            )
            if (!response.success || response.data == null) {
                throw IllegalStateException(response.error ?: "Failed to check result")
            }
            ResultLookup(response.data, response.cached)
        }
    }
}
