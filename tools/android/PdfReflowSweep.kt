package com.neb.ians.ui.screens.reader.pdf
import java.io.File
fun main(args: Array<String>) {
    val t0 = System.nanoTime()
    val f = PdfFile.open(File(args[0])) ?: run { println("OPEN FAIL"); return }
    val ex = PdfTextExtractor(f)
    val n = f.pages().size
    val samples = (0 until minOf(12, n)).map { (it * n / 12) }.mapNotNull { ex.extract(it) }
    val st = PdfReflow.stats(samples)
    var fails = 0; var slow = 0L; var maxMs = 0L; var blocks = 0; var figs = 0; var words = 0; var links = 0
    for (p in 0 until n) {
        val t = System.nanoTime()
        try {
            val c = ex.extract(p)!!
            val l = f.links(p); links += l.size
            val rp = PdfReflow.build(p, c, st, l)
            blocks += rp.blocks.size; figs += rp.blocks.count { it is FigureBlock }; words += rp.words
        } catch (e: Throwable) { fails++; if (fails < 3) e.printStackTrace() }
        val ms = (System.nanoTime() - t) / 1000000; maxMs = maxOf(maxMs, ms); slow += ms
    }
    println("${File(args[0]).name}: pages=$n body=${st.body} fails=$fails total=${(System.nanoTime()-t0)/1000000}ms avg=${slow/n} max=$maxMs blocks=$blocks figs=$figs words=$words links=$links outline=${f.outline().size}")
}
