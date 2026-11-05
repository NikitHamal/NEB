@file:OptIn(ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.components

import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.MaterialShapes
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.toShape
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Shape

/**
 * One shape per person, everywhere: the web's `neb-shapes.js` hashes the username (FNV-1a) into
 * the same seven silhouettes and picks one of three tones from the next byte. This is the same
 * function, so a person who is a clover on the site is a clover on the phone.
 */
object AvatarShapes {
    private val shapes: List<Shape> by lazy {
        listOf(
            MaterialShapes.Cookie9Sided.toShape(),
            MaterialShapes.Sunny.toShape(),
            MaterialShapes.Flower.toShape(),
            MaterialShapes.Clover4Leaf.toShape(),
            MaterialShapes.SoftBurst.toShape(),
            MaterialShapes.Oval.toShape(),
            MaterialShapes.Square.toShape()
        )
    }

    private fun hash(seed: String): Long {
        var h = 2166136261L
        for (c in seed) {
            h = h xor c.code.toLong()
            h = (h * 16777619L) and 0xFFFFFFFFL
        }
        return h
    }

    fun shapeFor(seed: String): Shape {
        if (seed.isBlank()) return CircleShape
        return shapes[(hash(seed.trim().lowercase()) % shapes.size).toInt()]
    }

    fun toneFor(seed: String): Int {
        if (seed.isBlank()) return 0
        return ((hash(seed.trim().lowercase()) ushr 8) % 3).toInt()
    }
}

/** The person's avatar shape, remembered per seed. */
@Composable
fun rememberAvatarShape(seed: String): Shape = remember(seed) { AvatarShapes.shapeFor(seed) }

/** Fill and ink for an initial-only avatar: the web's three tonal pairs, chosen by the same hash. */
@Composable
fun avatarTone(seed: String): Pair<Color, Color> {
    val c = MaterialTheme.colorScheme
    return when (AvatarShapes.toneFor(seed)) {
        1 -> c.tertiaryContainer to c.onTertiaryContainer
        2 -> c.primaryContainer to c.onPrimaryContainer
        else -> c.secondaryContainer to c.onSecondaryContainer
    }
}
