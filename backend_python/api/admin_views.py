import logging
import os
import time

from django.conf import settings
from django.db.models import Count, Sum, Q
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from .authentication import AuthTokenAuthentication
from .models import User, Resource, Post, Reply, FCMToken
from .serializers import UserSerializer, ResourceSerializer, PostSerializer, ReplySerializer

logger = logging.getLogger(__name__)

ADMIN_TOKEN = settings.ADMIN_TOKEN


def _check_admin(request):
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header[7:].strip()
        if token == ADMIN_TOKEN:
            return True
        try:
            user = User.objects.get(auth_token=token)
            if user.username == 'admin':
                return True
        except User.DoesNotExist:
            pass
    return False


def _admin_error():
    return Response({'error': 'Admin access required'}, status=403)


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
    subject_counts = {}
    for r in Resource.objects.all():
        s = r.subject
        subject_counts[s] = subject_counts.get(s, 0) + 1
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
    data = UserSerializer(users, many=True).data
    return Response(data)


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
        return Response(ResourceSerializer(resources, many=True).data)

    import uuid
    data = request.data
    resource = Resource(
        id=data.get('id', str(uuid.uuid4())),
        title=data.get('title', ''),
        description=data.get('description', ''),
        subject=data.get('subject', ''),
        grade_level=data.get('grade_level', ''),
        type=data.get('type', 'PDF'),
        file_url=data.get('file_url', ''),
        thumbnail_url=data.get('thumbnail_url', ''),
        file_size=data.get('file_size', 0),
        added_at=data.get('added_at', int(time.time() * 1000)),
        view_count=data.get('view_count', 0),
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
    for field in ['title', 'description', 'subject', 'grade_level', 'type', 'file_url', 'thumbnail_url']:
        if field in data:
            setattr(resource, field, data[field])
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
    return Response(PostSerializer(posts, many=True, context={'request': request}).data)


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
        post = reply.post
        reply.delete()
        post.reply_count = max(0, post.reply_count - 1)
        post.save(update_fields=['reply_count'])
    return Response({'success': True})