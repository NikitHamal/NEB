from django.urls import path
from . import admin_views

urlpatterns = [
    path('admin/stats/', admin_views.admin_stats, name='admin-stats'),
    path('admin/users/', admin_views.admin_users_list, name='admin-users-list'),
    path('admin/users/<str:user_id>/', admin_views.admin_user_detail, name='admin-user-detail'),
    path('admin/resources/', admin_views.admin_resources_list, name='admin-resources-list'),
    path('admin/resources/<str:resource_id>/', admin_views.admin_resource_detail, name='admin-resource-detail'),
    path('admin/posts/', admin_views.admin_posts_list, name='admin-posts-list'),
    path('admin/posts/<str:post_id>/', admin_views.admin_post_detail, name='admin-post-detail'),
    path('admin/posts/<str:post_id>/replies/', admin_views.admin_post_replies, name='admin-post-replies'),
    path('admin/replies/<str:reply_id>/', admin_views.admin_reply_detail, name='admin-reply-detail'),
]