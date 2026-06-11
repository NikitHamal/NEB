# NEBians — Next-Level Roadmap: 20 Ideas & Next Steps

This document captures concrete, prioritized ideas to take NEBians from a polished study hub to the leading learning platform for Nepali students. Each item lists the **why**, the **what**, and a pragmatic **first step** so any contributor (human or AI agent) can pick it up.

---

## Tier 1 — Highest leverage (do these first)

### 1. Spaced-Repetition Engine (SM-2) for Flashcards
**Why:** Flashcards already record confidence (hard/okay/easy) but reviews don't influence scheduling — students get no retention benefit.
**What:** Implement SM-2 (Anki's algorithm): per-card ease factor, interval, due date. Add a "Due today" queue on the Study Lab home and a daily review reminder notification.
**First step:** Add `ease_factor`, `interval_days`, `due_at` to `StudySpaceFlashcardReview`; compute next interval in `ajax_space_flashcard_review`.

### 2. Question Bank + Past-Paper Mock Exams
**Why:** NEB students obsess over past papers. The exam-mode timer now exists; the missing piece is real NEB-style question sets.
**What:** Curated question bank per subject/grade/chapter (seeded from past papers), blended with AI-generated questions. "Mock Exam" generates a full NEB-pattern paper (sections, marks weighting) with a timer and a printable result sheet.
**Why now:** This is the single biggest differentiator vs generic AI tools — it's Nepal-curriculum-specific.
**First step:** `QuestionBankItem` model (subject, grade, chapter, year, marks, type) + admin importer; exam composer view that mixes bank + AI questions.

### 3. Streaks, XP Levels & Daily Goals (Gamification v1)
**Why:** `contribution_score` exists but is invisible and unceremonious. Streaks are the cheapest retention feature in existence.
**What:** Daily study streak (any quiz/flashcard/summary activity counts), XP levels with named ranks ("Explorer → Scholar → NEBian Elite"), a weekly leaderboard reset, and streak-freeze items earned by consistency.
**First step:** `UserDailyActivity` table (user, date, actions); streak computation in `_build_local_stats`; streak flame in the topbar.

### 4. Study Space Templates & One-Click Setup
**Why:** New users face an empty space; activation suffers.
**What:** Templates per grade/subject ("Class 12 Physics — NEB") that pre-attach official syllabus resources from the Library, pre-generate a starter summary + 10-question diagnostic quiz, and suggest a learning path.
**First step:** `space_template` JSON fixtures + "Start from template" cards on the Study Lab landing page.

### 5. Async AI Generation with Job Queue + Live Progress
**Why:** Generation endpoints block an LSAPI worker for up to 2×120s. Under public load this is the #1 scaling bottleneck (rate limiting added, but the architecture is still synchronous).
**What:** A lightweight DB-backed job queue (or Redis + a single daemon worker, like the doc parser) for summary/mindmap/quiz/flashcards. Client gets a job id, progress streams over the existing WebSocket (`studyspace.<id>` channel: `generation.started/progress/completed`).
**First step:** `GenerationJob` model + a `run_generation_jobs` management command run via cron/daemon; views enqueue and return 202.

---

## Tier 2 — Product depth

### 6. AI Tutor Chat with Memory (threaded, streaming)
**Why:** The tutor is single-shot Q&A; students want a conversation that remembers context.
**What:** Persist tutor threads per space (reuse the Arena chat tables pattern), stream responses over SSE/WS, keep citations, and let the tutor reference the space's quiz mistakes ("You missed 3 questions on electrolysis — want me to explain?").
**First step:** `SpaceTutorThread`/`SpaceTutorMessage` models; reuse the SSE translator from `arena_views.py`.

### 7. Weak-Topic Analytics & Adaptive Quizzing
**Why:** Quiz attempts store per-question results but nothing aggregates them into insight.
**What:** Tag generated questions with a topic (ask the model for a `topic` field). Dashboard: accuracy by topic, trend over time. "Practice my weak areas" button generates a quiz weighted toward low-accuracy topics.
**First step:** Add `topic` to quiz question models + prompt; aggregate in the space analytics endpoint.

### 8. Collaborative Live Quiz Battles (Kahoot-style)
**Why:** Spaces already have presence + WebSockets. Synchronous group quizzing is wildly engaging for school groups.
**What:** Host starts a battle in a space; members join via invite code; questions appear simultaneously; live leaderboard between questions; XP rewards.
**First step:** `quiz_battle.*` WS events on the existing `studyspace.<id>` channel; a battle state machine in Redis.

### 9. Rich Collaborative Notes (CRDT or OT)
**Why:** Current notes are last-write-wins full-content overwrites — concurrent editing corrupts text and resets carets.
**What:** Move to Yjs (CRDT) over the existing WS, or minimally implement server-side diff-merge with version vectors. Add markdown preview and headings outline.
**First step:** Integrate `y-websocket`-compatible relay messages into `RealtimeConsumer` (binary payload passthrough on a `note.<space>` channel).

### 10. Mindmap v2 — Editable & Exportable
**Why:** Mindmaps are read-only AI output. Students learn by *making* maps.
**What:** Click-to-edit node titles, add/remove branches, drag to reorganize; AI "expand this branch" action; export PNG (exists) + SVG + Markdown outline. Persist user edits separately from the AI baseline.
**First step:** `mindmap_user_json` column; node edit popover in `study-mindmap.js`.

### 11. Offline-First PWA + Push Notifications
**Why:** Nepali students often study with unstable connectivity; the Android app exists but web reach is broader.
**What:** Service worker caching summaries/flashcards/quizzes for offline review; install prompt; web push for streak reminders and forum replies (FCM web).
**First step:** Workbox service worker for `/study-space/*` GET payloads + a manifest.json.

### 12. Teacher Dashboard & Assignments
**Why:** The teacher role exists with verification, but teachers have no tools — they're the strongest acquisition channel (1 teacher brings 40 students).
**What:** Teachers create a "classroom space", assign quizzes/flashcard decks with due dates, see a gradebook of member attempts, export CSV.
**First step:** `SpaceAssignment` model (space, quiz, due_at) + an "Assignments" tab gated by role; attempts already exist for grading.

---

## Tier 3 — Growth & platform

### 13. Public SEO Content from Generated Artifacts
**Why:** Organic search is free growth. Summaries/quizzes for common chapters are highly searchable ("NEB class 12 chemistry electrochemistry notes").
**What:** Owners can "Publish" a polished summary as a public, indexable page (`/notes/<grade>/<subject>/<slug>/`) with author credit, view counts, and a CTA to clone into your own Study Space. Moderation queue before indexing.
**First step:** `PublishedNote` model + sitemap entries + publish flow using the existing `publish_min_role` permission.

### 14. Nepali Language Mode (i18n + bilingual AI)
**Why:** Many NEB students study in Nepali medium; competitors are English-only.
**What:** Django i18n for UI strings; AI prompts accept `language: ne` for Nepali/bilingual summaries and explanations (the Qwen models handle Nepali reasonably; AI4Bharat arena models are Indic-focused).
**First step:** Add a `language` option to generation requests + a UI toggle; wrap templates in `{% trans %}` incrementally.

### 15. Resource Quality Loop: Ratings, Reports & Verified Badges
**Why:** As uploads open to the public, library quality will dilute.
**What:** 5-star ratings + "helpful" votes on resources, teacher-verified badge on vetted resources, auto-flagging of low-engagement uploads, and an uploader reputation score feeding `contribution_score`.
**First step:** `ResourceRating` model + aggregate columns (`rating_avg`, `rating_count`) maintained by `F()` updates.

### 16. Study Groups Calendar & Pomodoro Rooms
**Why:** The SaaS vision doc names pomodoro rooms; presence infrastructure is already live.
**What:** Scheduled group study sessions (calendar + reminders), a synchronized pomodoro timer per space (WS-broadcast start/break events), and "focus minutes" tracked into analytics/streaks.
**First step:** `pomodoro.start/tick/break` events on the space WS channel; timer UI in the space topbar.

### 17. Email Digests & Re-engagement
**Why:** No lifecycle emails exist; dormant users never come back.
**What:** Weekly digest (streak status, due flashcards, top forum posts in followed categories), triggered via a cron management command. Unsubscribe preferences in settings.
**First step:** `send_weekly_digest` management command reusing the existing SMTP setup + an `email_preferences` JSON field on User.

### 18. Full-Text Search with Meilisearch
**Why:** `icontains` LIKE-scans can't rank, typo-match, or scale past ~10k rows (already noted in AGENTS.md).
**What:** Self-hosted Meilisearch (single small process, cPanel-compatible) indexing resources, posts, published notes, and space titles; instant-search UI with highlighting; Nepali tokenization.
**First step:** `sync_search_index` management command + swap the `search()` view's resource/post queries behind a feature flag.

### 19. Billing-Ready Premium Tier (eSewa/Khalti)
**Why:** AI costs scale with usage; a sustainable model needs a premium tier with Nepali payment rails.
**What:** Free tier: N generations/day (rate limits already exist — reuse them as quota). Premium: higher limits, priority queue, exam-bank access, unlimited spaces. Integrate eSewa/Khalti checkout.
**First step:** `Subscription` model + plan-aware `_throttle` limits; eSewa sandbox integration behind a feature flag.

### 20. Observability & Quality Guardrails
**Why:** Going public means real traffic; today there's no error tracking, no slow-query visibility, and no AI-output quality measurement.
**What:** Sentry (self-hosted GlitchTip works on cheap VPS) for Django + JS errors; per-endpoint p95 timing middleware logged to Redis; AI generation telemetry (parse failure rate, dedupe hit rate, regeneration rate) on an admin dashboard; nightly `cleanup_stale_data` cron.
**First step:** Add GlitchTip DSN via env; a `TimingMiddleware` that logs >500ms requests; counter keys for AI parse failures (already structured in `qwen_utils/parsing.py`).

---

## Suggested sequencing (next 3 milestones)

| Milestone | Items | Theme |
|---|---|---|
| **M1 — Public-launch hardening** (1-2 weeks) | 5, 20, 15 | Survive traffic, keep quality |
| **M2 — Retention engine** (2-4 weeks) | 1, 3, 7, 11 | Make students come back daily |
| **M3 — Differentiation** (4-8 weeks) | 2, 12, 8, 13 | NEB-specific moats + viral loops |

---

*Generated as part of the Study Space revamp + backend hardening session. See `AGENTS.md` → Continuity Notes for what was shipped alongside this document.*