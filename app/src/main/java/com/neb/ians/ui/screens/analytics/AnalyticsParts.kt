package com.neb.ians.ui.screens.analytics

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.TrendingDown
import androidx.compose.material.icons.outlined.TrendingFlat
import androidx.compose.material.icons.outlined.TrendingUp
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.NebGlyphShapes
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.compactCount
import com.neb.ians.ui.components.nebShape
import androidx.graphics.shapes.RoundedPolygon

/** Page gutter shared by every analytics card. */
internal val AnalyticsGutter = 16.dp

/** A flat tonal card, the web's `.md-card` without the frame: surface container, 28 dp radius. */
@Composable
internal fun AnalyticsCard(
    modifier: Modifier = Modifier,
    container: Color = MaterialTheme.colorScheme.surfaceContainerLow,
    contentPadding: Int = 20,
    content: @Composable () -> Unit
) {
    Box(
        modifier = modifier
            .padding(horizontal = AnalyticsGutter)
            .fillMaxWidth()
            .clip(RoundedCornerShape(28.dp))
            .background(container)
            .padding(contentPadding.dp)
    ) { content() }
}

@Composable
internal fun SectionTitle(title: String, modifier: Modifier = Modifier, trailing: (@Composable () -> Unit)? = null) {
    Row(
        modifier = modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(
            text = title,
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.onSurface,
            modifier = Modifier.weight(1f)
        )
        trailing?.invoke()
    }
}

/** A squircle-ish glyph tile, the M3 Expressive stand-in for a round icon disc. */
@Composable
internal fun GlyphTile(
    icon: ImageVector,
    modifier: Modifier = Modifier,
    size: Int = 40,
    polygon: RoundedPolygon = NebGlyphShapes.Cookie,
    container: Color = MaterialTheme.colorScheme.secondaryContainer,
    tint: Color = MaterialTheme.colorScheme.onSecondaryContainer
) {
    val shape = nebShape(polygon)
    Box(
        modifier = modifier.size(size.dp).background(container, shape),
        contentAlignment = Alignment.Center
    ) {
        Icon(icon, contentDescription = null, tint = tint, modifier = Modifier.size((size * 0.5f).dp))
    }
}

/** A tonal label: filter pills, tags and small counts keep a surface fill. */
@Composable
internal fun TonalTag(
    text: String,
    modifier: Modifier = Modifier,
    container: Color = MaterialTheme.colorScheme.secondaryContainer,
    content: Color = MaterialTheme.colorScheme.onSecondaryContainer,
    icon: ImageVector? = null
) {
    Row(
        modifier = modifier
            .clip(WebPillShape)
            .background(container)
            .padding(horizontal = 10.dp, vertical = 5.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        if (icon != null) Icon(icon, contentDescription = null, tint = content, modifier = Modifier.size(14.dp))
        Text(
            text = text,
            style = MaterialTheme.typography.labelMedium,
            fontWeight = FontWeight.SemiBold,
            color = content,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

/** Change against the previous period. Null means there was nothing to compare with. */
@Composable
internal fun DeltaTag(change: Int?, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    if (change == null) return
    val (icon, fill, ink) = when {
        change > 0 -> Triple(Icons.Outlined.TrendingUp, cs.primaryContainer, cs.onPrimaryContainer)
        change < 0 -> Triple(Icons.Outlined.TrendingDown, cs.errorContainer, cs.onErrorContainer)
        else -> Triple(Icons.Outlined.TrendingFlat, cs.surfaceContainerHighest, cs.onSurfaceVariant)
    }
    val text = if (change > 0) "+$change%" else "$change%"
    TonalTag(text = text, modifier = modifier, container = fill, content = ink, icon = icon)
}

/** Big number over a small label, the unit of every stat grid. */
@Composable
internal fun StatBlock(value: String, label: String, modifier: Modifier = Modifier) {
    Column(modifier, verticalArrangement = Arrangement.spacedBy(2.dp)) {
        Text(
            text = value,
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onSurface,
            maxLines = 1
        )
        Text(
            text = label,
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            maxLines = 2,
            overflow = TextOverflow.Ellipsis
        )
    }
}

/** Two stat blocks per row; an odd last block gets an empty partner so columns line up. */
@Composable
internal fun StatGrid(items: List<Pair<String, String>>, modifier: Modifier = Modifier) {
    Column(modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(18.dp)) {
        items.chunked(2).forEach { row ->
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                row.forEach { (value, label) -> StatBlock(value, label, Modifier.weight(1f)) }
                if (row.size == 1) Box(Modifier.weight(1f).height(1.dp))
            }
        }
    }
}

/** A labelled horizontal bar: label, count, and a rounded fill proportional to [fraction]. */
@Composable
internal fun BarRow(label: String, count: Int, fraction: Float, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    Column(modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Text(
                text = label,
                style = MaterialTheme.typography.bodyMedium,
                color = cs.onSurface,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier.weight(1f)
            )
            Text(
                text = compactCount(count),
                style = MaterialTheme.typography.labelLarge,
                fontWeight = FontWeight.SemiBold,
                color = cs.onSurface
            )
        }
        Box(
            Modifier
                .fillMaxWidth()
                .height(8.dp)
                .clip(WebPillShape)
                .background(cs.surfaceContainerHighest)
        ) {
            val f = fraction.coerceIn(0f, 1f)
            if (count > 0) {
                Box(
                    Modifier
                        .fillMaxWidth(f.coerceAtLeast(0.04f))
                        .height(8.dp)
                        .clip(WebPillShape)
                        .background(cs.primary)
                )
            }
        }
    }
}

internal fun labelName(key: String): String = when (key) {
    "accepted" -> "Accepted answer"
    "correct" -> "Correct"
    "partial" -> "Partly correct"
    "incorrect" -> "Incorrect"
    "helpful" -> "Helpful"
    "spam" -> "Spam"
    "answer" -> "Answers"
    "solution" -> "Solutions"
    "hint" -> "Hints"
    "formula" -> "Formulas"
    "comment" -> "Comments"
    else -> key.replaceFirstChar { it.uppercase() }
}

