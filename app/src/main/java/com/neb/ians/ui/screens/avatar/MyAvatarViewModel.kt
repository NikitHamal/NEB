package com.neb.ians.ui.screens.avatar

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.AvatarStyleUpdateRequest
import com.neb.ians.data.repository.AvatarRepository
import com.neb.ians.ui.avatar.blobatar.BlobatarOpts
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class MyAvatarUiState(
    val username: String = "",
    val loading: Boolean = false,
    val saving: Boolean = false,
    val dirty: Boolean = false,
    val usePp: Boolean = false,
    val anim: String = "",
    val shape: String = "",
    val expression: String = "",
    val color: String = "",
    val bgcolor: String = "",
    val eyecolor: String = "",
    val message: String? = null
) {
    fun toOpts(): BlobatarOpts = BlobatarOpts(
        expression = expression.ifBlank { null },
        shape = shape.ifBlank { null },
        color = color.ifBlank { null },
        bgColor = bgcolor.ifBlank { null },
        eyeColor = eyecolor.ifBlank { null },
        anim = anim.ifBlank { null }
    )
}

val ANIM_OPTIONS = listOf(
    "" to "None",
    "bob" to "Bob",
    "wave" to "Wave",
    "spin" to "Spin",
    "pulse" to "Pulse"
)

val SHAPE_OPTIONS = listOf(
    "" to "Auto",
    "round" to "Round",
    "organic" to "Organic",
    "boxy" to "Boxy",
    "capsule" to "Capsule",
    "nub" to "Nub",
    "cloud" to "Cloud",
    "droplet" to "Droplet",
    "hexagon" to "Hexagon",
    "sun" to "Sun",
    "triangle" to "Triangle"
)

val EXPRESSION_OPTIONS = listOf(
    "" to "None",
    "idle" to "Idle",
    "happy" to "Happy",
    "sad" to "Sad",
    "mad" to "Mad",
    "surprised" to "Surprised",
    "wink" to "Wink",
    "sleepy" to "Sleepy",
    "smug" to "Smug",
    "unsure" to "Unsure",
    "scared" to "Scared",
    "love" to "Love",
    "shy" to "Shy",
    "sick" to "Sick",
    "thinking" to "Thinking"
)

val HEAD_PRESETS = listOf(
    "#7a5af5", "#2563eb", "#0ea5e9", "#10b981", "#f59e0b",
    "#ef4444", "#ec4899", "#8b5cf6", "#14b8a6", "#f97316"
)

val EYE_PRESETS = listOf(
    "#2b2b2b", "#0a1c4d", "#4b5563", "#1d4ed8", "#065f46",
    "#7c2d12", "#701a75", "#312e81"
)

@HiltViewModel
class MyAvatarViewModel @Inject constructor(
    private val avatarRepository: AvatarRepository,
    private val authRepository: com.neb.ians.data.repository.AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(MyAvatarUiState())
    val uiState: StateFlow<MyAvatarUiState> = _uiState.asStateFlow()

    fun clearMessage() = _uiState.update { it.copy(message = null) }

    fun load() {
        viewModelScope.launch {
            _uiState.update { it.copy(loading = true) }
            val username = try {
                authRepository.currentUsernameHandleFlow.first()
            } catch (_: Exception) { "" }
            _uiState.update { it.copy(username = username) }
            avatarRepository.getStyle()
                .onSuccess { style ->
                    _uiState.update {
                        it.copy(
                            loading = false,
                            usePp = style.usePp,
                            anim = style.anim,
                            shape = style.shape,
                            expression = style.expression,
                            color = style.color,
                            bgcolor = style.bgcolor,
                            eyecolor = style.eyecolor,
                            dirty = false
                        )
                    }
                }
                .onFailure { e ->
                    _uiState.update {
                        it.copy(loading = false, message = e.message ?: "Could not load your avatar style")
                    }
                }
        }
    }

    fun setAnim(v: String) = mutate { copy(anim = v) }
    fun setShape(v: String) = mutate { copy(shape = v) }
    fun setExpression(v: String) = mutate { copy(expression = v) }
    fun setColor(v: String?) = mutate { copy(color = v ?: "") }
    fun setEyeColor(v: String?) = mutate { copy(eyecolor = v ?: "") }
    fun setUsePp(v: Boolean) = mutate { copy(usePp = v) }

    private fun mutate(block: MyAvatarUiState.() -> MyAvatarUiState) =
        _uiState.update { it.block().copy(dirty = true) }

    fun save() {
        val s = _uiState.value
        if (!s.dirty || s.saving) return
        viewModelScope.launch {
            _uiState.update { it.copy(saving = true) }
            val req = AvatarStyleUpdateRequest(
                anim = s.anim,
                shape = s.shape,
                expression = s.expression,
                color = s.color,
                bgcolor = s.bgcolor,
                eyecolor = s.eyecolor,
                usePp = s.usePp
            )
            avatarRepository.updateStyle(req)
                .onSuccess { res ->
                    _uiState.update {
                        it.copy(
                            saving = false,
                            dirty = false,
                            message = if (res.status == "success") "Avatar style saved — live everywhere!" else (res.error ?: "Saved")
                        )
                    }
                }
                .onFailure { e ->
                    _uiState.update {
                        it.copy(saving = false, message = e.message ?: "Could not save — try again")
                    }
                }
        }
    }
}
