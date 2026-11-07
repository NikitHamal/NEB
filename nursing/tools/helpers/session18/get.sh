#!/bin/bash
cd /tmp/NEB
while IFS='|' read -r id title; do
  [ -z "$id" ] && continue
  /tmp/v/bin/python nursing/tools/assetget.py get "${SLUG:-nur13}/$id" "File:$title" 2>&1 | tail -1 | cut -c1-120
done
