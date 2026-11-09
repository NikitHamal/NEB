package com.neb.ians.ui.screens.reader.pdf

import java.nio.charset.Charset

internal const val ST_BOLD = 1
internal const val ST_ITALIC = 2
internal const val ST_MONO = 4

/**
 * What the reader needs of a font: how wide each character is, what Unicode text it stands for,
 * and whether it is bold, italic or monospaced. Glyph outlines are never read (the renderer draws).
 */
internal class PdfFont(
    private val twoByte: Boolean,
    private val toUni: HashMap<Int, String>?,
    private val simple: Array<String?>?,
    private val first: Int,
    private val widths: FloatArray?,
    private val missing: Float,
    private val cidWidths: HashMap<Int, Float>?,
    private val dw: Float,
    val style: Int
) {
    /** Calls [sink] once per character: its text, width in 1/1000 em, whether it is a single-byte space, whether its text is known. */
    fun decode(bytes: ByteArray, sink: (String, Float, Boolean, Boolean) -> Unit) {
        if (twoByte) {
            var i = 0
            while (i + 1 < bytes.size) {
                val code = ((bytes[i].toInt() and 0xFF) shl 8) or (bytes[i + 1].toInt() and 0xFF)
                i += 2
                val text = toUni?.get(code)
                val w = cidWidths?.get(code) ?: dw
                sink(text ?: "\uFFFC", w, false, text != null)
            }
        } else {
            for (b in bytes) {
                val code = b.toInt() and 0xFF
                val text = toUni?.get(code) ?: simple?.get(code)
                val w = if (widths != null && code - first in widths.indices) widths[code - first] else missing
                sink(text ?: "\uFFFC", if (w > 0f) w else missing, code == 32, text != null)
            }
        }
    }

    companion object {
        fun load(file: PdfFile, fontDict: PdfDict): PdfFont {
            val subtype = file.name(fontDict["Subtype"])
            val baseName = (file.name(fontDict["BaseFont"]) ?: "").substringAfter('+')
            var descriptor = file.dict(fontDict["FontDescriptor"])
            var toUni: HashMap<Int, String>? = null
            (file.resolve(fontDict["ToUnicode"]) as? PdfStreamObj)?.let { s ->
                toUni = file.decode(s, 8 * 1024 * 1024)?.let { runCatching { parseToUnicode(it) }.getOrNull() }
            }
            if (subtype == "Type0") {
                val desc = file.dict(file.list(fontDict["DescendantFonts"])?.firstOrNull())
                descriptor = file.dict(desc?.get("FontDescriptor")) ?: descriptor
                val dw = (file.resolve(desc?.get("DW")) as? Number)?.toFloat() ?: 1000f
                val cw = HashMap<Int, Float>()
                file.list(desc?.get("W"))?.let { w ->
                    var i = 0
                    while (i < w.size) {
                        val c = file.resolve(w[i]).int(-1)
                        val nxt = file.resolve(w.getOrNull(i + 1))
                        if (nxt is List<*>) {
                            for ((k, v) in nxt.withIndex()) cw[c + k] = file.resolve(v).num().toFloat()
                            i += 2
                        } else {
                            val hi = nxt.int(-1)
                            val v = file.resolve(w.getOrNull(i + 2)).num().toFloat()
                            if (c >= 0 && hi >= c && hi - c < 70000) for (k in c..hi) cw[k] = v
                            i += 3
                        }
                    }
                }
                return PdfFont(true, toUni, null, 0, null, 0f, cw, dw, styleOf(baseName, descriptor, file))
            }
            val first = file.resolve(fontDict["FirstChar"]).int(0)
            val ws = file.list(fontDict["Widths"])
            var scale = 1f
            if (subtype == "Type3") {
                (file.list(fontDict["FontMatrix"]))?.firstOrNull()?.let { scale = (file.resolve(it).num() * 1000.0).toFloat().takeIf { s -> s > 0f } ?: 1f }
            }
            val widths = ws?.let { l -> FloatArray(l.size) { file.resolve(l[it]).num().toFloat() * scale } }
            val missingW = (file.resolve(descriptor?.get("MissingWidth")) as? Number)?.toFloat()
            val style = styleOf(baseName, descriptor, file)
            val fallbackW = missingW ?: if (style and ST_MONO != 0) 600f else 500f
            return PdfFont(false, toUni, if (toUni == null || toUni!!.isEmpty()) encoding(file, fontDict) else null, first, widths, fallbackW, null, 1000f, style)
        }

        private fun styleOf(base: String, descriptor: PdfDict?, file: PdfFile): Int {
            val n = base.lowercase()
            var s = 0
            if (n.contains("bold") || n.contains("black") || n.contains("heavy") || n.contains("semibold") || n.contains("demi") || n.endsWith("-bd")) s = s or ST_BOLD
            if (n.contains("italic") || n.contains("oblique") || n.endsWith("-it")) s = s or ST_ITALIC
            if (n.contains("mono") || n.contains("courier") || n.contains("consolas") || n.contains("typewriter") || n.contains("menlo") || n.contains("lucidaconsole")) s = s or ST_MONO
            val flags = file.resolve(descriptor?.get("Flags")).int(0)
            if (flags and 1 != 0) s = s or ST_MONO
            if (flags and 64 != 0) s = s or ST_ITALIC
            if (flags and 262144 != 0) s = s or ST_BOLD
            val weight = file.resolve(descriptor?.get("FontWeight")).int(0)
            if (weight >= 600) s = s or ST_BOLD
            if (file.resolve(descriptor?.get("ItalicAngle")).num() < -3.0) s = s or ST_ITALIC
            return s
        }

        private fun charset(name: String): Charset? = runCatching { Charset.forName(name) }.getOrNull()
        private val WIN = charset("windows-1252") ?: Charsets.ISO_8859_1
        private val MAC = charset("x-MacRoman") ?: Charsets.ISO_8859_1

        private fun encoding(file: PdfFile, font: PdfDict): Array<String?> {
            val enc = file.resolve(font["Encoding"])
            val baseName = when (enc) {
                is PdfName -> enc.v
                is Map<*, *> -> file.name(enc["BaseEncoding"])
                else -> null
            }
            val cs = if (baseName == "MacRomanEncoding") MAC else if (baseName == "WinAnsiEncoding" || baseName == null) WIN else Charsets.ISO_8859_1
            val table = arrayOfNulls<String>(256)
            for (i in 32 until 256) {
                if (i == 127) continue
                val s = String(byteArrayOf(i.toByte()), cs)
                table[i] = if (s == "\uFFFD") null else s
            }
            if (enc is Map<*, *>) {
                file.list(enc["Differences"])?.let { diff ->
                    var code = 0
                    for (d in diff) {
                        when (val r = file.resolve(d)) {
                            is Int -> code = r
                            is Double -> code = r.toInt()
                            is PdfName -> { if (code in 0..255) table[code] = glyphToText(r.v); code++ }
                        }
                    }
                }
            }
            return table
        }

        // ------------------------------------------------------------- ToUnicode

        fun parseToUnicode(data: ByteArray): HashMap<Int, String> {
            val map = HashMap<Int, String>()
            val lx = Lexer(ArraySource(data), 0)
            var mode = 0
            val pending = ArrayList<Any?>()
            fun code(s: PdfString): Int { var v = 0; for (b in s.bytes) v = (v shl 8) or (b.toInt() and 0xFF); return v }
            fun text(x: Any?): String? = when (x) {
                is PdfString -> if (x.bytes.size >= 2) String(x.bytes, Charsets.UTF_16BE) else String(x.bytes, Charsets.ISO_8859_1)
                else -> null
            }
            while (true) {
                val o = lx.read(false)
                if (o === PdfEof) break
                if (o is PdfKeyword) {
                    when (o.v) {
                        "beginbfchar" -> { mode = 1; pending.clear() }
                        "beginbfrange" -> { mode = 2; pending.clear() }
                        "endbfchar", "endbfrange" -> { mode = 0; pending.clear() }
                    }
                    continue
                }
                if (mode == 0) continue
                pending.add(o)
                if (mode == 1 && pending.size == 2) {
                    val src = pending[0] as? PdfString; val dst = text(pending[1])
                    if (src != null && dst != null) map[code(src)] = dst
                    pending.clear()
                } else if (mode == 2 && pending.size == 3) {
                    val lo = pending[0] as? PdfString; val hi = pending[1] as? PdfString; val d = pending[2]
                    if (lo != null && hi != null) {
                        val a = code(lo); val b = code(hi)
                        if (b >= a && b - a < 70000) {
                            if (d is List<*>) {
                                for (k in 0..(b - a)) text(d.getOrNull(k))?.let { map[a + k] = it }
                            } else {
                                val base = text(d)
                                if (base != null && base.isNotEmpty()) {
                                    for (k in 0..(b - a)) {
                                        val sb = StringBuilder(base)
                                        sb.setCharAt(sb.length - 1, (base.last().code + k).toChar())
                                        map[a + k] = sb.toString()
                                    }
                                }
                            }
                        }
                    }
                    pending.clear()
                }
            }
            return map
        }

        // ------------------------------------------------------------ glyph names

        private val NAMES: Map<String, String> = run {
            val m = HashMap<String, String>()
            val pairs = listOf(
                "space" to " ", "exclam" to "!", "quotedbl" to "\"", "numbersign" to "#", "dollar" to "$", "percent" to "%",
                "ampersand" to "&", "quotesingle" to "'", "parenleft" to "(", "parenright" to ")", "asterisk" to "*",
                "plus" to "+", "comma" to ",", "hyphen" to "-", "minus" to "\u2212", "period" to ".", "slash" to "/",
                "colon" to ":", "semicolon" to ";", "less" to "<", "equal" to "=", "greater" to ">", "question" to "?",
                "at" to "@", "bracketleft" to "[", "backslash" to "\\", "bracketright" to "]", "asciicircum" to "^",
                "underscore" to "_", "grave" to "`", "braceleft" to "{", "bar" to "|", "braceright" to "}",
                "asciitilde" to "~", "bullet" to "\u2022", "endash" to "\u2013", "emdash" to "\u2014",
                "quoteleft" to "\u2018", "quoteright" to "\u2019", "quotedblleft" to "\u201C", "quotedblright" to "\u201D",
                "quotesinglbase" to "\u201A", "quotedblbase" to "\u201E", "fi" to "fi", "fl" to "fl", "ff" to "ff",
                "ffi" to "ffi", "ffl" to "ffl", "ellipsis" to "\u2026", "dagger" to "\u2020", "daggerdbl" to "\u2021",
                "degree" to "\u00B0", "multiply" to "\u00D7", "divide" to "\u00F7", "copyright" to "\u00A9",
                "registered" to "\u00AE", "trademark" to "\u2122", "section" to "\u00A7", "paragraph" to "\u00B6",
                "periodcentered" to "\u00B7", "guillemotleft" to "\u00AB", "guillemotright" to "\u00BB",
                "sterling" to "\u00A3", "yen" to "\u00A5", "Euro" to "\u20AC", "cent" to "\u00A2",
                "plusminus" to "\u00B1", "onehalf" to "\u00BD", "onequarter" to "\u00BC", "threequarters" to "\u00BE",
                "zero" to "0", "one" to "1", "two" to "2", "three" to "3", "four" to "4", "five" to "5", "six" to "6",
                "seven" to "7", "eight" to "8", "nine" to "9", "nbspace" to " ", "nonbreakingspace" to " ",
                "arrowright" to "\u2192", "arrowleft" to "\u2190", "infinity" to "\u221E", "lessequal" to "\u2264",
                "greaterequal" to "\u2265", "notequal" to "\u2260", "approxequal" to "\u2248", "summation" to "\u2211",
                "radical" to "\u221A", "pi" to "\u03C0", "alpha" to "\u03B1", "beta" to "\u03B2", "gamma" to "\u03B3",
                "delta" to "\u03B4", "mu" to "\u00B5", "Omega" to "\u03A9", "Delta" to "\u0394"
            )
            for ((k, v) in pairs) m[k] = v
            for (c in 'A'..'Z') m[c.toString()] = c.toString()
            for (c in 'a'..'z') m[c.toString()] = c.toString()
            val acc = mapOf(
                "agrave" to "à", "aacute" to "á", "acircumflex" to "â", "atilde" to "ã", "adieresis" to "ä", "aring" to "å",
                "ccedilla" to "ç", "egrave" to "è", "eacute" to "é", "ecircumflex" to "ê", "edieresis" to "ë",
                "igrave" to "ì", "iacute" to "í", "icircumflex" to "î", "idieresis" to "ï", "ntilde" to "ñ",
                "ograve" to "ò", "oacute" to "ó", "ocircumflex" to "ô", "otilde" to "õ", "odieresis" to "ö",
                "ugrave" to "ù", "uacute" to "ú", "ucircumflex" to "û", "udieresis" to "ü", "germandbls" to "ß"
            )
            m.putAll(acc)
            m
        }

        fun glyphToText(name: String): String? {
            val n = name.substringBefore('.')
            NAMES[n]?.let { return it }
            if (n.startsWith("uni") && n.length >= 7) {
                val sb = StringBuilder()
                var i = 3
                while (i + 4 <= n.length) { n.substring(i, i + 4).toIntOrNull(16)?.let { sb.append(it.toChar()) } ?: return null; i += 4 }
                return sb.toString().ifEmpty { null }
            }
            if (n.startsWith("u") && n.length in 5..7) n.substring(1).toIntOrNull(16)?.let { return String(Character.toChars(it)) }
            if (n.contains('_')) {
                val parts = n.split('_').map { glyphToText(it) }
                if (parts.all { it != null }) return parts.joinToString("")
            }
            return null
        }
    }
}
