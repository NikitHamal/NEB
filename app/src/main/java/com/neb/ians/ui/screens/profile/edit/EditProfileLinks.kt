package com.neb.ians.ui.screens.profile.edit

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material.icons.outlined.Link
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.neb.ians.R
import com.neb.ians.data.api.ApiSocialLink
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebAuthType
import com.neb.ians.ui.components.NebIconAction
import com.neb.ians.ui.components.NebOutlinePillButton
import com.neb.ians.ui.components.NebPickerSheet
import com.neb.ians.ui.components.NebPillButton
import com.neb.ians.ui.components.NebSheetSurface
import com.neb.ians.ui.screens.auth.CompleteProfileUiState
import com.neb.ians.ui.screens.auth.CompleteProfileViewModel
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.NebAuthTokens

@Composable
internal fun EditLinksSection(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    var showAdd by remember { mutableStateOf(false) }

    EditSection(title = "Links") {
        if (state.socialLinks.isEmpty()) {
            EditInlineHint(text = "No links yet. Add the places people can find you.")
            Spacer(modifier = Modifier.height(14.dp))
        } else {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                state.socialLinks.forEach { link ->
                    EditLinkRow(link = link, onDelete = { viewModel.deleteSocialLink(link.id) })
                }
            }
            Spacer(modifier = Modifier.height(14.dp))
        }

        NebOutlinePillButton(
            text = "Add a link",
            onClick = { showAdd = true },
            leadingIcon = Icons.Outlined.Add
        )
    }

    if (showAdd) {
        EditAddLinkSheet(
            onDismiss = { showAdd = false },
            onAdd = { platform, value, label ->
                viewModel.addSocialLink(platform, value, label)
                showAdd = false
            }
        )
    }
}

@Composable
private fun EditLinkRow(link: ApiSocialLink, onDelete: () -> Unit) {
    val palette = LocalNebAuthPalette.current
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(NebAuthTokens.FieldRadius))
            .background(palette.field)
            .padding(horizontal = 14.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .size(34.dp)
                .clip(CircleShape)
                .background(palette.card),
            contentAlignment = Alignment.Center
        ) {
            val iconRes = socialIconRes(link.platform)
            if (iconRes != null) {
                Icon(
                    painter = painterResource(id = iconRes),
                    contentDescription = null,
                    tint = Color.Unspecified,
                    modifier = Modifier.size(18.dp)
                )
            } else {
                val domain = socialDomainOf(link.url, link.websiteDomain)
                AsyncImage(
                    model = "https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON" +
                        "&fallback_opts=TYPE,SIZE,URL&url=https://$domain&size=64",
                    contentDescription = null,
                    modifier = Modifier.size(18.dp),
                    error = painterResource(R.drawable.ic_globe)
                )
            }
        }

        Spacer(modifier = Modifier.width(12.dp))

        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = link.platformLabel.ifBlank { link.platform.replaceFirstChar { it.uppercase() } },
                style = NebAuthType.Body,
                color = palette.ink,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = link.url,
                style = NebAuthType.Caption,
                color = palette.inkFaint,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }

        Spacer(modifier = Modifier.width(8.dp))

        NebIconAction(
            icon = Icons.Outlined.Close,
            contentDescription = "Remove link",
            onClick = onDelete,
            tint = palette.inkFaint
        )
    }
}

@Composable
private fun EditAddLinkSheet(
    onDismiss: () -> Unit,
    onAdd: (platform: String, value: String, label: String) -> Unit
) {
    val palette = LocalNebAuthPalette.current
    var platform by remember { mutableStateOf(SOCIAL_PLATFORMS.first()) }
    var value by remember { mutableStateOf("") }
    var label by remember { mutableStateOf("") }
    var showPlatforms by remember { mutableStateOf(false) }

    NebSheetSurface(title = "Add a link", onDismiss = onDismiss) {
        EditPickerRowField(
            label = "Platform",
            value = platform.label,
            placeholder = "Choose one",
            onClick = { showPlatforms = true }
        )

        Spacer(modifier = Modifier.height(NebAuthTokens.StackGap))

        NebAuthField(
            value = value,
            onValueChange = { value = it },
            label = platform.fieldLabel,
            placeholder = platform.placeholder,
            leadingIcon = Icons.Outlined.Link,
            helper = platform.help,
            helperTone = palette.inkFaint
        )

        if (platform.key == "website") {
            Spacer(modifier = Modifier.height(NebAuthTokens.StackGap))
            NebAuthField(
                value = label,
                onValueChange = { label = it },
                label = "Label",
                placeholder = "My portfolio"
            )
        }

        Spacer(modifier = Modifier.height(22.dp))

        NebPillButton(
            text = "Add link",
            onClick = { onAdd(platform.key, value.trim(), label.trim()) },
            enabled = value.isNotBlank()
        )
    }

    if (showPlatforms) {
        NebPickerSheet(
            title = "Platform",
            options = SOCIAL_PLATFORMS.map { it.label },
            selected = platform.label,
            onSelect = { picked ->
                platform = SOCIAL_PLATFORMS.first { it.label == picked }
                value = ""
            },
            onDismiss = { showPlatforms = false },
            searchPlaceholder = "Search platforms"
        )
    }
}
