from django.urls import path

from . import views

app_name = 'coding_agent'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('projects/new/', views.project_new, name='project_new'),
    path('projects/<str:project_id>/', views.project_detail, name='project_detail'),
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/<str:session_id>/', views.session_detail, name='session_detail'),

    path('oauth/github/', views.github_oauth_start, name='github_oauth_start'),
    path('oauth/github/callback/', views.github_oauth_callback, name='github_oauth_callback'),

    path('ajax/github/repos/', views.ajax_github_repos, name='ajax_github_repos'),
    path('ajax/projects/create/', views.ajax_project_create, name='ajax_project_create'),
    path('ajax/projects/<str:project_id>/refresh/', views.ajax_project_refresh, name='ajax_project_refresh'),
    path('ajax/projects/<str:project_id>/delete/', views.ajax_project_delete, name='ajax_project_delete'),

    path('ajax/sessions/create/', views.ajax_session_create, name='ajax_session_create'),
    path('ajax/sessions/<str:session_id>/message/', views.ajax_session_message, name='ajax_session_message'),
    path('ajax/sessions/<str:session_id>/control/', views.ajax_session_control, name='ajax_session_control'),
    path('ajax/sessions/<str:session_id>/resume-text/', views.ajax_session_resume, name='ajax_session_resume'),
    path('ajax/sessions/<str:session_id>/files/', views.ajax_session_files, name='ajax_session_files'),
    path('ajax/sessions/<str:session_id>/diff/', views.ajax_session_diff, name='ajax_session_diff'),
    path('ajax/sessions/<str:session_id>/download/', views.ajax_session_download, name='ajax_session_download'),
    path('ajax/sessions/<str:session_id>/push/', views.ajax_session_push, name='ajax_session_push'),
    path('ajax/sessions/<str:session_id>/pr/', views.ajax_session_open_pr, name='ajax_session_open_pr'),
]
