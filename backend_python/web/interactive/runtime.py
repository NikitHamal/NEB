"""Thin view-facing helpers for the Interactive learning runtime.

Keeps Django view functions small and centralises the course/lesson context
shape used by templates.
"""
from . import CATEGORY_MAP, get_course, get_lesson


def build_course_context(course_slug):
    """Return the context payload for a course page, or ``None`` if missing."""
    course = get_course(course_slug)
    if not course:
        return None
    return {
        'course': course,
        'category': CATEGORY_MAP.get(course.get('category')),
    }


def build_lesson_context(course_slug, lesson_slug):
    """Return the context payload for a lesson page, or ``None`` if missing."""
    course, lesson, prev_lesson, next_lesson = get_lesson(course_slug, lesson_slug)
    if not course or not lesson:
        return None
    lesson_index = next(i for i, item in enumerate(course['lessons']) if item['slug'] == lesson_slug)
    return {
        'course': course,
        'lesson': lesson,
        'lesson_index': lesson_index,
        'lesson_number': lesson_index + 1,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'sim_static_path': 'web/js/interactive/%s.js' % lesson['sim'],
        'category': CATEGORY_MAP.get(course.get('category')),
    }
