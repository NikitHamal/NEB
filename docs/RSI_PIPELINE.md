# NEBians RSI (Recursive Self-Improvement) Pipeline

## Purpose

Every AI engineering session operates under a strict sequential tool-call limit (75 calls) and faces potential mid-session container timeouts. Previously, 15 to 25 tool calls per session were spent on manual orientation (`git log`, reading status files, running individual linters, polling GitHub Actions) and work was vulnerable to session termination if not pushed incrementally.

`tools/rsi/rsi.py` + `tools/rsi/security_and_m3x_audit.py` compress orientation, multi-guard verification, secret-safe micro-commits, CI monitoring, and cPanel deployment into single atomic commands, multiplying effective output per session by 5 to 10x while guaranteeing zero lost work.

---

## Single-Call Commands

### 1. Session Pickup (`1 tool call` instead of `10+`)

```bash
python3 tools/rsi/rsi.py pickup
```

- Prints `git status -sb` and the last 6 commits on `main`.
- Extracts the most recent session table and `Next` items from `ANDROID_STATUS.md`.
- Queries the GitHub Actions REST API for the latest 5 workflow runs on `main` (`Build Student Release APKs & AAB`, `Backend tests`, `Deploy Backend to cPanel`).

### 2. Full Static & Security Verification (`1 tool call` instead of `6+`)

```bash
python3 tools/rsi/rsi.py verify
```

Runs in under 2 seconds without invoking Gradle locally:
1. `tools/android/check_scrollers.py` (infinite-width horizontal scroll crash guard)
2. `tools/android/check_insets.py` (status bar & top bar alignment guard)
3. `tools/android/check_sheets.py` (`NebModalSheet` padding & status bar guard)
4. `tools/android/check_text_fit.py` (unbounded `Text` in `Row` ratchet)
5. `tools/css/bundle.py --check` (verifies `m3x-app.css` and all CSS bundles are in sync)
6. `tools/rsi/security_and_m3x_audit.py` (AST syntax check on modified Python files, staged diff secret-leak detector, and core security invariant check)

### 3. Atomic Micro-Checkpoint & Push (`1 tool call` per milestone)

```bash
python3 tools/rsi/rsi.py checkpoint "concise milestone commit message"
```

- Runs `verify` first; aborts immediately if any guard or AST check fails.
- Stages changes (`git add -A`), excluding local sandbox artifacts (`package.json`).
- Scans `git diff --cached` for PATs, private keys, or API secrets (`check_staged_secrets`).
- Commits and pushes immediately to `origin main` using `/tmp/gitenv.sh`.
- **Mandatory Rule**: Run `checkpoint` after every completed logical milestone (every 3 to 5 file edits) so no work can ever be lost to a session timeout.

### 4. CI Status & Deployment Dispatch

```bash
python3 tools/rsi/rsi.py ci
python3 tools/rsi/rsi.py deploy
```

- `ci` prints the status and conclusion of the latest `main` workflow runs.
- `deploy` triggers `deploy-backend.yml` (`workflow_dispatch`) on `main` using the repository's `SSH_HOST` and `SSH_KEY` secrets.
