package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.DarkMode
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.LightMode
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.PhoneAndroid
import androidx.compose.material.icons.filled.Storage
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.LargeTopAppBar
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.SegmentedButton
import androidx.compose.material3.SegmentedButtonDefaults
import androidx.compose.material3.SingleChoiceSegmentedButtonRow
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import com.neb.ians.utils.ThemePreference
import com.neb.ians.utils.ThemeSettings
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(
    themeSettings: ThemeSettings,
    currentTheme: ThemePreference,
) {
    val scope = rememberCoroutineScope()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState()),
    ) {
        LargeTopAppBar(
            title = {
                Column {
                    Text("Profile", style = MaterialTheme.typography.headlineMedium)
                    Text(
                        "Settings & preferences",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            },
        )

        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.primaryContainer,
            ),
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(20.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Surface(
                    shape = MaterialTheme.shapes.extraLarge,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(56.dp),
                ) {
                    Icon(
                        Icons.Filled.Person,
                        contentDescription = null,
                        modifier = Modifier.padding(12.dp),
                        tint = MaterialTheme.colorScheme.onPrimary,
                    )
                }
                Spacer(Modifier.width(16.dp))
                Column {
                    Text(
                        "NEB Student",
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.onPrimaryContainer,
                    )
                    Text(
                        "Grade 12 • Science",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.7f),
                    )
                }
            }
        }

        Spacer(Modifier.height(20.dp))

        Text(
            "Appearance",
            style = MaterialTheme.typography.titleSmall,
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
        )

        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.surfaceContainerLow,
            ),
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    "Theme",
                    style = MaterialTheme.typography.bodyMedium,
                )
                Spacer(Modifier.height(8.dp))
                SingleChoiceSegmentedButtonRow(modifier = Modifier.fillMaxWidth()) {
                    SegmentedButton(
                        selected = currentTheme == ThemePreference.LIGHT,
                        onClick = { scope.launch { themeSettings.setTheme(ThemePreference.LIGHT) } },
                        shape = SegmentedButtonDefaults.itemShape(index = 0, count = 3),
                        icon = {
                            Icon(
                                Icons.Filled.LightMode,
                                contentDescription = null,
                                modifier = Modifier.size(18.dp),
                            )
                        },
                    ) {
                        Text("Light")
                    }
                    SegmentedButton(
                        selected = currentTheme == ThemePreference.DARK,
                        onClick = { scope.launch { themeSettings.setTheme(ThemePreference.DARK) } },
                        shape = SegmentedButtonDefaults.itemShape(index = 1, count = 3),
                        icon = {
                            Icon(
                                Icons.Filled.DarkMode,
                                contentDescription = null,
                                modifier = Modifier.size(18.dp),
                            )
                        },
                    ) {
                        Text("Dark")
                    }
                    SegmentedButton(
                        selected = currentTheme == ThemePreference.SYSTEM,
                        onClick = { scope.launch { themeSettings.setTheme(ThemePreference.SYSTEM) } },
                        shape = SegmentedButtonDefaults.itemShape(index = 2, count = 3),
                        icon = {
                            Icon(
                                Icons.Filled.PhoneAndroid,
                                contentDescription = null,
                                modifier = Modifier.size(18.dp),
                            )
                        },
                    ) {
                        Text("Auto")
                    }
                }
            }
        }

        Spacer(Modifier.height(20.dp))

        Text(
            "About",
            style = MaterialTheme.typography.titleSmall,
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
        )

        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.surfaceContainerLow,
            ),
        ) {
            Column {
                SettingsItem(
                    icon = Icons.Filled.Info,
                    title = "Version",
                    subtitle = "1.0.0",
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp))
                SettingsItem(
                    icon = Icons.Filled.Storage,
                    title = "Offline Storage",
                    subtitle = "Cached resources available offline",
                )
                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp))
                SettingsItem(
                    icon = Icons.Filled.Notifications,
                    title = "Notifications",
                    subtitle = "Announcements and community updates",
                )
            }
        }

        Spacer(Modifier.height(24.dp))

        Text(
            "NEBians - Your NEB Study Companion",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier
                .padding(horizontal = 16.dp)
                .align(Alignment.CenterHorizontally),
        )

        Spacer(Modifier.height(32.dp))
    }
}

@Composable
private fun SettingsItem(
    icon: ImageVector,
    title: String,
    subtitle: String,
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Icon(
            icon,
            contentDescription = null,
            modifier = Modifier.size(24.dp),
            tint = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Spacer(Modifier.width(16.dp))
        Column {
            Text(title, style = MaterialTheme.typography.bodyMedium)
            Text(
                subtitle,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}
