package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.animate
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Stable
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathFillType
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Fill
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.withTransform
import androidx.compose.ui.graphics.lerp
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.launch

private const val KMAX = 16f

/** View of the map: zoom [k] and shift ([tx], [ty], in map units). Screen = origin + base * (t + k * p). */
@Stable
internal class MapCam(val geo: NepalGeo) {
    var k by mutableFloatStateOf(1f)
    var tx by mutableFloatStateOf(0f)
    var ty by mutableFloatStateOf(0f)
    var cw by mutableFloatStateOf(0f)
    var ch by mutableFloatStateOf(0f)
    private var epoch = 0
    val base: Float get() = minOf(cw / geo.w, ch / geo.h).let { if (it > 0f) it else 1f }
    val ox: Float get() = (cw - geo.w * base) / 2f
    val oy: Float get() = (ch - geo.h * base) / 2f

    private fun clamp() {
        k = k.coerceIn(1f, KMAX)
        val px = geo.w * 0.25f; val py = geo.h * 0.25f
        tx = tx.coerceIn(geo.w - geo.w * k - px, px); ty = ty.coerceIn(geo.h - geo.h * k - py, py)
    }
    fun stop() { epoch++ }
    fun viewX(sx: Float) = (sx - ox) / base
    fun viewY(sy: Float) = (sy - oy) / base
    fun zoomAt(px: Float, py: Float, f: Float) {
        val k2 = (k * f).coerceIn(1f, KMAX); val r = k2 / k
        tx = px - (px - tx) * r; ty = py - (py - ty) * r; k = k2; clamp()
    }
    fun panBy(dx: Float, dy: Float) { tx += dx / base; ty += dy / base; clamp() }
    fun pick(sx: Float, sy: Float): GeoDistrict? = geo.hit((viewX(sx) - tx) / k, (viewY(sy) - ty) / k)

    suspend fun fly(k2: Float, x2: Float, y2: Float) {
        val k0 = k; val x0 = tx; val y0 = ty; val e = ++epoch
        animate(0f, 1f, animationSpec = tween(380, easing = FastOutSlowInEasing)) { v, _ ->
            if (epoch != e) throw CancellationException("moved by hand")
            k = k0 + (k2 - k0) * v; tx = x0 + (x2 - x0) * v; ty = y0 + (y2 - y0) * v; clamp()
        }
    }
    suspend fun zoomTo(sx: Float, sy: Float, f: Float) {
        val px = viewX(sx); val py = viewY(sy); val k2 = (k * f).coerceIn(1f, KMAX); val r = k2 / k
        fly(k2, px - (px - tx) * r, py - (py - ty) * r)
    }
    suspend fun zoomCentre(f: Float) = zoomTo(cw / 2f, ch / 2f, f)
    suspend fun fit(d: GeoDistrict?) {
        if (d == null) { if (k != 1f || tx != 0f || ty != 0f) fly(1f, 0f, 0f); return }
        val k2 = (0.55f * minOf(geo.w / d.width, geo.h / d.height)).coerceIn(1.6f, 7f)
        fly(k2, geo.w / 2f - k2 * (d.minX + d.width / 2f), geo.h / 2f - k2 * (d.minY + d.height / 2f))
    }
}

/** Five levels of college count: none, 1, 2 to 3, 4 to 6, 7 or more. */
internal fun mapBin(n: Int) = when { n <= 0 -> 0; n == 1 -> 1; n < 4 -> 2; n < 7 -> 3; else -> 4 }

@Composable
internal fun mapFills(): List<Color> {
    val c = MaterialTheme.colorScheme
    return remember(c.primary, c.surfaceContainerHighest) {
        listOf(0f, 0.2f, 0.38f, 0.58f, 0.8f).map { lerp(c.surfaceContainerHighest, c.primary, it) }
    }
}

@Composable
internal fun PwNepalCanvas(cam: MapCam, counts: Map<String, Int>, selected: String, full: Boolean, onPick: (String) -> Unit, modifier: Modifier = Modifier) {
    val c = MaterialTheme.colorScheme
    val geo = cam.geo
    val fills = mapFills()
    val bins = remember(geo, counts) {
        List(5) { Path().apply { fillType = PathFillType.EvenOdd } }.also { ps -> geo.districts.forEach { ps[mapBin(counts[it.name] ?: 0)].addPath(it.path) } }
    }
    val measurer = rememberTextMeasurer(cacheSize = 240)
    // five fixed sizes so the text cache is reused while zooming; a size grows only when the map has grown
    val dist = remember { listOf(7, 8, 9, 10, 11).map { TextStyle(fontSize = it.sp, fontWeight = FontWeight.Medium, letterSpacing = 0.1.sp) } }
    val prov = remember { TextStyle(fontSize = 10.sp, fontWeight = FontWeight.SemiBold, letterSpacing = 1.6.sp) }
    val byArea = remember(geo) { geo.districts.sortedByDescending { it.width * it.height } }
    val sel = geo.byName[selected]
    val scope = rememberCoroutineScope()
    val interactive by remember(full) { derivedStateOf { full || cam.k > 1.02f } }
    Canvas(
        modifier
            .onSizeChanged { cam.cw = it.width.toFloat(); cam.ch = it.height.toFloat() }
            .pointerInput(interactive) {
                if (interactive) detectTransformGestures { centroid, pan, zoom, _ ->
                    cam.stop(); cam.zoomAt(cam.viewX(centroid.x), cam.viewY(centroid.y), zoom); cam.panBy(pan.x, pan.y)
                }
            }
            .pointerInput(geo, full) {
                detectTapGestures(
                    onDoubleTap = if (full) ({ o: Offset -> scope.launch { cam.zoomTo(o.x, o.y, 2.2f) }; Unit }) else null,
                    onTap = { o -> onPick(cam.pick(o.x, o.y)?.name.orEmpty()) },
                )
            },
    ) {
        val s = cam.base * cam.k
        val line = 1.dp.toPx() / s
        withTransform({ translate(cam.ox + cam.base * cam.tx, cam.oy + cam.base * cam.ty); scale(s, s, Offset.Zero) }) {
            for (i in 0..4) drawPath(bins[i], fills[i])
            if (sel != null) drawPath(sel.path, c.primary)
            drawPath(geo.borders, c.onSurface.copy(alpha = 0.26f), style = Stroke(0.8f * line, join = StrokeJoin.Round))
            drawPath(geo.provinces, c.onSurface.copy(alpha = 0.5f), style = Stroke(1.5f * line, join = StrokeJoin.Round))
            drawPath(geo.outline, c.onSurface, style = Stroke(2f * line, join = StrokeJoin.Round))
            if (sel != null) drawPath(sel.path, c.onSurface, style = Stroke(2.4f * line, join = StrokeJoin.Round))
        }
        fun sx(x: Float) = cam.ox + cam.base * (cam.tx + cam.k * x)
        fun sy(y: Float) = cam.oy + cam.base * (cam.ty + cam.k * y)
        val halo = c.surface.copy(alpha = 0.9f)
        val taken = ArrayList<Rect>(48)
        fun free(r: Rect): Boolean = taken.none { it.overlaps(r) }
        if (cam.k < 1.6f) geo.provinceCentres.forEachIndexed { i, p ->
            val l = measurer.measure(PROVINCES[i].uppercase(), prov)
            val tl = Offset(sx(p.x) - l.size.width / 2f, sy(p.y) - l.size.height / 2f)
            drawText(l, c.onSurfaceVariant.copy(alpha = 0.7f), tl, drawStyle = Fill)
            taken.add(Rect(tl, Size(l.size.width.toFloat(), l.size.height.toFloat())).inflate(2.dp.toPx()))
        }
        val style = dist[when { cam.k < 1.6f -> 0; cam.k < 2.6f -> 1; cam.k < 4.2f -> 2; cam.k < 7f -> 3; else -> 4 }]
        val gap = 2.dp.toPx()
        val order = if (sel != null) listOf(sel) + byArea else byArea
        for (d in order) {
            val on = d === sel
            if (!on && d.width * s < 20.dp.toPx()) continue
            val x = sx(d.cx); val y = sy(d.cy)
            if (x < -60f || y < -30f || x > size.width + 60f || y > size.height + 30f) continue
            val l = measurer.measure(d.name, if (on) dist[maxOf(2, dist.indexOf(style))] else style)
            if (!on && d.width * s < l.size.width * 1.15f) continue
            val tl = Offset(x - l.size.width / 2f, y - l.size.height / 2f)
            val box = Rect(tl, Size(l.size.width.toFloat(), l.size.height.toFloat())).inflate(gap)
            if (!on && !free(box)) continue
            taken.add(box)
            if (on && l.size.width * 1.05f <= d.width * s) {
                // the picked district reads on its own fill: white text, no halo
                drawText(l, c.onPrimary, tl, drawStyle = Fill)
            } else {
                drawText(l, halo, tl, drawStyle = Stroke(2.5.dp.toPx(), join = StrokeJoin.Round))
                drawText(l, c.onSurface, tl, drawStyle = Fill)
            }
        }
    }
}
