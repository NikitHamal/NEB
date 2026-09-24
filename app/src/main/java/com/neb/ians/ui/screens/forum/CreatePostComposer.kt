@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.forum

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.AddPhotoAlternate
import androidx.compose.material.icons.rounded.AttachFile
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.VisibilityOff
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
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
import com.neb.ians.ui.components.NebRailTab
import com.neb.ians.ui.components.NebTabRail
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.components.resolveMediaUrl

/**
 * The one container the composer uses.
 *
 * A hairline and a fill, no shadow. Everything on this screen is a group of
 * fields rather than a card that floats, so nothing here needs to look lifted.
 */
@Composable
fun PostPanel(
    modifier: Modifier = Modifier,
    padding: Int = 14,
    content: @Composable ColumnScope.() -> Unit
) {
    val shape = RoundedCornerShape(24.dp)
    Column(
        modifier = modifier
            .fillMaxWidth()
            .clip(shape)
            .background(MaterialTheme.colorScheme.surfaceContainerLow)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, shape)
            .padding(padding.dp),
        content = content
    )
}

/** The one text field shape the composer uses. */
@Composable
fun PostTextField(
    value: String,
    onValueChange: (String) -> Unit,
    label: String,
    modifier: Modifier = Modifier,
    placeholder: String? = null,
    singleLine: Boolean = true,
    minLines: Int = 1,
    keyboardType: KeyboardType = KeyboardType.Text,
    supporting: String? = null,
    enabled: Boolean = true
) {
    OutlinedTextField(
        value = value,
        onValueChange = onValueChange,
        label = { Text(label, maxLines = 1, overflow = TextOverflow.Ellipsis) },
        placeholder = placeholder?.let { { Text(it, maxLines = 1, overflow = TextOverflow.Ellipsis) } },
        supportingText = supporting?.let { { Text(it) } },
        singleLine = singleLine,
        minLines = minLines,
        enabled = enabled,
        keyboardOptions = KeyboardOptions(keyboardType = keyboardType),
        shape = RoundedCornerShape(16.dp),
        textStyle = MaterialTheme.typography.bodyLarge,
        colors = OutlinedTextFieldDefaults.colors(
            focusedContainerColor = MaterialTheme.colorScheme.surfaceContainerLow,
            unfocusedContainerColor = MaterialTheme.colorScheme.surfaceContainerLow,
            unfocusedBorderColor = MaterialTheme.colorScheme.outlineVariant
        ),
        modifier = modifier.fillMaxWidth()
    )
}

/** Icon, title, a line of explanation, and the switch it belongs to. */
@Composable
fun PostSwitchRow(
    icon: ImageVector,
    title: String,
    subtitle: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true
) {
    Row(
        modifier = modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Box(
            modifier = Modifier
                .size(38.dp)
                .clip(RoundedCornerShape(13.dp))
                .background(MaterialTheme.colorScheme.surfaceContainerHighest),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onSurface,
                modifier = Modifier.size(18.dp)
            )
        }
        Column(modifier = Modifier.weight(1f)) {
            Text(text = title, style = MaterialTheme.typography.bodyLarge)
            Text(
                text = subtitle,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        Switch(checked = checked, onCheckedChange = onCheckedChange, enabled = enabled)
    }
}

/**
 * Write and Preview, as the same piece of paper seen two ways.
 *
 * The toolbar sits above the text and the counter below it, so the typing area
 * itself stays empty of decoration.
 */
@Composable
fun PostEditorPanel(
    state: CreatePostUiState,
    viewModel: CreatePostViewModel,
    handle: InlineImageFieldHandle,
    pendingInlineCount: Int,
    onPendingCountChange: (Int) -> Unit,
    onImageClick: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(8.dp)) {
        NebTabRail(
            tabs = listOf(NebRailTab("Write"), NebRailTab("Preview")),
            selectedIndex = if (state.showPreview) 1 else 0,
            onSelect = { viewModel.togglePreview(it == 1) },
            contentPadding = PaddingValues(0.dp)
        )

        PostPanel {
            if (state.showPreview) {
                Box(modifier = Modifier.heightIn(min = 160.dp)) {
                    if (state.content.text.isBlank()) {
                        Text(
                            text = "Nothing to preview yet.",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    } else {
                        MarkdownText(
                            markdown = state.content.text,
                            onInlineImageClick = onImageClick
                        )
                    }
                }
            } else {
                MarkdownToolbar(
                    value = state.content,
                    onValueChange = viewModel::onContentChange,
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState())
                )
                Spacer(modifier = Modifier.height(6.dp))
                InlineImageField(
                    value = state.content,
                    onValueChange = viewModel::onContentChange,
                    uploader = viewModel::uploadInlineImage,
                    onError = viewModel::reportError,
                    handle = handle,
                    placeholder = "Say what you want to ask or share. Type @ to mention a Nebian.",
                    textStyle = MaterialTheme.typography.bodyLarge,
                    minLines = 6,
                    maxLines = 16,
                    enabled = !state.isSubmitting,
                    onPendingCountChange = onPendingCountChange,
                    onImageClick = onImageClick
                )
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    IconButton(
                        onClick = { handle.pickImage() },
                        enabled = !state.isSubmitting && pendingInlineCount == 0,
                        modifier = Modifier.size(32.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Rounded.AddPhotoAlternate,
                            contentDescription = "Insert image in text",
                            tint = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.size(19.dp)
                        )
                    }
                    Spacer(modifier = Modifier.weight(1f))
                    Text(
                        text = "${state.content.text.length}/$MAX_POST_CONTENT",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }

        if (!state.showPreview) {
            MentionSuggestions(
                users = state.mentionSuggestions,
                onSelect = viewModel::selectMention
            )
        }
    }
}

/** The pictures that ride along with the post, as a row of the pictures themselves. */
@Composable
fun PostImagesPanel(
    state: CreatePostUiState,
    viewModel: CreatePostViewModel,
    onAddImages: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(
                text = "Images",
                style = MaterialTheme.typography.labelMediumEmphasized,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.weight(1f)
            )
            Text(
                text = "${state.activeImageCount} of $MAX_POST_IMAGES",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            state.visibleExistingImages.forEach { image ->
                PostImageTile(
                    model = resolveMediaUrl(image.imageUrl),
                    onRemove = { viewModel.removeExistingImage(image.id) }
                )
            }
            state.images.forEach { uri ->
                PostImageTile(model = uri, onRemove = { viewModel.removeImage(uri) })
            }
            if (state.activeImageCount < MAX_POST_IMAGES) {
                Column(
                    modifier = Modifier
                        .nebPressable(enabled = !state.isSubmitting, onClick = onAddImages)
                        .size(88.dp)
                        .clip(RoundedCornerShape(20.dp))
                        .background(MaterialTheme.colorScheme.surfaceContainerHigh),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    Icon(
                        imageVector = Icons.Rounded.AddPhotoAlternate,
                        contentDescription = "Add image",
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(20.dp)
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = "Add",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}

@Composable
private fun PostImageTile(model: Any?, onRemove: () -> Unit) {
    Box(modifier = Modifier.size(88.dp)) {
        AsyncImage(
            model = model,
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .size(88.dp)
                .clip(RoundedCornerShape(20.dp))
                .background(MaterialTheme.colorScheme.surfaceContainerHigh)
        )
        Box(
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(6.dp)
                .nebPressable(onClick = onRemove)
                .size(24.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.surface),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Rounded.Close,
                contentDescription = "Remove image",
                tint = MaterialTheme.colorScheme.onSurface,
                modifier = Modifier.size(14.dp)
            )
        }
    }
}

/** Video, audio and files — one tappable line, then whatever was picked. */
@Composable
fun PostAttachmentsPanel(
    state: CreatePostUiState,
    viewModel: CreatePostViewModel,
    onPick: () -> Unit,
    modifier: Modifier = Modifier
) {
    PostPanel(modifier = modifier) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .nebPressable(enabled = !state.isSubmitting, onClick = onPick)
                .clip(RoundedCornerShape(16.dp))
                .padding(vertical = 2.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(38.dp)
                    .clip(RoundedCornerShape(13.dp))
                    .background(MaterialTheme.colorScheme.surfaceContainerHighest),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Rounded.AttachFile,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onSurface,
                    modifier = Modifier.size(18.dp)
                )
            }
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = "Attach video, audio or files",
                    style = MaterialTheme.typography.bodyLarge
                )
                Text(
                    text = "Up to ${ForumMediaUploadHelper.MAX_ATTACHMENTS} files, " +
                        "150 MB a video and 40 MB an audio",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
        if (state.mediaAttachments.isNotEmpty()) {
            Spacer(modifier = Modifier.height(10.dp))
            state.mediaAttachments.forEach { attachment ->
                ForumAttachmentChip(
                    attachment = attachment,
                    onRemove = { viewModel.removeMediaAttachment(attachment.localId) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 3.dp)
                )
            }
        }
    }
}

/** Posting without a name attached. */
@Composable
fun PostAnonymousPanel(
    state: CreatePostUiState,
    viewModel: CreatePostViewModel,
    modifier: Modifier = Modifier
) {
    PostPanel(modifier = modifier) {
        PostSwitchRow(
            icon = Icons.Rounded.VisibilityOff,
            title = "Post anonymously",
            subtitle = "Nebians see Anonymous Nebian instead of your name",
            checked = state.isAnonymous,
            onCheckedChange = viewModel::setAnonymous,
            enabled = !state.isSubmitting
        )
    }
}
