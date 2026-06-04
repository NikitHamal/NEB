package com.neb.ians.ui.screens.settings

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material.icons.outlined.Person
import androidx.compose.ui.res.painterResource
import com.neb.ians.R
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.UserAvatar

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    settingsViewModel: SettingsViewModel,
    onNavigateToEditProfile: () -> Unit,
    onNavigateToLogin: () -> Unit = {}
) {
    val isDarkMode by settingsViewModel.isDarkMode.collectAsStateWithLifecycle()
    val notificationsEnabled by settingsViewModel.notificationsEnabled.collectAsStateWithLifecycle()
    val downloadWifiOnly by settingsViewModel.downloadWifiOnly.collectAsStateWithLifecycle()
    val userProfile by settingsViewModel.userProfile.collectAsStateWithLifecycle()

    val scrollBehavior = TopAppBarDefaults.exitUntilCollapsedScrollBehavior()
    val isGuest = userProfile == null || userProfile?.id == "guest_user"

    Scaffold(
        modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            LargeTopAppBar(
                title = {
                    Text(
                        text = "Settings",
                        fontWeight = FontWeight.Bold
                    )
                },
                scrollBehavior = scrollBehavior,
                colors = TopAppBarDefaults.largeTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    scrolledContainerColor = MaterialTheme.colorScheme.surfaceContainer
                )
            )
        },
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .verticalScroll(rememberScrollState())
        ) {
            SettingsSectionLabel(label = "Account")

            if (!isGuest && userProfile != null) {
                val profile = userProfile!!

                ListItem(
                    modifier = Modifier.clickable { onNavigateToEditProfile() },
                    headlineContent = {
                        Text(
                            text = profile.displayName?.takeIf { it.isNotEmpty() } ?: profile.username,
                            fontWeight = FontWeight.SemiBold
                        )
                    },
                    supportingContent = {
                        Text("@${profile.username}")
                    },
                    leadingContent = {
                        UserAvatar(
                            name = profile.displayName?.takeIf { it.isNotEmpty() } ?: profile.username,
                            photoUrl = profile.photoUrl,
                            size = 48.dp
                        )
                    },
                    colors = ListItemDefaults.colors(
                        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
                    )
                )

                HorizontalDivider(
                    modifier = Modifier.padding(horizontal = 16.dp),
                    color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)
                )

                if (!isGuest && userProfile != null) {
                    PasswordSection(settingsViewModel = settingsViewModel, hasPassword = userProfile!!.hasPassword)
                }

                ListItem(
                    headlineContent = { Text("Profile Visibility", fontWeight = FontWeight.Medium) },
                    supportingContent = {
                        Text(if (profile.isLocked) "Private — only username visible to others" else "Public — your profile is visible")
                    },
                    leadingContent = {
                        Icon(
                            painter = painterResource(id = if (profile.isLocked) R.drawable.ic_visibility_off else R.drawable.ic_visibility),
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    },
                    trailingContent = {
                        Switch(
                            checked = profile.isLocked,
                            onCheckedChange = { settingsViewModel.toggleProfileLock(it) }
                        )
                    },
                    colors = ListItemDefaults.colors(
                        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
                    )
                )
            } else {
                ListItem(
                    headlineContent = {
                        Text("Guest Mode", fontWeight = FontWeight.SemiBold)
                    },
                    supportingContent = {
                        Text("Sign in to back up annotations, join discussions, and vote.")
                    },
                    leadingContent = {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .clip(CircleShape)
                                .background(MaterialTheme.colorScheme.surfaceContainerHigh),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.Person,
                                contentDescription = null,
                                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.size(28.dp)
                            )
                        }
                    },
                    colors = ListItemDefaults.colors(
                        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
                    )
                )
            }

            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.3f))

            SettingsSectionLabel(label = "Preferences")

            ListItem(
                headlineContent = { Text("Dark Theme", fontWeight = FontWeight.Medium) },
                supportingContent = { Text(if (isDarkMode) "Enabled" else "Disabled") },
                leadingContent = {
                    Icon(
                        painter = painterResource(id = R.drawable.ic_dark_mode),
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                },
                trailingContent = {
                    Switch(
                        checked = isDarkMode,
                        onCheckedChange = { settingsViewModel.setDarkMode(it) }
                    )
                },
                colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)
            )

            HorizontalDivider(
                modifier = Modifier.padding(horizontal = 16.dp),
                color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)
            )

            ListItem(
                headlineContent = { Text("Push Notifications", fontWeight = FontWeight.Medium) },
                supportingContent = { Text(if (notificationsEnabled) "On" else "Off") },
                leadingContent = {
                    Icon(
                        imageVector = Icons.Outlined.Notifications,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                },
                trailingContent = {
                    Switch(
                        checked = notificationsEnabled,
                        onCheckedChange = { settingsViewModel.setNotificationsEnabled(it) }
                    )
                },
                colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)
            )

            HorizontalDivider(
                modifier = Modifier.padding(horizontal = 16.dp),
                color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)
            )

            ListItem(
                headlineContent = { Text("Wi-Fi Only Downloads", fontWeight = FontWeight.Medium) },
                supportingContent = { Text(if (downloadWifiOnly) "Only download on Wi-Fi" else "Download on any network") },
                leadingContent = {
                    Icon(
                        painter = painterResource(id = R.drawable.ic_wifi),
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                },
                trailingContent = {
                    Switch(
                        checked = downloadWifiOnly,
                        onCheckedChange = { settingsViewModel.setDownloadWifiOnly(it) }
                    )
                },
                colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)
            )

            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.3f))

            SettingsSectionLabel(label = "About")

            ListItem(
                headlineContent = { Text("Version", fontWeight = FontWeight.Medium) },
                supportingContent = { Text("1.0.0 (Stable Release)") },
                leadingContent = {
                    Icon(
                        imageVector = Icons.Outlined.Info,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                },
                colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)
            )

            HorizontalDivider(
                modifier = Modifier.padding(horizontal = 16.dp),
                color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)
            )

            ListItem(
                headlineContent = { Text("NEBians Network", fontWeight = FontWeight.Medium) },
                supportingContent = { Text("Collaborative resources for Nepali students") },
                leadingContent = {
                    Icon(
                        painter = painterResource(id = R.drawable.ic_school),
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                },
                colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)
            )

            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.3f))

            Spacer(modifier = Modifier.height(16.dp))

            if (isGuest) {
                Button(
                    onClick = { onNavigateToLogin() },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp)
                        .padding(horizontal = 16.dp),
                    shape = CircleShape
                ) {
                    Text("Sign In", fontWeight = FontWeight.SemiBold)
                }
            } else {
                OutlinedButton(
                    onClick = { settingsViewModel.logout() },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp)
                        .padding(horizontal = 16.dp),
                    shape = CircleShape,
                    colors = ButtonDefaults.outlinedButtonColors(
                        contentColor = MaterialTheme.colorScheme.error
                    ),
                    border = androidx.compose.foundation.BorderStroke(
                        width = 1.dp,
                        color = MaterialTheme.colorScheme.error.copy(alpha = 0.5f)
                    )
                ) {
                    Text("Sign Out", fontWeight = FontWeight.SemiBold)
                }
            }

            Spacer(modifier = Modifier.height(40.dp))
        }
    }
}

@Composable
private fun SettingsSectionLabel(label: String) {
    Text(
        text = label,
        style = MaterialTheme.typography.labelMedium,
        color = MaterialTheme.colorScheme.primary,
        fontWeight = FontWeight.SemiBold,
        modifier = Modifier.padding(start = 16.dp, end = 16.dp, top = 20.dp, bottom = 4.dp)
    )
}

@Composable
private fun PasswordSection(settingsViewModel: SettingsViewModel, hasPassword: Boolean) {
    var showSetDialog by remember { mutableStateOf(false) }
    var showChangeDialog by remember { mutableStateOf(false) }

    ListItem(
        headlineContent = {
            Text(
                if (hasPassword) "Change Password" else "Set Password",
                fontWeight = FontWeight.Medium
            )
        },
        supportingContent = {
            Text(if (hasPassword) "Update your account password" else "Add a password to sign in with email/username")
        },
        leadingContent = {
            Icon(
                imageVector = Icons.Outlined.Lock,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onSurfaceVariant
            )
        },
        modifier = Modifier.clickable {
            if (hasPassword) showChangeDialog = true else showSetDialog = true
        },
        colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)
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
    var passwordVisible by remember { mutableStateOf(false) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Set Password") },
        text = {
            Column {
                Text(
                    "Add a password so you can also sign in with your email or username.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(16.dp))
                OutlinedTextField(
                    value = password,
                    onValueChange = { password = it },
                    label = { Text("Password") },
                    singleLine = true,
                    visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                    trailingIcon = {
                        IconButton(onClick = { passwordVisible = !passwordVisible }) {
                            Icon(
                                painter = painterResource(id = if (passwordVisible) R.drawable.ic_visibility_off else R.drawable.ic_visibility),
                                contentDescription = null
                            )
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    supportingText = { Text("At least 8 characters") }
                )
                Spacer(modifier = Modifier.height(12.dp))
                OutlinedTextField(
                    value = confirmPassword,
                    onValueChange = { confirmPassword = it },
                    label = { Text("Confirm Password") },
                    singleLine = true,
                    visualTransformation = PasswordVisualTransformation(),
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    isError = confirmPassword.isNotBlank() && password != confirmPassword,
                    supportingText = {
                        if (confirmPassword.isNotBlank() && password != confirmPassword) {
                            Text("Passwords don't match", color = MaterialTheme.colorScheme.error)
                        }
                    }
                )
            }
        },
        confirmButton = {
            TextButton(
                onClick = { onSetPassword(password) },
                enabled = password.length >= 8 && password == confirmPassword
            ) {
                Text("Set Password")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel") }
        }
    )
}

@Composable
private fun ChangePasswordDialog(
    onDismiss: () -> Unit,
    onChangePassword: (String, String) -> Unit
) {
    var currentPassword by remember { mutableStateOf("") }
    var newPassword by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var currentVisible by remember { mutableStateOf(false) }
    var newVisible by remember { mutableStateOf(false) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Change Password") },
        text = {
            Column {
                OutlinedTextField(
                    value = currentPassword,
                    onValueChange = { currentPassword = it },
                    label = { Text("Current Password") },
                    singleLine = true,
                    visualTransformation = if (currentVisible) VisualTransformation.None else PasswordVisualTransformation(),
                    trailingIcon = {
                        IconButton(onClick = { currentVisible = !currentVisible }) {
                            Icon(
                                painter = painterResource(id = if (currentVisible) R.drawable.ic_visibility_off else R.drawable.ic_visibility),
                                contentDescription = null
                            )
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
                Spacer(modifier = Modifier.height(12.dp))
                OutlinedTextField(
                    value = newPassword,
                    onValueChange = { newPassword = it },
                    label = { Text("New Password") },
                    singleLine = true,
                    visualTransformation = if (newVisible) VisualTransformation.None else PasswordVisualTransformation(),
                    trailingIcon = {
                        IconButton(onClick = { newVisible = !newVisible }) {
                            Icon(
                                painter = painterResource(id = if (newVisible) R.drawable.ic_visibility_off else R.drawable.ic_visibility),
                                contentDescription = null
                            )
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    supportingText = { Text("At least 8 characters") }
                )
                Spacer(modifier = Modifier.height(12.dp))
                OutlinedTextField(
                    value = confirmPassword,
                    onValueChange = { confirmPassword = it },
                    label = { Text("Confirm New Password") },
                    singleLine = true,
                    visualTransformation = PasswordVisualTransformation(),
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    isError = confirmPassword.isNotBlank() && newPassword != confirmPassword,
                    supportingText = {
                        if (confirmPassword.isNotBlank() && newPassword != confirmPassword) {
                            Text("Passwords don't match", color = MaterialTheme.colorScheme.error)
                        }
                    }
                )
            }
        },
        confirmButton = {
            TextButton(
                onClick = { onChangePassword(currentPassword, newPassword) },
                enabled = currentPassword.isNotBlank() && newPassword.length >= 8 && newPassword == confirmPassword
            ) {
                Text("Change Password")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel") }
        }
    )
}