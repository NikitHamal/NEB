package com.neb.ians.data

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.util.UUID

class CommunityRepository(context: Context) {
    private val prefs = context.applicationContext.getSharedPreferences("neb_community", Context.MODE_PRIVATE)

    fun threads(): List<CommunityThread> {
        val stored = prefs.getString(KEY_THREADS, null)
        if (stored.isNullOrBlank()) {
            val seeded = seedThreads()
            saveThreads(seeded)
            return seeded
        }
        return parseThreads(stored)
    }

    fun thread(id: String): CommunityThread? = threads().firstOrNull { it.id == id }

    fun addThread(title: String, body: String, subject: Subject): CommunityThread {
        val thread = CommunityThread(
            id = UUID.randomUUID().toString(),
            title = title.trim(),
            body = body.trim(),
            subject = subject,
            author = "NEBian",
            createdAt = "Just now",
            thumbs = 0,
            answers = emptyList()
        )
        saveThreads(listOf(thread) + threads())
        return thread
    }

    fun addAnswer(threadId: String, body: String) {
        val updated = threads().map { thread ->
            if (thread.id != threadId) return@map thread
            thread.copy(
                answers = thread.answers + CommunityAnswer(
                    id = UUID.randomUUID().toString(),
                    author = "NEBian",
                    body = body.trim(),
                    createdAt = "Just now",
                    thumbs = 0
                )
            )
        }
        saveThreads(updated)
    }

    fun thumbThread(threadId: String) {
        saveThreads(threads().map { if (it.id == threadId) it.copy(thumbs = it.thumbs + 1) else it })
    }

    fun thumbAnswer(threadId: String, answerId: String) {
        saveThreads(
            threads().map { thread ->
                if (thread.id != threadId) return@map thread
                thread.copy(
                    answers = thread.answers.map { answer ->
                        if (answer.id == answerId) answer.copy(thumbs = answer.thumbs + 1) else answer
                    }
                )
            }
        )
    }

    private fun saveThreads(threads: List<CommunityThread>) {
        prefs.edit().putString(KEY_THREADS, threadsToJson(threads).toString()).apply()
    }

    private fun parseThreads(raw: String): List<CommunityThread> {
        val array = JSONArray(raw)
        return buildList {
            for (index in 0 until array.length()) {
                val item = array.getJSONObject(index)
                val answersArray = item.optJSONArray("answers") ?: JSONArray()
                val answers = buildList {
                    for (answerIndex in 0 until answersArray.length()) {
                        val answer = answersArray.getJSONObject(answerIndex)
                        add(
                            CommunityAnswer(
                                id = answer.getString("id"),
                                author = answer.getString("author"),
                                body = answer.getString("body"),
                                createdAt = answer.getString("createdAt"),
                                thumbs = answer.optInt("thumbs")
                            )
                        )
                    }
                }
                add(
                    CommunityThread(
                        id = item.getString("id"),
                        title = item.getString("title"),
                        body = item.getString("body"),
                        subject = Subject.valueOf(item.getString("subject")),
                        author = item.getString("author"),
                        createdAt = item.getString("createdAt"),
                        thumbs = item.optInt("thumbs"),
                        answers = answers
                    )
                )
            }
        }
    }

    private fun seedThreads(): List<CommunityThread> = listOf(
        CommunityThread(
            id = "seed-physics-vector",
            title = "How do I resolve vectors quickly in Physics?",
            body = "I understand components but lose marks when questions mix angles and signs.",
            subject = Subject.Physics,
            author = "Aarav",
            createdAt = "2h ago",
            thumbs = 12,
            answers = listOf(
                CommunityAnswer(
                    id = "seed-answer-vector",
                    author = "Samiksha",
                    body = "Draw axes first, mark the angle from the positive axis, then write x = r cos theta and y = r sin theta before substituting values.",
                    createdAt = "1h ago",
                    thumbs = 18
                )
            )
        ),
        CommunityThread(
            id = "seed-chemistry-mole",
            title = "Best way to revise mole concept numericals?",
            body = "Should I memorize formulas or solve past paper patterns first?",
            subject = Subject.Chemistry,
            author = "Nisha",
            createdAt = "Yesterday",
            thumbs = 9,
            answers = listOf(
                CommunityAnswer(
                    id = "seed-answer-mole",
                    author = "Rabin",
                    body = "Start with unit conversion and balanced equation questions. After that, past paper patterns become much easier.",
                    createdAt = "Yesterday",
                    thumbs = 11
                )
            )
        )
    )

    private fun threadsToJson(threads: List<CommunityThread>): JSONArray {
        val array = JSONArray()
        threads.forEach { thread ->
            array.put(
                JSONObject()
                    .put("id", thread.id)
                    .put("title", thread.title)
                    .put("body", thread.body)
                    .put("subject", thread.subject.name)
                    .put("author", thread.author)
                    .put("createdAt", thread.createdAt)
                    .put("thumbs", thread.thumbs)
                    .put("answers", answersToJson(thread.answers))
            )
        }
        return array
    }

    private fun answersToJson(answers: List<CommunityAnswer>): JSONArray {
        val array = JSONArray()
        answers.forEach { answer ->
            array.put(
                JSONObject()
                    .put("id", answer.id)
                    .put("author", answer.author)
                    .put("body", answer.body)
                    .put("createdAt", answer.createdAt)
                    .put("thumbs", answer.thumbs)
            )
        }
        return array
    }

    companion object {
        private const val KEY_THREADS = "threads"
    }
}
