"""Study Lab views — upload documents, generate summaries, quizzes, flashcards via Qwen AI."""
import json
import logging
import os

from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST

from .view_helpers import *  # noqa: F401,F403
from api.models import (
    StudyDocument, StudyQuiz, StudyQuizQuestion, StudyQuizAttempt,
    StudyFlashcard, StudyFlashcardReview,
)
from api.utils import now_ms, uuid_str
from api import qwen_proxy
from api.qwen_utils.file_upload import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, upload_file_from_bytes

logger = logging.getLogger(__name__)

MAX_TEXT_CHARS = 50000  # Truncate extracted document text to avoid oversized prompts

# ── Qwen model helper ──────────────────────────────────────────────────

_QWEN_MODEL_CACHE = None


def _qwen_model():
    """Return the default Qwen model ID for Study Lab generations.

    Uses the live model catalog (cached 5 min via ``get_default_model``)
    to pick the newest vision+document-capable model.
    Falls back to ``qwen3.7-plus``.

    Uses a process-level cache to avoid hitting Redis on every call.
    """
    global _QWEN_MODEL_CACHE
    if _QWEN_MODEL_CACHE:
        return _QWEN_MODEL_CACHE
    try:
        from api.qwen_utils.models import get_default_model
        model = get_default_model()
        _QWEN_MODEL_CACHE = model
        return model
    except Exception:
        return 'qwen3.7-plus'


# ── Qwen prompt templates ──────────────────────────────────────────────

_SUMMARY_SYSTEM_PROMPT = (
    "You are an expert study assistant for Nepali students following the NEB curriculum. "
    "Given the content of a study document, produce a clear, well-structured summary. "
    "Use markdown formatting with headings (##), bullet points, and bold key terms. "
    "Write in English unless the source is in Nepali. "
    "Keep the summary concise but thorough — aim for 20-30% of the original length."
)

_QUIZ_SYSTEM_PROMPT = (
    "You are an expert quiz generator for Nepali students following the NEB curriculum. "
    "Given the content of a study document, generate multiple-choice questions (MCQs). "
    "You MUST respond with ONLY a valid JSON array, no other text. Each element must have: "
    '"question" (string), "options" (array of 4 strings: A, B, C, D), '
    '"correct" (string: "A", "B", "C", or "D"), "explanation" (string). '
    "Generate exactly {count} questions. Make them exam-style and progressively harder. "
    "Do NOT wrap the JSON in markdown code fences."
)

_FLASHCARD_SYSTEM_PROMPT = (
    "You are an expert flashcard creator for Nepali students following the NEB curriculum. "
    "Given the content of a study document, create study flashcards. "
    "You MUST respond with ONLY a valid JSON array, no other text. Each element must have: "
    '"front" (string: the question or term), "back" (string: the answer or definition). '
    "Generate exactly {count} flashcards. Cover the most important concepts. "
    "Do NOT wrap the JSON in markdown code fences."
)


# ── Page views ─────────────────────────────────────────────────────────

def study_lab(request):
    """Study Lab landing page."""
    user_id = _get_user_id(request)
    if not user_id:
        return redirect('web:login')
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect('web:login')

    documents = StudyDocument.objects.filter(user=user).order_by('-updated_at')[:50]
    doc_list = []
    for d in documents:
        doc_list.append({
            'id': d.id,
            'title': d.title or d.file_name or 'Untitled',
            'fileName': d.file_name,
            'fileSize': d.file_size,
            'status': d.status,
            'summaryGenerated': bool(d.summary),
            'quizCount': d.quizzes.count(),
            'flashcardCount': d.flashcards.count(),
            'createdAt': d.created_at,
            'updatedAt': d.updated_at,
        })

    ctx = _ctx(request, documents=doc_list, page='study_lab')
    return render(request, 'web/study_lab.html', ctx)


# ── Document upload ────────────────────────────────────────────────────

def ajax_study_upload(request):
    """Upload a PDF/image/text document for study. Returns document metadata."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    f = request.FILES.get('file')
    if not f:
        return JsonResponse({'error': 'No file provided'}, status=400)

    ext = os.path.splitext(f.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return JsonResponse({'error': f'Unsupported file type: {ext}'}, status=400)
    if f.size > MAX_FILE_SIZE:
        return JsonResponse({'error': f'File too large (max {MAX_FILE_SIZE // (1024*1024)}MB)'}, status=400)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile

    file_data = f.read()
    file_name = f.name
    mime_type = f.content_type or 'application/octet-stream'

    # Save file to media storage
    storage_path = f'study_lab/{user_id}/{uuid_str()}{ext}'
    saved_path = default_storage.save(storage_path, ContentFile(file_data))
    file_url = default_storage.url(saved_path)

    now = now_ms()
    doc = StudyDocument.objects.create(
        id=uuid_str(),
        user=user,
        title=os.path.splitext(file_name)[0],
        file_url=file_url,
        file_name=file_name,
        file_size=f.size,
        mime_type=mime_type,
        status='ready',
        created_at=now,
        updated_at=now,
    )

    return JsonResponse({
        'document': {
            'id': doc.id,
            'title': doc.title,
            'fileName': doc.file_name,
            'fileSize': doc.file_size,
            'status': doc.status,
            'summaryGenerated': False,
            'quizCount': 0,
            'flashcardCount': 0,
            'createdAt': doc.created_at,
            'updatedAt': doc.updated_at,
        }
    }, status=201)


# ── Document list/detail ───────────────────────────────────────────────

def ajax_study_documents(request):
    """List user's study documents."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    documents = StudyDocument.objects.filter(user=user).order_by('-updated_at')[:50]
    doc_list = []
    for d in documents:
        doc_list.append({
            'id': d.id,
            'title': d.title or d.file_name or 'Untitled',
            'fileName': d.file_name,
            'fileSize': d.file_size,
            'status': d.status,
            'summaryGenerated': bool(d.summary),
            'quizCount': d.quizzes.count(),
            'flashcardCount': d.flashcards.count(),
            'createdAt': d.created_at,
            'updatedAt': d.updated_at,
        })

    return JsonResponse({'documents': doc_list})


def ajax_study_document_detail(request, doc_id):
    """Get document detail with summary, quizzes, flashcards."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        doc = StudyDocument.objects.get(pk=doc_id)
    except StudyDocument.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)

    if doc.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    quizzes = doc.quizzes.all().order_by('-created_at')
    flashcards = doc.flashcards.all().order_by('card_number')

    return JsonResponse({
        'document': {
            'id': doc.id,
            'title': doc.title or doc.file_name or 'Untitled',
            'fileName': doc.file_name,
            'fileSize': doc.file_size,
            'mimeType': doc.mime_type,
            'status': doc.status,
            'summary': doc.summary,
            'summaryGenerated': bool(doc.summary),
            'createdAt': doc.created_at,
            'updatedAt': doc.updated_at,
        },
        'quizzes': [
            {
                'id': q.id,
                'title': q.title,
                'questionCount': q.question_count,
                'attemptCount': q.attempts.filter(user_id=user_id).count(),
                'bestScore': max(
                    (a.score for a in q.attempts.filter(user_id=user_id)),
                    default=0,
                ),
                'createdAt': q.created_at,
            }
            for q in quizzes
        ],
        'flashcards': [
            {
                'id': fc.id,
                'front': fc.front,
                'back': fc.back,
                'cardNumber': fc.card_number,
                'confidence': (
                    fc.reviews.filter(user_id=user_id).first().confidence
                    if fc.reviews.filter(user_id=user_id).exists()
                    else 'new'
                ),
            }
            for fc in flashcards
        ],
        'totalFlashcards': flashcards.count(),
    })


def ajax_study_delete_document(request, doc_id):
    """Delete a study document and all related quizzes/flashcards."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        doc = StudyDocument.objects.get(pk=doc_id)
    except StudyDocument.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)

    if doc.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    doc.delete()
    return JsonResponse({'success': True})


# ── Generate summary ──────────────────────────────────────────────────

def ajax_study_generate_summary(request, doc_id):
    """Generate a summary for a document using Qwen."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        doc = StudyDocument.objects.get(pk=doc_id)
    except StudyDocument.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)

    if doc.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    prepared = _prepare_doc_for_qwen(doc)
    if not prepared:
        logger.error("DEBUG: 502 reason: Could not read document content")
        return JsonResponse({'error': 'Could not read document content'}, status=502)

    qwen_session, _ = qwen_proxy._get_session()
    midtoken = qwen_proxy.get_midtoken(qwen_session)
    if midtoken:
        qwen_session.headers['bx-umidtoken'] = midtoken
        qwen_session.headers['bx-v'] = '2.5.31'

    chat_id = qwen_proxy.create_chat(qwen_session, model=_qwen_model())
    if not chat_id:
        logger.error("DEBUG: 502 reason: Could not start AI session")
        return JsonResponse({'error': 'Could not start AI session — try again'}, status=502)

    if prepared.get('has_file') or prepared.get('is_image'):
        if prepared.get('is_image'):
            prompt = "Summarize the content shown in this image thoroughly. Use clear headings, bullet points, and bold key terms."
        else:
            prompt = "Summarize this document thoroughly. Use clear headings, bullet points, and bold key terms."
        result = qwen_proxy.send_message(
            qwen_session, chat_id, prompt, model=_qwen_model(),
            parent_id=None, uploaded_files=prepared['uploaded_files'],
        )
    else:
        prompt = (
            "Summarize this document thoroughly. Use clear headings, bullet points, and bold key terms.\n\n"
            "--- DOCUMENT CONTENT ---\n" + prepared['text_content'] + "\n--- END ---"
        )
        result = qwen_proxy.send_message(
            qwen_session, chat_id, prompt, model=_qwen_model(),
            parent_id=None,
        )

    if not result:
        logger.error("DEBUG: 502 reason: AI returned an empty response")
        return JsonResponse({'error': 'AI returned an empty response'}, status=502)

    doc.summary = result
    doc.summary_generated_at = now_ms()
    doc.updated_at = now_ms()
    doc.save(update_fields=['summary', 'summary_generated_at', 'updated_at'])

    return JsonResponse({'summary': result})


# ── Generate quiz ──────────────────────────────────────────────────────

def ajax_study_generate_quiz(request, doc_id):
    """Generate an MCQ quiz from a document using Qwen."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        doc = StudyDocument.objects.get(pk=doc_id)
    except StudyDocument.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)

    if doc.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    try:
        body = json.loads(request.body) if request.body else {}
    except ValueError:
        body = {}

    question_count = min(max(int(body.get('count', 10)), 3), 30)

    prepared = _prepare_doc_for_qwen(doc)
    if not prepared:
        return JsonResponse({'error': 'Could not read document content'}, status=502)

    qwen_session, _ = qwen_proxy._get_session()
    midtoken = qwen_proxy.get_midtoken(qwen_session)
    if midtoken:
        qwen_session.headers['bx-umidtoken'] = midtoken
        qwen_session.headers['bx-v'] = '2.5.31'

    chat_id = qwen_proxy.create_chat(qwen_session, model=_qwen_model())
    if not chat_id:
        return JsonResponse({'error': 'Could not start AI session — try again'}, status=502)

    if prepared.get('has_file') or prepared.get('is_image'):
        if prepared.get('is_image'):
            prompt = f"Generate {question_count} MCQ questions based on the content shown in this image."
        else:
            prompt = f"Generate {question_count} MCQ questions from this document."
        result = qwen_proxy.send_message(
            qwen_session, chat_id, prompt, model=_qwen_model(),
            parent_id=None, uploaded_files=prepared['uploaded_files'],
            system_prompt=_QUIZ_SYSTEM_PROMPT.format(count=question_count),
        )
    else:
        prompt = (
            f"Generate {question_count} MCQ questions from this document.\n\n"
            "--- DOCUMENT CONTENT ---\n" + prepared['text_content'] + "\n--- END ---"
        )
        result = qwen_proxy.send_message(
            qwen_session, chat_id, prompt, model=_qwen_model(),
            parent_id=None,
            system_prompt=_QUIZ_SYSTEM_PROMPT.format(count=question_count),
        )

    if not result:
        return JsonResponse({'error': 'AI returned an empty response'}, status=502)

    questions = _parse_json_response(result)
    if not questions:
        return JsonResponse({'error': 'Failed to parse quiz questions from AI response'}, status=502)

    now = now_ms()
    quiz = StudyQuiz.objects.create(
        id=uuid_str(),
        document=doc,
        user_id=user_id,
        title=f"Quiz: {doc.title or doc.file_name or 'Untitled'}",
        question_count=len(questions),
        created_at=now,
    )

    for i, q in enumerate(questions):
        options = q.get('options', [])
        StudyQuizQuestion.objects.create(
            id=uuid_str(),
            quiz=quiz,
            question_number=i + 1,
            question_text=q.get('question', ''),
            option_a=options[0] if len(options) > 0 else '',
            option_b=options[1] if len(options) > 1 else '',
            option_c=options[2] if len(options) > 2 else '',
            option_d=options[3] if len(options) > 3 else '',
            correct_answer=(q.get('correct', 'A') or 'A').upper()[:1],
            explanation=q.get('explanation', ''),
        )

    doc.updated_at = now
    doc.save(update_fields=['updated_at'])

    return JsonResponse({
        'quiz': {
            'id': quiz.id,
            'title': quiz.title,
            'questionCount': quiz.question_count,
            'questions': [
                {
                    'id': sq.id,
                    'number': sq.question_number,
                    'question': sq.question_text,
                    'optionA': sq.option_a,
                    'optionB': sq.option_b,
                    'optionC': sq.option_c,
                    'optionD': sq.option_d,
                }
                for sq in quiz.questions.all().order_by('question_number')
            ],
        }
    }, status=201)


# ── Generate flashcards ───────────────────────────────────────────────

def ajax_study_generate_flashcards(request, doc_id):
    """Generate flashcards from a document using Qwen."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        doc = StudyDocument.objects.get(pk=doc_id)
    except StudyDocument.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)

    if doc.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    try:
        body = json.loads(request.body) if request.body else {}
    except ValueError:
        body = {}

    card_count = min(max(int(body.get('count', 15)), 5), 50)

    prepared = _prepare_doc_for_qwen(doc)
    if not prepared:
        return JsonResponse({'error': 'Could not read document content'}, status=502)

    qwen_session, _ = qwen_proxy._get_session()
    midtoken = qwen_proxy.get_midtoken(qwen_session)
    if midtoken:
        qwen_session.headers['bx-umidtoken'] = midtoken
        qwen_session.headers['bx-v'] = '2.5.31'

    chat_id = qwen_proxy.create_chat(qwen_session, model=_qwen_model())
    if not chat_id:
        return JsonResponse({'error': 'Could not start AI session — try again'}, status=502)

    if prepared.get('has_file') or prepared.get('is_image'):
        if prepared.get('is_image'):
            prompt = f"Create {card_count} flashcards based on the content shown in this image."
        else:
            prompt = f"Create {card_count} flashcards from this document."
        result = qwen_proxy.send_message(
            qwen_session, chat_id, prompt, model=_qwen_model(),
            parent_id=None, uploaded_files=prepared['uploaded_files'],
            system_prompt=_FLASHCARD_SYSTEM_PROMPT.format(count=card_count),
        )
    else:
        prompt = (
            f"Create {card_count} flashcards from this document.\n\n"
            "--- DOCUMENT CONTENT ---\n" + prepared['text_content'] + "\n--- END ---"
        )
        result = qwen_proxy.send_message(
            qwen_session, chat_id, prompt, model=_qwen_model(),
            parent_id=None,
            system_prompt=_FLASHCARD_SYSTEM_PROMPT.format(count=card_count),
        )

    if not result:
        return JsonResponse({'error': 'AI returned an empty response'}, status=502)

    cards = _parse_json_response(result)
    if not cards:
        return JsonResponse({'error': 'Failed to parse flashcards from AI response'}, status=502)

    now = now_ms()
    flashcard_objs = []
    for i, c in enumerate(cards):
        fc = StudyFlashcard.objects.create(
            id=uuid_str(),
            document=doc,
            user_id=user_id,
            front=c.get('front', ''),
            back=c.get('back', ''),
            card_number=i + 1,
            created_at=now,
        )
        flashcard_objs.append(fc)

    doc.updated_at = now
    doc.save(update_fields=['updated_at'])

    return JsonResponse({
        'flashcards': [
            {
                'id': fc.id,
                'front': fc.front,
                'back': fc.back,
                'cardNumber': fc.card_number,
                'confidence': 'new',
            }
            for fc in flashcard_objs
        ],
        'totalFlashcards': len(flashcard_objs),
    }, status=201)


# ── Submit quiz attempt ────────────────────────────────────────────────

def ajax_study_quiz_submit(request, quiz_id):
    """Submit answers for a quiz and get score + XP."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        quiz = StudyQuiz.objects.get(pk=quiz_id)
    except StudyQuiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)

    try:
        body = json.loads(request.body)
    except ValueError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    answers = body.get('answers', {})
    if not answers:
        return JsonResponse({'error': 'No answers provided'}, status=400)

    questions = list(quiz.questions.all().order_by('question_number'))
    score = 0
    results = {}

    for q in questions:
        user_answer = answers.get(str(q.question_number), '').upper()
        is_correct = user_answer == q.correct_answer
        if is_correct:
            score += 1
        results[str(q.question_number)] = {
            'userAnswer': user_answer,
            'correctAnswer': q.correct_answer,
            'isCorrect': is_correct,
            'explanation': q.explanation,
        }

    xp_earned = score * 10  # 10 XP per correct answer

    now = now_ms()
    attempt = StudyQuizAttempt.objects.create(
        id=uuid_str(),
        quiz=quiz,
        user_id=user_id,
        score=score,
        total_questions=len(questions),
        answers=json.dumps(answers),
        xp_earned=xp_earned,
        completed_at=now,
        created_at=now,
    )

    # Update user XP (contribution score)
    User.objects.filter(pk=user_id).update(contribution_score=F('contribution_score') + xp_earned)

    return JsonResponse({
        'attempt': {
            'id': attempt.id,
            'score': attempt.score,
            'totalQuestions': attempt.total_questions,
            'xpEarned': attempt.xp_earned,
            'results': results,
        }
    })


# ── Flashcard review ───────────────────────────────────────────────────

def ajax_study_flashcard_review(request, card_id):
    """Mark a flashcard's confidence level."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        card = StudyFlashcard.objects.get(pk=card_id)
    except StudyFlashcard.DoesNotExist:
        return JsonResponse({'error': 'Flashcard not found'}, status=404)

    try:
        body = json.loads(request.body)
    except ValueError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    confidence = body.get('confidence', 'medium')
    if confidence not in ('easy', 'medium', 'hard'):
        return JsonResponse({'error': 'Invalid confidence level'}, status=400)

    now = now_ms()
    intervals = {'easy': 7 * 86400000, 'medium': 2 * 86400000, 'hard': 30 * 60000}

    review, created = StudyFlashcardReview.objects.update_or_create(
        flashcard=card,
        user_id=user_id,
        defaults={
            'confidence': confidence,
            'review_count': 1,
            'last_reviewed_at': now,
            'next_review_at': now + intervals.get(confidence, 2 * 86400000),
        },
    )
    if not created:
        StudyFlashcardReview.objects.filter(pk=review.pk).update(review_count=F('review_count') + 1)

    return JsonResponse({
        'flashcardId': card.id,
        'confidence': confidence,
        'reviewCount': review.review_count if created else review.review_count,
        'nextReviewAt': review.next_review_at,
    })


# ── Get quiz detail ────────────────────────────────────────────────────

def ajax_study_quiz_detail(request, quiz_id):
    """Get quiz questions (without correct answers — client fetches after submit)."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        quiz = StudyQuiz.objects.get(pk=quiz_id)
    except StudyQuiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)

    if quiz.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    previous_attempts = quiz.attempts.filter(user_id=user_id).order_by('-completed_at')
    questions = quiz.questions.all().order_by('question_number')

    return JsonResponse({
        'quiz': {
            'id': quiz.id,
            'title': quiz.title,
            'questionCount': quiz.question_count,
            'createdAt': quiz.created_at,
            'attemptCount': previous_attempts.count(),
            'bestScore': max((a.score for a in previous_attempts), default=0),
            'questions': [
                {
                    'id': q.id,
                    'number': q.question_number,
                    'question': q.question_text,
                    'optionA': q.option_a,
                    'optionB': q.option_b,
                    'optionC': q.option_c,
                    'optionD': q.option_d,
                }
                for q in questions
            ],
        }
    })


# ── Helpers ────────────────────────────────────────────────────────────

def _prepare_doc_for_qwen(doc):
    """Read document and return context for Qwen prompt.
    
    Returns dict with:
      'is_image' — True if file was uploaded to Qwen OSS
      'uploaded_files' — list of file_obj dicts (for images)
      'text_content' — extracted text (for documents)
    Returns None on failure.
    """
    if not doc.file_url:
        return None

    try:
        from django.core.files.storage import default_storage
        file_path = doc.file_url
        if file_path.startswith('/media/'):
            file_path = file_path[len('/media/'):]
        elif file_path.startswith('/'):
            file_path = file_path.lstrip('/')
        if not default_storage.exists(file_path):
            return None
        with default_storage.open(file_path, 'rb') as f:
            file_data = f.read()
    except Exception as e:
        logger.warning("Failed to read study document: %s", e)
        return None

    ext = os.path.splitext(doc.file_name)[1].lower()

    # Image types and PDF → upload to Qwen OSS (Qwen supports these natively)
    if ext in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg', '.pdf'):
        qwen_session, _ = qwen_proxy._get_session()
        midtoken = qwen_proxy.get_midtoken(qwen_session)
        if midtoken:
            qwen_session.headers['bx-umidtoken'] = midtoken
            qwen_session.headers['bx-v'] = '2.5.31'
        req_headers = dict(qwen_session.headers)
        file_obj = upload_file_from_bytes(doc.file_name, file_data, qwen_session, req_headers)
        if file_obj:
            is_image = ext not in ('.pdf',)
            return {'is_image': is_image, 'has_file': True, 'uploaded_files': [file_obj], 'text_content': None}
        return None

    # Plain text files
    if ext == '.txt':
        try:
            text = file_data.decode('utf-8')
            if text.strip():
                text = text[:MAX_TEXT_CHARS]
                return {'is_image': False, 'uploaded_files': None, 'text_content': text}
        except UnicodeDecodeError:
            pass

    logger.warning("Could not extract content from %s", doc.file_name)
    return None


def _parse_json_response(text):
    """Extract a JSON array from Qwen's response text (may have markdown fences)."""
    if not text:
        return []

    # Strip markdown code fences if present
    stripped = text.strip()
    if stripped.startswith('```'):
        first_newline = stripped.find('\n')
        if first_newline != -1:
            stripped = stripped[first_newline + 1:]
        if stripped.endswith('```'):
            stripped = stripped[:-3]
        stripped = stripped.strip()

    try:
        parsed = json.loads(stripped)
        if isinstance(parsed, list):
            return parsed
        return []
    except json.JSONDecodeError:
        # Try to find a JSON array in the text
        import re
        match = re.search(r'\[.*\]', stripped, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                pass
        logger.warning("Failed to parse Qwen JSON response: %s...", text[:200])
        return []