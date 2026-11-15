@file:OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)

package com.neb.ians.ui.screens.notes

import androidx.compose.ui.text.AnnotatedString
import com.neb.ians.ui.components.InlineImageTokens
import com.neb.ians.ui.components.LiveColors
import com.neb.ians.ui.components.LiveMarkdown
import androidx.compose.animation.core.animateFloat
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.offset
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.foundation.shape.CircleShape
import com.neb.ians.ui.components.NebToastHost
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.expandVertically
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.combinedClickable
import com.neb.ians.ui.components.nebHorizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.lazy.staggeredgrid.LazyVerticalStaggeredGrid
import androidx.compose.foundation.lazy.staggeredgrid.StaggeredGridCells
import androidx.compose.foundation.lazy.staggeredgrid.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.Archive
import androidx.compose.material.icons.outlined.CalendarMonth
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.Checklist
import androidx.compose.material.icons.outlined.ChevronRight
import androidx.compose.material.icons.outlined.MenuBook
import androidx.compose.material.icons.outlined.Notes
import androidx.compose.material.icons.outlined.Quiz
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.Translate
import androidx.compose.material.icons.outlined.Flag
import androidx.compose.material.icons.outlined.VerticalSplit
import androidx.compose.material.icons.outlined.Groups
import androidx.compose.material.icons.outlined.AccountTree
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.layout.heightIn
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.DeleteForever
import androidx.compose.material.icons.outlined.EditNote
import androidx.compose.material.icons.outlined.GraphicEq
import androidx.compose.material.icons.outlined.GridView
import androidx.compose.material.icons.outlined.Mic
import androidx.compose.material.icons.outlined.Palette
import androidx.compose.material.icons.outlined.PushPin
import androidx.compose.material.icons.outlined.RestoreFromTrash
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.SelectAll
import androidx.compose.material.icons.outlined.Sort
import androidx.compose.material.icons.outlined.Unarchive
import androidx.compose.material.icons.outlined.ViewAgenda
import com.neb.ians.ui.components.NebDropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExtendedFloatingActionButton
import androidx.compose.material3.FloatingActionButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SmallFloatingActionButton
import androidx.compose.material3.SnackbarDuration
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.SnackbarResult
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.local.entity.NoteEntity
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebModalSheet
import com.neb.ians.util.TactileType
import com.neb.ians.util.rememberTactileFeedback
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Locale

@Composable
fun NotesScreen(
    onOpenNote: (String) -> Unit,
    onNewNote: (dictate: Boolean) -> Unit,
    onOpenVoice: () -> Unit,
    vm: NotesViewModel = hiltViewModel(),
) {
    val ui by vm.ui.collectAsStateWithLifecycle()
    val c = MaterialTheme.colorScheme
    val snack = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()
    val tactile = rememberTactileFeedback()
    var toneSheet by remember { mutableStateOf(false) }
    var templateSheet by remember { mutableStateOf(false) }
    val selecting = ui.selection.isNotEmpty()

    fun undoable(message: String, ids: List<String>, undo: (List<String>) -> Unit) {
        scope.launch {
            snack.currentSnackbarData?.dismiss()
            val r = snack.showSnackbar(message, actionLabel = "Undo", duration = SnackbarDuration.Short)
            if (r == SnackbarResult.ActionPerformed) undo(ids)
        }
    }

    Scaffold(
        containerColor = c.surface,
        snackbarHost = { NebToastHost(snack, Modifier.padding(bottom = 76.dp)) },
    ) { inner ->
        Column(Modifier.fillMaxSize().padding(inner).statusBarsPadding()) {
            if (selecting) {
                SelectionBar(
                    count = ui.selection.size,
                    inBin = ui.filter == NoteFilter.Trash,
                    inArchive = ui.filter == NoteFilter.Archive,
                    onClose = vm::clearSelection,
                    onAll = vm::selectAll,
                    onPin = { vm.pinSelected() },
                    onTone = { toneSheet = true },
                    onArchive = {
                        val unarchive = ui.filter == NoteFilter.Archive
                        val ids = vm.archiveSelected()
                        undoable(if (unarchive) "Moved to notes" else "Archived", ids) { if (unarchive) vm.archive(it) else vm.unarchive(it) }
                    },
                    onTrash = { val ids = vm.trashSelected(); undoable("Moved to bin", ids) { vm.restore(it) } },
                    onRestore = { vm.restoreSelected() },
                    onDeleteForever = vm::deleteSelectedForever,
                )
            } else {
                Header(ui, vm, onOpenVoice, showAdd = ui.filter != NoteFilter.Trash) { tactile.perform(TactileType.LightTap); templateSheet = true }
            }
            AnimatedVisibility(ui.searching && !selecting, enter = expandVertically() + fadeIn(), exit = shrinkVertically() + fadeOut()) {
                SearchField(ui.query, vm::setQuery)
            }
            FilterRow(ui, vm)
            if (ui.filter == NoteFilter.Trash && ui.notes.isNotEmpty()) {
                Row(Modifier.fillMaxWidth().padding(horizontal = 12.dp), horizontalArrangement = Arrangement.End) {
                    TextButton(onClick = { vm.emptyBin() }) { Text("Empty bin", color = c.error) }
                }
            }
            Box(Modifier.weight(1f).fillMaxWidth()) {
                when {
                    !ui.loaded -> Unit
                    ui.notes.isEmpty() && ui.query.isBlank() && ui.tag == null && ui.filter == NoteFilter.All -> NotesEmptyState(
                        onWrite = { tactile.perform(TactileType.LightTap); templateSheet = true },
                        onDictate = { tactile.perform(TactileType.LightTap); onNewNote(true) },
                        modifier = Modifier.align(Alignment.Center),
                    )
                    ui.notes.isEmpty() -> NebEmptyState(
                        icon = Icons.Outlined.EditNote,
                        title = when {
                            ui.query.isNotBlank() || ui.tag != null -> "No matches"
                            ui.filter == NoteFilter.Trash -> "The bin is empty"
                            ui.filter == NoteFilter.Archive -> "Nothing archived"
                            else -> "Nothing pinned"
                        },
                        modifier = Modifier.align(Alignment.Center),
                    )
                    else -> LazyVerticalStaggeredGrid(
                        columns = if (ui.grid) StaggeredGridCells.Adaptive(156.dp) else StaggeredGridCells.Fixed(1),
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(start = 12.dp, end = 12.dp, top = 4.dp, bottom = 160.dp),
                        verticalItemSpacing = 8.dp,
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        items(ui.notes, key = { it.id }) { note ->
                            NoteCard(
                                note = note,
                                selected = note.id in ui.selection,
                                compact = ui.grid,
                                onClick = { if (selecting) vm.toggleSelect(note.id) else onOpenNote(note.id) },
                                onLongClick = { tactile.perform(TactileType.LightTap); vm.toggleSelect(note.id) },
                            )
                        }
                    }
                }
            }
        }
    }

    if (templateSheet) {
        NoteSheet(onDismiss = { templateSheet = false }, title = "New note") {
            TemplateGrid(onPick = { t ->
                NoteTemplate.pending = t
                templateSheet = false
                onNewNote(false)
            })
        }
    }

    if (toneSheet) {
        NoteSheet(onDismiss = { toneSheet = false }, title = "Colour") {
            ToneSwatches(current = -1, onPick = { vm.toneSelected(it); toneSheet = false })
        }
    }
}

private fun templateIcon(t: NoteTemplate) = when (t) {
    NoteTemplate.Blank -> Icons.Outlined.Notes
    NoteTemplate.Class -> Icons.Outlined.School
    NoteTemplate.Tasks -> Icons.Outlined.Checklist
    NoteTemplate.Exam -> Icons.Outlined.Quiz
    NoteTemplate.Week -> Icons.Outlined.CalendarMonth
    NoteTemplate.Reading -> Icons.Outlined.MenuBook
    NoteTemplate.Journal -> Icons.Outlined.EditNote
    NoteTemplate.Outline -> Icons.Outlined.AccountTree
    NoteTemplate.Meeting -> Icons.Outlined.Groups
    NoteTemplate.Cornell -> Icons.Outlined.VerticalSplit
    NoteTemplate.Project -> Icons.Outlined.Flag
    NoteTemplate.Vocab -> Icons.Outlined.Translate
}

/** Where a note starts: a blank page, or one already shaped like what it is for. */
@Composable
private fun TemplateGrid(onPick: (NoteTemplate) -> Unit) {
    val c = MaterialTheme.colorScheme
    Column(
        Modifier.fillMaxWidth().heightIn(max = 520.dp).verticalScroll(rememberScrollState()).padding(bottom = 16.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp),
    ) {
        NoteTemplate.entries.chunked(2).forEach { pair ->
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                pair.forEach { t ->
                    val blank = t == NoteTemplate.Blank
                    Row(
                        Modifier.weight(1f).clip(RoundedCornerShape(24.dp))
                            .background(if (blank) c.primaryContainer else c.surfaceContainerLow)
                            .clickable { onPick(t) }.padding(14.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        Box(
                            Modifier.size(40.dp).clip(RoundedCornerShape(14.dp)).background(if (blank) c.primary else c.secondaryContainer),
                            contentAlignment = Alignment.Center,
                        ) { Icon(templateIcon(t), null, tint = if (blank) c.onPrimary else c.onSecondaryContainer, modifier = Modifier.size(22.dp)) }
                        Text(
                            t.label, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold,
                            color = if (blank) c.onPrimaryContainer else c.onSurface, modifier = Modifier.weight(1f),
                        )
                    }
                }
                if (pair.size == 1) Box(Modifier.weight(1f))
            }
        }
    }
}

@Composable
private fun Header(ui: NotesUi, vm: NotesViewModel, onOpenVoice: () -> Unit, showAdd: Boolean, onAdd: () -> Unit) {
    var sortMenu by remember { mutableStateOf(false) }
    val c = MaterialTheme.colorScheme
    // one 56dp row: the title, four quiet 40dp tools four apart, and the one filled action
    Row(
        Modifier.fillMaxWidth().height(56.dp).padding(start = 20.dp, end = 12.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(4.dp),
    ) {
        Text(
            "Notes", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.SemiBold,
            color = c.onSurface, modifier = Modifier.weight(1f),
        )
        HeaderTool(Icons.Outlined.Search, "Search", on = ui.searching) { vm.setSearching(!ui.searching) }
        HeaderTool(if (ui.grid) Icons.Outlined.ViewAgenda else Icons.Outlined.GridView, if (ui.grid) "List view" else "Grid view", on = false, onClick = vm::toggleGrid)
        Box {
            HeaderTool(Icons.Outlined.Sort, "Sort", on = sortMenu) { sortMenu = true }
            NebDropdownMenu(
                expanded = sortMenu, onDismissRequest = { sortMenu = false },
            ) {
                NoteSort.entries.forEach { s ->
                    DropdownMenuItem(
                        text = { Text(s.label) },
                        onClick = { vm.setSort(s); sortMenu = false },
                        trailingIcon = { if (ui.sort == s) Icon(Icons.Outlined.Check, null, Modifier.size(18.dp)) },
                    )
                }
            }
        }
        HeaderTool(Icons.Outlined.GraphicEq, "Voice", on = false, onClick = onOpenVoice)
        if (showAdd) {
            Box(
                Modifier
                    .padding(start = 4.dp)
                    .size(44.dp)
                    .clip(RoundedCornerShape(16.dp))
                    .background(c.primary)
                    .clickable(onClickLabel = "New note", onClick = onAdd),
                contentAlignment = Alignment.Center,
            ) { Icon(Icons.Outlined.Add, "New note", tint = c.onPrimary) }
        }
    }
}

/** A 40dp tool: ghost at rest, tonal while it is on. Clipped to its own rounded box so press feedback keeps the shape. */
@Composable
private fun HeaderTool(icon: androidx.compose.ui.graphics.vector.ImageVector, label: String, on: Boolean, onClick: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val bg by androidx.compose.animation.animateColorAsState(if (on) c.secondaryContainer else androidx.compose.ui.graphics.Color.Transparent, label = "toolBg")
    Box(
        Modifier.size(40.dp).clip(RoundedCornerShape(14.dp)).background(bg).clickable(onClickLabel = label, onClick = onClick),
        contentAlignment = Alignment.Center,
    ) { Icon(icon, label, tint = if (on) c.onSecondaryContainer else c.onSurface, modifier = Modifier.size(22.dp)) }
}

/** No notes yet: a small stack of paper, still, and the two ways to begin. */
@Composable
private fun NotesEmptyState(onWrite: () -> Unit, onDictate: () -> Unit, modifier: Modifier = Modifier) {
    val c = MaterialTheme.colorScheme
    Column(
        modifier.fillMaxWidth().padding(horizontal = 32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(22.dp),
    ) {
        Box(Modifier.size(width = 200.dp, height = 160.dp), contentAlignment = Alignment.Center) {
            PaperCard(c.tertiaryContainer, c.onTertiaryContainer, -13f, (-46).dp, 8.dp)
            PaperCard(c.secondaryContainer, c.onSecondaryContainer, 11f, 46.dp, 10.dp)
            PaperCard(c.primaryContainer, c.onPrimaryContainer, 0f, 0.dp, 0.dp, front = true)
        }
        Text("No notes yet", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold)
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), verticalAlignment = Alignment.CenterVertically) {
            com.neb.ians.ui.components.NebButton("Write a note", onWrite, icon = Icons.Outlined.Add)
            com.neb.ians.ui.components.NebButton("Dictate", onDictate, tone = com.neb.ians.ui.components.NebButtonTone.Tonal, icon = Icons.Outlined.Mic)
        }
    }
}

@Composable
private fun PaperCard(color: androidx.compose.ui.graphics.Color, ink: androidx.compose.ui.graphics.Color, tilt: Float, x: androidx.compose.ui.unit.Dp, y: androidx.compose.ui.unit.Dp, front: Boolean = false) {
    Box(
        Modifier
            .offset(x = x, y = y)
            .graphicsLayer { rotationZ = tilt }
            .size(width = if (front) 104.dp else 88.dp, height = if (front) 132.dp else 112.dp)
            .clip(RoundedCornerShape(24.dp))
            .background(color)
            .padding(16.dp),
    ) {
        Column(verticalArrangement = Arrangement.spacedBy(9.dp)) {
            Box(Modifier.fillMaxWidth(0.7f).height(7.dp).clip(CircleShape).background(ink.copy(alpha = 0.55f)))
            Box(Modifier.fillMaxWidth().height(6.dp).clip(CircleShape).background(ink.copy(alpha = 0.25f)))
            Box(Modifier.fillMaxWidth(0.85f).height(6.dp).clip(CircleShape).background(ink.copy(alpha = 0.25f)))
            if (front) Box(Modifier.fillMaxWidth(0.5f).height(6.dp).clip(CircleShape).background(ink.copy(alpha = 0.25f)))
        }
        if (front) {
            Icon(
                Icons.Outlined.Add, null, tint = MaterialTheme.colorScheme.onPrimary,
                modifier = Modifier.align(Alignment.BottomEnd).size(34.dp).clip(RoundedCornerShape(12.dp)).background(MaterialTheme.colorScheme.primary).padding(7.dp),
            )
        }
    }
}

@Composable
private fun SearchField(query: String, onChange: (String) -> Unit) {
    val c = MaterialTheme.colorScheme
    val focus = remember { FocusRequester() }
    androidx.compose.runtime.LaunchedEffect(Unit) { focus.requestFocus() }
    Row(
        Modifier.fillMaxWidth().padding(start = 16.dp, end = 16.dp, top = 0.dp, bottom = 8.dp).height(48.dp)
            .clip(RoundedCornerShape(24.dp)).background(c.surfaceContainerHigh).padding(horizontal = 16.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Icon(Icons.Outlined.Search, null, tint = c.onSurfaceVariant, modifier = Modifier.size(20.dp))
        Box(Modifier.weight(1f).padding(start = 10.dp)) {
            if (query.isEmpty()) Text("Search notes", color = c.onSurfaceVariant, style = MaterialTheme.typography.bodyLarge)
            BasicTextField(
                value = query, onValueChange = onChange, singleLine = true,
                textStyle = MaterialTheme.typography.bodyLarge.copy(color = c.onSurface),
                cursorBrush = SolidColor(c.primary),
                modifier = Modifier.fillMaxWidth().focusRequester(focus),
            )
        }
        if (query.isNotEmpty()) {
            IconButton(onClick = { onChange("") }, modifier = Modifier.size(32.dp)) { Icon(Icons.Outlined.Close, "Clear", Modifier.size(18.dp)) }
        }
    }
}

@Composable
private fun FilterRow(ui: NotesUi, vm: NotesViewModel) {
    Row(
        Modifier.fillMaxWidth().nebHorizontalScroll(rememberScrollState()).padding(start = 16.dp, end = 16.dp, top = 0.dp, bottom = 6.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        NoteFilter.entries.forEach { f ->
            val label = if (f == NoteFilter.Trash && ui.binCount > 0) "${f.label} ${ui.binCount}" else f.label
            ToneChip(label, ui.filter == f, { vm.setFilter(f) })
        }
        ui.tags.forEach { t -> ToneChip("#$t", ui.tag == t, { vm.setTag(t) }) }
    }
}

@Composable
private fun SelectionBar(
    count: Int, inBin: Boolean, inArchive: Boolean,
    onClose: () -> Unit, onAll: () -> Unit, onPin: () -> Unit, onTone: () -> Unit,
    onArchive: () -> Unit, onTrash: () -> Unit, onRestore: () -> Unit, onDeleteForever: () -> Unit,
) {
    Row(Modifier.fillMaxWidth().padding(horizontal = 8.dp, vertical = 12.dp), verticalAlignment = Alignment.CenterVertically) {
        IconButton(onClick = onClose) { Icon(Icons.Outlined.Close, "Cancel selection") }
        Text("$count", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold, modifier = Modifier.weight(1f))
        IconButton(onClick = onAll) { Icon(Icons.Outlined.SelectAll, "Select all") }
        if (inBin) {
            IconButton(onClick = onRestore) { Icon(Icons.Outlined.RestoreFromTrash, "Restore") }
            IconButton(onClick = onDeleteForever) { Icon(Icons.Outlined.DeleteForever, "Delete forever", tint = MaterialTheme.colorScheme.error) }
        } else {
            if (!inArchive) IconButton(onClick = onPin) { Icon(Icons.Outlined.PushPin, "Pin") }
            IconButton(onClick = onTone) { Icon(Icons.Outlined.Palette, "Colour") }
            IconButton(onClick = onArchive) { Icon(if (inArchive) Icons.Outlined.Unarchive else Icons.Outlined.Archive, if (inArchive) "Unarchive" else "Archive") }
            IconButton(onClick = onTrash) { Icon(Icons.Outlined.Delete, "Move to bin") }
        }
    }
}

@Composable
internal fun ToneSwatches(current: Int, onPick: (Int) -> Unit) {
    Column(Modifier.fillMaxWidth().padding(vertical = 8.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        (0 until NoteTones.count).chunked(5).forEach { row ->
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                row.forEach { i ->
                    val tone = noteTone(i)
                    Column(Modifier.weight(1f), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Box(
                            Modifier.fillMaxWidth().height(52.dp).clip(RoundedCornerShape(if (current == i) 26.dp else 18.dp)).background(tone.container)
                                .then(if (tone.hairline || current == i) Modifier.androidBorder(current == i) else Modifier)
                                .combinedClickable(onClick = { onPick(i) }),
                            contentAlignment = Alignment.Center,
                        ) {
                            if (current == i) Icon(Icons.Outlined.Check, null, tint = tone.content)
                        }
                        Text(NoteTones.labels[i], style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1)
                    }
                }
                repeat(5 - row.size) { Spacer(Modifier.weight(1f)) }
            }
        }
    }
}

@Composable
private fun Modifier.androidBorder(strong: Boolean): Modifier {
    val c = MaterialTheme.colorScheme
    return this.then(Modifier.border(if (strong) 2.dp else 1.dp, if (strong) c.primary else c.outlineVariant, RoundedCornerShape(18.dp)))
}

private sealed interface PreviewLine {
    data class Plain(val text: AnnotatedString) : PreviewLine
    data class Check(val text: AnnotatedString, val done: Boolean) : PreviewLine
}

private val previewCheck = Regex("^\\s*[-*+]\\s\\[([ xX])]\\s?(.*)$")
private val previewSkip = setOf("[image]", "[audio recording]", "[drawing]")
private val previewRule = Regex("^\\s*(-{3,}|\\*{3,}|_{3,})\\s*$")

/** The first lines of a note as they will look: markers are hidden and their effect drawn, never shown as characters. */
private fun previewLines(body: String, max: Int, colors: LiveColors): List<PreviewLine> {
    val out = ArrayList<PreviewLine>()
    var inCode = false
    for (line in body.lineSequence()) {
        if (line.trimStart().startsWith("```")) { inCode = !inCode; continue }
        val raw = InlineImageTokens.plainText(line, "").replace(LiveMarkdown.ZWSP, "")
        if (inCode || raw.isBlank() || previewRule.matches(raw) || raw.trim() in previewSkip) continue
        val chk = previewCheck.find(raw)
        if (chk != null) {
            val text = LiveMarkdown.transform(chk.groupValues[2].trim(), colors).styled
            if (text.isNotEmpty()) out += PreviewLine.Check(text, chk.groupValues[1].lowercase() == "x")
        } else {
            val text = LiveMarkdown.transform(raw.trim(), colors).styled
            if (text.isNotEmpty()) out += PreviewLine.Plain(text)
        }
        if (out.size >= max) break
    }
    return out
}

private fun dateLabel(ms: Long): String {
    val now = Calendar.getInstance()
    val then = Calendar.getInstance().apply { timeInMillis = ms }
    val sameDay = now.get(Calendar.YEAR) == then.get(Calendar.YEAR) && now.get(Calendar.DAY_OF_YEAR) == then.get(Calendar.DAY_OF_YEAR)
    val days = (now.timeInMillis - ms) / 86_400_000L
    val pattern = when {
        sameDay -> "h:mm a"
        days < 7 -> "EEE"
        now.get(Calendar.YEAR) == then.get(Calendar.YEAR) -> "MMM d"
        else -> "MMM d, yyyy"
    }
    return SimpleDateFormat(pattern, Locale.getDefault()).format(ms)
}

@Composable
private fun NoteCard(
    note: NoteEntity,
    selected: Boolean,
    compact: Boolean,
    onClick: () -> Unit,
    onLongClick: () -> Unit,
) {
    val c = MaterialTheme.colorScheme
    val tone = noteTone(note.tone)
    val shape = RoundedCornerShape(24.dp)
    val live = LiveColors(tone.content.copy(alpha = 0.12f), tone.content, tone.content, tone.content.copy(alpha = 0.75f), tone.content.copy(alpha = 0.6f))
    val lines = remember(note.body, compact, tone) { previewLines(note.body, if (compact) 3 else 4, live) }
    val (done, total) = remember(note.body) { NoteFormatting.checkProgress(note.body) }
    // the first pictures of the note, so a card with photos looks like it has photos
    val pics = remember(note.doc) {
        if (!note.doc.contains("\"Image\"")) emptyList()
        else NoteDoc.fromJson(note.doc).filter { it.type == BlockType.Image && it.path.isNotBlank() }.map { it.path }
    }
    // the nearest date among the open to-dos, shown as a chip on the card
    val nextDue = remember(note.doc) {
        if (!note.doc.contains("\"Todo\"") || !note.doc.contains("\"d\"")) 0L
        else NoteDoc.fromJson(note.doc).filter { it.type == BlockType.Todo && !it.checked && it.due > 0L }.minOfOrNull { it.due } ?: 0L
    }
    val border = when {
        selected -> BorderStroke(2.dp, c.primary)
        tone.hairline -> BorderStroke(1.dp, c.outlineVariant)
        else -> null
    }
    Column(
        Modifier.fillMaxWidth().clip(shape).background(tone.container)
            .then(if (border != null) Modifier.border(border, shape) else Modifier)
            .combinedClickable(onClick = onClick, onLongClick = onLongClick),
    ) {
    if (note.cover != 0) {
        val ctx = androidx.compose.ui.platform.LocalContext.current
        val photo = if (note.cover < 0 && note.coverPhoto.isNotEmpty()) java.io.File(ctx.filesDir, "notes/${note.id}/${note.coverPhoto}") else null
        NoteCover(note.cover, photo, Modifier.fillMaxWidth().height(if (compact) 64.dp else 84.dp), animate = false, light = true)
    }
    val pad = if (compact) 12.dp else 16.dp
    Column(Modifier.fillMaxWidth().padding(horizontal = pad, vertical = if (compact) 10.dp else 14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        Row(verticalAlignment = Alignment.Top, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            if (note.icon.isNotEmpty()) NoteIconTile(note.icon, if (compact) 24.dp else 30.dp, container = tone.content.copy(alpha = 0.12f), content = tone.content)
            if (note.title.isNotBlank()) {
                Text(
                    note.title,
                    style = if (compact) MaterialTheme.typography.titleSmall else MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold, color = tone.content, maxLines = 2, overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f).padding(top = if (note.icon.isNotEmpty()) 2.dp else 0.dp),
                )
            } else Box(Modifier.weight(1f))
            if (selected) Icon(Icons.Outlined.Check, null, tint = readableOn(c.primary, tone.container, 3f), modifier = Modifier.size(20.dp))
            else if (note.pinned) Icon(Icons.Outlined.PushPin, "Pinned", tint = readableOn(tone.content, tone.container, 3f), modifier = Modifier.size(16.dp))
        }
        lines.forEach { line ->
            when (line) {
                is PreviewLine.Plain -> Text(
                    line.text, style = MaterialTheme.typography.bodySmall.copy(lineHeight = 18.sp), color = tone.content.copy(alpha = 0.86f),
                    maxLines = if (compact) 2 else 3, overflow = TextOverflow.Ellipsis,
                )
                is PreviewLine.Check -> Row(verticalAlignment = Alignment.Top, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Box(
                        Modifier.padding(top = 3.dp).size(14.dp).clip(RoundedCornerShape(4.dp))
                            .background(if (line.done) c.primary else tone.content.copy(alpha = 0.18f)),
                        contentAlignment = Alignment.Center,
                    ) { if (line.done) Icon(Icons.Outlined.Check, null, tint = c.onPrimary, modifier = Modifier.size(10.dp)) }
                    Text(
                        line.text, style = MaterialTheme.typography.bodySmall.copy(lineHeight = 18.sp),
                        color = tone.content.copy(alpha = if (line.done) 0.6f else 0.86f),
                        maxLines = 2, overflow = TextOverflow.Ellipsis,
                    )
                }
            }
        }
        if (pics.isNotEmpty()) {
            val ctx = androidx.compose.ui.platform.LocalContext.current
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                pics.take(if (compact) 2 else 3).forEach { path ->
                    coil.compose.AsyncImage(
                        model = remember(path) { coil.request.ImageRequest.Builder(ctx).data(java.io.File(path)).size(320).build() },
                        contentDescription = null,
                        contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                        modifier = Modifier.weight(1f).height(if (compact) 52.dp else 64.dp).clip(RoundedCornerShape(12.dp)).background(tone.content.copy(alpha = 0.08f)),
                    )
                }
                if (pics.size > (if (compact) 2 else 3)) Text(
                    "+${pics.size - (if (compact) 2 else 3)}", style = MaterialTheme.typography.labelMedium, color = tone.content.copy(alpha = 0.7f),
                    modifier = Modifier.align(Alignment.CenterVertically),
                )
            }
        }
        if (note.tagList.isNotEmpty()) {
            Row(Modifier.nebHorizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                note.tagList.take(3).forEach { t ->
                    Text(
                        "#$t", style = MaterialTheme.typography.labelSmall, color = tone.content,
                        modifier = Modifier.clip(RoundedCornerShape(8.dp)).background(tone.content.copy(alpha = 0.10f)).padding(horizontal = 8.dp, vertical = 3.dp),
                    )
                }
            }
        }
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(dateLabel(note.updatedAt), style = MaterialTheme.typography.labelSmall, color = tone.content.copy(alpha = 0.6f), modifier = Modifier.weight(1f))
            if (nextDue > 0L) Text(
                NoteDue.label(nextDue), style = MaterialTheme.typography.labelSmall,
                color = if (NoteDue.overdue(nextDue)) c.error else tone.content,
                modifier = Modifier.padding(end = 8.dp).clip(RoundedCornerShape(8.dp)).background(tone.content.copy(alpha = 0.10f)).padding(horizontal = 8.dp, vertical = 3.dp),
            )
            if (total > 0) Text("$done/$total", style = MaterialTheme.typography.labelSmall, color = tone.content.copy(alpha = 0.6f))
        }
    }
    }
}
