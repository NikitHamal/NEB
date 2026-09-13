import json
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from api.models import BotConfig, LazyDocMessage, LazyDocSession
from web.view_helpers import _ctx, _require_staff_admin
from web.lazy_service import (
    LAZY_GENERATE_SYSTEM, LAZY_EDIT_SYSTEM, LAZY_SECTION_SYSTEM,
    LAZY_REPLY_SYSTEM, LAZY_PLANNER_SYSTEM, get_lazy_prompts,
)


def _get_or_create_lazy_bot(username, default_name, default_provider, default_model, default_chain):
    cfg, _ = BotConfig.objects.get_or_create(
        bot_username__iexact=username,
        defaults={
            'name': default_name,
            'bot_username': username,
            'display_name': default_name,
            'provider': default_provider,
            'model': default_model,
            'fallback_chain': default_chain,
            'enabled': True,
        }
    )
    return cfg


@require_http_methods(['GET', 'POST'])
def admin_lazy_config(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    default_pro_chain = (
        '[{"provider": "geminiweb", "model": "geminiweb/gemini-flash-lite"}, '
        '{"provider": "tryingopen", "model": "qwen/qwen3.8-27b"}, '
        '{"provider": "inception", "model": "mercury-2"}, '
        '{"provider": "k2think", "model": "IFM/K2-Horizon-375B-A23B"}, '
        '{"provider": "longcat", "model": "longcat/LongCat-2.0"}, '
        '{"provider": "qwencloud", "model": "qwen3.8-max"}]'
    )
    default_fast_chain = (
        '[{"provider": "geminiweb", "model": "geminiweb/gemini-flash-lite"}, '
        '{"provider": "longcat", "model": "longcat/LongCat-2.0"}, '
        '{"provider": "tryingopen", "model": "qwen/qwen3.8-27b"}, '
        '{"provider": "qwencloud", "model": "qwen-flash"}, '
        '{"provider": "deepai", "model": "standard"}]'
    )

    pro_cfg = _get_or_create_lazy_bot("neby_pro", "Neby Pro (Smart Mode)", "qwen", "qwen3.8-max", default_pro_chain)
    fast_cfg = _get_or_create_lazy_bot("neby_fast", "Neby Fast (Speed Mode)", "geminiweb", "geminiweb/gemini-flash-lite", default_fast_chain)

    if request.method == 'POST':
        action = request.POST.get('action', '').strip()

        if action == 'save_modes':
            # Save Pro Mode
            pro_cfg.provider = request.POST.get('pro_provider', 'qwen').strip()
            pro_cfg.model = request.POST.get('pro_model', 'qwen3.8-max').strip()
            pro_cfg.api_url = request.POST.get('pro_api_url', '').strip()
            pro_cfg.api_key = request.POST.get('pro_api_key', '').strip()
            pro_cfg.fallback_chain = request.POST.get('pro_fallback_chain', '[]').strip()
            pro_cfg.enabled = request.POST.get('pro_enabled') == 'on'
            pro_cfg.save()

            # Save Fast Mode
            fast_cfg.provider = request.POST.get('fast_provider', 'geminiweb').strip()
            fast_cfg.model = request.POST.get('fast_model', 'geminiweb/gemini-flash-lite').strip()
            fast_cfg.api_url = request.POST.get('fast_api_url', '').strip()
            fast_cfg.api_key = request.POST.get('fast_api_key', '').strip()
            fast_cfg.fallback_chain = request.POST.get('fast_fallback_chain', '[]').strip()
            fast_cfg.enabled = request.POST.get('fast_enabled') == 'on'
            fast_cfg.save()

            messages.success(request, 'Lazy AI mode configurations updated successfully!')
            return redirect('web:admin_lazy_config')

        elif action == 'save_prompts':
            prompts_dict = {
                'generate': request.POST.get('prompt_generate', '').strip() or LAZY_GENERATE_SYSTEM,
                'edit': request.POST.get('prompt_edit', '').strip() or LAZY_EDIT_SYSTEM,
                'section': request.POST.get('prompt_section', '').strip() or LAZY_SECTION_SYSTEM,
                'reply': request.POST.get('prompt_reply', '').strip() or LAZY_REPLY_SYSTEM,
                'planner': request.POST.get('prompt_planner', '').strip() or LAZY_PLANNER_SYSTEM,
            }
            pro_cfg.system_prompt = json.dumps(prompts_dict, ensure_ascii=False)
            pro_cfg.save()
            messages.success(request, 'Lazy system prompts updated successfully!')
            return redirect('web:admin_lazy_config')

        elif action == 'reset_prompts':
            pro_cfg.system_prompt = ''
            pro_cfg.save()
            messages.success(request, 'System prompts reset to default academic templates!')
            return redirect('web:admin_lazy_config')

    # Load active prompts
    prompts = get_lazy_prompts()

    # Calculate statistics
    total_sessions = LazyDocSession.objects.count()
    total_docs = LazyDocSession.objects.exclude(doc_html='').count()
    total_messages = LazyDocMessage.objects.count()
    recent_sessions = LazyDocSession.objects.select_related('user').order_by('-updated_at')[:15]

    ctx = _ctx(request,
        active_page='lazy',
        pro_cfg=pro_cfg,
        fast_cfg=fast_cfg,
        prompts=prompts,
        provider_choices=BotConfig.PROVIDER_CHOICES,
        total_sessions=total_sessions,
        total_docs=total_docs,
        total_messages=total_messages,
        recent_sessions=recent_sessions,
    )
    return render(request, 'admin_panel/lazy_config.html', ctx)
