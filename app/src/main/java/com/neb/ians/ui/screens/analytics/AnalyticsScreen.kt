package com.neb.ians.ui.screens.analytics

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import com.neb.ians.R
import com.neb.ians.data.api.ApiProfileStats
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebKpiCard
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

data class AnalyticsUiState(
    val username: String = "",
    val stats: ApiProfileStats? = null,
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
                val profile = authRepository.userProfileFlow.first()
                val username = profile?.username?.takeIf { it.isNotBlank() }
                    ?: authRepository.currentUserNameFlow.first()
                if (username.isBlank() || username == "Guest") {
                    _uiState.update { it.copy(isLoading = false, error = "Sign in to view analytics") }
                    return@launch
                }
                val stats = apiService.getProfileStats(authRepository.getBearerToken(), username)
                _uiState.update { it.copy(username = username, stats = stats, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = e.localizedMessage ?: "Could not load analytics") }
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
            uiState.isLoading -> {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) { CircularProgressIndicator() }
            }
            uiState.error != null -> {
                WebEmptyState(
                    title = "Analytics unavailable",
                    message = uiState.error ?: "Try again later.",
                    icon = painterResource(id = R.drawable.ic_school),
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding)
                )
            }
            uiState.stats != null -> {
                AnalyticsContent(
                    stats = uiState.stats!!,
                    modifier = Modifier.padding(padding)
                )
            }
        }
    }
}

@Composable
private fun AnalyticsContent(stats: ApiProfileStats, modifier: Modifier = Modifier) {
    LazyColumn(
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 16.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        item {
            Column {
                Text(
                    text = "Analytics",
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.ExtraBold
                )
                Text(
                    text = "Private insights for your NEBians activity, community footprint, and learning loop.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 3,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
        item {
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                WebKpiCard(
                    label = "Posts",
                    value = compactCount(stats.postCount),
                    detail = "${compactCount(stats.replyCount)} replies made",
                    painter = painterResource(id = R.drawable.ic_forum_outlined),
                    modifier = Modifier.weight(1f)
                )
                WebKpiCard(
                    label = "Likes",
                    value = compactCount(stats.likesReceived),
                    detail = "${compactCount(stats.likesGiven)} likes given",
                    painter = painterResource(id = R.drawable.ic_bookmark),
                    modifier = Modifier.weight(1f)
                )
            }
        }
        item {
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                WebKpiCard(
                    label = "Followers",
                    value = compactCount(stats.followerCount),
                    detail = "${compactCount(stats.followingCount)} following",
                    painter = painterResource(id = R.drawable.ic_school),
                    modifier = Modifier.weight(1f)
                )
                WebKpiCard(
                    label = "Score",
                    value = compactCount(stats.contributionScore),
                    detail = if (stats.isPrivate) "Private profile" else "Public contribution",
                    painter = painterResource(id = R.drawable.ic_science),
                    modifier = Modifier.weight(1f)
                )
            }
        }
        item {
            androidx.compose.material3.Surface(
                modifier = Modifier.fillMaxWidth(),
                shape = WebPanelShape,
                color = MaterialTheme.colorScheme.surfaceContainerLowest,
                border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
            ) {
                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(
                        text = "Suggestions",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    val suggestions = buildList {
                        if (stats.postCount == 0) add("Start one useful forum discussion to build your profile.")
                        if (stats.replyCount < stats.postCount) add("Reply to other learners to grow your community footprint.")
                        if (stats.likesReceived == 0) add("Share clearer titles and context so posts are easier to discover.")
                        if (isEmpty()) add("Your community loop looks healthy. Keep contributing steadily.")
                    }
                    suggestions.forEach {
                        Text(
                            text = it,
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }
        item { Spacer(modifier = Modifier.height(32.dp)) }
    }
}
