package com.neb.ians.ui.screens.resource

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Download
import androidx.compose.material.icons.filled.MenuBook
import androidx.compose.material.icons.filled.OpenInNew
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.ThumbUp
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.Schedule
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiResourceComment
import com.neb.ians.ui.components.NebAvatar
import com.neb.ians.ui.components.NebCard
import com.neb.ians.ui.components.NebChip
import com.neb.ians.ui.components.NebTopBar
import com.neb.ians.util.formatTimeAgo
import com.neb.ians.util.getSubjectColor

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ResourceDetailScreen(
    onNavigateBack: () -> Unit,
    onOpenPdf: (resourceId: String, fileUrl: String, title: String) -> Unit,
    isDark: Boolean = false,
    onToggleTheme: () -> Unit = {},
    viewModel: ResourceDetailViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current

    fun openExternal(url: String) {
        if (url.isBlank()) return
        runCatching { context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url))) }
    }

    fun share(resource: ApiResource) {
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_SUBJECT, resource.title)
            putExtra(Intent.EXTRA_TEXT, "${resource.title}\nhttps://nebians.consica.com.np/resource/${resource.id}/")
        }
        runCatching { context.startActivity(Intent.createChooser(intent, "Share")) }
    }

    Scaffold(
        topBar = {
            NebTopBar(
                showBrand = false,
                title = "Resource",
                onBack = onNavigateBack,
                isDark = isDark,
                onToggleTheme = onToggleTheme
            )
        },
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
    ) { padding ->
        when {
            uiState.isLoading -> Box(
                Modifier.fillMaxSize().padding(padding),
                contentAlignment = Alignment.Center
            ) { CircularProgressIndicator() }

            uiState.resource == null -> Box(
                Modifier.fillMaxSize().padding(padding),
                contentAlignment = Alignment.Center
            ) {
                Text(uiState.error ?: "Resource not found", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }

            else -> {
                val resource = uiState.resource!!
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(top = padding.calculateTopPadding())
                        .verticalScroll(rememberScrollState())
                        .padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    HeroCard(
                        resource = resource,
                        isLiked = uiState.isLiked,
                        likeCount = uiState.likeCount,
                        canLike = uiState.isAuthenticated,
                        onLike = viewModel::toggleLike,
                        onShare = { share(resource) }
                    )

                    val isPdf = resource.type.contains("pdf", true) ||
                        resource.fileUrl.endsWith(".pdf", true)
                    val isImage = resource.type.contains("image", true) ||
                        Regex("\\.(png|jpe?g|gif|webp|bmp)$", RegexOption.IGNORE_CASE).containsMatchIn(resource.fileUrl)

                    if (resource.fileUrl.isNotBlank()) {
                        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                            if (isPdf) {
                                Button(
                                    onClick = { onOpenPdf(resource.id, resource.fileUrl, resource.title) },
                                    modifier = Modifier.weight(1f),
                                    shape = RoundedCornerShape(24.dp)
                                ) {
                                    Icon(Icons.Filled.MenuBook, null, modifier = Modifier.size(18.dp))
                                    Spacer(Modifier.width(8.dp))
                                    Text("Read")
                                }
                            } else {
                                Button(
                                    onClick = { openExternal(resource.fileUrl) },
                                    modifier = Modifier.weight(1f),
                                    shape = RoundedCornerShape(24.dp)
                                ) {
                                    Icon(Icons.Filled.OpenInNew, null, modifier = Modifier.size(18.dp))
                                    Spacer(Modifier.width(8.dp))
                                    Text("Open")
                                }
                            }
                            OutlinedButton(
                                onClick = { openExternal(resource.fileUrl) },
                                modifier = Modifier.weight(1f),
                                shape = RoundedCornerShape(24.dp)
                            ) {
                                Icon(Icons.Filled.Download, null, modifier = Modifier.size(18.dp))
                                Spacer(Modifier.width(8.dp))
                                Text("Download")
                            }
                        }
                    }

                    if (isImage && resource.fileUrl.isNotBlank()) {
                        AsyncImage(
                            model = resource.fileUrl,
                            contentDescription = resource.title,
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(16.dp))
                        )
                    }

                    CommentsSection(
                        comments = uiState.comments,
                        loading = uiState.commentsLoading,
                        isAuthenticated = uiState.isAuthenticated,
                        currentUserId = uiState.currentUserId,
                        draft = uiState.commentDraft,
                        posting = uiState.isPostingComment,
                        onDraftChange = viewModel::onCommentDraftChange,
                        onPost = viewModel::postComment,
                        onDelete = viewModel::deleteComment
                    )

                    Spacer(Modifier.height(24.dp))
                }
            }
        }
    }
}

@Composable
private fun HeroCard(
    resource: ApiResource,
    isLiked: Boolean,
    likeCount: Int,
    canLike: Boolean,
    onLike: () -> Unit,
    onShare: () -> Unit
) {
    val subjectColor = Color(getSubjectColor(resource.subject.split(",").first().trim()))
    NebCard(modifier = Modifier.fillMaxWidth()) {
        Column {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(8.dp)
                    .background(subjectColor)
            )
            Column(modifier = Modifier.padding(20.dp)) {
                FlowChips(resource = resource, subjectColor = subjectColor)
                Spacer(Modifier.height(12.dp))
                Text(
                    text = resource.title,
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Spacer(Modifier.height(10.dp))
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(14.dp)
                ) {
                    MetaItem(Icons.Outlined.Schedule, formatTimeAgo(resource.addedAt))
                    MetaItem(Icons.Outlined.Visibility, "${resource.viewCount} views")
                    if (resource.fileSize > 0) {
                        MetaItem(null, fileSizeHuman(resource.fileSize))
                    }
                }
                if (resource.description.isNotBlank()) {
                    Spacer(Modifier.height(14.dp))
                    Text(
                        text = resource.description,
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                if (!resource.authorName.isNullOrBlank()) {
                    Spacer(Modifier.height(12.dp))
                    Text(
                        text = "By ${resource.authorName}",
                        style = MaterialTheme.typography.labelLarge,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Spacer(Modifier.height(16.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp), verticalAlignment = Alignment.CenterVertically) {
                    LikeButton(isLiked = isLiked, count = likeCount, enabled = canLike, onClick = onLike)
                    FilledTonalIconButton(onClick = onShare) {
                        Icon(Icons.Filled.Share, contentDescription = "Share", modifier = Modifier.size(20.dp))
                    }
                }
            }
        }
    }
}

@Composable
private fun FlowChips(resource: ApiResource, subjectColor: Color) {
    Row(
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(50))
                .background(subjectColor.copy(alpha = 0.12f))
                .padding(horizontal = 12.dp, vertical = 5.dp)
        ) {
            Text(
                resource.subject.split(",").first().trim(),
                color = subjectColor,
                fontSize = 12.sp,
                fontWeight = FontWeight.SemiBold
            )
        }
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(50))
                .background(MaterialTheme.colorScheme.secondaryContainer)
                .padding(horizontal = 12.dp, vertical = 5.dp)
        ) {
            Text(
                resource.type,
                color = MaterialTheme.colorScheme.onSecondaryContainer,
                fontSize = 12.sp,
                fontWeight = FontWeight.SemiBold
            )
        }
        if (resource.gradeLevel.isNotBlank()) {
            Text(
                resource.gradeLevel,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                fontSize = 12.sp
            )
        }
    }
}

@Composable
private fun MetaItem(icon: androidx.compose.ui.graphics.vector.ImageVector?, text: String) {
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
        if (icon != null) {
            Icon(icon, null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(15.dp))
        }
        Text(text, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

@Composable
private fun LikeButton(isLiked: Boolean, count: Int, enabled: Boolean, onClick: () -> Unit) {
    val container = if (isLiked) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceContainerHigh
    val content = if (isLiked) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
    Row(
        modifier = Modifier
            .clip(RoundedCornerShape(50))
            .background(container)
            .then(if (enabled) Modifier.clickableNoRipple(onClick) else Modifier)
            .padding(horizontal = 16.dp, vertical = 9.dp),
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            if (isLiked) Icons.Filled.ThumbUp else Icons.Outlined.ThumbUp,
            null, tint = content, modifier = Modifier.size(18.dp)
        )
        Text(count.toString(), color = content, fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
    }
}

@Composable
private fun CommentsSection(
    comments: List<ApiResourceComment>,
    loading: Boolean,
    isAuthenticated: Boolean,
    currentUserId: String?,
    draft: String,
    posting: Boolean,
    onDraftChange: (String) -> Unit,
    onPost: () -> Unit,
    onDelete: (String) -> Unit
) {
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Text(
            "Comments (${comments.size})",
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold
        )

        if (isAuthenticated) {
            NebCard(modifier = Modifier.fillMaxWidth()) {
                Row(
                    modifier = Modifier.padding(8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    OutlinedTextField(
                        value = draft,
                        onValueChange = onDraftChange,
                        modifier = Modifier.weight(1f),
                        placeholder = { Text("Add a comment...") },
                        maxLines = 4,
                        shape = RoundedCornerShape(20.dp),
                        keyboardOptions = KeyboardOptions.Default,
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Color.Transparent,
                            unfocusedBorderColor = Color.Transparent
                        )
                    )
                    IconButton(onClick = onPost, enabled = draft.isNotBlank() && !posting) {
                        Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Post comment")
                    }
                }
            }
        }

        when {
            loading -> Box(Modifier.fillMaxWidth().padding(16.dp), contentAlignment = Alignment.Center) {
                CircularProgressIndicator(modifier = Modifier.size(24.dp))
            }
            comments.isEmpty() -> Column(
                modifier = Modifier.fillMaxWidth().padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Icon(
                    Icons.Outlined.ChatBubbleOutline, null,
                    tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f),
                    modifier = Modifier.size(32.dp)
                )
                Text(
                    "No comments yet. Be the first!",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            else -> comments.forEach { comment ->
                CommentItem(
                    comment = comment,
                    canDelete = comment.userId == currentUserId,
                    onDelete = { onDelete(comment.id) }
                )
            }
        }
    }
}

@Composable
private fun CommentItem(comment: ApiResourceComment, canDelete: Boolean, onDelete: () -> Unit) {
    Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
        NebAvatar(photoUrl = comment.userPhotoUrl, name = comment.userName, size = 36.dp)
        Column(modifier = Modifier.weight(1f)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                Text(
                    comment.userName,
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Text(
                    formatTimeAgo(comment.createdAt),
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(Modifier.weight(1f))
                if (canDelete) {
                    Icon(
                        Icons.Filled.Delete,
                        contentDescription = "Delete",
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(16.dp).clickableNoRipple(onDelete)
                    )
                }
            }
            Spacer(Modifier.height(2.dp))
            Text(comment.content, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface)
        }
    }
}

private fun fileSizeHuman(bytes: Long): String {
    if (bytes <= 0) return ""
    val units = arrayOf("B", "KB", "MB", "GB")
    var value = bytes.toDouble()
    var unit = 0
    while (value >= 1024 && unit < units.size - 1) {
        value /= 1024
        unit++
    }
    return if (unit == 0) "${value.toInt()} ${units[unit]}" else String.format("%.1f %s", value, units[unit])
}

@Composable
private fun Modifier.clickableNoRipple(onClick: () -> Unit): Modifier =
    this.then(androidx.compose.foundation.clickable(
        interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
        indication = null,
        onClick = onClick
    ))
