"""
Django signals to keep Meilisearch index in sync with database changes.

Only active when MEILISEARCH_URL is configured.
"""
import logging

from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver

logger = logging.getLogger(__name__)


def _sync_enabled():
    from api.search import is_enabled
    return is_enabled()


@receiver(post_save, sender='api.Resource')
def resource_saved(sender, instance, **kwargs):
    if not _sync_enabled():
        return
    from api.search import sync_resources
    try:
        sync_resources(queryset=type(instance).objects.filter(pk=instance.pk))
    except Exception:
        logger.warning("Meilisearch: failed to sync resource %s", instance.pk, exc_info=True)


@receiver(post_delete, sender='api.Resource')
def resource_deleted(sender, instance, **kwargs):
    if not _sync_enabled():
        return
    from api.search import delete_resource
    try:
        delete_resource(instance.pk)
    except Exception:
        logger.warning("Meilisearch: failed to delete resource %s", instance.pk, exc_info=True)


@receiver(post_save, sender='api.Post')
def post_saved(sender, instance, **kwargs):
    if not _sync_enabled():
        return
    if instance.is_archived:
        from api.search import delete_post
        try:
            delete_post(instance.pk)
        except Exception:
            logger.warning("Meilisearch: failed to delete archived post %s", instance.pk, exc_info=True)
        return
    from api.search import sync_posts
    try:
        sync_posts(queryset=type(instance).objects.filter(pk=instance.pk))
    except Exception:
        logger.warning("Meilisearch: failed to sync post %s", instance.pk, exc_info=True)


@receiver(post_delete, sender='api.Post')
def post_deleted(sender, instance, **kwargs):
    if not _sync_enabled():
        return
    from api.search import delete_post
    try:
        delete_post(instance.pk)
    except Exception:
        logger.warning("Meilisearch: failed to delete post %s", instance.pk, exc_info=True)


@receiver(post_save, sender='api.User')
def user_saved(sender, instance, **kwargs):
    if not _sync_enabled():
        return
    from api.search import sync_users
    try:
        sync_users(queryset=type(instance).objects.filter(pk=instance.pk))
    except Exception:
        logger.warning("Meilisearch: failed to sync user %s", instance.pk, exc_info=True)


@receiver(post_delete, sender='api.User')
def user_deleted(sender, instance, **kwargs):
    if not _sync_enabled():
        return
    from api.search import delete_user
    try:
        delete_user(instance.pk)
    except Exception:
        logger.warning("Meilisearch: failed to delete user %s", instance.pk, exc_info=True)