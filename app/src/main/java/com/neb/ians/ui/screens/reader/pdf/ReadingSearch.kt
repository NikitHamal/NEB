package com.neb.ians.ui.screens.reader.pdf

import androidx.compose.runtime.Immutable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString

/** One match in reading mode: the page, the block on it, and which occurrence inside that block. */
@Immutable
data class ReadHit(val page: Int, val block: Int, val nth: Int)

/** Search inside reading mode. It reads the reflowed text, so it works on every Android version. */
@Immutable
data class ReadSearch(
    val open: Boolean = false,
    val query: String = "",
    val running: Boolean = false,
    val scanned: Int = 0,
    val hits: List<ReadHit> = emptyList(),
    val index: Int = -1,
    /** Bumped whenever the reader should move to the current hit. */
    val jump: Int = 0
) {
    val current: ReadHit? get() = hits.getOrNull(index)

    /** The text that is marked on screen; short queries match too much to be useful. */
    val marking: String get() = if (open) query.trim().takeIf { it.length >= 2 }.orEmpty() else ""
}

/** The searchable text of a block, or null for blocks that carry none (figures, labels). */
internal fun readBlockText(block: Block): String? = when (block) {
    is HeadingBlock -> block.text
    is ParaBlock -> block.text
    is ItemBlock -> block.text
    is CodeBlock -> block.text
    is TableBlock -> block.rows.joinToString("\n") { it.cells.joinToString("\n") }
    else -> null
}

/** Start indexes of every non overlapping, case insensitive occurrence of [q] in [text]. */
internal fun occurrences(text: String, q: String): List<Int> {
    if (q.isEmpty() || text.length < q.length) return emptyList()
    val out = ArrayList<Int>(4)
    var from = 0
    while (true) {
        val at = text.indexOf(q, from, ignoreCase = true)
        if (at < 0) break
        out.add(at)
        from = at + q.length
    }
    return out
}

/** Every hit of [q] on a reflowed page, in reading order. */
internal fun findReadHits(page: ReflowPage, q: String): List<ReadHit> {
    var out: ArrayList<ReadHit>? = null
    page.blocks.forEachIndexed { i, block ->
        val text = readBlockText(block) ?: return@forEachIndexed
        val count = occurrences(text, q).size
        if (count > 0) {
            val list = out ?: ArrayList<ReadHit>().also { out = it }
            for (n in 0 until count) list.add(ReadHit(page.page, i, n))
        }
    }
    return out ?: emptyList()
}

internal val SearchMark = Color(0x66FFC83D)
internal val SearchMarkActive = Color(0xFFFFC83D)
internal val SearchMarkInk = Color(0xFF1C1B1A)

/** [this] with every occurrence of [q] marked; occurrence number [active] stands out (-1: none). */
internal fun AnnotatedString.marked(q: String, active: Int): AnnotatedString {
    if (q.isEmpty()) return this
    val starts = occurrences(text, q)
    if (starts.isEmpty()) return this
    val base = this
    return buildAnnotatedString {
        append(base)
        starts.forEachIndexed { n, s ->
            val style = if (n == active) SpanStyle(background = SearchMarkActive, color = SearchMarkInk) else SpanStyle(background = SearchMark)
            addStyle(style, s, s + q.length)
        }
    }
}
