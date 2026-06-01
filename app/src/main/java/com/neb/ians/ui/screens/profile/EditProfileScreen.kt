package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import javax.inject.Inject
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.data.repository.AuthRepository

data class EditProfileUiState(
    val profile: UserProfileResponse? = null,
    val isLoading: Boolean = true,
    val error: String? = null
)

@HiltViewModel
class EditProfileViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(EditProfileUiState())
    val uiState: StateFlow<EditProfileUiState> = _uiState.asStateFlow()

    fun loadProfile() {
        viewModelScope.launch {
            try {
                val token = authRepository.getBearerToken()
                val username = authRepository.userProfileFlow.first()?.username ?: return@launch
                val profile = apiService.getProfile(token, username)
                _uiState.value = _uiState.value.copy(profile = profile, isLoading = false)
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(error = e.localizedMessage, isLoading = false)
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EditProfileScreen(
    onNavigateBack: () -> Unit,
    viewModel: EditProfileViewModel = hiltViewModel()
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Edit Profile") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Box(modifier = Modifier.fillMaxSize().padding(padding)) {
            Text("Edit Profile - Coming Soon", modifier = Modifier.padding(16.dp))
        }
    }
}