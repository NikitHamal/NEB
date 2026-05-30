"""
DRF serializers for all NEBians API resources.
"""
from rest_framework import serializers
from .models import User, Resource, Post, Reply, FCMToken, UserPhoto, Follow, EditHistory


class UserSerializer(serializers.ModelSerializer):
    hasPassword = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'photo_url', 'display_name',
            'dob', 'gender', 'class_level', 'subjects',
            'pradesh', 'district', 'school', 'bio', 'is_locked', 'created_at',
            'email_verified', 'hasPassword',
        ]
        read_only_fields = ['id', 'created_at', 'email_verified', 'hasPassword']

    def get_hasPassword(self, obj):
        return bool(obj.password_hash)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Rename class_level to class for Kotlin expectations, keep both
        if 'class_level' in ret:
            ret['class'] = ret['class_level']
        # Convert is_locked to 0 or 1 integer for Kotlin expectations
        if 'is_locked' in ret:
            ret['is_locked'] = 1 if ret['is_locked'] else 0
        return ret


class UserPublicSerializer(serializers.ModelSerializer):
    """Restricted view for locked/private profiles."""
    class Meta:
        model = User
        fields = ['username', 'display_name', 'photo_url', 'bio', 'is_locked']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Convert is_locked to 0 or 1 integer for Kotlin expectations
        if 'is_locked' in ret:
            ret['is_locked'] = 1 if ret['is_locked'] else 0
        return ret


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = [
            'id', 'title', 'description', 'subject', 'grade_level',
            'type', 'file_url', 'thumbnail_url', 'file_size',
            'added_at', 'view_count'
        ]


class PostSerializer(serializers.ModelSerializer):
    authorName = serializers.SerializerMethodField()
    authorPhotoUrl = serializers.SerializerMethodField()
    authorId = serializers.CharField(source='user_id', read_only=True)
    thumbsUpCount = serializers.IntegerField(source='thumbs_up_count', read_only=True)
    replyCount = serializers.IntegerField(source='reply_count', read_only=True)
    createdAt = serializers.IntegerField(source='created_at', read_only=True)
    updatedAt = serializers.SerializerMethodField()
    isEdited = serializers.BooleanField(source='is_edited', read_only=True)
    isArchived = serializers.BooleanField(source='is_archived', read_only=True)
    isThumbedUp = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'category',
            'authorName', 'authorPhotoUrl', 'authorId',
            'thumbsUpCount', 'replyCount', 'createdAt', 'updatedAt',
            'isEdited', 'isArchived', 'isThumbedUp'
        ]

    def get_authorName(self, obj):
        try:
            return obj.user.username
        except Exception:
            return 'Guest'

    def get_authorPhotoUrl(self, obj):
        try:
            return obj.user.photo_url
        except Exception:
            return None

    def get_updatedAt(self, obj):
        return obj.edited_at if obj.edited_at else obj.created_at

    def get_isThumbedUp(self, obj):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user') or request.user is None:
            return False
        user = request.user
        if not isinstance(user, User):
            return False
        return obj.likes.filter(user=user).exists()


class ReplySerializer(serializers.ModelSerializer):
    authorName = serializers.SerializerMethodField()
    authorPhotoUrl = serializers.SerializerMethodField()
    authorId = serializers.CharField(source='user_id', read_only=True)
    postId = serializers.CharField(source='post_id', read_only=True)
    parentReplyId = serializers.CharField(source='parent_reply_id', read_only=True, allow_null=True)
    thumbsUpCount = serializers.IntegerField(source='thumbs_up_count', read_only=True)
    createdAt = serializers.IntegerField(source='created_at', read_only=True)
    isEdited = serializers.BooleanField(source='is_edited', read_only=True)
    editedAt = serializers.IntegerField(source='edited_at', read_only=True)
    isThumbedUp = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = [
            'id', 'postId', 'parentReplyId', 'content',
            'authorName', 'authorPhotoUrl', 'authorId',
            'thumbsUpCount', 'createdAt', 'isEdited', 'editedAt', 'isThumbedUp'
        ]

    def get_authorName(self, obj):
        try:
            return obj.user.username
        except Exception:
            return 'Guest'

    def get_authorPhotoUrl(self, obj):
        try:
            return obj.user.photo_url
        except Exception:
            return None

    def get_isThumbedUp(self, obj):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user') or request.user is None:
            return False
        user = request.user
        if not isinstance(user, User):
            return False
        return obj.likes.filter(user=user).exists()


class UserPhotoSerializer(serializers.ModelSerializer):
    """
    Serializes a saved profile photo entry.
    Used by web profile page and Android app photo history grid.
    """
    class Meta:
        model = UserPhoto
        fields = ['id', 'url', 'uploaded_at', 'is_current']


class UserStatsSerializer(serializers.Serializer):
    """
    Aggregated public stats for a user profile.
    Consumed by both the web UI and the Android app.
    contribution_score = posts*3 + replies*2 + likes_given*1 (expandable)
    """
    username = serializers.CharField()
    post_count = serializers.IntegerField()
    reply_count = serializers.IntegerField()
    follower_count = serializers.IntegerField()
    following_count = serializers.IntegerField()
    likes_received = serializers.IntegerField()      # total thumbs_up on posts + replies
    likes_given = serializers.IntegerField()         # total likes this user has given
    contribution_score = serializers.IntegerField()  # weighted composite score


class FollowSerializer(serializers.ModelSerializer):
    """Used when listing followers / following for a user (web + Android)."""
    follower_username = serializers.CharField(source='follower.username', read_only=True)
    follower_photo_url = serializers.CharField(source='follower.photo_url', read_only=True)
    follower_display_name = serializers.CharField(source='follower.display_name', read_only=True)
    following_username = serializers.CharField(source='following.username', read_only=True)
    following_photo_url = serializers.CharField(source='following.photo_url', read_only=True)
    following_display_name = serializers.CharField(source='following.display_name', read_only=True)

    class Meta:
        model = Follow
        fields = [
            'id', 'created_at',
            'follower_username', 'follower_photo_url', 'follower_display_name',
            'following_username', 'following_photo_url', 'following_display_name',
        ]


class EditHistorySerializer(serializers.ModelSerializer):
    editedByUsername = serializers.CharField(source='edited_by.username', read_only=True)
    editedByPhotoUrl = serializers.CharField(source='edited_by.photo_url', read_only=True)

    class Meta:
        model = EditHistory
        fields = ['id', 'target_type', 'target_id', 'field', 'old_value', 'new_value', 'editedByUsername', 'editedByPhotoUrl', 'edited_at']
