package com.neb.ians.data.model

enum class Subject(val display: String) {
    PHYSICS("Physics"),
    CHEMISTRY("Chemistry"),
    MATHEMATICS("Mathematics"),
    BIOLOGY("Biology"),
    ENGLISH("English"),
    NEPALI("Nepali"),
    COMPUTER("Computer Science"),
    ACCOUNTANCY("Accountancy"),
    ECONOMICS("Economics");
    companion object { fun fromName(n: String?) = values().firstOrNull { it.name == n } }
}

enum class Grade(val display: String) {
    GRADE_11("Grade 11"),
    GRADE_12("Grade 12");
    companion object { fun fromName(n: String?) = values().firstOrNull { it.name == n } }
}

enum class ResourceType(val display: String) {
    TEXTBOOK("Textbook"),
    NOTES("Notes"),
    PAST_PAPER("Past Papers"),
    SYLLABUS("Syllabus"),
    REFERENCE("Reference");
    companion object { fun fromName(n: String?) = values().firstOrNull { it.name == n } }
}
