---
subject: Project II
grade: BCA Semester 5
unit: 2
title: Building the REST API and the Database
area: BCA 306 · Project II · Unit 2
---

This unit builds the heart of ClinicQ: a database with constraints and a REST API that runs on a real HTTP server. You will see a complete working program of 78 lines, run it, and read its replies line by line. The goal is that you can explain every status code in the viva, because you saw it produced.

::: key What this unit gives you
- A database design for ClinicQ with an ER figure and the constraints that keep it correct.
- How an HTTP request is turned into a handler call, a SQL statement and a JSON reply.
- A complete runnable API with validation, 201/400/404/422 replies and real output.
- Why a database constraint, not Python code, makes token numbers unique under parallel requests.
:::

## 2.1 Designing the data

ClinicQ stores two things: **patients** and **tokens**. A patient can have many tokens over time (one per visit); each token belongs to exactly one patient. Staff accounts are added in Unit 3.

```svgfig label="2.1" caption="ER diagram of ClinicQ. One patient has many tokens (1 to N). The pair (day, no) is unique, which is what stops duplicate token numbers on the same day."
f = Fig(520, 190)
f.box(20, 30, 170, 120, "", fill=BLUE, stroke=NAVY)
f.text(105, 48, "PATIENT", size=12, color=NAVY, bold=True)
f.text(105, 75, "id  (PK)", size=11, color=NAVY)
f.text(105, 97, "name  NOT NULL", size=11, color=NAVY)
f.text(105, 119, "phone  NOT NULL", size=11, color=NAVY)
f.box(330, 20, 170, 150, "", fill=SOFT, stroke=TEAL)
f.text(415, 38, "TOKEN", size=12, color=NAVY, bold=True)
f.text(415, 62, "id  (PK)", size=11, color=NAVY)
f.text(415, 82, "day  NOT NULL", size=11, color=NAVY)
f.text(415, 102, "no  NOT NULL", size=11, color=NAVY)
f.text(415, 122, "patient_id  (FK)", size=11, color=NAVY)
f.text(415, 142, "status  CHECK(...)", size=11, color=NAVY)
f.arrow([(190, 95), (330, 95)], color=NAVY)
f.text(260, 82, "has", size=11, color=NAVY)
f.text(205, 112, "1", size=11, color=RED, bold=True)
f.text(312, 112, "N", size=11, color=RED, bold=True)
f.text(415, 183, "UNIQUE (day, no)", size=10, color=RED)
```

Every constraint in the figure is a rule enforced by the database itself:

| Constraint | Written as | Rule it enforces |
|---|---|---|
| Primary key | `id INTEGER PRIMARY KEY` | each row has one unique identity |
| Not null | `name TEXT NOT NULL` | a patient always has a name and phone |
| Foreign key | `REFERENCES patient(id)` | a token cannot point at a missing patient |
| Check | `CHECK(status IN (...))` | status is one of three allowed words |
| Unique | `UNIQUE(day, no)` | no two tokens share a number on a day |

## 2.2 What happens when a request arrives

An HTTP request is plain text: a request line (`POST /api/tokens HTTP/1.1`), headers, a blank line and an optional body. The server program reads it, picks the handler by method and path, runs the handler and writes a reply: a status line (`201 Created`), headers and a body. In our program Python's `http.server` does the reading; we write the handler.

```svgfig label="2.2" caption="Life of one request through ClinicQ. Steps 1 to 6: parse, validate, run SQL, build JSON, send reply. Validation failure short-circuits to a 400 or 422 before the database is touched."
f = Fig(560, 150)
names = ["Parse request", "Validate input", "Run SQL", "Build JSON", "Send reply"]
cols = [BLUE, SOFT, BLUE, SOFT, BLUE]
for i, n in enumerate(names):
    x = 10 + i * 110
    f.box(x, 40, 92, 50, n, fill=cols[i], stroke=NAVY, size=11, color=NAVY)
    if i < 4: f.arrow([(x + 92, 65), (x + 110, 65)], color=NAVY)
f.arrow([(166, 40), (166, 18), (506, 18), (506, 40)], color=RED, dash=True)
f.text(336, 12, "invalid: reply 400 / 422 at once", size=10, color=RED)
f.text(280, 125, "Parameterised SQL: values travel separately from the statement", size=11, color=NAVY)
```

## 2.3 The ClinicQ API, complete

The program below creates the database in memory, defines a handler class with one method per HTTP verb, starts the server on a free port in a background thread and then calls it with ordinary HTTP requests. Read the code in this order: the `CREATE TABLE` text, `do_POST`, `do_GET`, `do_PATCH`, and last the calls at the bottom.

```python
import json, sqlite3, threading, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DB = sqlite3.connect(":memory:", check_same_thread=False)
DB.executescript("""
CREATE TABLE patient(id INTEGER PRIMARY KEY, name TEXT NOT NULL, phone TEXT NOT NULL);
CREATE TABLE token(id INTEGER PRIMARY KEY, day TEXT NOT NULL, no INTEGER NOT NULL,
                   patient_id INTEGER NOT NULL REFERENCES patient(id),
                   status TEXT NOT NULL DEFAULT 'waiting' CHECK(status IN ('waiting','served','cancelled')),
                   UNIQUE(day, no));
""")
LOCK = threading.Lock()

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)
    def body(self):
        n = int(self.headers.get("Content-Length", 0))
        try: return json.loads(self.rfile.read(n) or b"{}")
        except ValueError: return None
    def do_POST(self):
        if self.path == "/api/patients":
            b = self.body()
            if not b or not str(b.get("name", "")).strip() or not str(b.get("phone", "")).isdigit():
                return self.send(400, {"error": "name and numeric phone required"})
            with LOCK:
                c = DB.execute("INSERT INTO patient(name, phone) VALUES (?, ?)", (b["name"].strip(), b["phone"]))
            return self.send(201, {"id": c.lastrowid})
        if self.path == "/api/tokens":
            b = self.body() or {}
            with LOCK:
                if not DB.execute("SELECT 1 FROM patient WHERE id=?", (b.get("patient_id"),)).fetchone():
                    return self.send(404, {"error": "no such patient"})
                no = DB.execute("SELECT COALESCE(MAX(no),0)+1 FROM token WHERE day=?", (b.get("day", "2083-01-15"),)).fetchone()[0]
                c = DB.execute("INSERT INTO token(day,no,patient_id) VALUES (?,?,?)", (b.get("day", "2083-01-15"), no, b["patient_id"]))
            return self.send(201, {"id": c.lastrowid, "no": no, "status": "waiting"})
        self.send(404, {"error": "not found"})
    def do_GET(self):
        if self.path.startswith("/api/tokens"):
            with LOCK:
                rows = DB.execute("SELECT t.no, p.name, t.status FROM token t JOIN patient p ON p.id=t.patient_id ORDER BY t.no").fetchall()
            return self.send(200, [{"no": r[0], "name": r[1], "status": r[2]} for r in rows])
        self.send(404, {"error": "not found"})
    def do_PATCH(self):
        if self.path.startswith("/api/tokens/"):
            b = self.body() or {}
            if b.get("status") not in ("served", "cancelled"):
                return self.send(422, {"error": "status must be served or cancelled"})
            with LOCK:
                c = DB.execute("UPDATE token SET status=? WHERE id=?", (b["status"], self.path.rsplit("/", 1)[1]))
            return self.send(200 if c.rowcount else 404, {"updated": c.rowcount})
        self.send(404, {"error": "not found"})

srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{srv.server_port}"

def call(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=None if body is None else json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r: return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e: return e.code, json.loads(e.read())

print(*call("POST", "/api/patients", {"name": "Sita Gurung", "phone": "9841000001"}))
print(*call("POST", "/api/patients", {"name": "Ram Thapa", "phone": "98x"}))
print(*call("POST", "/api/tokens", {"patient_id": 1}))
print(*call("POST", "/api/tokens", {"patient_id": 1}))
print(*call("POST", "/api/tokens", {"patient_id": 99}))
print(*call("PATCH", "/api/tokens/1", {"status": "served"}))
print(*call("PATCH", "/api/tokens/2", {"status": "done"}))
print(*call("GET", "/api/tokens"))
srv.shutdown()
```
```output
201 {'id': 1}
400 {'error': 'name and numeric phone required'}
201 {'id': 1, 'no': 1, 'status': 'waiting'}
201 {'id': 2, 'no': 2, 'status': 'waiting'}
404 {'error': 'no such patient'}
200 {'updated': 1}
422 {'error': 'status must be served or cancelled'}
200 [{'no': 1, 'name': 'Sita Gurung', 'status': 'served'}, {'no': 2, 'name': 'Sita Gurung', 'status': 'waiting'}]
```
Read the replies against the code:

| Call | Reply | Why |
|---|---|---|
| register Sita | `201 {'id': 1}` | valid name and numeric phone; 201 Created |
| register Ram with phone `98x` | `400` | `isdigit()` fails, so the database is never touched |
| token for patient 1, twice | numbers 1 then 2 | `MAX(no)+1` for the day |
| token for patient 99 | `404` | no such patient row |
| PATCH token 1 to `served` | `200 {'updated': 1}` | one row changed |
| PATCH token 2 to `done` | `422` | well-formed JSON but not an allowed value |
| GET the queue | JSON list with a JOIN | names come from the patient table |

Three habits in this code are worth defending in the viva. **Validate first**, so bad input gets a 400 before any SQL runs. **Use `?` placeholders**, so user text can never become SQL (Unit 3 shows the attack). **Return the right code**: the client can then react without reading the message text.

## 2.4 Two clerks at the same moment: the race condition

The token number is computed as "highest number today plus one". If two requests both read 7 before either writes, both write 8. This is a **race condition**. The program below forces the bad interleaving with a barrier, first without a constraint and then with `UNIQUE(day, no)`.

```python
import sqlite3, threading
def run(constraint):
    db = sqlite3.connect(":memory:", check_same_thread=False, isolation_level=None)
    db.execute("CREATE TABLE token(day TEXT, no INTEGER" + (", UNIQUE(day, no)" if constraint else "") + ")")
    db.execute("INSERT INTO token VALUES ('d1', 7)")
    gate, out, lock = threading.Barrier(2), [], threading.Lock()
    def clerk(name):
        for attempt in range(3):
            with lock: nxt = db.execute("SELECT MAX(no)+1 FROM token WHERE day='d1'").fetchone()[0]
            if attempt == 0: gate.wait()             # both clerks have read the same value
            try:
                with lock: db.execute("INSERT INTO token VALUES ('d1', ?)", (nxt,))
                out.append((name, nxt)); return
            except sqlite3.IntegrityError:
                out.append((name, f"{nxt} rejected, retry"))
    ts = [threading.Thread(target=clerk, args=(n,)) for n in ("A", "B")]
    [t.start() for t in ts]; [t.join() for t in ts]
    rows = [r[0] for r in db.execute("SELECT no FROM token ORDER BY no")]
    return "rejected inserts: " + str(sum("rejected" in str(o[1]) for o in out)), "table: " + str(rows)
for c in (False, True):
    print("constraint" if c else "no constraint", *run(c), sep="\n  ")
```
```output
no constraint
  rejected inserts: 0
  table: [7, 8, 8]
constraint
  rejected inserts: 1
  table: [7, 8, 9]
```
Without the constraint both clerks receive 8 and the table holds `[7, 8, 8]`: two patients with the same token. With the constraint the database refuses the second insert; that clerk's code catches the `IntegrityError`, reads again and gets 9. The lesson is general: **if a rule must always hold, put it in the database**, because application code in two requests can interleave but the database cannot be bypassed.

## 2.5 Transactions and error replies

A **transaction** groups statements so that they all happen or none does (the ACID rule). In SQLite and MariaDB a plain `INSERT` is already atomic; a transaction matters when two statements belong together, for example *mark token served* and *write the audit log row*. Use `BEGIN ... COMMIT`, and `ROLLBACK` on error.

Error replies should be **safe and useful**: say what the client did wrong (`name and numeric phone required`) but never reveal internals such as a SQL statement or a file path. Log the details on the server and return `500 {"error": "server error"}` for faults of your own.

## 2.6 Eight reasons to validate and constrain at every layer

1. **Browsers can be bypassed.** JavaScript checks run on the user's machine, so a script or a tool can send anything. The server must check again. This is the first rule of web security.
2. **Bad data lives for years.** A wrong phone number stored today is shown in reports next year. Rejecting it at entry costs one line; cleaning it later costs a week.
3. **The database is the last guard.** Even a perfect handler can be changed by a new developer. `NOT NULL`, `UNIQUE` and `CHECK` rules cannot be forgotten because they live with the data.
4. **Clear codes help clients.** A mobile app can show "fix the phone number" for 400 and "log in again" for 401 only if the codes are honest. Hiding errors inside `200 OK` forces clients to guess.
5. **Placeholders stop injection.** Separating the SQL text from the values means that a name such as `x'; DROP TABLE patient;--` is stored as a name, not executed (Unit 3).
6. **Constraints remove race conditions.** As in Section 2.4, `UNIQUE(day, no)` makes duplicate tokens impossible rather than unlikely, which is the difference between a demo and a system.
7. **Validation documents the rules.** A reader sees `phone must be digits` in the code and learns the business rule. The tests in Unit 4 repeat the same rules as examples.
8. **Examiners ask for it.** A common viva question is "what happens if I send a blank name?". A project whose answer is "400, shown here" scores better than one that crashes.

```photogrid label="2.1" cols="2" ratio="1.2" caption="Two clerks, one counter: all possible orders. (a) A queue-token display at a hospital counter; each new patient takes the next number. (b) Suppose the counter holds 41 and each of two clerks does two steps: read the counter (R), then write back the value they read plus 1 (W). The steps of each clerk keep their order, but the two clerks can interleave in 6 ways. In 2 of them (clerk 1 finishes before clerk 2 starts, or the reverse) the counter ends at 43, which is correct. In the other 4 both clerks read 41 before either writes, so both write 42 and one token is lost: a 67 per cent chance of a lost update in this simplest case. The cure is to make read-and-write one indivisible step, with a database transaction, a row lock or a single UPDATE counter = counter + 1 statement, and to add a UNIQUE constraint as the last line of defence."
@ photo id="bcapj/token" cap="A queue-token display: B-003 is next"
fit 1.2
focus 0.5 0.5
@ svg cap="All 6 interleavings of two clerks, start value 41"
import itertools
res = []
for perm in sorted(set(itertools.permutations(["R1", "W1", "R2", "W2"]))):
    if perm.index("R1") < perm.index("W1") and perm.index("R2") < perm.index("W2"):
        v = 41; loc = {}
        for s in perm:
            if s[0] == "R": loc[s[1]] = v
            else: v = loc[s[1]] + 1
        res.append((perm, v))
assert len(res) == 6 and sum(v == 43 for _, v in res) == 2 and sum(v == 42 for _, v in res) == 4
f = Fig(300, 240)
f.text(150, 14, "R = read counter, W = write read + 1", size=10.5, color=NAVY, bold=True)
for i, (perm, v) in enumerate(res):
    y = 26 + i * 29
    for k, s in enumerate(perm):
        col = "#bfdbfe" if s[1] == "1" else "#fde68a"
        f.box(8 + k * 42, y, 38, 22, s, fill=col, stroke=NAVY, color=NAVY, size=10.5, bold=s[0] == "W", r=4, sw=1)
    ok = v == 43
    f.box(184, y, 106, 22, f"ends {v}: " + ("correct" if ok else "lost one"), fill="#bbf7d0" if ok else "#fecaca", stroke="#0f766e" if ok else "#b91c1c", color="#0f766e" if ok else "#b91c1c", size=10.5, bold=True, r=4, sw=1)
f.text(150, 214, "4 of 6 orders lose an update (67%)", size=10.5, color=RED, bold=True)
f.text(150, 230, "fix: transaction, lock or one UPDATE", size=10.5, color=TEAL, bold=True)
```

## Formula and fact sheet

- Request line: `METHOD /path HTTP/1.1`; reply status line: `HTTP/1.1 201 Created`.
- ACID: atomicity, consistency, isolation, durability.
- Constraints: PRIMARY KEY, NOT NULL, FOREIGN KEY, CHECK, UNIQUE.
- Next token number = highest number of the day + 1, protected by `UNIQUE(day, no)` and retried on conflict.

## Chapter summary

- ClinicQ has two tables, patient and token, in a one-to-many relation with five kinds of constraint.
- A request flows: parse, validate, run SQL, build JSON, reply; invalid input is rejected early.
- The 78-line API replies 201, 400, 404, 422 and 200 and was run over a real local HTTP connection.
- Race conditions are solved by database constraints plus a retry, not by hoping.
- Safe errors tell the client what to fix and hide the internals.

## Practice

1. Write the SQL for the token table with all five kinds of constraint.
2. Which status code would you return for a phone number of 5 digits? Defend it.
3. Why is the SQL written with `?` placeholders?
4. What does `UNIQUE(day, no)` stop?
5. Why does the handler check the patient exists before inserting a token, when a foreign key also exists?
6. Give one example of two statements that should be in one transaction.
7. What does `GET /api/tokens` return when there are no tokens?
8. Explain the difference between 400 and 422 using ClinicQ examples.
9. Draw the ER diagram of a bus-ticket system with routes and bookings.
10. If 150 tokens are issued in 8 hours, what is the average arrival rate per minute?

::: note Answers and worked solutions
**1.** See the `CREATE TABLE token` statement in Section 2.3.
**2.** 400, because the input is malformed against the stated format (digits only, usual length).
**3.** So that user text is data and never part of the SQL statement.
**4.** Two tokens with the same number on the same day.
**5.** To return a friendly 404; otherwise the database error would become a 500.
**6.** Mark a token served and write the audit-log row: both or neither.
**7.** `200` and the empty list `[]`.
**8.** 400: the body is not JSON or a field is missing. 422: valid JSON with a value the rules refuse, such as `status: "done"`.
**9.** Route(id, from, to), Booking(id, route_id FK, seat, day), unique(route_id, day, seat).
**10.** 150 / 480 minutes = 0.3125 patients per minute, about 1 patient every 3.2 minutes.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is a race condition? Show how a web application issuing token numbers can suffer from it and how it is prevented.**

*Introduction.* A race condition is a fault in which the result of a program depends on the timing of two or more simultaneous actions. It is common in web systems because many requests are handled at the same time.

*Example.* ClinicQ computes the next token as "highest number today plus one". Two clerks submit at the same instant. Both read 7, both compute 8 and both insert 8. Two patients now hold the same token, and the program printed no error. The run in Section 2.4 produced the table `[7, 8, 8]`.

*Prevention.*

1. **Database constraint.** Declare `UNIQUE(day, no)`. The second insert is rejected with an integrity error, so duplicates become impossible.
2. **Retry.** The handler catches the error, reads the highest number again and inserts 9. The same run then gave `[7, 8, 9]` with one rejected insert.
3. **Transaction or lock.** Alternatively wrap the read and the insert in one transaction or use an atomic counter, so the pair cannot interleave.

*Conclusion.* Rules that must always hold belong in the database; application checks alone cannot prevent a race.

**Q2 (5 marks). Describe how an HTTP request is processed by a REST API, from arrival to reply.**

*Introduction.* A REST API is a server program that exposes resources over HTTP and answers with JSON. Each request is processed in the same fixed sequence.

*Steps.*

1. **Parse.** The server reads the request line (method and path), the headers and the body, for example `POST /api/tokens` with `{"patient_id": 1}`.
2. **Route.** The method and path pick the handler, such as `do_POST` for `/api/tokens`. An unknown path gets 404.
3. **Validate.** The handler checks that the JSON is well formed and that fields have the right type and range. Failure gives 400 or 422 and stops.
4. **Execute.** The handler runs parameterised SQL inside a transaction; constraint errors are caught and turned into 4xx replies.
5. **Build the reply.** The result is converted to JSON with a status code (201 for creation, 200 for success) and a `Content-Type` header.
6. **Log.** Method, path, status and time are written to a log, never the password or token.

*Example.* In the real run, `POST /api/tokens` for patient 99 produced `404 {'error': 'no such patient'}` at step 4, while patient 1 produced `201 {'no': 1}`.

*Conclusion.* Knowing this sequence makes the API easy to debug and defend.

**Q3 (10 marks). Design the database and REST API for a clinic token-queue system and justify your constraints, status codes and error handling.**

*Introduction.* A clinic token system needs a shared database and a network interface so that clerks, nurses and patients can use it at once. The design below is ClinicQ.

*1. Database design.* Two tables: `patient(id, name, phone)` and `token(id, day, no, patient_id, status)`, related one-to-many (Figure 2.1). Every table has a primary key; names and phones are `NOT NULL`; `patient_id` is a foreign key; `status` is restricted by `CHECK` to waiting, served or cancelled; `UNIQUE(day, no)` stops duplicate numbers.

*2. Resources.* `POST /api/patients`, `POST /api/tokens`, `GET /api/tokens`, `PATCH /api/tokens/{id}`; later `POST /api/login`. Nouns are plural; verbs state the action; GET never changes data.

*3. Status codes.*

| Situation | Code |
|---|---|
| patient or token created | 201 |
| list or update succeeded | 200 |
| missing name or non-numeric phone | 400 |
| patient does not exist | 404 |
| status other than served or cancelled | 422 |
| no or invalid login (Unit 3) | 401 |

*4. Processing sequence.* Each request is parsed, validated, executed with `?` placeholders, answered in JSON and logged (Figure 2.2). Validation happens before SQL so that bad input never reaches the database.

*5. Concurrency.* Two simultaneous requests could take the same number. The `UNIQUE` constraint rejects the second insert and the handler retries, producing 7, 8, 9 rather than 7, 8, 8.

*6. Error handling.* Client faults get 4xx with a short message; server faults get a generic 500 and a detailed server log. Messages never show SQL or file paths.

*7. Verification.* The 78-line program was started on a local port and called over HTTP; the printed replies match the table above (Section 2.3).

| Design choice | Reason |
|---|---|
| constraints in the database | cannot be bypassed |
| placeholders | prevent SQL injection |
| honest status codes | clients can react |
| retry on conflict | no duplicates under load |

*Conclusion.* A small API with strong constraints, honest status codes and safe errors is easier to test, secure and explain than a large one built on assumptions.
