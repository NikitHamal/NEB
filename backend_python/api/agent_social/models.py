import json

from django.db import models

from api.utils import now_ms, uuid_str


class AgentPersona(models.Model):
    """Character, goals, and autonomy settings for a bot User.

    One-to-one with BotConfig. The matching User is looked up by
    bot_username (charset-safe — no FK onto the latin1 users table).
    """
    id = models.CharField(max_length=36, primary_key=True, default=uuid_str)
    bot_config = models.OneToOneField(
        'api.BotConfig', on_delete=models.CASCADE, related_name='persona',
    )
    user_id = models.CharField(max_length=255, db_index=True, default='')
    tagline = models.CharField(max_length=200, blank=True, default='')
    origin_story = models.TextField(blank=True, default='')
    goals_json = models.TextField(blank=True, default='[]')
    traits_json = models.TextField(blank=True, default='[]')
    preferred_categories_json = models.TextField(blank=True, default='[]')
    voice_notes = models.TextField(blank=True, default='')
    autonomy_enabled = models.BooleanField(default=False, db_index=True)
    birth_announced = models.BooleanField(default=False)
    tick_interval_minutes = models.PositiveIntegerField(default=2)
    min_hours_between_posts = models.PositiveIntegerField(default=4)
    max_posts_per_day = models.PositiveIntegerField(default=4)
    max_replies_per_tick = models.PositiveIntegerField(default=2)
    max_likes_per_tick = models.PositiveIntegerField(default=4)
    max_follows_per_tick = models.PositiveIntegerField(default=2)
    last_tick_at = models.BigIntegerField(default=0)
    last_post_at = models.BigIntegerField(default=0)
    last_reply_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'agent_personas'
        indexes = [
            models.Index(fields=['autonomy_enabled', 'last_tick_at']),
        ]

    def save(self, *args, **kwargs):
        now = now_ms()
        self.updated_at = now
        if not self.created_at:
            self.created_at = now
        if not self.id:
            self.id = uuid_str()
        super().save(*args, **kwargs)

    def _load_list(self, raw):
        try:
            data = json.loads(raw or '[]')
        except (ValueError, TypeError):
            return []
        if not isinstance(data, list):
            return []
        return [str(item).strip() for item in data if str(item).strip()][:12]

    @property
    def goals(self):
        return self._load_list(self.goals_json)

    @goals.setter
    def goals(self, value):
        self.goals_json = json.dumps(list(value or [])[:12], ensure_ascii=False)

    @property
    def traits(self):
        return self._load_list(self.traits_json)

    @traits.setter
    def traits(self, value):
        self.traits_json = json.dumps(list(value or [])[:12], ensure_ascii=False)

    @property
    def preferred_categories(self):
        return self._load_list(self.preferred_categories_json)

    @preferred_categories.setter
    def preferred_categories(self, value):
        self.preferred_categories_json = json.dumps(list(value or [])[:12], ensure_ascii=False)

    def get_user(self):
        from api.models import User
        if not self.user_id:
            return None
        try:
            return User.objects.get(pk=self.user_id)
        except User.DoesNotExist:
            return None


class AgentAction(models.Model):
    ACTION_CHOICES = [
        ('introduce', 'Introduce'),
        ('post', 'Post'),
        ('reply', 'Reply'),
        ('like_post', 'Like post'),
        ('like_reply', 'Like reply'),
        ('follow', 'Follow'),
        ('unfollow', 'Unfollow'),
        ('tick', 'Heartbeat tick'),
        ('skip', 'Skip'),
    ]
    STATUS_CHOICES = [
        ('done', 'Done'),
        ('skipped', 'Skipped'),
        ('failed', 'Failed'),
    ]
    SOURCE_CHOICES = [
        ('heartbeat', 'Heartbeat'),
        ('mention', 'Mention'),
        ('api', 'Agent API'),
        ('admin', 'Admin'),
        ('seed', 'Seed'),
    ]

    id = models.CharField(max_length=36, primary_key=True, default=uuid_str)
    persona = models.ForeignKey(
        AgentPersona, on_delete=models.CASCADE, related_name='actions',
    )
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES, db_index=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='done')
    source = models.CharField(max_length=12, choices=SOURCE_CHOICES, default='heartbeat')
    target_type = models.CharField(max_length=20, blank=True, default='')
    target_id = models.CharField(max_length=64, blank=True, default='')
    content_preview = models.CharField(max_length=400, blank=True, default='')
    reasoning = models.CharField(max_length=400, blank=True, default='')
    extra_json = models.TextField(blank=True, default='{}')
    created_at = models.BigIntegerField(default=0, db_index=True)

    class Meta:
        db_table = 'agent_actions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['persona', '-created_at']),
            models.Index(fields=['persona', 'action_type', 'target_id']),
            models.Index(fields=['-created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = now_ms()
        if not self.id:
            self.id = uuid_str()
        super().save(*args, **kwargs)


class AgentApiKey(models.Model):
    """Bearer key for third-party agents (moltbook-style protocol)."""
    id = models.CharField(max_length=36, primary_key=True, default=uuid_str)
    user_id = models.CharField(max_length=255, db_index=True)
    key_prefix = models.CharField(max_length=16, db_index=True)
    key_hash = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=80, blank=True, default='')
    claim_code = models.CharField(max_length=32, blank=True, default='')
    claimed_at = models.BigIntegerField(default=0)
    last_used_at = models.BigIntegerField(default=0)
    revoked_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'agent_api_keys'
        indexes = [
            models.Index(fields=['user_id', 'revoked_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = now_ms()
        if not self.id:
            self.id = uuid_str()
        super().save(*args, **kwargs)
