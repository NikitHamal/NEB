package com.neb.ians.ui.screens.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.EmailAuthResult
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

enum class EmailAuthMode { SignIn, CreateAccount }

sealed interface EmailAuthEvent {
    data object GoHome : EmailAuthEvent
    data object GoOnboarding : EmailAuthEvent
    data class GoVerify(val email: String) : EmailAuthEvent
    data class GoForgotPassword(val email: String) : EmailAuthEvent
}

data class EmailAuthUiState(
    val mode: EmailAuthMode = EmailAuthMode.SignIn,
    val identifier: String = "",
    val password: String = "",
    val isSubmitting: Boolean = false,
    val formError: String? = null,
    val identifierError: String? = null,
    val passwordError: String? = null,
    val event: EmailAuthEvent? = null
) {
    val canSubmit: Boolean
        get() = !isSubmitting && identifier.isNotBlank() && password.isNotBlank()
}

@HiltViewModel
class EmailAuthViewModel @Inject constructor(
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(EmailAuthUiState())
    val uiState: StateFlow<EmailAuthUiState> = _uiState.asStateFlow()

    fun setMode(mode: EmailAuthMode) {
        _uiState.update {
            if (it.mode == mode) it else it.copy(
                mode = mode,
                formError = null,
                identifierError = null,
                passwordError = null
            )
        }
    }

    fun toggleMode() {
        setMode(if (_uiState.value.mode == EmailAuthMode.SignIn) EmailAuthMode.CreateAccount else EmailAuthMode.SignIn)
    }

    fun onIdentifierChange(value: String) {
        _uiState.update { it.copy(identifier = value.trim(), identifierError = null, formError = null) }
    }

    fun onPasswordChange(value: String) {
        _uiState.update { it.copy(password = value, passwordError = null, formError = null) }
    }

    fun requestForgotPassword() {
        val email = _uiState.value.identifier.takeIf { it.contains("@") } ?: ""
        _uiState.update { it.copy(event = EmailAuthEvent.GoForgotPassword(email)) }
    }

    fun consumeEvent() {
        _uiState.update { it.copy(event = null) }
    }

    fun submit() {
        val state = _uiState.value
        if (state.isSubmitting) return
        if (state.mode == EmailAuthMode.SignIn) signIn(state) else createAccount(state)
    }

    private fun signIn(state: EmailAuthUiState) {
        val identifier = state.identifier.trim()
        val password = state.password.trim()
        if (identifier.isEmpty() || password.isEmpty()) {
            _uiState.update {
                it.copy(
                    identifierError = if (identifier.isEmpty()) "Enter your email or username" else null,
                    passwordError = if (password.isEmpty()) "Enter your password" else null
                )
            }
            return
        }

        _uiState.update { it.copy(isSubmitting = true, formError = null) }
        viewModelScope.launch {
            when (val result = authRepository.emailLogin(identifier, password)) {
                is EmailAuthResult.LoginSuccess -> _uiState.update {
                    it.copy(
                        isSubmitting = false,
                        event = if (result.isNewUser) EmailAuthEvent.GoOnboarding else EmailAuthEvent.GoHome
                    )
                }
                is EmailAuthResult.Failure -> {
                    val needsVerification = result.message.contains("verify", ignoreCase = true)
                    _uiState.update {
                        it.copy(
                            isSubmitting = false,
                            formError = result.message,
                            event = if (needsVerification && identifier.contains("@")) {
                                EmailAuthEvent.GoVerify(identifier)
                            } else {
                                null
                            }
                        )
                    }
                }
                else -> _uiState.update {
                    it.copy(isSubmitting = false, formError = "Unexpected response. Please try again.")
                }
            }
        }
    }

    private fun createAccount(state: EmailAuthUiState) {
        val email = state.identifier.trim()
        val password = state.password.trim()

        val emailError = when {
            email.isEmpty() -> "Enter your email address"
            !email.contains("@") || !email.contains(".") -> "That does not look like an email address"
            else -> null
        }
        val passwordError = when {
            password.isEmpty() -> "Choose a password"
            password.length < 8 -> "Use at least 8 characters"
            else -> null
        }
        if (emailError != null || passwordError != null) {
            _uiState.update { it.copy(identifierError = emailError, passwordError = passwordError) }
            return
        }

        _uiState.update { it.copy(isSubmitting = true, formError = null) }
        viewModelScope.launch {
            val username = email.substringBefore("@").filter { it.isLetterOrDigit() || it == '_' }.ifBlank { "nebian" }
            when (val result = authRepository.emailSignup(email, password, username)) {
                is EmailAuthResult.SignupSuccess -> _uiState.update {
                    it.copy(isSubmitting = false, event = EmailAuthEvent.GoVerify(email))
                }
                is EmailAuthResult.Failure -> _uiState.update {
                    it.copy(isSubmitting = false, formError = result.message)
                }
                else -> _uiState.update {
                    it.copy(isSubmitting = false, formError = "Could not create the account. Please try again.")
                }
            }
        }
    }
}
