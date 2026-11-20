package com.neb.ians.ui.components

import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.foundation.lazy.grid.LazyGridState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.snapshotFlow
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.distinctUntilChanged
import java.util.concurrent.ConcurrentHashMap

/**
 * Remembers where a reader tapped a post from, so the view that the post page records says
 * "feed" or "profile" instead of "direct". Read once, when the post page opens.
 */
object PostReachHints {
    private val surfaces = ConcurrentHashMap<String, String>()

    fun set(postId: String, surface: String) {
        if (postId.isNotBlank()) surfaces[postId] = surface
    }

    fun take(postId: String): String = surfaces.remove(postId) ?: "direct"
}

/**
 * Shared batcher behind every list tracker. An id counts once per list session, only what is
 * still on screen after a short pause counts (a fast fling does not), and the server turns the
 * batch into one impression per viewer per day.
 */
private suspend fun collectImpressions(
    visibleIds: () -> List<String>,
    onVisible: (List<String>) -> Unit
) {
    val seen = HashSet<String>()
    snapshotFlow { visibleIds() }
        .distinctUntilChanged()
        .collect { visible ->
            val fresh = visible.filter { seen.add(it) }
            if (fresh.isNotEmpty()) {
                delay(1200)
                val stillThere = visibleIds().toSet()
                val kept = fresh.filter { it in stillThere }
                (fresh - kept.toSet()).forEach { seen.remove(it) }
                if (kept.isNotEmpty()) onVisible(kept)
            }
        }
}

/** Reports posts that scrolled into view in a lazy column. */
@Composable
fun TrackPostImpressions(
    listState: LazyListState,
    postIdForKey: (Any) -> String?,
    onVisible: (List<String>) -> Unit
) {
    val latest = rememberUpdatedState(onVisible)
    val mapKey = rememberUpdatedState(postIdForKey)
    val visibleSnapshot = androidx.compose.runtime.remember(listState) {
        androidx.compose.runtime.derivedStateOf {
            val first = listState.firstVisibleItemIndex
            val count = listState.layoutInfo.visibleItemsInfo.size
            first to count
        }
    }
    LaunchedEffect(listState) {
        collectImpressions(
            visibleIds = {
                visibleSnapshot.value
                listState.layoutInfo.visibleItemsInfo.mapNotNull { info -> info.key.let(mapKey.value) }
            },
            onVisible = { latest.value(it) }
        )
    }
}

/** Reports library resource cards that scrolled into view in a grid. */
@Composable
fun TrackGridImpressions(
    gridState: LazyGridState,
    idForKey: (Any) -> String?,
    onVisible: (List<String>) -> Unit
) {
    val latest = rememberUpdatedState(onVisible)
    val mapKey = rememberUpdatedState(idForKey)
    val visibleSnapshot = androidx.compose.runtime.remember(gridState) {
        androidx.compose.runtime.derivedStateOf {
            val first = gridState.firstVisibleItemIndex
            val count = gridState.layoutInfo.visibleItemsInfo.size
            first to count
        }
    }
    LaunchedEffect(gridState) {
        collectImpressions(
            visibleIds = {
                visibleSnapshot.value
                gridState.layoutInfo.visibleItemsInfo.mapNotNull { info -> info.key.let(mapKey.value) }
            },
            onVisible = { latest.value(it) }
        )
    }
}
