from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from web.view_helpers import _require_staff_admin, _ctx, now_ms
from api.models import Post, Reply, User, BotConfig, NebyTask
from api.serializers import PostSerializer, ReplySerializer


def admin_neby_manager(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        action = request.POST.get('action', '').strip()
        task_id = request.POST.get('task_id', '').strip()
        post_id = request.POST.get('post_id', '').strip()
        reply_id = request.POST.get('reply_id', '').strip()
        if action == 'cancel_task' and task_id:
            NebyTask.objects.filter(pk=task_id, status__in=('pending', 'processing', 'failed')).delete()
        elif action == 'retry_task' and task_id:
            NebyTask.objects.filter(pk=task_id, status='failed').update(status='pending', attempts=0)
        elif action == 'delete_post' and post_id:
            from api.cleanup import delete_post_with_cleanup
            try:
                delete_post_with_cleanup(post_id)
            except Post.DoesNotExist:
                pass
        elif action == 'delete_reply' and reply_id:
            from api.cleanup import delete_reply_with_cleanup
            try:
                delete_reply_with_cleanup(reply_id)
            except Reply.DoesNotExist:
                pass
        elif action == 'clear_pending':
            NebyTask.objects.filter(status__in=('pending', 'processing')).delete()
        elif action == 'clear_failed':
            NebyTask.objects.filter(status='failed').delete()
        return redirect('web:admin_neby_manager')

    bot_user = None
    try:
        bot_user = User.objects.get(username__iexact='neby', is_bot=True)
    except User.DoesNotExist:
        pass

    bot_config = BotConfig.objects.filter(bot_username__iexact='neby').first()
    if not bot_config:
        bot_config = BotConfig.objects.filter(enabled=True).first()

    pending_qs = NebyTask.objects.select_related('bot_config').order_by('-created_at')[:50]
    pending_tasks = list(pending_qs)
    pending_count = NebyTask.objects.filter(status='pending').count()
    processing_count = NebyTask.objects.filter(status='processing').count()
    failed_count = NebyTask.objects.filter(status='failed').count()
    done_count = NebyTask.objects.filter(status='done').count()

    bot_posts_qs = Post.objects.filter(user=bot_user).order_by('-created_at') if bot_user else Post.objects.none()
    bot_posts_paginator = Paginator(bot_posts_qs, 20)
    bot_posts_page = bot_posts_paginator.get_page(request.GET.get('posts_page', 1))
    bot_posts_data = []
    for p in bot_posts_page:
        bot_posts_data.append({
            'id': p.id,
            'title': p.title,
            'category': p.category,
            'replyCount': p.reply_count,
            'thumbsUpCount': p.thumbs_up_count,
            'viewCount': p.view_count,
            'createdAt': p.created_at,
        })

    bot_replies_qs = Reply.objects.filter(user=bot_user).select_related('post').order_by('-created_at') if bot_user else Reply.objects.none()
    bot_replies_paginator = Paginator(bot_replies_qs, 20)
    bot_replies_page = bot_replies_paginator.get_page(request.GET.get('replies_page', 1))
    bot_replies_data = []
    for r in bot_replies_page:
        bot_replies_data.append({
            'id': r.id,
            'post_id': r.post_id,
            'post_title': r.post.title if r.post else '',
            'parent_id': r.parent_reply_id or '',
            'content': r.content,
            'thumbsUpCount': r.thumbs_up_count,
            'createdAt': r.created_at,
        })

    stats = {
        'pending': pending_count,
        'processing': processing_count,
        'failed': failed_count,
        'done': done_count,
        'bot_posts_total': bot_posts_qs.count() if bot_user else 0,
        'bot_replies_total': bot_replies_qs.count() if bot_user else 0,
    }

    return render(request, 'admin_panel/neby_manager.html', _ctx(request,
        active_page='neby',
        bot_user=bot_user,
        bot_config=bot_config,
        stats=stats,
        pending_tasks=pending_tasks,
        bot_posts=bot_posts_data,
        bot_posts_page=bot_posts_page,
        bot_replies=bot_replies_data,
        bot_replies_page=bot_replies_page,
    ))


def admin_neby_task_delete(request, task_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    NebyTask.objects.filter(pk=task_id).delete()
    return redirect('web:admin_neby_manager')
