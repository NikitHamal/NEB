package com.neb.ians.ui.components

import androidx.annotation.DrawableRes
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn

/**
 * The identity the next post will go out as. The home launcher and the composer share it,
 * so picking "anonymous" on the feed is still picked when the composer opens.
 */
object PostIdentityPreference {
    var anonymous by mutableStateOf(false)
}

@HiltViewModel
class ComposerIdentityViewModel @Inject constructor(
    authRepository: AuthRepository
) : ViewModel() {
    val userName: StateFlow<String> = authRepository.currentUserNameFlow
    val handle: StateFlow<String> = authRepository.currentUsernameHandleFlow
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "")
    val photoUrl: StateFlow<String?> = authRepository.currentUserPhotoUrlFlow
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), null)
    val anonTag: StateFlow<String> = authRepository.currentUserIdFlow
        .map { anonTagFor(it) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "Anonymous")
}

/**
 * The web feed's composer launcher: an identity dropdown, a prompt, and four tools.
 * Every part opens the full composer; nothing is typed here.
 */
@Composable
fun NebComposerLauncher(
    onOpen: () -> Unit,
    modifier: Modifier = Modifier,
    viewModel: ComposerIdentityViewModel = hiltViewModel()
) {
    val scheme = MaterialTheme.colorScheme
    val userName by viewModel.userName.collectAsStateWithLifecycle()
    val handle by viewModel.handle.collectAsStateWithLifecycle()
    val photoUrl by viewModel.photoUrl.collectAsStateWithLifecycle()
    val anonTag by viewModel.anonTag.collectAsStateWithLifecycle()

    Column(modifier = modifier.fillMaxWidth().padding(horizontal = 16.dp)) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            NebIdentityPicker(
                isAnonymous = PostIdentityPreference.anonymous,
                userName = userName,
                handle = handle,
                photoUrl = photoUrl,
                anonTag = anonTag,
                onSelect = { PostIdentityPreference.anonymous = it },
                showName = false,
                avatarSize = 32.dp
            )
            Box(
                modifier = Modifier
                    .weight(1f)
                    .heightIn(min = 44.dp)
                    .clip(RoundedCornerShape(22.dp))
                    .background(scheme.surfaceContainerLow)
                    .nebPressable(scale = 0.98f, onClick = onOpen)
                    .padding(horizontal = 16.dp),
                contentAlignment = Alignment.CenterStart
            ) {
                Text(
                    text = "Ask a question or share your notes",
                    style = MaterialTheme.typography.bodyMedium,
                    color = scheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
        Row(
            modifier = Modifier.padding(top = 4.dp, bottom = 4.dp),
            horizontalArrangement = Arrangement.spacedBy(2.dp)
        ) {
            LauncherTool(NebIcons.Image, "Attach photos", onOpen)
            LauncherTool(NebIcons.Video, "Add video or audio", onOpen)
            LauncherTool(NebIcons.Poll, "Ask a poll or quiz", onOpen)
            LauncherTool(NebIcons.Book, "Share a PDF or study notes", onOpen)
        }
    }
}

@Composable
private fun LauncherTool(@DrawableRes icon: Int, description: String, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .size(44.dp)
            .clip(RoundedCornerShape(16.dp))
            .nebPressable(scale = 0.9f, onClick = onClick)
            .semantics {
                role = Role.Button
                contentDescription = description
            },
        contentAlignment = Alignment.Center
    ) {
        NebIcon(icon, null, size = 22.dp, tint = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

/** A full-width hairline, the only separator between feed rows. */
@Composable
fun NebHairline(modifier: Modifier = Modifier) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .height(1.dp)
            .background(MaterialTheme.colorScheme.outlineVariant)
    )
}
