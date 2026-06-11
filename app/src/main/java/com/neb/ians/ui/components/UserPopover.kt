package com.neb.ians.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiUserPopup
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

data class UserPopoverState(
    val popup: ApiUserPopup? = null,
    val isLoading: Boolean = true,
    val error: String? = null,
    val isFollowBusy: Boolean = false
)

@HiltViewModel
class UserPopoverViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _state = MutableStateFlow(UserPopoverState())
    val state: StateFlow<UserPopoverState> = _state.asStateFlow()

    fun load(username: String) {
        _state.value = UserPopoverState(isLoading = true)
        viewModelScope.launch {
            try {
                val bearer = authRepository.getBearerToken()
                val popup = apiService.getUserPopup(bearer, username)
                _state.value = UserPopoverState(popup = popup, isLoading = false)
            } catch (e: Exception) {
                _state.value = UserPopoverState(isLoading = false, error = "Couldn't load profile")
            }
        }
    }

    fun toggleFollow() {
        val current = _state.value.popup ?: return
        if (current.isSelf || _state.value.isFollowBusy) return
        viewModelScope.launch {
            _state.value = _state.value.copy(isFollowBusy = true)
            try {
                val bearer = authRepository.getBearerToken() ?: return@launch
                val result = apiService.toggleFollow(bearer, current.id)
                _state.value = _state.value.copy(
                    popup = current.copy(
                        isFollowing = result.isFollowing,
                        followerCount = result.followerCount ?: current.followerCount
                    ),
                    isFollowBusy = false
                )
            } catch (e: Exception) {
                _state.value = _state.value.copy(isFollowBusy = false)
            }
        }
    }
}

/**
 * Mini-profile popover, shown when long-pressing a username or avatar.
 * Pixel-parity with the web's `/ajax/user-popup/` hover card: avatar,
 * display name + role badge, @username, bio, class level, posts/replies/
 * followers stats and a Follow button.
 */
@Composable
fun UserPopoverDialog(
    username: String,
    onDismiss: () -> Unit,
    onViewProfile: (String) -> Unit,
    viewModel: UserPopoverViewModel = hiltViewModel()
) {
    val state by viewModel.state.collectAsState()

    LaunchedEffect(username) { viewModel.load(username) }

    Dialog(onDismissRequest = onDismiss) {
        Surface(
            shape = WebPanelShape,
            color = MaterialTheme.colorScheme.surfaceContainerLowest,
            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
            modifier = Modifier.fillMaxWidth()
        ) {
            when {
                state.isLoading -> Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(180.dp),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator(modifier = Modifier.size(28.dp), strokeWidth = 3.dp)
                }
                state.error != null || state.popup == null -> Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(140.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = state.error ?: "Couldn't load profile",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                else -> {
                    val popup = state.popup!!
                    Column(modifier = Modifier.padding(20.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Avatar(
                                name = popup.displayName.ifBlank { popup.username },
                                imageUrl = popup.photoUrl,
                                size = 52.dp
                            )
                            Spacer(modifier = Modifier.width(12.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Text(
                                        text = popup.displayName.ifBlank { popup.username },
                                        style = MaterialTheme.typography.titleMedium,
                                        fontWeight = FontWeight.Bold,
                                        maxLines = 1,
                                        overflow = TextOverflow.Ellipsis,
                                        modifier = Modifier.weight(1f, fill = false)
                                    )
                                    popup.badgeInfo?.let { badge ->
                                        Spacer(modifier = Modifier.width(6.dp))
                                        RoleBadgeChip(badge.type, badge.label, badge.color)
                                    }
                                }
                                Text(
                                    text = "@${popup.username}",
                                    style = MaterialTheme.typography.labelMedium,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis
                                )
                            }
                        }

                        if (popup.bio.isNotBlank()) {
                            Spacer(modifier = Modifier.height(10.dp))
                            Text(
                                text = popup.bio,
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                maxLines = 3,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                        if (popup.classLevel.isNotBlank()) {
                            Spacer(modifier = Modifier.height(6.dp))
                            Text(
                                text = popup.classLevel,
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }

                        Spacer(modifier = Modifier.height(14.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceEvenly
                        ) {
                            PopoverStat(value = popup.postCount, label = "Posts")
                            PopoverStat(value = popup.replyCount, label = "Replies")
                            PopoverStat(value = popup.followerCount, label = "Followers")
                        }

                        Spacer(modifier = Modifier.height(14.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            if (!popup.isSelf) {
                                Button(
                                    onClick = { viewModel.toggleFollow() },
                                    enabled = !state.isFollowBusy,
                                    shape = WebPillShape,
                                    modifier = Modifier.weight(1f),
                                    colors = if (popup.isFollowing) ButtonDefaults.buttonColors(
                                        containerColor = MaterialTheme.colorScheme.surfaceContainerHigh,
                                        contentColor = MaterialTheme.colorScheme.onSurface
                                    ) else ButtonDefaults.buttonColors()
                                ) {
                                    Text(if (popup.isFollowing) "Following" else "Follow")
                                }
                            }
                            OutlinedButton(
                                onClick = {
                                    onDismiss()
                                    onViewProfile(popup.username)
                                },
                                shape = WebPillShape,
                                modifier = Modifier.weight(1f)
                            ) {
                                Text("View profile")
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun PopoverStat(value: Int, label: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(
            text = compactCount(value),
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.ExtraBold
        )
        Text(
            text = label,
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center
        )
    }
}

/**
 * Compact role badge chip matching the web `.role-badge` (22px circle,
 * 15px filled icon, 15% alpha background of the role color).
 */
@Composable
fun RoleBadgeChip(type: String, label: String, colorHex: String?, modifier: Modifier = Modifier) {
    val color = remember(colorHex) { parseHexColor(colorHex) ?: Color(0xFF1B9AF0) }
    Surface(
        modifier = modifier.size(22.dp),
        shape = CircleShape,
        color = color.copy(alpha = 0.15f)
    ) {
        Box(contentAlignment = Alignment.Center) {
            Text(
                text = badgeGlyph(type),
                style = MaterialTheme.typography.labelSmall,
                color = color,
                fontWeight = FontWeight.Bold
            )
        }
    }
}

internal fun badgeGlyph(type: String): String = when (type) {
    "bot" -> "\u2726"          // ✦ AI sparkle
    "admin" -> "\u265B"        // ♛ crown
    "moderator" -> "\u2694"    // shield-ish
    "teacher" -> "\uD83C\uDF93" // 🎓
    "institution" -> "\uD83C\uDFDB" // 🏛
    "explorer" -> "\u2316"     // ⌖ explore
    "verified" -> "\u2713"     // ✓
    else -> "\u2713"
}

internal fun parseHexColor(hex: String?): Color? {
    if (hex.isNullOrBlank()) return null
    return try {
        val cleaned = hex.removePrefix("#")
        val value = cleaned.toLong(16)
        when (cleaned.length) {
            6 -> Color(0xFF000000 or value)
            8 -> Color(value)
            else -> null
        }
    } catch (e: Exception) {
        null
    }
}
