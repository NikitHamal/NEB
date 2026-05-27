package com.neb.ians.pdf

enum class AnnotationType {
    Highlight,
    Underline,
    StickyNote
}

data class PdfAnnotation(
    val id: String,
    val resourceId: String,
    val pageIndex: Int,
    val type: AnnotationType,
    val startX: Float,
    val startY: Float,
    val endX: Float,
    val endY: Float,
    val note: String,
    val createdAt: Long
)
