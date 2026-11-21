package com.neb.ians.ui.screens.credits

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiConvertPointsRequest
import com.neb.ians.data.api.ApiCreditBalanceResponse
import com.neb.ians.data.api.ApiCreditTransaction
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.SecurePrefs
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import javax.inject.Inject

data class CreditUiState(
    val isLoading: Boolean = true,
    val balance: ApiCreditBalanceResponse = ApiCreditBalanceResponse(),
    val transactions: List<ApiCreditTransaction> = emptyList(),
    val isConverting: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class NebyCreditsViewModel @Inject constructor(
    application: Application,
    private val apiService: ApiService
) : AndroidViewModel(application) {

    private val _uiState = MutableStateFlow(CreditUiState())
    val uiState: StateFlow<CreditUiState> = _uiState.asStateFlow()

    init {
        loadData()
    }

    fun loadData() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val (bal, hist) = withContext(Dispatchers.IO) {
                    val token = SecurePrefs.getAuthToken(getApplication()) ?: ""
                    val bearer = "Bearer $token"
                    kotlinx.coroutines.coroutineScope {
                        val b = kotlinx.coroutines.async { apiService.getCreditBalance(bearer) }
                        val h = kotlinx.coroutines.async { apiService.getCreditHistory(bearer) }
                        b.await() to h.await()
                    }
                }
                _uiState.update { it.copy(isLoading = false, balance = bal, transactions = hist.transactions) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = "Failed to load Neby Credits info") }
            }
        }
    }

    fun convertPoints(points: Int, onSuccess: (String) -> Unit, onError: (String) -> Unit) {
        viewModelScope.launch {
            _uiState.update { it.copy(isConverting = true) }
            try {
                val token = withContext(Dispatchers.IO) { SecurePrefs.getAuthToken(getApplication()) } ?: ""
                val resp = apiService.convertPointsToCredits("Bearer $token", ApiConvertPointsRequest(points))
                if (resp.error != null) {
                    onError(resp.error)
                } else {
                    onSuccess(resp.message.ifBlank { "Converted successfully!" })
                    loadData()
                }
            } catch (e: Exception) {
                onError("Failed to convert points")
            } finally {
                _uiState.update { it.copy(isConverting = false) }
            }
        }
    }
}
