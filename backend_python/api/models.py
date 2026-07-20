"""
Django models for NEBians.
Schema is the source of truth — keep in sync with the Kotlin app's ApiService.
"""
import time
import uuid
from django.db import models
from .security import generate_numeric_code

NEPAL_DISTRICTS = [
    'Achham', 'Arghakhanchi', 'Baglung', 'Baitadi', 'Bajhang', 'Bajura',
    'Banke', 'Bara', 'Bardiya', 'Bhaktapur', 'Bhojpur', 'Chitwan',
    'Dadeldhura', 'Dailekh', 'Dang', 'Darchula', 'Dhading', 'Dhankuta',
    'Dhanusha', 'Dolakha', 'Dolpa', 'Doti', 'Gorkha', 'Gulmi',
    'Humla', 'Ilam', 'Jajarkot', 'Jhapa', 'Jumla', 'Kailali',
    'Kalikot', 'Kanchanpur', 'Kapilvastu', 'Kaski', 'Kathmandu',
    'Kavrepalanchok', 'Khotang', 'Lalitpur', 'Lamjung', 'Mahottari',
    'Makwanpur', 'Manang', 'Morang', 'Mugu', 'Mustang', 'Myagdi',
    'Nawalparasi East', 'Nawalparasi West', 'Nuwakot', 'Okhaldhunga',
    'Palpa', 'Panchthar', 'Parbat', 'Parsa', 'Pyuthan', 'Ramechhap',
    'Rasuwa', 'Rautahat', 'Rolpa', 'Rukum East', 'Rukum West',
    'Rupandehi', 'Salyan', 'Sankhuwasabha', 'Saptari', 'Sarlahi',
    'Sindhuli', 'Sindhupalchok', 'Siraha', 'Solukhumbu', 'Sunsari',
    'Surkhet', 'Syangja', 'Tanahu', 'Taplejung', 'Terhathum',
    'Udayapur',
]

DISTRICTS_BY_PROVINCE = {
    '1': ['Bhojpur', 'Dhankuta', 'Ilam', 'Jhapa', 'Khotang', 'Morang',
          'Okhaldhunga', 'Panchthar', 'Sankhuwasabha', 'Solukhumbu',
          'Sunsari', 'Taplejung', 'Terhathum', 'Udayapur'],
    '2': ['Bara', 'Dhanusha', 'Mahottari', 'Parsa', 'Rautahat',
          'Saptari', 'Sarlahi', 'Siraha'],
    '3': ['Bhaktapur', 'Chitwan', 'Dhading', 'Dolakha', 'Kathmandu',
          'Kavrepalanchok', 'Lalitpur', 'Makwanpur', 'Nuwakot',
          'Ramechhap', 'Rasuwa', 'Sindhuli', 'Sindhupalchok'],
    '4': ['Baglung', 'Gorkha', 'Kaski', 'Lamjung', 'Manang', 'Mustang',
          'Myagdi', 'Nawalparasi East', 'Parbat', 'Syangja', 'Tanahu'],
    '5': ['Arghakhanchi', 'Banke', 'Bardiya', 'Dang', 'Gulmi',
          'Kapilvastu', 'Palpa', 'Pyuthan', 'Rolpa', 'Rukum East',
          'Nawalparasi West', 'Rupandehi'],
    '6': ['Dailekh', 'Dolpa', 'Humla', 'Jajarkot', 'Jumla', 'Kalikot',
          'Mugu', 'Salyan', 'Surkhet', 'Rukum West'],
    '7': ['Achham', 'Baitadi', 'Bajhang', 'Bajura', 'Dadeldhura',
          'Darchula', 'Doti', 'Kailali', 'Kanchanpur'],
}


class User(models.Model):
    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'
    ROLE_INSTITUTION = 'institution'
    ROLE_EXPLORER = 'explorer'
    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Student'),
        (ROLE_TEACHER, 'Teacher'),
        (ROLE_INSTITUTION, 'Institution'),
        (ROLE_EXPLORER, 'Explorer'),
    ]
    id = models.CharField(max_length=255, primary_key=True)
    auth_token = models.CharField(max_length=64, unique=True, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True, null=True, db_index=True)
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
    school_username = models.CharField(max_length=50, blank=True, default='')
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
    last_active = models.BigIntegerField(default=0)

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

    # Teacher verification — admin-verified teachers get a special badge
    teacher_verified = models.BooleanField(default=False, db_index=True)

    # Institution verification — admin-verified institutions get a special badge
    institution_verified = models.BooleanField(default=False, db_index=True)

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
    study_level = models.CharField(max_length=80, blank=True, default='')
    # TODO: dead columns — remove in cleanup migration (this `subject` is
    # shadowed by the second `subject` definition below; the StudySpace-style
    # *_min_role fields were copy-pasted and are unused on Resource).
    subject = models.CharField(max_length=120, blank=True, default='')
    exam = models.CharField(max_length=120, blank=True, default='')
    generate_min_role = models.CharField(max_length=20, default='moderator')
    upload_min_role = models.CharField(max_length=20, default='member')
    invite_min_role = models.CharField(max_length=20, default='admin')
    moderate_min_role = models.CharField(max_length=20, default='moderator')
    publish_min_role = models.CharField(max_length=20, default='owner')
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
            models.Index(fields=['approval_status', 'is_lead', '-added_at'], name='res_appr_lead_added_idx'),
            models.Index(fields=['approval_status', 'is_lead', '-view_count'], name='res_appr_lead_views_idx'),
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
            models.Index(fields=['status', '-created_at'], name='resreq_status_created_idx'),
            models.Index(fields=['requested_by', '-created_at'], name='resreq_user_created_idx'),
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
    is_anonymous = models.BooleanField(default=False)
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
            models.Index(fields=['category', 'is_archived', '-created_at'], name='post_cat_arch_created_idx'),
            models.Index(fields=['is_archived', '-thumbs_up_count', '-created_at'], name='post_arch_rank_idx'),
        ]

    def __str__(self):
        return self.title


class PostImage(models.Model):
    """Images attached to a post (max 3 per post)."""
    id = models.CharField(max_length=36, primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image_url = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'post_images'
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['post_id', 'order']),
        ]


class PostMedia(models.Model):
    """Attachments on posts and replies: videos, audio files and generic files.
    Images keep using PostImage (the 3-image gallery); PostMedia covers
    everything richer while keeping one serializer shape for all clients."""
    KIND_CHOICES = (
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('file', 'File'),
    )
    id = models.CharField(max_length=36, primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media', null=True, blank=True)
    reply = models.ForeignKey('Reply', on_delete=models.CASCADE, related_name='media', null=True, blank=True)
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default='file')
    url = models.TextField()
    name = models.CharField(max_length=255, blank=True, default='')
    mime_type = models.CharField(max_length=120, blank=True, default='')
    size_bytes = models.BigIntegerField(default=0)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'post_media'
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['post_id', 'order']),
            models.Index(fields=['reply_id', 'order']),
        ]


class Poll(models.Model):
    DURATION_CHOICES = [
        (0, 'No expiry'),
        (3600000, '1 hour'),
        (86400000, '24 hours'),
        (259200000, '3 days'),
        (604800000, '7 days'),
    ]
    POLL_TYPE_VOTING = 'voting'
    POLL_TYPE_MCQ = 'mcq'
    POLL_TYPE_CHOICES = [
        (POLL_TYPE_VOTING, 'Voting'),
        (POLL_TYPE_MCQ, 'MCQ Quiz'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='poll')
    question = models.CharField(max_length=300, blank=True, default='')
    poll_type = models.CharField(max_length=10, choices=POLL_TYPE_CHOICES, default=POLL_TYPE_VOTING)
    allow_multiple = models.BooleanField(default=False)
    explanation = models.TextField(blank=True, default='')
    duration_ms = models.BigIntegerField(default=0, choices=DURATION_CHOICES)
    total_votes = models.PositiveIntegerField(default=0)
    created_at = models.BigIntegerField()

    @property
    def is_expired(self):
        if self.duration_ms == 0:
            return False
        return int(time.time() * 1000) > self.created_at + self.duration_ms

    class Meta:
        db_table = 'polls'


class PollOption(models.Model):
    """An option in a poll."""
    id = models.CharField(max_length=36, primary_key=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    vote_count = models.PositiveIntegerField(default=0)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'poll_options'
        ordering = ['order']
        indexes = [
            models.Index(fields=['poll_id', 'order']),
        ]


class PollVote(models.Model):
    """A user's vote on a poll option."""
    id = models.CharField(max_length=36, primary_key=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poll_votes')
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'poll_votes'
        indexes = [
            models.Index(fields=['poll_id', 'user_id']),
        ]


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
    is_anonymous = models.BooleanField(default=False)
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'replies'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post_id', 'created_at']),
            models.Index(fields=['parent_reply_id', 'created_at']),
            models.Index(fields=['post_id', 'is_archived', '-thumbs_up_count', 'created_at'], name='reply_post_rank_idx'),
            models.Index(fields=['user_id', '-created_at'], name='reply_user_created_idx'),
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


class FollowRequest(models.Model):
    """Instagram-style follow request for private accounts."""
    id = models.CharField(max_length=36, primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_follow_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_follow_requests')
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'follow_requests'
        ordering = ['-created_at']
        unique_together = ('sender', 'receiver')
        indexes = [
            models.Index(fields=['receiver_id']),
            models.Index(fields=['sender_id']),
        ]

    def __str__(self):
        return f"{self.sender_id} requested to follow {self.receiver_id}"


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
    actor_anonymous = models.BooleanField(default=False)
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
            models.Index(fields=['resource_id', '-like_count', 'created_at'], name='rescomm_rank_idx'),
            models.Index(fields=['user_id', '-created_at'], name='rescomm_user_created_idx'),
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
        ('egov', 'eGov Chat AI (Philippines)'),
        ('deepai', 'DeepAI (deepai.org)'),
        ('inception', 'Inception Labs (Mercury 2)'),
        ('custom', 'Custom OpenAI-compatible endpoint'),
        # Official API providers (handled through api.llm — real API formats,
        # not the web scrapers above).
        ('agnes', 'Agnes 2.0 Flash (Sapiens AI — official API, currently free)'),
        ('openai', 'OpenAI (ChatGPT official API)'),
        ('anthropic', 'Anthropic (Claude official API)'),
        ('gemini', 'Google Gemini (official API)'),
        ('deepseek', 'DeepSeek (official API)'),
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
    model = models.CharField(max_length=200, default='qwen3.7-plus')
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
    """A user's persistent conversation with an AI provider.

    Supports two providers:
      - 'ai4bharat': the AI4Bharat Arena (anonymous token pool, no file uploads)
      - 'qwen': the Qwen proxy (browser-spoofed session, supports file uploads)

    Each session maps to one remote session ID and is bound to provider-specific
    credentials. For AI4Bharat, arena_token_id is the bound anonymous pool token.
    For Qwen, qwen_chat_id is the Qwen chat ID.
    """
    PROVIDER_CHOICES = [
        ('ai4bharat', 'AI4Bharat Arena'),
        ('qwen', 'Qwen (chat.qwen.ai)'),
        ('egov', 'eGov Chat AI (Philippines)'),
        ('deepai', 'DeepAI (deepai.org)'),
        ('inception', 'Inception Labs (Mercury 2)'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='arena_sessions', db_index=True,
    )
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='ai4bharat')
    arena_session_id = models.CharField(max_length=64, db_index=True)
    arena_token_id = models.CharField(max_length=64, blank=True, default='')
    qwen_chat_id = models.CharField(max_length=64, blank=True, default='')
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


class ArenaChatAttachment(models.Model):
    """A file attached to an ArenaChatMessage (image, PDF, audio, video)."""
    id = models.CharField(max_length=36, primary_key=True)
    message = models.ForeignKey(
        'ArenaChatMessage', on_delete=models.CASCADE, related_name='attachments', db_index=True,
    )
    file_type = models.CharField(max_length=20)
    file_name = models.CharField(max_length=500)
    file_size = models.PositiveIntegerField(default=0)
    mime_type = models.CharField(max_length=200, blank=True, default='')
    qwen_file_id = models.CharField(max_length=200, blank=True, default='')
    qwen_file_url = models.TextField(blank=True, default='')
    show_type = models.CharField(max_length=20, blank=True, default='')
    file_class = models.CharField(max_length=20, blank=True, default='')
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'arena_chat_attachments'


class StudySpace(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_spaces', db_index=True)
    title = models.CharField(max_length=200, blank=True, default='')
    description = models.TextField(blank=True, default='')
    SHARE_PRIVATE = 'private'
    SHARE_LINK = 'link'
    SHARE_SPECIFIC = 'specific'
    SHARE_CHOICES = [
        (SHARE_PRIVATE, 'Private'),
        (SHARE_LINK, 'Invite link'),
        (SHARE_SPECIFIC, 'Specific users'),
    ]
    VISIBILITY_PRIVATE = 'private'
    VISIBILITY_UNLISTED = 'unlisted'
    VISIBILITY_PUBLIC = 'public'
    VISIBILITY_CHOICES = [
        (VISIBILITY_PRIVATE, 'Private'),
        (VISIBILITY_UNLISTED, 'Unlisted invite'),
        (VISIBILITY_PUBLIC, 'Public'),
    ]
    share_token = models.CharField(max_length=64, unique=True, default=uuid.uuid4, db_index=True)
    invite_code = models.CharField(max_length=12, unique=True, blank=True, default='', db_index=True)
    share_mode = models.CharField(max_length=20, choices=SHARE_CHOICES, default=SHARE_PRIVATE, db_index=True)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default=VISIBILITY_PRIVATE, db_index=True)
    allow_join_by_code = models.BooleanField(default=True)
    study_level = models.CharField(max_length=80, blank=True, default='')
    subject = models.CharField(max_length=120, blank=True, default='')
    exam = models.CharField(max_length=120, blank=True, default='')
    generate_min_role = models.CharField(max_length=20, default='moderator')
    upload_min_role = models.CharField(max_length=20, default='member')
    invite_min_role = models.CharField(max_length=20, default='admin')
    moderate_min_role = models.CharField(max_length=20, default='moderator')
    publish_min_role = models.CharField(max_length=20, default='owner')
    shared_at = models.BigIntegerField(default=0)
    link_summary_compact = models.TextField(blank=True, default='')
    link_summary_detailed = models.TextField(blank=True, default='')
    link_summary_generated_at = models.BigIntegerField(default=0)
    link_mindmap_json = models.TextField(blank=True, default='')
    link_mindmap_generated_at = models.BigIntegerField(default=0)
    learning_plan = models.TextField(blank=True, default='')
    learning_plan_days = models.IntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'study_spaces'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['visibility', '-updated_at'], name='space_visibility_updated_idx'),
            models.Index(fields=['user', 'visibility', '-updated_at'], name='space_user_vis_updated_idx'),
        ]


class StudySpaceShare(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    space = models.ForeignKey(StudySpace, on_delete=models.CASCADE, related_name='share_grants', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_space_shares', db_index=True)
    granted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_space_grants')
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'study_space_shares'
        unique_together = ('space', 'user')
        indexes = [
            models.Index(fields=['space', 'user']),
            models.Index(fields=['user', '-created_at']),
        ]


class StudySpaceMember(models.Model):
    ROLE_OWNER = 'owner'
    ROLE_ADMIN = 'admin'
    ROLE_MODERATOR = 'moderator'
    ROLE_MEMBER = 'member'
    ROLE_CHOICES = [
        (ROLE_OWNER, 'Owner'),
        (ROLE_ADMIN, 'Admin'),
        (ROLE_MODERATOR, 'Moderator'),
        (ROLE_MEMBER, 'Member'),
    ]
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    space = models.ForeignKey(StudySpace, on_delete=models.CASCADE, related_name='members', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_space_memberships', db_index=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER, db_index=True)
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='study_space_invites_sent')
    joined_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'study_space_members'
        unique_together = ('space', 'user')
        indexes = [
            models.Index(fields=['space', 'role']),
            models.Index(fields=['user', '-joined_at']),
        ]


class StudySpaceQuiz(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    space = models.ForeignKey(StudySpace, on_delete=models.CASCADE, related_name='quizzes', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_space_quizzes', db_index=True)
    title = models.CharField(max_length=500, blank=True, default='')
    question_count = models.PositiveIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'study_space_quizzes'
        ordering = ['-created_at']


class StudySpaceQuizQuestion(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    quiz = models.ForeignKey(StudySpaceQuiz, on_delete=models.CASCADE, related_name='questions', db_index=True)
    question_number = models.PositiveIntegerField(default=0)
    question_text = models.TextField()
    option_a = models.TextField(blank=True, default='')
    option_b = models.TextField(blank=True, default='')
    option_c = models.TextField(blank=True, default='')
    option_d = models.TextField(blank=True, default='')
    correct_answer = models.CharField(max_length=1, default='A')
    explanation = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'study_space_quiz_questions'
        ordering = ['question_number']


class StudySpaceQuizAttempt(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    quiz = models.ForeignKey(StudySpaceQuiz, on_delete=models.CASCADE, related_name='attempts', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_space_quiz_attempts', db_index=True)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    answers = models.TextField(blank=True, default='')
    xp_earned = models.PositiveIntegerField(default=0)
    completed_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'study_space_quiz_attempts'
        ordering = ['-completed_at']


class StudySpaceFlashcard(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    space = models.ForeignKey(StudySpace, on_delete=models.CASCADE, related_name='flashcards', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_space_flashcards', db_index=True)
    front = models.TextField()
    back = models.TextField()
    card_number = models.PositiveIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'study_space_flashcards'
        ordering = ['card_number']


class StudySpaceFlashcardReview(models.Model):
    CONFIDENCE_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    flashcard = models.ForeignKey(StudySpaceFlashcard, on_delete=models.CASCADE, related_name='reviews', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_space_flashcard_reviews', db_index=True)
    confidence = models.CharField(max_length=10, choices=CONFIDENCE_CHOICES, default='medium')
    review_count = models.PositiveIntegerField(default=0)
    last_reviewed_at = models.BigIntegerField(default=0)
    next_review_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'study_space_flashcard_reviews'
        indexes = [
            models.Index(fields=['user', 'flashcard']),
        ]




class StudySpaceNote(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    space = models.OneToOneField(StudySpace, on_delete=models.CASCADE, related_name='shared_note', db_index=True)
    content = models.TextField(blank=True, default='')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='study_space_notes_updated')
    version = models.PositiveIntegerField(default=1)
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'study_space_notes'


class PageView(models.Model):
    path = models.TextField()
    full_url = models.TextField(blank=True, default='')
    referrer = models.TextField(blank=True, default='')
    referrer_domain = models.CharField(max_length=255, blank=True, default='')
    referrer_type = models.CharField(max_length=20, blank=True, default='')
    utm_source = models.CharField(max_length=255, blank=True, default='')
    utm_medium = models.CharField(max_length=255, blank=True, default='')
    utm_campaign = models.CharField(max_length=255, blank=True, default='')
    user_agent = models.TextField(blank=True, default='')
    source = models.CharField(max_length=10, default='web')
    platform = models.CharField(max_length=30, blank=True, default='')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, default='')
    user_id = models.BigIntegerField(blank=True, null=True)
    user_identifier = models.CharField(max_length=255, blank=True, default='')
    country = models.CharField(max_length=100, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'page_views'
        indexes = [
            models.Index(fields=['created_at'], name='pv_created_at_idx'),
            models.Index(fields=['referrer_type'], name='pv_referrer_type_idx'),
            models.Index(fields=['source'], name='pv_source_idx'),
            models.Index(fields=['user_id'], name='pv_user_id_idx'),
        ]


class DailyStat(models.Model):
    date = models.DateField(unique=True)
    total_visits = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    new_users = models.PositiveIntegerField(default=0)
    web_visits = models.PositiveIntegerField(default=0)
    app_visits = models.PositiveIntegerField(default=0)
    direct_visits = models.PositiveIntegerField(default=0)
    search_visits = models.PositiveIntegerField(default=0)
    social_visits = models.PositiveIntegerField(default=0)
    referral_visits = models.PositiveIntegerField(default=0)
    internal_visits = models.PositiveIntegerField(default=0)
    new_posts = models.PositiveIntegerField(default=0)
    new_resources = models.PositiveIntegerField(default=0)
    new_replies = models.PositiveIntegerField(default=0)
    avg_session_duration = models.FloatField(default=0.0)
    bounce_count = models.PositiveIntegerField(default=0)
    total_sessions = models.PositiveIntegerField(default=0)
    pages_per_session = models.FloatField(default=0.0)
    peak_hour = models.IntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'daily_stats'
        ordering = ['-date']


class StudySpacePresence(models.Model):
    STATUS_INSIDE = 'inside'
    STATUS_READING = 'reading'
    STATUS_TYPING = 'typing'
    STATUS_GENERATING = 'generating'
    STATUS_EDITING = 'editing'
    STATUS_IDLE = 'idle'
    STATUS_CHOICES = [
        (STATUS_INSIDE, 'Inside'),
        (STATUS_READING, 'Reading'),
        (STATUS_TYPING, 'Typing'),
        (STATUS_GENERATING, 'Generating'),
        (STATUS_EDITING, 'Editing'),
        (STATUS_IDLE, 'Idle'),
    ]
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    space = models.ForeignKey(StudySpace, on_delete=models.CASCADE, related_name='presence_rows', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_space_presence', db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_INSIDE, db_index=True)
    current_tab = models.CharField(max_length=40, blank=True, default='')
    current_document_id = models.CharField(max_length=36, blank=True, default='')
    detail = models.CharField(max_length=120, blank=True, default='')
    is_typing = models.BooleanField(default=False)
    session_id = models.CharField(max_length=64, blank=True, default='')
    last_seen_at = models.BigIntegerField(default=0, db_index=True)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'study_space_presence'
        unique_together = ('space', 'user')
        indexes = [
            models.Index(fields=['space', '-last_seen_at']),
            models.Index(fields=['user', '-last_seen_at']),
        ]

class StudyDocument(models.Model):
    STATUS_CHOICES = [
        ('uploading', 'Uploading'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    space = models.ForeignKey(StudySpace, on_delete=models.CASCADE, related_name='documents', db_index=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_documents', db_index=True)
    title = models.CharField(max_length=500, blank=True, default='')
    file_url = models.TextField(blank=True, default='')
    file_name = models.CharField(max_length=500, blank=True, default='')
    file_size = models.PositiveIntegerField(default=0)
    mime_type = models.CharField(max_length=200, blank=True, default='')
    page_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploading')
    parse_status = models.CharField(max_length=20, default='pending')
    parsed_text = models.TextField(blank=True, default='')
    parsed_at = models.BigIntegerField(default=0)
    parse_error = models.TextField(blank=True, default='')
    qwen_file_id = models.CharField(max_length=200, blank=True, default='')
    summary_compact = models.TextField(blank=True, default='')
    summary_detailed = models.TextField(blank=True, default='')
    summary_generated_at = models.BigIntegerField(default=0)
    summary_updated_at = models.BigIntegerField(default=0)
    mindmap_json = models.TextField(blank=True, default='')
    mindmap_generated_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'study_documents'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['space', '-updated_at']),
            models.Index(fields=['user', 'status', '-updated_at'], name='studydoc_user_status_idx'),
            models.Index(fields=['space', 'status', '-updated_at'], name='studydoc_space_status_idx'),
        ]




class StudyDocumentShare(models.Model):
    """Explicit access grants for a Study Lab document shared with specific users."""
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    document = models.ForeignKey(StudyDocument, on_delete=models.CASCADE, related_name='share_grants', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_document_shares', db_index=True)
    granted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_document_grants')
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'study_document_shares'
        unique_together = ('document', 'user')
        indexes = [
            models.Index(fields=['document', 'user']),
            models.Index(fields=['user', '-created_at']),
        ]


class StudyQuiz(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    document = models.ForeignKey(StudyDocument, on_delete=models.CASCADE, related_name='quizzes', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_quizzes', db_index=True)
    title = models.CharField(max_length=500, blank=True, default='')
    question_count = models.PositiveIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'study_quizzes'
        ordering = ['-created_at']


class StudyQuizQuestion(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    quiz = models.ForeignKey(StudyQuiz, on_delete=models.CASCADE, related_name='questions', db_index=True)
    question_number = models.PositiveIntegerField(default=0)
    question_text = models.TextField()
    option_a = models.TextField(blank=True, default='')
    option_b = models.TextField(blank=True, default='')
    option_c = models.TextField(blank=True, default='')
    option_d = models.TextField(blank=True, default='')
    correct_answer = models.CharField(max_length=1, default='A')
    explanation = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'study_quiz_questions'
        ordering = ['question_number']


class StudyQuizAttempt(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    quiz = models.ForeignKey(StudyQuiz, on_delete=models.CASCADE, related_name='attempts', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_quiz_attempts', db_index=True)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    answers = models.TextField(blank=True, default='')  # JSON: {"1":"A","2":"C",...}
    xp_earned = models.PositiveIntegerField(default=0)
    completed_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'study_quiz_attempts'
        ordering = ['-completed_at']


class StudyFlashcard(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    document = models.ForeignKey(StudyDocument, on_delete=models.CASCADE, related_name='flashcards', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_flashcards', db_index=True)
    front = models.TextField()
    back = models.TextField()
    card_number = models.PositiveIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'study_flashcards'
        ordering = ['card_number']


class StudyFlashcardReview(models.Model):
    CONFIDENCE_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    flashcard = models.ForeignKey(StudyFlashcard, on_delete=models.CASCADE, related_name='reviews', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_flashcard_reviews', db_index=True)
    confidence = models.CharField(max_length=10, choices=CONFIDENCE_CHOICES, default='medium')
    review_count = models.PositiveIntegerField(default=0)
    last_reviewed_at = models.BigIntegerField(default=0)
    next_review_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'study_flashcard_reviews'
        indexes = [
            models.Index(fields=['user', 'flashcard']),
        ]


class GenerationJob(models.Model):
    TYPE_SUMMARY = 'summary'
    TYPE_MINDMAP = 'mindmap'
    TYPE_QUIZ = 'quiz'
    TYPE_FLASHCARD = 'flashcard'
    TYPE_CHOICES = [
        (TYPE_SUMMARY, 'Summary'),
        (TYPE_MINDMAP, 'Mindmap'),
        (TYPE_QUIZ, 'Quiz'),
        (TYPE_FLASHCARD, 'Flashcard'),
    ]
    STATUS_QUEUED = 'queued'
    STATUS_PROCESSING = 'processing'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_QUEUED, 'Queued'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    job_type = models.CharField(max_length=20, choices=TYPE_CHOICES, db_index=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_QUEUED, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generation_jobs', db_index=True)
    space = models.ForeignKey(StudySpace, on_delete=models.CASCADE, related_name='generation_jobs', null=True, blank=True)
    document = models.ForeignKey(StudyDocument, on_delete=models.CASCADE, related_name='generation_jobs', null=True, blank=True)
    params = models.TextField(blank=True, default='')
    result = models.TextField(blank=True, default='')
    error = models.TextField(blank=True, default='')
    progress = models.PositiveSmallIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    started_at = models.BigIntegerField(default=0)
    completed_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'generation_jobs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['space', 'job_type', '-created_at']),
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


class Announcement(models.Model):
    """News, announcements, and important notices (e.g., NEB result publication)."""
    CATEGORY_CHOICES = [
        ('exam_results', 'Exam Results'),
        ('notice', 'Notice'),
        ('event', 'Event'),
        ('update', 'Update'),
        ('alert', 'Alert'),
        ('general', 'General'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, db_index=True)
    summary = models.CharField(max_length=500, blank=True, default='')
    content = models.TextField(blank=True, default='')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general', db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    is_pinned = models.BooleanField(default=False, db_index=True)
    cover_image_url = models.TextField(blank=True, default='')
    external_url = models.TextField(blank=True, default='')
    tags = models.CharField(max_length=500, blank=True, default='')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='announcements')
    published_at = models.BigIntegerField(default=0, db_index=True)
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'announcements'
        ordering = ['-is_pinned', '-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['-is_pinned', '-published_at']),
        ]

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    parent_comment = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='children'
    )
    text = models.TextField()
    like_count = models.PositiveIntegerField(default=0)
    reply_count = models.PositiveIntegerField(default=0)
    is_edited = models.BooleanField(default=False)
    edited_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'blog_comments'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['announcement_id', 'created_at']),
            models.Index(fields=['parent_comment_id', 'created_at']),
        ]

    def __str__(self):
        return f"Comment by {self.author_id} on {self.announcement_id}"


class BlogCommentLike(models.Model):
    comment = models.ForeignKey(BlogComment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comment_likes')

    class Meta:
        db_table = 'blog_comment_likes'
        unique_together = ('comment', 'user')


class AccountDeletionRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending Review'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deletion_requests')
    reason = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)
    created_at = models.BigIntegerField()
    scheduled_delete_at = models.BigIntegerField()
    completed_at = models.BigIntegerField(default=0)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='completed_deletions')

    class Meta:
        db_table = 'account_deletion_requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"Deletion request for {self.user_id} ({self.status})"


SOCIAL_PLATFORMS = {
    'instagram':  {'label': 'Instagram',  'icon': 'instagram',   'color': '#E4405F', 'base_url': 'instagram.com'},
    'facebook':   {'label': 'Facebook',   'icon': 'facebook',    'color': '#1877F2', 'base_url': 'facebook.com'},
    'twitter':    {'label': 'X (Twitter)','icon': 'x',            'color': '#000000', 'base_url': 'x.com'},
    'youtube':    {'label': 'YouTube',    'icon': 'youtube',      'color': '#FF0000', 'base_url': 'youtube.com'},
    'tiktok':     {'label': 'TikTok',     'icon': 'tiktok',       'color': '#000000', 'base_url': 'tiktok.com'},
    'linkedin':   {'label': 'LinkedIn',   'icon': 'linkedin',     'color': '#0A66C2', 'base_url': 'linkedin.com'},
    'github':     {'label': 'GitHub',     'icon': 'github',       'color': '#181717', 'base_url': 'github.com'},
    'telegram':   {'label': 'Telegram',   'icon': 'telegram',     'color': '#26A5E4', 'base_url': 't.me'},
    'whatsapp':   {'label': 'WhatsApp',   'icon': 'whatsapp',     'color': '#25D366', 'base_url': 'wa.me'},
    'discord':    {'label': 'Discord',    'icon': 'discord',      'color': '#5865F2', 'base_url': 'discord.com'},
    'snapchat':   {'label': 'Snapchat',   'icon': 'snapchat',     'color': '#FFFC00', 'base_url': 'snapchat.com'},
    'pinterest':  {'label': 'Pinterest',  'icon': 'pinterest',    'color': '#E60023', 'base_url': 'pinterest.com'},
    'reddit':     {'label': 'Reddit',     'icon': 'reddit',       'color': '#FF4500', 'base_url': 'reddit.com'},
    'website':    {'label': 'Website',    'icon': 'language',     'color': '#1B6EF3', 'base_url': ''},
}


class SocialLink(models.Model):
    PLATFORM_CHOICES = [(k, v['label']) for k, v in SOCIAL_PLATFORMS.items()]

    id = models.CharField(max_length=36, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='website')
    url = models.TextField()
    label = models.CharField(max_length=100, blank=True, default='')
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'social_links'
        ordering = ['sort_order', 'created_at']
        indexes = [
            models.Index(fields=['user_id', 'sort_order']),
        ]

    def __str__(self):
        return f"{self.user_id} - {self.platform}: {self.url[:50]}"


class SocialLinkClick(models.Model):
    link = models.ForeignKey(SocialLink, on_delete=models.CASCADE, related_name='clicks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='link_clicks')
    clicker_id = models.BigIntegerField(blank=True, null=True)
    is_follower = models.BooleanField(null=True, blank=True)
    clicker_country = models.CharField(max_length=100, blank=True, default='')
    clicker_gender = models.CharField(max_length=20, blank=True, default='')
    clicker_age = models.PositiveSmallIntegerField(null=True, blank=True)
    platform = models.CharField(max_length=20, db_index=True)
    url = models.TextField()
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'social_link_clicks'
        indexes = [
            models.Index(fields=['user_id', 'created_at']),
            models.Index(fields=['platform']),
            models.Index(fields=['is_follower']),
        ]

    def __str__(self):
        return f"click {self.platform} on user {self.user_id}"


class HeroBackground(models.Model):
    name = models.CharField(max_length=100)
    filename = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'hero_backgrounds'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f"{self.name} ({self.filename}){' [ACTIVE]' if self.is_active else ''}"


class PostView(models.Model):
    """Record of who viewed a forum post (admin-only analytics)."""
    id = models.CharField(max_length=36, primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_views')
    viewed_at = models.BigIntegerField()

    class Meta:
        db_table = 'post_views'
        unique_together = ('post', 'user', 'viewed_at')
        indexes = [
            models.Index(fields=['post_id', '-viewed_at']),
            models.Index(fields=['user_id']),
        ]

    def __str__(self):
        return f"view {self.post_id} by user {self.user_id}"


class BackgroundAgentCredential(models.Model):
    admin_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='background_agent_credential')
    github_user_id = models.BigIntegerField(default=0)
    github_login = models.CharField(max_length=255, blank=True, default='')
    github_avatar_url = models.TextField(blank=True, default='')
    encrypted_access_token = models.TextField(blank=True, default='')
    token_scopes = models.TextField(blank=True, default='')
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)
    last_validated_at = models.BigIntegerField(default=0)
    revoked_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'background_agent_credentials'

    @property
    def is_connected(self):
        return bool(self.encrypted_access_token) and not self.revoked_at


class BackgroundAgentProject(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'), ('syncing', 'Syncing'), ('ready', 'Ready'),
        ('error', 'Error'), ('archived', 'Archived'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='background_agent_projects')
    credential = models.ForeignKey(BackgroundAgentCredential, on_delete=models.PROTECT, related_name='projects')
    github_repo_id = models.BigIntegerField(default=0)
    repo_full_name = models.CharField(max_length=255)
    repo_html_url = models.TextField(blank=True, default='')
    clone_url = models.TextField()
    default_branch = models.CharField(max_length=255, default='main')
    preferred_base_branch = models.CharField(max_length=255, blank=True, default='')
    is_private = models.BooleanField(default=False)
    autofix_enabled = models.BooleanField(
        default=True,
        help_text='When a GitHub Actions run fails for this repo, queue an agent session with the failing job log.',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', db_index=True)
    mirror_path = models.TextField(blank=True, default='')
    last_synced_at = models.BigIntegerField(default=0)
    last_error = models.TextField(blank=True, default='')
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'background_agent_projects'
        ordering = ['-updated_at']
        constraints = [
            models.UniqueConstraint(fields=['admin_user', 'repo_full_name'], name='uniq_bg_agent_admin_repo'),
        ]
        indexes = [
            models.Index(fields=['admin_user', '-updated_at'], name='bg_project_admin_updated_idx'),
            models.Index(fields=['status', '-updated_at'], name='bg_project_status_updated_idx'),
        ]


class BackgroundAgentAutofixRun(models.Model):
    """Records a CI-failure-triggered auto-fix session for a project.

    Guards double work: one session per failing workflow run, and one per
    head SHA (a run re-triggered on the same commit is not fixed twice).
    """
    id = models.CharField(max_length=36, primary_key=True)
    project = models.ForeignKey(BackgroundAgentProject, on_delete=models.CASCADE, related_name='autofix_runs')
    run_id = models.BigIntegerField(default=0)
    head_sha = models.CharField(max_length=64, blank=True, default='')
    branch = models.CharField(max_length=255, blank=True, default='')
    workflow_name = models.CharField(max_length=255, blank=True, default='')
    session = models.ForeignKey(
        'BackgroundAgentSession', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='autofix_origin'
    )
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'background_agent_autofix_runs'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['project', 'run_id'], name='uniq_bg_autofix_project_run'),
        ]
        indexes = [
            models.Index(fields=['project', '-created_at'], name='bg_autofix_project_created_idx'),
            models.Index(fields=['project', 'head_sha'], name='bg_autofix_project_sha_idx'),
        ]


class BackgroundAgentSession(models.Model):
    STATUS_CHOICES = [
        ('queued', 'Queued'), ('preparing', 'Preparing'), ('running', 'Running'),
        ('paused', 'Paused'), ('waiting', 'Waiting for input'), ('completed', 'Completed'),
        ('failed', 'Failed'), ('cancelled', 'Cancelled'),
    ]
    CONTROL_CHOICES = [
        ('', 'None'), ('pause', 'Pause'), ('stop', 'Stop'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    project = models.ForeignKey(BackgroundAgentProject, on_delete=models.CASCADE, related_name='sessions')
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='background_agent_sessions')
    bot_config = models.ForeignKey('BotConfig', on_delete=models.SET_NULL, null=True, blank=True, related_name='background_agent_sessions')
    title = models.CharField(max_length=255, blank=True, default='')
    goal = models.TextField()
    source_branch = models.CharField(max_length=255)
    work_branch = models.CharField(max_length=255, blank=True, default='')
    base_sha = models.CharField(max_length=64, blank=True, default='')
    head_sha = models.CharField(max_length=64, blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued', db_index=True)
    control_state = models.CharField(max_length=10, choices=CONTROL_CHOICES, blank=True, default='')
    progress = models.PositiveSmallIntegerField(default=0)
    progress_label = models.CharField(max_length=255, blank=True, default='Queued')
    iteration = models.PositiveIntegerField(default=0)
    max_iterations = models.PositiveIntegerField(default=30)
    workspace_path = models.TextField(blank=True, default='')
    agent_state = models.TextField(blank=True, default='{}')
    context_summary = models.TextField(blank=True, default='')
    context_tokens_estimate = models.PositiveIntegerField(default=0)
    context_window_tokens = models.PositiveIntegerField(default=131072)
    context_compactions = models.PositiveIntegerField(default=0)
    context_compacted_at = models.BigIntegerField(default=0)
    last_compaction_at = models.BigIntegerField(default=0)
    # Operator-requested manual compaction (/compact) — consumed by the runner.
    compact_requested_at = models.BigIntegerField(default=0)
    # Live task-plan checklist the agent maintains via the update_plan tool.
    todos_json = models.TextField(blank=True, default='[]')
    # LLM selection for this session. Empty llm_provider = legacy default
    # (the shared Qwen web bot). Official presets ('agnes', 'openai',
    # 'anthropic', 'gemini', 'deepseek') resolve per the api.llm registry;
    # 'custom' + llm_provider_id refers to the user's own BYOK provider row.
    llm_provider = models.CharField(max_length=40, blank=True, default='')
    llm_model = models.CharField(max_length=200, blank=True, default='')
    llm_provider_id = models.CharField(max_length=36, blank=True, default='')
    summary = models.TextField(blank=True, default='')
    final_diff = models.TextField(blank=True, default='')
    changed_files = models.TextField(blank=True, default='[]')
    test_summary = models.TextField(blank=True, default='')
    last_error = models.TextField(blank=True, default='')
    worker_id = models.CharField(max_length=128, blank=True, default='')
    last_heartbeat_at = models.BigIntegerField(db_index=True, default=0)
    created_at = models.BigIntegerField(default=0)
    started_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)
    completed_at = models.BigIntegerField(default=0)
    archived_at = models.BigIntegerField(default=0, db_index=True)

    class Meta:
        db_table = 'background_agent_sessions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at'], name='bg_session_status_created_idx'),
            models.Index(fields=['admin_user', '-created_at'], name='bg_session_admin_created_idx'),
            models.Index(fields=['project', '-created_at'], name='bg_session_project_created_idx'),
        ]


class BackgroundAgentMessage(models.Model):
    ROLE_CHOICES = [
        ('system', 'System'), ('user', 'User'), ('assistant', 'Assistant'), ('tool', 'Tool'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    session = models.ForeignKey(BackgroundAgentSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, db_index=True)
    content = models.TextField()
    metadata = models.TextField(blank=True, default='{}')
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'background_agent_messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['session', 'created_at'], name='bg_message_session_created_idx'),
        ]


class BackgroundAgentAttachment(models.Model):
    KIND_CHOICES = [
        ('text', 'Text'), ('image', 'Image'), ('pdf', 'PDF'),
        ('document', 'Document'), ('audio', 'Audio'), ('video', 'Video'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    session = models.ForeignKey(BackgroundAgentSession, on_delete=models.CASCADE, related_name='attachments')
    message = models.ForeignKey(BackgroundAgentMessage, on_delete=models.CASCADE, related_name='attachments')
    file_name = models.CharField(max_length=255)
    stored_name = models.CharField(max_length=255)
    file_path = models.TextField()
    content_type = models.CharField(max_length=160, blank=True, default='application/octet-stream')
    extension = models.CharField(max_length=24, blank=True, default='')
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default='document', db_index=True)
    size_bytes = models.BigIntegerField(default=0)
    sha256 = models.CharField(max_length=64, blank=True, default='')
    sent_iteration = models.PositiveIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'background_agent_attachments'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['session', 'created_at'], name='bg_attach_session_created_idx'),
            models.Index(fields=['message', 'created_at'], name='bg_attach_message_created_idx'),
        ]


class BackgroundAgentEvent(models.Model):
    id = models.BigAutoField(primary_key=True)
    session = models.ForeignKey(BackgroundAgentSession, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=64, db_index=True)
    message = models.TextField(blank=True, default='')
    payload = models.TextField(blank=True, default='{}')
    created_at = models.BigIntegerField(db_index=True, default=0)

    class Meta:
        db_table = 'background_agent_events'
        ordering = ['id']
        indexes = [
            models.Index(fields=['session', 'id'], name='bg_event_session_id_idx'),
        ]


class BackgroundAgentArtifact(models.Model):
    KIND_CHOICES = [
        ('changes_zip', 'Changed files ZIP'),
        ('patch', 'Git patch'),
        ('log', 'Execution log'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    session = models.ForeignKey(BackgroundAgentSession, on_delete=models.CASCADE, related_name='artifacts')
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, db_index=True)
    file_path = models.TextField()
    file_name = models.CharField(max_length=255)
    size_bytes = models.BigIntegerField(default=0)
    sha256 = models.CharField(max_length=64, blank=True, default='')
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'background_agent_artifacts'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['session', 'kind'], name='uniq_bg_artifact_session_kind'),
        ]


class BackgroundAgentAction(models.Model):
    ACTION_CHOICES = [
        ('push', 'Push branch'),
        ('open_pr', 'Open pull request'),
        ('refresh', 'Refresh repository'),
        ('artifacts', 'Rebuild artifacts'),
    ]
    STATUS_CHOICES = [
        ('queued', 'Queued'), ('processing', 'Processing'),
        ('completed', 'Completed'), ('failed', 'Failed'), ('cancelled', 'Cancelled'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    session = models.ForeignKey(BackgroundAgentSession, on_delete=models.CASCADE, related_name='actions')
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='background_agent_actions')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued', db_index=True)
    payload = models.TextField(blank=True, default='{}')
    result = models.TextField(blank=True, default='{}')
    error = models.TextField(blank=True, default='')
    worker_id = models.CharField(max_length=128, blank=True, default='')
    created_at = models.BigIntegerField(default=0)
    started_at = models.BigIntegerField(default=0)
    completed_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'background_agent_actions'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['status', 'created_at'], name='bg_action_status_created_idx'),
            models.Index(fields=['session', 'created_at'], name='bg_action_session_created_idx'),
        ]


class BackgroundAgentWorker(models.Model):
    STATUS_CHOICES = [
        ('starting', 'Starting'), ('idle', 'Idle'),
        ('busy', 'Busy'), ('stopping', 'Stopping'),
    ]
    worker_id = models.CharField(max_length=255, primary_key=True)
    hostname = models.CharField(max_length=255, blank=True, default='')
    process_id = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='starting', db_index=True)
    current_kind = models.CharField(max_length=20, blank=True, default='')
    current_id = models.CharField(max_length=36, blank=True, default='')
    started_at = models.BigIntegerField(default=0)
    last_heartbeat_at = models.BigIntegerField(db_index=True, default=0)

    class Meta:
        db_table = 'background_agent_workers'
        ordering = ['worker_id']
        indexes = [
            models.Index(fields=['status', '-last_heartbeat_at'], name='bg_worker_status_heartbeat_idx'),
        ]



class BackgroundAgentDevicePairing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('approved', 'Approved'),
        ('consumed', 'Consumed'), ('expired', 'Expired'), ('denied', 'Denied'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    device_code_hash = models.CharField(max_length=64, unique=True)
    user_code = models.CharField(max_length=12, unique=True, db_index=True)
    device_name = models.CharField(max_length=120, blank=True, default='Zeus')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='background_agent_pairings', db_constraint=False)
    created_at = models.BigIntegerField(default=0)
    expires_at = models.BigIntegerField(db_index=True, default=0)
    approved_at = models.BigIntegerField(default=0)
    consumed_at = models.BigIntegerField(default=0)
    last_polled_at = models.BigIntegerField(default=0)
    poll_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'background_agent_device_pairings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'expires_at'], name='bg_pair_status_expiry_idx'),
        ]


class BackgroundAgentDeviceToken(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='background_agent_device_tokens', db_constraint=False)
    token_hash = models.CharField(max_length=64, unique=True, db_index=True)
    device_name = models.CharField(max_length=120, blank=True, default='Zeus')
    scopes = models.CharField(max_length=255, default='agent:read,agent:write,repo:read,artifact:read')
    created_at = models.BigIntegerField(default=0)
    last_used_at = models.BigIntegerField(default=0)
    expires_at = models.BigIntegerField(default=0, db_index=True)
    revoked_at = models.BigIntegerField(default=0, db_index=True)

    class Meta:
        db_table = 'background_agent_device_tokens'
        ordering = ['-last_used_at', '-created_at']
        indexes = [
            models.Index(fields=['admin_user', '-last_used_at'], name='bg_device_admin_used_idx'),
        ]


class UserLLMProvider(models.Model):
    """A user's personal LLM connection (BYOK).

    Two shapes:
      * `provider = 'custom'` — fully user-defined endpoint: any name, base
        URL, API format and model list. Works for OpenRouter, Groq, Together,
        Ollama (OpenAI-compatible), LM Studio, vLLM, company gateways, ...
      * `provider = <preset slug>` ('agnes', 'openai', 'anthropic', 'gemini',
        'deepseek') — the user's own key for a known official provider, which
        overrides admin-shared and server-env credentials for that user.

    Keys are AES-GCM encrypted at rest (api.llm.crypto) and never leave the
    server — browsers/apps only ever see masked versions.
    """
    FORMAT_CHOICES = [
        ('openai', 'OpenAI-compatible (chat completions)'),
        ('anthropic', 'Anthropic Messages API'),
        ('gemini', 'Google Gemini API'),
    ]

    id = models.CharField(max_length=36, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='llm_providers')
    name = models.CharField(max_length=100, blank=True, default='')
    provider = models.CharField(max_length=40, db_index=True)
    api_format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='openai')
    base_url = models.TextField(blank=True, default='')
    api_key = models.TextField(blank=True, default='')
    models_json = models.TextField(blank=True, default='[]')
    default_model = models.CharField(max_length=200, blank=True, default='')
    context_window = models.PositiveIntegerField(default=131072)
    max_output_tokens = models.PositiveIntegerField(default=4096)
    enabled = models.BooleanField(default=True, db_index=True)
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'user_llm_providers'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', 'provider', 'enabled'], name='llmprov_user_slug_idx'),
        ]

    def __str__(self):
        return f"{self.name or self.provider} ({self.user_id})"

