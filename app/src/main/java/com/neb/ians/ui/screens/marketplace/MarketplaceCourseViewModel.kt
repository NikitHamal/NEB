package com.neb.ians.ui.screens.marketplace

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiCreatorResource
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiMarketplaceCourseDetail
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.MarketplaceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class MarketplaceCourseUiState(
    val courseId: String = "",
    val isLoading: Boolean = true,
    val isSubmittingPurchase: Boolean = false,
    val error: String? = null,
    val isAuthenticated: Boolean = false,
    val isOwner: Boolean = false,
    val course: ApiMarketplaceCourseDetail? = null,
    val courseResources: List<ApiCreatorResource> = emptyList()
)

@HiltViewModel
class MarketplaceCourseViewModel @Inject constructor(
    private val repository: MarketplaceRepository,
    private val authRepository: AuthRepository,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val courseId: String = savedStateHandle.get<String>("courseId").orEmpty()

    private val _uiState = MutableStateFlow(MarketplaceCourseUiState(courseId = courseId))
    val uiState: StateFlow<MarketplaceCourseUiState> = _uiState.asStateFlow()

    private val _purchaseSheetVisible = MutableStateFlow(false)
    val purchaseSheetVisible: StateFlow<Boolean> = _purchaseSheetVisible.asStateFlow()

    private val _purchaseSubmitting = MutableStateFlow(false)
    val purchaseSubmitting: StateFlow<Boolean> = _purchaseSubmitting.asStateFlow()

    private val _snackbarMessage = MutableStateFlow<String?>(null)
    val snackbarMessage: StateFlow<String?> = _snackbarMessage.asStateFlow()

    fun load() {
        if (courseId.isBlank()) {
            _uiState.update { it.copy(isLoading = false, error = "This offering is not available") }
            return
        }
        _uiState.update { it.copy(isLoading = it.course == null, error = null) }

        viewModelScope.launch {
            val signedIn = !authRepository.getBearerToken().isNullOrBlank()
            repository.course(courseId).fold(
                onSuccess = { detail ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            error = null,
                            isAuthenticated = signedIn,
                            isOwner = detail.page?.isMine == true,
                            course = detail,
                            courseResources = detail.resources
                        )
                    }
                    if (signedIn && !detail.isFree && !detail.hasAccess) refreshPurchaseStatus()
                },
                onFailure = { failure ->
                    _uiState.update {
                        it.copy(isLoading = false, error = ApiErrorMapper.mapException(failure))
                    }
                }
            )
        }
    }

    /** The buyer-scoped view of the same course, so the gate is server-authentic. */
    private fun refreshPurchaseStatus() {
        viewModelScope.launch {
            repository.purchaseStatus(courseId).onSuccess { status ->
                _uiState.update { current ->
                    val course = current.course ?: return@update current
                    current.copy(
                        course = course.copy(
                            hasAccess = status.hasAccess,
                            accessReason = status.accessReason,
                            purchaseStatus = status.purchaseStatus,
                            price = status.price.ifBlank { course.price }
                        )
                    )
                }
            }
        }
    }

    fun openPurchaseSheet() {
        if (!_uiState.value.isAuthenticated) return
        _purchaseSheetVisible.value = true
    }

    fun dismissPurchaseSheet() {
        _purchaseSheetVisible.value = false
    }

    fun clearSnackbar() {
        _snackbarMessage.value = null
    }

    fun submitPurchase(transactionId: String, proofFile: java.io.File?) {
        viewModelScope.launch {
            _purchaseSubmitting.value = true
            repository.submitPurchase(courseId, transactionId, proofFile).fold(
                onSuccess = { response ->
                    _purchaseSubmitting.value = false
                    _purchaseSheetVisible.value = false
                    _snackbarMessage.value = response.message.ifBlank {
                        "Payment submitted for verification."
                    }
                    _uiState.update { current ->
                        val course = current.course
                        if (course == null) {
                            current
                        } else {
                            current.copy(
                                course = course.copy(
                                    hasAccess = response.hasAccess,
                                    accessReason = response.accessReason,
                                    purchaseStatus = response.purchaseStatus.ifBlank { "pending" }
                                )
                            )
                        }
                    }
                },
                onFailure = { failure ->
                    _purchaseSubmitting.value = false
                    _snackbarMessage.value = ApiErrorMapper.mapException(failure)
                }
            )
        }
    }
}
