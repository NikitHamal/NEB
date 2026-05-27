package com.neb.ians

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.pdf.PdfDocument
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.net.HttpURLConnection
import java.net.URL
import java.util.UUID
import java.util.concurrent.ConcurrentHashMap
import kotlin.math.max

private val Context.settingsDataStore by preferencesDataStore(name = "neb_settings")

class SettingsRepository(private val context: Context) {
    private val darkModeKey = booleanPreferencesKey("dark_mode")

    val darkMode: Flow<Boolean> = context.settingsDataStore.data.map { preferences ->
        preferences[darkModeKey] ?: false
    }

    suspend fun setDarkMode(enabled: Boolean) {
        context.settingsDataStore.edit { preferences ->
            preferences[darkModeKey] = enabled
        }
    }
}

class ResourceCacheManager(private val context: Context) {
    private val pdfCacheDir = File(context.filesDir, "pdf_cache").apply { mkdirs() }

    fun cachedFileFor(resource: LearningResource): File = File(pdfCacheDir, resource.localFileName)

    fun isCached(resource: LearningResource): Boolean = cachedFileFor(resource).exists()

    suspend fun getOrCreatePdf(resource: LearningResource): File = withContext(Dispatchers.IO) {
        val target = cachedFileFor(resource)
        if (target.exists() && target.length() > 0L) return@withContext target

        val downloaded = resource.remoteUrl?.let { downloadToFile(it, target) } ?: false
        if (!downloaded) {
            SamplePdfFactory.create(resource, target)
        }
        target
    }

    suspend fun cacheSizeBytes(): Long = withContext(Dispatchers.IO) {
        pdfCacheDir.walkTopDown()
            .filter { it.isFile }
            .sumOf { it.length() }
    }

    suspend fun clearCache() = withContext(Dispatchers.IO) {
        pdfCacheDir.listFiles()?.forEach { it.deleteRecursively() }
    }

    private fun downloadToFile(url: String, target: File): Boolean {
        return runCatching {
            val connection = URL(url).openConnection() as HttpURLConnection
            connection.connectTimeout = 12_000
            connection.readTimeout = 20_000
            connection.instanceFollowRedirects = true
            connection.inputStream.use { input ->
                target.outputStream().use { output -> input.copyTo(output) }
            }
            connection.disconnect()
            target.length() > 0L
        }.getOrDefault(false)
    }
}

object SamplePdfFactory {
    fun create(resource: LearningResource, target: File) {
        target.parentFile?.mkdirs()
        val document = PdfDocument()
        val pages = listOf(
            listOf(
                resource.title,
                "${resource.grade.label} - ${resource.subject.label} - ${resource.type.label}",
                resource.description,
                "Key focus:",
                "- Read definitions first, then solve worked examples.",
                "- Mark confusing lines with sticky notes inside NEBians.",
                "- Revisit highlighted sections before weekly revision."
            ),
            listOf(
                "Practice Plan",
                "1. Review the formula or concept summary.",
                "2. Solve two board-style questions without checking hints.",
                "3. Compare your answer with class notes.",
                "4. Underline steps that are easy to forget.",
                "5. Add a sticky note for teacher questions."
            ),
            listOf(
                "NEB Exam Checklist",
                "- Keep units clear in every numerical answer.",
                "- Draw diagrams cleanly and label axes.",
                "- Use short definitions for theory answers.",
                "- Save important annotations for offline revision."
            )
        )

        pages.forEachIndexed { index, lines ->
            val pageInfo = PdfDocument.PageInfo.Builder(595, 842, index + 1).create()
            val page = document.startPage(pageInfo)
            drawPage(page.canvas, lines, index + 1)
            document.finishPage(page)
        }

        target.outputStream().use { document.writeTo(it) }
        document.close()
    }

    private fun drawPage(canvas: Canvas, lines: List<String>, pageNumber: Int) {
        val titlePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = android.graphics.Color.rgb(14, 93, 78)
            textSize = 28f
            isFakeBoldText = true
        }
        val bodyPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = android.graphics.Color.rgb(31, 35, 32)
            textSize = 16f
        }
        val mutedPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = android.graphics.Color.rgb(100, 108, 101)
            textSize = 12f
        }

        canvas.drawColor(android.graphics.Color.rgb(251, 253, 249))
        canvas.drawText("NEBians", 48f, 54f, mutedPaint)
        canvas.drawLine(48f, 74f, 547f, 74f, mutedPaint)

        var y = 126f
        lines.forEachIndexed { index, line ->
            val paint = if (index == 0) titlePaint else bodyPaint
            val wrapped = wrap(line, paint, 495f)
            wrapped.forEach { segment ->
                canvas.drawText(segment, 48f, y, paint)
                y += if (index == 0) 36f else 26f
            }
            y += if (index == 0) 20f else 10f
        }

        canvas.drawText("Page $pageNumber", 492f, 800f, mutedPaint)
    }

    private fun wrap(text: String, paint: Paint, maxWidth: Float): List<String> {
        if (paint.measureText(text) <= maxWidth) return listOf(text)
        val words = text.split(" ")
        val lines = mutableListOf<String>()
        var current = ""
        words.forEach { word ->
            val candidate = if (current.isBlank()) word else "$current $word"
            if (paint.measureText(candidate) <= maxWidth) {
                current = candidate
            } else {
                if (current.isNotBlank()) lines += current
                current = word
            }
        }
        if (current.isNotBlank()) lines += current
        return lines
    }
}

class AnnotationStore(private val context: Context) {
    private val annotationsDir = File(context.filesDir, "annotations").apply { mkdirs() }
    private val flows = ConcurrentHashMap<String, MutableStateFlow<List<PdfAnnotation>>>()

    fun observe(pdfId: String): StateFlow<List<PdfAnnotation>> {
        return flows.getOrPut(pdfId) { MutableStateFlow(readAnnotations(pdfId)) }
    }

    suspend fun add(annotation: PdfAnnotation) = withContext(Dispatchers.IO) {
        val flow = flows.getOrPut(annotation.pdfId) { MutableStateFlow(readAnnotations(annotation.pdfId)) }
        val next = (flow.value + annotation).sortedWith(compareBy({ it.pageIndex }, { it.createdAt }))
        writeAnnotations(annotation.pdfId, next)
        flow.value = next
    }

    suspend fun clear(pdfId: String) = withContext(Dispatchers.IO) {
        val flow = flows.getOrPut(pdfId) { MutableStateFlow(emptyList()) }
        writeAnnotations(pdfId, emptyList())
        flow.value = emptyList()
    }

    suspend fun remove(pdfId: String, annotationId: String) = withContext(Dispatchers.IO) {
        val flow = flows.getOrPut(pdfId) { MutableStateFlow(readAnnotations(pdfId)) }
        val next = flow.value.filterNot { it.id == annotationId }
        writeAnnotations(pdfId, next)
        flow.value = next
    }

    private fun fileFor(pdfId: String) = File(annotationsDir, "$pdfId.json")

    private fun readAnnotations(pdfId: String): List<PdfAnnotation> {
        val file = fileFor(pdfId)
        if (!file.exists()) return emptyList()
        return runCatching {
            val array = JSONArray(file.readText())
            List(array.length()) { index ->
                val item = array.getJSONObject(index)
                PdfAnnotation(
                    id = item.getString("id"),
                    pdfId = item.getString("pdfId"),
                    pageIndex = item.getInt("pageIndex"),
                    kind = AnnotationKind.valueOf(item.getString("kind")),
                    x = item.getDouble("x").toFloat(),
                    y = item.getDouble("y").toFloat(),
                    width = item.getDouble("width").toFloat(),
                    height = item.getDouble("height").toFloat(),
                    note = item.optString("note"),
                    color = item.getInt("color"),
                    createdAt = item.getLong("createdAt")
                )
            }
        }.getOrDefault(emptyList())
    }

    private fun writeAnnotations(pdfId: String, annotations: List<PdfAnnotation>) {
        val array = JSONArray()
        annotations.forEach { annotation ->
            array.put(
                JSONObject()
                    .put("id", annotation.id)
                    .put("pdfId", annotation.pdfId)
                    .put("pageIndex", annotation.pageIndex)
                    .put("kind", annotation.kind.name)
                    .put("x", annotation.x)
                    .put("y", annotation.y)
                    .put("width", annotation.width)
                    .put("height", annotation.height)
                    .put("note", annotation.note)
                    .put("color", annotation.color)
                    .put("createdAt", annotation.createdAt)
            )
        }
        fileFor(pdfId).writeText(array.toString())
    }
}

object ForumRepository {
    private val _threads = MutableStateFlow(
        listOf(
            ForumThread(
                id = "thread-physics-vectors",
                subject = Subject.Physics,
                grade = GradeLevel.Grade12,
                title = "How do I resolve vectors faster in exams?",
                body = "I understand components, but I lose time choosing signs in board questions.",
                author = "Aarav",
                createdAt = "Today",
                thumbs = 24,
                replies = listOf(
                    ForumReply(
                        id = "reply-1",
                        author = "Samriddhi",
                        body = "Draw the x-y axes first, then write signs before values. It prevents most mistakes.",
                        createdAt = "1h",
                        thumbs = 18
                    )
                )
            ),
            ForumThread(
                id = "thread-chemistry-bonding",
                subject = Subject.Chemistry,
                grade = GradeLevel.Grade11,
                title = "Best way to remember hybridization?",
                body = "Is there a quick pattern for sp, sp2, and sp3 examples?",
                author = "Nisha",
                createdAt = "Yesterday",
                thumbs = 17,
                replies = listOf(
                    ForumReply(
                        id = "reply-2",
                        author = "Bikash",
                        body = "Count sigma bonds plus lone pairs around the central atom. Two is sp, three is sp2, four is sp3.",
                        createdAt = "3h",
                        thumbs = 21
                    )
                )
            )
        )
    )

    val threads: StateFlow<List<ForumThread>> = _threads

    fun thread(threadId: String): ForumThread? = _threads.value.firstOrNull { it.id == threadId }

    fun addReply(threadId: String, body: String) {
        if (body.isBlank()) return
        _threads.update { threads ->
            threads.map { thread ->
                if (thread.id != threadId) return@map thread
                thread.copy(
                    replies = thread.replies + ForumReply(
                        id = UUID.randomUUID().toString(),
                        author = "You",
                        body = body.trim(),
                        createdAt = "Now",
                        thumbs = 0
                    )
                )
            }
        }
    }

    fun thumbThread(threadId: String) {
        _threads.update { threads ->
            threads.map { thread ->
                if (thread.id == threadId) thread.copy(thumbs = thread.thumbs + 1) else thread
            }
        }
    }

    fun thumbReply(threadId: String, replyId: String) {
        _threads.update { threads ->
            threads.map { thread ->
                if (thread.id != threadId) return@map thread
                thread.copy(
                    replies = thread.replies.map { reply ->
                        if (reply.id == replyId) reply.copy(thumbs = reply.thumbs + 1) else reply
                    }
                )
            }
        }
    }
}

object AnnouncementRepository {
    val announcements = listOf(
        Announcement(
            id = "exam-routine",
            title = "Grade 12 board routine checklist",
            body = "Keep admit card, calculator, pens, and subject notes ready one day before each exam.",
            category = "Exam",
            time = "Pinned"
        ),
        Announcement(
            id = "community-guidelines",
            title = "Community answers now support replies",
            body = "Use thumbs for helpful answers and keep discussion focused on study questions.",
            category = "Forum",
            time = "Today"
        ),
        Announcement(
            id = "offline-cache",
            title = "Offline PDF cache enabled",
            body = "Opened resources remain available from the device cache with saved annotations.",
            category = "Library",
            time = "This week"
        )
    )
}

object NotificationHelper {
    const val CHANNEL_ID = "neb_important_updates"

    fun ensureChannel(context: Context) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return
        val channel = NotificationChannel(
            CHANNEL_ID,
            "Important updates",
            NotificationManager.IMPORTANCE_DEFAULT
        ).apply {
            description = "Announcements and community activity from NEBians"
        }
        context.getSystemService(NotificationManager::class.java).createNotificationChannel(channel)
    }

    fun show(context: Context, title: String, body: String) {
        val intent = Intent(context, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            context,
            0,
            intent,
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )
        val notification = NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setContentTitle(title)
            .setContentText(body)
            .setStyle(NotificationCompat.BigTextStyle().bigText(body))
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .build()

        runCatching {
            NotificationManagerCompat.from(context)
                .notify(max(1, title.hashCode()), notification)
        }
    }
}
