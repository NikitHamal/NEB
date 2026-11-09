package com.neb.ians.ui.screens.reader.pdf

import android.content.Context
import android.graphics.Bitmap
import android.os.Handler
import android.os.Looper
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.gestures.animateScrollBy
import androidx.compose.foundation.layout.asPaddingValues
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsIgnoringVisibility
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsIgnoringVisibility
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.AutoAwesome
import androidx.compose.material.icons.outlined.Bookmark
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.FormatSize
import androidx.compose.material.icons.outlined.Fullscreen
import androidx.compose.material.icons.outlined.FullscreenExit
import androidx.compose.material.icons.outlined.MoreVert
import androidx.compose.material.icons.outlined.Pause
import androidx.compose.material.icons.outlined.PictureAsPdf
import androidx.compose.material.icons.outlined.PlayArrow
import androidx.compose.material.icons.outlined.Toc
import androidx.compose.material.icons.outlined.VolumeUp
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
import androidx.compose.material3.SliderDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.Stable
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshotFlow
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ColorFilter
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.LinkAnnotation
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextLinkStyles
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.BaselineShift
import androidx.compose.ui.text.style.Hyphens
import androidx.compose.ui.text.style.LineBreak
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.text.withLink
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.em
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebIconButton
import com.neb.ians.ui.components.NebModalSheet
import com.neb.ians.ui.components.NebSegment
import com.neb.ians.ui.components.NebSegmentedChoice
import com.neb.ians.ui.components.NebToggleRow
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.Poppins
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec
import kotlinx.coroutines.flow.distinctUntilChanged
import kotlinx.coroutines.launch
import kotlin.math.roundToInt

/** Colours of one reading theme. Paper and Sepia match the page filters, so cropped figures blend in. */
@Stable
class ReadingPalette(
    val bg: Color, val ink: Color, val muted: Color, val accent: Color,
    val tonal: Color, val line: Color, val filter: ColorFilter?
)

fun readingPalette(theme: ReadingTheme, look: ReaderLook): ReadingPalette = when (theme) {
    ReadingTheme.Paper -> ReadingPalette(Color.White, Color(0xFF1C1B1A), Color(0xFF66635C), Color(0xFF1F5FBF), Color(0xFFF1EFEA), Color(0xFFE0DDD5), null)
    ReadingTheme.Sepia -> ReadingPalette(Color(0xFFF4ECD8), Color(0xFF3B2F23), Color(0xFF86775F), Color(0xFF2F5D9B), Color(0xFFEADFC6), Color(0xFFD9CCAC), look.filter)
    ReadingTheme.Night -> ReadingPalette(Color(0xFF141414), Color(0xFFE2E0DA), Color(0xFF9B9890), Color(0xFF8AB4F8), Color(0xFF212120), Color(0xFF30302E), look.filter)
}

/** A request to scroll reading mode to a page; [id] lets the same page be asked for twice. */
data class ReadJump(val page: Int, val id: Int)

/** What reading mode needs from the document. */
@Stable
class ReadSource(
    val cached: (Int) -> ReflowPage?,
    val load: suspend (Int) -> ReflowPage?,
    val cachedCrop: (Int, FRect, Int) -> Bitmap?,
    val loadCrop: suspend (Int, FRect, Int) -> Bitmap?,
    val bodyPoints: () -> Float
)

@Stable
private class ReadType(val settings: ReadingSettings, val p: ReadingPalette) {
    val base = (18f * settings.fontScale).sp
    val lineHeight = (18f * settings.fontScale * 1.55f * settings.lineSpacing).sp
    val family: FontFamily = if (settings.font == ReadingFont.Serif) FontFamily.Serif else Poppins
    val gap: Dp = (18f * settings.fontScale * 0.85f).dp
    val sidePadding: Dp = when (settings.margin) { 0 -> 14.dp; 2 -> 40.dp; else -> 24.dp }
    val body = TextStyle(
        fontFamily = family, fontSize = base, lineHeight = lineHeight, color = p.ink,
        textAlign = if (settings.justify) TextAlign.Justify else TextAlign.Start,
        lineBreak = LineBreak.Paragraph, hyphens = if (settings.justify) Hyphens.Auto else Hyphens.None
    )

    fun heading(level: Int): TextStyle {
        val k = when (level) { 1 -> 1.7f; 2 -> 1.4f; 3 -> 1.2f; else -> 1.07f }
        return TextStyle(
            fontFamily = Poppins, fontWeight = FontWeight.SemiBold, fontSize = (18f * settings.fontScale * k).sp,
            lineHeight = (18f * settings.fontScale * k * 1.28f).sp, color = p.ink
        )
    }
}

private val UrlPattern = Regex("(https?://[^\\s]+|\\b(?:[a-z0-9-]+\\.)+(?:com|org|net|edu|gov|np|io|info|co|in)\\b(?:/[^\\s]*)?)", RegexOption.IGNORE_CASE)

private fun annotate(spans: List<Span>, p: ReadingPalette): AnnotatedString {
    val linkStyle = TextLinkStyles(SpanStyle(color = p.accent, textDecoration = TextDecoration.Underline))
    return buildAnnotatedString {
        for (s in spans) {
            val style = SpanStyle(
                fontWeight = if (s.bold) FontWeight.SemiBold else null,
                fontStyle = if (s.italic) FontStyle.Italic else null,
                fontFamily = if (s.mono) FontFamily.Monospace else null,
                background = if (s.mono) p.tonal else Color.Unspecified,
                fontSize = if (s.sup || s.sub) 0.72.em else androidx.compose.ui.unit.TextUnit.Unspecified,
                baselineShift = if (s.sup) BaselineShift.Superscript else if (s.sub) BaselineShift.Subscript else null
            )
            val href = s.href
            if (href != null) {
                withLink(LinkAnnotation.Url(href, linkStyle)) { withStyle(style) { append(s.text) } }
                continue
            }
            var last = 0
            for (m in UrlPattern.findAll(s.text)) {
                var value = m.value
                while (value.isNotEmpty() && value.last() in ".,;:!?)]\"'") value = value.dropLast(1)
                if (value.length < 4) continue
                val start = m.range.first
                withStyle(style) { append(s.text.substring(last, start)) }
                val url = if (value.startsWith("http", ignoreCase = true)) value else "https://$value"
                withLink(LinkAnnotation.Url(url, linkStyle)) { withStyle(style) { append(value) } }
                last = start + value.length
            }
            withStyle(style) { append(s.text.substring(last)) }
        }
    }
}

private class RdCtx(
    val source: ReadSource,
    val onJump: (Int) -> Unit,
    val onOpenPage: (Int) -> Unit
)

private sealed interface RdLoad {
    data object Loading : RdLoad
    data object Failed : RdLoad
    class Ready(val page: ReflowPage) : RdLoad
}

@Composable
private fun RdBlock(block: Block, t: ReadType, ctx: RdCtx, maxWidth: Dp, topGap: Dp) {
    val p = t.p
    when (block) {
        is HeadingBlock -> {
            val extra = when (block.level) { 1 -> t.gap * 1.6f; 2 -> t.gap * 1.0f; else -> t.gap * 0.4f }
            Text(
                block.text,
                style = t.heading(block.level),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = extra + topGap)
                    .then(if (block.jump >= 0) Modifier.clickable { ctx.onJump(block.jump) } else Modifier)
            )
        }
        is ParaBlock -> {
            val text = remember(block, p) { annotate(block.spans, p) }
            val m = Modifier.fillMaxWidth().padding(top = topGap)
            if (block.jump >= 0) {
                Text(text, style = t.body.copy(color = p.accent), modifier = m.clickable { ctx.onJump(block.jump) })
            } else {
                SelectionContainer { Text(text, style = t.body, modifier = m) }
            }
        }
        is ItemBlock -> {
            val text = remember(block, p) { annotate(block.spans, p) }
            val numbered = block.marker.firstOrNull()?.isLetterOrDigit() == true || block.marker.startsWith("(")
            Row(
                Modifier
                    .fillMaxWidth()
                    .padding(top = topGap, start = (block.depth * 18).dp)
                    .then(if (block.jump >= 0) Modifier.clickable { ctx.onJump(block.jump) } else Modifier)
            ) {
                Text(
                    if (numbered) block.marker else "\u2022",
                    style = t.body.copy(color = p.muted, fontWeight = FontWeight.Medium, textAlign = TextAlign.End),
                    modifier = Modifier.width(if (numbered) 30.dp else 22.dp)
                )
                Spacer(Modifier.width(8.dp))
                SelectionContainer(Modifier.weight(1f)) { Text(text, style = t.body) }
            }
        }
        is CodeBlock -> {
            Box(
                Modifier
                    .fillMaxWidth()
                    .padding(top = topGap)
                    .clip(RoundedCornerShape(16.dp))
                    .background(p.tonal)
                    .horizontalScroll(rememberScrollState())
                    .padding(16.dp)
            ) {
                SelectionContainer {
                    Text(
                        block.text,
                        style = t.body.copy(fontFamily = FontFamily.Monospace, fontSize = t.base * 0.82f, lineHeight = t.lineHeight * 0.86f, textAlign = TextAlign.Start),
                        softWrap = false
                    )
                }
            }
        }
        is LabelBlock -> {
            Box(
                Modifier
                    .padding(top = t.gap * 0.6f + topGap)
                    .clip(RoundedCornerShape(50))
                    .background(p.tonal)
                    .padding(horizontal = 12.dp, vertical = 5.dp)
            ) {
                Text(
                    block.text,
                    style = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.SemiBold, fontSize = (11.5f * t.settings.fontScale.coerceAtMost(1.4f)).sp, letterSpacing = 0.6.sp, color = p.ink)
                )
            }
        }
        is TableBlock -> RdTable(block, t, ctx, topGap)
        is FigureBlock -> RdFigure(block, t, ctx, maxWidth, topGap)
    }
}

@Composable
private fun RdTable(b: TableBlock, t: ReadType, ctx: RdCtx, topGap: Dp) {
    val p = t.p
    val cols = b.rows.maxOfOrNull { it.cells.size } ?: return
    val weights = remember(b) { (0 until cols).map { c -> b.rows.map { it.cells.getOrNull(c)?.length ?: 0 }.average().toFloat().coerceIn(3f, 40f) } }
    val cellStyle = t.body.copy(fontSize = t.base * 0.86f, lineHeight = t.lineHeight * 0.88f, textAlign = TextAlign.Start)
    val wide = cols >= 5
    Column(
        Modifier
            .fillMaxWidth()
            .padding(top = topGap)
            .clip(RoundedCornerShape(18.dp))
            .background(p.tonal)
            .then(if (wide) Modifier.horizontalScroll(rememberScrollState()) else Modifier)
    ) {
        b.rows.forEachIndexed { i, row ->
            Row(
                Modifier
                    .then(if (wide) Modifier else Modifier.fillMaxWidth())
                    .then(if (row.jump >= 0) Modifier.clickable { ctx.onJump(row.jump) } else Modifier)
                    .padding(horizontal = 14.dp, vertical = 11.dp),
                horizontalArrangement = Arrangement.spacedBy(14.dp)
            ) {
                for (c in 0 until cols) {
                    Text(
                        row.cells.getOrElse(c) { "" },
                        style = cellStyle.copy(fontWeight = if (b.header && i == 0) FontWeight.SemiBold else FontWeight.Normal, color = if (row.jump >= 0 && c == 0) p.accent else p.ink),
                        modifier = if (wide) Modifier.width(132.dp) else Modifier.weight(weights[c])
                    )
                }
            }
            if (i < b.rows.lastIndex) HorizontalDivider(color = p.line)
        }
    }
}

@Composable
private fun RdFigure(b: FigureBlock, t: ReadType, ctx: RdCtx, maxWidth: Dp, topGap: Dp) {
    val p = t.p
    val density = LocalDensity.current
    val dpPerPoint = t.base.value / ctx.source.bodyPoints().coerceAtLeast(4f)
    val natural = (b.widthPts * dpPerPoint).dp
    val width = minOf(maxWidth, natural.coerceAtLeast(if (b.equation) 24.dp else 120.dp))
    val aspect = (b.heightPts / b.widthPts.coerceAtLeast(1f)).coerceIn(0.02f, 6f)
    val widthPx = with(density) { width.roundToPx() }.coerceIn(64, 1500)
    val bitmap by produceState(ctx.source.cachedCrop(b.page, b.rect, widthPx), b, widthPx) {
        ctx.source.loadCrop(b.page, b.rect, widthPx)?.let { value = it }
    }
    val image = remember(bitmap) { bitmap?.asImageBitmap() }
    Box(Modifier.fillMaxWidth().padding(top = topGap + if (b.equation) 0.dp else 4.dp), contentAlignment = Alignment.Center) {
        Box(
            Modifier
                .width(width)
                .aspectRatio(1f / aspect)
                .clip(RoundedCornerShape(if (b.equation) 4.dp else 14.dp))
                .background(if (image == null) p.tonal else Color.Transparent)
                .clickable { ctx.onOpenPage(b.page) }
        ) {
            if (image != null) {
                Image(image, "Figure from page ${b.page + 1}", Modifier.fillMaxSize(), contentScale = ContentScale.FillBounds, colorFilter = p.filter)
            }
        }
    }
}

@Composable
private fun RdPage(
    page: Int, t: ReadType, ctx: RdCtx, maxWidth: Dp,
    onWords: (Int, Int) -> Unit
) {
    val p = t.p
    val load by produceState<RdLoad>(ctx.source.cached(page)?.let { RdLoad.Ready(it) } ?: RdLoad.Loading, page) {
        if (value is RdLoad.Ready) return@produceState
        val r = ctx.source.load(page)
        value = if (r != null) RdLoad.Ready(r) else RdLoad.Failed
    }
    val previous = ctx.source.cached(page - 1)
    when (val state = load) {
        RdLoad.Loading -> Box(Modifier.fillMaxWidth().height(380.dp).padding(top = 16.dp), contentAlignment = Alignment.TopCenter) {
            Box(Modifier.fillMaxWidth(0.7f).height(12.dp).clip(RoundedCornerShape(50)).background(p.tonal))
        }
        RdLoad.Failed -> Column(Modifier.fillMaxWidth().padding(vertical = 24.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("Page ${page + 1} could not be reflowed", style = MaterialTheme.typography.bodyMedium, color = p.muted)
            NebButton("Open the page as it is", { ctx.onOpenPage(page) }, tone = NebButtonTone.Tonal)
        }
        is RdLoad.Ready -> {
            LaunchedEffect(page, state) { onWords(page, state.page.words) }
            val blocks = state.page.blocks
            val joins = blocks.firstOrNull().let { first ->
                first is ParaBlock && first.startsLower && (previous?.blocks?.lastOrNull() as? ParaBlock)?.endsOpen == true
            }
            Column(Modifier.fillMaxWidth()) {
                if (!joins && page > 0) RdPageMark(page, p) { ctx.onOpenPage(page) }
                blocks.forEachIndexed { i, block ->
                    val gap = if (i == 0 && joins) 0.dp else if (i == 0) 0.dp else t.gap
                    RdBlock(block, t, ctx, maxWidth, gap)
                }
                if (blocks.isEmpty()) Spacer(Modifier.height(8.dp))
            }
        }
    }
}

@Composable
private fun RdPageMark(page: Int, p: ReadingPalette, onOpen: () -> Unit) {
    Row(
        Modifier.fillMaxWidth().padding(top = 22.dp, bottom = 14.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        HorizontalDivider(Modifier.weight(1f), color = p.line)
        Box(Modifier.padding(horizontal = 10.dp).clip(RoundedCornerShape(50)).clickable(onClick = onOpen).padding(horizontal = 10.dp, vertical = 4.dp)) {
            Text("Page ${page + 1}", style = MaterialTheme.typography.labelSmall, color = p.muted)
        }
        HorizontalDivider(Modifier.weight(1f), color = p.line)
    }
}

/** The article view of a PDF: a single column of reflowed text and pictures, set in the reader's own type. */
@OptIn(ExperimentalLayoutApi::class, ExperimentalMaterial3Api::class)
@Composable
fun ReadingMode(
    title: String,
    pageCount: Int,
    startPage: Int,
    jump: ReadJump?,
    settings: ReadingSettings,
    theme: ReadingTheme,
    look: ReaderLook,
    outline: List<OutlineItem>,
    bookmarked: Boolean,
    source: ReadSource,
    chromeVisible: Boolean,
    assistantHidden: Boolean,
    onChromeToggle: () -> Unit,
    onPage: (Int) -> Unit,
    onBack: () -> Unit,
    onToggleBookmark: () -> Unit,
    onContents: () -> Unit,
    onTypography: () -> Unit,
    onOriginal: (Int) -> Unit,
    onJumpPage: (Int) -> Unit,
    onZen: () -> Unit,
    onToggleAssistant: () -> Unit,
    modifier: Modifier = Modifier
) {
    val palette = remember(theme, look) { readingPalette(theme, look) }
    val t = remember(settings, palette) { ReadType(settings, palette) }
    val listState = rememberLazyListState(initialFirstVisibleItemIndex = startPage.coerceIn(0, (pageCount - 1).coerceAtLeast(0)))
    val scope = rememberCoroutineScope()
    val ctx = remember(source) { RdCtx(source, { onJumpPage(it) }, { onOriginal(it) }) }

    val current by remember(listState) {
        derivedStateOf {
            val info = listState.layoutInfo
            val mid = info.viewportStartOffset + info.viewportSize / 3
            info.visibleItemsInfo.firstOrNull { it.offset + it.size > mid }?.index ?: listState.firstVisibleItemIndex
        }
    }
    LaunchedEffect(listState) { snapshotFlow { current }.distinctUntilChanged().collect { onPage(it.coerceIn(0, pageCount - 1)) } }
    LaunchedEffect(jump) { jump?.let { listState.scrollToItem(it.page.coerceIn(0, pageCount - 1)) } }
    // pages are read ahead of the eye, so scrolling never meets a blank stretch
    LaunchedEffect(listState) {
        snapshotFlow { listState.firstVisibleItemIndex }.distinctUntilChanged().collect { first ->
            for (i in (first - 1)..(first + 3)) if (i in 0 until pageCount) source.load(i)
        }
    }

    // a running estimate of the words per page, for the time left
    var wordTotal by remember { mutableIntStateOf(0) }
    var wordPages by remember { mutableIntStateOf(0) }
    val seen = remember { HashSet<Int>() }
    val onWords: (Int, Int) -> Unit = { page, words -> if (seen.add(page)) { wordTotal += words; wordPages++ } }
    val wordsPerPage = if (wordPages > 0) wordTotal / wordPages.toFloat() else 260f
    val minutesLeft = (((pageCount - 1 - current).coerceAtLeast(0)) * wordsPerPage / 230f).roundToInt()

    // read aloud
    val context = LocalContext.current
    var listening by remember { mutableStateOf(false) }
    var speechPage by remember { mutableIntStateOf(0) }
    val listeningNow by rememberUpdatedState(listening)
    val speaker = remember { RdSpeaker(context) { if (listeningNow) speechPage++ } }
    DisposableEffect(Unit) { onDispose { speaker.shutdown() } }
    LaunchedEffect(listening, speechPage) {
        if (!listening) { speaker.stop(); return@LaunchedEffect }
        if (speechPage >= pageCount) { listening = false; return@LaunchedEffect }
        val text = source.load(speechPage)?.let { rdSpeechText(it) }.orEmpty()
        listState.animateScrollToItem(speechPage)
        if (text.isBlank()) { speechPage++; return@LaunchedEffect }
        speaker.speak(text)
    }

    val topInset = WindowInsets.statusBarsIgnoringVisibility.asPaddingValues().calculateTopPadding()
    val bottomInset = WindowInsets.navigationBarsIgnoringVisibility.asPaddingValues().calculateBottomPadding()
    val zen = settings.zen
    val showBars = chromeVisible && !zen
    val chapter = remember(outline, current) { outline.lastOrNull { it.page <= current }?.title }
    val progress = if (pageCount > 1) current / (pageCount - 1f) else 1f

    Box(modifier.fillMaxSize().background(palette.bg)) {
        BoxWithConstraintsContent(t) { maxWidth ->
            LazyColumn(
                state = listState,
                modifier = Modifier
                    .fillMaxSize()
                    .pointerInput(showBars, zen) {
                        detectTapGestures { offset ->
                            val h = size.height
                            when {
                                !showBars && offset.y < h * 0.18f -> scope.launch { listState.animateScrollBy(-h * 0.85f) }
                                !showBars && offset.y > h * 0.82f -> scope.launch { listState.animateScrollBy(h * 0.85f) }
                                else -> onChromeToggle()
                            }
                        }
                    },
                contentPadding = PaddingValues(
                    top = topInset + ReaderBarHeight + 10.dp, bottom = bottomInset + 120.dp, start = t.sidePadding, end = t.sidePadding
                ),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                items(count = pageCount, key = { it }) { page ->
                    Box(Modifier.widthIn(max = 680.dp).fillMaxWidth()) {
                        RdPage(page, t, ctx, minOf(maxWidth - t.sidePadding * 2, 680.dp), onWords)
                    }
                }
                item(key = "end") {
                    Column(
                        Modifier.widthIn(max = 680.dp).fillMaxWidth().padding(top = 40.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        Text("End of document", style = MaterialTheme.typography.titleSmall, color = palette.muted)
                        NebButton("Back to the start", { scope.launch { listState.scrollToItem(0) } }, tone = NebButtonTone.Tonal)
                    }
                }
            }
        }

        // a hairline of progress while the bars are away
        if (!showBars) {
            Box(Modifier.fillMaxWidth().windowInsetsPadding(WindowInsets.statusBarsIgnoringVisibility).height(2.dp)) {
                Box(Modifier.fillMaxWidth(progress.coerceIn(0f, 1f)).height(2.dp).background(palette.muted.copy(alpha = 0.7f)))
            }
        }

        // top bar
        AnimatedVisibility(
            visible = showBars,
            modifier = Modifier.align(Alignment.TopCenter),
            enter = slideInVertically(nebSpatialSpec()) { -it } + fadeIn(nebEffectsSpec()),
            exit = slideOutVertically(nebSpatialSpec()) { -it } + fadeOut(nebEffectsSpec())
        ) {
            Column(Modifier.fillMaxWidth().background(palette.bg.copy(alpha = 0.97f))) {
                Row(
                    Modifier.windowInsetsPadding(WindowInsets.statusBarsIgnoringVisibility).height(ReaderBarHeight).padding(horizontal = 6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    NebIconButton(Icons.AutoMirrored.Outlined.ArrowBack, "Back", onBack, tint = palette.ink)
                    Column(Modifier.weight(1f).padding(horizontal = 6.dp)) {
                        Text(title.ifBlank { "Document" }, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, color = palette.ink, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Text(chapter ?: "Reading mode", style = MaterialTheme.typography.labelMedium, color = palette.muted, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    }
                    NebIconButton(Icons.Outlined.Toc, "Contents", onContents, tint = palette.ink)
                    NebIconButton(Icons.Outlined.FormatSize, "Text and page settings", onTypography, tint = palette.ink)
                    var menu by remember { mutableStateOf(false) }
                    Box {
                        NebIconButton(Icons.Outlined.MoreVert, "More", { menu = true }, tint = palette.ink)
                        DropdownMenu(expanded = menu, onDismissRequest = { menu = false }) {
                            DropdownMenuItem(
                                text = { Text(if (bookmarked) "Remove bookmark" else "Bookmark this page") },
                                leadingIcon = { Icon(if (bookmarked) Icons.Outlined.Bookmark else Icons.Outlined.BookmarkBorder, null) },
                                onClick = { menu = false; onToggleBookmark() }
                            )
                            DropdownMenuItem(
                                text = { Text("Zen mode") },
                                leadingIcon = { Icon(Icons.Outlined.Fullscreen, null) },
                                onClick = { menu = false; onZen() }
                            )
                            DropdownMenuItem(
                                text = { Text(if (listening) "Stop reading aloud" else "Read aloud") },
                                leadingIcon = { Icon(Icons.Outlined.VolumeUp, null) },
                                onClick = { menu = false; speechPage = current; listening = !listening }
                            )
                            DropdownMenuItem(
                                text = { Text("View original PDF") },
                                leadingIcon = { Icon(Icons.Outlined.PictureAsPdf, null) },
                                onClick = { menu = false; onOriginal(current) }
                            )
                            DropdownMenuItem(
                                text = { Text(if (assistantHidden) "Show Neby AI button" else "Hide Neby AI button") },
                                leadingIcon = { Icon(Icons.Outlined.AutoAwesome, null) },
                                onClick = { menu = false; onToggleAssistant() }
                            )
                        }
                    }
                }
                HorizontalDivider(color = palette.line)
            }
        }

        // bottom bar
        AnimatedVisibility(
            visible = showBars,
            modifier = Modifier.align(Alignment.BottomCenter),
            enter = slideInVertically(nebSpatialSpec()) { it } + fadeIn(nebEffectsSpec()),
            exit = slideOutVertically(nebSpatialSpec()) { it } + fadeOut(nebEffectsSpec())
        ) {
            Column(Modifier.fillMaxWidth().background(palette.bg.copy(alpha = 0.97f))) {
                HorizontalDivider(color = palette.line)
                Column(Modifier.windowInsetsPadding(WindowInsets.navigationBarsIgnoringVisibility).padding(horizontal = 6.dp, vertical = 4.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        NebIconButton(
                            if (listening) Icons.Outlined.Pause else Icons.Outlined.PlayArrow,
                            if (listening) "Pause reading aloud" else "Read aloud",
                            { speechPage = current; listening = !listening },
                            tint = palette.ink
                        )
                        var dragging by remember { mutableStateOf<Float?>(null) }
                        if (pageCount > 1) {
                            Slider(
                                value = dragging ?: current.toFloat(),
                                onValueChange = { dragging = it },
                                onValueChangeFinished = { dragging?.let { v -> scope.launch { listState.scrollToItem(v.roundToInt()) } }; dragging = null },
                                valueRange = 0f..(pageCount - 1).toFloat(),
                                colors = SliderDefaults.colors(thumbColor = palette.ink, activeTrackColor = palette.ink, inactiveTrackColor = palette.line),
                                modifier = Modifier.weight(1f)
                            )
                        } else Spacer(Modifier.weight(1f))
                        Spacer(Modifier.width(8.dp))
                    }
                    Text(
                        "Page ${current + 1} of $pageCount" + if (minutesLeft > 0) "   \u00B7   ${if (minutesLeft >= 60) "${minutesLeft / 60} h ${minutesLeft % 60} min" else "$minutesLeft min"} left" else "",
                        style = MaterialTheme.typography.labelMedium, color = palette.muted,
                        modifier = Modifier.padding(start = 16.dp, bottom = 6.dp)
                    )
                }
            }
        }

        // leaving zen mode
        AnimatedVisibility(
            visible = chromeVisible && zen,
            modifier = Modifier.align(Alignment.BottomCenter),
            enter = fadeIn(nebEffectsSpec()), exit = fadeOut(nebEffectsSpec())
        ) {
            Row(
                Modifier
                    .windowInsetsPadding(WindowInsets.navigationBarsIgnoringVisibility)
                    .padding(bottom = 24.dp)
                    .clip(CircleShape)
                    .background(palette.ink)
                    .nebPressable(onClick = onZen)
                    .padding(horizontal = 16.dp, vertical = 10.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(Icons.Outlined.FullscreenExit, null, tint = palette.bg)
                Spacer(Modifier.width(8.dp))
                Text("Leave zen mode", style = MaterialTheme.typography.labelLarge, color = palette.bg)
            }
        }
    }
}

@Composable
private fun BoxWithConstraintsContent(t: ReadType, content: @Composable (Dp) -> Unit) {
    androidx.compose.foundation.layout.BoxWithConstraints(Modifier.fillMaxSize()) { content(maxWidth) }
}

/** Text size, type, margins and page colour; also the zen and Neby AI switches. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReadingSheet(
    settings: ReadingSettings,
    theme: ReadingTheme,
    assistantHidden: Boolean,
    onSettings: ((ReadingSettings) -> ReadingSettings) -> Unit,
    onTheme: (ReadingTheme) -> Unit,
    onAssistantHidden: (Boolean) -> Unit,
    onDismiss: () -> Unit
) {
    NebModalSheet(onDismiss = onDismiss, title = "Reading") {
        Column(Modifier.padding(horizontal = 22.dp).padding(bottom = 16.dp), verticalArrangement = Arrangement.spacedBy(18.dp)) {
            RdSliderRow("Text size", "${(settings.fontScale * 100).roundToInt()}%", settings.fontScale, 0.7f..2.2f) { v -> onSettings { it.copy(fontScale = (v * 20).roundToInt() / 20f) } }
            RdSliderRow("Line spacing", "${(settings.lineSpacing * 100).roundToInt()}%", settings.lineSpacing, 0.8f..1.6f) { v -> onSettings { it.copy(lineSpacing = (v * 10).roundToInt() / 10f) } }
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                RdLabel("Typeface")
                NebSegmentedChoice(
                    listOf(NebSegment(ReadingFont.Serif.name, "Serif"), NebSegment(ReadingFont.Sans.name, "Sans")),
                    settings.font.name, { v -> onSettings { it.copy(font = ReadingFont.valueOf(v)) } }, minHeight = 48.dp
                )
            }
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                RdLabel("Margins")
                NebSegmentedChoice(
                    listOf(NebSegment("0", "Narrow"), NebSegment("1", "Normal"), NebSegment("2", "Wide")),
                    settings.margin.toString(), { v -> onSettings { it.copy(margin = v.toInt()) } }, minHeight = 48.dp
                )
            }
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                RdLabel("Alignment")
                NebSegmentedChoice(
                    listOf(NebSegment("left", "Left"), NebSegment("justify", "Justified")),
                    if (settings.justify) "justify" else "left", { v -> onSettings { it.copy(justify = v == "justify") } }, minHeight = 48.dp
                )
            }
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                RdLabel("Page colour")
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    RdThemeTile("Paper", Color.White, Color(0xFF1C1B1A), theme == ReadingTheme.Paper, Modifier.weight(1f)) { onTheme(ReadingTheme.Paper) }
                    RdThemeTile("Sepia", Color(0xFFF4ECD8), Color(0xFF3B2F23), theme == ReadingTheme.Sepia, Modifier.weight(1f)) { onTheme(ReadingTheme.Sepia) }
                    RdThemeTile("Night", Color(0xFF141414), Color(0xFFE2E0DA), theme == ReadingTheme.Night, Modifier.weight(1f)) { onTheme(ReadingTheme.Night) }
                }
            }
            val auto = settings.brightness < 0f
            RdSliderRow("Brightness", if (auto) "Auto" else "${(settings.brightness * 100).roundToInt()}%", if (auto) 0.5f else settings.brightness, 0.05f..1f) { v -> onSettings { it.copy(brightness = v) } }
            if (!auto) NebButton("Use system brightness", { onSettings { it.copy(brightness = -1f) } }, tone = NebButtonTone.Text)
            NebToggleRow("Zen mode", null, settings.zen, { v -> onSettings { it.copy(zen = v) }; if (v) onDismiss() })
            NebToggleRow("Neby AI button", null, !assistantHidden, { v -> onAssistantHidden(!v) })
        }
    }
}

@Composable
private fun RdLabel(text: String) {
    Text(text, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
}

@Composable
private fun RdSliderRow(label: String, value: String, current: Float, range: ClosedFloatingPointRange<Float>, onChange: (Float) -> Unit) {
    Column {
        Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            RdLabel(label)
            Spacer(Modifier.weight(1f))
            Text(value, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold)
        }
        val ink = MaterialTheme.colorScheme.onSurface
        Slider(
            value = current.coerceIn(range.start, range.endInclusive), onValueChange = onChange, valueRange = range,
            colors = SliderDefaults.colors(thumbColor = ink, activeTrackColor = ink, inactiveTrackColor = MaterialTheme.colorScheme.outlineVariant)
        )
    }
}

@Composable
private fun RdThemeTile(label: String, paper: Color, ink: Color, selected: Boolean, modifier: Modifier, onClick: () -> Unit) {
    val shape = RoundedCornerShape(16.dp)
    Column(
        modifier
            .clip(shape)
            .background(paper)
            .then(if (selected) Modifier.border(2.dp, MaterialTheme.colorScheme.onSurface, shape) else Modifier)
            .nebPressable(onClick = onClick)
            .padding(vertical = 14.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        Text("Aa", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold, color = ink)
        Text(label, style = MaterialTheme.typography.labelMedium, color = ink.copy(alpha = if (selected) 1f else 0.7f), fontWeight = if (selected) FontWeight.Bold else FontWeight.Normal)
    }
}

private fun rdSpeechText(page: ReflowPage): String = buildString {
    for (b in page.blocks) {
        when (b) {
            is HeadingBlock -> append(b.text).append(".\n")
            is ParaBlock -> append(b.text).append('\n')
            is ItemBlock -> append(b.text).append('\n')
            is TableBlock -> b.rows.forEach { append(it.cells.joinToString(", ")).append(".\n") }
            else -> {}
        }
    }
}

/** Text to speech for read aloud: one page at a time, calls [onFinished] when the page has been spoken. */
private class RdSpeaker(context: Context, private val onFinished: () -> Unit) {
    private var tts: TextToSpeech? = null
    private val main = Handler(Looper.getMainLooper())
    @Volatile private var ready = false
    private var queued: String? = null

    init {
        tts = TextToSpeech(context.applicationContext) { status ->
            ready = status == TextToSpeech.SUCCESS
            if (ready) {
                tts?.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
                    override fun onStart(utteranceId: String?) {}
                    override fun onDone(utteranceId: String?) { if (utteranceId == "last") main.post { onFinished() } }
                    override fun onError(utteranceId: String?) {}
                })
                queued?.let { speak(it) }
            }
        }
    }

    fun speak(text: String) {
        val engine = tts
        if (engine == null || !ready) { queued = text; return }
        queued = null
        val chunks = ArrayList<String>()
        var rest = text.trim()
        while (rest.length > 3500) {
            var cut = rest.lastIndexOf(". ", 3500)
            if (cut < 1000) cut = rest.lastIndexOf(' ', 3500)
            if (cut < 1) cut = 3500
            chunks.add(rest.substring(0, cut + 1)); rest = rest.substring(cut + 1).trim()
        }
        if (rest.isNotEmpty()) chunks.add(rest)
        chunks.forEachIndexed { i, c ->
            engine.speak(c, if (i == 0) TextToSpeech.QUEUE_FLUSH else TextToSpeech.QUEUE_ADD, null, if (i == chunks.lastIndex) "last" else "c$i")
        }
    }

    fun stop() { queued = null; tts?.stop() }

    fun shutdown() { runCatching { tts?.stop(); tts?.shutdown() }; tts = null }
}
