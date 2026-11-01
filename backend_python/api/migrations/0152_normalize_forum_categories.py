from django.db import migrations

CATEGORIES = ('General', 'Science', 'Math', 'Exam Prep', 'Entrance Exams')

ALIASES = {
    'general': 'General', 'general discussion': 'General', 'discussion': 'General',
    'other': 'General', 'misc': 'General', 'english': 'General',
    'expo': 'General', 'event': 'General', 'events': 'General',
    'science': 'Science', 'physics': 'Science', 'chemistry': 'Science',
    'biology': 'Science', 'computer science': 'Science', 'computer': 'Science',
    'environmental science': 'Science', 'environment': 'Science',
    'geology': 'Science', 'botany': 'Science', 'zoology': 'Science',
    'astronomy': 'Science',
    'math': 'Math', 'maths': 'Math', 'mathematics': 'Math',
    'additional mathematics': 'Math',
    'exam prep': 'Exam Prep', 'exam preparation': 'Exam Prep',
    'exam tips': 'Exam Prep', 'exam/test': 'Exam Prep', 'exam test': 'Exam Prep',
    'exam': 'Exam Prep', 'test': 'Exam Prep', 'tests': 'Exam Prep', 'ble': 'Exam Prep',
    'entrance exams': 'Entrance Exams', 'entrance exam': 'Entrance Exams',
    'entrance': 'Entrance Exams', 'entrance preparation': 'Entrance Exams',
}


def _normalize(value):
    text = (value or '').strip()
    if not text:
        return CATEGORIES[0]
    key = ' '.join(text.lower().split())
    for category in CATEGORIES:
        if key == category.lower():
            return category
    return ALIASES.get(key) or text


def forwards(apps, schema_editor):
    Post = apps.get_model('api', 'Post')
    for post in Post.objects.all().only('id', 'category').iterator():
        category = _normalize(post.category)
        if category != post.category:
            Post.objects.filter(pk=post.pk).update(category=category)


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0151_keep_deleted_user_content'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
