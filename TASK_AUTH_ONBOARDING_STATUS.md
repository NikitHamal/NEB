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
- [ ] Web onboarding wizard `/welcome/` (motion, shapes, live preview)
- [ ] Sign-in / sign-up / verify / forgot rebuilt on m3x (`m3x/app-auth.css`)
- [ ] Edit profile uses the same education picker + portfolio header fields
- [ ] Profile page: headline, education card, open-to, skills, portfolio sections + owner editor
- [ ] Android parity (catalog consumption, role at sign-up) -- open

## Rules that bite
- `class_level` still stores the level *value*; legacy values unchanged so resource filtering works.
- Anyone whose status is not "studying" is a global user (sees the full library).
- CI: `.github/workflows/backend-tests.yml` runs the Django tests, `bundle.py --check` and `makemigrations --check`. Never build locally in the sandbox.
