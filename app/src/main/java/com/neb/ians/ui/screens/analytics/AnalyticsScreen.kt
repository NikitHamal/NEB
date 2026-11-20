package com.neb.ians.ui.screens.analytics

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.CloudOff
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.ApiPrivateAnalyticsResponse
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebChoiceChips
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebLoader

/**
 * The member's own analytics. Everything on it comes from one request
 * (`api/users/me/analytics/?days=`), see backend_python/docs/ANALYTICS.md.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AnalyticsScreen(
    onNavigateBack: () -> Unit,
    onPostClick: (String) -> Unit = {},
    onResourceClick: (String) -> Unit = {},
    viewModel: AnalyticsViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val data = uiState.data

    Scaffold(
        topBar = {
            Column {
                TopAppBar(
                    title = { Text("Analytics", fontWeight = FontWeight.SemiBold) },
                    navigationIcon = {
                        IconButton(onClick = onNavigateBack) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
                )
                if (uiState.isRefreshing) {
                    LinearProgressIndicator(Modifier.fillMaxWidth().height(2.dp))
                } else {
                    Box(Modifier.height(2.dp))
                }
            }
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        when {
            data != null && data.version >= 2 -> AnalyticsContent(
                data = data,
                days = uiState.days,
                onRange = viewModel::selectRange,
                onPostClick = onPostClick,
                onResourceClick = onResourceClick,
                modifier = Modifier.padding(padding)
            )
            uiState.isLoading -> Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) { NebLoader() }
            else -> Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                NebEmptyState(
                    icon = Icons.Outlined.CloudOff,
                    title = if (data != null) "Analytics is updating" else "Analytics unavailable",
                    subtitle = when {
                        data != null -> "The new analytics are not live on the server yet."
                        else -> uiState.error ?: "Try again in a moment."
                    },
                    action = {
                        NebButton(
                            text = "Try again",
                            onClick = viewModel::load,
                            tone = NebButtonTone.Outlined,
                            size = NebButtonSize.Small
                        )
                    }
                )
            }
        }
    }
}

@Composable
private fun AnalyticsContent(
    data: ApiPrivateAnalyticsResponse,
    days: Int,
    onRange: (Int) -> Unit,
    onPostClick: (String) -> Unit,
    onResourceClick: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxSize()) {
        NebChoiceChips(
            options = AnalyticsRanges.map { "$it days" },
            selectedIndex = AnalyticsRanges.indexOf(days).coerceAtLeast(0),
            onSelect = { onRange(AnalyticsRanges[it]) },
            modifier = Modifier.padding(horizontal = AnalyticsGutter, vertical = 6.dp)
        )
        LazyColumn(
            modifier = Modifier.weight(1f).fillMaxWidth(),
            contentPadding = PaddingValues(top = 6.dp, bottom = 40.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            item(key = "standing") { StandingHero(data.standing) }
        item(key = "streak") { StreakCard(data.streak, data.trend) }
        item(key = "insights") { InsightsCard(data.insights) }
        item(key = "kpis") { KpiGrid(data.overview) }
        item(key = "trend") { TrendCard(data.trend, days) }
        item(key = "consistency") { ConsistencyCard(data.heatmap, data.streak.activeDays30) }
        item(key = "rhythm") { RhythmCard(data.rhythm) }
        item(key = "mix") { MixCard(data.mix, days) }
        item(key = "reach") { ReachCard(data.reach, days) }
        item(key = "helpfulness") { HelpfulnessCard(data.helpfulness, data.stats) }
        item(key = "community") { CommunityCard(data.stats, data.library) }
        item(key = "topPosts") { TopPostsCard(data.topPosts, onPostClick) }
        ResourceInsightsNav.open?.let { open ->
            item(key = "libraryInsights") {
                Box(Modifier.padding(horizontal = AnalyticsGutter)) {
                    NebButton(
                        text = "Library insights",
                        onClick = { open(null) },
                        tone = NebButtonTone.Outlined,
                        size = NebButtonSize.Small
                    )
                }
            }
        }
        item(key = "topResources") { TopResourcesCard(data.topResources, onResourceClick) }
        item(key = "topics") { TopicsCard(data.topCategories, data.topSubjects) }
        item(key = "milestones") { MilestonesCard(data.milestones) }
        }
    }
}
