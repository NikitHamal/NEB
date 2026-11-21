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
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.text.InlineTextContent
import androidx.compose.foundation.text.appendInlineContent
import androidx.compose.ui.text.Placeholder
import androidx.compose.ui.text.PlaceholderVerticalAlign
import androidx.compose.runtime.key
import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.material.icons.outlined.ExpandMore
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.gestures.animateScrollBy
import androidx.compose.foundation.layout.asPaddingValues
import androidx.compose.foundation.clickable
import androidx.compose.foundation.selection.selectable
import androidx.compose.material.icons.outlined.TextDecrease
import androidx.compose.material.icons.outlined.TextIncrease
import androidx.compose.ui.semantics.CustomAccessibilityAction
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.customActions
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.foundation.gestures.detectTapGestures
import com.neb.ians.ui.components.nebHorizontalScroll
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.outlined.KeyboardArrowDown
import androidx.compose.material.icons.outlined.KeyboardArrowUp
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.layout.LayoutCoordinates
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.layout.positionInRoot
import androidx.compose.ui.text.input.ImeAction
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
import androidx.compose.foundation.layout.windowInsetsTopHeight
import androidx.compose.foundation.layout.windowInsetsBottomHeight
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.navigationBars
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
import com.neb.ians.ui.components.NebDropdownMenu
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
    ReadingTheme.Paper -> ReadingPalette(Color.White, Color(0xFF16171A), Color(0xFF62656C), Color(0xFF0058DF), Color(0xFFF3F4F6), Color(0xFFE2E4E8), null)
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

/** Text where each private use character (a formula set as a picture) becomes a slot the picture is drawn in. */
internal fun AnnotatedString.Builder.putMath(text: String) {
    var from = 0
    for (i in text.indices) {
        if (isMathChar(text[i])) {
            if (i > from) append(text.substring(from, i))
            appendInlineContent("m${text[i].code - MATH_BASE}", " ")
            from = i + 1
        }
    }
    if (from < text.length) append(text.substring(from))
}

private fun mathText(text: String): AnnotatedString = buildAnnotatedString { putMath(text) }

internal fun plainText(text: String): String = if (text.any { isMathChar(it) }) text.filterNot { isMathChar(it) } else text

/** The slots of a block's text, each filled with the crop of its formula at the size of the text around it. */
@Composable
private fun rememberInline(page: Int, text: String, t: ReadType, ctx: RdCtx): Map<String, InlineTextContent> {
    val has = text.any { isMathChar(it) }
    val inl = if (has) ctx.source.cached(page)?.inlines else null
    val factor = t.base.value / ctx.source.bodyPoints().coerceAtLeast(4f)
    val p = t.p
    return remember(inl, factor, p, has) { inlineMap(inl, factor, p, ctx.source) }
}

/**
 * The slot of every formula in a page's text. A formula drawn from outlines gets a slot centred on the text's middle
 * and tall enough for it, so its baseline lines up with the words; one that needs the page (text or a picture in it)
 * is a crop of the page.
 */
internal fun inlineMap(inl: List<InlineImg>?, factor: Float, p: ReadingPalette, source: ReadSource): Map<String, InlineTextContent> {
    val map = HashMap<String, InlineTextContent>()
    inl?.forEachIndexed { k, img ->
        val w = (img.widthPts * factor).coerceAtLeast(2f)
        val art = img.vec
        if (art != null) {
            val half = img.half
            val h = (2f * half * factor).coerceAtLeast(2f)
            val shift = half - img.center
            map["m$k"] = InlineTextContent(Placeholder(w.sp, h.sp, PlaceholderVerticalAlign.TextCenter)) {
                RdVector(art, p.ink, Modifier.fillMaxSize(), shift)
            }
        } else {
            val h = (img.heightPts * factor).coerceAtLeast(2f)
            map["m$k"] = InlineTextContent(Placeholder(w.sp, h.sp, PlaceholderVerticalAlign.TextCenter)) { RdInlineMath(img, w, source, p) }
        }
    }
    return map
}

@Composable
private fun RdInlineMath(img: InlineImg, widthSp: Float, source: ReadSource, p: ReadingPalette) {
    val density = LocalDensity.current
    val px = (with(density) { widthSp.sp.toPx() } * 2f).roundToInt().coerceIn(24, 1500)
    val bitmap by produceState(source.cachedCrop(img.page, img.rect, px), img, px) {
        source.loadCrop(img.page, img.rect, px)?.let { value = it }
    }
    val image = remember(bitmap) { bitmap?.asImageBitmap() }
    if (image != null) {
        Image(image, "Formula", Modifier.fillMaxSize(), contentScale = ContentScale.FillBounds, colorFilter = inkMask(p.ink))
    }
}

private val MarkChip = Regex("\\[\\d+(?:\\.\\d+)?\\]")
private val ExamTag = Regex("\\((?:NEB|HSEB|SEE|CDC|TU|IOE|CEE|NEET|JEE)\\b[^)]{0,32}\\)")

/** The marks chip [1] and exam tags (NEB 2081) are quieter than the question they follow, as they are in print. */
private fun AnnotatedString.withTags(p: ReadingPalette): AnnotatedString {
    val t = text
    if (t.indexOf('[') < 0 && t.indexOf('(') < 0) return this
    val b = AnnotatedString.Builder(this)
    for (m in MarkChip.findAll(t)) b.addStyle(SpanStyle(fontSize = 0.78.em, fontWeight = FontWeight.Medium, color = p.muted, background = p.muted.copy(alpha = 0.14f)), m.range.first, m.range.last + 1)
    for (m in ExamTag.findAll(t)) b.addStyle(SpanStyle(fontSize = 0.86.em, fontWeight = FontWeight.Medium, color = p.muted), m.range.first, m.range.last + 1)
    return b.toAnnotatedString()
}

private fun annotate(spans: List<Span>, p: ReadingPalette): AnnotatedString = annotateRaw(spans, p).withTags(p)

private fun annotateRaw(spans: List<Span>, p: ReadingPalette): AnnotatedString {
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
                withLink(LinkAnnotation.Url(href, linkStyle)) { withStyle(style) { putMath(s.text) } }
                continue
            }
            var last = 0
            for (m in UrlPattern.findAll(s.text)) {
                var value = m.value
                while (value.isNotEmpty() && value.last() in ".,;:!?)]\"'") value = value.dropLast(1)
                if (value.length < 4) continue
                val start = m.range.first
                withStyle(style) { putMath(s.text.substring(last, start)) }
                val url = if (value.startsWith("http", ignoreCase = true)) value else "https://$value"
                withLink(LinkAnnotation.Url(url, linkStyle)) { withStyle(style) { putMath(value) } }
                last = start + value.length
            }
            withStyle(style) { putMath(s.text.substring(last)) }
        }
    }
}

private class RdCtx(
    val source: ReadSource,
    val onJump: (Int) -> Unit,
    val onOpenPage: (Int) -> Unit,
    /** The text being searched for (empty: nothing is marked) and the occurrence that is current. */
    val query: String = "",
    val active: ReadHit? = null,
    val jumpId: Int = 0,
    val onZoom: (RdZoomItem) -> Unit = {},
    val onActiveShown: (Float, Int) -> Unit = { _, _ -> }
) {
    /** Which occurrence inside block [index] of [page] is the current hit, or -1. */
    fun activeIn(page: Int, index: Int): Int = active?.takeIf { it.page == page && it.block == index }?.nth ?: -1
}

/** Reports where the current search hit sits on screen once, so the list can bring it to the eye. */
@Composable
private fun Modifier.searchAnchor(ctx: RdCtx, activeNth: Int): Modifier {
    if (activeNth < 0) return this
    var coords by remember { mutableStateOf<LayoutCoordinates?>(null) }
    LaunchedEffect(ctx.jumpId, coords) {
        val c = coords ?: return@LaunchedEffect
        if (c.isAttached) ctx.onActiveShown(c.positionInRoot().y, ctx.jumpId)
    }
    return this.onGloballyPositioned { coords = it }
}

private sealed interface RdLoad {
    data object Loading : RdLoad
    data object Failed : RdLoad
    class Ready(val page: ReflowPage) : RdLoad
}

@Composable
private fun RdBlock(block: Block, page: Int, index: Int, t: ReadType, ctx: RdCtx, maxWidth: Dp, topGap: Dp) {
    val p = t.p
    val q = ctx.query
    val activeNth = ctx.activeIn(page, index)
    when (block) {
        is HeadingBlock -> {
            val extra = when (block.level) { 1 -> t.gap * 1.6f; 2 -> t.gap * 1.0f; else -> t.gap * 0.4f }
            val text = remember(block, q, activeNth) { AnnotatedString(plainText(block.text)).marked(q, activeNth) }
            Text(
                text,
                style = t.heading(block.level),
                modifier = Modifier
                    .fillMaxWidth()
                    .searchAnchor(ctx, activeNth)
                    .padding(top = extra + topGap)
                    .then(if (block.jump >= 0) Modifier.clickable { ctx.onJump(block.jump) } else Modifier)
            )
        }
        is ParaBlock -> {
            val text = remember(block, p, q, activeNth) { annotate(block.spans, p).marked(q, activeNth) }
            val m = Modifier.fillMaxWidth().searchAnchor(ctx, activeNth).padding(top = topGap)
            val math = rememberInline(page, block.text, t, ctx)
            val callout = remember(block) { if (block.jump < 0) CalloutPattern.find(block.text) else null }
            if (callout != null) {
                val label = remember(callout) { calloutLabel(callout.groupValues[1]) }
                val body = remember(text, callout) { text.subSequence(callout.range.last + 1, text.length) }
                RdCallout(label, body, t.body, p, foldable = isAnswerCallout(label), folded = t.settings.hideAnswers, forceOpen = q.isNotEmpty(), modifier = m, math = math)
            } else if (block.jump >= 0) {
                Text(text, style = t.body.copy(color = p.accent), inlineContent = math, modifier = m.clickable { ctx.onJump(block.jump) })
            } else {
                SelectionContainer { Text(text, style = t.body, inlineContent = math, modifier = m) }
            }
        }
        is ItemBlock -> {
            val text = remember(block, p, q, activeNth) { annotate(block.spans, p).marked(q, activeNth) }
            val numbered = block.marker.firstOrNull()?.isLetterOrDigit() == true || block.marker.startsWith("(")
            val math = rememberInline(page, block.text, t, ctx)
            Row(
                Modifier
                    .fillMaxWidth()
                    .searchAnchor(ctx, activeNth)
                    .padding(top = topGap, start = (block.depth * 18).dp)
                    .then(if (block.jump >= 0) Modifier.clickable { ctx.onJump(block.jump) } else Modifier)
            ) {
                Text(
                    if (numbered) block.marker else "\u2022",
                    style = t.body.copy(color = if (numbered) p.accent else p.muted, fontFamily = Poppins, fontWeight = FontWeight.SemiBold, fontSize = t.base * 0.92f, textAlign = TextAlign.End),
                    modifier = Modifier.width(if (numbered) 30.dp else 22.dp)
                )
                Spacer(Modifier.width(8.dp))
                SelectionContainer(Modifier.weight(1f)) { Text(text, style = t.body, inlineContent = math) }
            }
        }
        is CodeBlock -> {
            val code = remember(block, q, activeNth) { AnnotatedString(block.text).marked(q, activeNth) }
            Box(
                Modifier
                    .fillMaxWidth()
                    .searchAnchor(ctx, activeNth)
                    .padding(top = topGap)
                    .clip(RoundedCornerShape(16.dp))
                    .background(p.tonal)
                    .nebHorizontalScroll(rememberScrollState())
                    .padding(16.dp)
            ) {
                SelectionContainer {
                    Text(
                        code,
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
                    .background(if (LocalRdInCard.current) p.bg else p.tonal)
                    .padding(horizontal = 12.dp, vertical = 5.dp)
            ) {
                Text(
                    block.text,
                    style = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.SemiBold, fontSize = (11.5f * t.settings.fontScale.coerceAtMost(1.4f)).sp, letterSpacing = 0.6.sp, color = p.ink)
                )
            }
        }
        is TableBlock -> RdTable(block, page, t, ctx, topGap, activeNth)
        is FigureBlock -> RdFigure(block, t, ctx, maxWidth, topGap)
    }
}

@Composable
private fun RdTable(b: TableBlock, page: Int, t: ReadType, ctx: RdCtx, topGap: Dp, activeNth: Int) {
    Column(Modifier.fillMaxWidth()) {
        RdTableBody(b, page, t, ctx, topGap, activeNth)
        if ((b.rows.maxOfOrNull { it.cells.size } ?: 0) >= 4) Row(
            Modifier
                .align(Alignment.End)
                .padding(top = 6.dp)
                .clip(RoundedCornerShape(50))
                .clickable { ctx.onZoom(RdZoomItem.Table(b, page)) }
                .padding(horizontal = 10.dp, vertical = 5.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            Icon(Icons.Outlined.Fullscreen, null, Modifier.size(16.dp), tint = t.p.muted)
            Text("Expand", style = MaterialTheme.typography.labelMedium, color = t.p.muted)
        }
    }
}

@Composable
private fun RdTableBody(b: TableBlock, page: Int, t: ReadType, ctx: RdCtx, topGap: Dp, activeNth: Int) {
    val p = t.p
    val hasMath = remember(b) { b.rows.any { r -> r.cells.any { c -> c.any { isMathChar(it) } } } }
    val math = rememberInline(page, if (hasMath) "\uE000" else "", t, ctx)
    val cols = b.rows.maxOfOrNull { it.cells.size } ?: return
    val q = ctx.query
    // how many matches come before each cell, so the current one can be found inside the table
    val before = remember(b, q) {
        var n = 0
        b.rows.map { r -> (0 until cols).map { c -> n.also { n += occurrences(r.cells.getOrElse(c) { "" }, q).size } } }
    }
    val weights = remember(b) { (0 until cols).map { c -> b.rows.map { it.cells.getOrNull(c)?.sumOf { ch -> if (isMathChar(ch)) 9 else 1 } ?: 0 }.average().toFloat().coerceIn(3f, 40f) } }
    val cellStyle = t.body.copy(fontSize = t.base * 0.86f, lineHeight = t.lineHeight * 0.88f, textAlign = TextAlign.Start)
    val wide = cols >= 5
    Column(
        Modifier
            .fillMaxWidth()
            .searchAnchor(ctx, activeNth)
            .padding(top = topGap)
            .clip(RoundedCornerShape(18.dp))
            .background(p.tonal)
            .then(if (wide) Modifier.nebHorizontalScroll(rememberScrollState()) else Modifier)
    ) {
        b.rows.forEachIndexed { i, row ->
            Row(
                Modifier
                    .then(if (wide) Modifier else Modifier.fillMaxWidth())
                    .then(if (b.header && i == 0) Modifier.background(p.line.copy(alpha = 0.55f)) else Modifier)
                    .then(if (row.jump >= 0) Modifier.clickable { ctx.onJump(row.jump) } else Modifier)
                    .padding(horizontal = 14.dp, vertical = 11.dp),
                horizontalArrangement = Arrangement.spacedBy(14.dp)
            ) {
                for (c in 0 until cols) {
                    val cell = row.cells.getOrElse(c) { "" }
                    val local = activeNth - before[i][c]
                    Text(
                        mathText(cell).marked(q, if (local >= 0 && local < occurrences(cell, q).size) local else -1),
                        inlineContent = math,
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
private fun RdFigure(b: FigureBlock, t: ReadType, ctx: RdCtx, maxWidth: Dp, topGap: Dp, alignStart: Boolean = false) {
    val p = t.p
    val density = LocalDensity.current
    val dpPerPoint = t.base.value / ctx.source.bodyPoints().coerceAtLeast(4f)
    val natural = (b.widthPts * dpPerPoint).dp
    val width = minOf(maxWidth, natural.coerceAtLeast(if (b.equation) 24.dp else 120.dp))
    val aspect = (b.heightPts / b.widthPts.coerceAtLeast(1f)).coerceIn(0.02f, 6f)
    val art = b.vec
    if (art != null) {
        Box(Modifier.fillMaxWidth().padding(top = topGap), contentAlignment = if (alignStart) Alignment.CenterStart else Alignment.Center) {
            RdVector(
                art, p.ink,
                Modifier.width(width).aspectRatio(1f / aspect).clickable { ctx.onZoom(RdZoomItem.Figure(b)) }
                    .semantics { contentDescription = "Equation from page ${b.page + 1}" }
            )
        }
        return
    }
    val widthPx = with(density) { width.roundToPx() }.coerceIn(64, 1500)
    val bitmap by produceState(ctx.source.cachedCrop(b.page, b.rect, widthPx), b, widthPx) {
        ctx.source.loadCrop(b.page, b.rect, widthPx)?.let { value = it }
    }
    val image = remember(bitmap) { bitmap?.asImageBitmap() }
    Box(Modifier.fillMaxWidth().padding(top = topGap + if (b.equation) 0.dp else 4.dp), contentAlignment = if (alignStart) Alignment.CenterStart else Alignment.Center) {
        Box(
            Modifier
                .width(width)
                .aspectRatio(1f / aspect)
                .clip(RoundedCornerShape(if (b.equation) 4.dp else 14.dp))
                .background(if (image == null) p.tonal else Color.Transparent)
                .clickable { ctx.onZoom(RdZoomItem.Figure(b)) }
        ) {
            if (image != null) {
                Image(image, (if (b.equation) "Equation from page " else "Figure from page ") + (b.page + 1), Modifier.fillMaxSize(), contentScale = ContentScale.FillBounds,
                    colorFilter = if (b.equation) inkMask(p.ink) else if (LocalRdInCard.current && p.filter == null) androidx.compose.ui.graphics.ColorFilter.tint(p.tonal, androidx.compose.ui.graphics.BlendMode.Multiply) else p.filter)
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
                (first is ParaBlock && first.startsLower && (previous?.blocks?.lastOrNull() as? ParaBlock)?.endsOpen == true) ||
                    // the choices of a question that began at the foot of the page before
                    (first is ItemBlock && first.choiceCols > 0 && first.marker.trim().trim('(', ')', '.', ':').equals("a", true) &&
                        (previous?.blocks?.lastOrNull() as? ItemBlock)?.let { it.choiceCols == 0 } == true)
            }
            Column(Modifier.fillMaxWidth()) {
                if (!joins && page > 0) Spacer(Modifier.height(t.gap * 0.7f))
                RdBlocks(blocks, 0, blocks.size, page, t, ctx, maxWidth, if (joins) t.gap * 0.5f else 0.dp)
                if (blocks.isEmpty()) Spacer(Modifier.height(8.dp))
            }
        }
    }
}

private val LocalRdInCard = androidx.compose.runtime.compositionLocalOf { false }
private val AnswerKeyLabel = Regex("^(answers?|solutions?|answer key|marking scheme|mark scheme)\\b", RegexOption.IGNORE_CASE)

/** Blocks [from] until [to] of a page: tonal cards for blocks that share a box id, choice grids for lettered choices. */
@Composable
private fun RdBlocks(blocks: List<Block>, from: Int, to: Int, page: Int, t: ReadType, ctx: RdCtx, maxWidth: Dp, firstGap: Dp) {
    val inCard = LocalRdInCard.current
    var i = from
    while (i < to) {
        val gap = if (i == from) firstGap else t.gap
        val at = i
        val box = blocks[i].box
        if (box > 0 && !inCard) {
            var j = i + 1
            while (j < to && blocks[j].box == box) j++
            val end = j
            key(page, at) { RdCard(blocks, at, end, page, t, ctx, maxWidth, gap) }
            i = j
            continue
        }
        val run = optionRun(blocks, i)
        if (run != null && i + run.length <= to) {
            key(page, at) { RdChoices(run, page, t, ctx, gap) }
            i += run.length
        } else {
            key(page, at) { RdBlock(blocks[at], page, at, t, ctx, maxWidth, gap) }
            i++
        }
    }
}

/** The print `.box` as a tonal card. An answer key folds under its title when "Hide answers" is on. */
@Composable
private fun RdCard(blocks: List<Block>, from: Int, to: Int, page: Int, t: ReadType, ctx: RdCtx, maxWidth: Dp, topGap: Dp) {
    val p = t.p
    val first = blocks[from]
    val key = first as? LabelBlock
    val answerKey = key != null && AnswerKeyLabel.containsMatchIn(key.text.trim())
    var open by remember(page, from, answerKey, t.settings.hideAnswers) { mutableStateOf(!(answerKey && t.settings.hideAnswers)) }
    val shown = open || ctx.query.isNotEmpty() || !answerKey
    val turn by animateFloatAsState(if (shown) 180f else 0f, label = "card-chevron")
    Column(
        Modifier
            .fillMaxWidth()
            .padding(top = topGap)
            .clip(RoundedCornerShape(22.dp))
            .background(p.tonal)
            .animateContentSize()
            .padding(horizontal = 16.dp, vertical = 14.dp)
    ) {
        androidx.compose.runtime.CompositionLocalProvider(LocalRdInCard provides true) {
            if (answerKey && key != null) {
                Row(
                    Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .clickable(role = Role.Button, onClickLabel = if (shown) "Hide the answers" else "Show the answers") { open = !open }
                        .padding(vertical = 4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(Modifier.clip(RoundedCornerShape(50)).background(p.bg).padding(horizontal = 12.dp, vertical = 5.dp)) {
                        Text(
                            key.text,
                            style = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.SemiBold, fontSize = (11.5f * t.settings.fontScale.coerceAtMost(1.4f)).sp, letterSpacing = 0.6.sp, color = p.ink)
                        )
                    }
                    Spacer(Modifier.weight(1f))
                    Icon(Icons.Outlined.ExpandMore, null, tint = p.muted, modifier = Modifier.size(22.dp).graphicsLayer { rotationZ = turn })
                }
            }
            if (shown) RdBlocks(blocks, if (answerKey) from + 1 else from, to, page, t, ctx, maxWidth - 32.dp, if (answerKey) t.gap * 0.45f else 0.dp)
        }
    }
}

/**
 * Lettered choices, set the way print sets them and not as buttons: a letter tile and the text, in a grid that follows the
 * printed layout (four across, two by two, or one under another) and gives way to fewer columns when the type is large.
 */
@Composable
private fun RdChoices(run: OptionRun, page: Int, t: ReadType, ctx: RdCtx, topGap: Dp) {
    val density = LocalDensity.current
    val colGap = with(density) { 16.dp.roundToPx() }
    val rowGap = with(density) { (t.gap.value * 0.42f).dp.roundToPx() }
    androidx.compose.ui.layout.Layout(
        content = { run.rows.forEach { row -> RdChoice(row, page, t, ctx) } },
        modifier = Modifier.fillMaxWidth().padding(top = topGap * 0.45f, start = 38.dp)
    ) { ms, c ->
        val n = ms.size
        val maxW = c.maxWidth
        val natural = ms.map { it.maxIntrinsicWidth(0) }
        var cols = minOf(run.cols, n)
        while (cols > 1) {
            val cw = (maxW - colGap * (cols - 1)) / cols
            if (natural.all { it <= cw }) break
            cols--
        }
        if (cols == 3 && n == 4) cols = 2
        val cw = ((maxW - colGap * (cols - 1)) / cols).coerceAtLeast(0)
        val placeables = ms.map { it.measure(androidx.compose.ui.unit.Constraints.fixedWidth(cw)) }
        val rowsH = placeables.chunked(cols).map { r -> r.maxOf { it.height } }
        val height = rowsH.sum() + rowGap * (rowsH.size - 1).coerceAtLeast(0)
        layout(maxW, height) {
            var y = 0
            placeables.chunked(cols).forEachIndexed { r, items ->
                items.forEachIndexed { k, pl -> pl.placeRelative(k * (cw + colGap), y) }
                y += rowsH[r] + rowGap
            }
        }
    }
}

@Composable
private fun RdChoice(row: OptionRow, page: Int, t: ReadType, ctx: RdCtx) {
    val p = t.p
    val b = row.item
    val activeNth = ctx.activeIn(page, row.at)
    val text = remember(b, p, ctx.query, activeNth) { annotate(b.spans, p).marked(ctx.query, activeNth) }
    val letter = b.marker.trim().trim('(', ')', '.', ':').uppercase()
    val tile = with(LocalDensity.current) { (t.lineHeight.toDp() * 0.8f).coerceIn(22.dp, 40.dp) }
    val pad = with(LocalDensity.current) { ((t.lineHeight.toDp() - tile) / 2).coerceAtLeast(0.dp) }
    val inCard = LocalRdInCard.current
    Row(
        Modifier.searchAnchor(ctx, activeNth).semantics(mergeDescendants = true) { },
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Box(Modifier.padding(top = pad).size(tile).clip(RoundedCornerShape(tile * 0.34f)).background(if (inCard) p.bg else p.tonal), contentAlignment = Alignment.Center) {
            Text(letter, style = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.SemiBold, fontSize = t.base * 0.66f, color = p.accent))
        }
        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            if (b.text.isNotBlank() || row.figures.isEmpty()) Text(text, style = t.body.copy(textAlign = TextAlign.Start), inlineContent = rememberInline(page, b.text, t, ctx))
            row.figures.forEach { f -> RdFigure(f, t, ctx, 260.dp, 0.dp, alignStart = true) }
        }
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
    search: ReadSearch,
    onSearchOpen: () -> Unit,
    onSearchQuery: (String) -> Unit,
    onSearchStep: (Int) -> Unit,
    onSearchClose: () -> Unit,
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
    onFontScale: (Float) -> Unit,
    modifier: Modifier = Modifier
) {
    val palette = remember(theme, look) { readingPalette(theme, look) }
    val t = remember(settings, palette) { ReadType(settings, palette) }
    val listState = rememberLazyListState(initialFirstVisibleItemIndex = startPage.coerceIn(0, (pageCount - 1).coerceAtLeast(0)))
    val scope = rememberCoroutineScope()
    var handledJump by remember { mutableIntStateOf(0) }
    var zoomItem by remember { mutableStateOf<RdZoomItem?>(null) }
    var pinchLive by remember { mutableStateOf<Float?>(null) }
    val ctx = remember(source, search.marking, search.current, search.jump) {
        RdCtx(source, { onJumpPage(it) }, { onOriginal(it) }, search.marking, search.current, search.jump, onZoom = { zoomItem = it }) { y, id ->
            // the hit is on screen now: bring it to the upper third, once per request
            if (id != handledJump) {
                handledJump = id
                scope.launch { listState.animateScrollBy(y - listState.layoutInfo.viewportSize.height * 0.3f) }
            }
        }
    }
    LaunchedEffect(search.jump) {
        val hit = search.current ?: return@LaunchedEffect
        val page = hit.page.coerceIn(0, pageCount - 1)
        if (search.jump > 0 && listState.layoutInfo.visibleItemsInfo.none { it.index == page }) listState.scrollToItem(page)
    }

    val current by remember(listState) {
        derivedStateOf {
            val info = listState.layoutInfo
            val mid = info.viewportStartOffset + info.viewportSize.height / 3
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
    val showBars = (chromeVisible && !zen) || search.open
    val chapter = remember(outline, current) { outline.lastOrNull { it.page <= current }?.title }
    val progress = if (pageCount > 1) current / (pageCount - 1f) else 1f

    Box(modifier.fillMaxSize().background(palette.bg)) {
        BoxWithConstraintsContent(t) { maxWidth ->
            LazyColumn(
                state = listState,
                modifier = Modifier
                    .fillMaxSize()
                    .semantics {
                        customActions = listOf(
                            CustomAccessibilityAction("Larger text") { onFontScale(((settings.fontScale + 0.1f).coerceIn(0.7f, 3f) * 20).roundToInt() / 20f); true },
                            CustomAccessibilityAction("Smaller text") { onFontScale(((settings.fontScale - 0.1f).coerceIn(0.7f, 3f) * 20).roundToInt() / 20f); true }
                        )
                    }
                    .pinchTextSize(settings.fontScale, onFontScale, { pinchLive = it })
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
                items(count = pageCount, key = { it }, contentType = { "page" }) { page ->
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

        pinchLive?.let { RdSizeBadge(it, palette, Modifier.align(Alignment.Center)) }
        zoomItem?.let { item ->
            RdZoomDialog(item, palette, source, onClose = { zoomItem = null }, onOpenPage = onOriginal)
        }

        // a hairline of progress while the bars are away
        if (!showBars) {
            Box(Modifier.fillMaxWidth().windowInsetsPadding(WindowInsets.statusBarsIgnoringVisibility).height(2.dp)) {
                Box(Modifier.fillMaxWidth(progress.coerceIn(0f, 1f)).height(2.dp).background(palette.muted.copy(alpha = 0.7f)))
            }
        }

        // what the system draws over the page (status icons, the navigation buttons) always sits on the page colour
        Spacer(Modifier.align(Alignment.TopCenter).fillMaxWidth().windowInsetsTopHeight(WindowInsets.statusBars).background(palette.bg))
        Spacer(Modifier.align(Alignment.BottomCenter).fillMaxWidth().windowInsetsBottomHeight(WindowInsets.navigationBars).background(palette.bg))

        // top bar
        AnimatedVisibility(
            visible = showBars,
            modifier = Modifier.align(Alignment.TopCenter),
            enter = slideInVertically(nebSpatialSpec()) { -it } + fadeIn(nebEffectsSpec()),
            exit = slideOutVertically(nebSpatialSpec()) { -it } + fadeOut(nebEffectsSpec())
        ) {
            Column(Modifier.fillMaxWidth().background(palette.bg)) {
                if (search.open) RdSearchRow(search, pageCount, palette, onSearchQuery, onSearchStep, onSearchClose) else Row(
                    Modifier.windowInsetsPadding(WindowInsets.statusBarsIgnoringVisibility).height(ReaderBarHeight).padding(horizontal = 6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    NebIconButton(Icons.AutoMirrored.Outlined.ArrowBack, "Back", onBack, tint = palette.ink)
                    Column(Modifier.weight(1f).padding(horizontal = 6.dp)) {
                        Text(title.ifBlank { "Document" }, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, color = palette.ink, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Text(chapter ?: "Reading mode", style = MaterialTheme.typography.labelMedium, color = palette.muted, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    }
                    NebIconButton(Icons.Outlined.Search, "Search", onSearchOpen, tint = palette.ink)
                    NebIconButton(Icons.Outlined.Toc, "Contents", onContents, tint = palette.ink)
                    NebIconButton(Icons.Outlined.FormatSize, "Text and page settings", onTypography, tint = palette.ink)
                    var menu by remember { mutableStateOf(false) }
                    Box {
                        NebIconButton(Icons.Outlined.MoreVert, "More", { menu = true }, tint = palette.ink)
                        NebDropdownMenu(expanded = menu, onDismissRequest = { menu = false }) {
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
            visible = showBars && !search.open,
            modifier = Modifier.align(Alignment.BottomCenter),
            enter = slideInVertically(nebSpatialSpec()) { it } + fadeIn(nebEffectsSpec()),
            exit = slideOutVertically(nebSpatialSpec()) { it } + fadeOut(nebEffectsSpec())
        ) {
            Column(Modifier.fillMaxWidth().background(palette.bg)) {
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
                                modifier = Modifier.weight(1f).semantics { stateDescription = "Page ${(dragging ?: current.toFloat()).roundToInt() + 1} of $pageCount" }
                            )
                        } else Spacer(Modifier.weight(1f))
                        NebIconButton(
                            Icons.Outlined.TextDecrease, "Smaller text",
                            { onFontScale(((settings.fontScale - 0.1f).coerceIn(0.7f, 3f) * 20).roundToInt() / 20f) }, tint = palette.ink
                        )
                        NebIconButton(
                            Icons.Outlined.TextIncrease, "Larger text",
                            { onFontScale(((settings.fontScale + 0.1f).coerceIn(0.7f, 3f) * 20).roundToInt() / 20f) }, tint = palette.ink
                        )
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
            visible = chromeVisible && zen && !search.open,
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

/** The top bar while searching: a field in the page's own colours, the match count and previous and next. */
@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun RdSearchRow(
    search: ReadSearch,
    pageCount: Int,
    p: ReadingPalette,
    onQuery: (String) -> Unit,
    onStep: (Int) -> Unit,
    onClose: () -> Unit
) {
    val focus = remember { FocusRequester() }
    LaunchedEffect(Unit) { runCatching { focus.requestFocus() } }
    Column(Modifier.fillMaxWidth()) {
        Row(
            Modifier.windowInsetsPadding(WindowInsets.statusBarsIgnoringVisibility).height(ReaderBarHeight).padding(horizontal = 6.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            NebIconButton(Icons.AutoMirrored.Outlined.ArrowBack, "Close search", onClose, tint = p.ink)
            Box(Modifier.weight(1f).padding(horizontal = 6.dp), contentAlignment = Alignment.CenterStart) {
                if (search.query.isEmpty()) Text("Search", style = MaterialTheme.typography.bodyLarge, color = p.muted)
                BasicTextField(
                    value = search.query,
                    onValueChange = onQuery,
                    singleLine = true,
                    textStyle = MaterialTheme.typography.bodyLarge.copy(color = p.ink),
                    cursorBrush = SolidColor(p.ink),
                    keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                    keyboardActions = KeyboardActions(onSearch = { onStep(1) }),
                    modifier = Modifier.fillMaxWidth().focusRequester(focus)
                )
            }
            val label = when {
                search.query.trim().length < 2 -> ""
                search.hits.isNotEmpty() -> "${search.index + 1} / ${search.hits.size}${if (search.running) "+" else ""}"
                search.running -> "\u2026"
                else -> "None"
            }
            Text(label, style = MaterialTheme.typography.labelLarge, color = p.muted, modifier = Modifier.padding(horizontal = 4.dp))
            NebIconButton(Icons.Outlined.KeyboardArrowUp, "Previous match", { onStep(-1) }, tint = p.ink)
            NebIconButton(Icons.Outlined.KeyboardArrowDown, "Next match", { onStep(1) }, tint = p.ink)
        }
        if (search.running && pageCount > 0) {
            LinearProgressIndicator(
                progress = { search.scanned / pageCount.toFloat() },
                color = p.ink, trackColor = Color.Transparent,
                modifier = Modifier.fillMaxWidth().height(2.dp)
            )
        }
    }
}

@Composable
private fun BoxWithConstraintsContent(t: ReadType, content: @Composable (Dp) -> Unit) {
    androidx.compose.foundation.layout.BoxWithConstraints(Modifier.fillMaxSize()) { content(maxWidth) }
}

private fun rdSpeechText(page: ReflowPage): String = buildString {
    for (b in page.blocks) {
        when (b) {
            is HeadingBlock -> append(b.text).append(".\n")
            is ParaBlock -> append(plainText(b.text)).append('\n')
            is ItemBlock -> append(plainText(b.text)).append('\n')
            is TableBlock -> b.rows.forEach { append(plainText(it.cells.joinToString(", "))).append(".\n") }
            else -> {}
        }
    }
}

/** Text to speech for read aloud: one page at a time, calls [onFinished] when the page has been spoken. */
internal class RdSpeaker(context: Context, private val onFinished: () -> Unit) {
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
