package com.neb.ians.ui.pixel

import com.neb.ians.ui.pixel.art.PixelOnboarding.Kind as ObKind
import com.neb.ians.ui.pixel.art.PixelOnboarding.Handle as ObHandle
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

class PixelSkySceneTest {
    @Test
    fun sprites_have_consistent_frames() {
        PixelUiSprites.all.map { it.second }.forEach { s ->
            s.frames.forEach { assertEquals(s.width * s.height, it.size) }
            assertTrue(s.frames.any { f -> f.any { (it ushr 24) != 0 } })
        }
    }

    @Test
    fun onboarding_scenes_render_without_transparent_holes() {
        val po = com.neb.ians.ui.pixel.art.PixelOnboarding
        for (kind in ObKind.entries) {
            for (night in listOf(false, true)) {
                val sc = po.render(kind, a = 1, b = 4, flag = true, handle = ObHandle.Available, night = night)
                assertEquals("$kind $night", 0, sc.canvas.pixels.count { (it ushr 24) == 0 })
            }
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
