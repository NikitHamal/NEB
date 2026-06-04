"""
Register models with Django Admin for easy content management.
Accessible at /admin-django/ after creating a superuser. The public custom admin UI is /admin/ and now uses the same Django staff/superuser credentials.
"""
from django.contrib import admin
from .models import User, Resource, Post, Reply, PostLike, ReplyLike, FCMToken, UserPhoto, Follow, EditHistory, Report, BotConfig, TakedownRequest, SyllabusContent
from .models import ResourceComment, ResourceLike, ResourceCommentLike


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'display_name', 'class_level', 'created_at']
    search_fields = ['username', 'email', 'display_name']
    list_filter = ['gender', 'class_level', 'is_locked']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'grade_level', 'type', 'source_type', 'view_count', 'like_count', 'added_at']
    search_fields = ['title', 'description', 'author_name']
    list_filter = ['subject', 'grade_level', 'type', 'source_type']
    raw_id_fields = ['uploaded_by']


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


@admin.register(UserPhoto)
class UserPhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_current', 'uploaded_at']
    list_filter = ['is_current']
    search_fields = ['user__username']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    search_fields = ['follower__username', 'following__username']


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']
    search_fields = ['user__username', 'post__title']


@admin.register(ReplyLike)
class ReplyLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'reply']
    search_fields = ['user__username', 'reply__content']


@admin.register(EditHistory)
class EditHistoryAdmin(admin.ModelAdmin):
    list_display = ['target_type', 'target_id', 'field', 'edited_by', 'edited_at']
    search_fields = ['target_id', 'field', 'edited_by__username']
    list_filter = ['target_type', 'field']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'reporter', 'target_type', 'target_id', 'reason', 'status', 'created_at']
    search_fields = ['target_id', 'description']
    list_filter = ['status', 'reason', 'target_type']
    raw_id_fields = ['reporter', 'resolved_by']


@admin.register(BotConfig)
class BotConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'bot_username', 'model', 'updated_at']


@admin.register(ResourceComment)
class ResourceCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'resource', 'content', 'like_count', 'created_at']
    search_fields = ['content', 'user__username', 'resource__title']
    list_filter = ['resource__subject']
    raw_id_fields = ['user', 'resource', 'parent_comment']


@admin.register(ResourceLike)
class ResourceLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'resource']
    search_fields = ['user__username', 'resource__title']


@admin.register(ResourceCommentLike)
class ResourceCommentLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment']
    search_fields = ['user__username']


@admin.register(TakedownRequest)
class TakedownRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'organization', 'infringing_url', 'status', 'created_at']
    search_fields = ['name', 'email', 'organization', 'infringing_url', 'proof_of_ownership']
    list_filter = ['status']
    raw_id_fields = ['resolved_by']


@admin.register(SyllabusContent)
class SyllabusContentAdmin(admin.ModelAdmin):
    list_display = ['chapter_title', 'subject', 'grade_level', 'order', 'created_at']
    search_fields = ['chapter_title', 'text_content', 'question_answers', 'subject']
    list_filter = ['grade_level', 'subject']
