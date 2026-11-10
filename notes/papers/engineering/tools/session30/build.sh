#!/bin/bash
# usage: build.sh id...
cd /app
export PATH=/tmp/menv/bin:$PATH FONTCONFIG_PATH=/tmp/menv/etc/fonts PAPERS_CONTENT=/app/notes/papers/engineering/content PAPERS_OUT=/app/notes/papers/engineering/pdf
python3 /app/shots/asm.py "$@" || exit 1
for i in "$@"; do python3 notes/papers/engineering/tools/fixq.py notes/papers/engineering/content/$i.md >/dev/null; python3 notes/papers/build_paper.py $i 2>&1 | tail -8; done
