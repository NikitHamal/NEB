package com.neb.ians.data.api

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * The syllabus tab. [grades] holds the school classes only (installed app versions print every
 * entry as "Class N"); [tracks] holds the entrance-examination tracks (CEE, IOE, CSIT, BCA), which
 * older servers do not send.
 */
@Serializable
data class ApiSyllabusIndex(
    val grades: List<ApiSyllabusGrade> = emptyList(),
    val tracks: List<ApiSyllabusGrade> = emptyList(),
    val totals: ApiSyllabusTotals = ApiSyllabusTotals()
) {
    /** School classes first, then the entrance tracks: everything the class switch offers. */
    val all: List<ApiSyllabusGrade> get() = grades + tracks
}

@Serializable
data class ApiSyllabusTotals(
    val grades: Int = 0,
    val subjects: Int = 0,
    val units: Int = 0,
    val topics: Int = 0
)

/** A school class ("11") or an entrance track ("cee"); [grade] is the key in every route. */
@Serializable
data class ApiSyllabusGrade(
    val grade: String = "",
    val label: String = "",
    @SerialName("label_ne") val labelNe: String = "",
    val exam: String = "",
    /** What a button prints where a class number would go: "Class 11", "CEE". */
    val short: String = "",
    /** "school" or "entrance". */
    val kind: String = "school",
    val subjects: List<ApiSyllabusSubjectCard> = emptyList()
) {
    val isTrack: Boolean get() = isSyllabusTrack(kind, grade)
}

@Serializable
data class ApiSyllabusSubjectCard(
    val subject: String = "",
    val name: String = "",
    @SerialName("name_ne") val nameNe: String = "",
    val icon: String = "",
    val group: String = "",
    val lang: String = "en",
    val hours: Int? = null,
    /** Entrance tracks: how many questions of the paper the subject carries. */
    val questions: Int? = null,
    @SerialName("unit_count") val unitCount: Int = 0,
    @SerialName("topic_count") val topicCount: Int = 0,
    /** Objective and subjective question sets of the subject (model papers are counted apart). */
    @SerialName("bank_count") val bankCount: Int = 0,
    @SerialName("model_count") val modelCount: Int = 0,
    @SerialName("has_guide") val hasGuide: Boolean = false
)

@Serializable
data class ApiSyllabusDoc(
    val grade: String = "",
    @SerialName("grade_label") val gradeLabel: String = "",
    @SerialName("grade_label_ne") val gradeLabelNe: String = "",
    val subject: String = "",
    val name: String = "",
    @SerialName("name_ne") val nameNe: String = "",
    val icon: String = "",
    val lang: String = "en",
    val code: String = "",
    val hours: Int? = null,
    /** Entrance tracks: questions in the paper for the whole subject (spine `QUESTIONS:`). */
    val questions: Int? = null,
    val kind: String = "school",
    val short: String = "",
    val exam: String = "",
    val areas: List<String> = emptyList(),
    val units: List<ApiSyllabusUnit> = emptyList(),
    @SerialName("unit_count") val unitCount: Int = 0,
    @SerialName("topic_count") val topicCount: Int = 0,
    val banks: List<ApiSyllabusBank> = emptyList(),
    val guide: String? = null
) {
    val isTrack: Boolean get() = isSyllabusTrack(kind, grade)
}

@Serializable
data class ApiSyllabusUnit(
    val no: Int = 0,
    val title: String = "",
    val hours: Int? = null,
    /** Entrance tracks: questions this chapter carries in the paper (hours stay null). */
    val questions: Int? = null,
    val area: String = "",
    val topics: List<String> = emptyList(),
    val sections: List<ApiSyllabusBookSection> = emptyList(),
    val summary: List<String> = emptyList(),
    val terms: List<String> = emptyList(),
    @SerialName("read_min") val readMin: Int = 0,
    @SerialName("has_chapter") val hasChapter: Boolean = false,
    /** Set on a model paper of an entrance mock book: it can be taken as a timed test. */
    val exam: ApiStudyExam? = null
)

/** One question-bank chapter of a subject: objective, subjective or model sets. */
@Serializable
data class ApiSyllabusBank(
    val no: Int = 0,
    val kind: String = "",
    val title: String = "",
    val label: String = "",
    val blurb: String = "",
    @SerialName("read_min") val readMin: Int = 0
)

/**
 * A chapter, a question-bank chapter or the exam guide, as the book prints it: HTML with
 * maths left as TeX in `span.m` (KaTeX typesets it), figures as /static/web/study/ URLs,
 * answers folded in `details.ans`, multiple-choice items carrying `data-key`.
 */
@Serializable
data class ApiStudyDoc(
    val title: String = "",
    val area: String? = null,
    val hours: String? = null,
    val lang: String = "en",
    val words: Int = 0,
    @SerialName("read_min") val readMin: Int = 0,
    val figures: Int = 0,
    val toc: List<ApiStudyTocItem> = emptyList(),
    val html: String = "",
    val kind: String? = null,
    val type: String = "unit",
    val no: Int? = null,
    val prev: Int? = null,
    val next: Int? = null,
    @SerialName("media_base") val mediaBase: String = "https://nebians.consica.com.np/",
    /** Set on a model paper: it can be taken as a timed test. */
    val exam: ApiStudyExam? = null
)

/** A model paper as a timed test: its length and the marks lost per wrong answer. */
@Serializable
data class ApiStudyExam(
    val minutes: Int = 0,
    val negative: Double = 0.0
)

@Serializable
data class ApiStudyTocItem(
    val id: String = "",
    val title: String = "",
    val kind: String = ""
)

@Serializable
data class ApiSyllabusBookSection(
    val no: String = "",
    val title: String = ""
)

@Serializable
data class ApiSyllabusSearch(
    val q: String = "",
    val results: List<ApiSyllabusHit> = emptyList(),
    val total: Int = 0
)

@Serializable
data class ApiSyllabusHit(
    val grade: String = "",
    /** "Class 10" or "CEE"; older servers send none. */
    val short: String = "",
    val subject: String = "",
    val name: String = "",
    val unit: Int = 0,
    val title: String = "",
    val match: String = ""
)

/** A school class has a numeric key ("8", "11"); entrance tracks have a name ("cee"). */
fun isSchoolGrade(grade: String): Boolean = grade.isNotEmpty() && grade.all { it.isDigit() }

/** An entry is a track when the server says so, or (older servers) when its key is not a number. */
fun isSyllabusTrack(kind: String, grade: String): Boolean = kind != "school" || !isSchoolGrade(grade)

/** What to print where a class number would go: the server's `short`, else "Class 11" or "CEE". */
fun syllabusShort(grade: String, short: String = ""): String =
    short.ifBlank { if (isSchoolGrade(grade)) "Class $grade" else grade.uppercase() }
