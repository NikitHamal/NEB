package com.neb.ians.data.api

import kotlinx.serialization.KSerializer
import kotlinx.serialization.descriptors.PrimitiveKind
import kotlinx.serialization.descriptors.PrimitiveSerialDescriptor
import kotlinx.serialization.descriptors.SerialDescriptor
import kotlinx.serialization.encoding.Decoder
import kotlinx.serialization.encoding.Encoder
import kotlinx.serialization.json.JsonDecoder
import kotlinx.serialization.json.JsonNull
import kotlinx.serialization.json.JsonPrimitive

/**
 * Reads a `String` field that the server sometimes sends unquoted.
 *
 * The two resource serialisers on the backend disagree: `api/serializers.py`
 * formats `price` as a string (`"150"`), while `web/view_helpers.py` hands
 * back the raw `float` (`150.0`). Strict JSON decoding throws on the second
 * shape, and because the whole response is decoded in one pass a single
 * unquoted number empties an entire list — that is what made the profile
 * Resources tab read "No activity yet" for everyone.
 *
 * `coerceInputValues` does not help: it rescues `null`, not a type mismatch.
 * So take whatever primitive arrives and render it as text; `null` and any
 * non-primitive become "", which is what the defaults already meant.
 */
object LenientStringSerializer : KSerializer<String> {

    override val descriptor: SerialDescriptor =
        PrimitiveSerialDescriptor("com.neb.ians.LenientString", PrimitiveKind.STRING)

    override fun deserialize(decoder: Decoder): String {
        val jsonDecoder = decoder as? JsonDecoder ?: return decoder.decodeString()
        return when (val element = jsonDecoder.decodeJsonElement()) {
            is JsonNull -> ""
            is JsonPrimitive -> element.content.let { raw ->
                // 150.0 and 150 mean the same price; keep the shorter form so
                // "Rs. $price" never reads "Rs. 150.0".
                if (!element.isString) raw.removeSuffix(".0") else raw
            }
            else -> ""
        }
    }

    override fun serialize(encoder: Encoder, value: String) {
        encoder.encodeString(value)
    }
}
