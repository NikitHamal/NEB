import logging
import time

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count, Sum, Q
from django.db.models import F
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .security import verify_internal_admin_signature, validate_resource_file_url
from .models import User, Resource, Post, Reply, FCMToken
from .serializers import UserSerializer, ResourceSerializer, PostSerializer, ReplySerializer

logger = logging.getLogger(__name__)


def _django_user_from_request(request):
    raw_request = getattr(request, '_request', request)
    return getattr(raw_request, 'user', None)


def _check_admin(request):
    """Allow only Django staff/superusers or signed internal server calls.

    The old shared-token and username == 'admin' bypasses were removed.
    Custom admin pages authenticate with Django's built-in staff user session;
    their server-side API client uses a short-lived signed internal header.
    """
    django_user = _django_user_from_request(request)
    if getattr(django_user, 'is_authenticated', False) and getattr(django_user, 'is_staff', False):
        return True
    signature = request.headers.get('X-Internal-Admin-Signature', '')
    return verify_internal_admin_signature(signature, max_age=60)


def _admin_error():
    return Response({'error': 'Admin access required'}, status=403)


def _paginate(request, queryset, serializer_class, *, context=None, default_page_size=50, max_page_size=100):
    try:
        page_number = int(request.query_params.get('page', '1'))
    except (TypeError, ValueError):
        page_number = 1
    try:
        page_size = int(request.query_params.get('page_size', default_page_size))
    except (TypeError, ValueError):
        page_size = default_page_size
    page_size = max(1, min(page_size, max_page_size))
    paginator = Paginator(queryset, page_size)
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages or 1)
    serializer = serializer_class(page.object_list, many=True, context=context or {})
    return Response({
        'count': paginator.count,
        'page': page.number,
        'page_size': page_size,
        'num_pages': paginator.num_pages,
        'results': serializer.data,
    })


@api_view(['GET'])
def admin_stats(request):
    if not _check_admin(request):
        return _admin_error()
    total_users = User.objects.count()
    total_resources = Resource.objects.count()
    total_posts = Post.objects.count()
    total_replies = Reply.objects.count()
    total_likes = Post.objects.aggregate(total=Sum('thumbs_up_count'))['total'] or 0
    seven_days_ago = int((time.time() - 7 * 86400) * 1000)
    new_users_week = User.objects.filter(created_at__gte=seven_days_ago).count()
    new_posts_week = Post.objects.filter(created_at__gte=seven_days_ago).count()
    top_posts = Post.objects.select_related('user').order_by('-thumbs_up_count')[:5]
    top_posts_data = PostSerializer(top_posts, many=True, context={'request': request}).data
    recent_users = User.objects.order_by('-created_at')[:5]
    recent_users_data = UserSerializer(recent_users, many=True).data
    subject_counts = dict(Resource.objects.values('subject').annotate(cnt=Count('id')).values_list('subject', 'cnt'))
    return Response({
        'total_users': total_users,
        'total_resources': total_resources,
        'total_posts': total_posts,
        'total_replies': total_replies,
        'total_likes': total_likes,
        'new_users_week': new_users_week,
        'new_posts_week': new_posts_week,
        'top_posts': top_posts_data,
        'recent_users': recent_users_data,
        'subject_counts': subject_counts,
    })


@api_view(['GET'])
def admin_users_list(request):
    if not _check_admin(request):
        return _admin_error()
    users = User.objects.all().order_by('-created_at')
    search = request.query_params.get('search', '').strip()
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(display_name__icontains=search)
        )
    if request.query_params.get('page'):
        return _paginate(request, users, UserSerializer)
    return Response(UserSerializer(users[:100], many=True).data)


@api_view(['GET', 'PATCH', 'DELETE'])
def admin_user_detail(request, user_id):
    if not _check_admin(request):
        return _admin_error()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    if request.method == 'GET':
        return Response(UserSerializer(user).data)

    if request.method == 'DELETE':
        user.delete()
        return Response({'success': True})

    if request.method == 'PATCH':
        data = request.data
        for field in ['username', 'email', 'display_name', 'gender', 'class_level', 'subjects', 'pradesh', 'district', 'school', 'photo_url', 'dob']:
            if field in data:
                setattr(user, field, data[field])
        if 'isLocked' in data:
            user.is_locked = bool(data['isLocked'])
        user.save()
        return Response(UserSerializer(user).data)


@api_view(['GET', 'POST'])
def admin_resources_list(request):
    if not _check_admin(request):
        return _admin_error()

    if request.method == 'GET':
        resources = Resource.objects.all().order_by('-added_at')
        search = request.query_params.get('search', '').strip()
        if search:
            resources = resources.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        if request.query_params.get('page'):
            return _paginate(request, resources, ResourceSerializer)
        return Response(ResourceSerializer(resources[:100], many=True).data)

    import uuid
    data = request.data
    title = data.get('title', '').strip()
    subject = data.get('subject', '').strip()
    grade_level = data.get('grade_level', '').strip()
    file_url = data.get('file_url', '').strip()
    if not title or not subject or not grade_level or not file_url:
        return Response({'error': 'title, subject, grade_level, and file_url are required'}, status=400)
    try:
        safe_file_url = validate_resource_file_url(file_url)
        thumbnail_url = data.get('thumbnail_url', '').strip()
        if thumbnail_url:
            thumbnail_url = validate_resource_file_url(thumbnail_url)
    except Exception as exc:
        messages = getattr(exc, 'messages', [str(exc)])
        return Response({'error': ' '.join(messages)}, status=400)
    resource = Resource(
        id=data.get('id', str(uuid.uuid4())),
        title=title,
        description=data.get('description', '').strip(),
        subject=subject,
        grade_level=grade_level,
        type=data.get('type', 'PDF').strip() or 'PDF',
        file_url=safe_file_url,
        thumbnail_url=thumbnail_url,
        file_size=int(data.get('file_size') or 0),
        added_at=data.get('added_at', int(time.time() * 1000)),
        view_count=int(data.get('view_count') or 0),
    )
    resource.save()
    return Response(ResourceSerializer(resource).data, status=201)


@api_view(['GET', 'PATCH', 'DELETE'])
def admin_resource_detail(request, resource_id):
    if not _check_admin(request):
        return _admin_error()
    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=404)

    if request.method == 'GET':
        return Response(ResourceSerializer(resource).data)

    if request.method == 'DELETE':
        resource.delete()
        return Response({'success': True})

    data = request.data
    for field in ['title', 'description', 'subject', 'grade_level', 'type']:
        if field in data:
            setattr(resource, field, str(data[field]).strip())
    for field in ['file_url', 'thumbnail_url']:
        if field in data:
            value = str(data[field]).strip()
            if value:
                try:
                    value = validate_resource_file_url(value)
                except Exception as exc:
                    messages = getattr(exc, 'messages', [str(exc)])
                    return Response({'error': ' '.join(messages)}, status=400)
            setattr(resource, field, value)
    if 'file_size' in data:
        resource.file_size = int(data['file_size'])
    if 'view_count' in data:
        resource.view_count = int(data['view_count'])
    resource.save()
    return Response(ResourceSerializer(resource).data)


@api_view(['GET'])
def admin_posts_list(request):
    if not _check_admin(request):
        return _admin_error()
    posts = Post.objects.select_related('user').all().order_by('-created_at')
    search = request.query_params.get('search', '').strip()
    if search:
        from django.db.models import Q
        posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))
    if request.query_params.get('page'):
        return _paginate(request, posts, PostSerializer, context={'request': request})
    return Response(PostSerializer(posts[:100], many=True, context={'request': request}).data)


@api_view(['GET', 'DELETE'])
def admin_post_detail(request, post_id):
    if not _check_admin(request):
        return _admin_error()
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)

    if request.method == 'GET':
        return Response(PostSerializer(post, context={'request': request}).data)

    post.delete()
    return Response({'success': True})


@api_view(['GET'])
def admin_post_replies(request, post_id):
    if not _check_admin(request):
        return _admin_error()
    replies = Reply.objects.filter(post_id=post_id).select_related('user')
    return Response(ReplySerializer(replies, many=True, context={'request': request}).data)


@api_view(['DELETE'])
def admin_reply_detail(request, reply_id):
    if not _check_admin(request):
        return _admin_error()
    try:
        reply = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return Response({'error': 'Reply not found'}, status=404)
    from django.db import transaction
    with transaction.atomic():
        post_id = reply.post_id
        reply.delete()
        Post.objects.filter(pk=post_id, reply_count__gt=0).update(reply_count=F('reply_count') - 1)
    return Response({'success': True})