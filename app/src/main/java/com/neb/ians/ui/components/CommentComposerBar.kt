package com.neb.ians.ui.components

import androidx.compose.animation.animateColorAsState
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
        trailingContent = trailingContent,
        extraContent = extraContent
    ) { fieldModifier: Modifier ->
        ComposerInput(
            value = value,
            onValueChange = onValueChange,
            enabled = enabled,
            placeholder = placeholder,
            modifier = fieldModifier.then(textFieldModifier),
            leadingContent = leadingContent
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
        trailingContent = trailingContent,
        extraContent = extraContent
    ) { fieldModifier: Modifier ->
        ComposerInput(
            value = value,
            onValueChange = onValueChange,
            enabled = enabled,
            placeholder = placeholder,
            modifier = fieldModifier.then(textFieldModifier),
            visualTransformation = visualTransformation,
            leadingContent = leadingContent
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
    trailingContent: (@Composable RowScope.() -> Unit)?,
    extraContent: @Composable () -> Unit,
    textField: @Composable (Modifier) -> Unit
) {
    val recording = voiceNote?.isRecording == true
    val active = enabled && canSend && !posting
    // Mic shows only when there's nothing to send yet (empty text, no staged
    // attachment — canSend already accounts for those at call sites).
    val showMic = !recording && !active && !posting && voiceNote != null && enabled

    var focused by remember { mutableStateOf(false) }
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
    val shape = RoundedCornerShape(28.dp)

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

            // One container, as on the web: the stroke turns primary while anything inside
            // it has focus, and the send button lives inside the same outline.
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .defaultMinSize(minHeight = 52.dp)
                    .clip(shape)
                    .background(scheme.surfaceContainerLowest)
                    .border(1.dp, stroke, shape)
                    .padding(start = 4.dp, end = 6.dp, top = 6.dp, bottom = 6.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.Start
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
                            .onFocusChanged { focused = it.hasFocus }
                    )
                }
                if (trailingContent != null && !recording) trailingContent()
                Spacer(modifier = Modifier.width(6.dp))

                val trailingActive = recording || active || showMic
                val trailingColor by animateColorAsState(
                    targetValue = when {
                        recording -> scheme.error
                        active || showMic -> scheme.primary
                        else -> scheme.secondaryContainer
                    },
                    animationSpec = nebEffectsSpec(),
                    label = "sendFill"
                )
                IconButton(
                    onClick = {
                        when {
                            recording -> voiceNote?.stop()
                            showMic -> voiceNote?.micClick?.invoke()
                            else -> onSend()
                        }
                    },
                    enabled = trailingActive,
                    modifier = Modifier
                        .size(40.dp)
                        .background(color = trailingColor, shape = CircleShape)
                ) {
                    when {
                        posting -> NebLoader(size = NebLoaderSize.Inline, color = scheme.onPrimary)
                        recording -> Icon(
                            imageVector = Icons.Filled.Check,
                            contentDescription = "Finish recording",
                            tint = scheme.onError
                        )
                        showMic -> Icon(
                            imageVector = Icons.Filled.Mic,
                            contentDescription = "Record a voice note",
                            tint = scheme.onPrimary
                        )
                        else -> Icon(
                            imageVector = sendIcon,
                            contentDescription = sendContentDescription,
                            tint = if (active) scheme.onPrimary
                            else scheme.onSecondaryContainer
                        )
                    }
                }
            }
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
    leadingContent: (@Composable RowScope.() -> Unit)?
) {
    val scheme = MaterialTheme.colorScheme
    BasicTextField(
        value = value,
        onValueChange = onValueChange,
        enabled = enabled,
        maxLines = 5,
        textStyle = MaterialTheme.typography.bodyLarge.copy(color = scheme.onSurface),
        cursorBrush = SolidColor(scheme.primary),
        modifier = modifier,
        decorationBox = { inner -> ComposerInputRow(value.isEmpty(), placeholder, leadingContent, inner) }
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
    leadingContent: (@Composable RowScope.() -> Unit)?
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
        decorationBox = { inner -> ComposerInputRow(value.text.isEmpty(), placeholder, leadingContent, inner) }
    )
}

@Composable
private fun ComposerInputRow(
    empty: Boolean,
    placeholder: String,
    leadingContent: (@Composable RowScope.() -> Unit)?,
    inner: @Composable () -> Unit
) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        if (leadingContent != null) leadingContent()
        Box(
            modifier = Modifier
                .weight(1f)
                .padding(horizontal = if (leadingContent != null) 4.dp else 12.dp, vertical = 8.dp)
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

/** The web's paperclip, in the composer's tool slot (inside the stroke). */
@Composable
fun ComposerAttachButton(enabled: Boolean, onClick: () -> Unit) {
    IconButton(
        onClick = onClick,
        enabled = enabled,
        modifier = Modifier.size(38.dp)
    ) {
        NebIcon(
            NebIcons.Attach,
            "Attach media",
            size = 20.dp,
            tint = if (enabled) MaterialTheme.colorScheme.onSurfaceVariant
            else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.4f)
        )
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
