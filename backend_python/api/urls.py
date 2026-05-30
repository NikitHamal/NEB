"""
URL patterns for the NEBians API.
All paths are relative to /api/ (prefix added in nebians/urls.py).
"""
from django.urls import path, include
from . import views

urlpatterns = [
    # Auth
    path('auth/google/', views.auth_google, name='auth-google'),

    # Users — profile
    path('users/check-username/', views.check_username, name='check-username'),
    path('users/profile/', views.user_profile_create_or_update, name='profile-create-update'),
    path('users/profile/<str:username>/', views.user_profile_get, name='profile-get'),
    path('users/profile/<str:username>/stats/', views.user_profile_stats, name='profile-stats'),

    # Users — photo history (auth required)
    path('users/me/photos/', views.user_photos, name='user-photos'),
    path('users/me/photos/<int:photo_id>/activate/', views.user_photo_activate, name='user-photo-activate'),

    # Users — follow system
    path('users/<str:user_id>/follow/', views.user_follow_toggle, name='user-follow'),
    path('users/<str:user_id>/followers/', views.user_followers_list, name='user-followers'),
    path('users/<str:user_id>/following/', views.user_following_list, name='user-following'),

    # Resources
    path('resources/', views.resources_list, name='resources-list'),
    path('resources/<str:resource_id>/', views.resource_detail, name='resource-detail'),
    path('resources/<str:resource_id>/view/', views.resource_view, name='resource-view'),

    # Search
    path('search/', views.search_all, name='search-all'),

    # Posts — GET list + POST create handled by posts_endpoint dispatcher
    path('posts/', views.posts_endpoint, name='posts'),
    path('posts/<str:post_id>/', views.post_detail, name='post-detail'),
    path('posts/<str:post_id>/like/', views.post_like, name='post-like'),

    # Replies — GET list + POST create handled by replies_endpoint dispatcher
    path('posts/<str:post_id>/replies/', views.replies_endpoint, name='replies'),

    # Replies
    path('replies/<str:reply_id>/', views.reply_detail, name='reply-detail'),
    path('replies/<str:reply_id>/like/', views.reply_like, name='reply-like'),

    # Edit History
    path('edit-history/<str:target_type>/<str:target_id>/', views.edit_history, name='edit-history'),

    # FCM
    path('fcm/register/', views.fcm_register, name='fcm-register'),

    # Admin API
    path('', include('api.admin_urls')),
]
