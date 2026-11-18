package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.EditNote
import androidx.compose.material.icons.filled.LocalFireDepartment
import androidx.compose.material.icons.filled.ThumbUp
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
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
import com.neb.ians.data.api.ApiGlanceTile
import com.neb.ians.data.api.ApiStudying
import com.neb.ians.ui.components.M3xThumb

private fun glanceIcon(name: String): ImageVector = when (name) {
    "description" -> Icons.Filled.Description
    "thumb_up" -> Icons.Filled.ThumbUp
    "verified" -> Icons.Filled.Verified
    "check_circle" -> Icons.Filled.CheckCircle
    "local_fire_department" -> Icons.Filled.LocalFireDepartment
    else -> Icons.Filled.Visibility
}

/** Profile v3 glance row: three tonal tiles (primary, secondary, tertiary container). Flat, 24dp, no shadow. */
@Composable
fun ProfileGlance(tiles: List<ApiGlanceTile>, modifier: Modifier = Modifier) {
    if (tiles.isEmpty()) return
    val scheme = MaterialTheme.colorScheme
    Row(
        modifier = modifier.fillMaxWidth().padding(horizontal = 14.dp).height(IntrinsicSize.Min),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        tiles.take(3).forEachIndexed { i, t ->
            val (bg, fg) = when (t.tone) {
                2 -> scheme.secondaryContainer to scheme.onSecondaryContainer
                3 -> scheme.tertiaryContainer to scheme.onTertiaryContainer
                else -> scheme.primaryContainer to scheme.onPrimaryContainer
            }
            Column(
                modifier = Modifier.weight(if (i == 0) 1.25f else 1f).fillMaxHeight()
                    .clip(RoundedCornerShape(22.dp)).background(bg)
                    .padding(horizontal = 12.dp, vertical = 12.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Icon(glanceIcon(t.icon), contentDescription = null, tint = fg, modifier = Modifier.size(22.dp))
                Column {
                    Text(t.value, color = fg, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold, maxLines = 1)
                    Text(t.label, color = fg, style = MaterialTheme.typography.labelMedium, maxLines = 2, overflow = TextOverflow.Ellipsis)
                }
            }
        }
    }
}

/** "Studying now": subject art with the subject chip, latest post, today and streak, the week as bars. */
@Composable
fun ProfileStudyingNow(study: ApiStudying, onOpenPost: (String) -> Unit, modifier: Modifier = Modifier) {
    val scheme = MaterialTheme.colorScheme
    Column(modifier.fillMaxWidth().padding(horizontal = 14.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text("Studying now", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(start = 4.dp))
        Card(
            shape = RoundedCornerShape(24.dp),
            colors = CardDefaults.cardColors(containerColor = scheme.surfaceContainerLowest),
            border = BorderStroke(1.dp, scheme.outlineVariant),
            elevation = CardDefaults.cardElevation(0.dp),
            modifier = Modifier.fillMaxWidth().clickable { onOpenPost(study.postId) }
        ) {
            Row(Modifier.height(IntrinsicSize.Min)) {
                Box(Modifier.width(112.dp).fillMaxHeight()) {
                    M3xThumb(seed = "${study.postId}|study", subject = study.subject, modifier = Modifier.matchParentSize())
                    Text(
                        study.subject, maxLines = 1, overflow = TextOverflow.Ellipsis,
                        color = scheme.onPrimaryContainer, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.SemiBold,
                        modifier = Modifier.align(Alignment.BottomStart).padding(8.dp).clip(RoundedCornerShape(14.dp))
                            .background(scheme.primaryContainer).padding(horizontal = 10.dp, vertical = 5.dp)
                    )
                }
                Column(Modifier.weight(1f).padding(14.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text(study.title, maxLines = 2, overflow = TextOverflow.Ellipsis, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                    Row(horizontalArrangement = Arrangement.spacedBy(14.dp), verticalAlignment = Alignment.CenterVertically) {
                        Fact(Icons.Filled.EditNote, "${study.today} today")
                        Fact(Icons.Filled.LocalFireDepartment, "${study.streak} day streak")
                    }
                    WeekBars(study.week, study.todayIndex)
                }
            }
        }
    }
}

@Composable
private fun Fact(icon: ImageVector, text: String) {
    val c = MaterialTheme.colorScheme.onSurfaceVariant
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
        Icon(icon, null, tint = c, modifier = Modifier.size(16.dp))
        Text(text, color = c, style = MaterialTheme.typography.labelMedium, maxLines = 1)
    }
}

@Composable
private fun WeekBars(week: List<Int>, todayIndex: Int) {
    val scheme = MaterialTheme.colorScheme
    val letters = "MTWTFSS"
    Row(Modifier.fillMaxWidth().height(48.dp), horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.Bottom) {
        for (i in 0 until 7) {
            val n = week.getOrElse(i) { 0 }
            val h = if (n <= 0) 4.dp else (8 + minOf(n, 6) * 4).dp
            val tone: Color = if (i == todayIndex) scheme.primary else scheme.surfaceContainerHighest
            Column(Modifier.weight(1f), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(3.dp)) {
                Box(Modifier.width(18.dp).height(h).clip(RoundedCornerShape(6.dp)).background(tone))
                Text(letters[i].toString(), color = scheme.onSurfaceVariant, style = MaterialTheme.typography.labelSmall)
            }
        }
    }
}
