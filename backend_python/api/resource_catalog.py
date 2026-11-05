from django.core.cache import cache

from .models import Resource

DEFAULT_SUBJECTS = [
    'Physics', 'Chemistry', 'Mathematics', 'Biology', 'English', 'Nepali',
    'Computer Science', 'Economics', 'Accountancy', 'Business Studies',
    'Social Studies', 'History', 'Geography', 'Civics', 'Health & Physical Education',
    'Environment Science', 'Science', 'General Science', 'Life Science',
    'Physical Science', 'Earth Science', 'Applied Mathematics',
    'Business Mathematics', 'Statistics', 'Probability',
    'Microeconomics', 'Macroeconomics',
    'Financial Accounting', 'Cost Accounting', 'Auditing',
    'Marketing', 'Office Management', 'Hotel Management',
    'Computer Engineering', 'Electronics', 'Electrical Engineering',
    'Civil Engineering', 'Mechanical Engineering', 'Architecture',
    'Mechanics', 'Thermodynamics', 'Optics', 'Electricity & Magnetism',
    'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
    'Botany', 'Zoology', 'Genetics', 'Ecology',
    'English Grammar', 'English Literature', 'Creative Writing',
    'Nepali Grammar', 'Nepali Literature', 'Essay Writing',
    'Population Studies', 'Sociology', 'Psychology', 'Philosophy',
    'Education', 'Pedagogy', 'Curriculum Development',
    'Law', 'Constitutional Law', 'International Law',
    'Medicine', 'Pharmacy', 'Nursing', 'Public Health',
    'Agriculture', 'Forestry', 'Veterinary Science',
    'Management', 'Human Resource Management', 'Entrepreneurship',
    'Information Technology', 'Programming', 'Web Development',
    'Database Management', 'Networking', 'Cybersecurity',
    'Machine Learning', 'Artificial Intelligence', 'Data Science',
    'C Programming', 'C++ Programming', 'Python Programming', 'Java Programming',
    'Digital Logic', 'Operating Systems', 'Software Engineering',
    'Surveying', 'Estimating & Costing', 'Building Construction',
    'Fluid Mechanics', 'Strength of Materials', 'Engineering Drawing',
    'Purana Veda', 'Upanishad', 'Sanskrit', 'Maithili',
]

COMMON_TAGS = [
    'Board Exam', 'SEE', 'Past Paper', 'Model Paper', 'Solution',
    'Important Questions', 'Numerical', 'Derivation', 'Formula Sheet',
    'Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4', 'Chapter 5',
    'Chapter 6', 'Chapter 7', 'Chapter 8', 'Chapter 9', 'Chapter 10',
    'Unit 1', 'Unit 2', 'Unit 3', 'Unit 4', 'Unit 5',
    'Class 11', 'Class 12', 'Grade 11', 'Grade 12',
    'Science', 'Management', 'Humanities', 'Education', 'Law',
    'Final Exam', 'Midterm', 'Internal Assessment', 'Practical',
    'Old Course', 'New Course', 'Revised Syllabus', 'Curriculum',
    'Textbook', 'Reference Book', 'Guide', 'Notes', 'Summary',
    'Objective Questions', 'Subjective Questions', 'MCQ', 'Long Answer',
    'Short Answer', 'Very Short Answer', 'Essay Type',
    '2080 BS', '2081 BS', '2082 BS', '2079 BS',
    '2078 BS', '2077 BS', '2076 BS',
    'Kathmandu', 'Pokhara', 'Chitwan', 'Biratnagar', 'Butwal',
    'HSEB', 'TU', 'KU', 'PU', 'CTEVT',
    'Entrance', 'IOE', 'IOM', 'CEEE', 'KUUMAT',
    'C Programming', 'Python', 'Java', 'Web Development',
    'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
    'Mechanics', 'Optics', 'Thermodynamics', 'Electricity',
    'Calculus', 'Algebra', 'Trigonometry', 'Geometry', 'Statistics',
    'Botany', 'Zoology', 'Ecology', 'Genetics',
    'Nepali', 'English', 'Social Studies',
]

EDUCATION_LEVELS = [
    'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
    'Diploma', 'Bachelor', 'Master', 'PhD',
    'Entrance Prep', 'Competitive Exam', 'Other',
]

EXAM_TYPES = ['', 'Final', 'Midterm', 'Board', 'Entrance', 'SEE', 'Mock', 'Assignment', 'Notes', 'Reference', 'Other']

PRADESH_OPTIONS = [
    'Province 1', 'Madhesh', 'Bagmati', 'Gandaki', 'Lumbini', 'Karnali', 'Sudurpashchim',
]

RESOURCE_TYPES = ['PDF', 'Note', 'Video', 'Audio', 'Image', 'Link', 'Textbook', 'Past Paper', 'Model Paper', 'Guide', 'Solution', 'Presentation']


def known_subjects():
    def _resolver():
        subjects = set()
        for s_str in Resource.objects.values_list('subject', flat=True).distinct():
            for s in (s_str or '').split(','):
                if s.strip():
                    subjects.add(s.strip())
        return sorted(subjects)
    return cache.get_or_set('distinct_subjects', _resolver, 600)


def upload_form_options():
    return dict(
        subjects=sorted(set(DEFAULT_SUBJECTS + known_subjects())),
        education_levels=EDUCATION_LEVELS,
        exam_types=EXAM_TYPES,
        pradesh_options=PRADESH_OPTIONS,
        resource_types=RESOURCE_TYPES,
        common_tags=COMMON_TAGS,
    )
