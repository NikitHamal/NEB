@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class
)

package com.neb.ians.ui.screens.forum

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material.icons.automirrored.rounded.Send
import androidx.compose.material.icons.rounded.Category
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.InlineImageTokens
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebChoiceSheet
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.NebSectionLabel
import com.neb.ians.ui.components.NebSelectField
import com.neb.ians.ui.components.rememberInlineImageFieldHandle
import com.neb.ians.ui.components.ZoomableImageDialog

private enum class PostSheet { Category, PollDuration }

/**
 * Writing a discussion, in the order it is written.
 *
 * The title and what you want to say come first and fill the screen. Everything
 * that decorates the post — pictures, files, a poll, a name to hide — sits
 * below in its own quiet group, and the button that sends it stays out of the
 * way at the bottom, grey with a reason next to it until the post is real.
 */
@Composable
fun CreatePostScreen(
    onNavigateBack: () -> Unit,
    onPostCreated: () -> Unit,
    postId: String? = null,
    viewModel: CreatePostViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val isEditing = postId != null || uiState.isEditMode

    val inlineHandle = rememberInlineImageFieldHandle()
    var pendingInlineCount by remember { mutableIntStateOf(0) }
    var zoomImageUrl by remember { mutableStateOf<String?>(null) }
    var sheet by remember { mutableStateOf<PostSheet?>(null) }

    zoomImageUrl?.let { url ->
        ZoomableImageDialog(imageUrl = url, onDismiss = { zoomImageUrl = null })
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

    val blocker = submitBlocker(uiState, pendingInlineCount)

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        text = if (isEditing) "Edit discussion" else "New discussion",
                        style = MaterialTheme.typography.titleLargeEmphasized,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Rounded.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        bottomBar = {
            CreatePostActionBar(
                isEditing = isEditing,
                submitting = uiState.isSubmitting,
                blocker = blocker,
                error = uiState.error,
                onSubmit = { viewModel.submitPost(onSuccess = onPostCreated) }
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        if (uiState.isLoadingPost) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentAlignment = Alignment.Center
            ) {
                NebLoader(size = NebLoaderSize.Screen)
            }
            return@Scaffold
        }

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            PostTextField(
                value = uiState.title,
                onValueChange = viewModel::onTitleChange,
                label = "Title",
                placeholder = "What is this about?",
                supporting = "${uiState.title.length} of $MAX_POST_TITLE",
                enabled = !uiState.isSubmitting
            )

            NebSelectField(
                label = "Category",
                values = listOfNotNull(uiState.effectiveCategory.takeIf { it.isNotBlank() }),
                placeholder = "Pick one, or name your own",
                icon = Icons.Rounded.Category,
                onClick = { sheet = PostSheet.Category }
            )

            PostEditorPanel(
                state = uiState,
                viewModel = viewModel,
                handle = inlineHandle,
                pendingInlineCount = pendingInlineCount,
                onPendingCountChange = { pendingInlineCount = it },
                onImageClick = { zoomImageUrl = it }
            )

            Spacer(modifier = Modifier.height(2.dp))
            NebSectionLabel(text = "Add to your post")

            PostImagesPanel(
                state = uiState,
                viewModel = viewModel,
                onAddImages = { imagePicker.launch("image/*") }
            )

            if (!isEditing) {
                PostAttachmentsPanel(
                    state = uiState,
                    viewModel = viewModel,
                    onPick = {
                        mediaPicker.launch(
                            arrayOf("video/*", "audio/*", "application/*", "text/*")
                        )
                    }
                )
                PostPollPanel(
                    state = uiState,
                    viewModel = viewModel,
                    onOpenDuration = { sheet = PostSheet.PollDuration }
                )
                PostAnonymousPanel(state = uiState, viewModel = viewModel)
            }

            Spacer(modifier = Modifier.height(12.dp))
        }
    }

    CreatePostSheets(
        sheet = sheet,
        state = uiState,
        viewModel = viewModel,
        onDismiss = { sheet = null }
    )
}

@Composable
private fun CreatePostSheets(
    sheet: PostSheet?,
    state: CreatePostUiState,
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
                subtitle = "Where this discussion belongs",
                options = options,
                selected = listOfNotNull(state.effectiveCategory.takeIf { it.isNotBlank() }),
                multiSelect = false,
                allowCustom = true,
                customPlaceholder = "Name your own",
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

        PostSheet.PollDuration -> NebChoiceSheet(
            title = "Closes",
            subtitle = "When the poll stops taking answers",
            options = CreatePostUiState.POLL_DURATIONS.map { it.second },
            selected = listOfNotNull(
                CreatePostUiState.POLL_DURATIONS.firstOrNull { it.first == state.pollDurationMs }?.second
            ),
            multiSelect = false,
            onDismiss = onDismiss,
            onConfirm = { picked ->
                val label = picked.firstOrNull()
                CreatePostUiState.POLL_DURATIONS.firstOrNull { it.second == label }?.let {
                    viewModel.onPollDurationChange(it.first)
                }
                onDismiss()
            }
        )

        null -> Unit
    }
}

@Composable
private fun CreatePostActionBar(
    isEditing: Boolean,
    submitting: Boolean,
    blocker: String?,
    error: String?,
    onSubmit: () -> Unit
) {
    Surface(color = MaterialTheme.colorScheme.surface) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .navigationBarsPadding()
                .imePadding()
                .padding(horizontal = 16.dp, vertical = 10.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            NebButton(
                text = if (isEditing) "Save changes" else "Post discussion",
                onClick = onSubmit,
                icon = Icons.AutoMirrored.Rounded.Send,
                size = NebButtonSize.Hero,
                fillWidth = true,
                loading = submitting,
                enabled = blocker == null
            )
            AnimatedVisibility(visible = error != null || blocker != null) {
                Text(
                    text = error ?: blocker.orEmpty(),
                    style = MaterialTheme.typography.bodySmall,
                    color = if (error != null) MaterialTheme.colorScheme.error
                    else MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.fillMaxWidth()
                )
            }
        }
    }
}

/** The single reason the post cannot go yet, said the way a person would say it. */
private fun submitBlocker(state: CreatePostUiState, pendingInline: Int): String? = when {
    state.isLoadingPost -> "Loading your discussion"
    state.title.isBlank() -> "Give it a title"
    state.content.text.isBlank() -> "Write something first"
    state.isCustomCategory && state.customCategory.isBlank() -> "Name your category"
    pendingInline > 0 || InlineImageTokens.hasPending(state.content.text) ->
        "An image is still uploading"
    state.mediaAttachments.any { it.uploading } -> "An attachment is still uploading"
    else -> pollProblem(state)
}
