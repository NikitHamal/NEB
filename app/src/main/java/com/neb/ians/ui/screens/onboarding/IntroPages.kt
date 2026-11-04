@file:OptIn(ExperimentalLayoutApi::class)

package com.neb.ians.ui.screens.onboarding

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.AutoAwesome
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.Quiz
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.TaskAlt
import androidx.compose.material.icons.outlined.ThumbUpOffAlt
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.graphics.shapes.RoundedPolygon
import com.neb.ians.ui.components.NebGlyphShapes
import com.neb.ians.ui.components.NebTone
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebFastSpatialSpec
import com.neb.ians.ui.theme.nebSlowSpatialSpec
import kotlinx.coroutines.delay

private val PillShape = RoundedCornerShape(28.dp)

/** The hero: a search box that types, and the three things it finds. */
@Composable
internal fun FinderIllustration(active: Boolean) {
    val cs = MaterialTheme.colorScheme
    var caret by remember { mutableStateOf(true) }
    LaunchedEffect(active) {
        while (active) {
            delay(520)
            caret = !caret
        }
    }
    Reveal(active, 0, Modifier.fillMaxWidth().padding(horizontal = 28.dp)) {
        IntroPanel(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Row(
                    Modifier
                        .fillMaxWidth()
                        .height(52.dp)
                        .clip(PillShape)
                        .background(cs.surfaceContainer)
                        .padding(horizontal = 16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Outlined.Search, null, tint = cs.onSurfaceVariant, modifier = Modifier.size(22.dp))
                    Spacer(Modifier.width(10.dp))
                    TypedText("Physics Class 12", active, MaterialTheme.typography.bodyLarge, cs.onSurface)
                    Box(
                        Modifier
                            .padding(start = 2.dp)
                            .width(2.dp)
                            .height(20.dp)
                            .graphicsLayer { alpha = if (caret) 1f else 0f }
                            .background(cs.primary)
                    )
                }
                FINDER_ROWS.forEachIndexed { i, row ->
                    Reveal(active, i + 3, rise = 18.dp) {
                        Row(
                            Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp, horizontal = 4.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            val dark = isDarkSurface()
                            GlyphTile(row.shape, row.tone, 48.dp) {
                                Icon(row.icon, null, tint = row.tone.deep(dark), modifier = Modifier.size(24.dp))
                            }
                            Spacer(Modifier.width(14.dp))
                            Text(
                                row.label,
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.SemiBold,
                                color = cs.onSurface
                            )
                        }
                    }
                }
            }
        }
    }
}

private data class FinderRow(val label: String, val icon: ImageVector, val shape: RoundedPolygon, val tone: NebTone)

private val FINDER_ROWS = listOf(
    FinderRow("Chapter notes", Icons.Outlined.Description, NebGlyphShapes.Cookie, NebTone.Azure),
    FinderRow("Past papers", Icons.Outlined.Quiz, NebGlyphShapes.Sunny, NebTone.Sky),
    FinderRow("Solved exercises", Icons.Outlined.TaskAlt, NebGlyphShapes.Flower, NebTone.Aqua)
)

private val LEVELS = listOf(
    "Class 8", "Class 9", "Class 10", "Class 11", "Class 12", "+2 Passout", "Bachelors", "Masters"
)

/** The level picker: chips pop in, then a selection walks across them. */
@Composable
internal fun LevelIllustration(active: Boolean) {
    var picked by remember { mutableIntStateOf(4) }
    LaunchedEffect(active) {
        if (active) {
            val walk = listOf(4, 1, 3, 6, 2, 5)
            var i = 0
            delay(1500)
            while (true) {
                picked = walk[i % walk.size]
                i++
                delay(1300)
            }
        }
    }
    FlowRow(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 28.dp),
        horizontalArrangement = Arrangement.spacedBy(10.dp, Alignment.CenterHorizontally),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        LEVELS.forEachIndexed { i, level ->
            Reveal(active, i, rise = 22.dp) { LevelChip(level, selected = picked == i) }
        }
    }
}

@Composable
private fun LevelChip(label: String, selected: Boolean) {
    val cs = MaterialTheme.colorScheme
    val bg by animateColorAsState(if (selected) cs.primary else cs.surfaceContainerLowest, nebEffectsSpec())
    val fg by animateColorAsState(if (selected) cs.onPrimary else cs.onSurface, nebEffectsSpec())
    val line by animateColorAsState(if (selected) cs.primary else cs.outlineVariant, nebEffectsSpec())
    val scale by animateFloatAsState(if (selected) 1.08f else 1f, nebFastSpatialSpec())
    Box(
        Modifier
            .graphicsLayer { scaleX = scale; scaleY = scale }
            .height(48.dp)
            .clip(PillShape)
            .background(bg)
            .border(1.5.dp, line, PillShape)
            .padding(horizontal = 20.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(label, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, color = fg)
    }
}

/** Two forum threads sliding in from opposite sides. */
@Composable
internal fun ForumIllustration(active: Boolean) {
    Column(
        Modifier.fillMaxWidth().padding(horizontal = 28.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Reveal(active, 0, fromX = (-48).dp) {
            ThreadCard("Asha", "A", "Chemistry", "Why is the second ionisation energy always higher?", "24", "6", "310", NebTone.Azure, solved = true)
        }
        Reveal(active, 2, Modifier.padding(start = 24.dp), fromX = 48.dp) {
            ThreadCard("Ravi", "R", "Physics", "How do I read a velocity-time graph?", "11", "3", "128", NebTone.Sky, solved = false)
        }
    }
}

@Composable
private fun ThreadCard(
    name: String,
    initial: String,
    tag: String,
    title: String,
    likes: String,
    replies: String,
    views: String,
    tone: NebTone,
    solved: Boolean
) {
    val cs = MaterialTheme.colorScheme
    val dark = isDarkSurface()
    IntroPanel(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                GlyphTile(NebGlyphShapes.Cookie, tone, 44.dp) {
                    Text(initial, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = tone.deep(dark))
                }
                Spacer(Modifier.width(12.dp))
                Column(Modifier.weight(1f)) {
                    Text(name, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, color = cs.onSurface)
                    Text("today", style = MaterialTheme.typography.labelMedium, color = cs.onSurfaceVariant)
                }
                Text(
                    tag,
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.SemiBold,
                    color = cs.onSecondaryContainer,
                    modifier = Modifier
                        .clip(PillShape)
                        .background(cs.secondaryContainer)
                        .padding(horizontal = 12.dp, vertical = 6.dp)
                )
            }
            Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold, color = cs.onSurface)
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                Stat(Icons.Outlined.ThumbUpOffAlt, likes)
                Stat(Icons.Outlined.ChatBubbleOutline, replies)
                Stat(Icons.Outlined.Visibility, views)
                if (solved) {
                    Spacer(Modifier.weight(1f))
                    Row(
                        Modifier
                            .clip(PillShape)
                            .background(NebTone.Aqua.container(dark))
                            .padding(horizontal = 10.dp, vertical = 5.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(Icons.Outlined.TaskAlt, null, tint = NebTone.Aqua.deep(dark), modifier = Modifier.size(16.dp))
                        Spacer(Modifier.width(6.dp))
                        Text("Solved", style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.SemiBold, color = NebTone.Aqua.deep(dark))
                    }
                }
            }
        }
    }
}

@Composable
private fun Stat(icon: ImageVector, value: String) {
    val color = MaterialTheme.colorScheme.onSurfaceVariant
    Row(verticalAlignment = Alignment.CenterVertically) {
        Icon(icon, null, tint = color, modifier = Modifier.size(18.dp))
        Spacer(Modifier.width(5.dp))
        Text(value, style = MaterialTheme.typography.labelMedium, color = color)
    }
}

/** The reader, the Ask Neby button, and the answer sheet that rises over the page. */
@Composable
internal fun NebyIllustration(active: Boolean) {
    val cs = MaterialTheme.colorScheme
    val progress by animateFloatAsState(if (active) 0.31f else 0f, nebSlowSpatialSpec())
    Reveal(active, 0, Modifier.fillMaxWidth().padding(horizontal = 28.dp)) {
        IntroPanel(Modifier.fillMaxWidth().height(330.dp)) {
            Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    Text("Physics 12", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.Bold, color = cs.onSurface, modifier = Modifier.weight(1f))
                    Text("84 / 275", style = MaterialTheme.typography.labelMedium, color = cs.onSurfaceVariant)
                }
                Box(Modifier.fillMaxWidth().height(6.dp).clip(PillShape).background(cs.surfaceContainerHigh)) {
                    Box(Modifier.fillMaxWidth(progress).fillMaxHeight().clip(PillShape).background(cs.primary))
                }
                Text("5.2 Refraction", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = cs.onSurface)
                SkeletonLine(0.96f, false)
                SkeletonLine(0.82f, true)
                SkeletonLine(0.9f, false)
                SkeletonLine(0.55f, false)
            }
            Reveal(active, 4, Modifier.align(Alignment.BottomEnd).padding(18.dp)) {
                Row(
                    Modifier
                        .clip(PillShape)
                        .background(cs.primary)
                        .padding(horizontal = 16.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Outlined.AutoAwesome, null, tint = cs.onPrimary, modifier = Modifier.size(20.dp))
                    Spacer(Modifier.width(8.dp))
                    Text("Ask Neby", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, color = cs.onPrimary)
                }
            }
            Reveal(active, 7, Modifier.align(Alignment.BottomCenter).padding(10.dp), rise = 90.dp) {
                Column(
                    Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(22.dp))
                        .background(cs.primaryContainer)
                        .padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text(
                        "Why does a pencil look bent in water?",
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.SemiBold,
                        color = cs.onPrimaryContainer
                    )
                    AnswerBar(0.95f)
                    AnswerBar(0.8f)
                    AnswerBar(0.5f)
                }
            }
        }
    }
}

@Composable
private fun SkeletonLine(fraction: Float, highlight: Boolean) {
    val cs = MaterialTheme.colorScheme
    Box(
        Modifier
            .fillMaxWidth(fraction)
            .height(10.dp)
            .clip(PillShape)
            .background(if (highlight) cs.primaryContainer else cs.surfaceContainerHigh)
    )
}

@Composable
private fun AnswerBar(fraction: Float) {
    Box(
        Modifier
            .fillMaxWidth(fraction)
            .height(8.dp)
            .clip(PillShape)
            .background(MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.22f))
    )
}
