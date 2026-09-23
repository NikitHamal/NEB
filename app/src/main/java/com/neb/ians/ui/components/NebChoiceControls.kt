package com.neb.ians.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.NebAuthTokens
import com.neb.ians.ui.theme.NebMotion
import com.neb.ians.util.TactileType

// ---------------------------------------------------------------------------
// Choosing. Three shapes cover every pick the app asks for: a row for a choice
// that needs explaining, a token for a set, and a segmented bank for two to four
// one-word answers.
//
// None of them is outlined while resting. An unselected choice is a quiet filled
// surface with no border at all; selection is what draws a line, lifts the fill
// to the page colour and closes a mark. That inversion is the whole idea — the
// screen stays calm until the user has answered, and their answer is the only
// thing on it with an edge.
// ---------------------------------------------------------------------------

/** The selection mark: an open ring that closes into a filled disc and draws a tick. */
@Composable
fun NebSelectionMark(
    selected: Boolean,
    modifier: Modifier = Modifier,
    diameter: Dp = 24.dp
) {
    val palette = LocalNebAuthPalette.current
    val progress by animateFloatAsState(
        targetValue = if (selected) 1f else 0f,
        animationSpec = tween(NebMotion.Short, easing = NebMotion.Decelerate),
        label = "neb_mark"
    )
    Canvas(modifier = modifier.size(diameter)) {
        val r = size.minDimension / 2f
        val center = Offset(r, r)
        val ringWidth = r * 0.16f

        if (progress < 0.999f) {
            drawCircle(
                color = palette.hairlineStrong.copy(alpha = 1f - progress),
                radius = r - ringWidth / 2f,
                center = center,
                style = Stroke(width = ringWidth)
            )
        }
        if (progress > 0.001f) {
            drawCircle(color = palette.sapphire, radius = r * progress, center = center)
        }
        if (progress > 0.35f) {
            val t = ((progress - 0.35f) / 0.65f).coerceIn(0f, 1f)
            val a = Offset(center.x - r * 0.38f, center.y + r * 0.02f)
            val b = Offset(center.x - r * 0.09f, center.y + r * 0.30f)
            val c = Offset(center.x + r * 0.40f, center.y - r * 0.28f)
            val tick = Path().apply {
                moveTo(a.x, a.y)
                if (t <= 0.5f) {
                    val k = t / 0.5f
                    lineTo(a.x + (b.x - a.x) * k, a.y + (b.y - a.y) * k)
                } else {
                    val k = (t - 0.5f) / 0.5f
                    lineTo(b.x, b.y)
                    lineTo(b.x + (c.x - b.x) * k, b.y + (c.y - b.y) * k)
                }
            }
            drawPath(
                path = tick,
                color = palette.onSapphire,
                style = Stroke(width = r * 0.17f, cap = StrokeCap.Round)
            )
        }
    }
}

/**
 * A choice that owns a whole row: role, intent, institution type — anything that
 * needs a line of explanation under it. Resting it is a flat field tile; picking
 * it lifts the fill to the page, morphs the corner out and closes the mark.
 */
@Composable
fun NebOptionCard(
    title: String,
    subtitle: String?,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    leading: (@Composable () -> Unit)? = null,
    trailing: (@Composable () -> Unit)? = null
) {
    val palette = LocalNebAuthPalette.current
    val fill by animateColorAsState(
        targetValue = if (selected) palette.card else palette.field,
        animationSpec = tween(NebMotion.Short),
        label = "neb_option_fill"
    )
    val edge by animateColorAsState(
        targetValue = if (selected) palette.sapphire else Color.Transparent,
        animationSpec = tween(NebMotion.Short),
        label = "neb_option_edge"
    )
    val edgeWidth by animateDpAsState(
        targetValue = if (selected) 1.6.dp else 0.dp,
        animationSpec = tween(NebMotion.Short),
        label = "neb_option_edge_w"
    )
    val radius by animateDpAsState(
        targetValue = if (selected) 22.dp else 16.dp,
        animationSpec = tween(NebMotion.Standard, easing = NebMotion.Decelerate),
        label = "neb_option_radius"
    )
    val titleColor by animateColorAsState(
        targetValue = if (selected) palette.sapphire else palette.ink,
        animationSpec = tween(NebMotion.Short),
        label = "neb_option_title"
    )
    val shape = RoundedCornerShape(radius)

    Row(
        modifier = modifier
            .fillMaxWidth()
            .clip(shape)
            .background(fill)
            .border(edgeWidth, edge, shape)
            .nebPressable(scale = 0.985f, tactile = TactileType.SelectionChange, onClick = onClick)
            .padding(start = 18.dp, end = 16.dp, top = 15.dp, bottom = 15.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (leading != null) {
            leading()
            Spacer(modifier = Modifier.width(14.dp))
        }
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = title,
                style = NebAuthType.Title.copy(fontSize = 15.5.sp),
                color = titleColor
            )
            if (!subtitle.isNullOrBlank()) {
                Spacer(modifier = Modifier.height(3.dp))
                Text(text = subtitle, style = NebAuthType.Caption, color = palette.inkMuted)
            }
        }
        Spacer(modifier = Modifier.width(12.dp))
        if (trailing != null) trailing() else NebSelectionMark(selected = selected)
    }
}

/**
 * A token in a set: subjects, levels, provinces. Unselected it is a bare label on
 * the field tint; selected it takes a sapphire edge, a sapphire wash and a tick
 * that slides its own width open ahead of the text.
 */
@Composable
fun NebSelectChip(
    label: String,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val palette = LocalNebAuthPalette.current
    val fill by animateColorAsState(
        targetValue = if (selected) palette.sapphireSoft else palette.field,
        animationSpec = tween(NebMotion.Quick),
        label = "neb_chip_fill"
    )
    val content by animateColorAsState(
        targetValue = if (selected) palette.sapphire else palette.inkMuted,
        animationSpec = tween(NebMotion.Quick),
        label = "neb_chip_fg"
    )
    val edge by animateColorAsState(
        targetValue = if (selected) palette.sapphire else Color.Transparent,
        animationSpec = tween(NebMotion.Quick),
        label = "neb_chip_edge"
    )
    val tickWidth by animateDpAsState(
        targetValue = if (selected) 18.dp else 0.dp,
        animationSpec = tween(NebMotion.Short, easing = NebMotion.Decelerate),
        label = "neb_chip_tick"
    )
    val shape = RoundedCornerShape(14.dp)

    Row(
        modifier = modifier
            .clip(shape)
            .background(fill)
            .border(NebAuthTokens.Hairline, edge, shape)
            .nebPressable(scale = 0.95f, tactile = TactileType.SelectionChange, onClick = onClick)
            .padding(horizontal = 14.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (tickWidth > 0.dp) {
            Box(
                modifier = Modifier.width(tickWidth),
                contentAlignment = Alignment.CenterStart
            ) {
                NebTick(color = content, modifier = Modifier.size(13.dp))
            }
        }
        Text(
            text = label,
            style = NebAuthType.Caption.copy(fontWeight = FontWeight.SemiBold, fontSize = 13.sp),
            color = content
        )
    }
}

/**
 * Two to four one-word answers side by side, sharing one track. A stacked list of
 * cards for three words is a form; a single bank of equal tiles is an answer.
 */
@Composable
fun NebChoiceRow(
    options: List<String>,
    selected: String?,
    onSelect: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val palette = LocalNebAuthPalette.current
    Row(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(18.dp))
            .background(palette.field)
            .padding(5.dp),
        horizontalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        options.forEach { option ->
            val isOn = option == selected
            val fill by animateColorAsState(
                targetValue = if (isOn) palette.card else Color.Transparent,
                animationSpec = tween(NebMotion.Short),
                label = "neb_seg_fill"
            )
            val edge by animateColorAsState(
                targetValue = if (isOn) palette.sapphire else Color.Transparent,
                animationSpec = tween(NebMotion.Short),
                label = "neb_seg_edge"
            )
            val content by animateColorAsState(
                targetValue = if (isOn) palette.sapphire else palette.inkMuted,
                animationSpec = tween(NebMotion.Short),
                label = "neb_seg_fg"
            )
            val shape = RoundedCornerShape(14.dp)
            Box(
                modifier = Modifier
                    .weight(1f)
                    .heightIn(min = 52.dp)
                    .clip(shape)
                    .background(fill)
                    .border(if (isOn) 1.4.dp else 0.dp, edge, shape)
                    .nebPressable(scale = 0.97f, tactile = TactileType.SelectionChange) { onSelect(option) },
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = option,
                    style = NebAuthType.Body.copy(fontWeight = FontWeight.SemiBold, fontSize = 14.sp),
                    color = content,
                    textAlign = TextAlign.Center,
                    modifier = Modifier.padding(horizontal = 6.dp)
                )
            }
        }
    }
}

/** A bare tick, for anywhere a chip or a row needs one without a disc behind it. */
@Composable
fun NebTick(color: Color, modifier: Modifier = Modifier) {
    Canvas(modifier = modifier) {
        val w = size.width
        val h = size.height
        val path = Path().apply {
            moveTo(w * 0.14f, h * 0.52f)
            lineTo(w * 0.40f, h * 0.78f)
            lineTo(w * 0.88f, h * 0.20f)
        }
        drawPath(path, color, style = Stroke(width = w * 0.15f, cap = StrokeCap.Round))
    }
}

/** A rounded glyph tile, for the leading slot of an option card. */
@Composable
fun NebGlyphTile(
    selected: Boolean,
    modifier: Modifier = Modifier,
    size: Dp = 40.dp,
    content: @Composable () -> Unit
) {
    val palette = LocalNebAuthPalette.current
    val fill by animateColorAsState(
        targetValue = if (selected) palette.sapphireSoft else palette.card,
        animationSpec = tween(NebMotion.Short),
        label = "neb_glyph_fill"
    )
    Box(
        modifier = modifier
            .size(size)
            .clip(RoundedCornerShape(size / 3f))
            .background(fill),
        contentAlignment = Alignment.Center,
        content = { content() }
    )
}

/** A circle, for the leading slot of a list row that wants no square. */
@Composable
fun NebDotTile(color: Color, modifier: Modifier = Modifier, diameter: Dp = 8.dp) {
    Box(
        modifier = modifier
            .size(diameter)
            .clip(CircleShape)
            .background(color)
    )
}

/**
 * A setting that is simply on or off. The track is a hairline until it is on,
 * so a row of these reads as a list rather than as a wall of coloured pills.
 */
@Composable
fun NebToggleRow(
    title: String,
    subtitle: String?,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true
) {
    val palette = LocalNebAuthPalette.current
    val track by animateColorAsState(
        targetValue = if (checked) palette.sapphire else palette.field,
        animationSpec = tween(NebMotion.Short),
        label = "neb_toggle_track"
    )
    val knob by animateColorAsState(
        targetValue = if (checked) palette.onSapphire else palette.hairlineStrong,
        animationSpec = tween(NebMotion.Short),
        label = "neb_toggle_knob"
    )
    val knobOffset by animateDpAsState(
        targetValue = if (checked) 20.dp else 0.dp,
        animationSpec = tween(NebMotion.Short, easing = NebMotion.Decelerate),
        label = "neb_toggle_offset"
    )

    Row(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(NebAuthTokens.FieldRadius))
            .nebPressable(enabled = enabled, tactile = TactileType.SelectionChange) { onCheckedChange(!checked) }
            .padding(horizontal = 16.dp, vertical = 14.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(text = title, style = NebAuthType.Body, color = palette.ink)
            if (subtitle != null) {
                Spacer(modifier = Modifier.height(3.dp))
                Text(text = subtitle, style = NebAuthType.Caption, color = palette.inkFaint)
            }
        }
        Spacer(modifier = Modifier.width(14.dp))
        Box(
            modifier = Modifier
                .width(46.dp)
                .height(26.dp)
                .clip(CircleShape)
                .background(track),
            contentAlignment = Alignment.CenterStart
        ) {
            Box(
                modifier = Modifier
                    .padding(horizontal = 3.dp)
                    .offset(x = knobOffset)
                    .size(20.dp)
                    .clip(CircleShape)
                    .background(knob)
            )
        }
    }
}
