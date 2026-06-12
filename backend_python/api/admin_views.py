import logging
import time

from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count, Sum, Q
from django.db.models import F
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .security import verify_internal_admin_signature, validate_resource_file_url
from .models import User, Resource, ResourceRequest, Post, Reply, FCMToken, Report
from .serializers import UserSerializer, ResourceSerializer, ResourceRequestSerializer, PostSerializer, ReplySerializer, ReportSerializer

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
@permission_classes([AllowAny])
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
    subject_counts_raw = Resource.objects.values('subject').annotate(cnt=Count('id')).values_list('subject', 'cnt')
    subject_counts_split = {}
    for subj_str, cnt in subject_counts_raw:
        for s in (subj_str or '').split(','):
            s = s.strip()
            if s:
                subject_counts_split[s] = subject_counts_split.get(s, 0) + cnt
    subject_counts = dict(sorted(subject_counts_split.items(), key=lambda x: x[1], reverse=True)[:15])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
        for field in ['username', 'email', 'display_name', 'gender', 'class_level', 'subjects', 'pradesh', 'district', 'school', 'photo_url', 'banner_url', 'dob']:
            if field in data:
                setattr(user, field, data[field])
        if 'isLocked' in data:
            user.is_locked = bool(data['isLocked'])
        if 'verification_level' in data:
            try:
                user.verification_level = max(0, min(4, int(data['verification_level'])))
            except (TypeError, ValueError):
                pass
        if 'moderator_level' in data:
            try:
                user.moderator_level = max(0, min(3, int(data['moderator_level'])))
            except (TypeError, ValueError):
                pass
        if 'is_admin' in data:
            user.is_admin = bool(data['is_admin'])
        if 'is_bot' in data:
            user.is_bot = bool(data['is_bot'])
        if 'teacher_verified' in data:
            user.teacher_verified = bool(data['teacher_verified'])
        if 'role' in data:
            if data['role'] in ('student', 'teacher', 'institution', 'explorer'):
                user.role = data['role']
        if 'achievement_badges' in data:
            user.achievement_badges = str(data['achievement_badges'])
        user.save()
        return Response(UserSerializer(user).data)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
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
    cache.delete_many(['home_resources', 'library_all_resources'])
    return Response(ResourceSerializer(resource).data, status=201)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
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
        cache.delete_many(['home_resources', 'library_all_resources'])
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
    cache.delete_many(['home_resources', 'library_all_resources'])
    return Response(ResourceSerializer(resource).data)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def admin_pending_resources(request):
    """GET /api/admin/resources/pending/ — list pending resources.
    POST /api/admin/resources/pending/ — approve or reject a pending resource."""
    if not _check_admin(request):
        return _admin_error()

    if request.method == 'GET':
        qs = Resource.objects.filter(approval_status='pending').order_by('added_at')
        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(subject__icontains=search))
        return Response(ResourceSerializer(qs[:100], many=True).data)

    data = request.data
    resource_id = data.get('resource_id', '').strip()
    action = data.get('action', '').strip()
    if not resource_id or action not in ('approve', 'reject'):
        return Response({'error': 'resource_id and action (approve/reject) required'}, status=400)
    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=404)
    admin_user = _django_user_from_request(request)
    if action == 'approve':
        resource.approval_status = 'approved'
        resource.reviewed_by = admin_user
        resource.reviewed_at = int(time.time() * 1000)
        resource.rejection_reason = ''
        resource.save()
        if resource.uploaded_by_id:
            from . import counters as _counters
            from . import notifications as _notif
            _counters.increment_user_resource_approved(resource.uploaded_by_id)
            _notif.notify_resource_approved(resource.id, resource.uploaded_by_id)
    else:
        resource.approval_status = 'rejected'
        resource.reviewed_by = admin_user
        resource.reviewed_at = int(time.time() * 1000)
        resource.rejection_reason = data.get('reason', '').strip()[:500]
        resource.save()
        if resource.uploaded_by_id:
            from . import notifications as _notif
            _notif.notify_resource_rejected(resource.id, resource.uploaded_by_id, resource.rejection_reason)
    cache.delete_many(['home_resources', 'library_all_resources'])
    return Response(ResourceSerializer(resource).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def admin_resource_requests(request):
    """GET /api/admin/resource-requests/ — list all resource requests."""
    if not _check_admin(request):
        return _admin_error()
    qs = ResourceRequest.objects.select_related('requested_by').all().order_by('-created_at')
    status_filter = request.query_params.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return Response(ResourceRequestSerializer(qs[:100], many=True, context={'request': request}).data)


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_resource_request_update(request, request_id):
    """POST /api/admin/resource-requests/<request_id>/ — fulfill or close a request."""
    if not _check_admin(request):
        return _admin_error()
    try:
        req = ResourceRequest.objects.get(pk=request_id)
    except ResourceRequest.DoesNotExist:
        return Response({'error': 'Request not found'}, status=404)
    action = request.data.get('action', '').strip()
    if action == 'fulfill':
        resource_id = request.data.get('resource_id', '').strip()
        req.status = 'fulfilled'
        req.fulfilled_at = int(time.time() * 1000)
        if resource_id:
            try:
                req.fulfilled_by_id = resource_id
            except Exception:
                pass
        req.save()
    elif action == 'close':
        req.status = 'closed'
        req.save()
    else:
        return Response({'error': 'action must be "fulfill" or "close"'}, status=400)
    return Response(ResourceRequestSerializer(req, context={'request': request}).data)


@api_view(['GET'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def admin_post_detail(request, post_id):
    if not _check_admin(request):
        return _admin_error()
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)

    if request.method == 'GET':
        return Response(PostSerializer(post, context={'request': request}).data)

    from api.cleanup import delete_post_with_cleanup
    try:
        delete_post_with_cleanup(post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)
    return Response({'success': True})


@api_view(['GET'])
@permission_classes([AllowAny])
def admin_post_replies(request, post_id):
    if not _check_admin(request):
        return _admin_error()
    replies = Reply.objects.filter(post_id=post_id).select_related('user')
    return Response(ReplySerializer(replies, many=True, context={'request': request}).data)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def admin_reply_detail(request, reply_id):
    if not _check_admin(request):
        return _admin_error()
    from api.cleanup import delete_reply_with_cleanup
    try:
        delete_reply_with_cleanup(reply_id)
    except Reply.DoesNotExist:
        return Response({'error': 'Reply not found'}, status=404)
    return Response({'success': True})


@api_view(['GET'])
@permission_classes([AllowAny])
def admin_reports_list(request):
    if not _check_admin(request):
        return _admin_error()
    reports = Report.objects.select_related('reporter').all().order_by('-created_at')
    status_filter = request.query_params.get('status', '').strip()
    if status_filter in ('open', 'reviewing', 'resolved', 'dismissed'):
        reports = reports.filter(status=status_filter)
    if request.query_params.get('page'):
        return _paginate(request, reports, ReportSerializer)
    return Response(ReportSerializer(reports[:100], many=True).data)


@api_view(['GET', 'PATCH'])
@permission_classes([AllowAny])
def admin_report_detail(request, report_id):
    if not _check_admin(request):
        return _admin_error()
    try:
        report = Report.objects.get(pk=report_id)
    except Report.DoesNotExist:
        return Response({'error': 'Report not found'}, status=404)

    if request.method == 'GET':
        return Response(ReportSerializer(report).data)

    data = request.data
    new_status = None
    if 'status' in data:
        new_status = str(data['status']).strip()
        if new_status not in ('open', 'reviewing', 'resolved', 'dismissed'):
            return Response({'error': 'Invalid status'}, status=400)
        report.status = new_status
        if new_status in ('resolved', 'dismissed'):
            report.resolved_at = int(time.time() * 1000)
    report.save()
    return Response(ReportSerializer(report).data)