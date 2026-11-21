@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.upload

import androidx.compose.ui.graphics.luminance
import androidx.compose.animation.AnimatedVisibility
import com.neb.ians.ui.components.boundedWidth
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.layout.offset
import androidx.compose.material3.MaterialShapes
import androidx.compose.runtime.getValue
import androidx.graphics.shapes.RoundedPolygon
import com.neb.ians.ui.components.NebMorphBlob
import com.neb.ians.ui.components.NebShapedBox
import com.neb.ians.ui.components.NebTone
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.Description
import androidx.compose.material.icons.rounded.FolderOpen
import androidx.compose.material.icons.rounded.Link
import androidx.compose.material.icons.rounded.PhotoCamera
import androidx.compose.material.icons.rounded.PhotoLibrary
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.neb.ians.ui.components.nebPressable

/**
 * Where the upload comes from.
 *
 * This is the first thing on the screen because it is the thing the user has
 * already done — they have the photos, they came here to hand them over. The
 * old wizard put the file picker on step two, behind a form, which meant the
 * work they had finished was the part they had to wait to do.
 */
@Composable
fun UploadSourceSection(
    state: UploadFormState,
    onCapturePages: () -> Unit,
    onPickPhotos: () -> Unit,
    onPickFiles: () -> Unit,
    onUseLink: () -> Unit,
    onRemovePage: (Int) -> Unit,
    onCombineChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        if (state.selectedFiles.isEmpty()) {
            EmptySource(
                isEditMode = state.isEditMode,
                currentFileLabel = state.currentFileLabel,
                onCapturePages = onCapturePages,
                onPickPhotos = onPickPhotos,
                onPickFiles = onPickFiles,
                onUseLink = onUseLink
            )
        } else {
            PageStrip(
                files = state.selectedFiles,
                onAdd = if (state.isEditMode) onPickFiles else onCapturePages,
                onRemove = onRemovePage
            )
            SourceSummary(state)
            AnimatedVisibility(visible = state.isPageSet) {
                CombineToggle(
                    combine = state.combinePages,
                    pageCount = state.selectedFiles.size,
                    onChange = onCombineChange
                )
            }
        }
    }
}

@Composable
private fun EmptySource(
    isEditMode: Boolean,
    currentFileLabel: String,
    onCapturePages: () -> Unit,
    onPickPhotos: () -> Unit,
    onPickFiles: () -> Unit,
    onUseLink: () -> Unit
) {
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        if (isEditMode && currentFileLabel.isNotBlank()) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(18.dp))
                    .background(MaterialTheme.colorScheme.surfaceContainerLow)
                    .padding(14.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Icon(
                    imageVector = Icons.Rounded.Description,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Column(Modifier.weight(1f)) {
                    Text("Currently attached", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Text(currentFileLabel, style = MaterialTheme.typography.bodyLarge, maxLines = 1, overflow = TextOverflow.Ellipsis)
                }
            }
        }

        SourceHero(
            icon = Icons.Rounded.PhotoCamera,
            label = "Scan pages",
            onClick = onCapturePages
        )

        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
            SourceTile(
                icon = Icons.Rounded.PhotoLibrary,
                label = "Gallery",
                tone = NebTone.Sky,
                glyph = MaterialShapes.Cookie9Sided,
                onClick = onPickPhotos,
                modifier = Modifier.weight(1f)
            )
            SourceTile(
                icon = Icons.Rounded.FolderOpen,
                label = "Files",
                tone = NebTone.Aqua,
                glyph = MaterialShapes.Gem,
                onClick = onPickFiles,
                modifier = Modifier.weight(1f)
            )
        }

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .nebPressable(onClick = onUseLink)
                .clip(RoundedCornerShape(16.dp))
                .padding(vertical = 10.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = Icons.Rounded.Link,
                contentDescription = null,
                modifier = Modifier.size(18.dp),
                tint = MaterialTheme.colorScheme.primary
            )
            Text(
                text = "Share a link instead",
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary
            )
        }
    }
}

private const val SourceHeroHeight = 196

/**
 * The tile that does the thing most people came here to do.
 *
 * It runs the full width and a shape keeps turning into other shapes behind its
 * label, because scanning a set of pages is the upload this app exists for. The
 * two quieter tiles under it are the same family in other tones.
 */
@Composable
private fun SourceHero(
    icon: ImageVector,
    label: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val dark = androidx.compose.material3.MaterialTheme.colorScheme.surface.luminance() < 0.5f
    val tone = NebTone.Azure
    val transition = rememberInfiniteTransition(label = "source_hero")
    val position by transition.animateFloat(
        initialValue = 0f,
        targetValue = HeroShapes.size - 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 5200, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "source_hero_morph"
    )
    val turn by transition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 20000, easing = LinearEasing)
        ),
        label = "source_hero_turn"
    )
    Box(
        modifier = modifier
            .fillMaxWidth()
            .height(SourceHeroHeight.dp)
            .nebPressable(onClick = onClick)
            .clip(RoundedCornerShape(32.dp))
            .background(tone.container(dark))
    ) {
        NebMorphBlob(
            shapes = HeroShapes,
            color = tone.vivid.copy(alpha = if (dark) 0.34f else 0.62f),
            modifier = Modifier
                .align(Alignment.CenterEnd)
                .offset(x = 64.dp)
                .size(240.dp),
            rotation = { turn },
            position = { position }
        )
        Column(
            modifier = Modifier
                .align(Alignment.BottomStart)
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            NebShapedBox(
                polygon = MaterialShapes.Clover4Leaf,
                diameter = 56.dp,
                fill = tone.deep(dark)
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = tone.container(dark),
                    modifier = Modifier.size(26.dp)
                )
            }
            Text(
                text = label,
                style = MaterialTheme.typography.headlineSmallEmphasized,
                color = tone.deep(dark),
                maxLines = 1
            )
        }
    }
}

private val HeroShapes by lazy {
    listOf(MaterialShapes.Cookie9Sided, MaterialShapes.SoftBurst, MaterialShapes.Flower)
}

/** Gallery and Files: one line each, a glyph cut to its own shape, a tone of its own. */
@Composable
private fun SourceTile(
    icon: ImageVector,
    label: String,
    tone: NebTone,
    glyph: RoundedPolygon,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val dark = androidx.compose.material3.MaterialTheme.colorScheme.surface.luminance() < 0.5f
    Row(
        modifier = modifier
            .height(84.dp)
            .nebPressable(onClick = onClick)
            .clip(RoundedCornerShape(28.dp))
            .background(tone.container(dark))
            .padding(horizontal = 14.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        NebShapedBox(polygon = glyph, diameter = 42.dp, fill = tone.deep(dark)) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = tone.container(dark),
                modifier = Modifier.size(20.dp)
            )
        }
        Text(
            text = label,
            style = MaterialTheme.typography.titleSmallEmphasized,
            color = tone.deep(dark),
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

/**
 * The pages, in order, with the next one always one tap away.
 *
 * Somebody photographing a hundred pages needs to see that page ninety-nine
 * landed and reach page one hundred without leaving the screen, so the add tile
 * lives at the end of the same strip.
 */
@Composable
private fun PageStrip(
    files: List<SelectedFile>,
    onAdd: () -> Unit,
    onRemove: (Int) -> Unit
) {
    LazyRow(
        modifier = Modifier.fillMaxWidth().boundedWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        contentPadding = PaddingValues(end = 4.dp)
    ) {
        itemsIndexed(files, key = { _, file -> file.uri.toString() }, contentType = { _, _ -> "page_tile" }) { index, file ->
            PageTile(
                file = file,
                index = index,
                onRemove = { onRemove(index) },
                modifier = Modifier.animateItem()
            )
        }
        item(key = "add", contentType = "add_tile") {
            Column(
                modifier = Modifier
                    .animateItem()
                    .width(96.dp)
                    .height(128.dp)
                    .nebPressable(onClick = onAdd)
                    .clip(RoundedCornerShape(18.dp))
                    .background(MaterialTheme.colorScheme.secondaryContainer),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Icon(
                    imageVector = Icons.Rounded.Add,
                    contentDescription = "Add more pages",
                    tint = MaterialTheme.colorScheme.onSecondaryContainer
                )
                Text(
                    text = "Add",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSecondaryContainer
                )
            }
        }
    }
}

@Composable
private fun PageTile(file: SelectedFile, index: Int, onRemove: () -> Unit, modifier: Modifier = Modifier) {
    Box(
        modifier = modifier
            .width(96.dp)
            .height(128.dp)
            .clip(RoundedCornerShape(18.dp))
            .background(MaterialTheme.colorScheme.surfaceContainerHigh)
    ) {
        if (file.isImage) {
            AsyncImage(
                model = file.uri,
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize()
            )
        } else {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(10.dp),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Icon(
                    imageVector = Icons.Rounded.Description,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = file.name,
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    textAlign = TextAlign.Center,
                    maxLines = 3,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }

        Text(
            text = "${index + 1}",
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.surface,
            modifier = Modifier
                .align(Alignment.BottomStart)
                .padding(6.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.72f))
                .padding(horizontal = 7.dp, vertical = 2.dp)
        )

        Box(
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(6.dp)
                .size(24.dp)
                .nebPressable(onClick = onRemove)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.72f)),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Rounded.Close,
                contentDescription = "Remove page ${index + 1}",
                tint = MaterialTheme.colorScheme.surface,
                modifier = Modifier.size(14.dp)
            )
        }
    }
}

@Composable
private fun SourceSummary(state: UploadFormState) {
    val files = state.selectedFiles
    val totalSize = files.sumOf { it.size }
    val label = when {
        state.willCombine -> "${files.size} pages, one PDF, ${formatFileSize(totalSize)} before shrinking"
        files.size == 1 -> "${files.first().name}  —  ${formatFileSize(totalSize)}"
        else -> "${files.size} files  —  ${formatFileSize(totalSize)}"
    }
    Text(
        text = label,
        style = MaterialTheme.typography.bodySmall,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
        maxLines = 2,
        overflow = TextOverflow.Ellipsis
    )
}

@Composable
private fun CombineToggle(combine: Boolean, pageCount: Int, onChange: (Boolean) -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(18.dp))
            .background(MaterialTheme.colorScheme.surfaceContainerLow)
            .padding(horizontal = 14.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Column(Modifier.weight(1f)) {
            Text("Publish as one document", style = MaterialTheme.typography.bodyLarge)
            Text(
                text = if (combine) {
                    "$pageCount pages become a single PDF"
                } else {
                    "$pageCount separate resources will be created"
                },
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        Switch(checked = combine, onCheckedChange = onChange)
    }
}

/** Kept for the cover preview, which is the one square image on the screen. */
@Composable
fun CoverPreview(model: Any?, modifier: Modifier = Modifier) {
    if (model == null) return
    AsyncImage(
        model = model,
        contentDescription = "Cover image",
        contentScale = ContentScale.Crop,
        modifier = modifier
            .fillMaxWidth()
            .aspectRatio(16f / 9f)
            .clip(RoundedCornerShape(18.dp))
    )
}
