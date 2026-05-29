package com.neb.ians.ui.screens.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.UserProfileRequest
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.UserProfileCache
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class CompleteProfileUiState(
    val username: String = "",
    val dob: String = "",
    val gender: String = "Male",
    val classLevel: String = "Class 11",
    val subjects: List<String> = emptyList(),
    val pradesh: String = "Bagmati",
    val district: String = "Kathmandu",
    val school: String = "",
    val isLocked: Boolean = false,
    val isCheckingUsername: Boolean = false,
    val usernameAvailable: Boolean? = null,
    val usernameError: String? = null,
    val isSubmitting: Boolean = false,
    val submissionResult: Boolean? = null,
    val isEditing: Boolean = false
)

@OptIn(FlowPreview::class, ExperimentalCoroutinesApi::class)
@HiltViewModel
class CompleteProfileViewModel @Inject constructor(
    private val authRepository: AuthRepository,
    private val apiService: ApiService
) : ViewModel() {

    private val _uiState = MutableStateFlow(CompleteProfileUiState())
    val uiState: StateFlow<CompleteProfileUiState> = _uiState.asStateFlow()

    private val _usernameQuery = MutableStateFlow("")

    private var cachedUsername: String = ""

    init {
        viewModelScope.launch {
            val cached = authRepository.userProfileFlow.first()
            if (cached != null && cached.username.isNotEmpty()) {
                cachedUsername = cached.username
                _uiState.update { state ->
                    state.copy(
                        isEditing = true,
                        username = cached.username,
                        dob = cached.dob,
                        gender = cached.gender ?: "Male",
                        classLevel = cached.classLevel ?: "Class 11",
                        subjects = cached.subjects?.split(",")?.filter { it.isNotBlank() } ?: emptyList(),
                        pradesh = cached.pradesh ?: "Bagmati",
                        district = cached.district ?: "Kathmandu",
                        school = cached.school ?: "",
                        isLocked = cached.isLocked
                    )
                }
            }
        }

        viewModelScope.launch {
            _usernameQuery
                .debounce(500)
                .distinctUntilChanged()
                .mapLatest { query ->
                    if (query.length < 3) {
                        _uiState.update { it.copy(
                            usernameAvailable = null,
                            usernameError = if (query.isNotEmpty()) "Must be at least 3 characters" else null,
                            isCheckingUsername = false
                        )}
                        return@mapLatest
                    }
                    if (!query.matches(Regex("^[a-zA-Z0-9_]+$"))) {
                        _uiState.update { it.copy(
                            usernameAvailable = null,
                            usernameError = "Letters, numbers, underscores only",
                            isCheckingUsername = false
                        )}
                        return@mapLatest
                    }
                    if (query == cachedUsername) {
                        _uiState.update { it.copy(
                            usernameAvailable = null,
                            usernameError = null,
                            isCheckingUsername = false
                        )}
                        return@mapLatest
                    }
                    _uiState.update { it.copy(isCheckingUsername = true, usernameError = null) }
                    try {
                        val response = apiService.checkUsername(query)
                        _uiState.update { it.copy(usernameAvailable = response.available, isCheckingUsername = false) }
                    } catch (e: Exception) {
                        _uiState.update { it.copy(usernameAvailable = null, isCheckingUsername = false) }
                    }
                }
                .collect()
        }
    }

    fun onUsernameChange(value: String) {
        val trimmed = value.trim()
        _uiState.update { it.copy(username = trimmed) }
        _usernameQuery.value = trimmed
    }

    fun onDobChange(dob: String) {
        _uiState.update { it.copy(dob = dob) }
    }

    fun onGenderChange(gender: String) {
        _uiState.update { it.copy(gender = gender) }
    }

    fun onClassChange(classLevel: String) {
        _uiState.update { it.copy(classLevel = classLevel) }
    }

    fun onSubjectToggle(subject: String) {
        _uiState.update { state ->
            val current = state.subjects.toMutableList()
            if (current.contains(subject)) current.remove(subject) else current.add(subject)
            state.copy(subjects = current)
        }
    }

    fun onPradeshChange(pradesh: String) {
        _uiState.update { it.copy(pradesh = pradesh) }
    }

    fun onDistrictChange(district: String) {
        _uiState.update { it.copy(district = district) }
    }

    fun onSchoolChange(school: String) {
        _uiState.update { it.copy(school = school) }
    }

    fun onLockedChange(locked: Boolean) {
        _uiState.update { it.copy(isLocked = locked) }
    }

    fun submitProfile() {
        val state = _uiState.value
        if (state.isSubmitting) return

        _uiState.update { it.copy(isSubmitting = true, submissionResult = null) }

        viewModelScope.launch {
            val cachedUser = authRepository.userProfileFlow.first()
            val request = UserProfileRequest(
                username = state.username,
                email = cachedUser?.email,
                photoUrl = cachedUser?.photoUrl,
                displayName = cachedUser?.displayName ?: cachedUser?.email?.substringBefore("@"),
                dob = state.dob,
                gender = state.gender,
                classLevel = state.classLevel,
                subjects = state.subjects.joinToString(","),
                pradesh = state.pradesh,
                district = state.district,
                school = state.school,
                isLocked = state.isLocked
            )

            val success = authRepository.completeProfile(request)
            _uiState.update { it.copy(isSubmitting = false, submissionResult = success) }
        }
    }
}