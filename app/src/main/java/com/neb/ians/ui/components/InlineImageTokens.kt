package com.neb.ians.ui.components

import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.input.OffsetMapping
import androidx.compose.ui.text.input.TransformedText
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.graphics.Color
import kotlin.random.Random

/**
 * Inline text-image tokens (`[[img:ID]]`) shared by the composer and every
 * content renderer. Mirrors `api/content_images.py` on the server:
 * real uploads carry a numeric id; in-flight uploads carry a temporary
 * `uXXXXXXXX` key that is swapped for the numeric id once the upload lands.
 */
object InlineImageTokens {

    const val MAX_IMAGES_PER_CONTENT = 8

    /** Numeric ids = uploaded; `u`-prefixed keys = pending upload. */
    val REGEX = Regex("\\[\\[img:(\\d{1,10}|u[A-Za-z0-9]{6,16})\\]\\]")

    /** Private Use Area char each token collapses to inside the editor. */
    const val PLACEHOLDER_CHAR = '\uE107'
    const val PLACEHOLDER_LEN = 4
    val PLACEHOLDER: String = PLACEHOLDER_CHAR.toString().repeat(PLACEHOLDER_LEN)

    fun newPendingKey(): String = "u" + Random.nextInt(0x1000000, 0xFFFFFFF).toString(16)

    fun pendingToken(key: String): String = "[[img:$key]]"

    fun tokenFor(id: Int): String = "[[img:$id]]"

    /** Ordered unique numeric image ids referenced by the text. */
    fun extractIds(text: String): List<Int> {
        val seen = linkedSetOf<Int>()
        REGEX.findAll(text).forEach { m ->
            m.groupValues[1].toIntOrNull()?.let { seen.add(it) }
        }
        return seen.toList()
    }

    fun countTokens(text: String): Int = REGEX.findAll(text).count()

    fun hasPending(text: String): Boolean =
        REGEX.findAll(text).any { it.groupValues[1].startsWith("u") }

    /** Replace tokens with a plain-text placeholder (previews, share sheets). */
    fun plainText(text: String, placeholder: String = "[image]"): String =
        REGEX.replace(text, placeholder)

    fun stripTokens(text: String): String = REGEX.replace(text, "")

    fun replacePendingKey(text: String, key: String, id: Int): String =
        text.replace("[[img:$key]]", tokenFor(id))

    fun removeToken(text: String, token: String): String = text.replace(token, "")
}

/**
 * Visual transformation that collapses every `[[img:…]]` token into ONE
 * private-use character so Backspace deletes the whole chip at once and the
 * caret can never sit between the token's characters — matching the web
 * contenteditable chip behaviour.
 *
 * The placeholder glyph itself is painted fully transparent; visible
 * thumbnails are drawn by [InlineImageField]'s overlay positioned via the
 * transformed layout's bounding boxes.
 */
class InlineImageVisualTransformation : VisualTransformation {

    data class Mapping(
        val transformed: TransformedText,
        /** Transformed-string index of each placeholder char, in token order. */
        val placeholderIndices: List<Int>,
        /** Original-string ranges of each token, aligned with [placeholderIndices]. */
        val tokenRanges: List<IntRange>
    )

    fun map(raw: String): Mapping {
        val matches = InlineImageTokens.REGEX.findAll(raw).toList()
        if (matches.isEmpty()) {
            return Mapping(
                TransformedText(AnnotatedString(raw), OffsetMapping.Identity),
                emptyList(),
                emptyList()
            )
        }

        val ranges = matches.map { it.range.first..it.range.last }
        val transparent = SpanStyle(color = Color.Transparent)

        val pieces = mutableListOf<Pair<String, Boolean>>() // text to isToken
        var cursor = 0
        ranges.forEach { r ->
            if (r.first > cursor) pieces.add(raw.substring(cursor, r.first) to false)
            pieces.add(raw.substring(r.first, r.last + 1) to true)
            cursor = r.last + 1
        }
        if (cursor < raw.length) pieces.add(raw.substring(cursor) to false)

        val annotated = buildAnnotatedString {
            pieces.forEach { (segment, isToken) ->
                if (isToken) {
                    pushStyle(transparent)
                    append(InlineImageTokens.PLACEHOLDER)
                    pop()
                } else {
                    append(segment)
                }
            }
        }

        // ---- Offset mappings -------------------------------------------------
        val origToTrans = IntArray(raw.length + 1)
        val transToOrig = IntArray(annotated.length + 1)
        val placeholders = mutableListOf<Int>()

        var o = 0
        var t = 0
        pieces.forEach { (segment, isToken) ->
            if (isToken) {
                val startO = o
                val endO = o + segment.length
                placeholders.add(t)
                origToTrans[startO] = t
                for (i in startO until endO) origToTrans[i] = t
                origToTrans[endO] = t + InlineImageTokens.PLACEHOLDER_LEN
                repeat(InlineImageTokens.PLACEHOLDER_LEN) { k ->
                    transToOrig[t + k] = startO
                }
                transToOrig[t + InlineImageTokens.PLACEHOLDER_LEN] = endO
                o = endO
                t += InlineImageTokens.PLACEHOLDER_LEN
            } else {
                repeat(segment.length) { k ->
                    origToTrans[o] = t
                    transToOrig[t] = o
                    o += 1
                    t += 1
                }
                origToTrans[o] = t
                transToOrig[t] = o
            }
        }

        val offsetMapping = object : OffsetMapping {
            override fun originalToTransformed(offset: Int): Int =
                origToTrans[offset.coerceIn(0, raw.length)]

            override fun transformedToOriginal(offset: Int): Int =
                transToOrig[offset.coerceIn(0, annotated.length)]
        }

        return Mapping(
            TransformedText(annotated, offsetMapping),
            placeholders.toList(),
            ranges
        )
    }

    override fun filter(text: AnnotatedString): TransformedText = map(text.text).transformed
}
