package com.neb.ians.data.model

import com.neb.ians.data.local.entity.ForumPostEntity
import com.neb.ians.data.local.entity.ForumReplyEntity
import com.neb.ians.data.local.entity.ResourceEntity

object SampleData {

    val resources = listOf(
        // Physics - Grade 11
        ResourceEntity(
            id = "res_phy_11_01",
            title = "NEB Physics Class 11 Textbook",
            description = "Official NEB curriculum textbook for Physics Class 11 covering Mechanics, Heat, and Waves.",
            subject = "Physics",
            gradeLevel = "Grade 11",
            type = "Textbook",
            fileUrl = "https://resources.nebians.com/physics/class11/textbook.pdf",
            fileSize = 15_400_000,
            author = "CDC Nepal"
        ),
        ResourceEntity(
            id = "res_phy_11_02",
            title = "Physics Notes - Mechanics & Kinematics",
            description = "Comprehensive handwritten notes covering Newton's Laws, projectile motion, and circular motion for Class 11.",
            subject = "Physics",
            gradeLevel = "Grade 11",
            type = "Notes",
            fileUrl = "https://resources.nebians.com/physics/class11/mechanics_notes.pdf",
            fileSize = 4_200_000,
            author = "NEBians Community"
        ),
        // Physics - Grade 12
        ResourceEntity(
            id = "res_phy_12_01",
            title = "NEB Physics Class 12 Textbook",
            description = "Official NEB curriculum textbook for Physics Class 12 covering Electricity, Magnetism, and Modern Physics.",
            subject = "Physics",
            gradeLevel = "Grade 12",
            type = "Textbook",
            fileUrl = "https://resources.nebians.com/physics/class12/textbook.pdf",
            fileSize = 18_200_000,
            author = "CDC Nepal"
        ),
        ResourceEntity(
            id = "res_phy_12_02",
            title = "Physics Past Paper 2080 BS",
            description = "NEB board examination paper for Physics from 2080 BS with marking scheme.",
            subject = "Physics",
            gradeLevel = "Grade 12",
            type = "Past Papers",
            fileUrl = "https://resources.nebians.com/physics/class12/past_paper_2080.pdf",
            fileSize = 2_100_000,
            author = "NEB Board"
        ),

        // Chemistry - Grade 11
        ResourceEntity(
            id = "res_chem_11_01",
            title = "NEB Chemistry Class 11 Textbook",
            description = "Official NEB curriculum textbook for Chemistry Class 11 covering General and Physical Chemistry.",
            subject = "Chemistry",
            gradeLevel = "Grade 11",
            type = "Textbook",
            fileUrl = "https://resources.nebians.com/chemistry/class11/textbook.pdf",
            fileSize = 14_800_000,
            author = "CDC Nepal"
        ),
        ResourceEntity(
            id = "res_chem_11_02",
            title = "Chemistry Notes - Atomic Structure & Periodic Table",
            description = "Detailed notes on atomic models, electronic configuration, and periodic properties.",
            subject = "Chemistry",
            gradeLevel = "Grade 11",
            type = "Notes",
            fileUrl = "https://resources.nebians.com/chemistry/class11/atomic_structure_notes.pdf",
            fileSize = 3_500_000,
            author = "NEBians Community"
        ),
        // Chemistry - Grade 12
        ResourceEntity(
            id = "res_chem_12_01",
            title = "Chemistry Notes - Organic Chemistry",
            description = "Complete notes on organic chemistry including hydrocarbons, alcohols, aldehydes, ketones, and carboxylic acids.",
            subject = "Chemistry",
            gradeLevel = "Grade 12",
            type = "Notes",
            fileUrl = "https://resources.nebians.com/chemistry/class12/organic_notes.pdf",
            fileSize = 5_600_000,
            author = "NEBians Community"
        ),
        ResourceEntity(
            id = "res_chem_12_02",
            title = "Chemistry Past Paper 2080 BS",
            description = "NEB board examination paper for Chemistry from 2080 BS with solution guide.",
            subject = "Chemistry",
            gradeLevel = "Grade 12",
            type = "Past Papers",
            fileUrl = "https://resources.nebians.com/chemistry/class12/past_paper_2080.pdf",
            fileSize = 1_800_000,
            author = "NEB Board"
        ),

        // Mathematics - Grade 11
        ResourceEntity(
            id = "res_math_11_01",
            title = "NEB Mathematics Class 11 Textbook",
            description = "Official NEB curriculum textbook for Mathematics Class 11 covering Algebra, Trigonometry, and Coordinate Geometry.",
            subject = "Mathematics",
            gradeLevel = "Grade 11",
            type = "Textbook",
            fileUrl = "https://resources.nebians.com/math/class11/textbook.pdf",
            fileSize = 12_500_000,
            author = "CDC Nepal"
        ),
        ResourceEntity(
            id = "res_math_11_02",
            title = "Mathematics Notes - Trigonometry",
            description = "Step-by-step solutions and notes for trigonometric identities, equations, and inverse functions.",
            subject = "Mathematics",
            gradeLevel = "Grade 11",
            type = "Notes",
            fileUrl = "https://resources.nebians.com/math/class11/trigonometry_notes.pdf",
            fileSize = 3_800_000,
            author = "NEBians Community"
        ),
        // Mathematics - Grade 12
        ResourceEntity(
            id = "res_math_12_01",
            title = "NEB Mathematics Class 12 Textbook",
            description = "Official NEB curriculum textbook for Mathematics Class 12 covering Calculus, Vectors, and Statistics.",
            subject = "Mathematics",
            gradeLevel = "Grade 12",
            type = "Textbook",
            fileUrl = "https://resources.nebians.com/math/class12/textbook.pdf",
            fileSize = 13_700_000,
            author = "CDC Nepal"
        ),
        ResourceEntity(
            id = "res_math_12_02",
            title = "Mathematics Past Paper 2080 BS",
            description = "NEB board examination paper for Mathematics from 2080 BS with detailed solutions.",
            subject = "Mathematics",
            gradeLevel = "Grade 12",
            type = "Past Papers",
            fileUrl = "https://resources.nebians.com/math/class12/past_paper_2080.pdf",
            fileSize = 2_400_000,
            author = "NEB Board"
        ),

        // Biology - Grade 11
        ResourceEntity(
            id = "res_bio_11_01",
            title = "NEB Biology Class 11 Textbook",
            description = "Official NEB curriculum textbook for Biology Class 11 covering Botany and Zoology.",
            subject = "Biology",
            gradeLevel = "Grade 11",
            type = "Textbook",
            fileUrl = "https://resources.nebians.com/biology/class11/textbook.pdf",
            fileSize = 16_300_000,
            author = "CDC Nepal"
        ),
        ResourceEntity(
            id = "res_bio_11_02",
            title = "Biology Notes - Cell Biology & Biomolecules",
            description = "Comprehensive notes covering cell structure, cell division, enzymes, and biomolecules.",
            subject = "Biology",
            gradeLevel = "Grade 11",
            type = "Notes",
            fileUrl = "https://resources.nebians.com/biology/class11/cell_biology_notes.pdf",
            fileSize = 4_100_000,
            author = "NEBians Community"
        ),

        // English - Grade 12
        ResourceEntity(
            id = "res_eng_12_01",
            title = "NEB English Class 12 Textbook - Meanings into Words",
            description = "Official NEB English textbook for Class 12 with all prose, poetry, and drama sections.",
            subject = "English",
            gradeLevel = "Grade 12",
            type = "Textbook",
            fileUrl = "https://resources.nebians.com/english/class12/textbook.pdf",
            fileSize = 8_900_000,
            author = "CDC Nepal"
        ),
        ResourceEntity(
            id = "res_eng_12_02",
            title = "English Past Paper 2080 BS",
            description = "NEB board examination paper for Compulsory English from 2080 BS.",
            subject = "English",
            gradeLevel = "Grade 12",
            type = "Past Papers",
            fileUrl = "https://resources.nebians.com/english/class12/past_paper_2080.pdf",
            fileSize = 1_500_000,
            author = "NEB Board"
        ),

        // Computer Science - Grade 11
        ResourceEntity(
            id = "res_cs_11_01",
            title = "NEB Computer Science Class 11 Textbook",
            description = "Official NEB curriculum textbook for Computer Science Class 11 covering fundamentals, C programming, and web technology.",
            subject = "Computer Science",
            gradeLevel = "Grade 11",
            type = "Textbook",
            fileUrl = "https://resources.nebians.com/cs/class11/textbook.pdf",
            fileSize = 10_200_000,
            author = "CDC Nepal"
        ),
        ResourceEntity(
            id = "res_cs_11_02",
            title = "Computer Science Notes - C Programming",
            description = "Complete notes on C programming language including arrays, functions, structures, pointers, and file handling.",
            subject = "Computer Science",
            gradeLevel = "Grade 11",
            type = "Notes",
            fileUrl = "https://resources.nebians.com/cs/class11/c_programming_notes.pdf",
            fileSize = 3_200_000,
            author = "NEBians Community"
        ),
        // Computer Science - Grade 12
        ResourceEntity(
            id = "res_cs_12_01",
            title = "Computer Science Past Paper 2080 BS",
            description = "NEB board examination paper for Computer Science from 2080 BS with model answers.",
            subject = "Computer Science",
            gradeLevel = "Grade 12",
            type = "Past Papers",
            fileUrl = "https://resources.nebians.com/cs/class12/past_paper_2080.pdf",
            fileSize = 1_900_000,
            author = "NEB Board"
        )
    )

    val forumPosts = listOf(
        ForumPostEntity(
            id = "forum_01",
            title = "Help with Integration problems",
            content = "I am struggling with integration by parts in Class 12 Mathematics. Can someone explain the LIATE rule with examples? I keep getting confused about which function to choose as 'u' and which as 'dv'. Any tips would be really helpful!",
            authorName = "Aarav Sharma",
            authorId = "user_01",
            category = "Mathematics",
            thumbsUpCount = 12,
            replyCount = 5,
            createdAt = System.currentTimeMillis() - 86_400_000 * 3,
            updatedAt = System.currentTimeMillis() - 86_400_000 * 2
        ),
        ForumPostEntity(
            id = "forum_02",
            title = "Best way to study organic chemistry?",
            content = "Organic chemistry is so hard to memorize! There are so many reactions and mechanisms. How do you all study for the NEB exam? I have tried flashcards but they don't seem to work well for reaction mechanisms. Please share your study strategies.",
            authorName = "Sita Poudel",
            authorId = "user_02",
            category = "Chemistry",
            thumbsUpCount = 24,
            replyCount = 8,
            createdAt = System.currentTimeMillis() - 86_400_000 * 5,
            updatedAt = System.currentTimeMillis() - 86_400_000 * 4
        ),
        ForumPostEntity(
            id = "forum_03",
            title = "Numerical problems in Current Electricity",
            content = "Can someone help me understand how to solve Kirchhoff's law problems? I understand the theory but whenever I try to apply KVL and KCL in complex circuits with multiple loops, I get confused with the sign conventions. Any step-by-step approach?",
            authorName = "Bikash Thapa",
            authorId = "user_03",
            category = "Physics",
            thumbsUpCount = 18,
            replyCount = 6,
            createdAt = System.currentTimeMillis() - 86_400_000 * 2,
            updatedAt = System.currentTimeMillis() - 86_400_000
        ),
        ForumPostEntity(
            id = "forum_04",
            title = "NEB 2081 exam preparation tips",
            content = "The NEB exams are approaching and I feel like I haven't prepared enough. How are you all managing your revision schedule? I need to cover Physics, Chemistry, and Math. Should I focus more on past papers or textbook exercises? Any advice from seniors who have already given the exam would be great.",
            authorName = "Priya Karki",
            authorId = "user_04",
            category = "General",
            thumbsUpCount = 45,
            replyCount = 15,
            createdAt = System.currentTimeMillis() - 86_400_000,
            updatedAt = System.currentTimeMillis() - 43_200_000
        ),
        ForumPostEntity(
            id = "forum_05",
            title = "C programming - pointers and arrays confusion",
            content = "I cannot understand the difference between array notation and pointer notation in C. When we pass an array to a function, is it a pointer or a copy? Also, what is the difference between char *str and char str[]? Our textbook explanation is not clear enough.",
            authorName = "Rohan Adhikari",
            authorId = "user_05",
            category = "Computer Science",
            thumbsUpCount = 9,
            replyCount = 4,
            createdAt = System.currentTimeMillis() - 86_400_000 * 7,
            updatedAt = System.currentTimeMillis() - 86_400_000 * 6
        ),
        ForumPostEntity(
            id = "forum_06",
            title = "Cell division - Mitosis vs Meiosis differences",
            content = "I always mix up the stages of mitosis and meiosis in the exam. Can someone share a simple comparison table or mnemonic to remember the key differences? Especially the differences in prophase I of meiosis with crossing over and synapsis.",
            authorName = "Anisha Gurung",
            authorId = "user_06",
            category = "Biology",
            thumbsUpCount = 15,
            replyCount = 7,
            createdAt = System.currentTimeMillis() - 86_400_000 * 4,
            updatedAt = System.currentTimeMillis() - 86_400_000 * 3
        )
    )

    val forumReplies = listOf(
        ForumReplyEntity(
            id = "reply_01",
            postId = "forum_01",
            content = "The LIATE rule is simple - pick u in this order: Logarithmic, Inverse trig, Algebraic, Trigonometric, Exponential. The first one you find in your integral becomes u, the rest becomes dv. Practice with examples like ∫x·e^x dx where x is algebraic (u) and e^x is exponential (dv).",
            authorName = "Manish KC",
            authorId = "user_07",
            thumbsUpCount = 8,
            createdAt = System.currentTimeMillis() - 86_400_000 * 2
        ),
        ForumReplyEntity(
            id = "reply_02",
            postId = "forum_01",
            content = "I found it helpful to practice at least 10 problems of each type. Start with simple ones like ∫ln(x)dx and work your way up to harder ones with trig functions.",
            authorName = "Sita Poudel",
            authorId = "user_02",
            thumbsUpCount = 5,
            createdAt = System.currentTimeMillis() - 86_400_000
        ),
        ForumReplyEntity(
            id = "reply_03",
            postId = "forum_02",
            content = "I use reaction maps! Draw a flowchart connecting different functional groups with the reactions that convert between them. It helps you see the big picture instead of memorizing individual reactions.",
            authorName = "Aarav Sharma",
            authorId = "user_01",
            thumbsUpCount = 12,
            createdAt = System.currentTimeMillis() - 86_400_000 * 4
        ),
        ForumReplyEntity(
            id = "reply_04",
            postId = "forum_04",
            content = "Focus on past papers! I gave the exam last year and about 60% of the questions were similar to previous years. Make sure you solve at least 5 years of past papers for each subject.",
            authorName = "Dipesh Maharjan",
            authorId = "user_08",
            thumbsUpCount = 20,
            createdAt = System.currentTimeMillis() - 43_200_000
        ),
        ForumReplyEntity(
            id = "reply_05",
            postId = "forum_03",
            content = "For Kirchhoff's problems: 1) Assign current directions (assume any direction), 2) Pick loops and apply KVL consistently - voltage drops are negative when going through a resistor in the current direction, 3) Set up equations and solve. If you get a negative current, it just means the actual direction is opposite to what you assumed.",
            authorName = "Priya Karki",
            authorId = "user_04",
            thumbsUpCount = 15,
            createdAt = System.currentTimeMillis() - 86_400_000
        )
    )
}
