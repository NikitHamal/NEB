package com.neb.ians.data.repository

import com.neb.ians.data.api.ApiCreatorCourse
import com.neb.ians.data.api.ApiCreatorEditorSchema
import com.neb.ians.data.api.ApiCreatorTemplatesResponse
import com.neb.ians.data.api.ApiCreatorCourseEnvelope
import com.neb.ians.data.api.ApiCreatorPage
import com.neb.ians.data.api.ApiCreatorPost
import com.neb.ians.data.api.ApiCreatorPostEnvelope
import com.neb.ians.data.api.ApiCoursePurchaseResponse
import com.neb.ians.data.api.ApiMarketplaceCourseDetail
import com.neb.ians.data.api.ApiMarketplaceCoursesResponse
import com.neb.ians.data.api.ApiMarketplaceCreatorsResponse
import com.neb.ians.data.api.ApiMarketplaceDashboard
import com.neb.ians.data.api.ApiMarketplaceStats
import com.neb.ians.data.api.ApiMessageResponse
import com.neb.ians.data.api.ApiMyCreatorCoursesResponse
import com.neb.ians.data.api.ApiMyCreatorPageResponse
import com.neb.ians.data.api.ApiMyCreatorPostsResponse
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiWithdrawal
import com.neb.ians.data.api.ApiWithdrawalsResponse
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.buildJsonArray
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.put
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import javax.inject.Inject
import javax.inject.Singleton

/**
 * The creator marketplace, from the app's side.
 *
 * Writes go out as hand-built JSON objects rather than serialised data classes:
 * the server treats "this key is present" as "change this field", so sending a
 * null for a field nobody touched would wipe it. Building the object key by key
 * makes every write say exactly what it means.
 */
@Singleton
class MarketplaceRepository @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) {
    private val json = Json { ignoreUnknownKeys = true; encodeDefaults = true }
    private val jsonMedia = "application/json".toMediaType()

    private suspend fun token(required: Boolean = false): String? {
        val bearer = authRepository.getBearerToken()
        if (required && bearer.isNullOrBlank()) throw IllegalStateException("Not authenticated")
        return bearer
    }

    private fun body(payload: JsonObject): RequestBody =
        json.encodeToString(JsonObject.serializer(), payload).toRequestBody(jsonMedia)

    // ----- Reading -----

    suspend fun creators(
        kind: String? = null,
        query: String? = null,
        sort: String? = null,
        page: Int? = null,
        pageSize: Int = 12
    ): Result<ApiMarketplaceCreatorsResponse> = runCatching {
        apiService.getMarketplaceCreators(
            bearerToken = token(),
            kind = kind?.takeIf { it.isNotBlank() },
            query = query?.takeIf { it.isNotBlank() },
            sort = sort,
            page = page,
            pageSize = pageSize
        )
    }

    suspend fun stats(): Result<ApiMarketplaceStats> = runCatching {
        apiService.getMarketplaceStats()
    }

    /** The platform's commission, so the price control quotes the real number. */
    suspend fun commissionPercent(): Result<Double> = runCatching {
        val config = apiService.getPaymentsConfig()
        config.commissionPercent.toDoubleOrNull() ?: 2.5
    }

    /** The shelf above the creator list: published offerings, best first. */
    suspend fun recentCourses(
        kind: String? = null,
        query: String? = null,
        sort: String? = "featured",
        limit: Int = 8
    ): Result<ApiMarketplaceCoursesResponse> = runCatching {
        apiService.getMarketplaceCourseShelf(
            bearerToken = token(),
            kind = kind?.takeIf { it.isNotBlank() },
            query = query?.takeIf { it.isNotBlank() },
            sort = sort,
            limit = limit
        )
    }

    suspend fun creatorPage(slug: String): Result<ApiCreatorPage> = runCatching {
        apiService.getCreatorPage(token(), slug)
    }

    suspend fun course(courseId: String): Result<ApiMarketplaceCourseDetail> = runCatching {
        apiService.getMarketplaceCourse(token(), courseId)
    }

    suspend fun dashboard(): Result<ApiMarketplaceDashboard> = runCatching {
        apiService.getMarketplaceDashboard(token(required = true)!!)
    }

    suspend fun myPage(): Result<ApiMyCreatorPageResponse> = runCatching {
        apiService.getMyCreatorPage(token(required = true)!!)
    }

    suspend fun myCourses(): Result<ApiMyCreatorCoursesResponse> = runCatching {
        apiService.getMyCreatorCourses(token(required = true)!!)
    }

    suspend fun myPosts(): Result<ApiMyCreatorPostsResponse> = runCatching {
        apiService.getMyCreatorPosts(token(required = true)!!)
    }

    suspend fun withdrawals(): Result<ApiWithdrawalsResponse> = runCatching {
        apiService.getWithdrawals(token(required = true)!!)
    }

    /** Ask for a payout. The server reserves the amount out of the wallet the
     *  moment the request lands, so the caller should refresh the dashboard. */
    suspend fun requestWithdrawal(
        amount: String,
        payoutMethod: String,
        payoutDetails: String
    ): Result<ApiWithdrawal> = runCatching {
        val payload = buildJsonObject {
            put("amount", amount)
            put("payout_method", payoutMethod)
            put("payout_details", payoutDetails)
        }
        apiService.requestWithdrawal(token(required = true)!!, body(payload))
    }

    // ----- Writing -----

    suspend fun savePage(
        displayName: String? = null,
        tagline: String? = null,
        about: String? = null,
        slug: String? = null,
        kind: String? = null,
        avatarUrl: String? = null,
        coverUrl: String? = null,
        accentHex: String? = null,
        layout: String? = null,
        style: Map<String, JsonElement>? = null,
        socials: Map<String, String>? = null,
        contactEmail: String? = null,
        contactPhone: String? = null,
        location: String? = null,
        subjects: List<String>? = null,
        languages: List<String>? = null,
        blocks: List<JsonObject>? = null,
        published: Boolean? = null,
        acceptingStudents: Boolean? = null
    ): Result<ApiMyCreatorPageResponse> = runCatching {
        val payload = buildJsonObject {
            displayName?.let { put("display_name", it) }
            tagline?.let { put("tagline", it) }
            about?.let { put("about", it) }
            slug?.let { put("slug", it) }
            kind?.let { put("kind", it) }
            avatarUrl?.let { put("avatar_url", it) }
            coverUrl?.let { put("cover_url", it) }
            accentHex?.let { put("accent_hex", it) }
            layout?.let { put("layout", it) }
            location?.let { put("location", it) }
            contactEmail?.let { put("contact_email", it) }
            contactPhone?.let { put("contact_phone", it) }
            subjects?.let { list -> put("subjects", JsonArray(list.map { JsonPrimitive(it) })) }
            languages?.let { list -> put("languages", JsonArray(list.map { JsonPrimitive(it) })) }
            socials?.let { map ->
                put("socials", JsonObject(map.filterValues { it.isNotBlank() }.mapValues { JsonPrimitive(it.value) }))
            }
            style?.let { put("style", JsonObject(it)) }
            blocks?.let { list -> put("blocks", JsonArray(list)) }
            published?.let { put("published", it) }
            acceptingStudents?.let { put("accepting_students", it) }
        }
        apiService.updateMyCreatorPage(token(required = true)!!, body(payload))
    }

    /** The section catalogue and style vocabulary. Public and cacheable -- it is
     *  a catalogue, not anybody's data -- so no token goes with it. */
    suspend fun editorSchema(): Result<ApiCreatorEditorSchema> = runCatching {
        apiService.getCreatorEditorSchema()
    }

    suspend fun templates(kind: String? = null): Result<ApiCreatorTemplatesResponse> = runCatching {
        apiService.getCreatorTemplates(kind?.takeIf { it.isNotBlank() })
    }

    /**
     * Put a ready-made page under the signed-in creator.
     *
     * `mode` decides how much it replaces: `page` takes the look and the
     * sections, `theme` repaints and keeps every word, `sections` brings the
     * sections into the colours already chosen.
     */
    suspend fun applyTemplate(templateId: String, mode: String = "theme"): Result<ApiMyCreatorPageResponse> =
        runCatching {
            val payload = buildJsonObject {
                put("template", templateId)
                put("mode", mode)
            }
            apiService.applyCreatorTemplate(token(required = true)!!, body(payload))
        }

    suspend fun saveCourse(
        id: String? = null,
        title: String,
        summary: String? = null,
        description: String? = null,
        isFree: Boolean,
        price: String? = null,
        level: String? = null,
        durationLabel: String? = null,
        lessonCount: Int? = null,
        seatLimit: Int? = null,
        includes: List<String>? = null,
        tags: String? = null,
        coverUrl: String? = null,
        status: String? = null,
        featured: Boolean? = null,
        resourceIds: List<String>? = null
    ): Result<ApiCreatorCourseEnvelope> = runCatching {
        val payload = buildJsonObject {
            id?.let { put("id", it) }
            put("title", title)
            summary?.let { put("summary", it) }
            description?.let { put("description", it) }
            put("is_free", isFree)
            price?.let { put("price", it) }
            level?.let { put("level", it) }
            durationLabel?.let { put("duration_label", it) }
            lessonCount?.let { put("lesson_count", it) }
            seatLimit?.let { put("seat_limit", it) }
            includes?.let { list -> put("includes", JsonArray(list.map { JsonPrimitive(it) })) }
            tags?.let { put("tags", it) }
            coverUrl?.let { put("cover_url", it) }
            status?.let { put("status", it) }
            featured?.let { put("featured", it) }
            resourceIds?.let { list -> put("resource_ids", JsonArray(list.map { JsonPrimitive(it) })) }
        }
        val bearer = token(required = true)!!
        if (id.isNullOrBlank()) {
            apiService.createCreatorCourse(bearer, body(payload))
        } else {
            apiService.updateCreatorCourse(bearer, id, body(payload))
        }
    }

    suspend fun deleteCourse(courseId: String): Result<ApiMessageResponse> = runCatching {
        apiService.deleteCreatorCourse(token(required = true)!!, courseId)
    }

    suspend fun savePost(
        id: String? = null,
        title: String? = null,
        body: String? = null,
        mediaUrl: String? = null,
        linkUrl: String? = null,
        pinned: Boolean? = null,
        published: Boolean? = null
    ): Result<ApiCreatorPostEnvelope> = runCatching {
        val payload = buildJsonObject {
            id?.let { put("id", it) }
            title?.let { put("title", it) }
            body?.let { put("body", it) }
            mediaUrl?.let { put("media_url", it) }
            linkUrl?.let { put("link_url", it) }
            pinned?.let { put("pinned", it) }
            published?.let { put("published", it) }
        }
        val bearer = token(required = true)!!
        if (id.isNullOrBlank()) {
            apiService.createCreatorPost(bearer, body(payload))
        } else {
            apiService.updateCreatorPost(bearer, id, body(payload))
        }
    }

    suspend fun deletePost(postId: String): Result<ApiMessageResponse> = runCatching {
        apiService.deleteCreatorPost(token(required = true)!!, postId)
    }

    // ----- Buying -----

    suspend fun purchaseStatus(courseId: String): Result<ApiCoursePurchaseResponse> = runCatching {
        apiService.getCoursePurchaseStatus(token(required = true)!!, courseId)
    }

    suspend fun submitPurchase(
        courseId: String,
        transactionId: String,
        proofFile: java.io.File?
    ): Result<ApiCoursePurchaseResponse> = runCatching {
        val bearer = token(required = true)!!
        val txn = transactionId.takeIf { it.isNotBlank() }
            ?.toRequestBody("text/plain".toMediaTypeOrNull())
        val proof = proofFile?.let { file ->
            MultipartBody.Part.createFormData(
                "payment_proof",
                file.name,
                file.asRequestBody(guessImageMime(file.name))
            )
        }
        val response = apiService.submitCoursePurchase(bearer, courseId, txn, proof)
        if (response.error != null) throw IllegalStateException(response.error)
        response
    }

    /** Blend the saved page with a fresh set of blocks, ready to send back. */
    fun blocksPayload(page: ApiCreatorPage): List<JsonObject> = page.blocks.map { block ->
        buildJsonObject {
            put("id", block.id)
            put("type", block.type)
            put("enabled", block.enabled)
            put("title", block.title)
            put("subtitle", block.subtitle)
            put("body", block.body)
            put("cta_label", block.ctaLabel)
            put("cta_url", block.ctaUrl)
            put("image_url", block.imageUrl)
            put("media_url", block.mediaUrl)
            // Only sent when the creator moved one of them off its default.
            // `sanitize_block_settings` drops defaults anyway, so an untouched
            // page stays exactly as small on the wire as it was before these
            // existed.
            val settings = block.settings
            if (settings.align != "start" || settings.tone != "plain" ||
                settings.width != "standard" || settings.columns in 1..4
            ) {
                put("settings", buildJsonObject {
                    put("align", settings.align)
                    put("tone", settings.tone)
                    put("width", settings.width)
                    if (settings.columns in 1..4) put("columns", settings.columns)
                })
            }
            if (block.items.isNotEmpty()) {
                put("items", JsonArray(block.items.map { item ->
                    buildJsonObject {
                        if (item.label.isNotEmpty()) put("label", item.label)
                        if (item.value.isNotEmpty()) put("value", item.value)
                        if (item.icon.isNotEmpty()) put("icon", item.icon)
                        if (item.title.isNotEmpty()) put("title", item.title)
                        if (item.subtitle.isNotEmpty()) put("subtitle", item.subtitle)
                        if (item.imageUrl.isNotEmpty()) put("image_url", item.imageUrl)
                        if (item.linkUrl.isNotEmpty()) put("link_url", item.linkUrl)
                        if (item.badge.isNotEmpty()) put("badge", item.badge)
                        if (item.name.isNotEmpty()) put("name", item.name)
                        if (item.role.isNotEmpty()) put("role", item.role)
                        if (item.quote.isNotEmpty()) put("quote", item.quote)
                        if (item.avatarUrl.isNotEmpty()) put("avatar_url", item.avatarUrl)
                        if (item.q.isNotEmpty()) put("q", item.q)
                        if (item.a.isNotEmpty()) put("a", item.a)
                        if (item.day.isNotEmpty()) put("day", item.day)
                        if (item.time.isNotEmpty()) put("time", item.time)
                        if (item.note.isNotEmpty()) put("note", item.note)
                        if (item.url.isNotEmpty()) put("url", item.url)
                        if (item.price.isNotEmpty()) put("price", item.price)
                        if (item.period.isNotEmpty()) put("period", item.period)
                        if (item.features.isNotEmpty()) put("features", item.features)
                        if (item.ctaLabel.isNotEmpty()) put("cta_label", item.ctaLabel)
                        if (item.ctaUrl.isNotEmpty()) put("cta_url", item.ctaUrl)
                    }
                }))
            }
            if (block.images.isNotEmpty()) {
                put("images", JsonArray(block.images.map { JsonPrimitive(it) }))
            }
        }
    }

    private fun guessImageMime(name: String): okhttp3.MediaType? {
        return when (name.substringAfterLast('.', "").lowercase()) {
            "png" -> "image/png".toMediaTypeOrNull()
            "webp" -> "image/webp".toMediaTypeOrNull()
            "gif" -> "image/gif".toMediaTypeOrNull()
            "heic" -> "image/heic".toMediaTypeOrNull()
            else -> "image/jpeg".toMediaTypeOrNull()
        }
    }
}
