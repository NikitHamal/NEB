package com.neb.ians.pdf

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Typeface
import android.graphics.pdf.PdfDocument
import com.neb.ians.data.LearningResource
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.io.FileOutputStream

object PdfCacheRepository {
    suspend fun ensurePdf(context: Context, resource: LearningResource): File = withContext(Dispatchers.IO) {
        val directory = File(context.applicationContext.filesDir, "pdf_cache").apply { mkdirs() }
        val file = File(directory, "${resource.id}.pdf")
        if (!file.exists() || file.length() == 0L) {
            generatePdf(file, resource)
        }
        file
    }

    private fun generatePdf(file: File, resource: LearningResource) {
        val document = PdfDocument()
        val titlePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = Color.rgb(25, 72, 66)
            textSize = 28f
            typeface = Typeface.create(Typeface.SANS_SERIF, Typeface.BOLD)
        }
        val metaPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = Color.rgb(91, 99, 94)
            textSize = 13f
            typeface = Typeface.create(Typeface.SANS_SERIF, Typeface.NORMAL)
        }
        val bodyPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = Color.rgb(30, 35, 32)
            textSize = 16f
            typeface = Typeface.create(Typeface.SANS_SERIF, Typeface.NORMAL)
        }
        val sectionPaint = Paint(titlePaint).apply { textSize = 22f }
        val chipPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = Color.rgb(226, 238, 233)
            style = Paint.Style.FILL
        }
        val accentPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = Color.rgb(36, 84, 77)
            strokeWidth = 3f
        }

        repeat(resource.pages) { page ->
            val pageInfo = PdfDocument.PageInfo.Builder(PAGE_WIDTH, PAGE_HEIGHT, page + 1).create()
            val pdfPage = document.startPage(pageInfo)
            val canvas = pdfPage.canvas
            canvas.drawColor(Color.rgb(250, 252, 248))
            canvas.drawRoundRect(44f, 48f, 551f, 120f, 18f, 18f, chipPaint)
            canvas.drawText(resource.title, 62f, 86f, titlePaint)
            canvas.drawText("${resource.grade.label} • ${resource.subject.label} • ${resource.type.label}", 62f, 108f, metaPaint)
            canvas.drawLine(62f, 148f, 533f, 148f, accentPaint)

            val heading = when (page) {
                0 -> "Overview"
                1 -> "Key ideas"
                2 -> "Important questions"
                3 -> "Exam strategy"
                else -> "Practice section ${page + 1}"
            }
            canvas.drawText(heading, 62f, 188f, sectionPaint)

            val paragraphs = listOf(
                resource.summary,
                "This offline copy is generated and cached locally by NEBians. Open it once and the file remains available for reading without network access.",
                "Use highlight for definitions, underline for formulas or dates, and sticky notes for personal reminders. All annotations stay linked to this PDF file on your device.",
                "Suggested focus: ${resource.tags.joinToString(", ")}. Revise in short sessions, then test yourself using board-style questions."
            )
            var y = 228f
            paragraphs.forEach { paragraph ->
                y = canvas.drawWrappedText(paragraph, 62f, y, 470f, bodyPaint, 8f) + 18f
            }
            canvas.drawText("Page ${page + 1} of ${resource.pages}", 452f, 800f, metaPaint)
            document.finishPage(pdfPage)
        }

        FileOutputStream(file).use { output -> document.writeTo(output) }
        document.close()
    }

    private fun Canvas.drawWrappedText(text: String, x: Float, y: Float, width: Float, paint: Paint, lineSpacing: Float): Float {
        val words = text.split(" ")
        val line = StringBuilder()
        var currentY = y
        for (word in words) {
            val candidate = if (line.isEmpty()) word else "$line $word"
            if (paint.measureText(candidate) > width) {
                drawText(line.toString(), x, currentY, paint)
                line.clear()
                line.append(word)
                currentY += paint.textSize + lineSpacing
            } else {
                line.clear()
                line.append(candidate)
            }
        }
        if (line.isNotEmpty()) {
            drawText(line.toString(), x, currentY, paint)
        }
        return currentY + paint.textSize + lineSpacing
    }

    private const val PAGE_WIDTH = 595
    private const val PAGE_HEIGHT = 842
}
