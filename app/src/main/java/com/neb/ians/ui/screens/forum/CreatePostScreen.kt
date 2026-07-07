package com.neb.ians.ui.screens.forum

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.outlined.AddPhotoAlternate
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.Poll
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import com.neb.ians.ui.components.MarkdownText
import com.neb.ians.ui.components.MarkdownToolbar
import com.neb.ians.ui.components.MentionSuggestions
import com.neb.ians.ui.components.MentionsVisualTransformation
import com.neb.ians.ui.components.resolveMediaUrl
import com.neb.ians.ui.components.WebPillShape


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CreatePostScreen(
    onNavigateBack: () -> Unit,
    onPostCreated: () -> Unit,
    postId: String? = null,
    viewModel: CreatePostViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val isEditing = postId != null || uiState.isEditMode
    var categoryExpanded by remember { mutableStateOf(false) }
    var durationExpanded by remember { mutableStateOf(false) }

    val imagePicker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri -> viewModel.addImage(uri) }

    LaunchedEffect(postId) {
        if (postId != null) viewModel.loadForEdit(postId)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(if (isEditing) "Edit Discussion" else "New Discussion") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
    ) { paddingValues ->
        if (uiState.isLoadingPost) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator()
            }
        } else {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .verticalScroll(rememberScrollState())
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp)
            ) {
            // ----- Title -----
            OutlinedTextField(
                value = uiState.title,
                onValueChange = viewModel::onTitleChange,
                label = { Text("Title") },
                placeholder = { Text("Enter a descriptive title") },
                supportingText = { Text("${uiState.title.length}/$MAX_POST_TITLE") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp),
                enabled = !uiState.isSubmitting
            )

            // ----- Category -----
            ExposedDropdownMenuBox(
                expanded = categoryExpanded,
                onExpandedChange = { categoryExpanded = !categoryExpanded }
            ) {
                OutlinedTextField(
                    value = if (uiState.isCustomCategory) CreatePostUiState.OTHER_CATEGORY else uiState.selectedCategory,
                    onValueChange = {},
                    readOnly = true,
                    label = { Text("Category") },
                    trailingIcon = {
                        ExposedDropdownMenuDefaults.TrailingIcon(expanded = categoryExpanded)
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .menuAnchor(),
                    shape = RoundedCornerShape(12.dp),
                    enabled = !uiState.isSubmitting
                )
                ExposedDropdownMenu(
                    expanded = categoryExpanded,
                    onDismissRequest = { categoryExpanded = false }
                ) {
                    (CreatePostUiState.CATEGORIES + CreatePostUiState.OTHER_CATEGORY).forEach { category ->
                        DropdownMenuItem(
                            text = { Text(category) },
                            onClick = {
                                viewModel.onCategoryChange(category)
                                categoryExpanded = false
                            },
                            contentPadding = ExposedDropdownMenuDefaults.ItemContentPadding
                        )
                    }
                }
            }
            if (uiState.isCustomCategory) {
                OutlinedTextField(
                    value = uiState.customCategory,
                    onValueChange = viewModel::onCustomCategoryChange,
                    label = { Text("Custom category") },
                    placeholder = { Text("e.g. Nepali") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    enabled = !uiState.isSubmitting
                )
            }

            // ----- Write / Preview toggle -----
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                SegmentPill("Write", selected = !uiState.showPreview) { viewModel.togglePreview(false) }
                SegmentPill("Preview", selected = uiState.showPreview) { viewModel.togglePreview(true) }
            }

            if (!uiState.showPreview) {
                Column {
                    MarkdownToolbar(
                        value = uiState.content,
                        onValueChange = viewModel::onContentChange,
                        modifier = Modifier
                            .fillMaxWidth()
                            .horizontalScroll(rememberScrollState())
                    )
                    OutlinedTextField(
                        value = uiState.content,
                        onValueChange = viewModel::onContentChange,
                        label = { Text("Content") },
                        placeholder = { Text("Write your discussion content... Use @ to mention users.") },
                        supportingText = { Text("${uiState.content.text.length}/$MAX_POST_CONTENT") },
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(min = 180.dp),
                        shape = RoundedCornerShape(12.dp),
                        enabled = !uiState.isSubmitting,
                        visualTransformation = MentionsVisualTransformation(MaterialTheme.colorScheme.primary)
                    )
                    MentionSuggestions(
                        users = uiState.mentionSuggestions,
                        onSelect = viewModel::selectMention,
                        modifier = Modifier.padding(top = 4.dp)
                    )
                }
            } else {
                Surface(
                    modifier = Modifier
                        .fillMaxWidth()
                        .heightIn(min = 180.dp),
                    shape = RoundedCornerShape(12.dp),
                    color = MaterialTheme.colorScheme.surfaceContainerLow,
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                ) {
                    Box(modifier = Modifier.padding(14.dp)) {
                        if (uiState.content.text.isBlank()) {
                            Text(
                                text = "Nothing to preview yet.",
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        } else {
                            MarkdownText(markdown = uiState.content.text)
                        }
                    }
                }
            }

            // ----- Images -----
            Column {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = "Images",
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.SemiBold,
                        modifier = Modifier.weight(1f)
                    )
                    Text(
                        text = "${uiState.activeImageCount}/$MAX_POST_IMAGES",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Spacer(modifier = Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    uiState.visibleExistingImages.forEach { image ->
                        Box {
                            AsyncImage(
                                model = resolveMediaUrl(image.imageUrl),
                                contentDescription = null,
                                modifier = Modifier
                                    .size(80.dp)
                                    .clip(RoundedCornerShape(8.dp)),
                                contentScale = ContentScale.Crop
                            )
                            Box(
                                modifier = Modifier
                                    .align(Alignment.TopEnd)
                                    .padding(3.dp)
                                    .size(20.dp)
                                    .clip(CircleShape)
                                    .background(Color.Black.copy(alpha = 0.6f))
                                    .clickable { viewModel.removeExistingImage(image.id) },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Filled.Close,
                                    contentDescription = "Remove image",
                                    modifier = Modifier.size(13.dp),
                                    tint = Color.White
                                )
                            }
                        }
                    }
                    uiState.images.forEach { uri ->
                        Box {
                            AsyncImage(
                                model = uri,
                                contentDescription = null,
                                modifier = Modifier
                                    .size(80.dp)
                                    .clip(RoundedCornerShape(8.dp)),
                                contentScale = ContentScale.Crop
                            )
                            Box(
                                modifier = Modifier
                                    .align(Alignment.TopEnd)
                                    .padding(3.dp)
                                    .size(20.dp)
                                    .clip(CircleShape)
                                    .background(Color.Black.copy(alpha = 0.6f))
                                    .clickable { viewModel.removeImage(uri) },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Filled.Close,
                                    contentDescription = "Remove image",
                                    modifier = Modifier.size(13.dp),
                                    tint = Color.White
                                )
                            }
                        }
                    }
                    if (uiState.activeImageCount < MAX_POST_IMAGES) {
                        Box(
                            modifier = Modifier
                                .size(80.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(MaterialTheme.colorScheme.surfaceContainerHigh)
                                .clickable(enabled = !uiState.isSubmitting) { imagePicker.launch("image/*") },
                            contentAlignment = Alignment.Center
                        ) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Icon(
                                    imageVector = Icons.Outlined.AddPhotoAlternate,
                                    contentDescription = "Add image",
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                                Text(
                                    text = "Add",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                }
            }

            // ----- Poll builder -----
            if (!isEditing) {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    color = MaterialTheme.colorScheme.surfaceContainerLow,
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            imageVector = Icons.Outlined.Poll,
                            contentDescription = null,
                            modifier = Modifier.size(18.dp),
                            tint = MaterialTheme.colorScheme.primary
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = "Add poll",
                            style = MaterialTheme.typography.titleSmall,
                            fontWeight = FontWeight.SemiBold,
                            modifier = Modifier.weight(1f)
                        )
                        Switch(
                            checked = uiState.pollEnabled,
                            onCheckedChange = viewModel::togglePoll,
                            enabled = !uiState.isSubmitting
                        )
                    }

                    if (uiState.pollEnabled) {
                        Spacer(modifier = Modifier.height(10.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            SegmentPill("Voting", selected = uiState.pollType == "voting") {
                                viewModel.onPollTypeChange("voting")
                            }
                            SegmentPill("MCQ Quiz", selected = uiState.pollType == "mcq") {
                                viewModel.onPollTypeChange("mcq")
                            }
                        }

                        Spacer(modifier = Modifier.height(10.dp))
                        OutlinedTextField(
                            value = uiState.pollQuestion,
                            onValueChange = viewModel::onPollQuestionChange,
                            label = { Text("Question") },
                            placeholder = { Text("Ask something...") },
                            singleLine = true,
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(12.dp),
                            enabled = !uiState.isSubmitting
                        )

                        Spacer(modifier = Modifier.height(8.dp))
                        uiState.pollOptions.forEachIndexed { index, option ->
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                modifier = Modifier.padding(vertical = 3.dp)
                            ) {
                                OutlinedTextField(
                                    value = option.text,
                                    onValueChange = { viewModel.onPollOptionChange(index, it) },
                                    placeholder = { Text("Option ${index + 1}") },
                                    singleLine = true,
                                    modifier = Modifier.weight(1f),
                                    shape = RoundedCornerShape(12.dp),
                                    enabled = !uiState.isSubmitting
                                )
                                if (uiState.pollType == "mcq") {
                                    IconButton(onClick = { viewModel.togglePollOptionCorrect(index) }) {
                                        Icon(
                                            imageVector = if (option.isCorrect) Icons.Filled.CheckCircle
                                            else Icons.Outlined.CheckCircle,
                                            contentDescription = if (option.isCorrect) "Correct answer" else "Mark as correct",
                                            tint = if (option.isCorrect) Color(0xFF16A34A)
                                            else MaterialTheme.colorScheme.onSurfaceVariant
                                        )
                                    }
                                }
                                if (uiState.pollOptions.size > 2) {
                                    IconButton(onClick = { viewModel.removePollOption(index) }) {
                                        Icon(
                                            imageVector = Icons.Filled.Close,
                                            contentDescription = "Remove option",
                                            modifier = Modifier.size(18.dp),
                                            tint = MaterialTheme.colorScheme.onSurfaceVariant
                                        )
                                    }
                                }
                            }
                        }
                        if (uiState.pollOptions.size < 6) {
                            Text(
                                text = "+ Add option",
                                style = MaterialTheme.typography.labelLarge,
                                color = MaterialTheme.colorScheme.primary,
                                fontWeight = FontWeight.SemiBold,
                                modifier = Modifier
                                    .clip(WebPillShape)
                                    .clickable(enabled = !uiState.isSubmitting) { viewModel.addPollOption() }
                                    .padding(horizontal = 10.dp, vertical = 6.dp)
                            )
                        }

                        if (uiState.pollType == "voting") {
                            Spacer(modifier = Modifier.height(6.dp))
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text(
                                    text = "Allow multiple selections",
                                    style = MaterialTheme.typography.bodyMedium,
                                    modifier = Modifier.weight(1f)
                                )
                                Switch(
                                    checked = uiState.pollAllowMultiple,
                                    onCheckedChange = viewModel::onPollAllowMultipleChange,
                                    enabled = !uiState.isSubmitting
                                )
                            }
                        } else {
                            Spacer(modifier = Modifier.height(8.dp))
                            OutlinedTextField(
                                value = uiState.pollExplanation,
                                onValueChange = viewModel::onPollExplanationChange,
                                label = { Text("Explanation (optional)") },
                                placeholder = { Text("Shown after answering") },
                                modifier = Modifier.fillMaxWidth(),
                                minLines = 2,
                                shape = RoundedCornerShape(12.dp),
                                enabled = !uiState.isSubmitting
                            )
                        }

                        Spacer(modifier = Modifier.height(10.dp))
                        ExposedDropdownMenuBox(
                            expanded = durationExpanded,
                            onExpandedChange = { durationExpanded = !durationExpanded }
                        ) {
                            OutlinedTextField(
                                value = CreatePostUiState.POLL_DURATIONS
                                    .firstOrNull { it.first == uiState.pollDurationMs }?.second ?: "No expiry",
                                onValueChange = {},
                                readOnly = true,
                                label = { Text("Duration") },
                                trailingIcon = {
                                    ExposedDropdownMenuDefaults.TrailingIcon(expanded = durationExpanded)
                                },
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .menuAnchor(),
                                shape = RoundedCornerShape(12.dp),
                                enabled = !uiState.isSubmitting
                            )
                            ExposedDropdownMenu(
                                expanded = durationExpanded,
                                onDismissRequest = { durationExpanded = false }
                            ) {
                                CreatePostUiState.POLL_DURATIONS.forEach { (millis, label) ->
                                    DropdownMenuItem(
                                        text = { Text(label) },
                                        onClick = {
                                            viewModel.onPollDurationChange(millis)
                                            durationExpanded = false
                                        },
                                        contentPadding = ExposedDropdownMenuDefaults.ItemContentPadding
                                    )
                                }
                            }
                        }
                    }
                }
            }
            }

            // ----- Error -----
            uiState.error?.let { error ->
                Text(
                    text = error,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.error
                )
            }

            // ----- Submit -----
            Button(
                onClick = { viewModel.submitPost(onSuccess = onPostCreated) },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(52.dp),
                shape = RoundedCornerShape(50),
                enabled = uiState.title.isNotBlank() && uiState.content.text.isNotBlank() &&
                    (!uiState.isCustomCategory || uiState.customCategory.isNotBlank()) &&
                    !uiState.isSubmitting && !uiState.isLoadingPost
            ) {
                if (uiState.isSubmitting) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(20.dp),
                        strokeWidth = 2.dp,
                        color = MaterialTheme.colorScheme.onPrimary
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                }
                Text(if (uiState.isSubmitting) { if (isEditing) "Saving..." else "Posting..." } else { if (isEditing) "Save Changes" else "Post Discussion" })
            }
            Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
}

/** Pill segment used for Write/Preview and Voting/MCQ toggles. */
@Composable
internal fun SegmentPill(label: String, selected: Boolean, onClick: () -> Unit) {
    Surface(
        shape = WebPillShape,
        color = if (selected) MaterialTheme.colorScheme.secondaryContainer
        else MaterialTheme.colorScheme.surfaceContainerHigh,
        modifier = Modifier.clip(WebPillShape).clickable(onClick = onClick)
    ) {
        Text(
            text = label,
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 7.dp),
            style = MaterialTheme.typography.labelMedium,
            fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Medium,
            color = if (selected) MaterialTheme.colorScheme.onSecondaryContainer
            else MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}
