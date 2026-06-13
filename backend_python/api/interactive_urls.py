from django.urls import path
from . import interactive_views

urlpatterns = [
    path('categories/', interactive_views.interactive_categories, name='interactive-categories'),
    path('stats/', interactive_views.interactive_stats, name='interactive-stats'),
    path('courses/', interactive_views.interactive_courses_list, name='interactive-courses-list'),
    path('courses/<str:course_slug>/', interactive_views.interactive_course_detail, name='interactive-course-detail'),
    path('courses/<str:course_slug>/<str:lesson_slug>/', interactive_views.interactive_lesson_detail, name='interactive-lesson-detail'),
]