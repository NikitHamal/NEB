from django.http import JsonResponse
from django.views.decorators.http import require_GET
from web.interactive import get_all_courses, get_course, get_lesson, get_courses_by_category, get_stats


@require_GET
def interactive_categories(request):
    cats = get_courses_by_category()
    return JsonResponse({
        'categories': [
            {
                'key': c['key'],
                'label': c['label'],
                'icon': c['icon'],
                'color': c['color'],
                'blurb': c['blurb'],
                'courses': [
                    {
                        'slug': course['slug'],
                        'title': course['title'],
                        'category': course['category'],
                        'ageRange': course.get('age_range', ''),
                        'level': course.get('level', ''),
                        'icon': course.get('icon', ''),
                        'color': course.get('color', ''),
                        'tagline': course.get('tagline', ''),
                        'lessonCount': course.get('lesson_count', 0),
                        'totalMinutes': course.get('total_minutes', 0),
                    }
                    for course in c.get('courses', [])
                ],
            }
            for c in cats
        ]
    })


@require_GET
def interactive_courses_list(request):
    courses = get_all_courses()
    return JsonResponse({
        'courses': [
            {
                'slug': c['slug'],
                'title': c['title'],
                'category': c['category'],
                'categoryLabel': c.get('category_label', ''),
                'ageRange': c.get('age_range', ''),
                'level': c.get('level', ''),
                'icon': c.get('icon', ''),
                'color': c.get('color', ''),
                'tagline': c.get('tagline', ''),
                'description': c.get('description', ''),
                'skills': c.get('skills', []),
                'lessonCount': c.get('lesson_count', 0),
                'totalMinutes': c.get('total_minutes', 0),
            }
            for c in courses
        ]
    })


@require_GET
def interactive_course_detail(request, course_slug):
    course = get_course(course_slug)
    if not course:
        return JsonResponse({'error': 'Course not found'}, status=404)
    lessons = [
        {
            'slug': l['slug'],
            'title': l['title'],
            'icon': l.get('icon', ''),
            'minutes': l.get('minutes', 0),
            'simType': l.get('sim_type', ''),
            'summary': l.get('summary', ''),
            'objectives': l.get('objectives', []),
        }
        for l in course.get('lessons', [])
    ]
    return JsonResponse({
        'slug': course['slug'],
        'title': course['title'],
        'category': course['category'],
        'categoryLabel': course.get('category_label', ''),
        'ageRange': course.get('age_range', ''),
        'level': course.get('level', ''),
        'icon': course.get('icon', ''),
        'color': course.get('color', ''),
        'tagline': course.get('tagline', ''),
        'description': course.get('description', ''),
        'skills': course.get('skills', []),
        'lessons': lessons,
        'lessonCount': course.get('lesson_count', 0),
        'totalMinutes': course.get('total_minutes', 0),
    })


@require_GET
def interactive_lesson_detail(request, course_slug, lesson_slug):
    result = get_lesson(course_slug, lesson_slug)
    course, lesson, prev_lesson, next_lesson = result
    if not lesson:
        return JsonResponse({'error': 'Lesson not found'}, status=404)

    def _lesson_summary(l):
        if not l:
            return None
        return {
            'slug': l['slug'],
            'title': l['title'],
            'icon': l.get('icon', ''),
            'minutes': l.get('minutes', 0),
            'simType': l.get('sim_type', ''),
        }

    return JsonResponse({
        'course': {
            'slug': course['slug'],
            'title': course['title'],
            'category': course['category'],
            'icon': course.get('icon', ''),
            'color': course.get('color', ''),
            'lessonCount': course.get('lesson_count', 0),
        },
        'lesson': {
            'slug': lesson['slug'],
            'title': lesson['title'],
            'icon': lesson.get('icon', ''),
            'minutes': lesson.get('minutes', 0),
            'simType': lesson.get('sim_type', ''),
            'sim': lesson.get('sim', ''),
            'summary': lesson.get('summary', ''),
            'objectives': lesson.get('objectives', []),
            'knowledge': lesson.get('knowledge', []),
            'funFact': lesson.get('fun_fact', ''),
            'quiz': [
                {
                    'q': q['q'],
                    'options': q['options'],
                    'answer': q['answer'],
                    'explain': q.get('explain', ''),
                }
                for q in lesson.get('quiz', [])
            ],
        },
        'prevLesson': _lesson_summary(prev_lesson),
        'nextLesson': _lesson_summary(next_lesson),
        'lessonIndex': course.get('lessons', []).index(lesson) + 1 if lesson in course.get('lessons', []) else 0,
        'totalLessons': course.get('lesson_count', 0),
    })


@require_GET
def interactive_stats(request):
    stats = get_stats()
    return JsonResponse(stats)