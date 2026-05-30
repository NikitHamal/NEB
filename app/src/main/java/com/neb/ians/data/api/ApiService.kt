package com.neb.ians.data.api

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.kotlinx.serialization.asConverterFactory
import retrofit2.http.*
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType

// -------------------------------------------------------------
// REQUEST/RESPONSE DATA MODELS
// -------------------------------------------------------------

@Serializable
data class GoogleAuthRequest(
    val idToken: String
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
data class SetPasswordRequest(
    val password: String
)

@Serializable
data class ChangePasswordRequest(
    val currentPassword: String,
    val newPassword: String
)

@Serializable
data class EmailVerifyRequest(
    val email: String,
    val code: String
)

@Serializable
data class EmailResendRequest(
    val email: String
)

@Serializable
data class EmailForgotRequest(
    val email: String
)

@Serializable
data class EmailResetPasswordRequest(
    val email: String,
    val code: String,
    val newPassword: String
)

@Serializable
data class EmailSignupResponse(
    val status: String = "",
    val message: String = "",
    val userId: String = "",
    val email: String = ""
)

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
    val isNewUser: Boolean = false,
    @SerialName("authToken") val authToken: String? = null,
    val user: UserProfileResponse
)

@Serializable
data class UserProfileResponse(
    val id: String,
    val username: String = "",
    val email: String? = null,
    @SerialName("photo_url") val photoUrl: String? = null,
    @SerialName("display_name") val displayName: String? = null,
    val dob: String = "",
    val gender: String? = null,
    @SerialName("class") val classLevel: String? = null,
    val subjects: String? = null, // Comma separated list of subjects
    val pradesh: String? = null,
    val district: String? = null,
    val school: String? = null,
    @SerialName("is_locked") val isLocked: Int = 0,
    @SerialName("created_at") val createdAt: Long = 0,
    val is_private: Boolean = false, // Set if profile is locked and we are not the owner
    @SerialName("email_verified") val emailVerified: Boolean = false,
    val hasPassword: Boolean = false
)

@Serializable
data class UsernameCheckResponse(
    val available: Boolean
)

@Serializable
data class UserProfileRequest(
    val username: String,
    val email: String?,
    val photoUrl: String?,
    val displayName: String?,
    val dob: String,
    val gender: String?,
    val classLevel: String?,
    val subjects: String?,
    val pradesh: String?,
    val district: String?,
    val school: String?,
    val isLocked: Boolean
)

@Serializable
data class ApiResource(
    val id: String,
    val title: String,
    val description: String = "",
    val subject: String,
    @SerialName("grade_level") val gradeLevel: String,
    val type: String,
    @SerialName("file_url") val fileUrl: String,
    @SerialName("thumbnail_url") val thumbnailUrl: String = "",
    @SerialName("file_size") val fileSize: Long = 0,
    @SerialName("added_at") val addedAt: Long = 0,
    @SerialName("view_count") val viewCount: Int = 0
)

@Serializable
data class ApiPost(
    val id: String,
    val title: String,
    val content: String,
    val authorName: String,
    val authorId: String,
    val category: String,
    val thumbsUpCount: Int,
    val replyCount: Int,
    val createdAt: Long,
    val updatedAt: Long,
    val isThumbedUp: Boolean
)

@Serializable
data class ApiPostCreateRequest(
    val title: String,
    val content: String,
    val category: String
)

@Serializable
data class ApiReply(
    val id: String,
    val postId: String,
    val parentReplyId: String?,
    val content: String,
    val authorName: String,
    val authorId: String,
    val thumbsUpCount: Int,
    val createdAt: Long,
    val isThumbedUp: Boolean
)

@Serializable
data class ApiReplyCreateRequest(
    val content: String,
    val parentReplyId: String? = null
)

@Serializable
data class LikeResponse(
    val thumbsUpCount: Int,
    val isThumbedUp: Boolean
)

@Serializable
data class FcmTokenRequest(
    val token: String
)

@Serializable
data class ApiReplyUpdateRequest(
    val content: String
)

@Serializable
data class ApiSearchResponse(
    val resources: List<ApiResource> = emptyList(),
    val posts: List<ApiPost> = emptyList()
)

// -------------------------------------------------------------
// RETROFIT API INTERFACE
// -------------------------------------------------------------

interface ApiService {

    @POST("api/auth/google")
    suspend fun authenticateGoogle(
        @Body request: GoogleAuthRequest
    ): GoogleAuthResponse

    @POST("api/auth/email/signup")
    suspend fun emailSignup(
        @Body request: EmailSignupRequest
    ): EmailSignupResponse

    @POST("api/auth/email/verify")
    suspend fun emailVerify(
        @Body request: EmailVerifyRequest
    ): GoogleAuthResponse

    @POST("api/auth/email/resend")
    suspend fun emailResendCode(
        @Body request: EmailResendRequest
    ): EmailSignupResponse

    @POST("api/auth/email/login")
    suspend fun emailLogin(
        @Body request: EmailLoginRequest
    ): GoogleAuthResponse

    @POST("api/auth/email/forgot")
    suspend fun emailForgotPassword(
        @Body request: EmailForgotRequest
    ): EmailSignupResponse

    @POST("api/auth/email/reset-password")
    suspend fun emailResetPassword(
        @Body request: EmailResetPasswordRequest
    ): GoogleAuthResponse

    @POST("api/auth/set-password")
    suspend fun setPassword(
        @Header("Authorization") bearerToken: String,
        @Body request: SetPasswordRequest
    ): GenericMessageResponse

    @POST("api/auth/change-password")
    suspend fun changePassword(
        @Header("Authorization") bearerToken: String,
        @Body request: ChangePasswordRequest
    ): ChangePasswordResponse

    @GET("api/users/check-username")
    suspend fun checkUsername(
        @Query("username") username: String
    ): UsernameCheckResponse

    @POST("api/users/profile")
    suspend fun updateProfile(
        @Header("Authorization") bearerToken: String,
        @Body request: UserProfileRequest
    ): GoogleAuthResponse

    @GET("api/users/profile/{username}")
    suspend fun getProfile(
        @Header("Authorization") bearerToken: String?,
        @Path("username") username: String
    ): UserProfileResponse

    @GET("api/resources")
    suspend fun getResources(): List<ApiResource>

    @GET("api/resources/{resourceId}")
    suspend fun getResource(
        @Path("resourceId") resourceId: String
    ): ApiResource

    @POST("api/resources/{resourceId}/view")
    suspend fun viewResource(
        @Path("resourceId") resourceId: String
    )

    @GET("api/posts")
    suspend fun getPosts(
        @Header("Authorization") bearerToken: String?
    ): List<ApiPost>

    @GET("api/posts/{postId}")
    suspend fun getPost(
        @Header("Authorization") bearerToken: String?,
        @Path("postId") postId: String
    ): ApiPost

    @PATCH("api/posts/{postId}")
    suspend fun updatePost(
        @Header("Authorization") bearerToken: String,
        @Path("postId") postId: String,
        @Body request: ApiPostCreateRequest
    ): ApiPost

    @POST("api/posts")
    suspend fun createPost(
        @Header("Authorization") bearerToken: String,
        @Body request: ApiPostCreateRequest
    ): ApiPost

    @DELETE("api/posts/{postId}")
    suspend fun deletePost(
        @Header("Authorization") bearerToken: String,
        @Path("postId") postId: String
    )

    @POST("api/posts/{postId}/like")
    suspend fun toggleLikePost(
        @Header("Authorization") bearerToken: String,
        @Path("postId") postId: String
    ): LikeResponse

    @GET("api/posts/{postId}/replies")
    suspend fun getReplies(
        @Header("Authorization") bearerToken: String?,
        @Path("postId") postId: String
    ): List<ApiReply>

    @POST("api/posts/{postId}/replies")
    suspend fun createReply(
        @Header("Authorization") bearerToken: String,
        @Path("postId") postId: String,
        @Body request: ApiReplyCreateRequest
    ): ApiReply

    @POST("api/replies/{replyId}/like")
    suspend fun toggleLikeReply(
        @Header("Authorization") bearerToken: String,
        @Path("replyId") replyId: String
    ): LikeResponse

    @DELETE("api/replies/{replyId}")
    suspend fun deleteReply(
        @Header("Authorization") bearerToken: String,
        @Path("replyId") replyId: String
    )

    @PATCH("api/replies/{replyId}")
    suspend fun updateReply(
        @Header("Authorization") bearerToken: String,
        @Path("replyId") replyId: String,
        @Body request: ApiReplyUpdateRequest
    ): ApiReply

    @GET("api/search")
    suspend fun search(
        @Query("q") query: String
    ): ApiSearchResponse

    @POST("api/fcm/register")
    suspend fun registerFcmToken(
        @Header("Authorization") bearerToken: String?,
        @Body request: FcmTokenRequest
    )

    companion object {
        private val BASE_URL = "https://nebians.consica.com.np/"

        fun create(): ApiService {
            val logger = HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            }

            val client = OkHttpClient.Builder()
                .addInterceptor(logger)
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
