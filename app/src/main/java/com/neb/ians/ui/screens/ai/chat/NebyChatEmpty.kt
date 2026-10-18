package com.neb.ians.ui.screens.ai.chat

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Calculate
import androidx.compose.material.icons.outlined.EventNote
import androidx.compose.material.icons.outlined.Lightbulb
import androidx.compose.material.icons.outlined.Science
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.pixel.NebyPixel
import com.neb.ians.ui.pixel.NebyState
import java.util.Calendar

private data class Starter(val icon: ImageVector, val title: String, val prompt: String)

private val STARTERS = listOf(
    Starter(Icons.Outlined.Lightbulb, "Explain simply", "Explain Newton's three laws of motion simply, with an everyday example for each."),
    Starter(Icons.Outlined.Calculate, "Solve step by step", "Solve x² − 5x + 6 = 0 step by step and check the answer."),
    Starter(Icons.Outlined.Science, "Quiz me", "Give me 5 quick questions on photosynthesis, then check my answers one by one."),
    Starter(Icons.Outlined.EventNote, "Plan my revision", "Make me a 7-day revision plan for my board exams, two hours a day.")
)

/**
 * A fresh chat: pixel Neby waving hello (tap for more), a greeting for the time of day, and
 * four starters that fill the question in one tap.
 */
@Composable
fun NebyChatWelcome(name: String?, onStarter: (String) -> Unit, modifier: Modifier = Modifier) {
    val hour = remember { Calendar.getInstance().get(Calendar.HOUR_OF_DAY) }
    val greeting = when (hour) { in 4..11 -> "Good morning"; in 12..16 -> "Good afternoon"; in 17..21 -> "Good evening"; else -> "Up late" }
    var line by remember { mutableStateOf("What are we studying today?") }
    Column(modifier.fillMaxWidth().padding(horizontal = 20.dp, vertical = 12.dp), horizontalAlignment = Alignment.CenterHorizontally) {
        NebyPixel(
            size = 132.dp,
            interactive = true,
            intro = NebyState.Wave,
            onReaction = { r ->
                line = when (r) {
                    NebyState.Laugh -> "Okay okay, that tickles."
                    NebyState.Love -> "Studying together is more fun."
                    NebyState.Cool -> "Exam? We've got this."
                    NebyState.Surprised -> "Whoa! Ask me something hard."
                    else -> "Tap me all you like, then ask away."
                }
            }
        )
        Spacer(Modifier.height(10.dp))
        Text(
            if (name.isNullOrBlank()) "$greeting!" else "$greeting, ${name.substringBefore(' ')}!",
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.SemiBold,
            textAlign = TextAlign.Center
        )
        Text(line, style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant, textAlign = TextAlign.Center, modifier = Modifier.padding(top = 4.dp))
        Spacer(Modifier.height(22.dp))
        Column(Modifier.widthIn(max = 520.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            STARTERS.chunked(2).forEach { row ->
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    row.forEach { s -> StarterCard(s, Modifier.weight(1f)) { onStarter(s.prompt) } }
                }
            }
        }
    }
}

@Composable
private fun StarterCard(s: Starter, modifier: Modifier, onClick: () -> Unit) {
    val shape = RoundedCornerShape(18.dp)
    Column(
        modifier
            .clip(shape)
            .background(MaterialTheme.colorScheme.surfaceContainerLow)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.6f), shape)
            .nebPressable(onClick = onClick)
            .padding(14.dp),
        verticalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        Icon(s.icon, contentDescription = null, modifier = Modifier.size(20.dp), tint = MaterialTheme.colorScheme.onSurface)
        Text(s.title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
        Text(s.prompt, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 2)
    }
}
