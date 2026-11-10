package com.neb.ians.ui.screens.reader.pdf

import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

/*
 * Turns what a page draws into what a person reads: headings, paragraphs, lists, code, tables, and
 * the pictures (diagrams, equations drawn as outlines, photos) kept as crops of the real page.
 * The reading mode shows these blocks in a column that reflows to the screen and the type size.
 * Pure Kotlin on purpose; see PdfSyntax.kt.
 */

const val SPAN_SUP = 8
const val SPAN_SUB = 16

data class Span(val text: String, val flags: Int = 0, val href: String? = null) {
    val bold get() = flags and ST_BOLD != 0
    val italic get() = flags and ST_ITALIC != 0
    val mono get() = flags and ST_MONO != 0
    val sup get() = flags and SPAN_SUP != 0
    val sub get() = flags and SPAN_SUB != 0
}

/** [box] is the id of the tonal card (callout, answer key, note) the block sits in, 0 when it is on the page itself. */
sealed class Block { var box: Int = 0 }
class HeadingBlock(val level: Int, val text: String, val jump: Int) : Block()
class ParaBlock(val spans: List<Span>, val jump: Int, val startsLower: Boolean, val endsOpen: Boolean) : Block() {
    val text: String by lazy(LazyThreadSafetyMode.NONE) { spans.joinToString("") { it.text } }
}
/** [choiceCols] is above 0 for a lettered choice (a to h): how many choices stood side by side on the printed line. */
class ItemBlock(val marker: String, val spans: List<Span>, val depth: Int, val jump: Int, val choiceCols: Int = 0) : Block() {
    val text: String by lazy(LazyThreadSafetyMode.NONE) { spans.joinToString("") { it.text } }
}
class CodeBlock(val text: String) : Block()
class LabelBlock(val text: String) : Block()
class TableRow(val cells: List<String>, val jump: Int)
class TableBlock(val rows: List<TableRow>, val header: Boolean) : Block()

/** A crop of the page. [widthPts] and [heightPts] are its size on the page, so it can scale with the text. */
class FigureBlock(
    val page: Int, val rect: FRect, val widthPts: Float, val heightPts: Float, val equation: Boolean,
    /** The equation as outlines when it can be drawn from them; null: show the crop of the page. */
    val vec: VectorArt? = null
) : Block()

/** A small picture (typeset maths) that sits inside a line of text. Its place in the text is [MATH_BASE] plus its index. */
class InlineImg(
    val page: Int, val rect: FRect, val widthPts: Float, val heightPts: Float,
    /** The formula as outlines (null: use the crop), the baseline of its line measured from the formula's top, and that line's type size. */
    val vec: VectorArt? = null, val base: Float = 0f, val em: Float = 0f
) {
    /** Where the middle of the text of the line sits inside the formula's box, in points from its top. */
    val center: Float get() = base - 0.36f * em
    /** Half the height of the slot: the formula sits centred on the text's middle, so it lines up with the baseline. */
    val half: Float get() = PdfVector.half(center, heightPts)
}

class ReflowPage(val page: Int, val blocks: List<Block>, val words: Int, val inlines: List<InlineImg> = emptyList())

/** Private use characters stand in the text for the pictures set inside it; the reader swaps them for the crops. */
const val MATH_BASE = 0xE000
fun isMathChar(c: Char): Boolean = c.code >= MATH_BASE && c.code < MATH_BASE + 0x400

class ReflowStats(val body: Float, val headSizes: List<Float>, val furniture: Set<String>, val leading: Float)

internal class Cell(val x0: Float, val x1: Float, val spans: List<Span>) {
    val text: String get() = spans.joinToString("") { it.text }.trim()
}

internal class Line(val runs: List<Run>, val size: Float, val base: Float) {
    val x0 = runs.minOf { it.x0 }
    val x1 = runs.maxOf { it.x1 }
    val top get() = base - size * 0.95f
    val bottom get() = base + size * 0.32f
    var cells: List<Cell> = emptyList()
    var bold = false
    var mono = false
    var unmapped = false
    var jump = -1
    val text: String get() = cells.joinToString(" ") { it.text }
    val spans: List<Span>
        get() {
            val out = ArrayList<Span>()
            cells.forEachIndexed { i, c ->
                if (i > 0) out.add(Span(" "))
                out.addAll(c.spans)
            }
            return out
        }
    val chars: Int get() = runs.sumOf { it.text.length }
}

private class Box(var l: Float, var t: Float, var r: Float, var b: Float) {
    fun union(o: Box) { l = min(l, o.l); t = min(t, o.t); r = max(r, o.r); b = max(b, o.b) }
    fun intersects(o: Box, pad: Float = 0f) = l - pad <= o.r && r + pad >= o.l && t - pad <= o.b && b + pad >= o.t
    fun contains(o: Box) = l <= o.l + 1 && r >= o.r - 1 && t <= o.t + 1 && b >= o.b - 1
    val w get() = r - l
    val h get() = b - t
    val area get() = max(0f, w) * max(0f, h)
}

internal object PdfReflow {

    // ----------------------------------------------------------------- lines

    private fun clean(s: String): String {
        val sb = StringBuilder(s.length)
        for (ch in s) {
            when {
                ch == '\u00A0' || ch == '\u2009' || ch == '\u202F' || ch == '\u2002' || ch == '\u2003' -> sb.append(' ')
                ch == '\u00AD' || ch == '\uFFFC' || ch == '\u200B' || ch == '\u200C' || ch == '\u200D' || ch == '\uFEFF' -> {}
                ch < ' ' -> {}
                else -> sb.append(ch)
            }
        }
        return sb.toString()
    }

    internal fun groupLines(runs: List<Run>): List<Line> {
        if (runs.isEmpty()) return emptyList()
        val sorted = runs.sortedWith(compareBy<Run>({ it.base }, { it.x0 }))
        val groups = ArrayList<ArrayList<Run>>()
        var cur: ArrayList<Run>? = null
        var curBase = 0f
        var curSize = 0f
        for (r in sorted) {
            val c = cur
            val mx = max(r.size, curSize)
            val differ = c != null && (r.size < curSize * 0.82f || curSize < r.size * 0.82f)
            val tol = if (differ) 0.55f * mx else 0.3f * mx
            if (c != null && abs(r.base - curBase) <= tol) {
                c.add(r)
                if (r.size > curSize) { curSize = r.size; curBase = r.base }
            } else {
                cur = arrayListOf(r); groups.add(cur)
                curBase = r.base; curSize = r.size
            }
        }
        val lines = ArrayList<Line>(groups.size)
        for (g in groups) {
            val big = g.maxByOrNull { it.size * (1 + it.text.length.coerceAtMost(8) * 0.01f) }!!
            val line = Line(g.sortedBy { it.x0 }, big.size, big.base)
            buildCells(line)
            if (line.text.isNotBlank()) lines.add(line)
        }
        return lines.sortedBy { it.base }
    }

    private fun buildCells(line: Line) {
        val cells = ArrayList<Cell>()
        var spans = ArrayList<Span>()
        var cellX0 = 0f
        var prev: Run? = null
        var prevEndsSpace = true
        var boldAll = true
        var monoAll = true
        var any = false
        var jump = -1
        fun add(text: String, flags: Int, href: String?) {
            if (text.isEmpty()) return
            val last = spans.lastOrNull()
            if (last != null && last.flags == flags && last.href == href) spans[spans.size - 1] = Span(last.text + text, flags, href)
            else spans.add(Span(text, flags, href))
        }
        for (r in line.runs) {
            val text = clean(r.text)
            if (r.unmapped) line.unmapped = true
            if (text.isBlank()) {
                if (prev != null && spans.isNotEmpty() && !prevEndsSpace) add(" ", spans.last().flags, null)
                if (prev != null) prevEndsSpace = true
                continue
            }
            any = true
            if (r.style and ST_BOLD == 0) boldAll = false
            if (r.style and ST_MONO == 0) monoAll = false
            if (r.jump >= 0 && jump < 0) jump = r.jump
            var flags = r.style
            if (r.size < line.size * 0.82f) {
                if (r.base < line.base - line.size * 0.12f) flags = flags or SPAN_SUP
                else if (r.base > line.base + line.size * 0.12f) flags = flags or SPAN_SUB
            }
            val p = prev
            if (p == null) {
                cellX0 = r.x0
            } else {
                val gap = r.x0 - p.x1
                val ref = max(p.size, r.size)
                val badge = text.trim().length == 1 && text.trim()[0].lowercaseChar() in 'a'..'h' && r.size < p.size * 0.85f &&
                    abs(r.base - line.base) < 0.14f * line.size && gap > 0.5f * ref && !p.unmapped && clean(p.text).isNotBlank()
                if (badge || (gap > 2.0f * ref && gap > 12f)) {
                    cells.add(Cell(cellX0, p.x1, spans)); spans = ArrayList(); cellX0 = r.x0; prevEndsSpace = true
                } else if (gap > 0.15f * ref && !prevEndsSpace && !text.startsWith(" ")) {
                    add(" ", spans.lastOrNull()?.flags ?: 0, null)
                }
            }
            val lead = if (spans.isEmpty()) text.trimStart() else text
            add(lead, flags, r.href)
            prevEndsSpace = text.endsWith(" ")
            prev = r
        }
        if (prev != null) cells.add(Cell(cellX0, prev.x1, spans))
        line.cells = cells
        line.bold = any && boldAll
        line.mono = any && monoAll
        line.jump = jump
    }

    // ----------------------------------------------------------------- stats

    private fun norm(t: String) = t.lowercase().replace(Regex("[0-9]+"), "#").replace(Regex("\\s+"), " ").trim()

    private fun inBand(l: Line, h: Float) = l.base < 0.085f * h || l.base > 0.925f * h

    fun stats(samples: List<PageContent>): ReflowStats {
        val sizeChars = HashMap<Int, Int>()
        val furn = HashMap<String, Int>()
        val diffs = ArrayList<Float>()
        for (c in samples) {
            val lines = groupLines(c.runs.filter { !it.hidden })
            val seen = HashSet<String>()
            val mid = ArrayList<Line>()
            for (l in lines) {
                if (inBand(l, c.height)) { for (cell in l.cells) seen.add(norm(cell.text)); continue }
                mid.add(l)
                val key = Math.round(l.size * 2f)
                sizeChars[key] = (sizeChars[key] ?: 0) + l.chars
            }
            for (s in seen) furn[s] = (furn[s] ?: 0) + 1
            for (i in 1 until mid.size) {
                val a = mid[i - 1]; val b = mid[i]
                val d = b.base - a.base
                if (abs(a.size - b.size) < 0.6f && d > a.size * 1.0f && d < a.size * 2.4f) diffs.add(d / a.size)
            }
        }
        val bodyKey = sizeChars.maxByOrNull { it.value }?.key ?: 22
        val body = bodyKey / 2f
        val heads = sizeChars.filter { it.key / 2f >= body * 1.15f && it.value >= 3 }.keys.sortedDescending().map { it / 2f }
        val merged = ArrayList<Float>()
        for (h in heads) if (merged.isEmpty() || merged.last() - h > 0.12f * h) merged.add(h)
        val need = max(2, Math.ceil(samples.size * 0.34).toInt())
        val furniture = furn.filter { it.value >= need && it.key.isNotBlank() }.keys
        val leading = if (diffs.isEmpty()) 1.45f else diffs.sorted()[diffs.size / 2]
        return ReflowStats(body, merged.take(4), furniture, leading.coerceIn(1.1f, 2.0f))
    }

    // ----------------------------------------------------------------- build

    private val BULLET = Regex("^([\\u2022\\u00B7\\u25AA\\u25E6\\u2023\\u25CF\\u25CB\\u25A0\\u25A1\\u2013\\u2014\\u2713\\u2714*]|-)\\s+")
    private val NUMBERED = Regex("^(\\(?\\d{1,3}[.)]|\\(?[a-z]\\)|\\(?[ivx]{1,4}[.)])\\s+")
    private val DASHES = setOf("\u2013", "\u2014", "-")
    private val TERMINAL = Regex("[.!?:;\\u201D\")\\u2026]$")

    fun build(page: Int, c: PageContent, st: ReflowStats, links: List<PdfLink>): ReflowPage {
        val W = c.width; val H = c.height
        assignLinks(c.runs, links, W, H)
        var runs = c.runs.filter { !it.hidden }
        val visibleChars = runs.sumOf { it.text.length }
        val hiddenRuns = c.runs.filter { it.hidden }
        val ocr = visibleChars < 10 && hiddenRuns.sumOf { it.text.length } >= 10
        if (ocr) runs = hiddenRuns
        val body = st.body

        // tables the print draws cell by cell (a filled box per cell): the text and formulas inside each box belong to that cell
        val grids = if (ocr) emptyList() else findGrids(c, body)
        val cellRuns = grids.map { g -> g.rows.map { r -> r.map { ArrayList<Run>() } } }
        if (grids.isNotEmpty()) {
            val keep = ArrayList<Run>()
            for (r in runs) {
                val cx = (r.x0 + r.x1) / 2f; val cy = r.base - r.size * 0.3f
                var placed = false
                loop@ for ((gi, g) in grids.withIndex()) for ((ri, row) in g.rows.withIndex()) for ((ci, cell) in row.withIndex()) {
                    if (cx >= cell.l - 1f && cx <= cell.r + 1f && cy >= cell.t - 1f && cy <= cell.b + 1f) { cellRuns[gi][ri][ci].add(r); placed = true; break@loop }
                }
                if (!placed) keep.add(r)
            }
            runs = keep
        }
        val grouped = groupLines(runs)

        // pictures first: they take the text that is part of them
        val figs = figures(c, grouped, st, ocr || visibleChars > 200)
        val absorbed = HashSet<Line>()
        val items = ArrayList<Pair<Float, Block>>()
        for (f in figs) {
            if (f.owner != null) continue
            val r = f.box
            for (l in grouped) {
                val cx = (l.x0 + l.x1) / 2f
                val cy = l.base - l.size * 0.3f
                if (cx >= r.l - 2 && cx <= r.r + 2 && cy >= r.t - 2 && cy <= r.b + 2) absorbed.add(l)
            }
        }
        // small pictures inside a line of text (typeset maths) become a character in that line, so the
        // line stays a line: a question with a formula in it is one paragraph, not text, a figure, text
        val inlines = ArrayList<InlineImg>()
        val marks = LinkedHashMap<Line, ArrayList<Run>>()
        // a formula inside a table cell is a character in that cell's text
        val cellFigs = HashSet<Fig>()
        if (grids.isNotEmpty()) for (f in figs) {
            val r = f.box
            val cx = (r.l + r.r) / 2f; val cy = (r.t + r.b) / 2f
            var hit: Triple<Int, Int, Int>? = null
            loop@ for ((gi, g) in grids.withIndex()) for ((ri, row) in g.rows.withIndex()) for ((ci, cell) in row.withIndex()) {
                if (cx >= cell.l && cx <= cell.r && cy >= cell.t && cy <= cell.b) { hit = Triple(gi, ri, ci); break@loop }
            }
            val h = hit ?: continue
            val rect = FRect((r.l / W).coerceIn(0f, 1f), (r.t / H).coerceIn(0f, 1f), (r.r / W).coerceIn(0f, 1f), (r.b / H).coerceIn(0f, 1f))
            if (rect.w < 0.002f || rect.h < 0.002f || inlines.size >= 0x3F0) continue
            val cellList = cellRuns[h.first][h.second][h.third]
            val near = cellList.filter { it.text.isNotBlank() && !isMathChar(it.text[0]) }.minByOrNull { abs((it.base - it.size * 0.3f) - cy) }
            val em = near?.size ?: body
            val base = if (near != null && abs((near.base - near.size * 0.3f) - cy) < 0.9f * near.size) near.base else cy + 0.36f * em
            val k = inlines.size
            val vec = PdfVector.of(c, r.l, r.t, r.r, r.b, !f.equation && r.h > 4.6f * body)
            inlines.add(InlineImg(page, rect, rect.w * W, rect.h * H, vec, base - r.t, em))
            cellList.add(Run((MATH_BASE + k).toChar().toString(), r.l, r.r, base, em, 0, false, false))
            cellFigs.add(f)
        }
        for (f in figs) {
            val owner = f.owner
            if (f in cellFigs) continue
            if (owner == null || owner in absorbed) continue
            val r = f.box
            val rect = FRect((r.l / W).coerceIn(0f, 1f), (r.t / H).coerceIn(0f, 1f), (r.r / W).coerceIn(0f, 1f), (r.b / H).coerceIn(0f, 1f))
            if (rect.w < 0.002f || rect.h < 0.002f || inlines.size >= 0x3F0) {
                f.inlineFailed = true
                continue
            }
            val k = inlines.size
            val vec = PdfVector.of(c, r.l, r.t, r.r, r.b)
            inlines.add(InlineImg(page, rect, rect.w * W, rect.h * H, vec, owner.base - r.t, owner.size))
            marks.getOrPut(owner) { ArrayList() }.add(Run((MATH_BASE + k).toChar().toString(), r.l, r.r, owner.base, owner.size, 0, false, false))
        }
        val all = grouped.map { l ->
            val extra = marks[l]
            if (extra == null) l else {
                val nl = Line((l.runs + extra).sortedBy { it.x0 }, l.size, l.base)
                buildCells(nl)
                nl
            }
        }
        for (f in figs) {
            if (f in cellFigs) continue
            if (f.owner != null && !f.inlineFailed && f.owner !in absorbed) continue
            val r = f.box
            val rect = FRect((r.l / W).coerceIn(0f, 1f), (r.t / H).coerceIn(0f, 1f), (r.r / W).coerceIn(0f, 1f), (r.b / H).coerceIn(0f, 1f))
            if (rect.w < 0.01f || rect.h < 0.004f) continue
            val vec = PdfVector.of(c, r.l, r.t, r.r, r.b, !f.equation)
            items.add(r.t to FigureBlock(page, rect, rect.w * W, rect.h * H, f.equation, vec))
        }

        for ((gi, g) in grids.withIndex()) {
            val out = ArrayList<TableRow>()
            var head = false
            g.rows.forEachIndexed { ri, row ->
                val cellLines = row.indices.map { ci -> groupLines(cellRuns[gi][ri][ci]) }
                if (ri == 0) head = cellLines.filter { it.isNotEmpty() }.let { ls -> ls.isNotEmpty() && ls.all { l -> l.all { it.bold } } }
                out.add(TableRow(cellLines.map { ls -> ls.joinToString(" ") { it.text.trim() }.replace(Regex("\\s+"), " ").trim() }, -1))
            }
            if (out.any { r -> r.cells.any { it.isNotEmpty() } }) items.add(g.rows[0][0].t to TableBlock(out, head))
        }

        val lines = all.filter { it !in absorbed && !(inBand(it, H) && (isPageNumber(it.text) || it.cells.any { c -> norm(c.text) in st.furniture || isPageNumber(c.text) })) }
        val body10 = lines.filter { abs(it.size - body) < body * 0.15f && it.text.length > 24 }
        val left = if (body10.isNotEmpty()) body10.map { it.x0 }.sorted()[body10.size / 10] else (lines.minOfOrNull { it.x0 } ?: 0f)

        var i = 0
        val n = lines.size
        while (i < n) {
            val line = lines[i]
            val top = line.top
            // lettered choices set in a row or a grid (a 8   b 12   c 19   d 30) are choices, never a table
            if (!line.mono) {
                val opts = optionRows(lines, i)
                if (opts != null) {
                    for (b in opts.first) items.add(top to b)
                    i = opts.second; continue
                }
            }
            // table
            if (line.cells.size >= 2 && !line.mono) {
                val t = table(lines, i, 0)
                if (t != null) { items.add(top to t.first); i = t.second; continue }
            } else if (line.cells.size == 1 && !line.mono && i + 1 < n && lines[i + 1].cells.size >= 2 && !lines[i + 1].mono &&
                lines[i + 1].base - line.base < 1.2f * line.size && line.size <= body * 1.02f
            ) {
                val t = table(lines, i + 1, 1)
                if (t != null) { items.add(top to t.first); i = t.second; continue }
            }
            // code
            if (line.mono && line.text.length >= 2) {
                var j = i
                val sb = StringBuilder()
                val unit = line.size * 0.6f
                var minX = Float.MAX_VALUE
                while (j < n && lines[j].mono && (j == i || lines[j].base - lines[j - 1].base < lines[j - 1].size * 2.4f)) { minX = min(minX, lines[j].x0); j++ }
                for (k in i until j) {
                    val l = lines[k]
                    if (k > i) {
                        val blank = ((l.base - lines[k - 1].base) / (lines[k - 1].size * 1.5f)).toInt() - 1
                        repeat(blank.coerceIn(0, 2)) { sb.append('\n') }
                        sb.append('\n')
                    }
                    repeat(((l.x0 - minX) / unit).toInt().coerceIn(0, 40)) { sb.append(' ') }
                    sb.append(l.cells.joinToString("  ") { it.text })
                }
                items.add(top to CodeBlock(sb.toString())); i = j; continue
            }
            // heading by size
            val level = headingLevel(line, st)
            if (level > 0) {
                var j = i + 1
                val sb = StringBuilder(line.text)
                while (j < n && headingLevel(lines[j], st) > 0 && lines[j].size >= line.size * 0.84f && lines[j].size <= line.size * 1.06f && lines[j].base - lines[j - 1].base < line.size * 1.7f && lines[j].cells.size == 1) { sb.append(' ').append(lines[j].text); j++ }
                items.add(top to HeadingBlock(level, sb.toString().trim(), jumpOf(lines, i, j)))
                i = j; continue
            }
            // label: short bold capitals
            if (line.bold && isCaps(line.text) && line.text.length in 3..80 && line.size <= body * 1.05f) {
                items.add(top to LabelBlock(line.text)); i++; continue
            }
            // list item
            val marker = markerOf(line)
            if (marker != null) {
                val first = line.runs.firstOrNull { clean(it.text).isNotBlank() }
                val second = line.runs.firstOrNull { it !== first && it.x0 >= (first?.x1 ?: 0f) - 0.5f && clean(it.text).isNotBlank() }
                val textX = if (first != null && clean(first.text).trim() == marker && second != null) second.x0 else line.x0 + line.size * 1.3f
                var j = i + 1
                val spans = ArrayList<Span>(stripMarker(line, marker))
                while (j < n) {
                    val l = lines[j]
                    val gap = l.base - lines[j - 1].base
                    val chip = isMarkChip(l.text)
                    if (gap > st.leading * line.size * 1.22f || (!chip && abs(l.size - line.size) > line.size * 0.15f)) break
                    if (l.cells.size != 1 || markerOf(l) != null || l.mono || l.x0 < textX - line.size * 0.8f) break
                    if (headingLevel(l, st) > 0) break
                    joinInto(spans, l.spans)
                    j++
                }
                val depth = ((line.x0 - left) / (line.size * 1.8f)).let { Math.round(it) }.coerceIn(0, 3)
                items.add(top to ItemBlock(marker.trim(), spans, depth, jumpOf(lines, i, j)))
                i = j; continue
            }
            // bold-only short line: a sub heading
            if (line.bold && line.cells.size == 1 && line.text.length <= 100 && !TERMINAL.containsMatchIn(line.text.trim()) &&
                (i + 1 >= n || lines[i + 1].base - line.base > line.size * 1.05f) && line.size >= body * 0.9f
            ) {
                // only when what follows is not more of the same line
                val lvl = min(st.headSizes.size + 1, 4).coerceAtLeast(2)
                items.add(top to HeadingBlock(lvl, line.text.trim(), jumpOf(lines, i, i + 1)))
                i++; continue
            }
            // paragraph
            var j = i + 1
            val spans = ArrayList<Span>(line.spans)
            var prevLine = line
            val paraLeft = line.x0
            val rightEdge = lines.filter { abs(it.size - body) < body * 0.15f }.maxOfOrNull { it.x1 } ?: line.x1
            while (j < n) {
                val l = lines[j]
                val gap = l.base - prevLine.base
                if (gap > st.leading * max(line.size, l.size) * 1.22f) break
                if (abs(l.size - line.size) > line.size * 0.12f && !isMarkChip(l.text)) break
                if (l.mono) break
                val mk = markerOf(l)
                // a dash opening a line inside a sentence is punctuation, not a bullet
                if (mk != null && !(mk in DASHES && !TERMINAL.containsMatchIn(prevLine.text.trim()))) break
                if (l.cells.size != 1) {
                    // gaps in a line are usually a formula set as a picture; only a real table or a row of choices ends the paragraph
                    if (optionCells(l) != null || table(lines, j, 0) != null) break
                }
                if (headingLevel(l, st) > 0) break
                if (l.bold && !line.bold && isCaps(l.text)) break
                val prevShort = prevLine.x1 < rightEdge - line.size * 3f
                val prevEnds = TERMINAL.containsMatchIn(prevLine.text.trim())
                if (prevShort && prevEnds && gap > st.leading * line.size * 1.05f) break
                if (l.x0 - paraLeft > line.size * 1.2f && prevEnds && prevShort) break
                if (paraLeft - l.x0 > line.size * 2.5f) break
                joinInto(spans, l.spans)
                prevLine = l
                j++
            }
            val text = spans.joinToString("") { it.text }.trim()
            // choices run into the paragraph: the question, then "a ... b ... c ..." with bold letters
            val runIn = runInOptions(spans)
            if (runIn != null) {
                val headText = runIn.first.joinToString("") { it.text }.trim()
                if (headText.isNotEmpty()) {
                    items.add(top to ParaBlock(runIn.first, jumpOf(lines, i, j), startsLower = false, endsOpen = false))
                }
                for (o in runIn.second) items.add(top to ItemBlock(o.first, o.second, 0, -1, 1))
                i = j; continue
            }
            if (text.isNotEmpty()) {
                val firstLetter = text.firstOrNull { it.isLetter() }
                items.add(top to ParaBlock(
                    spans, jumpOf(lines, i, j),
                    startsLower = firstLetter != null && firstLetter.isLowerCase() && !(text.length > 1 && text[0].isDigit()),
                    endsOpen = !TERMINAL.containsMatchIn(text) && text.length > 40
                ))
            }
            i = j
        }
        val sorted = items.sortedBy { it.first }
        assignCards(sorted, c, body)
        val blocks = sorted.map { it.second }
        val words = blocks.sumOf {
            when (it) {
                is ParaBlock -> wordCount(it.text)
                is ItemBlock -> wordCount(it.text)
                is HeadingBlock -> wordCount(it.text)
                is TableBlock -> it.rows.sumOf { r -> r.cells.sumOf { c -> wordCount(c) } }
                else -> 0
            }
        }
        return ReflowPage(page, blocks, words, inlines)
    }


    /**
     * Tonal cards of the page (the print `.box`: notes, answer keys, how-to-read panels). A painted rounded box wide
     * enough to be a panel gives its id to the blocks that start inside it, smallest box first. Boxes behind a table, a
     * code block or a lone picture are not cards.
     */
    private fun assignCards(items: List<Pair<Float, Block>>, c: PageContent, body: Float) {
        val W = c.width; val H = c.height
        val cards = c.gfx.filter {
            it.kind == G_PATH && it.diag == 0 && it.curves <= 12 && it.straight >= 3 &&
                it.w >= 0.45f * W && it.w < 0.97f * W && it.h >= 2.2f * body && it.h < 0.85f * H
        }.sortedBy { it.w * it.h }
        if (cards.isEmpty()) return
        val taken = BooleanArray(items.size)
        var id = 0
        for (card in cards) {
            val inside = items.indices.filter { items[it].first >= card.y0 - 1f && items[it].first <= card.y1 - 2f }
            if (inside.isEmpty()) continue
            if (inside.any { items[it].second is TableBlock || items[it].second is CodeBlock }) continue
            val free = inside.filter { !taken[it] }
            if (free.isEmpty() || free.all { items[it].second is FigureBlock }) continue
            id++
            for (k in free) { items[k].second.box = id; taken[k] = true }
        }
    }

    // --------------------------------------------------------------- lettered choices

    private val OPT_CELL = Regex("^\\(?([A-Ha-h])[.):]?(?:\\s+|$)")

    private class OptCell(val letter: Char, val spans: List<Span>, val x0: Float)

    /** [spans] without their first [n] characters. */
    private fun dropPrefix(spans: List<Span>, n: Int): List<Span> {
        var left = n
        val out = ArrayList<Span>()
        for (s in spans) {
            if (left >= s.text.length) { left -= s.text.length; continue }
            val t = if (left > 0) s.text.substring(left) else s.text
            left = 0
            out.add(Span(if (out.isEmpty()) t.trimStart() else t, s.flags, s.href))
        }
        return out
    }

    private fun trimSpans(l: List<Span>): List<Span> {
        val out = ArrayList(l)
        while (out.isNotEmpty() && out.first().text.isBlank()) out.removeAt(0)
        while (out.isNotEmpty() && out.last().text.isBlank()) out.removeAt(out.size - 1)
        if (out.isNotEmpty()) { val f = out[0]; out[0] = Span(f.text.trimStart(), f.flags, f.href) }
        if (out.isNotEmpty()) { val n = out.size - 1; val e = out[n]; out[n] = Span(e.text.trimEnd(), e.flags, e.href) }
        return out
    }

    /** The choices of a line: every cell starts with a letter, a b c in order; null when the line is not that. */
    private fun optionCells(l: Line): List<OptCell>? {
        if (l.mono || l.cells.isEmpty()) return null
        val cs = l.cells
        val out = ArrayList<OptCell>()
        var k = 0
        while (k < cs.size) {
            val c = cs[k]
            val m = OPT_CELL.find(c.text) ?: return null
            var spans = dropPrefix(c.spans, m.value.length)
            // a letter alone in its cell: the choice itself is the next cell
            if (spans.isEmpty() && k + 1 < cs.size && OPT_CELL.find(cs[k + 1].text) == null) {
                spans = cs[k + 1].spans; k++
            }
            out.add(OptCell(m.groupValues[1][0].lowercaseChar(), spans, c.x0))
            k++
        }
        for (n in out.indices) if (out[n].letter != out[0].letter + n) return null
        return out
    }

    /**
     * Choices from line [start] on: a row of them (a 8   b 12   c 19   d 30) or a grid of rows, with lines that wrap
     * under a choice (d 1 / mark) taken into it. Needs a, b, c in order: a lone "a" opening a sentence is not a choice.
     */
    private fun optionRows(lines: List<Line>, start: Int): Pair<List<ItemBlock>, Int>? {
        val first = optionCells(lines[start]) ?: return null
        if (first[0].letter != 'a') return null
        val out = ArrayList<ItemBlock>()
        var j = start
        var want = 'a'
        var wide = false
        while (j < lines.size && want <= 'h') {
            val l = lines[j]
            if (j > start && l.base - lines[j - 1].base > lines[j - 1].size * 3.4f) break
            val cells = optionCells(l) ?: break
            if (cells[0].letter != want) break
            if (cells.size >= 2) wide = true
            val texts = cells.map { ArrayList(it.spans) }
            var e = j + 1
            while (e < lines.size) {
                val w = lines[e]
                val gap = w.base - lines[e - 1].base
                if (w.mono || gap > w.size * 1.6f || abs(w.size - l.size) > l.size * 0.2f) break
                if (optionCells(w) != null || markerOf(w) != null) break
                val tol = max(6f, w.size * 0.9f)
                val cols = w.cells.map { cell -> cells.indexOfLast { it.x0 + w.size * 0.3f <= cell.x0 + tol && it.x0 <= cell.x0 } }
                if (cols.any { it < 0 }) break
                // text wrapped under a choice starts after its letter, not at the margin
                if (w.cells.indices.any { w.cells[it].x0 < cells[cols[it]].x0 + w.size * 0.3f }) break
                w.cells.forEachIndexed { n, cell -> joinInto(texts[cols[n]], cell.spans) }
                e++
            }
            cells.forEachIndexed { n, c -> out.add(ItemBlock(c.letter.toString(), texts[n], 0, -1, cells.size)) }
            want = cells.last().letter + 1
            j = e
        }
        if (out.size < 2 || (out.size < 3 && !wide)) return null
        return out to j
    }

    /** "question a ... b ... c ...": the bold letters a, b, c... in order split a paragraph into the question and its choices. */
    private fun runInOptions(spans: List<Span>): Pair<List<Span>, List<Pair<String, List<Span>>>>? {
        val marks = ArrayList<Int>()
        var want = 'a'
        for ((k, s) in spans.withIndex()) {
            val t = s.text.trim()
            if (s.bold && !s.sup && !s.sub && t.length == 1 && t[0].lowercaseChar() == want) {
                marks.add(k)
                want++
                if (want > 'h') break
            }
        }
        if (marks.size < 2) return null
        val head = trimSpans(spans.subList(0, marks[0]))
        val opts = ArrayList<Pair<String, List<Span>>>()
        for ((n, at) in marks.withIndex()) {
            val end = if (n + 1 < marks.size) marks[n + 1] else spans.size
            opts.add(('a' + n).toString() to trimSpans(spans.subList(at + 1, end)))
        }
        return head to opts
    }

    /** A mark chip or exam tag that wrapped onto a line of its own: [1] or (NEB 2078). */
    private fun isMarkChip(t: String): Boolean = t.trim().matches(Regex("^(\\[\\d+(\\.\\d+)?\\]|\\([A-Za-z]{2,6}[^)]{0,24}\\))(\\s+(\\[\\d+(\\.\\d+)?\\]|\\([A-Za-z]{2,6}[^)]{0,24}\\)))*$"))

    private fun isHyphen(c: Char?) = c == '-' || c == '\u2010' || c == '\u2011'

    private fun wordCount(s: String): Int {
        var n = 0; var inWord = false
        for (ch in s) { if (ch.isWhitespace()) inWord = false else if (!inWord) { inWord = true; n++ } }
        return n
    }

    private fun jumpOf(lines: List<Line>, from: Int, to: Int): Int {
        for (k in from until min(to, lines.size)) if (lines[k].jump >= 0) return lines[k].jump
        return -1
    }

    private fun isPageNumber(t: String): Boolean {
        val s = t.trim().lowercase()
        return s.matches(Regex("(page\\s*)?[0-9]{1,4}(\\s*(/|of)\\s*[0-9]{1,4})?")) || s.matches(Regex("[ivxlc]{1,6}")) || s.matches(Regex("-\\s*[0-9]{1,4}\\s*-"))
    }

    private fun isCaps(t: String): Boolean {
        var letters = 0
        for (ch in t) if (ch.isLetter()) { letters++; if (ch.isLowerCase()) return false }
        return letters >= 3
    }

    private fun headingLevel(l: Line, st: ReflowStats): Int {
        if (l.cells.size != 1 || l.mono) return 0
        if (l.size < st.body * 1.15f) return 0
        if (l.text.length > 180) return 0
        val idx = st.headSizes.indexOfFirst { l.size >= it - 0.45f }
        return when {
            idx < 0 -> 3
            idx == 0 -> 1
            idx == 1 -> 2
            else -> 3
        }
    }

    private fun markerOf(l: Line): String? {
        if (l.cells.isEmpty() || l.mono) return null
        val t = l.cells[0].text
        BULLET.find(t + " ")?.let { return it.groupValues[1] }
        NUMBERED.find(t)?.let { return it.groupValues[1] }
        // a bullet drawn alone in its own run
        val first = l.runs.firstOrNull { clean(it.text).isNotBlank() }?.let { clean(it.text).trim() }
        if (first != null && first.length == 1 && first in "\u2022\u00B7\u25AA\u25E6\u2023\u25CF\u25CB\u25A0\u25A1\u2713\u2714" && t.length > 1) return first
        return null
    }

    private fun stripMarker(l: Line, marker: String): List<Span> {
        val spans = ArrayList(l.spans)
        if (spans.isEmpty()) return spans
        var first = spans[0]
        var t = first.text
        if (t.startsWith(marker)) t = t.substring(marker.length).trimStart()
        if (t.isEmpty()) spans.removeAt(0) else { first = Span(t, first.flags, first.href); spans[0] = first }
        return spans
    }

    private fun joinInto(spans: MutableList<Span>, more: List<Span>) {
        if (more.isEmpty()) return
        val last = spans.lastOrNull()
        val firstNew = more[0]
        var startIndex = 0
        if (last != null) {
            val lt = last.text
            if (isHyphen(lt.lastOrNull()) && lt.length > 1 && firstNew.text.firstOrNull()?.isLowerCase() == true) {
                val soft = lt[lt.length - 2].isLetter()
                spans[spans.size - 1] = Span((if (soft) lt.dropLast(1) else lt) + firstNew.text, last.flags, last.href)
                startIndex = 1
            } else if (!lt.endsWith(" ") && !firstNew.text.startsWith(" ")) {
                spans[spans.size - 1] = Span(lt + " ", last.flags, last.href)
            }
        }
        for (k in startIndex until more.size) {
            val s = more[k]
            val l2 = spans.lastOrNull()
            if (l2 != null && l2.flags == s.flags && l2.href == s.href) spans[spans.size - 1] = Span(l2.text + s.text, s.flags, s.href)
            else spans.add(s)
        }
    }

    private fun assignLinks(runs: List<Run>, links: List<PdfLink>, w: Float, h: Float) {
        if (links.isEmpty()) return
        for (r in runs) {
            val cx = (r.x0 + r.x1) / 2f / w
            val cy = (r.base - r.size * 0.3f) / h
            for (l in links) {
                if (l.rect.contains(cx, cy)) {
                    if (l.page >= 0) r.jump = l.page else if (l.uri != null) r.href = l.uri
                    break
                }
            }
        }
    }

    // ---------------------------------------------------------------- tables

    /**
     * A table starting at [start] (a line with several cells). [pre] single-cell lines just above it belong to
     * the first row: cells are centred in their row, so a tall cell's first line sits above the row's other cells.
     */
    private fun table(lines: List<Line>, start: Int, pre: Int): Pair<TableBlock, Int>? {
        val first = lines[start]
        val head = lines.subList(start - pre, start + 1)
        val cols = ArrayList<Float>()
        for (l in head) for (c in l.cells) if (cols.none { abs(it - c.x0) <= max(6f, l.size * 0.9f) }) cols.add(c.x0)
        cols.sort()
        class Row(val cells: Array<StringBuilder>, var jump: Int, var bold: Boolean)
        val rows = ArrayList<Row>()
        fun colOf(c: Cell, size: Float): Int {
            var best = -1; var bd = Float.MAX_VALUE
            for ((k, x) in cols.withIndex()) { val d = abs(c.x0 - x); if (d < bd) { bd = d; best = k } }
            return if (bd <= max(6f, size * 0.9f)) best else -1
        }
        fun put(row: Row, l: Line): Boolean {
            val idx = ArrayList<Int>()
            for ((k, c) in l.cells.withIndex()) {
                var ix = colOf(c, l.size)
                // a cell that lands between columns (a formula set after a comma) continues the one before it
                if (ix < 0 && k > 0 && idx[k - 1] >= 0 && c.x0 > cols[idx[k - 1]]) ix = idx[k - 1]
                idx.add(ix)
            }
            if (idx.any { it < 0 }) return false
            for ((k, c) in l.cells.withIndex()) {
                val sb = row.cells[idx[k]]
                val t = c.text
                if (sb.isNotEmpty() && isHyphen(sb.last()) && t.firstOrNull()?.isLowerCase() == true) {
                    if (sb.length > 1 && sb[sb.length - 2].isLetter()) sb.setLength(sb.length - 1)
                } else if (sb.isNotEmpty()) sb.append(' ')
                sb.append(t)
            }
            if (row.jump < 0) row.jump = l.jump
            return true
        }
        var row = Row(Array(cols.size) { StringBuilder() }, -1, first.bold)
        for (l in head) if (!put(row, l)) return null
        rows.add(row)
        var j = start + 1
        while (j < lines.size) {
            val l = lines[j]
            val prev = lines[j - 1]
            val gap = l.base - prev.base
            if (gap > 4.6f * prev.size || abs(l.size - first.size) > first.size * 0.35f || l.mono) break
            val multi = l.cells.size >= 2
            if (!multi) {
                val c = l.cells[0]
                val k = colOf(c, l.size)
                if (k < 0) break
                val colWidth = (cols.getOrNull(k + 1) ?: (c.x0 + 200f)) - cols[k]
                if (c.x1 - c.x0 > colWidth * 1.15f) break
                if (markerOf(l) != null && k == 0 && gap > 1.9f * l.size) break
            }
            // a single cell line right above a multi cell line belongs to that next row
            val nextMulti = j + 1 < lines.size && lines[j + 1].cells.size >= 2 && lines[j + 1].base - l.base < 1.2f * l.size
            val isNew = gap > 1.9f * prev.size || (!multi && nextMulti && gap > 1.1f * prev.size)
            if (isNew) {
                row = Row(Array(cols.size) { StringBuilder() }, -1, l.bold)
                if (!put(row, l)) break
                rows.add(row)
            } else if (!put(row, l)) break
            j++
        }
        if (rows.size < 2) return null
        if (rows.count { r -> r.cells.count { it.isNotEmpty() } >= 2 } < 2) return null
        val out = rows.map { r -> TableRow(r.cells.map { it.toString().trim() }, r.jump) }
        return TableBlock(out, rows[0].bold && rows.size > 1) to j
    }

    // --------------------------------------------------------------- grid tables

    private class GridCell(val l: Float, val t: Float, val r: Float, val b: Float)
    private class Grid(val rows: List<List<GridCell>>)

    /**
     * Tables the print draws as one filled box per cell (fact sheets, tonal tables): boxes of the same height side by
     * side make a row, rows that touch make a table. Each box is a cell, however many lines or formulas it holds.
     */
    private fun findGrids(c: PageContent, body: Float): List<Grid> {
        val seen = HashSet<String>()
        val cells = ArrayList<GridCell>()
        for (g in c.gfx) {
            if (g.kind != G_PATH || !g.fill || g.curves != 0 || g.diag != 0) continue
            if (g.w < 1.5f * body || g.h < 0.9f * body || g.h > 60f * body || g.w > 0.97f * c.width) continue
            if (g.straight < 3 || !seen.add("${Math.round(g.x0)}_${Math.round(g.y0)}_${Math.round(g.x1)}_${Math.round(g.y1)}")) continue
            cells.add(GridCell(g.x0, g.y0, g.x1, g.y1))
        }
        if (cells.size < 4) return emptyList()
        // rows: boxes with the same top and bottom
        val rows = ArrayList<ArrayList<GridCell>>()
        for (cell in cells.sortedWith(compareBy({ it.t }, { it.l }))) {
            val row = rows.firstOrNull { abs(it[0].t - cell.t) <= 1.5f && abs(it[0].b - cell.b) <= 1.5f }
            if (row != null) row.add(cell) else rows.add(arrayListOf(cell))
        }
        rows.sortBy { it[0].t }
        for (r in rows) r.sortBy { it.l }
        // a row is boxes that sit edge to edge; one box alone is a card, not a table row
        val good = rows.filter { r -> r.size >= 2 && (1 until r.size).all { r[it].l - r[it - 1].r in -1.5f..3f } }
        val tables = ArrayList<Grid>()
        var chain = ArrayList<List<GridCell>>()
        fun flush() { if (chain.size >= 2) tables.add(Grid(chain.toList())); chain = ArrayList() }
        for (r in good) {
            val last = chain.lastOrNull()
            val joins = last != null && r[0].t - last[0].b in -1.5f..3.5f && r.size == last.size && r.indices.all { abs(r[it].l - last[it].l) <= 3f }
            if (!joins) flush()
            chain.add(r)
        }
        flush()
        return tables
    }

    // --------------------------------------------------------------- figures

    private class Fig(val box: Box, var equation: Boolean, val owner: Line? = null) {
        var inlineFailed = false
    }

    private fun figures(c: PageContent, lines: List<Line>, st: ReflowStats, hasText: Boolean): List<Fig> {
        val W = c.width; val H = c.height
        val body = st.body
        val pageArea = W * H
        val inks = ArrayList<Box>()
        val decor = ArrayList<Box>()
        for (g in c.gfx) {
            if (g.w <= 0f && g.h <= 0f) continue
            val box = Box(g.x0, g.y0, g.x1, g.y1)
            if (g.kind == G_IMAGE) {
                if (g.w < 4f || g.h < 4f) continue
                if (box.area > 0.6f * pageArea && hasText) continue
                inks.add(box); continue
            }
            if (box.area > 0.7f * pageArea) continue
            val axis = g.curves == 0 && g.diag == 0
            val boxLike = g.diag == 0 && g.curves <= 12 && g.straight >= 3 && min(g.w, g.h) >= 0.9f * body
            val circle = g.diag == 0 && g.curves in 1..8 && g.straight == 0 && g.w >= 1.1f * body && g.h >= 1.1f * body && abs(g.w - g.h) < 0.25f * max(g.w, g.h)
            if (axis || boxLike || circle) decor.add(box) else inks.add(box)
        }
        if (inks.isEmpty()) return emptyList()

        // group inks that touch: half a text size sideways, a fifth up and down, so two rows of maths stay two
        val tolX = body * 0.5f
        val tolY = body * 0.2f
        val parent = IntArray(inks.size) { it }
        fun find(x: Int): Int { var a = x; while (parent[a] != a) { parent[a] = parent[parent[a]]; a = parent[a] }; return a }
        val cell = max(24f, body * 2.4f)
        val gw = (W / cell).toInt() + 2
        val gh = (H / cell).toInt() + 2
        val buckets = HashMap<Int, ArrayList<Int>>()
        for ((k, b) in inks.withIndex()) {
            val cx0 = ((b.l - tolX) / cell).toInt().coerceIn(0, gw - 1); val cx1 = ((b.r + tolX) / cell).toInt().coerceIn(0, gw - 1)
            val cy0 = ((b.t - tolY) / cell).toInt().coerceIn(0, gh - 1); val cy1 = ((b.b + tolY) / cell).toInt().coerceIn(0, gh - 1)
            for (y in cy0..cy1) for (x in cx0..cx1) buckets.getOrPut(y * gw + x) { ArrayList() }.add(k)
        }
        for (list in buckets.values) {
            for (u in 0 until list.size) {
                val a = inks[list[u]]
                for (v in u + 1 until list.size) {
                    val c = inks[list[v]]
                    if (a.l - tolX <= c.r && a.r + tolX >= c.l && a.t - tolY <= c.b && a.b + tolY >= c.t) {
                        val ra = find(list[u]); val rb = find(list[v])
                        if (ra != rb) parent[rb] = ra
                    }
                }
            }
        }
        val byRoot = HashMap<Int, Box>()
        for ((k, b) in inks.withIndex()) {
            val r = find(k)
            val ex = byRoot[r]
            if (ex == null) byRoot[r] = Box(b.l, b.t, b.r, b.b) else ex.union(b)
        }
        val clusters = ArrayList(byRoot.values)

        // decoration that touches a cluster belongs to it (arrows' boxes, fraction bars, axes)
        val used = BooleanArray(decor.size)
        repeat(3) {
            for (cl in clusters) {
                for ((k, d) in decor.withIndex()) {
                    if (used[k]) continue
                    if (!cl.intersects(d, 3f)) continue
                    if (d.contains(cl) && d.area > cl.area * 1.1f) continue
                    if (d.w > 0.6f * W) continue
                    cl.union(d); used[k] = true
                }
            }
        }
        // clusters that now overlap are one picture
        var merged = true
        while (merged) {
            merged = false
            loop@ for (a in 0 until clusters.size) for (b in a + 1 until clusters.size) {
                if (clusters[a].intersects(clusters[b], 2f)) { clusters[a].union(clusters[b]); clusters.removeAt(b); merged = true; break@loop }
            }
        }

        // the line of text a picture sits in (typeset maths inside a sentence, a choice, a table cell)
        fun ownerOf(cl: Box): Line? {
            val cyImg = (cl.t + cl.b) / 2f
            return lines.filter { l ->
                val ov = min(l.bottom, cl.b) - max(l.top, cl.t)
                ov > 0.3f * min(l.bottom - l.top, cl.h) && l.size < body * 1.6f &&
                    cyImg >= l.top - 0.5f * body && cyImg <= l.bottom + 0.5f * body &&
                    ((l.x0 - 2.5f * body <= cl.r && l.x1 + 2.5f * body >= cl.l) ||
                        // a table row: the label on the left owns the formulas set in the cells to its right
                        (cl.h <= 4.6f * body && l.size <= body * 1.2f && l.x1 - l.x0 < 0.5f * W && l.x1 <= cl.l && cl.l - l.x1 <= 0.7f * W))
            }.maxByOrNull { min(it.bottom, cl.b) - max(it.top, cl.t) }
        }

        // pieces of one drawing (labels beside a diagram, rows of a figure) sit a few characters apart
        run {
            var guard = 0
            var changed = true
            while (changed && guard++ < 60) {
                changed = false
                loop@ for (a in 0 until clusters.size) for (b in a + 1 until clusters.size) {
                    val ca = clusters[a]; val cb = clusters[b]
                    val gx = max(ca.l, cb.l) - min(ca.r, cb.r)
                    val gy = max(ca.t, cb.t) - min(ca.b, cb.b)
                    val u = Box(min(ca.l, cb.l), min(ca.t, cb.t), max(ca.r, cb.r), max(ca.b, cb.b))
                    // pictures that fit one line of text are formulas set inside it: only glyph sized pieces of one
                    // formula join, never two formulas with words between them
                    val near = if (u.h <= 4.4f * body) (gx <= 0.7f * body && gy < 0) else (
                        (gx <= 5.6f * body && gy < 0 && -gy >= 0.3f * min(ca.h, cb.h)) ||
                            (gy <= 3.4f * body && gx < 0 && -gx >= 0.2f * min(ca.w, cb.w)) ||
                            (gx <= 2.0f * body && gy <= 2.0f * body))
                    if (!near) continue
                    // two formulas in different rows (table cells, choices) are never one picture
                    if (u.h > 4.4f * body && ca.h <= 4.6f * body && cb.h <= 4.6f * body && gy >= 0f && ownerOf(ca) != null && ownerOf(cb) != null) continue
                    if (u.h > 2.6f * body) {
                        // never swallow the middle of a paragraph
                        val swallows = lines.any { l ->
                            val ov = min(l.bottom, u.b) - max(l.top, u.t)
                            ov > 0.35f * (l.bottom - l.top) && (l.x0 < u.l - 2f * body || l.x1 > u.r + 2f * body) && l.text.length > 12
                        }
                        if (swallows) continue
                    }
                    ca.union(cb); clusters.removeAt(b); changed = true
                    break@loop
                }
            }
        }

        // content bounds, for pictures that stand in for whole lines
        val bodyLines = lines.filter { abs(it.size - body) < body * 0.15f && it.text.length > 20 }
        val contentL = if (bodyLines.isNotEmpty()) bodyLines.minOf { it.x0 } else W * 0.07f
        val contentR = if (bodyLines.isNotEmpty()) bodyLines.maxOf { it.x1 } else W * 0.93f

        val result = ArrayList<Fig>()
        val bands = ArrayList<Box>()
        for (cl in clusters) {
            val tiny = cl.w < 0.7f * body && cl.h < 0.7f * body
            if (tiny && (max(cl.w, cl.h) < 0.35f * body || ownerOf(cl) == null)) continue
            if (cl.area > 0.7f * pageArea && hasText) continue
            if (cl.h <= 4.6f * body && cl.w <= 0.95f * W) {
                val owner = ownerOf(cl)
                result.add(Fig(Box(cl.l - 1f, cl.t - 1f, cl.r + 1f, cl.b + 1f), true, owner))
            } else {
                // big picture: take nearby short, small labels
                val fb = Box(cl.l - 3f, cl.t - 3f, cl.r + 3f, cl.b + 3f)
                repeat(2) {
                    for (l in lines) {
                        val cy = l.base - l.size * 0.3f
                        val small = l.size <= body * 1.02f
                        val short = (l.x1 - l.x0) < 0.62f * max(fb.w, 1f) || (l.x1 - l.x0) < 0.4f * W
                        val sameBand = cy >= fb.t - l.size * 2.4f && cy <= fb.b + l.size * 2.4f
                        val xNear = l.x1 >= fb.l - 0.35f * W && l.x0 <= fb.r + 0.35f * W
                        val inside = (l.x0 + l.x1) / 2f in fb.l..fb.r && cy in fb.t..fb.b
                        val abovBelow = l.x0 >= fb.l - 8f && l.x1 <= fb.r + 8f && (cy < fb.t || cy > fb.b)
                        val beside = cy in fb.t..fb.b && (l.x1 < fb.l || l.x0 > fb.r)
                        if (inside) continue
                        if (small && short && sameBand && xNear && l.cells.size == 1 && l.text.length < 90 && (abovBelow || beside) && !l.bold) {
                            fb.union(Box(l.x0 - 2f, l.top, l.x1 + 2f, l.bottom))
                        }
                    }
                }
                result.add(Fig(fb, false))
            }
        }
        // consecutive bands are one picture
        bands.sortBy { it.t }
        val joined = ArrayList<Box>()
        for (b in bands) {
            val last = joined.lastOrNull()
            if (last != null && b.t - last.b < body * 0.9f) last.union(b) else joined.add(b)
        }
        for (b in joined) result.add(Fig(Box(max(0f, b.l), max(0f, b.t), min(W, b.r), min(H, b.b)), false))
        // unmapped text (no way to know what it says) is shown as it is drawn
        val extra = ArrayList<Box>()
        for (l in lines) {
            if (!l.unmapped) continue
            val cx = (l.x0 + l.x1) / 2f; val cy = l.base - l.size * 0.3f
            if (result.any { cx >= it.box.l && cx <= it.box.r && cy >= it.box.t && cy <= it.box.b }) continue
            extra.add(Box(min(contentL, l.x0) - 4f, l.top - 1.5f, max(contentR, l.x1) + 4f, l.bottom + 1.5f))
        }
        extra.sortBy { it.t }
        val ej = ArrayList<Box>()
        for (b in extra) {
            val last = ej.lastOrNull()
            if (last != null && b.t - last.b < body * 0.9f) last.union(b) else ej.add(b)
        }
        for (b in ej) result.add(Fig(Box(max(0f, b.l), max(0f, b.t), min(W, b.r), min(H, b.b)), false))
        // a picture that sits inside another one (labels pulled in around a drawing swallowed pieces of its maths) is part of it
        run {
            var again = true
            var guard = 0
            while (again && guard++ < 80) {
                again = false
                loop@ for (a in 0 until result.size) for (b in 0 until result.size) {
                    if (a == b) continue
                    val big = result[a].box; val small = result[b].box
                    if (result[a].owner != null || result[b].owner != null) continue
                    val iw = min(big.r, small.r) - max(big.l, small.l); val ih = min(big.b, small.b) - max(big.t, small.t)
                    if (iw > 0f && ih > 0f && iw * ih >= 0.5f * small.area && big.area >= small.area) {
                        big.union(small); result.removeAt(b); again = true; break@loop
                    }
                }
            }
        }
        // display equations are one block: a fraction (numerator, bar, denominator, the "=" beside it), a derivation line by
        // line, a limit, a matrix come out of the outlines as several small pieces; with no word between them they are one picture
        run {
            var again = true
            var guard = 0
            while (again && guard++ < 120) {
                again = false
                val eq = result.filter { it.owner == null && (it.equation || (it.box.h <= 12f * body && it.box.w <= 0.7f * W)) }
                loop@ for (a in eq.indices) for (b in a + 1 until eq.size) {
                    if (!eq[a].equation && !eq[b].equation) continue
                    val fa = eq[a].box; val fb = eq[b].box
                    val gy = max(fa.t, fb.t) - min(fa.b, fb.b)
                    val gx = max(fa.l, fb.l) - min(fa.r, fb.r)
                    val ox = min(fa.r, fb.r) - max(fa.l, fb.l)
                    val stacked = gy <= 1.1f * body && (ox >= 0.4f * min(fa.w, fb.w) || gx <= (if (gy < 0f) 3.4f else 2.6f) * body)
                    val sameRow = gy < 0f && gx <= 1.2f * body
                    if (!stacked && !sameRow) continue
                    val u = Box(min(fa.l, fb.l), min(fa.t, fb.t), max(fa.r, fb.r), max(fa.b, fb.b))
                    if (u.w > 0.95f * W || u.h > 16f * body) continue
                    val textInside = lines.any { l ->
                        val cx = (l.x0 + l.x1) / 2f; val cy = l.base - l.size * 0.3f
                        cx >= u.l && cx <= u.r && cy >= u.t && cy <= u.b &&
                            !(cx >= fa.l && cx <= fa.r && cy >= fa.t && cy <= fa.b) && !(cx >= fb.l && cx <= fb.r && cy >= fb.t && cy <= fb.b)
                    }
                    if (textInside) continue
                    fa.union(fb); eq[a].equation = eq[a].equation && eq[b].equation; result.remove(eq[b]); again = true
                    break@loop
                }
            }
        }
        return result
    }
}
