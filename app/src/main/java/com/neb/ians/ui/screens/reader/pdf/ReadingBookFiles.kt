package com.neb.ians.ui.screens.reader.pdf

import java.io.File
import java.io.FileOutputStream
import java.io.InputStream
import java.util.zip.GZIPInputStream

/** The payload the print pipeline attaches to a book, and how it is unpacked. */
internal object ReadingBookFiles {
    const val ATTACHMENT = "neb-reading.tgz"

    /** Unpack the solid tar.gz into [dest] (written beside it and renamed, so a half unpacked book is never used). */
    fun unpack(bytes: ByteArray, dest: File): File {
        val tmp = File(dest.parentFile, dest.name + ".part")
        tmp.deleteRecursively(); tmp.mkdirs()
        val root = tmp.canonicalPath + File.separator
        GZIPInputStream(bytes.inputStream().buffered(1 shl 16)).use { gz ->
            val h = ByteArray(512)
            while (readFully(gz, h)) {
                if (h.all { it == 0.toByte() }) break
                val name = cstr(h, 0, 100)
                val prefix = cstr(h, 345, 155)
                val size = cstr(h, 124, 12).trim().ifEmpty { "0" }.toLong(8)
                val type = h[156].toInt().toChar()
                val out = File(tmp, if (prefix.isNotEmpty()) "$prefix/$name" else name)
                if ((type == '0' || type == '\u0000') && out.canonicalPath.startsWith(root)) {
                    out.parentFile?.mkdirs()
                    FileOutputStream(out).use { o ->
                        var left = size
                        val buf = ByteArray(64 * 1024)
                        while (left > 0) {
                            val n = gz.read(buf, 0, minOf(buf.size.toLong(), left).toInt())
                            if (n < 0) break
                            o.write(buf, 0, n); left -= n
                        }
                    }
                } else skip(gz, size)
                val pad = (512 - size % 512) % 512
                skip(gz, pad)
            }
        }
        dest.deleteRecursively()
        check(tmp.renameTo(dest)) { "reading book: rename failed" }
        return dest
    }

    private fun cstr(b: ByteArray, off: Int, len: Int): String {
        var e = off
        while (e < off + len && b[e] != 0.toByte()) e++
        return String(b, off, e - off, Charsets.UTF_8)
    }

    private fun readFully(i: InputStream, b: ByteArray): Boolean {
        var n = 0
        while (n < b.size) { val r = i.read(b, n, b.size - n); if (r < 0) return false; n += r }
        return true
    }

    private fun skip(i: InputStream, count: Long) {
        var left = count
        val buf = ByteArray(8192)
        while (left > 0) { val r = i.read(buf, 0, minOf(buf.size.toLong(), left).toInt()); if (r < 0) return; left -= r }
    }
}

