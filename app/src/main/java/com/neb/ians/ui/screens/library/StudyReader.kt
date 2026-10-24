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
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
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
    val answers: Map<Int, Boolean> = emptyMap()
) {
    val key: String get() = "$grade/$subject/" + if (kind == "guide") "guide" else "$kind$no"
    val label: String
        get() = when (kind) {
            "bank" -> "Question bank"
            "guide" -> "Exam guide"
            else -> "Unit $no"
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
            progress.open(s.key, doc.title, "Class ${s.grade} · ${s.subject.replace('-', ' ').replaceFirstChar { it.uppercase() }}")
            _state.update { it.copy(doc = doc, isLoading = false, mark = progress.get(s.key), answers = progress.answers(s.key)) }
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

    fun toggleDone() {
        val key = _state.value.key
        progress.setDone(key, !_state.value.mark.markedDone)
        _state.update { it.copy(mark = progress.get(key)) }
    }
}

/** What the page calls back into: reading credit, answers, the figure viewer. Called on a WebView thread. */
private class ReaderBridge(
    private val onReading: (Int, Int) -> Unit,
    private val onAnswer: (Int, Boolean) -> Unit,
    private val onClear: () -> Unit,
    private val onZoom: (Boolean) -> Unit
) {
    @JavascriptInterface fun reading(read: Int, place: Int) = onReading(read, place)
    @JavascriptInterface fun answer(index: Int, right: Boolean) = onAnswer(index, right)
    @JavascriptInterface fun clear() = onClear()
    @JavascriptInterface fun zoom(open: Boolean) = onZoom(open)
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun StudyReaderScreen(onBack: () -> Unit, viewModel: StudyReaderViewModel = hiltViewModel()) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    var web by remember { mutableStateOf<WebView?>(null) }
    var showToc by remember { mutableStateOf(false) }
    var answersOpen by remember(state.key) { mutableStateOf(false) }
    var zoomOpen by remember { mutableStateOf(false) }
    val doc = state.doc
    val closeZoom = { web?.evaluateJavascript("window.nebZoomClose && nebZoomClose()", null); zoomOpen = false }
    BackHandler(enabled = zoomOpen) { closeZoom() }

    Scaffold(
        topBar = {
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
                    if (doc != null && doc.html.contains("details class=\"ans")) {
                        Text(
                            if (answersOpen) "Hide answers" else "Show answers",
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.SemiBold,
                            modifier = Modifier
                                .padding(end = 2.dp)
                                .clip(RoundedCornerShape(999.dp))
                                .background(if (answersOpen) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.surfaceContainerHigh)
                                .nebPressable(onClick = {
                                    answersOpen = !answersOpen
                                    web?.evaluateJavascript("window.nebAnswers && nebAnswers($answersOpen)", null)
                                })
                                .padding(horizontal = 12.dp, vertical = 7.dp),
                            color = if (answersOpen) MaterialTheme.colorScheme.surface else MaterialTheme.colorScheme.onSurface
                        )
                    }
                    if (doc != null && doc.toc.isNotEmpty()) {
                        IconButton(onClick = { showToc = true }) { Icon(Icons.AutoMirrored.Outlined.List, contentDescription = "Contents") }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
            )
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
                else -> ReaderWeb(state, doc, viewModel, onWeb = { web = it }, onZoom = { zoomOpen = it })
            }
        }
    }

    if (showToc && doc != null) {
        ModalBottomSheet(onDismissRequest = { showToc = false }, containerColor = MaterialTheme.colorScheme.surfaceContainer) {
            Text("Contents", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(start = 20.dp, bottom = 8.dp))
            LazyColumn(Modifier.fillMaxWidth().navigationBarsPadding()) {
                items(doc.toc) { item ->
                    Text(
                        item.title,
                        style = MaterialTheme.typography.bodyLarge,
                        fontWeight = if (item.kind.isNotEmpty()) FontWeight.SemiBold else FontWeight.Normal,
                        modifier = Modifier
                            .fillMaxWidth()
                            .nebPressable(scale = 0.99f, onClick = {
                                showToc = false
                                web?.evaluateJavascript("window.nebGo && nebGo('${item.id}')", null)
                            })
                            .padding(horizontal = 20.dp, vertical = 12.dp)
                    )
                }
            }
        }
    }
}

@Composable
private fun ReaderBottomBar(state: StudyReaderState, onPrev: () -> Unit, onNext: () -> Unit, onDone: () -> Unit) {
    val doc = state.doc ?: return
    Surface(color = MaterialTheme.colorScheme.surface) {
        Column {
            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                modifier = Modifier.fillMaxWidth().navigationBarsPadding().padding(horizontal = 12.dp, vertical = 8.dp)
            ) {
                IconButton(onClick = onPrev, enabled = doc.prev != null) { Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "Previous") }
                val done = state.mark.markedDone
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.Center,
                    modifier = Modifier
                        .weight(1f)
                        .clip(RoundedCornerShape(999.dp))
                        .nebPressable(onClick = onDone)
                        .then(Modifier)
                ) {
                    Surface(
                        shape = RoundedCornerShape(999.dp),
                        color = if (done) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.surfaceContainerHigh,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.Center, modifier = Modifier.padding(vertical = 11.dp)) {
                            Icon(Icons.Outlined.CheckCircle, contentDescription = null, tint = if (done) MaterialTheme.colorScheme.surface else MaterialTheme.colorScheme.onSurface, modifier = Modifier.size(20.dp))
                            Spacer(Modifier.width(8.dp))
                            Text(
                                when {
                                    done -> "Done"
                                    state.mark.tried > 0 -> "Mark as done · ${state.mark.right}/${state.mark.tried} right"
                                    else -> "Mark as done"
                                },
                                style = MaterialTheme.typography.labelLarge,
                                fontWeight = FontWeight.SemiBold,
                                color = if (done) MaterialTheme.colorScheme.surface else MaterialTheme.colorScheme.onSurface
                            )
                        }
                    }
                }
                IconButton(onClick = onNext, enabled = doc.next != null) { Icon(Icons.AutoMirrored.Outlined.ArrowForward, contentDescription = "Next") }
            }
        }
    }
}

private fun Color.hex(): String = String.format("#%06X", 0xFFFFFF and toArgb())

@SuppressLint("SetJavaScriptEnabled")
@Composable
private fun ReaderWeb(state: StudyReaderState, doc: ApiStudyDoc, viewModel: StudyReaderViewModel, onWeb: (WebView) -> Unit, onZoom: (Boolean) -> Unit) {
    val c = MaterialTheme.colorScheme
    val dark = c.surface.toArgb().let { (android.graphics.Color.red(it) + android.graphics.Color.green(it) + android.graphics.Color.blue(it)) < 384 }
    val vars = "--bg:${c.surface.hex()};--ink:${c.onSurface.hex()};--mute:${c.onSurfaceVariant.hex()};--line:${c.outlineVariant.hex()};" +
        "--line2:${c.outline.hex()};--card:${c.surfaceContainerLow.hex()};--card2:${c.surfaceContainerHigh.hex()}"
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
                        onZoom = { open -> post { onZoom(open) } }
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
