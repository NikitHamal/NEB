import re
from api.models import Resource

CURRICULUM_MAP = {
    ("Class 12", "English"): [
        {"id": "the-selfish-giant", "name": "Story 1: The Selfish Giant", "keywords": ["selfish giant", "selfish-giant"]},
        {"id": "the-oval-portrait", "name": "Story 2: The Oval Portrait", "keywords": ["oval portrait", "oval-portrait"]},
        {"id": "god-sees-the-truth", "name": "Story 3: God Sees the Truth, but Waits", "keywords": ["god sees the truth"]},
        {"id": "last-voyage", "name": "Story 4: The Last Voyage of the Ghost Ship", "keywords": ["last voyage", "ghost ship"]},
        {"id": "boarding-house", "name": "Story 5: The Boarding House", "keywords": ["boarding house", "boarding-house"]},
        {"id": "enormous-wings", "name": "Story 6: A Very Old Man with Enormous Wings", "keywords": ["enormous wings", "enormous-wings"]},
        {"id": "half-closed-eyes", "name": "Story 7: The Half-closed Eyes of the Buddha", "keywords": ["half closed eyes", "half-closed eyes"]},
        {"id": "corona-sonnets", "name": "Poem 1: A Corona of Sonnets", "keywords": ["corona of sonnets"]},
        {"id": "chimney-sweeper", "name": "Poem 2: The Chimney Sweeper", "keywords": ["chimney sweeper", "chimney-sweeper"]},
        {"id": "my-own-route", "name": "Poem 3: I Was My Own Route", "keywords": ["my own route", "my-own-route"]},
        {"id": "awakening-age", "name": "Poem 4: The Awakening Age", "keywords": ["awakening age", "awakening-age"]},
        {"id": "soft-storm", "name": "Poem 5: Soft Storm", "keywords": ["soft storm", "soft-storm"]},
        {"id": "sharing-tradition", "name": "Essay 1: Sharing Tradition", "keywords": ["sharing tradition", "sharing-tradition"]},
        {"id": "colored-me", "name": "Essay 2: How It Feels to Be Colored Me", "keywords": ["colored me", "colored-me"]},
        {"id": "on-libraries", "name": "Essay 3: On Libraries", "keywords": ["libraries", "on libraries", "on-libraries"]},
        {"id": "scientific-research", "name": "Essay 4: Scientific Research is a Token of Friendship", "keywords": ["scientific research", "scientific-research"]},
        {"id": "humility", "name": "Essay 5: Humility", "keywords": ["humility"]},
        {"id": "the-bull", "name": "Play 1: The Bull", "keywords": ["the bull"]},
        {"id": "the-sandbox", "name": "Play 2: The Sandbox", "keywords": ["sandbox", "the sandbox", "the-sandbox"]},
    ],
    ("Class 12", "Computer Science"): [
        {"id": "ch1-dbms", "name": "Chapter 1: Database Management System (DBMS)", "keywords": ["dbms", "database", "sql", "chapter 1"]},
        {"id": "ch2-networks", "name": "Chapter 2: Computer Network & Communication", "keywords": ["network", "osi model", "topology", "chapter 2"]},
        {"id": "ch3-web-tech", "name": "Chapter 3: Web Technology II (JS/PHP)", "keywords": ["web technology", "php", "javascript", "chapter 3"]},
        {"id": "ch4-cpp", "name": "Chapter 4: Object-Oriented Programming in C++", "keywords": ["oop", "c++", "chapter 4"]},
        {"id": "ch5-software-eng", "name": "Chapter 5: Software Engineering", "keywords": ["software engineering", "sdlc", "chapter 5"]},
        {"id": "ch6-dsa", "name": "Chapter 6: Data Structure & Algorithm (DSA)", "keywords": ["dsa", "data structure", "stack", "queue", "chapter 6"]},
        {"id": "ch7-system-design", "name": "Chapter 7: System Analysis & Design", "keywords": ["system analysis", "dfd", "chapter 7"]},
        {"id": "ch8-recent-trends", "name": "Chapter 8: Recent Trends in Technology", "keywords": ["recent trends", "ai", "cloud", "iot", "chapter 8"]},
    ],
    ("Class 11", "Physics"): [
        {"id": "unit1-mechanics", "name": "Unit 1: Mechanics", "keywords": ["mechanics", "vector", "projectile", "circular motion", "gravity", "elasticity", "unit 1"]},
        {"id": "unit2-thermodynamics", "name": "Unit 2: Heat & Thermodynamics", "keywords": ["thermodynamics", "heat", "carnot", "entropy", "calorimetry", "unit 2"]},
        {"id": "unit3-optics", "name": "Unit 3: Geometrical Optics", "keywords": ["optics", "prism", "lens", "microscope", "telescope", "unit 3"]},
        {"id": "unit4-electrostatics", "name": "Unit 4: Electrostatics", "keywords": ["electrostatics", "electric charge", "capacitance", "unit 4"]},
    ]
}

def get_grade_db_value(grade_slug):
    """Normalize URL grade slugs to DB values."""
    mapping = {
        "class-12": "Class 12",
        "class-11": "Class 11",
        "class-10-see": "Class 10 / SEE",
        "class-10": "Class 10 / SEE",
        "class-9": "Class 9",
        "class-8": "Class 8",
        "diploma": "Diploma",
        "bachelor": "Bachelor",
        "master": "Master",
        "phd": "PhD",
        "entrance-prep": "Entrance Prep",
        "competitive-exam": "Competitive Exam",
    }
    return mapping.get(grade_slug.lower().strip(), "Other")

def get_subject_db_value(subject_slug):
    """Normalize subject slug to exact DB case or name."""
    mapping = {
        "english": "English",
        "physics": "Physics",
        "chemistry": "Chemistry",
        "mathematics": "Mathematics",
        "math": "Mathematics",
        "biology": "Biology",
        "nepali": "Nepali",
        "computer-science": "Computer Science",
        "economics": "Economics",
        "accountancy": "Accountancy",
        "general": "General",
        "exam-tips": "Exam Tips",
    }
    val = mapping.get(subject_slug.lower().strip())
    if val:
        return val
    # Fallback to Title Case
    return subject_slug.replace("-", " ").title()

def get_chapters_for_subject(grade_db_val, subject_db_val):
    """Return list of chapter dicts for the specified grade and subject.
    
    Returns predefined chapters from CURRICULUM_MAP or empty list.
    """
    key = (grade_db_val, subject_db_val)
    if key in CURRICULUM_MAP:
        return CURRICULUM_MAP[key]
    return []

def slugify_tag(text):
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')
