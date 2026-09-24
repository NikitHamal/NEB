package com.neb.ians.ui.screens.settings

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.AutoAwesome
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.DarkMode
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.Description
import android.content.Intent
import android.net.Uri
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material.icons.outlined.Palette
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material.icons.outlined.SpaceDashboard
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material.icons.outlined.VisibilityOff
import androidx.compose.material.icons.outlined.Wifi
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
import com.neb.ians.ui.components.Avatar

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    onNavigateBack: () -> Unit,
    settingsViewModel: SettingsViewModel,
    onNavigateToEditProfile: () -> Unit,
    onNavigateToBookmarks: () -> Unit = {},
    onNavigateToNebyCredits: () -> Unit = {},
    onNavigateToMyAvatar: () -> Unit = {},
    onNavigateToDeleteAccount: () -> Unit = {},
    onNavigateToLogin: () -> Unit = {},
    onNavigateToWebPortal: (String) -> Unit = {},
    onNavigateToCanvas: () -> Unit = {}
) {
    val isDarkMode by settingsViewModel.isDarkMode.collectAsStateWithLifecycle()
    val notificationsEnabled by settingsViewModel.notificationsEnabled.collectAsStateWithLifecycle()
    val downloadWifiOnly by settingsViewModel.downloadWifiOnly.collectAsStateWithLifecycle()
    val userProfile by settingsViewModel.userProfile.collectAsStateWithLifecycle()

    val scrollBehavior = TopAppBarDefaults.exitUntilCollapsedScrollBehavior()
    val isGuest = userProfile == null || userProfile?.id == "guest_user"

    val context = androidx.compose.ui.platform.LocalContext.current
    val permissionLauncher = androidx.activity.compose.rememberLauncherForActivityResult(
        contract = androidx.activity.result.contract.ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        settingsViewModel.setNotificationsEnabled(isGranted)
    }

    Scaffold(
        modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            MediumTopAppBar(
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back"
                        )
                    }
                },
                title = {
                    Text(
                        text = "Settings",
                        fontWeight = FontWeight.SemiBold
                    )
                },
                scrollBehavior = scrollBehavior,
                colors = TopAppBarDefaults.mediumTopAppBarColors(
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
                            fontWeight = FontWeight.SemiBold,
                            style = MaterialTheme.typography.bodyLarge
                        )
                    },
                    supportingContent = {
                        Text("@${profile.username}", style = MaterialTheme.typography.bodySmall)
                    },
                    leadingContent = {
                        Avatar(
                            name = profile.username,
                            imageUrl = profile.photoUrl,
                            size = 40.dp
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
                    headlineContent = { Text("Profile Visibility", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium) },
                    supportingContent = {
                        Text(
                            if (profile.isLocked) "Private — only username visible" else "Public — profile visible to everyone",
                            style = MaterialTheme.typography.bodySmall
                        )
                    },
                    leadingContent = {
                        Icon(
                            imageVector = if (profile.isLocked) Icons.Outlined.VisibilityOff else Icons.Outlined.Visibility,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.size(22.dp)
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

                HorizontalDivider(
                    modifier = Modifier.padding(horizontal = 16.dp),
                    color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)
                )

                ListItem(
                    modifier = Modifier.clickable { onNavigateToBookmarks() },
                    headlineContent = { Text("Bookmarks", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium) },
                    supportingContent = {
                        Text("Saved posts and resources", style = MaterialTheme.typography.bodySmall)
                    },
                    leadingContent = {
                        Icon(
                            imageVector = Icons.Outlined.BookmarkBorder,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.size(22.dp)
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

                ListItem(
                    modifier = Modifier.clickable { onNavigateToNebyCredits() },
                    headlineContent = { Text("Neby Credits", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium) },
                    supportingContent = {
                        Text("10 free monthly credits, convert points & developer contact", style = MaterialTheme.typography.bodySmall)
                    },
                    leadingContent = {
                        Icon(
                            imageVector = Icons.Outlined.AutoAwesome,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.size(22.dp)
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

                ListItem(
                    modifier = Modifier.clickable { onNavigateToMyAvatar() },
                    headlineContent = { Text("My Avatar", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium) },
                    supportingContent = {
                        Text("Customize your generated avatar — shape, mood, colors", style = MaterialTheme.typography.bodySmall)
                    },
                    leadingContent = {
                        Icon(
                            imageVector = Icons.Outlined.Palette,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.size(22.dp)
                        )
                    },
                    colors = ListItemDefaults.colors(
                        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
                    )
                )
            } else {
                ListItem(
                    headlineContent = {
                        Text("Guest Mode", fontWeight = FontWeight.SemiBold, style = MaterialTheme.typography.bodyLarge)
                    },
                    supportingContent = {
                        Text("Sign in to join discussions and vote.", style = MaterialTheme.typography.bodySmall)
                    },
                    leadingContent = {
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .clip(CircleShape)
                                .background(MaterialTheme.colorScheme.surfaceContainerHigh),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.Person,
                                contentDescription = null,
                                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.size(22.dp)
                            )
                        }
                    },
                    colors = ListItemDefaults.colors(
                        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
                    )
                )
            }

            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.3f))

            SettingsSectionLabel(label = "Tools & Whiteboard")

            ListItem(
                modifier = Modifier.clickable { onNavigateToCanvas() },
                headlineContent = { Text("NEBians Canvas", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold) },
                supportingContent = {
                    Text("Interactive visual concept mapping, diagrams & whiteboards powered by Neby", style = MaterialTheme.typography.bodySmall)
                },
                leadingContent = {
                    Icon(
                        imageVector = Icons.Outlined.SpaceDashboard,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.size(22.dp)
                    )
                },
                trailingContent = {
                    Surface(
                        shape = RoundedCornerShape(99.dp),
                        color = MaterialTheme.colorScheme.primaryContainer
                    ) {
                        Text(
                            "New",
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp),
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onPrimaryContainer,
                            fontWeight = FontWeight.Bold
                        )
                    }
                },
                colors = ListItemDefaults.colors(
                    containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
                )
            )

            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.3f))

            SettingsSectionLabel(label = "Preferences")

            ListItem(
                headlineContent = { Text("Dark Theme", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium) },
                supportingContent = { Text(if (isDarkMode) "On" else "Off", style = MaterialTheme.typography.bodySmall) },
                leadingContent = {
                    Icon(
                        imageVector = Icons.Outlined.DarkMode,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(22.dp)
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
                headlineContent = { Text("Push Notifications", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium) },
                supportingContent = { Text(if (notificationsEnabled) "On" else "Off", style = MaterialTheme.typography.bodySmall) },
                leadingContent = {
                    Icon(
                        imageVector = Icons.Outlined.Notifications,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(22.dp)
                    )
                },
                trailingContent = {
                    Switch(
                        checked = notificationsEnabled,
                        onCheckedChange = { enabled ->
                            if (enabled && android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
                                if (androidx.core.content.ContextCompat.checkSelfPermission(
                                        context,
                                        android.Manifest.permission.POST_NOTIFICATIONS
                                    ) != android.content.pm.PackageManager.PERMISSION_GRANTED
                                ) {
                                    permissionLauncher.launch(android.Manifest.permission.POST_NOTIFICATIONS)
                                } else {
                                    settingsViewModel.setNotificationsEnabled(true)
                                }
                            } else {
                                settingsViewModel.setNotificationsEnabled(enabled)
                            }
                        }
                    )
                },
                colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)
            )

            HorizontalDivider(
                modifier = Modifier.padding(horizontal = 16.dp),
                color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)
            )

            ListItem(
                headlineContent = { Text("Wi-Fi Only Downloads", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium) },
                supportingContent = { Text(if (downloadWifiOnly) "Wi-Fi only" else "Any network", style = MaterialTheme.typography.bodySmall) },
                leadingContent = {
                    Icon(
                        imageVector = Icons.Outlined.Wifi,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(22.dp)
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

            val appVersionName = remember(context) {
                runCatching {
                    context.packageManager.getPackageInfo(context.packageName, 0).versionName
                }.getOrNull() ?: "1.0.5"
            }

            ListItem(
                headlineContent = { Text("Version", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium) },
                supportingContent = { Text(appVersionName, style = MaterialTheme.typography.bodySmall) },
                leadingContent = {
                    Icon(
                        imageVector = Icons.Outlined.Info,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(22.dp)
                    )
                },
                colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)
            )

            HorizontalDivider(
                modifier = Modifier.padding(horizontal = 16.dp),
                color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)
            )

            ListItem(
                modifier = Modifier.clickable {
                    onNavigateToWebPortal("https://nebians.consica.com.np/privacy/")
                },
                headlineContent = { Text("Privacy Policy", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium) },
                supportingContent = { Text("How we protect your data", style = MaterialTheme.typography.bodySmall) },
                leadingContent = {
                    Icon(
                        imageVector = Icons.Outlined.Lock,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(22.dp)
                    )
                },
                colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)
            )

            HorizontalDivider(
                modifier = Modifier.padding(horizontal = 16.dp),
                color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)
            )

            ListItem(
                modifier = Modifier.clickable {
                    onNavigateToWebPortal("https://nebians.consica.com.np/terms/")
                },
                headlineContent = { Text("Terms of Service", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium) },
                supportingContent = { Text("Rules and guidelines for usage", style = MaterialTheme.typography.bodySmall) },
                leadingContent = {
                    Icon(
                        imageVector = Icons.Outlined.Description,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(22.dp)
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
                        .height(48.dp)
                        .padding(horizontal = 16.dp),
                    shape = CircleShape
                ) {
                    Text("Sign In", fontWeight = FontWeight.SemiBold)
                }
            } else {
                Spacer(modifier = Modifier.height(16.dp))
                SettingsSectionLabel(label = "Danger Zone")
                ListItem(
                    modifier = Modifier.clickable { onNavigateToDeleteAccount() },
                    headlineContent = { Text("Delete Account", color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium) },
                    supportingContent = { Text("Permanently delete your profile and data", style = MaterialTheme.typography.bodySmall) },
                    leadingContent = {
                        Icon(
                            imageVector = Icons.Outlined.Delete,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.error,
                            modifier = Modifier.size(22.dp)
                        )
                    },
                    colors = ListItemDefaults.colors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)
                )
                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.3f))
                Spacer(modifier = Modifier.height(24.dp))

                OutlinedButton(
                    onClick = { settingsViewModel.logout() },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(48.dp)
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

            Spacer(modifier = Modifier.navigationBarsPadding().height(96.dp))
        }
    }
}

@Composable
private fun SettingsSectionLabel(label: String) {
    Text(
        text = label,
        style = MaterialTheme.typography.labelSmall,
        color = MaterialTheme.colorScheme.primary,
        fontWeight = FontWeight.SemiBold,
        modifier = Modifier.padding(start = 16.dp, end = 16.dp, top = 16.dp, bottom = 2.dp)
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
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium
            )
        },
        supportingContent = {
            Text(
                if (hasPassword) "Update your account password" else "Add a password for email sign-in",
                style = MaterialTheme.typography.bodySmall
            )
        },
        leadingContent = {
            Icon(
                imageVector = Icons.Outlined.Lock,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.size(22.dp)
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
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(12.dp))
                OutlinedTextField(
                    value = password,
                    onValueChange = { password = it },
                    label = { Text("Password") },
                    singleLine = true,
                    visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                    trailingIcon = {
                        IconButton(onClick = { passwordVisible = !passwordVisible }) {
                            Icon(
                                imageVector = if (passwordVisible) Icons.Outlined.VisibilityOff else Icons.Outlined.Visibility,
                                contentDescription = null,
                                modifier = Modifier.size(20.dp)
                            )
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    supportingText = { Text("At least 8 characters", style = MaterialTheme.typography.bodySmall) }
                )
                Spacer(modifier = Modifier.height(8.dp))
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
                            Text("Passwords don't match", color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
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
                                imageVector = if (currentVisible) Icons.Outlined.VisibilityOff else Icons.Outlined.Visibility,
                                contentDescription = null,
                                modifier = Modifier.size(20.dp)
                            )
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
                Spacer(modifier = Modifier.height(8.dp))
                OutlinedTextField(
                    value = newPassword,
                    onValueChange = { newPassword = it },
                    label = { Text("New Password") },
                    singleLine = true,
                    visualTransformation = if (newVisible) VisualTransformation.None else PasswordVisualTransformation(),
                    trailingIcon = {
                        IconButton(onClick = { newVisible = !newVisible }) {
                            Icon(
                                imageVector = if (newVisible) Icons.Outlined.VisibilityOff else Icons.Outlined.Visibility,
                                contentDescription = null,
                                modifier = Modifier.size(20.dp)
                            )
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    supportingText = { Text("At least 8 characters", style = MaterialTheme.typography.bodySmall) }
                )
                Spacer(modifier = Modifier.height(8.dp))
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
                            Text("Passwords don't match", color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
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