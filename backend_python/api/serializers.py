"""
DRF serializers for all NEBians API resources.
"""
from rest_framework import serializers
from .models import User, Resource, ResourceLike, ResourceRequest, ResourceRequestUpvote, Post, PostImage, Poll, PollOption, PollVote, Reply, FCMToken, UserPhoto, Follow, EditHistory, Report, Bookmark, Notification


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
        fields = ['id', 'username', 'display_name', 'photo_url', 'banner_url', 'bio', 'is_locked',
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
    is_liked = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    isBookmarked = serializers.SerializerMethodField()
    uploaded_by_username = serializers.SerializerMethodField()
    uploadedByUsername = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()
    authorUsername = serializers.SerializerMethodField()

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
            'uploaded_by_username', 'uploadedByUsername',
            'author_username', 'authorUsername',
            'is_liked', 'isLiked', 'is_bookmarked', 'isBookmarked',
        ]

    def get_fileUrl(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return obj.file_url or ''

    def _viewer(self):
        request = self.context.get('request')
        user = getattr(request, 'user', None) if request is not None else None
        return user if isinstance(user, User) else None

    def get_is_liked(self, obj):
        user = self._viewer()
        if not user:
            return False
        liked_ids = self.context.get('liked_resource_ids')
        if liked_ids is not None:
            return obj.pk in liked_ids
        prefetched = getattr(obj, '_viewer_liked', None)
        if prefetched is not None:
            return bool(prefetched)
        return ResourceLike.objects.filter(resource_id=obj.pk, user_id=user.pk).exists()

    def get_isLiked(self, obj):
        return self.get_is_liked(obj)

    def get_is_bookmarked(self, obj):
        user = self._viewer()
        if not user:
            return False
        bookmarked_ids = self.context.get('bookmarked_resource_ids')
        if bookmarked_ids is not None:
            return str(obj.pk) in bookmarked_ids
        prefetched = getattr(obj, '_viewer_bookmarked', None)
        if prefetched is not None:
            return bool(prefetched)
        return Bookmark.objects.filter(target_type='resource', target_id=str(obj.pk), user_id=user.pk).exists()

    def get_isBookmarked(self, obj):
        return self.get_is_bookmarked(obj)

    def get_uploaded_by_username(self, obj):
        user = getattr(obj, 'uploaded_by', None)
        return user.username if user else ''

    def get_uploadedByUsername(self, obj):
        return self.get_uploaded_by_username(obj)

    def get_author_username(self, obj):
        return self.get_uploaded_by_username(obj)

    def get_authorUsername(self, obj):
        return self.get_uploaded_by_username(obj)

    def to_representation(self, obj):
        data = super().to_representation(obj)
        user = getattr(obj, 'uploaded_by', None)
        if obj.source_type == 'user' and user is not None and not data.get('author_name'):
            data['author_name'] = user.username
        return data


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
    pollType = serializers.CharField(source='poll_type', read_only=True)
    allowMultiple = serializers.BooleanField(source='allow_multiple', read_only=True)
    durationMs = serializers.IntegerField(source='duration_ms', read_only=True)
    totalVotes = serializers.IntegerField(source='total_votes', read_only=True)
    createdAt = serializers.IntegerField(source='created_at', read_only=True)
    userVote = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ['id', 'question', 'poll_type', 'allow_multiple', 'explanation', 'duration_ms', 'total_votes',
                  'pollType', 'allowMultiple', 'durationMs', 'totalVotes', 'createdAt', 'isExpired', 'userVote', 'options']

    def get_isExpired(self, obj):
        return obj.is_expired

    def get_userVote(self, obj):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user') or request.user is None:
            return None
        user = request.user
        if not isinstance(user, User):
            return None
        user_poll_votes = self.context.get('user_poll_votes')
        if user_poll_votes is not None:
            vote = user_poll_votes.get(obj.id)
            if vote is None:
                return None
            return str(vote)
        try:
            votes = list(PollVote.objects.filter(poll=obj, user=user).values_list('option_id', flat=True))
        except Exception:
            return None
        if not votes:
            return None
        if obj.allow_multiple:
            return [str(v) for v in votes]
        return str(votes[0])


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
    isBookmarked = serializers.SerializerMethodField()
    authorBadgeInfo = serializers.SerializerMethodField()
    images = PostImageSerializer(many=True, read_only=True)
    poll = PollSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'category',
            'authorName', 'authorPhotoUrl', 'authorId', 'authorIsBot', 'authorBadgeInfo',
            'thumbsUpCount', 'replyCount', 'viewCount', 'createdAt', 'updatedAt',
            'isEdited', 'isArchived', 'isThumbedUp', 'isBookmarked', 'images', 'poll'
        ]

    def get_authorBadgeInfo(self, obj):
        from .badges import user_badge_info
        try:
            return user_badge_info(obj.user)
        except Exception:
            return None

    def get_isBookmarked(self, obj):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user') or request.user is None:
            return False
        user = request.user
        if not isinstance(user, User):
            return False
        bookmarked_ids = self.context.get('bookmarked_post_ids')
        if bookmarked_ids is not None:
            return obj.id in bookmarked_ids
        try:
            return Bookmark.objects.filter(user=user, target_type='post', target_id=obj.id).exists()
        except Exception:
            return False

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
    isArchived = serializers.BooleanField(source='is_archived', read_only=True)
    isThumbedUp = serializers.SerializerMethodField()
    isBookmarked = serializers.SerializerMethodField()
    authorBadgeInfo = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = [
            'id', 'postId', 'parentReplyId', 'content',
            'authorName', 'authorPhotoUrl', 'authorId', 'authorIsBot', 'authorBadgeInfo',
            'thumbsUpCount', 'childCount', 'viewCount', 'createdAt', 'isEdited', 'editedAt',
            'isArchived', 'isThumbedUp', 'isBookmarked'
        ]

    def get_authorBadgeInfo(self, obj):
        from .badges import user_badge_info
        try:
            return user_badge_info(obj.user)
        except Exception:
            return None

    def get_isBookmarked(self, obj):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user') or request.user is None:
            return False
        user = request.user
        if not isinstance(user, User):
            return False
        bookmarked_ids = self.context.get('bookmarked_reply_ids')
        if bookmarked_ids is not None:
            return obj.id in bookmarked_ids
        try:
            return Bookmark.objects.filter(user=user, target_type='reply', target_id=obj.id).exists()
        except Exception:
            return False

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

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'id' in ret and ret['id'] is not None:
            ret['id'] = str(ret['id'])
        return ret


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
    reporter_display_name = serializers.CharField(source='reporter.display_name', read_only=True, allow_null=True)
    reporter_photo_url = serializers.CharField(source='reporter.photo_url', read_only=True, allow_null=True)
    target_summary = serializers.SerializerMethodField()
    target_author_username = serializers.SerializerMethodField()
    target_author_id = serializers.SerializerMethodField()
    target_url = serializers.SerializerMethodField()
    target_exists = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'reporter', 'reporter_username', 'reporter_display_name', 'reporter_photo_url',
            'target_type', 'target_id', 'target_summary', 'target_author_username', 'target_author_id',
            'target_url', 'target_exists', 'reason', 'description', 'status', 'created_at', 'resolved_at',
            'resolved_by',
        ]
        read_only_fields = [
            'id', 'reporter', 'status', 'created_at', 'resolved_at', 'resolved_by',
            'reporter_username', 'reporter_display_name', 'reporter_photo_url', 'target_summary',
            'target_author_username', 'target_author_id', 'target_url', 'target_exists',
        ]

    def _target_obj(self, obj):
        cache_attr = '_report_target_cache'
        if hasattr(obj, cache_attr):
            return getattr(obj, cache_attr)
        target = None
        try:
            if obj.target_type == 'post':
                target = Post.objects.select_related('user').get(pk=obj.target_id)
            elif obj.target_type == 'reply':
                target = Reply.objects.select_related('user', 'post').get(pk=obj.target_id)
            elif obj.target_type == 'resource':
                target = Resource.objects.select_related('uploaded_by').get(pk=obj.target_id)
            elif obj.target_type == 'user':
                target = User.objects.get(pk=obj.target_id)
        except (Post.DoesNotExist, Reply.DoesNotExist, Resource.DoesNotExist, User.DoesNotExist):
            target = None
        setattr(obj, cache_attr, target)
        return target

    @staticmethod
    def _truncate(value, limit=240):
        value = (value or '').strip()
        if len(value) <= limit:
            return value
        return value[: limit - 1].rstrip() + '…'

    def get_target_exists(self, obj):
        return self._target_obj(obj) is not None

    def get_target_summary(self, obj):
        target = self._target_obj(obj)
        if target is None:
            return ''
        if obj.target_type == 'post':
            return self._truncate(f'{target.title}\n\n{target.content}')
        if obj.target_type == 'reply':
            post_title = getattr(target.post, 'title', '') if getattr(target, 'post', None) else ''
            return self._truncate(f'Reply on: {post_title}\n\n{target.content}')
        if obj.target_type == 'resource':
            return self._truncate(f'{target.title}\n\n{target.description}')
        if obj.target_type == 'user':
            return self._truncate(target.display_name or target.username)
        return ''

    def get_target_author_username(self, obj):
        target = self._target_obj(obj)
        if target is None:
            return None
        if obj.target_type in ('post', 'reply'):
            return target.user.username if getattr(target, 'user', None) else None
        if obj.target_type == 'resource':
            if getattr(target, 'uploaded_by', None):
                return target.uploaded_by.username
            return target.author_name or None
        if obj.target_type == 'user':
            return target.username
        return None

    def get_target_author_id(self, obj):
        target = self._target_obj(obj)
        if target is None:
            return None
        if obj.target_type in ('post', 'reply'):
            return str(target.user_id) if getattr(target, 'user_id', None) else None
        if obj.target_type == 'resource':
            return str(target.uploaded_by_id) if getattr(target, 'uploaded_by_id', None) else None
        if obj.target_type == 'user':
            return str(target.id)
        return None

    def get_target_url(self, obj):
        target = self._target_obj(obj)
        if target is None:
            return ''
        if obj.target_type == 'post':
            return f'/forum/post/{target.id}/'
        if obj.target_type == 'reply':
            return f'/forum/post/{target.post_id}/#reply-{target.id}'
        if obj.target_type == 'resource':
            return f'/reader/{target.id}/'
        if obj.target_type == 'user':
            return f'/profile/{target.username}/'
        return ''


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
