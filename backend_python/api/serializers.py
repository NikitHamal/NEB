"""
DRF serializers for all NEBians API resources.
"""
from rest_framework import serializers
from .models import User, Resource, Post, Reply, FCMToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'photo_url', 'display_name',
            'dob', 'gender', 'class_level', 'subjects',
            'pradesh', 'district', 'school', 'is_locked', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

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
        fields = ['username', 'display_name', 'photo_url', 'is_locked']

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
    updatedAt = serializers.IntegerField(source='created_at', read_only=True)
    isThumbedUp = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'category',
            'authorName', 'authorPhotoUrl', 'authorId',
            'thumbsUpCount', 'replyCount', 'createdAt', 'updatedAt',
            'isThumbedUp'
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


class ReplySerializer(serializers.ModelSerializer):
    authorName = serializers.SerializerMethodField()
    authorPhotoUrl = serializers.SerializerMethodField()
    authorId = serializers.CharField(source='user_id', read_only=True)
    postId = serializers.CharField(source='post_id', read_only=True)
    parentReplyId = serializers.CharField(source='parent_reply_id', read_only=True, allow_null=True)
    thumbsUpCount = serializers.IntegerField(source='thumbs_up_count', read_only=True)
    createdAt = serializers.IntegerField(source='created_at', read_only=True)
    isThumbedUp = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = [
            'id', 'postId', 'parentReplyId', 'content',
            'authorName', 'authorPhotoUrl', 'authorId',
            'thumbsUpCount', 'createdAt', 'isThumbedUp'
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
