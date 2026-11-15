package com.neb.ians.ui.screens.pathways

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.unit.dp

/** District centres as (longitude, latitude). Drawn on a schematic outline of Nepal, not a survey map. */
internal val DISTRICT_POINT = mapOf(
    "Baglung" to (83.60f to 28.27f), "Banke" to (81.62f to 28.05f), "Bhaktapur" to (85.43f to 27.67f), "Bhojpur" to (87.05f to 27.17f),
    "Chitwan" to (84.43f to 27.53f), "Dadeldhura" to (80.58f to 29.30f), "Dang" to (82.30f to 28.10f), "Dhankuta" to (87.34f to 26.98f),
    "Dhanusha" to (85.95f to 26.85f), "Dolakha" to (86.07f to 27.70f), "Doti" to (80.98f to 29.25f), "Gorkha" to (84.63f to 28.00f),
    "Ilam" to (87.93f to 26.91f), "Jhapa" to (87.89f to 26.62f), "Jumla" to (82.18f to 29.27f), "Kailali" to (80.95f to 28.75f),
    "Kanchanpur" to (80.35f to 28.85f), "Kaski" to (84.00f to 28.25f), "Kathmandu" to (85.32f to 27.71f), "Kavrepalanchok" to (85.55f to 27.55f),
    "Lalitpur" to (85.32f to 27.55f), "Lamjung" to (84.38f to 28.25f), "Makwanpur" to (85.05f to 27.42f), "Morang" to (87.45f to 26.65f),
    "Nawalparasi East" to (84.10f to 27.55f), "Palpa" to (83.55f to 27.87f), "Parsa" to (84.85f to 27.10f), "Rupandehi" to (83.45f to 27.55f),
    "Saptari" to (86.75f to 26.62f), "Siraha" to (86.20f to 26.65f), "Sunsari" to (87.20f to 26.67f), "Surkhet" to (81.62f to 28.60f),
    "Tanahu" to (84.25f to 27.95f),
    "Achham" to (81.25f to 29.05f),
    "Arghakhanchi" to (83.15f to 27.95f),
    "Baitadi" to (80.45f to 29.52f),
    "Bajhang" to (81.20f to 29.55f),
    "Bajura" to (81.50f to 29.45f),
    "Bara" to (85.05f to 27.00f),
    "Bardiya" to (81.45f to 28.35f),
    "Dailekh" to (81.70f to 28.85f),
    "Darchula" to (80.55f to 29.85f),
    "Dhading" to (84.90f to 27.90f),
    "Dolpa" to (82.90f to 29.00f),
    "Gulmi" to (83.30f to 28.05f),
    "Humla" to (81.85f to 29.97f),
    "Jajarkot" to (82.20f to 28.70f),
    "Kalikot" to (81.85f to 29.15f),
    "Kapilvastu" to (83.00f to 27.55f),
    "Khotang" to (86.80f to 27.20f),
    "Mahottari" to (85.80f to 26.95f),
    "Manang" to (84.15f to 28.65f),
    "Mugu" to (82.20f to 29.55f),
    "Mustang" to (83.85f to 28.95f),
    "Myagdi" to (83.40f to 28.45f),
    "Nawalparasi West" to (83.65f to 27.60f),
    "Nuwakot" to (85.15f to 27.90f),
    "Okhaldhunga" to (86.50f to 27.30f),
    "Panchthar" to (87.80f to 27.15f),
    "Parbat" to (83.70f to 28.20f),
    "Pyuthan" to (82.85f to 28.10f),
    "Ramechhap" to (86.10f to 27.35f),
    "Rasuwa" to (85.30f to 28.20f),
    "Rautahat" to (85.30f to 26.95f),
    "Rolpa" to (82.65f to 28.35f),
    "Rukum East" to (82.65f to 28.60f),
    "Rukum West" to (82.20f to 28.60f),
    "Salyan" to (82.15f to 28.35f),
    "Sankhuwasabha" to (87.25f to 27.40f),
    "Sarlahi" to (85.55f to 27.00f),
    "Sindhuli" to (85.95f to 27.25f),
    "Sindhupalchok" to (85.70f to 27.95f),
    "Solukhumbu" to (86.65f to 27.70f),
    "Syangja" to (83.85f to 28.00f),
    "Taplejung" to (87.65f to 27.55f),
    "Terhathum" to (87.55f to 27.12f),
    "Udayapur" to (86.55f to 26.95f),
)

private val OUTLINE = listOf(
    80.06f to 28.83f, 80.25f to 29.15f, 80.55f to 29.30f, 80.95f to 29.70f, 81.10f to 30.15f, 81.60f to 30.35f, 82.10f to 30.35f, 82.70f to 29.95f,
    83.35f to 29.45f, 84.05f to 29.25f, 84.20f to 28.90f, 84.65f to 28.65f, 85.15f to 28.30f, 85.75f to 28.25f, 86.00f to 27.95f, 86.60f to 28.10f,
    87.10f to 27.85f, 87.80f to 27.95f, 88.15f to 27.90f, 88.05f to 27.45f, 88.15f to 26.45f, 87.50f to 26.40f, 86.75f to 26.45f, 86.00f to 26.65f,
    85.25f to 26.75f, 84.65f to 27.05f, 84.20f to 27.40f, 83.40f to 27.45f, 82.70f to 27.70f, 82.00f to 28.00f, 81.50f to 28.30f, 80.80f to 28.65f,
)

private const val LON0 = 79.9f
private const val LON1 = 88.3f
private const val LAT0 = 26.3f
private const val LAT1 = 30.5f

private fun project(p: Pair<Float, Float>, w: Float, h: Float, pad: Float) =
    Offset(pad + (p.first - LON0) / (LON1 - LON0) * (w - 2 * pad), pad + (LAT1 - p.second) / (LAT1 - LAT0) * (h - 2 * pad))

/** Tap a dot to pick its district. Dots grow with the number of listed colleges. */
@Composable
internal fun PwNepalMap(counts: Map<String, Int>, selected: String, onSelect: (String) -> Unit, modifier: Modifier = Modifier) {
    val c = MaterialTheme.colorScheme
    val water = pwTone(0).bg
    val dot = pwTone(1).solid
    val land = c.surface.copy(alpha = 0.62f)
    val line = c.outline.copy(alpha = 0.45f)
    val pts = remember(counts) { counts.keys.mapNotNull { k -> DISTRICT_POINT[k]?.let { k to it } } }
    Canvas(
        modifier.fillMaxWidth().aspectRatio(1.8f).clip(RoundedCornerShape(28.dp))
            .pointerInput(pts) {
                detectTapGestures { tap ->
                    val w = size.width.toFloat(); val h = size.height.toFloat()
                    val hit = pts.minByOrNull { (_, p) -> (project(p, w, h, 24f) - tap).getDistance() }
                    if (hit != null && (project(hit.second, w, h, 24f) - tap).getDistance() < 72f) onSelect(hit.first)
                }
            },
    ) {
        val w = size.width; val h = size.height; val pad = 24f
        drawRect(water)
        for (i in 1..5) drawLine(line.copy(alpha = 0.12f), Offset(0f, h * i / 6f), Offset(w, h * i / 6f), 1f)
        for (i in 1..9) drawLine(line.copy(alpha = 0.12f), Offset(w * i / 10f, 0f), Offset(w * i / 10f, h), 1f)
        val path = Path().apply {
            OUTLINE.forEachIndexed { i, p -> project(p, w, h, pad).let { if (i == 0) moveTo(it.x, it.y) else lineTo(it.x, it.y) } }
            close()
        }
        drawPath(path, land)
        drawPath(path, line, style = Stroke(2.5f))
        pts.filter { it.first != selected }.forEach { (k, p) ->
            drawCircle(dot, 8f + (counts[k] ?: 1).coerceAtMost(6) * 1.6f, project(p, w, h, pad))
        }
        pts.firstOrNull { it.first == selected }?.let { (k, p) ->
            val at = project(p, w, h, pad)
            drawCircle(c.primary.copy(alpha = 0.22f), 34f, at)
            drawCircle(c.surface, 17f, at)
            drawCircle(c.primary, 13f + (counts[k] ?: 1).coerceAtMost(6) * 0.6f, at)
        }
    }
}
