package com.neb.ians.data

import com.neb.ians.data.local.entity.ForumPostEntity
import com.neb.ians.data.local.entity.ResourceEntity

object SampleData {

    val subjects = listOf(
        "Physics", "Chemistry", "Mathematics", "Biology",
        "English", "Nepali", "Computer Science", "Economics",
        "Account", "Social Studies"
    )

    val grades = listOf("Grade 11", "Grade 12")

    val resourceTypes = listOf("Textbook", "Notes", "Past Papers", "Solution", "Guide")

    fun getSampleResources(): List<ResourceEntity> = listOf(
        ResourceEntity(
            title = "Physics Complete Notes",
            description = "Comprehensive notes covering all chapters of NEB Physics for Grade 12 including mechanics, thermodynamics, optics, and modern physics.",
            subject = "Physics",
            grade = "Grade 12",
            type = "Notes",
            fileUrl = "https://example.com/physics-12-notes.pdf",
            fileSize = 5_200_000,
            author = "Prof. Ram Sharma",
        ),
        ResourceEntity(
            title = "Chemistry Textbook",
            description = "Official NEB Chemistry textbook for Grade 11 with detailed explanations and solved examples.",
            subject = "Chemistry",
            grade = "Grade 11",
            type = "Textbook",
            fileUrl = "https://example.com/chemistry-11.pdf",
            fileSize = 12_400_000,
            author = "CDC Nepal",
        ),
        ResourceEntity(
            title = "Mathematics Past Papers 2080",
            description = "Collection of past examination papers for NEB Mathematics Grade 12 from year 2080 BS.",
            subject = "Mathematics",
            grade = "Grade 12",
            type = "Past Papers",
            fileUrl = "https://example.com/math-past-2080.pdf",
            fileSize = 3_100_000,
            author = "NEB Board",
        ),
        ResourceEntity(
            title = "Biology Guide",
            description = "Study guide with key concepts, diagrams, and practice questions for NEB Biology Grade 11.",
            subject = "Biology",
            grade = "Grade 11",
            type = "Guide",
            fileUrl = "https://example.com/biology-guide-11.pdf",
            fileSize = 8_700_000,
            author = "Dr. Sita Devi",
        ),
        ResourceEntity(
            title = "English Grammar Notes",
            description = "Complete grammar and composition notes following NEB English syllabus for Grade 12.",
            subject = "English",
            grade = "Grade 12",
            type = "Notes",
            fileUrl = "https://example.com/english-grammar-12.pdf",
            fileSize = 2_800_000,
            author = "Mrs. Anita Thapa",
        ),
        ResourceEntity(
            title = "Computer Science Solution",
            description = "Chapter-wise solutions manual for NEB Computer Science Grade 11 covering programming and theory.",
            subject = "Computer Science",
            grade = "Grade 11",
            type = "Solution",
            fileUrl = "https://example.com/cs-solution-11.pdf",
            fileSize = 4_500_000,
            author = "Er. Bikash KC",
        ),
        ResourceEntity(
            title = "Nepali Sahitya Notes",
            description = "Detailed literary analysis and notes for NEB Nepali curriculum Grade 12.",
            subject = "Nepali",
            grade = "Grade 12",
            type = "Notes",
            fileUrl = "https://example.com/nepali-sahitya-12.pdf",
            fileSize = 3_900_000,
            author = "Guru Prasad Mainali",
        ),
        ResourceEntity(
            title = "Economics Textbook",
            description = "Macroeconomics and microeconomics concepts for NEB Grade 11 with Nepali context examples.",
            subject = "Economics",
            grade = "Grade 11",
            type = "Textbook",
            fileUrl = "https://example.com/economics-11.pdf",
            fileSize = 6_200_000,
            author = "CDC Nepal",
        ),
        ResourceEntity(
            title = "Physics Past Papers 2079",
            description = "NEB Physics Grade 12 past examination papers from 2079 BS with marking scheme.",
            subject = "Physics",
            grade = "Grade 12",
            type = "Past Papers",
            fileUrl = "https://example.com/physics-past-2079.pdf",
            fileSize = 2_500_000,
            author = "NEB Board",
        ),
        ResourceEntity(
            title = "Account Complete Guide",
            description = "Full accounting guide with solved numericals for NEB Grade 11 including journal entries and ledger.",
            subject = "Account",
            grade = "Grade 11",
            type = "Guide",
            fileUrl = "https://example.com/account-guide-11.pdf",
            fileSize = 7_100_000,
            author = "CA Rajesh Adhikari",
        ),
        ResourceEntity(
            title = "Mathematics Formula Sheet",
            description = "Quick reference formula sheet for NEB Math Grade 11 covering algebra, trigonometry, and calculus.",
            subject = "Mathematics",
            grade = "Grade 11",
            type = "Notes",
            fileUrl = "https://example.com/math-formulas-11.pdf",
            fileSize = 1_200_000,
            author = "Mr. Hari Bahadur",
        ),
        ResourceEntity(
            title = "Chemistry Lab Manual",
            description = "Laboratory manual with practical experiments for NEB Chemistry Grade 12.",
            subject = "Chemistry",
            grade = "Grade 12",
            type = "Guide",
            fileUrl = "https://example.com/chem-lab-12.pdf",
            fileSize = 4_800_000,
            author = "Dr. Binod Karki",
        ),
    )

    fun getSamplePosts(): List<ForumPostEntity> = listOf(
        ForumPostEntity(
            title = "How to solve integration by parts?",
            body = "I'm struggling with integration by parts in Mathematics Grade 12. Can someone explain the LIATE rule with examples? I keep getting confused about which function to choose as u and which as dv.",
            authorName = "Aarav S.",
            subject = "Mathematics",
            grade = "Grade 12",
            thumbsUp = 15,
            replyCount = 8,
        ),
        ForumPostEntity(
            title = "NEB Physics practical tips?",
            body = "The practical exam is coming up next month. What are the most important experiments to focus on for Grade 12 Physics? Also, any tips for the viva section?",
            authorName = "Priya M.",
            subject = "Physics",
            grade = "Grade 12",
            thumbsUp = 23,
            replyCount = 12,
        ),
        ForumPostEntity(
            title = "Best study schedule for board exams",
            body = "I have 3 months until boards. Currently in Grade 12 science. How should I divide my time between subjects? I'm weak in Chemistry and English but strong in Physics and Math.",
            authorName = "Rohan K.",
            subject = "",
            grade = "Grade 12",
            thumbsUp = 45,
            replyCount = 20,
        ),
        ForumPostEntity(
            title = "Organic Chemistry reaction mechanisms",
            body = "Does anyone have a simplified chart or flowchart for organic chemistry reaction mechanisms? The textbook explanations are too complex for me to follow.",
            authorName = "Suman R.",
            subject = "Chemistry",
            grade = "Grade 12",
            thumbsUp = 18,
            replyCount = 6,
        ),
        ForumPostEntity(
            title = "Grade 11 Computer Science project ideas",
            body = "We need to submit a project for Computer Science. What are some interesting project ideas that are doable but impressive? Preferably in C programming.",
            authorName = "Diksha T.",
            subject = "Computer Science",
            grade = "Grade 11",
            thumbsUp = 31,
            replyCount = 14,
        ),
    )
}
