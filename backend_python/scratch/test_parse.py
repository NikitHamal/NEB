from api.models import SyllabusContent
from web.views import parse_sections, parse_qas

chapters = SyllabusContent.objects.filter(grade_level='Class 12', subject='English').order_by('order')
for ch in chapters[:5]:
    print(f"=== {ch.chapter_title} ===")
    print(f"  text_content: {len(ch.text_content)} chars")
    print(f"  question_answers: {len(ch.question_answers)} chars")
    secs = parse_sections(ch.text_content)
    print(f"  parse_sections: {len(secs)} sections")
    for s in secs[:3]:
        print(f"    - {s['title'][:60]}: {len(s['content'])} chars, {len(s.get('parsed_items', []))} items")
    qa = parse_qas(ch.question_answers)
    print(f"  parse_qas: {len(qa)} Q&A pairs")
    qa_secs = parse_sections(ch.question_answers)
    print(f"  qa_sections: {len(qa_secs)} sections")