package com.neb.ians.data.model

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

enum class Subject(val displayName: String) {
    PHYSICS("Physics"),
    CHEMISTRY("Chemistry"),
    MATHEMATICS("Mathematics"),
    BIOLOGY("Biology"),
    ENGLISH("English"),
    NEPALI("Nepali"),
    COMPUTER("Computer Science")
}

enum class Grade(val displayName: String) {
    GRADE_11("Grade 11"),
    GRADE_12("Grade 12")
}

enum class ResourceType(val displayName: String) {
    TEXTBOOK("Textbook"),
    NOTES("Notes"),
    PAST_PAPERS("Past Papers"),
    GUIDE("Guide")
}

@Parcelize
data class Resource(
    val id: String,
    val title: String,
    val subject: Subject,
    val grade: Grade,
    val type: ResourceType,
    val remoteUrl: String,
    val localPath: String? = null,
    val fileSizeBytes: Long = 0L,
    val isDownloaded: Boolean = false
) : Parcelable

@Parcelize
data class ForumThread(
    val id: String,
    val title: String,
    val body: String,
    val authorName: String = "Student",
    val likes: Int = 0,
    val repliesCount: Int = 0,
    val createdAt: Long = System.currentTimeMillis()
) : Parcelable

@Parcelize
data class ForumReply(
    val id: String,
    val threadId: String,
    val body: String,
    val authorName: String = "Student",
    val likes: Int = 0,
    val createdAt: Long = System.currentTimeMillis()
) : Parcelable

data class PdfAnnotation(
    val id: String,
    val pdfPath: String,
    val pageIndex: Int,
    val type: AnnotationType,
    val x: Float,
    val y: Float,
    val width: Float,
    val height: Float,
    val noteText: String? = null,
    val color: Int = 0xFFFFEB3B.toInt(),
    val createdAt: Long = System.currentTimeMillis()
)

enum class AnnotationType {
    HIGHLIGHT, UNDERLINE, STICKY_NOTE
}
