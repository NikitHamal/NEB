"""Views Admin extracted from views.py."""
from django.shortcuts import get_object_or_404
import json
import os
import re
from api import counters as _counters, notifications as _notif
from api.models import (
    PaymentVerification,
    Post,
    Reply,
    Report,
    Resource,
    ResourceRequest,
    User,
    WithdrawalRequest,
)
from api.resource_catalog import EDUCATION_LEVELS, upload_form_options
from api.security import (
    revoke_auth_token,
    validate_and_save_resource_file,
)
from api.serializers import PostSerializer, ReplySerializer, ResourceSerializer, UserSerializer
from api.utils import now_ms, uuid_str
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout as django_logout
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from urllib.parse import quote
from . import api_client as api
from api.resource_form import discard_saved_files, read_listing_fields
from api.view_helpers import parse_paid_fields
from .resource_upload import (
    apply_price,
    clean_file_url_or_error,
    clean_source_url_or_error,
    clean_thumbnail_or_error,
    create_resources,
    replace_file,
    save_uploaded_files,
)
from .view_helpers import (
    _ctx,
    _get_platform_admin,
    _get_platform_user,
    _is_staff_admin,
    _require_staff_admin,
    _serialize_resource,
    _user_achievement_badges,
    get_or_create_seller_balance,
)

def admin_pending_resources(request):
    """Admin page to approve/reject pending resources."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        resource_id = request.POST.get('resource_id', '').strip()
        action = request.POST.get('action', '').strip()
        try:
            resource_obj = Resource.objects.get(pk=resource_id)
            admin_user = _get_platform_admin(request)

            # Identify all resources in the same upload group (or just the resource itself if no group)
            if resource_obj.upload_group_id:
                group_resources = Resource.objects.filter(upload_group_id=resource_obj.upload_group_id)
            else:
                group_resources = [resource_obj]

            if action == 'approve':
                for r in group_resources:
                    r.approval_status = 'approved'
                    r.reviewed_by = admin_user
                    r.reviewed_at = now_ms()
                    r.rejection_reason = ''
                    r.save()
                    if r.uploaded_by_id:
                        _counters.increment_user_resource_approved(r.uploaded_by_id)
                        _notif.notify_resource_approved(r.id, r.uploaded_by_id)
            elif action == 'reject':
                reason = request.POST.get('reason', '').strip()[:500]
                for r in group_resources:
                    r.approval_status = 'rejected'
                    r.reviewed_by = admin_user
                    r.reviewed_at = now_ms()
                    r.rejection_reason = reason
                    r.save()
                    if r.uploaded_by_id:
                        _notif.notify_resource_rejected(r.id, r.uploaded_by_id, reason)
            
            cache.delete_many(['home_resources', 'library_all_resources'])
        except Resource.DoesNotExist:
            pass
        return redirect('web:admin_pending_resources')

    pending = list(Resource.objects.filter(approval_status='pending').select_related('uploaded_by').order_by('added_at'))
    
    # Group the pending resources by upload_group_id to show them as a single request card
    group_members_map = {}
    for r in pending:
        if r.upload_group_id:
            group_members_map.setdefault(r.upload_group_id, []).append(r)

    grouped_pending = []
    seen_groups = set()
    
    for r in pending:
        if r.upload_group_id:
            if r.upload_group_id in seen_groups:
                continue
            seen_groups.add(r.upload_group_id)
            
            group_members = group_members_map.get(r.upload_group_id, [])
            if not group_members:
                continue
                
            lead_r = next((m for m in group_members if m.is_lead), group_members[0])
            lead_data = _serialize_resource(lead_r)
            
            # List all file details in this group
            lead_data['group_files'] = [
                {
                    'id': m.id,
                    'title': m.title,
                    'file_url': m.file.url if m.file else m.file_url,
                    'file_name': os.path.basename(m.file.name) if m.file else 'External URL'
                } for m in group_members
            ]
            grouped_pending.append(lead_data)
        else:
            data = _serialize_resource(r)
            data['group_files'] = [
                {
                    'id': r.id,
                    'title': r.title,
                    'file_url': r.file.url if r.file else r.file_url,
                    'file_name': os.path.basename(r.file.name) if r.file else 'External URL'
                }
            ]
            grouped_pending.append(data)

    return render(request, 'admin_panel/pending_resources.html', {
        'is_admin': True,
        'pending_resources': grouped_pending,
        'active_page': 'pending_resources',
    })

def admin_resource_requests(request):
    """Admin page to manage resource requests."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        request_id = request.POST.get('request_id', '').strip()
        action = request.POST.get('action', '').strip()
        try:
            req = ResourceRequest.objects.get(pk=request_id)
            if action == 'fulfill':
                req.status = 'fulfilled'
                req.fulfilled_at = now_ms()
                resource_id = request.POST.get('resource_id', '').strip()
                if resource_id:
                    req.fulfilled_by_id = resource_id
                req.save()
            elif action == 'close':
                req.status = 'closed'
                req.save()
            elif action == 'reopen':
                req.status = 'open'
                req.save()
        except ResourceRequest.DoesNotExist:
            pass
        return redirect('web:admin_resource_requests')

    status_filter = request.GET.get('status', '')
    qs = ResourceRequest.objects.select_related('requested_by').all().order_by('-created_at')
    if status_filter:
        qs = qs.filter(status=status_filter)
    requests_data = []
    for req in qs[:100]:
        rd = {
            'id': req.id,
            'title': req.title,
            'description': req.description or '',
            'subject': req.subject,
            'grade_level': req.grade_level,
            'status': req.status,
            'upvote_count': req.upvote_count,
            'created_at': req.created_at,
            'requested_by_name': req.requested_by.display_name or req.requested_by.username if req.requested_by else (req.requester_name or 'Anonymous'),
            'requester_email': req.requester_email or '',
        }
        requests_data.append(rd)
    return render(request, 'admin_panel/resource_requests.html', {
        'is_admin': True,
        'requests': requests_data,
        'current_status': status_filter,
        'active_page': 'resource_requests',
    })

def admin_login(request):
    if _is_staff_admin(request):
        return redirect('web:admin_dashboard')
    if _get_platform_user(request):
        return HttpResponse('Administrator access is required.', status=403)
    next_url = quote(reverse('web:admin_dashboard'), safe='/')
    return redirect(f"{reverse('web:login')}?next={next_url}")

def admin_logout(request):
    token = api.get_session_token(request)
    if token:
        revoke_auth_token(token)
    api.clear_session_auth(request)
    django_logout(request)
    return redirect('web:landing')

def admin_dashboard(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    stats = cache.get('admin_stats')
    if stats is None or 'pulse_insights' not in stats:
        from django.db.models import Sum, Count
        _now = now_ms()
        one_day_ago = _now - 86400000
        seven_days_ago = _now - 7 * 86400000
        fourteen_days_ago = _now - 14 * 86400000
        thirty_days_ago = _now - 30 * 86400000

        user_agg = User.objects.aggregate(
            total=Count('pk'),
            active_24h=Count('pk', filter=Q(last_active__gte=one_day_ago)),
            week=Count('pk', filter=Q(created_at__gte=seven_days_ago)),
            prev_week=Count('pk', filter=Q(created_at__gte=fourteen_days_ago, created_at__lt=seven_days_ago)),
            month=Count('pk', filter=Q(created_at__gte=thirty_days_ago)),
        )
        res_agg = Resource.objects.aggregate(
            total=Count('pk'),
            views=Sum('view_count'),
            downloads=Sum('download_count'),
            pending=Count('pk', filter=Q(approval_status='pending')),
            week=Count('pk', filter=Q(added_at__gte=seven_days_ago)),
            month=Count('pk', filter=Q(added_at__gte=thirty_days_ago)),
        )
        post_agg = Post.objects.aggregate(
            total=Count('pk'),
            likes=Sum('thumbs_up_count'),
            views=Sum('view_count'),
            solved=Count('pk', filter=Q(is_resolved=True, is_archived=False)),
            week=Count('pk', filter=Q(created_at__gte=seven_days_ago)),
            month=Count('pk', filter=Q(created_at__gte=thirty_days_ago)),
        )
        reply_agg = Reply.objects.aggregate(
            total=Count('pk'),
            likes=Sum('thumbs_up_count'),
            week=Count('pk', filter=Q(created_at__gte=seven_days_ago)),
            month=Count('pk', filter=Q(created_at__gte=thirty_days_ago)),
        )

        total_users = user_agg['total'] or 0
        active_users_24h = user_agg['active_24h'] or 0
        total_resources = res_agg['total'] or 0
        total_posts = post_agg['total'] or 0
        total_replies = reply_agg['total'] or 0
        total_likes = post_agg['likes'] or 0
        total_reply_likes = reply_agg['likes'] or 0
        total_resource_views = res_agg['views'] or 0
        total_resource_downloads = res_agg['downloads'] or 0
        total_post_views = post_agg['views'] or 0
        solved_posts = post_agg['solved'] or 0
        solution_rate = round(solved_posts * 100.0 / total_posts, 1) if total_posts else 0.0
        pending_resources = res_agg['pending'] or 0
        new_users_week = user_agg['week'] or 0
        prev_users_week = user_agg['prev_week'] or 0
        new_users_month = user_agg['month'] or 0
        new_posts_week = post_agg['week'] or 0
        new_posts_month = post_agg['month'] or 0
        new_replies_week = reply_agg['week'] or 0
        new_replies_month = reply_agg['month'] or 0
        new_resources_week = res_agg['week'] or 0
        new_resources_month = res_agg['month'] or 0

        open_reports = Report.objects.filter(status='open').count()
        pending_payments = PaymentVerification.objects.filter(status='pending').count()
        pending_withdrawals = WithdrawalRequest.objects.filter(status='pending').count()

        pulse_insights = [
            {
                'icon': 'trending_up',
                'label': 'Weekly sign-up velocity',
                'value': f'+{new_users_week}',
                'sub': f'{prev_users_week} in the prior 7 days · {active_users_24h} active in 24h',
                'url_name': 'web:admin_analytics',
            },
            {
                'icon': 'check_circle',
                'label': 'Forum resolution rate',
                'value': f'{solution_rate:g}%',
                'sub': f'{solved_posts} solved threads · {total_replies} total replies',
                'url_name': 'web:admin_posts',
            },
            {
                'icon': 'download',
                'label': 'Library reach & downloads',
                'value': f'{total_resource_downloads}',
                'sub': f'{total_resource_views} total resource opens across {total_resources} items',
                'url_name': 'web:admin_resources',
            },
            {
                'icon': 'fact_check',
                'label': 'Action queues needing review',
                'value': f'{pending_resources + open_reports + pending_payments + pending_withdrawals}',
                'sub': f'{pending_resources} uploads · {open_reports} reports · {pending_payments} payments · {pending_withdrawals} payouts',
                'url_name': 'web:admin_pending_resources',
            },
        ]

        recent_users = list(User.objects.order_by('-created_at')[:10])
        top_posts = list(Post.objects.select_related('user').filter(is_archived=False).order_by('-thumbs_up_count')[:10])
        top_viewed_posts = list(Post.objects.select_related('user').filter(is_archived=False).order_by('-view_count')[:10])
        top_viewed_resources = list(Resource.objects.filter(approval_status='approved').order_by('-view_count')[:10])
        subject_counts_raw = Resource.objects.filter(approval_status='approved').values_list('subject').annotate(count=Count('id'))
        subject_counts_split = {}
        for subj_str, cnt in subject_counts_raw:
            for s in (subj_str or '').split(','):
                s = s.strip()
                if s:
                    subject_counts_split[s] = subject_counts_split.get(s, 0) + cnt
        subject_counts = dict(sorted(subject_counts_split.items(), key=lambda x: x[1], reverse=True)[:15])
        category_counts = dict(Post.objects.filter(is_archived=False).values_list('category').annotate(count=Count('id')).order_by('-count')[:10])
        resource_type_counts = dict(Resource.objects.filter(approval_status='approved').values_list('type').annotate(count=Count('id')).order_by('-count'))

        stats = {
            'total_users': total_users,
            'active_users_24h': active_users_24h,
            'total_resources': total_resources,
            'total_posts': total_posts,
            'total_replies': total_replies,
            'total_likes': total_likes,
            'total_reply_likes': total_reply_likes,
            'total_resource_views': total_resource_views,
            'total_resource_downloads': total_resource_downloads,
            'total_post_views': total_post_views,
            'solved_posts': solved_posts,
            'solution_rate': solution_rate,
            'pending_resources': pending_resources,
            'open_reports': open_reports,
            'pending_payments': pending_payments,
            'pending_withdrawals': pending_withdrawals,
            'new_users_week': new_users_week,
            'new_users_month': new_users_month,
            'new_posts_week': new_posts_week,
            'new_posts_month': new_posts_month,
            'new_replies_week': new_replies_week,
            'new_replies_month': new_replies_month,
            'new_resources_week': new_resources_week,
            'new_resources_month': new_resources_month,
            'pulse_insights': pulse_insights,
            'recent_users': recent_users,
            'top_posts': top_posts,
            'top_viewed_posts': top_viewed_posts,
            'top_viewed_resources': top_viewed_resources,
            'subject_counts': subject_counts,
            'category_counts': category_counts,
            'resource_type_counts': resource_type_counts,
        }
        cache.set('admin_stats', stats, 300)
    return render(request, 'admin_panel/dashboard.html', {
        'is_admin': True,
        'stats': stats,
        'active_page': 'dashboard',
    })

def admin_users(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    users_qs = User.objects.all().order_by('-created_at')
    search = request.GET.get('q', '').strip()
    role_filter = request.GET.get('role', '').strip()
    if search:
        users_qs = users_qs.filter(
            Q(username__icontains=search) | Q(email__icontains=search) | Q(display_name__icontains=search)
        )
    if role_filter == 'teacher_verified':
        users_qs = users_qs.filter(role='teacher', teacher_verified=True)
    elif role_filter == 'institution_verified':
        users_qs = users_qs.filter(role='institution', institution_verified=True)
    elif role_filter in ('student', 'teacher', 'institution', 'explorer'):
        users_qs = users_qs.filter(role=role_filter)
    paginator = Paginator(users_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    users_data = [UserSerializer(u).data for u in page_obj]
    return render(request, 'admin_panel/users.html', {
        'is_admin': True,
        'users': users_data,
        'page_obj': page_obj,
        'search': search,
        'role_filter': role_filter,
        'active_page': 'users',
    })

def admin_user_detail(request, user_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        user_obj = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect('web:admin_users')
    if request.method == 'POST':
        if request.POST.get('_method') == 'delete':
            from api.services import delete_user_account
            delete_user_account(user_obj.id, completed_by=_get_platform_admin(request))
            return redirect('web:admin_users')
        new_username = request.POST.get('username', '').strip()
        if new_username and new_username != user_obj.username:
            if User.objects.filter(username=new_username).exclude(pk=user_obj.pk).exists():
                return HttpResponse('Username already taken by another user.', status=409)
            user_obj.username = new_username
        for field in ['email', 'display_name', 'gender', 'class_level', 'subjects', 'pradesh', 'district', 'school', 'bio', 'photo_url', 'banner_url']:
            val = request.POST.get(field, '').strip()
            if val:
                setattr(user_obj, field, val)
        # Allow clearing these explicit-clear fields (e.g. to remove a photo)
        for clearable in ['bio', 'photo_url', 'banner_url']:
            if clearable in request.POST and not request.POST.get(clearable, '').strip():
                setattr(user_obj, clearable, None)
        # Handle direct image uploads (override URL field if a file is provided)
        from api.security import save_profile_image_upload, save_banner_image_upload
        photo_upload = request.FILES.get('photo_upload')
        if photo_upload:
            try:
                user_obj.photo_url = save_profile_image_upload(request, user_obj, photo_upload)
            except Exception as upload_err:
                return HttpResponse(f'Photo upload failed: {upload_err}', status=400)
        banner_upload = request.FILES.get('banner_upload')
        if banner_upload:
            try:
                user_obj.banner_url = save_banner_image_upload(request, user_obj, banner_upload)
            except Exception as upload_err:
                return HttpResponse(f'Banner upload failed: {upload_err}', status=400)
        user_obj.is_locked = request.POST.get('is_locked') == 'on'
        ban = request.POST.get('is_banned') == 'on'
        if ban and not user_obj.is_banned:
            user_obj.is_banned = True
            try:
                from api.security import revoke_all_user_tokens
                revoke_all_user_tokens(user_obj)
            except Exception:
                pass
        elif not ban:
            user_obj.is_banned = False
        user_obj.verification_level = int(request.POST.get('verification_level', '0'))
        user_obj.moderator_level = int(request.POST.get('moderator_level', '0'))
        user_obj.is_admin = request.POST.get('is_admin') == 'on'
        user_obj.is_bot = request.POST.get('is_bot') == 'on'
        role = request.POST.get('role', '').strip()
        if role in ('student', 'teacher', 'institution', 'explorer'):
            user_obj.role = role
        user_obj.teacher_verified = request.POST.get('teacher_verified') == 'on'
        user_obj.institution_verified = request.POST.get('institution_verified') == 'on'
        user_obj.achievement_badges = request.POST.get('achievement_badges', '')
        user_obj.save()
        try:
            from api.institutions import heal_owner
            heal_owner(user_obj)
        except Exception:
            pass
    user_data = UserSerializer(user_obj).data
    achievement_badges_list = _user_achievement_badges(user_obj)
    from api.models import NEPAL_DISTRICTS
    return render(request, 'admin_panel/user_detail.html', {
        'is_admin': True,
        'user_detail': user_data,
        'user_is_banned': bool(user_obj.is_banned),
        'achievement_badges_list': achievement_badges_list,
        'active_page': 'users',
        'nepal_districts': NEPAL_DISTRICTS,
    })

def admin_resources(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        subject = request.POST.get('subject', '').strip()
        from api.education_catalog import canonical_level
        grade_level = canonical_level(request.POST.get('grade_level', ''))
        rtype = request.POST.get('type', '').strip() or 'PDF'
        file_url = request.POST.get('file_url', '').strip()
        thumbnail_url = request.POST.get('thumbnail_url', '').strip()
        description = request.POST.get('description', '').strip()
        uploaded_file = request.FILES.get('file')
        tags = request.POST.get('tags', '').strip()
        faculty = request.POST.get('faculty', '').strip()
        program = request.POST.get('program', '').strip()
        year = request.POST.get('year', '').strip()
        exam_type = request.POST.get('exam_type', '').strip()
        pradesh = request.POST.get('pradesh', '').strip()
        district = request.POST.get('district', '').strip()
        school = request.POST.get('school', '').strip()
        author_name = request.POST.get('author_name', '').strip()
        source_url = request.POST.get('source_url', '').strip()
        source_label = request.POST.get('source_label', '').strip()

        file_path = ''
        file_size = 0
        if uploaded_file:
            path, size, err_resp = validate_and_save_resource_file(request, uploaded_file)
            if not err_resp:
                file_path = path or ''
                file_size = size
                file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path) if file_path else ''

        if title and subject and (file_path or file_url):
            try:
                from api.security import validate_resource_file_url as _validate, clean_source_url as _clean_src
                safe_url = ''
                if file_url and not file_path:
                    safe_url = _validate(file_url)
                elif file_url:
                    safe_url = file_url
                safe_thumb = ''
                if thumbnail_url:
                    safe_thumb = _validate(thumbnail_url)
                source_url = _clean_src(source_url)
                Resource.objects.create(
                    id=uuid_str(),
                    title=title,
                    description=description,
                    subject=subject,
                    grade_level=grade_level,
                    faculty=faculty,
                    program=program,
                    year=year,
                    exam_type=exam_type,
                    pradesh=pradesh,
                    district=district,
                    school=school,
                    tags=tags,
                    type=rtype,
                    file=file_path or None,
                    file_url=safe_url,
                    thumbnail_url=safe_thumb,
                    file_size=file_size or int(request.POST.get('file_size', '0')),
                    added_at=now_ms(),
                    view_count=0,
                    author_name=author_name,
                    source_url=source_url,
                    source_label=source_label,
                )
            except Exception:
                pass
    resources_qs = Resource.objects.all().order_by('-added_at')
    search = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    if search:
        resources_qs = resources_qs.filter(Q(title__icontains=search) | Q(description__icontains=search))
    if status_filter in ('approved', 'pending', 'rejected'):
        resources_qs = resources_qs.filter(approval_status=status_filter)
    paginator = Paginator(resources_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    resources_data = [ResourceSerializer(r).data for r in page_obj]
    return render(request, 'admin_panel/resources.html', {
        'is_admin': True,
        'resources': resources_data,
        'page_obj': page_obj,
        'search': search,
        'status_filter': status_filter,
        'pending_count': Resource.objects.filter(approval_status='pending').count(),
        'active_page': 'resources',
    })

def admin_resource_create(request):
    """Standalone admin resource creation page â€” full-featured form matching the public upload page."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    form_options = upload_form_options()

    if request.method == 'POST':
        post = request.POST
        fields = read_listing_fields(post)
        errors = []
        source_type = post.get('source_type', 'admin').strip()
        if source_type not in ('admin', 'user', 'anonymous', 'external'):
            source_type = 'admin'
        approval_status = post.get('approval_status', 'approved').strip()
        if approval_status not in ('approved', 'pending', 'rejected'):
            approval_status = 'approved'
        view_count = int(post.get('view_count', '0') or '0')
        behalf_username = post.get('behalf_username', '').strip().lstrip('@')
        behalf_user = None
        if behalf_username:
            behalf_user = User.objects.filter(username__iexact=behalf_username).first()
            if not behalf_user:
                errors.append(f"No platform user found with username '@{behalf_username}'.")

        is_paid, price = parse_paid_fields(post)
        if is_paid and price <= 0:
            errors.append('Please set a valid price (greater than Rs. 0) for paid resources.')
        source_url = clean_source_url_or_error(post, errors)

        uploaded_files = request.FILES.getlist('file')
        file_url = post.get('file_url', '').strip()
        if not fields['title']:
            errors.append('Title is required.')
        if not fields['subject']:
            errors.append('Subject is required.')
        if not uploaded_files and not file_url:
            errors.append('Please upload a file or provide a file URL.')

        saved_files = save_uploaded_files(request, uploaded_files, errors)
        safe_file_url = clean_file_url_or_error(file_url, errors) if file_url and not uploaded_files else ''
        thumbnail_url = clean_thumbnail_or_error(request, errors)

        if not errors:
            admin_user = _get_platform_admin(request)
            approved = approval_status == 'approved'
            create_resources(
                request, fields, saved_files,
                file_url=safe_file_url,
                thumbnail_url=thumbnail_url,
                view_count=view_count,
                source_type='user' if behalf_user else source_type,
                uploaded_by=behalf_user or admin_user,
                source_url=source_url,
                approval_status=approval_status,
                reviewed_by=admin_user if approved else None,
                reviewed_at=now_ms() if approved else 0,
                is_paid=is_paid,
                price=price,
            )
            cache.delete_many(['home_resources', 'library_all_resources'])
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'redirect': reverse('web:admin_resources')})
            return redirect('web:admin_resources')
        discard_saved_files(saved_files)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        return render(request, 'admin_panel/resource_create.html', {
            'is_admin': True,
            'active_page': 'resources',
            **form_options,
            'source_types': Resource.SOURCE_TYPES,
            'approval_choices': Resource.APPROVAL_CHOICES,
            'errors': errors,
            'form_data': request.POST,
        })

    return render(request, 'admin_panel/resource_create.html', {
        'is_admin': True,
        'active_page': 'resources',
        **form_options,
        'source_types': Resource.SOURCE_TYPES,
        'approval_choices': Resource.APPROVAL_CHOICES,
    })

def admin_resource_edit(request, resource_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        resource_obj = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return redirect('web:admin_resources')
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            replace_file(request, resource_obj, uploaded_file)
        for field in ['title', 'description', 'subject', 'grade_level', 'faculty', 'program', 'year', 'exam_type', 'pradesh', 'district', 'school', 'tags', 'type', 'author_name', 'source_url', 'source_label']:
            setattr(resource_obj, field, request.POST.get(field, '').strip())
        resource_obj.file_url = request.POST.get('file_url', '').strip()
        resource_obj.thumbnail_url = request.POST.get('thumbnail_url', '').strip()
        st = request.POST.get('source_type', '').strip()
        if st in ('admin', 'user', 'anonymous', 'external'):
            resource_obj.source_type = st
        behalf_username = request.POST.get('behalf_username', '').strip().lstrip('@')
        if behalf_username:
            try:
                resource_obj.uploaded_by = User.objects.get(username__iexact=behalf_username)
                resource_obj.source_type = 'user'
            except User.DoesNotExist:
                pass
        elif request.POST.get('clear_behalf') == '1':
            resource_obj.uploaded_by = None
        if request.POST.get('view_count', '').strip():
            resource_obj.view_count = int(request.POST.get('view_count', '0'))
        apply_price(resource_obj, request.POST)
        new_status = request.POST.get('approval_status', '').strip()
        if new_status in ('approved', 'pending', 'rejected'):
            old_status = resource_obj.approval_status
            resource_obj.approval_status = new_status
            resource_obj.reviewed_by = _get_platform_admin(request)
            resource_obj.reviewed_at = now_ms()
            if new_status == 'rejected':
                resource_obj.rejection_reason = request.POST.get('rejection_reason', '').strip()[:500]
            else:
                resource_obj.rejection_reason = ''
            if old_status == 'pending' and new_status == 'approved' and resource_obj.uploaded_by_id:
                _counters.increment_user_resource_approved(resource_obj.uploaded_by_id)
                _notif.notify_resource_approved(resource_obj.id, resource_obj.uploaded_by_id)
            elif old_status == 'pending' and new_status == 'rejected' and resource_obj.uploaded_by_id:
                _notif.notify_resource_rejected(resource_obj.id, resource_obj.uploaded_by_id, resource_obj.rejection_reason)
        resource_obj.save()
        cache.delete_many(['home_resources', 'library_all_resources'])
        return redirect('web:admin_resources')
    form_options = upload_form_options()
    resource_data = ResourceSerializer(resource_obj).data
    resource_data['rejection_reason'] = resource_obj.rejection_reason or ''
    if resource_obj.uploaded_by:
        resource_data['uploaded_by_name'] = resource_obj.uploaded_by.display_name or resource_obj.uploaded_by.username
        resource_data['uploaded_by_username'] = resource_obj.uploaded_by.username
        resource_data['uploaded_by_photo'] = resource_obj.uploaded_by.photo_url or ''
    else:
        resource_data['uploaded_by_name'] = ''
        resource_data['uploaded_by_username'] = ''
        resource_data['uploaded_by_photo'] = ''
    return render(request, 'admin_panel/resource_edit.html', {
        'is_admin': True,
        'resource': resource_data,
        'active_page': 'resources',
        'source_types': Resource.SOURCE_TYPES,
        'approval_choices': Resource.APPROVAL_CHOICES,
        **form_options,
    })

@require_POST
def admin_resource_delete(request, resource_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        Resource.objects.get(pk=resource_id).delete()
    except Resource.DoesNotExist:
        pass
    return redirect('web:admin_resources')

def _admin_report_target_context(report):
    target = None
    target_url = ''
    admin_url = ''
    public_url = ''
    author_name = ''
    author_id = ''
    summary = ''
    title = ''
    exists = True
    try:
        if report.target_type == 'post':
            target = Post.objects.select_related('user').get(pk=report.target_id)
            title = target.title
            summary = target.content
            author_name = target.user.username if target.user else ''
            author_id = str(target.user_id or '')
            target_url = reverse('web:admin_post_detail', kwargs={'post_id': target.id})
            admin_url = target_url
            public_url = reverse('web:forum_post', kwargs={'post_id': target.id})
        elif report.target_type == 'reply':
            target = Reply.objects.select_related('user', 'post').get(pk=report.target_id)
            title = 'Reply on ' + (target.post.title if target.post else 'forum post')
            summary = target.content
            author_name = target.user.username if target.user else ''
            author_id = str(target.user_id or '')
            target_url = reverse('web:admin_post_detail', kwargs={'post_id': target.post_id})
            admin_url = target_url
            public_url = reverse('web:forum_post', kwargs={'post_id': target.post_id}) + '#reply-' + target.id
        elif report.target_type == 'resource':
            target = Resource.objects.select_related('uploaded_by').get(pk=report.target_id)
            title = target.title
            summary = target.description
            author_name = target.uploaded_by.username if target.uploaded_by else (target.author_name or '')
            author_id = str(target.uploaded_by_id or '')
            target_url = reverse('web:admin_resource_edit', kwargs={'resource_id': target.id})
            admin_url = target_url
            public_url = reverse('web:reader', kwargs={'resource_id': target.id})
        elif report.target_type == 'user':
            target = User.objects.get(pk=report.target_id)
            title = target.display_name or target.username
            summary = target.bio
            author_name = target.username
            author_id = str(target.id)
            target_url = reverse('web:admin_user_detail', kwargs={'user_id': target.id})
            admin_url = target_url
            public_url = reverse('web:profile', kwargs={'username': target.username})
    except Exception:
        exists = False
    return {
        'exists': exists,
        'title': title or report.target_id,
        'summary': (summary or '')[:500],
        'author_name': author_name,
        'author_id': author_id,
        'target_url': target_url,
        'admin_url': admin_url,
        'public_url': public_url,
    }


def admin_reports(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    status_filter = request.GET.get('status', '').strip()
    type_filter = request.GET.get('type', '').strip()
    search = request.GET.get('q', '').strip()
    qs = Report.objects.select_related('reporter', 'resolved_by').all().order_by('-created_at')
    if status_filter:
        qs = qs.filter(status=status_filter)
    if type_filter:
        qs = qs.filter(target_type=type_filter)
    if search:
        qs = qs.filter(
            Q(id__icontains=search) |
            Q(target_id__icontains=search) |
            Q(description__icontains=search) |
            Q(reporter__username__icontains=search)
        )
    from django.db.models import Count
    raw_counts = Report.objects.aggregate(
        open=Count('pk', filter=Q(status='open')),
        reviewing=Count('pk', filter=Q(status='reviewing')),
        resolved=Count('pk', filter=Q(status='resolved')),
        dismissed=Count('pk', filter=Q(status='dismissed')),
        total=Count('pk'),
    )
    counts = {k: (v or 0) for k, v in raw_counts.items()}
    paginator = Paginator(qs, 30)
    page_obj = paginator.get_page(request.GET.get('page'))
    reports = []
    for report in page_obj:
        reports.append({
            'report': report,
            'target': _admin_report_target_context(report),
        })
    return render(request, 'admin_panel/reports.html', {
        'is_admin': True,
        'active_page': 'reports',
        'reports': reports,
        'page_obj': page_obj,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'search': search,
        'counts': counts,
        'status_choices': Report.STATUS_CHOICES,
        'type_choices': [('post', 'Post'), ('reply', 'Reply'), ('resource', 'Resource'), ('user', 'User')],
    })


def admin_report_detail(request, report_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        report = Report.objects.select_related('reporter', 'resolved_by').get(pk=report_id)
    except Report.DoesNotExist:
        return redirect('web:admin_reports')

    if request.method == 'POST':
        status = request.POST.get('status', '').strip()
        if status in dict(Report.STATUS_CHOICES):
            report.status = status
            if status in ('resolved', 'dismissed'):
                report.resolved_at = now_ms()
                report.resolved_by = _get_platform_admin(request)
            elif status in ('open', 'reviewing'):
                report.resolved_at = 0
                report.resolved_by = None
            report.save()
        return redirect('web:admin_report_detail', report_id=report.id)

    return render(request, 'admin_panel/report_detail.html', {
        'is_admin': True,
        'active_page': 'reports',
        'report': report,
        'target': _admin_report_target_context(report),
        'status_choices': Report.STATUS_CHOICES,
    })

def admin_posts(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    posts_qs = Post.objects.select_related('user', 'poll').all().order_by('-created_at')
    search = request.GET.get('q', '').strip()
    if search:
        posts_qs = posts_qs.filter(Q(title__icontains=search) | Q(content__icontains=search))
    paginator = Paginator(posts_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    from api.view_helpers import prime_for_serializers
    page_items = list(page_obj)
    prime_for_serializers(None, posts=page_items)
    posts_data = [PostSerializer(p, context={}).data for p in page_items]
    return render(request, 'admin_panel/posts.html', {
        'is_admin': True,
        'posts': posts_data,
        'page_obj': page_obj,
        'search': search,
        'active_page': 'posts',
    })

def admin_post_detail(request, post_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        post_obj = Post.objects.select_related('user').get(pk=post_id)
    except Post.DoesNotExist:
        return redirect('web:admin_posts')
    post_data = PostSerializer(post_obj, context={}).data
    replies_qs = Reply.objects.filter(post_id=post_id).select_related('user')
    replies_data = [ReplySerializer(r, context={}).data for r in replies_qs]
    from api.models import PostView
    viewers_qs = PostView.objects.filter(post_id=post_id).select_related('user').order_by('-viewed_at')[:50]
    viewers = [
        {
            'userId': v.user_id,
            'username': v.user.username,
            'displayName': v.user.display_name,
            'photoUrl': v.user.photo_url or '',
            'viewedAt': v.viewed_at,
        }
        for v in viewers_qs
    ]
    viewer_count = PostView.objects.filter(post_id=post_id).count()
    return render(request, 'admin_panel/post_detail.html', {
        'is_admin': True,
        'post': post_data,
        'replies': replies_data,
        'viewers': viewers,
        'viewer_count': viewer_count,
        'active_page': 'posts',
    })

@require_POST
def admin_post_delete(request, post_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.cleanup import delete_post_with_cleanup
    try:
        delete_post_with_cleanup(post_id)
    except Post.DoesNotExist:
        pass
    return redirect('web:admin_posts')

@require_POST
def admin_reply_delete(request, reply_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.cleanup import delete_reply_with_cleanup
    try:
        delete_reply_with_cleanup(reply_id)
    except Reply.DoesNotExist:
        pass
    return redirect('web:admin_posts')

def admin_bots(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.models import BotConfig
    bots = BotConfig.objects.all().order_by('id')
    bot_list = []
    for bot in bots:
        bot_user = BotConfig.get_bot_user(bot)
        task_stats = {
            'pending': bot.tasks.filter(status='pending').count(),
            'processing': bot.tasks.filter(status='processing').count(),
            'done': bot.tasks.filter(status='done').count(),
            'failed': bot.tasks.filter(status='failed').count(),
        }
        bot_list.append({
            'config': bot,
            'user': bot_user,
            'task_stats': task_stats,
        })
    ctx = _ctx(request, active_page='bot', bot_list=bot_list)
    return render(request, 'admin_panel/bot_list.html', ctx)

def admin_bot_edit(request, bot_id=None):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.models import BotConfig
    if bot_id:
        config = BotConfig.objects.filter(pk=bot_id).first()
        if not config:
            messages.error(request, 'Bot not found.')
            return redirect('/admin/bots/')
    else:
        config = None

    if request.method == 'POST':
        action = request.POST.get('action', 'save')
        if action == 'delete' and config:
            bot_username = config.bot_username
            config.delete()
            from django.core.cache import cache
            cache.delete('neby_enabled')
            messages.success(request, f'Bot @{bot_username} deleted.')
            return redirect('/admin/bots/')
        if not config:
            config = BotConfig()
        config.enabled = request.POST.get('enabled') == 'on'
        config.name = request.POST.get('name', config.name or 'Neby').strip()[:100] or 'Neby'
        config.bot_username = request.POST.get('bot_username', config.bot_username or 'neby').strip()[:50].lower() or 'neby'
        config.display_name = request.POST.get('display_name', '').strip()[:100]
        config.avatar_url = request.POST.get('avatar_url', '').strip()
        provider = (request.POST.get('provider') or 'qwen').strip().lower()
        from api.llm.registry import ALL_PRESETS
        allowed_providers = set(ALL_PRESETS.keys()) | {'custom'}
        if provider not in allowed_providers:
            provider = 'qwen'
        config.provider = provider
        config.api_url = request.POST.get('api_url', config.api_url).strip()
        config.api_key = request.POST.get('api_key', config.api_key).strip()
        model = (request.POST.get('model') or '').strip()
        if not model:
            model = (request.POST.get('model_select') or request.POST.get('model_text') or '').strip()
        if model:
            config.model = model[:200]
        elif not config.model:
            config.model = 'qwen3.8-max'
        try:
            raw_chain = json.loads(request.POST.get('fallback_chain') or '[]')
            if not isinstance(raw_chain, list):
                raw_chain = []
        except (ValueError, TypeError):
            raw_chain = []
        chain_allowed = allowed_providers
        clean_chain = []
        for entry in raw_chain[:5]:
            if not isinstance(entry, dict):
                continue
            provider = (entry.get('provider') or '').strip().lower()
            if provider not in chain_allowed:
                continue
            clean_chain.append({
                'provider': provider,
                'model': (entry.get('model') or '').strip()[:200],
                'api_url': (entry.get('api_url') or '').strip()[:2000],
                'api_key': (entry.get('api_key') or '').strip()[:2000],
            })
        config.fallback_chain = json.dumps(clean_chain, ensure_ascii=False)
        config.system_prompt = request.POST.get('system_prompt', config.system_prompt).strip()
        try:
            config.max_context_posts = int(request.POST.get('max_context_posts', config.max_context_posts))
        except (TypeError, ValueError):
            pass
        try:
            config.max_context_replies = int(request.POST.get('max_context_replies', config.max_context_replies))
        except (TypeError, ValueError):
            pass
        try:
            config.response_max_length = int(request.POST.get('response_max_length', config.response_max_length))
        except (TypeError, ValueError):
            pass
        # Validate bot_username uniqueness
        existing = BotConfig.objects.filter(bot_username__iexact=config.bot_username).exclude(pk=config.pk)
        if existing.exists():
            messages.error(request, f'A bot with username @{config.bot_username} already exists.')
            bot_user = BotConfig.get_bot_user(config) if config.pk else None
            ctx = _ctx(request, active_page='bot', config=config, bot_user=bot_user, is_new=not config.pk,
                       **_bot_provider_catalog_ctx())
            return render(request, 'admin_panel/bot_edit.html', ctx)
        config.save()
        from django.core.cache import cache
        cache.delete('neby_enabled')
        bot_user = BotConfig.get_bot_user(config)
        if bot_user:
            from api.agent_social.ensure import ensure_persona
            persona, _ = ensure_persona(
                config, bot_user,
                autonomy_enabled=request.POST.get('autonomy_enabled') == 'on',
                apply_neby_defaults=config.bot_username.lower() == 'neby',
            )
            persona.tagline = (request.POST.get('tagline') or '')[:200]
            persona.origin_story = (request.POST.get('origin_story') or '')[:4000]
            persona.voice_notes = (request.POST.get('voice_notes') or '')[:4000]
            goals_raw = (request.POST.get('goals_text') or '').strip()
            if goals_raw:
                persona.goals = [ln.strip('-• ').strip() for ln in goals_raw.splitlines() if ln.strip()]
            persona.autonomy_enabled = request.POST.get('autonomy_enabled') == 'on'
            try:
                persona.tick_interval_minutes = max(int(request.POST.get('tick_interval_minutes') or persona.tick_interval_minutes), 1)
            except (TypeError, ValueError):
                pass
            try:
                persona.max_posts_per_day = max(int(request.POST.get('max_posts_per_day') or persona.max_posts_per_day), 0)
            except (TypeError, ValueError):
                pass
            persona.save()
        messages.success(request, f'Bot "@{config.bot_username}" saved. Provider: {provider}.')
        return redirect(f'/admin/bots/{config.pk}/')

    bot_user = BotConfig.get_bot_user(config) if config else None
    persona = None
    if config:
        from api.agent_social.models import AgentPersona
        persona = AgentPersona.objects.filter(bot_config=config).first()
    ctx = _ctx(request, active_page='bot', config=config, bot_user=bot_user, is_new=config is None,
               persona=persona, goals_text='\n'.join((persona.goals if persona else [])),
               **_bot_provider_catalog_ctx())
    return render(request, 'admin_panel/bot_edit.html', ctx)


def _bot_provider_catalog_ctx():
    """Registry-driven provider catalog for the bot editor UI."""
    import json as _json
    from api.llm.registry import admin_catalog
    catalog = admin_catalog()
    scraper_options = [{'slug': e['slug'], 'label': e['label']} for e in catalog['scrapers']]
    official_options = [{'slug': e['slug'], 'label': e['label']} for e in catalog['official']]
    provider_config = {}
    for entry in catalog['scrapers'] + catalog['official']:
        provider_config[entry['slug']] = {
            'urlLabel': 'API URL',
            'urlHelp': f"{entry['label']} endpoint (leave default).",
            'urlDefault': entry['base_url'],
            'modelControl': 'select' if entry['models'] else 'text',
            'modelHelp': f"Pick a model (default: {entry['default_model']}).",
            'options': [{'value': m['id'], 'label': m['label']} for m in entry['models']],
        }
    provider_config['custom'] = {
        'urlLabel': 'API URL',
        'urlHelp': 'Full URL to any OpenAI-compatible /chat/completions endpoint.',
        'urlDefault': '',
        'modelControl': 'text',
        'modelHelp': 'Free-form model name as required by the provider.',
        'options': [],
    }
    return {
        'scraper_options': scraper_options,
        'official_options': official_options,
        'provider_options_scrapers': scraper_options,
        'provider_options_official': official_options,
        'provider_config_json': _json.dumps(provider_config),
    }

def admin_bot_create_user(request, bot_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.models import BotConfig, User
    config = get_object_or_404(BotConfig, pk=bot_id)
    if request.method == 'POST':
        username = config.bot_username
        display_name = request.POST.get('display_name') or config.display_name or config.name
        try:
            bot_user = User.objects.create(
                id=f'{username}-bot',
                username=username,
                display_name=display_name,
                is_bot=True,
                email_verified=True,
                created_at=now_ms(),
            )
            messages.success(request, f'Created bot user @{username} (id={bot_user.id}).')
        except Exception as e:
            messages.error(request, f'Failed to create bot user: {e}')
        return redirect(f'/admin/bots/{bot_id}/')
    ctx = _ctx(request, active_page='bot', config=config)
    return render(request, 'admin_panel/bot_create_user.html', ctx)


def admin_agent_activity(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.agent_social.models import AgentAction
    actions = list(
        AgentAction.objects.select_related('persona', 'persona__bot_config').order_by('-created_at')[:120]
    )
    return render(request, 'admin_panel/agent_activity.html', _ctx(
        request, active_page='agent_activity', recent_actions=actions,
    ))


def admin_agent_tick(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    if request.method != 'POST':
        return redirect('/admin/agents/activity/')
    from api.agent_social.heartbeat import tick_neby
    result = tick_neby(force=True, source='admin')
    messages.success(request, f'Heartbeat: {result}')
    return redirect('/admin/agents/activity/')

def admin_syllabus_list(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    
    from api.models import SyllabusContent
    syllabus_qs = SyllabusContent.objects.all().order_by('grade_level', 'subject', 'order')
    
    search = request.GET.get('q', '').strip()
    filter_grade = request.GET.get('grade', '').strip()
    filter_subject = request.GET.get('subject', '').strip()
    
    if search:
        syllabus_qs = syllabus_qs.filter(
            Q(grade_level__icontains=search) | 
            Q(subject__icontains=search) | 
            Q(chapter_title__icontains=search)
        )
    if filter_grade:
        syllabus_qs = syllabus_qs.filter(grade_level=filter_grade)
    if filter_subject:
        syllabus_qs = syllabus_qs.filter(subject__iexact=filter_subject)
    
    all_grades = list(SyllabusContent.objects.order_by('grade_level').values_list('grade_level', flat=True).distinct())
    all_subjects = list(SyllabusContent.objects.order_by('subject').values_list('subject', flat=True).distinct())
    total_count = SyllabusContent.objects.count()
    
    paginator = Paginator(syllabus_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin_panel/syllabus_list.html', {
        'is_admin': True,
        'page_obj': page_obj,
        'search': search,
        'filter_grade': filter_grade,
        'filter_subject': filter_subject,
        'all_grades': all_grades,
        'all_subjects': all_subjects,
        'total_count': total_count,
        'active_page': 'syllabus',
    })

SYLLABUS_GRADE_SUBJECTS = {
    'Class 8': ['English', 'Nepali', 'Mathematics', 'Science', 'Social Studies', 'Health & Physical Education'],
    'Class 9': ['English', 'Nepali', 'Mathematics', 'Science', 'Social Studies', 'Health & Physical Education', 'Account'],
    'Class 10 / SEE': ['English', 'Nepali', 'Mathematics', 'Science', 'Social Studies', 'Health & Physical Education', 'Account', 'Optional Mathematics'],
    'Class 11': ['English', 'Nepali', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'Computer Science', 'Account', 'Economics', 'Business Studies', 'Business Mathematics', 'Hotel Management', 'Sociology', 'Mass Communication', 'Psychology', 'Education', 'Health & Physical Education'],
    'Class 12': ['English', 'Nepali', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'Computer Science', 'Account', 'Economics', 'Business Studies', 'Business Mathematics', 'Hotel Management', 'Sociology', 'Mass Communication', 'Psychology', 'Education', 'Health & Physical Education'],
    'Diploma': ['Computer Engineering', 'Civil Engineering', 'Electrical Engineering', 'Electronics Engineering', 'Architecture', 'Mechanical Engineering', 'Pharmacy'],
    'Bachelor': ['Computer Science', 'Business Administration', 'Engineering', 'Medicine', 'Law', 'Education', 'Management', 'Humanities'],
    'Master': ['Computer Science', 'Business Administration', 'Engineering', 'Education', 'Management'],
    'PhD': ['Science', 'Engineering', 'Humanities', 'Management', 'Education'],
    'Entrance Prep': ['IIT JEE', 'NEET', 'CMAT', 'IOE Entrance', 'CEE Medical', 'Lok Sewa Aayog', 'Public Service Commission'],
    'Competitive Exam': ['Lok Sewa Aayog', 'Bank Exam', 'Nepal Police', 'Armed Police', 'Teacher Service Commission', 'Public Service Commission'],
    'Other': [],
}


def _parse_syllabus_rich_json(raw_text):
    text = (raw_text or '').strip()
    if not text:
        return {}, None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, 'Interactive content JSON is invalid: {}'.format(exc)
    if not isinstance(parsed, dict):
        return None, 'Interactive content JSON must be a JSON object.'
    return parsed, None


def _syllabus_form(request, syllabus_obj=None):
    from api.models import SyllabusContent

    is_edit = syllabus_obj is not None
    existing_ids = list(
        SyllabusContent.objects.exclude(pk=syllabus_obj.pk).values_list('chapter_id', flat=True)
        if is_edit else SyllabusContent.objects.values_list('chapter_id', flat=True)
    )
    context = {
        'is_admin': True,
        'education_levels': EDUCATION_LEVELS,
        'grade_subjects_json': json.dumps(SYLLABUS_GRADE_SUBJECTS),
        'existing_subjects': list(SyllabusContent.objects.order_by('subject').values_list('subject', flat=True).distinct()),
        'existing_ids_json': json.dumps(existing_ids),
        'active_page': 'syllabus',
        'is_edit': is_edit,
    }
    if is_edit:
        context['syllabus'] = syllabus_obj
        context['rich_content_json'] = json.dumps(syllabus_obj.rich_content or {}, ensure_ascii=False, indent=2)

    if request.method != 'POST':
        return render(request, 'admin_panel/syllabus_form.html', context)

    from api.education_catalog import canonical_level
    grade_level = canonical_level(request.POST.get('grade_level', ''))
    subject = request.POST.get('subject', '').strip()
    chapter_title = request.POST.get('chapter_title', '').strip()
    chapter_id = request.POST.get('chapter_id', '').strip()
    rich_content, rich_error = _parse_syllabus_rich_json(request.POST.get('rich_content_json', ''))
    try:
        order = int(request.POST.get('order', '0').strip())
    except ValueError:
        order = 0

    form_error = None
    if not grade_level or not subject or not chapter_title or not chapter_id:
        form_error = 'All required fields (Level, Subject, Chapter Title, Chapter ID) must be filled.'
    elif rich_error:
        form_error = rich_error
    elif chapter_id in existing_ids:
        form_error = 'Chapter ID "{}" already exists. Please use a unique identifier.'.format(chapter_id)
    if form_error:
        return render(request, 'admin_panel/syllabus_form.html', {**context, 'form_error': form_error, 'form_data': request.POST})

    fields = dict(
        grade_level=grade_level,
        subject=subject,
        chapter_id=chapter_id,
        chapter_title=chapter_title,
        text_content=request.POST.get('text_content', '').strip(),
        question_answers=request.POST.get('question_answers', '').strip(),
        rich_content=rich_content or {},
        source_resource_id=request.POST.get('source_resource_id', '').strip()[:36],
        source_label=request.POST.get('source_label', '').strip()[:255],
        order=order,
        updated_at=now_ms(),
    )
    if is_edit:
        for name, value in fields.items():
            setattr(syllabus_obj, name, value)
        syllabus_obj.save()
    else:
        SyllabusContent.objects.create(id=uuid_str(), created_at=fields['updated_at'], **fields)
    return redirect('web:admin_syllabus_list')


def admin_syllabus_create(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    return _syllabus_form(request)


def admin_syllabus_edit(request, entry_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.models import SyllabusContent
    try:
        syllabus_obj = SyllabusContent.objects.get(pk=entry_id)
    except SyllabusContent.DoesNotExist:
        return redirect('web:admin_syllabus_list')
    return _syllabus_form(request, syllabus_obj)


def admin_syllabus_delete(request, entry_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
        
    from api.models import SyllabusContent
    try:
        syllabus_obj = SyllabusContent.objects.get(pk=entry_id)
    except SyllabusContent.DoesNotExist:
        return redirect('web:admin_syllabus_list')
        
    if request.method == 'POST':
        syllabus_obj.delete()
        
    return redirect('web:admin_syllabus_list')

def admin_syllabus_preview(request, entry_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
        
    from api.models import SyllabusContent
    try:
        syllabus_obj = SyllabusContent.objects.get(pk=entry_id)
    except SyllabusContent.DoesNotExist:
        return redirect('web:admin_syllabus_list')
        
    siblings = SyllabusContent.objects.filter(
        grade_level=syllabus_obj.grade_level,
        subject=syllabus_obj.subject
    ).order_by('order', 'chapter_title')
    
    return render(request, 'admin_panel/syllabus_preview.html', {
        'is_admin': True,
        'syllabus': syllabus_obj,
        'siblings': siblings,
        'active_page': 'syllabus',
    })

def admin_syllabus_import(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
        
    from api.models import SyllabusContent
    
    import_result = None
    
    if request.method == 'POST':
        json_data = request.POST.get('json_data', '').strip()
        overwrite = request.POST.get('overwrite', '') == 'on'
        
        if not json_data:
            import_result = {'success': False, 'message': 'No JSON data provided.'}
        else:
            try:
                data = json.loads(json_data)
                if isinstance(data, dict):
                    data = [data]
                if not isinstance(data, list):
                    import_result = {'success': False, 'message': 'JSON must be an array of chapter objects (or a single object).'}
                else:
                    created = 0
                    updated = 0
                    skipped = 0
                    errors = []
                    _now = now_ms()
                    
                    for i, item in enumerate(data):
                        grade = str(item.get('grade_level', '')).strip()
                        subject = str(item.get('subject', '')).strip()
                        title = str(item.get('chapter_title', '')).strip()
                        slug = str(item.get('chapter_id', item.get('slug', ''))).strip()
                        
                        if not grade or not subject or not title:
                            errors.append('Row {}: Missing required field (grade_level, subject, or chapter_title).'.format(i + 1))
                            skipped += 1
                            continue
                        if not slug:
                            slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
                        
                        content = str(item.get('text_content', '')).strip()
                        qa = str(item.get('question_answers', '')).strip()
                        rich_content = item.get('rich_content', {})
                        if not isinstance(rich_content, dict):
                            errors.append('Row {}: rich_content must be a JSON object.'.format(i + 1))
                            skipped += 1
                            continue
                        source_resource_id = str(item.get('source_resource_id', '')).strip()[:36]
                        source_label = str(item.get('source_label', '')).strip()[:255]
                        order = int(item.get('order', 0))
                        
                        if overwrite:
                            existing = SyllabusContent.objects.filter(chapter_id=slug).first()
                            if existing:
                                existing.grade_level = grade
                                existing.subject = subject
                                existing.chapter_title = title
                                existing.text_content = content
                                existing.question_answers = qa
                                existing.rich_content = rich_content
                                existing.source_resource_id = source_resource_id
                                existing.source_label = source_label
                                existing.order = order
                                existing.updated_at = _now
                                existing.save()
                                updated += 1
                                continue
                        
                        obj, created_flag = SyllabusContent.objects.get_or_create(
                            chapter_id=slug,
                            defaults={
                                'id': uuid_str(),
                                'grade_level': grade,
                                'subject': subject,
                                'chapter_title': title,
                                'text_content': content,
                                'question_answers': qa,
                                'rich_content': rich_content,
                                'source_resource_id': source_resource_id,
                                'source_label': source_label,
                                'order': order,
                                'created_at': _now,
                                'updated_at': _now,
                            }
                        )
                        if created_flag:
                            created += 1
                        else:
                            if overwrite:
                                obj.grade_level = grade
                                obj.subject = subject
                                obj.chapter_title = title
                                obj.text_content = content
                                obj.question_answers = qa
                                obj.rich_content = rich_content
                                obj.source_resource_id = source_resource_id
                                obj.source_label = source_label
                                obj.order = order
                                obj.updated_at = _now
                                obj.save()
                                updated += 1
                            else:
                                skipped += 1
                                errors.append('Row {}: chapter_id "{}" already exists. Use overwrite to update.'.format(i + 1, slug))
                    
                    import_result = {
                        'success': True,
                        'created': created,
                        'updated': updated,
                        'skipped': skipped,
                        'errors': errors,
                        'total': len(data),
                        'message': 'Imported {} of {} chapters ({} created, {} updated, {} skipped).'.format(
                            created + updated, len(data), created, updated, skipped
                        ),
                    }
            except json.JSONDecodeError as e:
                import_result = {'success': False, 'message': 'Invalid JSON: {}'.format(str(e))}
    
    return render(request, 'admin_panel/syllabus_import.html', {
        'is_admin': True,
        'education_levels': EDUCATION_LEVELS,
        'import_result': import_result,
        'active_page': 'syllabus',
    })

def admin_syllabus_export(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
        
    from api.models import SyllabusContent
    
    grade = request.GET.get('grade', '').strip()
    subject = request.GET.get('subject', '').strip()
    
    qs = SyllabusContent.objects.all().order_by('grade_level', 'subject', 'order')
    if grade:
        from api.education_catalog import level_match_values
        gq = Q()
        for v in level_match_values(grade) or [grade]:
            gq |= Q(grade_level__iexact=v)
        qs = qs.filter(gq)
    if subject:
        qs = qs.filter(subject__iexact=subject)
    
    data = []
    for item in qs:
        data.append({
            'grade_level': item.grade_level,
            'subject': item.subject,
            'chapter_id': item.chapter_id,
            'chapter_title': item.chapter_title,
            'text_content': item.text_content,
            'question_answers': item.question_answers,
            'rich_content': item.rich_content or {},
            'source_resource_id': item.source_resource_id,
            'source_label': item.source_label,
            'order': item.order,
        })
    
    response = JsonResponse(data, safe=False, json_dumps_params={'indent': 2, 'ensure_ascii': False})
    response['Content-Disposition'] = 'attachment; filename="syllabus_export.json"'
    return response


# ==================== Study Spaces Admin ====================

def admin_study_spaces(request):
    """Admin: list all study spaces with stats, allow deletion."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    from api.models import StudySpace, StudyDocument

    if request.method == 'POST':
        action = request.POST.get('action', '').strip()
        space_id = request.POST.get('space_id', '').strip()
        if action == 'delete' and space_id:
            try:
                StudySpace.objects.filter(id=space_id).delete()
            except Exception:
                pass
        return redirect('web:admin_study_spaces')

    search = request.GET.get('q', '').strip()
    spaces_qs = StudySpace.objects.select_related('user').order_by('-created_at')
    if search:
        spaces_qs = spaces_qs.filter(
            Q(title__icontains=search) |
            Q(user__username__icontains=search)
        )

    from django.db.models import Count
    space_agg = StudySpace.objects.aggregate(
        total=Count('pk'),
        public=Count('pk', filter=Q(visibility='public')),
    )
    total_spaces = space_agg['total'] or 0
    total_documents = StudyDocument.objects.count()
    public_spaces = space_agg['public'] or 0

    spaces_annotated = spaces_qs.annotate(
        _doc_count=Count('documents', distinct=True),
        _member_count=Count('members', distinct=True),
    )[:100]
    spaces = [
        {
            'id': sp.id,
            'name': sp.title,
            'owner': sp.user,
            'visibility': sp.visibility,
            'doc_count': sp._doc_count,
            'member_count': sp._member_count,
            'created_at': sp.created_at,
        }
        for sp in spaces_annotated
    ]

    return render(request, 'admin_panel/study_spaces.html', {
        'is_admin': True,
        'active_page': 'study_spaces',
        'spaces': spaces,
        'search': search,
        'total_spaces': total_spaces,
        'total_documents': total_documents,
        'public_spaces': public_spaces,
    })


def admin_study_space_delete(request, space_id):
    """Admin: delete a single study space."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    from api.models import StudySpace
    if request.method == 'POST':
        StudySpace.objects.filter(id=space_id).delete()
    return redirect('web:admin_study_spaces')


def admin_deletions(request):
    """Admin view to list pending account deletion requests."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    from api.models import AccountDeletionRequest
    pending_requests = AccountDeletionRequest.objects.filter(status=AccountDeletionRequest.STATUS_PENDING).select_related('user').order_by('-created_at')

    return render(request, 'admin_panel/deletions.html', {
        'is_admin': True,
        'active_page': 'deletions',
        'pending_requests': pending_requests,
    })


def admin_process_deletion(request, request_id):
    """Admin view to execute (delete data) or reject/cancel a deletion request."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    if request.method != 'POST':
        return redirect('web:admin_deletions')

    from api.models import AccountDeletionRequest
    from api.services import delete_user_account

    try:
        del_request = AccountDeletionRequest.objects.get(pk=request_id)
    except AccountDeletionRequest.DoesNotExist:
        return redirect('web:admin_deletions')

    action = request.POST.get('action', '').strip()
    admin_user = _get_platform_admin(request)

    if action == 'delete':
        # Execute the deletion service
        delete_user_account(del_request.user_id, completed_by=admin_user)
    elif action == 'reject':
        # Just delete the request so user is not deleted
        del_request.delete()

    return redirect('web:admin_deletions')

def admin_pending_payments(request):
    """Admin page to verify buyer payment screenshots & transaction IDs."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    admin_user = _get_platform_admin(request)

    if request.method == 'POST':
        payment_id = request.POST.get('payment_id', '').strip()
        action = request.POST.get('action', '').strip()
        reason = request.POST.get('reason', '').strip()[:500]

        try:
            payment_obj = (PaymentVerification.objects
                           .select_related('buyer', 'seller', 'resource', 'course', 'course__page')
                           .get(pk=payment_id))
            title = payment_obj.target_title
            if action == 'approve' and payment_obj.status == 'pending':
                # Claim the row before crediting anybody. A double-clicked
                # Approve, a retried POST or two admins working the same queue
                # all used to pass the `status == 'pending'` check above and
                # credit the seller twice for one transfer; the conditional
                # UPDATE is the lock, and only the request that actually
                # flipped the row goes on to pay out.
                claimed = (PaymentVerification.objects
                           .filter(pk=payment_obj.pk, status='pending')
                           .update(status='approved', verified_at=now_ms(),
                                   verified_by=admin_user, admin_notes=reason))
                if claimed:
                    payment_obj.refresh_from_db()
                    with transaction.atomic():
                        # Credit the seller's wallet, both parties' Nebians points and
                        # the buyer's lifetime spend — one shared implementation, so a
                        # course sale and a resource sale are rewarded identically.
                        from api.marketplace import grant_purchase_rewards
                        grant_purchase_rewards(payment_obj)

                        if payment_obj.course_id:
                            from django.db.models import F
                            from api.models import CreatorCourse
                            CreatorCourse.objects.filter(pk=payment_obj.course_id).update(
                                sale_count=F('sale_count') + 1,
                                enrollment_count=F('enrollment_count') + 1,
                            )

                        _notif.create_notification(
                            recipient=payment_obj.buyer,
                            actor=admin_user or payment_obj.seller,
                            verb='payment_approved',
                            target=payment_obj.course or payment_obj.resource,
                            message=f"Your payment of Rs. {payment_obj.amount} for '{title}' has been verified & approved! You now have full access."
                        )
                        _notif.create_notification(
                            recipient=payment_obj.seller,
                            actor=payment_obj.buyer,
                            verb='sale_credited',
                            target=payment_obj.course or payment_obj.resource,
                            message=f"You earned Rs. {payment_obj.seller_earnings} from the sale of '{title}' to @{payment_obj.buyer.username}!"
                        )

            elif action == 'reject' and payment_obj.status == 'pending':
                rejected = (PaymentVerification.objects
                            .filter(pk=payment_obj.pk, status='pending')
                            .update(status='rejected', verified_at=now_ms(),
                                    verified_by=admin_user, admin_notes=reason))
                if not rejected:
                    return redirect('web:admin_pending_payments')
                payment_obj.refresh_from_db()

                _notif.create_notification(
                    recipient=payment_obj.buyer,
                    actor=admin_user or payment_obj.seller,
                    verb='payment_rejected',
                    target=payment_obj.course or payment_obj.resource,
                    message=f"Your payment verification for '{title}' was rejected. Reason: {reason or 'Invalid proof'}"
                )
        except PaymentVerification.DoesNotExist:
            pass

        return redirect('web:admin_pending_payments')

    # Capped like the processed list below: this queue is unbounded by nature, and
    # a backlog of thousands would render thousands of proof thumbnails into one page.
    pending_payments = (PaymentVerification.objects.filter(status='pending')
                        .select_related('buyer', 'seller', 'resource', 'course', 'course__page')
                        .order_by('-created_at')[:200])
    processed_payments = (PaymentVerification.objects.exclude(status='pending')
                          .select_related('buyer', 'seller', 'resource', 'course', 'course__page', 'verified_by')
                          .order_by('-verified_at')[:50])

    return render(request, 'admin_panel/payments.html', _ctx(request,
        active_page='payments',
        pending_payments=pending_payments,
        processed_payments=processed_payments,
    ))


def admin_withdrawals(request):
    """Admin view for processing seller earnings withdrawal requests."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    admin_user = _get_platform_admin(request)

    if request.method == 'POST':
        request_id = request.POST.get('request_id', '').strip()
        action = request.POST.get('action', '').strip()
        reason = request.POST.get('reason', '').strip()[:500]

        try:
            w_req = WithdrawalRequest.objects.select_related('user').get(pk=request_id)
            if action == 'approve' and w_req.status == 'pending':
                with transaction.atomic():
                    w_req.status = 'approved'
                    w_req.processed_at = now_ms()
                    w_req.processed_by = admin_user
                    w_req.admin_notes = reason
                    w_req.save()

                    # Update total_withdrawn in SellerBalance
                    seller_bal = get_or_create_seller_balance(w_req.user)
                    seller_bal.total_withdrawn += w_req.amount
                    seller_bal.updated_at = now_ms()
                    seller_bal.save()

                    _notif.create_notification(
                        recipient=w_req.user,
                        actor=admin_user,
                        verb='withdrawal_paid',
                        target=None,
                        message=f"Your withdrawal of Rs. {w_req.amount} via {w_req.get_payout_method_display()} has been processed & paid!"
                    )

            elif action == 'reject' and w_req.status == 'pending':
                with transaction.atomic():
                    w_req.status = 'rejected'
                    w_req.processed_at = now_ms()
                    w_req.processed_by = admin_user
                    w_req.admin_notes = reason
                    w_req.save()

                    # Refund balance back to seller
                    seller_bal = get_or_create_seller_balance(w_req.user)
                    seller_bal.current_balance += w_req.amount
                    seller_bal.updated_at = now_ms()
                    seller_bal.save()

                    _notif.create_notification(
                        recipient=w_req.user,
                        actor=admin_user,
                        verb='withdrawal_rejected',
                        target=None,
                        message=f"Your withdrawal request of Rs. {w_req.amount} was rejected. Amount has been refunded to your balance. Reason: {reason or 'Incorrect details'}"
                    )
        except WithdrawalRequest.DoesNotExist:
            pass

        return redirect('web:admin_withdrawals')

    pending_withdrawals = WithdrawalRequest.objects.filter(status='pending').select_related('user').order_by('-created_at')
    processed_withdrawals = WithdrawalRequest.objects.exclude(status='pending').select_related('user', 'processed_by').order_by('-processed_at')[:50]

    return render(request, 'admin_panel/withdrawals.html', _ctx(request,
        active_page='withdrawals',
        pending_withdrawals=pending_withdrawals,
        processed_withdrawals=processed_withdrawals,
    ))