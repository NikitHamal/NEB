from api.models import SyllabusContent
chapters = SyllabusContent.objects.filter(grade_level='Class 12', subject='English').order_by('order')
for c in chapters:
    tc = len(c.text_content) if c.text_content else 0
    qa = len(c.question_answers) if c.question_answers else 0
    print(f'{c.order:2d}. {c.chapter_title}: text={tc:5d}, qa={qa:5d}')
print(f'Total: {chapters.count()} chapters')