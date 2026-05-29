"""
URL patterns for the NEBians API.
All paths are relative to /api/ (prefix added in nebians/urls.py).
"""
from django.urls import path, include
from . import views

urlpatterns = [
    # Auth
    path('auth/google', views.auth_google, name='auth-google'),

    # Users
    path('users/check-username', views.check_username, name='check-username'),
    path('users/profile', views.user_profile_create_or_update, name='profile-create-update'),
    path('users/profile/<str:username>', views.user_profile_get, name='profile-get'),

    # Resources
    path('resources', views.resources_list, name='resources-list'),

    # Posts — GET list + POST create handled by posts_endpoint dispatcher
    path('posts', views.posts_endpoint, name='posts'),
    path('posts/<str:post_id>', views.post_delete, name='post-delete'),
    path('posts/<str:post_id>/like', views.post_like, name='post-like'),

    # Replies — GET list + POST create handled by replies_endpoint dispatcher
    path('posts/<str:post_id>/replies', views.replies_endpoint, name='replies'),

    # Replies
    path('replies/<str:reply_id>/like', views.reply_like, name='reply-like'),

    # FCM
    path('fcm/register', views.fcm_register, name='fcm-register'),

    # Admin API
    path('', include('api.admin_urls')),
]
