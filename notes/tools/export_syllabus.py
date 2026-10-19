import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'notes/pipeline'))
import spine

SUBJECTS = {
    'eng': ('English', 'English'), 'nep': ('Nepali', 'नेपाली'),
    'math': ('Mathematics', 'Mathematics'), 'omath': ('Optional Mathematics', 'Optional Mathematics'),
    'sci': ('Science and Technology', 'Science and Technology'),
    'soc': ('Social Studies', 'सामाजिक अध्ययन तथा मानव मूल्य शिक्षा'),
    'health': ('Health Physical and Creative Arts', 'स्वास्थ्य, शारीरिक तथा सिर्जनात्मक कला'),
    'acc': ('Accountancy', 'Accountancy'), 'eco': ('Economics', 'Economics'),
    'phy': ('Physics', 'Physics'), 'chem': ('Chemistry', 'Chemistry'),
    'bio': ('Biology', 'Biology'), 'cs': ('Computer Science', 'Computer Science'),
}
OUT = ROOT / 'backend_python/api/data/note_syllabus.json'


def clean(text):
    text = re.sub(r'```(?:figure|photo)[^\n]*\n.*?```', '', text, flags=re.S)
    text = re.sub(r'^:::.*$|^:::$', '', text, flags=re.M)
    text = re.sub(r'<span class="marks">(.*?)</span>', r'\1', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def section(text, pattern):
    for match in re.finditer(r'^##[ \t]+([^\n]+)\n(.*?)(?=^##[ \t]+|\Z)', text, re.M | re.S):
        if re.search(pattern, match[1], re.I):
            return clean(match[2])
    return ''


def export():
    books = []
    for slug in spine.ALL:
        m = re.fullmatch(r'([a-z]+)(8|10|11|12)', slug)
        if not m or m[1] not in SUBJECTS:
            continue
        head, units = spine.load(slug)
        subject, display = SUBJECTS[m[1]]
        grade = int(m[2])
        nepali = m[1] in ('nep', 'soc', 'health')
        chapters = []
        for unit in units:
            relative = f"notes/content/{slug}/unit-{unit['no']:02d}.md"
            path = ROOT / relative
            if not path.exists():
                raise ValueError(f'Missing chapter: {relative}')
            source = path.read_text(encoding='utf-8')
            body = source.split('---', 2)[-1].strip()
            summary = section(body, r'summary|सारांश|पाठको सार|एकाइको सार')
            headings = re.findall(r'^##\s+\d+[.।]\d+\s+(.+)', body, re.M)
            detail_headings = re.findall(r'^###[ \t]+([^\n]+)', body, re.M)
            topics = [x for x in (unit['sub'] + headings + detail_headings) if not re.search(r'concepts, formulas and worked problems|Exercises of the SEE type|^\d*\.?\s*(Worked example|Practice|Exercise|Answer|About the text)', x, re.I)]
            topics = list(dict.fromkeys(topics)) or headings or unit['sub']
            intro = clean(re.split(r'^## |^:::', body, maxsplit=1, flags=re.M)[0])
            examples = []
            for match in re.finditer(r'^::: example\s*([^\n]*)\n(.*?)^:::', body, re.M | re.S):
                examples.append({'question': match[1].strip(), 'answer': clean(match[2])})
            if not examples:
                for match in re.finditer(r'^::: note[ \t]*([^\n]*)\n(.*?)^:::', body, re.M | re.S):
                    if re.search(r'model answers?|नमुना उत्तर|^उत्तर$', match[1].strip(), re.I):
                        examples.append({'question': match[1].strip(), 'answer': clean(match[2])})
            if not examples:
                practice = section(body, r'^Practice questions$')
                for match in re.finditer(r'^\*\*([^\n]+)\*\*[ \t]*\n(.*?)(?=^\*\*[^\n]+\*\*|^### |\Z)', practice, re.M | re.S):
                    answer = re.sub(r'^\[\d+\][ \t]*\n', '', match[2].strip())
                    if answer:
                        examples.append({'question': match[1].strip(), 'answer': clean(answer)})
            labels = ('विषयवस्तु', 'पाठको सार', 'अध्ययन विधि', 'आफैँ जाँच्नुहोस्') if nepali else ('Topics to cover', 'Chapter summary', 'Study route', 'Check your understanding')
            steps = ('पहिले विषयवस्तु पढ्नुहोस् र नबुझेका शब्द छुट्याउनुहोस्।\n\nपुस्तक नहेरी मुख्य विचार आफ्नै शब्दमा लेख्नुहोस्।\n\nहल गरिएको उदाहरण आफैँ हल गरेर तुलना गर्नुहोस्।\n\nअभ्यास गर्नुहोस्; गल्ती सच्याएपछि मात्र पुनरावलोकन पूरा भएको चिनो लगाउनुहोस्।' if nepali else 'Read the topics and identify unfamiliar terms.\n\nClose the book and explain the key ideas in your own words.\n\nAttempt a worked example before revealing its solution.\n\nComplete the chapter practice, correct mistakes, then mark the chapter revised.')
            guide = f"## {labels[0]}\n\n" + '\n'.join('- '+x for x in topics)
            if intro:
                guide += '\n\n'+intro
            if summary:
                guide += f'\n\n## {labels[1]}\n\n'+summary
            guide += f'\n\n## {labels[2]}\n\n'+steps
            qa = '\n\n'.join(f"## {x['question'] or labels[3]}\n\n{x['answer']}" for x in examples)
            chapters.append({
                'id': f"{slug}-unit-{unit['no']:02d}", 'name': unit['title'],
                'order': unit['no'], 'hours': int(unit['hours']) if unit['hours'] else None,
                'area': unit['area'], 'topics': topics, 'summary': summary,
                'text_content': guide, 'question_answers': qa,
                'self_checks': examples, 'source_path': relative,
                'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'source_url': f'https://github.com/NikitHamal/NEB/blob/resources/grade8-10-polish-syllabus-c/{relative}',
            })
        books.append({'slug': slug, 'grade': 'Class 10 / SEE' if grade == 10 else f'Class {grade}',
                      'subject': subject, 'display_name': display, 'language': 'ne' if nepali else 'en',
                      'source_label': 'नेबियन्स अध्ययन टिपोट' if nepali else 'NEBians study notes',
                      'curriculum_source': next((x for x in head['notes'] if x.startswith('SOURCE:')), ''),
                      'chapters': chapters})
    payload = {'version': 1, 'books': books}
    encoded = json.dumps(payload, ensure_ascii=False, indent=2)+'\n'
    if '--check' in sys.argv:
        if not OUT.exists() or OUT.read_text() != encoded:
            raise SystemExit('Syllabus catalogue is stale. Run notes/tools/export_syllabus.py.')
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(encoded)
    print(f'{len(books)} subjects, {sum(len(b["chapters"]) for b in books)} chapters; all sources present.')


if __name__ == '__main__':
    export()
