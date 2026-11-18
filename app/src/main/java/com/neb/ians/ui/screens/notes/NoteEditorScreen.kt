@file:OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.notes

import android.Manifest
import android.content.pm.PackageManager
import androidx.activity.compose.BackHandler
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.animation.scaleOut
import androidx.compose.animation.scaleIn
import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import com.neb.ians.ui.components.nebHorizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.Archive
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.Checklist
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material.icons.outlined.Code
import androidx.compose.material.icons.outlined.ContentCopy
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.DeleteForever
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.Category
import androidx.compose.material.icons.outlined.Image
import androidx.compose.material.icons.outlined.FormatBold
import androidx.compose.material.icons.outlined.FormatItalic
import androidx.compose.material.icons.outlined.FormatListBulleted
import androidx.compose.material.icons.outlined.FormatListNumbered
import androidx.compose.material.icons.outlined.FormatQuote
import androidx.compose.material.icons.outlined.GraphicEq
import androidx.compose.material.icons.outlined.HorizontalRule
import androidx.compose.material.icons.outlined.Mic
import androidx.compose.material.icons.outlined.MoreVert
import androidx.compose.material.icons.outlined.Palette
import androidx.compose.material.icons.outlined.Pause
import androidx.compose.material.icons.outlined.PlayArrow
import androidx.compose.material.icons.outlined.PushPin
import androidx.compose.material.icons.outlined.Redo
import androidx.compose.material.icons.outlined.RestoreFromTrash
import androidx.compose.material.icons.outlined.Share
import androidx.compose.material.icons.outlined.SkipNext
import androidx.compose.material.icons.outlined.SkipPrevious
import androidx.compose.material.icons.outlined.Stop
import androidx.compose.material.icons.outlined.Title
import androidx.compose.material.icons.outlined.Undo
import androidx.compose.material.icons.outlined.Unarchive
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material.icons.outlined.VolumeUp
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.CircularProgressIndicator
import com.neb.ians.ui.components.NebDropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.layout.layout
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.layout.positionInWindow
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.material.icons.outlined.TextFormat
import androidx.compose.material.icons.outlined.AutoAwesome
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.speech.DictationState
import com.neb.ians.speech.ModelState
import com.neb.ians.speech.ReadState
import com.neb.ians.ui.components.NebModalSheet
import com.neb.ians.ui.components.shareText
import com.neb.ians.util.TactileType
import com.neb.ians.util.rememberTactileFeedback
import kotlin.math.PI
import kotlin.math.max
import kotlin.math.sin

private enum class Setup { Dictate, Listen }

@Composable
fun NoteEditorScreen(
    onNavigateBack: () -> Unit,
    onOpenNote: (String) -> Unit,
    onOpenVoice: () -> Unit,
    vm: NoteEditorViewModel = hiltViewModel(),
    speech: SpeechViewModel = hiltViewModel(),
) {
    val c = MaterialTheme.colorScheme
    val context = LocalContext.current
    val tactile = rememberTactileFeedback()
    val focusManager = LocalFocusManager.current

    val ready by vm.ready.collectAsStateWithLifecycle()
    val title by vm.title.collectAsStateWithLifecycle()
    val blocks by vm.blocks.collectAsStateWithLifecycle()
    val notice by vm.notice.collectAsStateWithLifecycle()
    val registry = remember { BlockFieldRegistry() }
    val toneIndex by vm.tone.collectAsStateWithLifecycle()
    val iconKey by vm.icon.collectAsStateWithLifecycle()
    val coverIndex by vm.cover.collectAsStateWithLifecycle()
    val coverPhoto by vm.coverPhoto.collectAsStateWithLifecycle()
    val paperKind by vm.paper.collectAsStateWithLifecycle()
    val bgName by vm.bgPhoto.collectAsStateWithLifecycle()
    val backdrop by rememberBackdrop(if (bgName.isEmpty()) null else vm.coverFile(bgName))
    val bgPicker = androidx.activity.compose.rememberLauncherForActivityResult(
        androidx.activity.result.contract.ActivityResultContracts.PickVisualMedia(),
    ) { uri -> if (uri != null) vm.setBgPhoto(uri) }
    val tags by vm.tags.collectAsStateWithLifecycle()
    val pinned by vm.pinned.collectAsStateWithLifecycle()
    val archived by vm.archived.collectAsStateWithLifecycle()
    val trashed by vm.trashed.collectAsStateWithLifecycle()
    val canUndo by vm.canUndo.collectAsStateWithLifecycle()
    val canRedo by vm.canRedo.collectAsStateWithLifecycle()
    val dictation by vm.dictation.collectAsStateWithLifecycle()
    val readState by vm.readState.collectAsStateWithLifecycle()
    val sttState by speech.stt.collectAsStateWithLifecycle()
    val ttsState by speech.tts.collectAsStateWithLifecycle()

    val tone = noteTone(toneIndex)
    val bg = if (toneIndex == 0) c.surface else tone.container
    val fg = readableOn(if (toneIndex == 0) c.onSurface else tone.content, bg, 7f)
    val pinTint = readableOn(c.primary, bg, 3f)

    var setup by remember { mutableStateOf<Setup?>(null) }
    var menu by remember { mutableStateOf(false) }
    var toneSheet by remember { mutableStateOf(false) }
    var barOpen by rememberSaveable { mutableStateOf(true) }
    var iconSheet by remember { mutableStateOf(false) }
    var coverSheet by remember { mutableStateOf(false) }
    var tagDialog by remember { mutableStateOf(false) }
    var confirmDelete by remember { mutableStateOf(false) }
    val titleFocus = remember { FocusRequester() }

    val listening = dictation is DictationState.Listening || dictation is DictationState.Preparing
    val reading = readState is ReadState.Speaking || readState is ReadState.Paused || readState is ReadState.Loading

    val micPermission = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        if (granted) vm.startDictation()
    }

    fun beginDictation() {
        when {
            sttState !is ModelState.Installed -> setup = Setup.Dictate
            ContextCompat.checkSelfPermission(context, Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED ->
                vm.startDictation()
            else -> micPermission.launch(Manifest.permission.RECORD_AUDIO)
        }
    }

    fun beginListening() {
        if (ttsState !is ModelState.Installed) setup = Setup.Listen else vm.listen()
    }

    fun leave() {
        vm.flush()
        onNavigateBack()
    }

    BackHandler { leave() }
    DisposableEffect(Unit) { onDispose { vm.flush() } }

    LaunchedEffect(ready) {
        if (!ready) return@LaunchedEffect
        if (vm.startDictating) beginDictation()
        else if (vm.isNew) runCatching { titleFocus.requestFocus() }
    }

    Column(Modifier.fillMaxSize().background(bg).statusBarsPadding().navigationBarsPadding().imePadding()) {
        // ---- top bar
        Row(Modifier.fillMaxWidth().padding(horizontal = 4.dp, vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
            IconButton(onClick = { leave() }) { Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back", tint = fg) }
            Spacer(Modifier.weight(1f))
            if (!trashed) {
                IconButton(onClick = vm::undo, enabled = canUndo) { Icon(Icons.Outlined.Undo, "Undo", tint = if (canUndo) fg else softReadable(fg, bg, 0.5f)) }
                IconButton(onClick = vm::redo, enabled = canRedo) { Icon(Icons.Outlined.Redo, "Redo", tint = if (canRedo) fg else softReadable(fg, bg, 0.5f)) }
            }
            IconButton(onClick = { if (reading) vm.readStop() else beginListening() }) {
                Icon(if (reading) Icons.Outlined.Stop else Icons.Outlined.VolumeUp, if (reading) "Stop reading" else "Read aloud", tint = fg)
            }
            if (!trashed) {
                IconButton(onClick = vm::togglePin) {
                    Icon(Icons.Outlined.PushPin, if (pinned) "Unpin" else "Pin", tint = if (pinned) pinTint else fg)
                }
            }
            Box {
                IconButton(onClick = { menu = true }) { Icon(Icons.Outlined.MoreVert, "More", tint = fg) }
                NebDropdownMenu(
                    expanded = menu, onDismissRequest = { menu = false },
                ) {
                    val words = NoteDoc.wordCount(blocks)
                    DropdownMenuItem(
                        text = { Text("$words words \u00B7 ${max(1, words / 200)} min", color = c.onSurfaceVariant, style = MaterialTheme.typography.labelLarge) },
                        onClick = {}, enabled = false,
                    )
                    if (trashed) {
                        MenuItem("Restore", Icons.Outlined.RestoreFromTrash) { menu = false; vm.restoreFromBin() }
                        MenuItem("Delete forever", Icons.Outlined.DeleteForever, danger = true) { menu = false; confirmDelete = true }
                    } else {
                        MenuItem("Appearance", Icons.Outlined.Palette) { menu = false; toneSheet = true }
                        MenuItem("Add tag", Icons.Outlined.Add) { menu = false; tagDialog = true }
                        MenuItem("Share", Icons.Outlined.Share) { menu = false; shareText(context, vm.shareText()) }
                        MenuItem("Duplicate", Icons.Outlined.ContentCopy) { menu = false; vm.duplicate(onOpenNote) }
                        MenuItem(if (archived) "Unarchive" else "Archive", if (archived) Icons.Outlined.Unarchive else Icons.Outlined.Archive) {
                            menu = false; vm.toggleArchive(); if (!archived) leave()
                        }
                        MenuItem("Voice settings", Icons.Outlined.GraphicEq) { menu = false; onOpenVoice() }
                        MenuItem("Move to bin", Icons.Outlined.Delete, danger = true) { menu = false; vm.moveToBin(onNavigateBack) }
                    }
                }
            }
        }

        // ---- content
        val bodyScroll = rememberScrollState()
        val reorder = remember { BlockReorder() }
        reorder.scroller = bodyScroll
        Column(
            Modifier.weight(1f).fillMaxWidth()
                .onGloballyPositioned {
                    val at = it.positionInWindow().y
                    reorder.viewTop = at
                    reorder.viewBottom = at + it.size.height
                }
                .noteBackdrop({ backdrop }, bg.copy(alpha = 0.78f))
                .verticalScroll(bodyScroll)
                .notePaper(paperKind, fg),
        ) {
            NotePageHeader(
                icon = iconKey, cover = coverIndex, photo = if (coverPhoto.isEmpty()) null else vm.coverFile(coverPhoto), fg = fg, container = if (toneIndex == 0) c.surfaceContainerHigh else fg.copy(alpha = 0.12f),
                editable = !trashed, onIcon = { iconSheet = true }, onCover = { coverSheet = true },
                onClearCover = { vm.setCover(0) },
            )
            Column(Modifier.fillMaxWidth().padding(horizontal = 22.dp)) {
            BasicTextField(
                value = title, onValueChange = vm::setTitle, readOnly = trashed,
                textStyle = MaterialTheme.typography.headlineLarge.copy(color = fg, fontWeight = FontWeight.Bold),
                cursorBrush = SolidColor(c.primary),
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Next),
                keyboardActions = KeyboardActions(onNext = { vm.focusFirst() }),
                decorationBox = { inner ->
                    Box {
                        if (title.isEmpty()) Text("Untitled", style = MaterialTheme.typography.headlineLarge, fontWeight = FontWeight.Bold, color = softReadable(fg, bg, 0.5f))
                        inner()
                    }
                },
                modifier = Modifier.fillMaxWidth().padding(top = 8.dp).focusRequester(titleFocus),
            )
            if (tags.isNotEmpty() || !trashed) {
                FlowRow(
                    Modifier.fillMaxWidth().padding(top = 10.dp, bottom = 6.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    tags.forEach { t ->
                        Row(
                            Modifier.clip(RoundedCornerShape(10.dp)).background(fg.copy(alpha = 0.10f))
                                .clickable(enabled = !trashed) { vm.removeTag(t) }.padding(start = 10.dp, end = 8.dp, top = 5.dp, bottom = 5.dp),
                            verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp),
                        ) {
                            Text("#$t", style = MaterialTheme.typography.labelMedium, color = fg)
                            if (!trashed) Icon(Icons.Outlined.Close, "Remove tag", tint = fg.copy(alpha = 0.6f), modifier = Modifier.size(14.dp))
                        }
                    }
                    if (!trashed && tags.size < 8) {
                        Row(
                            Modifier.clip(RoundedCornerShape(10.dp)).clickable { tagDialog = true }.padding(horizontal = 8.dp, vertical = 5.dp),
                            verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp),
                        ) {
                            Icon(Icons.Outlined.Add, null, tint = fg.copy(alpha = 0.6f), modifier = Modifier.size(16.dp))
                            Text("Tag", style = MaterialTheme.typography.labelMedium, color = fg.copy(alpha = 0.6f))
                        }
                    }
                }
            }
            val todoTotal = blocks.count { it.type == BlockType.Todo }
            if (todoTotal > 0) {
                val todoDone = blocks.count { it.type == BlockType.Todo && it.checked }
                TodoProgress(todoDone, todoTotal, fg, trashed) { vm.clearDone() }
            }
            Spacer(Modifier.height(6.dp))
            NoteBlockEditor(blocks, vm, registry, readOnly = trashed, fg = fg, modifier = Modifier.padding(top = 4.dp), reorder = reorder)
            Spacer(Modifier.height(40.dp))
            }
        }

        // ---- dock
        Column(
            Modifier.fillMaxWidth().animateContentSize(),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            AnimatedVisibility(reading, enter = expandVertically() + fadeIn(), exit = shrinkVertically() + fadeOut()) {
                ReadBar(vm)
            }
            (readState as? ReadState.Error)?.let { ErrorBar(it.message, vm::clearReadError) }
            AnimatedVisibility(listening || dictation is DictationState.Finishing || dictation is DictationState.Error,
                enter = expandVertically() + fadeIn(), exit = shrinkVertically() + fadeOut()) {
                DictationStrip(vm)
            }
            notice?.let { ErrorBar(it, vm::clearNotice) }
            if (!trashed) {
                AnimatedVisibility(barOpen, enter = expandVertically(spring(stiffness = 500f)) + fadeIn(), exit = shrinkVertically() + fadeOut()) {
                    BlockFormatBar(
                        blocks = blocks, vm = vm, registry = registry, fg = fg,
                        modifier = Modifier.padding(start = 12.dp, end = 16.dp, top = 4.dp, bottom = 10.dp),
                        onCollapse = { barOpen = false },
                    ) {
                        Spacer(Modifier.width(8.dp))
                        MicButton(listening = listening, level = vm.level) {
                            tactile.perform(TactileType.LightTap)
                            if (listening) vm.stopDictation() else beginDictation()
                        }
                    }
                }
                AnimatedVisibility(!barOpen, enter = expandVertically() + fadeIn(), exit = shrinkVertically() + fadeOut()) {
                    Row(Modifier.fillMaxWidth().padding(start = 16.dp, end = 16.dp, top = 4.dp, bottom = 10.dp), verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            Modifier.size(40.dp).clip(RoundedCornerShape(20.dp)).background(c.surfaceContainerHigh).clickable { barOpen = true },
                            contentAlignment = Alignment.Center,
                        ) { Icon(Icons.Outlined.TextFormat, "Show toolbar", tint = c.onSurface) }
                        Spacer(Modifier.weight(1f))
                        MicButton(listening = listening, level = vm.level) {
                            tactile.perform(TactileType.LightTap)
                            if (listening) vm.stopDictation() else beginDictation()
                        }
                    }
                }
            }
        }
    }

    if (iconSheet) {
        NoteIconSheet(current = iconKey, onPick = { vm.setIcon(it); iconSheet = false }, onDismiss = { iconSheet = false })
    }
    if (coverSheet) {
        NoteCoverSheet(
            current = coverIndex, onPick = { vm.setCover(it); coverSheet = false },
            onPhoto = { vm.setCoverPhoto(it); coverSheet = false }, onDismiss = { coverSheet = false },
        )
    }
    if (toneSheet) {
        NoteSheet(onDismiss = { toneSheet = false }, title = "Appearance") {
            Column(Modifier.heightIn(max = 560.dp).verticalScroll(rememberScrollState()), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text("Themes", style = MaterialTheme.typography.labelLarge, color = c.onSurfaceVariant)
                NoteThemeRow(toneIndex) { th -> vm.setTone(th.tone); vm.setCover(th.cover); vm.setIcon(th.icon); vm.setPaper(th.paper) }
                Text("Colour", style = MaterialTheme.typography.labelLarge, color = c.onSurfaceVariant)
                ToneSwatches(current = toneIndex, onPick = { vm.setTone(it) })
                Text("Paper", style = MaterialTheme.typography.labelLarge, color = c.onSurfaceVariant)
                PaperPicker(paperKind) { vm.setPaper(it) }
                Text("Page picture", style = MaterialTheme.typography.labelLarge, color = c.onSurfaceVariant)
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    GhostChip(if (bgName.isEmpty()) "Add picture" else "Change picture", Icons.Outlined.Image, Modifier.weight(1f)) {
                        bgPicker.launch(androidx.activity.result.PickVisualMediaRequest(androidx.activity.result.contract.ActivityResultContracts.PickVisualMedia.ImageOnly))
                    }
                    if (bgName.isNotEmpty()) GhostChip("Remove", Icons.Outlined.Delete, Modifier.weight(1f)) { vm.setBgPhoto(null) }
                }
                Row(Modifier.fillMaxWidth().padding(top = 4.dp, bottom = 16.dp), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    GhostChip(if (iconKey.isEmpty()) "Add icon" else "Change icon", Icons.Outlined.Category, Modifier.weight(1f)) { toneSheet = false; iconSheet = true }
                    GhostChip(if (coverIndex == 0) "Add cover" else "Change cover", Icons.Outlined.Image, Modifier.weight(1f)) { toneSheet = false; coverSheet = true }
                }
            }
        }
    }
    if (setup != null) {
        VoiceSetupSheet(
            forDictation = setup == Setup.Dictate,
            onReady = {
                val kind = setup
                setup = null
                if (kind == Setup.Dictate) beginDictation() else vm.listen()
            },
            onDismiss = { setup = null },
            vm = speech,
        )
    }
    if (tagDialog) TagDialog(onAdd = { vm.addTag(it); tagDialog = false }, onDismiss = { tagDialog = false })
    if (confirmDelete) {
        AlertDialog(
            onDismissRequest = { confirmDelete = false },
            shape = RoundedCornerShape(28.dp), containerColor = com.neb.ians.ui.theme.nebFloatColor(),
            title = { Text("Delete forever?") },
            text = { Text("This note will be gone for good.") },
            confirmButton = { TextButton(onClick = { confirmDelete = false; vm.deleteForever(onNavigateBack) }) { Text("Delete", color = c.error) } },
            dismissButton = { TextButton(onClick = { confirmDelete = false }) { Text("Keep") } },
        )
    }
}

/** The cover and its Change / Remove pills. Own function so no ColumnScope receiver leaks into AnimatedVisibility. */
@Composable
private fun NoteCoverArea(cover: Int, photo: java.io.File?, editable: Boolean, onCover: () -> Unit, onClearCover: () -> Unit) {
    var tools by remember { mutableStateOf(false) }
    LaunchedEffect(tools) { if (tools) { kotlinx.coroutines.delay(4200); tools = false } }
    Box(
        Modifier.fillMaxWidth().heightIn(min = 140.dp, max = 216.dp).aspectRatio(NoteCoverFrameAspect)
            .then(if (editable) Modifier.clickable(interactionSource = remember { MutableInteractionSource() }, indication = null) { tools = !tools } else Modifier),
    ) {
        NoteCover(cover, photo, Modifier.matchParentSize())
        if (editable) {
            AnimatedVisibility(
                visible = tools,
                modifier = Modifier.align(Alignment.BottomEnd),
                enter = fadeIn(tween(140)) + scaleIn(spring(dampingRatio = 0.7f, stiffness = 500f), initialScale = 0.86f),
                exit = fadeOut(tween(120)) + scaleOut(targetScale = 0.9f),
            ) {
                Row(Modifier.padding(12.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    HeaderPill("Change", Icons.Outlined.Image, { tools = false; onCover() })
                    HeaderPill(null, Icons.Outlined.Close, { tools = false; onClearCover() }, "Remove cover")
                }
            }
        }
    }
}

/**
 * The top of the page: the cover runs edge to edge, the icon tile overlaps its lower edge, and a
 * page with neither shows two quiet actions. Changing the cover or icon springs the new one in.
 */
@Composable
private fun NotePageHeader(
    icon: String, cover: Int, photo: java.io.File?, fg: Color, container: Color,
    editable: Boolean, onIcon: () -> Unit, onCover: () -> Unit, onClearCover: () -> Unit,
) {
    val c = MaterialTheme.colorScheme
    val hasIcon = icon.isNotEmpty()
    val hasCover = cover != 0
    Column(Modifier.fillMaxWidth().animateContentSize(spring(dampingRatio = 0.8f, stiffness = 380f))) {
        if (hasCover) NoteCoverArea(cover, photo, editable, onCover, onClearCover)
        if (hasIcon) {
            Box(
                Modifier.padding(start = 22.dp, top = if (hasCover) 0.dp else 8.dp)
                    .then(
                        if (hasCover) Modifier.layout { m, constraints ->
                            val placeable = m.measure(constraints)
                            val pull = 30.dp.roundToPx()
                            layout(placeable.width, placeable.height - pull) { placeable.place(0, -pull) }
                        } else Modifier
                    )
                    .let { if (editable) it.clip(RoundedCornerShape(20.dp)).clickable(onClick = onIcon) else it },
            ) {
                NoteIconTile(icon, 64.dp, container = container, content = fg)
            }
        }
        if (editable && (!hasIcon || !hasCover)) {
            Row(
                Modifier.padding(start = 18.dp, top = if (hasIcon && hasCover) 0.dp else 6.dp),
                horizontalArrangement = Arrangement.spacedBy(4.dp),
            ) {
                if (!hasIcon) GhostAction("Add icon", Icons.Outlined.Category, fg, onIcon)
                if (!hasCover) GhostAction("Add cover", Icons.Outlined.Image, fg, onCover)
            }
        }
    }
}

@Composable
private fun HeaderPill(label: String?, icon: ImageVector, onClick: () -> Unit, description: String? = null) {
    val c = MaterialTheme.colorScheme
    Row(
        Modifier.height(36.dp).clip(RoundedCornerShape(18.dp)).background(c.surface).clickable(onClick = onClick)
            .padding(start = 10.dp, end = if (label == null) 10.dp else 14.dp),
        verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp),
    ) {
        Icon(icon, description, tint = c.onSurface, modifier = Modifier.size(16.dp))
        if (label != null) Text(label, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.SemiBold, color = c.onSurface)
    }
}

@Composable
private fun GhostAction(label: String, icon: ImageVector, fg: Color, onClick: () -> Unit) {
    Row(
        Modifier.clip(RoundedCornerShape(50)).clickable(onClick = onClick).padding(horizontal = 10.dp, vertical = 7.dp),
        verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp),
    ) {
        Icon(icon, null, tint = fg.copy(alpha = 0.6f), modifier = Modifier.size(18.dp))
        Text(label, style = MaterialTheme.typography.labelLarge, color = fg.copy(alpha = 0.6f))
    }
}

@Composable
private fun MenuItem(label: String, icon: ImageVector, danger: Boolean = false, onClick: () -> Unit) {
    val color = if (danger) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface
    DropdownMenuItem(
        text = { Text(label, color = color) },
        leadingIcon = { Icon(icon, null, tint = color, modifier = Modifier.size(20.dp)) },
        onClick = onClick,
    )
}

@Composable
private fun ToolButton(icon: ImageVector, label: String, tint: Color, onClick: () -> Unit) {
    val tactile = rememberTactileFeedback()
    Box(
        Modifier.size(44.dp).clip(RoundedCornerShape(14.dp)).clickable { tactile.perform(TactileType.LightTap); onClick() },
        contentAlignment = Alignment.Center,
    ) { Icon(icon, label, tint = tint, modifier = Modifier.size(22.dp)) }
}

@Composable
private fun MicButton(listening: Boolean, level: kotlinx.coroutines.flow.StateFlow<Float>, onClick: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val lvl by level.collectAsStateWithLifecycle()
    val pulse by animateFloatAsState(if (listening) 1f + lvl * 0.14f else 1f, tween(90), label = "micPulse")
    Surface(
        onClick = onClick,
        shape = RoundedCornerShape(if (listening) 14.dp else 20.dp),
        color = if (listening) c.error else c.primary,
        contentColor = if (listening) c.onError else c.onPrimary,
        modifier = Modifier.size(40.dp).scale(pulse),
    ) {
        Box(contentAlignment = Alignment.Center) {
            Icon(if (listening) Icons.Outlined.Stop else Icons.Outlined.Mic, if (listening) "Stop dictation" else "Dictate", modifier = Modifier.size(20.dp))
        }
    }
}

private fun clock(seconds: Int) = "%d:%02d".format(seconds / 60, seconds % 60)

@Composable
private fun DictationStrip(vm: NoteEditorViewModel) {
    val c = MaterialTheme.colorScheme
    val state by vm.dictation.collectAsStateWithLifecycle()
    val level by vm.level.collectAsStateWithLifecycle()
    val pending by vm.pending.collectAsStateWithLifecycle()
    val seconds by vm.seconds.collectAsStateWithLifecycle()
    if (state is DictationState.Error) {
        ErrorBar((state as DictationState.Error).message, vm::clearDictationError)
        return
    }
    Surface(
        shape = RoundedCornerShape(24.dp), color = c.primaryContainer, contentColor = c.onPrimaryContainer,
        modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp),
    ) {
        Row(Modifier.padding(horizontal = 16.dp, vertical = 12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
            if (state is DictationState.Listening) LevelBars(level, c.primary) else CircularProgressIndicator(Modifier.size(24.dp), strokeWidth = 2.5.dp, color = c.primary)
            Column(Modifier.weight(1f)) {
                Text(
                    when (state) {
                        is DictationState.Preparing -> "Loading model"
                        is DictationState.Finishing -> "Finishing"
                        else -> "Listening  ${clock(seconds)}"
                    },
                    style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold,
                )
                if (pending.isNotBlank()) {
                    Text(pending, style = MaterialTheme.typography.bodySmall, fontStyle = FontStyle.Italic, maxLines = 2, overflow = TextOverflow.Ellipsis)
                }
            }
        }
    }
}

@Composable
private fun LevelBars(level: Float, color: Color) {
    val t = rememberInfiniteTransition(label = "bars")
    val phase by t.animateFloat(0f, (2 * PI).toFloat(), infiniteRepeatable(tween(900, easing = LinearEasing), RepeatMode.Restart), label = "phase")
    val smooth by animateFloatAsState(level, tween(120), label = "level")
    Canvas(Modifier.size(width = 52.dp, height = 28.dp)) {
        val n = 7
        val gap = 4.dp.toPx()
        val w = (size.width - gap * (n - 1)) / n
        for (i in 0 until n) {
            val wave = 0.5f + 0.5f * sin(phase + i * 0.9f)
            val h = size.height * (0.18f + 0.82f * (smooth.coerceIn(0f, 1f) * wave))
            drawRoundRect(
                color, topLeft = Offset(i * (w + gap), (size.height - h) / 2f),
                size = androidx.compose.ui.geometry.Size(w, h), cornerRadius = CornerRadius(w / 2f),
            )
        }
    }
}

@Composable
private fun ReadBar(vm: NoteEditorViewModel) {
    val c = MaterialTheme.colorScheme
    val state by vm.readState.collectAsStateWithLifecycle()
    val progress by vm.readProgress.collectAsStateWithLifecycle()
    Surface(
        shape = RoundedCornerShape(24.dp), color = c.secondaryContainer, contentColor = c.onSecondaryContainer,
        modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp),
    ) {
        Column(Modifier.padding(start = 16.dp, end = 8.dp, top = 12.dp, bottom = 6.dp)) {
            val p = progress
            if (p != null) {
                LinearProgressIndicator(
                    progress = { (p.index + 1f) / p.total },
                    modifier = Modifier.fillMaxWidth().padding(end = 8.dp).height(4.dp).clip(RoundedCornerShape(2.dp)),
                    color = c.primary, trackColor = c.onSecondaryContainer.copy(alpha = 0.12f),
                )
            }
            Row(verticalAlignment = Alignment.CenterVertically) {
                if (state is ReadState.Loading) {
                    CircularProgressIndicator(Modifier.size(20.dp), strokeWidth = 2.dp, color = c.primary)
                    Spacer(Modifier.width(12.dp))
                }
                Text(
                    if (state is ReadState.Loading) "Loading voice" else p?.text.orEmpty(),
                    style = MaterialTheme.typography.bodySmall, maxLines = 2, overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f).padding(vertical = 8.dp),
                )
                IconButton(onClick = vm::readPrevious) { Icon(Icons.Outlined.SkipPrevious, "Previous") }
                Surface(
                    onClick = vm::readPause, shape = RoundedCornerShape(16.dp), color = c.primary, contentColor = c.onPrimary,
                    modifier = Modifier.size(44.dp),
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(if (state is ReadState.Paused) Icons.Outlined.PlayArrow else Icons.Outlined.Pause, if (state is ReadState.Paused) "Resume" else "Pause")
                    }
                }
                IconButton(onClick = vm::readNext) { Icon(Icons.Outlined.SkipNext, "Next") }
                IconButton(onClick = vm::readStop) { Icon(Icons.Outlined.Close, "Stop") }
            }
        }
    }
}

@Composable
private fun ErrorBar(message: String, onDismiss: () -> Unit) {
    val c = MaterialTheme.colorScheme
    Surface(
        shape = RoundedCornerShape(20.dp), color = c.errorContainer, contentColor = c.onErrorContainer,
        modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp),
    ) {
        Row(Modifier.padding(start = 16.dp, end = 4.dp, top = 4.dp, bottom = 4.dp), verticalAlignment = Alignment.CenterVertically) {
            Text(message, style = MaterialTheme.typography.bodyMedium, modifier = Modifier.weight(1f).padding(vertical = 8.dp))
            IconButton(onClick = onDismiss) { Icon(Icons.Outlined.Close, "Dismiss") }
        }
    }
}

@Composable
private fun TagDialog(onAdd: (String) -> Unit, onDismiss: () -> Unit) {
    var text by remember { mutableStateOf(TextFieldValue("")) }
    val c = MaterialTheme.colorScheme
    AlertDialog(
        onDismissRequest = onDismiss,
        shape = RoundedCornerShape(28.dp), containerColor = com.neb.ians.ui.theme.nebFloatColor(),
        title = { Text("Add tag") },
        text = {
            OutlinedTextField(
                value = text, onValueChange = { text = it }, singleLine = true, shape = RoundedCornerShape(16.dp),
                prefix = { Text("#") },
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                keyboardActions = KeyboardActions(onDone = { onAdd(text.text) }),
            )
        },
        confirmButton = { TextButton(onClick = { onAdd(text.text) }, enabled = text.text.isNotBlank()) { Text("Add") } },
        dismissButton = { TextButton(onClick = onDismiss) { Text("Cancel") } },
    )
}

@Composable
private fun GhostChip(label: String, icon: ImageVector, modifier: Modifier, onClick: () -> Unit) {
    val c = MaterialTheme.colorScheme
    Row(
        modifier.height(48.dp).clip(RoundedCornerShape(24.dp)).background(c.surfaceContainerHigh).clickable(onClick = onClick),
        verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp, Alignment.CenterHorizontally),
    ) {
        Icon(icon, null, tint = c.onSurfaceVariant, modifier = Modifier.size(18.dp))
        Text(label, style = MaterialTheme.typography.labelLarge, color = c.onSurface)
    }
}

/** A slim bar and a count above the list of to-dos; the bar fills with a spring as items are ticked. */
@Composable
private fun TodoProgress(done: Int, total: Int, fg: Color, readOnly: Boolean, onClear: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val p by androidx.compose.animation.core.animateFloatAsState(
        if (total == 0) 0f else done.toFloat() / total,
        androidx.compose.animation.core.spring(dampingRatio = 0.7f, stiffness = 300f), label = "todo_progress",
    )
    Row(Modifier.fillMaxWidth().padding(top = 6.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
        Box(Modifier.weight(1f).height(6.dp).clip(RoundedCornerShape(3.dp)).background(fg.copy(alpha = 0.12f))) {
            Box(Modifier.fillMaxWidth(p).height(6.dp).clip(RoundedCornerShape(3.dp)).background(c.primary))
        }
        Text("$done of $total", style = MaterialTheme.typography.labelMedium, color = fg.copy(alpha = 0.7f))
        if (done > 0 && !readOnly) {
            Text(
                "Clear", style = MaterialTheme.typography.labelMedium, color = c.primary,
                modifier = Modifier.clip(RoundedCornerShape(12.dp)).clickable(onClick = onClear).padding(horizontal = 8.dp, vertical = 6.dp),
            )
        }
    }
}
