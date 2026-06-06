from api.models import SyllabusContent
for c in SyllabusContent.objects.filter(grade_level='Class 12', subject='English').order_by('order'):
    tc = len(c.text_content) if c.text_content else 0
    qa = len(c.question_answers) if c.question_answers else 0
    print(f'{c.order:2d}. {c.chapter_title}: text={tc}, qa={qa}')