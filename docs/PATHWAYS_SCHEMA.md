# Pathways data schema

Source files live in `backend_python/api/data/pathways/` and are merged by `api/pathways.py` into `/api/pathways/`.
The Android app (`ui/screens/pathways`) reads every field below. Fields marked optional can be left out: the screen
that needs them simply hides. Add them as data is collected; no app update is needed.

Ratings `demand`, `competition` and `abroad` use 1 to 5 (the app shows them as 0 to 100). Money is NPR.
Months are 1 to 12.

## routes (courses)

Existing: `id, stage, name, kind, group, years, fee [min, max] (whole course), entry, about, exam, careers[], skills[], next[], where[]`.

Optional:

| field | type | used for |
| --- | --- | --- |
| `plan` | `["Year 1: Programming", ...]` | Overview journey steps |
| `tags` | `["build", "num"]` | Match. Overrides the group guess. Keys: build heal num ppl make law nature serve, math sci bio lang biz comp art |
| `exam_id` | govt id | Entry tab links to the exam |
| `demand`, `competition` | 1 to 5 | Overrides the average of the route's careers |

## careers

Existing: `id, name, about, demand, competition, trend (rising|steady|falling), abroad, salary {entry [min,max], senior [min,max]}` (monthly).

Optional: `skills[]`, `ladder ["Junior","Mid-level","Senior","Lead"]`, `day [["Coding", 45], ...]` (percent of a week),
`hours` (per week), `jobs [["Kathmandu Valley", 55], ...]`, `employers[]`, `traits {"stability": 60, "flexibility": 85, "growth": 90}` (0 to 100),
`history [60, 64, 70, 75, 82, 90]` (demand 0 to 100, oldest first), `licence {"name": "NEC registration", "exam": "<govt id>"}`.

## providers (colleges)

Optional: `fees {"<route id>": [min, max]}` and `seats`.

## scholarships

Optional: `country` (abroad id), `type` (Embassy, Government, University), `open [fromMonth, toMonth]`, `awards`.

## abroad

Optional: `code` ("AU"), `visa_rate` (percent), `work_hours` (per week), `stay_back` ("2 to 4 years").
`intakes` month names are read to draw the intake strip.

## govt (exams)

Existing: `id, track, name, level, need, age, body, stages [[name, detail]], subjects[], prep[], note`.
`need` and `age` are read for eligibility ("SEE", "+2", "Bachelor", "Master"; "18 to 35 years, up to 40 for women").

Optional: a third item in each stage for marks, `seats`, `applicants`, `fee`, `apply [fromMonth, toMonth]`, `exam_month`,
`prep_hours`, `syllabus [["General knowledge", 30], ...]`, `quota [["Open", 55], ...]`,
`ladder [["Kharidar", 33000], ...]` (lowest first, monthly pay), `rung` (index of this post in the ladder), `career` (career id), `pay`.

## guides (new file `guides.json`: `{"guides": [...]}`)

```json
{"id": "passport", "name": "Passport", "cat": "Documents",
 "steps": [["Pre-enrol online", 1, 0, "online"], ["Pay the fee", 1, 5000, "in person"]],
 "docs": ["Citizenship", "National ID"], "link": "exam:g-kharidar"}
```

Each step is `[title, days, cost, "online" | "in person"]`. `link` is any app target: `route:<id>`, `career:<id>`, `exam:<id>`, `guide:<id>`.
