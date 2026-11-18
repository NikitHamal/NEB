package com.neb.ians.ui.screens.profile.edit

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Palette
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.M3xCover
import com.neb.ians.ui.screens.auth.CompleteProfileUiState
import com.neb.ians.ui.screens.auth.CompleteProfileViewModel
import com.neb.ians.ui.screens.profile.CoverPickerSheet

/** The profile cover as it shows on the profile (a library piece), with one button that opens the picker. */
@Composable
internal fun EditCoverSection(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    val scheme = MaterialTheme.colorScheme
    var picking by remember { mutableStateOf(false) }
    val shape = RoundedCornerShape(24.dp)
    EditSection(title = "Cover") {
        Box(
            Modifier.fillMaxWidth().aspectRatio(3f).clip(shape)
                .border(BorderStroke(1.dp, scheme.outlineVariant), shape)
                .clickable { picking = true }
        ) {
            M3xCover(coverId = state.coverArt, username = state.username, modifier = Modifier.fillMaxSize())
            Row(
                Modifier.align(Alignment.BottomEnd).padding(10.dp)
                    .clip(RoundedCornerShape(20.dp)).background(scheme.surface.copy(alpha = 0.92f))
                    .padding(horizontal = 14.dp, vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Icon(Icons.Outlined.Palette, contentDescription = null, tint = scheme.onSurface, modifier = Modifier.size(18.dp))
                Text("Change cover", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, color = scheme.onSurface)
            }
        }
    }
    if (picking) {
        CoverPickerSheet(
            currentId = state.coverArt.ifBlank { null },
            onPick = { viewModel.setCoverArt(it); picking = false },
            onDefault = { viewModel.setCoverArt(""); picking = false },
            onDismiss = { picking = false }
        )
    }
}
