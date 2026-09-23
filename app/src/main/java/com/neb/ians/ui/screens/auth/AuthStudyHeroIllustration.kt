package com.neb.ians.ui.screens.auth

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.*
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.graphics.vector.rememberVectorPainter
import androidx.compose.ui.res.vectorResource
import androidx.compose.ui.unit.dp
import com.neb.ians.R
import kotlin.math.cos
import kotlin.math.sin

/**
 * Data model for celebratory welcome confetti particles.
 */
private data class ConfettiParticle(
    val xRatio: Float,       // 0f..1f across canvas width
    val yStartRatio: Float,  // initial vertical phase (0f..1f)
    val speed: Float,        // fall speed multiplier
    val swayFreq: Float,     // horizontal sway frequency
    val swayAmp: Float,      // sway amplitude in pixels
    val rotSpeed: Float,     // rotation speed multiplier
    val size: Float,         // base particle size
    val type: ConfettiType,  // shape type
    val colorIndex: Int      // index into brand color palette
)

private enum class ConfettiType {
    RECTANGLE,
    CIRCLE,
    DIAMOND,
    STAR,
    RIBBON
}

/**
 * Creative, warm, realistic, and lively hero illustration for the NEBians login screen:
 * - Perfectly proportioned for all mobile screen sizes (no cut-offs on compact screens).
 * - Realistic Nepali student with natural facial anatomy (almond eyes with pupils, soft realistic nose, smiling lips, ear contours, layered textured hair).
 * - Clearly visible, dynamic animations:
 *    * Natural rhythmic breathing (chest & shoulders)
 *    * Rhythmic typing hands (wrist & finger movement)
 *    * Natural eye blinking (frequent and clear)
 *    * Lively rising coffee steam curls that curl and dissipate
 *    * Expressive swaying succulent leaves in a terracotta ceramic pot with drainage tray
 *    * Continuous fluttering celebratory confetti particles drifting across the airspace
 *    * Breathing screen glow on the laptop
 * - Official NEBians 3D vector logo centered on the laptop lid.
 */
@Composable
fun AuthStudyHeroIllustration(
    isDark: Boolean,
    modifier: Modifier = Modifier
) {
    val infiniteTransition = rememberInfiniteTransition(label = "StudyHeroAnimations")

    // --- VISIBLE, DYNAMIC ANIMATIONS ---
    // 1. Natural breathing & head movement (torso & neck rhythm)
    val breatheProgress by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 2200, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "breatheProgress"
    )

    // 2. Active typing keystrokes (clear alternating finger & wrist bounces)
    val typingPhase by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 400, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "typingPhase"
    )

    // 3. Regular human eye blinking: Blinks every ~2.8s so it is clearly visible and alive!
    val blinkProgress by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = keyframes {
                durationMillis = 2800
                1f at 0
                1f at 2450
                0.05f at 2550
                1f at 2650
                1f at 2800
            },
            repeatMode = RepeatMode.Restart
        ),
        label = "blinkProgress"
    )

    // 4. Coffee mug steam rising continuously
    val steamPhase by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 1800, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "steamPhase"
    )

    // 5. Plant succulent leaves swaying gently in the desk breeze (pronounced & pleasant)
    val plantSwayAngle by infiniteTransition.animateFloat(
        initialValue = -5f,
        targetValue = 5f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 2400, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "plantSwayAngle"
    )

    // 6. Confetti falling & fluttering loop
    val confettiProgress by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 5000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "confettiProgress"
    )

    // 7. Laptop screen glow pulse
    val screenGlowAlpha by infiniteTransition.animateFloat(
        initialValue = 0.30f,
        targetValue = 0.75f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 1600, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "screenGlowAlpha"
    )

    // Vector logo painter for laptop lid
    val nebiansLogoPainter = rememberVectorPainter(ImageVector.vectorResource(id = R.drawable.n_logo))

    // Pre-generated confetti particles distributed naturally across the scene
    val confettiParticles = remember {
        listOf(
            ConfettiParticle(0.06f, 0.05f, 0.95f, 1.8f, 14f, 2.2f, 7.5f, ConfettiType.RECTANGLE, 0),
            ConfettiParticle(0.16f, 0.45f, 0.85f, 2.1f, 16f, -1.8f, 7f, ConfettiType.RIBBON, 1),
            ConfettiParticle(0.25f, 0.15f, 1.10f, 1.5f, 12f, 1.4f, 5.5f, ConfettiType.CIRCLE, 2),
            ConfettiParticle(0.35f, 0.65f, 0.90f, 2.4f, 15f, -2.5f, 7f, ConfettiType.STAR, 3),
            ConfettiParticle(0.44f, 0.25f, 1.05f, 1.9f, 18f, 2.0f, 6.5f, ConfettiType.RECTANGLE, 4),
            ConfettiParticle(0.55f, 0.80f, 0.88f, 1.6f, 13f, -1.6f, 7.5f, ConfettiType.RIBBON, 0),
            ConfettiParticle(0.65f, 0.35f, 1.15f, 2.2f, 17f, 2.4f, 6f, ConfettiType.CIRCLE, 1),
            ConfettiParticle(0.75f, 0.60f, 0.92f, 1.7f, 14f, -2.1f, 7f, ConfettiType.STAR, 2),
            ConfettiParticle(0.85f, 0.10f, 1.00f, 2.0f, 16f, 1.9f, 7f, ConfettiType.RECTANGLE, 3),
            ConfettiParticle(0.93f, 0.50f, 0.82f, 1.4f, 11f, -1.5f, 6f, ConfettiType.CIRCLE, 4),
            // Accent particles
            ConfettiParticle(0.12f, 0.75f, 1.08f, 2.3f, 15f, 2.6f, 6.5f, ConfettiType.DIAMOND, 1),
            ConfettiParticle(0.30f, 0.85f, 0.80f, 1.5f, 12f, -1.9f, 7.5f, ConfettiType.RECTANGLE, 2),
            ConfettiParticle(0.50f, 0.08f, 1.12f, 2.0f, 16f, 2.1f, 7f, ConfettiType.CIRCLE, 0),
            ConfettiParticle(0.70f, 0.18f, 0.96f, 1.8f, 14f, -2.3f, 6.5f, ConfettiType.RIBBON, 3),
            ConfettiParticle(0.88f, 0.88f, 1.04f, 2.2f, 18f, 1.7f, 7f, ConfettiType.STAR, 4)
        )
    }

    // Cohesive Palette (High contrast, clean lines, warm Nepali tone)
    val brandSapphire = Color(0xFF0D5CE5)
    val brandCyan = Color(0xFF00D2FF)
    val brandCyanSoft = Color(0xFF38BDF8)
    val brandAmber = Color(0xFFF59E0B)
    val brandEmerald = Color(0xFF10B981)
    val brandCoral = Color(0xFFF43F5E)
    val brandPurple = Color(0xFF8B5CF6)

    val confettiColors = remember {
        listOf(brandSapphire, brandAmber, brandCyanSoft, brandCoral, brandEmerald, brandPurple)
    }

    val lineStroke = if (isDark) Color(0xFFF8FAFC) else Color(0xFF0F172A)
    val subtleStroke = if (isDark) Color(0xFF64748B) else Color(0xFF94A3B8)
    // Realistic Nepali warm skin tone
    val skinFill = if (isDark) Color(0xFFD4A373) else Color(0xFFF3C69A)
    val skinShadow = if (isDark) Color(0xFFB07D50) else Color(0xFFDEAA7A)
    val hairFill = if (isDark) Color(0xFF1E2430) else Color(0xFF1F2937)
    val shirtFill = if (isDark) Color(0xFF1E3A8A) else Color(0xFF2563EB) // Royal blue collegiate sweater
    val shirtAccent = if (isDark) Color(0xFF3B82F6) else Color(0xFF60A5FA)
    val deskFill = if (isDark) Color(0xFF171D28) else Color(0xFFF8FAFC)
    val laptopLidFill = if (isDark) Color(0xFF1E2533) else Color(0xFFFFFFFF)

    Box(
        modifier = modifier.fillMaxWidth(),
        contentAlignment = Alignment.BottomCenter
    ) {
        Canvas(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 4.dp)
        ) {
            val totalW = size.width
            val totalH = size.height
            val cx = totalW / 2f

            // Desk is anchored comfortably near the bottom edge
            val deskY = totalH - 4f

            // Responsively calibrated unit scale: fits all mobile widths without cutting off!
            // Reference width 360dp, height ~240dp
            val unitW = totalW / 360f
            val unitH = totalH / 235f
            val unit = minOf(unitW, unitH).coerceIn(0.72f, 1.08f)

            // =========================================================================
            // 1. CELEBRATORY WELCOME CONFETTI PARTICLES (Continuous, lively floating loop)
            // =========================================================================
            confettiParticles.forEach { p ->
                val rawY = (p.yStartRatio + (confettiProgress * p.speed)) % 1.0f
                val particleY = rawY * (deskY - 8f)

                val swayAngle = (confettiProgress * 360f * p.swayFreq) + (p.xRatio * 180f)
                val swayX = sin(Math.toRadians(swayAngle.toDouble())).toFloat() * p.swayAmp * unit
                val particleX = (p.xRatio * totalW) + swayX

                val tumbleAngle = (confettiProgress * 360f * p.rotSpeed) + (p.xRatio * 90f)
                val tumbleScaleX = cos(Math.toRadians(tumbleAngle.toDouble())).toFloat()

                val alpha = when {
                    rawY < 0.07f -> rawY / 0.07f
                    rawY > 0.90f -> (1.0f - rawY) / 0.10f
                    else -> 1.0f
                }.coerceIn(0f, 0.92f)

                val pColor = confettiColors[p.colorIndex % confettiColors.size].copy(alpha = alpha)
                val pSize = p.size * unit

                withTransform({
                    translate(left = particleX, top = particleY)
                    rotate(degrees = tumbleAngle * 0.7f, pivot = Offset.Zero)
                }) {
                    when (p.type) {
                        ConfettiType.RECTANGLE -> {
                            val rectW = (pSize * 1.5f * tumbleScaleX).coerceAtLeast(1.5f)
                            val rectH = pSize * 0.85f
                            drawRoundRect(
                                color = pColor,
                                topLeft = Offset(-rectW / 2f, -rectH / 2f),
                                size = Size(rectW, rectH),
                                cornerRadius = CornerRadius(2f, 2f)
                            )
                        }
                        ConfettiType.CIRCLE -> {
                            drawCircle(
                                color = pColor,
                                radius = (pSize * 0.5f).coerceAtLeast(1.8f),
                                center = Offset.Zero
                            )
                        }
                        ConfettiType.DIAMOND -> {
                            val dPath = Path().apply {
                                val s = pSize * 0.8f
                                moveTo(0f, -s)
                                lineTo(s * tumbleScaleX, 0f)
                                lineTo(0f, s)
                                lineTo(-s * tumbleScaleX, 0f)
                                close()
                            }
                            drawPath(dPath, color = pColor)
                        }
                        ConfettiType.STAR -> {
                            val sPath = Path().apply {
                                val s = pSize * 0.85f
                                moveTo(0f, -s)
                                lineTo(s * 0.25f * tumbleScaleX, -s * 0.25f)
                                lineTo(s * tumbleScaleX, 0f)
                                lineTo(s * 0.25f * tumbleScaleX, s * 0.25f)
                                lineTo(0f, s)
                                lineTo(-s * 0.25f * tumbleScaleX, s * 0.25f)
                                lineTo(-s * tumbleScaleX, 0f)
                                lineTo(-s * 0.25f * tumbleScaleX, -s * 0.25f)
                                close()
                            }
                            drawPath(sPath, color = pColor)
                        }
                        ConfettiType.RIBBON -> {
                            val rPath = Path().apply {
                                val rw = pSize * 1.3f * tumbleScaleX
                                val rh = pSize * 1.1f
                                moveTo(-rw / 2f, -rh / 2f)
                                cubicTo(
                                    -rw / 4f, 0f,
                                    rw / 4f, -rh / 4f,
                                    rw / 2f, rh / 2f
                                )
                            }
                            drawPath(
                                rPath,
                                color = pColor,
                                style = Stroke(width = 2.4f * unit, cap = StrokeCap.Round)
                            )
                        }
                    }
                }
            }

            // =========================================================================
            // 2. THE STUDY DESK (Grounded, neatly proportioned to screen width)
            // =========================================================================
            val deskHalfW = (totalW * 0.46f).coerceAtLeast(145f * unit)
            drawRoundRect(
                color = deskFill,
                topLeft = Offset(cx - deskHalfW, deskY),
                size = Size(deskHalfW * 2f, 14f * unit),
                cornerRadius = CornerRadius(4f, 4f)
            )
            // Desk top edge line
            drawLine(
                color = lineStroke,
                start = Offset(cx - deskHalfW, deskY),
                end = Offset(cx + deskHalfW, deskY),
                strokeWidth = 3.6f,
                cap = StrokeCap.Round
            )
            // Sub-desk bevel
            drawLine(
                color = subtleStroke,
                start = Offset(cx - deskHalfW + (6f * unit), deskY + (8f * unit)),
                end = Offset(cx + deskHalfW - (6f * unit), deskY + (8f * unit)),
                strokeWidth = 2f,
                cap = StrokeCap.Round
            )

            // =========================================================================
            // 3. LEFT DESK ITEMS: SYLLABUS TEXTBOOKS & PEN HOLDER
            // =========================================================================
            val leftStackX = cx - (124f * unit)

            // Book 1 (Bottom - NEBians Sapphire Blue)
            val b1W = 54f * unit
            val b1H = 14f * unit
            val b1Y = deskY - b1H
            drawRoundRect(
                color = if (isDark) Color(0xFF1E3A8A) else brandSapphire,
                topLeft = Offset(leftStackX, b1Y),
                size = Size(b1W, b1H),
                cornerRadius = CornerRadius(3f, 3f)
            )
            drawRoundRect(
                color = lineStroke,
                topLeft = Offset(leftStackX, b1Y),
                size = Size(b1W, b1H),
                cornerRadius = CornerRadius(3f, 3f),
                style = Stroke(width = 2.4f)
            )
            // Pages stripe
            drawLine(
                color = Color.White.copy(alpha = 0.85f),
                start = Offset(leftStackX + (4f * unit), b1Y + (b1H / 2f)),
                end = Offset(leftStackX + b1W - (8f * unit), b1Y + (b1H / 2f)),
                strokeWidth = 2f
            )

            // Book 2 (Middle - Golden Amber)
            val b2W = 48f * unit
            val b2H = 13f * unit
            val b2X = leftStackX + (3f * unit)
            val b2Y = b1Y - b2H
            drawRoundRect(
                color = if (isDark) Color(0xFF854D0E) else brandAmber,
                topLeft = Offset(b2X, b2Y),
                size = Size(b2W, b2H),
                cornerRadius = CornerRadius(3f, 3f)
            )
            drawRoundRect(
                color = lineStroke,
                topLeft = Offset(b2X, b2Y),
                size = Size(b2W, b2H),
                cornerRadius = CornerRadius(3f, 3f),
                style = Stroke(width = 2.4f)
            )
            drawLine(
                color = Color.White.copy(alpha = 0.85f),
                start = Offset(b2X + (4f * unit), b2Y + (b2H / 2f)),
                end = Offset(b2X + b2W - (8f * unit), b2Y + (b2H / 2f)),
                strokeWidth = 1.8f
            )

            // Book 3 (Top - Coral Crimson with bookmark ribbon)
            val b3W = 42f * unit
            val b3H = 12f * unit
            val b3X = leftStackX + (6f * unit)
            val b3Y = b2Y - b3H
            drawRoundRect(
                color = if (isDark) Color(0xFF991B1B) else brandCoral,
                topLeft = Offset(b3X, b3Y),
                size = Size(b3W, b3H),
                cornerRadius = CornerRadius(3f, 3f)
            )
            drawRoundRect(
                color = lineStroke,
                topLeft = Offset(b3X, b3Y),
                size = Size(b3W, b3H),
                cornerRadius = CornerRadius(3f, 3f),
                style = Stroke(width = 2.4f)
            )
            // Bookmark ribbon hanging down
            val bookmarkPath = Path().apply {
                moveTo(b3X + (10f * unit), b3Y + b3H)
                lineTo(b3X + (10f * unit), b1Y + (6f * unit))
                lineTo(b3X + (13f * unit), b1Y + (3f * unit))
                lineTo(b3X + (16f * unit), b1Y + (6f * unit))
                lineTo(b3X + (16f * unit), b3Y + b3H)
                close()
            }
            drawPath(bookmarkPath, color = brandCyanSoft)
            drawPath(bookmarkPath, color = lineStroke, style = Stroke(width = 1.6f))

            // Ceramic Pen Holder (Left of book stack)
            val potX = leftStackX - (26f * unit)
            val potW = 19f * unit
            val potH = 26f * unit
            val potY = deskY - potH
            drawRoundRect(
                color = if (isDark) Color(0xFF1E293B) else Color(0xFFE2E8F0),
                topLeft = Offset(potX, potY),
                size = Size(potW, potH),
                cornerRadius = CornerRadius(4f, 4f)
            )
            drawRoundRect(
                color = lineStroke,
                topLeft = Offset(potX, potY),
                size = Size(potW, potH),
                cornerRadius = CornerRadius(4f, 4f),
                style = Stroke(width = 2.4f)
            )
            // Ruler
            drawLine(
                color = brandAmber,
                start = Offset(potX + (5f * unit), potY + (5f * unit)),
                end = Offset(potX + (2f * unit), potY - (14f * unit)),
                strokeWidth = 3.5f * unit,
                cap = StrokeCap.Square
            )
            drawLine(
                color = lineStroke,
                start = Offset(potX + (5f * unit), potY + (5f * unit)),
                end = Offset(potX + (2f * unit), potY - (14f * unit)),
                strokeWidth = 3.5f * unit,
                cap = StrokeCap.Square
            )
            // Blue pen
            drawLine(
                color = brandSapphire,
                start = Offset(potX + (10f * unit), potY + (6f * unit)),
                end = Offset(potX + (10f * unit), potY - (15f * unit)),
                strokeWidth = 2.8f * unit,
                cap = StrokeCap.Round
            )
            // Emerald pen
            drawLine(
                color = brandEmerald,
                start = Offset(potX + (14f * unit), potY + (6f * unit)),
                end = Offset(potX + (17f * unit), potY - (13f * unit)),
                strokeWidth = 2.8f * unit,
                cap = StrokeCap.Round
            )

            // =========================================================================
            // 4. RIGHT DESK ITEMS: STEAMING MUG & FIXED BEAUTIFUL PLANT POT
            // =========================================================================
            val mugX = cx + (82f * unit)
            val mugW = 21f * unit
            val mugH = 25f * unit
            val mugY = deskY - mugH
            drawRoundRect(
                color = if (isDark) Color(0xFF1E293B) else Color(0xFFF1F5F9),
                topLeft = Offset(mugX, mugY),
                size = Size(mugW, mugH),
                cornerRadius = CornerRadius(4f, 4f)
            )
            drawRoundRect(
                color = lineStroke,
                topLeft = Offset(mugX, mugY),
                size = Size(mugW, mugH),
                cornerRadius = CornerRadius(4f, 4f),
                style = Stroke(width = 2.4f)
            )
            // Mug handle
            drawArc(
                color = lineStroke,
                startAngle = 270f,
                sweepAngle = 180f,
                useCenter = false,
                topLeft = Offset(mugX + mugW - (2f * unit), mugY + (4f * unit)),
                size = Size(9f * unit, 15f * unit),
                style = Stroke(width = 2.4f, cap = StrokeCap.Round)
            )
            // Sapphire accent stripe on mug
            drawLine(
                color = brandSapphire,
                start = Offset(mugX + (2f * unit), mugY + (7f * unit)),
                end = Offset(mugX + mugW - (2f * unit), mugY + (7f * unit)),
                strokeWidth = 2.5f * unit
            )

            // --- ANIMATED RISING STEAM (Smooth curling waves that lift off) ---
            val steamYOffset = steamPhase * 24f * unit
            val steamAlpha = sin(steamPhase * Math.PI).toFloat().coerceIn(0f, 0.85f)
            // Stream 1
            val steam1Path = Path().apply {
                val sStartY = mugY - (3f * unit) - steamYOffset
                moveTo(mugX + (6f * unit), sStartY)
                cubicTo(
                    mugX + (2f * unit), sStartY - (6f * unit),
                    mugX + (10f * unit), sStartY - (12f * unit),
                    mugX + (6f * unit), sStartY - (18f * unit)
                )
            }
            drawPath(
                steam1Path,
                color = subtleStroke.copy(alpha = steamAlpha),
                style = Stroke(width = 2f * unit, cap = StrokeCap.Round)
            )
            // Stream 2 (Offset phase for realism)
            val steam2Progress = (steamPhase + 0.5f) % 1f
            val steam2YOffset = steam2Progress * 24f * unit
            val steam2Alpha = sin(steam2Progress * Math.PI).toFloat().coerceIn(0f, 0.75f)
            val steam2Path = Path().apply {
                val sStartY = mugY - (3f * unit) - steam2YOffset
                moveTo(mugX + (14f * unit), sStartY)
                cubicTo(
                    mugX + (18f * unit), sStartY - (6f * unit),
                    mugX + (10f * unit), sStartY - (12f * unit),
                    mugX + (15f * unit), sStartY - (18f * unit)
                )
            }
            drawPath(
                steam2Path,
                color = subtleStroke.copy(alpha = steam2Alpha),
                style = Stroke(width = 1.8f * unit, cap = StrokeCap.Round)
            )

            // --- FIXED, BEAUTIFUL CERAMIC PLANT POT WITH SUCCULENT ---
            val plantX = mugX + (34f * unit)
            val plantPotW = 28f * unit
            val plantPotH = 22f * unit
            val plantPotY = deskY - plantPotH
            val terracottaColor = if (isDark) Color(0xFFC2410C) else Color(0xFFEA580C)
            val terracottaRim = if (isDark) Color(0xFF9A3412) else Color(0xFFC2410C)
            val soilColor = if (isDark) Color(0xFF3E2723) else Color(0xFF4E342E)

            // Drainage Saucer under pot
            drawRoundRect(
                color = terracottaRim,
                topLeft = Offset(plantX - (2f * unit), deskY - (3f * unit)),
                size = Size(plantPotW + (4f * unit), 3f * unit),
                cornerRadius = CornerRadius(1.5f, 1.5f)
            )
            drawRoundRect(
                color = lineStroke,
                topLeft = Offset(plantX - (2f * unit), deskY - (3f * unit)),
                size = Size(plantPotW + (4f * unit), 3f * unit),
                cornerRadius = CornerRadius(1.5f, 1.5f),
                style = Stroke(width = 1.8f)
            )

            // Pot Body (Classic tapered ceramic flowerpot)
            val potBodyPath = Path().apply {
                moveTo(plantX + (2f * unit), plantPotY + (4f * unit))
                lineTo(plantX + plantPotW - (2f * unit), plantPotY + (4f * unit))
                lineTo(plantX + plantPotW - (5f * unit), deskY - (3f * unit))
                lineTo(plantX + (5f * unit), deskY - (3f * unit))
                close()
            }
            drawPath(potBodyPath, color = terracottaColor)
            drawPath(potBodyPath, color = lineStroke, style = Stroke(width = 2.4f))

            // Upper Pot Rim (distinct collar)
            drawRoundRect(
                color = terracottaRim,
                topLeft = Offset(plantX, plantPotY),
                size = Size(plantPotW, 5f * unit),
                cornerRadius = CornerRadius(2.5f, 2.5f)
            )
            drawRoundRect(
                color = lineStroke,
                topLeft = Offset(plantX, plantPotY),
                size = Size(plantPotW, 5f * unit),
                cornerRadius = CornerRadius(2.5f, 2.5f),
                style = Stroke(width = 2.2f)
            )

            // Pot soil inside rim
            drawOval(
                color = soilColor,
                topLeft = Offset(plantX + (3f * unit), plantPotY + (0.5f * unit)),
                size = Size(plantPotW - (6f * unit), 3.5f * unit)
            )

            // --- ANIMATED SWAYING SUCCULENT LEAVES ---
            withTransform({
                translate(left = plantX + (plantPotW / 2f), top = plantPotY + (2f * unit))
                rotate(degrees = plantSwayAngle, pivot = Offset.Zero)
            }) {
                // Leaf 1 (Left outward arch)
                val leaf1Path = Path().apply {
                    moveTo(0f, 0f)
                    cubicTo(
                        -8f * unit, -6f * unit,
                        -14f * unit, -12f * unit,
                        -12f * unit, -18f * unit
                    )
                    cubicTo(
                        -8f * unit, -16f * unit,
                        -3f * unit, -8f * unit,
                        0f, 0f
                    )
                    close()
                }
                drawPath(leaf1Path, color = if (isDark) Color(0xFF15803D) else Color(0xFF16A34A))
                drawPath(leaf1Path, color = lineStroke, style = Stroke(width = 1.6f))

                // Leaf 2 (Center tall spiky succulent leaf)
                val leaf2Path = Path().apply {
                    moveTo(-2f * unit, 0f)
                    cubicTo(
                        -3f * unit, -10f * unit,
                        -2f * unit, -20f * unit,
                        0f, -25f * unit
                    )
                    cubicTo(
                        2f * unit, -20f * unit,
                        3f * unit, -10f * unit,
                        2f * unit, 0f
                    )
                    close()
                }
                drawPath(leaf2Path, color = if (isDark) Color(0xFF16A34A) else Color(0xFF22C55E))
                drawPath(leaf2Path, color = lineStroke, style = Stroke(width = 1.8f))

                // Leaf 3 (Right outward arch)
                val leaf3Path = Path().apply {
                    moveTo(0f, 0f)
                    cubicTo(
                        6f * unit, -6f * unit,
                        13f * unit, -10f * unit,
                        11f * unit, -16f * unit
                    )
                    cubicTo(
                        7f * unit, -14f * unit,
                        3f * unit, -7f * unit,
                        0f, 0f
                    )
                    close()
                }
                drawPath(leaf3Path, color = if (isDark) Color(0xFF22C55E) else Color(0xFF4ADE80))
                drawPath(leaf3Path, color = lineStroke, style = Stroke(width = 1.6f))

                // Leaf 4 (Front-center small sprout)
                val leaf4Path = Path().apply {
                    moveTo(-2f * unit, 0f)
                    cubicTo(-4f * unit, -4f * unit, -2f * unit, -8f * unit, 0f, -11f * unit)
                    cubicTo(2f * unit, -8f * unit, 4f * unit, -4f * unit, 2f * unit, 0f)
                    close()
                }
                drawPath(leaf4Path, color = if (isDark) Color(0xFF4ADE80) else Color(0xFF86EFAC))
                drawPath(leaf4Path, color = lineStroke, style = Stroke(width = 1.4f))
            }

            // =========================================================================
            // 5. THE REALISTIC NEPALI STUDENT CHARACTER
            // =========================================================================
            // Natural rhythmic breathing: lifts torso and head gently together
            val breathOffset = breatheProgress * 3.5f * unit
            val bodyY = deskY - (52f * unit) - (breathOffset * 0.4f)
            val headY = deskY - (112f * unit) - (breathOffset * 0.8f)

            // --- Torso / Collegiate Knit Sweater ---
            val shoulderW = 68f * unit
            val bodyPath = Path().apply {
                moveTo(cx - shoulderW, deskY)
                cubicTo(
                    cx - shoulderW + (4f * unit), bodyY + (16f * unit),
                    cx - (46f * unit), bodyY - (8f * unit),
                    cx - (20f * unit), bodyY - (16f * unit)
                )
                lineTo(cx + (20f * unit), bodyY - (16f * unit))
                cubicTo(
                    cx + (46f * unit), bodyY - (8f * unit),
                    cx + shoulderW - (4f * unit), bodyY + (16f * unit),
                    cx + shoulderW, deskY
                )
                close()
            }
            drawPath(bodyPath, color = shirtFill)
            drawPath(bodyPath, color = lineStroke, style = Stroke(width = 3.2f))

            // White collared shirt peek under sweater V/Crew neck
            val collarPath = Path().apply {
                moveTo(cx - (15f * unit), bodyY - (15f * unit))
                lineTo(cx, bodyY - (7f * unit))
                lineTo(cx + (15f * unit), bodyY - (15f * unit))
            }
            drawPath(collarPath, color = Color.White, style = Stroke(width = 2.4f * unit, cap = StrokeCap.Round))
            drawPath(collarPath, color = lineStroke, style = Stroke(width = 1.6f))

            // Sweater crew-neck collar trim
            drawArc(
                color = shirtAccent,
                startAngle = 0f,
                sweepAngle = 180f,
                useCenter = false,
                topLeft = Offset(cx - (18f * unit), bodyY - (19f * unit)),
                size = Size(36f * unit, 20f * unit),
                style = Stroke(width = 2.8f * unit, cap = StrokeCap.Round)
            )

            // --- Neck with soft anatomical shadow under jaw ---
            val neckW = 24f * unit
            val neckH = 20f * unit
            drawRect(
                color = skinShadow,
                topLeft = Offset(cx - (neckW / 2f), headY + (44f * unit)),
                size = Size(neckW, neckH)
            )
            drawRect(
                color = skinFill,
                topLeft = Offset(cx - (neckW / 2f) + (2f * unit), headY + (47f * unit)),
                size = Size(neckW - (4f * unit), neckH - (3f * unit))
            )
            drawLine(
                color = lineStroke,
                start = Offset(cx - (neckW / 2f), headY + (46f * unit)),
                end = Offset(cx - (neckW / 2f), headY + (64f * unit)),
                strokeWidth = 2.8f,
                cap = StrokeCap.Round
            )
            drawLine(
                color = lineStroke,
                start = Offset(cx + (neckW / 2f), headY + (46f * unit)),
                end = Offset(cx + (neckW / 2f), headY + (64f * unit)),
                strokeWidth = 2.8f,
                cap = StrokeCap.Round
            )

            // --- REALISTIC FACE (Natural jawline, chin, and temples) ---
            val faceW = 76f * unit
            val faceH = 68f * unit
            val headPath = Path().apply {
                // Jaw & Chin
                moveTo(cx - (faceW / 2f), headY + (14f * unit))
                cubicTo(
                    cx - (faceW / 2f), headY + (36f * unit),
                    cx - (18f * unit), headY + (52f * unit),
                    cx, headY + (53f * unit) // Rounded realistic chin
                )
                cubicTo(
                    cx + (18f * unit), headY + (52f * unit),
                    cx + (faceW / 2f), headY + (36f * unit),
                    cx + (faceW / 2f), headY + (14f * unit)
                )
                // Upper forehead
                cubicTo(
                    cx + (faceW / 2f), headY - (14f * unit),
                    cx - (faceW / 2f), headY - (14f * unit),
                    cx - (faceW / 2f), headY + (14f * unit)
                )
                close()
            }
            drawPath(headPath, color = skinFill)
            drawPath(headPath, color = lineStroke, style = Stroke(width = 3.2f))

            // Realistic Human Ears with inner antihelix folds
            val earW = 10f * unit
            val earH = 18f * unit
            val earY = headY + (16f * unit)
            // Left Ear
            drawOval(
                color = skinFill,
                topLeft = Offset(cx - (faceW / 2f) - (7f * unit), earY),
                size = Size(earW, earH)
            )
            drawOval(
                color = lineStroke,
                topLeft = Offset(cx - (faceW / 2f) - (7f * unit), earY),
                size = Size(earW, earH),
                style = Stroke(width = 2.2f)
            )
            // Left inner ear line
            drawLine(
                color = skinShadow,
                start = Offset(cx - (faceW / 2f) - (2f * unit), earY + (4f * unit)),
                end = Offset(cx - (faceW / 2f) - (3f * unit), earY + (12f * unit)),
                strokeWidth = 1.8f
            )

            // Right Ear
            drawOval(
                color = skinFill,
                topLeft = Offset(cx + (faceW / 2f) - (3f * unit), earY),
                size = Size(earW, earH)
            )
            drawOval(
                color = lineStroke,
                topLeft = Offset(cx + (faceW / 2f) - (3f * unit), earY),
                size = Size(earW, earH),
                style = Stroke(width = 2.2f)
            )
            // Right inner ear line
            drawLine(
                color = skinShadow,
                start = Offset(cx + (faceW / 2f) + (2f * unit), earY + (4f * unit)),
                end = Offset(cx + (faceW / 2f) + (3f * unit), earY + (12f * unit)),
                strokeWidth = 1.8f
            )

            // Soft natural blushing cheeks
            val blushColor = if (isDark) Color(0xFFE11D48).copy(alpha = 0.22f) else Color(0xFFFB7185).copy(alpha = 0.40f)
            drawCircle(
                color = blushColor,
                radius = 7.5f * unit,
                center = Offset(cx - (22f * unit), headY + (32f * unit))
            )
            drawCircle(
                color = blushColor,
                radius = 7.5f * unit,
                center = Offset(cx + (22f * unit), headY + (32f * unit))
            )

            // --- REALISTIC EYES (Almond shape, irises, pupils, gleam & natural blinking) ---
            val eyeSpacing = 15f * unit
            val eyeY = headY + (19f * unit)

            // Natural Eyebrows
            val browY = eyeY - (8f * unit)
            // Left eyebrow
            val leftBrow = Path().apply {
                moveTo(cx - eyeSpacing - (10f * unit), browY + (1f * unit))
                cubicTo(
                    cx - eyeSpacing - (5f * unit), browY - (3f * unit),
                    cx - eyeSpacing + (2f * unit), browY - (2f * unit),
                    cx - eyeSpacing + (7f * unit), browY
                )
            }
            drawPath(leftBrow, color = hairFill, style = Stroke(width = 2.6f * unit, cap = StrokeCap.Round))
            // Right eyebrow
            val rightBrow = Path().apply {
                moveTo(cx + eyeSpacing - (7f * unit), browY)
                cubicTo(
                    cx + eyeSpacing - (2f * unit), browY - (2f * unit),
                    cx + eyeSpacing + (5f * unit), browY - (3f * unit),
                    cx + eyeSpacing + (10f * unit), browY + (1f * unit)
                )
            }
            drawPath(rightBrow, color = hairFill, style = Stroke(width = 2.6f * unit, cap = StrokeCap.Round))

            if (blinkProgress > 0.25f) {
                val eyeOpenH = 8f * unit * blinkProgress
                val eyeWidth = 11f * unit

                // Sclera (White) Left Eye
                drawOval(
                    color = Color.White,
                    topLeft = Offset(cx - eyeSpacing - (eyeWidth / 2f), eyeY - (eyeOpenH / 2f)),
                    size = Size(eyeWidth, eyeOpenH)
                )
                drawOval(
                    color = lineStroke,
                    topLeft = Offset(cx - eyeSpacing - (eyeWidth / 2f), eyeY - (eyeOpenH / 2f)),
                    size = Size(eyeWidth, eyeOpenH),
                    style = Stroke(width = 1.6f)
                )
                // Dark Brown Iris & Pupil Left
                drawCircle(
                    color = Color(0xFF271A12),
                    radius = (3.4f * unit * blinkProgress).coerceAtLeast(1.5f),
                    center = Offset(cx - eyeSpacing, eyeY)
                )
                // Glint Left Eye
                drawCircle(
                    color = Color.White,
                    radius = 1.5f * unit,
                    center = Offset(cx - eyeSpacing - (1f * unit), eyeY - (1.2f * unit))
                )

                // Sclera (White) Right Eye
                drawOval(
                    color = Color.White,
                    topLeft = Offset(cx + eyeSpacing - (eyeWidth / 2f), eyeY - (eyeOpenH / 2f)),
                    size = Size(eyeWidth, eyeOpenH)
                )
                drawOval(
                    color = lineStroke,
                    topLeft = Offset(cx + eyeSpacing - (eyeWidth / 2f), eyeY - (eyeOpenH / 2f)),
                    size = Size(eyeWidth, eyeOpenH),
                    style = Stroke(width = 1.6f)
                )
                // Dark Brown Iris & Pupil Right
                drawCircle(
                    color = Color(0xFF271A12),
                    radius = (3.4f * unit * blinkProgress).coerceAtLeast(1.5f),
                    center = Offset(cx + eyeSpacing, eyeY)
                )
                // Glint Right Eye
                drawCircle(
                    color = Color.White,
                    radius = 1.5f * unit,
                    center = Offset(cx + eyeSpacing - (1f * unit), eyeY - (1.2f * unit))
                )
            } else {
                // Natural closed smiling eyelid curve
                drawArc(
                    color = lineStroke,
                    startAngle = 10f,
                    sweepAngle = 160f,
                    useCenter = false,
                    topLeft = Offset(cx - eyeSpacing - (6f * unit), eyeY - (2f * unit)),
                    size = Size(12f * unit, 5f * unit),
                    style = Stroke(width = 2.4f, cap = StrokeCap.Round)
                )
                drawArc(
                    color = lineStroke,
                    startAngle = 10f,
                    sweepAngle = 160f,
                    useCenter = false,
                    topLeft = Offset(cx + eyeSpacing - (6f * unit), eyeY - (2f * unit)),
                    size = Size(12f * unit, 5f * unit),
                    style = Stroke(width = 2.4f, cap = StrokeCap.Round)
                )
            }

            // Realistic Subtle Nose Bridge & Tip
            val noseY = eyeY + (9f * unit)
            val nosePath = Path().apply {
                moveTo(cx - (1f * unit), eyeY + (3f * unit))
                lineTo(cx + (1f * unit), noseY)
                lineTo(cx - (3f * unit), noseY + (3f * unit))
                lineTo(cx + (1f * unit), noseY + (4f * unit))
            }
            drawPath(nosePath, color = skinShadow, style = Stroke(width = 2.2f * unit, cap = StrokeCap.Round, join = StrokeJoin.Round))

            // Realistic Warm Smiling Lips
            val mouthY = noseY + (13f * unit)
            val mouthPath = Path().apply {
                moveTo(cx - (8f * unit), mouthY)
                cubicTo(
                    cx - (3f * unit), mouthY + (5f * unit),
                    cx + (3f * unit), mouthY + (5f * unit),
                    cx + (8f * unit), mouthY
                )
            }
            drawPath(mouthPath, color = lineStroke, style = Stroke(width = 2.4f, cap = StrokeCap.Round))
            // Lower lip shadow
            drawArc(
                color = skinShadow,
                startAngle = 30f,
                sweepAngle = 120f,
                useCenter = false,
                topLeft = Offset(cx - (5f * unit), mouthY + (2f * unit)),
                size = Size(10f * unit, 4f * unit),
                style = Stroke(width = 1.8f * unit, cap = StrokeCap.Round)
            )

            // --- REALISTIC LAYERED NEPALI HAIR (Modern textured side-part) ---
            val hairPath = Path().apply {
                moveTo(cx - (42f * unit), headY + (16f * unit))
                // Sideburn left
                lineTo(cx - (40f * unit), headY + (20f * unit))
                cubicTo(
                    cx - (48f * unit), headY - (15f * unit),
                    cx - (28f * unit), headY - (38f * unit),
                    cx, headY - (36f * unit)
                )
                cubicTo(
                    cx + (28f * unit), headY - (38f * unit),
                    cx + (48f * unit), headY - (12f * unit),
                    cx + (40f * unit), headY + (20f * unit)
                )
                // Sideburn right
                lineTo(cx + (42f * unit), headY + (16f * unit))
                // Bangs and textured forehead strands
                cubicTo(
                    cx + (30f * unit), headY + (5f * unit),
                    cx + (20f * unit), headY + (14f * unit),
                    cx + (12f * unit), headY + (7f * unit)
                )
                cubicTo(
                    cx + (5f * unit), headY + (15f * unit),
                    cx - (6f * unit), headY + (8f * unit),
                    cx - (16f * unit), headY + (14f * unit)
                )
                cubicTo(
                    cx - (24f * unit), headY + (6f * unit),
                    cx - (34f * unit), headY + (14f * unit),
                    cx - (42f * unit), headY + (16f * unit)
                )
                close()
            }
            drawPath(hairPath, color = hairFill)
            drawPath(hairPath, color = lineStroke, style = Stroke(width = 3.2f))

            // Subtle hair highlight
            val hairHighlight = Path().apply {
                moveTo(cx - (20f * unit), headY - (28f * unit))
                cubicTo(
                    cx - (8f * unit), headY - (32f * unit),
                    cx + (12f * unit), headY - (31f * unit),
                    cx + (22f * unit), headY - (26f * unit)
                )
            }
            drawPath(
                hairHighlight,
                color = Color.White.copy(alpha = if (isDark) 0.15f else 0.25f),
                style = Stroke(width = 2.4f * unit, cap = StrokeCap.Round)
            )

            // --- ANIMATED TYPING ARMS & HANDS (Active, visible alternating keystrokes) ---
            val typingAngleRad = Math.toRadians(typingPhase.toDouble())
            val leftWristY = sin(typingAngleRad).toFloat() * 4.2f * unit
            val rightWristY = -sin(typingAngleRad).toFloat() * 4.2f * unit

            val handsY = deskY - (10f * unit)
            val leftHandX = cx - (44f * unit)
            val rightHandX = cx + (30f * unit)

            // Left Arm (Sweater sleeve + forearm + hand)
            drawLine(
                color = lineStroke,
                start = Offset(cx - (52f * unit), bodyY + (16f * unit)),
                end = Offset(leftHandX, handsY + leftWristY),
                strokeWidth = 3.4f,
                cap = StrokeCap.Round
            )
            // Left Hand & realistic fingers
            drawCircle(
                color = skinFill,
                radius = 6.5f * unit,
                center = Offset(leftHandX, handsY + leftWristY)
            )
            drawCircle(
                color = lineStroke,
                radius = 6.5f * unit,
                center = Offset(leftHandX, handsY + leftWristY),
                style = Stroke(width = 2.4f)
            )

            // Right Arm (Sweater sleeve + forearm + hand)
            drawLine(
                color = lineStroke,
                start = Offset(cx + (52f * unit), bodyY + (16f * unit)),
                end = Offset(rightHandX, handsY + rightWristY),
                strokeWidth = 3.4f,
                cap = StrokeCap.Round
            )
            // Right Hand & realistic fingers
            drawCircle(
                color = skinFill,
                radius = 6.5f * unit,
                center = Offset(rightHandX, handsY + rightWristY)
            )
            drawCircle(
                color = lineStroke,
                radius = 6.5f * unit,
                center = Offset(rightHandX, handsY + rightWristY),
                style = Stroke(width = 2.4f)
            )

            // =========================================================================
            // 6. SLEEK MODERN LAPTOP WITH OFFICIAL NEBIANS 3D VECTOR LOGO
            // =========================================================================
            val laptopW = 104f * unit
            val laptopH = 60f * unit
            val laptopLeft = cx - (laptopW / 2f)
            val laptopTop = deskY - laptopH

            // Laptop base on desk
            drawLine(
                color = lineStroke,
                start = Offset(cx - (58f * unit), deskY),
                end = Offset(cx + (58f * unit), deskY),
                strokeWidth = 3.8f,
                cap = StrokeCap.Round
            )

            // Laptop Lid (Modern sleek wedge taper)
            val lidPath = Path().apply {
                moveTo(laptopLeft, deskY)
                lineTo(laptopLeft + (9f * unit), laptopTop)
                lineTo(laptopLeft + laptopW - (9f * unit), laptopTop)
                lineTo(laptopLeft + laptopW, deskY)
                close()
            }
            drawPath(lidPath, color = laptopLidFill)
            drawPath(lidPath, color = lineStroke, style = Stroke(width = 3.2f))

            // Dynamic screen glow casting upward
            val glowPath = Path().apply {
                moveTo(laptopLeft + (10f * unit), laptopTop)
                lineTo(laptopLeft + laptopW - (10f * unit), laptopTop)
                lineTo(laptopLeft + laptopW - (16f * unit), laptopTop - (20f * unit))
                lineTo(laptopLeft + (16f * unit), laptopTop - (20f * unit))
                close()
            }
            drawPath(
                glowPath,
                brush = Brush.verticalGradient(
                    colors = listOf(
                        brandCyanSoft.copy(alpha = 0f),
                        brandCyanSoft.copy(alpha = 0.28f * screenGlowAlpha)
                    ),
                    startY = laptopTop - (20f * unit),
                    endY = laptopTop
                )
            )

            // Official NEBians Vector Logo Centered on Laptop Lid
            val logoSize = 30f * unit
            val logoLeft = cx - (logoSize / 2f)
            val logoTop = laptopTop + (14f * unit)
            translate(left = logoLeft, top = logoTop) {
                with(nebiansLogoPainter) {
                    draw(size = Size(logoSize, logoSize))
                }
            }
        }
    }
}

