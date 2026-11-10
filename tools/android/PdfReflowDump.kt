package com.neb.ians.ui.screens.reader.pdf
import java.io.File
fun vis(s: String) = s.map { if (isMathChar(it)) "<" + (it.code - MATH_BASE) + ">" else it.toString() }.joinToString("")
fun main(args: Array<String>) {
    val f = PdfFile.open(File(args[0]))!!
    val ex = PdfTextExtractor(f)
    val n = f.pages().size
    val t0 = System.nanoTime()
    val samples = (0 until 12).map { 1 + it * (n - 2) / 12 }.mapNotNull { ex.extract(it) }
    val st = PdfReflow.stats(samples)
    println("stats body=${st.body} heads=${st.headSizes} lead=${st.leading} furniture=${st.furniture} (${(System.nanoTime()-t0)/1e6}ms)")
    for (p in args.drop(1).map { it.toInt() }) {
        val t1 = System.nanoTime()
        val c = ex.extract(p)!!
        if (System.getenv("GFX") != null) for (g in c.gfx) if (g.w > 60f && g.h < 3f && g.kind == G_PATH) println("RULE y=%.1f x=%.1f..%.1f h=%.2f fill=%b stroke=%b rgb=%06x/%06x lw=%.2f".format(g.y0, g.x0, g.x1, g.h, g.fill, g.stroke, g.fillRgb, g.strokeRgb, g.lineWidth))
        if (System.getenv("GFX") != null) for (g in c.gfx) if (g.w > 150f && g.h > 12f && g.kind == G_PATH && g.fill) println("BOX y=%.1f..%.1f x=%.1f..%.1f curves=%d rgb=%06x a=%.2f".format(g.y0, g.y1, g.x0, g.x1, g.curves, g.fillRgb, g.fillA))
        val rp = PdfReflow.build(p, c, st, f.links(p))
        println("=== page $p  ${(System.nanoTime()-t1)/1e6}ms  words=${rp.words}")
        for (b in rp.blocks) when (b) {
            is HeadingBlock -> println("[box${b.box}] H${b.level}[${b.jump}] ${vis(b.text)}")
            is ParaBlock -> println("[box${b.box}] P${if (b.jump>=0) "[->${b.jump}]" else ""}${if (b.startsLower) "<" else ""} ${vis(b.text).take(200)}${if (b.endsOpen) " >>" else ""}")
            is ItemBlock -> println("[box${b.box} c${b.choiceCols}]  ${"  ".repeat(b.depth)}LI ${b.marker} ${vis(b.text).take(160)}")
            is CodeBlock -> println("CODE: ${b.text.replace("\n", "\\n").take(130)}")
            is LabelBlock -> println("[box${b.box}] LABEL ${b.text}")
            is TableBlock -> { println("TABLE hdr=${b.header}"); b.rows.forEach { println("   | " + it.cells.joinToString(" | ") { c -> vis(c) } + if (it.jump>=0) "  ->${it.jump}" else "") } }
            is FigureBlock -> println("FIG vec=${b.vec != null} eq=${b.equation} ${"%.2f %.2f %.2f %.2f".format(b.rect.l,b.rect.t,b.rect.r,b.rect.b)} ${b.widthPts.toInt()}x${b.heightPts.toInt()}")
        }
        println("  inlines: " + rp.inlines.mapIndexed { k, i -> "<$k>" + (if (i.vec != null) "v" else "CROP") + "${i.widthPts.toInt()}x${i.heightPts.toInt()}" }.joinToString(" "))
    }
}
