package com.neb.ians.ui.screens.settings

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.EmailAuthResult
import com.neb.ians.data.repository.EmailChangeResult
import com.neb.ians.data.repository.PasswordResult
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

// ---------------------------------------------------------------------------
// Account security -- the one place an account's email and password change.
//
// Both are guarded the way the rest of the industry guards them. A new address
// is not believed until a code sent *to it* comes back, so a borrowed session
// cannot quietly move the mailbox that resets the password. A new password
// needs the old one, or -- when there is no old one to remember -- a code to
// the address already on file.
// ---------------------------------------------------------------------------

/** Which panel of the screen is up. The screen is a small flow, not a list. */
enum class SecurityStep {
    Overview,

    /** New address plus the current password, before any code goes out. */
    EmailForm,

    /** The six digits sent to the new address. */
    EmailCode,

    /** Current password (when there is one) and the new one, twice. */
    PasswordForm,

    /** The code sent to the address on file, plus the password to set. */
    ForgotCode
}

data class AccountSecurityUiState(
    val loading: Boolean = true,
    val loadError: String? = null,
    val email: String = "",
    val emailVerified: Boolean = false,
    val hasPassword: Boolean = false,
    /** An address waiting on its code. Empty when no change is in flight. */
    val pendingEmail: String = "",
    val step: SecurityStep = SecurityStep.Overview,
    val busy: Boolean = false,
    val error: String? = null,
    val notice: String? = null,
    /** Stamped every time a code goes out, so the screen can run a cooldown. */
    val codeSentAt: Long = 0L
)

@HiltViewModel
class AccountSecurityViewModel @Inject constructor(
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _state = MutableStateFlow(AccountSecurityUiState())
    val state: StateFlow<AccountSecurityUiState> = _state.asStateFlow()

    /**
     * What the email change was asked for with, so "Resend code" can repeat the
     * request without asking for the password again. Deliberately not in the UI
     * state: nothing on screen should be able to read a password back out.
     */
    private var pendingCredentials: Pair<String, String>? = null

    init {
        load()
    }

    fun load() {
        viewModelScope.launch {
            _state.update { it.copy(loading = true, loadError = null) }
            val info = authRepository.accountSecurity()
            if (info == null) {
                _state.update {
                    it.copy(loading = false, loadError = "Couldn't load your account details.")
                }
                return@launch
            }
            _state.update {
                it.copy(
                    loading = false,
                    loadError = null,
                    email = info.email,
                    emailVerified = info.emailVerified,
                    hasPassword = info.hasPassword,
                    pendingEmail = info.pendingEmail
                )
            }
        }
    }

    // -- Moving between panels -------------------------------------------------

    fun openEmailForm() = goTo(SecurityStep.EmailForm)

    fun openEmailCode() = goTo(SecurityStep.EmailCode)

    fun openPasswordForm() = goTo(SecurityStep.PasswordForm)

    fun back() = goTo(SecurityStep.Overview)

    private fun goTo(step: SecurityStep) {
        _state.update { it.copy(step = step, error = null, notice = null) }
    }

    fun clearError() {
        _state.update { it.copy(error = null) }
    }

    fun clearNotice() {
        _state.update { it.copy(notice = null) }
    }

    // -- Email -----------------------------------------------------------------

    fun requestEmailChange(newEmail: String, password: String) {
        val address = newEmail.trim()
        if (address.isBlank()) {
            _state.update { it.copy(error = "Enter the new email address.") }
            return
        }
        if (_state.value.hasPassword && password.isBlank()) {
            _state.update { it.copy(error = "Enter your current password.") }
            return
        }
        submit(
            work = { authRepository.requestEmailChange(address, password) },
            onResult = { result ->
                when (result) {
                    is EmailChangeResult.CodeSent -> {
                        pendingCredentials = address to password
                        _state.update {
                            it.copy(
                                pendingEmail = result.pendingEmail.ifBlank { address },
                                step = SecurityStep.EmailCode,
                                codeSentAt = System.currentTimeMillis(),
                                notice = null,
                                error = null
                            )
                        }
                    }
                    is EmailChangeResult.Changed -> onEmailChanged(result.email)
                    is EmailChangeResult.Failure ->
                        _state.update { it.copy(error = result.message) }
                }
            }
        )
    }

    fun resendEmailCode() {
        val saved = pendingCredentials
        val pending = _state.value.pendingEmail
        when {
            saved != null -> requestEmailChange(saved.first, saved.second)
            // Coming back to a change started earlier: the address survived on
            // the server, the password never left the last screen. Only an
            // account without a password can repeat the request unprompted.
            pending.isNotBlank() && !_state.value.hasPassword ->
                requestEmailChange(pending, "")
            else -> _state.update {
                it.copy(
                    step = SecurityStep.EmailForm,
                    error = "Enter your password again to send a new code."
                )
            }
        }
    }

    fun confirmEmailChange(code: String) {
        if (code.length < 6) {
            _state.update { it.copy(error = "Enter the 6-digit code.") }
            return
        }
        submit(
            work = { authRepository.confirmEmailChange(code) },
            onResult = { result ->
                when (result) {
                    is EmailChangeResult.Changed -> onEmailChanged(result.email)
                    is EmailChangeResult.CodeSent ->
                        _state.update { it.copy(codeSentAt = System.currentTimeMillis()) }
                    is EmailChangeResult.Failure ->
                        _state.update { it.copy(error = result.message) }
                }
            }
        )
    }

    fun cancelEmailChange() {
        submit(
            work = { authRepository.cancelEmailChange() },
            onResult = { cancelled ->
                pendingCredentials = null
                _state.update {
                    if (cancelled) {
                        it.copy(
                            pendingEmail = "",
                            step = SecurityStep.Overview,
                            notice = "Email change cancelled.",
                            error = null
                        )
                    } else {
                        it.copy(error = "Couldn't cancel the change. Try again.")
                    }
                }
            }
        )
    }

    private fun onEmailChanged(email: String) {
        pendingCredentials = null
        _state.update {
            it.copy(
                email = email,
                emailVerified = true,
                pendingEmail = "",
                step = SecurityStep.Overview,
                error = null,
                notice = "Email updated. You've been signed out everywhere else."
            )
        }
    }

    // -- Password --------------------------------------------------------------

    fun submitPassword(currentPassword: String, newPassword: String, confirmPassword: String) {
        val hasPassword = _state.value.hasPassword
        if (hasPassword && currentPassword.isBlank()) {
            _state.update { it.copy(error = "Enter your current password.") }
            return
        }
        if (newPassword.length < 8) {
            _state.update { it.copy(error = "Use at least 8 characters.") }
            return
        }
        if (newPassword != confirmPassword) {
            _state.update { it.copy(error = "The two passwords don't match.") }
            return
        }
        submit(
            work = {
                if (hasPassword) {
                    authRepository.changePassword(currentPassword, newPassword)
                } else {
                    authRepository.setPassword(newPassword)
                }
            },
            onResult = { result ->
                when (result) {
                    is PasswordResult.Success -> _state.update {
                        it.copy(
                            hasPassword = true,
                            step = SecurityStep.Overview,
                            error = null,
                            notice = if (hasPassword) {
                                "Password changed."
                            } else {
                                "Password set. You can sign in with it from now on."
                            }
                        )
                    }
                    is PasswordResult.Failure ->
                        _state.update { it.copy(error = result.message) }
                }
            }
        )
    }

    // -- Forgotten password ----------------------------------------------------

    /**
     * The way through when the current password is the thing that's missing: a
     * code to the address on file, then a new password in the same step.
     */
    fun startForgotPassword() {
        val email = _state.value.email
        if (email.isBlank()) {
            _state.update {
                it.copy(error = "Add an email to your account first, then reset your password.")
            }
            return
        }
        submit(
            work = { authRepository.emailForgotPassword(email) },
            onResult = { result ->
                when (result) {
                    is EmailAuthResult.Failure ->
                        _state.update { it.copy(error = result.message) }
                    else -> _state.update {
                        it.copy(
                            step = SecurityStep.ForgotCode,
                            codeSentAt = System.currentTimeMillis(),
                            error = null,
                            notice = null
                        )
                    }
                }
            }
        )
    }

    fun submitForgotReset(code: String, newPassword: String, confirmPassword: String) {
        if (code.length < 6) {
            _state.update { it.copy(error = "Enter the 6-digit code.") }
            return
        }
        if (newPassword.length < 8) {
            _state.update { it.copy(error = "Use at least 8 characters.") }
            return
        }
        if (newPassword != confirmPassword) {
            _state.update { it.copy(error = "The two passwords don't match.") }
            return
        }
        val email = _state.value.email
        submit(
            work = { authRepository.emailResetPassword(email, code, newPassword) },
            onResult = { result ->
                when (result) {
                    is EmailAuthResult.ResetSuccess -> _state.update {
                        it.copy(
                            hasPassword = true,
                            step = SecurityStep.Overview,
                            error = null,
                            notice = "Password reset. You're still signed in here."
                        )
                    }
                    is EmailAuthResult.Failure ->
                        _state.update { it.copy(error = result.message) }
                    else -> _state.update {
                        it.copy(error = "Couldn't reset the password. Try again.")
                    }
                }
            }
        )
    }

    /** One busy flag, one error slot: every call above is the same shape. */
    private fun <T> submit(work: suspend () -> T, onResult: (T) -> Unit) {
        if (_state.value.busy) return
        viewModelScope.launch {
            _state.update { it.copy(busy = true, error = null) }
            val result = work()
            onResult(result)
            _state.update { it.copy(busy = false) }
        }
    }
}
