import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
import django
django.setup()

from api.models import Resource

for f in Resource._meta.get_fields():
    if f.name in ['title', 'description', 'subject', 'tags', 'category', 'grade', 'grade_level', 'type', 'language', 'school', 'author']:
        mt = getattr(f, 'max_length', None)
        print(f'{f.name}: {type(f).__name__} max_length={mt} null={f.null} blank={getattr(f, "blank", None)}')
print('---')
print('resource_detail.html keywords block uses: subject, type, grade_level')
print('It does NOT include resource.tags in the keywords meta tag')
print('It does NOT include resource.author in the title')
