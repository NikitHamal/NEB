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
    val id: String = "",
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
    @SerialName("thumbsUpCount") private val thumbsUpCountCamel: Int? = null,
    @SerialName("thumbs_up_count") private val thumbsUpCountSnake: Int? = null,
    @SerialName("isThumbedUp") private val isThumbedUpCamel: Boolean? = null,
    @SerialName("is_thumbed_up") private val isThumbedUpSnake: Boolean? = null
) {
    val thumbsUpCount: Int get() = thumbsUpCountCamel ?: thumbsUpCountSnake ?: 0
    val isThumbedUp: Boolean get() = isThumbedUpCamel ?: isThumbedUpSnake ?: false
}

@Serializable
data class ResourceLikeResponse(
    @SerialName("likeCount") private val likeCountCamel: Int? = null,
    @SerialName("like_count") private val likeCountSnake: Int? = null,
    @SerialName("isLiked") private val isLikedCamel: Boolean? = null,
    @SerialName("is_liked") private val isLikedSnake: Boolean? = null
) {
    val likeCount: Int get() = likeCountCamel ?: likeCountSnake ?: 0
    val isLiked: Boolean get() = isLikedCamel ?: isLikedSnake ?: false
}

@Serializable
data class BookmarkResponse(
    @SerialName("isBookmarked") private val isBookmarkedCamel: Boolean? = null,
    @SerialName("is_bookmarked") private val isBookmarkedSnake: Boolean? = null
) {
    val isBookmarked: Boolean get() = isBookmarkedCamel ?: isBookmarkedSnake ?: false
}

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
    @SerialName("resourceId") private val resourceIdCamel: String? = null,
    @SerialName("resource_id") private val resourceIdSnake: String? = null,
    @SerialName("authorId") private val userIdCamel: String? = null,
    @SerialName("user_id") private val userIdSnake: String? = null,
    @SerialName("authorName") private val userNameCamel: String? = null,
    @SerialName("user_name") private val userNameSnake: String? = null,
    @SerialName("authorPhoto") private val userPhotoUrlCamel: String? = null,
    @SerialName("user_photo_url") private val userPhotoUrlSnake: String? = null,
    val content: String,
    @SerialName("likeCount") private val likeCountCamel: Int? = null,
    @SerialName("like_count") private val likeCountSnake: Int? = null,
    @SerialName("replyCount") private val replyCountCamel: Int? = null,
    @SerialName("reply_count") private val replyCountSnake: Int? = null,
    @SerialName("isLiked") private val isLikedCamel: Boolean? = null,
    @SerialName("is_liked") private val isLikedSnake: Boolean? = null,
    @SerialName("parentCommentId") private val parentCommentIdCamel: String? = null,
    @SerialName("parent_comment_id") private val parentCommentIdSnake: String? = null,
    @SerialName("isEdited") private val isEditedCamel: Boolean? = null,
    @SerialName("is_edited") private val isEditedSnake: Boolean? = null,
    @SerialName("createdAt") private val createdAtCamel: Long? = null,
    @SerialName("created_at") private val createdAtSnake: Long? = null
) {
    val resourceId: String get() = resourceIdCamel ?: resourceIdSnake ?: ""
    val userId: String get() = userIdCamel ?: userIdSnake ?: ""
    val userName: String get() = userNameCamel ?: userNameSnake ?: ""
    val userPhotoUrl: String? get() = userPhotoUrlCamel ?: userPhotoUrlSnake
    val likeCount: Int get() = likeCountCamel ?: likeCountSnake ?: 0
    val replyCount: Int get() = replyCountCamel ?: replyCountSnake ?: 0
    val isLiked: Boolean? get() = isLikedCamel ?: isLikedSnake
    val parentCommentId: String? get() = parentCommentIdCamel ?: parentCommentIdSnake
    val isEdited: Boolean? get() = isEditedCamel ?: isEditedSnake
    val createdAt: Long get() = createdAtCamel ?: createdAtSnake ?: 0L
}

@Serializable
data class ApiResourceCommentCreateRequest(
    val content: String,
    @SerialName("parent_comment_id") val parentCommentId: String? = null
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
data class ApiPaginatedBookmarks(
    @SerialName("results") val bookmarks: List<ApiBookmark> = emptyList(),
    @SerialName("count") val totalCount: Int = 0,
    val next: String? = null,
    val previous: String? = null
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
        @Query("search") search: String? = null,
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
        @Query("target_type") targetType: String? = null
    ): ApiPaginatedBookmarks

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
    @SerialName("created_at") val createdAt: Long
)
