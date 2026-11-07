@file:OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.notes

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Download
import androidx.compose.material.icons.outlined.Mic
import androidx.compose.material.icons.outlined.PlayArrow
import androidx.compose.material.icons.outlined.RecordVoiceOver
import androidx.compose.material.icons.outlined.Stop
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.speech.ModelState
import com.neb.ians.speech.LocalTtsCatalog
import com.neb.ians.speech.LocalTtsId
import com.neb.ians.speech.LocalTtsInfo
import com.neb.ians.speech.PhononVoice
import com.neb.ians.speech.ReadState
import com.neb.ians.speech.SpeechCatalog
import com.neb.ians.speech.SpeechModelId
import com.neb.ians.speech.VoiceCatalog
import com.neb.ians.ui.components.NebModalSheet

internal fun formatBytes(b: Long): String =
    if (b >= 1_000_000) String.format(java.util.Locale.US, "%.1f MB", b / 1_000_000.0)
    else String.format(java.util.Locale.US, "%d KB", (b / 1000).coerceAtLeast(1))

/** Tonal filter chip: secondary container when chosen, a hairline outline when not. */
@Composable
internal fun ToneChip(
    label: String,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    icon: ImageVector? = null,
) {
    val c = MaterialTheme.colorScheme
    Surface(
        onClick = onClick,
        modifier = modifier,
        shape = RoundedCornerShape(14.dp),
        color = if (selected) c.secondaryContainer else c.surfaceContainerLowest,
        contentColor = if (selected) c.onSecondaryContainer else c.onSurfaceVariant,
        border = if (selected) null else BorderStroke(1.dp, c.outlineVariant),
    ) {
        Row(
            Modifier.padding(horizontal = 14.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            if (icon != null) Icon(icon, null, Modifier.size(16.dp))
            Text(label, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.Medium)
        }
    }
}

@Composable
fun VoiceModelsScreen(
    onNavigateBack: () -> Unit,
    vm: SpeechViewModel = hiltViewModel(),
) {
    LaunchedEffect(Unit) { vm.loadCatalog() }
    Scaffold(
        containerColor = MaterialTheme.colorScheme.surface,
        topBar = {
            Row(
                Modifier.fillMaxWidth().statusBarsPadding().padding(horizontal = 8.dp, vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                IconButton(onClick = onNavigateBack) { Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back") }
                Text("Voice", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold)
            }
        },
    ) { inner ->
        LazyColumn(
            Modifier.fillMaxSize().padding(inner),
            contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 4.dp, bottom = 40.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            item { SttModelCard(vm, showLanguages = true) }
            item { TtsModelCard(vm, showVoices = true) }
            items(LocalTtsCatalog.all, key = { it.id.key }) { info -> LocalTtsCard(vm, info) }
        }
    }
}

@Composable
private fun ModelShell(
    icon: ImageVector,
    title: String,
    meta: String,
    state: ModelState,
    supported: Boolean,
    onDownload: () -> Unit,
    onCancel: () -> Unit,
    onRemove: () -> Unit,
    content: @Composable () -> Unit = {},
) {
    val c = MaterialTheme.colorScheme
    var confirm by remember { mutableStateOf(false) }
    Surface(
        shape = RoundedCornerShape(28.dp),
        color = c.surfaceContainerLowest,
        border = BorderStroke(1.dp, c.outlineVariant),
    ) {
        Column(Modifier.fillMaxWidth().padding(20.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                Box(
                    Modifier.size(48.dp).clip(RoundedCornerShape(16.dp)).background(c.primaryContainer),
                    contentAlignment = Alignment.Center,
                ) { Icon(icon, null, tint = c.onPrimaryContainer) }
                Column(Modifier.weight(1f)) {
                    Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                    Text(meta, style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant)
                }
            }
            when {
                !supported -> Text("Not supported on this phone", style = MaterialTheme.typography.bodyMedium, color = c.error)
                state is ModelState.NotInstalled -> DownloadButton("Download", onDownload)
                state is ModelState.Failed -> {
                    Text(state.message, style = MaterialTheme.typography.bodyMedium, color = c.error)
                    DownloadButton("Try again", onDownload)
                }
                state is ModelState.Downloading -> {
                    LinearProgressIndicator(
                        progress = { state.fraction },
                        modifier = Modifier.fillMaxWidth().height(8.dp).clip(RoundedCornerShape(4.dp)),
                        strokeCap = StrokeCap.Round,
                        trackColor = c.surfaceContainerHighest,
                    )
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            "${formatBytes(state.done)} of ${formatBytes(state.total)}",
                            style = MaterialTheme.typography.bodyMedium,
                            color = c.onSurfaceVariant,
                            modifier = Modifier.weight(1f),
                        )
                        TextButton(onClick = onCancel) { Text("Cancel") }
                    }
                }
                state is ModelState.Installed -> {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Outlined.CheckCircle, null, tint = c.primary, modifier = Modifier.size(20.dp))
                        Spacer(Modifier.size(8.dp))
                        Text(
                            "Ready \u00B7 ${formatBytes(state.bytes)}",
                            style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium,
                            modifier = Modifier.weight(1f),
                        )
                        TextButton(onClick = { confirm = true }) {
                            Text("Remove", color = c.error)
                        }
                    }
                    content()
                }
            }
        }
    }
    if (confirm) {
        AlertDialog(
            onDismissRequest = { confirm = false },
            shape = RoundedCornerShape(28.dp),
            containerColor = c.surfaceContainerHigh,
            title = { Text("Remove $title?") },
            text = { Text("You can download it again at any time.") },
            confirmButton = { TextButton(onClick = { confirm = false; onRemove() }) { Text("Remove", color = c.error) } },
            dismissButton = { TextButton(onClick = { confirm = false }) { Text("Keep") } },
        )
    }
}

@Composable
private fun DownloadButton(label: String, onClick: () -> Unit) {
    val c = MaterialTheme.colorScheme
    Surface(
        onClick = onClick,
        shape = RoundedCornerShape(28.dp),
        color = c.primary,
        contentColor = c.onPrimary,
        modifier = Modifier.fillMaxWidth().height(52.dp),
    ) {
        Row(Modifier.fillMaxSize(), horizontalArrangement = Arrangement.Center, verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Outlined.Download, null, Modifier.size(20.dp))
            Spacer(Modifier.size(8.dp))
            Text(label, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold)
        }
    }
}

@Composable
fun SttModelCard(vm: SpeechViewModel, showLanguages: Boolean) {
    val state by vm.stt.collectAsStateWithLifecycle()
    val lang by vm.sttLanguage.collectAsStateWithLifecycle()
    ModelShell(
        icon = Icons.Outlined.Mic,
        title = "Speech to text",
        meta = "${SpeechCatalog.WHISTLE_LABEL} \u00B7 ${formatBytes(SpeechCatalog.totalBytes(SpeechModelId.Whistle))}",
        state = state,
        supported = vm.sttSupported,
        onDownload = { vm.download(SpeechModelId.Whistle) },
        onCancel = { vm.cancel(SpeechModelId.Whistle) },
        onRemove = { vm.remove(SpeechModelId.Whistle) },
    ) {
        if (showLanguages) {
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                SpeechCatalog.sttLanguages.forEach { (code, label) ->
                    ToneChip(label, lang == code, { vm.setSttLanguage(code) })
                }
            }
        }
    }
}

@Composable
fun TtsModelCard(vm: SpeechViewModel, showVoices: Boolean) {
    val state by vm.phononState.collectAsStateWithLifecycle()
    ModelShell(
        icon = Icons.Outlined.RecordVoiceOver,
        title = "Text to speech",
        meta = "${SpeechCatalog.PHONON_LABEL} \u00B7 ${formatBytes(SpeechCatalog.totalBytes(SpeechModelId.Phonon))}",
        state = state,
        supported = vm.ttsSupported,
        onDownload = { vm.download(SpeechModelId.Phonon) },
        onCancel = { vm.cancel(SpeechModelId.Phonon) },
        onRemove = { vm.remove(SpeechModelId.Phonon) },
    ) {
        if (showVoices) VoiceList(vm)
    }
}

@Composable
private fun VoiceList(vm: SpeechViewModel) {
    val c = MaterialTheme.colorScheme
    val installed by vm.installedVoices.collectAsStateWithLifecycle()
    val catalog by vm.catalog.collectAsStateWithLifecycle()
    val busy by vm.voiceBusy.collectAsStateWithLifecycle()
    val chosen by vm.voice.collectAsStateWithLifecycle()
    val engine by vm.engine.collectAsStateWithLifecycle()
    val selected = if (engine == "phonon") chosen else ""
    val reading by vm.readState.collectAsStateWithLifecycle()
    val remote = (catalog as? VoiceCatalog.Ready)?.voices.orEmpty()
    val remoteByName = remote.associateBy { it.name }
    val names = (listOf("default") + installed.filter { it != "default" }).distinct()
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text("Voices", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
        names.forEach { name ->
            VoiceRow(
                title = if (name == "default") "Default" else name,
                subtitle = remoteByName[name]?.let { subtitleOf(it) },
                selected = selected == name,
                installed = true,
                busy = false,
                previewing = reading != ReadState.Idle && selected == name,
                onUse = { vm.useVoice(name) },
                onPreview = { vm.preview(name) },
                onDownload = {},
                onRemove = if (name == "default") null else ({ vm.removeVoice(name) }),
            )
        }
        when (catalog) {
            VoiceCatalog.Loading -> Box(Modifier.fillMaxWidth().padding(8.dp), contentAlignment = Alignment.Center) {
                CircularProgressIndicator(Modifier.size(22.dp), strokeWidth = 2.dp)
            }
            VoiceCatalog.Unavailable -> Row(verticalAlignment = Alignment.CenterVertically) {
                Text("More voices need a connection", Modifier.weight(1f), style = MaterialTheme.typography.bodyMedium, color = c.onSurfaceVariant)
                TextButton(onClick = { vm.loadCatalog() }) { Text("Retry") }
            }
            is VoiceCatalog.Ready -> remote.filter { it.name !in installed }.forEach { v ->
                VoiceRow(
                    title = v.name,
                    subtitle = subtitleOf(v),
                    selected = false,
                    installed = false,
                    busy = v.name in busy,
                    previewing = false,
                    onUse = {},
                    onPreview = {},
                    onDownload = { vm.downloadVoice(v) },
                    onRemove = null,
                )
            }
        }
    }
}

@Composable
fun LocalTtsCard(vm: SpeechViewModel, info: LocalTtsInfo) {
    val states by vm.local.collectAsStateWithLifecycle()
    val voices by vm.localVoices.collectAsStateWithLifecycle()
    val engine by vm.engine.collectAsStateWithLifecycle()
    val reading by vm.readState.collectAsStateWithLifecycle()
    val state = states[info.id] ?: ModelState.NotInstalled
    ModelShell(
        icon = Icons.Outlined.RecordVoiceOver,
        title = info.title,
        meta = "${info.meta} \u00B7 ${formatBytes(info.bytes)}",
        state = state,
        supported = true,
        onDownload = { vm.downloadLocal(info.id) },
        onCancel = { vm.cancelLocal(info.id) },
        onRemove = { vm.removeLocal(info.id) },
    ) {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            info.voices.forEach { v ->
                val selected = engine == info.id.key && voices[info.id] == v.key
                VoiceRow(
                    title = v.label,
                    subtitle = null,
                    selected = selected,
                    installed = true,
                    busy = false,
                    previewing = reading != ReadState.Idle && selected,
                    onUse = { vm.useLocalVoice(info.id, v.key) },
                    onPreview = {
                        vm.useLocalVoice(info.id, v.key)
                        vm.previewLocal(info.id, v.key)
                    },
                    onDownload = {},
                    onRemove = null,
                )
            }
        }
    }
}

private fun subtitleOf(v: PhononVoice): String =
    listOf(v.gender, v.age).filter { it.isNotBlank() }.joinToString(" \u00B7 ") { it.replaceFirstChar(Char::uppercase) }

@Composable
private fun VoiceRow(
    title: String,
    subtitle: String?,
    selected: Boolean,
    installed: Boolean,
    busy: Boolean,
    previewing: Boolean,
    onUse: () -> Unit,
    onPreview: () -> Unit,
    onDownload: () -> Unit,
    onRemove: (() -> Unit)?,
) {
    val c = MaterialTheme.colorScheme
    Surface(
        onClick = if (installed) onUse else onDownload,
        shape = RoundedCornerShape(20.dp),
        color = if (selected) c.secondaryContainer else c.surfaceContainerLow,
        contentColor = if (selected) c.onSecondaryContainer else c.onSurface,
    ) {
        Row(
            Modifier.fillMaxWidth().padding(start = 16.dp, end = 4.dp, top = 6.dp, bottom = 6.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(Modifier.weight(1f)) {
                Text(title, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Medium)
                if (!subtitle.isNullOrBlank()) {
                    Text(subtitle, style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant)
                }
            }
            if (installed) {
                if (selected) Icon(Icons.Outlined.Check, "Selected", Modifier.padding(horizontal = 4.dp).size(20.dp))
                IconButton(onClick = onPreview) {
                    Icon(if (previewing) Icons.Outlined.Stop else Icons.Outlined.PlayArrow, if (previewing) "Stop" else "Preview")
                }
                if (onRemove != null) IconButton(onClick = onRemove) { Icon(Icons.Outlined.Delete, "Remove voice") }
            } else if (busy) {
                Box(Modifier.size(48.dp), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(Modifier.size(20.dp), strokeWidth = 2.dp)
                }
            } else {
                IconButton(onClick = onDownload) { Icon(Icons.Outlined.Download, "Download voice") }
            }
        }
    }
}

/** Shown from the editor when a voice feature is used before its model is on the phone. */
@Composable
fun VoiceSetupSheet(
    forDictation: Boolean,
    onReady: () -> Unit,
    onDismiss: () -> Unit,
    vm: SpeechViewModel = hiltViewModel(),
) {
    val sttState by vm.stt.collectAsStateWithLifecycle()
    val ttsState by vm.tts.collectAsStateWithLifecycle()
    val state = if (forDictation) sttState else ttsState
    LaunchedEffect(state) {
        if (state is ModelState.Installed) onReady()
    }
    NebModalSheet(onDismiss = onDismiss, title = if (forDictation) "Dictate your notes" else "Listen to your notes") {
        Column(Modifier.padding(bottom = 24.dp)) {
            if (forDictation) {
                SttModelCard(vm, showLanguages = false)
            } else {
                Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                    LocalTtsCard(vm, LocalTtsCatalog.info(LocalTtsId.Paradee))
                    TtsModelCard(vm, showVoices = false)
                }
            }
        }
    }
}
