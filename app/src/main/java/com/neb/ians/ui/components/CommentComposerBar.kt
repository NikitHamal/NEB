package com.neb.ians.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.expandHorizontally
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkHorizontally
import androidx.compose.animation.shrinkVertically
import androidx.compose.ui.unit.IntSize
import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.material.icons.outlined.CloseFullscreen
import androidx.compose.material.icons.outlined.Image
import androidx.compose.material.icons.outlined.MusicNote
import androidx.compose.material.icons.outlined.PictureAsPdf
import androidx.compose.material.icons.outlined.Poll
import androidx.compose.material.icons.outlined.Videocam
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.widthIn
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.DpOffset
import androidx.compose.material.icons.outlined.FormatColorText
import androidx.compose.material.icons.outlined.OpenInFull
import com.neb.ians.ui.theme.nebSpatialSpec
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.SolidColor
import com.neb.ians.ui.theme.nebEffectsSpec
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.RowScope
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ArrowUpward
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material.icons.outlined.VisibilityOff
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.screens.forum.PendingForumAttachment

/**
 * The shared comment composer used by every comment bar (forum posts, forum
 * threads, resource comments, resource threads). Attach + anonymous controls
 * sit INSIDE the field stroke via [leadingContent]; when [voiceNote] is
 * provided the trailing button morphs: empty text → mic (tap to record),
 * recording → finish, content/staged media → send.
 */
@Composable
fun NebCommentComposerBar(
    value: String,
    onValueChange: (String) -> Unit,
    placeholder: String,
    enabled: Boolean,
    canSend: Boolean,
    onSend: () -> Unit,
    modifier: Modifier = Modifier,
    posting: Boolean = false,
    sendContentDescription: String = "Send",
    sendIcon: ImageVector = Icons.Filled.ArrowUpward,
    textFieldModifier: Modifier = Modifier,
    leadingContent: (@Composable RowScope.() -> Unit)? = null,
    voiceNote: VoiceNoteRecorder? = null,
    docked: Boolean = true,
    kind: String? = null,
    onKindChange: ((String) -> Unit)? = null,
    trailingContent: (@Composable RowScope.() -> Unit)? = null,
    extraContent: @Composable () -> Unit = {}
) {
    NebCommentComposerBarFrame(
        modifier = modifier,
        enabled = enabled,
        canSend = canSend,
        posting = posting,
        onSend = onSend,
        sendContentDescription = sendContentDescription,
        sendIcon = sendIcon,
        voiceNote = voiceNote,
        docked = docked,
        kind = kind,
        onKindChange = onKindChange,
        formatBar = null,
        leadingContent = leadingContent,
        trailingContent = trailingContent,
        extraContent = extraContent
    ) { fieldModifier: Modifier, minHeight, leadingVisible ->
        ComposerInput(
            value = value,
            onValueChange = onValueChange,
            enabled = enabled,
            placeholder = placeholder,
            modifier = fieldModifier.then(textFieldModifier).defaultMinSize(minHeight = minHeight),
            leadingContent = leadingContent,
            leadingVisible = leadingVisible
        )
    }
}

@Composable
fun NebCommentComposerBar(
    value: TextFieldValue,
    onValueChange: (TextFieldValue) -> Unit,
    placeholder: String,
    enabled: Boolean,
    canSend: Boolean,
    onSend: () -> Unit,
    modifier: Modifier = Modifier,
    posting: Boolean = false,
    sendContentDescription: String = "Send",
    sendIcon: ImageVector = Icons.Filled.ArrowUpward,
    textFieldModifier: Modifier = Modifier,
    visualTransformation: VisualTransformation = VisualTransformation.None,
    leadingContent: (@Composable RowScope.() -> Unit)? = null,
    voiceNote: VoiceNoteRecorder? = null,
    docked: Boolean = true,
    kind: String? = null,
    onKindChange: ((String) -> Unit)? = null,
    trailingContent: (@Composable RowScope.() -> Unit)? = null,
    extraContent: @Composable () -> Unit = {}
) {
    NebCommentComposerBarFrame(
        modifier = modifier,
        enabled = enabled,
        canSend = canSend,
        posting = posting,
        onSend = onSend,
        sendContentDescription = sendContentDescription,
        sendIcon = sendIcon,
        voiceNote = voiceNote,
        docked = docked,
        kind = kind,
        onKindChange = onKindChange,
        formatBar = { MarkdownToolbar(value = value, onValueChange = onValueChange) },
        leadingContent = leadingContent,
        trailingContent = trailingContent,
        extraContent = extraContent
    ) { fieldModifier: Modifier, minHeight, leadingVisible ->
        ComposerInput(
            value = value,
            onValueChange = onValueChange,
            enabled = enabled,
            placeholder = placeholder,
            modifier = fieldModifier.then(textFieldModifier).defaultMinSize(minHeight = minHeight),
            visualTransformation = visualTransformation,
            leadingContent = leadingContent,
            leadingVisible = leadingVisible
        )
    }
}

@Composable
private fun NebCommentComposerBarFrame(
    modifier: Modifier,
    enabled: Boolean,
    canSend: Boolean,
    posting: Boolean,
    onSend: () -> Unit,
    sendContentDescription: String,
    sendIcon: ImageVector,
    voiceNote: VoiceNoteRecorder?,
    docked: Boolean,
    kind: String?,
    onKindChange: ((String) -> Unit)?,
    formatBar: (@Composable () -> Unit)?,
    leadingContent: (@Composable RowScope.() -> Unit)?,
    trailingContent: (@Composable RowScope.() -> Unit)?,
    extraContent: @Composable () -> Unit,
    textField: @Composable (Modifier, androidx.compose.ui.unit.Dp, Boolean) -> Unit
) {
    val recording = voiceNote?.isRecording == true
    val active = enabled && canSend && !posting

    var focused by remember { mutableStateOf(false) }
    var open by rememberSaveable { mutableStateOf(false) }
    var expanded by rememberSaveable { mutableStateOf(false) }
    var kindSheet by remember { mutableStateOf(false) }
    val scheme = MaterialTheme.colorScheme
    val stroke by animateColorAsState(
        targetValue = when {
            recording -> scheme.error.copy(alpha = 0.55f)
            focused -> scheme.primary
            else -> scheme.outlineVariant
        },
        animationSpec = nebEffectsSpec(),
        label = "composerStroke"
    )
    val shape = RoundedCornerShape(24.dp)
    val canFormat = formatBar != null
    val canKind = kind != null && onKindChange != null

    Surface(
        modifier = modifier.fillMaxWidth(),
        tonalElevation = 0.dp,
        shadowElevation = 0.dp,
        color = scheme.surface
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = if (docked) 12.dp else 16.dp, vertical = if (docked) 8.dp else 12.dp)
                .then(if (docked) Modifier.navigationBarsPadding().imePadding() else Modifier)
        ) {
            extraContent()

            // One outlined container, as on the web `neb-composer`: the stroke turns primary while anything inside
            // it has focus. Collapsed it is one row: the profile picture, the field, the tools, send. Opened by the A
            // tool it grows a row on top with the picture first and the formatting after it, the field gets the full
            // width below, and the tools and send move to a row underneath. Each part slides and fades in its place.
            val writing = open && canFormat
            val spatial = nebSpatialSpec<IntSize>()
            val effects = nebEffectsSpec<Float>()
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(shape)
                    .background(scheme.surface)
                    .border(1.dp, stroke, shape)
                    .animateContentSize(nebSpatialSpec())
                    .padding(start = 4.dp, end = 6.dp, top = 6.dp, bottom = 6.dp)
            ) {
                AnimatedVisibility(
                    visible = writing,
                    enter = expandVertically(spatial) + fadeIn(effects),
                    exit = shrinkVertically(spatial) + fadeOut(effects)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(vertical = 2.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        leadingContent?.invoke(this)
                        Row(
                            modifier = Modifier
                                .weight(1f)
                                .horizontalScroll(rememberScrollState())
                                .padding(start = 4.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) { formatBar?.invoke() }
                    }
                }
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .defaultMinSize(minHeight = 44.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    if (recording && voiceNote != null) {
                        VoiceRecordingStrip(
                            recorder = voiceNote,
                            modifier = Modifier
                                .weight(1f)
                                .padding(horizontal = 10.dp, vertical = 2.dp)
                        )
                    } else {
                        textField(
                            Modifier
                                .weight(1f)
                                .onFocusChanged { focused = it.hasFocus },
                            if (!writing) 0.dp else if (expanded) 200.dp else 72.dp,
                            !writing
                        )
                    }
                    AnimatedVisibility(
                        visible = !writing,
                        enter = fadeIn(effects) + expandHorizontally(spatial),
                        exit = fadeOut(effects) + shrinkHorizontally(spatial)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            ComposerTools(
                                formatOpen = false,
                                canFormat = canFormat,
                                onFormat = { open = true },
                                enabled = enabled,
                                kind = null,
                                onKind = null,
                                trailingContent = if (recording) null else trailingContent
                            )
                            Spacer(Modifier.width(4.dp))
                            ComposerSendButton(recording, active, posting, sendIcon, sendContentDescription) {
                                if (recording) voiceNote?.stop() else onSend()
                            }
                        }
                    }
                }
                AnimatedVisibility(
                    visible = writing,
                    enter = expandVertically(spatial) + fadeIn(effects),
                    exit = shrinkVertically(spatial) + fadeOut(effects)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(start = 4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        ComposerTools(
                            formatOpen = true,
                            canFormat = canFormat,
                            onFormat = { open = false },
                            enabled = enabled,
                            kind = if (canKind) kind else null,
                            onKind = if (canKind) ({ kindSheet = true }) else null,
                            trailingContent = trailingContent
                        )
                        Spacer(Modifier.weight(1f))
                        ComposerToolButton(
                            icon = {
                                Icon(
                                    if (expanded) Icons.Outlined.CloseFullscreen else Icons.Outlined.OpenInFull,
                                    contentDescription = if (expanded) "Shrink the field" else "Expand the field",
                                    modifier = Modifier.size(20.dp)
                                )
                            },
                            active = false,
                            enabled = enabled,
                            onClick = { expanded = !expanded }
                        )
                        Spacer(Modifier.width(4.dp))
                        ComposerSendButton(recording, active, posting, sendIcon, sendContentDescription) {
                            if (recording) voiceNote?.stop() else onSend()
                        }
                    }
                }
            }
        }
    }
    if (kindSheet && kind != null && onKindChange != null) {
        ReplyKindSheet(selected = kind, onSelect = onKindChange, onDismiss = { kindSheet = false })
    }
}

/** Tool row shared by the collapsed and the opened composer: A, the kind picker, then the call site's tools. */
@Composable
private fun RowScope.ComposerTools(
    formatOpen: Boolean,
    canFormat: Boolean,
    onFormat: () -> Unit,
    enabled: Boolean,
    kind: String?,
    onKind: (() -> Unit)?,
    trailingContent: (@Composable RowScope.() -> Unit)?
) {
    if (canFormat) {
        ComposerToolButton(
            icon = {
                Icon(
                    Icons.Outlined.FormatColorText,
                    contentDescription = if (formatOpen) "Hide formatting" else "Show formatting",
                    modifier = Modifier.size(20.dp)
                )
            },
            active = formatOpen,
            enabled = enabled,
            onClick = onFormat
        )
    }
    trailingContent?.invoke(this)
    if (kind != null && onKind != null) {
        val spec = REPLY_KINDS.firstOrNull { it.key == kind } ?: REPLY_KINDS.first()
        ComposerToolButton(
            icon = { Icon(spec.icon, contentDescription = "Reply type: ${spec.label}", modifier = Modifier.size(20.dp)) },
            active = kind != "comment",
            enabled = enabled,
            onClick = onKind
        )
    }
}

/** A 38dp tool: ghost at rest, a tonal rounded square while it is on. */
@Composable
fun ComposerToolButton(icon: @Composable () -> Unit, active: Boolean, enabled: Boolean, onClick: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    val bg by animateColorAsState(if (active) scheme.secondaryContainer else Color.Transparent, nebEffectsSpec(), label = "toolBg")
    val fg = when {
        !enabled -> scheme.onSurfaceVariant.copy(alpha = 0.4f)
        active -> scheme.onSecondaryContainer
        else -> scheme.onSurfaceVariant
    }
    Box(
        modifier = Modifier
            .size(38.dp)
            .clip(RoundedCornerShape(14.dp))
            .background(bg)
            .nebPressable(enabled = enabled, onClick = onClick),
        contentAlignment = Alignment.Center
    ) {
        androidx.compose.runtime.CompositionLocalProvider(androidx.compose.material3.LocalContentColor provides fg) { icon() }
    }
}

/** The round send button inside the stroke: tonal while there is nothing to send, brand blue once there is. */
@Composable
private fun ComposerSendButton(
    recording: Boolean,
    active: Boolean,
    posting: Boolean,
    sendIcon: ImageVector,
    description: String,
    onClick: () -> Unit
) {
    val scheme = MaterialTheme.colorScheme
    val live = recording || active
    val fill by animateColorAsState(
        targetValue = when {
            recording -> scheme.error
            active -> scheme.primary
            else -> scheme.secondaryContainer
        },
        animationSpec = nebEffectsSpec(),
        label = "sendFill"
    )
    IconButton(
        onClick = onClick,
        enabled = live,
        modifier = Modifier
            .size(40.dp)
            .background(color = fill, shape = CircleShape)
    ) {
        when {
            posting -> NebLoader(size = NebLoaderSize.Inline, color = scheme.onPrimary)
            recording -> Icon(Icons.Filled.Check, contentDescription = "Finish recording", tint = scheme.onError)
            else -> Icon(
                imageVector = sendIcon,
                contentDescription = description,
                tint = if (active) scheme.onPrimary else scheme.onSecondaryContainer
            )
        }
    }
}

/** The borderless input inside the composer container: leading tools, then the text. */
@Composable
private fun ComposerInput(
    value: String,
    onValueChange: (String) -> Unit,
    enabled: Boolean,
    placeholder: String,
    modifier: Modifier,
    leadingContent: (@Composable RowScope.() -> Unit)?,
    leadingVisible: Boolean = true
) {
    val scheme = MaterialTheme.colorScheme
    BasicTextField(
        value = value,
        onValueChange = onValueChange,
        enabled = enabled,
        maxLines = 5,
        textStyle = MaterialTheme.typography.bodyLarge.copy(color = scheme.onSurface),
        cursorBrush = SolidColor(scheme.primary),
        visualTransformation = LiveMarkdown.rememberTransformation(),
        modifier = modifier,
        decorationBox = { inner -> ComposerInputRow(value.isEmpty(), placeholder, leadingContent, leadingVisible, inner) }
    )
}

@Composable
private fun ComposerInput(
    value: TextFieldValue,
    onValueChange: (TextFieldValue) -> Unit,
    enabled: Boolean,
    placeholder: String,
    modifier: Modifier,
    visualTransformation: VisualTransformation,
    leadingContent: (@Composable RowScope.() -> Unit)?,
    leadingVisible: Boolean = true
) {
    val scheme = MaterialTheme.colorScheme
    BasicTextField(
        value = value,
        onValueChange = onValueChange,
        enabled = enabled,
        maxLines = 5,
        textStyle = MaterialTheme.typography.bodyLarge.copy(color = scheme.onSurface),
        cursorBrush = SolidColor(scheme.primary),
        visualTransformation = visualTransformation,
        modifier = modifier,
        decorationBox = { inner -> ComposerInputRow(value.text.isEmpty(), placeholder, leadingContent, leadingVisible, inner) }
    )
}

@Composable
private fun ComposerInputRow(
    empty: Boolean,
    placeholder: String,
    leadingContent: (@Composable RowScope.() -> Unit)?,
    leadingVisible: Boolean,
    inner: @Composable () -> Unit
) {
    val shown = leadingContent != null && leadingVisible
    val gap by animateDpAsState(if (shown) 4.dp else 12.dp, nebSpatialSpec(), label = "composerGap")
    Row(verticalAlignment = Alignment.CenterVertically) {
        if (leadingContent != null) {
            AnimatedVisibility(
                visible = leadingVisible,
                enter = fadeIn(nebEffectsSpec()) + expandHorizontally(nebSpatialSpec()),
                exit = fadeOut(nebEffectsSpec()) + shrinkHorizontally(nebSpatialSpec())
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) { leadingContent() }
            }
        }
        Box(
            modifier = Modifier
                .weight(1f)
                .padding(horizontal = gap, vertical = 8.dp)
        ) {
            if (empty) {
                Text(
                    text = placeholder,
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            inner()
        }
    }
}

/** The poll entry of the plus menu: whether one is being written and how to open or remove it. */
class ComposerPoll(val active: Boolean, val onToggle: () -> Unit)

private class PlusOption(val icon: ImageVector, val label: String, val active: Boolean, val onClick: () -> Unit)

/**
 * The one plus button of every comment composer. It opens a compact popup: image, PDF, audio, video and, where the
 * screen takes polls, a poll. [onPick] receives the MIME types for the system file picker. The plus turns into a
 * cross while the popup is open.
 */
@Composable
fun ComposerAttachMenu(
    enabled: Boolean,
    onPick: (Array<String>) -> Unit,
    modifier: Modifier = Modifier,
    poll: ComposerPoll? = null
) {
    var open by remember { mutableStateOf(false) }
    val turn by animateFloatAsState(if (open) 45f else 0f, nebSpatialSpec(), label = "composerPlusTurn")
    val scheme = MaterialTheme.colorScheme
    val options = buildList {
        add(PlusOption(Icons.Outlined.Image, "Image", false) { onPick(arrayOf("image/*")) })
        add(PlusOption(Icons.Outlined.PictureAsPdf, "PDF", false) { onPick(arrayOf("application/pdf")) })
        add(PlusOption(Icons.Outlined.MusicNote, "Audio", false) { onPick(arrayOf("audio/*")) })
        add(PlusOption(Icons.Outlined.Videocam, "Video", false) { onPick(arrayOf("video/*")) })
        if (poll != null) add(PlusOption(Icons.Outlined.Poll, if (poll.active) "Remove poll" else "Poll", poll.active) { poll.onToggle() })
    }
    Box(modifier) {
        val bg by animateColorAsState(if (open || poll?.active == true) scheme.secondaryContainer else Color.Transparent, nebEffectsSpec(), label = "composerPlusBg")
        Box(
            Modifier
                .size(38.dp)
                .clip(RoundedCornerShape(14.dp))
                .background(bg)
                .nebPressable(enabled = enabled, onClick = { open = true }),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                Icons.Filled.Add,
                contentDescription = "Add to your message",
                tint = if (enabled) (if (open) scheme.onSecondaryContainer else scheme.onSurfaceVariant) else scheme.onSurfaceVariant.copy(alpha = 0.4f),
                modifier = Modifier.size(22.dp).graphicsLayer { rotationZ = turn }
            )
        }
        NebDropdownMenu(
            expanded = open,
            onDismissRequest = { open = false },
            offset = DpOffset(0.dp, 6.dp)
        ) {
            options.forEach { option ->
                Row(
                    Modifier
                        .widthIn(min = 176.dp)
                        .clickable(role = Role.Button) { open = false; option.onClick() }
                        .padding(horizontal = 10.dp, vertical = 5.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Box(
                        Modifier
                            .size(34.dp)
                            .clip(RoundedCornerShape(11.dp))
                            .background(if (option.active) scheme.primary else scheme.secondaryContainer),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(option.icon, null, tint = if (option.active) scheme.onPrimary else scheme.onSecondaryContainer, modifier = Modifier.size(19.dp))
                    }
                    Text(option.label, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium, color = scheme.onSurface)
                }
            }
        }
    }
}

/**
 * Incognito-style anonymous toggle for the leading slot of [NebCommentComposerBar] —
 * filled disc + tinted icon when anonymous posting is on, outlined icon when off.
 */
@Composable
fun ComposerAnonymousButton(
    isAnonymous: Boolean,
    enabled: Boolean,
    onToggle: (Boolean) -> Unit
) {
    IconButton(
        onClick = { onToggle(!isAnonymous) },
        enabled = enabled,
        modifier = Modifier.size(38.dp)
    ) {
        Box(
            modifier = Modifier
                .size(30.dp)
                .background(
                    if (isAnonymous) MaterialTheme.colorScheme.primary
                    else MaterialTheme.colorScheme.surfaceContainer,
                    CircleShape
                ),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = if (isAnonymous) Icons.Filled.VisibilityOff else Icons.Outlined.VisibilityOff,
                contentDescription = if (isAnonymous) "Anonymous mode on" else "Anonymous mode off",
                tint = when {
                    isAnonymous -> MaterialTheme.colorScheme.onPrimary
                    enabled -> MaterialTheme.colorScheme.onSurfaceVariant
                    else -> MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.4f)
                },
                modifier = Modifier.size(17.dp)
            )
        }
    }
}

/** Pending attachment chips shown above the composer input once media is staged. */
@Composable
fun ComposerAttachmentChips(
    attachments: List<PendingForumAttachment>,
    onRemoveAttachment: (String) -> Unit
) {
    if (attachments.isEmpty()) return
    Column(modifier = Modifier
        .fillMaxWidth()
        .padding(bottom = 4.dp)) {
        attachments.forEach { attachment ->
            if (attachment.kind == "audio") {
                // Voice notes: playable preview (play/pause + waveform + times)
                PendingVoiceNoteChip(
                    attachment = attachment,
                    onRemove = onRemoveAttachment
                )
            } else {
                ForumAttachmentChip(
                    attachment = attachment,
                    onRemove = { onRemoveAttachment(attachment.localId) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 2.dp)
                )
            }
        }
    }
}
