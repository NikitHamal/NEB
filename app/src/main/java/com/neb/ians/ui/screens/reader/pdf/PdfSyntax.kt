package com.neb.ians.ui.screens.reader.pdf

import java.io.ByteArrayOutputStream
import java.io.Closeable
import java.io.File
import java.io.RandomAccessFile
import java.nio.MappedByteBuffer
import java.nio.channels.FileChannel
import java.util.zip.Inflater

/*
 * A small, read-only PDF object reader. The platform PdfRenderer draws pages but cannot say where
 * the links are on most phones, so this reads the file structure itself: cross reference tables and
 * streams, object streams, filters, the page tree. It never loads the file into the heap (the file is
 * memory mapped and objects are parsed on demand), so a 100 MB book costs a few hundred kilobytes.
 * No Android classes are used here, so it can be exercised on a plain JVM.
 */

internal typealias PdfDict = Map<String, Any?>

internal class PdfName(val v: String) {
    override fun equals(other: Any?) = other is PdfName && other.v == v
    override fun hashCode() = v.hashCode()
    override fun toString() = "/$v"
}

internal class PdfKeyword(val v: String)

internal class PdfString(val bytes: ByteArray) {
    /** Text strings: UTF-16BE with a byte order mark, UTF-8 with a mark, otherwise Latin-1 (close to PDFDocEncoding). */
    fun text(): String = when {
        bytes.size >= 2 && bytes[0] == 0xFE.toByte() && bytes[1] == 0xFF.toByte() -> String(bytes, 2, bytes.size - 2, Charsets.UTF_16BE)
        bytes.size >= 2 && bytes[0] == 0xFF.toByte() && bytes[1] == 0xFE.toByte() -> String(bytes, 2, bytes.size - 2, Charsets.UTF_16LE)
        bytes.size >= 3 && bytes[0] == 0xEF.toByte() && bytes[1] == 0xBB.toByte() && bytes[2] == 0xBF.toByte() -> String(bytes, 3, bytes.size - 3, Charsets.UTF_8)
        else -> String(bytes, Charsets.ISO_8859_1)
    }
}

internal data class PdfRef(val num: Int, val gen: Int)

internal class PdfStreamObj(val dict: PdfDict, val offset: Int, val length: Int, val src: PdfSource)

internal object PdfEof

internal interface PdfSource : Closeable {
    val size: Int
    fun at(i: Int): Int
    fun copy(off: Int, len: Int): ByteArray
}

internal class ArraySource(private val b: ByteArray) : PdfSource {
    override val size get() = b.size
    override fun at(i: Int) = b[i].toInt() and 0xFF
    override fun copy(off: Int, len: Int): ByteArray = b.copyOfRange(off, minOf(b.size, off + len))
    override fun close() {}
}

internal class MappedSource(file: File) : PdfSource {
    private val raf = RandomAccessFile(file, "r")
    private val buf: MappedByteBuffer
    init {
        val length = raf.length()
        require(length in 8..Int.MAX_VALUE.toLong()) { "unsupported size" }
        buf = raf.channel.map(FileChannel.MapMode.READ_ONLY, 0, length)
    }
    override val size get() = buf.limit()
    override fun at(i: Int) = buf.get(i).toInt() and 0xFF
    override fun copy(off: Int, len: Int): ByteArray {
        val n = minOf(len, size - off).coerceAtLeast(0)
        val out = ByteArray(n)
        val dup = buf.duplicate()
        dup.position(off)
        dup.get(out, 0, n)
        return out
    }
    override fun close() { runCatching { raf.close() } }
}

internal fun isWhite(c: Int) = c == 32 || c == 10 || c == 13 || c == 9 || c == 12 || c == 0
internal fun isDelim(c: Int) = c == '('.code || c == ')'.code || c == '<'.code || c == '>'.code || c == '['.code ||
    c == ']'.code || c == '{'.code || c == '}'.code || c == '/'.code || c == '%'.code

internal fun Any?.num(default: Double = 0.0): Double = when (this) {
    is Int -> toDouble()
    is Double -> this
    is Long -> toDouble()
    else -> default
}

internal fun Any?.int(default: Int = 0): Int = when (this) {
    is Int -> this
    is Double -> toInt()
    is Long -> toInt()
    else -> default
}

internal class Lexer(private val s: PdfSource, var pos: Int = 0, private val end: Int = s.size) {

    fun atEnd(): Boolean { skipWhite(); return pos >= end }

    fun skipWhite() {
        while (pos < end) {
            val c = s.at(pos)
            if (isWhite(c)) pos++
            else if (c == '%'.code) { while (pos < end && s.at(pos) != 10 && s.at(pos) != 13) pos++ }
            else break
        }
    }

    /** Reads the next object. Keywords come back as [PdfKeyword]; the end of data as [PdfEof]. */
    fun read(refs: Boolean): Any? {
        skipWhite()
        if (pos >= end) return PdfEof
        val c = s.at(pos)
        when {
            c == '/'.code -> { pos++; return PdfName(readName()) }
            c == '('.code -> { pos++; return readLiteral() }
            c == '<'.code -> {
                if (pos + 1 < end && s.at(pos + 1) == '<'.code) { pos += 2; return readDict(refs) }
                pos++
                return readHex()
            }
            c == '>'.code -> {
                if (pos + 1 < end && s.at(pos + 1) == '>'.code) { pos += 2; return PdfKeyword(">>") }
                pos++; return PdfKeyword(">")
            }
            c == '['.code -> { pos++; return readArray(refs) }
            c == ']'.code -> { pos++; return PdfKeyword("]") }
            c == ')'.code || c == '{'.code || c == '}'.code -> { pos++; return PdfKeyword(c.toChar().toString()) }
            c == '+'.code || c == '-'.code || c == '.'.code || (c >= '0'.code && c <= '9'.code) -> return readNumber(refs)
        }
        val start = pos
        while (pos < end) { val d = s.at(pos); if (isWhite(d) || isDelim(d)) break; pos++ }
        if (pos == start) { pos++; return PdfKeyword("") }
        val word = String(s.copy(start, pos - start), Charsets.ISO_8859_1)
        return when (word) {
            "true" -> true
            "false" -> false
            "null" -> null
            else -> PdfKeyword(word)
        }
    }

    private fun readName(): String {
        val sb = StringBuilder()
        while (pos < end) {
            val c = s.at(pos)
            if (isWhite(c) || isDelim(c)) break
            if (c == '#'.code && pos + 2 < end) {
                val h = hex(s.at(pos + 1)); val l = hex(s.at(pos + 2))
                if (h >= 0 && l >= 0) { sb.append((h * 16 + l).toChar()); pos += 3; continue }
            }
            sb.append(c.toChar()); pos++
        }
        return sb.toString()
    }

    private fun hex(c: Int) = when (c) {
        in '0'.code..'9'.code -> c - '0'.code
        in 'a'.code..'f'.code -> c - 'a'.code + 10
        in 'A'.code..'F'.code -> c - 'A'.code + 10
        else -> -1
    }

    private fun readLiteral(): PdfString {
        val out = ByteArrayOutputStream()
        var depth = 1
        while (pos < end) {
            val c = s.at(pos++)
            when (c) {
                '\\'.code -> {
                    if (pos >= end) break
                    val e = s.at(pos++)
                    when (e) {
                        'n'.code -> out.write(10)
                        'r'.code -> out.write(13)
                        't'.code -> out.write(9)
                        'b'.code -> out.write(8)
                        'f'.code -> out.write(12)
                        13 -> if (pos < end && s.at(pos) == 10) pos++
                        10 -> {}
                        in '0'.code..'7'.code -> {
                            var v = e - '0'.code
                            var n = 1
                            while (n < 3 && pos < end && s.at(pos) in '0'.code..'7'.code) { v = v * 8 + (s.at(pos++) - '0'.code); n++ }
                            out.write(v and 0xFF)
                        }
                        else -> out.write(e)
                    }
                }
                '('.code -> { depth++; out.write(c) }
                ')'.code -> { depth--; if (depth == 0) return PdfString(out.toByteArray()); out.write(c) }
                else -> out.write(c)
            }
        }
        return PdfString(out.toByteArray())
    }

    private fun readHex(): PdfString {
        val out = ByteArrayOutputStream()
        var hi = -1
        while (pos < end) {
            val c = s.at(pos++)
            if (c == '>'.code) break
            val h = hex(c)
            if (h < 0) continue
            if (hi < 0) hi = h else { out.write(hi * 16 + h); hi = -1 }
        }
        if (hi >= 0) out.write(hi * 16)
        return PdfString(out.toByteArray())
    }

    private fun readArray(refs: Boolean): List<Any?> {
        val list = ArrayList<Any?>()
        while (true) {
            val o = read(refs)
            if (o === PdfEof) break
            if (o is PdfKeyword) { if (o.v == "]") break else continue }
            list.add(o)
        }
        return list
    }

    private fun readDict(refs: Boolean): PdfDict {
        val d = LinkedHashMap<String, Any?>()
        while (true) {
            val k = read(refs)
            if (k === PdfEof) break
            if (k is PdfKeyword) { if (k.v == ">>") break else continue }
            if (k !is PdfName) continue
            val v = read(refs)
            if (v === PdfEof) break
            if (v is PdfKeyword) { if (v.v == ">>") break else continue }
            d[k.v] = v
        }
        return d
    }

    private fun readNumber(refs: Boolean): Any? {
        val start = pos
        var real = false
        if (s.at(pos) == '+'.code || s.at(pos) == '-'.code) pos++
        while (pos < end && s.at(pos) == '-'.code) pos++
        while (pos < end) {
            val c = s.at(pos)
            if (c == '.'.code) { real = true; pos++ }
            else if (c >= '0'.code && c <= '9'.code) pos++
            else break
        }
        if (pos < end && !isWhite(s.at(pos)) && !isDelim(s.at(pos))) {
            // glued to a keyword, such as "0.5rg": the number ends here
        }
        val text = String(s.copy(start, pos - start), Charsets.ISO_8859_1).replace("--", "-")
        if (text == "+" || text == "-" || text == "." || text.isEmpty()) return PdfKeyword(text)
        if (real) return text.toDoubleOrNull() ?: 0.0
        val n = text.toLongOrNull() ?: return text.toDoubleOrNull() ?: 0.0
        if (refs && n >= 0 && n < Int.MAX_VALUE) {
            val save = pos
            skipWhite()
            val p = pos
            if (p < end && s.at(p) in '0'.code..'9'.code) {
                var q = p
                while (q < end && s.at(q) in '0'.code..'9'.code) q++
                val gen = String(s.copy(p, q - p), Charsets.ISO_8859_1).toIntOrNull()
                var r = q
                while (r < end && isWhite(s.at(r))) r++
                if (gen != null && r > q && r < end && s.at(r) == 'R'.code && (r + 1 >= end || isWhite(s.at(r + 1)) || isDelim(s.at(r + 1)))) {
                    pos = r + 1
                    return PdfRef(n.toInt(), gen)
                }
            }
            pos = save
        }
        return if (n in Int.MIN_VALUE..Int.MAX_VALUE) n.toInt() else n.toDouble()
    }
}

/** Where a page is, as the platform renderer shows it: size in points after rotation, and how to place a PDF point on it. */
internal class PageGeom(val x0: Double, val y0: Double, val x1: Double, val y1: Double, val rot: Int) {
    private val w = (x1 - x0).coerceAtLeast(1.0)
    private val h = (y1 - y0).coerceAtLeast(1.0)
    val width: Double get() = if (rot == 90 || rot == 270) h else w
    val height: Double get() = if (rot == 90 || rot == 270) w else h

    /** Display coordinates in points, origin top left, y down. */
    fun fx(x: Double, y: Double): Double = when (rot) {
        90 -> (y - y0)
        180 -> (x1 - x)
        270 -> (y1 - y)
        else -> (x - x0)
    }

    fun fy(x: Double, y: Double): Double = when (rot) {
        90 -> (x - x0)
        180 -> (y - y0)
        270 -> (x1 - x)
        else -> (y1 - y)
    }
}

internal class PageNode(val num: Int, val dict: PdfDict, val resources: Any?, val geom: PageGeom)

internal class PdfFile private constructor(private val src: PdfSource) : Closeable {
    private var xType = ByteArray(0)
    private var xA = IntArray(0)
    private var xB = IntArray(0)
    var trailer: PdfDict = emptyMap(); private set
    var encrypted = false; private set

    private val objects = object : LinkedHashMap<Int, Any?>(256, 0.75f, true) {
        override fun removeEldestEntry(eldest: MutableMap.MutableEntry<Int, Any?>?) = size > 3000
    }
    private val objStms = object : LinkedHashMap<Int, ObjStm>(8, 0.75f, true) {
        override fun removeEldestEntry(eldest: MutableMap.MutableEntry<Int, ObjStm>?) = size > 3
    }

    private class ObjStm(val data: ByteArray, val nums: IntArray, val offsets: IntArray, val first: Int)

    private var pageList: List<PageNode>? = null
    private val pageByNum = HashMap<Int, Int>()

    private fun ensure(n: Int) {
        if (n < xType.size) return
        val size = maxOf(n + 1, xType.size * 2, 64).coerceAtMost(12_000_000)
        if (n >= size) return
        xType = xType.copyOf(size); xA = xA.copyOf(size); xB = xB.copyOf(size)
    }

    private fun setEntry(num: Int, type: Int, a: Int, b: Int) {
        if (num < 0) return
        ensure(num)
        if (num >= xType.size || xType[num].toInt() != 0) return
        xType[num] = type.toByte(); xA[num] = a; xB[num] = b
    }

    // ------------------------------------------------------------------ xref

    private fun startXref(): Int {
        val tail = maxOf(0, src.size - 2048)
        var i = src.size - 9
        while (i >= tail) {
            if (matches(i, "startxref")) {
                val lx = Lexer(src, i + 9)
                return (lx.read(false) as? Int) ?: -1
            }
            i--
        }
        return -1
    }

    private fun matches(at: Int, word: String): Boolean {
        if (at < 0 || at + word.length > src.size) return false
        for (k in word.indices) if (src.at(at + k) != word[k].code) return false
        return true
    }

    private fun indexOf(word: String, from: Int, to: Int = src.size): Int {
        val first = word[0].code
        var i = from.coerceAtLeast(0)
        val last = to - word.length
        while (i <= last) {
            if (src.at(i) == first && matches(i, word)) return i
            i++
        }
        return -1
    }

    private fun readXrefChain(start: Int): Boolean {
        val seen = HashSet<Int>()
        var next = start
        var ok = false
        while (next >= 0 && seen.add(next)) {
            val result = runCatching { readXrefSection(next) }.getOrNull() ?: break
            ok = true
            next = result
        }
        return ok
    }

    /** Reads one table or stream; returns the offset of the previous section, or -1. */
    private fun readXrefSection(off: Int): Int {
        if (off < 0 || off >= src.size) throw IllegalStateException("bad xref offset")
        val lx = Lexer(src, off)
        lx.skipWhite()
        val dict: PdfDict
        if (matches(lx.pos, "xref")) {
            lx.pos += 4
            while (true) {
                val t = lx.read(false)
                if (t is PdfKeyword && t.v == "trailer") break
                if (t !is Int) throw IllegalStateException("bad xref table")
                val count = lx.read(false) as? Int ?: throw IllegalStateException("bad xref table")
                for (k in 0 until count) {
                    val o = lx.read(false); val g = lx.read(false); val f = lx.read(false)
                    if (f !is PdfKeyword) throw IllegalStateException("bad xref entry")
                    if (f.v == "n") setEntry(t + k, 2, o.int(), g.int()) else setEntry(t + k, 1, 0, 0)
                }
            }
            dict = lx.read(true) as? PdfDict ?: throw IllegalStateException("no trailer")
            val stm = dict["XRefStm"]
            if (stm is Int) runCatching { readXrefSection(stm) }
        } else {
            val obj = parseIndirectAt(off) as? PdfStreamObj ?: throw IllegalStateException("no xref stream")
            dict = obj.dict
            val data = decode(obj) ?: throw IllegalStateException("xref stream")
            val w = (dict["W"] as? List<*>)?.map { it.int() } ?: throw IllegalStateException("W")
            val size = dict["Size"].int()
            val index = (dict["Index"] as? List<*>)?.map { it.int() } ?: listOf(0, size)
            val rowLen = w.sum()
            var p = 0
            var k = 0
            while (k + 1 < index.size) {
                for (n in 0 until index[k + 1]) {
                    if (p + rowLen > data.size) break
                    fun field(i: Int): Long {
                        var v = 0L
                        for (b in 0 until w[i]) v = (v shl 8) or (data[p++].toLong() and 0xFF)
                        return v
                    }
                    val type = if (w[0] == 0) 1L else field(0)
                    val a = field(1)
                    val b = field(2)
                    when (type) {
                        1L -> setEntry(index[k] + n, 2, a.toInt(), b.toInt())
                        2L -> setEntry(index[k] + n, 3, a.toInt(), b.toInt())
                        else -> setEntry(index[k] + n, 1, 0, 0)
                    }
                }
                k += 2
            }
        }
        if (trailer.isEmpty()) trailer = dict
        else {
            val merged = LinkedHashMap(trailer)
            for ((key, v) in dict) if (key !in merged) merged[key] = v
            trailer = merged
        }
        return (dict["Prev"] as? Number)?.toInt() ?: -1
    }

    /** Last resort for damaged files: find every "n g obj" and take the last trailer-like dictionary. */
    private fun rebuild() {
        var i = 0
        val size = src.size
        while (true) {
            val at = indexOf("obj", i)
            if (at < 0) break
            i = at + 3
            if (at > 0 && src.at(at - 1) == 'd'.code) continue  // endobj
            var p = at - 1
            while (p >= 0 && isWhite(src.at(p))) p--
            val genEnd = p
            while (p >= 0 && src.at(p) in '0'.code..'9'.code) p--
            if (p == genEnd) continue
            val gen = String(src.copy(p + 1, genEnd - p), Charsets.ISO_8859_1).toIntOrNull() ?: continue
            while (p >= 0 && isWhite(src.at(p))) p--
            val numEnd = p
            while (p >= 0 && src.at(p) in '0'.code..'9'.code) p--
            if (p == numEnd) continue
            val num = String(src.copy(p + 1, numEnd - p), Charsets.ISO_8859_1).toIntOrNull() ?: continue
            // later definitions win: write directly
            ensure(num)
            if (num < xType.size) { xType[num] = 2; xA[num] = p + 1; xB[num] = gen }
        }
        var t = indexOf("trailer", 0)
        var last: PdfDict? = null
        while (t >= 0) {
            val d = runCatching { Lexer(src, t + 7).read(true) as? PdfDict }.getOrNull()
            if (d != null && d["Root"] != null) last = d
            t = indexOf("trailer", t + 7)
        }
        if (last == null) {
            // cross reference streams: look through objects for one with /Root
            for (n in xType.indices) {
                if (xType[n].toInt() != 2) continue
                val o = runCatching { parseIndirectAt(xA[n]) }.getOrNull()
                val d = (o as? PdfStreamObj)?.dict ?: o as? PdfDict
                if (d != null && d["Root"] != null && (d["Type"] as? PdfName)?.v == "XRef") last = d
            }
        }
        if (last == null) {
            for (n in xType.indices) {
                if (xType[n].toInt() != 2) continue
                val d = runCatching { parseIndirectAt(xA[n]) }.getOrNull() as? PdfDict ?: continue
                if ((d["Type"] as? PdfName)?.v == "Catalog") { last = mapOf("Root" to PdfRef(n, 0)); break }
            }
        }
        trailer = last ?: emptyMap()
        // object streams hide objects in rebuilt files: index their members
        for (n in xType.indices) {
            if (xType[n].toInt() != 2) continue
            val o = runCatching { parseIndirectAt(xA[n]) }.getOrNull() as? PdfStreamObj ?: continue
            if ((o.dict["Type"] as? PdfName)?.v != "ObjStm") continue
            val stm = runCatching { loadObjStm(n, o) }.getOrNull() ?: continue
            for (k in stm.nums.indices) {
                if (stm.nums[k] < xType.size && xType[stm.nums[k]].toInt() != 2) { xType[stm.nums[k]] = 3; xA[stm.nums[k]] = n; xB[stm.nums[k]] = k }
            }
        }
    }

    // --------------------------------------------------------------- objects

    private fun parseIndirectAt(off: Int): Any? {
        if (off < 0 || off >= src.size) return null
        val lx = Lexer(src, off)
        val n = lx.read(false); val g = lx.read(false); val kw = lx.read(false)
        if (n !is Int || g !is Int || kw !is PdfKeyword || !kw.v.startsWith("obj")) return null
        if (kw.v.length > 3) lx.pos -= kw.v.length - 3
        val value = lx.read(true)
        if (value is PdfKeyword) return null
        if (value !is Map<*, *>) return value
        @Suppress("UNCHECKED_CAST") val dict = value as PdfDict
        lx.skipWhite()
        if (!matches(lx.pos, "stream")) return dict
        var p = lx.pos + 6
        if (p < src.size && src.at(p) == 13) p++
        if (p < src.size && src.at(p) == 10) p++
        var len = -1
        val declared = dict["Length"]
        val ln = when (declared) {
            is PdfRef -> if (declared.num != n) resolve(declared) else null
            else -> declared
        }
        if (ln is Int && ln >= 0 && p + ln <= src.size) {
            var q = p + ln
            while (q < src.size && isWhite(src.at(q))) q++
            if (matches(q, "endstream")) len = ln
        }
        if (len < 0) {
            val e = indexOf("endstream", p)
            len = if (e < 0) src.size - p else {
                var q = e
                if (q > p && src.at(q - 1) == 10) q--
                if (q > p && src.at(q - 1) == 13) q--
                q - p
            }
        }
        return PdfStreamObj(dict, p, len, src)
    }

    private fun loadObjStm(num: Int, stream: PdfStreamObj): ObjStm? {
        val data = decode(stream) ?: return null
        val n = stream.dict["N"].int()
        val first = stream.dict["First"].int()
        val lx = Lexer(ArraySource(data), 0, minOf(first, data.size))
        val nums = IntArray(n); val offs = IntArray(n)
        for (k in 0 until n) {
            nums[k] = lx.read(false).int(-1)
            offs[k] = lx.read(false).int(0)
        }
        return ObjStm(data, nums, offs, first)
    }

    @Synchronized
    fun get(num: Int): Any? {
        if (num < 0 || num >= xType.size) return null
        if (objects.containsKey(num)) return objects[num]
        val value: Any? = when (xType[num].toInt()) {
            2 -> parseIndirectAt(xA[num])
            3 -> {
                val holder = xA[num]
                val stm = objStms[holder] ?: run {
                    val h = get(holder) as? PdfStreamObj
                    val loaded = h?.let { runCatching { loadObjStm(holder, it) }.getOrNull() }
                    if (loaded != null) objStms[holder] = loaded
                    loaded
                }
                if (stm == null) null else {
                    var idx = xB[num]
                    if (idx !in stm.nums.indices || stm.nums[idx] != num) idx = stm.nums.indexOf(num)
                    if (idx < 0) null else {
                        val lx = Lexer(ArraySource(stm.data), stm.first + stm.offsets[idx])
                        lx.read(true).takeIf { it !is PdfKeyword && it !== PdfEof }
                    }
                }
            }
            else -> null
        }
        objects[num] = value
        return value
    }

    fun resolve(x: Any?): Any? {
        var cur = x
        var guard = 0
        while (cur is PdfRef && guard++ < 16) cur = get(cur.num)
        return cur
    }

    fun dict(x: Any?): PdfDict? = when (val r = resolve(x)) {
        is PdfStreamObj -> r.dict
        is Map<*, *> -> @Suppress("UNCHECKED_CAST") (r as PdfDict)
        else -> null
    }

    fun list(x: Any?): List<Any?>? = resolve(x) as? List<Any?>

    fun name(x: Any?): String? = (resolve(x) as? PdfName)?.v

    // --------------------------------------------------------------- filters

    @Synchronized
    fun decode(s: PdfStreamObj, limit: Int = 96 * 1024 * 1024): ByteArray? {
        var data = s.src.copy(s.offset, s.length)
        val filterObj = resolve(s.dict["Filter"] ?: s.dict["F"])
        val filters = when (filterObj) {
            null -> emptyList()
            is List<*> -> filterObj.map { name(it) ?: "" }
            else -> listOf(name(filterObj) ?: "")
        }
        val parmObj = resolve(s.dict["DecodeParms"] ?: s.dict["DP"])
        val parms: List<PdfDict?> = when (parmObj) {
            is List<*> -> parmObj.map { dict(it) }
            is Map<*, *> -> listOf(dict(parmObj))
            else -> emptyList()
        }
        for ((i, f) in filters.withIndex()) {
            val p = parms.getOrNull(i)
            data = when (f) {
                "FlateDecode", "Fl" -> predictor(inflate(data, limit), p)
                "LZWDecode", "LZW" -> predictor(lzw(data, if (p != null) (resolve(p["EarlyChange"]) as? Int ?: 1) else 1, limit), p)
                "ASCIIHexDecode", "AHx" -> asciiHex(data)
                "ASCII85Decode", "A85" -> ascii85(data)
                "RunLengthDecode", "RL" -> runLength(data, limit)
                "Crypt" -> data
                else -> return null
            }
        }
        return data
    }

    private fun inflate(input: ByteArray, limit: Int): ByteArray {
        val inflater = Inflater()
        val out = ByteArrayOutputStream(maxOf(1024, input.size * 3))
        try {
            inflater.setInput(input)
            val buf = ByteArray(32 * 1024)
            while (!inflater.finished() && out.size() < limit) {
                val n = try { inflater.inflate(buf) } catch (e: java.util.zip.DataFormatException) { break }
                if (n == 0 && (inflater.needsInput() || inflater.needsDictionary())) break
                out.write(buf, 0, n)
            }
        } finally { inflater.end() }
        return out.toByteArray()
    }

    private fun predictor(data: ByteArray, p: PdfDict?): ByteArray {
        if (p == null) return data
        val pred = resolve(p["Predictor"]).int(1)
        if (pred < 2) return data
        val colors = resolve(p["Colors"]).int(1).coerceAtLeast(1)
        val bpc = resolve(p["BitsPerComponent"]).int(8).coerceAtLeast(1)
        val columns = resolve(p["Columns"]).int(1).coerceAtLeast(1)
        val bpp = ((colors * bpc + 7) / 8).coerceAtLeast(1)
        val row = (colors * bpc * columns + 7) / 8
        if (pred == 2) {
            if (bpc != 8) return data
            val out = data.copyOf()
            var r = 0
            while (r + row <= out.size) {
                for (i in bpp until row) out[r + i] = (out[r + i] + out[r + i - bpp]).toByte()
                r += row
            }
            return out
        }
        val rows = data.size / (row + 1) + if (data.size % (row + 1) > 1) 1 else 0
        val out = ByteArray(rows * row)
        var prev = ByteArray(row)
        var cur = ByteArray(row)
        var ip = 0
        for (r in 0 until rows) {
            if (ip >= data.size) break
            val tag = data[ip++].toInt()
            val n = minOf(row, data.size - ip)
            java.util.Arrays.fill(cur, 0)
            System.arraycopy(data, ip, cur, 0, n)
            ip += n
            when (tag) {
                1 -> for (i in bpp until row) cur[i] = (cur[i] + cur[i - bpp]).toByte()
                2 -> for (i in 0 until row) cur[i] = (cur[i] + prev[i]).toByte()
                3 -> for (i in 0 until row) {
                    val left = if (i >= bpp) cur[i - bpp].toInt() and 0xFF else 0
                    cur[i] = (cur[i] + ((left + (prev[i].toInt() and 0xFF)) shr 1)).toByte()
                }
                4 -> for (i in 0 until row) {
                    val a = if (i >= bpp) cur[i - bpp].toInt() and 0xFF else 0
                    val b = prev[i].toInt() and 0xFF
                    val c = if (i >= bpp) prev[i - bpp].toInt() and 0xFF else 0
                    val pp = a + b - c
                    val pa = kotlin.math.abs(pp - a); val pb = kotlin.math.abs(pp - b); val pc = kotlin.math.abs(pp - c)
                    val pr = if (pa <= pb && pa <= pc) a else if (pb <= pc) b else c
                    cur[i] = (cur[i] + pr).toByte()
                }
            }
            System.arraycopy(cur, 0, out, r * row, row)
            val t = prev; prev = cur; cur = t
        }
        return out
    }

    private fun lzw(input: ByteArray, early: Int, limit: Int): ByteArray {
        val out = ByteArrayOutputStream(input.size * 3)
        val table = arrayOfNulls<ByteArray>(4096)
        for (i in 0 until 256) table[i] = byteArrayOf(i.toByte())
        var next = 258
        var bits = 9
        var buffer = 0
        var have = 0
        var prev: ByteArray? = null
        var ip = 0
        while (out.size() < limit) {
            while (have < bits && ip < input.size) { buffer = (buffer shl 8) or (input[ip++].toInt() and 0xFF); have += 8 }
            if (have < bits) break
            val code = (buffer shr (have - bits)) and ((1 shl bits) - 1)
            have -= bits
            buffer = buffer and ((1 shl have) - 1)
            if (code == 256) { next = 258; bits = 9; prev = null; continue }
            if (code == 257) break
            val entry: ByteArray = if (code < next && table[code] != null) table[code]!!
            else if (prev != null) prev + prev[0] else break
            out.write(entry)
            if (prev != null && next < 4096) { table[next++] = prev + entry[0] }
            prev = entry
            bits = when {
                next + early >= 4096 -> 12
                next + early >= 2048 -> 12
                next + early >= 1024 -> 11
                next + early >= 512 -> 10
                else -> 9
            }
        }
        return out.toByteArray()
    }

    private fun asciiHex(input: ByteArray): ByteArray {
        val out = ByteArrayOutputStream()
        var hi = -1
        for (b in input) {
            val c = b.toInt() and 0xFF
            if (c == '>'.code) break
            val h = when (c) { in 48..57 -> c - 48; in 97..102 -> c - 87; in 65..70 -> c - 55; else -> -1 }
            if (h < 0) continue
            if (hi < 0) hi = h else { out.write(hi * 16 + h); hi = -1 }
        }
        if (hi >= 0) out.write(hi * 16)
        return out.toByteArray()
    }

    private fun ascii85(input: ByteArray): ByteArray {
        val out = ByteArrayOutputStream()
        val group = LongArray(5)
        var n = 0
        var i = 0
        if (input.size >= 2 && input[0] == '<'.code.toByte() && input[1] == '~'.code.toByte()) i = 2
        while (i < input.size) {
            val c = input[i++].toInt() and 0xFF
            if (c == '~'.code) break
            if (isWhite(c)) continue
            if (c == 'z'.code && n == 0) { out.write(0); out.write(0); out.write(0); out.write(0); continue }
            if (c < '!'.code || c > 'u'.code) continue
            group[n++] = (c - 33).toLong()
            if (n == 5) {
                var v = 0L
                for (k in 0 until 5) v = v * 85 + group[k]
                out.write((v shr 24).toInt() and 0xFF); out.write((v shr 16).toInt() and 0xFF)
                out.write((v shr 8).toInt() and 0xFF); out.write(v.toInt() and 0xFF)
                n = 0
            }
        }
        if (n > 1) {
            for (k in n until 5) group[k] = 84
            var v = 0L
            for (k in 0 until 5) v = v * 85 + group[k]
            for (k in 0 until n - 1) out.write((v shr (24 - 8 * k)).toInt() and 0xFF)
        }
        return out.toByteArray()
    }

    private fun runLength(input: ByteArray, limit: Int): ByteArray {
        val out = ByteArrayOutputStream()
        var i = 0
        while (i < input.size && out.size() < limit) {
            val l = input[i++].toInt() and 0xFF
            if (l == 128) break
            if (l < 128) { val n = minOf(l + 1, input.size - i); out.write(input, i, n); i += n }
            else if (i < input.size) { val b = input[i++].toInt(); repeat(257 - l) { out.write(b) } }
        }
        return out.toByteArray()
    }

    // ----------------------------------------------------------------- pages

    val catalog: PdfDict? get() = dict(trailer["Root"])

    @Synchronized
    fun pages(): List<PageNode> {
        pageList?.let { return it }
        val result = ArrayList<PageNode>()
        val root = catalog?.get("Pages")
        val seen = HashSet<Int>()
        fun walk(ref: Any?, inherited: PdfDict, depth: Int) {
            if (depth > 40 || result.size > 200_000) return
            val num = (ref as? PdfRef)?.num ?: -1
            if (num >= 0 && !seen.add(num)) return
            val d = dict(ref) ?: return
            val merged = HashMap<String, Any?>(inherited)
            for (key in INHERITED) d[key]?.let { merged[key] = it }
            val kids = list(d["Kids"])
            val type = name(d["Type"])
            if (kids != null && type != "Page") {
                for (k in kids) walk(k, merged, depth + 1)
            } else {
                result.add(PageNode(num, d, merged["Resources"], geometry(merged)))
            }
        }
        walk(root, emptyMap(), 0)
        pageList = result
        for ((i, p) in result.withIndex()) if (p.num >= 0) pageByNum[p.num] = i
        return result
    }

    fun pageIndex(num: Int): Int { pages(); return pageByNum[num] ?: -1 }

    private fun box(x: Any?): DoubleArray? {
        val l = list(x) ?: return null
        if (l.size < 4) return null
        val v = DoubleArray(4) { resolve(l[it]).num() }
        return doubleArrayOf(minOf(v[0], v[2]), minOf(v[1], v[3]), maxOf(v[0], v[2]), maxOf(v[1], v[3]))
    }

    private fun geometry(d: PdfDict): PageGeom {
        val media = box(d["MediaBox"]) ?: doubleArrayOf(0.0, 0.0, 612.0, 792.0)
        var b = media
        box(d["CropBox"])?.let { c ->
            val x0 = maxOf(c[0], media[0]); val y0 = maxOf(c[1], media[1])
            val x1 = minOf(c[2], media[2]); val y1 = minOf(c[3], media[3])
            if (x1 > x0 && y1 > y0) b = doubleArrayOf(x0, y0, x1, y1)
        }
        val rot = ((resolve(d["Rotate"]).int(0) % 360) + 360) % 360
        return PageGeom(b[0], b[1], b[2], b[3], if (rot % 90 == 0) rot else 0)
    }

    override fun close() {
        synchronized(this) { objects.clear(); objStms.clear() }
        src.close()
    }

    companion object {
        private val INHERITED = listOf("Resources", "MediaBox", "CropBox", "Rotate")

        /** Opens [file], or returns null when the file cannot be read as a PDF or needs a password. */
        fun open(file: File): PdfFile? = open(MappedSource(file))

        fun open(bytes: ByteArray): PdfFile? = open(ArraySource(bytes))

        private fun open(source: PdfSource): PdfFile? {
            val f = PdfFile(source)
            try {
                val start = f.startXref()
                var ok = start >= 0 && f.readXrefChain(start) && f.catalog?.get("Pages") != null
                if (!ok) {
                    f.xType = ByteArray(0); f.xA = IntArray(0); f.xB = IntArray(0)
                    f.objects.clear(); f.trailer = emptyMap()
                    f.rebuild()
                    ok = f.catalog?.get("Pages") != null
                }
                if (!ok) { f.close(); return null }
                f.encrypted = f.trailer["Encrypt"] != null
                if (f.encrypted) { f.close(); return null }
                return f
            } catch (t: Throwable) {
                runCatching { f.close() }
                return null
            }
        }
    }
}
