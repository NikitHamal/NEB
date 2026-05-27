package com.neb.ians.data

import com.neb.ians.data.local.ForumThreadEntity
import com.neb.ians.data.local.ResourceEntity
import com.neb.ians.data.model.Grade
import com.neb.ians.data.model.ResourceType
import com.neb.ians.data.model.Subject
import com.neb.ians.data.prefs.UserPrefsRepository
import javax.inject.Inject
import javax.inject.Singleton
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

@Singleton
class Seeder @Inject constructor(
    private val resources: ResourceRepository,
    private val forum: ForumRepository,
    private val prefs: UserPrefsRepository,
    private val scope: CoroutineScope,
) {
    fun bootstrap() {
        scope.launch {
            val seen = prefs.flow.first().seededOnce
            if (seen && resources.count() > 0) return@launch
            if (resources.count() == 0) resources.upsertAll(seedResources())
            if (forum.count() == 0) seedForum().forEach { forum.postThread(it) }
            prefs.markSeeded()
        }
    }

    private fun seedResources(): List<ResourceEntity> = listOf(
        ResourceEntity(
            title = "Physics — Mechanics", author = "NEB",
            description = "Complete chapter notes on kinematics, dynamics, and rotational motion.",
            subject = Subject.Physics, grade = Grade.Grade11, type = ResourceType.Notes,
            pageCount = 124, sizeBytes = 2_400_000,
            sourceUri = "asset://samples/physics_mechanics.pdf",
        ),
        ResourceEntity(
            title = "Chemistry Textbook", author = "Pioneer Publication",
            description = "Reference textbook covering inorganic, organic, and physical chemistry.",
            subject = Subject.Chemistry, grade = Grade.Grade12, type = ResourceType.Textbook,
            pageCount = 412, sizeBytes = 18_000_000,
            sourceUri = "asset://samples/chemistry_textbook.pdf",
        ),
        ResourceEntity(
            title = "Mathematics Past Papers — 2076 to 2080", author = "NEB",
            description = "Solved + unsolved past papers, with marking schemes where available.",
            subject = Subject.Mathematics, grade = Grade.Grade12, type = ResourceType.PastPapers,
            pageCount = 98, sizeBytes = 1_800_000,
            sourceUri = "asset://samples/maths_past_papers.pdf",
        ),
        ResourceEntity(
            title = "Biology — Cell Biology Notes", author = "Buddha Acad.",
            description = "Cells, organelles, mitosis, meiosis. Diagram-heavy.",
            subject = Subject.Biology, grade = Grade.Grade11, type = ResourceType.Notes,
            pageCount = 84, sizeBytes = 3_100_000,
            sourceUri = "asset://samples/biology_cells.pdf",
        ),
        ResourceEntity(
            title = "English Grammar Practice Book", author = "Asmita",
            description = "Tense, voice, narration, transformation. With exercises.",
            subject = Subject.English, grade = Grade.Grade11, type = ResourceType.Ebook,
            pageCount = 220, sizeBytes = 6_500_000,
            sourceUri = "asset://samples/english_grammar.pdf",
        ),
        ResourceEntity(
            title = "Nepali Sahitya Sanchayan", author = "NEB",
            description = "Prescribed Nepali literature anthology for Grade 12.",
            subject = Subject.Nepali, grade = Grade.Grade12, type = ResourceType.Textbook,
            pageCount = 360, sizeBytes = 12_000_000,
            sourceUri = "asset://samples/nepali_anthology.pdf",
        ),
        ResourceEntity(
            title = "Computer Science — Programming in C", author = "Pioneer",
            description = "Variables, control flow, functions, pointers, file I/O.",
            subject = Subject.ComputerScience, grade = Grade.Grade12, type = ResourceType.Ebook,
            pageCount = 290, sizeBytes = 9_400_000,
            sourceUri = "asset://samples/cs_c_programming.pdf",
        ),
        ResourceEntity(
            title = "Accountancy — Final Accounts", author = "Asmita",
            description = "Trading account, P&L, balance sheet with adjustments.",
            subject = Subject.Accountancy, grade = Grade.Grade12, type = ResourceType.Notes,
            pageCount = 70, sizeBytes = 1_400_000,
            sourceUri = "asset://samples/accounts_finals.pdf",
        ),
        ResourceEntity(
            title = "Economics — Microeconomic Theory", author = "Sukunda",
            description = "Demand, supply, elasticity, market structure.",
            subject = Subject.Economics, grade = Grade.Grade11, type = ResourceType.Textbook,
            pageCount = 240, sizeBytes = 7_800_000,
            sourceUri = "asset://samples/economics_micro.pdf",
        ),
        ResourceEntity(
            title = "SEE Compulsory Math — Solutions", author = "NEB",
            description = "Step-by-step solutions to SEE compulsory mathematics.",
            subject = Subject.Mathematics, grade = Grade.SEE, type = ResourceType.Solution,
            pageCount = 132, sizeBytes = 2_900_000,
            sourceUri = "asset://samples/see_math_solutions.pdf",
        ),
    )

    private fun seedForum(): List<ForumThreadEntity> = listOf(
        ForumThreadEntity(
            title = "How are you preparing for the math board exam?",
            body = "I've been doing 5 past papers a week. Any tips on time management for trigonometry?",
            author = "Aakriti",
            tags = "math,grade-12,boards",
        ),
        ForumThreadEntity(
            title = "Best free PDF for Chemistry — Grade 11?",
            body = "Looking for organic chemistry reference. Sharing here once I find something good.",
            author = "Rohit",
            tags = "chemistry,grade-11,resources",
        ),
        ForumThreadEntity(
            title = "Tips for Nepali essay writing",
            body = "Struggling with structure. How do you outline before writing?",
            author = "Sneha",
            tags = "nepali,writing,exam-tips",
        ),
    )
}
