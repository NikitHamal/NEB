"""GENERATED FILE. Do not hand-edit -- run tools/art/gensubjects.py.

The subject hue tables and family routing, shared with the app and with
neb-art.js. Imported by templatetags/web_extras.py.
"""
SUBJECT_HUES = {
    "Physics": ("#1D4ED8", "#DBE7FE", "#1B3FA8", "#9DBBFF", "#1B2A4D", "#D6E3FF"),
    "Chemistry": ("#15803D", "#DCFCE7", "#14602F", "#7CD9A0", "#14301F", "#D3F5DF"),
    "Mathematics": ("#B91C1C", "#FEE2E2", "#8F1717", "#FF9C93", "#3A1A18", "#FFDAD6"),
    "Biology": ("#0F766E", "#CCFBF1", "#0C5B55", "#5FD3C4", "#10302D", "#CDF3ED"),
    "English": ("#7E22CE", "#F3E8FF", "#631AA3", "#D3B4FE", "#2C1A44", "#EDE0FF"),
    "Nepali": ("#9A6206", "#FEF3C7", "#7A4E05", "#E8B457", "#32260E", "#F7E6C2"),
    "Computer Science": ("#0E7490", "#CFFAFE", "#0B5A70", "#5CC8E0", "#0E2C36", "#C9EFF8"),
    "Economics": ("#C2410C", "#FFEDD5", "#9A330A", "#FFA76B", "#3A2013", "#FFE0CB"),
    "Accountancy": ("#9D174D", "#FCE7F3", "#7D1240", "#F79CC0", "#3A1428", "#FBDCE9"),
    "Exam Tips": ("#6D28D9", "#EDE9FE", "#56209F", "#C4B5FD", "#261C46", "#E6E0FF"),
}

FAMILY_HUES = {
    "PHYSICS": ("#1D4ED8", "#DBE7FE", "#1B3FA8", "#9DBBFF", "#1B2A4D", "#D6E3FF"),
    "CHEMISTRY": ("#15803D", "#DCFCE7", "#14602F", "#7CD9A0", "#14301F", "#D3F5DF"),
    "MATH": ("#B91C1C", "#FEE2E2", "#8F1717", "#FF9C93", "#3A1A18", "#FFDAD6"),
    "BIOLOGY": ("#0F766E", "#CCFBF1", "#0C5B55", "#5FD3C4", "#10302D", "#CDF3ED"),
    "LANGUAGE": ("#7E22CE", "#F3E8FF", "#631AA3", "#D3B4FE", "#2C1A44", "#EDE0FF"),
    "COMPUTING": ("#0E7490", "#CFFAFE", "#0B5A70", "#5CC8E0", "#0E2C36", "#C9EFF8"),
    "COMMERCE": ("#C2410C", "#FFEDD5", "#9A330A", "#FFA76B", "#3A2013", "#FFE0CB"),
    "EXAM": ("#6D28D9", "#EDE9FE", "#56209F", "#C4B5FD", "#261C46", "#E6E0FF"),
    "SCIENCE": ("#047857", "#D1FAE5", "#04604A", "#6EDCB4", "#0D2E25", "#CFF5E6"),
    "SOCIAL": ("#3F5A8A", "#DDE6F6", "#2C4066", "#9CB7E8", "#1B2638", "#D9E4F7"),
    "HEALTH": ("#BE123C", "#FFE4E9", "#8F0E2E", "#FF9BB0", "#3D1520", "#FFD9E1"),
    "GENERAL": ("#004AC6", "#DBE1FF", "#00174B", "#B4C5FF", "#22324C", "#DBE1FF"),
}

# Ordered: the first family whose keyword appears in the subject wins, so a
# string like "Health and Physical Education" cannot be claimed by LANGUAGE
# on the word "education" before HEALTH has had a look at it.
FAMILY_KEYWORDS = (
    ("HEALTH", ("health", "physical education", "phy. edu", "hpe", "sport", "fitness", "nutrition", "yoga", "स्वास्थ्य",)),
    ("EXAM", ("exam tip", "exam prep", "entrance", "model paper", "model set", "past paper", "question bank", "mock test", "revision",)),
    ("COMPUTING", ("computer", "software", "programming", "informatics", "information tech", "digital", "coding", "algorithm", "database", "web dev",)),
    ("PHYSICS", ("physics", "भौतिक",)),
    ("CHEMISTRY", ("chemistry", "chemical", "रसायन",)),
    ("MATH", ("math", "algebra", "geometry", "trigonometry", "calculus", "statistic", "गणित",)),
    ("BIOLOGY", ("biology", "botany", "zoology", "microbio", "anatomy", "genetic", "जीव",)),
    ("SOCIAL", ("social", "history", "geography", "civic", "population", "culture", "सामाजिक", "अध्ययन",)),
    ("COMMERCE", ("economic", "account", "business", "finance", "commerce", "marketing", "banking", "book keeping", "bookkeeping", "अर्थ",)),
    ("LANGUAGE", ("english", "nepali", "literature", "grammar", "language", "sanskrit", "hindi", "maithili", "newari", "writing", "नेपाली", "अंग्रेजी", "साहित्य",)),
    ("SCIENCE", ("science", "environment", "astronomy", "geology", "laboratory", "विज्ञान",)),
)

SUBJECT_ICONS = {
    "Physics": "science",
    "Chemistry": "biotech",
    "Mathematics": "calculate",
    "Biology": "eco",
    "English": "menu_book",
    "Nepali": "translate",
    "Computer Science": "computer",
    "Economics": "trending_up",
    "Accountancy": "account_balance",
    "Exam Tips": "quiz",
}

FAMILY_ICONS = {
    "PHYSICS": "science",
    "CHEMISTRY": "biotech",
    "MATH": "calculate",
    "BIOLOGY": "eco",
    "LANGUAGE": "menu_book",
    "COMPUTING": "computer",
    "COMMERCE": "trending_up",
    "EXAM": "quiz",
    "SCIENCE": "travel_explore",
    "SOCIAL": "public",
    "HEALTH": "favorite",
    "GENERAL": "category",
}

_LOWER = {k.lower(): k for k in SUBJECT_HUES}


def subject_family(subject):
    """The family a subject belongs to. Mirrors neb-art.js `subjectFamily` and
    the app's `subjectFamily`, keyword table and order included."""
    s = (subject or "").lower().strip()
    if not s:
        return "GENERAL"
    for fam, kws in FAMILY_KEYWORDS:
        for kw in kws:
            if kw in s:
                return fam
    return "GENERAL"


def subject_key(subject):
    """The exact named subject, if this is one; otherwise None."""
    s = (subject or "").strip()
    return _LOWER.get(s.lower())


def subject_hue(subject):
    """The six-value hue tuple: light, lightContainer, onLightContainer, then
    the same three for dark."""
    key = subject_key(subject)
    if key:
        return SUBJECT_HUES[key]
    return FAMILY_HUES.get(subject_family(subject), FAMILY_HUES["GENERAL"])


def subject_slug(subject):
    """The CSS class suffix, matching a block in material3/06-subject-tokens.css.
    A named subject gets its own; anything else gets its family's."""
    key = subject_key(subject)
    if key:
        import re
        return re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-")
    return "fam-" + subject_family(subject).lower()


def subject_icon(subject):
    key = subject_key(subject)
    if key:
        return SUBJECT_ICONS[key]
    return FAMILY_ICONS.get(subject_family(subject), "category")
