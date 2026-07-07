"""
Meilisearch integration for full-text search.

Feature-flagged: if MEILISEARCH_URL is not set, falls back to icontains queries.
When configured, provides instant typo-tolerant search with highlighting.
"""
import logging
import os

from django.conf import settings

logger = logging.getLogger(__name__)

_client = None
_enabled = None


def is_enabled():
    global _enabled
    if _enabled is None:
        _enabled = bool(getattr(settings, 'MEILISEARCH_URL', ''))
    return _enabled


def get_client():
    global _client
    if _client is not None:
        return _client
    if not is_enabled():
        return None
    try:
        from meilisearch import Client
        url = settings.MEILISEARCH_URL
        api_key = getattr(settings, 'MEILISEARCH_API_KEY', '')
        _client = Client(url, api_key)
        _client.health()
        return _client
    except Exception:
        logger.warning("Meilisearch not reachable, falling back to DB search")
        _client = None
        return None


INDEX_RESOURCES = 'resources'
INDEX_POSTS = 'posts'
INDEX_USERS = 'users'


def _ensure_indexes():
    client = get_client()
    if not client:
        return
    for index_uid, pk_field in [
        (INDEX_RESOURCES, 'id'),
        (INDEX_POSTS, 'id'),
        (INDEX_USERS, 'id'),
    ]:
        index = client.index(index_uid)
        task_info = index.update(primary_key=pk_field)
        logger.info("Ensured index %s (task %s)", index_uid, task_info.task_uid)
    for index_uid in [INDEX_RESOURCES, INDEX_POSTS]:
        index = client.index(index_uid)
        index.update_filterable_attributes(['category', 'subject', 'grade_level', 'type', 'is_archived'])
        index.update_searchable_attributes(['title', 'content', 'description', 'tags', 'subject', 'faculty', 'school', 'username', 'display_name'])
        index.update_sortable_attributes(['created_at', 'thumbs_up_count', 'view_count'])
        index.update_ranking_rules([
            'words', 'typo', 'proximity', 'attribute', 'sort', 'exactness',
        ])


def _serialize_resource(r):
    return {
        'id': r.id,
        'title': r.title,
        'description': r.description or '',
        'subject': r.subject or '',
        'grade_level': r.grade_level or '',
        'faculty': r.faculty or '',
        'program': r.program or '',
        'school': r.school or '',
        'type': r.type or '',
        'tags': r.tags or '',
        'created_at': r.added_at if hasattr(r, 'added_at') else 0,
    }


def _serialize_post(p):
    username = p.user.username if p.user else ''
    return {
        'id': p.id,
        'title': p.title,
        'content': p.content,
        'category': p.category or '',
        'thumbs_up_count': p.thumbs_up_count,
        'reply_count': p.reply_count,
        'view_count': p.view_count,
        'created_at': p.created_at,
        'is_archived': p.is_archived,
        'username': username,
    }


def _serialize_user(u):
    return {
        'id': u.id,
        'username': u.username or '',
        'display_name': u.display_name or '',
    }


def sync_resources(queryset=None):
    client = get_client()
    if not client:
        return 0
    from api.models import Resource
    qs = queryset if queryset is not None else Resource.objects.filter(approval_status='approved', is_lead=True)
    docs = [_serialize_resource(r) for r in qs.iterator()]
    if not docs:
        return 0
    index = client.index(INDEX_RESOURCES)
    task_info = index.add_documents(docs)
    logger.info("Synced %d resources to Meilisearch (task %s)", len(docs), task_info.task_uid)
    return len(docs)


def sync_posts(queryset=None):
    client = get_client()
    if not client:
        return 0
    from api.models import Post
    qs = queryset if queryset is not None else Post.objects.filter(is_archived=False).select_related('user')
    docs = [_serialize_post(p) for p in qs.iterator()]
    if not docs:
        return 0
    index = client.index(INDEX_POSTS)
    task_info = index.add_documents(docs)
    logger.info("Synced %d posts to Meilisearch (task %s)", len(docs), task_info.task_uid)
    return len(docs)


def sync_users(queryset=None):
    client = get_client()
    if not client:
        return 0
    from api.models import User
    qs = queryset if queryset is not None else User.objects.filter(is_locked=False, email_verified=True)
    docs = [_serialize_user(u) for u in qs.iterator()]
    if not docs:
        return 0
    index = client.index(INDEX_USERS)
    task_info = index.add_documents(docs)
    logger.info("Synced %d users to Meilisearch (task %s)", len(docs), task_info.task_uid)
    return len(docs)


def sync_all():
    _ensure_indexes()
    total = 0
    total += sync_resources()
    total += sync_posts()
    total += sync_users()
    return total


def search_resources(query, subject='', grade='', rtype='', limit=30):
    client = get_client()
    if not client:
        return None
    filters_parts = []
    if subject:
        filters_parts.append(f"subject = \"{subject}\"")
    if grade:
        filters_parts.append(f"grade_level = \"{grade}\"")
    if rtype:
        filters_parts.append(f"type = \"{rtype}\"")
    filter_str = ' AND '.join(filters_parts) if filters_parts else None
    search_params = {'limit': limit, 'attributesToHighlight': ['title', 'description', 'subject', 'tags']}
    if filter_str:
        search_params['filter'] = filter_str
    results = client.index(INDEX_RESOURCES).search(query, search_params)
    return results.get('hits', [])


def search_posts(query, category='', limit=20):
    client = get_client()
    if not client:
        return None
    filters_parts = ['is_archived = false']
    if category:
        filters_parts.append(f"category = \"{category}\"")
    filter_str = ' AND '.join(filters_parts)
    search_params = {
        'limit': limit,
        'filter': filter_str,
        'attributesToHighlight': ['title', 'content'],
    }
    results = client.index(INDEX_POSTS).search(query, search_params)
    return results.get('hits', [])


def search_users(query, limit=30):
    client = get_client()
    if not client:
        return None
    search_params = {'limit': limit, 'attributesToHighlight': ['username', 'display_name']}
    results = client.index(INDEX_USERS).search(query, search_params)
    return results.get('hits', [])


def delete_resource(resource_id):
    client = get_client()
    if not client:
        return
    client.index(INDEX_RESOURCES).delete_document(str(resource_id))


def delete_post(post_id):
    client = get_client()
    if not client:
        return
    client.index(INDEX_POSTS).delete_document(str(post_id))


def delete_user(user_id):
    client = get_client()
    if not client:
        return
    client.index(INDEX_USERS).delete_document(str(user_id))