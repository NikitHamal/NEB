package com.consica.code.ui.screens.path

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.consica.code.R
import com.consica.code.domain.model.LearningPath
import com.consica.code.ui.components.EcoCard
import com.consica.code.ui.components.XpProgressBar

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LearningPathScreen(
    onOpenLesson: (String) -> Unit,
    onBack: () -> Unit,
    viewModel: LearningPathViewModel = hiltViewModel(),
) {
    val state by viewModel.uiState.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.path_title), style = MaterialTheme.typography.titleLarge) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = stringResource(R.string.back))
                    }
                },
            )
        },
    ) { padding ->
        LazyColumn(
            Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(start = 20.dp, end = 20.dp, bottom = 32.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            items(state.sections, key = { it.path.name }) { section ->
                PathCard(section = section, onOpenLesson = onOpenLesson)
            }
        }
    }
}

@Composable
private fun PathCard(section: PathSection, onOpenLesson: (String) -> Unit) {
    EcoCard(modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(section.path.emoji(), style = MaterialTheme.typography.headlineMedium)
                Spacer(Modifier.width(10.dp))
                Column(Modifier.weight(1f)) {
                    Text(
                        stringResource(section.path.nameRes()),
                        style = MaterialTheme.typography.titleMedium,
                    )
                    Text(
                        stringResource(section.path.descRes()),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
            Spacer(Modifier.height(12.dp))
            XpProgressBar(
                progress = section.progressPercent / 100f,
                modifier = Modifier.fillMaxWidth(),
            )
            Spacer(Modifier.height(4.dp))
            Text(
                stringResource(R.string.path_progress, section.progressPercent),
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Spacer(Modifier.height(10.dp))
            section.lessons.forEach { lesson ->
                val completed = lesson.id in section.completedIds
                Row(
                    Modifier
                        .fillMaxWidth()
                        .padding(vertical = 6.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Icon(
                        Icons.Default.Check,
                        contentDescription = null,
                        tint = if (completed) MaterialTheme.colorScheme.primary
                        else MaterialTheme.colorScheme.outlineVariant,
                        modifier = Modifier.alpha(if (completed) 1f else 0.6f),
                    )
                    Spacer(Modifier.width(8.dp))
                    Text(
                        text = stringResource(lesson.titleRes),
                        style = MaterialTheme.typography.bodyLarge,
                        modifier = Modifier
                            .weight(1f)
                            .alpha(if (completed) 0.7f else 1f),
                    )
                    androidx.compose.material3.TextButton(onClick = { onOpenLesson(lesson.id) }) {
                        Text(stringResource(R.string.path_open))
                    }
                }
            }
        }
    }
}

private fun LearningPath.emoji(): String = when (this) {
    LearningPath.BEGINNER_WEB -> "🌿"
    LearningPath.BEGINNER_PYTHON -> "🌻"
    LearningPath.INTERMEDIATE -> "🌳"
    LearningPath.ADVANCED -> "🏔️"
}

private fun LearningPath.nameRes(): Int = when (this) {
    LearningPath.BEGINNER_WEB -> R.string.path_beginner_web
    LearningPath.BEGINNER_PYTHON -> R.string.path_beginner_python
    LearningPath.INTERMEDIATE -> R.string.path_intermediate
    LearningPath.ADVANCED -> R.string.path_advanced
}

private fun LearningPath.descRes(): Int = when (this) {
    LearningPath.BEGINNER_WEB -> R.string.path_beginner_web_desc
    LearningPath.BEGINNER_PYTHON -> R.string.path_beginner_python_desc
    LearningPath.INTERMEDIATE -> R.string.path_intermediate_desc
    LearningPath.ADVANCED -> R.string.path_advanced_desc
}
