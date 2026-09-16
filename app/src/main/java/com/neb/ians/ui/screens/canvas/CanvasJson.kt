package com.neb.ians.ui.screens.canvas

import androidx.compose.ui.graphics.Color
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonNull
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive

internal fun JsonElement?.asStr(): String {
    if (this == null || this is JsonNull) return ""
    return (this as? JsonPrimitive)?.content ?: ""
}

internal fun JsonObject.str(key: String): String = this[key].asStr()

internal fun JsonObject.bool(key: String): Boolean =
    this[key].asStr().toBooleanStrictOrNull() ?: false

internal fun JsonObject.num(key: String): Double =
    this[key].asStr().toDoubleOrNull() ?: 0.0

internal fun JsonObject.arr(key: String): JsonArray =
    (this[key] as? JsonArray) ?: JsonArray(emptyList())

internal fun JsonObject.obj(key: String): JsonObject? = this[key] as? JsonObject

internal fun String.toComposeColor(fallback: Color): Color = try {
    val hex = trim().removePrefix("#")
    when (hex.length) {
        6 -> Color((0xFF000000L or hex.toLong(16)).toULong())
        8 -> Color(hex.toLong(16).toULong())
        else -> fallback
    }
} catch (_: Exception) { fallback }

internal fun canvasKindColor(kind: String, primary: Color): Color = when (kind) {
    "note" -> Color(0xFFD97706)
    "source" -> Color(0xFF0F9F78)
    "question" -> Color(0xFF7C3AED)
    "practice" -> Color(0xFFDB2777)
    "comparison" -> Color(0xFFE11D48)
    "summary" -> Color(0xFF2563EB)
    else -> primary
}

internal fun canvasMetaColor(meta: JsonObject?, primary: Color): Color {
    val color = meta?.str("color") ?: "default"
    if (color == "default" || color.isBlank()) return Color.Unspecified
    return when (color) {
        "blue" -> Color(0xFF2563EB)
        "green" -> Color(0xFF16A34A)
        "amber" -> Color(0xFFD97706)
        "rose" -> Color(0xFFE11D48)
        "purple" -> Color(0xFF7C3AED)
        "slate" -> Color(0xFF64748B)
        else -> primary
    }
}

internal fun canvasToneColor(tone: String): Color = when (tone) {
    "green" -> Color(0xFF16A34A)
    "amber" -> Color(0xFFD97706)
    "rose" -> Color(0xFFE11D48)
    "slate" -> Color(0xFF64748B)
    else -> Color(0xFF2563EB)
}
