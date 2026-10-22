package com.neb.ians.ui.components

import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.OffsetMapping
import androidx.compose.ui.text.input.TransformedText
import androidx.compose.ui.text.input.VisualTransformation

private val MentionRegex = Regex("@[a-zA-Z0-9_.-]+")

/**
 * Highlights @mentions as they are typed. A data class, so the text field sees an equal
 * transformation on recomposition and does not re-run [filter] for it.
 */
data class MentionsVisualTransformation(private val highlightColor: Color) : VisualTransformation {
    override fun filter(text: AnnotatedString): TransformedText {
        val annotated = buildAnnotatedString {
            val raw = text.text
            append(raw)
            MentionRegex.findAll(raw).forEach { match ->
                addStyle(
                    style = SpanStyle(
                        color = highlightColor,
                        fontWeight = FontWeight.Bold
                    ),
                    start = match.range.first,
                    end = match.range.last + 1
                )
            }
        }
        return TransformedText(annotated, OffsetMapping.Identity)
    }
}
