package com.neb.ians.ui.screens.notes

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

/** The 40 drawn note banners keep one composition: the reference frame is exact, other frames follow the limiting side. */
class NoteCoverUnitTest {
    @Test fun referenceFrameKeepsTheDrawnSize() {
        // editor frame 2.3 : 1 -> 0.9 of its height, zoomed a little
        assertEquals(0.9f * NoteCoverZoom * 200f, noteCoverUnit(460f, 200f), 0.001f)
    }

    @Test fun zoomOutPullsCentresTowardTheMiddle() {
        assertEquals(0.5f, noteCoverPos(0.5f), 0.0001f)
        assertEquals(0.5f + 0.3f * NoteCoverZoom, noteCoverPos(0.8f), 0.0001f)
        assertEquals(0.5f - 0.4f * NoteCoverZoom, noteCoverPos(0.1f), 0.0001f)
    }

    @Test fun sameHeightSameSizeInAnyWiderFrame() {
        assertEquals(noteCoverUnit(460f, 60f), noteCoverUnit(1200f, 60f), 0.001f)
    }

    @Test fun sameWidthSameSizeInAnyTallerFrame() {
        assertEquals(noteCoverUnit(230f, 100f), noteCoverUnit(230f, 400f), 0.001f)
    }

    @Test fun scalesLinearly() {
        assertTrue(Math.abs(noteCoverUnit(920f, 400f) - 2f * noteCoverUnit(460f, 200f)) < 0.001f)
    }
}
