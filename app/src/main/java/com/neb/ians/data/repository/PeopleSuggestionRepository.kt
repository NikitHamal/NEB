package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiService
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.Semaphore
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.sync.withPermit
import kotlin.random.Random
import javax.inject.Inject
import javax.inject.Singleton

data class PersonSuggestion(
    val id: String,
    val username: String,
    val name: String,
    val photoUrl: String?,
    val detail: String?,
    val reason: String,
    val followsYou: Boolean,
    val mutualCount: Int,
    val isFollowing: Boolean = false
)

/**
 * Who to suggest the user follows, from every signal the server exposes.
 *
 * The old suggestion list was the authors of recent forum posts, which is why
 * it handed everyone the same five names — the most active posters are the
 * same for every account — and why it emptied out once people already
 * followed were correctly excluded. There is no suggestions endpoint, so this
 * assembles one: people who follow the user back, people followed by people
 * the user follows, people at the same school or in the same class, and only
 * then the forum's recent authors.
 *
 * The shortlist is resolved through the popup and stats endpoints because
 * neither the follow list nor user search says whether an account is locked
 * or private, and both must be kept out of suggestions.
 */
@Singleton
class PeopleSuggestionRepository @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository,
    private val forumRepository: ForumRepository,
    private val followStateRepository: FollowStateRepository
) {

    private val _suggestions = MutableStateFlow<List<PersonSuggestion>>(emptyList())
    val suggestions: StateFlow<List<PersonSuggestion>> = _suggestions.asStateFlow()

    private val mutex = Mutex()
    private var lastLoadedAt = 0L
    private var loadedForUserId: String? = null

    suspend fun load(forceRefresh: Boolean = false): Result<List<PersonSuggestion>> = mutex.withLock {
        val selfId = authRepository.currentUserIdFlow.first()?.takeIf { it.isNotBlank() }
        if (selfId != loadedForUserId) {
            loadedForUserId = selfId
            lastLoadedAt = 0L
            _suggestions.value = emptyList()
        }
        if (selfId == null) return Result.success(emptyList())

        val now = System.currentTimeMillis()
        val cached = _suggestions.value
        if (!forceRefresh && cached.isNotEmpty() && now - lastLoadedAt < TTL_MS) {
            return Result.success(cached)
        }

        followStateRepository.sync(forceRefresh)
        val token = authRepository.getBearerToken() ?: return Result.success(emptyList())
        val profile = runCatching { authRepository.userProfileFlow.first() }.getOrNull()
        val graph = followStateRepository.graph.value

        return runCatching {
            val seeds = gather(token, selfId, profile, graph)
            val shortlist = seeds.values
                .filter { it.handle.isNotBlank() && !graph.contains(it.id, it.handle) }
                .sortedByDescending { it.score }
                .take(SHORTLIST)
            val resolved = resolve(token, shortlist).take(MAX_VISIBLE)
            lastLoadedAt = now
            _suggestions.value = resolved
            resolved
        }
    }

    fun record(userId: String?, handle: String?, following: Boolean) {
        val id = userId?.trim().orEmpty()
        val name = handle?.trim()?.lowercase().orEmpty()
        _suggestions.update { current ->
            current.map { person ->
                val match = (id.isNotEmpty() && person.id == id) ||
                    (name.isNotEmpty() && person.username.lowercase() == name)
                if (match) person.copy(isFollowing = following) else person
            }
        }
    }

    private suspend fun gather(
        token: String,
        selfId: String,
        profile: UserProfileCache?,
        graph: FollowStateRepository.Graph
    ): Map<String, Seed> = coroutineScope {
        val followersTask = async {
            runCatching { apiService.getFollowers(token, selfId).results }.getOrDefault(emptyList())
        }
        val mutualsTask = async { mutualCounts(token, graph) }
        val schoolTask = async { peerSearch(token, profile?.school) }
        val classTask = async { peerSearch(token, profile?.classLevel) }
        val feedTask = async { feedAuthors() }

        val seeds = LinkedHashMap<String, Seed>()
        fun seed(handle: String?): Seed? {
            val key = handle?.trim()?.lowercase()?.removePrefix("@")?.takeIf { it.isNotEmpty() } ?: return null
            if (key == profile?.username?.lowercase()) return null
            return seeds.getOrPut(key) { Seed(handle = key) }
        }

        followersTask.await().forEach { item ->
            seed(item.followerUsername)?.apply {
                followsYou = true
                name = name ?: item.followerDisplayName
                photoUrl = photoUrl ?: item.followerPhotoUrl
            }
        }
        mutualsTask.await().forEach { (handle, count) ->
            seed(handle)?.apply { mutualCount = maxOf(mutualCount, count) }
        }
        schoolTask.await().forEach { result ->
            if (result.isSelf == true || result.isFollowing == true) return@forEach
            seed(result.username)?.apply {
                id = id ?: result.id.takeIf { it.isNotBlank() }
                name = name ?: result.displayName
                photoUrl = photoUrl ?: result.photoUrl
                followerCount = maxOf(followerCount, result.followerCount)
                sameSchool = true
            }
        }
        classTask.await().forEach { result ->
            if (result.isSelf == true || result.isFollowing == true) return@forEach
            seed(result.username)?.apply {
                id = id ?: result.id.takeIf { it.isNotBlank() }
                name = name ?: result.displayName
                photoUrl = photoUrl ?: result.photoUrl
                followerCount = maxOf(followerCount, result.followerCount)
                sameClass = true
            }
        }
        feedTask.await().forEach { author ->
            seed(author.handle)?.apply {
                id = id ?: author.id
                name = name ?: author.name
                photoUrl = photoUrl ?: author.photoUrl
                feedActive = true
            }
        }
        seeds
    }

    private suspend fun mutualCounts(
        token: String,
        graph: FollowStateRepository.Graph
    ): Map<String, Int> = coroutineScope {
        if (graph.handles.isEmpty()) return@coroutineScope emptyMap()
        val seedHandles = graph.handles
            .shuffled(Random(System.currentTimeMillis() / DAY_MS))
            .take(MUTUAL_SEEDS)
        seedHandles
            .map { handle ->
                async {
                    val popup = runCatching { apiService.getUserPopup(token, handle) }.getOrNull()
                    val id = popup?.id?.takeIf { it.isNotBlank() } ?: return@async emptyList<String>()
                    runCatching { apiService.getFollowing(token, id).results }
                        .getOrDefault(emptyList())
                        .mapNotNull { it.followingUsername?.trim()?.lowercase()?.takeIf(String::isNotEmpty) }
                }
            }
            .awaitAll()
            .flatten()
            .groupingBy { it }
            .eachCount()
    }

    private suspend fun peerSearch(token: String, term: String?): List<com.neb.ians.data.api.ApiUserSearchResult> {
        val query = term?.trim()?.takeIf { it.length >= 3 } ?: return emptyList()
        return runCatching { apiService.searchUsers(token, query) }.getOrDefault(emptyList())
    }

    private suspend fun feedAuthors(): List<FeedAuthor> {
        val authors = LinkedHashMap<String, FeedAuthor>()
        for (page in 1..FEED_PAGES) {
            val result = forumRepository.getPosts(page = page).getOrNull() ?: break
            result.posts.forEach { post ->
                if (post.isAnonymous || post.authorIsBot || post.authorName.isBlank()) return@forEach
                val key = post.authorName.lowercase()
                authors.putIfAbsent(
                    key,
                    FeedAuthor(
                        handle = post.authorName,
                        id = post.authorId.takeIf { it.isNotBlank() },
                        name = post.authorName,
                        photoUrl = post.authorPhotoUrl
                    )
                )
            }
            if (!result.hasMore) break
        }
        return authors.values.toList()
    }

    private suspend fun resolve(token: String, shortlist: List<Seed>): List<PersonSuggestion> =
        coroutineScope {
            val gate = Semaphore(CONCURRENCY)
            shortlist
                .map { seed ->
                    async {
                        val popup = gate.withPermit {
                            runCatching { apiService.getUserPopup(token, seed.handle) }.getOrNull()
                        } ?: return@async null
                        if (popup.isSelf || popup.isLocked || popup.isFollowing) return@async null
                        val id = popup.id.takeIf { it.isNotBlank() } ?: seed.id ?: return@async null
                        val stats = gate.withPermit {
                            runCatching { apiService.getProfileStats(token, seed.handle) }.getOrNull()
                        }
                        if (stats?.isPrivate == true || stats?.isFollowing == true || stats?.isRequested == true) {
                            return@async null
                        }
                        PersonSuggestion(
                            id = id,
                            username = popup.username.ifBlank { seed.handle },
                            name = popup.displayName.ifBlank { seed.name ?: seed.handle },
                            photoUrl = popup.photoUrl.ifBlank { null } ?: seed.photoUrl,
                            detail = popup.classLevel.ifBlank { null }
                                ?: popup.badgeInfo?.label?.takeIf { it.isNotBlank() },
                            reason = seed.reason(),
                            followsYou = seed.followsYou,
                            mutualCount = seed.mutualCount
                        )
                    }
                }
                .awaitAll()
                .filterNotNull()
        }

    private data class FeedAuthor(
        val handle: String,
        val id: String?,
        val name: String,
        val photoUrl: String?
    )

    private data class Seed(
        val handle: String,
        var id: String? = null,
        var name: String? = null,
        var photoUrl: String? = null,
        var followsYou: Boolean = false,
        var mutualCount: Int = 0,
        var sameSchool: Boolean = false,
        var sameClass: Boolean = false,
        var feedActive: Boolean = false,
        var followerCount: Int = 0
    ) {
        val score: Int
            get() = (if (followsYou) 120 else 0) +
                minOf(mutualCount, 4) * 28 +
                (if (sameSchool) 34 else 0) +
                (if (sameClass) 16 else 0) +
                (if (feedActive) 12 else 0) +
                minOf(followerCount, 60) / 5

        fun reason(): String = when {
            followsYou -> "Follows you"
            mutualCount == 1 -> "1 mutual connection"
            mutualCount > 1 -> "$mutualCount mutual connections"
            sameSchool -> "From your school"
            sameClass -> "In your class"
            else -> "Active in the forum"
        }
    }

    private companion object {
        const val TTL_MS = 10 * 60 * 1000L
        const val DAY_MS = 24 * 60 * 60 * 1000L
        const val MUTUAL_SEEDS = 4
        const val FEED_PAGES = 3
        const val SHORTLIST = 14
        const val MAX_VISIBLE = 12
        const val CONCURRENCY = 6
    }
}
