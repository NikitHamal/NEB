#!/bin/bash
# usage: build_book.sh <rel e.g. semester-5/mis-and-e-business> <src dir name> <check script or -> "<commit message>"
set -e
: "${GH_PAT:?set GH_PAT in the environment (never in the repo)}"; export GIT_ASKPASS=/tmp/gitenv.sh GIT_TERMINAL_PROMPT=0 NEB_PY=/tmp/v/bin/python
cd /tmp/NEB; rel=$1; src=$2; chk=$3; msg=$4; d=bca/course/$rel; PY=/tmp/v/bin/python
rm -f $d/unit-*.md; cp /tmp/src/$src/unit-*.md $d/; cp /tmp/src/$src/README.md $d/README.md
[ "$chk" != "-" ] && $PY bca/tools/$chk --fill $d/unit-*.md
$PY bca/tools/normalize_md.py $d/unit-*.md
$PY bca/tools/fill_script_outputs.py $d/unit-*.md
if grep -q '^```java' $d/unit-*.md; then $PY bca/tools/fill_java_outputs.py $d/unit-*.md; fi
[ "$chk" != "-" ] && $PY bca/tools/$chk --verify $d/unit-*.md
$PY bca/tools/nebpdf.py course/$rel 2>&1 | tail -4
sem=$(echo $rel | sed 's/semester-\([0-9]\).*/\1/')
pdf=$(ls -t bca/course/semester-$sem/pdfs/*.pdf | head -1); echo "PDF: $pdf"
qa=$($PY bca/tools/qa_pdf.py $pdf 2>&1); echo "$qa" | tail -8
echo "$qa" | grep -q "fails=0\|0 FAIL" || { echo "QA NOT CLEAN"; exit 3; }
$PY bca/tools/gen_status.py 2>&1 | tail -2
cat $d/unit-*.md | wc -w
git add -A bca AGENTS.md
if git diff --cached | grep -qE 'ghp_[A-Za-z0-9]{20,}'; then echo "TOKEN LEAK"; exit 4; fi
git -c user.name="NEBians" -c user.email="iamnikithamal@gmail.com" commit -q -m "$msg"
git push -q origin claude/bca-entrance-complete 2>&1 | tail -2
git ls-remote origin claude/bca-entrance-complete; git log --oneline | head -1
