package com.neb.ians.ui.screens.onboarding

import androidx.activity.compose.BackHandler
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowForward
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebGlyphShapes
import com.neb.ians.ui.components.NebMorphBlob
import com.neb.ians.ui.components.NebTone
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebFastSpatialSpec
import kotlinx.coroutines.launch

private val INTRO_BLOB = listOf(
    NebGlyphShapes.Cookie,
    NebGlyphShapes.Sunny,
    NebGlyphShapes.Flower,
    NebGlyphShapes.Clover
)

private val INTRO_TONES = listOf(NebTone.Azure, NebTone.Sky, NebTone.Aqua, NebTone.Peri)

private val INTRO_TITLES = listOf(
    listOf("Notes.", "Past papers.", "Answers."),
    listOf("Pick your", "level."),
    listOf("Ask what you wonder.", "Share what you know."),
    listOf("Lost on a page?", "Ask Neby.")
)

/**
 * The first-run intro, taken from the landing page: the hero search, the level picker, the
 * forum and Ask Neby. A single tonal blob sits behind the pages and morphs between the
 * landing glyph shapes as the pager moves, so a swipe is one continuous gesture rather
 * than four slides. Each page plays its own entrance with springs when it settles.
 */
@Composable
fun IntroScreen(onFinish: () -> Unit) {
    val cs = MaterialTheme.colorScheme
    val dark = isDarkSurface()
    val pager = rememberPagerState(pageCount = { INTRO_TITLES.size })
    val scope = rememberCoroutineScope()
    val last = INTRO_TITLES.lastIndex
    val onLast = pager.currentPage == last

    BackHandler(enabled = pager.currentPage > 0) {
        scope.launch { pager.animateScrollToPage(pager.currentPage - 1) }
    }

    val blobColor by animateColorAsState(
        INTRO_TONES[pager.currentPage].container(dark),
        nebEffectsSpec()
    )

    Box(Modifier.fillMaxSize().background(cs.surface)) {
        NebMorphBlob(
            shapes = INTRO_BLOB,
            color = blobColor,
            modifier = Modifier
                .align(Alignment.TopCenter)
                .statusBarsPadding()
                .padding(top = 56.dp)
                .size(340.dp)
                .graphicsLayer {
                    val p = pager.currentPage + pager.currentPageOffsetFraction
                    translationX = -(p - 1.5f) * 18.dp.toPx()
                },
            rotation = { (pager.currentPage + pager.currentPageOffsetFraction) * 38f },
            position = { pager.currentPage + pager.currentPageOffsetFraction }
        )

        Column(Modifier.fillMaxSize().statusBarsPadding().navigationBarsPadding()) {
            Row(
                Modifier.fillMaxWidth().height(56.dp).padding(horizontal = 12.dp),
                horizontalArrangement = Arrangement.End,
                verticalAlignment = Alignment.CenterVertically
            ) {
                if (!onLast) {
                    Text(
                        "Skip",
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = FontWeight.SemiBold,
                        color = cs.onSurface,
                        modifier = Modifier
                            .clip(RoundedCornerShape(28.dp))
                            .nebPressable(onClick = onFinish)
                            .padding(horizontal = 16.dp, vertical = 10.dp)
                    )
                }
            }

            HorizontalPager(
                state = pager,
                modifier = Modifier.weight(1f),
                beyondViewportPageCount = 1
            ) { page ->
                val active = pager.settledPage == page || pager.currentPage == page
                Column(
                    Modifier.fillMaxSize().graphicsLayer {
                        val offset = (pager.currentPage - page) + pager.currentPageOffsetFraction
                        translationX = offset * size.width * 0.18f
                    }
                ) {
                    Box(Modifier.weight(1f).fillMaxWidth(), contentAlignment = Alignment.Center) {
                        when (page) {
                            0 -> FinderIllustration(active)
                            1 -> LevelIllustration(active)
                            2 -> ForumIllustration(active)
                            else -> NebyIllustration(active)
                        }
                    }
                    Column(Modifier.fillMaxWidth().padding(horizontal = 28.dp, vertical = 16.dp)) {
                        INTRO_TITLES[page].forEachIndexed { i, line ->
                            Reveal(active, 5 + i, rise = 20.dp) {
                                Text(
                                    line,
                                    fontSize = 34.sp,
                                    lineHeight = 40.sp,
                                    fontWeight = FontWeight.ExtraBold,
                                    style = MaterialTheme.typography.headlineLarge,
                                    color = cs.onSurface
                                )
                            }
                        }
                    }
                }
            }

            Row(
                Modifier.fillMaxWidth().padding(start = 28.dp, end = 20.dp, top = 8.dp, bottom = 20.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    Modifier.weight(1f),
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    repeat(INTRO_TITLES.size) { i -> PageDot(selected = pager.currentPage == i) }
                }
                NebButton(
                    text = if (onLast) "Get started" else "Next",
                    onClick = {
                        if (onLast) onFinish()
                        else scope.launch { pager.animateScrollToPage(pager.currentPage + 1) }
                    },
                    size = NebButtonSize.Hero,
                    tone = NebButtonTone.Primary,
                    trailingIcon = Icons.AutoMirrored.Outlined.ArrowForward
                )
            }
        }
    }
}

/** The active dot stretches into a pill; the width is a spring, so it overshoots a touch. */
@Composable
private fun PageDot(selected: Boolean) {
    val cs = MaterialTheme.colorScheme
    val width by animateDpAsState(if (selected) 28.dp else 8.dp, nebFastSpatialSpec())
    val color by animateColorAsState(if (selected) cs.primary else cs.outlineVariant, nebEffectsSpec())
    Spacer(
        Modifier
            .size(width = width.coerceAtLeast(8.dp), height = 8.dp)
            .clip(RoundedCornerShape(4.dp))
            .background(color)
    )
}
