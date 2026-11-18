package com.neb.ians.ui.screens.profile.edit

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.asPaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.ui.draw.drawBehind
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.AddAPhoto
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
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.Avatar
import com.neb.ians.ui.components.M3xCover
import com.neb.ians.ui.components.NebAuthType
import com.neb.ians.ui.components.NebLoadingIndicator
import com.neb.ians.ui.components.NebProgressRail
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.components.profileCoverHeight
import com.neb.ians.ui.screens.auth.CompleteProfileUiState
import com.neb.ians.ui.screens.auth.CompleteProfileViewModel
import com.neb.ians.ui.screens.profile.CoverPickerSheet
import com.neb.ians.ui.theme.LocalNebAuthPalette

private val AvatarSize = 104.dp

/**
 * The top of the editor, built like the profile it edits: the cover runs edge to edge (behind the status bar, at the same
 * proportions as the profile so what you see is what they see), the photo hangs across its bottom edge in the middle, and
 * the name, handle and strength sit under it. Back and Save live in [EditProfileTopBar], which stays on screen while the page scrolls. Nothing here has a shadow or a ring.
 */
@Composable
internal fun EditProfileHero(
    state: CompleteProfileUiState,
    viewModel: CompleteProfileViewModel,
    strength: Float,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    val palette = LocalNebAuthPalette.current
    var picking by remember { mutableStateOf(false) }
    val statusTop = WindowInsets.statusBars.asPaddingValues().calculateTopPadding()

    Column(modifier.fillMaxWidth()) {
        BoxWithConstraints(Modifier.fillMaxWidth()) {
            val coverHeight = profileCoverHeight(maxWidth, statusTop)
            Box(Modifier.fillMaxWidth().padding(top = statusTop).height(coverHeight)) {
                M3xCover(
                    coverId = state.coverArt, username = state.username.ifBlank { state.displayName },
                    modifier = Modifier.fillMaxSize().clickable(role = Role.Button) { picking = true },
                    live = true
                )
                Row(
                    Modifier.align(Alignment.BottomEnd).padding(end = 12.dp, bottom = 12.dp)
                        .clip(RoundedCornerShape(20.dp)).background(scheme.surface.copy(alpha = 0.92f))
                        .clickable(role = Role.Button) { picking = true }
                        .padding(horizontal = 14.dp, vertical = 9.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Icon(Icons.Outlined.Palette, contentDescription = null, tint = scheme.onSurface, modifier = Modifier.size(18.dp))
                    Text("Change", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, color = scheme.onSurface, maxLines = 1)
                }
            }
            Box(
                Modifier.align(Alignment.BottomCenter).offset(y = AvatarSize / 2).size(AvatarSize)
                    .nebPressable(scale = 0.95f, onClick = viewModel::openPhotoGallery)
            ) {
                Avatar(
                    name = state.displayName.ifBlank { state.username }, imageUrl = state.photoUrl.ifBlank { null },
                    size = AvatarSize, modifier = Modifier.fillMaxSize()
                )
                if (state.isPhotoUploading) {
                    Box(Modifier.fillMaxSize().background(palette.page.copy(alpha = 0.7f)), contentAlignment = Alignment.Center) {
                        NebLoadingIndicator(modifier = Modifier.size(28.dp), color = palette.accent)
                    }
                }
                Box(
                    Modifier.align(Alignment.BottomEnd).size(34.dp).clip(CircleShape).background(palette.accent),
                    contentAlignment = Alignment.Center
                ) { Icon(Icons.Outlined.AddAPhoto, contentDescription = "Change photo", tint = palette.onAccent, modifier = Modifier.size(17.dp)) }
            }
        }

        Spacer(Modifier.height(AvatarSize / 2 + 12.dp))
        Column(Modifier.fillMaxWidth().padding(horizontal = 24.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Text(
                text = state.displayName.ifBlank { "Your name" }, style = NebAuthType.Title,
                color = if (state.displayName.isBlank()) palette.inkFaint else palette.ink, maxLines = 1
            )
            Spacer(Modifier.height(2.dp))
            Text(text = "@" + state.username.ifBlank { "username" }, style = NebAuthType.Caption, color = palette.accent)
            Spacer(Modifier.height(18.dp))
            Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                Text("Profile strength", style = NebAuthType.Caption, color = palette.inkMuted, maxLines = 1)
                Spacer(Modifier.weight(1f))
                Text("${(strength * 100).toInt()}%", style = NebAuthType.Caption, color = palette.accent, maxLines = 1)
            }
            Spacer(Modifier.height(8.dp))
            NebProgressRail(progress = strength)
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

/**
 * Back and Save, pinned to the top of the screen. Over the cover they float on it; as the page scrolls the bar's own surface
 * fades in (progress 0 to 1, read only while drawing) so the buttons never sit on text.
 */
@Composable
internal fun EditProfileTopBar(
    progress: () -> Float,
    canSave: Boolean,
    onBack: () -> Unit,
    onSave: () -> Unit,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    val line = scheme.outlineVariant
    Row(
        modifier.fillMaxWidth()
            .drawBehind {
                val p = progress()
                if (p > 0f) {
                    drawRect(scheme.surface.copy(alpha = p))
                    drawRect(line.copy(alpha = p), topLeft = androidx.compose.ui.geometry.Offset(0f, size.height - 1.dp.toPx()), size = androidx.compose.ui.geometry.Size(size.width, 1.dp.toPx()))
                }
            }
            .windowInsetsPadding(WindowInsets.statusBars)
            .padding(horizontal = 12.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        HeroButton(modifier = Modifier, onClick = onBack) {
            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = scheme.onSurface, modifier = Modifier.size(22.dp))
        }
        Spacer(Modifier.weight(1f))
        Box(
            Modifier.height(44.dp)
                .clip(RoundedCornerShape(22.dp))
                .background(scheme.surface.copy(alpha = if (canSave) 0.92f else 0.6f))
                .clickable(enabled = canSave, role = Role.Button, onClick = onSave)
                .padding(horizontal = 20.dp),
            contentAlignment = Alignment.Center
        ) {
            Text("Save", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, color = if (canSave) scheme.primary else scheme.onSurfaceVariant)
        }
    }
}

/** Scroll distance (px) after which the top bar is fully solid: the cover's lower edge has slid under it. */
internal fun editBarRange(coverPx: Float, barPx: Float): Float = (coverPx - barPx).coerceAtLeast(1f)

@Composable
private fun HeroButton(modifier: Modifier, onClick: () -> Unit, content: @Composable () -> Unit) {
    Box(
        modifier.size(44.dp).clip(RoundedCornerShape(22.dp))
            .background(MaterialTheme.colorScheme.surface.copy(alpha = 0.92f))
            .clickable(role = Role.Button, onClick = onClick),
        contentAlignment = Alignment.Center
    ) { content() }
}
