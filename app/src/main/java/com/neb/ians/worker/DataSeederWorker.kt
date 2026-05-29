package com.neb.ians.worker

import android.content.Context
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.neb.ians.data.local.dao.ForumDao
import com.neb.ians.data.local.dao.ResourceDao
import com.neb.ians.data.local.entity.ForumPostEntity
import com.neb.ians.data.local.entity.ForumReplyEntity
import com.neb.ians.data.local.entity.ResourceEntity
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject
import kotlinx.coroutines.flow.first

@HiltWorker
class DataSeederWorker @AssistedInject constructor(
    @Assisted private val context: Context,
    @Assisted workerParams: WorkerParameters,
    private val resourceDao: ResourceDao,
    private val forumDao: ForumDao
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        val existingResources = resourceDao.getAll().first()
        if (existingResources.isNotEmpty()) {
            return Result.success()
        }

        val now = System.currentTimeMillis()
        val dayMs = 86400000L

        val resources = listOf(
            ResourceEntity(
                id = "res-physics-11-textbook",
                title = "Physics Grade 11 Textbook",
                description = "Complete NEB Physics textbook for Grade 11 covering mechanics, thermodynamics, and optics.",
                subject = "Physics",
                gradeLevel = "Grade 11",
                type = "Textbook",
                fileUrl = "",
                thumbnailUrl = "",
                fileSize = 0,
                addedAt = now - 30 * dayMs,
                viewCount = 245
            ),
            ResourceEntity(
                id = "res-chemistry-11-notes",
                title = "Chemistry Grade 11 Notes",
                description = "Comprehensive notes for NEB Chemistry Grade 11 including organic and inorganic chemistry.",
                subject = "Chemistry",
                gradeLevel = "Grade 11",
                type = "Notes",
                fileUrl = "",
                thumbnailUrl = "",
                fileSize = 0,
                addedAt = now - 25 * dayMs,
                viewCount = 189
            ),
            ResourceEntity(
                id = "res-math-12-guide",
                title = "Mathematics Grade 12 Guide",
                description = "Step-by-step guide for NEB Mathematics Grade 12 with solved examples.",
                subject = "Mathematics",
                gradeLevel = "Grade 12",
                type = "Guide",
                fileUrl = "",
                thumbnailUrl = "",
                fileSize = 0,
                addedAt = now - 20 * dayMs,
                viewCount = 312
            ),
            ResourceEntity(
                id = "res-biology-11-pastpapers",
                title = "Biology Grade 11 Past Papers",
                description = "Collection of NEB Biology past papers from 2075 to 2080 with model answers.",
                subject = "Biology",
                gradeLevel = "Grade 11",
                type = "Past Papers",
                fileUrl = "",
                thumbnailUrl = "",
                fileSize = 0,
                addedAt = now - 15 * dayMs,
                viewCount = 156
            ),
            ResourceEntity(
                id = "res-english-12-solution",
                title = "English Grade 12 Solution",
                description = "Complete solutions for NEB English Grade 12 textbook exercises.",
                subject = "English",
                gradeLevel = "Grade 12",
                type = "Solution",
                fileUrl = "",
                thumbnailUrl = "",
                fileSize = 0,
                addedAt = now - 10 * dayMs,
                viewCount = 98
            ),
            ResourceEntity(
                id = "res-cs-11-notes",
                title = "Computer Science Grade 11 Notes",
                description = "Detailed notes covering programming concepts, databases, and networking for NEB CS Grade 11.",
                subject = "Computer Science",
                gradeLevel = "Grade 11",
                type = "Notes",
                fileUrl = "",
                thumbnailUrl = "",
                fileSize = 0,
                addedAt = now - 5 * dayMs,
                viewCount = 134
            ),
            ResourceEntity(
                id = "res-physics-12-pastpapers",
                title = "Physics Grade 12 Past Papers",
                description = "NEB Physics Grade 12 past papers with solutions.",
                subject = "Physics",
                gradeLevel = "Grade 12",
                type = "Past Papers",
                fileUrl = "",
                thumbnailUrl = "",
                fileSize = 0,
                addedAt = now - 3 * dayMs,
                viewCount = 278
            ),
            ResourceEntity(
                id = "res-nepali-11-textbook",
                title = "Nepali Grade 11 Textbook",
                description = "NEB Nepali textbook for Grade 11 covering literature, grammar, and composition.",
                subject = "Nepali",
                gradeLevel = "Grade 11",
                type = "Textbook",
                fileUrl = "",
                thumbnailUrl = "",
                fileSize = 0,
                addedAt = now - 2 * dayMs,
                viewCount = 67
            ),
            ResourceEntity(
                id = "res-economics-12-guide",
                title = "Economics Grade 12 Guide",
                description = "Comprehensive guide for NEB Economics Grade 12 with diagrams and charts.",
                subject = "Economics",
                gradeLevel = "Grade 12",
                type = "Guide",
                fileUrl = "",
                thumbnailUrl = "",
                fileSize = 0,
                addedAt = now - 1 * dayMs,
                viewCount = 45
            ),
            ResourceEntity(
                id = "res-math-11-textbook",
                title = "Mathematics Grade 11 Textbook",
                description = "Complete NEB Mathematics textbook for Grade 11.",
                subject = "Mathematics",
                gradeLevel = "Grade 11",
                type = "Textbook",
                fileUrl = "",
                thumbnailUrl = "",
                fileSize = 0,
                addedAt = now,
                viewCount = 201
            )
        )

        resourceDao.insertAll(resources)

        val existingPosts = forumDao.getAllPosts().first()
        if (existingPosts.isNotEmpty()) {
            return Result.success()
        }

        val posts = listOf(
            ForumPostEntity(
                id = "post-1",
                title = "How to solve projectile motion problems?",
                content = "I'm having trouble understanding projectile motion in Physics. Can someone explain the key formulas and how to approach numerical problems? Especially the ones involving range and maximum height.",
                authorName = "Suman Sharma",
                authorId = "user-1",
                category = "Physics",
                thumbsUpCount = 12,
                replyCount = 3,
                createdAt = now - 7 * dayMs,
                updatedAt = now - 7 * dayMs,
                isThumbedUp = false
            ),
            ForumPostEntity(
                id = "post-2",
                title = "Best reference books for Chemistry Grade 12?",
                content = "Which reference books do you recommend for NEB Chemistry Grade 12? I'm looking for books with good numerical problems and clear explanations of organic chemistry reactions.",
                authorName = "Priya Thapa",
                authorId = "user-2",
                category = "Chemistry",
                thumbsUpCount = 8,
                replyCount = 2,
                createdAt = now - 5 * dayMs,
                updatedAt = now - 5 * dayMs,
                isThumbedUp = false
            ),
            ForumPostEntity(
                id = "post-3",
                title = "Tips for NEB exam preparation",
                content = "Share your best study tips for NEB exams! How do you manage time between multiple subjects? What's your revision strategy?",
                authorName = "Rajesh KC",
                authorId = "user-3",
                category = "Exam Tips",
                thumbsUpCount = 25,
                replyCount = 5,
                createdAt = now - 3 * dayMs,
                updatedAt = now - 3 * dayMs,
                isThumbedUp = false
            ),
            ForumPostEntity(
                id = "post-4",
                title = "Organic chemistry reaction mechanisms",
                content = "Can someone explain SN1 and SN2 reaction mechanisms with examples? I always get confused between the two.",
                authorName = "Anita Gurung",
                authorId = "user-4",
                category = "Chemistry",
                thumbsUpCount = 6,
                replyCount = 1,
                createdAt = now - 2 * dayMs,
                updatedAt = now - 2 * dayMs,
                isThumbedUp = false
            ),
            ForumPostEntity(
                id = "post-5",
                title = "Integration techniques for Grade 12",
                content = "What are the most important integration techniques for NEB Mathematics Grade 12? I need help with integration by parts and substitution methods.",
                authorName = "Bikash Adhikari",
                authorId = "user-5",
                category = "Mathematics",
                thumbsUpCount = 10,
                replyCount = 2,
                createdAt = now - 1 * dayMs,
                updatedAt = now - 1 * dayMs,
                isThumbedUp = false
            ),
            ForumPostEntity(
                id = "post-6",
                title = "How to write effective exam answers?",
                content = "What format and structure do you follow for writing NEB exam answers? How much should we write for 5-mark and 10-mark questions?",
                authorName = "Maya Tamang",
                authorId = "user-6",
                category = "Exam Tips",
                thumbsUpCount = 15,
                replyCount = 4,
                createdAt = now,
                updatedAt = now,
                isThumbedUp = false
            )
        )

        for (post in posts) {
            forumDao.insertPost(post)
        }

        val replies = listOf(
            ForumReplyEntity(
                id = "reply-1-1",
                postId = "post-1",
                content = "The key formulas are: Range = v²sin(2θ)/g, Max Height = v²sin²(θ)/2g, Time of Flight = 2vsin(θ)/g. Always draw a diagram first!",
                authorName = "Dipak Poudel",
                authorId = "user-7",
                thumbsUpCount = 5,
                createdAt = now - 6 * dayMs,
                isThumbedUp = false
            ),
            ForumReplyEntity(
                id = "reply-1-2",
                content = "Remember that horizontal and vertical motions are independent. Split the initial velocity into components first.",
                authorName = "Sita Basnet",
                authorId = "user-8",
                thumbsUpCount = 3,
                createdAt = now - 5 * dayMs,
                isThumbedUp = false
            ),
            ForumReplyEntity(
                id = "reply-1-3",
                content = "Practice with past NEB questions - they usually follow a pattern. The angle of 45° gives maximum range.",
                authorName = "Hari Magar",
                authorId = "user-9",
                thumbsUpCount = 4,
                createdAt = now - 4 * dayMs,
                isThumbedUp = false
            ),
            ForumReplyEntity(
                id = "reply-2-1",
                content = "I recommend 'A Textbook of Chemistry' by Stha and 'Fundamentals of Chemistry' for Grade 12. Both have excellent numerical problems.",
                authorName = "Krishna Rai",
                authorId = "user-10",
                thumbsUpCount = 4,
                createdAt = now - 4 * dayMs,
                isThumbedUp = false
            ),
            ForumReplyEntity(
                id = "reply-3-1",
                content = "Start with the hardest subject first when your mind is fresh. Take 10-minute breaks every hour. Make flashcards for formulas.",
                authorName = "Nabin Shrestha",
                authorId = "user-11",
                thumbsUpCount = 8,
                createdAt = now - 2 * dayMs,
                isThumbedUp = false
            )
        )

        for (reply in replies) {
            forumDao.insertReply(reply)
        }

        return Result.success()
    }
}