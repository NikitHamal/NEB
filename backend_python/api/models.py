"""
Django models for NEBians.
Schema is the source of truth — keep in sync with the Kotlin app's ApiService.
"""
import uuid
from django.db import models


class User(models.Model):
    """
    NEBians user profile.
    id = Google 'sub' (subject) claim — used as primary key.
    auth_token = server-issued token for subsequent authenticated requests.
    """
    id = models.CharField(max_length=255, primary_key=True)
    auth_token = models.CharField(max_length=64, unique=True, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True, null=True)
    photo_url = models.TextField(blank=True, null=True)
    display_name = models.CharField(max_length=150, blank=True, null=True)
    dob = models.CharField(max_length=20, default='')
    gender = models.CharField(max_length=20, blank=True, null=True)
    class_level = models.CharField(max_length=10, blank=True, null=True, db_column='class')
    subjects = models.TextField(blank=True, null=True)  # comma-separated
    pradesh = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    school = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, default='')
    is_locked = models.BooleanField(default=False)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username or self.id

    @staticmethod
    def generate_token():
        return uuid.uuid4().hex + uuid.uuid4().hex

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return not self.is_locked


class Resource(models.Model):
    """Study resources — ebooks, PDFs, notes."""
    id = models.CharField(max_length=36, primary_key=True)  # UUID
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=20)
    type = models.CharField(max_length=50)  # e.g. "PDF", "Note", "Video"
    file_url = models.TextField()
    thumbnail_url = models.TextField(blank=True, null=True)
    file_size = models.BigIntegerField(default=0)
    added_at = models.BigIntegerField()  # Unix ms timestamp
    view_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'resources'
        ordering = ['-added_at']

    def __str__(self):
        return self.title


class Post(models.Model):
    """Forum post."""
    id = models.CharField(max_length=36, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=300)
    content = models.TextField()
    category = models.CharField(max_length=100)
    thumbs_up_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    is_edited = models.BooleanField(default=False)
    edited_at = models.BigIntegerField(default=0)
    is_archived = models.BooleanField(default=False)
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']

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
    is_edited = models.BooleanField(default=False)
    edited_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField()

    class Meta:
        db_table = 'replies'
        ordering = ['created_at']

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
