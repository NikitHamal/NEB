"""Reply kinds and reviewer labels for forum threads.

A reply says what it is (kind: set by its author) and a reviewer says how it
landed (label: set by the thread's author or an admin). Both are plain short
strings on the reply row so every client reads the same two fields.
"""
KINDS = (
    ('comment', 'Comment', 'chat_bubble', 'Add to the discussion'),
    ('answer', 'Answer', 'task_alt', 'A direct answer to the question'),
    ('solution', 'Solution', 'format_list_numbered', 'A worked, step by step solution'),
    ('hint', 'Hint', 'lightbulb', 'A nudge without the full answer'),
    ('formula', 'Formula', 'function', 'A formula, rule or key fact'),
)
KIND_KEYS = tuple(k[0] for k in KINDS)

LABELS = (
    ('accepted', 'Accepted answer', 'check_circle', 'This solved it', 'good'),
    ('correct', 'Correct', 'verified', 'The working and result are right', 'good'),
    ('partial', 'Partly correct', 'rule', 'Right idea, something is missing', 'warn'),
    ('incorrect', 'Incorrect', 'cancel', 'There is a mistake in it', 'bad'),
    ('helpful', 'Helpful', 'volunteer_activism', 'Useful, even if not the answer', 'info'),
    ('spam', 'Spam', 'report', 'Off topic, ads or noise', 'bad'),
)
LABEL_KEYS = tuple(k[0] for k in LABELS)


def meta():
    return {
        'kinds': [{'key': k, 'label': l, 'icon': i, 'hint': h} for k, l, i, h in KINDS],
        'labels': [{'key': k, 'label': l, 'icon': i, 'hint': h, 'tone': t} for k, l, i, h, t in LABELS],
    }


_KIND_BY_KEY = {k: (l, i) for k, l, i, _ in KINDS}
_LABEL_BY_KEY = {k: (l, i, t) for k, l, i, _, t in LABELS}


def clean_kind(value):
    value = str(value or '').strip().lower()
    return value if value in KIND_KEYS else 'comment'


def kind_info(key):
    label, icon = _KIND_BY_KEY.get(key or 'comment', _KIND_BY_KEY['comment'])
    return {'key': key or 'comment', 'label': label, 'icon': icon}


def label_info(key):
    if key not in _LABEL_BY_KEY:
        return None
    label, icon, tone = _LABEL_BY_KEY[key]
    return {'key': key, 'label': label, 'icon': icon, 'tone': tone}


def can_label(user_id, is_admin, post_user_id):
    return bool(user_id and (is_admin or post_user_id == user_id))


def reply_extras(r, viewer_id=None, viewer_is_admin=False):
    """The fields added to every serialized reply."""
    post_owner = getattr(getattr(r, 'post', None), 'user_id', None)
    kind = r.kind or 'comment'
    return {
        'kind': kind,
        'kindInfo': kind_info(kind),
        'label': r.label or '',
        'labelInfo': label_info(r.label),
        'labeledAt': r.labeled_at or 0,
        'canLabel': can_label(viewer_id, viewer_is_admin, post_owner) and kind is not None,
    }
