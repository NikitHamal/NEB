package com.neb.ians.ui.screens.bookmarks

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
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
import com.neb.ians.data.api.ApiBookmark
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.ui.components.WebChip
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.util.formatTimeAgo
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class BookmarkListItem(
    val bookmark: ApiBookmark,
    val title: String,
    val excerpt: String,
    val meta: String
)

data class BookmarksUiState(
    val items: List<BookmarkListItem> = emptyList(),
    val selectedType: String = "all",
    val totalCount: Int = 0,
    val isLoading: Boolean = true,
    val error: String? = null
)

@HiltViewModel
class BookmarksViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(BookmarksUiState())
    val uiState: StateFlow<BookmarksUiState> = _uiState.asStateFlow()

    init {
        load()
    }

    fun selectType(type: String) {
        _uiState.update { it.copy(selectedType = type) }
    }

    fun load() {
        viewModelScope.launch {
            val token = authRepository.getBearerToken()
            if (token == null) {
                _uiState.update { it.copy(isLoading = false, error = "Sign in to view bookmarks") }
                return@launch
            }
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val page = apiService.getBookmarks(token)
                val enriched = page.bookmarks.take(60).map { bookmark ->
                    async { enrichBookmark(token, bookmark) }
                }.awaitAll()
                _uiState.update { it.copy(items = enriched, totalCount = page.totalCount, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = e.localizedMessage ?: "Could not load bookmarks") }
            }
        }
    }

    private suspend fun enrichBookmark(token: String, bookmark: ApiBookmark): BookmarkListItem {
        return try {
            when (bookmark.targetType) {
                "resource" -> {
                    val resource = apiService.getResource(token, bookmark.targetId)
                    BookmarkListItem(
                        bookmark = bookmark,
                        title = resource.title,
                        excerpt = resource.description,
                        meta = listOf(resource.subject, resource.gradeLevel, resource.type).filter { it.isNotBlank() }.joinToString(" - ")
                    )
                }
                "post" -> {
                    val post = apiService.getPost(token, bookmark.targetId)
                    BookmarkListItem(
                        bookmark = bookmark,
                        title = post.title,
                        excerpt = post.content,
                        meta = "${post.authorName} - ${post.replyCount} replies"
                    )
                }
                else -> BookmarkListItem(
                    bookmark = bookmark,
                    title = "Saved reply",
                    excerpt = "Open this saved reply from the related discussion on the web.",
                    meta = "Reply"
                )
            }
        } catch (_: Exception) {
            BookmarkListItem(
                bookmark = bookmark,
                title = bookmark.targetType.replaceFirstChar { it.uppercase() },
                excerpt = bookmark.targetId,
                meta = "Saved ${formatTimeAgo(bookmark.createdAt)}"
            )
        }
    }
}

@Composable
fun BookmarksScreen(
    onNavigateBack: () -> Unit,
    onResourceClick: (String) -> Unit,
    onPostClick: (String) -> Unit,
    onSearchClick: () -> Unit = {},
    viewModel: BookmarksViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val visibleItems = uiState.items.filter { uiState.selectedType == "all" || it.bookmark.targetType == uiState.selectedType }

    Scaffold(
        topBar = {
            WebTopBar(
                title = "Bookmarks",
                subtitle = "${uiState.totalCount} saved",
                showBack = true,
                onBackClick = onNavigateBack,
                onSearchClick = onSearchClick
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            Row(
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                listOf("all" to "All", "post" to "Posts", "reply" to "Replies", "resource" to "Resources").forEach { (type, label) ->
                    WebChip(text = label, selected = uiState.selectedType == type, onClick = { viewModel.selectType(type) })
                }
            }
            when {
                uiState.isLoading -> {
                    Column(
                        modifier = Modifier.fillMaxSize(),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) { CircularProgressIndicator() }
                }
                uiState.error != null -> {
                    WebEmptyState(
                        title = "Bookmarks unavailable",
                        message = uiState.error ?: "Try again later.",
                        icon = painterResource(id = R.drawable.ic_bookmark),
                        modifier = Modifier.padding(16.dp)
                    )
                }
                visibleItems.isEmpty() -> {
                    WebEmptyState(
                        title = "No bookmarks yet",
                        message = "Save posts, replies, and resources from across NEBians and they will appear here.",
                        icon = painterResource(id = R.drawable.ic_bookmark),
                        modifier = Modifier.padding(16.dp)
                    )
                }
                else -> {
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 4.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        items(visibleItems, key = { it.bookmark.id }) { item ->
                            BookmarkCard(
                                item = item,
                                onClick = {
                                    when (item.bookmark.targetType) {
                                        "resource" -> onResourceClick(item.bookmark.targetId)
                                        "post" -> onPostClick(item.bookmark.targetId)
                                    }
                                }
                            )
                        }
                        item { Spacer(modifier = Modifier.height(32.dp)) }
                    }
                }
            }
        }
    }
}

@Composable
private fun BookmarkCard(item: BookmarkListItem, onClick: () -> Unit) {
    val icon = when (item.bookmark.targetType) {
        "post" -> R.drawable.ic_forum_outlined
        "reply" -> R.drawable.ic_forum_filled
        else -> R.drawable.ic_book
    }
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.Top,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Surface(
                modifier = Modifier.size(44.dp),
                shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp),
                color = MaterialTheme.colorScheme.primaryContainer
            ) {
                androidx.compose.foundation.layout.Box(contentAlignment = Alignment.Center) {
                    Icon(
                        painter = painterResource(id = icon),
                        contentDescription = null,
                        modifier = Modifier.size(22.dp),
                        tint = MaterialTheme.colorScheme.primary
                    )
                }
            }
            Column(modifier = Modifier.weight(1f)) {
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                    WebChip(text = item.bookmark.targetType.replaceFirstChar { it.uppercase() }, selected = true)
                    Text(
                        text = formatTimeAgo(item.bookmark.createdAt),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Spacer(modifier = Modifier.height(6.dp))
                Text(
                    text = item.title,
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.Bold,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
                if (item.excerpt.isNotBlank()) {
                    Text(
                        text = item.excerpt,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                if (item.meta.isNotBlank()) {
                    Text(
                        text = item.meta,
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
        }
    }
}
