@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.forum

import androidx.annotation.DrawableRes
import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.offset
import androidx.compose.runtime.remember
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.MarkdownToolbar
import com.neb.ians.ui.components.NebIcon
import com.neb.ians.ui.components.NebIcons
import com.neb.ians.ui.components.NebIdentityPicker
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.nebEffectsSpec

/*
 * The composer chrome, drawn with the website's own icon set:
 *
 *   header   close, identity dropdown, #category pill, round publish arrow
 *   format   markdown row (scrolls sideways), picture-in-text, Write / Preview
 *   footer   photos, video, poll, book, and the character count at the far end
 */

/** Who it goes out as, where it goes, and the round publish button. */
@Composable
fun ComposerHeader(
    showIdentity: Boolean,
    userName: String,
    userHandle: String,
    userPhotoUrl: String?,
    anonTag: String,
    isAnonymous: Boolean,
    category: String,
    canPublish: Boolean,
    submitting: Boolean,
    onClose: () -> Unit,
    onIdentitySelect: (anonymous: Boolean) -> Unit,
    onCategoryClick: () -> Unit,
    onPublish: () -> Unit,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    Column(modifier = modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 8.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            ChromeButton(NebIcons.Close, "Close", onClick = onClose)

            if (showIdentity) {
                NebIdentityPicker(
                    isAnonymous = isAnonymous,
                    userName = userName,
                    handle = userHandle,
                    photoUrl = userPhotoUrl,
                    anonTag = anonTag,
                    onSelect = onIdentitySelect,
                    enabled = !submitting,
                    modifier = Modifier.weight(1f, fill = false)
                )
            }

            Spacer(modifier = Modifier.weight(1f))

            ComposerPill(
                onClick = onCategoryClick,
                container = scheme.secondaryContainer,
                content = scheme.onSecondaryContainer,
                outlined = false,
                modifier = Modifier.widthIn(max = 124.dp)
            ) {
                Text(
                    text = "#" + category.ifBlank { "Category" },
                    style = MaterialTheme.typography.labelLarge,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f, fill = false)
                )
                NebIcon(NebIcons.ChevronDown, null, size = 14.dp)
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
                    .nebPressable(enabled = canPublish && !submitting, onClick = onPublish)
                    .semantics {
                        role = Role.Button
                        contentDescription = "Publish"
                    },
                contentAlignment = Alignment.Center
            ) {
                if (submitting) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(18.dp),
                        strokeWidth = 2.dp,
                        color = ink
                    )
                } else {
                    NebIcon(NebIcons.Send, null, size = 20.dp, tint = ink)
                }
            }
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
private fun ChromeButton(@DrawableRes icon: Int, description: String, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .size(40.dp)
            .clip(CircleShape)
            .nebPressable(onClick = onClick)
            .semantics {
                role = Role.Button
                contentDescription = description
            },
        contentAlignment = Alignment.Center
    ) {
        NebIcon(icon, null, size = 20.dp, tint = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

/** The markdown row, scrolling sideways, with Write and Preview pinned at its end. */
@Composable
fun ComposerFormatRow(
    state: CreatePostUiState,
    viewModel: CreatePostViewModel,
    insertImageEnabled: Boolean,
    onInlineImage: () -> Unit,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    var open by androidx.compose.runtime.saveable.rememberSaveable { androidx.compose.runtime.mutableStateOf(true) }
    val showTools = open && !state.showPreview
    Row(
        modifier = modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (!state.showPreview) {
            // Hide the formatting row to write on a clean page; the same button brings it back.
            Box(
                modifier = Modifier
                    .size(36.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .background(if (open) androidx.compose.ui.graphics.Color.Transparent else scheme.primaryContainer)
                    .nebPressable(scale = 0.88f, onClick = { open = !open })
                    .semantics {
                        role = Role.Button
                        contentDescription = if (open) "Hide formatting" else "Show formatting"
                    },
                contentAlignment = Alignment.Center
            ) {
                androidx.compose.material3.Icon(
                    if (open) androidx.compose.material.icons.Icons.Outlined.ChevronLeft else androidx.compose.material.icons.Icons.Outlined.FormatSize,
                    null,
                    modifier = Modifier.size(20.dp),
                    tint = if (open) scheme.onSurfaceVariant else scheme.onPrimaryContainer
                )
            }
        }
        Box(modifier = Modifier.weight(1f)) {
            androidx.compose.animation.AnimatedVisibility(
                visible = showTools,
                enter = androidx.compose.animation.expandHorizontally() + androidx.compose.animation.fadeIn(),
                exit = androidx.compose.animation.shrinkHorizontally() + androidx.compose.animation.fadeOut()
            ) {
                Row(
                    modifier = Modifier.horizontalScroll(rememberScrollState()),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    MarkdownToolbar(state = viewModel.editor)
                    FormatTool(
                        icon = NebIcons.Image,
                        description = "Insert picture in text",
                        enabled = insertImageEnabled && !state.isSubmitting,
                        onClick = onInlineImage
                    )
                }
            }
        }
        ModeSwitch(preview = state.showPreview, onChange = viewModel::togglePreview, modifier = Modifier.padding(start = 8.dp))
    }
}

@Composable
private fun FormatTool(@DrawableRes icon: Int, description: String, enabled: Boolean, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .size(36.dp)
            .clip(RoundedCornerShape(12.dp))
            .nebPressable(enabled = enabled, scale = 0.88f, onClick = onClick)
            .semantics {
                role = Role.Button
                contentDescription = description
            },
        contentAlignment = Alignment.Center
    ) {
        NebIcon(
            icon, null, size = 19.dp,
            tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = if (enabled) 1f else 0.38f)
        )
    }
}

/** Write / Preview: one thumb slides between the two; neither icon takes a press or ripple of its own. */
@Composable
private fun ModeSwitch(preview: Boolean, onChange: (Boolean) -> Unit, modifier: Modifier = Modifier) {
    val scheme = MaterialTheme.colorScheme
    val slot = 38.dp
    val thumb by androidx.compose.animation.core.animateDpAsState(
        targetValue = if (preview) slot else 0.dp,
        animationSpec = androidx.compose.animation.core.spring(dampingRatio = 0.8f, stiffness = 700f),
        label = "modeThumb"
    )
    Box(
        modifier = modifier
            .clip(RoundedCornerShape(18.dp))
            .background(scheme.surfaceContainerLow)
            .padding(2.dp)
    ) {
        Box(
            modifier = Modifier
                .offset(x = thumb)
                .size(width = slot, height = 32.dp)
                .clip(RoundedCornerShape(16.dp))
                .background(scheme.surface)
        )
        Row {
            ModeIcon(NebIcons.Pen, "Write", selected = !preview, slot = slot) { onChange(false) }
            ModeIcon(NebIcons.Eye, "Preview", selected = preview, slot = slot) { onChange(true) }
        }
    }
}

@Composable
private fun ModeIcon(@DrawableRes icon: Int, description: String, selected: Boolean, slot: androidx.compose.ui.unit.Dp, onClick: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    val tint by animateColorAsState(
        targetValue = if (selected) scheme.primary else scheme.onSurfaceVariant,
        animationSpec = nebEffectsSpec(),
        label = "modeTint"
    )
    Box(
        modifier = Modifier
            .size(width = slot, height = 32.dp)
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                role = Role.Tab,
                onClick = { if (!selected) onClick() }
            )
            .semantics { contentDescription = description },
        contentAlignment = Alignment.Center
    ) {
        NebIcon(icon, null, size = 18.dp, tint = tint)
    }
}
/** Photos, video and audio, poll, book: the web footer, with the character count at its end. */
@Composable
fun ComposerFooter(
    state: CreatePostUiState,
    isEditing: Boolean,
    onPhotos: () -> Unit,
    onMedia: () -> Unit,
    onDocument: () -> Unit,
    onPoll: () -> Unit,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    val enabled = !state.isSubmitting
    Column(modifier = modifier.fillMaxWidth()) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(1.dp)
                .background(scheme.outlineVariant)
        )
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 8.dp, vertical = 4.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(2.dp)
        ) {
            FooterTool(NebIcons.Image, "Attach photos", enabled, state.activeImageCount > 0, onPhotos)
            if (!isEditing) {
                FooterTool(NebIcons.Video, "Add video or audio", enabled, state.mediaAttachments.isNotEmpty(), onMedia)
                FooterTool(NebIcons.Poll, "Ask a poll or quiz", enabled, state.pollEnabled, onPoll)
                FooterTool(NebIcons.Book, "Share a PDF or study notes", enabled, false, onDocument)
            }
            Spacer(modifier = Modifier.weight(1f))
            Text(
                text = "%,d / %,d".format(state.content.text.length, MAX_POST_CONTENT),
                style = MaterialTheme.typography.labelSmall,
                color = scheme.onSurfaceVariant,
                modifier = Modifier.padding(end = 8.dp)
            )
        }
    }
}

@Composable
private fun FooterTool(
    @DrawableRes icon: Int,
    description: String,
    enabled: Boolean,
    active: Boolean,
    onClick: () -> Unit
) {
    val scheme = MaterialTheme.colorScheme
    val fill by animateColorAsState(
        targetValue = if (active) scheme.secondaryContainer else Color.Transparent,
        animationSpec = nebEffectsSpec(),
        label = "toolFill"
    )
    Box(
        modifier = Modifier
            .size(44.dp)
            .clip(RoundedCornerShape(16.dp))
            .background(fill)
            .nebPressable(enabled = enabled, onClick = onClick)
            .semantics {
                role = Role.Button
                contentDescription = description
            },
        contentAlignment = Alignment.Center
    ) {
        NebIcon(
            icon, null, size = 22.dp,
            tint = (if (active) scheme.onSecondaryContainer else scheme.onSurfaceVariant)
                .copy(alpha = if (enabled) 1f else 0.38f)
        )
    }
}
