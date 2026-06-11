package com.consica.code.ui.screens

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.item
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.PlayCircle
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.consica.code.R
import com.consica.code.core.design.CardShape
import com.consica.code.core.design.Dimens
import com.consica.code.core.design.PillShape
import com.consica.code.domain.content.LessonCatalog
import com.consica.code.domain.content.LessonStatus
import com.consica.code.domain.content.Progression
import com.consica.code.ui.AppViewModel

@Composable
fun PathScreen(
    viewModel: AppViewModel,
    onOpenLesson: (String) -> Unit,
) {
    val prefs by viewModel.prefs.collectAsState()
    val completed by viewModel.completedLessonIds.collectAsState()

    LazyColumn(
        modifier = Modifier.fillMaxWidth(),
        contentPadding = PaddingValues(Dimens.screenPadding),
        verticalArrangement = Arrangement.spacedBy(Dimens.lg),
    ) {
        item {
            Text(
                stringResource(R.string.path_title),
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
            )
        }
        LessonCatalog.tracks.forEach { track ->
            val lessons = track.lessonIds.mapNotNull { LessonCatalog.byId(it) }
            val doneCount = lessons.count { it.id in completed }
            item(key = "track_${track.id}") {
                Column(Modifier.fillMaxWidth()) {
                    Text(
                        stringResource(track.titleRes),
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                    )
                    Spacer(Modifier.height(Dimens.sm))
                    LinearProgressIndicator(
                        progress = { if (lessons.isEmpty()) 0f else doneCount.toFloat() / lessons.size },
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(8.dp),
                        trackColor = MaterialTheme.colorScheme.surfaceVariant,
                    )
                    Spacer(Modifier.height(Dimens.xs))
                    Text(
                        stringResource(R.string.path_progress, doneCount, lessons.size),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
            items@ for (lesson in lessons) {
                item(key = lesson.id) {
                    val status = Progression.status(lesson.id, completed, prefs.proUnlocked)
                    PathLessonRow(
                        title = stringResource(lesson.titleRes),
                        status = status,
                        onClick = { if (status != LessonStatus.LOCKED) onOpenLesson(lesson.id) },
                    )
                }
            }
        }
        item { Spacer(Modifier.height(Dimens.xl)) }
    }
}

@Composable
private fun PathLessonRow(title: String, status: LessonStatus, onClick: () -> Unit) {
    val (icon, tint) = when (status) {
        LessonStatus.COMPLETED -> Icons.Filled.CheckCircle to MaterialTheme.colorScheme.primary
        LessonStatus.ACTIVE -> Icons.Filled.PlayCircle to MaterialTheme.colorScheme.secondary
        LessonStatus.LOCKED -> Icons.Filled.Lock to MaterialTheme.colorScheme.outline
    }
    Surface(
        onClick = onClick,
        enabled = status != LessonStatus.LOCKED,
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Row(
            Modifier.padding(Dimens.cardPadding),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Box(
                Modifier
                    .size(Dimens.iconButton)
                    .clip(PillShape)
                    .background(tint.copy(alpha = 0.14f)),
                contentAlignment = Alignment.Center,
            ) {
                Icon(icon, contentDescription = null, tint = tint)
            }
            Spacer(Modifier.width(Dimens.lg))
            Column(Modifier.weight(1f)) {
                Text(
                    title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                    color = if (status == LessonStatus.LOCKED)
                        MaterialTheme.colorScheme.onSurfaceVariant else MaterialTheme.colorScheme.onSurface,
                )
                if (status == LessonStatus.LOCKED) {
                    Text(
                        stringResource(R.string.path_locked),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }
    }
}
