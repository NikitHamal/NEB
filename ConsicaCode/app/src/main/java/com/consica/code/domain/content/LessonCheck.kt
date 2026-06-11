package com.consica.code.domain.content

/** Pure, offline lesson-solution check. Substring matching keeps validation simple & local. */
object LessonCheck {

    /** True when every success needle appears in the relevant haystack (code or output). */
    fun passes(lesson: Lesson, code: String, output: String): Boolean {
        if (lesson.successNeedles.isEmpty()) return true
        val haystack = when (lesson.validateOn) {
            ValidateOn.CODE -> code
            ValidateOn.OUTPUT -> output
        }.lowercase()
        return lesson.successNeedles.all { haystack.contains(it.lowercase()) }
    }
}
