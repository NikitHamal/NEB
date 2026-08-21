package com.neb.ians.ui.avatar.blobatar

data class PoseParams(
    val esx: Double = 1.0, val esy: Double = 1.0, val tilt: Double = 0.0,
    val edy: Double = 0.0, val edx: Double = 0.0,
    val esx2: Double = 0.0, val esy2: Double = 0.0, val tilt2: Double = 0.0, val edy2: Double = 0.0,
    val lock: Double = 0.0, val heat: Double = 0.0, val bdy: Double = 0.0
)

data class BakedLayout(val eyes: List<EyeDef>, val bodyTranslateY: Double)

fun bakePose(layout: BlobLayout, p: PoseParams): BakedLayout {
    val eyes = layout.eyes.mapIndexed { i, e ->
        e.copy(
            n = e.n,
            cx = e.cx + p.edx * (if (i == 1) 1 else -1),
            cy = e.cy + p.edy + (if (i == 1) p.edy2 else 0.0),
            rx = e.rx * (p.esx + (if (i == 1) p.esx2 else 0.0)),
            ry = e.ry * (p.esy + (if (i == 1) p.esy2 else 0.0)),
            rot = e.rot * (1 - p.lock) + (p.tilt + (if (i == 1) p.tilt2 else 0.0)) * (if (i == 1) 1 else -1)
        )
    }
    return BakedLayout(eyes, p.bdy)
}

private fun mkPose(p: PoseParams, tint: Any? = null): Pair<PoseParams, String?> {
    val tintName = when (tint) {
        is String -> tint
        else -> null
    }
    return p to tintName
}

val IDENT = PoseParams()

val EXPRESSIONS: Map<String, Pair<PoseParams, String?>> = mapOf(
    "idle" to (IDENT to null),
    "happy" to (PoseParams(1.72, 0.3, 8.0, -1.5, 1.5, 0.08, 0.05, -16.0, 0.0, 1.0, 0.0, -2.2) to null),
    "sad" to (PoseParams(0.6, 0.56, 26.0, 3.6, 1.9, -0.05, -0.07, -7.0, 0.0, 1.0, 0.0, 2.6) to null),
    "mad" to (PoseParams(1.85, 0.26, -33.0, 0.4, 0.6, 0.0, -0.03, 5.0, 0.0, 1.0, 0.62, 0.8) to "hot"),
    "surprised" to (PoseParams(1.34, 1.2, -6.0, -1.05, 0.5, 0.05, 0.07, 3.0, 0.0, 1.0, 0.0, -1.4) to null),
    "wink" to (PoseParams(1.32, 0.76, 5.0, -0.6, 0.8, 0.26, -0.56, -11.0, 0.0, 1.0, 0.0, -1.1) to null),
    "sleepy" to (PoseParams(1.14, 0.22, 0.0, 2.4, 0.3, -0.04, 0.03, 4.0, 0.0, 1.0, 0.0, 1.2) to null),
    "smug" to (PoseParams(1.3, 0.42, 18.0, -0.5, 0.5, 0.06, -0.06, -36.0, 0.0, 1.0, 0.0, -1.0) to null),
    "unsure" to (PoseParams(0.95, 1.02, 4.0, -0.2, 0.3, 0.24, -0.44, -18.0, 0.0, 1.0, 0.0, 0.0) to null),
    "scared" to (PoseParams(0.78, 0.96, -12.0, -1.5, -0.8, -0.04, 0.05, 4.0, 0.0, 1.0, 0.0, -0.6) to null),
    "love" to (PoseParams(0.86, 1.28, -14.0, -0.5, -0.35, 0.05, 0.06, 6.0, 0.0, 1.0, 0.6, -1.6) to "rose"),
    "shy" to (PoseParams(0.62, 0.5, 10.0, 1.4, -0.2, -0.05, -0.04, -8.0, 0.0, 1.0, 0.55, 0.9) to "blush"),
    "sick" to (PoseParams(1.25, 0.34, 20.0, 1.8, 0.8, 0.05, -0.05, -6.0, 0.0, 1.0, 0.6, 1.4) to "bile"),
    "thinking" to (PoseParams(1.15, 0.62, 0.0, 4.2, 0.4, 0.02, 0.06, 0.0, -8.4, 1.0, 0.0, -0.4) to null)
)

fun tintNameFor(expression: String): String? = EXPRESSIONS[expression]?.second
fun poseFor(expression: String): PoseParams = EXPRESSIONS[expression]?.first ?: IDENT
