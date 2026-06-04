import uuid
import time
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Resource, User, SyllabusContent

class Command(BaseCommand):
    help = 'Seed realistic mock study resources for testing Class & Subject pages.'

    def handle(self, *args, **options):
        # Fetch an admin/staff user to assign as uploader if needed
        admin_user = User.objects.filter(is_admin=True).first() or User.objects.first()
        if not admin_user:
            self.stdout.write(self.style.ERROR('No users found in database. Please run migrations or create a user first.'))
            return

        now = int(time.time() * 1000)
        
        resources_data = [
            # ── CLASS 12 ENGLISH ──
            {
                'title': 'The Bull (Play) - Summary & Exercise Solutions',
                'description': 'Complete summary, character sketches, and exercise answers for the one-act play "The Bull" by Bhimnidhi Tiwari. Ideal for NEB Class 12 preparation.',
                'subject': 'English',
                'grade_level': 'Class 12',
                'faculty': 'Science, Management, Humanities',
                'exam_type': 'Notes',
                'tags': 'The Bull, Play, Summary, Question Answer, Chapter 1, Section II',
                'type': 'Note',
                'file_url': 'https://nebians.consica.com.np/static/web/mock/the_bull_notes.pdf',
                'view_count': 1420,
                'like_count': 45,
            },
            {
                'title': 'The Selfish Giant - Complete Analysis & Summary',
                'description': 'Short story analysis, theme discussion, and long question answers for "The Selfish Giant" by Oscar Wilde.',
                'subject': 'English',
                'grade_level': 'Class 12',
                'faculty': 'Science, Management, Humanities',
                'exam_type': 'Notes',
                'tags': 'The Selfish Giant, Summary, Oscar Wilde, Short Stories, Chapter 2',
                'type': 'PDF',
                'file_url': 'https://nebians.consica.com.np/static/web/mock/selfish_giant.pdf',
                'view_count': 820,
                'like_count': 23,
            },
            {
                'title': 'The Oval Portrait - Short Question Answers',
                'description': 'Solves all short questions and gothic element analysis for Edgar Allan Poe\'s "The Oval Portrait".',
                'subject': 'English',
                'grade_level': 'Class 12',
                'faculty': 'Science, Management, Humanities',
                'exam_type': 'Notes',
                'tags': 'The Oval Portrait, Short Stories, Edgar Allan Poe, Question Answer, Chapter 3',
                'type': 'Note',
                'file_url': 'https://nebians.consica.com.np/static/web/mock/oval_portrait.pdf',
                'view_count': 640,
                'like_count': 18,
            },
            {
                'title': 'NEB Class 12 Compulsory English Board Paper - 2080 BS',
                'description': 'Official board exam question paper of Compulsory English for Class 12 (NEB Nepal), held in 2080 BS.',
                'subject': 'English',
                'grade_level': 'Class 12',
                'faculty': 'Science, Management, Humanities',
                'exam_type': 'Board',
                'tags': 'Past Paper, Board Exam, 2080 BS, Model Question, Exam Prep',
                'type': 'PDF',
                'file_url': 'https://nebians.consica.com.np/static/web/mock/english_2080_board.pdf',
                'view_count': 3240,
                'like_count': 112,
            },
            {
                'title': 'Class 12 English Grammar - Rules & Practice Set',
                'description': 'Handy cheatsheet containing all grammar rules required for NEB Class 12 English syllabus, including reported speech, passive voice, and prepositions.',
                'subject': 'English',
                'grade_level': 'Class 12',
                'faculty': 'Science, Management, Humanities',
                'exam_type': 'Notes',
                'tags': 'Grammar, Rules, Prepositions, Voice, Concord, Final Exam',
                'type': 'PDF',
                'file_url': 'https://nebians.consica.com.np/static/web/mock/english_grammar.pdf',
                'view_count': 1950,
                'like_count': 89,
            },

            # ── CLASS 12 COMPUTER SCIENCE ──
            {
                'title': 'Chapter 1: Database Management System (DBMS) Notes',
                'description': 'Comprehensive lecture notes covering database models, relational algebra, SQL queries, normalization (1NF, 2NF, 3NF), and database administration concepts.',
                'subject': 'Computer Science',
                'grade_level': 'Class 12',
                'faculty': 'Science',
                'exam_type': 'Notes',
                'tags': 'DBMS, SQL, Normalization, Chapter 1, Database, Lecture Notes',
                'type': 'PDF',
                'file_url': 'https://nebians.consica.com.np/static/web/mock/dbms_notes.pdf',
                'view_count': 1580,
                'like_count': 62,
            },
            {
                'title': 'Chapter 2: Computer Network & Communication notes',
                'description': 'Study materials on network topologies, transmission media, OSI reference model, TCP/IP protocols, and basic network devices.',
                'subject': 'Computer Science',
                'grade_level': 'Class 12',
                'faculty': 'Science',
                'exam_type': 'Notes',
                'tags': 'Computer Network, Topology, OSI Model, TCP/IP, Chapter 2',
                'type': 'PDF',
                'file_url': 'https://nebians.consica.com.np/static/web/mock/networks_notes.pdf',
                'view_count': 1140,
                'like_count': 41,
            },
            {
                'title': 'Chapter 3: Web Technology II (PHP & JavaScript) Solutions',
                'description': 'Exercise answers and code snippets for PHP database integration, form handling, cookies, sessions, and dynamic client-side scripting.',
                'subject': 'Computer Science',
                'grade_level': 'Class 12',
                'faculty': 'Science',
                'exam_type': 'Notes',
                'tags': 'Web Technology, PHP, JavaScript, Forms, Chapter 3, Solution',
                'type': 'Note',
                'file_url': 'https://nebians.consica.com.np/static/web/mock/web_tech_solutions.pdf',
                'view_count': 940,
                'like_count': 35,
            },
            {
                'title': 'NEB Class 12 Computer Science Model Questions & Solution',
                'description': 'Important model questions prepared according to the new grid syllabus of NEB Class 12 Computer Science, along with detailed solutions.',
                'subject': 'Computer Science',
                'grade_level': 'Class 12',
                'faculty': 'Science',
                'exam_type': 'Mock',
                'tags': 'Model Paper, Solution, Coding, SQL, C++, HTML, Board Prep',
                'type': 'PDF',
                'file_url': 'https://nebians.consica.com.np/static/web/mock/computer_model_solution.pdf',
                'view_count': 2210,
                'like_count': 94,
            },
            
            # ── CLASS 11 PHYSICS ──
            {
                'title': 'Unit 1: Mechanics - Complete Theory & Derivations',
                'description': 'Handwritten notes covering vector algebra, kinematics, projectile motion, Newton\'s laws of motion, work, energy, power, and rotational mechanics.',
                'subject': 'Physics',
                'grade_level': 'Class 11',
                'faculty': 'Science',
                'exam_type': 'Notes',
                'tags': 'Mechanics, Projectile Motion, Circular Motion, Derivations, Unit 1',
                'type': 'PDF',
                'file_url': 'https://nebians.consica.com.np/static/web/mock/physics_mechanics.pdf',
                'view_count': 2890,
                'like_count': 143,
            },
            {
                'title': 'First and Second Law of Thermodynamics Notes',
                'description': 'Detailed notes on thermodynamic systems, work done in isobaric/isothermal processes, heat engines, Carnot cycle, entropy, and second law statements.',
                'subject': 'Physics',
                'grade_level': 'Class 11',
                'faculty': 'Science',
                'exam_type': 'Notes',
                'tags': 'Thermodynamics, Carnot Cycle, Heat Engine, Unit 2, Notes',
                'type': 'PDF',
                'file_url': 'https://nebians.consica.com.np/static/web/mock/thermodynamics.pdf',
                'view_count': 1810,
                'like_count': 78,
            },
            {
                'title': 'Geometrical Optics - Derivations & Formulas',
                'description': 'Reflection, refraction, prism formula, lens maker\'s formula derivations, and optical instrument diagrams (microscope, telescope) for Class 11 Physics.',
                'subject': 'Physics',
                'grade_level': 'Class 11',
                'faculty': 'Science',
                'exam_type': 'Notes',
                'tags': 'Optics, Lens Maker Formula, Prism, Microscope, Unit 3, Derivation',
                'type': 'Note',
                'file_url': 'https://nebians.consica.com.np/static/web/mock/optics_derivations.pdf',
                'view_count': 1230,
                'like_count': 56,
            },
            {
                'title': 'Class 11 Physics Board Exam Question Paper - 2080 BS',
                'description': 'Board question paper of Class 11 Physics (NEB Science stream) held in 2080 BS.',
                'subject': 'Physics',
                'grade_level': 'Class 11',
                'faculty': 'Science',
                'exam_type': 'Board',
                'tags': 'Board Exam, Past Paper, 2080 BS, Physics, Mechanics, Thermodynamics',
                'type': 'PDF',
                'file_url': 'https://nebians.consica.com.np/static/web/mock/physics_2080_board.pdf',
                'view_count': 4150,
                'like_count': 176,
            },
        ]

        created_count = 0
        with transaction.atomic():
            for item in resources_data:
                # Check if this resource already exists by title
                if Resource.objects.filter(title=item['title']).exists():
                    continue
                
                Resource.objects.create(
                    id=str(uuid.uuid4()),
                    title=item['title'],
                    description=item['description'],
                    subject=item['subject'],
                    grade_level=item['grade_level'],
                    faculty=item['faculty'],
                    exam_type=item['exam_type'],
                    tags=item['tags'],
                    type=item['type'],
                    file_url=item['file_url'],
                    added_at=now,
                    view_count=item['view_count'],
                    like_count=item['like_count'],
                    source_type='admin',
                    uploaded_by=admin_user,
                    approval_status='approved',
                    is_lead=True
                )
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created_count} mock resources.'))

        # Seed SyllabusContent
        syllabus_data = [
            {
                'grade_level': 'Class 12',
                'subject': 'English',
                'chapter_id': 'the-selfish-giant',
                'chapter_title': 'Story 1: The Selfish Giant',
                'text_content': 'Theme:\nThe story reflects Oscar Wilde\'s view on love, charity, and Christian redemption.\n\nSummary:\nA selfish giant builds a wall to keep children out of his garden, bringing perpetual winter to his property. When he realizes his selfishness and allows them back in, spring returns instantly. A small child (representing Christ) blesses him for his kindness, and years later, takes the giant to his own garden—Paradise.',
                'question_answers': (
                    "Q1: Where did the children use to play?\n"
                    "The children used to play in the Giant's garden after returning from school. It was a large, lovely garden with soft green grass, peach trees, and sweet birds.\n\n"
                    "Q2: Why was the Giant called selfish?\n"
                    "The Giant was called selfish because he banned the children from playing in his garden, built a high wall all around it, and put up a sign that read 'Trespassers will be prosecuted'. He wanted the garden only for himself.\n\n"
                    "Q3: What happened in the Giant's garden when winter stayed there?\n"
                    "When winter stayed in the garden, spring and autumn did not visit it. Only snow, frost, north wind, and hail danced through the trees. The birds did not sing, and the trees forgot to blossom.\n\n"
                    "Q4: How did the Giant's heart melt at last?\n"
                    "The Giant's heart melted when he looked out of the window and saw a beautiful scene: children had crept in through a hole in the wall, and the trees were in blossom. He saw a tiny boy struggling to climb a tree and weeping. The Giant realized how selfish he had been and helped the boy, melting his heart."
                ),
                'order': 1
            },
            {
                'grade_level': 'Class 12',
                'subject': 'English',
                'chapter_id': 'the-oval-portrait',
                'chapter_title': 'Story 2: The Oval Portrait',
                'text_content': 'Theme:\nGothic story exploring the relationship between art and life.\n\nSummary:\nEdgar Allan Poe\'s story describes a painter who is so obsessed with creating a realistic portrait of his young bride that he ignores her presence. As he completes the masterpiece, he turns to look at his bride and discovers she is dead, showing that the art literally consumed her life force.',
                'question_answers': (
                    "Q1: Why did the painter paint his wife's portrait in a dark tower?\n"
                    "The painter wanted absolute control over light and environment to create his ultimate masterpiece, ignoring his wife's comfort in the cold, dark tower.\n\n"
                    "Q2: What is the relation between art and life in the story?\n"
                    "The story suggests a fatal relationship where art feeds on life. The painter transfers his wife's life force onto the canvas, killing the human being to give immortality to the portrait."
                ),
                'order': 2
            },
            {
                'grade_level': 'Class 12',
                'subject': 'English',
                'chapter_id': 'god-sees-the-truth',
                'chapter_title': 'Story 3: God Sees the Truth, but Waits',
                'text_content': 'Theme:\nFaith, forgiveness, and moral redemption.\n\nSummary:\nIvan Dmitrich Aksionov is falsely imprisoned for a merchant\'s murder in Siberia. After 26 years of prison labor, he meets the real killer, Semyonich. Aksionov protects Semyonich during a prison investigation, prompting Semyonich to confess. Aksionov forgives him and dies in peace just as his release order arrives.',
                'question_answers': (
                    "Q1: Why did Aksionov\'s wife warn him not to go to the fair?\n"
                    "Aksionov's wife warned him because she had a bad dream that he returned from the town with grey hair, which she interpreted as an evil omen.\n\n"
                    "Q2: Why did Semyonich decide to confess his crime?\n"
                    "Semyonich confessed because Aksionov saved him from being flogged by not telling the governor about the tunnel Semyonich dug, which deeply touched Semyonich's conscience."
                ),
                'order': 3
            },
            {
                'grade_level': 'Class 12',
                'subject': 'English',
                'chapter_id': 'boarding-house',
                'chapter_title': 'Story 5: The Boarding House',
                'text_content': 'Theme:\nSocial convention, entrapment, and marriage.\n\nSummary:\nMrs. Mooney runs a boarding house and manipulates Mr. Doran, a respectable clerk, into marrying her daughter Polly after they have a brief affair. Mr. Doran feels trapped by societal expectations and fear of losing his job, ultimately submitting to the marriage.',
                'order': 5
            },
            {
                'grade_level': 'Class 12',
                'subject': 'English',
                'chapter_id': 'scientific-research',
                'chapter_title': 'Essay 4: Scientific Research is a Token of Friendship',
                'text_content': 'Theme:\nThe value of scientific research in international relations.\n\nSummary:\nVladimir Keilis-Borok explains how science provides intellectual stimulation, solves global problems, and fosters deep cross-border friendships. It emphasizes that science belongs to humanity rather than any single nation.',
                'order': 18
            },
            {
                'grade_level': 'Class 12',
                'subject': 'English',
                'chapter_id': 'the-bull',
                'chapter_title': 'Play 1: The Bull',
                'text_content': 'Theme:\nSatire on the feudal society of 18th century Nepal.\n\nSummary:\nKing Ran Bahadur Shah\'s bull falls ill. The caretakers, Jit and Bir, are terrified of telling the king that the bull has died because the king loves the bull like a son. The play exposes the fear, flattery, and helplessness of subjects under a tyrannical ruler.',
                'question_answers': (
                    "Q1: Who was Jit and Bir?\n"
                    "Jit and Bir were the cowherds and caretakers of King Ran Bahadur Shah's royal bull.\n\n"
                    "Q2: Why were Jit and Bir terrified in the play?\n"
                    "They were terrified because the royal bull had died. The King was extremely fond of the bull and had declared that anyone who brought news of the bull's death would be executed. They were caught in a dilemma of how to report the situation without losing their heads.\n\n"
                    "Q3: How did they manage to escape the death penalty?\n"
                    "They escaped by reporting that the bull was extremely inactive, did not eat, and was sleeping with open eyes, rather than saying it was dead. The King decided to visit the bull himself, saw the truth, and declared it dead himself, thereby sparing Jit and Bir."
                ),
                'order': 20
            },
            {
                'grade_level': 'Class 12',
                'subject': 'English',
                'chapter_id': 'the-sandbox',
                'chapter_title': 'Play 2: The Sandbox',
                'text_content': 'Theme:\nAbsurdist critique of modern family dynamics and treatment of the elderly.\n\nSummary:\nEdward Albee\'s play critiques modern family dynamics, aging, and the treatment of the elderly. Mommy and Daddy bring Grandma to a beach sandbox to die, ignoring her presence until the Angel of Death arrives, satirizing the coldness of familial love in consumerist society.',
                'order': 21
            }
        ]

        syllabus_created = 0
        with transaction.atomic():
            for item in syllabus_data:
                obj, created = SyllabusContent.objects.update_or_create(
                    grade_level=item['grade_level'],
                    subject=item['subject'],
                    chapter_id=item['chapter_id'],
                    defaults={
                        'chapter_title': item['chapter_title'],
                        'text_content': item['text_content'],
                        'question_answers': item.get('question_answers', ''),
                        'order': item['order'],
                        'updated_at': now
                    }
                )
                if created:
                    obj.id = str(uuid.uuid4())
                    obj.created_at = now
                    obj.save()
                    syllabus_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated or seeded {len(syllabus_data)} syllabus content entries.'))
