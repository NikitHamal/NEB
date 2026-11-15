package com.neb.ians.ui.screens.pathways

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.ui.components.nebHorizontalScroll

private enum class Pattern { None, Dots, Lines, Grid, Waves, Rings }

/** One look: paper, ink, accent, type, a cover pattern and a few decorations. Flat colour only. */
private class Look(
    val name: String, val bg: Color, val ink: Color, val accent: Color, val soft: Color,
    val font: FontFamily, val pattern: Pattern, val dropCap: Boolean, val quoteBar: Boolean, val corner: Int,
)

private val LOOKS = listOf(
    Look("Paper", Color(0xFFFBF8F1), Color(0xFF2B2620), Color(0xFFB4532A), Color(0xFFEFE7D6), FontFamily.Serif, Pattern.Lines, true, true, 28),
    Look("Ink", Color(0xFF15171A), Color(0xFFEDEBE6), Color(0xFFE9B949), Color(0xFF24272C), FontFamily.Serif, Pattern.Rings, true, true, 28),
    Look("Garden", Color(0xFFEAF3E4), Color(0xFF1F3322), Color(0xFF2F7D46), Color(0xFFD3E6C9), FontFamily.SansSerif, Pattern.Waves, false, true, 32),
    Look("Sunrise", Color(0xFFFFF0E0), Color(0xFF3A2414), Color(0xFFE2622B), Color(0xFFFFDDBA), FontFamily.SansSerif, Pattern.Dots, false, false, 36),
    Look("Blueprint", Color(0xFFE6EEF7), Color(0xFF14283D), Color(0xFF1E5F9E), Color(0xFFCADBEC), FontFamily.Monospace, Pattern.Grid, false, true, 16),
    Look("Rose", Color(0xFFFBEAEC), Color(0xFF3A1D22), Color(0xFFC03A52), Color(0xFFF5CFD5), FontFamily.Serif, Pattern.Dots, true, false, 32),
)

private const val TITLE = "How I stopped dreading Maths in Class 10"
private const val BODY = "Last year I could not finish a paper in time. Then I changed three small things, and the marks followed. Here is the plan I wish someone had handed me."
private const val QUOTE = "Do one chapter badly before you do one chapter perfectly."
private val STEPS = listOf("Solve the last five years of papers", "Keep a mistakes notebook", "Teach one friend each Sunday")

@Composable
fun DynamicPostsLabScreen(onNavigateBack: () -> Unit) {
    var index by rememberSaveable { mutableIntStateOf(0) }
    var reading by rememberSaveable { mutableStateOf(false) }
    var fallback by rememberSaveable { mutableStateOf(false) }
    val c = MaterialTheme.colorScheme
    val look = if (fallback) Look("Default", c.surfaceContainerLowest, c.onSurface, c.primary, c.secondaryContainer, FontFamily.Default, Pattern.None, false, true, 24) else LOOKS[index]
    Scaffold(
        topBar = { WebTopBar(title = "Dynamic posts", showBack = true, onBackClick = onNavigateBack) },
        containerColor = c.surface,
    ) { inner ->
        Column(Modifier.fillMaxSize().padding(inner).verticalScroll(rememberScrollState()).padding(16.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            Row(Modifier.fillMaxWidth().nebHorizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                LOOKS.forEachIndexed { i, l -> Pill(l.name, !fallback && index == i, dot = l.accent) { index = i; fallback = false } }
                Pill("Default", fallback) { fallback = true }
            }
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Pill("Feed card", !reading) { reading = false }
                Pill("Reading", reading) { reading = true }
            }
            if (reading) ReadingView(look) else FeedCard(look)
            Text("Pick a look to preview how a post would feel in the feed and when it is opened.", style = MaterialTheme.typography.bodySmall, color = c.onSurfaceVariant)
        }
    }
}

@Composable
private fun Pill(label: String, on: Boolean, dot: Color? = null, onClick: () -> Unit) {
    val c = MaterialTheme.colorScheme
    Surface(
        onClick = onClick, shape = RoundedCornerShape(18.dp),
        color = if (on) c.secondaryContainer else Color.Transparent,
        contentColor = if (on) c.onSecondaryContainer else c.onSurfaceVariant,
        border = if (on) null else BorderStroke(1.dp, c.outlineVariant),
    ) {
        Row(Modifier.padding(horizontal = 14.dp, vertical = 9.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            if (dot != null) Box(Modifier.width(10.dp).height(10.dp).clip(RoundedCornerShape(5.dp)).drawBehind { drawRect(dot) })
            Text(label, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.SemiBold)
        }
    }
}

private fun DrawScope.art(look: Look) {
    val col = look.accent.copy(alpha = 0.22f)
    val w = size.width; val h = size.height
    when (look.pattern) {
        Pattern.None -> {}
        Pattern.Dots -> { var y = 14f; while (y < h) { var x = 14f; while (x < w) { drawCircle(col, 3.2f, Offset(x, y)); x += 26f }; y += 26f } }
        Pattern.Lines -> { var y = 12f; while (y < h) { drawLine(col, Offset(0f, y), Offset(w, y), 2f); y += 16f } }
        Pattern.Grid -> {
            var x = 0f; while (x < w) { drawLine(col, Offset(x, 0f), Offset(x, h), 1.5f); x += 28f }
            var y = 0f; while (y < h) { drawLine(col, Offset(0f, y), Offset(w, y), 1.5f); y += 28f }
        }
        Pattern.Waves -> {
            var row = 0
            while (row * 24f < h + 24f) {
                val p = Path(); p.moveTo(0f, row * 24f)
                var x = 0f; while (x < w) { p.relativeQuadraticTo(15f, -12f, 30f, 0f); p.relativeQuadraticTo(15f, 12f, 30f, 0f); x += 60f }
                drawPath(p, col, style = Stroke(2.5f)); row++
            }
        }
        Pattern.Rings -> { for (i in 1..6) drawCircle(col, i * 26f, Offset(w * 0.86f, h * 0.2f), style = Stroke(2.5f)) }
    }
}

@Composable
private fun FeedCard(look: Look) {
    val shape = RoundedCornerShape(look.corner.dp)
    Surface(Modifier.fillMaxWidth(), shape = shape, color = look.bg, contentColor = look.ink, border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)) {
        Column {
            if (look.pattern != Pattern.None) Box(Modifier.fillMaxWidth().height(96.dp).drawBehind { drawRect(look.soft); art(look) })
            Column(Modifier.padding(20.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text(TITLE, fontFamily = look.font, fontSize = 22.sp, lineHeight = 28.sp, fontWeight = FontWeight.SemiBold)
                Text(BODY, fontFamily = look.font, fontSize = 14.sp, lineHeight = 21.sp, maxLines = 3, color = look.ink.copy(alpha = 0.8f))
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                    Chip("Study tips", look); Chip("Class 10", look)
                    Text("3 min read", fontSize = 12.sp, color = look.ink.copy(alpha = 0.6f), modifier = Modifier.padding(start = 4.dp))
                }
            }
        }
    }
}

@Composable
private fun Chip(text: String, look: Look) {
    Surface(shape = RoundedCornerShape(12.dp), color = look.soft, contentColor = look.ink) {
        Text(text, Modifier.padding(horizontal = 10.dp, vertical = 4.dp), fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
    }
}

@Composable
private fun ReadingView(look: Look) {
    val shape = RoundedCornerShape(look.corner.dp)
    Surface(Modifier.fillMaxWidth(), shape = shape, color = look.bg, contentColor = look.ink, border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)) {
        Column {
            if (look.pattern != Pattern.None) Box(Modifier.fillMaxWidth().height(150.dp).drawBehind { drawRect(look.soft); art(look) })
            Column(Modifier.padding(24.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
                Chip("Study tips", look)
                Text(TITLE, fontFamily = look.font, fontSize = 30.sp, lineHeight = 36.sp, fontWeight = FontWeight.Bold)
                val text = if (look.dropCap) buildAnnotatedString {
                    withStyle(SpanStyle(fontSize = 46.sp, color = look.accent, fontWeight = FontWeight.Bold)) { append(BODY.first()) }
                    append(BODY.drop(1))
                } else buildAnnotatedString { append(BODY) }
                Text(text, fontFamily = look.font, fontSize = 17.sp, lineHeight = 27.sp)
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                    if (look.quoteBar) Box(Modifier.width(4.dp).height(56.dp).clip(RoundedCornerShape(2.dp)).drawBehind { drawRect(look.accent) })
                    Text(QUOTE, fontFamily = look.font, fontSize = 19.sp, lineHeight = 27.sp, fontStyle = FontStyle.Italic, color = if (look.quoteBar) look.ink else look.accent)
                }
                STEPS.forEachIndexed { i, s ->
                    Row(horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.CenterVertically) {
                        Surface(shape = RoundedCornerShape(14.dp), color = look.accent, contentColor = look.bg) {
                            Text("${i + 1}", Modifier.padding(horizontal = 10.dp, vertical = 3.dp), fontSize = 13.sp, fontWeight = FontWeight.Bold)
                        }
                        Text(s, fontFamily = look.font, fontSize = 16.sp)
                    }
                }
            }
        }
    }
}
