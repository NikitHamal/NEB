"""Lightweight web search for grounding LLM prompts.

Uses DuckDuckGo HTML (no API key) with a Bing fallback.
Designed to be best-effort: never raises, returns [] on failure.
"""
import logging
import os
import re
import time
from html import unescape
from typing import Dict, List
from urllib.parse import quote_plus, unquote

import requests

logger = logging.getLogger(__name__)

_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
_TIMEOUT = 8
_CACHE: Dict[str, tuple] = {}
_CACHE_TTL = 300


def _parse_ddg_html(html: str, num: int = 3) -> List[Dict]:
    out = []
    # DuckDuckGo html has <div class="result ..."> with <a class="result__a"> title + <a class="result__snippet"> snippet
    # Use a single regex that captures title, url, snippet together across the result block
    pattern = re.compile(
        r'<div[^>]+class="[^"]*result[^"]*"[^>]*>.*?<a[^>]+class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?<a[^>]+class="result__snippet"[^>]*>(.*?)</a>',
        re.S | re.I,
    )
    for m in pattern.finditer(html):
        raw_url, raw_title, raw_snip = m.group(1), m.group(2), m.group(3)
        url = unescape(raw_url)
        m_uddg = re.search(r'uddg=([^&"]+)', url)
        if m_uddg:
            try:
                url = unquote(m_uddg.group(1))
            except Exception:
                pass
        if url.startswith("//"):
            url = "https:" + url
        if not url.startswith("http"):
            continue
        title = unescape(re.sub(r'<[^>]+>', '', raw_title).strip())
        snippet = unescape(re.sub(r'<[^>]+>', '', raw_snip).strip())
        if title or snippet:
            out.append({"title": title[:120], "snippet": snippet[:300], "url": url[:300]})
        if len(out) >= num:
            break
    if out:
        return out
    # Fallback: try looser block capture if above failed (e.g. no snippet)
    blocks = re.findall(r'<div[^>]+class="[^"]*result[^"]*"[^>]*>(.*?)</div>\s*</div>', html, re.S | re.I)
    if not blocks:
        blocks = re.findall(r'<tr>.*?</tr>', html, re.S | re.I)
    for b in blocks[: num * 2]:
        m_url = re.search(r'class="result__a"[^>]*href="([^"]+)"', b)
        if not m_url:
            m_url = re.search(r'href="([^"]+)"', b)
        if not m_url:
            continue
        url = unescape(m_url.group(1))
        m_uddg = re.search(r'uddg=([^&"]+)', url)
        if m_uddg:
            try:
                url = unquote(m_uddg.group(1))
            except Exception:
                pass
        if url.startswith("//"):
            url = "https:" + url
        if not url.startswith("http"):
            continue
        m_title = re.search(r'class="result__a"[^>]*>(.*?)</a>', b, re.S)
        title = re.sub(r'<[^>]+>', '', m_title.group(1)).strip() if m_title else url
        title = unescape(title)
        m_snip = re.search(r'class="result__snippet"[^>]*>(.*?)</a>', b, re.S)
        snippet = re.sub(r'<[^>]+>', '', m_snip.group(1)).strip() if m_snip else ""
        snippet = unescape(snippet)
        if title or snippet:
            out.append({"title": title[:120], "snippet": snippet[:300], "url": url[:300]})
        if len(out) >= num:
            break
    return out


def _search_duckduckgo(query: str, num: int = 3) -> List[Dict]:
    for host in ("https://html.duckduckgo.com/html/", "https://lite.duckduckgo.com/lite/"):
        try:
            r = requests.get(
                host,
                params={"q": query},
                headers={"User-Agent": _UA, "Accept": "text/html"},
                timeout=_TIMEOUT,
            )
            if r.status_code != 200:
                logger.debug("DDG status %s for %s", r.status_code, host)
                continue
            html = r.text
            if "anomaly" in html.lower() or "challenge-form" in html:
                logger.debug("DDG anomaly page for %s", host)
                continue
            parsed = _parse_ddg_html(html, num=num)
            # If we got titles but no snippets, still consider it weak — try next host/Bing
            if parsed and any(p.get("snippet") for p in parsed):
                return parsed
            if parsed and len(parsed) >= 2:
                # Even without snippets, return titles/urls — better than nothing
                return parsed
            if parsed:
                return parsed
        except Exception as exc:
            logger.debug("DDG search failed for %s: %s", host, exc)
            continue
    return []


def _search_exa(query: str, num: int = 3) -> List[Dict]:
    key = os.environ.get("EXA_API_KEY", "").strip()
    if not key:
        return []
    try:
        r = requests.post(
            "https://api.exa.ai/search",
            json={"query": query, "numResults": num, "type": "auto", "contents": {"text": {"maxCharacters": 300}}},
            headers={"x-api-key": key, "Content-Type": "application/json"},
            timeout=_TIMEOUT,
        )
        if r.status_code != 200:
            logger.debug("Exa status %s", r.status_code)
            return []
        data = r.json()
        out = []
        for item in (data.get("results") or [])[:num]:
            title = (item.get("title") or "")[:120]
            snippet = (item.get("text") or item.get("snippet") or "")[:300]
            url = (item.get("url") or "")[:300]
            if url and url.startswith("http"):
                out.append({"title": title, "snippet": snippet, "url": url})
        return out
    except Exception as exc:
        logger.debug("Exa search failed: %s", exc)
        return []


def _search_bing(query: str, num: int = 3) -> List[Dict]:
    try:
        r = requests.get(
            "https://www.bing.com/search",
            params={"q": query},
            headers={"User-Agent": _UA, "Accept": "text/html"},
            timeout=_TIMEOUT,
        )
        if r.status_code != 200:
            return []
        html = r.text
        out = []
        # Bing results: <li class="b_algo"><h2><a href="...">title</a></h2><div class="b_caption"><p>snippet...
        blocks = re.findall(r'<li[^>]+class="b_algo"[^>]*>(.*?)</li>', html, re.S | re.I)
        for b in blocks[: num * 2]:
            m_url = re.search(r'<a[^>]+href="([^"]+)"', b)
            if not m_url:
                continue
            url = unescape(m_url.group(1))
            if not url.startswith("http"):
                continue
            m_title = re.search(r'<a[^>]*>(.*?)</a>', b, re.S)
            title = re.sub(r'<[^>]+>', '', m_title.group(1)).strip() if m_title else url
            title = unescape(title)
            m_snip = re.search(r'<p[^>]*>(.*?)</p>', b, re.S)
            snippet = re.sub(r'<[^>]+>', '', m_snip.group(1)).strip() if m_snip else ""
            snippet = unescape(snippet)
            out.append({"title": title[:120], "snippet": snippet[:300], "url": url[:300]})
            if len(out) >= num:
                break
        return out
    except Exception as exc:
        logger.debug("Bing search failed: %s", exc)
        return []


def web_search(query: str, num: int = 3) -> List[Dict]:
    """Best-effort web search — cached, no exceptions. Tries Exa (if key set) → DDG → Bing."""
    query = (query or "").strip()
    if not query:
        return []
    key = f"{query}:{num}"
    now = time.time()
    cached = _CACHE.get(key)
    if cached and now - cached[0] < _CACHE_TTL:
        return cached[1]
    # Truncate very long queries
    if len(query) > 400:
        query = query[:400]
    # 1) Exa (fast, high-quality, if EXA_API_KEY set)
    results = _search_exa(query, num=num)
    if results and any(r.get("snippet") for r in results):
        _CACHE[key] = (now, results)
        return results
    # 2) DuckDuckGo
    results = _search_duckduckgo(query, num=num)
    # If DDG gave titles but no snippets, try Bing for richer snippets
    if results and not any(r.get("snippet") for r in results):
        bing = _search_bing(query, num=num)
        if bing and any(r.get("snippet") for r in bing):
            results = bing
    if not results:
        results = _search_bing(query, num=num)
        if not results and not _search_exa(query, num=1):
            # Final fallback: try DDG lite again with shorter query
            short_q = " ".join(query.split()[:6])
            if short_q != query:
                results = _search_duckduckgo(short_q, num=num)
    _CACHE[key] = (now, results)
    return results


def format_search_context(results: List[Dict]) -> str:
    if not results:
        return ""
    lines = ["Web search results (use for grounding, cite sources):"]
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. {r['title']} — {r['snippet']} ({r['url']})")
    return "\n".join(lines)


def needs_search(prompt: str) -> bool:
    """Heuristic: does this prompt likely need live web data?"""
    if not prompt:
        return False
    low = prompt.lower()
    triggers = [
        "latest", "current", "today", "yesterday", "tomorrow", "news", "weather",
        "price", "stock", "cricket", "football", "match", "score", "result",
        "2025", "2026", "search", "web", "internet", "online", "nepal",
        "neb", "see", "slc", "election", "government", "who won", "what is the",
        "when is", "where is",
    ]
    if any(t in low for t in triggers):
        return True
    # Explicit search request
    if "search" in low or "browse" in low or "look up" in low:
        return True
    # Question that is likely time-sensitive and longer than 40 chars
    if "?" in prompt and len(prompt) > 40:
        return True
    return False
