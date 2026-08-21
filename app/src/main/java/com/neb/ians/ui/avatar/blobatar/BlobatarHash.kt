package com.neb.ians.ui.avatar.blobatar

import java.text.Normalizer

private const val MASK32 = 0xFFFFFFFFu
private const val SEP: Byte = 0xFF.toByte()

private fun imul(a: UInt, b: UInt): UInt = a * b

private fun feed(h: UInt, data: ByteArray): UInt {
    var hh = h
    for (b in data) {
        val bv = (b.toInt() and 0xFF).toUInt()
        hh = imul(hh xor bv, 3432918353u)
        hh = (hh shl 13) or (hh shr 19)
    }
    return hh
}

private fun finalizeHash(h: UInt): UInt {
    var hh = imul(h xor (h shr 16), 2246822507u)
    hh = imul(hh xor (hh shr 13), 3266489909u)
    return hh xor (hh shr 16)
}

private fun normalizeSeed(seed: String): String =
    Normalizer.normalize(seed, Normalizer.Form.NFC).trim().lowercase()

fun seedState(seed: String, normalize: Boolean = true): UInt {
    val s = if (normalize) normalizeSeed(seed) else seed
    val utf8 = s.toByteArray(Charsets.UTF_8)
    return feed(1779033703u xor s.length.toUInt(), utf8)
}

fun stream(state: UInt, key: String): Double {
    val sepBytes = byteArrayOf(SEP)
    val afterSep = feed(state, sepBytes)
    val afterKey = feed(afterSep, key.toByteArray(Charsets.UTF_8))
    val fin = finalizeHash(afterKey)
    return fin.toDouble() / 4294967296.0
}

class Traits(
    seed: String,
    normalize: Boolean = true,
    private val overrides: Map<String, Any?> = emptyMap()
) {
    private val state: UInt = seedState(seed, normalize)

    operator fun invoke(key: String): Double {
        val v = overrides[key]
        val o: Double? = when {
            v is List<*> && v.isNotEmpty() -> {
                val idx = (stream(state, key) * v.size).toInt().coerceIn(0, v.size - 1)
                (v[idx] as? Number)?.toDouble()
            }
            v is Number -> v.toDouble()
            else -> null
        }
        if (o == null) return stream(state, key)
        if (o > 0) return if (o < 1) o else 0.999999
        return 0.0
    }

    fun num(key: String, minimum: Double, maximum: Double): Double =
        minimum + invoke(key) * (maximum - minimum)

    fun int(key: String, minimum: Int, maximum: Int): Int =
        minimum + (invoke(key) * (maximum - minimum + 1)).toInt()

    fun pick(key: String, options: List<String>): String =
        options[(invoke(key) * options.size).toInt().coerceIn(0, options.size - 1)]

    fun bool(key: String, p: Double = 0.5): Boolean = invoke(key) < p

    fun jitter(key: String, amount: Double): Double = (invoke(key) * 2 - 1) * amount
}

fun traits(seed: String, normalize: Boolean = true, overrides: Map<String, Any?>? = null): Traits =
    Traits(seed, normalize, overrides ?: emptyMap())
