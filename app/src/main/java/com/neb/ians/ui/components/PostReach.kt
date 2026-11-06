package com.neb.ians.ui.components

import androidx.compose.foundation.lazy.LazyListState
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
 * Reports posts that scrolled into view. A post counts once per list session, ids are batched
 * for a couple of seconds, and the server turns them into one impression per viewer per day.
 */
@Composable
fun TrackPostImpressions(
    listState: LazyListState,
    postIdForKey: (Any) -> String?,
    onVisible: (List<String>) -> Unit
) {
    val latest = rememberUpdatedState(onVisible)
    val mapKey = rememberUpdatedState(postIdForKey)
    LaunchedEffect(listState) {
        val seen = HashSet<String>()
        snapshotFlow {
            listState.layoutInfo.visibleItemsInfo.mapNotNull { info -> info.key.let(mapKey.value) }
        }
            .distinctUntilChanged()
            .collect { visible ->
                val fresh = visible.filter { seen.add(it) }
                if (fresh.isNotEmpty()) {
                    // Let a fast fling settle: only what is still on screen after the pause counts.
                    delay(1200)
                    val stillThere = listState.layoutInfo.visibleItemsInfo
                        .mapNotNull { info -> info.key.let(mapKey.value) }
                        .toSet()
                    val kept = fresh.filter { it in stillThere }
                    (fresh - kept.toSet()).forEach { seen.remove(it) }
                    if (kept.isNotEmpty()) latest.value(kept)
                }
            }
    }
}
