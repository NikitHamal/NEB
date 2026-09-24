@file:OptIn(ExperimentalMaterial3Api::class)

package com.neb.ians.ui.screens.settings

import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.outlined.KeyboardArrowRight
import androidx.compose.material.icons.outlined.AutoAwesome
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.DarkMode
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material.icons.outlined.Palette
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.SpaceDashboard
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material.icons.outlined.VisibilityOff
import androidx.compose.material.icons.outlined.Wifi
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.MediumTopAppBar
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.repository.UserProfileCache
import com.neb.ians.ui.components.Avatar
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.screens.legal.NebLegal

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
    onNavigateToLegal: (String) -> Unit = {},
    onNavigateToCanvas: () -> Unit = {}
) {
    val isDarkMode by settingsViewModel.isDarkMode.collectAsStateWithLifecycle()
    val notificationsEnabled by settingsViewModel.notificationsEnabled.collectAsStateWithLifecycle()
    val downloadWifiOnly by settingsViewModel.downloadWifiOnly.collectAsStateWithLifecycle()
    val userProfile by settingsViewModel.userProfile.collectAsStateWithLifecycle()

    val scrollBehavior = TopAppBarDefaults.exitUntilCollapsedScrollBehavior()
    val profile = userProfile?.takeIf { it.id != "guest_user" }

    val context = LocalContext.current
    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { isGranted -> settingsViewModel.setNotificationsEnabled(isGranted) }

    Scaffold(
        modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            MediumTopAppBar(
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                title = { Text("Settings", fontWeight = FontWeight.SemiBold) },
                scrollBehavior = scrollBehavior,
                colors = TopAppBarDefaults.mediumTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    scrolledContainerColor = MaterialTheme.colorScheme.surfaceContainer
                )
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .verticalScroll(rememberScrollState())
        ) {
            IdentityCard(
                profile = profile,
                onEditProfile = onNavigateToEditProfile,
                onSignIn = onNavigateToLogin
            )

            if (profile != null) {
                SettingsGroup(title = "Account") {
                    PasswordSection(
                        settingsViewModel = settingsViewModel,
                        hasPassword = profile.hasPassword
                    )
                    SettingsDivider()
                    SettingsToggleRow(
                        icon = if (profile.isLocked) Icons.Outlined.VisibilityOff else Icons.Outlined.Visibility,
                        title = "Private profile",
                        subtitle = if (profile.isLocked) {
                            "Only your username is visible"
                        } else {
                            "Anyone can see your profile"
                        },
                        checked = profile.isLocked,
                        onCheckedChange = { settingsViewModel.toggleProfileLock(it) }
                    )
                    SettingsDivider()
                    SettingsRow(
                        icon = Icons.Outlined.BookmarkBorder,
                        title = "Bookmarks",
                        subtitle = "Saved posts and resources",
                        onClick = onNavigateToBookmarks
                    )
                    SettingsDivider()
                    SettingsRow(
                        icon = Icons.Outlined.AutoAwesome,
                        title = "Neby credits",
                        subtitle = "Balance, top-ups and point conversion",
                        onClick = onNavigateToNebyCredits
                    )
                    SettingsDivider()
                    SettingsRow(
                        icon = Icons.Outlined.Palette,
                        title = "My avatar",
                        subtitle = "Shape, mood and colours",
                        onClick = onNavigateToMyAvatar
                    )
                }
            }

            SettingsGroup(title = "Tools") {
                SettingsRow(
                    icon = Icons.Outlined.SpaceDashboard,
                    title = "NEBians Canvas",
                    subtitle = "Visual concept maps and whiteboards",
                    badge = "New",
                    onClick = onNavigateToCanvas
                )
            }

            SettingsGroup(title = "Preferences") {
                SettingsToggleRow(
                    icon = Icons.Outlined.DarkMode,
                    title = "Dark theme",
                    subtitle = if (isDarkMode) "On" else "Off",
                    checked = isDarkMode,
                    onCheckedChange = { settingsViewModel.setDarkMode(it) }
                )
                SettingsDivider()
                SettingsToggleRow(
                    icon = Icons.Outlined.Notifications,
                    title = "Push notifications",
                    subtitle = if (notificationsEnabled) "On" else "Off",
                    checked = notificationsEnabled,
                    onCheckedChange = { enabled ->
                        val needsPermission = enabled &&
                            Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU &&
                            ContextCompat.checkSelfPermission(
                                context,
                                Manifest.permission.POST_NOTIFICATIONS
                            ) != PackageManager.PERMISSION_GRANTED
                        if (needsPermission) {
                            permissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
                        } else {
                            settingsViewModel.setNotificationsEnabled(enabled)
                        }
                    }
                )
                SettingsDivider()
                SettingsToggleRow(
                    icon = Icons.Outlined.Wifi,
                    title = "Wi-Fi only downloads",
                    subtitle = if (downloadWifiOnly) "Wi-Fi only" else "Any network",
                    checked = downloadWifiOnly,
                    onCheckedChange = { settingsViewModel.setDownloadWifiOnly(it) }
                )
            }

            val appVersionName = remember(context) {
                runCatching {
                    context.packageManager.getPackageInfo(context.packageName, 0).versionName
                }.getOrNull() ?: "1.0.5"
            }

            SettingsGroup(title = "About") {
                SettingsRow(
                    icon = Icons.Outlined.Lock,
                    title = "Privacy policy",
                    subtitle = "How we protect your data",
                    onClick = { onNavigateToLegal(NebLegal.PRIVACY) }
                )
                SettingsDivider()
                SettingsRow(
                    icon = Icons.Outlined.Description,
                    title = "Terms of service",
                    subtitle = "Rules and guidelines for usage",
                    onClick = { onNavigateToLegal(NebLegal.TERMS) }
                )
                SettingsDivider()
                SettingsRow(
                    icon = Icons.Outlined.Info,
                    title = "Version",
                    subtitle = appVersionName
                )
            }

            if (profile != null) {
                SettingsGroup(title = "Account control") {
                    SettingsRow(
                        icon = Icons.Outlined.Delete,
                        title = "Delete account",
                        subtitle = "Permanently remove your profile and data",
                        tint = MaterialTheme.colorScheme.error,
                        titleColor = MaterialTheme.colorScheme.error,
                        onClick = onNavigateToDeleteAccount
                    )
                }

                Spacer(modifier = Modifier.height(24.dp))
                NebButton(
                    text = "Sign out",
                    onClick = { settingsViewModel.logout() },
                    modifier = Modifier.padding(horizontal = 16.dp),
                    tone = NebButtonTone.Outlined,
                    fillWidth = true
                )
            }

            Spacer(modifier = Modifier.navigationBarsPadding().height(96.dp))
        }
    }
}

@Composable
private fun IdentityCard(
    profile: UserProfileCache?,
    onEditProfile: () -> Unit,
    onSignIn: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .nebPressable(onClick = if (profile != null) onEditProfile else onSignIn)
            .clip(RoundedCornerShape(26.dp))
            .background(MaterialTheme.colorScheme.surfaceContainerLow)
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        if (profile != null) {
            Avatar(name = profile.username, imageUrl = profile.photoUrl, size = 52.dp)
        } else {
            Box(
                modifier = Modifier
                    .size(52.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.surfaceContainerHighest),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Outlined.Person,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.size(24.dp)
                )
            }
        }
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = profile?.displayName?.takeIf { it.isNotEmpty() }
                    ?: profile?.username
                    ?: "Guest mode",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold
            )
            Text(
                text = profile?.let { "@${it.username}" } ?: "Sign in to post, vote and upload",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        if (profile != null) {
            Icon(
                imageVector = Icons.AutoMirrored.Outlined.KeyboardArrowRight,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.outline
            )
        } else {
            NebButton(text = "Sign in", onClick = onSignIn)
        }
    }
}
