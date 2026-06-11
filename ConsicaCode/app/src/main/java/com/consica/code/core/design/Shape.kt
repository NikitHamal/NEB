package com.consica.code.core.design

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Shapes
import androidx.compose.ui.unit.dp

/** Eco-Logic shapes: generous radii, 24dp cards, pill buttons. */
val EcoShapes = Shapes(
    extraSmall = RoundedCornerShape(8.dp),
    small = RoundedCornerShape(12.dp),
    medium = RoundedCornerShape(18.dp),
    large = RoundedCornerShape(24.dp),
    extraLarge = RoundedCornerShape(32.dp),
)

val PillShape = RoundedCornerShape(percent = 50)
val CardShape = RoundedCornerShape(24.dp)
val SheetShape = RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp)
