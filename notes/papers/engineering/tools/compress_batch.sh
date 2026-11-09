#!/bin/bash
# Compress up to N not-yet-processed big PDFs under DIR within a time budget. Usage: compress_batch.sh DIR [MIN_MB=3] [N=24] [BUDGET_S=140]
# Progress is tracked in /tmp/w/compressed.txt so repeat calls pick up where the previous left off.
D=$1; MIN=${2:-3}; N=${3:-24}; B=${4:-140}; touch /tmp/w/compressed.txt
find "$D" -name '*.tmp' -delete
find "$D" -type f -name '*.pdf' -size +${MIN}M | sort | grep -vxFf /tmp/w/compressed.txt | head -$N > /tmp/w/batch.txt
echo "batch: $(wc -l < /tmp/w/batch.txt) files; remaining before: $(find "$D" -type f -name '*.pdf' -size +${MIN}M | grep -vxFf /tmp/w/compressed.txt | wc -l)"
[ -s /tmp/w/batch.txt ] || exit 0
timeout $B python3 "$(dirname "$0")/compress.py" 0 $(cat /tmp/w/batch.txt | tr '\n' ' ') | tail -1 && cat /tmp/w/batch.txt >> /tmp/w/compressed.txt
