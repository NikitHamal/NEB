@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class
)

package com.neb.ians.ui.screens.forum

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.InlineImageTokens
import com.neb.ians.ui.components.NebChoiceSheet
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.ZoomableImageDialog

private enum class PostSheet { Category }

/**
 * Writing a discussion, laid out like the web composer on a phone.
 *
 * The header carries everything that decides where the post goes (who, which category)
 * and the round publish button, grey until the post is real. Under it the title and the
 * formatting row stay pinned while the body scrolls; polls, pictures and attachments
 * appear in the body only once the footer tools ask for them.
 */
@Composable
fun CreatePostScreen(
    onNavigateBack: () -> Unit,
    onPostCreated: () -> Unit,
    postId: String? = null,
    viewModel: CreatePostViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val userName by viewModel.userName.collectAsStateWithLifecycle()
    val userPhotoUrl by viewModel.userPhotoUrl.collectAsStateWithLifecycle()
    val userHandle by viewModel.userHandle.collectAsStateWithLifecycle()
    val anonTag by viewModel.anonTag.collectAsStateWithLifecycle()
    val isEditing = postId != null || uiState.isEditMode

    var zoomGallery by remember { mutableStateOf<Pair<List<String>, Int>?>(null) }
    val inlinePicker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickMultipleVisualMedia(InlineImageTokens.MAX_IMAGES_PER_CONTENT)
    ) { uris -> if (uris.isNotEmpty()) viewModel.addInlinePictures(uris) }
    var sheet by remember { mutableStateOf<PostSheet?>(null) }

    zoomGallery?.let { (urls, at) ->
        ZoomableImageDialog(imageUrls = urls, initialIndex = at, onDismiss = { zoomGallery = null })
    }

    val imagePicker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetMultipleContents()
    ) { uris -> uris?.forEach { viewModel.addImage(it) } }

    val mediaPicker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.OpenMultipleDocuments()
    ) { uris -> if (!uris.isNullOrEmpty()) viewModel.addMediaAttachments(uris) }

    LaunchedEffect(postId) {
        if (postId != null) viewModel.loadForEdit(postId)
    }

    val blocker = submitBlocker(uiState)
    val scheme = MaterialTheme.colorScheme

    Scaffold(
        containerColor = scheme.surface,
        contentWindowInsets = WindowInsets.statusBars
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .navigationBarsPadding()
                .imePadding()
        ) {
            ComposerHeader(
                showIdentity = !isEditing,
                userName = userName,
                userHandle = userHandle,
                userPhotoUrl = userPhotoUrl,
                anonTag = anonTag,
                isAnonymous = uiState.isAnonymous,
                category = uiState.effectiveCategory,
                canPublish = blocker == null,
                submitting = uiState.isSubmitting,
                onClose = onNavigateBack,
                onIdentitySelect = viewModel::setAnonymous,
                onCategoryClick = { sheet = PostSheet.Category },
                onPublish = { viewModel.submitPost(onSuccess = onPostCreated) }
            )

            if (uiState.isLoadingPost) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f),
                    contentAlignment = Alignment.Center
                ) {
                    NebLoader(size = NebLoaderSize.Screen)
                }
            } else {
                Column(modifier = Modifier.padding(horizontal = 16.dp)) {
                    ComposerTitleField(
                        value = uiState.title,
                        onValueChange = viewModel::onTitleChange,
                        enabled = !uiState.isSubmitting
                    )
                    ComposerFormatRow(
                        state = uiState,
                        viewModel = viewModel,
                        insertImageEnabled = !uiState.showPreview,
                        onInlineImage = {
                            inlinePicker.launch(androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
                        }
                    )
                }

                Column(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxWidth()
                        .verticalScroll(rememberScrollState())
                        .padding(horizontal = 16.dp, vertical = 12.dp),
                    verticalArrangement = Arrangement.spacedBy(14.dp)
                ) {
                    ComposerEditor(
                        state = uiState,
                        viewModel = viewModel,
                        onImageClick = { urls, at -> zoomGallery = urls to at }
                    )
                    if (!isEditing && uiState.pollEnabled) {
                        PostPollPanel(state = uiState, viewModel = viewModel)
                    }
                    ComposerImageStrip(state = uiState, viewModel = viewModel)
                    if (!isEditing) {
                        ComposerAttachmentList(state = uiState, viewModel = viewModel)
                    }
                    val message = uiState.error
                        ?: blocker?.takeIf { uiState.content.text.isNotBlank() }
                    if (message != null) {
                        Text(
                            text = message,
                            style = MaterialTheme.typography.bodySmall,
                            color = if (uiState.error != null) scheme.error else scheme.onSurfaceVariant,
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                }

                ComposerFooter(
                    state = uiState,
                    isEditing = isEditing,
                    onPhotos = { imagePicker.launch("image/*") },
                    onMedia = { mediaPicker.launch(arrayOf("video/*", "audio/*")) },
                    onDocument = {
                        mediaPicker.launch(arrayOf("application/pdf", "application/*", "text/*"))
                    },
                    onPoll = { viewModel.togglePoll(!uiState.pollEnabled) },
                    modifier = Modifier.background(scheme.surface)
                )
            }
        }
    }

    CreatePostSheets(
        sheet = sheet,
        state = uiState,
        userName = userName,
        viewModel = viewModel,
        onDismiss = { sheet = null }
    )
}

@Composable
private fun CreatePostSheets(
    sheet: PostSheet?,
    state: CreatePostUiState,
    userName: String,
    viewModel: CreatePostViewModel,
    onDismiss: () -> Unit
) {
    when (sheet) {
        PostSheet.Category -> {
            val known = CreatePostUiState.CATEGORIES
            val options = (known + listOfNotNull(
                state.customCategory.takeIf { state.isCustomCategory && it.isNotBlank() }
            )).distinct()
            NebChoiceSheet(
                title = "Category",
                options = options,
                selected = listOfNotNull(state.effectiveCategory.takeIf { it.isNotBlank() }),
                multiSelect = false,
                allowCustom = true,
                customPlaceholder = "Your own tag",
                onDismiss = onDismiss,
                onConfirm = { picked ->
                    val value = picked.firstOrNull().orEmpty().trim()
                    if (value.isNotBlank()) {
                        if (known.any { it.equals(value, ignoreCase = true) }) {
                            viewModel.onCategoryChange(known.first { it.equals(value, ignoreCase = true) })
                        } else {
                            viewModel.onCategoryChange(CreatePostUiState.OTHER_CATEGORY)
                            viewModel.onCustomCategoryChange(value)
                        }
                    }
                    onDismiss()
                }
            )
        }

        null -> Unit
    }
}

/** The single reason the post cannot go yet, said the way a person would say it. */
private fun submitBlocker(state: CreatePostUiState): String? = when {
    state.isLoadingPost -> "Loading your discussion"
    state.isSubmitting -> "Posting"
    state.content.text.isBlank() -> "Write something first"
    state.isCustomCategory && state.customCategory.isBlank() -> "Name your category"
    state.mediaAttachments.any { it.uploading } -> "An attachment is still uploading"
    else -> pollProblem(state)
}
