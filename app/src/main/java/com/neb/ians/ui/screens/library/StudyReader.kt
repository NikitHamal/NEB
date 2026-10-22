package com.neb.ians.ui.screens.library

import android.annotation.SuppressLint
import android.content.Intent
import android.net.Uri
import android.webkit.JavascriptInterface
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
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
import androidx.compose.material.icons.outlined.Visibility
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
import org.json.JSONObject
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

/** What the page calls back into: reading credit, answers. Called on a WebView thread. */
private class ReaderBridge(
    private val onReading: (Int, Int) -> Unit,
    private val onAnswer: (Int, Boolean) -> Unit,
    private val onClear: () -> Unit
) {
    @JavascriptInterface fun reading(read: Int, place: Int) = onReading(read, place)
    @JavascriptInterface fun answer(index: Int, right: Boolean) = onAnswer(index, right)
    @JavascriptInterface fun clear() = onClear()
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun StudyReaderScreen(onBack: () -> Unit, viewModel: StudyReaderViewModel = hiltViewModel()) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    var web by remember { mutableStateOf<WebView?>(null) }
    var showToc by remember { mutableStateOf(false) }
    var answersOpen by remember { mutableStateOf(false) }
    val doc = state.doc

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
                navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "Back") } },
                actions = {
                    if (doc != null && doc.html.contains("details class=\"ans")) {
                        IconButton(onClick = {
                            answersOpen = !answersOpen
                            web?.evaluateJavascript("window.nebAnswers && nebAnswers($answersOpen)", null)
                        }) { Icon(Icons.Outlined.Visibility, contentDescription = if (answersOpen) "Fold the answers" else "Open every answer") }
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
                else -> ReaderWeb(state, doc, viewModel, onWeb = { web = it })
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
private fun ReaderWeb(state: StudyReaderState, doc: ApiStudyDoc, viewModel: StudyReaderViewModel, onWeb: (WebView) -> Unit) {
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
                        onClear = { post { viewModel.clearAnswers() } }
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

private fun esc(s: String) = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

/** The whole page the WebView shows: the book's HTML in the app's colours, KaTeX from assets. */
private fun readerPage(doc: ApiStudyDoc, state: StudyReaderState, vars: String, dark: Boolean): String {
    val body = doc.html.replace("src=\"/static/", "src=\"${doc.mediaBase}static/")
    val answers = JSONObject(state.answers.mapKeys { it.key.toString() }.mapValues { if (it.value) 1 else 0 }).toString()
    val eyebrow = listOfNotNull(state.label, doc.area?.takeIf { it.isNotBlank() }, "${doc.readMin} min read").joinToString(" · ")
    return """<!doctype html><html lang="${doc.lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="katex/katex.min.css"><style>:root{$vars}$READER_CSS</style></head>
<body class="${if (dark) "dark" else ""}"><article>
<p class="eyebrow">${esc(eyebrow)}</p><h1 class="title">${esc(doc.title)}</h1>
<div class="body">$body</div></article>
<script src="katex/katex.min.js"></script>
<script>var NEB_ANSWERS=$answers, NEB_MIN=${maxOf(1, doc.readMin)}, NEB_PLACE=${state.mark.place}, NEB_READ=${state.mark.read};$READER_JS</script>
</body></html>"""
}

private const val READER_CSS = """
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.72 system-ui,-apple-system,Roboto,'Noto Sans','Noto Sans Devanagari',sans-serif;overflow-wrap:break-word}
article{padding:18px 18px 48px;max-width:760px;margin:0 auto}
.eyebrow{margin:0 0 6px;font-size:13px;font-weight:600;color:var(--mute)}
.title{margin:0 0 18px;font-size:26px;line-height:1.2;font-weight:700;letter-spacing:-.01em}
.body p{margin:0 0 1em}.body h2{margin:2em 0 .6em;font-size:1.3em;line-height:1.3}.body h3{margin:1.6em 0 .5em;font-size:1.1em}
.body ul,.body ol{padding-left:1.4em}.body li{margin:.3em 0}.body li.num{list-style:none}
.body strong{font-weight:650}.body a{color:var(--ink)}
.body code{font-family:ui-monospace,monospace;font-size:.88em;padding:.1em .3em;border-radius:6px;background:var(--card2)}
.body pre{padding:12px 14px;border-radius:12px;background:var(--card2);overflow-x:auto;font-size:.85em;line-height:1.5}.body pre code{background:none;padding:0}
.body blockquote{margin:1em 0;padding-left:1em;border-left:3px solid var(--line);color:var(--mute)}
.body table{display:block;max-width:100%;overflow-x:auto;border-collapse:collapse;margin:1.2em 0;font-size:.88em;line-height:1.5}
.body th,.body td{padding:.5em .7em;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}.body th{background:var(--card);white-space:nowrap}
.m{white-space:nowrap}.dm{margin:1em 0;overflow-x:auto;overflow-y:hidden;text-align:center}.dm .m{display:block}.katex{font-size:1.05em}.katex-display{margin:0}
.eqx .fr{display:inline-block;vertical-align:-.62em;text-align:center}.eqx .fr .fn{display:block;padding:0 .3em 1px;border-bottom:1px solid currentColor}.eqx .fr .fd{display:block;padding:1px .3em 0}
figure{margin:1.4em 0;text-align:center}figure img{max-width:100%;height:auto;border-radius:12px;background:#fff;padding:8px}figure.photo img{padding:0}
figcaption{margin-top:.6em;font-size:.85em;line-height:1.5;color:var(--mute);text-align:left}figcaption .src{display:block;font-size:.85em;opacity:.8}
.photokey{display:block;text-align:left;font-size:.85em;margin-top:.5em}.photokey .pk{display:block}.photokey .pk i{font-style:normal;font-weight:700;display:inline-block;min-width:1.6em}
.box{margin:1.3em 0;padding:.9em 1em;border-radius:14px;background:var(--card);border:1px solid var(--line);border-left:4px solid var(--line2)}
.box>:last-child{margin-bottom:0}.box .bt,details.ans>summary{font-size:.76em;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--mute);margin-bottom:.4em}
.box.key,.box.definition{border-left-color:var(--ink)}.box.key .bt,.box.definition .bt{color:var(--ink)}
.chsum{margin:2em 0 1.2em;padding:1em 1.1em .3em;border-radius:16px;background:var(--card);border:1px solid var(--line)}.chsum h2{margin-top:0;font-size:1.12em}
h2.qs{padding-top:1em;border-top:1px solid var(--line)}
.marks{margin-left:.3em;padding:.05em .45em;border-radius:99px;font-size:.72em;font-weight:600;color:var(--mute);background:var(--card2);white-space:nowrap}
.opts{display:grid;gap:.45em;margin:.55em 0 .2em}.opts.c4{grid-template-columns:repeat(2,minmax(0,1fr))}.opts.c2,.opts.c1{grid-template-columns:1fr}
.opt{display:flex;gap:.5em;align-items:baseline;padding:.5em .75em;border-radius:12px;border:1px solid var(--line);background:var(--bg);line-height:1.45}
.opt>i{flex:none;font-style:normal;font-weight:700;font-size:.85em;color:var(--mute)}.opt>i:after{content:"."}
[data-key] .opt{cursor:pointer}[data-key] .opt:active{background:var(--card2)}
.opt.right{border-color:#1f8a4c;background:rgba(31,138,76,.12)}.opt.right>i{color:#1f8a4c}
.opt.wrong{border-color:#c2412d;background:rgba(194,65,45,.11)}.opt.wrong>i{color:#c2412d}
body.dark .opt.right>i{color:#5fd391}body.dark .opt.wrong>i{color:#ff8a73}
ol.mcq>li,.mcq-p{margin-bottom:1em}.mcq-p>p{margin-bottom:.2em}
.parts{display:block;margin:.4em 0 0}.part{display:block;margin:.35em 0;padding-left:1.9em;text-indent:-1.9em}.part>i{display:inline-block;width:1.9em;text-indent:0;font-style:normal;font-weight:600;color:var(--mute)}
details.ans{margin:1em 0 1.5em;border-radius:14px;border:1px dashed var(--line2)}
details.ans>summary{display:flex;align-items:center;margin:0;padding:.85em 1em;list-style:none;color:var(--ink)}details.ans>summary::-webkit-details-marker{display:none}
details.ans>summary:after{content:"Show";margin-left:auto;text-transform:none;letter-spacing:0;font-size:1.05em;color:var(--mute)}
details.ans[open]{border-style:solid;background:var(--card)}details.ans[open]>summary:after{content:"Hide"}
.ans-body{padding:0 1em 1em}.ans-body>:last-child{margin-bottom:0}.ansline{margin:0 0 .5em}
.tip{font-size:.85em;color:var(--mute);margin:.2em 0 .8em}.score{margin:2em 0 0;padding:.9em 1em;border-radius:14px;background:var(--card);border:1px solid var(--line);font-size:.95em}
.score button,.resume{border:0;background:var(--ink);color:var(--bg);font:600 14px system-ui,sans-serif;border-radius:99px;padding:9px 16px;margin-top:8px}
.resume{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);box-shadow:0 6px 18px rgba(0,0,0,.25);z-index:5}
"""

private const val READER_JS = """
(function(){
var body=document.querySelector('.body');
function ty(el){if(el.dataset.done)return;el.dataset.done=1;try{katex.render(el.textContent,el,{throwOnError:false,displayMode:el.classList.contains('d'),strict:'ignore'})}catch(e){}}
var ms=document.querySelectorAll('.m');
if(window.katex){if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){ty(e.target);io.unobserve(e.target)}})},{rootMargin:'800px 0px'});ms.forEach(function(m){io.observe(m)})}else ms.forEach(ty)}
var qs=[].slice.call(body.querySelectorAll('ol.mcq > li[data-key], .mcq-p[data-key]'));
function mark(q,choice){var k=q.getAttribute('data-key');q.classList.add('done');q.querySelectorAll('.opt').forEach(function(o){var l=o.getAttribute('data-opt');o.classList.toggle('right',l===k);o.classList.toggle('wrong',l===choice&&choice!==k)})}
function score(){var el=document.querySelector('.score');if(!el)return;var a=0,r=0;qs.forEach(function(q){if(q.classList.contains('done')){a++;if(q.dataset.ok==='1')r++}});
el.style.display=a?'block':'none';el.firstChild.textContent=r+' of '+a+' right'+(a<qs.length?' · '+(qs.length-a)+' still to try':'')}
qs.forEach(function(q,i){q.querySelectorAll('.opt').forEach(function(o){if(!o.getAttribute('data-opt')){var t=o.querySelector('i');o.setAttribute('data-opt',t?t.textContent.trim():'')}
o.addEventListener('click',function(){if(q.classList.contains('done'))return;var ok=o.getAttribute('data-opt')===q.getAttribute('data-key');q.dataset.ok=ok?'1':'0';mark(q,o.getAttribute('data-opt'));NebStudy.answer(i,ok);score()})});
if(NEB_ANSWERS[i]!==undefined){q.dataset.ok=String(NEB_ANSWERS[i]);mark(q,NEB_ANSWERS[i]?q.getAttribute('data-key'):'')}});
if(qs.length){var first=qs[0].tagName==='LI'?qs[0].parentNode:qs[0];var tip=document.createElement('p');tip.className='tip';tip.textContent='Tap an option to check it.';first.parentNode.insertBefore(tip,first);
var sc=document.createElement('div');sc.className='score';sc.appendChild(document.createTextNode(''));var b=document.createElement('button');b.textContent='Try the questions again';
b.onclick=function(){NebStudy.clear();qs.forEach(function(q){q.classList.remove('done');delete q.dataset.ok;q.querySelectorAll('.opt').forEach(function(o){o.classList.remove('right','wrong')})});score()};
sc.appendChild(document.createElement('br'));sc.appendChild(b);document.querySelector('article').appendChild(sc);score()}
window.nebAnswers=function(open){body.querySelectorAll('details.ans').forEach(function(d){d.open=open})};
window.nebGo=function(id){var h=document.getElementById(id);if(h)window.scrollTo({top:h.getBoundingClientRect().top+scrollY-12,behavior:'smooth'})};
var rate=100/(NEB_MIN*60*0.25),credit=NEB_READ,here=0,last=Date.now(),sent=0;
function pos(){var h=document.documentElement.scrollHeight-innerHeight;return h>0?Math.max(0,Math.min(100,100*scrollY/h)):100}
function send(){if(Date.now()-sent<2000)return;sent=Date.now();NebStudy.reading(Math.round(credit),Math.round(here))}
addEventListener('scroll',function(){here=pos();send()},{passive:true});
setInterval(function(){var n=Date.now(),dt=Math.min(5,(n-last)/1000);last=n;here=pos();if(here>credit){credit=Math.min(here,credit+rate*dt);send()}},1000);
if(NEB_PLACE>4&&NEB_PLACE<95){var r=document.createElement('button');r.className='resume';r.textContent='Resume where you stopped ('+NEB_PLACE+'%)';
r.onclick=function(){var h=document.documentElement.scrollHeight-innerHeight;scrollTo({top:h*NEB_PLACE/100,behavior:'smooth'});r.remove()};document.body.appendChild(r);
setTimeout(function(){if(r.parentNode)r.remove()},9000);addEventListener('scroll',function x(){if(scrollY>200&&r.parentNode){r.remove();removeEventListener('scroll',x)}})}
})();
"""
