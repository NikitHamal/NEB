"""High-level services for drafting and publishing Neby blog posts."""
import logging
import re
import time
from typing import Dict, Optional

from django.utils.text import slugify

from api.models import Announcement, BotConfig, User
from api.utils import now_ms, uuid_str

from .feature_catalog import get_all_features, get_feature_by_id, pick_random_feature
from .generator import generate_blog_post
from .git_reader import format_commits_for_prompt, get_recent_commits

logger = logging.getLogger(__name__)


def _get_neby_author() -> Optional[User]:
    """Retrieve or resolve the bot user 'neby' as author."""
    user = User.objects.filter(username__iexact='neby').first()
    if not user:
        user = User.objects.filter(is_bot=True).first()
    if not user:
        user = User.objects.filter(is_admin=True).first()
    return user


def _generate_unique_slug(base_title: str) -> str:
    """Generate a unique slug for the announcement."""
    base_slug = slugify(base_title) or f"neby-update-{int(time.time())}"
    base_slug = base_slug[:80]
    slug = base_slug
    counter = 1
    while Announcement.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


def _create_announcement_from_data(
    data: Dict[str, str],
    publish: bool = False,
    author: Optional[User] = None,
) -> Announcement:
    """Persist generated blog post into the database."""
    author = author or _get_neby_author()
    now = now_ms()
    slug = _generate_unique_slug(data.get('slug') or data.get('title') or 'neby-update')

    announcement = Announcement.objects.create(
        id=uuid_str(),
        title=data.get('title', 'NEBians Community Update'),
        slug=slug,
        summary=data.get('summary', '')[:490],
        content=data.get('content', ''),
        category=data.get('category', 'update'),
        status='published' if publish else 'draft',
        tags=data.get('tags', 'NEBians, Updates'),
        cover_image_url=data.get('cover_image_url', ''),
        author=author,
        published_at=now if publish else 0,
        created_at=now,
        updated_at=now,
    )
    return announcement


def draft_blog_from_git(publish: bool = False, limit_commits: int = 25) -> Optional[Announcement]:
    """Inspect recent Git commits and draft a release update post."""
    commits = get_recent_commits(limit=limit_commits)
    formatted = format_commits_for_prompt(commits)
    topic = (
        f"Latest platform updates, performance improvements, and feature rollouts "
        f"recently pushed to the NEBians codebase:\n\n{formatted}"
    )
    
    config = BotConfig.objects.filter(bot_username__iexact='neby').first()
    data = generate_blog_post(
        topic_description=topic,
        context_type="update",
        additional_notes="Highlight the most exciting changes and how they help students and teachers.",
        bot_config=config,
    )
    if not data:
        logger.warning('draft_blog_from_git: failed to generate blog data')
        return None
    return _create_announcement_from_data(data, publish=publish)


def draft_blog_from_spotlight(
    feature_id: Optional[str] = None,
    publish: bool = False,
) -> Optional[Announcement]:
    """Pick a feature spotlight and write an in-depth student guide / tutorial."""
    if feature_id:
        feature = get_feature_by_id(feature_id) or pick_random_feature()
    else:
        # Avoid features featured in the last 3 announcements
        recent_announcements = Announcement.objects.filter(status='published').order_by('-published_at')[:5]
        recent_text = " ".join([f"{a.title} {a.tags}" for a in recent_announcements]).lower()
        exclude = [f['id'] for f in get_all_features() if f['id'] in recent_text]
        feature = pick_random_feature(exclude_ids=exclude)

    topic = (
        f"Feature Spotlight: {feature['title']}\n"
        f"Tagline: {feature['tagline']}\n"
        f"Description: {feature['description']}\n\n"
        f"Key Highlights to explain:\n" + "\n".join([f"- {h}" for h in feature['highlights']])
    )
    
    config = BotConfig.objects.filter(bot_username__iexact='neby').first()
    data = generate_blog_post(
        topic_description=topic,
        context_type=feature.get('category', 'update'),
        additional_notes=f"Default suggested tags: {feature.get('default_tags', '')}",
        bot_config=config,
    )
    if not data:
        logger.warning('draft_blog_from_spotlight: failed to generate blog data')
        return None
    return _create_announcement_from_data(data, publish=publish)


def draft_blog_from_prompt(
    prompt_text: str,
    category: str = "update",
    publish: bool = False,
) -> Optional[Announcement]:
    """Draft a blog post based on custom user/admin prompt."""
    config = BotConfig.objects.filter(bot_username__iexact='neby').first()
    data = generate_blog_post(
        topic_description=prompt_text,
        context_type=category,
        bot_config=config,
    )
    if not data:
        logger.warning('draft_blog_from_prompt: failed to generate blog data')
        return None
    return _create_announcement_from_data(data, publish=publish)
