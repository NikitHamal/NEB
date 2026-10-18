package com.neb.ians.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.runtime.Composable
import androidx.compose.runtime.State
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.clipPath
import androidx.compose.ui.graphics.drawscope.withTransform
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.vector.PathParser

/**
 * The NEBians "N", drawn from the same facets as R.drawable.n_logo, so each facet can move on
 * its own. [assembly] runs 0..1 and brings the facets in one after another; [shine] runs 0..1
 * and sweeps a band of light across the finished mark. Both are read in the draw phase only:
 * animating them never recomposes.
 *
 * With both states at 1 this is a static logo, so it doubles as the mark anywhere a Canvas
 * version is handier than the drawable.
 */
@Composable
fun NebLogoMark(
    assembly: State<Float>,
    shine: State<Float>,
    modifier: Modifier = Modifier
) {
    val facets = remember { LOGO_FACETS.map { it to PathParser().parsePathString(it.path).toPath() } }
    val union = remember(facets) { Path().apply { facets.forEach { addPath(it.second) } } }

    Canvas(modifier) {
        val s = size.minDimension / 1024f
        val a = assembly.value
        val sh = shine.value
        withTransform({
            translate((size.width - 1024f * s) / 2f, (size.height - 1024f * s) / 2f)
            scale(s, s, pivot = Offset.Zero)
            translate(210.601f, 86.137f)
            scale(0.610119f, 0.610119f, pivot = Offset.Zero)
        }) {
            facets.forEachIndexed { i, (facet, path) ->
                // each facet gets its own window of the assembly timeline
                val t = ((a - facet.start) / FACET_WINDOW).coerceIn(0f, 1f)
                if (t <= 0f) return@forEachIndexed
                val eased = 1f - (1f - t) * (1f - t) * (1f - t)
                withTransform({
                    translate(facet.fromX * (1f - eased), facet.fromY * (1f - eased))
                }) {
                    val alpha = (t * 2.2f).coerceAtMost(1f)
                    drawPath(path, Brush.linearGradient(facet.colors, facet.gradStart, facet.gradEnd), alpha = alpha)
                    if (facet.edge) {
                        drawPath(path, EDGE, alpha = alpha * 0.9f, style = Stroke(8f, join = StrokeJoin.Round))
                    }
                }
            }
            if (sh in 0.001f..0.999f) {
                // a soft diagonal band of light, clipped to the mark
                val x = -500f + sh * 1700f
                clipPath(union) {
                    drawRect(
                        Brush.linearGradient(
                            0f to Color.Transparent, 0.5f to Color.White.copy(alpha = 0.42f), 1f to Color.Transparent,
                            start = Offset(x - 160f, 0f), end = Offset(x + 160f, 260f)
                        ),
                        topLeft = Offset(0f, 0f),
                        size = androidx.compose.ui.geometry.Size(1000f, 1400f)
                    )
                }
            }
        }
    }
}

private class LogoFacet(
    val path: String,
    val colors: List<Color>,
    val gradStart: Offset,
    val gradEnd: Offset,
    /** Where the facet starts its move from, relative to its resting place, in logo units. */
    val fromX: Float,
    val fromY: Float,
    /** When the facet starts moving, as a fraction of the assembly. */
    val start: Float,
    val edge: Boolean = true
)

private const val FACET_WINDOW = 0.55f
private val EDGE = Color(0xFFEEF5FF)

/** Back to front, as in n_logo.xml. The big ribbon rises; the pillars drop; the light facet slides in. */
private val LOGO_FACETS = listOf(
    LogoFacet(
        "M500,42 L501,135 L856,370 L858,1287 L943,1219 L943,331 Z",
        listOf(Color(0xFF07337F), Color(0xFF052566), Color(0xFF021B54)),
        Offset(505f, 30f), Offset(960f, 1290f), fromX = 0f, fromY = -260f, start = 0.18f
    ),
    LogoFacet(
        "M441,191 L441,282 L691,447 L691,799 L774,886 L775,408 Z",
        listOf(Color(0xFF06327C), Color(0xFF04215E)),
        Offset(435f, 180f), Offset(780f, 890f), fromX = 0f, fromY = -200f, start = 0.3f
    ),
    LogoFacet(
        "M306,320 L307,377 L613,706 L613,485 Z",
        listOf(Color(0xFFA8C5FF), Color(0xFF90B4FB), Color(0xFF82A8F5)),
        Offset(305f, 320f), Offset(615f, 705f), fromX = -180f, fromY = -150f, start = 0.42f
    ),
    LogoFacet(
        "M51,228 L51,1132 L263,1346 L267,812 L775,1353 L775,887 L691,800 L685,902 Z",
        listOf(Color(0xFF0058DF), Color(0xFF004BD4), Color(0xFF003CC3)),
        Offset(40f, 220f), Offset(800f, 1350f), fromX = 0f, fromY = 240f, start = 0f
    ),
    LogoFacet(
        "M691,800 L775,887 L775,1052 L691,958 Z",
        listOf(Color(0x590030A5), Color(0x00001E77)),
        Offset(690f, 780f), Offset(780f, 1050f), fromX = 0f, fromY = 0f, start = 0.45f, edge = false
    )
)
