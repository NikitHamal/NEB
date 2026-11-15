package com.neb.ians.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.key
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.isSpecified
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.input.key.Key
import androidx.compose.ui.input.key.KeyEventType
import androidx.compose.ui.input.key.key
import androidx.compose.ui.input.key.onPreviewKeyEvent
import androidx.compose.ui.input.key.type
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.TextLayoutResult
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.em
import coil.compose.AsyncImage
import kotlin.math.roundToInt

/**
 * The one writing field for posts, replies and notes. It shows what the text will look like, never the markers, and
 * pictures sit inside the text as small rounded thumbnails that move with the words around them. Tap a thumbnail to
 * open it, press and hold to drag it elsewhere, tap the cross to take it out.
 */
@Composable
fun RichTextField(
    state: RichState,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    placeholder: String = "",
    textStyle: TextStyle = MaterialTheme.typography.bodyLarge,
    minLines: Int = 1,
    maxLines: Int = Int.MAX_VALUE,
    chipDp: Float = 38f,
    onImageClick: (Int) -> Unit = {},
    onChange: ((androidx.compose.ui.text.input.TextFieldValue) -> Unit)? = null,
    keyboardCapitalization: KeyboardCapitalization = KeyboardCapitalization.Sentences,
    readOnly: Boolean = false,
    decorationBox: (@Composable (inner: @Composable () -> Unit) -> Unit)? = null
) {
    val scheme = MaterialTheme.colorScheme
    val density = LocalDensity.current
    val doc = state.doc
    val hasImages = doc.keys.isNotEmpty()
    val emPx = with(density) { textStyle.fontSize.toPx() }
    val chipPx = with(density) { chipDp.dp.toPx() }
    val gapPx = emPx * 0.4f

    val style = remember(textStyle, hasImages, density) {
        if (!hasImages) textStyle else {
            val need = with(density) { (chipDp + 8f).dp.toSp() }
            val cur = textStyle.lineHeight
            textStyle.copy(lineHeight = if (cur.isSp && cur.value >= need.value) cur else need)
        }
    }
    val measurer = rememberTextMeasurer()
    val advance = remember(style, measurer) {
        val w = runCatching { measurer.measure(AnnotatedString(InlineImageTokens.PLACEHOLDER_CHAR.toString()), style).size.width.toFloat() }
            .getOrDefault(emPx * 0.6f)
        if (w > 1f) w else emPx * 0.6f
    }
    val spacing: TextUnit = remember(advance, chipPx, gapPx, emPx) {
        val n = InlineImageTokens.PLACEHOLDER_LEN
        val extra = ((chipPx + gapPx) - advance * n) / (n - 1)
        if (extra > 0.5f) (extra / emPx).em else TextUnit.Unspecified
    }
    val built = remember(doc, scheme, spacing) {
        RichVisual.build(
            doc,
            LiveColors(scheme.surfaceContainerHighest, scheme.onSurface, scheme.primary, scheme.onSurfaceVariant, scheme.onSurfaceVariant),
            spacing
        )
    }
    var layout by remember { mutableStateOf<TextLayoutResult?>(null) }
    // where a dragged picture would land: the caret is drawn there while the finger is down
    var dropCaret by remember { mutableStateOf<androidx.compose.ui.geometry.Rect?>(null) }
    val value = state.value

    Box(modifier = modifier, propagateMinConstraints = true) {
        BasicTextField(
            value = value,
            onValueChange = onChange ?: state::onChange,
            enabled = enabled,
            readOnly = readOnly,
            textStyle = style.copy(color = if (style.color.isSpecified) style.color else scheme.onSurface),
            cursorBrush = SolidColor(scheme.primary),
            minLines = minLines,
            maxLines = maxLines,
            visualTransformation = built.transformation,
            keyboardOptions = KeyboardOptions(capitalization = keyboardCapitalization),
            onTextLayout = { layout = it },
            modifier = Modifier
                .fillMaxWidth()
                .onPreviewKeyEvent { e -> e.type == KeyEventType.KeyDown && e.key == Key.Backspace && state.backspaceAtLineStart() },
            decorationBox = { inner ->
                if (decorationBox != null) decorationBox(inner) else Box {
                    if (value.text.isEmpty() && placeholder.isNotEmpty()) {
                        Text(text = placeholder, style = style.copy(color = scheme.onSurfaceVariant), maxLines = 1)
                    }
                    inner()
                }
            }
        )
        val lr = layout
        if (lr != null && decorationBox == null && hasImages) Box(Modifier.matchParentSize()) {
            doc.keys.forEachIndexed { index, imageKey ->
                val slot = built.slots.getOrNull(index) ?: return@forEachIndexed
                val box = runCatching { lr.getBoundingBox(slot) }.getOrNull() ?: return@forEachIndexed
                val left = box.left + gapPx / 2f
                val line = runCatching { lr.getLineForOffset(slot) }.getOrDefault(0)
                val lineTop = lr.getLineTop(line)
                val lineBottom = lr.getLineBottom(line)
                // centred in its own line and never above it, so the line the keyboard scrolls into view holds the whole picture
                val top = (lineTop + (lineBottom - lineTop - chipPx) / 2f).coerceAtLeast(lineTop)
                key(imageKey) {
                    RichChip(
                        model = imageKey.toIntOrNull()?.let { resolveMediaUrl("/media/content_images/${it}t.webp") } ?: state.uris[imageKey],
                        sizeDp = chipDp,
                        leftPx = left,
                        topPx = top,
                        enabled = enabled,
                        onOpen = { onImageClick(index) },
                        onRemove = { state.removeImage(state.doc.keys.indexOf(imageKey)) },
                        onHover = { center ->
                            dropCaret = center?.let { runCatching { lr.getCursorRect(lr.getOffsetForPosition(it)) }.getOrNull() }
                        },
                        onDrop = { center ->
                            val at = built.toOriginal(lr.getOffsetForPosition(center))
                            dropCaret = null
                            state.moveImage(state.doc.keys.indexOf(imageKey), at)
                        }
                    )
                }
            }
        }
        dropCaret?.let { r ->
            Box(
                Modifier
                    .offset { IntOffset((r.left - with(density) { 1.25.dp.toPx() }).roundToInt(), r.top.roundToInt()) }
                    .size(width = 2.5.dp, height = with(density) { r.height.toDp() })
                    .clip(RoundedCornerShape(2.dp))
                    .background(scheme.primary)
            )
        }
    }
}

@Composable
private fun RichChip(
    model: Any?,
    sizeDp: Float,
    leftPx: Float,
    topPx: Float,
    enabled: Boolean,
    onOpen: () -> Unit,
    onRemove: () -> Unit,
    onHover: (Offset?) -> Unit,
    onDrop: (Offset) -> Unit
) {
    val scheme = MaterialTheme.colorScheme
    val density = LocalDensity.current
    val sizePx = with(density) { sizeDp.dp.toPx() }
    var drag by remember { mutableStateOf(Offset.Zero) }
    var lifted by remember { mutableStateOf(false) }
    val left by rememberUpdatedState(leftPx)
    val top by rememberUpdatedState(topPx)
    val drop by rememberUpdatedState(onDrop)
    val hover by rememberUpdatedState(onHover)
    val shape = RoundedCornerShape(10.dp)

    Box(
        modifier = Modifier
            .offset { IntOffset((left + drag.x).roundToInt(), (top + drag.y).roundToInt()) }
            .size(sizeDp.dp)
            .graphicsLayer { val k = if (lifted) 1.12f else 1f; scaleX = k; scaleY = k }
            .alpha(if (lifted) 0.85f else 1f)
            .clip(shape)
            .background(scheme.surfaceContainerHigh)
            .pointerInput(enabled) {
                if (!enabled) return@pointerInput
                detectDragGesturesAfterLongPress(
                    onDragStart = { lifted = true; drag = Offset.Zero },
                    onDrag = { change, amount ->
                        change.consume(); drag += amount
                        hover(Offset(left + drag.x + sizePx / 2f, top + drag.y + sizePx / 2f))
                    },
                    onDragEnd = {
                        val center = Offset(left + drag.x + sizePx / 2f, top + drag.y + sizePx / 2f)
                        lifted = false; drag = Offset.Zero
                        drop(center)
                    },
                    onDragCancel = { lifted = false; drag = Offset.Zero; hover(null) }
                )
            }
    ) {
        AsyncImage(
            model = model,
            contentDescription = "Picture in text",
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .size(sizeDp.dp)
                .clickable(enabled = enabled, interactionSource = remember { MutableInteractionSource() }, indication = null, onClick = onOpen)
        )
        Box(
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(2.dp)
                .size(18.dp)
                .clip(CircleShape)
                .background(Color.Black.copy(alpha = 0.62f))
                .clickable(enabled = enabled, interactionSource = remember { MutableInteractionSource() }, indication = null, onClick = onRemove),
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Filled.Close, contentDescription = "Remove picture", tint = Color.White, modifier = Modifier.size(12.dp))
        }
    }
}

/**
 * An editor state wired to Markdown held somewhere else (a view model, a draft). Edits are sent out as Markdown; a value
 * that arrives from outside and is not the echo of what was just sent replaces the text (a cleared draft, a mention).
 */
@Composable
fun rememberRichState(
    markdown: String,
    caret: Int = markdown.length,
    maxChars: Int = Int.MAX_VALUE,
    onMarkdown: (markdown: String, caret: Int) -> Unit
): RichState {
    val state = remember { RichState(maxChars).also { it.setMarkdown(markdown, caret) } }
    val latest by rememberUpdatedState(onMarkdown)
    remember(state) { state.onEdited = { r -> latest(r.lastMarkdown, r.lastCaret) } }
    LaunchedEffect(markdown, caret) { state.adopt(markdown, caret) }
    return state
}
