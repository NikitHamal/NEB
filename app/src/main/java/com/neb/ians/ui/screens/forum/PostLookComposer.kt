package com.neb.ians.ui.screens.forum

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.AutoAwesome
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material.icons.outlined.Image
import androidx.compose.material.icons.outlined.Palette
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.PostLook
import com.neb.ians.ui.components.PostLookCover
import com.neb.ians.ui.components.nebHorizontalScroll
import com.neb.ians.ui.screens.notes.NoteCoverSheet
import com.neb.ians.ui.screens.notes.NoteIconSheet
import com.neb.ians.ui.screens.notes.NoteSheet
import com.neb.ians.ui.screens.notes.NoteThemeRow
import com.neb.ians.ui.screens.notes.PaperPicker
import com.neb.ians.ui.screens.notes.ToneSwatches

/** Which appearance sheet is open in the post composer. */
internal enum class LookSheet { Style, Icon, Cover }

/**
 * The top of a dynamic post page in the composer: the cover with its icon, and one row of
 * chips to add, change or remove each of them. Shows only the chips until something is set.
 */
@Composable
internal fun ComposerLookHeader(
    look: PostLook,
    coverUri: android.net.Uri?,
    onSheet: (LookSheet) -> Unit,
    viewModel: CreatePostViewModel,
) {
    val hasPhoto = coverUri != null || look.photo > 0
    val hasCover = hasPhoto || look.cover > 0
    val hasIcon = look.icon.isNotEmpty()
    Column(Modifier.fillMaxWidth()) {
        if (hasCover || hasIcon) {
            Box(Modifier.fillMaxWidth()) {
                PostLookCover(look, coverHeight = 132.dp, iconSize = 60.dp, animate = true, pendingPhoto = coverUri)
            }
        }
        Row(
            Modifier.fillMaxWidth().nebHorizontalScroll(rememberScrollState()).padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            LookChip(if (hasCover) "Change cover" else "Add cover", Icons.Outlined.Image) { onSheet(LookSheet.Cover) }
            LookChip(if (hasIcon) "Change icon" else "Add icon", Icons.Outlined.AutoAwesome) { onSheet(LookSheet.Icon) }
            LookChip("Style", Icons.Outlined.Palette) { onSheet(LookSheet.Style) }
            if (hasCover) LookChip("Remove cover", Icons.Outlined.Close) { viewModel.clearCover() }
            if (hasIcon) LookChip("Remove icon", Icons.Outlined.Close) { viewModel.setLook(look.copy(icon = "")) }
        }
    }
}

@Composable
private fun LookChip(label: String, icon: ImageVector, onClick: () -> Unit) {
    val c = MaterialTheme.colorScheme
    Row(
        Modifier.height(38.dp).clip(RoundedCornerShape(19.dp)).background(c.secondaryContainer)
            .clickable(onClick = onClick).padding(horizontal = 14.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        Icon(icon, null, tint = c.onSecondaryContainer, modifier = Modifier.size(18.dp))
        Text(label, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, color = c.onSecondaryContainer, maxLines = 1)
    }
}

/** Add, change or remove the picture behind the page. The pick stays on the phone until the post is published. */
@Composable
private fun PagePictureRow(has: Boolean, onPhoto: (android.net.Uri) -> Unit, onRemove: () -> Unit) {
    val gallery = androidx.activity.compose.rememberLauncherForActivityResult(
        androidx.activity.result.contract.ActivityResultContracts.PickVisualMedia(),
    ) { uri -> if (uri != null) onPhoto(uri) }
    Row(Modifier.fillMaxWidth().padding(top = 6.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        LookChip(if (has) "Change picture" else "Add picture", Icons.Outlined.Image) {
            gallery.launch(androidx.activity.result.PickVisualMediaRequest(androidx.activity.result.contract.ActivityResultContracts.PickVisualMedia.ImageOnly))
        }
        if (has) LookChip("Remove", Icons.Outlined.Close, onRemove)
    }
}

@Composable
private fun SectionLabel(text: String) {
    Text(
        text, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold,
        color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(top = 14.dp, bottom = 2.dp),
    )
}

/** The three appearance sheets, the same ones a note uses. */
@Composable
internal fun PostLookSheets(
    sheet: LookSheet?,
    state: CreatePostUiState,
    viewModel: CreatePostViewModel,
    onDismiss: () -> Unit,
) {
    val look = state.look
    when (sheet) {
        LookSheet.Icon -> NoteIconSheet(
            current = look.icon,
            onPick = { viewModel.setLook(look.copy(icon = it)); onDismiss() },
            onDismiss = onDismiss,
        )
        LookSheet.Cover -> NoteCoverSheet(
            current = if (state.coverUri != null || look.photo > 0) -1 else look.cover,
            onPick = { i -> if (i == 0) viewModel.clearCover() else viewModel.setLook(look.copy(cover = i, photo = 0)); onDismiss() },
            onPhoto = { uri -> viewModel.setCoverPhoto(uri); onDismiss() },
            onDismiss = onDismiss,
        )
        LookSheet.Style -> NoteSheet(onDismiss = onDismiss, title = "Appearance") {
            Column(Modifier.heightIn(max = 560.dp).verticalScroll(rememberScrollState())) {
                SectionLabel("Themes")
                NoteThemeRow(look.tone) { th ->
                    viewModel.setLook(look.copy(tone = th.tone, cover = th.cover, photo = 0, icon = th.icon, paper = th.paper))
                }
                SectionLabel("Page colour")
                ToneSwatches(look.tone) { viewModel.setLook(look.copy(tone = it)) }
                SectionLabel("Paper")
                PaperPicker(look.paper) { viewModel.setLook(look.copy(paper = it)) }
                SectionLabel("Page picture")
                PagePictureRow(has = state.bgUri != null || look.bg > 0, onPhoto = viewModel::setBgPhoto, onRemove = viewModel::clearBg)
                SectionLabel("Type")
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    PostLook.fontLabels.forEachIndexed { index, label ->
                        val on = look.font == index
                        val c = MaterialTheme.colorScheme
                        Box(
                            Modifier.height(44.dp).clip(RoundedCornerShape(22.dp))
                                .background(if (on) c.secondaryContainer else c.surfaceContainerHigh)
                                .clickable { viewModel.setLook(look.copy(font = index)) }
                                .padding(horizontal = 20.dp),
                            contentAlignment = Alignment.Center,
                        ) {
                            Text(
                                label, style = MaterialTheme.typography.labelLarge,
                                color = if (on) c.onSecondaryContainer else c.onSurface,
                                fontFamily = when (index) {
                                    PostLook.FONT_SERIF -> androidx.compose.ui.text.font.FontFamily.Serif
                                    PostLook.FONT_MONO -> androidx.compose.ui.text.font.FontFamily.Monospace
                                    else -> null
                                },
                            )
                        }
                    }
                }
                if (!look.isPlain || state.coverUri != null || state.bgUri != null) {
                    Box(
                        Modifier.padding(top = 18.dp).height(48.dp).clip(RoundedCornerShape(24.dp))
                            .background(MaterialTheme.colorScheme.surfaceContainerHigh)
                            .clickable { viewModel.clearLookAll() }
                            .padding(horizontal = 22.dp),
                        contentAlignment = Alignment.Center,
                    ) { Text("Back to a plain post", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurface) }
                }
                Box(Modifier.height(20.dp))
            }
        }
        null -> Unit
    }
}
