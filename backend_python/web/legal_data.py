"""Privacy Policy and Terms of Service for NEBians (Web, Android, and Desktop).

This module is the canonical source for the web legal pages (/privacy/ and /terms/)
and stays in lockstep with:
  * Android: app/src/main/java/com/neb/ians/ui/screens/legal/LegalContent.kt
  * Desktop: desktop/src/screens/legal_data.rs

Every section has a number, a slug id for anchor navigation, a title, and a list
of plain paragraphs (using **...** for inline bold emphasis so Android's
legalAnnotated(), Desktop's legal.rs, and Web's render_paragraph_html() all
render from the exact same text).
"""
from __future__ import annotations

import html
import json
import re

SITE = 'https://nebians.consica.com.np'
COMPANY = 'Consica Labs'
SUPPORT_EMAIL = 'support@nebians.consica.com.np'
SUBTITLE = 'NEBians Learning Platform • Nepal'
LAST_UPDATED = 'Last updated: November 2026'

PRIVACY_SECTIONS = [
    {
        'number': '1',
        'id': 'information-we-collect',
        'title': 'Information We Collect',
        'paragraphs': [
            'When you create or use an account on NEBians, we collect the information needed to operate your account and profile. Depending on how you sign in, this includes your display name, username, email address (and any pending email address awaiting verification), Google or GitHub account identifier if you use social sign-in, or a one-way password hash and hashed six-digit verification or reset codes if you use email sign-in. Passwords and verification codes are never stored in plaintext.',
            'You may optionally add profile, education, and portfolio details such as your role (Student, Teacher, Institution, or Explorer), profile photo, banner, or custom NEBians avatar settings, date of birth, gender, education level and status, program or course, academic term, completion year, subjects, teaching subjects, province, district, linked school or college, headline, skills, open-to preferences, bio, social links, and portfolio entries (courses, work, projects, and achievements).',
            'We also store the content and activity you create on the platform: forum posts, replies, polls and poll votes, uploaded study resources, resource requests, comments on resources and announcements, inline images, voice notes and media attachments, bookmarks, personal notes, Study Space or Canvas boards, and interactions with the Neby AI study assistant. If you connect a personal Bring-Your-Own-Key (BYOK) LLM provider, your API key is encrypted at rest using AES-GCM and only ever shown to you in masked form.',
            'If you apply to verify and claim an educational institution, we collect the applicant contact details (name, role, email, phone, registration number) and supporting verification documents, which are stored in private non-public storage accessible only to authorized staff reviewers. If you buy or sell paid study resources or courses in the Marketplace, we collect payment verification proofs (QR payment screenshots and eSewa, Khalti, Mobile Banking, or ConnectIPS transaction reference IDs) and seller payout account details solely to verify purchases, credit seller balances, and process withdrawals.',
        ],
    },
    {
        'number': '2',
        'id': 'device-signals-analytics-permissions',
        'title': 'Device Signals, Analytics & App Permissions',
        'paragraphs': [
            'NEBians measures post and resource reach, list impressions, and member analytics using first-party signals rather than third-party advertising trackers. In internal analytics and reach tables, viewer and actor identifiers are stored as one-way HMAC-SHA256 keyed tags (with guest viewer tags rotating daily) rather than raw IP addresses or advertising IDs. Coarse device attributes (device class, OS family, browser or app version, and country) power aggregate creator and member insights, while detailed device context in internal security rows is sealed with AES-GCM encryption.',
            'The NEBians Android app requests only the permissions required for its features: network access (INTERNET and ACCESS_NETWORK_STATE) to sync content and support offline caching; notifications (POST_NOTIFICATIONS and Firebase Cloud Messaging tokens) to deliver replies, announcements, and optional new-resource alerts; microphone access (RECORD_AUDIO) exclusively when you actively record a voice attachment in a comment or post composer (never in the background); and local on-device storage (Room database and file cache) for offline reading, notes, bookmarks, and downloaded PDFs.',
        ],
    },
    {
        'number': '3',
        'id': 'how-we-use-your-information',
        'title': 'How We Use Your Information',
        'paragraphs': [
            'We use the information we collect to operate, maintain, and improve NEBians: displaying your profile and academic portfolio; hosting and delivering library resources, forum discussions, polls, interactive lessons, NEB and SEE result lookups, and the Nepal Institutions Directory; and powering AI study features such as summaries, quizzes, flashcards, mindmaps, and Ask Neby.',
            'We also use your information to review teacher and institution verification claims, verify marketplace payment proofs and process seller withdrawals, send verification codes and service notifications (respecting quiet hours, daily caps, and your notification preferences), and protect platform security through rate limiting, WAF anti-abuse checks, and community moderation.',
        ],
    },
    {
        'number': '4',
        'id': 'information-sharing-visibility',
        'title': 'Information Sharing & Profile Visibility',
        'paragraphs': [
            '**We do not sell, rent, or trade your personal information to third parties or advertisers.** By default, public profile details such as your display name, username, role and verification badges, photo or avatar, bio, portfolio entries, and public contributions are visible to the community. If you post or comment using the anonymous option, your contribution is shown under an anonymized handle to other members.',
            'If you **lock your profile** in Settings, your personal details, portfolio entries, statistics, and activity are hidden from non-followers, new followers require your approval, and your profile page is excluded from search engine indexing. Your email address, pending email, password hash, verification code hashes, session tokens, encrypted BYOK API keys, private institution verification documents, and payment proof screenshots or payout details are never shared publicly. We may disclose information only when required by applicable law or valid legal process, or to protect the safety and rights of our members and platform.',
        ],
    },
    {
        'number': '5',
        'id': 'data-security',
        'title': 'Data Security',
        'paragraphs': [
            'We apply technical and organizational safeguards including HTTPS-only transport in production, CSRF and WAF challenge protections, one-way password and verification-code hashing, hashed bearer tokens for web and mobile sessions, AES-GCM encryption at rest for personal LLM keys and internal signal payloads, private filesystem storage for institution verification documents, rate limiting, and restricted staff-only administrative access. However, no method of electronic transmission or storage is 100% secure.',
        ],
    },
    {
        'number': '6',
        'id': 'your-choices-controls',
        'title': 'Your Choices & Controls',
        'paragraphs': [
            'You can edit your profile, role, education details, linked school, social links, and portfolio at any time from Edit Profile. From Settings on Web or Android, you can lock or unlock your profile to control visibility, approve or decline follow requests, toggle inline images in composers, switch new-resource push alerts on or off, manage or remove personal LLM provider keys, change your password, and request or cancel account deletion.',
        ],
    },
    {
        'number': '7',
        'id': 'data-retention-account-deletion',
        'title': 'Data Retention & Account Deletion',
        'paragraphs': [
            'We retain your account data for as long as your account remains active. You can request account deletion directly from Settings on the website or Android app. When you submit a deletion request, your account enters a **30-day grace period** during which you may cancel the request at any time to restore normal access.',
            'Once the 30-day window completes, your personal profile, photos, posts, replies, likes, follows, bookmarks, notifications, push tokens, edit history, and poll votes are permanently deleted from our databases. Any study resources or resource requests you uploaded remain in the library so other students do not lose access to educational materials, with all authorship permanently anonymized to **"Anonymous"**. Unreferenced inline content images older than 48 hours are purged automatically.',
        ],
    },
    {
        'number': '8',
        'id': 'childrens-privacy',
        'title': "Children's Privacy",
        'paragraphs': [
            'NEBians is designed for students, educators, and learners aged **13 and above**. We do not knowingly collect personal information from children under 13. If we learn that we have collected personal information from a child under 13, we will delete the account and associated data promptly.',
        ],
    },
    {
        'number': '9',
        'id': 'changes-to-this-policy',
        'title': 'Changes to This Policy',
        'paragraphs': [
            'We may update this Privacy Policy from time to time as NEBians adds features or updates its practices. We will notify you of significant changes by posting the updated policy on this page and in the app with a revised "Last updated" date.',
        ],
    },
    {
        'number': '10',
        'id': 'contact-us',
        'title': 'Contact Us',
        'paragraphs': [
            f'If you have questions about this Privacy Policy, your personal data, or a privacy request, please contact Consica Labs at {SUPPORT_EMAIL}.',
        ],
    },
]

TERMS_SECTIONS = [
    {
        'number': '1',
        'id': 'acceptance-of-terms',
        'title': 'Acceptance of Terms',
        'paragraphs': [
            'By accessing or using NEBians on the web, Android, or desktop, you agree to be bound by these Terms of Service and our Privacy Policy. If you do not agree to these terms, please do not use our services.',
        ],
    },
    {
        'number': '2',
        'id': 'description-of-service',
        'title': 'Description of Service',
        'paragraphs': [
            'NEBians (operated by Consica Labs) is an educational platform and learning community for students, teachers, institutions, and lifelong learners across Nepal, covering School (up to Class 10 / SEE), Plus Two (Class 11 and 12 / NEB), Diploma (CTEVT), Bachelor\'s, Master\'s, and Entrance Preparation. Core features include the study resource library (notes, past papers, solved books, syllabi), an interactive PDF and book reader with offline and read-aloud support, discussion forums and polls, AI study tools (Ask Neby, summaries, quizzes, flashcards, mindmaps, 3D labs, Study Spaces, and Canvas boards), the NEB and SEE Result Checker, the Nepal Institutions Directory, academic portfolios, and the Creator Marketplace.',
        ],
    },
    {
        'number': '3',
        'id': 'user-accounts-roles-verification',
        'title': 'User Accounts, Roles & Verification',
        'paragraphs': [
            'You may sign in using Google, GitHub, or an email and password account. You must be at least 13 years old to create an account. You are responsible for safeguarding your account credentials, verification codes, and password reset codes, and for all activity under your account.',
            'Account roles (Student, Teacher, Institution, Explorer) and verification badges (Verified, Teacher, Institution, Moderator, Admin) reflect community trust and manual verification. They cannot be bought, sold, or transferred. Applying to claim and verify an institution requires authority to represent that school, college, institute, or university and authentic supporting documentation. Impersonating an educator or institution or submitting altered documents will result in immediate revocation and account termination.',
        ],
    },
    {
        'number': '4',
        'id': 'user-content-uploaded-materials',
        'title': 'User Content & Uploaded Materials',
        'paragraphs': [
            'You retain ownership of original content you post or upload on NEBians, including forum posts, replies, polls, voice notes, portfolio entries, and study resources. By posting or uploading content, you grant NEBians a non-exclusive, worldwide, royalty-free license to host, store, format, index, display, and distribute that content for educational use across our web and mobile applications.',
            'You are solely responsible for any study notes, past papers, or other materials you upload. **These terms and responsibilities apply to both registered users and anonymous uploaders.** You represent and warrant that your uploads do not infringe any third-party intellectual property rights. Uploading pirated commercial textbooks, full commercial test-prep books, or proprietary publisher keys without authorization is strictly prohibited. The library is intended for self-authored notes, past examination papers, and educational resources shared in compliance with the Fair Use provisions of Nepal\'s Copyright Act, 2059.',
        ],
    },
    {
        'number': '5',
        'id': 'marketplace-paid-resources-courses',
        'title': 'Marketplace, Paid Resources, Courses & Payouts',
        'paragraphs': [
            'Members, verified teachers, and institutions in good standing may list paid study resources or courses (recorded, live, hybrid, or in-person) through the Creator Marketplace, either via on-platform QR checkout or direct contact inquiry. Sellers warrant that they hold all necessary rights to sell listed materials and will deliver advertised course sessions honestly. Once a buyer has paid for a resource, that resource cannot be deleted from buyer access.',
            'For on-platform purchases, buyers must submit genuine payment proof (a valid eSewa, Khalti, Mobile Banking, or ConnectIPS transaction reference ID and payment screenshot). Administrators verify payment proofs before unlocking buyer access and crediting seller earnings (net of applicable platform commission) to the seller\'s balance. Submitting fabricated, altered, or duplicate payment receipts is strictly prohibited and grounds for immediate account suspension. Sellers may request a payout withdrawal once their available balance reaches the minimum threshold of **NPR 1,000**.',
        ],
    },
    {
        'number': '6',
        'id': 'ai-study-tools-credits-byok',
        'title': 'AI Study Tools, Credits & Bring-Your-Own-Key',
        'paragraphs': [
            'AI-powered features on NEBians (Ask Neby, document summaries, generated quizzes, flashcards, mindmaps, and study assistants) are provided as study aids and may occasionally generate incomplete or inaccurate statements. You should verify formulas, definitions, and exam preparation against official textbooks and curricula.',
            'Members may use monthly free AI credits, persistent AI credits, or NEBians points according to platform rules, or optionally connect personal third-party LLM API keys (BYOK). When you use your own API key, your usage of that external provider remains subject to that provider\'s terms, rate limits, and billing.',
        ],
    },
    {
        'number': '7',
        'id': 'result-checker-directory-notices',
        'title': 'Result Checker, Syllabus & Institution Directory',
        'paragraphs': [
            'The NEB and SEE Result Checker, syllabus references, automated news and notice imports, and the Nepal Institutions Directory (compiled from OpenStreetMap under ODbL, Wikidata under CC0, and verified institution claims) are provided for informational and academic convenience. Official gradesheets, certificates, and institutional statuses are determined solely by the National Examinations Board (NEB), the Office of the Controller of Examinations (OCE), or the respective university or institution. External links to school websites or teacher contact channels lead to third-party sites that NEBians does not control.',
        ],
    },
    {
        'number': '8',
        'id': 'academic-integrity',
        'title': 'Academic Integrity',
        'paragraphs': [
            'NEBians is built to support genuine learning, not academic dishonesty. You must not use the platform to leak or circulate live examination question papers before or during an exam, coordinate live exam cheating, or misrepresent someone else\'s work as your own. We reserve the right to remove content and suspend accounts that violate academic integrity.',
        ],
    },
    {
        'number': '9',
        'id': 'prohibited-conduct',
        'title': 'Prohibited Conduct',
        'paragraphs': [
            'You agree not to: use NEBians for any unlawful purpose; harass, threaten, or defame other members; spam, flood, or abuse forums, comments, or resource requests; impersonate any person, teacher, or institution; upload malware, unsafe links, or destructive code; attempt unauthorized access to accounts, APIs, or administrative tools; bypass WAF challenges, rate limits, or profile privacy controls; artificially inflate views, likes, votes, or leaderboard scores; or scrape or bulk-harvest platform content without written permission.',
        ],
    },
    {
        'number': '10',
        'id': 'intellectual-property-takedown',
        'title': 'Intellectual Property & Takedown Policy',
        'paragraphs': [
            'The NEBians platform, including its M3X user interface design, brand marks, custom artwork, database schema, and source code, is protected by copyright and intellectual property laws of Nepal. Study resources and community posts remain the intellectual property of their respective creators or rights holders.',
            'As an educational intermediary platform, we respect intellectual property rights and comply with the Copyright Act, 2059 and the Electronic Transactions Act, 2063 of Nepal. If you believe that your copyrighted work has been uploaded or hosted on NEBians without authorization, please file a formal notice using our online Copyright Takedown Request Form. Upon review of a valid claim, we will promptly remove or disable access to the infringing material.',
        ],
    },
    {
        'number': '11',
        'id': 'disclaimer-of-warranties',
        'title': 'Disclaimer of Warranties',
        'paragraphs': [
            'NEBians is provided on an "as is" and "as available" basis without warranties of any kind, whether express or implied. We do not guarantee that the service will be uninterrupted, error-free, or immune from security incidents, nor do we warrant the completeness or accuracy of user-contributed or AI-generated content.',
        ],
    },
    {
        'number': '12',
        'id': 'limitation-of-liability',
        'title': 'Limitation of Liability',
        'paragraphs': [
            'To the fullest extent permitted by law, NEBians and Consica Labs shall not be liable for any indirect, incidental, special, consequential, or punitive damages, or any loss of data, academic standing, or revenue arising out of or related to your use of the service.',
        ],
    },
    {
        'number': '13',
        'id': 'termination-account-deletion',
        'title': 'Termination & Account Deletion',
        'paragraphs': [
            'We may suspend, restrict, or permanently ban your account at any time for violations of these Terms of Service. You may request account deletion at any time through Settings on the website or Android app. Upon requesting deletion, your account enters a 30-day grace period during which you may cancel the request to restore your account. After 30 days, your profile and forum activity are permanently erased, while any study resources you uploaded remain in the library under "Anonymous" authorship to preserve educational access for other students.',
        ],
    },
    {
        'number': '14',
        'id': 'governing-law-modifications-contact',
        'title': 'Governing Law, Modifications & Contact',
        'paragraphs': [
            f'These Terms of Service are governed by the laws of Nepal. We may update these terms from time to time by posting the revised version with an updated "Last updated" date; continued use of NEBians after changes take effect constitutes acceptance of the revised terms. For questions regarding these terms, please contact Consica Labs at {SUPPORT_EMAIL}.',
        ],
    },
]

_BOLD_RE = re.compile(r'\*\*(.+?)\*\*')


def render_paragraph_html(raw: str, *, takedown_url: str = '/copyright-takedown/') -> str:
    """Escape plain paragraph text and upgrade **bold**, support email, and takedown form links."""
    escaped = html.escape(raw, quote=True)
    escaped = _BOLD_RE.sub(r'<strong>\1</strong>', escaped)
    escaped = escaped.replace(
        SUPPORT_EMAIL,
        f'<a href="mailto:{SUPPORT_EMAIL}" class="lg-link">{SUPPORT_EMAIL}</a>',
    )
    escaped = escaped.replace(
        'Copyright Takedown Request Form',
        f'<a href="{html.escape(takedown_url, quote=True)}" class="lg-link">Copyright Takedown Request Form</a>',
    )
    return escaped


def _hydrate(sections: list[dict], *, takedown_url: str = '/copyright-takedown/') -> list[dict]:
    out = []
    for sec in sections:
        out.append({
            'number': sec['number'],
            'id': sec['id'],
            'title': sec['title'],
            'paragraphs': sec['paragraphs'],
            'html_paragraphs': [
                render_paragraph_html(p, takedown_url=takedown_url) for p in sec['paragraphs']
            ],
        })
    return out


def get_legal_document(key: str, *, takedown_url: str = '/copyright-takedown/') -> dict:
    if key == 'terms':
        sections = _hydrate(TERMS_SECTIONS, takedown_url=takedown_url)
        doc = {
            'key': 'terms',
            'title': 'Terms of Service',
            'seo_title': "Terms of Service — Nepal's Learning Community | NEBians",
            'description': (
                'NEBians Terms of Service — Rules, rights, marketplace terms, AI study tool guidelines, '
                'and responsibilities for students, teachers, and institutions using NEBians.'
            ),
            'subtitle': SUBTITLE,
            'last_updated': LAST_UPDATED,
            'contact_email': SUPPORT_EMAIL,
            'path': '/terms/',
            'canonical': f'{SITE}/terms/',
            'sections': sections,
        }
    else:
        sections = _hydrate(PRIVACY_SECTIONS, takedown_url=takedown_url)
        doc = {
            'key': 'privacy',
            'title': 'Privacy Policy',
            'seo_title': "Privacy Policy — Nepal's Learning Community | NEBians",
            'description': (
                'NEBians Privacy Policy — How Nepal\'s Learning Community collects, protects, encrypts, '
                'and gives you control over your account, profile, and study data across Web and Android.'
            ),
            'subtitle': SUBTITLE,
            'last_updated': LAST_UPDATED,
            'contact_email': SUPPORT_EMAIL,
            'path': '/privacy/',
            'canonical': f'{SITE}/privacy/',
            'sections': sections,
        }
    doc['jsonld'] = jsonld(doc)
    return doc


def get_takedown_document() -> dict:
    doc = {
        'key': 'takedown',
        'title': 'Copyright Takedown Request',
        'seo_title': "Copyright Takedown Request — Nepal's Learning Community | NEBians",
        'description': (
            "File a copyright takedown request under Nepal's Copyright Act, 2059 and Electronic "
            'Transactions Act, 2063 for any materials hosted on NEBians without authorization.'
        ),
        'path': '/copyright-takedown/',
        'canonical': f'{SITE}/copyright-takedown/',
    }
    doc['jsonld'] = jsonld(doc)
    return doc


def jsonld(doc: dict) -> str:
    """schema.org @graph for /privacy/, /terms/, and /copyright-takedown/."""
    url = doc['canonical']
    graph = [
        {
            '@type': 'WebPage',
            '@id': f'{url}#page',
            'url': url,
            'name': doc['seo_title'],
            'description': doc['description'],
            'inLanguage': 'en',
            'isPartOf': {'@type': 'WebSite', 'name': 'NEBians', 'url': f'{SITE}/'},
            'publisher': {'@type': 'Organization', 'name': COMPANY, 'url': f'{SITE}/about/'},
            'breadcrumb': {'@id': f'{url}#crumbs'},
        },
        {
            '@type': 'BreadcrumbList',
            '@id': f'{url}#crumbs',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'NEBians', 'item': f'{SITE}/'},
                {'@type': 'ListItem', 'position': 2, 'name': doc['title'], 'item': url},
            ],
        },
    ]
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, separators=(',', ':')).replace('<', '\\u003c')
