package com.neb.ians.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.RowScope
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.painter.Painter
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.neb.ians.R
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiResource
import com.neb.ians.ui.theme.getSubjectTheme
import com.neb.ians.util.formatTimeAgo
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.realtime.RealtimeClient
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.stateIn
import javax.inject.Inject
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle

val WebCardShape = RoundedCornerShape(8.dp)
val WebPanelShape = RoundedCornerShape(16.dp)
val WebPillShape = RoundedCornerShape(999.dp)

@Composable
fun NebiansLogo(
    modifier: Modifier = Modifier
) {
    Image(
        painter = painterResource(id = R.drawable.ic_nebians_logo),
        contentDescription = "NEBians",
        modifier = modifier,
        contentScale = ContentScale.Fit
    )
}

@HiltViewModel
class TopBarViewModel @Inject constructor(
    authRepository: AuthRepository,
    realtimeClient: RealtimeClient
) : ViewModel() {
    val userName = authRepository.currentUserNameFlow
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "Student")
    val userPhotoUrl = authRepository.currentUserPhotoUrlFlow
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), null)

    /** Live unread notification count (web parity: topbar badge). */
    val unreadCount: kotlinx.coroutines.flow.StateFlow<Int> = realtimeClient.unreadCount
}

/**
 * Small error-colored count pill shown at the top-end of an icon
 * (web parity: red unread badge with count, "9+" above 9).
 */
@Composable
fun UnreadCountBadge(
    count: Int,
    modifier: Modifier = Modifier
) {
    if (count <= 0) return
    Box(
        modifier = modifier
            .size(8.dp)
            .background(Color(0xFFEF4444), CircleShape)
            .border(1.dp, MaterialTheme.colorScheme.surface, CircleShape)
    )
}

@Composable
fun WebTopBar(
    modifier: Modifier = Modifier,
    title: String? = null,
    subtitle: String? = null,
    showBack: Boolean = false,
    onBackClick: () -> Unit = {},
    onLogoClick: () -> Unit = {},
    onSearchClick: () -> Unit = {},
    onNotificationsClick: () -> Unit = {},
    onProfileClick: () -> Unit = {},
    avatarInitial: String? = null,
    avatarUrl: String? = null,
    unreadCount: Int = 0,
    compactTitle: Boolean = false,
    actions: @Composable RowScope.() -> Unit = {},
    viewModel: TopBarViewModel = hiltViewModel()
) {
    val dbUserName by viewModel.userName.collectAsStateWithLifecycle()
    val dbUserPhotoUrl by viewModel.userPhotoUrl.collectAsStateWithLifecycle()
    val vmUnreadCount by viewModel.unreadCount.collectAsStateWithLifecycle()

    val name = (avatarInitial ?: dbUserName).ifEmpty { "N" }
    val photo = avatarUrl ?: dbUserPhotoUrl
    val badgeCount = maxOf(unreadCount, vmUnreadCount)

    Surface(
        modifier = modifier.fillMaxWidth(),
        color = MaterialTheme.colorScheme.surface,
        tonalElevation = 0.dp,
        shadowElevation = 0.dp
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .windowInsetsPadding(WindowInsets.statusBars)
                .height(64.dp)
                .padding(horizontal = 16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            if (showBack) {
                IconButton(onClick = onBackClick) {
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                        contentDescription = "Back"
                    )
                }
            } else {
                Row(
                    modifier = Modifier
                        .clip(WebPillShape)
                        .clickable(onClick = onLogoClick)
                        .padding(end = 8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    NebiansLogo(modifier = Modifier.size(40.dp))
                    Text(
                        text = "NEBians",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.primary,
                        maxLines = 1
                    )
                }
            }

            if (title != null || subtitle != null) {
                Column(
                    modifier = Modifier.weight(1f),
                    verticalArrangement = Arrangement.Center
                ) {
                    title?.let {
                        Text(
                            text = it,
                            style = if (compactTitle) MaterialTheme.typography.bodyMedium else MaterialTheme.typography.titleMedium,
                            fontWeight = if (compactTitle) FontWeight.Normal else FontWeight.Bold,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                    subtitle?.let {
                        Text(
                            text = it,
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }
            } else {
                Spacer(modifier = Modifier.weight(1f))
            }

            actions()

            WebIconButton(
                imageVector = Icons.Outlined.Search,
                contentDescription = "Search",
                onClick = onSearchClick
            )
            Box {
                WebIconButton(
                    imageVector = Icons.Outlined.Notifications,
                    contentDescription = "Notifications",
                    onClick = onNotificationsClick
                )
                if (badgeCount > 0) {
                    UnreadCountBadge(
                        count = badgeCount,
                        modifier = Modifier
                            .align(Alignment.TopEnd)
                            .padding(top = 8.dp, end = 8.dp)
                    )
                }
            }
            Avatar(
                name = name,
                imageUrl = photo,
                modifier = Modifier.clickable(onClick = onProfileClick),
                size = 40.dp
            )
        }
    }
}

@Composable
fun WebIconButton(
    imageVector: ImageVector,
    contentDescription: String?,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    IconButton(
        onClick = onClick,
        modifier = modifier
            .size(40.dp)
            .clip(CircleShape)
    ) {
        Icon(
            imageVector = imageVector,
            contentDescription = contentDescription,
            tint = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
fun WebIconButton(
    painter: Painter,
    contentDescription: String?,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    IconButton(
        onClick = onClick,
        modifier = modifier
            .size(40.dp)
            .clip(CircleShape)
    ) {
        Icon(
            painter = painter,
            contentDescription = contentDescription,
            tint = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.size(20.dp)
        )
    }
}

@Composable
fun WebPageHeader(
    title: String,
    subtitle: String,
    modifier: Modifier = Modifier,
    trailing: @Composable RowScope.() -> Unit = {}
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 14.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = title,
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.ExtraBold,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = subtitle,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 3,
                overflow = TextOverflow.Ellipsis
            )
        }
        trailing()
    }
}

@Composable
fun WebSectionHeader(
    title: String,
    modifier: Modifier = Modifier,
    actionLabel: String? = null,
    onActionClick: (() -> Unit)? = null
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = title,
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onSurface,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
        if (actionLabel != null && onActionClick != null) {
            Text(
                text = actionLabel,
                modifier = Modifier
                    .clip(WebPillShape)
                    .clickable(onClick = onActionClick)
                    .padding(horizontal = 10.dp, vertical = 6.dp),
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary,
                fontWeight = FontWeight.SemiBold
            )
        }
    }
}

@Composable
fun WebChip(
    text: String,
    modifier: Modifier = Modifier,
    selected: Boolean = false,
    onClick: (() -> Unit)? = null,
    leading: (@Composable () -> Unit)? = null
) {
    val background = if (selected) MaterialTheme.colorScheme.secondaryContainer else Color.Transparent
    val contentColor = if (selected) MaterialTheme.colorScheme.onSecondaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
    val borderColor = if (selected) Color.Transparent else MaterialTheme.colorScheme.outline
    Row(
        modifier = modifier
            .clip(WebPillShape)
            .background(background)
            .border(1.dp, borderColor, WebPillShape)
            .then(if (onClick != null) Modifier.clickable(onClick = onClick) else Modifier)
            .padding(horizontal = 14.dp, vertical = 7.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        leading?.invoke()
        Text(
            text = text,
            style = MaterialTheme.typography.labelMedium,
            fontWeight = if (selected) FontWeight.Bold else FontWeight.Medium,
            color = contentColor,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

@Composable
fun WebChipRow(
    items: List<String>,
    selectedItem: String?,
    onItemClick: (String?) -> Unit,
    modifier: Modifier = Modifier,
    contentPadding: PaddingValues = PaddingValues(horizontal = 16.dp)
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState())
            .padding(contentPadding),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items.forEach { item ->
            WebChip(
                text = item,
                selected = selectedItem == item,
                onClick = { onItemClick(item) }
            )
        }
    }
}

@Composable
fun WebPrimaryButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    painter: Painter? = null,
    imageVector: ImageVector? = null
) {
    Button(
        onClick = onClick,
        modifier = modifier.heightIn(min = 44.dp),
        shape = WebPillShape,
        colors = ButtonDefaults.buttonColors(
            containerColor = MaterialTheme.colorScheme.primary,
            contentColor = MaterialTheme.colorScheme.onPrimary
        ),
        contentPadding = PaddingValues(horizontal = 22.dp, vertical = 10.dp)
    ) {
        ButtonIcon(painter = painter, imageVector = imageVector)
        Text(text = text, fontWeight = FontWeight.SemiBold, maxLines = 1)
    }
}

@Composable
fun WebOutlinedButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    painter: Painter? = null,
    imageVector: ImageVector? = null
) {
    OutlinedButton(
        onClick = onClick,
        modifier = modifier.heightIn(min = 44.dp),
        shape = WebPillShape,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        colors = ButtonDefaults.outlinedButtonColors(
            contentColor = MaterialTheme.colorScheme.primary,
            containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
        ),
        contentPadding = PaddingValues(horizontal = 22.dp, vertical = 10.dp)
    ) {
        ButtonIcon(painter = painter, imageVector = imageVector)
        Text(text = text, fontWeight = FontWeight.SemiBold, maxLines = 1)
    }
}

@Composable
private fun ButtonIcon(painter: Painter?, imageVector: ImageVector?) {
    when {
        painter != null -> {
            Icon(
                painter = painter,
                contentDescription = null,
                modifier = Modifier
                    .padding(end = 8.dp)
                    .size(18.dp)
            )
        }
        imageVector != null -> {
            Icon(
                imageVector = imageVector,
                contentDescription = null,
                modifier = Modifier
                    .padding(end = 8.dp)
                    .size(18.dp)
            )
        }
    }
}

@Composable
fun WebResourceCard(
    resource: ApiResource,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    minWidth: Dp? = 220.dp
) {
    val subject = remember(resource.subject) { resource.subject.substringBefore(",").trim().ifBlank { "General" } }
    val subjectTheme = getSubjectTheme(subject)
    Card(
        modifier = modifier
            .then(if (minWidth != null) Modifier.width(minWidth) else Modifier.fillMaxWidth())
            .clip(WebPanelShape)
            .clickable(onClick = onClick),
        shape = WebPanelShape,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        // Web parity: thin subject-colored header strip (color-mix accent) at the very top.
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(4.dp)
                .clip(RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp))
                .background(subjectTheme.color)
        )
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(110.dp)
        ) {
            if (resource.thumbnailUrl.isNotBlank()) {
                AsyncImage(
                    model = resource.thumbnailUrl,
                    contentDescription = resource.title,
                    modifier = Modifier.fillMaxSize(),
                    contentScale = ContentScale.Crop
                )
            } else {
                ResourceArt(
                    primary = subjectTheme.color,
                    container = subjectTheme.container,
                    modifier = Modifier.fillMaxSize()
                )
            }
            Surface(
                modifier = Modifier
                    .align(Alignment.TopStart)
                    .padding(10.dp),
                shape = WebPillShape,
                color = MaterialTheme.colorScheme.surfaceContainerLowest.copy(alpha = 0.92f)
            ) {
                Text(
                    text = resource.type,
                    modifier = Modifier.padding(horizontal = 9.dp, vertical = 4.dp),
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontWeight = FontWeight.Bold,
                    maxLines = 1
                )
            }
        }
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .background(subjectTheme.color.copy(alpha = 0.08f))
                .padding(12.dp)
        ) {
            Surface(
                shape = WebPillShape,
                color = subjectTheme.container
            ) {
                Text(
                    text = subject,
                    modifier = Modifier.padding(horizontal = 9.dp, vertical = 3.dp),
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = FontWeight.Bold,
                    color = subjectTheme.onContainer,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = resource.title,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.SemiBold,
                color = MaterialTheme.colorScheme.onSurface,
                minLines = 2,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = listOf(resource.gradeLevel, resource.type).filter { it.isNotBlank() }.joinToString(" - "),
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = "${compactCount(resource.viewCount)} views",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1
            )
        }
    }
}

@Composable
fun ResourceArt(
    primary: Color,
    container: Color,
    modifier: Modifier = Modifier
) {
    Canvas(modifier = modifier.background(container)) {
        val c2 = primary.copy(alpha = 0.38f)
        val c3 = primary.copy(alpha = 0.24f)
        val c4 = primary.copy(alpha = 0.16f)
        drawRect(color = container, size = size)
        drawWave(color = c2, startY = size.height * 0.58f, controlLift = size.height * 0.52f)
        drawWave(color = c3, startY = size.height * 0.76f, controlLift = size.height * 0.36f)
        drawWave(color = c4, startY = size.height * 0.88f, controlLift = size.height * 0.22f)
    }
}

private fun DrawScope.drawWave(color: Color, startY: Float, controlLift: Float) {
    val path = Path().apply {
        moveTo(0f, size.height)
        lineTo(0f, startY)
        cubicTo(size.width * 0.18f, startY - controlLift, size.width * 0.34f, startY + controlLift * 0.32f, size.width * 0.5f, startY)
        cubicTo(size.width * 0.66f, startY - controlLift * 0.32f, size.width * 0.82f, startY + controlLift * 0.24f, size.width, startY - controlLift * 0.18f)
        lineTo(size.width, size.height)
        close()
    }
    drawPath(path = path, color = color)
}

@Composable
fun WebPostCard(
    post: ApiPost,
    onClick: () -> Unit,
    onLikeClick: () -> Unit,
    modifier: Modifier = Modifier,
    compact: Boolean = false
) {
    val category = post.category.ifBlank { "General" }
    val categoryTheme = getSubjectTheme(category)
    Card(
        modifier = modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = WebPanelShape,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(
                verticalAlignment = Alignment.Top,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Avatar(
                    name = post.authorName,
                    imageUrl = post.authorPhotoUrl,
                    size = 38.dp
                )
                Column(modifier = Modifier.weight(1f)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = post.authorName,
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.Bold,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f, fill = false)
                        )
                        Text(
                            text = "  posted",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1
                        )
                    }
                    Text(
                        text = "$category - ${formatTimeAgo(post.createdAt)}",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                Surface(
                    shape = WebPillShape,
                    color = categoryTheme.container
                ) {
                    Text(
                        text = category,
                        modifier = Modifier.padding(horizontal = 9.dp, vertical = 4.dp),
                        style = MaterialTheme.typography.labelSmall,
                        fontWeight = FontWeight.Bold,
                        color = categoryTheme.onContainer,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }

            Spacer(modifier = Modifier.height(10.dp))
            Text(
                text = post.title,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface,
                maxLines = if (compact) 2 else 3,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                text = post.content,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = if (compact) 2 else 4,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.height(12.dp))
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                PostAction(
                    text = compactCount(post.thumbsUpCount),
                    selected = post.isThumbedUp,
                    onClick = onLikeClick
                )
                Surface(
                    shape = WebPillShape,
                    color = Color.Transparent,
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                ) {
                    Text(
                        text = "${post.replyCount} Replies",
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1
                    )
                }
            }
        }
    }
}

@Composable
private fun PostAction(text: String, selected: Boolean, onClick: () -> Unit) {
    Row(
        modifier = Modifier
            .clip(WebPillShape)
            .border(
                1.dp,
                if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant,
                WebPillShape
            )
            .clickable(onClick = onClick)
            .padding(horizontal = 10.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        Icon(
            imageVector = Icons.Outlined.ThumbUp,
            contentDescription = "Like",
            modifier = Modifier.size(16.dp),
            tint = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            text = text,
            style = MaterialTheme.typography.labelMedium,
            color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
fun Avatar(
    name: String,
    imageUrl: String?,
    modifier: Modifier = Modifier,
    size: Dp = 40.dp
) {
    Surface(
        modifier = modifier.size(size),
        shape = CircleShape,
        color = MaterialTheme.colorScheme.primary
    ) {
        val resolvedUrl = remember(imageUrl) {
            if (imageUrl.isNullOrBlank()) null
            else {
                var url = imageUrl.trim()
                if (url.startsWith("http://127.0.0.1:8000/") || url.startsWith("http://localhost:8000/")) {
                    url = url.replace("http://127.0.0.1:8000/", "https://nebians.consica.com.np/")
                             .replace("http://localhost:8000/", "https://nebians.consica.com.np/")
                }
                if (url.startsWith("http://") || url.startsWith("https://")) {
                    url
                } else {
                    "https://nebians.consica.com.np${if (url.startsWith("/")) "" else "/"}$url"
                }
            }
        }
        var isError by remember(resolvedUrl) { mutableStateOf(false) }
        if (!resolvedUrl.isNullOrBlank() && !isError) {
            AsyncImage(
                model = resolvedUrl,
                contentDescription = name,
                modifier = Modifier.fillMaxSize(),
                contentScale = ContentScale.Crop,
                onError = { isError = true }
            )
        } else {
            Box(contentAlignment = Alignment.Center) {
                Text(
                    text = name.firstOrNull()?.uppercase() ?: "?",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onPrimary
                )
            }
        }
    }
}

@Composable
fun WebEmptyState(
    title: String,
    message: String,
    modifier: Modifier = Modifier,
    icon: Painter? = null
) {
    Column(
        modifier = modifier
            .fillMaxWidth()
            .padding(28.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        if (icon != null) {
            Surface(
                modifier = Modifier.size(54.dp),
                shape = CircleShape,
                color = MaterialTheme.colorScheme.surfaceContainerHigh
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        painter = icon,
                        contentDescription = null,
                        modifier = Modifier.size(26.dp),
                        tint = MaterialTheme.colorScheme.primary
                    )
                }
            }
            Spacer(modifier = Modifier.height(12.dp))
        }
        Text(
            text = title,
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onSurface
        )
        Spacer(modifier = Modifier.height(4.dp))
        Text(
            text = message,
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            maxLines = 3,
            overflow = TextOverflow.Ellipsis
        )
    }
}

@Composable
fun WebKpiCard(
    label: String,
    value: String,
    detail: String,
    modifier: Modifier = Modifier,
    painter: Painter? = null,
    color: Color = MaterialTheme.colorScheme.primary
) {
    Surface(
        modifier = modifier
            .heightIn(min = 118.dp),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            if (painter != null) {
                Surface(
                    modifier = Modifier.size(38.dp),
                    shape = RoundedCornerShape(12.dp),
                    color = MaterialTheme.colorScheme.primaryContainer
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            painter = painter,
                            contentDescription = null,
                            modifier = Modifier.size(21.dp),
                            tint = color
                        )
                    }
                }
            }
            Text(
                text = value,
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.ExtraBold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Text(
                text = label,
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(1.dp)
                    .background(MaterialTheme.colorScheme.outlineVariant)
            )
            Text(
                text = detail,
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}

@Composable
fun LiquidNavContainer(
    modifier: Modifier = Modifier,
    content: @Composable RowScope.() -> Unit
) {
    Surface(
        modifier = modifier
            .navigationBarsPadding()
            .padding(horizontal = 18.dp, vertical = 12.dp)
            .shadow(18.dp, WebPillShape, ambientColor = Color.Black.copy(alpha = 0.10f), spotColor = Color.Black.copy(alpha = 0.16f)),
        shape = WebPillShape,
        color = MaterialTheme.colorScheme.surfaceContainer.copy(alpha = 0.88f),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.72f)),
        tonalElevation = 0.dp
    ) {
        Row(
            modifier = Modifier.padding(4.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(2.dp),
            content = content
        )
    }
}

fun compactCount(value: Int): String {
    return when {
        value >= 1_000_000 -> "${value / 1_000_000}M"
        value >= 10_000 -> "${value / 1_000}K"
        value >= 1_000 -> String.format("%.1f", value / 1000f).removeSuffix(".0") + "K"
        else -> value.toString()
    }
}

fun fileSizeLabel(bytes: Long): String {
    if (bytes <= 0L) return ""
    val kb = bytes / 1024.0
    val mb = kb / 1024.0
    val gb = mb / 1024.0
    return when {
        gb >= 1 -> String.format("%.1f GB", gb)
        mb >= 1 -> String.format("%.1f MB", mb)
        kb >= 1 -> String.format("%.0f KB", kb)
        else -> "$bytes B"
    }
}
