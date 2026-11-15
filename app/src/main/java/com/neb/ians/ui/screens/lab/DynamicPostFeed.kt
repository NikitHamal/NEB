package com.neb.ians.ui.screens.lab

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/** Tag, label or category chip on a post: tonal fill in the look's soft colour. */
@Composable
internal fun LookChip(text: String, look: Look, modifier: Modifier = Modifier) {
    Surface(modifier, shape = RoundedCornerShape(12.dp), color = look.soft, contentColor = look.ink) {
        Text(text, Modifier.padding(horizontal = 10.dp, vertical = 4.dp), fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
    }
}

/** Frameless squircle avatar, never a ring. */
@Composable
internal fun LookAvatar(name: String, look: Look) {
    Box(
        Modifier.size(30.dp).drawBehind { drawRoundRect(look.soft, cornerRadius = androidx.compose.ui.geometry.CornerRadius(10.dp.toPx())) },
        contentAlignment = Alignment.Center,
    ) { Text(name.take(1), color = look.accent, fontSize = 13.sp, fontWeight = FontWeight.Bold) }
}

@Composable
internal fun LookByline(look: Look, s: Sample, time: String) {
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        LookAvatar(s.author, look)
        Text(s.author, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
        Text(time, fontSize = 12.sp, color = look.ink.copy(alpha = 0.55f))
    }
}

@Composable
internal fun LookCover(look: Look, height: Int, content: @Composable () -> Unit = {}) {
    Box(Modifier.fillMaxWidth().height(height.dp).drawBehind { drawRect(look.soft); drawPattern(look) }) {
        Box(Modifier.align(Alignment.BottomStart).padding(14.dp)) { content() }
    }
}

@Composable
internal fun LookFooter(look: Look, s: Sample) {
    val dim = look.ink.copy(alpha = 0.7f)
    Row(verticalAlignment = Alignment.CenterVertically) {
        Icon(Icons.Outlined.FavoriteBorder, null, Modifier.size(18.dp), tint = dim)
        Text("128", Modifier.padding(start = 5.dp), fontSize = 12.sp, color = dim)
        Spacer(Modifier.width(16.dp))
        Icon(Icons.Outlined.ChatBubbleOutline, null, Modifier.size(18.dp), tint = dim)
        Text("24", Modifier.padding(start = 5.dp), fontSize = 12.sp, color = dim)
        Spacer(Modifier.weight(1f))
        Text("${s.minutes} min read", fontSize = 12.sp, color = look.ink.copy(alpha = 0.55f))
        Spacer(Modifier.width(12.dp))
        Icon(Icons.Outlined.BookmarkBorder, null, Modifier.size(18.dp), tint = dim)
    }
}

@Composable
internal fun FeedCard(look: Look, s: Sample, modifier: Modifier = Modifier) {
    Surface(
        modifier.fillMaxWidth(), shape = RoundedCornerShape(look.corner.dp), color = look.bg, contentColor = look.ink,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
    ) {
        Column {
            val cover = look.pattern != Pattern.None
            if (cover) LookCover(look, if (look.tall) 124 else 80) { LookChip(s.tag, look.copy(soft = look.bg)) }
            Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                if (!cover) LookChip(s.tag, look)
                LookByline(look, s, "2h")
                Text(
                    s.title, Modifier.fillMaxWidth(), fontFamily = look.font, fontSize = 21.sp, lineHeight = 27.sp,
                    fontWeight = FontWeight.SemiBold, textAlign = if (look.center) TextAlign.Center else TextAlign.Start,
                    maxLines = 3, overflow = TextOverflow.Ellipsis,
                )
                Text(
                    s.lead, Modifier.fillMaxWidth(), fontFamily = look.font, fontSize = 14.sp, lineHeight = 21.sp, maxLines = 3,
                    overflow = TextOverflow.Ellipsis, color = look.ink.copy(alpha = 0.8f),
                    textAlign = if (look.center) TextAlign.Center else TextAlign.Start,
                )
                LookFooter(look, s)
            }
        }
    }
}
