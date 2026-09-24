package com.neb.ians.ui.screens.study

import com.neb.ians.ui.components.LinkifyText

import androidx.activity.compose.BackHandler
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import com.neb.ians.R
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiStudyCountRequest
import com.neb.ians.data.api.ApiStudyDocument
import com.neb.ians.data.api.ApiStudyFlashcard
import com.neb.ians.data.api.ApiStudyFlashcardReviewRequest
import com.neb.ians.data.api.ApiStudyMindmap
import com.neb.ians.data.api.ApiStudyQuizDetail
import com.neb.ians.data.api.ApiStudyQuizSummary
import com.neb.ians.data.api.ApiStudyQuizSubmitRequest
import com.neb.ians.data.api.ApiStudySpaceDetail
import com.neb.ians.data.api.ApiStudySummaryRequest
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.ui.components.WebChip
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebKpiCard
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebSectionHeader
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.ui.components.fileSizeLabel
import com.neb.ians.util.formatTimeAgo
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json
import kotlinx.serialization.decodeFromString
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.toRequestBody
import javax.inject.Inject
import com.neb.ians.ui.components.NebLoader

data class StudySpaceUiState(
    val space: ApiStudySpaceDetail? = null,
    val isLoading: Boolean = true,
    val error: String? = null,
    val isUploading: Boolean = false,
    val aiTab: String = "summary",
    val summaryMode: String = "compact",
    val summaryCompact: String = "",
    val summaryDetailed: String = "",
    val isGeneratingSummary: Boolean = false,
    val mindmap: ApiStudyMindmap? = null,
    val isGeneratingMindmap: Boolean = false,
    val quizzes: List<ApiStudyQuizSummary> = emptyList(),
    val isGeneratingQuiz: Boolean = false,
    val openingQuizId: String? = null,
    val activeQuiz: ApiStudyQuizDetail? = null,
    val isSubmittingQuiz: Boolean = false,
    val quizResult: StudyQuizResultData? = null,
    val flashcards: List<ApiStudyFlashcard> = emptyList(),
    val isGeneratingFlashcards: Boolean = false,
    val actionError: String? = null
)

@HiltViewModel
class StudySpaceViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {
    private val spaceId: String = savedStateHandle.get<String>("spaceId") ?: ""
    private val _uiState = MutableStateFlow(StudySpaceUiState())
    val uiState: StateFlow<StudySpaceUiState> = _uiState.asStateFlow()

    private var pollJob: Job? = null

    init {
        load()
    }

    fun load() {
        viewModelScope.launch {
            val token = authRepository.getBearerToken()
            if (token == null) {
                _uiState.update { it.copy(isLoading = false, error = "Sign in to open this Study Space") }
                return@launch
            }
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val detail = apiService.getStudySpaceDetail(token, spaceId)
                val spaceMindmap = try {
                    if (!detail.linkMindmapJson.isNullOrBlank()) {
                        Json { ignoreUnknownKeys = true }.decodeFromString<ApiStudyMindmap>(detail.linkMindmapJson)
                    } else null
                } catch (e: Exception) {
                    null
                }
                _uiState.update {
                    it.copy(
                        space = detail,
                        summaryCompact = detail.linkSummaryCompact ?: "",
                        summaryDetailed = detail.linkSummaryDetailed ?: "",
                        mindmap = spaceMindmap,
                        quizzes = detail.quizzes,
                        flashcards = detail.flashcards,
                        isLoading = false
                    )
                }
                ensurePolling()
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = e.localizedMessage ?: "Could not load Study Space") }
            }
        }
    }

    fun selectAiTab(tab: String) {
        _uiState.update { it.copy(aiTab = tab, actionError = null) }
    }

    fun setSummaryMode(mode: String) {
        _uiState.update { it.copy(summaryMode = mode) }
    }

    fun reportError(message: String) {
        _uiState.update { it.copy(actionError = message) }
    }

    private fun updateDocuments(transform: (List<ApiStudyDocument>) -> List<ApiStudyDocument>) {
        _uiState.update { state ->
            val space = state.space ?: return@update state
            state.copy(space = space.copy(documents = transform(space.documents)))
        }
    }

    fun uploadDocument(fileName: String, mime: String?, bytes: ByteArray) {
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            _uiState.update { it.copy(isUploading = true, actionError = null) }
            try {
                val mediaType = mime?.toMediaTypeOrNull() ?: "application/octet-stream".toMediaType()
                val body = bytes.toRequestBody(mediaType)
                val part = MultipartBody.Part.createFormData("file", fileName, body)
                val resp = apiService.uploadSpaceDocument(token, spaceId, part)
                val doc = resp.document
                if (doc == null) {
                    _uiState.update { it.copy(isUploading = false, actionError = resp.error ?: "Upload failed") }
                    return@launch
                }
                _uiState.update { it.copy(isUploading = false) }
                updateDocuments { docs -> listOf(doc) + docs }
                ensurePolling()
            } catch (e: Exception) {
                _uiState.update { it.copy(isUploading = false, actionError = studyErrorMessage(e)) }
            }
        }
    }

    fun reparseDocument(docId: String) {
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            _uiState.update { it.copy(actionError = null) }
            try {
                val resp = apiService.reparseSpaceDocument(token, spaceId, docId)
                val newStatus = resp.document?.parseStatus?.ifBlank { null }
                    ?: resp.parseStatus.ifBlank { "parsing" }
                updateDocuments { docs ->
                    docs.map { doc ->
                        if (doc.id == docId) doc.copy(parseStatus = newStatus, parseError = "") else doc
                    }
                }
                ensurePolling()
            } catch (e: Exception) {
                _uiState.update { it.copy(actionError = studyErrorMessage(e)) }
            }
        }
    }

    /** Polls parse status for non-terminal docs every 3s until all settle. */
    private fun ensurePolling() {
        if (pollJob?.isActive == true) return
        pollJob = viewModelScope.launch {
            while (isActive) {
                val pending = _uiState.value.space?.documents.orEmpty().filter {
                    studyParseStatusOf(it) !in STUDY_TERMINAL_PARSE_STATES
                }
                if (pending.isEmpty()) break
                delay(3000)
                val token = authRepository.getBearerToken() ?: break
                pending.forEach { doc ->
                    try {
                        val status = apiService.getSpaceParseStatus(token, spaceId, doc.id)
                        if (status.status.isNotBlank()) {
                            updateDocuments { docs ->
                                docs.map { d ->
                                    if (d.id == doc.id) {
                                        d.copy(
                                            parseStatus = status.status,
                                            parsedTextLength = status.parsedTextLength,
                                            parseError = status.error ?: d.parseError
                                        )
                                    } else d
                                }
                            }
                        }
                    } catch (_: Exception) {
                        // ignore transient polling errors
                    }
                }
            }
        }
    }

    override fun onCleared() {
        pollJob?.cancel()
        super.onCleared()
    }

    fun generateSummary(mode: String) {
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            _uiState.update { it.copy(isGeneratingSummary = true, actionError = null) }
            try {
                val resp = apiService.generateSpaceSummary(token, spaceId, ApiStudySummaryRequest(mode))
                if (resp.parseStatus == "parsing") {
                    _uiState.update {
                        it.copy(isGeneratingSummary = false, actionError = "Documents are still being parsed — try again shortly")
                    }
                    return@launch
                }
                if (resp.error != null && resp.summary.isBlank() && resp.summaryCompact.isBlank() && resp.summaryDetailed.isBlank()) {
                    _uiState.update { it.copy(isGeneratingSummary = false, actionError = resp.error) }
                    return@launch
                }
                _uiState.update { state ->
                    val newCompact = resp.summaryCompact.ifBlank {
                        if (mode == "compact") resp.summary.ifBlank { state.summaryCompact } else state.summaryCompact
                    }
                    val newDetailed = resp.summaryDetailed.ifBlank {
                        if (mode == "detailed") resp.summary.ifBlank { state.summaryDetailed } else state.summaryDetailed
                    }
                    state.copy(
                        isGeneratingSummary = false,
                        summaryCompact = newCompact,
                        summaryDetailed = newDetailed
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isGeneratingSummary = false, actionError = studyErrorMessage(e)) }
            }
        }
    }

    fun generateMindmap() {
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            _uiState.update { it.copy(isGeneratingMindmap = true, actionError = null) }
            try {
                val resp = apiService.generateSpaceMindmap(token, spaceId)
                if (resp.parseStatus == "parsing") {
                    _uiState.update {
                        it.copy(isGeneratingMindmap = false, actionError = "Documents are still being parsed — try again shortly")
                    }
                    return@launch
                }
                if (resp.mindmap == null) {
                    _uiState.update { it.copy(isGeneratingMindmap = false, actionError = resp.error ?: "AI generation failed, try again") }
                    return@launch
                }
                _uiState.update { it.copy(isGeneratingMindmap = false, mindmap = resp.mindmap) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isGeneratingMindmap = false, actionError = studyErrorMessage(e)) }
            }
        }
    }

    fun generateQuiz(count: Int) {
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            _uiState.update { it.copy(isGeneratingQuiz = true, actionError = null) }
            try {
                val resp = apiService.generateSpaceQuiz(token, spaceId, ApiStudyCountRequest(count))
                if (resp.parseStatus == "parsing") {
                    _uiState.update {
                        it.copy(isGeneratingQuiz = false, actionError = "Documents are still being parsed — try again shortly")
                    }
                    return@launch
                }
                val quiz = resp.quiz
                if (quiz == null) {
                    _uiState.update { it.copy(isGeneratingQuiz = false, actionError = resp.error ?: "AI generation failed, try again") }
                    return@launch
                }
                // Refresh the quiz list from the server (keeps counts consistent), fall back to local insert.
                val refreshed = try {
                    apiService.getSpaceQuizzes(token, spaceId).quizzes
                } catch (_: Exception) {
                    emptyList()
                }
                _uiState.update { state ->
                    state.copy(
                        isGeneratingQuiz = false,
                        quizzes = refreshed.ifEmpty {
                            listOf(
                                ApiStudyQuizSummary(
                                    id = quiz.id,
                                    title = quiz.title,
                                    questionCount = quiz.questionCount.takeIf { c -> c > 0 } ?: quiz.questions.size,
                                    createdAt = quiz.createdAt,
                                    attemptCount = quiz.attemptCount,
                                    bestScore = quiz.bestScore
                                )
                            ) + state.quizzes
                        },
                        activeQuiz = quiz,
                        quizResult = null
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isGeneratingQuiz = false, actionError = studyErrorMessage(e)) }
            }
        }
    }

    fun openQuiz(quizId: String) {
        if (_uiState.value.openingQuizId != null) return
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            _uiState.update { it.copy(openingQuizId = quizId, actionError = null) }
            try {
                val resp = apiService.getSpaceQuiz(token, quizId)
                val quiz = resp.quiz
                if (quiz == null) {
                    _uiState.update { it.copy(openingQuizId = null, actionError = resp.error ?: "Could not open quiz") }
                    return@launch
                }
                _uiState.update { it.copy(openingQuizId = null, activeQuiz = quiz, quizResult = null) }
            } catch (e: Exception) {
                _uiState.update { it.copy(openingQuizId = null, actionError = studyErrorMessage(e)) }
            }
        }
    }

    fun closeQuiz() {
        _uiState.update { it.copy(activeQuiz = null, quizResult = null, isSubmittingQuiz = false, actionError = null) }
    }

    /** Space quizzes: answers keyed by question ID. */
    fun submitQuiz(answers: Map<String, String>) {
        val quiz = _uiState.value.activeQuiz ?: return
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            _uiState.update { it.copy(isSubmittingQuiz = true, actionError = null) }
            try {
                val resp = apiService.submitSpaceQuiz(token, quiz.id, ApiStudyQuizSubmitRequest(answers))
                val attempt = resp.attempt
                if (attempt == null) {
                    _uiState.update { it.copy(isSubmittingQuiz = false, actionError = resp.error ?: "Could not submit quiz") }
                    return@launch
                }
                val recordByQuestion = attempt.answers.associateBy { it.questionId }
                val rows = quiz.questions.map { q ->
                    val record = recordByQuestion[q.id]
                    StudyQuizResultRow(
                        number = q.displayNumber,
                        question = q.displayQuestion,
                        userAnswer = record?.given ?: answers[q.id].orEmpty(),
                        correctAnswer = record?.correct?.ifBlank { null } ?: q.correctAnswer.orEmpty(),
                        isCorrect = record?.isCorrect ?: false,
                        explanation = q.explanation.orEmpty()
                    )
                }
                val result = StudyQuizResultData(
                    score = attempt.score,
                    total = attempt.totalQuestions.takeIf { it > 0 } ?: quiz.questions.size,
                    xp = attempt.xpEarned,
                    rows = rows
                )
                _uiState.update { state ->
                    state.copy(
                        isSubmittingQuiz = false,
                        quizResult = result,
                        quizzes = state.quizzes.map { summary ->
                            if (summary.id == quiz.id) {
                                summary.copy(
                                    attemptCount = summary.attemptCount + 1,
                                    bestScore = maxOf(summary.bestScore, attempt.score)
                                )
                            } else summary
                        }
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isSubmittingQuiz = false, actionError = studyErrorMessage(e)) }
            }
        }
    }

    /** Fire-and-forget confidence review; updates local card state optimistically. */
    fun reviewFlashcard(cardId: String, confidence: String) {
        _uiState.update { state ->
            state.copy(flashcards = state.flashcards.map { card ->
                if (card.id == cardId) card.copy(confidence = confidence) else card
            })
        }
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            try {
                apiService.reviewSpaceFlashcard(token, cardId, ApiStudyFlashcardReviewRequest(confidence))
            } catch (_: Exception) {
                // fire-and-forget
            }
        }
    }

    fun generateFlashcards(count: Int) {
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            _uiState.update { it.copy(isGeneratingFlashcards = true, actionError = null) }
            try {
                val resp = apiService.generateSpaceFlashcards(token, spaceId, ApiStudyCountRequest(count))
                if (resp.parseStatus == "parsing") {
                    _uiState.update {
                        it.copy(isGeneratingFlashcards = false, actionError = "Documents are still being parsed — try again shortly")
                    }
                    return@launch
                }
                if (resp.flashcards.isEmpty()) {
                    _uiState.update { it.copy(isGeneratingFlashcards = false, actionError = resp.error ?: "AI generation failed, try again") }
                    return@launch
                }
                _uiState.update { it.copy(isGeneratingFlashcards = false, flashcards = resp.flashcards) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isGeneratingFlashcards = false, actionError = studyErrorMessage(e)) }
            }
        }
    }
}

@Composable
fun StudySpaceScreen(
    onNavigateBack: () -> Unit,
    onSearchClick: () -> Unit = {},
    viewModel: StudySpaceViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val space = uiState.space
    val context = LocalContext.current
    val scope = rememberCoroutineScope()

    val filePicker = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri ->
        if (uri == null) return@rememberLauncherForActivityResult
        scope.launch {
            val picked = withContext(Dispatchers.IO) { readPickedStudyFile(context, uri) }
            if (picked == null) {
                viewModel.reportError("Could not read the selected file")
                return@launch
            }
            val validationError = studyUploadValidationError(picked.name, picked.size)
            if (validationError != null) {
                viewModel.reportError(validationError)
                return@launch
            }
            viewModel.uploadDocument(picked.name, picked.mime, picked.bytes)
        }
    }

    val quizFlowOpen = uiState.activeQuiz != null || uiState.quizResult != null
    BackHandler(enabled = quizFlowOpen) {
        viewModel.closeQuiz()
    }

    Scaffold(
        topBar = {
            WebTopBar(
                title = space?.title ?: "Study Space",
                subtitle = space?.memberRole?.ifBlank { null } ?: "Collaborative learning",
                showBack = true,
                onBackClick = {
                    if (quizFlowOpen) viewModel.closeQuiz() else onNavigateBack()
                },
                onSearchClick = onSearchClick
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        when {
            uiState.isLoading -> {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    NebLoader()
                }
            }
            uiState.error != null -> {
                WebEmptyState(
                    title = "Could not open space",
                    message = uiState.error ?: "Try again later.",
                    icon = painterResource(id = R.drawable.ic_science),
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding)
                )
            }
            space != null && uiState.quizResult != null -> {
                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 14.dp),
                    verticalArrangement = Arrangement.spacedBy(14.dp)
                ) {
                    item(key = "quiz-results") {
                        StudyQuizResults(
                            result = uiState.quizResult!!,
                            onDone = { viewModel.closeQuiz() }
                        )
                    }
                    item(key = "bottom-spacer") { Spacer(modifier = Modifier.height(32.dp)) }
                }
            }
            space != null && uiState.activeQuiz != null -> {
                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 14.dp),
                    verticalArrangement = Arrangement.spacedBy(14.dp)
                ) {
                    item(key = "quiz-player") {
                        StudyQuizPlayer(
                            quiz = uiState.activeQuiz!!,
                            isSubmitting = uiState.isSubmittingQuiz,
                            error = uiState.actionError,
                            answerKeyFor = { q -> q.id },
                            onSubmit = { answers -> viewModel.submitQuiz(answers) },
                            onExit = { viewModel.closeQuiz() }
                        )
                    }
                    item(key = "bottom-spacer") { Spacer(modifier = Modifier.height(32.dp)) }
                }
            }
            space != null -> {
                val readyDocumentCount = space.documents.count { studyParseStatusOf(it) == "ready" }
                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 14.dp),
                    verticalArrangement = Arrangement.spacedBy(14.dp)
                ) {
                    item(key = "header") { StudySpaceHeader(space) }
                    item(key = "kpi-row-1") {
                        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                            WebKpiCard(
                                label = "Documents",
                                value = "${space.documents.size.coerceAtLeast(space.docCount)}",
                                detail = "$readyDocumentCount ready",
                                painter = painterResource(id = R.drawable.ic_document),
                                modifier = Modifier.weight(1f)
                            )
                            WebKpiCard(
                                label = "Quizzes",
                                value = "${uiState.quizzes.size}",
                                detail = "${uiState.quizzes.sumOf { it.attemptCount }} attempts",
                                painter = painterResource(id = R.drawable.ic_school),
                                modifier = Modifier.weight(1f)
                            )
                        }
                    }
                    item(key = "kpi-row-2") {
                        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                            WebKpiCard(
                                label = "Flashcards",
                                value = "${uiState.flashcards.size.coerceAtLeast(space.flashcardCount)}",
                                detail = "${uiState.flashcards.size} loaded",
                                painter = painterResource(id = R.drawable.ic_book),
                                modifier = Modifier.weight(1f)
                            )
                            WebKpiCard(
                                label = "Members",
                                value = "${space.memberCount.coerceAtLeast(1)}",
                                detail = "${space.activeNow} active now",
                                painter = painterResource(id = R.drawable.ic_forum_outlined),
                                modifier = Modifier.weight(1f)
                            )
                        }
                    }
                    item(key = "documents-header") {
                        WebSectionHeader(
                            title = "Documents",
                            modifier = Modifier.padding(horizontal = 0.dp),
                            actionLabel = if (uiState.isUploading) "Uploading…" else "Upload",
                            onActionClick = {
                                if (!uiState.isUploading) filePicker.launch("*/*")
                            }
                        )
                    }
                    if (uiState.actionError != null) {
                        item(key = "action-error") {
                            Text(
                                text = uiState.actionError ?: "",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.error
                            )
                        }
                    }
                    if (space.documents.isEmpty()) {
                        item(key = "no-documents") {
                            WebEmptyState(
                                title = "No documents",
                                message = "Upload PDFs, notes, or images to power the AI tools below.",
                                icon = painterResource(id = R.drawable.ic_document)
                            )
                        }
                    } else {
                        items(space.documents, key = { it.id }) { doc ->
                            StudyDocumentRow(
                                doc = doc,
                                onRetryParse = { viewModel.reparseDocument(doc.id) }
                            )
                        }
                    }
                    item(key = "ai-tools-header") {
                        WebSectionHeader(title = "AI Tools", modifier = Modifier.padding(horizontal = 0.dp))
                    }
                    item(key = "ai-tabs") {
                        StudyFeatureTabRow(
                            selected = uiState.aiTab,
                            onSelect = { viewModel.selectAiTab(it) }
                        )
                    }
                    when (uiState.aiTab) {
                        "summary" -> item(key = "ai-summary") {
                            StudySummarySection(
                                summaryCompact = uiState.summaryCompact,
                                summaryDetailed = uiState.summaryDetailed,
                                mode = uiState.summaryMode,
                                onModeChange = { viewModel.setSummaryMode(it) },
                                isGenerating = uiState.isGeneratingSummary,
                                onGenerate = { mode -> viewModel.generateSummary(mode) }
                            )
                        }
                        "mindmap" -> item(key = "ai-mindmap") {
                            StudyMindmapSection(
                                mindmap = uiState.mindmap,
                                isGenerating = uiState.isGeneratingMindmap,
                                onGenerate = { viewModel.generateMindmap() }
                            )
                        }
                        "quiz" -> item(key = "ai-quiz") {
                            StudyQuizListSection(
                                quizzes = uiState.quizzes,
                                isGenerating = uiState.isGeneratingQuiz,
                                openingQuizId = uiState.openingQuizId,
                                onGenerate = { count -> viewModel.generateQuiz(count) },
                                onOpenQuiz = { quizId -> viewModel.openQuiz(quizId) }
                            )
                        }
                        "flashcards" -> item(key = "ai-flashcards") {
                            StudyFlashcardsSection(
                                cards = uiState.flashcards,
                                isGenerating = uiState.isGeneratingFlashcards,
                                onReview = { cardId, confidence -> viewModel.reviewFlashcard(cardId, confidence) },
                                onGenerateMore = { count -> viewModel.generateFlashcards(count) }
                            )
                        }
                    }
                    item(key = "bottom-spacer") { Spacer(modifier = Modifier.height(32.dp)) }
                }
            }
        }
    }
}

@Composable
private fun StudySpaceHeader(space: ApiStudySpaceDetail) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text(
                text = space.title,
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.ExtraBold,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            if (space.description.isNotBlank()) {
                LinkifyText(
                    text = space.description,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 4,
                    overflow = TextOverflow.Ellipsis
                )
            }
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                WebChip(text = space.visibility.replaceFirstChar { it.uppercase() }, selected = space.visibility == "public")
                if (space.inviteCode.isNotBlank()) WebChip(text = "Code ${space.inviteCode}")
                WebChip(text = "Updated ${formatTimeAgo(space.updatedAt)}")
            }
        }
    }
}

@Composable
private fun StudyDocumentRow(
    doc: ApiStudyDocument,
    onRetryParse: () -> Unit
) {
    val status = studyParseStatusOf(doc)
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Icon(
                painter = painterResource(id = R.drawable.ic_document),
                contentDescription = null,
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(24.dp)
            )
            Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(
                    text = doc.title.ifBlank { doc.fileName.ifBlank { "Untitled" } },
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.Bold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    ParseStatusPill(status = status)
                    Text(
                        text = listOf(fileSizeLabel(doc.fileSize), "${doc.parsedTextLength} chars")
                            .filter { it.isNotBlank() }
                            .joinToString(", "),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
            if (status == "failed") {
                IconButton(onClick = onRetryParse) {
                    Icon(
                        imageVector = Icons.Filled.Refresh,
                        contentDescription = "Retry parse",
                        tint = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.size(20.dp)
                    )
                }
            }
        }
    }
}
