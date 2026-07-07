package com.neb.ians.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowUpward
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

/**
 * Shared transparent bottom composer used by post replies, resource comments, and any
 * future comment-style surfaces.  Keep this as the single source of truth so the
 * library/resource UI stays visually aligned with the forum post detail composer.
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
            colors = NebCommentTextFieldColors()
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
            visualTransformation = visualTransformation
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
    extraContent: @Composable () -> Unit,
    textField: @Composable (Modifier) -> Unit
) {
    val active = enabled && canSend && !posting

    Surface(
        modifier = modifier.fillMaxWidth(),
        tonalElevation = 0.dp,
        shadowElevation = 0.dp,
        color = Color.Transparent
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
                textField(Modifier.weight(1f))
                Spacer(modifier = Modifier.width(8.dp))
                IconButton(
                    onClick = onSend,
                    enabled = active,
                    modifier = Modifier
                        .size(48.dp)
                        .background(
                            color = if (active) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                            shape = CircleShape
                        )
                ) {
                    if (posting) {
                        CircularProgressIndicator(
                            modifier = Modifier.size(20.dp),
                            strokeWidth = 2.dp,
                            color = MaterialTheme.colorScheme.onPrimary
                        )
                    } else {
                        Icon(
                            imageVector = sendIcon,
                            contentDescription = sendContentDescription,
                            tint = if (active) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.4f)
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun NebCommentTextFieldColors() = OutlinedTextFieldDefaults.colors(
    focusedContainerColor = Color.Transparent,
    unfocusedContainerColor = Color.Transparent,
    disabledContainerColor = Color.Transparent,
    focusedBorderColor = MaterialTheme.colorScheme.primary,
    unfocusedBorderColor = MaterialTheme.colorScheme.outlineVariant,
    disabledBorderColor = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.55f)
)
