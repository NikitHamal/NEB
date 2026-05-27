package com.neb.ians.data.model

enum class Subject(val display: String) {
    Physics("Physics"),
    Chemistry("Chemistry"),
    Mathematics("Mathematics"),
    Biology("Biology"),
    English("English"),
    Nepali("Nepali"),
    ComputerScience("Computer Science"),
    Economics("Economics"),
    Accountancy("Accountancy"),
    BusinessStudies("Business Studies"),
    Other("Other"),
}

enum class Grade(val display: String) {
    Grade11("Grade 11"),
    Grade12("Grade 12"),
    SEE("SEE"),
    BachelorPrep("Bachelor Prep"),
    Other("Other"),
}

enum class ResourceType(val display: String) {
    Textbook("Textbook"),
    Notes("Notes"),
    PastPapers("Past Papers"),
    Solution("Solutions"),
    Ebook("Ebook"),
    Other("Other"),
}
