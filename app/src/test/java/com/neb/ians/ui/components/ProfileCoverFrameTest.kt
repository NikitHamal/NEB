package com.neb.ians.ui.components

import androidx.compose.ui.unit.dp
import org.junit.Assert.assertEquals
import org.junit.Test

/** The cover frame is one exact rectangle: 2.4 : 1 on phones, 3 : 1 from 600dp, never clamped. */
class ProfileCoverFrameTest {
    @Test fun phoneFrameIsTwoPointFourToOne() {
        assertEquals(150f, profileCoverHeight(360.dp, 0.dp).value, 0.001f)
        assertEquals(2.4f, profileCoverAspect(360.dp), 0.0001f)
    }

    @Test fun wideFrameIsThreeToOne() {
        assertEquals(300f, profileCoverHeight(900.dp, 0.dp).value, 0.001f)
        assertEquals(3f, profileCoverAspect(600.dp), 0.0001f)
    }

    @Test fun frameKeepsItsRatioAtAnyWidth() {
        for (w in listOf(320, 411, 599, 600, 840, 1280)) {
            val width = w.dp
            assertEquals(width.value / profileCoverHeight(width, 0.dp).value, profileCoverAspect(width), 0.001f)
        }
    }
}
