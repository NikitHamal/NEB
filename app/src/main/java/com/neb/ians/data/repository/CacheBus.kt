package com.neb.ians.data.repository

import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.channels.BufferOverflow
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.debounce
import kotlinx.coroutines.flow.emitAll
import kotlinx.coroutines.flow.filter
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onEach
import javax.inject.Inject
import javax.inject.Singleton

/**
 * "Cache updated" signal bus.
 *
 * Repositories serve cache-first and revalidate in the background
 * (stale-while-revalidate). Without a signal, screens kept showing their
 * first cached snapshot until a manual refresh even though fresher data had
 * already been written to the offline cache underneath them. Repositories
 * publish the cache key they just wrote; view-models subscribe (debounced)
 * and re-pull their cache-only getters so the UI updates silently.
 */
@Singleton
class CacheBus @Inject constructor() {

    private val _signals = MutableSharedFlow<String>(
        extraBufferCapacity = 64,
        onBufferOverflow = BufferOverflow.DROP_OLDEST
    )

    /** Emits the cache key that was just refreshed from the network. */
    val signals: SharedFlow<String> = _signals.asSharedFlow()

    fun publish(key: String) {
        _signals.tryEmit(key)
    }

    /**
     * Every key refreshed since the last batch, once the signals have been quiet for [quietMs].
     * A plain debounce keeps only the last key, so a post refreshed together with its replies (or
     * the home feed's resources together with its posts) would lose one of the two updates.
     */
    @OptIn(FlowPreview::class)
    fun batches(quietMs: Long = 400): Flow<Set<String>> = flow {
        val pending = LinkedHashSet<String>()
        emitAll(
            signals
                .onEach { key -> synchronized(pending) { pending += key } }
                .debounce(quietMs)
                .map { synchronized(pending) { pending.toSet().also { pending.clear() } } }
                .filter { it.isNotEmpty() }
        )
    }

    companion object {
        const val PREFIX_POSTS_LIST = "posts|"
        const val PREFIX_POST = "post|"
        const val PREFIX_POST_REPLIES = "post-replies|"
        const val PREFIX_RESOURCES = "resources|"
        const val PREFIX_RESOURCE = "resource|"
        const val PREFIX_RESOURCE_COMMENTS = "resource-comments|"
        const val PREFIX_NEWS_LIST = "news|"
        const val PREFIX_NEWS_DETAIL = "news-detail|"
        const val PREFIX_NEWS_COMMENTS = "news-comments|"
        const val PREFIX_PROFILE = "profile|"
        const val PREFIX_HOME = "home|"
        const val PREFIX_SUGGESTED = "suggested-feed|"
    }
}
