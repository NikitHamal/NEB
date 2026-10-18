package com.neb.ians.ui.pixel

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

class PixelSkySceneTest {
    @Test
    fun scene_renders_every_layer_without_holes() {
        val scene = PixelSkyScene()
        for (t in longArrayOf(0, 1234, 4100, 9000)) {
            scene.render(t)
            assertTrue("no transparent pixels", scene.canvas.pixels.all { (it ushr 24) == 0xFF })
        }
    }

    @Test
    fun sprites_have_consistent_frames() {
        (listOf(PixelSprites.bird, PixelSprites.sparkle, PixelSprites.paperPlane, PixelSprites.heartPop,
            PixelSprites.star, PixelSprites.hourglass, PixelSprites.book) + PixelUiSprites.all.map { it.second }).forEach { s ->
            s.frames.forEach { assertEquals(s.width * s.height, it.size) }
            assertTrue(s.frames.any { f -> f.any { (it ushr 24) != 0 } })
        }
    }

    /** Set PIXEL_OUT to a directory to export frames as PPM (scene at 24 fps, plus a sprite sheet). */
    @Test
    fun export_frames_when_asked() {
        val out = System.getenv("PIXEL_OUT") ?: return
        val dir = File(out).apply { mkdirs() }
        val scene = PixelSkyScene()
        val seconds = (System.getenv("PIXEL_SECONDS") ?: "10").toInt()
        for (i in 0 until seconds * 24) {
            scene.render(i * 1000L / 24)
            write(scene.canvas.pixels, PixelSkyScene.WIDTH, PixelSkyScene.HEIGHT, File(dir, "scene_%05d.ppm".format(i)))
        }
        val sprites = listOf(PixelSprites.bird, PixelSprites.sparkle, PixelSprites.paperPlane, PixelSprites.heartPop,
            PixelSprites.star, PixelSprites.hourglass, PixelSprites.book) + PixelUiSprites.all.map { it.second } +
            listOf("kite", "diyo", "gulal", "gurans", "drop", "snow", "pencil").mapNotNull { PixelMotifs.sprite(it, 0xFFB3261E.toInt()) }
        val sheetW = sprites.maxOf { it.width * it.frames.size + it.frames.size * 2 }
        val sheetH = sprites.sumOf { it.height + 4 }
        val sheet = IntArray(sheetW * sheetH) { 0xFFF2ECE1.toInt() }
        var y = 0
        for (s in sprites) {
            s.frames.forEachIndexed { f, data ->
                val ox = f * (s.width + 2)
                for (sy in 0 until s.height) for (sx in 0 until s.width) {
                    val c = data[sy * s.width + sx]
                    if ((c ushr 24) != 0) sheet[(y + sy) * sheetW + ox + sx] = c
                }
            }
            y += s.height + 4
        }
        write(sheet, sheetW, sheetH, File(dir, "sprites.ppm"))
    }

    /** Binary PPM: no imaging library needed on the Android unit-test classpath. */
    private fun write(px: IntArray, w: Int, h: Int, file: File) {
        val header = "P6\n$w $h\n255\n".toByteArray()
        val body = ByteArray(w * h * 3)
        px.forEachIndexed { i, c ->
            body[i * 3] = (c shr 16).toByte(); body[i * 3 + 1] = (c shr 8).toByte(); body[i * 3 + 2] = c.toByte()
        }
        file.writeBytes(header + body)
    }
}
