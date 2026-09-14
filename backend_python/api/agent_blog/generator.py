"""Generate complete markdown blog posts using Neby's AI reasoning pipeline."""
import json
import logging
import re
from typing import Dict, Optional

from api.models import BotConfig
from api.neby import call_ai_api

logger = logging.getLogger(__name__)

_JSON_BLOCK_RE = re.compile(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```')
_JSON_OBJECT_RE = re.compile(r'(\{[\s\S]*\})')


def _clean_json_output(raw_text: str) -> Optional[Dict]:
    """Robustly parse JSON object from LLM response text."""
    if not raw_text:
        return None
    raw_text = raw_text.strip()

    # Match fenced ```json ... ```
    m = _JSON_BLOCK_RE.search(raw_text)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass

    # Match standalone { ... }
    m = _JSON_OBJECT_RE.search(raw_text)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass

    return None


def generate_blog_post(
    topic_description: str,
    context_type: str = "update",
    additional_notes: str = "",
    bot_config: Optional[BotConfig] = None,
) -> Optional[Dict[str, str]]:
    """Generate a high quality blog post in Markdown format.

    Returns dict with keys:
        - title: str
        - slug: str
        - summary: str (under 300 chars)
        - content: str (rich markdown body)
        - category: str (update, notice, event, general)
        - tags: str (comma-separated)
        - cover_image_url: str (optional)
    """
    system_prompt = (
        "You are Neby, the friendly, smart, and enthusiastic AI peer for NEBians "
        "(Nepal's learning community platform for students, teachers, and learners). "
        "Your task is to write a warm, engaging, and highly informative blog article or feature update.\n\n"
        "Style & Formatting Guidelines:\n"
        "- Write from Neby's perspective (friendly, inspiring, student-focused, clear).\n"
        "- Use rich Markdown formatting with clear H2 (##) and H3 (###) headers, bullet points, "
        "practical tips, and a conclusion.\n"
        "- Explain concepts clearly in accessible English with authentic touch for Nepali learners.\n"
        "- Do NOT sound like a generic corporate press release — be genuine and excited to help students learn better.\n"
        "- Output strictly valid JSON matching the requested schema."
    )

    user_prompt = f"""Write a full blog post for NEBians about the following topic / updates:

Topic & Highlights:
{topic_description}

Context Type: {context_type}
{f"Additional Notes: {additional_notes}" if additional_notes else ""}

Respond ONLY with a valid JSON object in this exact format:
{{
  "title": "An exciting, engaging title for the article",
  "slug": "url-friendly-slug-with-hyphens",
  "summary": "A punchy 1-2 sentence overview for the blog card (under 300 characters)",
  "category": "{context_type if context_type in ['update', 'notice', 'event', 'general'] else 'update'}",
  "tags": "NEBians, Updates, Study Tips, RelevantTag1, RelevantTag2",
  "content": "Full markdown body of the post. Use ## headings, bullet points, step-by-step tips, and an encouraging closing message from Neby."
}}
"""

    try:
        raw_response = call_ai_api(
            system_prompt=system_prompt,
            user_message=user_prompt,
            config=bot_config,
        )

        parsed = _clean_json_output(raw_response)
        if parsed and parsed.get('title') and parsed.get('content'):
            return {
                'title': str(parsed.get('title', '')).strip(),
                'slug': str(parsed.get('slug', '')).strip().lower().replace(' ', '-'),
                'summary': str(parsed.get('summary', ''))[:490].strip(),
                'content': str(parsed.get('content', '')).strip(),
                'category': str(parsed.get('category', 'update')).strip().lower(),
                'tags': str(parsed.get('tags', 'NEBians, Updates')).strip(),
                'cover_image_url': str(parsed.get('cover_image_url', '')).strip(),
            }
        
        # Fallback if JSON parsing failed but text exists
        if raw_response and len(raw_response.strip()) > 100:
            lines = raw_response.strip().split('\n')
            title = lines[0].replace('#', '').strip() or "Exciting New Updates on NEBians"
            slug = re.sub(r'[^a-zA-Z0-9]+', '-', title).strip('-').lower()
            return {
                'title': title,
                'slug': slug[:80],
                'summary': (lines[1] if len(lines) > 1 else title)[:300],
                'content': raw_response.strip(),
                'category': context_type if context_type in ['update', 'notice', 'event', 'general'] else 'update',
                'tags': 'NEBians, Updates',
                'cover_image_url': '',
            }
        return None
    except Exception as e:
        logger.error('generate_blog_post failed: %s', e)
        return None
