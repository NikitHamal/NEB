package com.neb.ians.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.InlineTextContent
import androidx.compose.foundation.text.appendInlineContent
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.Placeholder
import androidx.compose.ui.text.PlaceholderVerticalAlign
import androidx.compose.ui.text.TextLayoutResult
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.em
import coil.compose.AsyncImage

/** Prefix for inline-content ids carrying an image id ("nebimg:<id>"). */
const val INLINE_IMG_PREFIX = "nebimg:"

/**
 * Builds the [InlineTextContent] map that renders `[[img:ID]]` tokens as small
 * tappable thumbnails flowing with the text — the native counterpart of the
 * web `.neb-chip` styling (1.55em tall, 2.2em wide, 6dp radius, hairline
 * outline). Only ids actually present in [text] get entries.
 */
@Composable
fun rememberInlineImageContents(
    text: String,
    onClick: (String) -> Unit
): Map<String, InlineTextContent> {
    if (!text.contains("[[img:")) return emptyMap()
    val outline = MaterialTheme.colorScheme.outlineVariant
    val surfaceHigh = MaterialTheme.colorScheme.surfaceContainerHigh
    val ids = remember(text) { InlineImageTokens.extractIds(text) }
    return remember(ids, outline, surfaceHigh) {
        if (ids.isEmpty()) {
            emptyMap<String, InlineTextContent>()
        } else {
            ids.associateWith { id ->
                InlineTextContent(
                    placeholder = Placeholder(
                        width = 2.2f.em,
                        height = 1.55f.em,
                        placeholderVerticalAlign = PlaceholderVerticalAlign.TextCenter
                    )
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .clip(RoundedCornerShape(6.dp))
                            .background(surfaceHigh)
                            .border(BorderStroke(0.75.dp, outline.copy(alpha = 0.7f)), RoundedCornerShape(6.dp))
                            .clickable {
                                onClick(resolveMediaUrl("/media/content_images/$id.webp") ?: "")
                            }
                    ) {
                        AsyncImage(
                            model = resolveMediaUrl("/media/content_images/${id}t.webp"),
                            contentDescription = "Attached image",
                            modifier = Modifier.fillMaxSize(),
                            contentScale = ContentScale.Crop
                        )
                    }
                }
            }
        }
    }
}

/**
 * Drop-in replacement for ClickableText that ALSO supports inlineContent
 * (ClickableText has no inlineContent parameter). Tap resolution mirrors
 * ClickableText: reports the character offset under the tap. Inline chips are
 * real composables and consume their own taps before this handler fires.
 */
@Composable
fun NebAnnotatedText(
    text: AnnotatedString,
    style: TextStyle,
    modifier: Modifier = Modifier,
    inlineContent: Map<String, InlineTextContent> = emptyMap(),
    maxLines: Int = Int.MAX_VALUE,
    overflow: TextOverflow = TextOverflow.Clip,
    onTextLayout: (TextLayoutResult) -> Unit = {},
    onClick: (Int) -> Unit = {}
) {
    var layout: TextLayoutResult? = null
    Text(
        text = text,
        modifier = modifier.pointerInput(text, onClick) {
            detectTapGestures { position ->
                layout?.getOffsetForPosition(position)?.let(onClick)
            }
        },
        style = style,
        inlineContent = inlineContent,
        maxLines = maxLines,
        overflow = overflow,
        onTextLayout = {
            layout = it
            onTextLayout(it)
        }
    )
}
