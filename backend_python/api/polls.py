"""Polls on posts and on comments: one payload shape for web, app and realtime.

A poll hangs off a post or a reply. A poll with `allow_add_options` lets any
signed-in member append an option of their own, like a Facebook poll.
"""
from __future__ import annotations

from django.db import transaction
from django.db.models import F

from .models import Poll, PollOption, PollVote
from .utils import now_ms, uuid_str

MAX_INITIAL_OPTIONS = 6
MAX_TOTAL_OPTIONS = 12
MAX_OPTION_LEN = 100
MIN_OPTIONS = 2


# --------------------------------------------------------------------------
# Payload
# --------------------------------------------------------------------------

def _option_dict(o, my_votes: set, added_by_me: set) -> dict:
    return {
        'id': o.id, 'text': o.text, 'order': o.order,
        'isCorrect': o.is_correct, 'is_correct': o.is_correct,
        'voteCount': o.vote_count, 'vote_count': o.vote_count,
        'isMine': o.id in my_votes,
        'addedByMe': o.id in added_by_me,
        'isAdded': bool(o.added_by_id),
    }


def poll_dict(poll: Poll, user_id=None, my_votes=None) -> dict:
    """Serialise one poll. `my_votes` is a set of option ids the viewer picked
    (pass it when serialising in bulk, otherwise it is queried)."""
    options = list(poll.options.all()) if hasattr(poll, '_prefetched_objects_cache') and \
        'options' in getattr(poll, '_prefetched_objects_cache', {}) else list(poll.options.order_by('order'))
    options.sort(key=lambda o: (o.order, o.created_at))
    if my_votes is None:
        my_votes = set()
        if user_id:
            my_votes = set(PollVote.objects.filter(poll=poll, user_id=user_id).values_list('option_id', flat=True))
    added_by_me = {o.id for o in options if user_id and o.added_by_id == user_id}
    expired = poll.is_expired
    voted = bool(my_votes)
    user_vote = None
    if voted:
        user_vote = sorted(my_votes) if poll.allow_multiple else next(iter(my_votes))
    leader = None
    if options and poll.total_votes:
        top = max(options, key=lambda o: o.vote_count)
        if top.vote_count > 0:
            leader = top.id
    can_retract = bool(voted and not expired and poll.poll_type == Poll.POLL_TYPE_VOTING)
    return {
        'id': poll.id,
        'postId': poll.post_id or '',
        'replyId': poll.reply_id or '',
        'question': poll.question,
        'pollType': poll.poll_type, 'poll_type': poll.poll_type,
        'allowMultiple': poll.allow_multiple, 'allow_multiple': poll.allow_multiple,
        'allowAddOptions': poll.allow_add_options, 'allow_add_options': poll.allow_add_options,
        'explanation': poll.explanation,
        'durationMs': poll.duration_ms, 'duration_ms': poll.duration_ms,
        'createdAt': poll.created_at,
        'expiresAt': (poll.created_at + poll.duration_ms) if poll.duration_ms else 0,
        'totalVotes': poll.total_votes, 'total_votes': poll.total_votes,
        'isExpired': expired,
        'options': [_option_dict(o, my_votes, added_by_me) for o in options],
        'optionCount': len(options),
        'leaderId': leader,
        'userVote': user_vote,
        'userVotes': sorted(my_votes),
        'hasVoted': voted,
        'canAddOption': bool(poll.allow_add_options and not expired and len(options) < MAX_TOTAL_OPTIONS
                             and poll.poll_type == Poll.POLL_TYPE_VOTING),
        'canRetract': can_retract,
    }


def _my_votes_by_poll(poll_ids, user_id) -> dict:
    out: dict = {}
    if user_id and poll_ids:
        for pid, oid in PollVote.objects.filter(poll_id__in=poll_ids, user_id=user_id).values_list('poll_id', 'option_id'):
            out.setdefault(pid, set()).add(oid)
    return out


def for_posts(post_ids, user_id=None) -> dict:
    """{post_id: payload} for the posts that have a poll."""
    polls = list(Poll.objects.filter(post_id__in=list(post_ids)).prefetch_related('options'))
    votes = _my_votes_by_poll([p.id for p in polls], user_id)
    return {p.post_id: poll_dict(p, user_id, votes.get(p.id, set())) for p in polls}


def for_replies(reply_ids, user_id=None) -> dict:
    """{reply_id: payload} for the replies that have a poll."""
    polls = list(Poll.objects.filter(reply_id__in=list(reply_ids)).prefetch_related('options'))
    votes = _my_votes_by_poll([p.id for p in polls], user_id)
    return {p.reply_id: poll_dict(p, user_id, votes.get(p.id, set())) for p in polls}


# --------------------------------------------------------------------------
# Creation
# --------------------------------------------------------------------------

def clean_poll_input(raw) -> tuple[dict | None, str]:
    """Validate a client `poll` object. Returns (poll_data, error)."""
    if not raw:
        return None, ''
    if not isinstance(raw, dict):
        return None, 'Invalid poll'
    options = raw.get('options') or []
    cleaned = []
    for opt in options:
        if isinstance(opt, dict):
            text = str(opt.get('text', '')).strip()
            correct = bool(opt.get('is_correct') or opt.get('isCorrect'))
        else:
            text, correct = str(opt).strip(), False
        if not text:
            return None, 'Poll options cannot be empty'
        if len(text) > MAX_OPTION_LEN:
            return None, f'Poll options must be {MAX_OPTION_LEN} characters or fewer'
        cleaned.append({'text': text, 'is_correct': correct})
    if len(cleaned) < MIN_OPTIONS:
        return None, 'Poll must have at least 2 options'
    if len(cleaned) > MAX_INITIAL_OPTIONS:
        return None, f'Poll can have at most {MAX_INITIAL_OPTIONS} options'
    if len({o['text'].lower() for o in cleaned}) != len(cleaned):
        return None, 'Poll options must be different'
    ptype = raw.get('poll_type') or raw.get('pollType') or 'voting'
    if ptype not in ('voting', 'mcq'):
        ptype = 'voting'
    try:
        duration = int(raw.get('duration_ms') or raw.get('durationMs') or 0)
    except (TypeError, ValueError):
        duration = 0
    if duration not in {d for d, _ in Poll.DURATION_CHOICES}:
        duration = 0
    return {
        'question': str(raw.get('question', '')).strip()[:300],
        'poll_type': ptype,
        'allow_multiple': bool(raw.get('allow_multiple') or raw.get('allowMultiple')),
        'allow_add_options': bool(raw.get('allow_add_options') or raw.get('allowAddOptions')) and ptype == 'voting',
        'explanation': str(raw.get('explanation', '')).strip()[:1000],
        'duration_ms': duration,
        'options': cleaned,
    }, ''


def create_poll(poll_data: dict, *, post=None, reply=None, now: int | None = None) -> Poll:
    now = now or now_ms()
    poll = Poll.objects.create(
        id=uuid_str(), post=post, reply=reply,
        question=poll_data.get('question', ''),
        poll_type=poll_data.get('poll_type', 'voting'),
        allow_multiple=bool(poll_data.get('allow_multiple', False)),
        allow_add_options=bool(poll_data.get('allow_add_options', False)),
        explanation=poll_data.get('explanation', ''),
        duration_ms=poll_data.get('duration_ms', 0),
        total_votes=0, created_at=now,
    )
    rows = []
    for i, opt in enumerate(poll_data.get('options', [])):
        if isinstance(opt, dict):
            text, correct = str(opt.get('text', '')).strip(), bool(opt.get('is_correct', False))
        else:
            text, correct = str(opt).strip(), False
        if text:
            rows.append(PollOption(id=uuid_str(), poll=poll, text=text[:200], is_correct=correct,
                                   vote_count=0, order=i, created_at=now))
    if rows:
        PollOption.objects.bulk_create(rows)
    return poll


# --------------------------------------------------------------------------
# Actions
# --------------------------------------------------------------------------

def add_option(user, poll_id: str, text: str, vote: bool = True):
    """Append an option. Returns (payload | {'error':..}, status)."""
    text = ' '.join(str(text or '').split())
    if not text:
        return {'error': 'Type an option first'}, 400
    if len(text) > MAX_OPTION_LEN:
        return {'error': f'Options must be {MAX_OPTION_LEN} characters or fewer'}, 400
    with transaction.atomic():
        try:
            poll = Poll.objects.select_for_update().get(pk=poll_id)
        except Poll.DoesNotExist:
            return {'error': 'Poll not found'}, 404
        if not poll.allow_add_options or poll.poll_type != Poll.POLL_TYPE_VOTING:
            return {'error': 'This poll does not accept new options'}, 403
        if poll.is_expired:
            return {'error': 'This poll has ended'}, 400
        existing = list(poll.options.all())
        if len(existing) >= MAX_TOTAL_OPTIONS:
            return {'error': f'A poll can have at most {MAX_TOTAL_OPTIONS} options'}, 400
        if any(o.text.strip().lower() == text.lower() for o in existing):
            return {'error': 'That option is already in the poll'}, 409
        nxt = max([o.order for o in existing], default=-1) + 1
        option = PollOption.objects.create(
            id=uuid_str(), poll=poll, text=text, is_correct=False, vote_count=0,
            order=nxt, added_by=user, created_at=now_ms(),
        )
    if vote:
        already = PollVote.objects.filter(poll_id=poll_id, user=user).exists()
        if poll.allow_multiple or not already:
            from . import services
            services.vote_poll(user, poll_id, [option.id])
    poll = Poll.objects.prefetch_related('options').get(pk=poll_id)
    return poll_dict(poll, user.id), 201


def retract_vote(user, poll_id: str):
    """Remove the viewer's votes so they can choose again."""
    with transaction.atomic():
        try:
            poll = Poll.objects.select_for_update().get(pk=poll_id)
        except Poll.DoesNotExist:
            return {'error': 'Poll not found'}, 404
        if poll.is_expired:
            return {'error': 'This poll has ended'}, 400
        if poll.poll_type != Poll.POLL_TYPE_VOTING:
            return {'error': 'Quiz answers are final'}, 400
        votes = list(PollVote.objects.filter(poll=poll, user=user))
        if not votes:
            return {'error': 'You have not voted'}, 400
        for v in votes:
            PollOption.objects.filter(pk=v.option_id, vote_count__gt=0).update(vote_count=F('vote_count') - 1)
        Poll.objects.filter(pk=poll.pk, total_votes__gte=len(votes)).update(total_votes=F('total_votes') - len(votes))
        PollVote.objects.filter(pk__in=[v.pk for v in votes]).delete()
    poll = Poll.objects.prefetch_related('options').get(pk=poll_id)
    return poll_dict(poll, user.id), 200
