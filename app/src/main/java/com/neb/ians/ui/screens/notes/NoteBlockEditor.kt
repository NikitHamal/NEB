@file:OptIn(ExperimentalMaterial3Api::class, androidx.compose.foundation.layout.ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.notes

import com.neb.ians.ui.components.Fmt
import com.neb.ians.ui.components.RichTextField
import androidx.compose.ui.graphics.luminance
import com.neb.ians.ui.components.RichState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.spring
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Spacer
import androidx.compose.material.icons.outlined.ArrowUpward
import androidx.compose.material.icons.outlined.ArrowDownward
import androidx.compose.material.icons.outlined.ContentCopy
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.MoreHoriz
import androidx.compose.material.icons.outlined.KeyboardArrowDown
import androidx.compose.material.icons.outlined.AddPhotoAlternate
import com.neb.ians.ui.components.NebModalSheet
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import com.neb.ians.ui.components.nebHorizontalScroll
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
import androidx.compose.foundation.ScrollState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.ChevronRight
import androidx.compose.material.icons.outlined.FormatIndentDecrease
import androidx.compose.material.icons.outlined.FormatIndentIncrease
import androidx.compose.material.icons.outlined.HorizontalRule
import androidx.compose.material.icons.outlined.Image
import androidx.compose.material.icons.outlined.Lightbulb
import androidx.compose.material.icons.outlined.Mic
import androidx.compose.material.icons.outlined.Notes
import androidx.compose.material.icons.outlined.TableChart
import androidx.compose.material.icons.outlined.Draw
import androidx.compose.material.icons.outlined.Checklist
import androidx.compose.material.icons.outlined.Code
import androidx.compose.material.icons.outlined.FormatBold
import androidx.compose.material.icons.outlined.FormatItalic
import androidx.compose.material.icons.outlined.FormatListBulleted
import androidx.compose.material.icons.outlined.FormatListNumbered
import androidx.compose.material.icons.outlined.FormatQuote
import androidx.compose.material.icons.outlined.FormatStrikethrough
import androidx.compose.material.icons.outlined.Event
import androidx.compose.material.icons.outlined.FormatUnderlined
import androidx.compose.material.icons.outlined.Link
import androidx.compose.material.icons.outlined.MoreVert
import androidx.compose.material.icons.outlined.SelectAll
import androidx.compose.material.icons.outlined.Title
import androidx.compose.material3.AlertDialog
import com.neb.ians.ui.components.NebDropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.material.icons.outlined.DragIndicator
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.layout.positionInWindow
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.zIndex
import androidx.compose.animation.core.animateFloatAsState as animateShift
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.Stable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.key
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.withFrameNanos
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.input.key.Key
import androidx.compose.ui.input.key.KeyEventType
import androidx.compose.ui.input.key.isShiftPressed
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
import com.neb.ians.ui.components.LiveReconcile
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
    private val states = HashMap<String, RichState>()
    var focusedId by mutableStateOf<String?>(null)
    /** A picture, recording, table or drawing the user has tapped: its tools show right under it. */
    var selectedId by mutableStateOf<String?>(null)

    /** The editor of one block. Plain text and its formatting live in it; the view model gets Markdown on every edit. */
    fun stateOf(vm: NoteEditorViewModel, block: NoteBlock): RichState {
        val raw = block.type == BlockType.Code
        return states.getOrPut(block.id + if (raw) "|c" else "|t") {
            RichState(blockMode = true, raw = raw).also { st ->
                st.setMarkdown(block.text)
                st.onEdited = { r -> vm.setText(block.id, r.lastMarkdown) }
            }
        }
    }

    fun focusedState(): RichState? = focusedId?.let { id -> states[id + "|t"] }
}

/**
 * Drag to reorder. A handle on every block starts a drag; the block follows the finger, the blocks it passes slide out of
 * the way, and the drop moves it (and whatever is nested under it) to the slot it was over.
 */
@Stable
class BlockReorder {
    var dragId by mutableStateOf<String?>(null)
        private set
    var offset by mutableFloatStateOf(0f)
        private set
    var gap = 0f
    var order: List<String> = emptyList()
    var commit: (String, String) -> Unit = { _, _ -> }
    private val heights = HashMap<String, Int>()

    fun measured(id: String, height: Int) { heights[id] = height }
    fun heightOf(id: String): Float = (heights[id] ?: 0).toFloat()

    /** The scrolling column the blocks live in: its edges (window coordinates) and how far it is scrolled. */
    var scroller: ScrollState? = null
    var viewTop = 0f
    var viewBottom = 0f
    private var startY = 0f
    private var travelled = 0f
    var fingerY by mutableFloatStateOf(0f)
        private set

    fun start(id: String, handleY: Float) { dragId = id; offset = 0f; startY = handleY; travelled = 0f; fingerY = handleY }
    fun drag(dy: Float) { offset += dy; travelled += dy; fingerY = startY + travelled }
    fun cancel() { dragId = null; offset = 0f }

    /** The column scrolled by [by] while the finger stayed put: the block has to travel the same way to stay under it. */
    fun follow(by: Float) { offset += by }

    /** Pixels per frame the column should scroll right now: faster the closer the finger is to an edge, 0 away from them. */
    fun edgeSpeed(edge: Float, top: Float): Float = when {
        viewBottom <= viewTop -> 0f
        fingerY < viewTop + edge -> -top * ((viewTop + edge - fingerY) / edge).coerceIn(0f, 1.5f)
        fingerY > viewBottom - edge -> top * ((fingerY - (viewBottom - edge)) / edge).coerceIn(0f, 1.5f)
        else -> 0f
    }

    /** The slot, as an index into [order], the dragged block is hovering over. */
    fun target(): Int {
        val id = dragId ?: return -1
        val from = order.indexOf(id)
        if (from < 0) return -1
        var target = from
        var travelled = 0f
        if (offset > 0f) {
            var i = from + 1
            while (i < order.size) {
                val step = heightOf(order[i]) + gap
                if (offset > travelled + step / 2f) { travelled += step; target = i; i++ } else break
            }
        } else {
            var i = from - 1
            while (i >= 0) {
                val step = heightOf(order[i]) + gap
                if (-offset > travelled + step / 2f) { travelled += step; target = i; i-- } else break
            }
        }
        return target
    }

    fun finish(slot: Int) {
        val id = dragId
        val over = order.getOrNull(slot)
        cancel()
        if (id != null && over != null && over != id) commit(id, over)
    }
}

/** How far a block that is not being dragged should sit from its place while [slot] is hovered. */
private fun BlockReorder.shiftFor(id: String, slot: Int): Float {
    val dragged = dragId ?: return 0f
    if (id == dragged) return 0f
    val from = order.indexOf(dragged)
    val at = order.indexOf(id)
    if (from < 0 || at < 0 || slot < 0) return 0f
    val room = heightOf(dragged) + gap
    return when {
        slot > from && at in (from + 1)..slot -> -room
        slot < from && at in slot until from -> room
        else -> 0f
    }
}

@Composable
private fun ReorderSlot(id: String, reorder: BlockReorder, slot: Int, content: @Composable () -> Unit) {
    val dragging = reorder.dragId == id
    val shift by animateShift(
        targetValue = reorder.shiftFor(id, slot),
        label = "block_shift",
    )
    Box(
        Modifier
            .onSizeChanged { reorder.measured(id, it.height) }
            .zIndex(if (dragging) 1f else 0f)
            .graphicsLayer {
                translationY = if (dragging) reorder.offset else shift
                val lift = if (dragging) 1.02f else 1f
                scaleX = lift
                scaleY = lift
                alpha = if (dragging) 0.94f else 1f
            },
    ) { content() }
}

@Composable
fun NoteBlockEditor(
    blocks: List<NoteBlock>,
    vm: NoteEditorViewModel,
    registry: BlockFieldRegistry,
    readOnly: Boolean,
    fg: Color,
    modifier: Modifier = Modifier,
    reorder: BlockReorder = remember { BlockReorder() },
) {
    val focusRequest by vm.focusRequest.collectAsStateWithLifecycle()
    // numbers count per level: a nested list starts again at 1 and does not break the one around it
    val numbers = remember(blocks) {
        val counters = IntArray(NoteDoc.MAX_INDENT + 2)
        blocks.map { b ->
            if (b.type == BlockType.Number) {
                counters[b.indent]++
                for (j in b.indent + 1 until counters.size) counters[j] = 0
                counters[b.indent]
            } else {
                for (j in b.indent until counters.size) counters[j] = 0
                0
            }
        }
    }
    val hidden = remember(blocks) { NoteDoc.hiddenIndexes(blocks) }
    // a picture set beside text takes the text block after it into its own row
    val partners = remember(blocks) {
        blocks.indices.filter { i ->
            val b = blocks[i]
            val n = blocks.getOrNull(i + 1)
            b.type == BlockType.Image && b.wrap && b.path.isNotBlank() && i !in hidden && n != null && n.type.hasText && n.type != BlockType.Code && (i + 1) !in hidden
        }.toSet()
    }
    val skip = remember(hidden, partners) { hidden + partners.map { it + 1 } }
    reorder.order = blocks.filterIndexed { i, _ -> i !in skip }.map { it.id }
    reorder.gap = with(LocalDensity.current) { 6.dp.toPx() }
    reorder.commit = { id, over -> vm.moveBlock(id, over) }
    val slot by remember { derivedStateOf { reorder.target() } }
    // holding a block near the top or bottom edge scrolls the note under it, and the block keeps up with the finger
    val edge = with(LocalDensity.current) { 96.dp.toPx() }
    val top = with(LocalDensity.current) { 18.dp.toPx() }
    LaunchedEffect(reorder.dragId) {
        if (reorder.dragId == null) return@LaunchedEffect
        while (true) {
            withFrameNanos { }
            val state = reorder.scroller ?: continue
            val speed = reorder.edgeSpeed(edge, top)
            if (speed != 0f) {
                reorder.follow(state.dispatchRawDelta(speed))
            }
        }
    }
    Column(modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        blocks.forEachIndexed { index, block ->
            if (index in skip) return@forEachIndexed
            key(block.id) {
                ReorderSlot(block.id, reorder, slot) {
                    when (block.type) {
                        BlockType.Divider -> MediaFrame(block, vm, registry, readOnly, reorder, tappable = true) {
                            Box(Modifier.fillMaxWidth().padding(vertical = 10.dp).height(2.dp).clip(RoundedCornerShape(1.dp)).background(fg.copy(alpha = 0.2f)))
                        }
                        BlockType.Image -> {
                            val partner = if (index in partners) blocks[index + 1] else null
                            val picked = registry.selectedId == block.id
                            val imageTools: (@Composable () -> Unit)? = if (block.path.isNotBlank()) ({ ImageTools(block, vm) }) else null
                            val sideText: (@Composable () -> Unit)? = if (partner != null) ({
                                TextBlockRow(partner, numbers[index + 1], false, vm, registry, readOnly, fg, focusRequest == partner.id, 0, reorder)
                            }) else null
                            MediaFrame(block, vm, registry, readOnly, reorder, tappable = false, tools = imageTools, beside = sideText) { inRow ->
                                ImageBlockView(block, vm, readOnly, picked, { registry.selectedId = if (picked) null else block.id }, inRow = inRow)
                            }
                        }
                        BlockType.Audio -> MediaFrame(block, vm, registry, readOnly, reorder, tappable = true) { AudioBlockView(block, vm, readOnly) }
                        BlockType.Table -> MediaFrame(block, vm, registry, readOnly, reorder, tappable = true) { TableBlockView(block, vm, readOnly, fg) }
                        BlockType.Drawing -> MediaFrame(block, vm, registry, readOnly, reorder, tappable = false) { DrawingBlockView(block, vm, readOnly) }
                        else -> TextBlockRow(block, numbers[index], blocks.size == 1, vm, registry, readOnly, fg, focusRequest == block.id, if (block.type == BlockType.Toggle && !block.open) NoteDoc.childCount(blocks, index) else 0, reorder)
                    }
                }
            }
        }
        if (!readOnly) {
            Box(Modifier.fillMaxWidth().height(180.dp).clickable(interactionSource = remember { MutableInteractionSource() }, indication = null) { registry.selectedId = null; vm.tapBelow() })
        }
    }
}

/**
 * A media block. Tap selects it and its tools open right under it (no floating buttons over the content); press and hold
 * moves it, the others slide out of the way and a line shows where it will land.
 */
@Composable
private fun MediaFrame(
    block: NoteBlock, vm: NoteEditorViewModel, registry: BlockFieldRegistry, readOnly: Boolean, reorder: BlockReorder,
    tappable: Boolean,
    tools: (@Composable () -> Unit)? = null,
    beside: (@Composable () -> Unit)? = null,
    content: @Composable (inRow: Boolean) -> Unit,
) {
    val selected = registry.selectedId == block.id && !readOnly
    val centreY = remember { FloatArray(1) }
    val haptic = androidx.compose.ui.platform.LocalHapticFeedback.current
    Column(
        Modifier.fillMaxWidth()
            .onGloballyPositioned { centreY[0] = it.positionInWindow().y + it.size.height / 2f }
            .then(
                if (readOnly) Modifier else Modifier.pointerInput(block.id) {
                    detectDragGesturesAfterLongPress(
                        onDragStart = { haptic.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.LongPress); reorder.start(block.id, centreY[0]) },
                        onDrag = { change, amount -> change.consume(); reorder.drag(amount.y) },
                        onDragEnd = {
                            val moved = kotlin.math.abs(reorder.offset) > 6f
                            if (moved) reorder.finish(reorder.target()) else { reorder.cancel(); registry.selectedId = block.id }
                        },
                        onDragCancel = { reorder.cancel() },
                    )
                }
            )
            .then(
                if (tappable && !readOnly) Modifier.clickable(interactionSource = remember { MutableInteractionSource() }, indication = null) {
                    registry.selectedId = if (selected) null else block.id
                } else Modifier
            ),
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        if (beside != null) {
            val share = block.size.coerceIn(0.25f, 0.6f)
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                if (block.align == 2) Box(Modifier.weight(1f - share)) { beside() }
                Box(Modifier.weight(share)) { content(true) }
                if (block.align != 2) Box(Modifier.weight(1f - share)) { beside() }
            }
        } else content(false)
        AnimatedVisibility(selected, enter = expandVertically(spring(stiffness = 500f)) + fadeIn(), exit = shrinkVertically() + fadeOut()) {
            Row(Modifier.nebHorizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                if (tools != null) { tools(); ToolDivider() }
                ToolIcon(Icons.Outlined.ArrowUpward, "Move up", false) { vm.move(block.id, -1) }
                ToolIcon(Icons.Outlined.ArrowDownward, "Move down", false) { vm.move(block.id, 1) }
                ToolIcon(Icons.Outlined.ContentCopy, "Duplicate", false) { vm.duplicate(block.id) }
                ToolIcon(Icons.Outlined.Delete, "Delete", false) { registry.selectedId = null; vm.delete(block.id) }
            }
        }
    }
}

/** Everything a block can be turned into, moved, copied or removed. Opened from the bar, so no handle sits on the page. */
@Composable
private fun BlockSheet(block: NoteBlock, vm: NoteEditorViewModel, onDismiss: () -> Unit) {
    val c = MaterialTheme.colorScheme
    NoteSheet(onDismiss = onDismiss, title = "Block") {
        Column(
            Modifier.heightIn(max = 560.dp).verticalScroll(rememberScrollState()).padding(vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            if (block.type.hasText) {
                FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf(BlockType.Text, BlockType.H1, BlockType.H2, BlockType.H3, BlockType.Todo, BlockType.Toggle, BlockType.Bullet, BlockType.Number, BlockType.Quote, BlockType.Callout, BlockType.Code).forEach { t ->
                        ToolChip(label = t.label, on = block.type == t, icon = blockIcon(t)) { onDismiss(); vm.convert(block.id, t) }
                    }
                }
                if (block.type != BlockType.Code) InkControls(block) { a, t, m -> vm.setLook(block.id, a, t, m) }
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    ToolChip("Outdent", false, Icons.Outlined.FormatIndentDecrease) { vm.indent(block.id, -1) }
                    ToolChip("Indent", false, Icons.Outlined.FormatIndentIncrease) { vm.indent(block.id, 1) }
                }
            }
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                ToolChip("Move up", false, Icons.Outlined.ArrowUpward) { vm.move(block.id, -1) }
                ToolChip("Move down", false, Icons.Outlined.ArrowDownward) { vm.move(block.id, 1) }
                ToolChip("Duplicate", false, Icons.Outlined.ContentCopy) { onDismiss(); vm.duplicate(block.id) }
                ToolChip("Delete", false, Icons.Outlined.Delete) { onDismiss(); vm.delete(block.id) }
            }
            if (block.type == BlockType.Todo) {
                var pick by remember { mutableStateOf(false) }
                FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    ToolChip("Today", block.due == NoteDue.today(), Icons.Outlined.Event) { onDismiss(); vm.setDue(block.id, NoteDue.today()) }
                    ToolChip("Tomorrow", block.due == NoteDue.today() + 1, Icons.Outlined.Event) { onDismiss(); vm.setDue(block.id, NoteDue.today() + 1) }
                    ToolChip("Pick date", false, Icons.Outlined.Event) { pick = true }
                    if (block.due > 0L) ToolChip("No date", false) { onDismiss(); vm.setDue(block.id, 0L) }
                }
                if (pick) DueDialog(block.due, onPick = { vm.setDue(block.id, it) }, onDismiss = { pick = false; onDismiss() })
                Text("Clear completed", style = MaterialTheme.typography.labelLarge, color = c.primary,
                    modifier = Modifier.clip(RoundedCornerShape(18.dp)).clickable { onDismiss(); vm.clearDone() }.padding(horizontal = 4.dp, vertical = 8.dp))
            }
        }
        Spacer(Modifier.height(16.dp))
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
    hiddenKids: Int = 0,
    reorder: BlockReorder,
) {
    val c = MaterialTheme.colorScheme
    val type = block.type
    val focusRequester = remember { FocusRequester() }
    var focused by remember { mutableStateOf(false) }
    val state = registry.stateOf(vm, block)

    LaunchedEffect(block.text) {
        state.adopt(block.text, block.text.length)
        if (wantsFocus && vm.selectAllRequested) state.selectAll()
    }
    LaunchedEffect(wantsFocus) {
        if (wantsFocus) {
            val selectAll = vm.selectAllRequested
            when {
                selectAll -> {
                    state.adopt(block.text, block.text.length)
                    state.selectAll()
                }
                vm.focusCaretOffset >= 0 -> state.setMarkdown(block.text, vm.focusCaretOffset)
                vm.caretAtStart -> state.setMarkdown(block.text, 0)
            }
            runCatching { focusRequester.requestFocus() }
            vm.consumeFocus()
            if (selectAll) {
                withFrameNanos { }
                state.selectAll()
            }
        }
    }

    var pickDue by remember { mutableStateOf(false) }
    val typo = MaterialTheme.typography
    val done = type == BlockType.Todo && block.checked
    val darkPage = c.surface.luminance() < 0.5f
    val inkText = if (type == BlockType.Code) null else NoteInk.text(block.tint, darkPage)
    val inkFill = if (type == BlockType.Code || type == BlockType.Callout) null else NoteInk.fill(block.mark, darkPage)
    val textColor = when {
        done -> (inkText ?: fg).copy(alpha = 0.5f)
        inkText != null -> inkText
        type == BlockType.Callout -> c.onPrimaryContainer
        else -> fg
    }
    val style: TextStyle = when (type) {
        BlockType.H1 -> typo.headlineMedium.copy(fontWeight = FontWeight.SemiBold)
        BlockType.H2 -> typo.titleLarge.copy(fontWeight = FontWeight.SemiBold)
        BlockType.H3 -> typo.titleMedium.copy(fontWeight = FontWeight.SemiBold)
        BlockType.Code -> typo.bodyMedium.copy(fontFamily = FontFamily.Monospace)
        else -> typo.bodyLarge.copy(lineHeight = 24.sp)
    }.copy(color = textColor, textDecoration = if (done) TextDecoration.LineThrough else TextDecoration.None, textAlign = inkAlign(block.align))
    val hint = when (type) {
        BlockType.Text -> if (onlyBlock) "Start writing, or type / for blocks" else if (focused) "Type / for blocks" else ""
        BlockType.H1, BlockType.H2, BlockType.H3 -> "Heading"
        BlockType.Todo -> "To-do"
        BlockType.Toggle -> "Toggle"
        BlockType.Bullet, BlockType.Number -> "List"
        BlockType.Quote -> "Quote"
        BlockType.Callout -> "Callout"
        BlockType.Code -> "Code"
        else -> ""
    }
    val mdLines = remember(block.text) { block.text.split('\n') }
    val slashLineIndex = remember(block.text, state.value.text, state.value.selection) {
        if (type != BlockType.Text) -1
        else {
            val plain = state.value.text
            val caret = state.value.selection.start.coerceIn(0, plain.length)
            val lineIdx = plain.substring(0, caret).count { it == '\n' }.coerceIn(0, (mdLines.size - 1).coerceAtLeast(0))
            val ln = mdLines.getOrNull(lineIdx).orEmpty()
            if (ln.startsWith("/") && !ln.contains(' ')) lineIdx else -1
        }
    }
    val slash = if (slashLineIndex >= 0) {
        val q = mdLines[slashLineIndex].drop(1)
        BlockType.entries.filter { q.isBlank() || it.label.contains(q, true) || it.keywords.contains(q, true) }.take(9)
    } else emptyList()

    val container: Modifier = when (type) {
        BlockType.Callout -> Modifier.clip(RoundedCornerShape(16.dp)).background(c.primaryContainer.copy(alpha = 0.6f)).padding(14.dp)
        BlockType.Code -> Modifier.clip(RoundedCornerShape(14.dp)).background(c.surfaceContainerHighest).padding(12.dp)
        else -> if (inkFill != null) Modifier.clip(RoundedCornerShape(12.dp)).background(inkFill).padding(horizontal = 10.dp, vertical = 6.dp) else Modifier
    }
    val topPad = when (type) { BlockType.H1 -> 14.dp; BlockType.H2 -> 10.dp; BlockType.H3 -> 6.dp; else -> 0.dp }

    Row(
        Modifier.fillMaxWidth().padding(start = (block.indent * 24).dp, top = topPad).then(if (type == BlockType.Quote) Modifier.height(IntrinsicSize.Min) else Modifier).then(container),
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
            BlockType.Toggle -> {
                val turn by animateFloatAsState(if (block.open) 90f else 0f, label = "toggle")
                Box(
                    Modifier.padding(end = 4.dp).size(28.dp).clip(CircleShape).clickable { vm.toggleOpen(block.id) },
                    contentAlignment = Alignment.Center,
                ) {
                    Icon(
                        Icons.Outlined.ChevronRight, if (block.open) "Fold" else "Unfold", tint = fg.copy(alpha = 0.75f),
                        modifier = Modifier.size(22.dp).graphicsLayer { rotationZ = turn },
                    )
                }
            }
            BlockType.Quote -> Box(Modifier.padding(end = 12.dp).width(3.dp).fillMaxHeight().clip(RoundedCornerShape(2.dp)).background(c.primary))
            else -> {}
        }
        Box(Modifier.weight(1f)) {
            val isMultiLineBlock = type == BlockType.Text || type == BlockType.Code || type == BlockType.Quote || type == BlockType.Callout
            RichTextField(
                state = state,
                onChange = { typed ->
                    val exitQuoteOrCallout = (type == BlockType.Quote || type == BlockType.Callout) && typed.text.endsWith("\n\n")
                    if (exitQuoteOrCallout) {
                        state.onChangeQuiet(typed)
                        val trimmed = state.markdown().trimEnd('\n')
                        state.setMarkdown(trimmed)
                        vm.split(block.id, trimmed, listOf(""))
                    } else if (!isMultiLineBlock && typed.text.contains('\n')) {
                        state.onChangeQuiet(typed)
                        val parts = state.markdown().split('\n')
                        state.setMarkdown(parts.first())
                        vm.split(block.id, parts.first(), parts.drop(1))
                    } else {
                        state.onChange(typed)
                    }
                },
                readOnly = readOnly,
                textStyle = style,
                keyboardCapitalization = if (type == BlockType.Code) KeyboardCapitalization.None else KeyboardCapitalization.Sentences,
                decorationBox = { inner ->
                    Box {
                        if (block.text.isEmpty() && hint.isNotEmpty()) Text(hint, modifier = Modifier.fillMaxWidth(), style = style.copy(color = fg.copy(alpha = 0.35f), textDecoration = TextDecoration.None))
                        inner()
                    }
                },
                modifier = Modifier.fillMaxWidth()
                    .focusRequester(focusRequester)
                    .onFocusChanged {
                        focused = it.hasFocus
                        if (it.hasFocus) { registry.focusedId = block.id; registry.selectedId = null; vm.setFocused(block.id) }
                    }
                    .onPreviewKeyEvent { ev ->
                        val sel = state.value.selection
                        if (ev.type == KeyEventType.KeyDown && ev.key == Key.Tab && !readOnly) {
                            vm.indent(block.id, if (ev.isShiftPressed) -1 else 1); true
                        } else if (ev.type == KeyEventType.KeyDown && ev.key == Key.Backspace && sel.collapsed && sel.start == 0 && !readOnly) {
                            vm.backspaceAtStart(block.id); true
                        } else false
                    },
            )
            NebDropdownMenu(
                expanded = focused && slash.isNotEmpty(), onDismissRequest = {},
                properties = PopupProperties(focusable = false),
            ) {
                slash.forEach { t ->
                    DropdownMenuItem(
                        text = {
                            Column {
                                Text(t.label, fontWeight = FontWeight.Medium)
                                Text(t.hint, style = MaterialTheme.typography.labelSmall, color = c.onSurfaceVariant)
                            }
                        },
                        leadingIcon = { Icon(blockIcon(t), null, tint = c.primary, modifier = Modifier.size(22.dp)) },
                        onClick = {
                            if (slashLineIndex >= 0 && mdLines.size > 1) {
                                val beforeMd = mdLines.subList(0, slashLineIndex).joinToString("\n")
                                val afterMd = mdLines.subList(slashLineIndex + 1, mdLines.size).joinToString("\n")
                                vm.applySlashOnLine(block.id, beforeMd, afterMd, t)
                            } else {
                                vm.applySlash(block.id, t)
                            }
                        },
                    )
                }
            }
        }
        if (type == BlockType.Todo && block.due > 0L) {
            DueChip(block.due, block.checked, onClick = { if (!readOnly) pickDue = true }, modifier = Modifier.padding(start = 8.dp, top = 1.dp))
        }
        if (pickDue) DueDialog(block.due, onPick = { vm.setDue(block.id, it) }, onDismiss = { pickDue = false })
        if (hiddenKids > 0) {
            Text(
                "$hiddenKids", style = MaterialTheme.typography.labelSmall, color = c.onSecondaryContainer,
                modifier = Modifier.padding(start = 6.dp, top = 4.dp).clip(RoundedCornerShape(8.dp)).background(c.secondaryContainer).padding(horizontal = 8.dp, vertical = 2.dp),
            )
        }
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
    onCollapse: () -> Unit = {},
    trailing: @Composable () -> Unit,
) {
    val c = MaterialTheme.colorScheme
    val focusedId = registry.focusedId
    val block = blocks.firstOrNull { it.id == (registry.selectedId ?: focusedId) }
    val textBlock = blocks.firstOrNull { it.id == focusedId }
    var blockSheet by remember { mutableStateOf(false) }
    val photos = rememberLauncherForActivityResult(ActivityResultContracts.PickMultipleVisualMedia(10)) { uris ->
        var after = registry.selectedId ?: vm.focusedId
        uris.forEach { uri ->
            val b = NoteBlock(type = BlockType.Image)
            vm.insert(BlockType.Image, afterId = after, block = b)
            vm.fillImage(b.id, uri)
            after = b.id
        }
    }
    val rich = textBlock?.let { registry.stateOf(vm, it) }
    val canInline = textBlock != null && textBlock.type.hasText && textBlock.type != BlockType.Code
    rich?.value
    rich?.armed
    var insertMenu by remember { mutableStateOf(false) }
    var linkDialog by remember { mutableStateOf(false) }

    fun applyInline(flag: Int) {
        if (rich != null && canInline) rich.toggleInline(flag)
    }
    fun active(flag: Int) = canInline && rich != null && rich.isActive(flag)
    fun turn(type: BlockType) {
        val id = textBlock?.id ?: vm.focusedId ?: return
        vm.convert(id, type)
    }

    Row(modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
        Row(Modifier.weight(1f).nebHorizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(4.dp), verticalAlignment = Alignment.CenterVertically) {
            BarButton(Icons.Outlined.KeyboardArrowDown, "Hide toolbar", fg, false) { onCollapse() }
            Box {
                BarButton(Icons.Outlined.Add, "Add a block", fg, false) { insertMenu = true }
                NebDropdownMenu(
                    expanded = insertMenu, onDismissRequest = { insertMenu = false },
                ) {
                    listOf(BlockType.Image, BlockType.Audio, BlockType.Drawing, BlockType.Table, BlockType.Toggle, BlockType.Callout, BlockType.Code, BlockType.Divider).forEach { t ->
                        DropdownMenuItem(
                            text = { Text(t.label) },
                            leadingIcon = { Icon(blockIcon(t), null, tint = c.primary) },
                            onClick = {
                                insertMenu = false
                                when (t) {
                                    BlockType.Table -> vm.newTable()
                                    BlockType.Callout, BlockType.Code, BlockType.Toggle -> vm.insert(t)
                                    else -> vm.insert(t)
                                }
                            },
                        )
                    }
                }
            }
            BarButton(Icons.Outlined.AddPhotoAlternate, "Photos", fg, false) {
                photos.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
            }
            BarButton(Icons.Outlined.FormatBold, "Bold", fg, active(Fmt.BOLD)) { applyInline(Fmt.BOLD) }
            BarButton(Icons.Outlined.FormatItalic, "Italic", fg, active(Fmt.ITALIC)) { applyInline(Fmt.ITALIC) }
            BarButton(Icons.Outlined.FormatUnderlined, "Underline", fg, active(Fmt.UNDERLINE)) { applyInline(Fmt.UNDERLINE) }
            BarButton(Icons.Outlined.FormatStrikethrough, "Strikethrough", fg, active(Fmt.STRIKE)) { applyInline(Fmt.STRIKE) }
            BarButton(Icons.Outlined.Code, "Inline code", fg, active(Fmt.CODE)) { applyInline(Fmt.CODE) }
            BarButton(Icons.Outlined.Link, "Link", fg, false) { if (canInline) linkDialog = true }
            BarButton(Icons.Outlined.Title, "Heading", fg, textBlock?.type == BlockType.H2) { turn(BlockType.H2) }
            BarButton(Icons.Outlined.Checklist, "To-do", fg, textBlock?.type == BlockType.Todo) { turn(BlockType.Todo) }
            BarButton(Icons.Outlined.FormatListBulleted, "Bullets", fg, textBlock?.type == BlockType.Bullet) { turn(BlockType.Bullet) }
            BarButton(Icons.Outlined.FormatListNumbered, "Numbers", fg, textBlock?.type == BlockType.Number) { turn(BlockType.Number) }
            BarButton(Icons.Outlined.FormatQuote, "Quote", fg, textBlock?.type == BlockType.Quote) { turn(BlockType.Quote) }
            BarButton(Icons.Outlined.FormatIndentDecrease, "Outdent", fg, false) { (textBlock?.id ?: vm.focusedId)?.let { vm.indent(it, -1) } }
            BarButton(Icons.Outlined.FormatIndentIncrease, "Indent", fg, false) { (textBlock?.id ?: vm.focusedId)?.let { vm.indent(it, 1) } }
            BarButton(Icons.Outlined.SelectAll, "Select all", fg, false) { vm.selectAllText(registry) }
            BarButton(Icons.Outlined.MoreHoriz, "Block options", fg, false) { if (block != null) blockSheet = true }
        }
        trailing()
    }

    if (blockSheet && block != null) BlockSheet(block, vm) { blockSheet = false }
    if (linkDialog && block != null && rich != null) {
        var url by remember { mutableStateOf("") }
        AlertDialog(
            onDismissRequest = { linkDialog = false },
            shape = RoundedCornerShape(28.dp), containerColor = com.neb.ians.ui.theme.nebFloatColor(),
            title = { Text("Add link") },
            text = { OutlinedTextField(value = url, onValueChange = { url = it }, singleLine = true, shape = RoundedCornerShape(16.dp), placeholder = { Text("Paste a link") }) },
            confirmButton = {
                TextButton(
                    onClick = { rich.insertLink(url); linkDialog = false },
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


/** The glyph a block kind carries in the "/" list, the insert menu and the template sheet. */
internal fun blockIcon(type: BlockType): ImageVector = when (type) {
    BlockType.Text -> Icons.Outlined.Notes
    BlockType.H1, BlockType.H2, BlockType.H3 -> Icons.Outlined.Title
    BlockType.Todo -> Icons.Outlined.Checklist
    BlockType.Toggle -> Icons.Outlined.ChevronRight
    BlockType.Bullet -> Icons.Outlined.FormatListBulleted
    BlockType.Number -> Icons.Outlined.FormatListNumbered
    BlockType.Quote -> Icons.Outlined.FormatQuote
    BlockType.Callout -> Icons.Outlined.Lightbulb
    BlockType.Code -> Icons.Outlined.Code
    BlockType.Divider -> Icons.Outlined.HorizontalRule
    BlockType.Table -> Icons.Outlined.TableChart
    BlockType.Image -> Icons.Outlined.Image
    BlockType.Audio -> Icons.Outlined.Mic
    BlockType.Drawing -> Icons.Outlined.Draw
}
