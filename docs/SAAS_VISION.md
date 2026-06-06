# NEBians — The SaaS Vision
## Transforming from a Static Content Hub to an Interactive Academic Workspace

### 1. Introduction & Philosophy
NEBians was originally conceived as a modern study resource repository (PDF reader, offline-first notes) and community forum. However, to realize its full potential and deliver maximum value to the academic ecosystem of Nepal, the platform is transitioning into a **Web Software / SaaS (Software as a Service)**.

Instead of a passive website where files are merely viewed or downloaded, NEBians will behave as a **live educational operating system**. It will serve as an active utility platform that students, teachers, and institutions "live" in to study, teach, track progress, and collaborate in real-time.

Our UI/UX core values will remain intact: **No generic landing page filler, zero latency, high information density, and instant utility upon entry.**

---

### 2. The Three-Pillar Persona Framework (Role-Based Onboarding)
We will transition the platform from flat, uniform user accounts into customized, role-based workflows with tailored user dashboards.

```
                  ┌──────────────────────┐
                  │   User Model (DB)    │
                  └──────────┬───────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
     [ STUDENT ROLE ] [ TEACHER ROLE ] [ SCHOOL/COLLEGE ]
```

#### A. Student Persona (The Learner Workspace)
* **Custom Onboarding:** Students select their current Grade, Academic Stream (Science, Management, Humanities, etc.), and their current School.
* **Active Dashboard:**
  * **Study Tracker:** A personal timeline displaying reading progress, upcoming exams, and active study habits.
  * **My Notebook:** Collection of personal bookmarks, sticky annotations from the PDF Reader, and solved questions.
  * **Gamified Ranking:** A progress bar showcasing their "Contribution Score" and achievements (e.g., "Quest Solver," "Resource Curator").

#### B. Teacher Persona (The Educator Workspace)
* **Verification Loop:** Teachers submit school credentials or a license to obtain a **"Verified Educator"** badge. Verified answers and notes are boosted in ranking.
* **Active Dashboard:**
  * **Resource Publisher:** An interface to compile syllabus guides, model answers, and term papers.
  * **Performance Metrics:** Stats showing how many students have viewed, downloaded, or bookmarked their materials.
  * **Quest Hub:** A board highlighting unanswered student questions (Quests) within their subject specialty. Solving these boosts their prestige score.

#### C. School / College Persona (The Institutional Portal)
* **Dedicated Space:** Schools can set up official, managed profiles to publish authentic internal resources.
* **Active Dashboard:**
  * **Official Notice Board:** Broadcast verified notices directly to students registered under their school.
  * **Classrooms / Study Circles:** Teachers within the school can form managed virtual groups for focused syllabus discussions.
  * **Leaderboards:** Internal school dashboards showing top-performing student contributors.

---

### 3. Active "Study Services" (SaaS Utilities)
We will expand the platform's features from "passive content consumption" to "active learning tools."

#### A. Interactive Mock Tests & Adaptive Quizzing
* **Custom Quiz Engine:** Rather than simply downloading old model question papers, students can trigger an interactive practice quiz.
* **Neby AI Integration:** Leverage our custom AI4Bharat Indic LLM proxy. Students can click **"Quiz Me on This"** while reading a specific PDF. Neby AI will parse the document, generate a 5-question multi-choice quiz, grade the answers in real-time, and explain incorrect choices.

#### B. Real-Time Study Circles (WebSockets Powered)
* **The Concept:** A collaborative virtual workspace where peers study together.
* **Implementation:** 
  * Leveraging the existing **Django Channels / Redis WebSocket architecture**, students can create a "Study Room" around a specific book or syllabus topic.
  * Features a shared **Pomodoro Timer**, a synchronized PDF viewer, and a real-time group chat.
  * Fully synchronized over WebSockets without database polling.

#### C. Gamified "Quests" & Bounty Solving
* **Academic Quests:** Instead of standard forum posts, students can format a challenging question as an **Active Quest** (complete with subject tags, difficulty level, and optional screenshot).
* **The Bounty System:** Peers and verified teachers submit step-by-step solutions. The community votes on the best solution. The solver earns **Contribution Points** (using the User model's `contribution_score`), raising their rank on the leaderboard.

#### D. Web-Based PDF Annotation Sync
* **The Canvas:** Bring the Android version's rich canvas annotation tools (highlight, underline, sticky notes) to the web.
* **Real-time Collaboration:** Multiple students can join a room to annotate a shared PDF together in real-time, saved to Room/MySQL database.

---

### 4. Technical Integration Architecture (Under the Hood)
Our existing backend is perfectly positioned to support these features with minimal overhead:

1. **Database Schema Evolution:**
   * Extend the `User` model to include a `role` field (`student`, `teacher`, `institution`, `guest`).
   * Add a `VerificationRequest` model to handle teacher verification.
   * Add `Quest` (sub-type of `Post`) and `QuestSolution` (sub-type of `Reply`) tables to track bounty-solving.
   
2. **WebSocket Scaling:**
   * Harness `api.consumers_ws.RealtimeConsumer` for Study Room sync.
   * Expand the subscription channel patterns to support `study_room.<id>` channels.

3. **Performance & Caching:**
   * Maintain the highly optimized Redis cache backend (`django.contrib.sessions.backends.cache`).
   * Cache student dashboard widgets with low-TTL (e.g., 60 seconds) or employ invalidation triggers on content upload/bounty submission.

4. **Neby AI Scaling:**
   * Expand our Indic LLM proxy pool to handle heavy quizzing and step-by-step tutoring.

---

### 5. Architectural Alignment for AI Agents
Any AI agent modifying this codebase must adhere to the **SaaS product vision**:
* **High-Density, High-Performance:** UI modifications must be fast, responsive, and avoid bloated assets. Keep layout transitions instant (using HTMX).
* **Security & Verification First:** Ensure teacher-uploaded or institutional content goes through robust verification workflows.
* **Component Reusability:** When designing dashboards or study workspaces, reuse existing Material 3 styling variables (`app.css` and `material3.css`) to ensure consistent branding.
