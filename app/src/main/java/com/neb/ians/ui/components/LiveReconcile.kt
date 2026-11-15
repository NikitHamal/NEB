package com.neb.ians.ui.components

import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.input.TextFieldValue

/**
 * Every edit to a composer goes through [apply] before it is stored, so the text a field holds is always valid Markdown
 * and the live view never has a frame where a marker shows. Plain typing returns at once; the work happens only next to
 * markers: a space typed at the end of bold text moves outside the markers, Enter inside a style closes and reopens it,
 * Backspace never eats half of a hidden marker (it deletes the character you can see), and backspacing a line start
 * removes the whole bullet, number, quote or heading mark in one go.
 */
object LiveReconcile {
    private const val Z = '\u200B'
    private val prefixRe = Regex("^(#{1,3} |> |[-*+] \\[[ xX]] |[-*+] |\\d+[.)] )")

    private class Edit(val start: Int, val end: Int, val text: String, val caret: Int)

    fun apply(old: TextFieldValue, new: TextFieldValue): TextFieldValue {
        val o = old.text
        val n = new.text
        if (o == n) return prune(new)
        if (n.length >= o.length && !hasMarks(o)) return new
        var p = 0
        val minLen = minOf(o.length, n.length)
        while (p < minLen && o[p] == n[p]) p++
        var sfx = 0
        while (sfx < minLen - p && o[o.length - 1 - sfx] == n[n.length - 1 - sfx]) sfx++
        val oEnd = o.length - sfx
        val nEnd = n.length - sfx
        if (nEnd == p && oEnd > p) deletion(old, p, oEnd)?.let { return it }
        return fixPairs(old, new, p, oEnd, nEnd)
    }

    private fun hasMarks(s: String): Boolean {
        for (ch in s) if (ch == '*' || ch == '~' || ch == '`' || ch == '_' || ch == Z) return true
        return false
    }

    /** Pure deletion of [p, oEnd) from the old text; null when it is an ordinary deletion. */
    private fun deletion(old: TextFieldValue, p: Int, oEnd: Int): TextFieldValue? {
        val o = old.text
        val ls = o.lastIndexOf('\n', p - 1) + 1
        var le = o.indexOf('\n', ls)
        if (le < 0) le = o.length
        val pre = prefixRe.find(o.substring(ls, le))
        if (pre != null) {
            val len = pre.value.length
            if (p >= ls && oEnd <= ls + len && !(p == ls && oEnd == ls + len)) {
                return TextFieldValue(o.removeRange(ls, ls + len), TextRange(ls))
            }
        }
        val lt = LiveMarkdown.structure(o)
        for (i in p until oEnd) if (!lt.hidden[i]) return null
        val empty = lt.pairs.firstOrNull { pr ->
            val m = pr.mark.length
            pr.close == pr.open + m && (p in pr.open until pr.open + m || p in pr.close until pr.close + m)
        }
        if (empty != null) return TextFieldValue(o.removeRange(empty.open, empty.close + empty.mark.length), TextRange(empty.open))
        var idx = p - 1
        while (idx >= 0 && lt.hidden[idx]) idx--
        if (idx < 0) return TextFieldValue(o, old.selection)
        val from = if (o[idx].isLowSurrogate() && idx > 0 && o[idx - 1].isHighSurrogate()) idx - 1 else idx
        return apply(old, TextFieldValue(o.removeRange(from, idx + 1), TextRange(from)))
    }

    private fun fixPairs(old: TextFieldValue, new: TextFieldValue, p: Int, oEnd: Int, nEnd: Int): TextFieldValue {
        val o = old.text
        val n = new.text
        val lt = LiveMarkdown.structure(o)
        if (lt.pairs.isEmpty()) return new
        val delta = nEnd - oEnd
        fun map(a: Int, len: Int) = if (a + len <= p) a else if (a >= oEnd) a + delta else -1
        val sel = new.selection
        val caret = if (sel.collapsed) sel.start else -1
        val edits = ArrayList<Edit>()
        for (pair in lt.pairs) {
            val m = pair.mark.length
            val po = map(pair.open, m)
            val pc = map(pair.close, m)
            if (po < 0 && pc < 0) continue
            if (po < 0 || pc < 0) {
                val at = if (po < 0) pc else po
                edits.add(Edit(at, at + m, "", -1))
                continue
            }
            if (pc < po + m || pc + m > n.length) continue
            val inner = n.substring(po + m, pc)
            val ci = if (caret in (po + m)..pc) caret - (po + m) else -1
            val oldInner = o.substring(pair.open + m, pair.close)
            val pendingOk = ci >= 0 &&
                (inner.indexOf(Z) >= 0 || inner.indexOf('\n') >= 0 || oldInner.any { it != Z && !it.isWhitespace() })
            val r = rebuildPair(inner, pair.mark, ci, pendingOk)
            if (r.text != n.substring(po, pc + m)) edits.add(Edit(po, pc + m, r.text, if (ci >= 0) r.caret else -1))
        }
        if (edits.isEmpty()) return new
        edits.sortByDescending { it.start }
        val applied = ArrayList<Edit>()
        var floor = Int.MAX_VALUE
        val sb = StringBuilder(n)
        for (e in edits) {
            if (e.end > floor) continue
            sb.replace(e.start, e.end, e.text)
            applied.add(e)
            floor = e.start
        }
        fun shiftOf(limit: Int): Int = applied.filter { it.end <= limit }.sumOf { it.text.length - (it.end - it.start) }
        fun mapCaret(c: Int): Int {
            val hit = applied.firstOrNull { c > it.start && c < it.end }
            if (hit != null) {
                val base = hit.start + shiftOf(hit.start)
                return base + (if (hit.caret >= 0) hit.caret else (c - hit.start).coerceAtMost(hit.text.length))
            }
            return c + shiftOf(c)
        }
        val text = sb.toString()
        val a = mapCaret(sel.start).coerceIn(0, text.length)
        val b = mapCaret(sel.end).coerceIn(0, text.length)
        return TextFieldValue(text, TextRange(a, b))
    }

    /** A style armed with nothing typed yet is dropped once the caret leaves it. */
    private fun prune(v: TextFieldValue): TextFieldValue {
        val t = v.text
        if (t.indexOf(Z) < 0) return v
        val lt = LiveMarkdown.structure(t)
        val sel = v.selection
        val dead = lt.pairs.filter { pr ->
            val m = pr.mark.length
            pr.close - pr.open - m == 1 && t[pr.open + m] == Z && (sel.max < pr.open + m || sel.min > pr.close)
        }.sortedByDescending { it.open }
        if (dead.isEmpty()) return v
        val sb = StringBuilder(t)
        for (d in dead) sb.delete(d.open, d.close + d.mark.length)
        fun mapPos(c: Int) = c - dead.sumOf { if (it.close + it.mark.length <= c) it.close + it.mark.length - it.open else 0 }
        val text = sb.toString()
        return TextFieldValue(text, TextRange(mapPos(sel.start).coerceIn(0, text.length), mapPos(sel.end).coerceIn(0, text.length)))
    }
}
