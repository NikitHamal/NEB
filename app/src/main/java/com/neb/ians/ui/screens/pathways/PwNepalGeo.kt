package com.neb.ians.ui.screens.pathways

import android.content.Context
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathFillType
import com.neb.ians.R
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject

/**
 * Official map of Nepal (May 2020 boundary, 77 districts, 7 provinces) from `res/raw/nepal_map.json`.
 * Same file as the web map (`static/web/data/nepal_map.json`), built by `backend_python/tools/pathways/build_nepal_map.js`.
 * Integer grid, x right, y down, [w] by [h]. Paths are built once; drawing only transforms them.
 */
internal class GeoDistrict(
    val name: String, val province: Int, val hq: String, val cx: Float, val cy: Float,
    val rings: List<FloatArray>, val path: Path, val minX: Float, val minY: Float, val maxX: Float, val maxY: Float,
) {
    val width get() = maxX - minX
    val height get() = maxY - minY

    fun contains(x: Float, y: Float): Boolean {
        if (x < minX || x > maxX || y < minY || y > maxY) return false
        var inside = false
        for (r in rings) {
            var j = r.size - 2
            var i = 0
            while (i < r.size) {
                val xi = r[i]; val yi = r[i + 1]; val xj = r[j]; val yj = r[j + 1]
                if ((yi > y) != (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) inside = !inside
                j = i; i += 2
            }
        }
        return inside
    }
}

internal class NepalGeo(
    val w: Float, val h: Float, val districts: List<GeoDistrict>,
    val borders: Path, val provinces: Path, val outline: Path, val provinceCentres: List<Offset>,
) {
    val byName: Map<String, GeoDistrict> = districts.associateBy { it.name }
    fun hit(x: Float, y: Float): GeoDistrict? = districts.firstOrNull { it.contains(x, y) }
}

internal object NepalGeoLoader {
    @Volatile private var cached: NepalGeo? = null

    fun peek(): NepalGeo? = cached

    suspend fun get(context: Context): NepalGeo {
        cached?.let { return it }
        val app = context.applicationContext
        return withContext(Dispatchers.Default) { parse(app) }.also { cached = it }
    }

    private fun ringsOf(a: JSONArray): List<FloatArray> = List(a.length()) { i ->
        val r = a.getJSONArray(i)
        val out = FloatArray(r.length())
        var x = 0; var y = 0
        var k = 0
        while (k < r.length()) {
            if (k == 0) { x = r.getInt(0); y = r.getInt(1) } else { x += r.getInt(k); y += r.getInt(k + 1) }
            out[k] = x.toFloat(); out[k + 1] = y.toFloat()
            k += 2
        }
        out
    }

    private fun addTo(p: Path, rings: List<FloatArray>) {
        for (r in rings) {
            p.moveTo(r[0], r[1])
            var i = 2
            while (i < r.size) { p.lineTo(r[i], r[i + 1]); i += 2 }
            p.close()
        }
    }

    private fun parse(context: Context): NepalGeo {
        val j = JSONObject(context.resources.openRawResource(R.raw.nepal_map).bufferedReader().use { it.readText() })
        val borders = Path().apply { fillType = PathFillType.EvenOdd }
        val sumX = FloatArray(7); val sumY = FloatArray(7); val cnt = IntArray(7)
        val ds = j.getJSONArray("d")
        val districts = List(ds.length()) { i ->
            val o = ds.getJSONObject(i)
            val rings = ringsOf(o.getJSONArray("r"))
            val path = Path().apply { fillType = PathFillType.EvenOdd }
            addTo(path, rings); addTo(borders, rings)
            var x0 = Float.MAX_VALUE; var y0 = Float.MAX_VALUE; var x1 = -Float.MAX_VALUE; var y1 = -Float.MAX_VALUE
            for (r in rings) { var k = 0; while (k < r.size) { x0 = minOf(x0, r[k]); x1 = maxOf(x1, r[k]); y0 = minOf(y0, r[k + 1]); y1 = maxOf(y1, r[k + 1]); k += 2 } }
            val c = o.getJSONArray("c")
            val p = o.getInt("p")
            sumX[p] += c.getInt(0); sumY[p] += c.getInt(1); cnt[p]++
            GeoDistrict(o.getString("n"), p, o.optString("hq"), c.getInt(0).toFloat(), c.getInt(1).toFloat(), rings, path, x0, y0, x1, y1)
        }
        val provinces = Path().apply { fillType = PathFillType.EvenOdd }
        val pv = j.getJSONArray("pv")
        for (i in 0 until pv.length()) addTo(provinces, ringsOf(pv.getJSONArray(i)))
        val outline = Path().apply { fillType = PathFillType.EvenOdd }
        addTo(outline, ringsOf(j.getJSONArray("o")))
        val centres = List(7) { Offset(sumX[it] / cnt[it].coerceAtLeast(1), sumY[it] / cnt[it].coerceAtLeast(1)) }
        return NepalGeo(j.getInt("w").toFloat(), j.getInt("h").toFloat(), districts, borders, provinces, outline, centres)
    }
}
