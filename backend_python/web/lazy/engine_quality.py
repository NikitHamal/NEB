"""Deterministic quality guards for generated documents.

The model cannot be trusted to notice its own structural faults, so these
check the *shape* of a draft instead: does the section named for data hold a
table, has it drifted off the requested topic, did it emit the same table
twice. Everything here is free — no model calls.
"""

import re


_STOPWORDS = {
    'the', 'a', 'an', 'of', 'to', 'for', 'and', 'or', 'in', 'on', 'by', 'with',
    'using', 'from', 'is', 'are', 'be', 'this', 'that', 'report', 'document',
}


def _topic_overlap(left, right):
    """Word overlap between two titles, 0..1, ignoring stopwords.

    Used only as a drift alarm: a real topic change shares almost no content
    words with the request, while a reworded title still shares most.
    """
    def words(text):
        return {
            w for w in re.findall(r"[a-z0-9']+", str(text or '').lower())
            if len(w) > 2 and w not in _STOPWORDS
        }
    a, b = words(left), words(right)
    if not a or not b:
        return 0.0
    return len(a & b) / float(min(len(a), len(b)))


def _dedupe_tables(sections):
    """Drop a table that restates an earlier one.

    The revision pass can add the table a section was missing while the original
    draft's weaker version stays put. Two tables of the same readings with
    different numbers in one report reads as an error, so the later copy goes.
    """
    seen = []
    removed = 0
    for sec in sections or []:
        blocks = sec.get('blocks') or []
        if not blocks:
            continue
        kept = []
        for block in blocks:
            if str(block.get('type')) != 'table':
                kept.append(block)
                continue
            signature = _table_signature(block)
            # Headers get reworded between the draft and the revision ("Trial No."
            # vs "Trial No"), so match on content-word overlap, not equality.
            duplicate = signature and any(
                len(signature & other) / float(min(len(signature), len(other))) >= 0.6
                for other in seen
            )
            if duplicate:
                removed += 1
                continue
            if signature:
                seen.append(signature)
            kept.append(block)
        sec['blocks'] = kept
    return removed


def _table_signature(block):
    header = [str(h).strip().lower() for h in (block.get('header') or [])]
    header = [h for h in header if h and len(h) > 1]
    if len(header) < 2:
        return None
    key = set(re.findall(r"[a-z]+", ' '.join(header)))
    return key if len(key) >= 2 else None


def _missing_tables(outline, sections):
    """Sections planned as data-bearing that came back without a table block.

    A drafter that describes a table in prose passes every content check — the
    words are right, the structure is not. This catches it deterministically so
    the critic sees the defect instead of reading past it.
    """
    planned = outline.get('sections') or []
    missing = []
    for sec in sections or []:
        types = [str(t).lower() for t in (sec.get('block_types') or [])]
        heading = sec.get('heading') or ''
        heading_looks_tabular = any(
            word in heading.lower()
            for word in ('observation', 'observation table', 'result', 'comparison',
                         'specification', 'schedule', 'tabulation', 'data')
        )
        if 'table' not in types and not heading_looks_tabular:
            continue
        has_table = any(str(b.get('type')) == 'table' for b in (sec.get('blocks') or []))
        if not has_table:
            missing.append(heading)
    if missing:
        return missing
    # Fall back to the outline's own declaration when the draft dropped the hint.
    # Match on heading, never on position: a revision pass can reorder or drop
    # sections, and positional matching would then blame the wrong one.
    drafted = {(s.get('heading') or '').strip().lower(): s for s in sections or []}
    for plan in planned:
        types = [str(t).lower() for t in (plan.get('block_types') or [])]
        if 'table' not in types:
            continue
        heading = plan.get('heading') or ''
        drafted_section = drafted.get(heading.strip().lower())
        if drafted_section is None:
            continue
        has_table = any(str(b.get('type')) == 'table' for b in (drafted_section.get('blocks') or []))
        if not has_table:
            missing.append(heading)
    return missing
