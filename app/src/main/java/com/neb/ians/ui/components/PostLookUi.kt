package com.neb.ians.ui.components

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.spring
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.ColorScheme
import androidx.compose.material3.LocalContentColor
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.compositeOver
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.layout.ContentScale
import coil.compose.AsyncImage
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.PostLook
import com.neb.ians.ui.screens.notes.NoteCoverBanner
import com.neb.ians.ui.screens.notes.NoteIconTile
import com.neb.ians.ui.screens.notes.NoteTone
import com.neb.ians.ui.screens.notes.noteTone
import com.neb.ians.ui.screens.notes.notePaper

/*
 * Dynamic posts. A post can wear a note page's look: a tonal page colour, a cover, an icon,
 * paper and a type face. Everything is drawn from the notes vocabulary (flat, no shadow, no
 * gradient), so a post and a note feel like one family. A plain post never reaches this code.
 */

private fun mixOver(ink: Color, bg: Color, amount: Float): Color = ink.copy(alpha = amount).compositeOver(bg)

private fun contrastOf(a: Color, b: Color): Float {
    val l1 = a.luminance()
    val l2 = b.luminance()
    return (maxOf(l1, l2) + 0.05f) / (minOf(l1, l2) + 0.05f)
}

/** The app colour scheme re-pointed at one tone, so every child (markdown, polls, chips) reads on it. */
private fun lookScheme(base: ColorScheme, tone: NoteTone): ColorScheme {
    val bg = tone.container
    val ink = tone.content
    val accent = if (contrastOf(base.primary, bg) >= 4.5f) base.primary else ink
    return base.copy(
        primary = accent,
        onPrimary = bg,
        primaryContainer = mixOver(ink, bg, 0.14f),
        onPrimaryContainer = ink,
        secondaryContainer = mixOver(ink, bg, 0.14f),
        onSecondaryContainer = ink,
        background = bg,
        onBackground = ink,
        surface = bg,
        onSurface = ink,
        surfaceVariant = mixOver(ink, bg, 0.10f),
        onSurfaceVariant = mixOver(ink, bg, 0.78f),
        surfaceContainerLowest = bg,
        surfaceContainerLow = mixOver(ink, bg, 0.04f),
        surfaceContainer = mixOver(ink, bg, 0.07f),
        surfaceContainerHigh = mixOver(ink, bg, 0.10f),
        surfaceContainerHighest = mixOver(ink, bg, 0.14f),
        outline = mixOver(ink, bg, 0.50f),
        outlineVariant = mixOver(ink, bg, 0.20f),
    )
}

private fun lookTypography(t: Typography, font: Int): Typography {
    val family = when (font) {
        PostLook.FONT_SERIF -> FontFamily.Serif
        PostLook.FONT_MONO -> FontFamily.Monospace
        else -> return t
    }
    fun TextStyle.f() = copy(fontFamily = family)
    return t.copy(
        titleLarge = t.titleLarge.f(), titleMedium = t.titleMedium.f(), titleSmall = t.titleSmall.f(),
        bodyLarge = t.bodyLarge.f(), bodyMedium = t.bodyMedium.f(), bodySmall = t.bodySmall.f(),
        headlineSmall = t.headlineSmall.f(), headlineMedium = t.headlineMedium.f(), headlineLarge = t.headlineLarge.f(),
    )
}

/** Wraps [content] in the look's colours and type. A null or plain look leaves the app theme alone. */
@Composable
fun PostLookTheme(look: PostLook?, content: @Composable () -> Unit) {
    if (look == null || look.isPlain) {
        content()
        return
    }
    val tone = noteTone(look.tone)
    val base = MaterialTheme.colorScheme
    val scheme = remember(base, tone) { lookScheme(base, tone) }
    val type = MaterialTheme.typography
    val styled = remember(type, look.font) { lookTypography(type, look.font) }
    MaterialTheme(colorScheme = scheme, typography = styled, shapes = MaterialTheme.shapes) {
        CompositionLocalProvider(LocalContentColor provides tone.content, content = content)
    }
}

/**
 * The top of a dynamic page: the cover, and the icon tile that straddles its lower edge
 * (or sits alone when there is no cover). Draws nothing when the look has neither.
 */
@Composable
fun PostLookCover(
    look: PostLook,
    coverHeight: Dp,
    iconSize: Dp,
    modifier: Modifier = Modifier,
    animate: Boolean = true,
    /** A picture picked on this phone and not uploaded yet (the composer); otherwise the uploaded cover photo. */
    pendingPhoto: Any? = null,
) {
    val photo: Any? = pendingPhoto ?: look.photo.takeIf { it > 0 }?.let { resolveMediaUrl("/media/content_images/$it.webp") }
    val hasCover = look.cover > 0 || photo != null
    val hasIcon = look.icon.isNotEmpty()
    if (!hasCover && !hasIcon) return
    val tone = noteTone(look.tone)
    val tile = mixOver(tone.content, tone.container, 0.14f)
    // the icon tile settles on a spring when the page opens; scale only, so layout never moves
    val pop = remember(look.icon) { Animatable(if (animate) 0.6f else 1f) }
    LaunchedEffect(look.icon, animate) { if (animate) pop.animateTo(1f, spring(dampingRatio = 0.5f, stiffness = 380f)) }
    Box(modifier.fillMaxWidth().padding(bottom = if (hasCover && hasIcon) iconSize / 2 else 0.dp)) {
        if (photo != null) {
            AsyncImage(
                model = photo, contentDescription = null, contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxWidth().height(coverHeight).background(tile),
            )
        } else if (look.cover > 0) {
            NoteCoverBanner(look.cover, Modifier.fillMaxWidth().height(coverHeight), animate = animate)
        }
        if (hasIcon) {
            NoteIconTile(
                look.icon, iconSize,
                container = if (hasCover) tone.container else tile,
                content = tone.content,
                modifier = Modifier
                    .align(if (hasCover) Alignment.BottomStart else Alignment.TopStart)
                    .padding(start = 16.dp, top = if (hasCover) 0.dp else 16.dp)
                    .offset(y = if (hasCover) iconSize / 2 else 0.dp)
                    .graphicsLayer { scaleX = pop.value; scaleY = pop.value },
            )
        }
    }
}

/**
 * A picture behind the page, cropped to fill, under a flat wash of the page colour so text stays readable.
 * Draws nothing extra when the look has no page picture. [pending] is a picture picked on this phone and not uploaded yet.
 */
@Composable
fun PostLookBackdrop(look: PostLook, modifier: Modifier = Modifier, pending: Any? = null, wash: Float = 0.84f, content: @Composable () -> Unit) {
    val model: Any? = pending ?: look.bg.takeIf { it > 0 }?.let { resolveMediaUrl("/media/content_images/$it.webp") }
    if (model == null) {
        Box(modifier) { content() }
        return
    }
    val tone = noteTone(look.tone)
    Box(modifier) {
        AsyncImage(model = model, contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.matchParentSize())
        Box(Modifier.matchParentSize().background(tone.container.copy(alpha = wash)))
        content()
    }
}

/** The reading page: tone, paper, cover and icon around the post. Plain posts pass straight through. */
@Composable
fun PostLookPage(look: PostLook?, content: @Composable () -> Unit) {
    if (look == null || look.isPlain) {
        content()
        return
    }
    PostLookTheme(look) {
        val tone = noteTone(look.tone)
        Column(Modifier.fillMaxWidth().background(tone.container).notePaper(look.paper, tone.content)) {
            PostLookBackdrop(look) {
                Column(Modifier.fillMaxWidth()) {
                    PostLookCover(look, coverHeight = 148.dp, iconSize = 56.dp)
                    content()
                }
            }
        }
    }
}

/**
 * A feed card. Plain posts keep the flat row; a post with a look becomes a tonal card with
 * its cover and icon on top, and every colour inside follows the tone.
 */
@Composable
fun ForumPostCard(
    post: ApiPost,
    isOwnPost: Boolean,
    onClick: () -> Unit,
    onLikeClick: () -> Unit,
    onBookmarkClick: () -> Unit,
    onShareClick: () -> Unit,
    onReportClick: () -> Unit,
    modifier: Modifier = Modifier,
    onEditClick: () -> Unit = {},
    onArchiveClick: () -> Unit = {},
    onDeleteClick: () -> Unit = {},
    onAuthorClick: () -> Unit = {},
    onAuthorLongPress: () -> Unit = {},
) {
    val look = post.look
    if (look == null || look.isPlain) {
        ForumPostCardPlain(
            post, isOwnPost, onClick, onLikeClick, onBookmarkClick, onShareClick, onReportClick,
            modifier, onEditClick, onArchiveClick, onDeleteClick, onAuthorClick, onAuthorLongPress, true,
        )
        return
    }
    PostLookTheme(look) {
        val tone = noteTone(look.tone)
        val edge = MaterialTheme.colorScheme.outlineVariant
        val shape = RoundedCornerShape(28.dp)
        Column(
            modifier
                .fillMaxWidth()
                .padding(horizontal = 8.dp, vertical = 6.dp)
                .clip(shape)
                .background(tone.container)
                .notePaper(look.paper, tone.content)
                .then(if (tone.hairline) Modifier.border(1.dp, edge, shape) else Modifier),
        ) {
            PostLookBackdrop(look, wash = 0.88f) {
                Column(Modifier.fillMaxWidth()) {
                    PostLookCover(look, coverHeight = 92.dp, iconSize = 44.dp, animate = false)
                    ForumPostCardPlain(
                        post, isOwnPost, onClick, onLikeClick, onBookmarkClick, onShareClick, onReportClick,
                        Modifier, onEditClick, onArchiveClick, onDeleteClick, onAuthorClick, onAuthorLongPress, false,
                    )
                }
            }
        }
    }
}
