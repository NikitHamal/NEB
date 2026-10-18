package com.neb.ians.ui.pixel

/**
 * Frames of pixel art. [frameMs] is how long each frame shows when the sprite plays; [loop]
 * says whether it starts again. Frames are ARGB, with alpha 0 for transparent.
 */
class PixelSprite(
    val width: Int,
    val height: Int,
    val frames: List<IntArray>,
    val frameMs: Int = 120,
    val loop: Boolean = true
) {
    val durationMs: Int get() = frames.size * frameMs

    fun frameAt(timeMs: Long): Int {
        val i = (timeMs / frameMs).toInt()
        return if (loop) Math.floorMod(i, frames.size) else minOf(i, frames.size - 1)
    }

    companion object {
        /**
         * Builds a sprite from ASCII frames: one character per pixel, rows separated by newlines,
         * '.' or ' ' transparent, any other character looked up in [palette]. Rows are padded to
         * the widest row, so a frame never has to be counted by hand.
         */
        fun parse(palette: Map<Char, Int>, frameMs: Int, vararg art: String, loop: Boolean = true): PixelSprite {
            val grids = art.map { frame -> frame.trimIndent().lines().filter { it.isNotEmpty() } }
            val w = grids.maxOf { g -> g.maxOf { it.length } }
            val h = grids.maxOf { it.size }
            val frames = grids.map { rows ->
                IntArray(w * h).also { out ->
                    rows.forEachIndexed { y, row ->
                        row.forEachIndexed { x, ch ->
                            if (ch != '.' && ch != ' ') {
                                out[y * w + x] = palette[ch] ?: error("No colour for '$ch'")
                            }
                        }
                    }
                }
            }
            return PixelSprite(w, h, frames, frameMs, loop)
        }

        /** Draws each frame with [draw] into a fresh transparent canvas. */
        fun build(width: Int, height: Int, count: Int, frameMs: Int, loop: Boolean = true, draw: PixelCanvas.(Int) -> Unit): PixelSprite {
            val frames = List(count) { i ->
                PixelCanvas(width, height).apply { draw(i) }.pixels.copyOf()
            }
            return PixelSprite(width, height, frames, frameMs, loop)
        }
    }
}
