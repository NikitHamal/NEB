# Project II — BCA 306

Semester V · 3 credits · a project course. TU does not publish a unit-wise syllabus for it, so this book is a **companion handbook**. Project I (BCA 256) built a stand-alone program; Project II is where you build a **networked web system**: a browser or phone talks to a server over HTTP, many users log in at once, data lives in a database, and the whole thing must be secured, tested and deployed. The running example is **ClinicQ**, a token-queue and appointment system for a community health post.

| Unit | Title |
|---|---|
| 1 | From Stand-alone to Web System: Scope, Architecture and Stack |
| 2 | Building the REST API and the Database |
| 3 | Security: Login, Passwords, Tokens and Attacks |
| 4 | Testing, Performance and Deployment |
| 5 | Documentation, Demo, Report and Viva for Project II |

## Verification

Every program in this book was run and the printed output pasted from the real run (Python 3 standard library: `http.server`, `sqlite3`, `hashlib`, `hmac`, `unittest`). The API in Unit 2 starts a real HTTP server on a local port and calls it over the network stack. Capacity and security figures were computed by those scripts.

## Source and honesty

**The unit structure is reconstructed.** BCA 306 has no published topic list; colleges set their own proposal and report format. **Always follow your own college's project guidelines and your supervisor's instructions first**; where they differ from this book, they win. ClinicQ is an invented teaching example, not a real health post's system; all names, phone numbers and statistics in it are made up. Production frameworks (Flask, Django, Express, Laravel) are named but the code uses only the Python standard library so that every line can be read and verified. Nothing here has had a subject-teacher review.
