package com.neb.ians.ui.screens.interactive

import android.annotation.SuppressLint
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.viewinterop.AndroidView
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.ApiInteractiveLessonDetailResponse
import com.neb.ians.ui.components.NebTopBar

data class InteractiveLessonUiState(
    val lesson: ApiInteractiveLessonDetailResponse? = null,
    val isLoading: Boolean = true,
    val error: String? = null
)

@SuppressLint("SetJavaScriptEnabled")
@Suppress("DEPRECATION")
@Composable
fun InteractiveLessonScreen(
    courseSlug: String,
    lessonSlug: String,
    onNavigateBack: () -> Unit,
    viewModel: InteractiveLessonViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    LaunchedEffect(courseSlug, lessonSlug) {
        viewModel.loadLesson(courseSlug, lessonSlug)
    }

    InteractiveLessonContent(
        courseSlug = courseSlug,
        lessonSlug = lessonSlug,
        uiState = uiState,
        onNavigateBack = onNavigateBack,
        onRetry = { viewModel.loadLesson(courseSlug, lessonSlug) }
    )
}

@Composable
private fun InteractiveLessonContent(
    courseSlug: String,
    lessonSlug: String,
    uiState: InteractiveLessonUiState,
    onNavigateBack: () -> Unit,
    onRetry: () -> Unit
) {
    val context = LocalContext.current
    var pageProgress by remember { mutableStateOf(0) }

    Column(modifier = Modifier.fillMaxSize()) {
        NebTopBar(
            showBrand = false,
            title = when {
                uiState.isLoading -> "Lesson"
                uiState.lesson != null -> uiState.lesson!!.lesson.title
                else -> "Lesson"
            },
            onBack = onNavigateBack
        )

        when {
            uiState.isLoading -> {
                LinearProgressIndicator(
                    progress = { pageProgress / 100f },
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.primary,
                )
            }
            uiState.error != null -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    TextButton(onClick = onRetry) {
                        Text(uiState.error ?: "Failed to load lesson")
                    }
                }
            }
            uiState.lesson != null -> {
                val lessonData = uiState.lesson!!
                AndroidView(
                    modifier = Modifier.fillMaxSize(),
                    factory = { ctx ->
                        WebView(ctx).apply {
                            settings.apply {
                                javaScriptEnabled = true
                                domStorageEnabled = true
                                allowFileAccess = true
                                allowContentAccess = true
                                allowFileAccessFromFileURLs = true
                                allowUniversalAccessFromFileURLs = true
                                cacheMode = WebSettings.LOAD_DEFAULT
                                mixedContentMode = 0
                                userAgentString = userAgentString + " NEBiansAndroid"
                            }
                            webViewClient = object : WebViewClient() {
                                override fun onPageFinished(view: WebView?, url: String?) {
                                    super.onPageFinished(view, url)
                                    pageProgress = 100
                                }
                            }
                            webChromeClient = object : WebChromeClient() {
                                override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                    pageProgress = newProgress
                                }
                            }
                            loadLesson(context, lessonData, courseSlug, lessonSlug)
                        }
                    }
                )
            }
        }
    }
}

private fun WebView.loadLesson(
    context: android.content.Context,
    data: ApiInteractiveLessonDetailResponse,
    courseSlug: String,
    lessonSlug: String
) {
    val simPath = data.lesson.sim

    val html = context.assets.open("interactive/lesson.html")
        .bufferedReader().use { it.readText() }
        .replace("{{COURSE_COLOR}}", data.course.color.ifBlank { "#004ac6" })
        .replace("{{COURSE_SLUG}}", courseSlug)
        .replace("{{LESSON_SLUG}}", lessonSlug)
        .replace("{{SIM_TYPE}}", data.lesson.simType)
        .replace("{{SIM_URL}}", if (simPath.isNotBlank()) "js/$simPath.js" else "")
        .replace("{{LESSON_DATA}}", buildLessonJson(data, courseSlug, lessonSlug))

    loadDataWithBaseURL(
        "file:///android_asset/interactive/",
        html,
        "text/html",
        "UTF-8",
        null
    )
}

private fun buildLessonJson(
    data: ApiInteractiveLessonDetailResponse,
    courseSlug: String,
    lessonSlug: String
): String {
    val lesson = data.lesson
    val quizArray = lesson.quiz.joinToString(",") { q ->
        """{"q":${escapeJson(q.q)},"options":[${q.options.joinToString(",") { escapeJson(it) }}],"answer":${q.answer},"explain":${escapeJson(q.explain)}}"""
    }
    val knowledgeArray = lesson.knowledge.joinToString(",") { k ->
        """{"heading":${escapeJson(k.heading)},"body":${escapeJson(k.body)}}"""
    }
    val objectivesArray = lesson.objectives.joinToString(",") { escapeJson(it) }

    return """{"courseSlug":"$courseSlug","lessonSlug":"$lessonSlug","simType":${escapeJson(lesson.simType)},"lessonIndex":${data.lessonIndex},"totalLessons":${data.totalLessons},"lessonMinutes":${lesson.minutes},"objectives":[$objectivesArray],"knowledge":[$knowledgeArray],"funFact":${escapeJson(lesson.funFact)},"quiz":[$quizArray]}"""
}

private fun escapeJson(s: String): String {
    if (s.isBlank()) return "null"
    val escaped = s.replace("\\", "\\\\")
        .replace("\"", "\\\"")
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    return "\"$escaped\""
}