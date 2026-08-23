import json

from api.models import CanvasNode
from api.utils import now_ms, uuid_str


TEMPLATES = {
    'blank': {
        'name': 'Blank canvas',
        'icon': 'space_dashboard',
        'description': 'Start from one question and branch freely.',
        'nodes': [],
    },
    'exam-sprint': {
        'name': 'Exam sprint',
        'icon': 'school',
        'description': 'Map a syllabus, weak areas, practice and revision.',
        'nodes': [
            ('Goal', 'Write the exam, subject, date and target score here.', 120, 80, 'goal'),
            ('Syllabus map', 'List the chapters or units you must cover. Branch each one into concepts.', 120, 360, 'topic'),
            ('Weak spots', 'Collect confusing concepts and mistakes. Ask Neby to diagnose each one.', 720, 360, 'question'),
            ('Practice bank', 'Add past-paper questions, likely questions and mini quizzes.', 120, 660, 'practice'),
            ('Final review', 'Turn the strongest branches into a one-page revision path.', 720, 660, 'summary'),
        ],
    },
    'research-map': {
        'name': 'Research map',
        'icon': 'travel_explore',
        'description': 'Question, evidence, counterpoints, sources and synthesis.',
        'nodes': [
            ('Research question', 'State the exact question, scope and what would count as a useful answer.', 120, 80, 'goal'),
            ('What we know', 'Capture established facts and definitions. Add sources to each branch.', 120, 390, 'source'),
            ('Open questions', 'Track uncertainties, missing evidence and assumptions worth testing.', 720, 390, 'question'),
            ('Counterpoints', 'Collect competing explanations, objections and alternative interpretations.', 120, 700, 'comparison'),
            ('Synthesis', 'Summarize what the evidence supports, what remains uncertain and what to do next.', 720, 700, 'summary'),
        ],
    },
    'essay-builder': {
        'name': 'Essay builder',
        'icon': 'edit_note',
        'description': 'Build a thesis from claims, evidence and counterarguments.',
        'nodes': [
            ('Prompt', 'Paste the essay prompt and constraints.', 120, 80, 'goal'),
            ('Thesis', 'Draft a specific, arguable one-sentence thesis.', 120, 370, 'summary'),
            ('Claims', 'Create one branch per body-paragraph claim.', 720, 370, 'topic'),
            ('Evidence', 'Attach examples, quotations, facts or sources to each claim.', 120, 680, 'source'),
            ('Counterargument', 'Represent the strongest opposing view, then answer it fairly.', 720, 680, 'comparison'),
        ],
    },
    'project-plan': {
        'name': 'Project plan',
        'icon': 'account_tree',
        'description': 'Outcome, milestones, risks, decisions and next actions.',
        'nodes': [
            ('Outcome', 'Define what done means, for whom, and by when.', 120, 80, 'goal'),
            ('Milestones', 'Break the outcome into measurable checkpoints.', 120, 370, 'topic'),
            ('Risks', 'List the biggest uncertainties, blockers and dependencies.', 720, 370, 'warning'),
            ('Decisions', 'Capture important choices and why they were made.', 120, 680, 'decision'),
            ('Next actions', 'Keep the immediate 3–7 actions here. Branch owners or details as needed.', 720, 680, 'task'),
        ],
    },
    'concept-master': {
        'name': 'Concept mastery',
        'icon': 'psychology',
        'description': 'Learn a concept through definition, mechanism, example and test.',
        'nodes': [
            ('Concept', 'Write the concept you want to truly understand.', 120, 80, 'goal'),
            ('Explain simply', 'Ask for an intuitive explanation with no jargon.', 120, 370, 'question'),
            ('How it works', 'Map the mechanism, steps, causes or internal structure.', 720, 370, 'topic'),
            ('Worked example', 'Create a concrete example and walk through it step by step.', 120, 680, 'practice'),
            ('Test me', 'Generate retrieval questions, misconceptions and one challenge problem.', 720, 680, 'practice'),
        ],
    },
}


def template_catalog():
    return [
        {'key': key, 'name': item['name'], 'icon': item['icon'], 'description': item['description']}
        for key, item in TEMPLATES.items()
    ]


def apply_template(board, user, key):
    template = TEMPLATES.get(key)
    if not template:
        return []
    now = now_ms()
    created = []
    for title, body, x, y, kind in template['nodes']:
        content = {
            'title': title,
            'summary': body,
            'sections': [{'type': 'text', 'content': body}],
        }
        created.append(CanvasNode(
            id=uuid_str(),
            board=board,
            user=user,
            prompt='',
            title=title,
            content=json.dumps(content, ensure_ascii=False),
            status='done',
            x=float(x),
            y=float(y),
            kind='note',
            metadata=json.dumps({'templateRole': kind}, ensure_ascii=False),
            created_at=now,
            updated_at=now,
        ))
    if created:
        CanvasNode.objects.bulk_create(created)
    board.settings = json.dumps({'template': key, 'layout': 'freeform'}, ensure_ascii=False)
    board.updated_at = now
    board.save(update_fields=['settings', 'updated_at'])
    return created
