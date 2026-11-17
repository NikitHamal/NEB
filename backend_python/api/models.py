"""
Django models for NEBians.
Schema is the source of truth — keep in sync with the Kotlin app's ApiService.
"""
import json
import time
import uuid
from decimal import Decimal
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
    username_changed_at = models.BigIntegerField(default=0)
    username_change_count = models.PositiveIntegerField(default=0)
    avatar_bg = models.CharField(max_length=16, default='', blank=True)
    avatar_hue = models.IntegerField(default=-1)
    avatar_tone = models.FloatField(default=-1.0)
    avatar_anim = models.CharField(max_length=16, default='', blank=True)
    avatar_shape = models.CharField(max_length=16, default='', blank=True)
    avatar_expression = models.CharField(max_length=16, default='', blank=True)
    avatar_color = models.CharField(max_length=7, default='', blank=True)
    avatar_bg_color = models.CharField(max_length=7, default='', blank=True)
    avatar_eye_color = models.CharField(max_length=7, default='', blank=True)
    avatar_use_pp = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True, db_index=True)
    # Address awaiting confirmation during an email change. `email` only
    # moves once a code sent to this address is handed back, so an account
    # can never end up pointing at a mailbox its owner does not control.
    pending_email = models.EmailField(blank=True, null=True)
    photo_url = models.TextField(blank=True, null=True)
    banner_url = models.TextField(blank=True, null=True)
    # Id of a cover from the M3X art library (cover-NNN). Empty = the default role cover.
    cover_art = models.CharField(max_length=16, blank=True, default='')
    display_name = models.CharField(max_length=150, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STUDENT, db_index=True)
    dob = models.CharField(max_length=20, default='')
    gender = models.CharField(max_length=20, blank=True, null=True)
    class_level = models.CharField(max_length=40, blank=True, null=True, db_column='class')
    # Education situation. `class_level` is the level; these say what is going on
    # at that level (see api/education_catalog.py). All optional.
    edu_status = models.CharField(max_length=20, blank=True, default='')
    edu_program = models.CharField(max_length=100, blank=True, default='')
    edu_term = models.CharField(max_length=40, blank=True, default='')
    edu_completed = models.CharField(max_length=40, blank=True, default='')
    # Portfolio header: a one-line headline, skills and what the person is open to.
    headline = models.CharField(max_length=120, blank=True, default='')
    skills = models.TextField(blank=True, default='')  # comma-separated
    open_to = models.CharField(max_length=300, blank=True, default='')  # comma-separated keys
    subjects = models.TextField(blank=True, null=True)  # comma-separated
    teaching_subjects = models.TextField(blank=True, default='')  # teacher-specific: comma-separated
    institution_type = models.CharField(max_length=30, blank=True, default='')  # school/college/academy/other
    teach_levels = models.CharField(max_length=200, blank=True, db_default='', default='')  # teacher: comma-separated level keys
    experience_years = models.PositiveSmallIntegerField(db_default=0, default=0)  # teacher: years of teaching
    employment = models.CharField(max_length=20, blank=True, db_default='', default='')  # teacher: full_time/part_time/tutor/freelance
    pradesh = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    school = models.CharField(max_length=200, blank=True, null=True)
    school_username = models.CharField(max_length=50, blank=True, default='')
    school_slug = models.CharField(max_length=90, blank=True, default='', db_index=True)
    bio = models.TextField(blank=True, default='')
    is_locked = models.BooleanField(default=False)
    # Administrative ban. DISTINCT from is_locked (which is the user's own
    # private-profile toggle): banned users cannot authenticate anywhere.
    is_banned = models.BooleanField(default=False)
    enable_inline_images = models.BooleanField(default=True)
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
    # Library autopilot: tell me when a resource lands for my class and subjects. On by
    # default, one switch on web and in the app (api/resource_alerts.py).
    notify_new_resources = models.BooleanField(default=True)

    # Marketplace economy — Nebians points, AI credits (persistent + monthly free), spend
    nebians_points = models.PositiveIntegerField(default=0)
    ai_credits = models.PositiveIntegerField(default=0)
    free_credits = models.PositiveIntegerField(default=0)
    free_credits_month = models.CharField(max_length=7, blank=True, default='')
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        db_table = 'users'
        indexes = [
            # People suggestions: classmates and schoolmates.
            models.Index(fields=['school'], name='users_school_idx'),
            models.Index(fields=['class_level'], name='users_class_idx'),
        ]

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
    # Milliseconds epoch after which the token is refused. 0 means "unset"
    # and is treated as expired (fail closed); the migration backfills it.
    expires_at = models.BigIntegerField(default=0)

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
    download_count = models.PositiveIntegerField(default=0)
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
    # Marketplace paid content fields
    is_paid = models.BooleanField(default=False, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

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
            models.Index(fields=['is_paid']),
            # The library feed's sorts, each with its tie-breakers so MySQL can read the page
            # straight off the index instead of sorting every approved resource: newest/default
            # (-added_at, -view_count), trending (-view_count, -like_count, -added_at) and
            # liked (-like_count, -added_at).
            models.Index(fields=['approval_status', 'is_lead', '-added_at', '-view_count'], name='res_appr_lead_newest_idx'),
            models.Index(fields=['approval_status', 'is_lead', '-view_count', '-like_count', '-added_at'], name='res_appr_lead_trend_idx'),
            models.Index(fields=['approval_status', 'is_lead', '-like_count', '-added_at'], name='res_appr_lead_liked_idx'),
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
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
    is_resolved = models.BooleanField(default=False)
    accepted_reply_id = models.CharField(max_length=36, blank=True, default='')
    # Dynamic post look (api/post_look.py): JSON string, '' is the plain post.
    look = models.CharField(max_length=400, blank=True, default='')
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
            models.Index(fields=['is_archived', '-reply_count', '-created_at'], name='post_arch_discussed_idx'),
            # Per-author counts (profile stats, popup, profile tabs) and the forum's COUNT(*),
            # answered from the index alone.
            models.Index(fields=['user_id', 'is_archived', 'is_anonymous'], name='post_user_arch_anon_idx'),
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
    thumbnail_url = models.TextField(blank=True, default='')
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
    # A poll belongs to a post OR to a reply (comment poll), never both.
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='poll', null=True, blank=True)
    reply = models.OneToOneField('Reply', on_delete=models.CASCADE, related_name='poll', null=True, blank=True)
    # Facebook-style: anyone who can vote may append an option of their own.
    allow_add_options = models.BooleanField(default=False)
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
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='added_poll_options')
    created_at = models.BigIntegerField(default=0)

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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    content = models.TextField()
    thumbs_up_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    is_edited = models.BooleanField(default=False)
    edited_at = models.BigIntegerField(default=0)
    is_archived = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    kind = models.CharField(max_length=12, blank=True, default='comment')
    label = models.CharField(max_length=12, blank=True, default='')
    labeled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    labeled_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'replies'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post_id', 'created_at']),
            models.Index(fields=['parent_reply_id', 'created_at']),
            models.Index(fields=['post_id', 'is_archived', '-thumbs_up_count', 'created_at'], name='reply_post_rank_idx'),
            models.Index(fields=['user_id', '-created_at'], name='reply_user_created_idx'),
            models.Index(fields=['user_id', 'is_archived', 'is_anonymous'], name='reply_user_arch_anon_idx'),
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
            # Followers / following lists, newest first.
            models.Index(fields=['following_id', '-created_at'], name='follow_following_created_idx'),
            models.Index(fields=['follower_id', '-created_at'], name='follow_follower_created_idx'),
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
        ('new_resource', 'New resource for you'),
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
    # Push campaign this row belongs to (api.push_engine); '' for ordinary activity.
    campaign_id = models.CharField(max_length=36, blank=True, default='')
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resource_comments')
    parent_comment = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='children'
    )
    content = models.TextField()
    like_count = models.PositiveIntegerField(default=0)
    reply_count = models.PositiveIntegerField(default=0)
    is_edited = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
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


class ResourceCommentMedia(models.Model):
    """Attachments (voice notes, audio, video, files) on resource comments —
    mirrors PostMedia for forum posts/replies so every comment bar can carry
    recorded voice or picked media."""
    KIND_CHOICES = (
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('file', 'File'),
    )
    id = models.CharField(max_length=36, primary_key=True)
    comment = models.ForeignKey(ResourceComment, on_delete=models.CASCADE, related_name='media')
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default='file')
    url = models.TextField()
    name = models.CharField(max_length=255, blank=True, default='')
    mime_type = models.CharField(max_length=120, blank=True, default='')
    size_bytes = models.BigIntegerField(default=0)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'resource_comment_media'
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['comment_id', 'order']),
        ]


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
        ('qwencloud', 'Qwen Cloud (qwencloud.com ??? 11 models, free)'),
        ('tryingopen', 'TryingOpen (tryingopen.com ??? 16 open models, free)'),
        ('longcat', 'LongCat (longcat.chat ??? free, no login)'),
        ('geminiweb', 'Gemini Web (gemini.google.com ??? anonymous Flash-Lite)'),
        ('yqcloud', 'Yqcloud (chat9.yqcloud.top — free, no login)'),
        ('chatjimmy', 'ChatJimmy (chatjimmy.ai — Llama 3.1 8B, no login)'),
        ('unikey', 'Unikey (getunikey.ai — 12 models, free trial, no login)'),
        ('ptero', 'Ptero (ptero.pro — 12 models, free, no login)'),
        ('deepai', 'DeepAI (deepai.org)'),
        ('inception', 'Inception Labs (Mercury 3)'),
        ('k2think', 'K2 Horizon (chat.ifm.ai — MBZUAI 375B reasoning)'),
        ('poolside', 'Poolside (chat.poolside.ai — Laguna 2.1)'),
        ('custom', 'Custom OpenAI-compatible endpoint'),
        # Official API providers (handled through api.llm — real API formats,
        # not the web scrapers above).
        ('agnes', 'Agnes 2.0 Flash (Sapiens AI — official API, currently free)'),
        ('openai', 'OpenAI (ChatGPT official API)'),
        ('anthropic', 'Anthropic (Claude official API)'),
        ('gemini', 'Google Gemini (official API)'),
        ('deepseek', 'DeepSeek (official API)'),
        ('llm7', 'LLM7 (llm7.io — free, no key)'),
        ('kilo', 'Kilo Gateway (kilo.ai — free :free models, no key)'),
        ('zen', 'OpenCode Zen (opencode.ai — free -free models, no key)'),
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
    model = models.CharField(max_length=200, default='qwen3.8-max')
    fallback_chain = models.TextField(
        blank=True, default='[]',
        help_text='JSON list of fallback provider entries tried in order when the primary provider fails. '
                  'Each entry: {"provider": slug, "model": "...", "api_url": "...", "api_key": "..."}.',
    )
    system_prompt = models.TextField(
        default="You are Neby, a friendly and helpful AI assistant for NEBians — Nepal's learning community platform for teachers, learners, explorers, students, and parents across all levels, faculties, and fields. "
                'You help with questions, explain concepts clearly, and assist with resources and learning.\n\n'
                'Rules:\n'
                '- Answer the question directly and accurately. Do NOT force curriculum references.\n'
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

    def get_fallback_chain(self):
        """Ordered fallback provider entries as a list of dicts."""
        try:
            chain = self.fallback_chain or '[]'
            if isinstance(chain, str):
                chain = json.loads(chain or '[]')
            if not isinstance(chain, list):
                return []
            return [e for e in chain if isinstance(e, dict) and (e.get('provider') or '').strip()][:15]
        except (ValueError, TypeError):
            return []

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

    Supports multiple providers via web proxies:
      - 'qwen': the Qwen proxy (browser-spoofed session, supports file uploads)
      - 'qwencloud', 'deepai', 'inception': other arena-style proxies
        (qwencloud keeps "session_id|tab_code" in arena_token_id)

    Each session maps to one remote session ID and is bound to provider-specific
    credentials. For Qwen, qwen_chat_id is the Qwen chat ID; for others,
    arena_session_id and arena_token_id are used.
    """
    PROVIDER_CHOICES = [
        ('qwen', 'Qwen (chat.qwen.ai)'),
        ('qwencloud', 'Qwen Cloud (qwencloud.com — 11 models, free)'),
        ('tryingopen', 'TryingOpen (tryingopen.com — 16 open models, free)'),
        ('deepai', 'DeepAI (deepai.org)'),
        ('inception', 'Inception Labs (Mercury 3)'),
        ('k2think', 'K2 Horizon (chat.ifm.ai — MBZUAI 375B reasoning)'),
        ('poolside', 'Poolside (chat.poolside.ai — Laguna 2.1)'),
        ('yqcloud', 'Yqcloud (chat9.yqcloud.top — free, no login)'),
        ('chatjimmy', 'ChatJimmy (chatjimmy.ai — Llama 3.1 8B, no login)'),
        ('unikey', 'Unikey (getunikey.ai — 12 models, free trial, no login)'),
        ('ptero', 'Ptero (ptero.pro — 12 models, free, no login)'),
    ]
    id = models.CharField(max_length=36, primary_key=True)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='arena_sessions', db_index=True,
    )
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='qwen')
    arena_session_id = models.CharField(max_length=64, db_index=True)
    arena_token_id = models.CharField(max_length=128, blank=True, default='')
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
    """One anonymous page view. Written by nebians.analytics, read by the admin
    Analytics page. See docs/ANALYTICS.md.

    No raw IP address, user agent or query string is stored for new rows. A
    visitor is a pseudonymous hash (daily-rotating for logged-out visitors) and
    a session is a run of hits from one visitor with no 30 minute gap.
    """
    path = models.TextField()
    page_key = models.CharField(max_length=200, blank=True, default='')
    referrer = models.TextField(blank=True, default='')  # host + path, no query string
    referrer_domain = models.CharField(max_length=255, blank=True, default='')
    # Channel: direct / search / social / email / ai / referral / campaign / internal
    referrer_type = models.CharField(max_length=20, blank=True, default='')
    referrer_name = models.CharField(max_length=80, blank=True, default='')
    utm_source = models.CharField(max_length=255, blank=True, default='')
    utm_medium = models.CharField(max_length=255, blank=True, default='')
    utm_campaign = models.CharField(max_length=255, blank=True, default='')
    source = models.CharField(max_length=10, default='web')  # web | app
    platform = models.CharField(max_length=30, blank=True, default='')  # OS family
    device_class = models.CharField(max_length=10, blank=True, default='')  # mobile | tablet | desktop | other
    browser = models.CharField(max_length=30, blank=True, default='')
    visitor_id = models.CharField(max_length=24, blank=True, default='')
    session_id = models.CharField(max_length=24, blank=True, default='')
    is_entry = models.BooleanField(default=False)  # first hit of its session
    is_bot = models.BooleanField(default=False)
    user_identifier = models.CharField(max_length=255, blank=True, default='')  # account id when signed in
    country = models.CharField(max_length=100, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    created_at = models.BigIntegerField(default=0)

    # LEGACY: only populated on rows written before the analytics rebuild.
    # `manage.py backfill_analytics` derives the new fields from them and then
    # scrubs ip_address / user_agent / full_url. Safe to drop in a later migration.
    full_url = models.TextField(blank=True, default='')
    user_agent = models.TextField(blank=True, default='')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, default='')
    user_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'page_views'
        indexes = [
            models.Index(fields=['created_at'], name='pv_created_at_idx'),
            models.Index(fields=['referrer_type'], name='pv_referrer_type_idx'),
            models.Index(fields=['source'], name='pv_source_idx'),
            models.Index(fields=['user_id'], name='pv_user_id_idx'),
        ]


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
    rich_content = models.JSONField(default=dict, blank=True)
    source_resource_id = models.CharField(max_length=36, blank=True, default='')
    source_label = models.CharField(max_length=255, blank=True, default='')
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
        ('news', 'News'),
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
    # Autopilot imports (services/news_sync.py). `source_key` names the feed in
    # services/news_sources.py, `source_guid` is the item's stable id there, so
    # a re-run never creates the same story twice. Hand-written posts leave all
    # of these empty.
    source_key = models.CharField(max_length=40, blank=True, default='', db_index=True)
    source_name = models.CharField(max_length=120, blank=True, default='')
    source_guid = models.CharField(max_length=300, blank=True, default='')
    source_official = models.BooleanField(default=False)
    attachments = models.JSONField(blank=True, default=list)

    class Meta:
        db_table = 'announcements'
        ordering = ['-is_pinned', '-published_at', '-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['source_key', 'source_guid'],
                condition=~models.Q(source_guid=''),
                name='uniq_announcement_source_item',
            ),
        ]
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['-is_pinned', '-published_at']),
        ]

    def __str__(self):
        return self.title


class NewsSyncState(models.Model):
    """One row per auto-import source: whether it is on, and how its last run went."""
    key = models.CharField(max_length=40, primary_key=True)
    enabled = models.BooleanField(default=True)
    last_run_at = models.BigIntegerField(default=0)
    last_ok_at = models.BigIntegerField(default=0)
    last_status = models.CharField(max_length=300, blank=True, default='')
    last_new = models.PositiveIntegerField(default=0)
    total_imported = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'news_sync_state'

    def __str__(self):
        return self.key


class BlogComment(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_comments')
    parent_comment = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='children'
    )
    text = models.TextField()
    like_count = models.PositiveIntegerField(default=0)
    reply_count = models.PositiveIntegerField(default=0)
    is_edited = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
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


class ContentImage(models.Model):
    """A normalised image that can be embedded inline inside any text
    content (posts, replies, comments) via a [[img:ID]] token.

    Files are stored under media content_images/<id>.webp (+<id>t.webp
    thumbnail, <id>.gif for animated uploads) so URLs are derivable from
    the id alone. Rows are immutable after creation; sha256 dedupes
    identical uploads. `used` flips once saved content references the row;
    cleanup purges unused rows older than 48h.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='content_images')
    file = models.FileField(upload_to='content_images/', max_length=255)
    thumb = models.FileField(upload_to='content_images/', max_length=255)
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    size = models.PositiveIntegerField(default=0)
    sha256 = models.CharField(max_length=64, db_index=True)
    is_animated = models.BooleanField(default=False)
    used = models.BooleanField(default=False)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'content_images'
        indexes = [
            models.Index(fields=['used', 'created_at']),
        ]

    def __str__(self):
        return f"ContentImage {self.id}"


class BlogCommentMedia(models.Model):
    """Attachments (voice notes, audio, video, files) on blog/news comments —
    mirrors PostMedia/ResourceCommentMedia so every comment bar can carry
    recorded voice or picked media."""
    KIND_CHOICES = (
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('file', 'File'),
    )
    id = models.CharField(max_length=36, primary_key=True)
    comment = models.ForeignKey(BlogComment, on_delete=models.CASCADE, related_name='media')
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default='file')
    url = models.TextField()
    name = models.CharField(max_length=255, blank=True, default='')
    mime_type = models.CharField(max_length=120, blank=True, default='')
    size_bytes = models.BigIntegerField(default=0)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'blog_comment_media'
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['comment_id', 'order']),
        ]


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


class ProfileEntry(models.Model):
    """One line of a person's portfolio: a course, a job, a project, a prize."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_entries')
    kind = models.CharField(max_length=16, db_index=True)
    title = models.CharField(max_length=150)
    org = models.CharField(max_length=150, blank=True, default='')
    start = models.CharField(max_length=7, blank=True, default='')  # YYYY or YYYY-MM
    end = models.CharField(max_length=7, blank=True, default='')
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True, default='')
    url = models.CharField(max_length=300, blank=True, default='')
    position = models.PositiveSmallIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'profile_entries'
        ordering = ['kind', 'position', '-created_at']
        indexes = [models.Index(fields=['user', 'kind'], name='profile_entry_user_kind')]

    def __str__(self):
        return f"{self.user_id} {self.kind}: {self.title}"


class SocialLinkClick(models.Model):
    link = models.ForeignKey(SocialLink, on_delete=models.CASCADE, related_name='clicks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='link_clicks')
    clicker_id = models.CharField(max_length=255, blank=True, null=True)
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


class SiteTheme(models.Model):
    """A site theme an admin switched on or scheduled. The themes themselves live in
    ``web/site_themes.py``; this row only says which one, and when."""
    key = models.CharField(max_length=32)
    starts_on = models.DateField(null=True, blank=True)
    ends_on = models.DateField(null=True, blank=True)
    is_forced = models.BooleanField(default=False, help_text='On right now, whatever the dates say.')
    show_in_app = models.BooleanField(default=True)
    show_greeting = models.BooleanField(default=True)
    note = models.CharField(max_length=120, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'site_themes'
        ordering = ['-is_forced', 'starts_on', 'id']
        indexes = [models.Index(fields=['is_forced', 'starts_on', 'ends_on'], name='site_theme_window_idx')]

    def __str__(self):
        when = 'now' if self.is_forced else f'{self.starts_on} to {self.ends_on}'
        return f'{self.key} ({when})'


class NebyConfig(models.Model):
    """How pixel Neby looks and behaves across the site and the app. One row; the newest wins.
    The looks themselves live in the apps (``web/neby_looks.py`` names them). ``auto`` dresses
    Neby for whichever festival theme is live."""
    look = models.CharField(max_length=24, default='auto')
    ambient = models.BooleanField(default=True, help_text='Idle Neby looks around, waves and hops now and then.')
    reactions = models.BooleanField(default=True, help_text='Tapping Neby plays a reaction.')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'neby_config'

    def __str__(self):
        return f'Neby: {self.look}'


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

class CanvasBoard(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='canvas_boards', db_index=True)
    title = models.CharField(max_length=200, blank=True, default='Untitled canvas')
    share_token = models.CharField(max_length=64, unique=True, blank=True, null=True, db_index=True)
    shared_at = models.BigIntegerField(default=0)
    settings = models.TextField(blank=True, default='{}')
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'canvas_boards'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
        ]

    def __str__(self):
        return f"{self.title} ({self.user_id})"


class CanvasNode(models.Model):
    STATUS_CHOICES = [
        ('generating', 'Generating'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    ]
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    board = models.ForeignKey(CanvasBoard, on_delete=models.CASCADE, related_name='nodes', db_index=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='canvas_nodes', null=True, blank=True)
    prompt = models.TextField(blank=True, default='')
    title = models.CharField(max_length=300, blank=True, default='')
    content = models.TextField(blank=True, default='')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='generating', db_index=True)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    web_search_enabled = models.BooleanField(default=False)
    model_used = models.CharField(max_length=100, blank=True, default='')
    kind = models.CharField(max_length=24, blank=True, default='ai', db_index=True)
    metadata = models.TextField(blank=True, default='{}')
    error = models.TextField(blank=True, default='')
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'canvas_nodes'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['board', 'created_at']),
            models.Index(fields=['parent', 'created_at']),
        ]

    def __str__(self):
        return f"Node {self.title[:30]} ({self.board_id})"


class CanvasSnapshot(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    board = models.ForeignKey(CanvasBoard, on_delete=models.CASCADE, related_name='snapshots', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='canvas_snapshots', db_index=True)
    label = models.CharField(max_length=120, blank=True, default='Checkpoint')
    payload = models.TextField()
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'canvas_snapshots'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['board', '-created_at'], name='canvas_snap_board_created_idx'),
        ]


class CanvasObject(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    board = models.ForeignKey(CanvasBoard, on_delete=models.CASCADE, related_name='canvas_objects', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_canvas_objects', null=True, blank=True)
    obj_type = models.CharField(max_length=24, default='pen', db_index=True)
    payload = models.TextField(blank=True, default='{}')
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    z = models.IntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'canvas_objects'
        ordering = ['z', 'created_at']
        indexes = [
            models.Index(fields=['board', 'z'], name='canvas_obj_board_z_idx'),
        ]

    def __str__(self):
        return f"{self.obj_type} ({self.board_id})"


class CanvasNebyRun(models.Model):
    """Persistent history of Neby agent runs (explore/suggest) on a canvas."""
    KIND_CHOICES = [
        ('explore', 'Explore'),
        ('suggest', 'Suggest'),
    ]
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    board = models.ForeignKey(CanvasBoard, on_delete=models.CASCADE, related_name='neby_runs', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='canvas_neby_runs', db_index=True)
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default='explore', db_index=True)
    goal = models.TextField(blank=True, default='')
    summary = models.TextField(blank=True, default='')
    questions = models.JSONField(default=list, blank=True)
    provider = models.CharField(max_length=60, blank=True, default='')
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'canvas_neby_runs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['board', '-created_at'], name='canvas_run_board_created_idx'),
        ]

    def __str__(self):
        return f"{self.kind} on {self.board_id} at {self.created_at}"


class PaymentVerification(models.Model):
    """Buyers submit QR payment proof (screenshots & transaction ID) for paid resources/classes.
    Admins verify and approve these payments manually to credit the seller.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('approved', 'Approved'),
        ('hold', 'On Hold'),
        ('rejected', 'Rejected'),
    ]

    id = models.CharField(max_length=36, primary_key=True)  # UUID
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_purchases')
    # Exactly one of `resource` / `course` is set: a paid-library purchase or a
    # paid offering on a creator's marketplace page. Both are settled the same
    # way (QR proof -> admin verification -> seller wallet).
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='purchases', null=True, blank=True)
    course = models.ForeignKey('CreatorCourse', on_delete=models.SET_NULL, related_name='purchases', null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_sales')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    platform_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    seller_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=50, default='qr_code')
    transaction_id = models.CharField(max_length=100, blank=True, default='')  # eSewa / Khalti / Mobile Banking Ref ID or phone
    payment_proof = models.FileField(upload_to='payments/%Y/%m/', blank=True, null=True)
    payment_proof_url = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    admin_notes = models.TextField(blank=True, default='')
    created_at = models.BigIntegerField(default=0)
    verified_at = models.BigIntegerField(default=0)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_payments')

    class Meta:
        db_table = 'payment_verifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['buyer', 'resource', 'status']),
            models.Index(fields=['buyer', 'course', 'status']),
            models.Index(fields=['seller', 'status']),
            models.Index(fields=['status', '-created_at']),
        ]
        # One pending submission per buyer per target, enforced by the database.
        # `record_purchase` looks for an existing pending row before inserting,
        # but two taps of Submit racing each other both saw none and both
        # inserted -- leaving an admin two identical proofs to verify and the
        # seller at risk of being credited twice. Split in two so neither index
        # ever spans a NULL column (a NULL makes a unique row unique by itself,
        # which would defeat the constraint).
        constraints = [
            models.UniqueConstraint(
                fields=['buyer', 'course'],
                condition=models.Q(status='pending', course__isnull=False),
                name='uniq_pending_payment_per_course',
            ),
            models.UniqueConstraint(
                fields=['buyer', 'resource'],
                condition=models.Q(status='pending', resource__isnull=False),
                name='uniq_pending_payment_per_resource',
            ),
        ]

    @property
    def target_title(self):
        if self.course_id and self.course:
            return self.course.title
        if self.resource_id and self.resource:
            return self.resource.title
        return 'Removed item'

    @property
    def target_kind(self):
        return 'course' if self.course_id else 'resource'

    def __str__(self):
        return f"Payment {self.id[:8]} - {self.buyer.username} for {self.target_title} ({self.status})"


class SellerBalance(models.Model):
    """Tracks cumulative earnings, current available balance, and withdrawals for sellers/tutors/institutions."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='seller_balance')
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_withdrawn = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'seller_balances'

    def __str__(self):
        return f"Balance for {self.user.username}: Rs. {self.current_balance}"


class WithdrawalRequest(models.Model):
    """Sellers submit requests to withdraw their accumulated earnings (Minimum threshold: 1,000 NPR)."""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved & Paid'),
        ('rejected', 'Rejected'),
    ]
    PAYOUT_METHODS = [
        ('esewa', 'eSewa'),
        ('khalti', 'Khalti'),
        ('mobile_banking', 'Mobile Banking'),
        ('connectips', 'ConnectIPS'),
        ('bank', 'Bank Transfer'),
    ]

    id = models.CharField(max_length=36, primary_key=True)  # UUID
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawal_requests')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payout_method = models.CharField(max_length=30, choices=PAYOUT_METHODS, default='esewa')
    payout_details = models.TextField(help_text="Account holder name, ID, or account number")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    admin_notes = models.TextField(blank=True, default='')
    created_at = models.BigIntegerField(default=0)
    processed_at = models.BigIntegerField(default=0)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_withdrawals')

    class Meta:
        db_table = 'withdrawal_requests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return f"Withdrawal {self.amount} NPR by {self.user.username} ({self.status})"


class PaymentConfig(models.Model):
    """Singleton marketplace/company-QR/commission economy configuration."""
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    company_qr_url = models.TextField(blank=True, default='')
    company_qr_caption = models.CharField(max_length=200, blank=True, default='NEBians — Company QR')
    payment_instructions = models.TextField(blank=True, default='')
    upi_id = models.CharField(max_length=100, blank=True, default='')
    commission_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('2.50'))
    withdraw_min = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1000.00'))
    points_per_rupee_buyer = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.10'))
    points_per_rupee_seller = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.10'))
    points_to_credit = models.PositiveIntegerField(default=2)
    free_credits_per_month = models.PositiveIntegerField(default=10)
    updated_at = models.BigIntegerField(default=0)

class NebyCreditTransaction(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credit_transactions')
    transaction_type = models.CharField(max_length=30)  # 'monthly_grant', 'conversion', 'ai_usage', 'manual_topup'
    amount = models.IntegerField(default=0)
    points_spent = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=255, blank=True, default='')
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'neby_credit_transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.amount} credits ({self.transaction_type})"


class AiFeedback(models.Model):
    """Thumbs up/down on AI assistant replies (Neby chat / admin chat)."""
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4)
    user_id = models.CharField(max_length=255, db_index=True, default='')
    surface = models.CharField(max_length=30, default='neby')
    vote = models.SmallIntegerField(default=0)
    provider = models.CharField(max_length=60, blank=True, default='')
    model_name = models.CharField(max_length=120, blank=True, default='')
    query = models.TextField(blank=True, default='')
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'ai_feedback'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['surface', '-created_at']),
        ]

    def __str__(self):
        return f"{self.surface} {self.vote} by {self.user_id}"


CREATOR_KINDS = [
    ('tutor', 'Tutor'),
    ('institute', 'Institute'),
    ('admin', 'NEBians Official'),
]

CREATOR_LAYOUTS = [
    ('editorial', 'Editorial'),
    ('spotlight', 'Spotlight'),
    ('grid', 'Grid'),
    ('classic', 'Classic'),
    ('magazine', 'Magazine'),
    ('stack', 'Stack'),
]

COURSE_STATUSES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('archived', 'Archived'),
]


class CreatorPage(models.Model):
    """A marketplace storefront a teacher, institute or admin builds for
    themselves — their own page, in their own arrangement.

    Everything a visitor reads is data, not markup: `blocks` is an ordered list
    of section descriptors the owner reorders and fills in, and `style` holds
    the surface choices (hero treatment, radius, density, cover/avatar art).
    The renderers on the web and in the app read the same list, so a page looks
    like the same page in both places.
    """
    id = models.CharField(max_length=36, primary_key=True)  # UUID
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='creator_page')
    kind = models.CharField(max_length=16, choices=CREATOR_KINDS, default='tutor')
    slug = models.SlugField(max_length=80, unique=True)
    display_name = models.CharField(max_length=120)
    tagline = models.CharField(max_length=180, blank=True, default='')
    about = models.TextField(blank=True, default='')
    avatar_url = models.TextField(blank=True, default='')
    cover_url = models.TextField(blank=True, default='')
    accent_hex = models.CharField(max_length=7, default='#004BD4')
    layout = models.CharField(max_length=20, choices=CREATOR_LAYOUTS, default='editorial')
    style = models.JSONField(default=dict, blank=True)
    blocks = models.JSONField(default=list, blank=True)
    socials = models.JSONField(default=dict, blank=True)
    contact_email = models.EmailField(blank=True, default='')
    contact_phone = models.CharField(max_length=40, blank=True, default='')
    location = models.CharField(max_length=120, blank=True, default='')
    subjects = models.TextField(blank=True, default='')  # comma-separated
    languages = models.TextField(blank=True, default='')  # comma-separated
    verified = models.BooleanField(default=False)
    featured = models.BooleanField(default=False, db_index=True)
    published = models.BooleanField(default=False, db_index=True)
    accepting_students = models.BooleanField(default=True)
    follower_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'creator_pages'
        ordering = ['-featured', '-updated_at']
        indexes = [
            models.Index(fields=['published', '-featured', '-updated_at'], name='creator_pub_feat_idx'),
            models.Index(fields=['kind', 'published']),
            models.Index(fields=['-view_count']),
        ]

    def __str__(self):
        return f"{self.display_name} (@{self.slug})"

    @property
    def subject_list(self):
        return [s.strip() for s in (self.subjects or '').split(',') if s.strip()]

    @property
    def language_list(self):
        return [s.strip() for s in (self.languages or '').split(',') if s.strip()]


class CreatorCourse(models.Model):
    """A paid or free offering on a creator page — a course, a class, a batch."""
    id = models.CharField(max_length=36, primary_key=True)  # UUID
    page = models.ForeignKey(CreatorPage, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=90)
    summary = models.CharField(max_length=300, blank=True, default='')
    description = models.TextField(blank=True, default='')
    cover_url = models.TextField(blank=True, default='')
    promo_url = models.TextField(blank=True, default='')
    is_free = models.BooleanField(default=False, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    level = models.CharField(max_length=60, blank=True, default='')
    duration_label = models.CharField(max_length=60, blank=True, default='')
    lesson_count = models.PositiveIntegerField(default=0)
    seat_limit = models.PositiveIntegerField(default=0)  # 0 = unlimited
    # How it is taught, and how a student gets in: buy it here (QR checkout) or reach the teacher.
    delivery = models.CharField(max_length=12, default='recorded')
    enroll_mode = models.CharField(max_length=12, default='buy')
    contact_label = models.CharField(max_length=120, blank=True, default='')
    contact_url = models.TextField(blank=True, default='')
    includes = models.JSONField(default=list, blank=True)
    tags = models.TextField(blank=True, default='')
    status = models.CharField(max_length=12, choices=COURSE_STATUSES, default='draft', db_index=True)
    featured = models.BooleanField(default=False)
    enrollment_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    sale_count = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('0.00'))
    rating_count = models.PositiveIntegerField(default=0)
    sort_order = models.IntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)
    published_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'creator_courses'
        ordering = ['sort_order', '-created_at']
        unique_together = ('page', 'slug')
        indexes = [
            models.Index(fields=['page', 'status', 'sort_order'], name='course_page_status_idx'),
            models.Index(fields=['status', 'is_free', '-created_at']),
            models.Index(fields=['-sale_count']),
        ]

    def __str__(self):
        return f"{self.title} ({self.page.display_name})"

    @property
    def tag_list(self):
        return [t.strip() for t in (self.tags or '').split(',') if t.strip()]


class CreatorCourseResource(models.Model):
    """A library resource attached to a course as its reading material."""
    course = models.ForeignKey(CreatorCourse, on_delete=models.CASCADE, related_name='course_resources')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='course_links')
    sort_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'creator_course_resources'
        ordering = ['sort_order']
        unique_together = ('course', 'resource')


class CreatorPost(models.Model):
    """An update the owner posts on their page — announcements, batches, notes."""
    id = models.CharField(max_length=36, primary_key=True)  # UUID
    page = models.ForeignKey(CreatorPage, on_delete=models.CASCADE, related_name='page_posts')
    title = models.CharField(max_length=180, blank=True, default='')
    body = models.TextField(blank=True, default='')
    media_url = models.TextField(blank=True, default='')
    link_url = models.TextField(blank=True, default='')
    pinned = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    like_count = models.PositiveIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'creator_posts'
        ordering = ['-pinned', '-created_at']
        indexes = [
            models.Index(fields=['page', 'published', '-created_at'], name='creatorpost_page_pub_idx'),
        ]

    def __str__(self):
        return self.title or f"Post {self.id[:8]}"


# --------------------------------------------------------------------------
# Post reach (per viewer per day) and feed impressions. Written by
# api.post_reach, read by api.post_insights and the admin Analytics page.
# --------------------------------------------------------------------------

class PostReach(models.Model):
    """One viewer's opens of one post on one local day. `viewer` is a keyed
    hash (api.signals.viewer_tag), never a user id or an IP."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reach_rows')
    viewer = models.CharField(max_length=24)
    day = models.CharField(max_length=10)          # YYYY-MM-DD, settings.TIME_ZONE
    first_at = models.BigIntegerField()
    last_at = models.BigIntegerField()
    hits = models.PositiveIntegerField(default=1)
    dwell_ms = models.PositiveIntegerField(default=0)
    surface = models.CharField(max_length=12, blank=True, default='')   # feed|search|profile|share|direct|notification|related
    source = models.CharField(max_length=6, default='web')               # web|app
    device_class = models.CharField(max_length=10, blank=True, default='')
    os_family = models.CharField(max_length=16, blank=True, default='')
    country = models.CharField(max_length=60, blank=True, default='')
    channel = models.CharField(max_length=12, blank=True, default='')    # referrer channel
    is_member = models.BooleanField(default=False)
    is_follower = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

    class Meta:
        db_table = 'post_reach'
        unique_together = ('post', 'viewer', 'day')
        indexes = [
            models.Index(fields=['post', 'day']),
            models.Index(fields=['day']),
        ]


class PostImpression(models.Model):
    """Daily count of times a post scrolled into view in a list."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='impression_rows')
    day = models.CharField(max_length=10)
    source = models.CharField(max_length=6, default='web')
    count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'post_impressions'
        unique_together = ('post', 'day', 'source')
        indexes = [models.Index(fields=['day'])]


class ActorSignal(models.Model):
    """Private first-party context for account and interaction events.

    Internal analytics only (see docs/ANALYTICS.md, "Private signals"). No
    user id, IP or user agent lives here. `actor` is an HMAC of the user id under
    a key derived from SECRET_KEY: staff can go user -> signals by recomputing
    the tag, but the table cannot be turned back into users. `detail` is
    AES-GCM ciphertext. Never expose this model through an API serializer.
    """
    kind = models.CharField(max_length=10)         # signup|login|post|reply|vote|like|option
    actor = models.CharField(max_length=24)
    ref = models.CharField(max_length=36, blank=True, default='')    # post id the event belongs to
    ref2 = models.CharField(max_length=36, blank=True, default='')   # reply / option id
    source = models.CharField(max_length=6, default='web')
    device_class = models.CharField(max_length=10, blank=True, default='')
    os_family = models.CharField(max_length=16, blank=True, default='')
    browser = models.CharField(max_length=24, blank=True, default='')
    app_version = models.CharField(max_length=16, blank=True, default='')
    country = models.CharField(max_length=60, blank=True, default='')
    detail = models.TextField(blank=True, default='')
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'sys_ctx'
        indexes = [
            models.Index(fields=['kind', '-created_at']),
            models.Index(fields=['actor', 'kind']),
            models.Index(fields=['ref', 'kind']),
        ]


# ---------------------------------------------------------------------------
# Push campaigns, deliveries, library autopilot (api.push_engine, api.resource_alerts)
# ---------------------------------------------------------------------------
class PushCampaign(models.Model):
    """One push send: a hand-written broadcast, an announced batch of library uploads, or an
    autopilot digest. Counters are filled by api.push_engine as the send runs."""
    KIND_CHOICES = [('manual', 'Broadcast'), ('library', 'Library announcement'), ('autopilot', 'Autopilot'), ('test', 'Test')]
    STATUS_CHOICES = [('scheduled', 'Scheduled'), ('sending', 'Sending'), ('sent', 'Sent'),
                      ('failed', 'Failed'), ('canceled', 'Canceled')]
    id = models.CharField(max_length=36, primary_key=True)
    kind = models.CharField(max_length=12, choices=KIND_CHOICES, default='manual', db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sending', db_index=True)
    title = models.CharField(max_length=120)
    body = models.TextField(blank=True, default='')
    url = models.CharField(max_length=300, blank=True, default='')
    target_type = models.CharField(max_length=20, blank=True, default='system')
    target_id = models.CharField(max_length=36, blank=True, default='')
    audience = models.JSONField(default=dict, blank=True)
    audience_label = models.CharField(max_length=240, blank=True, default='')
    also_inbox = models.BooleanField(default=True)
    resource_ids = models.JSONField(default=list, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='push_campaigns')
    created_at = models.BigIntegerField()
    scheduled_at = models.BigIntegerField(default=0)
    started_at = models.BigIntegerField(default=0)
    finished_at = models.BigIntegerField(default=0)
    users_targeted = models.PositiveIntegerField(default=0)
    users_pushed = models.PositiveIntegerField(default=0)
    users_inbox_only = models.PositiveIntegerField(default=0)
    users_suppressed = models.PositiveIntegerField(default=0)
    devices_targeted = models.PositiveIntegerField(default=0)
    devices_accepted = models.PositiveIntegerField(default=0)
    devices_failed = models.PositiveIntegerField(default=0)
    tokens_pruned = models.PositiveIntegerField(default=0)
    errors = models.JSONField(default=dict, blank=True)
    note = models.CharField(max_length=240, blank=True, default='')

    class Meta:
        db_table = 'push_campaigns'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['kind', '-created_at'], name='pushc_kind_created_idx'),
                   models.Index(fields=['status', 'scheduled_at'], name='pushc_status_sched_idx')]


class PushDelivery(models.Model):
    """What one campaign did for one person. Aggregated only; never shown with a name."""
    campaign = models.ForeignKey(PushCampaign, on_delete=models.CASCADE, related_name='deliveries')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_deliveries')
    notification_id = models.CharField(max_length=36, blank=True, default='')
    status = models.CharField(max_length=12, default='queued')   # sent|inbox|failed|capped|quiet|queued
    devices = models.PositiveSmallIntegerField(default=0)
    accepted = models.PositiveSmallIntegerField(default=0)
    error = models.CharField(max_length=60, blank=True, default='')
    class_level = models.CharField(max_length=40, blank=True, default='')
    created_at = models.BigIntegerField(default=0)
    opened_at = models.BigIntegerField(default=0)
    opened_via = models.CharField(max_length=8, blank=True, default='')   # push|inbox
    clicked_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'push_deliveries'
        unique_together = ('campaign', 'user')
        indexes = [models.Index(fields=['user', '-created_at'], name='pushd_user_created_idx'),
                   models.Index(fields=['notification_id'], name='pushd_notif_idx'),
                   models.Index(fields=['campaign', 'opened_at'], name='pushd_camp_open_idx')]


class PushSettings(models.Model):
    """Singleton (id=1): how the library autopilot behaves."""
    id = models.PositiveSmallIntegerField(primary_key=True, default=1)
    autopilot_enabled = models.BooleanField(default=True)
    daily_cap = models.PositiveSmallIntegerField(default=2)
    quiet_start_hour = models.PositiveSmallIntegerField(default=21)
    quiet_end_hour = models.PositiveSmallIntegerField(default=7)
    settle_minutes = models.PositiveSmallIntegerField(default=5)
    max_wait_minutes = models.PositiveSmallIntegerField(default=30)
    include_paid = models.BooleanField(default=False)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'push_settings'


class ResourceAlert(models.Model):
    """Autopilot queue: one row per library resource that went live. `sent`/`manual` mean the
    audience was told; `skipped` says why not. Resources that predate the autopilot have no row."""
    resource = models.OneToOneField(Resource, on_delete=models.CASCADE, related_name='alert')
    state = models.CharField(max_length=10, default='pending', db_index=True)   # pending|sending|sent|manual|skipped
    reason = models.CharField(max_length=60, blank=True, default='')
    queued_at = models.BigIntegerField(default=0)
    processed_at = models.BigIntegerField(default=0)
    audience_size = models.PositiveIntegerField(default=0)
    campaign_id = models.CharField(max_length=36, blank=True, default='')

    class Meta:
        db_table = 'resource_alerts'
        indexes = [models.Index(fields=['state', 'queued_at'], name='resalert_state_q_idx')]


class ResourceReach(models.Model):
    """One viewer's opens of one resource on one local day (the PostReach twin).
    `viewer` is a keyed hash, never a user id or an IP."""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='reach_rows')
    viewer = models.CharField(max_length=24)
    day = models.CharField(max_length=10)
    first_at = models.BigIntegerField()
    last_at = models.BigIntegerField()
    hits = models.PositiveIntegerField(default=1)
    dwell_ms = models.PositiveIntegerField(default=0)
    surface = models.CharField(max_length=12, blank=True, default='')   # library|search|subject|profile|share|direct|notification|related
    source = models.CharField(max_length=6, default='web')
    device_class = models.CharField(max_length=10, blank=True, default='')
    os_family = models.CharField(max_length=16, blank=True, default='')
    country = models.CharField(max_length=60, blank=True, default='')
    channel = models.CharField(max_length=12, blank=True, default='')
    class_level = models.CharField(max_length=40, blank=True, default='')
    is_member = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    downloaded = models.BooleanField(default=False)
    shared = models.BooleanField(default=False)

    class Meta:
        db_table = 'resource_reach'
        unique_together = ('resource', 'viewer', 'day')
        indexes = [models.Index(fields=['resource', 'day'], name='resreach_res_day_idx'),
                   models.Index(fields=['day'], name='resreach_day_idx')]


class ResourceImpression(models.Model):
    """Daily count of times a resource card scrolled into view in a list."""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='impression_rows')
    day = models.CharField(max_length=10)
    source = models.CharField(max_length=6, default='web')
    count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'resource_impressions'
        unique_together = ('resource', 'day', 'source')
        indexes = [models.Index(fields=['day'], name='resimp_day_idx')]

from .models_institutions import Institution, InstitutionVerification, InstitutionDocument, InstitutionProfile  # noqa: E402,F401
