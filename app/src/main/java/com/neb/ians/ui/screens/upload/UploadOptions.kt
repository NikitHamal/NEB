package com.neb.ians.ui.screens.upload

/**
 * The lists the upload screen offers and the limits it enforces.
 *
 * Kept apart from the view model because they are content, not behaviour —
 * a new subject or a new exam type is an edit to a list, not to a screen.
 */
object UploadOptions {

    val SUBJECTS = listOf(
        "Accountancy", "Biology", "Chemistry", "Computer Science", "Economics",
        "English", "Exam Tips", "Mathematics", "Microbiology", "Nepali",
        "Physics", "Physics - Technical Stream", "Science", "Social Studies",
        "Software Engineering", "Software Engineering and Project Management",
        "Visual Programming", "Zoology", "\u0938\u093E\u092E\u093E\u091C\u093F\u0915 \u0905\u0927\u094D\u092F\u092F\u0928"
    )

    val GRADE_LEVELS = listOf(
        "Class 8", "Class 10 / SEE", "Class 11", "Class 12", "Entrance Prep",
        "Bachelor", "Other"
    )

    val RESOURCE_TYPES = listOf(
        "PDF", "Note", "Video", "Audio", "Image", "Link", "Textbook",
        "Past Paper", "Model Paper", "Guide", "Solution", "Presentation"
    )

    val EXAM_TYPES = listOf(
        "Final", "Midterm", "Board", "Entrance", "SEE", "Mock", "Assignment", "Notes", "Reference", "Other"
    )

    val PROVINCES = listOf(
        "Koshi", "Madhesh", "Bagmati", "Gandaki", "Lumbini", "Karnali", "Sudurpashchim"
    )

    val COMMON_TAGS = listOf(
        "NEB", "SEE", "Class 11", "Class 12", "Important Questions",
        "Past Paper", "Notes", "Solution", "Guide", "Textbook",
        "Formula", "Practical", "Project", "Tips", "Revision"
    )

    val VIDEO_EXTENSIONS = setOf("mp4", "mkv", "mov", "webm", "avi", "m4v", "3gp", "wmv", "flv")

    fun isVideoFileName(name: String): Boolean =
        name.substringAfterLast('.', "").lowercase() in VIDEO_EXTENSIONS

    /** The server rejects anything larger, so the screen has to say so first. */
    const val MAX_FILE_SIZE = 50L * 1024 * 1024

    /** Page photos become one document, so the ceiling is a thick set of notes. */
    const val MAX_PAGES = 120
}
