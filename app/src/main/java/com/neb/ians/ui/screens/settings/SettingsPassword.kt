package com.neb.ians.ui.screens.settings

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.NebDialog
import com.neb.ians.ui.components.NebDialogAction
import com.neb.ians.ui.components.NebDialogPasswordField

@Composable
fun PasswordSection(settingsViewModel: SettingsViewModel, hasPassword: Boolean) {
    var showSetDialog by remember { mutableStateOf(false) }
    var showChangeDialog by remember { mutableStateOf(false) }

    SettingsRow(
        icon = Icons.Outlined.Lock,
        title = if (hasPassword) "Change password" else "Set password",
        subtitle = if (hasPassword) {
            "Update your account password"
        } else {
            "Add a password for email sign-in"
        },
        onClick = {
            if (hasPassword) showChangeDialog = true else showSetDialog = true
        }
    )

    if (showSetDialog) {
        SetPasswordDialog(
            onDismiss = { showSetDialog = false },
            onSetPassword = { settingsViewModel.setPassword(it) }
        )
    }

    if (showChangeDialog) {
        ChangePasswordDialog(
            onDismiss = { showChangeDialog = false },
            onChangePassword = { current, new -> settingsViewModel.changePassword(current, new) }
        )
    }

    val passwordState by settingsViewModel.passwordState.collectAsStateWithLifecycle()
    LaunchedEffect(passwordState) {
        if (passwordState is PasswordUiState.Success) {
            showSetDialog = false
            showChangeDialog = false
            settingsViewModel.resetPasswordState()
        }
    }
}

@Composable
private fun SetPasswordDialog(
    onDismiss: () -> Unit,
    onSetPassword: (String) -> Unit
) {
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    val mismatch = confirmPassword.isNotBlank() && password != confirmPassword

    NebDialog(
        onDismissRequest = onDismiss,
        title = "Set a password",
        supportingText = "Add a password so you can also sign in with your email or username.",
        icon = Icons.Outlined.Lock,
        confirm = NebDialogAction(
            label = "Set password",
            onClick = { onSetPassword(password) },
            enabled = password.length >= 8 && password == confirmPassword
        ),
        dismiss = NebDialogAction("Cancel", onDismiss)
    ) {
        NebDialogPasswordField(
            value = password,
            onValueChange = { password = it },
            label = "Password",
            supportingText = "At least 8 characters"
        )
        NebDialogPasswordField(
            value = confirmPassword,
            onValueChange = { confirmPassword = it },
            label = "Confirm password",
            isError = mismatch,
            supportingText = if (mismatch) "Passwords don't match" else null,
            revealable = false
        )
    }
}

@Composable
private fun ChangePasswordDialog(
    onDismiss: () -> Unit,
    onChangePassword: (String, String) -> Unit
) {
    var currentPassword by remember { mutableStateOf("") }
    var newPassword by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    val mismatch = confirmPassword.isNotBlank() && newPassword != confirmPassword

    NebDialog(
        onDismissRequest = onDismiss,
        title = "Change password",
        icon = Icons.Outlined.Lock,
        confirm = NebDialogAction(
            label = "Change",
            onClick = { onChangePassword(currentPassword, newPassword) },
            enabled = currentPassword.isNotBlank() &&
                newPassword.length >= 8 &&
                newPassword == confirmPassword
        ),
        dismiss = NebDialogAction("Cancel", onDismiss)
    ) {
        NebDialogPasswordField(
            value = currentPassword,
            onValueChange = { currentPassword = it },
            label = "Current password"
        )
        NebDialogPasswordField(
            value = newPassword,
            onValueChange = { newPassword = it },
            label = "New password",
            supportingText = "At least 8 characters"
        )
        NebDialogPasswordField(
            value = confirmPassword,
            onValueChange = { confirmPassword = it },
            label = "Confirm new password",
            isError = mismatch,
            supportingText = if (mismatch) "Passwords don't match" else null,
            revealable = false
        )
    }
}
