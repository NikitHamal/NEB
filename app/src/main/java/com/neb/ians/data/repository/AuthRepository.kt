package com.neb.ians.data.repository

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.*
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.coroutines.launch
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.SupervisorJob
import javax.inject.Inject
import javax.inject.Singleton
import com.neb.ians.data.api.ApiErrorMapper
import dagger.hilt.android.qualifiers.ApplicationContext

sealed interface AuthState {
    object Loading : AuthState
    object Unauthenticated : AuthState
    object Guest : AuthState
    data class Authenticated(val userId: String, val isProfileComplete: Boolean) : AuthState
}

@Singleton
class AuthRepository @Inject constructor(
    @ApplicationContext private val appContext: Context,
    private val dataStore: DataStore<Preferences>,
    private val apiService: com.neb.ians.data.api.ApiService
) {
    private val LEGACY_AUTH_TOKEN = stringPreferencesKey("auth_token")

    init {
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
            migratePlaintextTokenToSecurePrefs()
        }
    }

    private suspend fun migratePlaintextTokenToSecurePrefs() {
        try {
            val prefs = dataStore.data.first()
            val legacyToken = prefs[LEGACY_AUTH_TOKEN]
            if (!legacyToken.isNullOrBlank()) {
                SecurePrefs.setAuthToken(appContext, legacyToken)
                dataStore.edit { it.remove(LEGACY_AUTH_TOKEN) }
            }
        } catch (_: Exception) { }
    }
    companion object {
        private val AUTH_STATUS = stringPreferencesKey("auth_status")
        private val PROFILE_COMPLETED = booleanPreferencesKey("profile_completed")

        val USER_ID = stringPreferencesKey("user_id")
        val USER_NAME = stringPreferencesKey("user_name")
        val USER_EMAIL = stringPreferencesKey("user_email")
        val USER_PHOTO_URL = stringPreferencesKey("user_photo_url")
        val USER_DISPLAY_NAME = stringPreferencesKey("user_display_name")
        val USER_BANNER_URL = stringPreferencesKey("user_banner_url")
        val USER_ROLE = stringPreferencesKey("user_role")
        val USER_TEACHING_SUBJECTS = stringPreferencesKey("user_teaching_subjects")
        val USER_INSTITUTION_TYPE = stringPreferencesKey("user_institution_type")
        val USER_DOB = stringPreferencesKey("user_dob")
        val USER_GENDER = stringPreferencesKey("user_gender")
        val USER_CLASS = stringPreferencesKey("user_class")
        val USER_SUBJECTS = stringPreferencesKey("user_subjects")
        val USER_PRADESH = stringPreferencesKey("user_pradesh")
        val USER_DISTRICT = stringPreferencesKey("user_district")
        val USER_SCHOOL = stringPreferencesKey("user_school")
        val USER_SCHOOL_USERNAME = stringPreferencesKey("user_school_username")
        val USER_BIO = stringPreferencesKey("user_bio")
        val USER_LOCKED = booleanPreferencesKey("user_locked")
        val USER_HAS_PASSWORD = booleanPreferencesKey("user_has_password")
        val USER_IS_ADMIN = booleanPreferencesKey("user_is_admin")
        val USER_VERIFICATION_LEVEL = intPreferencesKey("user_verification_level")
        val USER_MODERATOR_LEVEL = intPreferencesKey("user_moderator_level")
        val USER_POST_COUNT = intPreferencesKey("user_post_count")
        val USER_REPLY_COUNT = intPreferencesKey("user_reply_count")
        val USER_FOLLOWER_COUNT = intPreferencesKey("user_follower_count")
        val USER_FOLLOWING_COUNT = intPreferencesKey("user_following_count")
        val USER_CONTRIBUTION_SCORE = intPreferencesKey("user_contribution_score")
        val USER_ACHIEVEMENT_BADGES = stringPreferencesKey("user_achievement_badges")
        val USER_FCM_TOKEN = stringPreferencesKey("user_fcm_token")

        const val GOOGLE_SERVER_CLIENT_ID = "68143624035-que25r0vmrke4agasr715j5u9p8gic2s.apps.googleusercontent.com"
        const val GITHUB_CLIENT_ID = "Ov23lii7dRW1FhLQ09w7"
        const val GITHUB_REDIRECT_URI = "https://nebians.consica.com.np/auth/github/callback/"
    }

    val authState: Flow<AuthState> = dataStore.data.map { preferences ->
        val status = preferences[AUTH_STATUS] ?: "unauthenticated"
        val token = SecurePrefs.getAuthToken(appContext)
        val completed = preferences[PROFILE_COMPLETED] ?: false

        when (status) {
            "guest" -> AuthState.Guest
            "authenticated" -> {
                if (!token.isNullOrBlank()) AuthState.Authenticated(token, completed)
                else AuthState.Unauthenticated
            }
            else -> AuthState.Unauthenticated
        }
    }

    val tokenFlow: Flow<String?> = dataStore.data.map { SecurePrefs.getAuthToken(appContext) }
    val isProfileCompletedFlow: Flow<Boolean> = dataStore.data.map { it[PROFILE_COMPLETED] ?: false }
    private val ioScope = CoroutineScope(Dispatchers.IO + SupervisorJob())

    private fun firstName(prefs: Preferences): String =
        prefs[USER_DISPLAY_NAME]?.split(Regex("\\s+"))?.firstOrNull()?.takeIf { it.isNotBlank() }
            ?: prefs[USER_NAME]?.takeIf { it.isNotBlank() }
            ?: "Student"

    val currentUserNameFlow: StateFlow<String> = dataStore.data.map { firstName(it) }
        .stateIn(ioScope, SharingStarted.Eagerly, "Student")
    val currentUsernameHandleFlow: Flow<String> = dataStore.data.map { it[USER_NAME] ?: "" }
    val currentUserIdFlow: Flow<String?> = dataStore.data.map { it[USER_ID] }
    val currentUserPhotoUrlFlow: Flow<String?> = dataStore.data.map { it[USER_PHOTO_URL] }
    val currentUserVerificationLevelFlow: Flow<Int> = dataStore.data.map { it[USER_VERIFICATION_LEVEL] ?: 0 }
    val currentUserIsAdminFlow: Flow<Boolean> = dataStore.data.map { it[USER_IS_ADMIN] ?: false }

    val userProfileFlow: Flow<UserProfileCache?> = dataStore.data.map { preferences ->
        val userId = preferences[USER_ID]
        val status = preferences[AUTH_STATUS] ?: "unauthenticated"
        if (userId.isNullOrBlank() || userId == "guest_user" || status != "authenticated") return@map null
        UserProfileCache(
            id = userId,
            username = preferences[USER_NAME] ?: "",
            email = preferences[USER_EMAIL],
            photoUrl = preferences[USER_PHOTO_URL],
            bannerUrl = preferences[USER_BANNER_URL],
            displayName = preferences[USER_DISPLAY_NAME],
            role = preferences[USER_ROLE],
            teachingSubjects = preferences[USER_TEACHING_SUBJECTS],
            institutionType = preferences[USER_INSTITUTION_TYPE],
            dob = preferences[USER_DOB] ?: "",
            gender = preferences[USER_GENDER],
            classLevel = preferences[USER_CLASS],
            subjects = preferences[USER_SUBJECTS],
            pradesh = preferences[USER_PRADESH],
            district = preferences[USER_DISTRICT],
            school = preferences[USER_SCHOOL],
            schoolUsername = preferences[USER_SCHOOL_USERNAME],
            bio = preferences[USER_BIO],
            isLocked = preferences[USER_LOCKED] ?: false,
            hasPassword = preferences[USER_HAS_PASSWORD] ?: false,
            isAdmin = preferences[USER_IS_ADMIN] ?: false,
            verificationLevel = preferences[USER_VERIFICATION_LEVEL] ?: 0,
            moderatorLevel = preferences[USER_MODERATOR_LEVEL] ?: 0,
            postCount = preferences[USER_POST_COUNT] ?: 0,
            replyCount = preferences[USER_REPLY_COUNT] ?: 0,
            followerCount = preferences[USER_FOLLOWER_COUNT] ?: 0,
            followingCount = preferences[USER_FOLLOWING_COUNT] ?: 0,
            contributionScore = preferences[USER_CONTRIBUTION_SCORE] ?: 0,
            achievementBadges = preferences[USER_ACHIEVEMENT_BADGES]
        )
    }

    suspend fun getToken(): String? = SecurePrefs.getAuthToken(appContext)

    fun getTokenSync(): String? {
        return try {
            SecurePrefs.getAuthToken(appContext)
        } catch (_: Exception) { null }
    }

    suspend fun getBearerToken(): String? {
        val token = getToken()?.takeIf { it.isNotBlank() } ?: return null
        return "Bearer $token"
    }

    suspend fun signInWithGoogle(idToken: String): OAuthResult {
        return try {
            val response = withContext(Dispatchers.IO) {
                apiService.authenticateGoogle(com.neb.ians.data.api.GoogleAuthRequest(idToken))
            }
            val authToken = response.authToken ?: return OAuthResult.Failure("No auth token received")
            withContext(Dispatchers.IO) { cacheUser(response.user, authToken, response.isNewUser) }
            OAuthResult.Success(response.isNewUser)
        } catch (e: Exception) {
            OAuthResult.Failure(ApiErrorMapper.mapException(e))
        }
    }

    suspend fun signInWithGitHub(code: String): OAuthResult {
        return try {
            val response = withContext(Dispatchers.IO) {
                apiService.authenticateGitHub(com.neb.ians.data.api.GitHubAuthRequest(code, GITHUB_REDIRECT_URI))
            }
            val authToken = response.authToken ?: return OAuthResult.Failure("No auth token received")
            withContext(Dispatchers.IO) { cacheUser(response.user, authToken, response.isNewUser) }
            OAuthResult.Success(response.isNewUser)
        } catch (e: Exception) {
            OAuthResult.Failure(ApiErrorMapper.mapException(e))
        }
    }

    suspend fun signInWithWebToken(token: String, isNewUser: Boolean, username: String?): Boolean {
        return try {
            SecurePrefs.setAuthToken(appContext, token)
            dataStore.edit { prefs ->
                prefs[AUTH_STATUS] = "authenticated"
                prefs[PROFILE_COMPLETED] = !isNewUser
                prefs[USER_NAME] = username ?: ""
                prefs.remove(USER_ID)
            }
            if (!username.isNullOrEmpty()) {
                refreshProfile()
            }
            syncFcmToken()
            true
        } catch (e: Exception) {
            false
        }
    }

    private suspend fun cacheUser(user: com.neb.ians.data.api.UserProfileResponse, authToken: String, isNewUser: Boolean) {
        SecurePrefs.setAuthToken(appContext, authToken)
        dataStore.edit { prefs ->
            prefs[AUTH_STATUS] = "authenticated"
            prefs[USER_ID] = user.id
            prefs[USER_EMAIL] = user.email ?: ""
            prefs[USER_PHOTO_URL] = user.photoUrl ?: ""
            prefs[USER_DISPLAY_NAME] = user.displayName ?: ""
            prefs[USER_BANNER_URL] = user.bannerUrl ?: ""
            prefs[USER_BIO] = user.bio ?: ""
            if (isNewUser) {
                prefs[PROFILE_COMPLETED] = false
                prefs[USER_NAME] = user.username
            } else {
                prefs[PROFILE_COMPLETED] = true
                prefs[USER_NAME] = user.username
                prefs[USER_DOB] = user.dob
                prefs[USER_GENDER] = user.gender ?: ""
                prefs[USER_CLASS] = user.classLevel ?: ""
                prefs[USER_SUBJECTS] = user.subjects ?: ""
                prefs[USER_PRADESH] = user.pradesh ?: ""
                prefs[USER_DISTRICT] = user.district ?: ""
                prefs[USER_SCHOOL] = user.school ?: ""
                prefs[USER_SCHOOL_USERNAME] = user.schoolUsername ?: ""
                prefs[USER_LOCKED] = user.isLocked == 1
                prefs[USER_HAS_PASSWORD] = user.hasPassword
                prefs[USER_IS_ADMIN] = user.isAdmin
                prefs[USER_VERIFICATION_LEVEL] = user.verificationLevel
                prefs[USER_MODERATOR_LEVEL] = user.moderatorLevel
                prefs[USER_POST_COUNT] = user.postCount
                prefs[USER_REPLY_COUNT] = user.replyCount
                prefs[USER_FOLLOWER_COUNT] = user.followerCount
                prefs[USER_FOLLOWING_COUNT] = user.followingCount
                prefs[USER_CONTRIBUTION_SCORE] = user.contributionScore
                prefs[USER_ACHIEVEMENT_BADGES] = user.achievementBadges ?: ""
            }
        }
        syncFcmToken()
    }

    suspend fun continueAsGuest() {
        SecurePrefs.clearAuthToken(appContext)
        dataStore.edit { prefs ->
            prefs[AUTH_STATUS] = "guest"
            prefs[PROFILE_COMPLETED] = false
            prefs[USER_ID] = "guest_user"
            prefs[USER_NAME] = "Guest"
        }
    }

    suspend fun emailSignup(email: String, password: String, username: String, role: String = "student"): EmailAuthResult {
        return try {
            val response = withContext(Dispatchers.IO) {
                apiService.emailSignup(com.neb.ians.data.api.EmailSignupRequest(email, password, username, role))
            }
            if (response.status == "success") {
                EmailAuthResult.SignupSuccess(response.userId, response.email)
            } else {
                EmailAuthResult.Failure("Signup failed")
            }
        } catch (e: Exception) {
            EmailAuthResult.Failure(ApiErrorMapper.mapException(e))
        }
    }

    suspend fun emailVerify(email: String, code: String): EmailAuthResult {
        return try {
            val response = withContext(Dispatchers.IO) {
                apiService.emailVerify(com.neb.ians.data.api.EmailVerifyRequest(email, code))
            }
            if (response.status == "success" && response.authToken != null) {
                val user = response.user
                val authToken = response.authToken!!
                withContext(Dispatchers.IO) { cacheUser(user, authToken, response.isNewUser) }
                EmailAuthResult.VerifySuccess(response.isNewUser, authToken, user)
            } else {
                EmailAuthResult.Failure("Verification failed")
            }
        } catch (e: Exception) {
            EmailAuthResult.Failure(ApiErrorMapper.mapException(e))
        }
    }

    suspend fun emailResendCode(email: String): EmailAuthResult {
        return try {
            val response = withContext(Dispatchers.IO) { apiService.emailResendCode(com.neb.ians.data.api.EmailResendRequest(email)) }
            EmailAuthResult.Message(response.message.ifEmpty { "Code resent" })
        } catch (e: Exception) {
            EmailAuthResult.Failure(ApiErrorMapper.mapException(e))
        }
    }

    suspend fun emailLogin(email: String, password: String): EmailAuthResult {
        return try {
            val response = withContext(Dispatchers.IO) {
                apiService.emailLogin(com.neb.ians.data.api.EmailLoginRequest(email, password))
            }
            if (response.status == "success" && response.authToken != null) {
                val user = response.user
                val authToken = response.authToken!!
                withContext(Dispatchers.IO) { cacheUser(user, authToken, response.isNewUser) }
                EmailAuthResult.LoginSuccess(response.isNewUser, authToken, user)
            } else {
                EmailAuthResult.Failure("Login failed")
            }
        } catch (e: Exception) {
            EmailAuthResult.Failure(ApiErrorMapper.mapException(e))
        }
    }

    suspend fun emailForgotPassword(email: String): EmailAuthResult {
        return try {
            val response = withContext(Dispatchers.IO) { apiService.emailForgotPassword(com.neb.ians.data.api.EmailForgotRequest(email)) }
            EmailAuthResult.Message(response.message.ifEmpty { "If an account exists, a code has been sent" })
        } catch (e: Exception) {
            EmailAuthResult.Failure(ApiErrorMapper.mapException(e))
        }
    }

    suspend fun emailResetPassword(email: String, code: String, newPassword: String): EmailAuthResult {
        return try {
            val response = withContext(Dispatchers.IO) {
                apiService.emailResetPassword(com.neb.ians.data.api.EmailResetPasswordRequest(email, code, newPassword))
            }
            if (response.status == "success" && response.authToken != null) {
                val user = response.user
                val authToken = response.authToken!!
                withContext(Dispatchers.IO) { cacheUser(user, authToken, false) }
                EmailAuthResult.ResetSuccess(authToken, user)
            } else {
                EmailAuthResult.Failure("Password reset failed")
            }
        } catch (e: Exception) {
            EmailAuthResult.Failure(ApiErrorMapper.mapException(e))
        }
    }

    suspend fun setPassword(password: String): PasswordResult {
        return try {
            val bearer = getBearerToken() ?: return PasswordResult.Failure("Not authenticated")
            val response = withContext(Dispatchers.IO) { apiService.setPassword(bearer, com.neb.ians.data.api.SetPasswordRequest(password)) }
            if (response.status == "success") {
                dataStore.edit { prefs -> prefs[USER_HAS_PASSWORD] = true }
                PasswordResult.Success
            } else {
                PasswordResult.Failure(response.error ?: "Failed to set password")
            }
        } catch (e: Exception) {
            PasswordResult.Failure(ApiErrorMapper.mapException(e))
        }
    }

    suspend fun changePassword(currentPassword: String, newPassword: String): PasswordResult {
        return try {
            val bearer = getBearerToken() ?: return PasswordResult.Failure("Not authenticated")
            val response = withContext(Dispatchers.IO) {
                apiService.changePassword(bearer, com.neb.ians.data.api.ChangePasswordRequest(currentPassword, newPassword))
            }
            if (response.status == "success") {
                response.authToken?.let { newToken ->
                    SecurePrefs.setAuthToken(appContext, newToken)
                }
                PasswordResult.Success
            } else {
                PasswordResult.Failure(response.error ?: "Failed to change password")
            }
        } catch (e: Exception) {
            PasswordResult.Failure(ApiErrorMapper.mapException(e))
        }
    }

    suspend fun completeProfile(profile: com.neb.ians.data.api.UserProfileRequest): String? {
        return try {
            val bearer = getBearerToken() ?: return "Not authenticated"
            val response = withContext(Dispatchers.IO) {
                apiService.updateProfile(bearer, profile)
            }
            val user = response.user
            withContext(Dispatchers.IO) {
                dataStore.edit { prefs ->
                    prefs[USER_ID] = user.id
                    prefs[PROFILE_COMPLETED] = true
                    prefs[USER_NAME] = user.username
                    prefs[USER_EMAIL] = user.email ?: ""
                    prefs[USER_PHOTO_URL] = user.photoUrl ?: ""
                    prefs[USER_DISPLAY_NAME] = user.displayName ?: ""
                    prefs[USER_BANNER_URL] = user.bannerUrl ?: ""
                    prefs[USER_ROLE] = user.role ?: ""
                    prefs[USER_TEACHING_SUBJECTS] = user.teachingSubjects ?: ""
                    prefs[USER_INSTITUTION_TYPE] = user.institutionType ?: ""
                    prefs[USER_DOB] = user.dob
                    prefs[USER_GENDER] = user.gender ?: ""
                    prefs[USER_CLASS] = user.classLevel ?: ""
                    prefs[USER_SUBJECTS] = user.subjects ?: ""
                    prefs[USER_PRADESH] = user.pradesh ?: ""
                    prefs[USER_DISTRICT] = user.district ?: ""
                    prefs[USER_SCHOOL] = user.school ?: ""
                    prefs[USER_SCHOOL_USERNAME] = user.schoolUsername ?: ""
                    prefs[USER_BIO] = user.bio ?: ""
                    prefs[USER_LOCKED] = user.isLocked == 1
                    prefs[USER_HAS_PASSWORD] = user.hasPassword
                }
            }
            null
        } catch (e: Exception) {
            ApiErrorMapper.mapException(e)
        }
    }

    suspend fun uploadProfilePhoto(filePart: okhttp3.MultipartBody.Part): String? {
        return try {
            val bearer = getBearerToken() ?: return null
            val response = withContext(Dispatchers.IO) {
                apiService.uploadProfilePhoto(bearer, filePart)
            }
            withContext(Dispatchers.IO) {
                dataStore.edit { prefs ->
                    prefs[USER_PHOTO_URL] = response.url
                }
            }
            response.url
        } catch (e: Exception) {
            null
        }
    }

    suspend fun refreshProfile() {
        try {
            val bearer = getBearerToken() ?: return
            val username = dataStore.data.first()[USER_NAME] ?: return
            val response = withContext(Dispatchers.IO) { apiService.getProfile(bearer, username) }
            withContext(Dispatchers.IO) {
                dataStore.edit { prefs ->
                    prefs[USER_ID] = response.id
                    prefs[USER_EMAIL] = response.email ?: ""
                    prefs[USER_PHOTO_URL] = response.photoUrl ?: ""
                    prefs[USER_DISPLAY_NAME] = response.displayName ?: ""
                    prefs[USER_BANNER_URL] = response.bannerUrl ?: ""
                    prefs[USER_ROLE] = response.role ?: ""
                    prefs[USER_TEACHING_SUBJECTS] = response.teachingSubjects ?: ""
                    prefs[USER_INSTITUTION_TYPE] = response.institutionType ?: ""
                    prefs[USER_DOB] = response.dob
                    prefs[USER_GENDER] = response.gender ?: ""
                    prefs[USER_CLASS] = response.classLevel ?: ""
                    prefs[USER_SUBJECTS] = response.subjects ?: ""
                    prefs[USER_PRADESH] = response.pradesh ?: ""
                    prefs[USER_DISTRICT] = response.district ?: ""
                    prefs[USER_SCHOOL] = response.school ?: ""
                    prefs[USER_SCHOOL_USERNAME] = response.schoolUsername ?: ""
                    prefs[USER_BIO] = response.bio ?: ""
                    prefs[USER_LOCKED] = response.isLocked == 1
                    prefs[USER_HAS_PASSWORD] = response.hasPassword
                    prefs[USER_FOLLOWER_COUNT] = response.followerCount
                    prefs[USER_FOLLOWING_COUNT] = response.followingCount
                    prefs[USER_POST_COUNT] = response.postCount
                    prefs[USER_REPLY_COUNT] = response.replyCount
                    prefs[USER_CONTRIBUTION_SCORE] = response.contributionScore
                    prefs[USER_VERIFICATION_LEVEL] = response.verificationLevel
                    prefs[USER_MODERATOR_LEVEL] = response.moderatorLevel
                    prefs[USER_IS_ADMIN] = response.isAdmin
                    prefs[USER_ACHIEVEMENT_BADGES] = response.achievementBadges ?: ""
                }
            }
        } catch (_: Exception) { }
    }

    suspend fun getPublicProfile(username: String): com.neb.ians.data.api.UserProfileResponse? {
        return try {
            val bearer = getBearerToken()
            withContext(Dispatchers.IO) { apiService.getProfile(bearer, username) }
        } catch (_: Exception) { null }
    }

    suspend fun logout() {
        try {
            val bearer = getBearerToken()
            if (bearer != null) {
                val prefs = dataStore.data.first()
                val savedToken = prefs[USER_FCM_TOKEN] ?: ""
                if (savedToken.isNotBlank()) {
                    kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
                        try {
                            apiService.unregisterFcmToken(bearer, com.neb.ians.data.api.FcmTokenRequest(savedToken))
                        } catch (_: Exception) {}
                    }
                }
            }
        } catch (_: Exception) {}
        SecurePrefs.clearAuthToken(appContext)
        dataStore.edit { prefs ->
            prefs[AUTH_STATUS] = "unauthenticated"
            prefs[PROFILE_COMPLETED] = false
            prefs[USER_ID] = ""
            prefs[USER_NAME] = "Student"
            prefs[USER_EMAIL] = ""
            prefs[USER_PHOTO_URL] = ""
            prefs[USER_DISPLAY_NAME] = ""
            prefs[USER_BANNER_URL] = ""
            prefs[USER_ROLE] = ""
            prefs[USER_TEACHING_SUBJECTS] = ""
            prefs[USER_INSTITUTION_TYPE] = ""
            prefs[USER_DOB] = ""
            prefs[USER_GENDER] = ""
            prefs[USER_CLASS] = ""
            prefs[USER_SUBJECTS] = ""
            prefs[USER_PRADESH] = ""
            prefs[USER_DISTRICT] = ""
            prefs[USER_SCHOOL] = ""
            prefs[USER_SCHOOL_USERNAME] = ""
            prefs[USER_BIO] = ""
            prefs[USER_LOCKED] = false
            prefs[USER_HAS_PASSWORD] = false
            prefs[USER_IS_ADMIN] = false
            prefs[USER_VERIFICATION_LEVEL] = 0
            prefs[USER_MODERATOR_LEVEL] = 0
            prefs[USER_POST_COUNT] = 0
            prefs[USER_REPLY_COUNT] = 0
            prefs[USER_FOLLOWER_COUNT] = 0
            prefs[USER_FOLLOWING_COUNT] = 0
            prefs[USER_CONTRIBUTION_SCORE] = 0
        }
    }

    suspend fun updateCachedPhotoUrl(url: String?) {
        dataStore.edit { prefs -> prefs[USER_PHOTO_URL] = url ?: "" }
    }

    fun syncFcmToken() {
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
            try {
                val fcmRefreshedKey = booleanPreferencesKey("fcm_project_refreshed_nebiansnepal_v2")
                val prefs = dataStore.data.first()
                val isRefreshed = prefs[fcmRefreshedKey] ?: false
                if (!isRefreshed) {
                    try {
                        com.google.firebase.messaging.FirebaseMessaging.getInstance().deleteToken()
                            .addOnCompleteListener { task ->
                                kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
                                    try {
                                        dataStore.edit { it[fcmRefreshedKey] = true }
                                        fetchAndRegisterNewToken()
                                    } catch (_: Exception) {}
                                }
                            }
                    } catch (e: Exception) {
                        fetchAndRegisterNewToken()
                    }
                } else {
                    fetchAndRegisterNewToken()
                }
            } catch (e: Exception) {
                fetchAndRegisterNewToken()
            }
        }
    }

    private fun fetchAndRegisterNewToken() {
        try {
            com.google.firebase.messaging.FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
                if (task.isSuccessful) {
                    val token = task.result
                    if (!token.isNullOrBlank()) {
                        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
                            try {
                                val bearer = getBearerToken()
                                if (bearer != null) {
                                    apiService.registerFcmToken(bearer, com.neb.ians.data.api.FcmTokenRequest(token))
                                    dataStore.edit { it[USER_FCM_TOKEN] = token }
                                }
                            } catch (_: Exception) {
                            }
                        }
                    }
                }
            }
        } catch (_: Exception) {
        }
    }

    suspend fun getDeleteAccountRequestStatus(): com.neb.ians.data.api.AccountDeletionRequestResponse? {
        return try {
            val bearer = getBearerToken() ?: return null
            withContext(Dispatchers.IO) {
                apiService.getDeleteAccountRequestStatus(bearer)
            }
        } catch (e: Exception) {
            null
        }
    }

    suspend fun requestAccountDeletion(reason: String): com.neb.ians.data.api.AccountDeletionSubmitResponse? {
        return try {
            val bearer = getBearerToken() ?: return null
            withContext(Dispatchers.IO) {
                apiService.requestAccountDeletion(bearer, com.neb.ians.data.api.AccountDeletionSubmitRequest(reason))
            }
        } catch (e: Exception) {
            null
        }
    }

    suspend fun cancelAccountDeletion(): Boolean {
        return try {
            val bearer = getBearerToken() ?: return false
            val response = withContext(Dispatchers.IO) {
                apiService.cancelAccountDeletion(bearer)
            }
            response.status == "success" || response.message.isNotEmpty()
        } catch (e: Exception) {
            false
        }
    }

    suspend fun markNotificationRead(notificationId: String) {
        try {
            val bearer = getBearerToken() ?: return
            withContext(Dispatchers.IO) {
                apiService.markNotificationsRead(
                    bearer,
                    com.neb.ians.data.api.ApiNotificationMarkReadRequest(
                        notificationIds = listOf(notificationId)
                    )
                )
            }
        } catch (_: Exception) {}
    }
}

sealed class PasswordResult {
    object Success : PasswordResult()
    data class Failure(val message: String) : PasswordResult()
}

sealed class OAuthResult {
    data class Success(val isNewUser: Boolean) : OAuthResult()
    data class Failure(val message: String) : OAuthResult()
}

sealed class EmailAuthResult {
    data class SignupSuccess(val userId: String, val email: String) : EmailAuthResult()
    data class VerifySuccess(val isNewUser: Boolean, val authToken: String, val user: com.neb.ians.data.api.UserProfileResponse) : EmailAuthResult()
    data class LoginSuccess(val isNewUser: Boolean, val authToken: String, val user: com.neb.ians.data.api.UserProfileResponse) : EmailAuthResult()
    data class ResetSuccess(val authToken: String, val user: com.neb.ians.data.api.UserProfileResponse) : EmailAuthResult()
    data class Message(val message: String) : EmailAuthResult()
    data class Failure(val message: String) : EmailAuthResult()
}

data class UserProfileCache(
    val id: String,
    val username: String,
    val email: String?,
    val photoUrl: String?,
    val bannerUrl: String?,
    val displayName: String?,
    val role: String?,
    val teachingSubjects: String?,
    val institutionType: String?,
    val dob: String,
    val gender: String?,
    val classLevel: String?,
    val subjects: String?,
    val pradesh: String?,
    val district: String?,
    val school: String?,
    val schoolUsername: String? = null,
    val bio: String?,
    val isLocked: Boolean,
    val hasPassword: Boolean = false,
    val isAdmin: Boolean = false,
    val verificationLevel: Int = 0,
    val moderatorLevel: Int = 0,
    val postCount: Int = 0,
    val replyCount: Int = 0,
    val followerCount: Int = 0,
    val followingCount: Int = 0,
    val contributionScore: Int = 0,
    val achievementBadges: String? = null
)
