package com.neb.ians.data.news

import com.neb.ians.data.api.ApiBadgeInfo
import com.neb.ians.data.api.ApiReply
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class NewsComment(
    val id: String,
    @SerialName("author_name") val authorNameSnake: String? = null,
    @SerialName("authorName") val authorNameCamel: String? = null,
    @SerialName("author_initials") val authorInitials: String = "N",
    @SerialName("author_photo") val authorPhotoSnake: String? = null,
    @SerialName("authorPhotoUrl") val authorPhotoCamel: String? = null,
    @SerialName("authorId") val authorId: String = "",
    @SerialName("text") val textLegacy: String? = null,
    @SerialName("content") val content: String? = null,
    @SerialName("parentCommentId") val parentCommentId: String = "",
    @SerialName("thumbsUpCount") val thumbsUpCount: Int = 0,
    @SerialName("childCount") val childCount: Int = 0,
    @SerialName("isThumbedUp") val isThumbedUp: Boolean = false,
    @SerialName("isBookmarked") val isBookmarked: Boolean = false,
    @SerialName("isOwner") val isOwner: Boolean = false,
    @SerialName("isEdited") val isEdited: Boolean = false,
    @SerialName("authorBadgeInfo") val authorBadgeInfo: ApiBadgeInfo? = null,
    @SerialName("created_at") val createdAtSnake: Long? = null,
    @SerialName("createdAt") val createdAtCamel: Long? = null
) {
    val authorName: String get() = authorNameCamel ?: authorNameSnake.orEmpty().ifBlank { "NEBian" }
    val authorPhoto: String get() = authorPhotoCamel ?: authorPhotoSnake.orEmpty()
    val text: String get() = content ?: textLegacy.orEmpty()
    val createdAt: Long get() = createdAtCamel ?: createdAtSnake ?: 0

    /** One shared comment shape for the standard CommentCard/thread UI. */
    fun toApiReply(): ApiReply = ApiReply(
        id = id,
        postId = "",
        authorId = authorId,
        authorName = authorName,
        authorPhotoUrl = authorPhoto,
        authorBadgeInfo = authorBadgeInfo,
        content = text,
        thumbsUpCount = thumbsUpCount,
        replyCount = childCount,
        isThumbedUp = isThumbedUp,
        isBookmarked = isBookmarked,
        isEdited = isEdited,
        createdAt = createdAt,
        parentReplyId = parentCommentId.ifBlank { null }
    )
}

@Serializable
data class NewsCommentsResponse(
    val ok: Boolean = false,
    val comments: List<NewsComment> = emptyList(),
    val error: String? = null
)

@Serializable
data class NewsCommentRequest(
    val slug: String,
    val text: String,
    @SerialName("parentCommentId") val parentCommentId: String? = null
)

@Serializable
data class NewsCommentResponse(
    val ok: Boolean = false,
    val comment: NewsComment? = null,
    val error: String? = null
)

@Serializable
data class NewsCommentLikeResponse(
    @SerialName("likeCount") val likeCount: Int = 0,
    @SerialName("like_count") val likeCountSnake: Int? = null,
    @SerialName("isLiked") val isLiked: Boolean = false,
    @SerialName("is_liked") val isLikedSnake: Boolean? = null,
    val error: String? = null
) {
    val resolvedLikeCount: Int get() = likeCountSnake ?: likeCount
    val resolvedIsLiked: Boolean get() = isLikedSnake ?: isLiked
}
