package com.neb.ians.ui.screens.reader.pdf

import kotlin.math.abs
import kotlin.math.hypot

/** A stretch of text drawn in one go. Coordinates are display points: origin top left, y down, [base] the baseline. */
internal class Run(
    val text: String,
    val x0: Float,
    val x1: Float,
    val base: Float,
    val size: Float,
    val style: Int,
    val unmapped: Boolean,
    val hidden: Boolean
) {
    /** Page a link on this text jumps to, or -1. */
    var jump = -1
    var href: String? = null
}

internal const val G_IMAGE = 1
internal const val G_PATH = 2

/** The box of something that was painted but is not text: an image, or a filled or stroked path. */
internal class Gfx(
    val x0: Float, val y0: Float, val x1: Float, val y1: Float,
    val kind: Int, val curves: Int, val diag: Int, val straight: Int, val maxCurve: Float
) {
    val w: Float get() = x1 - x0
    val h: Float get() = y1 - y0

    /** The outline itself (see PdfVector.kt) for small paths, null for big ones and images. */
    var cmds: FloatArray? = null
    var fill = false
    var stroke = false
    var fillRgb = 0
    var strokeRgb = 0
    var lineWidth = 0f
    var evenOdd = false
    /** Fill and stroke opacity (the graphics state's ca and CA): a tinted disc in a diagram is a pale wash, not a solid. */
    var fillA = 1f
    var strokeA = 1f
}

internal class PageContent(val width: Float, val height: Float, val runs: List<Run>, val gfx: List<Gfx>)

/**
 * Walks a page's content streams and reports the text runs and painted boxes, nothing more. It does
 * not draw. Fonts are cached across pages (a book re-uses a few dozen).
 */
internal class PdfTextExtractor(private val file: PdfFile) {
    private val fonts = object : LinkedHashMap<Int, PdfFont>(64, 0.75f, true) {
        override fun removeEldestEntry(eldest: MutableMap.MutableEntry<Int, PdfFont>?) = size > 96
    }

    private class GS(
        var ctm: DoubleArray, var font: PdfFont? = null, var fs: Double = 0.0, var tc: Double = 0.0, var tw: Double = 0.0,
        var th: Double = 1.0, var tl: Double = 0.0, var rise: Double = 0.0, var tr: Int = 0,
        var fillRgb: Int = 0, var strokeRgb: Int = 0, var lw: Double = 1.0, var fa: Float = 1f, var sa: Float = 1f
    ) {
        fun copy() = GS(ctm.copyOf(), font, fs, tc, tw, th, tl, rise, tr, fillRgb, strokeRgb, lw, fa, sa)
    }

    private lateinit var geom: PageGeom
    private val runs = ArrayList<Run>()
    private val gfx = ArrayList<Gfx>()
    private var forms = 0
    private var opCount = 0
    /** Floats of outline kept on this page so far; a drawing with thousands of paths stops being kept past the budget. */
    private var vecFloats = 0

    fun extract(index: Int): PageContent? {
        val node = file.pages().getOrNull(index) ?: return null
        geom = node.geom
        runs.clear(); gfx.clear(); forms = 0; opCount = 0; vecFloats = 0
        val contents = file.resolve(node.dict["Contents"])
        val parts = when (contents) {
            is PdfStreamObj -> listOf(contents)
            is List<*> -> contents.mapNotNull { file.resolve(it) as? PdfStreamObj }
            else -> emptyList()
        }
        val buffer = java.io.ByteArrayOutputStream()
        for (p in parts) {
            file.decode(p)?.let { buffer.write(it); buffer.write(10) }
        }
        val res = file.dict(node.resources)
        runCatching { exec(buffer.toByteArray(), res, doubleArrayOf(1.0, 0.0, 0.0, 1.0, 0.0, 0.0), 0) }
        return PageContent(geom.width.toFloat(), geom.height.toFloat(), ArrayList(runs), ArrayList(gfx))
    }

    private fun mul(m: DoubleArray, n: DoubleArray): DoubleArray = doubleArrayOf(
        m[0] * n[0] + m[1] * n[2], m[0] * n[1] + m[1] * n[3],
        m[2] * n[0] + m[3] * n[2], m[2] * n[1] + m[3] * n[3],
        m[4] * n[0] + m[5] * n[2] + n[4], m[4] * n[1] + m[5] * n[3] + n[5]
    )

    private fun loadFont(res: PdfDict?, name: String): PdfFont? {
        val ref = file.dict(res?.get("Font"))?.get(name)
        val key = (ref as? PdfRef)?.num
        if (key != null) fonts[key]?.let { return it }
        val d = file.dict(ref) ?: return null
        val font = runCatching { PdfFont.load(file, d) }.getOrNull() ?: return null
        if (key != null) fonts[key] = font
        return font
    }

    private fun exec(data: ByteArray, res: PdfDict?, base: DoubleArray, depth: Int) {
        val lx = Lexer(ArraySource(data), 0)
        val ops = ArrayList<Any?>(8)
        var gs = GS(base.copyOf())
        val stack = ArrayList<GS>()
        var tm = doubleArrayOf(1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
        var tlm = tm.copyOf()

        // path state
        var minX = Float.MAX_VALUE; var minY = Float.MAX_VALUE; var maxX = -Float.MAX_VALUE; var maxY = -Float.MAX_VALUE
        var curves = 0; var diag = 0; var straight = 0; var maxCurve = 0f
        var cx = 0f; var cy = 0f
        var segs = 0

        fun px(x: Double, y: Double): Float = geom.fx(gs.ctm[0] * x + gs.ctm[2] * y + gs.ctm[4], gs.ctm[1] * x + gs.ctm[3] * y + gs.ctm[5]).toFloat()
        fun py(x: Double, y: Double): Float = geom.fy(gs.ctm[0] * x + gs.ctm[2] * y + gs.ctm[4], gs.ctm[1] * x + gs.ctm[3] * y + gs.ctm[5]).toFloat()
        fun expand(x: Float, y: Float) {
            if (x < minX) minX = x; if (x > maxX) maxX = x
            if (y < minY) minY = y; if (y > maxY) maxY = y
        }
        // the outline of the path being built, kept for small paths (typeset maths) so it can be drawn again
        var rec = FloatArray(128); var recN = 0; var recOver = false
        fun put(v: Float) {
            if (recN >= 3000) { recOver = true; return }
            if (recN == rec.size) rec = rec.copyOf(rec.size * 2)
            rec[recN++] = v
        }
        fun resetPath() { minX = Float.MAX_VALUE; minY = Float.MAX_VALUE; maxX = -Float.MAX_VALUE; maxY = -Float.MAX_VALUE; curves = 0; diag = 0; straight = 0; maxCurve = 0f; segs = 0; recN = 0; recOver = false }
        fun paint(fill: Boolean, stroke: Boolean, evenOdd: Boolean) {
            if (segs > 0 && minX <= maxX && gfx.size < 20000) {
                val g = Gfx(minX, minY, maxX, maxY, G_PATH, curves, diag, straight, maxCurve)
                if (!recOver && recN > 0 && maxX - minX < 0.9f * geom.width && vecFloats + recN < 900_000) {
                    g.cmds = rec.copyOf(recN); vecFloats += recN
                }
                g.fill = fill; g.stroke = stroke; g.evenOdd = evenOdd
                g.fillRgb = gs.fillRgb; g.strokeRgb = gs.strokeRgb; g.fillA = gs.fa; g.strokeA = gs.sa
                val k = Math.sqrt(abs(gs.ctm[0] * gs.ctm[3] - gs.ctm[1] * gs.ctm[2]))
                g.lineWidth = (gs.lw * k).toFloat()
                gfx.add(g)
            }
            resetPath()
        }
        fun lineToDev(nx: Float, ny: Float) {
            if (abs(nx - cx) > 0.4f && abs(ny - cy) > 0.4f) diag++ else straight++
            expand(cx, cy); expand(nx, ny); cx = nx; cy = ny; segs++
            put(V_LINE.toFloat()); put(nx); put(ny)
        }
        fun lineTo(x: Double, y: Double) = lineToDev(px(x, y), py(x, y))
        fun curveToDev(x1: Float, y1: Float, x2: Float, y2: Float, x3: Float, y3: Float) {
            val xs = floatArrayOf(cx, x1, x2, x3); val ys = floatArrayOf(cy, y1, y2, y3)
            var a = Float.MAX_VALUE; var b = -Float.MAX_VALUE; var c = Float.MAX_VALUE; var d = -Float.MAX_VALUE
            for (k in 0 until 4) { a = minOf(a, xs[k]); b = maxOf(b, xs[k]); c = minOf(c, ys[k]); d = maxOf(d, ys[k]); expand(xs[k], ys[k]) }
            curves++; segs++
            maxCurve = maxOf(maxCurve, maxOf(b - a, d - c))
            put(V_CUBIC.toFloat()); put(x1); put(y1); put(x2); put(y2); put(x3); put(y3)
            cx = x3; cy = y3
        }
        fun curveTo(x1: Double, y1: Double, x2: Double, y2: Double, x3: Double, y3: Double) =
            curveToDev(px(x1, y1), py(x1, y1), px(x2, y2), py(x2, y2), px(x3, y3), py(x3, y3))
        fun packRgb(r: Double, g: Double, b: Double): Int =
            (Math.round(r.coerceIn(0.0, 1.0) * 255).toInt() shl 16) or (Math.round(g.coerceIn(0.0, 1.0) * 255).toInt() shl 8) or Math.round(b.coerceIn(0.0, 1.0) * 255).toInt()
        fun cmyk(c: Double, m: Double, y: Double, k: Double): Int = packRgb((1 - c) * (1 - k), (1 - m) * (1 - k), (1 - y) * (1 - k))
        fun colorFrom(stroke: Boolean) {
            val last = ops.lastOrNull()
            if (last is PdfName) return
            val nums = ops.count { it is Int || it is Double }
            val v = when (nums) {
                1 -> packRgb(ops[0].num(), ops[0].num(), ops[0].num())
                3 -> packRgb(ops[0].num(), ops[1].num(), ops[2].num())
                4 -> cmyk(ops[0].num(), ops[1].num(), ops[2].num(), ops[3].num())
                else -> return
            }
            if (stroke) gs.strokeRgb = v else gs.fillRgb = v
        }
        fun imageBox() {
            val xs = floatArrayOf(px(0.0, 0.0), px(1.0, 0.0), px(0.0, 1.0), px(1.0, 1.0))
            val ys = floatArrayOf(py(0.0, 0.0), py(1.0, 0.0), py(0.0, 1.0), py(1.0, 1.0))
            if (gfx.size < 20000) gfx.add(Gfx(xs.min(), ys.min(), xs.max(), ys.max(), G_IMAGE, 0, 0, 0, 0f))
        }

        // text
        val sb = StringBuilder()
        var runX0 = 0f; var runBase = 0f; var runSize = 0f; var runFont: PdfFont? = null; var runUnmapped = false; var runStarted = false
        var runDirOk = true

        fun origin(): FloatArray {
            val m = mul(tm, gs.ctm)
            val ux = m[4] + gs.rise * m[2]; val uy = m[5] + gs.rise * m[3]
            return floatArrayOf(geom.fx(ux, uy).toFloat(), geom.fy(ux, uy).toFloat())
        }
        fun startRun() {
            if (runStarted) return
            runStarted = true
            val o = origin()
            runX0 = o[0]; runBase = o[1]
            val m = mul(tm, gs.ctm)
            runSize = (gs.fs * hypot(m[2], m[3])).toFloat()
            val ux = m[4] + gs.rise * m[2]; val uy = m[5] + gs.rise * m[3]
            val ex = geom.fx(ux + m[0], uy + m[1]).toFloat(); val ey = geom.fy(ux + m[0], uy + m[1]).toFloat()
            runDirOk = ex - o[0] > 0f && abs(ey - o[1]) < 0.4f * (ex - o[0])
            runFont = gs.font
            sb.setLength(0); runUnmapped = false
        }
        fun flushRun() {
            if (!runStarted) return
            runStarted = false
            val text = sb.toString()
            if (text.isNotEmpty() && runDirOk && runSize > 0.5f && runSize < 400f && runs.size < 60000) {
                val o = origin()
                runs.add(Run(text, runX0, o[0], runBase, runSize, runFont?.style ?: 0, runUnmapped, gs.tr == 3))
            }
            sb.setLength(0)
        }
        fun advance(tx: Double) { tm[4] += tx * tm[0]; tm[5] += tx * tm[1] }
        fun showText(bytes: ByteArray) {
            val font = gs.font ?: return
            startRun()
            font.decode(bytes) { text, w, space, mapped ->
                sb.append(text)
                if (!mapped) runUnmapped = true
                advance((w / 1000.0 * gs.fs + gs.tc + (if (space) gs.tw else 0.0)) * gs.th)
            }
        }
        fun newLine(tx: Double, ty: Double) {
            tlm = doubleArrayOf(tlm[0], tlm[1], tlm[2], tlm[3], tx * tlm[0] + ty * tlm[2] + tlm[4], tx * tlm[1] + ty * tlm[3] + tlm[5])
            tm = tlm.copyOf()
        }
        fun num(i: Int) = ops.getOrNull(i).num()

        while (opCount < 3_000_000) {
            val o = lx.read(false)
            if (o === PdfEof) break
            if (o !is PdfKeyword) { if (ops.size < 64) ops.add(o); continue }
            opCount++
            when (o.v) {
                "q" -> stack.add(gs.copy())
                "Q" -> if (stack.isNotEmpty()) { flushRun(); gs = stack.removeAt(stack.size - 1) }
                "cm" -> if (ops.size >= 6) gs.ctm = mul(doubleArrayOf(num(0), num(1), num(2), num(3), num(4), num(5)), gs.ctm)
                "BT" -> { tm = doubleArrayOf(1.0, 0.0, 0.0, 1.0, 0.0, 0.0); tlm = tm.copyOf() }
                "ET" -> flushRun()
                "Tf" -> {
                    flushRun()
                    val name = (ops.getOrNull(0) as? PdfName)?.v
                    gs.fs = num(1)
                    gs.font = if (name != null) loadFont(res, name) else null
                }
                "Tc" -> { flushRun(); gs.tc = num(0) }
                "Tw" -> gs.tw = num(0)
                "Tz" -> { flushRun(); gs.th = num(0) / 100.0 }
                "TL" -> gs.tl = num(0)
                "Ts" -> { flushRun(); gs.rise = num(0) }
                "Tr" -> { flushRun(); gs.tr = ops.getOrNull(0).int() }
                "Td" -> { flushRun(); newLine(num(0), num(1)) }
                "TD" -> { flushRun(); gs.tl = -num(1); newLine(num(0), num(1)) }
                "Tm" -> { flushRun(); if (ops.size >= 6) { tlm = doubleArrayOf(num(0), num(1), num(2), num(3), num(4), num(5)); tm = tlm.copyOf() } }
                "T*" -> { flushRun(); newLine(0.0, -gs.tl) }
                "Tj" -> { (ops.getOrNull(0) as? PdfString)?.let { showText(it.bytes) }; flushRun() }
                "'" -> { flushRun(); newLine(0.0, -gs.tl); (ops.getOrNull(0) as? PdfString)?.let { showText(it.bytes) }; flushRun() }
                "\"" -> { flushRun(); gs.tw = num(0); gs.tc = num(1); newLine(0.0, -gs.tl); (ops.getOrNull(2) as? PdfString)?.let { showText(it.bytes) }; flushRun() }
                "TJ" -> {
                    val arr = ops.getOrNull(0) as? List<*>
                    if (arr != null) {
                        for (e in arr) {
                            when (e) {
                                is PdfString -> showText(e.bytes)
                                is Int, is Double -> {
                                    val n = e.num()
                                    if (runStarted && n < -200.0 && sb.isNotEmpty() && sb.last() != ' ') sb.append(' ')
                                    advance(-n / 1000.0 * gs.fs * gs.th)
                                }
                            }
                        }
                    }
                    flushRun()
                }
                "m" -> { cx = px(num(0), num(1)); cy = py(num(0), num(1)); put(V_MOVE.toFloat()); put(cx); put(cy) }
                "l" -> lineTo(num(0), num(1))
                "c" -> curveTo(num(0), num(1), num(2), num(3), num(4), num(5))
                "v" -> curveToDev(cx, cy, px(num(0), num(1)), py(num(0), num(1)), px(num(2), num(3)), py(num(2), num(3)))
                "y" -> curveTo(num(0), num(1), num(2), num(3), num(2), num(3))
                "h" -> put(V_CLOSE.toFloat())
                "re" -> {
                    val x = num(0); val y = num(1); val w = num(2); val h = num(3)
                    expand(px(x, y), py(x, y)); expand(px(x + w, y), py(x + w, y))
                    expand(px(x, y + h), py(x, y + h)); expand(px(x + w, y + h), py(x + w, y + h))
                    straight += 4; segs += 4
                    put(V_MOVE.toFloat()); put(px(x, y)); put(py(x, y))
                    put(V_LINE.toFloat()); put(px(x + w, y)); put(py(x + w, y))
                    put(V_LINE.toFloat()); put(px(x + w, y + h)); put(py(x + w, y + h))
                    put(V_LINE.toFloat()); put(px(x, y + h)); put(py(x, y + h))
                    put(V_CLOSE.toFloat())
                    cx = px(x, y); cy = py(x, y)
                }
                "f", "F" -> paint(true, false, false)
                "f*" -> paint(true, false, true)
                "B" -> paint(true, true, false)
                "B*" -> paint(true, true, true)
                "b" -> paint(true, true, false)
                "b*" -> paint(true, true, true)
                "S", "s" -> paint(false, true, false)
                "n" -> resetPath()
                "w" -> gs.lw = num(0)
                "gs" -> {
                    val name = (ops.getOrNull(0) as? PdfName)?.v
                    val eg = if (name != null) file.dict(file.dict(res?.get("ExtGState"))?.get(name)) else null
                    if (eg != null) {
                        eg["ca"]?.let { v -> runCatching { gs.fa = file.resolve(v).num().toFloat().coerceIn(0f, 1f) } }
                        eg["CA"]?.let { v -> runCatching { gs.sa = file.resolve(v).num().toFloat().coerceIn(0f, 1f) } }
                    }
                }
                "g" -> { val v = num(0); gs.fillRgb = packRgb(v, v, v) }
                "G" -> { val v = num(0); gs.strokeRgb = packRgb(v, v, v) }
                "rg" -> gs.fillRgb = packRgb(num(0), num(1), num(2))
                "RG" -> gs.strokeRgb = packRgb(num(0), num(1), num(2))
                "k" -> gs.fillRgb = cmyk(num(0), num(1), num(2), num(3))
                "K" -> gs.strokeRgb = cmyk(num(0), num(1), num(2), num(3))
                "sc", "scn" -> colorFrom(false)
                "SC", "SCN" -> colorFrom(true)
                "Do" -> {
                    val name = (ops.getOrNull(0) as? PdfName)?.v
                    val xo = if (name != null) file.resolve(file.dict(res?.get("XObject"))?.get(name)) as? PdfStreamObj else null
                    if (xo != null) {
                        when (file.name(xo.dict["Subtype"])) {
                            "Image" -> imageBox()
                            "Form" -> if (depth < 6 && forms < 600) {
                                forms++
                                flushRun()
                                val mat = file.list(xo.dict["Matrix"])?.let { l -> if (l.size >= 6) DoubleArray(6) { file.resolve(l[it]).num() } else null }
                                val nb = if (mat != null) mul(mat, gs.ctm) else gs.ctm.copyOf()
                                val fd = file.decode(xo)
                                if (fd != null) {
                                    val fres = file.dict(xo.dict["Resources"]) ?: res
                                    runCatching { exec(fd, fres, nb, depth + 1) }
                                }
                            }
                        }
                    }
                }
                "BI" -> {
                    // inline image: skip its data, keep its box
                    while (true) {
                        val t = lx.read(false)
                        if (t === PdfEof || (t is PdfKeyword && t.v == "ID")) break
                    }
                    lx.pos += 1
                    val src = data
                    var p = lx.pos
                    while (p + 2 < src.size) {
                        if (src[p] == 'E'.code.toByte() && src[p + 1] == 'I'.code.toByte() && isWhite(src[p - 1].toInt() and 0xFF) &&
                            (p + 2 >= src.size || isWhite(src[p + 2].toInt() and 0xFF))
                        ) break
                        p++
                    }
                    lx.pos = minOf(p + 2, src.size)
                    imageBox()
                }
            }
            ops.clear()
        }
        flushRun()
    }
}
