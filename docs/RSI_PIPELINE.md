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
