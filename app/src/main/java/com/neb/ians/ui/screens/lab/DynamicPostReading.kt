package com.neb.ians.ui.screens.lab

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
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
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.FormatQuote
import androidx.compose.material.icons.outlined.Lightbulb
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
internal fun ReadingView(look: Look, s: Sample) {
    Surface(
        Modifier.fillMaxWidth(), shape = RoundedCornerShape(look.corner.dp), color = look.bg, contentColor = look.ink,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
    ) {
        Column {
            if (look.pattern != Pattern.None) LookCover(look, if (look.tall) 200 else 140) { LookChip(s.tag, look.copy(soft = look.bg)) }
            Column(Modifier.padding(24.dp), verticalArrangement = Arrangement.spacedBy(18.dp)) {
                if (look.pattern == Pattern.None) LookChip(s.tag, look)
                Text(
                    s.title, Modifier.fillMaxWidth(), fontFamily = look.font, fontSize = 30.sp, lineHeight = 37.sp,
                    fontWeight = FontWeight.Bold, textAlign = if (look.center) TextAlign.Center else TextAlign.Start,
                )
                LookByline(look, s, "${s.minutes} min read")
                Text(leadText(look, s), Modifier.fillMaxWidth(), fontFamily = look.font, fontSize = 17.sp, lineHeight = 28.sp)
                Callout(look, s.callout)
                PullQuote(look, s.quote)
                if (s.kind == ListKind.Steps) Steps(look, s.items) else Checks(look, s)
                Box(Modifier.fillMaxWidth().height(22.dp).drawBehind { drawDivider(look) })
                Text(s.outro, Modifier.fillMaxWidth(), fontFamily = look.font, fontSize = 16.sp, lineHeight = 26.sp, color = look.ink.copy(alpha = 0.85f))
                LookFooter(look, s)
            }
        }
    }
}

private fun leadText(look: Look, s: Sample) = buildAnnotatedString {
    append(s.lead)
    if (look.dropCap) addStyle(SpanStyle(fontSize = 44.sp, color = look.accent, fontWeight = FontWeight.Bold), 0, 1)
    if (look.mark) {
        val i = s.lead.indexOf(s.mark)
        if (i >= 0) addStyle(SpanStyle(background = look.accent.copy(alpha = 0.22f), fontWeight = FontWeight.SemiBold), i, i + s.mark.length)
    }
}

@Composable
private fun Callout(look: Look, text: String) {
    Row(
        Modifier.fillMaxWidth().clip(RoundedCornerShape(18.dp)).background(look.soft).padding(14.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.CenterVertically,
    ) {
        Icon(Icons.Outlined.Lightbulb, null, Modifier.size(22.dp), tint = look.accent)
        Text(text, fontFamily = look.font, fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight.Medium)
    }
}

@Composable
private fun PullQuote(look: Look, text: String) {
    if (look.quoteBar) {
        Box(Modifier.fillMaxWidth().padding(start = 16.dp).drawBehind {
            drawRoundRect(look.accent, Offset(-16.dp.toPx(), 0f), Size(4.dp.toPx(), size.height), CornerRadius(2.dp.toPx()))
        }) {
            Text(text, fontFamily = look.font, fontStyle = FontStyle.Italic, fontSize = 20.sp, lineHeight = 28.sp, fontWeight = FontWeight.Medium)
        }
    } else {
        Column(Modifier.fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Icon(Icons.Outlined.FormatQuote, null, Modifier.size(34.dp), tint = look.accent)
            Text(text, fontFamily = look.font, fontStyle = FontStyle.Italic, fontSize = 20.sp, lineHeight = 28.sp, textAlign = TextAlign.Center)
        }
    }
}

@Composable
private fun Steps(look: Look, items: List<String>) {
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        items.forEachIndexed { i, t ->
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.CenterVertically) {
                Box(Modifier.size(30.dp).clip(RoundedCornerShape(11.dp)).background(look.accent), contentAlignment = Alignment.Center) {
                    Text("${i + 1}", color = look.bg, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                }
                Text(t, fontFamily = look.font, fontSize = 16.sp, lineHeight = 22.sp)
            }
        }
    }
}

@Composable
private fun Checks(look: Look, s: Sample) {
    var done by remember(s.key) { mutableStateOf(setOf<Int>()) }
    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        s.items.forEachIndexed { i, t ->
            val on = i in done
            val fill by animateColorAsState(if (on) look.accent else Color.Transparent, label = "check")
            val shape = RoundedCornerShape(14.dp)
            Row(
                Modifier.fillMaxWidth().clip(shape).clickable { done = if (on) done - i else done + i }.padding(vertical = 8.dp, horizontal = 4.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.CenterVertically,
            ) {
                Box(Modifier.size(26.dp).clip(RoundedCornerShape(9.dp)).background(fill).border(2.dp, look.accent, RoundedCornerShape(9.dp)), contentAlignment = Alignment.Center) {
                    if (on) Icon(Icons.Outlined.Check, null, Modifier.size(16.dp), tint = look.bg)
                }
                Text(
                    t, fontFamily = look.font, fontSize = 16.sp, lineHeight = 22.sp, color = look.ink.copy(alpha = if (on) 0.5f else 1f),
                    textDecoration = if (on) TextDecoration.LineThrough else TextDecoration.None,
                )
            }
        }
    }
}
