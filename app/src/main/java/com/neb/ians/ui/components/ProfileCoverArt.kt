package com.neb.ians.ui.components

import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import kotlin.math.cos
import kotlin.math.sin

/**
 * The art behind a profile cover.
 *
 * The old cover was six fixed graphite gradients plus a huge centred word.
 * Every admin looked like every other admin, and the word was the only thing
 * in it, so the cover carried no information and no craft. This replaces it
 * with a drawing that is *themed* by role and *seeded* by the username: two
 * moderators share a palette and a motif family, but not a composition.
 *
 * Covers stay deep in both light and dark themes, deliberately. The avatar
 * ring, the deco mark and the profile actions all straddle the cover's lower
 * edge, and a cover that flips to a pale wash in light mode would need a
 * second set of contrast rules for every one of them. Sitting dark in both is
 * what X, GitHub and LinkedIn all settled on for the same reason.
 *
 * The drawing vocabulary is the same as [ResourceBannerArt]: strokes, not
 * fills; a small number of large shapes rather than a busy field; density
 * derived from the box rather than assumed.
 */

/** A cover's identity. Both the palette and the motif come from this. */
enum class CoverRole { ADMIN, MODERATOR, VERIFIED, TUTOR, INSTITUTION, BOT, MEMBER }

/**
 * @property deep   the darkest ground tone, and the vignette
 * @property mid    the ground's middle stop
 * @property rise   the ground's lit corner
 * @property glow   the bloom — one soft light source, placed by seed
 * @property ink    line work; always near-white so strokes hold at low alpha
 * @property accent the one brighter hue, used on a handful of nodes only
 */
data class CoverPalette(
    val deep: Color,
    val mid: Color,
    val rise: Color,
    val glow: Color,
    val ink: Color,
    val accent: Color
)

/**
 * Deep, low-key role tones. Each is dark enough that white ink at 10–30%
 * alpha reads cleanly over it, and separated enough in hue that two roles are
 * never mistaken for each other at thumbnail size.
 */
fun coverPalette(role: CoverRole): CoverPalette = when (role) {
    // Obsidian. Authority reads as absence of colour, not as a loud one.
    CoverRole.ADMIN -> CoverPalette(
        deep = Color(0xFF060608), mid = Color(0xFF131318), rise = Color(0xFF24242C),
        glow = Color(0xFF4A4A5A), ink = Color(0xFFFFFFFF), accent = Color(0xFFCFCFDC)
    )
    // Steel night — the Steel ramp pushed under its own S10.
    CoverRole.MODERATOR -> CoverPalette(
        deep = Color(0xFF05101C), mid = Color(0xFF102338), rise = Color(0xFF1B3A5A),
        glow = Color(0xFF2E5C8C), ink = Color(0xFFFFFFFF), accent = Color(0xFF9FC4EC)
    )
    // Brand night. The only cover that is literally the brand blue, because
    // verification is the badge the brand itself grants.
    CoverRole.VERIFIED -> CoverPalette(
        deep = Color(0xFF03122A), mid = Color(0xFF0A2A5E), rise = Color(0xFF12459B),
        glow = Color(0xFF2C6BE0), ink = Color(0xFFFFFFFF), accent = Color(0xFFAEC9FF)
    )
    // Violet night, matching the Violet ramp the app already uses for tutors.
    CoverRole.TUTOR -> CoverPalette(
        deep = Color(0xFF120B26), mid = Color(0xFF241544), rise = Color(0xFF3C2470),
        glow = Color(0xFF6A43B8), ink = Color(0xFFFFFFFF), accent = Color(0xFFCDB6F5)
    )
    // Pine night. Institutions get the one green in the set.
    CoverRole.INSTITUTION -> CoverPalette(
        deep = Color(0xFF03140F), mid = Color(0xFF0B2A20), rise = Color(0xFF134737),
        glow = Color(0xFF1F6E55), ink = Color(0xFFFFFFFF), accent = Color(0xFFA4DCC4)
    )
    // Cyan night — machine light, and far enough from tutor violet to tell.
    CoverRole.BOT -> CoverPalette(
        deep = Color(0xFF021118), mid = Color(0xFF05283A), rise = Color(0xFF0A4358),
        glow = Color(0xFF13738F), ink = Color(0xFFFFFFFF), accent = Color(0xFF8FE2F7)
    )
    // Slate. The default, and the most common cover in the app by far, so it
    // is the quietest one.
    CoverRole.MEMBER -> CoverPalette(
        deep = Color(0xFF070A11), mid = Color(0xFF141A27), rise = Color(0xFF232E44),
        glow = Color(0xFF3A4C6E), ink = Color(0xFFFFFFFF), accent = Color(0xFFB3C2DB)
    )
}

/**
 * Ground, bloom, vignette and grain — the four layers every cover shares.
 * The motif is drawn on top of this by [drawCoverMotif].
 */
fun DrawScope.drawCoverGround(p: CoverPalette, r: Rng) {
    val w = size.width
    val h = size.height

    // The ground runs on a diagonal rather than straight down, so the lit
    // corner lands somewhere other than "the top", which is where every
    // default gradient in every app puts it.
    val tilt = r.range(0.55f, 1.0f)
    drawRect(
        brush = Brush.linearGradient(
            colors = listOf(p.deep, p.mid, p.rise),
            start = Offset(w * (1f - tilt), h),
            end = Offset(w * tilt, 0f)
        )
    )

    // One soft light source. Its position is the single biggest reason two
    // covers of the same role read as different pictures.
    val bx = w * r.range(0.16f, 0.86f)
    val by = h * r.range(0.02f, 0.46f)
    val span = if (w > h) w else h
    drawRect(
        brush = Brush.radialGradient(
            colors = listOf(p.glow.copy(alpha = 0.50f), p.glow.copy(alpha = 0f)),
            center = Offset(bx, by),
            radius = span * r.range(0.50f, 0.85f)
        )
    )
}

/**
 * The closing layers: a vignette that pulls the eye back to the middle, and a
 * bottom scrim so the avatar's white ring never sits on a lit patch. Drawn
 * *after* the motif, which is why it is separate from [drawCoverGround].
 */
fun DrawScope.drawCoverFinish(p: CoverPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val span = if (w > h) w else h

    drawRect(
        brush = Brush.radialGradient(
            colors = listOf(p.deep.copy(alpha = 0f), p.deep.copy(alpha = 0.55f)),
            center = Offset(w * 0.5f, h * 0.42f),
            radius = span * 0.72f
        )
    )
    drawRect(
        brush = Brush.verticalGradient(
            colors = listOf(p.deep.copy(alpha = 0f), p.deep.copy(alpha = 0.42f)),
            startY = h * 0.52f,
            endY = h
        )
    )

    // Grain. Twenty specks is nothing to draw and it takes the flatness off a
    // large synthetic gradient on an OLED panel.
    val specks = ((w * h) / 2600f).toInt().coerceIn(14, 54)
    for (i in 0 until specks) {
        drawCircle(
            color = p.ink.copy(alpha = r.range(0.02f, 0.07f)),
            radius = r.range(0.5f, 1.4f),
            center = Offset(w * r.next(), h * r.next())
        )
    }
}

/** Dispatches to the role's motif. */
fun DrawScope.drawCoverMotif(role: CoverRole, p: CoverPalette, r: Rng) {
    if (role == CoverRole.ADMIN) {
        coverKeystone(p, r)
    } else if (role == CoverRole.MODERATOR) {
        coverGuard(p, r)
    } else if (role == CoverRole.VERIFIED) {
        coverSeal(p, r)
    } else if (role == CoverRole.TUTOR) {
        coverOrbits(p, r)
    } else if (role == CoverRole.INSTITUTION) {
        coverColonnade(p, r)
    } else if (role == CoverRole.BOT) {
        coverSignal(p, r)
    } else {
        coverRidgeline(p, r)
    }
}

// --------------------------------------------------------------- motifs ----

/**
 * ADMIN — a lattice of interlocking plates, with one of them solid.
 * Structure, and a single piece of it that is answerable.
 */
private fun DrawScope.coverKeystone(p: CoverPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val step = unit * r.range(0.30f, 0.40f)
    val cols = ((w + step) / step).toInt().coerceIn(3, 14)
    val rows = ((h + step) / step).toInt().coerceIn(2, 8)
    val x0 = (w - (cols - 1) * step) * 0.5f
    val y0 = (h - (rows - 1) * step) * 0.5f
    val half = step * 0.48f
    val markCol = r.int(cols)
    val markRow = r.int(rows)

    for (row in 0 until rows) {
        for (col in 0 until cols) {
            val cx = x0 + col * step + (row % 2) * step * 0.5f
            val cy = y0 + row * step
            val path = Path()
            path.moveTo(cx, cy - half)
            path.lineTo(cx + half, cy)
            path.lineTo(cx, cy + half)
            path.lineTo(cx - half, cy)
            path.close()
            // Plates fade toward the left edge, so the lattice reads as a
            // surface catching light rather than as wallpaper.
            val fall = 0.10f + 0.24f * (cx / w)
            if (col == markCol && row == markRow) {
                drawPath(path = path, color = p.accent.copy(alpha = 0.16f))
                drawPath(
                    path = path,
                    color = p.accent.copy(alpha = 0.70f),
                    style = Stroke(width = unit * 0.016f)
                )
            } else {
                drawPath(
                    path = path,
                    color = p.ink.copy(alpha = fall),
                    style = Stroke(width = unit * 0.010f)
                )
            }
        }
    }
}

/**
 * MODERATOR — concentric guard arcs sweeping out of one corner, cut by a
 * rule of tick marks. A shield without drawing a shield.
 */
private fun DrawScope.coverGuard(p: CoverPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val left = r.next() < 0.5f
    val ox = if (left) w * r.range(0.04f, 0.20f) else w * r.range(0.80f, 0.96f)
    val oy = h * r.range(0.92f, 1.10f)
    val gap = unit * r.range(0.20f, 0.28f)
    val rings = ((if (w > h) w else h) / gap).toInt().coerceIn(4, 12)

    for (i in 0 until rings) {
        val rad = gap * (i + 1)
        drawArc(
            color = p.ink.copy(alpha = 0.26f - 0.015f * i),
            startAngle = 180f,
            sweepAngle = 180f,
            useCenter = false,
            topLeft = Offset(ox - rad, oy - rad),
            size = Size(rad * 2f, rad * 2f),
            style = Stroke(width = unit * 0.014f, cap = StrokeCap.Round)
        )
    }

    // The rule: a hairline across the cover with graduated ticks, the way a
    // ruler or a levelling staff is marked.
    val ry = h * r.range(0.24f, 0.40f)
    drawLine(
        color = p.ink.copy(alpha = 0.22f),
        start = Offset(0f, ry),
        end = Offset(w, ry),
        strokeWidth = unit * 0.010f
    )
    val tick = unit * 0.14f
    val ticks = (w / tick).toInt().coerceIn(6, 40)
    for (i in 0 until ticks) {
        val tx = tick * (i + 0.5f)
        val tall = i % 4 == 0
        drawLine(
            color = p.ink.copy(alpha = if (tall) 0.34f else 0.16f),
            start = Offset(tx, ry),
            end = Offset(tx, ry + if (tall) unit * 0.12f else unit * 0.06f),
            strokeWidth = unit * 0.009f
        )
    }
    drawCircle(
        color = p.accent.copy(alpha = 0.85f),
        radius = unit * 0.026f,
        center = Offset(ox, ry)
    )
}

/**
 * VERIFIED — a rosette seal: concentric rings, radial ticks, a scalloped
 * outer edge. Sits off-centre so the cover is not symmetrical.
 */
private fun DrawScope.coverSeal(p: CoverPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * r.range(0.56f, 0.80f)
    val cy = h * r.range(0.40f, 0.58f)
    val rad = unit * r.range(0.30f, 0.40f)

    // Scalloped rim, drawn as one closed path so the cusps stay crisp.
    val lobes = 12 + r.int(7)
    val path = Path()
    val steps = lobes * 12
    for (i in 0 until steps + 1) {
        val ang = i / steps.toFloat() * 6.2831855f
        val wob = rad * (1f + 0.075f * cos(ang * lobes))
        val px = cx + cos(ang) * wob
        val py = cy + sin(ang) * wob
        if (i == 0) {
            path.moveTo(px, py)
        } else {
            path.lineTo(px, py)
        }
    }
    path.close()
    drawPath(
        path = path,
        color = p.ink.copy(alpha = 0.30f),
        style = Stroke(width = unit * 0.013f)
    )

    drawCircle(
        color = p.ink.copy(alpha = 0.22f),
        radius = rad * 0.80f,
        center = Offset(cx, cy),
        style = Stroke(width = unit * 0.010f)
    )
    drawCircle(
        color = p.accent.copy(alpha = 0.55f),
        radius = rad * 0.52f,
        center = Offset(cx, cy),
        style = Stroke(width = unit * 0.016f)
    )

    val spokes = 24
    for (i in 0 until spokes) {
        val ang = i / spokes.toFloat() * 6.2831855f
        val long = i % 3 == 0
        val inner = rad * if (long) 0.58f else 0.66f
        val outer = rad * 0.74f
        drawLine(
            color = p.ink.copy(alpha = if (long) 0.34f else 0.16f),
            start = Offset(cx + cos(ang) * inner, cy + sin(ang) * inner),
            end = Offset(cx + cos(ang) * outer, cy + sin(ang) * outer),
            strokeWidth = unit * 0.010f,
            cap = StrokeCap.Round
        )
    }

    // A check, struck through the core rather than drawn inside a box.
    val arm = rad * 0.30f
    drawLine(
        color = p.accent.copy(alpha = 0.95f),
        start = Offset(cx - arm, cy + arm * 0.10f),
        end = Offset(cx - arm * 0.22f, cy + arm * 0.72f),
        strokeWidth = unit * 0.026f,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.accent.copy(alpha = 0.95f),
        start = Offset(cx - arm * 0.22f, cy + arm * 0.72f),
        end = Offset(cx + arm * 0.96f, cy - arm * 0.74f),
        strokeWidth = unit * 0.026f,
        cap = StrokeCap.Round
    )

    // Loose sparks, so the seal is not floating on an empty field.
    val sparks = 5 + r.int(5)
    for (i in 0 until sparks) {
        drawCircle(
            color = p.ink.copy(alpha = r.range(0.10f, 0.30f)),
            radius = unit * r.range(0.008f, 0.022f),
            center = Offset(w * r.next(), h * r.next())
        )
    }
}

/**
 * TUTOR — tilted orbits around an off-centre core, with a node riding each
 * one. Something taught, orbiting the person who taught it.
 */
private fun DrawScope.coverOrbits(p: CoverPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val cx = w * r.range(0.24f, 0.44f)
    val cy = h * r.range(0.44f, 0.62f)
    val rings = 3 + r.int(2)
    val base = unit * r.range(0.32f, 0.44f)

    for (i in 0 until rings) {
        val grow = 1f + i * 0.34f
        val rx = base * grow
        val ry = base * grow * r.range(0.26f, 0.44f)
        val spin = r.range(-40f, 40f)
        rotate(degrees = spin, pivot = Offset(cx, cy)) {
            drawArc(
                color = p.ink.copy(alpha = 0.30f - 0.05f * i),
                startAngle = 0f,
                sweepAngle = 360f,
                useCenter = false,
                topLeft = Offset(cx - rx, cy - ry),
                size = Size(rx * 2f, ry * 2f),
                style = Stroke(width = unit * 0.012f)
            )
            val at = r.range(0f, 6.2831855f)
            drawCircle(
                color = if (i == 0) p.accent.copy(alpha = 0.95f) else p.ink.copy(alpha = 0.70f),
                radius = unit * (0.030f - 0.005f * i),
                center = Offset(cx + cos(at) * rx, cy + sin(at) * ry)
            )
        }
    }

    // The core: a filled disc with a halo ring, so the centre has weight.
    drawCircle(
        color = p.accent.copy(alpha = 0.22f),
        radius = unit * 0.14f,
        center = Offset(cx, cy)
    )
    drawCircle(
        color = p.accent.copy(alpha = 0.90f),
        radius = unit * 0.070f,
        center = Offset(cx, cy)
    )

    // Rays leaving the core toward the open side of the cover.
    val rays = 4 + r.int(4)
    for (i in 0 until rays) {
        val ang = r.range(-0.9f, 0.9f)
        val len = unit * r.range(0.55f, 1.15f)
        drawLine(
            color = p.ink.copy(alpha = r.range(0.07f, 0.17f)),
            start = Offset(cx + cos(ang) * unit * 0.20f, cy + sin(ang) * unit * 0.20f),
            end = Offset(cx + cos(ang) * len, cy + sin(ang) * len),
            strokeWidth = unit * 0.010f,
            cap = StrokeCap.Round
        )
    }
}

/**
 * INSTITUTION — a colonnade: fluted columns under an architrave, with a
 * stepped base. Read as a building without drawing a building.
 */
private fun DrawScope.coverColonnade(p: CoverPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val baseY = h * r.range(0.80f, 0.90f)
    val capY = h * r.range(0.26f, 0.36f)
    val pitch = unit * r.range(0.26f, 0.34f)
    val cols = (w / pitch).toInt().coerceIn(3, 16)
    val x0 = (w - (cols - 1) * pitch) * 0.5f
    val shaft = pitch * 0.30f
    val markCol = r.int(cols)

    // Architrave: two rules with a pediment slope resting on them.
    drawLine(
        color = p.ink.copy(alpha = 0.34f),
        start = Offset(x0 - pitch * 0.6f, capY),
        end = Offset(x0 + (cols - 1) * pitch + pitch * 0.6f, capY),
        strokeWidth = unit * 0.016f
    )
    drawLine(
        color = p.ink.copy(alpha = 0.18f),
        start = Offset(x0 - pitch * 0.45f, capY - unit * 0.06f),
        end = Offset(x0 + (cols - 1) * pitch + pitch * 0.45f, capY - unit * 0.06f),
        strokeWidth = unit * 0.010f
    )
    val apex = capY - unit * r.range(0.16f, 0.26f)
    val mid = x0 + (cols - 1) * pitch * 0.5f
    drawLine(
        color = p.ink.copy(alpha = 0.26f),
        start = Offset(x0 - pitch * 0.45f, capY - unit * 0.06f),
        end = Offset(mid, apex),
        strokeWidth = unit * 0.012f,
        cap = StrokeCap.Round
    )
    drawLine(
        color = p.ink.copy(alpha = 0.26f),
        start = Offset(mid, apex),
        end = Offset(x0 + (cols - 1) * pitch + pitch * 0.45f, capY - unit * 0.06f),
        strokeWidth = unit * 0.012f,
        cap = StrokeCap.Round
    )

    for (i in 0 until cols) {
        val cx = x0 + i * pitch
        val lit = i == markCol
        val alpha = if (lit) 0.62f else 0.14f + 0.10f * sin(i * 1.7f) * sin(i * 1.7f)
        val ink = if (lit) p.accent.copy(alpha = alpha) else p.ink.copy(alpha = alpha)
        drawLine(
            color = ink,
            start = Offset(cx - shaft * 0.5f, capY),
            end = Offset(cx - shaft * 0.5f, baseY),
            strokeWidth = unit * 0.012f
        )
        drawLine(
            color = ink,
            start = Offset(cx + shaft * 0.5f, capY),
            end = Offset(cx + shaft * 0.5f, baseY),
            strokeWidth = unit * 0.012f
        )
        // Flute: a single inner line is enough at cover scale.
        drawLine(
            color = ink.copy(alpha = alpha * 0.5f),
            start = Offset(cx, capY + unit * 0.04f),
            end = Offset(cx, baseY - unit * 0.04f),
            strokeWidth = unit * 0.008f
        )
    }

    // Stepped base, two treads.
    for (i in 0 until 2) {
        val over = pitch * (0.6f + i * 0.35f)
        drawLine(
            color = p.ink.copy(alpha = 0.30f - i * 0.10f),
            start = Offset(x0 - over, baseY + i * unit * 0.055f),
            end = Offset(x0 + (cols - 1) * pitch + over, baseY + i * unit * 0.055f),
            strokeWidth = unit * 0.014f
        )
    }
}

/**
 * BOT — a routed circuit with pads, and one waveform crossing it. Machine
 * light: orthogonal, regular, and obviously not hand-drawn.
 */
private fun DrawScope.coverSignal(p: CoverPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w
    val lane = unit * r.range(0.16f, 0.22f)
    val lanes = (h / lane).toInt().coerceIn(3, 12)
    val y0 = (h - (lanes - 1) * lane) * 0.5f

    for (i in 0 until lanes) {
        val ly = y0 + i * lane
        val runs = 1 + r.int(3)
        var x = w * r.range(-0.05f, 0.18f)
        for (k in 0 until runs) {
            val len = w * r.range(0.16f, 0.42f)
            val alpha = r.range(0.10f, 0.26f)
            drawLine(
                color = p.ink.copy(alpha = alpha),
                start = Offset(x, ly),
                end = Offset(x + len, ly),
                strokeWidth = unit * 0.011f
            )
            // A trace that turns: the dogleg is what makes it read as routed
            // copper rather than as a set of rules.
            if (r.next() < 0.55f) {
                val drop = lane * (if (r.next() < 0.5f) 1f else -1f)
                drawLine(
                    color = p.ink.copy(alpha = alpha),
                    start = Offset(x + len, ly),
                    end = Offset(x + len + lane * 0.7f, ly + drop),
                    strokeWidth = unit * 0.011f,
                    cap = StrokeCap.Round
                )
            }
            drawCircle(
                color = p.ink.copy(alpha = alpha + 0.16f),
                radius = unit * 0.020f,
                center = Offset(x + len, ly)
            )
            x = x + len + w * r.range(0.06f, 0.16f)
        }
    }

    // One live signal across the board.
    val wy = h * r.range(0.38f, 0.66f)
    val amp = unit * r.range(0.10f, 0.18f)
    val cycles = r.range(1.6f, 3.4f)
    val steps = (w / (unit * 0.05f)).toInt().coerceIn(24, 220)
    val path = Path()
    for (i in 0 until steps + 1) {
        val t = i / steps.toFloat()
        val px = w * t
        val py = wy + sin(t * cycles * 6.2831855f) * amp * (0.35f + 0.65f * sin(t * 3.1415927f))
        if (i == 0) {
            path.moveTo(px, py)
        } else {
            path.lineTo(px, py)
        }
    }
    drawPath(
        path = path,
        color = p.accent.copy(alpha = 0.80f),
        style = Stroke(width = unit * 0.018f, cap = StrokeCap.Round)
    )
}

/**
 * MEMBER — a ridgeline. Nested contours rising out of the lower edge, which
 * is both the quietest thing in the set and the one that means Nepal.
 */
private fun DrawScope.coverRidgeline(p: CoverPalette, r: Rng) {
    val w = size.width
    val h = size.height
    val unit = if (h < w) h else w

    // Sky first: a low sun with a halo, and a handful of stars. Everything
    // after this occludes it, which is what puts the ranges in front.
    val sx = w * r.range(0.14f, 0.86f)
    val sy = h * r.range(0.16f, 0.34f)
    drawRect(
        brush = Brush.radialGradient(
            colors = listOf(p.accent.copy(alpha = 0.22f), p.accent.copy(alpha = 0f)),
            center = Offset(sx, sy),
            radius = unit * 0.34f
        )
    )
    drawCircle(
        color = p.accent.copy(alpha = 0.72f),
        radius = unit * 0.075f,
        center = Offset(sx, sy)
    )
    val stars = 8 + r.int(9)
    for (i in 0 until stars) {
        drawCircle(
            color = p.ink.copy(alpha = r.range(0.10f, 0.34f)),
            radius = unit * r.range(0.004f, 0.012f),
            center = Offset(w * r.next(), h * r.range(0.04f, 0.55f))
        )
    }

    // Ranges, far to near. The far ones are tall and pale and sit high; the
    // near ones are short, opaque and sit low, so each one cuts the one
    // behind it. That occlusion is the entire illusion of depth.
    val ranges = 4 + r.int(2)
    for (k in 0 until ranges) {
        val depth = k / (ranges - 0.999f)
        val baseY = h * (0.62f + 0.34f * depth)
        val amp = unit * (0.50f - 0.085f * k) * r.range(0.80f, 1.10f)
        val freq = r.range(0.8f, 1.5f) + k * 0.55f
        val phase = r.range(0f, 6.2831855f)
        val steps = (w / (unit * 0.045f)).toInt().coerceIn(24, 220)
        // Two paths over the same points: a closed one to occlude what is
        // behind, and an open one to stroke. Stroking the closed one would
        // draw the two vertical sides as well, and a range that ends in a
        // hard vertical line at the edge of the cover looks like a mistake.
        val body = Path()
        val crest = Path()
        body.moveTo(0f, h * 1.2f)
        for (i in 0 until steps + 1) {
            val t = i / steps.toFloat()
            val ridge = (sin(t * freq * 6.2831855f + phase) * 0.62f +
                sin(t * freq * 2.3f * 6.2831855f + phase * 1.7f) * 0.20f +
                sin(t * freq * 0.5f * 6.2831855f + phase * 0.6f) * 0.18f)
            val py = baseY - amp * ridge
            body.lineTo(w * t, py)
            if (i == 0) {
                crest.moveTo(0f, py)
            } else {
                crest.lineTo(w * t, py)
            }
        }
        body.lineTo(w, h * 1.2f)
        body.close()
        drawPath(path = body, color = p.deep.copy(alpha = 0.52f + 0.13f * k))
        drawPath(
            path = crest,
            color = p.ink.copy(alpha = 0.34f - 0.055f * k),
            style = Stroke(width = unit * 0.013f)
        )
    }
}
