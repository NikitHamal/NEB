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
        // one horizontal strip per UI sprite, for the web (scripts turn them into PNG + CSS)
        val ui = File(dir, "ui").apply { mkdirs() }
        val meta = StringBuilder()
        for ((name, s) in PixelUiSprites.all) {
            val n = s.frames.size
            val strip = IntArray(s.width * n * s.height)
            s.frames.forEachIndexed { f, data ->
                for (y in 0 until s.height) for (x in 0 until s.width) strip[y * s.width * n + f * s.width + x] = data[y * s.width + x]
            }
            writeArgb(strip, s.width * n, s.height, File(ui, "$name.pam"))
            meta.append("$name ${s.width} ${s.height} $n ${s.frameMs}\n")
        }
        File(ui, "meta.txt").writeText(meta.toString())
        // every Neby look in every state: neby/<look>/<state>.pam, the same frames for web and app
        val nebyDir = File(dir, "neby").apply { mkdirs() }
        val nebyMeta = StringBuilder()
        for (look in NebyLook.entries) {
            val ld = File(nebyDir, look.key).apply { mkdirs() }
            for (state in NebyState.entries) {
                val s = state.sprite(look)
                val n = s.frames.size
                val strip = IntArray(s.width * n * s.height)
                s.frames.forEachIndexed { f, data ->
                    for (y in 0 until s.height) for (x in 0 until s.width) strip[y * s.width * n + f * s.width + x] = data[y * s.width + x]
                }
                writeArgb(strip, s.width * n, s.height, File(ld, "${state.key}.pam"))
                if (look == NebyLook.Classic) nebyMeta.append("${state.key} $n ${s.frameMs}\n")
            }
        }
        File(nebyDir, "meta.txt").writeText(nebyMeta.toString())
        // every resource banner, by day and by night
        val bannerDir = File(dir, "banners").apply { mkdirs() }
        for (family in com.neb.ians.ui.pixel.art.PixelBanners.FAMILIES) for (v in 0 until com.neb.ians.ui.pixel.art.PixelBanners.VARIANTS) for (night in listOf(false, true)) {
            val cv = com.neb.ians.ui.pixel.art.PixelBanners.render(family, v, night)
            writeArgb(cv.pixels, cv.width, cv.height, File(bannerDir, "${family.lowercase()}-$v-${if (night) "night" else "day"}.pam"))
        }
        val coverDir = File(dir, "covers").apply { mkdirs() }
        for (role in com.neb.ians.ui.pixel.art.PixelCovers.ROLES) for (v in 0 until com.neb.ians.ui.pixel.art.PixelCovers.VARIANTS) {
            val cv = com.neb.ians.ui.pixel.art.PixelCovers.render(role, v)
            writeArgb(cv.pixels, cv.width, cv.height, File(coverDir, "${role.lowercase()}-$v.pam"))
        }
    }

    @Test
    fun every_banner_fills_its_frame() {
        val pb = com.neb.ians.ui.pixel.art.PixelBanners
        for (family in pb.FAMILIES) for (v in 0 until pb.VARIANTS) for (night in listOf(false, true)) {
            val cv = pb.render(family, v, night)
            // a banner is a full picture: no transparent holes for the card to show through
            assertEquals("$family $v $night", 0, cv.pixels.count { (it ushr 24) == 0 })
        }
        val pc = com.neb.ians.ui.pixel.art.PixelCovers
        for (role in pc.ROLES) for (v in 0 until pc.VARIANTS) {
            val cv = pc.render(role, v)
            assertEquals("$role $v", 0, cv.pixels.count { (it ushr 24) == 0 })
        }
    }

    @Test
    fun every_look_and_state_renders() {
        for (look in NebyLook.entries) for (state in NebyState.entries) {
            val s = state.sprite(look)
            assertEquals(state.frameMs, s.frameMs)
            // the figure is there in every frame, and nothing is drawn in the corner a crop would show oddly
            s.frames.forEach { f -> assertTrue("$look $state", f.count { (it ushr 24) != 0 } > 500) }
        }
        assertEquals(NebyLook.Dashain, NebyLook.forTheme("dashain"))
        assertEquals(NebyLook.Classic, NebyLook.forTheme("everyday"))
        assertEquals(NebyState.LookAround, NebyState.fromName(NebyState.LookAround.key))
    }

    /** PAM with alpha (RGB_ALPHA), so transparent pixels survive the trip to PNG. */
    private fun writeArgb(px: IntArray, w: Int, h: Int, file: File) {
        val header = "P7\nWIDTH $w\nHEIGHT $h\nDEPTH 4\nMAXVAL 255\nTUPLTYPE RGB_ALPHA\nENDHDR\n".toByteArray()
        val body = ByteArray(w * h * 4)
        px.forEachIndexed { i, c ->
            body[i * 4] = (c shr 16).toByte(); body[i * 4 + 1] = (c shr 8).toByte(); body[i * 4 + 2] = c.toByte(); body[i * 4 + 3] = (c ushr 24).toByte()
        }
        file.writeBytes(header + body)
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
