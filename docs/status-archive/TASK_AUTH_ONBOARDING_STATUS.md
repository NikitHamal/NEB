# Auth, onboarding, education levels and portfolio profile -- status

Owner brief: sign-in / sign-up were never moved to m3x; a user reported the role
choice not changing the default (Student); onboarding needs real motion design;
education options must cover Nepal (dropouts, +2, TSLC, diplomas, bachelors,
masters, prep, abroad, self-learners) with optional year/semester; profiles
should become an education + professional portfolio and a social page.

## Root cause of the role report
Only email sign-up asked for a role. Google/GitHub sign-ups never did and were
created as Student, and the edit-profile role cards were driven by a click
handler on the card that read the class from a different widget. Role is now
chosen once, in onboarding step 1, explicitly saved server-side, and no role
is preselected for social sign-ups.

## Plan / done
- [x] `api/education_catalog.py` single catalog: statuses, 30+ levels, 200+ programs, terms, open-to
- [x] User fields (edu_status/program/term/completed, headline, skills, open_to), `ProfileEntry` model, migration 0161
- [x] `api/profile_education.py` shared validation; `/api/education/catalog/`, `/api/profile/entries/`, public portfolio
- [x] Web onboarding wizard `/welcome/` (motion, shapes, live preview) -- `web/views_onboarding.py`, `js/onboarding.js`, `m3x/app-onboard.css`
- [x] Sign-in / sign-up / verify / forgot rebuilt on m3x (`m3x/app-auth.css`, `js/auth.js`); legacy `app/04-auth-layout.css` removed
- [x] Edit profile rebuilt on the shared pickers (session 3, below)
- [x] Profile page: headline, education card, open-to, skills, portfolio sections + owner editor (`web/profile/_portfolio.html`, `js/portfolio.js`, `m3x/app-portfolio.css`)
- [ ] Android parity (catalog consumption, role at sign-up) -- open

## Polish pass (session 2)
- [x] Welcome flow crash: `h()` in `onboarding.js` passed an array to `appendChild` (role step); it now flattens arrays/NodeLists
- [x] Sign-in / sign-up / verify / reset: tonal card, dark-mode field + art tokens, autofill, tablet / phone / landscape layouts, `.ax-note` spam-folder hint on verify and reset; legacy `email_login/verify` pages redirect to `/login/`
- [x] One stroke on focus: `m3x/app-focus.css` (fields recolour their own border, no outside ring); the post pill no longer stacks border + ring
- [x] `@` popup in the post dialog: the click after the popup hid read as a backdrop click; dialog now closes only when the press began on the backdrop, and the picker swallows that click
- [x] Reply composer / poll builder / staged media lost their inset: the poll wrapper `.pb-scope` broke `.fp-center-panel > .neb-composer`; the rule now covers the wrapper
- Tests: `web.test_polish_regressions`

## Rules that bite
- `class_level` still stores the level *value*; legacy values unchanged so resource filtering works.
- Anyone whose status is not "studying" is a global user (sees the full library).
- CI: `.github/workflows/backend-tests.yml` runs the Django tests, `bundle.py --check` and `makemigrations --check`. Never build locally in the sandbox.

## Entry points
- `/login/` (`?panel=signup|forgot`, `?next=`), `/welcome/` (prefilled when the profile is complete), `/ajax/portfolio/save|delete/`
- API: `/api/education/catalog/`, `/api/profile/entries/`, `/api/users/profile/<u>/portfolio/`; `POST /api/users/profile/` accepts `eduStatus eduProgram eduTerm eduCompleted headline skills openTo`
- Tests: `api.test_education_portfolio`, `web.test_onboarding`, `web.test_auth_pages`, `web.test_portfolio_profile` (all run by `backend-tests.yml`)

## Ideas not built yet
Profile completeness ring + nudges, shareable portfolio card image (og card), study-partner matching from `open_to` + level + program, mentor/junior pairing,
verified credentials (teacher/school confirms an entry), resume PDF export, "class of" year groups and alumni of a school, entrance-prep cohorts, streak and study-goal badges,
skill endorsements, Android consumption of the catalog + onboarding parity.

## Session 3: one set of controls for onboarding and edit profile
Owner brief: reuse the profile editor's date wheel and gender tiles in onboarding, stack them (date above gender) in both
places, make onboarding minimal, overhaul the editor, and make Bachelor's/Master's courses (BCA, BBS, BBA, Nursing, CSIT, CS, BE)
quick to pick instead of one huge list.
- [x] `components/_dob_field.html`, `_gender_tiles.html`, `_dob_sheet.html` + `js/neb-dob-field.js`: the only date + gender implementation; onboarding carries the server-rendered nodes into step two
- [x] `js/neb-edu.js` (`window.NebEdu`): `chips/combo/tags/picker`; onboarding and `js/epf-education.js` (editor) both mount `picker()`
- [x] Catalog: `STAGES` (School, +2, Diploma, Bachelor's, Master's, Exam prep, Other), `POPULAR` courses per level (<=16 chips, rest behind a search), `LEVEL_STATUS`; `BSc Computer Science` added. Full lists stay for search (API/Android unchanged, keys are additive)
- [x] Onboarding is role -> you (name, date, gender) -> one role step (studies / subjects / institution; explorers skip) -> done. Province, school, headline, skills, open-to, bio and interests moved to the editor. Status is implied by the stage
- [x] Editor: Basics (+headline), Role, Education (picker with status, year/semester), Personal (date over gender), Where, Skills + Open to, Links, Privacy; taglines cut; POST runs `apply_education`
- Tests: `api.test_education_stages`, `web.test_onboarding` (shared controls), `web.test_edit_profile`
- Open: Android picker parity (stages / popular), edit-profile photo hint removed on purpose
