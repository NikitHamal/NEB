package com.neb.ians.ui.screens.reader.pdf

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.gestures.detectHorizontalDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.FormatAlignJustify
import androidx.compose.material.icons.outlined.FormatAlignLeft
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.setProgress
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.components.NebToggleRow
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.Poppins
import kotlin.math.roundToInt

/** The size the reading type is built on; [ReadingSettings.fontScale] is a multiple of it. */
internal const val READING_BASE_SP = 18f

/** One tonal card of the reading sheet: its surface, its ink, and the strong colour for what is selected. */
private class RdTone(val surface: Color, val ink: Color, val strong: Color, val onStrong: Color, val soft: Color)

private val LightTones = mapOf(
    "size" to RdTone(Color(0xFFDCE5FF), Color(0xFF001A41), Color(0xFF0058DF), Color.White, Color(0xFFB9CBF7)),
    "line" to RdTone(Color(0xFFFFE2BC), Color(0xFF2B1700), Color(0xFF8A4F00), Color.White, Color(0xFFF5C98C)),
    "margin" to RdTone(Color(0xFFCDEFE0), Color(0xFF00281A), Color(0xFF006C4C), Color.White, Color(0xFFA6DCC5)),
    "face" to RdTone(Color(0xFFE6DEFF), Color(0xFF1D0B5A), Color(0xFF5B3CC4), Color.White, Color(0xFFCFC3F5)),
    "align" to RdTone(Color(0xFFDEE1FF), Color(0xFF00164E), Color(0xFF0050CB), Color.White, Color(0xFFC1C9F2)),
    "bright" to RdTone(Color(0xFFFFDDE0), Color(0xFF3E0010), Color(0xFFB3213F), Color.White, Color(0xFFF7BCC4))
)

private val DarkTones = mapOf(
    "size" to RdTone(Color(0xFF1B2D52), Color(0xFFD9E3FF), Color(0xFF9DB9FF), Color(0xFF002A70), Color(0xFF34497A)),
    "line" to RdTone(Color(0xFF3B2A12), Color(0xFFFFE2BC), Color(0xFFFFB866), Color(0xFF462800), Color(0xFF5A4122)),
    "margin" to RdTone(Color(0xFF14342A), Color(0xFFCDEFE0), Color(0xFF7DDBB1), Color(0xFF00382A), Color(0xFF285243)),
    "face" to RdTone(Color(0xFF2B2450), Color(0xFFE6DEFF), Color(0xFFC9BDFF), Color(0xFF2C1578), Color(0xFF433B73)),
    "align" to RdTone(Color(0xFF212949), Color(0xFFDEE1FF), Color(0xFFAEC2FF), Color(0xFF002C7A), Color(0xFF383F66)),
    "bright" to RdTone(Color(0xFF3F1C25), Color(0xFFFFDDE0), Color(0xFFFFB2BD), Color(0xFF5E0A21), Color(0xFF5A303A))
)

private val CardShape = RoundedCornerShape(24.dp)

/** Text size, line spacing, margins, typeface, alignment, brightness and page colour, plus the zen and Neby AI switches. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReadingSheet(
    settings: ReadingSettings,
    theme: ReadingTheme,
    assistantHidden: Boolean,
    onSettings: ((ReadingSettings) -> ReadingSettings) -> Unit,
    onTheme: (ReadingTheme) -> Unit,
    onAssistantHidden: (Boolean) -> Unit,
    onDismiss: () -> Unit
) {
    val dark = MaterialTheme.colorScheme.background.luminance() < 0.5f
    val tones = if (dark) DarkTones else LightTones
    val sheetColor = if (dark) MaterialTheme.colorScheme.surfaceContainerLow else Color(0xFFF3F4F9)
    val cardWhite = if (dark) MaterialTheme.colorScheme.surfaceContainerHigh else Color.White
    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true),
        containerColor = sheetColor,
        contentColor = MaterialTheme.colorScheme.onSurface,
        scrimColor = MaterialTheme.colorScheme.scrim.copy(alpha = 0.40f),
        shape = RoundedCornerShape(topStart = 32.dp, topEnd = 32.dp),
        dragHandle = {
            Box(Modifier.fillMaxWidth().padding(top = 12.dp, bottom = 2.dp), contentAlignment = Alignment.Center) {
                Box(Modifier.width(36.dp).height(4.dp).clip(CircleShape).background(MaterialTheme.colorScheme.outlineVariant))
            }
        }
    ) {
        Column(
            Modifier
                .verticalScroll(rememberScrollState())
                .navigationBarsPadding()
                .padding(horizontal = 14.dp)
                .padding(bottom = 16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                "Reading",
                style = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.Bold, fontSize = 26.sp, color = MaterialTheme.colorScheme.onSurface),
                modifier = Modifier.padding(start = 8.dp, top = 4.dp, bottom = 4.dp)
            )

            // text size
            val sp = (settings.fontScale * READING_BASE_SP)
            val sizeTone = tones.getValue("size")
            RdCard(sizeTone) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    RdCardLabel("Text size", sizeTone)
                    Spacer(Modifier.weight(1f))
                    RdBigValue("${sp.roundToInt()}sp", sizeTone)
                }
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text("A", style = TextStyle(fontFamily = FontFamily.Serif, fontWeight = FontWeight.Bold, fontSize = 15.sp, color = sizeTone.ink))
                    RdSlider(
                        sp, 13f..54f, 1f, sizeTone, "Text size", "${sp.roundToInt()} sp", Modifier.weight(1f)
                    ) { v -> onSettings { it.copy(fontScale = v / READING_BASE_SP) } }
                    Text("A", style = TextStyle(fontFamily = FontFamily.Serif, fontWeight = FontWeight.Bold, fontSize = 30.sp, color = sizeTone.ink))
                }
            }

            // line spacing and margins
            Row(Modifier.height(IntrinsicSize.Max), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                val lineTone = tones.getValue("line")
                val lineSp = (sp * 1.55f * settings.lineSpacing).roundToInt()
                RdCard(lineTone, Modifier.weight(1f).fillMaxHeight()) {
                    RdCardLabel("Line spacing", lineTone)
                    RdBigValue("${lineSp}sp", lineTone)
                    Spacer(Modifier.weight(1f, fill = false))
                    RdSlider(
                        settings.lineSpacing, 0.8f..1.6f, 0.05f, lineTone, "Line spacing", "$lineSp sp"
                    ) { v -> onSettings { it.copy(lineSpacing = v) } }
                }
                val marginTone = tones.getValue("margin")
                RdCard(marginTone, Modifier.weight(1f).fillMaxHeight()) {
                    RdCardLabel("Margins", marginTone)
                    Spacer(Modifier.weight(1f, fill = false))
                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
                        listOf("Narrow", "Normal", "Wide").forEachIndexed { m, name ->
                            RdChoice(
                                selected = settings.margin == m, tone = marginTone, label = name,
                                modifier = Modifier.weight(1f).height(48.dp)
                            ) { onSettings { it.copy(margin = m) } }
                        }
                    }
                }
            }

            // typeface
            val faceTone = tones.getValue("face")
            RdCard(faceTone) {
                RdCardLabel("Typeface", faceTone)
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                    RdFaceChoice("Serif", FontFamily.Serif, settings.font == ReadingFont.Serif, faceTone, Modifier.weight(1.15f)) { onSettings { it.copy(font = ReadingFont.Serif) } }
                    RdFaceChoice("Sans", Poppins, settings.font == ReadingFont.Sans, faceTone, Modifier.weight(1f)) { onSettings { it.copy(font = ReadingFont.Sans) } }
                }
            }

            // alignment and brightness
            Row(Modifier.height(IntrinsicSize.Max), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                val alignTone = tones.getValue("align")
                RdCard(alignTone, Modifier.weight(1f).fillMaxHeight()) {
                    RdCardLabel("Alignment", alignTone)
                    Spacer(Modifier.weight(1f, fill = false))
                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
                        RdIconChoice(Icons.Outlined.FormatAlignLeft, "Left", !settings.justify, alignTone, Modifier.weight(1f)) { onSettings { it.copy(justify = false) } }
                        RdIconChoice(Icons.Outlined.FormatAlignJustify, "Justified", settings.justify, alignTone, Modifier.weight(1f)) { onSettings { it.copy(justify = true) } }
                    }
                }
                val brightTone = tones.getValue("bright")
                val auto = settings.brightness < 0f
                RdCard(brightTone, Modifier.weight(1f).fillMaxHeight()) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        RdCardLabel("Brightness", brightTone)
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        RdBigValue(if (auto) "Auto" else "${(settings.brightness * 100).roundToInt()}%", brightTone)
                        Spacer(Modifier.weight(1f))
                        if (!auto) {
                            Box(
                                Modifier
                                    .clip(CircleShape)
                                    .background(brightTone.strong)
                                    .nebPressable(onClick = { onSettings { it.copy(brightness = -1f) } })
                                    .padding(horizontal = 12.dp, vertical = 6.dp)
                            ) {
                                Text("Auto", style = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.SemiBold, fontSize = 12.sp, color = brightTone.onStrong))
                            }
                        }
                    }
                    Spacer(Modifier.weight(1f, fill = false))
                    RdSlider(
                        if (auto) 0.5f else settings.brightness, 0.05f..1f, 0.05f, brightTone, "Brightness",
                        if (auto) "Auto" else "${(settings.brightness * 100).roundToInt()} percent"
                    ) { v -> onSettings { it.copy(brightness = v) } }
                }
            }

            // page colour: only the page, no names
            RdCard(RdTone(cardWhite, MaterialTheme.colorScheme.onSurface, MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.onPrimary, cardWhite)) {
                Text("Page colour", style = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.SemiBold, fontSize = 13.sp, color = MaterialTheme.colorScheme.onSurface))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                    RdPageTile("Paper", Color.White, Color(0xFF16171A), theme == ReadingTheme.Paper, Modifier.weight(1f)) { onTheme(ReadingTheme.Paper) }
                    RdPageTile("Sepia", Color(0xFFF4ECD8), Color(0xFF3B2F23), theme == ReadingTheme.Sepia, Modifier.weight(1f)) { onTheme(ReadingTheme.Sepia) }
                    RdPageTile("Night", Color(0xFF141414), Color(0xFFE2E0DA), theme == ReadingTheme.Night, Modifier.weight(1f)) { onTheme(ReadingTheme.Night) }
                }
            }

            // switches
            RdCard(RdTone(cardWhite, MaterialTheme.colorScheme.onSurface, MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.onPrimary, cardWhite), gap = 0.dp) {
                NebToggleRow("Zen mode", null, settings.zen, { v -> onSettings { it.copy(zen = v) }; if (v) onDismiss() })
                NebToggleRow("Hide answers until tapped", null, settings.hideAnswers, { v -> onSettings { it.copy(hideAnswers = v) } })
                NebToggleRow("Neby AI button", null, !assistantHidden, { v -> onAssistantHidden(!v) })
            }
        }
    }
}

@Composable
private fun RdCard(tone: RdTone, modifier: Modifier = Modifier, gap: androidx.compose.ui.unit.Dp = 10.dp, content: @Composable androidx.compose.foundation.layout.ColumnScope.() -> Unit) {
    Column(
        modifier.clip(CardShape).background(tone.surface).padding(horizontal = 16.dp, vertical = 14.dp),
        verticalArrangement = Arrangement.spacedBy(gap),
        content = content
    )
}

@Composable
private fun RdCardLabel(text: String, tone: RdTone) {
    Text(text, style = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.SemiBold, fontSize = 13.sp, color = tone.ink))
}

@Composable
private fun RdBigValue(text: String, tone: RdTone) {
    Text(text, style = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.Bold, fontSize = 30.sp, lineHeight = 34.sp, color = tone.ink))
}

/**
 * A slider that can be seen and found with a thumb: a thick rail, a strong fill that runs to a round thumb,
 * a step that is felt (a light tick of the haptics) and a role for screen readers.
 */
@Composable
private fun RdSlider(
    value: Float,
    range: ClosedFloatingPointRange<Float>,
    step: Float,
    tone: RdTone,
    label: String,
    shown: String,
    modifier: Modifier = Modifier,
    onChange: (Float) -> Unit
) {
    val density = LocalDensity.current
    val haptic = LocalHapticFeedback.current
    val knob = 30.dp
    val knobPx = with(density) { knob.toPx() }
    val span = range.endInclusive - range.start
    val frac = ((value - range.start) / span).coerceIn(0f, 1f)
    var width by remember { mutableIntStateOf(0) }
    val latest by rememberUpdatedState(onChange)
    val current by rememberUpdatedState(value)
    fun at(x: Float): Float {
        val room = (width - knobPx).coerceAtLeast(1f)
        val f = ((x - knobPx / 2f) / room).coerceIn(0f, 1f)
        val raw = range.start + f * span
        return ((raw / step).roundToInt() * step).coerceIn(range.start, range.endInclusive)
    }
    fun push(v: Float) {
        if (kotlin.math.abs(v - current) > step * 0.5f) haptic.performHapticFeedback(HapticFeedbackType.TextHandleMove)
        latest(v)
    }
    val knobX = frac * (width - knobPx).coerceAtLeast(0f)
    val fillWidth = with(density) { (knobX + knobPx / 2f).toDp() }
    Box(
        modifier
            .fillMaxWidth()
            .height(40.dp)
            .onSizeChanged { width = it.width }
            .pointerInput(range, step) { detectTapGestures { push(at(it.x)) } }
            .pointerInput(range, step) {
                detectHorizontalDragGestures(onDragStart = { push(at(it.x)) }) { change, _ ->
                    change.consume()
                    push(at(change.position.x))
                }
            }
            .semantics {
                contentDescription = label
                stateDescription = shown
                setProgress { v -> latest(((v / step).roundToInt() * step).coerceIn(range.start, range.endInclusive)); true }
            },
        contentAlignment = Alignment.CenterStart
    ) {
        Box(Modifier.fillMaxWidth().height(14.dp).clip(CircleShape).background(tone.soft))
        Box(Modifier.width(fillWidth).height(14.dp).clip(CircleShape).background(tone.strong))
        Box(
            Modifier
                .offset { IntOffset(knobX.roundToInt(), 0) }
                .size(knob)
                .clip(CircleShape)
                .background(tone.strong)
        ) {
            Box(Modifier.align(Alignment.Center).size(10.dp).clip(CircleShape).background(tone.onStrong))
        }
    }
}

/** A segment with a line icon of the margin it sets. */
@Composable
private fun RdChoice(selected: Boolean, tone: RdTone, label: String, modifier: Modifier, onClick: () -> Unit) {
    val bg by animateColorAsState(if (selected) tone.strong else tone.soft, label = "rd-choice-bg")
    val ink by animateColorAsState(if (selected) tone.onStrong else tone.ink, label = "rd-choice-ink")
    val corner by animateDpAsState(if (selected) 24.dp else 14.dp, label = "rd-choice-corner")
    val bar = when (label) { "Narrow" -> 20.dp; "Normal" -> 15.dp; else -> 10.dp }
    Box(
        modifier
            .clip(RoundedCornerShape(corner))
            .background(bg)
            .nebPressable(onClick = onClick)
            .semantics { contentDescription = "$label margins"; stateDescription = if (selected) "Selected" else "Not selected" },
        contentAlignment = Alignment.Center
    ) {
        Column(verticalArrangement = Arrangement.spacedBy(3.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            repeat(3) { Box(Modifier.width(bar).height(2.5.dp).clip(CircleShape).background(ink)) }
        }
    }
}

@Composable
private fun RdIconChoice(icon: androidx.compose.ui.graphics.vector.ImageVector, label: String, selected: Boolean, tone: RdTone, modifier: Modifier, onClick: () -> Unit) {
    val bg by animateColorAsState(if (selected) tone.strong else tone.soft, label = "rd-icon-bg")
    val ink by animateColorAsState(if (selected) tone.onStrong else tone.ink, label = "rd-icon-ink")
    val corner by animateDpAsState(if (selected) 24.dp else 14.dp, label = "rd-icon-corner")
    Box(
        modifier
            .height(48.dp)
            .clip(RoundedCornerShape(corner))
            .background(bg)
            .nebPressable(onClick = onClick)
            .semantics { contentDescription = label; stateDescription = if (selected) "Selected" else "Not selected" },
        contentAlignment = Alignment.Center
    ) {
        Icon(icon, null, tint = ink, modifier = Modifier.size(22.dp))
    }
}

@Composable
private fun RdFaceChoice(name: String, family: FontFamily, selected: Boolean, tone: RdTone, modifier: Modifier, onClick: () -> Unit) {
    val bg by animateColorAsState(if (selected) tone.strong else tone.soft, label = "rd-face-bg")
    val ink by animateColorAsState(if (selected) tone.onStrong else tone.ink, label = "rd-face-ink")
    val corner by animateDpAsState(if (selected) 36.dp else 20.dp, label = "rd-face-corner")
    Row(
        modifier
            .heightIn(min = 64.dp)
            .clip(RoundedCornerShape(corner))
            .background(bg)
            .nebPressable(onClick = onClick)
            .padding(horizontal = 18.dp)
            .semantics { contentDescription = "$name typeface"; stateDescription = if (selected) "Selected" else "Not selected" },
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.Center
    ) {
        Text("Ag", style = TextStyle(fontFamily = family, fontWeight = FontWeight.SemiBold, fontSize = 32.sp, color = ink))
        Spacer(Modifier.width(10.dp))
        Text(name, style = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.SemiBold, fontSize = 14.sp, color = ink))
    }
}

/** A page colour shown as the page itself: "Aa" in its ink on its paper, the chosen one outlined in the brand blue. */
@Composable
private fun RdPageTile(name: String, paper: Color, ink: Color, selected: Boolean, modifier: Modifier, onClick: () -> Unit) {
    val shape = RoundedCornerShape(18.dp)
    val line by animateColorAsState(if (selected) Color(0xFF0058DF) else Color.Transparent, label = "rd-page-line")
    Box(
        modifier
            .height(56.dp)
            .clip(shape)
            .background(paper)
            .border(2.5.dp, line, shape)
            .nebPressable(onClick = onClick)
            .semantics { contentDescription = "$name page"; stateDescription = if (selected) "Selected" else "Not selected" },
        contentAlignment = Alignment.Center
    ) {
        Text("Aa", style = TextStyle(fontFamily = FontFamily.Serif, fontWeight = FontWeight.SemiBold, fontSize = 24.sp, color = ink))
    }
}
