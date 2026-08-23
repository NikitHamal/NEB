"""Curated feature catalog of NEBians for spotlight blogs and tutorials."""
import random
from typing import Dict, List, Optional

FEATURES = [
    {
        "id": "canvas",
        "title": "Neby Canvas — Interactive Knowledge Maps",
        "category": "update",
        "tagline": "Explore it. Prove it. Teach it.",
        "description": (
            "Neby Canvas allows students and teachers to turn complex subjects, derivations, "
            "and lessons into living, interactive knowledge maps. You can explore conceptual connections, "
            "add rich markdown notes, break down formulas step-by-step, and generate deep explorations with Neby AI."
        ),
        "highlights": [
            "Visual node canvas with custom colors, sticky notes, and connections",
            "Neby Explore: automatically expands prerequisite and advanced concepts",
            "Multi-format export and real-time auto-saving",
            "Minimalist, distraction-free study layout with dark mode support",
        ],
        "default_tags": "Canvas, Knowledge Maps, AI Learning, Study Tools, Visual Notes",
    },
    {
        "id": "3d_labs",
        "title": "Interactive 3D Labs & Physics Simulations",
        "category": "update",
        "tagline": "See formulas come to life in 3D real-time simulations.",
        "description": (
            "Visual interactive simulations designed specifically for NEB Physics and Biology topics. "
            "Students can interactively adjust parameters like gravity, resistance, charge, and focal length "
            "to understand the underlying physical laws before doing numerical problems."
        ),
        "highlights": [
            "Real-time 2D and 3D interactive physics engines (Projectile motion, Optics, Simple Harmonic Motion)",
            "Interactive Biology 3D anatomy and cellular structures",
            "Intuitive sliders to test hypotheses and verify textbook equations",
            "Mobile-optimized touch controls for tablets and smartphones",
        ],
        "default_tags": "3D Labs, Physics Simulations, Biology, Interactive Learning, NEB Science",
    },
    {
        "id": "pdf_reader",
        "title": "Smart PDF Reader with Annotation Tools",
        "category": "update",
        "tagline": "Read, highlight, and take notes directly inside NEB syllabus books.",
        "description": (
            "A fast, built-in PDF viewer engineered for NEB textbooks, question banks, and solution sets. "
            "Annotations (highlights, bookmarks, underlines, sticky notes) stay saved seamlessly on your device and account."
        ),
        "highlights": [
            "Multi-color highlights and custom note overlays",
            "Fast page jump, bookmarks, and full-screen reading mode",
            "Offline-first support for downloaded study resources",
            "Seamless dark mode reading to reduce eye strain during late-night revision",
        ],
        "default_tags": "PDF Reader, Ebooks, Annotations, Offline Study, NEB Textbooks",
    },
    {
        "id": "study_spaces",
        "title": "Study Spaces & Focus Timers",
        "category": "update",
        "tagline": "Boost your productivity with distraction-free Pomodoro study spaces.",
        "description": (
            "Study Spaces give students a structured environment to maintain deep focus. "
            "Equipped with customizable Pomodoro timers, ambient soundscapes, task checklists, and peer study rooms."
        ),
        "highlights": [
            "Customizable work/break intervals based on proven study techniques",
            "Integrated study checklists and session progress tracking",
            "Ambient soundscapes to improve focus and block distractions",
            "Peer study mode to study alongside classmates across Nepal",
        ],
        "default_tags": "Study Spaces, Pomodoro, Productivity, Focus, Exam Prep",
    },
    {
        "id": "cosmetics_store",
        "title": "Cosmetics Store & Profile Customization",
        "category": "general",
        "tagline": "Personalize your NEBians journey with exclusive themes, banners, and badges.",
        "description": (
            "Express your identity across the NEBians community! Earn rewards and unlock custom "
            "profile banners, glowing avatar borders, role badges, and app theme palettes."
        ),
        "highlights": [
            "Exclusive Material 3 dynamic color themes (OLED Dark, Cyberpunk, Forest, Sunset)",
            "Custom animated and illustrated profile banners",
            "Subject master badges and community achievement flair",
            "Reward-based unlocks from community participation and helpful answers",
        ],
        "default_tags": "Cosmetics, Profile, Themes, Badges, Community",
    },
    {
        "id": "forum_community",
        "title": "Community Forum & Peer Discussion",
        "category": "notice",
        "tagline": "Ask tough questions, share solutions, and learn together.",
        "description": (
            "The heart of NEBians — an open, supportive learning forum for students and educators in Nepal. "
            "Post difficult board exam questions, get step-by-step peer solutions, participate in polls, and collaborate."
        ),
        "highlights": [
            "Rich markdown & LaTeX math formula rendering for science and math equations",
            "Thumbs up voting, best answer pins, and helpful feedback",
            "Mention @all for broadcast announcements and @neby for instant peer insights",
            "Filter questions by subject, grade level (Class 11 & 12), and faculty",
        ],
        "default_tags": "Forum, Discussion, Question Bank, Peer Learning, NEB Community",
    },
]


def get_all_features() -> List[Dict]:
    return list(FEATURES)


def get_feature_by_id(feature_id: str) -> Optional[Dict]:
    for f in FEATURES:
        if f["id"] == feature_id:
            return f
    return None


def pick_random_feature(exclude_ids: List[str] = None) -> Dict:
    exclude = set(exclude_ids or [])
    available = [f for f in FEATURES if f["id"] not in exclude]
    if not available:
        available = FEATURES
    return random.choice(available)
