package com.neb.ians.data.api

import android.content.Context
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.kotlinx.serialization.asConverterFactory
import retrofit2.http.*
import com.neb.ians.BuildConfig
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.ResponseBody

// -------------------------------------------------------------
// REQUEST MODELS
// -------------------------------------------------------------

@Serializable
data class GoogleAuthRequest(val idToken: String)

@Serializable
data class GitHubAuthRequest(
    val code: String,
    @SerialName("redirectUri") val redirectUri: String
)

@Serializable
data class EmailSignupRequest(
    val email: String,
    val password: String,
    val username: String,
    val role: String = "student"
)

@Serializable
data class EmailLoginRequest(
    val email: String,
    val password: String
)

@Serializable
data class SetPasswordRequest(val password: String)

@Serializable
data class ChangePasswordRequest(
    @SerialName("current_password") val currentPassword: String,
    @SerialName("new_password") val newPassword: String
)

@Serializable
data class EmailVerifyRequest(
    val email: String,
    val code: String
)

@Serializable
data class EmailResendRequest(val email: String)

@Serializable
data class EmailForgotRequest(val email: String)

@Serializable
data class EmailResetPasswordRequest(
    val email: String,
    val code: String,
    @SerialName("new_password") val newPassword: String
)

@Serializable
data class UserProfileRequest(
    val username: String,
    val email: String? = null,
    @SerialName("photo_url") val photoUrl: String? = null,
    @SerialName("display_name") val displayName: String? = null,
    val role: String? = null,
    @SerialName("teaching_subjects") val teachingSubjects: String? = null,
    @SerialName("institution_type") val institutionType: String? = null,
    val dob: String? = null,
    val gender: String? = null,
    @SerialName("class_level") val classLevel: String? = null,
    val subjects: String? = null,
    val pradesh: String? = null,
    val district: String? = null,
    val school: String? = null,
    @SerialName("is_locked") val isLocked: Boolean? = null,
    @SerialName("banner_url") val bannerUrl: String? = null,
    val bio: String? = null
)

@Serializable
data class PostCreateRequest(
    val title: String,
    val content: String,
    val category: String,
    @SerialName("image_urls") val imageUrls: List<String> = emptyList(),
    val poll: ApiPollCreate? = null
)

@Serializable
data class ApiPollCreate(
    val question: String = "",
    @SerialName("poll_type") val pollType: String = "voting",
    @SerialName("allow_multiple") val allowMultiple: Boolean = false,
    val explanation: String = "",
    @SerialName("duration_ms") val durationMs: Long = 0,
    val options: List<ApiPollOptionCreate> = emptyList()
)

@Serializable
data class ApiPollOptionCreate(
    val text: String,
    @SerialName("is_correct") val isCorrect: Boolean = false,
    val index: Int = 0
)

/** Web AJAX create-post request — supports full poll builder (MCQ, explanation, multi-select). */
@Serializable
data class WebPostCreateRequest(
    val title: String,
    val content: String,
    val category: String,
    val images: List<String> = emptyList(),
    val poll: ApiPollCreate? = null
)

@Serializable
data class PollVoteRequest(
    @SerialName("option_id") val optionId: String? = null,
    @SerialName("option_ids") val optionIds: List<String>? = null
)

@Serializable
data class ApiPollVoteResponse(
    val id: String = "",
    val question: String = "",
    @SerialName("pollType") val pollType: String = "voting",
    @SerialName("allowMultiple") val allowMultiple: Boolean = false,
    val explanation: String = "",
    @SerialName("total_votes") val totalVotes: Int = 0,
    @SerialName("isExpired") val isExpired: Boolean = false,
    val options: List<ApiPollVoteOption> = emptyList(),
    val error: String? = null
)

@Serializable
data class ApiPollVoteOption(
    val id: String,
    val text: String = "",
    @SerialName("is_correct") val isCorrect: Boolean = false,
    @SerialName("vote_count") val voteCount: Int = 0,
    val order: Int = 0
)

@Serializable
data class UploadImageResponse(
    val url: String = "",
    val error: String? = null
)

@Serializable
data class PostUpdateRequest(
    val title: String? = null,
    val content: String? = null,
    val category: String? = null,
    @SerialName("image_urls") val imageUrls: List<String>? = null
)

@Serializable
data class ReplyCreateRequest(
    val content: String,
    @SerialName("parentReplyId") val parentReplyId: String? = null
)

@Serializable
data class ReplyUpdateRequest(val content: String)

@Serializable
data class FollowToggleRequest(
    @SerialName("user_id") val userId: String
)

@Serializable
data class BookmarkToggleRequest(
    @SerialName("target_type") val targetType: String,
    @SerialName("target_id") val targetId: String
)

@Serializable
data class ReportRequest(
    @SerialName("target_type") val targetType: String,
    @SerialName("target_id") val targetId: String,
    val reason: String,
    val description: String? = null,
    @SerialName("context_path") val contextPath: String? = null,
    val platform: String = "android"
)

@Serializable
data class FcmTokenRequest(val token: String)

@Serializable
data class ResultCheckRequest(
    val exam: String,
    val symbol: String,
    val dob: String = "",
    val batch: String = "2083"
)

@Serializable
data class ResultCheckResponse(
    val success: Boolean = false,
    val error: String? = null,
    val cached: Boolean = false,
    val data: ResultPayload? = null
)

@Serializable
data class ResultPayload(
    @SerialName("student_name") val studentName: String = "",
    val exam: String = "",
    val batch: String = "",
    val symbol: String = "",
    val school: String = "",
    val gpa: String = "",
    val grade: String = "",
    @SerialName("registration_no") val registrationNo: String = "",
    val dob: String = "",
    val source: String = "",
    val subjects: List<ResultSubject> = emptyList()
)

@Serializable
data class ResultSubject(
    val code: String = "",
    val name: String = "",
    @SerialName("credit_hour") val creditHour: String = "",
    val grade: String = "",
    @SerialName("grade_point") val gradePoint: String = ""
)

// -------------------------------------------------------------
// RESPONSE MODELS
// -------------------------------------------------------------

@Serializable
data class GenericMessageResponse(
    val status: String = "",
    val message: String = "",
    val error: String? = null
)

@Serializable
data class ChangePasswordResponse(
    val status: String = "",
    val message: String = "",
    @SerialName("authToken") val authToken: String? = null,
    val user: UserProfileResponse? = null,
    val error: String? = null
)

@Serializable
data class GoogleAuthResponse(
    val status: String,
    @SerialName("isNewUser") val isNewUser: Boolean = false,
    @SerialName("authToken") val authToken: String? = null,
    val user: UserProfileResponse
)

@Serializable
data class EmailSignupResponse(
    val status: String = "",
    val message: String = "",
    @SerialName("user_id") val userId: String = "",
    val email: String = ""
)

@Serializable
data class UsernameCheckResponse(val available: Boolean)

@Serializable
data class UserProfileResponse(
    val id: String,
    val username: String = "",
    val email: String? = null,
    @SerialName("photo_url") val photoUrl: String? = null,
    @SerialName("banner_url") val bannerUrl: String? = null,
    @SerialName("display_name") val displayName: String? = null,
    val role: String? = null,
    @SerialName("teaching_subjects") val teachingSubjects: String? = null,
    @SerialName("institution_type") val institutionType: String? = null,
    val dob: String = "",
    val gender: String? = null,
    @SerialName("class") val classLevel: String? = null,
    val subjects: String? = null,
    val pradesh: String? = null,
    val district: String? = null,
    val school: String? = null,
    val bio: String? = null,
    @SerialName("is_locked") val isLocked: Int = 0,
    @SerialName("created_at") val createdAt: Long = 0,
    @SerialName("is_private") val isPrivate: Boolean = false,
    @SerialName("email_verified") val emailVerified: Boolean = false,
    @SerialName("hasPassword") val hasPassword: Boolean = false,
    @SerialName("verification_level") val verificationLevel: Int = 0,
    @SerialName("moderator_level") val moderatorLevel: Int = 0,
    @SerialName("is_admin") val isAdmin: Boolean = false,
    @SerialName("is_bot") val isBot: Boolean = false,
    @SerialName("post_count") val postCount: Int = 0,
    @SerialName("reply_count") val replyCount: Int = 0,
    @SerialName("follower_count") val followerCount: Int = 0,
    @SerialName("following_count") val followingCount: Int = 0,
    @SerialName("likes_given_count") val likesGivenCount: Int = 0,
    @SerialName("likes_received_count") val likesReceivedCount: Int = 0,
    @SerialName("contribution_score") val contributionScore: Int = 0,
    @SerialName("is_following") val isFollowing: Boolean? = null,
    @SerialName("is_requested") val isRequested: Boolean? = null,
    @SerialName("is_self") val isSelf: Boolean? = null,
    @SerialName("achievement_badges") val achievementBadges: String? = null
)

@Serializable
data class UserPhotoResponse(
    val id: Int,
    val url: String,
    @SerialName("uploaded_at") val uploadedAt: Long,
    @SerialName("is_current") val isCurrent: Boolean
)

@Serializable
data class ApiResource(
    val id: String,
    val title: String,
    val description: String = "",
    val subject: String,
    @SerialName("grade_level") val gradeLevel: String,
    val type: String,
    @SerialName("file_url") val fileUrl: String = "",
    @SerialName("thumbnail_url") val thumbnailUrl: String = "",
    @SerialName("file_size") val fileSize: Long = 0,
    @SerialName("added_at") val addedAt: Long = 0,
    @SerialName("view_count") val viewCount: Int = 0,
    @SerialName("like_count") val likeCount: Int = 0,
    @SerialName("comment_count") val commentCount: Int = 0,
    @SerialName("author_name") val authorName: String? = null,
    @SerialName("source_type") val sourceType: String? = null,
    @SerialName("source_url") val sourceUrl: String? = null,
    @SerialName("source_label") val sourceLabel: String? = null,
    @SerialName("uploaded_by_username") val uploadedByUsernameSnake: String? = null,
    @SerialName("uploadedByUsername") val uploadedByUsernameCamel: String? = null,
    @SerialName("author_username") val authorUsernameSnake: String? = null,
    @SerialName("authorUsername") val authorUsernameCamel: String? = null,
    @SerialName("is_liked") val isLiked: Boolean? = null,
    @SerialName("is_bookmarked") val isBookmarked: Boolean? = null
) {
    val uploadedByUsername: String get() = uploadedByUsernameSnake ?: uploadedByUsernameCamel ?: authorUsernameSnake ?: authorUsernameCamel ?: ""
}

@Serializable
data class ApiPost(
    val id: String,
    val title: String,
    val content: String,
    @SerialName("authorName") val authorName: String,
    @SerialName("authorId") val authorId: String,
    @SerialName("authorPhotoUrl") val authorPhotoUrl: String? = null,
    @SerialName("authorBadge") val authorBadge: String? = null,
    @SerialName("authorBadgeInfo") val authorBadgeInfo: ApiBadgeInfo? = null,
    @SerialName("authorIsBot") val authorIsBot: Boolean = false,
    val category: String,
    @SerialName("thumbsUpCount") val thumbsUpCount: Int,
    @SerialName("replyCount") val replyCount: Int,
    @SerialName("viewCount") val viewCount: Int = 0,
    @SerialName("isThumbedUp") val isThumbedUp: Boolean,
    @SerialName("isBookmarked") val isBookmarked: Boolean? = null,
    @SerialName("isFollowingAuthor") val isFollowingAuthor: Boolean? = null,
    @SerialName("isEdited") val isEdited: Boolean? = null,
    @SerialName("isArchived") val isArchived: Boolean? = null,
    @SerialName("createdAt") val createdAt: Long,
    @SerialName("updatedAt") val updatedAt: Long? = null,
    val images: List<ApiPostImage> = emptyList(),
    val poll: ApiPoll? = null
)

@Serializable
data class ApiPoll(
    val id: String,
    val question: String = "",
    @SerialName("pollType") val pollType: String = "voting",
    @SerialName("allowMultiple") val allowMultiple: Boolean = false,
    val explanation: String = "",
    @SerialName("durationMs") val durationMs: Long = 0,
    @SerialName("totalVotes") val totalVotes: Int = 0,
    @SerialName("createdAt") val createdAt: Long = 0,
    @SerialName("isExpired") val isExpired: Boolean = false,
    @SerialName("userVote") val userVote: kotlinx.serialization.json.JsonElement? = null,
    val options: List<ApiPollOption> = emptyList()
) {
    /** Option ids the current user voted for (handles both single-id string and list shapes). */
    val userVoteIds: List<String>
        get() {
            val el = userVote ?: return emptyList()
            return try {
                when (el) {
                    is kotlinx.serialization.json.JsonArray ->
                        el.mapNotNull { (it as? kotlinx.serialization.json.JsonPrimitive)?.content }
                    is kotlinx.serialization.json.JsonPrimitive ->
                        if (el.content.isBlank() || el.content == "null") emptyList() else listOf(el.content)
                    else -> emptyList()
                }
            } catch (e: Exception) {
                emptyList()
            }
        }
}

@Serializable
data class ApiPollOption(
    val id: String,
    val text: String = "",
    @SerialName("is_correct") val isCorrect: Boolean = false,
    @SerialName("isCorrect") val isCorrectCamel: Boolean? = null,
    @SerialName("vote_count") val voteCount: Int = 0,
    @SerialName("voteCount") val voteCountCamel: Int? = null,
    val order: Int = 0
) {
    val correct: Boolean get() = isCorrectCamel ?: isCorrect
    val votes: Int get() = voteCountCamel ?: voteCount
}

@Serializable
data class ApiPostImage(
    val id: String,
    @SerialName("imageUrl") val imageUrl: String,
    val order: Int = 0
)

@Serializable
data class ApiReply(
    val id: String,
    @SerialName("postId") val postId: String,
    @SerialName("postTitle") val postTitle: String = "",
    @SerialName("parentReplyId") val parentReplyId: String? = null,
    val content: String,
    @SerialName("authorName") val authorName: String,
    @SerialName("authorId") val authorId: String,
    @SerialName("authorPhotoUrl") val authorPhotoUrl: String? = null,
    @SerialName("authorBadge") val authorBadge: String? = null,
    @SerialName("authorBadgeInfo") val authorBadgeInfo: ApiBadgeInfo? = null,
    @SerialName("authorIsBot") val authorIsBot: Boolean = false,
    @SerialName("thumbsUpCount") val thumbsUpCount: Int,
    @SerialName("childCount") val replyCount: Int = 0,
    @SerialName("isThumbedUp") val isThumbedUp: Boolean,
    @SerialName("isBookmarked") val isBookmarked: Boolean? = null,
    @SerialName("isEdited") val isEdited: Boolean? = null,
    @SerialName("isArchived") val isArchived: Boolean? = null,
    @SerialName("createdAt") val createdAt: Long,
    @SerialName("editedAt") val updatedAt: Long? = null
)

@Serializable
data class LikeResponse(
    @SerialName("thumbsUpCount") val thumbsUpCount: Int,
    @SerialName("isThumbedUp") val isThumbedUp: Boolean
)

@Serializable
data class ResourceLikeResponse(
    @SerialName("like_count") val likeCountSnake: Int? = null,
    @SerialName("likeCount") val likeCountCamel: Int? = null,
    @SerialName("is_liked") val isLikedSnake: Boolean? = null,
    @SerialName("isLiked") val isLikedCamel: Boolean? = null
) {
    val likeCount: Int get() = likeCountSnake ?: likeCountCamel ?: 0
    val isLiked: Boolean get() = isLikedSnake ?: isLikedCamel ?: false
}

@Serializable
data class BookmarkResponse(
    @SerialName("isBookmarked") val isBookmarked: Boolean
)

@Serializable
data class FollowResponse(
    @SerialName("is_following") val isFollowing: Boolean,
    @SerialName("follower_count") val followerCount: Int? = null,
    @SerialName("requested") val requested: Boolean? = null
)

@Serializable
data class ApiSearchResponse(
    val resources: List<ApiResource> = emptyList(),
    val posts: List<ApiPost> = emptyList(),
    val users: List<ApiUserSearchResult> = emptyList()
)

@Serializable
data class ApiResourceUploadResponse(
    val id: String = "",
    val title: String = "",
    val error: String? = null
)

@Serializable
data class ApiSyllabusCategoriesResponse(
    val categories: List<ApiSyllabusCategory> = emptyList()
)

@Serializable
data class ApiSyllabusCategory(
    val grade: String = "",
    val subjects: List<ApiSyllabusSubject> = emptyList(),
    val order: Int = 999
)

@Serializable
data class ApiSyllabusSubject(
    val name: String = "",
    val slug: String = "",
    val url: String = ""
)



@Serializable
data class ApiSyllabusSubjectDetailResponse(
    val grade: String = "",
    val subject: String = "",
    @SerialName("grade_slug") val gradeSlug: String = "",
    @SerialName("subject_slug") val subjectSlug: String = "",
    @SerialName("grade_list") val gradeList: List<ApiSyllabusNavItem> = emptyList(),
    @SerialName("subject_list") val subjectList: List<ApiSyllabusNavItem> = emptyList(),
    val chapters: List<ApiSyllabusChapter> = emptyList(),
    @SerialName("total_count") val totalCount: Int = 0
)

@Serializable
data class ApiSyllabusNavItem(
    val name: String = "",
    val slug: String = ""
)

@Serializable
data class ApiSyllabusChapter(
    val id: String = "",
    val name: String = "",
    @SerialName("guide_sections") val guideSections: List<ApiSyllabusSection> = emptyList(),
    @SerialName("qa_sections") val qaSections: List<ApiSyllabusQaSection> = emptyList(),
    val notes: List<ApiResource> = emptyList(),
    val solutions: List<ApiResource> = emptyList(),
    val papers: List<ApiResource> = emptyList(),
    val textbooks: List<ApiResource> = emptyList(),
    val other: List<ApiResource> = emptyList(),
    val count: Int = 0
)

@Serializable
data class ApiSyllabusSection(
    val title: String = "",
    val content: String = "",
    val id: String = ""
)

@Serializable
data class ApiSyllabusQaSection(
    val title: String = "",
    val content: String = "",
    val id: String = "",
    @SerialName("parsed_items") val parsedItems: List<ApiSyllabusQaItem> = emptyList()
)

@Serializable
data class ApiSyllabusQaItem(
    val question: String = "",
    val answer: String = ""
)

@Serializable
data class ApiUserSearchResult(
    val id: String,
    val username: String,
    @SerialName("display_name") val displayName: String? = null,
    @SerialName("photo_url") val photoUrl: String? = null,
    val bio: String? = null,
    val school: String? = null,
    @SerialName("class_level") val classLevel: String? = null,
    @SerialName("follower_count") val followerCount: Int = 0,
    @SerialName("is_following") val isFollowing: Boolean? = null,
    @SerialName("is_self") val isSelf: Boolean? = null,
    @SerialName("badge_info") val badgeInfo: ApiBadgeInfo? = null
)

@Serializable
data class ApiBadgeInfo(
    val type: String,
    val label: String = "",
    val icon: String? = null,
    val color: String? = null
)

@Serializable
data class ApiFollowItem(
    val id: String,
    @SerialName("created_at") val createdAt: Long = 0,
    @SerialName("follower_username") val followerUsername: String? = null,
    @SerialName("follower_photo_url") val followerPhotoUrl: String? = null,
    @SerialName("follower_display_name") val followerDisplayName: String? = null,
    @SerialName("following_username") val followingUsername: String? = null,
    @SerialName("following_photo_url") val followingPhotoUrl: String? = null,
    @SerialName("following_display_name") val followingDisplayName: String? = null
)

@Serializable
data class ApiFollowListResponse(
    val count: Int = 0,
    val next: String? = null,
    val previous: String? = null,
    val results: List<ApiFollowItem> = emptyList()
)

@Serializable
data class ApiFollowRequestItem(
    val id: String,
    val sender: ApiFollowRequestUser,
    @SerialName("created_at") val createdAt: Long
)

@Serializable
data class ApiFollowRequestUser(
    val id: String,
    val username: String,
    @SerialName("display_name") val displayName: String,
    @SerialName("photo_url") val photoUrl: String = ""
)

/** Mini profile shown in the user popover (long-press a username/avatar). */
@Serializable
data class ApiUserPopup(
    val id: String = "",
    val username: String = "",
    @SerialName("displayName") val displayName: String = "",
    @SerialName("photoUrl") val photoUrl: String = "",
    val bio: String = "",
    @SerialName("classLevel") val classLevel: String = "",
    @SerialName("isLocked") val isLocked: Boolean = false,
    @SerialName("badgeInfo") val badgeInfo: ApiBadgeInfo? = null,
    @SerialName("postCount") val postCount: Int = 0,
    @SerialName("replyCount") val replyCount: Int = 0,
    @SerialName("followerCount") val followerCount: Int = 0,
    @SerialName("isFollowing") val isFollowing: Boolean = false,
    @SerialName("isSelf") val isSelf: Boolean = false
)

@Serializable
data class ApiProfileActivityResponse(
    val posts: List<ApiPost> = emptyList(),
    @SerialName("has_more") val hasMore: Boolean = false,
    @SerialName("total_count") val totalCount: Int = 0
)

@Serializable
data class ApiProfileRepliesResponse(
    val replies: List<ApiReply> = emptyList(),
    @SerialName("has_more") val hasMore: Boolean = false,
    @SerialName("total_count") val totalCount: Int = 0
)

@Serializable
data class ApiProfileResourcesResponse(
    val resources: List<ApiResource> = emptyList(),
    @SerialName("has_more") val hasMore: Boolean = false,
    @SerialName("total_count") val totalCount: Int = 0
)

@Serializable
data class ApiRealtimeConfig(
    @SerialName("ws_url") val wsUrl: String = "",
    @SerialName("heartbeat_interval") val heartbeatInterval: Int = 25
)

@Serializable
data class ApiNotification(
    val id: String,
    @SerialName("actorId") val actorId: String? = null,
    @SerialName("actorName") val actorName: String? = null,
    @SerialName("actorPhotoUrl") val actorPhotoUrl: String? = null,
    @SerialName("actorBadge") val actorBadge: String? = null,
    val verb: String,
    @SerialName("targetType") val targetType: String? = null,
    @SerialName("targetId") val targetId: String? = null,
    @SerialName("referenceType") val referenceType: String? = null,
    @SerialName("referenceId") val referenceId: String? = null,
    val message: String,
    @SerialName("isRead") val isRead: Boolean,
    @SerialName("createdAt") val createdAt: Long
)

@Serializable
data class ApiNotificationListResponse(
    val notifications: List<ApiNotification>,
    @SerialName("has_more") val hasMore: Boolean = false
)

@Serializable
data class ApiNotificationMarkReadRequest(
    @SerialName("mark_all") val markAll: Boolean? = null,
    @SerialName("notification_ids") val notificationIds: List<String>? = null
)

@Serializable
data class ApiNotificationMarkReadResponse(
    val status: String = "",
    val message: String = ""
)

@Serializable
data class ApiNotificationUnreadCountResponse(
    val count: Int
)

@Serializable
data class ApiEditHistory(
    val id: String,
    @SerialName("target_type") val targetType: String = "",
    @SerialName("target_id") val targetId: String = "",
    val field: String = "",
    @SerialName("old_value") val oldValue: String = "",
    @SerialName("new_value") val newValue: String = "",
    @SerialName("editedByUsername") val editedByUsername: String = "",
    @SerialName("editedByPhotoUrl") val editedByPhotoUrl: String? = null,
    @SerialName("edited_at") val editedAt: Long = 0
)

@Serializable
data class ApiResourceComment(
    val id: String,
    @SerialName("resource_id") val resourceIdSnake: String? = null,
    @SerialName("resourceId") val resourceIdCamel: String? = null,
    @SerialName("user_id") val userIdSnake: String? = null,
    @SerialName("authorId") val userIdCamel: String? = null,
    @SerialName("user_name") val userNameSnake: String? = null,
    @SerialName("authorName") val userNameCamel: String? = null,
    @SerialName("user_photo_url") val userPhotoUrlSnake: String? = null,
    @SerialName("authorPhoto") val userPhotoUrlCamel: String? = null,
    val content: String = "",
    @SerialName("like_count") val likeCountSnake: Int? = null,
    @SerialName("likeCount") val likeCountCamel: Int? = null,
    @SerialName("reply_count") val replyCountSnake: Int? = null,
    @SerialName("replyCount") val replyCountCamel: Int? = null,
    @SerialName("is_liked") val isLikedSnake: Boolean? = null,
    @SerialName("isLiked") val isLikedCamel: Boolean? = null,
    @SerialName("parent_comment_id") val parentCommentIdSnake: String? = null,
    @SerialName("parentCommentId") val parentCommentIdCamel: String? = null,
    @SerialName("is_edited") val isEditedSnake: Boolean? = null,
    @SerialName("isEdited") val isEditedCamel: Boolean? = null,
    @SerialName("created_at") val createdAtSnake: Long? = null,
    @SerialName("createdAt") val createdAtCamel: Long? = null
) {
    val resourceId: String get() = resourceIdSnake ?: resourceIdCamel ?: ""
    val userId: String get() = userIdSnake ?: userIdCamel ?: ""
    val userName: String get() = userNameSnake ?: userNameCamel ?: ""
    val userPhotoUrl: String? get() = userPhotoUrlSnake ?: userPhotoUrlCamel
    val likeCount: Int get() = likeCountSnake ?: likeCountCamel ?: 0
    val replyCount: Int get() = replyCountSnake ?: replyCountCamel ?: 0
    val isLiked: Boolean? get() = isLikedSnake ?: isLikedCamel
    val parentCommentId: String? get() = parentCommentIdSnake ?: parentCommentIdCamel
    val isEdited: Boolean? get() = isEditedSnake ?: isEditedCamel
    val createdAt: Long get() = createdAtSnake ?: createdAtCamel ?: 0L
}

@Serializable
data class ApiResourceCommentCreateRequest(
    val content: String,
    @SerialName("parent_comment_id") val parentCommentId: String? = null
)

@Serializable
data class ApiResourceCommentsResponse(
    val comments: List<ApiResourceComment> = emptyList()
)

@Serializable
data class ApiStatsResponse(
    @SerialName("total_users") val totalUsers: Int = 0,
    @SerialName("total_posts") val totalPosts: Int = 0,
    @SerialName("total_replies") val totalReplies: Int = 0,
    @SerialName("total_resources") val totalResources: Int = 0
)

@Serializable
data class ApiPaginatedResources(
    @SerialName("results") val resources: List<ApiResource> = emptyList(),
    @SerialName("count") val totalCount: Int = 0,
    val next: String? = null,
    val previous: String? = null
)

@Serializable
data class ApiPaginatedPosts(
    @SerialName("results") val posts: List<ApiPost> = emptyList(),
    @SerialName("count") val totalCount: Int = 0,
    val next: String? = null,
    val previous: String? = null
)

@Serializable
data class ApiPaginatedReplies(
    @SerialName("results") val replies: List<ApiReply> = emptyList(),
    @SerialName("count") val totalCount: Int = 0,
    val next: String? = null,
    val previous: String? = null
)

@Serializable
data class AccountDeletionSubmitRequest(
    val reason: String
)

@Serializable
data class DeletionRequestInfo(
    val id: String,
    val status: String,
    val reason: String,
    val createdAt: Long,
    val scheduledDeleteAt: Long
)

@Serializable
data class AccountDeletionRequestResponse(
    val hasPending: Boolean,
    val request: DeletionRequestInfo? = null
)

@Serializable
data class AccountDeletionSubmitResponse(
    val success: Boolean,
    val request: DeletionRequestInfo? = null,
    val error: String? = null
)

// -------------------------------------------------------------
// RETROFIT API INTERFACE
// -------------------------------------------------------------

interface ApiService {

    // --- Auth ---
    @POST("api/auth/google/")
    suspend fun authenticateGoogle(@Body request: GoogleAuthRequest): GoogleAuthResponse

    @POST("api/auth/github/")
    suspend fun authenticateGitHub(@Body request: GitHubAuthRequest): GoogleAuthResponse

    @POST("api/auth/email/signup/")
    suspend fun emailSignup(@Body request: EmailSignupRequest): EmailSignupResponse

    @POST("api/auth/email/verify/")
    suspend fun emailVerify(@Body request: EmailVerifyRequest): GoogleAuthResponse

    @POST("api/auth/email/resend/")
    suspend fun emailResendCode(@Body request: EmailResendRequest): EmailSignupResponse

    @POST("api/auth/email/login/")
    suspend fun emailLogin(@Body request: EmailLoginRequest): GoogleAuthResponse

    @POST("api/auth/email/forgot/")
    suspend fun emailForgotPassword(@Body request: EmailForgotRequest): EmailSignupResponse

    @POST("api/auth/email/reset-password/")
    suspend fun emailResetPassword(@Body request: EmailResetPasswordRequest): GoogleAuthResponse

    @POST("api/auth/set-password/")
    suspend fun setPassword(
        @Header("Authorization") bearerToken: String,
        @Body request: SetPasswordRequest
    ): GenericMessageResponse

    @POST("api/auth/change-password/")
    suspend fun changePassword(
        @Header("Authorization") bearerToken: String,
        @Body request: ChangePasswordRequest
    ): ChangePasswordResponse

    // --- Users ---
    @GET("api/users/check-username/")
    suspend fun checkUsername(@Query("username") username: String): UsernameCheckResponse

    @POST("api/users/profile/")
    suspend fun updateProfile(
        @Header("Authorization") bearerToken: String,
        @Body request: UserProfileRequest
    ): GoogleAuthResponse

    @GET("api/users/profile/{username}/")
    suspend fun getProfile(
        @Header("Authorization") bearerToken: String?,
        @Path("username") username: String
    ): UserProfileResponse

    @Multipart
    @POST("api/users/me/photos/")
    suspend fun uploadProfilePhoto(
        @Header("Authorization") bearerToken: String,
        @Part file: okhttp3.MultipartBody.Part
    ): UserPhotoResponse

    @GET("api/users/profile/{username}/stats/")
    suspend fun getProfileStats(
        @Header("Authorization") bearerToken: String?,
        @Path("username") username: String
    ): ApiProfileStats

    @GET("api/users/me/analytics/")
    suspend fun getPrivateAnalytics(
        @Header("Authorization") bearerToken: String
    ): ApiPrivateAnalyticsResponse

    @POST("api/users/{userId}/follow/")
    suspend fun toggleFollow(
        @Header("Authorization") bearerToken: String,
        @Path("userId") userId: String
    ): FollowResponse

    @GET("api/users/{userId}/followers/")
    suspend fun getFollowers(
        @Header("Authorization") bearerToken: String?,
        @Path("userId") userId: String
    ): ApiFollowListResponse

    @GET("api/users/{userId}/following/")
    suspend fun getFollowing(
        @Header("Authorization") bearerToken: String?,
        @Path("userId") userId: String
    ): ApiFollowListResponse

    @GET("api/users/me/follow-requests/")
    suspend fun getFollowRequests(
        @Header("Authorization") bearerToken: String
    ): List<ApiFollowRequestItem>

    @POST("api/users/follow-requests/{requestId}/accept/")
    suspend fun acceptFollowRequest(
        @Header("Authorization") bearerToken: String,
        @Path("requestId") requestId: String
    ): GenericMessageResponse

    @POST("api/users/follow-requests/{requestId}/reject/")
    suspend fun rejectFollowRequest(
        @Header("Authorization") bearerToken: String,
        @Path("requestId") requestId: String
    ): GenericMessageResponse

    @GET("api/users/me/photos/")
    suspend fun getUserPhotos(
        @Header("Authorization") bearerToken: String
    ): List<ApiUserPhoto>

    @POST("api/users/me/photos/{photoId}/activate/")
    suspend fun activatePhoto(
        @Header("Authorization") bearerToken: String,
        @Path("photoId") photoId: Int
    ): GenericMessageResponse

    // --- Resource Upload ---
    @Multipart
    @POST("api/resources/upload/")
    suspend fun uploadResource(
        @Header("Authorization") bearerToken: String,
        @Part file: okhttp3.MultipartBody.Part?,
        @Part("title") title: okhttp3.RequestBody,
        @Part("subject") subject: okhttp3.RequestBody,
        @Part("description") description: okhttp3.RequestBody?,
        @Part("grade_level") gradeLevel: okhttp3.RequestBody?,
        @Part("type") type: okhttp3.RequestBody?,
        @Part("exam_type") examType: okhttp3.RequestBody?,
        @Part("faculty") faculty: okhttp3.RequestBody?,
        @Part("program") program: okhttp3.RequestBody?,
        @Part("year") year: okhttp3.RequestBody?,
        @Part("school") school: okhttp3.RequestBody?,
        @Part("pradesh") pradesh: okhttp3.RequestBody?,
        @Part("district") district: okhttp3.RequestBody?,
        @Part("tags") tags: okhttp3.RequestBody?,
        @Part("file_url") fileUrl: okhttp3.RequestBody?,
        @Part("thumbnail_url") thumbnailUrl: okhttp3.RequestBody?,
        @Part("author_name") authorName: okhttp3.RequestBody?,
        @Part("source_label") sourceLabel: okhttp3.RequestBody?,
        @Part("source_url") sourceUrl: okhttp3.RequestBody?
    ): ApiResourceUploadResponse

    // --- Resources ---
    @GET("api/resources/")
    suspend fun getResources(
        @Header("Authorization") bearerToken: String?,
        @Query("subject") subject: String? = null,
        @Query("grade") grade: String? = null,
        @Query("type") type: String? = null,
        @Query("sort") sort: String? = null,
        @Query("page") page: Int? = null,
        @Query("page_size") pageSize: Int? = null
    ): ApiPaginatedResources

    @GET("api/resources/{resourceId}/")
    suspend fun getResource(
        @Header("Authorization") bearerToken: String?,
        @Path("resourceId") resourceId: String
    ): ApiResource

    @POST("api/resources/{resourceId}/view/")
    suspend fun viewResource(@Path("resourceId") resourceId: String)

    @POST("api/resources/{resourceId}/like/")
    suspend fun toggleLikeResource(
        @Header("Authorization") bearerToken: String,
        @Path("resourceId") resourceId: String
    ): ResourceLikeResponse

    @GET("api/resources/{resourceId}/comments/")
    suspend fun getResourceComments(
        @Header("Authorization") bearerToken: String?,
        @Path("resourceId") resourceId: String
    ): ApiResourceCommentsResponse

    @POST("api/resources/{resourceId}/comments/")
    suspend fun createResourceComment(
        @Header("Authorization") bearerToken: String,
        @Path("resourceId") resourceId: String,
        @Body request: ApiResourceCommentCreateRequest
    ): ApiResourceComment

    @DELETE("api/resources/{resourceId}/comments/{commentId}/")
    suspend fun deleteResourceComment(
        @Header("Authorization") bearerToken: String,
        @Path("resourceId") resourceId: String,
        @Path("commentId") commentId: String
    )

    // --- Posts ---
    @GET("api/posts/")
    suspend fun getPosts(
        @Header("Authorization") bearerToken: String?,
        @Query("category") category: String? = null,
        @Query("page") page: Int? = null,
        @Query("sort") sort: String? = null,
        @Query("search") search: String? = null,
        @Query("username") username: String? = null,
        @Query("page_size") pageSize: Int? = null
    ): ApiPaginatedPosts

    @GET("api/posts/{postId}/")
    suspend fun getPost(
        @Header("Authorization") bearerToken: String?,
        @Path("postId") postId: String
    ): ApiPost

    @POST("api/posts/")
    suspend fun createPost(
        @Header("Authorization") bearerToken: String,
        @Body request: PostCreateRequest
    ): ApiPost

    @PATCH("api/posts/{postId}/")
    suspend fun updatePost(
        @Header("Authorization") bearerToken: String,
        @Path("postId") postId: String,
        @Body request: PostUpdateRequest
    ): ApiPost

    @DELETE("api/posts/{postId}/")
    suspend fun deletePost(
        @Header("Authorization") bearerToken: String,
        @Path("postId") postId: String
    )

    @POST("api/posts/{postId}/like/")
    suspend fun toggleLikePost(
        @Header("Authorization") bearerToken: String,
        @Path("postId") postId: String
    ): LikeResponse

    @POST("api/posts/{postId}/archive/")
    suspend fun archivePost(
        @Header("Authorization") bearerToken: String,
        @Path("postId") postId: String
    ): GenericMessageResponse

    // --- Replies ---
    @GET("api/posts/{postId}/replies/")
    suspend fun getReplies(
        @Header("Authorization") bearerToken: String?,
        @Path("postId") postId: String
    ): ApiPaginatedReplies

    @POST("api/posts/{postId}/replies/")
    suspend fun createReply(
        @Header("Authorization") bearerToken: String,
        @Path("postId") postId: String,
        @Body request: ReplyCreateRequest
    ): ApiReply

    @PATCH("api/replies/{replyId}/")
    suspend fun updateReply(
        @Header("Authorization") bearerToken: String,
        @Path("replyId") replyId: String,
        @Body request: ReplyUpdateRequest
    ): ApiReply

    @DELETE("api/replies/{replyId}/")
    suspend fun deleteReply(
        @Header("Authorization") bearerToken: String,
        @Path("replyId") replyId: String
    )

    @POST("api/replies/{replyId}/like/")
    suspend fun toggleLikeReply(
        @Header("Authorization") bearerToken: String,
        @Path("replyId") replyId: String
    ): LikeResponse

    @POST("api/replies/{replyId}/archive/")
    suspend fun archiveReply(
        @Header("Authorization") bearerToken: String,
        @Path("replyId") replyId: String
    ): GenericMessageResponse

    // --- Edit History ---
    @GET("api/edit-history/{targetType}/{targetId}/")
    suspend fun getEditHistory(
        @Header("Authorization") bearerToken: String?,
        @Path("targetType") targetType: String,
        @Path("targetId") targetId: String
    ): List<ApiEditHistory>

    // --- News / Announcements (public web parity) ---
    @GET("news/")
    suspend fun getNewsPage(
        @Query("category") category: String? = null
    ): ResponseBody

    @GET("news/{slug}/")
    suspend fun getNewsDetailPage(
        @Path("slug") slug: String
    ): ResponseBody

    // --- Result Checker (same endpoint as the live website) ---
    @POST("ajax/results/check/")
    suspend fun checkResult(
        @Body request: ResultCheckRequest
    ): ResultCheckResponse

    // --- Search ---
    @GET("api/search/")
    suspend fun search(
        @Header("Authorization") bearerToken: String?,
        @Query("q") query: String,
        @Query("tab") tab: String? = null,
        @Query("subject") subject: String? = null,
        @Query("grade") grade: String? = null,
        @Query("type") type: String? = null,
        @Query("page_size") pageSize: Int? = null
    ): ApiSearchResponse

    // --- Bookmarks ---
    @POST("api/bookmarks/toggle/")
    suspend fun toggleBookmark(
        @Header("Authorization") bearerToken: String,
        @Body request: BookmarkToggleRequest
    ): BookmarkResponse

    @GET("api/bookmarks/check/")
    suspend fun checkBookmark(
        @Header("Authorization") bearerToken: String,
        @Query("target_type") targetType: String,
        @Query("target_id") targetId: String
    ): BookmarkResponse

    @GET("api/bookmarks/")
    suspend fun getBookmarks(
        @Header("Authorization") bearerToken: String,
        @Query("target_type") targetType: String? = null
    ): ApiPaginatedBookmarks

    // --- Study Spaces / Study Lab ---
    @GET("ajax/study-space/list/")
    suspend fun getStudySpaces(
        @Header("Authorization") bearerToken: String
    ): ApiStudySpaceListResponse

    @GET("ajax/study-space/public/")
    suspend fun getPublicStudySpaces(
        @Header("Authorization") bearerToken: String,
        @Query("q") query: String? = null,
        @Query("sort") sort: String? = null
    ): ApiStudySpaceListResponse

    @POST("ajax/study-space/create/")
    suspend fun createStudySpace(
        @Header("Authorization") bearerToken: String,
        @Body request: ApiStudySpaceCreateRequest
    ): ApiStudySpaceDetail

    @POST("ajax/study-space/join-code/")
    suspend fun joinStudySpaceByCode(
        @Header("Authorization") bearerToken: String,
        @Body request: ApiStudySpaceJoinRequest
    ): ApiStudySpaceJoinResponse

    @GET("ajax/study-space/{spaceId}/")
    suspend fun getStudySpaceDetail(
        @Header("Authorization") bearerToken: String,
        @Path("spaceId") spaceId: String
    ): ApiStudySpaceDetail

    // --- Neby AI / Arena ---
    @GET("api/neby-arena/models/")
    suspend fun getArenaModels(
        @Header("Authorization") bearerToken: String
    ): ApiArenaModelsResponse

    @GET("api/neby-arena/qwen/models/")
    suspend fun getQwenModels(
        @Header("Authorization") bearerToken: String
    ): ApiArenaModelsResponse

    @GET("api/neby-arena/sessions/")
    suspend fun getArenaSessions(
        @Header("Authorization") bearerToken: String
    ): ApiArenaSessionsResponse

    @POST("api/neby-arena/sessions/")
    suspend fun createArenaSession(
        @Header("Authorization") bearerToken: String,
        @Body request: ApiArenaCreateSessionRequest
    ): ApiArenaSessionResponse

    @POST("api/neby-arena/qwen/sessions/")
    suspend fun createQwenArenaSession(
        @Header("Authorization") bearerToken: String,
        @Body request: ApiArenaCreateSessionRequest
    ): ApiArenaSessionResponse

    @GET("api/neby-arena/sessions/{sessionId}/")
    suspend fun getArenaSessionDetail(
        @Header("Authorization") bearerToken: String,
        @Path("sessionId") sessionId: String
    ): ApiArenaSessionDetailResponse

    @Streaming
    @POST("api/neby-arena/sessions/{sessionId}/messages/")
    suspend fun sendArenaMessage(
        @Header("Authorization") bearerToken: String,
        @Path("sessionId") sessionId: String,
        @Body request: ApiArenaSendMessageRequest
    ): ResponseBody

    @Streaming
    @POST("api/neby-arena/qwen/sessions/{sessionId}/messages/sse/")
    suspend fun sendQwenArenaMessage(
        @Header("Authorization") bearerToken: String,
        @Path("sessionId") sessionId: String,
        @Body request: ApiArenaSendMessageRequest
    ): ResponseBody

    // --- Notifications ---
    @GET("api/notifications/")
    suspend fun getNotifications(
        @Header("Authorization") bearerToken: String,
        @Query("page") page: Int? = null
    ): ApiNotificationListResponse

    @POST("api/notifications/mark-read/")
    suspend fun markNotificationsRead(
        @Header("Authorization") bearerToken: String,
        @Body body: ApiNotificationMarkReadRequest = ApiNotificationMarkReadRequest(markAll = true)
    ): ApiNotificationMarkReadResponse

    @GET("api/notifications/unread-count/")
    suspend fun getUnreadNotificationCount(
        @Header("Authorization") bearerToken: String
    ): ApiNotificationUnreadCountResponse

    // --- FCM ---
    @POST("api/fcm/register/")
    suspend fun registerFcmToken(
        @Header("Authorization") bearerToken: String?,
        @Body request: FcmTokenRequest
    )

    // --- Account Deletion ---
    @GET("api/users/me/delete-account/")
    suspend fun getDeleteAccountRequestStatus(
        @Header("Authorization") bearerToken: String
    ): AccountDeletionRequestResponse

    @POST("api/users/me/delete-account/")
    suspend fun requestAccountDeletion(
        @Header("Authorization") bearerToken: String,
        @Body request: AccountDeletionSubmitRequest
    ): AccountDeletionSubmitResponse

    @DELETE("api/users/me/delete-account/")
    suspend fun cancelAccountDeletion(
        @Header("Authorization") bearerToken: String
    ): GenericMessageResponse

    // --- Reports ---
    @POST("api/reports/")
    suspend fun createReport(
        @Header("Authorization") bearerToken: String,
        @Body request: ReportRequest
    ): GenericMessageResponse

    // --- User search (for @mentions) ---
    @GET("api/users/search/")
    suspend fun searchUsers(
        @Header("Authorization") bearerToken: String?,
        @Query("q") query: String
    ): List<ApiUserSearchResult>

    // --- Web AJAX (Bearer-token authenticated; CSRF-exempt for mobile) ---

    /** Create a post with full poll support (MCQ, multi-select, explanation) + images. */
    @POST("ajax/post/")
    suspend fun createPostWeb(
        @Header("Authorization") bearerToken: String,
        @Body request: WebPostCreateRequest
    ): ApiPost

    /** Upload one post image; returns its hosted URL. Max 3 per post, 10MB each. */
    @Multipart
    @POST("ajax/post/upload-image/")
    suspend fun uploadPostImage(
        @Header("Authorization") bearerToken: String,
        @Part image: okhttp3.MultipartBody.Part
    ): UploadImageResponse

    /** Vote on a poll (single option_id or option_ids for multi-select). */
    @POST("api/polls/{pollId}/vote/")
    suspend fun votePoll(
        @Header("Authorization") bearerToken: String,
        @Path("pollId") pollId: String,
        @Body request: PollVoteRequest
    ): ApiPollVoteResponse

    /** Mini profile popover (web parity: shown on username hover / long-press). */
    @GET("ajax/user-popup/{username}/")
    suspend fun getUserPopup(
        @Header("Authorization") bearerToken: String?,
        @Path("username") username: String
    ): ApiUserPopup

    /** Paginated posts by a user, for the profile Posts tab. */
    @GET("ajax/profile/{username}/activity/")
    suspend fun getProfileActivity(
        @Header("Authorization") bearerToken: String?,
        @Path("username") username: String,
        @Query("offset") offset: Int = 0,
        @Query("limit") limit: Int = 10
    ): ApiProfileActivityResponse

    @GET("ajax/profile/{username}/replies/")
    suspend fun getProfileReplies(
        @Header("Authorization") bearerToken: String?,
        @Path("username") username: String,
        @Query("offset") offset: Int = 0,
        @Query("limit") limit: Int = 10
    ): ApiProfileRepliesResponse

    @GET("ajax/profile/{username}/resources/")
    suspend fun getProfileResources(
        @Header("Authorization") bearerToken: String?,
        @Path("username") username: String,
        @Query("offset") offset: Int = 0,
        @Query("limit") limit: Int = 10
    ): ApiProfileResourcesResponse

    // --- Realtime ---
    @GET("api/realtime/config/")
    suspend fun getRealtimeConfig(): ApiRealtimeConfig

    // --- Neby AI extras ---
    @PATCH("api/neby-arena/sessions/{sessionId}/")
    suspend fun updateArenaSession(
        @Header("Authorization") bearerToken: String,
        @Path("sessionId") sessionId: String,
        @Body request: ApiArenaUpdateSessionRequest
    ): GenericMessageResponse

    @DELETE("api/neby-arena/sessions/{sessionId}/")
    suspend fun deleteArenaSession(
        @Header("Authorization") bearerToken: String,
        @Path("sessionId") sessionId: String
    ): GenericMessageResponse

    @Streaming
    @POST("api/neby-arena/messages/{messageId}/regenerate/")
    suspend fun regenerateArenaMessage(
        @Header("Authorization") bearerToken: String,
        @Path("messageId") messageId: String
    ): ResponseBody

    /** Qwen send with base64-encoded file attachments (images, PDFs, docs — max 5 x 20MB). */
    @Streaming
    @POST("api/neby-arena/qwen/sessions/{sessionId}/messages/sse/")
    suspend fun sendQwenMessageWithFiles(
        @Header("Authorization") bearerToken: String,
        @Path("sessionId") sessionId: String,
        @Body request: ApiQwenSendMessageRequest
    ): ResponseBody

    // --- Study Lab: documents (web-parity AJAX endpoints, Bearer-auth) ---
    @Multipart
    @POST("ajax/study-lab/upload/")
    suspend fun uploadStudyDocument(
        @Header("Authorization") bearerToken: String,
        @Part file: okhttp3.MultipartBody.Part
    ): ApiStudyUploadResponse

    @GET("ajax/study-lab/documents/")
    suspend fun getStudyDocuments(
        @Header("Authorization") bearerToken: String
    ): ApiStudyDocumentsResponse

    @GET("ajax/study-lab/document/{docId}/")
    suspend fun getStudyDocumentDetail(
        @Header("Authorization") bearerToken: String,
        @Path("docId") docId: String
    ): ApiStudyDocDetailResponse

    @POST("ajax/study-lab/document/{docId}/delete/")
    suspend fun deleteStudyDocument(
        @Header("Authorization") bearerToken: String,
        @Path("docId") docId: String
    ): ApiStudySuccessResponse

    @GET("ajax/study-lab/document/{docId}/parse-status/")
    suspend fun getStudyParseStatus(
        @Header("Authorization") bearerToken: String,
        @Path("docId") docId: String
    ): ApiStudyParseStatus

    @POST("ajax/study-lab/document/{docId}/reparse/")
    suspend fun reparseStudyDocument(
        @Header("Authorization") bearerToken: String,
        @Path("docId") docId: String,
        @Query("force") force: Boolean? = null
    ): ApiStudyReparseResponse

    @POST("ajax/study-lab/document/{docId}/summary/")
    suspend fun generateStudySummary(
        @Header("Authorization") bearerToken: String,
        @Path("docId") docId: String,
        @Body request: ApiStudySummaryRequest
    ): ApiStudySummaryResponse

    @POST("ajax/study-lab/document/{docId}/mindmap/")
    suspend fun generateStudyMindmap(
        @Header("Authorization") bearerToken: String,
        @Path("docId") docId: String
    ): ApiStudyMindmapResponse

    @POST("ajax/study-lab/document/{docId}/quiz/")
    suspend fun generateStudyQuiz(
        @Header("Authorization") bearerToken: String,
        @Path("docId") docId: String,
        @Body request: ApiStudyCountRequest
    ): ApiStudyQuizResponse

    @POST("ajax/study-lab/document/{docId}/flashcards/")
    suspend fun generateStudyFlashcards(
        @Header("Authorization") bearerToken: String,
        @Path("docId") docId: String,
        @Body request: ApiStudyCountRequest
    ): ApiStudyFlashcardsResponse

    @GET("ajax/study-lab/quiz/{quizId}/")
    suspend fun getStudyQuiz(
        @Header("Authorization") bearerToken: String,
        @Path("quizId") quizId: String
    ): ApiStudyQuizResponse

    /** Document quizzes: answers keyed by question NUMBER (as string). */
    @POST("ajax/study-lab/quiz/{quizId}/submit/")
    suspend fun submitStudyQuiz(
        @Header("Authorization") bearerToken: String,
        @Path("quizId") quizId: String,
        @Body request: ApiStudyQuizSubmitRequest
    ): ApiStudyQuizSubmitResponse

    @POST("ajax/study-lab/flashcard/{cardId}/review/")
    suspend fun reviewStudyFlashcard(
        @Header("Authorization") bearerToken: String,
        @Path("cardId") cardId: String,
        @Body request: ApiStudyFlashcardReviewRequest
    ): ApiStudyFlashcardReviewResponse

    // --- Study Spaces: uploads + AI generation (web-parity) ---
    @Multipart
    @POST("ajax/study-space/{spaceId}/upload/")
    suspend fun uploadSpaceDocument(
        @Header("Authorization") bearerToken: String,
        @Path("spaceId") spaceId: String,
        @Part file: okhttp3.MultipartBody.Part
    ): ApiStudyUploadResponse

    @GET("ajax/study-space/{spaceId}/document/{docId}/parse-status/")
    suspend fun getSpaceParseStatus(
        @Header("Authorization") bearerToken: String,
        @Path("spaceId") spaceId: String,
        @Path("docId") docId: String
    ): ApiStudyParseStatus

    @POST("ajax/study-space/{spaceId}/document/{docId}/reparse/")
    suspend fun reparseSpaceDocument(
        @Header("Authorization") bearerToken: String,
        @Path("spaceId") spaceId: String,
        @Path("docId") docId: String
    ): ApiStudyReparseResponse

    @POST("ajax/study-space/{spaceId}/summary/")
    suspend fun generateSpaceSummary(
        @Header("Authorization") bearerToken: String,
        @Path("spaceId") spaceId: String,
        @Body request: ApiStudySummaryRequest
    ): ApiStudySummaryResponse

    @POST("ajax/study-space/{spaceId}/mindmap/")
    suspend fun generateSpaceMindmap(
        @Header("Authorization") bearerToken: String,
        @Path("spaceId") spaceId: String
    ): ApiStudyMindmapResponse

    @POST("ajax/study-space/{spaceId}/quiz/")
    suspend fun generateSpaceQuiz(
        @Header("Authorization") bearerToken: String,
        @Path("spaceId") spaceId: String,
        @Body request: ApiStudyCountRequest
    ): ApiStudyQuizResponse

    @GET("ajax/study-space/{spaceId}/quizzes/")
    suspend fun getSpaceQuizzes(
        @Header("Authorization") bearerToken: String,
        @Path("spaceId") spaceId: String
    ): ApiSpaceQuizzesResponse

    @POST("ajax/study-space/{spaceId}/flashcards/")
    suspend fun generateSpaceFlashcards(
        @Header("Authorization") bearerToken: String,
        @Path("spaceId") spaceId: String,
        @Body request: ApiStudyCountRequest
    ): ApiStudyFlashcardsResponse

    @GET("ajax/study-space/quiz/{quizId}/")
    suspend fun getSpaceQuiz(
        @Header("Authorization") bearerToken: String,
        @Path("quizId") quizId: String
    ): ApiStudyQuizResponse

    /** Space quizzes: answers keyed by question ID. */
    @POST("ajax/study-space/quiz/{quizId}/submit/")
    suspend fun submitSpaceQuiz(
        @Header("Authorization") bearerToken: String,
        @Path("quizId") quizId: String,
        @Body request: ApiStudyQuizSubmitRequest
    ): ApiStudyQuizSubmitResponse

    @POST("ajax/study-space/flashcard/{cardId}/review/")
    suspend fun reviewSpaceFlashcard(
        @Header("Authorization") bearerToken: String,
        @Path("cardId") cardId: String,
        @Body request: ApiStudyFlashcardReviewRequest
    ): ApiStudyFlashcardReviewResponse

    // --- Syllabus (public, web-synced categories) ---
    @GET("api/syllabus/categories/")
    suspend fun getSyllabusCategories(): ApiSyllabusCategoriesResponse

    @GET("api/syllabus/subjects/{gradeSlug}/{subjectSlug}/")
    suspend fun getSyllabusSubjectDetail(
        @Path("gradeSlug") gradeSlug: String,
        @Path("subjectSlug") subjectSlug: String
    ): ApiSyllabusSubjectDetailResponse

    // --- Interactive Learning (public, no auth required) ---
    @GET("api/interactive/categories/")
    suspend fun getInteractiveCategories(): ApiInteractiveCategoriesResponse

    @GET("api/interactive/courses/")
    suspend fun getInteractiveCourses(): ApiInteractiveCoursesResponse

    @GET("api/interactive/courses/{courseSlug}/")
    suspend fun getInteractiveCourseDetail(
        @Path("courseSlug") courseSlug: String
    ): ApiInteractiveCourseDetailResponse

    @GET("api/interactive/courses/{courseSlug}/{lessonSlug}/")
    suspend fun getInteractiveLessonDetail(
        @Path("courseSlug") courseSlug: String,
        @Path("lessonSlug") lessonSlug: String
    ): ApiInteractiveLessonDetailResponse

    companion object {
        private const val BASE_URL = "https://nebians.consica.com.np/"

        fun create(context: Context, tokenProvider: (() -> String?)? = null): ApiService {
            val logger = HttpLoggingInterceptor().apply {
                level = if (BuildConfig.DEBUG) HttpLoggingInterceptor.Level.BODY else HttpLoggingInterceptor.Level.NONE
            }

            val client = OkHttpClient.Builder()
                .addInterceptor(logger)
                .addInterceptor(WafChallengeInterceptor(context))
                .addInterceptor(RetryInterceptor(maxRetries = 2, initialBackoffMs = 500))
                .addInterceptor { chain ->
                    val request = chain.request().newBuilder()
                    tokenProvider?.invoke()?.let { token ->
                        request.header("Authorization", "Bearer $token")
                    }
                    chain.proceed(request.build())
                }
                .connectTimeout(30, java.util.concurrent.TimeUnit.SECONDS)
                .readTimeout(30, java.util.concurrent.TimeUnit.SECONDS)
                .writeTimeout(30, java.util.concurrent.TimeUnit.SECONDS)
                .build()

            val json = Json {
                ignoreUnknownKeys = true
                coerceInputValues = true
            }

            return Retrofit.Builder()
                .baseUrl(BASE_URL)
                .client(client)
                .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
                .build()
                .create(ApiService::class.java)
        }
    }
}

@Serializable
data class ApiUserPhoto(
    val id: Int,
    val url: String,
    @SerialName("uploaded_at") val uploadedAt: Long,
    @SerialName("is_current") val isCurrent: Boolean
)

@Serializable
data class ApiBookmark(
    val id: String,
    @SerialName("target_type") val targetType: String,
    @SerialName("target_id") val targetId: String,
    @SerialName("created_at") val createdAt: Long
)

@Serializable
data class ApiPaginatedBookmarks(
    @SerialName("results") val bookmarks: List<ApiBookmark> = emptyList(),
    @SerialName("count") val totalCount: Int = 0,
    val next: String? = null,
    val previous: String? = null
)

@Serializable
data class ApiAnalyticsStats(
    val posts: Int = 0,
    val replies: Int = 0,
    @SerialName("postViews") val postViews: Int = 0,
    @SerialName("postLikesReceived") val postLikesReceived: Int = 0,
    @SerialName("postRepliesReceived") val postRepliesReceived: Int = 0,
    val resources: Int = 0,
    @SerialName("resourceViews") val resourceViews: Int = 0,
    @SerialName("resourceLikesReceived") val resourceLikesReceived: Int = 0,
    @SerialName("resourceCommentsReceived") val resourceCommentsReceived: Int = 0,
    @SerialName("resourceCommentsMade") val resourceCommentsMade: Int = 0,
    val followers: Int = 0,
    val following: Int = 0,
    val bookmarks: Int = 0,
    @SerialName("notificationsUnread") val notificationsUnread: Int = 0,
    @SerialName("studyDocs") val studyDocs: Int = 0,
    val summaries: Int = 0,
    val mindmaps: Int = 0,
    val quizzes: Int = 0,
    @SerialName("quizAttempts") val quizAttempts: Int = 0,
    @SerialName("quizAccuracy") val quizAccuracy: Int = 0,
    @SerialName("quizXp") val quizXp: Int = 0,
    val flashcards: Int = 0,
    @SerialName("flashReviews") val flashReviews: Int = 0,
    @SerialName("easyReviews") val easyReviews: Int = 0,
    @SerialName("mediumReviews") val mediumReviews: Int = 0,
    @SerialName("hardReviews") val hardReviews: Int = 0,
    @SerialName("recentPosts") val recentPosts: Int = 0,
    @SerialName("recentReplies") val recentReplies: Int = 0,
    @SerialName("recentStudyActions") val recentStudyActions: Int = 0,
    @SerialName("contributionScore") val contributionScore: Int = 0,
    @SerialName("likesGiven") val likesGiven: Int = 0
)

@Serializable
data class ApiAnalyticsDay(
    val label: String = "",
    val total: Int = 0,
    val posts: Int = 0,
    val replies: Int = 0,
    val resources: Int = 0,
    val study: Int = 0,
    val height: Int = 8
)

@Serializable
data class ApiAnalyticsTopic(
    val label: String = "",
    val count: Int = 0,
    val width: Int = 0
)

@Serializable
data class ApiAnalyticsPost(
    val id: String = "",
    val title: String = "",
    val category: String = "",
    @SerialName("view_count") val viewCount: Int = 0,
    @SerialName("like_count") val likeCount: Int = 0,
    @SerialName("reply_count") val replyCount: Int = 0,
    @SerialName("created_at") val createdAt: Long = 0
)

@Serializable
data class ApiAnalyticsResource(
    val id: String = "",
    val title: String = "",
    val subject: String = "",
    val type: String = "",
    @SerialName("view_count") val viewCount: Int = 0,
    @SerialName("like_count") val likeCount: Int = 0,
    @SerialName("comment_count") val commentCount: Int = 0,
    @SerialName("added_at") val addedAt: Long = 0
)

@Serializable
data class ApiPrivateAnalyticsResponse(
    val username: String = "",
    val stats: ApiAnalyticsStats = ApiAnalyticsStats(),
    @SerialName("activityDays") val activityDays: List<ApiAnalyticsDay> = emptyList(),
    @SerialName("topCategories") val topCategories: List<ApiAnalyticsTopic> = emptyList(),
    @SerialName("topSubjects") val topSubjects: List<ApiAnalyticsTopic> = emptyList(),
    @SerialName("topPosts") val topPosts: List<ApiAnalyticsPost> = emptyList(),
    @SerialName("topResources") val topResources: List<ApiAnalyticsResource> = emptyList(),
    val suggestions: List<String> = emptyList()
)

@Serializable
data class ApiProfileStats(
    val username: String = "",
    @SerialName("post_count") val postCount: Int = 0,
    @SerialName("reply_count") val replyCount: Int = 0,
    @SerialName("follower_count") val followerCount: Int = 0,
    @SerialName("following_count") val followingCount: Int = 0,
    @SerialName("likes_received") val likesReceived: Int = 0,
    @SerialName("likes_given") val likesGiven: Int = 0,
    @SerialName("contribution_score") val contributionScore: Int = 0,
    @SerialName("uploaded_resources_count") val uploadedResourcesCount: Int = 0,
    @SerialName("is_following") val isFollowing: Boolean = false,
    @SerialName("is_requested") val isRequested: Boolean = false,
    @SerialName("follow_requests_count") val followRequestsCount: Int = 0,
    @SerialName("is_self") val isSelf: Boolean = false,
    @SerialName("is_private") val isPrivate: Boolean = false
)

@Serializable
data class ApiStudySpaceOwner(
    val id: String = "",
    val username: String = "",
    val displayName: String = "",
    val photoUrl: String = "",
    val badge: String = ""
)

@Serializable
data class ApiStudySpace(
    val id: String,
    val title: String = "Untitled Space",
    val description: String = "",
    val docCount: Int = 0,
    val memberCount: Int = 0,
    val activeNow: Int = 0,
    val shareMode: String = "",
    val visibility: String = "private",
    val inviteCode: String = "",
    val shareToken: String = "",
    val studyLevel: String = "",
    val subject: String = "",
    val exam: String = "",
    val isJoined: Boolean = false,
    val memberRole: String = "",
    val owner: ApiStudySpaceOwner? = null,
    val createdAt: Long = 0,
    val updatedAt: Long = 0,
    val hasSummary: Boolean = false,
    val hasMindmap: Boolean = false,
    val hasQuiz: Boolean = false,
    val hasFlashcards: Boolean = false
)

@Serializable
data class ApiStudySpaceListResponse(
    val spaces: List<ApiStudySpace> = emptyList()
)

@Serializable
data class ApiStudySpaceCreateRequest(
    val title: String,
    val description: String = ""
)

@Serializable
data class ApiStudySpaceJoinRequest(
    val code: String
)

@Serializable
data class ApiStudyDocument(
    val id: String,
    val title: String = "Untitled",
    val fileName: String = "",
    val fileSize: Long = 0,
    val mimeType: String = "",
    val pageCount: Int = 0,
    val status: String = "",
    val parseStatus: String = "",
    val parsedTextLength: Int = 0,
    val parseError: String = "",
    val summaryCompact: String = "",
    val summaryDetailed: String = "",
    val mindmapJson: String = "",
    val summaryGenerated: Boolean = false,
    val mindmapGenerated: Boolean = false,
    val quizCount: Int = 0,
    val flashcardCount: Int = 0,
    val shareMode: String = "",
    val sharedAt: Long = 0,
    val createdAt: Long = 0,
    val updatedAt: Long = 0
)

@Serializable
data class ApiStudyQuizSummary(
    val id: String,
    val title: String = "Study quiz",
    val questionCount: Int = 0,
    val createdAt: Long = 0,
    val attemptCount: Int = 0,
    val bestScore: Int = 0,
    val lastAttemptAt: Long? = null
)

@Serializable
data class ApiStudyFlashcard(
    val id: String,
    val front: String = "",
    val back: String = "",
    val cardNumber: Int = 0,
    val confidence: String = "new",
    val createdAt: Long = 0
)

@Serializable
data class ApiStudySpaceDetail(
    val id: String,
    val title: String = "Untitled Space",
    val description: String = "",
    val docCount: Int = 0,
    val documents: List<ApiStudyDocument> = emptyList(),
    val quizzes: List<ApiStudyQuizSummary> = emptyList(),
    val flashcardCount: Int = 0,
    val flashcards: List<ApiStudyFlashcard> = emptyList(),
    val shareMode: String = "",
    val visibility: String = "private",
    val inviteCode: String = "",
    val shareToken: String = "",
    val memberCount: Int = 0,
    val activeNow: Int = 0,
    val memberRole: String = "",
    val linkSummaryCompact: String? = null,
    val linkSummaryDetailed: String? = null,
    val linkMindmapJson: String? = null,
    val createdAt: Long = 0,
    val updatedAt: Long = 0
)

@Serializable
data class ApiStudySpaceJoinResponse(
    val success: Boolean = false,
    val space: ApiStudySpaceDetail? = null,
    val spaceId: String? = null,
    val redirectUrl: String? = null,
    val error: String? = null
)

@Serializable
data class ApiArenaModel(
    val id: String = "",
    val code: String = "",
    val name: String = "",
    val provider: String = "",
    val thinking: Boolean = false,
    val randomOnly: Boolean = false,
    val active: Boolean = true
)

@Serializable
data class ApiArenaModelsResponse(
    val models: List<ApiArenaModel> = emptyList(),
    val cached: Boolean = false
)

@Serializable
data class ApiArenaSession(
    val id: String,
    val title: String = "New chat",
    val modelId: String = "",
    val modelCode: String = "",
    val modelName: String = "",
    val provider: String = "ai4bharat",
    val messageCount: Int = 0,
    val createdAt: Long = 0,
    val updatedAt: Long = 0,
    val lastMessageAt: Long = 0,
    val isActive: Boolean = true
)

@Serializable
data class ApiArenaSessionsResponse(
    val sessions: List<ApiArenaSession> = emptyList()
)

@Serializable
data class ApiArenaCreateSessionRequest(
    val modelId: String,
    val title: String = "New chat"
)

@Serializable
data class ApiArenaSessionResponse(
    val session: ApiArenaSession
)

@Serializable
data class ApiArenaMessage(
    val id: String,
    val role: String,
    val content: String = "",
    val parentId: String = "",
    val finishReason: String = "",
    val error: String = "",
    val durationMs: Int = 0,
    val createdAt: Long = 0,
    val attachments: List<ApiArenaAttachment> = emptyList()
)

@Serializable
data class ApiArenaSessionDetailResponse(
    val session: ApiArenaSession,
    val messages: List<ApiArenaMessage> = emptyList()
)

@Serializable
data class ApiArenaSendMessageRequest(
    val content: String
)

// -------------------------------------------------------------
// NEBY AI EXTRA MODELS
// -------------------------------------------------------------

@Serializable
data class ApiArenaUpdateSessionRequest(
    val title: String? = null,
    @SerialName("isActive") val isActive: Boolean? = null
)

@Serializable
data class ApiQwenSendMessageRequest(
    val content: String,
    val files: List<ApiQwenFile> = emptyList()
)

@Serializable
data class ApiQwenFile(
    val name: String,
    /** Base64-encoded file content. */
    val data: String
)

@Serializable
data class ApiArenaAttachment(
    val id: String = "",
    val fileType: String = "",
    val fileName: String = "",
    val fileSize: Long = 0,
    val mimeType: String = "",
    val showType: String = "",
    val fileClass: String = ""
)

// -------------------------------------------------------------
// STUDY LAB MODELS (web-parity AJAX shapes)
// -------------------------------------------------------------

@Serializable
data class ApiStudySuccessResponse(
    val success: Boolean = false,
    val error: String? = null
)

@Serializable
data class ApiStudyUploadResponse(
    val document: ApiStudyDocument? = null,
    val error: String? = null
)

@Serializable
data class ApiStudyDocumentsResponse(
    val documents: List<ApiStudyDocument> = emptyList()
)

@Serializable
data class ApiStudyDocDetailResponse(
    val document: ApiStudyDocument? = null,
    val mindmap: ApiStudyMindmap? = null,
    val quizzes: List<ApiStudyQuizSummary> = emptyList(),
    val flashcards: List<ApiStudyFlashcard> = emptyList(),
    @SerialName("total_flashcards") val totalFlashcards: Int = 0,
    val error: String? = null
)

@Serializable
data class ApiStudyParseStatus(
    val id: String = "",
    val status: String = "",
    val parsedTextLength: Int = 0,
    val error: String? = null,
    val parsedAt: Long = 0
)

@Serializable
data class ApiStudyReparseResponse(
    val success: Boolean = false,
    val parseStatus: String = "",
    val document: ApiStudyDocument? = null,
    val error: String? = null
)

@Serializable
data class ApiStudySummaryRequest(
    val mode: String = "compact"
)

@Serializable
data class ApiStudyCountRequest(
    val count: Int
)

@Serializable
data class ApiStudySummaryResponse(
    val mode: String = "compact",
    val summary: String = "",
    val summaryCompact: String = "",
    val summaryDetailed: String = "",
    val error: String? = null,
    val parseStatus: String? = null
)

@Serializable
data class ApiStudyMindmap(
    val title: String = "",
    val nodes: List<ApiStudyMindmapNode> = emptyList()
)

@Serializable
data class ApiStudyMindmapNode(
    val title: String = "",
    val note: String = "",
    val children: List<ApiStudyMindmapNode> = emptyList()
)

@Serializable
data class ApiStudyMindmapResponse(
    val mindmap: ApiStudyMindmap? = null,
    val error: String? = null,
    val parseStatus: String? = null
)

@Serializable
data class ApiStudyQuizQuestion(
    val id: String,
    /** Document quizzes use `number`; space quizzes use `questionNumber`. */
    val number: Int = 0,
    @SerialName("questionNumber") val questionNumber: Int = 0,
    val question: String = "",
    @SerialName("questionText") val questionText: String = "",
    val optionA: String = "",
    val optionB: String = "",
    val optionC: String = "",
    val optionD: String = "",
    @SerialName("correctAnswer") val correctAnswer: String? = null,
    val explanation: String? = null
) {
    val displayNumber: Int get() = if (number > 0) number else questionNumber
    val displayQuestion: String get() = question.ifBlank { questionText }
}

@Serializable
data class ApiStudyQuizDetail(
    val id: String,
    val title: String = "Study quiz",
    val questionCount: Int = 0,
    val createdAt: Long = 0,
    val attemptCount: Int = 0,
    val bestScore: Int = 0,
    val questions: List<ApiStudyQuizQuestion> = emptyList()
)

@Serializable
data class ApiStudyQuizResponse(
    val quiz: ApiStudyQuizDetail? = null,
    val error: String? = null,
    val parseStatus: String? = null
)

@Serializable
data class ApiSpaceQuizzesResponse(
    val quizzes: List<ApiStudyQuizSummary> = emptyList(),
    val error: String? = null
)

@Serializable
data class ApiStudyQuizSubmitRequest(
    /** Document quizzes: keys are question NUMBERS as strings. Space quizzes: keys are question IDs. */
    val answers: Map<String, String>
)

@Serializable
data class ApiStudyQuizResult(
    val userAnswer: String = "",
    val correctAnswer: String = "",
    val isCorrect: Boolean = false,
    val explanation: String = ""
)

@Serializable
data class ApiSpaceQuizAnswerRecord(
    val questionId: String = "",
    val given: String = "",
    val correct: String = "",
    val isCorrect: Boolean = false
)

@Serializable
data class ApiStudyQuizAttempt(
    val id: String = "",
    val score: Int = 0,
    val totalQuestions: Int = 0,
    val xpEarned: Int = 0,
    /** Document quiz results: keyed by question number string. */
    val results: Map<String, ApiStudyQuizResult> = emptyMap(),
    /** Space quiz results: list of per-question records. */
    val answers: List<ApiSpaceQuizAnswerRecord> = emptyList()
)

@Serializable
data class ApiStudyQuizSubmitResponse(
    val attempt: ApiStudyQuizAttempt? = null,
    val error: String? = null
)

@Serializable
data class ApiStudyFlashcardsResponse(
    val flashcards: List<ApiStudyFlashcard> = emptyList(),
    val totalFlashcards: Int = 0,
    val error: String? = null,
    val parseStatus: String? = null
)

@Serializable
data class ApiStudyFlashcardReviewRequest(
    val confidence: String
)

@Serializable
data class ApiStudyFlashcardReviewResponse(
    @SerialName("flashcardId") val flashcardId: String = "",
    @SerialName("cardId") val cardId: String = "",
    val confidence: String = "",
    val reviewCount: Int = 0,
    @SerialName("nextReviewAt") val nextReviewAt: Long = 0,
    val error: String? = null
)

@Serializable
data class ApiInteractiveCategory(
    val key: String = "",
    val label: String = "",
    val icon: String = "",
    val color: String = "",
    val blurb: String = "",
    val courses: List<ApiInteractiveCourseSummary> = emptyList()
)

@Serializable
data class ApiInteractiveCourseSummary(
    val slug: String = "",
    val title: String = "",
    val category: String = "",
    val ageRange: String = "",
    val level: String = "",
    val icon: String = "",
    val color: String = "",
    val tagline: String = "",
    val lessonCount: Int = 0,
    val totalMinutes: Int = 0
)

@Serializable
data class ApiInteractiveCategoriesResponse(
    val categories: List<ApiInteractiveCategory> = emptyList()
)

@Serializable
data class ApiInteractiveCoursesResponse(
    val courses: List<ApiInteractiveCourseSummary> = emptyList()
)

@Serializable
data class ApiInteractiveCourseDetailResponse(
    val slug: String = "",
    val title: String = "",
    val category: String = "",
    val categoryLabel: String = "",
    val ageRange: String = "",
    val level: String = "",
    val icon: String = "",
    val color: String = "",
    val tagline: String = "",
    val description: String = "",
    val skills: List<String> = emptyList(),
    val lessons: List<ApiInteractiveLessonSummary> = emptyList(),
    val lessonCount: Int = 0,
    val totalMinutes: Int = 0
)

@Serializable
data class ApiInteractiveLessonSummary(
    val slug: String = "",
    val title: String = "",
    val icon: String = "",
    val minutes: Int = 0,
    val simType: String = "",
    val summary: String = "",
    val objectives: List<String> = emptyList()
)

@Serializable
data class ApiInteractiveLessonDetailResponse(
    val course: ApiInteractiveLessonCourseInfo = ApiInteractiveLessonCourseInfo(),
    val lesson: ApiInteractiveLessonFull = ApiInteractiveLessonFull(),
    val prevLesson: ApiInteractiveLessonNavInfo? = null,
    val nextLesson: ApiInteractiveLessonNavInfo? = null,
    val lessonIndex: Int = 0,
    val totalLessons: Int = 0
)

@Serializable
data class ApiInteractiveLessonCourseInfo(
    val slug: String = "",
    val title: String = "",
    val category: String = "",
    val icon: String = "",
    val color: String = "",
    val lessonCount: Int = 0
)

@Serializable
data class ApiInteractiveLessonFull(
    val slug: String = "",
    val title: String = "",
    val icon: String = "",
    val minutes: Int = 0,
    val simType: String = "",
    val sim: String = "",
    val summary: String = "",
    val objectives: List<String> = emptyList(),
    val knowledge: List<ApiInteractiveKnowledge> = emptyList(),
    val funFact: String = "",
    val quiz: List<ApiInteractiveQuizQuestion> = emptyList()
)

@Serializable
data class ApiInteractiveKnowledge(
    val heading: String = "",
    val body: String = ""
)

@Serializable
data class ApiInteractiveQuizQuestion(
    val q: String = "",
    val options: List<String> = emptyList(),
    val answer: Int = 0,
    val explain: String = ""
)

@Serializable
data class ApiInteractiveLessonNavInfo(
    val slug: String = "",
    val title: String = "",
    val icon: String = "",
    val minutes: Int = 0,
    val simType: String = ""
)
