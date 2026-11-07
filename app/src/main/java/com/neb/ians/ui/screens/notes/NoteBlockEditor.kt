@file:OptIn(ExperimentalMaterial3Api::class)

package com.neb.ians.ui.screens.notes

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.Checklist
import androidx.compose.material.icons.outlined.Code
import androidx.compose.material.icons.outlined.FormatBold
import androidx.compose.material.icons.outlined.FormatItalic
import androidx.compose.material.icons.outlined.FormatListBulleted
import androidx.compose.material.icons.outlined.FormatListNumbered
import androidx.compose.material.icons.outlined.FormatQuote
import androidx.compose.material.icons.outlined.FormatStrikethrough
import androidx.compose.material.icons.outlined.Link
import androidx.compose.material.icons.outlined.MoreVert
import androidx.compose.material.icons.outlined.Title
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.Stable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.key
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.input.key.Key
import androidx.compose.ui.input.key.KeyEventType
import androidx.compose.ui.input.key.key
import androidx.compose.ui.input.key.onPreviewKeyEvent
import androidx.compose.ui.input.key.type
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.PopupProperties
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.LiveMarkdown
import com.neb.ians.util.TactileType
import com.neb.ians.util.rememberTactileFeedback

/*
 * The note body: a column of blocks. Every text block is its own field that draws its Markdown live, so a note reads like
 * the finished page while it is being written. Type "/" on an empty line for the block list, press Enter to start the next
 * block, and use the bar above the keyboard to format the selection.
 */

/**
 * Keeps the field state of every text block in one place so the format bar can read and change the selection of the block
 * that has the caret. Text typed in a field is written here first; the view model hears about it right after.
 */
@Stable
class BlockFieldRegistry {
    val values = mutableStateMapOf<String, TextFieldValue>()
    private val sent = HashMap<String, String>()
    var focusedId by mutableStateOf<String?>(null)

    fun valueOf(block: NoteBlock): TextFieldValue = values[block.id] ?: TextFieldValue(block.text, TextRange(block.text.length))

    fun write(vm: NoteEditorViewModel, id: String, nv: TextFieldValue) {
        values[id] = nv
        sent[id] = nv.text
        vm.setText(id, nv.text)
    }

    fun setLocal(id: String, nv: TextFieldValue) {
        values[id] = nv
        sent[id] = nv.text
    }

    /** The block's text changed from outside the field (undo, merge, dictation): adopt it. */
    fun external(id: String, text: String) {
        if (sent[id] != text) {
            sent[id] = text
            values[id] = TextFieldValue(text, TextRange(text.length))
        }
    }
}

@Composable
fun NoteBlockEditor(
    blocks: List<NoteBlock>,
    vm: NoteEditorViewModel,
    registry: BlockFieldRegistry,
    readOnly: Boolean,
    fg: Color,
    modifier: Modifier = Modifier,
) {
    val focusRequest by vm.focusRequest.collectAsStateWithLifecycle()
    val numbers = remember(blocks) {
        var run = 0
        blocks.map { if (it.type == BlockType.Number) ++run else { run = 0; 0 } }
    }
    Column(modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        blocks.forEachIndexed { index, block ->
            key(block.id) {
                when (block.type) {
                    BlockType.Divider -> MediaFrame(block, vm, readOnly, always = false) {
                        Box(Modifier.fillMaxWidth().padding(vertical = 10.dp).height(2.dp).clip(RoundedCornerShape(1.dp)).background(fg.copy(alpha = 0.2f)))
                    }
                    BlockType.Image -> MediaFrame(block, vm, readOnly) { ImageBlockView(block, vm, readOnly) }
                    BlockType.Audio -> MediaFrame(block, vm, readOnly) { AudioBlockView(block, vm, readOnly) }
                    BlockType.Table -> MediaFrame(block, vm, readOnly) { TableBlockView(block, vm, readOnly, fg) }
                    BlockType.Drawing -> MediaFrame(block, vm, readOnly) { DrawingBlockView(block, vm, readOnly) }
                    else -> TextBlockRow(block, numbers[index], blocks.size == 1, vm, registry, readOnly, fg, focusRequest == block.id)
                }
            }
        }
        if (!readOnly) {
            Box(Modifier.fillMaxWidth().height(180.dp).clickable { vm.tapBelow() })
        }
    }
}

/** A media block with its menu pinned top-right. */
@Composable
private fun MediaFrame(block: NoteBlock, vm: NoteEditorViewModel, readOnly: Boolean, always: Boolean = true, content: @Composable () -> Unit) {
    Box(Modifier.fillMaxWidth()) {
        content()
        if (!readOnly && always) Box(Modifier.align(Alignment.TopEnd).padding(4.dp)) { BlockMenuButton(block, vm, onSurface = true) }
    }
}

@Composable
private fun BlockMenuButton(block: NoteBlock, vm: NoteEditorViewModel, onSurface: Boolean = false) {
    val c = MaterialTheme.colorScheme
    var open by remember { mutableStateOf(false) }
    Box {
        Box(
            Modifier.size(32.dp).clip(CircleShape).then(if (onSurface) Modifier.background(c.surface.copy(alpha = 0.85f)) else Modifier).clickable { open = true },
            contentAlignment = Alignment.Center,
        ) { Icon(Icons.Outlined.MoreVert, "Block options", tint = c.onSurfaceVariant, modifier = Modifier.size(20.dp)) }
        DropdownMenu(
            expanded = open, onDismissRequest = { open = false },
            shape = RoundedCornerShape(20.dp), containerColor = c.surfaceContainerHigh, tonalElevation = 0.dp, shadowElevation = 0.dp,
        ) {
            if (block.type.hasText) {
                listOf(BlockType.Text, BlockType.H1, BlockType.H2, BlockType.H3, BlockType.Todo, BlockType.Bullet, BlockType.Number, BlockType.Quote, BlockType.Callout, BlockType.Code).forEach { t ->
                    DropdownMenuItem(
                        text = { Text(t.label, color = if (block.type == t) c.primary else c.onSurface, fontWeight = if (block.type == t) FontWeight.SemiBold else FontWeight.Normal) },
                        onClick = { open = false; vm.convert(block.id, t) },
                    )
                }
            }
            DropdownMenuItem(text = { Text("Move up") }, onClick = { open = false; vm.move(block.id, -1) })
            DropdownMenuItem(text = { Text("Move down") }, onClick = { open = false; vm.move(block.id, 1) })
            DropdownMenuItem(text = { Text("Duplicate") }, onClick = { open = false; vm.duplicate(block.id) })
            DropdownMenuItem(text = { Text("Delete", color = c.error) }, onClick = { open = false; vm.delete(block.id) })
        }
    }
}

@Composable
private fun TextBlockRow(
    block: NoteBlock,
    number: Int,
    onlyBlock: Boolean,
    vm: NoteEditorViewModel,
    registry: BlockFieldRegistry,
    readOnly: Boolean,
    fg: Color,
    wantsFocus: Boolean,
) {
    val c = MaterialTheme.colorScheme
    val type = block.type
    val focusRequester = remember { FocusRequester() }
    var focused by remember { mutableStateOf(false) }
    val live = LiveMarkdown.rememberTransformation()

    LaunchedEffect(block.text) { registry.external(block.id, block.text) }
    LaunchedEffect(wantsFocus) {
        if (wantsFocus) {
            if (vm.caretAtStart) registry.setLocal(block.id, TextFieldValue(block.text, TextRange(0)))
            runCatching { focusRequester.requestFocus() }
            vm.consumeFocus()
        }
    }

    val value = registry.valueOf(block)
    val typo = MaterialTheme.typography
    val done = type == BlockType.Todo && block.checked
    val textColor = when {
        type == BlockType.Callout -> c.onPrimaryContainer
        done -> fg.copy(alpha = 0.5f)
        else -> fg
    }
    val style: TextStyle = when (type) {
        BlockType.H1 -> typo.headlineMedium.copy(fontWeight = FontWeight.SemiBold)
        BlockType.H2 -> typo.titleLarge.copy(fontWeight = FontWeight.SemiBold)
        BlockType.H3 -> typo.titleMedium.copy(fontWeight = FontWeight.SemiBold)
        BlockType.Code -> typo.bodyMedium.copy(fontFamily = FontFamily.Monospace)
        else -> typo.bodyLarge.copy(lineHeight = 26.sp)
    }.copy(color = textColor, textDecoration = if (done) TextDecoration.LineThrough else TextDecoration.None)
    val hint = when (type) {
        BlockType.Text -> if (onlyBlock) "Start writing, or type / for blocks" else if (focused) "Type / for blocks" else ""
        BlockType.H1, BlockType.H2, BlockType.H3 -> "Heading"
        BlockType.Todo -> "To-do"
        BlockType.Bullet, BlockType.Number -> "List"
        BlockType.Quote -> "Quote"
        BlockType.Callout -> "Callout"
        BlockType.Code -> "Code"
        else -> ""
    }
    val slash = if (type == BlockType.Text && block.text.startsWith("/") && !block.text.contains(' ')) {
        val q = block.text.drop(1)
        BlockType.entries.filter { q.isBlank() || it.label.contains(q, true) || it.keywords.contains(q, true) }.take(8)
    } else emptyList()

    val container: Modifier = when (type) {
        BlockType.Callout -> Modifier.clip(RoundedCornerShape(16.dp)).background(c.primaryContainer.copy(alpha = 0.6f)).padding(14.dp)
        BlockType.Code -> Modifier.clip(RoundedCornerShape(14.dp)).background(c.surfaceContainerHighest).padding(12.dp)
        else -> Modifier
    }
    val topPad = when (type) { BlockType.H1 -> 14.dp; BlockType.H2 -> 10.dp; BlockType.H3 -> 6.dp; else -> 0.dp }

    Row(
        Modifier.fillMaxWidth().padding(top = topPad).then(if (type == BlockType.Quote) Modifier.height(IntrinsicSize.Min) else Modifier).then(container),
        verticalAlignment = Alignment.Top,
    ) {
        when (type) {
            BlockType.Bullet -> Text("\u2022", style = style, modifier = Modifier.width(22.dp))
            BlockType.Number -> Text("$number.", style = style, modifier = Modifier.width(30.dp))
            BlockType.Todo -> Box(
                Modifier.padding(top = 3.dp, end = 12.dp).size(22.dp).clip(CircleShape)
                    .then(if (block.checked) Modifier.background(c.primary) else Modifier.border(2.dp, c.outline, CircleShape))
                    .clickable(enabled = !readOnly) { vm.toggleTodo(block.id) },
                contentAlignment = Alignment.Center,
            ) { if (block.checked) Icon(Icons.Outlined.Check, "Done", tint = c.onPrimary, modifier = Modifier.size(14.dp)) }
            BlockType.Quote -> Box(Modifier.padding(end = 12.dp).width(3.dp).fillMaxHeight().clip(RoundedCornerShape(2.dp)).background(c.primary))
            else -> {}
        }
        Box(Modifier.weight(1f)) {
            BasicTextField(
                value = value,
                onValueChange = { nv ->
                    if (type != BlockType.Code && nv.text.contains('\n')) {
                        val parts = nv.text.split('\n')
                        registry.setLocal(block.id, TextFieldValue(parts.first(), TextRange(parts.first().length)))
                        vm.split(block.id, parts.first(), parts.drop(1))
                    } else {
                        registry.write(vm, block.id, nv)
                    }
                },
                readOnly = readOnly,
                textStyle = style,
                cursorBrush = SolidColor(c.primary),
                visualTransformation = if (type == BlockType.Code) VisualTransformation.None else live,
                keyboardOptions = KeyboardOptions(capitalization = if (type == BlockType.Code) KeyboardCapitalization.None else KeyboardCapitalization.Sentences),
                decorationBox = { inner ->
                    Box {
                        if (block.text.isEmpty() && hint.isNotEmpty()) Text(hint, style = style.copy(color = fg.copy(alpha = 0.35f), textDecoration = TextDecoration.None))
                        inner()
                    }
                },
                modifier = Modifier.fillMaxWidth()
                    .focusRequester(focusRequester)
                    .onFocusChanged {
                        focused = it.isFocused
                        if (it.isFocused) { registry.focusedId = block.id; vm.setFocused(block.id) }
                    }
                    .onPreviewKeyEvent { ev ->
                        val sel = registry.valueOf(block).selection
                        if (ev.type == KeyEventType.KeyDown && ev.key == Key.Backspace && sel.collapsed && sel.start == 0 && !readOnly) {
                            vm.backspaceAtStart(block.id); true
                        } else false
                    },
            )
            DropdownMenu(
                expanded = focused && slash.isNotEmpty(), onDismissRequest = {},
                properties = PopupProperties(focusable = false),
                shape = RoundedCornerShape(20.dp), containerColor = c.surfaceContainerHigh, tonalElevation = 0.dp, shadowElevation = 0.dp,
            ) {
                slash.forEach { t -> DropdownMenuItem(text = { Text(t.label) }, onClick = { vm.applySlash(block.id, t) }) }
            }
        }
        if (!readOnly && focused) Box(Modifier.padding(start = 4.dp)) { BlockMenuButton(block, vm) }
    }
}

// ---------------------------------------------------------------------------------------------------- format bar

@Composable
fun BlockFormatBar(
    blocks: List<NoteBlock>,
    vm: NoteEditorViewModel,
    registry: BlockFieldRegistry,
    fg: Color,
    modifier: Modifier = Modifier,
    trailing: @Composable () -> Unit,
) {
    val c = MaterialTheme.colorScheme
    val focusedId = registry.focusedId
    val block = blocks.firstOrNull { it.id == focusedId }
    val value = block?.let { registry.valueOf(it) }
    val canInline = block != null && block.type.hasText && block.type != BlockType.Code
    var insertMenu by remember { mutableStateOf(false) }
    var linkDialog by remember { mutableStateOf(false) }

    fun applyInline(mark: String) {
        if (block != null && value != null && canInline) registry.write(vm, block.id, LiveMarkdown.toggleInline(value, mark))
    }
    fun active(kind: String) = canInline && value != null && LiveMarkdown.isActive(value, kind)
    fun turn(type: BlockType) {
        val id = block?.id ?: vm.focusedId ?: return
        vm.convert(id, type)
    }

    Row(modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
        Row(Modifier.weight(1f).horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(2.dp), verticalAlignment = Alignment.CenterVertically) {
            Box {
                BarButton(Icons.Outlined.Add, "Add a block", fg, false) { insertMenu = true }
                DropdownMenu(
                    expanded = insertMenu, onDismissRequest = { insertMenu = false },
                    shape = RoundedCornerShape(20.dp), containerColor = c.surfaceContainerHigh, tonalElevation = 0.dp, shadowElevation = 0.dp,
                ) {
                    listOf(BlockType.Image, BlockType.Audio, BlockType.Drawing, BlockType.Table, BlockType.Callout, BlockType.Code, BlockType.Divider).forEach { t ->
                        DropdownMenuItem(
                            text = { Text(t.label) },
                            onClick = {
                                insertMenu = false
                                when (t) {
                                    BlockType.Table -> vm.newTable()
                                    BlockType.Callout, BlockType.Code -> vm.insert(t)
                                    else -> vm.insert(t)
                                }
                            },
                        )
                    }
                }
            }
            BarButton(Icons.Outlined.FormatBold, "Bold", fg, active("bold")) { applyInline("**") }
            BarButton(Icons.Outlined.FormatItalic, "Italic", fg, active("italic")) { applyInline("*") }
            BarButton(Icons.Outlined.FormatStrikethrough, "Strikethrough", fg, active("strike")) { applyInline("~~") }
            BarButton(Icons.Outlined.Code, "Inline code", fg, active("code")) { applyInline("`") }
            BarButton(Icons.Outlined.Link, "Link", fg, active("link")) { if (canInline) linkDialog = true }
            BarButton(Icons.Outlined.Title, "Heading", fg, block?.type == BlockType.H2) { turn(BlockType.H2) }
            BarButton(Icons.Outlined.Checklist, "To-do", fg, block?.type == BlockType.Todo) { turn(BlockType.Todo) }
            BarButton(Icons.Outlined.FormatListBulleted, "Bullets", fg, block?.type == BlockType.Bullet) { turn(BlockType.Bullet) }
            BarButton(Icons.Outlined.FormatListNumbered, "Numbers", fg, block?.type == BlockType.Number) { turn(BlockType.Number) }
            BarButton(Icons.Outlined.FormatQuote, "Quote", fg, block?.type == BlockType.Quote) { turn(BlockType.Quote) }
        }
        trailing()
    }

    if (linkDialog && block != null && value != null) {
        var url by remember { mutableStateOf("") }
        AlertDialog(
            onDismissRequest = { linkDialog = false },
            shape = RoundedCornerShape(28.dp), containerColor = c.surfaceContainerHigh,
            title = { Text("Add link") },
            text = { OutlinedTextField(value = url, onValueChange = { url = it }, singleLine = true, shape = RoundedCornerShape(16.dp), placeholder = { Text("Paste a link") }) },
            confirmButton = {
                TextButton(
                    onClick = { registry.write(vm, block.id, LiveMarkdown.insertLink(value, url)); linkDialog = false },
                    enabled = url.isNotBlank(),
                ) { Text("Add") }
            },
            dismissButton = { TextButton(onClick = { linkDialog = false }) { Text("Cancel") } },
        )
    }
}

@Composable
private fun BarButton(icon: ImageVector, label: String, tint: Color, active: Boolean, onClick: () -> Unit) {
    val tactile = rememberTactileFeedback()
    val c = MaterialTheme.colorScheme
    Box(
        Modifier.size(44.dp).clip(RoundedCornerShape(14.dp)).background(if (active) c.primaryContainer else Color.Transparent)
            .clickable { tactile.perform(TactileType.LightTap); onClick() },
        contentAlignment = Alignment.Center,
    ) { Icon(icon, label, tint = if (active) c.onPrimaryContainer else tint, modifier = Modifier.size(22.dp)) }
}
