package com.neb.ians.ui.screens.library

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Article
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.Folder
import androidx.compose.material.icons.outlined.MenuBook
import androidx.compose.material.icons.outlined.Quiz
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiSyllabusChapter
import com.neb.ians.ui.components.WebResourceCard

@Composable
fun ChapterFiles(chapter: ApiSyllabusChapter, onResourceClick: (String) -> Unit) {
    val groups = listOf(
        ResourceGroup("Notes & Summaries", Icons.Outlined.Description, chapter.notes),
        ResourceGroup("Solved Exercises", Icons.Outlined.Quiz, chapter.solutions),
        ResourceGroup("Past & Model Papers", Icons.Outlined.Article, chapter.papers),
        ResourceGroup("Textbooks", Icons.Outlined.MenuBook, chapter.textbooks),
        ResourceGroup("Other Files", Icons.Outlined.Folder, chapter.other)
    ).filter { it.resources.isNotEmpty() }
    if (groups.isEmpty()) {
        EmptyChapterBlock(
            icon = Icons.Outlined.Description,
            message = "No study files are attached to this chapter yet."
        )
        return
    }
    Column(verticalArrangement = Arrangement.spacedBy(18.dp)) {
        groups.forEach { group ->
            StudyResourceGroup(group = group, onResourceClick = onResourceClick)
        }
    }
}

private data class ResourceGroup(
    val title: String,
    val icon: ImageVector,
    val resources: List<ApiResource>
)

@Composable
private fun StudyResourceGroup(group: ResourceGroup, onResourceClick: (String) -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Icon(
                imageVector = group.icon,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(18.dp)
            )
            Text(
                text = group.title,
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Bold
            )
        }
        Row(
            modifier = Modifier.horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            group.resources.forEach { resource ->
                WebResourceCard(
                    resource = resource,
                    onClick = { onResourceClick(resource.id) },
                    modifier = Modifier.width(220.dp),
                    minWidth = null
                )
            }
        }
    }
}

@Composable
fun EmptyChapterBlock(icon: ImageVector, message: String) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.42f),
            modifier = Modifier.size(40.dp)
        )
        Text(
            text = message,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontWeight = FontWeight.Medium
        )
    }
}
