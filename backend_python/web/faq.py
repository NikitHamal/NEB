"""The FAQ, as data.

Three things read this: the page, the FAQPage structured data, and the client
side filter. Keeping the questions in one list rather than in markup means those
three can never disagree about what the answers are.

Answers are written as small HTML fragments because most of them need a link to
the page that actually does the thing. They are authored here and rendered with
`|safe`, so nothing user-supplied ever reaches them -- if that ever changes,
this is the file that has to stop being trusted.

`answer_text` is the plain-text version handed to Google; the schema wants the
answer, not our anchor tags.
"""
from __future__ import annotations

import re
from typing import Dict, List

_TAG = re.compile(r'<[^>]+>')


CATEGORIES: List[Dict] = [
    {
        'id': 'basics',
        'label': 'Getting started',
        'icon': 'explore',
        'blurb': 'What NEBians is, who it is for, and what it costs.',
        'questions': [
            {
                'q': 'What is NEBians?',
                'a': "NEBians is an open learning community in Nepal. It is three things at once: "
                     "a <a href=\"/library/\">library</a> of study material that anyone can read, a "
                     "<a href=\"/forum/\">forum</a> where students and teachers answer each other's "
                     "questions, and a set of AI study tools that turn a PDF into summaries, "
                     "mindmaps, quizzes and flashcards.",
            },
            {
                'q': 'Is NEBians free?',
                'a': "Yes. Reading, downloading, posting, and the AI study tools are all free. A small "
                     "number of resources are sold by the person who made them, and those are marked "
                     "with a price before you open them. Nothing else is behind a payment.",
            },
            {
                'q': 'Is NEBians only for NEB, or only for Classes 11 and 12?',
                'a': "No. NEB material is the largest part of the library because that is where it "
                     "started, but the platform is not scoped to it. There is material for SEE, for "
                     "bachelor-level courses, for entrance preparation and for subjects that sit "
                     "outside any board at all. Teachers, schools and self-taught learners all use it.",
            },
            {
                'q': 'Do I need an account to use NEBians?',
                'a': "Not to read. The library, subject pages, forum threads and the blog are open to "
                     "everyone without signing in. You need a free account to post, reply, upload, "
                     "bookmark, or use the AI study tools. "
                     "<a href=\"/auth/email/signup/\" rel=\"nofollow\">Create one here</a>.",
            },
            {
                'q': 'Is there a NEBians app?',
                'a': "Yes, for Android, on "
                     "<a href=\"https://play.google.com/store/apps/details?id=com.neb.ians\" "
                     "target=\"_blank\" rel=\"noopener\">Google Play</a>. It shares your account and "
                     "your bookmarks with the website, so you can start something on one and finish "
                     "it on the other.",
            },
        ],
    },
    {
        'id': 'study',
        'label': 'Finding study material',
        'icon': 'menu_book',
        'blurb': 'Past papers, model questions, notes and textbooks.',
        'questions': [
            {
                'q': 'Where can I find NEB past papers?',
                'a': "On the <a href=\"/past-papers/\">past papers page</a>, which is the library "
                     "filtered to board question papers. Narrow it by subject, grade and faculty from "
                     "the filter bar. If you would rather see one subject's papers, notes and "
                     "discussions together, open its subject page instead — for example "
                     "<a href=\"/subject/class-12/physics/\">Class 12 Physics</a>.",
            },
            {
                'q': 'Where are the NEB model questions and solutions?',
                'a': "On the <a href=\"/model-questions/\">model questions page</a>. Each set is "
                     "listed with the year and grade it belongs to, and many have worked solutions "
                     "attached by the member who uploaded them.",
            },
            {
                'q': 'How do I find notes for one specific subject?',
                'a': "Use the subject filter in the <a href=\"/library/\">library</a>, or go straight "
                     "to the subject page for your grade. Subject pages collect every resource type "
                     "for that subject in one place — notes, papers, solutions, and the threads people "
                     "have started about it.",
            },
            {
                'q': 'Can I download resources as PDF?',
                'a': "Most of them, yes. Whatever the uploader attached is what you get: usually a PDF, "
                     "sometimes images or a document. The download button sits on the resource page, "
                     "under the preview.",
            },
            {
                'q': 'Something I need is missing. Can I ask for it?',
                'a': "Yes — post it on the <a href=\"/requests/\">resource requests page</a>. "
                     "Requests are visible to everyone, and members upload against them regularly.",
            },
            {
                'q': 'How do I check my NEB or SEE result?',
                'a': "Use the <a href=\"/results/check/\">result checker</a>. Enter your symbol number "
                     "and date of birth and it will fetch your gradesheet. The "
                     "<a href=\"/results/\">results guide</a> explains grading, GPA and what to do "
                     "about a re-totalling request.",
            },
        ],
    },
    {
        'id': 'tools',
        'label': 'AI study tools',
        'icon': 'auto_awesome',
        'blurb': 'Study Lab, Canvas, and what the AI can and cannot do.',
        'questions': [
            {
                'q': 'What is Study Lab?',
                'a': "<a href=\"/study-lab/\">Study Lab</a> takes a document — yours, or anything in "
                     "the library — and builds study material from it: a summary, a mindmap of how the "
                     "ideas connect, a quiz that marks itself, and flashcards you can revise from. It "
                     "is meant for the night before, when reading forty pages again is not an option.",
            },
            {
                'q': 'What is Canvas?',
                'a': "<a href=\"/canvas/\">Canvas</a> is an infinite board for thinking on. You ask a "
                     "question, it answers in a card, and every card can branch into follow-up "
                     "questions that stay connected to where they came from. It is closer to a "
                     "conversation you can see all of at once than to a chat window.",
            },
            {
                'q': 'Can I trust the AI summaries and quizzes?',
                'a': "Treat them as a study aid, not as a source. They are generated from the document "
                     "you gave them and they are usually accurate, but they can misread a diagram, "
                     "flatten an exception, or state something with more confidence than it deserves. "
                     "Check anything you are going to be marked on against the original.",
            },
            {
                'q': 'What else is in the tools section?',
                'a': "The <a href=\"/tools/\">tools hub</a> has document conversion, text-to-speech, "
                     "transcription, and a few subject calculators. They are free and they do not "
                     "require anything beyond an account.",
            },
        ],
    },
    {
        'id': 'contribute',
        'label': 'Uploading and contributing',
        'icon': 'upload_file',
        'blurb': 'Sharing your own notes, and what happens after you do.',
        'questions': [
            {
                'q': 'How do I upload my notes?',
                'a': "Use the <a href=\"/upload/\">upload page</a>. Give the file a "
                     "clear title, pick the subject and grade, and say what kind of resource it is. "
                     "The better those three are, the more people find it.",
            },
            {
                'q': 'What can I upload?',
                'a': "Anything you made, or anything you have the right to share: your own notes, "
                     "solved past papers, question banks, presentations, lab reports. Board question "
                     "papers are public documents and are fine. Scanned copies of commercial textbooks "
                     "are not.",
            },
            {
                'q': 'How long does approval take?',
                'a': "A moderator looks at every upload before it goes public. Most are through within "
                     "a day. You will get a notification either way, and a rejected upload comes with "
                     "the reason so you can fix it and try again.",
            },
            {
                'q': 'Can I post or upload anonymously?',
                'a': "Yes. Both the composer and the upload form have an anonymous option. Your name "
                     "and photo are hidden from everyone reading it; moderators can still see who "
                     "posted, which is what keeps the option from being abused.",
            },
            {
                'q': 'Someone uploaded my copyrighted work. What do I do?',
                'a': "File a notice on the <a href=\"/copyright-takedown/\">copyright takedown page</a>. We act "
                     "on valid notices and remove the material; repeated infringement costs the "
                     "uploader their account.",
            },
        ],
    },
    {
        'id': 'community',
        'label': 'Community and the forum',
        'icon': 'forum',
        'blurb': 'Asking, answering, moderation and reputation.',
        'questions': [
            {
                'q': 'How does the forum work?',
                'a': "Ask a question or start a discussion in the <a href=\"/forum/\">forum</a>, tag "
                     "it with a subject, and anyone can reply. Replies thread, so a long answer and "
                     "the three follow-ups to it stay together instead of scattering.",
            },
            {
                'q': 'Who moderates NEBians?',
                'a': "A team of moderators, plus reports from members. Anything that breaks the "
                     "<a href=\"/terms/\">terms of service</a> — harassment, exam leaks, spam, "
                     "plagiarism — is removed. Report anything you see with the menu on the post.",
            },
            {
                'q': 'What are the badges next to some names?',
                'a': "They mark verified teachers, verified institutions, moderators and admins. "
                     "Verification is checked by hand and is not something you can buy or switch on "
                     "yourself.",
            },
            {
                'q': 'What is the leaderboard?',
                'a': "The <a href=\"/forum/leaderboard/\">leaderboard</a> ranks members by what they have "
                     "contributed — resources people use, answers people found helpful, discussions "
                     "that went somewhere. It is a thank-you, not a score you need.",
            },
        ],
    },
    {
        'id': 'account',
        'label': 'Account and privacy',
        'icon': 'shield_person',
        'blurb': 'Your profile, your data, and how to leave.',
        'questions': [
            {
                'q': 'Can I make my profile private?',
                'a': "Yes. Turn it on in <a href=\"/settings/\" rel=\"nofollow\">settings</a>. A "
                     "private profile is hidden from search engines and only approved followers can "
                     "see what you have posted.",
            },
            {
                'q': 'How do I change my username or photo?',
                'a': "From <a href=\"/profile/edit/\" rel=\"nofollow\">edit profile</a>. You can also "
                     "build a NEBians avatar there instead of uploading a photo.",
            },
            {
                'q': 'How do I delete my account?',
                'a': "In <a href=\"/settings/delete-account/\" rel=\"nofollow\">settings</a>. Deletion "
                     "removes your profile, posts, replies and uploads together — it is not a "
                     "deactivation, and it cannot be undone.",
            },
            {
                'q': 'What do you do with my data?',
                'a': "The <a href=\"/privacy/\">privacy policy</a> says exactly what is "
                     "collected and why. The short version: an account, what you post, and basic "
                     "usage analytics. We do not sell it.",
            },
        ],
    },
]


def _plain(html: str) -> str:
    return _TAG.sub('', html).replace('&amp;', '&').strip()


def all_questions() -> List[Dict]:
    """Flattened, with the category each one came from, for search and schema."""
    out = []
    for cat in CATEGORIES:
        for item in cat['questions']:
            out.append({
                'q': item['q'],
                'a': item['a'],
                'answer_text': _plain(item['a']),
                'category': cat['id'],
                'category_label': cat['label'],
            })
    return out


def question_count() -> int:
    return sum(len(c['questions']) for c in CATEGORIES)
