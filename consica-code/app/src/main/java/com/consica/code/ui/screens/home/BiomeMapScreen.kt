package com.consica.code.ui.screens.home

import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Code
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.LocalFireDepartment
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Terminal
import androidx.compose.material.icons.filled.WaterDrop
import androidx.compose.material.icons.filled.WbSunny
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.AppContainer
import com.consica.code.R
import com.consica.code.core.designsystem.LocalEcoUiConfig
import com.consica.code.core.designsystem.PillShape
import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.Biome
import com.consica.code.core.model.Lesson
import com.consica.code.core.model.LessonStatus
import com.consica.code.core.model.LessonType
import com.consica.code.core.model.TerraExpression
import com.consica.code.data.content.LessonCatalog
import com.consica.code.data.local.entity.LessonProgressEntity
import com.consica.code.data.local.entity.WorkspaceEntity
import com.consica.code.data.prefs.UserState
import com.consica.code.ui.character.TerraAvatar
import com.consica.code.ui.common.EcoCard
import com.consica.code.ui.common.OfflineBanner
import com.consica.code.ui.common.StatChip
import com.consica.code.ui.common.appViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn

data class HomeUiState(
    val user: UserState = UserState(),
    val progress: Map<String, LessonProgressEntity> = emptyMap(),
    val recentWorkspaces: List<WorkspaceEntity> = emptyList(),
    val online: Boolean = true,
    val loaded: Boolean = false,
)

class HomeViewModel(private val container: AppContainer) : ViewModel() {

    val state: StateFlow<HomeUiState> = combine(
        container.prefs.userState,
        container.learning.progressMap,
        container.learning.recentWorkspaces,
        container.connectivity.isOnline,
    ) { user, progress, workspaces, online ->
        HomeUiState(user, progress, workspaces, online, loaded = true)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), HomeUiState())

    fun statusFor(lesson: Lesson, progress: Map<String, LessonProgressEntity>): LessonStatus =
        container.learning.statusFor(lesson, progress)

    fun suggestedNext(progress: Map<String, LessonProgressEntity>): Lesson? =
        container.learning.suggestedNext(progress)
}

@Composable
fun BiomeMapScreen(
    onOpenLesson: (lessonId: String, isPuzzle: Boolean) -> Unit,
    onOpenPlayground: () -> Unit,
    onOpenWorkspace: (Long) -> Unit,
    onOpenSettings: () -> Unit,
) {
    val viewModel = appViewModel { HomeViewModel(it) }
    val state by viewModel.state.collectAsState()
    val user = state.user

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = androidx.compose.foundation.layout.PaddingValues(bottom = 32.dp),
    ) {
        item {
            HomeHeader(user = user, onOpenSettings = onOpenSettings)
        }

        item {
            OfflineBanner(
                visible = state.loaded && !state.online,
                title = stringResource(R.string.offline_title),
                body = stringResource(
                    when (user.ageGroup) {
                        AgeGroup.KIDS -> R.string.offline_body_kids
                        AgeGroup.TEENS -> R.string.offline_body_teens
                        AgeGroup.PRO -> R.string.offline_body_pro
                    },
                ),
            )
        }

        item {
            val next = viewModel.suggestedNext(state.progress)
            if (next != null) {
                SuggestedNextCard(
                    lesson = next,
                    onClick = { onOpenLesson(next.id, next.type == LessonType.PUZZLE && next.steps.isEmpty()) },
                )
            }
        }

        if (user.proToolsUnlocked) {
            item {
                QuickAccessRow(
                    recentWorkspaces = state.recentWorkspaces,
                    professional = user.professionalEditor,
                    onOpenPlayground = onOpenPlayground,
                    onOpenWorkspace = onOpenWorkspace,
                )
            }
        }

        for (biome in Biome.entries) {
            val lessons = LessonCatalog.lessonsFor(biome)
            if (lessons.isEmpty()) continue

            item(key = "biome_${biome.name}") {
                BiomeHeader(biome = biome, lessons = lessons, progress = state.progress)
            }

            items(lessons, key = { it.id }) { lesson ->
                val status = viewModel.statusFor(lesson, state.progress)
                LessonNode(
                    lesson = lesson,
                    status = status,
                    index = lesson.order,
                    onClick = {
                        if (status != LessonStatus.LOCKED) {
                            onOpenLesson(lesson.id, false)
                        }
                    },
                )
            }
        }
    }
}

@Composable
private fun HomeHeader(user: UserState, onOpenSettings: () -> Unit) {
    Column(modifier = Modifier.padding(horizontal = 16.dp)) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 16.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = stringResource(
                        when (user.ageGroup) {
                            AgeGroup.KIDS -> R.string.home_greeting_kids
                            AgeGroup.TEENS -> R.string.home_greeting_teens
                            AgeGroup.PRO -> R.string.home_greeting_pro
                        },
                    ),
                    style = MaterialTheme.typography.headlineSmall,
                )
                Text(
                    text = stringResource(R.string.home_level_label, user.level) + "  ·  " +
                        stringResource(R.string.home_xp_label, user.xp),
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            Box(
                modifier = Modifier
                    .clip(CircleShape)
                    .clickable(onClick = onOpenSettings)
                    .semantics { contentDescription = "" },
            ) {
                TerraAvatar(expression = TerraExpression.HAPPY, size = 64.dp, bounce = false)
            }
        }

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 12.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            StatChip(
                icon = Icons.Filled.LocalFireDepartment,
                value = stringResource(R.string.home_streak_days, user.streak),
                contentDescription = stringResource(R.string.a11y_streak_counter),
                tint = MaterialTheme.colorScheme.error,
            )
            StatChip(
                icon = Icons.Filled.WbSunny,
                value = user.sunCoins.toString(),
                contentDescription = stringResource(R.string.a11y_sun_counter),
                tint = MaterialTheme.colorScheme.tertiary,
            )
            StatChip(
                icon = Icons.Filled.WaterDrop,
                value = user.waterDrops.toString(),
                contentDescription = stringResource(R.string.a11y_water_counter),
                tint = MaterialTheme.colorScheme.secondary,
            )
            StatChip(
                icon = Icons.Filled.Bolt,
                value = user.xp.toString(),
                contentDescription = stringResource(R.string.a11y_xp_counter),
            )
        }
    }
}

@Composable
private fun SuggestedNextCard(lesson: Lesson, onClick: () -> Unit) {
    EcoCard(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 12.dp),
        containerColor = MaterialTheme.colorScheme.primaryContainer,
    ) {
        Column(Modifier.padding(20.dp)) {
            Text(
                stringResource(R.string.home_suggested_next),
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onPrimaryContainer,
            )
            Text(
                stringResource(lesson.titleRes),
                style = MaterialTheme.typography.titleLarge,
                color = MaterialTheme.colorScheme.onPrimaryContainer,
            )
            Text(
                stringResource(lesson.descriptionRes),
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.85f),
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
            )
            Box(Modifier.height(12.dp))
            Button(onClick = onClick, shape = PillShape) {
                Icon(Icons.Filled.PlayArrow, contentDescription = null, modifier = Modifier.size(18.dp))
                Box(Modifier.width(6.dp))
                Text(stringResource(R.string.home_continue_lesson))
            }
        }
    }
}

@Composable
private fun QuickAccessRow(
    recentWorkspaces: List<WorkspaceEntity>,
    professional: Boolean,
    onOpenPlayground: () -> Unit,
    onOpenWorkspace: (Long) -> Unit,
) {
    Column(modifier = Modifier.padding(horizontal = 16.dp)) {
        Text(
            stringResource(R.string.home_quick_access),
            style = MaterialTheme.typography.titleMedium,
            modifier = Modifier.padding(vertical = 8.dp),
        )
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            OutlinedButton(
                onClick = onOpenPlayground,
                shape = PillShape,
                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
            ) {
                Icon(Icons.Filled.Terminal, contentDescription = null, modifier = Modifier.size(16.dp))
                Box(Modifier.width(6.dp))
                Text(
                    stringResource(
                        if (professional) R.string.home_pro_editor else R.string.home_open_playground,
                    ),
                    maxLines = 1,
                )
            }
        }
        if (recentWorkspaces.isNotEmpty()) {
            Text(
                stringResource(R.string.home_recent_workspaces),
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(top = 12.dp, bottom = 4.dp),
            )
            recentWorkspaces.take(3).forEach { ws ->
                Surface(
                    shape = MaterialTheme.shapes.medium,
                    color = MaterialTheme.colorScheme.surface,
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 3.dp)
                        .clickable { onOpenWorkspace(ws.id) },
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        Icon(
                            Icons.Filled.Code,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.size(18.dp),
                        )
                        Box(Modifier.width(10.dp))
                        Text(ws.name, style = MaterialTheme.typography.bodyMedium, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Box(Modifier.weight(1f))
                        Text(
                            ws.language,
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun BiomeHeader(
    biome: Biome,
    lessons: List<Lesson>,
    progress: Map<String, LessonProgressEntity>,
) {
    val done = lessons.count { progress[it.id]?.completed == true }
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 12.dp),
    ) {
        Text(stringResource(biome.titleRes), style = MaterialTheme.typography.headlineSmall)
        Text(
            stringResource(biome.subtitleRes),
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Text(
            text = if (done == lessons.size) {
                stringResource(R.string.home_path_complete)
            } else {
                stringResource(R.string.home_lessons_done, done, lessons.size)
            },
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.primary,
            modifier = Modifier.padding(top = 4.dp),
        )
    }
}

@Composable
private fun LessonNode(
    lesson: Lesson,
    status: LessonStatus,
    index: Int,
    onClick: () -> Unit,
) {
    val config = LocalEcoUiConfig.current
    // Winding path: alternate node offset left/right
    val offsetFraction = when (index % 4) {
        0 -> 0.0f
        1 -> 0.25f
        2 -> 0.5f
        else -> 0.25f
    }

    val pulse: Float
    if (status == LessonStatus.UNLOCKED && !config.reducedMotion) {
        val transition = rememberInfiniteTransition(label = "nodePulse")
        val animated by transition.animateFloat(
            initialValue = 1f,
            targetValue = 1.08f,
            animationSpec = infiniteRepeatable(tween(800), RepeatMode.Reverse),
            label = "nodePulseScale",
        )
        pulse = animated
    } else {
        pulse = 1f
    }

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Box(Modifier.weight(0.1f + offsetFraction))
        Surface(
            shape = MaterialTheme.shapes.large,
            color = when (status) {
                LessonStatus.COMPLETED -> MaterialTheme.colorScheme.primaryContainer
                LessonStatus.UNLOCKED -> MaterialTheme.colorScheme.surface
                LessonStatus.LOCKED -> MaterialTheme.colorScheme.surfaceVariant
            },
            border = BorderStroke(
                width = if (status == LessonStatus.UNLOCKED) 2.dp else 1.dp,
                color = when (status) {
                    LessonStatus.UNLOCKED -> MaterialTheme.colorScheme.primary
                    else -> MaterialTheme.colorScheme.outlineVariant
                },
            ),
            modifier = Modifier
                .weight(2f)
                .scale(pulse)
                .alpha(if (status == LessonStatus.LOCKED) 0.55f else 1f)
                .clickable(enabled = status != LessonStatus.LOCKED, onClick = onClick)
                .semantics {
                    contentDescription = ""
                },
        ) {
            Row(
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 14.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Box(
                    modifier = Modifier
                        .size(36.dp)
                        .clip(CircleShape)
                        .background(
                            when (status) {
                                LessonStatus.COMPLETED -> MaterialTheme.colorScheme.primary
                                LessonStatus.UNLOCKED -> MaterialTheme.colorScheme.primaryContainer
                                LessonStatus.LOCKED -> MaterialTheme.colorScheme.outlineVariant
                            },
                        ),
                    contentAlignment = Alignment.Center,
                ) {
                    when (status) {
                        LessonStatus.COMPLETED -> Icon(
                            Icons.Filled.Check,
                            contentDescription = stringResource(R.string.a11y_lesson_completed),
                            tint = MaterialTheme.colorScheme.onPrimary,
                            modifier = Modifier.size(20.dp),
                        )
                        LessonStatus.LOCKED -> Icon(
                            Icons.Filled.Lock,
                            contentDescription = stringResource(R.string.a11y_lesson_locked),
                            tint = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.size(18.dp),
                        )
                        LessonStatus.UNLOCKED -> Icon(
                            Icons.Filled.PlayArrow,
                            contentDescription = stringResource(R.string.a11y_lesson_active),
                            tint = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.size(20.dp),
                        )
                    }
                }
                Box(Modifier.width(12.dp))
                Column(Modifier.weight(1f)) {
                    Text(
                        stringResource(lesson.titleRes),
                        style = MaterialTheme.typography.titleSmall,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis,
                    )
                    Text(
                        stringResource(lesson.descriptionRes),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                    )
                }
            }
        }
        Box(Modifier.weight(0.6f - offsetFraction))
    }
}
