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
    BasicTextField(
        value = value,
        onValueChange = onValueChange,
        enabled = enabled,
        singleLine = singleLine,
        minLines = minLines,
        textStyle = MaterialTheme.typography.bodyLarge.copy(color = scheme.onSurface),
        cursorBrush = SolidColor(scheme.primary),
        keyboardOptions = KeyboardOptions(keyboardType = keyboardType),
        modifier = modifier.fillMaxWidth(),
        decorationBox = { inner ->
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .background(scheme.surfaceContainerLow)
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

/** Close, who it goes out as, where it goes, and the round send button. */
@Composable
fun ComposerHeader(
    showIdentity: Boolean,
    userName: String,
    userPhotoUrl: String?,
    isAnonymous: Boolean,
    category: String,
    showCategory: Boolean,
    canPublish: Boolean,
    submitting: Boolean,
    onClose: () -> Unit,
    onIdentityClick: () -> Unit,
    onCategoryClick: () -> Unit,
    onPublish: () -> Unit,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    Column(modifier = modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 8.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            IconButton(onClick = onClose, modifier = Modifier.size(40.dp)) {
                Icon(
                    imageVector = Icons.Rounded.Close,
                    contentDescription = "Close",
                    tint = scheme.onSurfaceVariant,
                    modifier = Modifier.size(20.dp)
                )
            }

            Box(modifier = Modifier.weight(1f), contentAlignment = Alignment.CenterStart) {
                if (showIdentity) {
                    ComposerPill(
                        onClick = onIdentityClick,
                        container = scheme.surfaceContainer,
                        content = scheme.onSurface,
                        outlined = true
                    ) {
                        if (isAnonymous) {
                            Box(
                                modifier = Modifier
                                    .size(26.dp)
                                    .clip(CircleShape)
                                    .background(scheme.surfaceContainerHighest),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Rounded.VisibilityOff,
                                    contentDescription = null,
                                    tint = scheme.onSurfaceVariant,
                                    modifier = Modifier.size(15.dp)
                                )
                            }
                        } else {
                            NebAvatar(photoUrl = userPhotoUrl, name = userName, size = 26.dp, showBorder = false)
                        }
                        Text(
                            text = if (isAnonymous) "Anonymous" else userName.ifBlank { "You" },
                            style = MaterialTheme.typography.labelLarge,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f, fill = false)
                        )
                        Icon(
                            imageVector = Icons.Rounded.KeyboardArrowDown,
                            contentDescription = null,
                            modifier = Modifier.size(16.dp)
                        )
                    }
                }
            }

            if (showCategory) {
                ComposerPill(
                    onClick = onCategoryClick,
                    container = scheme.secondaryContainer,
                    content = scheme.onSecondaryContainer,
                    outlined = false,
                    modifier = Modifier.widthIn(max = 150.dp)
                ) {
                    Text(text = "#", style = MaterialTheme.typography.labelLarge)
                    Text(
                        text = category.ifBlank { "Category" },
                        style = MaterialTheme.typography.labelLarge,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.weight(1f, fill = false)
                    )
                    Icon(
                        imageVector = Icons.Rounded.KeyboardArrowDown,
                        contentDescription = null,
                        modifier = Modifier.size(16.dp)
                    )
                }
            }

            val fill by animateColorAsState(
                targetValue = if (canPublish) scheme.primary else scheme.surfaceContainerHigh,
                animationSpec = nebEffectsSpec(),
                label = "publishFill"
            )
            val ink by animateColorAsState(
                targetValue = if (canPublish) scheme.onPrimary else scheme.onSurface.copy(alpha = 0.38f),
                animationSpec = nebEffectsSpec(),
                label = "publishInk"
            )
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
                    .background(fill)
                    .nebPressable(enabled = canPublish && !submitting, onClick = onPublish),
                contentAlignment = Alignment.Center
            ) {
                if (submitting) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(18.dp),
                        strokeWidth = 2.dp,
                        color = ink
                    )
                } else {
                    Icon(
                        imageVector = Icons.AutoMirrored.Rounded.Send,
                        contentDescription = "Publish",
                        tint = ink,
                        modifier = Modifier.size(18.dp)
                    )
                }
            }
            Spacer(modifier = Modifier.width(4.dp))
        }
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(1.dp)
                .background(scheme.outlineVariant)
        )
    }
}

@Composable
private fun ComposerPill(
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

/** The markdown row, scrolling sideways, with Write and Preview pinned at its end. */
@Composable
fun ComposerFormatRow(
    state: CreatePostUiState,
    viewModel: CreatePostViewModel,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    Row(
        modifier = modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(modifier = Modifier.weight(1f)) {
            if (!state.showPreview) {
                MarkdownToolbar(
                    value = state.content,
                    onValueChange = viewModel::onContentChange,
                    modifier = Modifier.horizontalScroll(rememberScrollState())
                )
            }
        }
        Row(
            modifier = Modifier
                .clip(RoundedCornerShape(18.dp))
                .background(scheme.surfaceContainer)
                .padding(2.dp),
            horizontalArrangement = Arrangement.spacedBy(2.dp)
        ) {
            ModeButton(Icons.Rounded.Edit, "Write", selected = !state.showPreview) { viewModel.togglePreview(false) }
            ModeButton(Icons.Rounded.Visibility, "Preview", selected = state.showPreview) { viewModel.togglePreview(true) }
        }
    }
}

@Composable
private fun ModeButton(icon: ImageVector, description: String, selected: Boolean, onClick: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    val fill by animateColorAsState(
        targetValue = if (selected) scheme.surfaceContainerLowest else Color.Transparent,
        animationSpec = nebEffectsSpec(),
        label = "modeFill"
    )
    Box(
        modifier = Modifier
            .size(width = 38.dp, height = 32.dp)
            .clip(RoundedCornerShape(16.dp))
            .background(fill)
            .nebPressable(onClick = onClick),
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = icon,
            contentDescription = description,
            tint = if (selected) scheme.primary else scheme.onSurfaceVariant,
            modifier = Modifier.size(18.dp)
        )
    }
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

/** A hairline that ends in the character count. */
@Composable
fun ComposerCounterBar(count: Int, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .weight(1f)
                .height(1.dp)
                .background(MaterialTheme.colorScheme.outlineVariant)
        )
        Text(
            text = "%,d / %,d".format(count, MAX_POST_CONTENT),
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.padding(start = 10.dp)
        )
    }
}

/** Photos, video and audio, poll, document, and a picture inside the text. */
@Composable
fun ComposerFooter(
    state: CreatePostUiState,
    isEditing: Boolean,
    insertImageEnabled: Boolean,
    onPhotos: () -> Unit,
    onMedia: () -> Unit,
    onDocument: () -> Unit,
    onPoll: () -> Unit,
    onInlineImage: () -> Unit,
    modifier: Modifier = Modifier
) {
    val enabled = !state.isSubmitting
    Row(
        modifier = modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState())
            .padding(horizontal = 8.dp, vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(2.dp)
    ) {
        FooterTool(Icons.Rounded.AddPhotoAlternate, "Attach photos", enabled, false, onPhotos)
        if (!isEditing) {
            FooterTool(Icons.Rounded.Videocam, "Add video or audio", enabled, state.mediaAttachments.isNotEmpty(), onMedia)
            FooterTool(Icons.Rounded.Poll, "Ask a poll or quiz", enabled, state.pollEnabled, onPoll)
            FooterTool(Icons.AutoMirrored.Rounded.MenuBook, "Share a PDF or study notes", enabled, false, onDocument)
        }
        Box(
            modifier = Modifier
                .padding(horizontal = 6.dp)
                .width(1.dp)
                .height(20.dp)
                .background(MaterialTheme.colorScheme.outlineVariant)
        )
        FooterTool(Icons.Rounded.Image, "Insert picture in text", enabled && insertImageEnabled, false, onInlineImage)
    }
}

@Composable
private fun FooterTool(icon: ImageVector, description: String, enabled: Boolean, active: Boolean, onClick: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    val fill by animateColorAsState(
        targetValue = if (active) scheme.secondaryContainer else Color.Transparent,
        animationSpec = nebEffectsSpec(),
        label = "toolFill"
    )
    IconButton(
        onClick = onClick,
        enabled = enabled,
        modifier = Modifier
            .size(44.dp)
            .clip(CircleShape)
            .background(fill)
    ) {
        Icon(
            imageVector = icon,
            contentDescription = description,
            tint = if (active) scheme.onSecondaryContainer else scheme.onSurfaceVariant,
            modifier = Modifier.size(22.dp)
        )
    }
}
