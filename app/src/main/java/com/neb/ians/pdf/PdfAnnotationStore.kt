package com.neb.ians.pdf

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.util.UUID

class PdfAnnotationStore(context: Context) {
    private val directory = File(context.applicationContext.filesDir, "pdf_annotations").apply { mkdirs() }

    fun load(resourceId: String): List<PdfAnnotation> {
        val file = fileFor(resourceId)
        if (!file.exists()) return emptyList()
        val array = JSONArray(file.readText())
        return buildList {
            for (index in 0 until array.length()) {
                val item = array.getJSONObject(index)
                add(
                    PdfAnnotation(
                        id = item.getString("id"),
                        resourceId = item.getString("resourceId"),
                        pageIndex = item.getInt("pageIndex"),
                        type = AnnotationType.valueOf(item.getString("type")),
                        startX = item.getDouble("startX").toFloat(),
                        startY = item.getDouble("startY").toFloat(),
                        endX = item.getDouble("endX").toFloat(),
                        endY = item.getDouble("endY").toFloat(),
                        note = item.optString("note"),
                        createdAt = item.optLong("createdAt")
                    )
                )
            }
        }
    }

    fun add(
        resourceId: String,
        pageIndex: Int,
        type: AnnotationType,
        startX: Float,
        startY: Float,
        endX: Float,
        endY: Float,
        note: String = ""
    ): List<PdfAnnotation> {
        val annotation = PdfAnnotation(
            id = UUID.randomUUID().toString(),
            resourceId = resourceId,
            pageIndex = pageIndex,
            type = type,
            startX = startX.coerceIn(0f, 1f),
            startY = startY.coerceIn(0f, 1f),
            endX = endX.coerceIn(0f, 1f),
            endY = endY.coerceIn(0f, 1f),
            note = note,
            createdAt = System.currentTimeMillis()
        )
        val updated = load(resourceId) + annotation
        save(resourceId, updated)
        return updated
    }

    fun clearPage(resourceId: String, pageIndex: Int): List<PdfAnnotation> {
        val updated = load(resourceId).filterNot { it.pageIndex == pageIndex }
        save(resourceId, updated)
        return updated
    }

    private fun save(resourceId: String, annotations: List<PdfAnnotation>) {
        val array = JSONArray()
        annotations.forEach { item ->
            array.put(
                JSONObject()
                    .put("id", item.id)
                    .put("resourceId", item.resourceId)
                    .put("pageIndex", item.pageIndex)
                    .put("type", item.type.name)
                    .put("startX", item.startX)
                    .put("startY", item.startY)
                    .put("endX", item.endX)
                    .put("endY", item.endY)
                    .put("note", item.note)
                    .put("createdAt", item.createdAt)
            )
        }
        fileFor(resourceId).writeText(array.toString())
    }

    private fun fileFor(resourceId: String): File {
        val safeId = resourceId.replace(Regex("[^A-Za-z0-9_-]"), "_")
        return File(directory, "$safeId.json")
    }
}
