@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.forum

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.Send
import androidx.compose.material.icons.rounded.AddPhotoAlternate
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.Edit
import androidx.compose.material.icons.rounded.Image
import androidx.compose.material.icons.rounded.KeyboardArrowDown
import androidx.compose.material.icons.automirrored.rounded.MenuBook
import androidx.compose.material.icons.rounded.Poll
import androidx.compose.material.icons.rounded.Videocam
import androidx.compose.material.icons.rounded.Visibility
import androidx.compose.material.icons.rounded.VisibilityOff
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.neb.ians.ui.components.ForumAttachmentChip
import com.neb.ians.ui.components.InlineImageField
import com.neb.ians.ui.components.InlineImageFieldHandle
import com.neb.ians.ui.components.MarkdownText
import com.neb.ians.ui.components.MarkdownToolbar
import com.neb.ians.ui.components.MentionSuggestions
import com.neb.ians.ui.components.NebAvatar
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.components.resolveMediaUrl
import com.neb.ians.ui.theme.nebEffectsSpec

/*
 * The composer, laid out the way the web dialog is on a phone:
 *
 *   header   close, identity pill, category pill, round publish button
 *   pinned   borderless title, formatting row with the Write / Preview toggle
 *   body     the writing area, then poll, pictures and attachments as they are added
 *   counter  a hairline and the character count
 *   footer   photos, video and audio, poll, document, picture inside the text
 *
 * One white sheet and one hairline. Nothing here is lifted, nothing is boxed twice.
 */

/** The container the poll builder uses: a fill and a hairline, no shadow. */
@Composable
fun PostPanel(
    modifier: Modifier = Modifier,
    padding: Int = 14,
    content: @Composable androidx.compose.foundation.layout.ColumnScope.() -> Unit
) {
    val shape = RoundedCornerShape(24.dp)
    Column(
        modifier = modifier
            .fillMaxWidth()
            .clip(shape)
            .background(MaterialTheme.colorScheme.surfaceContainerLowest)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, shape)
            .padding(padding.dp),
        content = content
    )
}

/** A rounded single-line field on a tonal fill, used by the poll builder. */
@Composable
fun PostInput(
    value: String,
    onValueChange: (String) -> Unit,
    placeholder: String,
    modifier: Modifier = Modifier,
    singleLine: Boolean = true,
    minLines: Int = 1,
    enabled: Boolean = true,
    keyboardType: KeyboardType = KeyboardType.Text
) {
    val scheme = MaterialTheme.colorScheme
    var focused by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }
    // One white field, one 1.5dp stroke; only the stroke colour changes on focus (web .md-input).
    val stroke by animateColorAsState(
        targetValue = if (focused) scheme.primary else scheme.outline.copy(alpha = 0.58f),
        animationSpec = nebEffectsSpec(),
        label = "postInputStroke"
    )
    val fieldShape = RoundedCornerShape(18.dp)
    BasicTextField(
        value = value,
        onValueChange = onValueChange,
        enabled = enabled,
        singleLine = singleLine,
        minLines = minLines,
        textStyle = MaterialTheme.typography.bodyLarge.copy(color = scheme.onSurface),
        cursorBrush = SolidColor(scheme.primary),
        keyboardOptions = KeyboardOptions(keyboardType = keyboardType),
        modifier = modifier
            .fillMaxWidth()
            .onFocusEdge { focused = it },
        decorationBox = { inner ->
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(fieldShape)
                    .background(scheme.surfaceContainerLowest)
                    .border(1.5.dp, stroke, fieldShape)
                    .padding(horizontal = 14.dp, vertical = 12.dp)
            ) {
                if (value.isEmpty()) {
                    Text(
                        text = placeholder,
                        style = MaterialTheme.typography.bodyLarge,
                        color = scheme.onSurfaceVariant,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                inner()
            }
        }
    )
}

@Composable
internal fun ComposerPill(
    onClick: () -> Unit,
    container: Color,
    content: Color,
    outlined: Boolean,
    modifier: Modifier = Modifier,
    body: @Composable androidx.compose.foundation.layout.RowScope.() -> Unit
) {
    val shape = RoundedCornerShape(18.dp)
    Row(
        modifier = modifier
            .heightIn(min = 36.dp)
            .clip(shape)
            .background(container)
            .then(
                if (outlined) Modifier.border(1.dp, MaterialTheme.colorScheme.outlineVariant, shape)
                else Modifier
            )
            .nebPressable(onClick = onClick)
            .padding(horizontal = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        androidx.compose.runtime.CompositionLocalProvider(
            androidx.compose.material3.LocalContentColor provides content
        ) { body() }
    }
}

/** Borderless title, the first thing on the page. */
@Composable
fun ComposerTitleField(
    value: String,
    onValueChange: (String) -> Unit,
    enabled: Boolean,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    BasicTextField(
        value = value,
        onValueChange = onValueChange,
        enabled = enabled,
        singleLine = true,
        textStyle = MaterialTheme.typography.titleLargeEmphasized.copy(color = scheme.onSurface),
        cursorBrush = SolidColor(scheme.primary),
        modifier = modifier.fillMaxWidth(),
        decorationBox = { inner ->
            Box(modifier = Modifier.padding(vertical = 10.dp)) {
                if (value.isEmpty()) {
                    Text(
                        text = "Title (optional)",
                        style = MaterialTheme.typography.titleLargeEmphasized,
                        color = scheme.onSurfaceVariant.copy(alpha = 0.7f)
                    )
                }
                inner()
            }
        }
    )
}

/** The writing area, or what it will look like once posted. No frame of its own. */
@Composable
fun ComposerEditor(
    state: CreatePostUiState,
    viewModel: CreatePostViewModel,
    handle: InlineImageFieldHandle,
    onPendingCountChange: (Int) -> Unit,
    onImageClick: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxWidth()) {
        if (state.showPreview) {
            Box(modifier = Modifier.heightIn(min = 200.dp)) {
                if (state.content.text.isBlank()) {
                    Text(
                        text = "Nothing to preview yet.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                } else {
                    MarkdownText(markdown = state.content.text, onInlineImageClick = onImageClick)
                }
            }
        } else {
            InlineImageField(
                value = state.content,
                onValueChange = viewModel::onContentChange,
                uploader = viewModel::uploadInlineImage,
                onError = viewModel::reportError,
                handle = handle,
                placeholder = "Ask a question, share notes, formulas, or exam tips...",
                textStyle = MaterialTheme.typography.bodyLarge,
                minLines = 8,
                maxLines = 60,
                enabled = !state.isSubmitting,
                onPendingCountChange = onPendingCountChange,
                onImageClick = onImageClick
            )
            MentionSuggestions(
                users = state.mentionSuggestions,
                onSelect = viewModel::selectMention
            )
        }
    }
}

/** The pictures that ride along with the post, as the pictures themselves. */
@Composable
fun ComposerImageStrip(
    state: CreatePostUiState,
    viewModel: CreatePostViewModel,
    modifier: Modifier = Modifier
) {
    if (state.activeImageCount == 0) return
    Row(
        modifier = modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState()),
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        state.visibleExistingImages.forEach { image ->
            ImageTile(
                model = resolveMediaUrl(image.imageUrl),
                onRemove = { viewModel.removeExistingImage(image.id) }
            )
        }
        state.images.forEach { uri ->
            ImageTile(model = uri, onRemove = { viewModel.removeImage(uri) })
        }
    }
}

@Composable
private fun ImageTile(model: Any?, onRemove: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    Box(modifier = Modifier.size(96.dp)) {
        AsyncImage(
            model = model,
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .size(96.dp)
                .clip(RoundedCornerShape(20.dp))
                .background(scheme.surfaceContainerHigh)
        )
        Box(
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(6.dp)
                .size(26.dp)
                .clip(CircleShape)
                .background(scheme.surfaceContainerLowest)
                .nebPressable(onClick = onRemove),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Rounded.Close,
                contentDescription = "Remove image",
                tint = scheme.onSurface,
                modifier = Modifier.size(14.dp)
            )
        }
    }
}

/** Video, audio and documents that were picked, one line each. */
@Composable
fun ComposerAttachmentList(
    state: CreatePostUiState,
    viewModel: CreatePostViewModel,
    modifier: Modifier = Modifier
) {
    if (state.mediaAttachments.isEmpty()) return
    Column(modifier = modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        state.mediaAttachments.forEach { attachment ->
            ForumAttachmentChip(
                attachment = attachment,
                onRemove = { viewModel.removeMediaAttachment(attachment.localId) },
                modifier = Modifier.fillMaxWidth()
            )
        }
    }
}

private fun Modifier.onFocusEdge(onChange: (Boolean) -> Unit): Modifier =
    this.onFocusChanged { onChange(it.isFocused) }
