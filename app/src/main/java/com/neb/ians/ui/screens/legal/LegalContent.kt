package com.neb.ians.ui.screens.legal

import androidx.compose.runtime.Immutable

@Immutable
data class LegalSection(
    val number: String,
    val title: String,
    val paragraphs: List<String>
)

@Immutable
data class LegalDocument(
    val key: String,
    val title: String,
    val subtitle: String,
    val lastUpdated: String,
    val sections: List<LegalSection>,
    val contactEmail: String,
    val webUrl: String
)

object NebLegal {

    const val PRIVACY = "privacy"
    const val TERMS = "terms"

    private const val SUPPORT_EMAIL = "support@nebians.consica.com.np"

    val privacyPolicy = LegalDocument(
        key = PRIVACY,
        title = "Privacy Policy",
        subtitle = "NEBians Learning Platform • Nepal",
        lastUpdated = "Last updated: May 2026",
        contactEmail = SUPPORT_EMAIL,
        webUrl = "https://nebians.consica.com.np/privacy/",
        sections = listOf(
            LegalSection(
                "1",
                "Information We Collect",
                listOf(
                    "When you create or use an account, we collect the information needed to operate your account. This may include your name, username, email address, Google account ID if you use Google sign-in, profile photo, and optional profile details such as date of birth, gender, class level, subjects, province, district, school, and bio. If you use email/password sign-in, passwords are stored only as one-way password hashes, not as plaintext."
                )
            ),
            LegalSection(
                "2",
                "How We Use Your Information",
                listOf(
                    "We use your information to provide and improve NEBians services: displaying your profile, enabling forum discussions, personalizing content, and communicating with you about your account or our services."
                )
            ),
            LegalSection(
                "3",
                "Information Sharing",
                listOf(
                    "We do not sell your personal information. Public profile information such as display name, username, photo, and bio may be visible to other users. If you lock your profile, personal details, stats, and activity are hidden from other users. Your email address, password hash, reset/verification code hashes, and account identifiers are not shared publicly. We may share information if required by law or to protect our rights."
                )
            ),
            LegalSection(
                "4",
                "Data Security",
                listOf(
                    "We use security controls such as HTTPS-only production cookies, CSRF protection, password hashing, verification-code expiry, rate limits, and restricted administrative access. However, no method of electronic transmission or storage is 100% secure."
                )
            ),
            LegalSection(
                "5",
                "Your Choices",
                listOf(
                    "You can edit profile information from the Edit Profile page, lock your profile to make personal details private, and change your password if you use email/password sign-in. You can request account deletion directly through your profile settings page in the application or website."
                )
            ),
            LegalSection(
                "6",
                "Data Retention and Deletion",
                listOf(
                    "We retain your account data for as long as your account is active. If you request account deletion, your personal profile, posts, comments, replies, bookmarks, and activity history will be permanently deleted after a 30-day processing window. Any study resources you uploaded will remain in the library to preserve access for other students, but all references to your authorship will be permanently anonymized (assigned to \"Anonymous\")."
                )
            ),
            LegalSection(
                "7",
                "Children's Privacy",
                listOf(
                    "NEBians is designed for users aged 13 and above. We do not knowingly collect personal information from children under 13. If we learn that we have collected data from a child under 13, we will delete it promptly."
                )
            ),
            LegalSection(
                "8",
                "Changes to This Policy",
                listOf(
                    "We may update this privacy policy from time to time. We will notify you of significant changes by posting the updated policy on this page with a new \"Last updated\" date."
                )
            ),
            LegalSection(
                "9",
                "Contact Us",
                listOf(
                    "If you have questions about this privacy policy or your data, please contact us at $SUPPORT_EMAIL."
                )
            )
        )
    )

    val termsOfService = LegalDocument(
        key = TERMS,
        title = "Terms of Service",
        subtitle = "NEBians Learning Platform • Nepal",
        lastUpdated = "Last updated: May 2026",
        contactEmail = SUPPORT_EMAIL,
        webUrl = "https://nebians.consica.com.np/terms/",
        sections = listOf(
            LegalSection(
                "1",
                "Acceptance of Terms",
                listOf(
                    "By accessing or using NEBians, you agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use our services."
                )
            ),
            LegalSection(
                "2",
                "Description of Service",
                listOf(
                    "NEBians is a free educational platform for students and teachers of all classes and faculties. We provide study resources (ebooks, PDFs, notes), a discussion forum, and a PDF/resource viewer. The service is provided free of charge."
                )
            ),
            LegalSection(
                "3",
                "User Accounts",
                listOf(
                    "You may sign in with Google or with an email/password account, depending on the options available on NEBians. You are responsible for maintaining the security of your account and must not share credentials, verification codes, or reset codes with others. You must be at least 13 years old to create an account."
                )
            ),
            LegalSection(
                "4",
                "User Content & Uploaded Materials",
                listOf(
                    "You retain ownership of content you post or upload on NEBians (forum posts, replies, profile information, and study resources). By posting or uploading content, you grant NEBians a non-exclusive, royalty-free, worldwide license to display, host, distribute, and format that content for educational, non-commercial use on our platform.",
                    "You are solely responsible for any study notes, model papers, or other resources you upload. **These terms and responsibilities apply to both registered users and anonymous uploaders.** You represent and warrant that your uploads do not violate any intellectual property rights of others. Uploading full commercial textbooks, question sets, or copyrighted keys of commercial publishers is strictly prohibited. The platform is designed solely for sharing self-created notes, past papers, or public/educational resources in compliance with the Fair Use provisions of Nepal's Copyright Act, 2059."
                )
            ),
            LegalSection(
                "5",
                "Academic Integrity",
                listOf(
                    "NEBians is designed to support learning, not to facilitate academic dishonesty. You must not use the platform to share exam questions before an exam, distribute answer keys, or engage in any form of cheating. We reserve the right to remove content that violates academic integrity."
                )
            ),
            LegalSection(
                "6",
                "Prohibited Conduct",
                listOf(
                    "You agree not to: use the service for any unlawful purpose; attempt to gain unauthorized access to any portion of the service or administrative tools; interfere with or disrupt the service or servers; spam, flood, or otherwise abuse the forum; impersonate any person or entity; upload viruses, malicious files, unsafe links, or code; scrape or collect data without permission; or bypass profile privacy controls."
                )
            ),
            LegalSection(
                "7",
                "Intellectual Property & Takedown Policy",
                listOf(
                    "The NEBians platform, including its user interface design, logo, database schema, and source code, is protected by copyright and intellectual property laws of Nepal. Study resources and files shared on the platform remain the intellectual property of their respective creators or owners.",
                    "As an intermediary educational platform, we respect intellectual property rights and comply with the Copyright Act, 2059 and the Electronic Transactions Act, 2063 of Nepal. We do not pre-screen all user contributions but will act promptly upon receiving valid copyright notifications. If you believe that your copyrighted work has been uploaded or hosted on NEBians without authorization, please file a formal claim using our online Copyright Takedown Request Form. Upon review of a valid claim, we will remove or restrict access to the infringing material."
                )
            ),
            LegalSection(
                "8",
                "Disclaimer of Warranties",
                listOf(
                    "NEBians is provided \"as is\" without warranties of any kind. We do not guarantee that the service will be uninterrupted, secure, or error-free. We do not warrant the accuracy, completeness, or usefulness of any content on the platform."
                )
            ),
            LegalSection(
                "9",
                "Limitation of Liability",
                listOf(
                    "In no event shall NEBians be liable for any indirect, incidental, special, consequential, or punitive damages arising out of your use of the service, even if we have been advised of the possibility of such damages."
                )
            ),
            LegalSection(
                "10",
                "Modifications",
                listOf(
                    "We reserve the right to modify these terms at any time. Continued use of the service after modifications constitutes acceptance of the updated terms. We will make reasonable efforts to notify you of significant changes."
                )
            ),
            LegalSection(
                "11",
                "Termination & Account Deletion",
                listOf(
                    "We may suspend or terminate your account at any time for violation of these terms. You may request account deletion at any time through your profile settings page. Upon requesting deletion, your account is immediately deactivated and will be permanently deleted after a 30-day grace period. During this period, you may cancel the request to restore your account. Please note that while your profile and forum activity will be permanently erased, any study resources you uploaded will remain in the library but will be completely anonymized to preserve educational content access for other users."
                )
            ),
            LegalSection(
                "12",
                "Contact",
                listOf(
                    "For questions about these terms, please contact us at $SUPPORT_EMAIL."
                )
            )
        )
    )

    fun documentFor(key: String): LegalDocument = when (key) {
        TERMS -> termsOfService
        else -> privacyPolicy
    }
}
