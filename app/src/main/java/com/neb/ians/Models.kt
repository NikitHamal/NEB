package com.neb.ians

enum class Subject(val label: String) {
    Physics("Physics"),
    Chemistry("Chemistry"),
    Mathematics("Mathematics"),
    Biology("Biology"),
    English("English"),
    Nepali("Nepali"),
    ComputerScience("Computer Science"),
    Accountancy("Accountancy")
}

enum class GradeLevel(val label: String) {
    Grade11("Grade 11"),
    Grade12("Grade 12")
}

enum class ResourceType(val label: String) {
    Textbook("Textbook"),
    Notes("Notes"),
    PastPapers("Past Papers"),
    FormulaSheet("Formula Sheet"),
    Syllabus("Syllabus")
}

data class LearningResource(
    val id: String,
    val title: String,
    val subject: Subject,
    val grade: GradeLevel,
    val type: ResourceType,
    val description: String,
    val localFileName: String,
    val remoteUrl: String? = null,
    val tags: List<String> = emptyList()
)

enum class AnnotationKind {
    Highlight,
    Underline,
    StickyNote
}

enum class AnnotationTool(val label: String) {
    Navigate("Read"),
    Highlight("Highlight"),
    Underline("Underline"),
    StickyNote("Note")
}

data class PdfAnnotation(
    val id: String,
    val pdfId: String,
    val pageIndex: Int,
    val kind: AnnotationKind,
    val x: Float,
    val y: Float,
    val width: Float,
    val height: Float,
    val note: String,
    val color: Int,
    val createdAt: Long
)

data class ForumReply(
    val id: String,
    val author: String,
    val body: String,
    val createdAt: String,
    val thumbs: Int
)

data class ForumThread(
    val id: String,
    val subject: Subject,
    val grade: GradeLevel,
    val title: String,
    val body: String,
    val author: String,
    val createdAt: String,
    val thumbs: Int,
    val replies: List<ForumReply>
)

data class Announcement(
    val id: String,
    val title: String,
    val body: String,
    val category: String,
    val time: String
)

object SampleCatalog {
    val resources = listOf(
        LearningResource(
            id = "physics-11-textbook",
            title = "Physics Concepts and Numericals",
            subject = Subject.Physics,
            grade = GradeLevel.Grade11,
            type = ResourceType.Textbook,
            description = "Mechanics, heat, waves, and worked numerical patterns for NEB.",
            localFileName = "physics_11_textbook.pdf",
            tags = listOf("mechanics", "waves", "numericals")
        ),
        LearningResource(
            id = "chemistry-11-notes",
            title = "Chemistry Quick Notes",
            subject = Subject.Chemistry,
            grade = GradeLevel.Grade11,
            type = ResourceType.Notes,
            description = "Atomic structure, bonding, periodic trends, and short revision notes.",
            localFileName = "chemistry_11_notes.pdf",
            tags = listOf("bonding", "periodic table", "revision")
        ),
        LearningResource(
            id = "math-12-past-papers",
            title = "Mathematics Past Papers",
            subject = Subject.Mathematics,
            grade = GradeLevel.Grade12,
            type = ResourceType.PastPapers,
            description = "Board-style calculus, algebra, vectors, and probability practice.",
            localFileName = "math_12_past_papers.pdf",
            tags = listOf("calculus", "vectors", "probability")
        ),
        LearningResource(
            id = "biology-12-notes",
            title = "Biology Revision Notes",
            subject = Subject.Biology,
            grade = GradeLevel.Grade12,
            type = ResourceType.Notes,
            description = "Cell biology, genetics, ecology, and human physiology summaries.",
            localFileName = "biology_12_notes.pdf",
            tags = listOf("genetics", "ecology", "physiology")
        ),
        LearningResource(
            id = "english-11-syllabus",
            title = "English Syllabus and Writing Guide",
            subject = Subject.English,
            grade = GradeLevel.Grade11,
            type = ResourceType.Syllabus,
            description = "Updated reading, grammar, essay, and exam-writing structure.",
            localFileName = "english_11_syllabus.pdf",
            tags = listOf("writing", "grammar", "syllabus")
        ),
        LearningResource(
            id = "computer-12-formulas",
            title = "Computer Science Formula Sheet",
            subject = Subject.ComputerScience,
            grade = GradeLevel.Grade12,
            type = ResourceType.FormulaSheet,
            description = "Logic gates, networking, database, and programming quick reference.",
            localFileName = "computer_12_formulas.pdf",
            tags = listOf("database", "networking", "programming")
        )
    )
}
