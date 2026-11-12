package com.neb.ians.ui.screens.reader.pdf

import android.util.LruCache
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import java.io.Closeable
import java.io.File

/**
 * Everything the reader knows about a document beyond its pixels: links, the table of contents and
 * the reflowed text for reading mode. Opened lazily on a background thread, one page at a time, with
 * small caches (the file itself is memory mapped, never loaded). When the file cannot be read this
 * way ([available] is false) the reader simply has no links and no reading mode.
 */
class PdfStructureEngine(private val file: File, private val renderedPages: Int) : Closeable {
    private val mutex = Mutex()
    private var pdf: PdfFile? = null
    private var extractor: PdfTextExtractor? = null
    private var stats: ReflowStats? = null
    private var opened = false
    @Volatile private var closed = false
    @Volatile var available: Boolean = true
        private set

    private val linkCache = object : LruCache<Int, List<PdfLink>>(160) {}
    private val reflowCache = object : LruCache<Int, ReflowPage>(48) {}
    private var outlineCache: List<OutlineItem>? = null

    private fun ensureOpen(): PdfFile? {
        if (!opened) {
            opened = true
            val f = PdfFile.open(file)
            if (f == null || f.pages().size != renderedPages) {
                f?.close()
                available = false
                return null
            }
            pdf = f
            extractor = PdfTextExtractor(f)
        }
        return pdf
    }

    /**
     * The book's own structure (see `notes/pipeline/reading.py`) unpacked into [cacheRoot], or null when this
     * file carries none (an older build, or someone else's PDF): then reading mode reflows the drawn page.
     */
    suspend fun readingBook(cacheRoot: File): File? = withContext(Dispatchers.IO) {
        val dir = File(cacheRoot, "reading/" + file.name.replace(Regex("[^A-Za-z0-9._-]"), "_") + "-" + file.length())
        if (File(dir, "meta.json").exists()) return@withContext dir
        mutex.withLock {
            if (closed) return@withLock null
            val f = ensureOpen() ?: return@withLock null
            val bytes = runCatching { f.embeddedFile(ReadingBookFiles.ATTACHMENT) }.getOrNull() ?: return@withLock null
            runCatching { ReadingBookFiles.unpack(bytes, dir) }.getOrNull()
        }
    }

    /** Links on [page]; empty when there are none or the file cannot be read. */
    suspend fun links(page: Int): List<PdfLink> {
        linkCache.get(page)?.let { return it }
        return withContext(Dispatchers.IO) {
            mutex.withLock {
                linkCache.get(page)?.let { return@withLock it }
                if (closed) return@withLock emptyList()
                val f = ensureOpen() ?: return@withLock emptyList()
                val result = runCatching { f.links(page) }.getOrDefault(emptyList())
                linkCache.put(page, result)
                result
            }
        }
    }

    /** True when any page is known to carry links; cheap hint for the UI. */
    fun cachedLinks(page: Int): List<PdfLink>? = linkCache.get(page)

    suspend fun outline(): List<OutlineItem> = withContext(Dispatchers.IO) {
        mutex.withLock {
            outlineCache?.let { return@withLock it }
            if (closed) return@withLock emptyList()
            val f = ensureOpen() ?: return@withLock emptyList()
            val result = runCatching { f.outline() }.getOrDefault(emptyList())
            outlineCache = result
            result
        }
    }

    fun cachedReflow(page: Int): ReflowPage? = reflowCache.get(page)

    /** The reflowed content of [page], or null when it cannot be read. */
    suspend fun reflow(page: Int): ReflowPage? {
        reflowCache.get(page)?.let { return it }
        return withContext(Dispatchers.Default) {
            mutex.withLock {
                reflowCache.get(page)?.let { return@withLock it }
                if (closed) return@withLock null
                val f = ensureOpen() ?: return@withLock null
                val ex = extractor ?: return@withLock null
                val st = stats ?: runCatching {
                    val n = f.pages().size
                    val picks = if (n <= 12) (0 until n).toList() else (0 until 12).map { 1 + it * (n - 2) / 12 }
                    PdfReflow.stats(picks.mapNotNull { runCatching { ex.extract(it) }.getOrNull() })
                }.getOrNull()?.also { stats = it } ?: return@withLock null
                val content = runCatching { ex.extract(page) }.getOrNull() ?: return@withLock null
                val result = runCatching { PdfReflow.build(page, content, st, f.links(page)) }.getOrNull()
                if (result != null) reflowCache.put(page, result)
                result
            }
        }
    }

    /** Body text size of the document in points, so pictures can scale with the reading type size. */
    fun bodyPoints(): Float = stats?.body ?: 10.5f

    override fun close() {
        closed = true
        linkCache.evictAll(); reflowCache.evictAll()
        // a call in flight finishes first; the lock makes sure nothing is reading while the file closes
        if (mutex.tryLock()) {
            try { pdf?.close(); pdf = null; extractor = null } finally { mutex.unlock() }
        }
    }
}
