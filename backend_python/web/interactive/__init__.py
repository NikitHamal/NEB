"""Interactive learning catalog.

Course schema (each module exposes COURSES, a list of dicts):
{
  'slug': str (unique across all catalogs),
  'title': str,
  'category': 'robotics' | 'space' | 'physics' | 'chemistry' | 'biology' | 'ai' | 'coding',
  'age_range': str (e.g. '8-11'),
  'level': 'Beginner' | 'Intermediate' | 'Advanced',
  'icon': str (Material Symbol name),
  'color': str (hex),
  'tagline': str,
  'description': str,
  'skills': [str, ...],
  'lessons': [
    {
      'slug': str (unique within course),
      'title': str,
      'icon': str,
      'minutes': int,
      'sim': str ('<area>/<module-name>' relative to web/js/interactive/, no .js),
      'sim_type': '3d' | 'lab' | 'coding' | '2d',
      'summary': str,
      'objectives': [str, ...],
      'knowledge': [{'heading': str, 'body': str}, ...],
      'fun_fact': str (optional),
      'quiz': [{'q': str, 'options': [str, ...], 'answer': int, 'explain': str}, ...],
    }, ...
  ],
}
"""
from functools import lru_cache

CATEGORIES = [
    {'key': 'robotics', 'label': 'Robotics', 'icon': 'smart_toy', 'color': '#0EA5E9',
     'blurb': 'Build, wire and program virtual robots — from your first motor to inverse kinematics.'},
    {'key': 'space', 'label': 'Space & Astronomy', 'icon': 'rocket_launch', 'color': '#8B5CF6',
     'blurb': 'Fly through the solar system, bend orbits with gravity and explore our galaxy in 3D.'},
    {'key': 'physics', 'label': 'Physics Lab', 'icon': 'science', 'color': '#F59E0B',
     'blurb': 'A virtual physics lab — pendulums, projectiles, waves, optics and circuits you can touch.'},
    {'key': 'chemistry', 'label': 'Chemistry Lab', 'icon': 'experiment', 'color': '#10B981',
     'blurb': 'Build atoms, spin real 3D molecules and run safe virtual experiments.'},
    {'key': 'biology', 'label': 'Biology Lab', 'icon': 'microbiology', 'color': '#84CC16',
     'blurb': 'Peer through a virtual microscope, watch cells divide and explore the living world hands-on.'},
    {'key': 'ai', 'label': 'AI & Machine Learning', 'icon': 'neurology', 'color': '#6366F1',
     'blurb': 'Train neurons, teach machines to see and discover how ChatGPT-style AI really works — by playing with it.'},
    {'key': 'coding', 'label': 'Coding Adventures', 'icon': 'code_blocks', 'color': '#EC4899',
     'blurb': 'Learn HTML, CSS, JavaScript and Python through games, drag-and-drop blocks and friendly guides.'},
]

CATEGORY_MAP = {c['key']: c for c in CATEGORIES}


def _load_catalog_modules():
    from . import (
        catalog_robotics, catalog_space, catalog_physics, catalog_chemistry,
        catalog_neb_physics, catalog_neb_chemistry, catalog_biology, catalog_ai,
        catalog_coding,
    )
    return [
        catalog_robotics, catalog_space, catalog_physics, catalog_chemistry,
        catalog_neb_physics, catalog_neb_chemistry, catalog_biology, catalog_ai,
        catalog_coding,
    ]


@lru_cache(maxsize=1)
def get_all_courses():
    courses = []
    seen = set()
    for mod in _load_catalog_modules():
        for course in getattr(mod, 'COURSES', []):
            slug = course.get('slug')
            if not slug or slug in seen:
                continue
            seen.add(slug)
            cat = CATEGORY_MAP.get(course.get('category'))
            course.setdefault('category_label', cat['label'] if cat else course.get('category', ''))
            course.setdefault('color', cat['color'] if cat else '#004ac6')
            course.setdefault('icon', cat['icon'] if cat else 'school')
            course['lesson_count'] = len(course.get('lessons', []))
            course['total_minutes'] = sum(l.get('minutes', 0) for l in course.get('lessons', []))
            courses.append(course)
    return courses


@lru_cache(maxsize=1)
def get_courses_by_category():
    grouped = []
    all_courses = get_all_courses()
    for cat in CATEGORIES:
        cat_courses = [c for c in all_courses if c.get('category') == cat['key']]
        if cat_courses:
            grouped.append({**cat, 'courses': cat_courses})
    return grouped


def get_course(slug):
    for course in get_all_courses():
        if course['slug'] == slug:
            return course
    return None


def get_lesson(course_slug, lesson_slug):
    course = get_course(course_slug)
    if not course:
        return None, None, None, None
    lessons = course.get('lessons', [])
    for i, lesson in enumerate(lessons):
        if lesson['slug'] == lesson_slug:
            prev_l = lessons[i - 1] if i > 0 else None
            next_l = lessons[i + 1] if i < len(lessons) - 1 else None
            return course, lesson, prev_l, next_l
    return course, None, None, None


def get_stats():
    courses = get_all_courses()
    return {
        'course_count': len(courses),
        'lesson_count': sum(c['lesson_count'] for c in courses),
        'category_count': len({c['category'] for c in courses}),
    }
