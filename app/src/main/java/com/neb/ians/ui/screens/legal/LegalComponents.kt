package com.neb.ians.ui.screens.legal

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Immutable
data class LegalTextColors(
    val heading: Color,
    val body: Color,
    val marker: Color,
    val markerBackground: Color
)

@Composable
fun legalTextColors(): LegalTextColors = LegalTextColors(
    heading = MaterialTheme.colorScheme.onSurface,
    body = MaterialTheme.colorScheme.onSurfaceVariant,
    marker = MaterialTheme.colorScheme.onSurface,
    markerBackground = MaterialTheme.colorScheme.surfaceContainerHigh
)

fun legalAnnotated(raw: String): AnnotatedString = buildAnnotatedString {
    var cursor = 0
    while (true) {
        val open = raw.indexOf("**", cursor)
        if (open < 0) break
        val close = raw.indexOf("**", open + 2)
        if (close < 0) break
        append(raw.substring(cursor, open))
        withStyle(SpanStyle(fontWeight = FontWeight.SemiBold)) {
            append(raw.substring(open + 2, close))
        }
        cursor = close + 2
    }
    append(raw.substring(cursor))
}

@Composable
fun LegalSectionBlock(
    section: LegalSection,
    colors: LegalTextColors,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxWidth()) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Box(
                modifier = Modifier
                    .size(26.dp)
                    .background(colors.markerBackground, RoundedCornerShape(9.dp)),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = section.number,
                    style = MaterialTheme.typography.labelMedium.copy(
                        fontWeight = FontWeight.SemiBold,
                        fontSize = 12.sp
                    ),
                    color = colors.marker
                )
            }
            Spacer(modifier = Modifier.size(10.dp))
            Text(
                text = section.title,
                style = MaterialTheme.typography.titleSmall.copy(
                    fontWeight = FontWeight.Bold,
                    fontSize = 15.sp
                ),
                color = colors.heading
            )
        }
        Spacer(modifier = Modifier.height(8.dp))
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            section.paragraphs.forEach { paragraph ->
                val text = remember(paragraph) { legalAnnotated(paragraph) }
                Text(
                    text = text,
                    style = MaterialTheme.typography.bodyMedium.copy(
                        fontSize = 14.sp,
                        lineHeight = 21.sp
                    ),
                    color = colors.body,
                    modifier = Modifier.padding(start = 36.dp)
                )
            }
        }
    }
}
