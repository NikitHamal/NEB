package com.neb.ians.data.repository

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.*
import androidx.credentials.CredentialManager
import androidx.credentials.GetCredentialRequest
import androidx.credentials.CustomCredential
import com.google.android.libraries.identity.googleid.GetGoogleIdOption
import com.google.android.libraries.identity.googleid.GoogleIdTokenCredential
import com.neb.ians.data.api.*
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import javax.inject.Inject
import javax.inject.Singleton

sealed interface AuthState {
    object Loading : AuthState
    object Unauthenticated : AuthState
    object Guest : AuthState
    data class Authenticated(val userId: String, val isProfileComplete: Boolean) : AuthState
}

@Singleton
class AuthRepository @Inject constructor(
    private val dataStore: DataStore<Preferences>,
    private val apiService: ApiService
) {
    companion object {
        private val AUTH_TOKEN = stringPreferencesKey("auth_token")
        private val AUTH_STATUS = stringPreferencesKey("auth_status")
        private val PROFILE_COMPLETED = booleanPreferencesKey("profile_completed")

        val USER_ID = stringPreferencesKey("user_id")
        val USER_NAME = stringPreferencesKey("user_name")
        val USER_EMAIL = stringPreferencesKey("user_email")
        val USER_PHOTO_URL = stringPreferencesKey("user_photo_url")
        val USER_DISPLAY_NAME = stringPreferencesKey("user_display_name")
        val USER_BANNER_URL = stringPreferencesKey("user_banner_url")
        val USER_DOB = stringPreferencesKey("user_dob")
        val USER_GENDER = stringPreferencesKey("user_gender")
        val USER_CLASS = stringPreferencesKey("user_class")
        val USER_SUBJECTS = stringPreferencesKey("user_subjects")
        val USER_PRADESH = stringPreferencesKey("user_pradesh")
        val USER_DISTRICT = stringPreferencesKey("user_district")
        val USER_SCHOOL = stringPreferencesKey("user_school")
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
    }

    val authState: Flow<AuthState> = dataStore.data.map { preferences ->
        val status = preferences[AUTH_STATUS] ?: "unauthenticated"
        val token = preferences[AUTH_TOKEN]
        val completed = preferences[PROFILE_COMPLETED] ?: false

        when (status) {
            "guest" -> AuthState.Guest
            "authenticated" -> {
                if (token != null) AuthState.Authenticated(token, completed)
                else AuthState.Unauthenticated
            }
            else -> AuthState.Unauthenticated
        }
    }

    val tokenFlow: Flow<String?> = dataStore.data.map { it[AUTH_TOKEN] }
    val isProfileCompletedFlow: Flow<Boolean> = dataStore.data.map { it[PROFILE_COMPLETED] ?: false }
    val currentUserNameFlow: Flow<String> = dataStore.data.map { it[USER_NAME] ?: "Student" }
    val currentUserIdFlow: Flow<String?> = dataStore.data.map { it[USER_ID] }

    val userProfileFlow: Flow<UserProfileCache?> = dataStore.data.map { preferences ->
        val userId = preferences[USER_ID] ?: return@map null
        UserProfileCache(
            id = userId,
            username = preferences[USER_NAME] ?: "",
            email = preferences[USER_EMAIL],
            photoUrl = preferences[USER_PHOTO_URL],
            bannerUrl = preferences[USER_BANNER_URL],
            displayName = preferences[USER_DISPLAY_NAME],
            dob = preferences[USER_DOB] ?: "",
            gender = preferences[USER_GENDER],
            classLevel = preferences[USER_CLASS],
            subjects = preferences[USER_SUBJECTS],
            pradesh = preferences[USER_PRADESH],
            district = preferences[USER_DISTRICT],
            school = preferences[USER_SCHOOL],
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

    suspend fun getToken(): String? = tokenFlow.first()

    fun getTokenSync(): String? {
        return try {
            kotlinx.coroutines.runBlocking { tokenFlow.first() }
        } catch (_: Exception) { null }
    }

    suspend fun getBearerToken(): String? {
        val token = getToken() ?: return null
        return "Bearer $token"
    }

    private suspend fun cacheUser(user: UserProfileResponse, authToken: String, isNewUser: Boolean) {
        dataStore.edit { prefs ->
            prefs[AUTH_TOKEN] = authToken
            prefs[AUTH_STATUS] = "authenticated"
            prefs[USER_ID] = user.id
            prefs[USER_EMAIL] = user.email ?: ""
            prefs[USER_PHOTO_URL] = user.photoUrl ?: ""
            prefs[USER_DISPLAY_NAME] = user.displayName ?: ""
            prefs[USER_BANNER_URL] = user.bannerUrl ?: ""
            prefs[USER_BIO] = user.bio ?: ""
            if (isNewUser) {
                prefs[PROFILE_COMPLETED] = false
                prefs[USER_NAME] = ""
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
    }

    suspend fun signInWithGoogle(context: Context): GoogleSignInResult {
        return try {
            val credentialManager = CredentialManager.create(context)
            val googleIdOption = GetGoogleIdOption.Builder()
                .setFilterByAuthorizedAccounts(false)
                .setServerClientId("478709074228-cu0b0t75ghhsvqp2jotj75g6utj84nre.apps.googleusercontent.com")
                .setAutoSelectEnabled(false)
                .build()

            val request = GetCredentialRequest.Builder()
                .addCredentialOption(googleIdOption)
                .build()

            val result = credentialManager.getCredential(context, request)
            val credential = result.credential

            if (credential is CustomCredential && credential.type == GoogleIdTokenCredential.TYPE_GOOGLE_ID_TOKEN_CREDENTIAL) {
                val googleIdTokenCredential = GoogleIdTokenCredential.createFrom(credential.data)
                val idToken = googleIdTokenCredential.idToken

                val response = withContext(Dispatchers.IO) {
                    apiService.authenticateGoogle(GoogleAuthRequest(idToken))
                }

                val user = response.user
                val authToken = response.authToken ?: user.id
                withContext(Dispatchers.IO) {
                    cacheUser(user, authToken, response.isNewUser)
                }
                GoogleSignInResult.Success(response.isNewUser)
            } else {
                GoogleSignInResult.Failure("Unsupported credential type")
            }
        } catch (e: Exception) {
            GoogleSignInResult.Failure(e.localizedMessage ?: "Google Sign-In failed")
        }
    }

    suspend fun signInWithGithub(authCode: String): GithubSignInResult {
        return try {
            val response = withContext(Dispatchers.IO) {
                apiService.authenticateGithub(GithubAuthRequest(authCode, "nebians://github-callback"))
            }
            val user = response.user
            val authToken = response.authToken ?: user.id
            withContext(Dispatchers.IO) {
                cacheUser(user, authToken, response.isNewUser)
            }
            GithubSignInResult.Success(response.isNewUser)
        } catch (e: Exception) {
            GithubSignInResult.Failure(e.localizedMessage ?: "GitHub Sign-In failed")
        }
    }

    suspend fun completeProfile(profile: UserProfileRequest): Boolean {
        return try {
            val bearer = getBearerToken() ?: return false
            val response = withContext(Dispatchers.IO) {
                apiService.updateProfile(bearer, profile)
            }
            val user = response.user
            withContext(Dispatchers.IO) {
                dataStore.edit { prefs ->
                    prefs[PROFILE_COMPLETED] = true
                    prefs[USER_NAME] = user.username
                    prefs[USER_DOB] = user.dob
                    prefs[USER_GENDER] = user.gender ?: ""
                    prefs[USER_CLASS] = user.classLevel ?: ""
                    prefs[USER_SUBJECTS] = user.subjects ?: ""
                    prefs[USER_PRADESH] = user.pradesh ?: ""
                    prefs[USER_DISTRICT] = user.district ?: ""
                    prefs[USER_SCHOOL] = user.school ?: ""
                    prefs[USER_LOCKED] = user.isLocked == 1
                    prefs[USER_HAS_PASSWORD] = user.hasPassword
                }
            }
            true
        } catch (_: Exception) { false }
    }

    suspend fun continueAsGuest() {
        dataStore.edit { prefs ->
            prefs[AUTH_STATUS] = "guest"
            prefs[AUTH_TOKEN] = ""
            prefs[PROFILE_COMPLETED] = false
            prefs[USER_ID] = "guest_user"
            prefs[USER_NAME] = "Guest"
        }
    }

    suspend fun emailSignup(email: String, password: String, username: String): EmailAuthResult {
        return try {
            val response = withContext(Dispatchers.IO) {
                apiService.emailSignup(EmailSignupRequest(email, password, username))
            }
            if (response.status == "success") {
                EmailAuthResult.SignupSuccess(response.userId, response.email)
            } else {
                EmailAuthResult.Failure("Signup failed")
            }
        } catch (e: Exception) {
            EmailAuthResult.Failure(e.localizedMessage ?: "Signup failed")
        }
    }

    suspend fun emailVerify(email: String, code: String): EmailAuthResult {
        return try {
            val response = withContext(Dispatchers.IO) {
                apiService.emailVerify(EmailVerifyRequest(email, code))
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
            EmailAuthResult.Failure(e.localizedMessage ?: "Verification failed")
        }
    }

    suspend fun emailResendCode(email: String): EmailAuthResult {
        return try {
            val response = withContext(Dispatchers.IO) { apiService.emailResendCode(EmailResendRequest(email)) }
            EmailAuthResult.Message(response.message.ifEmpty { "Code resent" })
        } catch (e: Exception) {
            EmailAuthResult.Failure(e.localizedMessage ?: "Failed to resend code")
        }
    }

    suspend fun emailLogin(email: String, password: String): EmailAuthResult {
        return try {
            val response = withContext(Dispatchers.IO) {
                apiService.emailLogin(EmailLoginRequest(email, password))
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
            EmailAuthResult.Failure(e.localizedMessage ?: "Login failed")
        }
    }

    suspend fun emailForgotPassword(email: String): EmailAuthResult {
        return try {
            val response = withContext(Dispatchers.IO) { apiService.emailForgotPassword(EmailForgotRequest(email)) }
            EmailAuthResult.Message(response.message.ifEmpty { "If an account exists, a code has been sent" })
        } catch (e: Exception) {
            EmailAuthResult.Failure(e.localizedMessage ?: "Failed to send reset code")
        }
    }

    suspend fun emailResetPassword(email: String, code: String, newPassword: String): EmailAuthResult {
        return try {
            val response = withContext(Dispatchers.IO) {
                apiService.emailResetPassword(EmailResetPasswordRequest(email, code, newPassword))
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
            EmailAuthResult.Failure(e.localizedMessage ?: "Password reset failed")
        }
    }

    suspend fun setPassword(password: String): PasswordResult {
        return try {
            val bearer = getBearerToken() ?: return PasswordResult.Failure("Not authenticated")
            val response = withContext(Dispatchers.IO) { apiService.setPassword(bearer, SetPasswordRequest(password)) }
            if (response.status == "success") {
                dataStore.edit { prefs -> prefs[USER_HAS_PASSWORD] = true }
                PasswordResult.Success
            } else {
                PasswordResult.Failure(response.error ?: "Failed to set password")
            }
        } catch (e: Exception) {
            PasswordResult.Failure(e.localizedMessage ?: "Failed to set password")
        }
    }

    suspend fun changePassword(currentPassword: String, newPassword: String): PasswordResult {
        return try {
            val bearer = getBearerToken() ?: return PasswordResult.Failure("Not authenticated")
            val response = withContext(Dispatchers.IO) {
                apiService.changePassword(bearer, ChangePasswordRequest(currentPassword, newPassword))
            }
            if (response.status == "success") {
                response.authToken?.let { newToken ->
                    dataStore.edit { prefs -> prefs[AUTH_TOKEN] = newToken }
                }
                PasswordResult.Success
            } else {
                PasswordResult.Failure(response.error ?: "Failed to change password")
            }
        } catch (e: Exception) {
            PasswordResult.Failure(e.localizedMessage ?: "Failed to change password")
        }
    }

    suspend fun refreshProfile() {
        try {
            val bearer = getBearerToken() ?: return
            val username = dataStore.data.first()[USER_NAME] ?: return
            val response = withContext(Dispatchers.IO) { apiService.getProfile(bearer, username) }
            withContext(Dispatchers.IO) {
                dataStore.edit { prefs ->
                    prefs[USER_PHOTO_URL] = response.photoUrl ?: ""
                    prefs[USER_DISPLAY_NAME] = response.displayName ?: ""
                    prefs[USER_BANNER_URL] = response.bannerUrl ?: ""
                    prefs[USER_BIO] = response.bio ?: ""
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

    suspend fun logout() {
        dataStore.edit { prefs ->
            prefs[AUTH_STATUS] = "unauthenticated"
            prefs[AUTH_TOKEN] = ""
            prefs[PROFILE_COMPLETED] = false
            prefs[USER_ID] = ""
            prefs[USER_NAME] = "Student"
            prefs[USER_EMAIL] = ""
            prefs[USER_PHOTO_URL] = ""
            prefs[USER_DISPLAY_NAME] = ""
            prefs[USER_BANNER_URL] = ""
            prefs[USER_DOB] = ""
            prefs[USER_GENDER] = ""
            prefs[USER_CLASS] = ""
            prefs[USER_SUBJECTS] = ""
            prefs[USER_PRADESH] = ""
            prefs[USER_DISTRICT] = ""
            prefs[USER_SCHOOL] = ""
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
            prefs[USER_ACHIEVEMENT_BADGES] = ""
        }
    }
}

sealed class PasswordResult {
    object Success : PasswordResult()
    data class Failure(val message: String) : PasswordResult()
}

sealed class GithubSignInResult {
    data class Success(val isNewUser: Boolean) : GithubSignInResult()
    data class Failure(val message: String) : GithubSignInResult()
}

sealed class GoogleSignInResult {
    data class Success(val isNewUser: Boolean) : GoogleSignInResult()
    data class Failure(val message: String) : GoogleSignInResult()
}

sealed class EmailAuthResult {
    data class SignupSuccess(val userId: String, val email: String) : EmailAuthResult()
    data class VerifySuccess(val isNewUser: Boolean, val authToken: String, val user: UserProfileResponse) : EmailAuthResult()
    data class LoginSuccess(val isNewUser: Boolean, val authToken: String, val user: UserProfileResponse) : EmailAuthResult()
    data class ResetSuccess(val authToken: String, val user: UserProfileResponse) : EmailAuthResult()
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
    val dob: String,
    val gender: String?,
    val classLevel: String?,
    val subjects: String?,
    val pradesh: String?,
    val district: String?,
    val school: String?,
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