"""Interactive learning hub views."""
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.clickjacking import xframe_options_sameorigin

from .interactive.runtime import build_course_context, build_lesson_context
from .view_helpers import _ctx


def interactive_hub(request):
    return redirect('/library/?tab=interactive')


def interactive_course(request, course_slug):
    context = build_course_context(course_slug)
    if not context:
        raise Http404('Course not found')
    return render(request, 'web/interactive/course.html', _ctx(request, **context))


def interactive_lesson(request, course_slug, lesson_slug):
    context = build_lesson_context(course_slug, lesson_slug)
    if not context:
        raise Http404('Lesson not found')
    return render(request, 'web/interactive/lesson.html', _ctx(request, **context))


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
