"""Interactive learning hub: courses, lessons, simulations."""
from django.views.decorators.clickjacking import xframe_options_sameorigin

from .view_helpers import *  # noqa: F401,F403
from . import interactive as interactive_catalog


def interactive_hub(request):
    return redirect('/library/?tab=interactive')


def interactive_course(request, course_slug):
    course = interactive_catalog.get_course(course_slug)
    if not course:
        raise Http404('Course not found')
    return render(request, 'web/interactive/course.html', _ctx(request,
        course=course,
        category=interactive_catalog.CATEGORY_MAP.get(course['category']),
    ))


def interactive_lesson(request, course_slug, lesson_slug):
    course, lesson, prev_lesson, next_lesson = interactive_catalog.get_lesson(course_slug, lesson_slug)
    if not course or not lesson:
        raise Http404('Lesson not found')
    lesson_index = next(i for i, l in enumerate(course['lessons']) if l['slug'] == lesson_slug)
    return render(request, 'web/interactive/lesson.html', _ctx(request,
        course=course,
        lesson=lesson,
        lesson_index=lesson_index,
        lesson_number=lesson_index + 1,
        prev_lesson=prev_lesson,
        next_lesson=next_lesson,
        sim_static_path='web/js/interactive/%s.js' % lesson['sim'],
        category=interactive_catalog.CATEGORY_MAP.get(course['category']),
    ))


@xframe_options_sameorigin
def interactive_sandbox_frame(request):
    response = render(request, 'web/interactive/sandbox_frame.html')
    response['Content-Security-Policy'] = (
        "default-src 'none'; "
        "script-src 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'unsafe-inline'; "
        "img-src data: blob: https:; "
        "frame-ancestors 'self'"
    )
    return response
