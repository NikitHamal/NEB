package com.neb.ians.data.api

import kotlinx.serialization.KSerializer
import kotlinx.serialization.descriptors.PrimitiveKind
import kotlinx.serialization.descriptors.PrimitiveSerialDescriptor
import kotlinx.serialization.encoding.Decoder
import kotlinx.serialization.encoding.Encoder

private val ENTITY = Regex("&(amp|lt|gt|quot|apos|nbsp|#39|#x27|#34);")

/** Server text can arrive HTML escaped ("Tihar &amp; Puja"). Decode it once, when it is read. */
fun String.decodeEntities(): String {
    if (indexOf('&') < 0) return this
    return ENTITY.replace(this) {
        when (it.groupValues[1]) {
            "amp" -> "&"
            "lt" -> "<"
            "gt" -> ">"
            "quot", "#34" -> "\""
            "apos", "#39", "#x27" -> "'"
            else -> " "
        }
    }
}

object EntityString : KSerializer<String> {
    override val descriptor = PrimitiveSerialDescriptor("EntityString", PrimitiveKind.STRING)
    override fun deserialize(decoder: Decoder): String = decoder.decodeString().decodeEntities()
    override fun serialize(encoder: Encoder, value: String) = encoder.encodeString(value)
}
