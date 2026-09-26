package com.neb.ians.ui.components

import android.graphics.RuntimeShader
import android.os.Build
import androidx.annotation.RequiresApi
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.Stable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.draw.drawWithContent
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.BlurEffect
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Outline
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.Shape
import androidx.compose.ui.graphics.TileMode
import androidx.compose.ui.graphics.asComposeRenderEffect
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.clipPath
import androidx.compose.ui.graphics.drawscope.translate
import androidx.compose.ui.graphics.layer.GraphicsLayer
import androidx.compose.ui.graphics.layer.drawLayer
import androidx.compose.ui.graphics.rememberGraphicsLayer
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.IntSize
import androidx.compose.ui.unit.dp
import com.neb.ians.util.rememberIsLowEndDevice
import kotlin.math.cos
import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * Liquid glass.
 *
 * Not a translucent fill with a blur behind it — that is frosted plastic, and
 * it is what almost everything calling itself glassmorphism actually is. Real
 * glass does four things that plastic does not, and all four are here:
 *
 *   It *refracts*. Near the edge the material is thick and curved, so what is
 *   behind it is pulled inward and magnified. This is the single biggest tell:
 *   a straight line crossing under the edge of real glass bends. It is done in
 *   AGSL, by sampling the backdrop along the shape's own signed-distance
 *   gradient, with the displacement concentrated into the outer few pixels.
 *
 *   It *disperses*. Glass bends red and blue by slightly different amounts, so
 *   the refracted rim carries a faint colour fringe. Two extra taps, cheap, and
 *   the eye reads it as material rather than as a filter.
 *
 *   It *catches light*. A specular band sits where the surface normal faces the
 *   light, and the opposite rim darkens. Together they give the edge thickness.
 *   Without them the shape looks cut out of the page rather than laid on it.
 *
 *   It *carries colour forward*. Glass lifts the saturation of what it holds
 *   slightly rather than washing it out.
 *
 * The backdrop is real, not faked: the page records itself into a GraphicsLayer
 * ([Modifier.nebGlassBackdrop]) and each glass surface re-draws that layer,
 * offset to its own position, through its own shader. So the glass shows what
 * is genuinely underneath it and follows it as the page scrolls.
 *
 * Three tiers, chosen per device:
 *
 *   API 33+       blur, refraction, dispersion, specular — the full material.
 *   API 31-32     blur plus the drawn rim; no AGSL, so no bending.
 *   below 31      a tinted surface. No backdrop blur exists to build on.
 *
 * Low-end devices take the bottom tier regardless of API level.
 *
 * ---------------------------------------------------------------------------
 * To revert all of it, set [NEB_LIQUID_GLASS] to false. Every call site falls
 * back to the opaque surface it had before, with no other change.
 * ---------------------------------------------------------------------------
 */
const val NEB_LIQUID_GLASS = true

/** How much of the material is exposed. Tuned per surface, not per theme. */
@Immutable
data class NebGlassStyle(
    /** Backdrop blur. Modest on purpose — blur past ~20dp destroys the detail
     *  the refraction needs in order to be visible at all. */
    val blur: Dp = 16.dp,
    /** How far the rim pulls the backdrop inward at its strongest point. */
    val refraction: Dp = 13.dp,
    /** Width of the band the refraction lives in, measured from the edge. */
    val rim: Dp = 20.dp,
    /** Chromatic spread across that band, as a fraction of the displacement. */
    val dispersion: Float = 0.07f,
    val tint: Color = Color.White,
    val tintAlpha: Float = 0.10f,
    val saturation: Float = 1.22f,
    val specular: Float = 0.42f,
    val shade: Float = 0.26f,
    /** Where the light is, in degrees clockwise from "right". */
    val lightAngle: Float = -55f,
    /** The drawn hairline on top of the shader. Glass has an actual edge. */
    val rimLight: Color = Color.White,
    val rimLightAlpha: Float = 0.55f,
)

/**
 * The two readings.
 *
 * Tint alpha is the whole argument here. The reference this was built against
 * is a demo panel over flat colour blocks, where near-zero tint looks superb.
 * A navigation bar is not that: it sits over body text and thumbnails, and its
 * own icons have to win. So the tint is set at the point where the backdrop is
 * unmistakably *there* and moving — you can see the page slide under the rail
 * and bend at its edge — while the labels on top still read cleanly. Light
 * glass tints white, dark glass tints toward the deep navy of the dark surface
 * ramp, because a white haze over a dark page reads as fog, not glass.
 */
@Composable
fun rememberNebGlassStyle(isDark: Boolean): NebGlassStyle = remember(isDark) {
    if (isDark) {
        NebGlassStyle(
            blur = 15.dp,
            refraction = 14.dp,
            rim = 21.dp,
            dispersion = 0.08f,
            tint = Color(0xFF0B1220),
            tintAlpha = 0.30f,
            saturation = 1.34f,
            specular = 0.52f,
            shade = 0.34f,
            rimLight = Color.White,
            rimLightAlpha = 0.30f
        )
    } else {
        NebGlassStyle(
            blur = 15.dp,
            refraction = 14.dp,
            rim = 21.dp,
            dispersion = 0.07f,
            tint = Color.White,
            tintAlpha = 0.34f,
            saturation = 1.20f,
            specular = 0.40f,
            shade = 0.18f,
            rimLight = Color.White,
            rimLightAlpha = 0.66f
        )
    }
}

/** What the device can actually do. */
enum class NebGlassTier { FULL, BLUR_ONLY, FLAT }

@Composable
fun rememberNebGlassTier(): NebGlassTier {
    val lowEnd = rememberIsLowEndDevice()
    return remember(lowEnd) {
        when {
            !NEB_LIQUID_GLASS || lowEnd -> NebGlassTier.FLAT
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU -> NebGlassTier.FULL
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> NebGlassTier.BLUR_ONLY
            else -> NebGlassTier.FLAT
        }
    }
}

/**
 * The page, recorded once per frame so the glass above it has something true
 * to sample. Held by whoever owns both the content and the glass — in this app,
 * the root Box in Navigation.
 */
@Stable
class NebGlassBackdrop internal constructor(internal val layer: GraphicsLayer) {
    /** Where the recorded content sits in the window, so glass can find itself. */
    internal var origin by mutableStateOf(Offset.Zero)
}

@Composable
fun rememberNebGlassBackdrop(): NebGlassBackdrop {
    val layer = rememberGraphicsLayer()
    return remember(layer) { NebGlassBackdrop(layer) }
}

/**
 * Put this on the content that should show through the glass. It draws exactly
 * as before; it just keeps a copy of itself on the way past.
 */
fun Modifier.nebGlassBackdrop(backdrop: NebGlassBackdrop): Modifier = this
    .onGloballyPositioned { backdrop.origin = it.positionInRoot() }
    .drawWithContent {
        backdrop.layer.record { this@drawWithContent.drawContent() }
        drawLayer(backdrop.layer)
    }

/**
 * Turn this element into a pane of glass over [backdrop].
 *
 * Draws behind the element's own content, so whatever is inside — icons,
 * labels — sits on the glass rather than under it.
 */
@Composable
fun Modifier.nebLiquidGlass(
    backdrop: NebGlassBackdrop,
    shape: Shape,
    style: NebGlassStyle,
    tier: NebGlassTier = rememberNebGlassTier()
): Modifier {
    // Remembered before the bail-out, not after: an early return that skips
    // remember calls moves every slot after it if the condition ever flips.
    val glassLayer = rememberGraphicsLayer()
    var position by remember { mutableStateOf(Offset.Zero) }

    if (tier == NebGlassTier.FLAT) return this

    return this
        .onGloballyPositioned { position = it.positionInRoot() }
        .drawBehind {
            if (size.width <= 0f || size.height <= 0f) return@drawBehind

            // The recorded slab is bigger than the element on every side. Blur
            // pulls in whatever is beyond the edge of its input, and the edge
            // of a slab cropped to the element is transparent — which would
            // ring the whole shape in a dark halo. The margin gives the blur
            // real pixels to reach for.
            val pad = (style.blur.toPx() * 2f).coerceAtLeast(8f)
            val layerSize = IntSize(
                (size.width + pad * 2f).roundToInt(),
                (size.height + pad * 2f).roundToInt()
            )
            val outline = shape.createOutline(size, layoutDirection, this)
            val clip = outline.asPath()

            glassLayer.renderEffect = when (tier) {
                NebGlassTier.FULL -> buildGlassEffect(
                    width = layerSize.width.toFloat(),
                    height = layerSize.height.toFloat(),
                    pad = pad,
                    corner = outline.cornerRadiusPx(size),
                    style = style,
                    density = this.density
                )
                else -> BlurEffect(
                    radiusX = style.blur.toPx(),
                    radiusY = style.blur.toPx(),
                    edgeTreatment = TileMode.Clamp
                )
            }

            val originX = position.x - backdrop.origin.x
            val originY = position.y - backdrop.origin.y
            glassLayer.record(layerSize) {
                translate(pad - originX, pad - originY) {
                    drawLayer(backdrop.layer)
                }
            }

            clipPath(clip) {
                translate(-pad, -pad) { drawLayer(glassLayer) }

                // The blur-only tier gets its tint and its lighting drawn,
                // since it has no shader to do either.
                if (tier == NebGlassTier.BLUR_ONLY) {
                    drawRect(color = style.tint.copy(alpha = style.tintAlpha))
                    drawRect(
                        brush = Brush.linearGradient(
                            colors = listOf(
                                Color.White.copy(alpha = style.specular * 0.5f),
                                Color.Transparent,
                                Color.Black.copy(alpha = style.shade * 0.4f)
                            ),
                            start = Offset(0f, 0f),
                            end = Offset(size.width, size.height)
                        )
                    )
                }
            }

            // The edge itself. A hairline that is bright where the light hits
            // and fades away from it — the one thing a blur can never give you,
            // and the difference between a pane of glass and a soft rectangle.
            drawPath(
                path = clip,
                brush = Brush.linearGradient(
                    colors = listOf(
                        style.rimLight.copy(alpha = style.rimLightAlpha),
                        style.rimLight.copy(alpha = style.rimLightAlpha * 0.12f),
                        style.rimLight.copy(alpha = style.rimLightAlpha * 0.45f)
                    ),
                    start = Offset(0f, 0f),
                    end = Offset(size.width * 0.6f, size.height)
                ),
                style = Stroke(width = 1f * density)
            )
        }
}

// ----------------------------------------------------------------- internals

private fun Outline.asPath(): Path = when (this) {
    is Outline.Generic -> path
    is Outline.Rounded -> Path().apply { addRoundRect(roundRect) }
    is Outline.Rectangle -> Path().apply { addRect(rect) }
}

/**
 * The corner radius the shader should assume. The SDF only knows rounded
 * rectangles, so a generic outline (the clover on the create button, say) is
 * approximated by its inscribed pill — the refraction is a few pixels off in
 * the scallops and nowhere else, and the real silhouette still comes from the
 * clip.
 */
private fun Outline.cornerRadiusPx(size: Size): Float = when (this) {
    is Outline.Rounded -> roundRect.topLeftCornerRadius.x
    is Outline.Rectangle -> 0f
    is Outline.Generic -> minOf(size.width, size.height) * 0.5f
}

/**
 * AGSL. Runs once per pixel of the glass, with the blurred backdrop bound to
 * `content`.
 *
 * The shape is described by a signed-distance function rather than passed in as
 * a mask, because refraction needs the *gradient* of the edge, not just its
 * position: the direction to pull the backdrop in from is the surface normal,
 * and the normal is the normalised gradient of the distance field.
 */
private const val NEB_GLASS_AGSL = """
uniform shader content;
uniform float2 uSize;
uniform float uPad;
uniform float uCorner;
uniform float uRim;
uniform float uRefract;
uniform float uDisperse;
uniform float4 uTint;
uniform float2 uLight;
uniform float uSpecular;
uniform float uShade;
uniform float uSaturation;

float sdRound(float2 p, float2 b, float r) {
    float2 q = abs(p) - b + float2(r, r);
    return min(max(q.x, q.y), 0.0) + length(max(q, float2(0.0, 0.0))) - r;
}

half4 main(float2 coord) {
    float2 half_size = uSize * 0.5;
    float2 b = half_size - float2(uPad, uPad);
    float r = min(uCorner, min(b.x, b.y));
    float2 p = coord - half_size;

    float d = sdRound(p, b, r);

    // Surface normal, by central difference on the distance field.
    float e = 1.0;
    float gx = sdRound(p + float2(e, 0.0), b, r) - sdRound(p - float2(e, 0.0), b, r);
    float gy = sdRound(p + float2(0.0, e), b, r) - sdRound(p - float2(0.0, e), b, r);
    float2 n = normalize(float2(gx, gy) + float2(0.00001, 0.00001));

    // 0 in the flat middle, 1 at the very edge. Cubed so the bend is a lip
    // rather than a dome -- glass is flat until it is not.
    float t = clamp(1.0 + d / max(uRim, 1.0), 0.0, 1.0);
    float bend = t * t * t;

    // Pull the backdrop inward along the normal: magnification at the rim.
    float2 off = n * (bend * uRefract);
    float4 col = float4(content.eval(coord - off));

    if (uDisperse > 0.0) {
        float4 warm = float4(content.eval(coord - off * (1.0 + uDisperse)));
        float4 cool = float4(content.eval(coord - off * (1.0 - uDisperse)));
        col = float4(warm.r, col.g, cool.b, col.a);
    }

    // Glass carries colour forward rather than washing it out.
    float lum = dot(col.rgb, float3(0.2126, 0.7152, 0.0722));
    col = float4(clamp(mix(float3(lum, lum, lum), col.rgb, uSaturation), 0.0, 1.0), col.a);

    col = float4(mix(col.rgb, uTint.rgb, uTint.a), col.a);

    // Lit rim and shaded rim. Together they are the thickness of the material.
    float2 light = normalize(uLight);
    float facing = clamp(dot(n, light), 0.0, 1.0);
    float spec = facing * facing * facing * bend * uSpecular;
    float away = clamp(-dot(n, light), 0.0, 1.0);
    float dark = away * away * bend * uShade;

    float3 lit = col.rgb * (1.0 - dark) + float3(spec, spec, spec);
    return half4(float4(clamp(lit, 0.0, 1.0), col.a));
}
"""

@RequiresApi(Build.VERSION_CODES.TIRAMISU)
private fun buildGlassEffect(
    width: Float,
    height: Float,
    pad: Float,
    corner: Float,
    style: NebGlassStyle,
    density: Float
): androidx.compose.ui.graphics.RenderEffect {
    val shader = RuntimeShader(NEB_GLASS_AGSL)
    shader.setFloatUniform("uSize", width, height)
    shader.setFloatUniform("uPad", pad)
    shader.setFloatUniform("uCorner", corner)
    shader.setFloatUniform("uRim", style.rim.value * density)
    shader.setFloatUniform("uRefract", style.refraction.value * density)
    shader.setFloatUniform("uDisperse", style.dispersion)
    shader.setFloatUniform(
        "uTint",
        style.tint.red, style.tint.green, style.tint.blue, style.tintAlpha
    )
    val radians = style.lightAngle * (Math.PI.toFloat() / 180f)
    shader.setFloatUniform("uLight", cos(radians), sin(radians))
    shader.setFloatUniform("uSpecular", style.specular)
    shader.setFloatUniform("uShade", style.shade)
    shader.setFloatUniform("uSaturation", style.saturation)

    val blurPx = style.blur.value * density
    val blur = android.graphics.RenderEffect.createBlurEffect(
        blurPx, blurPx, android.graphics.Shader.TileMode.CLAMP
    )
    val glass = android.graphics.RenderEffect.createRuntimeShaderEffect(shader, "content")
    // Inner first: blur the backdrop, then refract the blurred result.
    return android.graphics.RenderEffect.createChainEffect(glass, blur).asComposeRenderEffect()
}
