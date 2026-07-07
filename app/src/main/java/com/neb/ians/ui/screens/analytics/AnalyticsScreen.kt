package com.neb.ians.ui.screens.analytics

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.AccountTree
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.FolderOpen
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.Groups
import androidx.compose.material.icons.outlined.Lightbulb
import androidx.compose.material.icons.outlined.QueryStats
import androidx.compose.material.icons.outlined.Quiz
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import com.neb.ians.R
import com.neb.ians.data.api.ApiAnalyticsDay
import com.neb.ians.data.api.ApiAnalyticsPost
import com.neb.ians.data.api.ApiAnalyticsResource
import com.neb.ians.data.api.ApiAnalyticsStats
import com.neb.ians.data.api.ApiAnalyticsTopic
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiPrivateAnalyticsResponse
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.ui.components.compactCount
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject
import kotlin.math.max

data class AnalyticsUiState(
    val data: ApiPrivateAnalyticsResponse? = null,
    val username: String = "",
    val isLoading: Boolean = true,
    val error: String? = null
)

@HiltViewModel
class AnalyticsViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(AnalyticsUiState())
    val uiState: StateFlow<AnalyticsUiState> = _uiState.asStateFlow()

    init {
        load()
    }

    fun load() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val token = authRepository.getBearerToken()
                if (token.isNullOrBlank()) {
                    _uiState.update { it.copy(isLoading = false, error = "Sign in to view analytics") }
                    return@launch
                }
                val data = apiService.getPrivateAnalytics(token)
                val fallbackUsername = authRepository.userProfileFlow.first()?.username.orEmpty()
                _uiState.update {
                    it.copy(
                        data = data,
                        username = data.username.ifBlank { fallbackUsername },
                        isLoading = false
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = ApiErrorMapper.mapException(e)) }
            }
        }
    }
}

@Composable
fun AnalyticsScreen(
    onNavigateBack: () -> Unit,
    onSearchClick: () -> Unit = {},
    viewModel: AnalyticsViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Scaffold(
        topBar = {
            WebTopBar(
                title = "Analytics",
                subtitle = if (uiState.username.isBlank()) "Private insights" else "@${uiState.username}",
                showBack = true,
                onBackClick = onNavigateBack,
                onSearchClick = onSearchClick
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        when {
            uiState.isLoading -> Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentAlignment = Alignment.Center
            ) { CircularProgressIndicator() }
            uiState.error != null -> WebEmptyState(
                title = "Analytics unavailable",
                message = uiState.error ?: "Try again later.",
                icon = painterResource(id = R.drawable.ic_school),
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
            )
            uiState.data != null -> AnalyticsContent(
                data = uiState.data!!,
                modifier = Modifier.padding(padding)
            )
        }
    }
}

@Composable
private fun AnalyticsContent(data: ApiPrivateAnalyticsResponse, modifier: Modifier = Modifier) {
    val stats = data.stats
    LazyColumn(
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 18.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        item {
            AnalyticsHero(stats)
        }
        item {
            DashboardKpiGrid(stats)
        }
        item {
            ActivityChartCard(data.activityDays, stats.recentStudyActions)
        }
        item {
            StudyProgressCard(stats)
        }
        item {
            CommunityDashboardCard(stats)
        }
        item {
            TopicDashboardCard(
                postTopics = data.topCategories,
                resourceTopics = data.topSubjects
            )
        }
        item {
            DashboardTableCard(
                title = "Top posts",
                subtitle = "Ranked by views and likes",
                emptyMessage = "No posts yet.",
                rows = data.topPosts
            )
        }
        item {
            ResourceTableCard(
                title = "Top resources",
                subtitle = "Ranked by views and likes",
                emptyMessage = "No resources yet.",
                rows = data.topResources
            )
        }
        item {
            SuggestionsCard(data.suggestions)
        }
        item { Spacer(modifier = Modifier.height(32.dp)) }
    }
}

@Composable
private fun AnalyticsHero(stats: ApiAnalyticsStats) {
    AnalyticsCard {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            Surface(
                shape = CircleShape,
                color = MaterialTheme.colorScheme.primaryContainer,
                contentColor = MaterialTheme.colorScheme.onPrimaryContainer,
                modifier = Modifier.size(48.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(Icons.Outlined.QueryStats, contentDescription = null, modifier = Modifier.size(26.dp))
                }
            }
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = "Analytics dashboard",
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.ExtraBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Text(
                    text = "Private insights for posts, resources, comments, and Study Lab progress.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
        Spacer(modifier = Modifier.height(14.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
            HeroMetric("Reach", compactCount(stats.postViews + stats.resourceViews), Icons.Outlined.Visibility, Modifier.weight(1f))
            HeroMetric("Engagement", compactCount(stats.postLikesReceived + stats.resourceLikesReceived + stats.postRepliesReceived), Icons.Outlined.ThumbUp, Modifier.weight(1f))
        }
    }
}

@Composable
private fun DashboardKpiGrid(stats: ApiAnalyticsStats) {
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
            KpiTile("Posts", compactCount(stats.posts), "${compactCount(stats.recentPosts)} in 30d", Icons.Outlined.Forum, Modifier.weight(1f))
            KpiTile("Post views", compactCount(stats.postViews), "${compactCount(stats.postLikesReceived)} likes", Icons.Outlined.Visibility, Modifier.weight(1f))
        }
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
            KpiTile("Resources", compactCount(stats.resources), "${compactCount(stats.resourceViews)} views", Icons.Outlined.FolderOpen, Modifier.weight(1f))
            KpiTile("Study docs", compactCount(stats.studyDocs), "${compactCount(stats.summaries)} summaries", Icons.Outlined.School, Modifier.weight(1f))
        }
    }
}

@Composable
private fun KpiTile(label: String, value: String, detail: String, icon: ImageVector, modifier: Modifier = Modifier) {
    AnalyticsCard(modifier = modifier) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            Surface(
                shape = CircleShape,
                color = MaterialTheme.colorScheme.surfaceContainerHigh,
                contentColor = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(38.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(icon, contentDescription = null, modifier = Modifier.size(21.dp))
                }
            }
            Column(modifier = Modifier.weight(1f)) {
                Text(value, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.ExtraBold, maxLines = 1)
                Text(label, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
            }
        }
        Spacer(modifier = Modifier.height(10.dp))
        Text(detail, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
    }
}

@Composable
private fun HeroMetric(label: String, value: String, icon: ImageVector, modifier: Modifier = Modifier) {
    Surface(
        modifier = modifier,
        shape = RoundedCornerShape(18.dp),
        color = MaterialTheme.colorScheme.surfaceContainer,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(18.dp))
            Column {
                Text(value, fontWeight = FontWeight.ExtraBold, maxLines = 1)
                Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1)
            }
        }
    }
}

@Composable
private fun ActivityChartCard(days: List<ApiAnalyticsDay>, recentStudyActions: Int) {
    AnalyticsCard {
        DashboardHeader("14-day activity", "Posts, replies, uploads, quiz attempts, and flashcard reviews.", "${compactCount(recentStudyActions)} study actions")
        Spacer(modifier = Modifier.height(16.dp))
        val chartDays = days.ifEmpty { listOf(ApiAnalyticsDay(label = "Today")) }
        val maxTotal = max(1, chartDays.maxOf { it.total })
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .height(184.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalAlignment = Alignment.Bottom
        ) {
            chartDays.forEach { day ->
                Column(
                    modifier = Modifier.weight(1f),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Bottom
                ) {
                    Box(
                        modifier = Modifier
                            .height(146.dp)
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(999.dp))
                            .background(MaterialTheme.colorScheme.surfaceContainerHigh)
                    ) {
                        Box(
                            modifier = Modifier
                                .align(Alignment.BottomCenter)
                                .fillMaxWidth()
                                .height((146f * (day.total.toFloat() / maxTotal.toFloat())).dp.coerceAtLeast(6.dp))
                                .clip(RoundedCornerShape(999.dp))
                                .background(MaterialTheme.colorScheme.primary)
                        )
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(day.label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1)
                }
            }
        }
        Spacer(modifier = Modifier.height(12.dp))
        ChartLegend()
    }
}

@Composable
private fun ChartLegend() {
    Row(horizontalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.fillMaxWidth()) {
        LegendItem("Posts")
        LegendItem("Replies")
        LegendItem("Resources")
        LegendItem("Study")
    }
}

@Composable
private fun LegendItem(text: String) {
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(5.dp)) {
        Box(modifier = Modifier.size(7.dp).background(MaterialTheme.colorScheme.primary, CircleShape))
        Text(text, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1)
    }
}

@Composable
private fun StudyProgressCard(stats: ApiAnalyticsStats) {
    AnalyticsCard {
        DashboardHeader("Study Lab progress", "Generated materials and learning outcomes.", null)
        Spacer(modifier = Modifier.height(16.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.CenterVertically) {
            DonutProgress(stats.quizAccuracy.coerceIn(0, 100), Modifier.size(112.dp))
            Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(9.dp)) {
                MiniRow(Icons.Outlined.Description, "Summaries", compactCount(stats.summaries))
                MiniRow(Icons.Outlined.AccountTree, "Mindmaps", compactCount(stats.mindmaps))
                MiniRow(Icons.Outlined.Quiz, "Quiz XP", compactCount(stats.quizXp))
                MiniRow(Icons.Outlined.BookmarkBorder, "Flash reviews", compactCount(stats.flashReviews))
            }
        }
        Spacer(modifier = Modifier.height(14.dp))
        ReviewSplit(stats)
    }
}

@Composable
private fun DonutProgress(percent: Int, modifier: Modifier = Modifier) {
    val primary = MaterialTheme.colorScheme.primary
    val track = MaterialTheme.colorScheme.surfaceContainerHigh
    Box(modifier = modifier, contentAlignment = Alignment.Center) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val stroke = Stroke(width = 16.dp.toPx(), cap = StrokeCap.Round)
            drawArc(track, -90f, 360f, false, style = stroke)
            drawArc(primary, -90f, 360f * percent / 100f, false, style = stroke)
        }
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text("$percent%", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.ExtraBold)
            Text("accuracy", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun ReviewSplit(stats: ApiAnalyticsStats) {
    val total = max(1, stats.easyReviews + stats.mediumReviews + stats.hardReviews)
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        ProgressMetric("Easy reviews", stats.easyReviews, total)
        ProgressMetric("Medium reviews", stats.mediumReviews, total)
        ProgressMetric("Hard reviews", stats.hardReviews, total)
    }
}

@Composable
private fun ProgressMetric(label: String, value: Int, total: Int) {
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text(label, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text(compactCount(value), style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold)
        }
        LinearProgressIndicator(
            progress = { value.toFloat() / total.toFloat() },
            modifier = Modifier.fillMaxWidth().height(7.dp).clip(RoundedCornerShape(999.dp)),
            trackColor = MaterialTheme.colorScheme.surfaceContainerHigh
        )
    }
}

@Composable
private fun CommunityDashboardCard(stats: ApiAnalyticsStats) {
    AnalyticsCard {
        DashboardHeader("Community footprint", "How your account contributes across NEBians.", null)
        Spacer(modifier = Modifier.height(12.dp))
        MetricTable(
            listOf(
                "Replies made" to stats.replies,
                "Resource comments" to stats.resourceCommentsMade,
                "Comments received" to stats.resourceCommentsReceived,
                "Followers" to stats.followers,
                "Following" to stats.following,
                "Bookmarks" to stats.bookmarks,
                "Unread notifications" to stats.notificationsUnread
            )
        )
    }
}

@Composable
private fun TopicDashboardCard(postTopics: List<ApiAnalyticsTopic>, resourceTopics: List<ApiAnalyticsTopic>) {
    AnalyticsCard {
        DashboardHeader("Top topics", "Based on your posts and resources.", null)
        Spacer(modifier = Modifier.height(12.dp))
        TopicList("Post categories", postTopics)
        Spacer(modifier = Modifier.height(16.dp))
        TopicList("Resource subjects", resourceTopics)
    }
}

@Composable
private fun TopicList(title: String, rows: List<ApiAnalyticsTopic>) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text(title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.Bold)
        if (rows.isEmpty()) {
            Text("No data yet.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        } else {
            rows.forEach { row ->
                Column(verticalArrangement = Arrangement.spacedBy(5.dp)) {
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text(row.label, style = MaterialTheme.typography.bodySmall, maxLines = 1, overflow = TextOverflow.Ellipsis, modifier = Modifier.weight(1f))
                        Text(row.count.toString(), style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold)
                    }
                    LinearProgressIndicator(
                        progress = { row.width.coerceIn(0, 100) / 100f },
                        modifier = Modifier.fillMaxWidth().height(7.dp).clip(RoundedCornerShape(999.dp)),
                        trackColor = MaterialTheme.colorScheme.surfaceContainerHigh
                    )
                }
            }
        }
    }
}

@Composable
private fun DashboardTableCard(title: String, subtitle: String, emptyMessage: String, rows: List<ApiAnalyticsPost>) {
    AnalyticsCard {
        DashboardHeader(title, subtitle, null)
        Spacer(modifier = Modifier.height(10.dp))
        if (rows.isEmpty()) {
            EmptyDashboardText(emptyMessage)
        } else {
            rows.forEachIndexed { index, row ->
                TableRow(
                    rank = index + 1,
                    title = row.title,
                    meta = row.category,
                    rightTop = compactCount(row.viewCount),
                    rightBottom = "${compactCount(row.likeCount)} likes · ${compactCount(row.replyCount)} replies"
                )
            }
        }
    }
}

@Composable
private fun ResourceTableCard(title: String, subtitle: String, emptyMessage: String, rows: List<ApiAnalyticsResource>) {
    AnalyticsCard {
        DashboardHeader(title, subtitle, null)
        Spacer(modifier = Modifier.height(10.dp))
        if (rows.isEmpty()) {
            EmptyDashboardText(emptyMessage)
        } else {
            rows.forEachIndexed { index, row ->
                TableRow(
                    rank = index + 1,
                    title = row.title,
                    meta = listOf(row.subject, row.type).filter { it.isNotBlank() }.joinToString(" · "),
                    rightTop = compactCount(row.viewCount),
                    rightBottom = "${compactCount(row.likeCount)} likes · ${compactCount(row.commentCount)} comments"
                )
            }
        }
    }
}

@Composable
private fun TableRow(rank: Int, title: String, meta: String, rightTop: String, rightBottom: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 9.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Surface(
            shape = CircleShape,
            color = MaterialTheme.colorScheme.surfaceContainerHigh,
            modifier = Modifier.size(28.dp)
        ) {
            Box(contentAlignment = Alignment.Center) {
                Text(rank.toString(), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold)
            }
        }
        Column(modifier = Modifier.weight(1f)) {
            Text(title.ifBlank { "Untitled" }, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
            Text(meta.ifBlank { "General" }, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
        }
        Column(horizontalAlignment = Alignment.End) {
            Text(rightTop, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.ExtraBold, maxLines = 1)
            Text(rightBottom, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
        }
    }
}

@Composable
private fun SuggestionsCard(items: List<String>) {
    AnalyticsCard {
        DashboardHeader("Suggestions", "Context-aware next steps.", null)
        Spacer(modifier = Modifier.height(10.dp))
        val rows = items.ifEmpty { listOf("Keep contributing steadily. Your dashboard will become richer as you use NEBians more.") }
        rows.forEach { item ->
            Row(
                modifier = Modifier.padding(vertical = 7.dp),
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                verticalAlignment = Alignment.Top
            ) {
                Icon(Icons.Outlined.Lightbulb, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(20.dp))
                Text(item, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
            }
        }
    }
}

@Composable
private fun DashboardHeader(title: String, subtitle: String, chip: String?) {
    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.Top) {
        Column(modifier = Modifier.weight(1f)) {
            Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.ExtraBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
            Text(subtitle, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 2, overflow = TextOverflow.Ellipsis)
        }
        if (!chip.isNullOrBlank()) {
            Spacer(modifier = Modifier.width(8.dp))
            Surface(shape = CircleShape, color = MaterialTheme.colorScheme.primaryContainer, contentColor = MaterialTheme.colorScheme.onPrimaryContainer) {
                Text(chip, style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp), maxLines = 1)
            }
        }
    }
}

@Composable
private fun MiniRow(icon: ImageVector, label: String, value: String) {
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(18.dp))
        Text(label, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f), maxLines = 1)
        Text(value, style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Bold, maxLines = 1)
    }
}

@Composable
private fun MetricTable(rows: List<Pair<String, Int>>) {
    Column {
        rows.forEach { row ->
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(row.first, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis, modifier = Modifier.weight(1f))
                Text(compactCount(row.second), style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.ExtraBold, maxLines = 1)
            }
        }
    }
}

@Composable
private fun EmptyDashboardText(text: String) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(MaterialTheme.colorScheme.surfaceContainer)
            .padding(18.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(text, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

@Composable
private fun AnalyticsCard(modifier: Modifier = Modifier, content: @Composable Column.() -> Unit) {
    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp), content = content)
    }
}
