"""Interactive learning hub: courses, lessons, simulations."""
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET

from .view_helpers import *  # noqa: F401,F403
from . import interactive as interactive_catalog


def interactive_hub(request):
    return redirect('/library/?tab=interactive')


@require_GET
@cache_page(60 * 15)  # cache for 15 minutes — catalog is static between deploys
def interactive_catalog_json(request):
    """JSON catalog for the Android app.

    Returns a list of category objects, each with a ``courses`` array.
    Each course includes lightweight fields suitable for list display plus a
    ``lessons`` array with per-lesson metadata.  Heavy fields (objectives,
    knowledge panels, quiz questions) are omitted to keep the payload small.
    """
    categories = []
    for cat in interactive_catalog.get_courses_by_category():
        course_list = []
        for course in cat.get('courses', []):
            lessons = []
            for lesson in course.get('lessons', []):
                lessons.append({
                    'slug': lesson.get('slug', ''),
                    'title': lesson.get('title', ''),
                    'icon': lesson.get('icon', ''),
                    'minutes': lesson.get('minutes', 0),
                    'sim_type': lesson.get('sim_type', '2d'),
                    'summary': lesson.get('summary', ''),
                })
            course_list.append({
                'slug': course.get('slug', ''),
                'title': course.get('title', ''),
                'category': course.get('category', ''),
                'category_label': course.get('category_label', ''),
                'level': course.get('level', ''),
                'icon': course.get('icon', ''),
                'color': course.get('color', '#004ac6'),
                'tagline': course.get('tagline', ''),
                'age_range': course.get('age_range', ''),
                'lesson_count': course.get('lesson_count', len(lessons)),
                'total_minutes': course.get('total_minutes', 0),
                'lessons': lessons,
            })
        categories.append({
            'key': cat.get('key', ''),
            'label': cat.get('label', ''),
            'icon': cat.get('icon', ''),
            'color': cat.get('color', '#004ac6'),
            'blurb': cat.get('blurb', ''),
            'courses': course_list,
        })
    return JsonResponse({'categories': categories}, json_dumps_params={'ensure_ascii': False})


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
    # Optional 3D companion module. When a lesson declares ``sim_3d`` the learner
    # gets a 2D/3D switch in the simulation toolbar (the 2D view is never removed).
    sim_3d = lesson.get('sim_3d')
    return render(request, 'web/interactive/lesson.html', _ctx(request,
        course=course,
        lesson=lesson,
        lesson_index=lesson_index,
        lesson_number=lesson_index + 1,
        prev_lesson=prev_lesson,
        next_lesson=next_lesson,
        sim_static_path='web/js/interactive/%s.js' % lesson['sim'],
        sim_3d_static_path=('web/js/interactive/%s.js' % sim_3d) if sim_3d else None,
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
