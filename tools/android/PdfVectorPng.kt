package com.neb.ians.ui.screens.reader.pdf

import java.awt.RenderingHints
import java.awt.geom.Path2D
import java.awt.image.BufferedImage
import java.io.File
import javax.imageio.ImageIO

/** Draws the maths outlines the reader keeps for one page (and nothing else) to a PNG, to compare with a render of the page. */
fun main(args: Array<String>) {
    val f = PdfFile.open(File(args[0]))!!
    val ex = PdfTextExtractor(f)
    val n = f.pages().size
    val samples = (0 until 12).map { 1 + it * (n - 2) / 12 }.mapNotNull { ex.extract(it) }
    val st = PdfReflow.stats(samples)
    val p = args[1].toInt()
    val scale = 2f
    val c = ex.extract(p)!!
    val rp = PdfReflow.build(p, c, st, f.links(p))
    val img = BufferedImage((c.width * scale).toInt(), (c.height * scale).toInt(), BufferedImage.TYPE_INT_RGB)
    val g = img.createGraphics()
    g.color = java.awt.Color.WHITE; g.fillRect(0, 0, img.width, img.height)
    g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
    var vec = 0; var crop = 0
    fun draw(a: VectorArt, ox: Float, oy: Float) {
        for (s in a.shapes) {
            val path = Path2D.Float(if (s.evenOdd) Path2D.WIND_EVEN_ODD else Path2D.WIND_NON_ZERO)
            var i = 0
            val m = s.cmds
            while (i < m.size) {
                when (m[i].toInt()) {
                    V_MOVE -> { path.moveTo((ox + m[i + 1]) * scale, (oy + m[i + 2]) * scale); i += 3 }
                    V_LINE -> { path.lineTo((ox + m[i + 1]) * scale, (oy + m[i + 2]) * scale); i += 3 }
                    V_CUBIC -> { path.curveTo((ox + m[i + 1]) * scale, (oy + m[i + 2]) * scale, (ox + m[i + 3]) * scale, (oy + m[i + 4]) * scale, (ox + m[i + 5]) * scale, (oy + m[i + 6]) * scale); i += 7 }
                    else -> { path.closePath(); i += 1 }
                }
            }
            g.color = java.awt.Color(if (rgbLuma(s.fillRgb) < 0.38f) 0 else s.fillRgb)
            if (s.fill) g.fill(path)
            if (s.stroke) { g.color = java.awt.Color(if (rgbLuma(s.strokeRgb) < 0.38f) 0 else s.strokeRgb); g.stroke = java.awt.BasicStroke(s.width * scale); g.draw(path) }
        }
    }
    for (i in rp.inlines) { if (i.vec != null) { vec++; draw(i.vec, i.rect.l * c.width, i.rect.t * c.height) } else crop++ }
    for (b in rp.blocks) if (b is FigureBlock) { if (b.vec != null) { vec++; draw(b.vec, b.rect.l * c.width, b.rect.t * c.height) } else crop++ }
    println("page $p: vector=$vec crop=$crop")
    ImageIO.write(img, "png", File(args[2]))
}
