"""
Register models with Django Admin for easy content management.
Accessible at /admin/ after creating a superuser.
"""
from django.contrib import admin
from .models import User, Resource, Post, Reply, PostLike, ReplyLike, FCMToken


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'display_name', 'class_level', 'created_at']
    search_fields = ['username', 'email', 'display_name']
    list_filter = ['gender', 'class_level', 'is_locked']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'grade_level', 'type', 'view_count', 'added_at']
    search_fields = ['title', 'description']
    list_filter = ['subject', 'grade_level', 'type']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'thumbs_up_count', 'reply_count', 'created_at']
    search_fields = ['title', 'content']
    list_filter = ['category']


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['content', 'user', 'post', 'thumbs_up_count', 'created_at']
    search_fields = ['content']


@admin.register(FCMToken)
class FCMTokenAdmin(admin.ModelAdmin):
    list_display = ['token', 'user', 'created_at']
