"""Canonical forum categories.

One list is used by the forum sidebar, the create-post form and the server-side
normaliser. Known variants fold into a canonical bucket (Mathematics -> Math,
Exam/Test -> Exam Prep, Physics -> Science). Unknown legacy values are kept so
older posts stay filterable; the create form no longer offers free text.
"""

CATEGORIES = (
    'General',
    'Science',
    'Math',
    'Exam Prep',
    'Entrance Exams',
)

_ALIASES = {
    'general': 'General',
    'general discussion': 'General',
    'discussion': 'General',
    'other': 'General',
    'misc': 'General',
    'english': 'General',
    'expo': 'General',
    'event': 'General',
    'events': 'General',
    'science': 'Science',
    'physics': 'Science',
    'chemistry': 'Science',
    'biology': 'Science',
    'computer science': 'Science',
    'computer': 'Science',
    'environmental science': 'Science',
    'environment': 'Science',
    'geology': 'Science',
    'botany': 'Science',
    'zoology': 'Science',
    'astronomy': 'Science',
    'math': 'Math',
    'maths': 'Math',
    'mathematics': 'Math',
    'additional mathematics': 'Math',
    'exam prep': 'Exam Prep',
    'exam preparation': 'Exam Prep',
    'exam tips': 'Exam Prep',
    'exam/test': 'Exam Prep',
    'exam test': 'Exam Prep',
    'exam': 'Exam Prep',
    'test': 'Exam Prep',
    'tests': 'Exam Prep',
    'ble': 'Exam Prep',
    'entrance exams': 'Entrance Exams',
    'entrance exam': 'Entrance Exams',
    'entrance': 'Entrance Exams',
    'entrance preparation': 'Entrance Exams',
}


def normalize_category(value):
    text = (value or '').strip()
    if not text:
        return CATEGORIES[0]
    key = ' '.join(text.lower().split())
    for category in CATEGORIES:
        if key == category.lower():
            return category
    return _ALIASES.get(key) or text
