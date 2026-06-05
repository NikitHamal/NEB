import time
import json
from django.core.management.base import BaseCommand
from api.models import SyllabusContent

# This command seeds Class 12 English syllabus content.
# Due to the massive volume (40 chapters), content is stored in a separate JSON file.
# If the JSON file doesn't exist, it creates placeholder chapters.
# To add full content, use the admin import at /admin/syllabus/import/

CHAPTERS = [
    # Language Development
    {'chapter_id': 'class-12-english-critical-thinking', 'chapter_title': 'Unit 1: Critical Thinking', 'order': 1},
    {'chapter_id': 'class-12-english-family', 'chapter_title': 'Unit 2: Family', 'order': 2},
    {'chapter_id': 'class-12-english-sports', 'chapter_title': 'Unit 3: Sports', 'order': 3},
    {'chapter_id': 'class-12-english-technology', 'chapter_title': 'Unit 4: Technology', 'order': 4},
    {'chapter_id': 'class-12-english-education', 'chapter_title': 'Unit 5: Education', 'order': 5},
    {'chapter_id': 'class-12-english-money-and-economy', 'chapter_title': 'Unit 6: Money and Economy', 'order': 6},
    {'chapter_id': 'class-12-english-humour', 'chapter_title': 'Unit 7: Humour', 'order': 7},
    {'chapter_id': 'class-12-english-human-culture', 'chapter_title': 'Unit 8: Human Culture', 'order': 8},
    {'chapter_id': 'class-12-english-ecology-and-environment', 'chapter_title': 'Unit 9: Ecology and Environment', 'order': 9},
    {'chapter_id': 'class-12-english-career-opportunities', 'chapter_title': 'Unit 10: Career Opportunities', 'order': 10},
    {'chapter_id': 'class-12-english-hobbies', 'chapter_title': 'Unit 11: Hobbies', 'order': 11},
    {'chapter_id': 'class-12-english-animal-world', 'chapter_title': 'Unit 12: Animal World', 'order': 12},
    {'chapter_id': 'class-12-english-history', 'chapter_title': 'Unit 13: History', 'order': 13},
    {'chapter_id': 'class-12-english-human-rights', 'chapter_title': 'Unit 14: Human Rights', 'order': 14},
    {'chapter_id': 'class-12-english-leisure-and-entertainment', 'chapter_title': 'Unit 15: Leisure and Entertainment', 'order': 15},
    {'chapter_id': 'class-12-english-fantasy', 'chapter_title': 'Unit 16: Fantasy', 'order': 16},
    {'chapter_id': 'class-12-english-war-and-peace', 'chapter_title': 'Unit 17: War and Peace', 'order': 17},
    {'chapter_id': 'class-12-english-music-and-creation', 'chapter_title': 'Unit 18: Music and Creation', 'order': 18},
    {'chapter_id': 'class-12-english-migration-and-diaspora', 'chapter_title': 'Unit 19: Migration and Diaspora', 'order': 19},
    {'chapter_id': 'class-12-english-power-and-politics', 'chapter_title': 'Unit 20: Power and Politics', 'order': 20},
    # Literature - Short Stories
    {'chapter_id': 'class-12-english-neighbours', 'chapter_title': 'Story 1: Neighbours', 'order': 21},
    {'chapter_id': 'class-12-english-a-respectable-woman', 'chapter_title': 'Story 2: A Respectable Woman', 'order': 22},
    {'chapter_id': 'class-12-english-a-devoted-son', 'chapter_title': 'Story 3: A Devoted Son', 'order': 23},
    {'chapter_id': 'class-12-english-the-treasure-in-the-forest', 'chapter_title': 'Story 4: The Treasure in the Forest', 'order': 24},
    {'chapter_id': 'class-12-english-my-old-home', 'chapter_title': 'Story 5: My Old Home', 'order': 25},
    {'chapter_id': 'class-12-english-half-closed-eyes-buddha', 'chapter_title': 'Story 6: The Half-closed Eyes of the Buddha and the Slowly Sinking Sun', 'order': 26},
    {'chapter_id': 'class-12-english-a-very-old-man-with-enormous-wings', 'chapter_title': 'Story 7: A Very Old Man with Enormous Wings', 'order': 27},
    # Literature - Poems
    {'chapter_id': 'class-12-english-a-day', 'chapter_title': 'Poem 1: A Day', 'order': 28},
    {'chapter_id': 'class-12-english-every-morning-i-wake', 'chapter_title': 'Poem 2: Every Morning I Wake', 'order': 29},
    {'chapter_id': 'class-12-english-i-was-my-own-route', 'chapter_title': 'Poem 3: I Was My Own Route', 'order': 30},
    {'chapter_id': 'class-12-english-the-awakening-age', 'chapter_title': 'Poem 4: The Awakening Age', 'order': 31},
    {'chapter_id': 'class-12-english-soft-storm', 'chapter_title': 'Poem 5: Soft Storm', 'order': 32},
    # Literature - Essays
    {'chapter_id': 'class-12-english-on-libraries', 'chapter_title': 'Essay 1: On Libraries', 'order': 33},
    {'chapter_id': 'class-12-english-marriage-as-a-social-institution', 'chapter_title': 'Essay 2: Marriage as a Social Institution', 'order': 34},
    {'chapter_id': 'class-12-english-knowledge-and-wisdom', 'chapter_title': 'Essay 3: Knowledge and Wisdom', 'order': 35},
    {'chapter_id': 'class-12-english-humility', 'chapter_title': 'Essay 4: Humility', 'order': 36},
    {'chapter_id': 'class-12-english-human-rights-and-the-age-of-inequality', 'chapter_title': 'Essay 5: Human Rights and the Age of Inequality', 'order': 37},
    # Literature - One Act Plays
    {'chapter_id': 'class-12-english-a-matter-of-husbands', 'chapter_title': 'Play 1: A Matter of Husbands', 'order': 38},
    {'chapter_id': 'class-12-english-facing-death', 'chapter_title': 'Play 2: Facing Death', 'order': 39},
    {'chapter_id': 'class-12-english-the-bull', 'chapter_title': 'Play 3: The Bull', 'order': 40},
]


class Command(BaseCommand):
    help = 'Seed Class 12 English syllabus content (40 chapters). Use --with-content to include exercise solutions.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Overwrite existing chapters with same chapter_id',
        )
        parser.add_argument(
            '--json-file',
            type=str,
            default='',
            help='Path to JSON file with full chapter content',
        )

    def handle(self, *args, **options):
        now = int(time.time() * 1000)
        grade = 'Class 12'
        subject = 'English'
        overwrite = options['overwrite']
        json_file = options['json_file']

        content_map = {}
        if json_file:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    raw = json.load(f)
                if isinstance(raw, list):
                    for item in raw:
                        cid = item.get('chapter_id', '')
                        if cid:
                            content_map[cid] = item
                elif isinstance(raw, dict):
                    content_map = raw
                self.stdout.write(self.style.SUCCESS(f'Loaded content from {json_file} ({len(content_map)} chapters)'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to load JSON: {e}'))
                return

        created = 0
        updated = 0
        skipped = 0

        for chapter_data in CHAPTERS:
            chapter_id = chapter_data['chapter_id']
            text_content = content_map.get(chapter_id, {}).get('text_content', '')
            question_answers = content_map.get(chapter_id, {}).get('question_answers', '')

            if not text_content and not overwrite:
                existing = SyllabusContent.objects.filter(chapter_id=chapter_id).first()
                if existing:
                    skipped += 1
                    self.stdout.write(f'Skipped (exists, no content): {chapter_data["chapter_title"]}')
                    continue

            try:
                obj = SyllabusContent.objects.get(chapter_id=chapter_id)
                obj.grade_level = grade
                obj.subject = subject
                obj.chapter_title = chapter_data['chapter_title']
                obj.text_content = text_content
                obj.question_answers = question_answers
                obj.order = chapter_data['order']
                obj.updated_at = now
                obj.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'Updated: {obj.chapter_title}'))
            except SyllabusContent.DoesNotExist:
                obj = SyllabusContent.objects.create(
                    id=chapter_id,
                    chapter_id=chapter_id,
                    grade_level=grade,
                    subject=subject,
                    chapter_title=chapter_data['chapter_title'],
                    text_content=text_content,
                    question_answers=question_answers,
                    order=chapter_data['order'],
                    created_at=now,
                    updated_at=now,
                )
                created += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {obj.chapter_title}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created: {created}, Updated: {updated}, Skipped: {skipped}'
        ))