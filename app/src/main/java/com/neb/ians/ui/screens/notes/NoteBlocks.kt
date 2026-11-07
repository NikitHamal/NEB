package com.neb.ians.ui.screens.notes

import org.json.JSONArray
import org.json.JSONObject
import java.util.UUID

/*
 * A note is a list of blocks, the way Notion keeps it: text in several shapes, to-dos, quotes, code, dividers, pictures,
 * voice recordings, tables and sketches. Text inside a block is inline Markdown that the editor draws live (see
 * LiveMarkdown), so nobody types syntax.
 *
 * Stored twice: `doc` holds the blocks as JSON (lossless), `body` holds a Markdown export, so the list, search, sharing
 * and read-aloud keep working on plain text. Notes written before blocks existed have no `doc` and open from `body`.
 */

enum class BlockType(val label: String, val keywords: String) {
    Text("Text", "text paragraph plain"),
    H1("Heading 1", "heading title h1 big"),
    H2("Heading 2", "heading h2 subtitle"),
    H3("Heading 3", "heading h3 small"),
    Todo("To-do", "todo checklist check task"),
    Bullet("Bulleted list", "bullet list unordered"),
    Number("Numbered list", "number list ordered"),
    Quote("Quote", "quote cite"),
    Callout("Callout", "callout note tip highlight"),
    Code("Code", "code snippet pre"),
    Divider("Divider", "divider line rule"),
    Table("Table", "table grid rows columns"),
    Image("Photo", "image photo picture gallery"),
    Audio("Audio", "audio voice record sound"),
    Drawing("Drawing", "drawing sketch draw pen");

    val hasText: Boolean get() = this != Divider && this != Table && this != Image && this != Audio && this != Drawing
    val isList: Boolean get() = this == Todo || this == Bullet || this == Number
}

/** One pen stroke. [points] is x0, y0, x1, y1... with x as a fraction of the canvas width and y of its height. */
data class Stroke(val color: Int, val width: Float, val points: List<Float>)

data class NoteBlock(
    val id: String = UUID.randomUUID().toString(),
    val type: BlockType = BlockType.Text,
    val text: String = "",
    val checked: Boolean = false,
    /** Image or audio file. */
    val path: String = "",
    /** Image width as a fraction of the page. */
    val size: Float = 1f,
    /** Audio length. */
    val seconds: Int = 0,
    val rows: List<List<String>> = emptyList(),
    val strokes: List<Stroke> = emptyList(),
    /** Height of a drawing, in dp. */
    val height: Float = 260f,
) {
    val isBlank: Boolean
        get() = when (type) {
            BlockType.Image, BlockType.Audio -> path.isBlank()
            BlockType.Table -> rows.all { r -> r.all { it.isBlank() } }
            BlockType.Drawing -> strokes.isEmpty()
            BlockType.Divider -> false
            else -> text.isBlank()
        }
}

object NoteDoc {
    fun starter(): List<NoteBlock> = listOf(NoteBlock())

    fun isBlank(blocks: List<NoteBlock>): Boolean = blocks.all { it.isBlank }

    // ---------------------------------------------------------------- JSON

    fun toJson(blocks: List<NoteBlock>): String {
        val arr = JSONArray()
        blocks.forEach { b ->
            val o = JSONObject()
            o.put("id", b.id)
            o.put("t", b.type.name)
            if (b.text.isNotEmpty()) o.put("x", b.text)
            if (b.checked) o.put("c", true)
            if (b.path.isNotEmpty()) o.put("p", b.path)
            if (b.size != 1f) o.put("s", b.size.toDouble())
            if (b.seconds > 0) o.put("d", b.seconds)
            if (b.rows.isNotEmpty()) {
                val rs = JSONArray()
                b.rows.forEach { r -> rs.put(JSONArray(r)) }
                o.put("r", rs)
            }
            if (b.strokes.isNotEmpty()) {
                val ss = JSONArray()
                b.strokes.forEach { st ->
                    val so = JSONObject()
                    so.put("k", st.color)
                    so.put("w", st.width.toDouble())
                    val pts = JSONArray()
                    st.points.forEach { pts.put(Math.round(it * 10000f) / 10000.0) }
                    so.put("p", pts)
                    ss.put(so)
                }
                o.put("k", ss)
            }
            if (b.type == BlockType.Drawing) o.put("h", b.height.toDouble())
            arr.put(o)
        }
        return arr.toString()
    }

    fun fromJson(json: String): List<NoteBlock> {
        return try {
            val arr = JSONArray(json)
            val out = ArrayList<NoteBlock>(arr.length())
            for (i in 0 until arr.length()) {
                val o = arr.getJSONObject(i)
                val type = runCatching { BlockType.valueOf(o.optString("t", "Text")) }.getOrDefault(BlockType.Text)
                val rows = ArrayList<List<String>>()
                o.optJSONArray("r")?.let { rs ->
                    for (r in 0 until rs.length()) {
                        val cells = rs.getJSONArray(r)
                        rows.add(List(cells.length()) { c -> cells.optString(c, "") })
                    }
                }
                val strokes = ArrayList<Stroke>()
                o.optJSONArray("k")?.let { ss ->
                    for (k in 0 until ss.length()) {
                        val so = ss.getJSONObject(k)
                        val pts = so.optJSONArray("p")
                        strokes.add(
                            Stroke(
                                color = so.optInt("k", 0xFF1B1B1F.toInt()),
                                width = so.optDouble("w", 4.0).toFloat(),
                                points = if (pts == null) emptyList() else List(pts.length()) { j -> pts.optDouble(j, 0.0).toFloat() }
                            )
                        )
                    }
                }
                out.add(
                    NoteBlock(
                        id = o.optString("id").ifBlank { UUID.randomUUID().toString() },
                        type = type,
                        text = o.optString("x", ""),
                        checked = o.optBoolean("c", false),
                        path = o.optString("p", ""),
                        size = o.optDouble("s", 1.0).toFloat(),
                        seconds = o.optInt("d", 0),
                        rows = rows,
                        strokes = strokes,
                        height = o.optDouble("h", 260.0).toFloat(),
                    )
                )
            }
            if (out.isEmpty()) starter() else out
        } catch (_: Exception) {
            starter()
        }
    }

    // ---------------------------------------------------------------- Markdown

    fun toMarkdown(blocks: List<NoteBlock>): String {
        val sb = StringBuilder()
        var number = 0
        var prev: BlockType? = null
        blocks.forEach { b ->
            if (b.isBlank && b.type != BlockType.Divider) return@forEach
            number = if (b.type == BlockType.Number) (if (prev == BlockType.Number) number + 1 else 1) else 0
            val piece = when (b.type) {
                BlockType.Text -> b.text
                BlockType.H1 -> "# ${b.text}"
                BlockType.H2 -> "## ${b.text}"
                BlockType.H3 -> "### ${b.text}"
                BlockType.Bullet -> "- ${b.text}"
                BlockType.Number -> "$number. ${b.text}"
                BlockType.Todo -> "- [${if (b.checked) "x" else " "}] ${b.text}"
                BlockType.Quote, BlockType.Callout -> b.text.lines().joinToString("\n") { "> $it" }
                BlockType.Code -> "```\n${b.text}\n```"
                BlockType.Divider -> "---"
                BlockType.Image -> "[image]"
                BlockType.Audio -> "[audio recording]"
                BlockType.Drawing -> "[drawing]"
                BlockType.Table -> tableMarkdown(b.rows)
            }
            if (sb.isNotEmpty()) sb.append(if (prev?.isList == true && b.type.isList) "\n" else "\n\n")
            sb.append(piece)
            prev = b.type
        }
        return sb.toString()
    }

    private fun tableMarkdown(rows: List<List<String>>): String {
        if (rows.isEmpty()) return ""
        val cols = rows.maxOf { it.size }.coerceAtLeast(1)
        fun line(r: List<String>) = "| " + List(cols) { c -> r.getOrElse(c) { "" }.replace("|", "\\|").replace("\n", " ").ifBlank { " " } }.joinToString(" | ") + " |"
        val sep = "|" + " --- |".repeat(cols)
        return (listOf(line(rows[0]), sep) + rows.drop(1).map(::line)).joinToString("\n")
    }

    private val numberRe = Regex("^\\s*\\d+[.)] ")
    private val todoRe = Regex("^\\s*[-*+] \\[([ xX])] ")
    private val bulletRe = Regex("^\\s*[-*+] ")
    private val headRe = Regex("^(#{1,3}) ")
    private val hrRe = Regex("^(-{3,}|\\*{3,}|_{3,})$")

    /** Notes saved as Markdown (older ones, or text pasted in) become blocks. */
    fun fromMarkdown(md: String): List<NoteBlock> {
        val out = ArrayList<NoteBlock>()
        val lines = md.replace("\r\n", "\n").split('\n')
        var i = 0
        while (i < lines.size) {
            val line = lines[i]
            when {
                line.startsWith("```") -> {
                    val body = ArrayList<String>()
                    i++
                    while (i < lines.size && !lines[i].startsWith("```")) { body.add(lines[i]); i++ }
                    out.add(NoteBlock(type = BlockType.Code, text = body.joinToString("\n")))
                }
                line.isBlank() -> {}
                hrRe.matches(line.trim()) -> out.add(NoteBlock(type = BlockType.Divider))
                headRe.containsMatchIn(line) -> {
                    val m = headRe.find(line)!!
                    val type = when (m.groupValues[1].length) { 1 -> BlockType.H1; 2 -> BlockType.H2; else -> BlockType.H3 }
                    out.add(NoteBlock(type = type, text = line.removePrefix(m.value)))
                }
                todoRe.containsMatchIn(line) -> {
                    val m = todoRe.find(line)!!
                    out.add(NoteBlock(type = BlockType.Todo, checked = m.groupValues[1] != " ", text = line.removePrefix(m.value)))
                }
                bulletRe.containsMatchIn(line) -> out.add(NoteBlock(type = BlockType.Bullet, text = line.replaceFirst(bulletRe, "")))
                numberRe.containsMatchIn(line) -> out.add(NoteBlock(type = BlockType.Number, text = line.replaceFirst(numberRe, "")))
                line.startsWith("> ") -> out.add(NoteBlock(type = BlockType.Quote, text = line.removePrefix("> ")))
                line.trimStart().startsWith("|") -> {
                    val rows = ArrayList<List<String>>()
                    while (i < lines.size && lines[i].trimStart().startsWith("|")) {
                        val cells = lines[i].trim().trim('|').split('|').map { it.trim().replace("\\|", "|") }
                        if (!cells.all { c -> c.isNotEmpty() && c.all { ch -> ch == '-' || ch == ':' } }) rows.add(cells)
                        i++
                    }
                    i--
                    if (rows.isNotEmpty()) out.add(NoteBlock(type = BlockType.Table, rows = rows))
                }
                else -> out.add(NoteBlock(text = line))
            }
            i++
        }
        return if (out.isEmpty()) starter() else out
    }

    fun wordCount(blocks: List<NoteBlock>): Int =
        NoteFormatting.wordCount(toMarkdown(blocks.filter { it.type != BlockType.Code }))
}
