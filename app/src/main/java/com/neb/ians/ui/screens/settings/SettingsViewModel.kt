package com.neb.ians.ui.screens.settings

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.repository.SettingsRepository
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.UserProfileCache
import com.neb.ians.data.repository.PasswordResult
import com.neb.ians.data.api.UserProfileRequest
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class SettingsViewModel @Inject constructor(
    private val settingsRepository: SettingsRepository,
    private val authRepository: AuthRepository
) : ViewModel() {

    val isDarkMode: StateFlow<Boolean> = settingsRepository.isDarkMode
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), false)

    val userName: StateFlow<String> = settingsRepository.userName
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "Student")

    val notificationsEnabled: StateFlow<Boolean> = settingsRepository.notificationsEnabled
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), true)

    val downloadWifiOnly: StateFlow<Boolean> = settingsRepository.downloadWifiOnly
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), true)

    val userProfile: StateFlow<UserProfileCache?> = authRepository.userProfileFlow
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), null)

    val authState = authRepository.authState
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), com.neb.ians.data.repository.AuthState.Loading)

    fun setDarkMode(enabled: Boolean) {
        viewModelScope.launch { settingsRepository.setDarkMode(enabled) }
    }

    fun setUserName(name: String) {
        viewModelScope.launch { settingsRepository.setUserName(name) }
    }

    fun setNotificationsEnabled(enabled: Boolean) {
        viewModelScope.launch { settingsRepository.setNotificationsEnabled(enabled) }
    }

    fun setDownloadWifiOnly(enabled: Boolean) {
        viewModelScope.launch { settingsRepository.setDownloadWifiOnly(enabled) }
    }

    fun toggleProfileLock(isLocked: Boolean) {
        viewModelScope.launch {
            val current = authRepository.userProfileFlow.first()
            if (current != null) {
                val req = UserProfileRequest(
                    username = current.username,
                    email = current.email,
                    photoUrl = current.photoUrl,
                    displayName = current.displayName,
                    dob = current.dob,
                    gender = current.gender,
                    classLevel = current.classLevel,
                    subjects = current.subjects,
                    pradesh = current.pradesh,
                    district = current.district,
                    school = current.school,
                    isLocked = isLocked
                )
                authRepository.completeProfile(req)
            }
        }
    }

    fun logout() {
        viewModelScope.launch {
            authRepository.logout()
        }
    }

    private val _passwordState = MutableStateFlow<PasswordUiState>(PasswordUiState.Idle)
    val passwordState: StateFlow<PasswordUiState> = _passwordState.asStateFlow()

    fun setPassword(password: String) {
        viewModelScope.launch {
            _passwordState.value = PasswordUiState.Loading
            val result = authRepository.setPassword(password)
            _passwordState.value = when (result) {
                is PasswordResult.Success -> PasswordUiState.Success
                is PasswordResult.Failure -> PasswordUiState.Error(result.message)
            }
        }
    }

    fun changePassword(currentPassword: String, newPassword: String) {
        viewModelScope.launch {
            _passwordState.value = PasswordUiState.Loading
            val result = authRepository.changePassword(currentPassword, newPassword)
            _passwordState.value = when (result) {
                is PasswordResult.Success -> PasswordUiState.Success
                is PasswordResult.Failure -> PasswordUiState.Error(result.message)
            }
        }
    }

    fun resetPasswordState() {
        _passwordState.value = PasswordUiState.Idle
    }
}

sealed class PasswordUiState {
    object Idle : PasswordUiState()
    object Loading : PasswordUiState()
    object Success : PasswordUiState()
    data class Error(val message: String) : PasswordUiState()
}
