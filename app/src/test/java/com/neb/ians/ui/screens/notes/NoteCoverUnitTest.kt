package com.neb.ians.ui.screens.notes

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

/** The 40 drawn note banners keep one composition: the reference frame is exact, other frames follow the limiting side. */
class NoteCoverUnitTest {
    @Test fun referenceFrameKeepsTheDrawnSize() {
        // editor frame 1.9 : 1 -> 0.9 of its height
        assertEquals(0.9f * 200f, noteCoverUnit(380f, 200f), 0.001f)
    }

    @Test fun sameHeightSameSizeInAnyWiderFrame() {
        assertEquals(noteCoverUnit(380f, 60f), noteCoverUnit(1200f, 60f), 0.001f)
    }

    @Test fun sameWidthSameSizeInAnyTallerFrame() {
        assertEquals(noteCoverUnit(190f, 100f), noteCoverUnit(190f, 400f), 0.001f)
    }

    @Test fun scalesLinearly() {
        assertTrue(Math.abs(noteCoverUnit(760f, 400f) - 2f * noteCoverUnit(380f, 200f)) < 0.001f)
    }
}
