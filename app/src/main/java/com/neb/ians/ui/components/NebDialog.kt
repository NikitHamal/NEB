package com.neb.ians.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.MutableTransitionState
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.scaleIn
import androidx.compose.animation.scaleOut
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.BasicAlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material.icons.outlined.VisibilityOff
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialShapes
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.DialogProperties
import com.neb.ians.ui.theme.nebFastEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec

@Immutable
data class NebDialogAction(
    val label: String,
    val onClick: () -> Unit,
    val enabled: Boolean = true,
    val destructive: Boolean = false
)

@OptIn(ExperimentalMaterial3Api::class, ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun NebDialog(
    onDismissRequest: () -> Unit,
    title: String,
    modifier: Modifier = Modifier,
    supportingText: String? = null,
    icon: ImageVector? = null,
    confirm: NebDialogAction? = null,
    dismiss: NebDialogAction? = null,
    dismissOnClickOutside: Boolean = true,
    scrollable: Boolean = true,
    content: (@Composable ColumnScope.() -> Unit)? = null
) {
    BasicAlertDialog(
        onDismissRequest = onDismissRequest,
        properties = DialogProperties(
            dismissOnClickOutside = dismissOnClickOutside,
            usePlatformDefaultWidth = false
        ),
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp)
    ) {
        val entry = remember { MutableTransitionState(false).apply { targetState = true } }
        AnimatedVisibility(
            visibleState = entry,
            enter = scaleIn(animationSpec = nebSpatialSpec(), initialScale = 0.88f) +
                fadeIn(animationSpec = nebFastEffectsSpec()),
            exit = scaleOut(animationSpec = nebSpatialSpec(), targetScale = 0.94f) +
                fadeOut(animationSpec = nebFastEffectsSpec())
        ) {
            Surface(
                shape = RoundedCornerShape(30.dp),
                color = MaterialTheme.colorScheme.surfaceContainerHigh,
                contentColor = MaterialTheme.colorScheme.onSurface,
                tonalElevation = 0.dp,
                modifier = Modifier
                    .fillMaxWidth()
                    .widthIn(max = 420.dp)
                    .heightIn(max = 620.dp)
            ) {
                Column(modifier = Modifier.fillMaxWidth()) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(start = 26.dp, end = 26.dp, top = 26.dp)
                    ) {
                        if (icon != null) {
                            Box(
                                modifier = Modifier
                                    .size(46.dp)
                                    .clip(nebShape(MaterialShapes.Cookie9Sided))
                                    .background(MaterialTheme.colorScheme.secondaryContainer),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = icon,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.onSecondaryContainer,
                                    modifier = Modifier.size(22.dp)
                                )
                            }
                            Spacer(modifier = Modifier.height(16.dp))
                        }
                        Text(
                            text = title,
                            style = MaterialTheme.typography.headlineSmallEmphasized,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        if (supportingText != null) {
                            Spacer(modifier = Modifier.height(10.dp))
                            Text(
                                text = supportingText,
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }

                    if (content != null) {
                        val body = Modifier
                            .fillMaxWidth()
                            .weight(1f, fill = false)
                            .padding(start = 26.dp, end = 26.dp, top = 18.dp)
                        Column(
                            modifier = if (scrollable) body.verticalScroll(rememberScrollState()) else body,
                            verticalArrangement = Arrangement.spacedBy(12.dp),
                            content = content
                        )
                    }

                    if (confirm != null || dismiss != null) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(start = 20.dp, end = 20.dp, top = 22.dp, bottom = 20.dp),
                            horizontalArrangement = Arrangement.spacedBy(8.dp, Alignment.End),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            if (dismiss != null) {
                                TextButton(
                                    onClick = dismiss.onClick,
                                    enabled = dismiss.enabled,
                                    shape = RoundedCornerShape(50),
                                    colors = ButtonDefaults.textButtonColors(
                                        contentColor = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                ) {
                                    Text(
                                        text = dismiss.label,
                                        style = MaterialTheme.typography.labelLargeEmphasized
                                    )
                                }
                            }
                            if (confirm != null) {
                                Button(
                                    onClick = confirm.onClick,
                                    enabled = confirm.enabled,
                                    shape = RoundedCornerShape(50),
                                    colors = if (confirm.destructive) {
                                        ButtonDefaults.buttonColors(
                                            containerColor = MaterialTheme.colorScheme.error,
                                            contentColor = MaterialTheme.colorScheme.onError
                                        )
                                    } else {
                                        ButtonDefaults.buttonColors(
                                            containerColor = MaterialTheme.colorScheme.primary,
                                            contentColor = MaterialTheme.colorScheme.onPrimary
                                        )
                                    }
                                ) {
                                    Text(
                                        text = confirm.label,
                                        style = MaterialTheme.typography.labelLargeEmphasized
                                    )
                                }
                            }
                        }
                    } else {
                        Spacer(modifier = Modifier.height(24.dp))
                    }
                }
            }
        }
    }
}

@Composable
fun NebConfirmDialog(
    title: String,
    message: String,
    confirmLabel: String,
    onConfirm: () -> Unit,
    onDismiss: () -> Unit,
    modifier: Modifier = Modifier,
    icon: ImageVector? = null,
    dismissLabel: String = "Cancel",
    destructive: Boolean = false,
    confirmEnabled: Boolean = true
) {
    NebDialog(
        onDismissRequest = onDismiss,
        title = title,
        supportingText = message,
        icon = icon,
        modifier = modifier,
        confirm = NebDialogAction(
            label = confirmLabel,
            onClick = onConfirm,
            enabled = confirmEnabled,
            destructive = destructive
        ),
        dismiss = NebDialogAction(label = dismissLabel, onClick = onDismiss)
    )
}

@Composable
fun NebDialogTextField(
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier,
    placeholder: String? = null,
    label: String? = null,
    singleLine: Boolean = true,
    minLines: Int = 1,
    enabled: Boolean = true,
    isError: Boolean = false,
    supportingText: String? = null,
    visualTransformation: VisualTransformation = VisualTransformation.None,
    trailingIcon: (@Composable () -> Unit)? = null
) {
    OutlinedTextField(
        value = value,
        onValueChange = onValueChange,
        modifier = modifier.fillMaxWidth(),
        enabled = enabled,
        isError = isError,
        visualTransformation = visualTransformation,
        trailingIcon = trailingIcon,
        placeholder = placeholder?.let {
            {
                Text(
                    text = it,
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f)
                )
            }
        },
        label = label?.let { { Text(text = it, style = MaterialTheme.typography.bodyMedium) } },
        supportingText = supportingText?.let {
            {
                Text(
                    text = it,
                    style = MaterialTheme.typography.bodySmall,
                    color = if (isError) {
                        MaterialTheme.colorScheme.error
                    } else {
                        MaterialTheme.colorScheme.onSurfaceVariant
                    }
                )
            }
        },
        singleLine = singleLine,
        minLines = minLines,
        textStyle = MaterialTheme.typography.bodyLarge,
        shape = RoundedCornerShape(18.dp),
        colors = OutlinedTextFieldDefaults.colors(
            focusedContainerColor = MaterialTheme.colorScheme.surfaceContainerHighest,
            unfocusedContainerColor = MaterialTheme.colorScheme.surfaceContainerHighest,
            focusedBorderColor = MaterialTheme.colorScheme.onSurface,
            unfocusedBorderColor = Color.Transparent,
            focusedLabelColor = MaterialTheme.colorScheme.onSurface,
            unfocusedLabelColor = MaterialTheme.colorScheme.onSurfaceVariant
        )
    )
}

@Composable
fun NebDialogPasswordField(
    value: String,
    onValueChange: (String) -> Unit,
    label: String,
    modifier: Modifier = Modifier,
    supportingText: String? = null,
    isError: Boolean = false,
    revealable: Boolean = true
) {
    var visible by remember { mutableStateOf(false) }
    NebDialogTextField(
        value = value,
        onValueChange = onValueChange,
        modifier = modifier,
        label = label,
        isError = isError,
        supportingText = supportingText,
        visualTransformation = if (visible) VisualTransformation.None else PasswordVisualTransformation(),
        trailingIcon = if (!revealable) null else {
            {
                IconButton(onClick = { visible = !visible }) {
                    Icon(
                        imageVector = if (visible) Icons.Outlined.VisibilityOff else Icons.Outlined.Visibility,
                        contentDescription = if (visible) "Hide password" else "Show password",
                        modifier = Modifier.size(20.dp)
                    )
                }
            }
        }
    )
}
