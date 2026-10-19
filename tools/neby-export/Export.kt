import com.neb.ians.ui.pixel.NebyLook
import com.neb.ians.ui.pixel.NebyState
import com.neb.ians.ui.pixel.PixelNebyStates
import java.awt.image.BufferedImage
import java.io.File
import javax.imageio.ImageIO

/**
 * Exports pixel Neby for the web: one horizontal strip per look and state, frames side by side,
 * drawn by the same code the Android app runs (ui/pixel). Usage: export <out-dir> [state ...]
 */
fun main(args: Array<String>) {
    val out = File(args.getOrElse(0) { "out" })
    val only = args.drop(1).toSet()
    var n = 0
    for (look in NebyLook.entries) for (state in NebyState.entries) {
        if (only.isNotEmpty() && state.key !in only) continue
        val sprite = PixelNebyStates.sprite(state, look)
        val w = sprite.width; val h = sprite.height
        val img = BufferedImage(w * sprite.frames.size, h, BufferedImage.TYPE_INT_ARGB)
        sprite.frames.forEachIndexed { i, px -> img.setRGB(i * w, 0, w, h, px, 0, w) }
        val dir = File(out, look.key).apply { mkdirs() }
        ImageIO.write(img, "png", File(dir, "${state.key}.png")); n++
    }
    println("wrote $n strips to ${out.path}")
}
