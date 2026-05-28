package com.neb.ians.data.repository

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.*
import androidx.credentials.CredentialManager
import androidx.credentials.GetCredentialRequest
import androidx.credentials.CustomCredential
import com.google.android.libraries.identity.googleid.GetGoogleIdOption
import com.google.android.libraries.identity.googleid.GoogleIdTokenCredential
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.GoogleAuthRequest
import com.neb.ians.data.api.UserProfileRequest
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map
import java.io.IOException
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
        private val AUTH_STATUS = stringPreferencesKey("auth_status") // "unauthenticated", "guest", "authenticated"
        private val PROFILE_COMPLETED = booleanPreferencesKey("profile_completed")
        
        // User metadata keys cached locally
        val USER_ID = stringPreferencesKey("user_id")
        val USER_NAME = stringPreferencesKey("user_name")
        val USER_EMAIL = stringPreferencesKey("user_email")
        val USER_PHOTO_URL = stringPreferencesKey("user_photo_url")
        val USER_DISPLAY_NAME = stringPreferencesKey("user_display_name")
        val USER_DOB = stringPreferencesKey("user_dob")
        val USER_GENDER = stringPreferencesKey("user_gender")
        val USER_CLASS = stringPreferencesKey("user_class")
        val USER_SUBJECTS = stringPreferencesKey("user_subjects")
        val USER_PRADESH = stringPreferencesKey("user_pradesh")
        val USER_DISTRICT = stringPreferencesKey("user_district")
        val USER_SCHOOL = stringPreferencesKey("user_school")
        val USER_LOCKED = booleanPreferencesKey("user_locked")
    }

    val authState: Flow<AuthState> = dataStore.data.map { preferences ->
        val status = preferences[AUTH_STATUS] ?: "unauthenticated"
        val token = preferences[AUTH_TOKEN]
        val completed = preferences[PROFILE_COMPLETED] ?: false
        
        when (status) {
            "guest" -> AuthState.Guest
            "authenticated" -> {
                if (token != null) {
                    AuthState.Authenticated(token, completed)
                } else {
                    AuthState.Unauthenticated
                }
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
            displayName = preferences[USER_DISPLAY_NAME],
            dob = preferences[USER_DOB] ?: "",
            gender = preferences[USER_GENDER],
            classLevel = preferences[USER_CLASS],
            subjects = preferences[USER_SUBJECTS],
            pradesh = preferences[USER_PRADESH],
            district = preferences[USER_DISTRICT],
            school = preferences[USER_SCHOOL],
            isLocked = preferences[USER_LOCKED] ?: false
        )
    }

    // Modern Google One Tap login via Credential Manager
    suspend fun signInWithGoogle(context: Context): GoogleSignInResult {
        try {
            val credentialManager = CredentialManager.create(context)
            
            // Build the modern Google One Tap / Google ID request
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
                
                // Authenticate with server
                val response = apiService.authenticateGoogle(GoogleAuthRequest(idToken))
                
                // Cache user info in Datastore
                val user = response.user
                dataStore.edit { prefs ->
                    prefs[AUTH_TOKEN] = user.id
                    prefs[AUTH_STATUS] = "authenticated"
                    prefs[USER_ID] = user.id
                    prefs[USER_EMAIL] = user.email ?: ""
                    prefs[USER_PHOTO_URL] = user.photoUrl ?: ""
                    prefs[USER_DISPLAY_NAME] = user.displayName ?: ""
                    
                    if (response.isNewUser) {
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
                    }
                }
                
                return GoogleSignInResult.Success(response.isNewUser)
            } else {
                return GoogleSignInResult.Failure("Unsupported credential type")
            }
        } catch (e: Exception) {
            return GoogleSignInResult.Failure(e.localizedMessage ?: "Google Sign-In failed")
        }
    }

    suspend fun completeProfile(profile: UserProfileRequest): Boolean {
        return try {
            val token = tokenFlow.first() ?: return false
            val bearer = "Bearer $token"
            val response = apiService.updateProfile(bearer, profile)
            
            // Success, save details
            val user = response.user
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
            }
            true
        } catch (e: Exception) {
            false
        }
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
            prefs[USER_DOB] = ""
            prefs[USER_GENDER] = ""
            prefs[USER_CLASS] = ""
            prefs[USER_SUBJECTS] = ""
            prefs[USER_PRADESH] = ""
            prefs[USER_DISTRICT] = ""
            prefs[USER_SCHOOL] = ""
            prefs[USER_LOCKED] = false
        }
    }
}

sealed class GoogleSignInResult {
    data class Success(val isNewUser: Boolean) : GoogleSignInResult()
    data class Failure(val message: String) : GoogleSignInResult()
}

data class UserProfileCache(
    val id: String,
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
