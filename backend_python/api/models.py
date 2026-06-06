"""
Django models for NEBians.
Schema is the source of truth — keep in sync with the Kotlin app's ApiService.
"""
import uuid
from django.db import models
from .security import generate_numeric_code


class User(models.Model):
    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'
    ROLE_INSTITUTION = 'institution'
    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Student'),
        (ROLE_TEACHER, 'Teacher'),
        (ROLE_INSTITUTION, 'Institution'),
    ]
    id = models.CharField(max_length=255, primary_key=True)
    auth_token = models.CharField(max_length=64, unique=True, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True, null=True)
    photo_url = models.TextField(blank=True, null=True)
    banner_url = models.TextField(blank=True, null=True)
    display_name = models.CharField(max_length=150, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STUDENT, db_index=True)
    dob = models.CharField(max_length=20, default='')
    gender = models.CharField(max_length=20, blank=True, null=True)
    class_level = models.CharField(max_length=10, blank=True, null=True, db_column='class')
    subjects = models.TextField(blank=True, null=True)  # comma-separated
    teaching_subjects = models.TextField(blank=True, default='')  # teacher-specific: comma-separated
    institution_type = models.CharField(max_length=30, blank=True, default='')  # school/college/academy/other
    pradesh = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    school = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, default='')
    is_locked = models.BooleanField(default=False)
    password_hash = models.CharField(max_length=255, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    # Stores a Django password-hash of the short email verification/reset code.
    # Legacy rows may still contain a six-digit plain code until first rotation.
    verification_code = models.CharField(max_length=128, blank=True, null=True)
    verification_code_expires = models.BigIntegerField(default=0)
    verification_code_purpose = models.CharField(max_length=32, blank=True, default='')
    verification_code_attempts = models.PositiveSmallIntegerField(default=0)
    verification_code_last_sent_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    # Denormalized counters — kept in sync by signals/helpers
    post_count = models.PositiveIntegerField(default=0)
    reply_count = models.PositiveIntegerField(default=0)
    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    likes_given_count = models.PositiveIntegerField(default=0)
    likes_received_count = models.PositiveIntegerField(default=0)
    contribution_score = models.PositiveIntegerField(default=0)

    # Badge / role fields
    # verification_level: 0=none, 1=blue (standard), 2=green (expert), 3=gold (premium), 4=black (elite)
    verification_level = models.PositiveSmallIntegerField(default=0)
    # moderator_level: 0=none, 1=blue (community mod), 2=teal (senior mod), 3=purple (community lead)
    moderator_level = models.PositiveSmallIntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    # achievement_badges: comma-separated badge keys (e.g. "top_contributor,scholar,first_post")
    achievement_badges = models.TextField(blank=True, default='')

    # Bot / AI account flag
    is_bot = models.BooleanField(default=False)

    # Denormalized notification counter
    unread_notification_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username or self.id

    @staticmethod
    def generate_token():
        return uuid.uuid4().hex + uuid.uuid4().hex

    @staticmethod
    def generate_verification_code():
        return generate_numeric_code(6)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return not self.is_locked


class UserAuthToken(models.Model):
    """Hashed bearer tokens for concurrent web/mobile sessions."""
    id = models.CharField(max_length=36, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auth_tokens')
    token_hash = models.CharField(max_length=64, unique=True)
    created_at = models.BigIntegerField(default=0)
    last_used_at = models.BigIntegerField(default=0)
    revoked_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'user_auth_tokens'
        indexes = [
            models.Index(fields=['user_id', 'revoked_at']),
            models.Index(fields=['token_hash', 'revoked_at']),
        ]


class Resource(models.Model):
    """Study resources — ebooks, PDFs, notes, videos, audio, images, etc."""
    SOURCE_TYPES = [
        ('admin', 'Added by Admin'),
        ('user', 'User Upload'),
        ('anonymous', 'Anonymous Upload'),
        ('external', 'External Source'),
    ]
    APPROVAL_CHOICES = [
        ('approved', 'Approved'),
        ('pending', 'Pending Review'),
        ('rejected', 'Rejected'),
    ]
    EXAM_TYPES = [
        ('', '—'),
        ('Final', 'Final Exam'),
        ('Midterm', 'Midterm / Internal'),
        ('Board', 'Board Exam'),
        ('Entrance', 'Entrance Exam'),
        ('SEE', 'SEE Exam'),
        ('Mock', 'Mock / Model'),
        ('Assignment', 'Assignment / Project'),
        ('Notes', 'Class Notes'),
        ('Reference', 'Reference Material'),
        ('Other', 'Other'),
    ]
    id = models.CharField(max_length=36, primary_key=True)  # UUID
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    subject = models.CharField(max_length=500)
    grade_level = models.CharField(max_length=30, blank=True, default='')  # Class 8–12, Diploma, Bachelor, Master, PhD, etc.
    faculty = models.CharField(max_length=100, blank=True, default='')  # e.g. Science, Management, Computer Engineering
    program = models.CharField(max_length=200, blank=True, default='')  # e.g. BSc CSIT, BE Computer, +2 Science
    year = models.CharField(max_length=20, blank=True, default='')  # e.g. 2080, 2024
    exam_type = models.CharField(max_length=20, blank=True, default='', choices=EXAM_TYPES)
    pradesh = models.CharField(max_length=50, blank=True, default='')  # e.g. Bagmati, Province 3
    district = models.CharField(max_length=100, blank=True, default='')  # e.g. Kathmandu, Lalitpur
    school = models.CharField(max_length=200, blank=True, default='')  # e.g. St. Xavier's College, Budhanilkantha School
    tags = models.TextField(blank=True, default='')  # comma-separated tags
    type = models.CharField(max_length=50, default='PDF')  # e.g. "PDF", "Note", "Video", "Audio", "Image", "Link"
    file = models.FileField(upload_to='resources/%Y/%m/', blank=True, null=True)
    file_url = models.TextField(blank=True, default='')
    thumbnail_url = models.TextField(blank=True, null=True)
    file_size = models.BigIntegerField(default=0)
    added_at = models.BigIntegerField()  # Unix ms timestamp
    view_count = models.IntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    author_name = models.CharField(max_length=100, blank=True, default='')  # credit/attribution
    # Source tracking
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES, default='admin')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_resources')
    source_url = models.TextField(blank=True, default='')  # external source URL
    source_label = models.CharField(max_length=200, blank=True, default='')  # e.g. "NEB Official", "Contributed by students"
    # Approval workflow — admin-added resources are auto-approved; user/anonymous uploads require review
    approval_status = models.CharField(max_length=10, choices=APPROVAL_CHOICES, default='approved')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_resources')
    reviewed_at = models.BigIntegerField(default=0)
    rejection_reason = models.TextField(blank=True, default='')
    upload_group_id = models.CharField(max_length=36, blank=True, default='')
    is_lead = models.BooleanField(default=True)

    class Meta:
        db_table = 'resources'
        ordering = ['-added_at']
        indexes = [
            models.Index(fields=['subject']),
            models.Index(fields=['grade_level']),
            models.Index(fields=['faculty']),
            models.Index(fields=['exam_type']),
            models.Index(fields=['type']),
            models.Index(fields=['-like_count']),
            models.Index(fields=['approval_status']),
        ]

    def __str__(self):
        return self.title


class ResourceRequest(models.Model):
    """User requests for resources they need — e.g. 'I need Grade 12 Physics notes'."""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('fulfilled', 'Fulfilled'),
        ('closed', 'Closed'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    subject = models.CharField(max_length=500, blank=True, default='')
    grade_level = models.CharField(max_length=30, blank=True, default='')
    faculty = models.CharField(max_length=100, blank=True, default='')
    program = models.CharField(max_length=200, blank=True, default='')
    year = models.CharField(max_length=20, blank=True, default='')
    exam_type = models.CharField(max_length=20, blank=True, default='')
    pradesh = models.CharField(max_length=50, blank=True, default='')
    district = models.CharField(max_length=100, blank=True, default='')
    school = models.CharField(max_length=200, blank=True, default='')
    tags = models.TextField(blank=True, default='')
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resource_requests')
    requester_name = models.CharField(max_length=100, blank=True, default='')  # for anonymous
    requester_email = models.EmailField(blank=True, default='')  # for anonymous
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    upvote_count = models.PositiveIntegerField(default=0)
    created_at = models.BigIntegerField()
    fulfilled_by = models.ForeignKey(Resource, on_delete=models.SET_NULL, null=True, blank=True, related_name='fulfilling_requests')
    fulfilled_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'resource_requests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-upvote_count']),
            models.Index(fields=['subject']),
            models.Index(fields=['grade_level']),
        ]

    def __str__(self):
        return self.title


class ResourceRequestUpvote(models.Model):
    """Tracks which users upvoted which resource requests."""
    request = models.ForeignKey(ResourceRequest, on_delete=models.CASCADE, related_name='upvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_upvotes')

    class Meta:
        db_table = 'resource_request_upvotes'
        unique_together = ('request', 'user')


class Post(models.Model):
    """Forum post."""
    id = models.CharField(max_length=36, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=300)
    content = models.TextField()
    category = models.CharField(max_length=100)
    thumbs_up_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    is_edited = models.BooleanField(default=False)
    edited_at = models.BigIntegerField(default=0)
    is_archived = models.BooleanField(default=False)
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', '-created_at']),
            models.Index(fields=['category']),
            models.Index(fields=['is_archived', '-created_at']),
            models.Index(fields=['-thumbs_up_count']),
            models.Index(fields=['-view_count']),
        ]

    def __str__(self):
        return self.title


class PostLike(models.Model):
    """Tracks which users liked which posts (prevents double-liking)."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')

    class Meta:
        db_table = 'post_likes'
        unique_together = ('post', 'user')


class Reply(models.Model):
    """Forum reply — supports nested replies via parent_reply."""
    id = models.CharField(max_length=36, primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    parent_reply = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='children'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    thumbs_up_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    is_edited = models.BooleanField(default=False)
    edited_at = models.BigIntegerField(default=0)
    is_archived = models.BooleanField(default=False)
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'replies'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post_id', 'created_at']),
            models.Index(fields=['parent_reply_id', 'created_at']),
        ]

    def __str__(self):
        return f"Reply by {self.user_id} on {self.post_id}"


class ReplyLike(models.Model):
    """Tracks which users liked which replies."""
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_likes')

    class Meta:
        db_table = 'reply_likes'
        unique_together = ('reply', 'user')


class FCMToken(models.Model):
    """Firebase Cloud Messaging tokens for push notifications."""
    token = models.CharField(max_length=512, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='fcm_tokens')
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'fcm_tokens'
        indexes = [
            models.Index(fields=['user_id']),
        ]


class UserPhoto(models.Model):
    """
    Profile picture history for a user.
    Stores previously used photo URLs so users can switch back.
    is_current=True marks the active photo (should match user.photo_url).
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    url = models.TextField()
    uploaded_at = models.BigIntegerField()  # Unix ms timestamp
    is_current = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_photos'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['user_id']),
        ]

    def __str__(self):
        return f"Photo for {self.user_id} ({'active' if self.is_current else 'past'})"


class Follow(models.Model):
    """
    Instagram-style one-way follow relationship.
    follower  = the user who pressed Follow.
    following = the user being followed.
    Follower count of X  = Follow.objects.filter(following=X).count()
    Following count of X = Follow.objects.filter(follower=X).count()
    """
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set')
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'follows'
        ordering = ['-created_at']
        unique_together = ('follower', 'following')
        indexes = [
            models.Index(fields=['following_id']),
            models.Index(fields=['follower_id']),
        ]

    def __str__(self):
        return f"{self.follower_id} → {self.following_id}"


class EditHistory(models.Model):
    """Tracks edit history for posts and replies."""
    id = models.CharField(max_length=36, primary_key=True)
    target_type = models.CharField(max_length=10)
    target_id = models.CharField(max_length=36)
    field = models.CharField(max_length=50)
    old_value = models.TextField(blank=True, default='')
    new_value = models.TextField(blank=True, default='')
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edits_made')
    edited_at = models.BigIntegerField()

    class Meta:
        db_table = 'edit_history'
        ordering = ['edited_at']
        indexes = [
            models.Index(fields=['target_type', 'target_id']),
        ]


class Bookmark(models.Model):
    """User bookmarks for posts, replies, and resources."""
    TARGET_TYPES = [
        ('post', 'Post'),
        ('reply', 'Reply'),
        ('resource', 'Resource'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    target_type = models.CharField(max_length=10, choices=TARGET_TYPES)
    target_id = models.CharField(max_length=36)
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'bookmarks'
        ordering = ['-created_at']
        unique_together = ('user', 'target_type', 'target_id')
        indexes = [
            models.Index(fields=['user_id', 'target_type']),
            models.Index(fields=['target_type', 'target_id']),
        ]

    def __str__(self):
        return f"{self.user_id} bookmarked {self.target_type}:{self.target_id}"


class Report(models.Model):
    """Content / user reports for moderation."""
    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('abuse', 'Abuse / Harassment'),
        ('inappropriate', 'Inappropriate Content'),
        ('misinformation', 'Misinformation'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('reviewing', 'Reviewing'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_made')
    target_type = models.CharField(max_length=10)
    target_id = models.CharField(max_length=36)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES, default='other')
    description = models.TextField(blank=True, default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.BigIntegerField()
    resolved_at = models.BigIntegerField(default=0)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_resolved')

    class Meta:
        db_table = 'reports'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['target_type', 'target_id']),
        ]


class Notification(models.Model):
    """
    In-app notification for a user.
    verb examples: like_post, like_reply, reply, reply_reply, follow, mention, system
    target_type: post, reply, user, system
    target_id: PK of the target object
    reference_type/reference_id: optional link to related object (e.g. post where reply was made)
    """
    VERB_CHOICES = [
        ('like_post', 'Liked your post'),
        ('like_reply', 'Liked your reply'),
        ('like_resource', 'Liked your resource'),
        ('like_resource_comment', 'Liked your comment on a resource'),
        ('reply', 'Replied to your post'),
        ('reply_reply', 'Replied to your comment'),
        ('resource_comment', 'Commented on your resource'),
        ('resource_comment_reply', 'Replied to your comment on a resource'),
        ('follow', 'Started following you'),
        ('mention', 'Mentioned you'),
        ('resource_approved', 'Your resource was approved'),
        ('resource_rejected', 'Your resource was rejected'),
        ('system', 'System notification'),
    ]
    TARGET_TYPES = [
        ('post', 'Post'),
        ('reply', 'Reply'),
        ('user', 'User'),
        ('resource', 'Resource'),
        ('resource_comment', 'Resource Comment'),
        ('system', 'System'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_sent', null=True, blank=True)
    verb = models.CharField(max_length=30, choices=VERB_CHOICES)
    target_type = models.CharField(max_length=20, choices=TARGET_TYPES)
    target_id = models.CharField(max_length=36)
    reference_type = models.CharField(max_length=20, blank=True, default='')
    reference_id = models.CharField(max_length=36, blank=True, default='')
    message = models.TextField(blank=True, default='')
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient_id', '-created_at']),
            models.Index(fields=['recipient_id', 'is_read', '-created_at']),
            models.Index(fields=['target_type', 'target_id']),
            models.Index(fields=['recipient_id', 'actor_id', 'verb', 'target_type', 'target_id'], name='notif_dedup_idx'),
        ]


class ResourceComment(models.Model):
    """Comment on a resource — supports nested replies via parent_comment."""
    id = models.CharField(max_length=36, primary_key=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_comments')
    parent_comment = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='children'
    )
    content = models.TextField()
    like_count = models.PositiveIntegerField(default=0)
    reply_count = models.PositiveIntegerField(default=0)
    is_edited = models.BooleanField(default=False)
    edited_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'resource_comments'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['resource_id', 'created_at']),
            models.Index(fields=['parent_comment_id', 'created_at']),
        ]

    def __str__(self):
        return f"Comment by {self.user_id} on resource {self.resource_id}"


class ResourceLike(models.Model):
    """Tracks which users liked which resources."""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_likes')

    class Meta:
        db_table = 'resource_likes'
        unique_together = ('resource', 'user')


class ResourceCommentLike(models.Model):
    """Tracks which users liked which resource comments."""
    comment = models.ForeignKey(ResourceComment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_comment_likes')

    class Meta:
        db_table = 'resource_comment_likes'
        unique_together = ('comment', 'user')


class BotConfig(models.Model):
    """Configuration for an AI bot. Multiple bots can be defined, each with
    its own username, provider, model, and personality. When enabled, the bot
    responds to @username mentions in posts and replies.
    """
    PROVIDER_CHOICES = [
        ('qwen', 'Qwen (chat.qwen.ai)'),
        ('ai4bharat', 'AI4Bharat Arena (Indic LLM Arena)'),
        ('custom', 'Custom OpenAI-compatible endpoint'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='Neby', help_text='Display name shown in the admin panel.')
    enabled = models.BooleanField(default=False)
    bot_username = models.CharField(max_length=50, default='neby', unique=True, help_text='The @username that triggers this bot. Must match a User with is_bot=True.')
    display_name = models.CharField(max_length=100, blank=True, default='', help_text='Friendly name the bot uses in replies. Falls back to name.')
    avatar_url = models.TextField(blank=True, default='', help_text='URL for the bot avatar image.')
    provider = models.CharField(
        max_length=20, choices=PROVIDER_CHOICES, default='qwen',
    )
    api_url = models.TextField(default='https://chat.qwen.ai/api/v2')
    api_key = models.TextField(blank=True, default='')
    model = models.CharField(max_length=200, default='qwen3.6-plus')
    system_prompt = models.TextField(
        default='You are Neby, a friendly and helpful AI study buddy for Nepali students on the NEBians app. '
                'You help with academic questions, explain concepts clearly, and give study tips.\n\n'
                'Rules:\n'
                '- Answer the question directly and accurately. Do NOT start every answer with "is the branch of" or force NEB curriculum references.\n'
                '- Only mention NEB curriculum if the question is specifically about it.\n'
                '- Be conversational, warm, and concise. Use simple language.\n'
                '- You can use basic markdown: **bold**, *italic*.\n'
                '- Never reveal you are an AI language model. You are Neby, the NEBians assistant.\n'
                '- If you don\'t know something, say so honestly rather than making up an answer.'
    )
    max_context_posts = models.PositiveIntegerField(default=5)
    max_context_replies = models.PositiveIntegerField(default=10)
    response_max_length = models.PositiveIntegerField(default=500)
    updated_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'bot_config'
        ordering = ['id']

    def save(self, *args, **kwargs):
        import time
        now = int(time.time() * 1000)
        self.updated_at = now
        if not self.created_at:
            self.created_at = now
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} (@{self.bot_username})'

    @classmethod
    def get_enabled_bots(cls):
        return list(cls.objects.filter(enabled=True).select_related())

    @classmethod
    def get_bot_user(cls, bot_config=None):
        if bot_config is None:
            first = cls.objects.filter(enabled=True).first()
            if not first:
                return None
            bot_config = first
        try:
            return User.objects.get(username__iexact=bot_config.bot_username, is_bot=True)
        except User.DoesNotExist:
            return None


class NebyTask(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    ]
    TRIGGER_CHOICES = [
        ('post_mention', 'Post Mention'),
        ('reply_mention', 'Reply Mention'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    bot_config = models.ForeignKey(
        BotConfig, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='tasks', db_column='bot_config_id',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    trigger = models.CharField(max_length=20, choices=TRIGGER_CHOICES)
    post_id = models.CharField(max_length=36)
    reply_id = models.CharField(max_length=36, blank=True, null=True)
    created_at = models.BigIntegerField()
    started_at = models.BigIntegerField(default=0)
    finished_at = models.BigIntegerField(default=0)
    attempts = models.PositiveSmallIntegerField(default=0)
    error_message = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'neby_tasks'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]


class ArenaChatSession(models.Model):
    """A user's persistent conversation with the AI4Bharat Arena.

    Each session maps to one remote arena session (UUID) and is bound to a
    specific anonymous-pool token so multi-turn threading works server-side.
    The token is rotated on demand when its message budget runs low.
    """
    id = models.CharField(max_length=36, primary_key=True)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='arena_sessions', db_index=True,
    )
    arena_session_id = models.CharField(max_length=64, db_index=True)
    arena_token_id = models.CharField(max_length=64, blank=True, default='')
    model_id = models.CharField(max_length=64)
    model_code = models.CharField(max_length=100, blank=True, default='')
    model_display_name = models.CharField(max_length=200, blank=True, default='')
    title = models.CharField(max_length=200, blank=True, default='')
    is_active = models.BooleanField(default=True)
    message_count = models.PositiveIntegerField(default=0)
    last_message_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField()
    updated_at = models.BigIntegerField()

    class Meta:
        db_table = 'arena_chat_sessions'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['user', 'is_active']),
        ]


class ArenaChatMessage(models.Model):
    """A single message (user or assistant) inside an ArenaChatSession.

    `parent_id` is the local PK of the previous message in our DB
    (for OpenAI-style client threading). `arena_message_id` is the remote
    UUID the arena assigns to assistant messages — required for regenerations
    and to pass `parent_message_ids` in subsequent turns.
    """
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    session = models.ForeignKey(
        'ArenaChatSession', on_delete=models.CASCADE, related_name='messages', db_index=True,
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField(blank=True, default='')
    parent_id = models.CharField(max_length=36, blank=True, default='')
    arena_message_id = models.CharField(max_length=64, blank=True, default='')
    finish_reason = models.CharField(max_length=20, blank=True, default='')
    error = models.CharField(max_length=200, blank=True, default='')
    duration_ms = models.PositiveIntegerField(default=0)
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'arena_chat_messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['session', 'created_at']),
        ]


class TakedownRequest(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('reviewing', 'Reviewing'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    id = models.CharField(max_length=36, primary_key=True)  # UUID
    name = models.CharField(max_length=150)
    email = models.EmailField()
    organization = models.CharField(max_length=200, blank=True, default='')
    infringing_url = models.TextField()  # URL of file on NEBians
    proof_of_ownership = models.TextField()  # Description of original copyright
    statement_good_faith = models.BooleanField(default=False)
    statement_accurate = models.BooleanField(default=False)
    signature = models.CharField(max_length=150)  # Electronic signature
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.BigIntegerField()  # Unix ms timestamp
    resolved_at = models.BigIntegerField(default=0)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_takedowns')
    notes = models.TextField(blank=True, default='')  # Internal admin notes

    class Meta:
        db_table = 'takedown_requests'
        ordering = ['-created_at']


class SyllabusContent(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    grade_level = models.CharField(max_length=50)  # e.g., "Class 12"
    subject = models.CharField(max_length=100)      # e.g., "English"
    chapter_id = models.CharField(max_length=100)   # e.g., "the-selfish-giant"
    chapter_title = models.CharField(max_length=200) # e.g., "Story 1: The Selfish Giant"
    text_content = models.TextField()               # Text syllabus/summary/details
    question_answers = models.TextField(blank=True, default='') # Solved Question & Answers text
    order = models.IntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'syllabus_content'
        ordering = ['grade_level', 'subject', 'order']
        verbose_name = 'Syllabus Content'
        verbose_name_plural = 'Syllabus Contents'

