from django.urls import path

from api.background_agent import mobile_api

urlpatterns = [
    path('pair/start/', mobile_api.pair_start, name='bg_mobile_pair_start'),
    path('pair/token/', mobile_api.pair_token, name='bg_mobile_pair_token'),
    path('me/', mobile_api.me, name='bg_mobile_me'),
    path('revoke/', mobile_api.revoke, name='bg_mobile_revoke'),
    path('state/', mobile_api.state, name='bg_mobile_state'),
    path('repositories/', mobile_api.repositories, name='bg_mobile_repositories'),
    path('branches/', mobile_api.branches, name='bg_mobile_branches'),
    path('projects/', mobile_api.projects, name='bg_mobile_projects'),
    path('projects/<str:project_id>/settings/', mobile_api.project_settings, name='bg_mobile_project_settings'),
    path('sessions/', mobile_api.sessions, name='bg_mobile_sessions'),
    path('sessions/<str:session_id>/', mobile_api.session_detail, name='bg_mobile_session_detail'),
    path('sessions/<str:session_id>/events/', mobile_api.session_events, name='bg_mobile_session_events'),
    path('sessions/<str:session_id>/messages/', mobile_api.session_message, name='bg_mobile_session_message'),
    path('sessions/<str:session_id>/control/', mobile_api.session_control, name='bg_mobile_session_control'),
    path('sessions/<str:session_id>/actions/', mobile_api.session_action, name='bg_mobile_session_action'),
    path('sessions/<str:session_id>/lifecycle/', mobile_api.session_lifecycle, name='bg_mobile_session_lifecycle'),
    path('sessions/<str:session_id>/artifacts/<str:kind>/', mobile_api.artifact, name='bg_mobile_artifact'),
]
