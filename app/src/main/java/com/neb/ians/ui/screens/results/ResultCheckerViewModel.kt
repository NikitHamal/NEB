package com.neb.ians.ui.screens.results

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ResultPayload
import com.neb.ians.data.repository.ResultRepository
import com.neb.ians.data.results.BulkResultRow
import com.neb.ians.data.results.ResultExam
import com.neb.ians.data.results.ResultExamType
import com.neb.ians.data.results.ResultLookup
import com.neb.ians.data.results.ResultMode
import com.neb.ians.data.api.ApiErrorMapper
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class ResultCheckerUiState(
    val exam: ResultExam = ResultExam.Class12,
    val examType: ResultExamType = ResultExamType.Regular,
    val mode: ResultMode = ResultMode.Single,
    val batch: String = "2083",
    val symbol: String = "",
    val dob: String = "",
    val bulkInput: String = "",
    val isChecking: Boolean = false,
    val progressCurrent: Int = 0,
    val progressTotal: Int = 0,
    val result: ResultLookup? = null,
    val bulkRows: List<BulkResultRow> = emptyList(),
    val error: String? = null,
    val showGradesheet: Boolean = false
) {
    val needsDob: Boolean get() = exam == ResultExam.Class12
    val canSubmit: Boolean
        get() = if (mode == ResultMode.Single) {
            symbol.trim().isNotEmpty() && (!needsDob || dob.trim().isNotEmpty()) && !isChecking
        } else {
            bulkInput.lines().any { it.trim().isNotEmpty() } && !isChecking
        }
}

@HiltViewModel
class ResultCheckerViewModel @Inject constructor(
    private val resultRepository: ResultRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(ResultCheckerUiState())
    val uiState: StateFlow<ResultCheckerUiState> = _uiState.asStateFlow()
    private var bulkJob: Job? = null

    fun selectExam(exam: ResultExam) {
        _uiState.update {
            it.copy(
                exam = exam,
                examType = if (exam == ResultExam.Class10) ResultExamType.Regular else it.examType,
                dob = if (exam == ResultExam.Class10) "" else it.dob,
                result = null,
                bulkRows = emptyList(),
                error = null
            )
        }
    }

    fun selectExamType(type: ResultExamType) {
        if (_uiState.value.exam == ResultExam.Class10) return
        _uiState.update { it.copy(examType = type, result = null, bulkRows = emptyList(), error = null) }
    }

    fun selectMode(mode: ResultMode) {
        _uiState.update { it.copy(mode = mode, result = null, bulkRows = emptyList(), error = null) }
    }

    fun updateBatch(value: String) = _uiState.update { it.copy(batch = value, error = null) }
    fun updateSymbol(value: String) = _uiState.update { it.copy(symbol = value.take(24), error = null) }
    fun updateDob(value: String) = _uiState.update { it.copy(dob = value.take(10), error = null) }
    fun updateBulkInput(value: String) = _uiState.update { it.copy(bulkInput = value, error = null) }

    fun checkSingle() {
        val state = _uiState.value
        if (!state.canSubmit || state.mode != ResultMode.Single) return
        viewModelScope.launch {
            _uiState.update { it.copy(isChecking = true, error = null, result = null, bulkRows = emptyList()) }
            resultRepository.checkResult(
                exam = state.exam,
                examType = state.examType,
                symbol = state.symbol,
                dob = state.dob,
                batch = state.batch
            ).onSuccess { lookup ->
                _uiState.update { it.copy(isChecking = false, result = lookup, error = null) }
            }.onFailure { error ->
                _uiState.update { it.copy(isChecking = false, error = ApiErrorMapper.mapException(error)) }
            }
        }
    }

    fun runBulk() {
        val state = _uiState.value
        if (!state.canSubmit || state.mode != ResultMode.Bulk) return
        val entries = state.bulkInput.lines().map { it.trim() }.filter { it.isNotEmpty() }
        if (entries.isEmpty()) return
        bulkJob?.cancel()
        bulkJob = viewModelScope.launch {
            val initialRows = entries.map { entry -> BulkResultRow(symbol = entry.substringBefore(',').trim()) }
            _uiState.update {
                it.copy(
                    isChecking = true,
                    error = null,
                    result = null,
                    bulkRows = initialRows,
                    progressCurrent = 0,
                    progressTotal = entries.size
                )
            }
            entries.forEachIndexed { index, entry ->
                val symbol = entry.substringBefore(',').trim()
                val dob = if (_uiState.value.needsDob) entry.substringAfter(',', missingDelimiterValue = "").trim() else ""
                if (symbol.isBlank()) {
                    updateBulkRow(index, BulkResultRow(symbol = symbol, status = "Skipped", error = "Missing symbol"))
                    bumpProgress()
                    return@forEachIndexed
                }
                if (_uiState.value.needsDob && dob.isBlank()) {
                    updateBulkRow(index, BulkResultRow(symbol = symbol, status = "DOB missing", error = "DOB missing"))
                    bumpProgress()
                    return@forEachIndexed
                }
                resultRepository.checkResult(
                    exam = _uiState.value.exam,
                    examType = _uiState.value.examType,
                    symbol = symbol,
                    dob = dob,
                    batch = _uiState.value.batch
                ).onSuccess { lookup ->
                    val d = lookup.payload
                    updateBulkRow(
                        index,
                        BulkResultRow(
                            symbol = symbol,
                            name = d.studentName.ifBlank { "—" },
                            gpa = d.gpa.ifBlank { "—" },
                            grade = d.grade.ifBlank { "—" },
                            status = if (lookup.cached) "Cached" else "Fresh",
                            success = true
                        )
                    )
                    if (!lookup.cached) delay(450)
                }.onFailure { error ->
                    updateBulkRow(
                        index,
                        BulkResultRow(
                            symbol = symbol,
                            gpa = "—",
                            grade = "—",
                            status = "Failed",
                            success = false,
                            error = ApiErrorMapper.mapException(error)
                        )
                    )
                    delay(450)
                }
                bumpProgress()
            }
            _uiState.update { it.copy(isChecking = false) }
        }
    }

    fun cancelBulk() {
        bulkJob?.cancel()
        bulkJob = null
        _uiState.update { it.copy(isChecking = false, error = null) }
    }

    fun showGradesheet(show: Boolean) = _uiState.update { it.copy(showGradesheet = show) }

    private fun updateBulkRow(index: Int, row: BulkResultRow) {
        _uiState.update { state ->
            state.copy(bulkRows = state.bulkRows.mapIndexed { i, old -> if (i == index) row else old })
        }
    }

    private fun bumpProgress() {
        _uiState.update { it.copy(progressCurrent = (it.progressCurrent + 1).coerceAtMost(it.progressTotal)) }
    }
}

fun ResultPayload.registrationNumberOrFallback(): String {
    if (registrationNo.isNotBlank()) return registrationNo
    val symbolInt = symbol.filter { it.isDigit() }.toIntOrNull() ?: 12345678
    val part1 = symbolInt % 90 + 10
    val part2 = symbolInt % 900000 + 100000
    val part3 = symbolInt % 90 + 10
    return "$part1-$part2-$part3"
}
