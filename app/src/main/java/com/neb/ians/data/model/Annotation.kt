package com.neb.ians.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "annotations")
data class PdfAnnotation(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val pdfUri: String,         // identifier for the PDF file
    val pageIndex: Int,
    val x: Float,               // normalized 0..1
    val y: Float,               // normalized 0..1
    val width: Float,           // normalized 0..1
    val height: Float,          // normalized 0..1
    val type: AnnotationType,   // HIGHLIGHT, UNDERLINE, STICKY_NOTE
    val color: Int,             // ARGB color
    val noteText: String? = null,
    val createdAt: Long = System.currentTimeMillis()
)

enum class AnnotationType {
    HIGHLIGHT,
    UNDERLINE,
    STICKY_NOTE
}
