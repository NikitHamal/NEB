# Privacy Policy & Terms of Service: status

Single status doc for the legal review and M3X revamp across Web, Android, and Desktop. Read before editing `/privacy/`, `/terms/`, `/copyright-takedown/`, `LegalContent.kt`, or `legal_data.rs`; extend this file in place rather than creating a second one.

## Codebase audit findings

1. **Outdated date & missing platform capabilities (May 2026 -> November 2026)**:
   - The previous 9-section Privacy Policy and 12-section Terms of Service only described basic Google/email login, forum posts, and library PDFs.
   - Missing from Privacy Policy:
     * **GitHub OAuth** sign-in and pending email verification (`pending_email`) with hashed 6-digit verification/reset codes (`verification_code`).
     * **Roles, Education & Portfolio** (`role`: Student, Teacher, Institution, Explorer; `edu_status`, `edu_program`, `edu_term`, `edu_completed`, `headline`, `skills`, `open_to`, `SocialLink`, `ProfileEntry`, custom NEBians avatar settings, and `school_slug`).
     * **Content, Media & Study Tools**: polls and poll votes (`Poll`, `PollVote`), resource requests (`ResourceRequest`), inline images (`ContentImage` with 48-hour unused cleanup), voice notes/media attachments (`PostMedia`, `ResourceCommentMedia`, `BlogCommentMedia`), personal notes, Study Spaces/Canvas boards, and Neby AI study interactions.
     * **BYOK LLM API Keys (`UserLLMProvider`)**: personal API keys are encrypted at rest with **AES-GCM** (`api.llm.crypto`) and only returned in masked form.
     * **Institution Verification (`InstitutionVerification`, `InstitutionDocument`)**: applicant contact details, registration number, and verification documents stored in private non-public storage (`private_storage`) restricted to staff reviewers.
     * **Marketplace & Payouts (`PaymentVerification`, `SellerBalance`, `WithdrawalRequest`)**: QR payment screenshots, eSewa/Khalti/Mobile Banking/ConnectIPS transaction reference IDs, and seller payout details.
     * **First-Party Reach, Signals & Android Permissions (`PostReach`, `ResourceReach`, `ActorSignal`, `DeviceSignalInterceptor.kt`, `AndroidManifest.xml`)**: one-way **HMAC-SHA256** keyed viewer/actor tags (daily-rotating guest tags, no raw IPs or advertising IDs in reach/signal rows), **AES-GCM** sealed device context in `ActorSignal`, and Android permissions (`INTERNET`, `ACCESS_NETWORK_STATE`, `POST_NOTIFICATIONS` / `FCMToken`, `RECORD_AUDIO` strictly on active user voice-note recording, and local Room/file offline storage).
   - Missing from Terms of Service:
     * **Roles & Teacher/Institution Verification** rules and anti-impersonation / anti-forgery terms.
     * **Creator Marketplace, Paid Resources, Courses & Seller Payouts** (`recorded`, `live`, `hybrid`, `inperson` delivery; `buy` QR checkout vs. `contact` mode; prohibition on deleting resources after a buyer has paid; prohibition on fake/duplicate payment receipts; **NPR 1,000** minimum withdrawal threshold).
     * **AI Study Tools, Credits & BYOK** accuracy disclaimer and credit/BYOK terms.
     * **NEB & SEE Result Checker, Syllabus & Nepal Institutions Directory** (OpenStreetMap ODbL + Wikidata CC0 + verified claims) official-source disclaimers and third-party link notices.
2. **Markup & M3X defects fixed**:
   - `terms.html` previously rendered raw markdown asterisks (`**These terms and responsibilities apply to both registered users and anonymous uploaders.**`) as literal `**` in HTML.
   - `privacy.html` and `terms.html` relied entirely on inline `style="..."` attributes with no section navigation or document switcher.
   - `takedown.html` and `web-takedown.css` used `box-shadow` elevations, inline `style="..."` attributes, a `http://localhost:8000/...` placeholder, and a typo (`"Electronic signature signature is required."`).
   - `seo.py` listed `/app/privacy/`, `/app/terms/`, and `/app/copyright/` in `STATIC_PAGES`, which were unrouted; `seo.py` now lists canonical `/privacy/`, `/terms/`, and `/copyright-takedown/`, and `web/urls.py` permanently redirects `/app/privacy/`, `/app/terms/`, and `/app/copyright/` to the canonical URLs.
   - `faq.py` previously stated that account deletion had no deactivation window and deleted uploaded resources; it now matches `delete_user_account()` in `api/services.py` (30-day cancellation grace period + anonymization of uploaded library resources to `"Anonymous"`).
   - `_auth_social.html` on Web now includes the Terms of Service & Privacy Policy notice matching Android (`AuthActionButtons.kt`) and Desktop (`login.rs`).

## Shipped across Web, Android, and Desktop

| Platform | Files | Details |
| --- | --- | --- |
| **Web (Canonical Source + UI)** | `backend_python/web/legal_data.py`, `backend_python/web/views_public.py`, `backend_python/web/templates/web/legal/_document.html`, `privacy.html`, `terms.html`, `takedown.html`, `delete_account.html`, `delete_account_success.html`, `backend_python/web/static/web/css/pages/web-legal.css`, `web-takedown.css` | 10-section Privacy Policy and 14-section Terms of Service (`Last updated: November 2026`), schema.org JSON-LD (`WebPage` + `BreadcrumbList`), `.neb-back` standard circle, M3X segmented switcher (`Privacy Policy` / `Terms of Service` / `Copyright`), sticky section rail, M3X account deletion pages, zero inline styles, zero shadows/gradients/emojis. |
| **Android** | `app/src/main/java/com/neb/ians/ui/screens/legal/LegalContent.kt`, `LegalScreen.kt`, `app/src/main/java/com/neb/ians/ui/screens/auth/AuthLegalSheet.kt`, `app/src/main/java/com/neb/ians/ui/screens/settings/DeleteAccountScreen.kt` | Exact section-for-section and paragraph-for-paragraph parity with `web/legal_data.py`; `LegalDocSwitcher` segmented pill bar in both `LegalScreen` and `AuthLegalSheet` so users can switch between Privacy Policy and Terms of Service in place; `nebFloatColor()` / `nebFloatLine()` M3X sheet tokens; Outlined icons on `DeleteAccountScreen`; clickable `mailto:` contact card. |
| **Desktop** | `desktop/src/screens/legal_data.rs` | Updated `PRIVACY` (10 sections) and `TERMS` (14 sections) in lockstep with `LegalContent.kt` and `web/legal_data.py`. |

## Verify

```bash
cd backend_python
export DEBUG=True DB_ENGINE=sqlite SECRET_KEY=x
python3 manage.py test web.test_legal web.test_back_standard web.test_icon_font web.test_auth_pages web.test_about
python3 ../tools/css/bundle.py --check
```
