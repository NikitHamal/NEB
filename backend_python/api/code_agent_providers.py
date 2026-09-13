from __future__ import annotations

import time
from dataclasses import dataclass

from django.conf import settings

from api.llm import client as llm_client
from api.llm.credentials import ResolvedProvider, default_selection, resolve
from api.llm.registry import default_model_for, preset
from api.models import BotConfig, User


@dataclass
class CodeProviderResult:
    text: str
    provider: str
    model: str
    context_window: int
    max_output_tokens: int
    elapsed_ms: int


class CodeProviderError(RuntimeError):
    pass


class CodeProviderAdapter:
    def __init__(self, session, on_retry=None, cancelled=None):
        self.session = session
        self.on_retry = on_retry or (lambda *_args, **_kwargs: None)
        self.cancelled = cancelled or (lambda: False)
        self.user = User.objects.filter(pk=session.user_id).first()

    def primary_selection(self) -> dict:
        slug = (self.session.provider or '').strip().lower()
        model = (self.session.model or '').strip()
        provider_id = (getattr(self.session, 'provider_id', '') or '').strip()
        if not slug:
            try:
                sel = default_selection(self.user)
                slug = (sel.get('slug') or '').strip().lower()
                model = model or (sel.get('model') or '').strip()
                provider_id = provider_id or (sel.get('providerId') or '').strip()
            except Exception:
                slug = 'tryingopen'
        if not slug:
            slug = 'tryingopen'
        return {'provider': slug, 'model': model, 'provider_id': provider_id}

    def estimated_context_window(self) -> int:
        entry = self.primary_selection()
        try:
            resolved = self._resolve(entry)
            if resolved and resolved.context_window:
                return int(resolved.context_window)
        except Exception:
            pass
        p = preset(entry['provider'])
        return int(p.context_window if p else 131072)

    def provider_chain(self) -> list[dict]:
        primary = self.primary_selection()
        chain = [primary]
        seen = {(primary['provider'], primary.get('provider_id') or '')}

        try:
            bot = BotConfig.objects.filter(enabled=True, provider=primary['provider']).first()
            if bot and hasattr(bot, 'get_fallback_chain'):
                for entry in bot.get_fallback_chain() or []:
                    slug = str(entry.get('provider') or '').strip().lower()
                    if not slug:
                        continue
                    key = (slug, str(entry.get('provider_id') or ''))
                    if key in seen:
                        continue
                    seen.add(key)
                    chain.append({
                        'provider': slug,
                        'model': str(entry.get('model') or '').strip(),
                        'provider_id': str(entry.get('provider_id') or '').strip(),
                        'api_url': str(entry.get('api_url') or '').strip(),
                        'api_key': str(entry.get('api_key') or '').strip(),
                    })
        except Exception:
            pass

        fallbacks = getattr(
            settings,
            'CODE_AGENT_FALLBACKS',
            ['tryingopen', 'qwencloud', 'qwen', 'longcat', 'geminiweb', 'k2think'],
        )
        if isinstance(fallbacks, str):
            fallbacks = [item.strip() for item in fallbacks.split(',') if item.strip()]
        for raw in fallbacks or []:
            slug = str(raw or '').strip().lower()
            if not slug or (slug, '') in seen:
                continue
            seen.add((slug, ''))
            chain.append({'provider': slug, 'model': '', 'provider_id': ''})
        return chain

    def call(self, system: str, prompt: str) -> CodeProviderResult:
        errors = []
        chain = self.provider_chain()
        for index, entry in enumerate(chain):
            if self.cancelled():
                raise CodeProviderError('cancelled')
            slug = entry['provider']
            model = entry.get('model') or ''
            try:
                result = self._call_entry(entry, system, prompt)
                if result.text.strip():
                    return result
                errors.append(f'{slug}: empty response')
            except Exception as exc:
                errors.append(f'{slug}: {str(exc)[:500]}')
                if index + 1 < len(chain):
                    self.on_retry(slug, str(exc)[:500])
        raise CodeProviderError('All providers failed: ' + ' | '.join(errors[:6]))

    def _resolve(self, entry: dict) -> ResolvedProvider | None:
        slug = entry['provider']
        model = entry.get('model') or ''
        provider_id = entry.get('provider_id') or ''
        resolved = resolve(self.user, slug, model=model, user_provider_id=provider_id)
        if resolved and entry.get('api_url'):
            resolved.base_url = entry['api_url']
        if resolved and entry.get('api_key'):
            resolved.api_key = entry['api_key']
        return resolved

    def _call_entry(self, entry: dict, system: str, prompt: str) -> CodeProviderResult:
        slug = entry['provider']
        resolved = self._resolve(entry)
        if resolved and resolved.official:
            return self._call_official(resolved, system, prompt)

        p = preset(slug)
        model = entry.get('model') or (resolved.model if resolved else '') or default_model_for(slug)
        context_window = (resolved.context_window if resolved else 0) or (p.context_window if p else 131072)
        max_output = (resolved.max_output_tokens if resolved else 0) or (p.max_output_tokens if p else 8192)
        max_output = max(1000, min(int(getattr(settings, 'CODE_AGENT_MODEL_MAX_TOKENS', max_output)), 32768))
        started = time.monotonic()
        text = _call_community(
            slug,
            model,
            system,
            prompt,
            effort=(self.session.effort or 'balanced'),
            max_tokens=max_output,
        )
        elapsed_ms = int((time.monotonic() - started) * 1000)
        if not text:
            raise CodeProviderError(f'{slug} {model} returned an empty response')
        return CodeProviderResult(
            text=str(text), provider=slug, model=model,
            context_window=context_window, max_output_tokens=max_output,
            elapsed_ms=elapsed_ms,
        )

    def _call_official(self, resolved: ResolvedProvider, system: str, prompt: str) -> CodeProviderResult:
        max_output = max(
            1000,
            min(int(getattr(settings, 'CODE_AGENT_MODEL_MAX_TOKENS', resolved.max_output_tokens or 8192)), 32768),
        )
        messages = []
        if system.strip():
            messages.append({'role': 'system', 'content': system})
        messages.append({'role': 'user', 'content': prompt})
        started = time.monotonic()
        result = llm_client.chat(
            format=resolved.format,
            base_url=resolved.base_url,
            api_key=resolved.api_key,
            model=resolved.model,
            messages=messages,
            max_tokens=max_output,
            timeout=int(getattr(settings, 'CODE_AGENT_MODEL_TIMEOUT', 300)),
            temperature=0.2,
            provider=resolved.slug,
        )
        elapsed_ms = int((time.monotonic() - started) * 1000)
        return CodeProviderResult(
            text=result.text or '', provider=resolved.slug, model=resolved.model,
            context_window=resolved.context_window or 131072,
            max_output_tokens=max_output, elapsed_ms=elapsed_ms,
        )


def _call_community(slug: str, model: str, system: str, prompt: str, effort: str, max_tokens: int):
    effort = (effort or 'balanced').strip().lower()
    deep = 'high' if effort in ('deep', 'max', 'high', 'very_high', 'thinking') else 'medium'
    if slug == 'tryingopen':
        from api import tryingopen_proxy
        mapped = 'deep' if effort in ('deep', 'max', 'high', 'very_high', 'thinking') else ('quick' if effort in ('quick', 'low', 'fast') else 'balanced')
        return tryingopen_proxy.simple_chat(
            user_message=prompt, model=model or tryingopen_proxy.DEFAULT_MODEL,
            system_prompt=system, effort=mapped, max_tokens=max_tokens,
        )
    if slug == 'qwen':
        from api.qwen_proxy import call_qwen
        return call_qwen(system, prompt, model=model or 'qwen3.8-max', max_tokens=max_tokens)
    if slug == 'longcat':
        from api import longcat_proxy
        return longcat_proxy.simple_chat(prompt, model=model or 'longcat/LongCat-2.0', system_prompt=system, max_tokens=max_tokens)
    if slug == 'geminiweb':
        from api import geminiweb_proxy
        return geminiweb_proxy.simple_chat(prompt, model=model or 'geminiweb/gemini-flash-lite', system_prompt=system, max_tokens=max_tokens)
    if slug == 'k2think':
        from api import k2think_proxy
        return k2think_proxy.simple_chat(prompt, model=model or 'IFM/K2-Horizon-375B-A23B', system_prompt=system, max_tokens=max_tokens)
    if slug == 'poolside':
        from api import poolside_proxy
        return poolside_proxy.simple_chat(prompt, model=model or 'laguna-s-2.1', system_prompt=system, max_tokens=max_tokens)
    if slug == 'motiftech':
        from api import motiftech_proxy
        return motiftech_proxy.simple_chat(prompt, model=model or 'motif-102b', system_prompt=system, max_tokens=max_tokens, reasoning_effort=deep)
    if slug == 'inception':
        from api import inception_proxy
        return inception_proxy.simple_chat(prompt, model=model or 'mercury-2', system_prompt=system, reasoning_effort=deep)
    if slug == 'qwencloud':
        from api import qwencloud_proxy
        return qwencloud_proxy.simple_chat(prompt, model=model or 'qwen3.8-max', system_prompt=system)
    if slug == 'deepai':
        from api import deepai_proxy
        return deepai_proxy.simple_chat(prompt, model=model or 'standard', system_prompt=system)
    if slug == 'metaai':
        from api import metaai_proxy
        return metaai_proxy.simple_chat(prompt, model=model or 'metaai-instant', system_prompt=system, max_tokens=max_tokens)
    raise CodeProviderError(f'Unsupported provider: {slug}')
