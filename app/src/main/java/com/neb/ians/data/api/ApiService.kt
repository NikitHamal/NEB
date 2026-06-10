package com.neb.ians.data.api

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
    val username: String
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
    val category: String
)

@Serializable
data class PostUpdateRequest(
    val title: String? = null,
    val content: String? = null,
    val category: String? = null
)

@Serializable
data class ReplyCreateRequest(
    val content: String,
    @SerialName("parent_reply_id") val parentReplyId: String? = null
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
    val description: String? = null
)

@Serializable
data class FcmTokenRequest(val token: String)

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
    @SerialName("is_self") val isSelf: Boolean? = null,
    @SerialName("achievement_badges") val achievementBadges: String? = null
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
    @SerialName("is_liked") val isLiked: Boolean? = null,
    @SerialName("is_bookmarked") val isBookmarked: Boolean? = null
)

@Serializable
data class ApiPost(
    val id: String,
    val title: String,
    val content: String,
    @SerialName("authorName") val authorName: String,
    @SerialName("authorId") val authorId: String,
    @SerialName("authorPhotoUrl") val authorPhotoUrl: String? = null,
    @SerialName("authorBadge") val authorBadge: String? = null,
    val category: String,
    @SerialName("thumbsUpCount") val thumbsUpCount: Int,
    @SerialName("replyCount") val replyCount: Int,
    @SerialName("isThumbedUp") val isThumbedUp: Boolean,
    @SerialName("isBookmarked") val isBookmarked: Boolean? = null,
    @SerialName("isEdited") val isEdited: Boolean? = null,
    @SerialName("isArchived") val isArchived: Boolean? = null,
    @SerialName("createdAt") val createdAt: Long,
    @SerialName("updatedAt") val updatedAt: Long? = null
)

@Serializable
data class ApiReply(
    val id: String,
    @SerialName("postId") val postId: String,
    @SerialName("parentReplyId") val parentReplyId: String? = null,
    val content: String,
    @SerialName("authorName") val authorName: String,
    @SerialName("authorId") val authorId: String,
    @SerialName("authorPhotoUrl") val authorPhotoUrl: String? = null,
    @SerialName("authorBadge") val authorBadge: String? = null,
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
    @SerialName("thumbs_up_count") val thumbsUpCount: Int,
    @SerialName("is_thumbed_up") val isThumbedUp: Boolean
)

@Serializable
data class ResourceLikeResponse(
    @SerialName("like_count") val likeCount: Int,
    @SerialName("is_liked") val isLiked: Boolean
)

@Serializable
data class BookmarkResponse(
    @SerialName("is_bookmarked") val isBookmarked: Boolean
)

@Serializable
data class FollowResponse(
    @SerialName("is_following") val isFollowing: Boolean,
    @SerialName("follower_count") val followerCount: Int? = null
)

@Serializable
data class ApiSearchResponse(
    val resources: List<ApiResource> = emptyList(),
    val posts: List<ApiPost> = emptyList(),
    val users: List<ApiUserSearchResult> = emptyList()
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
    val label: String,
    val icon: String? = null
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
    @SerialName("target_type") val targetType: String,
    @SerialName("target_id") val targetId: String,
    val field: String,
    @SerialName("old_value") val oldValue: String,
    @SerialName("new_value") val newValue: String,
    @SerialName("edited_by") val editedBy: String,
    @SerialName("editor_name") val editorName: String? = null,
    @SerialName("edited_at") val editedAt: Long
)

@Serializable
data class ApiResourceComment(
    val id: String,
    @SerialName("resource_id") val resourceId: String,
    @SerialName("user_id") val userId: String,
    @SerialName("user_name") val userName: String,
    @SerialName("user_photo_url") val userPhotoUrl: String? = null,
    val content: String,
    @SerialName("like_count") val likeCount: Int = 0,
    @SerialName("reply_count") val replyCount: Int = 0,
    @SerialName("is_liked") val isLiked: Boolean? = null,
    @SerialName("parent_comment_id") val parentCommentId: String? = null,
    @SerialName("is_edited") val isEdited: Boolean? = null,
    @SerialName("created_at") val createdAt: Long
)

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

// -------------------------------------------------------------
// NEBY AI — AI4Bharat Arena chat proxy (/api/neby-arena/)
// -------------------------------------------------------------

@Serializable
data class ArenaModel(
    val id: String,
    val code: String = "",
    val name: String = "",
    val provider: String = "",
    val thinking: Boolean = false,
    val randomOnly: Boolean = false,
    val active: Boolean = true
)

@Serializable
data class ArenaModelsResponse(
    val models: List<ArenaModel> = emptyList(),
    val cached: Boolean = false
)

@Serializable
data class ArenaSession(
    val id: String,
    val title: String = "New chat",
    val modelId: String = "",
    val modelCode: String = "",
    val modelName: String = "",
    val messageCount: Int = 0,
    val createdAt: Long = 0,
    val updatedAt: Long = 0,
    val lastMessageAt: Long = 0,
    val provider: String = ""
)

@Serializable
data class ArenaSessionsResponse(
    val sessions: List<ArenaSession> = emptyList()
)

@Serializable
data class ArenaSessionCreateRequest(
    val modelId: String,
    val title: String? = null
)

@Serializable
data class ArenaSessionWrapper(
    val session: ArenaSession
)

@Serializable
data class ArenaSessionUpdateRequest(
    val title: String? = null,
    val isActive: Boolean? = null
)

@Serializable
data class ArenaAttachment(
    val id: String,
    val fileType: String = "",
    val fileName: String = "",
    val fileSize: Long = 0,
    val mimeType: String = "",
    val showType: String = "",
    val fileClass: String = ""
)

@Serializable
data class ArenaMessage(
    val id: String,
    val role: String,
    val content: String = "",
    val parentId: String? = null,
    val arenaMessageId: String? = null,
    val finishReason: String? = null,
    val error: String? = null,
    val durationMs: Long = 0,
    val createdAt: Long = 0,
    val attachments: List<ArenaAttachment> = emptyList()
)

@Serializable
data class ArenaSessionDetail(
    val id: String,
    val title: String = "",
    val modelId: String = "",
    val modelCode: String = "",
    val modelName: String = "",
    val messageCount: Int = 0,
    val createdAt: Long = 0,
    val updatedAt: Long = 0,
    val provider: String = ""
)

@Serializable
data class ArenaSessionDetailResponse(
    val session: ArenaSessionDetail,
    val messages: List<ArenaMessage> = emptyList()
)

// -------------------------------------------------------------
// ANALYTICS — private learning dashboard (/api/analytics/me/)
// -------------------------------------------------------------

@Serializable
data class AnalyticsStats(
    val posts: Int = 0,
    val replies: Int = 0,
    val postViews: Int = 0,
    val postLikesReceived: Int = 0,
    val postRepliesReceived: Int = 0,
    val resources: Int = 0,
    val resourceViews: Int = 0,
    val resourceLikesReceived: Int = 0,
    val resourceCommentsReceived: Int = 0,
    val resourceCommentsMade: Int = 0,
    val followers: Int = 0,
    val following: Int = 0,
    val bookmarks: Int = 0,
    val studyDocs: Int = 0,
    val summaries: Int = 0,
    val mindmaps: Int = 0,
    val quizzes: Int = 0,
    val quizAttempts: Int = 0,
    val quizAccuracy: Int = 0,
    val quizXp: Int = 0,
    val flashcards: Int = 0,
    val flashReviews: Int = 0,
    val easyReviews: Int = 0,
    val mediumReviews: Int = 0,
    val hardReviews: Int = 0,
    val recentPosts: Int = 0,
    val recentReplies: Int = 0,
    val recentStudyActions: Int = 0
)

@Serializable
data class AnalyticsActivityCounts(
    val posts: Int = 0,
    val replies: Int = 0,
    val resources: Int = 0,
    val study: Int = 0
)

@Serializable
data class AnalyticsActivityDay(
    val label: String = "",
    val total: Int = 0,
    val counts: AnalyticsActivityCounts = AnalyticsActivityCounts(),
    val height: Int = 8
)

@Serializable
data class AnalyticsCounterRow(
    val label: String = "",
    val count: Int = 0,
    val width: Int = 0
)

@Serializable
data class AnalyticsResponse(
    val stats: AnalyticsStats = AnalyticsStats(),
    val activityDays: List<AnalyticsActivityDay> = emptyList(),
    val topCategories: List<AnalyticsCounterRow> = emptyList(),
    val topSubjects: List<AnalyticsCounterRow> = emptyList(),
    val suggestions: List<String> = emptyList()
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

    @POST("api/users/{userId}/follow/")
    suspend fun toggleFollow(
        @Header("Authorization") bearerToken: String,
        @Path("userId") userId: String
    ): FollowResponse

    @GET("api/users/{userId}/followers/")
    suspend fun getFollowers(
        @Header("Authorization") bearerToken: String?,
        @Path("userId") userId: String
    ): List<UserProfileResponse>

    @GET("api/users/{userId}/following/")
    suspend fun getFollowing(
        @Header("Authorization") bearerToken: String?,
        @Path("userId") userId: String
    ): List<UserProfileResponse>

    @GET("api/users/me/photos/")
    suspend fun getUserPhotos(
        @Header("Authorization") bearerToken: String
    ): List<ApiUserPhoto>

    @POST("api/users/me/photos/{photoId}/activate/")
    suspend fun activatePhoto(
        @Header("Authorization") bearerToken: String,
        @Path("photoId") photoId: Int
    ): GenericMessageResponse

    // --- Resources ---
    @GET("api/resources/")
    suspend fun getResources(
        @Header("Authorization") bearerToken: String?,
        @Query("subject") subject: String? = null,
        @Query("grade") grade: String? = null,
        @Query("type") type: String? = null,
        @Query("sort") sort: String? = null,
        @Query("page") page: Int? = null
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
        @Query("page") page: Int? = null
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
    ): List<ApiReply>

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

    // --- Search ---
    @GET("api/search/")
    suspend fun search(
        @Header("Authorization") bearerToken: String?,
        @Query("q") query: String,
        @Query("tab") tab: String? = null,
        @Query("subject") subject: String? = null,
        @Query("grade") grade: String? = null,
        @Query("type") type: String? = null
    ): ApiSearchResponse

    // --- Bookmarks ---
    @POST("api/bookmarks/toggle/")
    suspend fun toggleBookmark(
        @Header("Authorization") bearerToken: String,
        @Body request: BookmarkToggleRequest
    ): BookmarkResponse

    @POST("api/bookmarks/check/")
    suspend fun checkBookmark(
        @Header("Authorization") bearerToken: String,
        @Body request: BookmarkToggleRequest
    ): BookmarkResponse

    @GET("api/bookmarks/")
    suspend fun getBookmarks(
        @Header("Authorization") bearerToken: String,
        @Query("target_type") targetType: String? = null,
        @Query("page") page: Int? = null
    ): ApiBookmarksResponse

    // --- Notifications ---
    @GET("api/notifications/")
    suspend fun getNotifications(
        @Header("Authorization") bearerToken: String,
        @Query("page") page: Int? = null
    ): ApiNotificationListResponse

    @POST("api/notifications/mark-read/")
    suspend fun markNotificationsRead(
        @Header("Authorization") bearerToken: String
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

    // --- Analytics ---
    @GET("api/analytics/me/")
    suspend fun getAnalytics(
        @Header("Authorization") bearerToken: String
    ): AnalyticsResponse

    // --- Neby AI (AI4Bharat Arena) ---
    @GET("api/neby-arena/models/")
    suspend fun getArenaModels(
        @Header("Authorization") bearerToken: String
    ): ArenaModelsResponse

    @GET("api/neby-arena/sessions/")
    suspend fun getArenaSessions(
        @Header("Authorization") bearerToken: String
    ): ArenaSessionsResponse

    @POST("api/neby-arena/sessions/")
    suspend fun createArenaSession(
        @Header("Authorization") bearerToken: String,
        @Body request: ArenaSessionCreateRequest
    ): ArenaSessionWrapper

    @GET("api/neby-arena/sessions/{sessionId}/")
    suspend fun getArenaSession(
        @Header("Authorization") bearerToken: String,
        @Path("sessionId") sessionId: String
    ): ArenaSessionDetailResponse

    @PATCH("api/neby-arena/sessions/{sessionId}/")
    suspend fun updateArenaSession(
        @Header("Authorization") bearerToken: String,
        @Path("sessionId") sessionId: String,
        @Body request: ArenaSessionUpdateRequest
    ): GenericMessageResponse

    @DELETE("api/neby-arena/sessions/{sessionId}/")
    suspend fun deleteArenaSession(
        @Header("Authorization") bearerToken: String,
        @Path("sessionId") sessionId: String
    ): GenericMessageResponse

    companion object {
        private const val BASE_URL = "https://nebians.consica.com.np/"

        fun create(tokenProvider: (() -> String?)? = null): ApiService {
            val logger = HttpLoggingInterceptor().apply {
                level = if (BuildConfig.DEBUG) HttpLoggingInterceptor.Level.BODY else HttpLoggingInterceptor.Level.NONE
            }

            val client = OkHttpClient.Builder()
                .addInterceptor(logger)
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
    @SerialName("created_at") val createdAt: Long,
    val resource: ApiResource? = null,
    val post: ApiPost? = null
)

@Serializable
data class ApiBookmarksResponse(
    @SerialName("results") val results: List<ApiBookmark> = emptyList(),
    @SerialName("count") val count: Int = 0,
    val next: String? = null,
    val previous: String? = null
)

