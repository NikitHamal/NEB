package com.neb.ians.ui.components

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextLayoutResult
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.input.OffsetMapping
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.input.TransformedText
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.em
import coil.compose.AsyncImage
import com.neb.ians.data.api.InlineImageUploadResponse
import kotlinx.coroutines.launch

/**
 * Controller handed to [InlineImageField] so host screens can trigger the
 * photo picker (e.g. from a toolbar button): call [pickImage].
 */
class InlineImageFieldHandle {
    internal var requestPick: (() -> Unit)? = null

    fun pickImage() {
        requestPick?.invoke()
    }
}

@Composable
fun rememberInlineImageFieldHandle(): InlineImageFieldHandle =
    remember { InlineImageFieldHandle() }

/** Resolved info for one chip rendered inside the editor overlay. */
data class InlineChipState(
    val token: String,
    val id: Int?,
    val pendingKey: String?,
    val imageModel: Any,
    val fullUrl: String,
    val aspectRatio: Float?
)

/**
 * Meta-style inline image editor field. Tokens (`[[img:ID]]`) collapse to a
 * single invisible char via [InlineImageVisualTransformation]; thumbnails are
 * drawn as an overlay at each placeholder's bounding box.
 *
 * - Tap chip → fullscreen viewer (uploaded only)
 * - X on chip → removes it
 * - Backspace beside a chip → deletes the whole chip
 * - Pending uploads show a local preview + shimmer until the server id lands
 */
@Composable
fun InlineImageField(
    value: TextFieldValue,
    onValueChange: (TextFieldValue) -> Unit,
    uploader: suspend (Uri) -> Result<InlineImageUploadResponse>,
    onError: (String) -> Unit,
    handle: InlineImageFieldHandle,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    placeholder: String = "",
    textStyle: TextStyle = MaterialTheme.typography.bodyMedium,
    minLines: Int = 1,
    maxLines: Int = 8,
    onPendingCountChange: (Int) -> Unit = {},
    onImageClick: (String) -> Unit = {}
) {
    val scope = rememberCoroutineScope()
    val currentValue by rememberUpdatedState(value)
    var layout by remember { mutableStateOf<TextLayoutResult?>(null) }
    val pendingMeta = remember { mutableStateMapOf<String, Pair<Int, Int>?>() }
    val pendingUris = remember { mutableStateMapOf<String, Uri>() }
    val uploadedMeta = remember { mutableStateMapOf<Int, Pair<Int, Int>>() }
    var pendingCount by remember { mutableIntStateOf(0) }

    fun bumpPending(delta: Int) {
        pendingCount = (pendingCount + delta).coerceAtLeast(0)
        onPendingCountChange(pendingCount)
    }

    fun insertToken(token: String) {
        val sel = currentValue.selection.end.coerceIn(0, currentValue.text.length)
        val newText = StringBuilder(currentValue.text).insert(sel, token).toString()
        onValueChange(TextFieldValue(text = newText, selection = TextRange(sel + token.length)))
    }

    fun startUpload(uri: Uri) {
        val textNow = currentValue.text
        if (InlineImageTokens.countTokens(textNow) >= InlineImageTokens.MAX_IMAGES_PER_CONTENT) {
            onError("Maximum ${InlineImageTokens.MAX_IMAGES_PER_CONTENT} images per post")
            return
        }
        if (InlineImageTokens.hasPending(textNow)) {
            onError("Wait for the current image to finish uploading")
            return
        }
        val key = InlineImageTokens.newPendingKey()
        pendingUris[key] = uri
        insertToken(InlineImageTokens.pendingToken(key))
        bumpPending(+1)

        scope.launch {
            val result = uploader(uri)
            val pendingToken = InlineImageTokens.pendingToken(key)
            val latest = currentValue.text
            if (result.isSuccess) {
                val res = result.getOrNull()!!
                uploadedMeta[res.id] = res.width to res.height
                onValueChange(
                    TextFieldValue(
                        text = InlineImageTokens.replacePendingKey(latest, key, res.id),
                        selection = currentValue.selection
                    )
                )
            } else {
                onValueChange(
                    TextFieldValue(
                        text = InlineImageTokens.removeToken(latest, pendingToken),
                        selection = currentValue.selection
                    )
                )
                onError(result.exceptionOrNull()?.message ?: "Image upload failed")
            }
            pendingUris.remove(key)
            bumpPending(-1)
        }
    }

    val picker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia()
    ) { uri ->
        if (uri != null && enabled) startUpload(uri)
    }

    SideEffect {
        handle.requestPick = {
            if (enabled) {
                picker.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
            }
        }
    }

    val density = LocalDensity.current
    val emPx = with(density) { textStyle.fontSize.toPx() }
    val minChipHeightPx = with(density) { INLINE_CHIP_MIN_HEIGHT_DP.dp.toPx() }

    val hasInlineImages = remember(value.text) { InlineImageTokens.countTokens(value.text) > 0 }
    val horizontalGapPx = emPx * 0.36f
    val editorTextStyle = remember(textStyle, hasInlineImages, density) {
        if (!hasInlineImages) {
            textStyle
        } else {
            val chipFromFont = textStyle.fontSize * INLINE_CHIP_HEIGHT_EM
            val chipMin = with(density) { INLINE_CHIP_MIN_HEIGHT_DP.dp.toSp() }
            val chipLine =
                if (chipFromFont.isSp && chipMin.isSp && chipFromFont.value < chipMin.value) chipMin else chipFromFont
            val current = textStyle.lineHeight
            val desired = if (chipLine.isSp) chipLine * 1.03f else chipLine
            val lineHeight =
                if (current.isSp && current.value >= desired.value) current else desired
            textStyle.copy(lineHeight = lineHeight)
        }
    }

    val textMeasurer = rememberTextMeasurer()
    val glyphAdvancePx = remember(editorTextStyle, textMeasurer) {
        try {
            val r = textMeasurer.measure(
                text = AnnotatedString(InlineImageTokens.PLACEHOLDER_CHAR.toString()),
                style = editorTextStyle,
            )
            val w = r.size.width.toFloat()
            if (w > 1f) w else emPx * 0.62f
        } catch (_: Exception) {
            emPx * 0.62f
        }
    }

    val mapping: InlineImageVisualTransformation.Mapping = run {
        val raw = value.text
        val matches = InlineImageTokens.REGEX.findAll(raw).toList()
        if (matches.isEmpty()) {
            InlineImageVisualTransformation.Mapping(
                TransformedText(AnnotatedString(raw), OffsetMapping.Identity),
                emptyList(),
                emptyList()
            )
        } else {
            val ranges = matches.map { it.range.first..it.range.last }
            val desiredWidthsPx = ranges.map { r ->
                val token = raw.substring(r.first, r.last + 1)
                val inner = token.removeSurrounding("[[img:", "]]")
                val numeric = inner.toIntOrNull()
                val aspect: Float? = if (numeric != null) {
                    uploadedMeta[numeric]?.let { (w, h) -> if (h > 0) w.toFloat() / h else null }
                } else {
                    pendingMeta[inner]?.let { d -> d?.let { (w, h) -> if (h > 0) w.toFloat() / h else null } }
                }
                val a = aspect ?: 2.2f
                val hPx = (emPx * INLINE_CHIP_HEIGHT_EM).coerceAtLeast(minChipHeightPx)
                val maxW = emPx * INLINE_CHIP_MAX_WIDTH_EM
                val minW = hPx * 1.05f
                val w = (hPx * a).coerceIn(minW, maxW)
                w + horizontalGapPx
            }
            val pieces = mutableListOf<Pair<String, Boolean>>()
            var cursor = 0
            ranges.forEach { r ->
                if (r.first > cursor) pieces.add(raw.substring(cursor, r.first) to false)
                pieces.add(raw.substring(r.first, r.last + 1) to true)
                cursor = r.last + 1
            }
            if (cursor < raw.length) pieces.add(raw.substring(cursor) to false)
            var tokenIdxForSpacing = 0
            val annotated = buildAnnotatedString {
                pieces.forEach { (segment, isToken) ->
                    if (isToken) {
                        val desired = desiredWidthsPx[tokenIdxForSpacing]
                        val defaultRun = glyphAdvancePx * InlineImageTokens.PLACEHOLDER_LEN
                        val extraPerGap = if (desired > defaultRun) (desired - defaultRun) / (InlineImageTokens.PLACEHOLDER_LEN - 1) else 0f
                        val spacing: TextUnit = if (extraPerGap > 0.5f) (extraPerGap / emPx).em else TextUnit.Unspecified
                        val style = if (spacing != TextUnit.Unspecified) SpanStyle(color = Color.Transparent, letterSpacing = spacing) else SpanStyle(color = Color.Transparent)
                        pushStyle(style)
                        append(InlineImageTokens.PLACEHOLDER)
                        pop()
                        tokenIdxForSpacing++
                    } else {
                        append(segment)
                    }
                }
            }
            val origToTrans = IntArray(raw.length + 1)
            val transToOrig = IntArray(annotated.length + 1)
            val placeholders = mutableListOf<Int>()
            var o = 0
            var t = 0
            pieces.forEach { (segment, isToken) ->
                if (isToken) {
                    val startO = o
                    val endO = o + segment.length
                    placeholders.add(t)
                    origToTrans[startO] = t
                    for (i in startO until endO) origToTrans[i] = t
                    origToTrans[endO] = t + InlineImageTokens.PLACEHOLDER_LEN
                    repeat(InlineImageTokens.PLACEHOLDER_LEN) { k -> transToOrig[t + k] = startO }
                    transToOrig[t + InlineImageTokens.PLACEHOLDER_LEN] = endO
                    o = endO
                    t += InlineImageTokens.PLACEHOLDER_LEN
                } else {
                    repeat(segment.length) { _ ->
                        origToTrans[o] = t
                        transToOrig[t] = o
                        o += 1
                        t += 1
                    }
                    origToTrans[o] = t
                    transToOrig[t] = o
                }
            }
            val offsetMapping = object : OffsetMapping {
                override fun originalToTransformed(offset: Int): Int = origToTrans[offset.coerceIn(0, raw.length)]
                override fun transformedToOriginal(offset: Int): Int = transToOrig[offset.coerceIn(0, annotated.length)]
            }
            InlineImageVisualTransformation.Mapping(
                TransformedText(annotated, offsetMapping),
                placeholders.toList(),
                ranges
            )
        }
    }
    val transformation = remember(mapping) {
        object : VisualTransformation {
            override fun filter(text: AnnotatedString): TransformedText = mapping.transformed
        }
    }

    val chips = remember(
        mapping, value.text,
        uploadedMeta.keys.toList(), pendingMeta.keys.toList(), pendingUris.keys.toList()
    ) {
        buildChips(
            text = value.text,
            ranges = mapping.tokenRanges,
            pendingMeta = pendingMeta,
            pendingUris = pendingUris,
            uploadedMeta = uploadedMeta
        )
    }

    Box(modifier = modifier) {
        BasicTextField(
            value = value,
            onValueChange = onValueChange,
            enabled = enabled,
            textStyle = editorTextStyle.copy(color = MaterialTheme.colorScheme.onSurface),
            cursorBrush = SolidColor(MaterialTheme.colorScheme.primary),
            minLines = minLines,
            maxLines = maxLines,
            visualTransformation = transformation,
            onTextLayout = { layout = it },
            decorationBox = { inner ->
                Box {
                    if (value.text.isEmpty() && placeholder.isNotEmpty()) {
                        Text(
                            text = placeholder,
                            style = editorTextStyle.copy(color = MaterialTheme.colorScheme.onSurfaceVariant),
                            maxLines = 1
                        )
                    }
                    inner()
                }
            },
            modifier = Modifier
        )

        val layoutResult = layout
        if (layoutResult != null) {
            chips.forEachIndexed { index, chip ->
                val slot = mapping.placeholderIndices.getOrNull(index) ?: return@forEachIndexed
                val boxes = (0 until InlineImageTokens.PLACEHOLDER_LEN).mapNotNull { k ->
                    runCatching { layoutResult.getBoundingBox(slot + k) }.getOrNull()
                }
                if (boxes.isEmpty()) return@forEachIndexed
                val leftPx = boxes.first().left + horizontalGapPx / 2f
                val chipHeightPx = (emPx * INLINE_CHIP_HEIGHT_EM).coerceAtLeast(minChipHeightPx)
                val topPx = boxes.first().top + (boxes.first().bottom - boxes.first().top - chipHeightPx) / 2f
                InlineChipOverlay(
                    chip = chip,
                    leftPx = leftPx,
                    topPx = topPx,
                    heightEm = INLINE_CHIP_HEIGHT_EM,
                    maxWidthEm = INLINE_CHIP_MAX_WIDTH_EM,
                    radiusEm = 0.42f,
                    onRemove = {
                        val range = mapping.tokenRanges.getOrNull(index) ?: return@InlineChipOverlay
                        val newText = currentValue.text.removeRange(range.first, range.last + 1)
                        onValueChange(
                            TextFieldValue(
                                text = newText,
                                selection = TextRange(range.first.coerceAtMost(newText.length))
                            )
                        )
                    },
                    onClick = { if (chip.id != null) onImageClick(chip.fullUrl) },
                    onDrop = { center ->
                        val sourceRange = mapping.tokenRanges.getOrNull(index)
                        if (sourceRange != null) {
                            val targetTransformed = layoutResult.getOffsetForPosition(center)
                            val targetOriginal = mapping.transformed.offsetMapping
                                .transformedToOriginal(targetTransformed)
                            val sourceEndExclusive = sourceRange.last + 1
                            if (targetOriginal !in sourceRange.first..sourceEndExclusive) {
                                val token = currentValue.text.substring(sourceRange.first, sourceEndExclusive)
                                val textWithoutToken = currentValue.text.removeRange(sourceRange)
                                val adjustedTarget = (if (targetOriginal > sourceEndExclusive) {
                                    targetOriginal - token.length
                                } else {
                                    targetOriginal
                                }).coerceIn(0, textWithoutToken.length)
                                val movedText = buildString(currentValue.text.length) {
                                    append(textWithoutToken, 0, adjustedTarget)
                                    append(token)
                                    append(textWithoutToken, adjustedTarget, textWithoutToken.length)
                                }
                                onValueChange(
                                    TextFieldValue(
                                        text = movedText,
                                        selection = TextRange(adjustedTarget + token.length)
                                    )
                                )
                            }
                        }
                    },
                    enabled = enabled,
                    fontSizePx = emPx
                )
            }
        }
    }
}

private const val INLINE_CHIP_HEIGHT_EM = 2.1f
private const val INLINE_CHIP_MAX_WIDTH_EM = 5.5f
private const val INLINE_CHIP_MIN_HEIGHT_DP = 36f

@Composable
private fun InlineChipOverlay(
    chip: InlineChipState,
    leftPx: Float,
    topPx: Float,
    heightEm: Float,
    maxWidthEm: Float,
    radiusEm: Float,
    fontSizePx: Float,
    onRemove: () -> Unit,
    onClick: () -> Unit,
    onDrop: (Offset) -> Unit,
    enabled: Boolean
) {
    val density = androidx.compose.ui.platform.LocalDensity.current.density
    val heightDp = (fontSizePx * heightEm / density)
        .coerceAtLeast(INLINE_CHIP_MIN_HEIGHT_DP)
        .dp
    val widthDp = (heightDp.value * (chip.aspectRatio ?: 2.2f))
        .coerceAtMost(fontSizePx * maxWidthEm / density)
        .coerceAtLeast(heightDp.value * 1.05f)
        .dp
    val shape = RoundedCornerShape((radiusEm * fontSizePx / density).dp.coerceAtLeast(4.dp))
    var dragOffset by remember(chip.token) { mutableStateOf(Offset.Zero) }
    var isDragging by remember(chip.token) { mutableStateOf(false) }
    val localDensity = LocalDensity.current
    val widthPx = with(localDensity) { widthDp.toPx() }
    val heightPx = with(localDensity) { heightDp.toPx() }
    val currentLeftPx by rememberUpdatedState(leftPx)
    val currentTopPx by rememberUpdatedState(topPx)
    val currentWidthPx by rememberUpdatedState(widthPx)
    val currentHeightPx by rememberUpdatedState(heightPx)
    val currentOnDrop by rememberUpdatedState(onDrop)

    val shimmer = rememberInfiniteTransition(label = "nebChipShimmer")
    val alpha by shimmer.animateFloat(
        initialValue = 0.55f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(900), RepeatMode.Reverse),
        label = "nebChipAlpha"
    )

    Box(
        modifier = Modifier
            .offsetPx(leftPx + dragOffset.x, topPx + dragOffset.y)
            .alpha(if (chip.pendingKey != null) alpha else if (isDragging) 0.72f else 1f)
            .size(width = widthDp, height = heightDp)
            .clip(shape)
            .background(MaterialTheme.colorScheme.surfaceContainerHigh)
            .border(BorderStroke(0.75.dp, MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.7f)), shape)
            .pointerInput(chip.token, enabled) {
                if (!enabled) return@pointerInput
                detectDragGestures(
                    onDragStart = {
                        dragOffset = Offset.Zero
                        isDragging = true
                    },
                    onDrag = { change, amount ->
                        change.consume()
                        dragOffset += amount
                    },
                    onDragEnd = {
                        val dropCenter = Offset(
                            currentLeftPx + dragOffset.x + currentWidthPx / 2f,
                            currentTopPx + dragOffset.y + currentHeightPx / 2f
                        )
                        isDragging = false
                        dragOffset = Offset.Zero
                        currentOnDrop(dropCenter)
                    },
                    onDragCancel = {
                        isDragging = false
                        dragOffset = Offset.Zero
                    }
                )
            }
    ) {
        AsyncImage(
            model = chip.imageModel,
            contentDescription = "Attached image",
            modifier = Modifier
                .size(width = widthDp, height = heightDp)
                .clickable(
                    enabled = enabled && chip.id != null,
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null,
                    onClick = onClick
                ),
            contentScale = ContentScale.Crop
        )
        Surface(
            onClick = onRemove,
            enabled = enabled,
            shape = CircleShape,
            color = Color.Black.copy(alpha = 0.65f),
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(1.dp)
                .size(15.dp)
        ) {
            Box(contentAlignment = Alignment.Center) {
                Icon(
                    imageVector = Icons.Filled.Close,
                    contentDescription = "Remove image",
                    tint = Color.White,
                    modifier = Modifier.size(10.dp)
                )
            }
        }
    }
}

private fun Modifier.offsetPx(x: Float, y: Float): Modifier =
    this.then(Modifier.offset { IntOffset(x.toInt(), y.toInt()) })

private fun buildChips(
    text: String,
    ranges: List<IntRange>,
    pendingMeta: Map<String, Pair<Int, Int>?>,
    pendingUris: Map<String, Uri>,
    uploadedMeta: Map<Int, Pair<Int, Int>>
): List<InlineChipState> {
    return ranges.mapNotNull { r ->
        val token = text.substring(r.first, r.last + 1)
        val inner = token.removeSurrounding("[[img:", "]]")
        val numeric = inner.toIntOrNull()
        if (numeric != null) {
            val dims = uploadedMeta[numeric]
            InlineChipState(
                token = token,
                id = numeric,
                pendingKey = null,
                imageModel = resolveMediaUrl("/media/content_images/${numeric}t.webp") ?: "",
                fullUrl = resolveMediaUrl("/media/content_images/$numeric.webp") ?: "",
                aspectRatio = dims?.let { (w, h) -> if (h > 0) w.toFloat() / h.toFloat() else null }
            )
        } else {
            val uri = pendingUris[inner] ?: return@mapNotNull null
            val dims = pendingMeta[inner]
            InlineChipState(
                token = token,
                id = null,
                pendingKey = inner,
                imageModel = uri,
                fullUrl = "",
                aspectRatio = dims?.let { (w, h) -> if (h > 0) w.toFloat() / h.toFloat() else null }
            )
        }
    }
}
