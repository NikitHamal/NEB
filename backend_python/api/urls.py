"""
URL patterns for the NEBians API.
All paths are relative to /api/ (prefix added in nebians/urls.py).
"""
from django.urls import path, include
from . import views
from . import views_presence
from . import pdf_assistant_views

urlpatterns = [
    # Auth
    path('auth/google/', views.auth_google, name='auth-google'),
    path('auth/github/', views.auth_github, name='auth-github'),
    path('auth/email/signup/', views.auth_email_signup, name='auth-email-signup'),
    path('auth/email/verify/', views.auth_email_verify, name='auth-email-verify'),
    path('auth/email/resend/', views.auth_email_resend, name='auth-email-resend'),
    path('auth/email/login/', views.auth_email_login, name='auth-email-login'),
    path('auth/email/forgot/', views.auth_email_forgot, name='auth-email-forgot'),
    path('auth/email/reset-password/', views.auth_email_reset_password, name='auth-email-reset-password'),
    path('auth/set-password/', views.auth_set_password, name='auth-set-password'),
    path('auth/change-password/', views.auth_change_password, name='auth-change-password'),
    path('auth/logout/', views.auth_logout, name='auth-logout'),

    # Users — profile
    path('users/check-username/', views.check_username, name='check-username'),
    path('users/profile/', views.user_profile_create_or_update, name='profile-create-update'),
    path('users/profile/<str:username>/', views.user_profile_get, name='profile-get'),
    path('users/profile/<str:username>/stats/', views.user_profile_stats, name='profile-stats'),
    path('users/institutions/', views.institutions_list, name='institutions-list'),

    # Users — photo history (auth required)
    path('users/me/photos/', views.user_photos, name='user-photos'),
    path('users/me/analytics/', views.user_private_analytics, name='user-private-analytics'),
    path('users/me/photos/<int:photo_id>/activate/', views.user_photo_activate, name='user-photo-activate'),
    path('users/me/delete-account/', views.user_delete_account_request, name='user-delete-account-request'),

    # Users — follow system
    path('users/me/follow-requests/', views.user_follow_requests_list, name='user-follow-requests'),
    path('users/follow-requests/<str:request_id>/accept/', views.user_follow_request_accept, name='user-follow-request-accept'),
    path('users/follow-requests/<str:request_id>/reject/', views.user_follow_request_reject, name='user-follow-request-reject'),
    path('users/<str:user_id>/follow/', views.user_follow_toggle, name='user-follow'),
    path('users/<str:user_id>/followers/', views.user_followers_list, name='user-followers'),
    path('users/<str:user_id>/following/', views.user_following_list, name='user-following'),

    # Resources
    path('resources/upload/', views.resource_upload, name='resource-upload'),
    path('resources/upload/anonymous/', views.resource_upload_anonymous, name='resource-upload-anonymous'),
    path('resources/', views.resources_list, name='resources-list'),
    path('resources/<str:resource_id>/', views.resource_detail, name='resource-detail'),
    path('resources/<str:resource_id>/view/', views.resource_view, name='resource-view'),
    path('resources/<str:resource_id>/like/', views.resource_like, name='resource-like'),
    path('resources/<str:resource_id>/comments/', views.resource_comments, name='resource-comments'),
    path('resources/<str:resource_id>/comments/<str:comment_id>/', views.resource_comment_detail, name='resource-comment-detail'),
    path('resources/<str:resource_id>/comments/<str:comment_id>/like/', views.resource_comment_like, name='resource-comment-like'),
    path('resources/<str:resource_id>/purchase/', views.resource_purchase, name='resource-purchase'),
    path('resources/<str:resource_id>/pdf-assistant/', pdf_assistant_views.resource_pdf_assistant, name='resource-pdf-assistant'),

    # Syllabus categories for native apps
    path('syllabus/categories/', views.syllabus_categories, name='syllabus-categories'),
    path('syllabus/subjects/<str:grade_slug>/<str:subject_slug>/', views.syllabus_subject_detail, name='syllabus-subject-detail'),

    # Resource Requests
    path('resource-requests/', views.resource_requests_list, name='resource-requests-list'),
    path('resource-requests/create/', views.resource_request_create, name='resource-request-create'),
    path('resource-requests/anonymous/', views.resource_request_create_anonymous, name='resource-request-create-anonymous'),
    path('resource-requests/<str:request_id>/upvote/', views.resource_request_upvote, name='resource-request-upvote'),

    # Search
    path('search/', views.search_all, name='search-all'),

    # Posts — GET list + POST create handled by posts_endpoint dispatcher
    path('posts/', views.posts_endpoint, name='posts'),
    path('posts/<str:post_id>/', views.post_detail, name='post-detail'),
    path('posts/<str:post_id>/view/', views.post_view, name='post-view'),
    path('posts/<str:post_id>/like/', views.post_like, name='post-like'),

    path('posts/<str:post_id>/images/', views.post_images, name='post-images'),
    path('forum/uploads/', views.forum_media_upload, name='forum-media-upload'),
    path('polls/<str:poll_id>/vote/', views.poll_vote, name='poll-vote'),

    # Intelligent mixed feed — never-empty suggestions (posts + resources)
    path('feed/suggested/', views.feed_suggested, name='feed-suggested'),

    # Replies — GET list + POST create handled by replies_endpoint dispatcher
    path('posts/<str:post_id>/replies/', views.replies_endpoint, name='replies'),

    # Replies
    path('replies/<str:reply_id>/', views.reply_detail, name='reply-detail'),
    path('replies/<str:reply_id>/like/', views.reply_like, name='reply-like'),

    # Edit History
    path('edit-history/<str:target_type>/<str:target_id>/', views.edit_history, name='edit-history'),

    # FCM
    path('fcm/register/', views.fcm_register, name='fcm-register'),
    path('fcm/unregister/', views.fcm_unregister, name='fcm-unregister'),

    # Notifications
    path('notifications/', views.notifications_list, name='notifications-list'),
    path('notifications/mark-read/', views.notifications_mark_read, name='notifications-mark-read'),
    path('notifications/unread-count/', views.notifications_unread_count, name='notifications-unread-count'),

    # Analytics tracking (mobile app)
    path('analytics/track/', views.analytics_track, name='analytics-track'),

    # Presence heartbeat (mobile app)
    path('presence/heartbeat/', views_presence.presence_heartbeat, name='presence-heartbeat'),

    # Reports
    path('reports/', views.report_create, name='report-create'),

    # Realtime discovery (mobile clients)
    path('realtime/config/', views.realtime_config, name='realtime-config'),

    # Bookmarks
    path('bookmarks/toggle/', views.bookmark_toggle, name='bookmark-toggle'),
    path('bookmarks/', views.bookmark_list, name='bookmark-list'),
    path('bookmarks/check/', views.bookmark_check, name='bookmark-check'),

    # AI4Bharat Arena chat (Neby AI on Android)
    path('neby-arena/', include('api.arena_urls')),

    # Interactive learning catalog
    path('interactive/', include('api.interactive_urls')),

    # Consica app AI bridge (non-guessable path, key-authenticated)

    path('background-agent/mobile/', include('api.background_agent.mobile_urls')),

    # Admin API
    path('', include('api.admin_urls')),
]
