"""
DRF serializers for all NEBians API resources.
"""
from rest_framework import serializers
from .models import User, Resource, ResourceRequest, ResourceRequestUpvote, Post, PostImage, Poll, PollOption, PollVote, Reply, FCMToken, UserPhoto, Follow, EditHistory, Report, Bookmark, Notification


class UserSerializer(serializers.ModelSerializer):
    hasPassword = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'photo_url', 'banner_url', 'display_name',
            'role', 'dob', 'gender', 'class_level', 'subjects', 'teaching_subjects',
            'institution_type',
            'pradesh', 'district', 'school', 'bio', 'is_locked', 'created_at',
            'email_verified', 'hasPassword',
            'verification_level', 'moderator_level', 'is_admin', 'achievement_badges',
            'is_bot', 'teacher_verified',
        ]
        read_only_fields = ['id', 'created_at', 'email_verified', 'hasPassword',
                            'verification_level', 'moderator_level', 'is_admin', 'achievement_badges', 'is_bot', 'teacher_verified']

    def get_hasPassword(self, obj):
        return bool(obj.password_hash)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'class_level' in ret:
            ret['class'] = ret['class_level']
        if 'is_locked' in ret:
            ret['is_locked'] = 1 if ret['is_locked'] else 0
        return ret


class UserPublicSerializer(serializers.ModelSerializer):
    """Restricted view for locked/private profiles."""
    class Meta:
        model = User
        fields = ['username', 'display_name', 'photo_url', 'banner_url', 'bio', 'is_locked',
                  'role', 'verification_level', 'moderator_level', 'is_admin', 'achievement_badges', 'is_bot', 'teacher_verified']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'is_locked' in ret:
            ret['is_locked'] = 1 if ret['is_locked'] else 0
        return ret


class ResourceSerializer(serializers.ModelSerializer):
    sourceType = serializers.CharField(source='source_type', read_only=True)
    sourceUrl = serializers.CharField(source='source_url', read_only=True)
    sourceLabel = serializers.CharField(source='source_label', read_only=True)
    likeCount = serializers.IntegerField(source='like_count', read_only=True)
    commentCount = serializers.IntegerField(source='comment_count', read_only=True)
    approvalStatus = serializers.CharField(source='approval_status', read_only=True)
    fileUrl = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = [
            'id', 'title', 'description', 'subject', 'grade_level',
            'faculty', 'program', 'year', 'exam_type',
            'pradesh', 'district', 'school', 'tags',
            'type', 'file', 'file_url', 'fileUrl', 'thumbnail_url', 'file_size',
            'added_at', 'view_count', 'author_name',
            'like_count', 'comment_count',
            'source_type', 'sourceType', 'source_url', 'sourceUrl',
            'source_label', 'sourceLabel', 'likeCount', 'commentCount',
            'approval_status', 'approvalStatus',
        ]

    def get_fileUrl(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return obj.file_url or ''


class ResourceRequestSerializer(serializers.ModelSerializer):
    requestedByName = serializers.SerializerMethodField()
    requestedByPhoto = serializers.SerializerMethodField()
    requestedByUsername = serializers.SerializerMethodField()
    isUpvoted = serializers.SerializerMethodField()
    upvoteCount = serializers.IntegerField(source='upvote_count', read_only=True)

    class Meta:
        model = ResourceRequest
        fields = [
            'id', 'title', 'description', 'subject', 'grade_level',
            'faculty', 'program', 'year', 'exam_type',
            'pradesh', 'district', 'school', 'tags',
            'requested_by', 'requestedByName', 'requestedByPhoto', 'requestedByUsername',
            'requester_name', 'requester_email',
            'status', 'upvote_count', 'upvoteCount', 'isUpvoted',
            'created_at', 'fulfilled_by', 'fulfilled_at',
        ]
        read_only_fields = ['id', 'status', 'upvote_count', 'fulfilled_by', 'fulfilled_at']

    def get_requestedByName(self, obj):
        if obj.requested_by:
            return obj.requested_by.display_name or obj.requested_by.username
        return obj.requester_name or 'Anonymous'

    def get_requestedByPhoto(self, obj):
        if obj.requested_by:
            return obj.requested_by.photo_url or ''
        return ''

    def get_requestedByUsername(self, obj):
        if obj.requested_by:
            return obj.requested_by.username
        return ''

    def get_isUpvoted(self, obj):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user') or request.user is None:
            return False
        user = request.user
        if not isinstance(user, User):
            return False
        upvote_ids = self.context.get('upvoted_request_ids')
        if upvote_ids is not None:
            return obj.id in upvote_ids
        return obj.upvotes.filter(user=user).exists()


class PostImageSerializer(serializers.ModelSerializer):
    imageUrl = serializers.CharField(source='image_url')

    class Meta:
        model = PostImage
        fields = ['id', 'imageUrl', 'order']


class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollOption
        fields = ['id', 'text', 'is_correct', 'vote_count', 'order']


class PollSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many=True, read_only=True)
    isExpired = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ['id', 'question', 'poll_type', 'allow_multiple', 'explanation', 'duration_ms', 'total_votes', 'isExpired', 'options']

    def get_isExpired(self, obj):
        return obj.is_expired


class PostSerializer(serializers.ModelSerializer):
    authorName = serializers.SerializerMethodField()
    authorPhotoUrl = serializers.SerializerMethodField()
    authorId = serializers.CharField(source='user_id', read_only=True)
    authorIsBot = serializers.SerializerMethodField()
    thumbsUpCount = serializers.IntegerField(source='thumbs_up_count', read_only=True)
    replyCount = serializers.IntegerField(source='reply_count', read_only=True)
    viewCount = serializers.IntegerField(source='view_count', read_only=True)
    createdAt = serializers.IntegerField(source='created_at', read_only=True)
    updatedAt = serializers.SerializerMethodField()
    isEdited = serializers.BooleanField(source='is_edited', read_only=True)
    isArchived = serializers.BooleanField(source='is_archived', read_only=True)
    isThumbedUp = serializers.SerializerMethodField()
    images = PostImageSerializer(many=True, read_only=True)
    poll = PollSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'category',
            'authorName', 'authorPhotoUrl', 'authorId', 'authorIsBot',
            'thumbsUpCount', 'replyCount', 'viewCount', 'createdAt', 'updatedAt',
            'isEdited', 'isArchived', 'isThumbedUp', 'images', 'poll'
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

    def get_authorIsBot(self, obj):
        try:
            return obj.user.is_bot
        except Exception:
            return False

    def get_updatedAt(self, obj):
        return obj.edited_at if obj.edited_at else obj.created_at

    def get_isThumbedUp(self, obj):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user') or request.user is None:
            return False
        user = request.user
        if not isinstance(user, User):
            return False
        liked_ids = self.context.get('liked_post_ids')
        if liked_ids is not None:
            return obj.id in liked_ids
        return obj.likes.filter(user=user).exists()


class ReplySerializer(serializers.ModelSerializer):
    authorName = serializers.SerializerMethodField()
    authorPhotoUrl = serializers.SerializerMethodField()
    authorId = serializers.CharField(source='user_id', read_only=True)
    authorIsBot = serializers.SerializerMethodField()
    postId = serializers.CharField(source='post_id', read_only=True)
    parentReplyId = serializers.CharField(source='parent_reply_id', read_only=True, allow_null=True)
    thumbsUpCount = serializers.IntegerField(source='thumbs_up_count', read_only=True)
    childCount = serializers.IntegerField(source='reply_count', read_only=True)
    viewCount = serializers.IntegerField(source='view_count', read_only=True)
    createdAt = serializers.IntegerField(source='created_at', read_only=True)
    isEdited = serializers.BooleanField(source='is_edited', read_only=True)
    editedAt = serializers.IntegerField(source='edited_at', read_only=True)
    isThumbedUp = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = [
            'id', 'postId', 'parentReplyId', 'content',
            'authorName', 'authorPhotoUrl', 'authorId', 'authorIsBot',
            'thumbsUpCount', 'childCount', 'viewCount', 'createdAt', 'isEdited', 'editedAt', 'isThumbedUp'
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

    def get_authorIsBot(self, obj):
        try:
            return obj.user.is_bot
        except Exception:
            return False

    def get_isThumbedUp(self, obj):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user') or request.user is None:
            return False
        user = request.user
        if not isinstance(user, User):
            return False
        liked_ids = self.context.get('liked_reply_ids')
        if liked_ids is not None:
            return obj.id in liked_ids
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
    contribution_score = posts*3 + replies*2 + likes_given + likes_received*2
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


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'target_type', 'target_id', 'created_at']


class ReportSerializer(serializers.ModelSerializer):
    reporter_username = serializers.CharField(source='reporter.username', read_only=True, allow_null=True)

    class Meta:
        model = Report
        fields = [
            'id', 'reporter', 'reporter_username', 'target_type', 'target_id',
            'reason', 'description', 'status', 'created_at', 'resolved_at',
            'resolved_by',
        ]
        read_only_fields = ['id', 'reporter', 'status', 'created_at', 'resolved_at', 'resolved_by']


class NotificationSerializer(serializers.ModelSerializer):
    actorName = serializers.SerializerMethodField()
    actorPhotoUrl = serializers.SerializerMethodField()
    actorId = serializers.CharField(source='actor_id', read_only=True, allow_null=True)
    targetType = serializers.CharField(source='target_type', read_only=True)
    targetId = serializers.CharField(source='target_id', read_only=True)
    referenceType = serializers.CharField(source='reference_type', read_only=True, allow_null=True)
    referenceId = serializers.CharField(source='reference_id', read_only=True, allow_null=True)
    createdAt = serializers.IntegerField(source='created_at', read_only=True)
    isRead = serializers.BooleanField(source='is_read', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'actorId', 'actorName', 'actorPhotoUrl',
            'verb', 'targetType', 'targetId', 'referenceType', 'referenceId',
            'message', 'isRead', 'createdAt',
        ]

    def get_actorName(self, obj):
        return obj.actor.username if obj.actor else None

    def get_actorPhotoUrl(self, obj):
        return obj.actor.photo_url if obj.actor else None
