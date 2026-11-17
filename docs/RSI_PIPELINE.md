# NEBians RSI (Recursive Self-Improvement) Pipeline v2

## Purpose & Session 1 Post-Mortem (`tools/rsi/sessions.txt`)

Every AI engineering session operates under a strict sequential tool-call limit (75 calls) and faces potential mid-session container timeouts.

Analysis of `tools/rsi/sessions.txt` (Session 1) revealed three major tool-call drains:
1. **Sparse-Checkout File Discovery Friction (~10 tool calls)**: Standard `glob_files` calls can return empty lists on sparse-checked-out subdirectories, causing repeated guessing.
2. **End-of-Session Idle CI Polling (11 consecutive turns in Session 1)**: Polling `rsi.py ci` in a tight loop while waiting for Android release builds burned 15% of the session's tool budget without doing productive work in between.
3. **Stale CSS Bundle & Admin Shell Regressions**: Editing CSS source files without running `tools/css/bundle.py` caused preventable verification round-trips, and parallel Django tests previously hit SQLite lock contention from background analytics threads.

`tools/rsi/rsi.py` v2 + `tools/rsi/security_and_m3x_audit.py` eliminate all three bottlenecks, multiplying effective output per session by 5 to 10x while guaranteeing zero lost work.

---

## Single-Call Commands

### 1. Session Pickup (`1 tool call` at Turn 1/2)

```bash
python3 tools/rsi/rsi.py pickup
```

- Prints `git status -sb` and the last 6 commits on `main`.
- Extracts the most recent session table and `Next` items from `ANDROID_STATUS.md`.
- Queries the GitHub Actions REST API for the latest 5 workflow runs on `main` (`Build Student Release APKs & AAB`, `Backend tests`, `Deploy Backend to cPanel`).

### 2. Instant Domain & File Mapper (`1 tool call` instead of repeated globs)

```bash
python3 tools/rsi/rsi.py map <regex_or_substring>
```

- Searches `git ls-files` by case-insensitive regex/substring and prints matching relative paths with line counts (up to 60 results). Use this instead of `glob_files` whenever locating files in `app/` or `backend_python/`.

### 3. Auto-Bundling Static, M3X & Security Verification (`1 tool call`)

```bash
python3 tools/rsi/rsi.py verify
```

Runs in under 2 seconds without invoking Gradle locally:
0. **Auto-CSS Bundle**: If `tools/css/bundle.py --check` detects modified CSS sources, automatically runs `tools/css/bundle.py` before checking guards.
1. `tools/android/check_scrollers.py` (infinite-width horizontal scroll crash guard)
2. `tools/android/check_insets.py` (status bar & top bar alignment guard)
3. `tools/android/check_sheets.py` (`NebModalSheet` padding & status bar guard)
4. `tools/android/check_text_fit.py` (unbounded `Text` in `Row` ratchet)
5. `tools/css/bundle.py --check` (verifies `m3x-app.css` and `admin.css` bundles are in sync)
6. `tools/rsi/security_and_m3x_audit.py` (AST syntax check on modified Python files, staged diff secret-leak detector, Admin M3X shadow/radius/dialog guard, and core security/obfuscation invariants)

### 4. Atomic Micro-Checkpoint & Push (`1 tool call` per milestone)

```bash
python3 tools/rsi/rsi.py checkpoint "concise milestone commit message"
```

- Runs `verify` first (including auto-rebuilding CSS bundles if needed); aborts immediately if any guard or AST check fails.
- Stages changes (`git add -A`), excluding local sandbox artifacts (`package.json`).
- Scans `git diff --cached` for PATs, private keys, or API secrets (`check_staged_secrets`).
- Commits, rebases (`git pull --rebase --autostash origin main`), and pushes immediately to `origin main` using `/tmp/gitenv.sh`.
- **Mandatory Rule**: Run `checkpoint` after every completed logical milestone (every 3 to 5 file edits) so no work can ever be lost to a session timeout.

### 5. CI Status with Auto-Failure Log Extraction & Deployment Dispatch

```bash
python3 tools/rsi/rsi.py ci
python3 tools/rsi/rsi.py deploy
```

- `ci` prints the status, active step of any `in_progress` workflow run, and automatically fetches the error log tail from the GitHub REST API if any job failed.
- `deploy` triggers `deploy-backend.yml` (`workflow_dispatch`) on `main` using the repository's `SSH_HOST` and `SSH_KEY` secrets.
- **Zero-Idle-Poll Rule (from Session 1 Post-Mortem)**: Never poll `rsi.py ci` in a tight loop while other tasks remain. Push code milestones first, then write tests, documentation, and `ANDROID_STATUS.md` updates while CI compiles in the background.

## Session 66 lessons (added)

- **Root cause before restyling.** "UI is a mess" on a page whose CSS module already had the rules was a stale-cache bug (`@import`-only entry file never changed its content hash). Check the shipped file, not the source, first. `web/test_css_entrypoints.py` now guards it.
- **One-turn cadence that worked:** pickup -> read the status tail + grep the failing template/CSS in one bash call -> fix -> `checkpoint` -> docs while CI runs. Four checkpoints before the first CI poll.
- **No local Django** in the sandbox: test pure modules directly (`cd backend_python/nebians/analytics && python3 -c "import rules"`); leave the Django suite to the Backend tests workflow.
- Budget rule: at most one `rsi.py ci` poll per 4 edits; deploy (`rsi.py deploy`) only after Backend tests are green on the same sha.

## Session 67 lessons (added)

- **Verify the live bytes, not the green tick.** `python3 tools/rsi/rsi.py live` fetches the shipped CSS and checks a marker selector. Session 66 shipped "green" twice while the server kept the old CSS (zip/unzip timezone skew made `collectstatic` skip the files, see `ANDROID_STATUS.md` 376).
- **Repair command:** `python3 tools/rsi/rsi.py deploy web/static/web/css` re-copies that dir on the server (files under 1 MB only).
- **If the same bug is reported twice, stop restyling and diff production against the repo** (curl the asset, grep a selector). That took 6 tool calls and found the cause that a full session of CSS work had not.
- Pull the deploy log with the API and filter it (`grep -v "Updating files"`): the unfiltered checkout progress is 9,000 lines.

## Session 68 lessons (incident: replies endpoint 500)

**What happened.** `983bada1` (backend perf pass) added `_reply_may_have_poll` using `Reply` without importing it. Every
`GET /api/posts/<id>/replies/` for a post with at least one reply returned 500 from the first deploy after that commit
(about 20:28 UTC, 02:13 NPT on 18 Nov) until the fix deploy (`3df858d`, 22:0x UTC). Measured with
`rsi.py diagnose`: exactly one failing request in that window (one IP, one post, the account `nebians`, app 1.7.5
build 29), because the site was quiet at night. The 6 other replies 500s in the log are from 5 Nov, unrelated.

**Why nothing caught it.** (1) the audit only parsed syntax, so a missing name passed; (2) the query-budget suite
already requests that endpoint with 30 replies, but it was not in the Backend tests command; (3) `deploy` was
dispatched without checking that tests were green for the same code.

**What now stops it.**
- `rsi.py verify` and the Backend tests workflow run a pyflakes undefined-name scan over all of `backend_python`.
- `api.test_api_query_budget` and `api.test_replies_regression` are in the Backend tests command.
- `rsi.py deploy` refuses unless a green Backend tests run covers the same `backend_python` tree. `--force` is for a
  proven hotfix only. `deploy <static_dir>` (static repair) is not gated.
- `rsi.py diagnose [script]` runs a read-only `.github/scripts/*.sh` on the server and prints the filtered log in
  one call (it replaces: dispatch, poll, find job, fetch log, trim). Scripts print aggregates only: the repo is public.

**Rules.**
- Any perf or refactor commit touching `api/` needs `rsi.py verify` before the checkpoint, no exceptions.
- A new test module that matters must be added to the workflow command in the same commit.
- Never commit a transcript. `sessions.txt` held the live GitHub token twice (public repo). It is redacted in the tree,
  the token must be rotated because git history keeps it. `check_staged_secrets` catches `ghp_` in staged diffs, so
  paste transcripts only after redacting.
- Admin error emails used to dump the Redis URL with its password. `RedactingExceptionReporterFilter`
  (`nebians/log_filters.py`) now masks REDIS, CACHE, CHANNEL, DATABASE, DB_, BRIDGE, SALT and `_URL` settings.

## Session 2 post-mortem (from `sessions.txt`) and cadence for session 4 onward

- Session 2 spent about 36 `rsi.py ci` calls and 23 sleeps. Cadence now: push, do docs and tests, then poll at most
  twice; never `sleep` as the only action in a turn.
- Two failures in session 2 came from signature drift after a perf refactor (`prime_for_serializers` argument order,
  a failing test run). The undefined-name scan plus the budget suite now cover that class.
- Turn plan that fits 75 calls: 1 `pickup`; 1 `map`+read in one bash call; edits batched 2 to 4 per turn;
  `checkpoint` every 3 to 5 edits; `deploy` (gated) once; `diagnose` once; docs in the same turn as the last push.
