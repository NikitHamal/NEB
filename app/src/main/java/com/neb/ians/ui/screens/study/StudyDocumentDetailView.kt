package com.neb.ians.ui.screens.study

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
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
import com.neb.ians.data.api.ApiStudySummaryRequest
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.ui.components.fileSizeLabel
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject
import com.neb.ians.ui.components.NebLoader

// -------------------------------------------------------------
// Document detail (Summary / Mindmap / Quiz / Flashcards) — the
// document-level Study Lab feature view, opened from the
// "My Documents" tab of StudyLabScreen via internal state.
// -------------------------------------------------------------

data class StudyDocDetailUiState(
    val docId: String = "",
    val document: ApiStudyDocument? = null,
    val mindmap: ApiStudyMindmap? = null,
    val quizzes: List<ApiStudyQuizSummary> = emptyList(),
    val flashcards: List<ApiStudyFlashcard> = emptyList(),
    val isLoading: Boolean = true,
    val error: String? = null,
    val featureTab: String = "summary",
    val summaryMode: String = "compact",
    val summaryCompact: String = "",
    val summaryDetailed: String = "",
    val isGeneratingSummary: Boolean = false,
    val isGeneratingMindmap: Boolean = false,
    val isGeneratingQuiz: Boolean = false,
    val openingQuizId: String? = null,
    val activeQuiz: ApiStudyQuizDetail? = null,
    val isSubmittingQuiz: Boolean = false,
    val quizResult: StudyQuizResultData? = null,
    val isGeneratingFlashcards: Boolean = false,
    val actionError: String? = null
)

@HiltViewModel
class StudyDocDetailViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(StudyDocDetailUiState())
    val uiState: StateFlow<StudyDocDetailUiState> = _uiState.asStateFlow()

    fun load(docId: String) {
        if (_uiState.value.docId == docId && _uiState.value.document != null) return
        _uiState.value = StudyDocDetailUiState(docId = docId, isLoading = true)
        viewModelScope.launch {
            val token = authRepository.getBearerToken()
            if (token == null) {
                _uiState.update { it.copy(isLoading = false, error = "Sign in to open this document") }
                return@launch
            }
            try {
                val detail = apiService.getStudyDocumentDetail(token, docId)
                val doc = detail.document
                _uiState.update {
                    it.copy(
                        document = doc,
                        mindmap = detail.mindmap,
                        quizzes = detail.quizzes,
                        flashcards = detail.flashcards,
                        summaryCompact = doc?.summaryCompact ?: "",
                        summaryDetailed = doc?.summaryDetailed ?: "",
                        isLoading = false,
                        error = detail.error
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = studyErrorMessage(e)) }
            }
        }
    }

    fun selectFeatureTab(tab: String) {
        _uiState.update { it.copy(featureTab = tab, actionError = null) }
    }

    fun setSummaryMode(mode: String) {
        _uiState.update { it.copy(summaryMode = mode) }
    }

    fun clearActionError() {
        _uiState.update { it.copy(actionError = null) }
    }

    fun generateSummary(mode: String) {
        val docId = _uiState.value.docId
        if (docId.isBlank()) return
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            _uiState.update { it.copy(isGeneratingSummary = true, actionError = null) }
            try {
                val resp = apiService.generateStudySummary(token, docId, ApiStudySummaryRequest(mode))
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
                        summaryDetailed = newDetailed,
                        document = state.document?.copy(
                            summaryCompact = newCompact,
                            summaryDetailed = newDetailed,
                            summaryGenerated = true
                        )
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isGeneratingSummary = false, actionError = studyErrorMessage(e)) }
            }
        }
    }

    fun generateMindmap() {
        val docId = _uiState.value.docId
        if (docId.isBlank()) return
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            _uiState.update { it.copy(isGeneratingMindmap = true, actionError = null) }
            try {
                val resp = apiService.generateStudyMindmap(token, docId)
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
                _uiState.update {
                    it.copy(
                        isGeneratingMindmap = false,
                        mindmap = resp.mindmap,
                        document = it.document?.copy(mindmapGenerated = true)
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isGeneratingMindmap = false, actionError = studyErrorMessage(e)) }
            }
        }
    }

    fun generateQuiz(count: Int) {
        val docId = _uiState.value.docId
        if (docId.isBlank()) return
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            _uiState.update { it.copy(isGeneratingQuiz = true, actionError = null) }
            try {
                val resp = apiService.generateStudyQuiz(token, docId, ApiStudyCountRequest(count))
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
                _uiState.update { state ->
                    state.copy(
                        isGeneratingQuiz = false,
                        quizzes = listOf(
                            ApiStudyQuizSummary(
                                id = quiz.id,
                                title = quiz.title,
                                questionCount = quiz.questionCount.takeIf { c -> c > 0 } ?: quiz.questions.size,
                                createdAt = quiz.createdAt,
                                attemptCount = quiz.attemptCount,
                                bestScore = quiz.bestScore
                            )
                        ) + state.quizzes,
                        activeQuiz = quiz,
                        quizResult = null,
                        document = state.document?.let { d -> d.copy(quizCount = d.quizCount + 1) }
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
                val resp = apiService.getStudyQuiz(token, quizId)
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

    /** Document quizzes: answers keyed by question NUMBER as string. */
    fun submitQuiz(answers: Map<String, String>) {
        val quiz = _uiState.value.activeQuiz ?: return
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            _uiState.update { it.copy(isSubmittingQuiz = true, actionError = null) }
            try {
                val resp = apiService.submitStudyQuiz(token, quiz.id, ApiStudyQuizSubmitRequest(answers))
                val attempt = resp.attempt
                if (attempt == null) {
                    _uiState.update { it.copy(isSubmittingQuiz = false, actionError = resp.error ?: "Could not submit quiz") }
                    return@launch
                }
                val rows = quiz.questions.map { q ->
                    val key = q.displayNumber.toString()
                    val r = attempt.results[key]
                    StudyQuizResultRow(
                        number = q.displayNumber,
                        question = q.displayQuestion,
                        userAnswer = r?.userAnswer ?: answers[key].orEmpty(),
                        correctAnswer = r?.correctAnswer.orEmpty(),
                        isCorrect = r?.isCorrect ?: false,
                        explanation = r?.explanation.orEmpty()
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
                apiService.reviewStudyFlashcard(token, cardId, ApiStudyFlashcardReviewRequest(confidence))
            } catch (_: Exception) {
                // fire-and-forget
            }
        }
    }

    fun generateFlashcards(count: Int) {
        val docId = _uiState.value.docId
        if (docId.isBlank()) return
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            _uiState.update { it.copy(isGeneratingFlashcards = true, actionError = null) }
            try {
                val resp = apiService.generateStudyFlashcards(token, docId, ApiStudyCountRequest(count))
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
                _uiState.update { state ->
                    state.copy(
                        isGeneratingFlashcards = false,
                        flashcards = resp.flashcards,
                        document = state.document?.copy(
                            flashcardCount = resp.totalFlashcards.takeIf { it > 0 } ?: resp.flashcards.size
                        )
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isGeneratingFlashcards = false, actionError = studyErrorMessage(e)) }
            }
        }
    }
}

@Composable
fun DocumentDetailView(
    docId: String,
    onClose: () -> Unit,
    onSearchClick: () -> Unit = {},
    viewModel: StudyDocDetailViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    LaunchedEffect(docId) {
        viewModel.load(docId)
    }

    BackHandler {
        when {
            uiState.quizResult != null -> viewModel.closeQuiz()
            uiState.activeQuiz != null -> viewModel.closeQuiz()
            else -> onClose()
        }
    }

    val doc = uiState.document
    val topBarTitle = doc?.let { d -> d.title.ifBlank { d.fileName } }?.ifBlank { "Document" } ?: "Document"
    Scaffold(
        topBar = {
            WebTopBar(
                title = topBarTitle,
                subtitle = "Study Lab",
                showBack = true,
                onBackClick = {
                    when {
                        uiState.quizResult != null || uiState.activeQuiz != null -> viewModel.closeQuiz()
                        else -> onClose()
                    }
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
            doc == null -> {
                WebEmptyState(
                    title = "Could not open document",
                    message = uiState.error ?: "Try again later.",
                    icon = painterResource(id = R.drawable.ic_document),
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding)
                )
            }
            else -> {
                val quizResult = uiState.quizResult
                val activeQuiz = uiState.activeQuiz
                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 14.dp),
                    verticalArrangement = Arrangement.spacedBy(14.dp)
                ) {
                    when {
                        quizResult != null -> {
                            item(key = "quiz-results") {
                                StudyQuizResults(
                                    result = quizResult,
                                    onDone = { viewModel.closeQuiz() }
                                )
                            }
                        }
                        activeQuiz != null -> {
                            item(key = "quiz-player") {
                                StudyQuizPlayer(
                                    quiz = activeQuiz,
                                    isSubmitting = uiState.isSubmittingQuiz,
                                    error = uiState.actionError,
                                    answerKeyFor = { q -> q.displayNumber.toString() },
                                    onSubmit = { answers -> viewModel.submitQuiz(answers) },
                                    onExit = { viewModel.closeQuiz() }
                                )
                            }
                        }
                        else -> {
                            item(key = "doc-header") {
                                Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                                    Text(
                                        text = doc.title.ifBlank { doc.fileName.ifBlank { "Untitled" } },
                                        style = MaterialTheme.typography.headlineSmall,
                                        fontWeight = FontWeight.ExtraBold,
                                        maxLines = 2,
                                        overflow = TextOverflow.Ellipsis
                                    )
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                                    ) {
                                        ParseStatusPill(status = studyParseStatusOf(doc))
                                        Text(
                                            text = listOf(doc.fileName, fileSizeLabel(doc.fileSize))
                                                .filter { it.isNotBlank() }
                                                .joinToString(", "),
                                            style = MaterialTheme.typography.labelSmall,
                                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                                            maxLines = 1,
                                            overflow = TextOverflow.Ellipsis
                                        )
                                    }
                                }
                            }
                            item(key = "feature-tabs") {
                                StudyFeatureTabRow(
                                    selected = uiState.featureTab,
                                    onSelect = { viewModel.selectFeatureTab(it) }
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
                            when (uiState.featureTab) {
                                "summary" -> item(key = "summary") {
                                    StudySummarySection(
                                        summaryCompact = uiState.summaryCompact,
                                        summaryDetailed = uiState.summaryDetailed,
                                        mode = uiState.summaryMode,
                                        onModeChange = { viewModel.setSummaryMode(it) },
                                        isGenerating = uiState.isGeneratingSummary,
                                        onGenerate = { mode -> viewModel.generateSummary(mode) }
                                    )
                                }
                                "mindmap" -> item(key = "mindmap") {
                                    StudyMindmapSection(
                                        mindmap = uiState.mindmap,
                                        isGenerating = uiState.isGeneratingMindmap,
                                        onGenerate = { viewModel.generateMindmap() }
                                    )
                                }
                                "quiz" -> item(key = "quiz-list") {
                                    StudyQuizListSection(
                                        quizzes = uiState.quizzes,
                                        isGenerating = uiState.isGeneratingQuiz,
                                        openingQuizId = uiState.openingQuizId,
                                        onGenerate = { count -> viewModel.generateQuiz(count) },
                                        onOpenQuiz = { quizId -> viewModel.openQuiz(quizId) }
                                    )
                                }
                                "flashcards" -> item(key = "flashcards") {
                                    StudyFlashcardsSection(
                                        cards = uiState.flashcards,
                                        isGenerating = uiState.isGeneratingFlashcards,
                                        onReview = { cardId, confidence -> viewModel.reviewFlashcard(cardId, confidence) },
                                        onGenerateMore = { count -> viewModel.generateFlashcards(count) }
                                    )
                                }
                            }
                        }
                    }
                    item(key = "bottom-spacer") { Spacer(modifier = Modifier.height(32.dp)) }
                }
            }
        }
    }
}
