package com.agentx.app.util

object FuzzyMatch {
    fun normalize(input: String): String {
        val out = StringBuilder(input.length)
        for (ch in input.lowercase()) {
            if (ch.isLetterOrDigit()) out.append(ch)
        }
        return out.toString()
    }

    fun score(query: String, target: String): Int {
        val q = normalize(query)
        val t = normalize(target)
        if (q.isEmpty() || t.isEmpty()) return 0
        if (q == t) return 1000
        var points = 0
        if (t.startsWith(q)) points += 300
        if (t.contains(q)) points += 200
        val qTokens = q.split(' ').filter { it.length > 1 }
        val tTokens = t.split(' ').filter { it.isNotEmpty() }
        var overlap = 0
        for (qt in qTokens) {
            for (tt in tTokens) {
                if (tt == qt) {
                    overlap += 2
                    break
                }
                if (tt.startsWith(qt) || qt.startsWith(tt)) {
                    overlap += 1
                    break
                }
            }
        }
        points += overlap * 60
        if (q.length >= 3 && t.contains(q.take(3))) points += 10
        return points
    }

    data class Scored<T>(val item: T, val score: Int)

    fun <T> rank(query: String, candidates: List<T>, labelOf: (T) -> String, limit: Int = 5): List<Scored<T>> {
        return candidates
            .map { Scored(it, score(query, labelOf(it))) }
            .filter { it.score > 0 }
            .sortedByDescending { it.score }
            .take(limit)
    }
}
