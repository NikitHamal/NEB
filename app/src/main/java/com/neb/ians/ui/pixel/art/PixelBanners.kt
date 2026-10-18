package com.neb.ians.ui.pixel.art

import com.neb.ians.ui.pixel.PixelCanvas

/**
 * Resource banners in pixel art. A banner is one of four [Backdrop]s with one of three props for
 * the subject's family standing in it, by day or by night: twelve pictures per family, picked
 * by a hash of the resource so the same resource always gets the same picture, on the web and
 * in the app. Banners are drawn at 128 x 64 and scaled up crisp; the prop stands right of centre
 * because the card's type pill sits top left.
 */
object PixelBanners {
    const val WIDTH = 128
    const val HEIGHT = 64
    const val VARIANTS = 12

    /** The families, by the names Color.kt's SubjectFamily uses. */
    val FAMILIES = listOf("PHYSICS", "CHEMISTRY", "MATH", "BIOLOGY", "SCIENCE", "LANGUAGE", "COMPUTING", "COMMERCE", "SOCIAL", "HEALTH", "EXAM", "GENERAL")

    private class Prop(val draw: (PixelCanvas, Int, Int) -> Unit, val shadow: Int = 14, val dx: Int = 0)

    private val S = PixelPropsScience
    private val H = PixelPropsHumanities
    private val props: Map<String, List<Prop>> = mapOf(
        "PHYSICS" to listOf(Prop(S::prism, 12), Prop(S::cradle, 17), Prop(S::telescope, 10, -6)),
        "CHEMISTRY" to listOf(Prop(S::flask, 13), Prop(S::tubes, 18), Prop(S::molecule, 8)),
        "MATH" to listOf(Prop(S::geometry, 20, -4), Prop(S::abacus, 18), Prop(S::solids, 22, -4)),
        "BIOLOGY" to listOf(Prop(S::microscope, 12), Prop(S::sprout, 10), Prop(S::helix, 8)),
        "SCIENCE" to listOf(Prop(S::globe, 10), Prop(S::volcano, 22), Prop(S::rocket, 16)),
        "LANGUAGE" to listOf(Prop(H::openBook, 22, -6), Prop(H::bookStack, 13), Prop(H::letterBlocks, 20)),
        "COMPUTING" to listOf(Prop(H::laptop, 22), Prop(H::robot, 11), Prop(H::terminal, 18)),
        "COMMERCE" to listOf(Prop(H::growth, 22, -2), Prop(H::calculator, 20), Prop(H::piggy, 14)),
        "SOCIAL" to listOf(Prop(H::pagoda, 16), Prop(H::stupa, 20), Prop(H::map, 22, -2)),
        "HEALTH" to listOf(Prop(H::football, 10), Prop(H::heart, 12), Prop(H::fitness, 22, -2)),
        "EXAM" to listOf(Prop(H::stopwatch, 12), Prop(H::answerSheet, 16, -6), Prop(H::trophy, 10)),
        "GENERAL" to listOf(Prop(H::deskLamp, 22, -4), Prop(H::backpack, 13), Prop(H::paperPlane, 0)),
    )

    /** Which picture a resource gets: the same arithmetic as the old banner art, so a resource keeps its slot. */
    fun variantFor(hash: Int): Int = ((hash ushr 3) and 0x7FFFFFFF) % VARIANTS

    /** Draws banner [variant] of [family] into a new 128 x 64 canvas. */
    fun render(family: String, variant: Int, night: Boolean): PixelCanvas {
        val list = props[family] ?: props.getValue("GENERAL")
        val v = Math.floorMod(variant, VARIANTS)
        val prop = list[v % list.size]
        val backdrop = Backdrop.entries[(v / list.size) % Backdrop.entries.size]
        val cv = PixelCanvas(WIDTH, HEIGHT)
        val seed = family.hashCode() * 31 + v
        val stage = PixelBackdrops.draw(cv, backdrop, night, seed)
        val x = 80 + prop.dx
        if (prop.shadow > 0) cv.contactShadow(x, stage.groundY, prop.shadow, stage.shadow)
        prop.draw(cv, x, stage.groundY - 1)
        return cv
    }
}
