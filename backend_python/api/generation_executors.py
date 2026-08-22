"""
Per-type generation executors.

Each executor is a function that takes a GenerationJob, runs the AI
generation, and returns a result dict. Errors are caught by the worker
and mark the job as failed.

Executors are intentionally stateless — all context comes from the
job's params JSON and the related space/document.
"""
import json
import logging

from api.models import (
    StudySpace,
    StudySpaceQuiz,
    StudySpaceQuizQuestion,
    StudySpaceFlashcard,
    GenerationJob,
)
from api.utils import now_ms, uuid_str
from api.qwen_utils.client import QwenClient
from api.qwen_utils.parsing import (
    clean_ai_markdown, normalize_formulas, parse_json_response,
    parse_json_object_response, dedupe_questions, dedupe_flashcards,
)
from api.qwen_utils.prompts import (
    summary_system_prompt, quiz_system_prompt, flashcard_system_prompt,
    MINDMAP_SYSTEM_PROMPT,
    summary_outline_prompt, summary_full_prompt,
    MINDMAP_OUTLINE_PROMPT, MINDMAP_FULL_PROMPT,
    quiz_outline_prompt, quiz_full_prompt,
    flashcard_outline_prompt, flashcard_full_prompt,
    exclusion_block,
)
from api.generation import mark_progress, mark_completed, mark_failed

logger = logging.getLogger(__name__)

MAX_TEXT_CHARS = 50000


# ── Shared helpers ──────────────────────────────────────────────────────────

def _get_space_texts(space):
    """Collect parsed text from all documents in a space."""
    docs = space.documents.filter(
        status='ready',
        parse_status='ready',
    ).exclude(parsed_text='').order_by('created_at')
    texts = []
    for d in docs:
        content = d.parsed_text or ''
        if content.strip():
            texts.append({'title': d.title or d.file_name or 'Document', 'content': content})
    return texts


def _combine_texts(texts):
    """Combine texts into a single string for the AI prompt."""
    combined = '\n\n'.join(f"=== {t['title']} ===\n{t['content']}" for t in texts)
    return combined[:MAX_TEXT_CHARS]


def _space_quiz_exclusions(space):
    """Return list of existing question texts for dedup."""
    questions = StudySpaceQuizQuestion.objects.filter(
        quiz__space=space
    ).values_list('question_text', flat=True)
    return list(questions)


def _space_flashcard_exclusions(space):
    """Return list of existing flashcard fronts for dedup."""
    cards = StudySpaceFlashcard.objects.filter(
        space=space
    ).values_list('front', flat=True)
    return list(cards)


def _qwen():
    return QwenClient()


FALLBACK_MAX_TOKENS = 4000


def _fallback_generate(system_prompt, user_message):
    """Route a generation through the shared Neby provider chain
    (enabled BotConfig + its fallback providers) when the Qwen web
    proxy is unavailable. Returns text or None."""
    try:
        from api.models import BotConfig
        from api.neby import call_ai_api
        cfg = BotConfig.objects.filter(enabled=True).first()
        if not cfg:
            return None
        cfg.response_max_length = FALLBACK_MAX_TOKENS
        return call_ai_api(system_prompt, user_message, cfg)
    except Exception as exc:
        logger.warning('generation fallback failed: %s', exc)
        return None


def _generate_two_turn(outline_prompt, full_prompt, combined, system_prompt=None, exclusion_text=None):
    """Qwen two-turn generation with provider-chain fallback.

    Returns (text, err) — same contract as QwenClient.two_turn_generation.
    """
    try:
        result, err = _generate_two_turn(
            outline_prompt, full_prompt, combined,
            system_prompt=system_prompt,
        )
        if not err and result:
            return result, None
        last_err = err or 'empty response'
    except Exception as exc:
        logger.warning('qwen generation errored: %s', exc)
        last_err = str(exc)[:500]

    fused = f"{outline_prompt}\n\n{full_prompt}\n\n=== SOURCE MATERIAL ===\n{combined}"
    text = _fallback_generate(system_prompt, fused[:MAX_TEXT_CHARS + 4000])
    if text:
        logger.info('generation: primary qwen unavailable (%s), used fallback provider', last_err)
        return text, None
    return None, f'All AI providers failed (last error: {last_err})'


def _normalize_mindmap(mindmap, space):
    """Normalize a mindmap dict, injecting space title if needed."""
    if not mindmap:
        return {}
    if not mindmap.get('title'):
        mindmap['title'] = space.title or 'Study Space'
    return mindmap


# ── Executors ────────────────────────────────────────────────────────────────

def execute_summary(job):
    """Generate a linked summary across all space documents."""
    space = StudySpace.objects.get(pk=job.space_id)
    params = json.loads(job.params) if job.params else {}
    mode = params.get('mode', 'compact')

    mark_progress(job, 20, 'Reading documents...')

    texts = _get_space_texts(space)
    if not texts:
        mark_failed(job, 'No readable documents in this space')
        return

    combined = _combine_texts(texts)
    mark_progress(job, 30, 'Generating outline...')

    result, err = _generate_two_turn(
        summary_outline_prompt(mode), summary_full_prompt(mode), combined,
        system_prompt=summary_system_prompt(mode),
    )
    if err:
        mark_failed(job, err)
        return

    mark_progress(job, 80, 'Finalizing...')

    summary = normalize_formulas(clean_ai_markdown(result))
    if mode == 'detailed':
        space.link_summary_detailed = summary
    else:
        space.link_summary_compact = summary
    space.link_summary_generated_at = now_ms()
    space.updated_at = now_ms()
    space.save(update_fields=['link_summary_compact', 'link_summary_detailed', 'link_summary_generated_at', 'updated_at'])

    mark_completed(job, {
        'mode': mode,
        'summary': summary,
        'summaryCompact': space.link_summary_compact,
        'summaryDetailed': space.link_summary_detailed,
    })


def execute_mindmap(job):
    """Generate a linked mindmap across all space documents."""
    space = StudySpace.objects.get(pk=job.space_id)

    mark_progress(job, 20, 'Reading documents...')

    texts = _get_space_texts(space)
    if not texts:
        mark_failed(job, 'No readable documents in this space')
        return

    combined = _combine_texts(texts)
    mark_progress(job, 30, 'Generating mindmap outline...')

    result, err = _generate_two_turn(
        MINDMAP_OUTLINE_PROMPT, MINDMAP_FULL_PROMPT, combined,
        system_prompt=MINDMAP_SYSTEM_PROMPT,
    )
    if err:
        mark_failed(job, err)
        return

    mark_progress(job, 70, 'Parsing mindmap...')

    mindmap = parse_json_object_response(result)
    if not mindmap:
        mark_failed(job, 'Could not parse mindmap from AI response')
        return

    normalized = _normalize_mindmap(mindmap, space)
    space.link_mindmap_json = json.dumps(normalized, ensure_ascii=False)
    space.link_mindmap_generated_at = now_ms()
    space.updated_at = now_ms()
    space.save(update_fields=['link_mindmap_json', 'link_mindmap_generated_at', 'updated_at'])

    mark_completed(job, {'mindmap': normalized})


def execute_quiz(job):
    """Generate a quiz across all space documents."""
    from django.db import transaction

    space = StudySpace.objects.get(pk=job.space_id)
    params = json.loads(job.params) if job.params else {}
    count = params.get('count', 5)
    count = max(3, min(20, int(count)))

    mark_progress(job, 20, 'Reading documents...')

    texts = _get_space_texts(space)
    if not texts:
        mark_failed(job, 'No readable documents in this space')
        return

    combined = _combine_texts(texts)
    mark_progress(job, 30, 'Generating quiz outline...')

    existing = _space_quiz_exclusions(space)
    exclusion_text = exclusion_block('Previously asked questions (do not repeat)', existing)

    outline_prompt = (
        f"Outline {count} multiple-choice quiz questions from these documents. "
        "List the topics and key concepts to test. "
        "Do not write the actual questions yet."
    )
    full_prompt = (
        f"Create {count} multiple-choice quiz questions from these documents "
        "based on the outline below. Each question must have exactly 4 options (A-D) "
        "and one correct answer. Return only a JSON array.\n\n"
        + exclusion_text
    )

    result, err = _generate_two_turn(
        outline_prompt, full_prompt, combined,
        system_prompt=quiz_system_prompt(count),
        exclusion_text=exclusion_text,
    )
    if err:
        mark_failed(job, err)
        return

    mark_progress(job, 70, 'Parsing questions...')

    items = parse_json_response(result)
    existing_normalized = [q.lower() for q in existing]
    items = dedupe_questions(items, existing_normalized)
    items = items[:count]

    if not items:
        mark_failed(job, 'Could not generate quiz questions')
        return

    mark_progress(job, 85, 'Saving quiz...')

    now = now_ms()
    with transaction.atomic():
        quiz = StudySpaceQuiz.objects.create(
            id=uuid_str(),
            space=space,
            user_id=job.user_id,
            title=f"Quiz: {space.title or 'Study Space'}",
            question_count=len(items),
            created_at=now,
        )
        question_rows = []
        for i, item in enumerate(items, 1):
            options = item.get('options', [])
            question_rows.append(StudySpaceQuizQuestion(
                id=uuid_str(),
                quiz=quiz,
                question_number=i,
                question_text=item.get('question', ''),
                option_a=options[0] if len(options) > 0 else '',
                option_b=options[1] if len(options) > 1 else '',
                option_c=options[2] if len(options) > 2 else '',
                option_d=options[3] if len(options) > 3 else '',
                correct_answer=(item.get('correct_answer') or item.get('correctAnswer') or item.get('correct') or 'A').upper()[:1],
                explanation=item.get('explanation', ''),
            ))
        StudySpaceQuizQuestion.objects.bulk_create(question_rows)
        space.updated_at = now
        space.save(update_fields=['updated_at'])

    mark_completed(job, {
        'quiz': {
            'id': quiz.id,
            'title': quiz.title,
            'questionCount': quiz.question_count,
            'createdAt': quiz.created_at,
            'questions': [
                {
                    'id': q.id,
                    'questionNumber': q.question_number,
                    'questionText': q.question_text,
                    'optionA': q.option_a,
                    'optionB': q.option_b,
                    'optionC': q.option_c,
                    'optionD': q.option_d,
                }
                for q in question_rows
            ],
        },
    })


def execute_flashcard(job):
    """Generate flashcards across all space documents."""
    from django.db import transaction

    space = StudySpace.objects.get(pk=job.space_id)
    params = json.loads(job.params) if job.params else {}
    count = params.get('count', 8)
    count = max(3, min(30, int(count)))

    mark_progress(job, 20, 'Reading documents...')

    texts = _get_space_texts(space)
    if not texts:
        mark_failed(job, 'No readable documents in this space')
        return

    combined = _combine_texts(texts)
    mark_progress(job, 30, 'Generating flashcard outline...')

    existing = _space_flashcard_exclusions(space)
    exclusion_text = exclusion_block('Previously generated flashcards (do not repeat)', existing)

    outline_prompt = (
        f"Outline {count} flashcard topics from these documents. "
        "List the key concepts, terms, and definitions to cover. "
        "Do not write the actual flashcards yet."
    )
    full_prompt = (
        f"Create {count} flashcards from these documents based on the outline below. "
        "Each flashcard must have a 'front' (question/term) and 'back' (answer/definition). "
        "Return only a JSON array.\n\n"
        + exclusion_text
    )

    result, err = _generate_two_turn(
        outline_prompt, full_prompt, combined,
        system_prompt=flashcard_system_prompt(count),
        exclusion_text=exclusion_text,
    )
    if err:
        mark_failed(job, err)
        return

    mark_progress(job, 70, 'Parsing flashcards...')

    items = parse_json_response(result)
    existing_normalized = [f.lower() for f in existing]
    items = dedupe_flashcards(items, existing_normalized)
    items = items[:count]

    if not items:
        mark_failed(job, 'Could not generate flashcards')
        return

    mark_progress(job, 85, 'Saving flashcards...')

    now = now_ms()
    card_rows = [
        StudySpaceFlashcard(
            id=uuid_str(),
            space=space,
            user_id=job.user_id,
            front=item.get('front', ''),
            back=item.get('back', ''),
            card_number=i,
            created_at=now,
        )
        for i, item in enumerate(items, 1)
    ]
    with transaction.atomic():
        StudySpaceFlashcard.objects.bulk_create(card_rows)
        space.updated_at = now
        space.save(update_fields=['updated_at'])

    cards = [
        {
            'id': fc.id,
            'front': fc.front,
            'back': fc.back,
            'cardNumber': fc.card_number,
        }
        for fc in card_rows
    ]

    mark_completed(job, {'flashcards': cards})


# ── Registry ────────────────────────────────────────────────────────────────

EXECUTORS = {
    GenerationJob.TYPE_SUMMARY: execute_summary,
    GenerationJob.TYPE_MINDMAP: execute_mindmap,
    GenerationJob.TYPE_QUIZ: execute_quiz,
    GenerationJob.TYPE_FLASHCARD: execute_flashcard,
}