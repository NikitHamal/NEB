package com.neb.ians.ui.avatar.blobatar

import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import androidx.collection.LruCache
import kotlin.math.max
import kotlin.math.min

data class BlobatarOpts(
    val hue: Int? = null,
    val tone: Double? = null,
    val background: Any? = null,
    val anim: String? = null,
    val expression: String? = null,
    val shape: String? = null,
    val color: String? = null,
    val bgColor: String? = null,
    val eyeColor: String? = null,
    val normalize: Boolean = true,
    val size: Int? = null
)

private val SHAPE_TRAIT_VALUES = mapOf(
    "round" to 0.11, "organic" to 0.35, "boxy" to 0.54, "capsule" to 0.65,
    "nub" to 0.745, "cloud" to 0.825, "droplet" to 0.8875, "hexagon" to 0.9325,
    "sun" to 0.965, "triangle" to 0.99
)

fun parseBlobatarOpts(params: Map<String, String>): BlobatarOpts {
    return BlobatarOpts(
        hue = params["hue"]?.toIntOrNull()?.coerceIn(0, 360),
        tone = params["tone"]?.toDoubleOrNull()?.coerceIn(0.0, 1.0),
        background = when (params["background"]) {
            null -> null
            "none" -> false
            "square", "circle", "squircle" -> params["background"]
            else -> null
        },
        anim = params["anim"]?.takeIf { it in setOf("bob", "wave", "spin", "pulse") },
        expression = params["expression"]?.takeIf { it in EXPRESSIONS.keys },
        shape = params["shape"]?.takeIf { it in SHAPE_TRAIT_VALUES.keys },
        color = params["color"]?.takeIf { it.matches(Regex("^#[0-9a-fA-F]{6}$")) }?.lowercase(),
        bgColor = params["bgcolor"]?.takeIf { it.matches(Regex("^#[0-9a-fA-F]{6}$")) }?.lowercase()
            ?: params["bgColor"]?.takeIf { it.matches(Regex("^#[0-9a-fA-F]{6}$")) }?.lowercase(),
        eyeColor = params["eyecolor"]?.takeIf { it.matches(Regex("^#[0-9a-fA-F]{6}$")) }?.lowercase()
            ?: params["eyeColor"]?.takeIf { it.matches(Regex("^#[0-9a-fA-F]{6}$")) }?.lowercase()
    )
}

private fun resolve(seed: String, opts: BlobatarOpts): Pair<Traits, Map<String, String>> {
    val traitOverrides: Map<String, Any?> = opts.shape?.let { mapOf("shape" to (SHAPE_TRAIT_VALUES[it] ?: 0.0)) } ?: emptyMap()
    val t = traits(seed, opts.normalize, traitOverrides)
    val hue = opts.hue?.toDouble() ?: t.num("hue", 0.0, 360.0)
    val baseTone = opts.tone ?: t("tone")
    var palette = palette(hue, true, baseTone)
    val overrides = mutableMapOf<String, String>()
    opts.color?.let { overrides["head"] = it }
    opts.bgColor?.let { overrides["bg"] = it }
    opts.eyeColor?.let { overrides["eye"] = it }
    if (overrides.isNotEmpty()) {
        val merged = palette.toMutableMap()
        merged.putAll(overrides)
        for ((fg, bg, minimum) in listOf(Triple("head", "bg", 1.25), Triple("eye", "head", 4.5))) {
            val fgOklch = hexToOklch(merged[fg]!!)
            val bgOklch = hexToOklch(merged[bg]!!)
            val fixed = ensureContrast(fgOklch, bgOklch, minimum)
            merged[fg] = oklchToHex(fixed.first, fixed.second, fixed.third)
        }
        palette = merged
    }
    return t to palette
}

private fun tintedPalette(palette: Map<String, String>, expression: String?): Map<String, String> {
    if (expression == null) return palette
    val tintName = tintNameFor(expression) ?: return palette
    val tintDef = when (tintName) {
        "hot" -> TINT_HOT
        "rose" -> TINT_ROSE
        "blush" -> TINT_BLUSH
        "bile" -> TINT_BILE
        else -> return palette
    }
    return tintWith(palette, tintDef)
}

private fun backdropPath(background: Any?, palette: Map<String, String>): Pair<Path, Int>? {
    if (background == false) return null
    val fill = try { Color.parseColor(palette["bg"]!!) } catch (_: Exception) { Color.TRANSPARENT }
    val path = when (background) {
        "square" -> Path().apply {
            moveTo(0f, 0f); lineTo(100f, 0f); lineTo(100f, 100f); lineTo(0f, 100f); close()
        }
        "circle" -> superellipsePath(50.0, 50.0, 50.0, 50.0, 2.0, 0.0)
        "squircle" -> superellipsePath(50.0, 50.0, 50.0, 50.0, 6.0, 0.0)
        else -> return null
    }
    return path to fill
}

fun drawBlobatar(canvas: Canvas, seed: String, opts: BlobatarOpts, sizePx: Int) {
    val (traits, rawPalette) = resolve(seed, opts)
    val palette = tintedPalette(rawPalette, opts.expression)
    val scale = sizePx / 100f
    canvas.save()
    canvas.scale(scale, scale)

    val headColor = try { Color.parseColor(palette["head"]!!) } catch (_: Exception) { Color.parseColor("#7a5af5") }
    val eyeColor = try { Color.parseColor(palette["eye"]!!) } catch (_: Exception) { Color.parseColor("#0a0a0a") }

    val headPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = headColor; style = Paint.Style.FILL }
    val eyePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = eyeColor; style = Paint.Style.FILL }

    backdropPath(opts.background, palette)?.let { (path, color) ->
        val p = Paint(Paint.ANTI_ALIAS_FLAG).apply { this.color = color; style = Paint.Style.FILL }
        canvas.drawPath(path, p)
    }

    val layout = blobLayout(traits)
    val pose = poseFor(opts.expression ?: "")
    val baked = bakePose(layout, pose)

    if (baked.bodyTranslateY != 0.0) {
        canvas.translate(0f, baked.bodyTranslateY.toFloat())
    }

    for (petal in layout.petals) {
        canvas.drawCircle(petal.cx.toFloat(), petal.cy.toFloat(), petal.r.toFloat(), headPaint)
    }
    for (extra in layout.extra) {
        canvas.drawPath(extra, headPaint)
    }
    val corePath: Path = layout.draw?.invoke(layout.body)
        ?: superellipsePath(layout.body.cx, layout.body.cy, layout.body.rx, layout.body.ry, layout.body.n, layout.body.rot)
    canvas.drawPath(corePath, headPaint)

    for (eye in baked.eyes) {
        val ep = superellipsePath(eye.cx, eye.cy, eye.rx, eye.ry, eye.n, eye.rot)
        canvas.drawPath(ep, eyePaint)
    }

    canvas.restore()
}

private val bitmapCache = object : LruCache<String, Bitmap>(8 * 1024 * 1024) {
    override fun sizeOf(key: String, value: Bitmap): Int = value.byteCount
}

private fun cacheKey(seed: String, opts: BlobatarOpts, sizePx: Int): String =
    "$seed|h=${opts.hue}|t=${opts.tone}|bg=${opts.background}|e=${opts.expression}|s=${opts.shape}|c=${opts.color}|bc=${opts.bgColor}|ec=${opts.eyeColor}|sz=$sizePx"

fun blobatarBitmap(seed: String, opts: BlobatarOpts, sizePx: Int): Bitmap {
    val px = sizePx.coerceIn(32, 512)
    val key = cacheKey(seed, opts, px)
    bitmapCache.get(key)?.let { if (!it.isRecycled) return it }
    val bmp = Bitmap.createBitmap(px, px, Bitmap.Config.ARGB_8888)
    val c = Canvas(bmp)
    drawBlobatar(c, seed.ifBlank { "?" }, opts, px)
    bitmapCache.put(key, bmp)
    return bmp
}

fun clearBlobatarCache() { bitmapCache.evictAll() }
