package com.neb.ians.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.automirrored.outlined.ArrowForward
import androidx.compose.material.icons.outlined.AccountBalance
import androidx.compose.material.icons.outlined.Checklist
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.EditNote
import androidx.compose.material.icons.outlined.Explore
import androidx.compose.material.icons.outlined.GraphicEq
import androidx.compose.material.icons.outlined.LocationOn
import androidx.compose.material.icons.outlined.Public
import androidx.compose.material.icons.outlined.Route
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.Verified
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.LineBreak
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.data.api.ApiWhatsNewConfig
import com.neb.ians.data.api.ApiWhatsNewItem
import com.neb.ians.ui.theme.nebFloatColor
import kotlinx.coroutines.launch
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.min
import kotlin.math.sin

val DefaultWhatsNewConfig = ApiWhatsNewConfig(
    releaseKey = "1.8",
    items = listOf(
        ApiWhatsNewItem(
            id = "pathways",
            badge = "NEW",
            title = "Pathways",
            description = "Explore 124 courses after SEE and +2, compare 58 careers, 77-district colleges, entrance exams and 46 study-abroad routes.",
            ctaLabel = "Try Pathways",
            targetRoute = "pathways",
            kind = "pathways",
        ),
        ApiWhatsNewItem(
            id = "notes_voice",
            badge = "NEW",
            title = "Notes & Voice AI",
            description = "Rich block notes with custom paper, covers, to-do due dates and offline on-device voice dictation and read-aloud.",
            ctaLabel = "Try Notes",
            targetRoute = "notes",
            kind = "notes",
        ),
        ApiWhatsNewItem(
            id = "schools",
            badge = "NEW",
            title = "Schools on NEBians",
            description = "Browse 24,675 schools and colleges across all 77 districts, check verified campus portfolios and claim your institution page.",
            ctaLabel = "Explore Schools",
            targetRoute = "schools",
            kind = "schools",
        ),
    )
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WhatsNewSheet(
    config: ApiWhatsNewConfig,
    onDismiss: () -> Unit,
    onTryItem: (ApiWhatsNewItem) -> Unit,
) {
    val items = config.items.ifEmpty { DefaultWhatsNewConfig.items }
    val pagerState = rememberPagerState(pageCount = { items.size })
    val scope = rememberCoroutineScope()
    val scheme = MaterialTheme.colorScheme
    val dark = scheme.surface.luminance() < 0.5f
    val badgeBg = if (dark) Color(0xFF584400) else Color(0xFFFFD54F)
    val badgeFg = if (dark) Color(0xFFFFE08A) else Color(0xFF241A00)

    NebModalSheet(onDismiss = onDismiss, bottomGap = 20.dp) {
        Column(
            modifier = Modifier.fillMaxWidth().padding(top = 6.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            HorizontalPager(
                state = pagerState,
                modifier = Modifier.fillMaxWidth().boundedWidth(),
            ) { page ->
                val item = items[page]
                Column(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 4.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                ) {
                    Spacer(Modifier.height(6.dp))
                    WhatsNewHeroCluster(kind = item.kind)
                    Spacer(Modifier.height(22.dp))
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(14.dp))
                            .background(badgeBg)
                            .padding(horizontal = 12.dp, vertical = 4.dp),
                        contentAlignment = Alignment.Center,
                    ) {
                        Text(
                            text = item.badge.ifBlank { "NEW" }.uppercase(),
                            color = badgeFg,
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 0.6.sp,
                            maxLines = 1,
                        )
                    }
                    Spacer(Modifier.height(12.dp))
                    Text(
                        text = item.title,
                        color = scheme.onSurface,
                        fontSize = 26.sp,
                        lineHeight = 30.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = (-0.5).sp,
                        textAlign = TextAlign.Center,
                        style = MaterialTheme.typography.headlineSmall.copy(lineBreak = LineBreak.Heading),
                    )
                    Spacer(Modifier.height(10.dp))
                    Text(
                        text = item.description,
                        color = scheme.onSurfaceVariant,
                        fontSize = 14.5.sp,
                        lineHeight = 21.sp,
                        fontWeight = FontWeight.Normal,
                        textAlign = TextAlign.Center,
                        modifier = Modifier.padding(horizontal = 8.dp),
                        style = MaterialTheme.typography.bodyMedium.copy(lineBreak = LineBreak.Paragraph),
                    )
                }
            }

            if (items.size > 1) {
                Spacer(Modifier.height(20.dp))
                WhatsNewPagerControls(
                    count = items.size,
                    current = pagerState.currentPage,
                    onPrev = {
                        val target = (pagerState.currentPage - 1).coerceAtLeast(0)
                        scope.launch { pagerState.animateScrollToPage(target) }
                    },
                    onNext = {
                        val target = (pagerState.currentPage + 1).coerceAtMost(items.lastIndex)
                        scope.launch { pagerState.animateScrollToPage(target) }
                    },
                )
            } else {
                Spacer(Modifier.height(24.dp))
            }

            Spacer(Modifier.height(18.dp))
            val currentItem = items[pagerState.currentPage.coerceIn(0, items.lastIndex)]
            WhatsNewTryButton(
                label = currentItem.ctaLabel.ifBlank { "Try ${currentItem.title}" },
                onClick = { onTryItem(currentItem) },
            )
        }
    }
}

@Composable
private fun WhatsNewHeroCluster(kind: String) {
    val scheme = MaterialTheme.colorScheme
    val floatBg = nebFloatColor()
    val (leftOuter, leftMid, centerIcon, rightMid, rightOuter) = when (kind) {
        "notes" -> listOf(
            Icons.Outlined.Checklist,
            Icons.Outlined.GraphicEq,
            Icons.Outlined.EditNote,
            Icons.Outlined.Description,
            Icons.Outlined.Explore,
        )
        "schools" -> listOf(
            Icons.Outlined.LocationOn,
            Icons.Outlined.School,
            Icons.Outlined.AccountBalance,
            Icons.Outlined.Verified,
            Icons.Outlined.Public,
        )
        else -> listOf(
            Icons.Outlined.Explore,
            Icons.Outlined.School,
            Icons.Outlined.Route,
            Icons.Outlined.Public,
            Icons.Outlined.Description,
        )
    }
    Box(
        modifier = Modifier.fillMaxWidth().height(76.dp),
        contentAlignment = Alignment.Center,
    ) {
        ClusterDisc(leftOuter, scheme.surfaceContainerHigh, scheme.onSurfaceVariant, 42.dp, (-84).dp)
        ClusterDisc(rightOuter, scheme.surfaceContainerHigh, scheme.onSurfaceVariant, 42.dp, 84.dp)
        ClusterDisc(leftMid, scheme.secondaryContainer, scheme.onSecondaryContainer, 50.dp, (-46).dp, floatBg)
        ClusterDisc(rightMid, scheme.tertiaryContainer, scheme.onTertiaryContainer, 50.dp, 46.dp, floatBg)
        val burstPath = remember { Path() }
        Box(
            modifier = Modifier
                .size(66.dp)
                .clip(RoundedCornerShape(20.dp))
                .background(scheme.onSurface)
                .border(2.5.dp, floatBg, RoundedCornerShape(20.dp)),
            contentAlignment = Alignment.Center,
        ) {
            Canvas(Modifier.size(44.dp)) {
                burstPath.rewind()
                val cx = size.width / 2f
                val cy = size.height / 2f
                val r0 = min(cx, cy) * 0.90f
                for (i in 0 until 96) {
                    val t = i / 96.0 * 2.0 * PI
                    val r = r0 * (0.85f + 0.15f * cos(8.0 * t).toFloat())
                    val x = cx + r * cos(t).toFloat()
                    val y = cy + r * sin(t).toFloat()
                    if (i == 0) burstPath.moveTo(x, y) else burstPath.lineTo(x, y)
                }
                burstPath.close()
                drawPath(burstPath, color = scheme.surface, style = Stroke(width = 5.5.dp.toPx()))
            }
            if (kind != "pathways") {
                Icon(centerIcon, null, tint = scheme.surface, modifier = Modifier.size(18.dp))
            }
        }
    }
}

@Composable
private fun ClusterDisc(icon: ImageVector, bg: Color, fg: Color, size: androidx.compose.ui.unit.Dp, offsetX: androidx.compose.ui.unit.Dp, ring: Color? = null) {
    Box(
        modifier = Modifier
            .offset(x = offsetX)
            .size(size)
            .clip(CircleShape)
            .background(bg)
            .then(if (ring != null) Modifier.border(2.dp, ring, CircleShape) else Modifier),
        contentAlignment = Alignment.Center,
    ) {
        Icon(icon, null, tint = fg, modifier = Modifier.size(size * 0.46f))
    }
}

@Composable
private fun WhatsNewPagerControls(count: Int, current: Int, onPrev: () -> Unit, onNext: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        PagerArrow(Icons.AutoMirrored.Outlined.ArrowBack, "Previous", enabled = current > 0, onClick = onPrev)
        Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
            for (i in 0 until count) {
                val active = i == current
                val w by animateDpAsState(if (active) 22.dp else 7.dp, spring(stiffness = Spring.StiffnessMediumLow), label = "dotW")
                val c by animateColorAsState(if (active) scheme.onSurface else scheme.outlineVariant, label = "dotC")
                Box(Modifier.width(w).height(7.dp).clip(RoundedCornerShape(4.dp)).background(c))
            }
        }
        PagerArrow(Icons.AutoMirrored.Outlined.ArrowForward, "Next", enabled = current < count - 1, onClick = onNext)
    }
}

@Composable
private fun PagerArrow(icon: ImageVector, label: String, enabled: Boolean, onClick: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    Box(
        modifier = Modifier
            .size(44.dp)
            .clip(CircleShape)
            .background(if (enabled) scheme.surfaceContainerHigh else scheme.surfaceContainerLow)
            .clickable(enabled = enabled, onClick = onClick),
        contentAlignment = Alignment.Center,
    ) {
        Icon(icon, label, tint = if (enabled) scheme.onSurface else scheme.outlineVariant, modifier = Modifier.size(18.dp))
    }
}

@Composable
private fun WhatsNewTryButton(label: String, onClick: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val pressed by interaction.collectIsPressedAsState()
    val scale by animateFloatAsState(if (pressed) 0.96f else 1f, spring(stiffness = Spring.StiffnessMediumLow), label = "tryScale")
    Surface(
        onClick = onClick,
        interactionSource = interaction,
        modifier = Modifier.fillMaxWidth().height(54.dp).graphicsLayer { scaleX = scale; scaleY = scale },
        shape = RoundedCornerShape(28.dp),
        color = scheme.onSurface,
        contentColor = scheme.surface,
    ) {
        Box(contentAlignment = Alignment.Center, modifier = Modifier.padding(horizontal = 20.dp)) {
            Text(label, fontSize = 16.sp, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
        }
    }
}
