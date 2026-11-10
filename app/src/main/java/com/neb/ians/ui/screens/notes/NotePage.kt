@file:OptIn(ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.notes

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Assignment
import androidx.compose.material.icons.outlined.Biotech
import androidx.compose.material.icons.outlined.Bolt
import androidx.compose.material.icons.outlined.Bookmark
import androidx.compose.material.icons.outlined.Brush
import androidx.compose.material.icons.outlined.Calculate
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material.icons.outlined.Code
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.Draw
import androidx.compose.material.icons.outlined.Event
import androidx.compose.material.icons.outlined.Favorite
import androidx.compose.material.icons.outlined.Flag
import androidx.compose.material.icons.outlined.Group
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.Language
import androidx.compose.material.icons.outlined.Lightbulb
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.Map
import androidx.compose.material.icons.outlined.MenuBook
import androidx.compose.material.icons.outlined.MusicNote
import androidx.compose.material.icons.outlined.Palette
import androidx.compose.material.icons.outlined.Psychology
import androidx.compose.material.icons.outlined.Public
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.Science
import androidx.compose.material.icons.outlined.Star
import androidx.compose.material.icons.outlined.Task
import androidx.compose.material.icons.outlined.Terminal
import androidx.compose.material.icons.outlined.Timer
import androidx.compose.material.icons.outlined.Translate
import androidx.compose.material.icons.outlined.Work
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.graphics.shapes.RoundedPolygon
import com.neb.ians.ui.components.NebGlyphShapes
import com.neb.ians.ui.components.NebModalSheet
import com.neb.ians.ui.components.NebTone
import com.neb.ians.ui.components.drawGlyph
import com.neb.ians.ui.components.rememberGlyphPath

/**
 * A note's page icon: a glyph from this fixed set, stored by key. Vectors only, so the icon
 * follows the theme and there is never an emoji in the data.
 */
object NoteIcons {
    val all: List<Pair<String, ImageVector>> = listOf(
        "page" to Icons.Outlined.Description,
        "book" to Icons.Outlined.MenuBook,
        "school" to Icons.Outlined.School,
        "science" to Icons.Outlined.Science,
        "bio" to Icons.Outlined.Biotech,
        "math" to Icons.Outlined.Calculate,
        "idea" to Icons.Outlined.Lightbulb,
        "mind" to Icons.Outlined.Psychology,
        "star" to Icons.Outlined.Star,
        "heart" to Icons.Outlined.Favorite,
        "flag" to Icons.Outlined.Flag,
        "bolt" to Icons.Outlined.Bolt,
        "draw" to Icons.Outlined.Draw,
        "brush" to Icons.Outlined.Brush,
        "palette" to Icons.Outlined.Palette,
        "code" to Icons.Outlined.Code,
        "terminal" to Icons.Outlined.Terminal,
        "task" to Icons.Outlined.Task,
        "assignment" to Icons.Outlined.Assignment,
        "event" to Icons.Outlined.Event,
        "timer" to Icons.Outlined.Timer,
        "work" to Icons.Outlined.Work,
        "group" to Icons.Outlined.Group,
        "home" to Icons.Outlined.Home,
        "world" to Icons.Outlined.Public,
        "language" to Icons.Outlined.Language,
        "translate" to Icons.Outlined.Translate,
        "map" to Icons.Outlined.Map,
        "music" to Icons.Outlined.MusicNote,
        "lock" to Icons.Outlined.Lock,
        "bookmark" to Icons.Outlined.Bookmark,
    )

    fun find(key: String): ImageVector? = all.firstOrNull { it.first == key }?.second
}

/** The icon tile that sits on a note's page, in the page's tone. */
@Composable
fun NoteIconTile(key: String, size: Dp, container: Color, content: Color, modifier: Modifier = Modifier) {
    val vector = NoteIcons.find(key) ?: return
    Box(
        modifier.size(size).clip(RoundedCornerShape(size * 0.32f)).background(container),
        contentAlignment = Alignment.Center,
    ) {
        Icon(vector, null, tint = content, modifier = Modifier.size(size * 0.54f))
    }
}

@Immutable
private class CoverSpec(
    val tone: NebTone,
    val a: RoundedPolygon, val ax: Float, val ay: Float, val asz: Float, val ar: Float,
    val b: RoundedPolygon, val bx: Float, val by: Float, val bsz: Float, val br: Float,
)

/** Cover 0 is none. 1..[count] are flat tonal banners with two big shapes, positions fixed per cover. */
object NoteCovers {
    const val count = 8
}

private fun coverSpec(index: Int): CoverSpec? = when (index) {
    1 -> CoverSpec(NebTone.Azure, NebGlyphShapes.Cookie, 0.82f, 0.30f, 1.9f, 12f, NebGlyphShapes.Pill, 0.18f, 0.95f, 1.0f, -20f)
    2 -> CoverSpec(NebTone.Sky, NebGlyphShapes.Flower, 0.16f, 0.35f, 1.7f, 0f, NebGlyphShapes.Gem, 0.78f, 0.85f, 1.1f, 15f)
    3 -> CoverSpec(NebTone.Aqua, NebGlyphShapes.Sunny, 0.70f, 0.40f, 2.0f, 25f, NebGlyphShapes.Clover, 0.10f, 0.90f, 1.0f, 0f)
    4 -> CoverSpec(NebTone.Peri, NebGlyphShapes.Clover, 0.88f, 0.55f, 1.8f, 0f, NebGlyphShapes.Burst, 0.30f, 0.10f, 1.1f, 30f)
    5 -> CoverSpec(NebTone.Azure, NebGlyphShapes.Burst, 0.25f, 0.45f, 2.0f, 8f, NebGlyphShapes.Flower, 0.90f, 0.10f, 1.0f, 0f)
    6 -> CoverSpec(NebTone.Sky, NebGlyphShapes.Pentagon, 0.60f, 0.50f, 1.9f, -10f, NebGlyphShapes.Cookie, 0.05f, 0.15f, 1.1f, 20f)
    7 -> CoverSpec(NebTone.Aqua, NebGlyphShapes.Gem, 0.85f, 0.45f, 1.8f, 0f, NebGlyphShapes.Sunny, 0.22f, 0.80f, 1.2f, 0f)
    8 -> CoverSpec(NebTone.Peri, NebGlyphShapes.Cookie, 0.12f, 0.50f, 1.8f, 0f, NebGlyphShapes.Pill, 0.80f, 0.20f, 1.3f, 40f)
    else -> null
}

/** The banner itself. Shapes settle in with a spring when the cover appears or changes. */
@Composable
fun NoteCoverBanner(cover: Int, modifier: Modifier = Modifier, animate: Boolean = true) {
    val spec = remember(cover) { coverSpec(cover) } ?: return
    val dark = MaterialTheme.colorScheme.surface.luminance() < 0.5f
    val pa = rememberGlyphPath(spec.a)
    val pb = rememberGlyphPath(spec.b)
    val settle = remember(cover) { Animatable(if (animate) 0f else 1f) }
    LaunchedEffect(cover) {
        if (animate) settle.animateTo(1f, spring(dampingRatio = 0.62f, stiffness = Spring.StiffnessLow))
    }
    val bg = spec.tone.container(dark)
    val ink = spec.tone.deep(dark)
    val vivid = spec.tone.vivid
    Canvas(modifier.clipToBounds().background(bg)) {
        val t = settle.value
        val fade = t.coerceIn(0f, 1f)
        val h = size.height
        val w = size.width
        drawGlyph(
            pa, Offset(w * spec.ax, h * spec.ay), h * spec.asz * (0.55f + 0.45f * t), vivid,
            rotation = spec.ar - 40f * (1f - t), alpha = (if (dark) 0.5f else 0.85f) * fade,
        )
        drawGlyph(
            pb, Offset(w * spec.bx, h * spec.by), h * spec.bsz * (0.4f + 0.6f * t), ink,
            rotation = spec.br + 60f * (1f - t), alpha = 0.26f * fade,
        )
    }
}

@Composable
fun NoteIconSheet(current: String, onPick: (String) -> Unit, onDismiss: () -> Unit) {
    val c = MaterialTheme.colorScheme
    NebModalSheet(onDismiss = onDismiss, title = "Icon") {
        FlowRow(
            Modifier.fillMaxWidth().padding(vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(10.dp), verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Box(
                Modifier.size(54.dp).clip(RoundedCornerShape(18.dp)).background(c.surfaceContainerHigh)
                    .clickable { onPick("") },
                contentAlignment = Alignment.Center,
            ) { Icon(Icons.Outlined.Close, "No icon", tint = c.onSurfaceVariant, modifier = Modifier.size(22.dp)) }
            NoteIcons.all.forEach { (key, vector) ->
                val on = key == current
                Box(
                    Modifier.size(54.dp).clip(RoundedCornerShape(if (on) 27.dp else 18.dp))
                        .background(if (on) c.primary else c.surfaceContainerHigh)
                        .clickable { onPick(key) },
                    contentAlignment = Alignment.Center,
                ) { Icon(vector, key, tint = if (on) c.onPrimary else c.onSurface, modifier = Modifier.size(24.dp)) }
            }
        }
        Box(Modifier.height(16.dp))
    }
}

@Composable
fun NoteCoverSheet(current: Int, onPick: (Int) -> Unit, onDismiss: () -> Unit) {
    val c = MaterialTheme.colorScheme
    NebModalSheet(onDismiss = onDismiss, title = "Cover") {
        Column(Modifier.padding(vertical = 8.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Row(
                Modifier.fillMaxWidth().height(54.dp).clip(RoundedCornerShape(18.dp))
                    .background(if (current == 0) c.primaryContainer else c.surfaceContainerHigh)
                    .clickable { onPick(0) }.padding(horizontal = 16.dp),
                verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Icon(Icons.Outlined.Close, null, tint = if (current == 0) c.onPrimaryContainer else c.onSurfaceVariant, modifier = Modifier.size(20.dp))
                Text(
                    "No cover", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold,
                    color = if (current == 0) c.onPrimaryContainer else c.onSurface,
                )
            }
            for (row in 1..NoteCovers.count step 2) {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    for (i in row..minOf(row + 1, NoteCovers.count)) {
                        NoteCoverBanner(
                            i, animate = false,
                            modifier = Modifier.weight(1f).height(84.dp)
                                .clip(RoundedCornerShape(if (i == current) 32.dp else 20.dp))
                                .clickable { onPick(i) },
                        )
                    }
                }
            }
        }
        Box(Modifier.height(16.dp))
    }
}
