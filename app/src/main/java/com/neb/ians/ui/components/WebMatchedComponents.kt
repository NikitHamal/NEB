package com.neb.ians.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
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
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ThumbUp
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.neb.ians.R
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiResource
import com.neb.ians.ui.theme.getSubjectTheme
import com.neb.ians.util.formatTimeAgo

private val WebCardShape = RoundedCornerShape(8.dp)
private val PillShape = RoundedCornerShape(999.dp)

fun cleanPreviewText(value: String): String {
    return value
        .replace(Regex("<[^>]*>"), " ")
        .replace("&nbsp;", " ")
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace(Regex("\\s+"), " ")
        .trim()
}

fun primarySubject(subject: String): String {
    return subject.split(",").firstOrNull()?.trim().orEmpty().ifEmpty { "General" }
}

fun subjectIcon(subject: String): Int {
    return when (primarySubject(subject)) {
        "Physics", "Chemistry", "Mathematics", "Biology", "Computer Science" -> R.drawable.ic_science
        "English", "Nepali", "Economics" -> R.drawable.ic_globe
        "Accountancy" -> R.drawable.ic_book
        else -> R.drawable.ic_document
    }
}

@Composable
fun WebAvatar(
    name: String,
    photoUrl: String?,
    modifier: Modifier = Modifier,
    size: Dp = 36.dp
) {
    Box(
        modifier = modifier
            .size(size)
            .clip(CircleShape)
            .background(MaterialTheme.colorScheme.primaryContainer),
        contentAlignment = Alignment.Center
    ) {
        if (!photoUrl.isNullOrBlank()) {
            AsyncImage(
                model = photoUrl,
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize()
            )
        } else {
            Text(
                text = name.firstOrNull()?.uppercase() ?: "?",
                style = MaterialTheme.typography.labelMedium,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onPrimaryContainer
            )
        }
    }
}

@Composable
fun WebResourceCard(
    resource: ApiResource,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    artHeight: Dp = 112.dp
) {
    val subject = primarySubject(resource.subject)
    val subjectTheme = getSubjectTheme(subject)
    val subjectCount = resource.subject.split(",").map { it.trim() }.filter { it.isNotEmpty() }.size
    val subjectLabel = if (subjectCount > 1) "$subject +${subjectCount - 1} more" else subject

    Card(
        onClick = onClick,
        modifier = modifier,
        shape = WebCardShape,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
    ) {
        Column {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(artHeight)
                    .clip(RoundedCornerShape(topStart = 8.dp, topEnd = 8.dp))
            ) {
                if (resource.thumbnailUrl.isNotBlank()) {
                    AsyncImage(
                        model = resource.thumbnailUrl,
                        contentDescription = null,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                } else {
                    SubjectArt(
                        c1 = subjectTheme.art1,
                        c2 = subjectTheme.art2,
                        c3 = subjectTheme.art3,
                        c4 = subjectTheme.art4
                    )
                }

                Surface(
                    shape = PillShape,
                    color = MaterialTheme.colorScheme.surface.copy(alpha = 0.72f),
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.surface.copy(alpha = 0.36f)),
                    modifier = Modifier
                        .align(Alignment.TopStart)
                        .padding(start = 12.dp, top = 10.dp)
                ) {
                    Text(
                        text = resource.type.uppercase(),
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 3.dp),
                        style = MaterialTheme.typography.labelSmall,
                        fontWeight = FontWeight.Bold,
                        color = subjectTheme.art4,
                        maxLines = 1
                    )
                }

                Surface(
                    shape = CircleShape,
                    color = MaterialTheme.colorScheme.surface.copy(alpha = 0.92f),
                    border = BorderStroke(1.dp, Color.Black.copy(alpha = 0.05f)),
                    modifier = Modifier
                        .align(Alignment.BottomEnd)
                        .padding(end = 12.dp, bottom = 10.dp)
                        .size(32.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            painter = painterResource(subjectIcon(subject)),
                            contentDescription = null,
                            tint = subjectTheme.art4,
                            modifier = Modifier.size(18.dp)
                        )
                    }
                }
            }

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 14.dp)
            ) {
                Surface(
                    shape = PillShape,
                    color = subjectTheme.container,
                    modifier = Modifier.padding(bottom = 6.dp)
                ) {
                    Text(
                        text = subjectLabel.uppercase(),
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp),
                        style = MaterialTheme.typography.labelSmall,
                        fontWeight = FontWeight.Bold,
                        color = subjectTheme.onContainer,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }

                Text(
                    text = resource.title,
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.SemiBold,
                    lineHeight = MaterialTheme.typography.bodyMedium.lineHeight,
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.heightIn(min = 42.dp)
                )

                Spacer(modifier = Modifier.height(6.dp))

                Text(
                    text = listOf(resource.gradeLevel, resource.type).filter { it.isNotBlank() }.joinToString(" · "),
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )

                Spacer(modifier = Modifier.height(10.dp))

                Text(
                    text = "${resource.viewCount} views · ${formatTimeAgo(resource.addedAt)}",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
    }
}

@Composable
fun WebPostCard(
    post: ApiPost,
    onClick: () -> Unit,
    onThumbsUpClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        onClick = onClick,
        modifier = modifier,
        shape = WebCardShape,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 18.dp, vertical = 14.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                WebAvatar(post.authorName, post.authorPhotoUrl)
                Column(modifier = Modifier.weight(1f)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = post.authorName,
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.SemiBold,
                            color = MaterialTheme.colorScheme.onSurface,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        CategoryPill(post.category)
                    }
                    Text(
                        text = formatTimeAgo(post.createdAt),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = post.title,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold,
                color = MaterialTheme.colorScheme.onSurface,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )

            val preview = cleanPreviewText(post.content)
            if (preview.isNotBlank()) {
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = preview,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                ActionStat(
                    count = post.thumbsUpCount,
                    active = post.isThumbedUp,
                    onClick = onThumbsUpClick
                )
                Surface(
                    shape = RoundedCornerShape(8.dp),
                    color = Color.Transparent,
                    modifier = Modifier.padding(horizontal = 4.dp, vertical = 2.dp)
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(5.dp),
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                    ) {
                        Icon(
                            painter = painterResource(R.drawable.ic_forum_outlined),
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.size(16.dp)
                        )
                        Text(
                            text = "${post.replyCount}",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun CategoryPill(category: String, modifier: Modifier = Modifier) {
    Surface(
        shape = PillShape,
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = modifier
    ) {
        Text(
            text = category,
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 2.dp),
            style = MaterialTheme.typography.labelSmall,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.primary,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

@Composable
fun ActionStat(
    count: Int,
    active: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .clip(RoundedCornerShape(8.dp))
            .clickable(onClick = onClick)
            .padding(horizontal = 10.dp, vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        Icon(
            imageVector = if (active) Icons.Filled.ThumbUp else Icons.Outlined.ThumbUp,
            contentDescription = null,
            modifier = Modifier.size(16.dp),
            tint = if (active) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            text = count.toString(),
            style = MaterialTheme.typography.labelMedium,
            color = if (active) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
private fun SubjectArt(
    c1: Color,
    c2: Color,
    c3: Color,
    c4: Color
) {
    Canvas(modifier = Modifier.fillMaxSize()) {
        drawRect(c1)
        val w = size.width
        val h = size.height
        drawPath(
            path = Path().apply {
                moveTo(0f, h)
                lineTo(0f, h * 0.58f)
                quadraticBezierTo(w * 0.13f, h * 0.17f, w * 0.33f, h * 0.46f)
                quadraticBezierTo(w * 0.53f, h * 0.75f, w * 0.73f, h * 0.38f)
                quadraticBezierTo(w * 0.9f, h * 0.08f, w, h * 0.42f)
                lineTo(w, h)
                close()
            },
            color = c2.copy(alpha = 0.5f)
        )
        drawPath(
            path = Path().apply {
                moveTo(0f, h)
                lineTo(0f, h * 0.7f)
                quadraticBezierTo(w * 0.2f, h * 0.33f, w * 0.43f, h * 0.58f)
                quadraticBezierTo(w * 0.67f, h * 0.83f, w * 0.87f, h * 0.5f)
                lineTo(w, h * 0.62f)
                lineTo(w, h)
                close()
            },
            color = c3.copy(alpha = 0.35f)
        )
        drawPath(
            path = Path().apply {
                moveTo(0f, h)
                lineTo(0f, h * 0.8f)
                quadraticBezierTo(w * 0.27f, h * 0.54f, w * 0.53f, h * 0.7f)
                quadraticBezierTo(w * 0.8f, h * 0.88f, w, h * 0.67f)
                lineTo(w, h)
                close()
            },
            color = c4.copy(alpha = 0.2f)
        )
        drawOval(
            color = Color.White.copy(alpha = 0.16f),
            topLeft = androidx.compose.ui.geometry.Offset(w * 0.66f, h * 0.1f),
            size = Size(w * 0.24f, h * 0.42f)
        )
    }
}
