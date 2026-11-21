package com.neb.ians.ui.screens.library

import android.annotation.SuppressLint
import android.content.Intent
import android.net.Uri
import android.webkit.JavascriptInterface
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.automirrored.outlined.ArrowForward
import androidx.compose.material.icons.automirrored.outlined.List
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiStudyDoc
import com.neb.ians.data.api.isSchoolGrade
import com.neb.ians.data.api.syllabusShort
import com.neb.ians.data.repository.StudyMark
import com.neb.ians.data.repository.StudyProgress
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.nebPressable
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class StudyReaderState(
    val grade: String = "",
    val subject: String = "",
    val kind: String = "unit",
    val no: Int = 0,
    val doc: ApiStudyDoc? = null,
    val isLoading: Boolean = true,
    val error: String? = null,
    val mark: StudyMark = StudyMark(),
    val answers: Map<Int, Boolean> = emptyMap(),
    /** A timed test of this model paper, as the page saved it (see EXAM_JS), or null. */
    val examState: String? = null
) {
    val key: String get() = "$grade/$subject/" + if (kind == "guide") "guide" else "$kind$no"
    val label: String
        get() = when (kind) {
            "bank" -> "Question bank"
            "guide" -> "Exam guide"
            // the entrance books (grade "cee", …) number chapters
            else -> if (isSchoolGrade(grade)) "Unit $no" else "Chapter $no"
        }
}

@HiltViewModel
class StudyReaderViewModel @Inject constructor(
    private val api: ApiService,
    private val progress: StudyProgress,
    savedState: SavedStateHandle
) : ViewModel() {
    private val _state = MutableStateFlow(
        StudyReaderState(
            grade = savedState.get<String>("grade").orEmpty(),
            subject = savedState.get<String>("subject").orEmpty(),
            kind = savedState.get<String>("kind") ?: "unit",
            no = savedState.get<String>("no")?.toIntOrNull() ?: 0
        )
    )
    val state: StateFlow<StudyReaderState> = _state.asStateFlow()

    init {
        load()
    }

    fun load() = viewModelScope.launch {
        val s = _state.value
        _state.update { it.copy(isLoading = true, error = null) }
        try {
            val doc = when (s.kind) {
                "bank" -> api.getStudyBank(s.grade, s.subject, s.no)
                "guide" -> api.getStudyGuide(s.grade, s.subject)
                else -> api.getStudyChapter(s.grade, s.subject, s.no)
            }
            val (loadedMark, loadedAnswers, loadedExam) = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) {
                progress.open(s.key, doc.title, "${syllabusShort(s.grade)} · ${s.subject.replace('-', ' ').replaceFirstChar { it.uppercase() }}")
                Triple(progress.get(s.key), progress.answers(s.key), progress.exam(s.key))
            }
            _state.update {
                it.copy(doc = doc, isLoading = false, mark = loadedMark, answers = loadedAnswers, examState = loadedExam)
            }
        } catch (e: Exception) {
            _state.update { it.copy(isLoading = false, error = ApiErrorMapper.mapException(e)) }
        }
    }

    /** Previous or next chapter (or set) of the same subject, read in place. */
    fun go(no: Int) {
        _state.update { it.copy(no = no, doc = null) }
        load()
    }

    fun reading(read: Int, place: Int) {
        val key = _state.value.key
        progress.setReading(key, read, place)
        _state.update { it.copy(mark = progress.get(key)) }
    }

    fun answer(index: Int, right: Boolean) {
        val key = _state.value.key
        progress.setAnswer(key, index, right)
        _state.update { it.copy(mark = progress.get(key)) }
    }

    fun clearAnswers() {
        val key = _state.value.key
        progress.clearAnswers(key)
        _state.update { it.copy(mark = progress.get(key), answers = emptyMap()) }
    }

    /** The page's timed-test state; "" when the student went back to practice. Any thread. */
    fun saveExam(json: String) {
        val key = _state.value.key
        val value = json.takeIf { it.isNotBlank() }
        progress.setExam(key, value)
        _state.update { it.copy(examState = value) }
    }

    fun toggleDone() {
        val key = _state.value.key
        progress.setDone(key, !_state.value.mark.markedDone)
        _state.update { it.copy(mark = progress.get(key)) }
    }
}

/** What the page calls back into: reading credit, answers, the figure viewer, the timed test. Called on a WebView thread. */
private class ReaderBridge(
    private val onReading: (Int, Int) -> Unit,
    private val onAnswer: (Int, Boolean) -> Unit,
    private val onClear: () -> Unit,
    private val onZoom: (Boolean) -> Unit,
    private val onExam: (Boolean) -> Unit,
    private val onExamSave: (String) -> Unit
) {
    @JavascriptInterface fun reading(read: Int, place: Int) = onReading(read, place)
    @JavascriptInterface fun answer(index: Int, right: Boolean) = onAnswer(index, right)
    @JavascriptInterface fun clear() = onClear()
    @JavascriptInterface fun zoom(open: Boolean) = onZoom(open)
    /** A timed test started (true) or ended: "Show answers" is hidden meanwhile. */
    @JavascriptInterface fun exam(on: Boolean) = onExam(on)
    /** The timed test's state as JSON, saved on every pick; "" clears it. */
    @JavascriptInterface fun examSave(state: String?) = onExamSave(state.orEmpty())
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun StudyReaderScreen(onBack: () -> Unit, viewModel: StudyReaderViewModel = hiltViewModel()) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    var web by remember { mutableStateOf<WebView?>(null) }
    var showToc by remember { mutableStateOf(false) }
    var answersOpen by remember(state.key) { mutableStateOf(false) }
    var zoomOpen by remember { mutableStateOf(false) }
    var textScaleIdx by remember { mutableStateOf(1) }
    val textScales = remember { floatArrayOf(0.92f, 1.0f, 1.1f, 1.2f) }
    // set by the page (NebStudy.exam); not keyed by remember, the WebView's bridge holds this one state
    var examOn by remember { mutableStateOf(false) }
    LaunchedEffect(state.key) { examOn = false }
    val doc = state.doc
    val closeZoom = { web?.evaluateJavascript("window.nebZoomClose && nebZoomClose()", null); zoomOpen = false }
    BackHandler(enabled = zoomOpen) { closeZoom() }

    Scaffold(
        topBar = {
            Column {
            TopAppBar(
                title = {
                    Column {
                        Text(doc?.title ?: state.label, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Text(
                            "${state.label} · ${doc?.readMin ?: 0} min · ${state.mark.read}% read",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                },
                navigationIcon = { IconButton(onClick = { if (zoomOpen) closeZoom() else onBack() }) { Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "Back") } },
                actions = {
                    if (doc != null && !examOn && doc.html.contains("details class=\"ans")) {
                        Text(
                            if (answersOpen) "Hide answers" else "Show answers",
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.SemiBold,
                            modifier = Modifier
                                .padding(end = 4.dp)
                                .clip(RoundedCornerShape(28.dp))
                                .background(if (answersOpen) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceContainerHigh)
                                .nebPressable(onClick = {
                                    answersOpen = !answersOpen
                                    web?.evaluateJavascript("window.nebAnswers && nebAnswers($answersOpen)", null)
                                })
                                .padding(horizontal = 12.dp, vertical = 7.dp),
                            color = if (answersOpen) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface
                        )
                    }
                    if (doc != null) {
                        Text(
                            text = if (textScaleIdx == 1) "Aa" else "Aa ${Math.round(textScales[textScaleIdx] * 100)}%",
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.SemiBold,
                            color = if (textScaleIdx != 1) MaterialTheme.colorScheme.onSecondaryContainer else MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier
                                .padding(end = 2.dp)
                                .clip(RoundedCornerShape(20.dp))
                                .background(if (textScaleIdx != 1) MaterialTheme.colorScheme.secondaryContainer else MaterialTheme.colorScheme.surfaceContainerLow)
                                .nebPressable(onClick = {
                                    textScaleIdx = (textScaleIdx + 1) % textScales.size
                                    val sc = textScales[textScaleIdx]
                                    web?.evaluateJavascript("document.documentElement.style.setProperty('--rd-scale','$sc')", null)
                                })
                                .padding(horizontal = 10.dp, vertical = 7.dp)
                        )
                    }
                    if (doc != null && doc.toc.isNotEmpty()) {
                        IconButton(onClick = { showToc = true }) { Icon(Icons.AutoMirrored.Outlined.List, contentDescription = "Contents") }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
            )
            ReaderProgressBar(readPercent = state.mark.read)
            }
        },
        bottomBar = {
            if (doc != null) ReaderBottomBar(state, onPrev = { doc.prev?.let(viewModel::go) }, onNext = { doc.next?.let(viewModel::go) }, onDone = viewModel::toggleDone)
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        Box(Modifier.fillMaxSize().padding(padding)) {
            when {
                doc == null && state.isLoading -> Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { NebLoader(size = NebLoaderSize.Standard) }
                doc == null -> ErrorCard(message = state.error ?: "This chapter could not be loaded.", onRetry = { viewModel.load() }, modifier = Modifier.padding(16.dp))
                else -> ReaderWeb(state, doc, viewModel, onWeb = { web = it }, onZoom = { zoomOpen = it }, onExam = { examOn = it })
            }
        }
    }

    if (showToc && doc != null) {
        com.neb.ians.ui.components.NebModalSheet(onDismiss = { showToc = false }, title = "On this page") {
            LazyColumn(
                modifier = Modifier.fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                items(doc.toc, key = { it.id }) { item ->
                    val isQs = item.kind == "qs"
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(10.dp),
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(16.dp))
                            .background(if (isQs) MaterialTheme.colorScheme.secondaryContainer else MaterialTheme.colorScheme.surfaceContainerLow)
                            .nebPressable(scale = 0.985f, onClick = {
                                showToc = false
                                web?.evaluateJavascript("window.nebGo && nebGo('${item.id}')", null)
                            })
                            .padding(horizontal = 14.dp, vertical = 12.dp)
                    ) {
                        Text(
                            text = item.title,
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = if (item.kind.isNotEmpty()) FontWeight.SemiBold else FontWeight.Medium,
                            color = if (isQs) MaterialTheme.colorScheme.onSecondaryContainer else MaterialTheme.colorScheme.onSurface,
                            modifier = Modifier.weight(1f)
                        )
                        if (isQs) {
                            Text(
                                text = "Practice",
                                style = MaterialTheme.typography.labelSmall,
                                fontWeight = FontWeight.SemiBold,
                                color = MaterialTheme.colorScheme.primary
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun ReaderProgressBar(readPercent: Int) {
    val readFraction by androidx.compose.animation.core.animateFloatAsState(
        targetValue = (readPercent / 100f).coerceIn(0f, 1f),
        label = "reader_progress"
    )
    Box(
        Modifier
            .fillMaxWidth()
            .height(3.dp)
            .background(MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.45f))
    ) {
        Box(
            Modifier
                .fillMaxWidth(readFraction)
                .height(3.dp)
                .clip(RoundedCornerShape(topEnd = 3.dp, bottomEnd = 3.dp))
                .background(MaterialTheme.colorScheme.primary)
        )
    }
}

@Composable
private fun ReaderBottomBar(state: StudyReaderState, onPrev: () -> Unit, onNext: () -> Unit, onDone: () -> Unit) {
    val doc = state.doc ?: return
    val c = MaterialTheme.colorScheme
    val done = state.mark.markedDone
    // Previous (round), mark done (tonal pill, fills the row), Next chapter (the one filled button).
    Column(Modifier.fillMaxWidth().background(c.surface)) {
        HorizontalDivider(thickness = 1.dp, color = c.outlineVariant)
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            modifier = Modifier
                .fillMaxWidth()
                .navigationBarsPadding()
                .padding(horizontal = 14.dp, vertical = 10.dp)
        ) {
        if (doc.prev != null) {
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(RoundedCornerShape(24.dp))
                    .background(c.surfaceContainerHigh)
                    .nebPressable(onClick = onPrev),
                contentAlignment = Alignment.Center
            ) { Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "Previous chapter", tint = c.onSurface) }
        }
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.Center,
            modifier = Modifier
                .weight(1f)
                .height(48.dp)
                .clip(RoundedCornerShape(24.dp))
                .background(if (done) c.secondaryContainer else c.surfaceContainerHigh)
                .nebPressable(onClick = onDone)
                .padding(horizontal = 14.dp)
        ) {
            Icon(
                Icons.Outlined.CheckCircle,
                contentDescription = null,
                tint = if (done) c.onSecondaryContainer else c.onSurfaceVariant,
                modifier = Modifier.size(20.dp)
            )
            Spacer(Modifier.width(8.dp))
            Text(
                when {
                    done -> "Done"
                    state.mark.tried > 0 -> "Mark done · ${state.mark.right}/${state.mark.tried}"
                    else -> "Mark as done"
                },
                style = MaterialTheme.typography.labelLarge,
                fontWeight = FontWeight.SemiBold,
                color = if (done) c.onSecondaryContainer else c.onSurface,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
        if (doc.next != null) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                modifier = Modifier
                    .height(48.dp)
                    .clip(RoundedCornerShape(24.dp))
                    .background(c.primary)
                    .nebPressable(onClick = onNext)
                    .padding(start = 18.dp, end = 14.dp)
            ) {
                Text("Next", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, color = c.onPrimary)
                Icon(Icons.AutoMirrored.Outlined.ArrowForward, contentDescription = "Next chapter", tint = c.onPrimary, modifier = Modifier.size(18.dp))
            }
        }
        }
    }
}

private fun Color.hex(): String = String.format("#%06X", 0xFFFFFF and toArgb())
private fun Color.rgba(alpha: Float): String {
    val a = toArgb()
    return "rgba(${android.graphics.Color.red(a)},${android.graphics.Color.green(a)},${android.graphics.Color.blue(a)},$alpha)"
}

@SuppressLint("SetJavaScriptEnabled")
@Composable
private fun ReaderWeb(
    state: StudyReaderState,
    doc: ApiStudyDoc,
    viewModel: StudyReaderViewModel,
    onWeb: (WebView) -> Unit,
    onZoom: (Boolean) -> Unit,
    onExam: (Boolean) -> Unit
) {
    val c = MaterialTheme.colorScheme
    val dark = c.surface.toArgb().let { (android.graphics.Color.red(it) + android.graphics.Color.green(it) + android.graphics.Color.blue(it)) < 384 }
    val vars = "--bg:${c.surface.hex()};--ink:${c.onSurface.hex()};--mute:${c.onSurfaceVariant.hex()};--line:${c.outlineVariant.hex()};" +
        "--line2:${c.outline.hex()};--card:${c.surfaceContainerLow.hex()};--card2:${c.surfaceContainerHigh.hex()};" +
        "--pri:${c.primary.hex()};--on-pri:${c.onPrimary.hex()};--pri-tint:${c.primary.rgba(if (dark) 0.14f else 0.07f)};" +
        "--pri-line:${c.primary.rgba(if (dark) 0.36f else 0.26f)};--zebra:${c.onSurface.rgba(0.04f)}"
    val html = remember(doc, state.key, vars) { readerPage(doc, state, vars, dark) }
    val context = androidx.compose.ui.platform.LocalContext.current
    AndroidView(
        factory = { ctx ->
            WebView(ctx).apply {
                setBackgroundColor(c.surface.toArgb())
                settings.javaScriptEnabled = true
                settings.domStorageEnabled = true
                settings.cacheMode = WebSettings.LOAD_DEFAULT
                settings.textZoom = 100
                addJavascriptInterface(
                    ReaderBridge(
                        onReading = { r, p -> post { viewModel.reading(r, p) } },
                        onAnswer = { i, ok -> post { viewModel.answer(i, ok) } },
                        onClear = { post { viewModel.clearAnswers() } },
                        onZoom = { open -> post { onZoom(open) } },
                        onExam = { on -> post { onExam(on) } },
                        // saved straight away, not posted: a pick made just before leaving must not be lost
                        onExamSave = { json -> viewModel.saveExam(json) }
                    ),
                    "NebStudy"
                )
                webViewClient = object : WebViewClient() {
                    override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                        val url = request?.url ?: return false
                        if (url.scheme == "http" || url.scheme == "https") {
                            runCatching { context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url.toString()))) }
                            return true
                        }
                        return false
                    }
                }
                onWeb(this)
            }
        },
        update = { view ->
            if (view.tag != html) {
                view.tag = html
                view.loadDataWithBaseURL("file:///android_asset/", html, "text/html", "UTF-8", null)
            }
        },
        modifier = Modifier.fillMaxSize()
    )
}
