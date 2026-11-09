package com.neb.ians.ui.screens.reader.pdf
import java.io.File
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
        val rp = PdfReflow.build(p, c, st, f.links(p))
        println("=== page $p  ${(System.nanoTime()-t1)/1e6}ms  words=${rp.words}")
        for (b in rp.blocks) when (b) {
            is HeadingBlock -> println("H${b.level}[${b.jump}] ${b.text}")
            is ParaBlock -> println("P${if (b.jump>=0) "[->${b.jump}]" else ""}${if (b.startsLower) "<" else ""} ${b.text.take(160)}${if (b.endsOpen) " >>" else ""}")
            is ItemBlock -> println("  ${"  ".repeat(b.depth)}LI ${b.marker} ${b.text.take(130)}")
            is CodeBlock -> println("CODE: ${b.text.replace("\n", "\\n").take(130)}")
            is LabelBlock -> println("LABEL ${b.text}")
            is TableBlock -> { println("TABLE hdr=${b.header}"); b.rows.forEach { println("   | " + it.cells.joinToString(" | ") + if (it.jump>=0) "  ->${it.jump}" else "") } }
            is FigureBlock -> println("FIG eq=${b.equation} ${"%.2f %.2f %.2f %.2f".format(b.rect.l,b.rect.t,b.rect.r,b.rect.b)} ${b.widthPts.toInt()}x${b.heightPts.toInt()}")
        }
    }
}
