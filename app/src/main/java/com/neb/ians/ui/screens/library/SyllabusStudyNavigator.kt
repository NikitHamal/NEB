package com.neb.ians.ui.screens.library

import android.content.Context
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Checkbox
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiSyllabusChapter
import com.neb.ians.ui.components.WebPanelShape

@Composable
fun SyllabusStudyNavigator(
    chapters: List<ApiSyllabusChapter>,
    selectedChapterId: String,
    scope: String,
    onSelect: (String) -> Unit
) {
    val context = LocalContext.current
    val preferences = remember(context) { context.getSharedPreferences("syllabus_revision_v1", Context.MODE_PRIVATE) }
    var revised by remember(scope, chapters.map { it.id }) {
        mutableStateOf(chapters.filter { preferences.getBoolean("$scope/${it.id}", false) }.map { it.id }.toSet())
    }
    var query by rememberSaveable(scope) { mutableStateOf("") }
    val index = chapters.indexOfFirst { it.id == selectedChapterId }.coerceAtLeast(0)
    val current = chapters.getOrNull(index)
    val nepali = current?.studyMeta?.language == "ne"
    val filtered = chapters.filter {
        (it.name + " " + it.studyMeta.topics.joinToString(" ")).contains(query.trim(), ignoreCase = true)
    }
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Text(if (nepali) "पुनरावलोकन प्रगति" else "Revision progress", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
        LinearProgressIndicator(
            progress = { revised.size.toFloat() / chapters.size.coerceAtLeast(1) },
            modifier = Modifier.fillMaxWidth(),
            color = MaterialTheme.colorScheme.onSurface,
            trackColor = MaterialTheme.colorScheme.surfaceContainerHigh
        )
        Text(
            text = if (nepali) "${revised.size} / ${chapters.size} पाठ पूरा · यस उपकरणमा सुरक्षित" else "${revised.size} of ${chapters.size} chapters revised · saved on this device",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        OutlinedTextField(
            value = query,
            onValueChange = { query = it },
            modifier = Modifier.fillMaxWidth(),
            label = { Text(if (nepali) "पाठ वा विषय खोज्नुहोस्" else "Find a chapter or topic") },
            singleLine = true,
            shape = WebPanelShape
        )
        Column(Modifier.fillMaxWidth().heightIn(max = 220.dp).verticalScroll(rememberScrollState())) {
            filtered.forEach { chapter ->
                Row(
                    modifier = Modifier.fillMaxWidth().clickable(role = Role.Button) { onSelect(chapter.id) }.padding(vertical = 12.dp, horizontal = 4.dp),
                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        chapter.name,
                        modifier = Modifier.weight(1f),
                        style = MaterialTheme.typography.bodyMedium,
                        fontWeight = if (chapter.id == selectedChapterId) FontWeight.Bold else FontWeight.Normal
                    )
                    if (chapter.id in revised) Text("✓", color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
            }
            if (filtered.isEmpty()) Text(if (nepali) "मिल्ने पाठ भेटिएन।" else "No matching chapters.", modifier = Modifier.padding(12.dp))
        }
        Row(verticalAlignment = Alignment.CenterVertically) {
            Checkbox(
                checked = selectedChapterId in revised,
                onCheckedChange = { done ->
                    revised = if (done) revised + selectedChapterId else revised - selectedChapterId
                    preferences.edit().putBoolean("$scope/$selectedChapterId", done).apply()
                }
            )
            Text(if (nepali) "यस पाठको पुनरावलोकन पूरा" else "I have revised this chapter", style = MaterialTheme.typography.bodyMedium)
        }
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            TextButton(onClick = { chapters.getOrNull(index - 1)?.let { onSelect(it.id) } }, enabled = index > 0) {
                Text(if (nepali) "अघिल्लो पाठ" else "Previous")
            }
            TextButton(onClick = { chapters.getOrNull(index + 1)?.let { onSelect(it.id) } }, enabled = index < chapters.lastIndex) {
                Text(if (nepali) "अर्को पाठ" else "Next chapter")
            }
        }
    }
}
