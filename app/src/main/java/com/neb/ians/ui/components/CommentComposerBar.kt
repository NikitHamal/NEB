package com.neb.ians.ui.components

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
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
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
        extraContent = extraContent
    ) { fieldModifier: Modifier ->
        OutlinedTextField(
            value = value,
            onValueChange = onValueChange,
            enabled = enabled,
            placeholder = { Text(placeholder, style = MaterialTheme.typography.bodyMedium) },
            modifier = fieldModifier.then(textFieldModifier),
            maxLines = 4,
            textStyle = MaterialTheme.typography.bodyMedium,
            shape = RoundedCornerShape(24.dp),
            colors = NebCommentTextFieldColors(),
            leadingIcon = if (leadingContent != null) {
                {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Start
                    ) { leadingContent() }
                }
            } else null
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
        extraContent = extraContent
    ) { fieldModifier: Modifier ->
        OutlinedTextField(
            value = value,
            onValueChange = onValueChange,
            enabled = enabled,
            placeholder = { Text(placeholder, style = MaterialTheme.typography.bodyMedium) },
            modifier = fieldModifier.then(textFieldModifier),
            maxLines = 4,
            textStyle = MaterialTheme.typography.bodyMedium,
            shape = RoundedCornerShape(24.dp),
            colors = NebCommentTextFieldColors(),
            visualTransformation = visualTransformation,
            leadingIcon = if (leadingContent != null) {
                {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Start
                    ) { leadingContent() }
                }
            } else null
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
    extraContent: @Composable () -> Unit,
    textField: @Composable (Modifier) -> Unit
) {
    val recording = voiceNote?.isRecording == true
    val active = enabled && canSend && !posting
    // Mic shows only when there's nothing to send yet (empty text, no staged
    // attachment — canSend already accounts for those at call sites).
    val showMic = !recording && !active && !posting && voiceNote != null && enabled

    Surface(
        modifier = modifier.fillMaxWidth(),
        tonalElevation = 0.dp,
        shadowElevation = 0.dp,
        color = MaterialTheme.colorScheme.surfaceContainerLowest
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 8.dp)
                .navigationBarsPadding()
                .imePadding()
        ) {
            extraContent()

            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.Start
            ) {
                if (recording && voiceNote != null) {
                    // Live recording strip — same stroke as the text field.
                    VoiceRecordingStrip(
                        recorder = voiceNote,
                        modifier = Modifier
                            .weight(1f)
                            .defaultMinSize(minHeight = 56.dp)
                            .border(
                                width = 1.dp,
                                color = MaterialTheme.colorScheme.error.copy(alpha = 0.55f),
                                shape = RoundedCornerShape(24.dp)
                            )
                            .background(
                                color = MaterialTheme.colorScheme.errorContainer.copy(alpha = 0.18f),
                                shape = RoundedCornerShape(24.dp)
                            )
                            .padding(horizontal = 14.dp, vertical = 8.dp)
                    )
                } else {
                    textField(Modifier.weight(1f))
                }
                Spacer(modifier = Modifier.width(8.dp))

                val trailingActive = when {
                    recording -> true       // finish = stop button
                    active -> true          // send
                    showMic -> true         // start recording
                    else -> false
                }
                val trailingColor = when {
                    recording -> MaterialTheme.colorScheme.error
                    active || showMic -> MaterialTheme.colorScheme.primary
                    else -> MaterialTheme.colorScheme.surfaceVariant
                }
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
                        .size(48.dp)
                        .background(color = trailingColor, shape = CircleShape)
                ) {
                    when {
                        posting -> CircularProgressIndicator(
                            modifier = Modifier.size(20.dp),
                            strokeWidth = 2.dp,
                            color = MaterialTheme.colorScheme.onPrimary
                        )
                        recording -> Icon(
                            imageVector = Icons.Filled.Check,
                            contentDescription = "Finish recording",
                            tint = MaterialTheme.colorScheme.onError
                        )
                        showMic -> Icon(
                            imageVector = Icons.Filled.Mic,
                            contentDescription = "Record a voice note",
                            tint = MaterialTheme.colorScheme.onPrimary
                        )
                        else -> Icon(
                            imageVector = sendIcon,
                            contentDescription = sendContentDescription,
                            tint = if (active) MaterialTheme.colorScheme.onPrimary
                            else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.4f)
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun NebCommentTextFieldColors() = OutlinedTextFieldDefaults.colors(
    focusedContainerColor = MaterialTheme.colorScheme.surfaceContainerLowest,
    unfocusedContainerColor = MaterialTheme.colorScheme.surfaceContainerLowest,
    disabledContainerColor = MaterialTheme.colorScheme.surfaceContainerLowest,
    focusedBorderColor = MaterialTheme.colorScheme.primary,
    unfocusedBorderColor = MaterialTheme.colorScheme.outlineVariant,
    disabledBorderColor = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.55f)
)

/** Round "+" attach button for the leading slot of [NebCommentComposerBar] (inside the stroke). */
@Composable
fun ComposerAttachButton(enabled: Boolean, onClick: () -> Unit) {
    IconButton(
        onClick = onClick,
        enabled = enabled,
        modifier = Modifier.size(38.dp)
    ) {
        Icon(
            imageVector = Icons.Filled.Add,
            contentDescription = "Attach media",
            tint = if (enabled) MaterialTheme.colorScheme.primary
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
                    if (isAnonymous) MaterialTheme.colorScheme.primary else Color.Transparent,
                    CircleShape
                )
                .border(
                    1.dp,
                    if (isAnonymous) Color.Transparent else MaterialTheme.colorScheme.outlineVariant,
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
