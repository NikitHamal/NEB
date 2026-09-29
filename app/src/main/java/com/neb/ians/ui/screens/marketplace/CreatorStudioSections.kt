@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class,
    androidx.compose.foundation.ExperimentalFoundationApi::class
)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress
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
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.ArrowDownward
import androidx.compose.material.icons.outlined.ArrowUpward
import androidx.compose.material.icons.outlined.ContentCopy
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.DragIndicator
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.MoreVert
import androidx.compose.material.icons.outlined.Tune
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material.icons.outlined.VisibilityOff
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.zIndex
import com.neb.ians.data.api.ApiCreatorBlock
import com.neb.ians.data.api.ApiCreatorBlockItem
import com.neb.ians.data.api.ApiCreatorChoice
import com.neb.ians.data.api.ApiCreatorSchemaBlock
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebFieldHint
import com.neb.ians.ui.components.WebCardShape

/* The sections half of the studio: the list, the picker and the editor.
 *
 * What went wrong the first time is worth writing down, because it is the whole
 * shape of this file. The old list put five icon buttons on every row -- hide,
 * up, down, delete, edit -- next to the section's name. On a phone that row has
 * about 150dp of room left after the icons, so the name wrapped, and it wrapped
 * one character to a line. A creator opened the builder and saw a column of
 * single letters.
 *
 * So: one handle, one title, one overflow menu. Long-press the handle to drag,
 * or use Move up / Move down in the menu -- a gesture is the fast path and never
 * the only path (WCAG 2.5.1). Everything that needs space gets a bottom sheet,
 * which is the one place on a phone where there is space. */


@Composable
internal fun StudioSectionsCard(
    uiState: CreatorStudioUiState,
    viewModel: CreatorStudioViewModel
) {
    StudioCard {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Text(
                text = "Sections",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.SemiBold,
                modifier = Modifier.weight(1f)
            )
            Text(
                text = "${uiState.blocks.size} of ${uiState.schema.maxBlocks}",
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        NebFieldHint("Your page is these sections, in this order. Hold the handle to drag one, or tap it to edit.")

        StudioBlockList(uiState, viewModel)

        NebButton(
            text = "Add a section",
            onClick = viewModel::openSectionPicker,
            icon = Icons.Outlined.Add,
            tone = NebButtonTone.Tonal,
            size = NebButtonSize.Standard,
            fillWidth = true
        )
        SaveRow(label = "Save sections", saving = uiState.isSavingPage, onSave = viewModel::savePage)
    }
}

/**
 * The reorderable list.
 *
 * Drag is implemented against a measured row height rather than against real
 * layout positions, which is only sound because every row here is the same
 * height by construction — two lines of fixed type inside a fixed 44dp-minimum
 * container. The swap happens at the halfway point, so a row commits its move
 * while the finger is still down and the list underneath is always the order
 * that will be saved.
 */
@Composable
private fun StudioBlockList(
    uiState: CreatorStudioUiState,
    viewModel: CreatorStudioViewModel
) {
    var dragIndex by remember { mutableIntStateOf(-1) }
    var dragOffset by remember { mutableFloatStateOf(0f) }
    var rowHeight by remember { mutableIntStateOf(0) }

    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        uiState.blocks.forEachIndexed { index, block ->
            StudioBlockRow(
                block = block,
                index = index,
                lastIndex = uiState.blocks.lastIndex,
                isDragging = dragIndex == index,
                dragOffset = if (dragIndex == index) dragOffset else 0f,
                onMeasured = { height -> if (rowHeight == 0) rowHeight = height },
                onDragStart = { dragIndex = index; dragOffset = 0f },
                onDrag = { delta ->
                    if (rowHeight > 0) {
                        dragOffset += delta
                        val threshold = rowHeight / 2f
                        // One step per crossing, and the offset is reduced by a
                        // whole row each time so a slow drag across four rows
                        // moves four places rather than one.
                        while (dragOffset > threshold && dragIndex < uiState.blocks.lastIndex) {
                            viewModel.moveBlock(dragIndex, 1)
                            dragIndex += 1
                            dragOffset -= rowHeight
                        }
                        while (dragOffset < -threshold && dragIndex > 0) {
                            viewModel.moveBlock(dragIndex, -1)
                            dragIndex -= 1
                            dragOffset += rowHeight
                        }
                    }
                },
                onDragEnd = { dragIndex = -1; dragOffset = 0f },
                viewModel = viewModel
            )
        }
    }
}

@Composable
private fun StudioBlockRow(
    block: ApiCreatorBlock,
    index: Int,
    lastIndex: Int,
    isDragging: Boolean,
    dragOffset: Float,
    onMeasured: (Int) -> Unit,
    onDragStart: () -> Unit,
    onDrag: (Float) -> Unit,
    onDragEnd: () -> Unit,
    viewModel: CreatorStudioViewModel
) {
    var menuOpen by remember { mutableStateOf(false) }
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .zIndex(if (isDragging) 1f else 0f)
            .graphicsLayer {
                translationY = dragOffset
                // Lifting the row is the only feedback that says "you have hold
                // of this"; without it a long-press drag feels like nothing
                // happened until the list jumps.
                scaleX = if (isDragging) 1.02f else 1f
                scaleY = if (isDragging) 1.02f else 1f
            }
            .onSizeChanged { size -> onMeasured(size.height) }
            .clip(WebCardShape)
            .background(
                if (isDragging) MaterialTheme.colorScheme.secondaryContainer
                else MaterialTheme.colorScheme.surfaceContainer
            )
            .then(
                if (block.enabled) Modifier
                else Modifier.border(1.dp, MaterialTheme.colorScheme.outlineVariant, WebCardShape)
            ),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // The handle. Long-press to drag; the same two moves are in the menu for
        // anybody who cannot or would rather not.
        Box(
            modifier = Modifier
                .size(44.dp)
                .pointerInput(index, lastIndex) {
                    detectDragGesturesAfterLongPress(
                        onDragStart = { onDragStart() },
                        onDragEnd = { onDragEnd() },
                        onDragCancel = { onDragEnd() },
                        onDrag = { _, amount -> onDrag(amount.y) }
                    )
                },
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Outlined.DragIndicator,
                contentDescription = "Drag to reorder ${blockLabel(block.type)}",
                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.size(20.dp)
            )
        }
        // Title and type fill the row and open the editor. A full-height target
        // rather than a pencil icon: the thing a creator wants most often should
        // be the biggest thing to hit.
        Column(
            modifier = Modifier
                .weight(1f)
                .heightIn(min = 44.dp)
                .clickable(onClickLabel = "Edit section") { viewModel.openBlockEditor(index) }
                .padding(vertical = 8.dp),
            verticalArrangement = Arrangement.Center
        ) {
            Text(
                text = block.title.ifBlank { blockLabel(block.type) },
                style = MaterialTheme.typography.bodyLarge,
                fontWeight = FontWeight.SemiBold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Text(
                text = buildString {
                    append(blockLabel(block.type))
                    if (!block.enabled) append(" · Hidden")
                    if (block.items.isNotEmpty()) append(" · ${block.items.size} items")
                    if (block.settings.tone != "plain") append(" · ${block.settings.tone}")
                },
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
        StudioIconButton(
            icon = if (block.enabled) Icons.Outlined.Visibility else Icons.Outlined.VisibilityOff,
            contentDescription = if (block.enabled) "Hide section" else "Show section",
            onClick = { viewModel.toggleBlock(index) }
        )
        // One menu instead of a row of icons. Five icons on a phone either wrap
        // or squeeze the section's name down to a character a line, which is
        // exactly what the old row did.
        Box {
            StudioIconButton(
                icon = Icons.Outlined.MoreVert,
                contentDescription = "More for ${blockLabel(block.type)}",
                onClick = { menuOpen = true }
            )
            DropdownMenu(expanded = menuOpen, onDismissRequest = { menuOpen = false }) {
                DropdownMenuItem(
                    text = { Text("Edit") },
                    leadingIcon = { Icon(Icons.Outlined.Edit, null) },
                    onClick = { menuOpen = false; viewModel.openBlockEditor(index) }
                )
                DropdownMenuItem(
                    text = { Text("Move up") },
                    leadingIcon = { Icon(Icons.Outlined.ArrowUpward, null) },
                    enabled = index > 0,
                    onClick = { menuOpen = false; viewModel.moveBlock(index, -1) }
                )
                DropdownMenuItem(
                    text = { Text("Move down") },
                    leadingIcon = { Icon(Icons.Outlined.ArrowDownward, null) },
                    enabled = index < lastIndex,
                    onClick = { menuOpen = false; viewModel.moveBlock(index, 1) }
                )
                DropdownMenuItem(
                    text = { Text("Duplicate") },
                    leadingIcon = { Icon(Icons.Outlined.ContentCopy, null) },
                    onClick = { menuOpen = false; viewModel.duplicateBlock(index) }
                )
                HorizontalDivider()
                DropdownMenuItem(
                    text = { Text("Remove", color = MaterialTheme.colorScheme.error) },
                    leadingIcon = {
                        Icon(Icons.Outlined.Delete, null, tint = MaterialTheme.colorScheme.error)
                    },
                    onClick = { menuOpen = false; viewModel.removeBlock(index) }
                )
            }
        }
    }
}


/**
 * The picker, as a bottom sheet grouped the way the server groups sections.
 *
 * Twenty-five names in a scrolling chip row is a list nobody reads to the end
 * of. Grouped, with each section's own one-line description under its name, it
 * is a list a creator can actually choose from — "Gallery" tells you nothing,
 * "Photos of your classroom, students and results" tells you whether you want
 * one.
 */
@Composable
internal fun StudioSectionPickerSheet(
    uiState: CreatorStudioUiState,
    viewModel: CreatorStudioViewModel
) {
    if (!uiState.showSectionPicker) return
    val byType = remember(uiState.schema) { uiState.schema.blocks.associateBy { it.type } }
    ModalBottomSheet(
        onDismissRequest = viewModel::closeSectionPicker,
        sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 16.dp)
                .padding(bottom = 28.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            Text(
                text = "Add a section",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold
            )
            uiState.schema.groups.forEach { group ->
                Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text(
                        text = group.label,
                        style = MaterialTheme.typography.labelMedium,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    group.types.forEach { type ->
                        val schemaBlock = byType[type] ?: return@forEach
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(WebCardShape)
                                .background(MaterialTheme.colorScheme.surfaceContainerHigh)
                                .clickable { viewModel.addBlock(type) }
                                .padding(horizontal = 14.dp, vertical = 11.dp),
                            verticalArrangement = Arrangement.spacedBy(2.dp)
                        ) {
                            Text(
                                text = schemaBlock.label,
                                style = MaterialTheme.typography.bodyLarge,
                                fontWeight = FontWeight.SemiBold
                            )
                            Text(
                                text = schemaBlock.hint,
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }
        }
    }
}


/**
 * The section editor, as a bottom sheet built from the schema.
 *
 * The fields are whatever `BLOCK_FIELDS` says the type has, and the item fields
 * whatever `ITEM_FIELDS` says — so all twenty-five section types are editable
 * here, and a section added on the server becomes editable in the app without
 * this composable changing. The old editor hardcoded seven types and silently
 * offered nothing for the rest.
 */
@Composable
internal fun StudioBlockEditorSheet(
    uiState: CreatorStudioUiState,
    viewModel: CreatorStudioViewModel
) {
    val editing = uiState.editingBlock ?: return
    val (index, block) = editing
    val schemaBlock = uiState.schema.blocks.firstOrNull { it.type == block.type }
    ModalBottomSheet(
        onDismissRequest = viewModel::closeBlockEditor,
        sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 16.dp)
                .padding(bottom = 28.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text(
                text = blockLabel(block.type),
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold
            )
            schemaBlock?.hint?.takeIf { it.isNotBlank() }?.let { NebFieldHint(it) }

            schemaBlock?.fields?.forEach { field ->
                StudioBlockField(index, block, field.key, field.label, field.multiline, field.url, viewModel)
            }

            if (schemaBlock?.serverFed == true) {
                NebFieldHint(
                    "This section fills itself from your ${blockLabel(block.type).lowercase()} " +
                        "elsewhere in NEBians. There is nothing to type in here."
                )
            }

            if (schemaBlock?.listKey == "images") {
                StudioImageListEditor(index, block, uiState, viewModel)
            } else if (schemaBlock?.listKey != null) {
                StudioItemListEditor(index, block, schemaBlock, uiState, viewModel)
            }

            HorizontalDivider()
            StudioBlockSettings(index, block, schemaBlock, uiState, viewModel)

            SaveRow(label = "Save section", saving = uiState.isSavingPage, onSave = viewModel::savePage)
            NebButton(
                text = "Done",
                onClick = viewModel::closeBlockEditor,
                tone = NebButtonTone.Text,
                size = NebButtonSize.Small,
                fillWidth = true
            )
        }
    }
}

/** One of the section's own fields, chosen by the schema's key. */
@Composable
private fun StudioBlockField(
    index: Int,
    block: ApiCreatorBlock,
    key: String,
    label: String,
    multiline: Boolean,
    isUrl: Boolean,
    viewModel: CreatorStudioViewModel
) {
    when (key) {
        "title" -> NebAuthField(block.title, { viewModel.updateBlockTitle(index, it) }, label)
        "subtitle" -> NebAuthField(block.subtitle, { viewModel.updateBlockSubtitle(index, it) }, label)
        "body" -> NebAuthField(
            value = block.body,
            onValueChange = { viewModel.updateBlockBody(index, it) },
            label = label,
            singleLine = false,
            minHeight = 120.dp
        )
        "cta_label" -> NebAuthField(block.ctaLabel, { viewModel.updateBlockCtaLabel(index, it) }, label)
        "cta_url" -> NebAuthField(
            value = block.ctaUrl,
            onValueChange = { viewModel.updateBlockCtaUrl(index, it) },
            label = label,
            placeholder = "#contact or https://…",
            helper = "A # link jumps down your own page. Anything else opens in the browser.",
            keyboardType = KeyboardType.Uri
        )
        // A picture field that shows the picture, not a bare "IMAGE URL" box.
        "image_url" -> StudioImageField(
            label = label,
            value = block.imageUrl,
            onValueChange = { viewModel.updateBlockImageUrl(index, it) },
            shape = StudioImageShape.Wide,
            hint = if (block.type == "hero") "Leave this empty to use your cover picture." else null
        )
        "media_url" -> NebAuthField(
            value = block.mediaUrl,
            onValueChange = { viewModel.updateBlockMediaUrl(index, it) },
            label = label,
            placeholder = "https://youtube.com/watch?v=…",
            helper = "YouTube or Vimeo. Other links are shown as a link rather than played.",
            keyboardType = KeyboardType.Uri
        )
        else -> if (multiline) {
            NebAuthField(block.body, { viewModel.updateBlockBody(index, it) }, label, singleLine = false, minHeight = 120.dp)
        } else if (isUrl) {
            NebAuthField(block.ctaUrl, { viewModel.updateBlockCtaUrl(index, it) }, label, keyboardType = KeyboardType.Uri)
        }
    }
}

@Composable
private fun StudioImageListEditor(
    index: Int,
    block: ApiCreatorBlock,
    uiState: CreatorStudioUiState,
    viewModel: CreatorStudioViewModel
) {
    StudioFieldLabel("Pictures")
    NebFieldHint("${block.images.size} in ${uiState.galleryColumns} columns.")
    block.images.forEachIndexed { imageIndex, image ->
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
            Box(modifier = Modifier.weight(1f)) {
                StudioImageField(
                    label = "Picture ${imageIndex + 1}",
                    value = image,
                    onValueChange = { viewModel.updateBlockImage(index, imageIndex, it) },
                    shape = StudioImageShape.Square
                )
            }
            StudioIconButton(
                icon = Icons.Outlined.Delete,
                contentDescription = "Remove picture ${imageIndex + 1}",
                onClick = { viewModel.removeBlockImage(index, imageIndex) },
                tint = MaterialTheme.colorScheme.error
            )
        }
    }
    NebButton(
        text = "Add a picture",
        onClick = { viewModel.addBlockImage(index) },
        icon = Icons.Outlined.Add,
        tone = NebButtonTone.Tonal,
        size = NebButtonSize.Small
    )
}

@Composable
private fun StudioItemListEditor(
    index: Int,
    block: ApiCreatorBlock,
    schemaBlock: ApiCreatorSchemaBlock,
    uiState: CreatorStudioUiState,
    viewModel: CreatorStudioViewModel
) {
    StudioFieldLabel("Items")
    schemaBlock.itemHint.takeIf { it.isNotBlank() }?.let { NebFieldHint(it) }
    block.items.forEachIndexed { itemIndex, item ->
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(WebCardShape)
                .background(MaterialTheme.colorScheme.surfaceContainerHigh)
                .padding(12.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = "${itemIndex + 1}",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.weight(1f)
                )
                StudioIconButton(
                    icon = Icons.Outlined.ArrowUpward,
                    contentDescription = "Move item up",
                    enabled = itemIndex > 0,
                    onClick = { viewModel.moveBlockItem(index, itemIndex, -1) }
                )
                StudioIconButton(
                    icon = Icons.Outlined.ArrowDownward,
                    contentDescription = "Move item down",
                    enabled = itemIndex < block.items.lastIndex,
                    onClick = { viewModel.moveBlockItem(index, itemIndex, 1) }
                )
                StudioIconButton(
                    icon = Icons.Outlined.Delete,
                    contentDescription = "Remove item ${itemIndex + 1}",
                    onClick = { viewModel.removeBlockItem(index, itemIndex) },
                    tint = MaterialTheme.colorScheme.error
                )
            }
            schemaBlock.itemFields.forEach { field ->
                val value = itemValue(item, field.key)
                if (field.url && (field.key == "image_url" || field.key == "avatar_url")) {
                    StudioImageField(
                        label = field.label,
                        value = value,
                        onValueChange = { next ->
                            viewModel.updateBlockItem(index, itemIndex) { setItemValue(it, field.key, next) }
                        },
                        shape = if (field.key == "avatar_url") StudioImageShape.Round else StudioImageShape.Square
                    )
                } else {
                    NebAuthField(
                        value = value,
                        onValueChange = { next ->
                            viewModel.updateBlockItem(index, itemIndex) { setItemValue(it, field.key, next) }
                        },
                        label = field.label,
                        singleLine = !field.multiline,
                        minHeight = if (field.multiline) 96.dp else 56.dp,
                        keyboardType = if (field.url) KeyboardType.Uri else KeyboardType.Text,
                        helper = if (field.key == "features") "One benefit per line." else null
                    )
                }
            }
        }
    }
    if (block.items.size < uiState.schema.maxItems) {
        NebButton(
            text = "Add an item",
            onClick = { viewModel.addBlockItem(index) },
            icon = Icons.Outlined.Add,
            tone = NebButtonTone.Tonal,
            size = NebButtonSize.Small
        )
    } else {
        NebFieldHint("That is the ${uiState.schema.maxItems} items a section holds.")
    }
}

/**
 * A section's own look.
 *
 * These four are what let one page have a centred quote on the accent between
 * two plain left-aligned shelves, instead of every section looking like every
 * other section. A value left at its default is not sent at all — same rule as
 * `sanitize_block_settings` on the server — so a creator who never opens this
 * saves exactly what they always did.
 */
@Composable
private fun StudioBlockSettings(
    index: Int,
    block: ApiCreatorBlock,
    schemaBlock: ApiCreatorSchemaBlock?,
    uiState: CreatorStudioUiState,
    viewModel: CreatorStudioViewModel
) {
    val theme = uiState.schema.theme
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        Icon(
            imageVector = Icons.Outlined.Tune,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.size(17.dp)
        )
        Text(
            text = "This section's look",
            style = MaterialTheme.typography.titleSmall,
            fontWeight = FontWeight.SemiBold
        )
    }
    StudioSegmented(
        label = "Text alignment",
        options = theme.blockAligns.ifEmpty {
            listOf(ApiCreatorChoice("start", "Start"), ApiCreatorChoice("center", "Center"))
        },
        selected = block.settings.align,
        onSelect = { viewModel.updateBlockAlign(index, it) }
    )
    StudioSegmented(
        label = "Background",
        options = theme.blockTones,
        selected = block.settings.tone,
        onSelect = { viewModel.updateBlockTone(index, it) }
    )
    StudioSegmented(
        label = "Width",
        options = theme.blockWidths,
        selected = block.settings.width,
        onSelect = { viewModel.updateBlockWidth(index, it) }
    )
    if (schemaBlock?.listKey != null && schemaBlock.listKey != "images") {
        StudioSegmentedValues(
            label = "Columns",
            options = listOf("0" to "Auto", "1" to "1", "2" to "2", "3" to "3", "4" to "4"),
            selected = block.settings.columns.toString(),
            onSelect = { value -> viewModel.updateBlockColumns(index, value.toIntOrNull() ?: 0) },
            hint = "Auto fits as many as the screen has room for."
        )
    }
}


/* Item fields are addressed by the server's key rather than by a Kotlin
 * property, so the editor above can render whatever `ITEM_FIELDS` lists without
 * a `when` per section type. These two functions are the only place the mapping
 * lives. */

private fun itemValue(item: ApiCreatorBlockItem, key: String): String = when (key) {
    "label" -> item.label
    "value" -> item.value
    "icon" -> item.icon
    "title" -> item.title
    "subtitle" -> item.subtitle
    "image_url" -> item.imageUrl
    "link_url" -> item.linkUrl
    "badge" -> item.badge
    "name" -> item.name
    "role" -> item.role
    "quote" -> item.quote
    "avatar_url" -> item.avatarUrl
    "q" -> item.q
    "a" -> item.a
    "day" -> item.day
    "time" -> item.time
    "note" -> item.note
    "url" -> item.url
    "price" -> item.price
    "period" -> item.period
    "features" -> item.features
    "cta_label" -> item.ctaLabel
    "cta_url" -> item.ctaUrl
    else -> ""
}

private fun setItemValue(item: ApiCreatorBlockItem, key: String, value: String): ApiCreatorBlockItem =
    when (key) {
        "label" -> item.copy(label = value)
        "value" -> item.copy(value = value)
        "icon" -> item.copy(icon = value)
        "title" -> item.copy(title = value)
        "subtitle" -> item.copy(subtitle = value)
        "image_url" -> item.copy(imageUrl = value)
        "link_url" -> item.copy(linkUrl = value)
        "badge" -> item.copy(badge = value)
        "name" -> item.copy(name = value)
        "role" -> item.copy(role = value)
        "quote" -> item.copy(quote = value)
        "avatar_url" -> item.copy(avatarUrl = value)
        "q" -> item.copy(q = value)
        "a" -> item.copy(a = value)
        "day" -> item.copy(day = value)
        "time" -> item.copy(time = value)
        "note" -> item.copy(note = value)
        "url" -> item.copy(url = value)
        "price" -> item.copy(price = value)
        "period" -> item.copy(period = value)
        "features" -> item.copy(features = value)
        "cta_label" -> item.copy(ctaLabel = value)
        "cta_url" -> item.copy(ctaUrl = value)
        else -> item
    }
