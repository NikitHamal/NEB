#!/bin/bash
# READ-ONLY. Calls every keyless chat provider once from the production host
# (the only place the upstream WAFs treat as a real client) and prints
# ok/FAIL, latency and the first words of each reply. Writes nothing.
cd /home/consicac/nebians_api || exit 1
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate
:
echo "== chat providers (native path, one call each)"
timeout 280 python scripts/probe_keyless_chat.py ${PROBE_ARGS:-} 2>&1 | cut -c1-260 | tail -60
