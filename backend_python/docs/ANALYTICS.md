
## Member analytics (the signed-in member's own numbers)

`GET /api/users/me/analytics/?days=7|30|90` (Bearer token), built by `api/user_analytics.py`.
It is the data behind the Android Analytics screen. Only the member's own rows are read.

| Block | What it holds |
| --- | --- |
| `standing` | contribution score, level (9 steps), progress to the next, top-percent rank (cached 10 min) |
| `overview` | six KPIs for the range with previous period, change % and a sparkline: contributions, likes received, replies received, new followers, readers, active days |
| `trend` | one row per day (posts, replies, resources, comments, reads, likes, responses, followers, actions) |
| `streak`, `heatmap`, `rhythm` | active-day streak, 17-week calendar (level 0-4, -1 = future), activity by hour and weekday (90 days) |
| `reach`, `helpfulness`, `library` | lifetime views / likes / engagement rate, reply kinds and labels earned, saves by type |
| `milestones`, `insights` | goals with progress; short notes chosen from the numbers (`tone`: good, info, action) |

An *active day* is a day with a post, reply, resource, resource comment, poll vote or post read by the
member. Likes and replies *received* come from the member's notifications, since likes carry no
timestamp of their own. A *reader* is another signed-in member who opened one of the member's posts
(`PostView`); guests are in the lifetime view counters but cannot be dated. Days are Nepal local days.
Page-view rows (`PageView`) are deliberately not read: they are not indexed by member.

Legacy keys (`stats`, `activityDays`, `topCategories`, `topSubjects`, `topPosts`, `topResources`,
`suggestions`) are kept for installed app versions. The Study Lab fields (`studyDocs`, `quizzes`,
`flashcards`, ...) are gone. Cost: 24 queries, fixed (`api.test_api_query_budget`). Tests:
`DB_ENGINE=sqlite SECRET_KEY=x DEBUG=1 python manage.py test api.test_user_analytics`.
