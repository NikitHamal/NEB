#!/bin/bash
# usage: build_book.sh <rel e.g. course/year-1/fundamentals-of-nursing> <check script (check_x.py) or -> "<commit message>"
# Runs: fill tokens -> normalise -> verify -> PDF -> qa_pdf (fails=0 required) -> commit -> push (PAT via /tmp/gitenv.sh, never in repo)
set -e -o pipefail
source /tmp/gitenv.sh
cd /tmp/NEB; rel=$1; chk=$2; msg=$3; d=nursing/$rel; PY=/tmp/v/bin/python
[ "$chk" != "-" ] && $PY nursing/tools/$chk --fill $d/unit-*.md
$PY nursing/tools/normalize_md.py $d/unit-*.md
[ "$chk" != "-" ] && $PY nursing/tools/$chk --verify $d/unit-*.md
t0=$(date +%s)
$PY nursing/tools/nebpdf.py $rel 2>&1 | tail -6
pdf=$(ls -t nursing/pdfs/*.pdf 2>/dev/null | head -1); echo "PDF: $pdf"
[ -n "$pdf" ] && [ "$(stat -c %Y "$pdf")" -ge "$t0" ] || { echo "NO FRESH PDF BUILT"; exit 5; }
qa=$($PY nursing/tools/qa_pdf.py $pdf 2>&1); echo "$qa" | tail -8
echo "$qa" | grep -E "^\[" | grep -q "fails=0" && ! echo "$qa" | grep -E "^\[" | grep -q "fails=[1-9]" || { echo "QA NOT CLEAN"; exit 3; }
cat $d/unit-*.md | wc -w
git add -A nursing AGENTS.md notes/assets
if git diff --cached | grep -qE 'ghp_[A-Za-z0-9]{20,}'; then echo "TOKEN LEAK"; exit 4; fi
git -c user.name="NikitHamal" -c user.email="iamnikithamal@gmail.com" commit -q -m "$msg"
git push -q origin claude/bsc-nursing 2>&1 | tail -2
git ls-remote origin claude/bsc-nursing; git log --oneline | head -1
