package com.neb.ians.data

enum class GradeLevel(val label: String) {
    Grade11("Grade 11"),
    Grade12("Grade 12")
}

enum class Subject(val label: String) {
    Physics("Physics"),
    Chemistry("Chemistry"),
    Mathematics("Mathematics"),
    English("English"),
    ComputerScience("Computer Science"),
    Biology("Biology"),
    Accountancy("Accountancy"),
    Economics("Economics")
}

enum class ResourceType(val label: String) {
    Textbook("Textbook"),
    Notes("Notes"),
    PastPapers("Past Papers"),
    FormulaSheet("Formula Sheet")
}

data class LearningResource(
    val id: String,
    val title: String,
    val subject: Subject,
    val grade: GradeLevel,
    val type: ResourceType,
    val pages: Int,
    val updated: String,
    val summary: String,
    val tags: List<String>
)

data class Announcement(
    val id: String,
    val title: String,
    val body: String,
    val important: Boolean,
    val time: String
)

object ResourceCatalog {
    val subjects = Subject.entries
    val grades = GradeLevel.entries
    val types = ResourceType.entries

    val resources = listOf(
        LearningResource(
            id = "physics-11-textbook",
            title = "Physics Core Textbook",
            subject = Subject.Physics,
            grade = GradeLevel.Grade11,
            type = ResourceType.Textbook,
            pages = 5,
            updated = "May 2026",
            summary = "Mechanics, measurements, heat, waves, and foundational NEB Physics concepts.",
            tags = listOf("mechanics", "waves", "heat")
        ),
        LearningResource(
            id = "chemistry-11-notes",
            title = "Chemistry Revision Notes",
            subject = Subject.Chemistry,
            grade = GradeLevel.Grade11,
            type = ResourceType.Notes,
            pages = 4,
            updated = "May 2026",
            summary = "Short notes for atomic structure, bonding, stoichiometry, and lab safety.",
            tags = listOf("bonding", "atomic structure", "mole concept")
        ),
        LearningResource(
            id = "mathematics-12-formulas",
            title = "Mathematics Formula Sheet",
            subject = Subject.Mathematics,
            grade = GradeLevel.Grade12,
            type = ResourceType.FormulaSheet,
            pages = 3,
            updated = "May 2026",
            summary = "Calculus, vectors, matrices, probability, and trigonometry formulas.",
            tags = listOf("calculus", "vectors", "matrix")
        ),
        LearningResource(
            id = "biology-12-past-papers",
            title = "Biology Past Papers",
            subject = Subject.Biology,
            grade = GradeLevel.Grade12,
            type = ResourceType.PastPapers,
            pages = 6,
            updated = "April 2026",
            summary = "Chapter-wise model questions and board-style answer outlines.",
            tags = listOf("model questions", "botany", "zoology")
        ),
        LearningResource(
            id = "computer-12-notes",
            title = "Computer Science Notes",
            subject = Subject.ComputerScience,
            grade = GradeLevel.Grade12,
            type = ResourceType.Notes,
            pages = 4,
            updated = "April 2026",
            summary = "Programming, databases, networking, and web technology notes.",
            tags = listOf("programming", "sql", "networking")
        ),
        LearningResource(
            id = "english-11-notes",
            title = "English Literature Guide",
            subject = Subject.English,
            grade = GradeLevel.Grade11,
            type = ResourceType.Notes,
            pages = 4,
            updated = "March 2026",
            summary = "Concise summaries, important questions, and writing format practice.",
            tags = listOf("summary", "writing", "grammar")
        ),
        LearningResource(
            id = "accountancy-12-textbook",
            title = "Accountancy Workbook",
            subject = Subject.Accountancy,
            grade = GradeLevel.Grade12,
            type = ResourceType.Textbook,
            pages = 5,
            updated = "March 2026",
            summary = "Company accounts, cash flow, partnership, and practical ledger examples.",
            tags = listOf("ledger", "cash flow", "partnership")
        ),
        LearningResource(
            id = "economics-11-papers",
            title = "Economics Practice Papers",
            subject = Subject.Economics,
            grade = GradeLevel.Grade11,
            type = ResourceType.PastPapers,
            pages = 4,
            updated = "February 2026",
            summary = "Practice sets for microeconomics, demand, supply, and market structures.",
            tags = listOf("microeconomics", "demand", "supply")
        )
    )

    val announcements = listOf(
        Announcement(
            id = "exam-routine",
            title = "Grade 12 model exam routine updated",
            body = "Check the latest routine and keep key dates saved in your study plan.",
            important = true,
            time = "Today"
        ),
        Announcement(
            id = "new-physics",
            title = "New Physics notes available",
            body = "Mechanics quick notes and solved numericals are now cached for offline reading.",
            important = false,
            time = "Yesterday"
        ),
        Announcement(
            id = "community-guidelines",
            title = "Community answer quality reminder",
            body = "Use clear steps, cite chapter names, and tap thumbs-up for helpful answers.",
            important = false,
            time = "This week"
        )
    )

    fun resourceById(id: String): LearningResource? = resources.firstOrNull { it.id == id }
}
